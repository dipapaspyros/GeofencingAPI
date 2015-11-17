import copy
from random import randint
from time import sleep
from uuid import uuid4
from math import sin, cos, sqrt

import math
from django.utils.timezone import now
from geofencing_api.client.util.point import Point
from util.boundary import Boundary
from util.points_of_interest import PointsOfInterest

__author__ = 'dipap'


class UserNotFound(Exception):
    pass


class User:

    def __init__(self, points_of_interest=None, uid=None):
        if uid:
            self.id = uid
            self.type = None
        else:
            self.id = uuid4()

            # movement direction
            self.f = randint(0, 359)

            # two cases - around point of interest, or by-passer
            if randint(0, 10) <= 7:
                self.p = points_of_interest.get_point()
                if randint(0, 10) <= 8:
                    self.type = 'Pedestrian'
                else:
                    self.type = 'Car'
            else:
                self.p = points_of_interest.boundary.random_point()
                if randint(0, 10) <= 6:
                    self.type = 'Car'
                else:
                    self.type = 'Pedestrian'

        # latest update time -- initially none
        self.updated_at = None
        self.speed = 0

    def update(self, x, y):
        p2 = Point(x, y)
        t = now()

        if self.updated_at:
            # calculate speed
            dx = self.distance_from(p2)
            dt = t - self.updated_at
            self.speed = dx/dt
            # calculate direction
            dx, dy = x - self.p.x, y - self.p.y
            self.f = math.atan2(dx/dy)

        self.p = p2
        self.updated_at = t

    def iteration(self):
        if self.speed == 0:
            return

        # The user moves according to their latest speed
        if self.type:
            if self.type == 'Car':
                speed = randint(10, 50)
            else:
                speed = randint(3, 5)
        else:
            speed = self.speed

        e = 100000.0
        self.p.x += speed/e*sin(self.f)
        self.p.y += speed/e*cos(self.f)

    def distance_from(self, p):
        return sqrt(pow(p.x - self.p.x, 2) + pow(p.y - self.p.y, 2))

    def in_range(self, p, r):
        in_dst = 0
        u = copy.copy(self)

        for i in range(1, 10):
            u.iteration()
            if u.distance_from(p) <= r:
                in_dst += 1

        return in_dst >= 5

    def to_json(self):
        return {
            'id': self.id,
            'position': {
                'lat': self.p.x,
                'lng': self.p.y,
            }
        }


class UserBase:

    def __init__(self, init_n_of_users):
        if init_n_of_users > 0:
            # simulated movements
            self.boundary = Boundary()
            self.points_of_interest = PointsOfInterest(self.boundary, 30)
            self.users = [User(self.points_of_interest) for _ in range(0, init_n_of_users)]
            self.simulation = True

        else:
            # actual environment
            self.simulation = False
            self.users = []

    def iteration(self):
        while True:
            for u in self.users:
                u.iteration()

            sleep(1)

    def get_user(self, uid):
        for u in self.users:
            if u.id == uid:
                return u

        u = User(uid=uid)
        self.users.append(u)
        return u

    def update(self, uid, x, y):
        u = self.get_user(uid)
        u.update(x, y)

    def in_group(self, x, y):
        node = Point(x, y)

        r = 0.01
        group = []
        for u in self.users:
            if u.in_range(node, r):
                group.append(u)

        return group
