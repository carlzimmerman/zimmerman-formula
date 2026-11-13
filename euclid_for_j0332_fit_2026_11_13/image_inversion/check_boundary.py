"""Independent continuity reproduction: constant ray map across a source edge."""
import sys,json
import numpy as np
from importlib import import_module
m=import_module(sys.argv[1]);obj=m.setup(nsource=3,source_pixel=1.,source_center=(0.,0.))
pred=[]
for beta in [-1.-1e-7,-1.+1e-7]:
    obj.operator(lambda X,N:(X-beta,N))
    pred.append(float((obj.fullB@np.ones(9)).reshape(100,100)[50,50]))
print(json.dumps(dict(module=sys.argv[1],brightness=pred,jump=pred[1]-pred[0])))
assert abs(pred[1]-pred[0])<1e-6,'Source brightness jumps at grid boundary'
