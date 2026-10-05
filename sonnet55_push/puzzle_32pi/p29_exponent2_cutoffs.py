"""p29: tail exponent exactly 2, different cutoffs. With nu - 1 ~ A/y^2 the BIMOND vacuum integral is I = 2A ln Y + c (log-divergent), so Lambda/a0^2 = A ln Y + c/2.
Kernels: F2 n = 2 ('standard', A = 1/2), F1 a = 2 (A = 1/4). Cutoffs a_cut = E c/hbar for physical energy scales (electron, proton, electroweak vev, GUT, Planck);
Y = a_cut/a0 (framework footing). Also: the cutoff each kernel NEEDS for 32 pi, and the amplitude A needed at the Planck cutoff.
Run: python3 p29_exponent2_cutoffs.py  |  MUTATE=1: standard kernel's tail amplitude taken as 1/4 (check C must fail)
"""
import os, sys, math
from scipy.integrate import quad
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
c, G, hbar, eV = 2.99792458e8, 6.67430e-11, 1.054571817e-34, 1.602176634e-19
a0 = 9.3603e-11; T = 64 * math.pi
N1 = lambda y: math.expm1(math.log1p(y**-2) / 4)
N2 = lambda y: math.expm1(math.log1p(2 * y**-2 / (1 + math.sqrt(1 + 4 * y**-2))) / 2)
Y0 = 1e4; segs = ((1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, Y0))
core = lambda e: sum(quad(lambda y: 2 * y * e(y), s, t, limit=2000, epsabs=1e-12, epsrel=1e-11)[0] for s, t in segs)
kern = {"F1 a=2 (A=1/4)": (N1, 0.25), "standard (A=1/2)": (N2, 0.25 if MUTATE else 0.5)}
cst = {k: core(e) - 2 * A * math.log(Y0) for k, (e, A) in kern.items()}
I = lambda k, Y: 2 * kern[k][1] * math.log(Y) + cst[k]
scales = {"electron m_e c^2": 0.51099895e6, "proton m_p c^2": 938.272e6, "electroweak vev": 246.22e9, "GUT 2e16 GeV": 2e25, "Planck": math.sqrt(hbar * c**5 / G) / eV}
print(f"   {'cutoff':18s} {'a_cut (m/s^2)':>14s} {'ln Y':>7s}   " + "   ".join(f"{k}: Lambda/a0^2" for k in kern))
for nm, E in scales.items():
    acut = E * eV * c / hbar if nm != "Planck" else math.sqrt(c**7 / (hbar * G)); Y = acut / a0
    print(f"   {nm:18s} {acut:14.3e} {math.log(Y):7.2f}   " + "   ".join(f"{I(k, Y)/2:22.2f}" for k in kern))
print(f"   target 32 pi = {32*math.pi:.2f}")
need = {k: (T - cst[k]) / (2 * kern[k][1]) for k in kern}
aPl = math.sqrt(c**7 / (hbar * G)); lnYP = math.log(aPl / a0)
for k in kern: print(f"   {k}: 32 pi needs ln Y = {need[k]:.1f}, a_cut = {math.exp(need[k])*a0:.1e} m/s^2 = {math.exp(need[k])*a0/aPl:.1e} x Planck")
Aneed = (T - cst["standard (A=1/2)"]) / (2 * lnYP)
print(f"   at the Planck cutoff, exponent 2 needs tail amplitude A = {Aneed:.4f} (standard has 1/2, F1 1/4)")
check("A with exponent exactly 2 the vacuum grows only as ln(cutoff): every physical cutoff (electron ... Planck) gives Lambda/a0^2 between 20 and 72 for these kernels",
      all(20 < I(k, (E * eV * c / hbar if n != 'Planck' else aPl) / a0) / 2 < 72 for k in kern for n, E in scales.items()))
check("B no physical cutoff reaches 32 pi: both kernels need a cutoff beyond the Planck acceleration (by 1e25 and 1e112)", all(math.exp(v) * a0 > 1e20 * aPl for v in need.values()))
check(f"C the standard kernel's own cutoff for 32 pi is a_cut = e^(64 pi - c0) a0 with c0 = {cst['standard (A=1/2)']:.4f} (p26: 0.1931)", abs(cst["standard (A=1/2)"] - 0.1931) < 2e-3)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
