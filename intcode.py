def assert_position_in_range(memory, pc, msg):
    assert memory[pc] >= 0 and memory[pc] < len(memory), "%s %d at mem[%d] is out of range"%(msg, memory[pc], pc)
def assert_immediate_in_range(memory, pc, msg):
    assert pc >= 0 and pc < len(memory), "%s %d is out of range"%(msg, pc)

# parameter index is 1-based
def get_instr_mode(instruction, param_index):
    return int(instruction[-2-param_index]) if len(instruction) > (1+param_index) else 0
    
def execute(memory, input=[]):
    pc = 0
    output = []
    input_pc = 0
    while memory[pc] != 99:
        # string stuff! but it's fine!
        instruction = str(memory[pc])
        op_code = int(instruction[-2:])
        
        if op_code <= 2: # *+
            sym = "+" if op_code == 1 else "*"
            #print(">", memory[pc], memory[pc+1], memory[pc+2], memory[pc+3])
            #print("[" + str(pc+3) + "] = [" + str(memory[pc+1]) + "]" + sym + "[" + str(memory[pc+2]) + "]" )

            param1_mode = get_instr_mode(instruction, 1)
            if param1_mode == 0:
                assert_position_in_range(memory, pc+1, sym + "param1")
                param1 = memory[memory[pc+1]]
            else:
                param1 = memory[pc+1]

            param2_mode = get_instr_mode(instruction, 2)
            if param2_mode == 0:
                assert_position_in_range(memory, pc+2, sym + "param2")
                param2 = memory[memory[pc+2]]
            else:
                param2 = memory[pc+2]

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
            param1_mode = get_instr_mode(instruction, 1)
            if param1_mode == 0:
                assert_position_in_range(memory, pc+1, "ouput param1")
                param1 = memory[memory[pc+1]]
            else:
                param1 = memory[pc+1]
            output.append(param1)
            pc = pc + 2

        elif op_code == 5: # jump if true
            param1_mode = get_instr_mode(instruction, 1)
            if param1_mode == 0:
                assert_position_in_range(memory, pc+1, "jumpiftrue param1")
                param1 = memory[memory[pc+1]]
            else:
                param1 = memory[pc+1]
                
            if param1 == 0:
                pc = pc + 3
            else:
                dest_mode = get_instr_mode(instruction, 2)
                if dest_mode == 0:
                    assert_position_in_range(memory, pc+1, "jumpiftrue new PC")
                    pc = memory[memory[pc+2]]
                else:
                    pc = memory[pc+2]
            
        else:
            assert False, "unexpected opcode %d at mem[%d]"%(op_code, pc)
    return output

def test_mem(memory, expected_memory, msg):
    execute(memory)
    assert memory == expected_memory, msg
    
def test_inmem(memory, input, expected_memory, msg):
    execute(memory, input)
    assert memory == expected_memory, msg

def test_inout(memory, input, expected_output, msg):
    actual_output = execute(memory, input)
    assert actual_output == expected_output, "%s expected %s got %s"%(msg, str(expected_output), str(actual_output))
