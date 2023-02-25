import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def pointloc(points, p):
    n = len(points)
    if rotate(points[0], points[1], p) > 0 or rotate(points[0], points[n-1], p) < 0:
        return False

def rotate(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

def isPointInsideConvex(points, p):
    start = 1
    end = len(points) - 1
    if (pointloc(points, p) == False):
        return False
    while (end - start > 1):
        sep = math.floor((end + start) / 2)
        if (rotate(points[0], points[sep], p) > 0):
            end = sep
        else:
            start = sep
    return not doIntersect(points[0], p, points[start], points[end])

def checkPointOnTheLine(p1, p2, p3):
  det = ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y))

  if det == 0 :
    return {'title': 'На прямой', 'flag': True}
  if det > 0 :
    return {'title': 'Левее', 'flag': False}
  if det < 0 :
    return {'title': 'Правее', 'flag': False}

def doLieOnSegment(p1, p2, p3):
  if((p2.x >= min(p1.x, p3.x)) and (p2.x <= max(p1.x, p3.x)) and (p2.y >= min(p1.y, p3.y)) and (p2.y <= max(p1.y, p3.y))):
    return True
  return False

def doIntersect(p1, p2, p3, p4):
    d1 = ((p4.x - p3.x) * (p1.y - p3.y) - (p1.x - p3.x) * (p4.y - p3.y))
    d2 = ((p4.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p4.y - p3.y))
    d3 = ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y))
    d4 = ((p2.x - p1.x) * (p4.y - p1.y) - (p4.x - p1.x) * (p2.y - p1.y))

    if (d1 == d2 == d3 == d4 == 0):
        if (doLieOnSegment(p1, p3, p2) or doLieOnSegment(p1, p4, p2)
                or doLieOnSegment(p3, p1, p4) or doLieOnSegment(p3, p2, p4)):
            return True
        else:
            return False
    else:
        if ((d1 * d2 <= 0) and (d3 * d4 <= 0)):
            return True
        else:
            return False

def isSimple(points):
    intersections = 0
    newPoints = points.copy()
    newPoints.append(points[0])
    for i in range(0, len(points) - 1):
        for j in range(0, len(points)):
            if (doIntersect(points[i], points[i + 1], newPoints[j], newPoints[j + 1])):
                intersections += 1
        if (intersections > 3):
            return False
        intersections = 0

    return True

def isConvex(points):
    products = []
    newPoints = points.copy()
    newPoints.append(points[0])
    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if ((newPoints[j].x == newPoints[i].x and newPoints[j].y == newPoints[i].y) or ((newPoints[j].x == newPoints[i + 1].x and newPoints[j].y == newPoints[i + 1].y))):
                continue
            if (checkPointOnTheLine(newPoints[i], newPoints[i + 1], newPoints[j])['title'] == 'Правее'):
                product = 1
                products.append(product)
            else:
                product = -1
                products.append(product)
    x = all(item > 0 for item in products)
    y = all(item <= 0 for item in products)
    return (x if x == True else y if y == True else False)

def generateSimplePolyPoints(n):
    points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, n)]
    while (not(isSimple(points))):
        points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, n)]
    return points

def checkSimpleInside(convexPoints, simplePoints):
    results = 0
    for i in range(0, len(simplePoints)):
        if (isPointInsideConvex(convexPoints, simplePoints[i])):
            results += 1
    if results == len(simplePoints):
        return True
    else:
        return False

def generateConvexPolyPoints(n, simplePoints):
    points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, n)]
    while (not(checkSimpleInside(points, simplePoints))):
        points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, n)]
    if (isConvex(points)):
        return points
    else:
        return generateConvexPolyPoints(n, simplePoints)

def generatePoints(n):
    points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, n)]
    return points

def main(n, point):
    points = generateSimplePolyPoints(n)
    points_2d = [[point.x, point.y] for point in points]
    simplePoly = Polygon(points_2d, facecolor='none', edgecolor='black')

    pointsConvex = generateConvexPolyPoints(n, points)
    points_2d_convex = [[point.x, point.y] for point in pointsConvex]
    convexPoly = Polygon(points_2d_convex, facecolor='none', edgecolor='blue')

    #pointsSet = generatePoints(n * 5)

    fig, ax = plt.subplots(1, 1)
    ax.add_patch(simplePoly)
    ax.add_patch(convexPoly)
    for index, item in enumerate(points):
        #plt.annotate(f'p{index + 1}', (item.x + 0.2, item.y - 0.6))
        plt.scatter(item.x, item.y, c="red", marker='o')
    for index, item in enumerate(pointsConvex):
        plt.annotate(f's{index + 1}', (item.x + 0.2, item.y - 0.6))
        plt.scatter(item.x, item.y, c="red", marker='o')
    #for index, item in enumerate(pointsSet):
        #plt.annotate(f'p{index + 1}', (item.x + 0.2, item.y - 0.6))
        #plt.scatter(item.x, item.y, c="green", marker='o')

    plt.ylim(0, 15)
    plt.xlim(0, 15)

    plt.show()


point = Point(random.randint(1, 11), random.randint(1, 11))
main(4, point)
