import math
import functools
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
from celluloid import Camera
from lab1 import checkPointOnTheLine

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

class Vector:
    def __init__(self, p1: Point, p2: Point):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y

    def getLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

def generatePoints():
    points = [Point(random.random() * 10, random.random() * 10) for p in range(0, 20)]
    return points

def compare(p1, p2):
    if(p1.y < p2.y):
        return -1
    elif(p1.y > p2.y):
        return 1
    else:
        return 0

def sortPoints(points):
    return sorted(points, key=functools.cmp_to_key(compare))

def getCosine(v1, v2):
    return (v1 * v2) / (v1.getLength() * v2.getLength())

def getArcs(points):
    arcs = []
    s0 = points[0]

    s0vector = Vector(s0, Point(s0.x + 1, s0.y))

    for i in range(1, len(points)):
        v = Vector(s0, points[i])
        arc_value = math.acos(getCosine(v, s0vector))
        arcs.append(arc_value)

    sort(points, arcs, s0)
    return arcs

def sort(points, arcs, s0):
    for i in range(len(arcs)):
        min = i
        for j in range(i + 1, len(arcs)):
            if arcs[min] > arcs[j]:
                min = j
                # если одинаковый полярный угол, оставляем ту, которая дальше
            elif arcs[min] == arcs[j]:
                minVector = Vector(s0, points[min])
                vector = Vector(s0, points[j])
                if vector.getLength() > minVector.getLength():
                    min = j

        arcs[i], arcs[min] = arcs[min], arcs[i]
        points[i + 1], points[min + 1] = points[min + 1], points[i + 1]
        
def buildHull(points):
    arcs = getArcs(points)

    hullPoints = []

    for i in range(0, len(points)):
        while (len(hullPoints) >= 2) and (
                checkPointOnTheLine(hullPoints[-2], hullPoints[-1], points[i])["title"] == "Правее"):
            del hullPoints[-1]
            drawPoints(points)
            drawHull(hullPoints)

        hullPoints.append(points[i])
        drawPoints(points)
        drawHull(hullPoints)

    drawPoints(points)
    hullPoints.append(hullPoints[0])
    drawHull(hullPoints)
    hullPoints.pop()
    
def drawPoints(points):
    for i in range(len(points)):
        plt.scatter(points[i].x, points[i].y)
        
fig, ax = plt.subplots(1, 1)
camera = Camera(fig)
        
def drawHull(points):
    for i in range(len(points) - 1):
        plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y])
    camera.snap()
    
if __name__ == "__main__":
    points = sortPoints(generatePoints())
    drawPoints(points)
    buildHull(points)
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation1.gif")
    plt.show()