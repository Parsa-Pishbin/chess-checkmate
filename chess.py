from randomizer import create_and_add_random_pieces_to_board
from pieces import WHITE, BLACK
from board import ChessBoard


while True:
    board = ChessBoard()

    create_and_add_random_pieces_to_board(board, WHITE)
    create_and_add_random_pieces_to_board(board, BLACK)
    
    board.pprint_board(large=False) # the "large" is size of chess board's cells
    board.status
    
    input('Press ENTER to continue')
    