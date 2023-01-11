import time
import vlc
import json


globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"


def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")
#invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")

oldInvictusRadioInfo = {"queue": [None]}
media = vlc.MediaPlayer("https://stream.joyradio.nl/joyradio")
media.audio_set_volume(100)
while True:
    try:
        invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
        if invictusRadioInfo["queue"][0] != oldInvictusRadioInfo["queue"][0]:
            print("yay")
            if media.is_playing():
                media.stop()
            media = vlc.MediaPlayer(invictusRadioInfo["queue"][0]["songPath"])
            media.play()
        oldInvictusRadioInfo = invictusRadioInfo
    except:
        print("something went wrong")
    time.sleep(1)


#"""






