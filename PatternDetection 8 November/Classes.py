import collections

class PatternString(object):
	patString=None
	start=-1
	end=-1
	corNode=None
	
	def __init__(self, data,s,e,n):
        	self.patString = data
        	self.start = s
		self.end=e
		self.corNode=n


class TreeNode(object):
	tagname=None
	position=-1
	endposition=-1
	subpages=None
	children=None
	parent=None
	def __init__(self, data):
        	self.tagname = data
        	self.children = []
		self.subpages=[]
	
	def add_child(self, obj):
        	self.children.append(obj)
	
	def set_parent(self, obj):
        	self.parent=obj

class Sequence(object):
	seqstring=None
	seqcount=0
	tagnums=0
	
	def __init__(self, data,numoftag):
        	self.seqstring = data
        	self.seqcount=1
		self.tagnums=numoftag

'''this class has the URLs and corresponding cities and # of meetings'''

class URLInfo(object):
	urlString=None
	urlCity=None
	urlNOM=0

	def __init__(self, u,c,n):
		self.urlString = u
		self.urlCity=c
		self.urlNOM=n


'''object of this class will keep track if any form contains dropdown with the days options in a page'''
class FormInfo(object):
	formelement=None
	dropdownelement=None

	def __init__(self, forme,dropdowne):
		self.formelement = forme
		self.dropdownelement=dropdowne

class MeetingInfo(object):
	mDay=None
	mTime=None
	mAddress=None
	mURL=None
	mCity=None
	mHTML=None
	mFirstTag=None
	mPosition=None
	
	def __init__(self, day,time,address,url,city,html,ftag,pos):
		self.mDay=day
		self.mTime=time
		self.mAddress=address
		self.mHTML=html
		self.mURL=url
		self.mCity=city
		self.mFirstTag=ftag
		self.mPosition=pos
		
class Position(object):
	x=-1
	y=-1
	w=-1
	h=-1
	def __init__(self, mx,my,mw,mh):
		self.x=mx
		self.y=my
		self.w=mw
		self.h=mh

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
	return self.fed
       # return ''.join(self.fed)

