#!/usr/bin/env python3
"""Exact complete Pauli Born tensor from two explicit spinor graphs."""
import json,sys
from pathlib import Path
import sympy as s

I=s.I;zz=s.zeros(2)
sig=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
g=[s.diag(1,1,-1,-1)]+[zz.row_join(a).col_join((-a).row_join(zz)) for a in sig]
metric=[1,-1,-1,-1]
nu,k,f1,f2=s.symbols('nu k F1 F2',real=True)
# Units m=1; rotational covariance allows q along the third spatial axis.
q=[nu,0,0,k];p=[1,0,0,0]
qs=nu*g[0]-k*g[3]
ps=g[0];unit=s.eye(4)
def vertex(mu,sgn):
    # i sigma^{mu nu}q_nu/(2m)=-[gamma^mu,qslash]/(4m).
    return f1*g[mu]-sgn*f2*(g[mu]*qs-qs*g[mu])/4
Gplus=[vertex(mu,1) for mu in range(4)]
Gminus=[vertex(mu,-1) for mu in range(4)]
Dp=nu*nu-k*k+2*nu
Dm=nu*nu-k*k-2*nu
Q2=k*k-nu*nu
den=Q2*Q2-4*nu*nu
T1=2*(Q2*Q2*(f1+f2)**2/den-f1*f1)
T2=8*Q2*(f1*f1+Q2*f2*f2/4)/den
pt=[p[a]+nu*q[a]/Q2 for a in range(4)]
checks=[];components={}
for mu in range(4):
    for nv in range(4):
        graphs=Gminus[mu]*(ps+qs+unit)*Gplus[nv]/Dp+Gplus[nv]*(ps-qs+unit)*Gminus[mu]/Dm
        # The time-ordered current convention has the minus of the tree
        # propagator trace; the 1/2 is the physical external spin average.
        direct=-s.trace((ps+unit)*graphs)/2
        target=(-metric[mu]*(1 if mu==nv else 0)-q[mu]*q[nv]/Q2)*T1+pt[mu]*pt[nv]*T2
        error=s.factor(direct-target)
        assert error==0,(mu,nv,str(error))
        checks.append('complete_tensor_%d%d'%(mu,nv))
        components[mu,nv]=direct
for nv in range(4):
    ward=s.factor(sum(metric[mu]*q[mu]*components[mu,nv] for mu in range(4)))
    assert ward==0,(nv,str(ward))
    checks.append('Ward_%d'%nv)
trace=s.factor(sum(metric[mu]*components[mu,mu] for mu in range(4)))
assert s.factor(trace-(-3*T1+(1+nu*nu/Q2)*T2))==0
checks.append('Minkowski_photon_trace')
r={'schema':'fsp008.independent_complete_pauli_tensor.v1','assertion_tested':'All sixteen spin-averaged Born tensor components equal the two-amplitude expression, from explicit two-graph gamma traces with arbitrary symbolic F1,F2,nu,k; four Ward identities and Lorentz trace.','domain':'Exact rational function field Q(i,F1,F2,nu,k), m=1 by units, generic off-pole kinematics; continuation supplies nu=iQx.','T1':'2[Q4(F1+F2)^2/(Q4-4nu^2)-F1^2]','T2':'8Q2[F1^2+(Q2/4)F2^2]/(Q4-4nu^2)','checks':checks,'check_count':len(checks),'limits':['No inelastic tensor or physical all-Q form factors.','Rational identities interpreted off the poles, with common analytic continuation/prescription required on poles.','Posttarget orthogonal verification; not counted as a pretarget derivation.']}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'exact_full_tensor_and_Ward_checks':len(checks)}))
