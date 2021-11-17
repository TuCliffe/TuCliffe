"""
    Description: A game of Sokoban, the player pushes the crates
                    into the holes to win.                
    Player = 'P'
    Crate = '#'
    Hole = 'o'
    Wall = '*'
    
    Adjust the test_board at the bottom to create a new board!!
    
"""

class Sokoban:    
    def __init__(self, board):
        self.__max_row = len(board)
        self.__max_col = len(board[0])
        self.__board_history = [Sokoban.copy_board(board)]
        
    def find_player(self):
        board = self.__board_history[-1]
        for i in range(len(board)):
            if 'P' in board[i]:
                return i, board[i].index('P')
            
    def complete(self):
        board = self.__board_history[-1]
        for index in range(len(board)):
            if 'o' in board[index]:
                return False
        return True
            
    def __overflow_check(self, i_next, j_next):
        if i_next < 0:
            i_next = self.__max_row - 1
        elif i_next >= self.__max_row:
            i_next = 0
        if j_next < 0:
            j_next = self.__max_col - 1
        elif j_next >= self.__max_col:
            j_next = 0
        return i_next, j_next

    def move(self, direction):
        next_board = Sokoban.copy_board(self.__board_history[-1])
        i, j = self.find_player()   # i = row, j = column
        current_board = self.__board_history[-1]

        if direction == 'a':
            x = 0
            y = -1
        elif direction == 'w':
            x = -1
            y = 0
        elif direction == 's':
            x = 1
            y = 0
        elif direction == 'd':
            x = 0
            y = 1
        else:
            return

        i_next, j_next = i + x, j + y
        i_next, j_next = self.__overflow_check(i_next, j_next)
        cell_next = current_board[i_next][j_next]
        
        if cell_next == ' ':
            next_board[i_next][j_next] = 'P'
            next_board[i][j] = ' '
            self.__board_history.append(next_board)
        elif cell_next == '*' or cell_next == 'o':
            return
        elif cell_next == '#':
            i_crate_next, j_crate_next = i_next + x, j_next + y
            i_crate_next, j_crate_next = self.__overflow_check(i_crate_next, j_crate_next)
            crate_next = next_board[i_crate_next][j_crate_next]
            
            if crate_next == '*':
                return
            elif crate_next == ' ':
                next_board[i_next][j_next] = 'P'
                next_board[i][j] = ' '
                next_board[i_crate_next][j_crate_next] = '#'
                self.__board_history.append(next_board)
            elif crate_next == 'o':
                next_board[i_next][j_next] = 'P'
                next_board[i][j] = ' '
                next_board[i_crate_next][j_crate_next] = ' '
                self.__board_history.append(next_board) 

    def get_board(self):
        return self.__board_history[-1]     
    
    def get_steps(self):
        return len(self.__board_history) - 1

    def restart(self):
        self.__board_history = self.__board_history[:1]
        
    def undo(self):
        if len(self.__board_history) > 1:
            self.__board_history.pop()
        
    def copy_board(board):
        board_copy = []
        for row in board:
            board_copy.append(list(row))
        return board_copy
        
    def __str__(self):
        result = ''
        for row in self.__board_history[-1]:
            result += ' '.join(row) + '\n'
        return result.strip()
    

def main(board):
    game = Sokoban(board)
    message = 'Press w/a/s/d to move, r to restart, or u to undo'
    print(message)
    while not game.complete():
        print(game)
        move = input('Move: ').lower()
        while move not in ('w', 'a', 's', 'd', 'r', 'u'):
            print('Invalid move.', message)
            move = input('Move: ').lower()
        if move == 'r':
            game.restart()
        elif move == 'u':
            game.undo()
        else:
            game.move(move)
    print(game)
    print(f'Game won in {game.get_steps()} steps!')

test_board = [
    ['*', 'o', '*'],
    ['*', '#', '*'],
    ['*', 'P', '*'],

]
main(test_board)
