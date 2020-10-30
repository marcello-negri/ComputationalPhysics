import numpy as np
import random
import matplotlib as mpl
from matplotlib import pyplot as plt
from datetime import datetime



#TASK 1

def create_lattice(L, p):
    lattice = np.zeros((L,L))
    random.seed(datetime.now())
    for i in range(L):
        for j in range(L):
            appo = random.random()
            if (appo<=p):
                lattice[i][j]=-1
    return lattice

def update_mass(M, k):
    k0=int(k)
    if (len(M)<=k0):
        M.append(1)
    else:
        M[k0]=M[k0]+1

def merge_cluster(lattice, i, j, M, k1, k2):
    mi=int(min(k1,k2))
    ma=int(max(k1,k2))
    lattice[i][j]=mi
    M[mi]=M[mi]+M[ma]+1
    M[ma]=0
    for k in range(0,i+1):
        for h in range(len(lattice)):
            if (lattice[k][h]==ma):
                lattice[k][h]=mi

def hoshen_kopelman(lattice):
    M=[]
    k=1

    if (lattice[0][0]==-1):
        lattice[0][0]=k
        update_mass(M,k)
        k=k+1

    for j in range(1,len(lattice)):
        if (lattice[0][j]==-1):
            if (lattice[0][j-1]!=0):
                lattice[0][j]=lattice[0][j-1]
                update_mass(M,k)
            else:
                lattice[0][j]=k
                update_mass(M,k)
                k=k+1

    for i in range(1,len(lattice)):
        for j in range(len(lattice)):
            if(lattice[i][j]==-1):
                if (j!=0):
                    if (lattice[i][j-1]==0 and lattice[i-1][j]==0):
                        lattice[i][j]=k
                        update_mass(M,k)
                        k=k+1
                    if any([lattice[i][j-1]!=0 and lattice[i-1][j]==0,
                        lattice[i][j-1]==0 and lattice[i-1][j]!=0,
                        lattice[i][j-1]==lattice[i-1][j] and lattice[i][j-1]!=0]):
                        lattice[i][j]=max(lattice[i][j-1],lattice[i-1][j])
                        update_mass(M,lattice[i][j])
                    if all([lattice[i][j-1]!=lattice[i-1][j],
                            lattice[i][j-1]!=0, lattice[i-1][j]!=0]):
                        merge_cluster(lattice,i,j,M,lattice[i][j-1],lattice[i-1][j])
                else:
                    if (lattice[i-1][j]==0):
                        lattice[i][j]=k
                        update_mass(M,k)
                        k=k+1
                    else:
                        lattice[i][j]=lattice[i-1][j]
                        update_mass(M,lattice[i][j])

    return M



#TASK 2

def resize (v):
    v=v[v!=0]
    v=np.sort(v)
    x=[]
    y=[]
    count=1

    for i in range(len(v)):
        if (i!=(len(v)-1)):
            if (v[i]==v[i+1]):
                count=count+1
            else:
                x.append(count)
                y.append(v[i])
                count=1
        else:
            if (v[i]==v[i-1]):
                count=count+1
            else:
                x.append(count)
                y.append(v[i])

    x=np.array(x)
    x=x/float(np.sum(x))
    y=np.array(y)
    matrix=np.concatenate((x,y))
    matrix= matrix.reshape(2,len(y))

    return matrix


#plot for p<p_c

plt.title('n_s(s): p<p_c')
plt.xlabel('s')
plt.ylabel('n_s')
color=['b','g','r','y','c','k']
plt.yscale('log')
plt.xscale('log')

k=0
myrange = [0.1, 0.2, 0.3, 0.4, 0.5, 0.59274]

for i in myrange:
    lat=create_lattice(200,i)
    appo=resize(np.array(hoshen_kopelman(lat)))
    plt.plot(appo[1], appo[0],'o', c=color[k], label='p=%0.2f'%i)
    k=k+1
    print ("%i th done \n"%k)

plt.legend(title='Lattice: 200x200',loc='best')
plt.savefig('p_less_pc.jpg')
plt.close()

#plot for p>p_c

plt.title('n_s(s): p>p_c')
plt.xlabel('s')
plt.ylabel('n_s')
color=['k','b','r','y','c','g']
plt.yscale('log')
plt.xscale('log')

k=0
myrange2 = [0.59274, 0.7, 0.8, 0.9]

for i in myrange2:
    lat=create_lattice(200,i)
    appo=resize(np.array(hoshen_kopelman(lat)))
    plt.plot(appo[1], appo[0],'o', c=color[k], label='p=%0.2f'%i)
    k=k+1
    print ("%i th done \n"%k)

plt.legend(title='Lattice: 200x200',loc='best')
plt.savefig('p_great_pc.jpg')
