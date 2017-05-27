import csv

resultsfilewi = "WI_deep_dive.csv"

class Locality:
	county = ""
	ward = ""
	trumpvotes = 0
	mcmullinvotes = 0
	gjohnsonvotes = 0
	rjohnsonvotes = 0
	potusvotes = 0
	senvotes = 0
	maxgopvotes = 0
	maxracevotes = 0
	
	def calcmax(self):
		if int(self.trumpvotes) + int(self.mcmullinvotes) + int(self.gjohnsonvotes) > int(self.rjohnsonvotes):
			self.maxgopvotes = int(self.trumpvotes) + int(self.mcmullinvotes) + int(self.gjohnsonvotes)
		else:
			self.maxgopvotes = int(self.rjohnsonvotes)
		if int(self.potusvotes) > int(self.senvotes):
			self.maxracevotes = int(self.potusvotes)
		else:
			self.maxracevotes = int(self.senvotes)
	
	def LocInfo(self):
		return '''This is %s in %s County. 
Trump got %s votes here. 
McMullin got %s votes here. 
Gary Johnson got %s votes here.
There were %s votes cast in the presidential election. 
Ron Johnson got %s votes here.
There were %s votes cast in the Senate election.
The maximum total number of votes for the GOP was %s. 
The maximum total votes in the election was %s.''' % (self.ward, self.county, self.trumpvotes,
		self.mcmullinvotes, self.gjohnsonvotes, self.potusvotes, self.rjohnsonvotes,
		self.senvotes, self.maxgopvotes, self.maxracevotes)

r = csv.reader(open(resultsfilewi))
resultswi = [l for l in r]

#filteredresultswi = []
localitylist = []
locality_dict = {}

totalgopvotes = 0
totalracevotes = 0
gjohnsonfactor = 0.8

for i in range(0,len(resultswi)):
	localityname = str(resultswi[i][0]) + ": " + str(resultswi[i][1])
	if localityname not in localitylist:
		localitylist.append(localityname)
		locality_dict[localityname] = Locality()
		locality_dict[localityname].county = resultswi[i][0]
		locality_dict[localityname].ward = resultswi[i][1]
	if resultswi[i][2] == "President":
		locality_dict[localityname].potusvotes = resultswi[i][4]
	elif resultswi[i][2] == "Senate":
		locality_dict[localityname].senvotes = resultswi[i][4]
	if resultswi[i][8] == "PresidentREPDon":
		locality_dict[localityname].trumpvotes = resultswi[i][7]
	elif resultswi[i][8] == "PresidentINDEva":
		locality_dict[localityname].mcmullinvotes = resultswi[i][7]
	elif resultswi[i][8] == "PresidentLIBGar":
		locality_dict[localityname].gjohnsonvotes = round(int(resultswi[i][7]) * gjohnsonfactor,0)
	elif resultswi[i][8] == "SenateREPRon":
		locality_dict[localityname].rjohnsonvotes = resultswi[i][7]

for i in range(0,len(localitylist)):
	locality_dict[localitylist[i]].calcmax()
	totalgopvotes += locality_dict[localitylist[i]].maxgopvotes 
	totalracevotes += locality_dict[localitylist[i]].maxracevotes

print str(totalgopvotes) + " total GOP votes."
print str(totalracevotes) + " total votes in the race."
print str(round(100 * float(totalgopvotes)/float(totalracevotes),2)) + " GOP percentage."
print str(totalgopvotes - 1409467) + " votes ahead of Trump."
