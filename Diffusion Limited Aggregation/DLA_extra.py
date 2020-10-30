# EXERCISE 7

import random
from datetime import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# OPTIONAL TASK
# generate a DLA cluster in continuous space

def initial_position_continuous(time):
    random.seed(datetime.now())
    angle = random.random() * 2 * np.pi
    x = time * np.cos(angle)
    y = time * np.sin(angle)

    return [x,y]

def check_position_continuous (vect, x, y, tolerance):
    for i in range(len(vect)):
        if np.sqrt((vect[i][0]-x)**2 + (vect[i][1] - y)**2) <= tolerance:
            return True

    return False

def random_walk_continuous (vect, time, step, tol):
    random.seed(datetime.now())
    go_on = True
    retry = True

    while (retry):
        walk = [initial_position_continuous(time)] # starting on a circle of radius time
        while (go_on):
            angle = random.random() * 2 * np.pi
            x = walk[-1][0] + np.cos(angle) # walk proceeds with unitary steps
            y = walk[-1][1] + np.sin(angle)

            if (np.sqrt(x**2 + y**2) > (time+step)):
                break

            walk.append([x,y])

            if check_position_continuous(vect, x, y, tol):
                return [x,y]

    return walk

def graph_walk_continuous (vector, length):
    color=['b','g','r','y','c','k','m']*10
    c = 0
    plt.title('Diffusion limited aggregation: continuous walk')
    plt.xlabel('x')
    plt.ylabel('y')

    for i in range(0,len(vector)-1,length):
        x = []
        y = []
        for j in range(i,i+length):
            x.append(vector[j][0])
            y.append(vector[j][1])
        plt.plot(x, y, '.', color=color[c])
        c+=1

    plt.savefig('dla2.pdf')
    plt.close()

vector = [[0,0]]
length = 250
tol = 1
step = 15

for iter in range(15,70,step):
    for i in range(0,length):
        vector.append(random_walk_continuous(vector,iter,step,tol))
        print "iteration %i"%i
    print "step %i"%iter

graph_walk_continuous (vector, length)
