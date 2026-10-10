#!/usr/bin/env python3
"""CFG538 (FROZEN_CRITERIA.md, criteria commit e6eb98396): does GHASP (Epinat+08 Halpha curves, Korsaga+19 Rc photometry) replicate
CFG534's SPARC early-type outer excess?  CFG534's statistic copied; shuffle-calibrated Z primary; SPARC overlaps removed.
STAGE=forecast  power forecasts only (labels, masses, band coverage; NO GHASP residual).
default         forecast + scoring + descriptive D1-D3 + overlap variants + free M/L + sensitivities.
CFG538_MUTATE=1 MU1 / MU2, outputs *_MUTATE.*
Data (read-only, owner-downloaded public CDS tables): ../_external_data/cfg538_work/ghasp/ (see FETCH_LOG.md).
Run: nice -n 10 python3 cfg538_ghasp.py > cfg538_ghasp.out ; CFG538_MUTATE=1 nice -n 10 python3 cfg538_ghasp.py > cfg538_ghasp_MUTATE.out
"""
import os, sys, re, json, math, collections
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
np.seterr(divide="ignore", invalid="ignore")   # B3's early-late dlog f has zero variance by construction (nan); keeps home paths out of .out
from scipy.stats import norm
from scipy.special import gamma as Gfun
from scipy.optimize import brentq, minimize_scalar

try:
    os.nice(10)
except OSError:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
GH = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg538_work", "ghasp"))
sys.path.insert(0, os.path.join(LANES, "CFG445_group_centrals_x3"))
from cfg445_common import freeman_g, GKPC  # noqa: E402  (read-only reuse of CFG445's exponential-disc force)

MUT = os.environ.get("CFG538_MUTATE", "0") == "1"
STAGE = os.environ.get("STAGE", "all")
EXT = os.environ.get("CFG538_SET", "390") == "combined"      # ADDENDUM b8f6c1be5: combined 388/500 + 390/466 extension
SUF = ("_ext" if EXT else "") + ("_MUTATE" if MUT else "")
LOG, CHK = [], {}
RES = {"lane": "CFG538", "mutate": MUT, "stage": STAGE, "criteria_commit": "e6eb98396", "addendum_commit": "b8f6c1be5",
       "set": "combined 388/500 + 390/466 (extension, declared post-freeze, pre-residual)" if EXT else "390/466 only (PRIMARY, frozen)",
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
CONV = 3.0857e19 / 1e6
REF = 0.071
EDG0 = np.arange(7.0, 12.2 + 1e-9, 0.4)
MSUN_RC = 4.42
NSH = 4000


def nu(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def wmean(r, w, m):
    m = m & np.isfinite(r)
    return float((r[m] * w[m]).sum() / w[m].sum()) if m.sum() >= 2 else np.nan


def normname(s):
    s = re.sub(r"\s+", "", s).upper()
    return re.sub(r"(?<=[A-Z])0+(?=\d)", "", s)


def bins_of(x, lm, early, edg=EDG0):
    out = []
    for lo, hi in zip(edg[:-1], edg[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        a, b = x[m & early], x[m & ~early]
        if len(a) >= 2 and len(b) >= 2:
            out.append((round(lo, 2), a, b))
    return out


def stat(x, lm, early, pooled=False, edg=EDG0):
    num = den = 0.0; per = []; ne = nl = 0
    for lo, a, b in bins_of(x, lm, early, edg):
        if pooled:
            s2 = (a.var(ddof=1) * (len(a) - 1) + b.var(ddof=1) * (len(b) - 1)) / (len(a) + len(b) - 2)
            v = s2 / len(a) + s2 / len(b)
        else:
            v = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)
        num += (a.mean() - b.mean()) / v; den += 1 / v; ne += len(a); nl += len(b)
        per.append(dict(bin=lo, n_early=len(a), n_late=len(b), diff=float(a.mean() - b.mean()), sig=float(v ** 0.5)))
    if den == 0:
        return dict(diff=np.nan, sig=np.nan, Z=np.nan, nbins=0, n_early=0, n_late=0, per_bin=[])
    return dict(diff=num / den, sig=den ** -0.5, Z=num / den ** 0.5, nbins=len(per), n_early=ne, n_late=nl, per_bin=per)


def shuffles(lm, T, rng, n, edg=EDG0):
    for _ in range(n):
        Ts = T.copy()
        for lo, hi in zip(edg[:-1], edg[1:]):
            idx = np.where((lm >= lo) & (lm < hi))[0]
            Ts[idx] = rng.permutation(Ts[idx])
        yield Ts


def calibrated(x, lm, T, cut=3, nsh=NSH, seed=538, edg=EDG0):
    x, lm, T = np.asarray(x, float), np.asarray(lm, float), np.asarray(T, float)
    o = stat(x, lm, T <= cut, edg=edg)
    o["adequate"] = bool(o["nbins"] >= 2 and o["n_early"] >= 8)
    if o["nbins"] == 0:
        o.update(Z_cal=np.nan, sig_cal=np.nan, p_shuffle=np.nan, null_mean=np.nan, null_sd=np.nan, Z_pooled=np.nan)
        return o
    rng = np.random.default_rng(seed)
    zs = np.array([stat(x, lm, Ts <= cut, edg=edg)["Z"] for Ts in shuffles(lm, T, rng, nsh, edg)])
    zs = zs[np.isfinite(zs)]
    Z = o["Z"]
    p = float((zs >= Z).mean()) if Z >= 0 else float((zs <= Z).mean())
    sgn = 1 if Z >= 0 else -1
    if p <= 0:
        zc = sgn * float(norm.isf(1.0 / (len(zs) + 1))); bound = True
    else:
        zc = sgn * float(norm.isf(min(p, 0.5))) if p < 0.5 else 0.0; bound = False
    sd = float(zs.std()) if len(zs) > 1 else np.nan
    pz = stat(x, lm, T <= cut, pooled=True, edg=edg)
    o.update(Z_cal=zc, Z_cal_is_bound=bound, p_shuffle=p, null_mean=float(zs.mean()), null_sd=sd, n_shuffles=len(zs),
             sig_cal=o["sig"] * sd if np.isfinite(sd) and sd > 1 else o["sig"], Z_pooled=pz["Z"])
    return o


def ladder(o, oi, ref=REF):
    if not o.get("adequate"):
        return "NO INDEPENDENT SAMPLE"
    d, zc, sc = o["diff"], o["Z_cal"], o["sig_cal"]
    testable = oi["nbins"] >= 1
    if d > 0 and zc >= 2 and testable and oi["diff"] > 0:
        return "REPLICATED"
    if (d < 0 and zc <= -2) or (d + 2 * sc < ref):
        return "NOT REPLICATED"
    if d > 0:
        if zc >= 2 and not testable:
            return "CONSISTENT, outer only"
        if zc >= 2 and oi["diff"] <= 0:
            return "CONSISTENT, radial pattern not reproduced"
        return "CONSISTENT"
    return "NOT DIAGNOSTIC (consistent with +%.3f)" % ref


def fmt(o):
    if o["nbins"] == 0:
        return "untestable (0 matched bins)"
    zc = o.get("Z_cal", np.nan)
    return (f"{o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; Z_cal {zc:+.2f}{' bound' if o.get('Z_cal_is_bound') else ''}, "
            f"null sd {o.get('null_sd', np.nan):.2f}; pooled Z {o.get('Z_pooled', np.nan):+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']}"
            f"{'' if o.get('adequate') else '; INADEQUATE'})")


# ================================================================== row counts + parsing (ReadMe byte layout)
def lines(fn):
    return [l.rstrip("\n") for l in open(os.path.join(GH, fn)) if l.strip()]


L_f = lines("J_MNRAS_390_466_tablef.dat"); L_b3 = lines("J_MNRAS_390_466_tableb3.dat"); L_c3 = lines("J_MNRAS_388_500_tablec3.dat")
L_t1 = lines("J_MNRAS_453_2965_table1.dat"); L_t4 = lines("J_MNRAS_453_2965_table4.dat")
L_a1 = lines("J_MNRAS_482_154_tablea1.dat"); L_a2 = lines("J_MNRAS_482_154_tablea2.dat")
cnts = dict(tablef=len(L_f), tableb3=len(L_b3), tablec3=len(L_c3), table1=len(L_t1), table4=len(L_t4), tablea1=len(L_a1), tablea2=len(L_a2))
exp_c = dict(tablef=4208, tableb3=203, tablec3=108, table1=170, table4=232, tablea1=124, tablea2=100)
RC = collections.defaultdict(list)
for l in L_f:
    RC[normname(l[0:8])].append((fnum(l[9:14]), fnum(l[31:34]), fnum(l[35:38]), l[42:43]))
check("C5 row counts match the ReadMes", cnts == exp_c and len(RC) == 82, f"{cnts}; RC galaxies {len(RC)}")
B3 = {}
for l in L_b3:
    B3[normname(l[0:9])] = dict(T=fnum(l[10:14]), D=fnum(l[31:36]), inc=fnum(l[55:57]), Vmax=fnum(l[79:83]))
A1 = {}
for l in L_a1:
    A1[normname(l[0:9])] = dict(type=l[12:24].strip(), BV=fnum(l[30:34]), R25h=fnum(l[40:43]), Rlh=fnum(l[44:48]), mu0=fnum(l[49:53]),
                                h=fnum(l[54:57]), LD=fnum(l[58:64]), mue=fnum(l[65:70]), re=fnum(l[71:75]), n=fnum(l[76:80]),
                                LB=fnum(l[81:87]), f=int(l[88]))
A2 = {normname(l[0:9]): fnum(l[80:84]) for l in L_a2}
T1 = {}
for l in L_t1:
    ra = 15 * (fnum(l[11:13]) + fnum(l[14:16]) / 60 + fnum(l[17:21]) / 3600)
    de = (fnum(l[23:25]) + fnum(l[26:28]) / 60 + fnum(l[29:31]) / 3600) * (-1 if l[22] == "-" else 1)
    T1[normname(l[0:10])] = dict(ra=ra, dec=de, seeing=fnum(l[72:75]))

# ================================================================== SPARC (CFG534 code, copied)
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


def sparc_rows(a0, bo=3.0):
    rows = []
    for g in SAMP:
        Vb2 = g["Vg"] * np.abs(g["Vg"]) + 0.5 * g["Vd"] ** 2 + 0.7 * g["Vb"] ** 2
        gb = Vb2 / g["R"]; gobs = g["V"] ** 2 / g["R"]; ok = (gb > 0) & (gobs > 0)
        r = np.full(len(g["R"]), np.nan); r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
        w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
        Rd = g["m"]["Rdisk"]; Ms, Mg = 0.5 * g["m"]["L36"], 1.33 * g["m"]["MHI"]
        di, do = wmean(r, w, ok & (g["R"] <= 1.5 * Rd)), wmean(r, w, ok & (g["R"] >= bo * Rd))
        rows.append(dict(name=g["name"], T=int(g["m"]["T"]), lMb=math.log10((Ms + Mg) * 1e9), d_in=di, d_out=do,
                         d_oi=do - di if np.isfinite(do) and np.isfinite(di) else np.nan))
    return rows


SPR = {f: sparc_rows(A0SI[f] * CONV) for f in FOOTS}
SPR2 = {f: sparc_rows(A0SI[f] * CONV, bo=2.0) for f in FOOTS}
c1 = {}
for f in FOOTS:
    T = np.array([r["T"] for r in SPR[f]])
    c1[f] = stat(np.array([r["d_out"] for r in SPR[f]]), np.array([r["lMb"] for r in SPR[f]]), T <= 3)
check("C1 copied SPARC code reproduces CFG534 Delta_out (+0.0712 / +0.0722 within 0.001)",
      abs(c1["canonical"]["diff"] - 0.0712) <= 0.001 and abs(c1["alt"]["diff"] - 0.0722) <= 0.001,
      f"{c1['canonical']['diff']:+.5f} / {c1['alt']['diff']:+.5f}")
SREF2 = {}
for f in FOOTS:
    rr = SPR2[f]; T = np.array([r["T"] for r in rr])
    SREF2[f] = stat(np.array([r["d_out"] for r in rr]), np.array([r["lMb"] for r in rr]), T <= 3)
P(f"SPARC D2 reference (R >= 2 R_d, CFG534 code): canonical {SREF2['canonical']['diff']:+.4f} +- {SREF2['canonical']['sig']:.4f} "
  f"(Z {SREF2['canonical']['Z']:+.2f}) / alt {SREF2['alt']['diff']:+.4f} +- {SREF2['alt']['sig']:.4f} (Z {SREF2['alt']['Z']:+.2f})")
RES["sparc_reference"] = {"R>=3Rd": {f: {k: v for k, v in c1[f].items() if k != "per_bin"} for f in FOOTS},
                          "R>=2Rd": {f: {k: v for k, v in SREF2[f].items() if k != "per_bin"} for f in FOOTS}}

# gas calibration on SPARC (all with MHI>0, L36>0)
X, Y = [], []
for nm, m in TAB.items():
    if m["MHI"] > 0 and m["L36"] > 0 and np.isfinite(m["T"]):
        X.append([1.0, math.log10(0.5 * m["L36"] * 1e9) - 10, m["T"] - 5]); Y.append(math.log10(m["MHI"] * 1e9))
X, Y = np.array(X), np.array(Y)
coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
SIGG = float(np.std(Y - X @ coef, ddof=3))
check("C4 SPARC HI scaling calibrated", np.isfinite(SIGG),
      f"log M_HI = {coef[0]:.3f} + {coef[1]:.3f}(log M* - 10) + {coef[2]:.3f}(T - 5); sigma_g {SIGG:.3f} dex; N {len(Y)}")
RES["gas_calibration"] = dict(a=coef[0], b=coef[1], c=coef[2], sigma_g=SIGG, N=len(Y))


def lMHI(lMs, T):
    return coef[0] + coef[1] * (lMs - 10) + coef[2] * (T - 5)


def gas_h(MHI):
    """exponential HI scale length (kpc) with Sigma_HI(D_HI/2) = 1 Msun/pc^2, D_HI from Wang+16; larger root."""
    Rhi = 0.5 * 10 ** (0.506 * math.log10(MHI) - 3.293) * 1e3          # pc
    fz = lambda h: math.log(MHI / (2 * math.pi * h * h)) - Rhi / h
    hm = Rhi / 2.0                                                      # argmax of fz
    if fz(hm) <= 0:
        return hm / 1e3, False
    return brentq(fz, hm, 100 * Rhi) / 1e3, True


# ================================================================== SPARC overlap tools
RC3n = {}
for line in open(os.path.join(DATA, "rc3_devaucouleurs1991_colors.tsv")):
    p = line.rstrip("\n").split("\t")
    if len(p) < 6 or not np.isfinite(fnum(p[0])):
        continue
    e = dict(ra=fnum(p[0]), dec=fnum(p[1]), name=normname(p[2]), alt=normname(p[3]), T=fnum(p[5]))
    for k in (e["name"], e["alt"]):
        if k:
            RC3n.setdefault(k, e)
spos = json.load(open(os.path.join(DATA, "sparc_positions_merged.json")))
SPN = {normname(n) for n in TAB} | {normname(n) for n in spos}


def unit(a, d):
    a, d = np.radians(a), np.radians(d)
    return np.array([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)])


SPU = np.array([unit(v["ra"], v["dec"]) for v in spos.values() if v.get("ra") is not None and v.get("dec") is not None])


def overlap(k):
    names = {k}
    e = RC3n.get(k)
    if e:
        names |= {e["name"], e["alt"]} - {""}
    hit = names & SPN
    pos = T1.get(k) or (dict(ra=e["ra"], dec=e["dec"]) if e else None)
    sep = np.nan
    if pos is not None:
        sep = float(np.degrees(np.arccos(np.clip(SPU @ unit(pos["ra"], pos["dec"]), -1, 1))).min() * 3600)
    return bool(hit or (np.isfinite(sep) and sep <= 60.0)), sorted(hit), sep, pos is not None


# ================================================================== ADDENDUM: merge 388/500 curves (extension only)
if EXT:
    L_f8 = lines("J_MNRAS_388_500_tablef.dat")
    RC8 = collections.defaultdict(list)
    for l in L_f8:
        RC8[normname(l[0:9])].append((fnum(l[10:15]), fnum(l[32:35]), fnum(l[36:39]), l[43:44]))
    mapped, unmapped, dup, added = [], [], [], 0
    for k8, pts in RC8.items():
        k = k8
        if not k.startswith("UGC"):
            e = RC3n.get(k8)
            cand = [x for x in ((e or {}).get("name", ""), (e or {}).get("alt", "")) if x.startswith("UGC")]
            if cand:
                k = cand[0]; mapped.append(f"{k8}->{k}")
            else:
                unmapped.append(k8)
        if k in RC:
            dup.append(k); continue
        RC[k] = pts; added += 1
    check("ADD-1 388/500 tablef row count 5505", len(L_f8) == 5505, f"{len(L_f8)} rows, {len(RC8)} galaxies")
    P(f"ADDENDUM merge: 388/500 galaxies {len(RC8)}; non-UGC names mapped via RC3 {len(mapped)} {mapped}; unmapped (kept under own name; "
      f"no Korsaga photometry unless listed) {unmapped}; duplicates of 390/466 (390/466 curve kept) {len(dup)} {dup}; added {added}; combined RC galaxies {len(RC)}")
    RES["addendum_merge"] = dict(n388=len(RC8), rows388=len(L_f8), mapped=mapped, unmapped=unmapped, duplicates=dup, added=added, combined=len(RC))

# ================================================================== baryon model
def cb_b(n):
    return 2 * n - 1 / 3 + 4 / (405 * n) + 46 / (25515 * n * n)


def sersic_menc_fn(n, re):
    """normalised enclosed-mass fraction M(<r)/M_tot of a Prugniel-Simien deprojected Sersic sphere; r, re in kpc."""
    b = cb_b(n); p = 1 - 0.6097 / n + 0.05463 / n ** 2
    r = np.logspace(-5, math.log10(300), 6000) * re
    rho = (r / re) ** (-p) * np.exp(-b * (r / re) ** (1 / n))
    dm = 4 * np.pi * r ** 2 * rho
    m = np.concatenate([[0], np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r))])
    m /= m[-1]
    return lambda R: np.interp(R, r, m, left=0.0, right=1.0)


def build():
    gals, cut_log = [], collections.Counter(); ovl = []; nopos = 0
    for k in sorted(RC):
        cut_log["rc"] += 1
        if k not in A1:
            continue
        cut_log["in_korsaga"] += 1
        a, b3 = A1[k], B3[k]
        R = np.array([x[0] for x in RC[k]]); V = np.array([x[1] for x in RC[k]]); eV = np.array([x[2] for x in RC[k]])
        ok = (R > 0) & (V > 0) & np.isfinite(eV)
        R, V, eV = R[ok], V[ok], eV[ok]
        I0 = 10 ** (0.4 * (MSUN_RC + 21.572 - a["mu0"])); h = a["h"]
        Ld = 2 * math.pi * I0 * (h * 1e3) ** 2
        Lb, fb = 0.0, None
        if np.isfinite(a["mue"]) and np.isfinite(a["re"]) and np.isfinite(a["n"]) and a["re"] > 0:
            Ie = 10 ** (0.4 * (MSUN_RC + 21.572 - a["mue"])); bn = cb_b(a["n"])
            Lb = 2 * math.pi * a["n"] * math.exp(bn) * bn ** (-2 * a["n"]) * Gfun(2 * a["n"]) * Ie * (a["re"] * 1e3) ** 2
            fb = sersic_menc_fn(a["n"], a["re"])
        ups = 10 ** (-0.660 + 1.222 * a["BV"])
        lMs = math.log10(ups * (Ld + Lb))
        lhi = lMHI(lMs, b3["T"]); hg, okh = gas_h(10 ** lhi)
        is_ov, hit, sep, haspos = overlap(k)
        nopos += (not haspos)
        if is_ov:
            ovl.append(dict(name=k, names=hit, sep=sep))
        x25 = a["R25h"]
        gals.append(dict(name=k, T=b3["T"], inc=b3["inc"], f=a["f"], R=R, V=V, eV=eV, h=h, Ld=Ld, Lb=Lb, fb=fb, ups=ups, ups_a2=A2.get(k, np.nan),
                         lMs=lMs, lMHI=lhi, hg=hg, hg_ok=okh, overlap=is_ov, sep=sep, Rlh=a["Rlh"],
                         LD_ratio=(Ld * (1 - (1 + x25) * math.exp(-x25)) / 1e8) / a["LD"] if a["LD"] > 0 else np.nan,
                         LB_ratio=(Lb / 1e8) / a["LB"] if np.isfinite(a["LB"]) and a["LB"] > 0 else np.nan,
                         nin=int((R <= 1.5 * h).sum()), nout3=int((R >= 3 * h).sum()), nout2=int((R >= 2 * h).sum()),
                         seeing=T1.get(k, {}).get("seeing", np.nan), D=b3["D"]))
    return gals, cut_log, ovl, nopos


GALS, CUTS, OVL, NOPOS = build()
for g in GALS:
    g["lMb"] = math.log10(10 ** g["lMs"] + 1.33 * 10 ** g["lMHI"])
lr = np.array([g["LD_ratio"] for g in GALS]); br = np.array([g["LB_ratio"] for g in GALS])
check("C2 photometry: profile luminosity vs Korsaga LD (to R25) and LB, medians within 10%",
      abs(np.nanmedian(lr) - 1) <= 0.10 and abs(np.nanmedian(br) - 1) <= 0.10,
      f"median L_d(<R25)/LD {np.nanmedian(lr):.3f} (range {np.nanmin(lr):.2f}-{np.nanmax(lr):.2f}); median L_b/LB {np.nanmedian(br):.3f} "
      f"(range {np.nanmin(br):.2f}-{np.nanmax(br):.2f}; N {np.isfinite(br).sum()})")
da2 = [abs(g["ups"] - g["ups_a2"]) for g in GALS if np.isfinite(g["ups_a2"])]
check("C3 Upsilon_Rc equals Korsaga tablea2 M/LfML to 0.01", max(da2) <= 0.01 + 1e-9, f"max |diff| {max(da2):.4f} over {len(da2)}")
P(f"gas scale-length root found for {sum(g['hg_ok'] for g in GALS)}/{len(GALS)} galaxies")
P(f"SPARC overlaps among the {len(GALS)} RC galaxies with Korsaga photometry: {len(OVL)} -> {[(o['name'], o['names'], round(o['sep'], 1)) for o in OVL]}; "
  f"galaxies without any position: {NOPOS}")


def select(gals, overlap_removed=True, cuts=True):
    out = []
    for g in gals:
        if cuts and (g["f"] > 2 or not g["inc"] >= 30):
            continue
        if overlap_removed and g["overlap"]:
            continue
        out.append(g)
    return out


PRIM = select(GALS)
nb = len(select(GALS, overlap_removed=False))
P(f"sample: RC {CUTS['rc']}; with Korsaga photometry {CUTS['in_korsaga']}; f_ID<=2 & i>=30 {nb}; minus SPARC overlaps -> PRIMARY N {len(PRIM)} "
  f"(early {sum(g['T'] <= 3 for g in PRIM)}, late {sum(g['T'] > 3 for g in PRIM)})")
P(f"inner band: {sum(g['nin'] >= 2 for g in PRIM)}/{len(PRIM)} have >= 2 points at R <= 1.5 R_d; outer band 3 R_d: {sum(g['nout3'] >= 2 for g in PRIM)} "
  f"(early {sum(g['nout3'] >= 2 and g['T'] <= 3 for g in PRIM)}); 2 R_d: {sum(g['nout2'] >= 2 for g in PRIM)} (early {sum(g['nout2'] >= 2 and g['T'] <= 3 for g in PRIM)})")
hs = [g["h"] / (g["D"] * 1e3 * math.pi / (180 * 3600)) / g["seeing"] for g in PRIM if np.isfinite(g["seeing"]) and g["seeing"] > 0]
P(f"median h / seeing (Barbosa table1, OHP) = {np.median(hs):.1f} (N {len(hs)})")
RES["sample"] = dict(counts=dict(CUTS), n_cut=nb, overlaps=OVL, n_overlap_in_cut=nb - len(PRIM), N_primary=len(PRIM),
                     n_early=sum(g['T'] <= 3 for g in PRIM), n_inner_ge2=sum(g['nin'] >= 2 for g in PRIM),
                     n_outer3_ge2=sum(g['nout3'] >= 2 for g in PRIM), n_outer3_ge2_early=sum(g['nout3'] >= 2 and g['T'] <= 3 for g in PRIM),
                     n_outer2_ge2=sum(g['nout2'] >= 2 for g in PRIM), n_outer2_ge2_early=sum(g['nout2'] >= 2 and g['T'] <= 3 for g in PRIM),
                     median_h_over_seeing=float(np.median(hs)) if hs else None)

# ================================================================== power forecast (no GHASP residual)
P("\n== POWER FORECAST (SPARC within-bin within-class d_out scatter x GHASP counts; no GHASP residual) ==")


def sparc_binvar(rows):
    x = np.array([r["d_out"] for r in rows]); lm = np.array([r["lMb"] for r in rows]); Ts = np.array([r["T"] for r in rows])
    binvar, pooled = {}, []
    for lo, hi in zip(EDG0[:-1], EDG0[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        vs = [(x[m & c].var(ddof=1), (m & c).sum() - 1) for c in (Ts <= 3, Ts > 3) if (m & c).sum() >= 2]
        if vs:
            binvar[round(lo, 2)] = float(np.average([v for v, n in vs], weights=[n for v, n in vs])); pooled += vs
    return binvar, float(np.average([v for v, n in pooled], weights=[n for v, n in pooled]))


def forecast(lmb, early, valid, binvar, pv, ref):
    out = {}
    for infl in (1.0, 1.5):
        den = 0.0; nbins = ne = nl = 0; per = []
        for lo, hi in zip(EDG0[:-1], EDG0[1:]):
            m = (lmb >= lo) & (lmb < hi) & valid
            a, b = int((m & early).sum()), int((m & ~early).sum())
            if a or b:
                per.append((round(lo, 2), a, b))
            if a >= 2 and b >= 2:
                s2 = binvar.get(round(lo, 2), pv) * infl ** 2
                den += 1 / (s2 / a + s2 / b); nbins += 1; ne += a; nl += b
        sig = den ** -0.5 if den else np.nan
        out[f"x{infl}"] = dict(sigma_fc=sig, expected_Z=ref / sig if den else np.nan,
                               power=float(norm.cdf(ref / sig - 2)) if den else 0.0, nbins=nbins, n_early=ne, n_late=nl,
                               adequate=bool(nbins >= 2 and ne >= 8))
    out["counts_per_bin(lo,early,late)"] = per
    return out


FC = {}
for f in FOOTS:
    bv3, pv3 = sparc_binvar(SPR[f]); bv2, pv2 = sparc_binvar(SPR2[f])
    lmb = np.array([g["lMb"] for g in PRIM]); E = np.array([g["T"] <= 3 for g in PRIM])
    FC[f] = {"primary R>=3Rd": forecast(lmb, E, np.array([g["nout3"] >= 2 for g in PRIM]), bv3, pv3, REF),
             "D2 R>=2Rd": forecast(lmb, E, np.array([g["nout2"] >= 2 for g in PRIM]), bv2, pv2, SREF2[f]["diff"])}
    # full-GHASP forecast from Korsaga Rlast/h (all tablea1, f<=2, tableb3 i>=30, overlaps removed)
    fl = []
    for k, a in A1.items():
        if a["f"] > 2 or not B3[k]["inc"] >= 30 or overlap(k)[0]:
            continue
        I0 = 10 ** (0.4 * (MSUN_RC + 21.572 - a["mu0"])); Ld = 2 * math.pi * I0 * (a["h"] * 1e3) ** 2; Lb = 0.0
        if np.isfinite(a["mue"]) and np.isfinite(a["re"]) and np.isfinite(a["n"]) and a["re"] > 0:
            Ie = 10 ** (0.4 * (MSUN_RC + 21.572 - a["mue"])); bn = cb_b(a["n"])
            Lb = 2 * math.pi * a["n"] * math.exp(bn) * bn ** (-2 * a["n"]) * Gfun(2 * a["n"]) * Ie * (a["re"] * 1e3) ** 2
        lMs = math.log10(10 ** (-0.660 + 1.222 * a["BV"]) * (Ld + Lb))
        fl.append(dict(name=k, lMb=math.log10(10 ** lMs + 1.33 * 10 ** lMHI(lMs, B3[k]["T"])), early=B3[k]["T"] <= 3, Rlh=a["Rlh"], inRC=k in RC))
    lmb = np.array([x["lMb"] for x in fl]); E = np.array([x["early"] for x in fl]); Rl = np.array([x["Rlh"] for x in fl])
    FC[f]["FULL GHASP (Korsaga Rlast/h>=3)"] = forecast(lmb, E, Rl >= 3, bv3, pv3, REF)
    FC[f]["FULL GHASP (Korsaga Rlast/h>=2), D2"] = forecast(lmb, E, Rl >= 2, bv2, pv2, SREF2[f]["diff"])
    FC[f]["full_ghasp_N"] = dict(N=len(fl), early=int(E.sum()), with_390_466_RC=int(sum(x["inRC"] for x in fl)),
                                 Rlh_ge3=int((Rl >= 3).sum()), Rlh_ge3_early=int(((Rl >= 3) & E).sum()),
                                 Rlh_ge2=int((Rl >= 2).sum()), Rlh_ge2_early=int(((Rl >= 2) & E).sum()))
    for nm_, o in FC[f].items():
        if nm_ == "full_ghasp_N":
            P(f"  [{f}] full GHASP (Korsaga f<=2, i>=30, no overlaps): {o}")
            continue
        for infl in ("x1.0", "x1.5"):
            q = o[infl]
            P(f"  [{f}] {nm_:36s} {infl}: sigma_fc {q['sigma_fc']:.4f}; expected Z {q['expected_Z']:.2f}; P(Z>=2) {q['power']:.2f}; "
              f"bins {q['nbins']}, early {q['n_early']}, late {q['n_late']}; adequate {q['adequate']}")
        P(f"        counts per bin (lo, early, late): {o['counts_per_bin(lo,early,late)']}")
RES["forecast"] = FC
if STAGE == "forecast":
    RES["checks"] = CHK
    json.dump(RES, open(os.path.join(HERE, f"cfg538_forecast{SUF}.json"), "w"), indent=1,
              default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    sys.exit(0)


# ================================================================== residuals
def residual_rows(gals, a0si, mult=None, gas=1.0, gas_dex=None, bo=3.0, inject=0.0, early_cut=3, Tkey="T", fixed_ups=None):
    a0 = a0si * CONV; rows = []
    for g in gals:
        u = (fixed_ups if fixed_ups is not None else g["ups"]) * (1.0 if mult is None else mult.get(g["name"], 1.0))
        R = g["R"]
        gs = freeman_g(u * g["Ld"], g["h"], R)
        if g["fb"] is not None:
            gs = gs + GKPC * u * g["Lb"] * g["fb"](R) / R ** 2
        mhi = 10 ** (g["lMHI"] + (0.0 if gas_dex is None else gas_dex.get(g["name"], 0.0))) * gas
        gg = freeman_g(1.33 * mhi, g["hg"], R) if mhi > 0 else 0.0 * R
        gb = gs + gg; gobs = g["V"] ** 2 / R
        ok = (gb > 0) & (gobs > 0) & np.isfinite(gb)
        r = np.full(len(R), np.nan); r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
        w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
        T = g[Tkey]
        if inject and T <= early_cut:
            r = r + inject * (R >= bo * g["h"])
        di, do = wmean(r, w, ok & (R <= 1.5 * g["h"])), wmean(r, w, ok & (R >= bo * g["h"]))
        rows.append(dict(name=g["name"], T=T, lMb=g["lMb"], d_in=di, d_out=do, d_oi=do - di if np.isfinite(do) and np.isfinite(di) else np.nan,
                         r=r, w=w, ok=ok))
    return rows


def arr(rows, k):
    return np.array([r[k] for r in rows], float)


def score(rows, cut=3, nsh=NSH, ref=REF):
    lm, T = arr(rows, "lMb"), arr(rows, "T")
    sc = {k: calibrated(arr(rows, k), lm, T, cut=cut, nsh=nsh) for k in ("d_out", "d_in", "d_oi")}
    sc["verdict"] = ladder(sc["d_out"], sc["d_oi"], ref=ref)
    return sc


def strip(o):
    return {k: v for k, v in o.items() if k not in ("r", "w", "ok")}


if not MUT:
    P("\n== SCORING (frozen ladder; primary = overlaps removed, gas nominal, colour M/L) ==")
    SC, V, ROWS = {}, {}, {}
    for f in FOOTS:
        rows = residual_rows(PRIM, A0SI[f]); ROWS[f] = rows
        sc = score(rows); SC[f] = sc; V[f] = sc["verdict"]
        for k in ("d_out", "d_in", "d_oi"):
            P(f"  [{f}] {k:6s}: {fmt(sc[k])}")
            for pb in sc[k]["per_bin"]:
                P(f"        bin {pb['bin']}: early {pb['n_early']} late {pb['n_late']}  {pb['diff']:+.4f} +- {pb['sig']:.4f}")
        P(f"  [{f}] VERDICT: {V[f]}")
    head = V["canonical"] if V["canonical"] == V["alt"] else f"FOOTING-DEPENDENT (canonical {V['canonical']} / alt {V['alt']})"
    P(f"\nHEADLINE (primary): {head}")
    RES["score"] = SC; RES["verdict"] = V; RES["headline"] = head
    RES["per_galaxy"] = {f: [{k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in strip(r).items()} for r in ROWS[f]] for f in FOOTS}
    for f in FOOTS:
        dout, din, T = arr(ROWS[f], "d_out"), arr(ROWS[f], "d_in"), arr(ROWS[f], "T"); E = T <= 3
        P(f"  [{f}] unmatched class means: d_out early {np.nanmean(dout[E]) if np.isfinite(dout[E]).any() else np.nan:+.4f} (N {np.isfinite(dout[E]).sum()}), "
          f"late {np.nanmean(dout[~E]):+.4f} (N {np.isfinite(dout[~E]).sum()}); d_in early {np.nanmean(din[E]):+.4f} (N {np.isfinite(din[E]).sum()}), "
          f"late {np.nanmean(din[~E]):+.4f} (N {np.isfinite(din[~E]).sum()})")

    P("\n== DESCRIPTIVE (pre-declared, NO verdict weight) ==")
    DESC = {}
    for f in FOOTS:
        a0 = A0SI[f]; ref2 = SREF2[f]["diff"]
        din = SC[f]["d_in"]
        if din["nbins"] == 0 or not din["adequate"]:
            lab = "NOT TESTABLE" if din["nbins"] == 0 else "NOT TESTABLE (inadequate)"
        else:
            lab = "INNER EXCESS" if (din["diff"] > 0 and din["Z_cal"] >= 2) else "INNER DEFICIT" if din["Z_cal"] <= -2 else "NO INNER DIFFERENCE"
        DESC[f"{f}|D1 inner half"] = dict(label=lab, **{k: v for k, v in din.items() if k != "per_bin"}, per_bin=din["per_bin"])
        P(f"  [{f}] D1 Delta_in: {fmt(din)} -> {lab}")
        variants = {
            "D2 R>=2Rd": (PRIM, dict(bo=2.0), ref2),
            "D3 no f/inc cuts": (select(GALS, cuts=False), {}, REF),
            "WITH OVERLAPS primary": (select(GALS, overlap_removed=False), {}, REF),
            "WITH OVERLAPS D2": (select(GALS, overlap_removed=False), dict(bo=2.0), ref2),
            "WITH OVERLAPS D3": (select(GALS, overlap_removed=False, cuts=False), {}, REF),
        }
        for nm_, (gs_, kw, ref) in variants.items():
            rows = residual_rows(gs_, a0, **kw); sc = score(rows, ref=ref)
            DESC[f"{f}|{nm_}"] = dict(N=len(gs_), ref=ref, verdict_label=sc["verdict"],
                                      **{k: {kk: vv for kk, vv in sc[k].items()} for k in ("d_out", "d_in", "d_oi")})
            P(f"  [{f}] {nm_:22s} N {len(gs_)} (ref {ref:+.4f}): d_out {fmt(sc['d_out'])}")
            P(f"  {'':28s} d_oi {fmt(sc['d_oi'])}; label: {sc['verdict']}")
            for pb in sc["d_out"]["per_bin"]:
                P(f"        bin {pb['bin']}: early {pb['n_early']} late {pb['n_late']}  {pb['diff']:+.4f} +- {pb['sig']:.4f}")
    RES["descriptive"] = DESC

    # which statistic carries the free-M/L / MUTATE / sensitivity work
    def target():
        if SC["canonical"]["d_out"]["adequate"] and SC["alt"]["d_out"]["adequate"]:
            return "primary", PRIM, dict(), REF
        for nm_, gs_, kw in (("D2 R>=2Rd", PRIM, dict(bo=2.0)), ("D3 no f/inc cuts", select(GALS, cuts=False), {}),
                             ("WITH OVERLAPS D2", select(GALS, overlap_removed=False), dict(bo=2.0))):
            if all(DESC[f"{f}|{nm_}"]["d_out"]["adequate"] for f in FOOTS):
                return nm_, gs_, kw, None
        cands = [("primary", PRIM, {}), ("D2 R>=2Rd", PRIM, dict(bo=2.0)), ("D3 no f/inc cuts", select(GALS, cuts=False), {}),
                 ("WITH OVERLAPS D2", select(GALS, overlap_removed=False), dict(bo=2.0))]
        nbs = [(SC["canonical"]["d_out"]["nbins"] if c[0] == "primary" else DESC[f"canonical|{c[0]}"]["d_out"]["nbins"]) for c in cands]
        c = cands[int(np.argmax(nbs))]
        return c[0], c[1], c[2], None
    TNAME, TG, TKW, _ = target()
    RES["work_statistic"] = TNAME
    P(f"\n(free-M/L / sensitivities run on: {TNAME}{'' if TNAME == 'primary' else ', NO verdict weight'})")
    json.dump(dict(target=TNAME), open(os.path.join(HERE, f"cfg538_target{'_ext' if EXT else ''}.json"), "w"))

    P("\n== FREE STELLAR M/L (multiplier on the colour M/L, log10 f in [-0.3, 0.3]) ==")
    GRID = np.round(np.arange(-0.30, 0.30 + 1e-9, 0.01), 2)
    MLR = {}

    def fit_mult(g, a0, region):
        best, bf = np.inf, np.nan
        for lf in GRID:
            rr = residual_rows([g], a0, mult={g["name"]: 10 ** lf}, **TKW)[0]
            m = rr["ok"] & np.isfinite(rr["r"])
            if region == "inner":
                m = m & (g["R"] <= 1.5 * g["h"])
            if m.sum() < 2:
                return np.nan
            c = float((rr["w"][m] * rr["r"][m] ** 2).sum())
            if c < best:
                best, bf = c, lf
        return bf

    for f in FOOTS:
        a0 = A0SI[f]
        ref = REF if TNAME in ("primary", "D3 no f/inc cuts") else SREF2[f]["diff"]
        F1 = {g["name"]: fit_mult(g, a0, "all") for g in TG}
        F2 = {}
        for g in TG:
            v = fit_mult(g, a0, "inner"); F2[g["name"]] = 0.0 if not np.isfinite(v) else v
        E_ = {g["name"]: g["T"] <= 3 for g in TG}
        VV = {"B1 global free": {k: 10 ** v for k, v in F1.items() if np.isfinite(v)},
              "B2 inner-fit": {k: 10 ** v for k, v in F2.items()},
              "B3 early x2 / late x0.5": {k: (2.0 if E_[k] else 0.5) for k in E_}}
        o = {}
        for nm_, mult in VV.items():
            rows = residual_rows(TG, a0, mult=mult, **TKW)
            sc = {k: calibrated(arr(rows, k), arr(rows, "lMb"), arr(rows, "T"), nsh=1000) for k in ("d_out", "d_in", "d_oi")}
            lfr = [dict(lMb=g["lMb"], lf=math.log10(mult.get(g["name"], 1.0))) for g in TG]
            sc["dlogf"] = stat(np.array([x["lf"] for x in lfr]), np.array([x["lMb"] for x in lfr]), np.array([g["T"] <= 3 for g in TG]))
            o[nm_] = sc
            P(f"  [{f}] {nm_:24s}: d_out {fmt(sc['d_out'])}")
            P(f"  {'':32s} d_in {sc['d_in']['diff']:+.4f} (Z_cal {sc['d_in'].get('Z_cal', np.nan):+.2f}); d_oi {sc['d_oi']['diff']:+.4f}; "
              f"early-late dlog f {sc['dlogf']['diff']:+.3f} (Z {sc['dlogf']['Z']:+.2f})")
        z1, z2 = o["B1 global free"]["d_out"], o["B2 inner-fit"]["d_out"]
        if z1["nbins"] == 0 or z2["nbins"] == 0:
            v = "NOT TESTABLE"
        elif z1["diff"] > 0 and z1["Z_cal"] >= 2 and z2["diff"] > 0 and z2["Z_cal"] >= 2:
            v = "EXCESS SURVIVES M/L"
        elif z1["Z_cal"] < 1 or z2["Z_cal"] < 1:
            v = "ABSORBED BY M/L"
        else:
            v = "PARTIAL"
        o["label"] = v + ("" if TNAME == "primary" else " (on %s; no verdict weight)" % TNAME)
        o["per_galaxy_log10f_B1"] = F1
        P(f"  [{f}] M/L label: {o['label']}")
        MLR[f] = o
    RES["free_ML"] = MLR

    P("\n== SENSITIVITIES (no verdict weight; on %s) ==" % TNAME)
    SENS = {}
    rng = np.random.default_rng(5380)
    draws = [{g["name"]: float(rng.normal(0, SIGG)) for g in TG} for _ in range(200)]
    medu = float(np.median([g["ups"] for g in TG]))
    for g in GALS:
        e = RC3n.get(g["name"])
        g["T_rc3"] = e["T"] if (e and np.isfinite(e["T"])) else g["T"]
    for f in FOOTS:
        a0 = A0SI[f]
        base = residual_rows(TG, a0, **TKW); b0 = stat(arr(base, "d_out"), arr(base, "lMb"), arr(base, "T") <= 3)
        var = {"S1 single Upsilon_Rc (median %.2f)" % medu: dict(fixed_ups=medu), "S2 RC3 T": dict(Tkey="T_rc3"),
               "G0 gas omitted": dict(gas=0.0), "G+ gas x2": dict(gas=2.0), "G- gas x0.5": dict(gas=0.5)}
        for nm_, kw in var.items():
            rows = residual_rows(TG, a0, **TKW, **kw)
            o = stat(arr(rows, "d_out"), arr(rows, "lMb"), arr(rows, "T") <= 3)
            oi = stat(arr(rows, "d_in"), arr(rows, "lMb"), arr(rows, "T") <= 3)
            SENS[f"{f}|{nm_}"] = dict(d_out={k: v for k, v in o.items() if k != "per_bin"}, d_in={k: v for k, v in oi.items() if k != "per_bin"})
            P(f"  [{f}] {nm_:30s}: d_out {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}); d_in {oi['diff']:+.4f} (Z {oi['Z']:+.2f}; bins {oi['nbins']})")
        g0 = SENS[f"{f}|G0 gas omitted"]["d_out"]["diff"] - b0["diff"]
        g0i = SENS[f"{f}|G0 gas omitted"]["d_in"]["diff"] - stat(arr(base, "d_in"), arr(base, "lMb"), arr(base, "T") <= 3)["diff"]
        SENS[f"{f}|gas bias Delta(G0)-Delta(nominal)"] = dict(d_out=g0, d_in=g0i)
        P(f"  [{f}] gas bias Delta(G0) - Delta(nominal): d_out {g0:+.4f}; d_in {g0i:+.4f}  (negative = against H, as pre-stated)")
        mc = []
        for dd in draws:
            rows = residual_rows(TG, a0, gas_dex=dd, **TKW)
            mc.append(stat(arr(rows, "d_out"), arr(rows, "lMb"), arr(rows, "T") <= 3)["diff"])
        mc = np.array(mc)
        SENS[f"{f}|GMC sigma_g scatter"] = dict(mean=float(np.nanmean(mc)), sd=float(np.nanstd(mc)), n=int(np.isfinite(mc).sum()))
        P(f"  [{f}] GMC (200 draws, sigma_g {SIGG:.2f} dex): d_out mean {np.nanmean(mc):+.4f}, sd {np.nanstd(mc):.4f}")
        for cut in (2, 4):
            rows = base
            o = stat(arr(rows, "d_out"), arr(rows, "lMb"), arr(rows, "T") <= cut)
            SENS[f"{f}|S3 T<={cut}"] = {k: v for k, v in o.items() if k != "per_bin"}
            P(f"  [{f}] S3 T<={cut:<27d}: d_out {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']})")
        o = stat(arr(base, "d_out"), arr(base, "lMb"), arr(base, "T") <= 3, edg=EDG0 + 0.2)
        SENS[f"{f}|S4 bins +0.2"] = {k: v for k, v in o.items() if k != "per_bin"}
        P(f"  [{f}] S4 bins +0.2 dex              : d_out {o['diff']:+.4f} +- {o['sig']:.4f} (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o['n_early']}, late {o['n_late']})")
        # leave-one-galaxy-out on the work statistic
        zs = []
        for i in range(len(base)):
            rr = base[:i] + base[i + 1:]
            o = stat(arr(rr, "d_out"), arr(rr, "lMb"), arr(rr, "T") <= 3)
            if np.isfinite(o["Z"]):
                zs.append((o["Z"], o["diff"], base[i]["name"]))
        if zs:
            SENS[f"{f}|leave-one-out"] = dict(Z_min=min(zs)[0], drop_min=min(zs)[2], Z_max=max(zs)[0], drop_max=max(zs)[2],
                                             diff_min=min(z[1] for z in zs), diff_max=max(z[1] for z in zs))
            P(f"  [{f}] leave-one-out Z {min(zs)[0]:+.2f} (drop {min(zs)[2]}) .. {max(zs)[0]:+.2f} (drop {max(zs)[2]})")
    RES["sensitivities"] = SENS
else:
    TNAME = json.load(open(os.path.join(HERE, f"cfg538_target{'_ext' if EXT else ''}.json")))["target"]
    TG, TKW = {"primary": (PRIM, {}), "D2 R>=2Rd": (PRIM, dict(bo=2.0)), "D3 no f/inc cuts": (select(GALS, cuts=False), {}),
               "WITH OVERLAPS D2": (select(GALS, overlap_removed=False), dict(bo=2.0))}[TNAME]
    P(f"\n== MUTATE (on {TNAME}) ==")
    MU = {}
    for f in FOOTS:
        rows = residual_rows(TG, A0SI[f], **TKW); lm, T = arr(rows, "lMb"), arr(rows, "T")
        base = stat(arr(rows, "d_out"), lm, T <= 3)
        rng = np.random.default_rng(538)
        zs = np.array([stat(arr(rows, "d_out"), lm, Ts <= 3)["Z"] for Ts in shuffles(lm, T, rng, 200)]); zs = zs[np.isfinite(zs)]
        MU[f"MU1_{f}"] = dict(mean_Z=float(zs.mean()), sd_Z=float(zs.std()), n=len(zs), frac_Z_ge_2=float((zs >= 2).mean()), base_Z=base["Z"])
        check(f"MU1 [{f}] T shuffled within bins kills Delta_out: |mean Z| < 0.5", abs(zs.mean()) < 0.5,
              f"mean Z {zs.mean():+.3f} (sd {zs.std():.2f}; n {len(zs)}; P(Z>=2) {(zs >= 2).mean():.3f}); unshuffled Z {base['Z']:+.2f}")
        inj = stat(arr(residual_rows(TG, A0SI[f], inject=REF, **TKW), "d_out"), lm, T <= 3)
        sh = inj["diff"] - base["diff"]
        MU[f"MU2_{f}"] = dict(shift=sh, base=base["diff"], injected=inj["diff"])
        check(f"MU2 [{f}] +{REF} injection into early outer residuals recovered within 0.002", abs(sh - REF) <= 0.002, f"shift {sh:+.4f}")
    RES["mutate_results"] = MU
    RES["work_statistic"] = TNAME

RES["checks"] = CHK
P(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass")
json.dump(RES, open(os.path.join(HERE, f"cfg538_ghasp_results{SUF}.json"), "w"), indent=1,
          default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else float(o) if isinstance(o, (np.floating, np.integer, np.bool_)) else str(o))
