#2004parse

def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("+003")
	return input1
	
rawdata = "2004rawdata.txt"

weirdfile = newlinefile(rawdata)
MEdata = []


for i in range(0,len(weirdfile)-1):
	if weirdfile[i][0:2] == "UT":
		print weirdfile[i]
