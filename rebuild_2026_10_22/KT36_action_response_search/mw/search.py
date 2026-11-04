#!/usr/bin/env python3
"""Action response experiments using the unchanged KT33/34 operators and data."""
import argparse
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RB = HERE.parents[1]
sys.path.insert(0, str(RB / 'KT34_reciprocal_epsilon_scan/mw'))
import scan as E
M, np = E.M, E.np


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    p.add_argument('--widths', type=float, nargs='+', required=True)
    p.add_argument('--refine', type=int, default=2)
    p.add_argument('--lmax', type=int, default=128)
    p.add_argument('--cut', type=float, default=120.)
    p.add_argument('--indices', type=int, nargs='+')
    p.add_argument('--feet', nargs='+', default=list(M.C.A0))
    args = p.parse_args()
    if any(x <= 0 for x in args.widths):
        p.error('Universal physical widths must be positive.')
    start = time.monotonic()
    cells = E.population()
    ids = list(range(len(cells))) if args.indices is None else args.indices
    out = dict(parameters=vars(args), law='Phi=N rho+S_ell* Phi_ph_simple[S_ell rho]',
               width_definition='ell is a universal physical length in kpc; no mass scaling or rounding',
               cells=cells, footings={})
    for foot in args.feet:
        cache = E.Cached(foot, args.refine, cells)
        f = dict(grid=dict(nr=cache.g.Nr, nt=cache.g.Nt),
                 density_basis_verification=cache.verify, scans=[])
        out['footings'][foot] = f
        for sig in args.widths:
            row = cache.scan(0., args.lmax, args.cut, ids,
                             explicit_widths={i: sig for i in ids})
            del row['epsilon']
            row['universal_width_kpc'] = sig
            f['scans'].append(row)
            print(foot, sig, json.dumps(row['summary']),
                  'seconds', time.monotonic()-start, flush=True)
            Path(args.output).write_text(json.dumps(out, indent=2, allow_nan=False))
    out['runtime_seconds'] = time.monotonic()-start
    Path(args.output).write_text(json.dumps(out, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
