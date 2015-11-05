import sys
from helper import *

# pre-defined addresses to be used/appended to by ainstr()
addresses = {
	"R0" : "0",    "SP" : "0",
	"R1" : "1",    "LCL" : "1",
	"R2" : "2",    "ARG" : "2",
	"R3" : "3",    "THIS" : "3",
	"R4" : "4",    "THAT" : "4",
	"R5" : "5",    "R6" : "6",
	"R7" : "7",    "R8" : "8",
	"R9" : "9",    "R10" : "10",
	"R11" : "11",  "R12" : "12",
	"R13" : "13",  "R14" : "14",
	"R15" : "15",  "SCREEN" : "16384",
	"KBD" : "24576"
}

# reraise File I/O exceptions with helpful errors
try:
	filename = str(sys.argv[1])
except:
	raise Exception("No file to assemble!\n")
try:
	outfile = filename.replace(".asm", ".hack")
except:
	raise Exception("Invalid or missing file extension!\n")

assembly = open(filename, 'r')

# enter labels into dictionary
romline = 0
labels = {}
for line in assembly:
	# labels mark the following address of ROM, so pre-increment the count,
	# but only if it's a non-label line of code
	temp = line.strip()
	if not is_skippable(temp):
		romline += 1
	if temp != "" and temp[0] == "(":
		labels[prepare_label(temp)] = str(romline)

# close and reopen to start from top of file
assembly.close()
assembly = open(filename, 'r')
machine = open(outfile, 'w')

# assemble
for line in assembly:
	command = line.strip()
	# ignore comments, whitespace, empty lines, and labels
	if is_skippable(command):
		continue
	if "//" in command:
		command = pop_inline_comment(command)
	# write the A instruction as a binary string to the .hack file	
	if is_ainstr(command):
		machine.write(ainstr(command, labels, addresses))
	# write the C instruction as a binary string to the .hack file
	else:
		machine.write(cinstr(command))

assembly.close()
machine.close()
