"""Matched short-time/dt/box controls; invoke only after run_matrix exits."""
import os,subprocess,sys,pathlib
P=pathlib.Path(__file__).resolve().parent;env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
for galaxy in ('draco','sextans','fornax','leoi'):
 for n,dt,box in [(64,.02,28),(96,.02,28),(96,.01,28),(96,.02,20)]:
  tag=f'{galaxy}_short_N{n}_dt{dt}_B{box}'
  subprocess.run([sys.executable,str(P/'galaxy.py'),'--galaxy',galaxy,'--n',str(n),'--box',str(box),'--dt',str(dt),'--T','.5','--wall','80','--tag',tag],env=env,check=True)
