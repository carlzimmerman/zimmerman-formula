#!/usr/bin/env python3
"""Run a named reviewed FR01 lane with the installed bounded runner."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
LANES={
    'radial':('radial_contract_v2.json','radial_stability_v2.py',True),
    'kinetic':('kinetic_contract_v2.json','kinetic_screen_v2.py',False),
    'canonical-energy':('canonical_energy_contract.json','canonical_energy_check.py',False),
    'static':('static_contract_A1.json','static_response_v2.py',True),
    'static-refinement':('static_refinement_contract.json','static_refinement.py',True),
    'dilute-stability':('dilute_stability_contract.json','dilute_stability.py',False),
    'dilute-static':('static_dilute_contract.json','static_dilute.py',True),
    'endpoints':('endpoint_stability_contract.json','endpoint_stability.py',False),
    'checks':('verify_results_contract.json','verify_results.py',False),
}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('lane',choices=sorted(LANES));p.add_argument('--runner',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();runner=a.runner.expanduser().resolve()
    output=(PROJECT/a.output).resolve()
    if not runner.is_file():p.error('runner must be the installed mathbox run_experiment.py')
    if output.exists():p.error('output must be a new directory; existing evidence is immutable')
    if PROJECT not in output.parents:p.error('output must be inside this repository')
    contract,script,profiles=LANES[a.lane]
    config=json.loads((HERE/contract).read_text())
    rel=output.relative_to(PROJECT)
    cmd=[sys.executable,str(runner),'--root',str(PROJECT),'--contract',str(HERE/contract)]
    for name in config['execution_artifacts']:cmd+=['--input',name]
    cmd+=['--output',str(rel),'--result',str(rel/'result.json')]
    if profiles:cmd+=['--result',str(rel/'profiles.npz')]
    cmd+=['--timeout','300','--max-cpu-seconds','240','--max-threads','1',
          '--max-output-bytes','1048576','--',sys.executable,str(HERE/script),str(rel/'result.json')]
    return subprocess.run(cmd,cwd=PROJECT).returncode


if __name__=='__main__':sys.exit(main())
