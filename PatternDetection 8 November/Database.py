import MySQLdb, csv, sys
from Classes import MeetingInfo,Position

import logging
logging.basicConfig(filename='error_log.log',level=logging.DEBUG)


def InitDatabase():
	conn = MySQLdb.connect (host = "localhost",user = "root", passwd = "br4cruta",db = "AAmeetings",charset='utf8')
	return conn

def InsertMeeting(conn,OneMeeting):
	cur = conn.cursor()
	try:
		cur.execute("""SELECT COUNT(*) FROM meetinginformation WHERE meetingday= %s and meetingtime= %s and meetingaddress = %s""",
		(OneMeeting.mDay,OneMeeting.mTime,OneMeeting.mAddress))

		if cur.fetchone()[0]:
			logging.error('DataBase - nothing in cur')
			return
		cur.execute("INSERT INTO meetinginformation(meetingday,meetingtime,meetingaddress,meetingurl,meetingcity,meetingX,meetingY,meetingwidth,meetingheight,meetingfulltext,meetingxpath) VALUES" + "('" + MySQLdb.escape_string(OneMeeting.mDay) +"','"+ MySQLdb.escape_string(OneMeeting.mTime) +"','"+ MySQLdb.escape_string(OneMeeting.mAddress) +"','"+ OneMeeting.mURL +"','"+ OneMeeting.mCity +"',"+ OneMeeting.mPosition.x +","+ OneMeeting.mPosition.y +","+ OneMeeting.mPosition.w +","+ OneMeeting.mPosition.h +",'"+ MySQLdb.escape_string(OneMeeting.mHTML) +"','"+ OneMeeting.mFirstTag +"')")
		conn.commit()
	except Exception as e:
		logging.error('DataBase - failed to excute cur -> exception: ' + str(e))
		print "exception in db"+str(e)
		conn.rollback()
