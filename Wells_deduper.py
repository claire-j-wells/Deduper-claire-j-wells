#!/usr/bin/env python

#FINAL COMMAND USED: 
#/usr/bin/time -v ./Wells_deduper.py -u STL96.txt -f final_input_sorted.sam -o final_output.sam 

#IMPORT TOOLS
import argparse
import re 

def get_args():
    parser = argparse.ArgumentParser(description="A script that takes in a sorted SAM file that can be sorted used SAMTOOLS to find PCR duplicates!")
    parser.add_argument("-f", help="input file")#, required= True)
    parser.add_argument("-o", help="output SAM file")#, required = True)
    parser.add_argument("-u",help = "UMI file")# required= True)
    return parser.parse_args()

args = get_args()
file = args.f #sorted file 1 from blastp output
outfile = args.o #sorted file 2 from blastp output 
umi = args.u #biomart file 1 with gene names, protein ID, etc 
#help = args.h #biomart file 2 with gene names, protein ID, etc 


#FUNCTIONS :) 

def grab_umi(curr_umi) -> str:
    '''This function is meant to grab the UMI from the QNAME '''
    curr_umi = curr_umi.split(":")
    grab_umi = curr_umi[-1]
    return(grab_umi)

def strandedness(bitwise_flag:int) -> bool:
     '''This function determines strandedness and returns a bool. 
     If the bool is TRUE, then it is the PLUS strand and FALSE indicates MINUS'''
     if((bitwise_flag & 16) != 16):
         return True
     return False

def positive_strand_soft_clipping(cigar_string,position):
    '''This function calculates soft clipping on positive strands'''
    matches = re.findall(r'(\d+)([A-Z]{1})', cigar_string)
    letter_dict = {'S':0}
    num_letter = matches[0]                 #this is the number you are doing math on
    number = num_letter[0]                  #this is the number you are doing math on
    adjust_letter = num_letter[1] 
    if adjust_letter == "S":
        letter_dict[adjust_letter] = int(number) 
    new_plus_pos = int(position) - letter_dict["S"]
    #print(f'the plus pos is:{new_plus_pos}')     
    return(new_plus_pos)

def minus_strand_soft_clipping(cigar_string,position):
    '''This function calculates soft clipping on the minus strand'''
    matches = re.findall(r'(\d+)([A-Z]{1})', cigar_string)
    letter_dict = {'M':0,
                   'D':0,
                   'S':0,
                   'N':0}
    first_item = True
    for num_letter in matches:
        number = int(num_letter[0])                   #this is the number you are doing math on
        adjust_letter = num_letter[1]
        if adjust_letter == "S" :
            if not first_item:
                letter_dict[adjust_letter] = int(number)
        elif adjust_letter in letter_dict:
            letter_dict[adjust_letter] += int(number)          
        first_item = False
    new_minus_pos =  int(letter_dict["M"]) + int(letter_dict["D"]) + int(letter_dict["S"]) + int(letter_dict["N"]) + int(position) - 1
    return(new_minus_pos)

#SET UP TEMP VAR        
temp_chr = "" #Assign temporary chromosome
temp_UMI = "" #Assign temporary UMI

#OPEN BIG UMI SET TO COMPARE TO 
big_umi_set = set(open(umi, "r").read().split("\n"))

#This set contains a tuple of UMI,Adjusted Position 
minus_umi_set = set()
plus_umi_set = set()

#ALL THE COUNTERS!
unknown_UMI = 0
header_lines = 0
unique_reads = 0 
duplicates = 0 
num_reads_chromo = 0 

#SET CHR EQUAL TO 1 FOR FIRST ITERATION UNDER THE ASSUMPTION OF RECEIVING A SORTED SAM FILE 
chr = "1"

#START: 
with open(file, "r") as file: 
    with open(outfile, "wt") as outfile: 
        for indiv_line in file:
            if indiv_line.startswith("@"):
                header_lines += 1
                outfile.write(indiv_line)
                continue
            indiv_line = indiv_line.strip("\n")
            split_list = indiv_line.split("\t")
        
            #ASSIGN VAR AND GET ALL THE INFORMATION NECESSARY 
            temp_chr = split_list[2]                  
            bitwise_flag = int(split_list[1])
            curr_umi = grab_umi(split_list[0])           
            positive_strand = strandedness(bitwise_flag)
            position = int(split_list[3])
            cigar_string = split_list[5]

            if curr_umi not in big_umi_set:
                unknown_UMI += 1 
                continue #SKIP! JUMP ONTO NEXT ITERATION
    
                
            if chr != temp_chr:
                print(f'{chr}\t{num_reads_chromo}')

                #If the chromosome doesn't match the last chromosome, reset for counting purposes and move to the next chr. 
                num_reads_chromo = 0    
                chr = temp_chr

                #CLEAR THE SETS
                minus_umi_set = set()
                plus_umi_set = set()

            if positive_strand:
                plus_pos = positive_strand_soft_clipping(cigar_string,position)
                if (plus_pos, curr_umi) not in plus_umi_set:
                    num_reads_chromo += 1 
                    plus_umi_set.add((plus_pos, curr_umi))
                    unique_reads += 1
                    indiv_line = f'{indiv_line}\n'
                    outfile.write(indiv_line)
                else:
                    duplicates += 1 
                    continue #This means it's a dupe because it's already in the set. 
            else:   # positive_strand is False: #negative strand
                minus_pos = minus_strand_soft_clipping(cigar_string,position)
                if (minus_pos, curr_umi) not in minus_umi_set:
                    num_reads_chromo += 1
                    minus_umi_set.add((minus_pos, curr_umi))
                    unique_reads += 1
                    indiv_line = f'{indiv_line}\n'
                    outfile.write(indiv_line)
                else:
                    duplicates += 1
                    continue #it's a dupe just like the last thing. 

print(f'The number of reads kept: {unique_reads}')
print(f'The number of duplicates: {duplicates}')
print(f'The number of reads tossed with unknown UMIs: {unknown_UMI}')
print(f'The number of header lines was: {header_lines}')
