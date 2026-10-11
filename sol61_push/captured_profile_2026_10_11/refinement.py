"""Post-result quadrature refinement; same bounded incoming DF and source."""
import argparse
import json
from pathlib import Path
import numpy as np
import experiment as ex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    edges = np.array([.01,.02,.03,.05,.07,.1,.14,.2,.28,.4,.6,1.,2.,4.,8.,16.,32.,64.,128.])
    rows = []
    for duration in (2., 8.):
        for n in (8, 10):
            row = ex.cell(n, duration, edges)
            rows.append(row)
            print('cell',n,duration,'capture',row['captured_fraction'],
                  'shape',{k:v['max_cdf_difference'] for k,v in row['shape_scores'].items()},flush=True)
    result = dict(edges=edges.tolist(),cells=rows,checks=ex.CHECKS,
                  assertions=len(ex.CHECKS),passed=sum(c['passed'] for c in ex.CHECKS))
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print('checks',result['passed'],'/',result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__=='__main__':
    main()
