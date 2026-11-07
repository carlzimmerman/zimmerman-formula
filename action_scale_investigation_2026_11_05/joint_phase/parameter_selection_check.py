"""Compile the explicit Lean certificate; retain logs and a wrong-factor control."""
import argparse, json, pathlib, subprocess
p=argparse.ArgumentParser(); p.add_argument('--out',required=True); p.add_argument('--mutate',action='store_true'); a=p.parse_args()
out=pathlib.Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
source=pathlib.Path('action_scale_investigation_2026_11_05/joint_phase/lean/ParameterSelection.lean')
if a.mutate:
    altered=out.parent/'WrongFactor.lean'
    altered.write_text(source.read_text().replace('gn^2+2*a*beta*gn','gn^2+a*beta*gn'))
    source=altered
run=subprocess.run(['lean',str(source)],capture_output=True,text=True,timeout=50)
(out.parent/'lean-output.txt').write_text(run.stdout+run.stderr)
result={'exit_code':run.returncode,'mutation':a.mutate,'source':str(source),
        'axiom_lines':[s for s in run.stdout.splitlines() if 'axioms' in s],
        'sorryAx_reported':'sorryAx' in run.stdout}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(run.returncode or int(result['sorryAx_reported']))
