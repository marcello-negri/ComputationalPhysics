# EXERCISE 6

import numpy as np
import random
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# TASK 1

def check_sphere (v, x, y, z, R):
    check = True
    for i in range(len(v)):
        dist = np.sqrt((v[i,0] - x)**2 + (v[i,1] - y)**2 + (v[i,2] - z)**2)
        if (dist<R):
            check = False

    return check

def new_sphere (vect, L, R):
    random.seed(datetime.now())
    generate = True
    while (generate):
        x = (random.random() * (L - 2*R) ) + R
        y = (random.random() * (L - 2*R) ) + R
        z = (random.random() * (L - 2*R) ) + R

        if (check_sphere(vect, x, y, z, R)):
            generate = False
    point = [x, y, z]

    return point

def create_spheres (N, L, R):
    positions = np.zeros ((N,3))
    for i in range(N):
        positions[i] = new_sphere(positions, L, R)

    return positions

def draw_spheres (vect):
    fig = plt.figure()
    plt.title('spheres in 3D')
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vect[:,0], vect[:,1], vect[:,2], c='b', marker='o')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.savefig('spheres.pdf')
    plt.close()


def calculate_d_k (vect):
    sum = 0
    N = len(vect)
    for i in range(N):
        for j in range(N):
            if (i<j):
                delta_x = vect[i,0] - vect[j,0]
                delta_y = vect[i,1] - vect[j,1]
                delta_z = vect[i,2] - vect[j,2]
                sum += np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

    return 2 * sum / (N * (N -1))

def average_distance (N, L, R, M):
    sum = 0
    for i in range(M):
        sum += calculate_d_k(create_spheres(N, L, R))
        if (i%50==0):
            print 'iteration %i'%i

    return sum / M


# TASK 2 and 3
# verify convergence of integral as a function of N and M

N = 100
R = 1
L = 100
M = 1000

interval = range (25, M, 25)
color=['b','g','r','y','c','k', 'm']
c = 0

fig = plt.figure()
plt.title('Convergence of integral')
plt.xlabel('M')
plt.ylabel('<d>')

for j in [2, 5, 10, 25, 50, 100]:
    integral = []
    print 'n = %i' %j
    for i in interval:
        integral.append(average_distance(j, L, R, i))
    plt.scatter(interval, integral, color=color[c], label='n = %i'%j)
    c += 1

plt.legend(loc='best')
plt.savefig('convergence.pdf')
plt.close()
