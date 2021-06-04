#!/usr/bin/env python

import sys

class Interface:

    #start the interface and initialize smith-waterman variables
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

        #minimum number of arguments
        if len(sys.argv) < 2:
            print("Invalid number of input arguments\n")
            self.help()
        
        for i in range(1, len(argv)):

            #help menu
            if argv[i] == '--help':
                self.help()
            
            #guided interface
            elif argv[i] == '--interface' :
                sequence_a = input("Insert the sequence A: ")
                sequence_b = input("Insert the second sequence B: ")
            
                character = False

                while character == False:
                    decision = input("Do you want to insert Match/Mismatch/GAP values? (Default 3,-3,-2) Y/N \n")
                    decision = decision.upper()
            
                    if decision == "Y":
                        match = self.isValid("Insert match value: ")
                        mismatch = self.isValid("Insert mismatch value: ")
                        gap = self.isValid("Insert gap value: ")
                        character = True       
            
                    elif decision == "N":
                        print("Setting default values")
                        character = True
                
                    else:
                        print("Error: character not recognized")

            #arguments: 
            #args = 2 only the two sequences with default values
            #args = 5 set the match, mismatch, gap values
            elif i == 1: 
                if len(sys.argv) == 3:
                    sequence_a = argv[i]
                    sequence_b = argv[i+1]

                elif len(sys.argv) == 6:
                    sequence_a = argv[i]
                    sequence_b = argv[i+1]
                    try:
                        match = int(argv[i+2])
                        mismatch = int(argv[i+3])
                        gap = int(argv[i+4])
                    except ValueError:
                        print("Error: Match, Mismatch or GAP are not numbers\n")
                        sys.exit()
                
                else:
                    print("Error: Invalid number of input arguments\n")
                    self.help() 
        
        return sequence_a, sequence_b, match, mismatch, gap

    
    #check in the guided interface if the match, mismatch and gap are numbers
    def isValid(self, message):
        error = True
        while error:
            value = input(message)
            try:
                val = int(value)
                return val
            except ValueError:
                print("Error: Enter a valid value")
        


    def help(self):
        print("Usage:")
        print("Default Match/Mismatch/Gap: python smith_waterman.py sequence_a sequence_b")
        print("Set Match/Mismatch/Gap: python smith_waterman.py sequence_a sequence_b match mismatch gap\n")
        print("Different options:")
        print("Guided interface: python smith_waterman.py --interface")
        print("Show the manual: python smith_waterman.py --help\n")   
        sys.exit()