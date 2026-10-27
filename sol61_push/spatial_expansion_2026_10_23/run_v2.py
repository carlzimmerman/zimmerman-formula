import argparse,json
from pathlib import Path
from model import evolve
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--n',type=int,default=8);p.add_argument('--amp',type=float,default=.001);p.add_argument('--zi',type=float,default=1100);p.add_argument('--zend',type=float,default=10);p.add_argument('--cfl',type=float,default=.6);a=p.parse_args();r=evolve(a.n,a.amp,a.zi,a.zend,a.cfl);r['checks']=[dict(name='reaches_target',passed=r['reason']=='endpoint'),dict(name='static_residual',passed=max(r['initial_residuals'])<1e-5,value=max(r['initial_residuals'])),dict(name='work_balance',passed=r['max_work_error']<.01,value=r['max_work_error'])];Path(a.output).write_text(json.dumps(r,indent=2,default=lambda x:x.item())+'\n')
