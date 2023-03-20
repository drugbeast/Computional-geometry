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
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

class Vector:
  def __init__(self, p1: Point, p2: Point):
    self.x = p2.x - p1.x
    self.y = p2.y - p1.y
      
  def __mul__(self, other):
    return self.x * other.x + self.y * other.y

  def getLength(self):
    return math.sqrt(self.x * self.x + self.y * self.y)

# генерация точек
def generatePoints():
  points = [Point(random.random() * 10, random.random() * 10) for p in range(0, 20)]
  return points

# генерация векторов движения
def getListOfVectors(length: int):
  vectors = []
  for i in range(length):
    p = Point(random.uniform(-1, 1), random.uniform(-1, 1))
    while p.x == 0 and p.y == 0:
      p = Point(random.uniform(-1, 1), random.uniform(-1, 1))
    vectors.append(p)
  return vectors

fig, ax = plt.subplots(1, 1)
camera = Camera(fig)

# отрисовка точек
def drawPoints(points: list):
  for i in range(len(points)):
    plt.scatter(points[i].x, points[i].y)

# отрисовка оболочки
def drawHull(points: list):
  for i in range(len(points) - 1):
    plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y])

# точки оболочки
def hullPoints(points: list):
  pl = minPoint(points)
  pr = maxPoint(points)
  hullPoints = []

  leftPointsArray = leftPoints(points, pl, pr)
  rightPointsArray = rightPoints(points, pl, pr)

  # добавление точек против часовой стрелки
  hullPoints.append(pl)
  buildHull(leftPointsArray, pl, pr, hullPoints)
  hullPoints.append(pr)
  buildHull(rightPointsArray, pr, pl, hullPoints)

  hullPoints.append(hullPoints[0])
  
  return hullPoints

# нахождение минимальной по х точки
def minPoint(points: list):
  min = points[0]
  for i in range(1, len(points)):
    if(min.x > points[i].x):
      min  = points[i]
  return min


# нахождение максимальной по х точки
def maxPoint(points: list):
  max = points[0]
  for i in range(1, len(points)):
    if(max.x < points[i].x):
      max = points[i]
  return max

# точки левее
def leftPoints(points: list, pl: Point, pr: Point):
  leftPoints = []
  for i in range(len(points)):
    if(checkPointOnTheLine(pl, pr, points[i])["title"] == "Левее"):
      leftPoints.append(points[i])
  return leftPoints

# точки правее
def rightPoints(points: list, pl: Point, pr: Point):
  rightPoints = []
  for i in range(len(points)):
    if(checkPointOnTheLine(pl, pr, points[i])["title"] == "Правее"):
      rightPoints.append(points[i])
  return rightPoints
  
# векторное произведение    
def vectorProduct(p0: Point, p1: Point, p2: Point):
    return math.fabs((p2.x - p1.x) * (p0.y - p1.y) - (p2.y - p1.y) * (p0.x - p1.x))
  
# Quick-Hull     
def buildHull(points: list, pl: Point, pr: Point, hullPoints: list):
  s = points[0]
  maxArea = vectorProduct(pl, pr, s)
  # нахождение максимально удаленной точки
  for i in range(1, len(points)):
    if(vectorProduct(pl, pr, points[i]) > maxArea):
      maxArea = vectorProduct(pl, pr, points[i])
      s = points[i]
  
  s1 = leftPoints(points, pl, s)
  s2 = leftPoints(points, s, pr)
  
  # если есть точки левее pls, то вызываем рекурсию до того момента, пока множество s1 не станет пустым
  if len(s1) != 0:
    buildHull(s1, pl, s, hullPoints)
    hullPoints.append(s)
  else:
    hullPoints.append(s)
  
  # если есть точки левее spr, делаем тоже самое
  if len(s2) != 0:
    buildHull(s2, s, pr, hullPoints)

# нахождение периметра    
def perimeter(points: list):
  perimeter = 0
  for i in range(len(points) - 1):
    perimeter += Vector(points[i], points[i + 1]).getLength()
  perimeter += Vector(points[len(points) - 1], points[0]).getLength()
  return perimeter

# движение точек  
def move(points: list, vectors: list):
  for i in range(len(points)):
    points[i] = points[i] + vectors[i]

# обратные векторы движения
def oppositeVector(vectors: list):
    for i in range(len(vectors)):
        vectors[i] = Point(-vectors[i].x, -vectors[i].y)
    return vectors

# анимирование точек 
def animatePoints(points: list):
  vectors = getListOfVectors(len(points))
  PERIMETER_LIMIT = 100

  count = 0
  while count < 50:
    hullPointsArray = hullPoints(points)

    drawPoints(points)
    drawHull(hullPointsArray)
    camera.snap()

    if perimeter(hullPointsArray) >= PERIMETER_LIMIT:
      vectors = oppositeVector(vectors)
        
    move(points, vectors)
    count += 1
  
if __name__ == "__main__":
  points = generatePoints()
  animatePoints(points)
  animation = camera.animate(blit=False, interval=300)
  animation.save("animation.gif")
  plt.show()