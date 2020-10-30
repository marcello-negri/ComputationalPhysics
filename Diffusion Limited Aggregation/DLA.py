# EXERCISE 7

import random
from datetime import datetime
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# TASK

def check_position_discrete (vect, x, y):
    for i in range(len(vect)):
        if ((vect[i][0]-x)**2 + (vect[i][1]-y)**2) <= 1:
            return True
    return False

def initial_position_discrete(time):
    random.seed(datetime.now())
    length = random.randint(0,8*time)
    if length<=2*time:
        return [length-time,time]
    elif length>2*time and length<=4*time:
        return [time, 3*time-length]
    elif length>4*time and length<=6*time:
        return [5*time-length,-time]
    else:
        return [-time, length-7*time]


def random_walk_discrete (vect, time, step):
    random.seed(datetime.now())
    go_on = True
    retry = True

    while (retry):
        walk = [initial_position_discrete(time)] # starting on a square of radius time
        while (go_on):
            appo = random.randint(0,3) # walk proceeds with unitary steps
            if appo == 0:
                x = walk[-1][0] + 1
                y = walk[-1][1]
            elif appo == 1:
                x = walk[-1][0]
                y = walk[-1][1] + 1
            elif appo == 2:
                x = walk[-1][0] - 1
                y = walk[-1][1]
            elif appo == 3:
                x = walk[-1][0]
                y = walk[-1][1] - 1

            if (abs(x) > (time+step) or abs(y) > (time+step)):
                break

            walk.append([x,y])

            if check_position_discrete (vect, x, y):
                return [x,y]


def graph_walk_discrete (vector, length, step):
    color=['b','g','r','y','c','k','m']*10
    c = 0

    plt.title('Diffusion limited aggregation: discrete walk')
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
    plt.axis('equal')
    plt.savefig('dla.pdf')
    plt.close()

vector = [[0,0]]
length = 250
step = 15

for iter in range(15,70,step):
    for i in range(0,length):
        appo = random_walk_discrete(vector,iter,step)
        vector.append(appo)
        print "iteration %i"%i
    print "step %i"%iter

graph_walk_discrete (vector, length, step)
