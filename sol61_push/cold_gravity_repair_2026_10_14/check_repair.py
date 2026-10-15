import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,x):
 assert s.simplify(x)==0,(name,s.simplify(x))
 checks.append(name)
def pos(name,x):
 assert x>0,(name,x)
 checks.append(name)
# Independent EH bulk action, matching scalar ADM up to boundary terms.
t,z=s.symbols('t z',real=True);x,y=s.symbols('x y');coords=(t,x,y,z)
al=s.Function('alpha')(t,z);ns=s.Function('N')(t,z);ze=s.Function('zeta')(t,z);ee=s.Function('e')(t,z)
hh=s.Matrix([[-2*al,0,0,ns],[0,2*ze,0,0],[0,0,2*ze,0],[ns,0,0,2*(ze+ee)]])
eta=s.diag(-1,1,1,1)
Ga=[[[sum(eta[a,d]*(s.diff(hh[d,c],coords[b])+s.diff(hh[d,b],coords[c])-s.diff(hh[b,c],coords[d])) for d in range(4))/2 for c in range(4)] for b in range(4)] for a in range(4)]
eh=s.expand(sum(eta[m,n]*sum(Ga[a][m][b]*Ga[b][n][a]-Ga[a][m][n]*Ga[b][a][b] for a in range(4) for b in range(4)) for m in range(4) for n in range(4))/2)
adm=-3*s.diff(ze,t)**2-2*s.diff(ze,t)*s.diff(ee,t)+2*s.diff(ze,t)*s.diff(ns,z)+s.diff(ze,z)**2+2*s.diff(al,z)*s.diff(ze,z)
for f in (al,ns,ze,ee):
 dd=s.expand(eh-adm)
 zero('independent EH Euler '+str(f),s.diff(dd,f)-s.diff(s.diff(dd,s.diff(f,t)),t)-s.diff(s.diff(dd,s.diff(f,z)),z))
q,r,C,L,mu,A=s.symbols('q r C L mu A',positive=True)
Z,E,zd,ed,alpha,b=s.symbols('Z E zd ed alpha b',real=True)
# a_i a^i term is +(Aq/2)alpha² in dimensionless Lagrangian.
lag=-3*zd**2-2*zd*ed+2*zd*b+q*Z**2+2*q*alpha*Z+r*(3*zd+ed-b)**2/2+(r*C+A*q)*alpha**2/2+r*L*b*b/(2*q)-r*mu*(3*Z*Z+2*Z*E+E*E)
asol=s.solve(s.diff(lag,alpha),alpha)[0];bsol=s.solve(s.diff(lag,b),b)[0]
zero('lapse solution',asol+2*q*Z/(r*C+A*q))
zero('shift solution',bsol-q*((3*r-2)*zd+r*ed)/(r*(q+L)))
red=s.factor(lag.subs({alpha:asol,b:bsol}))
K=s.hessian(red,(zd,ed)).applyfunc(s.factor);G=(-s.hessian(red,(Z,E))).applyfunc(s.factor)
zero('kinetic determinant',K.det()-L*(6*r-4)/(q+L))
zero('kinetic ee',K[1,1]-r*L/(q+L))
zero('potential determinant',G.det()-4*r*mu*(2*q*q/(r*C+A*q)-q+2*r*mu))
# Exact repair, with all scalar modes diagonal in Z,Y=Z+E.
pars={r:1,C:4,L:100,mu:2,A:s.Rational(3,2)}
Y,yd=s.symbols('Y yd',real=True)
newred=s.factor(red.subs(pars).subs({E:Y-Z,ed:yd-zd}))
f=s.factor(4-q+2*q*q/(4+s.Rational(3,2)*q))
expect=zd**2+50*yd**2/(q+100)-f*Z**2-2*Y**2
zero('diagonal full scalar action',newred-expect)
zero('positive frequency decomposition',f-(q/3+s.Rational(4,9)+s.Rational(256,9)/(3*q+8)))
zero('scalar minimum square identity',f-s.Rational(28,9)-(3*q-8)**2/(9*(3*q+8)))
# derivative changes sign exactly at8/3; |vg|²=q f'²/f.
fp=s.factor(s.diff(f,q));speed2=s.factor(q*fp*fp/f)
zero('frequency derivative',fp-(s.Rational(1,3)-s.Rational(256,3)/(3*q+8)**2))
# On0<q<=8/3: -1<=f'<=0 and f>=28/9 so speed²<=6/7.
# Onq>=8/3:0<=f'<1/3 and f>q/3 so speed²<1/3.
zero('derivative at zero',fp.subs(q,0)+1)
zero('derivative at turn',fp.subs(q,s.Rational(8,3)))
pos('monotonic frequency derivative',s.diff(fp,q))
# Vectors/tensors unchanged by scalar trace regulator and lapse gradient.
vd,sh,V=s.symbols('vd sh V',real=True)
lv=(vd-sh)**2/4+r*L*sh**2/(2*q)-r*mu*V**2/2
vv=s.solve(s.diff(lv,sh),sh)[0];vr=s.factor(lv.subs(sh,vv))
kv=s.factor(s.diff(vr,vd,2));fv=s.factor(-s.diff(vr,V,2)/kv)
zero('vector kinetic',kv-r*L/(q+2*r*L))
zero('vector frequency',fv-mu*q/L-2*r*mu)
ht,hd=s.symbols('ht hd',real=True);lt=hd**2/4-q*ht**2/4-r*mu*ht**2/2
zero('tensor frequency',-s.diff(lt,ht,2)/s.diff(lt,hd,2)-q-2*r*mu)
fy=q/25+4;fv=fv.subs(pars);ft=q+4
for name,ff,cc in [('material scalar',fy,s.Rational(1,25)),('vector',fv,s.Rational(1,50)),('tensor',ft,s.Integer(1))]:
 zero(name+' speed gap',cc-q*s.diff(ff,q)**2/ff-cc*4/ff)
# RouteA: sign/stiffness alone positive energy but highk velocity unbounded.
fA=s.factor((4-q+q*q/2))
zero('sign-only scalar frequency',f.subs({},simultaneous=True)*0+red.subs({r:1,C:4,L:100,mu:2,A:0}).subs({E:Y-Z,ed:yd-zd})-(zd**2+50*yd**2/(q+100)-fA*Z**2-2*Y**2))
zero('sign-only highq group-speed squared asymptotic',s.limit(q*s.diff(fA,q)**2/fA/q,q,s.oo)-2)
# RouteC: at fixedD, continuous r-to0 taper enters detK<0, irrespective A/C.
zero('taper kinetic degeneracy',K.det().subs(r,s.Rational(2,3)))
assert s.factor(K.det().subs(r,s.Rational(1,2)))<0
checks.append('fixedD taper counterexample r1/2 for allq')
rows=[]
for qq in [s.Rational(1,10**6),s.Rational(1,100),s.Rational(1,2),1,s.Rational(8,3),10,100,10000]:
 kp=K.subs(pars).subs(q,qq);gp=G.subs(pars).subs(q,qq)
 for name,value in [('K11',kp[0,0]),('detK',kp.det()),('G11',gp[0,0]),('detG',gp.det())]:pos(str(qq)+' '+name,value)
 vv2=speed2.subs(q,qq);assert 0<=vv2<s.Rational(6,7);checks.append(str(qq)+' scalar group')
 rows.append({'q':str(qq),'scalar_frequency2':[float(f.subs(q,qq)),float(fy.subs(q,qq))],'vector_frequency2':float(fv.subs(q,qq)),'tensor_frequency2':float(ft.subs(q,qq)),'clock_group_speed_c':float((s.sqrt(q)*fp/s.sqrt(f)).subs(q,qq))})
# Zero-background differences have zero first variation, including derivative terms.
eps,c0,c1=s.symbols('eps c0 c1');term=(eps*c0+eps**2*c1)**2
zero('quadratic difference background',term.subs(eps,0));zero('quadratic difference first variation',s.diff(term,eps).subs(eps,0))
result={'claim':'CGR-001','checks_passed':len(checks),'candidate':{'Q_regulator_sign':'+','r':1,'Kc':4,'L':100,'mu':2,'A':'3/2'},'K':str(K),'G':str(G),'detK':str(s.factor(K.det())),'diagonal_scalar_action':str(expect),'clock_frequency2':str(f),'material_scalar_frequency2':str(fy),'vector_frequency2':str(fv),'tensor_frequency2':str(ft),'uniform_clock_group_speed_squared_upper':'6/7 (conservative analytic bound)','all_q_quadratic_energy':'positive for q>0 in homogeneous exterior','routeA':'positive energy but highq group speed grows without bound','routeC':'fixedD smooth r-to0 taper crosses detK=0 at2/3 and negative kinetic for0<r<2/3','samples':rows,'limits':'No wall, nonlinear, UV/front causality, observability or engine certificate. Elliptic lapse equation requires boundary conditions.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
