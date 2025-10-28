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


class DynamicActionsCalculatorMixin:
    def __init__(self, color):
        if not hasattr(self, 'dynamic_directions'):
            raise ValueError('dynamic_directions must be set !')
        
        super().__init__(color)
        self.get_static_actions = super().get_actions

    def get_actions(self):
        if self.row is None or self.index is None or self.board is None:
            raise ValueError('the piece must be on a board')
        return self.get_static_actions().union(self.get_dynamic_actions())

    def get_dynamic_actions(self):
        result = set()

        for direction in self.dynamic_directions:
            row = self.row
            index = self.index

            while True:
                dynamic_action = self.calculate_dynamic_action(row, index, direction)
                if dynamic_action is None:
                    break
                piece = self.board[dynamic_action[0]][dynamic_action[1]]
                if piece is None:
                    result.add(dynamic_action)
                    row, index = dynamic_action
                    
                else:
                    result.add(dynamic_action)
                    break
        return result

    def calculate_dynamic_action(self, row, index, direction):
        dr, di = direction

        new_row = dr + row
        new_index = di + index

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

    