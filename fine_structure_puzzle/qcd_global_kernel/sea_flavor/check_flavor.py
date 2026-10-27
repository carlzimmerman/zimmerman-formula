#!/usr/bin/env python3
"""Exact finite determinant benchmark. This is not QCD or a proton model."""
import argparse
import itertools
import json
from pathlib import Path
import sympy as s

R=s.Rational
KEYS=((0,0),(1,0),(0,1),(2,0),(1,1),(0,2))
def jet(x=0):
    return x if isinstance(x,dict) else {(0,0):s.sympify(x)}
def add(x,y):
    x,y=jet(x),jet(y)
    return {k:x.get(k,0)+y.get(k,0) for k in KEYS}
def neg(x): return {k:-v for k,v in jet(x).items()}
def mul(x,y):
    ans={k:s.S.Zero for k in KEYS}
    for a,av in jet(x).items():
        for b,bv in jet(y).items():
            k=(a[0]+b[0],a[1]+b[1])
            if sum(k)<=2: ans[k]+=av*bv
    return ans
def inv(x):
    x=jet(x); c=x[(0,0)]
    assert c!=0
    z=mul(add(x,-c),1/c)
    return mul(add(add(1,neg(z)),mul(z,z)),1/c)
def div(x,y): return mul(x,inv(y))
def scalar_pow(x,n):
    ans=jet(1)
    for _ in range(n): ans=mul(ans,x)
    return ans
def matjet(A,V,W,q):
    ans=[]
    for i in range(2):
        row=[]
        for j in range(2):
            row.append({(0,0):A[i,j],(1,0):q*V[0][i,j],
                        (0,1):q*V[1][i,j],(2,0):q*q*W[0][0][i,j]/2,
                        (1,1):q*q*W[0][1][i,j],(0,2):q*q*W[1][1][i,j]/2})
        ans.append(row)
    return ans
def determinant(A): return add(mul(A[0][0],A[1][1]),neg(mul(A[0][1],A[1][0])))
def inverse(A):
    d=determinant(A)
    return [[div(A[1][1],d),div(neg(A[0][1]),d)],
            [div(neg(A[1][0]),d),div(A[0][0],d)]]
def tr(A): return s.trace(A)
def expect(v,p): return sum((x*w for x,w in zip(v,p)),s.S.Zero)
def cov(x,y,p): return expect([a*b for a,b in zip(x,y)],p)-expect(x,p)*expect(y,p)
def cumul(x,y,z,p):
    ex,ey,ez=expect(x,p),expect(y,p),expect(z,p)
    return (expect([a*b*c for a,b,c in zip(x,y,z)],p)
            -ex*expect([b*c for b,c in zip(y,z)],p)
            -ey*expect([a*c for a,c in zip(x,z)],p)
            -ez*expect([a*b for a,b in zip(x,y)],p)+2*ex*ey*ez)
def source_derivatives(S,V,W,q):
    first=[-q*S*v*S for v in V]
    second=[[q*q*(S*V[a]*S*V[b]*S+S*V[b]*S*V[a]*S-S*W[a][b]*S)
             for b in range(2)] for a in range(2)]
    return first,second
def baryon_derivatives(S,V,W):
    # Arbitrary three-propagator observable, not a baryon contraction.
    qu,qd=R(2,3),R(-1,3)
    du,ddu=source_derivatives(S,V,W,qu)
    dd,ddd=source_derivatives(S,V,W,qd)
    x,y=S[0,0],S[1,1]
    B=x*x*y
    Ba=[2*x*du[a][0,0]*y+x*x*dd[a][1,1] for a in range(2)]
    Bab=[[2*du[a][0,0]*du[b][0,0]*y+2*x*ddu[a][b][0,0]*y
           +2*x*du[a][0,0]*dd[b][1,1]+2*x*du[b][0,0]*dd[a][1,1]
           +x*x*ddd[a][b][1,1] for b in range(2)] for a in range(2)]
    return B,Ba,Bab

def run():
    configs=[s.Matrix([[3,1],[1,4]]),s.Matrix([[4,2],[1,5]]),s.Matrix([[5,-1],[2,3]])]
    V=[s.Matrix([[1,2],[-1,1]]),s.Matrix([[2,-1],[3,0]])]
    W=[[s.Matrix([[1,1],[0,-1]]),s.Matrix([[0,2],[1,1]])],
       [s.Matrix([[0,2],[1,1]]),s.Matrix([[2,0],[-1,1]])]]
    probs=[R(1,6),R(1,3),R(1,2)]
    charges=[R(2,3),R(-1,3),R(-1,3)]
    ml=R(1,2)
    checks=0; records=[]
    def checked(ok):
        nonlocal checks
        assert bool(ok)
        checks+=1
    nonzero_contact=False; nonzero_cumulant_correction=False
    for delta in [R(0),R(1,4),R(1),R(2)]:
        Bs=[]; Bas=[[],[]]; Babs=[[[],[]],[[],[]]]
        Las=[[],[]]; Labs=[[[],[]],[[],[]]]; Ts=[[],[]]
        numerator=jet(0); denominator=jet(0)
        hsall=[]; loops=[]; splitchecks=[]
        for k,D0 in enumerate(configs):
            Sl=(D0+ml*s.eye(2)).inv()
            Ss=(D0+(ml+delta)*s.eye(2)).inv()
            checked(Sl-Ss==delta*Sl*Ss)
            B,Ba,Bab=baryon_derivatives(Sl,V,W)
            Bs.append(B)
            for a in range(2):
                Bas[a].append(Ba[a]); Ts[a].append(tr(Sl*Ss*V[a]))
                La=R(1,3)*tr((Sl-Ss)*V[a])
                checked(La==delta*Ts[a][-1]/3)
                Las[a].append(La)
                for b in range(2):
                    Babs[a][b].append(Bab[a][b])
                    hl=tr(Sl*W[a][b]-Sl*V[a]*Sl*V[b])
                    hs=tr(Ss*W[a][b]-Ss*V[a]*Ss*V[b])
                    Lab=R(5,9)*hl+R(1,9)*hs
                    Labs[a][b].append(Lab)
                    P=Sl*Ss
                    rhs=delta*tr(-P*W[a][b]+P*V[a]*Ss*V[b]+Sl*V[a]*P*V[b])
                    checked(hs-hl==rhs)
            # Independent construction: polynomial determinant and adjugate.
            dj=[]; Sj=[]
            for m,q in zip([ml,ml,ml+delta],charges):
                A=matjet(D0+m*s.eye(2),V,W,q)
                dj.append(determinant(A)); Sj.append(inverse(A))
            weight=jet(1)
            for d in dj: weight=mul(weight,div(d,d[(0,0)]))
            Bj=mul(scalar_pow(Sj[0][0][0],2),Sj[1][1][1])
            numerator=add(numerator,mul(mul(weight,Bj),probs[k]))
            denominator=add(denominator,mul(weight,probs[k]))
            # Rademacher split-even estimator and its finite-noise product bias.
            noise=[s.Matrix(v) for v in itertools.product([-1,1],repeat=2)]
            A=Ss*V[0]*Sl; E=Ss*V[1]*Sl
            samplesA=[(eta.T*A*eta)[0] for eta in noise]
            samplesE=[(eta.T*E*eta)[0] for eta in noise]
            checked(sum(samplesA)/4==tr(Sl*Ss*V[0]))
            checked(sum(samplesE)/4==tr(Sl*Ss*V[1]))
            independent=sum(a*b for a in samplesA for b in samplesE)/16
            checked(independent==tr(A)*tr(E))
            bias=sum(a*b for a,b in zip(samplesA,samplesE))/4-independent
            splitchecks.append(str(bias))
        Cjet=div(numerator,denominator)
        tensor=[]
        for a in range(2):
            row=[]
            for b in range(2):
                val=expect(Babs[a][b],probs)
                mixed=cov(Bas[a],Las[b],probs)+cov(Bas[b],Las[a],probs)
                same=cov(Bs,Labs[a][b],probs)
                separate=cumul(Bs,Las[a],Las[b],probs)
                reduced=(cov(Bs,Labs[a][b],probs)+delta*(cov(Bas[a],Ts[b],probs)
                         +cov(Bas[b],Ts[a],probs))/3
                         +delta*delta*cumul(Bs,Ts[a],Ts[b],probs)/9)
                checked(reduced==same+mixed+separate)
                key=(2,0) if (a,b)==(0,0) else ((0,2) if (a,b)==(1,1) else (1,1))
                direct=Cjet[key]*(2 if a==b else 1)
                checked(direct==val+mixed+same+separate)
                # Vacuum determinant source second derivative, without baryon.
                zdirect=denominator[key]*(2 if a==b else 1)
                checked(zdirect==expect([lab+la*lb for lab,la,lb in zip(Labs[a][b],Las[a],Las[b])],probs))
                ordinary=cov(Bs,[la*lb for la,lb in zip(Las[a],Las[b])],probs)
                if ordinary!=separate: nonzero_cumulant_correction=True
                contact=R(5,9)*cov(Bs,[tr((d+ml*s.eye(2)).inv()*W[a][b]) for d in configs],probs)
                contact+=R(1,9)*cov(Bs,[tr((d+(ml+delta)*s.eye(2)).inv()*W[a][b]) for d in configs],probs)
                if contact!=0: nonzero_contact=True
                row.append({name:str(value) for name,value in [('valence',val),('mixed',mixed),('same_loop',same),('separate_loops',separate),('total',direct),('dropped_cumulant_error',ordinary-separate),('sea_W_contact',contact)]})
            tensor.append(row)
        if delta==0:
            checked(all(v==0 for row in Las for v in row))
            checked(tensor[0][0]['same_loop']!='0')
            # The first allowed coefficients of omitted classes; exact rational.
            mixed_slope=(cov(Bas[0],Ts[0],probs)*2)/3
            separate_leading=cumul(Bs,Ts[0],Ts[0],probs)/9
            checked(mixed_slope!=0); checked(separate_leading!=0)
            leading={'mixed_delta_coefficient':str(mixed_slope),'separate_delta_squared_coefficient':str(separate_leading)}
        records.append({'delta':str(delta),'C0':str(expect(Bs,probs)),
                        'mean_L0':str(expect(Las[0],probs)),'tensor':tensor,
                        'same_noise_product_bias_per_configuration':splitchecks})
    checked(nonzero_contact); checked(nonzero_cumulant_correction)
    return {'status':'passed','assertion_tested':'Finite determinant-quotient source jets equal the complete normalized flavor decomposition; exact resolvent and unbiased split-even trace products hold on all declared cases.',
            'domain':'Q, exact SymPy rationals; 3 explicit noncommuting 2x2 matrices; 2 source coordinates; 4 mass splittings',
            'checks':checks,'cases':records,'leading_coefficients_at_degeneracy':leading,
            'non_claims':['No QCD ensemble or physical baryon','No proton mass or H limit','No numerical alpha or cosmological fit','No stochastic cost or variance claim']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); result=run()
    path=Path(args.output); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','domain']}))
