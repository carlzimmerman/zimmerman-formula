#!/usr/bin/env python3
"""P3 -- independent recomputation, from stated inputs only, of the numbers in ALPHA_CHAIN_STATUS.md that are cheap to re-derive.

Pre-registered in P_PREREGISTRATION.md (protocol item 7).  Written from the declared formulas; NO lane script is imported or read at run time.
Inputs (declared): CODATA 1/alpha = 137.035999177, delta_CODATA = 1.6e-10, c, G, hbar (SI, 2019 values), H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.6847,
m_e = 0.51099895 MeV, 1/alpha_em(m_Z) = 127.930 (lanes B, C, M4) or 127.95 (lanes A, F, M1), sin^2 theta_W = 0.23122, m_Z = 91.1876 GeV, M_Planck = 1.22089e19 GeV.
Each line prints  [PASS|FAIL] tag: document value vs recomputed value (tolerance).  Exit 0 iff every check passes.

Run:     PYTHONDONTWRITEBYTECODE=1 python3 p3_independent_numbers.py
CONTROL: PYTHONDONTWRITEBYTECODE=1 python3 p3_independent_numbers.py MUTATE
         (the ONLY trigger is argv[1] == "MUTATE": the hypercharge coefficient is replaced by the known-wrong 3/5*41/10 (lane A's bug);
          the b_Y check, the m_P checks, the Z-offset checks and the f_g / M4 checks must fail -> exit 1)
"""
import math
import sys
from fractions import Fraction as F
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
FAILS = []


def chk(tag, doc, val, tol, note=""):
    ok = abs(val / doc - 1) <= tol
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}: document {doc:g}  recomputed {float(val):.6g}  (tol {tol:g}) {note}")
    if not ok:
        FAILS.append(tag)


def chk_bool(tag, cond, note=""):
    print(f"  [{'PASS' if cond else 'FAIL'}] {tag} {note}")
    if not cond:
        FAILS.append(tag)


c, G, hbar = mp.mpf("299792458"), mp.mpf("6.67430e-11"), mp.mpf("1.054571817e-34")
Mpc = mp.mpf("3.0856775814913673e22")
H0s = mp.mpf("67.4e3") / Mpc
OL = mp.mpf("0.6847")
alpha = 1 / mp.mpf("137.035999177")
lP2 = G * hbar / c ** 3
Lam = 3 * OL * H0s ** 2 / c ** 2
x = Lam * lP2
GEV_PER_KG = c ** 2 / mp.mpf("1.602176634e-10")
me_kg = mp.mpf("9.1093837015e-31")

print("== chain row 1 / AH5: x = Lambda l_P^2")
chk("S02 x = 2.85e-122", 2.85e-122, x, 0.01)

print("== chain row 4 / AH6: KK relation numbers (n = 1, alpha_n = 4 l_P^2/R^2)")
k = 2 / mp.sqrt(alpha)
lP = mp.sqrt(lP2)
MKK = hbar / (k * lP * c) * GEV_PER_KG
ratio_e = me_kg * (k * lP) * c / hbar
chk("S11 R/l_P = 23.41", 23.41, k, 1e-3)
chk("S11 M_KK = 5.2e17 GeV", 5.2e17, MKK, 0.01)
chk("S11 m_e R c/hbar = 1e-21 (document rounds 9.8e-22)", 1e-21, ratio_e, 0.03)
chk_bool("S11 tree relation at alpha^-1 = 106.8 (F3 T5 scale) needs R/l_P = 20.67, not 23.41", abs(2 * mp.sqrt(mp.mpf("106.8")) - 20.67) < 0.01,
        f"(2 sqrt(106.8) = {float(2 * mp.sqrt(mp.mpf('106.8'))):.3f})")

print("== lane A: n_max and the minimal-object size")
Nmax = 1 / (2 * mp.sqrt(alpha * x))
chk("S14 n ~ 3.5e61", 3.5e61, Nmax, 0.02)
k_th = 1 / (2 * mp.sqrt(alpha))
Z = 2 * mp.sqrt(8 * mp.pi / 3)
chk_bool("S14 required minimal-object size k = 1/(2 sqrt(alpha)) = 5.853 at Thomson; Z within 1.1% of it", abs(Z / k_th - 1) < 0.0115 and abs(k_th - 5.8531) < 1e-3,
         f"(Z/k = {float(Z / k_th):.4f})")

print("== lanes B/M: SM one-loop chain to the Planck mass, b_Y from field content (exact Fractions)")
gen = [(6, F(1, 6)), (3, F(2, 3)), (3, F(-1, 3)), (2, F(-1, 2)), (1, F(-1))]
bY_F = F(2, 3) * 3 * sum(n * y * y for n, y in gen) + F(1, 3) * 2 * F(1, 2) ** 2
if MUT:
    bY_F = F(3, 5) * F(41, 10)                                           # the lane-A bug
b2_F = -F(11, 3) * 2 + F(2, 3) * 12 * F(1, 2) + F(1, 3) * F(1, 2)
print(f"  b_Y = {bY_F} = {float(bY_F):.4f}, b_2 = {b2_F}")
chk_bool("b_Y = 41/6 and b_2 = -19/6 from field content", bY_F == F(41, 6) and b2_F == F(-19, 6))
bY, b2 = mp.mpf(bY_F.numerator) / bY_F.denominator, mp.mpf(b2_F.numerator) / b2_F.denominator
s2 = mp.mpf("0.23122")
mZ, mP = mp.mpf("91.1876"), mp.mpf("1.22089e19")
L = mp.log(mP / mZ)
res = {}
for aem in (mp.mpf("127.930"), mp.mpf("127.95")):
    aY = aem * (1 - s2) - bY / (2 * mp.pi) * L
    a2 = aem * s2 - b2 / (2 * mp.pi) * L
    res[round(float(aem), 2)] = (aY, a2, aY + a2)
    print(f"  input 1/alpha(m_Z) = {aem}: 1/alpha_Y(m_P) = {float(aY):.3f}, 1/alpha_2(m_P) = {float(a2):.3f}, 1/alpha_em(m_P) = {float(aY + a2):.3f}")
chk("S17/S35 1/alpha_em(m_P) = 104.94 (input 127.95)", 104.94, res[127.95][2], 2e-4)
chk("S17 1/alpha_em(m_P) ~ 105 (input 127.930, lane B prints 104.917)", 104.917, res[127.93][2], 2e-4)
k_P = mp.sqrt(res[127.95][2]) / 2
chk("S35 required k at m_P = 5.12", 5.12, k_P, 1e-3)
off_k = Z / k_P - 1              # offset of Z relative to the required k
off_Z = 1 - k_P / Z              # offset of the required k relative to Z
print(f"  Z = {float(Z):.4f}: Z/k - 1 = {float(off_k) * 100:.2f} %, 1 - k/Z = {float(off_Z) * 100:.2f} %  (document '12-13%'; lane A prints -12.0 = 2-significant-digit rounding of -11.5)")
chk_bool("S35 the document's '12-13%' = 13.0% relative to k and 11.5% relative to Z", abs(off_k * 100 - 13.0) < 0.1 and abs(off_Z * 100 - 11.5) < 0.1)
bug = mp.mpf("127.95") * (1 - s2) - (F(3, 5) * F(41, 10)).numerator / mp.mpf((F(3, 5) * F(41, 10)).denominator) / (2 * mp.pi) * L + mp.mpf("127.95") * s2 - b2 / (2 * mp.pi) * L
chk("S35 the buggy b_Y = 3/5*41/10 gives 132.39 and Z/k = 1.006 (the VOID remark)", 132.39, bug, 2e-4,
    f"Z/k_bug = {float(Z / (mp.sqrt(bug) / 2)):.4f}")

print("== lane B: precision needed of f_g and the universal-f sign statement (Eichhorn-Versteegen form beta_g = -f g + b g^3/(16 pi^2))")
MPL = mp.mpf("1.22089e19")
aY_mt = mp.mpf("127.930") * (1 - s2) - bY / (2 * mp.pi) * mp.log(mp.mpf(173) / mZ)
g2_meas = 4 * mp.pi / aY_mt
u_req = 1 / g2_meas - bY / (8 * mp.pi ** 2) * mp.log(MPL / 173)          # 1/g*^2 required
f_req = bY * (1 / u_req) / (16 * mp.pi ** 2)
def alphaY_inv_173(f):
    gstar2 = 16 * mp.pi ** 2 * f / bY
    return 4 * mp.pi * (1 / gstar2 + bY / (8 * mp.pi ** 2) * mp.log(MPL / 173))
h = f_req * mp.mpf("1e-8")
el = (mp.log(1 / alphaY_inv_173(f_req + h)) - mp.log(1 / alphaY_inv_173(f_req - h))) / (mp.log(f_req + h) - mp.log(f_req - h))
chk("S41 f_g needed for alpha_Y(173 GeV) to 1e-3: 0.18%", 0.0018, 1e-3 / el, 0.05, f"(f_req = {float(f_req):.6f}, elasticity {float(el):.4f})")
signs = {}
for name, b in (("U(1)_Y", F(41, 6)), ("SU(2)", F(-19, 6)), ("SU(3)", F(-7))):
    for fs in (1, -1):
        signs[(name, fs)] = (F(fs) / b) > 0                             # g*^2 = 16 pi^2 f/b must be positive
chk_bool("S41 universal f: U(1)_Y has an interacting fixed point only for f>0; SU(2), SU(3) only for f<0",
         signs[("U(1)_Y", 1)] and not signs[("U(1)_Y", -1)] and signs[("SU(2)", -1)] and not signs[("SU(2)", 1)] and signs[("SU(3)", -1)] and not signs[("SU(3)", 1)])

print("== lane C / M4: fermion-only emergence toy and the proper SM chain at the species cutoff")
ferm = [(0.51099895e-3, 1, 1), (0.1056584, 1, 1), (1.77686, 1, 1), (2.16e-3, 3, F(2, 3)), (4.67e-3, 3, F(-1, 3)), (0.0934, 3, F(-1, 3)),
        (1.27, 3, F(2, 3)), (4.18, 3, F(-1, 3)), (172.57, 3, F(2, 3))]
Mred = mp.mpf("2.435323e18")
Lam118 = Mred / mp.sqrt(118)
toy = 2 / (3 * mp.pi) * sum(nc * mp.mpf(q.numerator) ** 2 / q.denominator ** 2 * mp.log(Lam118 / mp.mpf(m)) if isinstance(q, F) else nc * q * q * mp.log(Lam118 / mp.mpf(m)) for m, nc, q in ferm)
chk("S19 fermion-only toy 1/alpha(0) ~ 70.4 (N = 118); 137.036/toy = 1.9 (1.91-1.95 across N)", 70.4444, toy, 1e-4, f"ratio {float(mp.mpf('137.035999177') / toy):.3f}")
Mred4 = mp.mpf("2.435e18")
L118 = Mred4 / mp.sqrt(118)
aem = mp.mpf("127.930")
aYc = aem * (1 - s2) - bY / (2 * mp.pi) * mp.log(L118 / mZ)
a2c = aem * s2 - b2 / (2 * mp.pi) * mp.log(L118 / mZ)
chk("S20 proper SM chain at M_red/sqrt(118): 1/alpha_em = 107.25", 107.25, aYc + a2c, 1e-3, f"(1/alpha_Y = {float(aYc):.2f}, 1/alpha_2 = {float(a2c):.2f}; only the U(1)_Y piece can 'emerge')")
def nx_root(selfcons):
    def resid(n):
        Lm = Mred4 / mp.sqrt(118 + 4 * n) if selfcons else L118
        return aem * (1 - s2) - bY / (2 * mp.pi) * mp.log(Lm / mZ) - (mp.mpf(4) / 3 * n) / (2 * mp.pi) * mp.log(Lm / 1000)
    return mp.findroot(resid, 8)
nx_f, nx_s = nx_root(False), nx_root(True)
chk("S20 extra unit-Y Dirac fermions at 1 TeV: 8.6", 8.6, nx_s, 0.01, f"(fixed-cutoff {float(nx_f):.3f})")
chk("S42 self-consistent cutoff shifts the requirement by 0.6%", 0.006, nx_s / nx_f - 1, 0.05)

print("== lane E: bounds")
YR = mp.mpf("365.25") * 86400
H0yr = H0s * YR
clock = mp.mpf("3.2e-18")
zmax = clock / (H0yr * mp.sqrt(3 * OL * (1 - mp.mpf("0.752"))))
chk("S23 zeta_max(w0 = -0.752) = 6.5e-8", 6.5e-8, zmax, 0.01)
chk("S23 1+w allowed at zeta = 6.5e-8: 0.25", 0.25, (clock / (H0yr * mp.mpf("6.5e-8"))) ** 2 / (3 * OL), 0.02)
p = mp.log(alpha) / mp.log(x)
chk("S23 AH5 power family: (1+w)_max ~ 1e-6 (8.8e-7)", 8.8e-7, clock / (3 * H0yr * abs(p)), 0.01)

print("== lane F: radion potential numbers")
cc = sp.symbols("c", positive=True)
R_, R0_, rho5 = sp.symbols("R R0 rho5", real=True)
VE = (R0_ / R_) ** 2 * (2 * sp.pi * R_ * rho5 - cc / R_ ** 4)
r5 = sp.solve(sp.diff(VE, R_).subs(R_, R0_), rho5)[0]
Vmin = sp.simplify(VE.subs(rho5, r5).subs(R_, R0_))
chk_bool("S24 extremum value V = 5c/R^4 and V'' = -30 c/R^6 (sign theorem: V>0 only at a maximum)",
         sp.simplify(Vmin - 5 * cc / R0_ ** 4) == 0 and sp.simplify(sp.diff(VE, R_, 2).subs(rho5, r5).subs(R_, R0_) + 30 * cc / R0_ ** 6) == 0)
c1 = 3 * mp.zeta(5) / (64 * mp.pi ** 6)
for DN in (5, 4):
    Rstar = (40 * mp.pi * DN * c1 / x) ** mp.mpf("0.25")
    decades = mp.log10(5 * DN * c1 / k ** 4 / (x / (8 * mp.pi)))
    print(f"  |DN| = {DN}: R*/l_P = {float(Rstar):.3e}; cancellation to reach R = 23.41 l_P: {float(decades):.2f} decades")
    chk(f"S24 R* ~ 1e30 l_P (|DN| = {DN}, within a factor 1.1)", 1e30, Rstar, 0.1)
    chk(f"S24 ~115 decades (|DN| = {DN})", 115, decades, 0.005)

print("== lane M: MacDowell-Mansouri coupling")
alpha_MM = mp.mpf(16) / 3 * x
chk("S43 (16/3) x = 1.5e-121", 1.5e-121, alpha_MM, 0.02)

print("== lane J: log needed for 137.036 at N_eff = 8")
Lreq = 3 * mp.pi * mp.mpf("137.035999177") / 8
chk("S29 Lambda/mu = 10^35 (10^35.06)", 35, mp.log10(mp.e ** (Lreq / 2)), 0.002)

print("== Lean AH3: the eps* window")
eps = mp.mpf("0.5") / mp.sqrt(4 * mp.pi / mp.mpf("137.036"))
chk_bool("S06 eps* in (1.64, 1.66), script value 1.6511", 1.64 < eps < 1.66 and abs(eps - 1.6511) < 1e-3, f"({float(eps):.4f})")

print("== lane K: closed forms and misses vs CODATA (independent formulas)")
T = mp.mpf("137.035999177")
gil = mp.pi / (29 * mp.cos(mp.pi / 137) * mp.tan(mp.pi / (29 * 137)))
chk("S48 Gilson miss 4.45e-9", 4.45e-9, abs(gil / T - 1), 0.01)
chk("S48 Gilson 27.8 sigma_CODATA", 27.8, abs(gil / T - 1) / mp.mpf("1.6e-10"), 0.01)
astar = mp.findroot(lambda a: mp.pi / (a * mp.cos(mp.pi / 137) * mp.tan(mp.pi / (a * 137))) - T, 29)
chk("S48 Gilson real parameter at b = 137 is 28.695", 28.695, astar, 1e-4)
wy = 1 / ((9 / (8 * mp.pi ** 4)) * (mp.pi ** 5 / (2 ** 4 * mp.factorial(5))) ** mp.mpf("0.25"))
chk("S48 Wyler miss 6.1e-7", 6.1e-7, abs(wy / T - 1), 0.02)
chk("S48 Wyler 3800 sigma", 3800, abs(wy / T - 1) / mp.mpf("1.6e-10"), 0.02)
chk("S48 Eddington 137 miss 2.6e-4", 2.6e-4, abs(137 / T - 1), 0.02)
chk("S48 Rosen N(N-1)/(4 pi), N = 42, miss 2.6e-5", 2.6e-5, abs(mp.mpf(42 * 41) / (4 * mp.pi) / T - 1), 0.03)
chk("S48 Sherbon 4 pi^3 + pi^2 + pi miss 2.2e-6", 2.2e-6, abs((4 * mp.pi ** 3 + mp.pi ** 2 + mp.pi) / T - 1), 0.03)
chk("S48 combinatorial hierarchy 137/(1 - 1/(30*127)) miss 2.3e-7", 2.3e-7, abs(137 / (1 - mp.mpf(1) / (30 * 127)) / T - 1), 0.03)
bl = 19596 / mp.mpf(143) + 5 * mp.log(2 + mp.sqrt(3)) / (6370 - 2 * mp.log(2 + mp.sqrt(3)))
chk("S48 Bleger closed form miss 3.3e-11 (formula as printed in lane K's table)", 3.3e-11, abs(bl / T - 1), 0.05)

print("\nFAILED:", FAILS if FAILS else "none")
sys.exit(1 if FAILS else 0)
