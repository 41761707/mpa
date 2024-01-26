import random
import math

#Distributions

def Logarithmic(x, min_val):
    U = random.random()
    p_k = -1 / (math.log(1-x))
    S = 0
    k = 1
    counter = 0
    print(U)
    while U > S:
        print(S)
        p_k = p_k * x * (float(k) / float(k+1))
        S = S + p_k
        k = k + 1
        counter = counter + 1
        if counter == 19:
            break

    return k

def Poisson(x, min_val):
    U = random.random()
    p_k = math.exp(-x)
    S = 0 
    k = 0

    print(U)
    while U > S:
        S = S + p_k
        p_k = (p_k / float(k+1)) * x 
        print(S)
        k = k + 1 

    return k

def Geometric(x, min_val):
    U = random.random()
    p_k = 1 - x
    S = 0 
    k = 0

    while U > S:
        S = S + p_k 
        p_k = p_k * x 
        k = k + 1
    return k

def main():
    print(Poisson(0.4,0))
if __name__ == '__main__':
    main()