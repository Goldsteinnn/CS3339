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
preIssue = [-1, -1, -1, -1]
preAlu = [-1, -1]
postAlu = [-1]
preMem = [-1, -1]
postMem = [-1]

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


class Dissembler:

    numInst = 0  # number of instructions in the file

    def populate_allInstr(self):
        for g in range(len(instructions)):
            allInstr.append((int(instructions[g], base=2)))
            self.numInst += 1
            # only read until break
            if instructions[g] == '11111110110111101111111111100111':
                break

    def get_opcode(self):
        for j in range(len(allInstr)):
            opcode.append(allInstr[j] >> 21)

    def findop(self):

        # returns twos complement value of passed number
        def twos_comp(val, bits):
            if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
                val = val - (1 << bits)  # compute negative value
            return val  # return positive value as is

        for j in range(len(opcode)):
            if opcode[j] == ADD:
                opcodeStr.append("ADD ")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " "
                                   + str(instructions[j][16:22]) + " " + str(instructions[j][22:27])
                                   + " " + str(instructions[j][27:32]))

            elif opcode[j] == SUB:
                opcodeStr.append("SUB ")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " "
                                   + str(instructions[j][16:22]) + " " + str(instructions[j][22:27])
                                   + " " + str(instructions[j][27:32]))

            elif opcode[j] == AND:
                opcodeStr.append("AND ")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & rmMask) >> 16))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", R" + str(arg2[j]))
                instrSpaced.append(str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " "
                                   + str(instructions[j][16:22]) + " " + str(instructions[j][22:27])
                                   + " " + str(instructions[j][27:32]))

            elif opcode[j] == ORR:
                opcodeStr.append("ORR ")
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
                opcodeStr.append("LSL ")
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
                opcodeStr.append("LSR ")
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
                opcodeStr.append("ASR ")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & shmtMask) >> 10))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:16]) + " " + str(instructions[j][16:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))

            elif opcode[j] == EOR:
                opcodeStr.append("EOR ")
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
                    str(instructions[j][0:10]) + " " + str(instructions[j][10:22]) + " " + str(instructions[j][22:27])
                    + " " + str(instructions[j][27:32]) + " ")

            elif opcode[j] in SUBI:
                opcodeStr.append("SUBI")
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & imMask) >> 10))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]))
                instrSpaced.append(
                    str(instructions[j][0:10]) + " " + str(instructions[j][10:22]) + " " + str(instructions[j][22:27])
                    + " " + str(instructions[j][27:32]) + " ")

            elif opcode[j] == STUR:
                opcodeStr.append("STUR")
                arg1.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg2.append(((int(instructions[j], base=2) & addrMask) >> 12))
                arg3.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", [R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]) + "]")
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:20]) + " " + str(instructions[j][20:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))

            elif opcode[j] == LDUR:
                opcodeStr.append("LDUR")
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg2.append(((int(instructions[j], base=2) & addrMask) >> 12))
                arg1.append(((int(instructions[j], base=2) & rnMask) >> 5))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", [R" + str(arg1[j]))
                arg3Str.append(", #" + str(arg2[j]) + "]")
                instrSpaced.append(
                    str(instructions[j][0:11]) + " " + str(instructions[j][11:20]) + " " + str(instructions[j][20:22])
                    + " " + str(instructions[j][22:27]) + " " + str(instructions[j][27:32]))

            elif opcode[j] in CBZ:
                opcodeStr.append("CBZ ")
                arg1.append(twos_comp(((int(instructions[j], base=2) & addr2Mask) >> 5), 19))
                arg2.append("")
                arg3.append((int(instructions[j], base=2) & rdMask))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", #" + str(arg1[j]))
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:8]) + " " + str(instructions[j][8:27]) + " " + str(instructions[j][27:32])
                    + "   ")

            elif opcode[j] in CBNZ:
                opcodeStr.append("CBNZ")
                arg1.append(twos_comp(((int(instructions[j], base=2) & addr2Mask) >> 5), 19))
                arg2.append("")
                arg3.append((int(instructions[j], base=2) & rdMask))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", #" + str(arg1[j]))
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:8]) + " " + str(instructions[j][8:27]) + " " + str(instructions[j][27:32])
                    + "   ")

            elif opcode[j] in MOVZ:
                opcodeStr.append("MOVZ")
                arg1.append(((int(instructions[j], base=2) & imdataMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & imsftMask) >> 21))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", " + str(arg1[j]))
                arg3Str.append(", LSL " + str(arg2[j] * 16))
                instrSpaced.append(
                    str(instructions[j][0:9]) + " " + str(instructions[j][9:11]) + " " + str(instructions[j][11:27]) +
                     " " + str(instructions[j][27:32]) + " ")

            elif opcode[j] in MOVK:
                opcodeStr.append("MOVK")
                arg1.append(((int(instructions[j], base=2) & imdataMask) >> 5))
                arg2.append(((int(instructions[j], base=2) & imsftMask) >> 21))
                arg3.append(((int(instructions[j], base=2) & rdMask) >> 0))
                arg1Str.append("R" + str(arg3[j]))
                arg2Str.append(", " + str(arg1[j]))
                arg3Str.append(", LSL " + str(arg2[j] * 16))
                instrSpaced.append(
                    str(instructions[j][0:9]) + " " + str(instructions[j][9:11]) + " " + str(instructions[j][11:27]) +
                    " " + str(instructions[j][27:32]) + " ")

            elif opcode[j] in B:
                opcodeStr.append("B\t")
                arg1.append("")
                arg2.append("")
                #arg3.append(((int(instructions[j], base=2) & bMask) >> 0))
                arg3.append(twos_comp((int(instructions[j], base=2) & bMask), 26))
                arg1Str.append("#" + str(arg3[j]))
                arg2Str.append("")
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:6]) + " " + str(instructions[j][6:32]) + "   ")

            elif opcode[j] == NOP:
                opcodeStr.append("NOP")
                arg1.append("")
                arg2.append("")
                arg3.append("")
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:8]) + " " + str(instructions[j][8:11]) + " "
                    + str(instructions[j][11:16]) + " " + str(instructions[j][16:21]) + " "
                    + str(instructions[j][21:26]) + " " + str(instructions[j][26:32]))

            elif opcode[j] == BREAK:
                opcodeStr.append("BREAK")
                arg1.append("")
                arg2.append("")
                arg3.append("")
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instrSpaced.append(
                    str(instructions[j][0:8]) + " " + str(instructions[j][8:11]) + " "
                    + str(instructions[j][11:16]) + " " + str(instructions[j][16:21]) + " "
                    + str(instructions[j][21:26]) + " " + str(instructions[j][26:32]))

                # reads everything after the break instruction
                for k in range(self.numInst, len(instructions)):
                    # append all data after the break to binMem
                    binMem.append(int(instructions[k], base=2))

                for k in range(len(binMem)):
                    # convert all values in binMem to twos complement
                    twos = twos_comp(binMem[k], 32)
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
            print >> outFile, (instrSpaced[j] + "\t" + str(pc) + "\t\t" + opcodeStr[j] + "\t" + arg1Str[j] + arg2Str[j] +
                               arg3Str[j])
            pc += 4

    def run(self):
        self.populate_allInstr()
        self.get_opcode()
        self.findop()
        self.print_dissembled()


class WriteBack:
    def write(self):
        if postAlu and postAlu[0] != -1 and postAlu[1] != -1:
            # update the register at position 1 with the instruction in position 0
            reg[postAlu[0]] = postAlu[1]
            # clear out the buffer
            postAlu[0] = -1
            postAlu[1] = -1
        if postMem and postMem[0] != -1 and postMem[1] != -1:
            reg[postMem[0]] = postMem[1]
            postMem[0] = -1
            postMem[1] = -1
    def run(self):
        self.write()


class Alu:
    def math(self):
        if preAlu:
            for k in preAlu:
                # ensure preAlu only holds 2 values
                if k == 2:
                    break
                if preAlu[k] == -1:
                    continue
                # find what operation to do; do operation
                if opcode[preAlu[k]] == ADD:
                    postAlu[0] = arg1[preAlu[k]] + arg2[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == SUB:
                    postAlu[0] = arg1[preAlu[k]] - arg2[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == AND:
                    postAlu[0] = arg2[preAlu[k]] & arg1[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == ORR:
                    postAlu[0] = arg2[preAlu[k]] | arg1[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == LSL:
                    postAlu[0] = arg1[preAlu[k]] << arg2[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == ASR:
                    postAlu[0] = arg1[preAlu[k]] / (2 ** arg2[preAlu[k]])
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == EOR:
                    postAlu[0] = arg2[preAlu[k]] ^ arg1[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == LSR:
                    postAlu[0] = arg1[preAlu[k]] % 0x100000000 >> arg2[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == ADDI:
                    postAlu[0] = arg1[preAlu[k]] + arg2[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == SUBI:
                    postAlu[0] = arg1[preAlu[k]] - arg2[preAlu[k]]
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == MOVZ:
                    postAlu[0] = arg1[preAlu[k]] << (arg2[preAlu[k]] * 16)
                    postAlu[1] = preAlu[k]
                elif opcode[preAlu[k]] == MOVK:
                    postAlu[0] += arg1[preAlu[k]] << (arg2[preAlu[k]] * 16)
                    postAlu[1] = preAlu[k]

    def run(self):
        self.math()


#TODO : write this one -- need cache
class InstructionFetch:

    def __init__(self):
        self.IfBuffer = [[-1, -1], [-1, -1]]

    def fetch(self):
        self.IfBuffer[0][0] = allInstr[Sim.address - 96]
        print(self.IfBuffer[0][0])

    def run(self):
        if self.fetch():
            return True
        else:
            return False


#TODO: write this one -- finish
class Issue:
    preBuff = [-1, -1, -1, -1]
    curr = preBuff[0]
    numIssued = 0
    numInPreIssueBuff = len(preBuff)

    # 1. Determine what's in the preIssueBuff at start of the cycle to get initial value ( numInIssueAtClockCycleBegin)
    # 2. Process instructions in preIssueBuff in 0 .. 3 order. Look for hazards of all types between mostly adjacent instructions.
    # while( numIssued < 2 and numInPreIssueBuff > 0 and curr < 4 ): # curr is current pre issue element - means you are int he queue
    # 2.1 Start with curr = preBuff [0]
    # 2.2 Check for room in the preMemBuff and preALUBuff
    #if sim.isMemOp( index ) and not -1 in sim.preMemBuff:
    # ..... ..... .....
    #
    # 2.3 Do WAR hazard check  - I am dropping this requirement

    #
    # War Check -- later instruction tried to read an operand before earlier instruction writes it
    # WAR Hazard is uncommon/impossible in a reasonable(in-order) pipeline but lets check first
    # We will chech each preIssuebuf entry against other preIssueBuff entries that are 'leftover' during processing
    # and against preMEM and preALU. IF the destination of the current instruction is equal to either source of a
    # previous instruction this is a hazard

    # first check against other preIssue. A little different thinking here. Start with curr = 0 which skips the
    # following check. If the isntruction has an issue then the next pass it will be checked against the 'current' instruction
    # not sure of how else to do this
    if curr > 0:
        for i in range(0, curr):
            if dest[index] == Sim.src1[preBuff[i]] or Sim.dest[index] == sim.src2[preBuff[i]]:
                # found WAR in Issue buffer
                issueMe = False
                break

    # next against preMem
    if Sim.isMemOp(index):
        for i in range(0, len(preBuff)):
            if preBuff[i] != -1:
                if dest[index] == src1[preBuff[i]] or dest[index] == src2[preBuff[i]]:
                    # found WAR in pre issue buff
                    issueMe = False
                    break
     finally against preAlu
    if not Sim.isMemOp(index):
        for i in range(0, len(preAlu)):
            if preAlu[i] != -1:
                if dest[index] == src1[preBuff[i]] or dest[index] == src2[preBuff[i]]:
                    # found WAR in pre issue buff
                    issueMe = False
                    break

# TODO: finish this one
class Cache:
    # 4 sets of two blocks -- 2 words / block
    # [ valid, dirty, tag, data, data ]
    cacheSets = [ [ [0,0,0,0,0], [0,0,0,0,0] ], [ [0,0,0,0,0], [0,0,0,0,0] ], [ [0,0,0,0,0], [0,0,0,0,0] ], [ [0,0,0,0,0], [0,0,0,0,0] ] ]
    lruBit = [0, 0, 0, 0]
    tagMask = 4294967264
    setMask = 24
    justMissedList = []
    setNum = (address1 & self.setMask) >> 3
    tag = (address1 & self.tageMask) >> 5
    def accessMem(self, memIndex, instructionIndex, isWriteToMem, dataToWrite):
        # 1. Given this index, calculate the address of the memory location (example 0 -> 96),
        # figure out which block in set (dataword = 0 or 1)
        #       Check if instruction or data and calculate appropriate address
        if(memIndex == -1):
          addressLocal = 96 + (4 * instructionIndex)
        else:
          addressLocal = 96 + (4 * Sim.numInstructions) + (4 * memIndex)

        # 2. Based on address, align address to two word alignment and create addresses for the two words in block
        # (address1 and address2) based on dataword value. Remember, we are enforcing that block 0 is associated with address 96+ n8!
        if address % 8 == 0:
            dataWord = 0 # block 0 was the address
            address1 = address
            address2 = address + 4
            # check for 'alignment'
            # this picks the second word as address so we need to fix it
            # set address1 - block 1 address to address -4
            if address % 8 != 0:
                dataWord = 1 # block 1 was the address
                address1 = address - 4
                address2 = address


        # 3. Get the word value for each address (data1 and data2) from the memory. We are not in cache yet!
        if address1 < 96 + (4 * Sim.numInstructions):
          data1 = Sim.Instructions[Sim.getIndexOfMemAddress(address1,False)]
        else:
          data1 = Sim.memory[Sim.getIndexOfMemAddress(address1,False)] 
        # 4. IF WRITING TO MEM (memIndex != -1 and isWritetoMem ==1)
        #       Overwrite either data1 or data2 with the passed in dataToWrite based on dataword value

        if isWriteToMem and dataWord == 0:
            data1 = dataToWrite
        elif isWriteToMem and dataWord == 1:
            data2 = dataToWrite

        # 5. Decode the cache address from the address for word0 (tag, set)

        # 6. Look in cache and see if the address we are looking for is either one of the blocks.
        # If hit, set assocblock to the block num.
        if(self.cacheSets[setNum][0][0] == 1 and self.cacheSets[setNum][0][2] == tag ):
          hit = True
          assocBlock = 0
        elif self.cacheSets[setNum][1][0] == 1 and self.cacheSets[setNum][1][2] == tag:
          hit = True
          assocblock = 1
        else:
          if(self.justMissedList.count(address1) == 0:
            self.justMissedList.append(address1)
          return [False, 0]
        # 7. If hit and we are writing to mem
        #   update cache blocks dirty bit
        #   recognize that we should only be writing data to cache other than the initial load
        #   return (True, word from requested set/block)
        if ( hit ):
          if hit and isWriteToMem:
            self.cacheSets[setNum][assocblock[1] = 1
            self.IruBit[setNum] = (assocblock + 1) % 2
            self.cacheSets[setNum][assocblock][dataWord +3] = dataToWrite
        # 8. If hit and we are NOT writing to mem
        #   update set LRU bit, return (True, word requested from set / block)
          elif hit:
            set.IruBit[setNum] = (assocblock + 1) % 2
          return[True,self.cacheSets[setNum][assocblock][dataWord + 3]]
        # 9. If miss figure out if this is the initial miss or the second miss
        if address1 in self.justMissedList:
          while(self.justMissedList.count(address1) > 0 ):
            self.justMissedList.remove(address1)
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
            # Lets say that word 0 is the last instruction and word on is the first data element
            # we would only want to update the second word
            # But if lets say we have two data elemeents, then the cache would have two data element and we would write
            # back both even if one was dirty.  This takes care of the boundry condition.
            if (wbAddr >= (sim.numInstructions * 4) + 96):
                sim.memory[sim.getIndexOfMemAddress(wbAddr)] = self.cacheSets[setNum][self.lruBit[setNum]][3]
            if (wbAddr + 4 >= (sim.numInstructions * 4) + 96):
                sim.memory[sim.getIndexOfMemAddress(wbAddr + 4)] = self.cacheSets[setNum][self.lruBit[setNum]][4]

            # now update the cache flag bits
            self.cacheSets[setNum][self.lruBit[setNum]][0] = 1  # valid  we are writing a block
            self.cacheSets[setNum][self.lruBit[setNum]][1] = 0  # reset the dirty bit
            if (isWriteToMem):
                self.cacheSets[setNum][self.lruBit[setNum]][
                    1] = 1  # dirty if is data mem is dirty again, intruction mem never dirty
            # update both words in the actual cache block in set
            self.cacheSets[setNum][self.lruBit[setNum]][2] = tag  # tag
            self.cacheSets[setNum][self.lruBit[setNum]][3] = data1  # data
            self.cacheSets[setNum][self.lruBit[setNum]][4] = data2  # nextData
            self.lruBit[setNum] = (self.lruBit[setNum] + 1) % 2  # set lru to show block is recently used

            # finally
            return [True, self.cacheSets[setNum][(self.lruBit[setNum] + 1) % 2][
                dataWord + 3]]  # dataword was the actual word thatgenerated the hit

            # 11. Then return (TRUE , word requested from cache)
            
            # 12. Only other case is first miss.
            #   Add address to justMissedList, return (False, 0)


class SimClass:

    cycle = 0
    cache = Cache()
    WB = WriteBack()
    ALU = Alu()
    Issue = Issue()
    fetch = InstructionFetch()

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

    def run(self):
        go = True
        while go:
            self.WB.run()
            self.ALU.run()
            self.MEM.run()
            go = self.fetch.run()
            self.printState()
            self.cycle += 1

    def printState(self):
        outFile = open(outputFileName + "_pipeline.txt", 'w')

        # store each results of each cycle in outFile
        print >> outFile, "--------------------"
        print >> outFile, "Cycle:" + str(self.cycle) + "\n"
        # print buffer and queue
        print >> outFile, ("Pre-Issue Buffer: ")
        if preIssue[0] != -1:
            print >> outFile, ("\tEntry 0:" + "\t", preIssue[0])
        else:
            print >> outFile, ("\tEntry 0:" + "\t")
        if preIssue[1] != -1:
            print >> outFile, ("\tEntry 1:" + "\t", preIssue[1])
        else:
            print >> outFile, ("\tEntry 1:" + "\t")
        if preIssue[2] != -1:
            print >> outFile, ("\tEntry 2:" + "\t", preIssue[2])
        else:
            print >> outFile, ("\tEntry 2:" + "\t")
        if preIssue[3] != -1:
            print >> outFile, ("\tEntry 3:" + "\t", preIssue[3])
        else:
            print >> outFile, ("\tEntry 3:" + "\t")
        print >> outFile, ("Pre_ALU Queue:")
        if preAlu[0] != -1:
            print >> outFile, ("\tEntry 0:" + "\t", preAlu[0])
        else:
            print >> outFile, ("\tEntry 0:" + "\t")
        if preAlu[1] != -1:
            print >> outFile, ("\tEntry 1:" + "\t", preAlu[1])
        else:
            print >> outFile, ("\tEntry 1:" + "\t")
        print >> outFile, ("Post_ALU Queue")
        if postAlu[0] != -1:
            print >> outFile, ("\tEntry 0:" + "\t", postAlu[0])
        else:
            print >> outFile, ("\tEntry 0:" + "\t")
        print >> outFile, ("Pre_MEM Queue")
        if preMem[0] != -1:
            print >> outFile, ("\tEntry 0:" + "\t", preMem[0])
        else:
            print >> outFile, ("\tEntry 0:" + "\t")
        if preMem[1] != -1:
            print >> outFile, ("\tEntry 1:" + "\t", preMem[1])
        else:
            print >> outFile, ("\tEntry 1:" + "\t")
        print >> outFile, ("Post_MEM Queue")
        if postMem[0] != -1:
            print >> outFile, ("\tEntry 0:" + "\t", postMem[0])
        else:
            print >> outFile, ("\tEntry 0:" + "\t")
        # print registers
        print >> outFile, "\nregisters:",
        for q in range(len(reg)):
            if q % 8 == 0:
                if q < 10:
                    print >> outFile, "\nr0" + str(q) + ":",
                else:
                    print >> outFile, "\nr" + str(q) + ":",
            print >> outFile, reg[q], "\t",

        # print cache
        print >> outFile, "Cache"
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
                    print >> outFile, ("\n" + str(startAddress + (dataCount * 4)) + ":"),
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

# instantiate classes into objects
disassemble = Dissembler()
disassemble.run()

Sim = SimClass(allInstr, opcode, mem, 0, 96, arg1, arg2, arg3, len(allInstr), dest, src1, src2)
Sim.run()

