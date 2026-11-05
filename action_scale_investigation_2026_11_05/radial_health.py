"""Scoped radial principal symbol on saved static toy backgrounds."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
checks={}
def check(name,ok):
 checks[name]=bool(ok);print(('PASS ' if ok else 'FAIL ')+name,flush=True)
r,N,B,p,Np,Bp,pp,m2,K,b,q,V,gam,ss=s.symbols('r N B p Np Bp pp M2 K b q V gamma s',positive=True)
X=q*q/(2*N*N);rho=X+V;a=s.sqrt(b*rho);d=pp+2*p/r
W=a*a/K*(-p/a-s.log(1-p/a))
L=m2*(N*B+N/B+2*r*Np/B)+N*B*r*r*(X-V-W)+r*r*p*Np/K-gam*N*r*r*d*d/(2*K*K*B)
y=[B,N,p];yp=[s.Symbol('Bprime'),Np,pp]
mix=s.Matrix([[s.diff(L,yi,yj) for yj in yp] for yi in y])
anti=mix-mix.T
check('BN derivative mixing',s.simplify(anti[0,1]+2*m2*r/B**2)==0)
check('Np derivative mixing',s.simplify(anti[1,2]+r*r/K+gam*r*r*d/(K*K*B))==0)
check('polarization spatial Hessian',s.simplify(s.diff(L,pp,2)+gam*N*r*r/(K*K*B))==0)
check('no lapse diagonal derivative coefficient',s.diff(L,N,Np)==0)
h=ss+ss/(1+ss)-2*s.log(1+ss)
T=1+b/(2*K)*h-b/(2*K)*X/rho*ss**3/(1+ss)
T_used=s.Integer(1) if args.mutate else T
ANN=s.diff(L,N,2)
ANNsub=s.expand_log(ANN.subs(p,a*ss/(1+ss)),force=True)
check('exact lapse Hessian retains density portal',s.simplify(ANNsub-2*B*r*r*X/N*T_used)==0)

# Shift contribution from the ADM extrinsic-curvature eigenvalues.
vel,shift,shiftp=s.symbols('Bdot shift shiftp',real=True)
kr=(vel/B-shiftp-shift*Bp/B)/N;kt=-shift/(N*r)
Ltime=s.expand(m2*N*B*r*r/2*((kr*kr+2*kt*kt)-(kr+2*kt)**2))
Ltarget=2*m2*r/N*shift*vel-m2*r/N*(Bp+B*Np/N)*shift**2
boundary_derivative=m2*((B+r*Bp)/N-r*B*Np/N**2)*shift**2+2*m2*B*r/N*shift*shiftp
check('shift integration by parts',s.simplify(Ltime+boundary_derivative-Ltarget)==0)
shift_sol=s.solve(s.diff(Ltarget,shift),shift)[0]
Mt=2*m2*r/(N*(Bp+B*Np/N))
check('shift-eliminated time Hessian',s.simplify(s.diff(Ltarget.subs(shift,shift_sol),vel,2)-Mt)==0)

# Generic Hermitian constrained symbol with arbitrary lower-order terms.
kk,cp=s.symbols('k cp',positive=True)
aa,an,ap_,abn,abp,anp,cc,db,dn=s.symbols('aa an ap abn abp anp c db dn',real=True)
H=s.Matrix([[aa,abn+s.I*kk*cc,abp+s.I*kk*db],
 [abn-s.I*kk*cc,an,anp+s.I*kk*dn],
 [abp-s.I*kk*db,anp-s.I*kk*dn,ap_-cp*kk**2]])
Hp=H[:2,:2]-H[:2,2:]*H[2:,:2]/H[2,2]
Heff=s.cancel(Hp[0,0]-Hp[0,1]*Hp[1,0]/Hp[1,1])
lim=s.limit(Heff/kk**2,kk,s.oo)
check('generic constrained radial principal coefficient',s.simplify(lim+cc**2/(an+dn*dn/cp))==0)

dd=s.symbols('d',real=True)
z=gam*dd/(K*B)
D0=2*X*T+(1+z)**2/gam
num=2*X+b*X/K*h+dd/(K*B)+gam*dd*dd/(K*K*B*B)
Aeff=B*r*r/N*D0
bg_sum=B*r/(2*m2)*(B*B*(2*X+b*X/K*h)+B*dd/K+gam*dd*dd/(K*K))
physical_speed=(2*m2*r/B**2)**2/Aeff*(N*bg_sum/(2*m2*r))*B*B/(N*N)
check('physical radial characteristic speed',s.simplify(physical_speed-num/D0)==0)
check('subluminality difference',s.simplify(D0-num-((1+z)/gam-b*X*X/(K*rho)*ss**3/(1+ss)))==0)

base=Path(__file__).resolve().parent
saved=json.loads((base/'evidence/shell/result.json').read_text())
rows=[]
for case in saved['cases']:
 bb=case['b'];length=case['Lstar'];gamma=.5*length**2/2;rr=np.array(case['profile']['r']);f=np.array(case['profile']['scaled_fields'])
 NN=np.exp(1e-4*f[0]);BB=np.exp(1e-4*f[1]);XX=2e-9/(2*NN*NN);rrho=XX+1e-8
 aref=np.sqrt(bb*(1e-9+1e-8));aa0=np.sqrt(bb*rrho);pol=f[2]*aref;div=f[3]*aref
 su=pol/(aa0-pol);hh=su+su/(1+su)-2*np.log1p(su)
 tt=1+bb*hh-bb*XX/rrho*su**3/(1+su)
 zz=gamma*div/(.5*BB)
 denom=2*XX*tt+(1+zz)**2/gamma
 numer=2*XX+bb*XX/.5*hh+div/(.5*BB)+gamma*div**2/(.25*BB**2)
 speed=numer/denom
 bg=BB*rr/2*(BB*BB*(2*XX+bb*XX/.5*hh)+BB*div/.5+gamma*div**2/.25)
 kinetic=2*rr/(NN*bg)
 row={'b':bb,'Lstar':length,'points':len(rr),'min_kinetic':float(min(kinetic)),
      'min_denominator':float(min(denom)),'min_speed2':float(min(speed)),'max_speed2':float(max(speed)),
      'min_two_clock_T':float(min(tt)),'positive':bool(np.all(kinetic>0) and np.all(denom>=1e-12) and np.all(speed>0) and np.all(speed<=1))}
 rows.append(row);print(json.dumps(row),flush=True)
check('four profiles and804 samples',len(rows)==4 and sum(x['points'] for x in rows)==804)
check('sampled radial kinetic gradient and speed signs',all(x['positive'] for x in rows))
out={'passed':all(checks.values()),'mode':'omit_portal_lapse' if args.mutate else 'main','checks':checks,'rows':rows,
     'scope':'Spherical static-branch short-wave symbol only; no full health, finite-k stability, causality or normalization claim.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');raise SystemExit(0 if out['passed'] else 1)
