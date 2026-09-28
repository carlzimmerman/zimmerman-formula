#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG32 -- THE X-RAY ELLIPTICALS UNDER CANDIDATE B, REFEREED: is the recorded "1.69x more boost" liability (B4) a real failure of B?

WHY.  FAILURES_EXECUTIVE_SUMMARY_2026-09-28 row B4: seven X-ray-bright early-type galaxies (Humphrey+2006, ApJ 646, 899; NGC 720,
1407, 4125, 4261, 4472, 4649, 6482) need a median 1.69x (canonical) / 1.57x (alt) more boost than the kernel gives over 5-70 kpc,
with stars only at a Kroupa stellar-population M/L (hunt_2026/h10_h18_xray_hse.py).  It was never scored under candidate B and never
given a significance.  Candidate B's rules for these systems:
  * T5: "baryon-poor galaxies are phantom-dominated, baryon-complete clusters keep the cosmic share" -- the dark mass is
    max(M_phantom, (Omega_c/Omega_b) M_b).  For clusters CFG4 applied it at the measurement aperture.  For galaxies B uses the law.
  * FG001's ownership: an isolated or top-level galaxy obeys the law with no external field; an accreted one (NGC 4472 and 4649 are
    Virgo members) obeys the isolated law of its infall baryons.  Either way, at 5-70 kpc B's prediction is the law on the galaxy's
    own baryons -- h10's prediction, with the contract kernel nu_mono.
So B changes little here; what this lane adds is the referee h10 never had.  h10 used the paper's BEST-FIT MODEL (NFW + stars, fitted
to the Chandra profiles), not the deprojected data, and omitted the hot gas; the IMF of massive ellipticals is uncertain between
Kroupa and Salpeter.  None of that was propagated.

THE METHOD (declared before this script's first run).  h10's data file and mass model, exec'd read-only (Hernquist stars with
a = R_e/1.8153, NFW with Humphrey's M_vir, R_vir, c; g_obs from the fitted model, g_bar from the stars at a population M/L; radii 5,
10, 20, 40, 70 kpc).  The offset of a point is log10[(g_obs/g_bar)/nu(g_bar/a0)]; a GALAXY's offset is the median over its radii (the
five radii of one galaxy are not independent), and the SAMPLE offset is the mean of the seven, with the galaxy-to-galaxy error
std/sqrt(7).  The systematic floor, computed by re-running the pipeline: the IMF (Kroupa -> Salpeter, Humphrey's own population
values) and the radial range (all radii -> r <= 40 kpc, where the fitted model is least extrapolated).  The hot gas cannot be added
(no gas profiles in the repository); instead the hot gas each galaxy would need to null its offset at 70 kpc is reported.

PRE-DECLARED
  C1  CONTROL  h10's committed medians reproduced: 1.69 (scatter 0.249 dex) canonical, 1.57 (0.242) alt.
  H1  [HEADLINE; MUTATE must fail] B4 SURVIVES THE REFEREE AS A FAILURE OF B: under B's law (nu_mono, no external field, Kroupa baryons)
      the mean per-galaxy offset exceeds zero by > 2 sigma, sigma = the galaxy-to-galaxy error and the floor (IMF, radial range) in
      quadrature, both footings.
  H2  THE MISSING MASS IS EXTENDED: the offset grows toward low acceleration -- the slope d log(ratio)/d log y is negative in at least
      6 of the 7 galaxies (Kroupa, canonical).  A wrong M/L would move the inner points most, not the outer ones.
  H3  B's CLUSTER CONVENTION IS NOT AN ESCAPE: applying the max rule at each radius (as CFG4 did at the cluster aperture) over-
      predicts g_obs/g_bar at 10 kpc by more than 2x in at least 5 of the 7 galaxies -- consistent with T5's class split (galaxies
      phantom-dominated).
  R1-R6 (reported): Salpeter and Humphrey's fitted M/L; r <= 40 kpc; the P2 kernel; per-galaxy offsets; the hot gas each galaxy
      would need at 70 kpc (M_gas/M_*); the max rule's outer-radius ratio.
  READING (declared): H1 PASS -> B4 stands as a failure of candidate B at the quoted significance; the shortfall grows outward, and
  the max rule is not an escape.  H1 FAIL -> B4 is within the IMF and radial-range systematics of the published best-fit models: not
  an established failure.  Either way the definitive test needs the deprojected gas density and temperature profiles.
MUTATE=1: every g_obs halved -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG32_xray_ellipticals_under_b.py   (MUTATE=1 for the control; ~5 s)
"""
import os, sys, math, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG32_xray_ellipticals_under_b", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every g_obs halved -- H1 must FAIL ***")
GSC = 0.5 if MUTATE else 1.0
FOOTS = ("canonical", "alt")

HUNT = os.path.join(C.REPO, "hunt_2026")
sys.path.insert(0, HUNT)
H10P = os.path.join(HUNT, "h10_h18_xray_hse.py")
g10, _ = C4.exec_slices(H10P, [(None, 'P("="*116); P("ITEM 10'),
                               ('rows = [l.rstrip("\\n").split("\\t") for l in open(os.path.join(DATA, "humphrey2006', 'm10c, s10c, y10, r10 = R10["canonical"]')],
                        name="h10_slices")
GAL, M_hern, M_nfw, R10 = g10["gal"], g10["M_hern"], g10["M_nfw"], g10["R10"]
G_, KPC, MSUN = g10["G"], g10["kpc"], g10["Msun"]
A0B = C.A0_SI
KERN = {"nu_mono": C.nu_mono, "P2": C.nu_p2}
COSMIC = 0.1200 / 0.02237
RADII = (5.0, 10.0, 20.0, 40.0, 70.0)
P(f"\n  h10's sample (exec'd read-only): {len(GAL)} galaxies: " + ", ".join(g["name"] for g in GAL))

# ================================================================================================ C1
R.banner("C1  CONTROL: h10's committed medians")
o10 = open(os.path.join(HUNT, "h10_h18_xray_hse.out")).read()
com = {f: tuple(float(x) for x in re.search(rf"{f}\s+over 35 \(galaxy, radius\) points.*?boost = ([0-9.]+), scatter ([0-9.]+) dex", o10).groups())
       for f in FOOTS}
dev = max(max(abs(round(R10[f][0], 2) - com[f][0]), abs(round(R10[f][1], 3) - com[f][1])) for f in FOOTS)
check("C1 CONTROL: h10's committed median boost and scatter reproduced (both footings)",
      "; ".join(f"{f}: {R10[f][0]:.3f} / {R10[f][1]:.4f} (committed {com[f][0]:.2f} / {com[f][1]:.3f})" for f in FOOTS), dev <= 1e-9)


def points(g, a0, ups="uk", kern="nu_mono", radii=RADII, gsc=GSC):
    """per radius: y, g_obs/g_bar, the law's nu, the ratio (g_obs/g_bar)/nu."""
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9); Ms = g[ups] * g["LK"]
    out = []
    for r in radii:
        Mtot = M_hern(r, Mfit, g["Re"]) + M_nfw(r, Mdm, g["Rvir"], g["c"])
        Mb = M_hern(r, Ms, g["Re"])
        rr = r * KPC; gobs = gsc * G_ * Mtot * MSUN / rr ** 2; gb = G_ * Mb * MSUN / rr ** 2
        y = gb / a0; nu_ = float(KERN[kern](np.array([y]))[0])
        out.append(dict(r=r, y=y, obs=gobs / gb, nu=nu_, ratio=gobs / gb / nu_, gobs=gobs, gb=gb))
    return out


def sample(a0, **kw):
    per = np.array([np.median([math.log10(p["ratio"]) for p in points(g, a0, **kw)]) for g in GAL])
    return dict(per=per, mean=float(per.mean()), err=float(per.std(ddof=1) / math.sqrt(len(per))), median=float(np.median(per)))


# ================================================================================================ H1
R.banner("H1  B's LAW ON THE SEVEN ELLIPTICALS: per-galaxy offsets, the galaxy-to-galaxy error, the floor")
RES = {}
for f in FOOTS:
    a0 = A0B[f]
    base = sample(a0)
    salp = sample(a0, ups="us")
    fitu = sample(a0, ups="uf")
    r40 = sample(a0, radii=(5.0, 10.0, 20.0, 40.0))
    p2 = sample(a0, kern="P2")
    floor = math.hypot(abs(salp["mean"] - base["mean"]), abs(r40["mean"] - base["mean"]))
    tot = math.hypot(base["err"], floor)
    RES[f] = dict(base=base, salp=salp, fit=fitu, r40=r40, p2=p2, floor=floor, tot=tot, z=base["mean"] / tot,
                  imf_term=abs(salp["mean"] - base["mean"]), radial_term=abs(r40["mean"] - base["mean"]))
    P(f"    {f:9s}: per-galaxy offsets (Kroupa) " + ", ".join(f"{g['name']} {o:+.2f}" for g, o in zip(GAL, base["per"])))
    P(f"    {'':9s}  mean {base['mean']:+.3f} +- {base['err']:.3f} (galaxy-to-galaxy); floor {floor:.3f} (IMF {RES[f]['imf_term']:.3f}, "
      f"radial range {RES[f]['radial_term']:.3f}) -> {RES[f]['z']:+.2f} sigma;  Salpeter {salp['mean']:+.3f}, fitted M/L {fitu['mean']:+.3f}, "
      f"r <= 40 kpc {r40['mean']:+.3f}, P2 {p2['mean']:+.3f}")
check("H1 [HEADLINE] B4 SURVIVES THE REFEREE AS A FAILURE OF B: the mean per-galaxy offset under B's law exceeds zero by > 2 sigma "
      "(galaxy-to-galaxy error + IMF and radial-range floor), both footings" + ("  [MUTATE: g_obs halved]" if MUTATE else ""),
      "; ".join(f"{f}: {v['base']['mean']:+.3f} +- {v['tot']:.3f} dex ({v['z']:+.2f} sigma; a factor {10 ** v['base']['mean']:.2f})" for f, v in RES.items()),
      all(v["z"] > 2 for v in RES.values()))

# ================================================================================================ H2 the shape
R.banner("H2  THE SHAPE: does the shortfall grow toward low acceleration?")
slopes = []
for g in GAL:
    pts = points(g, A0B["canonical"])
    ly = np.log10([p["y"] for p in pts]); lr = np.log10([p["ratio"] for p in pts])
    slopes.append(float(np.polyfit(ly, lr, 1)[0]))
nneg = int(sum(s < 0 for s in slopes))
check("H2 THE MISSING MASS IS EXTENDED: the offset grows toward low acceleration in at least 6 of the 7 galaxies (Kroupa, canonical)",
      "slopes d log(ratio)/d log y: " + ", ".join(f"{g['name']} {s:+.2f}" for g, s in zip(GAL, slopes)) + f"; {nneg} of 7 negative", nneg >= 6)

# ================================================================================================ H3 the cluster convention
R.banner("H3  B's CLUSTER CONVENTION (the max rule at each radius) in a galaxy")
over10, outer = [], []
for g in GAL:
    pts = {p["r"]: p for p in points(g, A0B["canonical"])}
    for rad, store in ((10.0, over10), (70.0, outer)):
        p = pts[rad]
        pred = 1.0 + max(p["nu"] - 1.0, COSMIC)
        store.append(pred / p["obs"])
n2 = int(sum(o > 2 for o in over10))
check("H3 B's CLUSTER CONVENTION IS NOT AN ESCAPE: the max rule applied at each radius over-predicts g_obs/g_bar at 10 kpc by more than "
      "2x in at least 5 of the 7 galaxies",
      "predicted / observed at 10 kpc: " + ", ".join(f"{g['name']} {o:.2f}" for g, o in zip(GAL, over10)) + f" ({n2} of 7 above 2); at 70 kpc: "
      + ", ".join(f"{o:.2f}" for o in outer), n2 >= 5)

# ================================================================================================ reported
R.banner("R1-R6  REPORTED")
need = []
for g in GAL:
    p = [q for q in points(g, A0B["canonical"]) if q["r"] == 70.0][0]
    lo_, hi_ = 0.0, 1e4
    for _ in range(100):
        mid = 0.5 * (lo_ + hi_)
        gb = p["gb"] * (1 + mid)
        pred = float(KERN["nu_mono"](np.array([gb / A0B["canonical"]]))[0]) * gb
        lo_, hi_ = (mid, hi_) if pred < p["gobs"] else (lo_, mid)
    need.append(0.5 * (lo_ + hi_))
check("R1 (reported) the IMF and the radial range: Salpeter, Humphrey's fitted M/L, r <= 40 kpc, the P2 kernel (sample means)",
      "; ".join(f"{f}: Kroupa {v['base']['mean']:+.3f}, Salpeter {v['salp']['mean']:+.3f}, fitted {v['fit']['mean']:+.3f}, r <= 40 {v['r40']['mean']:+.3f}, "
                f"P2 {v['p2']['mean']:+.3f}" for f, v in RES.items()), True, load_bearing=False)
check("R2 (reported) the per-galaxy offsets under Salpeter (canonical) and the galaxy-to-galaxy spread",
      ", ".join(f"{g['name']} {o:+.2f}" for g, o in zip(GAL, RES["canonical"]["salp"]["per"]))
      + f"; median Kroupa {RES['canonical']['base']['median']:+.3f}, Salpeter {RES['canonical']['salp']['median']:+.3f}", True, load_bearing=False)
check("R3 (reported) the hot gas each galaxy would need inside 70 kpc to null its offset there (M_gas / M_*, Kroupa, canonical)",
      ", ".join(f"{g['name']} {n_:.1f}" for g, n_ in zip(GAL, need)), True, load_bearing=False)
check("R4 (reported) the significance under Salpeter alone (the most favourable standard IMF), both footings",
      "; ".join(f"{f}: {v['salp']['mean']:+.3f} +- {math.hypot(v['salp']['err'], v['radial_term']):.3f} ({v['salp']['mean'] / math.hypot(v['salp']['err'], v['radial_term']):+.2f} sigma)"
                for f, v in RES.items()), True, load_bearing=False)
reading = (f"B4 stands as a failure of candidate B: the law under-predicts the X-ray ellipticals' mass by a factor "
           f"{10 ** RES['canonical']['base']['mean']:.2f} / {10 ** RES['alt']['base']['mean']:.2f} ({RES['canonical']['z']:.1f} / {RES['alt']['z']:.1f} sigma)"
           if all(v["z"] > 2 for v in RES.values()) else
           "B4 is within the IMF and radial-range systematics of the published best-fit models: not an established failure")
P(f"\n    READING (declared): {reading}; the definitive test needs the deprojected gas density and temperature profiles.")
R.num("C1", dict(committed=com, mine={f: [R10[f][0], R10[f][1]] for f in FOOTS}))
R.num("RES", {f: dict(v, base=dict(v["base"], per=v["base"]["per"].tolist()), salp=dict(v["salp"], per=v["salp"]["per"].tolist()),
                        fit=dict(v["fit"], per=v["fit"]["per"].tolist()), r40=dict(v["r40"], per=v["r40"]["per"].tolist()),
                        p2=dict(v["p2"], per=v["p2"]["per"].tolist())) for f, v in RES.items()})
R.num("H2", dict(slopes=slopes, n_negative=nneg)); R.num("H3", dict(over10=over10, outer70=outer)); R.num("R3_gas_needed", need)
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
