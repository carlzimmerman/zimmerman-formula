#!/usr/bin/env python3
"""Same-action source matching: exact identities and a bounded finite-mass witness.
Run from repository root, writes only alongside this script.
--mutate-drop-dark-source must fail. No prior scripts imported/executed.
"""
import argparse
import hashlib
import json
import math
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INPUTS = [
 'sol61_push/cold_component/README.md',
 'sol61_push/cold_component/identity_checks.py',
 'sol61_push/cold_component/contract.json',
 'sol61_push/support_and_assembly.py',
 'campaign_fresh_gravity/CFG4_README.md',
 'campaign_fresh_gravity/CFG4_target.out',
 'campaign_fresh_gravity/CFG44_fluid_target/B4_actions_reciprocity.py',
 'campaign_fresh_gravity/CFG45_rule_readings.py',
 'campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md',
 'real_research/dark_fluid_2026/FL1_order_parameter.py',
 'campaign_fresh_gravity/CFG253_dark_energy_to_cold_mass/README.md',
 'campaign_fresh_gravity/CFG293_wavefield_cores_satellites/README.md',
 'campaign_fresh_gravity/CFG344_postreion_cold_accretion/README.md',
 'campaign_fresh_gravity/CFG345_cold_component_small_scales/README.md',
 'sol61_push/cold_component/breakthrough_2026_10_05/source_matching.py',
]

def digest(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--mutate-drop-dark-source',action='store_true')
 ap.add_argument('--output-dir',type=Path,default=HERE)
 args=ap.parse_args(); tag='mutate' if args.mutate_drop_dark_source else 'main'
 outdir=args.output_dir.resolve(); outdir.relative_to(HERE)
 outdir.mkdir(parents=True,exist_ok=True)
 start=datetime.now(timezone.utc).isoformat(); tick=time.monotonic()
 before={p:digest(ROOT/p) for p in INPUTS}; checks=[]; nums={}
 def check(name,ok,detail):
  checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
  print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))

 # FL1 static gate-on plateau, retaining auxiliaries until AFTER variation.
 x=s.symbols('x', real=True); G,m=s.symbols('G m',positive=True)
 phi,u,v,w,lam,ps,a,b,rb=[s.Function(n)(x) for n in ('Phi','u','v','w','lambda','Psi','a','b','rho_b')]
 ep=8*s.pi*G; rd=m*(a*a+b*b); q=s.Function('q')
 d=lambda z:s.diff(z,x); dd=lambda z:s.diff(z,x,2)
 rd_source=0 if args.mutate_drop_dark_source else rd
 L=-(rb+rd_source)*phi-(2*d(phi)*d(u)-d(u)**2)/ep+q(d(w)**2)/ep
 L+=ps*(dd(w)-dd(u)+dd(v))/ep+lam*(dd(v)-4*s.pi*G*rd)/ep
 el=lambda z:s.expand(s.euler_equations(L,z,x)[0].lhs*ep)
 check('FL1_Phi_variation_total_source',s.simplify(el(phi)-(2*dd(u)-ep*(rb+rd)))==0,
       'Delta u=4piG(rho_b+rho_c), varied before constraints')
 check('FL1_lambda_variation_cold_source',s.simplify(el(lam)-(dd(v)-4*s.pi*G*rd))==0,'Delta v=4piG rho_c')
 check('FL1_Psi_constraint',s.simplify(el(ps)-(dd(w)-dd(u)+dd(v)))==0,'w=u-v modulo homogeneous boundary mode')
 check('FL1_v_variation_opposite_pair',s.simplify(el(v)-(dd(ps)+dd(lam)))==0,'lambda=-Psi under matching boundary conditions')
 check('FL1_u_variation_metric_plus_kernel',s.simplify(el(u)-(2*dd(phi)-2*dd(u)-dd(ps)))==0,
       'Phi=u+Psi/2; dark potential Phi+lambda/2=u')
 # Schrodinger evolution conserves positive material mass, even at phase nodes.
 potential=s.symbols('V',real=True)
 at=-dd(b)/(2*m)+m*potential*b; bt=dd(a)/(2*m)-m*potential*a
 j=a*d(b)-b*d(a)
 check('wave_mass_continuity',s.simplify(2*m*(a*at+b*bt)+d(j))==0,
       'partial_t rho_c+div j_c=0, rho_c=m|psi|^2>=0; no flux => total mass constant')
 # Finite source interaction checks reaction rather than silently frozen baryons.
 B,D,R=s.symbols('B D R',positive=True)
 cross=-G*B*D/R
 check('Newtonian_mixed_response_reciprocal',s.diff(cross,B,D)==-G/R,'same mixed derivative for both source orders')
 xb,xc=s.symbols('x_b x_c',real=True)
 spatial_cross=-G*B*D/(xc-xb) # sector xc>xb
 force_b=-s.diff(spatial_cross,xb); force_c=-s.diff(spatial_cross,xc)
 check('source_positions_equal_opposite',s.simplify(force_b+force_c)==0 and
       s.simplify(force_b-G*B*D/(xc-xb)**2)==0,
       'independent source-position derivatives; F_b=+GBD/(x_c-x_b)^2=-F_c')
 # Exact P2 exterior phantom. This is NOT adopted nu_mono.
 p=s.sqrt(B*B+B*R*R)-B
 dp=s.diff(p,R)
 check('P2_positive_exterior_density',s.simplify(dp-B*R/s.sqrt(B*B+B*R*R))==0,
       'P prime>0 for B,R>0 in G=a0=1 units')
 eta=s.Rational(134,25) # 5.36, example cosmic ratio only
 residual=eta*B-p
 check('constant_floor_requires_negative_cold_density',s.simplify(s.diff(residual,R)+dp)==0,
       'where eta B>P, rho_c=-P prime/(4pi R^2)<0')
 # Finite, positive, smooth Plummer budget avoids interpreting eta B radially.
 h=s.symbols('h',positive=True)
 f=eta*B*R**3/(R*R+h*h)**s.Rational(3,2)
 fp=s.diff(f,R)
 check('finite_Plummer_budget_density',s.simplify(fp-3*eta*B*h*h*R*R/(R*R+h*h)**s.Rational(5,2))==0,
       'F prime>0, F infinity=eta B')
 P=lambda r: math.sqrt(1+r*r)-1
 F=lambda r: float(eta)*r**3/(1+r*r)**1.5
 PP=lambda r:r/math.sqrt(1+r*r)
 FP=lambda r:3*float(eta)*r*r/(1+r*r)**2.5
 rows=[]
 for r in (2,4,6):
  rows.append(dict(r_over_rM=r,F=F(r),P=P(r),required_cold=F(r)-P(r),
                   required_cold_derivative=FP(r)-PP(r)))
 check('finite_positive_reservoir_counterexample',all(z['required_cold']>0 for z in rows) and
       rows[0]['required_cold']>rows[1]['required_cold']>rows[2]['required_cold'] and
       rows[1]['required_cold_derivative']<0,rows)
 nums['finite_budget_counterexample']=rows
 # Repair: EDGE matching only, retaining a positive finite Plummer profile.
 edge=4.; scale=1-P(edge)/F(edge); qtotal=float(eta)*scale
 Q=lambda r:scale*F(r)
 repair=[]
 for r in (0.5,1,2,4,6):
  target=max(F(r),P(r)); obs=P(r)+Q(r)
  repair.append(dict(r_over_rM=r,target_dark=target,actual_dark=obs,
      acceleration_ratio=(1+obs)/(1+target),velocity_log10_residual=0.5*math.log10((1+obs)/(1+target)),
      radial_shell_omega2=(1+Q(r))/r**3,
      cold_ESD_proxy=qtotal*r*r/(math.pi*(r*r+1)**2)))
 check('edge_matching_exact',abs(P(edge)+Q(edge)-max(F(edge),P(edge)))<1e-13,
       'one aperture match; not radial max')
 mass=quad(lambda r:3*qtotal*r*r/(1+r*r)**2.5,0,np.inf,epsabs=1e-11)[0]
 check('repair_finite_positive_mass',qtotal>0 and abs(mass/qtotal-1)<1e-10,
       f'total conserved mass parameter={qtotal}, integral={mass}; no formation selection claimed')
 check('repair_stable_ordered_circular_shells',all(z['radial_shell_omega2']>0 for z in repair),
       'classical collisionless support, same Newtonian u; no finite-hbar wave equilibrium theorem')
 check('repair_has_nonzero_rotation_prediction',abs(repair[2]['velocity_log10_residual'])>0.04,repair[2])
 nums['edge_repair']=dict(edge_over_rM=edge,h_over_rM=1,scale=scale,cold_total_mass_over_B=qtotal,rows=repair)
 # Alternative gate repairs algebra, but its naive action insertion adds source reaction.
 P0,E0=s.symbols('P E0',positive=True); W=1-D/P0
 check('suppression_gate_mass_dictionary',s.simplify(D+W*P0-P0)==0,'0<D<P: W=1-D/P; else W=0')
 check('gate_has_cold_source_reaction',s.diff(W*E0,D)==-E0/P0,
       'd(W E0)/dD=-E0/P; cannot retain unchanged dark Euler-Lagrange equation')
 E=-B*B/R; Ptoy=B*R
 gated=(1-D/Ptoy)*E
 mixed=s.simplify(s.diff(gated,B,D))
 check('gate_mixed_reaction_counterexample',mixed==1/R**2,
       'finite-coordinate surrogate E0=-B^2/R, P=B R: nonzero mixed derivative, not a physical MOND action')
 check('gate_radial_chain_rule',s.simplify(s.diff(gated,R)-(W*s.diff(E,R)).subs(P0,Ptoy))!=0,
       'varying the gate contributes E0 partial_R W; post-variation force multiplication omits it')
 nums['gate_toy_extra_radial_derivative']=str(s.simplify(s.diff(gated,R)-(W*s.diff(E,R)).subs(P0,Ptoy)))
 after={p:digest(ROOT/p) for p in INPUTS}
 check('inputs_unchanged_during_run',before==after,'actual source hashes pinned; dirty shared checkout')
 failures=sum(not c['passed'] for c in checks); exitcode=int(failures>0)
 result=outdir/(tag+'_results.json')
 result.write_text(json.dumps(dict(checks=checks,numbers=nums,mutation=args.mutate_drop_dark_source),indent=2)+'\n')
 manifest=dict(schema_version=1,claim_id='COLD_FL1_RADIAL_MAX_POSITIVITY_20261005',
  repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),dirty=True),
  command='python3 '+str(Path(__file__).relative_to(ROOT))+(' --mutate-drop-dark-source' if args.mutate_drop_dark_source else ''),
  environment=dict(software=[dict(name='Python',version=platform.python_version()),dict(name='Sympy',version=s.__version__),
      dict(name='Numpy',version=np.__version__),dict(name='Scipy',version=scipy.__version__)],hardware=platform.platform()),
  mathematics=dict(assertion_tested='Static FL1 plateau source dictionary; radial residual positivity; finite Plummer witness; edge-only repair and gate reaction',
      coefficient_domain='Exact real Sympy expressions plus IEEE754 finite witness/quadrature',
      conventions='Gate f=1,M2=0; matching homogeneous modes; P2 numeric witness; G=a0=B=1; eta=5.36,h=1,R_edge=4',
      inputs=[dict(path=p,sha256=sha) for p,sha in before.items()],
      bounds=dict(witness_radii=[2,4,6],repair_radii=[0.5,1,2,4,6],quadrature_absolute_tolerance=1e-11),
      non_claims=['No universal impossibility of T5 or alternate actions','No cold identity or abundance selection',
                  'No exact stationary wave, formation, merger, or relativistic lensing derivation']),
  randomness=dict(used=False,generator='',seed=None),run=dict(started_at=start,runtime_seconds=time.monotonic()-tick,exit_status=exitcode),
  outputs=[dict(path=str(result.relative_to(ROOT)),sha256=digest(result))],checks=checks,
  result=f'{len(checks)-failures}/{len(checks)} checks passed; '+('negative control rejects missing cold Poisson source' if args.mutate_drop_dark_source else 'scoped radial completion refuted by positive finite-mass witness'),
  residual_risks=['Self-review only','Static plateau with stated boundary conditions','P2 witness, not nu_mono numerical prediction',
                  'Plummer repair chosen, not dynamically selected','Lens ESD is Newtonian proxy conditional on relativistic dictionary'])
 (outdir/(tag+'_manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
 print(manifest['result']); return exitcode

if __name__=='__main__': raise SystemExit(main())
