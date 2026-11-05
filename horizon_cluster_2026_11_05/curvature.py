"""HC-006: exact tensor calculation for a static spherical GR metric.
python horizon_cluster_2026_11_05/curvature.py OUTPUT
"""
import sympy as s,json,sys
from pathlib import Path
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
t,r,th,ph=s.symbols('t r theta phi',real=True);m,L=s.symbols('m Lambda',positive=True)
x=[t,r,th,ph];f=1-2*m/r-L*r*r/3
g=[-f,1/f,r*r,r*r*s.sin(th)**2];gi=[1/v for v in g]
Gamma={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   v=gi[a]*(s.diff(g[a],x[b])*int(a==c)+s.diff(g[a],x[c])*int(a==b)-s.diff(g[b],x[a])*int(b==c))/2
   if v!=0:Gamma[a,b,c]=s.simplify(v)
def ga(a,b,c):return Gamma.get((a,b,c),s.S.Zero)
Rm={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   for d in range(4):
    v=s.diff(ga(a,b,d),x[c])-s.diff(ga(a,b,c),x[d])+sum(ga(a,e,c)*ga(e,b,d)-ga(a,e,d)*ga(e,b,c) for e in range(4))
    if v!=0:
     v=s.simplify(s.trigsimp(v))
     if v!=0:Rm[a,b,c,d]=v
Ric=s.Matrix(4,4,lambda b,d:s.simplify(sum(Rm.get((a,b,a,d),0) for a in range(4))))
R=s.simplify(sum(gi[a]*Ric[a,a] for a in range(4)))
Ric2=s.simplify(sum(gi[a]*gi[b]*Ric[a,b]**2 for a in range(4) for b in range(4)))
K=s.simplify(s.trigsimp(sum(gi[a]*gi[b]*gi[c]*gi[d]*(g[a]*v)**2 for (a,b,c,d),v in Rm.items())))
W=s.simplify(K-2*Ric2+R**2/3)
checks={
 'Ricci_scalar':s.simplify(R-4*L)==0,
 'Einstein_metric':all(s.simplify(Ric[a,b]-(L*g[a] if a==b else 0))==0 for a in range(4) for b in range(4)),
 'Ricci_square':s.simplify(Ric2-4*L**2)==0,
 'Kretschmann':s.simplify(K-(48*m*m/r**6+8*L*L/3))==0,
 'Weyl_square':s.simplify(W-48*m*m/r**6)==0,
 'flat_limit':s.simplify(K.subs({m:0,L:0}))==0,
 'deSitter_Weyl_zero':s.simplify(W.subs(m,0))==0,
 'Schwarzschild_Ricci_zero':s.simplify(R.subs(L,0))==0}
# Equality of mass tidal curvature and vacuum contribution defines a mass-dependent radius.
req=(18*m*m/L**2)**s.Rational(1,6)
checks['curvature_equality']=s.simplify(W.subs(r,req)-8*L*L/3)==0
acc=m/req**2 # geometric acceleration; physical multiply by c²
checks['acceleration_mass_exponent_one_third']=s.simplify(m*s.diff(acc,m)/acc-s.Rational(1,3))==0
checks['acceleration_Lambda_exponent_two_thirds']=s.simplify(L*s.diff(acc,L)/acc-s.Rational(2,3))==0
assert all(checks.values()),checks
payload={'metric':'diag(-f,1/f,r²,r² sin²theta), f=1-2m/r-Lambda*r²/3; m=GM/c²',
 'domain':'r>0, sin(theta)!=0, f!=0 coordinate patch; algebraic invariants extend where geometry regular',
 'R':str(R),'Ricci2':str(Ric2),'Kretschmann':str(K),'Weyl2':str(W),
 'curvature_equality_radius':str(req),'mass_acceleration_at_equality':str(s.simplify(acc)),
 'checks':checks,'count':len(checks),
 'conclusion':'Equality of Weyl and vacuum curvature contributions gives mass-dependent acceleration, not a universal a0 or selected 32pi coefficient.'}
(out/'results.json').write_text(json.dumps(payload,indent=2)+'\n');print(json.dumps(payload,indent=2))
