import random
import copy

dirr = [[0, 1], [1, 0], [-1, 0], [0, -1], [-1, -1], [1, 1], [-1, 1], [1, -1]]


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

    def mark_safe(self):
        #print("Check: {}".format(self.position))
        self.current_state = "S"
        # self.hidden_squares = find_in_neighbours(agent_board, self.position, "C")
        # self.identified_safe = find_in_neighbours(agent_board, self.position, "S")
        # self.identified_mines = find_in_neighbours(agent_board, self.position, "M")

    def mark_mine(self):
        self.current_state = "M"


class Knowledge:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        if self.cells == other.cells and self.count == other.count:
            return True
        return False

    def mark_safe(self, cell):
        if cell not in self.cells:
            return
        new_cells = set()

        for item in self.cells:
            if item != cell:
                new_cells.add(item)
        self.cells = new_cells

    def mark_mine(self, cell):
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

    def set_safe(self, cell):
        self.safes.add(cell)
        for info in self.knowledge_bank:
            info.mark_safe(cell)

    def set_mins(self, cell):
        self.mines.add(cell)
        for info in self.knowledge_bank:
            info.mark_mine(cell)

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
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
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
    return mine_count/neighbour_count

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
    number_of_unexplored_cells = board_size*board_size - number_of_explored_cells
    number_of_mines_remaining = number_of_mines - len(AI_knowledge_base.mines)

    for i in range(board_size):
        for j in range(board_size):
            item = (i,j)
            in_bank = False
            if item in AI_knowledge_base.mines:
                continue
            if item in AI_knowledge_base.moves:
                continue
            for knowledge in AI_knowledge_base.knowledge_bank:
                if item in knowledge.cells:
                    current_prob = knowledge.count / len(knowledge.cells)
                    temp_prob = insert_into_temp_prob(current_prob, item,  temp_prob)
                    in_bank = True
            if not in_bank:
                current_prob = number_of_mines_remaining/number_of_unexplored_cells
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

"""""
def add_knowledge(knowledge_base, current_cell, explored_mines, agent_board, safe_cells, solution_board,
                  unexplored_squares):
    neighbours = get_hidden_neighbour_positions(current_cell, agent_board)
    clue = get_surrounding_mines(solution_board, current_cell.position[0], current_cell.position[1], board_size)
    if len(neighbours) != 0:
        new_knowledge = Knowledge(neighbours, clue)
        knowledge_base.append(new_knowledge)

    knowledge_base.append(Knowledge([(current_cell.position[0], current_cell.position[1])], 0))
    # infer
    knowledge_to_add = []
    for sentence in knowledge_base:
        if len(sentence.cells) > 1:
            if sentence.count == 0:
                # add to safe
                for cell_pos in sentence.cells:
                    row = cell_pos[0]
                    col = cell_pos[1]
                    safe_cells.append(agent_board[row][col])
                    knowledge_to_add.append(Knowledge([(row, col)], 0))
                knowledge_base.remove(sentence)
            elif sentence.count == len(sentence.cells):
                for cell_pos in sentence.cells:
                    row = cell_pos[0]
                    col = cell_pos[1]
                    explored_mines.append(agent_board[row][col])
                    agent_board[row][col].current_state = "M"
                    # unexplored_squares.remove([row,col])
                    knowledge_to_add.append(Knowledge([(row, col)], 1))
                knowledge_base.remove(sentence)

    for sentence1 in knowledge_base:
        for sentence2 in knowledge_base:
            if sentence1 == sentence2:
                continue
            if sentence1.cells == sentence2.cells:
                continue
            if sentence1.cells.issubset(sentence2.cells):
                new_cells = sentence2.cells - sentence1.cells
                new_count = sentence2.count - sentence1.count
                new_sentence = Knowledge(new_cells, new_count)
                knowledge_to_add.append(new_sentence)
                # knowledge_base.remove(sentence2)

    for sentence in knowledge_to_add:
        if sentence not in knowledge_base:
            knowledge_base.append(sentence)
"""""

def ai_agent(board_size, solution_board, agent_board, make_smarter):
    AI_knowledge_base = Knowledge_Base()
    boom_count = 0
    while len(AI_knowledge_base.visited) != board_size * board_size:
        #print(AI_knowledge_base.mines)
        valid_move = AI_knowledge_base.get_safe_move()
        if valid_move is not None:
            # there are safe cells that we can explore
            current_cell = valid_move
            AI_knowledge_base.visited.add(current_cell)
            agent_board[current_cell[0]][current_cell[1]].mark_safe()
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
                agent_board[row][col].mark_safe()
                neighbours = get_hidden_neighbour_positions(current_cell, agent_board)
                clue = get_surrounding_mines(solution_board, current_cell[0], current_cell[1], board_size)
                curr_knowledge = Knowledge(neighbours, clue)
                AI_knowledge_base.add_knowledge(current_cell, clue, curr_knowledge, agent_board)
                # add_knowledge(knowledge_base, current_cell, explored_mines, agent_board, safe_cells, solution_board,
                # unexplored_squares)
            else:
                # random-move detected a mine
                (row, col) = valid_move
                AI_knowledge_base.set_mins((row, col))
                agent_board[row][col].mark_mine()
                #print("BOOM")
                boom_count += 1
    return boom_count


def basic_agent(board_size, solution_board, agent_board):
    explored_mines = []
    explored_safe = []
    boom_count = 0
    unexplored_squares = fill_unexplored_squares(board_size)
    while len(explored_safe) + len(explored_mines) != board_size ** 2:
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
                set_hidden_neighbours(agent_board, [row, col], "M", explored_mines, unexplored_squares)
            if check_remaining_safes(board_size, [row, col], agent_board[row][col]):
                set_hidden_neighbours(agent_board, [row, col], "S", explored_safe, unexplored_squares)
        else:
            # print("BOOM")
            explored_mines.append([row, col])
            agent_board[row][col].current_state = "M"
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


if __name__ == '__main__':

    """""
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

    """""
    board_size = 10
    number_of_mines = 25
    boom_count_basic = 0
    boom_count_normal = 0
    boom_count_smartai = 0
    for i in range(100):
        print(i)
        game_board = create_game(board_size)
        game_board = add_mines(game_board, board_size, number_of_mines)

        agent_board = create_board(board_size)
        #game_board_copy = copy.deepcopy(agent_board)
        boom_count_basic += basic_agent(board_size, game_board, agent_board)
        agent_board = create_board(board_size)

        boom_count_normal += ai_agent(board_size, game_board, agent_board, make_smarter=False)
        agent_board = create_board(board_size)
        boom_count_smartai += ai_agent(board_size, game_board, agent_board, make_smarter=True)

        #printLine(agent_board)
        #print(" 00  ")
        #printLine(game_board)
        #print(" ---------------------")

        #printLine(agent_board)
    print(boom_count_basic, boom_count_normal , boom_count_smartai)
