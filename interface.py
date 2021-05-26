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
            print('\033[91m'+"Invalid number of input arguments\n"+'\033[0m')
            self.help()
        
        for i in range(1, len(argv)):
            if argv[i] == '-h' or argv[i] == '--help':
                self.help()
            
            elif argv[i] == '-i' or argv[i] == '--interface':
                sequence_a = input("Insert the first sequence: ")
                sequence_b = input("Insert the second sequence: ")
            
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
                        print("Set default values")
                        character = True
                
                    else:
                        print('\033[91m'+"Error: character not recognized"+'\033[0m')

            elif i == 1: # if no option have been used
                if len(sys.argv) == 3:
                    sequence_a = argv[i]
                    sequence_b = argv[i+1]

                    print("LEN"+str(len(sys.argv)))

                elif len(sys.argv) == 6:
                    match = int(argv[i+2])
                    mismatch = int(argv[i+3])
                    gap = int(argv[i+4])
                
                else:
                    print('\033[91m'+"Invalid number of input arguments\n"+'\033[0m')
                    self.help() 
        
        return sequence_a, sequence_b, match, mismatch, gap
    

    def help(self):
        print("\033[1m"+"Usage:"+"\033[0m")
        print("Default Match/Mismatch/Gap: python smith_waterman.py sequence_a sequence_b")
        print("Set Match/Mismatch/Gap: python smith_waterman.py sequence_a sequence_b match mismatch gap\n")
        print("\033[1m"+"Additional options:""\033[0m")
        print("-i --interface: User friendly interface ")
        print("-h --help: Show the manual")
        print("-f --file: ")
        sys.exit()