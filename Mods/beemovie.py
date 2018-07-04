import requests
from bs4 import BeautifulSoup

def getQuote():
  try:
    # query the website and return the html to the variable ‘page’
    quote_page = "http://wizardlywonders.xyz:3054/"
    page = requests.get(quote_page)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract the body of the website, in this case the quote.
    quote = str(soup)
    return quote
  except Exception as e:
    print("Failed to load quote.")
