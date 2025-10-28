class Piece:
    row:int = None
    index:int = None
    directions:list[tuple] = []

    def __init__(self, color:bool):
        self.color = color

    def __repr__(self):
        return f'{"White" if self.color else "Black"} ' + self.__class__.__name__
    
    @property
    def location(self):
        return (self.row, self.index)
    