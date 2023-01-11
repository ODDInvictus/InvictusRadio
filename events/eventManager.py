import glob
import json
import datetime
import importlib
import random
import schedule
import time

globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"
localPath = "InvictusRadio V3/events/"


def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

def getEvents(type):
    eventPaths = []
    spam = glob.glob(globalPath + localPath + type + "/*.json", recursive=True)
    for egg in spam:
        eventPaths.append(egg)

    events = []
    for eventPath in eventPaths:
        events.append(getNonLocalInfo(eventPath))

    return events

def getManagerInfo():
    try:
        with open(globalPath + 'InvictusRadio V3/InvictusRadioInfo.json', 'r') as f:
            managerInfo = json.load(f)
    except:
        print("WARNING! Manager info corrupted or missing, default settings have been selected.")
        managerInfo = {"queueStyle" : "shuffle", "playlist" : None, "queue": [], "familiarityDictSongs": {}, "familiarityDictArtists": {}, "songStartTime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
    return managerInfo

def setManagerInfo(managerInfo):
    with open(globalPath + localPath + 'InvictusRadioInfo.json', 'w') as f:
        json.dump(managerInfo, f)

def doEvent(event):
    print("test")
    #update manager info to set event
    managerInfo = getManagerInfo()
    managerInfo["event"] = event["eventName"]
    setManagerInfo(managerInfo)

    #run event
    try: 
        importlib.import_module("events." + event["eventType"] + "." + event["fileName"])
    except:
        importlib.import_module(event["eventType"] + "." + event["fileName"])

    #update manager info so no event is active
    managerInfo = getManagerInfo()
    managerInfo["event"] = None
    setManagerInfo(managerInfo)

def doRandomEvents():
    #do nothing if event is already active
    managerInfo = getManagerInfo()
    try:
        if managerInfo["event"] == None:
            events = []
            semiScheduledEvents = getEvents("semiScheduled")

            dayOfWeek = datetime.datetime.now().strftime('%A')
            current = datetime.datetime.now().time()
            #only use semi scheduled events that are currently active
            for semiScheduledEvent in semiScheduledEvents:
                for eventTime in semiScheduledEvent["allowedTimes"]:
                    if eventTime["day"] == "Every" or eventTime["day"] == dayOfWeek:
                        start = datetime.time(int(eventTime["startTime"][:2]), int(eventTime["startTime"][3:]), 0)
                        end = datetime.time(int(eventTime["endTime"][:2]), int(eventTime["endTime"][3:]), 0)
                        if start <= current <= end:
                            events.append(semiScheduledEvent)
            
            #also use fully random events
            events = events + getEvents("random")
            #give each event a chance to get activated
            for event in events:
                if random.random() < 1/event["expectedTimeInterval"]:
                    #actualy do the event
                    doEvent(event)

    except:
        pass






#set up all the schedueled events
scheduledEvents = getEvents("scheduled")
for event in scheduledEvents:
    for scheduledTime in event["scheduledTimes"]:
        if scheduledTime["day"] == "Every":
            schedule.every().day.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Monday":
            schedule.every().monday.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Tuesday":
            schedule.every().tuesday.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Wednesday":
            schedule.every().wednesday.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Thursday":
            schedule.every().thursday.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Friday":
            schedule.every().friday.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Saturday":
            schedule.every().saturday.at(scheduledTime["startTime"]).do(doEvent, event)
        if scheduledTime["day"] == "Sunday":
            schedule.every().sunday.at(scheduledTime["startTime"]).do(doEvent, event)
        
#schedule the opertunety for random event ever minute
schedule.every().minute.do(doRandomEvents)

#schedule.every().minute.do(doEvent, getEvents("scheduled")[0])
#doEvent(getEvents("scheduled")[0])

def run():
    schedule.run_pending()






















