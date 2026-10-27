"""Reciprocal finite-source core-mode/radial-wave action diagnostic."""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import diags, bmat, csc_matrix
from scipy.sparse.linalg import splu


OPEN_OUTLET='--open-outlet' in sys.argv


def run(dx, dt, tmax, coupling):
    # Short run ends before boundary contact; extended run uses an impedance.
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
    if OPEN_OUTLET:
        lap[-1,-1]=1/(dx*dx)
    # modal mass=frequency=c_chi=1. The q/v coupling is antisymmetric.
    K=bmat([[csc_matrix([[1.]]),None],[None,mass_wave*lap]],format='csc')
    grow=csc_matrix((-mass_wave*b)[None,:])
    G=bmat([[csc_matrix((1,1)),grow],[-grow.T,csc_matrix((n,n))]],format='csc')
    damping=np.zeros(n+1)
    if OPEN_OUTLET:
        damping[-1]=4*math.pi
    D=diags(damping,format='csc')
    h=dt/2
    left=M+h*D-h*G+h*h*K
    right=M-h*D+h*G-h*h*K
    factor=splu(left)
    z=np.zeros(n+1);v=np.zeros(n+1);z[0]=.1
    initial=.005
    sample=[];maxerr=0.;outer_amplitude=0.;exported=0.
    monitor=int(round(70./dx))-1
    incoming=0.;outgoing=0.
    for step in range(int(round(tmax/dt))):
        vn=factor.solve(right@v-2*h*(K@z))
        v_mid=.5*(v+vn)
        exported+=dt*float(v_mid@(D@v_mid))
        z_mid=z+h*v_mid
        ux=(z_mid[monitor+2]-z_mid[monitor])/(2*dx)
        incoming+=dt*(v_mid[monitor+1]+ux)**2
        outgoing+=dt*(v_mid[monitor+1]-ux)**2
        z+=h*(v+vn);v=vn
        if step%20==0 or step==int(round(tmax/dt))-1:
            core=.5*(v[0]**2+z[0]**2)
            wave=.5*(mass_wave*float(v[1:]@v[1:])+float(z[1:]@(mass_wave*lap@z[1:])))
            maxerr=max(maxerr,abs(core+wave+exported-initial)/initial)
            outer_amplitude=max(outer_amplitude,float(np.max(np.abs(z[1:][r>85]))))
            sample.append([float((step+1)*dt),float(core/initial),float(wave/initial),float(exported/initial)])
    return {'dx':dx,'dt':dt,'tmax':tmax,'coupling':coupling,
            'relative_ledger_error':maxerr,'final_core_energy_fraction':sample[-1][1],
            'final_wave_energy_fraction':sample[-1][2],
            'exported_canonical_wave_energy_fraction':sample[-1][3],
            'final_q':float(z[0]),'history':sample,
            'outer_band_max_abs_r_chi':outer_amplitude,
            'monitor_radius':float(r[monitor]),
            'incoming_to_outgoing_characteristic_power':incoming/max(outgoing,1e-300),
            'final_spherical_surface_energy_over_initial':2*math.pi*z[-1]**2/(r[-1]*initial),
            'source_radius':1.,'outer_radius':radius,
            'outgoing_impedance_boundary':OPEN_OUTLET,
            'boundary_reachable':bool(tmax>=radius-1.)}


tmax=350. if OPEN_OUTLET else 70.
coarse=run(.05,.025,tmax,1.)
fine=run(.025,.0125,tmax,1.)
uncoupled=run(.05,.025,tmax,0.)
checks={
 'ledger_coarse':coarse['relative_ledger_error']<1e-8,
 'ledger_fine':fine['relative_ledger_error']<1e-8,
 'boundary_model':OPEN_OUTLET or (not coarse['boundary_reachable'] and not fine['boundary_reachable']),
 'core_energy_transferred':fine['final_core_energy_fraction']<.05,
 'continuum_refinement':abs(fine['final_core_energy_fraction']-coarse['final_core_energy_fraction'])<.005,
 'uncoupled_control':abs(uncoupled['final_core_energy_fraction']-1)<1e-8,
 'finite_radius_outgoing_or_boundary_quiet':OPEN_OUTLET or max(coarse['outer_band_max_abs_r_chi'],fine['outer_band_max_abs_r_chi'])<1e-10,
 'small_measured_incoming_characteristic':not OPEN_OUTLET or fine['incoming_to_outgoing_characteristic_power']<.01,
}
checks={k:bool(v) for k,v in checks.items()}
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
