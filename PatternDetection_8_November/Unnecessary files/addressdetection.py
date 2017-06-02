import pyap,re
import numpy
def GetOneAddress(text):
	line=text
	#grp=re.finditer(r'\d{1,2}(?:(?:am|pm)|(?::\d{1,2})( )(?:am|pm)?)', line,re.I|re.M)
	street_address = re.finditer("\d{1,4}(?:[\w\-]{1,2}) [\w\d\s\,\.\-\']{0,100}(?:street|st|avenue|av|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|pike|pk|lane)",line,re.I|re.M)
	
	'''for e in street_address:
		print "address:"+text[e.start():e.end()]'''
	'''for p in street_address:
	    print p.group()'''
	addsum=sum(1 for e in street_address)
	chcount=text.lower().count("Church".lower())
	allsum=addsum#+chcount
	if allsum==0 and chcount==1:
		return 1
		
	return allsum

#print GetOneAddress("Up Front Alano302 4th Ave. NE, Brainerd")

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
	for p in self.fed:
		print p
       # return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



def GetNumberOfTimes(text,seqcount):
	arr=["1 pm","2 pm","3 pm","4 pm","5 pm","6 pm","7 pm","8 pm","9 pm","10 pm","11 pm","12 pm","1 am","2 am","3 am","4 am","5 am","6 am","7 am","8 am","9 am","10 am","11 am","12 am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm", "12pm", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12am"]
	text=text.replace("&nbsp;"," ")
	text=text.replace("<"," ")
	text=text.lower()
	line=text
	count=0

	startadd=-1
	endadd=-1
	dist=0
				
	#grp=re.finditer('\d{1,2}(:(\d{2})*)\s*(AM|am|PM|pm|a|p)?', line,re.I|re.M)
	grp=re.finditer('(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(AM|am|PM|pm)?)|([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])?\s*(AM|am|PM|pm)|(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(a|A|p|P))',line,re.I|re.M)

		
	re.sub('\d{1,2}(:(\d{2})*)\s*(AM|am|PM|pm|a|p)','',line)
	
	for pp in grp:
		print text[pp.start():pp.end()]

print GetNumberOfTimes('<p>05:30 PM (06095) ................................. After Shifters Meeting <b>(O-D-NS-WA)</b><br /><a href="https://www.google.com/maps/place/1800+U.S.+Hwy+50+E,+Carson+City,+NV+89701/@39.1731208,-119.7492678,17z/data=!3m1!4b1!4m2!3m1!1s0x80990a85cfb0ba6b:0x2ae7febea2302372" target="_blank">1800 Highway 50 East #5</a><br /></p>"',124)
'''t=[14,7,10] 
v=0
v=sum(abs(t[i+1]-t[i]) for i in range(len(t)-1))
print v'''











