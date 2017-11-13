#Last FM Playlist Generator
#
#Ask about
#0 - need to auth, ask for last.fm user and pass
#1 - How many top tracks, artists, and tags to choose from
#2 - Choose from overall, this month, and random historical month
#3 - Go grab em!
#    a - Sort and deduplicate artist - tracks
#    b - Sort and deduplicate artist
#    c - Sort and deduplicate tags
#
#4 - Later, create a player that hooks up with spotify, tidal, grooveshark, etc...
#    a - create a player function for these guys
#    b - in the playlist acquisition, be picky if the artist - title is not an EXACT match, try another service
#    c - anyway we can get this on sonos? shouldn't be too hard, sonos is kinda already set up for this
#

#Better last.fm recommends
import pylast
import os
import datetime
import time
import random
import sys
import webbrowser
# -*- coding: utf-8 -*-

#Get necessary variables
print("Usage: 'python3 recommends.py USERNAME PASSWORD APIKEY APISECRET'")
if len(sys.argv) >= 2:
	username = str(sys.argv[1]).replace(" ","")
else:
	username = str(input("Last.FM username: "))
if len(sys.argv) >= 3:
	password_hash = pylast.md5(str(sys.argv[2]))
else:
	password_hash = pylast.md5(input("Last.FM password: "))
if len(sys.argv) >= 4:
	API_KEY = str(sys.argv[3])
else:
	API_KEY = str(input("Last.FM API Key: "))
if len(sys.argv) >= 5:
	API_SECRET = str(sys.argv[4])
else:
	API_SECRET = str(input("Last.FM API Secret: "))

#webbrowser.open("http://www.last.fm/api/auth/?api_key="+API_KEY+"&token=, new=0, autoraise=True)

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
print(network.session_key)
exit()
authuser = network.get_authenticated_user()
seed = int()
num = int()

# Test Vars
#song = network.get_track("Rancid", "Junkie Man")

def getmytracks(num):
    tracks = []
    for x in authuser.get_top_tracks()[0:num]:
        song = (str(x[0]))
        if song not in tracks:
            tracks.append(song)
    return(tracks)

def getmyweeklytracks(num):
    tracks = []
    for x in authuser.get_weekly_track_charts()[0:num]:
        song = str(x[0])
        if song not in tracks:
            tracks.append(song)
    return(tracks)

def getmyweeklyhistoricaltracks(startdate, num):
    tracks = []
    for x in authuser.get_weekly_track_charts(from_date=int(startdate), to_date=(int(startdate + 604800)))[0:num]:
        song = str(x[0])
        if song not in tracks:
            tracks.append(song)
    return(tracks)

def getartisttracks(artist, num):
    tracks = []
    group = network.get_artist(artist)
    for x in group.get_top_tracks()[0:num]:
        song = (str(x[0]))
        if song not in tracks:
            tracks.append(song)
    return(tracks)

def gettracktracks(song, num):
    tracks = []
    for x in song.get_similar()[0:num]:
        track = str(x[0])
        if track not in tracks:
            tracks.append(track)
    return(tracks)

def gettagtracks(tag, num):
    tracks = []
    tags = network.get_tag(tag)
    for x in tags.get_top_tracks()[0:num]:
        song = (str(x[0]))
        if song not in tracks:
            tracks.append(song)
    return(tracks)

def gettagsfromsong(song, num):
    tags = []
    for x in song.get_top_tags()[0:num]:
        tag = str(x[0])
        if tag not in tags:
            tags.append(tag)
    return(tags)


def getartist(song):
    artist = str(song).split(" - ")[0]
    return(artist)

def gettitle(song):
    title = str(song).split(" - ")[1]
    return(title)

def converttosong(artist, title):
    return(network.get_track(artist, title))

def addtoplaylist(song):
    global busy
    if busy%2 == 0:
        print("-", end='')
    else:
        print("o", end='')
    busy += 1
    global playlist
    artist = getartist(song)
    title = gettitle(song)
    track = artist + " - " + title
    #track = title + " - " + artist
    if track not in playlist:
        tracknl = track+"\n"
        open(file, "a+b").write(tracknl.encode('utf-8'))
        open(file, "a+b").close
        playlist.append(track)

def getalltracks(song, num):
    artist = getartist(song)
    title = gettitle(song)
    song = converttosong(artist, title)
    tags = gettagsfromsong(song, depth)
    addtoplaylist(song)
    for a in getartisttracks(artist, num):
        addtoplaylist(a)
    for b in gettracktracks(song, num):
        addtoplaylist(b)
    for c in tags:
        for d in gettagtracks(c, num):
            addtoplaylist(d)
    for e in gettracktracks(song, num):
        artist = getartist(e)
        title = gettitle(e)
        song = converttosong(artist, title)
        tags = gettagsfromsong(song, depth)
        for f in getartisttracks(artist, num):
            addtoplaylist(f)
        for g in gettracktracks(song, num):
            addtoplaylist(g)
        for h in tags:
            for i in gettagtracks(h, num):
                addtoplaylist(i)
    for e in getartisttracks(artist, num):
        artist = getartist(e)
        title = gettitle(e)
        song = converttosong(artist, title)
        tags = gettagsfromsong(song, depth)
        for f in getartisttracks(artist, num):
            addtoplaylist(f)
        for g in gettracktracks(song, num):
            addtoplaylist(g)
        for h in tags:
            for i in gettagtracks(h, num):
                addtoplaylist(i)
    for e in tags:
        for z in gettagtracks(e, num):
            artist = getartist(z)
            title = gettitle(z)
            song = converttosong(artist, title)
            tags = gettagsfromsong(song, depth)
            for f in getartisttracks(artist, num):
                addtoplaylist(f)
            for g in gettracktracks(song, num):
                addtoplaylist(g)
            for h in tags:
                for i in gettagtracks(h, num):
                    addtoplaylist(i)

def makeplaylist():
    all0 = []
    all1 = []
    all2 = []
    alltracks1 = []
    alltracks = []
    if mytracks_top == "Y" or mytracks_top == "y":
        all0 = getmytracks(seed)
        print("My Top Tracks")
        print(all0)
        alltracks1 += all0
    if mytracks_weekly == "Y" or mytracks_weekly == "y":
        all1 = getmyweeklytracks(seed)
        alltracks1 += all1
        print("My Weekly Top Tracks")
        print(all1)
    if mytracks_hist == "Y" or mytracks_hist == "y":
        while all2 == []:
            all2 = histint(seed)
        alltracks1 += all2
        print("My Historical Top Tracks")
        print(all2)
    for x in alltracks1:
        if x not in alltracks:
            alltracks.append(x)
    for x in alltracks:
        global count
        song = str(x)
        count += 1
        os.system("clear")
        print(str(count) + "/" + str(seed * 3) + ": " + x)
        print("|", end="")
        getalltracks(song, depth)
        print("|")
    return(playlist)

def histint(num):
    registered = float(authuser.get_registered())
    print("Registered on: " + str(datetime.datetime.fromtimestamp(registered)))
    now = time.time()
    timedif = int(now) - int(registered)
    weeks = float((timedif/604800)/100)
    print(weeks)
    #hist = random.randint(2, weeks)
    hist = random.uniform(1.01, weeks)
    interval = timedif/hist
    #interval = timedif/56
    startdate = int(registered) + int(interval)
    print("Random Number: " + str(hist))
    print("Random week: " + str(datetime.datetime.fromtimestamp(startdate)))
    return(getmyweeklyhistoricaltracks(startdate, num))

#PROGRAM BELOW
playlist = []
count = 0
busy = 0
seed = int(input("How many top tracks to seed from?: "))
depth = int(input("How many tracks to grab per seed?: "))
file = str(input("Enter output file name: "))
mytracks_top = input("Seed from Overall Top Tracks? (Y/N): ")
mytracks_weekly = input("Seed from this Week's Top Tracks? (Y/N): ")
mytracks_hist = input("Seed from Random Historical Week's Top Tracks? (Y/N): ")
makeplaylist()
playlist.sort()
