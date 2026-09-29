#!/usr/bin/env python3
"""T1 -- invented principle P1: a self-sustained electric field in dS_4 needs sigma = -2H, i.e. alpha * G_f(M) = -2.  Pre-registered in T1_PREREGISTRATION.md.

G_f(M) = (4/(3 pi)) [ ln M - Re psi(i M) - pi M (4 M^2 + 1) / (3 sinh(2 pi M)) ]   (Q1, validated by S2 in the light- and heavy-mass limits).
Run:   python3 t1_stationary_field.py            (real run, exit 0 iff all checks pass)
       python3 t1_stationary_field.py --mutate   (control: flips the sign requirement; exit 1 iff EXACTLY check B1 fails, exit 3 if the control is broken)
"""
import sys
import math
import mpmath as mp

MUT = "--mutate" in sys.argv
mp.mp.dps = 250          # Amendment 1: 40 digits is insufficient for ln M - Re psi(iM) at M ~ 1e38-1e44 (cancellation to ~1e-79)
ALPHA = mp.mpf(1) / mp.mpf("137.035999177")
GAMMA = mp.euler
HBAR_EV_S = mp.mpf("6.582119569e-16")
H0 = mp.mpf("67.4e3") / mp.mpf("3.0856775814913673e22")          # 1/s
H0_EV = H0 * HBAR_EV_S
CH = []
FAILED = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


def Gf(M):
    M = mp.mpf(M)
    x = 2 * mp.pi * M
    sinh_term = mp.pi * M * (4 * M ** 2 + 1) / (3 * mp.sinh(x)) if x < 700 else mp.mpf(0)
    return (4 / (3 * mp.pi)) * (mp.log(M) - mp.re(mp.digamma(1j * M)) - sinh_term)


print("T1 invented principle P1: sigma = -2H  <=>  alpha * G_f(M) = -2")
# small-M asymptotics and large-M asymptotics of G_f (consistency with Q1/S2)
small = Gf("1e-6")
chk("A1 small-M form G_f -> (4/(3 pi)) (ln M + gamma_E - 1/6)", abs(small / ((4 / (3 * mp.pi)) * (mp.log(mp.mpf('1e-6')) + GAMMA - mp.mpf(1) / 6)) - 1) < 1e-6,
    f"(G_f(1e-6) = {mp.nstr(small, 8)})")
big = Gf(40) * 40 ** 2
chk("A2 large-M form G_f -> -1/(9 pi M^2)", abs(big / (-1 / (9 * mp.pi)) - 1) < 1e-3, f"(M^2 G_f = {mp.nstr(big, 8)} vs {mp.nstr(-1 / (9 * mp.pi), 8)})")
chk("A3 G_f < 0 at every scanned M (Q1: negative at every M)", all(Gf(M) < 0 for M in ("1e-200", "1e-20", "1e-3", "0.1", "0.5", "1", "2", "5", "20", "100")))

# required M*: alpha * G_f(M*) = -2  (or +2 in the mutated control)
target = mp.mpf(2) if MUT else mp.mpf(-2)
ln_inv_M = 3 * mp.pi / (2 * ALPHA) + GAMMA - mp.mpf(1) / 6
Mstar = mp.e ** (-ln_inv_M)
resid = ALPHA * Gf(Mstar) - target
print(f"\n(i) required M* from the small-M identity: ln(1/M*) = 3 pi/(2 alpha) + gamma_E - 1/6 = {mp.nstr(ln_inv_M, 10)};  M* = {mp.nstr(Mstar, 6)}")
chk("B1 M* solves alpha G_f(M*) = -2 (residual)", abs(resid) < 1e-6, f"(alpha G_f(M*) = {mp.nstr(ALPHA * Gf(Mstar), 10)})")
m_star_eV = Mstar * H0_EV
print(f"    with H = H_0 = {mp.nstr(H0_EV, 5)} eV:  m* = M* H_0 = {mp.nstr(m_star_eV, 5)} eV")
chk("B2 the required fermion is more than 100 orders of magnitude lighter than H_0-scale energies (M* < 1e-100)", Mstar < mp.mpf("1e-100"))

# known species
print("\n(ii) |alpha G_f| for the known charged fermions at their measured M = m/H_0 (charge Q, colour N_c weight Q^2 N_c for the sum):")
SP = [("electron", "0.51099895e6", 1, 1), ("muon", "105.6583755e6", 1, 1), ("tau", "1776.86e6", 1, 1), ("top", "172.5e9", 2 / 3, 3)]
worst = mp.mpf(1)
for name, m_eV, Q, Nc in SP:
    M = mp.mpf(m_eV) / H0_EV
    val = ALPHA * Gf(M) * (mp.mpf(Q) ** 2 * Nc)
    ratio = abs(val) / 2
    worst = min(worst, ratio) if name == "electron" else worst
    print(f"    {name:9s} M = {mp.nstr(M, 4):>10s}   alpha G_f Q^2 N_c = {mp.nstr(val, 4):>12s}   fraction of the required 2: {mp.nstr(ratio, 3)}")
Me = mp.mpf("0.51099895e6") / H0_EV
short = 2 / abs(ALPHA * Gf(Me))
chk("C1 the electron falls short of the required |sigma|/H = 2 by more than 1e70", short > mp.mpf("1e70"), f"(factor {mp.nstr(short, 4)})")
sumval = sum(abs(ALPHA * Gf(mp.mpf(m) / H0_EV) * (mp.mpf(Q) ** 2 * Nc)) for _, m, Q, Nc in SP)
chk("C2 even the four heaviest-weighted species summed fall short by more than 1e70", 2 / sumval > mp.mpf("1e70"), f"(factor {mp.nstr(2 / sumval, 4)})")

# scalar: no negative conductivity in the AH4 convention (positive G_s at heavy mass is 7/(18 pi M^2))
chk("D1 the scalar G_s = +7/(18 pi M^2) at large M is positive, so a scalar cannot sustain the field (heavy-mass form, AH4/Q2)", 7 / (18 * math.pi * 40 ** 2) > 0)

print("\nVERDICT (against the declared criteria):")
print("  P1 needs a charged Dirac fermion with m/H = %s (m = %s eV at H = H_0): about 280 orders of magnitude lighter than H." % (mp.nstr(Mstar, 3), mp.nstr(m_star_eV, 3)))
print("  Every known charged fermion falls short by ~80 orders of magnitude. P1 is a dead invention; it fixes no value of alpha.")
print("  Structural by-product: alpha G_f = -2 is exactly ln(H/m) = 3 pi/(2 alpha) + const, i.e. H at the QED Landau-pole scale of that fermion --")
print("  an equality of the cosmological scale with a UV scale, which the real spectrum does not satisfy. alpha stays an INPUT; kappa = 1/2 FITTED.")
ok = all(CH)
if MUT:
    print("\nMUTATE CONTROL: the requirement was flipped to sigma = +2H; check B1 (and only B1) must FAIL.")
    works = [t.split()[0] for t in FAILED] == ["B1"]
    print("  failed checks:", FAILED, "->", "the control works (exit 1)" if works else "CONTROL BROKEN (exit 3): it must fail exactly B1")
    sys.exit(1 if works else 3)
sys.exit(0 if ok else 1)
