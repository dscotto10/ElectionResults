#2012datasetinspector

import csv

def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("\n")
	return input1

def newlinefile3(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split()
	return input1

rawdata = "2012rawdata.txt"
stateFIPS = "statefips.txt"

stateFIPS_dict = {}

stateset = newlinefile(stateFIPS)

for i in range(0,len(stateset)-1):
	stateabbrv = stateset[i][0:2]
	stateFIPS_dict[stateabbrv] = stateset[i][7:9]

splitset = newlinefile3(rawdata)

j = 0

newset = []

while j < len(splitset):
	stateabbrv = splitset[j+0]
	k = 1
	
	if splitset[j] == "AK":
		countyname = str(splitset[j+1][2:]) + str(splitset[j+2]) + str(splitset[j+3])
		stateFIPS = "02"
		countyFIPS = splitset[j+4]
		obamavotes = splitset[j+5][0:splitset[j+5].find(".")]
		romneyvotes = splitset[j+6][0:splitset[j+6].find(".")]
		othervotes = splitset[j+7][0:splitset[j+7].find(".")]
		obamaper = float(splitset[j+8]) / 100
		romneyper = float(splitset[j+9]) / 100
		otherper = float(splitset[j+10]) / 100
		
		j += 14
		
	else:
		while stateFIPS_dict[stateabbrv] != splitset[j+k+1][0:2]:
			k += 1
		countyname = splitset[j+1][2:]
		for m in range(1,k):
			countyname = countyname + str(splitset[j+1+m])
		stateFIPS = splitset[j+k+1][0:2]
		countyFIPS = splitset[j+k+1][2:]
		obamavotes = splitset[j+k+2][0:splitset[j+k+2].find(".")]
		romneyvotes = splitset[j+k+3][0:splitset[j+k+3].find(".")]
		othervotes = splitset[j+k+4][0:splitset[j+k+4].find(".")]
		obamaper = float(splitset[j+k+6]) / 100
		romneyper = float(splitset[j+k+7]) / 100
		otherper = float(splitset[j+k+8][0:5]) / 100
		
		j = j + k + 11
	
	countyline = []
		
	countyline.append(stateabbrv)
	countyline.append(countyname.upper())
	countyline.append(stateFIPS)
	countyline.append(countyFIPS)
	countyline.append(int(obamavotes))
	countyline.append('%.3f' % obamaper)
	countyline.append(int(romneyvotes))
	countyline.append('%.3f' % romneyper)
	countyline.append(int(othervotes))
	countyline.append('%.3f' % otherper)

	#write that list to the CSV file.
	with open('2012results.csv', 'a') as csvfile:
		countylinewriter = csv.writer(csvfile, delimiter=',')
		countylinewriter.writerow(countyline)

		
		
