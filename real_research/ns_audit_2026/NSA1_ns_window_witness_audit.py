#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
NSA1 -- THE NAVIER-STOKES WINDOW "WITNESS" IS AUTOMATIC: what the framework's constants can and cannot say about
Clay-NSE (audit of deepseek_push/navier_stokes_attempt N05 / N08 / N13).

THE CLAIMS AUDITED
  N05 (window theorem): any smooth NSE solution with sup|Du/Dt| <= 3.5*a0 is globally smooth; corollary: any
      singularity must EXIT the window.  N08/N13: the OpenAI forced-blowup construction exits the floor at
      tau_exit ~ 5e-7 -- "the N05 corollary's predicted exit, now witnessed"; N11 calls this "the record's most
      defensible claim" because the floor -> exit -> face structure was pre-registered before the witness.

WHAT THIS LANE SHOWS
  K1 THE CONSTANT IS INERT.  N05's proof uses a0*W only as "some finite C": sup|u(t)| <= U0 + C t, then Serrin.
     The corollary therefore holds for EVERY C > 0 and is equivalent to "a singularity has unbounded material
     acceleration" -- a statement with no a0 in it.  Any blowup with |Du/Dt| -> infinity exits every window;
     the construction's scaling |Du/Dt| ~ tau^-(3/2+2h) exits all C across 600 decades.  P(exit | C = 3.5 a0) =
     P(exit | any C) = 1: the "witness" has Bayes factor exactly 1 for the framework.
  K2 THE RECORDED EXIT TIME IS ALGEBRAICALLY INVERTED.  N13 defines eta(tau) = tau^-(3/2+2h) * a_scale/a0 and
     reports eta(1) = 1.07e10, then solves tau^(3/2+2h) = 3.5 a0/a_scale (should be a_scale/(3.5 a0)), giving
     tau_exit = 4.75e-7.  At that tau its own eta is ~3e19, not 3.5.  The correct crossing is tau* ~ 2e6 > 1:
     under the stated lab mapping the construction is above the floor for the WHOLE final decade -- there is no
     in-regime exit.  N08's 5.2e-7 "cross-check" repeats the same inversion.
  K3 THE LAB MAPPING IS A GAUGE.  NSE is invariant under u_l(x,t) = l u(l x, l^2 t); Du/Dt scales as l^3.  The
     choice a_scale = 1 m/s^2 (N13 l.34) is one point on that orbit; sweeping it moves tau* over (0, inf).  A
     dimensional constant has no invariant place in the dimensionless blowup statement.
  K4 a0-BOUNDED TERMS ARE IRRELEVANT AT A SINGULARITY.  Every NSE term scales as l^3; a force bounded by a0/2 (the
     Lean-certified cap, N02) scales as l^0, relative weight l^-3 -> 0.  Damping kappa|u|^(b-1)u has relative
     weight kappa l^(b-3): only b >= 3 reaches a singularity, and that global result is Zhou 2012 (cited).
  K5 kappa -> 0 IS THE CLAY PROBLEM.  The damped system's sup barrier (A/kappa)^(1/b) diverges as kappa -> 0, and
     the framework's own survival pin (kappa <= 2.6e-9, N06) pushes kappa toward that limit.  Passing to kappa = 0
     needs a kappa-uniform bound on ||u||_inf, i.e. the a priori estimate Clay (A)/(B) asks for.
  N6 (documentary, not load-bearing): per N08/N14 the OpenAI construction, if it survives review, satisfies
     Fefferman's (C) -- f in C_c^inf meets decay condition (5), u0 = 0 meets (4) -- with no framework input.

  MUTATE=1 gives the construction BOUNDED material acceleration (exponent p = 0): no singularity, so the exit
  sweep must fail for C above the bound and K1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/ns_audit_2026/NSA1_ns_window_witness_audit.py
"""
import os, sys, json
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "NSA1_ns_window_witness_audit"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "NSA1", "mutate": MUTATE, "checks": {}, "numbers": {}}

A0_CANON, A0_ALT = 9.36e-11, 1.13e-10     # both footings (m/s^2)
A0_N05 = 9.3619e-11                       # the value N05/N13 use
W = 3.5                                   # N05 floor
ASCALE_N13 = 1.0                          # N13 lab mapping, m/s^2
TAU_EXIT_N13 = {0.0: 4.752856420037148e-07, 1 / 200: 5.233945149518305e-07}   # N13_construction_audit_results.json


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


tau, h, C, U0, t, lam, kap, b, A = sp.symbols("tau h C U0 t lambda kappa beta A", positive=True)
p_sym = sp.Rational(3, 2) + 2 * h          # construction: |Du/Dt| ~ a_scale * tau^-p   (N13 A6)

# ============================================================================================ K1
banner("K1  THE WINDOW CONSTANT IS INERT: the corollary holds for every C > 0")
# N05 step 1: |u(t)| <= U0 + C t.  Finite for every finite C and t -> Serrin applies for every C.
bound = U0 + C * t
finite_for_all_C = sp.ask(sp.Q.finite(bound), sp.Q.positive(C) & sp.Q.positive(t) & sp.Q.positive(U0))
P(f"    N05 trajectory bound: sup|u| <= {bound}; finite for every C > 0, t < inf: {finite_for_all_C}")

p_run = 0 if MUTATE else 1.5 + 2 * (1 / 200)
Cs = np.logspace(-300, 300, 601)           # m/s^2, 600 decades
exits = []
for Cv in Cs:
    # exit <=> exists tau in (0,1) with a_scale*tau^-p > Cv
    if p_run > 0:
        exits.append(True)                 # tau^-p -> inf as tau -> 0: every finite Cv is crossed
    else:
        exits.append(ASCALE_N13 > Cv)      # bounded acceleration: exits only windows below the bound
frac = float(np.mean(exits))
for foot, a0 in (("canonical", A0_CANON), ("alt", A0_ALT)):
    P(f"    {foot:9s}: window 3.5*a0 = {W * a0:.4e} m/s^2 -> exited: {p_run > 0 or ASCALE_N13 > W * a0}")
OUT["numbers"]["K1"] = {"exponent_p": p_run, "decades_swept": 600, "fraction_of_C_exited": frac,
                        "bayes_factor_framework_vs_any_C": 1.0 if frac == 1.0 else None}
check("K1 every window C in 1e-300..1e300 m/s^2 is exited by the construction; the corollary contains no a0 "
      "(Bayes factor of the 'witness' = 1)", f"fraction exited = {frac:.3f} (p = {p_run})",
      finite_for_all_C and frac == 1.0,
      "'singularity => window exit' is 'singularity => unbounded Du/Dt' with a0 written in; any blowup witnesses it")

# ============================================================================================ K2
banner("K2  THE RECORDED tau_exit (N13 4.75e-7, N08 5.2e-7) SOLVES THE INVERTED EQUATION")
eta = lambda tv, hv, asc=ASCALE_N13, a0=A0_N05: tv ** -(1.5 + 2 * hv) * asc / a0
rows = {}
for hv, te in TAU_EXIT_N13.items():
    pv = 1.5 + 2 * hv
    tau_star = (ASCALE_N13 / (W * A0_N05)) ** (1 / pv)      # eta(tau*) = W, correct root
    rows[f"h={hv:.4f}"] = {"tau_exit_N13": te, "eta_at_N13_tau": eta(te, hv),
                           "tau_star_correct": tau_star, "eta_at_tau_star": eta(tau_star, hv),
                           "eta_at_tau_1": eta(1.0, hv)}
    P(f"    h = {hv:.4f}: N13 tau_exit = {te:.3e} -> eta there = {eta(te, hv):.3e}  (should be 3.5)")
    P(f"              correct root tau* = {tau_star:.3e} -> eta(tau*) = {eta(tau_star, hv):.4f};  "
      f"eta(tau=1) = {eta(1.0, hv):.3e}")
OUT["numbers"]["K2"] = rows
worst = min(np.log10(r["eta_at_N13_tau"] / W) for r in rows.values())
okK2 = all(abs(r["eta_at_tau_star"] - W) < 1e-9 and r["tau_star_correct"] > 1 and r["eta_at_tau_1"] > W
           for r in rows.values()) and worst > 15
check("K2 N13's tau_exit misses eta = 3.5 by >15 decades; the correct root is tau* > 1, so under N13's own lab "
      "mapping the flow is above the floor throughout tau in (0,1] -- no in-regime exit",
      f"eta at N13 tau_exit exceeds 3.5 by >= 10^{worst:.1f}; tau* = "
      f"{min(r['tau_star_correct'] for r in rows.values()):.2e}", okK2,
      "the N08/N13 '3 s.f. match' is two copies of one inversion: tau^p = 3.5 a0/a_scale instead of a_scale/(3.5 a0)")

# ============================================================================================ K3
banner("K3  THE LAB MAPPING IS A GAUGE OF THE NSE SCALING SYMMETRY")
x, nu = sp.symbols("x nu", positive=True)
# u_l(x,t) = l u(l x, l^2 t), tested on a concrete smooth profile: every term of the 1-D Burgers skeleton of NSE
# (u_t, u u_x, nu u_xx) must pick up exactly l^3 relative to the same term evaluated at (l x, l^2 t).
u0f = sp.sin(x) * sp.exp(-t) + sp.cos(2 * x) * sp.exp(-3 * t)
at = {x: lam * x, t: lam ** 2 * t}
ul = lam * u0f.subs(at, simultaneous=True)
terms = {"u_t": (sp.diff(ul, t), sp.diff(u0f, t)),
         "u u_x": (ul * sp.diff(ul, x), u0f * sp.diff(u0f, x)),
         "nu u_xx": (nu * sp.diff(ul, x, 2), nu * sp.diff(u0f, x, 2))}
ratios = {k: sp.simplify(sc / base.subs(at, simultaneous=True)) for k, (sc, base) in terms.items()}
P(f"    term ratios under u_l: {ratios}")
power_t = sp.simplify(sp.log(ratios["u_t"]) / sp.log(lam)) if all(r == ratios["u_t"] for r in ratios.values()) else None
ascales = np.logspace(-30, 30, 61)
tstars = (ascales / (W * A0_N05)) ** (1 / (1.5 + 2 / 200))
OUT["numbers"]["K3"] = {"accel_scaling_power": str(power_t), "a_scale_range": [ascales[0], ascales[-1]],
                        "tau_star_range": [float(tstars.min()), float(tstars.max())]}
P(f"    d/dt[l u(l x, l^2 t)] carries l^{power_t}; a_scale = U0^2/L0 takes any positive value along the orbit")
P(f"    a_scale 1e-30..1e30 m/s^2 -> tau* from {tstars.min():.2e} to {tstars.max():.2e}")
check("K3 Du/Dt scales as l^3 under the NSE symmetry, so the exit time of a dimensionless blowup against a "
      "dimensional window is set by the unit choice (tau* spans both sides of 1)",
      f"power {power_t}; tau* in [{tstars.min():.1e}, {tstars.max():.1e}]",
      sp.simplify(power_t - 3) == 0 and tstars.min() < 1 < tstars.max(),
      "'exit at tau ~ 5e-7' has no invariant meaning even with the algebra corrected")

# ============================================================================================ K4
banner("K4  a0-BOUNDED TERMS ARE SCALING-IRRELEVANT AT A SINGULARITY; ONLY DAMPING b >= 3 REACHES IT")
nse_power = 3
cap_rel = lam ** 0 / lam ** nse_power                  # |force| <= a0/2 does not scale
damp_rel = kap * lam ** b / lam ** nse_power
lim_cap = sp.limit(cap_rel, lam, sp.oo)
regimes = {bv: sp.limit(damp_rel.subs(b, bv), lam, sp.oo) for bv in (2, sp.Rational(5, 2), 3, 4)}
P(f"    a0/2-capped force, relative weight l^0/l^3 -> {lim_cap}")
for bv, lv in regimes.items():
    P(f"    damping kappa|u|^(b-1)u, b = {bv}: relative weight kappa l^(b-3) -> {lv}")
OUT["numbers"]["K4"] = {"cap_rel_limit": str(lim_cap), "damping_limits": {str(k): str(v) for k, v in regimes.items()}}
check("K4 the a0/2-capped class vanishes at blowup scales (l^-3); damping with b < 3 vanishes, b = 3 is critical, "
      "b > 3 dominates", f"cap -> {lim_cap}; b=2 -> {regimes[2]}, b=3 -> {regimes[3]}, b=4 -> {regimes[4]}",
      lim_cap == 0 and regimes[2] == 0 and regimes[3] == kap and regimes[4] == sp.oo,
      "the only regularising member is the damped NSE of Zhou 2012 (cited in N03b); a0 supplies no exponent")

# ============================================================================================ K5
banner("K5  kappa -> 0 IS THE CLAY GAP")
barrier = (A / kap) ** (1 / b)
lim_b = {bv: sp.limit(barrier.subs(b, bv), kap, 0, "+") for bv in (2, 3)}
kap_pin = 2.6e-9
OUT["numbers"]["K5"] = {"barrier_limits": {str(k): str(v) for k, v in lim_b.items()}, "kappa_pin_N06": kap_pin,
                        "barrier_b3_at_pin_over_A13": (1 / kap_pin) ** (1 / 3)}
P(f"    sup barrier (A/kappa)^(1/b) as kappa -> 0: b=2 -> {lim_b[2]}, b=3 -> {lim_b[3]}")
P(f"    framework survival pin kappa <= {kap_pin:g} (N06): barrier/A^(1/3) >= {(1 / kap_pin) ** (1 / 3):.3e} at b = 3")
check("K5 the damped family's regularity constant diverges as kappa -> 0; transferring it to NSE needs a "
      "kappa-uniform sup bound, which is the Clay (A)/(B) estimate itself",
      f"limits {lim_b}", all(v == sp.oo for v in lim_b.values()),
      "the framework does not fix kappa (G03 open) and its own survival pin drives kappa toward the singular limit")

# ============================================================================================ N6
banner("N6  (documentary) FEFFERMAN (C) vs THE OPENAI CONSTRUCTION AS RECORDED IN N08/N14")
fc = [("u0 smooth, div-free, decay (4)", "u0 = 0"),
      ("f smooth with decay (5): |d^a_x d^m_t f| <= C (1+|x|+t)^-K", "f in C_c^inf(R^3 x (0,inf)) -- compact support"),
      ("no solution with (1),(2),(3),(6),(7)", "no global finite-energy smooth solution (Lean: breakdownStatement)")]
for need, have in fc:
    P(f"    {need:62s} <- {have}")
check("N6 as recorded, the OpenAI construction targets Fefferman (C)/(D) with no framework input (unrefereed)",
      "per N08/N14; not re-verified here", True, "if it survives review, the prize question is answered by (C); "
      "(A)/(B) stay open either way", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P("""  The framework's constants cannot finish Clay-NSE.  The window theorem is true for every constant, so the
  'witnessed exit' holds for any blowup and carries no evidence for a0 (K1); the recorded exit time solves an
  inverted equation (K2) and in any case depends on an arbitrary unit choice (K3).  At a singularity every
  a0-bounded term is scaled away (K4), and the one regularising completion is the literature damped NSE, whose
  constant diverges in exactly the kappa -> 0 limit that is the Clay problem (K5).  What stays on the record as
  framework physics (N06's eBTFR fingerprint, conditional on a G03-derived kappa; N07's dust sector) is not a
  statement about Clay-NSE.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
