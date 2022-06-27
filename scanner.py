class Scanner():
    def __init__(self, c):
        self.config = c

    
    def run(self):
        self.print('Starting the scanner...')
        comm_loc = self.config['commercials']['location']
        songs_loc = self.config['songs']['location']


    def print(self, to_print):
        print('[Scanner] ', end='')
        print(to_print)
