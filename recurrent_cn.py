import numpy as np
import cutrk
import time
from utils import *
from graph_utils import *

CHECK=False
n=15
E=[(0,1)]
#E=[(0,1),(0,2),(0,3)] #star
#E=[(0,1),(1,2),(0,2),(0,3),(2,5),(1,4),(3,5),(5,4),(4,3)] #toblerone
#E=[(1,4),(0,1),(1,3),(3,2),(2,0),(0,4),(1,5),(3,7),(2,6),(4,5),(5,7),(7,6),(6,4)] #cube+1edge
#E=[(0,1),(2,3)]
def calc_T_cn(M, cn):
    n=M.shape[0]
    M1=M.copy()
    for i in range(n):
        M1[n-1,i]=M[cn,i]
        M1[cn,i]=M[n-1,i]
    M2=M1.copy()
    for i in range(n):
        M1[i, n-1]=M2[i, cn]
        M1[i, cn]=M2[i, n-1]

    #print(M1)
    colored=np.zeros(n-1).astype(int)
    colored[0]=1
    colored=floodfill(no_i(M1, n-1), 0, colored)
    A=[]
    B=[]
    
    for i in range(n-1):
        if colored[i]==1:
            A.append(i)
        else:
            B.append(i)
    #print(A,B)
    ml=M1[np.ix_(A,A)].copy()
    mr=M1[np.ix_(B,B)].copy()
    A.append(n-1)
    B.append(n-1)
    mlo=M1[np.ix_(A,A)].copy()
    mro=M1[np.ix_(B,B)].copy()
    l=calc_T_sparse(ml)
    r=calc_T_sparse(mr)
    lo=calc_T_sparse(mlo)
    ro=calc_T_sparse(mro)
    return l*r+(lo-l)*(ro-r)



def calc_T_e(M):
    #print('using calc e')
    edge=get_edge(M)
    l, r=sorted(edge)
    

    no_l=calc_T_sparse(no_i(M, l))
    no_r=calc_T_sparse(no_i(M, r))
    no_lr=calc_T_sparse(no_i(no_i(M, r), l))
    no_e=calc_T_sparse(no_edge(M, edge))
    lr_add_value=calc_T_sparse(lr_add(M, edge))
    T=2*no_l+2*no_r-3*no_lr-no_e+lr_add_value

    return T

def calc_T_sparse(M):
    #print(M)
    Mlist=partition(M)
    #print(Mlist)
    T=1
    for cur_M in Mlist:
        cur_n=cur_M.shape[0]
        if(cur_n==1):
            T*=2
        elif(cur_n<=2):
            T*=cutrk.T(cur_M)
        else:
            cn=get_critical_node(cur_M)
            if cn!=-1:
                #print('====================')
                #print('using cn for')
                #print(M)
                #print(cn)
                T*=calc_T_cn(cur_M, cn)
            elif cur_n<=2:
                T*=cutrk.T(cur_M)
            else:
                T*=calc_T_e(cur_M)
    return T



def timing(n, Emax=20, reps=1):
    f=open(f'time_data/recurrent_cn_{n}.time','w')
    Emax=n
    #for E in np.linspace(1,Emax,15,dtype=int):
    for E in np.arange(1,Emax,3,dtype=int):
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
            M=str_to_adj(e,n)
            t0=time.perf_counter()
            T=calc_T_sparse(str_to_adj(e,n))
            t1=time.perf_counter()
            t_tot+=t1-t0
            if CHECK:
                T1=cutrk.T(M)
                print(f'-----------------\ncalc_T for {n}\n')
                print(M)
                print(f'from cutrk:{T1}, from recurrent:{T}')
                if(T1!=T):
                    print('\n'*5+'--------ERROR:inconsitent T----------'+'\n'*5)
                    exit()
        t_ave=t_tot/reps
        print(f'n={n}, E={E}, t={t_tot}')
        f.write(f'{E} {t_tot}\n')
    f.close()


if __name__=='__main__':
    #M=np.zeros((n,n)).astype(int)
    #for (i,j) in E:
    #    M[i,j]=1
    #    M[j,i]=1
    #print(calc_T_sparse(M))
    for n in [200]:
        timing(n)



