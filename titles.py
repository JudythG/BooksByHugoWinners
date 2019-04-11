# comment

import hugo_winners
import json
import goodreads

# get list of winners and winning title from the Hugo site
hugo_2018_url = 'http://www.thehugoawards.org/hugo-history/2018-hugo-awards/'
winnersWithTitles = hugo_winners.getHugoWinners(hugo_2018_url)

# find books by each winnning author at goodreads
authors_and_titles_list = goodreads.getAuthorsWithTitles(winnersWithTitles)

# output structure
authors_and_titles = {'hugo_url': hugo_2018_url, 'goodreads_url': 'https://goodreads.com', 'authors_and_titles': authors_and_titles_list}

# convert data to json and write to file
f_out = open ('hugo_winners_json.txt', 'w')
f_out.write (json.dumps(authors_and_titles))

