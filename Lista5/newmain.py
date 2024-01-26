import sys 
import math
import random
from scipy.stats import bernoulli
#Generating Functions

import math

MinWheelSize = 3
MinWagonWheels = 2
MinLocomotiveWheels = 4
MinBodySize = 2
MinHeadSize = 1
MinTrainLength = 2
MinWagonLength = 2
MinPassengerCount = 0

def CycleGeneratingFunction(x):
    return math.log(1.0 / (1.0 - ZGeneratingFunction(x)))

def SeqGeneratingFunction(x):
    return 1.0 / (1.0 - x)

def SetGeneratingFunction(x):
    return math.exp(x)

def WheelGeneratingFunction(x):
    return CycleGeneratingFunction(ZGeneratingFunction(x))

def PlankGeneratingFunction(x):
    return ZGeneratingFunction(x) * ZGeneratingFunction(x) * (CycleGeneratingFunction(x) + OneGeneratingFunction(x))

def OneGeneratingFunction(x):
    return 1.0

def ZGeneratingFunction(x):
    return x

def WagonGeneratingFunction(x):
    return SeqGeneratingFunction(PlankGeneratingFunction(x)) - 1

def PassengerGeneratingFunction(x):
    return HeadGeneratingFunction(x) * BodyGeneratingFunction(x)

def HeadGeneratingFunction(x):
    return CycleGeneratingFunction(ZGeneratingFunction(x))

def BodyGeneratingFunction(x):
    return CycleGeneratingFunction(ZGeneratingFunction(x))

def TrainGeneratingFunction(x):
    return WagonGeneratingFunction(x) * SeqGeneratingFunction(WagonWithPassengersGeneratingFunction(x))

def WagonWithPassengersGeneratingFunction(x):
    return WagonGeneratingFunction(x) * SetGeneratingFunction(PassengerGeneratingFunction(x))


#Distributions

def Logarithmic(x, min_val):
    U = random.random()
    p_k = -1 / (math.log(1-x))
    S = 0
    k = 1
    counter = 0
    while U > S:
        p_k = p_k * x * (float(k) / float(k+1))
        S = S + p_k
        k = k + 1
        counter = counter + 1
        if counter == 5:
            break

    return k

def Poisson(x, min_val):
    U = random.random()
    p_k = math.exp(-x)
    S = 0 
    k = 0
    
    while U > S:
        S = S + p_k
        p_k = (p_k / float(k+1)) * x 
        k = k + 1 

    return k

def Geometric(x, min_val):
    U = random.random()
    p_k = 1 - x
    S = 0 
    k = 0

    while k < min_val:
        S = S + p_k 
        p_k = p_k * x 
        k = k + 1

    while U > S:
        S = S + p_k 
        p_k = p_k * x 
        k = k + 1
    return k

def next_bernoulli(x):
    #return bernoulli.rvs(x) == 1
    if random.random() < x:
        return 1
    return 0

#Tr = Wa * SEQ(Wa*SET(Pa))
def TrainSampler(x):
    global MinTrainLength
    locomotive = WagonSampler(x) #Wygeneruj lokomotywe, Wa
    #print("Liczba kół lokomotywy dla każdej deski(osi): ", locomotive)
    length = Geometric(WagonWithPassengersGeneratingFunction(x), 2) #SEQ
    wagons = [WagonWithPassengersSampler(x) for _ in range(length)] #Wa*SET(Pa)
    return [locomotive, wagons] #Z tego sklada sie pociag

#Pa = CYC(Z) * CYC(Z)
def WagonWithPassengersSampler(x):
    global MinPassengerCount
    wagon = WagonSampler(x)
    #print("Liczba kół każdego wagonu dla każdej deski (osi): ", wagon)
    length = Poisson(PassengerGeneratingFunction(x), MinPassengerCount)
    passengers = [PassengerSampler(x) for _ in range(length)]
    #print("Liczba passażerów: {}".format(length))
    #print("Struktura pasażerów: (head, body)", passengers)
    return [wagon, passengers]

def PassengerSampler(x):
    global MinHeadSize 
    global MinBodySize
    head = Logarithmic(HeadGeneratingFunction(x), MinHeadSize)
    body = Logarithmic(BodyGeneratingFunction(x), MinBodySize)
    return [head, body]
    

def EnoughWheels(planks, min_wheels):
    count = 0
    for plank in planks:
        if plank != 0:
            count = count +  1
    return count >= min_wheels

#Wa = SEQ_{>=1}(PL)
def WagonSampler(x): 
    global MinWagonLength
    global MinWagonWheels
    while True:
        length = Geometric(PlankGeneratingFunction(x), MinWagonLength) #SEQ
        planks = [PlankSampler(x) for _ in range(length)] #PL
        if EnoughWheels(planks, len(planks)):
            return planks #tutaj jest liczba desek oraz podpietych do nich kół
        
#Pl = Z * Z * (1+CYC(Z))
def PlankSampler(x):
    global MinWheelSize
    if next_bernoulli(WheelGeneratingFunction(x) / (OneGeneratingFunction(x) + WheelGeneratingFunction(x))): #???
        return Logarithmic(WheelGeneratingFunction(x), MinWheelSize) 
    return 0



def main():
    #print(TrainSampler(0.2))
    minX = 0.01
    maxX = 0.49
    deltaX = 0.01
    reps = 50
    x = minX 
    while x < maxX:
        for _ in range(reps):
            print("{}:".format(round(x, 2)), end="")
            result = TrainSampler(x)
            #Uklad pociagu 
            #print(result)

            #Liczba planków
            #planks = len(result[0])
            #for value in result[1]:
            #    planks = planks + len(value[0])
            #print(planks)

            #Liczba wagonow pasazerskich
            #print("{}".format(len(result[1])))

            #Liczba kol lokomotywy
            #print("{}".format(sum(result[0])))

            #Liczba kol wagonow
            #wheelsWagons = 0
            #for value in result[1]:
            #    wheelsWagons = wheelsWagons + sum(value[0])
            #print(wheelsWagons)

            #Liczba pasażerów
            #passengers_no = 0
            #for value in result[1]:
            #    for passenger in value[1]:
            #        passengers_no = passengers_no + 1
            #print(passengers_no)

            #Liczba "kółek" pasażerów
            #passengers_wheels = 0
            #for value in result[1]:
            #    for passenger in value[1]:
                    #print(passenger)
            #        passengers_wheels = passengers_wheels + sum(passenger)
            #print(passengers_wheels)
            #Liczba głów pasażerów
            #passengers_heads = 0
            #for value in result[1]:
            #    for passenger in value[1]:
            #        print(passenger)
            #        passengers_heads = passengers_heads + passenger[0]
            #print(passengers_heads)
            #Liczba ciał pasażerów
            passengers_bodies = 0
            for value in result[1]:
                for passenger in value[1]:
            #        print(passenger)
                    passengers_bodies = passengers_bodies + passenger[1]
            print(passengers_bodies)
        x = x + deltaX
if __name__ == "__main__":
    main()

'''
[
    [2, 2], 
    [
        [
            [2, 10], [
                [3, 6], [10, 10]
                ]
        ], 
        [
            [2, 10], [
                [10, 3]
                ]
        ], 
        [
            [10, 10], [
                [10, 2]
                ]
        ], 
        [
            [10, 2, 6], [
                [10, 6], [6, 2]
                ]
        ]
    ]
]
'''

