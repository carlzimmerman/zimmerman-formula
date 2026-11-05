#!/usr/bin/env python3
"""Fifteen-key identity and native-input availability; no shear prediction."""
import argparse,ast,json
from pathlib import Path
import numpy as np
from astropy.io import fits
import audit_inputs as A
EXPECTED=['G-IN-all',*[f'G-MID-T{i}' for i in (1,2,3)],'G-MID-b','G-OUT-all',*[f'G-OUT-T{i}' for i in (1,2,3)],'G-OUT-b','G-OUT-Mall',*[f'G-OUT-M{i}' for i in (1,2,3)],'G-IN-Mall']

def admissible(evidence,selector,mutate=False):
    needed=['native_geometry','raw_baryon_profile','prediction_rule']+(['mean_flow'] if selector=='I2' else [])
    return True if mutate else all(evidence.get(k,False) for k in needed)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutate',action='store_true');args=parser.parse_args();checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    source=A.ROOT/'rebuild_2026_10_22/BA1_joint_shear_statistic/ba1_worker_tail.py'
    node=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='_keys')
    # Isolated key definition only; no top-level bootstrap, imports or old drivers.
    I=np.arange(6);groups=np.repeat(np.arange(3),2);X=np.column_stack([np.ones(6),np.arange(6)-2.5])
    def wls(W,design,n,d):
        rows=[]
        for weight in W:
            rows.append(np.linalg.lstsq(design*np.sqrt(weight*d)[:,None],n/d*np.sqrt(weight*d),rcond=None)[0])
        return np.array(rows)
    ns=dict(np=np,BN=['INNER','MID','OUTER'],I=I,TID=groups,T3M=groups,ALLI=I,X1m=X,_wls=wls,
            _MEAS={('fixture','fixture'):dict(n=np.full((6,3),2.),d=np.ones((6,3)))})
    exec(compile(ast.Module(body=[node],type_ignores=[]),'isolated_BA1_keys','exec'),ns)
    fixture=ns['_keys'](np.ones((1,6)),'fixture','fixture')
    check('exact_fifteen_key_identity',list(fixture)==EXPECTED)
    for key,value in fixture.items():
        target=0. if key.endswith('-b') else 2.
        check('known_fixture_'+key,np.max(abs(value-target))<=1e-12,float(value[0]))
    complete=dict(native_geometry=True,raw_baryon_profile=True,prediction_rule=True,mean_flow=True)
    incomplete=dict(native_geometry=False,raw_baryon_profile=False,prediction_rule=False,mean_flow=False)
    for selector in ('I1','I2'):
        check(selector+'_complete_fixture_accepted',admissible(complete,selector,args.mutate))
        check(selector+'_incomplete_fixture_rejected',not admissible(incomplete,selector,args.mutate))
    catalogue=A.ROOT/'real_research/data/erass1cl_primary_v3.2.fits'
    with fits.open(catalogue,memmap=True,lazy_load_hdus=True) as h:
        schema=[dict(name=c.name,format=c.format,unit=c.unit) for c in h[1].columns]
        nrows=int(h[1].header['NAXIS2'])
    names=[c['name'] for c in schema]
    check('catalogue_summary_columns_present',all(k in names for k in ['MGAS500','R500','KT','F300kpc','F500']))
    files=[Path(__file__).resolve(),source,catalogue,A.HERE/'FROZEN_SHEAR_INPUTS.md',
        A.ROOT/'rebuild_2026_10_22/F1_cluster_cores/f1_cluster_cores.py',A.ROOT/'rebuild_2026_10_22/X2_cluster_outskirts/x2_cluster_outskirts.py',
        A.ROOT/'rebuild_2026_10_22/X30_sheet_cluster_profile/x30_sheet_cluster_profile.py',
        A.ROOT/'rebuild_2026_10_22/FA1_fresh_action/FROZEN_CRITERIA.md',A.ROOT/'rebuild_2026_10_22/FA1_fresh_action/I2_vorticity/FROZEN_CRITERIA.md']
    evidence={
      'I1':dict(native_geometry=False,raw_baryon_profile=False,prediction_rule=False),
      'I2':dict(native_geometry=False,raw_baryon_profile=False,prediction_rule=True,mean_flow=False)}
    notes=dict(native_geometry='F1 uses measured BAO ratios with HRD/h absolute calibration and an LCDM reference-distance conversion; full native calibration not authenticated here',
      raw_baryon_profile='Audited catalogue supplies aperture summaries and derived MGAS500/R500; X2 inserts beta-model shape and taper. Raw radial reconstruction not established by these inputs',
      I1_prediction_rule='I1 specifies only a non-decreasing F and necessary threshold support, not a unique shear-amplitude prescription',
      I2_prediction_rule='The old I2 system-level on/off reading supplies a conditional uniform1.5-times-law extra mass; this is not a healthy field-theory completion',
      mean_flow='No per-cluster vorticity or rotation-support map is supplied by this chain. The scalar temperature does not measure mean flow; the single-gradient floor fails the separate audit')
    rows=[]
    for selector in ('I1','I2'):
        for foot in ('canonical','alt'):
            ev=evidence[selector];needed=['native_geometry','raw_baryon_profile','prediction_rule']+(['mean_flow'] if selector=='I2' else [])
            missing=[key for key in needed if not ev[key]];ok=admissible(ev,selector,args.mutate)
            for key in EXPECTED:rows.append(dict(selector=selector,footing=foot,key=key,value=None,
                label='UNVERIFIED MUTANT EVALUABILITY' if ok else 'NOT EVALUABLE from audited inputs',missing=missing))
    obj=dict(label='NOT EVALUABLE: audited inputs do not support new selector shear grades' if not args.mutate else 'UNDECIDED: mutated input gate fails controls',
      mutate=args.mutate,checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),keys=EXPECTED,rows=rows,
      evidence=evidence,provenance_notes=notes,catalogue=dict(path=A.relative(catalogue),rows=nrows,schema=schema),
      source_hashes={A.relative(p):A.sha(p) for p in files},scope='Input availability only; not a physical failure or proof of absence elsewhere; Bullet3D remains open; retired sector, adopts nothing; kappa=1/2 FITTED; not theory closed')
    A.atomic(A.HERE/('mutate/shear_inputs.json' if args.mutate else 'shear_inputs.json'),obj)
    print(json.dumps(dict(label=obj['label'],passed=obj['passed'],total=obj['total'],rows=len(rows)),indent=2));return int(obj['passed']!=obj['total'])
if __name__=='__main__':raise SystemExit(main())
