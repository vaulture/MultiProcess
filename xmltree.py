import os 
import xml.etree.ElementTree as ET
from pprint import pprint
import pdb


class Fsscan():

	def __init__(self):
		self.clist = []
		self.tableoftables = {}	
		self.dl = ','
		self.fsfunctions = ({1:"self.clist.extend([kwargs['item'],kwargs['item'].name,kwargs['item'].path])",
		2:"self.xmlparser(kwargs['item'].path,None)",3:"self.filestatistics(kwargs['item'])",
		4:"self.findfiles(kwargs['item'].path,kwargs['Ikeywords'],kwargs['endonly'])",5:"self.findXinfile(kwargs['item'],kwargs['Ikeywords'],kwargs['alone'])",
		6:"self.xmlparser(kwargs['item'],None)"} )
		
		
		#x = self.filesystemscan_recursive(r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V\Assets\Gameplay\XML\Units")
		#x = self.onefile(r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V\Assets\Gameplay\XML\Units\CIV5Controls.xml")
		#pprint(self.tableoftables.keys()) #returns top-level keys
		#pprint(self.tableoftables) # returns tablenames, columns, and data
		
		#self.writetabletofile(r"C:\Users\Chris\Desktop\test.txt",None)
		#self.writetabletofile(None,r"C:\Users\Chris\Desktop")
		
		#	print(self.clist)	

	def filesystemscan_recursive(self,dir_root,index):		
		for item in os.scandir(dir_root):
			if item.is_dir():
				self.filesystemscan_recursive(item.path,index=index)
			else:
				#pdb.set_trace()
				self.filesystemfunctions(item = item, index = index, Ikeywords = '<GameData>', alone = 1)

					
		
	def onefile(self,file,index):
		self.filesystemfunctions(item = file, index = index, Ikeywords = '<GameData>', alone = 1)
	
	def filesystemfunctions(self,**kwargs):
		exec(self.fsfunctions[kwargs['index']])
			
			
# you should pass a raw filepath to this function
	def xmlparser(self,file,iterkeyword):
		try:
			xmlobj = ET.parse(file)
		except ET.ParseError as error:
			print(error.position)
		else:
			#self.xmlseperator(xmlobj)
			self.xmlseperatortable(xmlobj)

				
				
# you should pass an ElementTree object to this function	
	def xmlseperator(self,xmlobj):
		found = 0
		self.tags = ['Type','Row']
		try:
			for item in xmlobj.iter(): # loop through the ElementTree, each element
				if self.xmltagcheck(item,self.tags): # check if the element's tag is in list (self.includetags)
					if ((item.tag != 'Row') and (found == 0)):
						print(item.tag,item.text,item.attrib)
					elif (item.tag == 'Row' and found == 0):
						found = 1
					else:
						print(item.tag,item.text)
				else:
					pass
		except:
			print('there was an error')
	

	
# you should pass an ElementTree object to this function	
	def xmlseperatortable(self,xmlobj):
		columns = ['GameData','Row','Text','Column'] # ignore these elements
		
		for item in xmlobj.iter(): # loop through the ElementTree, each element
					
			if self.xmltagcheck(item,'Table'): # if it's a table, then combine table and columns into dictionary
				table = {}
				count = 0
				tmpcols = {}
									
				for childitem in item.iter():  # each column in the table
					if childitem == item:  # item.iter() will pull the table entry again
						pass
					else:
						count += 1
						tmpcols.update({('column'+str(count)):childitem.attrib})
						if not childitem.get('name') in columns:
							columns.append(childitem.get('name'))  #make a list of already used columns
						else:
							pass
							
				table.update({'tablename':item.get('name'),'columns':tmpcols,'data':{}})
				self.tableoftables.update({item.get('name'):table})

					
			elif not self.xmltagcheck(item,columns):  # if it's not a table (from the IF above) and not a column
		
				if item.tag in self.tableoftables.keys():  # if this element is the name of a table
					
					tmpdata = {}

					for childitem in item.iter():
						#print(childitem.tag)
						if not self.xmltagcheck(childitem,'Row'):
							tmpdata.update({childitem.tag:childitem.text})
					#print(tmpdata)
					table = self.tableoftables[item.tag]
					table.update({'tablename':table['tablename'],'columns':table['columns'],'data':tmpdata})
					self.tableoftables.update({table['tablename']:table})
					
		
			
				else:
					pass

				
			else:
				pass
				
				
					
	
		
# because .iter() can only take one keyword, check if element's tag is in list	
	def xmltagcheck(self,xmlelement,tags):
		if xmlelement.tag in tags:
			return 1
		else:
			return 0
		
	
	def filestatistics(self,dirobj):
			statobject = dirobj.stat()
			# for i in statobject:
				# print(i) 
				
			# if you know which item, you can use the index like statobject[index]
			# https://docs.python.org/3.6/library/os.html#os.stat_result
			# example : statobject.st_ctime
	
# same as filesystemscan_recursive with os.scandir(), but doesn't drop into each directory 

	def filesystemscan(self,clist,dir_root):
		if clist is None:
			clist = []
		else:
			clist = clist
		
		for item in os.scandir(dir_root):
			self.clist.extend([item,item.name,item.path])
			self.xmlparser(item.path,None)

	def filesystemscan_recursiveNC(self,clist,dir_root):
		if ((clist is None) | (clist == '')):
			clist = []
		else:
			clist = clist
		
		for item in os.scandir(dir_root):
			if not item.is_file():
				self.filesystemscan_recursiveNC(clist,item.path)
			else:
				clist.extend([item])
				
		pprint.pprint(clist)		

	
	
	def gettable(self,tablename):
		return self.tableoftables[tablename]
	
	def getcolumndata(self,table,tablename,columnname):
		if table is None:
			table = self.tableoftables[tablename]
			return table[columnname]
		else:
			return table[columnname]
			
			
	def settable(self,tablename,newdata):
		self.tableoftables.update({tablename:newdata})
		
	def setcolumn(self,table,tablename,columnname,newdata):
		if table is None:
			self.tableoftables.update({tablename:{columnname:newdata}})
		else:
			self.tableoftables.update({table['tablename']:{columnname:newdata}})
	
	
	def writetabletofile(self,filepath,filedir):
		if filedir is None:
			with open(filepath,'w') as f:
				self.writer(f)
		else:
			filepath = os.path.join(filedir,'tableoutput.txt') # could import datetime and include current time
			with open(filepath,'w') as f:
				self.writer(f)
			
	def writer(self,f):
		f.write('tablename'+self.dl+'columnname'+self.dl+'columndata'+'\r\n')
		for tablename in self.tableoftables:
			for column in self.tableoftables[tablename]['columns']:
				columnname = self.tableoftables[tablename]['columns'][column]['name']
				try:
					columndata = self.tableoftables[tablename]['data'][columnname]
				except:
					columndata = 'no data'
				
				if columndata == None:
					columndata = 'no data'
				
				f.write((tablename + self.dl + columnname + self.dl + columndata + '\r\n'))		
			
	
	def findfiles(self,file,keywords,endonly):
		if endonly is not 1:
		# this means you can include even if the keyword is only part of a word
			for keyword in keywords.split(self.dl):
				if file.find(keyword) != -1:
					print(file)
				else:
					print(keyword + ' not in this name')
			
			
		else:
			# this method counts the length of the extension and pulls that from the right-to-left of Filepath string
			for keyword in keywords.split(self.dl):
				kwlen = len(keyword)
				if file[-kwlen:] == keyword:
					print(file)
				else:
					print(keyword + ' not in this name')
			
	# this is unreliable as there may actually be a period earlier on in the file		
			# periodindex = file.find('.')
			# # this means the keyword must be the whole word
			# # check if the previous and next character are space
			# for keyword in keywords.split(self.dl):
				# if not file.find(keyword,periodindex) == -1 : 
					# print(file)
				# else:
					# print(keyword + ' not in this name')
	
		
	def findXinfile(self,file,keywords,alone):
		with open(file,'r') as f:
			for line in f:
				for keyword in keywords.split(self.dl):
					if alone is not 1:
					# this means you can include even if the keyword is only part of a word
						if line.find(keyword) != -1:
							print(keyword,self.dl,line,self.dl,file)
						else:
							print(keyword + ' not found this line')
					else:
						keywordstart = line.find(keyword) 
						#pdb.set_trace()
						if ((keywordstart != -1) and ((keywordstart == 0) or (line[keywordstart-1] == ' ')) and ((line[keywordstart+len(keyword)] == ' ') or (line[keywordstart+len(keyword)] == '\n'))):
							print(keyword,self.dl,line)
						else:
							pass
							#print(keyword + ' not found this line')
					# this means the keyword must be the whole word
					# check if the previous or next character are space
			
			
make = Fsscan()
#pprint(make.clist)===