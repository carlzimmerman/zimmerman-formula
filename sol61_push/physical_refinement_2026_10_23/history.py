import argparse,json
from pathlib import Path
import numpy as np
from radial_v2 import Radial,evolve
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--zi',type=float,default=2200);a=p.parse_args();target=.03;amp=target*1101/(1+a.zi);records=[]
for iteration in range(4):
 r=evolve(256,amp,a.zi,1100,1,.6);m=Radial(256,amp,a.zi,1);x=np.array(r['final']['xc']);k=np.pi/m.R;shape=np.sin(k*m.r);mode=-3*k*np.sum(m.mc*(x-m.r)*shape)/np.sum(m.mc*shape**2);records.append(dict(iteration=iteration,amp=amp,mode=float(mode),residuals=r['initial_residuals'],reason=r['reason'],work=r['max_work_error']))
 if r['reason']!='endpoint' or mode<=0:break
 if abs(mode/target-1)<1e-4:break
 amp*=target/mode
ok=r['reason']=='endpoint' and abs(mode/target-1)<1e-4
if ok:final=evolve(256,amp,a.zi,10,1,.6)
else:final=None
checks=[dict(name='matched_matter_mode_at1100',passed=bool(ok),value=float(mode/target-1))]
if final:checks.extend([dict(name='endpoint',passed=final['reason']=='endpoint'),dict(name='work_balance',passed=final['max_work_error']<.005,value=final['max_work_error'])])
Path(a.output).write_text(json.dumps(dict(checks=checks,shooting=records,matched_amp=amp,warmup_state=r['final'],evolution=final),indent=2,default=lambda x:x.item())+'\n')
