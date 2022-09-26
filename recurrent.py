import numpy as np
import pandas as pd
import os
import cutrk
from itertools import combinations as combinations
from utils import *

UPDATE=True
CHECK=False
NMAX=5

def calc_T(n, e):
    #w=weight(e)
    M, edge=str_to_adj(e, n, True)
    l, r=sorted(edge)

    no_l=get_data(n-1, adj_to_str(no_i(M, l)))
    no_r=get_data(n-1, adj_to_str(no_i(M, r)))
    no_lr=get_data(n-2, adj_to_str(no_i(no_i(M, r), l)))
    no_e=get_data(n, adj_to_str(no_edge(M, edge)))
    lr_add_value=get_data(n-1, adj_to_str(lr_add(M, edge)))
    T=2*no_l+2*no_r-3*no_lr-no_e+lr_add_value

    if CHECK:
        T1=cutrk.T(M, n)
        print(f'-----------------\ncalc_T for {n} {e}\n')
        print(M)
        print(edge)
        print(f'from cutrk:{T1}, from recurrent:{T}')
        if(T1!=T):
            print('\n'*5+'--------ERROR:inconsitent T----------'+'\n'*5)
            exit()



    return T


def update_nw(n, w):
    f_path=get_path(n, w)
    if (os.path.isfile(f_path) and not UPDATE):
        return 1
    length=n*(n-1)//2
    f=open(f_path, 'w')
    for comb in combinations(range(length), w):
        #t0=time.perf_counter()
        e=['0' for i in range(length)]
        for idx in comb:
            e[idx]='1'
        e=''.join(e)
        T=calc_T(n, e)
        f.write(f'e{e} {T}\n')
        #t1=time.perf_counter()
        #print(f'n={n}, time to retrieve data={t1-t0:0.4f}')
    f.close()



def update_n(n):
    folder_n=f'data/{n}-qubit'
    if(not os.path.isdir(folder_n)):
        os.mkdir(folder_n)
        with open(os.path.join(folder_n, '0-edge.txt'), 'w') as f:
            f.write('e'+'0'*(n*(n-1)//2)+' '+str(2**n))
        
    for w in range(1, n*(n-1)//2+1):
        update_nw(n, w)




if __name__=='__main__':
    #print(calc_T(3, '100'))
    #print(get_data(3, '001'))
    for n in range(3, NMAX+1):
        print(f'updating for n={n}...')
        update_n(n)



