#!/usr/bin/env python3
"""u2_1 -- U2 winding-charge model of the capped horizon condensate: derivation of alpha_c, the f(x) it implies, the declared 45-member family, inversions.
Pre-registered in U2_PREREGISTRATION.md (written before this ran).

Run:      PYTHONDONTWRITEBYTECODE=1 python3 u2_1_cap_condensate_alpha.py            (exit 0 iff every check, including the pre-registered expectations, passes)
Control:  PYTHONDONTWRITEBYTECODE=1 python3 u2_1_cap_condensate_alpha.py --mutate   (drops the factor 2 in F^2 = 2 P_cap xi^2; the A1 identity must FAIL; exit 1)
"""
import sys
sys.dont_write_bytecode = True
import mpmath as mp
import sympy as sp

MUT = "--mutate" in sys.argv
mp.mp.dps = 50
CH = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# ---- constants (SI, CODATA 2022 where relevant); programme inputs as in AH5
c = mp.mpf(299792458)
hbar = mp.mpf("1.054571817e-34")
G = mp.mpf("6.67430e-11")
eV = mp.mpf("1.602176634e-19")
Mpc = mp.mpf("3.0856775814913673e22")
H0 = mp.mpf("67.4e3") / Mpc
OmL = mp.mpf("0.6847")
kappa = mp.mpf(1) / 2
T = mp.mpf("137.035999177")          # 1/alpha target
alpha_t = 1 / T
Zc = 2 * mp.sqrt(8 * mp.pi / 3)      # the record's Z = 5.7888


def Lam_of(Om):
    return 3 * Om * H0 ** 2 / c ** 2


def lP2():
    return hbar * G / c ** 3


def Pcap(Lam, kap=kappa):
    return kap ** 2 * Lam * c ** 4 / (64 * mp.pi ** 2 * G)


def alpha_c(xi, Lam, w, kap=kappa):
    """alpha_c = w F^2 xi^2 / (hbar c) with F^2 = 2 P_cap xi^2 (P2); the mutated control drops the 2."""
    F2 = (1 if MUT else 2) * Pcap(Lam, kap) * xi ** 2
    return w * F2 * xi ** 2 / (hbar * c)


Lam = Lam_of(OmL)
lP = mp.sqrt(lP2())
x = Lam * lP2()
print("U2 / u2_1: cap-stiffness winding-charge model; alpha_c = w F^2 xi^2/(hbar c), F^2 = 2 P_cap xi^2")
print(f"inputs: Lambda = {mp.nstr(Lam, 8)} m^-2, l_P = {mp.nstr(lP, 8)} m, x = Lambda l_P^2 = {mp.nstr(x, 8)}, ln(1/x) = {mp.nstr(mp.log(1 / x), 8)}")
chk("A0 x reproduces AH5's 2.8485e-122 to 1e-3", abs(x / mp.mpf("2.8485e-122") - 1) < 1e-3)

# ---------------------------------------------------------------- A1 sympy identity
kap_s, Lam_s, G_s, c_s, hb_s, xi_s, w_s, s_s = sp.symbols("kappa Lambda G c hbar xi w s", positive=True)
P_s = kap_s ** 2 * Lam_s * c_s ** 4 / (64 * sp.pi ** 2 * G_s)
F2_s = (1 if MUT else 2) * P_s * xi_s ** 2
alpha_s = w_s * F2_s * xi_s ** 2 / (hb_s * c_s)
x_s = Lam_s * hb_s * G_s / c_s ** 3
lP_s = sp.sqrt(hb_s * G_s / c_s ** 3)
rhs = w_s * kap_s ** 2 / (32 * sp.pi ** 2) * x_s * (xi_s / lP_s) ** 4
chk("A1 alpha_c = w F^2 xi^2/(hbar c) = (w kappa^2/32 pi^2) x (xi/l_P)^4 (exact, sympy)", sp.simplify(alpha_s - rhs) == 0)

# ---------------------------------------------------------------- A2 principle Q
xi_q = (s_s * hb_s * c_s / P_s) ** sp.Rational(1, 4)
alpha_q = sp.simplify(w_s * 2 * P_s * xi_q ** 4 / (hb_s * c_s))
chk("A2a under P3 (P_cap xi^4 = s hbar c): alpha_c = 2 w s exactly", sp.simplify(alpha_q - 2 * w_s * s_s) == 0, f"(alpha_c = {alpha_q})")
chk("A2b alpha_c independent of kappa, Lambda, G, c, hbar (derivatives vanish)",
    all(sp.simplify(sp.diff(alpha_q, v)) == 0 for v in (kap_s, Lam_s, G_s, c_s, hb_s)))

# ---------------------------------------------------------------- A3 footings
LamA, LamB = Lam_of(OmL), Lam_of(mp.mpf(1))
PA, PB = Pcap(LamA), Pcap(LamB)
a0A, a0B = mp.sqrt(8 * mp.pi * G * PA), mp.sqrt(8 * mp.pi * G * PB)
a0B_ref = c * H0 / Zc
print(f"\nA3 footings: P_cap(rho_Lambda) = {mp.nstr(PA, 6)} J/m^3, P_cap(rho_crit) = {mp.nstr(PB, 6)} J/m^3;  a0 = {mp.nstr(a0A, 5)} and {mp.nstr(a0B, 5)} m/s^2 (c H0/Z = {mp.nstr(a0B_ref, 5)})")
chk("A3a a0 = sqrt(8 pi G P_cap) = 9.36e-11 (rho_Lambda footing) within 0.5%", abs(a0A / mp.mpf("9.36e-11") - 1) < 5e-3)
chk("A3b a0 = 1.13e-10 (rho_crit footing, = c H0/Z) within 0.5%", abs(a0B / mp.mpf("1.13e-10") - 1) < 5e-3 and abs(a0B / a0B_ref - 1) < 1e-9)
xiA = (hbar * c / PA) ** mp.mpf("0.25")
xiB = (hbar * c / PB) ** mp.mpf("0.25")
chk("A3c alpha_c(xi_cap, w = pi) is identical on both footings to 1e-12 (P_cap and xi_cap differ)",
    abs(alpha_c(xiA, LamA, mp.pi) / alpha_c(xiB, LamB, mp.pi) - 1) < 1e-12 and abs(xiA / xiB - 1) > 0.05,
    f"(alpha_c = {mp.nstr(alpha_c(xiA, LamA, mp.pi), 12)} vs {mp.nstr(alpha_c(xiB, LamB, mp.pi), 12)}; xi_cap = {mp.nstr(xiA, 5)} m vs {mp.nstr(xiB, 5)} m)")

# ---------------------------------------------------------------- A4 x-exponent table
def xi_of(kind, Lm):
    R1 = mp.sqrt(3 / Lm)
    return {"l_P": lP, "xi_cap": (hbar * c / Pcap(Lm)) ** mp.mpf("0.25"), "sqrt(l_P r_H)": mp.sqrt(lP * R1), "r_H": R1}[kind]


print("\nA4 exponent of alpha_c in x (Lambda -> 2 Lambda at fixed l_P), w = pi:")
exp_expected = {"l_P": 1, "xi_cap": 0, "sqrt(l_P r_H)": 0, "r_H": -1}
okA4 = True
for kind, ex in exp_expected.items():
    a1 = alpha_c(xi_of(kind, Lam), Lam, mp.pi)
    a2 = alpha_c(xi_of(kind, 2 * Lam), 2 * Lam, mp.pi)
    p = mp.log(a2 / a1) / mp.log(2)
    okA4 &= abs(p - ex) < 1e-9
    print(f"    xi = {kind:14s} xi/l_P = {mp.nstr(xi_of(kind, Lam) / lP, 5):>12s}   alpha_c = {mp.nstr(a1, 6):>12s}   1/alpha_c = {mp.nstr(1 / a1, 6):>12s}   exponent in x = {mp.nstr(p, 8)}")
chk("A4 exponents are 1, 0, 0, -1 (only xi_cap and the geometric mean avoid 1e+-122)", okA4)

# ---------------------------------------------------------------- A5 the declared 45-member family
S_LIST = [1 / (4 * mp.pi), 1 / (2 * mp.pi), mp.mpf(1) / 4, mp.mpf(1) / 2, 3 / (4 * mp.pi), mp.mpf(1), mp.mpf(2), 4 * mp.pi / 3, 2 * mp.pi, 4 * mp.pi]
S_NAMES = ["1/4pi", "1/2pi", "1/4", "1/2", "3/4pi", "1", "2", "4pi/3", "2pi", "4pi"]
W_LIST = [mp.pi, 2 * mp.pi, mp.mpf(1)]
W_NAMES = ["pi", "2pi", "1"]
R_LIST = [mp.sqrt(3 / Lam), 1 / mp.sqrt(Lam)]
R_NAMES = ["sqrt(3/L)", "1/sqrt(L)"]
lengths = [("l_P", lP)]
lengths += [(f"r_H[{n}]", R) for n, R in zip(R_NAMES, R_LIST)]
lengths += [(f"sqrt(l_P r_H)[{n}]", mp.sqrt(lP * R)) for n, R in zip(R_NAMES, R_LIST)]
P0 = Pcap(Lam)
lengths += [(f"xi_cap[s={n}]", (s * hbar * c / P0) ** mp.mpf("0.25")) for n, s in zip(S_NAMES, S_LIST)]
fam = []
for ln_, xi in lengths:
    for wn, w in zip(W_NAMES, W_LIST):
        a = alpha_c(xi, Lam, w)
        fam.append((ln_, wn, a, abs((1 / a) / T - 1)))
print(f"\nA5 family: {len(lengths)} lengths x {len(W_LIST)} w = {len(fam)} members; target 1/alpha = 137.035999177")
fam_sorted = sorted(fam, key=lambda r: r[3])
for r in fam_sorted[:6]:
    print(f"    {r[0]:26s} w={r[1]:4s}  alpha_c = {mp.nstr(r[2], 8):>14s}  1/alpha_c = {mp.nstr(1 / r[2], 8):>14s}  miss = {mp.nstr(r[3], 4)}")
hits = [r for r in fam if r[3] < 1e-3]
chk("A5a family has 45 members", len(fam) == 45)
chk("A5b no member is within 1e-3 of the target (pre-registered expectation 0 hits)", len(hits) == 0, f"(hits = {len(hits)})")
best = fam_sorted[0]
chk("A5c the closest member is the post-observation geometric mean sqrt(l_P r_H), R = sqrt(3/Lambda), w = pi, miss 2.2%",
    best[0] == "sqrt(l_P r_H)[sqrt(3/L)]" and best[1] == "pi" and abs(best[3] - 0.0219) < 5e-4, f"(miss = {mp.nstr(best[3], 5)})")
capfam = [r for r in fam if r[0].startswith("xi_cap")]
amin = min(r[2] for r in capfam)
chk("A5d every xi_cap member has alpha_c >= 0.159 (1/alpha <= 6.3): the Q sub-family is O(1)", amin >= mp.mpf("0.1591"), f"(min alpha_c = {mp.nstr(amin, 6)}, 1/alpha max = {mp.nstr(1 / amin, 6)})")
prim = [r for r in fam if r[0] == "xi_cap[s=1]" and r[1] == "pi"][0]
chk("A5e the primary member is alpha_c = 2 pi", abs(prim[2] / (2 * mp.pi) - 1) < 1e-30, f"(alpha_c = {mp.nstr(prim[2], 15)}, 1/alpha_c = {mp.nstr(1 / prim[2], 8)}; it exceeds the target alpha by {mp.nstr(prim[2] / alpha_t, 6)}x)")
amax_nonQ = [r for r in fam if not r[0].startswith("xi_cap") and r[0] not in ("l_P",)]
spread = max(r[2] for r in fam) / min(r[2] for r in fam)
print(f"    family spread max/min alpha_c = {mp.nstr(spread, 4)} (dominated by the l_P and r_H members at 1e-123 and 1e+121)")

# ---------------------------------------------------------------- A6 inversions (re-labellings, not scored)
print("\nA6 inversions (each trades alpha for one number; NOT evidence):")
xi_cap1 = (hbar * c / P0) ** mp.mpf("0.25")
ratio = (alpha_t / (2 * mp.pi)) ** mp.mpf("0.25")
xi_star = ratio * xi_cap1
s_star = alpha_t / (2 * mp.pi)
m_star_eV = hbar * c / xi_star / eV
kap_star = mp.sqrt(32 * mp.pi * alpha_t / 3)
print(f"    (w = pi) xi* = {mp.nstr(ratio, 6)} xi_cap = {mp.nstr(xi_star, 6)} m;  s* = {mp.nstr(s_star, 6)};  m* = hbar/(xi* c) = {mp.nstr(m_star_eV, 5)} eV (FL1 window 2e-19 .. 3 eV)")
print(f"    geometric-mean member (R = sqrt(3/Lambda), w = pi) would need kappa* = {mp.nstr(kap_star, 6)} instead of 1/2 (a {mp.nstr((kap_star / kappa - 1) * 100, 4)}% change)")
print(f"    fourth-power sensitivity: d alpha/alpha = 4 d xi/xi, so a {mp.nstr((1 / ratio - 1) * 100, 4)}% larger xi_cap than xi* moves alpha by the whole factor {mp.nstr(2 * mp.pi / alpha_t, 5)}")
chk("A6a xi* = 0.19 xi_cap (a factor 5.4 below the quantum-limited core), s* = 1.2e-3: no natural convention", abs(ratio - mp.mpf("0.1846")) < 2e-3 and abs(s_star - mp.mpf("1.161e-3")) < 2e-5)
chk("A6b m* inside FL1's allowed window (so the re-labelled model is not excluded by FL1's own window; it is still a re-labelling)", 2e-19 <= m_star_eV <= 3.0, f"(m* = {mp.nstr(m_star_eV, 5)} eV)")
chk("A6c required kappa for the geometric-mean member is 0.4945 (1.1% below the fitted 1/2)", abs(kap_star - mp.mpf("0.4945")) < 5e-4)

# ---------------------------------------------------------------- A7 record link
gm_R1 = [r for r in fam if r[0] == "sqrt(l_P r_H)[sqrt(3/L)]" and r[1] == "pi"][0]
four_Z2 = 4 * Zc ** 2
chk("A7a at kappa = 1/2 the geometric-mean member is 1/alpha = 32 pi/(3 kappa^2) = 128 pi/3 = 4 Z^2 exactly", abs(1 / gm_R1[2] / four_Z2 - 1) < 1e-12 and abs(four_Z2 - 128 * mp.pi / 3) < 1e-12,
    f"(1/alpha = {mp.nstr(1 / gm_R1[2], 12)}, 4Z^2 = {mp.nstr(four_Z2, 12)})")
resid = T - four_Z2
print(f"    residual to the target: {mp.nstr(resid, 8)} (the '+3' of the old formula 1/alpha = 4Z^2 + 3, scored as chance by lane D). This model does NOT produce it.")
chk("A7b the residual is 2.9947 (pre-registered as 2.996 from rounded numbers; tolerance 2e-3 unchanged), i.e. 4Z^2+3 misses by 3.9e-5", abs(resid - mp.mpf("2.996")) < 2e-3 and abs((four_Z2 + 3) / T - 1 - 3.9e-5) < 5e-6)

n_fail = CH.count(False)
print(f"\nchecks: {len(CH) - n_fail}/{len(CH)} pass")
print("\nVERDICT (against the pre-registered criteria):")
print("  f(x) implied: alpha_c = C x^(1-4p); only p = 1/4 (xi_cap and the geometric mean) is not 1e+-122, and then f is a CONSTANT (2 w s, or 3 w kappa^2/(32 pi^2) for the geometric mean): no x dependence, no logarithm, not forced.")
print("  Primary member (Q, s=1, w=pi): alpha_c = 2 pi. It misses the target by 860x. No member within 1e-3. The nearest (geometric mean, 1/134.04 = 4 Z^2) is post-observation and 2.2% off; it needs a +2.995 in 1/alpha the model does not supply.")
print("  Zero NEW free constants in the primary model; the freedom is in the pure-number conventions (s, w, R, which length), all counted (45). Re-labelled with xi free, alpha is a 4th-power function of xi.")
if MUT:
    print("\nMUTATE CONTROL: F^2 = P_cap xi^2 (factor 2 dropped); A1 must FAIL.")
    ok = not CH[1]      # CH[0] = A0, CH[1] = A1
    print("  " + ("FAILED as required -- the control works (exit 1)" if ok else "DID NOT FAIL -- the control is broken"))
    sys.exit(1 if ok else 0)
sys.exit(0 if n_fail == 0 else 1)
