from bs4 import BeautifulSoup
import codecs, collections, csv, string, sys, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from xlrd import open_workbook
#my files imported below
from Classes import PatternString, TreeNode, Sequence, MLStripper, URLInfo, FormInfo,MeetingInfo,Position
from Database import InitDatabase,InsertMeeting
from ExtraFunctions import HighlightMeeting, highlight
from Features import GetNumberOfTimes, GetNumberOfAddresses, GetPresenceOfDays, GetMissingAddresses, GetMissingDay, GetTotalTime
from MeetingInformationExtractionFunctions import GetMeetingTime, GetMeetingAddress,GetMeetingDay,RemoveHTMLTags
from TreeFunctions import readPageInString, traverse, traversePrint, SetSubtrees, FindDuplicates, FindTags

browser = webdriver.Chrome(executable_path="/home/ugrad00/wang3570/aa-database-builder/PatternDetection 8 November/chromedriver")
connection=InitDatabase()
#the file o write number of meetings found and expected number of meetings
meetingrecordcsv = open("mrecord.csv", 'wt')
writer = csv.writer(meetingrecordcsv)
try:
    writer.writerow( ('URL', 'Meetings found', 'Expected Meetings') )
finally:
    print "exception"

txt=""
mptc=40	#maxiumum # of patterns to consider
wAddress=0.3	#weights to be considered
wTime=0.4
totalNumOfMeetings=0

alreadyMeetingsIndices=[]
def FindMeetingXY(pattern,iniPage,day,time,address):
	global totalNumOfMeetings
	first_tag=pattern.patString.split(',')[0]

	pagesubstring= iniPage#[pattern.start:pattern.end]
	#print "text:"+iniPage
	soup=BeautifulSoup(pagesubstring)
	souptext=soup.text
	filtered_soup = filter(lambda x: x in string.printable, souptext)

	for e in browser.find_elements_by_xpath("//"+first_tag):#browser.find_elements_by_xpath(".//"+first_tag+"[contains(text(), \""+soup.text+"\")]"):
		content=browser.execute_script("return arguments[0].textContent", e)
		filtered_elemtext=filter(lambda x: x in string.printable, content)
		filtered_elemtext="".join(filtered_elemtext.split())
		etext=e.get_attribute("innerHTML")
		if filtered_elemtext.replace(" ","") ==filtered_soup.replace(" ",""):
			mPos=Position(e.location['x'],e.location['y'],e.size['width'],e.size['height'])
			mUrl=browser.current_url
			mCity=""#"Rochester, Minnesota"
			mFtag=first_tag
			mFulltext=etext
			OneMeeting=MeetingInfo(day,time,address,mUrl,mCity,mFulltext,mFtag,mPos)
			InsertMeeting(connection,OneMeeting)										#calls insert function from database file
			totalNumOfMeetings+=1
			alreadyMeetingsIndices.append(pattern)


def CheckNotSubset(ptn):
	for onepattern in alreadyMeetingsIndices:
		if ptn.start>=onepattern.start and ptn.end<=onepattern.end:
			return 0
	
	return 1
'''def FindInfoInParents(cNode,tillindex):
	parent=cNode.parent
	found=0
	cnt=0
	while not found:
		if cnt==5:
			break
		cnt+=1
		if GetNumberOfAddresses(initialPage[parent.position:tillindex])==1:

			found=1

		else:
			parent=parent.parent

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()'''



#browser.get("http://www.birminghamaa.org/meetings.php")#("http://www.aaspringfield.org/Meetings.aspx")"http://aaonmv.org/12step/meeting-schedule/"
#"http://www.aa-waterloo.org/all-meetings.html"
#"http://www.booneaa.org/mondays"
#"http://www.moorecountyaa.org/id2.html"
#"http://www.aajacksonvillenc.org/Pages/AAMeetings.aspx"
#"http://www.aadistrict51.org/Meetings/Meetings.html"
#http://www.aanc32.org/thursday/


meetingURLArr=[]
def readMeetingURLs():
	wb = open_workbook('List of Meeting Pages.xlsx')
	s=wb.sheets()[0]
	for row in range(1,s.nrows):
		col_value = []
		mCity= ""#(s.cell(row,0).value)
		mUrl  = (s.cell(row,0).value)
		mNOM=0#(s.cell(row,2).value)
		oneMeetingURL=URLInfo(mUrl,mCity,mNOM)
		meetingURLArr.append(oneMeetingURL)


#finds out if page has dropdown with all days
def FindFormWithDaysIfAvailable():
	all_day=["sunday","monday","tuesday","wednesday","thursday","friday","saturday","sun","mon","tues","tue","wed","thurs","thu","fri","sat"]
	forms=browser.find_elements_by_tag_name("form")
	indexofform=-1
	for form1 in forms:

		indexofform+=1
		dropdowns=form1.find_elements_by_tag_name("select")
		indexofdropdown=-1
		for dropdown in dropdowns:
			print dropdown.text
			indexofdropdown+=1
			day_arr=[]
			options= dropdown.find_elements_by_tag_name("option")
			for option in options:
				probable_day=option.get_attribute("value")
				probable_day_inText=option.get_attribute("innerHTML")
				if probable_day.lower() in all_day:
					day_arr.append(probable_day.lower())
				elif probable_day_inText.lower() in all_day:
					day_arr.append(probable_day_inText.lower())
			if len(day_arr)>0 and all(x in all_day for x in day_arr):
				FormClass=FormInfo(indexofform,indexofdropdown)
				return FormClass
	return None

#finds out if page has <li> with all days
def FindListWithDaysIfAvailable():
	all_day=["sunday","monday","tuesday","wednesday","thursday","friday","saturday","sun","mon","tues","tue","wed","thurs","thu","fri","sat","any day"]
	lis=browser.find_elements_by_tag_name("li")
	indexlistarray=[]
	listindex=-1
	for li in lis:
		listindex+=1
		try:
			href=li.find_element_by_tag_name("a")
			if href:
				probable_day=href.get_attribute('innerHTML')#text
				if probable_day.lower() in all_day:
					indexlistarray.append(listindex)
		except:
			continue
	return indexlistarray

'''the last 3 parameters are passed beforehead if the pattern has missing information according to PD algo'''
def ExtractMeetingInfo(mPattern,fulltext,mDay,mTime,mAddress):

	mTime2=GetMeetingTime(RemoveHTMLTags(fulltext))
	if mTime2 is not None:
		mTime=mTime2

	mAddress2=GetMeetingAddress(RemoveHTMLTags(fulltext))
	if mAddress2 is not None:
		mAddress=mAddress2

	mDay2=GetMeetingDay(RemoveHTMLTags(fulltext))
	if mDay2 is not None:
		mDay=mDay2

	if  mDay and  mTime  and mAddress:
		mPos=FindMeetingXY(mPattern,fulltext,mDay,mTime,mAddress)



'''this function mainly runs the pattern detection algorithm and call ExtractMeetingInfo() for each probable meeting pattern '''
def LoadPagesAndRunPD(dayInfo):
	global totalNumOfMeetings

	txt=browser.page_source	#browser.find_element_by_tag_name('html').get_attribute('outerHTML')
	'''txt=txt.replace("&nbsp;"," ")
	with codecs.open ("examplePage.html", "w",encoding='utf-8') as myfile:
	    myfile.write(txt)
	txt=txt.replace("%20"," ")'''


	pagetext=txt#readPageInString("examplePage.html")
	#pagetext=txt
	initialPage=txt#pagetext
	troot=TreeNode("root")
	current=troot
	FindTags(pagetext,current)

	#allPatternsDict={}
	allPatterns=SetSubtrees(troot)


	taglist=FindDuplicates(troot)
	newlist = sorted(taglist, key=lambda x: x.seqcount, reverse=True)

	newlistdict={}
	for val in newlist:
		newlistdict.update({val.seqstring:val})

	'''t=1
	for p in newlist:
		#print p.seqstring
		if t==mptc:
			break
		t+=1'''

	maxweight=0
	maxindex=-1
	i=0
	for tag in taglist:
		if tag.seqcount*.9+tag.tagnums*0.1>maxweight:
			maxweight=tag.seqcount*.9+tag.tagnums*0.1
			maxindex=i
		i+=1


	#for onerecord in newlist:
	for pattern in allPatterns:
		first_tag=pattern.patString.split(',')[0]
		onerecord=newlistdict.get(pattern.patString)
		if onerecord is not None and pattern.patString==onerecord.seqstring and CheckNotSubset(pattern)==1:
			#break
			target = open("testhtml.html", 'a')
			withtags=initialPage[pattern.start:pattern.end]
			#tagsArray=strip_tags(withtags)
			#bingo=RemoveHTMLTags(withtags)
			numTime=GetNumberOfTimes(withtags,onerecord.seqcount)
			numAddress=GetNumberOfAddresses(withtags,onerecord.seqcount)

			numDay=0
			if dayInfo is None:							#no day info available yet
				numDay=GetPresenceOfDays(withtags,onerecord.seqcount)
				#print "okay"+str(numDay)+" time "+str(numTime)+" add "+str(numAddress)
			else:										#day from list or dropdown option
				numDay=1
				#print "day found"+str(numDay)+" time "+str(numTime)+" add "+str(numAddress)
			if "Burnsville Group".lower() in initialPage[pattern.start:pattern.end].lower():
				print onerecord.seqstring+" time"+str(numTime)+" day"+str(numDay)+" address"+str(numAddress)

			if numTime>0.2 and numAddress>0.2 and numDay!=1 and numDay>0.4:			#day found in record itself
				print "day in record"
				'''target.write(initialPage[pattern.start:pattern.end])
				target.write("<br>")'''
				ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],"","","")
				#HighlightMeeting(pattern,initialPage,allelemdictionary,browser)
				#mPos=FindMeetingXY(pattern,initialPage)
			elif numTime>0.2 and numAddress>0.2 and numDay==1:						#day foud in list or dropdown beforehand
				'''target.write(initialPage[pattern.start:pattern.end])
				target.write("<br>")'''
				#print "day in list"+dayInfo
				ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],dayInfo,"","")
				#HighlightMeeting(pattern,initialPage,allelemdictionary,browser)
				#mPos=FindMeetingXY(pattern,initialPage)
			elif numTime>0.2 and numAddress>0.2 and numDay<0.4:						#day not in record, so search nearby
				dayInfo2=GetMissingDay(initialPage[0:pattern.start-1])
				print "day nearby"+dayInfo2
				#HighlightMeeting(pattern,initialPage,allelemdictionary,browser)
				ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],dayInfo2,"","")


allelemdictionary={}
def CreateAllElementsKey():
	print "starting"
	for e in browser.find_elements_by_xpath("//*"):
		content=browser.execute_script("return arguments[0].textContent", e)

		filtered_elemtext=filter(lambda x: x in string.printable, content)
		filtered_elemtext="".join(filtered_elemtext.split())
		filtered_elemtext=filtered_elemtext.replace(" ","").lower()
		allelemdictionary.update({filtered_elemtext:e})
		browser.execute_script("arguments[0].id='"+filtered_elemtext.replace("'","")+"'", e)
	print "ending"



readMeetingURLs()

'''loads all the meeting web pages, find out if dropdown/link of days are available, clicks through all of them'''
for oneURL in meetingURLArr:
	print "url:"+oneURL.urlString
	browser.get(oneURL.urlString)#("http://www.aalakesumter.com/meetings.html")
#("http://www.louisvilleaa.org/FindAMeeting.php")
#doesnt work have to check why("http://www.bluegrassintergroup.org/lexington-meetings-sunday")
#("http://www.aa-iowa.org/index.php?id=103")
#("http://www.aadesmoines.org/Sunday.html")
#("http://www.aadesmoines.org/schedule.htm")
#does not work("http://www.aa-waterloo.org/all-meetings.html")#("http://www.aa-cedarrapids.org/meetings/")
#("https://www.aaneok.org/meetings-V3.php")#("http://www.aadistrict1.org/page7.php")
#("http://aaminneapolis.org/meetings/?d=any&v=list")#(oneURL.urlString)
#"http://aaminneapolis.org/meetings/?d=any&v=list"
	formfound=FindFormWithDaysIfAvailable()
	listfound=FindListWithDaysIfAvailable()
	if formfound:									#if there is a form with dropdown option of all days
		forms=browser.find_elements_by_tag_name("form")
		dropdowns=forms[formfound.formelement].find_elements_by_tag_name("select")
		options=dropdowns[formfound.dropdownelement].find_elements_by_tag_name("option")
		for indexoption in range(0,len(options)-1):
			dayinfo=options[indexoption].text#get_attribute("value")
			options[indexoption].click()

			browser.execute_script("arguments[0].target = '_self';", forms[formfound.formelement])
			forms[formfound.formelement].submit()


			#CreateAllElementsKey()




			totalNumOfMeetings=0
			expected=GetTotalTime(RemoveHTMLTags(browser.page_source))
			LoadPagesAndRunPD(dayinfo)

			writer.writerow( (browser.current_url,totalNumOfMeetings,expected) )

			browser.execute_script("window.history.go(-1)")		#select one option, submit the form, find meeting, when done come back to the form page
			forms=browser.find_elements_by_tag_name("form")
			dropdowns=forms[formfound.formelement].find_elements_by_tag_name("select")
			options=dropdowns[formfound.dropdownelement].find_elements_by_tag_name("option")

	elif len(listfound)>0:
		lis=browser.find_elements_by_tag_name("li")
		for indexoption in range(0,len(listfound)-1):
			try:
				element=lis[listfound[indexoption]].find_element_by_tag_name("a")
				if elem:
					dayinfo=element.get_attribute("innerHTML")
					browser.execute_script("arguments[0].target = '_self';", element)
					browser.execute_script("arguments[0].click();", element)

					#CreateAllElementsKey()
					totalNumOfMeetings=0
					expected=GetTotalTime(RemoveHTMLTags(browser.page_source))
					LoadPagesAndRunPD(dayinfo)

					writer.writerow( (browser.current_url,str(totalNumOfMeetings),str(expected)) )

					browser.execute_script("window.history.go(-1)")
					lis=browser.find_elements_by_tag_name("li")

			except:
				continue
	else:
		print "in else"
		#CreateAllElementsKey()
		totalNumOfMeetings=0
		expected=GetTotalTime(RemoveHTMLTags(browser.page_source))
		LoadPagesAndRunPD(None)

		writer.writerow( (browser.current_url,str(totalNumOfMeetings),str(expected)) )
	#break
	alreadyMeetingsIndices=[]
