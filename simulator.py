import sys
reg= [0]*32
pc= 0
memory = [0]*32
BASE = 2**16  
HALT= "00000000000000000000000001100011"

def binary_to_int(binary):
    if binary[0]=='1':
        value = int(binary,2)
        total_bits = len(binary)
        max_value = 2**total_bits
        value = value-max_value
        return value
    else:
        return int(binary,2)

def check_32bits(y):
    while y>=2**32:
        y = y-(2**32)
    while y<0:
        y = y+(2**32)
    return y
    
def execute(inst):
    global pc
    opcode= inst[25:32]
    funct3 = inst[17:20]
    funct7= inst[0:7]
    rs1 = int(inst[12:17], 2)
    rs2= int(inst[7:12], 2)
    rd  = int(inst[20:25], 2)

    # R-type
    if opcode == "0110011":
        value1= reg[rs1]
        value2 = reg[rs2]

        if funct3 == "000":
            if funct7 == "0000000":
                result = value1+ value2
            else:
                result = value1 -value2
        elif funct3 == "111":
            result = value1 & value2
        elif funct3== "110":
            result= value1 | value2
        elif funct3 == "100":
            result = value1 ^ value2
        elif funct3== "001":
            shift = value2 % 32
            result= value1 << shift
        elif funct3 == "101":
            shift = value2 % 32
            result= (value1 % (2 ** 32)) >> shift
        elif funct3 == "010":
            if to_sign(value1) < to_sign(value2):
                result = 1
            else:
                result = 0
        elif funct3 == "011":
            if check_32bits(value1) < check_32bits(value2):
                result= 1
            else:
                result = 0
        result = check_32bits(result)
        if rd != 0:
            reg[rd] = result

        pc = pc + 4
    
def trace():
    line ="0b" + int_to_binary(pc)
    for value in reg:
        line=line + " 0b" + int_to_binary(value)
    return line

def dump_memory():
    result=[]
    for i in range(32):
        address= BASE + i*4
        binary_value= int_to_binary(memory[i])
        line = "0x"+ format(address, "08X") + ":0b" + binary_value
        result.append(line)
    return "\n".join(result)

def main():
    global pc
    input_file = sys.argv[1]
    instructions = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                instructions.append(line)
    

    output=[]
    while pc < len(instructions)*4:
        inst=instructions[pc//4]
        if inst == HALT:
            output.append(trace())
            break
        execute(inst)
        output.append(trace())


    output.append(dump_memory())
    for line in output:
        print(line)
    

if __name__ == "__main__":
    main()
