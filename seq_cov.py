#!/usr/bin/python3
import sys

#PART 1: get the argument from the command line and to set up the main variables.
if len(sys.argv) == 1:
	print("Syntax: " + sys.argv[0] + " file.sam genomelength")
	exit()

genome_length = int(sys.argv[2])
genome_change = [0]*genome_length # genome_change is a list of integers all set to zero

#PART 2: reads the entire sam file and calculate the coverage at every single base
sam_file = open(sys.argv[1]) # open sam file
for line in sam_file: # read each line into the variable "line"
	if line[0] != '@': # do the block below only if line does'n starti with @
		fields = line.split("\t") # make list of tab-separated fields
		print(fields)
		if((int(fields[1]) & 4) == 0): # flag indicates that the read maps
			start_pos = int(fields[3]) # fields[3] is the map position
			end_pos = start_pos + 100 # this is because reads are 100 bases
			genome_change[start_pos] += 1 # increment counter at start_pos by one
			genome_change[end_pos] -= 1 # decrement counter at end_pos by one
sam_file.close()

#PART 3:  output the wig file.
print("fixedStep chrom=genome start=1 step=1 span=1") # print track as a wiggle file
current_coverage = 0
for position in range(genome_length): # cicle over all positions of the genome
	current_coverage = current_coverage + genome_change[position]
	print(current_coverage)
