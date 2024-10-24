#!/usr/bin/env python

#import argparse
import re 

# def get_args():
#     parser = argparse.ArgumentParser(description="A program to introduce yourself")
#     parser.add_argument("-f", help="input file", required= True)
#     parser.add_argument("-o", help="output SAM file", required = True)
#     parser.add_argument("u",help = "UMI file", required= True)
#     parser.add_argument("-h",help = "Get Some Help!", required= True)
#     return parser.parse_args()

# args = get_args()
# file = args.f #sorted file 1 from blastp output
# outfile = args.o #sorted file 2 from blastp output 
# umi = args.u #biomart file 1 with gene names, protein ID, etc 
# help = args.h #biomart file 2 with gene names, protein ID, etc 

temp_chr = "" #Assign temporary chromosome
temp_UMI = "" #Assign temporary UMI

big_umi_set = set(open("STL96.txt", "r").read().split("\n"))
minus_umi_set = set()
plus_umi_set = set()


def grab_umi(curr_umi) -> str:
    '''This function is meant to grab the UMI from the QNAME '''
    curr_umi = curr_umi.split(":")
    print(curr_umi)
    grab_umi = curr_umi[-1]
    return(grab_umi)

def strandedness(bitwise_flag:int) -> bool:
     '''This function determines strandedness and returns a bool. 
     If the bool is TRUE, then it is the PLUS strand and FALSE indicates MINUS'''
     if((bitwise_flag & 4) != 4):
         return False
     return True

def positive_strand_soft_clipping(cigar_string):
     
          
          
          
          

     
def minus_strand_soft_clipping(cigar_string):
     

with open("test.sam", "r") as file: #open(outfile, "w") as outfile: 
    for indiv_line in file:
        if indiv_line.startswith("@"):
            #outfile.write(indiv_line)
            continue
        indiv_line = indiv_line.strip("\n")
        split_list = indiv_line.split("\t")
        chr = split_list[2]                         #Assign current chromosome
        bitwise_flag = int(split_list[1])
        curr_umi = grab_umi(split_list[0])           #Grabbing the UMI   
        positive_strand = strandedness(bitwise_flag)
        cigar_string = split_list[5]             
        if chr != temp_chr:                         #If the chromosome doesn't match the last chromosome, reset.
            chr = temp_chr
        if positive_strand is True:
            #soft clipping bullshit
                pass #to make pylance not shit itself 
        elif positive_strand is False: #negative strand 
             #more soft clipping bullshit

                

                                                    

                
            
                


