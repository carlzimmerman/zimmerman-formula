"""Independent high precision finite-polynomial checks of offset orbits."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import math,json,time,resource
import numpy as np
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
from common import CommonBackground
from precise_common import PreciseCommonOrbit
from oracle import OffsetOrbit,MASS

def main(out):
 start=time.monotonic();source=ROOT/'reviews/weak_completion_2026_11_04/integration/run_joint006/result.json';d=json.loads(source.read_text());N=d['state']['N'];Y=np.array(d['state']['Y']);q=np.array(d['case']['q']);W=np.array(d['case']['W']);model=PreciseCommonOrbit(CommonBackground(),q,W,64);model.J0=d['state']['J0'];model.last_x=d['state']['xmid'];oracle=OffsetOrbit(model,N,Y,64);coarse=OffsetOrbit(model,N,Y,32);mp.mp.dps=70
 # Independent real embedding of the serialized float polynomial coefficients.
 p2=[mp.mpf(float(z)) for z in oracle.p2];m=[[mp.mpf(float(z)) for z in row] for row in oracle.m];v=[mp.mpf(float(z)) for z in oracle.v];yy=[[mp.mpf(float(z)) for z in row] for row in oracle.Y];t3=mp.mpf(float(oracle.t3));e0=[[mp.sqrt(m[0][s]+pk) for pk in p2] for s in range(model.ns)]
 def direct_potential(x):
  potential=sum(v[j-1]*x**j for j in range(1,5));gas=[]
  for s in range(model.ns):
   dm=sum(m[j][s]*x**j for j in range(1,4))
   gas.extend(yy[s][k]*(mp.sqrt(e0[s][k]**2+dm)-e0[s][k]) for k in range(model.n))
  return potential+t3*mp.fsum(gas)
 # Independent degree-12 sqrt Taylor series with an explicit binomial-tail
 # bound. Use it only for the slow high-precision quadrature reference.
 order=12;poly=[mp.mpf(0)]*(3*order+1)
 for j in range(1,5):poly[j]=v[j-1]
 for s in range(model.ns):
  for k in range(model.n):
   if not yy[s][k]:continue
   E=e0[s][k];z=[mp.mpf(0)]+[m[j][s]/E**2 for j in range(1,4)];power=[mp.mpf(1)]
   for n in range(1,order+1):
    nxt=[mp.mpf(0)]*(len(power)+3)
    for i,a in enumerate(power):
     for j in range(1,4):nxt[i+j]+=a*z[j]
    power=nxt;factor=t3*yy[s][k]*E*mp.binomial(mp.mpf('.5'),n)
    for j,a in enumerate(power):poly[j]+=factor*a
 def polynomial(x):return mp.polyval(list(reversed(poly)),x)
 def derivative(x):return mp.polyval([j*poly[j] for j in range(len(poly)-1,0,-1)],x)
 center=mp.findroot(derivative,(mp.mpf('-1e-12'),mp.mpf('1e-12')),tol=mp.mpf('1e-60'));u0=polynomial(center)
 rows=[];checks={};max_direct=0.;max_tail=mp.mpf(0)
 for fraction in (1e-4,1e-8,1e-12,1e-16):
  J=model.J0*fraction;orbit=oracle.orbit(J);low=coarse.orbit(J);eps=mp.mpf(float(orbit['excitation']));points=np.linspace(orbit['left_displacement'],orbit['right_displacement'],17);errs=[]
  maxd=max(abs(oracle.center+orbit['left_displacement']),abs(oracle.center+orbit['right_displacement']))
  tail=mp.mpf(0);maxz=mp.mpf(0)
  for s in range(model.ns):
   dm_bound=sum(abs(m[j][s])*mp.mpf(float(maxd))**j for j in range(1,4))
   for k in range(model.n):
    z=dm_bound/e0[s][k]**2;maxz=max(maxz,z)
    if z>=1:raise ValueError('Taylor reference domain is not convergent')
    tail+=abs(t3*yy[s][k]*e0[s][k])*z**(order+1)/(1-z)
  for x in points:
   physical=direct_potential(mp.mpf(float(oracle.center+x)))-direct_potential(center)
   fast=float(oracle.offset(x)[0]);errs.append(float(abs(mp.mpf(fast)-physical)/eps))
  direct_error=max(errs);max_direct=max(max_direct,direct_error);max_tail=max(max_tail,tail/eps)
  # Polynomial reference turning points and high-precision Simpson integration
  # in theta avoid the float64 total-energy oracle entirely.
  guess=mp.mpf(float(orbit['left_displacement']));left=mp.findroot(lambda x:polynomial(center+x)-u0-eps,(guess*mp.mpf('.999'),guess*mp.mpf('1.001')),tol=mp.mpf('1e-60'))
  guess=mp.mpf(float(orbit['right_displacement']));right=mp.findroot(lambda x:polynomial(center+x)-u0-eps,(guess*mp.mpf('.999'),guess*mp.mpf('1.001')),tol=mp.mpf('1e-60'))
  mid=(left+right)/2;half=(right-left)/2
  def integrand(theta):
   dx=half*mp.sin(theta);x=mid-half*mp.cos(theta);kin=eps-(polynomial(center+x)-u0)
   return dx*mp.sqrt(max(kin,mp.mpf(0)))
  action=mp.sqrt(2*MASS)/mp.pi*mp.quad(integrand,[0,mp.pi/2,mp.pi],method='gauss-legendre')
  action_error=float(abs(action/mp.mpf(J)-1));phase_error=abs(low['excitation']/orbit['excitation']-1)
  ordinary=None
  if fraction==1e-4:
   old=model.orbit(N,Y,J=J);ordinary=dict(excitation_relative=float((old['E']-old['minimum'])/orbit['excitation']-1),period_relative=float(old['period']/orbit['period']-1),left_relative=float((old['x_inner']-old['xmid'])/orbit['left_displacement']-1),harmonic=old['harmonic'])
  checks['direct_offset_'+str(fraction)]=direct_error<2e-10
  checks['reference_action_'+str(fraction)]=action_error<2e-9
  checks['phase_refinement_'+str(fraction)]=phase_error<2e-9
  checks['reference_tail_'+str(fraction)]=float(tail/eps)<1e-12
  rows.append(dict(J_fraction_initial=fraction,J=J,excitation=orbit['excitation'],amplitude=(orbit['right_displacement']-orbit['left_displacement'])/2,
    period=orbit['period'],harmonic_excitation_relative_difference=orbit['harmonic_excitation_relative_difference'],
    harmonic_period_relative_difference=orbit['period']*oracle.omega/(2*math.pi)-1,
    excitation_lost_in_float_total=orbit['excitation_lost_in_float_total'],phase32_64_excitation_difference=phase_error,
    direct_mp_offset_error_over_excitation=direct_error,independent_mp_action_relative_error=action_error,
    reference_sqrt_taylor_tail_bound_over_excitation=str(tail/eps),max_delta_mass2_over_E0sq=float(maxz),ordinary_overlap=ordinary))
 overlap=rows[0]['ordinary_overlap'];checks['ordinary_nonharmonic_overlap']=(not overlap['harmonic'] and abs(overlap['excitation_relative'])<2e-5 and abs(overlap['period_relative'])<2e-5)
 checks['minimum_displacement']=abs(float(center)-oracle.center)<1e-22
 checks['tiny_excitation_retained']=rows[-1]['excitation_lost_in_float_total'] and rows[-1]['excitation']>0
 result=dict(claim_id='CC11_CANCELLATION_SAFE_LOCAL_ORBIT',checks={k:bool(v) for k,v in checks.items()},N=N,artificial_state=True,actual_Y_source=str(source.relative_to(ROOT)),rows=rows,
  local=dict(anchor=oracle.anchor,minimum_displacement=oracle.center,mp_minimum_displacement=str(center),first_derivative=oracle.F0,curvature=oracle.k,local_displacement_bounds=[oracle.left,oracle.right]),
  runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  scope='Artificial small-J stress states at the actual fresh common30 warm Y. Finite local spline representation only, direct70digitpotential differences and degree12sqrt-series action reference with tail bounds. No new cold population or coupled-history solution.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
