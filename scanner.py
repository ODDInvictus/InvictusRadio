from dataclasses import dataclass
import os
from typing import List

class Scanner:
    def __init__(self, c, s):
        self.config = c
        self.sched = s
        self.commercials: List[AudioFile] = []
        self.songs: List[AudioFile] = []


    def run(self) -> None:
        self.print('Starting the scanner...')
        self.comm_loc = self.config['commercials']['location']
        self.songs_loc = self.config['songs']['location']

        # Scan for files
        self.loop()

        # Run the loop every 30 minutes
        self.sched.add_job(self.loop, 'interval', seconds=30*60, replace_existing=True)
        self.sched.start()


    def loop(self) -> None:
        self.scan(self.comm_loc, self.commercials, 'commercials')
        self.scan(self.songs_loc, self.songs, 'songs')


    def scan(self, loc: str, list: List, type: str) -> None:
        files = os.listdir(loc)
        for file in files:
            if file.endswith('.wav') or file.endswith('.mp3'):
                list.append(AudioFile(file))
        self.print("Found " + str(len(files)) + " " + type)


    def print(self, to_print):
        print('[Scanner] ', end='')
        print(to_print)

@dataclass
class AudioFile:
    location: str
    times_played: int = 0