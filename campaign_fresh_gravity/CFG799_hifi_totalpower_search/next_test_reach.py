"""CFG799: reach of a purpose-built dish-antenna test of the two lines (table-top to 10 m^2).  Seconds.
Run: python3 -I next_test_reach.py
Same signal and noise formulas as CFG797 (P = (2/3) eps^2 rho c^3 A / S, sigma_P = kB T sqrt(dnu/t), 5 sigma), with the
geometry/coupling suppression S that CFG798 and CFG799 use (S = 1 is CFG797).  All inputs are provisional; T_sys values are
examples (a warm Schottky receiver at 600 GHz has been reported below 1200 K DSB, which is ~2400 K for a line in one sideband).
kappa = 1/2 FITTED; not theory closed.
"""
import math

c, kB, MSUN, PC = 2.99792458e8, 1.380649e-23, 1.989e30, 3.0857e16
rho = 0.01 * MSUN / PC ** 3
SIG = 2.3e5
LINES = (("541.664 GHz (canonical)", 541.664e9), ("595.463 GHz (alt)", 595.463e9))


def eps_min(A, T, t, nu, S):
    dnu = nu * (SIG / c) ** 2
    Ps = (2 / 3) * 1e-24 * rho * c ** 3 * A / S          # W at eps = 1e-12
    snr = Ps / (kB * T * math.sqrt(dnu / t))
    return 1e-12 * math.sqrt(5 / snr)


# K1: reproduce CFG797's published rows at S = 1 (541.7 GHz line width from the canonical value)
nu0 = 541.7e9
k1 = [(1.0, 1000.0, 3600.0, 7e-12), (1.0, 1000.0, 30 * 86400.0, 1.4e-12), (10.0, 100.0, 30 * 86400.0, 1.4e-13), (1.0, 100.0, 30 * 86400.0, 4.5e-13)]
ok = all(abs(eps_min(A, T, t, nu0, 1.0) / want - 1) < 0.1 for A, T, t, want in k1)
print(f"K1 reproduces CFG797 rows at S = 1 (within 10%): {'PASS' if ok else 'FAIL'}")
assert ok
print("\neps_min (5 sigma) for the line at 541.664 GHz / 595.463 GHz; kill line 1e-12, converter window 4e-9")
print("  A[m^2] T_sys[K]  time    S=1                 S=10                S=50")
for A in (1.0, 10.0):
    for T, lab in ((100.0, "SIS 100"), (1000.0, "warm 1000"), (2400.0, "warm 2400")):
        for tl, t in (("1 h", 3600.0), ("30 d", 30 * 86400.0), ("1 yr", 365 * 86400.0)):
            cells = []
            for S in (1.0, 10.0, 50.0):
                e = [eps_min(A, T, t, nu, S) for _, nu in LINES]
                cells.append(f"{e[0]:.1e} / {e[1]:.1e}")
            print(f"  {A:5.0f}  {lab:9s} {tl:5s}  " + "   ".join(cells))
print("\nreaches the kill line (eps_min <= 1e-12) at S = 50 only for:")
for A in (1.0, 10.0, 100.0):
    for T, lab in ((100.0, "SIS 100"), (1000.0, "warm 1000"), (2400.0, "warm 2400")):
        for tl, t in (("30 d", 30 * 86400.0), ("1 yr", 365 * 86400.0)):
            if max(eps_min(A, T, t, nu, 50.0) for _, nu in LINES) <= 1e-12:
                print(f"  A = {A:g} m^2, {lab}, {tl}")
w = lambda A, T, t, S: max(eps_min(A, T, t, nu, S) for _, nu in LINES)
print(f"\nconverter window (4e-9) covered by x{4e-9 / w(1.0, 2400.0, 3600.0, 50.0):.0f} even for 1 m^2, warm 2400 K, 1 h, S = 50")
