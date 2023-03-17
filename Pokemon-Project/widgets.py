import time
import pygame
from const import *
from pygame.locals import *
from pygame import gfxdraw

"""Objects file, wanted to separate my classes with the main script to make it cleaner, each of these objects have customizable style and functionnalities"""

"""Created a 'Frame' object, it inherits the 'Surface' class from pygame"""
class Frame(pygame.Surface):
    """Constructor"""
    def __init__(self, parent:pygame.Surface, size:tuple, pos:tuple=(0, 0), color:tuple=(0, 0, 0), surfImage:pygame.image=None):
        pygame.Surface.__init__(self, size)
        self.set_colorkey((1, 1, 1))
        self.width, self.height = size[0], size[1]
        self.pos = (pos[0], pos[1])
        self.color = color
        self.parent = parent
        self.surfImage, self.activeSurfImage = surfImage, surfImage
        self.fill(self.color)


    """Public methods"""

    #Returns the position of the Frame
    def get_SurfPos(self):
        return self.pos



    #Returns the Frame's color
    def get_SurfColor(self):
        return self.color
    

    
    def get_SurfSize(self):
        return (self.width, self.height)
    


    def ChangeBGFrame(self, newBG:pygame.Surface):
        self.surfImage = newBG
    


    #Enables the frame, called every frame in pygame's mainloop and also in other objects
    def ActiveFrame(self, drawPos:tuple=(), activeImage:pygame.image=None, parentIsFrameImage:bool=False):
        if drawPos == ():
            drawPos = self.pos
    
        if parentIsFrameImage:
            self.parent.surfImage.blit(self.surfImage, drawPos)
        elif activeImage != None:
            self.activeSurfImage = pygame.transform.smoothscale(activeImage, (self.width, self.height))
            self.parent.blit(self, drawPos)
            self.parent.blit(self.activeSurfImage, drawPos)
        elif self.surfImage != None:
            self.surfImage = pygame.transform.smoothscale(self.surfImage, (self.width, self.height))
            self.parent.blit(self, drawPos)
            self.parent.blit(self.surfImage, drawPos)
        else:
            self.parent.blit(self, drawPos)










class SpriteSheet:
    def __init__(self, scene:Frame, image:pygame.image, nFrames:int, scale:float=1.0, spriteCut:int=None, sheetPartSize:int=None, sheetPartStart:int=0, spriteSheetOrientation:str="x"):
        self.__scene = scene
        self.__sheet = image
        self.__frames = nFrames
        self.__imageScale = scale
        self.__spriteSheetOrientation = spriteSheetOrientation
        self.__spriteCut = spriteCut
        self.__sheetPartSize = sheetPartSize
        self.__sheetPartStart = sheetPartStart

        self.__spriteFrames = self.__InitAnimationFrames()
        self.__lastUpdate = 0




    '''Public methods'''


    def SpriteAnimation(self, pos:tuple, animSpeed:int, spriteSceneBG:pygame.Surface=None, animLoop:bool=True, sceneParent:Frame=None):
        time = pygame.time.get_ticks()
        animationCooldown = animSpeed
        frame = 0

        if animLoop:
            if time - self.__lastUpdate >= animationCooldown and frame <= len(self.__spriteFrames) - 1: 
                frame += 1
                self.__lastUpdate = time

            else: 
                frame = 0

            self.__scene.blit(self.__spriteFrames[frame], pos)

        elif not animLoop:
            while frame <= len(self.__spriteFrames) - 1:
                time = pygame.time.get_ticks()
                
                if time - self.__lastUpdate >= animationCooldown: 
                    frame += 1
                    self.__lastUpdate = time
                

                if sceneParent != None:
                    sceneParent.ActiveFrame()

                self.__scene.ActiveFrame()

                if spriteSceneBG != None:
                    self.__scene.surfImage.blit(spriteSceneBG, (0, 0))

                if frame < len(self.__spriteFrames) - 1:
                    self.__scene.surfImage.blit(self.__spriteFrames[frame], pos)

                pygame.display.update()



    def Get_Image(self, frame:int, spriteCut:bool=False, sheetPartSize:bool=False):
        sheetStart = 0

        if self.__spriteSheetOrientation.lower() == "y":
            if spriteCut and sheetPartSize:
                imageWidth, imageHeight = self.__sheetPartSize, self.__spriteCut
                sheetStart = self.__sheetPartStart
            elif spriteCut:
                imageWidth, imageHeight = self.__sheet.get_width(), self.__spriteCut
            elif sheetPartSize:
                imageWidth, imageHeight = self.__sheetPartSize, int(self.__sheet.get_height() / self.__frames)
                sheetStart = self.__sheetPartStart
            else:
                imageWidth, imageHeight = self.__sheet.get_width(), int(self.__sheet.get_height() / self.__frames)

            imageSurf = pygame.Surface((imageWidth, imageHeight)).convert_alpha()
            imageSurf.blit(self.__sheet, (0, 0), (sheetStart, (frame * imageHeight), imageWidth, imageHeight))


        else:
            if spriteCut and sheetPartSize:
                imageWidth, imageHeight = self.__sheetPartSize, self.__spriteCut
                sheetStart = self.__sheetPartStart
            elif spriteCut:
                imageWidth, imageHeight = self.__spriteCut, self.__sheet.get_height()
            elif sheetPartSize:
                imageWidth, imageHeight = int(self.__sheet.get_width() / self.__frames), self.__sheetPartSize
                sheetStart = self.__sheetPartStart
            else:
                imageWidth, imageHeight = int(self.__sheet.get_width() / self.__frames), self.__sheet.get_height()

            imageSurf = pygame.Surface((imageWidth, imageHeight)).convert_alpha()
            imageSurf.blit(self.__sheet, (0, 0), ((frame * imageWidth), sheetStart, imageWidth, imageHeight))

        imageSurf = pygame.transform.smoothscale(imageSurf, (imageWidth * self.__imageScale, imageHeight * self.__imageScale))
        imageSurf.set_colorkey((0, 0, 0))


        return imageSurf
    


    #Getters/Setters

    def GetSpriteSize(self):
        return (self.__sheet.get_width(), self.__sheet.get_height())
    
    def GetFrames(self):
        return self.__spriteFrames




    '''Private methods'''


    def __InitAnimationFrames(self):
        animationFrames = []
        for x in range(self.__frames):
            if self.__spriteCut != None and self.__sheetPartSize != None:
                animationFrames.append(self.Get_Image(x, spriteCut=True, sheetPartSize=True))
            elif self.__spriteCut != None:
                animationFrames.append(self.Get_Image(x, spriteCut=True))
            elif self.__sheetPartSize != None:
                animationFrames.append(self.Get_Image(x, sheetPartSize=True))
            else:
                animationFrames.append(self.Get_Image(x))

        return animationFrames
    
    












class ImageAnimation:
    def __init__(self, scene:Frame, imageFrames:list, scale:float=1.0):
        self.__scene = scene
        self.__frames = imageFrames
        self.__frameToDisplay = 0
        self.__lastUpdate = 0
        
        for i in range(len(self.__frames)):
            newWidth, newHeight = self.__frames[i].get_width(), self.__frames[i].get_height()
            self.__frames[i] = pygame.transform.smoothscale(self.__frames[i], (newWidth * scale, newHeight * scale))

    


    '''Public methods'''


    def ActiveAnimation(self, pos:tuple, speed:int, spriteSceneBG:pygame.image=None, animOff:bool=False, frameIfAnimOff:int=0):
        time = pygame.time.get_ticks()
        self.__frameToDisplay = (self.__frameToDisplay % len(self.__frames))


        if time - self.__lastUpdate >= speed and not animOff:
            
            if spriteSceneBG != None:
                self.__scene.surfImage.blit(spriteSceneBG, (0, 0))

            self.__scene.surfImage.blit(self.__frames[self.__frameToDisplay], pos)

            self.__frameToDisplay += 1
            self.__lastUpdate = time

        elif animOff:
            self.__scene.surfImage.blit(self.__frames[frameIfAnimOff], pos)












"""'TextLabel' object, similar to the 'Label' object from tkinter it just displays text onto a surface by creating its own (which also serves as a background)"""
class TextLabel:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, text:str, size:int, font:str=None, color:tuple=(255, 255, 255), bgColor:tuple=None, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False):
        self.frame = parent
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.textSize = size
        self.font = font
        self.text = text
        self.color = color
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY


        try:
            self.bg = self.frame.get_SurfColor()
            if bgColor != None:
                self.bg = bgColor

        except AttributeError:
            self.bg = (1, 1, 1)
            

        if self.font == None:
            self.textFont = pygame.font.Font("Arial", self.textSize)

        else:
            self.textFont = pygame.font.Font(self.font, self.textSize)
        

        self.myText = self.textFont.render(self.text, True, self.color)
        self.width, self.height = self.myText.get_width(), self.myText.get_height()
        self.__InitPos()
        self.textFrame = Frame(self.frame, (self.width, self.height), (self.left, self.top), color=self.bg)
        self.textFrame.blit(self.myText, (0, 0))
        self.textFrame.ActiveFrame((self.left, self.top))
        pygame.display.update()





    """Public methods"""

    #Changes the text by newText
    def NewText(self, newText, color=None):
        if color != None:
            self.color = color
        self.textFrame.fill(self.bg)
        self.textFrame.ActiveFrame((self.left, self.top))

        self.text = newText
        self.myText = self.textFont.render(self.text, True, self.color)
        self.width, self.height = self.myText.get_width(), self.myText.get_height()
        self.__InitPos()

        self.textFrame = Frame(self.frame, (self.width, self.height), (self.left, self.top), color=self.bg)
        self.textFrame.blit(self.myText, (0, 0))
        self.textFrame.ActiveFrame((self.left, self.top))
        pygame.display.update(self.textFrame.get_rect())



    '''def InputText(self, event):
        input = self.text
        if event == pygame.K_BACKSPACE:
            input = input[:-1]
            self.NewText(input)
            #print(self.text, input, input[:-1])
        else:
            input += event.unicode
            self.NewText(input)
            #print(input)
        print(self.text, input, input[:-1])'''




    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        self.width, self.height = self.myText.get_width(), self.myText.get_height()

        if self.centerX and self.centerY == False:

            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)

            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY

        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)

            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX

        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)

        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
        
        else:
            self.left = self.posX
            self.top = self.posY









class WindowBox:
    def __init__(self, parent:Frame, width:int, height:int, mode:str, windowElements:list=[], fontSize:int=25, pourcentMode:bool=False, posX:int=0, posY:int=0, borderOffset:int=0, textBG:tuple=(255, 255, 255), centerX:bool=False, centerY:bool=False, imageWindow:pygame.image=None):
        self.parent = parent
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.width, self.height = width, height
        self.__InitPos()


        self.frame = Frame(self.parent, (self.width, self.height), (self.left, self.top), color=(1, 1, 1), surfImage=imageWindow)
        self.textFrame = Frame(self.frame.surfImage, (self.width - borderOffset * 2, self.height - borderOffset * 2), pos=(borderOffset, borderOffset), color=textBG)
        self.__borderOffset = borderOffset
        self.__mode = mode

        if self.__mode == "Dialog":
            self.__textsToDisplay = windowElements
            self.__dialogProgression = 0
            self.__textPlaceHolder = TextLabel(self.textFrame, self.__textsToDisplay[self.__dialogProgression], fontSize, (FONT_PATH), color=(0, 0, 0), posX=0, posY=0)

        elif self.__mode == "Menu":
            self.__menuOptionsLabel = windowElements
            self.__options = []

            if all(isinstance(element, list) for element in self.__menuOptionsLabel):
                for row in range(len(self.__menuOptionsLabel)):
                    self.__options.append([])
                    for column in self.__menuOptionsLabel[row]:
                        button = GfxButton(self.frame)
                        self.__options[row].append(button)

            else:
                for button in self.__menuOptionsLabel:
                    button = GfxButton(self.frame)
                    self.__options.append(button)




    """Public methods"""


    def ActiveWindow(self):
        self.frame.ActiveFrame()
        self.textFrame.ActiveFrame()
        self.frame.surfImage.blit(self.textFrame, (self.__borderOffset, self.__borderOffset))


            
    def NextDialog(self):
        self.__dialogProgression += 1
        if self.__dialogProgression > len(self.__textsToDisplay) - 1:
            return
        
        self.__textPlaceHolder.NewText(self.__textsToDisplay[self.__dialogProgression])


    


    def MenuSelection(self, rowSelector:int=0, columnSelector:int=0):
        rowSelector = max(min(rowSelector, len(self.__options), 0))
        columnSelector = max(min(columnSelector, len(self.__options), 0))


        if all(isinstance(element, list) for element in self.__menuOptionsLabel):
            self.__options[rowSelector][columnSelector].ActiveButton(focused=True)

        else:
            None


    
    def EndOfDialog(self):
        if self.__dialogProgression > len(self.__textsToDisplay) - 1:
            return True
    



    """Private methods"""


    def __InitPos(self):
        if self.centerX and self.centerY == False:

            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.parent.get_height() * ((self.posY)/100)) - int(self.height/2)

            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY

        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.parent.get_width() * ((self.posX)/100)) - int(self.width/2)

            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX

        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)

        elif self.pourcentMode:
            self.left = int(self.parent.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.parent.get_height() * ((self.posY)/100)) - int(self.height/2)
        
        else:
            self.left = self.posX
            self.top = self.posY









"""A 'Button' class, as its name implies it creates buttons :D"""
class Button:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, width:int, height:int, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False, color:tuple=(255,255,255),
     borderR:int=0, type:str="Bool", buttonLabel:str="Button", imageButton:str=None, func=None):

        self.frame = parent
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.width, self.height = width, height
        self.__InitPos()

        self.borderRad = borderR
        self.fill = color
        self.buttonType = type
        self.state = False
        self.label, self.activeLab, self.unactiveLab = buttonLabel, buttonLabel, buttonLabel
        self.command = func
        self.buttonFormat = None

        if imageButton != None:
            self.buttonFormat = pygame.image.load(imageButton).convert_alpha()
            self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
            self.frame.blit(self.buttonFormat, (self.left, self.top))
            self.isImage = True
        elif imageButton == None:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.isImage = False






    """Public methods"""

    #Detects if the object has been clicked, different behaviour depending on its type
    def Click(self):
        if pygame.mouse.get_pressed()[0] and self.buttonType == "Bool":
            if self.state == False:
                self.label = self.activeLab
                self.state = True
            else:
                self.label = self.unactiveLab
                self.state = False
            self.__DrawLabel(self.label)
            pygame.display.update()
            self.command()
            time.sleep(0.07)
        if pygame.mouse.get_pressed()[0] and self.buttonType == "OnClick":
            self.command()
            time.sleep(0.5)



    #Enables the button, called every frame in pygame's mainloop
    def ActiveButton(self, buttonClicked=None):
        self.activeLab = buttonClicked
        self.__Hover()
        """mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1])
        if self.isImage:
            imgPos = self.buttonFormat.get_rect().move(self.left, self.top)
            if imgPos.collidepoint(mousePosToFrame):
                self.Click()
        elif self.isImage == False and self.buttonFormat.collidepoint(mousePosToFrame):
            hover = (self.__Cap(self.fill[0]*1.2, 0, 255), self.__Cap(self.fill[1]*1.2, 0, 255), self.__Cap(self.fill[2]*1.2, 0, 255))
            self.buttonFormat = pygame.draw.rect(self.frame, hover, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            pygame.display.update()
            self.__DrawLabel(self.label)
            self.Click() 
        elif self.isImage == False:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.__DrawLabel(self.label)
            pygame.display.update()"""

    #Changes the image
    def ImgChange(self, newImage:str):
        self.buttonFormat = pygame.image.load(newImage).convert_alpha()
        self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
        self.frame.blit(self.buttonFormat, (self.left, self.top))





    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.centerX and self.centerY == False:
            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY
        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX
        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)
        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)
        else:
            self.left = self.posX
            self.top = self.posY



    #Sets up the label on the button wether if it's an image or a text
    def __DrawLabel(self, label, color=(0, 0, 0)):
        if isinstance(label, str) and "/" not in label:
            font = pygame.font.Font(FONT_PATH, 30)
            myText = font.render(label, True, color)
            if self.isImage:
                buttonTextLab = TextLabel(self.buttonFormat, label, 20, FONT_PATH, centerX=True, centerY=True)
            else:
                self.frame.blit(myText, myText.get_rect(center=self.buttonFormat.center))
        else:
            img = pygame.image.load(label).convert_alpha()
            img = pygame.transform.smoothscale(img, (self.width/2, self.height/2))
            self.frame.blit(img, img.get_rect(center=self.buttonFormat.center))



    def __Hover(self):
        mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1])
        if self.isImage:
            imgPos = self.buttonFormat.get_rect().move(self.left, self.top)
            if imgPos.collidepoint(mousePosToFrame):
                self.Click()
        elif self.isImage == False and self.buttonFormat.collidepoint(mousePosToFrame):
            hover = (self.__Cap(self.fill[0]*1.2, 0, 255), self.__Cap(self.fill[1]*1.2, 0, 255), self.__Cap(self.fill[2]*1.2, 0, 255))
            self.buttonFormat = pygame.draw.rect(self.frame, hover, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            pygame.display.update()
            self.__DrawLabel(self.label)
            self.Click() 
        elif self.isImage == False:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.__DrawLabel(self.label)
            pygame.display.update()

    #Caps the value passed in by 'min' and 'max'
    def __Cap(self, value, mini:int, maxi:int):    
        return max(min(maxi, value), mini)











"""Slider object"""
class Slider:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, length:int, total:int, axis:str, thickness:int=5, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False, color:tuple=(255,255,255),
     borderR:int=50, setterStyle:str="rect"):
        self.frame = parent
        self.length = length
        self.limit = total
        self.fill = color
        self.borderRad = borderR
        self.width, self.height = thickness, thickness
        frameW, frameH = self.width, self.height
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.orientation = axis
        self.setterStyle = setterStyle
        self.changing = False


        try:
            if setterStyle.lower() == "rect" or setterStyle.lower() == "circle":
                self.setterStyle = setterStyle
        except:
            exit(f"Variable 'setterStyle' must be either 'rect' or 'circle'")


        if self.orientation.lower() == "x":
            self.width = length
            frameW, frameH = self.width, self.height*3

        elif self.orientation.lower() == "y":
            self.height = length
            frameW, frameH = self.width*3, self.height

        self.__InitPos()


        self.slideFrame = Frame(self.frame, (frameW, frameH), (self.left, self.top), color=self.frame.get_SurfColor())
        self.slideValue = int((1/self.limit)*100)
        pygame.display.update()




    """Public methods"""



    #Update the value of the slider when called
    def Update(self, newTotal):
        self.limit = newTotal
        self.slideValue = 0
        progressColor = (self.__Cap(self.fill[0]*15, 0, 255), self.__Cap(self.fill[1]*15, 0, 255), self.__Cap(self.fill[2]*15, 0, 255))
        if self.orientation.lower() == "x":
            self.slideBarValue = pygame.draw.rect(self.frame, progressColor, pygame.Rect(self.left, self.top, int(self.width*(self.slideValue/100)), self.height), border_radius=self.borderRad)
        elif self.orientation.lower() == "y":
            self.slideBarValue = pygame.draw.rect(self.frame, progressColor, pygame.Rect(self.left, self.top, self.width, int(self.height*(self.slideValue/100))), border_radius=self.borderRad)
        self.slideBar = pygame.draw.rect(self.frame, (10, 10, 10), pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)



    #Enables the slider, called every frame in pygame's mainloop
    def ActiveSlider(self, progress:int=0):
        if progress != 0:
            self.slideValue = int((progress/self.limit)*100)
        self.__SetValue()
        self.slideFrame.ActiveFrame()
        self.slideFrame.fill(self.frame.get_SurfColor())
        pygame.display.update(self.slideFrame.get_rect())
    


    #Returns the slider's value
    def GetSlideValue(self):
        return self.slideValue



    #Returns if the slider is being clicked
    def GetChangingState(self):
        return self.changing





    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.centerX and self.centerY == False:

            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)

            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY

        elif self.centerY and self.centerX == False:
            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)

            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX

        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)

        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)

        else:
            self.left = self.posX
            self.top = self.posY



    #Sets the value of the slider, the slider works with three rectangles that are growing/shrinking/moving depending on its value
    def __SetValue(self):
        mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0]-self.slideFrame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1]-self.slideFrame.get_SurfPos()[1])
        progressColor = (self.__Cap(self.fill[0]*15, 0, 255), self.__Cap(self.fill[1]*15, 0, 255), self.__Cap(self.fill[2]*15, 0, 255))
        
        if self.orientation.lower() == "x":
            if pygame.mouse.get_pressed()[0] and (self.changing or self.slideBar.collidepoint(mousePosToFrame) or self.slideBarValue.collidepoint(mousePosToFrame)):
                self.changing = True
                self.slideValue = int((self.__Cap((mouse_pos[0]-self.frame.get_SurfPos()[0]-self.left), 0, self.width)/self.width)*100)
            elif pygame.mouse.get_pressed()[0] == False:
                self.changing = False

            setValue = self.__Cap(int(self.width*(self.slideValue/100)), 0, self.width)
            self.slideBarValue = pygame.draw.rect(self.slideFrame, progressColor, pygame.Rect(0, ((self.slideFrame.get_rect().height/2)-self.height/2), setValue, self.height), border_radius=self.borderRad)
            self.slideBar = pygame.draw.rect(self.slideFrame, (10, 10, 10), pygame.Rect(setValue, ((self.slideFrame.get_rect().height/2)-self.height/2), (self.width-setValue), self.height), border_radius=self.borderRad)
            if self.setterStyle.lower() == "rect":
                pygame.draw.rect(self.slideFrame, (150, 150, 150), pygame.Rect(setValue, 0, 3, self.slideFrame.get_rect().height), 5)
            elif self.setterStyle.lower() == "circle":
                pygame.draw.circle(self.slideFrame, (150, 150, 150), (setValue, self.slideFrame.get_rect().height/2), 5)
                   
        elif self.orientation.lower() == "y":
            if pygame.mouse.get_pressed()[0] and (self.changing or self.slideBar.collidepoint(mousePosToFrame) or self.slideBarValue.collidepoint(mousePosToFrame)):
                self.changing = True
                self.slideValue = int((self.__Cap(self.height-(mouse_pos[1]-self.frame.get_SurfPos()[1]-self.top), 0, self.height)/self.height)*100)
            elif pygame.mouse.get_pressed()[0] == False:
                self.changing = False

            setValue = self.height - self.__Cap(int(self.height*(self.slideValue/100)), 0, self.height)
            self.slideBarValue = pygame.draw.rect(self.slideFrame, progressColor, pygame.Rect(((self.slideFrame.get_rect().width/2)-self.width/2), self.height, self.width, -self.height+setValue), border_radius=self.borderRad)
            self.slideBar = pygame.draw.rect(self.slideFrame, (10, 10, 10), pygame.Rect(((self.slideFrame.get_rect().width/2)-self.width/2), 0, self.width, setValue), border_radius=self.borderRad)
            if self.setterStyle.lower() == "rect":
                pygame.draw.rect(self.slideFrame, (150, 150, 150), pygame.Rect(0, setValue, self.slideFrame.get_rect().width, 3), 5)
            elif self.setterStyle.lower() == "circle":
                pygame.draw.circle(self.slideFrame, (150, 150, 150), (self.slideFrame.get_rect().width/2, setValue), 5)
    


    #Caps the value passed in by 'min' and 'max'
    def __Cap(self, value, min:int= (-1000), max:int=0):
        if value > max:
            value = max
        elif value < min:
            value = min
        return value
    













"""For anti-aliased rounded shapes"""
class GfxButton:
    """Constructor"""
    def __init__(self, parent:Frame, width:int, height:int, pourcentMode:bool=False, posX:int=0, posY:int=0, centerX:bool=False, centerY:bool=False, color:tuple=(255,255,255),
     borderR:int=0, type:str="Bool", buttonLabel:str="Button", labelColor:tuple=(0, 0, 0), labelSize:int=20, imageButton:str=None, func=None, parentImage=False):

        self.frame = parent
        self.buttonFrame = None
        self.parentMidX, self.parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.centerX, self.centerY, self.pourcentMode, self.posX, self.posY = centerX, centerY, pourcentMode, posX, posY
        self.width, self.height = width, height
        self.__InitPos()
        self.labelSize = labelSize

        self.borderRad = borderR
        self.fill = color
        self.buttonType = type
        self.state = False
        self.label, self.activeLab, self.unactiveLab = buttonLabel, buttonLabel, buttonLabel
        self.labelColor = labelColor
        self.__command = func
        self.buttonFormat = None


        if imageButton != None:
            try:
                self.buttonFormat = pygame.image.load(imageButton).convert_alpha()
            except:
                self.buttonFormat = imageButton

            self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
            self.buttonFrame = Frame(self.frame, (self.width, self.height), (self.left, self.top), color=(1, 1, 1), surfImage=self.buttonFormat)
            self.dark = pygame.Surface(self.buttonFrame.get_SurfSize())
            self.dark.fill((40, 40, 40))
            self.dark.set_alpha(120)
            self.darkBlitted = False
            self.parentImage = parentImage
            self.isImage = True

        elif imageButton == None:
            if borderR != 0:
                cornerPosX = self.left
                cornerPosY = self.top

                for i in range(4):
                    if i == 1 or i == 2:
                        cornerPosX = self.left + self.width

                    else:
                        cornerPosX = self.left


                    if i == 2 or i == 3:
                        cornerPosY = self.top + self.height

                    else:
                        cornerPosY = self.top


                    gfxdraw.aacircle(self.frame, cornerPosX, cornerPosY, borderR-1, self.fill)
                    gfxdraw.filled_circle(self.frame, cornerPosX, cornerPosY, borderR-1, self.fill)

                    
                gfxdraw.box(self.frame, pygame.Rect(self.left-borderR, self.top, self.width+(borderR*2), self.height), self.fill)
                gfxdraw.box(self.frame, pygame.Rect(self.left, self.top-borderR, self.width, self.height+(borderR*2)), self.fill)


            self.buttonFormat = gfxdraw.box(self.frame, pygame.Rect(self.left, self.top, self.width, self.height), self.fill)
            self.isImage = False


    """Public methods"""

    #Detects if the object has been clicked, different behaviour depending on its type
    def Click(self, input:bool=False):
        if (pygame.mouse.get_pressed()[0] and self.buttonType == "Bool") or (input and self.buttonType == "Bool"):

            if self.state == False:
                self.label = self.activeLab
                self.state = True

            else:
                self.label = self.unactiveLab
                self.state = False
            self.__DrawLabel(self.label)
            pygame.display.update()
            self.__command()
            input = False
            time.sleep(0.07)


        if (pygame.mouse.get_pressed()[0] and self.buttonType == "OnClick") or (input and self.buttonType == "OnClick"):
            self.__command()
            input = False
            #time.sleep(0.5)



    #Enables the button, called every frame in pygame's mainloop
    def ActiveButton(self, unfocusedIsDarker:bool=True, focused:bool=False, focusedImage:pygame.image=None, buttonClicked:str=None):
        self.activeLab = buttonClicked
        #pygame.draw.rect(dark, (10, 10, 10, 125), dark.get_rect())
        if focused and focusedImage != None:
            self.buttonFrame.ActiveFrame(activeImage=focusedImage)
            self.__DrawLabel(self.label, surf=self.buttonFrame.activeSurfImage)
        elif focused:
            if unfocusedIsDarker:
                self.buttonFrame.surfImage.blit(self.buttonFormat, (0, 0))
            self.__DrawLabel(self.label, labelColor=self.labelColor)
            self.darkBlitted = False

        else:
            self.buttonFrame.ActiveFrame(parentIsFrameImage=self.parentImage)
            self.__DrawLabel(self.label, labelColor=self.labelColor)
            if unfocusedIsDarker and not self.darkBlitted:
                self.buttonFrame.surfImage.blit(self.dark, (0, 0))
                self.darkBlitted = True
            elif not unfocusedIsDarker:
                self.buttonFrame.blit(self.buttonFormat, (0, 0))

            #self.__Hover()

        pygame.display.update()



    def Command(self, func):
        self.__command = func



    #Changes the image
    def ImgChange(self, newImage:str):
        self.buttonFormat = pygame.image.load(newImage).convert_alpha()
        self.buttonFormat = pygame.transform.smoothscale(self.buttonFormat, (self.width, self.height))
        self.frame.blit(self.buttonFormat, (self.left, self.top))



    
    """Private methods (utility for the class)"""

    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.centerX and self.centerY == False:

            if self.pourcentMode:
                self.left = self.parentMidX-(self.width/2)
                self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)

            else:
                self.left = self.parentMidX-(self.width/2)
                self.top = self.posY

        elif self.centerY and self.centerX == False:

            if self.pourcentMode:
                self.top = self.parentMidY-(self.width/2)
                self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)

            else:
                self.top = self.parentMidY-(self.height/2)
                self.left = self.posX

        elif self.centerX and self.centerY:
            self.top = self.parentMidY-(self.height/2)
            self.left = self.parentMidX-(self.width/2)

        elif self.pourcentMode:
            self.left = int(self.frame.get_width() * ((self.posX)/100)) - int(self.width/2)
            self.top = int(self.frame.get_height() * ((self.posY)/100)) - int(self.height/2)

        else:
            self.left = self.posX
            self.top = self.posY



    #Sets up the label on the button wether if it's an image or a text
    def __DrawLabel(self, label, labelColor=(0, 0, 0), surf=None):
        if isinstance(label, str) and "/" not in label:
            font = pygame.font.Font(FONT_PATH, 30)
            myText = font.render(self.label, True, labelColor)


            if self.isImage:

                if surf != None:
                    TextLabel(surf, label, self.labelSize, FONT_PATH, centerX=True, centerY=True, color=labelColor)

                else:
                    TextLabel(self.buttonFrame.surfImage, label, self.labelSize, FONT_PATH, centerX=True, centerY=True, color=labelColor)

            else:
                self.frame.blit(myText, myText.get_rect(center=self.buttonFormat.center))

        else:
            img = pygame.image.load(label).convert_alpha()
            img = pygame.transform.smoothscale(img, (self.width/2, self.height/2))
            self.frame.blit(img, img.get_rect(center=self.buttonFormat.center))



    def __Hover(self):
        mouse_pos = pygame.mouse.get_pos()
        mousePosToFrame = (mouse_pos[0]-self.frame.get_SurfPos()[0], mouse_pos[1]-self.frame.get_SurfPos()[1])
        if self.isImage:
            imgPos = self.buttonFrame.get_rect()
            self.__DrawLabel(self.label)

            if imgPos.collidepoint(mousePosToFrame):
                self.Click()

        elif self.isImage == False and self.buttonFormat.collidepoint(mousePosToFrame):
            hover = (self.__Cap(self.fill[0]*1.2, 0, 255), self.__Cap(self.fill[1]*1.2, 0, 255), self.__Cap(self.fill[2]*1.2, 0, 255))
            self.buttonFormat = pygame.draw.rect(self.frame, hover, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            pygame.display.update()
            self.__DrawLabel(self.label)
            self.Click() 

        elif self.isImage == False:
            self.buttonFormat = pygame.draw.rect(self.frame, self.fill, pygame.Rect(self.left, self.top, self.width, self.height), border_radius=self.borderRad)
            self.__DrawLabel(self.label)
            pygame.display.update()



    #Caps the value passed in by 'min' and 'max'
    def __Cap(self, value, mini:int, maxi:int):
        return max(min(maxi, value), mini)












class GridMap:
    """Constructor"""
    def __init__(self, parent:pygame.Surface, cellSize:tuple, posX:int, posY:int, nColumns:int, nRows:int, centerX:bool=False, centerY:bool=False, pourcentMode:bool=False, 
    cellGap:int=0, gridBG:tuple=(5, 5, 5)):
        self.frame = parent
        self.__cell = cellSize
        self.__cellGap = cellGap
        self.__gridBG = gridBG
        self.__parentMidX, self.__parentMidY = parent.get_rect().centerx, parent.get_rect().centery
        self.__centerX, self.__centerY, self.__pourcentMode, self.__posX, self.__posY = centerX, centerY, pourcentMode, posX, posY
        self.nColumns, self.nRows = nColumns, nRows
        self.__InitPos()

        self.gridSurf = Frame(self.frame, ((self.__cell[0]+self.__cellGap) * self.nColumns, (self.__cell[1]+self.__cellGap) * self.nRows), (self.left, self.top), self.__gridBG)
        self.__InitGrid()

        self.gridSurf.ActiveFrame()
    





    def GridUpdate(self):
        self.__InitGrid()
        self.gridSurf.ActiveFrame()
        self.gridSurf.fill(self.__gridBG)
        pygame.display.update(self.gridSurf.get_rect())




    """Private methods (utility for the class)"""
    
    #Places the object (sets up 'self.left' and 'self.top')
    def __InitPos(self):
        if self.__centerX and self.__centerY == False:

            if self.__pourcentMode:
                self.left = self.__parentMidX-(self.nRows/2)
                self.top = int(self.frame.get_height() * ((self.__posY)/100)) - int(self.nRows/2)

            else:
                self.left = self.__parentMidX-(self.nRows/2)
                self.top = self.__posY
                
        elif self.__centerY and self.__centerX == False:
            if self.__pourcentMode:
                self.top = self.__parentMidY-(self.nRows/2)
                self.left = int(self.frame.get_width() * ((self.__posX)/100)) - int(self.nRows/2)

            else:
                self.top = self.__parentMidY-(self.nRows/2)
                self.left = self.__posX

        elif self.__centerX and self.__centerY:
            self.top = self.__parentMidY-(self.nRows/2)
            self.left = self.__parentMidX-(self.nRows/2)

        elif self.__pourcentMode:
            self.left = int(self.frame.get_width() * ((self.__posX)/100)) - int(self.nRows/2)
            self.top = int(self.frame.get_height() * ((self.__posY)/100)) - int(self.nRows/2)

        else:
            self.left = self.__posX
            self.top = self.__posY



    #Creates the grid depending on defined cell size and number of columns/rows
    def __InitGrid(self):
        for row in range(0, self.nColumns):
            for column in range(0, self.nRows):
                cellRect = pygame.Rect((self.__cell[0]+self.__cellGap) * row, (self.__cell[1]+self.__cellGap) * column, self.__cell[0], self.__cell[1])
                gfxdraw.rectangle(self.gridSurf, cellRect, (15, 15, 15))






    