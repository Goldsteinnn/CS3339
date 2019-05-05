from team3_project1 import *
# registers
reg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data = []
preIssue = ["here","","",""]
preAlu = ["",""]
postAlu = [""]
preMem = ["",""]
postMem = [""]

class Simulator:

    def apply_op(self):
        cycle = 1
        pc = 96
        j = 0
        outFile = open(outputFileName + "_sim.txt", 'w')

        # determine starting data address
        startAddress = 96 + (4 * len(opcode))   # PC at break + 4
        # populate initial data
        self.afterBreak()

        # perform instructions
        while j < len(allInstr):
            if opcode[j] == ADD:
                reg[arg3[j]] = reg[arg2[j]] + reg[arg1[j]]

            elif opcode[j] == SUB:
                reg[arg3[j]] = reg[arg1[j]] - reg[arg2[j]]

            elif opcode[j] == AND:
                reg[arg3[j]] = reg[arg2[j]] & reg[arg1[j]]

            elif opcode[j] == ORR:
                reg[arg3[j]] = reg[arg2[j]] | reg[arg1[j]]

            elif opcode[j] == LSL:
                reg[arg3[j]] = reg[arg1[j]] << arg2[j]

            elif opcode[j] == LSR:
                reg[arg3[j]] = reg[arg1[j]] % 0x100000000 >> arg2[j]

            elif opcode[j] == ASR:
                reg[arg3[j]] = reg[arg1[j]] / (2 ** arg2[j])

            elif opcode[j] == EOR:
                reg[arg3[j]] = reg[arg2[j]] ^ reg[arg1[j]]

            elif opcode[j] in ADDI:
                reg[arg3[j]] = arg2[j] + reg[arg1[j]]

            elif opcode[j] in SUBI:
                reg[arg3[j]] = reg[arg1[j]] - arg2[j]

            elif opcode[j] == STUR:
                if len(data) < ((((4*arg2[j]) + reg[arg1[j]]) - startAddress)/4):
                    # add 0s until correct block
                    for k in range((((4*arg2[j]) + reg[arg1[j]]) - startAddress)/4 - dataCount):
                        data.append(0)
                    # add value in correct spot
                    data.append(reg[arg3[j]])
                    # finish the row out with 0s
                    k = ((((4*arg2[j]) + reg[arg1[j]]) - startAddress)/4) + 1
                    while k % 8 != 0:
                        data.append(0)
                        k += 1

                else:
                    data[reg[arg2[j]]+arg1[j]] = reg[arg3[j]]

            elif opcode[j] == LDUR:
                # load nothing if there's no data
                if not data:
                    reg[arg3[j]] = 0
                # if start register = 0, only count offset
                if reg[arg1[j]] == 0:
                    reg[arg3[j]] = data[arg2[j]-startAddress+4]
                else:
                    try:
                        reg[arg3[j]] = data[((arg2[j]) + (reg[arg1[j]] - startAddress)) / 4 + 1]
                    except IndexError:
                        # load nothing if data location is empty (out of range)
                        reg[arg3[j]] = 0
                    #reg[arg3[j]] = data[((arg2[j]) + (reg[arg1[j]] - startAddress)) / 4 + 1]

            elif opcode[j] in MOVZ:
                isBlank = (arg2[j] == "")
                if isBlank:
                    reg[arg3[j]] = arg1[j]
                else:
                    reg[arg3[j]] = arg1[j] << (arg2[j]*16)

            elif opcode[j] in MOVK:
                reg[arg3[j]] += arg1[j] << (arg2[j]*16)

            #elif opcode[j] == BREAK:

            # store each results of each cycle in outFile
            print >> outFile, ("=====================\n")
            print >> outFile, ("cycle: " + str(cycle) + ":")
            # print buffer and queue
            print >> outFile, ("Pre-Issue Buffer: ")
            print >> outFile, ("\tEntry 0" + "\t" + preIssue[0])
            print >> outFile, ("\tEntry 1" + "\t" + preIssue[1])
            print >> outFile, ("\tEntry 2" + "\t" + preIssue[2])
            print >> outFile, ("\tEntry 3" + "\t" + preIssue[3])
            print >> outFile, ("Pre_ALU Queue:")
            print >> outFile, ("\tEntry 0" + "\t" + preAlu[0])
            print >> outFile, ("\tEntry 1" + "\t" + preAlu[1])
            print >> outFile, ("Post_ALU Queue")
            print >> outFile, ("\tEntry 0" + "\t" + postAlu[0])
            print >> outFile, ("Pre_MEM Queue")
            print >> outFile, ("\tEntry 0" + "\t" + preMem[0])
            print >> outFile, ("\tEntry 1" + "\t" + preMem[1])
            print >> outFile, ("Post_MEM Queue")
            print >> outFile, ("\tEntry 0" + "\t" + postMem[0])
            postMem[0] = preMem[0]
            preMem[0] = ""
            preMem[0] = preMem[1]
            preMem[1] = ""
            preMem[1] = postAlu[0]
            postAlu[0] = ""
            postAlu[0] = preAlu[0]
            preAlu[0] = ""
            preAlu[0] = preAlu[1]
            preAlu[1] = ""
            preAlu[1] = preIssue[0]
            preIssue[0] = ""
            preIssue[0] = preIssue[1]
            preIssue[0] = ""
            preIssue[1] = preIssue[2]
            preIssue[2] = ""
            preIssue[2] = preIssue[3]
            preIssue[3] = ""
            # print registers
            print >> outFile, "\nregisters:",
            for q in range(len(reg)):
                if q % 8 == 0:
                    if q < 10:
                        print >> outFile, "\nr0" + str(q) + ":",
                    else:
                        print >> outFile, "\nr" + str(q) + ":",
                print >> outFile, reg[q], "\t",
            print >> outFile, ("\n\ndata:"),

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

            # check branch instructions
            if opcode[j] in B:
                pc += 4 * int(arg3[j])
                j += int(arg3[j]-1)

            elif opcode[j] in CBZ:
                if reg[arg3[j]] == 0:
                    pc += 4 * int(arg1[j])
                    j += int(arg1[j] - 1)
                else:
                    pc += 4

            elif opcode[j] in CBNZ:
                if reg[arg3[j]] != 0:
                    pc += 4 * int(arg1[j])
                    j += int(arg1[j]-1)
                else:
                    pc += 4
            else:
                pc += 4
            cycle += 1
            j += 1

    # reads all the data after the break and applies it to the data section
    def afterBreak(self):
        if not data:
            for f in range(len(binMem)):
                data.append(twos_comp(binMem[f], 32))

    def run(self):
        self.apply_op()
        self.afterBreak();

# get input and output files from command line args
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print inputFileName
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]

# returns twos complement value of passed number
def twos_comp(val, bits):
     if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits) # compute negative value
        return val   # return positive value as is

simulator = Simulator()
simulator.run()
