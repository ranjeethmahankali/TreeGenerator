import rhinoscriptsyntax as rs
import math
import random
import time
#created on 14th Jan, 2016

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
	#this is the structure of the tree
	node = []
	twig = []
	
	def __init__(self, basePt, sz, segL, fD):
		self.size = sz
		self.segLength = segL
		self.node.append(basePt)
		self.folDensity = fD
		self.treeVol = self.size[0]*self.size[1]*self.size[1]
		self.twigCount = self.treeVol*self.folDensity/(1000*self.segLength)
		#now actually creating the tree in the space
		self.treeID = rs.AddGroup()
		self.grow()
		rs.AddObjectsToGroup(self.twig, self.treeID)

	#this function adds a given random point to the growth
	#that means extending the growth in the direction of the random point by unit distance
	def addToGrowth(self, pt):
		joinPt = self.node[rs.PointArrayClosestPoint(self.node,pt)]
		vec = rs.VectorScale(rs.VectorUnitize(rs.VectorSubtract(pt, joinPt)), self.segLength)
		newPt = rs.PointAdd(joinPt, vec)
		self.node.append(newPt)
		self.twig.append(rs.AddLine(joinPt, newPt))
	
	def grow(self):
		x1 = self.node[0][0] - (self.size[1]/2)
		x2 = self.node[0][0] + (self.size[1]/2)
		y1 = self.node[0][1] - (self.size[1]/2)
		y2 = self.node[0][1] + (self.size[1]/2)
		z1 = self.node[0][2]
		z2 = self.node[0][2] + self.size[0]
		
		rs.EnableRedraw(False)
		i = 0
		while i < self.twigCount:
			randPt = placePt(x1, x2, y1, y2, z1, z2)
			self.addToGrowth(randPt)
			i += 1
		
		rs.EnableRedraw(True)
	
	def delete(self):
		rs.DeleteObjects(self.twig)
		rs.DeleteGroup(self.treeID)
		self.node = None
		self = None
		
#this function returns a random point in the given volume of space defined by the three parameters(from the origin)
def placePt(xMin,xMax,yMin,yMax,zMin,zMax):
	x = random.uniform(xMin,xMax)
	y = random.uniform(yMin,yMax)
	z = random.uniform(zMin,zMax)
	
	return [x,y,z]

newTree = tree([0,0,0], [100,100], 2, 0.01)
#newTree.delete()
otherTree = tree([10,10,0], [100,100], 2, 0.01)