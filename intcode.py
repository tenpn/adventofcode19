def assert_position_in_range(memory, pc, msg):
    assert memory[pc] >= 0 and memory[pc] < len(memory), "%s %d at mem[%d] is out of range"%(msg, memory[pc], pc)
def assert_immediate_in_range(memory, pc, msg):
    assert pc >= 0 and pc < len(memory), "%s %d is out of range"%(msg, pc)

# parameter index is 1-based
def get_instr_mode(instruction, param_index):
    return int(instruction[-2-param_index]) if len(instruction) > (1+param_index) else 0

# param index is 1-based
def get_param_value(param_index, name, instruction, memory, pc, relative_base):
    param_mode = get_instr_mode(instruction, param_index)
    if param_mode == 0:
        assert_position_in_range(memory, pc+param_index, name+str(param_index))
        return memory[memory[pc+param_index]]
    elif param_mode == 1:
        return memory[pc+param_index]
    else:
        assert param_mode == 2, "unknown param mode " + str(param_mode)
        assert_position_in_range(memory, pc+param_index, name+str(param_index))
        relative_position = relative_base + memory[pc+param_index]
        assert_position_in_range(memory, relative_position, name+str(param_index))
        return memory[relative_position]

def ensure_memory(memory, new_location):
    assert new_location >= 0, "Expected non-negative memory location but got %d"%(new_location)
    if len(memory) <= new_location:
        extra_pad = [0 for _ in range((new_location-len(memory))+1)]
        memory += extra_pad
    
def execute(memory, input=[]):
    pc = 0
    output = []
    input_pc = 0
    relative_base = 0
    while memory[pc] != 99:
        # string stuff! but it's fine!
        instruction = str(memory[pc])
        op_code = int(instruction[-2:])
        #print(instruction)
        
        if op_code <= 2: # *+
            sym = "+" if op_code == 1 else "*"
            #print(">", memory[pc], memory[pc+1], memory[pc+2], memory[pc+3])
            #print("[" + str(pc+3) + "] = [" + str(memory[pc+1]) + "]" + sym + "[" + str(memory[pc+2]) + "]" )

            param1 = get_param_value(1, sym, instruction, memory, pc, relative_base)
            param2 = get_param_value(2, sym, instruction, memory, pc, relative_base)

            dest = memory[pc+3]
            res = (param1+param2) if op_code == 1 else (param1*param2)
            #print(param1, sym, param2, "=", res)
            ensure_memory(memory, dest)
            memory[dest] = res
            pc = pc + 4
            
        elif op_code == 3: # input
            new_input = input[input_pc]
            input_pc = input_pc + 1
            dest = memory[pc+1]
            ensure_memory(memory, dest)
            memory[dest] = new_input
            pc = pc + 2

        elif op_code == 4: # output
            param = get_param_value(1, "output", instruction, memory, pc, relative_base)
            output.append(param)
            pc = pc + 2

        elif op_code == 5 or op_code == 6: # jump if true/false
            param = get_param_value(1, "jumpif", instruction, memory, pc, relative_base)
            
            if (param == 0 and op_code == 5) or (param != 0 and op_code == 6):
                pc = pc + 3
            else:
                pc = get_param_value(2, "jumpif", instruction, memory, pc, relative_base)

        elif op_code == 7: # less than
            param1 = get_param_value(1, "lt", instruction, memory, pc, relative_base)
            param2 = get_param_value(2, "lt", instruction, memory, pc, relative_base)
            dest = memory[pc+3]
            ensure_memory(memory, dest)
            memory[dest] = 1 if param1 < param2 else 0
            pc = pc + 4
            
        elif op_code == 8: # equal
            param1 = get_param_value(1, "eq", instruction, memory, pc, relative_base)
            param2 = get_param_value(2, "eq", instruction, memory, pc, relative_base)
            dest = memory[pc+3]
            ensure_memory(memory, dest)
            memory[dest] = 1 if param1 == param2 else 0
            pc = pc + 4

        elif op_code == 9: # move relative base
            param1 = get_param_value(1, "relbase", instruction, memory, pc, relative_base)
            relative_base += param1
            pc = pc + 2
            
        else:
            assert False, "unexpected opcode %d at mem[%d]"%(op_code, pc)

        #print(memory)
    return output

def test_mem(memory, expected_memory, msg):
    execute(memory)
    assert memory == expected_memory, "%s expected mem %s but got %s" %(msg, str(expected_memory), str(memory))
    
def test_inmem(memory, input, expected_memory, msg):
    execute(memory, input)
    assert memory == expected_memory, msg

def test_inout(memory, input, expected_output, msg):
    actual_output = execute(memory, input)
    assert actual_output == expected_output, "%s expected %s got %s"%(msg, str(expected_output), str(actual_output))

def tests():
    test_mem([1,1,0,3,99], [1,1,0,2,99], "defaults to positional")
    test_mem([101,10,0,3,99], [101,10,0,111,99], "first param immediate")
    test_mem([1001,0,10,3,99], [1001,0,10,1011,99], "second param immediate")
    test_inmem([3,1,99], [5], [3,5,99], "input")
    test_inout([4,0,99], [], [4], "output")
    test_inout([104,50,99], [], [50], "immediate output")
    # first instruction will test to see if we're jumping to the end or not, maybe with some data suffix.
    test_inout([5,8,7,99,104,10,99,4,1], [], [10], "jump if true passes")
    test_inout([5,8,7,99,104,10,99,4,0], [], [], "jump if true fails")
    test_inout([105,0,7,99,104,10,99,4], [], [], "jump if true immediate param1")
    test_inout([1105,1,4,99,104,10,99], [], [10], "jump if true immediate dest")
    # first instruction will test to see if we're jumping to the end or not, maybe with some data suffix.
    test_inout([6,8,7,99,104,10,99,4,1], [], [], "jump if false fails")
    test_inout([6,8,7,99,104,10,99,4,0], [], [10], "jump if false passes")
    test_inout([106,0,7,99,104,10,99,4], [], [10], "jump if false immediate param1")
    test_inout([1106,1,4,99,104,10,99], [], [], "jump if false immediate dest")
    # relationals
    test_mem([7,3,2,0,99], [1,3,2,0,99], "less than passes")
    test_mem([7,0,2,0,99], [0,0,2,0,99], "less than fails")
    test_mem([107,100,0,0,99], [1,100,0,0,99], "less than immediate param1")
    test_mem([1007,0,2000,0,99], [1,0,2000,0,99], "less than immediate param2")
    test_mem([8,5,6,0,99,1,1], [1,5,6,0,99,1,1], "equals passes")
    test_mem([8,5,6,0,99,1,2], [0,5,6,0,99,1,2], "equals fails")
    test_mem([108,2,5,0,99,2], [1,2,5,0,99,2], "equals immediate param1")
    test_mem([1008,5,2,0,99,2],[1,5,2,0,99,2], "equals immediate param2")
    # day5 part 2 test
    test_inout([3,9,8,9,10,9,4,9,99,-1,8], [8], [1], "1 if equal to 8")
    test_inout([3,9,8,9,10,9,4,9,99,-1,8], [9], [0], "0 if not equal to 8")
    test_inout([3,3,1108,-1,8,3,4,3,99], [8], [1], "1 if equal to 8")
    test_inout([3,3,1108,-1,8,3,4,3,99], [9], [0], "0 if not equal to 8")
    test_inout([3,9,7,9,10,9,4,9,99,-1,8], [7], [1], "1 if lt 8")
    test_inout([3,9,7,9,10,9,4,9,99,-1,8], [8], [0], "0 if not lt 8")
    test_inout([3,3,1107,-1,8,3,4,3,99], [7], [1], "1 if lt 8")
    test_inout([3,3,1107,-1,8,3,4,3,99], [8], [0], "0 if not lt 8")
    test_inout([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0], [0], "0 if 0")
    test_inout([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [10], [1], "1 if not 0")
    test_inout([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0], [0], "0 if 0")
    test_inout([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [10], [1], "1 if not 0")
    test_inout([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,
                        31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
                       [5],[999], "999 if below 8")
    test_inout([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,
                        31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
                       [8],[1000], "1000 if eq 8")
    test_inout([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,
                        31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
                       [15],[1001], "1001 if gt 8")
    # writing beyond the memory list will grow it
    test_inout([1101,1,1,7,4,7,99], [], [2], "extra memory math")
    test_inout([1108,1,1,7,4,7,99], [], [1], "extra memory eq")
    test_inout([1107,0,1,7,4,7,99], [], [1], "extra memory lt")
    test_inout([3,3,99], [1], [], "extra memory lt")
    # relative mode
    test_mem([201,5,6,7,99,1,1], [201,5,6,7,99,1,1,2], "relative mode starts off as position mode")
    test_inout([109,1,99], [], [], "op 9 does nothing by itself")
    test_mem([109,1,208,7,8,9,99,2,1], [109,1,208,7,8,9,99,2,1,1], "op 9 moves relative base")
    test_mem([9,8,208,7,8,9,99,2,1], [9,8,208,7,8,9,99,2,1,1], "op 9 moves relative base")
    print("tests pass")
    
