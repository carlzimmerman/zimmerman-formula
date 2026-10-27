"""Finite-amplitude homologous radius model; not a fluid-collapse simulation."""
import json, math, sys
from pathlib import Path
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

xi4=5.844772675963704
eq=solve_ivp(lambda x,y:[y[1],1/y[0]-2*y[1]/x],[1e-6,xi4],
              [1+1e-12/6,1e-6/3],rtol=1e-11,atol=1e-13,dense_output=True)
D=3*quad(lambda s:s*s*math.log(4/float(eq.sol(xi4*s)[0])),1e-6/xi4,1,epsabs=1e-11)[0]
def V(y):return -3*D/y+y**3*(-D-1+3*math.log(y))
def dV(y):return 3*D/y**2+3*y*y*(-D+3*math.log(y))
barrier=brentq(dV,1e-4,.999)
gamma=1.
cases=[]
for y0 in [.8,1.2]:
    def rhs(t,z):
        y,v,out=z
        return [v,-dV(y)-gamma*v,gamma*v*v]
    sol=solve_ivp(rhs,[0,100],[y0,0,0],rtol=1e-10,atol=1e-12,max_step=.04)
    E0=V(y0)
    errors=[abs(.5*v*v+V(y)+out-E0) for y,v,out in sol.y.T]
    y,v,out=sol.y[:,-1]
    cases.append({'initial_radius_ratio':y0,'below_collapse_barrier_energy':E0<V(barrier),
                  'final_radius_ratio':float(y),'final_Sigma_over_target':float(y**-2),
                  'exported_energy_in_A_V_units':float(out),
                  'energy_ledger_error':max(errors),
                  'min_radius_ratio':float(min(sol.y[0]))})
checks={'local_energy_minimum':9-12*D>0,'barrier_inside_equilibrium':0<barrier<1,
        'all_return':all(abs(v['final_radius_ratio']-1)<1e-6 for v in cases),
        'all_positive_export':all(v['exported_energy_in_A_V_units']>0 for v in cases),
        'ledgers':all(v['energy_ledger_error']<1e-8 for v in cases),
        'tested_initial_energy_below_barrier':all(v['below_collapse_barrier_energy'] for v in cases)}
result={'model':'fixed-mass homologous logotropic density family against fixed external pressure plus ideal outgoing half-line mediator',
        'D_volume_mean_log_density_contrast':D,'V_second_derivative_at_equilibrium':9-12*D,
        'collapse_barrier_radius_ratio':barrier,'barrier_energy_above_equilibrium':V(barrier)-V(1),
        'cases':cases,'checks':checks,
        'non_claims':['No time-dependent shape, phase transition or halo envelope solved',
                      'No coefficient or microscopic damping derived',
                      'Gravity makes the potential unbounded at zero radius; this is a finite attraction basin']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
