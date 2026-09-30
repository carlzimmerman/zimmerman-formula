#!/usr/bin/env python3
"""Force local dipoles by one actual-shaped point-mass passage, not seeded phases.

p_a=omega_a^2 xi_a/2, alpha_bar=1, eta=sqrt(3), beta=sqrt(3)/2.
g(t)=A*(1,0,t)/(1+t^2)^(3/2); units b/V=1. Sign is conventional.
Straight Born trajectory, fixed external field, no orbital reaction or Poisson
feedback. Propagate perturbative orders 1,2,3 and the full quadratic local ODE.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp


def cross(z):
    return np.array([np.cross(z[1],z[2]),np.cross(z[2],z[0]),np.cross(z[0],z[1])])


def mixed(a,b):
    return np.array([np.cross(a[1],b[2])+np.cross(b[1],a[2]),
                     np.cross(a[2],b[0])+np.cross(b[2],a[0]),
                     np.cross(a[0],b[1])+np.cross(b[0],a[1])])


def run(amplitude,frequency_scale,start=-20):
    omega=frequency_scale*np.array([.3,1.,1.002]); w2=omega[:,None]**2
    beta=math.sqrt(3)/2
    ts=np.linspace(start,40,3001)
    def field(t): return amplitude*np.array([1.,0.,t])/(1+t*t)**1.5
    def rhs(t,y):
        p=y[:27].reshape(3,3,3); dp=y[27:54].reshape(3,3,3)
        f=y[54:63].reshape(3,3); df=y[63:72].reshape(3,3)
        grav=field(t)
        dd=np.empty_like(p)
        dd[0]=w2*(grav-p[0])
        dd[1]=-w2*(p[1]+beta*cross(p[0]))
        dd[2]=-w2*(p[2]+beta*mixed(p[0],p[1]))
        ddf=w2*(grav-f-beta*cross(f))
        power=float(np.sum(df*grav))
        return np.r_[dp.ravel(),dd.ravel(),df.ravel(),ddf.ravel(),power]
    sol=solve_ivp(rhs,(start,40),np.zeros(73),t_eval=ts,method='DOP853',rtol=2e-10,atol=1e-14)
    p=sol.y[:27].reshape(3,3,3,-1)
    f=sol.y[54:63].reshape(3,3,-1); df=sol.y[63:72].reshape(3,3,-1)
    unit=np.array([np.ones_like(ts),np.zeros_like(ts),ts])/np.sqrt(1+ts*ts)
    core=np.abs(ts)<=4
    radial2=np.einsum('it,it->t',-p[1].sum(axis=0)/3,unit)
    radial3=np.einsum('it,it->t',-p[2].sum(axis=0)/3,unit)
    grav=np.array([field(t) for t in ts]).T
    radial_linear=np.einsum('it,it->t',grav-p[0].sum(axis=0)/3,unit)
    intrinsic=.5*np.sum(f*f+df*df/w2[:,:,None],axis=(0,1))+beta*np.einsum('it,it->t',f[0],np.cross(f[1].T,f[2].T).T)
    work=sol.y[72]
    budget_error=float(np.max(np.abs(intrinsic-work))/max(np.max(np.abs(intrinsic)),1e-30))
    approx=p.sum(axis=0)
    error=float(np.max(np.abs(f-approx))/max(np.max(np.abs(f)),1e-30))
    return dict(amplitude=amplitude,frequency_scale=frequency_scale,start=start,completed=sol.success,
                max_second_order_radial=float(np.max(np.abs(radial2))),
                max_second_order_transverse=float(np.max(np.abs(p[1,:,1]))),
                max_third_order_radial=float(np.max(np.abs(radial3[core]))),
                core_linear_radial_lag_over_peak_field=float(np.max(np.abs(radial_linear[core]))/amplitude),
                core_third_order_over_A_squared=float(np.max(np.abs(radial3[core]))/amplitude**2),
                first_order_excitation_over_A=float(np.max(np.abs(p[0]))/amplitude),
                full_vs_third_order_relative_error=error,energy_work_relative_error=budget_error,
                final_internal_energy=float(intrinsic[-1]),integrated_external_work=float(work[-1]),
                maximum_full_field=float(np.max(np.abs(f))))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}",flush=True)
    for amplitude,scale,start in [(.002,1.,-20),(.004,1.,-20),(.008,1.,-20),(.004,3.,-20),(.004,10.,-20),(.004,1.,-40)]:
        r=run(amplitude,scale,start); rows.append(r)
        label=f'A={amplitude}_omega_scale={scale}_start={start}'
        check('completed_'+label,r['completed'],str(r))
        check('pump_work_budget_'+label,r['energy_work_relative_error']<2e-7,'internal energy gain accounted for by prescribed external work; orbital reaction is absent')
        check('planar_quadratic_projection_'+label,r['max_second_order_radial']<1e-25 and r['max_second_order_transverse']>1e-12,'second-order cross force is perpendicular to the orbital plane, not a radial MOND term')
        check('perturbative_vs_full_'+label,r['full_vs_third_order_relative_error']<2e-5,'full local quadratic ODE agrees with the retained first three orders in tested weak forcing')
    primary=rows[:3]
    excitations=[r['first_order_excitation_over_A'] for r in primary]
    check('passage_derives_linear_amplitude_scaling',(max(excitations)-min(excitations))/np.mean(excitations)<1e-6,'zero upstream excitation; first-order oscillation amplitude proportional to force amplitude follows from the ODE')
    ratios=[primary[i+1]['max_third_order_radial']/primary[i]['max_third_order_radial'] for i in (0,1)]
    check('first_radial_nonlinearity_is_cubic',all(abs(v-8)<1e-5 for v in ratios),f'doubling forcing multiplies first radial nonlinear term by {ratios}; desired quadratic ratio would be four')
    check('adiabatic_limit_reduces_linear_lag',rows[4]['core_linear_radial_lag_over_peak_field']<primary[1]['core_linear_radial_lag_over_peak_field'],f'lag {primary[1]["core_linear_radial_lag_over_peak_field"]:.8g} -> {rows[4]["core_linear_radial_lag_over_peak_field"]:.8g} as frequencies increase')
    a,b=primary[1],rows[-1]
    sensitivity=abs(a['max_third_order_radial']-b['max_third_order_radial'])/a['max_third_order_radial']
    check('upstream_cutoff_sensitivity',sensitivity<.05,f'changing finite start from -20 to -40 changes cubic peak by {sensitivity:.8g}; planar projection is structural regardless')
    data=dict(checks=checks,rows=rows,bounds=dict(end=40,samples=3001,rtol=2e-10,atol=1e-14,core=[-4,4]),
              verdict='Passage pumps motion with field-proportional amplitudes without seeded phases, but the quadratic term is transverse and the first radial nonlinear term is cubic. This local planar mechanism does not derive the required MOND response or 32pi.',
              non_claims=['No complete stream action','Born trajectory not self-consistent deflection','No bath or matter reaction included','No gravitational field solve','Finite upstream cutoff','Quadratic truncation not a UV-complete model'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; theory and 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
