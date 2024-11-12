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


Sunday November 11th, 2024: Debugging has me tweaking out on another level 
---

A brief summary of all the bugs that were encountered on this long long long journey:

- Was clearing the set after every iteration instead of appending to the set resulting in keeping all of the reads instead of tossing duplicates 

- Mixed up temp_chr variable with the actual chr variable

- Had some issues with functions, forgot to account for one single case which was looking at soft clipping on the right which resulted in keeping a few hundred thousand reads that necessary. This kind of issue could have been resolved if I had simplified the function more and instead of iterating through the whole string, I instead just isolated the first tuple and stopped and didn't use a for loop. 

Command used to sort Leslie's big test file: 

`samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -o final_input_sorted.sam`


Final Command Used to Run the Script: 

`/usr/bin/time -v ./Wells_deduper.py -u STL96.txt -f final_input_sorted.sam -o final_output.sam `


Output:

Ordering was a little bit different due to the sam sort but this is what was copied into Leslie's survey with the technically correct chromosome order. 


```
1       697508
2       2787018
3       547615
4       589839
5       562160
6       510818
7       1113183
8       576463
9       627488
10      564903
11      1220389
12      359951
13      467659
14      387239
15      437465
16      360923
17      517566
18      290506
19      571665
MT      202002
X       317853
Y       2247
JH584299.1      3
GL456233.2      656
GL456211.1      6
GL456221.1      4
GL456354.1      1
GL456210.1      5
GL456212.1      4
JH584304.1      294
GL456379.1      2
GL456367.1      3
GL456239.1      1
GL456383.1      1
MU069435.1      5450
GL456389.1      1
GL456370.1      21
GL456390.1      1
GL456382.1      1
GL456396.1      17
GL456368.1      3
MU069434.1      3
The number of reads kept: 13719048
The number of duplicates: 4467362
The number of reads tossed with unknown UMIs: 0
The number of header lines was: 65
        Command being timed: "./Wells_deduper.py -u STL96.txt -f final_input_sorted.sam -o final_output.sam"
        User time (seconds): 71.83
        System time (seconds): 3.32
        Percent of CPU this job got: 99%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 1:15.56
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 557456
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 0
        Minor (reclaiming a frame) page faults: 193059
        Voluntary context switches: 1075
        Involuntary context switches: 96
        Swaps: 0
        File system inputs: 0
        File system outputs: 0
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0

```
