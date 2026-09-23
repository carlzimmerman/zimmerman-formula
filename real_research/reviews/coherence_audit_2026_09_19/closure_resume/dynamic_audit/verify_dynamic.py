from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve()
for name in ('audit_dynamics.py','constraints_check.py','phase_coordinates.py','high_precision.py'):
 print('RUN',name,flush=True)
 subprocess.run([sys.executable,str(here/name),str(out)],check=True)
