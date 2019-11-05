#!/usr/bin/python3

import json,requests,random,datetime

def _getRedditData(sub,after):
	if after == None or after == "":
		after = ""
	else:
		after = "".join(("?after=",after))

	rawData = requests.get(f'https://www.reddit.com/r/{sub}/new/.json{after}',headers={"User-Agent":"Megumin-tan/Discord"})
	if rawData.status_code == 200:
		rawData = rawData.json()
		return {"posts": rawData["data"]["children"],"after": rawData["data"]["after"]}
	else:
		return None

def getRedditPosts(sub,np):
	data = []
	next = ""
	for i in range(0,np):
		rawData = _getRedditData(sub,next)
		if rawData != None:
			data.append(rawData["posts"])
			next = rawData["after"]
		else:
			return None
	return data

def subExists(sub):
    ping = requests.get(f'https://www.reddit.com/r/{sub}/about/.json',headers={"User-Agent":"Megumin-tan/Discord"}).json()
    if ping["kind"] == "Listing":
        return False
    else:
        return True

def fetchRedditPost(sub):
    returnData= {"successful": 0}
    if subExists(sub):
        data = getRedditPosts(sub,2)
        page = data[random.randint(0,len(data) - 1)]
        post = page[random.randint(0,len(page) - 1)]["data"]
        sub = post["subreddit"]
        author = post["author"]
        url = post["url"]
        returnData["title"] = post["title"]
        if post["is_self"] == False:
            returnData["type"] = "image"
            returnData["description"] = f'[/r/{sub}](https://old.reddit.com/r/{sub}/top/) | Posted by: [/u/{author}](https://old.reddit.com/u/{author}/)\n[[post]]({url})'
            returnData["imgurl"] = url
        else:
            returnData["type"] = "text"
            #looking for tldr. very messy. pls don't hurt me.
            tl = ["TLDR","TL;DR","TL DR","TL:DR","tldr","tl;dr","tl dr","tl:dr"]
            tldr = None
            lines = post["selftext"].split("\n")
            for line in lines:
                for t in tl:
                    if line.startswith(t):
                        tldr = line
            returnData["description"] = f'[/r/{sub}](https://old.reddit.com/r/{sub}/top/) | Posted by: [/u/{author}](https://old.reddit.com/u/{author}/)\n[[text post]]({url})'
            if tldr != None:
                returnData["description"] = f'[/r/{sub}](https://old.reddit.com/r/{sub}/top/) | Posted by: [/u/{author}](https://old.reddit.com/u/{author}/)\n[[text post]]({url})\nTL;DR - ||{tldr}||'
        returnData["successful"] = 1
        returnData["footer"] = "".join(("▲",str(post["ups"])," | Created: ",datetime.datetime.utcfromtimestamp(post["created"]).strftime("%Y-%m-%dT%H%M")))
    else:
        returnData["successful"] = 0

    return returnData
