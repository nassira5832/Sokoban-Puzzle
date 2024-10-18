class  SokobanPuzzle:
    def __init__(self, grid):
        self.grid=grid
        self.player= self.findplayer()
        self.wall= self.findwall()
        self.box=self.findbox()
        self.target = self.target
        
    
