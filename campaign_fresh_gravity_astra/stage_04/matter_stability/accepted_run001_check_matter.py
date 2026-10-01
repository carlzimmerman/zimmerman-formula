"""Bounded direct-ODE/eigenvalue audit of the coupled-fluid derivation.

No imports from parent campaign code; no empirical data or theory search.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp


def eigenvalues(kernel,u):
    if kernel=='Q':
        return math.sqrt(u/(u+1)),2*math.sqrt(u*u+u)/(2*u+1)
    t=math.sqrt(u); d=-math.expm1(-t)
    return d,d*d/(d-.5*t*math.exp(-t))


def roots(k,L,K,cs2,c=1.,Crho=1.):
    tau=K/(c*c); s=cs2*k*k; A=L*k*k/tau
    J=Crho*k*k/tau
    plus=.5*(A+s+math.hypot(A-s,2*math.sqrt(J)))
    # Product/large root avoids catastrophic cancellation in the slow branch.
    product=k*k/tau*(cs2*L*k*k-Crho)
    minus=product/plus
    return minus,plus


def real_operator(k,L,K,cs2,c=1.,C=1.,rho=1.):
    tau=K/(c*c)
    return np.array([[0,-rho*k,0,0],
                     [cs2*k/rho,0,k,0],
                     [0,0,0,1],
                     [-C/tau,0,-L*k*k/tau,0]],float)


def energy(y,k,L,K,cs2,c=1.,C=1.,rho=1.):
    D,V,Psi,Pi=y
    pieces=np.array([rho*V*V,cs2*D*D/rho,K/(c*c)*Pi*Pi/C,
                     L*k*k*Psi*Psi/C,2*D*Psi])/4
    return np.sum(pieces,axis=0),np.sum(abs(pieces),axis=0)


def main(out):
    scan=[]; maximum_companion_error=0.; maximum_energy_derivative=0.
    for kernel in ['Q','R']:
        for u in [1e-4,.01,1,100]:
            perp,parallel=eigenvalues(kernel,u)
            assert parallel>perp>0
            for angle in [0,math.pi/4,math.pi/2]:
                L=perp*math.sin(angle)**2+parallel*math.cos(angle)**2
                for K in [2.,8.]:
                    for cs2 in [.001**2,.2**2]:
                        kJ=1/math.sqrt(L*cs2)
                        for ratio in [.01,.3,.9,1.,1.1,3.,100.]:
                            k=ratio*kJ; lower,upper=roots(k,L,K,cs2)
                            # Independent eigenvalues of the four first-order
                            # physical equations, not the two-root polynomial.
                            op=real_operator(k,L,K,cs2)
                            eig=np.linalg.eigvals(op)
                            candidates=-eig*eig
                            scale=max(1.,abs(lower),abs(upper))
                            err=max(min(abs(z-lower),abs(z-upper))/scale for z in candidates)
                            assert err<2e-12
                            maximum_companion_error=max(maximum_companion_error,float(err))
                            if ratio<1:
                                assert lower<0 and upper>0
                                assert -lower<1/L-cs2*k*k
                            elif ratio>1: assert lower>0 and upper>0
                            else: assert abs(lower)<1e-11/L
                            # Quadratic energy derivative at a nonmodal state.
                            y=np.array([.2,-.1,.3,-.4]);dy=op@y
                            D,V,Psi,Pi=y
                            gradient=np.array([cs2*D/2+Psi/2,V/2,L*k*k*Psi/2+D/2,K*Pi/2])
                            edot=float(gradient@dy)
                            denom=max(1.,float(np.sum(abs(gradient*dy))))
                            edot_relative=abs(edot)/denom
                            assert edot_relative<2e-14
                            maximum_energy_derivative=max(maximum_energy_derivative,edot_relative)
                            Ktrace=L/((upper+lower)/(k*k)-cs2)
                            assert abs(Ktrace/K-1)<2e-10
                            scan.append(dict(kernel=kernel,u=u,theta=angle,K=K,cs2=cs2,k_over_kJ=ratio,
                                             lambda_eff=L,kJ=kJ,omega2_low=lower,omega2_high=upper))
    # Discriminating direct integrations: growing and oscillatory coupled modes,
    # both Q/R and K=2/8; field-only stability is the deliberately false proxy.
    evolution=[]
    for kernel in ['Q','R']:
        L=eigenvalues(kernel,.1)[1];cs2=.04;kJ=1/math.sqrt(L*cs2)
        for K in [2.,8.]:
            for ratio in [.5,2.]:
                k=ratio*kJ;lower,upper=roots(k,L,K,cs2)
                op=real_operator(k,L,K,cs2)
                # Start with a slow-branch density eigenmode, zero velocities.
                # D=1; scalar relation is independently read from fluid equation.
                psi=(lower-cs2*k*k)/(k*k)
                y0=np.array([1.,0.,psi,0.])
                characteristic=math.sqrt(abs(lower))
                end=(4 if lower<0 else 4*math.pi)/characteristic
                times=np.linspace(0,end,401)
                sol=solve_ivp(lambda t,y:op@y,[0,end],y0,method='DOP853',t_eval=times,
                              rtol=2e-11,atol=1e-12,max_step=end/300)
                assert sol.success
                expected=np.cosh(characteristic*times) if lower<0 else np.cos(characteristic*times)
                trajectory_error=float(max(abs(sol.y[0]-expected))/max(1.,max(abs(expected))))
                assert trajectory_error<2e-8
                energies,terms=energy(sol.y,k,L,K,cs2)
                energy_error=float(max(abs(energies-energies[0]))/max(1.,max(terms)))
                assert energy_error<2e-10
                # Inversion from just this branch with calibrated rho and cs.
                x=lower
                Ksingle=k*k*(L*(x-cs2*k*k)+1)/(x*(x-cs2*k*k))
                assert abs(Ksingle/K-1)<2e-11
                evolution.append(dict(kernel=kernel,K=K,k_over_kJ=ratio,lambda_eff=L,
                                      coupled_omega2_low=lower,coupled_omega2_high=upper,
                                      field_only_omega2=L*k*k/K,
                                      trajectory_max_scaled_error=trajectory_error,
                                      energy_max_scaled_drift=energy_error,
                                      recovered_K_single_mode=Ksingle,
                                      duration=end,initial_energy=float(energies[0])))
    # Isolate limiting/degenerate cases: pressureless bounded high-k growth,
    # negative-compressibility high-k growth, and resonant principal speeds.
    L=eigenvalues('Q',.1)[1]; K=2.; v2=L/K
    edge=[]
    for cs2,label in [(0.,'pressureless'),(-.04,'negative_compressibility'),(v2,'equal_principal_speeds')]:
        values=[]
        for k in [1,10,100,1000,10000]:
            lo,hi=roots(k,L,K,cs2)
            values.append(dict(k=k,low=lo,high=hi,growth=math.sqrt(max(0,-lo))))
        if cs2==0:
            assert abs(values[-1]['low']/(-1/L)-1)<1e-6
        elif cs2<0:
            assert abs(values[-1]['growth']/(math.sqrt(-cs2)*1e4)-1)<1e-6
        else:
            assert values[-1]['low']>0
            for row in values:
                exact=v2*row['k']**2-row['k']/math.sqrt(K)
                assert abs(row['low']-exact)<1e-8*max(1,abs(exact))
        edge.append(dict(case=label,cs2=cs2,values=values))
    # Dynamic-data sensitivity: dimensional inputs are deliberately synthetic.
    G=6.67430e-11;c=299792458.;rho=1e-21;cs=1e5;B=1e-12
    KPC=3.085677581491367e19;MYR=365.25*86400*1e6;E3=math.sqrt(.315*64+.685)
    dimensional=[]
    for name,a0 in [('canonical',9.3619e-11),('alternative',1.1279e-10)]:
        for scaling,factor in [('vacuum',1.),('frozen_H_z3',E3)]:
            a=a0*factor
            for kernel in ['Q','R']:
                L=eigenvalues(kernel,B/a)[1]
                kJ=math.sqrt(4*math.pi*G*rho/(cs*cs*L));k=.5*kJ
                growth=[]
                for K in [2.,8.]:
                    low,high=roots(k,L,K,cs*cs,c,4*math.pi*G*rho)
                    growth.append(dict(K=K,growth_rate_per_second=math.sqrt(-low),
                                       efold_Myr=1/math.sqrt(-low)/MYR,
                                       scalar_principal_speed_over_c=math.sqrt(L/K)))
                relative=growth[1]['growth_rate_per_second']/growth[0]['growth_rate_per_second']-1
                assert relative<0
                dimensional.append(dict(normalization=name,scaling=scaling,kernel=kernel,a=a,B=B,
                    rho_kg_m3=rho,sound_speed_m_s=cs,theta=0,lambda_eff=L,
                    threshold_wavelength_kpc=2*math.pi/kJ/KPC,
                    growth_at_k_over_kJ=.5,models=growth,K8_over_K2_growth_minus_one=relative))
    # Check monotone rate suppression with K on a resolved representative.
    monotone=[];L=eigenvalues('Q',.1)[1];cs2=.04;k=.5/math.sqrt(L*cs2)
    for K in [1e-4,.01,1,2,8,1e2,1e4]:
        lo,_=roots(k,L,K,cs2);monotone.append(dict(K=K,gamma2=-lo))
    assert all(monotone[i+1]['gamma2']<monotone[i]['gamma2'] for i in range(len(monotone)-1))
    result=dict(scan_count=len(scan),scan=scan,maximum_companion_scaled_error=maximum_companion_error,
                maximum_energy_derivative_scaled_error=maximum_energy_derivative,
                direct_evolution=evolution,edge_controls=edge,dimensional_sensitivity=dimensional,
                monotone_K_growth=monotone,
                first_test_verdict='Positive field-only energy fails to imply coupled stability: every k/kJ=.5 evolution grows.',
                nonclaims=['No global unsupplemented homogeneous background or cosmological perturbations.',
                           'No observational constraints or calibration for K.',
                           'Finite binary64 checks are not interval-certified universal proofs.'])
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(scan_count=len(scan),evolution_cases=len(evolution),
        companion_error=maximum_companion_error,
        largest_trajectory_error=max(x['trajectory_max_scaled_error'] for x in evolution),
        largest_energy_drift=max(x['energy_max_scaled_drift'] for x in evolution),
        dimensional_cases=len(dimensional)),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    main(parser.parse_args().out)
