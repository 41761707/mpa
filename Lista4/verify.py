import math

SORTED_POINTS = [(27.246756419445962, 2.698188077271335), (26.68183607608955, 12.290105754977954), (38.10462864203979, 14.76675667209304), (16.82684682884277, 20.478882857623294), (98.14414007964722, 20.753060292285376), (36.41041398834096, 25.909459937854496), (0.21047832424051505, 28.49649302943954), (89.49223127669829, 31.307668621160634), (73.90409087408855, 35.95122189446206), (56.686951704876975, 38.12801024021801), (12.245082964483178, 45.033979134057404), (58.912445930010506, 45.64193660301046), (73.36094177922095, 49.06850563067289), (44.46458280117258, 52.20667771512546), (0.8960768161001664, 59.635075260001635), (12.880226195257228, 69.4881665687844), (7.346395135284101, 80.26734637575993), (19.82181492307794, 85.85132139258049), (81.84519713205559, 88.7263465820703), (39.349478304699545, 90.38808086664157)]

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def find_closest_points(points):
    closest_points = []
    min_distance = float('inf')

    for i in range(len(points) - 1):
        distance = euclidean_distance(points[i], points[i + 1])

        if distance < min_distance:
            min_distance = distance
            closest_points = [points[i], points[i + 1]]
        elif distance == min_distance:
            closest_points.extend([points[i], points[i + 1]])

    return closest_points

result = find_closest_points(SORTED_POINTS)
print("Najbliższe punkty w przestrzeni euklidesowej:")
for point in result:
    print(point)
