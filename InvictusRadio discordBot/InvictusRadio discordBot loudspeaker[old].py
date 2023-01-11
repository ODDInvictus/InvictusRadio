import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import time
import asyncio

globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"
intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix = "!", intents=intents)

def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

@client.event
async def on_ready():
    #let people know they can start lisening
    textChannel = client.get_channel(1058308860852576276)
    await textChannel.send("InvictusRadio dicord speaker is now active")

    voiceChannel = client.get_channel(1058308991022800976)
    voice = await voiceChannel.connect()
    oldInvictusRadioInfo = {"queue": [None]}
    t1 = time.time()
    while True:
        invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
        if invictusRadioInfo["queue"][0] != oldInvictusRadioInfo["queue"][0]:
            if voice.is_playing():
                voice.stop()
            source = FFmpegPCMAudio(invictusRadioInfo["queue"][0]["songPath"])
            player = voice.play(source)
            print("new")
        oldInvictusRadioInfo = invictusRadioInfo
        await asyncio.sleep(1)


client.run("MTA1ODMwMTE3MTU5MDIzODMwOQ.GkwwXQ.uw67scLhlC2rNSZ643VV3eJYRB0kY7WKqua8YA")
