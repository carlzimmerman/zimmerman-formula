"""Fully varied gated-AQUAL local quadratic checks; no complete covariant closure.
Only the specified output directory under this file's directory is writable.
"""
import argparse,hashlib,json,math,platform,subprocess
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True)
ap.add_argument('--mutate-drop-constitutive-mixing',action='store_true');args=ap.parse_args()
out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks={}
def check(name,value):
 checks[name]=bool(value);print(('PASS ' if value else 'FAIL ')+name)
# Energy convention: H_field=U+rho phi, L_field= -U-rho phi.
# Set 8 pi G=1, a0=m=1 in finite controls; general symbols in identities.
g,q,K,n,m,I,k,af,h,enq,enn,eqq,w=s.symbols('g q K n m I k a_field h enq enn eqq w',positive=True)
f=10*q**3-15*q**4+6*q**5
U=g*g+f*(2*g**3/3-g*g)
B=g*g-2*g**3/3
check('field_q_curvature_equals_frozen_gate',s.simplify(s.diff(U,q,2)+B*s.diff(f,q,2))==0)
check('longitudinal_elliptic_coefficient',s.simplify(s.diff(U,g,2)-2*(1-f+2*g*f))==0)
check('transverse_elliptic_coefficient',s.simplify(s.diff(U,g)/g-2*(1-f+g*f))==0)
check('constitutive_mixing_nonzero',s.simplify(s.diff(U,q,g)-s.diff(f,q)*(2*g*g-2*g))==0)
C=s.Matrix([m,s.I*k*h]);Hf=s.Matrix([[enn,enq],[enq,eqq]])
He=s.simplify(Hf-C*C.conjugate().T/(af*k*k))
check('reduced_density_Jeans_term',s.simplify(He[0,0]-enn+m*m/(af*k*k))==0)
check('reduced_scalar_constitutive_term',s.simplify(He[1,1]-eqq+h*h/af)==0)
check('reduced_hermitian_mixing',s.simplify(He[0,1]-enq-s.I*m*h/(af*k))==0)
M=s.diag(m/(n*k*k),n*I)
aa=n*enn*k*k/m-n*m/af;bb=(eqq-h*h/af)/(n*I)
cc2=enq*enq*k*k/(m*I)+m*h*h/(af*af*I)
poly=(aa-w)*(bb-w)-cc2
check('full_coupled_dispersion',s.simplify((He-w*M).det()/M.det()-poly)==0)
check('physical_density_displacement_inertia',M.det()==m*I/(k*k))
# Positive gradient field block lowers every quadratic form after elimination.
v1,v2=s.symbols('v1 v2',real=True);vec=s.Matrix([v1,v2]);decrement=s.simplify((vec.T*(Hf-He)*vec)[0])
check('Schur_decrement_positive_form',s.simplify(decrement-(m*m*v1*v1+h*h*k*k*v2*v2)/(af*k*k))==0)
# Characteristic UV low root if enn>0.
uv=(eqq-h*h/af-enq*enq/enn)/(n*I)
check('UV_low_root_from_asymptotic_product',s.simplify(s.limit((aa*bb-cc2)/(aa+bb),k,s.oo)-uv)==0)
ss=s.symbols('growth_rate_squared',nonnegative=True)
alpha=n*enn/m;JJ=n*m/af;LL=enq**2/(m*I);MM=m*h**2/(af**2*I)
check('exact_growth_bound_endpoint_reduction',s.simplify(poly.subs(w,-ss)-(k*k*(alpha*(bb+ss)-LL)+(ss-JJ)*(bb+ss)-MM))==0)
kap=s.symbols('kappa',positive=True);y=s.symbols('y',positive=True)
bbgrad=(eqq+kap*k*k-h*h/af)/(n*I)
gradpoly=s.expand((aa*bbgrad-cc2)*m*I)
cutpoly=kap*enn*y*y+(enn*(eqq-h*h/af)-enq*enq-m*m*kap/af)*y-m*m*eqq/af
check('positive_gradient_cutoff_polynomial',s.simplify(gradpoly-cutpoly.subs(y,k*k))==0)
check('gradient_principal_speeds_product',s.simplify(s.limit((aa*bbgrad-cc2)/(k**4),k,s.oo)-enn*kap/(m*I))==0)

def smooth(x):
 x=np.clip(x,0.,1.);return 10*x**3-15*x**4+6*x**5
def fp(x):return 30*x*x*(1-x)**2 if 0<x<1 else 0.
def fpp(x):return 60*x*(1-x)*(1-2*x) if 0<x<1 else 0.
def local(nn,gas=0.,angle=1.):
 gg=.2;kk=100.;gateB=gg*gg-2*gg**3/3;Q=smooth(nn-1)
 qq=brentq(lambda x:nn*kk*(x-Q)-gateB*fp(x),Q,min(1.,Q+.01),xtol=1e-14)
 delta=qq-Q;qp=fp(nn-1);qpp=fpp(nn-1)
 NN=gas-2*kk*delta*qp+nn*kk*qp*qp-nn*kk*delta*qpp
 NQ=kk*delta-nn*kk*qp;QQ=nn*kk-gateB*fpp(qq)
 fl=smooth(qq);along=2*(1-fl+2*gg*fl);across=2*(1-fl+gg*fl)
 field=along*angle*angle+across*(1-angle*angle)
 mix=fp(qq)*(2*gg*gg-2*gg)*angle
 return dict(n=nn,q=qq,epp=gas,angle_cos=angle,enn=NN,enq=NQ,eqq=QQ,
     a_field=field,h=mix,longitudinal=along,transverse=across,B=gateB,K=kk)
def root_pair(p,ii,kv,gradient=0.,mixing=True,gravity=True):
 nn=p['n'];NN=p['enn'];NQ=p['enq'];QQ=p['eqq'];a=p['a_field']
 h=p['h'] if mixing else 0.
 grav=nn/a if gravity else 0.
 aa=nn*NN*kv*kv-grav;bb=(QQ+gradient*kv*kv-(h*h/a if gravity else 0.))/(nn*ii)
 cc2=NQ*NQ*kv*kv/ii+(h*h/(a*a*ii) if gravity else 0.)
 tr=aa+bb;disc=np.sqrt((aa-bb)**2+4*cc2);hi=(tr+disc)/2
 # hi>0 in declared finite controls: rationalized low root is safe.
 lo=(aa*bb-cc2)/hi
 return float(lo),float(hi)
rows=[]
for nn in np.linspace(1.05,1.95,19):
 for angle in (0.,.5,1.):
  p=local(float(nn),0.,angle);ii=.01
  for kv in (.01,1.,10.,1e4):
   flo,fhi=root_pair(p,ii,kv,gravity=False)
   lo,hi=root_pair(p,ii,kv,mixing=not args.mutate_drop_constitutive_mixing)
   rows.append(dict(**p,I=ii,k=kv,frozen_w2=[flo,fhi],full_w2=[lo,hi]))
check('both_radial_and_transverse_ellipticity',all(r['longitudinal']>0 and r['transverse']>0 for r in rows))
check('positive_kinetic_in_all_controls',all(r['n']>0 and r['I']>0 and r['k']>0 for r in rows))
check('constraint_never_raises_low_eigenvalue',all(r['full_w2'][0]<=r['frozen_w2'][0]+1e-7 for r in rows))
mid=local(1.5);frozenmid=root_pair(mid,.01,1e4,gravity=False)
fullmid=root_pair(mid,.01,1e4,mixing=not args.mutate_drop_constitutive_mixing)
check('full_field_creates_UV_spinodal_at_frozen_stable_midpoint',frozenmid[0]>0 and fullmid[0]<-1.,
      )
# No constitutive mixing control (still gravity) and exact UV rate.
uvnum=(mid['eqq']-mid['h']**2/mid['a_field']-mid['enq']**2/mid['enn'])/(mid['n']*.01)
check('finite_UV_rate_matches_full_root',abs(fullmid[0]/uvnum-1)<1e-5)
formation=[]
kgrid=np.logspace(-3,6,401)
for ii in (.001,.01,.1,1.,10.):
 lows=[root_pair(mid,ii,float(kv))[0] for kv in kgrid]
 maxrate=np.sqrt(max(0.,-min(lows)));S=mid['enq']**2/mid['enn']-mid['eqq']+mid['h']**2/mid['a_field']
 beta=(mid['eqq']-mid['h']**2/mid['a_field'])/(mid['n']*ii)
 JJ=mid['n']/mid['a_field'];MM=mid['h']**2/(mid['a_field']**2*ii)
 s0=JJ+2*MM/(np.sqrt((JJ+beta)**2+4*MM)+JJ+beta)
 bound=np.sqrt(max(S/(mid['n']*ii),s0))
 check('uniform_endpoint_bound_'+str(ii),maxrate<=bound*(1+1e-8))
 formation.append(dict(I=ii,exact_uniform_growth_supremum=bound,UV_growth_rate=np.sqrt(S/(mid['n']*ii)),maximum_sampled_growth=maxrate,
   Jeans_rate=np.sqrt(mid['n']/mid['a_field']),scan_k_min=1e-3,scan_k_max=1e6))
check('large_finite_inertia_bounds_formation_rate',formation[3]['maximum_sampled_growth']<1.1*formation[3]['Jeans_rate'])
pressure=[]
for gas in (5.,10.,20.):
 for nn in np.linspace(1.01,1.99,99):
  p=local(float(nn),gas,1.)
  for kv in (1.,10.):
   lo,hi=root_pair(p,1e-8,kv);base=nn*gas*kv*kv-nn/p['a_field']
   pressure.append(dict(**p,I=1e-8,k=kv,w2=[lo,hi],baseline_gas_Jeans_w2=base,
     fractional_change=abs(lo/base-1)))
ctrl=[r for r in pressure if r['epp']==20.]
check('full_field_costed_pressure_control_positive',all(r['w2'][0]>0 and r['w2'][1]>0 for r in ctrl))
check('full_field_costed_pressure_control_fidelity',all(r['fractional_change']<.1 for r in ctrl))
# Shared inertia tradeoff across cold/warm states, same q,K,n,g.
def middev(ii):
 p=local(1.5,20.);return max(abs(root_pair(p,ii,kv)[0]/(1.5*20*kv*kv-1.5/p['a_field'])-1) for kv in (1.,10.))
Igas=brentq(lambda ii:middev(ii)-.1,1e-8,.01,xtol=1e-14)
S=mid['enq']**2/mid['enn']-mid['eqq']+mid['h']**2/mid['a_field'];Iformation=S*mid['a_field']/mid['n']**2
check('cold_formation_slowdown_and_warm_fidelity_disjoint_here',Iformation>Igas*1000)
# Positive spatial state energy regularizes high k, with an explicit finite band.
spatial=[]
for gradient in (.0001,.01,1.):
 p=mid;a=p['a_field'];NN=p['enn'];NQ=p['enq'];QQ=p['eqq'];h=p['h']
 coeff=[gradient*NN,NN*(QQ-h*h/a)-NQ*NQ-gradient/a,-QQ/a]
 ycut=float(max(np.roots(coeff)));cut=np.sqrt(ycut)
 kg=np.logspace(-3,4,1001);rates=[np.sqrt(max(0.,-root_pair(p,.01,float(kv),gradient=gradient)[0])) for kv in kg]
 imax=int(np.argmax(rates))
 warm=local(1.5,20.);devs=[]
 for probe in (1.,10.):
  base=1.5*20*probe*probe-1.5/warm['a_field']
  devs.append(abs(root_pair(warm,1e-8,probe,gradient=gradient)[0]/base-1))
 spatial.append(dict(kappa=gradient,cutoff_k=cut,static_internal_length_proxy=np.sqrt(gradient/QQ),
     warm_probe_max_fractional_change=max(devs),
     principal_speed2=[p['n']*NN,gradient/(p['n']*.01)],
     maximum_sampled_growth=float(rates[imax]),fastest_sampled_k=float(kg[imax]),
     high_k_w2=root_pair(p,.01,float(cut*10),gradient=gradient)))
check('spatial_cost_control_UV_positive',all(r['high_k_w2'][0]>0 for r in spatial))
check('large_spatial_cost_suppresses_extra_rapid_growth',spatial[-1]['maximum_sampled_growth']<1.1*np.sqrt(mid['n']/mid['a_field']))
paths=['sol61_push/main_theory/breakthrough_2026_10_05/REPORT.md',
 'sol61_push/main_theory/breakthrough_2026_10_05/formation_checks.py',
 'campaign_fresh_gravity/CFG349_khronon_memory_switch/README.md',
 'campaign_fresh_gravity/CFG349_khronon_memory_switch/FROZEN_CRITERIA.md']
summary=dict(midpoint=mid,frozen_mid_w2=frozenmid,full_mid_w2=fullmid,UV_w2=uvnum,
  pressure_max_changes={str(gas):max(r['fractional_change'] for r in pressure if r['epp']==gas) for gas in (5.,10.,20.)},
  shared_inertia_bound=dict(I_cold_UV_rate_at_most_Jeans=Iformation,I_warm_tenpercent_max=Igas,ratio=Iformation/Igas))
record=dict(checks=checks,summary=summary,rows=rows,pressure_controls=pressure,
  formation=formation,spatial_cost=spatial,mutation=args.mutate_drop_constitutive_mixing,
  provenance=dict(supplied_base='11b994fee',observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
   input_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
   software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__)))
(out/'results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(summary,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
