from pathlib import Path
import subprocess
import sys
here=Path(__file__).resolve().parent
root=here.parents[3]
out=Path(sys.argv[1]).resolve()
assert out.is_relative_to(here)
subprocess.run([sys.executable,str(here/'check_cluster.py'),str(out)],check=True,cwd=root)
run=subprocess.run(['lake','env','lean',str(here/'Hydrostatic.lean')],
                   cwd=root/'fable_independent_2026/lean_2026',capture_output=True,text=True)
(out/'lean.txt').write_text(run.stdout+run.stderr)
print(run.stdout,run.stderr)
assert run.returncode==0
assert 'sorryAx' not in run.stdout and 'warning:' not in run.stdout
