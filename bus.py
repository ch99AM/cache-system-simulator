
import main_memory

# Funtions for main memory===========================
main_mem = main_memory.Memory() #
clock = 3

def read_mem(dir):
    return main_mem.read(dir, clock)

def write_mem(block):
    main_mem.write(block[2], block[3], clock)

#====================================================
class Request:
    def __init__(self):
        self.msg = ''
        self.dir = ''
        self.data = ''   

#====================================================

import time
import numpy as np

class L1Cache(object):
    
    def __init__(self, clock):
        self.mem = [[[str(i+j*2), "I", "", "0000"] for i in range(2)] for j in range(2)]
        self.clock = clock

    def read(self, dir):
        if self.find_dir(dir):
            time.sleep(0.1*self.clock)
            set_m = int(dir[-1], 2)
            for block in self.mem[set_m]:
                if dir == block[2]:
                    return block
        else:
            return "CM"
    
    # write-through
    # remplazo aleatorio
    def write(self, dir, state, data):
        set_m = int(dir[-1], 2)
        if self.find_dir(dir):
            for i in range(len(self.mem[set_m])):
                if dir == self.mem[set_m][i][2]:
                    self.mem[set_m][i][3] = data
                    self.mem[set_m][i][1] = state
                    self.mem[set_m][i][2] = dir  
                    write_mem(self.mem[set_m][i])            
        else: 
            block = np.random.randint(2)
            self.mem[set_m][block][3] = data
            self.mem[set_m][block][1] = state
            self.mem[set_m][block][2] = dir
            write_mem(self.mem[set_m][block])     
        time.sleep(0.1*self.clock)

    def find_dir(self, dir):
        for block_m in self.mem[int(dir[-1], 2)]:
            if dir == block_m[2]:
                return True
        return False


"""
c = L1Cache(1)
c.write('0010', 'E', 'ABCD')
c.write('1101', 'E', 'FFFF')
print(c.read("0010"))
print(c.read("1101"))
print(c.read("0000"))
c.write('1101', 'E', 'FFEE')
print(c.read("1101"))
"""
# ------------------------------------

import threading 
lock = threading.Lock()

p1 = ""
p2 = ""
p3 = ""
p4 = ""


def bus_rd(block, num_proc):
    lock.acquire()
    request = Request()
    request.dir = block[0]
    request.msg = 'BusRd'
    temp_ctr = 0
    if num_proc != 'P1': # result is data
        r1 = p1.snoop_bus(request)
        if r1 != 'NA':
            result = [block[0], 'S', r1]
            temp_ctr += 1
    if num_proc != 'P2':
        r2 = p2.snoop_bus(request)
        if r2 != 'NA':
            result = [block[0], 'S', r2]
            temp_ctr += 1
    if num_proc != 'P3':
        r3 = p3.snoop_bus(request)
        if r3 != 'NA':
            result = [block[0], 'S', r3]
            temp_ctr += 1
    if num_proc != 'P4':
        r4 = p4.snoop_bus(request)
        if r4 != 'NA':
            result = [block[0], 'S', r4]
            temp_ctr += 1
    if temp_ctr == 0:
        r5 = read_mem(block[0])
        result = [block[0], 'E', r5]
    lock.release()
    return result
        

def bus_rdx(block, num_proc):
    lock.acquire()
    request = Request()
    request.dir = block[0]
    request.msg = 'BusRdX'
    if num_proc != 'P1': #result is confirmation
        result = p1.snoop_bus(request)
    if num_proc != 'P2':
        result = p2.snoop_bus(request)
    if num_proc != 'P3':
        result = p3.snoop_bus(request)
    if num_proc != 'P4':
        result = p4.snoop_bus(request)
    lock.release()
    return result

def bus_upgr(block, num_proc):
    lock.acquire()
    request = Request()
    request.dir = block[0]
    request.msg = 'BusUpgr'
    if num_proc != 'P1': #result is confirmation
        result = p1.snoop_bus(request)
    if num_proc != 'P2':
        result = p2.snoop_bus(request)
    if num_proc != 'P3':
        result = p3.snoop_bus(request)
    if num_proc != 'P4':
        result = p4.snoop_bus(request)
    lock.release()
    return result

#-------------------------------------

import processor as p


class CControler(object):

    def __init__(self, clock, n_proc):
        self.clock = clock
        self.proc = p.Processor(self.clock, n_proc)
        self.c_mem = L1Cache(self.clock)
        self.ins = [p.Inst(), p.Inst()]
        self.counter = 0

    def step(self, inst_send = 'NA'): 
        if inst_send != 'NA':
            inst = inst_send
        else:
            inst = self.proc.gen_instr()
        self.ins.append(inst)
        if inst.op == 'write': #Processor request PrWr
            s = self.get_state(inst.dir)
            if s == 'I' or s == 'NA':
                bus_rdx([inst.dir, inst.data], self.proc.n_proc) # BusRdX
            elif s == 'M':
                pass
            elif s == 'O':
                bus_upgr([inst.dir, inst.data], self.proc.n_proc) # BusUpgr
            elif s == 'E':
                pass
            elif s == 'S':
                bus_upgr([inst.dir, inst.data], self.proc.n_proc) # BusUpgr
            self.c_mem.write(inst.dir, 'M', inst.data)
        elif inst.op == 'read': #Processor request PrRd
            s = self.get_state(inst.dir)
            if s in ["S", "E", "M", "O"]:
                self.c_mem.read(inst.dir)
            elif s == 'I' or s == 'NA': #Bloque invalido o no tengo el dato
                block_temp = bus_rd([inst.dir, inst.data], self.proc.n_proc)
                self.c_mem.write(block_temp[0], block_temp[1], block_temp[2])
        self.counter += 1
                
    def num_cycles(self, cycles): 
        for i in range(cycles):
            inst = self.proc.gen_instr()
            self.ins.append(inst)
            if inst.op == 'write': #Processor request PrWr
                s = self.get_state(inst.dir)
                if s == 'I' or s == 'NA':
                    bus_rdx([inst.dir, inst.data], self.proc.n_proc) # BusRdX
                elif s == 'M':
                    pass
                elif s == 'O':
                    bus_upgr([inst.dir, inst.data], self.proc.n_proc) # BusUpgr
                elif s == 'E':
                    pass
                elif s == 'S':
                    bus_upgr([inst.dir, inst.data], self.proc.n_proc) # BusUpgr
                self.c_mem.write(inst.dir, 'M', inst.data)
            elif inst.op == 'read': #Processor request PrRd
                s = self.get_state(inst.dir)
                if s in ["S", "E", "M", "O"]:
                    self.c_mem.read(inst.dir)
                elif s == 'I' or s == 'NA': #Bloque invalido o no tengo el dato
                    block_temp = bus_rd([inst.dir, inst.data], self.proc.n_proc)
                    self.c_mem.write(block_temp[0], block_temp[1], block_temp[2])
            self.counter += 1
                                    
    
    def snoop_bus(self, request):
        if request.msg == 'BusRd':
            s = self.get_state(request.dir)
            if s == 'M':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'O'
                            return self.c_mem.mem[i][j][3]
            elif s == 'O':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'O'
                            return self.c_mem.mem[i][j][3]
            
            elif s == 'E':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'S'
                            return self.c_mem.mem[i][j][3]
            elif s == 'S':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'S'
                            return self.c_mem.mem[i][j][3]
            elif s == 'I':
                return 'NA'
            else:
                return 'NA'
                
        elif request.msg == 'BusRdX':
            s = self.get_state(request.dir)
            if s == 'M':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'I'
                            return self.c_mem.mem[i][j][3]
            elif s == 'O':
                return 'NA'           
            elif s == 'E':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'I'
                            return self.c_mem.mem[i][j][3]
            elif s == 'S':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'I'
                            return self.c_mem.mem[i][j][3]
            elif s == 'I':
                return 'NA'
            else:
                return 'NA'
        elif request.msg == 'BusUpgr':
            s = self.get_state(request.dir)
            if s == 'M':
                return 'NA'
            elif s == 'O':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'I'
                            return self.c_mem.mem[i][j][3]           
            elif s == 'E':
                return 'NA'
            elif s == 'S':
                for i in range(len(self.c_mem.mem)):
                    for j in range(len(self.c_mem.mem[i])):
                        if self.c_mem.mem[i][j][2] == request.dir:
                            self.c_mem.mem[i][j][1] = 'I'
                            return self.c_mem.mem[i][j][3]
            elif s == 'I':
                return 'NA'
            else:
                return 'NA'
    def get_state(self, dir):
        for set_m in self.c_mem.mem:
            for block_m in set_m:
                if block_m[2] == dir:
                    return block_m[1] 
        return 'NA'


p1 = CControler(clock, 'P1')
p2 = CControler(clock, 'P2')
p3 = CControler(clock, 'P3')
p4 = CControler(clock, 'P4')

"""
ctr = 1

thread1 = threading.Thread(target = p1.proc_req, args = (ctr, ), daemon = True)
thread2 = threading.Thread(target = p2.proc_req, args = (ctr, ), daemon = True)

thread1.start()
thread2.start()

while True:
    time.sleep(5)
    ctr = 0
    break
    
thread1.join()
thread2.join()
"""
    
