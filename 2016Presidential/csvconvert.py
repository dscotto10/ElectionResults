import csv

r = csv.reader(open('usfipscodes.csv')) # Here your csv file
lines = [l for l in r]
	
for i in range(0,len(lines)):
	lines[i][0] = lines[i][0].upper()
	lines[i][0] = lines[i][0].replace(" ","-")
	lines[i][1] = lines[i][1].upper()
	lines[i][1] = lines[i][1].replace(" ","")
		
	with open('newusfipscodes.csv', 'a') as csvfile:
		linewriter = csv.writer(csvfile, delimiter=',')
		linewriter.writerow(lines[i])