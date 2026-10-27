"""Necessary radial Jeans stress bound, allowing arbitrary nonnegative tangential stress."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from tension_charge import TensionCharge,h
from tension_refine import diagnostic
from refine import polish

def stress_bound(m,x):
    q=h(x);out={}
    for species,frac,mu in [('T',q,m.tpotential(x)),('F',1-q,m.fpotential(x))]:
        rho=m.m*frac/m.vol;acc=-np.gradient(mu,m.r,edge_order=2)
        integrand=m.r**2*rho*(m.g0-acc)
        upper=-cumulative_trapezoid(integrand[::-1],m.r[::-1],initial=0)[::-1]/m.r**2
        j=int(np.argmin(upper))
        out[species]=dict(min_radial_pressure_upper_bound=float(upper[j]),radius_kpc=float(m.r[j]*m.rm),population_at_minimum=float(frac[j]),virial_rhs=float(np.trapz(m.r**3*rho*(m.g0-acc),m.r)))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path(__file__).with_name('run_tension_refine').joinpath('results.json').read_text())['runs'];out=dict(stress=[],recovery=[])
    for r in rows:
        m=TensionCharge(6e10,3,r['n'],100,r['delta'],beta=1000,tau=.1);x=np.array(r['x']);out['stress'].append(dict(n=r['n'],delta=r['delta'],**stress_bound(m,x)))
    # Small displacements test return under energy minimization, not physical time evolution.
    for displacement in [-.2,.2]:
        x0=np.interp(m.r*m.rm+displacement,m.r*m.rm,x);xp,opt=polish(m,x0);d=diagnostic(m,xp)
        out['recovery'].append(dict(displacement_kpc=displacement,max_phase_difference=float(max(abs(xp-x))),energy_difference=float(d['energy']-rows[-1]['energy']),speed=d['speed'],qinner=d['qinner'],qouter=d['qouter'],force_error=d['force_error'],crossings_kpc=d['crossings_kpc']))
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
