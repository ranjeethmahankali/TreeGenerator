import rhinoscriptsyntax as rs
import math
import random
import time
#created on 14th Jan, 2016

#this function returns a random point in the given volume of space defined by the three parameters(from the origin)
def placePt(xMin,xMax,yMin,yMax,zMin,zMax):
	x = random.uniform(xMin,xMax)
	y = random.uniform(yMin,yMax)
	z = random.uniform(zMin,zMax)
	
	return [x,y,z]

#This is a tree class with all kinds of functions and crap
class tree:
	treeID = None
	#the first number in the list is the height of the tree
	#Second number is the size of the tree in horizontal direction
	size = [3000,3000]
	#this is the lenght of the smallest segment in the tree
	segLength = 2
	#this is the density of the foliage
	folDensity = 1
	treeVol = size[0]*size[1]*size[1]
	twigCount = treeVol*folDensity/(1000*segLength)
	
	#htis function initializes the tree with the given parameters
	def __init__(self, basePt, sz, segL, fD):
		self.size = sz
		self.segLength = segL
		#these lists below have to be initialized inside the __init__ function, or else,
		#they will be initialized as final variables which are shared among all objects of this class
		self.node = [basePt]
		self.twig = []
		self.structure = [[]] #this variable contains the entire tree structure
		
		self.folDensity = fD
		self.treeVol = self.size[0]*self.size[1]*self.size[1]
		self.twigCount = self.treeVol*self.folDensity/(1000*self.segLength)
		#now actually creating the tree in the space
		self.treeID = rs.AddGroup()
		self.grow()
	
	#this function adds a new twig to the tree joining joinNode and newNode
	#this function only adds to the data but not to the actual 3d space
	def addTwig(self, joinNode, newNode):
		joinIndex = self.node.index(joinNode)
		self.structure[joinIndex].append(len(self.node))
		self.node.append(newNode)
		self.structure.append([])
	
	#this function grows the tree completely and stores the data in self.node and self. structure
	def grow(self):
		x1 = self.node[0][0] - (self.size[1]/2)
		x2 = self.node[0][0] + (self.size[1]/2)
		y1 = self.node[0][1] - (self.size[1]/2)
		y2 = self.node[0][1] + (self.size[1]/2)
		z1 = self.node[0][2]
		z2 = self.node[0][2] + self.size[0]
		
		i = 0
		while i < self.twigCount:
			randPt = placePt(x1, x2, y1, y2, z1, z2)
			joinPt = self.node[rs.PointArrayClosestPoint(self.node,randPt)]
			vec = rs.VectorScale(rs.VectorUnitize(rs.VectorSubtract(randPt, joinPt)), self.segLength)
			newPt = rs.PointAdd(joinPt, vec)
			self.addTwig(joinPt, newPt)
			i += 1
	
	#this function renders the tree from teh data stored in the self.structure
	def render(self):
		i = 0
		while i < len(self.node):
			j = 0
			while j < len(self.structure[i]):
				joinPt = self.node[i]
				newPt = self.node[self.structure[i][j]]
				self.twig.append(rs.AddLine(joinPt, newPt))
				j += 1
			
			i += 1
		
		rs.AddObjectsToGroup(self.twig, self.treeID)
	
	#this function deletes the entire tree
	#this essentially uninitializes it so it has to grown again to be rendered
	def delete(self):
		rs.RemoveObjectsFromGroup(self.twig, self.treeID)
		rs.DeleteObjects(self.twig)
		self.node = None

rs.EnableRedraw(False)

newTree = tree([0,0,0], [100,100], 2, 1)
newTree.render()
newTree.delete()

rs.EnableRedraw(True)