import os,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
for dt,nr,tag in [(.01,1025,'draco_matched_dt001_T3'),(.02,2049,'draco_matched_nr2049_T3')]:
 subprocess.run([sys.executable,str(P/'galaxy_v2.py'),'--galaxy','draco','--n','64','--dt',str(dt),'--nr',str(nr),'--T','3','--tag',tag],env=env,check=True)
