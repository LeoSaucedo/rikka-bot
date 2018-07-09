import urllib.request
import json
from random import randint

# Feteches the JSON of the latest submission.
with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
    data = json.load(url)
   
latestComicID = data["num"]

def getLatestComic():
    return data["img"]

def getRandomComic():
    
    # Generates a random number to represent the ComicID.
    randomComicID = randint(1, latestComicID)
    
    
    # Fetches the JSON and returns the image.
    with urllib.request.urlopen("http://xkcd.com/" + str(randomComicID) + "/info.0.json") as randomUrl:
        data = json.load(randomUrl)
        
    return data["img"]
    
def getComic(comicID):
    
    imageUrl = None
    
    if comicID > 1 and comicID <= latestComicID:
        # Comic ID is valid.
        
        with urllib.request.urlopen("http://xkcd.com/" + str(comicID) + "/info.0.json") as comicUrl:
            data = json.load(comicUrl)
        imageUrl = data["img"]
        
    return imageUrl