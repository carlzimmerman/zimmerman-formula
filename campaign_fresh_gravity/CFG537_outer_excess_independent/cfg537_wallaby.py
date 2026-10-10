#!/usr/bin/env python3
"""CFG537 Part A (FROZEN_CRITERIA.md, criteria commit 4d77eb8da): replication of CFG534's SPARC early-type outer excess in WALLABY DR2.
WALLABY DR2 kinematic curves x 2MASS XSC (CFG445 baryon model) x RC3 T; SPARC overlaps removed; CFG534's statistic copied.
STAGE=forecast  power forecast only (labels, masses, band coverage; NO WALLABY residual).
default         forecast + scoring + sensitivities.   CFG537_MUTATE=1 -> MU1 / MU2, outputs *_MUTATE.*
Run: nice -n 10 python3 cfg537_wallaby.py > cfg537_wallaby.out ; CFG537_MUTATE=1 nice -n 10 python3 cfg537_wallaby.py > cfg537_wallaby_MUTATE.out
"""
import os, sys, re, csv, json, math
import numpy as np
from scipy.stats import norm

os.environ.setdefault("OMP_NUM_THREADS", "2")
try:
    os.nice(10)
except OSError:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
W445 = os.path.join(LANES, "CFG445_group_centrals_x3", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
sys.path.insert(0, os.path.join(LANES, "CFG445_group_centrals_x3"))
from cfg445_common import ring_sum_g, freeman_g  # noqa: E402  (read-only reuse of CFG445's force routines)

MUT = os.environ.get("CFG537_MUTATE", "0") == "1"
STAGE = os.environ.get("STAGE", "all")
SUF = "_MUTATE" if MUT else ""
LOG, CHK = [], {}
RES = {"lane": "CFG537", "part": "A (WALLABY replication)", "mutate": MUT, "stage": STAGE, "criteria_commit": "4d77eb8da",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu(y)=1/(1-exp(-sqrt y)); cold energy mass still required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
CONV = 3.0857e19 / 1e6          # m/s^2 -> (km/s)^2/kpc divisor as in CFG534
G2SI = 1e6 / 3.0857e19          # (km/s)^2/kpc -> m/s^2
REF = 0.071                     # CFG534 SPARC canonical Delta_out (frozen reference amplitude)
SIGCUT = 0.0355
EDG0 = np.arange(7.0, 12.2 + 1e-9, 0.4)
EDG = EDG0.copy()


def nu(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def wmean(r, w, m):
    m = m & np.isfinite(r)
    return float((r[m] * w[m]).sum() / w[m].sum()) if m.sum() >= 2 else np.nan


def matched(rows, key, early, edg=None):
    """CFG534's matched(): inverse-variance combination over log M_b bins of mean(early) - mean(late)."""
    edg = EDG if edg is None else edg
    x = np.array([r[key] for r in rows]); lm = np.array([r["lMb"] for r in rows])
    num = den = 0.0; nb = ne = nl = 0; per = []
    for lo, hi in zip(edg[:-1], edg[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        a, b = x[m & early], x[m & ~early]
        if len(a) >= 2 and len(b) >= 2:
            v = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)
            num += (a.mean() - b.mean()) / v; den += 1 / v; nb += 1; ne += len(a); nl += len(b)
            per.append(dict(bin=[round(lo, 2), round(hi, 2)], n_early=len(a), n_late=len(b), diff=float(a.mean() - b.mean()), sig=float(v ** 0.5)))
    if den == 0:
        return dict(diff=np.nan, sig=np.nan, Z=np.nan, nbins=0, n_early=0, n_late=0, per_bin=[])
    return dict(diff=num / den, sig=den ** -0.5, Z=num / den ** 0.5, nbins=nb, n_early=ne, n_late=nl, per_bin=per)


# ================================================================== SPARC (CFG534 rows, copied) for control A-C1 and the forecast
keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
TAB = {}
for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
    tok = line.split()
    if len(tok) != 19:
        continue
    try:
        TAB[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
    except ValueError:
        continue
SAMP = []
for f in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not f.endswith("_rotmod.dat"):
        continue
    d = np.genfromtxt(os.path.join(DATA, "sparc_data", f), comments="#")
    nm = f.replace("_rotmod.dat", "")
    if d.ndim != 2 or d.shape[1] < 6 or nm not in TAB:
        continue
    g = dict(name=nm, R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], m=TAB[nm])
    if int(g["m"]["Q"]) <= 2 and g["m"]["Inc"] >= 30:
        SAMP.append(g)


def sparc_rows(a0):
    rows = []
    for g in SAMP:
        Vb2 = g["Vg"] * np.abs(g["Vg"]) + 0.5 * g["Vd"] ** 2 + 0.7 * g["Vb"] ** 2
        gb = Vb2 / g["R"]; gobs = g["V"] ** 2 / g["R"]; ok = (gb > 0) & (gobs > 0)
        r = np.full(len(g["R"]), np.nan); r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
        w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
        Rd = g["m"]["Rdisk"]; Ms, Mg = 0.5 * g["m"]["L36"], 1.33 * g["m"]["MHI"]
        di, do = wmean(r, w, ok & (g["R"] <= 1.5 * Rd)), wmean(r, w, ok & (g["R"] >= 3 * Rd))
        rows.append(dict(name=g["name"], T=int(g["m"]["T"]), lMb=math.log10((Ms + Mg) * 1e9), d_in=di, d_out=do,
                         d_oi=do - di if np.isfinite(do) and np.isfinite(di) else np.nan))
    return rows


SPR = {f: sparc_rows(A0SI[f] * CONV) for f in FOOTS}
c1 = {}
for f in FOOTS:
    T = np.array([r["T"] for r in SPR[f]])
    c1[f] = dict(d_out=matched(SPR[f], "d_out", T <= 3), d_oi=matched(SPR[f], "d_oi", T <= 3))
check("A-C1 copied SPARC code reproduces CFG534 Delta_out (+0.0712/+0.0718 within 0.001)",
      abs(c1["canonical"]["d_out"]["diff"] - 0.0712) <= 0.001 and abs(c1["alt"]["d_out"]["diff"] - 0.0718) <= 0.001,
      f"{c1['canonical']['d_out']['diff']:+.4f} (Z {c1['canonical']['d_out']['Z']:+.2f}) / {c1['alt']['d_out']['diff']:+.4f} (Z {c1['alt']['d_out']['Z']:+.2f}); "
      f"d_oi {c1['canonical']['d_oi']['diff']:+.4f} / {c1['alt']['d_oi']['diff']:+.4f}")
RES["sparc_reference"] = {f: {k: {kk: vv for kk, vv in v.items() if kk != "per_bin"} for k, v in c1[f].items()} for f in FOOTS}

# ================================================================== WALLABY sample
def _lst(s):
    return np.array([fnum(x) for x in s.split(",")]) if s else np.array([])


def _tr(s):
    m = re.search(r"TR(\d+)", s or "")
    return int(m.group(1)) if m else 0


best = {}
for r in csv.DictReader(open(os.path.join(W445, "wallaby_dr2_kinematic_catalogue.csv"))):
    n = r["name"]
    if n not in best or _tr(r["team_release_kin"]) > _tr(best[n]["team_release_kin"]):
        best[n] = r
src = {}
for r in csv.DictReader(open(os.path.join(W445, "wallaby_dr2_source_catalogue.csv"))):
    src.setdefault(r["name"], []).append(r)
xsc = {}
for line in open(os.path.join(W445, "xsc_wallaby_cones.tsv"), encoding="utf-8"):
    if line.startswith("#") or line.startswith("wallaby_name"):
        continue
    f_ = line.rstrip("\n").split("\t")
    rr = fnum(f_[1])
    if rr <= 20.0 and (f_[0] not in xsc or rr < xsc[f_[0]]["r"]):
        xsc[f_[0]] = dict(r=rr, K=fnum(f_[5]), reff=fnum(f_[7]))
wise = {}
for r in csv.DictReader(open(os.path.join(EXT, "wallaby_dr2", "allwise_wallaby_dr2.csv"))):
    w1 = fnum(r.get("w1gmag"))
    if not np.isfinite(w1):
        w1 = fnum(r.get("w1mpro"))
    wise[r["wallaby_name"]] = w1
RC3 = []
for line in open(os.path.join(DATA, "rc3_devaucouleurs1991_colors.tsv")):
    p = line.rstrip("\n").split("\t")
    if len(p) < 6:
        continue
    a, d = fnum(p[0]), fnum(p[1])
    if np.isfinite(a) and np.isfinite(d):
        RC3.append((a, d, fnum(p[5]), p[2].strip(), p[3].strip()))
RCa = np.array([x[0] for x in RC3]); RCd = np.array([x[1] for x in RC3])


def unit(a, d):
    a, d = np.radians(a), np.radians(d)
    return np.stack([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)], axis=-1)


U3 = unit(RCa, RCd)
spos = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
SPU = np.array([unit(v["ra"], v["dec"]) for v in spos.values() if v.get("ra") is not None and v.get("dec") is not None])


def normname(s):
    s = re.sub(r"\s+", "", s).upper()
    return re.sub(r"(?<=[A-Z])0+(?=\d)", "", s)


SPN = {normname(n) for n in TAB}


def sep_arcsec(u, U):
    return np.degrees(np.arccos(np.clip(U @ u, -1, 1))) * 3600


def build(match_rad=30.0, use_wise=False, einc=False):
    out, cnt = [], dict(unique=len(best), q=0, inc=0, xsc=0, rc3=0, ambiguous=0, dist=0, sparc_overlap=0, overlap_names=[], seps=[])
    for n in sorted(best):
        r = best[n]
        if not fnum(r["QFlag_model"]) <= 1:
            continue
        cnt["q"] += 1
        if not fnum(r["Inc_model"]) >= 30:
            continue
        cnt["inc"] += 1
        x = xsc.get(n)
        if x is None or not (np.isfinite(x["K"]) and np.isfinite(x["reff"])):
            continue
        cnt["xsc"] += 1
        u = unit(fnum(r["RA_model"]), fnum(r["DEC_model"]))
        s = sep_arcsec(u, U3); o = np.argsort(s)[:3]
        if s[o[0]] > match_rad or not np.isfinite(RC3[o[0]][2]):
            continue
        if s[o[1]] <= match_rad and RC3[o[1]][2] != RC3[o[0]][2]:
            cnt["ambiguous"] += 1
            continue
        cnt["rc3"] += 1
        T = RC3[o[0]][2]
        same = [z for z in src.get(n, []) if z["team_release"] == r["team_release"]] or src.get(n, [])
        D = fnum(same[0]["dist_h"]) if same else np.nan
        lHI = fnum(same[0]["log_m_hi"]) if same else np.nan
        if not (np.isfinite(D) and D > 0 and np.isfinite(lHI)):
            continue
        cnt["dist"] += 1
        names = {normname(RC3[o[0]][3]), normname(RC3[o[0]][4])} - {""}
        if (len(SPU) and sep_arcsec(u, SPU).min() <= 60.0) or (names & SPN):
            cnt["sparc_overlap"] += 1; cnt["overlap_names"].append(n + " / " + "/".join(sorted(names)))
            continue
        cnt["seps"].append(float(s[o[0]]))
        akpc = D * 1e3 * math.pi / (180 * 3600)
        R = _lst(r["Rad"]) * akpc; V = _lst(r["Vrot_model"]); eV = _lst(r["e_Vrot_model"])
        if einc:
            eV = np.sqrt(eV ** 2 + _lst(r["e_Vrot_model_inc"]) ** 2)
        Rs = _lst(r["Rad_SD"]) * akpc; sd = _lst(r["SD_FO_model"])
        if use_wise:
            w1 = wise.get(n, np.nan)
            if not np.isfinite(w1):
                continue
            L = 10 ** (-0.4 * (w1 - 5 * math.log10(D) - 25 - 3.24)); ups = 0.5
        else:
            L = 10 ** (-0.4 * (x["K"] - 5 * math.log10(D) - 25 - 3.28)); ups = 0.6
        Rd = x["reff"] * akpc / 1.678
        Ms, Mg = ups * L, 1.33 * 10 ** lHI
        out.append(dict(name=n, T=T, D=D, R=R, V=V, eV=eV, Rs=Rs, sd=sd, Rd=Rd, Ms=Ms, Mg=Mg, lMb=math.log10(Ms + Mg),
                        lHI=lHI, nin=int((R <= 1.5 * Rd).sum()), nout=int((R >= 3 * Rd).sum())))
    return out, cnt


def residual_rows(gals, a0si, inject=0.0, early_cut=3):
    rows = []
    for g in gals:
        gg = ring_sum_g(g["Rs"], 1.33 * g["sd"], g["R"]) if len(g["Rs"]) >= 2 else np.zeros_like(g["R"])
        gs = freeman_g(g["Ms"], g["Rd"], g["R"])
        gb = (gg + gs) * G2SI
        gobs = (g["V"] * 1e3) ** 2 / (g["R"] * 3.0857e19)
        ok = (gb > 0) & (gobs > 0) & np.isfinite(gb) & np.isfinite(gobs)
        r = np.full(len(g["R"]), np.nan)
        r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0si) * gb[ok]))
        w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
        if inject and g["T"] <= early_cut:
            r = r + inject * (g["R"] >= 3 * g["Rd"])
        di, do = wmean(r, w, ok & (g["R"] <= 1.5 * g["Rd"])), wmean(r, w, ok & (g["R"] >= 3 * g["Rd"]))
        rows.append(dict(name=g["name"], T=g["T"], lMb=g["lMb"], d_in=di, d_out=do, fgas=g["Mg"] / (g["Ms"] + g["Mg"]),
                         d_oi=do - di if np.isfinite(do) and np.isfinite(di) else np.nan))
    return rows


GALS, CNT = build()
P(f"WALLABY: unique {CNT['unique']}; QFlag<=1 {CNT['q']}; inc>=30 {CNT['inc']}; XSC {CNT['xsc']}; RC3 T within 30\" {CNT['rc3']} "
  f"(ambiguous dropped {CNT['ambiguous']}); distance+HI {CNT['dist']}; SPARC overlaps removed {CNT['sparc_overlap']} {CNT['overlap_names']}; FINAL {len(GALS)}")
sp = np.array(CNT["seps"])
check("A-C3 RC3 match separations reported", len(sp) > 0, f"median {np.median(sp):.1f}\", max {sp.max():.1f}\", ambiguous dropped {CNT['ambiguous']}")
P(f"A-C4 SPARC overlaps removed: {CNT['sparc_overlap']}")
# A-C2 HI mass check
dif = []
for g in GALS:
    if len(g["Rs"]) >= 2:
        Rpc = g["Rs"] * 1e3; dR = np.median(np.diff(Rpc))
        dif.append(math.log10(np.sum(g["sd"] * 2 * np.pi * Rpc * dR)) - g["lHI"])
check("A-C2 WALLABY 2 pi int SD_FO R dR vs catalogue log M_HI, median |diff| <= 0.15 dex", np.median(np.abs(dif)) <= 0.15,
      f"median |diff| {np.median(np.abs(dif)):.3f} (median signed {np.median(dif):+.3f}, N {len(dif)})")
T_ = np.array([g["T"] for g in GALS]); E_ = T_ <= 3
P(f"labels: early (T<=3) {E_.sum()}, late {(~E_).sum()}; log M_b range {min(g['lMb'] for g in GALS):.2f}-{max(g['lMb'] for g in GALS):.2f}")
RES["sample"] = dict(counts={k: v for k, v in CNT.items() if k != "seps"}, N=len(GALS), n_early=int(E_.sum()), n_late=int((~E_).sum()),
                     rc3_sep_median=float(np.median(sp)), rc3_sep_max=float(sp.max()), hi_check_median_absdiff=float(np.median(np.abs(dif))),
                     n_inner_ge2=int(sum(g["nin"] >= 2 for g in GALS)), n_outer_ge2=int(sum(g["nout"] >= 2 for g in GALS)))

# ================================================================== power forecast (no WALLABY residual)
P("\n== POWER FORECAST (SPARC within-bin within-class scatter of d_out x WALLABY counts; no WALLABY residual) ==")
FC = {}
for f in FOOTS:
    rows = SPR[f]; x = np.array([r["d_out"] for r in rows]); lm = np.array([r["lMb"] for r in rows]); Ts = np.array([r["T"] for r in rows])
    pooled = []
    binvar = {}
    for lo, hi in zip(EDG0[:-1], EDG0[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        vs = [x[m & c].var(ddof=1) for c in (Ts <= 3, Ts > 3) if (m & c).sum() >= 2]
        ns = [(m & c).sum() - 1 for c in (Ts <= 3, Ts > 3) if (m & c).sum() >= 2]
        if vs:
            binvar[round(lo, 2)] = float(np.average(vs, weights=ns)); pooled += [(v, n) for v, n in zip(vs, ns)]
    pv = float(np.average([v for v, n in pooled], weights=[n for v, n in pooled]))
    lmw = np.array([g["lMb"] for g in GALS]); ok = np.array([g["nout"] >= 2 for g in GALS])
    out = {}
    for infl in (1.0, 1.5):
        den = 0.0; nb = 0; ne = nl = 0
        for lo, hi in zip(EDG0[:-1], EDG0[1:]):
            m = (lmw >= lo) & (lmw < hi) & ok
            a, b = int((m & E_).sum()), int((m & ~E_).sum())
            if a >= 2 and b >= 2:
                s2 = binvar.get(round(lo, 2), pv) * infl ** 2
                den += 1 / (s2 / a + s2 / b); nb += 1; ne += a; nl += b
        sig = den ** -0.5 if den else np.nan
        out[f"x{infl}"] = dict(sigma_fc=sig, expected_Z=REF / sig, power=float(norm.cdf(REF / sig - 2)), nbins=nb, n_early=ne, n_late=nl)
        P(f"  [{f}] scatter x{infl}: sigma_fc {sig:.4f}; expected Z at +{REF} = {REF / sig:.2f}; P(Z>=2) {norm.cdf(REF / sig - 2):.2f}; bins {nb}, early {ne}, late {nl}")
    out["sparc_pooled_within_bin_sd"] = pv ** 0.5
    out["underpowered_declared"] = bool(out["x1.0"]["sigma_fc"] > SIGCUT)
    FC[f] = out
P(f"  pre-declared UNDERPOWERED (sigma_fc x1.0 > {SIGCUT}): {[FC[f]['underpowered_declared'] for f in FOOTS]}")
RES["forecast"] = FC
if STAGE == "forecast":
    json.dump(RES, open(os.path.join(HERE, f"cfg537_wallaby_forecast{SUF}.json"), "w"), indent=1, default=float)
    sys.exit(0)


# ================================================================== scoring
def score(rows, early):
    return {k: matched(rows, k, early) for k in ("d_out", "d_in", "d_oi")}


def verdict(sc):
    o, oi = sc["d_out"], sc["d_oi"]
    if not (o["nbins"] >= 2 and o["n_early"] >= 8):
        return "NO INDEPENDENT SAMPLE"
    d, s, Z = o["diff"], o["sig"], o["Z"]
    testable = oi["nbins"] >= 1
    if d > 0 and Z >= 2 and testable and oi["diff"] > 0:
        return "REPLICATED"
    if (d <= 0 and s <= SIGCUT) or (d + 2 * s < REF):
        return "NOT REPLICATED"
    if d > 0:
        if Z >= 2 and not testable:
            return "CONSISTENT, outer only"
        if Z >= 2 and oi["diff"] <= 0:
            return "CONSISTENT, radial pattern not reproduced"
        return "CONSISTENT"
    return "NOT DIAGNOSTIC"


if not MUT:
    P("\n== SCORING (frozen) ==")
    SC, V, ROWS = {}, {}, {}
    for f in FOOTS:
        rows = residual_rows(GALS, A0SI[f]); ROWS[f] = rows
        sc = score(rows, E_); SC[f] = sc; V[f] = verdict(sc)
        for k in ("d_out", "d_in", "d_oi"):
            o = sc[k]
            P(f"  [{f}] {k:6s}: {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']})")
            for pb in o["per_bin"]:
                P(f"        bin {pb['bin']}: early {pb['n_early']} late {pb['n_late']}  {pb['diff']:+.4f} +- {pb['sig']:.4f}")
        P(f"  [{f}] VERDICT: {V[f]}")
    head = V["canonical"] if V["canonical"] == V["alt"] else f"FOOTING-DEPENDENT (canonical {V['canonical']} / alt {V['alt']})"
    P(f"\nHEADLINE (Part A): {head}")
    RES["score"] = SC; RES["verdict"] = V; RES["headline"] = head
    RES["per_galaxy"] = {f: [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items()} for r in ROWS[f]] for f in FOOTS}

    # verify-the-result block: leave-one-galaxy-out, class means
    P("\n== verification (no verdict weight) ==")
    LOO = {}
    for f in FOOTS:
        rows = ROWS[f]; zs = []
        for i in range(len(rows)):
            rr = rows[:i] + rows[i + 1:]; ee = np.array([r["T"] <= 3 for r in rr])
            o = matched(rr, "d_out", ee)
            zs.append((o["Z"], o["diff"], rows[i]["name"]))
        zs = [z for z in zs if np.isfinite(z[0])]
        lo_, hi_ = min(zs), max(zs)
        LOO[f] = dict(Z_min=lo_[0], Z_min_drop=lo_[2], Z_max=hi_[0], Z_max_drop=hi_[2], diff_min=min(z[1] for z in zs), diff_max=max(z[1] for z in zs))
        P(f"  [{f}] leave-one-out Delta_out Z {lo_[0]:+.2f} (drop {lo_[2]}) .. {hi_[0]:+.2f} (drop {hi_[2]}); diff {LOO[f]['diff_min']:+.4f} .. {LOO[f]['diff_max']:+.4f}")
        dout = np.array([r["d_out"] for r in rows]); fin = np.isfinite(dout)
        P(f"  [{f}] unmatched mean d_out: early {np.nanmean(dout[E_ & fin]):+.4f} (N {(E_ & fin).sum()}), late {np.nanmean(dout[~E_ & fin]):+.4f} (N {(~E_ & fin).sum()})")
    RES["leave_one_out"] = LOO

    P("\n== SENSITIVITIES (no verdict weight) ==")
    SENS = {}
    variants = {"S1 W1 luminosity": dict(use_wise=True), "S2 RC3 radius 15\"": dict(match_rad=15.0), "S3 eV incl. inclination": dict(einc=True)}
    for nm, kw in variants.items():
        gals, _ = build(**kw); ee = np.array([g["T"] <= 3 for g in gals])
        for f in FOOTS:
            o = matched(residual_rows(gals, A0SI[f]), "d_out", ee)
            SENS[f"{f}|{nm}"] = dict(diff=o["diff"], sig=o["sig"], Z=o["Z"], nbins=o["nbins"], n_early=o["n_early"], n_late=o["n_late"], N=len(gals))
            P(f"  [{f}] {nm:24s}: N {len(gals)}; Delta_out {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']})")
    for f in FOOTS:
        for cut in (2, 4):
            ee = T_ <= cut; o = matched(ROWS[f], "d_out", ee)
            SENS[f"{f}|S4 T<={cut}"] = dict(diff=o["diff"], sig=o["sig"], Z=o["Z"], nbins=o["nbins"], n_early=o["n_early"], n_late=o["n_late"])
            P(f"  [{f}] S4 T<={cut:<20d}: Delta_out {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']})")
        o = matched(ROWS[f], "d_out", E_, edg=EDG0 + 0.2)
        SENS[f"{f}|S5 bins +0.2"] = dict(diff=o["diff"], sig=o["sig"], Z=o["Z"], nbins=o["nbins"], n_early=o["n_early"], n_late=o["n_late"])
        P(f"  [{f}] S5 bins +0.2 dex        : Delta_out {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']})")
    RES["sensitivities"] = SENS
else:
    P("\n== MUTATE ==")
    MU = {}
    for f in FOOTS:
        rows = residual_rows(GALS, A0SI[f]); lm = np.array([r["lMb"] for r in rows])
        base = matched(rows, "d_out", E_)
        rng = np.random.default_rng(537); zs = []
        for _ in range(200):
            Tsh = T_.copy()
            for lo, hi in zip(EDG0[:-1], EDG0[1:]):
                idx = np.where((lm >= lo) & (lm < hi))[0]
                Tsh[idx] = rng.permutation(Tsh[idx])
            zs.append(matched(rows, "d_out", Tsh <= 3)["Z"])
        zs = np.array(zs); zs = zs[np.isfinite(zs)]
        MU[f"MU1_{f}"] = dict(mean_Z=float(zs.mean()), sd_Z=float(zs.std()), n=len(zs), frac_Z_ge_2=float((zs >= 2).mean()))
        check(f"MU1 [{f}] T shuffled within bins kills Delta_out: |mean Z| < 0.5", abs(zs.mean()) < 0.5,
              f"mean Z {zs.mean():+.3f} (sd {zs.std():.2f}; P(Z>=2) {(zs >= 2).mean():.3f}); unshuffled Z {base['Z']:+.2f}")
        inj = matched(residual_rows(GALS, A0SI[f], inject=REF), "d_out", E_)
        sh = inj["diff"] - base["diff"]
        MU[f"MU2_{f}"] = dict(shift=sh, base=base["diff"], injected=inj["diff"])
        check(f"MU2 [{f}] +{REF} injection into early outer residuals recovered within 0.002", abs(sh - REF) <= 0.002, f"shift {sh:+.4f}")
    RES["mutate"] = MU

RES["checks"] = CHK
npass = sum(c["ok"] for c in CHK.values())
P(f"\n{npass}/{len(CHK)} checks pass")
json.dump(RES, open(os.path.join(HERE, f"cfg537_wallaby_results{SUF}.json"), "w"), indent=1, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
