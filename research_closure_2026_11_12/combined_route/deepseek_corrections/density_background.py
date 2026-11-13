#!/usr/bin/env python3
"""Size of signed AQUAL EFE lobes against explicitly named cosmic backgrounds.

Xc=59.5 is interpreted as the asymptotic monopole enhancement, including baryons.
RE is the field-balance radius sqrt(G Mb a0)/(xe*a0), not a fitted settling radius.
Background cold density is Omega_c rho_crit at z=0. No external-field geometry
or a nonnegative cosmological completion is supplied by this calculation.
"""
import argparse
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode=True
from scipy.optimize import brentq
from corrected_core import G,MSUN,KPC,A0,mu_simple,aqual_asymptote


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    lane=Path(__file__).resolve().parent; out=args.output_dir.resolve()
    if lane not in out.parents: raise SystemExit('Output must be inside correction lane')
    out.mkdir(parents=True,exist_ok=True)
    xc=59.5
    xe=brentq(lambda x:aqual_asymptote(x)-xc,.001,.1,xtol=1e-15)
    mue=float(mu_simple(xe)); L=1/(1+xe)
    H0=67.4e3/(1000*KPC); rho_crit=3*H0**2/(8*math.pi*G)
    omega_c=.265; rho_cold=omega_c*rho_crit
    rows=[]
    for footing,a0 in A0.items():
        for mb in [1e9,1e10,1e11]:
            rM=math.sqrt(G*mb*MSUN/a0); rE=rM/xe
            for s in [2.,3.,5.]:
                r=s*rE
                negative=mb*MSUN*L/(4*math.pi*mue*r**3*(1+L)**1.5)
                perturb_max=xe/(mue*s*s)
                rows.append(dict(footing=footing,Mb_msun=mb,r_over_RE=s,RE_kpc=rE/KPC,
                    radius_kpc=r/KPC,rho_equator_kg_m3=-negative,
                    abs_rho_over_critical=negative/rho_crit,abs_rho_over_cosmic_cold=negative/rho_cold,
                    max_internal_over_external=perturb_max,
                    expansion_control='small (~4%)' if perturb_max<.05 else 'marginal; leading asymptote only',
                    uniform_cosmic_cold_offset_nonnegative=bool(rho_cold>=negative)))
    result=dict(Xc_definition='AQUAL far-field monopole M_eff/Mb',Xc=xc,xe=xe,
                y_newtonian=xe*mue,mu_e=mue,L=L,z=0,H0=67.4,Omega_c=omega_c,
                rho_critical_kg_m3=rho_crit,rho_cosmic_cold_kg_m3=rho_cold,
                rows=rows,interpretation='Negative effective source alone is not nonnegative cold rest density. A separate sufficiently positive background can hide the contrast; it must be included dynamically and is not derived here.',
                non_claims=['Not an exact nonlinear solution at 2RE or 3RE','No steady-state conservation flux derived','No uniform mean density determines a vector external field'])
    assert abs(aqual_asymptote(xe)/xc-1)<1e-12
    assert all(row['rho_equator_kg_m3']<0 for row in rows)
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
