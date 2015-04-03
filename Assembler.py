import sys

if sys.version_info >= (3,0):
	xrange = range

# command line argument passed is the input file for the Assembler

if len(sys.argv) == 1:
	sys.stdout.write("No file to assemble!")
	sys.exit()

filename = str(sys.argv[1])
outfile = ""

# guarantee that the assembler receives the correct type of file

if ".asm" not in filename:
	sys.stdout.write("Wrong file extension!")
	sys.exit()
else:
	outfile = filename.replace(".asm", ".hack")

assembly = open(filename, 'r')
machine = open(outfile, 'w')

assembly.close()
machine.close()
