from random import randint

from pieces import Piece, King, Queen, Bishop, Knight, Pawn, Rook
from board import ChessBoard


pop_random = lambda l: l.pop(randint(0, len(l)-1))


def create_and_add_random_pieces_to_board(board:ChessBoard, color):
    PIECES = [Pawn for _ in range(8)] \
    + [Bishop for _ in range(2)] \
    + [Knight for _ in range(2)] \
    + [Rook for _ in range(2)] \
    + [Queen]

    spaces = board.free_spaces

    king = King(color)
    board.insert(king, *pop_random(spaces))

    for _ in range(randint(0, 15)):
        random_location = pop_random(spaces)
        random_PieceClass:Piece = pop_random(PIECES)
        
        piece = random_PieceClass(color)
        
        board.insert(piece, *random_location)
