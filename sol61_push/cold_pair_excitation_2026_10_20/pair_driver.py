"""Bounded controls and same-action axisymmetric evolution driver.

No inferred mode amplitude is called a capture or galaxy prediction.
The enclosing runner creates output directory and pins code/binary/data.
"""
from pathlib import Path
import sys,json,subprocess,resource,time,math
import numpy as np

case_path,out=map(Path,sys.argv[1:3]);case=json.loads(case_path.read_text())
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
checks=[];rows=[];start=time.monotonic()
def ck(n,v):checks.append({'name':n,'pass':bool(v)})
executable=here/'pair_axisym';table=here/'profile_Q80000.bin'
omega=case['omega']
def run(name,c,benchmark=False):
    d=out/name;d.mkdir()
    args=[str(executable),str(table),str(d),str(c['nr']),str(c['nz']),str(c['dx']),str(c['dt']),
          str(c['T']),str(c.get('separation',24)),str(c.get('speed',0)),str(c.get('phase',0)),str(omega),
          c.get('kind','single_static'),str(c.get('snapshot_interval',20)),str(int(benchmark))]
    r=subprocess.run(args,capture_output=True,text=True,check=False)
    (d/'solver_stdout.txt').write_text(r.stdout);(d/'solver_stderr.txt').write_text(r.stderr)
    ck(name+' solver exits successfully',r.returncode==0)
    if r.returncode:raise RuntimeError(name+': '+r.stderr)
    data=json.loads(r.stdout);data.update(name=name,argv=args)
    print(json.dumps({k:v for k,v in data.items() if k!='argv'}),flush=True)
    return data

if case['kind']=='preflight':
    for dx,nr,nz in [(1.,18,36),(.5,36,72)]:
        r=run('gaussian_'+str(dx),dict(nr=nr,nz=nz,dx=dx,dt=.005,T=0),True);rows.append(r)
        ck(r['name']+' weighted selfadjointness',abs(r['weighted_self_adjoint_difference'])<1e-10)
    ck('Gaussian Laplacian refinement second order',rows[1]['benchmark_gaussian_relative_L2']/rows[0]['benchmark_gaussian_relative_L2']<.35)
    for name,c in case['evolutions'].items():
        r=run(name,c);rows.append(r)
        ck(name+' charge conserved',r['max_relative_Q_change']<case['bounds']['Q_relative_max'])
        ck(name+' energy pilot control',r['max_relative_E_change']<case['bounds']['E_relative_max'])
        ck(name+' measured solverRSS below1GB',r['peak_rss_macos_bytes']<1_000_000_000)
    a=next(r for r in rows if r['name']=='iso_dx05_dt005')
    b=next(r for r in rows if r['name']=='iso_dx05_dt0025')
    ck('isolated temporal energy-error refinement',b['max_relative_E_change']/a['max_relative_E_change']<.4)
else:
    r=run('evolution',case['evolution']);rows.append(r)
    ck('charge conserved',r['max_relative_Q_change']<case['bounds']['Q_relative_max'])
    ck('energy evolution control',r['max_relative_E_change']<case['bounds']['E_relative_max'])
    ck('measured solverRSS below1GB',r['peak_rss_macos_bytes']<1_000_000_000)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured driverRSS below1GB',rss<1_000_000_000)
result={'case':case,'rows':rows,'checks':checks,'all_checks_pass':all(x['pass'] for x in checks),
        'n_checks':len(checks),'runtime_seconds':time.monotonic()-start,'driver_peak_rss_bytes_macos':rss,
        'non_claims':['No galactic-velocity capture or four-dwarf fit',
                      'Mode projection conditional on a matched single remnant, not a field-shape label',
                      'Axisymmetry excludes nonzero orbital J, general impact parameters and general fragment cascades',
                      'Closed finite boundaries require time/box convergence and flux bookkeeping']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
