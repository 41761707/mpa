import sys
import random 
import math
import matplotlib.pyplot as plt

def generate_random_uniform_input(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

def f_distance(p1, p2):
    #print(p1,p2)
    #print(math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) )
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

    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            distance = f_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])

    return closest_pair, min_distance

def boundary_points(sorted_points, delta, best_pair):
    #print("BOUNDARY: ", delta)
    n = len(sorted_points)
    mid_y = sorted_points[n//2][1]
    to_consider = [point for point in sorted_points if mid_y - delta <= point[1] <= mid_y + delta]
    #print("TO CONSIDER: ", to_consider)

    best = delta
    sub_n = len(to_consider)

    for i in range(sub_n - 1):
        for j in range(i+1, min(i+7, sub_n)):
            distance = f_distance(sorted_points[i],sorted_points[j])
            if distance < best:
                best = distance
                best_pair = (sorted_points[i],sorted_points[j])
    return best_pair, best


def recursive(sorted_points):
    #print("SORTED_POINTS: ", sorted_points)
    n = len(sorted_points)
    if n <= 3:
        return brute_force_closest_pair(sorted_points)
    mid = n // 2
    left_half = sorted_points[:mid]
    #print("LEFT_HALF: ", left_half)
    right_half = sorted_points[mid:]
    #print("RIGHT_HALF: ", right_half)
    left_closest_pair, left_distance = recursive(left_half)
    right_closest_pair, right_distance = recursive(right_half)

    delta = 0
    current_best = 0
    if left_distance < right_distance:
        delta = left_distance
        current_best = left_closest_pair
    else:
        delta = right_distance
        current_best = right_closest_pair
    #print(delta)
    #print(current_best)
    closest_pair, min_distance = boundary_points(sorted_points, delta, current_best)
    return closest_pair, min_distance

def solution(points):
    sorted_points = sorted(points, key = lambda x : x[1])
    return recursive(sorted_points)

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


def test_loop(iters):
    for i in range(iters):
        #print(generate_random_uniform_input(3))
        points = generate_random_uniform_input(20)
        #show_on_grid(points)
        #points = [(1,1), (5,1), (9,1), (13,1), (1,3), (5,3), (9,3), (13,3), (7,2)]
        #print(points)
        #print(solution(points))
        closest_pair_alg, distance_alg = solution(points)
        closest_pair_force, distance_force = verify(points)
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
    result, points = test_loop(1000)
    if result == 0:
        print(points)

    
if __name__ == '__main__':
    main()