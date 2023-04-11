import random
import math
from matplotlib import pyplot as plt
from celluloid import Camera

fig = plt.figure()
camera = Camera(fig)
ax = fig.gca

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

    @staticmethod
    def reflectedVector(a: Point, p1: Point, p2: Point):
        b = Point(p2.x - p1.x, p2.y - p1.y)
        result = b
        product = ((a * b) / (b * b)) * 2
        result.x *= product
        result.y *= product
        return result - a

    @staticmethod
    def vectorsList(length):
        vectors = []
        for i in range(length):
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
            while p.x == 0 and p.y == 0:
                p = Point(random.randint(-1, 1), random.randint(-1, 1))
            vectors.append(p)
        return vectors

def getX(points: list):
    return [point.x for point in points]

def getY(points: list):
    return [point.y for point in points]
class Polygon:
    def __init__(self, points, name):
        self.points = points
        self.name = name

        self.points.append(self.points[0])

    def draw_polygon(self, color):
        # Вывод точки
        for i in range(len(self.points) - 1):
            plt.plot(self.points[i].x, self.points[i].y, marker="o", color=color)

        plt.plot(getX(self.points), getY(self.points), color=color)

def generatePoints(n):
    points = [Point(random.random() * n, random.random() * n) for p in range(0, 10)]
    return points

def distance(p1: Point, p2: Point):
    return math.sqrt(abs((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y)))

def bruteForce(points, n):
    minDistance = float("inf")
    for i in range(n):
        for j in range(i + 1, n):
            if distance(points[i], points[j]) < minDistance:
                minDistance = distance(points[i], points[j])
    return minDistance

def stripClosest(strip, size, d):
    minDistance = d

    for i in range(size):
        for j in range(i + 1, size):
            if (strip[j].y - strip[i].y) >= minDistance:
                break
            if distance(strip[i], strip[j]) < minDistance:
                minDistance = distance(strip[i], strip[j])
    return minDistance

def closestPairAlgorithm(pointsX, pointsY):
    n = len(pointsX)
    if n <= 3:
        return bruteForce(pointsX, n)
    mid = n // 2
    midPoint = pointsX[mid]
    dl = closestPairAlgorithm(pointsX[0:mid], pointsY)
    dr = closestPairAlgorithm(pointsX[mid:], pointsY)
    d = min(dl, dr)
    strip = []
    for i in range(n):
        if abs(pointsX[i].x - midPoint.x) < d:
            strip.append(pointsX[i])
    return min(d, stripClosest(pointsY, len(strip), d))

def getClosestPairIndexes(points, diameter):
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if distance(points[i], points[j]) == diameter:
                return [i, j]

def pointloc(points, p0):
    n = len(points)
    if rotate(points[0], points[1], p0) > 0 or rotate(points[0], points[n - 1], p0) < 0:
        return True

def isPointInside(points, p):
    start = 0
    end = len(points) - 1
    if (pointloc(points, p)):
        return False
    while (end - start > 1):
        sep = math.floor((end + start) / 2)
        if (rotate(points[0], points[sep], p) > 0):
            end = sep
        else:
            start = sep
    if rotate(points[start], points[end], p) < 0:
        return True
    else:
        return False

def det(a, b, c, d):
    return a * d - b * c

def rotate(p1, p2, p0):
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return -1  # Точка левее прямой
    elif d < 0:
        return 1  # Точка правее прямой
    else:
        return 0  # Точка лежит на прямой

def doIntersect(p1, p2, p3, p4):
    d1 = ((p4.x - p3.x) * (p1.y - p3.y) - (p1.x - p3.x) * (p4.y - p3.y))
    d2 = ((p4.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p4.y - p3.y))
    d3 = ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y))
    d4 = ((p2.x - p1.x) * (p4.y - p1.y) - (p4.x - p1.x) * (p2.y - p1.y))

    if d1 * d2 <= 0 and d3 * d4 <= 0:
        return True
    else:
        return False

def getIntersectedEdge(p1, p2, points):
    for i in range(len(points) - 1):
        if doIntersect(p1, p2, points[i], points[i + 1]):
            return [points[i], points[i + 1]]
    return []

def startMotion(points: list, n):
    radius = 5
    vectors = Vector.vectorsList(len(points))
    framePoints = [Point(0, 0), Point(0, n), Point(n, n), Point(n, 0)]
    frame = Polygon(framePoints, "frame")
    i = 0
    while i < 70:
        frame.draw_polygon("yellow")
        # Рисуем точки
        for j in range(len(points)):
            circle = plt.Circle((points[j].x, points[j].y), radius, edgecolor="green", facecolor='red')
            plt.gcf().gca().add_artist(circle)

        sortedByX = sorted(points, key=lambda point: point.x)
        sortedByY = sorted(points, key=lambda point: point.y)

        diameter = closestPairAlgorithm(sortedByX, sortedByY)
        closestPairIndexes = getClosestPairIndexes(points, diameter)
        # Рисуем диаметр
        plt.plot([points[closestPairIndexes[0]].x, points[closestPairIndexes[1]].x],
                 [points[closestPairIndexes[0]].y, points[closestPairIndexes[1]].y], "blue")
        camera.snap()

        for j in range(len(points)):
            nextPoint = Point(points[j].x + vectors[j].x, points[j].y + vectors[j].y)
            if not isPointInside(framePoints, nextPoint):
                edges = getIntersectedEdge(points[j], nextPoint, framePoints)
                if len(edges) == 0:
                    continue
                p1Edge = edges[0]
                p2Edge = edges[1]
                vectors[j] = Vector.reflectedVector(vectors[j], p1Edge, p2Edge)

        if diameter <= 2 * radius:
            # Векторы, имеющие противоположные направления
            vectors[closestPairIndexes[0]] = Point(-vectors[closestPairIndexes[0]].x, -vectors[closestPairIndexes[0]].y)
            vectors[closestPairIndexes[1]] = Point(-vectors[closestPairIndexes[1]].x, -vectors[closestPairIndexes[1]].y)
        # Двигаем точку на вектор
        for j in range(len(points)):
            points[j] = points[j] + vectors[j]

        i += 1

def init():
    n = 100
    points = generatePoints(n)
    startMotion(points, n)
    plt.grid(True)
    plt.gca().set_xlim((0, n))
    plt.gca().set_ylim((0, n))
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()

init()