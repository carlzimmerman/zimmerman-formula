import json, sys
from pathlib import Path
import sympy as s

n,R,h,a,b,w,k=s.symbols('n R h a b w k',positive=True)
v,pd=s.symbols('v Pdot',real=True)
checks=[]
def check(name,condition,detail):
    checks.append(dict(name=name,passed=bool(condition),detail=str(detail)))
    if not condition: raise AssertionError(name)

# Expansion is at fixed Eulerian density, as required by conserved-current variables.
j,z=s.symbols('j z',real=True)
E=s.Function('E')
proper=s.sqrt(n*n-z*z*j*j)
expansion=s.diff(-E(proper),z,2).subs(z,0)/2
check('reference kinetic from covariant energy',s.simplify(expansion-j*j*s.diff(E(n),n)/(2*n))==0,expansion)
L=(n*v-pd)**2/(2*R)+h*v*v/2
H=s.hessian(L,(v,pd))
check('positive Hessian determinant',s.simplify(H.det()-h/R)==0,H)
vs=s.solve(s.diff(L,v),v)[0]
Leff=s.simplify(L.subs(v,vs))
check('reduced carrier inertia',s.simplify(Leff-h*pd*pd/(2*(n*n+R*h)))==0,Leff)
check('dust limit removes reduced carrier inertia',s.limit(Leff,h,0)==0,'Free reference velocity cancels current; not fixed-anchor inertia')

eta,xi=s.symbols('etadot xidot',real=True)
M=s.hessian(n*(eta+xi)**2/2+n*a*eta**2/2,(eta,xi))
check('displacement kinetic determinant',s.simplify(M.det()-n*n*a)==0,M)
V=n*n*s.diag(b*k*k,w)
dyn=s.simplify(M.inv()*V)
check('frozen nongravitating frequency trace',s.simplify(s.trace(dyn)-n*(b*k*k+(1+a)*w)/a)==0,s.trace(dyn))
check('frozen nongravitating frequency product',s.simplify(dyn.det()-n*n*b*k*k*w/a)==0,dyn.det())
# Positive M and V imply positive eigenfrequencies via congruence; no gravity imported.

x=s.symbols('x',real=True)
N=s.Function('N')(x); nn=s.Function('n')(x)
mu=1+s.diff(E(n),n)
gradmu=s.diff((N*mu.subs(n,nn)),x)
expected=s.diff(N,x)*(1+s.Subs(s.diff(E(n),n),n,nn))+N*s.Subs(s.diff(E(n),n,2),n,nn)*s.diff(nn,x)
check('static constrained reference gradient',s.simplify(gradmu-expected)==0,gradmu)
pressure=n*s.diff(E(n),n)-E(n)
check('reference pressure differential',s.simplify(s.diff(pressure,n)-n*s.diff(E(n),n,2))==0,pressure)
# Variation of -N(n+divP+E) at fixed P is -N(1+E') delta n.
# delta n=-div(n displacement), integration by parts gives -n grad[N(1+E')].
check('static lapse source derivative',s.diff(n+E(n),n)==mu,mu)

eps,n0,lap=s.symbols('epsilon n0 N',positive=True)
energy=eps*n+b*n*n/2
C=1+eps+b*n0
neq=(C/lap-1-eps)/b
check('explicit hydrostatic first integral',s.simplify(lap*(1+s.diff(energy,n).subs(n,neq))-C)==0,neq)
dn=s.factor(neq-n0)
check('reference clustering increment',s.simplify(dn-C*(1-lap)/(b*lap))==0,dn)
src=n+energy
delta=s.factor(src.subs(n,neq)-src.subs(n,n0))
check('source increment factored',s.simplify(delta-dn*(1+eps+b*(neq+n0)/2))==0,delta)
check('pressure supports total carrier acceleration',s.simplify(s.diff(n*s.diff(energy,n)-energy,n)-b*n)==0,'p=b n^2/2; n b grad n=-n(1+Eprime) grad ln N')
check('dust energy cannot support static lapse',s.diff(eps*n,n,2)==0,'grad[N(1+epsilon)]=0 implies grad N=0')

# Dilute far field, background-subtracted source: exact linear susceptibility.
q=s.symbols('q',positive=True)
source_series=s.diff(delta.subs(lap,1-q),q).subs(q,0)
check('background subtraction retains positive susceptibility',s.simplify(source_series-C*C/b)==0,source_series)
rad,mass=s.symbols('r M',positive=True)
tail=source_series*mass/rad
tailmass=s.integrate(4*s.pi*rad*rad*tail,rad)
check('conditional Newtonian tail nonintegrability',s.simplify(tailmass-2*s.pi*C*C*mass*rad*rad/b)==0,tailmass)

rows=[]
for nv in [s.Rational(999,1000),s.Rational(99,100),s.Rational(9,10)]:
    vals={eps:s.Rational(1,10),b:s.Integer(2),n0:s.Rational(1,100),lap:nv}
    dnval=s.simplify(dn.subs(vals)); dsval=s.simplify(delta.subs(vals))
    check('positive density/source N='+str(nv),dnval>0 and dsval>0,(dnval,dsval))
    rows.append(dict(N=str(nv),density_increment=str(dnval),source_increment=str(dsval)))
inertia=[]
for av in [s.Rational(1,1000),s.Rational(1,10),s.Integer(1),s.Integer(10)]:
    mv=M.subs({n:1,a:av})
    eigs=[float(ev) for ev in mv.eigenvals()]
    check('positive displacement block a='+str(av),min(eigs)>0,eigs)
    inertia.append(dict(Eprime=str(av),eigenvalues=eigs,reduced_I_over_fixed_I=str(av/(1+av))))
out=dict(checks=checks,kinetic_hessian=str(H),reduced_L=str(Leff),hydrostatic_density=str(neq),source_increment=str(delta),hydrostatic_controls=rows,inertia_controls=inertia,
         scope='Fixed-clock local current/reference EOS comparison and static lapse variation; gravity/clock/full metric stability excluded.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),hydrostatic_controls=rows,inertia_controls=inertia),indent=2))
