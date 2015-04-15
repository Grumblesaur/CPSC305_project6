import sys

# function to determine whether command is an A-instruction
def is_ainstr(command):
	return command[0] == "@"


# function to parse an A-instruction and return a 16-bit binary string
# command = @-string passed from the main script
# labels = dictionary of user labels and corresponding ROM addresses
# addresses = dictionary of user and builtin labels and RAM storage locs.
def ainstr(command, labels, addresses):
	command = command.lstrip("@")
	
	# integer literal logic
	if command.isdigit():
		return "%s\n" % tobinary16(command)
	
	elif command not in addresses.keys():
		# label / jump target logic
		if command in labels.keys():
			return "%s\n" % tobinary16(labels[command])

		# variable logic
		else:
			addresses[command] = str(len(addresses) - 7)
			# there are 7 pre-defined labels that either overlap
			# or are not between 0-15 in the dictionary, so that's
			# why we're using a 7 here. Poor maintainability, I know,
			# but this is a one-off assignment.

			return "%s\n" % tobinary16(addresses[command])
	
	return "%s\n" % tobinary16(addresses[command])
	
# converts string of decimal characters to 16-bit wide binary string
def tobinary16(string):
	# convert to binary string headed by "0b"
	bits = bin(int(string))

	# remove leading "0b"
	bits = bits.lstrip("0b")
	
	# make the number 16 bits wide
	while len(bits) < 16:
		bits = "0" + bits
	
	return bits


# function to parse a C-instruction and return a 16-bit binary string
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
		sys.stdout.write("'%s' is an invalid instruction!\n" %command)
		sys.exit()
	
	comp = get_comp_bits(mid)
	dest = get_dest_bits(lhs)
	jump = get_jump_bits(rhs)
	
	return "111%s%s%s\n" %(comp, dest, jump)


# function to parse jump of a command and return 3-bit string
def get_jump_bits(string):
	jumpbits = ""
	jumps = {
		"" : "000",    "JGT" : "001",
		"JEQ" : "010", "JGE" : "011",
		"JLT" : "100", "JNE" : "101",
		"JLE" : "110", "JMP" : "111"
	}
	try:
		jumpbits = jumps[string]
	except:
		sys.stdout.write("'%s' is an invalid jump target!\n" %string)
		sys.exit()
	
	return jumpbits

# function to parse destination of a command and return 3-bit string
def get_dest_bits(string):
	d = "1" if "D" in string else "0"
	a = "1" if "A" in string else "0"
	m = "1" if "M" in string else "0"
	
	return "%s%s%s" %(a, d, m)

# function to parse comp of a command and return a 7-bit string
def get_comp_bits(string):
	# forgive me, but this code is stupid
	# it works, but it's not smart and would be totally impractical
	# on literally any other processor; I just can't think of a smarter
	# way to do it
	
	mnemonics = {
		# A-operations
		"0" : "0101010",     "1" : "0111111",
		"-1" : "0111010",    "D" : "0001100",
		"A" : "0110000",    "!D" : "0001101",
		"!A" : "0110001",   "-D" : "0001111",
		"-A" : "0110011",  "D+1" : "0011111",
		"A+1" : "0110111", "D-1" : "0001110",
		"A-1" : "0110010", "D+A" : "0000010",
		"A+D" : "0000010", # forgive A+D since + is commutative
		"D-A" : "0010011", "A-D" : "0000111",
		"D&A" : "0000000", "D|A" : "0010101",
		# forgive inverted A&D and A|D, since & and | are commutative
		"A&D" : "0000000", "A|D" : "0010101",
		
		# M-operations
		"M" : "1110000",   "!M" : "1110001",
		"-M" : "1110011",  "M+1" : "1110111",
		"M-1" : "1110010", "D+M" : "1000010",
		"M+D" : "1000010", # forgive M+D since addition is commutative
		"D-M" : "1010011", "M-D" : "1000111",
		"D&M" : "1000000", "D|M" : "1010101",
		# forgive inverted M&D and M|D since & and | are commutative
		"M&D" : "1000000", "M|D" : "1010101"
	}
	try:
		comp = mnemonics[string]
	except:
		sys.stdout.write("'%s' is an invalid command!\n" %string)
		sys.exit()
	return comp
	
