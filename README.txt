README.TXT

Name: Zachary Munro
Date: April 12, 2018
Problem Set 3: Behavior Tree 
Language: Python 3



	* * * * * * * * * * * * * * * * IMPORTANT: OUTPUT FUNCTIONALITY * * * * * * * * * * * * * * *   
	* In order to run this program such that it outputs a string saying what node it is in each *
	* time it enters a new node, run with command argument -i                                   *
	* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

Functionality of Program:
	- behavior_tree.py is an implementation of a behavior tree that is meant to replicate the
		basic decision making patterns of a Roomba robot. 

	- Due to the nature of the behavior tree, there are some design flaws with the Behavior 
		Tree asked to be implemented but the tree was implemented exactly as was described in
		the documentation provided. These issues include:
			1. The Battery Check condition inside the Until Fail operator sub-tree will never
				return Failure since the battery will have already been checked beforehand
			2. The Done General task will never execute since Until Fail will never receive 
				a Failure from its child Sequence node

	- The Behavior Tree is implemented as a directed, acyclic graph. Each node is an instance
		of a class data structure that was built specifically for that type of node. 
		Ex: the CLEAN SPOT class is instantiated twice since it occurs twice within the tree. 

	- The Blackboard for the program is an instance of a Blackboard class and has a global scope

	- The tree takes values to be stored in the Blackboard as its initial input.
		1. Battery Level (positive integer)
		2. Spot (True/False)
		3. General (True/False)
	- If you select to use Default Inputs when running program, they will be: 
		Battery:100  -  Spot:False  -  General:False
	- Dusty Spot has a 90% chance to be False each time program runs, and each iteration after
		it is cleaned
	

	Known Design Flaws: 
		- Global variables are used too often. I'm new to Python, give me a break.