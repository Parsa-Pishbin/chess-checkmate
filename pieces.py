WHITE = True
BLACK = False

class Piece:
    row:int = None
    index:int = None
    directions:list[tuple[int, int]] = []
    board = None

    def __init__(self, color:bool):
        self.color = color

    def __repr__(self):
        return f'{"White" if self.color else "Black"} ' + self.__class__.__name__
    
    @property
    def location(self):
        return (self.row, self.index)
    
    def get_actions(self):
        if self.row is None or self.index is None or self.board is None:
            raise ValueError('the piece must be on a board')

        result = set()

        for direction in self.directions:
            action = self.calculate_action(direction)
            if action is not None:
                result.add(action)

        return result
    
    def calculate_action(self, direction):
        dr, di = direction
        if not self.color:
            dr *= -1
        new_row = dr + self.row
        new_index = di + self.index

        if -1 < new_row < 8 and -1 < new_index < 8:
            return (new_row, new_index)


class Pawn(Piece):
    directions = [(+1, -1), (+1, +1)]


class Knight(Piece):
    directions = [(+2, -1), (+2, +1), (-2, -1), (-2, +1), (+1, -2), (-1, -2), (+1, +2), (-1, +2),]

    
class King(Piece):
    directions = [(+1, -1), (+1, 0), (+1, +1),
                  (0, -1),            (0, +1),
                  (-1, -1), (-1, 0), (-1, +1)]

    