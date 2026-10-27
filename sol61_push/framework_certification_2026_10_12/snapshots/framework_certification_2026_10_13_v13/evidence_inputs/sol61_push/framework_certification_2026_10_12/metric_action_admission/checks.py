import sympy as s,json,sys
from pathlib import Path
G,b,tau,zeta,kr=s.symbols('G b tau zeta kr',positive=True)
gamma,Ph,Psi,h,rho=s.symbols('gamma Ph Psi h rho',real=True)
checks=[]
def eq(n,e):
 e=s.factor(e);checks.append({'name':n,'passed':e==0,'residual':str(e)})
# Actual metric null-index n=sqrt(spatiallapse/temporallapse).
n=s.sqrt((1-2*h*Psi)/(1+2*h*Ph))
eq('actual opticalindex first derivative',s.diff(n,h).subs(h,0)+Ph+Psi)
eq('coordinate nullspeed inverseindex',s.diff(1/n,h).subs(h,0)-Ph-Psi)
eq('metric branch lens factor',s.diff(n,h).subs(h,0).subs(Psi,gamma*Ph)+(1+gamma)*Ph)
for gam in [0,1,-1]:eq('explicit opticalfactor '+str(gam),(1+gamma).subs(gamma,gam)-(1+gam))
# Reduced action derivative variables (one gradientcomponent, sums generalize).
f,p,ft,pt,fx,px=s.symbols('f p ft pt fx px',real=True)
L=-fx*fx/(8*s.pi*G)-b*(px-gamma*fx)**2/2+tau*ft*ft/2+zeta*(pt-gamma*ft)**2/2-rho*f
# Euler derivative dL/dfield - partialtime dL/dft - partialx dL/dfx.
ftt,ptt,fxx,pxx=s.symbols('ftt ptt fxx pxx',real=True)
def El(field,vel,grad):
 return s.diff(L,field)-s.diff(L,vel,ft)*ftt-s.diff(L,vel,pt)*ptt-s.diff(L,grad,fx)*fxx-s.diff(L,grad,px)*pxx
Ef=El(f,ft,fx);Ep=El(p,pt,px)
Rtt=ptt-gamma*ftt;Rxx=pxx-gamma*fxx
eq('actual reduced Psi variation',Ep-b*Rxx+zeta*Rtt)
eq('actual reduced Phi variation',Ef-(fxx/(4*s.pi*G)-tau*ftt-gamma*b*Rxx+gamma*zeta*Rtt-rho))
eq('reduced independentPhi equation',Ef+gamma*Ep-(fxx/(4*s.pi*G)-tau*ftt-rho))
eq('static Poisson with harmonicR',Ef.subs({ftt:0,ptt:0,pxx:gamma*fxx})-(fxx/(4*s.pi*G)-rho))
eq('static Psi equation harmonicR',Ep.subs({ftt:0,ptt:0,pxx:gamma*fxx}))
# Actual Legendre transform positivity and independence of gamma when R coordinate used.
Pf,Pp=s.symbols('Pf Pp',real=True)
K=s.hessian(L,(ft,pt));eq('kineticmatrix determinant',K.det()-tau*zeta)
eq('kinetic cross coefficient',K[0,1]+gamma*zeta)
rf,rt,rx=s.symbols('rf rt rx',real=True)
eq('Rcoordinate diagonal kinetic',L.subs({p:rf+gamma*f,pt:rt+gamma*ft,px:rx+gamma*fx})-(-fx*fx/(8*s.pi*G)-b*rx*rx/2+tau*ft*ft/2+zeta*rt*rt/2-rho*f))
# Fourierfree reduced operator det, two uncoupled speeds, staticinvariant.
omega=s.symbols('omega',real=True)
M=s.Matrix([[kr*kr/(4*s.pi*G)-tau*omega*omega+gamma*gamma*(b*kr*kr-zeta*omega*omega),-gamma*(b*kr*kr-zeta*omega*omega)],[-gamma*(b*kr*kr-zeta*omega*omega),b*kr*kr-zeta*omega*omega]])
eq('Fourier operator determinant',(M.det()-(kr*kr/(4*s.pi*G)-tau*omega*omega)*(b*kr*kr-zeta*omega*omega)))
eq('Phi propagation speed', (kr*kr/(4*s.pi*G)-tau*omega*omega).subs(omega*omega,kr*kr/(4*s.pi*G*tau)))
eq('R propagation speed',(b*kr*kr-zeta*omega*omega).subs(omega*omega,b*kr*kr/zeta))
eq('instantaneous operator choice',M.det().subs({tau:0,zeta:0})-b*kr**4/(4*s.pi*G))
eq('fixedc1Phi operator choice',(kr*kr/(4*s.pi*G)-tau*omega*omega).subs(tau,1/(4*s.pi*G))-(kr*kr-omega*omega)/(4*s.pi*G))
eq('fixedc1R operator choice',(b*kr*kr-zeta*omega*omega).subs(zeta,b)-b*(kr*kr-omega*omega))
# Cold slowworldline leadingweak potential independentPsi.
v2,m=s.symbols('v2 m',positive=True)
Lc=-m*s.sqrt(1+2*h*Ph-(1-2*h*Psi)*v2)
eq('cold leadingpotential independentPsi',s.diff(Lc,h).subs({h:0,v2:0})+m*Ph)
eq('sameNewtoniancold for allslips',s.diff(Lc,h).subs({h:0,v2:0,Psi:gamma*Ph})+m*Ph)
res={'claim':'bounded reduced metric action ambiguity','count':len(checks),'checks':checks,'all_passed':all(x['passed'] for x in checks),'interpretation':'A7/Poisson weakPhi insufficient to choose Psi/kineticoperators; reducedexamples not covariantframeworkactions','no_tensorGW_prediction':True}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'count':len(checks),'all_passed':res['all_passed']}));sys.exit(0 if res['all_passed'] else 1)
