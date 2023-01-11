import json
import glob
import time
import asyncio

globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"
localPath = "InvictusRadio V3/audioDatabase/"

def setAudioDatabaseInfo(audioDatabaseInfo):
    with open(globalPath + localPath + 'audioDatabaseInfo.json', 'w') as f:
        json.dump(audioDatabaseInfo, f)

def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

def generateAudioDatabaseInfo():
    songPaths = glob.glob("InvictusRadio V3/audioDatabase/**\\*.mp3",recursive=True)
    audioDatabaseInfo = {}
    for songPath in songPaths:
        songInfo = getNonLocalInfo(globalPath + songPath[:-4] + ".json")
        try:
            audioDatabaseInfo[songInfo["songName"]]["songPaths"].append(songPath)
        except:
            audioDatabaseInfo[songInfo["songName"]] = {"songName": songInfo["songName"], "songPaths": [songPath]}
    return audioDatabaseInfo

def run():
    setAudioDatabaseInfo(generateAudioDatabaseInfo())





