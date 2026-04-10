import sys
reg= [0]*32
pc= 0
memory = [0]*32
BASE = 2**16  
HALT= "00000000000000000000000001100011"

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
