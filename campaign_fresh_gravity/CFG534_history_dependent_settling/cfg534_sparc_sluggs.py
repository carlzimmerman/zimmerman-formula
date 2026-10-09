#!/usr/bin/env python3
"""CFG534 Tests 2, 3 and the SPARC / SLUGGS parts of Test 4 (FROZEN_CRITERIA.md, criteria commit aa8dc312e).
Test 2  SLUGGS (AUDIT_SLUGGS per-galaxy offsets, nu_mono): partial Spearman rho(offset, proxy | log M*) for environment, central
        status, E morphology, log L_X/L_B and a composite H-score; permutation p inside log M* tertile blocks.
Test 3  SPARC (Q <= 2, Inc >= 30; Ups 0.5 / 0.7): early (T <= 3) minus late (T >= 4) law residuals matched in log M_b bins; partial
        rho with T, f_gas, SB.
Test 4  inner vs outer: SPARC Delta_in (R <= 1.5 Rd) / Delta_out (R >= 3 Rd); SLUGGS D_in = -inner_salp, D_out = 2 off_salp.
MUTATE (CFG534_MUTATE=1 -> *_MUTATE.*): MU3 T shuffled inside M_b bins (200x), MU4 SLUGGS proxies shuffled inside mass blocks (2000x).
Run: nice -n 10 python3 cfg534_sparc_sluggs.py ; CFG534_MUTATE=1 nice -n 10 python3 cfg534_sparc_sluggs.py
"""
import os, sys, re, json, math
import numpy as np
from scipy.stats import spearmanr, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = os.environ.get("CFG534_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
LOG, CHK = [], {}
RES = {"lane": "CFG534", "script": "cfg534_sparc_sluggs", "mutate": MUT, "criteria_commit": "aa8dc312e",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass still required; not theory closed"}
try:
    os.nice(10)
except OSError:
    pass


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


G = 4.30091e-6
CONV = 3.0857e19 / 1e6
A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")


def nu(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def partial(a, b, c):
    ra, rb, rc = rankdata(a), rankdata(b), rankdata(c)
    X = np.vstack([rc, np.ones_like(rc)]).T
    res = lambda x: x - X @ np.linalg.lstsq(X, x, rcond=None)[0]
    return float(np.corrcoef(res(ra), res(rb))[0, 1])


# ================================================================== SPARC
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
ALLG = []
for f in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not f.endswith("_rotmod.dat"):
        continue
    d = np.genfromtxt(os.path.join(DATA, "sparc_data", f), comments="#")
    nm = f.replace("_rotmod.dat", "")
    if d.ndim != 2 or d.shape[1] < 6 or nm not in TAB:
        continue
    ALLG.append(dict(name=nm, R=d[:, 0], V=d[:, 1], eV=d[:, 2], Vg=d[:, 3], Vd=d[:, 4], Vb=d[:, 5], m=TAB[nm]))


def resid(g, a0):
    Vb2 = g["Vg"] * np.abs(g["Vg"]) + 0.5 * g["Vd"] ** 2 + 0.7 * g["Vb"] ** 2
    gb = Vb2 / g["R"]; gobs = g["V"] ** 2 / g["R"]
    ok = (gb > 0) & (gobs > 0)
    r = np.full(len(g["R"]), np.nan)
    r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
    sp = 2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)
    return r, ok, 1.0 / (sp ** 2 + 0.05 ** 2)


# K3: CFG533's K2 statistic (its footings 9.36e-11 / 1.13e-10)
ref533 = {"canonical": (9.36e-11, 0.1117), "alt": (1.13e-10, 0.1005)}
k3 = {}
for foot, (a, ref) in ref533.items():
    rs, ws = [], []
    for g in ALLG:
        if int(g["m"]["Q"]) > 2:
            continue
        r, ok, _ = resid(g, a * CONV)
        rs.append(r[ok]); ws.append((g["V"][ok] / np.maximum(g["eV"][ok], 1e-3)) ** 2)
    r, w = np.concatenate(rs), np.concatenate(ws)
    k3[foot] = float(np.sqrt(np.sum(w * r * r) / np.sum(w)))
check("K3 SPARC ALG weighted rms on Q <= 2 reproduces CFG533 K2 within 0.005", all(abs(k3[f] - ref533[f][1]) <= 0.005 for f in FOOTS),
      f"{k3} vs {[ref533[f][1] for f in FOOTS]}")

SAMP = [g for g in ALLG if int(g["m"]["Q"]) <= 2 and g["m"]["Inc"] >= 30]
P(f"SPARC: {len(ALLG)} rotmod with table rows; Q <= 2 & Inc >= 30: {len(SAMP)}")


def wmean(r, w, m):
    m = m & np.isfinite(r)
    return float((r[m] * w[m]).sum() / w[m].sum()) if m.sum() >= 2 else np.nan


ROWS = {}
for foot in FOOTS:
    a0 = A0SI[foot] * CONV
    rows = []
    for g in SAMP:
        r, ok, w = resid(g, a0)
        Rd = g["m"]["Rdisk"]
        Ms, Mg = 0.5 * g["m"]["L36"], 1.33 * g["m"]["MHI"]
        rows.append(dict(name=g["name"], T=int(g["m"]["T"]), lMb=math.log10((Ms + Mg) * 1e9), fgas=Mg / (Ms + Mg), lSB=math.log10(max(g["m"]["SBeff"], 1e-3)),
                         d_all=wmean(r, w, ok), d_in=wmean(r, w, ok & (g["R"] <= 1.5 * Rd)), d_out=wmean(r, w, ok & (g["R"] >= 3 * Rd))))
    ROWS[foot] = rows
EDG = np.arange(7.0, 12.2 + 1e-9, 0.4)


def matched(rows, key, early):
    """inverse-variance combination over log M_b bins of mean(early) - mean(late)."""
    x = np.array([r[key] for r in rows]); lm = np.array([r["lMb"] for r in rows])
    num = den = 0.0; nb = ne = nl = 0
    for lo, hi in zip(EDG[:-1], EDG[1:]):
        m = (lm >= lo) & (lm < hi) & np.isfinite(x)
        a, b = x[m & early], x[m & ~early]
        if len(a) >= 2 and len(b) >= 2:
            v = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)
            num += (a.mean() - b.mean()) / v; den += 1 / v; nb += 1; ne += len(a); nl += len(b)
    if den == 0:
        return dict(diff=np.nan, sig=np.nan, Z=np.nan, nbins=0)
    return dict(diff=num / den, sig=den ** -0.5, Z=num / den ** 0.5, nbins=nb, n_early=ne, n_late=nl)


def outin(rows):
    return [dict(r, d_oi=(r["d_out"] - r["d_in"]) if np.isfinite(r["d_out"]) and np.isfinite(r["d_in"]) else np.nan) for r in rows]


SP = {}
for foot in FOOTS:
    rows = outin(ROWS[foot])
    T = np.array([r["T"] for r in rows]); early = T <= 3
    out = {k: matched(rows, k, early) for k in ("d_out", "d_in", "d_all", "d_oi")}
    lm = np.array([r["lMb"] for r in rows]); dout = np.array([r["d_out"] for r in rows]); fin = np.isfinite(dout)
    out["rho_dout_T"] = partial(dout[fin], T[fin], lm[fin])
    out["rho_dout_fgas"] = partial(dout[fin], np.array([r["fgas"] for r in rows])[fin], lm[fin])
    out["rho_dout_SB"] = partial(dout[fin], np.array([r["lSB"] for r in rows])[fin], lm[fin])
    out["n_dout"] = int(fin.sum()); out["n_early_total"] = int(early.sum())
    SP[foot] = out
    P(f"\n[SPARC {foot}] early (T<=3, N {early.sum()}) - late matched in log M_b bins:")
    for k in ("d_out", "d_in", "d_all", "d_oi"):
        o = out[k]
        P(f"   {k:6s}: {o['diff']:+.4f} +- {o['sig']:.4f} dex (Z {o['Z']:+.2f}; bins {o['nbins']}, early {o.get('n_early')}, late {o.get('n_late')})")
    P(f"   partial rho(Delta_out, T | M_b) {out['rho_dout_T']:+.3f}; (f_gas) {out['rho_dout_fgas']:+.3f}; (log SB, reported) {out['rho_dout_SB']:+.3f}; N {out['n_dout']}")
RES["sparc"] = SP

# ------------------------------------------------------------------ POST-FREEZE robustness of the SPARC numbers (added 2026-10-09
# after the first run; NO verdict weight): Upsilon, class cut, region edges, bin phase, leave-one-galaxy-out, per-bin values.
if not MUT:
    P("\n== POST-FREEZE SPARC robustness (no verdict weight) ==")
    PFS = {}

    def rows_v(a0, ud=0.5, ub=0.7, rin=1.5, rout=3.0, incmax=91.0):
        out = []
        for g in SAMP:
            if g["m"]["Inc"] > incmax:
                continue
            Vb2 = g["Vg"] * np.abs(g["Vg"]) + ud * g["Vd"] ** 2 + ub * g["Vb"] ** 2
            gb = Vb2 / g["R"]; gobs = g["V"] ** 2 / g["R"]; ok = (gb > 0) & (gobs > 0)
            r = np.full(len(g["R"]), np.nan); r[ok] = np.log10(gobs[ok] / (nu(gb[ok] / a0) * gb[ok]))
            w = 1.0 / ((2 * g["eV"] / np.maximum(g["V"], 1e-3) / math.log(10)) ** 2 + 0.05 ** 2)
            Rd = g["m"]["Rdisk"]; Ms, Mg = ud * g["m"]["L36"], 1.33 * g["m"]["MHI"]
            di, do = wmean(r, w, ok & (g["R"] <= rin * Rd)), wmean(r, w, ok & (g["R"] >= rout * Rd))
            out.append(dict(name=g["name"], T=int(g["m"]["T"]), lMb=math.log10((Ms + Mg) * 1e9), d_in=di, d_out=do,
                            d_oi=do - di if np.isfinite(do) and np.isfinite(di) else np.nan))
        return out
    EDG0 = EDG.copy()
    for foot in FOOTS:
        a0 = A0SI[foot] * CONV
        var = {"base": {}, "Ups 0.6/0.8": dict(ud=0.6, ub=0.8), "Ups 0.4/0.6": dict(ud=0.4, ub=0.6), "outer R>=2Rd": dict(rout=2.0),
               "outer R>=4Rd": dict(rout=4.0), "inner R<=1Rd": dict(rin=1.0), "Inc<=80": dict(incmax=80.0)}
        for nm, kw in var.items():
            rows = rows_v(a0, **kw); T = np.array([r["T"] for r in rows])
            for cut in (3, 2, 4):
                for ph in (0.0, 0.2):
                    EDG = EDG0 + ph
                    o = matched(rows, "d_out", T <= cut); oi = matched(rows, "d_oi", T <= cut); oin = matched(rows, "d_in", T <= cut)
                    PFS[f"{foot}|{nm}|T<={cut}|phase{ph}"] = dict(d_out=o, d_oi=oi, d_in=oin)
                    if ph == 0.0 or nm == "base":
                        P(f"  [{foot}] {nm:13s} T<={cut} phase {ph}: d_out {o['diff']:+.3f}+-{o['sig']:.3f} (Z {o['Z']:+.2f}, bins {o['nbins']}); "
                          f"d_in {oin['diff']:+.3f} (Z {oin['Z']:+.2f}); d_out-d_in {oi['diff']:+.3f} (Z {oi['Z']:+.2f})")
            EDG = EDG0
        rows = rows_v(a0); T = np.array([r["T"] for r in rows]); early = T <= 3
        zs = []
        for i in range(len(rows)):
            keep = np.ones(len(rows), bool); keep[i] = False
            rr = [r for k, r in enumerate(rows) if keep[k]]
            zs.append((matched(rr, "d_out", early[keep])["Z"], matched(rr, "d_oi", early[keep])["Z"], rows[i]["name"]))
        zo = [z[0] for z in zs]; zi = [z[1] for z in zs]
        PFS[f"{foot}|LOO"] = dict(d_out_Z_min=float(np.nanmin(zo)), d_out_Z_max=float(np.nanmax(zo)), drop_min=zs[int(np.nanargmin(zo))][2],
                                  d_oi_Z_min=float(np.nanmin(zi)), drop_min_oi=zs[int(np.nanargmin(zi))][2])
        P(f"  [{foot}] leave-one-galaxy-out: d_out Z {np.nanmin(zo):+.2f}..{np.nanmax(zo):+.2f} (min when dropping {PFS[f'{foot}|LOO']['drop_min']}); "
          f"d_out-d_in Z min {np.nanmin(zi):+.2f} (dropping {PFS[f'{foot}|LOO']['drop_min_oi']})")
        # per-bin detail (base)
        x = np.array([r["d_out"] for r in rows]); lm = np.array([r["lMb"] for r in rows])
        for lo, hi in zip(EDG[:-1], EDG[1:]):
            m = (lm >= lo) & (lm < hi) & np.isfinite(x)
            a, b = x[m & early], x[m & ~early]
            if len(a) >= 2 and len(b) >= 2:
                P(f"     bin {lo:.1f}-{hi:.1f}: early {a.mean():+.3f} (n {len(a)}: {', '.join(r['name'] for r, mm in zip(rows, m & early) if mm)}), late {b.mean():+.3f} (n {len(b)})")
                PFS[f"{foot}|bin{lo:.1f}"] = dict(early=float(a.mean()), n_early=len(a), late=float(b.mean()), n_late=len(b))
    RES["sparc_postfreeze"] = PFS

# ================================================================== SLUGGS
AUD = json.load(open(os.path.join(LANES, "AUDIT_SLUGGS_2026-10-03", "audit_sluggs_recompute_results.json")))["per_galaxy"]
FB = {}
for line in open(os.path.join(DATA, "sluggs_forbes2017_galaxies.tsv")):
    c = line.rstrip("\n").split("\t")
    if len(c) < 10 or not c[1].strip().isdigit():
        continue
    FB[c[1].strip()] = dict(lMs=float(c[4]), mtype=c[6].strip(), env=c[7].strip())
LX = {}
for line in open(os.path.join(EXT, "osullivan2001_lx", "osullivan2001_table3.tsv")):
    if line.startswith("#") or not line.strip():
        continue
    c = line.rstrip("\n").split("\t")
    m = re.match(r"NGC\s*(\d+)$", c[1].strip())
    if m and len(c) > 6 and c[6].strip():
        try:
            LX[m.group(1)] = float(c[6]) - float(c[3])
        except ValueError:
            pass
CEN = {"4486", "4374", "4365", "5846", "4649"}
names = sorted(AUD["nu_mono|canonical"], key=int)
check("K4 SLUGGS: 17 AUDIT galaxies, all in Forbes+17; 16 with L_X", len(names) == 17 and all(n in FB for n in names) and sum(n in LX for n in names) == 16,
      f"N {len(names)}, L_X {sum(n in LX for n in names)}")
lMs = np.array([FB[n]["lMs"] for n in names])
PROX = {"env": np.array([{"F": 0, "G": 1, "C": 2}[FB[n]["env"]] for n in names], float),
        "central": np.array([n in CEN for n in names], float),
        "E_morph": np.array([FB[n]["mtype"].startswith("E") for n in names], float),
        "LX_LB": np.array([LX.get(n, np.nan) for n in names])}


def hscore(prox):
    S = np.zeros(len(names)); Nn = np.zeros(len(names))
    for v in prox.values():
        f = np.isfinite(v)
        r = (rankdata(v[f]) - 1) / (f.sum() - 1)
        S[f] += r; Nn[f] += 1
    return S / Nn


PROX["H_score"] = hscore({k: PROX[k] for k in ("env", "central", "E_morph", "LX_LB")})
rng = np.random.default_rng(534)


def blocks(idx):
    o = idx[np.argsort(lMs[idx])]
    return np.array_split(o, 3)


def perm_test(y, x, sel, nperm=20000):
    sel = np.nonzero(sel & np.isfinite(x) & np.isfinite(y))[0]
    r0 = partial(y[sel], x[sel], lMs[sel])
    bl = blocks(sel); pos = {i: k for k, i in enumerate(sel)}
    rs = np.empty(nperm)
    for t in range(nperm):
        xs = x.copy()
        for b in bl:
            xs[b] = x[rng.permutation(b)]
        rs[t] = partial(y[sel], xs[sel], lMs[sel])
    return dict(rho=r0, p_pos=float(np.mean(rs >= r0)), p_neg=float(np.mean(rs <= r0)), n=len(sel), perm_mean=float(rs.mean()))


def reading(t):
    if t["rho"] > 0 and t["p_pos"] < 0.05:
        return "SUPPORTING"
    if t["rho"] < 0 and t["p_neg"] < 0.05:
        return "INCONSISTENT"
    return "CONSISTENT" if t["rho"] > 0 else "NEUTRAL"


SL = {}
ALLN = np.ones(len(names), bool)
POP = np.array([int(n) in (1023, 2768, 3377, 3607, 4278, 4365, 4374, 4459, 4473, 4486, 4494, 4526, 4649, 4697, 5846, 7457) for n in names])
for foot in FOOTS:
    pg = AUD[f"nu_mono|{foot}"]
    off = np.array([pg[n]["off"] for n in names])
    Din = np.array([-pg[n]["inner_salp"] for n in names]); Dout = np.array([2 * pg[n]["off_salp"] for n in names])
    out = dict(rho_off_lMs=float(spearmanr(off, lMs).correlation))
    if not MUT:
        P(f"\n[SLUGGS {foot}] N {len(names)}; rho(offset, log M*) {out['rho_off_lMs']:+.2f}")
        for k, x in PROX.items():
            t = perm_test(off, x, ALLN); t["reading"] = reading(t); out[f"T2|{k}"] = t
            P(f"   T2 partial rho(offset, {k:8s} | log M*) {t['rho']:+.3f}  p+ {t['p_pos']:.3f}  p- {t['p_neg']:.3f}  N {t['n']}  -> {t['reading']}")
        for lab, y in (("D_in", Din), ("D_out-D_in", Dout - Din), ("D_out", Dout)):
            t = perm_test(y, PROX["H_score"], POP); t["reading"] = reading(t); out[f"T4|{lab}"] = t
            P(f"   T4 partial rho({lab:10s}, H_score | log M*) {t['rho']:+.3f}  p+ {t['p_pos']:.3f}  p- {t['p_neg']:.3f}  N {t['n']}")
        for k in ("env", "central", "E_morph", "LX_LB"):
            for lab, y in (("D_in", Din), ("D_out-D_in", Dout - Din)):
                t = perm_test(y, PROX[k], POP, 5000); out[f"T4|{lab}|{k}"] = t
            P(f"      by proxy {k:8s}: rho(D_in) {out[f'T4|D_in|{k}']['rho']:+.3f} (p+ {out[f'T4|D_in|{k}']['p_pos']:.3f}), "
              f"rho(D_out-D_in) {out[f'T4|D_out-D_in|{k}']['rho']:+.3f} (p+ {out[f'T4|D_out-D_in|{k}']['p_pos']:.3f}, p- {out[f'T4|D_out-D_in|{k}']['p_neg']:.3f})")
        P(f"   medians over the 16: D_in {np.median(Din[POP]):+.3f} dex, D_out {np.median(Dout[POP]):+.3f} dex")
        out["per_galaxy"] = {n: dict(off=float(off[i]), D_in=float(Din[i]), D_out=float(Dout[i]), lMs=float(lMs[i]),
                                     **{k: float(PROX[k][i]) for k in PROX}) for i, n in enumerate(names)}
    SL[foot] = out
RES["sluggs"] = SL

# ================================================================== MUTATE
if MUT:
    P("\n== MUTATE ==")
    mz = {}
    for foot in FOOTS:
        rows = ROWS[foot]
        T = np.array([r["T"] for r in rows]); lm = np.array([r["lMb"] for r in rows])
        zs = []
        for t in range(200):
            Ts = T.copy()
            for lo, hi in zip(EDG[:-1], EDG[1:]):
                m = np.nonzero((lm >= lo) & (lm < hi))[0]
                Ts[m] = T[rng.permutation(m)]
            zs.append(matched(rows, "d_out", Ts <= 3)["Z"])
        mz[foot] = float(np.nanmean(zs))
    check("MU3 SPARC T shuffled inside M_b bins (200x): |mean Z| early-late Delta_out < 0.5", all(abs(v) < 0.5 for v in mz.values()), f"{mz}")
    RES["MU3"] = mz
    m4 = {}
    for foot in FOOTS:
        off = np.array([AUD[f"nu_mono|{foot}"][n]["off"] for n in names])
        rs = []
        for t in range(2000):
            sh = {}
            for k in ("env", "central", "E_morph", "LX_LB"):
                x = PROX[k].copy()
                for b in blocks(np.arange(len(names))):
                    x[b] = PROX[k][rng.permutation(b)]
                sh[k] = x
            rs.append(partial(off, hscore(sh), lMs))
        m4[foot] = float(np.mean(rs))
    check("MU4 SLUGGS proxies shuffled inside mass blocks (2000x): |mean composite rho| < 0.1", all(abs(v) < 0.1 for v in m4.values()), f"{m4}")
    RES["MU4"] = m4

RES["checks"] = CHK
nf = sum(1 for v in CHK.values() if not v["ok"])
P(f"\n{len(CHK) - nf}/{len(CHK)} checks pass")
json.dump(RES, open(os.path.join(HERE, f"cfg534_sparc_sluggs_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg534_sparc_sluggs{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
