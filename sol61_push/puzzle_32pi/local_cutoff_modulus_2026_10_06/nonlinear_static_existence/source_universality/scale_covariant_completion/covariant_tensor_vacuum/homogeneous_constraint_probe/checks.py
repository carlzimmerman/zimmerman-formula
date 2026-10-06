"""Exact homogeneous Hessian of both-lapse averaged-connection action."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['gaugefix_lapses','common_rank_global','all_repairs_lapse_free']);args=ap.parse_args();rows=[]
def eq(name,e):
 e=s.factor(s.cancel(e));rows.append({'name':name,'passed':e==0,'residual':str(e)})
def ck(name,b,e=''):rows.append({'name':name,'passed':bool(b),'residual':str(e)})
u,v,w,N,L,a,b,n=s.symbols('u v w N L a b n',positive=True)
S1=-(u*u+n*w*w)/N**2+2*n*v*w/a**2
S2=(u+n*w)*(-u/N**2+n*v/a**2)
S3=-N**2*(-u/N**2+n*v/a**2)**2
S4=-(u+n*w)**2/N**2
S5=-u*u/N**2-n*N**2*v*v/a**4-2*n*w*w/N**2
SS=[S1,S2,S3,S4,S5];U=s.expand(S1-S2);J=s.expand(3*S1-2*S2-S4+S5)
def raw(D):
 C={(0,0,0):u}
 for i in range(1,D+1):C[0,i,i]=v;C[i,0,i]=w;C[i,i,0]=w
 cov=[-N*N]+[a*a]*D;inv=[1/z for z in cov]
 tr=[sum(C.get((j,i,j),0) for j in range(D+1)) for i in range(D+1)]
 bar=[sum(inv[j]*C.get((i,j,j),0) for j in range(D+1)) for i in range(D+1)]
 return [sum(inv[i]*C.get((j,i,k),0)*C.get((k,i,j),0) for i in range(D+1) for j in range(D+1) for k in range(D+1)),sum(bar[i]*tr[i] for i in range(D+1)),sum(cov[i]*bar[i]**2 for i in range(D+1)),sum(inv[i]*tr[i]**2 for i in range(D+1)),sum(cov[i]*inv[j]*inv[k]*z*z for (i,j,k),z in C.items())]
for D in [3,4,5]:
 for i,z in enumerate(raw(D)):eq('raw_S%d_n%d'%(i+1,D),z-SS[i].subs(n,D))
# Coincident positions, arbitrary relative velocities (do not set C=0 first).
eq('common_Upsilon',U.subs(v,a*a*w/N**2)+n*(n-1)*w*w/N**2)
eq('common_J',J.subs(v,a*a*w/N**2)+(u-n*w)**2/N**2)
eq('common_S3',S3.subs(v,a*a*w/N**2)+(u-n*w)**2/N**2)
# Exact homogeneous exchange-average and regular linear interaction.
h1,h2,K,m,xi,eta=s.symbols('h1 h2 K m xi eta');Hc=s.symbols('Hc');V=a*a*h1/N**2-b*b*h2/L**2
replace={v:V,w:h1-h2}
def sym(z):
 zg=z.subs(replace,simultaneous=True)
 zh=z.subs({N:L,a:b,v:V,w:h1-h2},simultaneous=True)
 return s.factor((zg+zh)/2)
Us,Js,R3=map(sym,[U,J,S3]);vol=s.sqrt(N*L)*(a*b)**(n/2)
Lu=s.diff(Us,u)
eq('exact_Upsilon_u',Lu+n*(L*L*a*a-N*N*b*b)*(a*a*h1+b*b*h2)/(2*L*L*N*N*a*a*b*b))
eq('exact_JminusS3_u',s.diff(Js-R3,u)-4*Lu)
eq('exact_J_u_u',s.diff(Js,u,2)+(1/N**2+1/L**2))
eq('exact_S3_u_u',s.diff(R3,u,2)+(1/N**2+1/L**2))
LK=-K*n*(n-1)*(a**n*h1*h1/N+b**n*h2*h2/L)+K*vol*(-m*Us+(xi*Js+eta*R3)/2)
full=s.hessian(LK,[h1,h2,u]);common=s.factor(LK.subs({a:1,b:1,N:1,L:1,h1:Hc+w/2,h2:Hc-w/2}))
expected=-2*K*n*(n-1)*Hc**2-K*n*(n-1)*(s.Rational(1,2)-m)*w*w-K*(xi+eta)*(u-n*w)**2/2
eq('common_full_kinetic',common-expected)
HC=s.hessian(common,[Hc,w,u]);eq('common_det',HC.det()-4*K**3*n*n*(n-1)**2*(xi+eta)*(2*m-1))
for name,mm,xx,ee,rank in [('regular_added',s.Rational(1,4),s.Rational(1,4),0,3),('regular_tuned',s.Rational(1,4),s.Rational(1,4),-s.Rational(1,4),2),('critical_added',s.Rational(1,2),s.Rational(1,2),0,2),('critical_tuned',s.Rational(1,2),s.Rational(1,2),-s.Rational(1,2),1)]:
 ck('common_rank_'+name,HC.subs({n:3,K:1,m:mm,xi:xx,eta:ee}).rank()==rank)
# Full physical five velocity coordinates, leaving both lapse velocities intact.
dN,dL,da,db,dT=s.symbols('dN dL da db dT');physical=LK.subs({h1:da/a,h2:db/b,u:dN/N-dL/L},simultaneous=True);H5=s.hessian(physical,[dN,dL,da,db,dT]);null=s.Matrix([N,L,0,0,0]);aux=s.Matrix([0,0,0,0,1])
ck('common_lapse_velocity_null',all(s.simplify(z)==0 for z in H5*null));ck('auxiliary_velocity_null',H5*aux==s.zeros(5,1))
# Tuned S3 counterterm cancels u² but only xi=m/2 also removes u dependence.
eq('tuned_no_u2',s.diff(LK.subs(eta,-xi),u,2))
eq('tuned_remaining_u',s.diff(LK.subs(eta,-xi),u)-K*vol*(2*xi-m)*Lu)
eq('fully_lapse_free_linear_choice',s.diff(LK.subs(eta,-xi).subs(xi,m/2),u))
# Arbitrarily nearby off-shell metric states: n3,N=L=a=1,b=1+epsilon.
r=s.symbols('r',positive=True);eps=s.symbols('eps');det=s.factor(full.det().subs({N:1,L:1,a:1,b:r,n:3,K:1,eta:-xi}));series=s.series(det.subs(r,1+eps),eps,0,3).removeO()
eq('near_common_tuned_det',s.expand(series)-216*(m-2*xi)**2*(1-2*m)*eps**2)
example=s.factor(full.det().subs({N:1,L:1,a:1,b:2,n:3,K:1,m:s.Rational(1,4),xi:s.Rational(1,4),eta:-s.Rational(1,4)}))
ck('tuned_repair_nearby_rank3',example!=0,example)
# Tensor repair and globally lapse-free choice cannot coexist for positive m,n>=3.
threshold=m*n/(n+1);eq('tensor_mass_at_lapse_free',m*n-(m/2)*(n+1)-m*(n-1)/2)
if args.mutation=='gaugefix_lapses':eq('claim_gaugefix_captures_added_lapse_Hessian',HC[2,2])
if args.mutation=='common_rank_global':eq('claim_common_tuning_removes_nearby_rank',216*(m-2*xi)**2*(1-2*m))
if args.mutation=='all_repairs_lapse_free':eq('claim_stable_tensor_threshold_lapse_free',threshold-m/2)
args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'mutation':args.mutation,'scope':'regular linear invariant continuation homogeneous Hessian; no Dirac or ghost theorem'},indent=2)+'\n');print(json.dumps({'passed':sum(r['passed'] for r in rows),'total':len(rows),'failed':[r for r in rows if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in rows) else 1)
