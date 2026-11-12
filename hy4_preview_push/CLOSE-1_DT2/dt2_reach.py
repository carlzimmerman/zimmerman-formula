#!/usr/bin/env python3
"""CLOSE-1 / DT2: the settled / turned-around charge inside the KiDS inner window,
independent-shell (FLD1's method), so the residual per mass can be quoted.

Each shell: comoving radius x, physical r = a x, integrated with

    rddot = -G [ M_b(ramp) + M_c(<r) + (4 pi/3) rho_m0 x^3 ] / r^2  +  (Lambda c^2/3) r

which reproduces the FRW background exactly when the perturbation is removed.  The clock's
dust contributes neither pressure nor self-gravity here: the run shows the collapsing dust
sits at q ~ 5e3 (the cold branch, above the band) with c_ad = 159 km/s against an infall
speed of 2604 km/s, and in that limit the polarization's gravity cancels the pressure force
term by term (DT2.lean: lawon_force_balance, pressure_cancel_weak).  That makes this the
pressure-favouring side of nothing: it is simply the cold-clock dynamics COL1 and FLD1
already graded.
"""
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import cumulative_trapezoid
import dt2_function as D

KPC = D.KPC
OM_M, OM_L = 0.31, 0.69
H0_S = 70.0e3 / D.MPC
LAM_ACC = (H0_S ** 2) * OM_L   # the Lambda acceleration coefficient: (Lambda c^2/3) r

_AG = np.geomspace(1.0 / 21.0, 1.0, 4000)
_TG = cumulative_trapezoid(1.0 / (_AG * H0_S * np.sqrt(OM_M * _AG ** -3 + OM_L)),
                           np.log(_AG), initial=0.0)
_TG -= _TG[0]
A_OF_T = interp1d(_TG, _AG, kind='cubic', bounds_error=False, fill_value=(_AG[0], 1.0))
T_OF_A = interp1d(_AG, _TG, kind='cubic')


def shells(lm, a0, z_i=10.0, N=4000, x_min=0.02 * D.MPC, x_max=40.0 * D.MPC,
           ramp_Gyr=1.0, soften_kpc=1.0):
    """Returns (x comoving radii, r at z=0, turned-around mask, dm per shell)."""
    M_b = 10.0 ** lm * D.MSUN
    a_i = 1.0 / (1.0 + z_i)
    rM = D.r_M(M_b, a0)
    soft = soften_kpc * KPC
    x = np.exp(np.linspace(np.log(x_min), np.log(x_max), N))
    rho_m0 = OM_M * 3.0 * H0_S ** 2 / (8.0 * np.pi * D.G_SI)
    M_bg = (4.0 * np.pi / 3.0) * rho_m0 * x ** 3
    dm = D.RHO_C0 * (4.0 * np.pi / 3.0) * x ** 3          # dust mass per shell (comoving)
    r = a_i * x
    v = H0_S * np.sqrt(OM_M * a_i ** -3 + OM_L) * r
    t = float(T_OF_A(a_i))
    T0 = float(T_OF_A(1.0))
    t_ramp = ramp_Gyr * 1.0e9 * 3.1557e7
    turned = np.zeros(N, dtype=bool)
    folded = np.zeros(N, dtype=bool)
    dead = np.zeros(N, dtype=bool)
    r_floor = 1.0e-3 * x_min
    while t < T0:
        a = float(A_OF_T(t))
        act = ~dead
        if not act.any():
            break
        rr = np.where(act, r, np.inf)
        dt = min((T0 - t) * 0.5,
                 0.02 * np.sqrt(np.min(rr) / max(np.max(np.abs(
                     -D.G_SI * M_bg[act] / r[act] ** 2 + LAM_ACC * r[act])), 1e-30)),
                 2.0e14)
        dt = max(dt, 1.0e11)
        ramp = min(1.0, max(0.0, (t - float(T_OF_A(a_i))) / t_ramp))
        Mc = M_b * D.X_formB(r / rM)
        Mb_r = M_b * ramp * r ** 3 / (r ** 2 + soft ** 2) ** 1.5
        acc = -D.G_SI * (Mb_r + Mc + M_bg) / r ** 2 + LAM_ACC * r
        v_half = v + 0.5 * acc * dt
        r = r + v_half * dt
        turned |= (v_half < 0.0) & act
        newly = (r <= r_floor) & act
        folded |= newly
        dead |= newly
        r = np.where(dead, r_floor, r)
        v = np.where(dead, 0.0, v)
        Mc2 = M_b * D.X_formB(r / rM)
        acc2 = -D.G_SI * (M_b * ramp * r ** 3 / (r ** 2 + soft ** 2) ** 1.5 + Mc2 + M_bg) / r ** 2 \
            + LAM_ACC * r
        v = v_half + 0.5 * acc2 * dt
        v = np.where(dead, 0.0, v)
        t += dt
    return x, r, turned, folded, dm, M_b, rM


def main():
    KIDS = {9.4: 81.0, 10.45: 272.0, 10.7: 362.0, 10.9: 456.0}
    print("=" * 112)
    print("DT2 SETTLED / TURNED-AROUND CHARGE INSIDE THE KiDS INNER WINDOW (independent shells)")
    print("=" * 112)
    print(f"{'footing':>10} {'log M_b':>7} {'R_KiDS':>7} {'M_stat/M_b':>10} {'R_ta(0)':>9} "
          f"{'R_fold(0)':>10} {'M_ta/M_stat':>12} {'residual':>9}")
    print("-" * 112)
    rows = {}
    for a0, lab in [(D.A0_CANON, "canonical"), (D.A0_ALT, "alt")]:
        for lm in [9.4, 10.45, 10.7, 10.9]:
            x, r, turned, folded, dm, M_b, rM = shells(lm, a0)
            Rk = KIDS[lm] * KPC
            M_stat = M_b * D.X_formB(Rk / rM)
            # turned-around dust whose CURRENT radius is inside the KiDS window
            inside = (r <= Rk)
            M_ta = float(np.sum(dm[turned & inside]))
            Rta = float(np.max(r[turned & ~folded])) if (turned & ~folded).any() else 0.0
            Rfo = float(np.max(x[folded])) if folded.any() else 0.0
            resid = abs(M_ta - M_stat) / M_stat
            print(f"{lab:>10} {lm:7.2f} {KIDS[lm]:7.0f} {M_stat / M_b:10.2f} "
                  f"{Rta / KPC:9.1f} {Rfo / KPC:10.1f} {M_ta / M_stat:12.4f} {resid:9.4f}")
            rows[(lab, lm)] = (M_ta / M_stat, resid, Rta / KPC)
    return rows


if __name__ == "__main__":
    main()
