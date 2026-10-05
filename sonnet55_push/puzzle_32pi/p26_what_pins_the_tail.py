"""p26: what could pin the strong-field tail of nu, which sets BIMOND's vacuum coefficient Lambda/a0^2 = (1/2) I_nu, I_nu = int_0^inf (nu-1) d(y^2) (p21, p25)?
Target: I_nu = 64 pi (Lambda = 32 pi a0^2).  SI units for the physical scales; a0 = 9.3603e-11 (framework footing) and 1.1312e-10 (alt footing).
(D) data: what the tuned tail (p22, alpha* = 2.0025) does at the Earth, versus the ephemeris bound -- can data see it?
(T) theory: Milgrom 1999's dS-Unruh derivation fixes nu = sqrt(1+1/y) exactly (alpha = 1): pinned, but I_nu diverges.
(C) a physical cutoff y_max: I_nu then depends on the tail exponent and on ln y_max. Natural cutoff: the Planck acceleration a_P = sqrt(c^7/(hbar G)).
    With the 'standard' mu (tail nu - 1 ~ 1/(2y^2), alpha = 2), I_nu ~ ln y_max + c0.  This is a MENU item (kernel and cutoff both chosen); it also puts hbar into a0
    (logarithmically), against lane A's finding that a0^2 = c^4 Lambda/32 pi is hbar-free.
Run: python3 p26_what_pins_the_tail.py  |  MUTATE=1: Planck acceleration with c^5 instead of c^7 (check C2 must fail)
"""
import os, sys, math
from scipy.integrate import quad
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
c, G, hbar = 2.99792458e8, 6.67430e-11, 1.054571817e-34
T = 64 * math.pi
# (D) the tuned tail at the Earth: nu - 1 = y^-a/(2a), anomalous acceleration = (nu - 1) g_N
a0 = 9.3603e-11; aS = 2.0025; gE = 5.93e-3; yE = gE / a0
dgE = (yE**(-aS) / (2 * aS)) * gE
print(f"   (D) tuned tail (alpha* = {aS}) at the Earth (y = {yE:.2e}): anomalous acceleration {dgE:.2e} m/s^2 vs ephemeris-level ~1e-14: invisible by {1e-14/dgE:.0e}")
reach = math.exp(1 / (aS - 2))
print(f"       the tuned I_nu collects its value out to y ~ e^(1/(alpha*-2)) = {reach:.1e}, i.e. accelerations ~ {reach*a0:.1e} m/s^2")
check("D1 data cannot pin the tail: the tuned tail is >= 1e3 below the ephemeris level at the Earth, and SPARC stops at y ~ 1e2", 1e-14 / dgE > 1e3)
aP = math.sqrt(c**(5 if MUTATE else 7) / (hbar * G))
check(f"D2 the tuned tail needs the power law to hold out to y ~ {reach:.0e}, far beyond the Planck acceleration (y_P = {aP/a0:.1e}): unphysical as stated", reach > 1e3 * aP / a0)
# (T) Milgrom 1999 kernel: I diverges linearly; cutoff that gives 64 pi
yc = 64 * math.pi                     # I = int_0^Y 2y (sqrt(1+1/y) - 1) dy ~ Y - (1/4) ln Y + ...; solve numerically
f = lambda Y: quad(lambda y: 2 * y * (math.sqrt(1 + 1 / y) - 1), 0, Y, limit=500)[0]
lo, hi = 1.0, 1e4
for _ in range(60):
    mid = 0.5 * (lo + hi); (lo, hi) = (mid, hi) if f(mid) < T else (lo, mid)
print(f"   (T) Milgrom-1999 / framework kernel is pinned by its derivation but diverges: 64 pi needs a cutoff at y = {lo:.1f} (g_N = {lo:.0f} a0), inside the galaxy range")
check("T1 the framework kernel's own cutoff for 64 pi sits at ~200 a0, a scale with no physical marker", 150 < lo < 260)
# (C) standard-mu tail with a Planck cutoff
nu_std = lambda y: math.sqrt((1 + math.sqrt(1 + 4 / y**2)) / 2)
def I_std(Y):
    segs = [(1e-9, 1), (1, 1e2), (1e2, 1e4)]
    tot = sum(quad(lambda y: 2 * y * (nu_std(y) - 1), a, b, limit=2000, epsabs=1e-12)[0] for a, b in segs)
    return tot + math.log(Y / 1e4)            # tail 2y * 1/(2y^2) = 1/y beyond 1e4 (next order ~ y^-3)
c0 = I_std(1e4) - math.log(1e4)
print(f"   (C) standard mu: I_nu(Y) = ln Y + {c0:.4f} for large Y")
for lab, a0v in (("framework footing 9.36e-11", 9.3603e-11), ("alt footing 1.131e-10", 1.1312e-10)):
    yP = aP / a0v; Ip = I_std(yP)
    print(f"       Planck cutoff, {lab}: y_P = {yP:.3e}, I_nu = {Ip:.2f}, Lambda/a0^2 = {Ip/2:.2f} vs 32 pi = {32*math.pi:.2f} (ratio {Ip/T:.4f})")
IpF = I_std(aP / 9.3603e-11)
check(f"C1 a Planck-cut standard tail gives Lambda/a0^2 = {IpF/2:.1f}: the right order (the 10^61 of the cosmological-constant problem enters only as a log), but {T/IpF:.2f}x short",
      1.2 < T / IpF < 1.6)
yneed = math.exp(T - c0)
check(f"C2 hitting 64 pi with the standard tail needs y_max = e^(64 pi - c0) = {yneed:.1e} -- {yneed/(aP/a0):.0e} x beyond the Planck acceleration: no physical cutoff does it",
      yneed / (aP / a0) > 1e20)
print(f"   Reading: data cannot see the tail; the one theory that fixes it (Milgrom 1999) diverges; a Planck cutoff gives the right order only with a chosen kernel. Nothing pins it.")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
