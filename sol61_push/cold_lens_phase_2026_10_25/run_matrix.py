import os,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
# The first N64 lens pilot failed earlier than the old static frame. Test the
# wider box across all four, and one spatial/rate control; do not launch a large
# campaign around a failed choice of carrier.
for galaxy,n,beta in [('draco',64,.1),('sextans',64,.1),('fornax',64,.1),('leoi',64,.1),('draco',96,.1),('draco',96,.08)]:
 tag=f'{galaxy}_lens_N{n}_B40_b{beta}'
 subprocess.run([sys.executable,str(P/'galaxy.py'),'--galaxy',galaxy,'--n',str(n),'--box','40','--beta',str(beta),'--T','6','--wall','120','--tag',tag],env=env,check=True)
