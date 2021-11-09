import random
import copy
import turtle
from time import sleep
import matplotlib.pyplot as plt
dirr = [[0, 1], [1, 0], [-1, 0], [0, -1], [-1, -1], [1, 1], [-1, 1], [1, -1]]

# Author: Nisarg Patel

## GUI classes
class wPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(20)


class bPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(20)


class lbPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("navy")
        self.penup()
        self.speed(20)


class oePen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("orange")
        self.penup()
        self.speed(20)


class pPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(20)


class fPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed(20)


## EOF Gui classes

class cell:
    def __init__(self, position, current_state="C", surrounding_mines=-1, identified_safe=-1, identified_mines=-1,
                 hidden_squares=-1):
        self.current_state = current_state
        self.position = position
        self.surrounding_mines = surrounding_mines
        self.identified_safe = identified_safe
        self.identified_mines = identified_mines
        self.hidden_squares = hidden_squares

    def __str__(self):
        return str(self.current_state)

    def mark_safe(self, game_gui):
        # print("Check: {}".format(self.position))
        self.current_state = "S"
        if game_gui:
            write_game(self.position[0], self.position[1], wpen)
        # self.hidden_squares = find_in_neighbours(agent_board, self.position, "C")
        # self.identified_safe = find_in_neighbours(agent_board, self.position, "S")
        # self.identified_mines = find_in_neighbours(agent_board, self.position, "M")

    def mark_mine(self, game_gui):
        self.current_state = "M"
        if game_gui:
            write_game(self.position[0], self.position[1], oepen)


class Knowledge:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        if self.cells == other.cells and self.count == other.count:
            return True
        return False

    def mark_safe(self, cell, game_gui):
        if game_gui:
            write_game(cell[0], cell[1], wpen)
        if cell not in self.cells:
            return
        new_cells = set()
        for item in self.cells:
            if item != cell:
                new_cells.add(item)
        self.cells = new_cells

    def mark_mine(self, cell, game_gui):
        if game_gui:
            write_game(cell[0], cell[1], oepen)
        if cell not in self.cells:
            return
        new_cells = set()

        for item in self.cells:
            if item == cell:
                self.count -= 1
                continue
            else:
                new_cells.add(item)
        self.cells = new_cells


class Knowledge_Base:
    def __init__(self):
        self.knowledge_bank = []
        self.mines = set()
        self.safes = set()
        self.moves = set()
        self.visited = set()

    def set_safe(self, cell, game_gui):
        self.safes.add(cell)
        if game_gui:
            write_game(cell[0], cell[1], wpen)
        for info in self.knowledge_bank:
            info.mark_safe(cell, game_gui)

    def set_mins(self, cell, game_gui):
        self.mines.add(cell)
        if game_gui:
            write_game(cell[0], cell[1], oepen)
        for info in self.knowledge_bank:
            info.mark_mine(cell, game_gui)

    def add_knowledge(self, cell, clue, new_knowledge, agent_board):
        self.moves.add(cell)
        self.safes.add(cell)
        self.knowledge_bank.append(new_knowledge)

        # adding to safe and mine
        for knowledge in self.knowledge_bank:
            if len(knowledge.cells) == knowledge.count:
                for k_cell in knowledge.cells:
                    self.mines.add(k_cell)
                self.knowledge_bank.remove(knowledge)
            elif knowledge.count == 0:
                for k_cell in knowledge.cells:
                    self.safes.add(k_cell)
                self.knowledge_bank.remove(knowledge)

        for knowledge in self.knowledge_bank:
            for k_cell in knowledge.cells.copy():
                if k_cell in self.safes or k_cell in self.mines:
                    knowledge.cells.remove(k_cell)
                    if k_cell in self.mines:
                        knowledge.count -= 1

        knowledge_to_add = []
        for knowledge1 in self.knowledge_bank.copy():
            for knowledge2 in self.knowledge_bank.copy():
                if knowledge1 == knowledge2:
                    continue
                if knowledge1.cells.issubset(knowledge2.cells):
                    new_cells = knowledge2.cells - knowledge1.cells
                    new_count = knowledge2.count - knowledge1.count  # new count is 0 then set all cells to safe.
                    new_sentence = Knowledge(new_cells, new_count)
                    knowledge_to_add.append(new_sentence)
                    self.knowledge_bank.remove(knowledge2)
        for k in knowledge_to_add:
            if k not in self.knowledge_bank:
                self.knowledge_bank.append(k)

    def get_safe_move(self):
        for k_cell in self.safes:
            if k_cell not in self.moves:  # self.visited
                return k_cell
        return None

    def get_random_move(self, dim):
        choice = random.Random()
        while len(self.safes) + len(self.mines) < dim * dim:
            i = choice.randint(0, dim - 1)
            j = choice.randint(0, dim - 1)
            if (i, j) in self.moves:
                continue
            if (i, j) in self.mines:
                continue
            return [i, j]
        return None


def give_prob_based_on_position(position, agent_board, AI_knowledge_base):
    global dirr
    mine_count = 1
    neighbour_count = 1
    for direction in dirr:
        x = position[0] + direction[0]
        y = position[1] + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size:
            neighbour_count += 1
            if agent_board[x][y].current_state == "M" or position in AI_knowledge_base.mines:
                mine_count += 1
    return mine_count / neighbour_count


def insert_into_temp_prob(current_prob, location, temp_prob):
    if len(temp_prob) == 0:
        temp_prob.append((current_prob, location))
    elif temp_prob[0][0] == current_prob:
        temp_prob.append((current_prob, location))
    elif current_prob < temp_prob[0][0]:
        temp_prob = []
        temp_prob.append((current_prob, location))
    return temp_prob


def get_best_random_move_based_on_prob(board_size, AI_knowledge_base, number_of_mines):
    temp_prob = []
    number_of_explored_cells = len(AI_knowledge_base.visited)
    number_of_unexplored_cells = board_size * board_size - number_of_explored_cells
    number_of_mines_remaining = number_of_mines - len(AI_knowledge_base.mines)

    for i in range(board_size):
        for j in range(board_size):
            item = (i, j)
            in_bank = False
            if item in AI_knowledge_base.mines:
                continue
            if item in AI_knowledge_base.moves:
                continue
            for knowledge in AI_knowledge_base.knowledge_bank:
                if item in knowledge.cells:
                    current_prob = knowledge.count / len(knowledge.cells)
                    temp_prob = insert_into_temp_prob(current_prob, item, temp_prob)
                    in_bank = True
            if not in_bank:
                current_prob = number_of_mines_remaining / number_of_unexplored_cells
                temp_prob = insert_into_temp_prob(current_prob, item, temp_prob)

    if len(temp_prob) == 0:
        return None
    index = random.randrange(len(temp_prob))
    return temp_prob[index][1]


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


def set_hidden_neighbours(agent_board, position, to_set, list, unexplored_squares, draw_gui):
    global dirr
    for direction in dirr:
        x = position[0] + direction[0]
        y = position[1] + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size and agent_board[x][y].current_state == "C":
            agent_board[x][y].current_state = to_set
            if to_set == "M" and draw_gui:
                write_game(x,y,oepen)
            if to_set == "S" and draw_gui:
                write_game(x, y, wpen)
            list.append([x, y])
            unexplored_squares.remove([x, y])


def fill_unexplored_squares(board_size):
    unexplored_squares = []
    for i in range(board_size):
        for j in range(board_size):
            unexplored_squares.append([i, j])
    return unexplored_squares


def get_hidden_neighbour_positions(current_cell, agent_board):
    pos = []
    global dirr
    [row, col] = current_cell
    for direction in dirr:
        x = row + direction[0]
        y = col + direction[1]
        if 0 <= x < board_size and 0 <= y < board_size:  # and agent_board[x][y].current_state == "C":
            pos.append((x, y))
    return pos


def ai_agent(board_size, solution_board, agent_board, make_smarter, game_gui):
    AI_knowledge_base = Knowledge_Base()
    boom_count = 0
    while len(AI_knowledge_base.visited) != board_size * board_size:
        # print(AI_knowledge_base.mines)
        # sleep(0.5)
        valid_move = AI_knowledge_base.get_safe_move()
        if valid_move is not None:
            # there are safe cells that we can explore
            current_cell = valid_move
            AI_knowledge_base.visited.add(current_cell)
            agent_board[current_cell[0]][current_cell[1]].mark_safe(game_gui)
            neighbours = get_hidden_neighbour_positions(current_cell, agent_board)
            clue = get_surrounding_mines(solution_board, current_cell[0], current_cell[1], board_size)
            curr_knowledge = Knowledge(neighbours, clue)
            AI_knowledge_base.add_knowledge(current_cell, clue, curr_knowledge, agent_board)
            # add_knowledge(knowledge_base, current_cell, explored_mines, agent_board, safe_cells, solution_board,
            # unexplored_squares)
        else:
            # make random move
            valid_move = AI_knowledge_base.get_random_move(board_size)
            # smart AI based on prob
            if make_smarter:
                valid_move = get_best_random_move_based_on_prob(board_size, AI_knowledge_base, number_of_mines)
            if valid_move is None:
                break
            [row, col] = valid_move
            current_cell = agent_board[row][col].position
            AI_knowledge_base.visited.add(current_cell)

            if solution_board[row][col] == 0:
                # valid random-move, then update the knowledge base
                agent_board[row][col].mark_safe(game_gui)
                neighbours = get_hidden_neighbour_positions(current_cell, agent_board)
                clue = get_surrounding_mines(solution_board, current_cell[0], current_cell[1], board_size)
                curr_knowledge = Knowledge(neighbours, clue)
                AI_knowledge_base.add_knowledge(current_cell, clue, curr_knowledge, agent_board)
                # add_knowledge(knowledge_base, current_cell, explored_mines, agent_board, safe_cells, solution_board,
                # unexplored_squares)
            else:
                # random-move detected a mine
                (row, col) = valid_move
                AI_knowledge_base.set_mins((row, col),game_gui)
                agent_board[row][col].mark_mine(game_gui)
                # print("BOOM")
                boom_count += 1
    return boom_count


def ai_agent_knowing_mines(board_size, solution_board, agent_board, number_of_mines,  make_smarter, game_gui):
    AI_knowledge_base = Knowledge_Base()
    boom_count = 0
    while len(AI_knowledge_base.mines) != number_of_mines:
        # print(AI_knowledge_base.mines)
        # sleep(0.5)
        valid_move = AI_knowledge_base.get_safe_move()
        if valid_move is not None:
            # there are safe cells that we can explore
            current_cell = valid_move
            AI_knowledge_base.visited.add(current_cell)
            agent_board[current_cell[0]][current_cell[1]].mark_safe(game_gui)
            neighbours = get_hidden_neighbour_positions(current_cell, agent_board)
            clue = get_surrounding_mines(solution_board, current_cell[0], current_cell[1], board_size)
            curr_knowledge = Knowledge(neighbours, clue)
            AI_knowledge_base.add_knowledge(current_cell, clue, curr_knowledge, agent_board)
            # add_knowledge(knowledge_base, current_cell, explored_mines, agent_board, safe_cells, solution_board,
            # unexplored_squares)
        else:
            # make random move
            valid_move = AI_knowledge_base.get_random_move(board_size)
            # smart AI based on prob
            if make_smarter:
                valid_move = get_best_random_move_based_on_prob(board_size, AI_knowledge_base, number_of_mines)
            if valid_move is None:
                break
            [row, col] = valid_move
            current_cell = agent_board[row][col].position
            AI_knowledge_base.visited.add(current_cell)

            if solution_board[row][col] == 0:
                # valid random-move, then update the knowledge base
                agent_board[row][col].mark_safe(game_gui)
                neighbours = get_hidden_neighbour_positions(current_cell, agent_board)
                clue = get_surrounding_mines(solution_board, current_cell[0], current_cell[1], board_size)
                curr_knowledge = Knowledge(neighbours, clue)
                AI_knowledge_base.add_knowledge(current_cell, clue, curr_knowledge, agent_board)
                # add_knowledge(knowledge_base, current_cell, explored_mines, agent_board, safe_cells, solution_board,
                # unexplored_squares)
            else:
                # random-move detected a mine
                (row, col) = valid_move
                AI_knowledge_base.set_mins((row, col),game_gui)
                agent_board[row][col].mark_mine(game_gui)
                # print("BOOM")
                boom_count += 1
    return boom_count



def basic_agent(board_size, solution_board, agent_board, draw_gui, oepen, wpen):
    explored_mines = []
    explored_safe = []
    boom_count = 0
    unexplored_squares = fill_unexplored_squares(board_size)
    while len(explored_safe) + len(explored_mines) != board_size ** 2:
        #sleep(0.5)
        [row, col] = get_random_cell(board_size, agent_board, unexplored_squares)
        unexplored_squares.remove([row, col])
        if solution_board[row][col] == 0:
            explored_safe.append([row, col])
            clue = get_surrounding_mines(solution_board, row, col, board_size)
            agent_board[row][col].surrounding_mines = clue
            agent_board[row][col].current_state = "S"
            if draw_gui:
                write_game(row, col, wpen)
            agent_board[row][col].hidden_squares = find_in_neighbours(agent_board, [row, col], "C")
            agent_board[row][col].identified_safe = find_in_neighbours(agent_board, [row, col], "S")
            agent_board[row][col].identified_mines = find_in_neighbours(agent_board, [row, col], "M")
            if check_remaining_mines(agent_board[row][col]):
                set_hidden_neighbours(agent_board, [row, col], "M", explored_mines, unexplored_squares, draw_gui)
            if check_remaining_safes(board_size, [row, col], agent_board[row][col]):
                set_hidden_neighbours(agent_board, [row, col], "S", explored_safe, unexplored_squares, draw_gui)
        else:
            #print("BOOM")
            explored_mines.append([row, col])
            agent_board[row][col].current_state = "M"
            if draw_gui:
                write_game(row, col, oepen)
            boom_count += 1
    return boom_count


def create_board(board_size):
    board = []
    for i in range(board_size):
        col = []
        for j in range(board_size):
            col.append(cell((i, j)))
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


def write_game(x, y, pen):
    screen_x = -288 + (y * 24)
    screen_y = 288 - (x * 24)
    pen.goto(screen_x, screen_y)
    pen.stamp()


def setup_game(dim, bpen):
    for i in range(dim):
        for j in range(dim):
            write_game(i, j, bpen)


if __name__ == '__main__':

    # Input variables
    board_size = 20
    number_of_mines = 25


    boom_count_basic = 0
    boom_count_normal = 0
    boom_count_smartai = 0

    ## Activating GUI
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Maze game")
    wn.setup(600, 600)
    wpen = wPen()
    oepen = oePen()
    bpen = bPen()
    setup_game(board_size, bpen)

    
    # single minecraft game with GUI
    game_board = create_game(board_size)
    game_board = add_mines(game_board, board_size, number_of_mines)

    # AI agent
    agent_board = create_board(board_size)
    boom_count_basic += basic_agent(board_size, game_board, agent_board,True,oepen,wpen)
    agent_board = create_board(board_size)
    setup_game(board_size, bpen)

    boom_count_normal += ai_agent(board_size, game_board, agent_board,False,True)
    agent_board = create_board(board_size)

    # AI agent with Knowledge base
    setup_game(board_size, bpen)
    boom_count_smartai += ai_agent(board_size, game_board, agent_board,True, True)
    print(boom_count_basic, boom_count_normal, boom_count_smartai)
    wn.exitonclick()
    exit(0)

    # This is for accuracy purpose to get the success rate
    mines = []
    basic_agent_success = []
    ai_agent_success = []
    smart_ai_success = []

    number_of_mines = 1
    while number_of_mines != 100:
        print(number_of_mines)
        boom_count_basic = 0
        boom_count_normal = 0
        boom_count_smartai = 0
        for i in range(100):
            # print(i)
            game_board = create_game(board_size)
            game_board = add_mines(game_board, board_size, number_of_mines)

            agent_board = create_board(board_size)
            # game_board_copy = copy.deepcopy(agent_board)
            boom_count_basic += basic_agent(board_size, game_board, agent_board,False, None, None)
            agent_board = create_board(board_size)

            boom_count_normal += ai_agent(board_size, game_board, agent_board, False, False)
            agent_board = create_board(board_size)
            boom_count_smartai += ai_agent(board_size, game_board, agent_board, True, False)
        mines.append(number_of_mines)
        basic_agent_success.append(100*(100*number_of_mines - boom_count_basic)/(100*number_of_mines))
        ai_agent_success.append(100*(100*number_of_mines - boom_count_normal)/(100*number_of_mines))

        smart_ai_success.append(100*(100*number_of_mines - boom_count_smartai)/(100*number_of_mines))
        number_of_mines += 1
        print(boom_count_basic, boom_count_normal, boom_count_smartai)

    plt.plot(mines, basic_agent_success, label="Basic agent")
    plt.plot(mines, ai_agent_success, label="AI agent")
    plt.plot(mines, smart_ai_success, label="Smart AI agent (decision based on probability)")
    plt.ylabel("Success Rate")
    plt.xlabel("Number of mines")
    plt.legend()
    plt.show()



