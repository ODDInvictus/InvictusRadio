import json
import glob
import random
import numpy as np
import datetime
import time
import asyncio

#print("test")

globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"
localPath = "InvictusRadio V3/"

# a few functions we need
def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

def getManagerInfo():
    try:
        with open(globalPath + localPath + 'InvictusRadioInfo.json', 'r') as f:
            managerInfo = json.load(f)
    except:
        print("WARNING! Manager info corrupted or missing, default settings have been selected.")
        managerInfo = {"queueStyle" : "shuffle", "playlist" : None, "queue": [], "familiarityDictSongs": {}, "familiarityDictArtists": {}, "songStartTime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    return managerInfo

def setManagerInfo(managerInfo):
    with open(globalPath + localPath + 'InvictusRadioInfo.json', 'w') as f:
        json.dump(managerInfo, f)

def getPlaylistInfo(playlist):
    #Check if the playlist exists
    validPlaylist = {}
    spam = glob.glob(globalPath + "InvictusRadio V3/audioDatabase/*/**/", recursive=True)
    for egg in spam:
        validPlaylist[egg[egg[:-1].rfind("\\")+1:-1]] = egg
    #print(validPlaylist.keys())

    if playlist == None:
        playlist = "music"
    elif playlist not in validPlaylist.keys():
        playlist = "music"
        print("WARNING! Selected play not avalible.")

    #colecting relefant information
    playlistPath = validPlaylist[playlist]
    songLinks = glob.glob(playlistPath+"**\\*.mp3",recursive=True)
    numSongs = len(songLinks)
    return {"playlistName" : playlist, "playlistPath" : playlistPath, "songLinks" : songLinks, "numSongs" : numSongs}

def addSongQueueShuffle():
    """
    Pick a random song but have a chance of picking another one if this song or artist is already played
    """
    #these setting determine how the shuffle algorithm prefents song or artists not to be picked too often
    songPenalty = 10
    artistPenalty = 5
    penaltyDecay = 0.8


    #get familiarity dict to check if a song or artist is already played a lot
    managerInfo = getManagerInfo()
    try:
        familiarityDictSongs = managerInfo["familiarityDictSongs"]
    except:
        familiarityDictSongs = {}
    try:
        familiarityDictArtists = managerInfo["familiarityDictArtists"]
    except:
        familiarityDictArtists = {}


    #get playlist info
    playlistInfo = getPlaylistInfo(managerInfo["playlist"])


    #this loop will repeat until it found a song that hasn't been played too much
    done = False
    i = 0
    while done == False and i <= 1000:
        #pick random song out of playlist and get song info
        suggestionLink = playlistInfo["songLinks"][random.randint(0,playlistInfo["numSongs"]-1)]
        try:
            with open(suggestionLink[:-4] + ".json", 'r') as f:
                suggestionInfo = json.load(f)
        except:
            print("WARNING! Song info corrupted or missing, song is not added to queue.\nLink to song: " + suggestionLink)
            continue
        
        
        #check if we had this song or artist before and get familiarity score
        if suggestionInfo["songName"] in familiarityDictSongs.keys():
            familiarityScoreSong = familiarityDictSongs[suggestionInfo["songName"]]
        else:
            familiarityScoreSong = 0
        
        familiarityScoreArtist = 0
        for artist in [i for i in suggestionInfo["artists"] if i in familiarityDictArtists.keys()]:
            familiarityScoreArtist = familiarityScoreArtist + familiarityDictArtists[artist]
        
        #if a song or artist has been played a lot it will be discriminated against
        discriminationOdds = np.e**((familiarityScoreSong + familiarityScoreArtist)*-1)
        
        if random.random() <= discriminationOdds:
            #add new song to queue
            managerInfo["queue"].append({"songName": suggestionInfo["songName"], "songPath": suggestionLink, "songType": "song"})
            
            #adjust the familiarity score so the song or artist is played less often in the future
            try:
                managerInfo["familiarityDictSongs"][suggestionInfo["songName"]] = managerInfo["familiarityDictSongs"][suggestionInfo["songName"]] + songPenalty
            except:
                managerInfo["familiarityDictSongs"][suggestionInfo["songName"]] = songPenalty
            for artist in suggestionInfo["artists"]:
                #print(artist)
                try:
                    managerInfo["familiarityDictArtists"][artist] = managerInfo["familiarityDictArtists"][artist] + artistPenalty
                except:
                    managerInfo["familiarityDictArtists"][artist] = artistPenalty

            #adjust the familiarity score so the song or artist is not discriminated against indevinately
            for song in managerInfo["familiarityDictSongs"]:
                managerInfo["familiarityDictSongs"][song] = managerInfo["familiarityDictSongs"][song]*penaltyDecay
            for artist in managerInfo["familiarityDictArtists"]:
                managerInfo["familiarityDictArtists"][artist] = managerInfo["familiarityDictArtists"][artist]*penaltyDecay            

            done = True
        i = i + 1
        
    if done == False:
        managerInfo["queue"].append({"songName": suggestionInfo["songName"], "songPath": globalPath + "InvictusRadio V3/audioDatabase/functional/manager warnings/too few songs to shuffle.mp3", "songType": "functional"})
        #managerInfo["queuePaths"].append(globalPath + "InvictusRadio V3/audioDatabase/functional/manager warnings/too few songs to shuffle.mp3")
        for song in managerInfo["familiarityDictSongs"]:
            managerInfo["familiarityDictSongs"][song] = managerInfo["familiarityDictSongs"][song]*penaltyDecay
        for artist in managerInfo["familiarityDictArtists"]:
            managerInfo["familiarityDictArtists"][artist] = managerInfo["familiarityDictArtists"][artist]*penaltyDecay   
    setManagerInfo(managerInfo)



managerInfo = getManagerInfo()
setManagerInfo(managerInfo)
addSongQueueShuffle()
#test = {'queueStyle': 'shuffle', 'playlist': 'test', 'queuePaths': ['C:/Users/2sylv/Desktop/opdrachten programeren/IBS/InvictusRadio V3/audioDatabase\\music\\test\\Crazy Frog+Axel F.mp3'], 'familiarityDictSongs': {'Crazy Frog': 8.0}, 'familiarityDictArtists': {'Axel F': 4.0}}
#setManagerInfo(test)

#onAir = datetime.datetime.now()
#while onAir + datetime.timedelta(seconds=100) >= datetime.datetime.now():
def run():
    managerInfo = getManagerInfo()
    #make sure the queue is long enough
    if len(managerInfo["queue"]) <= 5:
        if managerInfo["queueStyle"] == "shuffle":
            addSongQueueShuffle()
            print("queue len: " + str(len(managerInfo["queue"])))
            print("queue extended!")
            managerInfo = getManagerInfo()

    #remove song from queue when done
    if managerInfo["queue"][0]["songType"] == "song":
        currentSongInfo = getNonLocalInfo(managerInfo["queue"][0]["songPath"][:-4]+".json")
        if datetime.datetime.strptime(managerInfo["songStartTime"], "%m/%d/%Y, %H:%M:%S") + datetime.timedelta(seconds=currentSongInfo["duration"]) <= datetime.datetime.now():
            managerInfo["queue"] = managerInfo["queue"][1:]
            managerInfo["songStartTime"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            setManagerInfo(managerInfo)
            print("queue len: " + str(len(managerInfo["queue"])))
            print("song deleted")
    
    #make sure the queue is long enough
    if len(managerInfo["queue"]) <= 4:
        if managerInfo["queueStyle"] == "shuffle":
            addSongQueueShuffle()
            print("queue len: " + str(len(managerInfo["queue"])))
            print("queue extended!")



    #print("yay")
    #time.sleep(1)
    #asyncio.sleep(1)