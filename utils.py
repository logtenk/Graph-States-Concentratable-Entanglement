import numpy as np
import pandas as pd
def weight(e):
    return sum(map(int, e))

def adj_to_str(M):
    n=M.shape[0]
    e=''
    for i in range(n-1):
        for j in range(i+1, n):
            e+=str(int(M[i,j]))
    return e

def str_to_adj(e, n, get_edge=False):
    edge=None
    M=np.zeros((n,n)).astype(int)
    for i in range(n-1):
        for j in range(i+1, n):
            cur_e=int(e[0])
            M[i,j]=cur_e
            M[j,i]=cur_e
            e=e[1:]
            if((edge is None) and (cur_e==1)):
                edge=(i,j)

    if get_edge:
        return M, edge
    else:
        return M

def no_i(M, i):
    return np.delete(np.delete(M, i, 0), i, 1)

def no_edge(M, edge):
    l, r=edge
    M_no_e=M.copy()
    M_no_e[l,r]=0
    M_no_e[r,l]=0
    return M_no_e

def lr_add(M, edge):
    l, r=edge
    M_lr_add=M.copy()
    M_lr_add[l, :]=(M_lr_add[l, :]+M_lr_add[r, :])%2
    M_lr_add[:, l]=(M_lr_add[:, l]+M_lr_add[:, r])%2
    M_lr_add=no_i(M_lr_add, r)
    return M_lr_add

def get_path(n, w):
    return f'data/{n}-qubit/{w}-edge.txt'

def get_data(n, e):
    if n==1:
        return 2
    w=weight(e)
    df=pd.read_csv(get_path(n, w), header=None, index_col=0, sep=' ')
    return df.loc['e'+e,1]


