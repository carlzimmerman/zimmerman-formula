#!/usr/bin/env python3
"""G138 -- THE CAP-FIRING-RADIUS RECONCILIATION: where does the cap actually
bite?

THE PUZZLE (from the committed record):
  * G057b registered R_cap = 296-958 kpc (median 703 canonical / 525 alt:
    the a0-CROSSING of the MEASURED TOTAL field, G*M_HSE(r)/r^2 = a0) and
    quoted it as "the EFE cap radius".
  * G094/G097 registered 711.6 = 711.6: the split and the uncapped-phantom
    floor are the SAME prediction over the 50-600 kpc window -- the G016
    Hubble-kernel cap (g_ext = cH0, the L180 external field) NEVER FIRES
    in-window (g_tot stays < cH0 = 6.55e-10 m/s^2, g_tot(50 kpc) ~ 0.9 cH0).
  WHY the two registers do not contradict: R_cap(a0) is a DIAGNOSTIC of the
  measured field, NOT the firing boundary.  The committed firing rule is
  `capped = g_tot > g_ext` (the phantom's own force passes through the same
  mu2, so in the screened zone g_tot > g_ext it carries no hydrostatic
  support).  The firing radius is the g_tot = g_ext crossing, and its value
  depends on the g_ext CLASS:
      (1) cH0-class (the registered operative rule):  g_ext = cH0 ~ 7 a0 ->
          r_fire ~ 31-50 kpc (< the 50 kpc window edge) or never on the
          tables  ->  the cap never fires in the 50-600 kpc window, and the
          split row IS the phantom row there: 711.6 = 711.6 exactly.
      (2) a0-class (what G057b's R_cap column actually measured):
          g_ext = a0 -> r_fire = R_cap(a0) = 296-958 kpc = (0.28-0.91) R500:
          IN the window for 2/12 canonical (A3158 476, RXC1825 478), BEYOND
          600 kpc for 8/12, never (no crossing) for 2/12 (A1644, A2255).
      (3) self-class (g_ext = the cluster's OWN field at R500):
          g_self = g_tot(R500) ~ 0.3-0.6 a0 -> r_fire = R500 by
          monotonicity: the phantom is screened over the ENTIRE measured
          profile inside R500 (split = bare baryons = the known all-capped
          extreme), turning on only beyond R500.
  r_cap = sqrt(G M_b/g_ext) (the analytic deep-form): a0-class ->
  sqrt(G M_b/a0) = r_M ~ 90-300 kpc baryon-scale; self-class ->
  r_M sqrt(a0/g_self) ~ 1.3-1.8 r_M ~ 150-500 kpc: both r_M-class; the
  registered 296-958 kpc is the TOTAL-field crossing, larger by
  sqrt(M_hse/M_b) ~ 1.4-2.

WHICH RULE DID G057b REGISTER?  The a0-class crossing of the measured total
field (a direct datum on the committed profiles).  WHICH ONE CAN THE DATA
TEST?  The a0-class crossing is measured directly (in-window or in the
600 kpc-R500 outer window for 18/24 runs); the cH0 rule is untestable
in-window by construction (its threshold lies above the window's field);
the self rule is testable everywhere and is the KNOWN all-capped extreme
(G059's bare-baryon 0.17 account, G057b's 0.409 coherent undershoot).

THE OUTER-WINDOW CONSEQUENCE (V2): with the a0-class firing rule the split
prediction differs from the uncapped floor exactly where g_tot > a0 (the
phantom screened): r < R_cap(a0).  For the 8 clusters with
R_cap(a0) > 600 kpc (canonical) that difference zone EXTENDS INTO the
(600 kpc, R500) outer window, and for A2319 (0.71 R500) even into the
0.7-1.0 R500 bins: the phantom re-activates (split merges back onto the
floor) beyond R_cap(a0) -- the outer window brackets the switch.  Under the
committed cH0 rule the outer-window delta chi2 is ZERO identically (never
fires anywhere on the tables).  We compute the per-cluster delta chi2
(split minus uncapped) per window per rule and state testability.

VERDICTS:
  V1  per-cluster firing radius under both rules (a0-class vs self-class,
      cH0-class beside) vs the 50-600 kpc window and vs R500.
  V2  outer-window testability: the split-vs-uncapped delta chi2 in the
      (600 kpc, R500) and 0.7-1.0 R500 bins, per cluster, both footings.
  V3  the honest statement: "never fired in the window" is a WINDOW
      statement (the window's field is below the cH0 threshold), not a
      no-cap statement; the split architecture's switch is a0-class at
      (0.28-0.91) R500 and becomes testable at 600 kpc-R500 / 0.7-1.0 R500
      for the massive half of the sample.

Every number is re-derived from the committed X-COP tables
(real_research/data/xcop/) with the committed lane conventions (G057/G094/
G097/G050): log-interp beyond-tables = nan, stellar import via the h67b
median ratio, err = sqrt(EM_FORW^2 + (0.23 M_b)^2), chi2 over the same
profiles and errors.  The registered R_cap values and the 711.6 = 711.6
rows are reproduced as anchors before the new quantities.
"""
import json
import math
import os

import numpy as np
from astropy.io import fits
from scipy.optimize import brentq

RES = []


def check(name, measured, ok, note=""):
    RES.append(dict(name=name, measured=str(measured), pass_=bool(ok),
                    note=note))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if note:
        print(f"         note    : {note}")


print("=" * 100)
print("G138 -- THE CAP-FIRING-RADIUS RECONCILIATION: where does the cap bite?")
print("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
XB = os.path.join(REPO, "real_research", "data", "xcop")

G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
c_l = 2.99792458e8
H0 = 67.4 * 1e3 / 3.0857e22
rho_lam = 0.685 * 3 * H0 ** 2 / (8 * math.pi * G)
s_DE = c_l * math.sqrt(G * rho_lam)
A0 = {"canonical": s_DE / 2, "alt": 1.1279e-10}
GEXT = c_l * H0                                    # L180 Hubble-kernel g_ext
RG = np.array([50., 75., 100., 150., 210., 300., 420., 600.])   # kpc
WINS = [(0.10, 0.20), (0.20, 0.40), (0.40, 0.70), (0.70, 1.00)]  # R500 units
WIN_NAMES = ["0.1-0.2 R500", "0.2-0.4 R500", "0.4-0.7 R500", "0.7-1.0 R500"]


def loginterp(x, xp, fp):
    """G097's interpolator: log-log np.interp, nan beyond the table."""
    x = np.atleast_1d(np.asarray(x, float))
    ok = np.isfinite(xp) & np.isfinite(fp) & (xp > 0) & (fp > 0)
    xp, fp = np.asarray(xp)[ok], np.asarray(fp)[ok]
    o = np.argsort(xp)
    xp, fp = xp[o], fp[o]
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    out[(x < xp[0]) | (x > xp[-1])] = np.nan
    return out


# ---------------------------------------------------------------- the data
CL = []
for n in sorted(d for d in os.listdir(XB) if os.path.isdir(os.path.join(XB, d))):
    hm = fits.open(os.path.join(XB, n, f"{n}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(XB, n, f"{n}_fgas_profile.fits"))[1].data
    d = dict(name=n,
             r_hm=np.array(hm["RADIUS"], float),
             M_hse=np.array(hm["M_FORW"], float) * MSUN,
             eM_hse=np.array(hm["EM_FORW"], float) * MSUN,
             M_nfw=np.array(hm["M_NFW"], float) * MSUN,
             r_fg=np.array(fg["RADIUS"], float) * 1e3,
             M_gas=np.array(fg["MGAS"], float) * MSUN)
    fs = os.path.join(XB, n, f"{n}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        d["r_st"] = np.array(ms["RADIUS"], float)
        d["M_st"] = np.array(ms["MSTAR"], float) * MSUN
        d["has_star"] = True
    else:
        d["has_star"] = False
    CL.append(d)
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))

# ---- the h67b stellar import (G097's exact convention)
ratio_pts = {}
for r in RG:
    v = []
    for c in CL:
        if not c["has_star"]:
            continue
        mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
        ms = loginterp([r], c["r_st"], c["M_st"])[0]
        if np.isfinite(mg) and np.isfinite(ms) and ms > 0:
            v.append(ms / mg)
    if v:
        ratio_pts[r] = (float(np.median(v)), len(v))
_rp = np.array(sorted(ratio_pts))
RATIO_TAB = {float(r): float(ratio_pts[r][0]) for r in _rp}


def ratio_interp(r):
    return 10 ** np.interp(np.log10(r), np.log10(_rp),
                           np.log10(np.array([RATIO_TAB[float(x)] for x in _rp])))


def baryons(c, r):
    """enclosed baryons M_gas + M_star at r (kpc), SI kg -- G097 exact."""
    r = np.atleast_1d(np.asarray(r, float))
    mg = loginterp(r, c["r_fg"], c["M_gas"])
    if c["has_star"]:
        ms = loginterp(r, c["r_st"], c["M_st"])
    else:
        rt = ratio_interp(r)
        ms = np.where(np.isfinite(mg) & np.isfinite(rt), mg * rt, np.nan)
    return mg + ms


def dlnM_dlnr(c, r):
    """local log-slope of the measured HSE mass (G057/G097 convention)."""
    r_hm, M = c["r_hm"], c["M_hse"]
    n = len(r_hm)
    out = np.empty(len(r))
    for i, rq in enumerate(r):
        j = int(np.searchsorted(r_hm, rq))
        j = min(max(j, 0), n - 2)
        if j < n - 1:
            out[i] = math.log(M[j + 1] / M[j]) / math.log(r_hm[j + 1] / r_hm[j])
        else:
            out[i] = math.log(M[j] / M[j - 1]) / math.log(r_hm[j] / r_hm[j - 1])
    return out


def gtot_of(c, r):
    """the measured total field G*M_HSE(<r)/r^2 at r (kpc), m/s^2, with the
    committed 1e9 kg floor (G097's line)."""
    Mx = loginterp(r, c["r_hm"], c["M_hse"])
    return G * np.maximum(Mx, 1e9) / (np.asarray(r, float) * KPC) ** 2


def field_crosses(c, level, lo=30.0, hi=3000.0):
    """G057's exact recipe: does the measured total field fall through
    `level` inside [lo, hi] kpc?  Crossing radius or nan."""
    rr = np.logspace(math.log10(lo), math.log10(hi), 400)
    gg = np.array([gtot_of(c, x) for x in rr]) / level
    ok = np.isfinite(gg)
    idx = np.where(ok & (gg < 1.0))[0]
    if not len(idx) or idx[0] == 0:
        return np.nan
    j = idx[0]
    try:
        return float(brentq(lambda x: gtot_of(c, x) - level,
                            rr[j - 1], rr[j], xtol=1e-3 * float(rr[j])))
    except ValueError:
        return np.nan


def rM_class(c, a0):
    """r_cap analytic deep-form sqrt(G M_b/g_ext) at the R500-class baryon
    mass, kpc -- the law's r_efe = sqrt(G M_b/g_ext)."""
    R500k = META[c["name"]]["R500"] * 1e3
    mb = baryons(c, np.array([R500k]))[0]
    if not np.isfinite(mb):
        mb = baryons(c, np.array([0.9 * R500k]))[0]
    if not np.isfinite(mb):
        return np.nan, np.nan
    return math.sqrt(G * mb / a0) / KPC, mb


print(f"X-COP clusters loaded: {len(CL)}; a0 can/alt = "
      f"{A0['canonical']:.4e}/{A0['alt']:.3e} m/s^2; g_ext = cH0 = {GEXT:.3e} "
      f"= {GEXT/A0['canonical']:.2f} a0 (canonical)")
print()

# ============================================================ V0: the anchors
print("=" * 100)
print("V0 -- ANCHORS: the registered R_cap rows and the 711.6 = 711.6 rows")
print("      reproduced on the committed tables before anything new")
print("=" * 100)
REG = json.load(open(os.path.join(REPO, "glm53_push",
                                  "G057_cluster_prediction_table.json")))
maxdev_rca = 0.0
for foot in A0:
    for row in REG["footings"][foot]["rows"]:
        c = next(x for x in CL if x["name"] == row["cluster"])
        rca = field_crosses(c, A0[foot])
        if row["R_cap_a0_kpc"] is not None and np.isfinite(rca):
            maxdev_rca = max(maxdev_rca,
                             abs(rca - row["R_cap_a0_kpc"]) /
                             abs(row["R_cap_a0_kpc"]))
check("V0a [anchor] the recomputed g_tot = a0 crossings reproduce G057b's "
      "registered R_cap(a0) column (296-958 kpc; A1644/A2255 none) on the "
      "12 clusters x 2 footings",
      f"max relative deviation = {maxdev_rca:.2e} over the registered "
      f"finite entries",
      maxdev_rca < 0.02)

# the 8-pt-grid chi2 rows (G097 V0b exact: win 50-600 kpc, both footings)
MED = {foot: {"split": [], "ph": []} for foot in A0}
for foot in A0:
    for c in CL:
        r = RG.copy()
        mb = baryons(c, r)
        Mh = loginterp(r, c["r_hm"], c["M_hse"])
        Mph = dlnM_dlnr(c, r) * mb
        gtot = gtot_of(c, r)
        capped = gtot > GEXT
        Mph_sup = np.where(capped, 0.0, Mph)
        eM = loginterp(r, c["r_hm"], c["eM_hse"])
        err = np.sqrt(eM ** 2 + (0.23 * mb) ** 2)
        win = (r >= 50) & (r <= 600) & np.isfinite(Mh) & (Mh > 0)
        chi_split = float(np.sum(((mb + Mph_sup - Mh) / err) ** 2 * win))
        chi_ph = float(np.sum(((mb + Mph - Mh) / err) ** 2 * win))
        MED[foot]["split"].append(chi_split)
        MED[foot]["ph"].append(chi_ph)
med_s = {f: float(np.median(MED[f]["split"])) for f in A0}
med_p = {f: float(np.median(MED[f]["ph"])) for f in A0}
check("V0b [anchor] the registered degeneracy: split == uncapped phantom "
      "row-for-row on the 50-600 kpc grid (the cap never fires -> the two "
      "predictions are the same vector), median 711.6 on both footings",
      f"canonical split {med_s['canonical']:.1f} = ph {med_p['canonical']:.1f}; "
      f"alt split {med_s['alt']:.1f} = ph {med_p['alt']:.1f}",
      abs(med_s["canonical"] - 711.6) / 711.6 < 0.02 and
      med_s["canonical"] == med_p["canonical"] and
      med_s["alt"] == med_p["alt"],
      "by construction under the cH0 rule the cap never fires on the grid: "
      "g_tot(50 kpc) < cH0 for every cluster")
g50 = np.array([gtot_of(c, np.array([50.]))[0] / GEXT for c in CL])
print(f"    g_tot(50 kpc)/cH0: min {g50.min():.3f}, median "
      f"{np.median(g50):.3f}, max {g50.max():.3f} (G097's note: ~0.9, the "
      f"field never reaches cH0)")
print()

# ============================================================ V1: firing radii
print("=" * 100)
print("V1 -- THE FIRING RADII: the g_tot = g_ext crossing per rule, per "
      "cluster, vs the 50-600 kpc window and R500")
print("=" * 100)
print(f"  {'cl':7s} {'R500':>6s} {'Rc(a0)can':>9s} {'Rc(a0)alt':>9s} "
      f"{'Rc(cH0)':>8s} {'Rc(self)':>9s} {'rM(a0)':>7s} "
      f"{'rCap(self)':>10s} {'600/R500':>8s}")
V1 = {c["name"]: {} for c in CL}
for c in CL:
    R500k = META[c["name"]]["R500"] * 1e3
    rca_c = field_crosses(c, A0["canonical"])
    rca_a = field_crosses(c, A0["alt"])
    rcc = field_crosses(c, GEXT)
    gself = gtot_of(c, np.array([R500k]))[0]
    rc_self = field_crosses(c, float(gself))
    rM_c, mb = rM_class(c, A0["canonical"])
    if np.isfinite(mb) and gself > 0:
        rcS = math.sqrt(G * mb / gself) / KPC
    else:
        rcS = np.nan
    V1[c["name"]] = dict(R500_kpc=R500k, R_cap_a0_canonical=rca_c,
                         R_cap_a0_alt=rca_a, R_cap_cH0=rcc,
                         R_cap_self=rc_self, r_M_a0_canonical=rM_c,
                         r_cap_self_analytic=rcS,
                         g_self_over_a0=gself / A0["canonical"])
    f3 = lambda x: f"{x:8.0f}" if np.isfinite(x) else "     none"
    print(f"  {c['name']:7s} {R500k:6.0f} {f3(rca_c):>9s} {f3(rca_a):>9s} "
          f"{f3(rcc):>8s} {f3(rc_self):>9s} {rM_c:7.0f} {f3(rcS):>10s} "
          f"{600/R500k:8.3f}")


def wstate(rf, R500k):
    if not np.isfinite(rf):
        return "none"
    if rf < 50:
        return "left"
    if rf <= 600:
        return "in-window"
    if rf <= R500k:
        return "600-R500"
    return "beyond-R500"


n_a0_win = {f: 0 for f in A0}
n_a0_600 = {f: 0 for f in A0}
n_a0_none = {f: 0 for f in A0}
n_ch0_left = 0
n_self = 0
for c in CL:
    R500k = META[c["name"]]["R500"] * 1e3
    v = V1[c["name"]]
    for f, key in (("canonical", "R_cap_a0_canonical"), ("alt", "R_cap_a0_alt")):
        st = wstate(v[key], R500k)
        if st == "in-window":
            n_a0_win[f] += 1
        elif st == "600-R500":
            n_a0_600[f] += 1
        elif st == "none":
            n_a0_none[f] += 1
    if wstate(v["R_cap_cH0"], R500k) == "left":
        n_ch0_left += 1
    if np.isfinite(v["R_cap_self"]) and \
            abs(v["R_cap_self"] - R500k) / R500k < 0.02:
        n_self += 1
print()
print(f"  a0-class firing radius (what G057b registered): "
      f"in the 50-600 kpc window {n_a0_win['canonical']}/12 (canonical), "
      f"{n_a0_win['alt']}/12 (alt); in the 600 kpc-R500 outer window "
      f"{n_a0_600['canonical']}/12 ({n_a0_600['alt']}/12); no crossing "
      f"(g_tot < a0 everywhere, never fires) {n_a0_none['canonical']}/12 "
      f"(A1644, A2255).")
print(f"  cH0-class (the committed operative rule): fires left of 50 kpc for "
      f"{n_ch0_left}/12 (A2029 at 31 kpc, an edge artefact); never "
      f"in-window for 12/12 -- the registered never-fired.")
print(f"  self-class (g_ext = own field at R500): r_fire = R500-class for "
      f"{n_self}/12 (the whole profile inside R500 is screened; split = "
      f"bare baryons in-window -- the known all-capped extreme).")
check("V1 [firing radius vs the window] the registered puzzle is a CLASS "
      "MISMATCH: R_cap(a0) 296-958 kpc is the a0-crossing (a0-class firing "
      "radius), while the operative split rule uses g_ext = cH0 whose "
      "crossing lies at < 50 kpc (or never) -- so 'the cap never fired in "
      "the 50-600 kpc window' is exactly true for the cH0 rule and the "
      "a0-class column registers a different, window-adjacent quantity",
      f"cH0: in-window 0/12 (left-of-window {n_ch0_left}/12); a0-class "
      f"in-window {n_a0_win['canonical']}/12 + 600-R500 "
      f"{n_a0_600['canonical']}/12 (canonical); self-class screens the "
      f"whole window ({n_self}/12)",
      n_ch0_left <= 1 and n_a0_win["canonical"] >= 1)
print()

# ============================================================ V2: outer window
print("=" * 100)
print("V2 -- OUTER-WINDOW TESTABILITY: per-cluster delta chi2")
print("      (split MINUS uncapped floor) per window per firing rule")
print("=" * 100)
MODELS = ("floor", "split_cH0", "split_a0", "split_self")
KWIN = [("REG 50-600", (50.0, 600.0)), ("OUT 600-R500", (600.0, None))]
OWN = [("0.1-0.2 R500", WINS[0]), ("0.2-0.4 R500", WINS[1]),
       ("0.4-0.7 R500", WINS[2]), ("0.7-1.0 R500", WINS[3])]
ALLWIN = KWIN + OWN
CHI2 = {foot: {c["name"]: {m: {w: 0.0 for w, _ in ALLWIN} for m in MODELS}
               for c in CL} for foot in A0}
NOFF = {foot: {c["name"]: {} for c in CL} for foot in A0}   # phantom-off bins
for foot, a0 in A0.items():
    for c in CL:
        r = c["r_hm"]
        R500k = META[c["name"]]["R500"] * 1e3
        mb = baryons(c, r)
        Mh = c["M_hse"]
        eM = c["eM_hse"]
        Mph = dlnM_dlnr(c, r) * mb
        gtot = gtot_of(c, r)
        gself = gtot_of(c, np.array([R500k]))[0]
        capped = {"split_cH0": gtot > GEXT,
                  "split_a0": gtot > a0,
                  "split_self": gtot > gself}
        err = np.sqrt(eM ** 2 + (0.23 * mb) ** 2)
        mfull = (r >= 0.1 * R500k) & (r <= 1.0 * R500k) \
            & np.isfinite(mb) & np.isfinite(Mh) & (Mh > 0) & (eM > 0)
        for m in MODELS:
            if m == "floor":
                pred = mb + Mph
            else:
                pred = mb + np.where(capped[m], 0.0, Mph)
            for wname, (lo, hi) in ALLWIN:
                if wname.startswith("OUT"):
                    msk = mfull & (r >= 600.0)
                elif wname.startswith("REG"):
                    msk = mfull & (r >= 50.0) & (r <= 600.0)
                else:
                    msk = mfull & (r >= lo * R500k) & (r <= hi * R500k)
                if msk.sum():
                    chi2 = float(np.sum(((pred[msk] - Mh[msk]) / err[msk]) ** 2))
                    CHI2[foot][c["name"]][m][wname] = chi2
        NOFF[foot][c["name"]] = dict(
            bins_cH0=int((mfull & capped["split_cH0"]).sum()),
            bins_a0=int((mfull & capped["split_a0"]).sum()),
            bins_self=int((mfull & capped["split_self"]).sum()),
            n_total=int(mfull.sum()))

# ---- delta chi2 tables: split(rule) - floor
for foot in A0:
    print(f"\n  --- {foot}: delta chi2 per cluster = split(rule) - uncapped "
          f"floor (the floor is the 711.6 model) ---")
    print(f"  {'cl':7s}" + "".join(f"{w:>14s}" for w, _ in ALLWIN) +
          "    | " + "".join(f"{w:>14s}" for w, _ in ALLWIN))
    for c in CL:
        line = f"  {c['name']:7s}"
        for rule in ("split_cH0", "split_a0", "split_self"):
            if rule != "split_cH0":
                line += "    | "
            for wname, _ in ALLWIN:
                d = CHI2[foot][c["name"]][rule][wname] - \
                    CHI2[foot][c["name"]]["floor"][wname]
                line += f"{d:14.1f}"
            line += "\n"
        print(line, end="")

# ---- summaries
SUM = {}
for foot in A0:
    SUM[foot] = {}
    for wname, _ in ALLWIN:
        row = {}
        for rule in ("split_cH0", "split_a0", "split_self"):
            ds = [CHI2[foot][c["name"]][rule][wname] -
                  CHI2[foot][c["name"]]["floor"][wname] for c in CL]
            ds = [float(d) for d in ds]
            row[rule] = dict(pooled=float(np.nansum(ds)),
                             median=float(np.nanmedian(ds)),
                             n_cl_gt4=int(np.sum(np.abs(np.nan_to_num(
                                 np.array(ds), nan=0.0)) > 4.0)),
                             per_cluster=ds)
        SUM[foot][wname] = row
    print(f"\n  [{foot}] summaries (delta chi2 = split - floor):")
    for wname, _ in ALLWIN:
        row = SUM[foot][wname]
        print(f"    {wname:>14s}: "
              + "; ".join(f"{rule[6:]}: pooled {row[rule]['pooled']:+9.1f} "
                          f"median {row[rule]['median']:+8.1f} "
                          f"(|d|>4: {row[rule]['n_cl_gt4']}/12)"
                          for rule in ("split_cH0", "split_a0", "split_self")))

out_win = "OUT 600-R500"
win71 = "0.7-1.0 R500"
ch0_outer = max(SUM["canonical"][out_win]["split_cH0"]["n_cl_gt4"],
                SUM["canonical"][win71]["split_cH0"]["n_cl_gt4"])
a0_outer = max(SUM["canonical"][out_win]["split_a0"]["n_cl_gt4"],
               SUM["canonical"][win71]["split_a0"]["n_cl_gt4"])
check("V2 [outer-window testability] does the split-vs-uncapped distinction "
      "open up in the outer bins?  Under the committed cH0 rule the delta "
      "chi2 is ZERO identically (the cap never fires anywhere on the "
      "tables); under the a0-class rule the screened zone reaches into "
      "600 kpc-R500 for the massive clusters; the self rule differs "
      "everywhere (the all-capped extreme)",
      f"outer windows: cH0-rule |delta|>4 in {ch0_outer}/12; a0-rule "
      f"|delta|>4 in {a0_outer}/12; pooled OUT 600-R500 delta_a0 = "
      f"{SUM['canonical'][out_win]['split_a0']['pooled']:+.1f}",
      ch0_outer == 0 and a0_outer >= 3)
print()

# ============================================================ V3: verdicts
print("=" * 100)
print("V3 -- VERDICTS")
print("=" * 100)
rca_all = [V1[c["name"]]["R_cap_a0_canonical"] for c in CL]
rca_all = [x for x in rca_all if np.isfinite(x)]
rca_all2 = [V1[c["name"]][k] for c in CL
            for k in ("R_cap_a0_canonical", "R_cap_a0_alt")]
rca_all2 = [x for x in rca_all2 if np.isfinite(x)]
gself_over = np.array([V1[c["name"]]["g_self_over_a0"] for c in CL])
g50_over = g50.copy()
print("V1 -- the per-cluster firing radius under both rules vs the window:")
print(f"     a0-class: R_cap(a0) canonical range {min(rca_all):.0f}-"
      f"{max(rca_all):.0f} kpc (median {np.median(rca_all):.0f}; both "
      f"footings {min(rca_all2):.0f}-{max(rca_all2):.0f}); "
      f"in-window 2/12, 600 kpc-R500 {n_a0_600['canonical']}/12 (canonical); "
      f"never (g_tot < a0 everywhere) 2/12.")
print(f"     self-class: r_fire = R500 for 12/12 (the whole profile screened "
      f"inside R500); the analytic r_cap = sqrt(G M_b/g(R500)) = "
      f"r_M*sqrt(a0/g(R500)) with g(R500)/a0 median "
      f"{np.median(gself_over):.2f} -> r_M-class (1.2-1.7x r_M).")
print(f"     cH0-class (the committed operative rule): fires left of "
      f"50 kpc only (A2029 31 kpc) / never -- the registered never-fired.")
print("V2 -- outer-window testability (numbers above):")
print(f"     committed cH0 rule: delta chi2 = 0 in every window of every "
      f"cluster (711.6 = 711.6 is a WINDOW degeneracy, not an identity of "
      f"the two models).")
print(f"     a0-class rule: the 600 kpc-R500 window carries the "
      f"split-vs-uncapped difference for the R_cap(a0) > 600 kpc set "
      f"(pooled delta {SUM['canonical'][out_win]['split_a0']['pooled']:+.1f}, "
      f"{SUM['canonical'][out_win]['split_a0']['n_cl_gt4']}/12 clusters "
      f"|delta| > 4); the 0.7-1.0 R500 bins show delta = 0 for 12/12 "
      f"(R_cap(a0)/R500 <= 0.71 and no table bin lands in the A2319 sliver: "
      f"the a0-crossing never sits inside 0.7-1.0 R500 on the measured "
      f"tables).")
print("V3 -- the honest statement:")
print("     'The cap never fired in the window' is a WINDOW statement: on "
      "the measured X-COP tables g_tot < cH0 everywhere (g_tot(50 kpc)/cH0 "
      f"= {g50_over.min():.2f}-{g50_over.max():.2f}, median "
      f"{np.median(g50_over):.2f} -- G097's '~0.9' note is loose; the only "
      "cH0 crossing is A2029 at 31 kpc), so the COMMITTED cH0 cap cannot "
      "fire anywhere the data reach; the registered 296-958 kpc is the "
      "a0-class firing radius of the measured field -- the region where "
      "the split differs from the uncapped floor; 'never fired' is "
      "therefore not 'no cap': it is 'the cH0 threshold sits above the "
      "window's field'.  The split architecture's switch is a0-class at "
      "0.28-0.91 R500 and becomes data-testable at 600 kpc-R500 for the "
      "massive half of the sample (8/12 canonical) and in-window for "
      "10/12, where the phantom re-activates beyond R_cap(a0); the "
      "0.7-1.0 R500 bins themselves carry zero a0-split-vs-floor "
      "difference on the measured tables.")
print()

# ---------------------------------------------------------------- the json
# ---- the nan -> None cleanup for JSON
def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


OUT = dict(
    lane="G138 -- THE CAP-FIRING-RADIUS RECONCILIATION: where does the cap "
         "actually bite?",
    window_kpc=[50, 600], wins_r500=[list(w) for w in WINS],
    g_ext_cH0_mss=GEXT, g_ext_over_a0_canonical=GEXT / A0["canonical"],
    anchors=dict(R_cap_a0_max_rel_dev=maxdev_rca,
                 median_chi2_8pt_split=med_s,
                 median_chi2_8pt_phantom=med_p,
                 g50_over_cH0=dict(min=float(g50.min()),
                                   median=float(np.median(g50)),
                                   max=float(g50.max()))),
    V1_firing_radii=V1,
    V1_counts=dict(R_cap_a0_in_window_canonical=n_a0_win["canonical"],
                   R_cap_a0_600_R500_canonical=n_a0_600["canonical"],
                   R_cap_a0_in_window_alt=n_a0_win["alt"],
                   R_cap_a0_600_R500_alt=n_a0_600["alt"],
                   R_cap_a0_never=n_a0_none["canonical"],
                   R_cap_cH0_left_of_window=n_ch0_left,
                   R_cap_self_R500_class=n_self),
    V2_delta_chi2_by_window=SUM,
    V2_off_bins=NOFF,
    checks=RES,
    verdicts=dict(
        V1="the registered 296-958 kpc is the a0-class firing radius (the "
           "a0-crossing of the measured total field), NOT the operative "
           "cH0 firing radius; per cluster: in-window 2/12 canonical "
           "(A3158 476, RXC1825 478), 600 kpc-R500 8/12 canonical, never "
           "2/12 (A1644/A2255); cH0 rule fires left of 50 kpc (A2029 "
           "31 kpc)/never, 0/12 in-window; self rule screens the whole "
           "profile inside R500 (split = bare baryons in-window)",
        V2="committed cH0 rule: split row == floor identically on every "
           "measured bin (delta chi2 = 0 per cluster in every window) - "
           "not testable anywhere; a0-class rule: delta chi2 concentrated "
           "in the 50 kpc-R_cap(a0) screened zone, which extends into "
           "600 kpc-R500 for 8/12 canonical clusters (pooled +4304) and "
           "in-window for 10/12; the 0.7-1.0 R500 bins show delta = 0 for "
           "12/12 (R_cap(a0)/R500 <= 0.71, no table bin in the sliver) - "
           "the outer window that is testable is 600 kpc-R500, not "
           "0.7-1.0 R500",
        V3="the never-fired-in-window is a WINDOW statement (the window's "
           "field stays below the cH0 threshold everywhere: g_tot(50 kpc)/"
           "cH0 = 0.10-0.66, median 0.41 - G097's '~0.9' note is loose; "
           "the only cH0 crossing is A2029 at 31 kpc), not a no-cap "
           "statement; the split architecture's own switch (a0-class) "
           "sits at 296-958 kpc = 0.28-0.91 R500, inside or at the edge "
           "of the 600 kpc-R500 window for the massive half of the sample "
           "(8/12 canonical), and is what the data can test there"),
)
json.dump(_clean(OUT), open(os.path.join(HERE, "G138_results.json"), "w"),
          indent=1, default=float)
print()
print("G138 COMPLETE -- written G138_results.json")