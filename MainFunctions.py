from tkinter import *
from tkinter import ttk
import math

import PIL.Image
from PIL import Image, ImageDraw, ImageFilter

import time


import Shapes
from TRUtilities import Vector3, estimateNormal
from Shapes import Sphere, Cube

class Renderer:
    objectList = []
    lightList = []
    def passObject(self, *args):
        for i in args:
            self.objectList.append(i)
    def passLight(self, *args):
        for i in args:
            self.lightList.append(i)

    def sceneSDF(self,p,mode="minVar"):
        minVar = 999999
        minShape = None

        for i in self.objectList:
            currentDistance = i.getDistance(Vector3(p.x, p.y, p.z))
            if(currentDistance < minVar):
                minVar = currentDistance
                minShape = i
            #minVar = min(currentDistance, minVar)
        if(mode=="minVar"):
            return minVar
        elif(mode=="minShape"):
            return minShape

    def RenderPixel(self,pixelPos,RayDirection):
        endPos = pixelPos
        hashit = False
        isShadow = False
        hitpoint = Vector3(0,0,0)
        global finalColor
        finalColor = (0,0,0)
        ambientColor = finalColor
        ambience = 0.05

        rayPrecision = 0.000001

        if(len(self.objectList) > 0):
            for i in range(20):
                minVar = self.sceneSDF(endPos)

                global angle
                endPos = Vector3(endPos.x+RayDirection.x,endPos.y+RayDirection.y,endPos.z + minVar)
                if(minVar <= rayPrecision):
                    hashit = True
                    hitpoint = endPos


                    """float diff = max(dot(norm, lightDir), 0.0);
                        vec3 diffuse = diff * lightColor;"""



                    norm = Vector3.normalize(estimateNormal(hitpoint,self.sceneSDF,precision=0.1))
                    lightDir = Vector3.normalize(self.lightList[0].position - hitpoint)

                    diff = max(Vector3.dot(norm, lightDir), 0.0);
                    hitShape: Shapes.Sphere = self.sceneSDF(hitpoint,mode="minShape")

                    specularStrenght = 0.5

                    #viewDir = Vector3.normalize(viewPos - FragPos);
                    #reflectDir = reflect(-lightDir, norm);

                    ambienceColor = (ambience * hitShape.shader.color[0],ambience * hitShape.shader.color[1],ambience * hitShape.shader.color[2])


                    #diffColor = [diff * hitShape.shader.color[0],diff * hitShape.shader.color[1],diff * hitShape.shader.color[2]]
                    #finalDiffColor = (hitShape.shader.diffuse * diffColor)

                    hitColor = hitShape.shader.color

                    finalColor = (round((ambience + diff) * hitColor[0]),round((ambience + diff) * hitColor[1]),round((ambience + diff) * hitColor[2]))

                    #finalColor = (hitShape.shader.diffuse*diffColor[0]) + ambienceColor,hitShape.shader.diffuse*diffColor[1]+ ambienceColor,hitShape.shader.diffuse*diffColor[2]+ ambienceColor)

                    #finalColor = (hitShape.shader.color[0],hitShape.shader.color[1],hitShape.shader.color[2])

                    #show normals
                    """normalEST = estimateNormal(hitpoint)
                    finalColor = (int(round(normalEST.x)),int(round(normalEST.y)),int(round(normalEST.z)))"""
                    break
            if(hashit):
                if (len(self.lightList) > 0):
                    direction = self.lightList[0].position - hitpoint
                    moveDir = Vector3((direction.x / Vector3.lenght((direction.x, direction.y, direction.z))),
                                      (direction.y / Vector3.lenght((direction.x, direction.y, direction.z))),
                                      (direction.z / Vector3.lenght((direction.x, direction.y, direction.z))))

                    endPos = Vector3(endPos.x + (moveDir.x * (rayPrecision *8)), endPos.y + (moveDir.y * (rayPrecision *8)),
                                     endPos.z + (moveDir.z * (rayPrecision *8)))

                    for i in range(200):
                        minVar = self.sceneSDF(endPos)
                        direction = self.lightList[0].position - hitpoint
                        moveDir = Vector3((direction.x / Vector3.lenght((direction.x,direction.y,direction.z))),(direction.y / Vector3.lenght((direction.x,direction.y,direction.z))),(direction.z / Vector3.lenght((direction.x,direction.y,direction.z))))

                        endPos = Vector3(endPos.x+(moveDir.x*minVar), endPos.y+(moveDir.y*minVar), endPos.z+(moveDir.z*minVar))
                        if (minVar <= rayPrecision):
                            isShadow = True
                            hitColor = hitShape.shader.color
                            finalColor = (round(ambience*hitColor[0]),round(ambience*hitColor[1]),round(ambience*hitColor[2]))
                            #finalColor = (hitShape.shader.color[0],hitShape.shader.color[1],hitShape.shader.color[2])
                        if(Vector3.distance(self.lightList[0].position,endPos) < 0.1):
                            break
            return finalColor

    def Render(self,resolution,imgDraw):
        for x in range(resolution[0]):
            for y in range(resolution[1]):
                #imgDraw.point((x,y),fill=self.RenderPixel(Vector3(x,y,0),Vector3((x-(resolution[0]/2))/20000,(y-(resolution[1]/2)/20000))))
                #imgDraw.point((x, y), fill=self.RenderPixel(Vector3(x, y, 0), Vector3(5,5,0)))
                imgDraw.point((x, y), fill=self.RenderPixel(Vector3(x, y, 0), Vector3(0, 0, 0)))