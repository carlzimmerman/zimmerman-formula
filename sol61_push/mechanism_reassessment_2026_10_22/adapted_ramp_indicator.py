import json,sys
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
p=Path(__file__).parent;rows=json.load(open(p/'cold_assembly_run/results.json'))['rows'][::-1]
b=np.array([r['beta'] for r in rows]);o=np.array([r['spectra'][-1]['omega'][0] for r in rows]);f=PchipInterpolator(b,o);s=np.linspace(0,1,10001);S=10*s**3-15*s**4+6*s**5;Sd=30*s*s-60*s**3+30*s**4;out=[]
for label,bb,bd in [('linear_beta',.1+.9*S,.9*Sd/100),('reciprocal_beta',1/(10-9*S),9*Sd/(100*(10-9*S)**2))]:
 indicator=abs(f.derivative()(bb)*bd)/f(bb)**2;k=int(indicator.argmax());out.append(dict(ramp=label,T=100,max_indicator=float(indicator[k]),beta_at_max=float(bb[k])))
Path(sys.argv[1]).write_text(json.dumps(dict(rows=out,scope='PCHIP frequency diagnostic from nine equilibria, not a rigorous adiabatic criterion'),indent=2))
