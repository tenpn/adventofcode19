
puzzle_input = [264793, 803935]

def is_valid(number):
    numstr = str(number)

    # we assume you sent one in the puzzle range

    last_digit = -1
    seq_count = 1
    conseq = False
    for digstr in numstr:
        digit = int(digstr)
        if digit == last_digit:
            seq_count = seq_count + 1
        else:
            if seq_count == 2:
                conseq = True
            seq_count = 1
            if digit < last_digit:
                return False
        last_digit = digit
        
    return conseq or seq_count == 2

def test_num(num):
    print (num, "=", is_valid(num))

test_num(111111)
test_num(223450)
test_num(123789)
test_num(112233)
test_num(123444)
test_num(111122)

valids = 0
for num in range(puzzle_input[0], puzzle_input[1]+1):
    valids = valids + is_valid(num)
print("count:", valids)
