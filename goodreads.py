import requests
from bs4 import BeautifulSoup
import nltk.tokenize

# NB: should take list of titles down to a set in case an author won more 
#     than once
def getGoodReadsAuthorSearches (titleAndAuthorList):
    search_base = 'https://www.goodreads.com/search?utf8=%E2%9C%93&q='
    search_end = '&search_type=books&search%5Bfield%5D=author'
    search_links = []

    for d in titleAndAuthorList:
        author = d['author']
        author_tokens = nltk.tokenize.word_tokenize(author)
        search_string = search_base
        for tok in author_tokens:
            search_string = search_string + tok
            if tok != author_tokens[-1]:
                search_string = search_string + '+'
        search_string = search_string + search_end
        author_and_link = {'author': author, 'search_link': search_string}
        search_links.append (author_and_link)

    return search_links

# input: dict with two elements: author's name and  author's GoodReads search page
# returns: 	dict with two elements: author's name and  url of author's main page 
#		or False
def getAuthorMainPage (authorAndLink):
    response =  requests.get(authorAndLink['search_link'])
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ele = soup.find(class_='authorName')
        d = {'author': authorAndLink['author'], 'main_page_link': ele['href']}
        return d 
    return False

# input: dict with two elements: author's name and author's main page
# returns: 	dict with two elements: author's name and author's book page
#		or False
def getAuthorBookPage (author_and_main_page):
    response = requests.get(author_and_main_page['main_page_link'])
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # more books link 
        link_list = soup.findAll(class_='actionLink')
        for link in link_list:
            if 'More books by ' in link.text:
                next_page = 'https://www.goodreads.com' + link.get('href')
                author_and_book_page = {'author': author_and_main_page['author'], 'book_page_link': next_page}
                return author_and_book_page
    return False

def getTitlesFromCurPage (url):
    titles = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        l = soup.findAll(class_='bookTitle')
        for title in l:
            if (title.span):
                titles.append(title.span.text)
    return titles

def getNextPage (url):
    next_page_url = False
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ele = soup.find(class_='next_page')
        if ele != None and ele.get('href') != None:
            return 'https://www.goodreads.com' + ele.get('href')
    return False   

def getAuthorTitles (url):
    titles = getTitlesFromCurPage (url)

    while True:
        next_page_url = getNextPage (url)
        if next_page_url == False:
            break

        url = next_page_url
        next_titles = getTitlesFromCurPage (next_page_url)
        titles = titles + next_titles
    return titles

def getAuthorsWithTitles (author_with_winning_title):
    authorSearchLinks = getGoodReadsAuthorSearches (author_with_winning_title)
    authors_and_titles_list = []
    for authorLink in authorSearchLinks:
        author_and_main_url = getAuthorMainPage(authorLink)
        if author_and_main_url != False: 
            author_titles_url = getAuthorBookPage(author_and_main_url)
            if author_titles_url != False:
                titles = getAuthorTitles(author_titles_url['book_page_link'])
                author_and_titles = {'author': author_titles_url['author'], 'titles': titles}
                authors_and_titles_list.append (author_and_titles)
    return authors_and_titles_list

