#2004parse

import csv

def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("\n")
	return input1

def newlinefile3(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("+003")
	return input1
	
rawdata = "2004rawdata.txt"
stateFIPS = "statefips.txt"

stateFIPS_dict = {}


stateset = newlinefile(stateFIPS)

for i in range(0,len(stateset)-1):
	stateabbrv = stateset[i][0:2]
	stateFIPS_dict[stateabbrv] = stateset[i][7:9]

weirdfile = newlinefile3(rawdata)
usedFIPS = []

for i in range(1,len(weirdfile)-1):
	if len(weirdfile[i].split()) >= 15:
		countyset = weirdfile[i].split()
		j = 0
		stateabbrv = countyset[j][0:2]
		while stateFIPS_dict[stateabbrv] != countyset[j][0:2]:
			j += 1
		countyname = countyset[0][2:]
		for k in range(1,j-1):
			countyname = countyname + str(countyset[k])
		countyFIPS = str(countyset[j][2:5])
		if countyset[j][0:6] not in usedFIPS:
			usedFIPS.append(countyset[j][0:6])
			kerryvotes = countyset[j+1]
			kerryper = float(countyset[j+4]) / 100
			bushvotes = countyset[j+2]
			bushper = float(countyset[j+5]) / 100
			othervotes = countyset[j+3]
			otherper = float(countyset[j+6]) / 100
			
			countyline = []
		
			countyline.append(stateabbrv)
			countyline.append(countyname.upper())
			countyline.append(stateFIPS_dict[stateabbrv])
			countyline.append(countyFIPS)
			countyline.append(kerryvotes)
			countyline.append('%.3f' % kerryper)
			countyline.append(bushvotes)
			countyline.append('%.3f' % bushper)
			countyline.append(othervotes)
			countyline.append('%.3f' % otherper)
		
			#write that list to the CSV file.
			with open('2004resultsnew.csv', 'a') as csvfile:
				countylinewriter = csv.writer(csvfile, delimiter=',')
				countylinewriter.writerow(countyline)
