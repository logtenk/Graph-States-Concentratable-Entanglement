import numpy as np
import time
from itertools import combinations
from utils import *
"""
Specify the number of qubits and the edges of the graph here
"""
n=17
#E=[(0,1),(0,2),(0,3)] #star
#E=[(0,1),(1,2),(0,2),(0,3),(2,5),(1,4),(3,5),(5,4),(4,3)] #toblerone
#E=[(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(3,7),(2,6),(4,5),(5,7),(7,6),(6,4)] #cube
#E=[(1,4),(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(3,7),(2,6),(4,5),(5,7),(7,6),(6,4)] #cube+1edge
E=[(0,1),(1,2),(1,3),(2,4),(3,4),(3,5),(4,6),(5,6),(5,7),(6,8),(7,8),(7,9),(8,10),(9,10)] 

def gf2_rank(M):
    """
    Calculate the rank of a matrix over the binary field GF(2)
    based on https://stackoverflow.com/questions/56856378/fast-computation-of-matrix-rank-over-gf2
    M: (sub)matrix of adjacency matrix
    return: rank of M over GF(2)
    """
    if M.size==0:
        return 0
    rows=[]
    for row in M:
        rows.append(int(''.join(str(i) for i in row),2))

    #print("rows=",rows)
    rank=0
    while rows:
        pivot_row=rows.pop()
        if pivot_row:
            rank+=1
            lsb=pivot_row & -pivot_row
            for index, row in enumerate(rows):
                if row&lsb:
                    rows[index]=row^pivot_row
    return rank

def bipartite(M, p):
    """
    Output the M[A,B] submatrix for a bipartition (A,B) specified by p
    M: adjacency matrix
    p: a binary number of length n in which a 1 bit puts the index in set A 0 otherwise
    return: M[A,B]
    """
    n=M.shape[0]
    pstr=bin(p)[2:].zfill(n)
    A=[]
    B=[]
    for idx in range(n):
        if pstr[idx]=='1':
            A.append(idx)
        else:
            B.append(idx)
    return M[np.ix_(A,B)]

def T(M):
    """
    Calculate sum of subsystem purites
    M: adjacency matrix
    return: T(M)
    """
    n=M.shape[0]
    T=0
    for p in range(2**n):
        Mp=bipartite(M,p)
        cutrk=gf2_rank(Mp)
        T+=2**(-cutrk)
        #print("p=",bin(p)[2:].zfill(n))
        #print("Mp=",Mp)
        #print("rank=",cutrk)
        #print("\n-----------------\n")
    return int(T)

def timing(n, reps=10):
    t_tot=0
    for rep in range(reps):
        e=np.random.randint(0,2,n*(n-1)//2).astype(int)
        e=''.join([str(x) for x in e])
        M=str_to_adj(e, n)
        t0=time.perf_counter()
        T(M)
        t1=time.perf_counter()
        t_tot+=t1-t0
    t_ave=t_tot/reps
    print(f'n={n},  t={t_ave}')
    return t_ave

if __name__=='__main__':
    #M=np.zeros((n,n)).astype(int)
    #for (i,j) in E:
    #    M[i,j]=1
    #    M[j,i]=1

    #print("M=",M)
    #print("\n===================\n")

    #print(T(M))
    f=open(f'time_data/cutrk.time','w')
    for n in range(3,19):
        t=timing(n)
        f.write(f'{n} {t}\n')
    f.close()


