#!/usr/bin/env python3
"""
L2 -- THE CLUSTER INVERSE PROBLEM: solve for the kernel clusters demand, then ask if it is admissible
=========================================================================================================
Every cluster verdict in this programme so far has been FORWARD: propose a source or a kernel, compute what it
gives, watch it fail (g03r/g03s/g03u atmosphere scans; g04a-g04j relic and condensate pincers).  The INVERSE
problem has not been run.  This script runs it.

THE INVERSION.  The programme's static law is  div[ J_Y(|grad phi|) grad phi ] = grad^2 Psi, with the boost written
g_phi = a0 Delta(s), s = g_N/a0 (PAPER5 sec. "The carrier theorem is the bounded-boost theorem").  On a sphere the
divergence integrates EXACTLY by Gauss's theorem, so the field equation collapses to the pointwise algebraic relation

        J_Y(g_phi) g_phi = g_N        i.e.        g_obs(r) = g_N(r) + a0 Delta( g_N(r)/a0 ).

There is therefore no differential inverse problem to solve and no regularisation to choose: at every radius of every
cluster the required boost is read off directly,

        Delta_req( s_i )  =  ( g_HSE,i - g_bar,i ) / a0 ,      s_i = g_bar,i / a0 ,

and this Delta_req, by construction, reproduces the observed enclosed-mass profile M_HSE(<r) EXACTLY from the baryons
alone (M(<r) = g r^2/G, so matching g at every r matches M at every r).  The whole content of the lane is then the
question the forward runs never asked: IS THAT FUNCTION ADMISSIBLE?

Inputs, not retyped: the corrected X-COP rows of the lead's radius-unit audit,
  qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json  ('rows': g_hse_over_a0,
  g_baryon_over_a0 per cluster, radius and footing; 'radius_audit': each cluster's own R500; 'a0_m_s2': both footings),
loaded exactly as g03u_xcop_corrected_vs_atmosphere.py loads them.  Galaxies: the SPARC Rotmod files and Table 1 cuts
(Q < 3, i > 30 deg, Upsilon_disk = 0.5, Upsilon_bul = 0.7 at 3.6um) read exactly as g03u_bounded_boost_theorem.py
reads them, from real_research/data/sparc_data/*_rotmod.dat and real_research/data/SPARC_Lelli2016c.mrt.

Checks that can fail.  Each states a PROPOSITION; PASS means the proposition holds.
  C0 [machinery]  round trip: a synthetic cluster built FROM the carried kernel, pushed through this inversion,
                  returns the carried kernel to machine precision.  (The machinery is not broken.)
  C1 [control]    the programme's CARRIED kernel (nu_RAR, saturated) run through the same machinery reproduces the
                  known cluster shortfall: M_HSE/M_pred in [1.5, 3.0] at the outermost audited radius, both footings.
  C2 [function]   the required Delta_req is single-valued in s: pooled within-bin scatter across clusters < 0.30 dex.
                  (A necessary condition for ANY kernel of the class to exist.)
  C3 [stiffness]  the required Delta_req is non-decreasing in s, so the longitudinal stiffness dg_N/dg_phi = 1/Delta'
                  stays positive and the static problem stays well posed (PAPER5's admissibility condition).
  C4 [bounded]    the required Delta_req respects the bounded-boost ceiling C_max = sup Delta of the kernel family.
  C5 [THE TEST]   at the accelerations where clusters and galaxies OVERLAP, the required cluster Delta agrees with the
                  MEASURED galaxy Delta within 3 sigma in every bin.  No kernel is assumed on either side: both are
                  measurements.  PASS = one kernel can serve both = a live candidate.  FAIL = clean impossibility.
  C6 [solar]      the MINIMAL continuation the stiffness gate permits (Delta non-decreasing, hence Delta >= its cluster
                  maximum for all larger s) stays under the cited Saturn residual-acceleration bound 7.0e-15 m/s^2.
  C7 [RAR feed]   feeding the required Delta_req back to the SPARC points inside the overlap band reproduces the
                  observed accelerations to better than 0.10 dex median offset.
  C8 [escape]     the nonthermal support that would reconcile the two requires sigma_1D <= 2x the Hitomi Perseus
                  measurement 164 +/- 10 km/s.
  C9 [shape]      the required Delta has the LOG-SLOPE of a kernel of the class.  Any Delta = s[nu(s) - 1] with a
                  deep-MOND limit obeys d log Delta / d log s <= 1/2 everywhere (the slope starts at 1/2 as s -> 0 and
                  falls through 0 at the ceiling), which is verified numerically here for the five family members over
                  the cluster range.  A fitted p above 1/2 therefore has no kernel of the class; p = 1 is the opposite
                  extreme, g_phi = A g_N with a0 cancelling out -- a constant rescaling of G, i.e. extra MASS.
Both footings (a0 = 9.3619e-11 canonical, 1.1279e-10 alt) and both cluster subsets (all twelve; the seven that ship a
measured stellar profile, which carry the headline as in g04a/g03u) throughout.
"""
import numpy as np, math, json, os, sys, glob, time

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, ".."))
kpc = 3.0857e19; G = 6.674e-11; MSUN = 1.989e30
KEV = 1.602176634e-16; MP = 1.67262192e-27; MU = 0.61                      # for the nonthermal-support escape
DG_SATURN = 7.0e-15                                                        # cited 1-sigma residual-acceleration bound (prep_2026 laneR/BOUNDS.md)
SIG_HITOMI = 164.0                                                         # Hitomi Perseus 1-D turbulent velocity, km/s
RNG = np.random.default_rng(20260908)

print("=" * 122); print("L2 -- the cluster inverse problem: the Delta(s) clusters require, and whether it is admissible"); print("=" * 122, flush=True)

# ---------------------------------------------------------------- inputs (g03u's loader, not retyped numbers)
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
ROWS = CLJ["rows"]; RADII = np.array(CLJ["radii_kpc"], float); A0 = CLJ["a0_m_s2"]
R500 = {d["name"]: d["own_R500_kpc"] for d in CLJ["radius_audit"]}
print(f"\n  inputs: {len(ROWS)} corrected X-COP rows, {len(set(r['cluster'] for r in ROWS))} clusters, radii {RADII.astype(int).tolist()} kpc,")
print(f"          footings {A0}; source: closure_2026/cluster_measurement_audit_2026/results.json (the lead's radius-unit audit)")
print(f"          R500 per cluster: {min(R500.values()):.0f}-{max(R500.values()):.0f} kpc (median {np.median(list(R500.values())):.0f})", flush=True)

# ---------------------------------------------------------------- the kernels of the class
E = math.e
def Delta_RAR(s):                                                          # the CARRIED kernel (nu_RAR, saturated: THE_ACTION sec 3, g04k)
    s = np.asarray(s, float); sc = np.clip(s, 1e-300, 1e4)
    d = np.where(s > 0, sc/np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > 2.540, 0.6476, d)
_YT = np.logspace(-7, 7, 400001); _SN = _YT*(1 - np.exp(-_YT))
def Delta_carrier(s):                                                      # the exponential carrier, completed (g03j / PAPER5 B1): saturates at 1/e
    s = np.asarray(s, float); y = np.interp(s, _SN, _YT)
    return np.where(s <= 1 - 1/E, y*np.exp(-y), 1/E)
def Delta_simple(s):  s = np.asarray(s, float); return s*((1 + np.sqrt(1 + 4/np.maximum(s, 1e-300)))/2 - 1)
def Delta_standard(s):s = np.asarray(s, float); return s*(np.sqrt((1 + np.sqrt(1 + 4/np.maximum(s, 1e-300)**2))/2) - 1)
def Delta_dmond(s):   s = np.asarray(s, float); return np.maximum(np.sqrt(s) - s, 0.0)   # nu = y^-1/2 capped at Newtonian
FAM = {"carrier (exp, completed)": Delta_carrier, "nu_RAR (CARRIED)": Delta_RAR, "simple mu": Delta_simple,
       "standard mu": Delta_standard, "deep-MOND sqrt (capped)": Delta_dmond}
sg = np.logspace(-7, 7, 2000001); CS = {k: float(np.nanmax(f(sg))) for k, f in FAM.items()}
CMAX = max(CS.values())
print("\n  the kernel family and its bounded-boost ceilings C = sup_s Delta(s)  (PAPER5 B2 reports [0.250, 1.000]):")
for k, v in CS.items(): print(f"      {k:28s} C = {v:.4f}")
print(f"      widest ceiling of the family: C_max = {CMAX:.4f}", flush=True)

# ---------------------------------------------------------------- C0: the machinery, round-tripped
syn_s = np.array([r["g_baryon_over_a0"] for r in ROWS if r["footing"] == "canonical"])
syn_gh = syn_s + Delta_RAR(syn_s)                                          # a synthetic cluster set built FROM the carried kernel
syn_back = syn_gh - syn_s                                                  # ... pushed through the inversion
err0 = float(np.max(np.abs(syn_back - Delta_RAR(syn_s))))
check("C0 [machinery] a synthetic cluster set built from the CARRIED kernel and pushed through this inversion returns that kernel exactly (round trip)",
      err0 < 1e-12, f"max |Delta_recovered - Delta_RAR| = {err0:.1e} over {len(syn_s)} rows")

# ---------------------------------------------------------------- the inversion, per row
def pick(foot, subset):
    return [r for r in ROWS if r["footing"] == foot and (subset == "all" or r["stellar_file_present"])]
INV = {}
for foot in A0:
    for subset in ("all", "stellar"):
        R_ = pick(foot, subset)
        INV[(foot, subset)] = dict(
            s   = np.array([r["g_baryon_over_a0"] for r in R_]),
            D   = np.array([r["g_hse_over_a0"] - r["g_baryon_over_a0"] for r in R_]),
            gh  = np.array([r["g_hse_over_a0"] for r in R_]),
            r   = np.array([r["r_kpc"] for r in R_]),
            cl  = np.array([r["cluster"] for r in R_]))
sC = INV[("canonical", "stellar")]["s"]
print(f"\n  the acceleration range clusters actually probe (canonical, seven with stellar profiles): s = g_bar/a0 from {sC.min():.3f} to {sC.max():.3f}", flush=True)

# ---------------------------------------------------------------- C1: the control -- the carried kernel through the same machinery
print("\n  C1  CONTROL: the carried kernel (nu_RAR) and the exponential carrier, run through this machinery, against the audited profile.")
print("      shortfall factor = M_HSE(<r) / M_pred(<r) = g_HSE / (g_bar + a0 Delta_kernel(g_bar/a0))   [enclosed mass ~ g r^2 at fixed r]")
SHORT = {}
for foot in A0:
    for subset in ("all", "stellar"):
        d = INV[(foot, subset)]; out = []
        for rk in RADII:
            m = d["r"] == rk
            if m.sum() == 0: out.append(np.nan); continue
            sf = d["gh"][m]/(d["s"][m] + Delta_RAR(d["s"][m])); out.append(float(np.median(sf)))
        SHORT[(foot, subset)] = np.array(out)
        if subset == "stellar":
            print(f"      {foot:9s} stellar-7 : " + "  ".join(f"{rk:.0f}kpc {v:.2f}x" for rk, v in zip(RADII, out)), flush=True)
r_out = RADII[-1]; frac_R500 = r_out/np.median(list(R500.values()))
ctrl = {(f, s_): SHORT[(f, s_)][-1] for f in A0 for s_ in ("all", "stellar")}
check("C1 [control] the CARRIED kernel run through this inversion machinery reproduces the known cluster shortfall of about a factor 2 at the outermost audited radius, at both footings and both subsets",
      all(1.5 <= v <= 3.0 for v in ctrl.values()),
      f"M_HSE/M_pred at r = {r_out:.0f} kpc = {frac_R500:.2f} R500(median): " + ", ".join(f"{f}/{s_} {v:.2f}x" for (f, s_), v in ctrl.items()))

# ---------------------------------------------------------------- SPARC (g03u_bounded_boost's loader)
T1 = {}
for ln in open(os.path.join(REPO, "real_research/data/SPARC_Lelli2016c.mrt")):
    p = ln.split()
    if len(p) >= 18:
        try: T1[p[0]] = (int(p[17]), float(p[5]))
        except ValueError: pass
gobs, gbar, gstar, sgo, gnames, grads = [], [], [], [], [], []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6)); gname = os.path.basename(fn)[:-11]
    if gname in T1 and not (T1[gname][0] < 3 and T1[gname][1] > 30.0): continue
    m = (r > 0) & (Vo > 0) & (eV > 0) & (eV/Vo < 0.10)
    if m.sum() == 0: continue
    rk = r[m]; r_, Vo_, eV_, Vg_, Vd_, Vb_ = rk*kpc, Vo[m]*1e3, eV[m]*1e3, Vg[m]*1e3, Vd[m]*1e3, Vb[m]*1e3
    Vst2 = 0.5*Vd_**2 + 0.7*Vb_**2; Vbar2 = np.sign(Vg_)*Vg_**2 + Vst2; ok = Vbar2 > 0
    gobs.append(Vo_[ok]**2/r_[ok]); gbar.append(Vbar2[ok]/r_[ok]); gstar.append(Vst2[ok]/r_[ok])
    sgo.append(2*Vo_[ok]*eV_[ok]/r_[ok]); gnames += [gname]*int(ok.sum()); grads.append(rk[ok])
gobs = np.concatenate(gobs); gbar = np.concatenate(gbar); gstar = np.concatenate(gstar)
sgo = np.concatenate(sgo); gnames = np.array(gnames); grads = np.concatenate(grads)
sig_g = np.sqrt(sgo**2 + (0.26*gstar)**2)                                  # velocity error + 0.1 dex Upsilon (as g03u)
print(f"\n  SPARC: {len(set(gnames))} galaxies, {len(gobs)} points (Q<3, i>30, eV/V<0.10); file real_research/data/sparc_data/*_rotmod.dat", flush=True)

# ---------------------------------------------------------------- binning + cluster/galaxy bootstraps
NB = 7
def boot_median(vals, groups, nb=2000):
    """median with a bootstrap standard error resampled over GROUPS (clusters, or galaxies), not points."""
    if len(vals) == 0: return np.nan, np.nan
    uq = np.unique(groups); idx = {g: np.where(groups == g)[0] for g in uq}
    med = float(np.median(vals)); draws = np.empty(nb)
    for b in range(nb):
        pick_ = RNG.choice(uq, size=len(uq), replace=True)
        draws[b] = np.median(np.concatenate([vals[idx[g]] for g in pick_]))
    return med, float(np.std(draws))

def binned(s, v, groups, edges):
    out = []
    for i in range(len(edges) - 1):
        m = (s >= edges[i]) & (s < edges[i + 1])
        if m.sum() < 5 or len(np.unique(groups[m])) < 3: out.append(None); continue
        med, se = boot_median(v[m], groups[m])
        out.append(dict(lo=edges[i], hi=edges[i+1], n=int(m.sum()), ngrp=int(len(np.unique(groups[m]))),
                        smed=float(np.median(s[m])), med=med, se=se,
                        p16=float(np.percentile(v[m], 16)), p84=float(np.percentile(v[m], 84))))
    return out

# ---------------------------------------------------------------- the required Delta(s): the answer to the inverse problem
print("\n" + "-" * 122)
print("  THE REQUIRED Delta(s).  Delta_req(s) = (g_HSE - g_bar)/a0 at s = g_bar/a0, per cluster per radius, binned in s.")
print("  This Delta reproduces the corrected X-COP enclosed-mass profile EXACTLY from the baryons alone, by construction.")
print("-" * 122)
BINS = {}; FIT = {}
for foot in A0:
    for subset in ("all", "stellar"):
        d = INV[(foot, subset)]
        edges = np.geomspace(max(d["s"].min()*0.999, 1e-3), d["s"].max()*1.001, NB + 1)
        BINS[(foot, subset)] = binned(d["s"], d["D"], d["cl"], edges)
        # power-law fit Delta = A s^p on the point cloud, with a cluster-level bootstrap on (A, p)
        lo, lp = np.log10(d["s"]), np.log10(np.maximum(d["D"], 1e-6))
        p_, la_ = np.polyfit(lo, lp, 1); rms = float(np.sqrt(np.mean((lp - (p_*lo + la_))**2)))
        uq = np.unique(d["cl"]); idx = {g: np.where(d["cl"] == g)[0] for g in uq}; dr = np.empty((800, 2))
        for b in range(800):
            k = np.concatenate([idx[g] for g in RNG.choice(uq, size=len(uq), replace=True)])
            dr[b] = np.polyfit(lo[k], lp[k], 1)
        FIT[(foot, subset)] = dict(p=float(p_), A=float(10**la_), rms=rms, sp=float(np.std(dr[:, 0])), sA=float(np.std(10**dr[:, 1])))
for foot in A0:
    for subset in ("all", "stellar"):
        lbl = "all 12" if subset == "all" else "stellar 7"
        print(f"\n  {foot} footing, {lbl} clusters:")
        print(f"    {'s bin':>17s} {'N':>4s} {'ncl':>4s} {'med s':>8s} {'Delta_req':>11s} {'+/- (boot)':>11s} {'16-84 pct':>15s} "
              f"{'D_nuRAR':>9s} {'D_carr':>8s} {'ratio/RAR':>10s} {'J_Y=s/D':>9s}")
        for b in BINS[(foot, subset)]:
            if b is None: continue
            dr_ = float(Delta_RAR(b["smed"])); dc_ = float(Delta_carrier(b["smed"]))
            print(f"    {b['lo']:7.4f}-{b['hi']:7.4f} {b['n']:4d} {b['ngrp']:4d} {b['smed']:8.4f} {b['med']:11.3f} {b['se']:11.3f} "
                  f"  [{b['p16']:5.2f},{b['p84']:5.2f}] {dr_:9.3f} {dc_:8.3f} {b['med']/dr_:10.2f} {b['smed']/b['med']:9.4f}")
        f_ = FIT[(foot, subset)]
        print(f"    power-law fit over the cluster range: Delta_req = ({f_['A']:.2f} +/- {f_['sA']:.2f}) s^({f_['p']:.3f} +/- {f_['sp']:.3f}), "
              f"rms {f_['rms']:.3f} dex about the point cloud", flush=True)
HEAD = ("canonical", "stellar")
print(f"\n  the fit is the headline of the lane: Delta_req = A s^p with p = {FIT[HEAD]['p']:.3f} +/- {FIT[HEAD]['sp']:.3f} and A = {FIT[HEAD]['A']:.2f} +/- {FIT[HEAD]['sA']:.2f}.")
print(f"  Since g_phi = a0 Delta = A a0^(1-p) g_N^p, p = 1 makes a0 CANCEL: the requirement would then be g_phi = A g_N, a constant")
print(f"  rescaling of G by 1+A -- extra MASS tracing the baryons, not an interpolation function with an acceleration scale.", flush=True)

# ---------------------------------------------------------------- C2, C3, C4: admissibility of the required Delta
bh = [b for b in BINS[HEAD] if b is not None]
scat = []
for foot in A0:
    for subset in ("all", "stellar"):
        d = INV[(foot, subset)]
        for b in BINS[(foot, subset)]:
            if b is None: continue
            m = (d["s"] >= b["lo"]) & (d["s"] < b["hi"]); v = np.log10(np.maximum(d["D"][m], 1e-6))
            scat.append(np.sqrt(np.mean((v - np.median(v))**2)))
pool = float(np.sqrt(np.mean(np.array(scat)**2)))
check("C2 [function] the required Delta_req is single-valued in s to better than 0.30 dex: a necessary condition for ANY kernel Delta(s) of the class to reproduce clusters",
      pool < 0.30, f"pooled within-bin rms across clusters = {pool:.3f} dex (all bins, both footings, both subsets)")

mono_ok, mono_detail = True, []
for foot in A0:
    for subset in ("all", "stellar"):
        bb = [b for b in BINS[(foot, subset)] if b is not None]
        worst = min((bb[i+1]["med"] - bb[i]["med"])/max(bb[i]["se"], 1e-9) for i in range(len(bb)-1))
        mono_detail.append(f"{foot}/{subset} worst step {worst:+.2f} sigma"); mono_ok &= worst > -1.0
check("C3 [stiffness] the required Delta_req is non-decreasing in s, so the longitudinal stiffness dg_N/dg_phi = 1/Delta'(s) stays positive and the static field problem stays well posed",
      mono_ok, "; ".join(mono_detail))

Dmax = max(b["med"] for foot in A0 for subset in ("all", "stellar") for b in BINS[(foot, subset)] if b is not None)
Dmax_head = max(b["med"] for b in bh)
check("C4 [bounded] the required Delta_req respects the bounded-boost ceiling of the kernel family, so some interpolation function of the class can supply it",
      Dmax <= CMAX, f"max required Delta = {Dmax:.2f} (headline stellar-7 canonical {Dmax_head:.2f}) against the widest ceiling C_max = {CMAX:.3f}: over by {Dmax/CMAX:.1f}x")

# ---------------------------------------------------------------- C5: THE TEST -- clusters vs galaxies at the same s
print("\n" + "-" * 122)
print("  C5  THE TEST.  Both sides are MEASUREMENTS of the same quantity Delta = (g_obs - g_bar)/a0 at the same s = g_bar/a0.")
print("      No kernel is assumed on either side.  If a single-valued Delta(s) exists, the two columns must agree.")
print("-" * 122)
sgal = gbar/A0["canonical"]; Dgal = (gobs - gbar)/A0["canonical"]
OVER = {}
for foot in A0:
    a0 = A0[foot]; sgal_f = gbar/a0; Dgal_f = (gobs - gbar)/a0
    for subset in ("all", "stellar"):
        rowsout = []
        for b in BINS[(foot, subset)]:
            if b is None: continue
            m = (sgal_f >= b["lo"]) & (sgal_f < b["hi"])
            if m.sum() < 20 or len(np.unique(gnames[m])) < 10: continue
            gm, gse = boot_median(Dgal_f[m], gnames[m])
            z = (b["med"] - gm)/math.sqrt(b["se"]**2 + gse**2)
            rowsout.append(dict(b=b, gm=gm, gse=gse, ngal=int(len(np.unique(gnames[m]))), npt=int(m.sum()), z=z, ratio=b["med"]/gm))
        OVER[(foot, subset)] = rowsout
for foot in A0:
    for subset in ("all", "stellar"):
        lbl = "all 12" if subset == "all" else "stellar 7"
        print(f"\n  {foot} footing, {lbl} clusters vs SPARC galaxies, same s:")
        print(f"    {'s bin':>17s} {'med s':>8s} | {'Delta_cluster':>15s} {'ncl':>4s} | {'Delta_galaxy':>15s} {'ngal':>5s} {'npt':>5s} | {'ratio':>7s} {'z':>8s}")
        for o in OVER[(foot, subset)]:
            b = o["b"]
            print(f"    {b['lo']:7.4f}-{b['hi']:7.4f} {b['smed']:8.4f} | {b['med']:8.3f} +/-{b['se']:5.3f} {b['ngrp']:4d} | "
                  f"{o['gm']:8.3f} +/-{o['gse']:5.3f} {o['ngal']:5d} {o['npt']:5d} | {o['ratio']:7.2f} {o['z']:+8.1f}")
allz = [o["z"] for k in OVER for o in OVER[k]]
compat = all(abs(z) < 3 for z in allz)
zh = [o["z"] for o in OVER[HEAD]]; rh = [o["ratio"] for o in OVER[HEAD]]
check("C5 [THE TEST] at the accelerations where clusters and galaxies overlap the required cluster Delta agrees with the measured galaxy Delta within 3 sigma in every bin, so ONE Delta(s) can serve both (a live candidate kernel)",
      compat, f"headline (canonical, stellar-7): ratios cluster/galaxy {['%.1f' % x for x in rh]}, z = {['%+.0f' % x for x in zh]}; "
              f"worst over all footings and subsets |z| = {max(abs(np.array(allz))):.0f}, ratio range {min(o['ratio'] for k in OVER for o in OVER[k]):.1f}-{max(o['ratio'] for k in OVER for o in OVER[k]):.1f}")
print("      the ratio is a ratio of two directly measured accelerations, so a0 cancels out of it entirely and it is the same")
print("      number at both footings; the external field, which differs between a cluster outskirt and an isolated disc, acts")
print("      to SUPPRESS the boost in the denser environment, so including it widens this gap rather than closing it.")

# ---------------------------------------------------------------- C6: the Solar System
print("\n  C6  the Solar System.  Only the stiffness gate C3 is used, no extrapolation of the fit: Delta non-decreasing means")
print("      Delta(s) >= Delta(s_max,cluster) for every s above the cluster range, so the anomalous acceleration a0 Delta is")
print("      bounded BELOW by the cluster value all the way to Saturn.")
s_sat = {}
for foot, a0 in A0.items():
    gN_sat = G*1.989e30/(9.537*1.496e11)**2; s_sat[foot] = gN_sat/a0
    dmin = max(b["med"] for b in BINS[(foot, "stellar")] if b is not None)
    f_ = FIT[(foot, "stellar")]; dpl = f_["A"]*s_sat[foot]**f_["p"]
    print(f"      {foot:9s}: s(Saturn) = g_N/a0 = {s_sat[foot]:.3e};  minimal admissible Delta = {dmin:.2f} -> anomalous a = {dmin*a0:.2e} m/s^2 "
          f"= {dmin*a0/DG_SATURN:.1e}x the cited bound {DG_SATURN:.1e};  power-law continuation Delta = {dpl:.2e} -> {dpl*a0/DG_SATURN:.1e}x", flush=True)
worst6 = max(max(b["med"] for b in BINS[(f, 'stellar')] if b is not None)*A0[f] for f in A0)
check("C6 [solar] the minimal continuation the stiffness gate permits keeps the anomalous Solar-System acceleration under the cited Saturn residual bound 7.0e-15 m/s^2",
      worst6 <= DG_SATURN, f"minimal anomalous acceleration at Saturn = {worst6:.2e} m/s^2, i.e. {worst6/DG_SATURN:.1e}x the bound (no extrapolation of the fit is used)")

# ---------------------------------------------------------------- C7: feed the required Delta back to the galaxies
print("\n  C7  feeding the required Delta_req back to the SPARC points INSIDE the overlap band (log-log interpolation of the")
print("      binned cluster medians; no extrapolation): g_pred = g_bar + a0 Delta_req(g_bar/a0), compared with g_obs.")
FEED = {}
for foot in A0:
    a0 = A0[foot]
    for subset in ("all", "stellar"):
        bb = [b for b in BINS[(foot, subset)] if b is not None]
        xs = np.log10([b["smed"] for b in bb]); ys = np.log10([b["med"] for b in bb])
        sg_ = gbar/a0; m = (sg_ >= 10**xs.min()) & (sg_ <= 10**xs.max())
        dq = 10**np.interp(np.log10(sg_[m]), xs, ys)
        gpred = gbar[m] + a0*dq; off = np.log10(gpred/gobs[m])
        FEED[(foot, subset)] = (float(np.median(off)), float(np.sqrt(np.mean(off**2))), int(m.sum()), int(len(np.unique(gnames[m]))))
        print(f"      {foot:9s} {('all 12' if subset=='all' else 'stellar 7'):10s}: {m.sum()} SPARC points in {len(np.unique(gnames[m]))} galaxies -> "
              f"median offset {np.median(off):+.3f} dex, rms {np.sqrt(np.mean(off**2)):.3f} dex "
              f"(the carried kernel on the same points: {np.median(np.log10((gbar[m] + a0*Delta_RAR(sg_[m]))/gobs[m])):+.3f} dex)", flush=True)
check("C7 [RAR feed] the required cluster Delta_req, fed back to the SPARC points inside the overlap band, reproduces the observed accelerations to better than 0.10 dex median offset",
      all(abs(FEED[k][0]) < 0.10 for k in FEED), ", ".join(f"{k[0]}/{k[1]} {FEED[k][0]:+.3f} dex (rms {FEED[k][1]:.3f})" for k in FEED))

# ---------------------------------------------------------------- C8: the nonthermal escape, priced
print("\n  C8  the HSE escape, priced.  If the galaxy Delta is the true kernel, the HSE acceleration is over-estimated by")
print("      f = (g_bar + a0 Delta_gal)/g_HSE, and nonthermal support must carry the rest: sigma_1D^2 = (1-f)/f x kT/(mu m_p).")
kT = 5.0*KEV; v_th2 = kT/(MU*MP)
SIGREQ = {}
for foot in A0:
    for subset in ("stellar",):
        need = []
        for o in OVER[(foot, subset)]:
            b = o["b"]; f_ = (b["smed"] + o["gm"])/(b["smed"] + b["med"])
            need.append((b["smed"], f_, math.sqrt(max((1 - f_)/f_, 0)*v_th2)/1e3))
        SIGREQ[foot] = need
        print(f"      {foot:9s}: " + "; ".join(f"s={x:.3f}: f={y:.2f}, sigma_1D={z:.0f} km/s" for x, y, z in need), flush=True)
sig_worst = min(min(z for _, _, z in SIGREQ[f]) for f in A0)
check("C8 [escape] the nonthermal support that would reconcile clusters with the measured galaxy Delta is available: it needs sigma_1D no more than twice the Hitomi Perseus measurement of 164 +/- 10 km/s",
      sig_worst <= 2*SIG_HITOMI, f"the SMALLEST sigma_1D required in any overlap bin at either footing is {sig_worst:.0f} km/s = {sig_worst/SIG_HITOMI:.1f}x Hitomi (kT = 5 keV, mu = 0.61)")

# ---------------------------------------------------------------- C9: does the required Delta carry an acceleration scale?
print("\n  C9  the SHAPE gate.  Any Delta = s[nu(s)-1] with a deep-MOND limit has d log Delta/d log s -> 1/2 as s -> 0 and")
print("      falling to 0 at its ceiling, so its log-slope never exceeds 1/2.  Measured on the family over the cluster range:")
scl = np.geomspace(sC.min(), sC.max(), 400); SLOPE = {}
for k, f in FAM.items():
    v = np.log(np.maximum(f(scl), 1e-300)); SLOPE[k] = float(np.max(np.gradient(v, np.log(scl))))
    print(f"      {k:28s} max d log Delta/d log s over s in [{sC.min():.3f}, {sC.max():.3f}] = {SLOPE[k]:.3f}")
SLMAX = max(SLOPE.values())
zp = {k: (FIT[k]["p"] - 0.5)/FIT[k]["sp"] for k in FIT}
check("C9 [shape] the required Delta_req has the log-slope of a kernel of the class: the fitted p is not more than 3 sigma above the class ceiling of 1/2 (a p near 1 instead means g_phi = A g_N with a0 cancelling -- a constant rescaling of G, i.e. extra mass tracing the baryons, not an interpolation function)",
      all(v <= 3 for v in zp.values()),
      f"family max log-slope over the cluster range = {SLMAX:.3f}; required " +
      ", ".join(f"{k[0]}/{k[1]} p = {FIT[k]['p']:.3f} +/- {FIT[k]['sp']:.3f} ({zp[k]:+.1f} sigma above 1/2)" for k in FIT))

# ---------------------------------------------------------------- caveats + verdict
print("\n" + "-" * 122)
print("  THE ANSWER TO THE INVERSE PROBLEM, in one place.")
print(f"  Over the acceleration range clusters probe, s = g_bar/a0 in [{sC.min():.2f}, {sC.max():.2f}], the boost that reproduces the corrected")
print(f"  X-COP enclosed-mass profile exactly from the baryons alone is  Delta_req(s) = ({FIT[HEAD]['A']:.1f} +/- {FIT[HEAD]['sA']:.1f}) s^({FIT[HEAD]['p']:.2f} +/- {FIT[HEAD]['sp']:.2f})  (rms {FIT[HEAD]['rms']:.2f} dex,")
print(f"  seven clusters with measured stellar profiles, canonical footing; the alt footing returns the SAME exponent and A smaller")
print(f"  by {100*(1-FIT[('alt','stellar')]['A']/FIT[HEAD]['A']):.1f}%, since Delta a0 and s a0 are both measured accelerations and only the p != 1 residual sees the footing).  Equivalently J_Y = s/Delta_req = {min(b['smed']/b['med'] for b in bh):.3f}-{max(b['smed']/b['med'] for b in bh):.3f} over that range: nearly a")
print(f"  CONSTANT, i.e. G rescaled by 1/J_Y ~ {1/np.mean([b['smed']/b['med'] for b in bh]):.1f}.  It is single-valued (C2) and monotone (C3) -- so as a mathematical object it exists --")
print(f"  but it is {Dmax_head/CMAX:.1f}x above the widest ceiling any kernel of the class can reach (C4), it is {np.mean(rh):.1f}x the boost galaxies MEASURE at the")
print(f"  same accelerations (C5, worst |z| = {max(abs(np.array(allz))):.0f}), and its monotone continuation is {worst6/DG_SATURN:.0e}x the Saturn residual bound (C6).")
print("-" * 122)
print("\n  caveats: the cluster side inherits every caveat of the lead's audit (hydrostatic equilibrium, the FORW mass")
print("  reconstruction, sphericity, tabulated central profiles, no covariance) and the five clusters without a measured")
print("  stellar profile have gas-only baryons, which is why the seven-cluster subset carries the headline; the galaxy side")
print("  uses SPARC's fixed Upsilon at 3.6um, so a coherent stellar-normalisation shift moves Delta_galaxy, but the")
print("  Newtonian limit pins the coherent part to a few per cent (PAPER5) and the cluster/galaxy ratio here is far larger.")
print("  The inversion itself assumes only spherical symmetry and the programme's own static law; it is exact given those.")
print(f"  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
