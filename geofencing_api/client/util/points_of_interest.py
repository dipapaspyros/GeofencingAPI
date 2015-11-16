from random import randint

__author__ = 'dipap'

from point import Point


class PointOfInterest(Point):

    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight


class PointsOfInterest:

    def __init__(self, boundary, n_of_points):
        self.boundary = boundary
        self.points = []
        self.total_weight = 0

        for i in range(0, n_of_points):
            p = boundary.random_point()
            weight = randint(1, 100)

            self.total_weight += weight
            self.points.append(PointOfInterest(p.x, p.y, weight))

    def get_point_of_interest(self):
        i = randint(0, self.total_weight)
        current_weight = 0

        for p in self.points:
            if p.weight + current_weight >= i:
                return p

            current_weight += p.weight

    def get_point(self):
        poi = self.get_point_of_interest()
        p = None
        while not self.boundary.is_inside(p):
            p = Point(poi.x + randint(-70, 70)/10000.0, poi.y + randint(-70, 70)/10000.0)

        return p
