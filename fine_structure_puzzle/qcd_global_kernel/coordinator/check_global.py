"""Exact coefficients for FSP-008; writes only the caller's fresh result file."""
import json
import sys
from pathlib import Path
import sympy as s

x=s.symbols('x')
q=s.Rational
zeta=lambda n:s.zeta(n,q(3,2)).expand(func=True)
bracket=1/(2*x**2)-1/(8*x)
for k in range(7):
    bracket+=(-x)**k/s.factorial(k)*(zeta(-3-2*k)-zeta(-1-2*k)/4)
heat=s.series(s.exp(q(9,4)*x)*bracket/3,x,0,5).removeO().expand()
coeff={n:s.simplify(heat.coeff(x,n)) for n in range(-2,4)}
assert [coeff[n] for n in [-2,-1,0,1]]==[q(1,6),q(1,3),q(29,90),q(37,189)]
CA,nf,TF,NV,g,u,ell=s.symbols('CA nf TF NV g u ell')
b0=(11*CA-4*nf*TF)/3
G=NV*(CA*(49+33*ell)/(144*s.pi**2)-nf*TF*(5+3*ell)/(36*s.pi**2))
DG=-2*s.diff(G,ell)
assert s.simplify(DG+NV*b0/(8*s.pi**2))==0
rhoV=s.simplify(g**2*DG/8)
assert s.simplify(rhoV+NV*b0*g**2/(64*s.pi**2))==0
S=s.symbols('S')
Wq=u*S*(5+3*ell)/(72*s.pi**2)
rhoVq=s.simplify(s.diff(Wq,ell)/2)
assert rhoVq==S*u/(48*s.pi**2)
regauge=-NV*b0*g**2/(16*s.pi**2)
assert s.simplify(4*rhoV-regauge)==0
rea=S*u/(12*s.pi**2)
assert s.simplify(4*rhoVq-rea)==0
charges=[q(2,3),-q(1,3),-q(1,3)]
sq=3*sum(c*c for c in charges)
assert sq==2
a=q(62*9+11*9,360)
assert a==q(73,40)
omega=8*s.pi**2/3
free=s.simplify(a/omega)
strong=s.simplify(rhoV.subs({NV:8,CA:3,nf:3,TF:q(1,2)})/omega)
photon=s.simplify(rhoVq.subs({S:sq})/omega)
assert free==q(219,320)/s.pi**2
assert strong==-27*g*g/(64*s.pi**4)
assert photon==u/(64*s.pi**4)
alphaslope=s.simplify(4*s.pi*s.diff(photon,u))
assert alphaslope==1/(16*s.pi**3)
scalar_leading=s.simplify(3*coeff[1]/(32*s.pi**2))
assert scalar_leading==q(37,2016)/s.pi**2
result={'status':'completed','assertion_tested':'Exact scalar heat coefficients and source-UV sphere logarithmic coefficient, group-trace and RG conversions in declared theories','heat_coefficients':{str(n):str(v) for n,v in coeff.items()},'a_free':str(a),'rho_UV_over_H4':str(free+strong+photon),'leading_partial_alpha_rho_over_H4':str(alphaslope),'scalar_H6_over_M2_coefficient':str(scalar_leading),'physical_R_computed':False,'alpha_derived':False,'non_claims':['No full proton or curved nonperturbative QCD evaluation','No continuation of weak-sphere expansion to H=0','No mixed three-loop coefficient','Scalar heat series is asymptotic, not a complete global determinant']}
out=Path(sys.argv[1]);out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
