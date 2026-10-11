"""Tighter integration of positive Hill captures and the mixed isolated result."""
import argparse
import json
from pathlib import Path

import numpy as np
import experiment as ex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    rows = []
    cases = [('run_v2', 'isolated', .8, 2., 8),
             ('run_v2', 'hill', .8, 8., 8),
             ('phase_run', 'hill', .03, 2., 32),
             ('phase_run', 'hill', .8, 8., 32)]
    for source, environment, energy, duration, nphase in cases:
        stored = json.loads((folder/source/'results.json').read_text())
        old = next(c for c in stored['cells'] if c['environment']==environment
                   and c['energy_input']==energy and c['duration']==duration
                   and c['mode']=='contract' and c['n']==6*nphase)
        row = ex.run_cell(energy, duration, 'contract', environment, nphase=nphase, refined=True)
        ex.check(row['name']+'_refined_capture_mask', row['capture_mask']==old['capture_mask'])
        delta = float(np.max(np.abs(np.array(row['final_energy'])-old['final_energy'])))
        ex.check(row['name']+'_refined_energy_agreement', delta < 3e-7, delta)
        rows.append(row)
        print(row['name'], row['capture_count'], '/', row['n'], 'energy disagreement', delta, flush=True)
    result = dict(cells=rows, checks=ex.CHECKS, assertions=len(ex.CHECKS),
                  passed=sum(c['passed'] for c in ex.CHECKS))
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('checks', result['passed'], '/', result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__ == '__main__':
    main()
