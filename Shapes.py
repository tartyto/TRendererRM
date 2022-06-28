from TRUtilities import Vector3, Shader

class Sphere:
    type = "SPHERE"
    position = None
    size = None
    shader = None
    def __init__(self, position, radius,shader=None):
        if not(type(position) is Vector3):
            raise TypeError("Position takes Vector3 not " + str(type(position)))
        if(shader == None):
            self.shader = Shader()
        else:
            self.shader = shader
        self.position = position
        self.size = radius

    def getDistance(self, eye):
        return (Vector3.distance(eye, self.position)) - self.size

class Cube:
    type = "CUBE"
    position = None
    size = None
    def __init__(self, position, size):
        if not(type(position) is Vector3):
            raise TypeError("Position takes Vector3 not " + str(type(position)))
        self.position = position
        self.size = size
    def getDistance(self, eye):
        #pass
        p = eye
        centre = Vector3(self.position.x,self.position.y)
        size = Vector3(self.size,self.size)

        offset = Vector3(abs(p.x-centre.x),abs(p.y-centre.y)) - size

        unsignedDst = Vector3.lenght((max(offset.x,0),max(offset.y,0)))



        dstInsideBox = max(min(offset.x,0),min(offset.y,0))

        return unsignedDst + dstInsideBox

        #return math.sqrt(max(eye.x-self.size-self.position.x,0)**2) + (max(eye.x-self.size-self.position.y,0)**2)
