from scanner import Scanner
from playsound import playsound

class Player():
    def __init__(self, c, s):
        self.config = c
        self.scanner: Scanner = s

    
    def run(self):
        self.print('Starting the player...')
        


    def print(self, to_print):
        print('[Player] ', end='')
        print(to_print)
