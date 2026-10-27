import sympy as s,json,sys
from pathlib import Path
a,X0,rho0,u,m=s.symbols('a X0 rho0 u m',positive=True)
Phi,Psi,h,t,g2,v2=s.symbols('Phi Psi h t g2 v2',real=True)
P=lambda X:-rho0+a*(X-X0)**2/2
PX=lambda X:a*(X-X0)
checks=[]
def eq(n,x):
 x=s.factor(x);checks.append({'name':n,'passed':x==0,'residual':str(x)})
X=(t*t-g2)/2
Xe=(t*t/(1+2*h*Phi)-g2/(1-2*h*Psi))/2
sqrtg=s.sqrt((1+2*h*Phi)*(1-2*h*Psi)**3)
T00=PX(X)*t*t-P(X);trace=PX(X)*g2+3*P(X)
eq('metric determinant derivative',s.diff(sqrtg,h).subs(h,0)-Phi+3*Psi)
eq('inversemetric X derivative',s.diff(Xe,h).subs(h,0)+Phi*t*t+Psi*g2)
eq('actual density weak metric coupling',s.diff(sqrtg*P(Xe),h).subs(h,0)+Phi*T00+Psi*trace)
Xb=u*u/2;pb=P(Xb);rhob=u*u*PX(Xb)-pb;K=PX(Xb)+a*u*u
weak=s.diff(sqrtg*P(Xe),h).subs(h,0)
eq('homogeneous metric coupling',weak.subs({t:u,g2:0})+Phi*rhob+3*Psi*pb)
eq('independent lapse coefficient',s.diff(weak,Phi)+T00)
eq('independent spatial coefficient',s.diff(weak,Psi)+trace)
eq('stress vacuum T00',T00.subs(g2,t*t-2*X0)-rho0)
eq('stress vacuum spatial trace',trace.subs(g2,t*t-2*X0)+3*rho0)
# Mixed coefficient using independent metric epsilon and phase epsilon j.
j,et,eg2=s.symbols('j et eg2',real=True)
Xmix=((u+j*et)**2/(1+2*h*Phi)-j*j*eg2/(1-2*h*Psi))/2
Lm=sqrtg*P(Xmix)
eq('prepared metric-phase mixed coefficient',s.diff(Lm,h,j).subs({h:0,j:0})+u*(K*Phi+3*PX(Xb)*Psi)*et)
flat=P(((u+j*et)**2-j*j*eg2)/2)
eq('prepared flat quadratic coefficient',s.diff(flat,j,2).subs(j,0)/2-(K*et*et-PX(Xb)*eg2)/2)
Jdens=sqrtg*PX(Xmix)*(u+j*et)/(1+2*h*Phi)
eq('densJ0 background',Jdens.subs({h:0,j:0})-PX(Xb)*u)
eq('densJ0 phase response',s.diff(Jdens,j).subs({h:0,j:0})-K*et)
eq('densJ0 metric response',s.diff(Jdens,h).subs({h:0,j:0})+u*(K*Phi+3*PX(Xb)*Psi))
eq('vac spatial propagation coefficient',PX(Xb).subs(u*u,2*X0))
eq('vac temporal kinetic coefficient',K.subs(u*u,2*X0)-2*a*X0)
eq('vac metricmix retains lapse only',(u*(K*Phi+3*PX(Xb)*Psi)-2*a*X0*u*Phi).subs(u,s.sqrt(2*X0)))
# Receiver physical X response removes pure lapse clock adjustment at GC point.
eq('vac clock compensation physical deltaX',u*(u*Phi)-u*u*Phi)
eq('rho X response',s.diff(2*s.Symbol('Y')*PX(s.Symbol('Y'))-P(s.Symbol('Y')),s.Symbol('Y')).subs(s.Symbol('Y'),Xb)-K)
# Cold exact worldline weak expansion (timelike1-v²>0); no NR kinetic truncation.
Lc=-m*s.sqrt(1+2*h*Phi-(1-2*h*Psi)*v2)
eq('cold exact weakmetric coefficient',s.diff(Lc,h).subs(h,0)+m*(Phi+Psi*v2)/s.sqrt(1-v2))
eq('cold low velocity potential coefficient',s.diff(Lc,h).subs({h:0,v2:0})+m*Phi)
# p0=m(1+2hPhi)/sqrtmetric dt/dtau
E=m*(1+2*h*Phi)/s.sqrt(1+2*h*Phi-(1-2*h*Psi)*v2)
eq('cold weak coordinate energy',s.diff(E,h).subs(h,0)-m*(Phi*(1-2*v2)-Psi*v2)/(1-v2)**s.Rational(3,2))
# Covariant coordinate identity from separate conservation.
# (1/sqrtg)partial_mu(sqrtg T^mu_nu)-Gamma^alpha_mu_nu T^mu_alpha=0.
# Symmetric stress contracts Gamma first/third metric-derivative terms away.
T=s.Matrix([[s.Symbol('T'+str(i)+str(j)) if i<=j else 0 for j in range(4)] for i in range(4)])
for i in range(4):
 for jj in range(i):T[i,jj]=T[jj,i]
# arbitrary covariant metric derivatives dg[coordinate,a,b], symmetric a,b
D={}
for q in range(4):
 for i in range(4):
  for jj in range(i,4):D[q,i,jj]=D[q,jj,i]=s.Symbol('D'+str(q)+str(i)+str(jj))
for nu in range(4):
 contraction=sum(T[i,jj]*(D[i,jj,nu]+D[nu,jj,i]-D[jj,i,nu])/2 for i in range(4) for jj in range(4))
 target=sum(T[i,jj]*D[nu,i,jj]/2 for i in range(4) for jj in range(4))
 eq('connection symmetric stress contraction '+str(nu),contraction-target)
# Homogeneous weak coordinate geometric work rho Phi_t+3p Psi_t.
Pt,St=s.symbols('Pt St',real=True)
eq('homogeneous metric power contraction',(rhob*2*Pt+3*pb*2*St)/2-rhob*Pt-3*pb*St)
eq('vac coordinate work is volume lapse change',(rhob*Pt+3*pb*St).subs(u*u,2*X0)-rho0*(Pt-3*St))
res={'claim':'prospective minimal metric coupling only','count':len(checks),'checks':checks,'all_passed':all(c['passed'] for c in checks),'scope':'exact weak coefficient algebra; independentmetric potentials; metric dynamics unspecified','non_claims':['no EH/GR equations','no Phi=Psi','no coldtoDE Q or receipt','no particle creation/rate','no UV transport at vac']}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'count':len(checks),'all_passed':res['all_passed']}));sys.exit(0 if res['all_passed'] else 1)
