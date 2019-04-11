# BooksByHugoWinners
A list of books by 2018 Hugo Award winners ![Hugo logo](Hugo_Logo_1_100px.png)

## Overview
Scrapes 2018 Awards site for winners. 
Scrapes GoodReads for titles by each winner.
Outputs results in JSON file.

## Code Files
* goodreads.py - from an html search string, returns a list of authors and their respective titles
* hugo_winners.py - from Hugo Awards 2018 site, builds list of award winners with winning titles
* scraping.py - shared scraping code
* titles.py - main file scrapes Hugo site for winners and goodreads for their respective titles. Outputs results in JSON

## Output
JSON ouptut file: hugo_winners_json.txt

All elements in output file are strings. 

JSON elements
* hugo_url - URL of the 2018 Hugo Awards site
* goodreads_url - Homepage of GoodReads
* authors_and_titles - list of dictionary elements that have two fields
*   author - author name
*   titles - list of titles by that author
