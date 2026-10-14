import json, math, sys
from pathlib import Path
import sympy as s
import mpmath as mp

out = Path(sys.argv[1]); out.mkdir(exist_ok=True)
mp.mp.dps = 90
checks = []
def check(name, value):
    value = bool(value)
    checks.append({'name': name, 'ok': value})
    if not value: raise AssertionError(name)
def zero(name, expr): check(name, s.simplify(expr) == 0)

t, L, r, rg, alpha = s.symbols('t L r rg alpha', positive=True)
D=1+t+t*t; rc=L/s.sqrt(D); rb=t*rc
q=t*(1+t)/D**s.Rational(3,2)
zero('horizon root rb', 1-q*L/rb-rb**2/L**2)
zero('horizon root rc', 1-q*L/rc-rc**2/L**2)
zero('sum radius identity', rb**2+rb*rc+rc**2-L**2)
zero('mass identity', rb*rc*(rb+rc)/L**2-q*L)
zero('total entropy deficit geometric mean', L**2-rb**2-rc**2-rb*rc)
zero('mass vs cosmological area deficit', q*L**2-rc/L*(L**2-rc**2))
zero('rM vs cosmological area deficit', q*L**2/(2*alpha)-rc/(2*alpha*L)*(L**2-rc**2))
zero('rM vs horizon area geometric mean', q*L**2/(2*alpha)-(rb+rc)/(2*alpha*L)*rb*rc)
check('Nariai q', s.simplify(q.subs(t,1)-2/(3*s.sqrt(3)))==0)
f=1-rg/r-r*r/L**2
K=s.diff(f,r,2)**2+4*(s.diff(f,r)/r)**2+4*((1-f)/r**2)**2
zero('Kretschmann from radial metric', K-12*rg**2/r**6-24/L**4)
x, ell=s.symbols('x ell', positive=True)
V=(1-1/x)*(1+ell**2/x**2)
zero('marginal capture energy', V.subs({x:2,ell:2})-1)
zero('marginal capture stationary orbit', s.diff(V,x).subs({x:2,ell:2}))
check('marginal capture unstable', s.diff(V,x,2).subs({x:2,ell:2})<0)
zero('entropy-balance radius', (rg*r*L/r**3).subs(r,s.sqrt(rg*L))-1)

for st in ['1e-24','1e-18','1e-12','1e-6','.01','.1','.5','.9','1']:
    z=mp.mpf(st); d=1+z+z*z; bc=z/mp.sqrt(d); cc=1/mp.sqrt(d)
    qq=z*(1+z)/d**mp.mpf('1.5')
    for name,a,b in [('mass',qq,bc*cc*(bc+cc)),
                     ('entropy',1-bc*bc-cc*cc,bc*cc),
                     ('cosmo_deficit',qq,cc*(1-cc*cc))]:
        check(name+' t='+st, abs(a/b-1)<mp.mpf('1e-60'))

inp=Path('real_research/derivation_chain_2026/FP0_core_postulates_results.json')
nums=json.loads(inp.read_text())['numbers']
G=mp.mpf('6.67430e-11'); c=mp.mpf('299792458'); hbar=mp.mpf('1.054571817e-34')
kB=mp.mpf('1.380649e-23'); eV=mp.mpf('1.602176634e-19')
Ms=mp.mpf('1.98847e30'); pc=mp.mpf('3.0856775814913673e16')
a0=mp.mpf(str(nums['a0_canonical'])); al=mp.sqrt(3/(32*mp.pi)); LL=al*c*c/a0
lp2=hbar*G/c**3; H=c/LL
def fnum(v): return float(v)
rows=[]
for m in [1,4e6,1e8,6e10,1e14]:
    M=mp.mpf(str(m))*Ms; rr=2*G*M/c**2; qm=rr/LL
    tm=mp.findroot(lambda z:z*(1+z)/(1+z+z*z)**mp.mpf('1.5')-qm,(qm,qm*mp.mpf('1.001')))
    rbc=tm*LL/mp.sqrt(1+tm+tm*tm); rcc=LL/mp.sqrt(1+tm+tm*tm)
    rM=mp.sqrt(G*M/a0); rta=(G*M/H**2)**(mp.mpf(1)/3)
    rcurv=(rr*rr*LL**4/2)**(mp.mpf(1)/6)
    check('astrophysical root '+str(m),abs((rr/rbc+rbc*rbc/LL**2)-1)<mp.mpf('1e-60'))
    check('rM area equality '+str(m),abs(rM*rM/(rcc*(LL*LL-rcc*rcc)/(2*al*LL))-1)<mp.mpf('1e-55'))
    check('curvature vs turnaround '+str(m),abs(rcurv/rta-2**(mp.mpf(1)/6))<mp.mpf('1e-60'))
    rows.append({'M_solar':m,'r_g_pc':fnum(rr/pc),'rM_kpc':fnum(rM/pc/1000),
                 'r_turnaround_kpc':fnum(rta/pc/1000),'r_curvature_kpc':fnum(rcurv/pc/1000),
                 'vacuum_force_at_rM_over_a0':fnum(H*H*rM/a0),
                 'weyl_over_vacuum_K_at_rM':fnum(rr*rr*LL**4/(2*rM**6)),
                 'cosmological_entropy_loss_kB':fnum(mp.pi*(LL**2-rcc**2)/lp2),
                 'BH_kT_eV_if_mass_is_BH':fnum(hbar*c**3/(8*mp.pi*G*M)/eV)})

capture=[]
MBH=mp.mpf('4e6')*Ms; rbh=2*G*MBH/c**2
for vkm in [100,200,1000]:
    v=mp.mpf(vkm)*1000; e2=1/(1-(v/c)**2)
    xx=mp.findroot(lambda xx:e2*xx*(xx-mp.mpf('1.5'))-(xx-1)**2,(mp.mpf('1.99'),mp.mpf('2.01')))
    el2=xx**2/(2*xx-3)
    b_exact=rbh*mp.sqrt(el2/(e2-1)); b_nr=2*rbh*c/v
    check('capture nonrel error '+str(vkm),abs(b_exact/b_nr-1)<mp.mpf('1e-4'))
    rho=mp.mpf('.01')*Ms/pc**3; tenGyr=mp.mpf('1e10')*mp.mpf('365.25')*86400
    capture.append({'v_km_s':vkm,'b_capture_pc':fnum(b_exact/pc),
                    'relative_nonrel_error':fnum(b_exact/b_nr-1),
                    'homogeneous_capture_Msolar_per_10Gyr':fnum(rho*mp.pi*b_exact**2*v*tenGyr/Ms)})

thresholds=[{'carrier_rest_eV':en,'BH_mass_kg_for_kT_equals_rest':fnum(hbar*c**3/(8*mp.pi*G*en*eV))} for en in [.62,16,143]]
AV=c*c/(6*LL); kernel=[]
for yy in [1e-4,.01,.1,1,10,100]:
    y=mp.mpf(str(yy)); simple=(y+mp.sqrt(y*y+4*y))/2; ve=y+mp.sqrt(AV/a0*y)
    kernel.append({'gbar_over_a0':yy,'simple_g_over_a0':fnum(simple),'Verlinde_g_over_a0':fnum(ve),'relative_difference':fnum(ve/simple-1)})
result={'checks':checks,'passed':len(checks),'constants':{'G':fnum(G),'c':fnum(c),'Msun_kg':fnum(Ms),'a0':fnum(a0),'alpha':fnum(al),'L_Gpc':fnum(LL/pc/1e9),'H_per_s':fnum(H),'dS_kT_eV':fnum(hbar*H/(2*mp.pi)/eV),'Verlinde_aM_over_a0':fnum(AV/a0),'entropy_balance_radius_over_rM':fnum(mp.sqrt(2*al))},'mass_examples':rows,'capture_examples':capture,'Hawking_thresholds':thresholds,'kernel_comparison':kernel,'central_BH_to_galaxy_rM_ratio':math.sqrt(4e6/6e10),'precision_decimal_digits':mp.mp.dps}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
