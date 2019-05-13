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

# project 3 lists
dest = []
src1 = []
src2 = []
reg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data = []
preIssue = [-1, -1, -1, -1]  # [ instruction index ] x4
preAlu = [-1, -1]   # [ instruction index, instruction index ]
postAlu = [-1, -1]  # [ value, instruction index ]
preMem = [-1, -1]   # [ instruction index, instruction index ]
postMem = [-1, -1]  # [ value, instruction index ]

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
bMask = 0x0BFFFFFF

# instruction variables
ADD = 1112
SUB = 1624
B = range(160, 192)
AND = 1104
ADDI = [1160, 1162]
ORR = 1360
CBZ = range(1440, 1448)
CBNZ = range(1448, 1456)
SUBI = [1672, 1674]
MOVZ = range(1684, 1688)
MOVK = range(1940, 1944)
LSR = 1690
LSL = 1691
STUR = 1984
LDUR = 1986
ASR = 1692
NOP = 0
EOR = 1872
BREAK = 2038

# hardcode start PC
PC = 96

# TODO: !!! remove hardcoded input/output values for testing !!!
def inputOutput():
    # get input and output files from command line args
    inputFileName = ""
    outputFileName = ""
    for i in range(len(sys.argv)):
        if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
            inputFileName = sys.argv[i + 1]
        elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
            outputFileName = sys.argv[i + 1]

    # Todo: REMOVE HARDCODED FILENAMES BEFORE TURNING IT IN
    #inputFileName = "test3_bin.txt"
    #outputFileName = "team3_out"
    return inputFileName, outputFileName


def getAllInstr():
    inputFileName, outputFileNAme = inputOutput()
    instructions = [line.rstrip() for line in open(inputFileName, 'rb')]
    for g in range(len(instructions)):
        allInstr.append((int(instructions[g], base=2)))
        # only read until break
        if instructions[g] == '11111110110111101111111111100111':
            break


# reads the binary file
# populates all appropriate lists
class Dissembler:
    inputFileName, outputFileName = inputOutput()
    print inputFileName

    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2, arg1Str, arg2Str, arg3Str, opcodeStr, instrSpaced):
        self.instructions = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInst = numInstrs
        self.arg1 = args1
        self.arg2 = args2
        self.arg3 = args3
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.opcodeStr = opcodeStr
        self.instrSpaced = instrSpaced

    def get_opcode(self):
        for j in range(len(self.instructions)):
            op = (int(self.instructions[j]) % 0x100000000) >> 21
            self.opcode.append(op)

    def findop(self):

        # returns twos complement value of passed number
        def twos_comp(val, bits):
            if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
                val = val - (1 << bits)  # compute negative value
            return val  # return positive value as is

        for j in range(len(self.opcode)):
            if self.opcode[j] == ADD:
                self.opcodeStr.append("ADD ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & rmMask) >> 16))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", R" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == SUB:
                self.opcodeStr.append("SUB ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & rmMask) >> 16))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", R" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == AND:
                self.opcodeStr.append("AND ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & rmMask) >> 16))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", R" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == ORR:
                self.opcodeStr.append("ORR ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & rmMask) >> 16))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", R" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == LSL:
                self.opcodeStr.append("LSL ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & shmtMask) >> 10))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == LSR:
                self.opcodeStr.append("LSR ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & shmtMask) >> 10))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]))
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == ASR:
                self.opcodeStr.append("ASR ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & shmtMask) >> 10))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == EOR:
                self.opcodeStr.append("EOR ")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & rmMask) >> 16))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", R" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:16] + " "
                                        + instrString[16:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] in ADDI:
                self.opcodeStr.append("ADDI")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & imMask) >> 10))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:10] + " " + instrString[10:22] + " "
                                        + instrString[22:27] + " " + instrString[27:32] + "\t")

            elif self.opcode[j] in SUBI:
                self.opcodeStr.append("SUBI")
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg2.append(((self.instructions[j] & imMask) >> 10))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:10] + " " + instrString[10:22] + " "
                                        + instrString[22:27] + " " + instrString[27:32] + "\t")

            elif self.opcode[j] == STUR:
                self.opcodeStr.append("STUR")
                self.arg1.append(((self.instructions[j] & rdMask) >> 0))
                self.arg2.append(((self.instructions[j] & addrMask) >> 12))
                self.arg3.append(((self.instructions[j] & rnMask) >> 5))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", [R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]) + "]")
                self.dest.append(self.arg1[j])
                self.src1.append(self.arg3[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:20] + " "
                                        + instrString[20:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] == LDUR:
                self.opcodeStr.append("LDUR")
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg2.append(((self.instructions[j] & addrMask) >> 12))
                self.arg1.append(((self.instructions[j] & rnMask) >> 5))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", [R" + str(self.arg1[j]))
                self.arg3Str.append(", #" + str(self.arg2[j]) + "]")
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:11] + " " + instrString[11:20] + " "
                                        + instrString[20:22] + " " + instrString[22:27]
                                        + " " + instrString[27:32])

            elif self.opcode[j] in CBZ:
                self.opcodeStr.append("CBZ ")
                self.arg1.append(twos_comp(((self.instructions[j] & addr2Mask) >> 5), 19))
                self.arg2.append("")
                self.arg3.append((self.instructions[j] & rdMask))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", #" + str(self.arg1[j]))
                self.arg3Str.append("")
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:8] + " " + instrString[8:27] + " "
                                        + instrString[27:32])

            elif self.opcode[j] in CBNZ:
                self.opcodeStr.append("CBNZ")
                self.arg1.append(twos_comp(((self.instructions[j] & addr2Mask) >> 5), 19))
                self.arg2.append("")
                self.arg3.append((self.instructions[j] & rdMask))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", #" + str(self.arg1[j]))
                self.arg3Str.append("")
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:8] + " " + instrString[8:27] + " "
                                        + instrString[27:32])

            elif self.opcode[j] in MOVZ:
                self.opcodeStr.append("MOVZ")
                self.arg1.append(((self.instructions[j] & imdataMask) >> 5))
                self.arg2.append(((self.instructions[j] & imsftMask) >> 21))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", " + str(self.arg1[j]))
                self.arg3Str.append(", LSL " + str(self.arg2[j] * 16))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:9] + " " + instrString[9:11] + " "
                                        + instrString[11:27] + " " + instrString[27:32] + "\t")

            elif self.opcode[j] in MOVK:
                self.opcodeStr.append("MOVK")
                self.arg1.append(((self.instructions[j] & imdataMask) >> 5))
                self.arg2.append(((self.instructions[j] & imsftMask) >> 21))
                self.arg3.append(((self.instructions[j] & rdMask) >> 0))
                self.arg1Str.append("R" + str(self.arg3[j]))
                self.arg2Str.append(", " + str(self.arg1[j]))
                self.arg3Str.append(", LSL " + str(self.arg2[j] * 16))
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:9] + " " + instrString[9:11] + " "
                                        + instrString[11:27] + " " + instrString[27:32] + "\t")

            elif self.opcode[j] in B:
                self.opcodeStr.append("B\t")
                self.arg1.append("")
                self.arg2.append("")
                self.arg3.append(twos_comp((self.instructions[j] & bMask), 26))
                self.arg1Str.append("#" + str(self.arg3[j]))
                self.arg2Str.append("")
                self.arg3Str.append("")
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:6] + " " + instrString[6:32] + "   ")

            elif self.opcode[j] == NOP:
                self.opcodeStr.append("NOP")
                self.arg1.append("")
                self.arg2.append("")
                self.arg3.append("")
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:8] + " " + instrString[8:11] + " "
                                        + instrString[11:16] + " " + instrString[16:21]
                                        + " " + instrString[21:26]) + " " + instrString[26:32]

            elif self.opcode[j] == BREAK:
                self.opcodeStr.append("BREAK")
                self.arg1.append("")
                self.arg2.append("")
                self.arg3.append("")
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                self.dest.append(self.arg3[j])
                self.src1.append(self.arg1[j])
                self.src2.append(self.arg2[j])
                instrString = "{0:b}".format(self.instructions[j])
                self.instrSpaced.append(instrString[0:8] + " " + instrString[8:11] + " " + instrString[11:16] + " " +
                                        instrString[16:21] + " " + instrString[21:26] + " " + instrString[26:32])

                # reads everything after the break instruction
                for k in range(self.numInst, len(self.instructions)):
                    # append all data after the break to binMem
                    binMem.append(int(self.instructions[k], base=2))

                for k in range(len(binMem)):
                    # convert all values in binMem to twos complement
                    twos = twos_comp(binMem[k], 32)
                    self.instrSpaced.append(self.instructions[self.numInst + k][0:32])
                    self.opcodeStr.append(str(twos))
                    self.arg1.append("")
                    self.arg2.append("")
                    self.arg3.append("")
                    self.arg1Str.append("")
                    self.arg2Str.append("")
                    self.arg3Str.append("")

    def print_dissembled(self):
        outFile = open(self.outputFileName + "_dis.txt", 'w')
        pc = 96
        for j in range(len(instrSpaced)):
            print >> outFile, (instrSpaced[j] + "\t" + str(pc) + "\t\t" + opcodeStr[j] + "\t" + arg1Str[j] + arg2Str[j] +
                               arg3Str[j])
            pc += 4

    def run(self):
        #self.populate_allInstr()
        self.get_opcode()
        self.findop()
        self.print_dissembled()


class WriteBack:
    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2, postAlu, postMem, r):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.pAlu = postAlu
        self.pMem = postMem
        self.reg = r

    def write(self):
        # post ALU
        if self.pAlu[0] != -1 and self.pAlu[1] != -1:
            # update the register at position 1 with the value in position 0
            self.reg[self.destReg[self.pAlu[1]]] = self.pAlu[0]
            # clear out the buffer
            self.pAlu[0] = -1
            self.pAlu[1] = -1
        # post MEM
        if self.pMem[0] != -1 and self.pMem[1] != -1:
            self.reg[self.destReg[self.pMem[1]]] = self.pMem[0]
            # clear out the buffer
            self.pMem[0] = -1
            self.pMem[1] = -1

    def run(self):
        self.write()


class Alu:
    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2, preAlu, postAlu, reg):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = args1
        self.arg2 = args1
        self.arg3 = args1
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.pre = preAlu
        self.post = postAlu
        self.reg = reg

    def math(self):

        # looks for opcode of instruction index in preAlu buffer
        # puts result of calculation into postAlu[0], index of instruction into postAlu[1]
        if opcode[self.pre[0]] == ADD:
            self.post[0] = self.reg[self.arg1[self.pre[0]]] + self.reg[self.arg2[self.pre[0]]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == SUB:
            self.post[0] = self.reg[self.arg1[self.pre[0]]] - self.reg[self.arg2[self.pre[0]]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == AND:
            self.post[0] = self.reg[self.arg2[self.pre[0]]] & self.reg[self.arg1[self.pre[0]]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == ORR:
            self.post[0] = self.reg[self.arg2[self.pre[0]]] | self.reg[self.arg1[self.pre[0]]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == LSL:
            self.post[0] = self.reg[self.arg1[self.pre[0]]] << self.arg2[self.pre[0]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == ASR:
            self.post[0] = self.reg[self.arg1[self.pre[0]]] / (2 ** self.arg2[self.pre[0]])
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == EOR:
            self.post[0] = self.reg[self.arg2[self.pre[0]]] ^ self.reg[self.arg1[self.pre[0]]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] == LSR:
            self.post[0] = self.reg[self.arg1[self.pre[0]]] % 0x100000000 >> self.arg2[self.pre[0]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] in ADDI:
            self.post[0] = int(self.reg[self.arg1[self.pre[0]]] + self.arg2[self.pre[0]])
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] in SUBI:
            self.post[0] = self.reg[self.arg1[self.pre[0]]] - self.arg2[self.pre[0]]
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] in MOVZ:
            self.post[0] = self.arg1[self.pre[0]] << (self.arg2[self.pre[0]] * 16)
            self.post[1] = self.pre[0]
        elif opcode[self.pre[0]] in MOVK:
            self.post[0] += int(self.arg1[self.pre[0]] << (self.arg2[self.pre[0]] * 16))
            self.post[1] = self.pre[0]

        self.pre[0] = self.pre[1]
        self.pre[1] = -1

    def run(self):
        if self.pre[0] != -1:
            self.math()

 # TODO: write this one -- no idea what it's doing
class Mem:

    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2, preMem, postMem, cache):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.cache = cache
        self.premem = preMem
        self.postmem = postMem

    def mem(self):
    #checks the first in line of premem for STUR/LDUR
        isSW = False
        isLD = False
        if self.opcode[self.premem[0]] == STUR:
          isSW = True
        elif self.opcode[self.premem[0]] == LDUR:
          isLD = True
    #if hits and STUR then data in sent to cache
        cacheData = cache.accessMem(self.premem[0], self.premem[0], isSW, reg[self.premem[0]])
    #if hits and LDUR then data is sent to postmem
    #buffers gets updated
        if cacheData and isLD:
          self.postmem[0] = cacheData[1]
          self.postmem[1] = self.premem[0]
        if cacheData:
          self.premem[0] = self.premem[1]
          self.premem[1] = -1

    def run(self):
        self.mem()


class InstructionFetch:

    it = 0  # iterator for fetching instructions into the buffer from allinstr
    isStalled = 0  # number of cycles we're stalled for
    numFetched = 0
    breakFlag = False
    preIssueFull = False

    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2, cache, preIssue):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = args1
        self.arg2 = args2
        self.arg3 = args3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.pc = PC
        self.reg = reg
        self.Cache = cache
        self.preIssue = preIssue

    def fetch(self):
        # during - We will fetch up to two empty slots in the preissue buffer.
        # We get an instruction, check in cache for it, If hit we will determine if it is a branch or B instructions.
        # If is a branch instruction will check for hazards and if none perform the branch instruction. B done without checking.
        # The branch will never get posted to the pre issue buffer.
        # Checks for break  instruction and if found perfoms clean up making  sure all instructions finish. Else we don't have a break instruction.
        # If we can't get the first instruction out of cache we can't fetch the next instruction.

        # 1.	If the fetch unit is stalled, no instruction can be fetched at the current cycle (no pre-fetching).
        # The fetch unit can be stalled due to a branch instruction or a cache miss (cache is described below)
        if self.isStalled > 0:
            self.isStalled -= 1
            return True

        # find current largest empty space in preIssue
        preIssueIndex = 0
        for m in range(len(self.preIssue)):
            if self.preIssue[m] == -1:
                break
            else:
                preIssueIndex += 1

        # 2. If there is no room in the pre-issue buffer, no instructions can be fetched at the current cycle
        if preIssueIndex == 4:
            self.preIssueFull = True

        while self.numFetched != 2:
            if self.preIssueFull:
                return True
            if self.breakFlag:
                if (self.preIssue == [-1, -1, -1, -1]
                        and preAlu == [-1, -1]
                        and postAlu == [-1, -1]
                        and preMem == [-1, -1]
                        and postMem == [-1, -1]):
                    # all buffers empty
                    return False
                else:
                    return False
            else:
                hit = self.Cache.accessMem(-1, self.it, False, -1)
                if hit[0] and not self.preIssueFull:
                    if opcode[self.it] == B:
                        self.branch()
                    # TODO: add support for CBZ & CBNZ
                    elif opcode[self.it] == BREAK:
                        self.breakFlag = True
                        return True
                    else:
                        # find first empty space in preIssue, assign hit value to that
                        # then go to next instruction
                        r = 0
                        while self.preIssue[r] != -1:
                            if self.preIssueFull:
                                break
                            r += 1
                            if self.preIssue[r] == -1:
                                break
                            elif r > 4:
                                break
                        self.preIssue[r] = self.it
                        self.it += 1
                        self.numFetched += 1
                elif not hit[0]:
                    # stall for one cycle
                    return True
        self.numFetched = 0
        return True

    def branch(self):
        if opcode[self.it] in B:
            self.pc += arg3[self.it]
        elif opcode[self.it] in CBZ:
            if reg[arg3[self.it]] == 0:
                self.pc += arg1[self.it]
        elif opcode[self.it] in CBNZ:
            if reg[arg3[self.it]] != 0:
                self.pc += arg1[self.it]
        return True

    def run(self):
        cont = self.fetch()
        if cont:
            return True
        else:
            return False


# TODO: write this one -- currently just moving from pre to post
class Issue:
    numInPreIssueBuff = 0
    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2

    def pI(self):
        spaceInPreAlu = 0
        for k in range(len(preAlu)):
            if preAlu[k] == -1:
                spaceInPreAlu += 1  # index of filled space in preAlu
        spaceInPreMem = 0
        for k in range(len(preMem)):
            if preMem[k] == -1:
                spaceInPreMem += 1
        r = 0
        while preIssue[r] != -1:
            if self.instruction[preIssue[r]] >> 21 != LDUR and self.instruction[preIssue[r]] >> 21 != STUR:
                if spaceInPreAlu > 0:
                    preAlu[spaceInPreAlu % 2] = preIssue[r]
                    print "\tpreAlu", preAlu
                    if r+1 < 3:
                        preIssue[r] = preIssue[r+1]
                        preIssue[r+1] = -1
                    else:
                        preIssue[r] = -1
                    spaceInPreAlu -= 1
            elif self.instruction[preIssue[r]] >> 21 == LDUR and self.instruction[preIssue[r]] >> 21 == STUR:
                if spaceInPreMem > 0:
                    preMem[spaceInPreMem % 2] = preIssue[r]
                    spaceInPreMem -= 1


    def run(self):
        self.pI()


#
#   # 1. Determine what's in the preIssueBuff at start of the cycle to get initial value ( numInIssueAtClockCycleBegin)
#   # 2. Process instructions in preIssueBuff in 0 .. 3 order. Look for hazards of all types between mostly adjacent instructions.
#   # while( numIssued < 2 and numInPreIssueBuff > 0 and curr < 4 ): # curr is current pre issue element - means you are int he queue
#   # 2.1 Start with curr = preBuff [0]
#   # 2.2 Check for room in the preMemBuff and preALUBuff
#   #if sim.isMemOp( index ) and not -1 in sim.preMemBuff:
#   # ..... ..... .....
#   #
#   # 2.3 Do WAR hazard check  - I am dropping this requirement
#
#   #
#   # War Check -- later instruction tried to read an operand before earlier instruction writes it
#   # WAR Hazard is uncommon/impossible in a reasonable(in-order) pipeline but lets check first
#   # We will chech each preIssuebuf entry against other preIssueBuff entries that are 'leftover' during processing
#   # and against preMEM and preALU. IF the destination of the current instruction is equal to either source of a
#   # previous instruction this is a hazard
#
#   # first check against other preIssue. A little different thinking here. Start with curr = 0 which skips the
#   # following check. If the isntruction has an issue then the next pass it will be checked against the 'current' instruction
#   # not sure of how else to do this
#   if curr > 0:
#       for i in range(0, curr):
#           if dest[cycle] == src1[preBuff[i]] or dest[cycle] == src2[preBuff[i]]:
#               # found WAR in Issue buffer
#               issueMe = False
#               break
#
#   # next against preMem
#   if Sim.isMemOp(index):
#       for i in range(0, len(preBuff)):
#           if preBuff[i] != -1:
#               if dest[index] == src1[preBuff[i]] or dest[index] == src2[preBuff[i]]:
#                   # found WAR in pre issue buff
#                   issueMe = False
#                   break
#   # finally against preAlu
#   if not Sim.isMemOp(index):
#       for i in range(0, len(preAlu)):
#           if preAlu[i] != -1:
#               if dest[index] == src1[preBuff[i]] or dest[index] == src2[preBuff[i]]:
#                   # found WAR in pre issue buff
#                   issueMe = False
#                   break


# TODO: finish this one
class Cache:

    # 4 sets of two blocks -- 2 words / block
    # [ valid, dirty, tag, data, data ]
    cacheSets = [
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],  # set 0, blocks 1 & 2
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],  # set 1, blocks 1 & 2
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],  # set 2, blocks 1 & 2
        [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  # set 3, blocks 1 & 2
    ]
    lruBit = [0, 0, 0, 0]  # maps to a set
    tagMask = 4294967264
    setMask = 24
    justMissedList = []

    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2):
        self.instruction = instrs
        self.opcode = opcodes
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.memory = instrs + mem


    def accessMem(self, memIndex, instructionIndex, isWriteToMem, dataToWrite):
        dataWord = 0
        address = 0
        setNum = 0
        address1 = 0
        address2 = 0
        assocblock = 0
        hit = False

        #print "1"
        # 1. Given this index, calculate the address of the memory location (example 0 -> 96),
        # figure out which block in set (dataword = 0 or 1)
        #       Check if instruction or data and calculate appropriate address
        if memIndex == -1:
            address = 96 + (4 * instructionIndex)
        else:
            address = 96 + (4 * Sim.numInstructions) + (4 * memIndex)
        #print "2"
        # 2. Based on address, align address to two word alignment and create addresses for the two words in block
        # (address1 and address2) based on dataword value.
        # Remember, we are enforcing that block 0 is associated with address 96+ n8!
        if address % 8 == 0:
            dataWord = 0  # block 0 was the address
            address1 = address
            address2 = address + 4
            # check for 'alignment'
            # this picks the second word as address so we need to fix it
            # set address1 - block 1 address to address -4
        elif address % 8 != 0:
            dataWord = 1  # block 1 was the address
            address1 = address - 4
            address2 = address

        # 3. Get the word value for each address (data1 and data2) from the memory. We are not in cache yet!
        # if address1 is an instruction go to instruction list and get it
        if address1 < 96 + (4 * Sim.numInstructions):
            data1 = self.instruction[Sim.getIndexOfMemAddress(address1, False)]
        else:
            data1 = self.memory[Sim.getIndexOfMemAddress(address1, False)]
        if address2 < 100 + (4 * Sim.numInstructions):
            data2 = self.instruction[Sim.getIndexOfMemAddress(address2, False)]
        else:
            data2 = self.memory[Sim.getIndexOfMemAddress(address2, False)]

            # 4. IF WRITING TO MEM (memIndex != -1 and isWriteToMem ==1)
        #       Overwrite either data1 or data2 with the passed in dataToWrite based on dataword value

        if isWriteToMem and dataWord == 0:
            data1 = dataToWrite
        elif isWriteToMem and dataWord == 1:
            data2 = dataToWrite

        # 5. Decode the cache address from the address for word0 (tag, set)
        setNum = (address1 & self.setMask) >> 3
        tag = (address1 & self.tagMask) >> 5
        # 6. Look in cache and see if the address we are looking for is either one of the blocks.
        # If hit, set assocblock to the block num.
        if self.cacheSets[setNum][0][0] == 1 and self.cacheSets[setNum][0][2] == tag:
            hit = True
            assocblock = 0
        elif self.cacheSets[setNum][1][0] == 1 and self.cacheSets[setNum][1][2] == tag:
            hit = True
            assocblock = 1
        else:
            if self.justMissedList.count(address1) == 0:
                self.justMissedList.append(address1)
                return [False, 0]

        # 7. If hit and we are writing to mem
        #   update cache blocks dirty bit
        #   recognize that we should only be writing data to cache other than the initial load
        if(hit):#   return (True, word from requested set/block)
          if hit and isWriteToMem:
              self.cacheSets[setNum][assocblock][1] = 1
              self.lruBit[setNum] = (assocblock + 1) % 2
              self.cacheSets[setNum][assocblock][dataWord + 3] = dataToWrite

            # 8. If hit and we are NOT writing to mem
            #   update set LRU bit, return (True, word requested from set / block)
          elif hit:
              self.lruBit[setNum] = (assocblock + 1) % 2
              return [True, self.cacheSets[setNum][assocblock][dataWord + 3]]
        # not returning yet means we have a miss

        # 9. If miss figure out if this is the initial miss or the second miss
        if address1 in self.justMissedList:
            while self.justMissedList.count(address1) > 0:
                self.justMissedList.remove(address1)
                # 12. Only other case is first miss.
                #   Add address to justMissedList, return (False, 0)

        else:
            # VALID MISS on cycle
            # add the memory address to the just missed list
            if self.justMissedList.count(address1) == 0:
                self.justMissedList.append(address1)
                return False, 0

        # 10. If second miss we need to go to memory and get the appropriate data and if there is already something there
        # we need to first write back if we have a dirty DATA entry in the cache where we need to put the fetched word.

        if self.cacheSets[setNum][self.lruBit[setNum]][1] == 1:
            # write back the memory address asociated with the block
            wbAddr = self.cacheSets[setNum][self.lruBit[setNum]][2]  # tag
            # modify tag to get back to the original address, remember all addresses are inherently word aligned
            # lower 2 bits are zero !!!!
            wbAddr = (wbAddr << 5) + (setNum << 3)
            # we will, we better,  only have dirty cache entries for data mem, not instructions
            # update data mem locations!
            # if the cache tag: set gives us a double word aligned value ie. 96,104,
            # Lets say that word 0 is the last instruction and word is on the first data element
            # we would only want to update the second word
            # But if lets say we have two data elements, then the cache would have two data element and we would write
            # back both even if one was dirty.  This takes care of the boundary condition.
            if wbAddr >= (Sim.numInstructions * 4) + 96:
                Sim.memory[Sim.getIndexOfMemAddress(wbAddr, False)] = self.cacheSets[setNum][self.lruBit[setNum]][3]
            if wbAddr + 4 >= (Sim.numInstructions * 4) + 96:
                Sim.memory[Sim.getIndexOfMemAddress(wbAddr + 4, False)] = self.cacheSets[setNum][self.lruBit[setNum]][4]
            # now update the cache flag bits
        self.cacheSets[setNum][self.lruBit[setNum]][0] = 1  # valid we are writing a block
        self.cacheSets[setNum][self.lruBit[setNum]][1] = 0  # reset the dirty bit
        if isWriteToMem:
            self.cacheSets[setNum][self.lruBit[setNum]][1] = 1  # dirty if is data mem is dirty again, instruction mem never dirty
        # update both words in the actual cache block in set
        self.cacheSets[setNum][self.lruBit[setNum]][2] = tag  # tag
        self.cacheSets[setNum][self.lruBit[setNum]][3] = data1  # data
        self.cacheSets[setNum][self.lruBit[setNum]][4] = data2  # nextData
        self.lruBit[setNum] = (self.lruBit[setNum] + 1) % 2  # set lru to show block is recently used
        # finally
        # 11. Then return (TRUE , word requested from cache)
        return True, self.cacheSets[setNum][(self.lruBit[setNum] + 1) % 2][dataWord + 3]  # dataword was the actual word that generated the hit


# main simulator class -- pulls all other classes together
class SimClass:

    # init start values
    cycle = 1
    startAddress = 96 + (4 * len(opcode))  # PC at break + 4

    def __init__(self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs, dest, src1, src2,
                 WB, ALU, MEM, Issue, fetch, cache, reg, preIssue, preAlu, preMem, postAlu, postMem):
        self.instruction = instrs
        self.opcode = opcodes
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.memory = instrs + mem
        self.reg = reg
        self.preIssue = preIssue
        self.preAlu = preAlu
        self.preMem = preMem
        self.postAlu = postAlu
        self.postMem = postMem

        # pipeline components
        self.WB = WB
        self.ALU = ALU
        self.MEM = MEM
        self.Issue = Issue
        self.fetch = fetch
        self.cache = cache

    def printState(self):
        outFile = open(disassemble.outputFileName + "_pipeline.txt", 'a')

        # store each results of each cycle in outFile
        print >> outFile, "--------------------"
        print >> outFile, "Cycle:" + str(self.cycle) + "\n"
        # print buffer and queue
        print >> outFile, "Pre-Issue Buffer: "
        if preIssue[0] != -1:
            print >> outFile, "\tEntry 0:" + "\t", "[" + opcodeStr[preIssue[0]] + "\t" + arg1Str[preIssue[0]] + arg2Str[preIssue[0]] + arg3Str[preIssue[0]] + "]"
        else:
            print >> outFile, "\tEntry 0:" + "\t"
        if preIssue[1] != -1:
            print >> outFile, "\tEntry 1:" + "\t", "[" + opcodeStr[preIssue[1]] + "\t" + arg1Str[preIssue[1]] + arg2Str[preIssue[1]] + arg3Str[preIssue[1]] + "]"
        else:
            print >> outFile, "\tEntry 1:" + "\t"
        if preIssue[2] != -1:
            print >> outFile, "\tEntry 2:" + "\t", "[" + opcodeStr[preIssue[2]] + "\t" + arg1Str[preIssue[2]] + arg2Str[preIssue[2]] + arg3Str[preIssue[2]] + "]"
        else:
            print >> outFile, "\tEntry 2:" + "\t"
        if preIssue[3] != -1:
            print >> outFile, "\tEntry 3:" + "\t", "[" + opcodeStr[preIssue[3]] + "\t" + arg1Str[preIssue[3]] + arg2Str[preIssue[3]] + arg3Str[preIssue[3]] + "]"
        else:
            print >> outFile, "\tEntry 3:" + "\t"

        print >> outFile, "Pre_ALU Queue:"
        if preAlu[0] != -1:
            print >> outFile, "\tEntry 0:" + "\t", "[" + opcodeStr[preAlu[0]] + "\t" + arg1Str[preAlu[0]] + arg2Str[preAlu[0]] + arg3Str[preAlu[0]] + "]"
        else:
            print >> outFile, "\tEntry 0:" + "\t"
        if preAlu[1] != -1:
            print >> outFile, "\tEntry 1:" + "\t", "[" + opcodeStr[preAlu[1]] + "\t" + arg1Str[preAlu[1]] + arg2Str[preAlu[1]] + arg3Str[preAlu[1]] + "]"
        else:
            print >> outFile, "\tEntry 1:" + "\t"

        print >> outFile, "Post_ALU Queue"
        if postAlu[0] != -1:
            print >> outFile, "\tEntry 0:" + "\t", "[" + opcodeStr[postAlu[1]] + "\t" + arg1Str[postAlu[1]] + arg2Str[postAlu[1]] + arg3Str[postAlu[1]] + "]"
        else:
            print >> outFile, "\tEntry 0:" + "\t"
        print >> outFile, "Pre_MEM Queue"
        if preMem[0] != -1:
            print >> outFile, "\tEntry 0:" + "\t", "[" + opcodeStr[preMem[0]] + "\t" + arg1Str[preMem[0]] + arg2Str[preMem[0]] + arg3Str[preMem[0]] + "]"
        else:
            print >> outFile, "\tEntry 0:" + "\t"
        if preMem[1] != -1:
            print >> outFile, "\tEntry 1:" + "\t", "[" + opcodeStr[preMem[1]] + "\t" + arg1Str[preMem[1]] + arg2Str[preMem[1]] + arg3Str[preMem[1]] + "]"
        else:
            print >> outFile, ("\tEntry 1:" + "\t")
        print >> outFile, "Post_MEM Queue"
        if postMem[0] != -1:
            print >> outFile, "\tEntry 0:" + "\t", "[" + opcodeStr[postMem[1]] + "\t" + arg1Str[postMem[1]] + arg2Str[postMem[1]] + arg3Str[postMem[1]] + "]"
        else:
            print >> outFile, "\tEntry 0:" + "\t"
        # print registers
        print >> outFile, "\nregisters:",
        for q in range(len(self.reg)):
            if q % 8 == 0:
                if q < 10:
                    print >> outFile, "\nr0" + str(q) + ":",
                else:
                    print >> outFile, "\nr" + str(q) + ":",
            print >> outFile, self.reg[q], "\t",

        # print cache
        print >> outFile, "\n\nCache"
        print >> outFile, "Set 0:\tLRU=" + str(self.cache.lruBit[0])
        print >> outFile, "\tEntry 0:[(" + str(self.cache.cacheSets[0][0][0]) + "," + str(self.cache.cacheSets[0][0][1]) + "," + str(self.cache.cacheSets[0][0][2]) + ")<" + str(self.cache.cacheSets[0][0][3]) + "," + str(self.cache.cacheSets[0][0][4]) + ">]"
        print >> outFile, "\tEntry 1:[(" + str(self.cache.cacheSets[0][1][0]) + "," + str(self.cache.cacheSets[0][1][1]) + "," + str(self.cache.cacheSets[0][1][2]) + ")<" + str(self.cache.cacheSets[0][1][3]) + "," + str(self.cache.cacheSets[0][1][4]) + ">]"
        print >> outFile, "Set 1:\tLRU=" + str(self.cache.lruBit[1])
        print >> outFile, "\tEntry 0:[(" + str(self.cache.cacheSets[1][0][0]) + "," + str(self.cache.cacheSets[1][0][1]) + "," + str(self.cache.cacheSets[1][0][2]) + ")<" + str(self.cache.cacheSets[1][0][3]) + "," + str(self.cache.cacheSets[1][0][4]) + ">]"
        print >> outFile, "\tEntry 1:[(" + str(self.cache.cacheSets[1][1][0]) + "," + str(self.cache.cacheSets[1][1][1]) + "," + str(self.cache.cacheSets[1][1][2]) + ")<" + str(self.cache.cacheSets[1][1][3]) + "," + str(self.cache.cacheSets[1][1][4]) + ">]"
        print >> outFile, "Set 2:\tLRU=" + str(self.cache.lruBit[2])
        print >> outFile, "\tEntry 0:[(" + str(self.cache.cacheSets[2][0][0]) + "," + str(self.cache.cacheSets[2][0][1]) + "," + str(self.cache.cacheSets[2][0][2]) + ")<" + str(self.cache.cacheSets[2][0][3]) + "," + str(self.cache.cacheSets[2][0][4]) + ">]"
        print >> outFile, "\tEntry 1:[(" + str(self.cache.cacheSets[2][1][0]) + "," + str(self.cache.cacheSets[2][1][1]) + "," + str(self.cache.cacheSets[2][1][2]) + ")<" + str(self.cache.cacheSets[2][1][3]) + "," + str(self.cache.cacheSets[2][1][4]) + ">]"
        print >> outFile, "Set 3:\tLRU=" + str(self.cache.lruBit[3])
        print >> outFile, "\tEntry 0:[(" + str(self.cache.cacheSets[3][0][0]) + "," + str(self.cache.cacheSets[3][0][1]) + "," + str(self.cache.cacheSets[3][0][2]) + ")<" + str(self.cache.cacheSets[3][0][3]) + "," + str(self.cache.cacheSets[3][0][4]) + ">]"
        print >> outFile, "\tEntry 1:[(" + str(self.cache.cacheSets[3][1][0]) + "," + str(self.cache.cacheSets[3][1][1]) + "," + str(self.cache.cacheSets[3][1][2]) + ")<" + str(self.cache.cacheSets[3][1][3]) + "," + str(self.cache.cacheSets[3][1][4]) + ">]"

        # print data
        # print data
        if data:
            dataCount = 0
            for l in range(len(data)):
                if l % 8 == 0:
                    print >> outFile, ("\n" + str(self.startAddress + (dataCount * 4)) + ":"),
                print >> outFile, (str(data[l]) + "\t"),
                dataCount += 1
            print >> outFile
        else:
            print >> outFile, "\n\n\n",

    def isMemOp(self, index):
        if opcode[index] == STUR or opcode[index] == LDUR:
            return True
        else:
            return False

    def getIndexOfMemAddress(self, address, isInst):
        memAddr = address - 96
        if memAddr < len(self.instruction):
            return memAddr
        else:
            # address is out of range, return garbage
            return -1


    def run(self):
        go = True
        while go:
            print "WB:"
            self.WB.run()

            print "ALU:"
            print "\tpreAlu", self.preAlu
            print "\tpostAlu", self.postAlu
            self.ALU.run()
            print "\tpreAlu", self.preAlu
            print "\tpostAlu", self.postAlu

            print "MEM:"
            self.MEM.run()
            print "\tpreAlu", self.preAlu
            print "\tpostAlu", self.postAlu

            print "Issue:"
            self.Issue.run()
            print "\tpreAlu", self.preAlu
            print "\tpostAlu", self.postAlu

            print "fetch:"
            go = self.fetch.run()
            print "\tpreAlu", self.preAlu
            print "\tpostAlu", self.postAlu

            print "printState:"
            self.printState()
            print "\tpreAlu", self.preAlu
            print "\tpostAlu", self.postAlu

            print "\ncycle:", self.cycle
            self.cycle += 1

# end of SimClass


# disassemble & run simulator
getAllInstr()
numInst = len(allInstr)
disassemble = Dissembler(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2, arg1Str, arg2Str, arg3Str, opcodeStr, instrSpaced)
disassemble.run()
WB = WriteBack(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2, postAlu, postMem, reg)
ALU = Alu(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2, preAlu, postAlu, reg)
cache = Cache(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2)
MEM = Mem(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2, preAlu, postAlu, cache)
Issue = Issue(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2)
fetch = InstructionFetch(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2, cache, preIssue)
Sim = SimClass(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2, WB, ALU, MEM, Issue, fetch, cache, reg, preIssue, preAlu, preMem, postAlu, postMem)

Sim.run()
