import tkinter as tk
import resizing
import main_memory
import time
import threading

class Application(tk.Frame):
    def __init__(self, master=None, clock=1/(6)):
        super().__init__(master)
        self.master = master
        self.master.title("Memory System")
        #self.master.attributes("-zoomed", True)
        #self.master.resizable(False, False)
        self.pack()
        self.clock = clock
        self.mem = main_memory.Memory(self.clock) 
        #   
        self.mem.write('0000', 'ABCD')
        self.mem.write('0001', 'FBCE')
        self.mem.write('0010', 'EBCF')
        self.mem.write('0011', 'EECD')
        #

        self.dad_frame = tk.Frame(self.master)
        self.dad_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.dad_canvas = resizing.ResizingCanvas(self.dad_frame,
            width=1280, height=720, highlightthickness=0)
        self.dad_canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.create_frames()
        
    def create_frames(self):
        print(root.winfo_width(), root.winfo_height())
        self.canvas_bus = tk.Canvas(self.dad_canvas, width=self.winfo_screenwidth(), height=330)
        self.canvas_bus.place(x=self.winfo_screenwidth()/12, y=3*self.winfo_screenheight()/8)
        self.canvas_bus.create_rectangle(0, 150, 8*self.winfo_screenwidth()/10, 190, fill='gray')
        self.canvas_bus.create_rectangle(30, 0, 40, 150, fill='gray')
        self.canvas_bus.create_rectangle(500, 0, 510, 150, fill='gray')
        self.canvas_bus.create_rectangle(980, 0, 990, 150, fill='gray')
        self.canvas_bus.create_rectangle(1500, 0, 1510, 150, fill='gray')
        self.canvas_bus.create_rectangle(700, 190, 710, 330, fill='gray')

        self.p1 = tk.Frame(self.dad_canvas, width=self.winfo_screenwidth()/5, 
            height=400, bg="white")
        self.p1.place(x=20, y=20)

        self.p2 = tk.Frame(self.dad_canvas, width=self.winfo_screenwidth()/5,
            height=400, bg="white")
        self.p2.place(x=self.winfo_screenwidth()/4+10, y=20)
        self.p3 = tk.Frame(self.dad_canvas, width=self.winfo_screenwidth()/5,
            height=400, bg="white")
        self.p3.place(x=2*self.winfo_screenwidth()/4+10, y=20) 
        self.p4 = tk.Frame(self.dad_canvas, width=self.winfo_screenwidth()/5,
            height=400, bg="white")
        self.p4.place(x=3*self.winfo_screenwidth()/4+10, y=20)  
        
        self.frame_mem = tk.Frame(self.dad_canvas)
        self.frame_mem.place(x=self.winfo_screenwidth()/3, y=self.winfo_screenheight()/1.5)
        self.gui_mem()

        self.dad_canvas.addtag_all("all")
        self.canvas_bus.addtag_all("all")
        
    def gui_proc(self):
        pass
    def gui_mem(self):
        for i in range(8): 
            for j in range(2):
                l = tk.Label(self.frame_mem, text= "{0000:b}".format(j+i*2))
                e = tk.Entry(self.frame_mem, fg='blue', 
                            font=('Arial',16,'bold')) 
                l.grid(row=i, column=j*2)
                e.grid(row=i, column=j*2+1)
                e.insert(tk.END, self.mem.mem[j+i*2])
        root.after(1000, self.gui_mem)

root = tk.Tk()
app = Application(master=root)

app.mainloop()
