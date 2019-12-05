def assert_position_in_range(memory, pc, msg):
    assert memory[pc] >= 0 and memory[pc] < len(memory), "%s %d at mem[%d] is out of range"%(msg, memory[pc], pc)
def assert_immediate_in_range(memory, pc, msg):
    assert pc >= 0 and pc < len(memory), "%s %d is out of range"%(msg, pc)

# parameter index is 1-based
def get_instr_mode(instruction, param_index):
    return int(instruction[-2-param_index]) if len(instruction) > (1+param_index) else 0

# param index is 1-based
def get_param_value(param_index, name, instruction, memory, pc):
    param_mode = get_instr_mode(instruction, param_index)
    if param_mode == 0:
        assert_position_in_range(memory, pc+param_index, name+str(param_index))
        return memory[memory[pc+param_index]]
    else:
        return memory[pc+param_index]

def execute(memory, input=[]):
    pc = 0
    output = []
    input_pc = 0
    while memory[pc] != 99:
        # string stuff! but it's fine!
        instruction = str(memory[pc])
        op_code = int(instruction[-2:])
        #print(instruction)
        
        if op_code <= 2: # *+
            sym = "+" if op_code == 1 else "*"
            #print(">", memory[pc], memory[pc+1], memory[pc+2], memory[pc+3])
            #print("[" + str(pc+3) + "] = [" + str(memory[pc+1]) + "]" + sym + "[" + str(memory[pc+2]) + "]" )

            param1 = get_param_value(1, sym, instruction, memory, pc)
            param2 = get_param_value(2, sym, instruction, memory, pc)

            dest = memory[pc+3]
            res = (param1+param2) if op_code == 1 else (param1*param2)
            #print(param1, sym, param2, "=", res)
            memory[dest] = res
            pc = pc + 4
            
        elif op_code == 3: # input
            new_input = input[input_pc]
            input_pc = input_pc + 1
            dest = memory[pc+1]
            memory[dest] = new_input
            pc = pc + 2

        elif op_code == 4: # output
            param = get_param_value(1, "output", instruction, memory, pc)
            output.append(param)
            pc = pc + 2

        elif op_code == 5 or op_code == 6: # jump if true/false
            param = get_param_value(1, "jumpif", instruction, memory, pc)
            
            if (param == 0 and op_code == 5) or (param != 0 and op_code == 6):
                pc = pc + 3
            else:
                pc = get_param_value(2, "jumpif", instruction, memory, pc)

        elif op_code == 7: # less than
            param1 = get_param_value(1, "lt", instruction, memory, pc)
            param2 = get_param_value(2, "lt", instruction, memory, pc)
            dest = memory[pc+3]
            memory[dest] = 1 if param1 < param2 else 0
            pc = pc + 4
            
        elif op_code == 8: # equal
            param1 = get_param_value(1, "eq", instruction, memory, pc)
            param2 = get_param_value(2, "eq", instruction, memory, pc)
            dest = memory[pc+3]
            memory[dest] = 1 if param1 == param2 else 0
            pc = pc + 4
            
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
