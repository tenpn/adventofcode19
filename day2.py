import intcode

with open('day2.txt') as f:
    puzzle_memory_strings = f.read().split(",")
    puzzle_memory = [int(mem_str) for mem_str in puzzle_memory_strings]

def test(memory):
    print("testing", memory, ">", intcode.execute(memory))

#test([1,0,0,0,99])
#test([2,3,0,3,99])
#test([2,4,4,5,99,0])
#test([1,1,1,4,99,5,6,0,99])

#noun
puzzle_memory[1] = 94#12
#verb
puzzle_memory[2] = 25#2
puzzle_res = intcode.execute(puzzle_memory)
print("puzzle:", puzzle_res[0])
