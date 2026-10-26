import argparse,subprocess,shutil,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--R',required=True);p.add_argument('--output',required=True);p.add_argument('--work',required=True);a=p.parse_args()
b=Path(__file__).resolve().parent;out=Path(a.output)
subprocess.run([sys.executable,str(b.parent/'continuum/run_point.py'),'--R',a.R,'--nb','25','--lmax','2','--multipole','20','--work',a.work,'--bin','/private/tmp/ukrmol-build/build/bin','--output',a.output],check=True)
shutil.copy2(Path(a.work)/'fort.250',out.parent/'inner.ci')
