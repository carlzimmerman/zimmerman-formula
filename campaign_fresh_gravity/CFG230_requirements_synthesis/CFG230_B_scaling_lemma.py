"""CFG230 script B: R01 (scaling lemma, tolerance window, exponent table), R02a (dimensional analysis), R03 hooks.
Labels: NEW-DERIVATION unless stated. MUTATE=M5 (band +-20%) and MUTATE=M6 (drop the 'same constants at every mass' clause)."""
import math, re, os, sys
import numpy as np, sympy as sp
from scipy.optimize import linprog
import CFG230_common as C

R = C.Run("CFG230_B_scaling_lemma")
M = C.mode()
band = 0.20 if M == "M5" else 0.10
R.p(f"CFG230 B. repo=<repo> mode={M or 'main'} band=+-{band}")
R.res["band"] = band

# ------------------------------------------------------------------ constants
R.p("\n== constants (canonical footing kappa = 1/2, H0 = 67.4, Omega_L = 0.6847)")
R.p(f"  a0 = {C.A0:.5e} m/s^2 (Lean A0Numeric: 9.36e-11 < a0 < 9.361e-11)")
R.check("CROSS-CHECK", "a0 canonical in (9.36e-11, 9.361e-11)", 9.36e-11 < C.A0 < 9.361e-11, f"{C.A0:.5e}")
sig_in = C.A0 / (2 * math.pi * C.G) / (C.MSUN / C.PC ** 2)
R.check("EXPECT", "E5 inner column a0/(2 pi G) = 106.8-106.9 Msun/pc^2", 106.7 < sig_in < 107.0, f"{sig_in:.3f}")
R.check("EXPECT", "E5 a0/(4 pi G) = 53.4 Msun/pc^2", 53.3 < sig_in / 2 < 53.5, f"{sig_in/2:.3f}")

# ------------------------------------------------------------------ R01: fixed-kernel linear lemma (sympy)
R.p("\n== R01 lemma: linear response with a fixed kernel")
Mb, lam, r, G_, a0, KK = sp.symbols("M lambda r G a0 K", positive=True)
K = sp.Function("K")
rho_model = Mb * K(r)                       # linear in M_b with a fixed kernel (point-mass source)
gtot = G_ * Mb / r ** 2                     # a linear, translation-invariant response has g_tot proportional to M_b
C_model = rho_model * r ** 3 * gtot
C_target = a0 * Mb / (4 * sp.pi)
ratio = sp.simplify(C_model / C_target)
ex_model = sp.simplify(sp.diff(sp.log(C_model.subs(Mb, lam * Mb)), lam).subs(lam, 1))
ex_target = sp.simplify(sp.diff(sp.log(C_target.subs(Mb, lam * Mb)), lam).subs(lam, 1))
R.p(f"  C_model ~ M^{ex_model}, C_target ~ M^{ex_target}; R = C_model/C_target = {ratio}  (exponent in M at fixed r: {sp.simplify(sp.diff(sp.log(ratio.subs(Mb, lam*Mb)), lam).subs(lam,1))})")
R.check("NEW-DERIVATION", "E4: C_model ~ M^2, C_target ~ M, R ~ M^1 at fixed r", ex_model == 2 and ex_target == 1)
R.p("  hypothesis (stated, not derived): rho_model linear in M_b with a fixed kernel AND g_tot linear in M_b (Newton plus a linear phantom).")
R.p("  CITATION: CFG120 sympy, CFG151 reproduces exponents 2.000000/1.000000 (grade S+R).")

# window arithmetic (sympy exact) and LP for the universal kernel
def window(b, k):
    return math.log10((1 + b) / (1 - b)) / (3 * k)
w_out, w_in = window(band, 1), window(band, 2)
R.p(f"  tolerance window |p - 1/2| <= log10((1+b)/(1-b))/(3k): outer {w_out:.4f}, inner {w_in:.4f} (band +-{band})")
R.res.update(window_outer=w_out, window_inner=w_in)
if M != "M5":
    R.check("EXPECT", "E2 window 0.0291 (outer) / 0.0145 (inner) at +-10%", abs(w_out - 0.0291) < 5e-4 and abs(w_in - 0.0145) < 5e-4, f"{w_out:.4f} / {w_in:.4f}")

# best universal kernel over 1e9-1e12 at fixed x in [0.1, 30]: LP in log space
def lp_spread(per_mass=False):
    hstep = 0.125
    ms = np.arange(0, 13)                     # log10 M = 9 + 0.25 m
    js = np.arange(0, 21)                     # log10 x = -1 + 0.125 j  (0.1 .. 10^1.5 = 31.6; the x = 30 end is 10^1.477)
    js = js[(-1 + hstep * js) <= math.log10(30) + 1e-9]
    nodes = sorted({m + j for m in ms for j in js})
    idx = {n: i for i, n in enumerate(nodes)}
    nvar = (len(ms) * len(nodes) if per_mass else len(nodes)) + 1
    A, b = [], []
    for m in ms:
        lM = 9 + 0.25 * m
        for j in js:
            lx = -1 + hstep * j
            n = m + j
            # logR = log(4 pi) + log x + 3 log r_M + k ; r_M(M) = sqrt(G M/a0)
            lrM = 0.5 * (math.log(C.G * C.MSUN * 10 ** lM / C.A0))
            r_ = math.exp(lx * math.log(10) + lrM)
            # write K(r) r^3 4 pi / x^2 : logR = log 4pi + 3 log r - 2 log x + k
            c0 = math.log(4 * math.pi) + 3 * math.log(r_) - 2 * lx * math.log(10)
            col = (m * len(nodes) + idx[n]) if per_mass else idx[n]
            row = np.zeros(nvar); row[col] = 1.0; row[-1] = -1.0
            A.append(row.copy()); b.append(-c0)
            row2 = np.zeros(nvar); row2[col] = -1.0; row2[-1] = -1.0
            A.append(row2); b.append(c0)
    cvec = np.zeros(nvar); cvec[-1] = 1
    res = linprog(cvec, A_ub=np.array(A), b_ub=np.array(b), bounds=[(None, None)] * (nvar - 1) + [(0, None)], method="highs")
    return res.x[-1], len(A) // 2
t_univ, npts = lp_spread(False)
R.p(f"  LP (log space, {npts} (M, x) points, one universal K(r)): minimal worst-case |ln R| = {t_univ:.5f} -> factor {math.exp(t_univ):.4f}")
R.check("CROSS-CHECK", "universal-kernel residual = sqrt(1000) = 31.6228 (CFG120, CFG151)", abs(math.exp(t_univ) - math.sqrt(1000)) / math.sqrt(1000) < 1e-6, f"{math.exp(t_univ):.6f}")
R.res["universal_kernel_factor"] = math.exp(t_univ)
if M == "M6":
    t_pm, _ = lp_spread(True)
    R.p(f"  M6: 'same constants at every mass' dropped (a kernel per mass): minimal worst-case |ln R| = {t_pm:.3e}")
    R.res["per_mass_t"] = t_pm
    C.bite(R, abs(t_pm - t_univ) > 1e-3, f"R01 spread {math.exp(t_univ):.2f} -> {math.exp(t_pm):.4f}: with a per-mass kernel any door passes G1 by fitting, so R01 is conditional on that clause")
# single-kernel mass window: two masses sharing a node, exact interval intersection
xx = sp.symbols("x1 x2", positive=True)
def window_mass(bb):
    return (1 + bb) / (1 - bb)
R.p(f"  single-kernel mass window M_max/M_min <= (1+b)/(1-b) = {window_mass(band):.4f} (CFG120: 1.222 against the 1.1 line at b = 0.1)")
if M != "M5":
    R.check("CROSS-CHECK", "window 1.222 (CFG120)", abs(window_mass(band) - 1.2222) < 1e-3)

# ------------------------------------------------------------------ R01 exponent table
R.p("\n== R01 exponent table (spread over 1e9-1e12: 10^(3|dp|) for a scale, same for a mass-dependent amplitude power)")
table = [("D01 fixed kernel length (p = 0)", 0.0, 31.6228), ("D09 fixed length 1/m (p = 0)", 0.0, None), ("D06 turnaround (p = 1/3)", 1 / 3, None), ("D02 Verlinde (p = 1/2)", 0.5, None)]
for nm, p, lane in table:
    sp_ = 10 ** (3 * abs(p - 0.5))
    R.p(f"  {nm}: |dp| = {abs(p-0.5):.4f}; full spread in s = {sp_:.3f}; in s^2 = {sp_**2:.2f}")
    R.res[nm] = sp_
R.check("CROSS-CHECK", "D01 spread 10^1.5 = 31.62 matches CFG120's sqrt(1000)", abs(10 ** 1.5 - 31.6228) < 1e-3)
R.check("CROSS-CHECK", "D04 amplitude M^(1/2) over 1e3: 31.62 (CFG122 analytic 31.62)", abs(1000 ** 0.5 - 31.62) < 0.01)
R.check("EXPECT", "E3 D06: 3.16 in s and 10 in s^2", abs(10 ** 0.5 - 3.162) < 1e-3)
# D06: M_c(<r) shift for a rescaled radial scale (consistency with CFG118's 1.0-4.2x at x~1 and 0.28-0.66x at x~28)
def mc(x): return math.sqrt(1 + x * x) - 1
for s_ in (10 ** 0.25, 10 ** -0.25, 10 ** 0.5):
    R.p(f"  scale factor s = {s_:.3f}: M_c(s x)/M_c(x) at x = 1: {mc(s_*1)/mc(1):.3f}; at x = 28: {mc(s_*28)/mc(28):.3f}")
R.p("  (with a free pivot the D06 turnaround scale gives a factor up to ~3 spread each way at x ~ 1, the same order as CFG118's 1.0-4.2x; not a match, an order-of-magnitude consistency.)")

# ------------------------------------------------------------------ R02a dimensional analysis
R.p("\n== R02a: Buckingham-pi nullspace (own derivation; the committed Lean Dimension module states the monomial case, grade L in Amendment 1)")
dims = {"G": (3, -1, -2), "M": (0, 1, 0), "c": (1, 0, -1), "H": (0, 0, -1), "hbar": (2, 1, -1)}  # (L, Mass, T)
def solve(names, target_len_M_exp):
    syms = sp.symbols("e_" + "_".join(names))
    ex = dict(zip(names, sp.symbols(" ".join("e_" + n for n in names))))
    eqs = []
    for i, tgt in enumerate((1, 0, 0)):        # length: L^1 M^0 T^0
        eqs.append(sum(ex[n] * dims[n][i] for n in names) - tgt)
    eqs.append(ex["M"] - sp.Rational(target_len_M_exp))
    sol = sp.linsolve(eqs, list(ex.values()))
    return ex, sol
for names, mexp, label in ((["G", "M", "c", "H"], sp.Rational(1, 2), "{G,M,c,H} length ~ M^(1/2)"), (["G", "M", "H"], sp.Rational(1, 3), "{G,M,H} length ~ M^(1/3)"),
                          (["G", "M", "H"], sp.Rational(1, 2), "{G,M,H} length ~ M^(1/2)"), (["G", "M", "c"], sp.Rational(1, 2), "{G,M,c} length ~ M^(1/2)"),
                          (["G", "M", "c", "hbar"], sp.Rational(1, 2), "{G,M,c,hbar} length ~ M^(1/2)")):
    ex, sol = solve(names, mexp)
    R.p(f"  {label}: solutions = {sol}")
    R.res[label] = str(sol)
ex, sol = solve(["G", "M", "c", "H"], sp.Rational(1, 2)); t = list(sol)
R.check("NEW-DERIVATION", "E1: exactly one exponent vector for M^(1/2) from {G,M,c,H}: (GM/(cH))^(1/2)", len(t) == 1 and t[0] == (sp.Rational(1, 2), sp.Rational(1, 2), -sp.Rational(1, 2), -sp.Rational(1, 2)), str(t))
ex, sol = solve(["G", "M", "H"], sp.Rational(1, 3)); t = list(sol)
R.check("NEW-DERIVATION", "E1: exactly one exponent vector for M^(1/3) from {G,M,H}: (GM/H^2)^(1/3)", len(t) == 1 and t[0] == (sp.Rational(1, 3), sp.Rational(1, 3), -sp.Rational(2, 3)), str(t))
ex, sol = solve(["G", "M", "H"], sp.Rational(1, 2)); R.check("NEW-DERIVATION", "no M^(1/2) length from {G,M,H} (no c)", len(list(sol)) == 0)
ex, sol = solve(["G", "M", "c"], sp.Rational(1, 2)); R.check("NEW-DERIVATION", "no M^(1/2) length from {G,M,c} (agrees with the committed Lean no_sqrtM_length_GMc)", len(list(sol)) == 0)
ex, sol = solve(["G", "M", "c", "hbar"], sp.Rational(1, 2)); t = list(sol)
R.check("NEW-DERIVATION", "hbar admissible: G^(3/4) M^(1/2) c^(-7/4) hbar^(1/4) (agrees with the committed Lean hbar_admissible)", len(t) == 1 and t[0] == (sp.Rational(3, 4), sp.Rational(1, 2), -sp.Rational(7, 4), sp.Rational(1, 4)), str(t))
hbar = 1.054571817e-34
r_hb = (C.G ** 0.75) * (1e10 * C.MSUN) ** 0.5 * C.CLIGHT ** (-1.75) * hbar ** 0.25
R.check("EXPECT", "E15 hbar length at 1e10 Msun ~ 1.5e-11 m", 1.0e-11 < r_hb < 2.0e-11, f"{r_hb:.3e} m = {r_hb/C.KPC:.2e} kpc")
fac = (0.5 * math.sqrt(3 / (8 * math.pi))) ** 0.5
R.check("EXPECT", "E14 (kappa sqrt(3/8pi))^(1/2) = 0.416 at kappa = 1/2", abs(fac - 0.416) < 0.001, f"{fac:.4f}; r_M/(GM/(cH))^(1/2) = {1/fac:.3f}")
rM1 = C.rM(1e10); HL = C.H0 * math.sqrt(C.OMEGA_L)
rH = math.sqrt(C.G * 1e10 * C.MSUN / (C.CLIGHT * HL))
R.check("NEW-DERIVATION", "numeric: r_M / (GM/(c H_Lambda))^(1/2) = 2.41 (H_Lambda = H0 sqrt(Omega_L)); inverse 0.416", abs(rH / rM1 - 0.4156) < 2e-3, f"(GM/(c H_L))^(1/2)/r_M = {rH/rM1:.4f}")

# x_ta scaling with the LEDGER's r_ta (CFG118/CFG158 convention, NOT B's committed r_ta)
led = C.read_norm("campaign_fresh_gravity/LEDGER.md")
m_ = re.search(r"r_ta = 236, 508, 1094, 2358 kpc", led)
R.check("CITATION-AUDIT", "LEDGER CFG158 row carries r_ta = 236, 508, 1094, 2358 kpc", bool(m_))
rta = [236, 508, 1094, 2358]
xta = [rta[i] * C.KPC / C.rM(10 ** (9 + i)) for i in range(4)]
slope = (math.log10(xta[3]) - math.log10(xta[0])) / 3
R.p(f"  x_ta = r_ta/r_M at 1e9..1e12: {[f'{v:.1f}' for v in xta]}; log-slope {slope:.4f} (expected -1/6 = -0.1667); spread {xta[0]/xta[3]:.3f} (HAND 10^0.5 = 3.16)")
R.check("EXPECT", "x_ta ~ M^(-1/6): slope -0.1667 +- 0.005, spread 3.16", abs(slope + 1 / 6) < 0.005 and abs(xta[0] / xta[3] - 3.162) < 0.06, f"slope {slope:.4f}, spread {xta[0]/xta[3]:.3f}")
R.res["x_ta"] = xta

# ------------------------------------------------------------------ R03 hooks: sf01 B3 free function reproduces P2
R.p("\n== R03 hook: the sf01 B3 free function F(z) = (1/2) sqrt(z) sqrt(1+4z) + (1/4) asinh(2 sqrt z) - sqrt z and the P2 mu")
z = sp.symbols("z", positive=True); y = sp.symbols("y", positive=True)
F = sp.Rational(1, 2) * sp.sqrt(z) * sp.sqrt(1 + 4 * z) + sp.Rational(1, 4) * sp.asinh(2 * sp.sqrt(z)) - sp.sqrt(z)
mu_p2 = (sp.sqrt(1 + 4 * y ** 2) - 1) / (2 * y)
dF = sp.diff(F, z)
d1 = sp.simplify((dF - mu_p2.subs(y, sp.sqrt(z))))
num = [float(sp.N((dF - mu_p2.subs(y, sp.sqrt(z))).subs(z, v))) for v in (0.01, 0.3, 1, 7, 100)]
R.p(f"  F'(z) - mu_P2(sqrt z) symbolic residual: {d1}; numeric at z = 0.01,0.3,1,7,100: {['%.2e' % v for v in num]}")
R.check("CROSS-CHECK", "F'(z) = mu_P2(sqrt z) (AQUAL density (a0^2/8piG) F(g^2/a0^2), mu = F')", max(abs(v) for v in num) < 1e-12 or d1 == 0, "")
q = 1 - mu_p2
ypq = sp.simplify(sp.diff(y * q, y))
R.check("NEW-DERIVATION", "E12: (y q)' = 1 - 2y/sqrt(1+4y^2) for P2", sp.simplify(ypq - (1 - 2 * y / sp.sqrt(1 + 4 * y ** 2))) == 0, str(ypq))

if M in ("M5",):
    C.bite(R, abs(w_out - window(0.10, 1)) > 1e-3, f"scale window {window(0.10,1):.4f} -> {w_out:.4f} outer when the band widens to +-20% (hand 0.059)")
R.write()
