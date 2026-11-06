import sympy as s
import json
M,a,K,B,E,rho,p,pt=s.symbols('M a K B E rho p pt',nonzero=True)
Ca,Cm,CH,CA,CP=s.symbols('Ca Cm CH CA CP')
ax,Kx=s.symbols('ax Kx')
r,D,Wp=s.symbols('r D Wp')
nrho=-(rho+p)*K-2*(rho+pt)*B
nE=-a*B-B*E
nB=-a*E+(-3*B*B+E*E-p/M)/2
Z=B*B-E*E+(p-rho-2*pt)/(2*M)
nK=-ax+a*a-K*K+Z
eB=(K-B)*E+Cm
eE=K*B+(B*B-3*E*E)/2-rho/(2*M)+CH
ep=(rho+p)*(a+Ca)+2*(pt-p)*E+r*D*CA-Wp*CP
jets={a:ax,K:Kx,B:eB,E:eE,p:ep}
def ex(z):return sum(s.diff(z,x)*v for x,v in jets.items())
# n(eB) = e(nB) -(a+Ca)nB-K eB.
nCm=s.expand(ex(nB)-(a+Ca)*nB-K*eB-(nK-nB)*E-(K-B)*nE)
# n(eE) = e(nE) -(a+Ca)nE-K eE.
nCH=s.expand(ex(nE)-(a+Ca)*nE-K*eE-nK*B-K*nB-B*nB+3*E*nE+nrho/(2*M))
nCm=s.factor(nCm);nCH=s.factor(nCH)
zero={Ca:0,Cm:0,CH:0,CA:0,CP:0}
out={'n_Cmom':str(nCm),'n_CH':str(nCH),
 'coefficients_Cmom':{str(x):str(s.factor(s.diff(nCm,x))) for x in zero},
 'coefficients_CH':{str(x):str(s.factor(s.diff(nCH,x))) for x in zero},
 'independent_sources_zero':s.simplify(nCm.subs(zero))==0 and s.simplify(nCH.subs(zero))==0,
 'spatial_K_a_derivatives_cancel':not nCm.has(ax,Kx) and not nCH.has(ax,Kx)}
print(json.dumps(out,indent=2))
