# accepts "OrbitedID)OrbiterID\n..."
# returns {OrbiterID: OrbitedID, }
def process_orbit_data(orbit_string):
    return { orbit[1]: orbit[0] for orbit in [line.split(")") for line in orbit_string.splitlines()]}

with open('day6.txt') as f:
    puzzle_orbits = process_orbit_data(f.read()) #[line.split(")") for line in f.read().splitlines()]

def count_orbits(orbiter, orbit_data):
    count = 0;
    while orbiter in orbit_data:
        orbiter = orbit_data[orbiter]
        count += 1
    return count

def path_to_COM(orbiter, orbit_data):
    path = []
    while orbiter in orbit_data:
        orbiter = orbit_data[orbiter]
        path.append(orbiter)
    return path

def path_to(start, dest, orbit_data):
    start_to_COM = path_to_COM(start, orbit_data)
    dest_to_COM = path_to_COM(dest, orbit_data)

    # find where our two paths cross and stitch them together:
    
    dupes = [orbiter for orbiter in dest_to_COM if orbiter in start_to_COM]

    route = []
    first_dupe = None
    for start_COM_step in start_to_COM:
        route.append(start_COM_step)
        if start_COM_step == dest:
            return route
        if start_COM_step in dest_to_COM:
            first_dupe = start_COM_step
            break;

    # now walk back from the first dupe to the dest
    back_to_dest = reversed(dest_to_COM[:dest_to_COM.index(first_dupe)])
    route += back_to_dest
    route.append(dest)

    return route

def count_all_orbits(orbit_data):
    count = 0
    for orbiter in orbit_data.keys():
        count += count_orbits(orbiter, orbit_data)
    return count
    
def test_orbit(orbiter, expected_orbit_count, orbit_data):
    actual_orbit_count = count_orbits(orbiter, orbit_data)
    assert actual_orbit_count == expected_orbit_count, "For orbiter %s expected count %d but got %d"%(orbiter, expected_orbit_count, actual_orbit_count)
    
def test_orbit_route_COM(orbiter, expected_orbit_path, orbit_data):
    actual_orbit_path = path_to_COM(orbiter, orbit_data)
    assert actual_orbit_path == expected_orbit_path, "For orbiter %s expected path %s but got %s"%(orbiter, expected_orbit_path, actual_orbit_path)

def test_orbit_route(start, dest, expected_route, orbit_data):
    actual_route = path_to(start, dest, orbit_data)
    assert actual_route == expected_route, "For route between %s and %s expected path %s but got %s"%(start, dest, expected_route, actual_route)
    
def test_all_orbit_count(expected_all_orbit_count, orbit_data):
    actual_all_orbit_count = count_all_orbits(orbit_data)
    assert actual_all_orbit_count == expected_all_orbit_count, "Expected total count %d but got %d"%(expected_all_orbit_count, actual_all_orbit_count)

test_data_str = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
test_data = process_orbit_data(test_data_str)

def test():
    test_orbit("COM", 0, test_data)
    test_orbit("B", 1, test_data)
    test_orbit("C", 2, test_data)
    test_orbit("D", 3, test_data)
    test_orbit("L", 7, test_data)
    test_all_orbit_count(42, test_data)
    test_orbit_route_COM("COM", [], test_data)
    test_orbit_route_COM("B", ["COM"], test_data)
    test_orbit_route_COM("L", ["K", "J", "E", "D", "C", "B", "COM"], test_data)
    test_orbit_route("B", "COM", ["COM"], test_data)
    test_orbit_route("D", "COM", ["C", "B", "COM"], test_data)
    test_orbit_route("D", "B", ["C", "B"], test_data)
    test_orbit_route("G", "C", ["B", "C"], test_data)
    test_orbit_route("K", "I", ["J", "E", "D", "I"], test_data)
    print("tests passed")

test()
print(count_all_orbits(puzzle_orbits))
print(len(path_to(puzzle_orbits["YOU"], puzzle_orbits["SAN"], puzzle_orbits)))
