"""Reciprocal finite-source core-mode/radial-wave action diagnostic."""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import diags, bmat, csc_matrix
from scipy.sparse.linalg import splu


def run(dx, dt, tmax, coupling):
    # Boundary is outside the light cone of the compact source during this run.
    radius = 90.
    n = int(round(radius/dx))-1
    r = dx*np.arange(1,n+1)
    xi4=5.844772675963704
    lam=.0903960231974605
    def rhs(x,y):
        th,tp,eta,ep=y
        return [tp,1/th-2*tp/x,ep,-4*ep/x-(4*tp/(x*th)+lam/th)*eta]
    x0=1e-5
    eq=solve_ivp(rhs,[x0,xi4],[1+x0*x0/6,x0/3,
        1-(4/3+lam)*x0*x0/10,-(4/3+lam)*x0/5],
        rtol=1e-10,atol=1e-12,dense_output=True,max_step=.01)
    j=np.zeros(n)
    mask=r<1.
    th,tp,eta,ep=eq.sol(xi4*r[mask])
    # xi derivative ep: div(xi_displacement)=3eta+xi*ep.
    j[mask]=coupling*(3*eta+xi4*r[mask]*ep)/(th*th)
    b=r*j
    mass_wave=4*math.pi*dx
    M=diags(np.r_[1.,np.full(n,mass_wave)],format='csc')
    lap=diags([-np.ones(n-1),2*np.ones(n),-np.ones(n-1)],[-1,0,1],format='csc')/(dx*dx)
    # modal mass=frequency=c_chi=1. The q/v coupling is antisymmetric.
    K=bmat([[csc_matrix([[1.]]),None],[None,mass_wave*lap]],format='csc')
    grow=csc_matrix((-mass_wave*b)[None,:])
    G=bmat([[csc_matrix((1,1)),grow],[-grow.T,csc_matrix((n,n))]],format='csc')
    h=dt/2
    left=M-h*G+h*h*K
    right=M+h*G-h*h*K
    factor=splu(left)
    z=np.zeros(n+1);v=np.zeros(n+1);z[0]=.1
    initial=.005
    sample=[];maxerr=0.
    for step in range(int(round(tmax/dt))):
        vn=factor.solve(right@v-2*h*(K@z))
        z+=h*(v+vn);v=vn
        if step%20==0 or step==int(round(tmax/dt))-1:
            core=.5*(v[0]**2+z[0]**2)
            wave=.5*(mass_wave*float(v[1:]@v[1:])+float(z[1:]@(mass_wave*lap@z[1:])))
            maxerr=max(maxerr,abs(core+wave-initial)/initial)
            sample.append([float((step+1)*dt),float(core/initial),float(wave/initial)])
    return {'dx':dx,'dt':dt,'tmax':tmax,'coupling':coupling,
            'relative_ledger_error':maxerr,'final_core_energy_fraction':sample[-1][1],
            'final_wave_energy_fraction':sample[-1][2],
            'final_q':float(z[0]),'history':sample,
            'source_radius':1.,'outer_radius':radius,
            'boundary_reachable':bool(tmax>=radius-1.)}


coarse=run(.05,.025,70.,1.)
fine=run(.025,.0125,70.,1.)
uncoupled=run(.05,.025,70.,0.)
checks={
 'ledger_coarse':coarse['relative_ledger_error']<1e-8,
 'ledger_fine':fine['relative_ledger_error']<1e-8,
 'no_boundary_reflection':not coarse['boundary_reachable'] and not fine['boundary_reachable'],
 'core_energy_transferred':fine['final_core_energy_fraction']<.05,
 'continuum_refinement':abs(fine['final_core_energy_fraction']-coarse['final_core_energy_fraction'])<.005,
 'uncoupled_control':abs(uncoupled['final_core_energy_fraction']-1)<1e-8,
}
result={'model':'fixed stable active-phase mode coupled reciprocally to radial mediator',
        'coarse':coarse,'fine':fine,'uncoupled':uncoupled,'checks':checks,
        'non_claims':['Not a full nonlinear cold-field or halo-formation simulation',
          'No microscopic multistream gate or coefficient derived',
          'Times and coupling are synthetic modal units',
          'Numerical midpoint conserved energy is not a UV or relativistic-causality certificate']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['coarse','fine','uncoupled']},indent=2))
print(json.dumps({k:{a:b for a,b in result[k].items() if a!='history'}
                  for k in ['coarse','fine','uncoupled']},indent=2))
assert all(checks.values())
