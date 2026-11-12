#!/usr/bin/env python3
"""VSJ1 S-cosmo: set the primordial amplitude A by the frozen host-mass rule (FROZEN_CRITERIA.md section 2).

    python3 vsj1_cosmo.py grid A1 A2 ...     canonical runs at log M_b 10.5 for a list of amplitudes (the map A -> host)
    python3 vsj1_cosmo.py select             per footing, bracket and mass: the finished run nearest the target host

The host ratio is the charge inside the standing region R_st over M_b. Runs scale exactly with M_b, so one amplitude
serves any mass with the same target ratio. Writes runs/cosmo_*.json and vsj1_cosmo_tune.json.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import glob, json, math, os, sys
from multiprocessing import Pool
import numpy as np
import vsj1_hydro as H
import vsj1_grade as GR

HERE = os.path.dirname(os.path.abspath(__file__))
PROCS = int(os.environ.get('VSJ1_PROCS', '6'))


def job(args):
    f, A = args
    name = f'cosmo_{f}_A{A:g}_N300'
    p = os.path.join(H.RUNS, name + '.json')
    if os.path.exists(p):
        d = json.load(open(p))
    else:
        d = H.run_cosmo(f, A, 300)
        os.makedirs(H.RUNS, exist_ok=True); json.dump(d, open(p, 'w'))
    return {'footing': f, 'A': A, 'run': name, 'host_over_Mb': host(d), 'status': d['status'], 'R_st': GR.standing_a1(d['r'], d['v'], d['MX'], d['Mb'])[1],
            'R_ta': d['R_ta'], 'steps': d['steps'], 'seconds': d['seconds']}


def host(d):
    """Charge inside the standing region over M_b, with AMENDMENT A1's R_st."""
    i, _ = GR.standing_a1(d['r'], d['v'], d['MX'], d['Mb'])
    return float(d['MX'][i] / d['Mb']) if i >= 0 else 0.0


def table(f):
    rows = []
    for p in glob.glob(os.path.join(H.RUNS, f'cosmo_{f}_A*_N300.json')):
        d = json.load(open(p))
        if d['status'] == 'done' and host(d) > 0:
            rows.append((d['A'], host(d)))
    return sorted(set(rows))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'grid':
        jobs = [('canonical', float(a)) for a in sys.argv[2:]]
        with Pool(min(PROCS, len(jobs))) as pool:
            for r in pool.map(job, jobs):
                print(json.dumps(r))
    elif mode == 'select':
        # For each footing, bracket and mass: the finished run of that footing whose host ratio is nearest the target.
        tune = {}
        for f in GR.FOOT:
            runs = []
            for p in sorted(glob.glob(os.path.join(H.RUNS, f'cosmo_{f}_A*_N300.json'))):
                d = json.load(open(p))
                if d['status'] == 'done' and host(d) > 0:
                    runs.append({'A': d['A'], 'run': d['name'], 'achieved': host(d), 'steps': d['steps'], 'seconds': d['seconds']})
            tune[f] = {'H1': {}, 'H2': {}, 'runs': runs}
            for br in ('H1', 'H2'):
                for m in GR.MASSES:
                    T = GR.RSHARE[f] if br == 'H1' else GR.h2_share(f, m)
                    if not runs:
                        continue
                    best = min(runs, key=lambda x: abs(math.log(x['achieved'] / T)))
                    tune[f][br][str(m)] = dict(best, target=T, within_10pct=bool(abs(best['achieved'] / T - 1) <= 0.10))
                    print(f, br, m, f"target {T:.2f}: run {best['run']} achieved {best['achieved']:.2f} -> {'ok' if tune[f][br][str(m)]['within_10pct'] else 'OUTSIDE 10 %'}")
        json.dump(tune, open(os.path.join(HERE, 'vsj1_cosmo_tune.json'), 'w'), indent=1)
