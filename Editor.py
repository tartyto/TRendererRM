from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

from Shapes import Sphere
from TRUtilities import Vector3, Shader


#tkinter setup

v = Tk()

def setListtoListBox(list,listbox: Listbox,mode="ADD"):
    if(mode=="ADD"):
        for i in list:
            listbox.insert("end",i)

def setListboxEmpty(listbox: Listbox):
    listbox.delete(0,"end")

completeViewFrame = ttk.Frame(v)

frontViewFrame = ttk.LabelFrame(completeViewFrame,text="front view")
frontView = Canvas(frontViewFrame,width=(1920/4),height=(1080/4),background="#7080a0",borderwidth=5,relief="sunken")
frontView.pack()
frontViewFrame.pack()

sideViewFrame = ttk.LabelFrame(completeViewFrame,text="side view")
sideView = Canvas(sideViewFrame,width=(1920/4),height=(1080/4),background="#7080a0",borderwidth=5,relief="sunken")
sideView.pack()
sideViewFrame.pack()
completeViewFrame.grid(row=0,column=0)

optionsFrame = ttk.Frame(v)

resolutionFrame = ttk.LabelFrame(optionsFrame, text="resolution")

resolutionXvar = IntVar(value=int(1920/4))
resolutionX = ttk.Spinbox(resolutionFrame,from_=1, to=1920, textvariable = resolutionXvar)
resolutionX.grid(row=0,column=0)
resolutionXiconLabel = ttk.Label(resolutionFrame, text=" X ")
resolutionXiconLabel.grid(row=0,column=1)

resolutionYvar = IntVar(value=int(1080/4))
resolutionY = ttk.Spinbox(resolutionFrame,from_=1.0, to=1920.0, textvariable = resolutionYvar)
resolutionY.grid(row=0,column=2)

createListFrame = ttk.LabelFrame(optionsFrame,text="Create New Object")

def onSelectObjectListBox(e):
    try:

        global lastSelected
        lastSelected = getCurrentObjectListBox()
        changeXVar.set(lastSelected.position.x)
        changeYVar.set(lastSelected.position.y)
        changeZVar.set(lastSelected.position.z)

        global lastSelectedIndex
        lastSelectedIndex = objectListBox.curselection()[0]

        global objectNameVar
        objectNameVar.set(objectsStringList[lastSelectedIndex])

        setButtonColorRGB(objectsShapeList[lastSelectedIndex].shader.color)

        global sizeSpinbox
        sizeSpinbox.set(objectsShapeList[lastSelectedIndex].size)
    except:
        pass

def getCurrentObjectListBox():
    return objectsShapeList[objectListBox.curselection()[0]]

def setPos(variable,pos):
    variable.position = pos
    UpdateView()



objectsShapeList = [Sphere(Vector3(100,150,200),30,shader=Shader(color=(50,150,255)))]
objectsStringList = ["Default Sphere"]

lastSelected = objectsShapeList[0]
lastSelectedIndex = 0

objectListBox = Listbox(createListFrame)
objectListBox.bind("<<ListboxSelect>>", onSelectObjectListBox)

setListtoListBox(objectsStringList,objectListBox)

objectListBox.grid(row=1,column=0)

def createListObject():
    name = "New Object"
    objectsStringList.append(name)
    objectsShapeList.append(Sphere(Vector3(10,10,10),20,shader=Shader(color=(255,0,0))))
    objectListBox.insert("end",name)
    UpdateView()

def deleteObject():
    objectsStringList.pop(lastSelectedIndex)
    objectsShapeList.pop(lastSelectedIndex)
    objectListBox.delete(lastSelectedIndex)
    UpdateView()

CreateButton = ttk.Button(createListFrame,text="Create Object", command=createListObject)
CreateButton.grid(row=0,column=0)

DeleteButton = ttk.Button(createListFrame,text="Delete Object", command=deleteObject)
DeleteButton.grid(row=0,column=1)

objectOptionsFrame = ttk.LabelFrame(createListFrame,text="Options")

nameLabelFrame = ttk.LabelFrame(objectOptionsFrame,text="Name")

objectNameVar = StringVar(value=objectsStringList[0])

def onNameChange(*args):
    objectsStringList[lastSelectedIndex] = objectNameVar.get()

    setListboxEmpty(objectListBox)
    setListtoListBox(objectsStringList,objectListBox)

def rgb_to_hex(rgb):
    return "#" + ('%02x%02x%02x' % rgb)

objectNameVar.trace("w",onNameChange)

nameEntry = ttk.Entry(nameLabelFrame,textvariable=objectNameVar)
nameEntry.pack()

nameLabelFrame.grid(row=0)

colorLabelFrame = ttk.LabelFrame(objectOptionsFrame,text="Color")

def roundList(list):
    templist = []
    for i in list:
        templist.append(int(round(i)))
    return tuple(templist)

def setButtonColorRGB(rgb):
    changeColorButton.config(bg=rgb_to_hex(roundList(rgb)))

def setCurrentObjectColor():
    global objectsShapeList
    currentColor = colorchooser.askcolor("#ff0000")

    objectsShapeList[lastSelectedIndex].shader.color = roundList(currentColor[0])

    setButtonColorRGB(currentColor[0])




changeColorButton = Button(colorLabelFrame,bg="#ff0000",width=10,command=setCurrentObjectColor)
changeColorButton.pack()

colorLabelFrame.grid(row=8)

positionLabelFrame = ttk.LabelFrame(objectOptionsFrame,text="Position")

changePosSetPos = lambda: setPos(lastSelected,Vector3(changeXVar.get(),changeYVar.get(),changeZVar.get()))

changeXVar = DoubleVar(value=0)
changeX = ttk.LabelFrame(positionLabelFrame,text="X")
changePosX = ttk.Spinbox(changeX,from_=0,to=10000,increment=5,textvariable=changeXVar, command = changePosSetPos)
changePosX.pack()
changeX.grid(row=0,column=0)

changeYVar = DoubleVar(value=0)
changeY = ttk.LabelFrame(positionLabelFrame,text="Y")
changePosY = ttk.Spinbox(changeY,from_=0,to=10000,increment=5,textvariable=changeYVar, command = changePosSetPos)
changePosY.pack()
changeY.grid(row=1,column=0)

changeZVar = DoubleVar(value=0)
changeZ = ttk.LabelFrame(positionLabelFrame,text="Z")
changePosZ = ttk.Spinbox(changeZ,from_=-10000,to=10000,increment=5,textvariable=changeZVar, command = changePosSetPos)
changePosZ.pack()
changeZ.grid(row=2,column=0)

positionLabelFrame.grid(row=10)
objectOptionsFrame.grid(row=1,column=1,sticky="N")

def ChangeSize():
    global sizeSpinbox
    objectsShapeList[lastSelectedIndex].size = float(sizeSpinbox.get())
    UpdateView()

sizeLabelFrame = ttk.LabelFrame(objectOptionsFrame,text="Radius")
sizeVar = DoubleVar
sizeSpinbox = ttk.Spinbox(sizeLabelFrame,from_=0,to=100,increment=1,textvariable=sizeVar, command = ChangeSize)
sizeSpinbox.pack()
sizeLabelFrame.grid(row=9)

elementOptionsFrame = ttk.LabelFrame(createListFrame,text="element options")



elementOptionsFrame.grid(row=0,column=1)

createListFrame.grid(row=1,column=0)

def setResolution(resolutionX,resolutionY):
    frontView.config(width=resolutionX,height=resolutionY)
    sideView.config(width=resolutionX, height=resolutionY)
    resolutionYvar.set(resolutionY)
    resolutionXvar.set(resolutionX)

setResolutionButton = ttk.Button(resolutionFrame,text="apply resolution",command = lambda: setResolution(resolutionXvar.get(),resolutionYvar.get()))
setResolutionButton.grid(row=1,column=2)

resolutionFrame.grid(row=0,column=0)
optionsFrame.grid(row=0,column=1,sticky=N)

#render
from MainFunctions import Renderer
from TRUtilities import Shader
from PIL import Image,ImageDraw
import asyncio
Trenderer = Renderer()

def RenderImage():
    Trenderer.objectList = []
    Trenderer.lightList = []
    for i in objectsShapeList:
        Trenderer.passObject(i)
    Trenderer.passLight(Sphere(position=Vector3(0,0,0),radius=1,shader=Shader(color=(255,0,0))))

    image = Image.new("RGB", (resolutionXvar.get(),resolutionYvar.get()))
    imageDRW = ImageDraw.Draw(image)

    Trenderer.Render((resolutionXvar.get(),resolutionYvar.get()),imageDRW)

    image.save("uwu.gif")
    image.show()


renderButton = ttk.Button(optionsFrame,text="Render Image",command=RenderImage)
renderButton.grid(row=100,column=100,sticky=SE)

#draw things

#----------> set UI

objectFrontList = []
objectSideList = []

def UpdateView():
    DeleteView()
    drawView()

def DeleteView():
    for i in objectFrontList:
        frontView.delete(i)
    for i in objectSideList:
        sideView.delete(i)

def drawView():
    for i in objectsShapeList:
        currentPosX = i.position.x
        currentPosY = i.position.y
        currentSize = i.size
        currentType = i.type
        objectFrontList.append(frontView.create_oval(currentPosX-currentSize,currentPosY-currentSize,currentPosX+currentSize,currentPosY+currentSize))
    for i in objectsShapeList:
        currentPosX = i.position.z
        currentPosY = i.position.y
        currentSize = i.size
        currentType = i.type
        objectSideList.append(sideView.create_oval(currentPosX-currentSize,currentPosY-currentSize,currentPosX+currentSize,currentPosY+currentSize))


drawView()

v.mainloop()