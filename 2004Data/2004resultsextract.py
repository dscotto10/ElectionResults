from bs4 import BeautifulSoup
import urllib2
import csv
import time

def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("\n")
	return input1
	
def standardize(inputtext):
	inputtext = inputtext.upper()
	inputtext = inputtext.replace(" ","")
	inputtext = inputtext.replace(".","")
	inputtext = inputtext.replace("'","")
	return inputtext

def intconvert(inputtext):
	inputtext = inputtext.replace(",","")
	inputtext = inputtext.replace(" ","")
	inputtext = inputtext.replace("'","")
	return int(inputtext)

#get all state names, put into list
statelist = "statenames.txt"
statenameslist = newlinefile(statelist)

#put all FIPS codes in nested list called fipslines
r = csv.reader(open('newusfipscodes.csv'))
fipslines = [l for l in r]

#loop through every state in list
for n in range(0,len(statenameslist)-1):
	
	#for Virginia, for later.
	cityadder = "NO"
	
	web_string = "https://en.wikipedia.org/wiki/United_States_presidential_election_in_" + statenameslist[n] + ",_2004"
	web_page = urllib2.urlopen(web_string)
	soup = BeautifulSoup(web_page, "lxml")
	
	statename = statenameslist[n].upper()
	statename = statename.replace("_","-")
	print statename

	#print soup.prettify()

	countytables = soup.find_all("table")
	j = 0

	while j < len(countytables):
		if countytables[j].th is not None and (countytables[j].th.string == "County" or countytables[j].th.string == "Parish" or countytables[j].th.string == "County or City"):
			x = j
		j += 1

	countyrows = countytables[x].find_all("tr")
	countyheaders = countytables[x].find_all("th")

	for m in range(1,len(countyrows)):
		countyresults = countyrows[m].find_all("td")
		#print countyresults
		countyname = countyresults[0].string
		
		#print countyname
		
		if countyname is None:
			countyname = countyresults[0].get('a','title') #willproduceFIPS

		if countyname.find("County") > -1:
			countyname = countyname[0:countyname.find("County")-1]
		
		if countyname.find("(") > -1:
			countyname = countyname[0:countyname.find("(")-1]

		countyname = standardize(countyname)

		kerryvotes = countyresults[2].string
		kerryper = countyresults[1].string
		bushvotes = countyresults[4].string
		bushper = countyresults[3].string
		
		if len(countyresults) > 5:
			othervotes = countyresults[6].string
			otherper = countyresults[5].string
		else:
			othervotes = "0"
			otherper = "0"
		
		if kerryvotes.find(".") > -1 or kerryvotes.find("%") > -1 :
			kerryvotes, kerryper = kerryper, kerryvotes
		
		if bushvotes.find(".") > -1 or bushvotes.find("%") > -1:
			bushvotes, bushper = bushper, bushvotes
		
		if othervotes.find(".") > -1 or bushvotes.find(".")  > -1:
			othervotes, otherper = otherper, othervotes
		
		headercheck = countyheaders[1].string
		
		if headercheck[0:1] == "B":
			kerryvotes, bushvotes = bushvotes, kerryvotes
			kerryper, bushper = bushper, kerryper
		
		kerryvotes = intconvert(kerryvotes)
		bushvotes = intconvert(bushvotes)
		othervotes = intconvert(othervotes)
		
		#if you flipped cityadder to "YES", append the word "CITY" to the countyname.
		#this is a necessary fix becasue of how Virginia works.
		if cityadder == "YES":
			countyname = countyname[0:countyname.find(",")] + "CITY"
		
		fipsstate = "ERROR"
		fipscounty = "ERROR"
		
		#look for the state name and county name match from our FIPS list.
		#store those results in a variable.
		for k in range(0,len(fipslines)):
			if fipslines[k][0] == statename and fipslines[k][1] == countyname:
				fipsstate = str(fipslines[k][2])
				fipscounty = str(fipslines[k][3])
		
		#this is the "switch" for VA. After York, everything is a city.
		if statename == "VIRGINIA" and countyname == "YORK":
			cityadder = "YES"

		#the actual export begins here.
		#create a list of all of our elements for our CSV file.
		countyline = []
		
		countyline.append(statename)
		countyline.append(countyname)
		countyline.append(fipsstate)
		countyline.append(fipscounty)
		countyline.append(kerryvotes)
		countyline.append(kerryper)
		countyline.append(bushvotes)
		countyline.append(bushper)
		countyline.append(othervotes)
		countyline.append(otherper)
		
		#write that list to the CSV file.
		with open('2004results.csv', 'a') as csvfile:
			countylinewriter = csv.writer(csvfile, delimiter=',')
			countylinewriter.writerow(countyline)
	