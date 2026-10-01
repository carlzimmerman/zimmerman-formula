#!/usr/bin/env python3
"""Summarize recorded executions; do not equate check success with physics."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
records=[]
for p in sorted((HERE/'reproduction').glob('*/summary.json')):
    s=json.loads(p.read_text())
    result_files=list(p.parent.glob('*_results*.json'))
    result={}; checks={}; baseline_checks={}
    if result_files:
        result=json.loads(result_files[0].read_text())
        checks=result.get('checks',{})
        baseline=ROOT/Path(s['script']).parent/result_files[0].name
        if baseline.exists(): baseline_checks=json.loads(baseline.read_text()).get('checks',{})
    failures=[]; new_failures=[]; changed=[]
    if isinstance(checks,dict):
        for key,val in checks.items():
            if not isinstance(val,dict): continue
            ok=val.get('ok',val.get('pass',val.get('passed')))
            old=baseline_checks.get(key,{}) if isinstance(baseline_checks,dict) else {}
            old_ok=old.get('ok',old.get('pass',old.get('passed'))) if isinstance(old,dict) else None
            if ok is False:
                failures.append({'id':key,'load_bearing':val.get('load_bearing',val.get('load')),'measured':val.get('measured')})
            if ok != old_ok: changed.append({'id':key,'old':old_ok,'new':ok})
    err=(p.parent/'stderr.txt').read_text()
    crash='Traceback (most recent call last)' in err
    rec=dict(s,run=p.parent.name,result_present=bool(result_files),traceback=crash,failures=failures,changed_verdicts=changed)
    records.append(rec)

(HERE/'REPRODUCTION_INDEX.json').write_text(json.dumps(records,indent=2))
lines=['# Reproduction execution index','',
       'Generated from captured runs. The original thresholds remain unchanged. An exit code of 1 may be an expected mutation, a preserved scientific failure, numerical disagreement, or an execution error. Consult the named checks. Timing and other textual differences are retained in comparison files.','',
       '| Run | Seconds | Exit | Result JSON | Changed check verdicts | Interpretation |',
       '|---|---:|---:|---|---:|---|']
for r in records:
    kind='execution error' if r['traceback'] else ('original check verdicts preserved' if r['result_present'] and not r['changed_verdicts'] else 'inspect changed checks')
    if not r['result_present'] and not r['traceback']: kind='no result JSON; inspect logs'
    name=r['run']
    lines.append(f"| [{name}](reproduction/{name}/summary.json) | {r['runtime_s']:.1f} | {r['exit_code']} | {'yes' if r['result_present'] else 'no'} | {len(r['changed_verdicts'])} | {kind} |")
running=list((HERE/'reproduction').glob('*/RUNNING.json'))
if running:
    lines+=['','## Last observed running','']
    lines += ['- '+p.parent.name for p in running]
    lines+=['','These marker files are not a process-liveness guarantee. The coordinator must reconcile them with tool-session status.']
(HERE/'REPRODUCTION_INDEX.md').write_text('\n'.join(lines)+'\n')
print(f'{len(records)} recorded runs; {len(running)} running markers; full named failures in REPRODUCTION_INDEX.json')
