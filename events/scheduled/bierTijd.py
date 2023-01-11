import json
import datetime

globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"
localPath = "InvictusRadio V3/events/"

def getManagerInfo():
    try:
        with open(globalPath + 'InvictusRadio V3/InvictusRadioInfo.json', 'r') as f:
            managerInfo = json.load(f)
    except:
        print("WARNING! Manager info corrupted or missing, default settings have been selected.")
        managerInfo = {"queueStyle" : "shuffle", "playlist" : None, "queue": [], "familiarityDictSongs": {}, "familiarityDictArtists": {}, "songStartTime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    return managerInfo

def setManagerInfo(managerInfo):
    with open(globalPath + 'InvictusRadio V3/InvictusRadioInfo.json', 'w') as f:
        json.dump(managerInfo, f)

def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

def getPathFromDatabase(songName):
    database = getNonLocalInfo(globalPath + "InvictusRadio V3/audioDatabase/audioDatabaseInfo.json")
    if songName in database.keys():
        return database[songName]["songPaths"][0]


audioPath = getPathFromDatabase("Bier Bel")

invictusRadioInfo = getManagerInfo()
invictusRadioInfo["queue"].insert(1, {"songName": "Bier Bel", "songPath": globalPath + audioPath, "songType": "functional"})
invictusRadioInfo["songStartTime"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
setManagerInfo(invictusRadioInfo)




