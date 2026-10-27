"""Freeze one initial state per particle level before dependent controls."""
import argparse,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;REL=HERE.relative_to(ROOT)
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')

def launch(a):
    name='initial_n%d_s%d'%(a.ncold,a.seed);out=REL/name
    if (ROOT/out).exists():raise FileExistsError(name)
    files=['launch_initial.py','prepare_initial.py','evolution.py','refined_initial.py','test_refined_initial.py','fast_gravity.py','fast_gravity.c','fast_gravity.dylib','CONTRACT.md']
    if a.backend=='metal':files+=['metal_gravity.py','metal_gravity.mm','metal_gravity.dylib']
    inputs=[str(REL/f) for f in files]
    c=dict(claim_id='DWARF_COMMON_IC_'+name,mathematics=dict(assertion_tested='Prepared nested quiet initial dwarf arrays; same continuous law and species virials, fixed for backend/epsilon/scattering controls',coefficient_domain='CPUbinary64 initial phases and velocities, native CPU or independently admitted DSdirect virial force',conventions='pc,Msun,Myr; referencePlummer epsilon10pc; same originalpreparedlaw',inputs=['seed%d'%a.seed],bounds=dict(ncold=a.ncold,nstars=a.ncold//8,wall_seconds=180),non_claims=['No evolution or core result','Normalized velocities not identical between different N']),execution_artifacts=inputs,software=[dict(name='simulationPython',version='3.9.6')],randomness=dict(used=True,generator='scrambled6DSobol independent species streams',seed=a.seed))
    p=HERE/'contracts'/('common_'+name+'.json');p.write_text(json.dumps(c,indent=2)+'\n')
    cmd=['/opt/homebrew/bin/python3.12',str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),'--contract',str(p),'--output',str(out),'--timeout','180','--max-cpu-seconds','900','--max-threads','4']
    for f in inputs:cmd+=['--input',f]
    for f in ('initial.npz','initial_metadata.json'):cmd+=['--result',str(out/f)]
    cmd+=['--','nice','-n','19','/usr/bin/python3',str(REL/'prepare_initial.py'),'--output',str(out),'--ncold',str(a.ncold),'--seed',str(a.seed),'--backend',a.backend]
    return subprocess.call(cmd)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ncold',type=int,required=True);p.add_argument('--seed',type=int,default=87319);p.add_argument('--backend',choices=('cpu','metal'),default='metal');raise SystemExit(launch(p.parse_args()))
