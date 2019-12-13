from fractions import gcd

# returns [y][x] [[bool,],] 
def parse_map(mapStr):
    return [[c == "#" for c in line] for line in mapStr.splitlines()]

def is_in_map(pos, map):
    return pos[0] >= 0 and pos[1] >= 0 \
        and pos[1] < len(map) and pos[0] < len(map[0])

# returns number of visible asteroids
# where observer = (x,y)
def find_most_visible_from(observer, map):
    blocked = [[False for cell in row] for row in map]
    for y in range(len(map)):
        row = map[y]
        for x in range(len(row)):
            if blocked[y][x] or map[y][x] == False or (x,y) == observer:
                continue
            # block anyone beyond here
            from_observer = (x-observer[0], y-observer[1])
            from_divisor = abs(gcd(from_observer[0], from_observer[1]))
            from_baby_step = (int(from_observer[0]/from_divisor), int(from_observer[1]/from_divisor))
            next_blocked = (x+from_baby_step[0], y+from_baby_step[1])
            #print("blocking from", (x,y), "by", from_baby_step, from_observer, from_divisor)
            while is_in_map(next_blocked, map):
                #print("blocking", next_blocked)
                blocked[next_blocked[1]][next_blocked[0]] = True
                next_blocked = (next_blocked[0]+from_baby_step[0], next_blocked[1]+from_baby_step[1])
    #print(str(blocked))
    visible_count = 0
    for y in range((len(map))):
        row = map[y]
        for x in range(len(row)):
            if map[y][x] and (x,y) != observer and blocked[y][x] == False:
                visible_count += 1
                
    return visible_count

def find_best_spot_in(map):
    best_count = 0
    best_spot = (0,0)
    for y in range((len(map))):
        row = map[y]
        for x in range(len(row)):
            if map[y][x] == False:
                continue
            spot_count = find_most_visible_from((x,y), map)
            if spot_count > best_count:
                best_spot = (x,y)
                best_count = spot_count
    return best_spot

def test_best_spot(map, expected_best_spot, msg):
    actual_spot = find_best_spot_in(map)
    assert actual_spot == expected_best_spot, "%s expected %s got %s"%(msg, str(expected_best_spot), str(actual_spot))

def test_most_visible_from(observer, map, expected_count, msg):
    #print("from", observer, msg)
    actual_count = find_most_visible_from(observer, map)
    assert actual_count == expected_count, "%s expected %d found %d"%(msg, expected_count, actual_count)
            
def tests():
    test_most_visible_from((0,0), [[]], 0, "empty map")
    test_most_visible_from((0,0), [[False,True]], 1, "single neighbour")
    test_most_visible_from((0,0), [[True,True]], 1, "doesn't count self")
    test_most_visible_from((0,0), [[True,True,True]], 1, "ignores obstruction on row")
    test_most_visible_from((2,0), [[True,True,True]], 1, "ignores obstruction on row from right")
    test_most_visible_from((1,0), [[True,True,True]], 2, "ignores obstruction on row from middle")
    test_most_visible_from((0,0), [[True],[True],[True]], 1, "ignores obstruction on col")
    test_best_spot([[True]],(0,0),"single spot")
    test_best_spot([[True,True,True]], (1,0), "ignores obstruction on col")
    test_best_spot([[True,False,True]], (0,0), "don't count from unfilled spots")
    simple_map = parse_map(""".#..#
.....
#####
....#
...##
""")
    test_most_visible_from((3,4), simple_map, 8, "test data 1")
    test_most_visible_from((4,2), simple_map, 5, "test data 2")
    test_best_spot(simple_map, (3,4), "test data best spot")
    
tests()

with open('day10.txt') as f:
    puzzle_map = parse_map(f.read())

puzzle_best_spot = find_best_spot_in(puzzle_map)
print(find_most_visible_from(puzzle_best_spot, puzzle_map))
            
#print(parse_map(simpleMap))

