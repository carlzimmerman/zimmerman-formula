import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from atomic import Atom, HC, LIGHT, parcel

G=4.30091e-6  # kpc (km/s)^2 / Msun
KPC=3.085677581491367e21
MSUN=1.98847e33
EV_MASS=1.782661921e-33  # grams per eV/c^2
ETA=5.364
PROFILES=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)]
AGE=10e9*365.25*86400


def environment(atom,M,b):
    n=3*ETA*M*MSUN/(4*math.pi*(b*KPC)**3*(atom.mX+atom.mC)*EV_MASS)
    v2=G*(1+ETA)*M/b
    T=(atom.mX+atom.mC)*v2/(6*(LIGHT/1e5)**2)
    return n,T


def main(output):
    hydrogen=Atom(1/137.035999084,510998.95,938272088.16)
    a=Atom(.01,1e6,1e7)
    balance=[]; speed_checks=[]
    for theta in (.05,.1,.3,1.,3.,10.):
        T=theta*a.binding;rec=a.recombination(T,T)[0];beta=a.photo_rate(T)[0]
        balance.append(dict(theta=theta,ratio=beta/(rec*a.saha(T))))
        # Separate speed-space Maxwell integral, no use of the reduced J kernel.
        norm=a.threshold*LIGHT
        def integrand(u):
            if u==0 or u>27:return 0.
            return 4/math.sqrt(math.pi)*u**3*math.exp(-u*u)*math.sqrt(2*T/a.mu)*a.capture(T*u*u)/a.threshold
        direct=quad(integrand,0,27,epsabs=1e-12,epsrel=1e-9)[0]*norm
        speed_checks.append(dict(theta=theta,ratio=direct/a.recombination(T)[0]))
    parcels=[]
    for theta in (.01,.1,1.,10.):
        r=parcel(a,theta,10.,1e-8);fine=parcel(a,theta,10.,1e-10)
        r['refined']=fine
        r['refinement_bound_difference']=abs(r['bound_fraction']-fine['bound_fraction'])
        parcels.append(r)
    # Explicit common-flow invariance for a pair at the same spatial point.
    vx=np.array([.0002,-.0003,.0001]);vc=np.array([-.0001,.0004,.0002])
    boost=np.cross(np.array([.0001,.0003,-.0002]),np.array([2.,-1.,3.]))
    E=.5*a.mu*np.dot(vc-vx,vc-vx)
    Eb=.5*a.mu*np.dot((vc+boost)-(vx+boost),(vc+boost)-(vx+boost))
    boost_ratio=a.capture(Eb)*math.sqrt(Eb)/(a.capture(E)*math.sqrt(E))

    alpha_values=np.geomspace(1e-4,.1,61);mass_values=np.geomspace(1e3,1e9,31)
    rows=[];ratios=[]
    for alpha in alpha_values:
        base=Atom(float(alpha),1e6,1e7)
        basic=[]
        for M,b in PROFILES:
            n,T=environment(base,M,b);k=base.recombination(T)[0]
            basic.append((n,T,k))
        exposures=np.array([n*k*AGE for n,T,k in basic])
        ratios.append(dict(alpha=float(alpha),disk_over_others=(exposures[2]/exposures[[0,1,3]]).tolist()))
        for mC in mass_values:
            scale=float(mC/1e6);atom=Atom(float(alpha),float(mC),float(10*mC))
            ex=exposures/scale**3
            bound=ex/(1+ex)
            opacity=[];dilution=[];nonrel=[];degeneracy=[]
            for (M,b),(n,T,k) in zip(PROFILES,basic):
                ns=n/scale;Ts=T*scale
                opacity.append(ns*b*KPC*atom.threshold)
                dilution.append(ns*atom.radius**3)
                nonrel.append(Ts/atom.mu)
                degeneracy.append(ns*(2*math.pi*HC**2/(atom.mu*Ts))**1.5)
            success=bool(bound[2]>=.8 and np.max(bound[[0,1,3]])<=.2)
            rows.append(dict(alpha=float(alpha),mC_eV=float(mC),binding_eV=atom.binding,
                             bound_fractions=bound.tolist(),exposures=ex.tolist(),
                             all_neutral_threshold_opacity=opacity,
                             n_aD_cubed=dilution,degeneracy=degeneracy,T_over_mu=nonrel,
                             target_met=success))
    max_ratio=np.max([r['disk_over_others'] for r in ratios],axis=0)
    summary=dict(parameter_points=len(rows),profile_evaluations=4*len(rows),
                 targets_met=sum(r['target_met'] for r in rows),
                 max_disk_over_others=max_ratio.tolist(),other_profile_indices=[0,1,3],
                 max_disk_fraction_if_each_other_below_point2=(max_ratio/(4+max_ratio)).tolist(),
                 max_balance_error=max(abs(r['ratio']-1) for r in balance),
                 max_speed_quadrature_error=max(abs(r['ratio']-1) for r in speed_checks),
                 max_parcel_energy_error=max(max(r['max_energy_error'],r['refined']['max_energy_error']) for r in parcels),
                 max_parcel_refinement_difference=max(r['refinement_bound_difference'] for r in parcels),
                 boost_rate_ratio=boost_ratio,
                 max_T_over_mu=max(max(r['T_over_mu']) for r in rows),
                 all_profiles_opacity_below_point1=sum(max(r['all_neutral_threshold_opacity'])<.1 for r in rows))
    assert len(rows)==1891 and summary['max_balance_error']<2e-7
    assert summary['max_speed_quadrature_error']<2e-7
    assert summary['max_parcel_energy_error']<1e-7
    assert summary['max_parcel_refinement_difference']<2e-7
    assert abs(boost_ratio-1)<1e-12
    data=dict(summary=summary,conventions='radiative ground-state subsystem; fixed-T screen is not live gravity',
              profiles=[dict(index=i,mass_Msun=M,b_kpc=b) for i,(M,b) in enumerate(PROFILES)],
              hydrogen=dict(binding_eV=hydrogen.binding,threshold_cm2=hydrogen.threshold),
              balance=balance,speed_quadrature=speed_checks,parcels=parcels,ratios=ratios,scan=rows)
    Path(output).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    main(args.output)
