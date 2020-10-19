
import processor as p
import l1_cache as c


class Request:
    def __init__(self):
        self.msg = ''
        self.dir = ''
        self.data = ''

class CControler:

    def __init__(self, clock, n_proc):
        self.clock = clock
        self.proc = p.Processor(self.clock, n_proc)
        self.c_mem = c.L1Cache(self.clock)

    

    def proc_req(self):
        while True:
            inst = self.proc.gen_instr()
            print(inst.num_proc+" : "+inst.op+" "+inst.data+" "+ inst.dir)
            if inst.op == 'write': #Processor request PrWr
                print("Bus: BusRqX")
            elif inst.op == 'read': #Processor request PrRd
                print('Bus: BusRq')
    
    def snoop_bus(self, request):
        if request.msg == 'BusRq':
            print('Send data (Owned)')
        elif request.msg == 'BusRqX':
            print('I cache block')
        elif request.msg == 'BusUpgr':
            print('I cache block')
        elif request.msg == 'BusUpgr':
            print('I cache block')
        elif request.msg == 'flush':
            print('Catch data')
        elif request.msg == 'flushOpt':
            print('Catch data')

ctrler = CControler(1, 'P1')
ctrler.proc_req()