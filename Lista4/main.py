import sys
import random 
import math
import time
import matplotlib.pyplot as plt
import numpy as np 

f_distance_global = 0
boundary_counter = 0
brute_force_counter = 0
def generate_random_uniform_input(n):
    #return [(random.gauss(50, 50), random.gauss(50, 50)) for _ in range(n)]
    #return [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
    #return [(random.randint(0,101), random.randint(0,101)) for _ in range(n)]
    return [(np.random.exponential(scale = 1/2), np.random.exponential(scale = 1/2)) for _ in range(n)]

def f_distance(p1, p2):
    global  f_distance_global 
    f_distance_global= f_distance_global + 1

    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) 

def show_on_grid(points):
    x, y = zip(*points)

    plt.scatter(x, y, color='blue', marker='o')
    plt.title('Położenie {} punktów w dwuwymiarze'.format(len(points)))
    plt.xlabel('Współrzędna x')
    plt.ylabel('Współrzędna y')
    plt.grid(True)
    plt.savefig('wynik.png')

def show_on_grid_w_closest(points, closest_pair):
    x, y = zip(*points)

    plt.scatter(x, y, color='blue', marker='o')
    plt.title('Położenie {} punktów w dwuwymiarze'.format(len(points)))
    plt.xlabel('Współrzędna x')
    plt.ylabel('Współrzędna y')
    plt.grid(True)
    plt.plot([closest_pair[0][0], closest_pair[1][0]], [closest_pair[0][1], closest_pair[1][1]], color='red')
    plt.savefig('wynik.png')

def brute_force_closest_pair(points):
    min_distance = float('inf')
    closest_pair = None
    global brute_force_counter 
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            brute_force_counter = brute_force_counter + 1
            distance = f_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])

    return closest_pair, min_distance

def boundary_points(points, sorted_points, delta, best_pair):
    #print("BOUNDARY: ", delta)
    global boundary_counter 
    n = len(sorted_points)
    mid_y = sorted_points[n//2][1]
    to_consider = [point for point in points if mid_y - delta <= point[1] <= mid_y + delta]
    #print("TO CONSIDER: ", to_consider)
    best = delta
    sub_n = len(to_consider)

    for i in range(sub_n - 1):
        for j in range(i+1, min(i+8, sub_n)):
            if to_consider[i][1] + best <= to_consider[j][1]:
                break
            boundary_counter = boundary_counter + 1
            distance = f_distance(to_consider[i],to_consider[j])
            if distance < best:
                best = distance
                best_pair = (to_consider[i],to_consider[j])
                #print("NEW MIN: ", distance)
                #print("NEW MIN PAIR: ", best_pair)
    return best_pair, best


def recursive(points, sorted_points):
    #print("SORTED_POINTS: ", sorted_points)
    n = len(sorted_points)
    if n <= 3:
        return brute_force_closest_pair(sorted_points)
    mid = n // 2
    left_half = sorted_points[:mid]
    #print("LEFT_HALF: ", left_half)
    right_half = sorted_points[mid:]
    #print("RIGHT_HALF: ", right_half)
    left_closest_pair, left_distance = recursive(points, left_half)
    right_closest_pair, right_distance= recursive(points, right_half)

    delta = 0
    current_best = 0
    if left_distance < right_distance:
        delta = left_distance
        current_best = left_closest_pair
    else:
        delta = right_distance
        current_best = right_closest_pair

    #print("DELTA: ", delta)
    #print("CURRENT BEST: ",current_best)
    closest_pair, min_distance = boundary_points(left_half + right_half,sorted_points, delta, current_best)
    return closest_pair, min_distance

def solution(points):
    sorted_points = sorted(points, key = lambda x : x[1])
    return recursive(sorted_points, sorted_points)

def verify(points):
    closest_points = None
    min_distance = float('inf')
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            distance = f_distance(points[i], points[j])

            if distance < min_distance:
                min_distance = distance
                closest_points = (points[i], points[j])
    return closest_points, min_distance


def test_loop(iters, upper_bound):
    for n in range(100, upper_bound, 100):
        for i in range(iters):
            print(n, ':', end ="")
            global f_distance_global 
            global boundary_counter 
            global brute_force_counter
            f_distance_global = 0
            f_distance_global = 0
            boundary_counter = 0
            brute_force_counter = 0
            points = generate_random_uniform_input(n)
            #show_on_grid(points)
            #points = [(25, 61), (74, 2), (75, 100), (43, 70), (5, 25), (91, 54), (38, 9), (21, 50), (31, 52), (96, 54), (93, 0), (45, 33), (30, 8), (69, 98), (67, 13), (70, 47), (59, 25), (47, 40), (78, 7), (85, 19)]
            #print(points)
            #print(solution(points))
            start_time = time.time()
            closest_pair_alg, distance_alg = solution(points)
            end_time = time.time() 
            execution_time = end_time - start_time
            print(distance_alg, ';', end ="")
            print(execution_time, ";",end="")
            print(f_distance_global, ';', end = "")
            print(boundary_counter , ';', end = "")
            print(brute_force_counter, ';', end = "")
            f_distance_global = 0
            #print("Liczba wywołań funkcji dystansu: ", f_distance_global)
            start_time = time.time()
            closest_pair_force, distance_force = verify(points)
            #closest_pair_force = None
            #distance_force = -1
            print(f_distance_global, ';', end = "")
            print()
            #print("Algorytm z zajec: {} -> {}".format(closest_pair_alg, distance_alg))
            #print("Algorytm brute-force: {} -> {}".format(closest_pair_force, distance_force))
            '''if distance_alg == distance_force:
                print("Algorytmy zwróciły taką samą odległość")
            else:
                print("Algorytmy zwróciły inne odległości")'''
            if distance_alg != distance_force:
                show_on_grid_w_closest(points, closest_pair_alg)
                print("Algorytm z zajec: {} -> {}".format(closest_pair_alg, distance_alg))
                print("Algorytm brute-force: {} -> {}".format(closest_pair_force, distance_force))
                return 0, points
    return 1, None

def main():
    iters = int(sys.argv[1])
    upper_bound = int(sys.argv[2])
    result, points = test_loop(iters, upper_bound)
    if result == 0:
        print(points)

    
if __name__ == '__main__':
    main()