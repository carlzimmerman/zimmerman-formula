"""CFG88 sensitivities S1-S4 exactly as frozen in CFG88_SPEC_FROZEN.txt (reported only; no gates).  Imports cfg88.py (my own).  Run: python3 cfg88_sens.py"""
import math, json, sys, numpy as np
import cfg88 as C
from cfg88 import Cfg, row, offsets, med, load, load_collins, calib_set, predict, mstar_from_MV
ufd, cls, lvd, lf = load(); col = load_collins(); CAL = calib_set(lf)
P = {"ufd": ufd, "classical": cls, "m31lvd": lvd, "collins": col}
LOG = []
def out(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)
def line(tag, cfg, pops=("ufd", "classical", "m31lvd", "collins"), foot=("canonical",)):
    parts = []
    for f in foot:
        for p in pops:
            r = row(P[p], cfg.copy(foot=f, phi=1.0), CAL, True)
            parts.append(f"{p[:5]}{'/alt' if f=='alt' else ''} {r['off']:+.3f} ({r['z']:+.2f}s,e={r['tot']:.3f})")
    out(f"{tag:34s} " + " | ".join(parts))
out("=== S1 concentration (rule rows; offset (z, total error)) ===")
for k in C.CONC: line(k, Cfg(conc=k))
out("\n=== S1b concentration, alt footing ===")
for k in C.CONC: line(k, Cfg(conc=k), foot=("alt",))
out("\n=== S2 kernel (law rows too) ===")
for k in C.KERNELS:
    laws = [row(P[p], Cfg(kernel=k, phi=0.0), CAL, False) for p in ("ufd", "classical", "m31lvd", "collins")]
    out(f"{k:8s} LAW  " + " | ".join(f"{p[:5]} {r['off']:+.3f}({r['z']:+.2f}s)" for p, r in zip(("ufd", "classical", "m31lvd", "collins"), laws)))
    line(f"{k:8s} RULE", Cfg(kernel=k))
out("\n=== S3 Moster clamp value (every satellite the clamp touches) and unclamped ===")
for v in (1e8, 3e8, 1e9, 3e9, 1e10): line(f"clamp = {v:.0e}", Cfg(clamp=v))
line("unclamped extension (grid to 1e6)", Cfg(unclamped=True))
out("\n=== S3b UFD KM median vs collapse mass set ONLY for M_* < 1e5 satellites (CFG42's R1 scan) ===")
cu = np.array([s["ul"] for s in ufd])
for v in (3e7, 1e8, 2e8, 3e8, 1e9, 6e9, 1e10):
    out(f"    small_mcoll = {v:.0e}: UFD {med(offsets(ufd, Cfg(small_mcoll=v), CAL), cu):+.3f}   (M31 LVD {med(offsets(lvd, Cfg(small_mcoll=v), CAL), np.zeros(len(lvd), bool)):+.3f})")
out("\n=== S4 M31 LVD sample and conventions (rule offset, z with the frozen recipe; law offset) ===")
def s4(tag, sysl, cfg=Cfg(), law=True):
    r = row(sysl, cfg.copy(phi=1.0), CAL, True); l = row(sysl, cfg.copy(phi=0.0), CAL, False)
    ra = row(sysl, cfg.copy(phi=1.0, foot="alt"), CAL, True)
    out(f"{tag:46s} n={len(sysl):2d} RULE {r['off']:+.3f} ({r['z']:+.2f}s, e {r['tot']:.3f}) alt {ra['off']:+.3f} ({ra['z']:+.2f}s) | LAW {l['off']:+.3f}")
    return r
s4("all 34 (frozen)", lvd)
dE = {"M 32", "NGC 147", "NGC 185", "NGC 205"}
s4("minus 4 dwarf ellipticals", [s for s in lvd if s["name"] not in dE])
s4("only host m_031 (drop And XXII m_033, And XVIII)", [s for s in lvd if s["host"] == "m_031"])
s4("M_V >= -9 (drop the 9 brightest)", [s for s in lvd if s["MV"] >= -9])
s4("R_e < 1000 pc", [s for s in lvd if s["Re_pc"] < 1000])
s4("M_V > -7.7 (UFD-like, n small)", [s for s in lvd if s["MV"] > -7.7])
s4("M_V <= -7.7 (classical-like)", [s for s in lvd if s["MV"] <= -7.7])
s4("rhalf_physical (major axis) not circularised", lvd, Cfg(re_key="Re_maj_pc"))
for g in ("A1", "A2", "none", "ulatlimit"): s4(f"gas convention {g}", lvd, Cfg(gas=g))
# Collins overlap with each source's own data
def cname(n): return n.replace("Andromeda ", "And ").strip()
cmap = {s["name"]: s for s in col}
ov_l = [s for s in lvd if cname(s["name"]) in cmap]; ov_c = [cmap[cname(s["name"])] for s in ov_l]
s4("overlap with Collins: LVD data", ov_l); s4("overlap with Collins: Collins data (own D, R_e, sigma)", ov_c)
dl = []
for a, b in zip(ov_l, ov_c):
    dl.append((a["name"], a["dist"], b["dist"], a["Re_pc"], b["Re_pc"], a["sig"], b["sig"], a["MV"], b["MV"]))
out("   overlap details (name, D_LVD, D_Col, Re_LVD, Re_Col, sig_LVD, sig_Col, MV_LVD, MV_Col):")
for d in dl: out("     %-16s %6.0f %6.0f  %6.0f %6.0f  %5.1f %5.1f  %6.2f %6.2f" % d)
# distance swap: keep the LVD sigma and apparent magnitude, rescale R_e and M_V to Collins' distance
sw = []
for a, b in zip(ov_l, ov_c):
    f = b["dist"] / a["dist"]; t = dict(a); t["Re_pc"] = a["Re_pc"] * f; t["Re_maj_pc"] = a["Re_maj_pc"] * f; t["MV"] = a["MV"] - 5 * math.log10(f); sw.append(t)
s4("overlap: LVD data at Collins' distances", sw)
# leave-one-out
base = row(lvd, Cfg(), CAL, True); x = offsets(lvd, Cfg(), CAL); cz = np.zeros(len(lvd), bool)
loo = [(float(np.median(np.delete(x, i))), lvd[i]["name"]) for i in range(len(lvd))]
loo.sort(); out(f"   leave-one-out median range: {loo[0][0]:+.3f} ({loo[0][1]}) .. {loo[-1][0]:+.3f} ({loo[-1][1]}); full {float(np.median(x)):+.3f}")
# error-recipe diagnostics (reported only)
out("\n=== error-recipe diagnostics for the M31 LVD rule (post hoc, reported only) ===")
r = row(lvd, Cfg(), CAL, True); x = r["x"]
out(f"   offsets: median {np.median(x):+.4f} mean {x.mean():+.4f} std {x.std(ddof=1):.3f}; SE(mean) = {x.std(ddof=1)/math.sqrt(len(x)):.4f}; SE(median)~1.2533 SE(mean) = {1.2533*x.std(ddof=1)/math.sqrt(len(x)):.4f}")
out(f"   bootstrap stat {r['stat']:.4f}; U floor {r['fU']:.4f}; C floor {r['fC']:.4f}; total {r['tot']:.4f}; z = {r['z']:+.2f}")
for lab, e in (("stat only", r["stat"]), ("stat + C floor", math.hypot(r["stat"], r["fC"])), ("SE(mean) only", x.std(ddof=1) / math.sqrt(len(x))),
               ("total (frozen)", r["tot"])):
    out(f"   z with error = {lab:16s} {e:.4f}: {r['off']/e:+.2f}")
open("cfg88_sens.out", "w").write("\n".join(LOG) + "\n")
