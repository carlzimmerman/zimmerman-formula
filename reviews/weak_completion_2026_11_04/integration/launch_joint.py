"""Bounded continuation launcher; each scientific segment has its own contract."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUNNER = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')

def main(first='2', count='1', prior='run_joint001', step='.0001', prefix='run_joint'):
    base = json.loads((HERE/'contract_joint.json').read_text())
    old = HERE/prior/'result.json'
    for serial in range(int(first), int(first)+int(count)):
        previous = json.loads(old.read_text())
        if not previous['checks']['independent_energy_work']:
            raise RuntimeError('Previous independent work check failed')
        if previous['state']['N'] >= .0021690179772784167-1e-13:
            break
        folder = HERE/(prefix+format(serial, '03d'))
        result = folder/'result.json'
        contract = json.loads(json.dumps(base))
        contract['mathematics'].update(
            coefficient_domain='Float64 finite40node30group SF+polarized-vector 1<->2 network; leading e=.003, mu=2e6GeV, xi=.02.',
            inputs=['Fresh N=0 common30group initial packet, with complete successive checkpoint ancestry; independent work retained without resetting.',str(old.relative_to(ROOT))],
            non_claims=['No phase/momentum/continuum convergence claim from one trajectory.', 'No elastic2<->2 or loop decays in this early warm history.', 'Partial checkpoint is not completed target.', 'No cold-matter or derived vacuum-normalization claim.'])
        contract['mathematics']['bounds'].update(dN_max=float(step), stepmax=float(step), phase_nodes=8)
        contract['mathematics']['bounds'].pop('dN',None)
        artifacts = list(base['execution_artifacts'])
        for path in (old, old.parent/'manifest.json',Path(__file__).resolve()):
            rel=str(path.relative_to(ROOT))
            if rel not in artifacts:
                artifacts.append(rel)
        contract['execution_artifacts']=artifacts
        contract_path=HERE/('contract_'+folder.name+'.json')
        if contract_path.exists() or folder.exists():
            raise RuntimeError('Refusing to overwrite run or contract')
        contract_path.write_text(json.dumps(contract,indent=2)+'\n')
        command=[sys.executable,str(RUNNER),'--root',str(ROOT),'--contract',str(contract_path),
            '--output',str(folder.relative_to(ROOT)),'--result',str(result.relative_to(ROOT)),
            '--timeout','240','--max-cpu-seconds','235','--max-threads','1']
        for rel in artifacts:
            command += ['--input',rel]
        command += ['--',sys.executable,str(HERE/'joint_history.py'),str(result),str(old),'.0021690179772784167',step,'8']
        subprocess.run(command,cwd=ROOT,check=True)
        current=json.loads(result.read_text())
        if not all(value for key,value in current['checks'].items() if key!='target_reached'):
            raise RuntimeError('Physical checkpoint check failed')
        if current['state']['N'] <= previous['state']['N']:
            raise RuntimeError('No progress; inspect failed nonlinear steps')
        print(json.dumps({'run':folder.name,'N':current['state']['N'],'J':current['state']['J'],
            'max_energy_error_over_excitation':current['case']['max_energy_error_over_excitation'],
            'accepted':current['case']['accepted'],'rejected':current['case']['rejected']}),flush=True)
        old=result

if __name__=='__main__':
    main(*sys.argv[1:])
