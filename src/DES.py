import simpy
import random


RANDOM_SEED = 3
INTERVAL_CUSTOMERS = 10.0
#We create the environment
env = simpy.Environment()
def NewProcess(env,name, time, DES):
        memory = random.randint(1,10)
        ins = random.randint(1,10)
        #time of creation in new
        yield env.timeout(time)
        print('At %s: the %s has been created, memory = %d and instructions = %d, status: NEW' % (env.now, name, memory, ins))
        #Tries to get the memory from the ram
        yield DES.RAM.get(memory)
        print("RAM's memory has changed to %d"%DES.RAM.level)
        #runIns(env, DES, ins, name)
        #Cicle while there is at least one instruction left
        while (ins>0):
            with DES.CPU.request() as running:
                yield running
                print("At %s: the %s has entered the CPU, status: READY " %(env.now, name))
                
                #
                counter = 0
                while (counter<2):
                    ins -= 1
                    if (ins<=0):
                        break
                    else:
                        pass
                    counter+=1
                
                print("At %s: %d instructions have been executed for the %s, there are %d instructions left" %((env.now, counter, name, ins)))
                yield env.timeout(1)
            cases(env, ins, name)
        DES.RAM.put(memory)
        
        print("At %s: the %s has done all the instructions status: TERMINATED" %(env.now, name))
        print("%d amount of memory has been returned to RAM, RAM's memory status : %d"%(memory, DES.RAM.level))


        
def getMemory(env, DES, memory, name):
    DES.RAM.get(memory)
    print("At %s: the %s entered the RAM" %(env.now, name))
        

def runIns(env, DES, ins, name):
    #Cicle while there is at least one instruction left
    while (ins>0):
        with DES.CPU.request() as running:
            yield running
            print("At %s: the %s has entered the CPU, status: READY " %(env.now, name))
            counter = 0
            while (counter<2):
                ins -= 1
                if (ins<=0):
                    break
                else:
                    pass
                counter+=1
                
            print("At %s: %d instructions have been executed for the %s, there are %d instructions left" %((env.now, counter, name, ins)))
            yield env.timeout(1)
        cases(env, ins, name)
    

def cases(env, ins, name):
    if (ins>0):
        case = bool(random.getrandbits(1))
        if (case):
            print("At %d: the %s has %s instructions left, status: READY" %(env.now,name, ins))
        else:
            print("At %d: the %s is ready to do I/O operations, status: WAITING" %(env.now,name))
            #The operations done in the I/O are done in a random amount of time between 1 and 10
            yield env.timeout(random.randint(1,3))
            print("At %d: the %s has done the I/O operations, it has %d instructions left, status: READY " %(env.now,name, ins))
            
            
        


class DES:
    RAM = simpy.Container(env, init = 100, capacity= 100)
    CPU = simpy.Resource(env, capacity = 1)
    def __init__(self, env) -> None:
        pass
    

    
        

    

try:
    num = int(input("Write down the amount of process : "))
    # val = int(input("Write down the amount of RAM : "))
    # amo = int(input("Write down the amount of CPU : "))

except:
    print("No ingreso un valor valido")

# Create a CPU and a RAM
des = DES(env)
des.__init__(env)

#Create the processes
for i in range(num):
    creationTime = random.expovariate(1/10)
    print("Program %d will come at %s" %(i, creationTime))
    env.process(NewProcess(env, "Program %e"%i, creationTime, DES))


env.run()