#Two pass Assembler

import sys

import math



#Converting Decimal to binary

def DectoBin(a,n):

	return format(a, 'b').zfill(n)



def lengthOfInstr(line):

	#removing comments from line

	if(";" in line):

		line = line[:line.find("")]



	#removing Label definitions from line

	if(":" in line):

		line = line[line.find(":")+1:]



	elements = line.split()

	length = 0

	for a in elements:

		if a in opTable:

			length += 4

		else:

			length += 8

	return math.ceil(length/8) #returning nos of bytes in the line



#Checking if the line is a comment

def checkComments(line):

	return (line[0] == ";")



#First pass of a two pass assembler

def firstPass(lines):

	stpPresent = False

	lineNo = 0

	looctr = 2

	for lin in lines:

		breakReqd = False

		length = 0

		lineNo += 1

		if not(checkComments(lin)):

			operandCount = 0

			totNosOfOperand = 0

			interCode = []



			length = lengthOfInstr(lin)

			if ";" in lin :

				lin = lin[:lin.find(";")]

			line = lin.replace(","," ").split()



			if not(line):

				continue



			for element in range(len(line)):

				if (element == 0 and line[element][-1] != ":") or (element == 1 and line[0][-1] == ":"):

					if(line[element] not in opTable):

						print("lineNo",lineNo,": Error, illegal opcode, this line will not be included in the output")

						breakReqd = True

						break

				if line[element][-1]==":" and element == 0 and not(line[element][:-1].isdigit()):

					if line[element][:-1] in symTable and symTable[line[element][:-1]] != None:

						print("lineNo",lineNo,": Error, label defined more then once in program, this line will not be included in the output")

						breakReqd = True

						break

					symTable[line[element][:-1]] = ["l",DectoBin(looctr,8)]

					interCode.append(("ST",line[element][:-1]))

				elif line[element][-1]==":" and element == 0 and line[element][:-1].isdigit():

					NumericSymTable[line[element][:-1]] = DectoBin(looctr,8)

				elif line[element] in opTable:

					if line[element] == "STP":

						stpPresent = True

					interCode.append(("OP",opTable[line[element]]))

					if line[element] != "CLA" and line[element] != "STP":

						operandCount = 1

				elif line[element].isdigit():

					interCode.append(DectoBin(int(line[element]),8))

					totNosOfOperand += 1

				else:

					if line[element] not in symTable:

						symTable[line[element]] = None

					interCode.append(line[element])

					totNosOfOperand += 1



			#checking for operand count

			if totNosOfOperand < operandCount :

				print("lineNo",lineNo,": Not enough operands supplied for the given opcode, line ignored")

				breakReqd = True

			elif totNosOfOperand > operandCount:

				print("lineNo",lineNo,": Opcode supplied with too many operands, line ignored")

				breakReqd = True



			if breakReqd or not(interCode):

				continue



			intermediateTable.append(interCode)

			looctr += length



	for keys in symTable:

		if not(symTable[keys]):

			symTable[keys] =["v",DectoBin(looctr,8)]

			looctr += 1



	if not(stpPresent):

		print("Error: End not present in File, exiting....")

		sys.exit()



#Second pass of two pass assembler

def SecondPass():

	lineNo = 0

	for line in intermediateTable:

		lineNo += 1

		breakReqd = False

		opline = ""

		for i in line:

			if type(i) is tuple:

				if i[0]=="OP":

					opline += DectoBin(i[1],4)

			elif i.isdigit():

				opline += i

			else:

				if i in symTable and symTable[i][0] == "l" and not(line[line.index(i)-1][1] == 5 or line[line.index(i)-1][1] == 6 or line[line.index(i)-1][1] == 7):

					print("lineNos.",lineNo,": Error, Labels can be operands for JUMP type statements only, line will not be displayed in output")

					breakReqd = True

					break

				if i in symTable:

					opline += symTable[i][1]

				elif i in RegisterTable:

					opline += RegisterTable[i]

				elif len(i) == 2 and i[0].isdigit() and i[0] in NumericSymTable:

					opline += NumericSymTable[i[0]]

				else:

					breakReqd = True

					print("lineNo",lineNo,": Error, " + i + " not defined, line not displayed in output")

					break

			if not(type(i) is tuple and i[0] == "ST"):

				opline += " "

		if breakReqd:

			continue

		output.append(opline)

	return output



#Initializing all tables

opTable = {"CLA":0,"LAC":1,"SAC":2,"ADD":3,"SUB":4,"BRZ":5,"BRN":6,"BRP":7,"INP":8,"DSP":9,"MUL":10,"DIV":11,"STP":12}

symTable = {}

intermediateTable = []

output = []

RegisterTable = {"R1":"00000000","R2":"00000001"}

NumericSymTable = {}



#Reading file, passing the array of lines to firstPass method

inpFile = open("input.txt","r")

contents = inpFile.read()

lines = contents.split("\n")

firstPass(lines)

print("Output: intermediate values")

for lines in intermediateTable:

	print(lines)

if(len(NumericSymTable) != 0):

	print("\nNumeric symbol Table\n",NumericSymTable)

print("\nSymbol Table\n",symTable,"\n\nRegister Table\n",RegisterTable,"\n\nSecond pass output:")

SecondPass()

print("\n".join(output))

