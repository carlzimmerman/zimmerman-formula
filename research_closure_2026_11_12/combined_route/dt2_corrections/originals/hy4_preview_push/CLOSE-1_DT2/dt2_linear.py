#!/usr/bin/env python3
"""CLOSE-1 / DT2 check 1: the linear / Jeans behaviour in and around the band.

Two things are computed.

(A) The local linear closure at every epoch:
      c_ad^2 = n/(Q n'),  M_sus^2 = Q^2 n',  c_eff^2(k) = c_ad^2/(1 + k_phys^2/M_sus^2),
      omega^2(k) = -n_charge * Q^2 n'/(Q^2 n' + k_phys^2)      [law on, TPA1 S4.4 epsilon = 1]
    and the isolated-fluid (epsilon = 0) Jeans wavenumber k_J^2 = Q^2 n' (IC1 / audit S2).

(B) The growth factor of a mode, integrated through the band in the record's background:
      delta'' + [3 + dlnH/dlna] delta' = 1.5 Omega_m(a) F(k,a) delta,   ' = d/dln a,
      F(k,a) = Q^2 n' /(Q^2 n' + k_phys^2),
    against the pressureless reference F = 1.  This is K1.
"""
import numpy as np
from scipy.integrate import solve_ivp
import dt2_function as D

OM_M = 0.31
OM_L = 1.0 - OM_M


def E2(a):
    return OM_M * a ** -3 + OM_L


def dlnH_dlna(a):
    return 0.5 * (-3.0 * OM_M * a ** -3) / E2(a)


def Om_of_a(a):
    return OM_M * a ** -3 / E2(a)


def F_suppress(kcom_Mpc, a):
    """Law-on growth-suppression factor at comoving wavenumber kcom (Mpc^-1)."""
    q = a ** -3
    xbar = float(D.x_of_q(q))
    Qb = 1.0 + xbar
    npr = float(D.nprime_of_q(q))          # Mpc^-2
    Msus2 = Qb ** 2 * npr                  # Mpc^-2
    kphys2 = (kcom_Mpc / a) ** 2           # Mpc^-2
    return Msus2 / (Msus2 + kphys2)


def growth_factor(kcom_Mpc, a_start, a_end=1.0, dt2=True):
    """D(a_end)/D(a_start) for the growing mode (initialised deep in a ~ a)."""
    def rhs(lna, y):
        a = np.exp(lna)
        d, dp = y
        F = F_suppress(kcom_Mpc, a) if dt2 else 1.0
        ddp = 1.5 * Om_of_a(a) * F * d - (3.0 + dlnH_dlna(a)) * dp
        return [dp, ddp]

    a0 = a_start
    # growing-mode initial condition at a0 (matter-dominated early enough at a<=1/7)
    y0 = [a0, a0]
    sol = solve_ivp(rhs, [np.log(a0), np.log(a_end)], y0, rtol=1e-10, atol=1e-14,
                    dense_output=True, method='DOP853')
    return sol.y[0, -1] / y0[0]


def main():
    print("=" * 96)
    print("DT2 LINEAR CHECK  (canonical construction: q1=2, q2=26, L=8.00e-6, M=400 Mpc^-2)")
    print("=" * 96)
    print(f"n0 = {D.N0:.10e} Mpc^-2   A = {D.A_jump():.6e}   x(27) = {float(D.x_of_q(27)):.6e}")
    print()
    print("(A) local closure along the background q = a^-3")
    hdr = (f"{'z':>6} {'a':>8} {'q':>10} {'x_bar':>11} {'n_prime':>11} {'c_ad^2':>11} "
           f"{'c_ad[km/s]':>11} {'k_J[1/Mpc]':>11} {'F(20/Mpc)':>11} {'F(0.2/Mpc)':>11} {'F(2/Mpc)':>11}")
    print(hdr)
    print("-" * len(hdr))
    for z in [6.0, 5.0, 4.0, 3.0, 2.5, 2.0, 1.968, 1.74, 1.412, 1.04, 0.8, 0.5, 0.260, 0.1, 0.0]:
        a = 1.0 / (1.0 + z)
        q = a ** -3
        xb = float(D.x_of_q(q))
        npr = float(D.nprime_of_q(q))
        cad2 = float(D.c_ad2_of_x(xb))
        cad = np.sqrt(cad2) * D.C_SI / 1e3
        kJ = np.sqrt((1 + xb) ** 2 * npr)
        row = (f"{z:6.3f} {a:8.4f} {q:10.3f} {xb:11.4e} {npr:11.5f} {cad2:11.4e} {cad:11.1f} "
               f"{kJ:11.4f} {F_suppress(20.0, a):11.3e} {F_suppress(0.2, a):11.3e} {F_suppress(2.0, a):11.3e}")
        print(row)

    print()
    print("(B) growth factor from z = 6 to z = 0, DT2 vs the pressureless reference  (K1)")
    print(f"{'k_com[1/Mpc]':>13} {'k_phys(z=2)':>12} {'k_phys(z=0)':>12} {'D_DT2':>10} "
          f"{'D_ref':>10} {'D_DT2/D_ref':>12} {'line>=0.50':>11}")
    print("-" * 82)
    out = {}
    for kcom in [20.0 / 3.0, 6.667, 2.0, 0.2, 0.02]:
        ddt = growth_factor(kcom, 1 / 7.0, dt2=True)
        dref = growth_factor(kcom, 1 / 7.0, dt2=False)
        ratio = ddt / dref
        out[kcom] = (ddt, dref, ratio)
        flag = "PASS" if ratio >= 0.50 else "FAIL"
        print(f"{kcom:13.3f} {kcom * 3.0:12.3f} {kcom:12.3f} {ddt:10.4f} {dref:10.4f} "
              f"{ratio:12.5f} {flag:>11}")

    print()
    print("Growth factor in slices (k_com = 6.667/Mpc, i.e. k_phys = 20/Mpc at z = 2):")
    for a0, a1, lab in [(1 / 7., 1 / 3., "z 6 -> 2 (above the band)"),
                        (1 / 3., 1 / 2.968, "z 2 -> 1.968 (entering)"),
                        (1 / 2.968, 1 / 1.26, "z 1.968 -> 0.26 (the band)"),
                        (1 / 1.26, 1.0, "z 0.26 -> 0 (below the band)")]:
        ddt = growth_factor(6.667, a0, a1, dt2=True)
        dref = growth_factor(6.667, a0, a1, dt2=False)
        print(f"  {lab:34s} D_DT2 = {ddt:8.4f}  D_ref = {dref:8.4f}  ratio = {ddt / dref:9.5f}")
    return out


if __name__ == "__main__":
    main()
