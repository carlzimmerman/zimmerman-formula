import sympy as S
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true');o=ap.parse_args()
r,g,Q,D,mu,A,P,V,W=S.symbols('r gamma Q D mu A P V W',real=True,nonzero=True)
U=r*r/2-V-W+(Q-1-g*r*r)**2/(2*g)
L=U-Q*D
on=-D+r*r/2-V-W-g*D*D/2-g*D*r*r
off=-D+r*r/2-V-W+g*r**4/2
checks={}
checks['on_branch']=S.simplify(L.subs(Q,1+g*(D+r*r))-on)==0
checks['off_branch']=S.simplify(L.subs(Q,1)-off)==0
checks['KKT_off_multiplier']=S.simplify((S.diff(U,Q)-D-mu).subs({Q:1,mu:-D-r*r}))==0
# Generic derivative labels: integration by parts of A(b Pi_t-a Pi_x).
a,b,At,Ax,Pit,Pix,Pi,ab,ba=S.symbols('a b A_t A_x Pi_t Pi_x Pi a_x b_t')
original=A*(b*Pit-a*Pix)
div=At*b*Pi+A*ba*Pi+A*b*Pit-Ax*a*Pi-A*ab*Pi-A*a*Pix
top=Pi*(-b*At+a*Ax)
checks['topological_IBP']=S.simplify((original-div-top).subs(ba,ab))==0
# Pi equation at fixed phi has sign fixed by the topological term.
Wp,Ea=S.symbols('Wp exp2alpha')
ELpi=(-1 if o.mutate else 1)*(-b*At+a*Ax)-Ea*Wp
checks['clock_slice_A_equation']=S.simplify(ELpi-(a*(Ax-b/a*At)-Ea*Wp))==0
# Direct metric/canonical identity using original action and exact D.
N,Lscale,Ebeta=S.symbols('N L Ebeta',positive=True)
ell,T=S.symbols('ell T',real=True)
rr=S.sqrt(a*a/N**2-b*b/Lscale**2)
dd=(-b*T+a*ell)/(N*Lscale*rr)
Lm=N*Lscale*Ebeta*on.subs({r:rr,D:dd})
checks['normal_Hilbert_canonical']=S.simplify(Lscale*S.diff(Lm,Lscale)+b*S.diff(Lm,b)+ell*S.diff(Lm,ell)-Lm)==0
checks['scalar_contraction_on']=S.simplify(a*S.diff(Lm,a)+b*S.diff(Lm,b)-N*Lscale*Ebeta*rr**2*(1-2*g*dd))==0
Lmoff=N*Lscale*Ebeta*off.subs({r:rr,D:dd})
checks['scalar_contraction_off']=S.simplify(a*S.diff(Lmoff,a)+b*S.diff(Lmoff,b)-N*Lscale*Ebeta*rr**2*(1+2*g*rr**2))==0
H=U.subs(Q,A*r)
coefficient=(S.diff(H,r)-mu*A)/r
checks['Hilbert_coefficient']=S.simplify(coefficient-(1+(A*r-1-g*r*r)/g*(A/r-2*g)-mu*A/r))==0
out={'checks':checks,'all_pass':all(checks.values()),'mutation':o.mutate,'scope':'exact algebra; layer estimates have separate analytic hypotheses'}
open(o.output,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
