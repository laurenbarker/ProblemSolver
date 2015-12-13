#!/usr/bin/python

import Tkinter
top = Tkinter.Tk()

C = Tkinter.Canvas(top, bg="grey", height=250, width=300)

square = C.create_polygon(10, 10, 20, 10, 20, 20, 10, 20)

C.pack()

top.mainloop()
