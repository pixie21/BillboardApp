#!/bin/sh
import billboard
import json
import os
import sys
from flask import abort, request
from flask import Flask, jsonify
from itertools import groupby
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import requests
import spotipy
import webbrowser
import spotipy.util as util
from simplejson.decoder import JSONDecodeError
import datetime
import schedule
import time
from datetime import datetime, timedelta
from threading import Timer



#new variables
scope = "user-library-read playlist-modify-public playlist-modify-private"
spotify_client_id ='5de3031a97104148b06c9b93920b690b'
spotify_client_secret ='1c4f5105f76347de97fafa27b06d5ce5'
playlistID = '7gvWfcV32aaYMwhqWFRhWU'


app=Flask (__name__)

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID='5de3031a97104148b06c9b93920b690b'
SPOTIPY_CLIENT_SECRET='1c4f5105f76347de97fafa27b06d5ce5'
SPOTIPY_REDIRECT_URI='http://google.com/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
username='gr8okntjqo4j637vrz5ub7p8q'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

token = util.prompt_for_user_token(username, scope, client_id=spotify_client_id,client_secret=spotify_client_secret,
                                       redirect_uri='http://google.com/')
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']


chart = billboard.ChartData('hot-100')
chartartist= billboard.ChartData('artist-100')
chartrap= billboard.ChartData('r-b-hip-hop-songs')
chartpop = billboard.ChartData('pop-songs')
chartrock = billboard.ChartData('rock-songs')
chartchina= billboard.ChartData('billboard-china-social-chart')
chartholiday= billboard.ChartData('hot-holiday-songs')
chartlatin = billboard.ChartData('latin-songs')
chartdance = billboard.ChartData('dance-electronic-songs')
chartgoat = billboard.ChartData('greatest-hot-100-singles')
chartcountry = billboard.ChartData('country-songs')
chartgospel = billboard.ChartData('christian-songs')
chart200= billboard.ChartData('billboard-200')
i=0;
songs=[]
artists=[]
weeks=[]
peakPos=[]
rank=[]
lastPos=[]
isNew=[]
imgs=[]






while i<99:
    song=chart[i]
    billboardlisting=chart[i]
    aTitle={"title":song.title}
    aArtist={"title":song.artist}
    aWeeks={"title":song.weeks}
    aPeakPos={"title":song.peakPos}
    aRank={"title":song.rank}
    aLastPos={"title":song.lastPos}
    aIsNew={"title":song.isNew}



    songs.append(aTitle)
    artists.append(aArtist)
    weeks.append(aWeeks)
    peakPos.append(aPeakPos)
    rank.append(aRank)
    lastPos.append(aLastPos)
    isNew.append(aIsNew)

    i=i+1


'''PLAYLSIT CODE'''
def get_tracks_in_discover_weekly(sp):
    rawpl = sp.user_playlist('spotify', playlistID)['tracks']
    track_ids = []
    for i, item in enumerate(rawpl['items']):
        track_ids.append(item['track']['id'])

    return track_ids





def test(sp):
    trackss=['5NkfVQS8BkceRgoSQwcW6H']
    return trackss

def create_empty_playlist(sp):
    sp.trace = False
    now = 'Billboard Favorites'
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == now:
            return playlist['id']
        else:
            name = now
            sp.user_playlist_create(username, name, True)
            return playlist['id']


#FOR APP ROUTES


@app.route('/chart')
def getcharturlextension():
    exten= request.args['exten']
    approute='/'
    approute=approute+exten
    chart = billboard.ChartData(exten)
    return redirectcharfunction(exten)


@app.route('/chartt')
def getpreviouschart():
    exten= request.args['exten']
    approute='/'
    approute=approute+exten
    chart = billboard.ChartData(exten)
    return contentReadhot100(chart) #contentSongs()

def redirectcharfunction(chartname):
    if chartname=='hot-100':
        return contentSongs()
    elif chartname=='r-b-hip-hop-songs':
        return contentRap()
    elif chartname=='artist-100':
        return contentArtists()
    elif chartname=='pop-songs':
        return contentPop()
    elif chartname=='rock-songs':
        return contentRock()
    elif chartname=='billboard-china-social-chart':
        return 'coming soon'
    elif chartname=='holiday-songs':
        return contentholiday()
    elif chartname=='latin-songs':
        return contentLatin()
    elif chartname=='dance-electronic-songs':
        return contentDance()
    elif chartname=='greatest-hot-100-singles':
        return contentGoat()
    elif chartname=='country-songs':
        return contentCountry()
    elif chartname=='christian-songs':
        return contentChristian()
    elif chartname=='all-charts':
        contentSongs().start
        return''

    else:
        return 'Error in chart name'

def contentReadhot100(x):
    x=str(x)
    x=x.split("-")[0].strip()
    x="out"+x+".json"
    print(x)
    f=open(x,"r")
    if f.mode=="r":
        contents = f.read()
    return (contents)




tracksavailable = 0
tracksnotavailable = 0
tracksduplicate = 0
prev_playlist = [] #track uris of playlist already on spotify
track_ids = [] #track uris we will add to the playlist

#sp = spotipy.Spotify()
songs=['the jam a town called malice\n', 'ramones i wanna be sedated\n', 'nirvana the man who sold the world\n', 'the police roxanne\n', 'ray lamontagne jolene\n']


@app.route('/ss')
#search spotify for each track, determining if it is available and if so, whether it is a duplicate
def searchspot():
    global tracksavailable
    global tracksnotavailable
    global tracksduplicate
    global track_ids
    global results
    global songs

    artis= request.args['artis']
    trac= request.args['trac']
    glowbalist=[]
    glowbal = artis + ' ' +trac
    glowbalist.append(glowbal)

    #format for the return
    #http://192.168.56.1:5001/ss?artis=alie&trac=itworktobbc


    token = util.prompt_for_user_token(username, scope, client_id=spotify_client_id,client_secret=spotify_client_secret,
                                       redirect_uri='http://localhost:8080')
    sp = spotipy.Spotify(auth=token)



    songs=['kendrick lamar mona lisa\n', 'future poa\n','pumzfifinna sjj\n','kendrick lamar the spiteful chant\n', 'nirvana the man who sold the world\n', 'the police roxanne\n', 'ray lamontagne jolene\n']
    Tracks=[]
    for name in glowbalist:
        print("searching for " + name)
        results = sp.search(q=name, type='track')
        try: #check if song exists on spotify
            trackURI = results['tracks']['items'][0]['uri']
            Tracks.append(trackURI)
            if trackURI not in track_ids and trackURI not in prev_playlist:
                track_ids.append(trackURI)
                tracksavailable+=1
            else:
                print("**Duplicate track**\n")
                tracksduplicate+=1
        except IndexError:
            print("**Track not available**\n")
            tracksnotavailable+=1
    print (Tracks)
    new_playlist = create_empty_playlist(sp)
    sp.user_playlist_add_tracks(username, new_playlist, Tracks)
    return 'g'




@app.route('/bb100')
#def contentSongs(x):
def contentSongs():
    lst=[]
    text=open('bill.txt', 'w+')
    i=0;
    while i<100:
        song=chart[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split(" x")[0].strip()
        y=y.split("& ")[0].strip()
        y=y.split(" + ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist = y['artists']['items'][0]
        img=(artist['images'][0]['url'])


        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('bill.txt') as f, open("outhot.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")
    return 'success'



@app.route('/ba100')
def contentArtists():
    lst=[]
    text=open('artists.txt', 'w+')
    i=0;
    while i<21:
        song=chartartist[i]
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('artists.txt') as f, open("outartist.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")

    return 'success'

@app.route('/bbrap')
def contentRap():
    lst=[]
    text=open('billrap.txt', 'w+')
    i=0;
    while i<50:
        song=chartrap[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billrap.txt') as f, open("outr.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")
    return 'success'

@app.route('/bbpop')
def contentPop():
    lst=[]
    text=open('billpop.txt', 'w+')
    i=0;
    while i<40:
        song=chartpop[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billpop.txt') as f, open("outpop.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'
@app.route('/bbrock')
def contentRock():
    lst=[]
    text=open('billrock.txt', 'w+')
    i=0;
    while i<44:
        song=chartrock[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billrock.txt') as f, open("outrock.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'

@app.route('/bblatin')
def contentLatin():
    lst=[]
    text=open('billlatin.txt', 'w+')
    i=0;
    while i<5:
        song=chartlatin[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billlatin.txt') as f, open("outlatin.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'

@app.route('/bbdance')
def contentDance():
    lst=[]
    text=open('billdance.txt', 'w+')
    i=0;
    while i<23:
        song=chartdance[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billdance.txt') as f, open("outdance.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'

@app.route('/bbgoat')
def contentGoat():
    lst=[]
    text=open('billgoat.txt', 'w+')
    i=0;
    while i<33:
        song=chartgoat[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billgoat.txt') as f, open("outgreatest.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'

@app.route('/bbcountry')
def contentCountry():
    lst=[]
    text=open('billcountry.txt', 'w+')
    i=0;
    while i<23:
        song=chartcountry[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billcountry.txt') as f, open("outcountry.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'










def spotimage(artist):
    y=artist.split("Featuring")[0].strip()
    y=y.split(", ")[0].strip()
    y=y.split("X ")[0].strip()
    y=y.split("& ")[0].strip()
    y=y.split(" (")[0].strip()
    searchResults=spotifyObject.search(y,1,0,"artist")
    y=searchResults

    substring = 'scdn'


    artist= searchResults['artists']['items'][0]
    img=(artist['images'][0]['url'])

    img=str(img)
    if substring in img:
            img=(artist['images'][0]['url'])
            img=str(img)
    else:
        img=['http://worldartistsmanagement.com/wp-content/uploads/2017/04/1488554638.original-600x600.png']
        img=str(img)

    return(img)

def spottimage(artist):
    y=artist.split("Featuring")[0].strip()
    y=y.split(", ")[0].strip()
    y=y.split("X ")[0].strip()
    y=y.split("& ")[0].strip()
    y=y.split(" (")[0].strip()
    searchResults=spotifyObject.search(y,1,0,"artist")
    y=searchResults

    substring = 'scdn'


    try:
        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])
        img=str(img)
        return (img)

    except:
        img='http://worldartistsmanagement.com/wp-content/uploads/2017/04/1488554638.original-600x600.png'
        img=str(img)
        return (img)


@app.route('/bbchristian')
def contentChristian():
    lst=[]
    text=open('billchristian.txt', 'w+')
    i=0;
    while i<50:
        song=chartgospel[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(spottimage(aArtist))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billchristian.txt') as f, open("out.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    return 'success'

@app.route('/bbholiday')
def contentholiday():
    lst=[]
    text=open('billholiday.txt', 'w+')
    i=0;
    while i<14:
        song=chartholiday[i]
        aTitle=song.title
        aArtist=song.artist
        aWeeks=song.weeks
        aPeakPos=song.peakPos
        aRank=song.rank
        aLastPos=song.lastPos
        aIsNew=song.isNew

        xxx=aArtist

        y=xxx.split("Featuring")[0].strip()
        y=y.split(", ")[0].strip()
        y=y.split("X ")[0].strip()
        y=y.split("& ")[0].strip()
        searchResults=spotifyObject.search(y,1,0,"artist")
        y=searchResults


        artist= searchResults['artists']['items'][0]
        img=(artist['images'][0]['url'])

        text.write(str(aTitle+"\n"))
        text.write(str(aArtist+"\n"))
        text.write(str(aWeeks))
        text.write("\n")
        text.write(str(aPeakPos))
        text.write("\n")
        text.write(str(aRank))
        text.write("\n")
        text.write(str(aLastPos))
        text.write("\n")
        text.write(str(aIsNew))
        text.write("\n")
        text.write(str(img))
        text.write("\n")
        text.write("|-"+"\n")

        i=i+1
    text.close()
    names=["title","artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('billholiday.txt') as f, open("outholiday.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")
    f=open("out.json","r")
    if f.mode=="r":
        contents = f.read()
    return 'success'



@app.route('/check')
def contentSogs():
    x='pants'
    return x





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=False)
