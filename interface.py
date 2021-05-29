#!/usr/bin/env python

import sys

class Interface:

    
    def start(self):
        sequence_a, sequence_b, match, mismatch, gap = self.check_arguments(argv=sys.argv)
        return sequence_a, sequence_b, match, mismatch, gap

    def check_arguments(self, argv): 
        print("\n")
        print("*********** Smith-Waterman Algorithm ***********\n")
        sequence_a = "AGTAGGA"
        sequence_b = "AGTACCA"
        match = 3
        mismatch = -3
        gap = -2

        if len(sys.argv) < 2:
            print("Invalid number of input arguments\n")
            self.help()
        
        for i in range(1, len(argv)):
            if argv[i] == '-h':
                self.help()
            
            elif argv[i] == '-int' :
                sequence_a = input("Insert the sequence A: ")
                sequence_b = input("Insert the second sequence B: ")
            
                character = False

                while character == False:
                    decision = input("Do you want to insert Match/Mismatch/GAP values? (Default 3,-3,-2) Y/N \n")
                    decision = decision.upper()
            
                    if decision == "Y":
                        match = int(input("Insert match value: "))
                        mismatch = int(input("Insert mismatch value: "))
                        gap = int(input("Insert gap value: "))    
                        character = True       
            
                    elif decision == "N":
                        print("Setting default values")
                        character = True
                
                    else:
                        print("Error: character not recognized")

            elif i == 1: 
                if len(sys.argv) == 3:
                    sequence_a = argv[i]
                    sequence_b = argv[i+1]

                elif len(sys.argv) == 6:
                    match = int(argv[i+2])
                    mismatch = int(argv[i+3])
                    gap = int(argv[i+4])
                
                else:
                    print("Error: Invalid number of input arguments\n")
                    self.help() 
        
        return sequence_a, sequence_b, match, mismatch, gap
    

    def help(self):
        print("Usage:")
        print("Default Match/Mismatch/Gap: python smith_waterman.py sequence_a sequence_b")
        print("Set Match/Mismatch/Gap: python smith_waterman.py sequence_a sequence_b match mismatch gap\n")
        print("Different options:")
        print("Guided interface: python smith_waterman.py -int")
        print("Show the manual: python smith_waterman.py -h\n")   
        sys.exit()