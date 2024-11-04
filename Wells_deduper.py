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




def grab_umi(curr_umi) -> str:
    '''This function is meant to grab the UMI from the QNAME '''
    curr_umi = curr_umi.split(":")
    grab_umi = curr_umi[-1]
    return(grab_umi)

def strandedness(bitwise_flag:int) -> bool:
     '''This function determines strandedness and returns a bool. 
     If the bool is TRUE, then it is the PLUS strand and FALSE indicates MINUS'''
     if((bitwise_flag & 16) != 16):
         return False
     return True

def positive_strand_soft_clipping(cigar_string):
    matches = re.findall(r'(\d+)([A-Z]{1})', cigar_string)
    letter_dict = {} 
    for num_letter in matches:
        #print(matches)
        number = num_letter[0]                  #this is the number you are doing math on
        adjust_letter = num_letter[1]
        if adjust_letter == "S":
            letter_dict[adjust_letter] = int(number)       #this is the letter indicator
        if adjust_letter in letter_dict:
             continue
        new_plus_pos = int(position) - letter_dict["S"]
        #print(new_plus_pos)     
    return(positive_strand_soft_clipping)

def minus_strand_soft_clipping(cigar_string):
    matches = re.findall(r'(\d+)([A-Z]{1})', cigar_string)
    letter_dict = {'M':0,
                   'D':0,
                   'S':0,
                   'N':0}
    for num_letter in matches:
        print(num_letter)
        number = num_letter[0]                   #this is the number you are doing math on
        adjust_letter = num_letter[1]
        if adjust_letter == "S":
            letter_dict[adjust_letter] = int(number)
        elif adjust_letter in letter_dict:
            letter_dict[adjust_letter] += int(number)          
        else:
            letter_dict[adjust_letter] = int(number)
        print(letter_dict)
    new_minus_pos =  int(letter_dict["M"]) + int(letter_dict["D"]) + int(letter_dict["S"]) + int(letter_dict["N"]) + int(position) - 1
    #print(new_minus_pos)
    return(minus_strand_soft_clipping)
       
temp_chr = "" #Assign temporary chromosome
temp_UMI = "" #Assign temporary UMI

big_umi_set = set(open("STL96.txt", "r").read().split("\n"))
minus_umi_set = set()
plus_umi_set = set()


with open("small_test.sam", "r") as file: #open(outfile, "w") as outfile: 
    for indiv_line in file:
        if indiv_line.startswith("@"):
            #outfile.write(indiv_line)
            continue
        indiv_line = indiv_line.strip("\n")
        split_list = indiv_line.split("\t")
        print(split_list)

#Assign variables for all the information we need
        chr = split_list[2]                         
        bitwise_flag = int(split_list[1])
        curr_umi = grab_umi(split_list[0])             
        positive_strand = strandedness(bitwise_flag)
        position = split_list[3]
        cigar_string = split_list[5]


        if curr_umi not in big_umi_set:
            continue
     #print(cigar_string)             
        if chr != temp_chr:                         #If the chromosome doesn't match the last chromosome, reset.
            chr = temp_chr
        if positive_strand is True:
            adjust_pos = positive_strand_soft_clipping(cigar_string)

            #soft clipping bullshit#to make pylance not itself
        elif positive_strand is False: #negative strand
            minus_adjust_pos = minus_strand_soft_clipping(cigar_string)

                

                                                    

                
            
                


