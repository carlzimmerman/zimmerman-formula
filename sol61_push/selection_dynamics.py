#!/usr/bin/env python3
"""Equal-charge local dipoles: Hamiltonian, aligned stability, passive damping.

Published quadratic local ODE only. Damping is a diagnostic addition, not
a derivation of a bath or a closed physical energy budget.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def crosses(z):
    return np.array([np.cross(z[1],z[2]),np.cross(z[2],z[0]),np.cross(z[0],z[1])])


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}",flush=True)
    xs=sp.symbols('z0:9',real=True); c,lam=sp.symbols('c lambda',real=True)
    z=[sp.Matrix(xs[3*i:3*i+3]) for i in range(3)]
    ex=sp.Matrix([1,0,0])
    V=sum((q-ex).dot(q-ex)/2 for q in z)+c*z[0].dot(z[1].cross(z[2]))
    for a in range(3):
        b,d=(a+1)%3,(a+2)%3
        residual=sp.Matrix([sp.diff(V,t) for t in xs[3*a:3*a+3]])-(z[a]-ex+c*z[b].cross(z[d]))
        check(f'gradient_species_{a}',all(sp.simplify(t)==0 for t in residual),'one scalar triple product generates all cyclic forces')
    aligned={xx:(1 if i%3==0 else 0) for i,xx in enumerate(xs)}
    H=sp.hessian(V,xs).subs(aligned)
    polynomial=H.charpoly(lam)
    # Sympy charpoly creates a plain generator even if its requested name
    # was declared real. Use the actual generator for the comparison.
    lam=polynomial.gen
    characteristic=sp.factor(polynomial.as_expr())
    expected=(lam-1)**5*((lam-1)**2-3*c*c)**2
    check('aligned_Hessian_spectrum',sp.expand(characteristic-expected)==0,str(characteristic))
    check('weak_field_stability_threshold',sp.simplify(sp.sqrt(3)*(sp.sqrt(3)/2)*sp.Rational(2,3))==1,'eigenvalues 1 (five), 1 +/- 3g/2 (two each); all positive for 0<=g<2/3')
    omega=np.array([.3,1.,1.002]); w2=omega[:,None]**2
    target=np.tile([1.,0.,0.],(3,1))
    ts=np.linspace(0,600,3001)
    for g,gamma,chirality in [(.0002,.04,1),(.0002,.04,-1),(.002,.04,1),(.002,.04,-1),(.002,0.,1)]:
        coupling=math.sqrt(3)*g/2
        z0=target.copy(); z0[1,1]=.5; z0[2,2]=.5*chirality
        def rhs(t,y):
            zz=y[:9].reshape(3,3); dz=y[9:18].reshape(3,3)
            dd=-w2*(zz-target+coupling*crosses(zz))-gamma*dz
            sink=gamma*float(np.sum(dz*dz/w2))
            return np.r_[dz.ravel(),dd.ravel(),sink]
        sol=solve_ivp(rhs,(0,600),np.r_[z0.ravel(),np.zeros(10)],t_eval=ts,method='DOP853',rtol=1e-9,atol=1e-12)
        zz=sol.y[:9].reshape(3,3,-1); dz=sol.y[9:18].reshape(3,3,-1)
        potential=.5*np.sum((zz-target[:,:,None])**2,axis=(0,1))+coupling*np.einsum('it,it->t',zz[0],np.cross(zz[1].T,zz[2].T).T)
        kinetic=.5*np.sum(dz*dz/w2[:,:,None],axis=(0,1))
        energy=kinetic+potential; budget=energy+sol.y[18]
        drift=float(np.max(np.abs(budget-budget[0]))/abs(budget[0]))
        last=ts>=400
        avg=float(np.trapz(1-zz[:,0,last].sum(axis=0)/3,ts[last])/(ts[last][-1]-ts[last][0]))
        displacement=float(np.linalg.norm(zz[:,:,-1]-target))
        transverse=float(np.linalg.norm(zz[:,1:,-1]))
        row=dict(g=g,gamma=gamma,chirality=chirality,initial_energy=float(energy[0]),final_energy=float(energy[-1]),sink=float(sol.y[18,-1]),budget_relative_drift=drift,final_displacement=displacement,final_transverse=transverse,late_mean_D_over_g=avg,completed=sol.success)
        rows.append(row)
        check(f'energy_budget_{g}_{gamma}_{chirality}',sol.success and drift<2e-7,str(row))
        if gamma:
            check(f'damped_aligned_limit_{g}_{chirality}',displacement<2e-5 and abs(avg)<1e-8,'passive damping removes the seeded transverse response in the tested local basin')
            # Norm-one energy barrier: V >= (1-sqrt(3)|c|)/2-|c|/(3sqrt(3)).
            barrier=(1-math.sqrt(3)*abs(coupling))/2-abs(coupling)/(3*math.sqrt(3))
            convex_bound=1-4*abs(coupling)
            check(f'local_basin_bound_{g}_{chirality}',energy[0]<barrier and convex_bound>0,f'initial E={energy[0]:.8g}<norm-one barrier {barrier:.8g}; Hessian lower bound in ball {convex_bound:.8g}')
        else:
            check('conservative_motion_retains_excitation',abs(energy[-1]/energy[0]-1)<2e-7 and transverse>.1,'closed Hamiltonian has no dissipative attractor selecting one oscillator energy')
    data=dict(checks=checks,rows=rows,symbolic_characteristic=str(characteristic),
              bounds=dict(omega=omega.tolist(),time=[0,600],late_average=[400,600],samples=3001,rtol=1e-9,atol=1e-12),
              verdict='Weak local fields do not spontaneously destabilize the aligned state; passive damping erases coherent response. A pump/state-selection mechanism remains necessary.',
              non_claims=['No complete action','No full nonlinear field stability','Cubic potential is unbounded globally; only a declared local basin is used','Damping sink is recorded but bath dynamics are absent','No 32pi derivation'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not t['passed'] for t in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; common theory and coefficient OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
