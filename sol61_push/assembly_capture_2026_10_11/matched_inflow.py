"""Match satellite-relative inertial inflow between isolated and Hill cells.

The immutable baseline module initializes coordinate velocities. This adapter
explicitly transforms them before its Hill evolution, without editing the
source underlying earlier evidence. The temporary initializer is restored.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import experiment as ex

OMEGA = np.sqrt(1/3)
BASE_INITIAL = ex.initial


def matched_initial(energy, nphase=8):
    z = BASE_INITIAL(energy, nphase)
    # v_rot = v_inertial - Omega cross r.
    z[:, 2] += OMEGA*z[:, 1]
    z[:, 3] -= OMEGA*z[:, 0]
    return z


def cell(energy, duration, mode, nphase=8, refined=False):
    ex.initial = matched_initial
    try:
        row = ex.run_cell(energy, duration, mode, 'hill', nphase=nphase, refined=refined)
    finally:
        ex.initial = BASE_INITIAL
    row['frame_convention'] = 'same initial satellite-relative inertial positions and velocities as isolated cells'
    rotating_j = np.array(row.pop('initial_j'))
    inertial_j = rotating_j+OMEGA*ex.R0**2
    mask = np.array(row['capture_mask'])
    row['initial_rotating_j'] = rotating_j.tolist()
    row['initial_inertial_j'] = inertial_j.tolist()
    row['captures_by_initial_j'] = {str(j): int(np.sum(mask & np.isclose(inertial_j, j))) for j in ex.JVALUES}
    z = matched_initial(energy, nphase)
    inertial_v = z[:, 2:4]+OMEGA*np.column_stack((-z[:, 1], z[:, 0]))
    base = BASE_INITIAL(energy, nphase)
    mismatch = float(np.max(np.abs(inertial_v-base[:, 2:4])))
    ex.check(row['name']+'_matched_inertial_velocity', mismatch < 1e-14, mismatch)
    b0, _ = ex.shape(0., duration, mode)
    e_inertial = .5*np.sum(inertial_v**2, axis=1)-1/np.sqrt(ex.R0**2+b0*b0)
    ex.check(row['name']+'_satellite_only_initially_unbound', np.all(e_inertial > 0), float(e_inertial.min()))
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    rows, refined, phase = [], [], []
    for energy in (.03, .3, .8):
        for mode, duration in [('initial', 2.), ('final', 2.), ('contract', .5), ('contract', 2.), ('contract', 8.)]:
            row = cell(energy, duration, mode)
            rows.append(row)
            print(row['name'], row['capture_count'], '/', row['n'], flush=True)
    for energy, duration in [(.03, 2.), (.8, 8.)]:
        row = cell(energy, duration, 'contract', refined=True)
        old = next(c for c in rows if c['energy_input']==energy and c['duration']==duration and c['mode']=='contract')
        ex.check(row['name']+'_refined_capture', row['capture_mask']==old['capture_mask'])
        delta = float(np.max(np.abs(np.array(row['final_energy'])-old['final_energy'])))
        ex.check(row['name']+'_refined_energy', delta < 3e-7, delta)
        refined.append(row)
        for nphase in (16, 32):
            row = cell(energy, duration, 'contract', nphase=nphase)
            phase.append(row)
            print(row['name'], row['capture_count'], '/', row['n'], flush=True)
    result = dict(cells=rows, refined=refined, phase_cells=phase, checks=ex.CHECKS,
                  assertions=len(ex.CHECKS), passed=sum(c['passed'] for c in ex.CHECKS))
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('checks', result['passed'], '/', result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__ == '__main__':
    main()
