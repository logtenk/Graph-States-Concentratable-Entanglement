from utils import *
def floodfill(M, i, colored):
    for j in range(len(colored)):
        if M[i,j]==1 and colored[j]==0:
            colored[j]=1
            colored=floodfill(M, j, colored)
    return colored

def partition(M):
    #returns list of subgraphs
    cur_M=M.copy()
    Mlist=[]
    while(cur_M.size>0):
        cur_n=cur_M.shape[0]
        if cur_n==1:
            Mlist.append(cur_M)
            break

        colored=np.zeros(cur_n).astype(int)
        colored[0]=1
        colored=floodfill(cur_M,0,colored)
        #print('===========================')
        #print(cur_M)
        #print(colored)
        #print('===========================')
        A=[]
        B=[]
        for i in range(cur_n):
            if colored[i]==1:
                A.append(i)
            else:
                B.append(i)
        Amatrix=cur_M[np.ix_(A,A)].copy()
        Mlist.append(Amatrix)
        if len(B)==0:
            break
        cur_M=cur_M[np.ix_(B,B)].copy()

    return Mlist

def get_best_edge(M):
    n=M.shape[0]
    best_len=0
    best_var=9999
    best_edge=None
    for i in range(n-1):
        for j in range(i+1,n):
            if M[i,j]==1:
                Mlist=partition(M)
                size_list=np.array([M.shape[0] for M in Mlist])
                cur_var=np.var(size_list)
                cur_len=len(size_list)
                if (cur_len>best_len or (cur_len==best_len and cur_len>1 and cur_var<best_var)):
                    best_var=cur_var
                    best_len=cur_len
                    best_edge=(i,j)
    return best_edge

def get_critical_node(M):
    #print('>>>>>>>>>>>>>>>>>>>>>>')
    #print('getting cn for ')
    #print(M)
    n=M.shape[0]
    best_len=1
    best_var=9999
    best_i=-1
    for i in range(n):
        Mlist=partition(no_i(M,i))
        size_list=np.array([M.shape[0] for M in Mlist])
        #print(i)
        #print(Mlist)
        #print(size_list)
        cur_var=np.var(size_list)
        cur_len=len(size_list)
        if (cur_len>best_len or (cur_len==best_len and cur_len>1 and cur_var<best_var)):
            best_var=cur_var
            best_len=cur_len
            best_i=i
    #print(best_i)
    return best_i

