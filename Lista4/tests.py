import numpy as np
import random
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
from math import sqrt, log
import os
from statistics import variance


#nMin = 100
#nMax = 3000
nMin = 3000
nMax = 3000
step = 100
rep = 100
distribution = "exp"
result_path = "graphs/exp"


def main():
    counter_dict = {}
    counter_sums = {}
    comp_count_list = []
    n_range = range(nMin, nMax + 1, step)
    for n in n_range:
        counter_list = []
        counter_sum = 0
        print(f"n = {n}:")
        for _ in tqdm(range(rep)):
            list_of_points = generate_points(n, distribution)

            points, dist, compared_pairs = closest_points(list_of_points)
            counter_list.extend(compared_pairs)

        for d in counter_list:
            for key, value in d.items():
                counter_sum += value
                comp_count_list.append((key, value))
                if key in counter_dict:
                    counter_dict[key]["sum"] += value
                    counter_dict[key]["count"] += 1
                else:
                    counter_dict[key] = {"sum": value, "count": 1}
        counter_sums[n] = counter_sum / rep
    mean_dict = {key: value["sum"] / value["count"] for key, value in counter_dict.items()}
    sorted_mean_dict = {k: mean_dict[k] for k in sorted(mean_dict)}
    if len(n_range) > 1:
        analyze_results(sorted_mean_dict, counter_sums, nMax)
    else:
        analyze_result(comp_count_list, sorted_mean_dict, nMin)


def analyze_result(comp_count_list, sorted_mean_dict, n):
    xs, ys = zip(*comp_count_list)
    plt.scatter(xs, ys)
    plt.scatter(sorted_mean_dict.keys(), sorted_mean_dict.values(), label="mean")
    #plt.axvline(x=sqrt(n), label=f"sqrt({n})")
    plt.xlabel("n")
    plt.xscale("log")
    plt.ylabel("Porównane pary")
    plt.title(f"Porównane pary dla n={n}")
    plt.legend()
    os.makedirs(f"{result_path}", exist_ok=True)
    plt.savefig(f"{result_path}/compared_pairs_scatter_log_{nMin}.png")
    plt.clf()
    
    xs, ys = zip(*comp_count_list)
    plt.scatter(xs, ys, color="gray")
    plt.scatter(sorted_mean_dict.keys(), sorted_mean_dict.values(), label="mean")
    #plt.axvline(x=sqrt(n), label=f"sqrt({n})")
    plt.xlabel("n")
    plt.ylabel("Porównane pary")
    plt.title(f"Porównane pary dla n={n}")
    plt.legend()
    os.makedirs(f"{result_path}", exist_ok=True)
    plt.savefig(f"{result_path}/compared_pairs_scatter_{nMin}.png")
    plt.clf()


def analyze_results(sorted_mean_dict, counter_sums, n):
    # Mean of comparisons
    plt.plot(sorted_mean_dict.keys(), sorted_mean_dict.values(), label="Średnia porównanych par", linewidth=1.5)
    #plt.axvline(x=1/n, label=f"1/n", color = "red")
    plt.xlabel("n")
    plt.ylabel("Średnia porównanych par")
    plt.title(f"Średnia porównanych par w podproblemach")
    plt.legend()
    os.makedirs(f"{result_path}", exist_ok=True)
    plt.savefig(f"{result_path}/compared_pairs_subproblem.png")
    plt.clf()
    plt.plot(sorted_mean_dict.keys(), sorted_mean_dict.values(), label="Średnia porównanych par", linewidth=1.5)
    #plt.axvline(x=sqrt(n), label=f"sqrt({n})")
    plt.xlabel("n")
    plt.xscale("log")
    plt.ylabel("Średnia porównanych par")
    plt.title(f"Średnia porównanych par w podproblemach")
    plt.legend()
    os.makedirs(f"{result_path}", exist_ok=True)
    plt.savefig(f"{result_path}/compared_pairs_subproblem_log.png")
    plt.clf()
    plt.plot(
        counter_sums.keys(),
        counter_sums.values(),
        label="sum",
        linewidth=1.5,
        color="gray",
    )
    plt.xlabel("n")
    plt.ylabel("Suma par")
    plt.title(f"Suma par porównanych przez algorytm")
    plt.legend()
    os.makedirs(f"{result_path}", exist_ok=True)
    plt.savefig(f"{result_path}/compared_pairs_instance.png")
    plt.clf()
    
    values_div_n = [counter_sums[n] / n for n in counter_sums.keys()]
    values_div_nlogn = [counter_sums[n] / (n*log(n)) for n in counter_sums.keys()]
    values_div_nlogn2 = [counter_sums[n] / (n*log(n)**2) for n in counter_sums.keys()]
    plt.plot(counter_sums.keys(), values_div_n, label="średnia / n", linewidth=1.5, color="darkorange")
    plt.plot(counter_sums.keys(), values_div_nlogn, label="średnia / nlog(n)", linewidth=1.5, color="darkred")
    plt.plot(counter_sums.keys(), values_div_nlogn2, label="średnia / nlog(n)^2", linewidth=1.5, color="purple")
    plt.xlabel("n")
    plt.ylabel("Stała")
    plt.title(f"Suma par punktów porównana przez podproblemy")
    plt.legend()
    os.makedirs(f"{result_path}", exist_ok=True)
    plt.savefig(f"{result_path}/compared_pairs_constant.png")
    plt.clf()
    
    


def closest_points(list_of_points):
    x_sorted = sorted(list_of_points, key=lambda v: v[0])

    points, dist, _, compared_pairs = closest_points_rec(x_sorted)
    return points, dist, compared_pairs


def closest_points_rec(x_sorted):
    if len(x_sorted) <= 3:
        return bruteforce(x_sorted)

    mid = len(x_sorted) // 2
    median_point = x_sorted[mid][0]
    left_half = x_sorted[:mid]
    right_half = x_sorted[mid:]

    points_l, distance_l, y_left, pairs_left = closest_points_rec(left_half)
    right_closest_pair, right_distance, y_right, pairs_right = closest_points_rec(right_half)
    compared_pairs = pairs_left + pairs_right

    best_points = None
    delta = float("inf")
    if distance_l < right_distance:
        best_points, delta = points_l, distance_l
    else:
        best_points, delta = right_closest_pair, right_distance

    y_sorted = []
    l, r = 0, 0
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

    y_filtered = [(x, y) for x, y in y_sorted if abs(x - median_point) <= delta]
    min_dist = delta

    cnt = 0
    for i in range(len(y_filtered)):
        for j in range(i + 1, min(i + 8, len(y_filtered))):
            cnt += 1
            dist = calc_dist(y_filtered[i], y_filtered[j])
            if dist < min_dist:
                min_dist = dist
                best_points = (y_filtered[i], y_filtered[j])
    compared_pairs += [{len(x_sorted): cnt}]

    return best_points, min_dist, y_sorted, compared_pairs


def bruteforce(list_of_points):
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
        return [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(n)]
    elif distribution == "normal":
        return [(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)]
    elif distribution == "exp":
        return [(np.random.exponential(scale = 1/2), np.random.exponential(scale = 1/2)) for _ in range(n)]


if __name__ == "__main__":
    main()
