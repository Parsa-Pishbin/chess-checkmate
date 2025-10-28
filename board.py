from  pieces import King, Piece, Queen, Bishop, Rook

class ChessBoard:
    board = None
    
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = {
            True : set(),
            False : set(),
        }

    def pprint_board(self, large=True):
        line = "-|" + ( f"{'-' *15}|"*8)
        empty_line = " |" + ( f"{' ' *15}|"*8)
        print(line)
        print(empty_line)  if large else None
        
        for row_i, row in enumerate(reversed(self.board)):
            temp = [str(7-row_i)] + [f'{str(i if i else ""):^15}' for i in row] + ['']
            print(empty_line, empty_line, sep='\n') if large else None
            print('|'.join(temp))
            print(empty_line, empty_line, sep='\n') if large else None
            print(line)
            
        print(' |'+ '|'.join([f'{str(i):^15}' for i in range(8)] + ['']))

    def insert(self, piece:Piece, row:int, index:int): 
        if self.board[row][index] is None:
            self.board[row][index] = piece
            piece.row = row
            piece.index = index
            piece.board = self.board
            self.pieces[piece.color].add(piece)
            
        else:
            raise ValueError(f'({row}, {index}) is full !\nplease remove ({row}, {index}) first, then add another piece')
    
    @property
    def status(self):
        for color in self.pieces:
            check = self.is_check(color)
            check_mate = self.is_check_mate(color)
            print(f'{"White" if color else "Black"} check :', check)
            print(f'{"White" if color else "Black"} check mate:', check_mate) if check else None
            print()
            
    def get_pieces_location(self, color):
        locations = set()
        for piece in self.pieces[color]:
            locations.add((piece.row, piece.index))
        return locations

    def is_check(self, color):
        king = self.get_king(color)

        danger_locations = self.get_pieces_actions(not color)
        result = danger_locations.intersection({(king.row, king.index)}) or None
        return False if result is None else True
    
    def is_check_mate(self, color):
        if not self.is_check(color): return False
        if self.can_king_escape_or_attack(color): return False
        
        attackers = self.attacker_pieces_to(self.get_king(color))
        if len(attackers)> 1: return True
        
        if self.can_other_pieces_attack_for_king(color): return False
        if self.can_other_pieces_sacrifice_for_king(color): return False
        return True
        
    def get_king(self, color) -> King:
        try:
            king = next(filter(lambda piece: isinstance(piece, King), self.pieces[color]))
            return king
        except Exception:
            raise ValueError('The King not exists')

    def can_king_escape_or_attack(self, color):
        king = self.get_king(color)
        teammate_locations = self.get_pieces_location(color)
        
        king_available_actions = king.get_actions().difference(teammate_locations)
        danger_locations = self.get_pieces_actions(not color)
        result = king_available_actions.difference(danger_locations) or None

        return False if result is None else True
    
    def attacker_pieces_to(self, piece):
        attackers = []
        for opponent_piece in self.pieces[not piece.color]:
            if piece.location in opponent_piece.get_actions():
                attackers.append(opponent_piece)

        return attackers

    def can_other_pieces_attack_for_king(self, color):
        king = self.get_king(color)
        attackers = self.attacker_pieces_to(king)

        if len(attackers) > 1 or len(attackers) == 0: # second part is optional and not required
            return False
        
        attacker = attackers[0]
        teammate_actions = self.get_pieces_actions(color, King)

        if attacker.location in teammate_actions:
            return True
        return False
        
    def __points_between(self, location_1, location_2, n):
        x1, y1 = location_1
        x2, y2 = location_2
        points = set()
        for i in range(1, n):
            t = i / n
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            points.add((int(x), int(y)))
        return points

    def can_other_pieces_sacrifice_for_king(self, color):
        king = self.get_king(color)
        attackers = self.attacker_pieces_to(king)

        if len(attackers) > 1 or len(attackers) == 0: # second part is optional and not required
            return False
        
        attacker = attackers[0]

        if not isinstance(attacker, (Queen, Bishop, Rook)):
            return False
        
        places = max(abs(king.row-attacker.row), abs(king.index - attacker.index))
        if places < 2: return False
        
        sacrificable_places = self.__points_between(king.location, attacker.location, places)
        teammate_moves = self.get_pieces_moves(color, King)

        if teammate_moves.intersection(sacrificable_places):
            return True
        return False

    def get_pieces_actions(self, color, *exclude):
        result = set()
        for piece in self.pieces[color]:
            if exclude and isinstance(piece, exclude):
                continue
            result.update(piece.get_actions())
        
        return result

    def get_pieces_moves(self, color, *exclude):
        moves = set()
        for piece in self.pieces[color]:
            if exclude and isinstance(piece, exclude):
                continue
                
            moves.update(piece.get_moves())

        return moves
    

    free_spaces = lambda self : [(row_i, index_j) for row_i, row in enumerate(self.board) for index_j, index in enumerate(row) if index is None]
    free_spaces = property(fget=free_spaces)
