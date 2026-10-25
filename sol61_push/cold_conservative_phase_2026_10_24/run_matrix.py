"""Sequential bounded matrix; does not duplicate live jobs."""
import os,subprocess,sys,pathlib
P=pathlib.Path(__file__).resolve().parent
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
for n in (64,96):
 for galaxy in ('draco','sextans','fornax','leoi'):
  tag=f'{galaxy}_incoming_N{n}'
  subprocess.run([sys.executable,str(P/'galaxy.py'),'--galaxy',galaxy,'--n',str(n),'--tag',tag,'--T','10','--wall','80'],env=env,check=True)
 for galaxy in ('draco','sextans'):
  tag=f'{galaxy}_late_N{n}'
  subprocess.run([sys.executable,str(P/'galaxy.py'),'--galaxy',galaxy,'--late','--n',str(n),'--tag',tag,'--T','10','--wall','80'],env=env,check=True)
