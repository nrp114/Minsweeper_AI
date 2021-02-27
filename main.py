import random

dirr = [[0, 1], [1, 0], [-1, 0], [0, -1], [-1, -1], [1, 1], [-1, 1], [1, -1]]


class cell:
    def __init__(self, current_state="C", surrounding_mines=-1, identified_safe=-1, identified_mines=-1,
                 hidden_squares=-1):
        self.current_state = current_state
        self.surrounding_mines = surrounding_mines
        self.identified_safe = identified_safe
        self.identified_mines = identified_mines
        self.hidden_squares = hidden_squares

    def __str__(self):
        return str(self.current_state)


def check_remaining_mines(current_cell):
    explored_mines = current_cell.identified_mines
    clue = current_cell.surrounding_mines
    if clue - explored_mines == current_cell.hidden_squares:
        return True
    return False


def check_remaining_safes(board_size, position, current_cell):
    total_neighbours = valid_neighbours(position[0], position[1], board_size)
    safe_neighbour = current_cell.identified_safe
    clue = current_cell.surrounding_mines
    if (total_neighbours - clue) - safe_neighbour == current_cell.hidden_squares:
        return True
    return False


def get_random_cell(board_size, agent_board, unexplored_squares):
    pos_index = random.randrange(len(unexplored_squares))
    position = unexplored_squares[pos_index]
    return position


def find_in_neighbours(agent_board, position, to_find):
    global dirr
    counter = 0
    for direction in dirr:
        x = position[0] + direction[0]
        y = position[1] + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size and agent_board[x][y].current_state == to_find:
            counter += 1
    return counter


def set_hidden_neighbours(agent_board, position, to_set, list, unexplored_squares):
    global dirr
    for direction in dirr:
        x = position[0] + direction[0]
        y = position[1] + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size and agent_board[x][y].current_state == "C":
            agent_board[x][y].current_state = to_set
            list.append([x, y])
            unexplored_squares.remove([x, y])

def fill_unexplored_squares(board_size):
    unexplored_squares = []
    for i in range(board_size):
        for j in range(board_size):
            unexplored_squares.append([i, j])
    return unexplored_squares




def basic_agent(board_size, solution_board, agent_board):
    explored_mines = []
    explored_safe = []
    unexplored_squares = fill_unexplored_squares(board_size)
    while len(explored_safe) + len(explored_mines) != board_size**2:
        [row, col] = get_random_cell(board_size, agent_board, unexplored_squares)
        unexplored_squares.remove([row, col])
        if solution_board[row][col] == 0:
            explored_safe.append([row, col])
            clue = get_surrounding_mines(solution_board, row, col, board_size)
            agent_board[row][col].surrounding_mines = clue
            agent_board[row][col].current_state = "S"
            agent_board[row][col].hidden_squares = find_in_neighbours(agent_board, [row, col], "C")
            agent_board[row][col].identified_safe = find_in_neighbours(agent_board, [row, col], "S")
            agent_board[row][col].identified_mines = find_in_neighbours(agent_board, [row, col], "M")
            if check_remaining_mines(agent_board[row][col]):
                set_hidden_neighbours(agent_board,[row, col], "M", explored_mines, unexplored_squares)
            if check_remaining_safes(board_size, [row, col], agent_board[row][col]):
                set_hidden_neighbours(agent_board,[row, col], "S", explored_safe, unexplored_squares)
        else:
            print("BOOM")
            explored_mines.append([row, col])
            agent_board[row][col].current_state = "M"
    return agent_board

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
    print(" ---------------------")
    basic_agent(board_size, game_board, agent_board)
    printLine(agent_board)

