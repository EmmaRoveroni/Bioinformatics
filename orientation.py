#!/usr/bin/python3
import sys

#PART 1: get the argument from the command line and to set up the main variables.
if len(sys.argv) == 1:
	print("Syntax: " + sys.argv[0] + " file.sam genomelength max_fragment_size orientation")
	exit()

genome_length = int(sys.argv[2])
genome_change = [0]*genome_length # genome_change is a list of integers all set to zero
max_fragment_size = int(sys.argv[3])
orientation = int(sys.argv[4]) #orienation can be 0, 16, 32 or 48

#PART 2: reads the entire sam file and calculate the coverage at every single base
sam_file = open(sys.argv[1]) # open sam file
for line in sam_file: # read each line into the variable "line"
	if line[0] != '@': # do the block below only if line does'n starti with @
		fields = line.split("\t") # make list of tab-separated fields
		if((int(fields[1]) & 12) == 0): # both flags unset (equal to 0) indicates that  both segments map (8+4=12)
			if ((int(fields[8]) > 0) and (int(fields[8]) < max_fragment_size)): # consider only the one that are going in one direction (not the negative) AND we fixed the length to avoid the problem of the repeats
				if ((int(fields[1])) & 48 == orientation): #it does the bitwise & between the number present in fields[1] and 48, if the results of this operation is equal to the considered orientation value it enters the if 
					start_pos = int(fields[3]) # fields[3] is the map position (column 4)
					mate_length = 100
					end_pos = start_pos + mate_length # column 8
					# prof 2022 end_pos = start_pos + int(fields[8]) + 100
					genome_change[start_pos] += 1 # increment counter at start_pos by one
					genome_change[end_pos + mate_length ] -= 1 # decrement counter at end_pos by one
sam_file.close()

#PART 3:  output the wig file.
print("fixedStep chrom=genome start=1 step=1 span=1") # print track as a wiggle file
current_coverage = 0
current_sum = 0
for position in range(genome_length): # cicle over all positions of the genome
	current_coverage = current_coverage + genome_change[position]
	print(current_coverage)
