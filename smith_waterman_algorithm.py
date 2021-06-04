#!/usr/bin/env python

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
        
        #initialize maximum score, and its coordinates
        self.score = 0
        self.max_rows_score = []
        self.max_columns_score = []

        #initialize lists to save final alignments
        self.sequence_a_alignments = []
        self.sequence_b_alignments = []

    
    def execute(self):

        self.build_scoring_matrix()
        self.find_top_score()
        self.find_all_different_alignments()
        self.print_result()       


    def build_scoring_matrix(self):
	   
        # NOTE: Build scoring matrix using the maximum value calculated: 
        # tmp_m => calculated adding match or mismatch on the previous 
        #          diagonal score value depending on the equality of the 
        #          2 letters, 
        # gap_left => calculated adding gap to the left value
        # gap_top => calculated adding gap to the top value
        # assign to the actual cell the maximum between this 3 values

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

        # NOTE: find the maximum scores inside the matrix
        # and their coordinates using numpy functions

        self.score = np.amax(self.scoring_matrix)
    
        if self.score == 0:    
            sys.exit("Maximum score = 0 : no possible alignmets\n") 

        self.max_rows_score, self.max_columns_score = np.where(self.scoring_matrix == self.score)


          
    def traceback(self, i, j ,  partial_alignment_a=[""], partial_alignment_b=[""]):

        # NOTE: Finds recursively all the possible alignments, 
        # starting from top score coordinates i j, passing 
        # everytime the two partial alignments and updating them 
        # with the right letters, based on the values given by the
        # scoring matrix, using a string concatenation. Finally 
        # save them in two list where there are all the possible paths,
        # if more than one
        

        if self.scoring_matrix[i,j] == 0:
            return partial_alignment_a,partial_alignment_b
        else:
            total_alignments_a, total_alignments_b = [],[]
            tmp_al_a, tmp_al_b = [],[]

        
        
            if (self.sequence_a[i-1] == self.sequence_b[j-1]):
                diagonal_score = self.scoring_matrix[i-1,j-1] + self.match   
            else:
                diagonal_score = self.scoring_matrix[i-1,j-1] + self.mismatch

        # adding a match or mismatch pair on partial alignments
        # if the current value of matrix is equal to upper diagonal 
        # value plus match or mismatch

            if (self.scoring_matrix[i,j]==diagonal_score):
                pa_a, pa_b = partial_alignment_a.copy(), partial_alignment_b.copy()
                pa_a[0] = self.sequence_a[i-1] + pa_a[0]
                pa_b[0] = self.sequence_b[j-1] + pa_b[0]
                tmp_al_a, tmp_al_b  = self.traceback(i-1, j-1, pa_a, pa_b)
                total_alignments_a, total_alignments_b = total_alignments_a+tmp_al_a, total_alignments_b+tmp_al_b
        
        # adding gap on partial sequence a if the current value of matrix
        # is equal to the left value plus the gap

            if self.scoring_matrix[i, j-1] + self.gap == self.scoring_matrix[i, j]:          
                pa_a,pa_b = partial_alignment_a.copy(), partial_alignment_b.copy()
                pa_a[0] = "-" + pa_a[0]
                pa_b[0] = self.sequence_b[j-1] + pa_b[0]
                tmp_al_a, tmp_al_b  = self.traceback(i,j-1, pa_a, pa_b)
                total_alignments_a, total_alignments_b = total_alignments_a+tmp_al_a, total_alignments_b+tmp_al_b
        
        # adding gap on partial sequence b if the current value of matrix
        # is equal to the upper value

            if self.scoring_matrix[i-1, j] + self.gap == self.scoring_matrix[i, j]:    
                pa_a,pa_b = partial_alignment_a.copy(), partial_alignment_b.copy()
                pa_a[0] = self.sequence_a[i-1] + pa_a[0]
                pa_b[0] = "-" + pa_b[0]
                tmp_al_a, tmp_al_b  = self.traceback(i-1,j, pa_a, pa_b)
                total_alignments_a, total_alignments_b = total_alignments_a+tmp_al_a, total_alignments_b+tmp_al_b
        
            return total_alignments_a, total_alignments_b 


    def find_all_different_alignments(self):

        # NOTE: For all the top scores coordinates do the traceback 
        # to find the different local alignments

         for i in range(len(self.max_rows_score)):
            alignments1, alignments2 = self.traceback(i = self.max_rows_score[i], j = self.max_columns_score[i])
            self.sequence_a_alignments = self.sequence_a_alignments + alignments1
            self.sequence_b_alignments = self.sequence_b_alignments + alignments2        


    def print_result(self):

        print("\n")
        print("SCORING MATRIX:")
        print("\n")
        index = " "+self.sequence_a
        columns = " "+self.sequence_b
        matrix = pd.DataFrame(self.scoring_matrix, columns=[c for c in columns], index=[i for i in index] )
        matrix=matrix.astype(int)
        print(matrix)
        print("\n")
        print("Results:")
        print("Top score is: "+str(int(self.score)))
        print("There are ",len(self.sequence_a_alignments), " different alignments\n")
        

        for i in range(len(self.sequence_a_alignments)):
            n_match, n_mismatch, n_gap_seq_a, n_gap_seq_b, total_gaps, len_alignmet = \
                self.statistics(self.sequence_a_alignments[i], self.sequence_b_alignments[i])

            print("Alignment " + str(i+1) + ", length ("+str(len_alignmet)+"):")
            print("Match: "+str(n_match))
            print("Mismatch: "+str(n_mismatch))
            print("Total gaps: "+str(total_gaps))
            print("Gap sequence A: "+str(n_gap_seq_a))
            print("Gap sequence B: "+str(n_gap_seq_b)+"\n")
            print(self.sequence_a_alignments[i])
            print(self.sequence_b_alignments[i]) 
            print("\n")


    def statistics(self, a,b):
        # NOTE: Some statistics like number of 
        # mismatch, match, gaps, length of the
        # alignment

        len_alingment = len(a)
        n_mismatch = 0
        n_gap_seq_a = a.count("-")
        n_gap_seq_b = b.count("-")
        total_gaps = n_gap_seq_a + n_gap_seq_b
        n_match = 0

        for i in range(len(a)):
            if (a[i] != b[i]):
                if (a[i]=="-" or b[i]=="-"):
                    pass
                else:
                    n_mismatch += 1
            else:
                n_match += 1

        return n_match, n_mismatch, n_gap_seq_a, n_gap_seq_b, total_gaps, len_alingment