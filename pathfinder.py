import sys
from collections import deque
import heapq
from queue import PriorityQueue
import math

#PART 1: Command line argument
# First, check if at least the minimum required arguments for BFS or UCS are provided
if len(sys.argv) < 3:
    print("Expected input: python pathfinder.py [map] [algorithm]")
    sys.exit(1)

# Assign the map file and algorithm from the arguments
map_file = sys.argv[1]
algorithm = sys.argv[2]
heuristic = None


if algorithm == "astar":
    #ensure the heuristic argument is provided for A*
    if len(sys.argv) != 4:
        print("Expected input for A* search: python pathfinder.py [map] [algorithm] [heuristic]")
        sys.exit(1)
    heuristic = sys.argv[3]
elif len(sys.argv) > 3:
    #if there are more arguments than expected for BFS or UCS
    print("Unexpected number of arguments for BFS or UCS. No heuristic required.")
    sys.exit(1)



#PART 2: map files read
def convert_value(value):
    if(value.isdigit()):
        return int(value)
    else:
        return value
    
def read_map_from_file(file_path):
    with open(file_path, 'r') as file:
        #Read the map size
        rows, cols = map(int, file.readline().strip().split())
        #Read the start and end positions
        start_pos= tuple(map(int, file.readline().strip().split()))
        end_pos = tuple(map(int, file.readline().strip().split()))
        #Read the map layout
        map_layout = [[convert_value(char) for char in file.readline().strip().split()] for _ in range(rows)]
        
    return rows, cols, start_pos, end_pos, map_layout

file_path = map_file
rows, cols, start_pos, end_pos, map_layout = read_map_from_file(file_path)
start_pos = (start_pos[0] - 1, start_pos[1] - 1)
end_pos = (end_pos[0] - 1, end_pos[1] - 1)

def convert_map_layout(map_layout):
    converted_map = []
    for row in map_layout:
        converted_row = [int(cell) if isinstance(cell, str) and cell.isdigit() else cell for cell in row]
        converted_map.append(converted_row)
    return converted_map

map_layout = convert_map_layout(map_layout)



#PART 3: BFS and UCS


def bfs_or_ucs(start_pos, end_pos, map_layout, algorithm):
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    parent = {}
    visited = set()


    if algorithm == "bfs":
        queue = deque([start_pos])
        visited.add(start_pos)

        while queue:
            current = queue.popleft()    
            if current == end_pos:
                return reconstruct_path(parent, start_pos, end_pos)
            for i in directions:
                x, y = current[0] + i[0], current[1] + i[1]
                if (x < 0 or x >= rows) or (y < 0 or y >= cols) or (map_layout[x][y] == 'X') or ((x, y) in visited):
                    continue
                else:
                    queue.append((x, y))
                    parent[(x, y)] = current
                    visited.add((x, y))

    elif algorithm == "ucs":

        queue = []
        a1 = start_pos[0]
        a2 = start_pos[1]
        heapq.heappush(queue,[0,(-a1,-a2)])
        row = len(map_layout)
        col = len(map_layout[0])

        while queue:

            current = heapq.heappop(queue)
            cost = current[0]

      
            for i in range(len(directions)):
                x = -current[1][0] + directions[i][0]
                y = -current[1][1] + directions[i][1]

                if (x < 0) or (x >= row) or (y < 0) or (y >= col) or ((x,y) in parent) or (map_layout[x][y] == -1) or (map_layout[x][y]) == "X":
                    continue 
                else:
                    #Calculating elevation costs
                    elevation_cost = 0
                    curr_cost = 0
                    if(map_layout[x][y] > map_layout[-current[1][0]][-current[1][1]]):
                        elevation_cost = map_layout[x][y] - map_layout[-current[1][0]][-current[1][1]]
                    curr_cost = cost + elevation_cost+ 1
                    #Append to queue and map the parent if it is a valid case
                    heapq.heappush(queue,[curr_cost,(-x,-y)])
                    parent[(x,y)] = (-current[1][0],-current[1][1])

                if (x,y) == end_pos:
                    return reconstruct_path(parent, start_pos, end_pos)



def reconstruct_path(parent, start_pos, end_pos):
    path = []
    current = end_pos
    while current != start_pos:
        path.append(current)
        current = parent.get(current)
    path.append(start_pos)
    path.reverse()
    return path


#PART 4: Euclidean and Manhattan

def astar(start, end, map_layout, heuristic):

    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    parent = {}
    visited = set()
    queue=[] 

    a1 = start[0]
    a2 = start[1]
    heapq.heappush(queue,[0,(-a1,-a2)])
    row = len(map_layout)
    col = len(map_layout[0])

    while queue:

        #Popping variable from queue and storing the cost to reach here
        current = heapq.heappop(queue)
        cost = current[0]

        #Iterating over all of the direction
        for i in range(len(directions)):
            x = -current[1][0]+directions[i][0]
            y =-current[1][1]+directions[i][1]

            if (x <0) or (x >= row) or (y < 0) or (y >= col) or ((x,y) in parent) or (map_layout[x][y]==-1) or (map_layout[x][y]) == "X":
                continue
            else:
                #Calculating elevation costs
                elevation_cost = 0
                curr_cost = 0

                if(map_layout[x][y] > map_layout[-current[1][0]][-current[1][1]]):
                    elevation_cost = map_layout[x][y]-map_layout[-current[1][0]][-current[1][1]]

                if heuristic == "euclidean":
                    curr_cost = cost+ elevation_cost+ 1 + math.dist([x,y], [end[0],end[1]])
                elif heuristic == "manhattan":
                    curr_cost = cost + elevation_cost + 1 + abs(x + current[1][0]) + abs(y + current[1][1])
                #Append and map the parent if it's valid
                heapq.heappush(queue,[curr_cost,(-x,-y)])
                parent[(x,y)]=(-current[1][0],-current[1][1])

            if (x,y) == end:
                return reconstruct_path(parent, start_pos, end_pos)



def print_map_with_path(map_layout, path):
    # Adjust the map layout to include the path
    if path is None:
        print("null")
        return

    for (x, y) in path:
        # Check if the position is not an obstacle before marking it
        if map_layout[x][y] != 'X':
            map_layout[x][y] = '*'
    
    # Print the adjusted map layout
    for row in map_layout:
        print(' '.join(str(cell) for cell in row))


path = None
if algorithm == "bfs":
    path = bfs_or_ucs(start_pos, end_pos, map_layout, "bfs")
elif algorithm == "ucs":
    path = bfs_or_ucs(start_pos, end_pos, map_layout, "ucs")
elif algorithm == "astar":
    if heuristic == "euclidean":
        path = astar(start_pos, end_pos, map_layout, "euclidean")
    elif heuristic == "manhattan":
        path = astar(start_pos, end_pos, map_layout,"manhattan")

print_map_with_path(map_layout, path)

