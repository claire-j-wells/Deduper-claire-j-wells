#!/usr/bin/env python

#/usr/bin/time -v ./Wells_deduper.py -u STL96.txt -f final_input_sorted.sam -o final_output.sam 

#./Wells_deduper.py -u STL96.txt -f amelia_test_input_sorted.sam -o amelia_test.sam

import argparse
import re 

def get_args():
    parser = argparse.ArgumentParser(description="A script that takes in a sorted SAM file that can be sorted used SAMTOOLS to find PCR duplicates!")
    parser.add_argument("-f", help="input file")#, required= True)
    parser.add_argument("-o", help="output SAM file")#, required = True)
    parser.add_argument("-u",help = "UMI file")# required= True)
    #parser.add_argument("-h",help = "Get Some Help!")#, required= False)
    return parser.parse_args()

args = get_args()
file = args.f #sorted file 1 from blastp output
outfile = args.o #sorted file 2 from blastp output 
umi = args.u #biomart file 1 with gene names, protein ID, etc 
#help = args.h #biomart file 2 with gene names, protein ID, etc 



def grab_umi(curr_umi) -> str:
    '''This function is meant to grab the UMI from the QNAME '''
    curr_umi = curr_umi.split(":")
    grab_umi = curr_umi[-1]
    return(grab_umi)

def strandedness(bitwise_flag:int) -> bool:
     '''This function determines strandedness and returns a bool. 
     If the bool is TRUE, then it is the PLUS strand and FALSE indicates MINUS'''
     #bitwise_flag = int(bitwise_flag)
     if((bitwise_flag & 16) != 16):
         return True
     return False

def positive_strand_soft_clipping(cigar_string,position):
    matches = re.findall(r'(\d+)([A-Z]{1})', cigar_string)
    letter_dict = {'S':0}
    num_letter = matches[0]                 #this is the number you are doing math on
    number = num_letter[0]                  #this is the number you are doing math on
    adjust_letter = num_letter[1] 
    if adjust_letter == "S":
        letter_dict[adjust_letter] = int(number) 
        #print(matches)
        # number = num_letter[0]                  #this is the number you are doing math on
        # adjust_letter = num_letter[1]
        # if adjust_letter == "S":
        #     letter_dict[adjust_letter] = int(number)       #this is the letter indicator
        # #if adjust_letter not in letter_dict:
        #      #continue
    new_plus_pos = int(position) - letter_dict["S"]
    #print(f'the plus pos is:{new_plus_pos}')     
    return(new_plus_pos)

def minus_strand_soft_clipping(cigar_string,position):
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
        #else:
            #letter_dict[adjust_letter] = int(number)
        first_item = False
        #print(letter_dict)
    new_minus_pos =  int(letter_dict["M"]) + int(letter_dict["D"]) + int(letter_dict["S"]) + int(letter_dict["N"]) + int(position) - 1
    #print(f'the minus pos is:{new_minus_pos}')
    return(new_minus_pos)
       
temp_chr = "" #Assign temporary chromosome
temp_UMI = "" #Assign temporary UMI

big_umi_set = set(open(umi, "r").read().split("\n"))
#print(big_umi_set)

#This set contains a tuple of UMI and Adjusted Position 
minus_umi_set = set()
plus_umi_set = set()

#UMI counter 
unknown_UMI = 0
header_lines = 0
unique_reads = 0 
duplicates = 0 
num_reads_chromo = 0 
chr = "1"

with open(file, "r") as file: 
    with open(outfile, "wt") as outfile: 
        for indiv_line in file:
            if indiv_line.startswith("@"):
                header_lines += 1
                outfile.write(indiv_line)
                continue
            indiv_line = indiv_line.strip("\n")
            split_list = indiv_line.split("\t")
            #print(split_list)
            #ASSIGN variables for all the information we need
            temp_chr = split_list[2] 
            #print(f"Value of split_list[1]: {split_list[1]}")                        
            bitwise_flag = int(split_list[1])
            #print(f'the bit is: {bitwise_flag}')
            curr_umi = grab_umi(split_list[0]) 
            #print(f'the curr umi is: {curr_umi}')          
            positive_strand = strandedness(bitwise_flag)
            #print(f'strand is {positive_strand}')
            position = int(split_list[3])
            #print(f'position is {position}')
            cigar_string = split_list[5]
            #print(f'the cigar is: {cigar_string}')

            if curr_umi not in big_umi_set:
                unknown_UMI += 1 
                continue #SKIP! JUMP ONTO NEXT ITERATION
            #print(cigar_string)
                
            if chr != temp_chr:
                #print(chr) 
                #print(temp_chr)
                print(f'{chr}\t{num_reads_chromo}')
                num_reads_chromo = 0    #If the chromosome doesn't match the last chromosome, reset.
                chr = temp_chr
                #print(minus_umi_set)
                #print(temp_chr)
                minus_umi_set = set()
                plus_umi_set = set()
                #print(f'Chromosome {chr}\t{num_reads_chromo}')

            if positive_strand:
                plus_pos = positive_strand_soft_clipping(cigar_string,position)
                #print(plus_pos)
                if (plus_pos, curr_umi) not in plus_umi_set:
                    num_reads_chromo += 1 
                    plus_umi_set.add((plus_pos, curr_umi))
                    #print(plus_umi_set)
                    unique_reads += 1
                    indiv_line = f'{indiv_line}\n'
                    outfile.write(indiv_line)
                else:
                    duplicates += 1 
                    continue #This means it's a dupe because it's already in the set. 
            else:   # positive_strand is False: #negative strand
                minus_pos = minus_strand_soft_clipping(cigar_string,position)
                #print(minus_pos)
                if (minus_pos, curr_umi) not in minus_umi_set:
                    #print(indiv_line)
                    num_reads_chromo += 1
                    minus_umi_set.add((minus_pos, curr_umi))
                    #print(minus_umi_set)
                    unique_reads += 1
                    indiv_line = f'{indiv_line}\n'
                    outfile.write(indiv_line)
                else:
                    #print(indiv_line)
                    duplicates += 1
                    continue #it's a dupe just like the last thing. 

print(f'The number of reads kept: {unique_reads}')
print(f'The number of duplicates: {duplicates}')
print(f'The number of reads tossed with unknown UMIs: {unknown_UMI}')
print(f'The number of header lines was: {header_lines}')
