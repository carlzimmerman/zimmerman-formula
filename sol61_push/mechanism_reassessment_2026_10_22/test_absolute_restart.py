"""A split run must agree with an uninterrupted explicitly time-dependent run."""
from pathlib import Path
import tempfile,subprocess
import numpy as np
P=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as d:
 d=Path(d);rng=np.random.default_rng(14);state=rng.normal(0,.1,(2,4,4,4,4))
 def run(s,start,duration,name):
  path=d/(name+'.bin');np.concatenate(([4,8,.005,duration,.7,.2,.4,.03,1.],s.ravel())).astype('<f8').tofile(path)
  subprocess.run([str(P/'coupled_field_restart'),str(path),str(d/(name+'.csv')),str(d/(name+'_final.bin')),str(start)],check=True)
  return np.fromfile(d/(name+'_final.bin')).reshape(s.shape)
 whole=run(state,3.,.4,'whole');first=run(state,3.,.2,'first');split=run(first,3.2,.2,'split')
 err=float(np.max(abs(whole-split)));print('absolute time restart max error',err);assert err<1e-12
