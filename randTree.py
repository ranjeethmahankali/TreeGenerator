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
			
	def renderSubTree(self):
		#render the subtree starting at this node
		for ch in self.child:
			rs.AddLine(self.pos, ch.pos)
			ch.renderSubTree()

def randomPt(x1,x2,y1,y2,z1,z2):
	px = random.uniform(x1,x2)
	py = random.uniform(y1,y2)
	pz = random.uniform(z1,z2)
	
	return [px,py,pz]
	
def grow(num):
	if num == 0:
		return 0
	randPt = randomPt(-50,50,-50,50,0,100)
	print(randomPt)
	joinNode = nodeList[rs.PointArrayClosestPoint(ptArray, randPt)]
	joinPt = joinNode.pos
	joinVec = rs.VectorSubtract(randPt, joinPt)
	
	growthVec = rs.VectorUnitize(joinVec)
	newPt = rs.VectorAdd(joinPt, growthVec)
	
	newNode = node(newPt, joinNode)
	grow(num-1)
		
def maxDepth():
	maxD = 0
	nodeNum = None
	for nd in nodeList:
		if len(nd.child) == 0 and not nd.isDone:
			dpth = nd.depth()
			if dpth > maxD:
				maxD = dpth
				nodeNum = nodeList.index(nd)
	
	return [nodeNum, maxD]

rs.EnableRedraw(False)
root = node([0,0,0])

g = grow(100)

#root.renderSubTree()
#this function is the one that has all the problems
def renderTree():
	duplicateNodes = nodeList[:]
	while len(duplicateNodes) > 0:
		ptList = []
		maxD = maxDepth()
		if maxD is None:
			return 0
		ptList.append(nodeList[maxD[0]].pos)
		n = maxD[0]
		while (not nodeList[n].parent is None):
			if not nodeList[n].parent.isDone:
				ptList.append(nodeList[n].parent.pos)
				n = nodeList.index(nodeList[n].parent)
			else:
				break
		
		cur = rs.AddCurve(ptList,1)
		#print(len(duplicateNodes))
		duplicateNodes.remove(nodeList[maxD[0]])
		nodeList[maxD[0]].isDone = True
		

#root.renderSubTree()
renderTree()
rs.EnableRedraw(True)
print('yeah')
wait = input('waiting...')
rs.EnableRedraw(False)
root.renderSubTree()
rs.EnableRedraw(True)