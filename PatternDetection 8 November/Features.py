
import time ,os ,re
from xml.etree import ElementTree


def GetNumberOfTimes(text,seqcount):


	'''arr=["1 pm","2 pm","3 pm","4 pm","5 pm","6 pm","7 pm","8 pm","9 pm","10 pm","11 pm","12 pm","1 am","2 am","3 am","4 am","5 am","6 am","7 am","8 am","9 am","10 am","11 am","12 am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm", "12pm", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am", "12am"]'''
	text=text.replace("&nbsp;"," ")
	#text=text.replace("<"," ")
	text=text.lower()
	line=text

	adds=[]
	count=0
	dist=0

	grp=re.finditer('(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(AM|am|PM|pm)?)|([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])?\s*(AM|am|PM|pm)|(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(a|A|p|P))',line,re.I|re.M)

	for pp in grp:
		st=pp.start()
		if adds.count(st)==0:
			count+=1
			adds.append(st)

	#return count
	if count==0 and text.count("noon")==1:
		print "noon"+str(count)
		return 1
	elif count>=0 and count<=3:
		return count
	else:
		return -1
	'''if count==1 or count==0:
		return count

	else:
		adds.sort(reverse=True)
		dist=sum(abs(adds[i+1]-adds[i]) for i in range(len(adds)-1))
		return (1.0*dist)/len(text)#(1.0/dist)*seqcount'''

def GetNumberOfAddresses(text,seqcount):

	line=text.lower()
	street_address = re.finditer("\d{1,4}(?:[\w\-]{1,2}) [\w\d\s\,\.\-\']{0,100}(?:street|st|avenue|av|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|pike|pk|lane)",line,re.I|re.M)

	adds=[]
	dist=0
	countAdd=0
	countMap=0
	countChurch=0
	countClub=0

	for pp in street_address:
		st=pp.start()
		if adds.count(st)==0:
			countAdd+=1
			adds.append(st)
			#print "Address found:"+text[pp.start():pp.end()]
	if countAdd<=2:
		return 1
	for pp in re.finditer("church", line,re.I|re.M):
		st=pp.start()
		if adds.count(st)==0:
			countChurch+=1
			adds.append(st)
	if countChurch<=2:
		return 1
		
	for pp in re.finditer("club", line,re.I|re.M):
		st=pp.start()
		if adds.count(st)==0:
			countChurch+=1
			adds.append(st)
	if countClub<=2:
		return 1
		
	for pp in re.finditer("maps.google.com", line,re.I|re.M):
		st=pp.start()
		if adds.count(st)==0:
			countMap+=1
			adds.append(st)
	if countMap<=2:
		return 1
	for pp in re.finditer("google.com/maps", line,re.I|re.M):
		st=pp.start()
		if adds.count(st)==0:
			countMap+=1
			adds.append(st)

	if countMap<=2:
		return 1
	count=countAdd+countChurch+countClub+countMap
	if count<=0:
		return -1
	'''if count==1 or count==0:
		return count

	else:
		adds.sort(reverse=True)
		dist=sum(abs(adds[i+1]-adds[i]) for i in range(len(adds)-1))
		return (1.0*dist)/len(text)#(1.0/dist)*seqcount'''


def GetPresenceOfDays(text,seqcount):

	arr=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sun","Mon","Tues","Tue","Wed","Thurs","Thu","Fri","Sat"]
	text=text.lower()

	adds=[]
	count=0
	dist=0
	for el in arr:
		for pp in re.finditer(el.lower(), text,re.I|re.M):
			st=pp.start()
			if adds.count(st)==0:
				count+=1
				adds.append(st)
	if count==1 or count==0:
		return count
	else:

		adds.sort(reverse=True)
		dist=sum(abs(adds[i+1]-adds[i]) for i in range(len(adds)-1))
		#print "distance"+str(count)
		return (1.0/dist)*seqcount

def RemoveHTMLTags(s):
	tag = False
    	quote = False
	out = ""
	for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
		out = out + " "
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c
	return out




















def GetMissingAddresses(text):

	line=text.lower()
	street_address = re.finditer("\d{1,4}(?:[\w\-]{1,2}) [\w\d\s\,\.\-\']{0,100}(?:street|st|avenue|av|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|pike|pk|lane)(\s|\<)",line,re.I|re.M)

	adds=[]
	dist=0
	count=0
	st1=-1
	end1=-1

	st2=-1
	end2=-1

	st3=-1
	end3=-1

	st4=-1
	end4=-1

	for pp in street_address:
		st1=pp.start()
		end1=pp.end()

	'''for pp in re.finditer("church", line,re.I|re.M):
		st2=pp.start()
		end2=pp.end()

	for pp in re.finditer("maps.google.com", line,re.I|re.M):
		st3=pp.start()
		end3=pp.end()

	for pp in re.finditer("google.com/maps", line,re.I|re.M):
		st4=pp.start()
		end4=pp.end()'''

	string=text[st1:end1]
	return string

def GetMissingDay(text):

	arr=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sun","Mon","Tues","Tue","Wed","Thurs","Thu","Fri","Sat"]
	text=text.lower()

	st1=-1
	end1=-1
	for el in arr:
		for pp in re.finditer(el.lower()+'(\s|\<)', text,re.I|re.M):
			st=pp.start()
			if st>st1:
				st1=st
				end1=pp.end()

	string=text[st1:end1]
	return string


def GetTotalTime(text):
	text=text.lower()
	line=text

	adds=[]
	count=0
	grp=re.finditer('(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(AM|am|PM|pm)?)|([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])?\s*(AM|am|PM|pm)|(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(a|A|p|P))',line,re.I|re.M)
	for pp in grp:
		count+=1
	return count
