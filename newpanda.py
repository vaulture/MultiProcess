# new panda 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Highest():
	def __init__(self):
		self.x = 1

	def add(self,x,y):
		print(x+y)
	
	allowedfunctions = ['self.add','self.getsupercon',]
	constants = ['string','plus']
	roles = {'id':{},'supervisor':['chris','jill'],'level':[1,2,3,4],'sector':['a','b','c']}
	securedict = {'Roles':roles,'Shifts':['am','pm']}

	
class Middle():
	def __init__(self):
		self.y = 2

class Lowest(Highest,Middle):
	def __init__(self,highest,middle):
		super(Highest,self).__init__()
		#print(self.x)
		super(Middle,self).__init__()
		print(highest.x)
		print(middle.y)
		self.tryfunction('self.add(2,3)')
		self.checksecurity()
		
		
	def add(self,x,y):
		return super().add(x,y)
		
	def getsupercon(self):
		return super().constants		
	

	def checksecurity(self):
		requirements = {'supervisor':'chrfais','level':3}
		self.checkrequirements(requirements)
			
	def checkrequirements(self,requirements):
		securedict = super().securedict
		for type in iter(requirements):
			if not requirements[type] in securedict['Roles'][type]:
				print('user has no security for ' + str(type))
	
	
	def tryfunction(self,f):
		if f.split('(')[0] not in super().allowedfunctions:
			pass
		else:
			exec(f)
		
		mylist = super().allowedfunctions
		for item in enumerate(mylist):
			print(item)
	



	
	
h = Highest()
m = Middle()
l = Lowest(h,m)
