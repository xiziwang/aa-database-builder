from classes import PatternString, TreeNode, Sequence, MLStripper, URLInfo



def readPageInString(filename):
	with open (filename, "rb") as myfile:
	    pagetext=myfile.read()

	pagetext=pagetext.lower()
	pagetext=pagetext.replace("<br>"," ")
	pagetext=pagetext.replace("<br/>"," ")
	#pagetext=pagetext.replace("<a","")
	#pagetext=pagetext[500:]
	'''pagetext=pagetext.replace("<abbr>","")
	pagetext=pagetext.replace("</abbr>","")
	pagetext=pagetext.replace("<font","")
	pagetext=pagetext.replace("</font>","")
	pagetext=pagetext.replace("<small","")
	pagetext=pagetext.replace("</small>","")
	pagetext=pagetext.replace("<select","")
	pagetext=pagetext.replace("</select>","")
	pagetext=pagetext.replace("<option","")
	pagetext=pagetext.replace("</option>","")
	pagetext=pagetext.replace("<b>","")
	pagetext=pagetext.replace("</b>","")
	pagetext=pagetext.replace("<i>","")
	pagetext=pagetext.replace("</i>","")
	pagetext=pagetext.replace("<center>","")
	pagetext=pagetext.replace("<hr","")'''
	
	return pagetext


'''function to traverse in level order'''
def traverse(node):	
	traversalstring=""	
	thislevel = [node]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			#print n.tagname+",",
			traversalstring+=n.tagname+","
		
			for c in n.children:
				nextlevel.append(c)
		#print
		traversalstring+="$$"
		thislevel = nextlevel

	return traversalstring


'''same as traverse but print the nodes'''
def traversePrint(node):
	
	thislevel = [node]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			#print n.tagname+",",
			
			for c in n.children:
				nextlevel.append(c)
		#print
		thislevel = nextlevel


'''sets all the immediate subnodes of a node. for each node of the trees, 
traverses all it's child nodes and saves these strings as subpages of the node'''
									
'''this global list contains all the patterns with their start and 
end position to find out text inside the tags'''
def SetSubtrees(rootnode):
	allPatterns=[]	
	thislevel = [rootnode]
	while len(thislevel)>0:
		nextlevel = list()

  		for n in thislevel:
			for c in n.children:
				onenode=traverse(c)

				sNode=PatternString(onenode,c.position,c.endposition,c)
				n.subpages.append(sNode)
				allPatterns.append(sNode)
				nextlevel.append(c)
		thislevel = nextlevel
	
	return allPatterns


'''def printall(rootnode):
	
	traversalstring=""	
	thislevel = [rootnode]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			print n.tagname
			print n.subpages.patString
		
			for c in n.children:
				nextlevel.append(c)
		print
		
		thislevel = nextlevel'''

'''this function finds all the repetitive patterns in the page'''
def FindDuplicates(rootnode):
	taglist=[]									#list to contain specific patterns and their counts	
	stringlist=[]
	maxim=0
	nd=None
	thislevel = [rootnode]
	cnt=0
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			for child in n.subpages:
							
				cnt=taglist.count(child.patString)
				if child.patString not in stringlist:
					stringlist.append(child.patString)
					OneSeq=Sequence(child.patString,child.patString.count("$"))
					taglist.append(OneSeq)
				else:
					for seq in taglist:
						if seq.seqstring==child.patString:
							seq.seqcount+=1
							break
		
			for c in n.children:
				nextlevel.append(c)
		#print
		
		thislevel = nextlevel

	
	for tg in taglist:
		'''if tg.seqcount>2 and tg.seqstring.count(",")>5:
			print tg.seqstring
			print tg.seqcount'''
	return taglist


def FindTags(pagetext,current):
	i=0
	while i < len(pagetext):
		if pagetext[i]=='<' and ((pagetext[i+1]>="A" and pagetext[i+1]<="Z") or (pagetext[i+1]>="a" and pagetext[i+1]<="z")):
			if pagetext[i+1]=="b" and pagetext[i+2]=="r" and pagetext[i+3]==">":
				i=i+4
				continue		
			j=i+1
			tag=""
			while pagetext[j]!=">" and pagetext[j]!=" ":
				tag += pagetext[j]
				j+=1
			#print tag
		
			tagnode=TreeNode(tag)
			tagnode.position=i
			if current:
				current.add_child(tagnode)
				tagnode.set_parent(current)
				current=tagnode

			i=j

		if pagetext[i]=='<' and pagetext[i+1]=="/":
			#print current.tagname
			j=i+2
			endtag=""
			while pagetext[j]!=">":
				endtag += pagetext[j]
				j+=1
			#print "/"+endtag
		
			if current:		
				current.endposition=j+1
				current=current.parent
			i=j

		if pagetext[i]=='/' and pagetext[i+1]==">":
			current.endposition=i		
			i=i+1
			current=current.parent
		i += 1

