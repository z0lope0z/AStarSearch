A* Search and Greedy BFS
===========
The A* Search Algorithm was derived from pseudocode found in Wikipedia.
This is a solution for the 1st Machine Problem in CS-180 Artificial Intelligence

#### Quick Implementation Details
- A node's heuristic cost is derived from its current distance to the root node, the movement cost (left, right, diagonal) and its [Euclidean Distance] to the end node
- Stores unexplored nodes inside a priority queue using the heuristic cost as its key.
- Stores explored nodes inside a list.
- With each step in the loop, it pops the unexplored node's priority queue and adds it to the list of explored nodes
- Under various conditions, the current node's neighbors are added to the unexplored nodes priority queue along with its computed heuristic value.
- The Greedy BFS algorithm is just a modified A* Search wherein it does not keep track of a node's distance to the root node.

### Configuration

Sample **input.txt**:

```
6 5
0 0 0 0 0
0 1 1 1 0
1 0 1 0 0
0 0 1 0 1
0 1 1 0 1
0 0 0 0 0
Source: 3 1
Destination: 0 4
Up: 1
Down: 1
Left: 1
Right: 1
Diagonal: 1.5
```

### Running
```
python search.py
```

### Output
Sample **astar.out** and **greedy.out**:
```
3 1
2 1
1 0
0 1
0 2
0 3
0 4
7.0
```
Sources:

[A* Search - Wikipedia](http://en.wikipedia.org/wiki/A*_search_algorithm)

[Euclidean Distance]: http://en.wikipedia.org/wiki/Euclidean_distance

[A* Search - Policy Almanac](http://www.policyalmanac.org/games/aStarTutorial.htm)
