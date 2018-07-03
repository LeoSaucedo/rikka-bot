import urllib2
from bs4 import BeautifulSoup

def getQuote():
  try:
    # query the website and return the html to the variable ‘page’
    quote_page = "http://wizardlywonders.xyz:3054/"
    page = urllib2.urlopen(quote_page)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, ‘html.parser’)

    # Extract the body of the website, in this case the quote.
    quote = soup.find('body').text.strip()
    return quote
  except exception as e:
    print("Failed to load quote.")
