import numpy as np
import threading
import time

"""
    Definition of instruction 'struct'
"""
class Inst():
    def __init__(self):
        self.num_proc = ""
        self.op = ""
        self.dir = ""
        self.data = ""

class Processor():

    def __init__(self, clock, n_proc):
        self.clock = clock
        self.n_proc = n_proc
        

    def gen_instr(self):
        """
            Instructions Generator
            Constant cycle that generates instruction
            every clock cycle.
        """
        self.inst = Inst()
        ins = ('read', 'calc', 'write')
        p =[0.16, 0.68, 0.16]
        time.sleep(self.clock)
        self.inst.op = np.random.choice(ins, 1, replace=False, 
            p=p)[0] #normal distributions
        self.inst.num_proc = self.n_proc    
        if self.inst.op == 'read':
            self.__gen_dir()
        elif self.inst.op == 'write':
            self.__gen_dir()
            self.inst.data =  hex(np.random.randint(65536)).lstrip("0x")
        return self.inst

    def __gen_dir(self):
        """
        Dir memory selection with index generated by 
        poisson distribution
        """

        dir = ["{0000:b}".format(i) for i in range(16)]
        self.inst.dir = "0000"#dir[np.random.poisson(5)%16]

"""
c = Processor(1,"P1")
a = c.gen_instr()
print(a.num_proc+" : "+a.op+" "+a.data+" "+ a.dir)
"""