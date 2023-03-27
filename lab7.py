import random

from celluloid import Camera
from matplotlib import pyplot as plt

fig = plt.figure()
camera = Camera(fig)

# Класс точка
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

# Определяет, какая точка является средней из трех
def findMiddlePoint(p1: Point, p2: Point, p3: Point):
    if Point(p3, p1) * Point(p3, p2) <= 0:
        return p3
    elif Point(p2, p1) * Point(p2, p3) <= 0:
        return p2
    else:
        return p1

# Находит положение точки относительно прямой (d < 0 - правее, d > 0 - левее, d == 0 - на прямой)
def rotate(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

# Алгоритм построения динамической выпуклой оболочки
def dynamicConvexHull(points: list, old_convex_hull: list):

    if len(points) <= 2:
        return points

    if len(points) == 3:
        if rotate(points[0], points[1], points[2]) == 0:
            mid_point = findMiddlePoint(points[0], points[1], points[2])
            if mid_point == points[0]:
                return [points[1], points[2]]
            elif mid_point == points[1]:
                return [points[0], points[2]]
            else:
                return [points[0], points[1]]
        else:
            if rotate(points[2], points[0], points[1]) > 0:
                return [points[0], points[1], points[2]]
            if rotate(points[2], points[0], points[1]) < 0:
                return [points[0], points[2], points[1]]

    if len(points) > 3:
        new_point = points[-1]
        start = -1
        end = -1
        if rotate(new_point, old_convex_hull[-1], old_convex_hull[0]) < 0 \
                and rotate(new_point, old_convex_hull[0], old_convex_hull[1]) < 0:
            for i in range(len(old_convex_hull) - 1):
                if rotate(new_point, old_convex_hull[i], old_convex_hull[i + 1]) < 0:
                    start = i + 1
            end = len(old_convex_hull) - 1
            for i in range(len(old_convex_hull) - 1, start, -1):
                if rotate(new_point, old_convex_hull[i - 1], old_convex_hull[i]) < 0:
                    end = i - 1
            new_hull = old_convex_hull[start:end + 1] + [new_point]
        else:
            old_convex_hull.append(old_convex_hull[0])
            for i in range(len(old_convex_hull) - 1):
                if rotate(new_point, old_convex_hull[i], old_convex_hull[i + 1]) < 0:
                    start = i
                    break
            if start == -1:
                old_convex_hull.pop()
                return old_convex_hull
            for i in range(start, len(old_convex_hull) - 1):
                if rotate(new_point, old_convex_hull[i], old_convex_hull[i + 1]) < 0:
                    end = i + 1
                else:
                    break
            old_convex_hull.pop()
            new_hull = old_convex_hull[0:start + 1] + [new_point] + old_convex_hull[end:len(old_convex_hull)]

        return new_hull

# Инициирующая функция
def init():
    points = []
    convex_hull = []

    for i in range(30):
        points.append(Point(random.randint(0, 30), random.randint(0, 30)))

        is_existed = False
        for j in range(len(points) - 1):
            if points[j] == points[-1]:
                is_existed = True
        if is_existed:
            continue

        for i in range(len(points)):
            plt.scatter(points[i].x, points[i].y, color="blue")

        convex_hull = dynamicConvexHull(points, convex_hull)
        if len(convex_hull) == 1:
            plt.scatter(convex_hull[0].x, convex_hull[0].y, color="green")
        else:
            for i in range(len(convex_hull)):
                plt.plot([convex_hull[i].x, convex_hull[(i + 1) % len(convex_hull)].x],
                         [convex_hull[i].y, convex_hull[(i + 1) % len(convex_hull)].y],
                         color="green")
        camera.snap()

    plt.grid(True)
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()

init()
