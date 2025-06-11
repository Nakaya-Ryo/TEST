class OthelloGame:
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]

    def __init__(self):
        self.board = [[self.EMPTY for _ in range(8)] for _ in range(8)]
        # Initialize center
        self.board[3][3] = self.WHITE
        self.board[3][4] = self.BLACK
        self.board[4][3] = self.BLACK
        self.board[4][4] = self.WHITE

    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def valid_moves(self, player):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != self.EMPTY:
                    continue
                if self._would_flip(player, r, c):
                    moves.append((r, c))
        return moves

    def _would_flip(self, player, row, col):
        opponent = -player
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            has_opponent_between = False
            while self.in_bounds(r, c) and self.board[r][c] == opponent:
                r += dr
                c += dc
                has_opponent_between = True
            if has_opponent_between and self.in_bounds(r, c) and self.board[r][c] == player:
                return True
        return False

    def make_move(self, player, row, col):
        if (row, col) not in self.valid_moves(player):
            return False
        self.board[row][col] = player
        self._flip(player, row, col)
        return True

    def _flip(self, player, row, col):
        opponent = -player
        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            path = []
            while self.in_bounds(r, c) and self.board[r][c] == opponent:
                path.append((r, c))
                r += dr
                c += dc
            if path and self.in_bounds(r, c) and self.board[r][c] == player:
                for pr, pc in path:
                    self.board[pr][pc] = player

    def has_move(self, player):
        return len(self.valid_moves(player)) > 0

    def score(self):
        black = sum(row.count(self.BLACK) for row in self.board)
        white = sum(row.count(self.WHITE) for row in self.board)
        return {self.BLACK: black, self.WHITE: white}

    def print_board(self):
        header = '  ' + ' '.join(str(i) for i in range(8))
        print(header)
        for idx, row in enumerate(self.board):
            symbols = []
            for cell in row:
                if cell == self.BLACK:
                    symbols.append('B')
                elif cell == self.WHITE:
                    symbols.append('W')
                else:
                    symbols.append('.')
            print(f"{idx} " + ' '.join(symbols))


def play():
    game = OthelloGame()
    player = OthelloGame.BLACK
    while game.has_move(OthelloGame.BLACK) or game.has_move(OthelloGame.WHITE):
        if game.has_move(player):
            game.print_board()
            moves = game.valid_moves(player)
            print(f"Player {'Black' if player == OthelloGame.BLACK else 'White'}'s turn")
            print(f"Valid moves: {moves}")
            try:
                raw = input("Enter move as 'row col': ")
                row, col = map(int, raw.strip().split())
            except Exception:
                print('Invalid input')
                continue
            if not game.make_move(player, row, col):
                print('Invalid move, try again.')
                continue
        player = -player
    game.print_board()
    scores = game.score()
    if scores[OthelloGame.BLACK] > scores[OthelloGame.WHITE]:
        winner = 'Black'
    elif scores[OthelloGame.WHITE] > scores[OthelloGame.BLACK]:
        winner = 'White'
    else:
        winner = 'Draw'
    print('Game over!')
    print(f"Score - Black: {scores[OthelloGame.BLACK]}, White: {scores[OthelloGame.WHITE]}")
    print('Winner:', winner)


if __name__ == '__main__':
    play()
