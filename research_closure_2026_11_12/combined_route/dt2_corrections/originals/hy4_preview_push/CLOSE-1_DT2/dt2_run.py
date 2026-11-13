#!/usr/bin/env python3
"""CLOSE-1 / DT2: the formation run and the reach, 4 masses x 2 footings  (K3).

Produces: the first fold time, the settled reach R_set(0), the residual against form B's
static halo at the KiDS inner-window edge, and the diagnosis of why the run ends as it does
(infall speed vs the DT2 sound speed at the compression actually reached).
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
        print(f"{'log M_b':>7} {'t_fold[Gyr]':>11} {'M_cen/M_b':>10} {'R_set(0)':>10} "
              f"{'R_KiDS':>8} {'M_stat/M_b':>11} {'M_set/M_stat':>12} {'residual':>10} "
              f"{'FLD1 R_fold':>12} {'cover?':>8}")
        print("-" * 118)
        for lm in MASSES:
            res = F.run(lm, a0)
            M_b = res['M_b']
            t, a, Ff, v, s, rj, Mcen, dm = res['snaps'][-1]
            rM = D.r_M(M_b, a0)
            Rk = KIDS_INNER[lm] * KPC
            M_stat = M_b * D.X_formB(Rk / rM)
            Md_in = np.cumsum(dm) - 0.5 * dm + Mcen
            # settled charge inside the KiDS inner window = everything interior + the centre
            M_set = Mcen + float(np.sum(dm[rj <= Rk]))
            resid = abs(M_set - M_stat) / M_stat
            Rset, rj2, v2, vcirc, slow = F.settled_radius(res, a0)
            ff = res['first_fold']
            tf = (ff - float(F.T_OF_A(1 / 11.))) / 1e9 / F.YR if ff else float('nan')
            cover = "PASS" if Rset >= Rk else "FAIL"
            print(f"{lm:7.2f} {tf:11.4f} {Mcen / M_b:10.2f} {Rset / KPC:10.1f} "
                  f"{KIDS_INNER[lm]:8.0f} {M_stat / M_b:11.2f} {M_set / M_stat:12.4f} "
                  f"{resid:10.4f} {FLD1_RFOLD[lm]:12.0f} {cover:>8}")
            out[(lab, lm)] = dict(t_fold=tf, Mcen_Mb=Mcen / M_b, Rset=Rset / KPC,
                                  M_stat=M_stat / M_b, M_set=M_set / M_stat, resid=resid)
    return out


def diagnosis(lm=10.45, a0=D.A0_CANON):
    """Why: compare the infall speed with the DT2 sound speed at the compression reached."""
    print("\n" + "=" * 118)
    print("WHY: infall speed vs the DT2 sound speed along the collapse (log M_b %.2f, %s)"
          % (lm, "canonical" if a0 == D.A0_CANON else "alt"))
    print("=" * 118)
    res = F.run(lm, a0, absorb=False)
    print(f"first fold at t = {(res['first_fold'] - float(F.T_OF_A(1/11.)))/1e9/F.YR:.4f} Gyr"
          f"   (COL1's cold clock: {COL1_FOLD_T[0]} to {COL1_FOLD_T[1]} Gyr)")
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
