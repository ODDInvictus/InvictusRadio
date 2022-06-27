import configparser

from player import Player
from scanner import Scanner

config = None
scanner = None
player = None

def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    # print(config['songs']['location'])
    scanner = Scanner(config)
    scanner.run()

    player = Player(config, scanner)
    player.run()


if __name__ == '__main__':
    main()