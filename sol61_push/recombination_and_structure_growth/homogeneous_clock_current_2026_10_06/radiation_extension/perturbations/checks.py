"""Exact new radiation+dust constraints and six-state simple-zero residue."""
import argparse,json
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--freeze-radiation-clock',action='store_true');ap.add_argument('--omit-radiation-momentum',action='store_true');ap.add_argument('--omit-radiation-tadpole',action='store_true');args=ap.parse_args()
checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
def eq(x):return s.simplify(x)==0
M,rd,rr,theta,H,pp,kappa,sigma=s.symbols('M rd rr theta H pp kappa sigma',positive=True)
z,zd,vd,vdd,vr,vrd,pi,nu,t,Pr,P=s.symbols('z zd vd vdd vr vrd pi nu t Pr P',real=True)
Rr=4*rr/3;Cr=3*Rr/2;d=M/theta;ed=rd/(2*theta);er=Rr/(2*theta);S=sigma+kappa*M*pp;A=3*M+S*d*d;T=2*M*pp+3*rd+3*Rr
beta=0 if args.freeze_radiation_clock else -H
sr=vrd+beta*vr
tadpole=0 if args.omit_radiation_tadpole else 3*Rr*z*sr
raw=-3*M*zd**2+S*nu**2+6*theta*nu*zd-2*theta*nu*t+2*M*zd*t+M*pp*z*z+2*M*pp*nu*z+3*rd*z*nu+pi*(vdd-nu)-rd*pp*vd*vd/2+rd*vd*t+Cr*(sr-nu)**2+tadpole-Rr*pp*vr*vr/2+Rr*vr*t
nusol=d*zd+ed*vd+er*vr
ck('complete_shift_constraint',eq(s.diff(raw,t).subs(nu,nusol)))
red=s.expand(raw.subs(nu,nusol));Rnu=s.diff(raw,nu).subs(t,0)
Prraw=s.diff(red,vrd)
ck('actual_radiation_canonical_momentum',eq(Prraw-(2*Cr*(vrd-H*vr-nusol)+3*Rr*z)))
# Express radiation velocity in terms of its independently retained momentum.
vrdsol=H*vr+nusol+(Pr-3*Rr*z)/(2*Cr)
RnuP=s.simplify(Rnu.subs({nu:nusol,vrd:vrdsol},simultaneous=True))
expectedR=2*S*nusol+6*theta*zd+T*z-pi-Pr
ck('lapse_reaction_after_radiation_legendre',eq(RnuP-expectedR))
Praw=s.diff(red,zd).subs(vrd,vrdsol)
Pexpect=2*A*zd+A*(rd*vd+Rr*vr)/M+d*T*z-d*pi-d*Pr
ck('new_clock_momentum_identity',eq(Praw-Pexpect))
forcez=s.diff(red,z).subs(vrd,vrdsol)
ck('full_clock_spatial_force',eq(forcez-((2*M*pp-3*Rr)*z+T*nusol+Pr)))
forcer=s.diff(red,vr).subs(vrd,vrdsol)
ck('radiation_momentum_redshift_fourH',eq(forcer-(er*expectedR-H*Pr-Rr*pp*vr)))
ck('dust_canonical_equation',eq(s.diff(red,pi)-(vdd-nusol)))
ck('dust_momentum_equation',eq(s.diff(red,vd).subs(vrd,vrdsol)-(ed*expectedR-rd*pp*vd)))
KM=s.hessian(red,[zd,vrd])/2
ck('exact_clock_radiation_kinetic_determinant',eq(KM.det()-Cr*A))
# Independently expand N sqrtgamma P(Y), after spatial integration byparts.
eps,qchi,Y,lam=s.symbols('eps qchi Y lam',positive=True)
vel=s.symbols('vel',real=True)
Ypert=qchi*qchi/2*(1+2*eps*(vel-nu)+eps*eps*(vel*vel-4*vel*nu+3*nu*nu+2*vr*t-pp*vr*vr))
rad=(1+eps*nu)*s.exp(3*eps*z)*lam*Ypert**2
radquad=s.expand(s.series(rad,eps,0,3).removeO()).coeff(eps,2).subs(lam,4*rr/(3*qchi**4))
expectedquad=Cr*(vel-nu)**2+3*Rr*z*vel-3*rr*z*nu+s.Rational(3,2)*rr*z*z-Rr*pp*vr*vr/2+Rr*vr*t
ck('direct_radiation_PY_second_variation',eq(radquad-expectedquad))
Pfun=lam*Y**2;rho=2*Y*s.diff(Pfun,Y)-Pfun
ck('radiation_positive_cs',eq(s.diff(Pfun,Y)/(s.diff(Pfun,Y)+2*Y*s.diff(Pfun,Y,2))-s.Rational(1,3)))
qcd=s.symbols('qcd',real=True);Jchi=(qchi*s.diff(Pfun,Y)).subs(Y,qchi*qchi/2)
ck('radiation_qchi_redshift',eq(s.diff(Jchi,qchi)*qcd+3*H*Jchi-3*lam*qchi*qchi*(qcd+H*qchi)))
# Raw gravity tadpoles on the actual dust+radiation background.
c,b,Vpot,qdlog,Hdot=s.symbols('c b Vpot qdlog Hdot',real=True)
Nl=1+eps*nu
hom=s.exp(3*eps*z)*(-3*M*(H+eps*zd)**2/Nl+Nl*(2*c*s.log(Nl)-Vpot)-3*b*(H+eps*zd)*s.log(Nl)-b*qdlog)
gquad=s.expand(s.series(hom,eps,0,3).removeO()).coeff(eps,2)
ck('actual_matter_density_tadpole',eq(s.diff(gquad,z,nu).subs(Vpot,3*M*H*H+2*c-3*b*H-rd-rr)-3*(rd+rr)))
mass=gquad.coeff(z,2)+9*M*(Hdot+3*H*H)
ck('radiation_pressure_mass_cancellation',eq(mass.subs(Vpot,3*M*H*H+2*M*Hdot+rr/3-b*qdlog)+s.Rational(3,2)*rr))

# Six-state exact equations, keeping physicaltime normalization.
a,alpha=s.symbols('a alpha',nonzero=True,real=True);Scross=(a-3*M)*theta**2/M**2
zds=(P-a*(rd*vd+Rr*vr)/M-d*T*z+d*pi+d*Pr)/(2*a)
nue=d*zds+ed*vd+er*vr;Rfull=2*Scross*nue+6*theta*zds+T*z-pi-Pr
pid=ed*Rfull-rd*pp*vd-3*H*pi
Prd=er*Rfull-Rr*pp*vr-4*H*Pr
Pd=(2*M*pp-3*Rr)*z+T*nue+Pr-3*H*P
flow=s.Matrix([zds,nue,H*vr+nue+(Pr-3*Rr*z)/(2*Cr),pid,Prd,Pd]);ys=s.Matrix([z,vd,vr,pi,Pr,P])
res=(a*flow.jacobian(ys)).applyfunc(s.cancel).subs(a,0)/alpha
cv=s.Matrix([1,d,d,0,0,T*d]);rv=s.Matrix([[-d*T,0,0,d,d,1]])
used=rv.copy()
if args.omit_radiation_momentum:used[0,4]=0
ck('six_state_actual_residue',s.simplify(res-cv*used/(2*alpha))==s.zeros(6))
ck('rank_one_nonzero',res.rank()==1 and res[0,5]!=0)
ck('nilpotent_residue',s.simplify(res*res)==s.zeros(6))
ck('both_matter_momenta_regular',eq(s.cancel(a*pid).subs(a,0)) and eq(s.cancel(a*Prd).subs(a,0)))
ck('clock_invariant_pole_covector',eq(s.cancel(2*a*nue).subs(a,0)-d*(rv*ys)[0]))
# Exact ad_N nilpotency, sufficient for the analytic normalform recurrence.
Z=s.Matrix(6,6,lambda i,j:s.Symbol('Z%d%d'%(i,j)))
ad=lambda B:res*B-B*res
ck('adjoint_cube_zero',s.simplify(ad(ad(ad(Z))))==s.zeros(6))
# Bounded on-background transverse zero. Not an intervalcertified existence proof.
mp.mp.dps=60;ee=mp.mpf('.5');rf=mp.mpf('.25');df=1-4*rf/3;kk=mp.mpf('.1')
def L(v):return v-mp.log(v)-1
def hh(xx):
 target=df*(xx**-3-1)+rf*(xx**-4-1)+3*mp.log(xx)
 lo=mp.mpf(1);hi=mp.mpf(2)
 for _ in range(350):
  mid=(lo+hi)/2
  if L(mid)+ee*(mid-1)**2/2>target:hi=mid
  else:lo=mid
 return 1+ee*(lo+hi)/2
def numerator(xx):return 3*ee*(1+ee-hh(xx))+kk*kk/(xx*xx)
lo=mp.mpf('.9');hi=mp.mpf('1')
ck('bounded_crossing_bracket',numerator(lo)<0 and numerator(hi)>0)
for _ in range(220):
 mid=(lo+hi)/2
 if numerator(mid)>0:hi=mid
 else:lo=mid
xx=(lo+hi)/2;hv=hh(xx);fp=hv*(1/ee-1/(hv-1));Bp=-3*df*xx**-4-4*rf*xx**-5+3/xx;hp=Bp/fp
Adot=(-3*ee*hp-2*kk*kk/xx**3)/(hv-ee)**2*xx*hv
ck('bounded_crossing_simple_derivative',Adot>mp.mpf('.1'))
ck('bounded_crossing_constraint',abs(numerator(xx))<mp.mpf('1e-45'))
row={'eta':str(ee),'rf':str(rf),'df':str(df),'k_over_Hstar_af':str(kk),'a_over_af_at_zero':str(xx),'h_at_zero':str(hv),'dKc_over_M_dt_Hstar':str(Adot),'residual':str(numerator(xx))}
out={'checks':checks,'summary':{'passed':sum(i['passed'] for i in checks),'total':len(checks)},'bounded_simple_crossing':row,'scope':'Full radiation+dust quadraticaction and sixstate analyticalsimplezero theorem; no nonlinearcontinuation, quantumdecay, CMBoratomicrecombination.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(i['passed'] for i in checks) else 1)
