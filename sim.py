import sys
from team3_project1 import *
#registers
reg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class Simulator:

    def apply_op(self):
        cycle = 1
        pc = 96
        outFile = open(outputFileName + "_sim.txt", 'w')
        for j in range(len(opcode)):
            if opcode[j] == ADD:
                print("")
            elif opcode[j] == SUB:
                print("")
            elif opcode[j] == AND:
                print("")
            elif opcode[j] == ORR:
                print("")
            elif opcode[j] == LSL:
                print("")
            elif opcode[j] == LSR:
                print("")
            elif opcode[j] == ASR:
                print("")
            elif opcode[j] == EOR:
                print("")
            elif opcode[j] in ADDI:
                reg[arg3[j]] = arg2[j] + reg[arg1[j]]
            elif opcode[j] in SUBI:
                print("")
            elif opcode[j] == STUR:
                print("")
            elif opcode[j] == LDUR:
                print("")
            elif opcode[j] in CBZ:
                print("")
            elif opcode[j] in CBNZ:
                print("")
            elif opcode[j] in MOVZ:
                print("")
            elif opcode[j] in MOVK:
                print("")
            elif opcode[j] in B:
                print("")
            elif opcode[j] == BREAK:
                print("")
            print >> outFile, ("====================")
            print >> outFile, ("cycle: " + str(cycle) + " " +  str(pc) + "\t" + opcodeStr[j] + "\t" + arg1Str[j] + arg2Str[j] +
                               arg3Str[j] + "\n")
            print >> outFile, ("registers:\n" + "r00:\t" + str(reg[0:7]) + "\n" + "r08:\t" + str(reg[8:15]) + "\n" + "r16:\t" + str(reg[16:23]) +                                      "\n" + "r24:\t" + str(reg[24:31]) + "\n")
            print >> outFile, ("data:")
            cycle = cycle + 1
            pc = pc + 4
    def run(self):
        self.apply_op()

# get input and output files from command line args
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print inputFileName
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]

simulator = Simulator()
simulator.run()


