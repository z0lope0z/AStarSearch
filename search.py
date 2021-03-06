import math
import time
import heapq

def display(nodes):
    '''
    Helper function to display the nodes in a list
    '''
    return '%s' % ', '.join(map(str, nodes))

class Node:
    current_cost = None

    def __init__(self, x, y, value, board):
        self.x = x
        self.y = y
        self.current_cost = 0
        self.value = value
        self.board = board
        self.parent = None
        self.g_score = None
        self.f_score = None

    def traverse(self, next_node, cost):
        next_node.parent = self
        next_node.current_cost = cost

    def compute_path_cost(self, astar_search, node, amount):
        path = self.collect_parents(self, [])
        cost = 0
        previous = self
        for node in path:
            cost = cost + astar_search._movement_cost(previous, node)
            previous = node
        return cost
    
    def collect_parents(self, node, parents):
        node = self
        parents=[]
        while (node.parent is not None):
            parents.append(node)
            node = node.parent
        parents.append(node)
        return parents

    def get_neighbors(self):
        neighbors = self._get_neighbors_unclean(self)
        return_neighbors = []
        for neighbor in neighbors:
            try:
                node = self.board.get_node(neighbor.x, neighbor.y)
                if node.value != 1 and neighbor != None:
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

    def __eq__(self, another):
        try:
            return self.x == another.x and self.y == another.y
        except AttributeError:
            return self.x == another[1].x and self.y == another[1].y

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
        self.matrix[y][x] = node 

    def get_node(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.matrix[y][x]
        except:
            return None
    

class Search():
    cost_upper_left, cost_left, cost_lower_left, cost_bottom, cost_lower_right, cost_right, cost_upper_right, cost_top = 1, 1, 1, 1, 1, 1, 1, 1

    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node
        self.open_nodes = []
        self.closed_nodes = []

    def backtrack(self, path, node, cost, total):
        if node == self.start_node:
            path.append(self.start_node)
            total = cost
            return total, path
        else:
            path.append(node)
            cost = cost + self._movement_cost(node, node.parent)
            total, path2 = self.backtrack(path, node.parent, cost, total)
            return total, path

    def _heuristic(self, node):
        x_diff = abs(node.x-self.end_node.x)
        y_diff = abs(node.y-self.end_node.y)
        return math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2))

    def _movement_cost(self, node, neighbor):
        if node.x - 1 == neighbor.x:
            if neighbor.y + 1 == node.y:
                return self.cost_upper_left
            elif neighbor.y == node.y:
                return self.cost_left
            elif neighbor.y - 1 == node.y:
                return self.cost_lower_left
        elif node.x == neighbor.x:
            if neighbor.y + 1 == node.y:
                return self.cost_top
            elif neighbor.y == node.y:
                return 0
            elif neighbor.y - 1 == node.y:
                return self.cost_bottom 
        elif node.x + 1 == neighbor.x:
            if neighbor.y + 1 == node.y:
                return self.cost_upper_right
            elif neighbor.y == node.y:
                return self.cost_right
            elif neighbor.y - 1 == node.y:
                return self.cost_lower_right
        raise Exception('cost not found exception')

    def set_movement_cost(self, left, down, right, up, diagonal):
        self.cost_upper_left, self.cost_upper_right, self.cost_lower_left, self.cost_lower_right = diagonal, diagonal, diagonal, diagonal
        self.cost_left, self.cost_down, self.cost_right, self.cost_up = left, down, right, up 

class GreedyBFS(Search):

    def search(self):
        open_nodes = []
        heapq.heappush(open_nodes, (0, self.start_node))
        while (open_nodes):
            self.current_node = heapq.heappop(open_nodes)[1]
            if self.current_node == self.end_node:
                path = []
                total, path = self.backtrack(path, self.current_node, 0, 0)
                return total, path 
            self.closed_nodes.append(self.current_node)
            for neighbor in self.current_node.get_neighbors():
                score = self._heuristic(neighbor)
                if neighbor in self.closed_nodes and score >= neighbor.f_score:
                   continue 
                if neighbor not in open_nodes or score < neighbor.f_score:
                    neighbor.parent = self.current_node
                    # recycle f_score as score
                    neighbor.f_score = score 
                    if neighbor not in open_nodes:
                        heapq.heappush(open_nodes, (score, neighbor))


class AStarSearch(Search):

    def search(self):
        self.open_nodes = []
        heapq.heappush(self.open_nodes, (0, self.start_node))
        while (self.open_nodes):
            self.current_node = heapq.heappop(self.open_nodes)[1]
            if self.current_node == self.end_node:
                path = []
                total, path = self.backtrack(path, self.current_node, 0, 0)
                return total, path 
            self.closed_nodes.append(self.current_node)
            for neighbor in self.current_node.get_neighbors():
                tentative_g_score = self.current_node.compute_path_cost(self, None, 0) + self._movement_cost(self.current_node, neighbor)
                tentative_f_score = tentative_g_score + self._heuristic(neighbor)
                if neighbor in self.closed_nodes and tentative_f_score >= neighbor.f_score:
                   continue 
                if neighbor not in self.open_nodes or tentative_f_score < neighbor.f_score:
                    neighbor.parent = self.current_node
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_f_score 
                    if neighbor not in self.open_nodes:
                        heapq.heappush(self.open_nodes, (neighbor.f_score, neighbor)) 


class Runner():
    def __init__(self):
        self.board = None
        self.a_star_search = None
        self.greedy_search = None
        self.start_node = None
        self.end_node = None

    def read_file(self):
        with open('input.txt','r') as file:
            rows = []
            x, y = 0, 0
            self.start_node = None
            self.end_node = None
            self.cost_up, self.cost_down, self.cost_left, self.cost_right, self.cost_diagonal = None, None, None, None, None
            for (i, line) in enumerate(file):
                if i == 0:
                    y, x = line.split()
                    y, x = int(x), int(y)
                    self.board = Board(rows=y, columns=x)
                elif i <= x:
                    rows.append(line.split())
                else:
                    self.board.fill(rows)
                    if line.startswith('Source'):
                        y, x = self._convert_coordinates(int(line.split()[1]), int(line.split()[2]))
                        self.start_node = self.board.get_node(x, y)
                    elif line.startswith('Destination'):
                        y, x = self._convert_coordinates(int(line.split()[1]), int(line.split()[2]))
                        self.end_node = self.board.get_node(x, y)
                    elif line.startswith('Up'):
                        self.cost_up = float(line.split()[1])
                    elif line.startswith('Down'):
                        self.cost_down = float(line.split()[1])
                    elif line.startswith('Left'):
                        self.cost_left = float(line.split()[1])
                    elif line.startswith('Right'):
                        self.cost_right = float(line.split()[1])
                    elif line.startswith('Diagonal'):
                        self.cost_diagonal = float(line.split()[1])

    def scan_greedy(self):
        self.greedy_bfs_search = GreedyBFS(self.start_node, self.end_node)
        self.greedy_bfs_search.set_movement_cost(self.cost_up, self.cost_down, self.cost_left, self.cost_right, self.cost_diagonal)
        total_cost, path = self.greedy_bfs_search.search()
        path.reverse()
        with open('greedy.out', 'w') as write_greedy:
            for node in path:
                write_greedy.write('%d %d\n' % (node.y, node.x))
            write_greedy.write('%s' % total_cost)

    def scan_astar(self):
        self.a_star_search = AStarSearch(self.start_node, self.end_node)
        self.a_star_search.set_movement_cost(self.cost_up, self.cost_down, self.cost_left, self.cost_right, self.cost_diagonal)
        total_cost, path = self.a_star_search.search()
        path.reverse()
        with open('astar.out', 'w') as write_astar:
            for node in path:
                write_astar.write('%d %d\n' % (node.y, node.x)),
            write_astar.write('%s' % total_cost)

    def _convert_coordinates(self, x, y):
        return x, y

runner = Runner()
runner.read_file()
runner.scan_greedy()
runner = Runner()
runner.read_file()
runner.scan_astar()
