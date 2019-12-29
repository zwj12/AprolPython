#!/usr/bin/python
# -*- coding: utf-8 -*-

"""RobotResource

"""

class RobotResource(object):
    """RobotResource

    """

    def __init__(self, resource, key, value=None):
        self.__resource = resource
        self.__key = key
        self.value = value

    def get_resource(self):
        """RobotResource

        """
        return self.__resource

    def get_key(self):
        """RobotResource

        """
        return self.__key
