#Michael Pereira III

#
#
#
#
# MICHAEL GUI IMPORTS
#
#
#
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from tkinter import *
from tkinter import Tk, Label, Button, StringVar
from tkinter import ttk
import tkinter as tk

import tkinter.filedialog
from tkinter import filedialog

from tkinter import Menu

import urllib
import json


#For images
import PIL
from PIL import ImageTk, Image

import pandas as pd
import numpy as np




#
# CAMERON GUI IMPORTS
#



from recordNotes import *
from PlayWAVFile import playWAV
from PlayWAVFile import playSpace
from playSongFile import playSong
from covfefe import callCovfefe
from mixTracks import addToSong
from ResetMySong import resetSong
from ResetMySong import exportSong

xvalue = 0
yvalue = 0
zvalue = 0


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize = (5,5), dpi = 100)
a = f.add_subplot(111)

def animate(i):
        pullData = open("sampleData.txt", "r").read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
                if len(eachLine) > 1:
                        x, y = eachLine.split(',')
                        xList.append(int(x))
                        yList.append(int(y))
        a.clear()
        a.plot(xList, yList)





class ThreeDSynth(tk.Tk):
        def __init__(self, *args, **kwargs):
                tk.Tk.__init__(self, *args, **kwargs)

                tk.Tk.iconbitmap(self, "eighthnote.ico")
                tk.Tk.wm_title(self, "3D Synth")

                container = tk.Frame(self)
                container.pack(side = "top", fill = "both", expand = True)
                container.grid_rowconfigure(0, weight = 1)
                container.grid_columnconfigure(0, weight = 1)

                self.frames = {}

                for F in (StartPage, HomePage, PageOne, RecordPage, LocalizePage, FinalizeTrackPage, TrackPage):

                        frame = F(container, self)

                        self.frames[F] = frame

                        frame.grid(row = 0, column = 0, sticky = "nsew")

                self.show_frame(StartPage)

        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()





class StartPage(tk.Frame):

        def __init__(self, parent, controller):
                #parent is name of parent class (ThreeDSynth)
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "Welcome to 3D Synth, an app that lets you create your own 3D song!", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)

                button1 = tk.Button(self, text = "Get started", command = lambda:  controller.show_frame(HomePage))
                button1.pack()

                button2 = tk.Button(self, text = "Exit", command = quit)
                button2.pack()



                #homeImage = ImageTk.PhotoImage(Image.open("homepicture.jpg"))

                #panel = tk.Label(self, image = homeImage)

                #panel.pack(side = "bottom", fill = "both", expand = "yes")





class LocalizePage(tk.Frame):




        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "Using the X, Y, and Z sliders to localize your track in 3D space", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)

                #button2 = ttk.Button(self, text = "Stop")
                #button2.pack()

                def submitTrack():
                    callCovfefe(w1.get(),w2.get(),w3.get())
                    controller.show_frame(FinalizeTrackPage)

                def playLocalTrack():
                    callCovfefe(w1.get(),w2.get(),w3.get())
                    playSpace()


                button1 = tk.Button(self, text = "Play", command = playLocalTrack)
                button1.pack()

                button3 = tk.Button(self, text = "Done", command = submitTrack)
                button3.pack()

                def w1value():
                        yvalue = w1.get()
                        print(yvalue)
                def w2value():
                        xvalue = w2.get()
                        print(xvalue)
                def w3value():
                        zvalue =w3.get()
                        print(zvalue)



                w2 = Scale(self, from_ = -180, to = 180, length=300, tickinterval = 30 )
                w2.config(label = 'Y-axis')
                w2.pack()


                #button4 = tk.Button(self, text = "Confirm Y", command = w1value)
                #button4.pack()


                w1 = Scale(self, from_=-180, to=180, length=600,tickinterval=30, orient=HORIZONTAL)
                w1.config(label = 'X-axis')
                w1.pack()

                #button5 = tk.Button(self, text = "Confirm X", command = w2value)
                #button5.pack()

                w3 = Scale(self, from_=-180, to=180, length=600,tickinterval=30, orient=HORIZONTAL)
                w3.config(label = 'Z-axis')
                w3.pack()

                #button6 = tk.Button(self, text = "Confirm Z", command = w3value)
                #button6.pack()






class RecordPage(tk.Frame):

        def __init__(self,parent, controller):
                tk.Frame.__init__(self,parent)
                label = tk.Label(self, text = "Record a new track for your song!", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)

                button1 = tk.Button(self, text = "Record SIN", command = recordSIN)
                button1.pack()

                button2 = tk.Button(self, text = "Record SQUARE", command = recordSQUARE)
                button2.pack()

                button7 = tk.Button(self, text = "Record SAW", command = recordSAW)
                button7.pack()

                button3 = tk.Button(self, text = "Playback track", command = playWAV)
                button3.pack()

                button4 = tk.Button(self, text = "Localize track", command = lambda: controller.show_frame(LocalizePage))
                button4.pack()


                button5 = tk.Button(self, text = "Previous page", command = lambda: controller.show_frame(RecordPage))

                button6 = tk.Button(self, text = "Return to main page", command = lambda: controller.show_frame(HomePage))
                button6.pack()


                canvas = FigureCanvasTkAgg(f, self)
                canvas.show()
                canvas.get_tk_widget().pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)


##                toolbar = NavigationToolbar2TkAgg(canvas, self)
##                toolbar.update()
##                canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)



class FinalizeTrackPage(tk.Frame):

        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "Finalize the current track", font = LARGE_FONT)

                button1 = tk.Button(self, text = "Add track to song", command =  lambda: [addToSong(), controller.show_frame(HomePage)])
                button1.pack()

                button2 = tk.Button(self, text = "Discard track", command = lambda: controller.show_frame(HomePage))
                button2.pack()



class TrackPage(tk.Frame):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "Here all the current tracks you've recorded for your song!", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)

                button1 = tk.Button(self, text = "Edit a track")
                button1.pack()

                button2 = tk.Button(self, text = "Record new track", command = lambda: controller.show_frame(RecordPage))
                button2.pack()

                button3 = tk.Button(self, text = "Play song")
                button3.pack()

                button4 = tk.Button(self, text = "Previous page", command = lambda: controller.show_frame(PageOne))
                button4.pack()



class HomePage(tk.Frame):

        def __init__(self,parent, controller):
                tk.Frame.__init__(self,parent)
                label = tk.Label(self, text = "Start a new song, add to your current song, or play your current song", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)

                #For Home button

                button5 = tk.Button(self, text = "Start New Song", command = resetSong)
                button5.pack()

                button2 = tk.Button(self, text = "Play Current Song", command = playSong)
                button2.pack()

                button3 = tk.Button(self, text = "Add track to current song", command = lambda: controller.show_frame(RecordPage))
                button3.pack()

                button4 = tk.Button(self, text = "Export Song", command = exportSong)
                button4.pack()

                button1 = tk.Button(self, text = "Return to Home", command = lambda:  controller.show_frame(StartPage))
                button1.pack()




class PageOne(tk.Frame):

        def __init__(self,parent, controller):
                tk.Frame.__init__(self,parent)
                label = tk.Label(self, text = "Add to your song or play every track in your song!", font = LARGE_FONT)
                label.pack(pady = 10, padx = 10)

                button1 = tk.Button(self, text = "Add to song", command = lambda:  controller.show_frame(RecordPage))
                button1.pack()

                button2 = tk.Button(self, text = "Play Song", command = lambda: controller.show_frame(TrackPage))
                button2.pack()




app = ThreeDSynth()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
