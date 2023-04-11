from math import sqrt
import math
import random
import matplotlib.pyplot as plt
import functools
from lab1 import checkPointOnTheLine

class Point:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.pos = 0

  def __init__(self, x, y, pos):
    self.x = x
    self.y = y
    self.pos = pos

  def input(self):
    self.x = float(input())
    self.y = float(input())

  def equals(self, other):
    return self.x == other.x and self.y == other.y
  
class Vector:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  @staticmethod
  def getNormalVector(x, y):
    return Vector(y, -x)

  @staticmethod
  def scalarProduct(v1, v2):
    return v1.x * v2.x + v1.y * v2.y

  def getLen(self):
    return sqrt(self.x ** 2 + self.y ** 2)

  def mult(self, koef):
    self.x *= koef
    self.y *= koef
    return self

  def __sub__(self, other):
    self.x -= other.x
    self.y -= other.y
    return self

def generatePoints(n):
  points = [Point(random.random() * 500, random.random() * 500, i) for i in range(0, n)]
  return points

def addPositions(points):
  i = 0
  for point in points:
    point.pos = i
    i += 1
  return points

def angleBetweenVectors(vect1, vect2):
  return math.acos(Vector.scalarProduct(vect1, vect2) / (vect1.getLen() * vect2.getLen()))

def sortPoints(points):
  sortedPoints = points.copy()
  return sorted(sortedPoints, key=lambda point: point.y)

def findNearestPoint(points, p1, p2):
  maxAngle = -1
  maxPos = -1
  for i, point in enumerate(points):
    v1 = Vector(point.x - p1.x, point.y - p1.y)
    v2 = Vector(point.x - p2.x, point.y - p2.y)
    if not ((point.x == p1.x and point.y == p1.y) or (point.x == p2.x and point.y == p2.y)):
      angle = angleBetweenVectors(v1, v2)
      if angle > maxAngle:
        maxAngle = angle
        maxPos = i
  return maxPos

def firstStep(points, tri):
  maxPos = findNearestPoint(points, points[0], points[1])
  trianglePos = [points[0].pos, points[1].pos, points[maxPos].pos]
  tri.append(trianglePos)
  triangulation(points, points[0], points[maxPos], tri)
  triangulation(points, points[maxPos], points[1], tri)
  return tri

def doExist(arr, tri):
  flag = False
  for item in tri:
    if item[0] == arr[0] and item[1] == arr[1] and item[2] == arr[2]:
      flag = True
  return flag


def triangulation(points, point1, point2, tri):
  highPoints = []

  for point in points:
    if checkPointOnTheLine(point1, point2, point)["title"] == "Левее":
      highPoints.append(point)

  if len(highPoints):
    point = findNearestPoint(highPoints, point1, point2)
    triangle = [point1.pos, point2.pos, highPoints[point].pos]
    if not doExist(triangle, tri):
      tri.append(triangle)
      triangulation(points, point1, highPoints[point], tri)
      triangulation(points, highPoints[point], point2, tri)

def draw(points):
  points_y = []
  points_x = []
  for p in points:
    points_x.append(p.x)
    points_y.append(p.y)
  plt.scatter(points_x, points_y)
  plt.show()

def drawPolygon(points):
  n = len(points)
  for i in range(0, n - 1):
    plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y], color="black")
  plt.plot([points[n - 1].x, points[0].x], [points[n - 1].y, points[0].y], color="black")


if __name__ == "__main__":
  n = 20
  points = generatePoints(n)

  points = sortPoints(points)

  points = addPositions(points)

  triangle = firstStep(points, [])

  for i in triangle:
    polygon = map(lambda x: points[x], i)
    polygonList = list(polygon)
    drawPolygon(polygonList)

  draw(points)