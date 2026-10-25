import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import hashlib,json,pathlib,subprocess,sys,numpy as np
from scipy.integrate import simpson
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];checks=[]
def check(name,value):
 assert value,name
 checks.append(dict(name=name,passed=True))
for f in sorted((P/'runs').glob('*.json')):
 d=json.loads(f.read_text());q=np.load(f.with_suffix('.npz'));h=d['history'];check(f.stem+' source pins',d['inputs_before']==d['inputs_after'] and all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in d['inputs_before'].items()));check(f.stem+' saved norm',abs(np.sum(abs(q['u'])**2)-h[-1]['M'])<1e-11);check(f.stem+' measured RSS under1GB',d['peak_RSS_bytes']<1_000_000_000);check(f.stem+' norm history',max(abs(x['M']/h[0]['M']-1) for x in h)<1e-10)
for row in json.loads((P/'analysis.json').read_text()):
 if row['finite_mass_budget_residual'] is not None:check(row['tag']+' signed finite radial mass balance',row['finite_mass_budget_residual']<1e-10)
a=np.load(P/'runs/draco_v2_128.npz');b=np.load(P/'runs/draco_v2_256.npz');i=np.argmin(abs(a['physical_CDF_r']-1));massrel=abs(a['physical_CDF'][-1,i]/b['physical_CDF'][-1,i]-1);check('Draco T8 radial/time aperture refinement <1%',massrel<.01)
c=np.load(P/'runs/draco_v3_angle.npz');k=np.argmin(abs(c['times']-8));angularCDF=float(np.max(abs(c['physical_CDF'][k]-a['physical_CDF'][-1])));check('Draco T8 angular CDF refinement <1e-5 inventory',angularCDF<1e-5)
x=np.geomspace(1e-6,1e5,20001);virial=simpson(x**4/(1+x*x)**4,x=x);check('Plummer cold virial coefficient pi/32',abs(virial-np.pi/32)<1e-9)
alias=json.loads(subprocess.check_output([sys.executable,str(P/'alias_control.py')],text=True));check('aliasing failure and nf control preserved',abs(alias[0]['torque'])>.01 and abs(alias[1]['torque'])<1e-10)
controls=json.loads((P/'audit_001/checks.json').read_text());check('analytic free flux/wave controls passed',controls['free_control_v2'][-1]['L2_relative']<1e-5 and controls['free_control_v2'][-1]['energy_flux_relative']<.001)
out=dict(checks=checks,count=len(checks),Draco_T8_aperture_relative_difference=massrel,Draco_T8_angular_CDF_difference=angularCDF,alias_control=alias,non_claims=['late escaping energy is not resolved unless its own shell residual/transport test passes','no final bound remnant or evolved stellar survival','not theory closed'])
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(len(checks),'bounded evidence checks passed')
