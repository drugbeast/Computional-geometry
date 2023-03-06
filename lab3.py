import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
from celluloid import Camera

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

# вектор отражения        
def getReflectedVector(a: Point, p1: Point, p2: Point):
        b = Point(p2.x - p1.x, p2.y - p1.y)
        result = b
        product = ((a * b) / (b * b)) * 2
        result.x *= product
        result.y *= product
        return result - a

# список случайных векторов
def getListOfVectors(length):
        vectors = []
        for i in range(length):
            p = Point(random.uniform(-1, 1), random.uniform(-1, 1))
            while p.x == 0 and p.y == 0:
                p = Point(random.uniform(-1, 1), random.uniform(-1, 1))
            vectors.append(p)
        return vectors

# новые координаты точки после прибавления к ней вектора    
def move(movingPoints: list, vectors: list, i):
    movingPoints[i] = movingPoints[i] + vectors[i]

# если внутри простого многоугольника, удаляем данные о точке и векторе
def hasTrapped(p0: Point, v0: Point, movingPoints: list, vectors: list):
    movingPoints.remove(p0)
    vectors.remove(v0)

# проверка на то, лежит точка вне многоугольника
def pointloc(P,A):
    n = len(P)
    if rotate(P[0], P[1], A) > 0 or rotate(P[0], P[n-1], A) < 0:
        return False

# проверка на то, лежит точки внутри выпуклого многоугольника
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

# нахождение ориентации тройки точек
def rotate(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

# функция проверяющая лежит ли точка в отрезке
def doLieOnSegment(p1, p2, p3):
  if((p2.x >= min(p1.x, p3.x)) and (p2.x <= max(p1.x, p3.x)) and (p2.y >= min(p1.y, p3.y)) and (p2.y <= max(p1.y, p3.y))):
    return True
  return False

# функция проверяющая пересечение двух отрезков
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

# проверяет лежит ли простой многоугольник внутри выпуклого
def checkSimpleInside(convexPoints, simplePoints):
    results = 0
    for i in range(0, len(simplePoints)):
        if (isPointInsideConvex(convexPoints, simplePoints[i])):
            results += 1
    if results == len(simplePoints):
        return True
    else:
        return False

# удовлетворяют ли точки угловому тесту через октаны
def checkOctan(pointsSet, simplePoints):
    results = 0
    for i in range(0, len(simplePoints)):
        if (not angleOctanTest(pointsSet[i], simplePoints)):
            results += 1
    if results == len(simplePoints):
        return True
    else:
        return False

# проверка простой ли многоугольник
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

# генерация точек простого многоугольника
def generateSimplePolyPoints(n, pointsConvex):
    points = [Point(random.random() * 8 + 1, random.random() * 8 + 1) for p in range(0, n)]
    while (not(checkSimpleInside(pointsConvex, points))):
        points = [Point(random.random() * 8 + 1, random.random() * 8 + 1) for p in range(0, n)]
    if (isSimple(points)):
        return points
    else:
        return generateSimplePolyPoints(n, pointsConvex)

# генерация точек между выпуклым и простым многоугольниками
def generatePoints(n, pointsConvex, simplePoints):
    points = [Point(random.random() * 8, random.random() * 8) for p in range(0, n)]
    while (not (checkSimpleInside(pointsConvex, points))):
        points = [Point(random.random() * 8, random.random() * 8) for p in range(0, n)]
    if (checkOctan(points, simplePoints)):
        return points
    else:
        return generatePoints(n, pointsConvex, simplePoints)

# функция определяющая в каком октане лежит точка
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

# октановый тест
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


def getIntersectedEdge(p1: Point, p2: Point, points):
    for i in range(len(points) - 1):
        if doIntersect(p1, p2, points[i], points[i + 1]):
            return [points[i], points[i + 1]]
    return []

def main(n):
    pointsConvex = [Point(2, 2), Point(3, 6), Point(5, 8), Point(7, 6), Point(8, 4), Point(6, 2)]

    points_2d_convex = [[point.x, point.y] for point in pointsConvex]
    convexPoly = Polygon(points_2d_convex, facecolor='none', edgecolor='blue')

    points = generateSimplePolyPoints(n, pointsConvex)
    points_2d = [[point.x, point.y] for point in points]
    simplePoly = Polygon(points_2d, facecolor='none', edgecolor='black')

    movingPointsSet = generatePoints(n * 2, pointsConvex, points)
    
    vectors = getListOfVectors(len(movingPointsSet))

    fig, ax = plt.subplots(1, 1)
    camera = Camera(fig)

    plt.ylim(0, 10)
    plt.xlim(0, 10)
    
    while len(movingPointsSet) > 0:
        ax.add_patch(convexPoly)
        ax.add_patch(simplePoly)

        for index, item in enumerate(movingPointsSet):
            plt.scatter(item.x, item.y, c="green", marker='o')
        camera.snap()

        for i in range(len(movingPointsSet)):
            if i >= len(movingPointsSet):
                break

            next_point = Point(movingPointsSet[i].x + vectors[i].x, movingPointsSet[i].y + vectors[i].y)

            # проверка не вышел ли вектор за пределы многоугольника
            while not isPointInsideConvex(pointsConvex, next_point):
                edges = getIntersectedEdge(movingPointsSet[i], next_point, pointsConvex)
                if len(edges) == 0:
                    move(movingPointsSet, vectors, i)
                    continue
                edge_p1 = edges[0]
                edge_p2 = edges[1]

                vectors[i] = getReflectedVector(vectors[i], edge_p1, edge_p2)
                next_point = Point(movingPointsSet[i].x + vectors[i].x, movingPointsSet[i].y + vectors[i].y)

            if angleOctanTest(next_point, points):
                hasTrapped(movingPointsSet[i], vectors[i], movingPointsSet, vectors)
                continue
            move(movingPointsSet, vectors, i)
    
    animation = camera.animate(blit=False, interval=100)
    animation.save("animation3.gif")
    plt.show()

main(5)
