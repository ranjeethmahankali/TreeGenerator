import rhinoscriptsyntax as rs
import random

ptArray = list()
nodeList = list()

class node:
	def __init__(self, position, parent = None):
		self.pos = position
		self.child = list()#this is a list of references to the childnodes of this node
		self.parent = None
		self.index = len(ptArray)
		ptArray.append(self.pos)
		nodeList.append(self)
		
		self.isDone = False
		#this is a oolean which storess whether this has been drawn in the model
		#space as a part of a twig or not
		
		if not parent is None:
			parent.child.append(self)
			self.parent = parent
		
	def depth(self):
		#this method returns the depth of this node in the tree
		#root depth is 0 and leaf depth is maximum
		if self.parent is None:
			return 0
		else:
			return 1+self.parent.depth()
			
	def renderSubTreeWF(self):
		#render the subtree starting at this node
		#but renders just a wireframe
		#WF stands for wireframe
		for ch in self.child:
			rs.AddLine(self.pos, ch.pos)
			ch.renderSubTreeWF()
	
	def deepestChild(self, depth = 0):			
		if len(self.child)  ==  0:
			if self.isDone:
				return [self.parent, 0]
			else:
				return [self,depth]
		else:
			if self.isDone:
				maxDepth = 0
				deepChild = self.parent
			else:
				maxDepth = depth
				deepChild = self
			
			for ch in self.child:
				childDepth = ch.deepestChild(1+depth)
				if maxDepth < childDepth[1]:
					maxDepth = childDepth[1]
					deepChild = childDepth[0]
				
			return [deepChild,maxDepth]
	
	def childDoneStatus(self, ptList = []):
		#this method marks the isDone status of all the nodes of the subtree
		#by marking the done nodes in red and others in blue
		#this method also returns the list of the added point objects
		#so that they can be easily removed
		newPt = rs.AddPoint(self.pos)
		if self.isDone:
			#Add a red Point
			rs.ObjectColor(newPt, (255,0,0))
		else:
			#Add a blue point
			rs.ObjectColor(newPt, (0,0,255))
		
		ptList.append(newPt)
		for ch in self.child:
			ptList = ch.childDoneStatus(ptList)
		
		return ptList
	
	def renderSubTree(self, startRadius, growthFactor, curveDegree):
		while True:
			deepCh = self.deepestChild()
			startNode = deepCh[0]
			if startNode == None:
				#this is the case where the whole tree is rendered
				#later return the group id of the group
				#that contains the whole tree from here
				return True
			
			curNode = startNode
			nodeList = [startNode]
			while (not curNode.parent is None) and (not curNode.isDone):
				nodeList.append(curNode.parent)
				curNode = curNode.parent
			
			posList = []
			i = 0
			while i < len(nodeList):
				posList.append(nodeList[i].pos)
				i += 1
			
			curveId = rs.AddCurve(posList,curveDegree)
			
			for nd in nodeList:
				nd.isDone = True

def randomPt(x1,x2,y1,y2,z1,z2):
	px = random.uniform(x1,x2)
	py = random.uniform(y1,y2)
	pz = random.uniform(z1,z2)
	
	return [px,py,pz]
	
def grow(num):
	#this method grows the global ptArray list
	#this method grows teh pointClooud represented by this list
	if num == 0:
		return 0
	randPt = randomPt(-50,50,-50,50,0,100)
	
	joinNode = nodeList[rs.PointArrayClosestPoint(ptArray, randPt)]
	joinPt = joinNode.pos
	joinVec = rs.VectorSubtract(randPt, joinPt)
	
	growthVec = rs.VectorUnitize(joinVec)
	newPt = rs.VectorAdd(joinPt, growthVec)
	
	newNode = node(newPt, joinNode)
	g = grow(num-1)

rs.EnableRedraw(False)
root = node([0,0,0])

g = grow(20)

root.renderSubTreeWF()
root.renderSubTree(0.1, 1.2, 1)

rs.EnableRedraw(True)