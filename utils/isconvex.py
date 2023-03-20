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