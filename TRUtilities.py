import math
import numpy as np

class Vector3:
    x = None
    y = None
    z = None

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def distance(point1, point2):
        return math.sqrt(((point2.x - point1.x) ** 2) + ((point2.y - point1.y) ** 2) + ((point2.z - point1.z) ** 2))
    def __add__ (self, other):
        if (type(other) is float or type(other) is int):
            return Vector3((self.x + other), (self.y + other), (self.z + other))
        return Vector3((self.x+other.x),(self.y+other.y),(self.z+other.z))
    def __sub__(self, other):
        if(type(other) is float or type(other) is int):
            return Vector3((self.x - other), (self.y - other), (self.z - other))
        return Vector3((self.x-other.x),(self.y-other.y),(self.z-other.z))
    def __abs__(self):
        return Vector3(abs(self.x),abs(self.y),abs(self.z))
    def __str__(self):
        return ("( " + str(self.x) + ", " + str(self.y) + " ," + str(self.z) + " )")
    def abs(self):
        return Vector3(abs(self.x),abs(self.y),abs(self.z))

    @staticmethod
    def normalize(vector):
        #return vector / lenght((vector.z,vector.y,vector.z))
        vectorLenght = Vector3.lenght((vector.z,vector.y,vector.z))
        return Vector3(vector.x / vectorLenght,vector.y / vectorLenght,vector.z / vectorLenght)
    def normalized(self):
        return self.normalize(self)
    def __mul__(self, other):
        if (type(other) is float or type(other) is int):
            return Vector3((self.x * other), (self.y * other), (self.z * other))
        return Vector3((self.x * other.x), (self.y * other.y), (self.z * other.z))

    @staticmethod
    def dot(vector1,vector2):
        return np.dot([vector1.x,vector1.y,vector1.z],[vector2.x,vector2.y,vector2.z])

    @staticmethod
    def lenght(vector):
        result = 0
        for i in vector:
            result = result + (i ** 2)
        return math.sqrt(result)
    def getLenght(self):
        return Vector3.lenght(self)
    def inverted(self):
        return Vector3(-self.x,-self.y,-self.z)

    def __round__(self, n=None):
        return Vector3(round(self.x,n),round(self.y,n),round(self.z,n))


def estimateNormal(p, sceneSDF, precision = 0.1):
    EPSILON = precision

    return Vector3.normalize(Vector3(
        sceneSDF(Vector3(p.x + EPSILON, p.y, p.z)) - sceneSDF(Vector3(p.x - EPSILON, p.y, p.z)),
        sceneSDF(Vector3(p.x, p.y + EPSILON, p.z)) - sceneSDF(Vector3(p.x, p.y - EPSILON, p.z)),
        sceneSDF(Vector3(p.x, p.y, p.z + EPSILON)) - sceneSDF(Vector3(p.x, p.y, p.z - EPSILON))
    ))

class Shader:
    color = None
    diffuse = None
    def __init__(self,color=(255,255,255),diffuse=1):
        self.color = color
        self.diffuse = diffuse