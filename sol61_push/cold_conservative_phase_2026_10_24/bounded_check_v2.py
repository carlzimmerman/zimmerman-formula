"""Deterministic benchmark comparison with declared floating-point tolerance."""
import pathlib,subprocess,sys,json,numpy as np
P=pathlib.Path(__file__).resolve().parent;dest=pathlib.Path(sys.argv[1]);dest.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(P/'bench.py'),str(dest/'benchmark.json')],check=True)
a=json.loads((dest/'benchmark.json').read_text());b=json.loads((P/'bench.json').read_text())
def compare(a,b):
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:compare(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):compare(x,y)
 else:np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-14)
compare(a,b)
subprocess.run([sys.executable,str(P/'audit.py'),str(dest/'result.json')],check=True)
