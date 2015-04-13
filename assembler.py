import sys
from helper import *

if sys.version_info >= (3,0):
	xrange = range
	
# command line argument passed is the input file for the Assembler
try:
	filename = str(sys.argv[1])
except:
	sys.stdout.write("No file to assemble!\n")
	sys.exit()


outfile = ""

# guarantee that the assembler receives the correct type of file
try:
	outfile = filename.replace(".asm", ".hack")
except:
	sys.stdout.write("Invalid or missing file extension!\n")
	sys.exit()

assembly = open(filename, 'r')

# enter labels into dictionary
romline = 0
labels = {}
for line in assembly:
	# labels mark the following address of ROM, so pre-increment the count
	romline += 1
	
	# ignore leading whitespace, see if it's a label
	if line.strip()[0] == "(":
		# remove the bananas and store the raw label string
		label = line.lstrip("(").rstrip(")")
	
	# a label refers to the address in ROM of the following instruction
	labels[label] = str(romline)

assembly.close()

assembly.open()
machine = open(outfile, 'w')

# pre-defined addresses to be used/appended to by A-instruction
addresses = {
	"R0" : "0", "SP" : "0",
	"R1" : "1", "LCL" : "1",
	"R2" : "2", "ARG" : "2",
	"R3" : "3", "THIS" : "3",
	"R4" : "4", "THAT" : "4",
	"R5" : "5", "R6" : "6",
	"R7" : "7", "R8" : "8",
	"R9" : "9", "R10" : "10",
	"R11" : "11", "R12" : "12",
	"R13" : "13", "R14" : "14",
	"R15" : "15"
}

for line in assembly:
	# ignore comments
	if line.lstrip()[0:2] == "//":
		continue
	# ignore empty/whitespace-only lines
	if line.strip() == "":
		continue
	# ignore labels -- we've already stored them
	if line[0] == "(":
		continue
	
	if is_ainstr(line.strip()):
		machine.write(ainstr(line.strip(), labels, addresses))
	else:
		machine.write(cinstr(line.strip()))

assembly.close()
machine.close()
