import os,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
cases=[('draco',64,.02,1025,6,'draco_HJ_v2_N64'),('sextans',64,.02,1025,6,'sextans_HJ_v2_N64'),('fornax',64,.02,1025,6,'fornax_HJ_v2_N64'),('leoi',64,.02,1025,6,'leoi_HJ_v2_N64'),('draco',96,.02,1025,6,'draco_HJ_v2_N96'),('sextans',96,.02,1025,6,'sextans_HJ_v2_N96'),('draco',64,.01,1025,.5,'draco_short_dt001'),('draco',64,.02,2049,.5,'draco_short_nr2049')]
for name,n,dt,nr,T,tag in cases:
 subprocess.run([sys.executable,str(P/'galaxy_v2.py'),'--galaxy',name,'--n',str(n),'--dt',str(dt),'--nr',str(nr),'--T',str(T),'--wall','240','--tag',tag],env=env,check=True)
