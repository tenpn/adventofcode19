import intcode

day5_puzzle_input = [3,225,1,225,6,6,1100,1,238,225,104,0,101,20,183,224,101,-63,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1101,48,40,225,1101,15,74,225,2,191,40,224,1001,224,-5624,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,62,60,225,1102,92,15,225,102,59,70,224,101,-885,224,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1,35,188,224,1001,224,-84,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1001,66,5,224,1001,224,-65,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,1002,218,74,224,101,-2960,224,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1101,49,55,224,1001,224,-104,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1102,43,46,225,1102,7,36,225,1102,76,30,225,1102,24,75,224,101,-1800,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1101,43,40,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,226,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,344,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,359,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,374,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,107,677,677,224,1002,223,2,223,1006,224,404,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,419,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,434,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,449,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,479,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,494,101,1,223,223,7,226,677,224,102,2,223,223,1005,224,509,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,524,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,539,1001,223,1,223,1108,226,677,224,102,2,223,223,1006,224,554,101,1,223,223,108,226,677,224,102,2,223,223,1005,224,569,1001,223,1,223,8,677,677,224,1002,223,2,223,1005,224,584,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,614,101,1,223,223,1008,677,677,224,102,2,223,223,1006,224,629,1001,223,1,223,107,226,677,224,102,2,223,223,1006,224,644,101,1,223,223,1107,677,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,7,226,226,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226]

def tests():
    intcode.test_mem([1,1,0,3,99], [1,1,0,2,99], "defaults to positional")
    intcode.test_mem([101,10,0,3,99], [101,10,0,111,99], "first param immediate")
    intcode.test_mem([1001,0,10,3,99], [1001,0,10,1011,99], "second param immediate")
    intcode.test_inmem([3,1,99], [5], [3,5,99], "input")
    intcode.test_inout([4,0,99], [], [4], "output")
    intcode.test_inout([104,50,99], [], [50], "immediate output")
    # first instruction will test to see if we're jumping to the end or not, maybe with some data suffix.
    intcode.test_inout([5,8,7,99,104,10,99,4,1], [], [10], "jump if true passes")
    intcode.test_inout([5,8,7,99,104,10,99,4,0], [], [], "jump if true fails")
    intcode.test_inout([105,0,7,99,104,10,99,4], [], [], "jump if true immediate param1")
    intcode.test_inout([1105,1,4,99,104,10,99], [], [10], "jump if true immediate dest")
    # first instruction will test to see if we're jumping to the end or not, maybe with some data suffix.
    intcode.test_inout([6,8,7,99,104,10,99,4,1], [], [], "jump if false fails")
    intcode.test_inout([6,8,7,99,104,10,99,4,0], [], [10], "jump if false passes")
    intcode.test_inout([106,0,7,99,104,10,99,4], [], [10], "jump if false immediate param1")
    intcode.test_inout([1106,1,4,99,104,10,99], [], [], "jump if false immediate dest")
    # relationals
    intcode.test_mem([7,3,2,0,99], [1,3,2,0,99], "less than passes")
    intcode.test_mem([7,0,2,0,99], [0,0,2,0,99], "less than fails")
    intcode.test_mem([107,100,0,0,99], [1,100,0,0,99], "less than immediate param1")
    intcode.test_mem([1007,0,2000,0,99], [1,0,2000,0,99], "less than immediate param2")
    intcode.test_mem([8,3,2,0,99], [0,3,2,0,99], "greater than passes")
    intcode.test_mem([8,0,2,0,99], [1,0,2,0,99], "greater than fails")
    intcode.test_mem([108,100,0,0,99], [0,100,0,0,99], "greater than immediate param1")
    intcode.test_mem([1008,0,2000,0,99], [0,0,2000,0,99], "greater than immediate param2")

tests()
mode = 1
output = intcode.execute(day5_puzzle_input, [mode])
print(output)

