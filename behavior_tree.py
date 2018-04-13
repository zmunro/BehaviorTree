#!/usr/bin/python
from random import *
import sys



global info
info = False

class BlackBoard:
	def __init__(self, Battery_Level, Spot, General, Dusty_Spot):
		self.Battery_Level = Battery_Level
		self.Spot = Spot
		self.General = General
		self.Dusty_Spot = Dusty_Spot
		self.Home_Path = ""
		self.Running_List = []
		self.Running_Node = ""
		self.Run_Counter = 0


GLOB_Dusty = "False"
if (randint(1, 10) > 9):
	GLOB_Dusty = "True"

global BB
BB = BlackBoard(Battery_Level= "False", 
				Spot = "False", 
				General = "False", 
				Dusty_Spot = GLOB_Dusty
				)



class BaseNode:
	def run(self):
		print("BaseNode R")
		return "True"


#################################
#          CONDITIONS           #
#################################

class Condition(BaseNode):
	def run(self):
		print("Condition Run")
		return "True"

class BatteryCheck(Condition):
	def run(self):
		if info: print("in BATTERY_CHECK")
		global BB
		if BB.Battery_Level < 30:
			return "Succeeded"
		else:
			return "Failure"

class General(Condition):
	def run(self):
		if info: print("in GENERAL")
		global BB
		BB.General = "True"
		return "Succeeded"

class Spot(Condition):
	def run(self):
		if info: print("in SPOT")
		global BB
		if (BB.Spot == "True"):
			return "Succeeded"
		else:
			return "Failure"

class DustySpot(Condition):
	def run(self):
		if info: print("in DUSTY_SPOT")
		global BB
		if (BB.Dusty_Spot == "True"):
			return "Succeeded"
		else:
			return "Failure"



#################################
#            TASKS              #
#################################
class Task(BaseNode):
	def run(self):
		if info: print("Task run")
		return "Succeeded"

class CleanSpot(Task):
	def run(self):
		if info: print("in CLEAN SPOT")
		global BB
		BB.Spot = "True"
		return "Cleaning Spot"

class FindHome(Task):
	def run(self):
		if info: print("in FIND HOME")
		global BB
		BB.Home_Path = ["(x1,y1)", "(x2,y2)", "(x3,y3)", "(x4,y5)"]
		return "Found Home Path"

class GoHome(Task):
	def run(self):
		if info: print("in GO HOME")
		global BB
		return "Going home, Path: "+ ''.join(str(e) for e in BB.Home_Path)

class Dock(Task):
	def run(self):
		if info: print("in DOCK")
		global BB
		return "Docking"

class DoneSpot(Task):
	def run(self):
		if info: print("in DONE SPOT")
		global BB
		BB.Spot = "True"
		print("DONE SPOT: Succeeded")
		return "Succeeded"

class DoneGeneral(Task):
	def run(self):
		if info: print("in DONE GENERAL")
		global BB
		BB.DoneGeneral = "True"
		print("DONE GENERAL: Succeeded")
		return "Done General"

class DoNothing(Task):
	def run(self):
		if info: print("in DO NOTHING")
		return "Do Nothing"

class Clean(Task):
	def run(self):
		if info: print("in CLEAN")
		global BB
		return "Cleaning"

#################################
#           DECORATORS          #
#################################

class Decorator(BaseNode):
	def run(self):
		if info: print("Decorator Run")
		return "True"

class UntilFail(Decorator):
	def __init__(self, child_node):
		self.child = child_node

	def run(self):
		global BB
		if info: print("in UNTIL FAIL")
		output = self.child.run()
		if (output == "Running"):
			if(self not in BB.Running_List):		
				BB.Running_List.append(self)
			return "Running"
		elif (output == "Succeeded"):
			BB.Running_Node = self
			BB.Running_List = [self]
			return "Running"
		else: # output is "Failure"
			# clears out running list as nothing should be running now
			if(self in BB.Running_List):
				BB.Running_List.clear()
				BB.Running_Node = ""
			return "Succeeded"

class NotOperator(Decorator):
	def __init__(self, child_node):
		self.child = child_node

	def run(self):
		if info: print("in NOT OPERATOR")
		output = self.child.run()
		if (output == "Succeeded"):
			return "Failure"
		else:
			return "Succeeded"

class Timer20(Decorator):
	def __init__(self, child_node):
		self.child = child_node

	def run(self):
		if info: print("in TIMER20")
		global BB
		if (BB.Running_Node != self): #timer not yet running
			BB.Running_Node = self
			BB.Running_List.append(self)
			BB.Run_Counter = 20
			print(self.child.run() + " ("+ str(BB.Run_Counter) + ")")
			BB.Run_Counter = BB.Run_Counter - 1
			return "Running"
		else: #node already running
			print(self.child.run() + " ("+ str(BB.Run_Counter) + ")")
			BB.Run_Counter = BB.Run_Counter - 1
			if (BB.Run_Counter == 0): #finished running
				BB.Running_Node = ""
				BB.Running_List.clear()
				return "Succeeded"
			else:
				return "Running"

class Timer35(Decorator):
	def __init__(self, child_node):
		self.child = child_node

	def run(self):
		if info: print("in TIMER35")
		global BB
		if (BB.Running_Node != self): #timer not yet running
			BB.Running_Node = self
			BB.Running_List.append(self)
			BB.Run_Counter = 35
			print(self.child.run() + " ("+ str(BB.Run_Counter) + ")")
			BB.Run_Counter = BB.Run_Counter - 1
			return "Running"
		else: #node already running
			print(self.child.run() + " ("+ str(BB.Run_Counter) + ")")
			BB.Run_Counter = BB.Run_Counter - 1
			if (BB.Run_Counter == 0): #finished running
				print("run counter went to 0 ######################")
				BB.Running_Node = ""
				BB.Running_List.clear()
				return "Succeeded"
			else:
				return "Running"


#################################
#          COMPOSITES           #
#################################

class Composite(BaseNode):
	def run(self):
		if info: print("Running Composite")
		return "Succeeded"


class Priority(Composite):
	def __init__(self, child_nodes = []):
		self.children = child_nodes

	def run(self):
		global BB
		if info: print("in PRIORITY")
		for each in self.children:
			output = each.run()
			if (output == "Running"):
				if (self not in BB.Running_List):
					BB.Running_List.append(self)
				return "Running"
			elif (output == "Succeeded"):
				BB.Running_List.clear()
				BB.Running_Node = ""
				BB.Run_Counter = 0
				return "Succeeded"
			elif (output != "Failure"):
				BB.Running_List.clear()
				BB.Running_Node = ""
				BB.Run_Counter = 0
				print(output)
				return "Succeeded"
		BB.Running_List.clear()
		BB.Running_Node = ""
		BB.Run_Counter = 0
		return "Failure"


class Sequence(Composite):
	def __init__(self, child_nodes):
		self.children = child_nodes

	def run(self):
		global BB
		if info: print("in SEQUENCE")
		myIndex = 0
		if (self in BB.Running_List): #will set starting index to its running node
			index = BB.Running_List.index(self)
			node = BB.Running_List[index - 1]
			myIndex = self.children.index(node)

		for each in self.children[myIndex:]:
			output = each.run()
			if (output == "Failure"):
				return "Failure"
			elif (output == "Running"):
				if (self not in BB.Running_List):
					BB.Running_List.append(self)
				return "Running"
			elif (output != "Succeeded"):
				print(output)
		return "Succeeded"


class Selection(Composite):
	def __init__(self, child_nodes):
		self.children = child_nodes

	def run(self):
		global BB
		if info: print("in SELECTION")
		myIndex = 0
		if (self in BB.Running_List): #will set starting index to its running node
			index = BB.Running_List.index(self)
			node = BB.Running_List[index - 1]
			myIndex = self.children.index(node)

		for each in self.children[myIndex:]:
			output = each.run()
			if (output == "Succeeded"):
				return "Succeeded"
			if (output == "Running"):
				if (self not in BB.Running_List):
					BB.Running_List.append(self)
				return "Running"
			if (output != "Failure"):
				print(output)
				return "Succeeded"
		return "Failure"




def ExecuteTree():
	global BB
	if (len(sys.argv) > 1):
		if (str(sys.argv[1]) == "-i"):
			global info
			info = True
	defaults = input ("Use default blackboard input? (Y/N) ")
	if defaults == "N":
		BB.Battery_Level = int(input("Battery Level: "))
		print("Enter: True or False (case sensitive)")
		BB.Spot = input("Spot: ")
		BB.General = input("General: ")
		BB.Dusty_Spot = "False"
		if (randint(1, 10) > 9):
			BB.Dusty_Spot = "True"

	#################################
    #             TREE              #
    #################################
	root = Priority(child_nodes =[
		Sequence(child_nodes = [
			BatteryCheck(), 
			FindHome(), 
			GoHome(), 
			Dock()
		]),
		Selection(child_nodes = [
			Sequence(child_nodes = [
				Spot(),
				Timer20(child_node = CleanSpot()),
				DoneSpot()
			]),
			Sequence(child_nodes = [
				General(),
				Sequence(child_nodes = [
					UntilFail(child_node = 
						Sequence(child_nodes = [
							NotOperator(child_node = BatteryCheck()),
							Selection(child_nodes = [
								Sequence(child_nodes = [
									DustySpot(),
									Timer35(child_node = CleanSpot())
								]),
								Clean()
							])
						])
					),
					DoneGeneral()
				])
			])
		]),
		DoNothing()
	])

	while True:
		# Loop to run tree repeatedly while nodes are "Running"
		output = root.run()
		while (output == "Running"):
			BB.Battery_Level = BB.Battery_Level - 1
			if (BB.Dusty_Spot == "False" or BB.Run_Counter == 0):
				BB.Dusty_Spot = "False"
				if (randint(1, 10) > 9):
					BB.Dusty_Spot = "True"

			output = root.run()
		
		print ("EXIT: "+ output)
		print(" ")

		# Input new Blackboard criteria to run tree again
		proceed = input("Run Tree again? (Y/N)")
		if (proceed == "N" or proceed == "n"):
			break
		elif (proceed == "Y" or proceed == "y"):
			BB.Battery_Level = int(input("Battery Level: "))
			BB.Spot = input("Spot: ")
			BB.General = input("General: ")

			BB.Dusty_Spot = "False"
			if (randint(1, 10) > 9):
				BB.Dusty_Spot = "True"
			BB.Home_Path = ""
			BB.Running_List = []
			BB.Running_Node = ""
			BB.Run_Counter = 0


if __name__ == "__main__":
    ExecuteTree()
