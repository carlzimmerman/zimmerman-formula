"""Static phase/metric consistency, not a selected gravity theory."""
from pathlib import Path
import json,math
import sympy as s

HERE=Path(__file__).resolve().parent
checks=[]
def z(name,value):
    residue=s.simplify(value);assert residue==0,(name,str(residue))
    checks.append({'name':name,'passed':True})
def yes(name,value):
    assert value,name
    checks.append({'name':name,'passed':True})

a,X0,rho0,N,A,r,omega,psi=s.symbols('a X0 rho0 N A r omega psi_prime',positive=True)
X=s.symbols('X',positive=True);d=s.symbols('d',real=True)
P=-rho0+a*(X-X0)**2/2;PX=s.diff(P,X);rho=2*X*PX-P
z('actual C2 excess density',rho.subs(X,X0+d)-rho0-2*a*X0*d-3*a*d*d/2)
z('actual C2 excess pressure',P.subs(X,X0+d)+rho0-a*d*d/2)
K=s.limit((P.subs(X,X0+d)+rho0)/(rho.subs(X,X0+d)-rho0)**2,d,0)
z('leading polytropic coefficient',K-1/(8*a*X0**2))
z('charged hydrostatic enthalpy derivative',s.diff(P,X)/(rho+P)-1/(2*X))

properX=(omega*omega/(N*N)-psi*psi/(A*A))/2
L=N*A*r*r*P.subs(X,properX)
z('actual stationary phase radial canonical flux',s.diff(L,psi)+N*r*r*a*(properX-X0)*psi/A)
z('actual slice charge measure',s.diff(L,omega)-A*r*r*a*(properX-X0)*omega/N)
yes('missing proper volume factor mutation detected',
    s.simplify(s.diff(L,omega)-r*r*a*(properX-X0)*omega/N)!=0)
u0=s.sqrt(2*X0)
mu=s.symbols('mu',positive=True)
lapse=1-mu/r
delta=X0*(1/lapse**2-1)
excess=2*a*X0*delta+3*a*delta**2/2
slicecharge=a*delta*u0/lapse
z('charged rest-clock tail delta coefficient',s.limit(r*delta,r,s.oo)-2*X0*mu)
z('charged rest-clock tail density coefficient',s.limit(r*excess,r,s.oo)-4*a*X0**2*mu)
coefficient=2*a*X0*u0*mu
z('charged rest-clock tail slice charge coefficient',s.limit(r*slicecharge,r,s.oo)-coefficient)
z('integrated quadratic charge coefficient',2*s.pi*coefficient-4*s.pi*a*X0*u0*mu)
wrongdelta=X0*(lapse*lapse-1)
yes('wrong redshift mutation reverses tail health',s.simplify(s.limit(r*wrongdelta,r,s.oo)+2*X0*mu)==0)

# Vacuum phase gradient is allowed even though its shift current is zero.
vacgrad2=A*A*(omega*omega/(N*N)-2*X0)
z('vacuum phase gradient leaves X at X0',properX.subs(psi*psi,vacgrad2)-X0)
z('vacuum phase gradient has no shift charge',a*(properX.subs(psi*psi,vacgrad2)-X0)*omega/N)
z('vacuum phase gradient has no radial charge flux',
  (-N*r*r*a*(properX-X0)*psi/A).subs(psi*psi,vacgrad2))
yes('vacuum radial gradient need not imply charge flow',vacgrad2.subs({N:s.Rational(1,2),A:1,omega:u0})>0)
yes('finite zero charge does not fix clock frequency without rest-clock premise',
    vacgrad2.subs({N:1,A:1,omega:2*u0})>0)
yes('deleted PX source factor mutation detected',(-psi/A**2).subs({psi:s.sqrt(6),A:1})!=0)

# Compact-edge frequency and exterior upper bound.
edgeN=s.symbols('N_edge',positive=True)
upper=s.simplify(properX.subs({omega:u0*edgeN,psi:0})-X0)
z('compact boundary redshift condition',upper.subs(N,edgeN))
yes('compact exterior already unhealthy at zero radial gradient',
    upper.subs({edgeN:s.Rational(9,10),N:1})<0)
yes('real radial gradient only reduces X',s.diff(properX,psi)<0)

# Leading n=1 fluid construction, with all approximation boundaries explicit.
k,G,rhoc=s.symbols('k G rho_c',positive=True)
profile=rhoc*s.sin(k*r)/(k*r)
z('leading Newtonian radial fluid equation',s.diff(profile,r,2)+2*s.diff(profile,r)/r+k*k*profile)
mass=s.simplify(4*s.pi*s.integrate(profile*r*r,(r,0,s.pi/k)))
z('leading compact fluid mass',mass-4*s.pi**2*rhoc/k**3)
z('leading surface potential relation',s.simplify(G*mass/(s.pi/k)).subs(k*k,2*s.pi*G/K)-2*K*rhoc)
hc,y=s.symbols('h_c radius_over_edge',positive=True)
inside=-hc*(1+s.sin(s.pi*y)/(s.pi*y));outside=-hc/y
phase_inside=X0*(s.exp(2*(-hc-inside))-1)
phase_outside=X0*(s.exp(2*(-hc-outside))-1)
z('illustrative compact phase meets X0 at boundary',phase_outside.subs(y,1))
z('compact exterior sign exponent identity',phase_outside.subs(y,2)-X0*(s.exp(-hc)-1))
yes('illustrative compact phase outside crosses healthy branch by monotonic exp',s.simplify((2*(-hc-outside)).subs(y,2)).is_negative)

tails=[]
for radius in [10,100,1000]:
    vals={a:1,X0:1,mu:1,r:radius}
    tails.append({'r':radius,'r_times_excess_over_limit':float((r*excess/(4*a*X0**2*mu)).subs(vals)),
                  'r_times_slicecharge_over_limit':float((r*slicecharge/coefficient).subs(vals))})
edge=[]
for radius in [.5,1,2,10]:
    formula=phase_inside if radius<1 else phase_outside
    edge.append({'r_over_edge':radius,'d_over_X0':float((formula/X0).subs({hc:.001,y:radius}))})
yes('radial phase diagnostics have declared interior/edge/exterior signs',
    edge[0]['d_over_X0']>0 and abs(edge[1]['d_over_X0'])<1e-12 and all(x['d_over_X0']<0 for x in edge[2:]))
result={'checks':checks,'passed':len(checks),'failures':0,'tail_diagnostics':tails,'compact_phase_diagnostics':edge,
        'premises':['No S_g selected','N,A positive; asymptotically A->1 required for charge integral','Tail is an eventually charged rest-clock branch, not every zero-charge-flux state','Compact-edge N_edge<1 is an explicit Newtonian-well premise','Vacuum background absent/subtracted in asymptotically flat diagnostic','Smooth P-only phase; no extra interaction/current/wall'],
        'non_claims':['No universal gravity/C2 exclusion','No full nonlinear fluid/metric solution','No cosmological boundary or halo selector','No claim zero charge flux implies zero phase gradient']}
(HERE/'run_v2/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
