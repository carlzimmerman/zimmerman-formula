#!/usr/bin/env python3
"""Exact dust transfer modes and affine dark-fluid degeneracy, with bounded controls.
Only writes --output-dir beneath this script's directory; no Boltzmann run.
"""
import argparse,json,math,platform
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
import scipy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
INPUTS=[
 'fable_independent_2026/L37_recombination_footing.py',
 'fable_independent_2026/L182_recombination_kernel_solver.py',
 'fable_independent_2026/L183_class_kernel_recombination.py',
 'real_research/reviews/cmb_inertia_recombination.py',
 'campaign_fresh_gravity/CFG253_dark_energy_to_cold_mass/README.md',
 'campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md',
 'real_research/dark_fluid_2026/FL1_order_parameter.py',
 'sol61_push/recombination_and_structure_growth/growth_and_identity/checks.py',
]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,default=HERE)
 ap.add_argument('--mutate-drop-initial-velocity',action='store_true'); args=ap.parse_args()
 out=args.output_dir.resolve(); out.relative_to(HERE); out.mkdir(exist_ok=True,parents=True)
 checks=[]; numbers={}
 def check(name,passed,detail):
  checks.append(dict(name=name,passed=bool(passed),detail=str(detail)))
  print(('PASS ' if passed else 'FAIL ')+name+': '+str(detail))
 x=s.symbols('x',positive=True); u,v,w,z=s.symbols('u v w z',real=True)
 dN=lambda f:s.simplify(x*s.diff(f,x))
 A=(3*u+(0 if args.mutate_drop_initial_velocity else 2)*v)/5
 B=u-A
 dm=A*x+B*x**s.Rational(-3,2)
 rel=w+2*z*(1-x**s.Rational(-1,2))
 check('common_growth_ODE',s.simplify(dN(dN(dm))+dN(dm)/2-3*dm/2)==0,'matter-dominated subhorizon growing+decaying modes')
 check('common_initial_density',s.simplify(dm.subs(x,1)-u)==0,'delta_m at drag')
 check('common_initial_velocity',s.simplify(dN(dm).subs(x,1)-v)==0,'initial logarithmic derivative independently retained')
 check('relative_mode_ODE',s.simplify(dN(dN(rel))+dN(rel)/2)==0,'relative constant+velocity modes')
 check('relative_initial_data',s.simplify(rel.subs(x,1)-w)==0 and s.simplify(dN(rel).subs(x,1)-z)==0,'both density and velocity')
 matrix=s.Matrix([dm,dN(dm),rel,dN(rel)]).jacobian([u,v,w,z])
 check('finite_time_transfer_invertible',s.simplify(matrix.det()-1/x)==0,'det T=x^-1>0 for finite x')
 fb=s.symbols('f_b',positive=True); fc=1-fb
 db=dm+fc*rel; dc=dm-fb*rel
 check('species_mass_weight_recovery',s.simplify(fc*dc+fb*db-dm)==0,'cold and baryon source reaction share same potential')
 check('growing_projection_preserves_acoustic_density_and_velocity',s.diff((3*u+2*v)/5,v)==s.Rational(2,5),
       'A(k)=[3 delta_m,d(k)+2 delta_m,d prime(k)]/5')
 check('potential_memory',s.simplify(dm/x-A-B*x**s.Rational(-5,2))==0,
       'a² rho_m delta_m proportional to delta_m/x: constant A + decaying B')
 # Arbitrary-expansion relative null test, derived from equal pressureless forces.
 a,H,Hp=s.symbols('a H Hprime',positive=True); dn,dnn=s.symbols('Delta_prime Delta_doubleprime')
 derivative=a*a*H*(dnn+(2+Hp/H)*dn)
 check('arbitrary_background_relative_invariant',s.simplify(derivative.subs(dnn,-(2+Hp/H)*dn))==0,
       'd/dln a(a²H Delta prime)=0; exact linear GR pressureless relative equation')
 # Exact affine-fluid stress decomposition, arbitrary local velocity; metric (-+++).
 rhoC,rhoL,V=s.symbols('rho_c rho_Lambda V',real=True)
 gamma=1/s.sqrt(1-V*V); four=s.Matrix([gamma,gamma*V,0,0]); metric=s.diag(-1,1,1,1)
 rho=rhoC+rhoL; pressure=-rhoL
 stress=(rho+pressure)*four*four.T+pressure*metric
 dustvac=rhoC*four*four.T-rhoL*metric
 check('affine_stress_exact_identity',s.simplify(stress-dustvac)==s.zeros(4),'valid for |V|<1, rho_c>=0; no particle identity implied')
 aa=s.symbols('a',positive=True); charge=s.symbols('C',positive=True)
 rhoa=rhoL+charge/aa**3
 check('affine_background_continuity',s.simplify(aa*s.diff(rhoa,aa)+3*(rhoa-rhoL))==0,'rho=Lambda+C a^-3, C independent of Lambda')
 check('vacuum_does_not_select_cold_charge',s.diff(aa**3*(rhoa-rhoL),rhoL)==0,'an algebraic degeneracy, not a production mechanism')
 # Orthogonal coupled ODE integrations, arbitrary acoustic density/velocity data.
 fbn=.02237/(.02237+.1200); fcn=1-fbn
 samples=[(1,1,0,0),(1,1,.5,-.5),(1,1,-.5,.5),(0,0,1,-1),(0,0,1,0)]
 ode=[]; grid=np.linspace(0,math.log(1000),401)
 for ic in samples:
  def rhs(n,y):
   c,cp,b,bp=y; source=1.5*(fcn*c+fbn*b)
   return [cp,source-.5*cp,bp,source-.5*bp]
  sol=solve_ivp(rhs,(0,grid[-1]),ic,t_eval=grid,rtol=2e-11,atol=2e-13,method='DOP853')
  U=fcn*ic[0]+fbn*ic[2]; VV=fcn*ic[1]+fbn*ic[3]; WW=ic[2]-ic[0]; ZZ=ic[3]-ic[1]
  xx=np.exp(grid); am=(3*U+2*VV)/5; bm=2*(U-VV)/5
  mt=am*xx+bm*xx**-1.5; mtp=am*xx-1.5*bm*xx**-1.5
  dr=WW+2*ZZ*(1-xx**-.5); drp=ZZ*xx**-.5
  exact=np.array([mt-fbn*dr,mtp-fbn*drp,mt+fcn*dr,mtp+fcn*drp])
  err=float(np.max(np.abs(sol.y-exact)/(1+np.abs(exact))))
  inv=np.sqrt(xx)*(sol.y[3]-sol.y[1])
  drift=float(np.max(np.abs(inv-ZZ)))
  ode.append(dict(initial=ic,growing_amplitude=am,maximum_scaled_error=err,relative_invariant_drift=drift))
  check('coupled_ODE_'+str(ic),err<1e-8 and drift<1e-9,f'max scaled error={err:.3g}, relative invariant drift={drift:.3g}')
 numbers['coupled_controls']=ode
 # Controlled dust-start catch-up example, NOT a real transfer-function fit.
 ratio=lambda xx: fcn*(xx-3+2/np.sqrt(xx))/(fcn*xx+fbn*(3-2/np.sqrt(xx)))
 targets=[]
 for tol in (.5,.1,.01):
  xx=brentq(lambda xx:ratio(xx)-(1-tol),1,1e5)
  targets.append(dict(fractional_baryon_deficit=tol,a_over_drag=xx,
      illustrative_z_for_zdrag_1060=1061/xx-1))
 check('catchup_monotone_finite_thresholds',targets[0]['a_over_drag']<targets[1]['a_over_drag']<targets[2]['a_over_drag'],targets)
 numbers['catchup_example']=dict(fb=fbn,initial='delta_c=delta_c prime=1,delta_b=delta_b prime=0, normalized linear shape',thresholds=targets)
 # A residual relative density is not the same as lost acoustic structure memory.
 memory=[]
 for acoustic_phase in (0,math.pi/2,math.pi,3*math.pi/2):
  sd=.5*math.cos(acoustic_phase); vd=-.5*math.sin(acoustic_phase)
  projection=fcn+fbn*(3*sd+2*vd)/5
  memory.append(dict(phase=acoustic_phase,baryon_density=sd,baryon_log_derivative=vd,
                     common_growing_amplitude=projection))
 check('catchup_does_not_erase_acoustic_projection',max(r['common_growing_amplitude'] for r in memory)-min(r['common_growing_amplitude'] for r in memory)>0.09,memory)
 numbers['acoustic_memory_surrogate']=memory
 # Exact relative quadrature checks expansion dependence; no total-growth fit here.
 # Normalize a_drag=1 for EdS; integral Delta_N=z x^-1/2.
 for xx in (2,10,1000):
  integral=quad(lambda ax:ax**-1.5,1,xx,epsabs=1e-12)[0]
  check('relative_background_quadrature_'+str(xx),abs(integral-2*(1-xx**-.5))<1e-10,'a²H Delta_N constant, EdS H proportional a^-3/2')
 payload=dict(checks=checks,numbers=numbers,mutation=args.mutate_drop_initial_velocity,
              software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__))
 (out/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
 failed=sum(not c['passed'] for c in checks); print(f'{len(checks)-failed}/{len(checks)} checks pass; {failed} failures')
 return int(failed>0)

if __name__=='__main__': raise SystemExit(main())
