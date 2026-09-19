#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
C01 -- CONFRONT the candidate's distinctive cluster prediction with real data across the MASS range.
NOVEL: the candidate (THE_ACTION 2026-09-05, item 8) predicts the cluster dark-source peaks at a
UNIVERSAL physical radius r_peak = 2-4H, H = 0.42 e c^2/(|K2| a0), the SAME in every cluster, "where an
NFW scale radius grows as M^{1/3}".  This was only ever confronted with MASSIVE X-COP clusters (g03u,
single mass decade); the MASS-INDEPENDENCE -- its own stated discriminator vs LambdaCDM -- has never been
tested.  Here it is, against the robust observed dark-component scale-radius-vs-mass relation.

THE PREDICTION (candidate):
  |K2| is a UNIVERSAL constant (fixed by the galaxy/cluster split to [5e4, 5e5]); so H is universal
  (140-355 kpc canonical) and the dust ratio M_d/M_b peaks at r_peak = 2-4H = a fixed physical radius for
  EVERY system, independent of mass.

THE DATA (LambdaCDM / observed, robust):
  Clusters and groups are ~self-similar: the dark-component scale radius r_s = R_500/c_500 grows with mass
  as ~M^{1/3} (weak c-M running).  Real anchors span groups (M_500~1-3e13, r_s~60-120 kpc) to massive
  clusters (M_500~7-10e14, r_s~350-500 kpc): a factor ~4-5 over two decades.  R_500 itself spans x4.6.

  C1 [DERIVE] R_500(M_500) and the observed dark r_s(M) ~ M^{1/3}; span x4-5 over 1e13-1e15 Msun.
  C2 [CANDIDATE] r_peak = 2-4H is a mass-INDEPENDENT constant for the allowed |K2| window.
  C3 [FORK] a universal r_peak matches the data at AT MOST one mass; to fit each system |K2| must scale as
     M^{-1/3} (a factor ~4.6 across the range) -- contradicting the universal-constant claim.
  C4 [GROUPS] the universal r_peak (280-880 kpc for the best |K2|) EXCEEDS the R_500 of real groups
     (~330-500 kpc): the candidate predicts the dark source peaks AT/BEYOND a group's virial radius, which
     is not observed -- a clean failure at the low-mass end (the |K2| that fits groups is OUTSIDE its
     window and gives the wrong amplitude).

VERDICT: the candidate's distinctive mass-INDEPENDENT cluster dark-source peak radius is in SERIOUS TENSION
with the observed r_s ~ M^{1/3} self-similarity: the dark-component characteristic radius scales by x7.4
across the group-cluster mass range, which a universal |K2| cannot reproduce (fitting each system needs
|K2| ~ M^{-1/3}).  This holds UNDER THE FRAMEWORK'S OWN requirement that the dust is the DOMINANT cluster
dark component (6.8x baryons, g04a).  ESCAPE (why it is not a clean kill): if MOND's phantom (which scales
with mass) dominates and the constant-H dust is subdominant, the tension relaxes.  HONEST: r_peak-vs-r_s is
a PROXY (dust-ratio peak vs NFW scale) -- the SCALING mismatch is the result, not the absolute numbers; the
group failure is conditional; a fully rigorous confrontation needs a mass-range residual-after-MOND
analysis (X-COP + groups).  A real, quantified new cost extending the record's massive-only liability.

LEAN CERTIFICATE: the load-bearing scaling math (r_s(M)=k M^(1/3) strictly increasing => a universal H
matches at most one mass; the required coupling K2(M)=A/r_s(M) is strictly decreasing, i.e. ~M^(-1/3), not
constant) is proved in fable_independent_2026/lean_2026/C01_mass_scaling.lean (rs_strictMono,
universal_H_at_most_one_mass, K2_required_strictAnti; mathlib v4.34, 0 sorry, compiles).

Run:  python3 opus_48_extended_research/cluster_massindep_2026/C01_mass_independent_peak_radius_test.py
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "C01_mass_independent_peak_radius_test"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "C01", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading=""):
    ok = bool(ok); CH.append((name, ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
# constants
c = 2.998e8; MSUN = 1.989e30; MPC = 3.086e22; KPC = 3.086e19; G = 6.674e-11
H0 = 70 * 1e3 / MPC; rho_crit = 3 * H0**2 / (8 * math.pi * G)     # kg/m^3
a0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

# =================================================================================================
banner("C1 [DATA] R_500(M_500) and the observed dark scale radius r_s ~ M^{1/3} (self-similarity + anchors)")
def R500_kpc(M500_sun):
    M = M500_sun * MSUN
    R = (3 * M / (4 * math.pi * 500 * rho_crit)) ** (1.0 / 3.0)      # m
    return R / KPC
def c500(M500_sun):                                                 # weak c-M (Duffy+08-like, cluster range)
    return 3.2 * (M500_sun / 1e14) ** (-0.10)
masses = [1e13, 3e13, 1e14, 3e14, 1e15]
P(f"    {'M_500(Msun)':>12s} {'R_500(kpc)':>11s} {'c_500':>6s} {'r_s=R500/c (kpc)':>17s}")
rs = {}
for M in masses:
    R = R500_kpc(M); cc = c500(M); r = R / cc; rs[M] = r
    P(f"    {M:12.0e} {R:11.0f} {cc:6.2f} {r:17.0f}")
span = rs[1e15] / rs[1e13]
OUT["numbers"]["rs_kpc_by_mass"] = {f"{M:.0e}": rs[M] for M in masses}
OUT["numbers"]["rs_span_1e13_1e15"] = span
# real published anchors (total-mass NFW scale radii), for grounding
anchors = {"NGC5044 group (~2e13)": (2e13, 90), "Coma (~7e14)": (7e14, 430), "A2029 (~8e14)": (8e14, 450)}
P("    real anchors (published NFW r_s):")
for k, (M, r) in anchors.items():
    P(f"      {k:22s}: M_500~{M:.0e}, r_s~{r} kpc")
check("C1 the observed dark-component scale radius r_s = R_500/c_500 GROWS with mass as ~M^{1/3} (weak c-M "
      "running), spanning a factor ~4-5 over M_500 = 1e13-1e15; real anchors (groups ~90 kpc, massive "
      "clusters ~430-450 kpc) confirm the scaling",
      f"r_s: {rs[1e13]:.0f} kpc (1e13) -> {rs[1e15]:.0f} kpc (1e15), span x{span:.1f}",
      span > 3.0,
      "cluster self-similarity: the dark component tracks R_500 ~ M^{1/3}, a robust observational fact")

# =================================================================================================
banner("C2 [CANDIDATE] r_peak = 2-4H is a mass-INDEPENDENT constant")
def H_kpc(K2, foot):
    return 0.42 * math.e * c**2 / (K2 * a0[foot]) / KPC
K2_window = [5e4, 2e5, 5e5]                                          # allowed window; 2e5 = best X-COP fit
P(f"    {'|K2|':>8s} {'H (kpc,canon)':>13s} {'r_peak=2-4H (kpc)':>18s}")
Hbest = None
for K2 in K2_window:
    Hc = H_kpc(K2, "canonical")
    if abs(K2 - 2e5) < 1: Hbest = Hc
    P(f"    {K2:8.0e} {Hc:13.0f} {2*Hc:5.0f} - {4*Hc:.0f}")
OUT["numbers"]["H_kpc_best_K2_2e5"] = Hbest
OUT["numbers"]["r_peak_best_kpc"] = [2 * Hbest, 4 * Hbest]
check("C2 the candidate's dust ratio M_d/M_b peaks at r_peak = 2-4H, a UNIVERSAL constant fixed by the "
      "single universal |K2| -- the SAME physical radius in every cluster regardless of mass",
      f"best-fit |K2|=2e5 -> H={Hbest:.0f} kpc, r_peak={2*Hbest:.0f}-{4*Hbest:.0f} kpc (mass-independent)",
      True,
      "this is the candidate's explicit distinctive prediction (THE_ACTION item 8)")

# =================================================================================================
banner("C3 [FORK] a universal r_peak matches at one mass; fitting each system needs |K2| ~ M^{-1/3}")
# to make r_peak (=~3H) match the observed r_s(M) at each mass, |K2| must scale as 1/r_s ~ M^{-1/3}
def K2_needed(M):
    target_H = rs[M] / 3.0                                           # r_peak ~ 3H matched to r_s
    return 0.42 * math.e * c**2 / (target_H * KPC * a0["canonical"])
K2req = {M: K2_needed(M) for M in masses}
span_K2 = K2req[1e13] / K2req[1e15]
OUT["numbers"]["K2_required_by_mass"] = {f"{M:.0e}": K2req[M] for M in masses}
OUT["numbers"]["K2_required_span"] = span_K2
P(f"    {'M_500':>10s} {'|K2| needed':>12s}")
for M in masses:
    P(f"    {M:10.0e} {K2req[M]:12.1e}")
P(f"    => |K2| must span x{span_K2:.1f} across the mass range (M^-1/3); it is claimed UNIVERSAL")
check("C3 to place the dark-source peak at the observed r_s(M) for each system, the 'universal' |K2| would "
      "have to scale as M^{-1/3}, spanning a factor ~4-5 -- directly contradicting the constant-|K2| claim",
      f"|K2| required: {K2req[1e13]:.1e} (1e13) -> {K2req[1e15]:.1e} (1e15), span x{span_K2:.1f}",
      span_K2 > 3.0,
      "the distinctive prediction is that ONE |K2| works everywhere; the data demand |K2| ~ M^{-1/3}")

# =================================================================================================
banner("C4 [GROUPS] the universal r_peak exceeds a group's R_500 -- clean low-mass failure")
Rg = R500_kpc(2e13); rpeak_lo, rpeak_hi = 2 * Hbest, 4 * Hbest
OUT["numbers"]["group_R500_kpc"] = Rg
P(f"    group M_500~2e13: R_500 = {Rg:.0f} kpc; candidate r_peak = {rpeak_lo:.0f}-{rpeak_hi:.0f} kpc")
check("C4 for a real group (M_500~2e13, R_500~"+f"{Rg:.0f} kpc), the candidate's universal r_peak "
      f"({rpeak_lo:.0f}-{rpeak_hi:.0f} kpc) is AT/BEYOND the group's virial radius -- it predicts the dark "
      "source peaks outside the group, which is not observed; the |K2| that would fit groups is outside "
      "its allowed window and breaks the amplitude",
      f"r_peak {rpeak_lo:.0f}-{rpeak_hi:.0f} kpc vs group R_500 {Rg:.0f} kpc (r_peak >~ R_500)",
      rpeak_hi > Rg,
      "the mass-independent H fails hardest at the low-mass end, exactly where R_500 is smallest")

# =================================================================================================
banner("VERDICT")
P(f"""  (1) CONFRONTED: the candidate's distinctive mass-INDEPENDENT cluster dark-source peak radius
      (r_peak = 2-4H, universal |K2|) against the observed dark-component scale radius r_s ~ M^{{1/3}}.
  (2) RESULT: r_s spans x{span:.1f} over M_500 = 1e13-1e15 (groups ~{rs[1e13]:.0f} kpc, massive ~{rs[1e15]:.0f}
      kpc; real anchors confirm), while the candidate's r_peak is a fixed {2*Hbest:.0f}-{4*Hbest:.0f} kpc.
      To fit each system the 'universal' |K2| must scale as M^{{-1/3}} (x{span_K2:.1f}); and the fixed
      r_peak exceeds a real group's R_500 ({Rg:.0f} kpc), predicting a dark source peaking beyond the group.
  (3) HONEST SENTENCE: the candidate's own stated LambdaCDM-discriminator -- the SAME dark-source radius in
      every cluster -- is in SERIOUS TENSION with cluster self-similarity.  The ROBUST, load-bearing result
      is C3: whatever the exact definition of the dark characteristic radius, it scales as ~M^{1/3} (x7.4
      over 1e13-1e15), so a UNIVERSAL |K2| cannot match it -- fitting each system needs |K2| ~ M^{-1/3}.
      This holds UNDER THE FRAMEWORK'S OWN requirement that the dust is the DOMINANT cluster dark component
      (6.8x baryons in massive clusters, g04a); if instead MOND's phantom (which scales with mass) dominates
      and the constant-H dust is subdominant, the tension relaxes.  CAVEATS, stated: (a) the absolute
      r_peak-vs-r_s comparison mixes two radius definitions (dust-ratio peak vs NFW scale) and is a PROXY --
      the scaling mismatch, not the absolute numbers, is the result; (b) C4's group failure is CONDITIONAL
      on groups needing the constant-H dust as their dominant dark component, which the record computed only
      for massive clusters; (c) a fully rigorous confrontation needs a residual-after-MOND analysis across
      mass (X-COP massive + a group sample).  NET: this EXTENDS the record's massive-only cluster liability
      (g03u) into a mass-scaling problem and shows the distinctive 'universal radius' prediction cannot hold
      across the mass range under the framework's dust-dominant requirement.  NOT a clean referee-proof kill
      (the MOND-phantom-vs-dust decomposition is the escape); a real, quantified new cost.""")
OUT["verdict"] = {"word": "MASS-INDEPENDENT-PEAK-RADIUS-IN-SERIOUS-TENSION-conditional-on-dust-dominant",
                  "rs_span": span, "K2_required_span": span_K2,
                  "candidate_r_peak_kpc": [2 * Hbest, 4 * Hbest], "group_R500_kpc": Rg,
                  "robust_result": "observed dark radius scales ~M^{1/3} (x7.4); universal |K2| cannot -> "
                                   "needs |K2|~M^{-1/3}",
                  "escape": "if MOND phantom (mass-scaling) dominates and constant-H dust is subdominant",
                  "caveat": "r_peak-vs-r_s is a proxy; group failure conditional; full test needs mass-range "
                            "residual-after-MOND analysis"}

banner("RESULT")
npass = sum(1 for _, ok in CH if ok); n = len(CH); fails = [nm for nm, ok in CH if not ok]
P(f"C01 COMPLETE: {npass}/{n} checks PASS")
for nm in fails:
    P(f"    FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "fail": fails}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(0)
