#!/bin/sh
import billboard #API to get top tracks
import json
import os
import sys
from flask import abort, request #for flask server
from flask import Flask, jsonify, render_template, url_for, flash, redirect #for flask server
from itertools import groupby
from bs4 import BeautifulSoup #for scraping data from Websites
#from html.parser import HTMLParser
from HTMLParser import HTMLParser
import requests
#import time #used for the scheduler
#import atexit #used for the scheduler
#from apscheduler.schedulers.background import BackgroundScheduler#used for the scheduler
import spotipy
import webbrowser #open results in a webbrowser
import spotipy.util as util #Spotify API
from simplejson.decoder import JSONDecodeError
import datetime
#new import
import schedule #Used to set a time for the program to be updated on a weekly basis
import time
from datetime import datetime, timedelta
from threading import Timer


from flask_sqlalchemy import SQLAlchemy #new for sql alchemy database





#run spotify api scripts to be granted developer access to the API
'''
os.system("'export SPOTIPY_CLIENT_ID='5de3031a97104148b06c9b93920b690b'")
os.system("'export SPOTIPY_CLIENT_SECRET='1c4f5105f76347de97fafa27b06d5ce5'")
os.system("'export SPOTIPY_REDIRECT_URI='http://google.com/'")
'''


#export SPOTIPY_CLIENT_ID='5de3031a97104148b06c9b93920b690b'
#export SPOTIPY_CLIENT_SECRET='1c4f5105f76347de97fafa27b06d5ce5'
#export SPOTIPY_REDIRECT_URI='http://google.com/'


#new variables
scope = "user-library-read playlist-modify-public playlist-modify-private"
spotify_client_id ='5de3031a97104148b06c9b93920b690b'
spotify_client_secret ='1c4f5105f76347de97fafa27b06d5ce5'
playlistID = '7gvWfcV32aaYMwhqWFRhWU'


app=Flask (__name__)

'''added'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):

        return "User('{user}', '{eemail}', '{image}')".format(user =self.username,eemail=self.email,image=self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable= False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


#test for adding
def add():
    u=User('tester','woiyoi@test.com','password')
    db_session.add(u)
    db_session.commit()





PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID='5de3031a97104148b06c9b93920b690b'
SPOTIPY_CLIENT_SECRET='1c4f5105f76347de97fafa27b06d5ce5'
#SPOTIPY_REDIRECT_URI='http://localhost:8080'
SPOTIPY_REDIRECT_URI='http://google.com/'
#export SPOTIPY_CLIENT_ID='5de3031a97104148b06c9b93920b690b'
#export SPOTIPY_CLIENT_SECRET='1c4f5105f76347de97fafa27b06d5ce5'
#export SPOTIPY_REDIRECT_URI='http://google.com/'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
username='gr8okntjqo4j637vrz5ub7p8q'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

token = util.prompt_for_user_token(username, scope, client_id=spotify_client_id,client_secret=spotify_client_secret,
                                       redirect_uri='http://google.com/')
#token = util.prompt_for_user_token(username, scope) # add scope
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
@app.route('/updatechart/all')
def getallCharts():
    return contentSongs(), contentRap(),contentArtists(),contentPop(),contentRock(),contentholiday(),contentLatin(),contentDance(),contentGoat(),contentCountry(),contentChristian()



@app.route('/updatechart')
def getcharturlextension():
    exten= request.args['exten']
    approute='/'
    approute=approute+exten
    chart = billboard.ChartData(exten)

    return redirectcharfunction(exten)




@app.route('/getchart')
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
    elif chartname=='hot-holiday-songs':
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


    else:
        return 'Error in chart name'

def contentReadhot100(x):

    x=str(x)
    x=x.split("-")[0].strip()
    x="out"+x+".json"
    #x="outtut.json"
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

#test list of songs
#songs=['the jam a town called malice\n', 'ramones i wanna be sedated\n', 'nirvana the man who sold the world\n', 'the police roxanne\n', 'ray lamontagne jolene\n']


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
            #trackURI = trackURI.replace('spotify:track:', '')
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

def contentSongs():
    lst=[]
    text=open('billhott.txt', 'w+')
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
    with open ('billhott.txt') as f, open("outhot.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outhot.json"
    trunkss(file)

    return 'success'

def trunkss(file):
    with open(file, 'rb+') as f:
        f.seek(0,2)                 # end of file
        #f.seek(-2)
        size=f.tell()               # the size...
        f.truncate(size-3)          # truncate at that size - how ever many characters
        #f.write(']')
    with open(file, 'a+') as f:
        f.write(']')


@app.route('/ba100')
def contentArtists():
    lst=[]
    text=open('artists.txt', 'w+')
    i=0;
    while i<100:
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
    names=["artist","weeks","peakPos","rank","lastPos","isNew","url"]
    with open ('artists.txt') as f, open("outartist.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")


    file="outartist.json"
    trunkss(file)
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
    with open ('billrap.txt') as f, open("outr.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outr.json"
    trunkss(file)
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
    with open ('billpop.txt') as f, open("outpop.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outpop.json"
    trunkss(file)


    return 'success'


@app.route('/bbrock')
def contentRock():
    lst=[]
    text=open('billrock.txt', 'w+')
    i=0;
    while i<50:
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

    with open ('billrock.txt') as f, open("outrock.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outrock.json"
    trunkss(file)


    return 'success'

@app.route('/bblatin')
def contentLatin():
    lst=[]
    text=open('billlatin.txt', 'w+')
    i=0;
    while i<50:
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
    with open ('billlatin.txt') as f, open("outlatin.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outlatin.json"
    trunkss(file)

    return 'success'

@app.route('/bbdance')
def contentDance():
    lst=[]
    text=open('billdance.txt', 'w+')
    i=0;
    while i<50:
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
    with open ('billdance.txt') as f, open("outdance.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outdance.json"
    trunkss(file)

    return 'success'

@app.route('/bbgoat')
def contentGoat():
    lst=[]
    text=open('billgoat.txt', 'w+')
    i=0;
    while i<100:
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
    with open ('billgoat.txt') as f, open("outgreatest.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outgreatest.json"
    trunkss(file)

    return 'success'

@app.route('/bbcountry')
def contentCountry():
    lst=[]
    text=open('billcountry.txt', 'w+')
    i=0;
    while i<50:
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
    with open ('billcountry.txt') as f, open("outcountry.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outcountry.json"
    trunkss(file)
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

    with open ('billchristian.txt') as f, open("outchristian.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")

    file="outchristian.json"
    trunkss(file)

    return 'success'



@app.route('/bbholiday')
def contentholiday():
    lst=[]
    text=open('billholiday.txt', 'w+')
    i=0;
    while i<100:
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
    with open ('billholiday.txt') as f, open("outholiday.json", "w+") as out:
        out.write("[")
        grouped= groupby(map(str.rstrip,f), key=lambda x: x.startswith("|-"))
        for k,v in grouped:
            if not k:
                json.dump(dict(zip(names,v)),out)
                out.write(",\n")
        out.write("]")


    file="outholiday.json"
    trunkss(file)

    return 'success'



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




@app.route('/check')
def contentSogs():
    x='pants'
    return x





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=False)
