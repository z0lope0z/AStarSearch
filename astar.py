import pdb
import math


class Node:
    distance = None
    def __init__(self, x, y, board):
        self.x = x
        self.y = y

    def get_neighbors(self):
        neighbors = []
        neighbors.append(board.get_node(x-1, y-1))
        neighbors.append(board.get_node(x-1, y))
        neighbors.append(board.get_node(x-1, y+1))
        neighbors.append(board.get_node(x, y+1))
        neighbors.append(board.get_node(x+1, y+1))
        neighbors.append(board.get_node(x+1, y))
        neighbors.append(board.get_node(x+1, y-1))
        neighbors.append(board.get_node(x, y-1))
        return neighbors

class Board:

    def __init__(self, rows, columns):
        self.matrix = [[None]*rows for i in range(columns)]
    def set_node(self, x, y, node):
        self.matrix[x][y] = node 
    def get_node(self, x, y):
        return self.matrix[x][y] 

class AStarSearch:
    cost_upper_left, cost_left, cost_lower_left, cost_bottom, cost_lower_right, cost_right, cost_upper_right, cost_top = 1, 1, 1, 1, 1, 1, 1, 1

    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node

    def start(self):
        path = []
        while (self._compute_distance(self.current_node, self.end_node) != 0):
            path.append(self._get_nearest_neighbor(self.current_node))

    def _get_nearest_neighbor(self, node):
        neighbors = self.node.get_neighbors()
        if neighbors:
            nearest_neighbor = neighbors[0]
            for neighbor in neighbors:
                distance = self._compute_distance(node, neighbor)
                if distance < nearest_neighbor.distance:
                    nearest_neighbor = neighbor
        return nearest_neighbor

    def _compute_distance(self, node, neighbor):
        movement_cost = self._movement_cost(node, neighbor)
        if movement_cost == 0:
            return 0
        return movement_cost + self._heuristic(neighbor) + self.current_node.current_cost

    def _heuristic(self, node):
        x_diff = abs(node.x-self.end_node.x)
        y_diff = abs(node.y-self.end_node.y)
        return math.sqrt(math.pow(x_diff, 2), math.pow(y_diff, 2))

    def _movement_cost(self, node, neighbor):
        if node.x > neighbor.x:
            if neighbor.y > node.y:
                return cost_upper_left
            elif neighbor.y == node.y:
                return cost_left
            elif neighbor.y < node.y:
                return cost_right
        elif node.x == neighbor.x:
            if neighbor.y > node.y:
                return cost_top
            elif neighbor.y == node.y:
                return 0
            elif neighbor.y < node.y:
                return cost_bottom 
        elif node.x < neighbor.y:
            if neighbor.y > node.y:
                return cost_upper_right
            elif neighbor.y == node.y:
                return cost_right
            elif neighbor.y < node.y:
                return cost_lower_right
        raise Exception('cost not found exception')

board = Board(5,5)
board.get_node(2,2)
pdb.set_trace()
