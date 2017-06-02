from bs4 import BeautifulSoup
import string

def highlight(element,driver):
    """Highlights (blinks) a Selenium Webdriver element"""
    print "highlighting element"
    #driver = element._parent
    print driver

    driver.execute_script("arguments[0].style.background='yellow'",element)
    driver.execute_script("arguments[0].style.border='2px solid red'",element)
    #original_style = element.get_attribute('style')
    #apply_style("background: yellow; border: 5px solid red;")
    #apply_style("border: 5px solid red;")
    #time.sleep(.3)
    #apply_style(original_style)

def HighlightMeeting(pattern,initialPage,keydictionary,browser):

	first_tag=pattern.patString.split(',')[0]
	print "tag"+first_tag
	#print "highlight called:"+pattern.patString

	pagesubstring= initialPage[pattern.start:pattern.end]
	soup=BeautifulSoup(pagesubstring)
	souptext=soup.text
	filtered_soup = filter(lambda x: x in string.printable, souptext)
	filtered_soup="".join(filtered_soup.split())
	filtered_soup=filtered_soup.replace(" ","").lower()
	#print filtered_soup

	elem=keydictionary.get(filtered_soup)

	if elem is not None:
		#print elem.text
		elem=browser.find_element_by_id(filtered_soup.replace("'",""))#browser.find_element_by_xpath("//*[contains(text(), '"+elem.text+"')]")
		highlight(elem,browser)
