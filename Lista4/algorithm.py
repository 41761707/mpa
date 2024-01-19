
import random 
import numpy as np

def closest_points(points):
    sorted_points = sorted(points, key=lambda x: x[0])

    points, distance, _, compared_pairs = recursive(sorted_points)
    return points, distance, compared_pairs


def recursive(sorted_points):
    if len(sorted_points) <= 3:
        return bruteforce_distance(sorted_points)

    mid = len(sorted_points) // 2
    median_x = sorted_points[mid][0]
    left_x = sorted_points[:mid]
    right_x = sorted_points[mid:]

    left_closest_pair, left_distance, y_left, pairs_left = recursive(left_x)
    right_closest_pair, right_distance, y_right, pairs_right = recursive(right_x)
    compared_pairs = pairs_left + pairs_right

    best_points = None
    delta = float("inf")
    if left_distance < right_distance:
        best_points = left_closest_pair
        delta = left_distance
    else:
        best_points = right_closest_pair
        delta = right_distance

    y_sorted = []
    l = 0
    r = 0
    while l < len(y_left) and r < len(y_right):
        if y_left[l] <= y_right[r]:
            y_sorted.append(y_left[l])
            l += 1
        else:
            y_sorted.append(y_right[r])
            r += 1
    while l < len(y_left):
        y_sorted.append(y_left[l])
        l += 1
    while r < len(y_right):
        y_sorted.append(y_right[r])
        r += 1

    y_filtered = [(x, y) for x, y in y_sorted if abs(x - median_x) <= delta]
    min_dist = delta

    cnt = 0
    for i in range(len(y_filtered)):
        for j in range(i + 1, min(i + 8, len(y_filtered))):
            cnt += 1
            distance = calc_dist(y_filtered[i], y_filtered[j])
            if distance < min_dist:
                min_dist = distance
                best_points = (y_filtered[i], y_filtered[j])
    compared_pairs += [{len(sorted_points): cnt}]

    return best_points, min_dist, y_sorted, compared_pairs


def bruteforce_distance(list_of_points):
    min_dist = float("inf")
    points = None
    for i in range(len(list_of_points)):
        for j in range(i + 1, len(list_of_points)):
            dist = calc_dist(list_of_points[i], list_of_points[j])
            if dist < min_dist:
                min_dist = dist
                points = (list_of_points[i], list_of_points[j])
    return points, min_dist, sorted(list_of_points, key=lambda v: v[1]), [{len(list_of_points): 0}]


def calc_dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def generate_points(n, distribution):
    if distribution == "uniform":
        return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    elif distribution == "normal":
        return [(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)]
    elif distribution == "exp":
        return [(np.random.exponential(scale = 1/2), np.random.exponential(scale = 1/2)) for _ in range(n)]

    
def main():
    n = 100
    distribution = "uniform"
    list_of_points = generate_points(n, distribution)
    #list_of_points = [(25, 61), (74, 2), (75, 100), (43, 70), (5, 25), (91, 54), (38, 9), (21, 50), (31, 52), (96, 54), (93, 0), (45, 33), (30, 8), (69, 98), (67, 13), (70, 47), (59, 25), (47, 40), (78, 7), (85, 19)]
    points, dist, compared_pairs = closest_points(list_of_points)
    print(points)
    print(dist)


if __name__ == "__main__":
    main()