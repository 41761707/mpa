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
    S = p_k
    k = 1
    while k < min_val:
        p_k = p_k * x * (float(k) / float(k + 1))
        S = S + p_k
        k = k + 1

    while U > S:
        p_k = p_k * x * (float(k) / float(k+1))
        S = S + p_k
        k = k + 1

    return k

def Poisson(x, min_val):
    U = random.random()
    p_k = math.exp(-x)
    S = 0 
    k = 0

    while k < min_val:
        S = S + p_k
        p_k = (p_k / float(k+1)) * x 
        k = k + 1 
    
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
    return bernoulli.rvs(x) == 1

class Counter:
    def __init__(self, passengers, wheels, wagons, wheels_size, planks):
        self.Passengers = passengers
        self.Wheels = wheels
        self.Wagons = wagons
        self.WheelsSize = wheels_size
        self.Planks = planks

class Plank:
    def __init__(self, wheel):
        self.Wheel = wheel
    def __str__(self):
        return "Koła: {}".format(self.Wheel)

class Wagon:
    def __init__(self, planks):
        self.Planks = planks
    def __str__(self):
        query = ""
        for plank in self.Planks:
            query = query + "Plank: {};".format(plank)
        return query

class Passenger:
    def __init__(self, head, body):
        self.Head = head
        self.Body = body
    def __str__(self):
        return "Head: {}; Body: {}".format(self.Head, self.Body)

class WagonWithPassengers:
    def __init__(self, wagon, passengers):
        self.Wagon = wagon
        self.Passengers = passengers
    def __str__(self):
        query = ""
        query = query + "Wagon: {};".format(self.Wagon)
        for passenger in self.Passengers:
            return "Pasażerowie: {};".format(passenger)
        return query

class Train:
    def __init__(self, locomotive, wagons):
        self.Locomotive = locomotive
        self.Wagons = wagons
    def __str__(self):
        query = ""
        query = query + "Lokomotywa: {};".format(self.Locomotive)
        for wagon in self.Wagons:
            query = query + "Wagon: {};".format(wagon)
        return query

def PlankSampler(x):
    global MinWheelSize
    if next_bernoulli(WheelGeneratingFunction(x) / (OneGeneratingFunction(x) + WheelGeneratingFunction(x))):
        return Plank(Logarithmic(WheelGeneratingFunction(x), MinWheelSize))
    return Plank(0)

def WagonSampler(x):
    global MinWagonLength
    global MinWagonWheels
    while True:
        length = Geometric(PlankGeneratingFunction(x), MinWagonLength)
        planks = [PlankSampler(x) for _ in range(length)]
        if isEnoughWheels(planks, MinWagonWheels):
            return Wagon(planks)

def isEnoughWheels(planks, minWheels):
    count = sum(1 for p in planks if p.Wheel != 0)
    return count >= minWheels

def PassengerSampler(x):
    global MinHeadSize 
    global MinBodySize
    return Passenger(Logarithmic(HeadGeneratingFunction(x), MinHeadSize),
                     Logarithmic(BodyGeneratingFunction(x), MinBodySize))

def WagonWithPassengersSampler(x):
    global MinPassengerCount
    wagon = WagonSampler(x)
    length = Poisson(PassengerGeneratingFunction(x), MinPassengerCount)
    passengers = [PassengerSampler(x) for _ in range(length)]
    return WagonWithPassengers(wagon, passengers)

def TrainSampler(x):
    global MinTrainLength
    length = Geometric(WagonWithPassengersGeneratingFunction(x), MinTrainLength)
    locomotive = WagonSampler(x)
    wagons = [WagonWithPassengersSampler(x) for _ in range(length)]
    return Train(locomotive, wagons)

'''def printWagon(wagon):
    print(" Planks and wheels = ", end="")
    for p in wagon.Planks:
        print(p.Wheel, end=" ")
    print()

def printPassenger(passenger):
    print("{", passenger.Body, passenger.Head, "}", end="")

def printTrain(train):
    print("Lokomotywa: ", end="")
    printWagon(train.Locomotive)
    print()

    for w in train.Wagons:
        print("Passengers = {", end="")
        for p in w.Passengers:
            printPassenger(p)
        print("};;", end="")

        printWagon(w.Wagon)
        print()
'''

class BigResult:
    def __init__(self):
        self.Results = []

class Result:
    def __init__(self, x):
        self.Trains = []
        self.X = x

def main():
    #numOfTrials = 100
    numOfTrials = 1
    #minX = 0.001
    minX = 0.1
    maxX = 0.4851
    #deltaX = 0.0001
    deltaX = 0.1

    bR = BigResult()
    x = minX
    while x < maxX:
        print(x)

        r = Result(x)

        for i in range(numOfTrials):
            r.Trains.append(TrainSampler(x))
        bR.Results.append(r)
        x = x + deltaX
    for train in r.Trains:
        print(train)

    #try:
    #    with open("data/res.json", "w") as f:
    #        json.dump(bR, f, default=lambda o: o.__dict__, indent=4)
    #except Exception as e:
    #    print(e)

if __name__ == "__main__":
    main()