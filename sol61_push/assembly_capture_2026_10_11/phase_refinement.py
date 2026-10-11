"""Post-result angular sampling check; does not establish continuum convergence."""
import argparse
import json
from pathlib import Path

import experiment as ex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    rows = []
    for energy, duration in [(.03, 2.), (.3, 2.), (.8, 8.)]:
        for nphase in (16, 32):
            row = ex.run_cell(energy, duration, 'contract', 'hill', nphase=nphase)
            rows.append(row)
            print(row['name'], row['capture_count'], '/', row['n'], flush=True)
    result = dict(cells=rows, checks=ex.CHECKS, assertions=len(ex.CHECKS),
                  passed=sum(c['passed'] for c in ex.CHECKS))
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('checks', result['passed'], '/', result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__ == '__main__':
    main()
