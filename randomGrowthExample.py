import rhinoscriptsyntax as rs
import math
import random
#created on 14th Jan, 2016

#this function returns a random point in the given volume of space defined by the three parameters(from the origin)
def placePt(xMin,xMax,yMin,yMax,zMin,zMax):
	x = random.uniform(xMin,xMax)
	y = random.uniform(yMin,yMax)
	z = random.uniform(zMin,zMax)
	
	return [x,y,z]

#this function adds a given random point to the growth
#that means extending the growth in the direction of the random point by unit distance
def addToGrowth(pt, grth):
	joinPt = grth[rs.PointArrayClosestPoint(grth,pt)]
	vec = rs.VectorScale(rs.VectorUnitize(rs.VectorSubtract(pt, joinPt)), stepLength)
	newPt = rs.PointAdd(joinPt, vec)
	grth.append(newPt)
	lines.append(rs.AddLine(joinPt, newPt))

growth = [[0,0,0]]
lines = []
stepLength = 4

rs.EnableRedraw(False)
i = 0
while i < 5000:
	randPt = placePt(-50,50,-50,50,0,100)
	addToGrowth(randPt, growth)
	i += 1

rs.EnableRedraw(True)