import sys

opcodeStr = []  # <type 'list'>: ['Invalid Instruction', 'ADDI', 'SW', 'Invalid Instruction', 'LW', 'BLTZ', 'SLL',...]
instrSpaced = []  # <type 'list'>: ['0 01000 00000 00001 00000 00000 001010', '1 01000 00000 00001 00000 00000 001010',...]
arg1 = []  # <type 'list'>: [0, 0, 0, 0, 0, 1, 1, 10, 10, 0, 3, 4, 152, 4, 10, 1, 0, 112, 0]
arg2 = []  # <type 'list'>: [0, 1, 1, 0, 1, 0, 10, 3, 4, 5, 0, 5, 0, 5, 6, 1, 1, 0, 0]
arg3 = []  # <type 'list'>: [0, 10, 264, 0, 264, 48, 2, 172, 216, 260, 8, 6, 0, 6, 172, -1, 264, 0, 0]
arg1Str = []  # <type 'list'>: ['', '\tR1', '\tR1', '', '\tR1', '\tR1', '\tR10', '\tR3', '\tR4', .....]
arg2Str = []  # <type 'list'>: ['', ', R0', ', 264', '', ', 264', ', #48', ', R1', ', 172', ', 216', ...]
arg3Str = []  # <type 'list'>: ['', ', #10', '(R0)', '', '(R0)', '', ', #2', '(R10)', '(R10)', '(R0)',...]
mem = []  # <type 'list'>: [-1, -2, -3, 1, 2, 3, 0, 0, 5, -5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
binMem = []  # <type 'list'>: ['11111111111111111111111111111111', '11111111111111111111111111111110', ...]
opcode = []  # <type> 'list'>: ['11111111111', ...]
allInstr = [] # stores all the instructions - the memory data at the end
numInst = 0  # number of instructions in the file

rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
imMask = 0x3FFC00
shmtMask = 0xFC00
addrMask = 0x1FF000
addr2Mask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0

class Dissembler:

    def get_opcode(self):
        for j in range(len(allInstr)):
            opcode.append(allInstr[j] >> 21)

    def findop(self):
        for j in range(len(opcode)):
            if opcode[j] == 1112:
                opcodeStr.append("ADD")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                                   + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == 1624:
                opcodeStr.append("SUB")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                                   + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))

    def print_dissembled(self):
        outFile = open(outputFileName + "_dis.txt", 'w')
        pc = 96
        for j in range(len(opcodeStr)):
            print >> outFile, (instrSpaced[j] + "\t" + str(pc) + "\t" + opcodeStr[j] + "\t" + arg1Str[j] + arg2Str[j] + arg3Str[j])
            pc += 4

#get input and output files from command line args
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print inputFileName
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]
# put instructions into a list then get the opcodes
# into a separate list

instructions = [line.rstrip() for line in open(inputFileName, 'rb')]

# read instructions until break
for i in range(len(instructions)):
    allInstr.append((int(instructions[i], base=2)))
    numInst += 1
    if instructions[i] == '11111110110111101111111111100111':
        break

# reads everything after the break instruction
for i in range(numInst, len(instructions)):
    binMem.append(int(instructions[i], base=2))

disassemble = Dissembler()
disassemble.get_opcode()
disassemble.findop()
disassemble.print_dissembled()
