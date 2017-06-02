
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
	#grp=re.finditer('\d{1,2}(:(\d{2})*)\s*(AM|am|PM|pm|a|p)?', line,re.I|re.M)
	grp=re.finditer('(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(AM|am|PM|pm)?)|([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])?\s*(AM|am|PM|pm)|(([0-9]|0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9])\s*(a|A|p|P))',line,re.I|re.M)
		
	#re.sub('\d{1,2}(:(\d{2})*)\s*(AM|am|PM|pm|a|p)','',line)
	
	for pp in grp:
		st=pp.start()
		if adds.count(st)==0:
			count+=1
			adds.append(st)
	

	return count

def GetNumberOfAddresses(text,seqcount):

	line=text.lower()
	street_address = re.finditer("\d{1,4}(?:[\w\-]{1,2}) [\w\d\s\,\.\-\']{0,100}(?:street|st|avenue|av|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|pike|pk|lane)",line,re.I|re.M)
	
	adds=[]
	dist=0
	count=0

	for pp in street_address:
		st=pp.start()
		if adds.count(st)==0:
			count+=1
			adds.append(st)
	return count


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

	
	
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get("http://www.utahaa.org/southeast.php")
#"http://www.aacentrallakes.org/meetings.html"
#"http://www.aa-cedarrapids.org/meetings/"
string=browser.page_source
start=string.find("<body")
if start>=0:
	string=string[start:]

class DayRecord(object):
	daystring=None
	sindex=-1
	eindex=-1
	
	def __init__(self, data,i,j):
        	self.daystring = data
        	self.sindex=i
		self.eindex=j


alldays=[]	
def regex_day(text):
	text=text.lower()
	day_arr=["saturday","sunday","monday","tuesday","wednesday","thursday","friday"]
	
	dayreg = re.finditer("(satur|sun|mon|tues|wednes|thurs|fri)(day)",text,re.I|re.M)
	start_day=""
	
	arr_start_index=-1
	arr_end_index=-1

	count=0
	for elem in dayreg:
		daystr=DayRecord(text[elem.start():elem.end()],elem.start(),elem.end())
		print daystr.daystring
		alldays.append(daystr)
		

	curindex=0
	for i in range(0,len(alldays)):
		
		#print i
		arrindex=day_arr.index(alldays[i].daystring)
		for j in range(curindex,-1,-1):
			innerindex=day_arr.index(alldays[j].daystring)
			if arrindex-innerindex==1:
				#print text[alldays[j].eindex+1:alldays[i].sindex]
				print "time:"+str(GetNumberOfTimes(text[alldays[j].eindex+1:alldays[i].sindex],0))+"address:"+str(GetNumberOfAddresses(text[alldays[j].eindex+1:alldays[i].sindex],0))
				print "days:"+str(alldays[j].daystring)+","+str(alldays[i].daystring)
		
		curindex+=1
	'''dayreg = re.finditer("(satur|sun|mon|tues|wednes|thurs|fri)(day)",text,re.I|re.M)
	
	i=0
	for elem in dayreg:
		if i==0:
			prev=text[elem.start():elem.end()]
		else:
			cur=text[elem.start():elem.end()]
			if cur==prev:
				continue
			else:
				prev=cur
		
		print text[elem.start():elem.end()]'''



regex_day(string)

#GetNumberOfTimes('<br />8 pm - </strong>',0)









	
