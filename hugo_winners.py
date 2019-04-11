# from hugo awards site, get list of winners and their titles

import nltk.tokenize
import scraping

# input: list of strings that map to winners from the Hugo Awards site
# JTG: format of winners lines describe
# Assumptions:
#   For now, only one author per work
def getWinnersOfInterest (winners):
    to_remove = []
    for winner in winners:
        if 'by' not in winner:
            to_remove.append (winner)
        elif 'screenplay' in winner:
            to_remove.append (winner)
        elif 'directed' in winner:
            to_remove.append (winner)
        elif 'edited' in winner:
            to_remove.append (winner)
        elif 'presented' in winner:
            to_remove.append (winner)

        # JTG: put back when move up to multiple authors
        elif 'illustrated' in winner:
            to_remove.append (winner)
    for rem in to_remove:
        winners.remove(rem)

# Note: I need to look into NLP futher. Must be a better way to parse
def parseWinners (winners):
    titleAndAuthorList= []	# return value

    for winner in winners:
        tokens = nltk.tokenize.word_tokenize(winner)

        title = ''
        author = ''
        titleAndAuthor = {}

        for token in tokens:
            # title ends at a comma
            # assumes no comma in the title!
            if token == ',':
                break

            # remove double leading quotes
            elif token[0].isalpha() == False:
                continue
                
            title = title + ' ' + token

        authorStart = False
        for token in tokens:
            if token.strip() == '(':
                break
            elif authorStart == True:
                author = author + ' ' + token
            elif token.strip() == 'by':
                authorStart = True

        authorAndTitle = {'title': title.strip(), 'author': author.strip()}
        titleAndAuthorList.append (authorAndTitle)

    return titleAndAuthorList

def getHugoWinners(url):
    winners = scraping.scrapeByClass (url, 'winner')
    getWinnersOfInterest (winners)
    winnersWithTitles = parseWinners(winners)
    return winnersWithTitles
