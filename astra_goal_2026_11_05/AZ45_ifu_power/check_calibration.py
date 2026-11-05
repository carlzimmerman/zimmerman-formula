#!/usr/bin/env python3
"""Synthetic positive/negative controls for the frozen nonlinear-fit grader."""
import hashlib,json
from pathlib import Path
import numpy as np
import calibration as C
checks=[]
def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
n=np.zeros((2,3,3,4,3));n[:,1]=(.6*(np.array([.6,1.,1.4])-1))[None,:,None,None];n[:,2]=-.2
l=np.zeros((2,12,6));l[:,:,1]=-.2
for i,x in enumerate([.01,-.01,.005,-.005],start=2):l[:,:,i]=-.3*x
check('exact_calibrated_fixture',C.calibrate(n,l,True)['passed'])
check('unresolved_fit_rejected',not C.calibrate(n,l,False)['passed'])
x=n.copy();x[:,0]+=.08;check('flat_bias_detected',not C.calibrate(x,l,True)['passed'])
x=n.copy();x[:,1]=0;check('missing_rise_detected',not C.calibrate(x,l,True)['passed'])
x=n.copy();x[:,2]=0;check('ineffective_mutation_detected',not C.calibrate(x,l,True)['passed'])
x=n.copy();x[:,2]=-.3;check('wrong_mutation_lever_detected',not C.calibrate(x,l,True)['passed'])
x=n.copy();x[0,1,0,0,0]+=.02;check('single_fit_nonconvergence_detected',not C.calibrate(x,l,True)['passed'])
x=l.copy();x[:,:,4]+=.001;check('local_derivative_nonconvergence_detected',not C.calibrate(n,x,True)['passed'])
x=l.copy();x[0,0,1]+=.02;check('noiseless_fit_nonconvergence_detected',not C.calibrate(n,x,True)['passed'])
try:C.calibrate(n[:,:,:,:,:2],l,True);rejected=False
except ValueError:rejected=True
check('missing_replicates_rejected',rejected)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(C.__file__)]},scope='Synthetic gate controls only; no population power claim')
Path(__file__).with_name('calibration_checks.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
