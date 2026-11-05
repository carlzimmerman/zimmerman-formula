"""Regression: nested export stays bounded and preserves direct numerical values."""
import csv,time
from pathlib import Path
import numpy as np
import mpmath as mp
mp.mp.dps=80
import sympy as s
from sy1_export import mappings
from sy1_leaves import eval_H,FEATURES
start=time.monotonic()
L={k:np.linspace(.2,.8,17) for k in FEATURES}
L.update(one=np.ones(17),two=np.full(17,2.),half=np.full(17,.5),pi_=np.full(17,np.pi),ell=np.full(17,1e-10))
syms={k:s.Symbol(k) for k in FEATURES};n=0
with np.errstate(all='ignore'):
 for row in csv.DictReader(open(Path(__file__).parent/'recovery_2026_11_05/export_fixture.csv')):
  expr=s.sympify(row['Equation'],locals=dict(syms,**mappings()),evaluate=False)
  fn=s.lambdify(list(syms.values()),expr,'mpmath',cse=False)
  actual=np.array([float(fn(*(mp.mpf(float(L[k][i])) for k in FEATURES))) for i in range(17)])
  expected=np.broadcast_to(eval_H(row['Equation'],L),(17,))
  assert np.array_equal(np.isfinite(actual),np.isfinite(expected)),row['Complexity']
  good=np.isfinite(expected)
  assert np.allclose(actual[good],expected[good],rtol=1e-10,atol=1e-12),row['Complexity']
  n+=1
assert time.monotonic()-start<10
print({'expressions':n,'points_each':17,'seconds':time.monotonic()-start,'result':'PASS'})
