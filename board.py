from pieces import King, Piece

class ChessBoard:
    board = None
    
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = {
            True : set(),
            False : set(),
        }


    def insert(self, piece:Piece, row:int, index:int): 
        if self.board[row][index] is None:
            self.board[row][index] = piece
            piece.row = row
            piece.index = index
            piece.board = self.board
            self.pieces[piece.color].add(piece)
            
        else:
            raise ValueError(f'({row}, {index}) is full !\nplease remove ({row}, {index}) first, then add another piece')
    
    def get_pieces_location(self, color):
        locations = set()
        for piece in self.pieces[color]:
            locations.add((piece.row, piece.index))
        return locations

    def get_king(self, color) -> King:
        try:
            king = next(filter(lambda piece: isinstance(piece, King), self.pieces[color]))
            return king
        except Exception:
            raise ValueError('The King not exists')

    def get_pieces_actions(self, color, *exclude):
        result = set()
        for piece in self.pieces[color]:
            if exclude and isinstance(piece, exclude):
                continue
            result.update(piece.get_actions())
        
        return result

    free_spaces = lambda self : [(row_i, index_j) for row_i, row in enumerate(self.board) for index_j, index in enumerate(row) if index is None]
    free_spaces = property(fget=free_spaces)
