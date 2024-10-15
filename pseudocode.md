Part 1: Define the Problem 
----
## The Actual Problem 

PCR Duplicates are 

### Different Cases 

#### Case 1: Dupe: Same Chromosome, Same UMI, Same Strand, Same Position  
- When reads have all of the parameters the same. For this case though, note that since we are not accounting for read content or length, cases where Same Chromosome, Same UMI, Same Strand and Same Position are equivalent to a case where since we are not accounting for read content or length, cases where Same Chromosome, Same UMI, Same Strand and Same Position BUT lengths of the read are longer because position is counted from leftmost end of the strand. 

test_file_name: Case_1 

#### Case 2: Dupe: Same Chromosome, Same UMI, Same Strand, Same Position after calculating for SOFT CLIPPING
- In this case, the read appears to look like it is not a dupe because it has a different position but because of soft clipping, the position is the same and this read is therefore a dupe. 

test_file_name: Case_2

#### Case 3: NOT Dupe: Different Chromosomes
- Reads that are on different chromosomes are NOT considered dupes.

test_file_name: Case_3

#### Case 4: NOT Dupe: Same Chromosome, Different UMI 
- Reads that are on the Same Chromosome but have different UMI's are not dupes. 

test_file_name: Case_4

#### Case 5: NOT Dupe: Same Chromosome, Same UMI, DIFFERENT STRAND 
- Reads that are on the same chromosome with the same UMI but are on different strands are NOT dupes. 

test_file_name: Case_5

#### Case 6: NOT Dupe: Same Chromosome, Same UMI, Same Strand, DIFFERENT Position (but no soft clipping)
- Reads that are on the same chromosome, have the Same UMI, Same Strand but are on different positions with no soft clipping are NOT dupes. 

test_file_name: Case_6

#### Case 7: NOT Dupe: Same Chromosome, Same UMI, Same Strand, Different Position after SOFT CLIPPING
- When the line from the file is read in, all the parameters we are checking makes the read appear like a dupe, however because the the CIGAR string has an S, we know that soft clipping is actually occurring and therefore changing the position which makes this case *not a dupe*.

test_file_name: Case_7


Part 2: Test Files
----





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