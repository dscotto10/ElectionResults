import csv

def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("+003")
	return input1

resultsfile2004 = "2004results.csv"
resultsfile2016 = "2016results.csv"

r = csv.reader(open('2004results.csv'))
results2004 = [l for l in r]

r = csv.reader(open('2016results.csv'))
results2016 = [l for l in r]

for i in range(1,len(results2004)):

	statename = results2004[i][0]
	countyname = results2004[i][1]
	stateFIPS = results2004[i][2]
	countyFIPS = results2004[i][3]
	kerryvotes = results2004[i][4]
	kerryper = results2004[i][5]
	kerryper = kerryper.replace("%","")
	kerryper = kerryper.replace("'","")
	kerryper = float(kerryper) / 100
	
	for j in range(1,len(results2016)):
		if stateFIPS == results2016[j][2] and countyFIPS == results2016[j][3]:
			clintonvotes = results2016[j][4]
			clintonper = results2016[j][5]
			clintonper = clintonper.replace("%","")
			clintonper = clintonper.replace("'","")
			clintonper = float(clintonper)/100
			votediff = int(clintonvotes) - int(kerryvotes)
			perdiff = clintonper - kerryper
			
	
	countyline = []
	
	countyline.append(statename)
	countyline.append(countyname)
	countyline.append(stateFIPS)
	countyline.append(countyFIPS)
	countyline.append(kerryvotes)
	countyline.append('%.3f' % kerryper)
	countyline.append(clintonvotes)
	countyline.append('%.3f' % clintonper)
	countyline.append(votediff)
	countyline.append('%.3f' % perdiff)
	
	#write that list to the CSV file.
	with open('2004v2016.csv', 'a') as csvfile:
		countylinewriter = csv.writer(csvfile, delimiter=',')
		countylinewriter.writerow(countyline)