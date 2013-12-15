import pdb
import math
import time


class Node:
    current_cost = None

    def __init__(self, x, y, value, board):
        self.x = x
        self.y = y
        self.current_cost = 0
        self.value = value
        self.board = board
        self.parent = None

    def traverse(self, next_node, cost):
        next_node.parent = self
        next_node.current_cost = cost

    def get_neighbors(self):
        neighbors = self._get_neighbors_unclean(self)
        return_neighbors = []
        for neighbor in neighbors:
            try:
                node = self.board.get_node(neighbor.x, neighbor.y)
                if node.value != 1 and neighbor != None and node.current_cost == 0:
                    return_neighbors.append(node)
            except AttributeError:
                pass
            except IndexError:
                pass
        return return_neighbors

    def _get_neighbors_unclean(self, neighbors):
        neighbors = []
        neighbors.append(self.board.get_node(self.x-1, self.y+1))
        neighbors.append(self.board.get_node(self.x-1, self.y))
        neighbors.append(self.board.get_node(self.x-1, self.y-1))
        neighbors.append(self.board.get_node(self.x, self.y+1))
        neighbors.append(self.board.get_node(self.x+1, self.y+1))
        neighbors.append(self.board.get_node(self.x+1, self.y))
        neighbors.append(self.board.get_node(self.x+1, self.y-1))
        neighbors.append(self.board.get_node(self.x, self.y-1))                                          
        return neighbors

    def __str__(self):
        return "%d,%d" % (self.x, self.y)

class Board:

    def __init__(self, rows, columns):
        self.matrix = [[None]*rows for i in range(columns)]

    def fill(self, rows):
        for (i, row) in enumerate(rows):
            for (j, item) in enumerate(row):
                node = Node(x=j, y=i, value=int(item), board=self)
                self.matrix[i][j] = node
        return self.matrix 

    def set_node(self, x, y, node):
        self.matrix[x][y] = node 

    def get_node(self, x, y):
        try:
            return self.matrix[x][y]
        except:
            return None
    

class AStarSearch:
    cost_upper_left, cost_left, cost_lower_left, cost_bottom, cost_lower_right, cost_right, cost_upper_right, cost_top = 1, 1, 1, 1, 1, 1, 1, 1

    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node
        self.open_nodes = []

    def search(self):
        open_nodes= []
        while (self._compute_distance(self.current_node, self.end_node) != 0):
            open_nodes.append(self.current_node)
            self.current_node, is_shift = self._check_open_nodes()
            nearest_node = self._get_nearest_neighbor(self.current_node)
            print "moving from %d,%d to %d,%d" % (self.current_node.x, self.current_node.y, nearest_node.x, nearest_node.y)
            self._move(nearest_node)
            time.sleep(1)
        path = []
        self.backtrack(path, self.current_node)
        return path 
    
    def backtrack(self, path, node):
        if node == self.start_node:
            path.append(self.start_node)
            return path.reverse()
        else:
            path.append(node)
            self.backtrack(path, node.parent)

    def _move(self, node):
        movement_cost = self._movement_cost(self.current_node, node) 
        self.current_node.traverse(node, movement_cost)
        self.current_node = node

    def _check_open_nodes(self):
        cheapest_node = self.current_node
        is_shift = False
        for node in self.open_nodes:
            if self.current_node.current_cost < node.current_cost:
                cheapest_node = node
                is_shift = True
        return cheapest_node, is_shift 

    def _get_nearest_neighbor(self, node):
        neighbors = node.get_neighbors()
        print "node: %s,%s" % (node.x, node.y)
        try:
            if neighbors:
                nearest_neighbor = neighbors[0]
                for neighbor in neighbors:
                    print "%s,%s cost: %f value: %d" % (neighbor.x, neighbor.y, self._compute_distance(node, neighbor), neighbor.value)
                    distance = self._compute_distance(node, neighbor)
                    if distance < self._compute_distance(node, nearest_neighbor):
                        nearest_neighbor = neighbor
        except Exception, e:
            pdb.set_trace()
        return nearest_neighbor

    def _compute_distance(self, node, neighbor):
        movement_cost = self._movement_cost(node, neighbor)
        if movement_cost == 0:
            return 0
        comp = movement_cost + self._heuristic(neighbor) + self.current_node.current_cost
        return comp

    def _heuristic(self, node):
        x_diff = abs(node.x-self.end_node.x)
        y_diff = abs(node.y-self.end_node.y)
        return math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2))

    def _movement_cost(self, node, neighbor):
        if node.x > neighbor.x:
            if neighbor.y > node.y:
                return self.cost_upper_left
            elif neighbor.y == node.y:
                return self.cost_left
            elif neighbor.y < node.y:
                return self.cost_right
        elif node.x == neighbor.x:
            if neighbor.y > node.y:
                return self.cost_top
            elif neighbor.y == node.y:
                return 0
            elif neighbor.y < node.y:
                return self.cost_bottom 
        elif node.x < neighbor.x:
            if neighbor.y > node.y:
                return self.cost_upper_right
            elif neighbor.y == node.y:
                return self.cost_right
            elif neighbor.y < node.y:
                return self.cost_lower_right
        pdb.set_trace()
        raise Exception('cost not found exception')

    def set_movement_cost(self, left, down, right, up, diagonal):
        self.cost_upper_left, self.cost_upper_right, self.cost_lower_left, self.cost_lower_right = diagonal, diagonal, diagonal, diagonal
        self.cost_left, self.cost_down, self.cost_right, self.cost_up = left, down, right, up 

class Runner():
    def __init__(self):
        self.board = None
        self.a_star_search = None
        self.greedy_search = None

    def read_file(self):
        import pdb
        with open('input.txt','r') as file:
            rows = []
            x, y = 0, 0
            start_node = None
            end_node = None
            cost_up, cost_down, cost_left, cost_right, cost_diagonal = None, None, None, None, None
            for (i, line) in enumerate(file):
                if i == 0:
                    x, y = line.split()
                    x, y = int(x), int(y)
                    self.board = Board(x, y)
                elif i <= y:
                    rows.append(line.split())
                else:
                    print line
                    self.board.fill(rows)
                    if line.startswith('Source'):
                        x, y = self._convert_coordinates(int(line.split()[1]), int(line.split()[2]))
                        start_node = self.board.get_node(x, y)
                    elif line.startswith('Destination'):
                        x, y = self._convert_coordinates(int(line.split()[1]), int(line.split()[2]))
                        end_node = self.board.get_node(x, y)
                    elif line.startswith('Up'):
                        cost_up = int(line.split()[1])
                    elif line.startswith('Down'):
                        cost_down = int(line.split()[1])
                    elif line.startswith('Left'):
                        cost_left = int(line.split()[1])
                    elif line.startswith('Right'):
                        cost_right = int(line.split()[1])
                    elif line.startswith('Diagonal'):
                        cost_diagonal = int(line.split()[1])
        self.a_star_search = AStarSearch(start_node, end_node)
        self.a_star_search.set_movement_cost(cost_up, cost_down, cost_left, cost_right, cost_diagonal)
        path = self.a_star_search.search()
        for node in path:
            print('%d,%d' % (node.x, node.y)),
        pdb.set_trace()
    
    def _convert_coordinates(self, x, y):
        return y, x

runner = Runner()
runner.read_file()
pdb.set_trace()   
board = Board(5,5)
board.get_node(2,2)
pdb.set_trace()
