import pdb
import math
import time


def display(nodes):
    return '%s' % ', '.join(map(str, nodes))

def p(node):
    print "%s, %s" % (node.x, node.y)
    
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
        #print "path cost for node %s: %s" % (node, cost)
        return cost
        #return self.current_cost + compute_path_cost(self.parent.current_cost, 0)

    def collect_parents(self, node, parents):
        node = self
        parents=[]
        while (node.parent is not None):
            parents.append(node)
            node = node.parent
        parents.append(node)
        return parents
#recursion
        if not node.parent:
            print "-----"
            parents.append(node)
            pdb.set_trace()
            return parents
        parents.append(node)
        self.collect_parents(node, parents)
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
                print 'attribute error'
                pass
            except IndexError:
                print 'index error'
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
        pdb.set_trace()
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
    
import heapq
class AStarSearch:
    cost_upper_left, cost_left, cost_lower_left, cost_bottom, cost_lower_right, cost_right, cost_upper_right, cost_top = 1, 1, 1, 1, 1, 1, 1, 1

    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node
        self.open_nodes = []
        self.closed_nodes = []

    def search(self):
        open_nodes = []
        heapq.heappush(open_nodes, (0, self.start_node))
        while (open_nodes):
            self.current_node = heapq.heappop(open_nodes)[1]
            print "current node : %s" % self.current_node
            if self.current_node == self.end_node:
                path = []
                self.backtrack(path, self.current_node)
                return path                 
            self._update_closed_nodes(self.current_node)
            #pdb.set_trace()
            for neighbor in self.current_node.get_neighbors():
                tentative_g_score = neighbor.compute_path_cost(self, None, 0) + self._movement_cost(self.current_node, neighbor)
                tentative_f_score = tentative_g_score + self._heuristic(neighbor)
                print "neighbor %s with cost : %s" % (neighbor, tentative_f_score)
                if neighbor in self.closed_nodes and tentative_f_score >= neighbor.f_score:
                   continue 
                if neighbor not in open_nodes or tentative_f_score < neighbor.f_score:
                    neighbor.parent = self.current_node
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_f_score 
                    if neighbor not in open_nodes:
                        heapq.heappush(open_nodes, (neighbor.f_score, neighbor)) 
            #pdb.set_trace()

            #self.current_node, is_shift = self._check_open_nodes()
            #if is_shift:
            #    self._update_closed_nodes(self.current_node)
            #nearest_node = self._get_nearest_neighbor(self.current_node, self.closed_nodes)
            #if nearest_node:
            #    print "moving from %d,%d to %d,%d" % (self.current_node.x, self.current_node.y, nearest_node.x, nearest_node.y)
            #    self._move(nearest_node)
            #    self._update_closed_nodes(nearest_node)
            #else:
            #    print "found a dead end for %s"  % self.current_node
            #pdb.set_trace()
            time.sleep(1)

    
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
   
    def _update_closed_nodes(self, new_node):
         self.closed_nodes.append(new_node)
         #is_not_new_node = lambda x: x is not new_node
         #self.open_nodes = filter(is_not_new_node, self.open_nodes) 

    def _update_open_nodes(self):
        current_node_neighbors = self.current_node.get_neighbors()
        is_not_closed_node = lambda node: node not in self.closed_nodes
        current_node_neighbors = filter(is_not_closed_node, current_node_neighbors)
        for neighbor in current_node_neighbors:
            movement_cost = self._movement_cost(self.current_node, neighbor)
            if neighbor in self.open_nodes:
                if movement_cost < self._movement_cost(neighbor.parent, neighbor):
                    neighbor.parent = self.current_node
            else:
                print "assigned %s with parent : %s " % (neighbor, self.current_node)
                neighbor.parent = self.current_node
                self.open_nodes.append(neighbor)

    def _check_open_nodes(self):
        cheapest_node = self.current_node
        is_shift = False
        is_not_in_closed_nodes = lambda node: node not in self.closed_nodes
        open_nodes = filter(is_not_in_closed_nodes, self.open_nodes)
        for node in open_nodes:
            cheapest_node_cost = cheapest_node.compute_path_cost(self, None, 0) + self._heuristic(node)
            node_cost = node.compute_path_cost(self, None, 0) + self._heuristic(node)
            if cheapest_node_cost > node_cost: 
                cheapest_node = node 
                is_shift = True
                current_cost = cheapest_node_cost
                new_cost = node_cost
        if is_shift:
            print "Found an open node that has less cost" \
                  ", shifting from %d,%d with cost %s" \
                  " to %d,%d with cost %s" % (self.current_node.x, self.current_node.y, 
                                              current_cost,
                                              cheapest_node.x, cheapest_node.y,
                                              new_cost)
        return cheapest_node, is_shift 

    def _get_nearest_neighbor(self, node, closed_list):
        neighbors = node.get_neighbors()
        not_in_closed_list = lambda x: x not in closed_list
        neighbors = filter(not_in_closed_list, neighbors) 
        print "node: %s,%s" % (node.x, node.y)
        nearest_neighbor = None
        try:
            if neighbors:
                nearest_neighbor = neighbors[0]
                if node.x == 0 and node.y == 4:
                    pdb.set_trace()
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
        comp = movement_cost + self._heuristic(neighbor) + self.current_node.compute_path_cost(self, None, 0)
        return comp

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
        print "sotoooop"
        pdb.set_trace()
        raise Exception('cost not found exception')

    def set_movement_cost(self, left, down, right, up, diagonal):
        self.cost_upper_left, self.cost_upper_right, self.cost_lower_left, self.cost_lower_right = diagonal, diagonal, diagonal, diagonal
        self.cost_left, self.cost_down, self.cost_right, self.cost_up = left, down, right, up 

    def d(self):
        print "open nodes : %s" % display(self.open_nodes)
        print "closed nodes : %s" % display(self.closed_nodes)

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
                    y, x = line.split()
                    y, x = int(x), int(y)
                    self.board = Board(rows=y, columns=x)
                elif i <= y:
                    rows.append(line.split())
                else:
                    print line
                    self.board.fill(rows)
                    if line.startswith('Source'):
                        y, x = self._convert_coordinates(int(line.split()[1]), int(line.split()[2]))
                        start_node = self.board.get_node(x, y)
                    elif line.startswith('Destination'):
                        y, x = self._convert_coordinates(int(line.split()[1]), int(line.split()[2]))
                        end_node = self.board.get_node(x, y)
                    elif line.startswith('Up'):
                        cost_up = float(line.split()[1])
                    elif line.startswith('Down'):
                        cost_down = float(line.split()[1])
                    elif line.startswith('Left'):
                        cost_left = float(line.split()[1])
                    elif line.startswith('Right'):
                        cost_right = float(line.split()[1])
                    elif line.startswith('Diagonal'):
                        cost_diagonal = float(line.split()[1])
        self.a_star_search = AStarSearch(start_node, end_node)
        self.a_star_search.set_movement_cost(cost_up, cost_down, cost_left, cost_right, cost_diagonal)
        path = self.a_star_search.search()
        for node in path:
            print('%d,%d' % (node.x, node.y)),
        pdb.set_trace()
    
    def _convert_coordinates(self, x, y):
        return x, y

runner = Runner()
runner.read_file()
pdb.set_trace()   
board = Board(5,5)
board.get_node(2,2)
pdb.set_trace()
