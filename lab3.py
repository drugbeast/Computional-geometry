import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def pointloc(P,A):
    n = len(P)
    if rotate(P[0], P[1], A) > 0 or rotate(P[0], P[n-1], A) < 0:
        return False

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

def rotate(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

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

def checkSimpleInside(convexPoints, simplePoints):
    results = 0
    for i in range(0, len(simplePoints)):
        if (isPointInsideConvex(convexPoints, simplePoints[i])):
            results += 1
    if results == len(simplePoints):
        return True
    else:
        return False

def checkOctan(pointsSet, simplePoints):
    results = 0
    for i in range(0, len(simplePoints)):
        if (not angleOctanTest(pointsSet[i], simplePoints)):
            results += 1
    if results == len(simplePoints):
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

def checkPointOnTheLine(p1, p2, p3):
  det = ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y))

  if det == 0 :
    return {'title': 'На прямой', 'flag': True}
  if det > 0 :
    return {'title': 'Левее', 'flag': False}
  if det < 0 :
    return {'title': 'Правее', 'flag': False}

def generateSimplePolyPoints(n, pointsConvex):
    points = [Point(random.random() * 8, random.random() * 8) for p in range(0, n)]
    while (not(checkSimpleInside(pointsConvex, points))):
        points = [Point(random.random() * 8, random.random() * 8) for p in range(0, n)]
    if (isSimple(points)):
        return points
    else:
        return generateSimplePolyPoints(n, pointsConvex)

def generatePoints(n, pointsConvex, simplePoints):
    points = [Point(random.random() * 8, random.random() * 8) for p in range(0, n)]
    while (not (checkSimpleInside(pointsConvex, points))):
        points = [Point(random.random() * 8, random.random() * 8) for p in range(0, n)]
    if (checkOctan(points, simplePoints)):
        return points
    else:
        return generatePoints(n, pointsConvex, simplePoints)

def oct(p1, p2):
    v = Point(p1.x - p2.x, p1.y - p2.y)
    if (not v.x and not v.y):
        return 0
    if (0 <= v.y < v.x):
        return 1
    if (0 < v.x <= v.y):
        return 2
    if (0 <= v.x < v.y):
        return 3
    if (0 <= v.y <= -v.x):
        return 4
    if (0 <= -v.y <= -v.x):
        return 5
    if (0 < -v.x <= -v.y):
        return 6
    if (0 <= v.x < -v.y):
        return 7
    if (0 < -v.y < v.x):
        return 8
    return 1

def angleOctanTest(point, points):
    newPoints = points.copy()
    newPoints.append(points[0])
    count = 0
    for i in range(0, len(points)):
        deltaI = oct(point, newPoints[i])
        deltaIplus1 = oct(point, newPoints[i + 1])
        dif = deltaIplus1 - deltaI
        if (dif > 4):
            dif = dif - 8
        if (dif < -4):
            dif = dif + 8
        if (dif == 4 or dif == -4):
            d = (newPoints[i].x - point.x) * (newPoints[i + 1].y - point.y) - (newPoints[i + 1].x - point.x) * (newPoints[i].y - point.y)
            if d > 0:
                dif = 4
            if d < 0:
                dif = -4
            if d == 0:
                return False
        count += dif
    if count == 8 or count == -8:
        return True
    elif count == 0:
        return False

def main(n):
    pointsConvex = [Point(1, 1), Point(4, 6), Point(7, 6), Point(7, 3), Point(5, 1)]
    points_2d_convex = [[point.x, point.y] for point in pointsConvex]
    convexPoly = Polygon(points_2d_convex, facecolor='none', edgecolor='blue')

    points = generateSimplePolyPoints(n, pointsConvex)
    points_2d = [[point.x, point.y] for point in points]
    simplePoly = Polygon(points_2d, facecolor='none', edgecolor='black')

    pointsSet = generatePoints(n, pointsConvex, points)

    fig, ax = plt.subplots(1, 1)
    ax.add_patch(convexPoly)
    ax.add_patch(simplePoly)
    for index, item in enumerate(pointsConvex):
        plt.scatter(item.x, item.y, c="blue", marker='o')
    for index, item in enumerate(pointsSet):
        plt.scatter(item.x, item.y, c="green", marker='o')

    plt.ylim(0, 10)
    plt.xlim(0, 10)
    plt.show()

main(5)
