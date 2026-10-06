import sympy as z
s=z.symbols('s',positive=True);xi=z.symbols('xi',real=True);a,b,N,L=z.symbols('a b N L',positive=True);u,h1,h2=z.symbols('u h1 h2');n=z.S(3);w=h1-h2;v=a*a*h1/N**2-b*b*h2/L**2

def inv(nn,aa):
 S1=-(u*u+n*w*w)/nn**2+2*n*v*w/aa**2
 S2=(u+n*w)*(-u/nn**2+n*v/aa**2)
 S3=-nn**2*(-u/nn**2+n*v/aa**2)**2
 S4=-(u+n*w)**2/nn**2
 S5=-u*u/nn**2-2*n*w*w/nn**2-n*nn**2*v*v/aa**4
 return S1-S2,3*S1-2*S2-S4+S5-S3
Ug,Rg=inv(N,a);Uh,Rh=inv(L,b);U=(Ug+Uh)/2;R=(Rg+Rh)/2
kin=-6*(a**3*h1*h1/N+b**3*h2*h2/L)+z.sqrt(N*L)*(a*b)**z.Rational(3,2)*(-U/2+xi*R/2)
kin=z.factor(kin.subs({a:1,N:1,L:1,b:s*s}))
H=z.hessian(kin,[h1,h2,u]);det=z.factor(H.det());P=(xi+1)*(s**6+2*s**5+3*s**4+3*s**2+2*s+1)+(4*xi+2)*s**3
expected=-z.Rational(27,8)*s*(s-1)**4*(s+1)**2*(s*s+1)**2*(4*xi-1)**2*P

import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['common_global','loose_bound','mass_cancel']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=z.factor(z.cancel(e));rows.append({'name':name,'passed':e==0,'residual':str(e)})
def ck(name,b,e=''):rows.append({'name':name,'passed':bool(b),'residual':str(e)})
eq('raw_exact_critical_det',det-expected)
ck('common_critical_rank1',H.subs(s,1).rank()==1)
ck('offcritical_masscancel_rank3',H.subs({s:2,xi:z.Rational(3,8)}).rank()==3)
eq('lapsefree_xi_quarter_det',det.subs(xi,z.Rational(1,4)))
ck('lapsefree_xi_quarter_rank2_off',H.subs({s:2,xi:z.Rational(1,4)}).rank()==2)
B=(s**3+s**(-3)-2)+2*(s**2+s**(-2)-2)+3*(s+s**(-1)-2)
eq('sharp_positivity_dictionary',P/s**3-((xi+1)*B+16*xi+14))
for j in [1,2,3]:eq('reciprocal_positive_square_'+str(j),s**j+s**(-j)-2-(s**j-1)**2/s**j)
poly=11*s**6+22*s**5+33*s**4+28*s**3+33*s**2+22*s+11
mass=-z.Rational(27,256)*s*(s-1)**4*(s+1)**2*(s*s+1)**2*poly
eq('mass_cancel_exact_rank_witness',det.subs(xi,z.Rational(3,8))-mass)
eps=z.symbols('eps');near=z.series(det.subs(s,1+eps),eps,0,5).removeO()
eq('critical_near_fourth_order',near+108*(4*xi-1)**2*(8*xi+7)*eps**4)
eq('mass_cancel_near_coefficient',z.expand(near.subs(xi,z.Rational(3,8)))+270*eps**4)
ck('old_loose_bound_counterexample',P.subs({s:1,xi:-z.Rational(9,10)})<0,P.subs({s:1,xi:-z.Rational(9,10)}))
if args.mutation=='common_global':eq('claim_common_rank1_global',det)
if args.mutation=='loose_bound':ck('claim_P_positive_xi_greater_minus1',P.subs({s:1,xi:-z.Rational(9,10)})>0)
if args.mutation=='mass_cancel':eq('claim_TTmasscancel_homogeneous_degenerate',det.subs(xi,z.Rational(3,8)))
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'mutation':args.mutation,'scope':'critical regular linear homogeneous Hessian offshell; no on-shell/Dirac/ghost conclusion'},indent=2)+'\n');print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failed':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)
