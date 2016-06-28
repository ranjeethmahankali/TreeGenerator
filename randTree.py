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
		for ch in self.child:
			rs.AddLine(self.pos, ch.pos)
			ch.renderSubTreeWF()
	
	def deepestChild(self, depth = 0):			
		if len(self.child)  ==  0:
			return [self,depth]
		else:
			maxDepth = depth
			deepChild = self
			for ch in self.child:
				childDepth = ch.deepestChild(1+depth)
				if maxDepth < childDepth[1]:
					maxDepth = childDepth[1]
					deepChild = childDepth[0]
				
			return [deepChild,maxDepth]
			
	def UnfDeepestChild(self, depth = 0):			
		if len(self.child)  ==  0:
			return [self,depth]
		else:
			maxDepth = depth
			deepChild = self
			for ch in self.child:
				if ch.isDone == True:
					continue
				childDepth = ch.deepestChild(1+depth)
				if maxDepth < childDepth[1]:
					maxDepth = childDepth[1]
					deepChild = childDepth[0]
				
			return [deepChild,maxDepth]

def randomPt(x1,x2,y1,y2,z1,z2):
	px = random.uniform(x1,x2)
	py = random.uniform(y1,y2)
	pz = random.uniform(z1,z2)
	
	return [px,py,pz]
	
def grow(num):
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
deepCh = root.deepestChild()
rs.AddPoint(deepCh[0].pos)
print(deepCh)

rs.EnableRedraw(True)