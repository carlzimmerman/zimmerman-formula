#!/usr/bin/env python3
"""Exact collision angular quadratures and source-lifetime competition.
No astrophysical density, source replenishment, or full kinetic closure assumed.
"""
import json,math,sys
from pathlib import Path
from scipy.integrate import quad
checks=[];collisions=[];rates=[]
def check(name,a,b,rtol=1e-10,atol=1e-13):
 checks.append(dict(name=name,actual=a,expected=b,passed=abs(a-b)<=atol+rtol*abs(b)))
# Initial source at rest; isotropic COM scattering under contact approximation.
for r in [2.,2.0004,2.01,3.,10.]:
 a=4*r/(1+r)**2
 moments=[]
 for j in [1,2,3,4]:
  val=quad(lambda ct:((-a/2*(1-ct))**j)/2,-1,1,epsabs=1e-13)[0]
  expected=(-a)**j/(j+1)
  check(f'angular moment r={r} j={j}',val,expected)
  moments.append(val)
 # Independent velocity reconstruction verifies full kinetic energy and recoil.
 for ct in [-1.,-.2,.7,1.]:
  st=math.sqrt(1-ct*ct)
  va=(r*st/(1+r),(1+r*ct)/(1+r))
  vb=(-st/(1+r),(1-ct)/(1+r))
  E_a=(va[0]**2+va[1]**2)/2
  E_b=r*(vb[0]**2+vb[1]**2)/2
  check(f'energy r={r} cos={ct}',E_a+E_b,.5)
  check(f'momentum x r={r} cos={ct}',va[0]+r*vb[0],0.)
  check(f'momentum z r={r} cos={ct}',va[1]+r*vb[1],1.)
  check(f'energy fraction r={r} cos={ct}',2*E_a,1-a/2*(1-ct))
 collisions.append(dict(mass_ratio=r,maximum_fractional_loss=a,mean_fractional_loss=a/2,
                        third_to_second_scaled_moment=abs(moments[2]/moments[1]),
                        minimum_outgoing_energy_fraction=1-a))
# All energies dimensionless in m=1 units. c3^2 chosen small, cancels ratio.
c32=1e-9
for u in [.001,.02,.1]:
 m=1.;M=2*math.sqrt(1+u*u);delta=M-2;eps=math.sqrt(1-4/M**2)
 mu=M/(1+M);Gab=4*c32/delta;cross=mu**2*Gab**2/math.pi
 Gamma=c32*eps/math.pi # m=1
 for chi in [.001,.01,.1]:
  nb=chi*delta**2/(4*c32)
  for z in [.0001,.001,.01]:
   E=z*delta;v=math.sqrt(2*E)
   nu=nb*cross*v;ratio=nu/Gamma
   expected=4*chi*mu**2*v/eps
   check(f'rate cancellation u={u} chi={chi} z={z}',ratio,expected)
   check(f'probability integral u={u} chi={chi} z={z}',
         quad(lambda t:ratio*math.exp(-t)*math.exp(-ratio*(1-math.exp(-t))),0,40)[0],
         -math.expm1(-ratio))
   assert v<=eps and ratio<=4*chi
   rates.append(dict(u=u,source_mixing_proxy=chi,daughter_energy_over_gap=z,
                     v_over_epsilon=v/eps,collision_rate_over_decay_rate=ratio,
                     probability_first_elastic_collision=-math.expm1(-ratio)))
# Frozen-rate diagnostic: compare exact compound jumps with two-moment diffusion.
# The physical contact rate depends on energy; this subsection explicitly freezes it.
a=8/9; jump_comparison=[]
for exposure in [.1,1.,3.]:
 for order in [1,2,3,4]:
  r_moment=quad(lambda r:r**order,1-a,1)[0]/a
  exact=math.exp(exposure*(r_moment-1))
  fp=math.exp(exposure*(-order*a/2+order*(order-1)*a*a/6))
  if order<=2:check(f'matched low moment exposure={exposure} order={order}',exact,fp)
  if order==3:check(f'third moment discrepancy exposure={exposure}',math.log(fp/exact),exposure*a**3/4)
  jump_comparison.append(dict(exposure=exposure,order=order,exact_jump_moment=exact,diffusion_moment=fp))
heating_probability=.5*math.erfc((a/2+a*a/6)*math.sqrt(3)/(a*math.sqrt(2)))
assert heating_probability>.1
r=dict(all_passed=all(c['passed'] for c in checks),check_count=len(checks),checks=checks,
       collision_grid=collisions,rate_grid=rates,jump_comparison=jump_comparison,
       frozen_rate_diffusion_heating_probability_at_unit_exposure=heating_probability,
       scope='Conditional cold-source off-resonant Born contact model and unreplenished decaying bath. No target profile, population state, or empirical rate derived.')
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(dict(all_passed=r['all_passed'],checks=len(checks),collisions=collisions,
                     min_ratio=min(x['collision_rate_over_decay_rate'] for x in rates),
                     max_ratio=max(x['collision_rate_over_decay_rate'] for x in rates)),indent=2))
sys.exit(0 if r['all_passed'] else 1)
