__author__ = 'dipap'

import uuid

from django.db import models


# Create your models here.
class Graph(models.Model):
    """
    A Graph represents a set of nodes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid_list = models.TextField()  # comma-separated list of user IDs
    label = models.CharField(max_length=512)  # a humanized label -- just for display
    lat = models.FloatField()  # graph latitude
    lng = models.FloatField()  # graph longtitude

    def to_json(self):
        """
        :return: A json representation of the graph
        """
        result = {
            'GraphID': self.uuid,
            'lat': self.lat,
            'lng': self.lng,
            'size': len(self.uid_list.split(',')),
        }

        if self.label:
            result['label'] = self.label

        return result
