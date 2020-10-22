import tkinter as tk
import threading
import resizing

import numpy as np

import bus

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Memory System")
        self.master.resizable(False, False)
        self.pack()  
        
        self.stopped = threading.Event()
        self.ins_to_send = bus.p.Inst()
        
        self.dad_frame = tk.Frame(self.master)
        self.dad_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.dad_canvas = resizing.ResizingCanvas(self.dad_frame,
            width=1200, height=700, highlightthickness=0)
        self.dad_canvas.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.thread1 = threading.Thread()
        self.thread2 = threading.Thread()
        self.thread3 = threading.Thread()
        self.thread4 = threading.Thread()
        
        self.create_frames()
        
    def create_frames(self):        
        self.canvas_bus = tk.Canvas(self.dad_canvas, width=1100, height=330)
        self.canvas_bus.place(x=self.winfo_screenwidth()/12, y=230)
        self.canvas_bus.create_rectangle(2, 150, 980, 190, fill='gray')
        self.canvas_bus.create_rectangle(30, 80, 40, 150, fill='gray')
        self.canvas_bus.create_rectangle(330, 80, 340, 150, fill='gray')
        self.canvas_bus.create_rectangle(640, 80, 650, 150, fill='gray')
        self.canvas_bus.create_rectangle(940, 80, 950, 150, fill='gray')
        self.canvas_bus.create_rectangle(520, 190, 530, 330, fill='gray')

        self.fp1 = tk.Frame(self.dad_canvas, width=240, height=310, bg="white")
        self.fp1.place(x=20, y=20)
        
        self.fp2 = tk.Frame(self.dad_canvas, width=240, height=310, bg="white")
        self.fp2.place(x=330, y=20)
        
        self.fp3 = tk.Frame(self.dad_canvas, width=240, height=310, bg="white")
        self.fp3.place(x=640, y=20) 
        
        self.fp4 = tk.Frame(self.dad_canvas, width=240, height=310, bg="white")
        self.fp4.place(x=940, y=20)  
        
        self.frame_mem = tk.Frame(self.dad_canvas)
        self.frame_mem.place(x=370, y=460)

        self.dad_canvas.addtag_all("all")
        self.canvas_bus.addtag_all("all")
        
        tk.Label(self.fp1, text= 'P1', bg="white", font="none 18 bold").place(x=100, y=0)
        tk.Label(self.fp2, text= 'P2', bg="white", font="none 18 bold").place(x=100, y=0)
        tk.Label(self.fp3, text= 'P3', bg="white", font="none 18 bold").place(x=100, y=0)
        tk.Label(self.fp4, text= 'P4', bg="white", font="none 18 bold").place(x=100, y=0)
        
        #modes
        tk.Button(self.dad_canvas, text ="Num ciclos", command = self.run_cycles).place(x=100, y=500)
        self.cycles = tk.Entry(self.dad_canvas, fg='blue', width=5,font=('Arial',14,'bold'))
        self.cycles.place(x=10,y=500)
        self.cycles.insert(tk.END, '10') #default
        tk.Button(self.dad_canvas, text ="Paso->", command = self.step).place(x=100, y=550)
        tk.Button(self.dad_canvas, text ="Continuo", command = self.run_contiuos).place(x=100, y=600)
        tk.Button(self.dad_canvas, text ="Pausa", command = self.pause).place(x=200, y=600)
        self.ins_entry = tk.Entry(self.dad_canvas, fg='blue', width=20,font=('Arial',12,'bold'))
        self.ins_entry.place(x=100,y=640)
        self.gui_mem()
        self.gui_proc()
    
    def gui_proc(self):
        # Instruction label
        str_ins = 'U: '+bus.p1.ins[-2].num_proc+": "+bus.p1.ins[-2].op+" "+\
                    bus.p1.ins[-2].data+" "+bus.p1.ins[-2].dir
        l = tk.Label(self.fp1, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=70)
        str_ins = 'A: '+bus.p1.ins[-1].num_proc+": "+bus.p1.ins[-1].op+" "+\
                    bus.p1.ins[-1].data+" "+bus.p1.ins[-1].dir
        l = tk.Label(self.fp1, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=110)
        clk = 'clk: '+str(bus.p1.counter)
        if self.thread1.is_alive():
            tk.Label(self.fp1,text=clk,bg='green',font=('Arial', 12, 'bold')).place(x=180, y=10)
        else:
            tk.Label(self.fp1,text=clk,bg='red',font=('Arial', 12, 'bold')).place(x=180, y=10)
        
        str_ins = 'U: '+bus.p2.ins[-2].num_proc+": "+bus.p2.ins[-2].op+" "+\
                    bus.p2.ins[-2].data+" "+bus.p2.ins[-2].dir
        l = tk.Label(self.fp2, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=70)
        str_ins = 'A: '+bus.p2.ins[-1].num_proc+": "+bus.p2.ins[-1].op+" "+\
                    bus.p2.ins[-1].data+" "+bus.p2.ins[-1].dir
        l = tk.Label(self.fp2, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=110)
        clk = 'clk: '+str(bus.p2.counter)
        if self.thread2.is_alive():
            tk.Label(self.fp2,text=clk,bg='green',font=('Arial', 12, 'bold')).place(x=180, y=10)
        else:
            tk.Label(self.fp2,text=clk,bg='red',font=('Arial', 12, 'bold')).place(x=180, y=10)

        str_ins = 'U: '+bus.p3.ins[-2].num_proc+": "+bus.p3.ins[-2].op+" "+\
                    bus.p3.ins[-2].data+" "+bus.p3.ins[-2].dir
        l = tk.Label(self.fp3, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=70)
        str_ins = 'A: '+bus.p3.ins[-1].num_proc+": "+bus.p3.ins[-1].op+" "+\
                    bus.p3.ins[-1].data+" "+bus.p3.ins[-1].dir
        l = tk.Label(self.fp3, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=110)
        clk = 'clk: '+str(bus.p3.counter)
        if self.thread3.is_alive():
            tk.Label(self.fp3,text=clk,bg='green',font=('Arial', 12, 'bold')).place(x=180, y=10)
        else:
            tk.Label(self.fp3,text=clk,bg='red',font=('Arial', 12, 'bold')).place(x=180, y=10)

        str_ins = 'U: '+bus.p4.ins[-2].num_proc+": "+bus.p4.ins[-2].op+" "+\
                    bus.p4.ins[-2].data+" "+bus.p4.ins[-2].dir
        l = tk.Label(self.fp4, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=70)
        str_ins = 'A: '+bus.p4.ins[-1].num_proc+": "+bus.p4.ins[-1].op+" "+\
                    bus.p4.ins[-1].data+" "+bus.p4.ins[-1].dir
        l = tk.Label(self.fp4, width=20,text=str_ins , font=('Arial', 12, 'bold'))
        l.place(x=15, y=110)
        clk = 'clk: '+str(bus.p4.counter)
        if self.thread4.is_alive():
            tk.Label(self.fp4,text=clk,bg='green',font=('Arial', 12, 'bold')).place(x=180, y=10)
        else:
            tk.Label(self.fp4,text=clk,bg='red',font=('Arial', 12, 'bold')).place(x=180, y=10)        
        
        for i in range(2): 
            for j in range(2):
                #Caches block
                l = tk.Label(self.fp1, text= "{0000:b}".format(j+i*2))
                e = tk.Entry(self.fp1, fg='blue', width=35,
                            font=('Arial',14,'bold')) 
                axe_y = 170+(j+i*2)*30
                l.place(x=5, y=axe_y)
                e.place(x=30, y=axe_y)
                str_block = bus.p1.c_mem.mem[i][j][1]+" "+\
                    bus.p1.c_mem.mem[i][j][2]+" "+bus.p1.c_mem.mem[i][j][3]
                e.insert(tk.END, str_block)
                
                l = tk.Label(self.fp2, text= "{0000:b}".format(j+i*2))
                e = tk.Entry(self.fp2, fg='blue', width=35,
                            font=('Arial',14,'bold')) 
                axe_y = 170+(j+i*2)*30
                l.place(x=5, y=axe_y)
                e.place(x=30, y=axe_y)
                str_block = bus.p2.c_mem.mem[i][j][1]+" "+\
                    bus.p2.c_mem.mem[i][j][2]+" "+bus.p2.c_mem.mem[i][j][3]
                e.insert(tk.END, str_block)
                
                l = tk.Label(self.fp3, text= "{0000:b}".format(j+i*2))
                e = tk.Entry(self.fp3, fg='blue', width=35,
                            font=('Arial',14,'bold')) 
                axe_y = 170+(j+i*2)*30
                l.place(x=5, y=axe_y)
                e.place(x=30, y=axe_y)
                str_block = bus.p3.c_mem.mem[i][j][1]+" "+\
                    bus.p3.c_mem.mem[i][j][2]+" "+bus.p3.c_mem.mem[i][j][3]
                e.insert(tk.END, str_block)
                
                l = tk.Label(self.fp4, text= "{0000:b}".format(j+i*2))
                e = tk.Entry(self.fp4, fg='blue', width=35,
                            font=('Arial',14,'bold')) 
                axe_y = 170+(j+i*2)*30
                l.place(x=5, y=axe_y)
                e.place(x=30, y=axe_y)
                str_block = bus.p4.c_mem.mem[i][j][1]+" "+\
                    bus.p4.c_mem.mem[i][j][2]+" "+bus.p4.c_mem.mem[i][j][3]
                e.insert(tk.END, str_block)
        root.after(2000, self.gui_proc)
        
    def gui_mem(self):
        for i in range(8): 
            for j in range(2):
                l = tk.Label(self.frame_mem, text= "{0000:b}".format(j+i*2))
                e = tk.Entry(self.frame_mem, fg='blue', 
                            font=('Arial',16,'bold')) 
                l.grid(row=i, column=j*2)
                e.grid(row=i, column=j*2+1)
                e.insert(tk.END, bus.main_mem.mem[j+i*2])
        root.after(2000, self.gui_mem)
        
    def run_cycles(self):
        cycles = int(self.cycles.get())
        if  cycles != '': 
            self.thread1 = threading.Thread(target = bus.p1.num_cycles, args = (cycles, ), daemon = True)
            self.thread2 = threading.Thread(target = bus.p2.num_cycles, args = (cycles, ), daemon = True)
            self.thread3 = threading.Thread(target = bus.p3.num_cycles, args = (cycles, ), daemon = True)
            self.thread4 = threading.Thread(target = bus.p4.num_cycles, args = (cycles, ), daemon = True)
            self.thread1.start()
            self.thread2.start()
            self.thread3.start()
            self.thread4.start()
            
    def step(self):
        ins = self.ins_entry.get()
        if ins != '':
            self.ins_entry.delete(0, 'end')
            ins = ins.split()
        else: 
            ins = 'none'
        self.thread1 = threading.Thread(target = bus.p1.step, args = (ins,), daemon = True)
        self.thread2 = threading.Thread(target = bus.p2.step, args = (ins,), daemon = True)
        self.thread3 = threading.Thread(target = bus.p3.step, args = (ins,), daemon = True)
        self.thread4 = threading.Thread(target = bus.p4.step, args = (ins,), daemon = True)
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()
        
    def continuos(self):
        ins = self.ins_entry.get()
        if ins != '':
            self.ins_entry.delete(0, 'end')
            ins = ins.split()
        else: 
            ins = 'none'
        self.thread1 = threading.Thread(target = bus.p1.step, args = (ins,), daemon = True)
        self.thread2 = threading.Thread(target = bus.p2.step, args = (ins,), daemon = True)
        self.thread3 = threading.Thread(target = bus.p3.step, args = (ins,), daemon = True)
        self.thread4 = threading.Thread(target = bus.p4.step, args = (ins,), daemon = True)
        while not self.stopped.isSet():
            if not self.thread3.is_alive():  
                self.thread3 = threading.Thread(target = bus.p3.step, args = (ins,), daemon = True)  
                self.thread3.start()
            if not self.thread4.is_alive():
                self.thread4 = threading.Thread(target = bus.p4.step, args = (ins,), daemon = True)
                self.thread4.start()
            if not self.thread2.is_alive():
                self.thread2 = threading.Thread(target = bus.p2.step, args = (ins,), daemon = True)
                self.thread2.start()
            if not self.thread1.is_alive():
                self.thread1 = threading.Thread(target = bus.p1.step, args = (ins,), daemon = True)
                self.thread1.start()
        self.stopped.clear()
        
    def run_contiuos(self):      
        thread = threading.Thread(target = self.continuos, args = (), daemon = True)
        thread.start()
        
    def pause(self):
        self.stopped.set()
    
    

root = tk.Tk()
app = Application(master=root)

app.mainloop()
