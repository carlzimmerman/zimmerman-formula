#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG393 -- group-catalogue RAR.  Do SPARC centrals of group-mass hosts (log M_h >= 12.5) sit ABOVE the RAR at large radius,
as a STEP in host mass?  Criteria frozen in FROZEN_CRITERIA.md (commit 3a57634c6) before this script existed.

kappa = 1/2 FITTED; both footings (CFG4_common.A0).  No dark-matter particle; the cold-fluid mass is still required.
Inputs: data/ (KT2017 table2/3, T15 table3, SPARC VizieR table1 positions) + the T15 table5 copy kept outside git
(../_external_data/cfg393/t15_table5.tsv; URL + sha256 in FETCH_LOG.md).  SPARC curves via CFG4_common.load_sparc().
Outputs (this directory): cfg393_group_rar.out, cfg393_group_rar_results.json, cfg393_match_table.csv
(MUTATE=1: *_MUTATE.out, *_results_MUTATE.json; the match table is not rewritten).
"""
import os
import sys
import json
import math
import builtins

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import CFG4_common as C  # noqa: E402  (read-only: loader, nu_mono, A0)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
EXT = os.path.join(os.path.dirname(HERE), "_external_data", "cfg393")
DATA = os.path.join(HERE, "data")

LOGG_CUT = -10.5            # points with g_bar < 10^-10.5 m/s^2
UPS_D, UPS_B = 0.5, 0.7
MCUT = 12.5
MATCH_ARCSEC = 60.0
NBOOT, NPERM, SEED = 20000, 5000, 393


# ------------------------------------------------------------------------------------------------ harness (lane-local)
class Tee:
    def __init__(self, path):
        self.f = builtins.open(path, "w", encoding="utf-8")
        self.o = sys.stdout

    def write(self, t):
        self.o.write(t)
        self.f.write(t)

    def flush(self):
        self.o.flush()
        self.f.flush()


OUTP = os.path.join(HERE, f"cfg393_group_rar{SUF}.out")
JSONP = os.path.join(HERE, f"cfg393_group_rar_results{SUF}.json")
tee = Tee(OUTP)
sys.stdout = tee
CH, NUM = [], {}


def P(*a):
    print(*a, flush=True)


def check(name, measured, ok, lb=True):
    CH.append((name, bool(ok), lb, str(measured)))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}\n         measured: {measured}")


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o) if np.isfinite(o) else str(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


# ------------------------------------------------------------------------------------------------ readers
def read_tsv(path):
    """VizieR asu-tsv: header line, units line, dashes line, then rows."""
    rows, hdr, stage = [], None, 0
    for line in builtins.open(path, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if hdr is None:
            hdr = [h.strip() for h in f]
            continue
        if stage < 2:                                 # units, dashes
            stage += 1
            continue
        rows.append({h: (f[i].strip() if i < len(f) else "") for i, h in enumerate(hdr)})
    return rows


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def unitvec(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    return np.column_stack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)])


def nearest_two(sv, cv):
    """for each SPARC unit vector, the nearest and second-nearest catalogue separations (arcsec) and the nearest index."""
    out = []
    for v in sv:
        d = (cv * v).sum(axis=1)            # explicit sum (Accelerate matmul raises spurious FP warnings)
        i2 = np.argpartition(-d, 1)[:2]
        i2 = i2[np.argsort(-d[i2])]
        sep = np.degrees(np.arccos(np.clip(d[i2], -1, 1))) * 3600.0
        out.append((int(i2[0]), sep[0], sep[1]))
    return out


P("=" * 118)
P(f"CFG393 group-catalogue RAR  (MUTATE={int(MUTATE)})  -- criteria FROZEN_CRITERIA.md (3a57634c6)")
P("=" * 118)

# SPARC positions (VizieR-computed J2000 from the Simbad name)
sp = read_tsv(os.path.join(DATA, "sparc_table1_pos.tsv"))
SPOS = {}
for r in sp:
    ra, de = fnum(r["_RAJ2000"]), fnum(r["_DEJ2000"])
    if np.isfinite(ra) and np.isfinite(de):
        SPOS[r["Name"]] = (ra, de)
P(f"SPARC VizieR table1: {len(sp)} rows, {len(SPOS)} with positions")

# KT2017
kt3 = read_tsv(os.path.join(DATA, "kt2017_table3.tsv"))
kt2 = read_tsv(os.path.join(DATA, "kt2017_table2.tsv"))
KTG = {r["PGC1"]: dict(logMK=fnum(r["logMK"]), logMd=fnum(r["logMd"]), Nm=int(fnum(r["Nm"])), assoc=r["PGC1+"]) for r in kt2}
# POST-HOC (declared in README, after C2 failed): association level = all KT2017 groups sharing PGC1+; mass = sum of logMK
ASSOC = {}
for _k, _g in KTG.items():
    ASSOC[_g["assoc"]] = ASSOC.get(_g["assoc"], 0.0) + 10 ** _g["logMK"]
kt3 = [r for r in kt3 if np.isfinite(fnum(r["RAJ2000"]))]
KTV = unitvec(np.array([fnum(r["RAJ2000"]) for r in kt3]), np.array([fnum(r["DEJ2000"]) for r in kt3]))
P(f"KT2017: table3 {len(kt3)} galaxies, table2 {len(KTG)} groups")

# T15
t5 = read_tsv(os.path.join(EXT, "t15_table5.tsv"))
t3 = read_tsv(os.path.join(DATA, "t15_table3.tsv"))
T3 = {r["Nest"]: dict(Mlum=fnum(r["Mlum"]), PGC1=r["PGC1"], Nmb=int(fnum(r["Nmb"]))) for r in t3}
t5 = [r for r in t5 if np.isfinite(fnum(r["_RA.icrs"]))]
T5V = unitvec(np.array([fnum(r["_RA.icrs"]) for r in t5]), np.array([fnum(r["_DE.icrs"]) for r in t5]))
P(f"T15: table5 {len(t5)} galaxies, table3 {len(T3)} groups")

# ------------------------------------------------------------------------------------------------ cross-match
names = sorted(SPOS)
sv = unitvec(np.array([SPOS[n][0] for n in names]), np.array([SPOS[n][1] for n in names]))
mk = nearest_two(sv, KTV)
mt = nearest_two(sv, T5V)
MATCH = {}
for n, (ik, s1k, s2k), (it, s1t, s2t) in zip(names, mk, mt):
    rec = dict(name=n, cat="", pgc="", sep=np.nan, group="", pgc1="", logMh=np.nan, logMd=np.nan, Nm=0, flag="",
               assoc="", logMa=np.nan)
    if s1k <= MATCH_ARCSEC:
        if s2k <= MATCH_ARCSEC:
            rec.update(cat="KT2017", flag="AMBIGUOUS", sep=s1k)
        else:
            r = kt3[ik]
            g = KTG.get(r["PGC1"], {})
            rec.update(cat="KT2017", pgc=r["PGC"], sep=s1k, group=r["PGC1"], pgc1=r["PGC1"], logMh=g.get("logMK", np.nan),
                       logMd=g.get("logMd", np.nan), Nm=g.get("Nm", 0), flag="OK" if g else "NOGROUP",
                       assoc=g.get("assoc", ""), logMa=(math.log10(ASSOC[g["assoc"]]) if g else np.nan))
    elif s1t <= MATCH_ARCSEC:
        if s2t <= MATCH_ARCSEC:
            rec.update(cat="T15", flag="AMBIGUOUS", sep=s1t)
        else:
            r = t5[it]
            g = T3.get(r["Nest"], {})
            m = g.get("Mlum", np.nan)
            rec.update(cat="T15", pgc=r["PGC"], sep=s1t, group=r["Nest"], pgc1=g.get("PGC1", r["PGC1"]),
                       logMh=(math.log10(m) if m and np.isfinite(m) and m > 0 else np.nan), Nm=g.get("Nmb", 0),
                       flag="OK" if g else "NOGROUP")
    else:
        rec["flag"] = "UNMATCHED"
    MATCH[n] = rec

if not MUTATE:
    with builtins.open(os.path.join(HERE, "cfg393_match_table.csv"), "w", encoding="utf-8") as fh:
        fh.write("sparc_name,catalogue,pgc,sep_arcsec,group_id,group_pgc1,logMh_lum,logMd_KT,Nm,flag\n")
        for n in names:
            r = MATCH[n]
            fh.write(f"{n},{r['cat']},{r['pgc']},{r['sep']:.1f},{r['group']},{r['pgc1']},{r['logMh']:.3f},{r['logMd']:.3f},"
                     f"{r['Nm']},{r['flag']}\n")
flags = {}
for r in MATCH.values():
    flags[(r["cat"], r["flag"])] = flags.get((r["cat"], r["flag"]), 0) + 1
P("cross-match tallies (catalogue, flag): " + ", ".join(f"{k[0] or '-'}/{k[1]} {v}" for k, v in sorted(flags.items())))
NUM["match_tallies"] = {f"{k[0] or '-'}/{k[1]}": v for k, v in flags.items()}

# ------------------------------------------------------------------------------------------------ SPARC + residuals
gal = C.load_sparc()
nq = sum(1 for g in gal if g["meta"] and g["meta"]["Q"] <= 2)
check("C1 load_sparc: 175 galaxies, 163 with Q <= 2", f"{len(gal)} / {nq}", len(gal) == 175 and nq == 163)


def residuals(g, a0):
    R = g["R"] * C.KPC
    gobs = (g["Vobs"] * 1e3) ** 2 / R
    vb2 = g["Vgas"] * np.abs(g["Vgas"]) + UPS_D * g["Vdisk"] ** 2 + UPS_B * g["Vbul"] ** 2
    gbar = vb2 * 1e6 / R
    ok = (g["Vobs"] > 0) & (gbar > 0) & (np.log10(np.where(gbar > 0, gbar, 1)) < LOGG_CUT)
    if ok.sum() < 3:
        return None
    r = np.log10(gobs[ok]) - np.log10(gbar[ok] * C.nu_mono(gbar[ok] / a0))
    s = np.sqrt((0.8686 * g["eV"][ok] / g["Vobs"][ok]) ** 2 + 0.01 ** 2)
    w = 1.0 / s ** 2
    return float(np.sum(w * r) / np.sum(w)), int(ok.sum())


def classify(rec, mcut=MCUT, key="logMh"):
    m = rec[key]
    if rec["flag"] != "OK" or not np.isfinite(m):
        return None
    if m < mcut:
        return "F"
    top = rec["assoc"] if key == "logMa" else rec["pgc1"]
    return "GC" if rec["pgc"] == top else "SAT"


def rsd(x):
    x = np.asarray(x)
    return 1.4826 * np.median(np.abs(x - np.median(x)))


def boot_delta(a, b, rng, n=NBOOT):
    a, b = np.asarray(a), np.asarray(b)
    ia = rng.integers(0, len(a), (n, len(a)))
    ib = rng.integers(0, len(b), (n, len(b)))
    return np.median(a[ia], axis=1) - np.median(b[ib], axis=1)


def verdict(delta, sig, dbic, nGC, nF):
    if nGC < 5 or nF < 20:
        return "NON-DISCRIMINATING (UNDERPOWERED)"
    if delta > 0.05 and delta / sig > 3 and dbic > 2:
        return "TWO-REGIME SUPPORTED"
    if delta + 2 * sig < 0.05:
        return "NOT SUPPORTED"
    return "NON-DISCRIMINATING"


LADDER = {"NOT SUPPORTED": 0, "NON-DISCRIMINATING": 1, "NON-DISCRIMINATING (UNDERPOWERED)": 1, "TWO-REGIME SUPPORTED": 2}


def bic_fits(x, y):
    x, y = np.asarray(x), np.asarray(y)
    N = len(y)
    out = {}
    for nm, X in (("const", np.ones((N, 1))), ("linear", np.column_stack([np.ones(N), x])),
                  ("step", np.column_stack([np.ones(N), (x >= MCUT).astype(float)]))):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        rss = float(np.sum((y - X @ beta) ** 2))
        out[nm] = dict(beta=beta.tolist(), rss=rss, bic=N * math.log(rss / N) + X.shape[1] * math.log(N))
    return out


meta = {g["name"]: g for g in gal}
VERD = {}
for foot in C.FOOTS:
    a0 = C.A0[foot]
    rng = np.random.default_rng(SEED)
    P("\n" + "=" * 118 + f"\nFOOTING {foot}: a0 = {a0:.4e} m/s^2 (kappa = 1/2 fitted)\n" + "=" * 118)
    rows = []
    for g in gal:
        m = g["meta"]
        if not m or m["Q"] > 2 or g["name"] not in MATCH:
            continue
        cl = classify(MATCH[g["name"]])
        if cl is None:
            continue
        res = residuals(g, a0)
        if res is None:
            continue
        rows.append(dict(name=g["name"], cl=cl, R=res[0], npt=res[1], logMh=MATCH[g["name"]]["logMh"],
                         logMd=MATCH[g["name"]]["logMd"], cat=MATCH[g["name"]]["cat"], fD=m["fD"],
                         logL=math.log10(max(m["L36"], 1e-4)), rec=MATCH[g["name"]]))
    R0 = {r["name"]: r["R"] for r in rows}                       # the honest residuals (for C3)
    if MUTATE:
        for r in rows:
            if r["cl"] == "GC":
                r["R"] += 0.1
    by = {k: [r for r in rows if r["cl"] == k] for k in ("GC", "SAT", "F")}
    nGC, nSAT, nF = (len(by[k]) for k in ("GC", "SAT", "F"))
    P(f"classified Q<=2 galaxies with >= 3 points at g_bar < 1e-10.5: GC {nGC}, SAT {nSAT}, F {nF}")
    P("  GC: " + ", ".join(f"{r['name']}({r['cat']},{r['logMh']:.2f},{r['R']:+.3f})" for r in sorted(by["GC"], key=lambda r: -r["logMh"])))
    P("  SAT: " + ", ".join(f"{r['name']}({r['cat']},{r['logMh']:.2f},{r['R']:+.3f})" for r in sorted(by["SAT"], key=lambda r: -r["logMh"])))
    gc = np.array([r["R"] for r in by["GC"]])
    fl = np.array([r["R"] for r in by["F"]])
    sa = np.array([r["R"] for r in by["SAT"]])
    out = dict(nGC=nGC, nSAT=nSAT, nF=nF, GC=[r["name"] for r in by["GC"]], SAT=[r["name"] for r in by["SAT"]])
    if nGC == 0 or nF == 0:
        P("no centrals or no field galaxies -- nothing to score")
        VERD[foot] = "NON-DISCRIMINATING (UNDERPOWERED)"
        NUM[foot] = out
        continue
    # (a)
    D = float(np.median(gc) - np.median(fl))
    bd = boot_delta(gc, fl, rng)
    sD = float(np.std(bd))
    P(f"(a) median R: GC {np.median(gc):+.4f}, F {np.median(fl):+.4f}; Delta = {D:+.4f} +- {sD:.4f} dex  (S = {D / sD:+.2f})")
    # (b)
    Qs = rsd(gc) / rsd(fl)
    ia = rng.integers(0, nGC, (NBOOT, nGC))
    ib = rng.integers(0, nF, (NBOOT, nF))
    qb = (1.4826 * np.median(np.abs(gc[ia] - np.median(gc[ia], axis=1)[:, None]), axis=1)) / \
         (1.4826 * np.median(np.abs(fl[ib] - np.median(fl[ib], axis=1)[:, None]), axis=1))
    qlo, qhi = np.percentile(qb[np.isfinite(qb)], [2.5, 97.5])
    P(f"(b) robust SD: GC {rsd(gc):.4f}, F {rsd(fl):.4f}; Q_s = {Qs:.3f}  (95%: {qlo:.3f}-{qhi:.3f})")
    # (c)
    xs = np.array([r["logMh"] for r in by["GC"] + by["F"]])
    ys = np.array([r["R"] for r in by["GC"] + by["F"]])
    fits = bic_fits(xs, ys)
    dbic = fits["linear"]["bic"] - fits["step"]["bic"]
    P(f"(c) N = {len(ys)}: BIC const {fits['const']['bic']:.2f}, linear {fits['linear']['bic']:.2f} (slope {fits['linear']['beta'][1]:+.4f}/dex), "
      f"step {fits['step']['bic']:.2f} (jump {fits['step']['beta'][1]:+.4f}); dBIC(linear - step) = {dbic:+.2f}")
    # (d)
    if nSAT:
        Ds = float(np.median(sa) - np.median(fl))
        sDs = float(np.std(boot_delta(sa, fl, rng)))
        P(f"(d) satellites (cross-check, EFE predicts < 0): Delta_sat = {Ds:+.4f} +- {sDs:.4f} (S = {Ds / sDs:+.2f}); "
          "record's directional-EFE: +2.95 once, WALLABY -1.70 (quoted, not averaged)")
    else:
        Ds = sDs = float("nan")
        P("(d) no satellites classified")
    v = verdict(D, sD, dbic, nGC, nF)
    # mass-matched control M
    lgc = np.array([r["logL"] for r in by["GC"]])
    lfl = np.array([r["logL"] for r in by["F"]])

    def matched_delta(igc, ifl):
        mm = []
        for i in igc:
            d = np.abs(lfl[ifl] - lgc[i])
            mm.extend(fl[ifl][np.argsort(d, kind="stable")[:3]])
        return float(np.median(gc[igc]) - np.median(mm))

    DM = matched_delta(np.arange(nGC), np.arange(nF))
    bm = np.array([matched_delta(rng.integers(0, nGC, nGC), rng.integers(0, nF, nF)) for _ in range(4000)])
    sM = float(np.std(bm))
    P(f"control M (3 nearest field galaxies in log L3.6 per central): Delta_M = {DM:+.4f} +- {sM:.4f} (S = {DM / sM:+.2f}); "
      f"log L3.6 medians GC {np.median(lgc):.2f}, F {np.median(lfl):.2f}")
    if v == "TWO-REGIME SUPPORTED" and (DM < 0.05 or DM / sM < 2):
        v = "NON-DISCRIMINATING"
        P("  mass-confound downgrade applied: SUPPORTED -> NON-DISCRIMINATING")
    scat = (v != "TWO-REGIME SUPPORTED") and Qs > 1.5 and qlo > 1
    P(f"VERDICT [{foot}]: {v}" + ("  + SCATTER-ONLY SIGNAL" if scat else ""))
    VERD[foot] = v
    out.update(Delta=D, sigma=sD, S=D / sD, medGC=float(np.median(gc)), medF=float(np.median(fl)), Qs=Qs, Qs95=[qlo, qhi],
               bic=fits, dBIC=dbic, Delta_sat=Ds, sigma_sat=sDs, Delta_M=DM, sigma_M=sM, verdict=v, scatter_only=scat)

    # sensitivities (reported)
    P("-- sensitivities (reported, no verdict weight)")
    sens = {}
    for lab, mc, key, filt in (("mcut 12.3", 12.3, "logMh", None), ("mcut 12.7", 12.7, "logMh", None),
                               ("KT2017 logMd", MCUT, "logMd", "KT2017"), ("KT2017 only", MCUT, "logMh", "KT2017"),
                               ("T15 only", MCUT, "logMh", "T15"), ("C4 f_D != 1", MCUT, "logMh", "fD"),
                               ("POSTHOC assoc", MCUT, "logMa", "KT2017")):
        cls = []
        for r in rows:
            if filt in ("KT2017", "T15") and r["cat"] != filt:
                continue
            if filt == "fD" and r["fD"] == 1:
                continue
            c2 = classify(r["rec"], mc, key)
            if c2 is None:
                continue
            cls.append((c2, r["R"]))
        a = np.array([x for c2, x in cls if c2 == "GC"])
        b = np.array([x for c2, x in cls if c2 == "F"])
        if len(a) and len(b):
            dd = float(np.median(a) - np.median(b))
            ss = float(np.std(boot_delta(a, b, rng, 5000)))
            P(f"   {lab:14s}: N GC {len(a):3d}, F {len(b):3d}; Delta {dd:+.4f} +- {ss:.4f} (S {dd / ss if ss > 0 else float('nan'):+.2f})")
            sens[lab] = dict(nGC=len(a), nF=len(b), Delta=dd, sigma=ss)
        else:
            P(f"   {lab:14s}: N GC {len(a)}, F {len(b)} -- not computable")
            sens[lab] = dict(nGC=len(a), nF=len(b))
    out["sensitivities"] = sens
    # C5 permutation
    allv = np.concatenate([gc, fl])
    perm = np.empty(NPERM)
    for k in range(NPERM):
        p = rng.permutation(len(allv))
        perm[k] = np.median(allv[p[:nGC]]) - np.median(allv[p[nGC:]])
    pp = float(np.mean(np.abs(perm) >= abs(D)))
    check(f"C5 [{foot}] label-permutation p for |Delta|", f"p = {pp:.4f}", True, lb=False)
    out["perm_p"] = pp
    # C3 identity
    mx = 0.0
    for r in rows:
        rr = residuals(meta[r["name"]], a0)[0]
        mx = max(mx, abs(rr - r["R"]))
    check(f"C3 [{foot}] every R_g used equals R_g recomputed from rotmod (<= 1e-9 dex)", f"max |diff| = {mx:.3e}", mx <= 1e-9)
    if MUTATE:
        D0 = float(np.median([R0[r['name']] for r in by["GC"]]) - np.median(fl))
        g0 = np.array([R0[r["name"]] for r in by["GC"]])
        xs0 = xs.copy()
        ys0 = np.concatenate([g0, fl])
        dbic0 = bic_fits(xs0, ys0)["linear"]["bic"] - bic_fits(xs0, ys0)["step"]["bic"]
        v0 = verdict(D0, sD, dbic0, nGC, nF)
        check(f"MUT [{foot}] Delta rises by 0.100 +- 0.005 and the verdict does not move down",
              f"shift {D - D0:+.4f}; {v0} -> {v}", abs((D - D0) - 0.1) <= 0.005 and LADDER[v] >= LADDER[v0], lb=False)
    NUM[foot] = out

# ------------------------------------------------------------------------------------------------ C2 Ursa Major
uma = [g["name"] for g in gal if g["meta"] and g["meta"]["fD"] == 4]
grp = [MATCH[n]["pgc1"] for n in uma if n in MATCH and MATCH[n]["cat"] == "KT2017" and MATCH[n]["flag"] == "OK"]
if grp:
    top = max(set(grp), key=grp.count)
    frac = grp.count(top) / len(grp)
else:
    top, frac = "", 0.0
check("C2 Ursa Major (f_D = 4) SPARC galaxies matched in KT2017 share one PGC1 at >= 70%",
      f"{grp.count(top) if grp else 0}/{len(grp)} = {frac:.2f} in PGC1 {top} (of {len(uma)} f_D=4 galaxies)", frac >= 0.70)
# POST-HOC diagnostic (added after C2 failed; README departure): KT2017 splits UMa into groups but keeps one association
asc = [MATCH[n]["assoc"] for n in uma if n in MATCH and MATCH[n]["cat"] == "KT2017" and MATCH[n]["flag"] == "OK"]
atop = max(set(asc), key=asc.count) if asc else ""
check("C2b POST-HOC: the same UMa galaxies share one KT2017 association PGC1+ (diagnostic of C2's failure)",
      f"{asc.count(atop) if asc else 0}/{len(asc)} in PGC1+ {atop}; {len(set(grp))} distinct groups",
      bool(asc) and asc.count(atop) / len(asc) >= 0.70, lb=False)

P("\n" + "=" * 118)
fin = min(VERD.values(), key=lambda s: LADDER[s]) if VERD else "NON-DISCRIMINATING"
P(f"FOOTING VERDICTS: {VERD}  ->  REPORTED (weaker): {fin}")
npass = sum(1 for c in CH if c[1])
nlb = sum(1 for c in CH if not c[1] and c[2])
P(f"\n  {npass}/{len(CH)} checks pass; load-bearing failures: {nlb}")
rc = 1 if nlb else 0
P(f"rc = {rc}")
with builtins.open(JSONP, "w", encoding="utf-8") as fh:
    json.dump(jc(dict(lane="CFG393", mutate=MUTATE, verdicts=VERD, reported=fin, numbers=NUM,
                      checks=[dict(name=c[0], ok=c[1], load_bearing=c[2], measured=c[3]) for c in CH])), fh, indent=1)
sys.stdout = tee.o
tee.f.close()
sys.exit(rc)
