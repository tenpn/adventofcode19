import intcode

intcode.tests()

robot_program = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1001,1034,0,1039,1001,1036,0,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,1001,1036,0,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,1001,1038,0,1043,102,1,1037,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1001,1035,0,1040,1001,1038,0,1043,1002,1037,1,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,39,1032,1006,1032,165,1008,1040,39,1032,1006,1032,165,1101,0,2,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,69,1044,1106,0,224,1102,0,1,1044,1105,1,224,1006,1044,247,1001,1039,0,1034,101,0,1040,1035,1001,1041,0,1036,101,0,1043,1038,102,1,1042,1037,4,1044,1105,1,0,14,64,25,87,47,95,19,65,33,21,99,74,49,51,99,41,76,12,91,19,39,77,68,1,94,19,16,66,72,56,21,81,96,48,35,31,95,41,65,21,84,74,61,27,81,17,77,75,63,80,38,74,91,51,77,30,51,50,93,81,57,78,84,5,32,90,83,21,87,54,92,64,55,81,96,55,89,45,58,37,31,88,51,70,15,93,13,68,76,58,96,34,22,93,27,84,13,27,95,57,88,14,72,96,50,13,54,94,14,92,58,30,6,73,78,56,41,71,86,30,81,2,80,58,90,19,97,43,41,13,96,95,89,19,79,99,77,46,53,23,84,74,62,51,86,40,88,23,75,83,97,95,5,5,86,81,18,45,94,99,79,83,6,82,60,60,97,89,74,24,3,81,85,41,39,89,45,90,80,8,45,92,11,96,99,88,58,75,31,44,5,92,82,38,22,9,57,5,77,65,5,74,87,81,10,46,87,12,52,76,22,25,74,76,61,88,92,14,96,44,80,20,23,24,76,72,64,78,97,87,9,2,91,10,32,78,70,65,70,85,51,1,6,84,83,84,62,70,40,31,96,73,85,12,85,5,53,98,58,78,24,80,70,7,77,60,71,63,13,94,8,85,7,91,47,35,89,18,44,70,71,98,68,99,14,84,82,3,79,38,68,70,44,34,96,35,87,29,95,48,85,30,96,58,16,74,2,78,96,82,20,14,41,22,88,74,13,86,21,28,93,60,92,72,50,43,95,29,97,97,74,23,87,30,62,89,3,90,77,36,42,70,76,18,96,46,93,68,94,25,95,52,83,95,36,39,87,32,23,88,33,96,31,90,15,96,81,45,44,77,64,38,98,75,71,47,99,88,29,85,30,83,48,93,5,28,86,21,16,93,17,99,68,13,87,71,97,56,84,43,26,70,21,66,82,46,96,84,37,85,90,79,33,57,87,73,40,56,45,87,37,91,28,61,89,87,89,16,46,11,77,89,5,3,71,68,61,91,76,16,85,16,83,50,41,31,71,87,20,60,80,48,24,80,7,85,98,62,91,75,46,11,80,36,26,41,24,92,98,53,73,66,73,75,31,23,88,28,89,84,25,78,58,91,77,55,64,70,46,99,71,38,84,15,50,97,85,15,36,77,25,88,70,81,78,58,54,4,34,92,97,13,4,92,80,71,52,16,93,29,99,2,87,37,99,20,73,59,10,44,91,9,2,72,94,1,76,47,79,91,1,18,86,6,10,86,35,81,20,54,98,87,48,65,85,56,68,85,71,55,82,80,19,25,70,87,31,90,87,80,53,51,90,42,87,86,1,91,49,82,21,79,88,54,28,1,78,54,81,47,12,73,79,5,22,89,71,93,63,56,93,33,83,47,75,36,49,81,10,80,99,49,26,51,78,39,70,79,49,95,16,44,97,8,19,60,95,88,17,78,55,77,60,87,25,53,72,26,42,78,7,72,86,51,31,90,40,61,75,61,85,99,4,90,22,37,95,15,64,93,70,48,7,50,81,92,46,15,73,54,81,91,63,34,93,91,58,82,78,89,55,29,96,80,78,3,82,38,57,85,51,83,79,78,88,53,7,78,71,48,92,43,61,96,11,29,77,91,53,1,20,92,56,86,34,20,70,67,91,14,79,92,31,21,82,75,52,89,37,7,10,85,17,66,86,73,8,31,95,49,78,74,6,77,98,71,49,76,90,78,9,81,79,89,63,92,36,79,53,80,20,77,94,96,1,87,45,77,94,80,3,92,96,97,9,73,35,77,66,98,0,0,21,21,1,10,1,0,0,0,0,0,0]

def addv(a, b):
    return (a[0]+b[0], a[1]+b[1])

str_from_dir = { 1:"N", 2:"S", 3:"W", 4:"E"}
str_from_walk = { 0: "WALL", 1:"SPACE", 2:"O2" }

# 1-4 N,S,W,E
def delta_from_dir(d):
    return (0,1) if d == 1 \
        else (0,-1) if d == 2 \
             else (-1,0) if d == 3 \
                  else (1,0)

def turn_right(d):
    return 1 if d == 3 \
        else 2 if d == 4 \
             else 3 if d == 2 \
                  else 4
def turn_left(d):
    return 2 if d == 3 \
        else 1 if d == 4 \
             else 4 if d == 2 \
                  else 3

def move_in_dir(start, d):
    return addv(start, delta_from_dir(d))

# start at (0,0)
walkables = set()
walls = set()
dest = None

robot = intcode.IntComputer(robot_program)#, intcode.log_verbose)

# walk up until we find a wall
location = (0,0)
while True:
    walkables.add(location)
    move_res = robot.step(1)
    assert move_res != None, "got unexpected abort"
    print("north from", location, "gives", move_res)
    if move_res == 0:
        walls.add(move_in_dir(location, 1))
        break
    else:
        location = move_in_dir(location, 1)

print("found first wall at", addv(location, (0,1)))

# now keep the wall on our left until we find the thing
last_wall_dir = 1
start_passes_left = 2
while True:
    next_dir = turn_right(last_wall_dir)
    next_step_res = robot.step(next_dir)
    #print("keeping wall on left, moving", str_from_dir[next_dir], "found", str_from_walk[next_step_res], "at", move_in_dir(location, next_dir))
    
    if next_step_res == 0:
        new_wall_place = move_in_dir(location, next_dir)
        # if we walk into a wall, we need to turn on the spot and try again
        walls.add(new_wall_place)
        last_wall_dir = next_dir
    else:
        location = move_in_dir(location, next_dir)
        walkables.add(location)
        if location == (0,0):
            start_passes_left -= 1
            if start_passes_left == 0:
                break;
            
        if next_step_res == 2:
            #print("found o2 at", location)
            dest = location

        # check the wall is still where we said
        prev_wall_test = robot.step(last_wall_dir)
        #print("has wall moved?", str_from_walk[prev_wall_test], "at", move_in_dir(location, last_wall_dir))
        if prev_wall_test == 0:
            walls.add(move_in_dir(location, last_wall_dir))
        else:
            # go around the corner
            location = move_in_dir(location, last_wall_dir)
            last_wall_dir = turn_left(last_wall_dir)
            walkables.add(location)

def get_children_from(location):
    return [child for child in [addv(location,child_offset) for child_offset in [(1,0),(-1,0),(0,1),(0,-1)]]
            if child in walkables]
    
closed = set()
cost_from_start = {(0,0):0}
open = [(0,0)]

while len(open) > 0:
    cur = open.pop()
    cur_cost = cost_from_start[cur]
    
    for child in get_children_from(cur):
        if child in closed or child in open:
            continue
        cost_from_start[child] = cur_cost+1
        open.append(child)
        
    closed.add(cur)

#print(walkables)
#print(walls)
maze_min = addv((min([x for (x,y) in walkables]), min([y for (x,y) in walkables])), (-1,-1))
maze_max = addv((max([x for (x,y) in walkables]), max([y for (x,y) in walkables])), (1,1))
print(maze_min, maze_max)
for y in range(maze_max[1], maze_min[1]-1, -1):
    line = [("#" if (x,y) in walls
             else "S" if (x,y) == (0,0)
             else "F" if (x,y) == dest
             else "." if (x,y) in walkables
             else " ") for x in range(maze_min[0], maze_max[0]+1)]
    print("".join(line))

print(cost_from_start[dest])
