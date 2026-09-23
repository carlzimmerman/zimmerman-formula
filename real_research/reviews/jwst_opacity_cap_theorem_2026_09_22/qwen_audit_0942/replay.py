import json, os, subprocess, sys
from pathlib import Path
import sympy as S
p=Path(__file__).resolve().parent
runs={}
for mode in ['main','positive','negative']:
    r=subprocess.run([sys.executable,str(p/'candidate.py')],env=dict(os.environ,ORCH_MODE=mode),capture_output=True,text=True,timeout=15)
    if r.returncode: raise RuntimeError(r.stderr)
    runs[mode]=json.loads(r.stdout)
q,e=S.symbols('Qs E_Z2')
target=2*q/3+S.Rational(11,9)*(1-e)
main=S.sympify(runs['main']['measurements']['ED2_eliminated'],locals={'Qs':q,'E_Z2':e})
negative=S.sympify(runs['negative']['measurements']['ED2_eliminated'],locals={'Qs':q,'E_Z2':e})
checks={'main_algebra':S.expand(main-target)==0,
 'negative_actual_kernel_changes_algebra':S.expand(negative-target)!=0,
 'main_pass':runs['main']['checks']['bracket_certificate'],
 'positive_pass':runs['positive']['checks']['bracket_certificate'],
 'negative_rejects':not runs['negative']['checks']['bracket_certificate']}
result={'checks':checks,'all_checks_pass':all(checks.values()),'runs':runs,
 'verdict':'Algebra reproduced only. ED2 label is wrong: expected bracket equals Var(D), not E[D^2], since initial martingale value is d. Positive repeats main rather than changing variables. Stopping argument not implemented or established by this candidate.'}
(p/'certified'/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
