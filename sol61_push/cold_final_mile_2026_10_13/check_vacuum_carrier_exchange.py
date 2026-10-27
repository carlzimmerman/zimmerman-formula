import sys,json
import sympy as s
H,b,c,v,Qb,Qc,k,K=s.symbols('H b c v Qb Qc k K',positive=True)
checks=0
def ck(x):
 global checks
 assert s.simplify(x)==0;checks+=1
bdot=-3*H*b-Qb;cdot=-3*H*c+Qc;vdot=Qb-Qc
ck(bdot+cdot+vdot+3*H*(b+c))
ck(vdot-Qb+Qc)
ck((K*vdot)-K*(Qb-Qc))
# Naive added cold creation but unchanged vacuum history has uncancelled source.
ck(bdot+cdot+Qb+3*H*(b+c)-Qc)
# Ordinary massive growing population: physical dust pressure versus effective exponent.
a=s.symbols('a',positive=True);rho=a**(k-3);rdot=s.diff(rho,a)*a*H
ck(rdot+3*H*rho-k*H*rho)
ck(rdot+3*H*(1-k/3)*rho)
ck(rdot.subs(k,3))
assert s.simplify((rdot+3*H*rho).subs(k,3))==3*H;checks+=1
json.dump(dict(checks=checks,balanced_vacuum_derivative='Q_bv-Q_vc',naive_total_conservation_defect='Q_vc',scope='Exact homogeneous reciprocal-energy identity, not an adopted BH or carrier microphysics model'),open(sys.argv[1],'w'),indent=2)
