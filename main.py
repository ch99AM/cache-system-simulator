import tkinter as tk
import resizing

class Application(tk.Frame):
    def __init__(self, master=None, clock=1):
        super().__init__(master)
        self.master = master
        self.master.title("Memory System")
        self.master.attributes("-zoomed", True)
        self.master.resizable(False, False)
        
        self.dad_frame = tk.Frame(self.master)
        self.dad_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.pack()
        self.create_frames()
        self.clock = clock

    def create_frames(self):

        self.canvas_bus = tk.Canvas(self.master, width=self.winfo_screenwidth(), height=330)
        self.canvas_bus.place(x=self.winfo_screenwidth()/12, y=3*self.winfo_screenheight()/8)
        self.canvas_bus.create_rectangle(0, 150, 7*self.winfo_screenwidth()/9, 190, fill='gray')
        self.canvas_bus.create_rectangle(30, 0, 40, 150, fill='gray')
        self.canvas_bus.create_rectangle(450, 0, 460, 150, fill='gray')
        self.canvas_bus.create_rectangle(900, 0, 910, 150, fill='gray')
        self.canvas_bus.create_rectangle(1390, 0, 1400, 150, fill='gray')
        self.canvas_bus.create_rectangle(700, 190, 710, 330, fill='gray')

        self.p1 = tk.Frame(self.canvas_bus, width=self.winfo_screenwidth()/5, 
            height=400, bg="white")
        self.p1.place(x=20, y=20)
        self.p2 = tk.Frame(self.master, width=self.winfo_screenwidth()/5,
            height=400, bg="white")
        self.p2.place(x=self.winfo_screenwidth()/4+10, y=20)
        self.p3 = tk.Frame(self.master, width=self.winfo_screenwidth()/5,
            height=400, bg="white")
        self.p3.place(x=2*self.winfo_screenwidth()/4+10, y=20) 
        self.p4 = tk.Frame(self.master, width=self.winfo_screenwidth()/5,
            height=400, bg="white")
        self.p4.place(x=3*self.winfo_screenwidth()/4+10, y=20)  
        
        self.frame_mem = tk.Frame(self.master, bg="yellow")
        self.frame_mem.place(x=self.winfo_screenwidth()/3, y=self.winfo_screenheight()/1.5)
        self.gui_mem()

        
    def gui_proc(self):
        pass
    def gui_mem(self): 
        for i in range(8): 
            for j in range(2):
                e = tk.Entry(self.frame_mem, width=20, fg='blue', 
                               font=('Arial',16,'bold')) 
                e.grid(row=i, column=j)
                e.insert(tk.END, "1234") 

root = tk.Tk()
app = Application(master=root)
app.mainloop()