import random

dirr = [[0, 1], [1, 0], [-1, 0], [0, -1], [-1, -1],[1, 1], [-1, 1], [1, -1]]


class cell:
    def __init__(self, current_state="C", surrounding_mines=-1, identified_safe=-1, identified_mines=-1, hidden_squares=-1):
        self.current_state = current_state
        self.surrounding_mines = surrounding_mines
        self.identified_safe = identified_safe
        self.identified_mines = identified_mines
        self.hidden_squares = hidden_squares

    def __str__(self):
        return str(self.current_state)


def check_remaining_mines(total_mines, board_size, explored_mines):


def check_remaining_safes():


def create_board(board_size):
    board = []
    for i in range(board_size):
        col = []
        for j in range(board_size):
            col.append(cell())
        board.append(col)
    return board


def create_game(board_size):
    board = []
    for i in range(board_size):
        col = []
        for j in range(board_size):
            col.append(0)
        board.append(col)
    return board


def add_mines(board, board_size, number_of_mines):
    temp = number_of_mines
    while temp != 0:
        a = random.randrange(board_size)
        b = random.randrange(board_size)
        if board[a][b] == 1:
            continue
        board[a][b] = 1
        temp -= 1
    return board


def valid_neighbours(row, col, board_size):
    global dirr
    node_count = 0
    for direction in dirr:
        x = row + direction[0]
        y = col + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size:
            node_count += 1
    return node_count


def get_surrounding_mines(board, row, col, board_size):
    global dirr
    mine_count = 0
    for direction in dirr:
        x = row + direction[0]
        y = col + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size and board[x][y] == 1:
            mine_count += 1
    return mine_count


def printLine(printG):
    for i in range(len(printG)):
        for j in printG[i]:
            print(j, end=" ")
        print()

if __name__ == '__main__':

    try:
        board_size = int(input("Enter Board size (d): "))
        if board_size <= 0:
            print("Board size should be a positive integer")
            exit(0)
        number_of_mines = int(input("Enter number of mines (n): "))
        if number_of_mines > board_size * board_size or number_of_mines <= 0:
            print("n should be a positive integer less than d*d ")
            exit(0)
    except:
        print("Error")
        exit(0)

    game_board = create_game(board_size)
    game_board = add_mines(game_board, board_size, number_of_mines)

    agent_board = create_board(board_size)

    printLine(agent_board)
    print(" 00  ")
    printLine(game_board)
