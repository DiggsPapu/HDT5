from multiprocessing.connection import wait
import simpy
import random
import math

list = []
RANDOM_SEED = 3
#We create the environment
env = simpy.Environment()
def NewProcess(env,name, time, DES):
        memory = random.randint(1,10)
        ins = random.randint(1,10)
        time = env.now
        #time of creation in new
        yield env.timeout(time)
        print('At %s: the %s has been created, memory = %d and instructions = %d, status: NEW' % (env.now, name, memory, ins))
        #Tries to get the memory from the ram
        yield DES.RAM.get(memory)
        print("RAM's memory has changed to %d"%DES.RAM.level)
        
#dkdkdk
        #Cicle while there is at least one instruction left
        while (ins>0):
            with DES.CPU.request() as run:
                yield run
                print("At %s: the %s has entered the CPU, status: READY " %(env.now, name))
                
                #To run the instructions
                counter = 0
                while (counter<2):
                    ins -= 1
                    if (ins<=0):
                        break
                    else:
                        pass
                    counter+=1
                #To print the instructions at what time, and how many left.
                print("At %s: %d instructions have been executed for the %s, there are %d instructions left" %((env.now, counter, name, ins)))
                yield env.timeout(1)
            #To do the cases if is READY or WAITING
            if (ins>0):
                case = bool(random.getrandbits(1))
                if (case):
                    print("At %d: the %s has %s instructions left, status: READY" %(env.now,name, ins))
                else:
                    with DES.IO.request() as waitin:
                        yield waitin
                        print("At %d: the %s is ready to do I/O operations, status: WAITING" %(env.now,name))
                        #The operations done in the I/O are done in a random amount of time between 1 and 10
                    
                        yield env.timeout(random.randint(1,10))
                        print("At %d: the %s has done the I/O operations, it has %d instructions left, status: READY " %(env.now,name, ins))
                
        #To do the reinsertion of the memory used
        DES.RAM.put(memory)
       #To print that the memory has been returned and the process is done 
        print("At %s: the %s has done all the instructions status: TERMINATED" %(env.now, name))
        print("%d amount of memory has been returned to RAM, RAM's memory status : %d"%(memory, DES.RAM.level))
        time= env.now-time
        list.append(time)

#The function cases
def cases(env, ins, name):
    if (ins>0):
        case = bool(random.getrandbits(1))
        if (case):
            print("At %d: the %s has %s instructions left, status: READY" %(env.now,name, ins))
        else:
            print("At %d: the %s is ready to do I/O operations, status: WAITING" %(env.now,name))
            #The operations done in the I/O are done in a random amount of time between 1 and 10
            yield env.timeout(random.randint(1,10))
            print("At %d: the %s has done the I/O operations, it has %d instructions left, status: READY " %(env.now,name, ins))
        print(case)    
            
        


class DES:
    RAM = simpy.Container(env, init = 100, capacity= 100)
    CPU = simpy.Resource(env, capacity = 1)
    IO = simpy.Resource(env, capacity =1)
    def __init__(self, env, val, amo) -> None:
        self.RAM = simpy.Container(env, init = val, capacity= val)
        self.CPU = simpy.Resource(env, capacity = amo)
        self.IO = simpy.Resource(env, capacity =1) 

def standarDeviation(data, mean,ddof=0):
        variance =sum((x - mean) ** 2 for x in data) / (len(data) - ddof)
        std_dev = math.sqrt(variance)
        return std_dev  
        

    

try:
    num = int(input("Write down the amount of process : "))
    val = int(input("Write down the amount of RAM : "))
    amo = int(input("Write down the amount of CPU : "))
    interval = int(input("Write down the interval of comming: "))
        # Create a CPU and a RAM
    des = DES(env, val, amo)
    des.__init__(env, val, amo)

    #Create the processes

    for i in range(num):
        creationTime = random.expovariate(1/interval)
        print("Program %d will come at %s" %(i, creationTime))
        env.process(NewProcess(env, "Program %e"%i, creationTime, DES))


    

    env.run()
    mean = 0
    devSt = 0
    try:
        mean = sum(list)/len(list)
        devSt=standarDeviation(list, mean)
    except:
        mean=0
        devSt=0





    print("The mean time for a process while using %d amount of RAM, %d amount of CPU and an interval of comming of %d is: %d units of time"% (val, amo,interval,mean))
    print("The standar deviation time for a process while using %d amount of RAM, %d amount of CPU and an interval of comming of %d is: %d units of time"% (val, amo,interval, devSt))


except:
    print("No ingreso un valor valido")

# listNumProcess=[]
# listMean=[]
# listDesv=[]
# k=25
# j = 0
# while(k*j<250):
#     list = []
#     num = k*j
#     val = 100
#     amo = 1
#     interval = 1
#             # Create a CPU and a RAM
#     des = DES(env, val, amo)
#     des.__init__(env, val, amo)

#         #Create the processes

#     for i in range(num):
#         creationTime = random.expovariate(1/interval)
#         print("Program %d will come at %s" %(i, creationTime))
#         env.process(NewProcess(env, "Program %e"%i, creationTime, DES))


        

#     env.run()
#     mean = 0
#     devSt = 0
#     try:
#         mean = sum(list)/len(list)
#         devSt=standarDeviation(list, mean)
#     except:
#         mean=0
#         devSt=0
#     listMean.append(mean)
#     listDesv.append(devSt)
# for k in range(0, len(listNumProcess)):
#     print(listNumProcess)
#     print("The mean time for a process while using %d amount of RAM, %d amount of CPU and an interval of comming of %d is: %d units of time"% (100, 1,1,listMean[k]))
#     print("The standar deviation time for a process while using %d amount of RAM, %d amount of CPU and an interval of comming of %d is: %d units of time"% (100, 1,1,listMean[k]))
#     print("_____________________________________________________________________________________________________________________________________________")
