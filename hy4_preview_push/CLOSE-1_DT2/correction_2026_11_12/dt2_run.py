#!/usr/bin/env python3
"""CLOSE-1 / DT2: the formation run and the reach, 4 masses x 2 footings  (K3).

Produces a pre-breakdown diagnostic only. A central cutoff or shell crossing does
not define a post-caustic halo; R_set(0) and settled-charge residual are unavailable.
Corrected 2026-11-12; old .out and RESULT.md are retained with a correction notice.
"""
import numpy as np
import dt2_function as D
import dt2_form as F

KPC = D.KPC
MASSES = [9.4, 10.45, 10.7, 10.9]
KIDS_INNER = {9.4: 81.0, 10.45: 272.0, 10.7: 362.0, 10.9: 456.0}      # kpc, canonical
FLD1_RFOLD = {9.4: 62.0, 10.45: 139.0, 10.7: 169.0, 10.9: 197.0}      # kpc, canonical
COL1_FOLD_T = (0.063, 0.154)                                           # Gyr, both footings


def main():
    print("=" * 118)
    print("DT2 FORMATION AND REACH (K3).  Dust in Hubble flow at z = 10, baryon point mass")
    print("(1 kpc Plummer) ramped on over 1 Gyr -- COL1's initial condition.")
    print("=" * 118)
    out = {}
    for a0, lab in [(D.A0_CANON, "canonical"), (D.A0_ALT, "alt")]:
        print(f"\n--- footing {lab} : a0 = {a0:.4e} ---")
        print(f"{'log M_b':>7} {'event[Gyr]':>11} {'end_z':>9} {'termination':>18} "
              f"{'R_set(0)':>14}")
        print("-" * 118)
        for lm in MASSES:
            res = F.run(lm, a0, absorb=False)
            a = res['snaps'][-1][1]
            ff = res['first_fold']
            tf = (ff-float(F.T_OF_A(1/11))) / 1e9 / F.YR if ff is not None else None
            tf_text = f"{tf:.4f}" if tf is not None else "none"
            print(f"{lm:7.2f} {tf_text:>11} {1/a-1:9.3f} "
                  f"{res['termination_reason']:>18} {'UNAVAILABLE':>14}")
            out[(lab, lm)] = dict(first_event_Gyr=tf, end_z=1/a-1,
                                  termination=res['termination_reason'],
                                  Rset=None, settled_residual=None)
    return out


def diagnosis(lm=10.45, a0=D.A0_CANON):
    """Why: compare the infall speed with the DT2 sound speed at the compression reached."""
    print("\n" + "=" * 118)
    print("WHY: infall speed vs the DT2 sound speed along the collapse (log M_b %.2f, %s)"
          % (lm, "canonical" if a0 == D.A0_CANON else "alt"))
    print("=" * 118)
    res = F.run(lm, a0, absorb=False)
    if res['first_fold'] is not None:
        print(f"first {res['first_event_kind']} at t = "
              f"{(res['first_fold']-float(F.T_OF_A(1/11.)))/1e9/F.YR:.4f} Gyr")
    else:
        print(f"No event resolved before {res['termination_reason']}")
    for (t, a, Ff, v, s, rj, Mcen, dm) in res['snaps'][::max(1, len(res['snaps']) // 8)]:
        rho = res['rho'] if 'rho' in res else None
        q = F.x_of_rho(dm / ((4 * np.pi / 3) * (Ff[1:] ** 3 - Ff[:-1] ** 3)))
        qq = D.n_of_x(q) / D.N0
        cad = np.sqrt(D.C_SI ** 2 * D.n_of_x(q) / D.nprime_of_x(q))
        print(f"  z={1/a-1:6.2f}  q_bg={a**-3:9.2f}  q_max(inner shell)={qq.max():12.3e} "
              f" c_ad_max={cad.max()/1e3:9.1f} km/s  |v|_max={np.abs(v).max()/1e3:9.1f} km/s")


if __name__ == "__main__":
    main()
    diagnosis()
