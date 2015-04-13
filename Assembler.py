import sys

if sys.version_info >= (3,0):
	xrange = range

def is_ainstr(command):
	return true if word[0] == "@" else false

def ainstr(command):
	command = int(command.lstrip("@")
	
	# converts to binary string w/only significant bits and "0b" header
	word = bin(command)
	
	# removes "0b" header
	word = word.lstrip("0b")
	
	# concatenate leading zeroes until the word is 16 bits wide
	while len(word) < 16:
		word = "0" + instr
	
	return word

def cinstr(command):
	# initialize strings to fill with command information
	lhs = "" # left of equals sign
	mid = "" # the computation portion in the middle
	rhs = "" # right of semicolon
	
	# worst-case when command is of format DEST=COMP;JUMP
	if "=" in command and ";" in command:
		# this is a gnarly and probably unpythonic way to break this down
		temp = command.split("=")
		# get the expression left of the equals sign
		lhs = temp[0]
		
		# break down the remainder into mid and rhs
		temp = temp[1].split(";")
		mid = temp[0]
		rhs = temp[1]
	
	# case when command is of format DEST=COMP
	elif "=" in command and ";" not in command:
		temp = command.split("=")
		lhs = temp[0]
		mid = temp[1]
	
	# case when command is of format COMP;JUMP
	elif ";" in command and "=" not in command:
		temp = command.split(";")
		mid = temp[0]
		rhs = temp[1]

	# case w/o assignment or jump considered error
	else:
		sys.stdout.write("Assembly instruction was invalid!\n")
		sys.stdout.write("Blew chunks at command '%s'.\n" %command)
		sys.exit()
	
	comp = get_comp_bits(mid)
	dest = get_dest_bits(lhs)
	jump = get_jump_bits(rhs)
	
	return "111%s%s%s" %(comp, dest, jump)

def get_jump_bits(string):
	# if no jump mnemonic, return "000"; do not jump
	if string == "":
		return "000"
	# this is kinda dumb code, to be honest, but it's not worth overthinking
	elif string == "JGT":
		return "001"
	elif string == "JEQ":
		return "010"
	elif string == "JGE":
		return "011"
	elif string == "JLT":
		return "100"
	elif string == "JNE":
		return "101"
	elif string == "JLE":
		return "110"
	elif string == "JMP":
		return "111"

def get_dest_bits(string):
	d = "1" if "D" in string else "0"
	a = "1" if "A" in string else "0"
	m = "1" if "M" in string else "0"
	
	return a + d + m

def get_comp_bits(string):
	pass
	
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

assembly.close()
machine.close()
