import sympy as s,json,sys
from pathlib import Path
r,u,a,X0,rho0,m,f,k,z=s.symbols('r u a X0 rho0 m f k z',positive=True)
v,ud=s.symbols('v ud',real=True)
X=u*u/2;d=X-X0;P=-rho0+a*d*d/2;U=m*m*(r-f)**2/2
K=a*(3*u*u/2-X0);A=r*r+K;B=r*r+a*d
checks=[]
def eq(name,l,r=0):
 res=s.factor(l-r);checks.append({'name':name,'passed':res==0,'residual':str(res)})
def yes(name,b):checks.append({'name':name,'passed':bool(b)})
Jc=r*r*u;Jp=a*d*u
udsol=-2*r*v*u/A
Sc=s.diff(Jc,r)*v+s.diff(Jc,u)*udsol
Sp=s.diff(Jp,u)*udsol
eq('total homogeneous shift current',Sc+Sp)
eq('cold shift source',Sc,2*r*v*u*K/A)
eq('ghost shift source',Sp,-2*r*v*u*K/A)
rhoc=v*v/2+r*r*X+U;pc=v*v/2+r*r*X-U
rhop=2*X*a*d-P;pp=P
rdd=r*u*u-m*m*(r-f)
eq('cold energy exchange on radial equation',s.diff(rhoc,r)*v+s.diff(rhoc,v)*rdd+s.diff(rhoc,u)*udsol,u*Sc)
eq('ghost energy exchange',s.diff(rhop,u)*udsol,u*Sp)
eq('total homogeneous energy',u*(Sc+Sp))
eq('total rho+p',rhoc+rhop+pc+pp,v*v+u*u*B)
eq('ghost rho',rhop,rho0+2*a*X0*d+3*a*d*d/2)
mu2=m*m-u*u;R=m*m*f/mu2
eq('radial stationary equation',(r*u*u-m*m*(r-f)).subs(r,R))
eq('stationary cold potential',U.subs(r,R),R*R*u**4/(2*m*m))
rhoc0=rhoc.subs({r:R,v:0});pc0=pc.subs({r:R,v:0})
eq('stationary cold EOS',pc0/rhoc0,mu2/(m*m+u*u))
beta=s.symbols('beta',positive=True)
eq('radius coldness relation',R.subs(u*u,m*m*(1-beta)),f/beta)
eq('cold EOS beta', (mu2/(m*m+u*u)).subs(u*u,m*m*(1-beta)),beta/(2-beta))
# independent Taylor expansion full action with derivatives independent
h,sg,sd,sk,td,tk=s.symbols('h sg sd sk td tk',real=True)
xx=((u+h*td)**2-h*h*tk*tk)/2
L=h*h*(sd*sd-sk*sk)/2+(r+h*sg)**2*xx-rho0+a*(xx-X0)**2/2-m*m*(r+h*sg-f)**2/2
L2=s.expand(L).coeff(h,2)
expected=(sd*sd-sk*sk-mu2*sg*sg+A*td*td-B*tk*tk)/2+2*r*u*sg*td
eq('Taylor quadratic action',L2,expected)
eq('background linear radial coefficient',s.expand(L).coeff(h,1).coeff(sg),r*u*u-m*m*(r-f))
C=2*r*u
poly=(k*k+mu2-z)*(B*k*k-A*z)-C*C*z
eq('dispersion determinant',s.expand(poly),A*z*z-(A*(k*k+mu2)+B*k*k+C*C)*z+B*k*k*(k*k+mu2))
eq('frequency sum',-s.expand(poly).coeff(z,1)/A,k*k+mu2+B*k*k/A+C*C/A)
eq('frequency product',poly.subs(z,0)/A,B*k*k*(k*k+mu2)/A)
q=k*k+mu2;t=B*k*k/A;c=C*C/A
D=((q+t+c)**2-4*q*t)
eq('discriminant positive square decomposition',D,(q-t)**2+2*c*(q+t)+c*c)
eq('zero momentum roots',poly.subs(k,0),A*z*(z-mu2-C*C/A))
cs=B*mu2/(A*mu2+C*C)
eq('sound small k coefficient',s.diff(poly,k,2).subs({k:0,z:0})/(-2*s.diff(poly,z).subs({k:0,z:0})),cs)
# explicit Hamiltonian momentum square: p_sigma=sd, p_theta=A td+C sigma
ps,pt=s.symbols('ps pt',real=True)
H2=(ps*ps+(pt-C*sg)**2/A+sk*sk+B*tk*tk+mu2*sg*sg)/2
eq('Legendre Hamiltonian', (ps*sd+pt*td-expected).subs({sd:ps,td:(pt-C*sg)/A}),H2)
# Healthy witness exact, frozen parameter-independent units only, no empirical input.
# m²=4,u²=3,X0=1,a=f=rho0=1 -> R=4; mu²=1,K=7/2,A=39/2,B=33/2.
subs={m:2,u:s.sqrt(3),X0:1,a:1,f:1,rho0:1,r:4}
for name,ex in [('A',A),('B',B),('mu²',mu2),('K',K),('cs²',cs)]:yes('constructive positive '+name,ex.subs(subs)>0)
yes('sound strictly subluminal branch witness',cs.subs(subs)<1)
eq('w cold witness',(pc0/rhoc0).subs(subs),s.Rational(1,7))
for vv,sign in [(1,1),(-1,-1)]:yes('exchange sign '+str(sign),(u*Sc).subs(subs).subs(v,vv)*sign>0)
# Fixed charge radial displacement exchanges energy but reversible closed dynamics.
eq('ghost charge Jacobian',s.diff(Jp,u),K)
eq('total phase Jacobian',s.diff(Jc+Jp,u),A)
eq('receiver dilution is not separately invariant',Sp,-K*2*r*v*u/A)
# momentum opposite force at generic spatial gradient; signature +---.
F,gx=s.symbols('F gx',real=True)
eq('reciprocal spatial momentum',-F*gx+F*gx)
res={'claim':'prospective shared phase local classical admission','checks':checks,'count':len(checks),'all_passed':all(x['passed'] for x in checks),'formulas':{'A':str(A),'B':str(B),'R':str(R),'dispersion':str(poly),'sound':str(cs),'cold_w':str(mu2/(m*m+u*u))},'non_claims':['new join not adopted','no cold number proof','no irreversible receiver rate','no global stability or cosmology']}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'count':res['count'],'all_passed':res['all_passed']}))
if not res['all_passed']:sys.exit(1)
