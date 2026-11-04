"""Regrade saved results and validate all existing bounded evidence records."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE/'mw'))
import filtered_model as F
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    out=dict(manifests=[],mw={},solar={},dwarf={},complete=False)
    for p in sorted(HERE.glob('**/manifest.json')):
        if args.output.parent==p.parent:continue
        a=json.loads(p.read_text())
        proc=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],text=True,capture_output=True)
        assert proc.returncode==0,(p,proc.stdout,proc.stderr)
        out['manifests'].append(dict(path=str(p.relative_to(ROOT)),status=a['run']['status'],valid=True))
    read=lambda p:json.loads((HERE/p).read_text())
    scans={k:read('mw/'+k+'/results.json') for k in ['scan_001','refine_001','heat_refine_001','domain_001']}
    score_count=profile_count=0
    for name,scan in scans.items():
        assert scan['complete']
        for c in scan['cases']:
            q=c['score'];re=F.M.C.lines(q['vc'],q['K'],q['K0'],q['vc_Ou'])
            assert all(q[k]==re[k] for k in [*F.M.GATE,'Lh'])
            assert q['all_four']==all(re[k] for k in F.M.GATE)
            assert max(abs(q[k]-re[k]) for k in ['cK','cO','D'])<1e-10
            profile=c['profile_R12'];assert len(profile['z_kpc'])==len(profile['gz'])==149
            assert np.all(np.isfinite(profile['gz']))
            score_count+=1;profile_count+=149
    get=lambda name,c:next(b for b in scans[name]['cases'] if (b['footing'],b['width_kpc'])==(c['footing'],c['width_kpc']))
    changes={}
    for key,actual,prior,limit in [
        ('heat','heat_refine_001','scan_001',.05),
        ('spatial','refine_001','heat_refine_001',.02),
        ('domain','domain_001','heat_refine_001',.001)]:
        rows=[]
        for c in scans[actual]['cases']:
            try:b=get(prior,c)
            except StopIteration:continue
            rel=abs(c['gz_R12_z03']-b['gz_R12_z03'])/max(abs(c['gz_R12_z03']),1)
            assert rel<limit,(key,c['footing'],c['width_kpc'],rel)
            assert np.sign(c['gz_R12_z03'])==np.sign(b['gz_R12_z03'])
            assert c['score']['all_four']==b['score']['all_four']
            rows.append(dict(footing=c['footing'],width=c['width_kpc'],relative_force_change=rel))
        assert rows;changes[key]=rows
    difference_errors=[];table=[]
    for c in scans['refine_001']['cases']:
        err=min(abs(q['gz']-c['gz_R12_z03'])/abs(c['gz_R12_z03']) for q in c['potential_differences'])
        assert err<.005
        assert all(np.sign(q['gz'])==np.sign(c['gz_R12_z03']) for q in c['potential_differences'])
        difference_errors.append(err)
        z=np.array(c['profile_R12']['z_kpc']);gz=np.array(c['profile_R12']['gz']);bad=z[gz<0]
        table.append(dict(footing=c['footing'],width_kpc=c['width_kpc'],gz_point=c['gz_R12_z03'],
            min_sampled_profile_gz=float(gz.min()),outward_sample_band=None if not len(bad) else [float(bad.min()),float(bad.max())],
            primary_pass=c['score']['all_four'],strict_Lh=c['score']['Lh']))
    out['mw']=dict(regraded_rows=score_count,checked_profile_points=profile_count,
        convergence=changes,max_best_potential_difference_error=max(difference_errors),fine_table=table)
    solar=read('solar/run_002/results.json');sv=read('solar/verify_001/results.json')
    assert solar['all_checks_pass'] and sv['all_checks_pass']
    for foot,ff in solar['footings'].items():
        assert len(ff['rows'])==9
        for k,row in ff['rows'].items():
            v=row['fine'];ratio=abs(1.5*v['q_signed']*ff['a0']/ff['rM_m'])/5.2e-27
            assert abs(ratio-v['x_ceiling'])<1e-11
        out['solar'][foot]=dict(crossing_pc=sv['footings'][foot]['crossing']['a_pc'],
            grid_ratios={k:v['fine']['x_ceiling'] for k,v in ff['rows'].items()})
    dwarf=read('dwarf/run_001/results.json');assert dwarf['all_checks_pass']
    assert len(dwarf['summaries'])==36
    for c in dwarf['summaries']:
        assert abs(c['variance']-sum(c[k] for k in ['variance_Newton','variance_A','variance_B']))<1e-10
        passed=c['variance']>0 and abs(np.sqrt(c['variance'])-c['observed_sigma'])<=2*c['observed_error']
        assert passed==c['orientation_averaged_2sigma_screen']
    out['dwarf']=dict(regraded_rows=36,Draco_passes=sum(c['orientation_averaged_2sigma_screen'] for c in dwarf['summaries'] if c['name']=='Draco'))
    pop=read('pass_population/run_001/results.json')
    assert pop['complete'] and pop['all_checks_pass'] and len(pop['cases'])==156
    seen=set();outward=0;primary=0
    for c in pop['cases']:
        key=(c['footing'],c['index'],c['width_kpc']);assert key not in seen;seen.add(key)
        q=c['score'];re=F.M.C.lines(q['vc'],q['K'],q['K0'],q['vc_Ou'])
        assert all(q[k]==re[k] for k in [*F.M.GATE,'Lh'])
        assert q['all_four']==all(re[k] for k in F.M.GATE)
        assert c['outward']==(c['gz_R12_z03']<0)
        assert all(np.sign(v['gz'])==np.sign(c['gz_R12_z03']) for v in c['potential_differences'])
        outward+=c['outward'];primary+=q['all_four']
    out['historical_pass_population']=dict(rows=156,outward=outward,retained_primary_pass_rows=primary,
        coverage='52 historical primary-pass cells at three widths, not 1375 new-action cells or continuous widths')
    out['complete']=True;out['all_checks_pass']=True
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(manifests=len(out['manifests']),mw_rows=score_count,profile_points=profile_count,dwarf_rows=36,all_checks_pass=True)),flush=True)


if __name__=='__main__':main()
