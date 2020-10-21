
import main_memory

class Bus():
    def __init__(self, clock):
        self.clock = clock
        self.main_mem = main_memory.Memory(self.clock) 
        

    def read_mem(self, dir):
        return self.main_mem.read(dir)
    
    def write_mem(self, block):
        self.main_mem.write(block[2], block[3])

    @staticmethod
    def write_miss(self, block, num_proc):
        # Invalidacion por escritura a otros procesadores
        self.write_mem(block)
        if num_proc != 'P1':
            pass
            # invalidar el bloque( funcion de snoop)
        if num_proc != 'P2':
            pass
            # invalidar el bloque
        if num_proc != 'P3':
            pass
            # invalidar el bloque
        if num_proc != 'P4':
            pass
            # invalidar el bloque   
    @staticmethod
    def cache_miss(self, dir, num_proc):         
