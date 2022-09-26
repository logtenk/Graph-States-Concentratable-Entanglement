import numpy as np
import cutrk
import time
from utils import *

CHECK=False
n=18
#E=[(0,1),(0,2),(0,3)] #star
E=[(0,1),(1,2),(0,2),(0,3),(2,5),(1,4),(3,5),(5,4),(4,3)] #toblerone
#E=[(1,4),(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(3,7),(2,6),(4,5),(5,7),(7,6),(6,4)] #cube+1edge

def calc_T(n, e):
    #w=weight(e)
    M, edge=str_to_adj(e, n, True)
    if(n<=2):
        return cutrk.T(M)
    if not edge:
        return 2**n
    l, r=sorted(edge)
    

    no_l=calc_T(n-1, adj_to_str(no_i(M, l)))
    no_r=calc_T(n-1, adj_to_str(no_i(M, r)))
    no_lr=calc_T(n-2, adj_to_str(no_i(no_i(M, r), l)))
    no_e=calc_T(n, adj_to_str(no_edge(M, edge)))
    lr_add_value=calc_T(n-1, adj_to_str(lr_add(M, edge)))
    T=2*no_l+2*no_r-3*no_lr-no_e+lr_add_value

    if CHECK:
        T1=cutrk.T(M)
        print(f'-----------------\ncalc_T for {n} {e}\n')
        print(M)
        print(edge)
        print(f'from cutrk:{T1}, from recurrent:{T}')
        if(T1!=T):
            print('\n'*5+'--------ERROR:inconsitent T----------'+'\n'*5)
            exit()

    return T


def timing(n, Emax=9, reps=10):
    f=open(f'time_data/recurrent_{n}.time','w')
    for E in range(1,Emax+1):
        t_tot=0
        for rep in range(reps):
            e=np.zeros(n*(n-1)//2).astype(int)
            cur_E=E
            while(cur_E>0):
                idx=int(np.random.randint(len(e)))
                if e[idx]==0:
                    e[idx]=1
                    cur_E-=1
            e=''.join([str(x) for x in e])
            t0=time.perf_counter()
            calc_T(n,e)
            t1=time.perf_counter()
            t_tot+=t1-t0
        t_ave=t_tot/reps
        print(f'n={n}, E={E}, t={t_tot}')
        f.write(f'{E} {t_tot}\n')
    f.close()


if __name__=='__main__':
    #M=np.zeros((n,n)).astype(int)
    #for (i,j) in E:
    #    M[i,j]=1
    #    M[j,i]=1

    #print("M=",M)
    #print("\n===================\n")

    #print(calc_T(n, adj_to_str(M)))
    for n in [5,10,15]:
        timing(n)



