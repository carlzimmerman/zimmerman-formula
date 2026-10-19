"""Independent checks of only the continuation beyond FSP003."""
import json,sys
from pathlib import Path
import sympy as s
import mpmath as m
m.mp.dps=45
q=s.Rational
a0,a1,a2,a3,g=s.symbols('a0 a1 a2 a3 g')
v=s.symbols('v1 v2 v3'); av=s.Matrix([a1,a2,a3]); vv=s.Matrix(v)
newa=av*(1-vv.dot(vv)/2)+a0*vv-av.cross(vv)
def contract(poly):
    answer=0
    for powers,c in s.Poly(s.expand(poly),*v).terms():
        n=sum(powers)
        if n==0: answer+=c
        if n==2 and 2 in powers: answer+=c*g
    return s.expand(answer)
mass=contract(a0*(1-vv.dot(vv)/2)-av.dot(vv))
charge=contract(newa[0]**2+newa[1]**2)
s0=a1*a1+a2*a2
constraint=a0*a0+a1*a1+a2*a2+a3*a3-1
assert s.expand(mass-a0*(1-3*g/2))==0
assert s.expand(charge-(s0*(1-4*g)+2*g)-2*g*constraint)==0

def Z(x,y):
    return m.quad(lambda t:m.exp(-y*t)*m.besseli(0,x*m.sqrt(1-t)),[0,1])
def T(x,y):
    den=Z(x,y)
    ma=m.quad(lambda t:m.exp(-y*t)*m.sqrt(1-t)*m.besseli(1,x*m.sqrt(1-t)),[0,1])/den
    ms=m.quad(lambda t:t*m.exp(-y*t)*m.besseli(0,x*m.sqrt(1-t)),[0,1])/den
    return 2*y+m.mpf('1.5')*x*ma-4*y*ms
def matched(x,y): return T(x,y)-m.mpf('1.5')*x-2*y
def charge_matched(x,y): return matched(x,y)-matched(x,0)
def fmt(x): return m.nstr(x,34)
x=m.mpf('1.7'); y=m.mpf('.4'); dg=m.mpf('1e-7')
def shifted_w(gg): return 2*y*gg-m.log(Z(x*(1-m.mpf('1.5')*gg),y*(1-4*gg)))
fd=(shifted_w(dg)-shifted_w(-dg))/(2*dg)
assert abs(fd-T(x,y))<m.mpf('1e-12')
assert abs((T(x,y)-T(x,0)-2*y)-charge_matched(x,y))<m.mpf('1e-42')

# One fixed-parameter metric difference with an explicit finite-mu logarithm.
omega=8*m.pi**2/3; A=x/omega; B=y/omega
kappa=1/(8*m.pi**2); c=m.mpf('.013'); mu=m.mpf('1.3')
def geom(H):
    volume=omega/H**4; xx=A*volume; yy=B*volume
    gg=H**2*(c+kappa*m.log(mu**2/H**2))
    return volume,xx,yy,gg
def corr(H):
    vol,xx,yy,gg=geom(H)
    return gg*charge_matched(xx,yy)
vol,xx,yy,gg=geom(m.mpf(1))
DT=m.diff(lambda t:charge_matched(xx*m.exp(t),yy*m.exp(t)),0)
Hg=2*gg-2*kappa
rho=(gg*DT-Hg*charge_matched(xx,yy)/4)/vol
dh=m.mpf('1e-6')
rho_fd=-(corr(m.exp(dh))-corr(m.exp(-dh)))/(8*dh*vol)
assert abs(rho-rho_fd)<m.mpf('1e-13')

# Heat residue and a strong-counterterm normalization cross-check, all rational.
pole_green=q(1,6)/16  # R/(96*pi²*epsilon)
pole_mass=3*pole_green/2
delta_l13=-pole_mass/4
assert pole_green==q(1,96) and delta_l13==-q(1,256)
pred_em_beta=q(4,3); source_em_beta=q(2,3)
result={'status':'completed','assertion_tested':'First nonconstant-pion source contraction, aligned Gaussian subtraction and fixed-mu metric derivative; no repeated base grid',
 'exact_contractions':{'mass':str(mass),'s_before_constraint':str(charge),'s_after_constraint':'(1-4g)s+2g'},
 'one_source_case':{'x':fmt(x),'y':fmt(y),'T':fmt(T(x,y)),'finite_difference':fmt(fd),'difference':fmt(abs(fd-T(x,y)))},
 'matched_charge_correction':fmt(charge_matched(x,y)),
 'one_metric_case':{'rho_formula':fmt(rho),'rho_difference':fmt(rho_fd),'absolute_difference':fmt(abs(rho-rho_fd))},
 'UV':{'pi2_times_epsilon_Gbar_over_R':str(pole_green),'pi2_times_epsilon_delta_l13':str(delta_l13),'literal_operator_predicted_beta15_pion':str(pred_em_beta),'printed_source_beta15_pion':str(source_em_beta),'translation_resolved':False},
 'non_claims':['No full NLO pion+photon result','No k15 RG/basis reconciliation','No physical finite curvature LECs fixed','No epsilon-regime extrapolation to fixed-mass infinite volume','No alpha selection']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'completed','source_difference':result['one_source_case']['difference'],'metric_difference':result['one_metric_case']['absolute_difference'],'RG_translation_resolved':False}))
