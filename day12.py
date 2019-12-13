
def addv(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def subv(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def minusv(a):
    return (-a[0], -a[1], -a[2])

def sign(v):
    return 1 if v > 0 else \
        -1 if v < 0 else \
        0
def signv(a):
    return (sign(a[0]), sign(a[1]), sign(a[2]))

class Moons:
    def __init__(self, start_positions, init_vels = None):
        self.positions = list(start_positions)
        self.velocities = [(0,0,0) for pos in self.positions] if init_vels == None \
            else init_vels

    def step_gravity(self):
        for p in range(len(self.positions)):
            for k in range(p+1, len(self.positions)):
                p_k = signv(subv(self.positions[k], self.positions[p]))
                self.velocities[p] = addv(self.velocities[p], p_k)
                self.velocities[k] = addv(self.velocities[k], minusv(p_k))

    def step_velocity(self):
        for p in range(len(self.positions)):
            self.positions[p] = addv(self.positions[p], self.velocities[p])

    def step(self):
        self.step_gravity()
        self.step_velocity()

    def sum_energy(self):
        tot_energy = 0
        for i in range(len(self.positions)):
            pos = self.positions[i]
            vel = self.velocities[i]
            pot_energy = abs(pos[0]) + abs(pos[1]) + abs(pos[2])
            kin_energy = abs(vel[0]) + abs(vel[1]) + abs(vel[2])
            tot_energy += pot_energy * kin_energy
        return tot_energy

    def test_grav(self, expected_vels, msg):
        self.step_gravity()
        assert self.velocities == expected_vels, "%s expected %s but got %s"%(msg, str(expected_vels), str(self.velocities))

    def test_vels(self, expected_pos, msg):
        self.step_velocity()
        assert self.positions == expected_pos, "%s expected %s but got %s"%(msg, str(expected_pos), str(self.positions))

    def test_step(self, step_count, expected_pos, expected_vels, msg):
        for s in range(step_count):
            self.step()
        assert self.positions == expected_pos, "%s expected pos %s but got %s"%(msg, str(expected_pos), str(self.positions))
        assert self.velocities == expected_vels, "%s expected vel %s but got %s"%(msg, str(expected_vels), str(self.velocities))

    def test_energy(self, expected_energy, msg):
        actual_energy = self.sum_energy()
        assert actual_energy == expected_energy, "%s expected %d got %d"%(msg, expected_energy, actual_energy)

def test():
    Moons([(-1,0,0),(0,0,0)]).test_grav([(1,0,0),(-1,0,0)], "x moves towards")
    Moons([(-1,0,0),(1,0,0)]).test_grav([(1,0,0),(-1,0,0)], "x ignores distance")
    Moons([(-1,1,0),(0,0,0)]).test_grav([(1,-1,0),(-1,1,0)], "multiple components")
    Moons([(-1,0,0),(0,0,0)]).test_grav([(1,0,0),(-1,0,0)], "x moves towards")
    Moons([(-1,0,0),(0,0,0)], [(1,0,0),(-1,0,0)]).test_grav([(2,0,0),(-2,0,0)], "sum changes")
    Moons([(0,0,0)],[(0,0,0)]).test_vels([(0,0,0)], "no vel no move")
    Moons([(0,0,0)],[(1,0,0)]).test_vels([(1,0,0)], "apply vel to pos")
    Moons([(2,0,0)],[(5,0,0)]).test_vels([(7,0,0)], "add vel to pos")

    # test data
    test1 = Moons([(-1,0,2), (2,-10,-7), (4,-8,8), (3,5,-1)])
    test1.test_step(1,
                    [(2,-1,1),(3,-7,-4),(1,-7,5),(2,2,0)],
                    [(3,-1,-1),(1,3,3),(-3,1,-3),(-1,-3,1)],
                    "step1")
    test1.test_step(9,
                    [(2,1,-3),(1,-8,0),(3,-6,1),(2,0,4)],
                    [(-3,-2,1),(-1,1,3),(3,2,-3),(1,-1,-1)],
                    "step10")

    Moons([]).test_energy(0, "no moons no energy")
    Moons([(1,2,1)],[(1,0,0)]).test_energy(4, "summed potential")
    Moons([(-1,2,1)],[(1,0,0)]).test_energy(4, "summed abs potential")
    Moons([(1,0,0)],[(1,2,1)]).test_energy(4, "summed kinetic")
    Moons([(1,0,0)],[(-1,2,1)]).test_energy(4, "summed abs kinetic")
    Moons([(2,0,0)],[(3,0,0)]).test_energy(6, "mult kin/pots energy")
    Moons([(2,0,0),(5,0,0)],[(3,0,0),(7,0,0)]).test_energy(41, "sum all planet energy")

    test2 = Moons([(-8,-10,0),(5,5,10),(2,-7,3),(9,-8,-3)])
    test2.test_step(100,
                    [(8,-12,-9),(13,16,-3),(-29,-11,-1),(16,-13,23)],
                    [(-7,3,0),(3,-11,-5),(-3,7,4),(7,1,1)],
                    "test2 100")
    test2.test_energy(1940, "test2 energy")
    
    print("tests pass")

test()

puzzle = Moons([(-7,-1,6),
                (6,-9,-9),
                (-12,2,-7),
                (4,-17,-12)])
for i in range(1000):
    puzzle.step()
print(puzzle.sum_energy())
