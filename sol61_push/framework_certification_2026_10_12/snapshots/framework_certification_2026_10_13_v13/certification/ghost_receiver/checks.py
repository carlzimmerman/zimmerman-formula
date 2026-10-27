from pathlib import Path
import sympy as s,json,sys
DEST=Path(sys.argv[1]);checks=[]
def z(n,e):
 r=s.simplify(s.expand(e));checks.append({'name':n,'passed':r==0,'residual':str(r)})
def y(n,c):checks.append({'name':n,'passed':bool(c),'condition':str(c)})
a,X0,r0,d=s.symbols('a X0 rho0 d',positive=True);X=s.symbols('X',positive=True);P=-r0+a*(X-X0)**2/2;PX=s.diff(P,X);PXX=s.diff(P,X,2);rho=2*X*PX-P;K=PX+2*X*PXX;cs=PX/K
rd=s.simplify(rho.subs(X,X0+d));pd=P.subs(X,X0+d);Kd=K.subs(X,X0+d);csd=cs.subs(X,X0+d)
z('exact nonlinear receiver rho',rd-r0-2*a*X0*d-3*a*d*d/2)
z('exact nonlinear receiver pressure',pd+r0-a*d*d/2)
z('actual kinetic Legendre coefficient',Kd-a*(2*X0+3*d))
y('healthybuffer kinetic positive',Kd.is_positive);y('healthybuffer gradient positive',(a*d).is_positive)
z('sound speed exact',csd-d/(2*X0+3*d));y('sound positive',csd.is_positive);y('sound below one third',s.simplify(s.Rational(1,3)-csd).is_positive)
z('exact GC density',rho.subs(X,X0)-r0);z('exact GC w minus1',(P/rho).subs(X,X0)+1)
z('finite depositEOS',s.simplify((pd+r0)/(rd-r0))-d/(4*X0+3*d))
z('pressureless leading deposit only',s.diff(pd+r0,d).subs(d,0));y('finite positive deposit has pressure',(pd+r0).is_positive)
# Positive phase velocity Legendre map on healthybranch, pi>=0.
mu=s.sqrt(2*(X0+d));pi=a*d*mu
z('Legendre map derivative',s.diff(pi,d)-Kd/mu)
z('Hamiltonian derivative equals actual phase velocity',s.diff(rd,d)/s.diff(pi,d)-mu)
z('Hamiltonian curvature',s.diff(mu,d)/s.diff(pi,d)-1/Kd)
z('nonstall GC Hamiltonian derivative',mu.subs(d,0)-s.sqrt(2*X0))
# capacities and exact receiving/exporting snapshots, without inventing a rate.
di,alpha=s.symbols('d_initial alpha',positive=True);R=lambda u:r0+2*a*X0*u+3*a*u*u/2
C=R(di)-r0;z('exact export capacity',C-a*di*(2*X0+3*di/2));y('positivepreparedbuffer capacity',C.is_positive)
sf=s.symbols('withdrawal_fraction',real=True)
z('remaining branch after finite withdrawal energy',R(di)-R(sf*di)-a*(1-sf)*di*(2*X0+3*(1+sf)*di/2))
z('receiving energy change from positivebuffer',R((1+alpha)*di)-R(di)-a*alpha*di*(2*X0+3*(2+alpha)*di/2));y('positive absorption increment',s.simplify(R((1+alpha)*di)-R(di)).is_positive)
E=s.symbols('buffer_energy',nonnegative=True);inverse=(-2*X0+s.sqrt(4*X0*X0+6*E/a))/3
z('exact inversion energy to healthybranch',s.simplify(R(inverse)-r0-E))
# Formal DE tolerance and admissible window: do not choose rho0,a,X0.
eps=s.symbols('epsilon',positive=True);wplus=s.simplify((rd+pd)/rd)
z('DE window exact polynomial inequality',rd*(wplus-eps)-(a*((2-2*eps)*X0*d+(2-3*eps/2)*d*d)-eps*r0))
A=a*(2-3*eps/2);B=a*(2-2*eps)*X0;root=(-B+s.sqrt(B*B+4*A*eps*r0))/(2*A)
z('positive DE ceiling root solves constraint',s.simplify(A*root*root+B*root-eps*r0))
z('receiving and exporting headroom sum', (R(root)-R(di))+(R(di)-r0)-(R(root)-r0))
# Principal perturbation from actual P(X), not an added kinetic term.
lam,vt,gx=s.symbols('small_lambda perturbation_time perturbation_space',real=True)
Xpert=(mu+lam*vt)**2/2-lam**2*gx**2/2
quad=s.diff(P.subs(X,Xpert),lam,2).subs(lam,0)/2
z('actual quadratic kinetic and gradient action',quad-(Kd*vt*vt-a*d*gx*gx)/2)
# Plane acoustic energy flux: exactlinear identity in localrestframe.
vv,omega,kp=s.symbols('velocity amplitude_frequency wavenumber',real=True)
z('acoustic dispersion principal speed',Kd*(csd*kp*kp)-a*d*kp*kp)
# Moving uniform state theta=mu gamma(t-vx), Xfixed; boost not a new field.
v=s.symbols('boost_velocity',real=True);Lor=s.symbols('gammaLor',positive=True);td=mu*Lor;tx=-mu*Lor*v
z('movingtimelike X preserved under boost',((td*td-tx*tx)/2-(X0+d)).subs(Lor**2,1/(1-v*v)))
flux=-a*d*td*tx
z('actual movingbuffer energy flux',flux-(rd+pd)*Lor*Lor*v)
z('GCoffset alone has no transport flux',flux.subs(d,0))
z('movingcurrent energy relation',flux-td*(-a*d*tx))
# Current divergence/stress source relation from existing shiftkinetic action.
t,x=s.symbols('time position',real=True);th=s.Function('theta')(t,x);TX=(s.diff(th,t)**2-s.diff(th,x)**2)/2;Pt=P.subs(X,TX);px=a*(TX-X0)
jt=px*s.diff(th,t);jx=-px*s.diff(th,x);source=s.diff(jt,t)+s.diff(jx,x)
T00=px*s.diff(th,t)**2-Pt;T01=-px*s.diff(th,t)*s.diff(th,x);T11=px*s.diff(th,x)**2+Pt
z('actual local stress energy sourceidentity',s.diff(T00,t)+s.diff(T01,x)-source*s.diff(th,t))
z('actual local momentum reciprocal sourceidentity',s.diff(T01,t)+s.diff(T11,x)+source*s.diff(th,x))
# At sourcezero these are true conservation laws, not a new cooling interaction.
out={'checks':checks,'all_passed':all(c['passed'] for c in checks),'exact_formulas':{'rho':str(rd),'p':str(pd),'K':str(Kd),'cs2':str(csd),'depositEOS':'d/(4X0+3d), finitepressure O(d²)','exportcapacity':'a(2X0 di+1.5di²), di>0; cannotexportbelowrho0 whilehealthy','DEconstraint':'a[(2−2epsilon)X0d+(2−1.5epsilon)d²]<=epsilon rho0,0<epsilon<1','Hamiltonian':'Hprime(pi)=sqrt2X,Hsecond=1/K; healthypositivephasebranchpi>=0','flow':'T0i=−PX thetadot gradtheta; actualstressdiv=source*d^nu theta','quantum_extra':'none needed for these classical identities'},'scope':'Actual existing P(X), finite preparedhealthybuffer capacities and localprincipal flux, notcoldcoupling/Markov/microscopicselector orUVcausality certificate.'}
(DEST/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_passed']
