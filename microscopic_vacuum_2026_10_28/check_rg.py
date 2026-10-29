"""Exact checks for the conditional microscopic RG continuation."""
import json,sys
from pathlib import Path
import sympy as s
x,L,lam,a,b,F,C=s.symbols('x L lam a b F C',positive=True)
ap,bp=s.symbols('ap bp',real=True)
q=s.symbols('q',real=True)
W=2*s.sqrt(L)*(lam*x)**s.Rational(5,2)
up=a*F/b
vac=up+F
curv=(b*b+bp)*up+(a*a-ap)*F
ratio=a*b/9+(a*bp-b*ap)/(9*(a+b))
potential=F*(a*s.exp(b*q)/b+s.exp(-a*q))
checks={
 'SU2_five_flavor_cubic_energy':s.simplify(s.diff(W,x)**2-25*L*lam**5*x**3)==0,
 'stationary_balance':s.simplify(b*up-a*F)==0,
 'full_running_ratio':s.simplify(curv/(9*vac)-ratio)==0,
 'constant_slope_ratio':s.simplify(ratio.subs({ap:0,bp:0})-a*b/9)==0,
 'two_exponential_stationarity':s.simplify(s.diff(potential,q).subs(q,0))==0,
 'two_exponential_positive_curvature':s.simplify(s.diff(potential,q,2).subs(q,0)-a*(a+b)*F)==0,
 'full_offset_changes_ratio':s.simplify(curv/(9*(vac+C))-ratio*vac/(vac+C))==0,
 'compressibility_shape_test':s.simplify(s.diff(potential,q,2)-3*s.diff(potential,q)-(b*(b-3)*a*F/b*s.exp(b*q)+a*(a+3)*F*s.exp(-a*q)))==0,
 'b3_gamma_dictionary':s.simplify((a*b/9).subs({a:-2*s.Symbol('gamma'),b:3})+2*s.Symbol('gamma')/3)==0,
}
out={'claim_id':'MV28_RG','checks':{k:bool(v) for k,v in checks.items()},'integer_cubic_examples':[{'Nc':2*k,'Nf':5*k,'beta0':k,'radial_exponent':3} for k in [1,2,3]],'non_claims':['No complete orthogonal supersymmetry-breaking sector','No calculated negative singlet gamma','No full gravitational offset matching','No universal numerical ratio','No claim of protected canonical Kahler metric or original portal']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(checks.values()),checks
