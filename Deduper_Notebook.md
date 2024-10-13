Saturday October 12th, 2024: I am being pushed to the brink and it is only the third week of school 
---

Dedupe Pseudocode Day 

**Define the problem:**

We need to differentiate PCR duplicates from actual biological duplicates. This is the main overarching problem. 

Write up a strategy for writing a Reference Based PCR Duplicate Removal tool. That is, given a sam file of uniquely mapped reads, remove all PCR duplicates (retain only a single copy of each read). Develop a strategy that avoids loading everything into memory. You should not write any code for this portion of the assignment. Be sure to:




Write examples:
Include a properly formated sorted input sam file



Include a properly formated expected output sam file
Develop your algorithm using pseudocode
Determine high level functions
Description
Function headers
Test examples (for individual functions)
Return statement


1. Samtools sort by chromosome using a bash command and then do python code. 
    - If it's NOT on the same chromosome then it can't be a duplicate 
2. Sort by UMI 
    - This is the smallest partition we can divide things up by. 
    - Want to reduce the amount of memory being used
3. Strandedness 
4. Soft-clipping?
5. Position? 

S in CIGAR String means softclipped 

Different Cases: 

1. Not Duplicates 

2. Obvious Duplicates (No Soft Clipping)

3. Left Soft Clip 

4. Right Soft Clip 

5. All matching but position so not a duplicate (Not Dupe)


To Sort by UMI: 
`sort -t ':'  -k 8`


Installed Samtools into Base Environment 
`conda install bioconda::samtools`


Sorting by Chr and then by UMI in one step vs. Sorting by Chr and then taking that output and sorting by UMI 

Trying to sort by chromosome and then by the UMI in one command: 

Sort by chromosome then UMI using bash

`cat test.sam | grep -v "@" | sort -t ':'  -k 8 | sort -k 3 -s`


There are two cases duplicate cases. 

1. Same chromosome, same strandedness, same position
2. Soft Clipping duplicate 

We are not checking the right side soft clipping. We also are only checking position on the left. So reads that are different lengths but meet all the requirements of 1. are considered the same as reads that are the same lengths and meet the requirements of 1. 

If two reads have the same UMI, we toss one and keep the other 


Need to input the UMI's as a set 



Write function to recalculate position

Pseudocode: 

1. Sort by UMI's and then chromosomes using bash 

2. Establish a set of the known UMI's from the input list 

3. Read in the SAM file line by line!

4. If the UMI does != current UMI OR if the chr != current chromo, RESET EVERYTHING. 
Everytime you encounter a new UMI or a new chromosome then clear. 
        - If UMI is not in the list....then calculate the hamming distance to all the other 

5. Check strandedness to see whether or not it is + or - stranded. Do this using if bitwise flag, bit 16. 

bit 16 is 1 if it's a + strand and bit 16 is 0 if it's a - strand. 
If rev_comp is true then it is a - strand and it is checking this by seeing if the bit is set to 0 or 1. 

6. Establish an empty set that we are going to repopulate with position adjusted for the soft clip for every line

 - Calculuate position
    - Account for soft clipped by:
    If the CIGAR string contains an S:  
        - Calculate position by adjusting whatever is stated as the position in SAM column 4 and adding whatever is in front of the S by that number. So for example if we have position set to 100 and the CIGAR string has a 4S, then adjust the position by subtracting 4 from the position to give the new position of 96. 
            - If calculated position is not in the set, then write it to the output. 
            - else, continue. 
    Else: 
        - Check if position is not in the set. If position is not in the set, then write to the output. 
            - Else, continue. 


6. If it is on 

A List of Functions

def function_that_extracts_UMI_Chr(int)
    ```This function will be extracting the UMI and the Chr from each line as it is read through```
Output: 


def calculate_soft_clipped_position(takes in line of SAM file that has been softclipped)
```Calculate the new position of a read if soft clipping is occurring```
    return position
Input: Takes in the line of the SAM file that has been softclipped
Example SAM file Line: 
NS500451:154:HWKTMBGXX:1:11101:24936:1293:TGAGTGAG	0	2	100	36	4S16M	*	0	0	GTCCGATTGCTTCTTTATAC	6AEEEEEEEEEEEEEEEEEE	MD:Z:71	NH:i:1	HI:i:1	NM:i:0	SM:i:36	XQ:i:40	X2:i:0	XO:Z:UU	XS:A:-	XG:Z:A
Output: Calculated New Position that has been accounted for soft clipping.



### Possible Cases: 

####