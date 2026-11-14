#!/usr/bin/env python3
"""Independent physical-unit check of all explicit baryons at the actual join."""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'codex_mass_budget_2026_11_14/calculation/run_001'


def run(out):
    result=json.loads((BASE/'results.json').read_text())
    h=result['constants']['h']
    # Convert exactly the original code's G to kpc units for a separate physical-unit evaluation.
    G=4.30091e-6
    MPC=3.0856775814913673e22
    A0={'canonical':9.3603e-11,'alt':1.1312e-10}
    rows=[]; max_residual_difference=0.0
    for row in csv.DictReader((BASE/'halo_masses.csv').open()):
        z=float(row['z']); f=float(row['f']); foot=row['foot']
        radius=float(row['R_set_nominal_kpc'])
        bar=float(row['Bar_at_R_Msun_h'])/h
        source=float(row['source_baryons_at_R_Msun_h'])/h
        charge=float(row['cosmic_patch_cold_Msun_h'])/h
        cold_final=float(row['FZS1_cold_at_R_Msun_h'])/h
        cold_B=float(row['B_cold_at_R_Msun_h'])/h
        a0=A0[foot]*MPC/1e9  # (km/s)^2 / kpc
        gn=G*bar/radius**2
        glaw=(gn+math.sqrt(gn*gn+4*gn*a0))/2
        cold_needed=glaw*radius**2/G-bar
        gfinal=G*(bar+cold_final)/radius**2
        epsilon=gfinal*gfinal/(gn*(a0+gfinal))-1
        max_residual_difference=max(max_residual_difference,abs(epsilon-float(row['FZS1_force_residual_allbar_at_R'])))
        # Isolate just the cold rescaling, removing the uncondensed baryon component.
        s=float(row['s']); gncore=G*source/radius**2
        core_g=G*(source+s*cold_B)/radius**2
        core_eps=core_g*core_g/(gncore*(a0+core_g))-1
        r_budget=math.sqrt(G*charge*(charge+source)/(source*a0))
        rows.append(dict(z=z,foot=foot,f=f,grid_index=int(row['grid_index']),regime=row['regime'],
            split_reference=row['split_reference']=='True',
            allbar_exact_cold_at_R_Msun_h=cold_needed*h,
            allbar_exact_over_cosmic_patch_cold=cold_needed/charge,
            allbar_exact_over_reference_at_R=cold_needed/(float(row['reference_cold_at_R_Msun_h'])/h),
            full_profile_allbar_epsilon=epsilon,retained_core_plus_scaled_B_epsilon=core_eps,
            point_source_budget_radius_kpc=r_budget,R_set_over_point_source_budget_radius=radius/r_budget))
    assert max_residual_difference<1e-12
    summary=[]
    for z in (0.0,2.2,3.0,4.4):
        for foot in A0:
            for f in (1.25,2.0,3.0,5.0):
                active=[r for r in rows if r['z']==z and r['foot']==foot and r['f']==f and not r['split_reference']]
                def span(k):return [min(r[k] for r in active),max(r[k] for r in active)]
                summary.append(dict(z=z,foot=foot,f=f,n_active=len(active),
                    n_allbar_exact_exceeds_cosmic_charge=sum(r['allbar_exact_over_cosmic_patch_cold']>1+1e-12 for r in active),
                    allbar_exact_over_cosmic_charge=span('allbar_exact_over_cosmic_patch_cold'),
                    allbar_force_epsilon=span('full_profile_allbar_epsilon'),
                    retained_core_plus_scaled_B_epsilon=span('retained_core_plus_scaled_B_epsilon')))
    out.mkdir(parents=True,exist_ok=True)
    with (out/'source_comparisons.csv').open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (out/'results.json').write_text(json.dumps(dict(rows=len(rows),
        units='Physical kpc and Msun used internally; reported masses Msun/h',
        max_physical_vs_comoving_residual_difference=max_residual_difference,
        point_source_radius_nonclaim='Exact for a constant retained central source. Cluster source Bar(r) varies, so radius is a constant-source diagnostic only there.',
        summary=summary),indent=2)+'\n')
    print(json.dumps(dict(rows=len(rows),max_physical_vs_comoving_residual_difference=max_residual_difference)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    run(parser.parse_args().output)
