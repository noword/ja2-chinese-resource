#! /usr/bin/env python3
# coding=utf-8
from abc import ABC, abstractclassmethod
from io import BytesIO


class Base(ABC):
    def __init__(self, io=None):
        super().__init__()
        if io:
            self.load(io)

    @abstractclassmethod
    def load(self, io):
        raise NotImplementedError

    @abstractclassmethod
    def save(self, io):
        raise NotImplementedError

    def getvalue(self):
        io = BytesIO()
        self.save(io)
        return io.getvalue()
