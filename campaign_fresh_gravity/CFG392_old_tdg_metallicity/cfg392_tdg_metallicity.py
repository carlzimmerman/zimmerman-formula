#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG392 -- old tidal-dwarf (TDG) candidates selected by gas metallicity, against the RAR.

Criteria frozen first in FROZEN_CRITERIA.md (commit cccb2275f).  Departures are listed in README.md.

The settling working model: an old TDG (metal-rich for its mass, formed from pre-enriched disc gas) has a phantom
target but no catchment for the cold fluid, so it is Newtonian and sits BELOW the RAR by -log10 nu(g_bar/a0).
Plain modified gravity: it sits ON the RAR.  Metal-rich-for-mass is only a proxy for TDG origin.

Sample: SPARC dwarfs (Q < 3, Inc >= 30, M_b = 0.5 L36 + 1.33 M_HI < 1e10 Msun).
Metallicities (one source per galaxy, priority): Berg+2012 (direct; arXiv source tables 5 and 7, positions from 1/6)
> van Zee & Haynes 2006 (J/ApJ/636/214 tables 1, 6) > Hunter+2012 LITTLE THINGS (J/AJ/144/134, measured only)
> Pilyugin+2014 (J/AJ/147/131, O/H at 0.4 R25).
kappa = 1/2 FITTED; both footings (9.3603e-11 / 1.1312e-10).  MUTATE=1: flagged galaxies' g_obs -> g_bar.
"""
import os
import re
import sys
import json
import math
import builtins

import numpy as np
from scipy import stats

LANE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(LANE))
import CFG4_common as c4                                     # noqa: E402

c4.HERE = LANE                                               # Run writes its .out / .json into THIS lane dir
DD = os.path.join(LANE, "data")
ALIASFIX = os.environ.get("CFG392_ALIAS", "0") == "1"       # POST-FREEZE disclosed sensitivity (README departure D2)
SLUG = "cfg392_tdg_metallicity" + ("_aliasfix" if ALIASFIX else "")
R = c4.Run(SLUG, lane="CFG392")
P = R.P
MUT = c4.MUTATE
A0 = c4.A0
FOOTS = c4.FOOTS
KPC = c4.KPC
LOG_GCUT = -10.5
FLAG_PRI, FLAG_SEC = 0.40, 0.30
NBOOT = 20000
POS_TOL_ARCMIN = 1.0
# hand cross-identifications used ONLY in the post-freeze alias-fix run (each also checked against positions < 3')
HAND_ALIAS = [("IC 2574", "UGC 5666", "DDO 81"), ("NGC 2366", "UGC 3851", "DDO 42"), ("NGC 4214", "UGC 7278"),
              ("NGC 3741", "UGC 6572"), ("NGC 4068", "UGC 7047"), ("NGC 5204", "UGC 8490"), ("NGC 4395", "UGC 7524"),
              ("WLM", "UGCA 444", "DDO 221"), ("Holmberg II", "UGC 4305", "DDO 50"), ("NGC 2552", "UGC 4325")]


# ================================================================================================ helpers
def norm(s):
    s = s.upper().replace(" ", "").replace("-", "").replace("_", "")
    m = re.match(r"^([A-Z]+)0*(\d+)(.*)$", s)
    if m:
        s = m.group(1) + m.group(2) + m.group(3)
    return s


def sex2deg(ra, dec):
    dec = re.sub(r"^(-?\d+)\.(\d+):", r"\1:\2:", dec.strip())         # Berg's '45.59:30' typo (NGC 2537)
    h, m, s = [float(x) for x in ra.strip().split(":")]
    sg = -1.0 if dec.strip().startswith("-") else 1.0
    d, dm, ds = [abs(float(x)) for x in dec.strip().lstrip("+-").split(":")]
    return 15.0 * (h + m / 60 + s / 3600), sg * (d + dm / 60 + ds / 3600)


def sep_arcmin(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(math.radians, (ra1, de1, ra2, de2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c)))) * 60.0


def fcol(line, a, b):
    t = line[a - 1:b].strip()
    return float(t) if t else None


# ================================================================================================ catalogues
def load_berg():
    tex = builtins.open(os.path.join(DD, "berg2012_Berg0109.v7.tex"), encoding="latin-1").read()

    def table(num):
        m = re.search(r"\\tablenum\{%d\}.*?\\startdata(.*?)\\enddata" % num, tex, re.S)
        if m is None and num == 1:
            m = re.search(r"Low-Luminosity LVL Sample\}.*?\\startdata(.*?)\\enddata", tex, re.S)
        rows = []
        for ln in m.group(1).split("\n"):
            ln = ln.split("%")[0]
            if "&" not in ln or "multicolumn" in ln:
                continue
            rows.append([c.strip() for c in ln.replace("\\\\", "").split("&")])
        return rows

    pos = {}
    for num in (1, 6):
        for r in table(num):
            try:
                pos[norm(r[0])] = sex2deg(r[1], r[2])
            except Exception:
                pass
    out = []
    for num, col in ((5, 2), (7, 1)):
        for r in table(num):
            m = re.match(r"([\d.]+)\$\\pm\$([\d.]+)", r[col].replace(" ", ""))
            if not m:
                continue
            nm = r[0]
            ra, de = pos.get(norm(nm), (None, None))
            out.append(dict(src="Berg12", name=nm, alias={norm(nm)}, ra=ra, dec=de, oh=float(m.group(1)),
                            eoh=float(m.group(2)), note=f"table{num}"))
    return out


def load_vanzee():
    out = []
    for ln in builtins.open(os.path.join(DD, "vanzee2006_table1.dat")):
        if len(ln.strip()) < 50:
            continue
        nm = ln[0:12].strip()
        ra = 15 * (fcol(ln, 14, 15) + fcol(ln, 17, 18) / 60 + fcol(ln, 20, 23) / 3600)
        sg = -1 if ln[24] == "-" else 1
        de = sg * (fcol(ln, 26, 27) + fcol(ln, 29, 30) / 60 + fcol(ln, 32, 35) / 3600)
        out.append(dict(src="vZH06", name=nm, alias={norm(nm)}, ra=ra, dec=de, oh=fcol(ln, 91, 94),
                        eoh=fcol(ln, 96, 99), note="table1"))
    for ln in builtins.open(os.path.join(DD, "vanzee2006_table6.dat")):
        if len(ln.strip()) < 30:
            continue
        nm = ln[0:9].strip()
        out.append(dict(src="vZH06", name=nm, alias={norm(nm)}, ra=None, dec=None, oh=fcol(ln, 49, 52),
                        eoh=fcol(ln, 54, 57), note="table6"))
    return out


def load_hunter():
    out, excl = [], []
    for ln in builtins.open(os.path.join(DD, "hunter2012_table1.dat")):
        ln = ln.rstrip("\n").ljust(158)
        nm = ln[4:13].strip()
        if not nm:
            continue
        al = {norm(nm)}
        ugc = ln[30:35].strip()
        if ugc:
            al.add("UGC" + str(int(ugc)))
        for a, b in ((37, 50), (52, 64), (66, 85)):
            t = ln[a - 1:b].strip()
            if t:
                al.add(norm(t))
        oh = fcol(ln, 148, 150)
        e = ln[151:155].strip()
        rec = dict(src="Hunter12", name=nm, alias=al, ra=None, dec=None, oh=oh, eoh=float(e) if e else None,
                   note="measured" if ln[145] != "*" else "EMPIRICAL(*)")
        (excl if ln[145] == "*" or oh is None else out).append(rec)
    return out, excl


def load_pilyugin():
    pos = {}
    for ln in builtins.open(os.path.join(DD, "pilyugin2014_table1.dat")):
        if len(ln) < 40:
            continue
        pos[ln[0:9].strip()] = (fcol(ln, 21, 30), fcol(ln, 32, 41))
    out = []
    for ln in builtins.open(os.path.join(DD, "pilyugin2014_table2.dat")):
        if len(ln) < 30:
            continue
        nm = ln[0:9].strip()
        oh0, e0, grad = fcol(ln, 11, 14), fcol(ln, 16, 19), fcol(ln, 21, 26)
        ra, de = pos.get(nm, (None, None))
        out.append(dict(src="Pily14", name=nm, alias={norm(nm)}, ra=ra, dec=de, oh=oh0 + 0.4 * grad, eoh=e0,
                        note=f"O/H(0)={oh0:.2f} grad={grad:+.3f}/R25"))
    return out


# ================================================================================================ SPARC + match
R.banner("CFG392  old-TDG candidates by metallicity vs the RAR" + ("   [MUTATE: flagged g_obs -> g_bar]" if MUT else ""))
gals = c4.load_sparc()
R.check("C1 loader: 175 SPARC galaxies; footings 9.3603e-11 / 1.1312e-10",
        f"N={len(gals)}, a0={A0['canonical']:.4e}/{A0['alt']:.4e}",
        len(gals) == 175 and abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15)
SPOS = json.load(builtins.open(os.path.join(c4.DATA, "sparc_positions_merged.json")))

dw = []
for g in gals:
    m = g["meta"]
    if m is None or m["Q"] >= 3 or m["Inc"] < 30:
        continue
    Mst = 0.5 * m["L36"] * 1e9
    Mb = Mst + 1.33 * m["MHI"] * 1e9
    if Mb >= 1e10 or Mst <= 0:
        continue
    g.update(Mst=Mst, Mb=Mb, fgas=1.33 * m["MHI"] * 1e9 / Mb)
    dw.append(g)
P(f"  SPARC dwarfs after cuts (Q<3, Inc>=30, M_b<1e10): {len(dw)}")

berg = load_berg()
vzh = load_vanzee()
hun, hun_excl = load_hunter()
pil = load_pilyugin()
SOURCES = [("Berg12", berg), ("vZH06", vzh), ("Hunter12", hun), ("Pily14", pil)]
P(f"  catalogue entries with O/H: Berg12 {len(berg)}, vZH06 {len(vzh)}, Hunter12 measured {len(hun)} "
  f"(empirical '*' excluded: {len(hun_excl)}), Pily14 {len(pil)}")
R.num("n_catalogue", {k: len(v) for k, v in SOURCES})

EQUIV = {}
if ALIASFIX:
    POS_TOL_ARCMIN = 2.0
    groups = [set(e["alias"]) for e in hun + hun_excl] + [{norm(x) for x in t} for t in HAND_ALIAS]
    for grp in groups:
        for a in grp:
            EQUIV.setdefault(a, set()).update(grp)
    P(f"  ALIAS-FIX (post-freeze): position tolerance {POS_TOL_ARCMIN}'; {len(groups)} alias groups "
      f"(Hunter cross-IDs + {len(HAND_ALIAS)} hand groups)")
match_rows, audit_bad = [], []
for g in dw:
    sp = SPOS.get(g["name"])
    gn = norm(g["name"])
    geq = EQUIV.get(gn, set()) | {gn}
    g["oh"] = None
    for sname, cat in SOURCES:
        hits = []
        for e in cat:
            byname = bool(geq & e["alias"])
            sep = None
            if sp is not None and e["ra"] is not None:
                sep = sep_arcmin(sp["ra"], sp["dec"], e["ra"], e["dec"])
            bypos = sep is not None and sep < POS_TOL_ARCMIN
            if byname or bypos:
                hits.append((e, byname, bypos, sep))
        if len({id(h[0]) for h in hits}) > 1:
            audit_bad.append(f"{g['name']}: {sname} has {len(hits)} entries {[h[0]['name'] for h in hits]}")
        if hits and g["oh"] is None:
            e, byname, bypos, sep = hits[0]
            if byname and sep is not None and sep > 3.0:
                audit_bad.append(f"{g['name']}: name match to {e['name']} but separation {sep:.1f}'")
            g.update(oh=e["oh"], eoh=e["eoh"], ohsrc=sname, ohname=e["name"])
            match_rows.append(dict(sparc=g["name"], source=sname, cat_name=e["name"], oh=e["oh"], eoh=e["eoh"],
                                   by_name=byname, by_pos=bypos, sep_arcmin=None if sep is None else round(sep, 2),
                                   note=e["note"]))
# reverse uniqueness: no catalogue entry used for two SPARC galaxies
used = {}
for r in match_rows:
    used.setdefault((r["source"], r["cat_name"]), []).append(r["sparc"])
for k, v in used.items():
    if len(v) > 1:
        audit_bad.append(f"{k} matched to {v}")
P("\n  match table (SPARC -> chosen source):")
P(f"  {'SPARC':12s} {'src':9s} {'catalogue':14s} {'O/H':>5s} {'err':>5s} name pos  sep'  note")
for r in match_rows:
    P(f"  {r['sparc']:12s} {r['source']:9s} {r['cat_name']:14s} {r['oh']:5.2f} {r['eoh'] if r['eoh'] is not None else float('nan'):5.2f} "
      f"{'Y' if r['by_name'] else '-':4s} {'Y' if r['by_pos'] else '-':3s} "
      f"{'' if r['sep_arcmin'] is None else r['sep_arcmin']:5}  {r['note']}")
with builtins.open(os.path.join(LANE, "match_table" + ("_aliasfix" if ALIASFIX else "") + ".csv"), "w") as fh:
    fh.write("sparc,source,cat_name,oh,eoh,by_name,by_pos,sep_arcmin,note\n")
    for r in match_rows:
        fh.write(",".join(str(r[k]) for k in ("sparc", "source", "cat_name", "oh", "eoh", "by_name", "by_pos",
                                               "sep_arcmin", "note")) + "\n")
R.check("C2 match audit: no SPARC galaxy with two entries of a source, no entry used twice, no name/position conflict",
        f"{len(match_rows)} matched; problems: {audit_bad if audit_bad else 'none'}", not audit_bad)

# ================================================================================================ residuals
def gal_points(g, foot, kern, gobs_newton=False):
    Rk, V, eV = g["R"], g["Vobs"], g["eV"]
    vb2 = g["Vgas"] * np.abs(g["Vgas"]) + 0.5 * g["Vdisk"] * np.abs(g["Vdisk"]) + 0.7 * g["Vbul"] * np.abs(g["Vbul"])
    ok = (Rk > 0) & (V > 0) & (vb2 > 0)
    gobs_true = (V[ok] * 1e3) ** 2 / (Rk[ok] * KPC)
    gbar = vb2[ok] * 1e6 / (Rk[ok] * KPC)
    gobs = gbar.copy() if gobs_newton else gobs_true
    nu = kern(gbar / A0[foot])
    r = np.log10(gobs) - np.log10(nu * gbar)
    sig = np.sqrt(((2 / math.log(10)) * eV[ok] / V[ok]) ** 2 + 0.05 ** 2)
    return dict(r=r, sig=sig, lognu=np.log10(nu), lgbar=np.log10(gbar), gobs=gobs, gobs_true=gobs_true)


def wmean(x, s):
    w = 1 / s ** 2
    return float(np.sum(w * x) / np.sum(w))


def per_gal(sample, foot, kern, which, newton_set=frozenset()):
    res, exp_, names = [], [], []
    for g in sample:
        d = gal_points(g, foot, kern, gobs_newton=g["name"] in newton_set)
        sel = d["lgbar"] < LOG_GCUT if which == "low" else np.ones_like(d["r"], bool)
        if which == "low" and sel.sum() < 3:
            continue
        res.append(wmean(d["r"][sel], d["sig"][sel]))
        exp_.append(-wmean(d["lognu"][sel], d["sig"][sel]))
        names.append(g["name"])
    return names, np.array(res), np.array(exp_)


def delta_boot(rf, ru, seed=392):
    rng = np.random.default_rng(seed)
    D = np.median(rf) - np.median(ru)
    bf = rng.integers(0, len(rf), (NBOOT, len(rf)))
    bu = rng.integers(0, len(ru), (NBOOT, len(ru)))
    Db = np.median(rf[bf], axis=1) - np.median(ru[bu], axis=1)
    return float(D), float(np.std(Db))


def verdict(D, s, nf):
    if nf < 5:
        return "NON-DISCRIMINATING"
    if D + 3 * s < -0.15:
        return "SUPPORTED"
    if D - 2 * s > -0.15:
        return "DISFAVOURED"
    return "NON-DISCRIMINATING"


# ================================================================================================ MZR (before residuals)
ana = [g for g in dw if g["oh"] is not None]
lm = np.array([math.log10(g["Mst"]) for g in ana])
oh = np.array([g["oh"] for g in ana])
fit = stats.linregress(lm, oh)
ts = stats.theilslopes(oh, lm)
for g, x, y in zip(ana, lm, oh):
    g["dz"] = y - (fit.intercept + fit.slope * x)
    g["dz_ts"] = y - (ts[1] + ts[0] * x)
scat = float(np.std([g["dz"] for g in ana], ddof=2))
R.banner("MZR (own sample, M* = 0.5 L36) -- defined before any RAR residual is computed")
P(f"  N = {len(ana)};  OLS: 12+log(O/H) = {fit.intercept:.3f} + {fit.slope:.3f} log M*  (slope err {fit.stderr:.3f}); "
  f"scatter {scat:.3f} dex")
P(f"  Theil-Sen: intercept {ts[1]:.3f}, slope {ts[0]:.3f}")
R.num("mzr", dict(N=len(ana), intercept=fit.intercept, slope=fit.slope, slope_err=fit.stderr, scatter=scat,
                  ts_intercept=ts[1], ts_slope=ts[0]))
srcoff = {s: float(np.median([g["dz"] for g in ana if g["ohsrc"] == s])) for s, _ in SOURCES
          if any(g["ohsrc"] == s for g in ana)}
srcn = {s: sum(g["ohsrc"] == s for g in ana) for s, _ in SOURCES}
P(f"  per-source N {srcn}; median MZR residual by source {json.dumps({k: round(v, 3) for k, v in srcoff.items()})}")
R.num("source_N", srcn)
R.num("source_median_mzr_residual", srcoff)
flag = {thr: {g["name"] for g in ana if g["dz"] >= thr} for thr in (FLAG_PRI, FLAG_SEC)}
flag_ts = {g["name"] for g in ana if g["dz_ts"] >= FLAG_PRI}
P(f"  flagged >= +0.40 dex: {len(flag[FLAG_PRI])}  {sorted(flag[FLAG_PRI])}")
P(f"  flagged >= +0.30 dex: {len(flag[FLAG_SEC])}  {sorted(flag[FLAG_SEC])}")
P(f"  flagged >= +0.40 dex (Theil-Sen MZR): {len(flag_ts)}  {sorted(flag_ts)}")
R.num("flagged_040", sorted(flag[FLAG_PRI]))
R.num("flagged_030", sorted(flag[FLAG_SEC]))
P("\n  analysis galaxies (log M*, f_gas, O/H, src, MZR residual):")
for g in sorted(ana, key=lambda g: -g["dz"]):
    P(f"   {g['name']:12s} logM*={math.log10(g['Mst']):5.2f} fgas={g['fgas']:.2f} O/H={g['oh']:.2f} {g['ohsrc']:8s} "
      f"dZ={g['dz']:+.3f}{'  FLAG' if g['dz'] >= FLAG_PRI else ('  flag0.3' if g['dz'] >= FLAG_SEC else '')}")

# ================================================================================================ the test
R.banner("RAR residuals: flagged minus unflagged (median), bootstrap over galaxies")
newton = flag[FLAG_PRI] if MUT else frozenset()
# C3: the g_obs actually used is the observed one
mx = 0.0
for g in ana:
    d = gal_points(g, "canonical", c4.nu_mono, gobs_newton=g["name"] in newton)
    mx = max(mx, float(np.max(np.abs(np.log10(d["gobs"]) - np.log10(d["gobs_true"])))))
R.check("C3 g_obs used is the observed Vobs^2/R (max |dlog g_obs| = 0)", f"{mx:.3e} dex", mx == 0.0)

rows, VERD = [], {}
for kname, kern in (("nu_mono", c4.nu_mono), ("P2", c4.nu_p2)):
    for which in ("low", "all"):
        for thr in (FLAG_PRI, FLAG_SEC):
            for foot in FOOTS:
                names, res, ex = per_gal(ana, foot, kern, which, newton)
                fl = np.array([n in flag[thr] for n in names])
                nf, nu_ = int(fl.sum()), int((~fl).sum())
                if nf == 0 or nu_ == 0:
                    D, s = float("nan"), float("nan")
                else:
                    D, s = delta_boot(res[fl], res[~fl])
                pred = float(np.median(ex[fl]) - np.median(res[~fl])) if nf else float("nan")
                v = verdict(D, s, nf) if nf else "NON-DISCRIMINATING"
                row = dict(kernel=kname, points=which, flag=thr, foot=foot, N_flag=nf, N_unflag=nu_,
                           med_flag=float(np.median(res[fl])) if nf else None, med_unflag=float(np.median(res[~fl])),
                           Delta=D, sigma=s, settle_pred_Delta=pred,
                           settle_E_median=float(np.median(ex[fl])) if nf else None, verdict=v)
                rows.append(row)
                if kname == "nu_mono" and which == "low" and thr == FLAG_PRI:
                    VERD[foot] = v
                    R.num(f"primary_{foot}", row)
                    P(f"  PRIMARY [{foot}] flagged {nf} ({sorted(np.array(names)[fl])})")
                    for n_, r_, e_ in zip(np.array(names)[fl], res[fl], ex[fl]):
                        P(f"      {n_:12s} residual {r_:+.3f}   settling expectation (-log nu) {e_:+.3f}")
P(f"\n  {'kernel':8s} {'pts':4s} {'flag':5s} {'foot':10s} {'Nf':>3s} {'Nu':>3s} {'med_f':>7s} {'med_u':>7s} {'Delta':>7s} "
  f"{'sigma':>6s} {'pred':>7s}  verdict")
for r in rows:
    P(f"  {r['kernel']:8s} {r['points']:4s} {r['flag']:5.2f} {r['foot']:10s} {r['N_flag']:3d} {r['N_unflag']:3d} "
      f"{(r['med_flag'] if r['med_flag'] is not None else float('nan')):+7.3f} {r['med_unflag']:+7.3f} {r['Delta']:+7.3f} "
      f"{r['sigma']:6.3f} {r['settle_pred_Delta']:+7.3f}  {r['verdict']}")
R.num("rows", rows)
overall = VERD["canonical"] if VERD["canonical"] == VERD["alt"] else "NON-DISCRIMINATING"
P(f"\n  VERDICT (nu_mono, g_bar < 1e-10.5, flag >= 0.40): canonical {VERD['canonical']}, alt {VERD['alt']}  ->  {overall}")
R.num("verdict", dict(per_foot=VERD, overall=overall))

# Theil-Sen-flag variant (reported)
for foot in FOOTS:
    names, res, ex = per_gal(ana, foot, c4.nu_mono, "low", newton)
    fl = np.array([n in flag_ts for n in names])
    if fl.sum() and (~fl).sum():
        D, s = delta_boot(res[fl], res[~fl])
        P(f"  Theil-Sen flags [{foot}]: Nf {int(fl.sum())}, Delta {D:+.3f} +- {s:.3f} -> {verdict(D, s, int(fl.sum()))}")
        R.num(f"theilsen_{foot}", dict(N_flag=int(fl.sum()), Delta=D, sigma=s, verdict=verdict(D, s, int(fl.sum()))))

# ================================================================================================ controls
R.banner("controls")
names, res_all, _ = per_gal(ana, "canonical", c4.nu_mono, "all")
dwn, dw_all, _ = per_gal(dw, "canonical", c4.nu_mono, "all")
R.check("C4 sanity: median per-galaxy residual of all dwarfs (all points, canonical) within |0.15| dex",
        f"{np.median(dw_all):+.3f} dex over {len(dw_all)} dwarfs (matched subset {np.median(res_all):+.3f}, N {len(res_all)})",
        abs(np.median(dw_all)) < 0.15, load_bearing=False)
inj = {}
for foot in FOOTS:
    names, res, ex = per_gal(ana, foot, c4.nu_mono, "low", flag[FLAG_PRI])
    fl = np.array([n in flag[FLAG_PRI] for n in names])
    if fl.sum() and (~fl).sum():
        D, s = delta_boot(res[fl], res[~fl])
        inj[foot] = (D, s, verdict(D, s, int(fl.sum())))
    else:
        inj[foot] = (float("nan"), float("nan"), "NO FLAGGED")
R.num("injection", inj)
R.check("C5 power: Newtonian injection on the flagged set returns SUPPORTED on both footings",
        "; ".join(f"{f}: Delta {v[0]:+.3f} +- {v[1]:.3f} -> {v[2]}" for f, v in inj.items()),
        all(v[2] == "SUPPORTED" for v in inj.values()), load_bearing=False,
        reading="says whether the frozen test can see a fully Newtonian flagged set at this N")

inj3 = {}
for foot in FOOTS:
    names, res, ex = per_gal(ana, foot, c4.nu_mono, "low", flag[FLAG_SEC])
    fl = np.array([n in flag[FLAG_SEC] for n in names])
    if fl.sum() and (~fl).sum():
        D, s = delta_boot(res[fl], res[~fl])
        inj3[foot] = (D, s, verdict(D, s, int(fl.sum())))
R.num("injection_flag030", inj3)
P(f"  (reported extra) Newtonian injection on the 0.30-dex flags: {inj3}")
names, res, _ = per_gal(ana, "canonical", c4.nu_mono, "low")
byn = {g["name"]: g for g in ana}
fl = np.array([n in flag[FLAG_PRI] for n in names])
conf = {}
for key, fn in (("fgas", lambda g: g["fgas"]), ("logMst", lambda g: math.log10(g["Mst"])),
                ("fD", lambda g: g["meta"]["fD"]), ("Inc", lambda g: g["meta"]["Inc"]),
                ("D_Mpc", lambda g: g["meta"]["D"])):
    a = [fn(byn[n]) for n in np.array(names)[fl]]
    b = [fn(byn[n]) for n in np.array(names)[~fl]]
    conf[key] = (float(np.median(a)) if a else None, float(np.median(b)) if b else None)
dz = np.array([byn[n]["dz"] for n in names])
rho = stats.spearmanr(dz, res)
P(f"  C6 confounders (flagged vs unflagged medians, primary sample): {json.dumps(conf)}")
P(f"  C6 Spearman(MZR residual, RAR residual) over {len(names)} galaxies: rho = {rho.correlation:+.3f}, p = {rho.pvalue:.3f}")
R.num("confounders", dict(medians=conf, spearman_rho=float(rho.correlation), spearman_p=float(rho.pvalue),
                          N=len(names)))
R.check("C6 confounders reported", "see medians and Spearman above", True, load_bearing=False)
if MUT:
    P(f"  MUTATE: verdict with flagged g_obs -> g_bar is {overall} (must be SUPPORTED)")
    R.num("mutate_verdict", overall)
sys.exit(R.finish())
