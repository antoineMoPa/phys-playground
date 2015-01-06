# run specifying number of frames to render
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import math
import os
import sys
from copy import *

class Waves:
    def __init__(self,w,h):
        self.w, self.h = w,h
        self.data = np.zeros( (self.w,self.h,3), dtype=np.uint8)        
        self.time = 0
        self.interval = 0.2
        self.heights = np.ones( (self.w,self.h), dtype=np.float32)
        self.speeds = np.zeros( (self.w,self.h), dtype=np.float32)
        self.damping = 1
        
        self.heights /= 2
        
        self.point(self.w/2,self.h/4,8,1)
        
        self.image = 0
        
        if not os.path.exists("./images"):
            os.makedirs("./images")
            
        
        
        #for i in range(frames)
        #    self.outputImg()
        #    self.iterate()

    def outputImg(self):
        img = self.getImage()
        img.save('./images/test'+str(self.image).zfill(6)+'.png')
        self.image += 1
    def getImage(self):
        self.draw()
        return Image.fromarray(self.data,'RGB')
    def point(self,i,j,radius,value):
        i = math.floor(i)
        j = math.floor(j)
        for k in range(i - radius,i + radius):
            for l in range(j - radius,j + radius):
                d = self.dist(i,j,k,l)
                if(d < radius):
                    self.heights[k][l] += value * (1-d / radius)
                    
    def dist(self,x1,y1,x2,y2):
        return math.sqrt(math.pow(x2 - x1,2) + math.pow(y2 - y1,2))
        
    def iterate(self):
        # we equilibrate with 4 cells so we divide effect of each cell by 4
        factor = 1/4
        self.time += self.interval
        speeds = self.speeds
        heights = self.heights
        damping = self.damping
        
        # When I wrote that code, only god and I knew what it meant
        # now only god knows
        
        # find difference
        # multiply difference by factor
        # add it to speed
        # substract speed to neighbours
        
        h1 = np.roll(np.copy(heights),1,axis=0)
        h2 = np.roll(np.copy(heights),-1,axis=0)
        h3 = np.roll(np.copy(heights),1,axis=1)
        h4 = np.roll(np.copy(heights),-1,axis=1)

        d1 = factor * (heights - h1)
        d2 = factor * (heights - h2)
        d3 = factor * (heights - h3)
        d4 = factor * (heights - h4)
   
        speeds -= d1
        speeds -= d2
        speeds -= d3
        speeds -= d4
        
        speeds += np.roll(d1,-1,axis=0)
        speeds += np.roll(d2,1,axis=0)
        speeds += np.roll(d3,-1,axis=1)
        speeds += np.roll(d4,1,axis=1)
        
        speeds *= damping
        heights += speeds                

    def draw(self):        
        self.data[:,:,0] = np.floor(self.heights * 255)
        self.data[:,:,1] = np.floor(self.speeds * 255)
        self.data[:,:,2] = np.floor(self.heights * 255)

class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.waves = Waves(400,400)
        self.createWidgets()
        
        self.image = None

    def iterate(self):
        self.waves.iterate()
        self.putWavesImage()

    def putWavesImage(self):
        self.image = ImageTk.PhotoImage(self.waves.getImage())
        self.canvas.create_image(200,200,image = self.image)

    def createWidgets(self):
        self.iterate_btn = tk.Button(self)
        self.iterate_btn["text"] = "Iterate"
        self.iterate_btn["command"] = self.iterate
        self.iterate_btn.pack()
        
        self.canvas = tk.Canvas(self,
                                width = self.waves.w, 
                                height = self.waves.h)

        self.putWavesImage()
        self.canvas.pack()
        
app = Application()
app.master.title("Waves")
app.mainloop()


# get number of frames in argument
#num = 100
#w = Waves(100,100,num)
#print ("to generate gif:")
#print ("convert -delay 2 -loop 0 -layers optimize-frame -fuzz 50% images/*.png animat#ion.gif")
