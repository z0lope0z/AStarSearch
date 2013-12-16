A* Search and Greedy BFS
===========
The A* Search Algorithm was derived from pseudocode found in Wikipedia.
This is a solution for the 1st Machine Problem in CS-180 Artificial Intelligence

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


[A* Search - Policy Almanac](http://www.policyalmanac.org/games/aStarTutorial.htm)
