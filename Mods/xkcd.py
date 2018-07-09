import urllib.request, json
from random import randint
from discord import Embed

def getLatestComicData():
    # Feteches the JSON of the latest submission.
    with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
        data = json.load(url)
        return data

def getLatestComic():
    data = getLatestComicData()
    
    imgsrc =  data["img"]
    
    return _formatComic(data,imgsrc)
    
def getRandomComic():
    latest = getLatestComicData()
    
    # Generates a random number to represent the ComicID.
    randomComicID = randint(1, latest["num"])
    
    
    # Fetches the JSON and returns the image.
    with urllib.request.urlopen("http://xkcd.com/" + str(randomComicID) + "/info.0.json") as randomUrl:
        data = json.load(randomUrl)
        
    imgsrc =  data["img"]

    return _formatComic(data,imgsrc)
    
def getComic(comicID):
    latest = getLatestComicData()
    
    e = None
    
    if comicID > 1 and comicID <= latest["num"]:
        # Comic ID is valid.
        
        with urllib.request.urlopen("http://xkcd.com/" + str(comicID) + "/info.0.json") as comicUrl:
            data = json.load(comicUrl)
            
            imgsrc =  data["img"]
    
    return _formatComic(data,imgsrc)

def _formatComic(data,imgsrc):
    imgtitle = data["title"]
    imgdate = "".join((data["year"],"-",data["month"],"-",data["day"]))
    imgalt = data["alt"]
    
    e = Embed(color=0x7610ba)
    e.set_image(url=imgsrc)
    e.set_footer(text=imgalt)
    e.add_field(name=imgtitle, value=imgdate, inline=False)
        
    return e
