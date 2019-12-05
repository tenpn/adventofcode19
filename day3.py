def as_paths(lines):
    return [line.split(",") for line in lines]

# takes [[x,y],[x,y]] and returns [[minx,miny], [maxx,maxy]]
def sort_box(line):
    return [[min(line[0][0], line[1][0]), min(line[0][1], line[1][1])],
            [max(line[0][0], line[1][0]), max(line[0][1], line[1][1])]]

# takes [X99,] and returns [box,]
def as_boxes(path):
    lines = []
    position = [0,0]
    steps = 0
    for move in path:
        move_dist = int(move[1:])
        move_char = move[0]
        move = [move_dist,0] if move_char == "R" \
            else [-move_dist,0] if move_char == "L" \
            else [0,move_dist] if move_char == "U" \
            else [0,-move_dist]
        new_pos = [position[0]+move[0], position[1]+move[1]]
        lines.append(sort_box([position, new_pos]) + [steps, position])
        steps = steps + move_dist
        position = new_pos
    return lines

# returns None if no intersection
def find_intersection(abox, bbox):
    if (abox[0] == [0,0] or abox[1] == [0,0]) and (bbox[0] == [0,0] or bbox[1] == [0,0]):
        return None
    # it's a bounding box intersection test!
    if abox[1][0] < bbox[0][0] or bbox[1][0] < abox[0][0] \
       or abox[1][1] < bbox[0][1] or bbox[1][1] < abox[0][1]:
        return None
    # ok now where's the interesection
    intersect_x = abox[0][0] if abox[0][0] == abox[1][0] else bbox[0][0]
    intersect_y = abox[0][1] if abox[0][1] == abox[1][1] else bbox[0][1]
    return [intersect_x, intersect_y]

def manhatten_between(apos, bpos):
    return abs(bpos[0]-apos[0]) + abs(bpos[1]-apos[1])

def manhatten_of(pos):
    return abs(pos[0]) + abs(pos[1])

# takes [x99,]
# returns None if no intersection
def closest_intersection(paths):
    boxes = [as_boxes(path) for path in paths]
    #print(boxes)
    min_intersect_dist = None
    for bbox in boxes[1]:
        for abox in boxes[0]:
            intersection_point = find_intersection(abox, bbox)
            if intersection_point == None:
                continue
            
            intersect_dist = manhatten_of(intersection_point)
            #print("intersect:", abox, bbox, intersection_point, intersect_dist)
            if min_intersect_dist == None or intersect_dist < min_intersect_dist:
                min_intersect_dist = intersect_dist
                
    return min_intersect_dist

# takes [x99,]
# returns None if no intersection
def fewest_steps(paths):
    boxes = [as_boxes(path) for path in paths]
    #print(boxes)
    min_steps = None
    for bbox in boxes[1]:
        for abox in boxes[0]:
            intersection_point = find_intersection(abox, bbox)
            if intersection_point == None:
                continue
            # substep!
            bsteps = bbox[2] + manhatten_between(bbox[3], intersection_point)
            asteps = abox[2] + manhatten_between(abox[3], intersection_point)
            intersect_steps = bsteps + asteps
            
            #print("steps:", abox, bbox, intersection_point, intersect_steps)
            if min_steps == None or intersect_steps < min_steps:
                min_steps = intersect_steps
                
    return min_steps

with open('day3.txt') as f:
    puzzle_lines = f.read().splitlines()
    puzzle_paths = as_paths(puzzle_lines)

test1 = as_paths(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
#print(closest_intersection(test1))
#print(fewest_steps(test1))
test2 = as_paths(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])
#print(fewest_steps(test2))
print(fewest_steps(puzzle_paths))
