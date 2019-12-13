
# parameter index is 1-based
def get_instr_mode(instruction, param_index):
    return int(instruction[-2-param_index]) if len(instruction) > (1+param_index) else 0

log_none = "none"
log_normal = "normal"
log_verbose = "verbose"
global_log_level = "none"
global_prefix = ""

def lv(msg):
    global global_log_level, global_prefix
    if global_log_level == log_verbose:
        print(global_prefix, msg)
def ll(msg):
    global global_log_level, global_prefix
    if global_log_level != log_none:
        print(global_prefix, msg)
def lv_params(param_count, memory, pc):
    param_log = ""
    for i in range(param_count):
        param_log += "%d "%(memory[pc+i+1])
    lv(param_log)

class IntComputer:
    def __init__(self, memory, log_level=log_none):
        self.memory = memory
        self.log_level = log_level
        self.prefix = ""
        self.pc = 0
        self.relative_base = 0
        self.input = []
        self.input_pc = 0

    def lv(self, msg):
        if self.log_level == log_verbose:
            print(self.prefix, msg)
    def ll(self, msg):
        if self.log_level != log_none:
            print(self.prefix, msg)
    def lv_params(self, param_count, memory, pc):
        param_log = ""
        for i in range(param_count):
            param_log += "%d "%(memory[pc+i+1])
        self.lv(param_log)
        
    # param index is 1-based
    def get_param_value(self, param_index, name, instruction):
        param_location = self.get_param_location(param_index, name, instruction)
        return self.read_memory(param_location)

    # param index is 1-based
    def get_param_location(self, param_index, name, instruction):
        param_mode = get_instr_mode(instruction, param_index)
        if param_mode == 0:
            param_location = self.memory[self.pc+param_index]
            return param_location
        elif param_mode == 1:
            return self.pc+param_index
        else:
            assert param_mode == 2, "unknown param mode " + str(param_mode)
            relative_position = self.relative_base + self.memory[self.pc+param_index]
            return relative_position

    def read_memory(self, loc):
        assert loc >= 0, "expected non-negative memory location but got %d"%(loc)
        return 0 if len(self.memory) <= loc else self.memory[loc]

    def ensure_memory(self, new_location):
        assert new_location >= 0, "Expected non-negative memory location but got %d"%(new_location)
        if len(self.memory) <= new_location:
            extra_pad = [0 for _ in range((new_location-len(self.memory))+1)]
            self.memory += extra_pad

    def is_completed(self):
        return self.memory[self.pc] == 99

    def execute(self, input=[]):
        all_out = []
        while self.is_completed() == False:
            all_out += self.step(input)
            # strip out consumed input
            input = input[self.input_pc:]
        return all_out

    def step(self, input=[]):
        self.input_pc = 0
        output = []

        while self.is_completed() == False:
            # string stuff! but it's fine!
            instruction = str(self.memory[self.pc])
            op_code = int(instruction[-2:])
            self.prefix = str(self.pc) + " " + instruction + ":"

            if op_code <= 2: # *+
                self.lv_params(3, self.memory, self.pc)
                sym = "+" if op_code == 1 else "*"

                param1 = self.get_param_value(1, sym, instruction)
                param2 = self.get_param_value(2, sym, instruction)

                dest = self.get_param_location(3, sym, instruction)
                res = (param1+param2) if op_code == 1 else (param1*param2)
                self.ll("memory[%d] = %d %s %d = %d"%(dest, param1, sym, param2, res))
                self.ensure_memory(dest)
                self.memory[dest] = res
                self.pc = self.pc + 4

            elif op_code == 3: # input
                self.lv_params(1, self.memory, self.pc)
                new_input = input[self.input_pc]
                self.input_pc = self.input_pc + 1
                dest = self.get_param_location(1, "input", instruction)
                self.ensure_memory(dest)
                self.ll("memory[%d] = input %d"%(dest, new_input))
                self.memory[dest] = new_input
                self.pc = self.pc + 2

            elif op_code == 4: # output
                self.lv_params(1, self.memory, self.pc)
                param = self.get_param_value(1, "output", instruction)
                self.ll("output " + str(param))
                output.append(param)
                self.pc = self.pc + 2
                return output

            elif op_code == 5 or op_code == 6: # jump if true/false
                self.lv_params(2, self.memory, self.pc)
                param = self.get_param_value(1, "jumpif", instruction)
                sym = "jumpIfTrue" if op_code == 5 else "jumpIfFalse"
                if (param == 0 and op_code == 5) or (param != 0 and op_code == 6):
                    self.ll("%s %d fails"%(sym, param))
                    self.pc = self.pc + 3
                else:
                    self.pc = self.get_param_value(2, "jumpif", instruction)
                    self.ll("%s %d passed, jump to %d"%(sym, param, self.pc))

            elif op_code == 7: # less than
                self.lv_params(3, self.memory, self.pc)
                param1 = self.get_param_value(1, "lt", instruction)
                param2 = self.get_param_value(2, "lt", instruction)
                dest = self.get_param_location(3, "lt", instruction)
                self.ensure_memory(dest)
                self.memory[dest] = 1 if param1 < param2 else 0
                self.ll("memory[%d] = %d < %d = %d"%(dest, param1, param2, self.memory[dest]))
                self.pc = self.pc + 4

            elif op_code == 8: # equal
                self.lv_params(3, self.memory, self.pc)
                param1 = self.get_param_value(1, "eq", instruction)
                param2 = self.get_param_value(2, "eq", instruction)
                dest = self.get_param_location(3, "eq", instruction)
                self.ensure_memory(dest)
                self.memory[dest] = 1 if param1 == param2 else 0
                self.ll("memory[%d] = %d == %d = %d"%(dest, param1, param2, self.memory[dest]))
                self.pc = self.pc + 4

            elif op_code == 9: # move relative base
                self.lv_params(1, self.memory, self.pc)
                param1 = self.get_param_value(1, "relbase", instruction)
                self.relative_base += param1
                self.ll("relative += %d = %d"%(param1, self.relative_base))
                self.pc = self.pc + 2

            else:
                assert False, "unexpected opcode %d at mem[%d]"%(op_code, self.pc)

            #print(self.memory)
        return output

def test_mem(memory, expected_memory, msg, logging=log_none):
    IntComputer(memory, logging).execute([])
    assert memory == expected_memory, "%s expected mem %s but got %s" %(msg, str(expected_memory), str(memory))
    
def test_inmem(memory, input, expected_memory, msg, logging=log_none):
    IntComputer(memory, logging).execute(input)
    assert memory == expected_memory, "%s expected mem %s but got %s"%(msg, str(expected_memory), str(memory))

def test_inout(memory, input, expected_output, msg, logging=log_none):
    actual_output = IntComputer(memory, logging).execute(input)
    assert actual_output == expected_output, "%s expected %s got %s"%(msg, str(expected_output), str(actual_output))

def tests():
    test_mem([1,1,0,3,99], [1,1,0,2,99], "defaults to positional")
    test_mem([101,10,0,3,99], [101,10,0,111,99], "first param immediate")
    test_mem([1001,0,10,3,99], [1001,0,10,1011,99], "second param immediate")
    test_inmem([3,1,99], [5], [3,5,99], "input")
    test_inout([4,0,99], [], [4], "output")
    test_inout([104,50,99], [], [50], "immediate output")
    test_mem([109,10,21101,4,5,0,99],[109,10,21101,4,5,0,99,0,0,0,9], "math relative dest")
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
    test_mem([109,10,21107,4,5,0,99],[109,10,21107,4,5,0,99,0,0,0,1], "lt relative dest")
    test_mem([8,5,6,0,99,1,1], [1,5,6,0,99,1,1], "equals passes")
    test_mem([8,5,6,0,99,1,2], [0,5,6,0,99,1,2], "equals fails")
    test_mem([108,2,5,0,99,2], [1,2,5,0,99,2], "equals immediate param1")
    test_mem([1008,5,2,0,99,2],[1,5,2,0,99,2], "equals immediate param2")
    test_mem([109,10,21108,5,5,0,99],[109,10,21108,5,5,0,99,0,0,0,1], "equals relative dest")
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
    # reading beyond the memory returns 0
    test_inout([4,100,99],[],[0], "reading outside of memory")
    test_inout([204,100,99],[],[0], "reading outside of memory")
    # relative mode
    test_mem([201,5,6,7,99,1,1], [201,5,6,7,99,1,1,2], "relative mode starts off as position mode")
    test_inout([109,1,99], [], [], "op 9 does nothing by itself")
    test_mem([109,1,208,7,8,9,99,2,1], [109,1,208,7,8,9,99,2,1,1], "op 9 moves relative base")
    test_mem([9,8,208,7,8,9,99,2,1], [9,8,208,7,8,9,99,2,1,1], "op 9 moves relative base")
    test_inmem([109,10,203,0,99],[444],[109,10,203,0,99,0,0,0,0,0,444], "relative write dest in input")
    # day9 tests
    test_inout([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [], [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], "copy to output")
    output = IntComputer([1102,34915192,34915192,7,4,7,99,0]).execute()
    assert len(str(output[0])) == 16, "expected 16-digit number but got " + str(output)
    test_inout([104,1125899906842624,99], [], [1125899906842624], "output large number")

    stepper = IntComputer([104,1,104,2,99])
    step_out = stepper.step()
    assert step_out == [1], "expected first output only, got " + str(step_out)
    step_out = stepper.step()
    assert step_out == [2], "expected second output only, got " + str(step_out)

    test_inmem([3,10,104,1,3,11,104,2,99], [33,44], [3,10,104,1,3,11,104,2,99,0,33,44], "inputs split between steps")
    test_inmem([3,11,104,1,3,12,104,2,3,13,99], [33,44,55], [3,11,104,1,3,12,104,2,3,13,99,33,44,55], "inputs split between steps 2")
    
    print("tests pass")
    
