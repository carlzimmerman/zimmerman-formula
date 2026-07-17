#!/usr/bin/env python3
"""
scout_split.py -- DATA SCOUT for the TRGB lever on the a0-line.
Splits the gas-dominated dwarf subsample by SPARC distance-method flag fD and quantifies
the selection difference between the high-quality-distance (TRGB fD=2, Cepheid fD=3)
galaxies and the Hubble-flow (fD=1) galaxies. This decides whether a TRGB-restricted a0
is a clean measurement or needs range-matching against the Hubble-flow set.

Reuses fire_common.load (SPARC-standard cuts Q<=2, inc>=30, eV/Vobs<10%, gas-dom point cut
Vgas^2 > Ud*Vdisk^2 + Ub*Vbul^2). Fiducial Ud=0.5. READ-ONLY on frozen repo. Exit 0.
Credit: Lelli-McGaugh-Schombert 2016 (SPARC); McGaugh+2016 g_dagger=1.2e-10 (comparison).
"""
import sys, os, csv, json
import numpy as np

sys.path.insert(0, "/Users/carlzimmerman/new_physics/prep_2026/a0_line")
import fire_common as fc

OUT = "/Users/carlzimmerman/new_physics/prep_2026/a0_line_trgb"
REPO = fc.REPO
A0C, A0A = fc.A0C, fc.A0A          # canonical 9.355e-11 / alt 1.1305e-10
UD = 0.50                          # fiducial disk M/L
FD_NAME = {1: "Hubble-flow", 2: "TRGB", 3: "Cepheid", 4: "UMa-cluster", 5: "SNIa"}

# ---- galaxy-level metadata (D, Vflat, luminosity, HI mass, type) from master csv ----
gmeta = {}
with open(os.path.join(REPO, "data", "sparc_master_clean.csv")) as fh:
    for r in csv.DictReader(fh):
        gmeta[r["name"]] = dict(
            D=float(r["D_Mpc"]), fD=int(r["fD"]), Vflat=float(r["Vflat"]),
            L36=float(r["L36"]), MHI=float(r["MHI"]), T=float(r["T"]))

# ---- load the sample, keep only galaxies that CONTRIBUTE gas-dominated points ----
gals = fc.load(UD)
sub = []
for g in gals:
    m = g["gasdom"]
    if m.sum() == 0:
        continue
    name = g["name"]
    gm = gmeta[name]
    gb = g["gb"][m]
    go = g["go"][m]
    y = gb / A0C                                    # dimensionless x = g_bar/a0 (canonical)
    # baryonic mass proxy: Mbar = Ud*L36 + 1.33*MHI  (1e9 Msun units in csv; 1.33 = He)
    Mbar = UD * gm["L36"] + 1.33 * gm["MHI"]
    sub.append(dict(
        name=name, fD=gm["fD"], D=gm["D"], Vflat=gm["Vflat"], Mbar=Mbar,
        npts=int(m.sum()), y=y, gb=gb, ymin=float(y.min()), ymax=float(y.max()),
        straddle=bool((y.min() < 1.0) and (y.max() > 1.0))))

# ---- per-fD aggregation ----
def rng(a):
    a = np.asarray(a, float)
    return float(a.min()), float(a.max())

groups = {}
for fd in sorted(set(s["fD"] for s in sub)):
    G = [s for s in sub if s["fD"] == fd]
    allY = np.concatenate([s["y"] for s in G])
    D = [s["D"] for s in G]
    Vf = [s["Vflat"] for s in G if s["Vflat"] > 0]
    Mb = [s["Mbar"] for s in G if s["Mbar"] > 0]
    groups[fd] = dict(
        fd=fd, name=FD_NAME.get(fd, f"fD={fd}"),
        Ngal=len(G), Npts=int(sum(s["npts"] for s in G)),
        gals=[s["name"] for s in G],
        D_rng=rng(D), Vf_rng=rng(Vf) if Vf else (0, 0),
        Mb_rng=rng(Mb) if Mb else (0, 0),
        y_rng=(float(allY.min()), float(allY.max())),
        y_med=float(np.median(allY)),
        frac_below1=float(np.mean(allY < 1.0)),
        frac_above1=float(np.mean(allY > 1.0)),
        n_straddle=int(sum(s["straddle"] for s in G)),
        sample_straddles=bool(allY.min() < 1.0 and allY.max() > 1.0))

bar = "=" * 90
lines = []
def out(s=""):
    print(s); lines.append(s)

out(bar)
out("SCOUT: gas-dominated dwarf subsample split by SPARC distance flag fD  (Ud=%.2f)" % UD)
out("a0-line lever: TRGB(fD=2)/Cepheid(fD=3) carry sigma_lnD=0.05 vs Hubble-flow(fD=1)=0.25")
out(bar)
out("%-14s %5s %6s | %-13s | %-13s | %-15s | %-17s | y-straddle" % (
    "fD group", "Ngal", "Npts", "D [Mpc]", "Vflat [km/s]", "Mbar [1e9 Msun]",
    "y=g_bar/a0 range"))
out("-" * 118)
for fd in sorted(groups):
    G = groups[fd]
    out("%-14s %5d %6d | %5.1f - %6.1f | %5.1f - %6.1f | %6.2f - %7.2f | %6.3f - %8.2f | %s (%d gal)" % (
        "%d %s" % (fd, G["name"]), G["Ngal"], G["Npts"],
        G["D_rng"][0], G["D_rng"][1], G["Vf_rng"][0], G["Vf_rng"][1],
        G["Mb_rng"][0], G["Mb_rng"][1], G["y_rng"][0], G["y_rng"][1],
        "YES" if G["sample_straddles"] else "NO", G["n_straddle"]))

# ---- HQ (fD in 2,3) vs Hubble-flow (fD=1) selection-bias comparison ----
hq = [s for s in sub if s["fD"] in (2, 3)]
hf = [s for s in sub if s["fD"] == 1]
def summ(S):
    if not S:
        return None
    allY = np.concatenate([s["y"] for s in S])
    D = np.array([s["D"] for s in S])
    Vf = np.array([s["Vflat"] for s in S if s["Vflat"] > 0])
    Mb = np.array([s["Mbar"] for s in S if s["Mbar"] > 0])
    return dict(Ngal=len(S), Npts=int(sum(s["npts"] for s in S)),
                D_med=float(np.median(D)), D_rng=rng(D),
                Vf_med=float(np.median(Vf)) if len(Vf) else 0.0,
                Vf_rng=rng(Vf) if len(Vf) else (0, 0),
                Mb_med=float(np.median(Mb)) if len(Mb) else 0.0,
                Mb_rng=rng(Mb) if len(Mb) else (0, 0),
                y_med=float(np.median(allY)), y_rng=(float(allY.min()), float(allY.max())),
                frac_above1=float(np.mean(allY > 1.0)),
                straddles=bool(allY.min() < 1 and allY.max() > 1))
Shq, Shf = summ(hq), summ(hf)

out()
out(bar)
out("SELECTION-BIAS ASSESSMENT: HQ-distance (TRGB+Cepheid, fD 2,3) vs Hubble-flow (fD 1)")
out(bar)
for tag, S in (("HQ (fD 2,3)", Shq), ("Hubble-flow (fD 1)", Shf)):
    if S is None:
        out("  %-20s : EMPTY" % tag); continue
    out("  %-20s: Ngal=%d Npts=%d | D med=%.1f rng[%.1f,%.1f] | Vflat med=%.0f rng[%.0f,%.0f]"
        % (tag, S["Ngal"], S["Npts"], S["D_med"], S["D_rng"][0], S["D_rng"][1],
           S["Vf_med"], S["Vf_rng"][0], S["Vf_rng"][1]))
    out("  %-20s  Mbar med=%.2f rng[%.2f,%.2f]e9 | y med=%.3f rng[%.3f,%.2f] | frac(y>1)=%.2f | straddle=%s"
        % ("", S["Mb_med"], S["Mb_rng"][0], S["Mb_rng"][1], S["y_med"],
           S["y_rng"][0], S["y_rng"][1], S["frac_above1"], S["straddles"]))

if Shq and Shf:
    out()
    out("  DELTA (HQ / Hubble-flow ratios of medians):")
    out("    distance    : %.2fx  (HQ closer? %s)" % (
        Shq["D_med"] / Shf["D_med"], "yes" if Shq["D_med"] < Shf["D_med"] else "no"))
    out("    Vflat       : %.2fx" % (Shq["Vf_med"] / Shf["Vf_med"] if Shf["Vf_med"] else float("nan")))
    out("    Mbar        : %.2fx" % (Shq["Mb_med"] / Shf["Mb_med"] if Shf["Mb_med"] else float("nan")))
    out("    y (g_bar/a0): %.2fx  (median acceleration probe)" % (Shq["y_med"] / Shf["y_med"]))
    # power check: does the HQ set have enough baseline + y-lever to discriminate footings?
    out()
    out("  POWER / CONDITIONING for a0 fit on the HQ subsample:")
    out("    HQ y-range spans %.3f -> %.2f : %s y=1 (needed to condition the slope a0)" % (
        Shq["y_rng"][0], Shq["y_rng"][1], "STRADDLES" if Shq["straddles"] else "DOES NOT straddle"))
    gap = abs(A0A - A0C) / A0C
    out("    footing gap to resolve: canonical %.3e vs alt %.3e = %.1f%%" % (A0C, A0A, 100 * gap))
    out("    HQ has %d gas-dom points across %d galaxies (banked full gas set ~310/49)." % (
        Shq["Npts"], Shq["Ngal"]))

json.dump(dict(
    Ud=UD, a0_canon=A0C, a0_alt=A0A,
    groups={int(fd): {k: v for k, v in g.items() if k != "gals"} for fd, g in groups.items()},
    group_galaxies={int(fd): g["gals"] for fd, g in groups.items()},
    hq_summary=Shq, hubbleflow_summary=Shf,
    n_total_gasdom_gals=len(sub), n_total_gasdom_pts=int(sum(s["npts"] for s in sub))),
    open(os.path.join(OUT, "scout_split.json"), "w"), indent=1, default=float)

out()
out("[scout_split.json written]  total gas-dom: %d gals / %d pts" % (
    len(sub), sum(s["npts"] for s in sub)))
out("EXIT 0: split computed. Exit code is not a verdict.")

# save a plain-text copy of the console for SCOUT.md assembly
open(os.path.join(OUT, "_scout_console.txt"), "w").write("\n".join(lines) + "\n")
