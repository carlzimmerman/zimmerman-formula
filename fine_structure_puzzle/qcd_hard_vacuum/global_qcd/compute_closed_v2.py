#!/usr/bin/env python3
"""Exact finite SU(3) closed-complex vacuum series; no statistical sampling."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial
import json
import sys

def cells(n, k):
    out = []
    for axes in combinations(range(5), k):
        for base in product(*[range(n) if j in axes else range(n+1) for j in range(5)]):
            if any(base[j] in (0,n) for j in range(5) if j not in axes):
                out.append((axes,base))
    return out

def faces(cell):
    axes, base = cell
    for j,a in enumerate(axes):
        rest=tuple(b for b in axes if b!=a)
        for side in (0,1):
            b=list(base);b[a]+=side
            yield (rest,tuple(b)), ((-1)**j)*(1 if side else -1)

def rank_mod(columns, prime):
    pivots={}
    for col in columns:
        v={i:c%prime for i,c in col.items() if c%prime}
        while v:
            i=min(v)
            if i not in pivots:
                scale=pow(v[i],-1,prime)
                pivots[i]={j:c*scale%prime for j,c in v.items()}
                break
            scale=v[i]
            for j,c in pivots[i].items():
                q=(v.get(j,0)-scale*c)%prime
                if q:v[j]=q
                else:v.pop(j,None)
    return len(pivots)

def tensors(k,l):
    state={(0,0):1}
    for anti in [False]*k+[True]*l:
        nxt=Counter()
        for (p,q),m in state.items():
            targets=([(p,q+1)]+([(p+1,q-1)] if q else [])+([(p-1,q)] if p else [])) if anti else ([(p+1,q)]+([(p-1,q+1)] if p else [])+([(p,q-1)] if q else []))
            for target in targets:nxt[target]+=m
        state=nxt
    return state.get((0,0),0)

def partitions(n, maxpart=None, length=3):
    if n==0:
        yield ()
    elif length:
        for a in range(min(n,n if maxpart is None else maxpart),0,-1):
            for tail in partitions(n-a,a,length-1):yield (a,)+tail

def standard_dim(lam):
    hook=1
    for i,row in enumerate(lam):
        for j in range(row):hook*=row-j+sum(other>j for other in lam[i+1:])
    return factorial(sum(lam))//hook

def schur(k,l):
    a=Counter();b=Counter()
    for n,c in ((k,a),(l,b)):
        for lam in partitions(n):
            ll=lam+(0,)*(3-len(lam))
            c[(ll[0]-ll[1],ll[1]-ll[2])]+=standard_dim(lam)
    return sum(m*b[pq] for pq,m in a.items())

def mul(a,b,N):
    c=[Q(0)]*(N+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b[:N+1-i]):c[i+j]+=x*y
    return c

def power(a,n,N):
    r=[Q(1)]+[Q(0)]*N
    for _ in range(n):r=mul(r,a,N)
    return r

def log_series(a,N):
    assert a[0]==1
    z=a[:];z[0]=0
    s=[Q(0)]*(N+1)
    for k in range(1,N+1):
        zz=power(z,k,N)
        for j in range(N+1):s[j]+=Q((-1)**(k+1),k)*zz[j]
    return s

def support_search(plaquettes, edges, cap):
    """All small supports with no singly occupied edge, independent of color.

    For selected dangling edge, assign ALL its remaining incident faces at
    once, including explicit zeros. Thus the recursion does not discard a
    possible three- or four-face junction. First occupied face is fixed to
    eliminate disconnected zero prefixes. Closed supports are recorded; a
    minimal closed support of size six cannot admit another at cap six.
    """
    eindex={e:i for i,e in enumerate(edges)}
    f_edges=[tuple(eindex[e] for e,_ in faces(p)) for p in plaquettes]
    incident=[[] for _ in edges]
    for f,es in enumerate(f_edges):
        for e in es:incident[e].append(f)
    found=set();nodes=0;premature=[]
    def go(chosen,banned):
        nonlocal nodes
        nodes+=1
        counts=Counter(e for f in chosen for e in f_edges[f])
        dangling=[e for e,c in counts.items() if c==1]
        if not dangling:
            found.add(tuple(sorted(chosen)))
            if len(chosen)<cap:premature.append(tuple(sorted(chosen)))
            # Enumerate connected supersets too: a closed support need not
            # be minimal when cap is larger than the first cube surface.
            if len(chosen)<cap:
                adjacent={f for e in counts for f in incident[e]}
                for f in sorted(adjacent-chosen-banned):
                    go(chosen|{f},banned)
            return
        options=[]
        for e in dangling:
            av=[f for f in incident[e] if f not in chosen and f not in banned]
            if not av:return
            options.append(av)
        av=min(options,key=len)
        room=cap-len(chosen)
        for size in range(1,min(room,len(av))+1):
            for add in combinations(av,size):
                go(chosen|set(add),banned|(set(av)-set(add)))
    for root in range(len(plaquettes)):
        go({root},set(range(root)))
    return found,nodes,premature

def cube_contraction(N):
    oriented=[]
    for j in range(3):
        axes=[a for a in range(3) if a!=j]
        for side in (0,1):
            verts=[]
            for aa,bb in [(0,0),(1,0),(1,1),(0,1)]:
                v=[0]*3;v[j]=side;v[axes[0]]=aa;v[axes[1]]=bb;verts.append(tuple(v))
            if ((-1)**j)*(1 if side else -1)<0:verts=list(reversed(verts))
            oriented.append(verts)
    parents={}
    def root(i):
        parents.setdefault(i,i)
        if parents[i]!=i:parents[i]=root(parents[i])
        return parents[i]
    def join(a,b):parents[root(a)]=root(b)
    links=defaultdict(list)
    for f,verts in enumerate(oriented):
        for i,v in enumerate(verts):
            w=verts[(i+1)%4]
            key=tuple(sorted((v,w)))
            row=(f,i);col=(f,(i+1)%4)
            root(row);root(col)
            links[key].append((v==key[0],row,col))
    for pair in links.values():
        assert len(pair)==2 and pair[0][0]!=pair[1][0]
        pos,neg=sorted(pair,key=lambda v:not v[0])
        join(pos[1],neg[2]);join(pos[2],neg[1])
    loops=len({root(i) for i in parents})
    assert len(links)==12
    return {"index_loops":loops,"link_integrals":len(links),"value":str(Q(N**loops,N**len(links)))}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result',required=True);args=parser.parse_args()
    checks=0
    def check(b):
        nonlocal checks
        assert b;checks+=1
    geometry=[]
    saved={}
    for n in (1,2,3):
        cs=[cells(n,k) for k in range(5)]
        expected=[comb(5,k)*n**k*((n+1)**(5-k)-(n-1)**(5-k)) for k in range(5)]
        check([len(c) for c in cs]==expected)
        check(sum((-1)**k*len(c) for k,c in enumerate(cs))==2)
        if n<=2:
            for k in (2,3,4):
                for c in cs[k]:
                    boundary2=Counter()
                    for f,s in faces(c):
                        for ff,ss in faces(f):boundary2[ff]+=s*ss
                    check(all(v==0 for v in boundary2.values()))
        datum={"n":n,"counts":expected}
        if n<=2:
            eindex={e:i for i,e in enumerate(cs[1])}
            columns=[{eindex[e]:s for e,s in faces(p)} for p in cs[2]]
            ranks={str(p):rank_mod(columns,p) for p in (1009,1013)}
            expected_rank=expected[1]-expected[0]+1
            check(all(r==expected_rank for r in ranks.values()))
            datum["rank_boundary2_mod_primes"]=ranks
            datum["expected_rank_d1"]=expected_rank
        saved[n]=cs
        geometry.append(datum)
    closed,nodes,premature=support_search(saved[1][2],saved[1][1],9)
    pindex={p:i for i,p in enumerate(saved[1][2])}
    elementary={tuple(sorted(pindex[p] for p,_ in faces(c))) for c in saved[1][3]}
    check(closed==elementary)
    check(len(closed)==40)
    contractions={str(N):cube_contraction(N) for N in (2,3,4)}
    check(contractions['3']['value']=='1/81')
    check(all(c['index_loops']==8 for c in contractions.values()))
    N=9;c0=[Q(0)]*(N+1);nf=[Q(0)]*(N+1);moments=[]
    for k in range(11):
        for l in range(11-k):
            a=tensors(k,l);b=schur(k,l);check(a==b)
            moments.append({"k":k,"l":l,"multiplicity":a})
            if k+l<=N:c0[k+l]+=Q(a,factorial(k)*factorial(l)*6**(k+l))
            if l and k+l-1<=N:nf[k+l-1]+=Q(a,3*factorial(k)*factorial(l-1)*6**(k+l-1))
    logc0=log_series(c0,N)
    inv=[Q(1)]+[Q(0)]*N
    for j in range(1,N+1):inv[j]=-sum(c0[k]*inv[j-k] for k in range(1,j+1))
    fundamental=mul(nf,inv,N)
    collective=[720*c for c in power(fundamental,6,N)]
    cube=Q(2,81*6**6)
    check(cube==Q(18,18**6))
    z6=mul(power(c0,80,N),[Q(1)+collective[0]]+collective[1:],N)
    logz=log_series(z6,N)
    check(all(logz[i]==80*logc0[i]+collective[i] for i in range(N+1)))
    # Actual endpoint with rational upper bound on exp(x): exp(x)<=1/(1-x).
    beta=Q(1,10**6);small=80*beta
    P6=sum(c*beta**i for i,c in enumerate(z6))
    remainder=small**10/Q(factorial(10))/(1-small)
    check(P6>=1)
    connected=40*cube*beta**6
    check(remainder<connected/1000)
    # The exact c0 endpoint itself is not polynomial. Both P6 and these
    # intervals are finite total-partition statements; do not call P6 Z.
    result={"status":"completed","checks":checks,"python":sys.version.split()[0],
      "geometry":geometry,"supports":{"n":1,"max_distinct_plaquettes":9,"search_nodes":nodes,"closed_supports":len(closed),"premature_closed_states_visited":len(premature),"all_are_elementary_cube_boundaries":True,"supports_sorted":sorted(closed)},
      "contractions":contractions,"su3_singlet_moments":moments,
      "series":{"c0_beta_coefficients":list(map(str,c0)),"log_c0_beta_coefficients":list(map(str,logc0)),"fundamental_character_coefficient":list(map(str,fundamental)),"collective_coefficients":list(map(str,collective)),"K1_Z_beta_coefficients_through9":list(map(str,z6)),"K1_logZ_beta_coefficients_through9":list(map(str,logz)),"cube_mixed_beta_coefficient":str(cube),"K1_collective_beta6_coefficient":str(40*cube),"n4_collective_beta6_coefficient":str(40*cube)},
      "finite_endpoint":{"beta":str(beta),"P9_minus1":str(P6-1),"absolute_Z_remainder_upper":str(remainder),"absolute_logZ_vs_logP9_error_upper":str(remainder),"connected_beta6_term":str(connected),"remainder_to_connected_term_upper":str(remainder/connected)},
      "non_claims":["No dynamical physical quarks or photon", "No physical round-S4 coefficient A", "No uniform n remainder", "No full R or alpha prediction", "General-n total-degree-six completeness not established solely by K1 enumeration"]}
    with open(args.result,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({"checks":checks,"support_nodes":nodes,"closed_supports":len(closed),"c0":list(map(str,c0)),"logc0":list(map(str,logc0)),"collective_coefficient":str(40*cube),"error_fraction":float(remainder/connected)},indent=2))

if __name__=='__main__':main()
