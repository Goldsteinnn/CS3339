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
allInstr = []  # stores all the instructions - the memory data at the end

# masks
rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
imMask = 0x3FFC00
shmtMask = 0xFC00
addrMask = 0x1FF000
addr2Mask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0
bMask = 0x1FFFFF

# instruction variables
ADD = 1112
SUB = 1624
B = range(160, 192)
AND = 1104
ADDI = [1160, 1162]
ORR = 1360
CBZ = range(1440, 1448)
CBNZ = range(1448, 1456)
SUBI = [1672, 1673]
MOVZ = range(1684, 1688)
MOVK = range(1940, 1944)
LSR = 1690
LSL = 1691
STUR = 1984
LDUR = 1986
ASR = 1692
NOP = 0
EOR = 1982
BREAK = 2038

#registers
r00 = [0,0,0,0,0,0,0,0]
r08 = [0,0,0,0,0,0,0,0]
r16 = [0,0,0,0,0,0,0,0]
r24 = [0,0,0,0,0,0,0,0]


class Simulator:

    numInst = 0  # number of instructions in the file

    def populate_allInstr(self):
        for i in range(len(instructions)):
            allInstr.append((int(instructions[i], base=2)))
            self.numInst += 1
            # only read until break
            if instructions[i] == '11111110110111101111111111100111':
                break

    def get_opcode(self):
        for j in range(len(allInstr)):
            opcode.append(allInstr[j] >> 21)

    def findop(self):
        for j in range(len(opcode)):
            if opcode[j] == ADD:
                opcodeStr.append("ADD")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                                   + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == SUB:
                opcodeStr.append("SUB")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                                   + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == AND:
                opcodeStr.append("AND")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == ORR:
                opcodeStr.append("ORR")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == LSL:
                opcodeStr.append("LSR")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & shmtMask) >> 10))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == LSR:
                opcodeStr.append("LSL")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & shmtMask) >> 10))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == ASR:
                opcodeStr.append("ASR")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] == EOR:
                opcodeStr.append("EOR")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))
            elif opcode[j] in ADDI:
                opcodeStr.append("ADDI")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & imMask) >> 10))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:10]) + " " + str(instructions[j][10:22] + " " + str(instructions[j][22:27]) +
                                                           " " + str(instructions[j][27:32])))
            elif opcode[j] in SUBI:
                opcodeStr.append("SUBI")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & imMask) >> 10))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:10]) + " " + str(instructions[j][10:22] + " " + str(instructions[j][22:27]) +
                                                           " " + str(instructions[j][27:32])))
            elif opcode[j] == STUR:
                opcodeStr.append("STUR")
                arg1.append(((int(instructions[j], base=2) & rmMask) >> 0))
                arg2.append(((int(instructions[j], base=2) & addrMask) >> 12))
                arg3.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:20] + " " + str(instructions[j][20:22]) +
                                                           " " + str(instructions[j][22:27]) + " " + str(
                        instructions[j][27:32])))
            elif opcode[j] == LDUR:
                opcodeStr.append("LDUR")
                arg1.append(((int(instructions[j], base=2) & rmMask) >> 0))
                arg2.append(((int(instructions[j], base=2) & addrMask) >> 12))
                arg3.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:20] + " " + str(instructions[j][20:22]) +
                                                           " " + str(instructions[j][22:27]) + " " + str(
                        instructions[j][27:32])))
            elif opcode[j] in CBZ:
                opcodeStr.append("CBZ")
                arg1.append(((int(instructions[j], base=2) & addr2Mask) >> 5))
                arg2.append("")
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", #" + str(arg1[j]))
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:8]) + " " + str(instructions[j][8:27] + " " + str(instructions[j][27:32])))
            elif opcode[j] in CBNZ:
                opcodeStr.append("CBNZ")
                arg1.append(((int(instructions[j], base=2) & addr2Mask) >> 5))
                arg2.append("")
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", #" + str(arg1[j]))
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:8]) + " " + str(instructions[j][8:27] + " " + str(instructions[j][27:32])))
            elif opcode[j] in MOVZ:
                opcodeStr.append("MOVZ")
                arg1.append(((int(instructions[j], base=2) & imdataMask) >> 5))
                arg2.append("")
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", #" + str(arg1[j]))
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:9]) + " " + str(instructions[j][9:11] + " " + str(instructions[j][11:27]) +
                                                          " " + str(instructions[j][27:32])))
            elif opcode[j] in MOVK:
                opcodeStr.append("MOVK")
                arg1.append(((int(instructions[j], base=2) & imdataMask) >> 5))
                arg2.append("")
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", #" + str(arg1[j]))
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:9]) + " " + str(instructions[j][9:11] + " " + str(instructions[j][11:27]) +
                                                          " " + str(instructions[j][27:32])))
            elif opcode[j] in B:
                opcodeStr.append("B")
                arg1.append("")
                arg2.append("")
                arg3.append(((int(instructions[j], base=2) & bMask) >> 0))
                arg1Str.append("#" + str(arg3[j]))
                arg2Str.append("")
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:6]) + " " + str(instructions[j][6:32]))
            elif opcode[j] == BREAK:
                opcodeStr.append("BREAK")
                arg1.append("")
                arg2.append("")
                arg3.append("")
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")

                instrSpaced.append(
                    str(instructions[j][0:9]) + " " + str(instructions[j][9:12]) + " "
                    + str(instructions[j][12:17]) + " " + str(instructions[j][17:22]) + " "
                    + str(instructions[j][22:28]) + " " + str(instructions[j][28:32]))

                # reads everything after the break instruction
                for k in range(self.numInst, len(instructions)):
                    binMem.append(int(instructions[k], base=2))
                for k in range(len(binMem)):
                    # if negative number
                    if binMem[k] & (1 << 31) != 0:
                        twos = binMem[k]
                        twos = twos - (1 << 32)
                        instrSpaced.append(instructions[self.numInst + k][0:32])
                        opcodeStr.append(str(twos))
                        arg1.append("")
                        arg2.append("")
                        arg3.append("")
                        arg1Str.append("")
                        arg2Str.append("")
                        arg3Str.append("")

                    # if positive number
                    else:
                        twos = binMem[k]
                        instrSpaced.append(instructions[self.numInst + k][0:32])
                        opcodeStr.append(str(twos))
                        arg1.append("")
                        arg2.append("")
                        arg3.append("")
                        arg1Str.append("")
                        arg2Str.append("")
                        arg3Str.append("")

    def print_dissembled(self):
        outFile = open(outputFileName + "_dis.txt", 'w')
        pc = 96
        for j in range(len(instrSpaced)):
            print >> outFile, (instrSpaced[j] + "\t" + str(pc) + "\t" + opcodeStr[j] + "\t" + arg1Str[j] + arg2Str[j] +
                               arg3Str[j])
            pc += 4

    def print_sim(self):
        i = 0 #Iterates through opcode
        cycle = 1 
        pc = 96

        outFile = open(outputFileName + "_sim.txt", 'w')
        while opcodeStr[i] != "BREAK":
            print >> outFile, ("====================")
            print >> outFile, ("cycle: " + str(cycle) + " " +  str(pc) + "\t" + opcodeStr[i] + "\t" + arg1Str[i] + arg2Str[i] +
                               arg3Str[i] + "\n")
            print >> outFile, ("registers:\n" + "r00:\t" + str(r00) + "\n" + "r08:\t" + str(r08) + "\n" + "r16:\t" + str(r16) +                                      "\n" + "r24:\t" + str(r24) + "\n")
            print >> outFile, ("data:")
            i = i + 1
            cycle = cycle + 1
            pc = pc + 4

    def run(self):
        self.populate_allInstr()
        self.get_opcode()
        self.findop()
        self.print_dissembled()
        self.print_sim()


# get input and output files from command line args
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print inputFileName
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]

# put instructions into a list then get the opcodes
# into a separate list

instructions = [line.rstrip() for line in open(inputFileName, 'rb')]

simulator = Simulator()
simulator.run()
