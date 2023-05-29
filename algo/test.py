import numpy as np

path = [
    (75, 25),
    (30.0, 30.0),
    (25, 75),
    (25, 75),
    (70.0, 80.0),
    (80.0, 120.0),
    (120.0, 130.0),
    (125, 175),
    (125, 175),
    (120.0, 130.0),
    (80.0, 130.0),
    (30.0, 131.0),
    (30.0, 171.0),
    (75, 175),
]
print(path[0 : 4 - 1])
i = 1
p1 = path[i]
p2 = path[i + 1]
p3 = path[i + 2]
p1 = np.array(p1)
p2 = np.array(p2)
p3 = np.array(p3)

pv1 = p2 - p1
pv2 = p3 - p2


dot = np.dot(pv1, pv2)

print(dot)

dis1 = np.linalg.norm(pv1)
dis2 = np.linalg.norm(pv2)

print(dis1, dis2)
angle = np.abs(np.arccos(-1 * np.dot(pv1, pv2) / (dis1 * dis2)))


print(angle * (180 / np.pi))
