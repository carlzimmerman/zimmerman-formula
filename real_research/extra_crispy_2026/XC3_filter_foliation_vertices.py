#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XC3 -- THE FILTER'S OWN FOLIATION VERTICES, the piece XC1 left out.  The lead track's audit of XC1
(real_research/closure_resume_2026_09_26/, 09-26) scoped XC1's G8 result as a decoupling-limit pass that omits the
filter/foliation interaction: the MOND term 2 alpha_M^2 q(h^{mu nu} D_mu W D_nu W/alpha_M^2) with W = S[h] U,
S[h] = exp(b Delta_h), depends on the khronon's leaves twice -- through the leaf metric h in the argument and through the
leaf Laplacian Delta_h inside the heat kernel.  This lane derives both dependences and bounds every vertex they produce,
on a static background W_0 (the Solar System, a galaxy, a cluster), in the decoupling limit.

WHAT IS CHECKED (each check can fail)
  C1 [sympy, jets] for a STATIC field F the leaf Laplacian Delta_h F = h^{mu nu} d_mu d_nu F + K n^mu d_mu F under the
     tilt tau = t + pi has NO O(pi) term, and its O(pi^2) term is d_i pi d_j pi d_i d_j F + Lap pi (grad pi . grad F):
     every foliation correction to the filter carries the background's gradient or curvature.
  C2 [sympy, jets] the argument X_h = h^{mu nu} d_mu W_0 d_nu W_0 of a static W_0 is |grad W_0|^2 + (grad pi . grad W_0)^2
     - 2 pi_t (grad pi . grad W_0)^2 + O(pi^4): the leaf-metric dependence also starts at O(pi^2), with two powers of the
     background field.
  C3 [the heat-kernel derivative] dS = b Int_0^1 e^{(1-v) b Delta} dDelta e^{v b Delta} dv, verified against finite
     differences on a periodic grid with a non-commuting perturbation (absolute residual second order), with
     ||dS f|| <= b max_v ||dDelta e^{v b Delta} f||;
     at momentum K the factor is (1 - e^{-b K^2})/K^2 <= min(b, 1/K^2).
  C4 [the quadratic terms] the induced quadratic action is M_P^2 C_T [(grad pi . grad W_0)^2 + 2 grad W_0 . grad dW_2]:
     relative to the khronon's own gradient term (M_P^2/2) c_2 k^4 it is <= 6 C_T g^2/(c_2 k^2) (g = |grad W_0|), for the
     Sun (filtered field of the Galaxy, y = 2.3), a galaxy (y = 1, 0.1), a cluster core (y = 20), over k from 1/L_bg up.
  C5 [the sign, and why it is harmless] the (grad pi . grad W_0)^2 term enters the Lagrangian with a positive sign, i.e.
     it LOWERS the gradient energy: a band k < g sqrt(2 C_T/c_2) is formally unstable.  That band lies below the inverse
     coherence length of the background by the factor (Phi/c^2) sqrt(2 C_T/c_2) -- where a local (WKB) mode analysis does
     not apply -- for every background from the Solar System to clusters.
  C6 [the cubic and quartic vertices] every cubic vertex carries >= 2 background powers (the leading one is
     -2 M_P^2 C_T pi_t (grad pi . grad W_0)^2): a RELEVANT operator whose coupling C_T g^2 makes it strong only below
     Lambda_IR = C_T g^2/(M_P alpha^{3/2} c_s^{3/2}) -- computed over the window, UV and IR.

  MUTATE=1 gives the background a time dependence (d_t W_0 != 0): C1's "no O(pi) term" must FAIL -- the O(pi) terms
  -2 grad pi . grad(d_t F) - Lap pi d_t F reappear (they are what a MOVING source feeds the khronon; L340's T1 physics).  rc = 1.

SCOPE.  Decoupling limit (metric frozen), static background, plane-wave power counting; O(1) coefficients not tracked
beyond the displayed bounds.  With XC1 this completes G8 at frozen-background, decoupling-limit scope.  Still NOT
covered: full curved-background mixing, the assembled action (lead track: 'conditional at full-action scope'), loops.

Run from the repository root:  python3 real_research/extra_crispy_2026/XC3_filter_foliation_vertices.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "XC3", "XC3_filter_foliation_vertices"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
RNG = np.random.default_rng(3)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT IS CHECKED")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the background is time dependent (d_t W_0 != 0); C1 must FAIL ***")

# ============================================================================================ jets
e = sp.Symbol('e')
p = sp.symbols('p0:4')                                           # d_mu pi
Hh = [[None] * 4 for _ in range(4)]
for m in range(4):
    for n in range(m, 4):
        Hh[m][n] = Hh[n][m] = sp.Symbol(f'h{m}{n}')              # d_mu d_nu pi
w = sp.symbols('w0:4')                                           # d_mu W_0   (w0 = d_t W_0)
Wm = [[None] * 4 for _ in range(4)]
for m in range(4):
    for n in range(m, 4):
        Wm[m][n] = Wm[n][m] = sp.Symbol(f'W{m}{n}')              # d_mu d_nu W_0
STATIC = {} if MUTATE else {w[0]: 0, **{Wm[0][m]: 0 for m in range(4)}}
eta = [-1, 1, 1, 1]
NT = 4
def tr(expr, n=NT):
    ex = sp.expand(expr)
    return sum(ex.coeff(e, j) * e**j for j in range(n + 1))
d = [(1 if m == 0 else 0) + e * p[m] for m in range(4)]
u_ = tr(-sum(eta[m] * d[m]**2 for m in range(4)) - 1)
def powX(r):
    acc, term = sp.S(0), sp.S(1)
    for kx in range(NT + 1):
        acc += sp.binomial(r, kx) * term
        term = tr(term * u_)
    return tr(acc)
Xm12, Xm32 = powX(sp.Rational(-1, 2)), powX(sp.Rational(-3, 2))
n_dn = [tr(-d[m] * Xm12) for m in range(4)]
n_up = [eta[m] * n_dn[m] for m in range(4)]
Jn = [[tr(-(1 if m == a_ else 0) * Xm12 - d[m] * eta[a_] * d[a_] * Xm32) for a_ in range(4)] for m in range(4)]
dn = [[tr(sum(Jn[m][a_] * e * Hh[a_][nu] for a_ in range(4))) for nu in range(4)] for m in range(4)]
Kx = tr(sum(eta[m] * dn[m][m] for m in range(4)))
h_uu = [[tr(eta[m] * (1 if m == nn else 0) + n_up[m] * n_up[nn]) for nn in range(4)] for m in range(4)]

# ============================================================================================ C1
banner("C1  THE LEAF LAPLACIAN OF A (STATIC) BACKGROUND FIELD UNDER THE TILT tau = t + pi")
DeltaF = tr(sum(h_uu[m][nn] * Wm[m][nn] for m in range(4) for nn in range(4)) + Kx * sum(n_up[m] * w[m] for m in range(4)))
DeltaF = sp.expand(DeltaF.subs(STATIC))
D0, D1, D2 = [sp.expand(DeltaF.coeff(e, j)) for j in range(3)]
lap_pi = Hh[1][1] + Hh[2][2] + Hh[3][3]
pw = sum(p[i] * w[i] for i in (1, 2, 3))
target2 = sp.expand(sum(p[i] * p[j] * Wm[i][j] for i in (1, 2, 3) for j in (1, 2, 3)) + lap_pi * pw)
r0 = sp.expand(D0 - (Wm[1][1] + Wm[2][2] + Wm[3][3]))
r2 = sp.expand(D2 - target2)
P(f"    O(pi^0) - Lap F = {r0};   O(pi^1) = {D1}")
P(f"    O(pi^2) - [d_i pi d_j pi d_i d_j F + Lap pi (grad pi . grad F)] = {r2 if not MUTATE else '(time-dependent background: see O(pi))'}")
OUT["numbers"]["C1"] = {"O0_residual": str(r0), "O1": str(D1), "O2_residual": str(r2)}
check("C1 for a static background the leaf Laplacian has no O(pi) term and its O(pi^2) term is "
      "d_i pi d_j pi d_i d_j F + Lap pi (grad pi . grad F): every filter correction carries the background's gradient or curvature",
      f"O(pi^0) residual {r0}; O(pi) = {D1}; O(pi^2) residual {r2}", r0 == 0 and D1 == 0 and r2 == 0,
      "the tilt enters the heat kernel only at second order, and only through the background it acts on")

# ============================================================================================ C2
banner("C2  THE q-ARGUMENT h^{mu nu} d W_0 d W_0 UNDER THE TILT")
Xh = tr(sum(h_uu[m][nn] * w[m] * w[nn] for m in range(4) for nn in range(4)))
Xh = sp.expand(Xh.subs(STATIC))
X0, X1, X2, X3 = [sp.expand(Xh.coeff(e, j)) for j in range(4)]
w2 = w[1]**2 + w[2]**2 + w[3]**2
rX0, rX1 = sp.expand(X0 - w2), X1
rX2 = sp.expand(X2 - pw**2)
rX3 = sp.expand(X3 - (-2 * p[0] * pw**2))
P(f"    O(1) - |grad W0|^2 = {rX0};  O(pi) = {rX1};  O(pi^2) - (grad pi . grad W0)^2 = {rX2};  O(pi^3) + 2 pi_t (grad pi . grad W0)^2 = {rX3}")
OUT["numbers"]["C2"] = {"residuals": [str(rX0), str(rX1), str(rX2), str(rX3)]}
check("C2 the leaf-metric dependence of the q-argument starts at O(pi^2): X_h = |grad W0|^2 + (grad pi.grad W0)^2 "
      "- 2 pi_t (grad pi.grad W0)^2 + O(pi^4) -- two powers of the background field in every term",
      f"residuals {rX0}, {rX1}, {rX2}, {rX3}", rX0 == 0 and rX1 == 0 and rX2 == 0 and rX3 == 0)

# ============================================================================================ C3
banner("C3  THE HEAT-KERNEL DERIVATIVE dS = b Int_0^1 e^{(1-v) b Delta} dDelta e^{v b Delta} dv (periodic grid)")
NG = 96; L_ = 1.0; dxg = L_ / NG
# NOTE: Apple-Accelerate BLAS raises spurious floating-point flags on these dense matmuls; every matrix used below is
# checked finite and the result is cross-checked (finite differences), so the flags are silenced for this block only.
_errs = np.seterr(all='ignore')
kk = 2 * np.pi * np.fft.fftfreq(NG, d=dxg)
xg = np.arange(NG) * dxg
Dmat = np.real(np.fft.ifft(np.diag(-(kk**2)) @ np.fft.fft(np.eye(NG), axis=0), axis=0))      # spectral Laplacian
amp = 0.3 * (1 + 0.5 * np.sin(2 * np.pi * xg) + 0.3 * np.cos(6 * np.pi * xg))
Pmat = np.diag(amp) @ Dmat                                        # a non-commuting perturbation: a(x) d_x^2
bb = 2.5e-4
def expm_sym(A):
    As = 0.5 * (A + A.T)
    lam, V = np.linalg.eigh(As)
    return (V * np.exp(lam)) @ V.T
from scipy.linalg import expm
S0 = expm(bb * Dmat)
vs = np.linspace(0, 1, 401); wts = np.full(vs.size, vs[1] - vs[0]); wts[0] = wts[-1] = 0.5 * (vs[1] - vs[0])
f = np.real(np.fft.ifft(np.fft.fft(RNG.standard_normal(NG)) * np.exp(-0.5 * (kk / 40.0)**2)))
dSf = np.zeros(NG)
for v_, wt in zip(vs, wts):
    dSf += wt * (expm_sym((1 - v_) * bb * Dmat) @ (Pmat @ (expm_sym(v_ * bb * Dmat) @ f)))
dSf *= bb
errs = []
for eps in (1e-2, 5e-3, 2.5e-3):
    Sfd = expm(bb * (Dmat + eps * Pmat))
    errs.append(float(np.linalg.norm(Sfd @ f - S0 @ f - eps * dSf) / np.linalg.norm(eps * dSf)))
order = math.log(errs[0] / errs[2]) / math.log(4.0)
bound_ratio = float(np.linalg.norm(dSf) / (bb * max(np.linalg.norm(Pmat @ expm_sym(v_ * bb * Dmat) @ f) for v_ in vs)))
finite_ok = bool(np.all(np.isfinite(Dmat)) and np.all(np.isfinite(S0)) and np.all(np.isfinite(dSf)))
np.seterr(**_errs)
Kv = np.array([1.0, 10.0, 100.0]) / math.sqrt(bb)
fac = (1 - np.exp(-bb * Kv**2)) / Kv**2
P(f"    relative residual ||S(eps) f - S(0) f - eps dS f|| / ||eps dS f|| at eps = 1e-2, 5e-3, 2.5e-3: {', '.join(f'{x:.2e}' for x in errs)}"
  f"  (falls as eps^{order:.2f}: the absolute residual is second order; all matrices finite: {finite_ok})")
P(f"    ||dS f|| / (b max_v ||dDelta e^(v b Delta) f||) = {bound_ratio:.3f}  (<= 1: the heat semigroup is a contraction)")
P(f"    high-K factor (1 - e^(-b K^2))/K^2 at K sqrt(b) = 1, 10, 100: {', '.join(f'{x:.3e}' for x in fac)}  vs 1/K^2: "
  f"{', '.join(f'{x:.3e}' for x in 1 / Kv**2)}")
OUT["numbers"]["C3"] = {"fd_rel_residuals": errs, "order": order, "bound_ratio": bound_ratio}
check("C3 the Frechet-derivative formula for the leaf-dependent heat kernel is verified (the relative residual falls as "
      "eps^1, i.e. the absolute residual is second order) and the derivative is bounded by b times the perturbation acting "
      "on the smoothed field",
      f"relative-residual order {order:.2f}; residual at eps = 2.5e-3: {errs[-1]:.1e}; bound ratio {bound_ratio:.3f}",
      finite_ok and abs(order - 1.0) < 0.1 and errs[-1] < 1e-2 and bound_ratio <= 1.0 + 1e-6)

# ============================================================================================ backgrounds
C_SI, A0 = 2.99792458e8, 9.3619e-11
G_SI, MSUN, PC = 6.6743e-11, 1.98892e30, 3.0856775814913673e16
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.clip(y, 1e-300, 1e4))), 0.0)
def CT(y): return float(h_rar(y) / y)                          # nu_RAR's C_T = nu_mono's below y_p
L340 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")))
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
# (name, filtered-kernel argument y, background coherence length L_bg [m], potential depth Phi/c^2)
BG = [("Sun, in the Galaxy's field", 2.3, 8.2e3 * PC, 5.0e-7),
      ("galaxy, transition", 1.0, 1.0e4 * PC, 5.0e-7),
      ("galaxy, deep MOND", 0.1, 5.0e4 * PC, 3.0e-7),
      ("cluster core", 20.0, 3.0e5 * PC, 1.0e-5)]

# ============================================================================================ C4
banner("C4  THE INDUCED QUADRATIC TERMS vs THE KHRONON'S OWN GRADIENT TERM c_2 k^4")
rowsC4 = []
for nm, y, Lbg, phi in BG:
    g = y * A0 / C_SI**2                                           # |grad W0| in 1/m
    ct = CT(y)
    for kname, k in (("1/L_bg", 1 / Lbg), ("1/pc", 1 / PC), ("1/AU", 1 / 1.496e11)):
        for c2v in (C2_MIN, C2_MAX):
            ratio = 6 * ct * g**2 / (c2v * k**2)
            rowsC4.append({"bg": nm, "k": kname, "c2": c2v, "ratio": ratio})
worst4 = max(r["ratio"] for r in rowsC4)
for r in rowsC4:
    if r["c2"] == C2_MIN:
        P(f"    {r['bg']:28s} k = {r['k']:6s}: 6 C_T g^2/(c_2 k^2) = {r['ratio']:.2e}")
OUT["numbers"]["C4"] = {"rows": rowsC4, "worst": worst4}
check("C4 the filter/foliation quadratic terms are negligible against the khronon's own gradient term at every k inside "
      "the background (k >= 1/L_bg), for the Sun, galaxies and cluster cores, at both c_2 edges",
      f"largest ratio {worst4:.2e} (at k = 1/L_bg)", worst4 < 1e-3,
      "the ratio is 6 C_T (g L_bg)^2/c_2 at the lowest local k: set by (g L_bg) ~ Phi/c^2, the background's depth")

# ============================================================================================ C5
banner("C5  THE SIGN: a formally unstable band k < g sqrt(2 C_T/c_2), and why it lies outside the local regime")
rowsC5 = []
for nm, y, Lbg, phi in BG:
    g = y * A0 / C_SI**2; ct = CT(y)
    kthr = g * math.sqrt(2 * ct / C2_MIN)                         # the smallest c_2 widens the band most
    rowsC5.append({"bg": nm, "k_thr_1_per_m": kthr, "k_thr_L_bg": kthr * Lbg, "Phi_sqrt": phi * math.sqrt(2 * ct / C2_MIN)})
    P(f"    {nm:28s}: k_thr L_bg = {kthr * Lbg:.2e}   (Phi/c^2) sqrt(2 C_T/c_2) = {phi * math.sqrt(2 * ct / C2_MIN):.2e}   "
      f"-> wavelength {2 * math.pi / kthr / 3.0857e22:.2e} Mpc")
worst5 = max(r["k_thr_L_bg"] for r in rowsC5)
OUT["numbers"]["C5"] = {"rows": rowsC5, "worst_kthr_Lbg": worst5}
check("C5 the formally unstable band lies far below the background's inverse coherence length (k_thr L_bg << 1) for every "
      "background, so no local mode ever sees it; its width is set by g L_bg ~ Phi/c^2 << 1",
      f"largest k_thr L_bg = {worst5:.2e}", worst5 < 1e-2,
      "a WKB mode needs k L_bg >> 1; the band needs k < k_thr; both cannot hold. The destabilising sign is real but "
      "confined to wavelengths longer than the structure that produces it (Mpc-to-Gpc), where cosmology, not this term, rules")

# ============================================================================================ C6
banner("C6  THE CUBIC VERTICES: relevant operators with background-suppressed couplings")
HBARC = 1.973269804e-16; MPL = 2.435e18
def cs_uv(a, c2v): return math.sqrt(c2v * (2 - a) / (a * (2 + 3 * c2v)))
rowsC6 = []
for nm, y, Lbg, phi in BG:
    gG = y * A0 / C_SI**2 * HBARC                                  # g in GeV
    ct = CT(y)
    for a_c in (AC_MIN, AC_MAX):
        for c2v in (C2_MIN, C2_MAX):
            cs = cs_uv(a_c, c2v)
            lam_ir = ct * gG**2 / (MPL * a_c**1.5 * cs**1.5)       # coupling of -2 M^2 C_T pi_t (grad pi . grad W0)^2
            rowsC6.append({"bg": nm, "alpha_c": a_c, "c2": c2v, "Lambda_IR_GeV": lam_ir})
worst6 = max(r["Lambda_IR_GeV"] for r in rowsC6)
P(f"    leading cubic vertex -2 M_P^2 C_T pi_t (grad pi.grad W0)^2 (N = 3 derivatives, 3 fields): relevant, coupling C_T g^2")
P(f"    strong only BELOW Lambda_IR = C_T g^2/(M_P alpha^(3/2) c_s^(3/2)); over the window and backgrounds: max {worst6:.2e} GeV")
P(f"    (the Hubble scale is {6.582e-25 * 2.18e-18:.1e} GeV)")
OUT["numbers"]["C6"] = {"rows": rowsC6, "max_Lambda_IR_GeV": worst6}
check("C6 every filter/foliation cubic vertex is relevant with a background-suppressed coupling; its IR strong-coupling "
      "scale is far below the Hubble energy over the whole window, so it is never strong at any physical scale",
      f"max Lambda_IR = {worst6:.2e} GeV (Hubble energy 1.4e-42 GeV)", worst6 < 1e-50)

banner("VERDICT")
P(f"""  The filter's own foliation dependence -- the piece XC1 left out -- is harmless at frozen-background, decoupling-limit
  scope.  On a static background the tilt enters the heat kernel and the leaf metric only at O(pi^2), and every induced
  term carries two powers of the background (C1, C2).  The quadratic terms are <= {worst4:.0e} of the khronon's own gradient
  term wherever a local mode exists (C4); their destabilising sign is confined to wavelengths longer than the structure
  that produces them (C5); the cubic vertices are relevant operators strong only below {worst6:.0e} GeV (C6).  A MOVING
  background re-introduces O(pi) mixing (MUTATE) -- that is the moving-source physics of L340's T1, not a new vertex.
  With XC1: G8 is a bounded pass at frozen-background, decoupling-limit scope, now including the filter/foliation
  interaction.  Still conditional at full-action scope (curved-background mixing, the assembled action, loops).  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
