"""Post-result checks of positive matched-inflow Hill captures, including reversal."""
import argparse
import json
from pathlib import Path

import numpy as np
import experiment as ex
from matched_inflow import cell


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    stored = json.loads((folder/'matched_run/results.json').read_text())
    rows = []
    for duration in (2., 8.):
        old = next(c for c in stored['cells'] if c['energy_input']==.3 and c['duration']==duration and c['mode']=='contract')
        row = cell(.3, duration, 'contract', refined=True)
        ex.check(row['name']+'_refined_capture', row['capture_mask']==old['capture_mask'])
        delta = float(np.max(np.abs(np.array(row['final_energy'])-old['final_energy'])))
        ex.check(row['name']+'_refined_energy', delta < 3e-7, delta)
        rows.append(row)
        print(row['name'], 'refined', row['capture_count'], '/', row['n'], 'energy disagreement', delta, flush=True)
        for nphase in (16, 32):
            row = cell(.3, duration, 'contract', nphase=nphase)
            rows.append(row)
            print(row['name'], row['capture_count'], '/', row['n'], flush=True)
    result = dict(cells=rows, checks=ex.CHECKS, assertions=len(ex.CHECKS),
                  passed=sum(c['passed'] for c in ex.CHECKS))
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('checks', result['passed'], '/', result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__ == '__main__':
    main()
