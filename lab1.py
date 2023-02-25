import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
def doLieOnSegment(p1, p2, p3):
  if((p2.x >= min(p1.x, p3.x)) and (p2.x <= max(p1.x, p3.x)) and (p2.y >= min(p1.y, p3.y)) and (p2.y <= max(p1.y, p3.y))):
    return True
  return False

def checkPointOnTheLine(p1, p2, p3):
  det = ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y))

  if det == 0 :
    return {'title': 'На прямой', 'flag': True}
  if det > 0 :
    return {'title': 'Левее', 'flag': False}
  if det < 0 :
    return {'title': 'Правее', 'flag': False}

def doIntersect(p1, p2, p3, p4): 
  d1 = ((p4.x - p3.x) * (p1.y - p3.y) - (p1.x - p3.x) * (p4.y - p3.y))
  d2 = ((p4.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p4.y - p3.y))
  d3 = ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y))
  d4 = ((p2.x - p1.x) * (p4.y - p1.y) - (p4.x - p1.x) * (p2.y - p1.y))
  
  if(d1 == d2 == d3 == d4 == 0):
    if(doLieOnSegment(p1, p3, p2) or doLieOnSegment(p1, p4, p2)
      or doLieOnSegment(p3, p1, p4) or doLieOnSegment(p3, p2, p4)):
      return True
    else:
      return False
  else:
    if((d1 * d2 <= 0) and (d3 * d4 <= 0)):
      return True
    else:
      return False
    
def isSimple(points):
  for i in range(len(points) - 2):
    if(i == 0):
      for j in range(i + 2, len(points) - 1):
        if(doIntersect(points[i], points[i + 1], points[j], points[j + 1])):
          return False
    else:
      points.append(points[0])
      for j in range(i + 2, len(points) - 1):
        if(doIntersect(points[i], points[i + 1], points[j], points[j + 1])):
          points.pop()
          return False
      points.pop()
  
  return True

def showSegments(p1, p2, p3, p4):
  if(doIntersect(p1, p2, p3, p4)):
    plt.title('Пересекаются')
  else:
    plt.title('Не пересекаются')
  points = [p1, p2, p3, p4]
  
  plt.plot([p1.x, p2.x], [p1.y, p2.y], '-o', label = 'first segment')
  plt.plot([p3.x, p4.x], [p3.y, p4.y], '-o', label = 'second segment')
  for index, item in enumerate(points):
    plt.annotate(f'p{index + 1}', (item.x, item.y - 0.15))
  plt.legend()
  plt.show()
  
def showFirstTask(p1, p2, p3):
  result = checkPointOnTheLine(p1, p2, p3)
  
  plt.title(result["title"])
  
  plt.arrow(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y, head_width=0.08)

  plt.scatter(p3.x, p3.y)
  plt.show()
  
def showPolygon(points):
  points_2d = [[point.x, point.y] for point in points]
  
  myPolygon = Polygon(points_2d, facecolor='none', edgecolor='black')
  
  fig, ax = plt.subplots(1, 1)
  
  ax.add_patch(myPolygon)
  
  plt.ylim(0, 15)
  plt.xlim(0, 15)
  
  for index, item in enumerate(points):
    plt.annotate(f'p{index + 1}', (item.x, item.y - 0.15))
  
  if(isSimple(points)):
    plt.title('Простой')
    plt.show()
  else:
    plt.title('Не простой')
    plt.show()

points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, 6)]

p1 = Point(random.randint(1, 11), random.randint(1, 11))
p2 = Point(random.randint(1, 11), random.randint(1, 11))
p3 = Point(random.randint(1, 11), random.randint(1, 11))
p4 = Point(random.randint(1, 11), random.randint(1, 11))

# Special case

# x = [1, 4, 2, 5]
# y= [1, 1, 1, 1]

# isSimple(6)
# showFirstTask(p1, p2, p3)
# showSegments(p1, p2, p3, p4)
  