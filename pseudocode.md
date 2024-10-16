Part 1: Define the Problem 
----
## The Actual Problem 

When doing PCR in library prep, one of the issues that we face in our data are PCR duplicates. PCR duplicates can be tricky to identify because they differ from natural biological repeats that could indicate higher levels of gene expression. 

There are a few different ways we can differentiate PCR duplicates from natural duplicates. PCR duplicates are characterized by meeting a few conditions. These conditions include reads that are occurring on the same chromosome, have the same strandedness, same UMI and have the same position. If a read meets all four of these conditions then it is considered a PCR duplicate and we must toss it. 

There are a few considerations that we need to take into account when we are writing a script that takes care of these duplicates. Primarily, we need to consider the role of soft clipping. Soft clipping is when the front of the read doesn't map to the reference. When this occurs, it can alter the position listed in column 4 of the SAM file. As a result, we might see a read that appears to be a duplicate because it has the same position (and other matching parameters) but due to soft clipping is actually  not a duplicate. This could happen in the reverse too where a read might not appear to be a duplicate but because of soft clipping, the position is actually the same as another read making it a duplicate. 

### Different Cases 

#### Case 1: Dupe: Same Chromosome, Same UMI, Same Strand, Same Position  
- When reads have all of the parameters the same. For this case though, note that since we are not accounting for read content or length, cases where Same Chromosome, Same UMI, Same Strand and Same Position are equivalent to a case where since we are not accounting for read content or length, cases where Same Chromosome, Same UMI, Same Strand and Same Position BUT lengths of the read are longer because position is counted from leftmost end of the strand. 

- test_file_qname: Case_1 

#### Case 2: Dupe: Same Chromosome, Same UMI, Same Strand, Same Position after calculating for SOFT CLIPPING
- In this case, the read appears to look like it is not a dupe because it has a different position but because of soft clipping, the position is the same and this read is therefore a dupe. 

- test_file_qname: Case_2

#### Case 3: NOT Dupe: Different Chromosomes
- Reads that are on different chromosomes are NOT considered dupes.

- test_file_qname: Case_3

#### Case 4: NOT Dupe: Same Chromosome, Different UMI 
- Reads that are on the Same Chromosome but have different UMI's are not dupes. 

- test_file_qname: Case_4

#### Case 5: NOT Dupe: Same Chromosome, Same UMI, DIFFERENT STRAND 
- Reads that are on the same chromosome with the same UMI but are on different strands are NOT dupes. 

- test_file_qname: Case_5

#### Case 6: NOT Dupe: Same Chromosome, Same UMI, Same Strand, DIFFERENT Position (but no soft clipping)
- Reads that are on the same chromosome, have the Same UMI, Same Strand but are on different positions with no soft clipping are NOT dupes. 

- test_file_qname: Case_6

#### Case 7: NOT Dupe: Same Chromosome, Same UMI, Same Strand, Different Position after SOFT CLIPPING
- When the line from the file is read in, all the parameters we are checking makes the read appear like a dupe, however because the the CIGAR string has an S, we know that soft clipping is actually occurring and therefore changing the position which makes this case *not a dupe*.

- test_file_qname: Case_7


Part 2: Test Files
----

See test files in `unit_tests` folder. `test_input.sam` is the original unsorted file and then using bash, we sorted by chromosome and then UMI. `test_input1.sam` is the sorted variation of that. `test_output.sam` is the output file for the sorted input. 

Part 3: Pseudocode
----

```

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

```

Part 4: High Level Functions 
----

    def function_that_extracts_UMI_Chr(int)
        ```This function will be extracting the UMI and the Chr from each line as it is read through```
    return chr, UMI

    Input: Case_1:CTGTTCAC	0	2	100	36	10M	*	0	0	TCCACCACAA 6AEEEEEEEE	MD:Z:53G16	NH:i:1	HI:i:1	NM:i:2	SM:i:36	XQ:i:40	X2:i:0	XO:Z:UU
    Output: 2, CTGTTCAC


    def calculate_soft_clipped_position(takes in line of SAM file that has been softclipped)
    ```Calculate the new position of a read if soft clipping is occurring```
    return position

    Input: Takes in the line of the SAM file that has been softclipped
    Example SAM file Line: 
    NS500451:154:HWKTMBGXX:1:11101:24936:1293:TGAGTGAG	0	2	100	36	4S16M	*	0	0	GTCCGATTGCTTCTTTATAC	6AEEEEEEEEEEEEEEEEEE	MD:Z:71	NH:i:1	HI:i:1	NM:i:0	SM:i:36	XQ:i:40	X2:i:0	XO:Z:UU	XS:A:-	XG:Z:A

    Output: Calculated New Position that has been accounted for soft clipping. 