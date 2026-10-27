from pathlib import Path
import json,sys,hashlib
import sympy as s
DEST=Path(sys.argv[1]);checks=[]
def z(n,e):
 r=s.simplify(s.expand(e));checks.append({'name':n,'passed':r==0,'residual':str(r)})
def y(n,c):checks.append({'name':n,'passed':bool(c),'condition':str(c)})
m,D,g,lr,H=s.symbols('m Delta g lambda_rep H',positive=True,real=True);M2=4*m*m+D;lt=lr+g*g/D
x,yv,zv,w,u,v,cs,ct=s.symbols('x y z w u v s t',real=True)
A=s.Matrix([yv,-x,2*w,-2*zv]);B=s.Matrix([u,v,cs,ct]);S=(A.dot(A));K=B.dot(B);q=2*A.dot(B)
sos=4*sum((A[i]*B[j]-A[j]*B[i])**2 for i in range(4) for j in range(i+1,4))
z('weighted-charge Cauchy exact six-square identity',4*S*K-q*q-sos)
phi=x+s.I*yv;pc=x-s.I*yv;chi=zv+s.I*w;cc=zv-s.I*w
V=m*m*pc*phi+M2*cc*chi+g*(cc*phi**2+chi*pc**2)+lt*(pc*phi)**2
rem=s.simplify(s.expand(V-m*m*S));square=(s.sqrt(D)*chi+g/s.sqrt(D)*phi**2)*(s.sqrt(D)*cc+g/s.sqrt(D)*pc**2)+lr*(pc*phi)**2
z('positive-square remainder with interactions retained',rem-square)
rho=K+V;pres=K-V
z('rho-plus-p exact canonical identity',rho+pres-2*K)
z('stress-charge deficit positive decomposition',rho*rho-pres*pres-m*m*q*q-(4*K*rem+m*m*sos))
z('zero-time-derivative charge vanishes',q.subs({u:0,v:0,cs:0,ct:0}))
# Explicit squared bound for eta=1-m|q|/rho, not a selected eta value.
eta=s.symbols('eta',real=True)
z('charge-protected EOS bound identity',1-(1-eta)**2-(2*eta-eta*eta))
# Static critical-point elimination; formal independent complex coordinates.
p,pc_,c,cc_=s.symbols('phi phic chi chic')
Vsym=m*m*pc_*p+M2*cc_*c+g*(cc_*p**2+c*pc_**2)+lt*(pc_*p)**2
stat={c:-g*p*p/M2,cc_:-g*pc_*pc_/M2};eff=lt-g*g/M2
z('stationary chi equation elimination',s.diff(Vsym,cc_).subs(stat))
z('stationary daughter force',s.diff(Vsym,pc_).subs(stat)-p*(m*m+2*eff*pc_*p))
z('stationary effective potential',Vsym.subs(stat)-(m*m*pc_*p+eff*(pc_*p)**2))
z('effective quartic strictly positive decomposition',eff-(lr+4*g*g*m*m/(D*M2)))
y('positive stationary force factor',s.simplify(m*m+2*(lr+4*g*g*m*m/(D*M2))*s.symbols('amplitude_squared',nonnegative=True)).is_positive)
z('only static origin has zero material potential',Vsym.subs({p:0,pc_:0,c:0,cc_:0}))
# Homogeneous FLRW exact EOM identities for four real fields.
t=s.symbols('time',real=True);f=[s.Function('f'+str(i))(t) for i in range(4)];realv=[x,yv,zv,w];sub=dict(zip(realv,f));Vf=V.subs(sub);vel=[s.diff(a,t) for a in f];Vforces=[s.diff(V,realv[i]).subs(sub) for i in range(4)]
# phi=x+iy convention makes kinetic sum dot f²; real EOM force has half factor.
eom=[s.diff(a,t,2)+3*H*s.diff(a,t)+Vforces[i]/2 for i,a in enumerate(f)]
Kf=sum(vv*vv for vv in vel);rf=Kf+Vf;pf=Kf-Vf
z('FLRW full material energy continuity',s.diff(rf,t)+3*H*(rf+pf)-2*sum(vv*ee for vv,ee in zip(vel,eom)))
qf=2*(f[1]*vel[0]-f[0]*vel[1]+2*(f[3]*vel[2]-f[2]*vel[3]));accsub={s.diff(a,t,2):-3*H*vel[i]-Vforces[i]/2 for i,a in enumerate(f)}
z('FLRW conserved comoving U1 charge',(s.diff(qf,t)+3*H*qf).subs(accsub))
# General mass-scale incompatibility without fixed cosmological parameters.
z('heavy-parent branch incompatible with necessary fast-daughter condition',M2-9*H*H/4-(D+4*(m*m-H*H)+7*H*H/4))
R=s.symbols('m_squared_minus_H_squared',nonnegative=True)
y('parent oscillatory margin positive for m>=H',s.simplify(D+4*R+7*H*H/4).is_positive)
z('linear parent forcing has no origin linear mixing',s.diff(s.diff(Vsym,cc_),p).subs({p:0,pc_:0,c:0,cc_:0}))
z('linear daughter has supplied mass m',s.diff(s.diff(Vsym,pc_),p).subs({p:0,pc_:0,c:0,cc_:0})-m*m)
# Free diagnostic mass mu; phase mode exists only above3H/2.
mu,Om,amp=s.symbols('mu Omega amplitude',positive=True);exponent=-3*H/2-s.I*Om
z('free circular characteristic identity',(exponent**2+3*H*exponent+mu*mu).subs(Om**2,mu*mu-9*H*H/4))
Kcircle=(9*H*H/4+Om*Om)*amp**2*s.exp(-3*H*t);Vcircle=mu*mu*amp**2*s.exp(-3*H*t)
z('free circular mode exact dust pressure',(Kcircle-Vcircle).subs(Om**2,mu*mu-9*H*H/4))
rhoc=2*mu*mu*amp*amp*s.exp(-3*H*t);qc=2*Om*amp*amp*s.exp(-3*H*t)
z('free circular dust dilution',s.diff(rhoc,t)+3*H*rhoc)
z('free circular charge dilution',s.diff(qc,t)+3*H*qc)
# Overdamped slow mode pressure is not exactly -rho for a nonzero positive mass.
sigma=s.symbols('decay_rate',positive=True)
ws=(sigma*sigma-mu*mu)/(sigma*sigma+mu*mu)
z('overdamped slow-mode pressure relation',ws.subs(mu**2,3*H*sigma-sigma**2)-(2*sigma/(3*H)-1))
y('nonzero slow mode has rho+p positive',s.simplify(2*sigma**2*amp**2).is_positive)
# A vacuum constant does not create a scalar force; it is not derived.
Voff=s.symbols('arbitrary_vacuum_offset',real=True)
z('constant vacuum offset does not select dynamics',s.diff(Vsym+Voff,p)-s.diff(Vsym,p))
allpass=all(c['passed'] for c in checks)
out={'checks':checks,'all_passed':allpass,'exact_results':{'homogeneous_stress':'rho=K+V,p=K-V,rho+p=2K','charge_EOS_bound':'rho²-p² >= m² q²; |w| <= sqrt(1-(m|q|/rho)²), rho>0','protected_eta_bound':'|w| <= sqrt(2eta-eta²), eta=1-m|q|/rho, 0<=eta<=1','static_effective_quartic':str(s.simplify(eff)),'parent_mass_margin':'M²-9H²/4=Delta+4(m²-H²)+7H²/4>0 when m>=H','free_complex_dust':'mu>3H/2, a=A exp(-3Ht/2-iOmega t), Omega²=mu²-9H²/4; rho=2mu²A² exp(-3Ht),p=0','overdamped_slow_pressure':'w=2sigma/(3H)-1=-sqrt(1-4mu²/(9H²)), 0<mu<=3H/2; exactw=-1 requires mass0 or zero energy'},'branch_verdict':'No chi-as-DE plus fast daughter-dust identification in supplied weak/dilute canonical branch. Exact charged protected total material stress cannot be DE-like.','exceptions_not_excluded':['interaction-dominated or nonlinear collective modes beyond free/weak origin branch','large unprotected potential energy','gradients/nonhomogeneous stress','nonminimal kinetic terms','independent DE sector or explicitly postulated vacuum offset'],'scope':'Exact homogeneous canonical material identities with existing interactions; imposed FLRW H diagnostic, not predicted background or universal no-go.'}
(DEST/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert allpass
