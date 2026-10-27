import argparse,json
from pathlib import Path
from evolve import evolve,Radial
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--n',type=int,default=256);p.add_argument('--amp',type=float,default=.05);p.add_argument('--zend',type=float,default=10);p.add_argument('--gamma',type=float,default=5/3);p.add_argument('--xe',type=float,default=2e-4);p.add_argument('--baryon-ratio',type=float,default=1);p.add_argument('--cfl',type=float,default=.6);p.add_argument('--no-pressure',action='store_true');a=p.parse_args()
Radial.gamma=a.gamma;Radial.xe=a.xe;Radial.baryon_ratio=a.baryon_ratio;Radial.pressure=not a.no_pressure
r=evolve(n=a.n,amp=a.amp,zend=a.zend,cfl=a.cfl);r['checks']=[dict(name='endpoint_without_gas_crossing',passed=r['reason']=='endpoint'),dict(name='static_residual',passed=max(r['initial_residuals'])<1e-5,value=max(r['initial_residuals'])),dict(name='work_balance',passed=r['max_work_error']<.005,value=r['max_work_error'])];Path(a.output).write_text(json.dumps(r,indent=2,default=lambda x:x.item())+'\n')
