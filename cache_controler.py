
import processor as p
import l1_cache as c


class Request:
    def __init__(self):
        self.msg = ''
        self.dir = ''
        self.data = ''



class MS:
    
    def __init__(self):
        pass 
    
    @staticmethod
    def pr_rd(state, inst_dir):
        if state == "I":
            print('BusRd dir') #Respond is flush
            # return respond
        elif state == "S":
            print("Nothing")
            return "S"
        elif state == "E":
            print("Nothing")
            return "E"
        elif state == "M":
            print("Nothing")
            return "M"
        elif state == "O":
            print("Nothing")
            return "O"


class CControler(object):

    def __init__(self, clock, n_proc):
        self.clock = clock
        self.proc = p.Processor(self.clock, n_proc)
        self.c_mem = c.L1Cache(self.clock)

    

    def proc_req(self):
        import bus 
        while True:
            inst = self.proc.gen_instr()
            print(inst.num_proc+" : "+inst.op+" "+inst.data+" "+ inst.dir)
            if inst.op == 'write': #Processor request PrWr
                
                bus.Bus.bus_rdx([inst.dir, inst.data], self.proc.n_proc) # BusRdX
                self.c_mem.write(inst.dir, 'M', inst.data)
            elif inst.op == 'read': #Processor request PrRd
                s = self.get_state(inst.dir)
                ms_res = MS.pr_rd(s, inst.dir)
                if ms_res in ["S", "E", "M", "O"]:
                    print(self.c_mem.read(inst.dir, ms_res))
                else:
                    self.c_mem.write(ms_res[1], ms_res[0], ms_res[2])
                    self.c_mem.read(inst.dir, ms_res[1])

    
    def snoop_bus(self, request):
        if request.msg == 'BusRd':
            print('Send data (Owned)')
        elif request.msg == 'BusRdX':
            print('Invalidate cache block')
        elif request.msg == 'BusUpgr':
            print('Invalidate cache block')
        elif request.msg == 'flush':
            print('Catch data')
        elif request.msg == 'flushOpt':
            print('Catch data')

    def get_state(self, dir):
        for set_m in self.c_mem.mem:
            for block_m in set_m:
                if block_m[2] == dir:
                    return block_m[1] 
        return 'NA'


ctrler = CControler(1, 'P1')
ctrler.c_mem.write("0000","E","ABCD")
print(ctrler.proc_req())


