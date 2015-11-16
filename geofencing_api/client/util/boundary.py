from random import randint
from location_app.geofencing_api.client.util.point import Point

__author__ = 'dipap'


class Boundary:

    def __init__(self, location='Athens'):
        if location == 'Athens':
            self.min_x = 37.9
            self.max_x = 38
            self.min_y = 23.6
            self.max_y = 23.8

    def is_inside(self, p):
        if not p:
            return False

        return self.min_x <= p.x <= self.max_x and self.min_y <= p.y <= self.max_y

    def random_point(self):
        e = 1000000.0
        x = randint(int(self.min_x*e), int(self.max_x*e))/e
        y = randint(int(self.min_y*e), int(self.max_y*e))/e

        return Point(x, y)
