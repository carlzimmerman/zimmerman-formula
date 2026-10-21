"""Evolve pre-audited clean Cauchy data with the unchanged FV equations."""
from pathlib import Path
import sys,json,subprocess,resource,time
case_path,out=map(Path,sys.argv[1:3]);case=json.loads(case_path.read_text())
here=Path(__file__).resolve().parent;root=here.parents[1]
e=case['evolution'];d=out/'evolution';d.mkdir();start=time.monotonic()
seed=root/case['seed'];binary=here/'pair_axisym_seed'
argv=[str(binary),str(here/'profile_Q80000.bin'),str(d),str(e['nr']),str(e['nz']),str(e['dx']),
      str(e['dt']),str(e['T']),'0','0','0',str(case['omega']),'snapshot',str(e['snapshot_interval']),'0',str(seed)]
proc=subprocess.run(argv,capture_output=True,text=True)
(d/'solver_stdout.txt').write_text(proc.stdout);(d/'solver_stderr.txt').write_text(proc.stderr)
if proc.returncode:raise RuntimeError('seed solver failed: '+proc.stderr)
row=json.loads(proc.stdout);checks=[]
def ck(name,value):checks.append({'name':name,'pass':bool(value)})
ck('global energy conserved',row['max_relative_E_change']<case['bounds']['E_relative_max'])
ck('global charge conserved',row['max_relative_Q_change']<case['bounds']['Q_relative_max'])
ck('solver RAM below1GB',row['peak_rss_macos_bytes']<1000000000)
ck('t0 snapshot loads byte-identically',(d/'snap_t000000000.bin').read_bytes()==seed.read_bytes())
ee=[json.loads(x) for x in (d/'enclosed_energy.jsonl').read_text().splitlines()]
ck('positive-face energy identity',max(abs(x['relative_face_identity_error']) for x in ee)<1e-10)
audit=json.loads((root/case['seed_audit']).read_text())
ar=next(x for x in audit['rows'] if x['nominal_K']==case['nominal_K'])
ck('initial Q agrees independently audited seed',abs(row['initial_Q']-ar['Q_actual'])/abs(row['initial_Q'])<1e-10)
ck('initial E agrees independently audited seed',abs(row['initial_E']-ar['E_laplacian'])/abs(row['initial_E'])<1e-10)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('driver RAM below1GB',rss<1000000000)
result={'scope':'Clean finite-amplitude Cauchy data comparison, not a fixed-charge nonlinear normal mode or merger/capture law',
        'case':case,'rows':[dict(row,argv=argv)],'checks':checks,'all_checks_pass':all(x['pass'] for x in checks),
        'n_checks':len(checks),'driver_peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'non_claims':['No derived DC profile or nonlinear frequency dressing','Raw perturbation changes total charge at quadratic order; actual Q is retained',
                      'No four-dwarf mass/profile/population/stellar-heating closure','No orbital angular momentum: m0 axisymmetry']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(row),flush=True)
raise SystemExit(0 if result['all_checks_pass'] else 1)
