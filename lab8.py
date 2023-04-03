import math
import matplotlib.pyplot as plt
from time import sleep
from celluloid import Camera
from lab1 import checkPointOnTheLine, doIntersect

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
  def set_direction(self, vector):
    self.direction = vector[0]
    self.speed = vector[1]
  def move(self):
    self.x += self.direction.x
    self.y += self.direction.y

class Vector:
  def __init__(self, p1: Point, p2: Point):
    if type(p1) == Point:
      self.x = p2.x - p1.x
      self.y = p2.y - p1.y
    else:
      self.x = p1
      self.y = p2
      
  def __mul__(self, other):
    return self.x * other.x + self.y * other.y

  def getLength(self):
    return math.sqrt(self.x * self.x + self.y * self.y)
  
def intersectionType(p1: Point, p2: Point, a: Point, b: Point):
  if((b.x - a.x) * (p2.y - p1.y) - (b.y - b.x) * (p2.x - p1.x)) > 0:
    return 'PP'
  elif ((b.x - a.x) * (p2.y - p1.y) - (b.y - b.x) * (p2.x - p1.x)) < 0:
    return 'PB'
  else:
    return 0
  
def intersectionParameter(p1, p2, a, b):
  normalVector = Vector(p2.y - p1.y, -(p2.x - p1.x))
  return -((Vector(a.x - p1.x, a.y - p1.y) * normalVector)/(Vector(b.x - a.x, b.y - a.y) * normalVector))
  
def cyrusBack(p1, p2, points):
  n = len(points)
  t0 = [0]
  t1 = [1]
  
  for i in range(n):
    typeValue = intersectionType(points[i], points[(i + 1) % n], p1, p2)
    intersectParam = intersectionParameter(points[i], points[(i + 1) % n], p1, p2)
    if(typeValue == 'PB'):
      t0.append(intersectParam)
    if(typeValue == 'PP'):
      t1.append(intersectParam)
    else:
      continue
  
  t0Val = max(t0)
  t1Val = min(t1)
  
  if(t0Val > t1Val):
    return p1, p1
  else:
    x1 = p1.x * (1 - t0Val) + p2.x * t0Val
    y1 = p1.y * (1 - t0Val) + p2.y * t0Val
    x2 = p1.x * (1 - t1Val) + p2.x * t1Val
    y2 = p1.y * (1 - t1Val) + p2.y * t1Val
    
    return Point(x1, y1), Point(x2, y2)
  
def det(p1, p2, p3, p4):
  return (p2.x - p1.x) * (p4.y - p3.y) - (p2.y - p1.y) * (p4.x - p3.x)

# нацеленность
def isAimed(a1, a2, b1, b2):
  areCollinear = checkPointOnTheLine(a1, a2, b1)["flag"] and checkPointOnTheLine(a1, a2, b2)["flag"]

  if areCollinear:
    # если a1a2 и b1b2 не пересекаются и a2, b1 по одну сторону от a1 - нацелен
    if (not doIntersect(a1, a2, b1, b2)) and (checkPointOnTheLine(a1, a2, b1)["title"] == "Правее"):
      return True
  else:
    if det(b1, b2, a1, a2) < 0 and det(b1, b2, b1, a2) > 0:
      return True
    elif det(b1, b2, a1, a2) > 0 and det(b1, b2, b1, a2) < 0:
      return True
  return False

# внешняя ли точка
def isExternal(a2, b1, b2):
  if checkPointOnTheLine(b1, b2, a2)["title"] == "Правее":
    return True
  return False
  
def getIntersectionPoint(p1, p2, p3, p4):
  n = Vector(-(p2.y - p1.y), p2.x - p1.x)
  t = (n * Vector(p3, p1)) / (n * Vector(p3, p4))
  p = Vector(p3, p4)
  return Point(p3.x + t * p.x, p3.y + t * p.y)

def polygonIntersection(P, Q):
  Res = []
  n = len(P)
  m = len(Q)
  p = 0
  q = 0
  # подбираем окно в P относительно фиксированного окна в Q
  for i in range(n):
    if(checkPointOnTheLine(P[i], P[i + 1], Q[0])["title"] == "Правее" or checkPointOnTheLine(Q[0], Q[1], P[i + 1])["title"] == "Правее"):
      p = i
      break
    
  for i in range(2 * (n + m)):
    # если окна нацелены друг на друга
    if isAimed(P[p], P[(p + 1) % n], Q[q], Q[(q + 1) % m]) and isAimed(Q[q], Q[(q + 1) % m], P[p], P[(p + 1) % n]):
      # двигаем внешнее окно
      if isExternal(P[(p + 1) % n], Q[q], Q[(q + 1) % m]):
        p = (p + 1) % n
      else:
        q = (q + 1) % m

    # если p нацелен на q, а q на p не нацелен
    elif isAimed(P[p], P[(p + 1) % n], Q[q], Q[(q + 1) % m]) and not isAimed(Q[q], Q[(q + 1) % m], P[p], P[(p + 1) % n]):
      # если p - не внешнее окно, то добавляем конечную вершину в ответ
      if not isExternal(P[(p + 1) % n], Q[q], Q[(q + 1) % m]):
        Res.append(P[(p + 1) % n])
      # двигаем окно p
      p = (p + 1) % n

    # если q нацелен на p, а p на q не нацелен
    elif not isAimed(P[p], P[(p + 1) % n], Q[q], Q[(q + 1) % m]) and isAimed(Q[q], Q[(q + 1) % m], P[p], P[(p + 1) % n]):
      # если q - не внешнее окно, то добавляем конечную вершину в ответ
      if not isExternal(Q[(q + 1) % m], P[p], P[(p + 1) % n]):
        Res.append(Q[(q + 1) % m])
      # двигаем окно q
      q = (q + 1) % m

    # если окна не нацелены друг на друга
    elif not isAimed(P[p], P[(p + 1) % n], Q[q], Q[(q + 1) % m]) and not isAimed(Q[q], Q[(q + 1) % m], P[p], P[(p + 1) % n]):
      # если окна пересекаются, то добавляем точку пересечения в ответ
      if doIntersect(P[p], P[(p + 1) % n], Q[q], Q[(q + 1) % m]):
        Res.append(getIntersectionPoint(P[p], P[(p + 1) % n], Q[q], Q[(q + 1) % m]))
      # двигаем внешнее окно
      if isExternal(P[(p + 1) % n], Q[q], Q[(q + 1) % m]):
        p = (p + 1) % n
      else:
        q = (q + 1) % m

    # если первая добавленная точка совпала с последней - выход
    if len(Res) > 1 and Res[0] == Res[-1]:
      del Res[-1]
      break

  return Res

def drawPolygon(points):
  n = len(points)
  for i in range(0, n - 1):
    plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y], color="black")
  plt.plot([points[n - 1].x, points[0].x], [points[n - 1].y, points[0].y], color="black")


def drawLine(points, color):
  plt.plot([points[0].x, points[1].x], [points[0].y, points[1].y], color=color)
    
if __name__ == "__main__":
  P = [Point(-5.0, 1), Point(-2, 2.1), Point(-7, 4), Point(-10, 2.1)]
  Q = [Point(16, 3), Point(23, 4), Point(22, 6), Point(16, 7), Point(10, 6), Point(11, 4)]

  # задаем направление и скорость точкам
  speed = 0.4
  for point in P:
    point.set_direction([Vector(speed * 1, 0), speed])
  for point in Q:
    point.set_direction([Vector(speed * -1, 0), speed])
  fig, ax = plt.subplots()
  camera = Camera(fig)
  plt.ion()

  count = 50
  for k in range(0, count):
    # рисуем многоугольники
    drawPolygon(P)
    drawPolygon(Q)
    ax.fill(list(map(lambda p: p.x, P)), list(map(lambda p: p.y, P)), "blue")
    ax.fill(list(map(lambda p: p.x, Q)), list(map(lambda p: p.y, Q)), "orange")

    res = polygonIntersection(P, Q)  # массив точек пересечения многоугольников
    ax.fill(list(map(lambda p: p.x, res)), list(map(lambda p: p.y, res)), "black")

    p0_new, p2_new = cyrusBack(P[0], P[2], Q)
    ([P[0], P[2]], Q)  # концевые точки отсечения отрезка Р0Р2
    drawLine([p0_new, p2_new], "red")

    # делаем шаг анимации
    camera.snap()
    # двигаем многоугольники
    for p1 in P:
      p1.move()
    for p2 in Q:
      p2.move()

    plt.draw()
    plt.gcf().canvas.flush_events()
    sleep(0.00001)

  # сохраняем анимацию
  animation = camera.animate()
  animation.save('animation.gif')
  plt.ioff()
  plt.show()