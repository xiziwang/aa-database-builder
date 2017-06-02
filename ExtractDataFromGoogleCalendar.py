from selenium import webdriver
import string

# called by main function to extract meeting info from a google calendar
# search for any events hold in the period from start_date to end_date
def extract_from_google_calendar(url,start_date,end_date):
	driver = webdriver.PhantomJS()
	driver.get(url)
	# type 1 (use calendar is contained in iframe directly)
	search_for_possible_iframes(driver,start_date,end_date)
	# type 2 (a iframe contains another iframe)
	list_of_frames = driver.find_elements_by_tag_name("iframe")
	for frame in list_of_frames:
		try:
			driver.switch_to_frame(frame)
			search_for_possible_iframes(driver,start_date,end_date)
		except:
			print("Error: failed to switch to the frame")	
	driver.quit()

# for each iframe, identify if it is a google calendar
def search_for_possible_iframes(driver,start_date,end_date):
	google_calendar_list = driver.find_elements_by_xpath("//iframe[contains(@src,'google.com/calendar/embed?')]")

	# find if this page contains google calendar (a or b type)
	if len(google_calendar_list) > 0:
		# for each type a google calendar, 
		for google_calendar in google_calendar_list:
			info = google_calendar.get_attribute("src")
			two_parts = info.split("?")
			info = two_parts[1]
			extract_data(info,start_date,end_date)

# extract meeting info from a google calendar
def extract_data(info,start_date,end_date):
	list_of_para = info.split("&")
	calendar_iframe_url = "https://calendar.google.com/calendar/htmlembed?mode=AGENDA"

	for para in list_of_para:
		para_detail = para.split("=")
		if para_detail[0]=="src":
			calendar_iframe_url += "&src=" + para_detail[1]
	calendar_iframe_url += "&dates=" + start_date + "/" + end_date

	# nevigate to the google calendar and extract data
	driver = webdriver.PhantomJS()
	driver.get(calendar_iframe_url)

	list_of_event = driver.find_elements_by_xpath("//a[contains(@class, 'event-link')]")
	list_of_event_url = []
	# get the list of event
	for event in list_of_event:
		list_of_event_url.append(str(event.get_attribute("href")))
	# access to each event and save the data
	for event_url in list_of_event_url:
		driver.get(event_url)
		print("-------------")
		try:
			name = driver.find_element_by_xpath("//h3").text
			print("name: " + name)
		except:
			print("name: NOT FOUND")
		try:
			time = str(driver.find_element_by_xpath("//time[@itemprop='startDate']").get_attribute("datetime")) + " - " + str(driver.find_element_by_xpath("//time[@itemprop='endDate']").get_attribute("datetime"))
			print("time: " + time)
		except:
			print("time: NOT FOUND")
		try: 
			location = driver.find_element_by_xpath("//span[@itemprop='location']/span").text
			print("location: " + location)
		except:
			print("location: NOT FOUND")		

# main function
def main():
	extract_from_google_calendar("http://www.district5959aa.org/meeting-schedule","20170401","20170407")
	# extract_from_google_calendar("http://www.poconointergroupaa.org/Calendar.html","20170401","20170407")
	# extract_from_google_calendar("http://www.aaaustinhispano.org/","20170401","20170407")
	
	# !! failed because this website uses plugin ("http://aaroanoke.org/","20170401","20170407")
    # !! works but need to deal with monthly meetings ("http://www.aavalleyintergroup.org","20170420","20170427")

main() # Invoke the main function
