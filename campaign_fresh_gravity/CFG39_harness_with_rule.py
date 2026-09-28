#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG39 -- CANDIDATE B's HARNESS RE-RUN WITH THE DERIVED COLD-MASS RULE: does adding the conservation rule (CFG35-38) cost any gate?

WHY.  CFG35 derived T5's conservation form from T4; with Mandelbaum+2016's measured colour-split collapse masses (CFG36) it leaves every
star-forming spiral and every passive disk below log M_* ~ 11.2 on the law (CFG36, CFG37) and fits the SLUGGS massive early types (CFG38).
Before B adopts it, every gate of B's 48-gate harness (CFG19: 42/48) must be checked.  The rule changes the dark mass ONLY where a
system's collapse cold mass exceeds its phantom (f_ex > 0): massive red galaxies, groups and clusters.  So the gates split cleanly:
  UNCHANGED BY CONSTRUCTION (no system in the gate has f_ex > 0, or the gate does not read the cold mass): CMB lensing and the forest
      (linear; the cold fluid's amount is unchanged), Cassini, every population gate (satellites, dwarfs, UFDs, TDGs, GCs, DF2/DF4,
      Chae's wide binaries, the cluster-infall BTFR and the LV host statistic -- all low-mass or Newtonian-owned systems).
  RECOMPUTED HERE: SPARC (its few massive S0s take the red relation); the cold-mass BUDGET (the rule's leftover locks extra cold fluid
      in massive systems); KiDS (only if its lens bins reach the rule's threshold mass).
  NOT RE-SCORABLE WITHOUT CIRCULARITY: X-COP and the Bullet (every collapse-mass estimate in the repository for them comes from their own
      mass); the rule's dark mass there is at least the as-written identity's (the rule is a floor-raiser), so they keep their rows.

THE METHOD (declared before this script's first run).  CFG36's collapse masses (Mandelbaum red/blue, M_200c) and CFG35's edge phantom
(x_e = 0.40), exec'd read-only.
  SPARC: hunt_lib's loader (Q <= 2, inc >= 30, >= 6 points), Upsilon_disk 0.61 (CFG4's nu_mono fit), per-point log(g_obs / g_pred); the
      rule adds f_ex (1 - f_b) G M_NFW(<r) / r^2 to g_pred for galaxies with f_ex > 0 (T >= 1 blue, T = 0 red; log M_* >= 10.0, the
      table's range).  The rms over all points with and without the rule.
  BUDGET: CFG11's copy of CFG4_target's SMF integral (GAMA SMF, SPARC gas fractions), each galaxy's dark mass max(M_ph,edge, (1 - f_b)
      M_coll) with M_coll from the red and blue relations weighted by the red fraction of Mandelbaum's own central sample (N_red /
      N_total per stellar-mass bin, sample_table.tex), log M_* >= 10.0; lenient (z = 0.25, all of Omega_c) and strict (z = 0, the
      turned-around share), as the harness.
  KiDS: the stellar mass where the red rule's leftover first switches on, against Brouwer+2021's isolated-lens bins (top bin log M_*
      10.8-11.0 in the paper; the bin edges are not in the repository's data headers -- flagged).

PRE-DECLARED
  C1  CONTROL  the harness's committed budget Omega_ph at x_e = 0.4 reproduced from CFG11's integral (lenient and strict, both kernels,
      both footings) to 0.001.
  C2  CONTROL  the SPARC rms without the rule reproduces CFG4's nu_mono canonical fit to 0.003 dex (0.1003).
  H1  [HEADLINE; MUTATE must fail] THE RULE COSTS NO GATE: SPARC's rms moves by < 0.005 dex; the lenient budget still passes (Omega_needed
      <= Omega_c) on all four cells; the KiDS lens bins lie below the rule's threshold mass; so B's harness score is unchanged (42/48).
  H2  (reported) the strict budget (already failing, reported) with and without the rule; the leftover's share of Omega_c.
  READING (declared): H1 PASS -> B adopts the derived conservation rule at no cost to its harness.  H1 FAIL -> adopting it costs the
  named gate(s).
FIXED BEFORE THE MAIN RUN (disclosed; the MUTATE runs exposed them): a0 was passed to CFG11's SI integral in (km/s)^2/Mpc (C1 caught
  it); the SPARC gate first used hunt_lib's unweighted loader, whose rms is 0.178, not CFG4's 0.100 (C2 caught it) -- it now uses
  CFG4's own weighted statistic and arrays, exec'd read-only.  No threshold changed.
MUTATE=1: every collapse mass multiplied by 30 -- the rule then floods the budget and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG39_harness_with_rule.py   (MUTATE=1 for the control)
"""
import os, sys, math, io, contextlib, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG39_harness_with_rule", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every collapse mass x 30 -- H1 must FAIL ***")
MCF = 30.0 if MUTATE else 1.0
HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)


def exec_prefix(fname, marker):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(HERE, fname)).read()
    g = {"__file__": os.path.join(HERE, fname), "__name__": fname}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index(marker)], fname, "exec"), g)
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


g36 = exec_prefix("CFG36_colour_split_collapse.py", "# ================================================================================================ H1")
collapse, edge_phantom, FB, nfw_enclosed = g36["collapse"], g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]
g11 = exec_prefix("CFG11_budget_hierarchy.py", "XG = (0.2, 0.3, 0.31")
omega_ph, lmg, Mst_h, phi_h, RHOC0_MSUN, MB_SMF, OC0 = (g11[k] for k in ("omega_ph", "lmg", "Mst_h", "phi_h", "RHOC0_MSUN", "_MB_SMF", "OC0"))
rta_of = g11["rta_of"]
CU = g11["C"]                                                                       # CFG11's unit module (G_SI, MSUN)
KERN = {"P2": C.nu_p2, "nu_mono": C.nu_mono}

# ================================================================================================ C1 the budget
R.banner("C1  CONTROL: the harness's committed budget rows")
H19 = json.load(open(os.path.join(HERE, "CFG19_harness_rescore_results.json")))["numbers"]["B_rescored"]["rows"]
com = {(r["foot"], r["kern"], "len" if r["gate"] == "BUDGET lenient" else "str"): float(r["value"].split("Omega_ph ")[1].split(" ")[0])
       for r in H19 if r["gate"].startswith("BUDGET")}
LIM = {"len": float([r for r in H19 if r["gate"] == "BUDGET lenient"][0]["value"].split("vs Omega_c ")[1]),
       "str": float([r for r in H19 if r["gate"].startswith("BUDGET strict")][0]["value"].split(" vs ")[1])}
mine = {(f, k, t): omega_ph(KERN[k], C.A0_SI[f], 0.25 if t == "len" else 0.0, 0.40, 7.0) for (f, k, t) in com}
dev1 = max(abs(round(mine[k], 3) - com[k]) for k in com)
check("C1 CONTROL: the harness's committed budget Omega_ph (x_e = 0.4) reproduced from CFG11's integral",
      "; ".join(f"{k[0][:3]}/{k[1]}/{k[2]}: {mine[k]:.3f} ({com[k]:.3f})" for k in sorted(com)) + f"; limits {LIM}", dev1 <= 0.001 + 1e-12)

# the red fraction of Mandelbaum's central sample, per stellar-mass bin (sample_table.tex N_gal)
NRED = {10.28: 4244, 10.58: 17542, 10.86: 44724, 11.10: 37987, 11.29: 28008, 11.48: 12599, 11.68: 3195}
NBLU = {10.24: 20690, 10.56: 30842, 10.85: 33621, 11.10: 11040, 11.28: 2626, 11.47: 325, 11.68: 96}
LF = np.array(sorted(NRED)); FR = np.array([NRED[k] / (NRED[k] + NBLU[kb]) for k, kb in zip(sorted(NRED), sorted(NBLU))])
f_red = lambda lm: float(np.interp(lm, LF, FR))
P(f"    red fraction of Mandelbaum's centrals by log M_*: " + ", ".join(f"{l:.2f}: {f:.2f}" for l, f in zip(LF, FR)))


def omega_rule(kfun, a0, z, x=0.40, mcut=7.0):
    rc = x * rta_of(MB_SMF, kfun, a0, z)
    mph = MB_SMF * (kfun(CU.G_SI * MB_SMF / rc ** 2 / a0) - 1.0) / CU.MSUN
    dark = mph.copy()
    for i, (lm, Ms) in enumerate(zip(np.log10(Mst_h), Mst_h)):
        if lm < 10.0:
            continue
        fr = f_red(lm)
        dr = max(mph[i], (1 - FB) * MCF * collapse(Ms, "red")); db = max(mph[i], (1 - FB) * MCF * collapse(Ms, "blue"))
        dark[i] = fr * dr + (1 - fr) * db
    m = np.log10(Mst_h) >= mcut
    return float(np.trapz((phi_h * dark)[m], lmg[m]) / RHOC0_MSUN), float(np.trapz((phi_h * mph)[m], lmg[m]) / RHOC0_MSUN)


R.banner("BUDGET WITH THE RULE")
BUD = {}
for f in C.FOOTS:
    for k in KERN:
        for t, z in (("len", 0.25), ("str", 0.0)):
            om, oph = omega_rule(KERN[k], C.A0_SI[f], z)
            BUD[(f, k, t)] = dict(rule=om, phantom=oph, leftover=om - oph, limit=LIM[t], ok=om <= LIM[t])
            P(f"    {f:9s} {k:7s} {t}: Omega_ph {oph:.3f} + leftover {om - oph:.3f} = {om:.3f} vs {LIM[t]:.3f} -> {'pass' if om <= LIM[t] else 'FAIL'}")

# ================================================================================================ SPARC
R.banner("C2 / SPARC WITH THE RULE (CFG4's own statistic, exec'd read-only)")
g4 = exec_prefix("CFG4_galaxy_law.py", 'banner("K  CONTROLS')
GAL4, UPS, Rm, GB, GO, OK, WW, GI = (g4[k] for k in ("GAL", "UPS", "Rm", "GB", "GO", "OK", "WW", "GI"))
iu = int(np.argmin(np.abs(UPS - 0.61))); a0 = C.A0_SI["canonical"]; KPC_S = g4["KPC_S"]
gb, go, ok, ww = GB[:, iu], GO[:, iu], OK[:, iu], WW[:, iu]
gpred = np.where(ok, np.asarray(C.nu_mono(np.where(ok, gb, 1.0) / a0), float) * np.where(ok, gb, 1.0), 1.0)
gadd = np.zeros_like(gpred); touched = []
for i, g in enumerate(GAL4):
    m = g.get("meta") or {}
    if not m or m.get("L36", 0) <= 0:
        continue
    Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m.get("MHI", 0.0) * 1e9
    if math.log10(Ms) < 10.0:
        continue
    colour = "blue" if m.get("T", 1) >= 1 else "red"
    Mh = MCF * collapse(Ms, colour)
    fex = max(0.0, 1.0 - edge_phantom(Mb, "canonical", 0.40) / ((1 - FB) * Mh))
    if fex > 0:
        sel = GI == i
        gadd[sel] = fex * (1 - FB) * CU.G_SI * np.array([float(nfw_enclosed(Mh, rr / KPC_S)) for rr in Rm[sel]]) * CU.MSUN / Rm[sel] ** 2
        touched.append((g.get("name", str(i)), m.get("T"), round(math.log10(Ms), 2), round(fex, 2)))
r0 = np.log10(np.where(ok, go, 1.0)) - np.log10(gpred); r1 = np.log10(np.where(ok, go, 1.0)) - np.log10(gpred + gadd)
rms0 = float(np.sqrt(np.sum(ww * r0 ** 2) / np.sum(ww))); rms1 = float(np.sqrt(np.sum(ww * r1 ** 2) / np.sum(ww)))
check("C2 CONTROL: the SPARC rms without the rule reproduces CFG4's nu_mono canonical fit (0.1003 at Upsilon 0.61) to 0.003 dex",
      f"{len(GAL4)} galaxies: rms {rms0:.4f} at Upsilon {UPS[iu]:.2f}", abs(rms0 - 0.1003) <= 0.003)
P(f"    with the rule: rms {rms1:.4f} (change {rms1 - rms0:+.4f}); galaxies touched: {touched}")

# ================================================================================================ KiDS threshold
lms_grid = np.arange(10.0, 11.8, 0.01)
thr = next((lm for lm in lms_grid if (1 - FB) * MCF * collapse(10 ** lm, "red") > edge_phantom(10 ** lm * 1.1, "canonical", 0.40)), float("nan"))
P(f"\n    the red rule's leftover switches on at log M_* = {thr:.2f} (baryons 1.1 M_*, canonical); Brouwer+2021's isolated-lens top bin reaches 11.0")

# ================================================================================================ H1
okb = all(BUD[(f, k, "len")]["ok"] for f in C.FOOTS for k in KERN)
h1 = abs(rms1 - rms0) < 0.005 and okb and thr > 11.0
check("H1 [HEADLINE] THE RULE COSTS NO GATE: SPARC rms moves < 0.005 dex, the lenient budget still passes on all four cells, and the KiDS "
      "lens bins lie below the rule's threshold -- B's score stays 42/48" + ("  [MUTATE: collapse masses x 30]" if MUTATE else ""),
      f"SPARC d rms {rms1 - rms0:+.4f}; lenient budget " + ", ".join(f"{f[:3]}/{k}: {BUD[(f, k, 'len')]['rule']:.3f}" for f in C.FOOTS for k in KERN)
      + f" (limit {LIM['len']:.3f}); threshold log M_* {thr:.2f} vs 11.0", h1)
check("H2 (reported) the strict budget with the rule; the leftover's share of Omega_c",
      "; ".join(f"{f[:3]}/{k}: strict {BUD[(f, k, 'str')]['rule']:.3f} vs {LIM['str']:.3f}; leftover {BUD[(f, k, 'len')]['leftover']:.3f} (lenient)" for f in C.FOOTS for k in KERN),
      True, load_bearing=False)
kf = []
for lm in (10.15, 10.45, 10.7, 10.9):                                           # Brouwer+2021's four isolated-lens bins (centres)
    Ms = 10 ** lm; Mh = MCF * collapse(Ms, "red")
    kf.append((lm, round(max(0.0, 1.0 - edge_phantom(1.1 * Ms, "canonical", 0.40) / ((1 - FB) * Mh)), 3), round(f_red(lm), 2)))
check("R1 (reported; POST-HOC, added after the main run) the red leftover fraction f_ex at the KiDS lens-bin centres, and Mandelbaum's red fraction there",
      "; ".join(f"log M* {a}: f_ex(red) {b}, red fraction {c}" for a, b, c in kf), True, load_bearing=False)
R.num("kids_fex_red", kf)
reading = "B adopts the derived conservation rule at no cost to its harness (42/48)" if h1 else "adopting the rule costs a gate (see H1)"
P(f"\n    READING (declared): {reading}")
R.num("budget", {f"{a}|{b}|{c}": v for (a, b, c), v in BUD.items()}); R.num("sparc", dict(rms0=rms0, rms1=rms1, touched=touched))
R.num("kids_threshold_logMs", thr); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
