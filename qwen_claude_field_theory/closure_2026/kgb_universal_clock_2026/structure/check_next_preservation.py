#!/usr/bin/env python3
"""One supplied seed, independently refined/differentiated with mpmath.

No scan and no rank assignment. A nonzero next determinant excludes only this
seed from simultaneous next preservation. Units and source calibration remain
the conditional exterior conventions of the parent construction.
"""
import argparse
import json
import mpmath as mp
import closed_inverse as c


def parts(eps,point):
    X,F,y,U,w=point
    a=c.normalized(eps,y,X,U,w,F,backend=mp)
    A=mp.matrix([-2*a['gamma']*a['Rrad']/a['p'],-a['gamma']/U])
    direction=mp.matrix([0,1,1/(a['ry']*w),-2*a['g']*a['Q']/w,a['W']/w])
    def varied(t,index):
        q=mp.matrix(point)+t*direction
        row=c.normalized(eps,q[2],q[0],q[3],q[4],q[1],backend=mp)
        return row[('kappa','gamma')[index]]
    B=mp.matrix([mp.diff(lambda t:varied(t,index),0) for index in (0,1)])
    return a,A,B


def next_parts(eps,point,f):
    a,A,B=parts(eps,point)
    X,F,y,U,w=point
    direction=mp.matrix([1,f,f/(a['ry']*w),-2-2*f*a['g']*a['Q']/w,f*a['W']/w])
    def varied(t,index):
        _,aa,bb=parts(eps,mp.matrix(point)+t*direction)
        return aa[index]+f*bb[index]
    N=mp.matrix([mp.diff(lambda t:varied(t,index),0) for index in (0,1)])
    return a,A,B,N


def check(dps=60):
    with mp.workdps(dps):
        e1,e2,X,F,y1,U1=map(mp.mpf,('1e-6','2e-6','.5','.525','.1','3e-8'))
        start=tuple(map(mp.mpf,('-20.82451969','-27.44309','.15379369','.0260058','259.6853685')))
        def evaluate(w1,w2,y2,u2,f):
            p1=(X,F,y1,U1,w1);p2=(X,F,y2,e2*u2,w2)
            a,A1,B1=parts(e1,p1);b,A2,B2=parts(e2,p2)
            E=A1-A2+f*(B1-B2)
            return (a['P']-b['P'],a['kappa']-b['kappa'],a['gamma']-b['gamma'],E[0],E[1])
        initial=evaluate(*start)
        scales=tuple(max(abs(v),mp.mpf(1)) for v in initial)
        # Fixed initial scales alter conditioning only; no residual is projected.
        fun=lambda *args:tuple(v/scale for v,scale in zip(evaluate(*args),scales))
        root=mp.findroot(fun,start,tol=mp.power(10,-dps+15),maxsteps=30,verify=True)
        w1,w2,y2,u2,f=root
        a,A1,B1,N1=next_parts(e1,(X,F,y1,U1,w1),f)
        b,A2,B2,N2=next_parts(e2,(X,F,y2,e2*u2,w2),f)
        A=A1-A2;B=B1-B2;N=N1-N2
        determinant=N[0]*B[1]-N[1]*B[0]
        norm=lambda v:mp.sqrt(sum(x*x for x in v))
        normalized=determinant/(norm(N)*norm(B))
        controls=[-N[i]/B[i] if B[i] else None for i in (0,1)]
        string=lambda v:None if v is None else mp.nstr(v,dps)
        return dict(dps=dps,seed=[string(v) for v in root],
                    ordering=['w1','w2','y2','u2=U2/epsilon2','f'],
                    raw_first_residual=[string(v) for v in evaluate(*root)],
                    A=[string(v) for v in A],B=[string(v) for v in B],N=[string(v) for v in N],
                    next_determinant=string(determinant),normalized_next_determinant=string(normalized),
                    independent_j_controls=[string(v) for v in controls],
                    scope='One supplied regular seed, high-precision finite evidence; no universal no-go or interval construction')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--dps',type=int,default=60)
    args=parser.parse_args()
    print(json.dumps(check(args.dps),indent=2))
