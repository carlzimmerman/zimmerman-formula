#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XC1 -- G8, THE STRONG-COUPLING GATE, RUN ON C-H/K.  The recipe's red-flagged "make-or-break" gate
(qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md sec. 5 G8 and the sec. 9 table: "G8 Lambda_sc as
eta -> 0 -- OPEN -- THE make-or-break") was never computed on any candidate: the khronometric candidate it was written
for died first (FC-KH, radial gradient instability), and the live candidate C-H/K (L340) lists it nowhere.  This lane
runs it on C-H/K.

THE GATE (recipe G8, verbatim intent): canonically normalise; compute the strong-coupling scale on the ACTUAL
Solar-System background; require it far above the energies at which gravity is probed.  A vanishing kinetic
coefficient is not rescued by a large sound speed (recipe P7).

THE CANDIDATE.  I_CHK = I_CH + (c^3/16 pi G) Int sqrt(-g) [alpha_c a_mu a^mu - c_2 K^2]  (L340; beta = 0, c_T = 1;
L350's leaf-average form -c_2 (K - <K>)^2 is identical for every k != 0 mode).  astra's C-H supplies
2 h^{mu nu}(D_mu U - a_mu)(D_nu U - a_nu) + 2 alpha_M^2 q(|D S U|^2/alpha_M^2), with the heat filter
S = exp((xi^2/2) Delta_h) and alpha_M = a0/c^2.  The khronon is tau = x^0 + pi.  In the literature's covariant form
(Guemruekcueoglu, Saravani & Sotiriou 2018, PRD 97 024032, eq. 2) the khronometric part is alpha a.a - gamma K^2 with
gamma = c_2, beta = 0.

WHAT IS CHECKED (each check can fail)
  A1 [sympy, jet variables] the decoupling-limit khronometric Lagrangian alpha a.a - c_2 K^2 on flat space: no
     tadpole; the quadratic form alpha |grad pi_t|^2 - c_2 (Lap pi)^2; the cubic vertices EXACTLY
        2 c_2 Lap pi (2 grad pi.grad pi_t + pi_t Lap pi)
        - 2 alpha [pi_tt grad pi_t.grad pi + pi_t |grad pi_t|^2 + d_i pi_t d_i d_j pi d_j pi];
     every order-e^j monomial carries exactly j fields; and a_mu = h_mu^nu d_nu ln N (N = X^-1/2) to 4th order.
  A2 [power counting vs literature] each vertex class (coupling, number of time derivatives, total derivatives)
     becomes strong at a definite scale in the frame where the khronon is relativistic; the minimum over the cubic AND
     quartic classes must be sqrt(alpha) M c_s^{3/2} (c_s < 1) and sqrt(alpha) M c_s^{-1/2} (c_s > 1): eq. (15) of
     Guemruekcueoglu+18 (from Kimpton & Padilla 2010).  A literature control that can fail.
  A3 [the C-H sector] eliminating U from its quadratic block gives the clock inertia 2C/(1+C) (C = C_0 e^{-xi^2 k^2});
     with U = ln N the C-H term vanishes IDENTICALLY (h^{mu nu} n_mu = 0), and its cubic vertices vanish at C = 0.  So
     at k >> 1/xi the khronon is exactly the BPS khronon with alpha = alpha_c.  Numbers: log10 C(k) at AU scales.
  A4 [G8 proper: the Solar System] with alpha = alpha_c the strong-coupling momentum over L340's alpha_c window
     x {L350's Planck-era caps, L340's c_2 window}, against the probes: Solar-System orbits, LIGO at 100 Hz, the
     52 um torsion balance, the LHC.  Gate: >= 1e3 above every probe momentum.  a0 does not enter (both footings).
  A5 [the MOND regime, k < 1/xi] alpha_eff = alpha_c + 2C/(1+C) for nu_mono's C_T and C_L from deep MOND to a galactic
     nucleus, including y = 2.3 (the Galaxy's field at the Sun, which the filtered kernel sees); mode speed from L340's
     full block, c_s^2 = c_2/(C(2+3c_2)).
  A6 [the MOND vertex, sympy] the cubic term of 2 alpha_M^2 q(|v+w|^2) along the field is (2/3) C_L'(y) (d_par S dU)^3
     / alpha_M, with q' = C_T and C_L = C_T + y C_T'; eliminating dU = -pi_t/(1+C_L) and power counting gives the scale
     where the UNFILTERED MOND sector would be strongly coupled.
  A7 [the dark-energy identity] if a0 = kappa c sqrt(G rho) then sqrt(M_P a0/c^2) = (kappa^2/8 pi)^{1/4} rho^{1/4}
     exactly (natural units, M_P reduced): the unfiltered MOND sector's cutoff is set by the dark-energy scale itself.
  A8 [the filter] each MOND leg carries e^{-xi^2 k^2/2}, so the largest the MOND coupling ever gets is
     max_k (k/k_M)^2 e^{-3 xi^2 k^2/2} = (2/3e)/(xi k_M)^2, at the committed Cassini floors xi = 0.031 / 0.045 pc.
  A9 (reading, not load-bearing) the UV khronon speed c_s^2 = c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) over the window:
     finite and hyperbolic, causal on the preferred foliation (L318's criterion B); superluminal w.r.t. the metric cone
     (criterion A, which L318 shows every scalar realisation fails).

  MUTATE=1 sets alpha_c = 0.  The UV kinetic term is then 2C_0 e^{-xi^2 k^2}/(1+...), exponentially zero at every
  Solar-System momentum, so A4 must FAIL (the recipe's P7; Franchini, Herrero-Valea & Barausse 2021, PRD 103 084012,
  find the alpha = beta = 0 khronon strongly coupled on curved backgrounds too).  rc = 1.

SCOPE.  Tree-level power counting in the decoupling limit, which is exact in the structure and accurate to O(alpha_c,
c_2) in the UV, where C-H/K IS BPS khronometric gravity (A3); in the MOND regime metric mixing is O(1) (L340's block),
so A5/A6 are order-of-magnitude, which the margins found make irrelevant.  O(1) vertex coefficients are not tracked
(standard).  Frozen backgrounds.  The vertices from the filter's own metric/foliation dependence (the Frechet
derivative of S = exp(b Delta_h)) carry two powers of alpha_M or the background's second derivatives and are not
computed separately.  NOT a loop / naturalness statement (recipe G12) and NOT a UV completion.

Run from the repository root:  python3 real_research/extra_crispy_2026/XC1_strong_coupling_chk.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "XC1", "XC1_strong_coupling_chk"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


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
    P("\n  *** MUTATE=1: alpha_c = 0 -- the UV khronon keeps only the filtered C-H inertia; A4 must FAIL ***")

# ---------------------------------------------------------------------------------------------------- constants
HBARC_GEV_M = 1.973269804e-16          # GeV m
HBAR_GEV_S = 6.582119569e-25           # GeV s
GEV_J = 1.602176634e-10
G_SI, C_SI = 6.67430e-11, 2.99792458e8
MPL_RED = 2.435e18                     # reduced Planck mass, GeV (c^3/16 pi G = M^2/2)
PC, AU = 3.0856775814913673e16, 1.495978707e11
H0 = 67.4e3 / (1e6 * PC); OML = 0.6847
RHO_C = 3 * H0**2 / (8 * math.pi * G_SI)
FOOT = {"canonical": {"a0": 9.3619e-11, "rho": OML * RHO_C, "what": "rho_Lambda"},
        "alt": {"a0": 1.1279e-10, "rho": RHO_C, "what": "rho_total"}}
L340 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")))
L350 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L350_chk_cosmological_G_gate_results.json")))
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
CAPS = sorted({round(float(r["c2_ceiling"]), 6) for r in L350["numbers"]["G2"]["rows"]
               if r.get("c2_ceiling") is not None and np.isfinite(float(r["c2_ceiling"]))})
XI_FLOORS_PC = (0.031, 0.045)           # committed C-H/T-B Cassini floors (canonical/alt quadrupole), L340 S1
P(f"\n  inputs: L340 window alpha_c in ({AC_MIN:.2e}, {AC_MAX:.1e}), c_2 in ({C2_MIN:.2e}, {C2_MAX:.4f}); "
  f"L350 Planck-era c_2 caps {CAPS}; xi floors {XI_FLOORS_PC} pc")

# ============================================================================================ A1 jets
banner("A1  THE DECOUPLING-LIMIT KHRONOMETRIC LAGRANGIAN (jet variables, flat space, tau = t + e pi)")
e = sp.Symbol('e')
al, c2s = sp.symbols('alpha c_2', positive=True)
p = sp.symbols('p0:4')
H = [[None] * 4 for _ in range(4)]
for m in range(4):
    for n in range(m, 4):
        H[m][n] = H[n][m] = sp.Symbol(f'h{m}{n}')
HS = sorted({H[m][n] for m in range(4) for n in range(4)}, key=lambda s: s.name)
eta = [-1, 1, 1, 1]
NT = 5                                                                    # keep e^0 .. e^5 (quartic needs e^4; identities to e^5)
def tr(expr, n=NT):
    """exact truncation of a polynomial in e at order n (every quantity below is polynomial in e and the jets)."""
    ex = sp.expand(expr)
    return sum(ex.coeff(e, j) * e**j for j in range(n + 1))
d = [(1 if m == 0 else 0) + e * p[m] for m in range(4)]                  # d_mu tau
u_ = tr(-sum(eta[m] * d[m]**2 for m in range(4)) - 1)                   # X = 1 + u, u = O(e)
def powX(r):
    """X^r = (1 + u)^r as the exact binomial series truncated at e^NT (u starts at order e)."""
    acc, term = sp.S(0), sp.S(1)
    for kx in range(NT + 1):
        acc += sp.binomial(r, kx) * term
        term = tr(term * u_)
    return tr(acc)
Xm12, Xm32, Xm1 = powX(sp.Rational(-1, 2)), powX(sp.Rational(-3, 2)), powX(-1)
n_dn = [tr(-d[m] * Xm12) for m in range(4)]                              # n_mu = -d_mu tau / sqrt(X)
n_up = [eta[m] * n_dn[m] for m in range(4)]
Jn = [[tr(-(1 if m == a_ else 0) * Xm12 - d[m] * eta[a_] * d[a_] * Xm32) for a_ in range(4)] for m in range(4)]  # dn_m/dd_a
dn = [[tr(sum(Jn[m][a_] * e * H[a_][nu] for a_ in range(4))) for nu in range(4)] for m in range(4)]           # d_nu n_mu
a_dn = [tr(sum(n_up[nu] * dn[m][nu] for nu in range(4))) for m in range(4)]                                    # n^nu d_nu n_mu
Kx = tr(sum(eta[m] * dn[m][m] for m in range(4)))                                                              # d_mu n^mu
aa = tr(sum(eta[m] * a_dn[m]**2 for m in range(4)))
LB = tr(al * aa - c2s * tr(Kx**2))
Lk = {j: sp.expand(LB.coeff(e, j)) for j in range(5)}
lap = H[1][1] + H[2][2] + H[3][3]
gp_gpt = sum(p[i] * H[0][i] for i in (1, 2, 3))
gpt2 = sum(H[0][i]**2 for i in (1, 2, 3))
hgh = sum(H[0][i] * H[i][j] * p[j] for i in (1, 2, 3) for j in (1, 2, 3))
L2_target = al * gpt2 - c2s * lap**2
L3_target = 2 * c2s * lap * (2 * gp_gpt + p[0] * lap) - 2 * al * (H[0][0] * gp_gpt + p[0] * gpt2 + hgh)
r2 = sp.expand(Lk[2] - L2_target); r3 = sp.expand(Lk[3] - L3_target)
# homogeneity: an order-e^j monomial carries exactly j fields (p's and h's)
JET = list(p) + HS
def field_count_ok(expr, j):
    for mono in sp.Poly(expr, *JET).monoms():
        if sum(mono) != j:
            return False
    return True
homog = all(field_count_ok(Lk[j], j) for j in (2, 3, 4))
# a_mu = h_mu^nu d_nu ln N, N = X^{-1/2}:  d_nu ln N = -(d_nu X)/(2X),  d_nu X = sum_a (-2 eta_a d_a) e H_{a nu}
dX = [tr(sum(-2 * eta[a_] * d[a_] * e * H[a_][nu] for a_ in range(4))) for nu in range(4)]
dlnN = [tr(-dX[nu] * Xm1 / 2) for nu in range(4)]
h_mix = [[tr((1 if mu == nu else 0) + n_dn[mu] * n_up[nu]) for nu in range(4)] for mu in range(4)]       # h_mu^nu
ident = [tr(a_dn[mu] - sum(h_mix[mu][nu] * dlnN[nu] for nu in range(4))) for mu in range(4)]
P(f"    order 0 / 1: {Lk[0]} / {Lk[1]}")
P(f"    L2 = {sp.factor(Lk[2])}")
P(f"    L3 - target = {r3};  every order-e^j monomial has j fields: {homog};  a_mu - h_mu^nu d_nu ln N through e^4: {ident}")
OUT["numbers"]["A1"] = {"L2": str(Lk[2]), "L3": str(Lk[3]), "L2_residual": str(r2), "L3_residual": str(r3), "homogeneous": homog,
                        "acc_identity": [str(x) for x in ident]}
check("A1 no tadpole; L2 = alpha |grad pi_t|^2 - c_2 (Lap pi)^2; the cubic vertices are exactly the displayed c_2- and "
      "alpha-structures; a_mu = h_mu^nu d_nu ln N holds through 4th order",
      f"L0 = {Lk[0]}, L1 = {Lk[1]}, L2 residual {r2}, L3 residual {r3}, homogeneous {homog}, identity residuals {ident}",
      Lk[0] == 0 and Lk[1] == 0 and r2 == 0 and r3 == 0 and homog and all(x == 0 for x in ident),
      "the healthy BPS khronon: alpha > 0 gives the time kinetic term, c_2 > 0 the gradient term; c_s^2 = c_2/alpha here")

# ============================================================================================ A2 power counting
banner("A2  POWER COUNTING OF EVERY CUBIC AND QUARTIC CLASS, AGAINST THE LITERATURE'S STRONG-COUPLING SCALE")
M_, A_, CS_ = sp.symbols('M alpha c_s', positive=True)
def classes(expr, order):
    out = {}
    for mono, coeff in sp.Poly(expr, *JET).terms():
        pw = dict(zip(JET, mono))
        nt = pw[p[0]] + sum(pw[s] * ((s.name[1] == '0') + (s.name[2] == '0')) for s in HS)
        nd = sum(pw[x] for x in p) + 2 * sum(pw[s] for s in HS)
        cpl = 'c2' if sp.sympify(coeff).has(c2s) else 'alpha'
        out[(order, cpl, int(nt), int(nd))] = out.get((order, cpl, int(nt), int(nd)), 0) + 1
    return out
CL = {}
for j in (3, 4):
    CL.update(classes(Lk[j], j))
# A vertex g M^2 d_t^{n_t} d_x^{N-n_t} pi^F with the canonical field phi = M sqrt(alpha) |k| pi, time rescaled t = t~/c_s so
# the free khronon is relativistic, phi~ = sqrt(c_s) phi: its rescaled-frame coefficient is g M^{2-F} alpha^{-F/2}
# c_s^{n_t - F/2 - 1} with mass dimension 4 - N, so the vertex is O(1) at Lambda = coefficient^{1/(4-N)}.
rows, exps, pure_power = [], [], True
for (F, cpl, nt, N), cnt in sorted(CL.items()):
    j = 0 if cpl == 'alpha' else 1                                     # c_2 = alpha c_s^2
    g = A_ * CS_**(2 * j)
    coef = g * M_**(2 - F) * A_**sp.Rational(-F, 2) * CS_**(nt - sp.Rational(F, 2) - 1)
    Lam = sp.simplify(coef**sp.Rational(1, 4 - N))
    expo = (2 * j + nt - sp.Rational(F, 2) - 1) / sp.Integer(4 - N)
    pure_power = pure_power and sp.simplify(Lam / (sp.sqrt(A_) * M_ * CS_**expo)) == 1
    exps.append(expo)
    rows.append({"fields": F, "coupling": cpl, "n_t": nt, "N": N, "count": cnt, "Lambda": str(Lam), "cs_exponent": str(expo)})
    P(f"    {F}-point  {cpl:5s}  n_t = {nt}  N = {N}  ({cnt:3d} monomials):  Lambda = {Lam}  = sqrt(alpha) M c_s^({expo})")
lit_lt1, lit_gt1 = sp.Rational(3, 2), sp.Rational(-1, 2)
ok_lit = pure_power and max(exps) == lit_lt1 and min(exps) == lit_gt1
P(f"    every class is sqrt(alpha) M c_s^p exactly: {pure_power};  exponents {sorted(set(exps))}")
P(f"    minimum scale: c_s < 1 -> sqrt(alpha) M c_s^{max(exps)};  c_s > 1 -> sqrt(alpha) M c_s^{min(exps)}")
OUT["numbers"]["A2"] = {"classes": rows, "min_exponent_cs_lt_1": str(max(exps)), "min_exponent_cs_gt_1": str(min(exps))}
check("A2 the lowest strong-coupling scale over all cubic and quartic vertex classes reproduces Guemruekcueoglu+18 eq. (15): "
      "sqrt(alpha) M c_s^{3/2} for c_s < 1 and sqrt(alpha) M c_s^{-1/2} for c_s > 1",
      f"exponents found {sorted(set(exps))}; branch minima c_s^{max(exps)} / c_s^{min(exps)}", ok_lit,
      "for a superluminal khronon the binding vertices are the c_2 cubic and the alpha cubic with three time derivatives")

# ============================================================================================ A3 the C-H sector
banner("A3  THE C-H SECTOR: its clock inertia, its exact vanishing at U = ln N, and its cubic vertices at C = 0")
u, v, Cc, kk = sp.symbols('u v C k', real=True)
Lq = 2 * kk**2 * (u + v)**2 + 2 * Cc * kk**2 * u**2          # 2|grad(dU + pi_t)|^2 + 2 C |grad dU|^2, Fourier, v = pi_t
u_star = sp.solve(sp.diff(Lq, u), u)[0]
L_star = sp.simplify(Lq.subs(u, u_star))
sq_ok = sp.simplify(Lq - L_star - 2 * kk**2 * (1 + Cc) * (u - u_star)**2) == 0
# exact vanishing at U = ln N: 2 h^{mu nu}(d_mu lnN - a_mu)(d_nu lnN - a_nu), with a = h.dlnN from A1
h_up_up = [[tr(eta[m] * (1 if m == nn else 0) + n_up[m] * n_up[nn]) for nn in range(4)] for m in range(4)]
Vv = [tr(dlnN[mu] - a_dn[mu]) for mu in range(4)]
LCH_lnN_s = tr(2 * sum(h_up_up[m][nn] * tr(Vv[m] * Vv[nn]) for m in range(4) for nn in range(4)))
# cubic C-H vertices with the linear solution dU = -pi_t/(1+C) (dU at 2nd order multiplies the linear equation)
Cs = sp.Symbol('C', nonnegative=True)
dU1 = [-e * H[0][mu] / (1 + Cs) for mu in range(4)]           # d_mu dU_1 = -d_mu pi_t/(1+C)
V1 = [tr(dU1[mu] - a_dn[mu], 3) for mu in range(4)]
LCH_lin = tr(2 * sum(tr(h_up_up[m][nn] * tr(V1[m] * V1[nn], 3), 3) for m in range(4) for nn in range(4)), 3)
LCH3 = sp.expand(LCH_lin.coeff(e, 3))
LCH3_at0 = sp.simplify(LCH3.subs(Cs, 0))
LCH2 = sp.expand(LCH_lin.coeff(e, 2))
LCH2_target = sp.expand(2 * (Cs / (1 + Cs))**2 * gpt2)         # the linear-U part alone; + the q-term's 2C|grad dU|^2 -> 2C/(1+C)
P(f"    Fourier block 2k^2(u+v)^2 + 2Ck^2u^2:  u* = {u_star},  value {L_star};  perfect square about u*: {sq_ok}")
P(f"    2 h^mn (d lnN - a)_m (d lnN - a)_n through e^5: {LCH_lnN_s}   (h^{{mu nu}} n_mu = 0: U = ln N makes C-H vanish)")
P(f"    cubic C-H vertices on the linear solution, at C = 0: {LCH3_at0};  quadratic part = 2(C/(1+C))^2|grad pi_t|^2: "
  f"{sp.simplify(LCH2 - LCH2_target) == 0}")
LN10 = math.log(10.0)
logC_uv = {}
for xi_pc in XI_FLOORS_PC:
    xi_m = xi_pc * PC
    for nm, lam_m in (("1 AU", AU), ("Earth-Moon", 3.844e8), ("52 um", 52e-6)):
        k_m = 1.0 / lam_m
        logC_uv[f"xi={xi_pc}pc, k=1/{nm}"] = -(xi_m * k_m)**2 / LN10          # log10[C(k)/C_0]
for kx, vx in logC_uv.items():
    P(f"    log10 C(k)/C_0 = -(xi k)^2/ln10 at {kx}: {vx:.3e}")
OUT["numbers"]["A3"] = {"u_star": str(u_star), "inertia": str(L_star), "LCH_at_lnN": str(LCH_lnN_s), "cubic_at_C0": str(LCH3_at0),
                        "log10_C_over_C0": logC_uv}
check("A3 eliminating U gives the clock inertia 2C/(1+C) (a perfect square, so the minimum); with U = ln N the C-H term is "
      "identically zero; the cubic C-H vertices vanish at C = 0; at every Solar-System momentum C(k)/C_0 < 10^-400",
      f"inertia {L_star}; C-H at U = lnN: {LCH_lnN_s}; cubic at C=0: {LCH3_at0}; max log10 C/C0 = {max(logC_uv.values()):.2e}",
      sp.simplify(L_star - 2 * kk**2 * v**2 * Cc / (1 + Cc)) == 0 and sq_ok and LCH_lnN_s == 0 and LCH3_at0 == 0
      and max(logC_uv.values()) < -400,
      "above k ~ 1/xi the filter removes the MOND sector completely: the UV khronon of C-H/K IS the BPS khronon with "
      "alpha = alpha_c, lambda - 1 = c_2, beta = 0")

# ============================================================================================ A4 the Solar System
banner("A4  G8 PROPER: THE SOLAR-SYSTEM (UV) STRONG-COUPLING SCALE OVER THE WINDOW, AGAINST THE PROBES")
def cs2_bps(alpha, c2):
    return c2 * (2 - alpha) / (alpha * (2 + 3 * c2))      # Guemruekcueoglu+18 eq. (4), beta = 0, gamma = c_2
def msc(alpha, c2):
    """lowest strong-coupling MOMENTUM (GeV) and ENERGY (GeV): Guemruekcueoglu+18 eq. (15) (validated in A2)."""
    if alpha <= 0:
        return 0.0, 0.0, float("inf")
    cs = math.sqrt(cs2_bps(alpha, c2))
    k = math.sqrt(alpha) * MPL_RED * (cs**1.5 if cs < 1 else cs**-0.5)
    return k, k * cs, cs
PROBES = {"Solar System (1/AU)": HBARC_GEV_M / AU, "LIGO (100 Hz)": HBAR_GEV_S * 2 * math.pi * 100.0,
          "torsion balance (52 um)": HBARC_GEV_M / 52e-6, "LHC (13 TeV)": 1.3e4}
AC_GRID = [AC_MIN, 1e-12, 1e-11, 1e-10, 1e-9, AC_MAX]
C2_GRID = sorted(set(CAPS + [C2_MIN, 0.02, C2_MAX]))
C0_SUN_MAX = 2.0                                          # the largest C-H inertia 2C/(1+C) can reach (C -> infinity)
rowsA4, worst = [], None
for acv in AC_GRID:
    for c2v in C2_GRID:
        ac_eff = 0.0 if MUTATE else acv
        # UV kinetic coefficient at the LARGEST Solar-System wavelength probed (1 AU): alpha_c + (C-H inertia <= 2 C(k))
        chi = C0_SUN_MAX * 10**max(-300.0, max(v_ for k_, v_ in logC_uv.items() if "1 AU" in k_))
        alpha_uv = ac_eff + chi
        k_sc, E_sc, cs = msc(alpha_uv, c2v)
        margin = min(k_sc / kp for kp in PROBES.values()) if k_sc > 0 else 0.0
        rowsA4.append({"alpha_c": acv, "c2": c2v, "alpha_uv": alpha_uv, "c_s": cs, "k_sc_GeV": k_sc, "E_sc_GeV": E_sc,
                       "margin_vs_LHC": k_sc / PROBES["LHC (13 TeV)"] if k_sc > 0 else 0.0})
        if worst is None or margin < worst[0]:
            worst = (margin, acv, c2v, k_sc, E_sc, cs)
for r in rowsA4:
    if r["alpha_c"] in (AC_MIN, 1e-11, AC_MAX):
        P(f"    alpha_c {r['alpha_c']:.2e}  c_2 {r['c2']:.2e}:  c_s = {r['c_s']:.3e} c   k_sc = {r['k_sc_GeV']:.3e} GeV   "
          f"E_sc = {r['E_sc_GeV']:.3e} GeV   k_sc/LHC = {r['margin_vs_LHC']:.2e}")
P("    probes (momentum, GeV): " + ", ".join(f"{k_}: {v_:.2e}" for k_, v_ in PROBES.items()))
lo = min(r["k_sc_GeV"] for r in rowsA4)
OUT["numbers"]["A4"] = {"probes_GeV": PROBES, "rows": rowsA4, "min_k_sc_GeV": lo,
                        "worst": {"margin": worst[0], "alpha_c": worst[1], "c2": worst[2], "k_sc": worst[3], "E_sc": worst[4], "c_s": worst[5]}}
check("A4 (G8) on the Solar-System background the khronon's strong-coupling momentum exceeds every probe by >= 1e3 across "
      "L340's alpha_c window and every c_2 value (Planck-era caps and L340's window); a0 does not enter (both footings)",
      f"lowest k_sc = {lo:.3e} GeV at alpha_c = {worst[1]:.2e}, c_2 = {worst[2]:.2e} (c_s = {worst[5]:.2e} c); "
      f"margin over the LHC = {worst[3] / PROBES['LHC (13 TeV)']:.2e}", lo >= 1e3 * max(PROBES.values()),
      "alpha_c is the load-bearing term: it is the only kinetic coefficient the UV khronon keeps (A3); the heat filter "
      "removes the MOND sector's inertia at AU scales")

# ============================================================================================ nu_mono (L340's construction, re-built)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e_=1e-6):
    return (h_rar(y * (1 + e_)) - h_rar(y * (1 - e_))) / (2 * y * e_)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def h_mono(y): return np.interp(np.log10(y), LYG, H_MONO)
def CT(y): return h_mono(y) / y                           # nu - 1
def CLf(y): return np.interp(np.log10(y), LYG, DH_MONO)   # d(y nu)/dy - 1 = h'(y)
_ys = sp.Symbol('y', positive=True)
_h = _ys / (sp.exp(sp.sqrt(_ys)) - 1)
_h1 = sp.lambdify(_ys, sp.diff(_h, _ys), "math"); _h2 = sp.lambdify(_ys, sp.diff(_h, _ys, 2), "math")
def dCL(y):
    """C_L'(y) = h''(y) on nu_mono: nu_RAR's h'' where h'_RAR binds, else d/dy[DELTA h_p/(y + y_p)]."""
    floor = DELTA * H_P / (y + Y_P)
    return _h2(y) if (y < 1e4 and _h1(y) >= floor) else -DELTA * H_P / (y + Y_P)**2
yp_ok = abs(Y_P - L340["numbers"]["A1"]["y_p"]) < 1e-6 and abs(H_P - L340["numbers"]["A1"]["h_p"]) < 1e-6
P(f"\n  nu_mono rebuilt: y_p = {Y_P:.6f}, h_p = {H_P:.6f} (L340: {L340['numbers']['A1']['y_p']:.6f}, "
  f"{L340['numbers']['A1']['h_p']:.6f}; match {yp_ok})")

# ============================================================================================ A5 the MOND regime
banner("A5  THE MOND REGIME (k < 1/xi): alpha_eff = alpha_c + 2C/(1+C), mode speed from L340's full block")
YS = [1e-3, 1e-2, 0.1, 1.0, 2.3, 10.0, 20.0, 1e3, 1e6]
rowsA5 = []
for yv in YS:
    for lab, Cv in (("T", float(CT(yv))), ("L", float(CLf(yv)))):
        for c2v in (min(C2_GRID), C2_MAX):
            acv = 0.0 if MUTATE else AC_MIN
            a_eff = acv + 2 * Cv / (1 + Cv)
            cs = math.sqrt(c2v / (Cv * (2 + 3 * c2v)))       # L340 T1 (full block, alpha_c << C)
            k = math.sqrt(a_eff) * MPL_RED * (cs**1.5 if cs < 1 else cs**-0.5)
            rowsA5.append({"y": yv, "dir": lab, "C": Cv, "c2": c2v, "alpha_eff": a_eff, "c_s": cs, "k_sc_GeV": k})
for r in rowsA5:
    if r["c2"] == min(C2_GRID):
        P(f"    y = {r['y']:8.3g} {r['dir']}:  C = {r['C']:.3e}  alpha_eff = {r['alpha_eff']:.3e}  c_s = {r['c_s']:.3e} c  "
          f"k_sc = {r['k_sc_GeV']:.2e} GeV")
loA5 = min(r["k_sc_GeV"] for r in rowsA5)
OUT["numbers"]["A5"] = {"rows": rowsA5, "min_k_sc_GeV": loA5}
check("A5 in the MOND regime the khronon's own (alpha-type and c_2) vertices stay weak: lowest k_sc over deep MOND ... "
      "nucleus, both directions, both c_2 edges, far above the LHC", f"lowest k_sc = {loA5:.2e} GeV", loA5 > 1e3 * PROBES["LHC (13 TeV)"],
      "order of magnitude only (metric mixing is O(1) here); the y = 2.3 rows are the Sun's filtered field", load_bearing=False)

# ============================================================================================ A6 the MOND vertex
banner("A6  THE MOND VERTEX: the cubic term of 2 alpha_M^2 q(|v + w|^2) along the field (sympy, generic kernel)")
s_ = sp.Symbol('s', positive=True); Y_ = sp.Symbol('Y', positive=True); wv = sp.Symbol('w', real=True)
# Along the field, |v + w|^2 = (s + w)^2 (units alpha_M = 1, v = s e_par, w = grad S dU / alpha_M).  With delta = 2 s w + w^2,
# q(s^2 + delta) = ... + q'' delta^2/2 + q''' delta^3/6: the w^3 terms of 2 q are 2 [2 q'' s + (4/3) q''' s^3] w^3.
# q'(Y) = C_T(sqrt Y)  =>  q''(s^2) = C_T'(s)/(2s),  q'''(s^2) = (s C_T''(s) - C_T'(s))/(4 s^3).
Tp, Tpp, T0s = sp.symbols('Tp Tpp T0')
q2e, q3e = Tp / (2 * s_), (s_ * Tpp - Tp) / (4 * s_**3)
cubic_coeff = sp.simplify(2 * (2 * q2e * s_ + sp.Rational(4, 3) * q3e * s_**3))
CLp_expr = 2 * Tp + s_ * Tpp                                     # d C_L/ds with C_L = C_T + s C_T'
id_ok = sp.simplify(cubic_coeff - sp.Rational(2, 3) * CLp_expr) == 0
# independent control on a concrete kernel: q(Y) = Int_0^Y exp(-t^{1/4}) dt, i.e. C_T(s) = exp(-sqrt s); differentiate
# 2 q((s + w)^2) three times in w directly and compare with (2/3) C_L'(s)
Yt = sp.Symbol('t', positive=True)
qtest = sp.integrate(sp.exp(-Yt**sp.Rational(1, 4)), (Yt, 0, Y_))
third_test = sp.simplify(sp.diff(2 * qtest.subs(Y_, (s_ + wv)**2), wv, 3).subs(wv, 0) / 6)
CTt = sp.exp(-sp.sqrt(s_))
target_test = sp.simplify(sp.Rational(2, 3) * sp.diff(CTt + s_ * sp.diff(CTt, s_), s_))
test_ok = sp.simplify(third_test - target_test) == 0
P(f"    cubic coefficient of (d_par S dU)^3 in 2 alpha_M^2 q: (1/alpha_M) x {sp.factor(cubic_coeff)}  = (2/3) C_L'(s)/alpha_M: {id_ok}")
P(f"    concrete-kernel control (C_T = e^(-sqrt s)): third derivative / 3! vs (2/3) C_L': {test_ok}")
def k_mond(yv, a0, c2v, acv):
    alM = a0 / C_SI**2 * HBARC_GEV_M                             # alpha_M = a0/c^2 in GeV
    Cl = float(CLf(yv)); dcl = abs(float(dCL(yv)))
    g = dcl / (3 * alM * (1 + Cl)**3)                             # |C_L'|/(3 alpha_M (1+C_L)^3), GeV^-1
    a_eff = acv + 2 * Cl / (1 + Cl)
    cs = math.sqrt(c2v / (Cl * (2 + 3 * c2v)))
    return math.sqrt(MPL_RED * a_eff**1.5 / (g * cs**0.5)), g, a_eff, cs      # N = 6, n_t = 3 class: k^2 = M a^{3/2}/(g c_s^{1/2})
rowsA6 = []
for foot, fd in FOOT.items():
    for yv in (0.01, 0.1, 0.5, 1.0, 2.0):
        kM, g, a_eff, cs = k_mond(yv, fd["a0"], min(C2_GRID), AC_MIN)
        rowsA6.append({"footing": foot, "y": yv, "k_M_GeV": kM, "length_m": HBARC_GEV_M / kM, "g_M": g, "alpha_eff": a_eff, "c_s": cs})
for r in rowsA6:
    P(f"    {r['footing']:9s} y = {r['y']:4.2f}:  k_M = {r['k_M_GeV']:.3e} GeV = {1e12 * r['k_M_GeV']:.3f} meV  "
      f"(length {1e3 * r['length_m']:.3f} mm)")
kM_min = min(r["k_M_GeV"] for r in rowsA6); kM_max = max(r["k_M_GeV"] for r in rowsA6)
OUT["numbers"]["A6"] = {"cubic_coeff": str(cubic_coeff), "identity": id_ok, "concrete_control": test_ok, "rows": rowsA6}
check("A6 the MOND cubic vertex along the field is (2/3) C_L'(y)/alpha_M (sympy, generic kernel + a concrete-kernel control); "
      "unfiltered it would be strongly coupled at k_M ~ meV (sub-mm), both footings",
      f"identity {id_ok}, control {test_ok}; k_M from {1e12 * kM_min:.2f} to {1e12 * kM_max:.2f} meV", id_ok and test_ok and 1e-14 < kM_min < 1e-10,
      "the MOND sector's own quantum cutoff, before the filter: an EFT valid above ~0.1 mm only")

# ============================================================================================ A7 dark-energy identity
banner("A7  THE DARK-ENERGY IDENTITY: sqrt(M_P a0/c^2) = (kappa^2/8 pi)^{1/4} rho^{1/4}")
kap, rho_, Mp_ = sp.symbols('kappa rho M_P', positive=True)
a0_nat = kap * sp.sqrt(rho_ / (8 * sp.pi)) / Mp_                # a0 = kappa sqrt(G rho) with G = 1/(8 pi M_P^2), c = hbar = 1
ident_DE = sp.simplify((Mp_ * a0_nat)**2 - kap**2 * rho_ / (8 * sp.pi)) == 0
rowsA7 = {}
for foot, fd in FOOT.items():
    rho_E_GeV4 = fd["rho"] * C_SI**2 / GEV_J * HBARC_GEV_M**3       # energy density in GeV^4
    E_rho = rho_E_GeV4**0.25
    alM = fd["a0"] / C_SI**2 * HBARC_GEV_M
    lhs = math.sqrt(MPL_RED * alM)
    kappa_foot = fd["a0"] / (C_SI * math.sqrt(G_SI * fd["rho"]))
    rhs = (kappa_foot**2 / (8 * math.pi))**0.25 * E_rho
    rowsA7[foot] = {"rho^(1/4) meV": 1e12 * E_rho, "sqrt(M_P a0) meV": 1e12 * lhs, "(kappa^2/8pi)^(1/4) rho^(1/4) meV": 1e12 * rhs,
                    "kappa": kappa_foot, "rel_diff": abs(lhs / rhs - 1), "dark_energy_length_mm": 1e3 * HBARC_GEV_M / E_rho}
    P(f"    {foot:9s} ({fd['what']}): rho^1/4 = {1e12 * E_rho:.3f} meV;  sqrt(M_P a0/c^2) = {1e12 * lhs:.4f} meV;  "
      f"(kappa^2/8pi)^1/4 rho^1/4 = {1e12 * rhs:.4f} meV (kappa = {kappa_foot:.4f});  |diff| {abs(lhs / rhs - 1):.1e}")
OUT["numbers"]["A7"] = {"symbolic": ident_DE, "footings": rowsA7}
check("A7 with a0 = kappa c sqrt(G rho) the MOND scale sqrt(M_P a0/c^2) equals (kappa^2/8 pi)^{1/4} rho^{1/4} exactly "
      "(sympy) and numerically on both footings: the MOND sector's cutoff is the dark-energy scale",
      f"symbolic {ident_DE}; " + "; ".join(f"{k_}: {v_['sqrt(M_P a0) meV']:.3f} meV vs rho^1/4 {v_['rho^(1/4) meV']:.3f} meV" for k_, v_ in rowsA7.items()),
      ident_DE and all(v_["rel_diff"] < 2e-3 for v_ in rowsA7.values()),
      "the same vacuum energy that sets a0 = kappa c sqrt(G rho_Lambda) (with M_P, the seesaw) sets the MOND sector's "
      "own quantum scale, 0.3 x rho_Lambda^{1/4}; note Berezhiani & Khoury 2015 remarked on the same meV coincidence")

# ============================================================================================ A8 the filter
banner("A8  THE FILTER: the largest the MOND coupling ever gets, (2/3e)/(xi k_M)^2")
kk2 = sp.Symbol('x', nonnegative=True)
fmax = sp.maximum(kk2 * sp.exp(-sp.Rational(3, 2) * kk2), kk2, sp.Interval(0, sp.oo))
fmax_ok = sp.simplify(fmax - sp.Rational(2, 3) / sp.E) == 0
rowsA8 = {}
for xi_pc in XI_FLOORS_PC:
    xi_GeVinv = xi_pc * PC / HBARC_GEV_M
    gmax = float(2 / (3 * math.e)) / (xi_GeVinv * kM_min)**2
    rowsA8[f"{xi_pc} pc"] = gmax
    P(f"    xi = {xi_pc} pc = {xi_GeVinv:.3e} GeV^-1:  max_k (k/k_M)^2 e^(-3 xi^2 k^2/2) = {gmax:.2e}  (k_M = {kM_min:.2e} GeV, the lowest)")
OUT["numbers"]["A8"] = {"max_x_exp": str(fmax), "gmax": rowsA8}
check("A8 with the committed Cassini floors every MOND vertex stays below 1e-30 of strong coupling at every momentum "
      "(max_x x e^{-3x/2} = 2/(3e), sympy)", f"max = 2/(3e): {fmax_ok}; g_max = " + ", ".join(f"{k_}: {v_:.1e}" for k_, v_ in rowsA8.items()),
      fmax_ok and max(rowsA8.values()) < 1e-30,
      "the heat filter is an exponential form factor on every MOND leg: the sub-mm cutoff of A6 is never reached")

# ============================================================================================ A9 reading
banner("A9  READING: the UV khronon speed and causality")
cs_rng = [math.sqrt(cs2_bps(a_, c_)) for a_ in (AC_MIN, AC_MAX) for c_ in (min(C2_GRID), C2_MAX)]
P(f"    UV khronon speed over the window (alpha_c x c_2 corners): {min(cs_rng):.2e} c .. {max(cs_rng):.2e} c")
P("    finite, hyperbolic: causal on the preferred foliation (L318 criterion B); superluminal w.r.t. the metric cone "
  "(criterion A, which L318 shows every scalar MOND realisation fails).  Superluminal modes cannot be Cherenkov-emitted; "
  "the subluminal band exists only at k < 1/xi (A5) and is not computed here.")
OUT["numbers"]["A9"] = {"cs_uv_min": min(cs_rng), "cs_uv_max": max(cs_rng)}
check("A9 (reading) the UV khronon is superluminal but finite over the whole window", f"{min(cs_rng):.2e} .. {max(cs_rng):.2e} c",
      min(cs_rng) > 1, load_bearing=False)

banner("VERDICT")
P(f"""  G8 -- the strong-coupling gate the recipe called "THE make-or-break" and nobody ran -- PASSES on C-H/K, by a wide
  margin, and for two reasons that are both load-bearing:
    (1) alpha_c > 0.  Above k ~ 1/xi the heat filter removes the C-H sector exactly (A3), so the khronon's only kinetic
        term is alpha_c a^2.  Its strong-coupling momentum, Guemruekcueoglu+18's sqrt(alpha) M c_s^(-1/2) (reproduced
        from the vertices, A2), is >= {lo:.1e} GeV over the whole window, >= {worst[0]:.1e} x the LHC (A4).  With
        alpha_c = 0 (MUTATE) the UV kinetic term is exponentially zero and the gate fails: the recipe's P7 is real, and
        alpha_c is what answers it.
    (2) the heat filter.  Unfiltered, the MOND sector would be strongly coupled at k_M ~ {1e12 * kM_min:.1f}-{1e12 * kM_max:.1f} meV (A6),
        which is the dark-energy scale by an exact identity (A7: sqrt(M_P a0/c^2) = (kappa^2/8pi)^(1/4) rho_Lambda^(1/4)).
        The filter's exponential form factor caps the MOND coupling at {max(rowsA8.values()):.0e} (A8).
  Not covered: loops and naturalness (G12), the UV completion, and nonlinear well-posedness (next lane).  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
