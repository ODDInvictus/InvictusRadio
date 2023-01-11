from pytube import YouTube
import urllib.request
import re
import json
import os
import time

globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"




def getDownloaderInfo():
    try:
        with open(globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json", 'r') as f:
            return json.load(f)
    except:
        print("WARNING! downloader info corrupted or missing.")

def setDownloaderInfo(info):
    with open(globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json", 'w') as f:
        json.dump(info, f)

def setNonLocalInfo(info, path):
    with open(path, 'w') as f:
        json.dump(info, f)

def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

def downloadSong(songInfoPre):
    songInfo = songInfoPre.copy()
    #find song on yt
    search_keyword = (songInfo["songName"] + " " + songInfo["artists"][0]).replace(' ', '+')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]

    yt = YouTube(url)
    ys = yt.streams.filter(only_audio=True).first()

    #Starting download
    if songInfo["type"] == "playlist":
        addedPath1 = "/" + songInfo["playlistName"]
        addedPath2 = "/" + songInfo["playlistName"] + "/"
        addedPath3 = songInfo["playlistName"] + "/"
    else:
        addedPath1 = ""
        addedPath2 = "" 
        addedPath3 = "" 
    try:
        #do the actual downloading
        out_file = ys.download(globalPath + "InvictusRadio V3/audioDatabase/music/downloads" + addedPath1)
        os.rename(out_file, (globalPath + "InvictusRadio V3/audioDatabase/music/downloads/" + addedPath2 + songInfo["songName"] + ".mp3"))

        #prepare and store metadata
        if songInfo["priority"] != None:
            del songInfo["priority"]
        if songInfo["type"] != None:
            del songInfo["type"]
        songInfo["songFileName"] = songInfo["songName"]
        songInfo["duration"] = yt.length
        setNonLocalInfo(info=songInfo, path=(globalPath + "InvictusRadio V3/audioDatabase/music/downloads/" + addedPath3 + songInfo["songFileName"] + ".json"))

    except:
        os.remove(out_file)
        print("Can't download song that already exists")
        print(songInfo)

    

    
    




#songInfo = getDownloaderInfo()["downloadQueue"][0]
#downloadSong(songInfo)


def run():
    downloaderInfo = getDownloaderInfo()

    if downloaderInfo["downloadQueue"] != []:

        songInfo = downloaderInfo["downloadQueue"][0]
        if songInfo["type"] == "playlist":
            addedPath = songInfo["playlistName"] + "/"
        else:
            addedPath = ""

        #download song
        downloadSong(songInfo)

        #remove download request from queue
        downloaderInfo = getDownloaderInfo()
        downloaderInfo["downloadQueue"] = downloaderInfo["downloadQueue"][1:]
        setDownloaderInfo(info=downloaderInfo)

        if downloaderInfo["downloadQueue"] == []:
            print("Done downloading!")

        #place song in queue if requested to do so
        if songInfo["priority"]:
            invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            invictusRadioInfo["queue"].insert(1, {"songName": songInfo["songName"], "songPath": globalPath + "InvictusRadio V3/audioDatabase/music/downloads/" + addedPath + songInfo["songName"] + ".mp3", "songType": "song"})
            setNonLocalInfo(info=invictusRadioInfo, path = globalPath + "InvictusRadio V3/InvictusRadioInfo.json")

        












