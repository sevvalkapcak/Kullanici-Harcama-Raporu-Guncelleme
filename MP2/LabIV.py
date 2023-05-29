import tkinter as tk

class PlotEkrani(tk.Frame):
    
    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, background="blue")
        self.parent = parent
        self.width  = width
        self.height = height
        self.fill_color = "red"
        self.yazi_handles = []
        self.pack()
        self.initGui()

    def initGui(self):
        self.canvas_bg = tk.Canvas(self, width=self.width, height=self.height)
        # self.canvas_bg.create_rectangle(3, self.height-3, self.width-3, 3,
                                # outline="blue", fill="white", width=2)
        self.canvas_bg.pack()

    def bar_diagram(self, data= [90, 100, 80, 90, 100]):


        x_poses = range(0, self.width, int(self.width/len(data)))
        x_width = x_poses[1] *0.9

        for i, y in enumerate(data):
            # calculate reactangle coordinates (integers) for each bar
            x0 = x_poses[i]
            y1 = (100 - y) * self.height / 100
            x1 = x_poses[i] + x_width
            y0 = self.height
            # draw the bar
            self.canvas_bg.create_rectangle(x0, y0, x1, y1, fill=self.fill_color)
            # put the y value above each bar
            self.yazi_handles.append( self.canvas_bg.create_text(
                x0+x_width/2, y0, anchor=tk.SW, text=str(y), fill=self.fill_color))
        
        self.canvas_bg.bind("<Button-1>", self.button_click)
        self.canvas_bg.bind("<Enter>", self.mouse_on)
        self.canvas_bg.bind("<Leave>", self.mouse_off)

    def mouse_on(self, event):
        for yazi in self.yazi_handles:
            self.canvas_bg.itemconfig(yazi, fill= "white")
    
    def mouse_off(self, event):
        for yazi in self.yazi_handles:
            self.canvas_bg.itemconfig(yazi, fill= self.fill_color)

    def button_click(self, event):
        posx = event.x
        posy = event.y
        self.item_handle = self.canvas_bg.find_closest(posx, posy)
        self.canvas_bg.itemconfig(self.item_handle, fill="blue")
        self.canvas_bg.tag_bind(
            self.item_handle, "<ButtonRelease-1>", self.button_released)



    def button_released(self, event):
        self.canvas_bg.itemconfig(self.item_handle, fill=self.fill_color)
      



