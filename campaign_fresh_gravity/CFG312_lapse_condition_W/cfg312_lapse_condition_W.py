#!/usr/bin/env python3
"""
CFG312 -- CFG294's lapse-kernel condition W <= 0 (F2a, velocities fixed) for realistic data.

SOURCE.  CFG294 S4c(Lag): on Bianchi-I flat leaves the F2a lapse second variation is (alpha_c - 1/2)|k|^2 + W,
W = -2 Lambda - 16 pi G V - 8 pi G rho_rest (2 - 3u^2)/(1 - u^2)^(3/2); a trivial kernel needs W <= 0, W != 0.

WHAT IS CHECKED (frozen in FROZEN_CRITERIA.md, commit 030106e11, before this script existed)
  C1  re-derivation of W from an in-lane minisuperspace Lagrangian; identification of V, rho_rest, u
  C2  barotropic perfect fluid (fixed-flux action): W = -2 Lambda - 16 pi G V - 8 pi G B/(1-u^2)^2,
      B = 2 rho - 3 rho u^2 + p u^2 - 2 p u^4 + (rho + p) c_s^2 u^4; pressure drops out at u = 0
  C3  sign theorems on the matter term: dust threshold 2/3; universal identity B = 2 rho (1-u^2)^2 + (rho+p) u^2
      (1 - (2 - c_s^2) u^2); exact thresholds for w = 0, 1/3, 1, -1
  C4  W <= 0 iff 2 Lambda + 16 pi G V + 8 pi G Sum B_i/(1-u_i^2)^2 >= 0; sufficient + strict conditions
  C5  scope of W (homogeneous class, C-H sector absent) -- disclosure
  C6  static inhomogeneous patch: W_loc = (K.K - lambda K^2) + (alpha - 1/2) Delta ln N; Hardy sufficient conditions;
      s-wave zero-energy node counts (cross-check), with a control that must bind
  Backgrounds: FLRW today, radiation era, Solar System, Milky Way at R_sun, a cluster, a neutron star, AGN/GRB jets.
  Controls: (i) FLRW + Lambda + comoving dust at the 18 record c_2; (ii) vacuum W = 0; (iii) MUTATE=1 (u^2 = 0.70 dust,
  u^2 = 0.75 radiation, V = -1.5 Lambda/(8 pi G)) must give W > 0 and fail (rc 1); (iv) a super-compact lapse bump
  must bind in the node-count test.

SCOPE.  This closes (or scopes) CFG294's condition C4 only.  CFG294's overall verdict stays CONDITIONAL (A1-A5
assumed).  Lean certifies only the polynomial inequalities, never analysis.  kappa = 1/2 is FITTED and plays no role.

Run from the repository root:
  python3 campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W.py
  MUTATE=1 python3 campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "a0kit"))
import a0kit                                                     # committed constants (read-only)

MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG, FROZEN = "CFG312", "cfg312_lapse_condition_W", "030106e11"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "frozen_criteria_commit": FROZEN, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (finding, not load-bearing)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


P(__doc__.split("SCOPE.")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the background set is replaced by dust at u^2 = 0.70 (Lambda = V = 0), radiation at u^2 = 0.75 and "
      "V = -1.5 Lambda/(8 pi G); each must give W > 0, so the background checks must FAIL (rc 1) ***")

# ================================================================================================ INPUTS
banner("INPUTS: committed files")
J294 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG294_chassis_nonlinear_wellposedness/"
                                         "cfg294_chassis_nonlinear_wellposedness_results.json")))
ACTION = open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md"),
              encoding="utf-8").read()
POINTS = [(sp.Rational(a), sp.Rational(c)) for a, c in J294["numbers"]["inputs"]["points"]]
W294 = J294["numbers"]["S4c_lag"]["W"]
C, G, MPC, MSUN, LAM = a0kit.C, a0kit.G, a0kit.MPC, a0kit.MSUN, a0kit.LAMBDA_PLANCK
H0 = 67.36e3 / MPC; OML = 0.6847; OMM = 1 - OML                # Planck-alone chain named in a0kit's docstring
RHOC = 3 * H0**2 / (8 * math.pi * G)
lam_ok = "Lambda>=0 is a fixed cosmological" in ACTION
# the action block of ACTION.md: R - 2 Lambda, the C-H terms, point masses, Maxwell; no scalar potential
act_block = ACTION[ACTION.index("I = c^3/(16 pi G)"):ACTION.index("Here F=dA")]
noV = ("V(" not in act_block) and ("phi" not in act_block)
P(f"    CFG294 committed W: {W294}")
P(f"    CFG294 record points: {len(POINTS)}; alpha_c in [{float(min(a for a, _ in POINTS)):.4e}, {float(max(a for a, _ in POINTS)):.3e}]")
P(f"    ACTION.md: 'Lambda>=0 is a fixed cosmological constant' {lam_ok}; no scalar potential in the action block {noV}")
P(f"    a0kit: Lambda = {LAM:.4e} m^-2; H0 = 67.36 km/s/Mpc, Omega_L = {OML}: Lambda from H0 = {3 * OML * H0**2 / C**2:.4e} m^-2; "
  f"rho_crit = {RHOC:.4e} kg/m^3")
OUT["numbers"]["inputs"] = {"W294": W294, "Lambda": LAM, "H0_SI": H0, "Omega_L": OML, "rho_crit": RHOC,
                            "Lambda_ge_0_in_ACTION": lam_ok, "no_scalar_potential_in_action": noV}

# ================================================================================================ C1
banner("C1  RE-DERIVATION OF W (in-lane minisuperspace; Bianchi-I flat leaves; velocities fixed)")
al, c2, Lam, Gs, mu, v, phid, V0, NX = sp.symbols("alpha c_2 Lambda G mu v phidot V0 N_x", real=True)
a1, a2, a3, ad1, ad2, ad3 = sp.symbols("a1 a2 a3 ad1 ad2 ad3", real=True)
N, N0, u = sp.symbols("N N0 u", positive=True)
lamK = 1 + c2
sg = a1 * a2 * a3
Kk = sum((ad / (a * N))**2 for a, ad in ((a1, ad1), (a2, ad2), (a3, ad3)))     # K_ij K^ij
Kt = sum(ad / (a * N) for a, ad in ((a1, ad1), (a2, ad2), (a3, ad3)))          # K
grav = sg * (N * (Kk - lamK * Kt**2) + al * N * (NX / (a1 * N))**2 - 2 * Lam * N) / (16 * sp.pi * Gs)
gauge = -sp.Rational(1, 2) * N * sg * (NX / (a1 * N))**2 / (16 * sp.pi * Gs)    # F2a: -1/2 N sqrt(gamma)|D ln N|^2
dust = -mu * sp.sqrt(N**2 - a1**2 * v**2)                                        # dust, coordinate speed v along x1
scal = sg * (phid**2 / (2 * N) - N * V0)                                         # homogeneous test scalar


def lapse_hessian(L):
    LNN = sp.diff(L, N, 2).subs(NX, 0).subs(N, N0)
    LXX = sp.diff(L, NX, 2).subs(NX, 0).subs(N, N0)
    return LNN, LXX


Ltot = grav + gauge + dust + scal
LNN, LXX = lapse_hessian(Ltot)
_, LXXp = lapse_hessian(grav + dust + scal)
bg = sp.diff(Ltot, N).subs(NX, 0).subs(N, N0)                                    # homogeneous background lapse equation
Lam_bg = sp.solve(sp.Eq(bg, 0), Lam)[0]
W_raw = sp.simplify(8 * sp.pi * Gs * N0 * LNN / sg)                               # before the background equation
W_formula = -2 * Lam - 16 * sp.pi * Gs * V0 - 8 * sp.pi * Gs * (mu / sg) * (2 - 3 * u**2) / (1 - u**2)**sp.Rational(3, 2)
d1 = sp.simplify((W_raw - W_formula.subs(Lam, Lam_bg)).subs(v, u * N0 / a1))
c1_W = d1 == 0
coef_f2a = sp.simplify(8 * sp.pi * Gs * N0 * LXX * a1**2 / sg)
coef_phys = sp.simplify(8 * sp.pi * Gs * N0 * LXXp * a1**2 / sg)
c1_coef = sp.simplify(coef_f2a - (al - sp.Rational(1, 2))) == 0 and sp.simplify(coef_phys - al) == 0
# W_raw itself: the kinetic invariant plus the scalar kinetic energy plus the dust u^2 term (no Lambda, no V)
W_raw_pred = (Kk - lamK * Kt**2).subs(N, N0) + 8 * sp.pi * Gs * phid**2 / N0**2 \
    + 8 * sp.pi * Gs * (mu / sg) * u**2 / (1 - u**2)**sp.Rational(3, 2)
c1_raw = sp.simplify((W_raw - W_raw_pred).subs(v, u * N0 / a1)) == 0
# CFG294's committed string is the same expression
syms294 = {"G": Gs, "V0": V0, "mu": mu, "u": u, "a1": a1, "a2": a2, "a3": a3, "Lambda": Lam}
c1_294 = sp.simplify(sp.sympify(W294, locals=syms294) - W_formula) == 0
# identification: mu/sqrt(gamma) is the rest mass per proper leaf volume; the fluid-frame density is rho_0 = rho_rest sqrt(1-u^2)
P(f"    W_raw = 8 pi G N0 L_NN / sqrt(gamma) = (K.K - lambda K^2) + 8 pi G phidot^2/N0^2 + 8 pi G rho_rest u^2/(1-u^2)^(3/2): {c1_raw}")
P(f"    with the background lapse equation: W = {W_formula}  : {c1_W};  = CFG294's committed string: {c1_294}")
P(f"    k^2 coefficients: F2a {coef_f2a}, physical {coef_phys}: {c1_coef}")
P("    V: potential of an OPTIONAL minimally coupled scalar (CFG294's probe); not in the chassis action -> chassis-native V = 0")
P("    rho_rest = mu/sqrt(gamma) = Gamma rho_0 (rest mass per proper khronon-leaf volume); u = a1 v/N0 = speed in the khronon frame (units of c)")
OUT["numbers"]["C1"] = {"W": str(W_formula), "W_raw": str(W_raw_pred), "coef_F2a": str(coef_f2a), "coef_phys": str(coef_phys)}
check("C1 W re-derived in-lane from the minisuperspace Lagrangian (anisotropic Bianchi I, dust, homogeneous scalar): "
      "W = -2 Lambda - 16 pi G V - 8 pi G rho_rest (2-3u^2)/(1-u^2)^(3/2) after the background lapse equation; k^2 coefficients "
      "alpha - 1/2 (F2a) and alpha (physical); identical to CFG294's committed expression",
      f"W {c1_W}; W_raw {c1_raw}; coefficients {c1_coef}; CFG294 string {c1_294}; ACTION.md Lambda >= 0 {lam_ok}, no V {noV}",
      c1_W and c1_raw and c1_coef and c1_294 and lam_ok and noV,
      "V is not a chassis term (ACTION.md has R - 2 Lambda, C-H fields, point masses, Maxwell); the chassis-native W has V = 0 "
      "and Lambda >= 0.  The scalar's kinetic energy cancels exactly between W_raw and the background equation")

# ================================================================================================ C2
banner("C2  BAROTROPIC PERFECT FLUID (fixed-flux action -N sqrt(gamma) rho(n), J^mu fixed): does pressure enter?")
J0, r0, r1, r2, rho, p, cs2 = sp.symbols("J0 r0 r1 r2 rho p c_s2", real=True)
n_of_N = J0 * sp.sqrt(N**2 - a1**2 * v**2) / (N * sg)                # n = |J|/sqrt(-g), zero shift
n0 = n_of_N.subs(N, N0)
rho_n = lambda n_: r0 + r1 * (n_ - n0) + r2 / 2 * (n_ - n0)**2        # exact to 2nd order at n0 (all W needs)
fluid = -N * sg * rho_n(n_of_N)
LtotF = grav + gauge + fluid
LNN_F, _ = lapse_hessian(LtotF)
bgF = sp.diff(LtotF, N).subs(NX, 0).subs(N, N0)
LamF = sp.solve(sp.Eq(bgF, 0), Lam)[0]
WF_raw = 8 * sp.pi * Gs * N0 * LNN_F / sg                             # unrewritten Hessian
# thermodynamics: p = n rho' - rho, c_s^2 = dp/drho = n rho''/rho'
sub_th = {r0: rho, r1: (rho + p) / n0, r2: cs2 * (rho + p) / n0**2}
X = sp.Symbol("X", nonnegative=True)                                  # X = u^2
Bpred = 2 * rho - 3 * rho * u**2 + p * u**2 - 2 * p * u**4 + (rho + p) * cs2 * u**4
WF_pred = -2 * Lam - 8 * sp.pi * Gs * Bpred / (1 - u**2)**2          # V = 0 here (no scalar in this Lagrangian)
dF = (WF_raw - WF_pred.subs(Lam, LamF)).subs(sub_th).subs(v, u * N0 / a1)
c2_form = sp.simplify(dF) == 0
# background equation: energy density in the khronon frame
E_bg = sp.simplify((-sp.diff(fluid, N).subs(N, N0) / sg).subs(sub_th).subs(v, u * N0 / a1))
c2_E = sp.simplify(E_bg - (rho + p * u**2) / (1 - u**2)) == 0
# dust limit: rho(n) = m n  -> p = 0, c_s = 0, rho_0 = rho_rest sqrt(1-u^2)
rr = sp.Symbol("rho_rest", positive=True)
c2_dust = sp.simplify(WF_pred.subs({p: 0, cs2: 0, rho: rr * sp.sqrt(1 - u**2)})
                      - W_formula.subs({V0: 0, mu: rr * sg})) == 0
c2_u0 = sp.simplify(WF_pred.subs(u, 0) - (-2 * Lam - 16 * sp.pi * Gs * rho)) == 0
P(f"    W_fluid (symbolic, background equation used) = -2 Lambda - 8 pi G B/(1-u^2)^2 with the predicted B: {c2_form}")
P(f"    background lapse equation sources E = (rho + p u^2)/(1 - u^2) (khronon-frame energy density): {c2_E}")
P(f"    dust limit reproduces C1 (rho_0 = rho_rest sqrt(1-u^2)): {c2_dust};  u = 0: W = -2 Lambda - 16 pi G rho, pressure absent: {c2_u0}")
OUT["numbers"]["C2"] = {"B": str(Bpred), "W_fluid": str(WF_pred)}
check("C2 perfect fluid: W = -2 Lambda - 16 pi G V - 8 pi G B/(1-u^2)^2, B = 2 rho - 3 rho u^2 + p u^2 - 2 p u^4 + (rho+p) c_s^2 u^4 "
      "(rho, p fluid-frame; c_s^2 = dp/drho); dust limit = C1; at u = 0 the pressure drops out exactly (W = -2 Lambda - 16 pi G rho)",
      f"form {c2_form}; E_bg {c2_E}; dust limit {c2_dust}; u = 0 {c2_u0}", c2_form and c2_E and c2_dust and c2_u0,
      "pressure enters W only through moving matter (terms O(p u^2)); a fluid at rest in the khronon frame contributes -16 pi G rho "
      "whatever its pressure, so a compact star needs no pressure term in the condition")

# ================================================================================================ C3
banner("C3  SIGN THEOREMS ON THE MATTER TERM (symbolic)")
w_, cs_ = sp.symbols("w c", real=True)
BX = sp.expand(Bpred.subs(u, sp.sqrt(X)))
# (a) dust
Bd = BX.subs({p: 0, cs2: 0}) / rho
a_sol_pos = sp.solve_univariate_inequality(sp.simplify(Bd) > 0, X, relational=False)
a_sol_zero = sp.solve(sp.Eq(Bd, 0), X)
c3a = (sp.simplify(Bd - (2 - 3 * X)) == 0) and a_sol_zero == [sp.Rational(2, 3)] and \
    a_sol_pos.intersect(sp.Interval(0, 1)) == sp.Interval.Ropen(0, sp.Rational(2, 3))
P(f"    (a) dust: B/rho = {sp.simplify(Bd)}; B > 0 on X in {a_sol_pos.intersect(sp.Interval(0, 1))}; B = 0 at X = {a_sol_zero}")
# (b) universal identity
ident = sp.expand(BX - (2 * rho * (1 - X)**2 + (rho + p) * X * (1 - (2 - cs2) * X)))
c3b_id = ident == 0
# consequence: rho >= 0, rho + p >= 0, c_s^2 >= 0, X <= 1/(2 - c_s^2) => B >= 2 rho (1-X)^2 >= 0; X <= 1/2 suffices for every c_s^2 >= 0
# random-sample sanity check of the inequality over the admissible box (the proof is the identity + signs)
rng = np.random.default_rng(31201)
Bf = sp.lambdify((rho, p, cs2, X), BX, "numpy")
viol = 0; mins = []
for _ in range(200000):
    rv = rng.uniform(0, 1); pv = rng.uniform(-rv, rv); cv = rng.uniform(0, 1); xv = rng.uniform(0, 1 / (2 - cv))
    val = Bf(rv, pv, cv, xv) - 2 * rv * (1 - xv)**2
    mins.append(val); viol += val < -1e-14
c3b = c3b_id and viol == 0
P(f"    (b) identity B = 2 rho (1-u^2)^2 + (rho+p) u^2 (1 - (2 - c_s^2) u^2): {c3b_id};  sampled violations of B >= 2 rho (1-u^2)^2 "
  f"on {{rho >= 0, |p| <= rho, 0 <= c_s^2 <= 1, u^2 <= 1/(2 - c_s^2)}}: {viol}/200000")
# (c) exact thresholds for p = w rho, c_s^2 = w
thr = {}
for lab, wv in (("dust w=0", 0), ("radiation w=1/3", sp.Rational(1, 3)), ("stiff w=1", 1), ("w=-1", -1)):
    Bw = sp.factor(sp.expand(BX.subs({p: wv * rho, cs2: wv}) / rho))
    roots = [r_ for r_ in sp.solve(sp.Eq(Bw, 0), X) if r_.is_real and 0 <= r_ < 1]
    thr[lab] = {"B_over_rho": str(Bw), "threshold_u2": [str(sp.nsimplify(r_)) for r_ in roots],
                "threshold_u": [float(sp.sqrt(r_)) for r_ in roots]}
    P(f"    (c) {lab}: B/rho = {Bw};  roots in [0,1): {[sp.nsimplify(r_) for r_ in roots]} -> u = {[round(float(sp.sqrt(r_)), 5) for r_ in roots]}")
rad_ok = thr["radiation w=1/3"]["threshold_u2"] and abs(float(sp.sympify(thr["radiation w=1/3"]["threshold_u2"][0])) - (math.sqrt(45) - 6)) < 1e-12
c3c = (thr["dust w=0"]["threshold_u2"] == ["2/3"] and rad_ok and thr["stiff w=1"]["threshold_u2"] == []
       and thr["w=-1"]["threshold_u2"] == []
       and sp.simplify(sp.sympify(thr["w=-1"]["B_over_rho"], locals={"X": X}) - 2 * (1 - X)**2) == 0)
OUT["numbers"]["C3"] = {"thresholds": thr, "identity": "B = 2 rho (1-u^2)^2 + (rho+p) u^2 (1 - (2 - c_s^2) u^2)",
                        "sample_min_excess": float(min(mins))}
check("C3a dust: for rho > 0 the matter term is negative iff u^2 < 2/3, zero at u^2 = 2/3, positive above",
      f"B/rho = 2 - 3u^2; B > 0 on [0, 2/3)", c3a)
check("C3b universal: B = 2 rho (1-u^2)^2 + (rho+p) u^2 (1 - (2 - c_s^2) u^2) identically; so rho >= 0, rho + p >= 0 (null/weak "
      "energy condition), c_s^2 >= 0 and u^2 <= 1/(2 - c_s^2) (in particular u^2 <= 1/2 for every fluid) give B >= 2 rho (1-u^2)^2, "
      "i.e. a matter term <= -16 pi G rho",
      f"identity {c3b_id}; sampled violations {viol}/200000 (min excess {min(mins):.2e})", c3b,
      "the bound needs only NEC + c_s^2 >= 0; DEC (|p| <= rho) is not used beyond rho + p >= 0")
check("C3c exact thresholds (p = w rho, c_s^2 = w): dust u^2 = 2/3 (u = 0.8165); radiation u^2 = sqrt(45) - 6 (u = 0.8416); stiff "
      "w = 1 none (B = 2 rho (1 - u^2)); w = -1 none (B = 2 rho (1-u^2)^2)",
      {k_: v_["threshold_u"] for k_, v_ in thr.items()}, c3c)
U_DUST = math.sqrt(2 / 3); U_RAD = math.sqrt(math.sqrt(45) - 6); U_UNIV = math.sqrt(0.5)

# ================================================================================================ C4
banner("C4  THE SIGN CONDITION FOR W (exact, sufficient, strict; chassis-native)")
Vs, Mb = sp.symbols("V M_B", real=True)        # M_B = Sum_i B_i/(1-u_i^2)^2
Wgen = -2 * Lam - 16 * sp.pi * Gs * Vs - 8 * sp.pi * Gs * Mb
exact = sp.simplify(Wgen + 2 * (Lam + 8 * sp.pi * Gs * Vs) + 8 * sp.pi * Gs * Mb) == 0      # W = -[2(Lambda + 8 pi G V) + 8 pi G M_B]
# sufficient: Lambda + 8 pi G V >= 0 and M_B >= 0 => W <= 0 ; strict if either > 0  (sampled + sign algebra)
ok_s = True
for _ in range(20000):
    A_ = rng.uniform(0, 2); M_ = rng.uniform(0, 2); g_ = rng.uniform(0.1, 1)
    Wv = -2 * A_ - 8 * math.pi * g_ * M_
    ok_s &= Wv <= 0 and (Wv < 0 if (A_ > 0 or M_ > 0) else True)
# V bound
Vb = sp.solve(sp.Eq(Wgen.subs(Mb, 0), 0), Vs)[0]
c4_vb = sp.simplify(Vb + Lam / (8 * sp.pi * Gs)) == 0
P(f"    W = -[2 (Lambda + 8 pi G V) + 8 pi G Sum_i B_i/(1-u_i^2)^2]: {exact};  W = 0 with no matter at V = {Vb}: {c4_vb}")
P("    sufficient: V >= -Lambda/(8 pi G) and every component with rho_i >= 0, rho_i + p_i >= 0, c_s^2 >= 0, u_i below threshold;")
P("    strict:     additionally Lambda + 8 pi G V > 0, or some rho_i > 0 strictly below threshold;")
P("    chassis-native (V = 0, Lambda > 0 observed): W < 0 for every sub-threshold matter content, including vacuum + Lambda.")
check("C4 W <= 0 iff 2(Lambda + 8 pi G V) + 8 pi G Sum B_i/(1-u_i^2)^2 >= 0; sufficient: V >= -Lambda/(8 pi G) and all components "
      "sub-threshold with rho >= 0; strict W < 0 if Lambda + 8 pi G V > 0 or some rho_i > 0 sub-threshold; chassis-native "
      "(V = 0, Lambda > 0): W < 0 strictly",
      f"exact form {exact}; sign algebra on 20000 samples {ok_s}; V bound -Lambda/(8 pi G) {c4_vb}", exact and ok_s and c4_vb,
      "Lean (cfg312_lapse_condition_W.lean) certifies the polynomial core of C3a, C3b, C3c(radiation) and C4")

# ================================================================================================ C5
banner("C5  SCOPE OF W (disclosure)")
check("C5 (scope) W is derived on homogeneous Bianchi-I flat-leaf backgrounds with the C-H (MOND) sector absent, exactly as in "
      "CFG294; on a bound (inhomogeneous, static) system the background equation that turned W_raw into W is not the "
      "homogeneous one, so the pointwise W of the backgrounds below is an INDICATOR; the static case is treated properly in C6",
      "W_raw = (K.K - lambda K^2) + 8 pi G phidot^2/N^2 + 8 pi G rho_rest u^2/(1-u^2)^(3/2) is the unrewritten Hessian (C1)",
      c1_raw, "the C-H sector's zero-order contribution to the lapse potential is not computed here (CFG294 K4b: it enters at "
      "lower order on the U-shell)", load_bearing=False)

# ================================================================================================ C6
banner("C6  STATIC INHOMOGENEOUS PATCH: the lapse potential with N = N(x), matter at rest, homogeneous expansion term")
x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
cc, At, Lin = sp.symbols("c A_t L_lin", real=True)          # c = alpha - 1/2; A_t = N^2 (K.K - lambda K^2) (velocity part); Lin: linear-in-N terms
nn, n1, n2, n3 = sp.symbols("n n1 n2 n3", real=True)
dens = At / nn + cc * (n1**2 + n2**2 + n3**2) / nn + Lin * nn   # (16 pi G) x Lagrangian density on a flat static leaf
Nf = sp.Function("Nf")(x1, x2, x3)
rep = {nn: Nf, n1: sp.diff(Nf, x1), n2: sp.diff(Nf, x2), n3: sp.diff(Nf, x3)}
Lnn = sp.diff(dens, nn, 2).subs(rep)
pot = Lnn - sum(sp.diff(sp.diff(dens, nn, ni).subs(rep), xi) for ni, xi in ((n1, x1), (n2, x2), (n3, x3)))
lnN = sp.log(Nf)
lap_ln = sum(sp.diff(lnN, xi, 2) for xi in (x1, x2, x3))
pot_pred = (2 / Nf) * (At / Nf**2 + cc * lap_ln)
c6_pot = sp.simplify(pot - pot_pred) == 0
kin = sp.diff(dens, n1, 2).subs(rep)
c6_kin = sp.simplify(kin - 2 * cc / Nf) == 0
P(f"    second variation: potential = (2/N)[A_t/N^2 + (alpha - 1/2) Delta ln N]: {c6_pot};  gradient coefficient 2(alpha - 1/2)/N: {c6_kin}")
P("    in CFG294's normalisation: W_loc = (K.K - lambda K^2) + (alpha - 1/2) Delta ln N (+ 8 pi G rho_rest u^2/(1-u^2)^(3/2) if moving)")
P("    weak field: Delta ln N = Delta N/N - |D ln N|^2 with Delta N/N = 4 pi G (rho + 3p)/c^2 - Lambda  =>  in vacuum W_loc > 0 where")
P("    (1/2 - alpha)|D ln N|^2 exceeds (9 lambda - 3) H^2/c^2: positive pointwise, so CFG294's pointwise criterion does NOT apply there.")
P("    Hardy (R^3, centre x0): Int |grad f|^2 >= 1/4 Int f^2/|x - x0|^2.  Since -Delta + Delta ln N >= -Delta - |D ln N|^2 wherever")
P("    Delta N >= 0, the F2a operator (1/2 - alpha)(-Delta + Delta ln N) + (9 lambda - 3) H^2 is positive if |x - x0| |D ln N| <= 1/2,")
P("    i.e. G M(r)/(r c^2) <= 1/2 in the weak field (an isolated body).")
check("C6a static flat-leaf patch: the velocity-fixed lapse second variation has gradient coefficient (alpha - 1/2)/N (x2) and "
      "potential (2/N)[(K.K - lambda K^2) + (alpha - 1/2) Delta ln N]; W_loc differs from CFG294's W (no -16 pi G rho; a "
      "+(1/2 - alpha)|D ln N|^2 piece in vacuum)", f"potential {c6_pot}; gradient coefficient {c6_kin}", c6_pot and c6_kin)


def static_profile(compact, rho_shape="uniform", npts=4000):
    """Weak-field lapse of a uniform sphere, radius 1, from Delta N = k^2 N inside (k^2 = 4 pi G rho R^2/c^2 = 3 compact),
    N harmonic outside; returns r grid, l' = N'/N and V(r) = Delta ln N = k^2 [r<1] - l'^2."""
    k2 = 3 * compact
    def rhs(r, y):
        Nn, dN = y
        src = k2 * Nn if r < 1 else 0.0
        return [dN, src - 2 * dN / r]
    r0_ = 1e-6
    sol = solve_ivp(rhs, (r0_, 200.0), [1.0, k2 * r0_ / 3], dense_output=True, rtol=1e-11, atol=1e-14, max_step=0.01)
    rr_ = np.concatenate([np.linspace(r0_, 1, npts), np.geomspace(1, 200, npts)[1:]])
    Nn, dN = sol.sol(rr_)
    lp = dN / Nn
    V = np.where(rr_ < 1, k2, 0.0) - lp**2
    return rr_, lp, V


def swave_nodes(rr_, V, rmax=200.0):
    """zero-energy s-wave solution of -u'' + V u = 0, u(0) = 0, u'(0) = 1; number of sign changes = number of bound states."""
    from scipy.interpolate import interp1d
    Vi = interp1d(rr_, V, kind="linear", fill_value=(V[0], 0.0), bounds_error=False)
    sol = solve_ivp(lambda r, y: [y[1], Vi(r) * y[0]], (rr_[0], rmax), [rr_[0], 1.0], rtol=1e-10, atol=1e-14,
                    max_step=0.01, dense_output=True)
    rg = np.linspace(rr_[0], rmax, 200001)
    ug = sol.sol(rg)[0]
    return int(np.sum(np.sign(ug[1:]) != np.sign(ug[:-1])))


GMSUN = G * MSUN
cases6 = {"Sun (uniform, G M/(R c^2) = 2.1e-6)": GMSUN / (6.957e8 * C**2),
          "neutron star (G M/(R c^2) = 0.2, weak-field model)": 0.2}
rows6 = {}
for lab, comp in cases6.items():
    rr_, lp, V = static_profile(comp)
    hardy = float(np.max(rr_ * np.abs(lp)))
    nodes = swave_nodes(rr_, V)
    rows6[lab] = {"compactness": comp, "max_r_dlnN": hardy, "hardy_ok": hardy <= 0.5, "swave_bound_states": nodes}
    P(f"    {lab}: max r|D ln N| = {hardy:.4e} (<= 1/2: {hardy <= 0.5}); s-wave bound states of -Delta + Delta ln N: {nodes}")
# flat rotation curve / isothermal cluster: r |D ln N| = r g/c^2 = v^2/c^2 (analytic, no ODE)
for lab, vv in (("Milky Way-like galaxy, v_c = 230 km/s (flat curve): r|D ln N| = v_c^2/c^2", 230e3),
                ("cluster, 2 sigma^2 with sigma = 1000 km/s: r|D ln N| = 2 sigma^2/c^2", math.sqrt(2) * 1000e3)):
    hv = (vv / C)**2
    rows6[lab] = {"compactness": hv, "max_r_dlnN": hv, "hardy_ok": hv <= 0.5, "swave_bound_states": 0, "analytic": True}
    P(f"    {lab} = {hv:.3e} (<= 1/2: {hv <= 0.5})")
# control (iv): super-compact bump (unphysical) must bind; ln N = A exp(-r^2), V = Delta ln N exactly
rb = np.concatenate([np.linspace(1e-6, 1, 4000), np.geomspace(1, 200, 4000)[1:]])
A_b = 6.0
lnb = A_b * np.exp(-rb**2)
Vb_ = A_b * np.exp(-rb**2) * (4 * rb**2 - 6)                 # Laplacian of A e^{-r^2} in 3-D
nodes_b = swave_nodes(rb, Vb_)
hardy_b = float(np.max(rb * 2 * A_b * rb * np.exp(-rb**2)))
P(f"    control (iv): ln N = {A_b} exp(-r^2) (super-compact, unphysical): max r|D ln N| = {hardy_b:.3f}; s-wave bound states: {nodes_b}")
# pointwise W_loc in Solar-System vacuum at 1 AU vs the cosmological term
AU = 1.495978707e11
g_1au = GMSUN / AU**2
cos_term = 2 * LAM + 16 * math.pi * G * OMM * RHOC / C**2                # (9 lambda - 3) H^2/c^2 via the Friedmann equation (lambda ~ 1)
wloc_1au = -cos_term + 0.5 * (g_1au / C**2)**2
g_cross = C**2 * math.sqrt(cos_term / 0.5)
P(f"    pointwise W_loc at 1 AU (vacuum): -{cos_term:.3e} + (1/2)(g/c^2)^2 = {wloc_1au:+.3e} m^-2 (positive); crossover g = "
  f"c^2 sqrt(2 x cos) = {g_cross:.3e} m/s^2")
OUT["numbers"]["C6"] = {"static": rows6, "control_iv": {"A": A_b, "max_r_dlnN": hardy_b, "bound_states": nodes_b},
                        "W_loc_1AU": wloc_1au, "g_crossover": g_cross}
c6b = all(r_["hardy_ok"] and r_["swave_bound_states"] == 0 for r_ in rows6.values())
check("C6b Hardy sufficient condition for isolated static bodies: max r|D ln N| <= 1/2 for the Sun (2.1e-6), a weak-field "
      "neutron-star model (0.2), a Milky Way-like galaxy (5.9e-7) and a cluster (2.2e-5); the s-wave zero-energy solution has no node (no bound state), consistent",
      {k_: (round(v_["max_r_dlnN"], 8), v_["swave_bound_states"]) for k_, v_ in rows6.items()}, c6b,
      "galaxy and cluster rows are analytic (r g/c^2 = v^2/c^2), no node count.  The pointwise W_loc is positive in the Solar-System vacuum (+(1/2)(g/c^2)^2 beats the cosmological term for g > "
      f"{g_cross:.1e} m/s^2) -- CFG294's pointwise W <= 0 is the wrong test there; Hardy covers it.  NS: flat-leaf, weak-field "
      "model only; the strong-field interior is outside this derivation")
check("C6 control (iv): a super-compact (unphysical) lapse bump violates Hardy and the node-count test finds a bound state",
      f"max r|D ln N| = {hardy_b:.3f} > 1/2; bound states {nodes_b}", hardy_b > 0.5 and nodes_b >= 1)

# ================================================================================================ BACKGROUNDS
banner("BACKGROUNDS: W in m^-2 (geometric units: 8 pi G rho/c^2), chassis-native V = 0 unless stated")
PC = MPC / 1e6
MSPC3 = MSUN / PC**3                                        # 1 Msun/pc^3 in kg/m^3
MP = 1.67262192e-27; KB = 1.380649e-23; KMS = 1e3


def W_of(Lam_, V_, comps):
    """comps: list of (rho [kg/m^3], p [Pa], c_s^2 [c^2 units], u [c units]) in the fluid frame. V_ in J/m^3."""
    W = -2 * Lam_ - 16 * math.pi * G * V_ / C**4
    terms = []
    for (rho_, p_, cs_, u_) in comps:
        pr = p_ / C**2                                       # pressure as a mass density
        X_ = u_**2
        B_ = 2 * rho_ - 3 * rho_ * X_ + pr * X_ - 2 * pr * X_**2 + (rho_ + pr) * cs_ * X_**2
        t_ = -8 * math.pi * G * B_ / (C**2 * (1 - X_)**2)
        terms.append(t_); W += t_
    return W, terms


ORAD = 9.15e-5                                              # Omega_r (photons + 3 nu), reference value, not fetched
BG = []
if not MUTATE:
    BG += [
        ("FLRW today: Lambda + matter, comoving", LAM, 0.0, [(OMM * RHOC, 0.0, 0.0, 0.0)], "homogeneous"),
        ("FLRW today, matter with 1000 km/s peculiar speed", LAM, 0.0, [(OMM * RHOC, 0.0, 0.0, 1000 * KMS / C)], "homogeneous"),
        ("radiation era z = 1e4: radiation + matter, comoving", LAM, 0.0,
         [(ORAD * RHOC * 1e16, ORAD * RHOC * 1e16 * C**2 / 3, 1 / 3, 0.0), (OMM * RHOC * 1e12, 0.0, 0.0, 0.0)], "homogeneous"),
        ("radiation era z = 1e9: radiation (u = 1e-4) + matter", LAM, 0.0,
         [(ORAD * RHOC * 1e36, ORAD * RHOC * 1e36 * C**2 / 3, 1 / 3, 1e-4), (OMM * RHOC * 1e27, 0.0, 0.0, 1e-4)], "homogeneous"),
        ("radiation fluid at u = 0.80 c (below its 0.8416 threshold), z = 1e4", LAM, 0.0,
         [(ORAD * RHOC * 1e16, ORAD * RHOC * 1e16 * C**2 / 3, 1 / 3, 0.80)], "homogeneous"),
        ("Solar interior: mean density 1408 kg/m^3, u = 370 km/s", LAM, 0.0, [(1408.0, 0.0, 0.0, 370 * KMS / C)], "indicator"),
        ("Solar centre: 1.5e5 kg/m^3, p = 2.5e16 Pa, c_s^2 ~ 5e-6", LAM, 0.0, [(1.5e5, 2.5e16, 5e-6, 370 * KMS / C)], "indicator"),
        ("Earth: 5514 kg/m^3, u = 400 km/s", LAM, 0.0, [(5514.0, 0.0, 0.0, 400 * KMS / C)], "indicator"),
        ("solar wind at 1 AU: n = 5 cm^-3, u = 770 km/s", LAM, 0.0, [(5e6 * MP, 5e6 * 2 * KB * 1e5, 1e-8, 770 * KMS / C)], "indicator"),
        ("Milky Way at R_sun: stars 0.043 + gas 0.041 + cold component 0.010 Msun/pc^3, u = 1000 km/s", LAM, 0.0,
         [(0.043 * MSPC3, 0.0, 0.0, 1000 * KMS / C), (0.041 * MSPC3, 0.041 * MSPC3 * KB * 1e4 / (1.3 * MP), 1e-11, 1000 * KMS / C),
          (0.010 * MSPC3, 0.0, 0.0, 1000 * KMS / C)], "indicator"),
        ("cluster core: ICM 2e-23 kg/m^3 at 1e8 K, galaxies + cold component 1e-22, u = 2500 km/s", LAM, 0.0,
         [(2e-23, 2e-23 * KB * 1e8 / (0.6 * MP), 5 / 3 * KB * 1e8 / (0.6 * MP * C**2), 2500 * KMS / C),
          (1e-22, 0.0, 0.0, 2500 * KMS / C)], "indicator"),
        ("neutron-star centre: 1e18 kg/m^3, p/(rho c^2) = 0.4, c_s^2 = 0.6, u = 1000 km/s (kick)", LAM, 0.0,
         [(1e18, 0.4 * 1e18 * C**2, 0.6, 1000 * KMS / C)], "indicator"),
        ("neutron star, worst case: centre values with u = 0.18 c (fastest ms-pulsar surface spin)", LAM, 0.0,
         [(1e18, 0.4 * 1e18 * C**2, 0.6, 0.18)], "indicator"),
        ("neutron star, maximal stiffness p = rho c^2, c_s^2 = 1, u = 0.18 c", LAM, 0.0, [(1e18, 1e18 * C**2, 1.0, 0.18)], "indicator"),
        ("added scalar with V = -0.5 Lambda c^4/(8 pi G) (above the bound), no matter", LAM, -0.5 * LAM * C**4 / (8 * math.pi * G), [],
         "homogeneous"),
    ]
else:
    BG += [
        ("MUTATE dust u^2 = 0.70 > 2/3, Lambda = V = 0", 0.0, 0.0, [(1.0, 0.0, 0.0, math.sqrt(0.70))], "homogeneous"),
        ("MUTATE radiation u^2 = 0.75 > 0.7082, Lambda = V = 0", 0.0, 0.0, [(1.0, C**2 / 3, 1 / 3, math.sqrt(0.75))], "homogeneous"),
        ("MUTATE V = -1.5 Lambda c^4/(8 pi G), no matter", LAM, -1.5 * LAM * C**4 / (8 * math.pi * G), [], "homogeneous"),
    ]
bg_rows = []
for lab, L_, V_, comps, kind in BG:
    W, terms = W_of(L_, V_, comps)
    umax = max([c_[3] for c_ in comps], default=0.0)
    ratio = (W / (-2 * L_)) if L_ > 0 else float("nan")
    bg_rows.append({"background": lab, "kind": kind, "W_m^-2": W, "matter_terms": terms, "u_max": umax,
                    "W_over_minus2Lambda": ratio, "W_neg": W < 0})
    flag = "" if W < 0 else "   <-- W > 0 FLAGGED"
    P(f"    {lab}\n        W = {W:+.4e} m^-2  (W/(-2 Lambda) = {ratio:.4e}); u_max = {umax:.3e} c; [{kind}]{flag}")
OUT["numbers"]["backgrounds"] = bg_rows
bg_ok = all(r_["W_neg"] for r_ in bg_rows)
check("B1 every background (homogeneous class exactly; bound systems as pointwise indicators) has W < 0 with the chassis-native "
      "V = 0 (and with an added scalar above V = -Lambda/(8 pi G))" if not MUTATE else
      "B1 (MUTATE) the mutated backgrounds must give W < 0 -- they must NOT (u^2 > threshold or V below the bound)",
      f"{sum(r_['W_neg'] for r_ in bg_rows)}/{len(bg_rows)} with W < 0", bg_ok,
      "flagged rows are W > 0" if MUTATE else "pressure enters only through the O(p u^2) terms; at the NS centre with u = 0.18 c the "
      "matter term stays negative")
# NS: pressure contribution at u = 0.18 c relative to the u = 0 value
ns_u0 = W_of(0, 0, [(1e18, 0.4e18 * C**2, 0.6, 0.0)])[1][0]
ns_u = W_of(0, 0, [(1e18, 0.4e18 * C**2, 0.6, 0.18)])[1][0]
ns_nop = W_of(0, 0, [(1e18, 0.0, 0.0, 0.18)])[1][0]
OUT["numbers"]["NS_pressure"] = {"term_u0": ns_u0, "term_u018": ns_u, "term_u018_nopressure": ns_nop}
P(f"    NS matter term: u = 0 {ns_u0:+.4e}; u = 0.18 c with p = 0.4 rho c^2 {ns_u:+.4e}; same without pressure {ns_nop:+.4e} m^-2")

# speeds
VMAX_OBS = 1000 * KMS / C
spd = {"dust": U_DUST, "radiation": U_RAD, "universal (any fluid, NEC, c_s^2 >= 0)": U_UNIV}
P(f"    max |u|: dust {U_DUST:.5f} c = {U_DUST * C / 1e3:.0f} km/s; radiation {U_RAD:.5f} c = {U_RAD * C / 1e3:.0f} km/s; universal "
  f"{U_UNIV:.5f} c = {U_UNIV * C / 1e3:.0f} km/s;  peculiar velocities <= 1e3 km/s = {VMAX_OBS:.3e} c (u^2 = {VMAX_OBS**2:.2e})")
OUT["numbers"]["speeds"] = {"u_max": spd, "u_obs_peculiar": VMAX_OBS, "margin_universal": U_UNIV / VMAX_OBS}
sp_ok = VMAX_OBS < U_UNIV and 0.18 < U_UNIV
check("B2 the maximum allowed |u| relative to the khronon frame (dust 0.8165 c, radiation 0.8416 c, any fluid 0.7071 c) exceeds real "
      "peculiar velocities (<= 1e3 km/s = 3.3e-3 c) by x212 and the fastest non-jet bulk motion (ms-pulsar spin, 0.18 c)",
      f"universal/peculiar = {U_UNIV / VMAX_OBS:.0f}", sp_ok)

# ================================================================================================ JETS (sub-class)
banner("JETS: ultra-relativistic outflows exceed the threshold; Hardy about the engine (C6(ii) pointwise form)")
# steady conical outflow of isotropic-equivalent power L at Lorentz factor Gamma, cold (dust) or hot (radiation-like):
# khronon-frame energy density E = L/(4 pi r^2 u c); the matter term t(r) ~ 1/r^2, so W r^2 is r-independent.
# Hardy about the engine: (1/2 - alpha)(-Delta) - W_+ >= 0 if W_+(r) r^2 <= (1/2 - alpha)/4  (alpha_c <= 3.2e-9 -> 1/8).
def jet_Wr2(Liso, Gam, hot):
    u_ = math.sqrt(1 - 1 / Gam**2)
    r_ = 1.0
    E = Liso / (4 * math.pi * r_**2 * u_ * C)                  # J/m^3
    w = 1 / 3 if hot else 0.0
    rho0 = E / C**2 / ((1 + w * u_**2) / (1 - u_**2))          # fluid-frame density from E = (rho + p u^2)/(1-u^2)
    W, t = W_of(0.0, 0.0, [(rho0, w * rho0 * C**2, w, u_)])
    return W * r_**2
LIM = (0.5 - 3.2e-9) / 4
jets = [("M87 kpc jet: L = 1e37 W, Gamma = 10", 1e37, 10), ("powerful blazar: L = 1e40 W, Gamma = 50", 1e40, 50),
        ("typical GRB: L_iso = 1e45 W, Gamma = 300", 1e45, 300), ("bright GRB: L_iso = 1e46 W, Gamma = 300", 1e46, 300),
        ("extreme GRB: L_iso = 1e47 W, Gamma = 1000", 1e47, 1000)]
jet_rows = []
for lab, L_, Gm in jets:
    cold = jet_Wr2(L_, Gm, False); hot = jet_Wr2(L_, Gm, True)
    worst = max(cold, hot)
    jet_rows.append({"jet": lab, "W_r2_cold": cold, "W_r2_hot": hot, "W_positive": worst > 0, "hardy_ok": worst <= LIM})
    P(f"    {lab}: W r^2 cold {cold:+.3e}, hot {hot:+.3e}  (W > 0: {worst > 0}; Hardy <= {LIM:.4f}: {worst <= LIM})")
Lcrit = LIM / jet_Wr2(1.0, 1000, True) if jet_Wr2(1.0, 1000, True) > 0 else float("nan")
LG2 = {Gm: LIM / jet_Wr2(1.0, Gm, True) for Gm in (10, 100, 300, 1000)}
P(f"    Hardy-covered iff L_iso <~ {', '.join(f'{v_:.2e} W at Gamma {k_}' for k_, v_ in LG2.items())}  (L Gamma^2 ~ c^5/(16 G) = {C**5 / (16 * G):.2e} W)")
OUT["numbers"]["jets"] = {"rows": jet_rows, "hardy_limit": LIM, "L_crit_by_Gamma": LG2, "c5_over_16G": C**5 / (16 * G)}
jets_pos = all(r_["W_positive"] for r_ in jet_rows)
check("J1 (finding) ultra-relativistic jets exceed the threshold: the pointwise W is POSITIVE in every jet tested (AGN Gamma 10-50, "
      "GRB Gamma 300-1000) -- the exact sub-class where CFG294's pointwise condition fails",
      f"{sum(r_['W_positive'] for r_ in jet_rows)}/{len(jet_rows)} positive", jets_pos, load_bearing=False)
cov = [r_["hardy_ok"] for r_ in jet_rows]
check("J2 (finding) Hardy about the engine covers AGN jets and typical/bright GRBs (W r^2 <= (1/2 - alpha)/4) but NOT the most "
      "extreme GRBs (L_iso ~ 1e47 W at Gamma ~ 1000): there invertibility of the F2a lapse operator is not proved",
      f"covered {sum(cov)}/{len(cov)}: " + ", ".join(f"{r_['jet'].split(':')[0]} {r_['hardy_ok']}" for r_ in jet_rows),
      cov[:4] == [True] * 4 and not cov[4], load_bearing=False,
      reading="Hardy is sufficient, not necessary; a jet is also far outside the homogeneous flat-leaf class of W")

# ================================================================================================ CONTROLS
banner("CONTROLS (i) FLRW + Lambda + comoving dust at the 18 record c_2; (ii) vacuum")
ctl = []
for (a_, c_) in POINTS:
    lv = 1 + c_
    # 8 pi G = 1, Lambda = rho = 1: (9 lambda - 3) H^2 = 2 Lambda + 16 pi G rho = 4 ; K.K - lambda K^2 = 3H^2 - 9 lambda H^2
    H2 = sp.Rational(4) / (9 * lv - 3)
    Wraw = 3 * H2 - 9 * lv * H2
    Wf = W_formula.subs({Lam: 1, V0: 0, Gs: 1 / (8 * sp.pi), mu: sg, u: 0})
    ctl.append((float(Wraw), float(Wf)))
ctl_ok = all(abs(x_ + 4) < 1e-12 and abs(y_ + 4) < 1e-12 for x_, y_ in ctl)
vac = sp.simplify(W_formula.subs({Lam: 0, V0: 0, mu: 0}))
P(f"    (i) W_raw = K.K - lambda K^2 and W formula, both = -(2 Lambda + 16 pi G rho) = -4: {ctl_ok} at {len(ctl)} points")
P(f"    (ii) vacuum W = {vac}")
check("CTL(i) FLRW + Lambda + comoving dust reproduces CFG294: W = -(2 Lambda + 16 pi G rho) < 0 at all 18 record c_2, from the raw "
      "Hessian and from the formula", f"{len(ctl)} points, all -4 (units 8 pi G = Lambda = rho = 1): {ctl_ok}", ctl_ok)
check("CTL(ii) vacuum (Lambda = rho = V = 0) gives W = 0 exactly (the relabelling mode)", f"W = {vac}", vac == 0)

# ================================================================================================ VERDICT
banner("VERDICT")
core = [n_ for n_, ok, lb in CH if lb]
n_ok = sum(ok for _, ok, _ in CH)
lb_ok = all(ok for _, ok, lb in CH if lb)
if MUTATE:
    verdict = "MUTATE: W > 0 flagged on the mutated data (expected FAIL)" if not bg_ok else "MUTATE DID NOT FLAG (control failed)"
else:
    verdict = ("PASS-WITH-EXCEPTIONS (scoped)" if lb_ok else "FAIL")
OUT["verdict"] = verdict
OUT["summary"] = {
    "proven": ["W re-derived (C1); V is not a chassis term (V = 0 native), Lambda >= 0 (ACTION.md)",
               "perfect fluid: W = -2 Lambda - 16 pi G V - 8 pi G B/(1-u^2)^2; pressure drops out at u = 0 (C2)",
               "B = 2 rho (1-u^2)^2 + (rho+p) u^2 (1 - (2 - c_s^2) u^2): NEC + c_s^2 >= 0 + u^2 <= 1/(2 - c_s^2) => matter term <= -16 pi G rho (C3b)",
               "thresholds: dust u < 0.8165 c, radiation u < 0.8416 c, stiff and w = -1 none (C3)",
               "W <= 0 iff 2(Lambda + 8 pi G V) + 8 pi G Sum B_i/(1-u_i^2)^2 >= 0; strict W < 0 for chassis-native data (C4)"],
    "exceptions": ["ultra-relativistic flows (u above threshold): W > 0 pointwise; Hardy covers AGN and typical GRB jets, not L_iso Gamma^2 >~ 1e51 W",
                   "an added scalar with V < -Lambda/(8 pi G) (not a chassis field)",
                   "static bound systems: CFG294's pointwise W is the wrong test (W_loc > 0 in vacuum); covered by Hardy for G M/(r c^2) <= 1/2 (weak field)"],
    "not_covered": ["C-H sector's zero-order lapse potential", "strong-field interiors (flat-leaf derivation)", "CFG294 A1-A5 remain assumed"]}
P(f"    verdict: {verdict}")
P(f"    load-bearing checks: {sum(ok for _, ok, lb in CH if lb)}/{len(core)}")
P(f"\n{n_ok}/{len(CH)} checks pass")
OUT["n_pass"], OUT["n_checks"] = n_ok, len(CH)
fn = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, fn), "w"), indent=1, default=str)
sys.exit(0 if (lb_ok and not MUTATE) else 1)
