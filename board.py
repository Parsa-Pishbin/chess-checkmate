from  pieces import Piece


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
    

    free_spaces = lambda self : [(row_i, index_j) for row_i, row in enumerate(self.board) for index_j, index in enumerate(row) if index is None]
    free_spaces = property(fget=free_spaces)
