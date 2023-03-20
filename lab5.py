import math
from matplotlib import pyplot as plt
import random
from celluloid import Camera

fig = plt.figure()
camera = Camera(fig)
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

    def getLength (self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

# Функция, рисующая точку
def drawPoint(point: Point):
    plt.scatter(point.x, point.y)

# Функция, рисующая точки
def drawPoints(points: list):
    for i in range(len(points)):
        drawPoint(points[i])

# Функция, рисующая диаметр
def drawDiameter(points: list):
    plt.plot([points[0].x, points[1].x],
             [points[0].y, points[1].y], "pink")

# Функция, рисующая выпуклую оболочку
def drawConvexHull(convexHullPoints: list, color: str):
    for i in range(len(convexHullPoints) - 1):
        plt.plot([convexHullPoints[i].x, convexHullPoints[i + 1].x],
                 [convexHullPoints[i].y, convexHullPoints[i + 1].y], color=color)
    camera.snap()

# Функция, передвигающая точку на определенный вектор
def move(movingPoints: list, vectors: list):
    for i in range(len(movingPoints)):
        movingPoints[i] = movingPoints[i] + vectors[i]

# Функция, генерирующая векторы движения точек
def initMovingVectors(points: list):
    vectors = []
    xs = [random.randint(-1, 1) for _ in range(len(points))]
    ys = [random.randint(-1, 1) for _ in range(len(points))]
    for i in range(len(xs)):
        p = Point(xs[i], ys[i])
        while p.x == 0 and p.y == 0:
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
        vectors.append(p)
    return vectors

# Функция, возвращающая векторы с противоположным направлением
def reflectedVectors(vectors: list):
    for i in range(len(vectors)):
        vectors[i] = Point(-vectors[i].x, -vectors[i].y)
    return vectors

# Функция, генерирующая точки
def generatePoints():
    points = []
    xs = [random.randint(0, 10) for _ in range(10)]
    ys = [random.randint(0, 10) for _ in range(10)]
    for i in range(len(xs)):
        x = Point(xs[i], ys[i])
        points.append(x)
    return points

# Функция, возвращающая минимальную из всех ординат точек
def minY(points: list):
    miny = points[0].y
    for i in range(len(points)):
        if points[i].y < miny:
            miny = points[i].y
    return miny

# Функция, возвращающая точку, с которой начинается алгоритм Джарвиса
def getInitialPoint(points: list):
    miny = minY(points)
    initialPoint = Point(-1, -1)
    for i in range(len(points)):
        if points[i].y == miny:
            initialPoint = points[i]
    return initialPoint

# Функция, возвращающая следующую точку в алгоритме Джарвиса
def getNextActivePoint(points: list, currentActivePoint: Point, convexHullPoints: list):
    if len(convexHullPoints) < 2:
        polarAxis = Vector(Point(0, 0), Point(1, 0))
    else:
        polarAxis = Vector(convexHullPoints[-2], convexHullPoints[-1])
    nextActivePoint = get_point_with_min_arc(points, currentActivePoint, polarAxis, convexHullPoints)
    return nextActivePoint

# Функция, возвращающая следующую точку в алгоритме Джарвиса с минимальным косинусом
def get_point_with_min_arc(points: list, activePoint: Point, polarAxis: Vector, convexHullPoints: list):
    minArc = 2 * math.pi
    index = -1
    initial = getInitialPoint(points)
    for i in range(len(points)):
        if len(convexHullPoints) == 1 and points[i].x == initial.x and points[i].y == initial.y:
            continue
        onHull = False
        for j in range(1, len(convexHullPoints)):
            if points[i].x == convexHullPoints[j].x and points[i].y == convexHullPoints[j].y:
                onHull = True
                break
        if onHull:
            continue
        currentArc = math.acos(getCosine(Vector(activePoint, points[i]), polarAxis))
        if minArc > currentArc >= 0:
            minArc = currentArc
            index = i
    return points[index]

# Функция для нахождения косинуса угла
def getCosine(v1: Vector, v2: Vector):
    cos = (v1 * v2) / (v1.getLength() * v2.getLength())
    if cos > 1:
        return 1
    elif cos < -1:
        return -1
    else:
        return cos

# Алгоритм Джарвиса
def JarvisAlgorithm(points):
    initial = getInitialPoint(points)
    activePoint = initial
    convexHullPoints = [activePoint]

    while True:
        activePoint = getNextActivePoint(points, activePoint, convexHullPoints)
        convexHullPoints.append(activePoint)
        if initial.x == convexHullPoints[-1].x and initial.y == convexHullPoints[-1].y:
            break

    return convexHullPoints

# Функция для подсчета определителя
def det(a, b, c, d):
    return a * d - b * c

# Функция для подсчета векторного произведения
def square(p0: Point, p1: Point, p2: Point):
    return det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)

# Функция для подсчета диаметра выпуклой оболочки
def setDiameter(hullPoints):
    D = 0
    i = 1
    while square(hullPoints[len(hullPoints) - 1], hullPoints[0], hullPoints[i]) < square(hullPoints[len(hullPoints) - 1], hullPoints[0], hullPoints[i + 1]) and i < len(hullPoints):
        i = i + 1
    start = i
    j = 0
    while start < len(hullPoints):
        tmp = start
        while square(hullPoints[j % len(hullPoints)], hullPoints[(j + 1) % len(hullPoints)], hullPoints[tmp % len(hullPoints)]) <= square(hullPoints[j % len(hullPoints)], hullPoints[(j + 1) % len(hullPoints)], hullPoints[(tmp + 1) % len(hullPoints)]):
            tmp = tmp + 1
        end = tmp
        for k in range(start, end + 1):
            if D < Vector(hullPoints[j], hullPoints[k % len(hullPoints)]).getLength():
                tmp1 = hullPoints[j % len(hullPoints)]
                tmp2 = hullPoints[k % len(hullPoints)]
                D = Vector(hullPoints[j], hullPoints[k]).getLength()
        start = end
        j = j + 1

    res = {'distance': D, 'points': [tmp1, tmp2]}
    return res

# Функция для начала движений
def startMotion(points: list):
    vectors = initMovingVectors(points)
    diameterLimit = 40

    i = 0
    while i < 70:
        convexHullPoints = JarvisAlgorithm(points)

        drawPoints(points)
        drawDiameter(setDiameter(convexHullPoints)['points'])
        drawConvexHull(convexHullPoints, "orange")

        if setDiameter(convexHullPoints)['distance'] >= diameterLimit:
            vectors = reflectedVectors(vectors)

        move(points, vectors)
        i += 1

# ГЛАВНАЯ!
def mainFunc():
    points = generatePoints()
    startMotion(points)

    plt.grid(True)
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()

mainFunc()