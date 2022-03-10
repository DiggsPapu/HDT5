
import simpy
import random
import math


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
        
        #Cicle while there is at least one instruction left
        while (ins>0):
            with DES.CPU.request() as run:
                yield run
                print("At %s: the %s has entered the CPU, status: READY " %(env.now, name))
                
                #To run the instructions
                counter = 0
                while (counter<DES.Processor):
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
        
        


class DES:
    RAM = simpy.Container(env, init = 100, capacity= 100)
    CPU = simpy.Resource(env, capacity = 1)
    IO = simpy.Resource(env, capacity =1)
    Processor = 3
    def __init__(self, env, val, amo, insProcessor) -> None:
        self.RAM = simpy.Container(env, init = val, capacity= val)
        self.CPU = simpy.Resource(env, capacity = amo)
        self.IO = simpy.Resource(env, capacity =1) 
        self.Processor = insProcessor
        print(self.Processor)
#This code was obtained from https://stackabuse.com/calculating-variance-and-standard-deviation-in-python/
def standarDeviation(data, mean,ddof=0):
        variance =sum((x - mean) ** 2 for x in data) / (len(data) - ddof)
        std_dev = math.sqrt(variance)
        return std_dev  
        

    
#This is the try where u can put the numbers that u want. To see it you have to comment the automatized one.
list = []
try:
    num = int(input("Write down the amount of process : "))
    val = int(input("Write down the amount of RAM : "))
    amo = int(input("Write down the amount of CPU : "))
    interval = int(input("Write down the interval of comming: "))
    process = int(input("Write the maximum amount of instructions in a processing : "))
        # Create a CPU and a RAM
    des = DES(env, val, amo, process)

    #Create the processes

    for i in range(num):
        #velocity of creation, exponencial rate.
        creationTime = random.expovariate(1/interval)
        print("Program %d will come at %s" %(i, creationTime))
        env.process(NewProcess(env, "Program %e"%i, creationTime, des))


    

    env.run()
    mean = 0
    devSt = 0
    try:
        #get mean and standard deviation
        mean = sum(list)/len(list)
        devSt = standarDeviation(list, mean)
    except:
        mean=0
        devSt=0





    print("The mean time for a process while using %d amount of RAM, %d amount of CPU and an interval of comming of %d is: %d units of time"% (val, amo,interval,mean))
    print("The standard deviation time for a process while using %d amount of RAM, %d amount of CPU and an interval of comming of %d is: %d units of time"% (val, amo,interval, devSt))


except:
    print("No ingreso un valor valido")


#From here on I automatized the process for interval, number of process, memory capacity, amount of CPU, number of interval, and amount of instructions done in 1 run
listNum = []
listVal = []
listAmo = []
listInterval = []
listMean = []
listDevest = []
listProcess=[]
for k in range(0,9):
    list = []
    try:
        
        num = 25*k
        listNum.append(num)
        val = 100
        listVal.append(val)
        amo = 2
        listAmo.append(amo)
        interval = 1
        listInterval.append(interval)
        process = 3
        listProcess.append(process)
            # Create a CPU and a RAM
        des = DES(env, val, amo, process)

        #Create the processes

        for i in range(num):
            creationTime = random.expovariate(1/interval)
            print("Program %d will come at %s" %(i, creationTime))
            env.process(NewProcess(env, "Program %e"%i, creationTime, des))


        

        env.run()
        mean = 0
        devSt = 0
        try:
            mean = sum(list)/len(list)
            listMean.append(mean)
            devSt=standarDeviation(list, mean)
            listDevest.append(devSt)
        except:
            mean=0
            listMean.append(mean)
            devSt=0
            listDevest.append(devSt)
        





        print("%d: The mean time for a process, while using %d amount of RAM, %d amount of CPU, an interval of comming of %d and execution of %d instructions each time is: %d units of time"% (num,val, amo,interval,process,mean))
        print("%d: The standar deviation time for a process, while using %d amount of RAM, %d amount of CPU, an interval of comming of %d and execution of %d instructions each time is: %d units of time"% (num,val, amo,interval, process, devSt))


    except:
        print("No ingreso un valor valido")

for k in range(0, len(listNum)):
    print("%d: The mean time for a process, while using %d amount of RAM, %d amount of CPU, an interval of comming of %d and execution of %d instructions each time is: %d units of time"% (listNum[k],listVal[k], listAmo[k],listInterval[k],listProcess[k],listMean[k]))
    print("%d: The standar deviation time for a process, while using %d amount of RAM, %d amount of CPU, an interval of comming of %d and execution of %d instructions each time is: %d units of time"% (listNum[k],listVal[k], listAmo[k],listInterval[k],listProcess[k],listDevest[k]))
