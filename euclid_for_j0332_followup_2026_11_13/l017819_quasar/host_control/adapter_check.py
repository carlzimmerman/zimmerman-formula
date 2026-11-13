from pathlib import Path
import json,numpy as np
from arbitrary_field_adapter import FieldAdapter
from fit_host_v4 import Host,sie_deflection
B=Path(__file__).resolve().parent;r=json.loads((B/'run_04/result.json').read_text())['chosen'];p=np.array(r['params']);h=Host();lp=h.startlight.copy();lp[2:6]=p[:4];a=FieldAdapter(lp);cx,cy=h.masscenter
fn=lambda X,N:sie_deflection(X,N,p[4],p[5],p[6],cx,cy,0,0)
x=h.run(p,True);y=a.evaluate(fn,p[7]);err=float(np.max(abs(x['model']-y['model'])));assert err<1e-12;assert abs(x['score']-y['score'])<1e-9
out=B/'adapter_validation_01';out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps({'max_model_abs_difference':err,'score_difference':y['score']-x['score'],'light_parameters':lp.tolist(),'quasar_A':a.A.tolist(),'quasar_B':a.C.tolist(),'mass_center':list(h.masscenter),'source_grid':{'ns':a.ns,'h':a.h,'supersample':a.ss}},indent=2))
