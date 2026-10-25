
import math
import heapq
import matplotlib.pyplot as plt

hub = (50, 50)

restaurants = [
    (20, 30), (70, 20), (80, 70),
    (30, 80), (60, 60), (15, 60),
    (40, 20), (90, 40), (25, 70), (65, 90)
]

customers = [
    (15, 20), (80, 15), (90, 80),
    (20, 90), (70, 70), (10, 75),
    (35, 10), (95, 35), (20, 60), (75, 95)
]


def distance(a, b):
    return math.dist(a, b)


def dijkstra(graph, start, end):
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        dist, node, path = heapq.heappop(queue)

        if node == end:
            return dist, path

        if node in visited:
            continue

        visited.add(node)

        for neighbour, weight in graph[node]:
            if neighbour not in visited:
                heapq.heappush(
                    queue,
                    (dist + weight, neighbour, path + [neighbour])
                )

    return float("inf"), []


print("FOOD DELIVERY SHORTEST ROUTE OPTIMIZER")
n = int(input("Enter number of orders (1-10): "))

if not 1 <= n <= 10:
    print("Enter a number between 1 and 10.")
    raise SystemExit

locations = [hub]

for i in range(n):
    locations.append(restaurants[i])
    locations.append(customers[i])

# Build a road network connecting nearby locations.
# Every edge represents a road with a distance.

graph = {i: [] for i in range(len(locations))}

for i in range(len(locations)):
    neighbours = sorted(
        [
            (distance(locations[i], locations[j]), j)
            for j in range(len(locations))
            if i != j
        ]
    )[:4]

    for dist, j in neighbours:
        graph[i].append((j, dist))
        graph[j].append((i, dist))

# Find a separate shortest route for every order.

all_routes = []
total_distance = 0

for i in range(n):
    restaurant_node = 1 + 2 * i
    customer_node = restaurant_node + 1

    dist1, path1 = dijkstra(
        graph, 0, restaurant_node
    )

    dist2, path2 = dijkstra(
        graph, restaurant_node, customer_node
    )

    order_distance = dist1 + dist2

    all_routes.append((path1, path2, order_distance))
    total_distance += order_distance

    print(
        f"Order {i+1}: "
        f"Hub -> Restaurant -> Customer"
    )
    print(f"Shortest Distance: {order_distance:.2f} units")

print(f"\nTotal Distance of All Orders: {total_distance:.2f} units")

# Draw all possible road connections.

plt.figure(figsize=(10, 8))

for i in range(len(locations)):
    for j, _ in graph[i]:
        if i < j:
            a, b = locations[i], locations[j]
            plt.plot(
                [a[0], b[0]],
                [a[1], b[1]],
                color="lightgray",
                linewidth=1
            )

# Highlight each order's selected route.

for i, (path1, path2, dist) in enumerate(all_routes):
    full_path = path1 + path2[1:]

    px = [locations[p][0] for p in full_path]
    py = [locations[p][1] for p in full_path]

    plt.plot(
        px, py,
        marker="o",
        linewidth=2,
        label=f"Order {i+1}"
    )

# Draw hub, restaurants and customers.

plt.scatter(*hub, color="red", s=180, marker="s", label="Hub")

for i in range(n):
    r = restaurants[i]
    c = customers[i]

    plt.scatter(*r, color="orange", marker="^", s=100)
    plt.text(r[0] + 1, r[1] + 1, f"R{i+1}")

    plt.scatter(*c, color="green", marker="o", s=100)
    plt.text(c[0] + 1, c[1] + 1, f"C{i+1}")

plt.title("Food Delivery - Shortest Routes Using Dijkstra")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()