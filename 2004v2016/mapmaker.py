### color_map.py

#based on http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools/

import csv
from bs4 import BeautifulSoup
 
# Read in difference rates
perdiff = {}
min_value = 100; max_value = 0
reader = csv.reader(open('2004v2016.csv'), delimiter=",")
for row in reader:
	try:
		full_fips = str(row[2]) + str(row[3])
		rate = float(row[9].strip())
		perdiff[full_fips] = rate
	except:
		pass
 
# Load the SVG map
svg = open('uscountymap.svg', 'r').read()
 
# Load into Beautiful Soup
soup = BeautifulSoup(svg, "lxml")
 
# Find counties
paths = soup.findAll('path')
 
# Map colors
colors = ['#99bbff', '#6699ff','#3377ff','#0055ff','#0044cc','#003399',
'#ffffff','#ff9999','#ff6666','#ff3333','#ff0000','#cc0000','#990000']
 
# County style
path_style = '''font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;
stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;
marker-start:none;stroke-linejoin:bevel;fill:'''
 
# Color the counties based on unemployment rate
for p in paths:
	
	if p['id'] not in ["State_Lines", "separator"]:
		try:
			rate = perdiff[p['id']]
		except:
			continue

		if rate > .1:
			color_class = 0
		elif rate > .08:
			color_class = 1
		elif rate > .06:
			color_class = 2
		elif rate > .04:
			color_class = 3
		elif rate > .02:
			color_class = 4
		elif rate > 0:
			color_class = 5
		elif rate == 0:
			color_class = 6
		elif rate > -.02:
			color_class = 7
		elif rate > -.04:
			color_class = 8
		elif rate > -.06:
			color_class = 9
		elif rate > -.08:
			color_class = 10
		elif rate > -.1:
			color_class = 11
		else:
			color_class = 12
	
		color = colors[color_class]
		p['style'] = path_style + color
	 
print soup.prettify()
