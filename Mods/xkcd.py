import urllib.request, json
from random import randint
from discord import Embed

# Feteches the JSON of the latest submission.
with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
    data = json.load(url)
   
latestComicID = data["num"]

def getLatestComic():
    imgsrc =  data["img"]
    imgtitle = data["title"]
    imgdate = data["month"]+"/" + data["day"] + "/" + data["year"]
    imgalt = data["alt"]
    
    e = Embed(color=0x7610ba)
    e.set_image(url=imgsrc)
    e.set_footer(text=imgalt)
    e.add_field(name=imgtitle, value=imgdate, inline=False)
    
    return e
    
def getRandomComic():
    
    # Generates a random number to represent the ComicID.
    randomComicID = randint(1, latestComicID)
    
    
    # Fetches the JSON and returns the image.
    with urllib.request.urlopen("http://xkcd.com/" + str(randomComicID) + "/info.0.json") as randomUrl:
        data = json.load(randomUrl)
        
    imgsrc =  data["img"]
    imgtitle = data["title"]
    imgdate = data["month"]+"/" + data["day"] + "/" + data["year"]
    imgalt = data["alt"]
    
    e = Embed(color=0x7610ba)
    e.set_image(url=imgsrc)
    e.set_footer(text=imgalt)
    e.add_field(name=imgtitle, value=imgdate, inline=False)
    
    return e
    
def getComic(comicID):
    
    e = None
    
    if comicID > 1 and comicID <= latestComicID:
        # Comic ID is valid.
        
        with urllib.request.urlopen("http://xkcd.com/" + str(comicID) + "/info.0.json") as comicUrl:
            data = json.load(comicUrl)
            
            imgsrc =  data["img"]
            
        imgtitle = data["title"]
        imgdate = data["month"]+"/" + data["day"] + "/" + data["year"]
        imgalt = data["alt"]
        
        e = Embed(color=0x7610ba)
        e.set_image(url=imgsrc)
        e.set_footer(text=imgalt)
        e.add_field(name=imgtitle, value=imgdate, inline=False)
    
    return e