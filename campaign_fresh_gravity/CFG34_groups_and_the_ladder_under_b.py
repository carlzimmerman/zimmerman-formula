#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG34 -- THE a0 LADDER UNDER CANDIDATE B (B3), and its one untested rung: the X-ray groups under B's max rule.

WHY.  FAILURES_EXECUTIVE_SUMMARY_2026-09-28 row B3: h20's ladder asked every system class for its "implied a0" on the phantom-only
reading and found the cluster rung at 1.81e-10, 6.3 sigma from the deep tail's 1.14e-10 (hunt_2026/h20_a0_ladder.py).  h20 itself
concluded that what sits above the galaxies is missing MASS, not a wrong constant.  Candidate B adds exactly that mass.  T5's identity:
in a bound region the dark mass is max(M_phantom, (Omega_c/Omega_b) M_b).  CFG4 applied it to X-COP at the measurement aperture and
reproduced the hydrostatic masses to 0.946 +- 0.080.  So under B the cluster rung is not an a0 problem.  But the rule has only been
checked where the baryons are nearly cosmic (X-COP f_b ~ 0.15).  Groups test it: at 1-3 keV the baryon fraction inside R500 is ~0.10
(Lovisari+2015, 20 groups; hunt_2026/h7_groups_hot_gas.py, where the phantom-only law came up short by eta ~ 2 in baryons).  B's rule
AS WRITTEN takes the cosmic share of the baryons present TODAY, so where the phantom does not win it predicts only ~0.10 x 6.36 = 0.65
of a group's mass.

THE METHOD (declared before this script's first run).  h7's data and stellar-mass import exec'd read-only (Lovisari+2015 hydrostatic
masses and gas masses at R500 and R2500; stars from the Kravtsov+2018 SHMR, x/1.5 bracket, 0.65 of M_*,500 inside R2500 as h7).  At each
radius: M_b = M_gas + M_*; M_ph = (nu_mono(g_N/a0) - 1) M_b with g_N = G M_b / r^2 (the monopole reading, as CFG4); B's mass
M_B = M_b + max(M_ph, 5.364 M_b).  The statistic is the median over groups of log10(M_HSE / M_B).  Its error is the group-to-group
scatter / sqrt(N), with a floor in quadrature: the stellar bracket (half the spread of the median between the bracket's ends, re-run)
and a 20% hydrostatic bias (0.079 dex; HSE masses run LOW, which would make the ratio larger -- carried symmetrically).

PRE-DECLARED
  C1  CONTROL  h7's committed median eta at R500 reproduced (1.80 - 2.11 canonical, 1.54 - 1.81 alt, over the stellar bracket).
  C2  CONTROL  CFG4's committed X-COP identity ratios recomputed from its per-cluster f_b and phantom/M_b; the median 0.946 +- 0.080.
  H1  [HEADLINE; MUTATE must fail] B's MAX RULE, AS WRITTEN, REPRODUCES THE GROUPS AT R500: the median log(M_HSE/M_B) lies within
      2 sigma of zero, both footings.
  H2  ... and at R2500, both footings.
  H3  THE RULE TRACKS THE BARYON FRACTION: over the groups (R500) and the X-COP clusters together, log(M_HSE/M_B) falls with log f_b
      (Spearman rho < 0 at p < 0.01, canonical): where the rule falls short, it falls short by the baryons the system has lost.
  R1-R4 (reported): which branch of the max wins at each radius; the baryon fraction each group would need for the rule to hold; the
      phantom-only law beside it; THE LADDER UNDER B -- every rung re-scored in this campaign, with its significance.
  READING (declared): H1 PASS -> B's max rule covers the groups as well as the clusters, and the upper ladder closes under B.
  H1 FAIL -> B's rule as written fails at the group scale: its cosmic share must be tied to something other than today's baryons (the
  baryons a system collapsed with, which feedback can move but a cold component does not follow), or B is short there as the
  phantom-only law is.
MUTATE=1: every hydrostatic mass tripled -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG34_groups_and_the_ladder_under_b.py   (MUTATE=1 for the control; ~5 s)
"""
import os, sys, math, re, json
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG34_groups_and_the_ladder_under_b", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every hydrostatic mass tripled -- H1 must FAIL ***")
HMUT = 3.0 if MUTATE else 1.0
FOOTS = ("canonical", "alt")
COSMIC = 0.1200 / 0.02237
HSE_BIAS = math.log10(1.2)

HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)
H7P = os.path.join(HUNT, "h7_groups_hot_gas.py")
g7, _ = C4.exec_slices(H7P, [(None, 'P("="*116); P("ITEM 7A'), ('lp = os.path.join(DATA, "lovisari2015_groups.tsv")', "R7B = {}")],
                       name="h7_slices")
GR, mstar500, FIN, SBR, mreq = g7["gr"], g7["mstar500"], g7["FIN"], g7["SBR"], g7["mond_required_baryons"]
G_, KPC, MSUN, A0H = g7["G"], g7["kpc"], g7["Msun"], g7["A0"]
A0B = C.A0_SI
P(f"\n  h7's groups (exec'd read-only): {len(GR)}; median f_gas(R500) {np.median([g['Mg500'] / g['M500'] for g in GR]):.3f}")

# ================================================================================================ C1
R.banner("C1  CONTROL: h7's committed median eta at R500")
o7 = open(os.path.join(HUNT, "h7_groups_hot_gas.out")).read()
com = {f: tuple(float(x) for x in re.search(rf"{f}\s+MEDIAN eta at R2500 = [0-9.]+ - [0-9.]+; at R500 = ([0-9.]+) - ([0-9.]+)", o7).groups()) for f in FOOTS}
mine = {}
for f in FOOTS:
    lo_, hi_ = [], []
    for g in GR:
        Ms = mstar500(g["M500"]); r = g["R500"] * KPC; gobs = G_ * g["M500"] * MSUN / r ** 2
        Mr = mreq(gobs, r, A0H[f]) / MSUN
        lo_.append(Mr / (g["Mg500"] + Ms * SBR)); hi_.append(Mr / (g["Mg500"] + Ms / SBR))
    mine[f] = (float(np.median(lo_)), float(np.median(hi_)))
dev1 = max(abs(round(mine[f][i], 2) - com[f][i]) for f in FOOTS for i in (0, 1))
check("C1 CONTROL: h7's committed median eta at R500 reproduced over the stellar bracket (both footings)",
      "; ".join(f"{f}: {mine[f][0]:.3f} - {mine[f][1]:.3f} (committed {com[f][0]:.2f} - {com[f][1]:.2f})" for f in FOOTS), dev1 <= 1e-9)

# ================================================================================================ C2 X-COP under CFG4's rule
R.banner("C2  CONTROL: CFG4's X-COP identity ratios recomputed from its per-cluster numbers")
C4R = json.load(open(os.path.join(HERE, "CFG4_clusters_results.json")))["numbers"]
xc = C4R["C"]["canonical|nu_mono|b0.0"]
rec_id = [c["fb"] * (1 + max(c["phantom_over_Mb"], COSMIC)) for c in xc]
dev2 = max(abs(a - c["id_ratio"]) for a, c in zip(rec_id, xc))
h2c = C4R["H2"]["canonical|nu_mono"]
check("C2 CONTROL: CFG4's X-COP identity ratios recomputed exactly from its f_b and phantom/M_b (the max rule as CFG4 applied it)",
      f"max |d| {dev2:.1e} over {len(xc)} clusters; median {np.median(rec_id):.4f} (committed {h2c['id_ratio']:.4f} +- {h2c['id_sd']:.4f}); "
      f"the cosmic share wins in {sum(c['phantom_over_Mb'] < COSMIC for c in xc)} of {len(xc)}", dev2 <= 1e-12)


# ================================================================================================ B's rule on the groups
def b_mass(Mb, r_kpc, a0, kern=C.nu_mono):
    """B's mass inside r (the max rule as CFG4 applied it) and the phantom-only law's mass, nu M_b."""
    gN = G_ * Mb * MSUN / (r_kpc * KPC) ** 2
    nu_ = float(kern(np.array([gN / a0]))[0])
    Mph = (nu_ - 1.0) * Mb
    return Mb + max(Mph, COSMIC * Mb), Mph >= COSMIC * Mb, nu_ * Mb


def run(a0, sfac=1.0):
    out = {"R500": [], "R2500": []}
    for g in GR:
        Ms5 = mstar500(g["M500"]) * sfac
        for tag, R_, M_, Mg, Ms in (("R500", g["R500"], g["M500"], g["Mg500"], Ms5), ("R2500", g["R2500"], g["M2500"], g["Mg2500"], Ms5 * np.mean(FIN))):
            MB, ph, Mlaw = b_mass(Mg + Ms, R_, a0)
            out[tag].append(dict(name=g["name"], ratio=HMUT * M_ / MB, ph=ph, fb=(Mg + Ms) / M_, lawratio=HMUT * M_ / Mlaw))
    return out


R.banner("H1 / H2  B's MAX RULE ON THE TWENTY X-RAY GROUPS")
RES = {}
for f in FOOTS:
    base, lo_s, hi_s = run(A0B[f]), run(A0B[f], SBR), run(A0B[f], 1 / SBR)
    for tag in ("R500", "R2500"):
        lr = np.log10([d["ratio"] for d in base[tag]])
        med = float(np.median(lr)); err = float(np.std(lr, ddof=1) / math.sqrt(len(lr)))
        star = 0.5 * abs(np.median(np.log10([d["ratio"] for d in lo_s[tag]])) - np.median(np.log10([d["ratio"] for d in hi_s[tag]])))
        tot = math.sqrt(err ** 2 + star ** 2 + HSE_BIAS ** 2)
        nph = sum(d["ph"] for d in base[tag])
        lawm = float(np.median(np.log10([d["lawratio"] for d in base[tag]])))
        RES[(f, tag)] = dict(med=med, err=err, star=float(star), tot=tot, z=med / tot, n_phantom_wins=int(nph), n=len(lr),
                             law_med=lawm, fb_med=float(np.median([d["fb"] for d in base[tag]])))
        v = RES[(f, tag)]
        P(f"    {f:9s} {tag:5s}: median M_HSE/M_B = {10 ** v['med']:.2f} ({v['med']:+.3f} dex) +- {v['tot']:.3f} (groups {v['err']:.3f}, stars {v['star']:.3f}, "
          f"HSE {HSE_BIAS:.3f}) -> {v['z']:+.2f} sigma; the phantom wins the max in {v['n_phantom_wins']} of {v['n']}; median f_b {v['fb_med']:.3f}; "
          f"the phantom-only law alone {10 ** v['law_med']:.2f}")
check("H1 [HEADLINE] B's MAX RULE, AS WRITTEN, REPRODUCES THE GROUPS AT R500: median log(M_HSE/M_B) within 2 sigma of zero, both footings"
      + ("  [MUTATE: HSE masses tripled]" if MUTATE else ""),
      "; ".join(f"{f}: {10 ** RES[(f, 'R500')]['med']:.2f} ({RES[(f, 'R500')]['z']:+.2f} sigma)" for f in FOOTS),
      all(abs(RES[(f, "R500")]["z"]) < 2 for f in FOOTS))
check("H2 ... AND AT R2500, both footings",
      "; ".join(f"{f}: {10 ** RES[(f, 'R2500')]['med']:.2f} ({RES[(f, 'R2500')]['z']:+.2f} sigma)" for f in FOOTS),
      all(abs(RES[(f, "R2500")]["z"]) < 2 for f in FOOTS))

# ================================================================================================ H3
R.banner("H3  DOES THE RULE TRACK THE BARYON FRACTION? (groups at R500 + X-COP clusters, canonical)")
gb = run(A0B["canonical"])["R500"]
fb_all = np.array([d["fb"] for d in gb] + [c["fb"] for c in xc])
lr_all = np.log10(np.array([d["ratio"] for d in gb] + [HMUT / c["id_ratio"] for c in xc]))
rho, pval = spearmanr(np.log10(fb_all), lr_all)
check("H3 THE RULE TRACKS THE BARYON FRACTION: log(M_HSE/M_B) falls with log f_b over groups and clusters (Spearman rho < 0, p < 0.01)",
      f"rho = {rho:+.3f}, p = {pval:.1e} over {len(fb_all)} systems; f_b spans {fb_all.min():.3f}-{fb_all.max():.3f} (cosmic {0.02237 / (0.02237 + 0.1200):.3f})",
      rho < 0 and pval < 0.01)

# ================================================================================================ reported
R.banner("R1-R4  REPORTED")
need = [d["ratio"] * d["fb"] for d in gb]
check("R1 (reported) the baryon fraction each group would need inside R500 for B's rule to hold (M_HSE/M_B x f_b), canonical",
      f"median {np.median(need):.3f} (observed {np.median([d['fb'] for d in gb]):.3f}; cosmic {0.02237 / 0.14237:.3f}); range {min(need):.3f}-{max(need):.3f}",
      True, load_bearing=False)
check("R2 (reported) the phantom-only law beside B's rule (median M_HSE/M_law)",
      "; ".join(f"{f} {t}: law {10 ** RES[(f, t)]['law_med']:.2f} vs B {10 ** RES[(f, t)]['med']:.2f}" for f in FOOTS for t in ("R500", "R2500")),
      True, load_bearing=False)


def jnum(fn, *keys):
    try:
        v = json.load(open(os.path.join(HERE, fn)))["numbers"]
        for k in keys:
            v = v[k]
        return v
    except Exception:
        return None


LAD = []
u = jnum("CFG28_ufd_referee_results.json", "RES")
if u: LAD.append(("MW ultra-faint dwarfs (CFG28)", "~1e3-1e5", f"+{u['canonical']['km'][0]:.3f} dex in sigma", f"{u['canonical']['z_km']:.1f} / {u['alt']['z_km']:.1f}"))
s18 = jnum("CFG18_satellite_infall_gas_results.json", "RES")
if s18: LAD.append(("MW classical + M31 dwarfs, infall gas (CFG18)", "~1e6-1e8",
                    f"{s18['cls|zero|canonical']['mean']:+.3f} / {s18['m31|zero|canonical']['mean']:+.3f} dex in sigma",
                    f"{s18['cls|zero|canonical']['z']:.1f} / {s18['m31|zero|canonical']['z']:.1f}"))
u31 = jnum("CFG31_coma_udgs_under_b_results.json", "RES")
if u31: LAD.append(("Coma UDGs, isolated law of infall baryons (CFG31)", "~1e8", f"{u31['canonical|infall gas, non-detections zero']['mean']:+.3f} dex in g",
                    f"{u31['canonical|infall gas, non-detections zero']['z']:.1f} / {u31['alt|infall gas, non-detections zero']['z']:.1f}"))
LAD.append(("SPARC rotation curves (CFG4)", "1e8-1e11", "the law's fit: rms 0.100 dex", "fit"))
b30 = jnum("CFG30_binary_galaxies_referee_results.json", "H3")
if b30: LAD.append(("binary galaxies, timing orbits (CFG30)", "~1e11", f"A = {b30['canonical']['A']:.2f} (circular 1.89)", "orbit-degenerate"))
e32 = jnum("CFG32_xray_ellipticals_under_b_results.json", "RES")
if e32: LAD.append(("X-ray ellipticals (CFG32)", "~3e11", f"{e32['canonical']['base']['mean']:+.3f} dex in g", f"{e32['canonical']['z']:.1f} / {e32['alt']['z']:.1f}"))
s33 = jnum("CFG33_slacs_lensing_vs_dynamics_results.json", "H2")
if s33: LAD.append(("SLACS lensing vs ATLAS3D dynamics (CFG33)", "~2e11", f"{s33['canonical|V']['delta']:+.3f} dex in M_*", f"{s33['canonical|V']['z']:.1f} / {s33['alt|V']['z']:.1f} (floor)"))
LAD.append(("X-ray groups at R500 (this lane)", "2e13-1.4e14", f"{RES[('canonical', 'R500')]['med']:+.3f} dex in mass", f"{RES[('canonical', 'R500')]['z']:.1f} / {RES[('alt', 'R500')]['z']:.1f}"))
LAD.append(("X-COP clusters at ~0.8 R500 (CFG4)", "3e14-9e14", f"{-math.log10(h2c['id_ratio']):+.3f} dex in mass", f"{(1 - h2c['id_ratio']) / h2c['id_sd']:.1f}"))
P("\n    THE LADDER UNDER CANDIDATE B (every rung scored with B's own rule; significance canonical / alt as each lane reported it):")
for row in LAD:
    P(f"      {row[0]:52s} M ~ {row[1]:12s} {row[2]:34s} {row[3]}")
check("R4 (reported) the ladder under candidate B, from the committed re-scores", f"{len(LAD)} rungs listed above", True, load_bearing=False)

h1 = all(abs(RES[(f, "R500")]["z"]) < 2 for f in FOOTS)
reading = ("B's max rule covers the groups as well as the clusters, and the upper ladder closes under B" if h1 else
           "B's rule as written fails at the group scale: its cosmic share must be tied to something other than today's baryons, or B is short "
           "there as the phantom-only law is")
P(f"\n    READING (declared): {reading}")
R.num("C1", dict(committed=com, mine=mine)); R.num("C2", dict(recomputed=rec_id, median=float(np.median(rec_id))))
R.num("RES", {f"{f}|{t}": v for (f, t), v in RES.items()}); R.num("H3", dict(rho=float(rho), p=float(pval)))
R.num("ladder", LAD); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
