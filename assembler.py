import sys

registers = [
    ['zero','00000'],['ra','00001'],['sp','00010'],['gp','00011'],['tp','00100'],
    ['t0','00101'],['t1','00110'],['t2','00111'],
    ['s0','01000'],['fp','01000'],['s1','01001'],
    ['a0','01010'],['a1','01011'],['a2','01100'],['a3','01101'],['a4','01110'],['a5','01111'],
    ['a6','10000'],['a7','10001'],
    ['s2','10010'],['s3','10011'],['s4','10100'],['s5','10101'],['s6','10110'],['s7','10111'],
    ['s8','11000'],['s9','11001'],['s10','11010'],['s11','11011'],
    ['t3','11100'],['t4','11101'],['t5','11110'],['t6','11111']

]
# r-type data

r_type = [
    ['add','0110011','000','0000000'],
    ['sub','0110011','000','0100000'],
    ['sll','0110011','001','0000000'],
    ['slt','0110011','010','0000000'],
    ['sltu','0110011','011','0000000'],
    ['xor','0110011','100','0000000'],
    ['srl','0110011','101','0000000'],
    ['or','0110011','110','0000000'],
    ['and','0110011','111','0000000']
]

def finder(register):
    for name, code in registers:
        if register == name:
            return code
    print(f"Invalid register: {register}")
    sys.exit()
        


            

def main() :
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    lines = []
    f = open(inputfile)
    

    for line in f:
        line = line.strip()
        if line!= '' :
            lines.append(line)

    labels = []
    pc = 0
    
    for i in range(len(lines)):
        line = lines[i]
        if ":" in line:
            label = line.split(":")[0]
            labels.append((label,pc))
            
            lines[i] = line.split(":")[1].strip()
        if lines[i]!='':
            pc += 4
    

    pc = 0
    output = []

    for i in range(len(lines)):
        line = lines[i]
        if line =="":
            continue

        clean = line              
        clean = clean.replace(",", " ")
        clean = clean.replace("(", " ")
        clean = clean.replace(")", " ")

        parts = clean.split()
        function = parts[0]

        found = False

        # r-type

        for x in r_type:
            if x[0] == function:        
                opcode = x[1]
                fun3   = x[2]
                fun7   = x[3]
                found = True
                rd = parts[1]
                rs1 = parts[2]
                rs2 = parts[3]

                final = fun7 + finder(rs2) + finder(rs1) + fun3 + finder(rd) + opcode
                output.append(final)
                pc +=4


                break

        if not found:
            print("Invalid instruction",function)
            continue
        

    # print(output)
    with open(outputfile, "w") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    main()
   



