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

i_type = [
    ['addi','0010011','000'],
    ['lw','0000011','010'],
    ['jalr','1100111','000'],
    ['sltiu','0010011','011']
]

#b-type data

b_type = [
    ['beq','1100011','000'],
    ['bne','1100011','001'],
    ['blt','1100011','100'],
    ['bge','1100011','101'],
    ['bltu','1100011','110'],
    ['bgeu','1100011','111']
]

#j-type data

j_type = [
    ['jal','1101111']
]

#s-type data

s_type = [
     ['sw','0100011','010']
]

#u-type data

u_type = [
    ['lui','0110111'],
    ['auipc','0010111']
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

        # i-type

        for x in i_type:
            if x[0] == function:
                opcode = x[1]
                fun3 = x[2]
                found = True
                if function == 'lw':
                    rd = parts[1]
                    imm = int(parts[2])
                    rs1 = parts[3]
                else :
                    rd = parts[1]
                    rs1 = parts[2]
                    imm = int(parts[3])
                if imm < -2048 or imm > 2047:
                    print("Immediate out of range for I-type")
                    sys.exit()
                if imm <0 :
                    final = format((2**12)+imm,'012b') +finder(rs1) + fun3 + finder(rd) + opcode
                else :
                    final = format(imm,'012b') +finder(rs1) + fun3 + finder(rd) + opcode
                
                
                output.append(final)
                pc += 4
                break
        
        #b-type

        for x in b_type:
            if x[0] == function:
                opcode = x[1]
                fun3 = x[2]
                found = True

                rs1 = parts[1]
                rs2 = parts[2]
                label = parts[3]

                branch_addr = None
                for name, addr in labels:
                    if name == label:
                        branch_addr = addr
                    
                if branch_addr is None:
                    print("Label not found:", label)
                    sys.exit()
                    
                offset = branch_addr - pc
                
                if offset<0:
                    offset = (2**13) + offset
                
                branch_imm = format(offset, '013b')


                final = branch_imm[0] + branch_imm[2:8] + finder(rs2) + finder(rs1) + fun3 + branch_imm[8:12] + branch_imm[1] + opcode

                output.append(final)
                pc += 4
                break



        # s-type 
        for x in s_type:
            if x[0] == function:
                opcode = x[1]
                fun3 = x[2]
                found = True

                rs2 = parts[1]
                imm = int(parts[2])
                rs1 = parts[3]

                if imm < -2048 or imm > 2047:
                    print("The Immediate is out of the representable range.")
                    exit()

                if imm < 0:
                    imm = (2**12) + imm

                imm_bin = format(imm, '012b')
                imm_high = imm_bin[0:7]
                imm_low = imm_bin[7:12]

                final = imm_high + finder(rs2) + finder(rs1) + fun3 + imm_low + opcode 
                output.append(final)
                
                pc += 4
                break



       #u-type
        for x in u_type:
            if x[0] == function:
                opcode = x[1]
                found = True

                rd = parts[1]
                imm = int(parts[2])

                if imm < 0:
                    imm = (2**20) + imm

                imm_bin = format(imm//4096, '020b')

                final = imm_bin + finder(rd) + opcode

                output.append(final)
                pc += 4
                break
        
        
        
        #j-type
        
        for x in j_type:
            if x[0] == function:
                opcode = x[1]
                found = True

                rd = parts[1]
                label = parts[2]

                if label.lstrip('-').isdigit():
                    offset = int(label) 
                    
                else:
                    jump_addr = None
                    for name, addr in labels:
                        if name == label:
                            jump_addr = addr
                    if jump_addr ==None:
                        print("Label not found:", label)
                        sys.exit()

                    offset = (jump_addr - pc)

                if offset<0:
                    offset = (2**21) + offset

                jump_imm = format(offset,'021b')

                final = jump_imm[0] + jump_imm[10:20] + jump_imm[9] + jump_imm[1:9] + finder(rd) + opcode


                output.append(final)
                pc += 4
                break

        if not found:
            print("Invalid instruction",function)
            continue
        

    # print(output)
    with open(outputfile, "w") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    main()
   



