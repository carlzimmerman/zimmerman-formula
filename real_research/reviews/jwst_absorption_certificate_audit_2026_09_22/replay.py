import json,os,subprocess,sys,tempfile
from pathlib import Path
p=Path(__file__).resolve().parent
root=p.parents[2]
source=root/'real_research/reviews/jwst_cap_attempt_audit_2026_09_22/f0773c84727d48feaac1155b82ebf844.py'
runs={}
with tempfile.TemporaryDirectory(prefix='abs-certificate-audit-') as td:
    inputs=Path(td)/'inputs.json'
    inputs.write_text(json.dumps({'audited_absorption':str(source)}))
    for mode in ['main','positive','negative']:
        r=subprocess.run([sys.executable,str(p/'candidate.py')],env=dict(os.environ,ORCH_MODE=mode,ORCH_INPUTS=str(inputs)),capture_output=True,text=True,timeout=30)
        if r.returncode:raise RuntimeError(r.stderr)
        runs[mode]=json.loads(r.stdout)
checks={}
for mode in ['main','positive']:
    for alpha in ['0.1','0.5']:
        v=runs[mode]['measurements'][alpha]
        checks[f'{mode}_mean_{alpha}']=abs(v['z_mean'])<5
        checks[f'{mode}_escape_{alpha}']=abs(v['z_p'])<5
for alpha in ['0.1','0.5']:
    checks[f'negative_escape_{alpha}']=abs(runs['negative']['measurements'][alpha]['z_p'])>5
    checks[f'negative_rejected_{alpha}']=not runs['negative']['checks'][f'agreement_alpha_{alpha}']
result={'checks':checks,'all_checks_pass':all(checks.values()),'runs':runs,
 'scope':'Independent replay of unchanged Qwen statistical certificate; solver had prior independent-seed audit. Finite calibration only. The phrase significance level alpha=.1 in candidate prose is wrong: alpha is absorption rate, not test significance.'}
(p/'certified'/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
