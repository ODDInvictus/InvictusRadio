import discord
from discord.ext import commands
import json
import datetime
import asyncio
import time
from discord import FFmpegPCMAudio
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import glob

from passwords import *


globalPath = "C:/Users/2sylv/Desktop/opdrachten programeren/IBS/"
intents = discord.Intents.default()
intents.members = True


#scope = "user-library-read"




# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri = "http://google.com")
spotify = sp.Spotify(auth_manager=auth_manager)




client = commands.Bot(command_prefix = "!", intents=intents)

def getNonLocalInfo(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        print("WARNING! Info corrupted or missing.")

def setNonLocalInfo(info, path):
    with open(path, 'w') as f:
        json.dump(info, f)

def getPathFromDatabase(songName):
    database = getNonLocalInfo(globalPath + "InvictusRadio V3/audioDatabase/audioDatabaseInfo.json")
    if songName in database.keys():
        return database[songName]["songPaths"][0]

def getSpotifySongInfos(spotify, name):
    # Replace all spaces in name with '+'
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=5, type='track')
    
    infos = []
    for result in results["tracks"]["items"]:
        songName = result["name"]
        songArtists = []
        for artist in result["artists"]:
            songArtists.append(artist["name"])
    
        infos.append({"songName": songName, "artists": songArtists})
    return infos

def get_playlist_uri(playlist_link):
    return playlist_link.split("/")[-1].split("?")[0]


def getSongInPlaylist(playlistUrl):
    #get some info
    playlist_uri = get_playlist_uri(playlistUrl)
    results = spotify.playlist_tracks(playlist_uri)
    playlistName = spotify.user_playlist(user=None, playlist_id=playlist_uri, fields="name")["name"]
    
    tracks = []
    first = True
    while results['next'] or first == True:
        #load more data
        if first == False:
            results = spotify.next(results)
        else:
            first = False
        
        #extract info
        for track in results["items"]:
            songName = track["track"]["name"].encode('ascii', 'ignore').decode('ascii')
            artists = []
            for arist in track["track"]["artists"]:
                artists.append(arist["name"].encode('ascii', 'ignore').decode('ascii'))
            tracks.append({"type": "playlist", "playlistName": playlistName, "songName": songName, "artists": artists, "priority": False})
    
    return tracks


@client.event
async def on_ready():
    #let people know they can start lisening
    textChannel = client.get_channel(textChannelID)
    await textChannel.send("InvictusRadio dicord is now active")
    print(("InvictusRadio dicord is now active"))

    voiceChannel = client.get_channel(voiceChannelID)
    voice = await voiceChannel.connect()
    oldInvictusRadioInfo = {"queue": [None]}
    t1 = time.time()
    while True:
        try:
            invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            if invictusRadioInfo["queue"][0] != oldInvictusRadioInfo["queue"][0]:
                if voice.is_playing():
                    voice.stop()
                source = FFmpegPCMAudio(invictusRadioInfo["queue"][0]["songPath"])
                player = voice.play(source)
                #print("new")
            oldInvictusRadioInfo = invictusRadioInfo
        except:
            print("something went wrong")
        await asyncio.sleep(1)

@client.command()
async def helloWorld(ctx):
    await ctx.send("Hello World!")

@client.command()
async def skip(ctx):
    if ctx.channel.id == textChannelID:
        invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
        invictusRadioInfo["queue"] = invictusRadioInfo["queue"][1:]
        invictusRadioInfo["songStartTime"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        setNonLocalInfo(info=invictusRadioInfo, path = globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
        
        await ctx.send("Song skipped")

@client.command()
async def play(ctx, *, arg):
    if ctx.channel.id == textChannelID:
        #print(arg)
        spotifySongInfos = getSpotifySongInfos(spotify, arg)

        songPath = getPathFromDatabase(spotifySongInfos[0]["songName"])
        #print(songPath)

        if songPath != None:
            invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            invictusRadioInfo["queue"].insert(0, {"songName": spotifySongInfos[0]["songName"], "songPath": globalPath + songPath, "songType": "song"})
            invictusRadioInfo["songStartTime"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            setNonLocalInfo(info=invictusRadioInfo, path = globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            
            await ctx.send("Now playing " + spotifySongInfos[0]["songName"] + " by " + spotifySongInfos[0]["artists"][0])
        else:
            downloaderInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")
            downloaderInfo["downloadQueue"].append({"type": "song", "songName": spotifySongInfos[0]["songName"], "artists": spotifySongInfos[0]["artists"], "priority": True})
            setNonLocalInfo(info=downloaderInfo, path=globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")

            textChannel = client.get_channel(textChannelID)
            await textChannel.send("Currently downloading " + spotifySongInfos[0]["songName"] + " by " + spotifySongInfos[0]["artists"][0])

@client.command()
async def refreshQueue(ctx):
    if ctx.channel.id == textChannelID:
        invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
        invictusRadioInfo["queue"] = []
        setNonLocalInfo(info=invictusRadioInfo, path = globalPath + "InvictusRadio V3/InvictusRadioInfo.json")

        await ctx.send("Queue refreshed")

@client.command()
async def download(ctx, arg):
    if ctx.channel.id == textChannelID:
        spotifySongInfos = getSpotifySongInfos(spotify, arg)

        downloaderInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")
        downloaderInfo["downloadQueue"].append({"type": "song", "songName": spotifySongInfos[0]["songName"], "artists": spotifySongInfos[0]["artists"], "priority": True})
        setNonLocalInfo(info=downloaderInfo, path=globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")

        textChannel = client.get_channel(textChannelID)
        await textChannel.send("Currently downloading " + spotifySongInfos[0]["songName"] + " by " + spotifySongInfos[0]["artists"][0])

@client.command()
async def downloadPlaylist(ctx, arg):
    if ctx.channel.id == textChannelID:
        downloadRequests = getSongInPlaylist(arg)

        downloaderInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")
        downloaderInfo["downloadQueue"] = downloaderInfo["downloadQueue"] + downloadRequests
        setNonLocalInfo(info=downloaderInfo, path=globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")

        textChannel = client.get_channel(textChannelID)
        await textChannel.send("Currently downloading " + downloadRequests[0]["playlistName"])

@client.command()
async def playlist(ctx, *, arg):
    if ctx.channel.id == textChannelID:
        #Check if the playlist exists
        validPlaylist = {}
        spam = glob.glob(globalPath + "InvictusRadio V3/audioDatabase/*/**/", recursive=True)
        for egg in spam:
            validPlaylist[egg[egg[:-1].rfind("\\")+1:-1]] = egg
        
        textChannel = client.get_channel(textChannelID)
        invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
        if arg in validPlaylist.keys():
            invictusRadioInfo["playlist"] = arg
            setNonLocalInfo(info=invictusRadioInfo, path = globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            await textChannel.send("Playlist set to " + arg + ". Consider refreshing queue.")
        else:
            await textChannel.send("No playlis named " + arg + "!")

@client.command()
async def queue(ctx, *, arg):
    if ctx.channel.id == textChannelID:
        #print(arg)
        spotifySongInfos = getSpotifySongInfos(spotify, arg)

        songPath = getPathFromDatabase(spotifySongInfos[0]["songName"])
        #print(songPath)

        if songPath != None:
            invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            invictusRadioInfo["queue"] = invictusRadioInfo["queue"] + {"songName": spotifySongInfos[0]["songName"], "songPath": globalPath + songPath, "songType": "song"}
            setNonLocalInfo(info=invictusRadioInfo, path = globalPath + "InvictusRadio V3/InvictusRadioInfo.json")
            
            await ctx.send("Now playing " + spotifySongInfos[0]["songName"] + " by " + spotifySongInfos[0]["artists"][0])
        else:
            downloaderInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")
            downloaderInfo["downloadQueue"].append({"type": "song", "songName": spotifySongInfos[0]["songName"], "artists": spotifySongInfos[0]["artists"], "priority": True})
            setNonLocalInfo(info=downloaderInfo, path=globalPath + "InvictusRadio V3/audioDatabase/downloaderInfo.json")

            textChannel = client.get_channel(textChannelID)
            await textChannel.send("Currently downloading " + spotifySongInfos[0]["songName"] + " by " + spotifySongInfos[0]["artists"][0])

@client.command()
async def showQueue(ctx):
    if ctx.channel.id == textChannelID:
        invictusRadioInfo = getNonLocalInfo(globalPath + "InvictusRadio V3/InvictusRadioInfo.json")

        
        text = "The upcoming songs are:\n"
        for item in invictusRadioInfo["queue"]:
            if item["songType"] == "song":
                text = text + item["songName"] + "\n"
        textChannel = client.get_channel(textChannelID) 
        await textChannel.send(text) 

"""
@client.event
async def on_member_join(member):
    channel = client.get_channel(1058308860852576276)
    await channel.send("yay")
"""

client.run(discordToken)


