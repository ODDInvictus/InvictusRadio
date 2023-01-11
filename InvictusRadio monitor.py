import importlib.util as ilu
import importlib
import ray
import threaded
import asyncio
import time
import threading
from multiprocessing import Process


globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"


def load1(path):
    importlib.import_module(path)

def load2(path):
    importlib.import_module(path)


if __name__ == '__main__':
    #start discord bot and the music player in the colosseum in it's own paralel threads
    discordBot = Process(target=load1, args=('InvictusRadio discordBot.InvictusRadio discordBot',))
    discordBot.start()
    colosseumPlayer = Process(target=load2, args=('player.colosseumPlayer',))
    colosseumPlayer.start()


    #load all scripts
    invictusRadioManager = importlib.import_module('InvictusRadio Manager')
    audiodataBaseManager = importlib.import_module('audioDatabase.audioDatabase manager')
    downloader = importlib.import_module('audioDatabase.downloader')
    eventManager = importlib.import_module('events.eventManager')

    while True:
        if discordBot.is_alive() == False:
            print("Discord has crashed")
        else:
            print("All nominal")

        #run all threads
        try:
            audiodataBaseManager.run()
        except:
            print("something wrong in database manager")
        try:
            invictusRadioManager.run()
        except:
            print("something wrong in manager")
        try:
            downloader.run()
        except:
            print("something wrong in downloader")
        downloader.run()
        eventManager.run()

        time.sleep(1)
