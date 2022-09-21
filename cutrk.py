import numpy as np
from itertools import combinations
"""
Specify the number of qubits and the edges of the graph here
"""
n=8
#E=[(0,1),(0,2),(0,3)] #star
#E=[(0,1),(1,2),(0,2),(0,3),(2,5),(1,4),(3,5),(5,4),(4,3)] #toblerone
#E=[(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(3,7),(2,6),(4,5),(5,7),(7,6),(6,4)] #cube
E=[(1,4),(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(3,7),(2,6),(4,5),(5,7),(7,6),(6,4)] #cube+1edge

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

def bipartite(M, p, n=n):
    """
    Output the M[A,B] submatrix for a bipartition (A,B) specified by p
    M: adjacency matrix
    p: a binary number of length n in which a 1 bit puts the index in set A 0 otherwise
    return: M[A,B]
    """
    pstr=bin(p)[2:].zfill(n)
    A=[]
    B=[]
    for idx in range(n):
        if pstr[idx]=='1':
            A.append(idx)
        else:
            B.append(idx)
    return M[np.ix_(A,B)]

def T(M, n=n):
    """
    Calculate sum of subsystem purites
    M: adjacency matrix
    return: T(M)
    """
    T=0
    for p in range(2**n):
        Mp=bipartite(M,p,n)
        cutrk=gf2_rank(Mp)
        T+=2**(-cutrk)
        #print("p=",bin(p)[2:].zfill(n))
        #print("Mp=",Mp)
        #print("rank=",cutrk)
        #print("\n-----------------\n")
    return int(T)


if __name__=='__main__':
    M=np.zeros((n,n)).astype(int)
    for (i,j) in E:
        M[i,j]=1
        M[j,i]=1

    print("M=",M)
    print("\n===================\n")

    print(T(M))

