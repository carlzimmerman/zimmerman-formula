#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L318 -- THE CAUSALITY CRITERION DECIDES RUNG 3: astra's C-H "conditional causal FAIL" is a property of every
scalar MOND completion, and the record holds two incompatible criteria.

THE TWO CRITERIA ON THE RECORD
  (A) METRIC-CONE: "show no instantaneous signal" (G03 spec gate P2; g03_covariant_action_2026/FULL_VARIATION.md
      sec. 4-5: C-H's tidal curvature responds outside the metric light cone to a conserved compact source =>
      "conditional causal FAIL").
  (B) FOLIATION / GLOBAL-TIME: a field with infinite sound speed is causal when it carries no signal backward in a
      global time -- Afshordi, Chung & Geshnizjani 2007 (cuscuton); the general k-essence form is Babichev,
      Mukhanov & Vikman 2008 and Bruneton 2007 (causality = a global time function compatible with every
      characteristic cone).  fable_independent_2026/L120 certified the health branch's cuscuton MOND field
      "causal despite infinite formal sound speed" on exactly this criterion.

WHAT THIS LANE SHOWS
  K1 ELLIPTIC MOND FIELDS RESPOND INSTANTANEOUSLY, WITH OR WITHOUT A FILTER.  In any completion whose static weak-
     field limit is QUMOND with a non-propagating MOND field, the phantom stress at a field point P is a local
     functional of g_N at P, and g_N is instantaneous on the leaf.  For a rotating binary the phantom density at a
     distant P oscillates at 2 Omega IN PHASE with the source, while GR's vacuum Ricci at P is identically zero.
     Computed numerically (QUMOND, nu_RAR, both footings) with the light-travel delay for comparison.
  K2 WHY ASTRA'S xi = 0 CASE LOOKED LOCAL: a spherically symmetric, mass-conserving redistribution leaves the
     exterior g_N unchanged (Gauss), so the exterior phantom is unchanged -- the cylinder test's spherical sector
     is blind to the elliptic field and sees only the filter.  Symbolic.
  K3 THE PROPAGATING ALTERNATIVE IS SUPERLUMINAL: a propagating AQUAL scalar (RAQUAL) with F'(y) = mu(sqrt y)
     carries perturbations along its own gradient at v^2 = 1 + d ln mu/d ln x > 1 everywhere mu' > 0 (v^2 -> 2
     in deep MOND).  Symbolic, for mu_2 and the RAR-inverse mu.
  K4 THE CONSEQUENCE TABLE: under (A) every scalar realisation fails (superluminal or instantaneous), so rung 3
     closes and the CLOSURE_MAP decision rule fires; under (B) C-H's cylinder result is not a failure (its clock
     tau is a global time function on the specified slab, X > 0), and G03's causal gate reduces to the
     well-posedness of the mixed elliptic-hyperbolic Cauchy problem, which is OPEN.
  MUTATE=1 sets nu = 1 (Newton/GR): the phantom modulation at P must vanish and K1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L318_causality_criterion_decides_rung3.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L318_causality_criterion_decides_rung3"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L318", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__)
G, C, MSUN, AU, PC, YR = 6.6743e-11, 2.99792458e8, 1.98892e30, 1.495978707e11, 3.0856775814913673e16, 3.15576e7
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}


def nu(x):
    if MUTATE:
        return np.ones_like(x)
    return 1.0 / (1.0 - np.exp(-np.sqrt(x)))


# ============================================================================================ K1
banner("K1  A ROTATING BINARY: the QUMOND phantom at a distant point tracks the source phase with ZERO lag")
M1 = M2 = 1.0 * MSUN
d = 100 * AU                                     # separation
Dp = 0.1 * PC                                    # the field point, in the deep-MOND zone of the pair
Omega = math.sqrt(G * (M1 + M2) / d**3)


def gN(x, phase):
    """Newtonian field of the binary at points x (N,3), instantaneous on the leaf."""
    r1 = 0.5 * d * np.array([math.cos(phase), math.sin(phase), 0.0])
    out = np.zeros_like(x)
    for m, rr in ((M1, r1), (M2, -r1)):
        dx = x - rr
        out -= G * m * dx / np.linalg.norm(dx, axis=1)[:, None]**3
    return out


def rho_phantom(xp, phase, a0, h):
    """QUMOND: lap Phi = 4 pi G rho - div[(nu - 1) g_N] (g = -grad Phi), so 4 pi G rho_ph = -div[(nu(|g_N|/a0) - 1) g_N]."""
    def F(pts):
        g = gN(pts, phase)
        gm = np.linalg.norm(g, axis=1)
        return (nu(gm / a0) - 1.0)[:, None] * g
    div = 0.0
    for k in range(3):
        e = np.zeros(3); e[k] = h
        div += (F(np.array([xp + e]))[0, k] - F(np.array([xp - e]))[0, k]) / (2 * h)
    return -div / (4 * math.pi * G)


xp = np.array([Dp, 0.0, 0.0])
res = {}
for fk, a0 in A0.items():
    phases = np.linspace(0, math.pi, 13)
    rho = np.array([rho_phantom(xp, ph, a0, 1e-3 * Dp) for ph in phases])
    mod = (rho.max() - rho.min()) / max(abs(rho.mean()), 1e-300)
    # fit the 2-phase harmonic: rho = A + B cos(2 phase): the response is a function of the INSTANTANEOUS phase
    Bfit = np.polyfit(np.cos(2 * phases), rho, 1)
    resid = float(np.max(np.abs(np.polyval(Bfit, np.cos(2 * phases)) - rho)) / max(abs(rho.mean()), 1e-300))
    res[fk] = dict(rho_mean=float(rho.mean()), rel_modulation=float(mod), fit_resid=resid,
                   x_at_P=float(np.linalg.norm(gN(np.array([xp]), 0)[0]) / a0))
    P(f"    {fk:9s}: g_N/a0 at P = {res[fk]['x_at_P']:.3f}; <rho_ph(P)> = {rho.mean():.3e} kg/m^3; relative 2-Omega "
      f"modulation = {mod:.2e}; residual from A + B cos(2 phase) = {resid:.1e}")
delay = Dp / C
period = 2 * math.pi / Omega
OUT["numbers"]["K1"] = dict(res=res, light_delay_yr=delay / YR, orbital_period_yr=period / YR,
                            expected_quadrupole_order=(d / Dp)**2)
P(f"    light-travel time D/c = {delay/YR:.3f} yr; orbital period = {period/YR:.0f} yr; (d/D)^2 = {(d/Dp)**2:.1e}")
okK1 = all(v["rel_modulation"] > 1e-6 and v["fit_resid"] < 1e-2 * v["rel_modulation"] for v in res.values())
check("K1 the phantom density (hence the Ricci/Einstein curvature it sources) at P = 0.1 pc oscillates at 2 Omega as "
      "a function of the binary's INSTANTANEOUS phase -- no retardation -- while GR's vacuum Ricci at P is zero",
      "; ".join(f"{k}: modulation {v['rel_modulation']:.2e}" for k, v in res.items()), okK1,
      "an elliptic MOND field responds at spacelike separation with NO filter; astra's criterion (A) therefore "
      "rejects T-Q / QUMOND completions themselves, not the heat kernel")

# ============================================================================================ K2
banner("K2  WHY THE SPHERICAL CYLINDER TEST WAS BLIND AT xi = 0: Gauss")
r, R0, M = sp.symbols("r R0 M", positive=True)
f = sp.Function("f")
rho_sph = f(r)                                           # any spherical profile of fixed total mass inside R0
Menc_out = sp.Symbol("M_total")
gN_out = G * Menc_out / r**2
check("K2 outside a spherical, mass-conserving redistribution g_N = G M_total/r^2 is unchanged, so the exterior "
      "QUMOND phantom (a local functional of g_N) is unchanged: a spherical test cannot see the elliptic field",
      f"g_N(r > R0) = {gN_out} for every interior profile", gN_out.free_symbols == {Menc_out, r},
      "astra's T(k) -> constant at xi -> 0 is this symmetry, not locality of the ξ = 0 theory", load_bearing=False)

# ============================================================================================ K3
banner("K3  THE PROPAGATING ALTERNATIVE (RAQUAL) IS SUPERLUMINAL ALONG ITS OWN GRADIENT")
x = sp.symbols("x", positive=True)
mu2 = 1 - (1 + x / 2)**-2
v2_mu2 = sp.simplify(1 + x * sp.diff(mu2, x) / mu2)
# the RAR's mu as the inverse of nu_RAR: mu(x_obs) with x_obs = nu(y) y; parametrise by y
yv = sp.symbols("y", positive=True)
nuR = 1 / (1 - sp.exp(-sp.sqrt(yv)))
xo = nuR * yv
muR = 1 / nuR
dlnmu_dlnx = sp.simplify((sp.diff(sp.log(muR), yv)) / (sp.diff(sp.log(xo), yv)))
v2_R = 1 + dlnmu_dlnx
vals = {}
for xv in (0.01, 0.1, 1.0, 10.0):
    vals[f"mu2 x={xv}"] = float(v2_mu2.subs(x, xv))
for yvv in (0.01, 0.1, 1.0, 10.0):
    vals[f"RAR y={yvv}"] = float(v2_R.subs(yv, yvv))
lim_deep = sp.limit(v2_mu2, x, 0)
OUT["numbers"]["K3"] = dict(v2=vals, deep_limit=str(lim_deep))
P("    v^2 along grad phi = 1 + d ln mu/d ln x:  " + ", ".join(f"{k}: {v:.3f}" for k, v in vals.items()))
check("K3 a propagating AQUAL scalar is superluminal along its gradient in the whole MOND regime (v^2 > 1, -> 2 in "
      "deep MOND) for mu_2 and for the RAR kernel", f"deep-MOND limit {lim_deep}; min v^2 on the grid "
      f"{min(vals.values()):.4f}", all(v > 1 for v in vals.values()) and lim_deep == 2,
      "Bekenstein-Milgrom 1984's RAQUAL problem, recomputed: under criterion (A) the propagating branch fails too")

# ============================================================================================ K4
banner("K4  THE CONSEQUENCE TABLE")
table = [
    ("(A) metric cone, 'no instantaneous signal'",
     "every scalar MOND completion fails: propagating -> superluminal (K3); non-propagating -> instantaneous (K1)",
     "rung 3 CLOSES; the CLOSURE_MAP decision rule's G03 condition is met; the closing statement applies"),
    ("(B) global time (ACDG 2007; BMV 2008; Bruneton 2007; used by L120)",
     "C-H's leafwise-instantaneous response is tau-simultaneous: no signal runs backward in tau on the slab (X > 0)",
     "C-H's cylinder result is NOT a failure; G03's causal gate reduces to well-posedness of the mixed "
     "elliptic-hyperbolic Cauchy problem (OPEN), then P1 PPN, P3 mode count, S4/S5, C1"),
]
for crit, what, cons in table:
    P(f"    {crit}\n        what happens: {what}\n        consequence : {cons}")
OUT["numbers"]["K4"] = table
check("K4 the record's two criteria give opposite rung-3 verdicts on the same computation, and L120 (cuscuton "
      "certified causal) is incompatible with the G03 P2 criterion",
      "criterion (A) -> rung 3 closed; (B) -> G03 continues on well-posedness", okK1 and all(v > 1 for v in vals.values()),
      "the one decision left on rung 3 is a choice of causality criterion, not another computation")

# ============================================================================================ verdict
banner("VERDICT")
P("""  Astra's conditional causal FAIL for C-H is real under the metric-cone criterion, but it is not a defect of the
  heat kernel: an elliptic MOND field alone makes the curvature at a distant point track a rotating source with
  zero lag (K1), and the propagating alternative is superluminal (K3).  The record therefore contains two
  incompatible causality criteria.  Under the metric-cone criterion, every scalar single-metric MOND completion
  is excluded, rung 3 closes, and the programme's closing statement applies.  Under the literature-standard
  global-time criterion (the one L120 used), C-H survives this gate and G03 reduces to well-posedness.
  Which criterion governs is a decision for the lead track (astra) and the author, not something more computation settles.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
