import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
from lab1 import Point, doIntersect, doLieOnSegment, checkPointOnTheLine, isSimple

def isPointInside(points, p0):  
  xmax = points[0].x
  xmin = points[0].x
  ymax = points[0].y
  ymin = points[0].y
  
  for point in points:
    if(point.x > xmax):
      xmax = point.x
    if(point.x < xmin):
      xmin = point.x
    if(point.y > ymax):
      ymax = point.y
    if(point.y < ymin):
      ymin = point.y
      
  if((p0.x < xmin) or (p0.x > xmax) or (p0.y < ymin) or (p0.y > ymax)):
    return False
  
  q = Point(xmin - 1, p0.y)
  count = 0
  points.append(Point(points[0].x, points[0].y))
  for i in range(len(points) - 1):
    if(doIntersect(p0, q, points[i], points[i + 1])):
      if(not (doLieOnSegment(p0, q, points[i + 1])) and (doLieOnSegment(p0, q, points[i])) and not(checkVertices(points[i - 1], points[i], points[(i + 1) % len(points)]))):
        count += 1
      else:
        if(doLieOnSegment(p0, q, points[i])):
          j = i - 1
          while(doLieOnSegment(p0, q, points[j])):
            j -= 1
            if(j < 0):
              j += len(points)
          k = i + 1
          while(doLieOnSegment(p0, q, points[k])):
            k += 1
            if(k >= len(points)):
              k -= len(points)
          if(checkPointOnTheLine(p0, q, points[j])["title"] != "На прямой" and checkPointOnTheLine(p0, q, points[k])["title"] != "На прямой" and checkPointOnTheLine(p0, q, points[j])["title"] != checkPointOnTheLine(p0, q, points[k])["title"]):
            count += 1
          i = k
        else:
          j = i
          while(doLieOnSegment(p0, q, points[j])):
            j -= 1
            if(j < 0):
              j += len(points)
          k = (i + 2) % len(points)
          while(doLieOnSegment(p0, q, points[k])):
            k += 1
            if(k >= len(points)):
              k -= len(points)
          if(checkPointOnTheLine(p0, q, points[j])["title"] != checkPointOnTheLine(p0, q, points[k])["title"]):
            count += 1
          i = k
  points.pop()

  return count % 2 == 1

def checkVertices(point1, point2, point3, ymax):
  newPoint = Point(point1.x, ymax + 1)
  if (checkPointOnTheLine(point1, point2, newPoint)['title'] == checkPointOnTheLine(point3, point2, newPoint)['title']):
    return True
  return False

if __name__ == "__main__":
  points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, 6)]
  while(not isSimple(points)):
    points = [Point(random.randint(1, 11), random.randint(1, 11)) for p in range(0, 6)]
  p0 = Point(random.randint(1, 11), random.randint(1, 11))
  points_2d = [[point.x, point.y] for point in points]
  
  myPolygon = Polygon(points_2d, facecolor='none', edgecolor='black')
  fig, ax = plt.subplots(1, 1)
  
  ax.add_patch(myPolygon)
  
  plt.ylim(0, 15)
  plt.xlim(0, 15)
  
  for index, item in enumerate(points):
    plt.annotate(f'p{index + 1}', (item.x, item.y - 0.15))
    
  plt.scatter(p0.x, p0.y)
  plt.annotate('p0', (p0.x, p0.y))
  
  if(isPointInside(points, p0)):
    plt.title('В многоугольнике')
  else:
    plt.title('Не в многоугольнике')
    
  plt.show()