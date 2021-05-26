import numpy as np
import sys
from numpy.lib.utils import safe_eval
import pandas as pd


class SmithWaterman:

    def __init__(self, sequence_a, sequence_b, match, mismatch, gap):
        
        #initialize standard smith-waterman variables
        self.sequence_a = sequence_a
        self.sequence_b = sequence_b
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

        #initialize scoring matrix with the length of the two sequences + 1
        #for the 0s lines
        self.scoring_matrix = np.zeros((len(sequence_a)+ 1, len(sequence_b) + 1,)) 
        
        #initialize maximum score, and their coordinates
        self.score = 0
        self.max_rows_score = []
        self.max_columns_score = []

        #initialize lists to save alignments
        self.sequence_a_alignments = []
        self.sequence_b_alignments = []

      

    
    def execute(self):

        self.build_scoring_matrix()
        self.find_top_score()
        self.find_all_different_alignments()
        self.print_result()       


    def build_scoring_matrix(self):
	   
        #NOTE: Build scoring matrix using the maximum value calculated: 
        # tmp_m => adding match or mismatch depending on the equality 
        #          of the 2 letters on the previous diagonal score
        # gap_left => adding gap to the left value
        # gap_top => adding gap to the top value

	    for i in range(1, len(self.sequence_a) + 1):	
		    for j in range(1, len(self.sequence_b) + 1):	
			    tmp_m = 0; 		
			    a = self.sequence_a[i-1] 
			    b = self.sequence_b[j-1] 
			    if(a == b): 
				    tmp_m = self.match + self.scoring_matrix[i-1, j-1]	
			    else:  
				    tmp_m = self.mismatch + self.scoring_matrix[i-1, j-1]	
		
			    gap_left = self.gap + self.scoring_matrix[i-1, j] 
			    gap_top = self.gap + self.scoring_matrix[i, j-1] 

			    self.scoring_matrix[i, j] = max(tmp_m, gap_left, gap_top, 0)


    def find_top_score(self):

        #NOTE: find the maximum scores inside the matrix
        #and their coordinates using numpy functions

        self.score = np.amax(self.scoring_matrix)
    
        if self.score == 0:    
            sys.exit("Maximum score = 0 : no possible alignmets") 

        self.max_rows_score, self.max_columns_score = np.where(self.scoring_matrix == self.score)

        if (not self.max_rows_score[0]):
            self.max_rows_score = [self.max_rows_score,]
        if (not self.max_columns_score[0]):
            self.max_columns_score = [self.max_columns_score,]

  
    def traceback(self, i, j ,  partial_alignment_a=[""], partial_alignment_b=[""]):

        #NOTE: Finds recursively all the possible alignments, 
        #starting from top score coordinates i, j, passing 
        #everytime the two partial alignments and updated with
        #the right letter
        

        if self.scoring_matrix[i,j] == 0:
            return partial_alignment_a,partial_alignment_b
        else:
            all_alignments1, all_alignments2 = [],[]
            tmp_list1, tmp_list2 = [],[]

            if (self.sequence_a[i-1] == self.sequence_b[j-1]):
                diagonal_score = self.scoring_matrix[i-1,j-1] + self.match 
            
            else:
                diagonal_score = self.scoring_matrix[i-1,j-1] + self.mismatch


            if (self.scoring_matrix[i,j]==diagonal_score):
                
                pa_a, pa_b = partial_alignment_a.copy(), partial_alignment_b.copy()
                pa_a[0] = self.sequence_a[i-1] + pa_a[0]
                pa_b[0] = self.sequence_b[j-1] + pa_b[0]
                tmp_list1, tmp_list2 = self.traceback(i-1, j-1, pa_a, pa_b)
                all_alignments1, all_alignments2 = all_alignments1+tmp_list1, all_alignments2+tmp_list2

            if self.scoring_matrix[i, j-1] + self.gap == self.scoring_matrix[i, j]: # gap left       
                
                pa_a,pa_b = partial_alignment_a.copy(), partial_alignment_b.copy()
                pa_a[0] = "-" + pa_a[0]
                pa_b[0] = self.sequence_b[j-1] + pa_b[0]
                tmp_list1, tmp_list2 = self.traceback(i,j-1, pa_a, pa_b)
                all_alignments1, all_alignments2 = all_alignments1+tmp_list1, all_alignments2+tmp_list2

            if self.scoring_matrix[i-1, j] + self.gap == self.scoring_matrix[i, j]: # gap top
                
                pa_a,pa_b = partial_alignment_a.copy(), partial_alignment_b.copy()
                pa_a[0] = self.sequence_a[i-1] + pa_a[0]
                pa_b[0] = "-" + pa_b[0]
                tmp_list1, tmp_list2 = self.traceback(i-1,j, pa_a, pa_b)
                all_alignments1, all_alignments2 = all_alignments1+tmp_list1, all_alignments2+tmp_list2
        
            return all_alignments1, all_alignments2 


    def find_all_different_alignments(self):

        #NOTE: For all the top scores coordinates do the traceback

         for i in range(len(self.max_rows_score)):
            alignments1, alignments2 = self.traceback(i = self.max_rows_score[i], j = self.max_columns_score[i])
            self.sequence_a_alignments = self.sequence_a_alignments + alignments1
            self.sequence_b_alignments = self.sequence_b_alignments + alignments2        


    def print_result(self):

        print("\n")
        print("\033[1m"+"SCORING MATRIX:"+"\033[0m")
        print("\n")
        index = " "+self.sequence_a
        columns = " "+self.sequence_b
        matrix = pd.DataFrame(self.scoring_matrix, columns=[c for c in columns], index=[i for i in index] )
        matrix=matrix.astype(int)
        print(matrix)
        print("\n")
        print("\033[1m"+"Results:"+"\033[0m")
        print("Top score is: "+str(int(self.score)))
        print("There are ",len(self.sequence_a_alignments), " different alignments\n")
        

        for i in range(len(self.sequence_a_alignments)):
            print("\033[1m"+"Alignment " + str(i+1) + ":"+"\033[0m")
            n_match, n_mismatch, n_gap_seq_a, n_gap_seq_b = self.statistics(self.sequence_a_alignments[i], self.sequence_b_alignments[i])
            print("Match: "+str(n_match))
            print("Mismatch: "+str(n_mismatch))
            print("Gap sequence A: "+str(n_gap_seq_a))
            print("Gap sequence B: "+str(n_gap_seq_b)+"\n")
            print("\033[1m"+self.sequence_a_alignments[i]+"\033[0m")
            print("\033[1m"+self.sequence_b_alignments[i]+"\033[0m") 
            print("\n")


    def statistics(self, a,b):
        n_mismatch = 0
        n_gap_seq_a = a.count("-")
        n_gap_seq_b = b.count("-")
        n_match = 0

        for i in range(len(a)):
            if (a[i] != b[i]):
                if (a[i]=="-" or b[i]=="-"):
                    pass
                else:
                    n_mismatch += 1
            else:
                n_match += 1

        return n_match, n_mismatch, n_gap_seq_a, n_gap_seq_b