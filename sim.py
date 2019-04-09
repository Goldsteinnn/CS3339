import sys
from team3_project1 import *
#registers
reg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class Simulator:

    def print_sim(self):
        i = 0 #Iterates through opcode
        cycle = 1
        pc = 96

        outFile = open(outputFileName + "_sim.txt", 'w')
        while opcodeStr[i] != "BREAK":
            print >> outFile, ("====================")
            print >> outFile, ("cycle: " + str(cycle) + " " +  str(pc) + "\t" + opcodeStr[i] + "\t" + arg1Str[i] + arg2Str[i] +
                               arg3Str[i] + "\n")
            print >> outFile, ("registers:\n" + "r00:\t" + str(reg[0:7]) + "\n" + "r08:\t" + str(reg[8:15]) + "\n" + "r16:\t" + str(reg[16:23]) +                                      "\n" + "r24:\t" + str(reg[24:31]) + "\n")
            print >> outFile, ("data:")
            i = i + 1
            cycle = cycle + 1

    def run(self):
        self.print_sim()

# get input and output files from command line args
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        inputFileName = sys.argv[i + 1]
        print inputFileName
    elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        outputFileName = sys.argv[i + 1]

simulator = Simulator()
simulator.run()



