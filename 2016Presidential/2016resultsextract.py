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
	
	#open the HTML file with the state results. 
	statepagename = statenameslist[n] + ".html"	
	stateme = open(statepagename,"r")
	
	#convert the state name to all-caps
	statename = statenameslist[n].upper()

	#run the soup. put all the tables into a list called "souptables."
	soup = BeautifulSoup(stateme,"lxml")
	souptables = soup.find_all("table")	

	#for each element in souptables (except the totals), do the following.
	for j in range(1,len(souptables)):
		
		#get the county name, convert to all caps.
		countyname = souptables[j].td.string
		countyname = standardize(countyname)
		
		#if you flipped cityadder to "YES", append the word "CITY" to the countyname.
		#this is a necessary fix becasue of how Virginia works.
		if cityadder == "YES":
			countyname = countyname + "CITY"
		
		#put all of the results from a given county table into souprows.
		souprows = souptables[j].find_all("tr")
		
		#knowing that the sequence is standardized, grab results in order.
		#this set puts the 4 labels into variables.
		clintonvotes = souprows[0].find("td", attrs={'class':"dat"}).string
		clintonper = souprows[0].find("td", attrs={'class':"per"}).string
		trumpvotes = souprows[1].find("td", attrs={'class':"dat"}).string
		trumpper = souprows[1].find("td", attrs={'class':"per"}).string
		mcmullinvotes = souprows[2].find("td", attrs={'class':"dat"}).string
		mcmullinper = souprows[2].find("td", attrs={'class':"per"}).string
		othervotes = souprows[3].find("td", attrs={'class':"dat"}).string
		otherper = souprows[3].find("td", attrs={'class':"per"}).string

		#make the vote totals integers.
		clintonvotes = int(clintonvotes.replace(",",""))
		trumpvotes = int(trumpvotes.replace(",",""))
		mcmullinvotes = int(mcmullinvotes.replace(",",""))
		othervotes = int(othervotes.replace(",",""))
		
		#default the fipsstate and fipscounty to "ERROR."
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
		countyline.append(clintonvotes)
		countyline.append(clintonper)
		countyline.append(trumpvotes)
		countyline.append(trumpper)
		countyline.append(mcmullinvotes)
		countyline.append(mcmullinper)
		countyline.append(othervotes)
		countyline.append(otherper)
		
		#write that list to the CSV file.
		with open('2016results.csv', 'a') as csvfile:
			countylinewriter = csv.writer(csvfile, delimiter=',')
			countylinewriter.writerow(countyline)
	