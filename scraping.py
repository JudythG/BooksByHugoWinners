import requests
from bs4 import BeautifulSoup

# scrape specified site for text associated with the given class value
# returns False if no data or error
# returns list of text items if successful
def scrapeByClass (url, classValue):
    text_list = []  # return value if successful

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.findAll(class_=classValue)
        for element in elements:
            text_list.append (element.text)
    else:
        return False
    return text_list

