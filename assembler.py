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
machine = open(outfile, 'w')

for line in assembly:
	# ignore comments
	if line.lstrip()[0:2] == "//":
		continue
	# ignore empty/whitespace-only lines
	if line.strip() == "":
		continue
	
	if is_ainstr(line.strip()):
		machine.write(ainstr(line.strip()))
	else:
		machine.write(cinstr(line.strip()))

assembly.close()
machine.close()
