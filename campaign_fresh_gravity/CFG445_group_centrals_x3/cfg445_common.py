#!/usr/bin/env python3
"""CFG445 shared code: readers, cross-match, WALLABY baryon model, SPARC classes, the frozen statistics.
Criteria: FROZEN_CRITERIA.md (a1a2a05ac).  Lane-local; reads CFG393 data and CFG4_common read-only."""
import csv
import math
import os
import re
import sys

import numpy as np
from scipy.special import ellipk, ellipe, i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG4_common as C  # noqa: E402

D393 = os.path.join(CFG, "CFG393_group_catalogue_rar")
EXT393 = os.path.join(CFG, "_external_data", "cfg393")
DATA = os.path.join(HERE, "data")

LOGG_CUT = -10.5
MCUT = 12.5
MATCH_ARCSEC = 60.0
XSC_ARCSEC = 20.0
UPS_K = 0.6
MSUN_K = 3.28
GKPC = 4.30091e-6                     # kpc (km/s)^2 / Msun
G2SI = 1e6 / C.KPC                    # (km/s)^2/kpc -> m/s^2
SOFT = 0.1                            # kpc
NSUB = 600
WIN = 0.2


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def read_tsv(path):
    rows, hdr, stage = [], None, 0
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if hdr is None:
            hdr = [h.strip() for h in f]
            continue
        if stage < 2:
            stage += 1
            continue
        rows.append({h: (f[i].strip() if i < len(f) else "") for i, h in enumerate(hdr)})
    return rows


def unitvec(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.column_stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)])


def nearest_two(v, cv):
    d = (cv * v).sum(axis=1)
    i2 = np.argpartition(-d, 1)[:2]
    i2 = i2[np.argsort(-d[i2])]
    sep = np.degrees(np.arccos(np.clip(d[i2], -1, 1))) * 3600.0
    return int(i2[0]), sep[0], sep[1]


# ------------------------------------------------------------------------------------------------ group catalogues
class Groups:
    def __init__(self):
        kt3 = [r for r in read_tsv(os.path.join(D393, "data", "kt2017_table3.tsv")) if np.isfinite(fnum(r["RAJ2000"]))]
        kt2 = read_tsv(os.path.join(D393, "data", "kt2017_table2.tsv"))
        self.KTG = {r["PGC1"]: dict(logMK=fnum(r["logMK"]), logMd=fnum(r["logMd"]), Nm=int(fnum(r["Nm"])), Dg=fnum(r["Dist"]))
                    for r in kt2}
        self.kt3 = kt3
        self.KTV = unitvec(np.array([fnum(r["RAJ2000"]) for r in kt3]), np.array([fnum(r["DEJ2000"]) for r in kt3]))
        t5 = [r for r in read_tsv(os.path.join(EXT393, "t15_table5.tsv")) if np.isfinite(fnum(r["_RA.icrs"]))]
        t3 = read_tsv(os.path.join(D393, "data", "t15_table3.tsv"))
        self.T3 = {r["Nest"]: dict(Mlum=fnum(r["Mlum"]), PGC1=r["PGC1"], Nmb=int(fnum(r["Nmb"]))) for r in t3}
        self.t5 = t5
        self.T5V = unitvec(np.array([fnum(r["_RA.icrs"]) for r in t5]), np.array([fnum(r["_DE.icrs"]) for r in t5]))

    def match(self, ra, de):
        v = unitvec(np.array([ra]), np.array([de]))[0]
        rec = dict(cat="", pgc="", sep=np.nan, pgc1="", logMh=np.nan, logMd=np.nan, Nm=0, D=np.nan, flag="UNMATCHED")
        ik, s1k, s2k = nearest_two(v, self.KTV)
        if s1k <= MATCH_ARCSEC:
            if s2k <= MATCH_ARCSEC:
                rec.update(cat="KT2017", flag="AMBIGUOUS", sep=s1k)
                return rec
            r = self.kt3[ik]
            g = self.KTG.get(r["PGC1"], {})
            rec.update(cat="KT2017", pgc=r["PGC"], sep=s1k, pgc1=r["PGC1"], logMh=g.get("logMK", np.nan),
                       logMd=g.get("logMd", np.nan), Nm=g.get("Nm", 0), D=fnum(r["Dist"]), flag="OK" if g else "NOGROUP",
                       Dsrc="KT2017 galaxy", Dgrp=g.get("Dg", np.nan))
            if not np.isfinite(rec["D"]):                       # frozen: 'KT2017 table3 Dist, else T15 table5 Dist'
                it, s1t, s2t = nearest_two(v, self.T5V)
                if s1t <= MATCH_ARCSEC < s2t and np.isfinite(fnum(self.t5[it]["Dist"])):
                    rec.update(D=fnum(self.t5[it]["Dist"]), Dsrc="T15 galaxy")
            return rec
        it, s1t, s2t = nearest_two(v, self.T5V)
        if s1t <= MATCH_ARCSEC:
            if s2t <= MATCH_ARCSEC:
                rec.update(cat="T15", flag="AMBIGUOUS", sep=s1t)
                return rec
            r = self.t5[it]
            g = self.T3.get(r["Nest"], {})
            m = g.get("Mlum", np.nan)
            rec.update(cat="T15", pgc=r["PGC"], sep=s1t, pgc1=g.get("PGC1", r["PGC1"]),
                       logMh=(math.log10(m) if m and np.isfinite(m) and m > 0 else np.nan), Nm=g.get("Nmb", 0),
                       D=fnum(r["Dist"]), flag="OK" if g else "NOGROUP", Dsrc="T15 galaxy", Dgrp=np.nan)
        return rec


def classify(rec, mcut=MCUT, key="logMh"):
    m = rec.get(key, np.nan)
    if rec["flag"] != "OK" or not np.isfinite(m):
        return None
    if m < mcut:
        return "F"
    return "GC" if rec["pgc"] == rec["pgc1"] else "SAT"


# ------------------------------------------------------------------------------------------------ thin-disc forces
def ring_sum_g(Rsig, Sig, Reval, soft=SOFT, nsub=NSUB):
    """inward radial acceleration ((km/s)^2/kpc) of a razor-thin disc with Sigma (Msun/pc^2) given at radii Rsig (kpc),
    linearly interpolated, held at Sig[0] inside Rsig[0], zero beyond Rsig[-1]; evaluated at Reval (kpc)."""
    rmax = Rsig[-1]
    edges = np.linspace(0, rmax, nsub + 1)
    a = 0.5 * (edges[1:] + edges[:-1])
    dr = edges[1] - edges[0]
    s = np.interp(a, Rsig, Sig, left=Sig[0], right=0.0) * 1e6       # Msun/kpc^2
    m = s * 2 * np.pi * a * dr
    R = np.asarray(Reval, float)[:, None]
    z2 = soft ** 2
    den = (R + a) ** 2 + z2
    k2 = np.clip(4 * a * R / den, 0, 1 - 1e-12)
    K, E = ellipk(k2), ellipe(k2)
    g = (GKPC * m / (np.pi * R)) / np.sqrt(den) * (K - (a ** 2 - R ** 2 + z2) / ((a - R) ** 2 + z2) * E)
    return g.sum(axis=1)


def freeman_g(M, Rd, R):
    R = np.asarray(R, float)
    y = R / (2 * Rd)
    S0 = M / (2 * np.pi * Rd ** 2)
    v2 = 4 * np.pi * GKPC * S0 * Rd * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / R


# ------------------------------------------------------------------------------------------------ WALLABY
def _lst(s):
    return np.array([fnum(x) for x in s.split(",")]) if s else np.array([])


def _tr(s):
    m = re.search(r"TR(\d+)", s or "")
    return int(m.group(1)) if m else 0


def load_wallaby(groups):
    rows = list(csv.DictReader(open(os.path.join(DATA, "wallaby_dr2_kinematic_catalogue.csv"))))
    best = {}
    for r in rows:
        n = r["name"]
        if n not in best or _tr(r["team_release_kin"]) > _tr(best[n]["team_release_kin"]):
            best[n] = r
    src = {}
    for r in csv.DictReader(open(os.path.join(DATA, "wallaby_dr2_source_catalogue.csv"))):
        src.setdefault(r["name"], []).append(r)
    xsc = {}
    for line in open(os.path.join(DATA, "xsc_wallaby_cones.tsv"), encoding="utf-8"):
        if line.startswith("#") or line.startswith("wallaby_name"):
            continue
        f = line.rstrip("\n").split("\t")
        n, rr = f[0], fnum(f[1])
        if rr <= XSC_ARCSEC and (n not in xsc or rr < xsc[n]["r"]):
            xsc[n] = dict(r=rr, K=fnum(f[5]), reff=fnum(f[7]), id=f[2])
    out = []
    for n in sorted(best):
        r = best[n]
        g = dict(name=n, src="WALLABY", team=r["team_release_kin"], q=fnum(r["QFlag_model"]), inc=fnum(r["Inc_model"]),
                 ra=fnum(r["ra"]), dec=fnum(r["dec"]), rad=_lst(r["Rad"]), V=_lst(r["Vrot_model"]), eV=_lst(r["e_Vrot_model"]),
                 radsd=_lst(r["Rad_SD"]), sd=_lst(r["SD_FO_model"]), xsc=xsc.get(n), excl="")
        cands = src.get(n, [])
        same = [s for s in cands if s["team_release"] == r["team_release"]] or cands
        g["logMHI_cat"] = fnum(same[0]["log_m_hi"]) if same else np.nan
        g["dist_h"] = fnum(same[0]["dist_h"]) if same else np.nan
        g["rec"] = groups.match(g["ra"], g["dec"])
        if not (g["q"] <= 1):
            g["excl"] = "QFlag>1"
        elif not (g["inc"] >= 30):
            g["excl"] = "inc<30"
        elif g["xsc"] is None or not np.isfinite(g["xsc"]["K"]) or not np.isfinite(g["xsc"]["reff"]):
            g["excl"] = "no XSC"
        elif g["rec"]["flag"] != "OK":
            g["excl"] = "group " + g["rec"]["flag"]
        elif not (np.isfinite(g["rec"]["D"]) and g["rec"]["D"] > 0):
            g["excl"] = "no distance"
        out.append(g)
    return out


def wallaby_baryons(g, ups=UPS_K, soft=SOFT, D=None):
    """fills R (kpc), gbar (m/s^2) at the rotation-curve radii, logL (L_K, Lsun), M*, Rd."""
    D = g["rec"]["D"] if D is None else D
    akpc = D * 1e3 * math.pi / (180 * 3600)                          # kpc per arcsec
    R = g["rad"] * akpc
    Rs = g["radsd"] * akpc
    LK = 10 ** (-0.4 * (g["xsc"]["K"] - 5 * math.log10(D) - 25 - MSUN_K))
    Rd = g["xsc"]["reff"] * akpc / 1.678
    gg = ring_sum_g(Rs, 1.33 * g["sd"], R, soft=soft)
    gs = freeman_g(ups * LK, Rd, R)
    g.update(R=R, gbar=(gg + gs) * G2SI, ggas=gg * G2SI, gstar=gs * G2SI, LK=LK, logL=math.log10(LK), Rd=Rd, Mstar=ups * LK)
    return g


def hi_mass_check(g):
    """log10 of 2 pi int SD_FO R dR (no helium) at the source catalogue's dist_h."""
    D = g["dist_h"]
    akpc = D * 1e3 * math.pi / (180 * 3600)
    Rs = g["radsd"] * akpc * 1e3                                     # pc
    if len(Rs) < 2:
        return np.nan
    dR = np.median(np.diff(Rs))
    return math.log10(np.sum(g["sd"] * 2 * np.pi * Rs * dR))


# ------------------------------------------------------------------------------------------------ SPARC
def load_sparc_classes():
    mt = {}
    for r in csv.DictReader(open(os.path.join(D393, "cfg393_match_table.csv"))):
        rec = dict(cat=r["catalogue"], pgc=r["pgc"], pgc1=r["group_pgc1"], logMh=fnum(r["logMh_lum"]), logMd=fnum(r["logMd_KT"]),
                   flag=r["flag"])
        mt[r["sparc_name"]] = rec
    gal = C.load_sparc()
    return gal, mt


def sparc_gbar(g):
    R = g["R"] * C.KPC
    vb2 = g["Vgas"] * np.abs(g["Vgas"]) + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    return vb2 * 1e6 / R


# ------------------------------------------------------------------------------------------------ residuals
def resid(R_kpc, V, eV, gbar, a0, efloor=0.0):
    gobs = (V * 1e3) ** 2 / (R_kpc * C.KPC)
    ok = (V > 0) & (gbar > 0) & (np.log10(np.where(gbar > 0, gbar, 1)) < LOGG_CUT)
    if ok.sum() < 3:
        return None
    r = np.log10(gobs[ok]) - np.log10(gbar[ok] * C.nu_mono(gbar[ok] / a0))
    e = np.maximum(eV[ok], efloor)
    s = np.sqrt((0.8686 * e / V[ok]) ** 2 + 0.01 ** 2)
    w = 1.0 / s ** 2
    return float(np.sum(w * r) / np.sum(w)), int(ok.sum())


def n_outer(gbar, V):
    ok = (V > 0) & (gbar > 0) & (np.log10(np.where(gbar > 0, gbar, 1)) < LOGG_CUT)
    return int(ok.sum())


# ------------------------------------------------------------------------------------------------ frozen statistics
def delta_lm(Rv, cls, src, logL, win=WIN, idx_gc=None, idx_f=None):
    """luminosity-matched Delta.  Rv/cls/src/logL: arrays over the scoring sample.  idx_gc/idx_f: optional (bootstrap)
    index arrays into the sample (with replacement).  Returns (Delta, n_gc_used, per-GC d list)."""
    if idx_gc is None:
        idx_gc = np.where(cls == "GC")[0]
    if idx_f is None:
        idx_f = np.where(cls == "F")[0]
    d = []
    for i in idx_gc:
        f = idx_f[(src[idx_f] == src[i]) & (np.abs(logL[idx_f] - logL[i]) <= win)]
        if len(f):
            d.append(Rv[i] - np.median(Rv[f]))
    return (float(np.median(d)) if d else float("nan")), len(d), d


def boot_lm(Rv, cls, src, logL, rng, nb, win=WIN):
    gc = np.where(cls == "GC")[0]
    fl = np.where(cls == "F")[0]
    out = np.empty(nb)
    srcs = sorted(set(src))
    gcs = {s: gc[src[gc] == s] for s in srcs}
    fls = {s: fl[src[fl] == s] for s in srcs}
    for b in range(nb):
        ig = np.concatenate([rng.choice(gcs[s], len(gcs[s])) for s in srcs if len(gcs[s])])
        jf = np.concatenate([rng.choice(fls[s], len(fls[s])) for s in srcs if len(fls[s])])
        out[b] = delta_lm(Rv, cls, src, logL, win, ig, jf)[0]
    return out


def dbic_src(x, y, s, mcut=MCUT):
    x, y = np.asarray(x, float), np.asarray(y, float)
    N = len(y)
    srcs = sorted(set(s))
    S = np.column_stack([(np.asarray(s) == k).astype(float) for k in srcs])
    res = {}
    for nm, col in (("linear", x), ("step", (x >= mcut).astype(float))):
        X = np.column_stack([S, col])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        rss = float(np.sum((y - X @ beta) ** 2))
        res[nm] = dict(beta=beta.tolist(), rss=rss, bic=N * math.log(rss / N) + X.shape[1] * math.log(N))
    return res["linear"]["bic"] - res["step"]["bic"], res


def verdict(D, sig, dbic, ngc, nf):
    if ngc < 5 or nf < 20:
        return "NON-DISCRIMINATING (UNDERPOWERED)"
    if D > 0.05 and D / sig > 3 and dbic > 2:
        return "TWO-REGIME SUPPORTED"
    if D + 2 * sig < 0.05:
        return "NOT SUPPORTED"
    return "NON-DISCRIMINATING"


LADDER = {"NOT SUPPORTED": 0, "NON-DISCRIMINATING": 1, "NON-DISCRIMINATING (UNDERPOWERED)": 1, "TWO-REGIME SUPPORTED": 2}
