from collections import defaultdict


class LifeGame(object):
    """
    Class for Game life
    """
    def __init__(self, board):
        self.board = board
        self.size = len(board)

    def get_next_generation(self):
        """
        Calculate next generation
        """
        new_board = [[0 for _ in range(len(self.board[0]))] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                new_board[i][j] = self._next_cell_state(i, j)
        self.board = new_board

    def _next_cell_state(self, i, j):
        """
        Calculate next cell state
        """
        if self.board[i][j] == 1:
            return 1
        count = defaultdict(int)
        for x in range(max(0, i - 1), min(self.size, i + 2)):
            for y in range(max(0, j - 1), min(self.size, j + 2)):
                if x == i and y == j:
                    continue
                count[self.board[x][y]] += 1
        if 1 < count[2] < 4:
            return 2
        elif 1 < count[3] < 4:
            return 3
        else:
            return 0
