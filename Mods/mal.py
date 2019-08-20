#!/usr/bin/python3
#Made by Tomo-Nyan

import requests,datetime, urllib
from time import sleep
api = 'https://api.jikan.moe/v3'
lastRequest = datetime.datetime.utcnow().timestamp()

def RLRequest(url):
    global lastRequest
    while lastRequest == 0:
        sleep(0.5)
    time = datetime.datetime.utcnow().timestamp()
    lr = lastRequest + 2
    lastRequest = 0
    if time < lr:
        sleep(lr - time)
    response = requests.get(url,headers={'User-Agent':'Megumin-Tan/Discord'})
    lastRequest = datetime.datetime.utcnow().timestamp()
    return response

def fetchAnime(id):
    response = RLRequest(f'{api}/anime/{id}')
    result = {}
    if response.status_code == 200:
        data = response.json()
        result = _fetchAMShared(data,result)
        result['request_status'] = 1
        aStatus = False
        if 'title' in result:
            title = result['title']
        elif 'title_ja' in result:
            title = result['title_ja']
        if 'type_mal' in result and title != None:
            result['title_formatted'] = f'[A/{id}][{result["type_mal"]}][{title}]'
        if 'airing' in data:
            result['airing'] = data['airing']
            if data['airing'] and result['status']:
                result['airing_status'] = f'`{result["status"]}`'
                aStatus = True
            elif data['airing']:
                result['airing_status'] = '`unknown`'
                aStatus = True
        if 'aired' in data:
            if 'from' in data['aired']:
                if data['aired']['from']:
                    result['started'] = data['aired']['from'].split('T')[0]
            if 'to' in data['aired']:
                if data['aired']['to']:
                    result['ended'] = data['aired']['to'].split('T')[0]
            if aStatus == False and data['airing'] == False:
                if 'started' in result:
                    if result['started']:
                        if 'ended' in result:
                            if result['ended']:
                                result['airing_status'] = f'Aired `{result["started"]}` to `{result["ended"]}`'
                            else:
                                result['airing_status'] = f'Started Airing `{result["started"]}`'
                        else:
                            result['airing_status'] = f'Started Airing `{result["started"]}`'
                    else:
                        result['airing_status'] = f'`{data["status"]}`'
                else:
                    result['airing_status'] = f'`{data["status"]}`'
        if 'licensors' in data:
            result['licensors'] = []
            for licensor in data['licensors']:
                result['licensors'].append(licensor['name'])
            if len(result['licensors']) == 0:
                result['licensors'] = ['None']
        if 'studios' in data:
            result['studios'] = []
            for studio in data['studios']:
                result['studios'].append(studio['name'])
            if len(result['studios']) == 0:
                result['studios'] = ['None']
        if 'source' in data:
            result['origin'] = data['source']
    else:
        result['request_status'] = _responseParse(response)
    return result

def _responseParse(response):
    if response.status_code == 400: #invalid request
        print('[ERROR][mal.py] 400 Invalid Request')
        return 3
    elif response.status_code == 404: #mal not found
        print('[ERROR][mal.py] 404 Not Found')
        return 4
    elif response.status_code == 405: #invalid request
        print('[ERROR][mal.py] 405 Invalid Request')
        return 5
    elif response.status_code == 429: #rate limited
        print('[ERROR][mal.py] 429 Rate Limited')
        return 6
    elif response.status_code == 500: #cunt's fucked
        print('[ERROR][mal.py] 500 Internal Server Error')
        return 7
    else:
        return 0

def fetchManga(id):
    response = RLRequest(f'{api}/manga/{id}/')
    if response.status_code == 200:
        data = response.json()
        result = _fetchAMShared(data,{})
        result['request_status'] = 1
        pStatus = False
        if 'title' in result:
            title = result['title']
        elif 'title_ja' in result:
            title = result['title_ja']
        if 'type_mal' in result and title != None:
            result['title_formatted'] = f'[M/{id}][{result["type_mal"]}][{title}]'
        if 'publishing' in data:
            result['publishing'] = data['publishing']
            if data['publishing'] and result['status']:
                result['publishing_status'] = result['status']
                pStatus = True
            elif data['publishing']:
                result['publishing_status'] = 'unknown'
                pStatus = True
        if 'published' in data:
            if 'from' in data['published']:
                if data['published']['from']:
                    result['started'] = data['published']['from'].split('T')[0]
            if 'to' in data['published']:
                if data['published']['to']:
                    result['ended'] = data['published']['to'].split('T')[0]
            if pStatus == False and data['publishing'] == False:
                if 'started' in result:
                    if result['started']:
                        if 'ended' in result:
                            if result['ended']:
                                result['publishing_status'] = f'Published {result["started"]} to {result["ended"]}'
                            else:
                                result['publishing_status'] = f'Started Publishing {result["started"]}'
                        else:
                            result['publishing_status'] = f'Started Publishing {result["started"]}'
                    else:
                        result['publishing_status'] = data['status']
                else:
                    result['publishing_status'] = data['status']
        if 'authors' in data:
            result['authors'] = []
            for author in data['authors']:
                result['authors'].append(author['name'])
    else:
        result['request_status'] = _responseParse(response)
    return result

def _fetchAMShared(data,initialResult): #this sets the properties that both anime and manga pages use, to save space.
    result = initialResult
    if 'url' in data:
        result['page_url'] = data['url']
    if 'image_url' in data:
        result['thumb_url'] = data['image_url']
    if 'title' in data:
        result['title'] = data['title']
    if 'title_japanese' in data:
        result['title_ja'] = data['title_japanese']
    if 'type' in data:
        result['type_mal'] = data['type']
    if 'episodes' in data:
        result['episodes'] = data['episodes']
    elif 'chapters' in data:
        result['chapters'] = data['chapters']
    if 'status' in data:
        result['status'] = data['status']
    if 'synopsis' in data:
        result['synopsis'] = data['synopsis']
    if 'genres' in data:
        genres = []
        for genre in data['genres']:
            genres.append(genre['name'])
        result['genres'] = genres
    return result

def search(query,type):
    query = urllib.parse.quote(query)
    response = RLRequest(f'{api}/search/{type}?q={query}&page=1&limit=8')
    if response.status_code == 200:
        data = response.json()
        result = []
        if data['results']:
            if len(data['results']) > 0:
                for searchResult in data['results']:
                    if searchResult['type'].lower() != 'music':
                        result.append([searchResult['title'],searchResult['type'],searchResult['image_url'],searchResult['mal_id']])
                result = [1,result]
            else:
                result = ['NR']
        else:
            result = ['NR']
    else:
        result = [_responseParse(response)]
    return result
