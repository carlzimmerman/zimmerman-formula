#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG23d -- POST-HOC DIAGNOSTICS OF CFG23 (written and run AFTER CFG23's main run; nothing here was pre-declared except V1's
tolerance, and no check below is scored as a hypothesis -- V1 is a control, V2-V4 are reported numbers).

WHY.  CFG23's LCDM control failed KiDS (chi^2 174 vs the framework's 105) and still showed a larger KiDS-LG tension than the
framework.  Before any of that is read, three things need a committed script: that the NFW projection is right (V1), where the
LCDM misfit sits in radius (V2), how the KiDS chi^2 depends on the control's concentration and truncation (V3).  V4 puts a number
on a point CFG21's README states only in words -- KiDS wants the phantom far past the cold budget's edge -- by scoring the budget's
edge against KiDS's own best edge, i.e. with CFG21's statistic rather than CFG4's tolerance (+9 against the untruncated law).

  V1  CONTROL [MUTATE must fail]  FIX's projection of an untruncated NFW equals the analytic Delta Sigma (Wright & Brainerd 2000)
      within 1e-3 at every data radius, for three halos (log M200m 12.0 / 12.6 / 13.2; Duffy c x 1 / 1 / 0.7).
  V2  (reported) the misfit by radius band (R < 0.15, 0.15-0.6, >= 0.6 Mpc; diagonal chi^2 summed over bins, mean pull per bin)
      for CFG23's LCDM fits (x_t 1 / 4 / inf at Duffy c; x_t 1 at c x 0.7 / x 1.4) and the framework (canonical P2: CFG21's KiDS
      best edge 0.62 and untruncated).
  V3  (reported) CFG23's KiDS chi^2 on its whole (c, x_t) grid, Tinker caps; the best variant.
  V4  (reported) the KiDS cost of the cold budget's edge (CFG17's committed edge_A; CFG16's self-consistent caps) against KiDS's own
      best (CFG21's kids_min), every footing and kernel; the cost at CFG16's floor is 9 - kids_min by the floor's definition.
MUTATE=1: V1's analytic side uses half the concentration -- V1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG23_diagnostics.py   (MUTATE=1 for the control; ~30 s)
"""
import os, sys, math, json, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG23_diagnostics", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the analytic NFW uses c/2 -- V1 must FAIL ***")
np.seterr(all="ignore")

# ================================================================================================ CFG23's machinery, exec'd read-only up to its fits
C23P = os.path.join(HERE, "CFG23_lcdm_control.py")
src = open(C23P).read()
cut = src.index("# ================================================================================================ H1 (first-written) + H2 (first-written)")
g = {"__file__": C23P, "__name__": "cfg23_prefix"}
_sink = io.StringIO()
with contextlib.redirect_stdout(_sink):
    exec(compile(src[:cut], C23P, "exec"), g)
FIX, RRK, MPCK, MSK, RPK, Rd, Ed, Sd = (g[k] for k in ("FIX", "RRK", "MPCK", "MSK", "RPK", "Rd", "Ed", "Sd"))
M_nfw_msun, c_duffy, RHOMZ, PB, kfit_best, per_bin, Ci, DAT, XT, CF = (
    g[k] for k in ("M_nfw_msun", "c_duffy", "RHOMZ", "PB", "kfit_best", "per_bin", "Ci", "DAT", "XT", "CF"))
ns = g["ns"]
C = g["C"]
C21 = g["C21"]
C17 = json.load(open(os.path.join(HERE, "CFG17_budget_xgass_results.json")))["numbers"]["RES"]
BASE = ns["BASE"]


# ================================================================================================ V1
R.banner("V1  CONTROL: FIX's NFW projection against the analytic Delta Sigma")


def dsig_nfw(Rm, M200, c):
    """Wright & Brainerd (2000) Delta Sigma [Msun/pc^2] of an untruncated NFW (R in physical Mpc, Delta = 200 x mean at z_l)."""
    R200 = (3 * M200 / (4 * math.pi * 200 * RHOMZ)) ** (1 / 3); rs = R200 / c
    rhos = M200 / (4 * math.pi * rs ** 3 * (math.log1p(c) - c / (1 + c)))
    x = np.asarray(Rm, float) / rs
    F = np.ones_like(x)
    lo, hi = x < 1, x > 1
    F[lo] = np.arctanh(np.sqrt((1 - x[lo]) / (1 + x[lo]))) * 2 / np.sqrt(1 - x[lo] ** 2)
    F[hi] = np.arctan(np.sqrt((x[hi] - 1) / (1 + x[hi]))) * 2 / np.sqrt(x[hi] ** 2 - 1)
    Sig = 2 * rhos * rs / (x ** 2 - 1) * (1 - F)
    Sbar = 4 * rhos * rs / x ** 2 * (np.log(x / 2) + F)
    return (Sbar - Sig) / 1e12


dmax = 0.0
for lm2, cf in ((12.0, 1.0), (12.6, 1.0), (13.2, 0.7)):
    M200 = 10 ** lm2; c = cf * float(c_duffy(M200))
    num = FIX(M_nfw_msun(RRK / MPCK, lm2, float("inf"), cf) * MSK, 0.0)
    for b in range(4):
        n_ = np.interp(Rd[b], RPK / MPCK, num)
        a_ = dsig_nfw(Rd[b], M200, c / 2 if MUTATE else c)
        dmax = max(dmax, float(np.max(np.abs(n_ / a_ - 1))))
    P(f"    log M200m {lm2}, c {c:.2f}: FIX / analytic at R = 0.035 / 0.164 / 0.762 / 2.604 Mpc: " + " / ".join(
        f"{float(np.interp(r, RPK / MPCK, num)) / float(dsig_nfw(np.array([r]), M200, c / 2 if MUTATE else c)[0]):.4f}"
        for r in (Rd[0][0], Rd[0][5], Rd[0][10], Rd[0][-1])))
check("V1 CONTROL: FIX's projection of an untruncated NFW equals the analytic Delta Sigma within 1e-3 at every data radius" +
      ("  [MUTATE: c/2]" if MUTATE else ""), f"max |FIX/analytic - 1| = {dmax:.2e}", dmax < 1e-3)

# ================================================================================================ V2
R.banner("V2  WHERE THE MISFIT SITS (reported)")


def pattern(mods):
    dv = DAT - np.concatenate(mods)
    bands, pulls = np.zeros(3), []
    for b in range(4):
        r = Rd[b]; e = (Ed[b] - mods[b]) / Sd[b]
        m0, m1, m2 = r < 0.15, (r >= 0.15) & (r < 0.6), r >= 0.6
        bands += [np.sum(e[m0] ** 2), np.sum(e[m1] ** 2), np.sum(e[m2] ** 2)]
        pulls.append((float(np.mean(e[m1])), float(np.mean(e[m2]))))
    return dict(chi2=float(dv @ Ci @ dv), bands=[float(v) for v in bands], pull_mid=[p[0] for p in pulls], pull_out=[p[1] for p in pulls])


V2 = {}
for cf, xt in ((1.0, 1.0), (1.0, 4.0), (1.0, float("inf")), (0.7, 1.0), (1.4, 1.0)):
    pb = PB[(cf, xt, "T")]; _, ks = kfit_best(pb)
    V2[f"LCDM c x{cf} x_t {xt}"] = pattern([pb[b]["mod"][ks[b]] for b in range(4)])
xk = C21["canonical|P2|1.145e+11"]["kids_best_x"]
Tx = ns["table"](ns["M_trunc_xta"](ns["KERN"]["P2"], xk), "canonical")
pbx = per_bin(Tx[0][None], np.array([ns["caps_at"]("canonical", "P2", xk)]))
V2[f"framework P2 x_e {xk}"] = pattern([pbx[b]["mod"][0] for b in range(4)])
Tu = ns["table"](ns["M_law"](ns["KERN"]["P2"]), "canonical")
pbu = per_bin(Tu[0][None], np.zeros((1, 4)))
V2["framework P2 untruncated"] = pattern([pbu[b]["mod"][0] for b in range(4)])
for k, v in V2.items():
    P(f"    {k:28s}: chi^2 {v['chi2']:7.2f}; diagonal chi^2 R<0.15 / 0.15-0.6 / >=0.6 Mpc: " + " / ".join(f"{x:.1f}" for x in v["bands"]) +
      "; mean pull (data - model)/sigma, 0.15-0.6: " + ", ".join(f"{x:+.2f}" for x in v["pull_mid"]) + "; >=0.6: " +
      ", ".join(f"{x:+.2f}" for x in v["pull_out"]))
check("V2 (reported) the misfit by radius band, LCDM and the framework", "; ".join(
    f"{k}: >=0.6 Mpc {v['bands'][2]:.1f}" for k, v in V2.items()), True, load_bearing=False)

# ================================================================================================ V3
R.banner("V3  CFG23's KiDS chi^2 OVER ITS (c, x_t) GRID (reported)")
V3 = {f"c x{cf}|x_t {xt}": kfit_best(PB[(cf, xt, "T")])[0] for cf in CF for xt in XT}
for cf in CF:
    P(f"    c x{cf}: " + ", ".join(f"x_t {xt}: {V3[f'c x{cf}|x_t {xt}']:.1f}" for xt in XT))
kb = min(V3, key=V3.get)
fwb = BASE[("canonical", "P2")] + C21["canonical|P2|1.145e+11"]["kids_min"]
check("V3 (reported) the best LCDM variant on CFG23's grid against the framework's best", f"{kb}: {V3[kb]:.2f}; framework (canonical "
      f"P2, CFG21) {fwb:.2f}", True, load_bearing=False)

# ================================================================================================ V4
R.banner("V4  THE COLD BUDGET'S EDGE AGAINST KiDS's OWN BEST (CFG21's statistic; reported)")
V4 = {}
for f in C.FOOTS:
    for kn in ns["KERN"]:
        e = C17[f"{f}|{kn}"]["edge_A"]; fl = C17[f"{f}|{kn}"]["floor"]
        best = BASE[(f, kn)] + C21[f"{f}|{kn}|1.145e+11"]["kids_min"]
        ce = ns["kfit_caps"](ns["table"](ns["M_trunc_xta"](ns["KERN"][kn], e), f), ns["caps_at"](f, kn, e))
        ce = ce[0] if isinstance(ce, tuple) else ce
        V4[f"{f}|{kn}"] = dict(edge=e, floor=fl, chi2_edge=float(ce), chi2_best=best, cost_edge=float(ce - best),
                               cost_floor_def=float(9.0 - C21[f"{f}|{kn}|1.145e+11"]["kids_min"]), vs_untruncated=float(ce - BASE[(f, kn)]))
        v = V4[f"{f}|{kn}"]
        P(f"    {f:9s} {kn:8s}: budget edge x_e {e:.4f} (CFG16 floor {fl:.4f}): chi^2 {v['chi2_edge']:.2f} ({v['vs_untruncated']:+.2f} vs the "
          f"untruncated law) against KiDS's best {best:.2f} -> cost {v['cost_edge']:.1f} (~{math.sqrt(max(v['cost_edge'], 0)):.1f} sigma); "
          f"at the floor, by definition, {v['cost_floor_def']:.1f}")
check("V4 (reported) the KiDS cost of the cold budget's edge against KiDS's own best edge", "; ".join(
    f"{k}: {v['cost_edge']:.1f}" for k, v in V4.items()), True, load_bearing=False)
R.num("V1", dict(max_rel=dmax)); R.num("V2", V2); R.num("V3", V3); R.num("V4", V4)
nf = R.write()
sys.exit(1 if nf else 0)
