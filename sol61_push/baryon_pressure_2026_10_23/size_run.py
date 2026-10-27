import argparse,json
from pathlib import Path
import hydro_v2
Base=hydro_v2.Hydro
class Small(Base):
 def __init__(self,*args,**kw):kw['size']=.5;super().__init__(*args,**kw)
hydro_v2.Hydro=Small
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();r=hydro_v2.evolve(n=256);r['parameters']['size']=.5;r['checks']=[dict(name='endpoint',passed=r['reason']=='endpoint'),dict(name='work_heat',passed=r['max_work_heat_error']<.005,value=r['max_work_heat_error'])];Path(a.output).write_text(json.dumps(r,indent=2,default=lambda x:x.item())+'\n')
