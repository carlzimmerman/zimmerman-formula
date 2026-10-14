import json, sys
from pathlib import Path
import sympy as s
import mpmath as mp
out=Path(sys.argv[1]); out.mkdir(exist_ok=True); mp.mp.dps=80
checks=[]
def ck(n,v):
    checks.append({'name':n,'ok':bool(v)})
    if not bool(v): raise AssertionError(n)
def ze(n,e): ck(n,s.simplify(e)==0)
r,m,Q,L,b,c,x,a,u,D,D0,E=s.symbols('r m Q L b c x a u D D0 E',positive=True)
f=1-2*m/r+Q**2/r**2-r**2/L**2
mroots=(b+c)*(1-(b*b+c*c)/L**2)/2
qroots=b*c*(1-(b*b+b*c+c*c)/L**2)
ze('two-root mass',f.subs(r,b).subs({m:mroots,Q**2:qroots}))
ze('two-root charge',f.subs(r,c).subs({m:mroots,Q**2:qroots}))
tempsum=(s.diff(f,r).subs(r,b)+s.diff(f,r).subs(r,c)).subs({m:mroots,Q**2:qroots})
ze('temperature difference factorization',tempsum-(b-c)**2*(b+c)*((b+c)**2-L**2)/(L**2*b**2*c**2))
ze('distinct equal-temperature roots imply critical mass',mroots.subs(c,L-b)-b*(L-b)/L)
ze('distinct equal-temperature roots imply Q2=m2',(qroots-mroots**2).subs(c,L-b))
branch={m:L*x*(1-x),Q:L*x*(1-x)}
for label,rr,sign in [('bh',L*x,1),('cosmo',L*(1-x),-1)]:
    ze('lukewarm root '+label,f.subs(branch).subs(r,rr))
    ze('lukewarm derivative '+label,s.diff(f,r).subs(branch).subs(r,rr)-sign*2*(1-2*x)/L)
ze('horizon sum',L*x+L*(1-x)-L)
ze('horizon product',L*x*L*(1-x)-branch[m]*L)
ze('entropy deficit',L**2-(L*x)**2-(L*(1-x))**2-2*branch[m]*L)
rp=2/(r*s.diff(f,r))
rpp=-(s.diff(f,r,2)*rp**2+4*rp/r**2)/s.diff(f,r)
rq=-2*Q/(r**2*s.diff(f,r))
Sm=sum((2*s.pi*r*rp).subs(branch).subs(r,rr) for rr in [L*x,L*(1-x)])
Smm=sum((2*s.pi*(rp**2+r*rpp)).subs(branch).subs(r,rr) for rr in [L*x,L*(1-x)])
SQ=sum((2*s.pi*r*rq).subs(branch).subs(r,rr) for rr in [L*x,L*(1-x)])
ze('fixed-charge entropy stationary',Sm)
ze('fixed-charge entropy second derivative',Smm+2*s.pi/(x**3*(1-x)**3))
ze('charge-varying entropy derivative',SQ+2*s.pi*L)
ze('horizon electric potential difference', (Q/(L*x)-Q/(L*(1-x))).subs(branch)-(1-2*x))
K=s.symbols('K',positive=True)
W=(-a*u-a*a*s.log(1-u/a))/K
ze('full constitutive force',K*s.diff(W,u)-a*u/(a-u))
ze('residual after self-gravity',K*s.diff(W,u)-u-u*u/(a-u))
H=D0**2*(-D/D0-s.log(1-D/D0))
force=s.diff(H,D)
ze('gauge force reconstruction',force-D/(1-D/D0))
Lg=D0*E-D0**2*s.log(1+E/D0)
d=s.diff(Lg,E); ep=s.diff(d,E); et=d/E
ze('electric Legendre inverse',d.subs(E,force)-D)
ze('physical gauge cone',et/ep-(1+E/D0))
al=s.symbols('alpha',positive=True)
ze('BH wall ratio squared', (branch[Q]/(al/L))/(L*x)**2-(1-x)/(al*x))
ze('cosmo wall ratio squared',(branch[Q]/(al/L))/(L*(1-x))**2-x/(al*(1-x)))
ze('Maxwell field energy vs vacuum at transition',(branch[Q]**2/(3*(s.sqrt(branch[m]*L/al))**4/L**2))-al**2/3)

alpha=mp.sqrt(3/(32*mp.pi)); num=[]
for qm in ['1e-12','1e-6','.01','.1','.24']:
    z=mp.mpf(qm); xx=2*z/(1+mp.sqrt(1-4*z)); bb=xx; cc=1-xx
    ck('equal k '+qm,abs(((z/bb**2-z*z/bb**3-bb))-(cc-z/cc**2+z*z/cc**3))<mp.mpf('1e-55'))
    rat=mp.sqrt(cc/(alpha*bb))
    ck('wall exterior to BH '+qm,rat>1)
    ck('entropy fixed-charge maximum '+qm,-2*mp.pi/(xx**3*(1-xx)**3)<0)
    num.append({'m_over_L':float(z),'rb_over_L':float(bb),'rc_over_L':float(cc),'kappa_over_c2Linv':float(1-2*xx),'rwall_over_rb':float(rat),'u_b_over_a0':float(rat**2),'u_c_over_a0':float(bb/(alpha*cc))})

# Orthogonal finite differences at fixed charge, independent quartic root solve.
for z in ['.01','.1','.24']:
    mm=mp.mpf(z); qq=mm; xx=2*mm/(1+mp.sqrt(1-4*mm))
    def ent(mm0):
        fun=lambda rr:1-2*mm0/rr+qq**2/rr**2-rr**2
        bb=mp.findroot(fun,(xx*mp.mpf('.99999'),xx*mp.mpf('1.00001')))
        cc=mp.findroot(fun,((1-xx)*mp.mpf('.99999'),(1-xx)*mp.mpf('1.00001')))
        return mp.pi*(bb*bb+cc*cc)
    eps=mp.mpf('1e-18'); second=(ent(mm+eps)-2*ent(mm)+ent(mm-eps))/eps**2
    exact=-2*mp.pi/(xx**3*(1-xx)**3)
    ck('fixed Q numerical entropy curvature '+z,abs(second/exact-1)<mp.mpf('1e-16'))

# Exterior nonlinear field energy at the displacement wall is integrable.
coef=(1+2*mp.log(2))/3
integ=mp.quad(lambda zz:zz**2*(-1/zz**2-mp.log(1-1/zz**2)),[1,mp.mpf('1.01'),2,10,1000])
# At large z use the convergent series, avoiding cancellation at infinity.
tail=mp.fsum(mp.mpf(1000)**(3-2*n)/(n*(2*n-3)) for n in range(2,50))
ck('exterior field energy integral',abs((integ+tail)/coef-1)<mp.mpf('1e-50'))
base=json.loads(Path('sol61_push/cold_horizon_connection_2026_10_14/run_v1/results.json').read_text())['constants']
G=mp.mpf(str(base['G'])); cs=mp.mpf(str(base['c'])); ms=mp.mpf(str(base['Msun_kg'])); a0=mp.mpf(str(base['a0'])); pc=mp.mpf('3.0856775814913673e16'); LL=alpha*cs**2/a0
examples=[]
for Mass in [4e6,1e8,6e10]:
    mg=G*mp.mpf(str(Mass))*ms/cs**2; wall=mp.sqrt(mg*LL/alpha)
    examples.append({'mass_solar':Mass,'rwall_pc':float(wall/pc),'rwall_over_approximately_lukewarm_rb':float(wall/mg),'exterior_nonlinear_field_mass_over_total_mass':float(coef*mp.sqrt(alpha*mg/LL))})
result={'passed':len(checks),'checks':checks,'horizon_samples':num,'mass_examples':examples,'alpha':float(alpha),'critical_charge_to_mass_rationalized_SI':float(mp.sqrt(4*mp.pi*G)),'energy_equality_radius_over_rM':float((32*mp.pi)**(-mp.mpf(1)/4)),'max_central_BH_neutralization_fraction_assigned_4e6_vs_6e10':4e6/6e10,'exterior_energy_integral':float(coef),'interpretation':'Equal-T critical-charge bridge works in Maxwell theory at fixed charge. Saturating nonlinear medium is a different theory and cannot inherit its horizon solution; exact domain and characteristic gates fail for the naive identification.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
