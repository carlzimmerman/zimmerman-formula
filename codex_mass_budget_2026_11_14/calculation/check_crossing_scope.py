#!/usr/bin/env python3
"""Conditional condensed/patch baryon identity, with actual scope bookkeeping."""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'codex_mass_budget_2026_11_14/calculation/run_001'


def run(out):
    FB=json.loads((BASE/'results.json').read_text())['constants']['FB']
    q_grid=1/FB; q_cross=6.41
    G=6.67430e-11; MPC=3.0856775814913673e22
    H0=67.4e3/MPC; OM=0.3153
    A0={'canonical':9.3603e-11,'alt':1.1312e-10}
    bench=[]; error=0
    for foot,a0 in A0.items():
        for z in (0,2.2,3,4.4):
            H=H0*math.sqrt(OM*(1+z)**3+1-OM)
            for eta in (0.05,0.1,0.5,1.0):
                v=eta*a0/(10*q_cross*H)
                mcond=v**4/(G*a0)
                mpatch=(q_cross/eta)*mcond
                virial=(10*G*mpatch*H)**(1/3)
                residual=virial/v-1
                error=max(error,abs(residual))
                bench.append(dict(foot=foot,z=z,eta=eta,v_intersection_kms=v/1000,virial_vs_law_relative=residual))
    assert error<1e-12
    rows=[]
    for r in csv.DictReader((BASE/'halo_masses.csv').open()):
        if float(r['f'])!=1.25:continue
        b=float(r['Mb_fold_Msun_h']); mt=float(r['Mta_Msun_h']); m2=float(r['M200c_Msun_h'])
        vs=float(r['vstar_kms'])
        rows.append(dict(z=float(r['z']),foot=r['foot'],grid_index=int(r['grid_index']),regime=r['regime'],
            split_reference=r['split_reference']=='True',eta_lagrangian=b/(FB*mt),eta_200c=b/(FB*m2),
            Mta_over_condensed_baryon=mt/b,M200c_over_condensed_baryon=m2/b,
            conditional_lagrangian_crossing_ratio_to_JNT2=q_cross*b/mt,
            conditional_200c_crossing_ratio_to_JNT2=q_cross*b/m2,
            conditional_lagrangian_crossing_kms=vs*q_cross*b/mt,
            conditional_200c_crossing_kms=vs*q_cross*b/m2))
    summary=[]
    for z in (0,2.2,3,4.4):
        for foot in A0:
            rr=[r for r in rows if r['z']==z and r['foot']==foot and r['regime']=='galaxy']
            def span(k):return [min(r[k] for r in rr),max(r[k] for r in rr)]
            summary.append(dict(z=z,foot=foot,galaxy_branch_count=len(rr),
                eta_lagrangian=span('eta_lagrangian'),eta_200c=span('eta_200c'),
                conditional_lagrangian_crossing_kms=span('conditional_lagrangian_crossing_kms'),
                conditional_200c_crossing_kms=span('conditional_200c_crossing_kms'),
                conditional_200c_crossing_ratio_to_JNT2=span('conditional_200c_crossing_ratio_to_JNT2')))
    out.mkdir(parents=True,exist_ok=True)
    with (out/'scope_rows.csv').open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (out/'results.json').write_text(json.dumps(dict(q_crossing=q_cross,q_grid=q_grid,benchmarks=bench,
        max_conditional_identity_relative_error=error,actual_scope_rows=len(rows),galaxy_summary=summary,
        nonclaim='These are conditional common-patch/common-radius identities, not replacement switches or dynamical predictions. Actual JNT2 uses M200c speed while galaxy Mb is assigned from Mta, and the FRZ1/JNT2 cosmologies differ slightly.'),indent=2)+'\n')
    print(json.dumps(dict(rows=len(rows),max_conditional_identity_relative_error=error)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
