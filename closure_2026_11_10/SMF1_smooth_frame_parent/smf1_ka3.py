#!/usr/bin/env python3
"""SMF1 KA3: COL1's fold time with the member's alignment and exchange switched off and Psi absent.

With alpha = g_x = 0 and rho_Psi = 0 the SMF1 member's grading form is COL1's reduced system (frame + baryons + law).
COL1's solver modules are imported read-only from fable52_push/COL1_clock_collapse; nothing is written there. Output:
smf1_ka3.out / smf1_ka3.json in this folder. Criteria: FROZEN_CRITERIA.md section 3 (KA3).

    python3 smf1_ka3.py

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
COL1 = os.path.normpath(os.path.join(HERE, '../../fable52_push/COL1_clock_collapse'))
sys.path.insert(0, COL1)
import col1_lib as L        # noqa: E402  (read-only import)
import col1_shell as S      # noqa: E402

KD1 = json.load(open(os.path.join(COL1, '../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json')))
REF = {  # COL1 runs/hubble_mu0.1_<footing>_M<logMb>_J1200.json, event t_since_start_gyr
    ('canonical', 10.45): 0.08233105563943462, ('alt', 10.45): 0.08233958700859931,
    ('canonical', 9.4): 0.1532168404901205, ('alt', 9.4): 0.1532297080076174}
TOL = 1e-3


def fold_time(footing, logMb):
    md, ti, tend, cos = S.hubble_model(0.1, footing, logMb, 1200, KD1, lawkind='law', Xout=8000.0, visc=0.0)
    t, steps, ev = md.run(ti, tend, 1e-3, 0.25 / L.TU, on_snap=None, dt_floor=1e-20)
    return (ev['t'] - ti) * L.TU, ev.get('kind'), ev.get('r_kpc'), steps


def main():
    T = time.time()
    rows, ok = [], True
    for (ft, lm), ref in REF.items():
        tf, kind, rk, steps = fold_time(ft, lm)
        rel = abs(tf - ref) / ref
        p = rel <= TOL
        ok &= p
        rows.append({'footing': ft, 'logMb': lm, 't_fold_gyr': tf, 'COL1_recorded_gyr': ref, 'rel_diff': rel,
                     'event_kind': kind, 'r_kpc': rk, 'steps': steps, 'PASS': p})
    out = {'KA3': rows, 'KA3_PASS': ok, 'tolerance': TOL, 'runtime_s': time.time() - T,
           'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
    json.dump(out, open(os.path.join(HERE, 'smf1_ka3.json'), 'w'), indent=1, default=float)
    with open(os.path.join(HERE, 'smf1_ka3.out'), 'w') as f:
        f.write('SMF1 KA3: COL1 fold time, alignment and exchange off, Psi absent (mu_K 0.1 per Mpc, J 1200, Hubble mode)\n')
        for r in rows:
            f.write(f"  {r['footing']:9s} log M_b {r['logMb']:5.2f}: t_fold {r['t_fold_gyr']:.6f} Gyr vs COL1 "
                    f"{r['COL1_recorded_gyr']:.6f}  rel {r['rel_diff']:.2e}  event {r['event_kind']} r {r['r_kpc']:.3g} kpc"
                    f"  {'PASS' if r['PASS'] else 'FAIL'}\n")
        f.write(f"KA3 {'PASS' if ok else 'FAIL'} (line: relative {TOL:g}); runtime {out['runtime_s']:.1f} s\n")
        f.write('Adopts nothing. kappa = 1/2 FITTED; not theory closed.\n')
    print(open(os.path.join(HERE, 'smf1_ka3.out')).read())


if __name__ == '__main__':
    main()
# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
