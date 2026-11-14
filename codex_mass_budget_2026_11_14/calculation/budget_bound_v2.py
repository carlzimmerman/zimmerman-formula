#!/usr/bin/env python3
"""Exact raw-law charge bound on 64 representative actual halo profiles."""
import argparse
import contextlib
import csv
import io
import json
import math
import os
from pathlib import Path
import sys

for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
sys.dont_write_bytecode=True
import numpy as np
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'codex_mass_budget_2026_11_14/calculation/run_001'
JPATH=ROOT/'closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_hm.py'
INDICES=(0,80,120,160,200,240,280,320)


def cold(b,r,a0,G):
    if b==0:return 0.0
    t=a0*b*r*r/G
    return 2*t/(math.sqrt(b*b+4*t)+b)


def run(out):
    code=JPATH.read_text();sys.path.insert(0,str(JPATH.parent))
    J={'__file__':str(JPATH),'__name__':'jnt2_budget_bound'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code[:code.index('\nP(f"JNT2 G1')],str(JPATH),'exec'),J)
    Z,F,L=J['Z'],J['F'],J['L'];h,FB=F['h'],F['FB']
    G=F['G']*1000
    A0={foot:L['A0'][foot]*L['MPC']/1e9 for foot in Z['FOOTS']}
    stored=np.load(BASE/'representative_profiles.npz')
    rows=[];max_source_deviation=0;max_root_equivalence=0;max_budget_residual=0;max_closed_root_difference=0
    for z in (0.0,2.2,3.0,4.4):
        J['setz'](z)
        for foot in Z['FOOTS']:
            a0=A0[foot]
            for idx in INDICES:
                hb=L['HB'][idx];regime=Z['regime'](hb,foot)
                Q=(1-FB)*hb['Mta']/h
                Rta=hb['rta']*1000/(h*(1+z))
                Mb=Z['Mb_fold'](hb,foot)/h
                rcom=lambda R:R*h*(1+z)/1000
                bar=lambda R:float(Z['Bar'](hb,foot,np.array([rcom(R)]))[0])/h
                source=lambda R:Mb if regime=='galaxy' else bar(R)
                saved=stored[f'{foot}_z{z:g}_f3_i{idx}']
                for col,fn in ((1,source),(2,bar)):
                    vals=np.array([fn(r*1000/(h*(1+z))) for r in saved[:,0]])
                    max_source_deviation=max(max_source_deviation,float(np.max(abs(vals-saved[:,col]/h))/Q))
                for convention,bfun in (('FRZ1_retained_source',source),('all_explicit_Bar',bar)):
                    endcold=cold(bfun(Rta),Rta,a0,G)
                    has_cross=endcold>=Q
                    root=None;closed=None
                    if has_cross:
                        root=brentq(lambda r:cold(bfun(r),r,a0,G)/Q-1,0,Rta,xtol=1e-11,rtol=1e-13)
                        other=brentq(lambda r:(a0*bfun(r)*r*r/G-Q*(Q+bfun(r)))/(Q*Q),0,Rta,xtol=1e-11,rtol=1e-13)
                        max_root_equivalence=max(max_root_equivalence,abs(root-other)/root)
                        max_budget_residual=max(max_budget_residual,abs(cold(bfun(root),root,a0,G)/Q-1))
                        assert cold(bfun(root*.99),root*.99,a0,G)<Q
                        if root*1.01<=Rta:assert cold(bfun(root*1.01),root*1.01,a0,G)>Q
                    if convention=='FRZ1_retained_source' and regime=='galaxy':
                        closed=math.sqrt(G*Q*(Q+Mb)/(a0*Mb))
                        if root is not None:max_closed_root_difference=max(max_closed_root_difference,abs(root/closed-1))
                        else:assert closed>Rta
                    rr=np.linspace(0,Rta,1001)
                    bb=np.array([bfun(r) for r in rr]);cc=np.array([cold(b,r,a0,G) for b,r in zip(bb,rr)])
                    assert np.min(np.diff(bb))>=-1e-12*Q
                    assert np.min(np.diff(cc))>=-1e-12*Q
                    assert np.array_equal(cc<=Q,(a0*bb*rr*rr/G)<=Q*(Q+bb))
                    radii={f:Z['rset_com'](hb,foot,z,f)*1000/(h*(1+z)) for f in (1.25,2.0,3.0,5.0)}
                    row=dict(z=z,foot=foot,grid_index=idx,M200m_Msun_h=hb['M'],regime=regime,
                        split_reference=bool(J['above'](hb,foot)),source_convention=convention,
                        Mb_fold_Msun=Mb,cosmic_patch_cold_Msun=Q,rta_kpc=Rta,
                        C_exact_at_rta_over_Q=endcold/Q,has_crossing_inside_patch=has_cross,
                        R_budget_crossing_kpc=root,R_budget_fixed_source_unrestricted_kpc=closed,
                        max_allowed_radius_inside_patch_kpc=root if root is not None else Rta)
                    for f,R in radii.items():
                        tag=f'{f:g}'
                        row['Rset_f'+tag+'_kpc']=R
                        row['raw_demand_over_Q_f'+tag]=cold(bfun(R),R,a0,G)/Q
                        row['budget_permits_f'+tag]=cold(bfun(R),R,a0,G)<=Q*(1+1e-12)
                    rows.append({k: v.item() if isinstance(v, np.generic) else v for k,v in row.items()})
    assert len(rows)==128
    assert max_source_deviation<1e-12
    assert max_root_equivalence<1e-10
    assert max_budget_residual<1e-10
    assert max_closed_root_difference<1e-10
    # Zero source is a valid degenerate case: it requires no cold charge.
    assert cold(0,1e6,A0['canonical'],G)==0
    out.mkdir(parents=True,exist_ok=True)
    with (out/'budget_bounds.csv').open('w',newline='') as file:
        writer=csv.DictWriter(file,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result=dict(assertion_tested='Raw-law charge bound and first crossing on 64 representative actual halo profiles, two explicit source conventions; no physical switching rule inferred.',
        scope=dict(z=[0,2.2,3,4.4],footings=list(Z['FOOTS']),indices=list(INDICES),distinct_halos=64,source_convention_rows=128,monotonicity_nodes_per_row=1001),
        checks=dict(max_source_difference_vs_saved_profiles_relative_Q=max_source_deviation,
            max_two_root_formulations_relative_difference=max_root_equivalence,max_root_charge_relative_residual=max_budget_residual,
            max_closed_point_source_radius_relative_difference=max_closed_root_difference,zero_source_check=True),
        rows=rows,non_claims=['Representative profiles only, not the full 321-mass grid','No adoption of min(R_caustic,R_budget) as a derived settling model','A budget bound does not establish a static solution, stability or formation','Cluster all_explicit_Bar omits baryons in outer envelope as in actual code'])
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result['checks'],indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
