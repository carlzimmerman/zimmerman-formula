#!/usr/bin/env python3
"""EUC13 (POPULATION SOURCE GATE).  Frozen criteria: FROZEN_CRITERIA.md (commit 486c59d12a).

Population gate EUC13-P on ECLIPSE sample P: b_med and f25 of law S with source redshifts drawn from
  M1 AGEL DR2, M2 DESI SLF IV (published samples, EUC10 Part B recipe, honest intervals),
  M3 a forward model (arc VIS magnitude -> COSMOS2020 n(z|m) x the law's lensing cross-section), validated first.
Not EUC1-F, not EUC5-F.  EUC1's machinery is imported, not rewritten.

  python3 -I euc13.py --data-dir <ECLIPSE dir> --lit <EUC10 lit dir>
  EUC13_MUTATE=newton python3 -I euc13.py --data-dir <dir> --lit <dir>      (must exit 1)

kappa = 1/2 FITTED.  Footings never pooled.  One-sided: no outcome favours the framework.
"""
import argparse, csv, glob, json, math, os, re, sys, time
import numpy as np
from scipy.stats import kstest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
EUC10 = os.path.join(HERE, "..", "EUC10_published_source_redshifts")

MUT = (os.environ.get("EUC13_MUTATE", "") or "").strip()
FOOT = dict(E.FOOT)
if MUT == "newton":
    FOOT = {k: 1.0e-30 for k in FOOT}
SEED = 20261112
HOLD, FAIL = 0.15, 0.25
F_BROKEN, F_HOLDS = 0.25, 0.10
GUARD, ZMAX = 0.2, 6.0
XSTEP, NX = 0.05, 33                     # b table in x = log10(Sigma_cr(z_s)/Sigma_cr(inf)), 0 .. 1.60
NERR, NREP, NDRAW = 40, 400, 200
ZC = np.round(np.arange(0.025, 6.0, 0.05), 3)          # COSMOS z bin centres
ICEN = np.round(np.arange(16.05, 28.0, 0.1), 2)         # COSMOS i bin centres
MU_SET = ("mu3", "mu10", "mumarg")
W_SET = ("full", "sis")
FGRID = np.logspace(math.log10(0.2), math.log10(5.0), 31)
BANDS = {"theta_E < 1.0": {"canonical": (-0.19, 0.22), "alt": (-0.19, 0.21)},
         "1.0 - 1.3": {"canonical": (-0.05, 0.30), "alt": (-0.06, 0.34)},
         "theta_E >= 1.3": {"canonical": (0.03, 0.32), "alt": (0.03, 0.31)}}
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ COSMOS n(z | m)
def load_counts():
    H = []
    with open(os.path.join(HERE, "euc13_cosmos2020_counts.csv")) as f:
        r = csv.reader(f); next(r)
        for row in r: H.append([float(v) for v in row[1:]])
    return np.array(H)                                # (120 i bins, 120 z bins)

class Field:
    def __init__(self, H):
        self.H = H; self.widened = 0
        self.cum = np.vstack([np.zeros(H.shape[1]), np.cumsum(H, axis=0)])
    def window(self, m, half=0.25):
        """unnormalised counts of galaxies with |i_centre - m| <= half (m clamped to 27.5)"""
        m = min(max(m, 16.3), 27.5)
        lo = int(np.searchsorted(ICEN, m - half - 1e-9)); hi = int(np.searchsorted(ICEN, m + half + 1e-9, side="right"))
        return self.cum[hi] - self.cum[lo]
    def n_fixed(self, m):
        half = 0.25; c = self.window(m, half)
        while c.sum() < 20 and half < 2.0:
            half += 0.25; c = self.window(m, half)
        if half > 0.25: self.widened += 1
        return c / max(c.sum(), 1e-300)
    def n_marg(self, m):
        lmu = np.linspace(math.log(2.0), math.log(30.0), 57); dl = lmu[1] - lmu[0]
        mu = np.exp(lmu); wt = mu ** -2.0 * dl                 # p(mu) dmu ~ mu^-3 dmu = mu^-2 dln mu
        c = np.zeros(len(ZC)); clamp = 0.0
        for u, w in zip(mu, wt):
            mm = m + 2.5 * math.log10(u)
            cc = self.window(mm) * w; c += cc
            if mm > 27.5: clamp += cc.sum()
        return c / max(c.sum(), 1e-300), clamp / max(c.sum(), 1e-300)

def n_table(field, marcs, setting):
    out = np.zeros((len(marcs), len(ZC))); clamp = np.zeros(len(marcs))
    for j, m in enumerate(marcs):
        if setting == "mumarg":
            out[j], clamp[j] = field.n_marg(m)
        else:
            mu = 3.0 if setting == "mu3" else 10.0
            mi = m + 2.5 * math.log10(mu); out[j] = field.n_fixed(mi); clamp[j] = float(mi > 27.5)
    return out, clamp

# ------------------------------------------------------------------ lensing weights
def w_sis(zl, cosmo=E.EUCLID):
    dl = cosmo.DC(zl)[:, None]; ds = cosmo.DC(ZC)[None, :]
    w = np.clip((ds - dl) / ds, 0.0, None) ** 2
    return np.where(ZC[None, :] >= zl[:, None] + GUARD, w, 0.0)

def sigbar(sample, B, a0):
    """mean enclosed surface density at R = f R_E for the 31 factors f (N x 31)"""
    out = np.zeros((len(sample), len(FGRID)))
    tE0 = E.arr(sample, "tE")
    for j, f in enumerate(FGRID):
        eng, z, RE, _, _, _ = E.build(sample, tE=tE0 * f)
        out[:, j] = eng.M2D(B, a0, "S") / (math.pi * RE ** 2)
    return out

def w_full(sample, zl, B, a0):
    sb = sigbar(sample, B, a0)
    sc = E.EUCLID.sigcr(zl[:, None], np.maximum(ZC[None, :], zl[:, None] + 1e-3))
    tE0 = E.arr(sample, "tE"); w = np.zeros((len(sample), len(ZC))); capped = np.zeros((len(sample), len(ZC)), bool)
    lf = np.log(FGRID)
    for i in range(len(sample)):
        ls = np.log(sb[i])[::-1]                     # increasing
        x = np.log(sc[i])
        f = np.exp(np.interp(x, ls, lf[::-1]))      # interp clamps at the ends = cap
        capped[i] = (x > ls[-1]) | (x < ls[0])
        w[i] = (f * tE0[i]) ** 2
    ok = ZC[None, :] >= zl[:, None] + GUARD
    return np.where(ok, w, 0.0), capped & ok

# ------------------------------------------------------------------ b tables
class Btab:
    """per realisation: b on x = 0 .. 1.60 per footing; direct solve beyond."""
    def __init__(self, sample, z, lm, tE, te):
        self.sample, self.z, self.lm, self.tE, self.te = sample, z, lm, tE, te
        eng, _, RE, _, _, _ = E.build(sample, z=z, lm=lm, tE=tE, te=te)
        self.RE = RE; self.Minf = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF)
        self.tab = {}
        for nm, a0 in FOOT.items():
            T = np.zeros((len(sample), NX))
            for j in range(NX):
                T[:, j] = eng.solve_b(self.Minf * 10.0 ** (j * XSTEP), a0, "S")
            self.tab[nm] = T
        self.ndirect = 0
    def b(self, idx, zs, nm):
        """b for lenses idx (indices into the sample) at source redshifts zs"""
        z = self.z[idx]
        x = np.log10(E.EUCLID.sigcr(z, zs) / E.EUCLID.sigcr(z, E.ZS_INF)); x = np.maximum(x, 0.0)
        pos = x / XSTEP; i0 = np.clip(np.floor(pos).astype(int), 0, NX - 2); fr = pos - i0
        T = self.tab[nm]
        b = T[idx, i0] * (1 - fr) + T[idx, i0 + 1] * fr
        far = x > (NX - 1) * XSTEP
        if far.any():
            self.ndirect += int(far.sum())
            sel = [self.sample[i] for i in idx[far]]
            eng, zz, RE, _, _, _ = E.build(sel, z=z[far], lm=self.lm[idx[far]], tE=self.tE[idx[far]], te=self.te[idx[far]])
            b[far] = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(zz, zs[far]), FOOT[nm], "S")
        return b

def err_realisations(Pm, n):
    """EUC1 robustness run 6, exactly: catalogued errors of P, seed SEED + 1"""
    lm = E.arr(Pm, "lm"); rmc = np.random.default_rng(SEED + 1)
    def pm(v, lo, up, w):
        return v + w * np.where(w > 0, np.where(up > 0, up, 0.0), np.where(lo > 0, lo, 0.0))
    z0 = E.arr(Pm, "z"); szu = np.clip(E.arr(Pm, "zhi") - z0, 0, None) / 1.04; szl = np.clip(z0 - E.arr(Pm, "zlo"), 0, None) / 1.04
    tE0, te0 = E.arr(Pm, "tE"), E.arr(Pm, "te")
    def half(lo, up):
        s = 0.5 * (up - lo); return np.where((lo > 0) & (up > 0) & (s > 0), s, 0.0)
    sE = half(E.arr(Pm, "tE_lo"), E.arr(Pm, "tE_up")); se = half(E.arr(Pm, "te_lo"), E.arr(Pm, "te_up"))
    out = []
    for _ in range(n):
        w = rmc.standard_normal(len(Pm)); zz = np.clip(z0 + w * np.where(w > 0, szu, szl), 0.02, 3.0)
        lmm = pm(lm, E.arr(Pm, "lm_lo"), E.arr(Pm, "lm_up"), rmc.standard_normal(len(Pm))) + 2.0 * np.log10(E.EUCLID.DL(zz) / E.EUCLID.DL(z0))
        tEm = np.clip(tE0 + sE * rmc.standard_normal(len(Pm)), 0.05 * tE0, None)
        tem = np.clip(te0 + se * rmc.standard_normal(len(Pm)), 0.05 * te0, None)
        out.append((zz, lmm, tEm, tem))
    return out

# ------------------------------------------------------------------ helpers
def cdf_rows(p):
    c = np.cumsum(p, axis=1); return c / np.maximum(c[:, -1:], 1e-300)

def draw_rows(p, rng):
    c = cdf_rows(p); u = rng.random(len(p))
    return ZC[np.minimum((c < u[:, None]).sum(axis=1), len(ZC) - 1)]

def mix_cdf_fn(p):
    """mixture of per-system bin distributions, uniform inside 0.05 bins"""
    pm_ = p / np.maximum(p.sum(axis=1, keepdims=True), 1e-300)
    m = pm_.mean(axis=0); edges = np.concatenate([[0.0], ZC + 0.025])
    cm = np.concatenate([[0.0], np.cumsum(m)])
    return lambda x: np.interp(x, edges, cm), edges, cm

def row_cdf_at(p, z):
    pm_ = p / max(p.sum(), 1e-300); edges = np.concatenate([[0.0], ZC + 0.025])
    return float(np.interp(z, edges, np.concatenate([[0.0], np.cumsum(pm_)])))

def interval(point, reps):
    reps = np.asarray(reps, float); q = np.percentile(reps, [2.5, 50.0, 97.5])
    return dict(point=float(point), lo=float(point + q[0] - q[1]), hi=float(point + q[2] - q[1]),
                raw_lo=float(q[0]), raw_med=float(q[1]), raw_hi=float(q[2]))

def gate_word(ivs):
    if all(iv["hi"] <= HOLD for iv in ivs): return "POPULATION GATE HOLDS"
    if all(iv["lo"] >= FAIL for iv in ivs): return "POPULATION GATE FAILS"
    return "NO VERDICT"

def f25_word(ivs):
    if all(iv["lo"] >= F_BROKEN for iv in ivs): return "CEILING BROKEN"
    if all(iv["hi"] <= F_HOLDS for iv in ivs): return "CEILING HOLDS"
    return "NO VERDICT"

def band_place(iv, band):
    if iv["lo"] > band[1]: return "above"
    if iv["hi"] < band[0]: return "below"
    return "inside"

def load_slacs():
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}
    L = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        r = l.split("\t")
        if len(r) < len(hdr): continue
        d = dict(zl=E.fl(r[col["zlens"]]), zs=E.fl(r[col["zsrc"]]), RE=E.fl(r[col["RE"]]), lME=E.fl(r[col["Mass"]]),
                 Fs=E.fl(r[col["Fs"]]), Fc=E.fl(r[col["Fc"]]), ReV=E.fl(r[col["Re(V)"]]))
        if all(np.isfinite([d["zl"], d["zs"], d["RE"], d["lME"], d["Fs"], d["Fc"]])) and d["RE"] > 0: L.append(d)
    return L

# ------------------------------------------------------------------ SLF IV with magnitudes (V1)
def num(s):
    m = re.search(r"-?\d+\.\d+|-?\d+", s or ""); return float(m.group(0)) if m else None
def clean(s):
    return (s.replace("\\phantom{$-$}", "").replace("$-$", "-").replace("$+$", "+").replace("−", "-")
             .replace("~", " ").replace("\\,", " ").strip())
def slf4_mags(lit):
    """EUC10's SLF IV parse (same rows), plus the primary source's DESI r, i, z (fields 7-9)"""
    p = os.path.join(lit, "x", "2509.18078", "main.tex"); out, cur = [], None
    for ln, line in enumerate(open(p, encoding="utf-8").read().splitlines(), 1):
        if line.strip().startswith("%"): continue
        f = [clean(c) for c in line.split("&")]
        if len(f) < 9: continue
        if f[0].startswith("DESI"):
            cur = dict(name=f[0].replace(" ", ""), lens=None, src=None); out.append(cur)
        if cur is None: continue
        role = f[1]; z = num(f[4].split("\\pm")[0]); q = num(f[5])
        if z is None or q is None: continue
        if role in ("Lens", "Lens 1") and cur["lens"] is None: cur["lens"] = (z, q)
        elif role in ("Source", "Source A") and cur["src"] is None:
            mags = [num(f[k]) if len(f) > k and f[k].strip() not in ("-", "") else None for k in (7, 8, 9)]
            cur["src"] = (z, q, mags)
    res = []
    for c in out:
        if c["lens"] and c["src"] and c["lens"][1] <= 2 and c["src"][1] <= 2:
            r_, i_, z_ = c["src"][2]
            if i_ is not None: m = i_
            else:
                fl = [10 ** (-0.4 * v) for v in (r_, z_) if v is not None]
                m = -2.5 * math.log10(np.mean(fl)) if fl else None
            res.append(dict(name=c["name"], z_l=c["lens"][0], z_s=c["src"][0], m=m))
    return res

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--lit", required=True)
    args = ap.parse_args()
    t0 = time.time(); tag = "euc13" + ("_MUTATE_" + MUT if MUT else "")
    RES = dict(lane="EUC13", criteria_commit="486c59d12a", mutate=MUT, footings=FOOT)
    P("EUC13 (POPULATION SOURCE GATE)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    P("footings (m/s^2): canonical %.4e, alt %.4e" % (FOOT["canonical"], FOOT["alt"]))
    P("\n[data]")
    rows, _ = E.load(args.data_dir)
    Pm, _ = E.select(rows, ("A",)); N = len(Pm)
    byid = {r["id"]: r for r in rows}
    obj = {r["Unique_Identifier"]: r for r in csv.DictReader(open(os.path.join(args.data_dir, "ECLIPSE_object_catalogue.csv"), encoding="utf-8"))}
    key = {r["unique_identifier"]: r for r in csv.DictReader(open(os.path.join(args.data_dir, "eclipse_dr1_catalogue_key_v20261103.csv"), encoding="utf-8"))}
    mer = {}
    for fn in sorted(glob.glob(os.path.join(args.data_dir, "nisp_tables", "mer_*.csv"))):
        for r in csv.DictReader(open(fn)): mer[r["object_id"]] = r
    def m_arc_of(lid):
        o = obj.get(lid); k = key.get(lid)
        if o is None or k is None: return None
        ratio = E.fl(k["eclipse_vis_ratio_ls_l"]); mr = mer.get(o["MER_object_id"].strip())
        if ratio is None or not ratio > 0 or mr is None: return None
        fL = E.fl(mr["flux_detection_total"])
        if not fL > 0: return None
        return 23.9 - 2.5 * math.log10(ratio * fL)
    marc = np.array([m_arc_of(r["id"]) if m_arc_of(r["id"]) is not None else np.nan for r in Pm])
    has = np.isfinite(marc)
    z0 = E.arr(Pm, "z"); tE0 = E.arr(Pm, "tE")
    P("  P = %d; with an arc VIS magnitude %d; without %d (neighbour arcs)" % (N, has.sum(), (~has).sum()))
    if has.any():
        P("  arc VIS magnitude on P: median %.2f, 16-84 %% %.2f - %.2f" % (np.median(marc[has]), *np.percentile(marc[has], [16, 84])))
    ia = np.where(has)[0]
    dist = (z0[~has, None] - z0[None, ia]) ** 2 / 0.01 + (np.log10(tE0[~has, None]) - np.log10(tE0[None, ia])) ** 2 / 0.01
    NBR = ia[np.argsort(dist, axis=1)[:, :20]]                      # (n_missing, 20) indices into P
    miss = np.where(~has)[0]
    RES["inputs"] = dict(P=N, with_arc=int(has.sum()))

    H = load_counts(); FLD = Field(H)
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-4s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))

    SB = list(csv.DictReader(open(os.path.join(EUC10, "euc10_partB_samples.csv"), newline="")))
    PUB = {"M1": [r for r in SB if r["sample"] == "AGEL"], "M2": [r for r in SB if r["sample"] == "SLF4_MUSE"]}
    rng0 = np.random.default_rng(SEED)

    # -------------------------------------------------------------- known answers
    P("\n[known answers and instrument checks]")
    engP, zP, REP, _, _, _ = E.build(Pm)
    if not MUT:
        SL = load_slacs()
        zl = np.array([d["zl"] for d in SL]); zs = np.array([d["zs"] for d in SL])
        REs = np.array([d["RE"] for d in SL]) * E.KPC
        Res = np.array([d["ReV"] for d in SL]) * E.ARCSEC * E.AUGER.DA(zl)
        Ms = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(REs, Res, 4.0) * E.MSUN
        engS = E.Engine(REs, Res, np.full(len(SL), 4.0), Ms)
        k1 = [float(np.median(engS.solve_b(math.pi * REs ** 2 * E.AUGER.sigcr(zl, zs), FOOT[nm], "S"))) for nm in ("canonical", "alt")]
        ck("KA1", "SLACS at true z_s: +0.082 / +0.070 to 0.003", "%+.4f / %+.4f" % tuple(k1), abs(k1[0] - 0.082) <= 0.003 and abs(k1[1] - 0.070) <= 0.003)
        k2 = [float(np.median(E.run_b(engP, zP, REP, E.ZS_INF, FOOT[nm], "S"))) for nm in ("canonical", "alt")]
        ck("KA2", "EUC1 source-free b_med on P: -0.019 / -0.044 to 0.001, N = 3192", "N = %d, %+.4f / %+.4f" % (N, *k2),
           N == 3192 and abs(k2[0] + 0.019) <= 0.001 and abs(k2[1] + 0.044) <= 0.001)
        Hz = H[(ICEN > 23.5) & (ICEN < 24.5)].sum(axis=0); cz = np.cumsum(Hz) / Hz.sum()
        k6 = float(np.interp(0.5, cz, ZC))
        ck("KA6", "COSMOS2020 median lpzBEST at 23.5 < i < 24.5 in [0.6, 1.6] (N = %d galaxies; grid total %d)" % (Hz.sum(), H.sum()),
           "%.3f" % k6, 0.6 <= k6 <= 1.6)

    # -------------------------------------------------------------- b tables
    P("\n[b tables: catalogued values and %d error realisations]" % (0 if MUT else NERR))
    tb = time.time()
    BT0 = Btab(Pm, z0, E.arr(Pm, "lm"), tE0, E.arr(Pm, "te"))
    ERR = [] if MUT else [Btab(Pm, *e) for e in err_realisations(Pm, NERR)]
    P("  built in %.0f s" % (time.time() - tb))
    if not MUT:
        r5 = np.random.default_rng(SEED + 5); worst = {}
        for nm, a0 in FOOT.items():
            idx = r5.integers(0, N, 300); zs = z0[idx] + GUARD + r5.random(300) * (5.0 - z0[idx] - GUARD)
            bt = BT0.b(idx, zs, nm)
            eng, zz, RE, _, _, _ = E.build([Pm[i] for i in idx])
            bd = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(zz, zs), a0, "S")
            worst[nm] = float(np.max(np.abs(bt - bd)))
        ck("KA5", "tabulated b vs direct solves, 300 random (lens, z_s) per footing: max |db| <= 0.003",
           "%.1e / %.1e" % (worst["canonical"], worst["alt"]), max(worst.values()) <= 0.003)

    # -------------------------------------------------------------- M1/M2 draws (EUC10 recipe)
    def pub_draw(rr, zl_use, rng, idxP):
        zl_s = np.array([float(r["z_l"]) for r in rr]); zs_s = np.array([float(r["z_s"]) for r in rr])
        nn = np.argsort(np.abs(zl_use[idxP][:, None] - zl_s[None, :]) / 0.1, axis=1)[:, :10]
        zs_d = np.full(len(idxP), np.nan)
        for t in range(20):
            need = ~np.isfinite(zs_d)
            if not need.any(): break
            pick = zs_s[nn[need, rng.integers(0, 10, need.sum())]]
            ok = pick > zl_use[idxP][need] + GUARD
            ii = np.where(need)[0][ok]; zs_d[ii] = pick[ok]
        return zs_d

    if not MUT:
        P("\n[KA3 / KA4: EUC10 Part B reproduced, direct solves (KA3) and EUC13's table path (KA4)]")
        target = {"M1": (0.238, 0.220), "M2": (0.298, 0.282)}
        for mem in ("M1", "M2"):
            rr = PUB[mem]; zl_s = np.array([float(r["z_l"]) for r in rr]); zs_s = np.array([float(r["z_s"]) for r in rr])
            rng = np.random.default_rng(SEED)
            nn = np.argsort(np.abs(zP[:, None] - zl_s[None, :]) / 0.1, axis=1)[:, :10]
            md = {nm: [] for nm in FOOT}; mt = {nm: [] for nm in FOOT}
            for it in range(200):
                zs_d = np.full(N, np.nan)
                for t in range(20):
                    need = ~np.isfinite(zs_d)
                    if not need.any(): break
                    pick = zs_s[nn[need, rng.integers(0, 10, need.sum())]]
                    ok = pick > zP[need] + 0.2
                    ii = np.where(need)[0][ok]; zs_d[ii] = pick[ok]
                keep = np.isfinite(zs_d)
                for nm, a0 in FOOT.items():
                    b = engP.solve_b(math.pi * REP ** 2 * E.EUCLID.sigcr(zP, np.where(keep, zs_d, zP + 5.0)), a0, "S")
                    md[nm].append(float(np.median(b[keep])))
                    mt[nm].append(float(np.median(BT0.b(np.where(keep)[0], zs_d[keep], nm))))
            a = [float(np.median(md[nm])) for nm in ("canonical", "alt")]; b = [float(np.median(mt[nm])) for nm in ("canonical", "alt")]
            ck("KA3" + mem, "EUC10 Part B %s: %+.3f / %+.3f to 0.002" % (mem, *target[mem]), "%+.4f / %+.4f" % tuple(a),
               abs(a[0] - target[mem][0]) <= 0.002 and abs(a[1] - target[mem][1]) <= 0.002)
            ck("KA4" + mem, "same draws through the b table: within 0.005 of KA3", "%+.4f / %+.4f" % tuple(b),
               abs(a[0] - b[0]) <= 0.005 and abs(a[1] - b[1]) <= 0.005)

    # -------------------------------------------------------------- M3 ingredients
    P("\n[M3 ingredients]")
    NT, CL = {}, {}
    for s in MU_SET:
        NT[s], CL[s] = n_table(FLD, np.where(has, marc, 25.0), s)
        P("  %-7s share of n(z) weight evaluated at the 27.5 clamp (arc lenses): %.3f" % (s, float(np.mean(CL[s][has]))))
    P("  magnitude windows widened for < 20 galaxies: %d" % FLD.widened)
    WS = w_sis(z0)

    def predictive(s, w, nb_choice=None):
        """per-lens predictive on ZC; missing-arc lenses use neighbour nb_choice (indices into P) or the first neighbour"""
        n = NT[s].copy()
        if len(miss):
            pick = NBR[:, 0] if nb_choice is None else nb_choice
            n[miss] = NT[s][pick]
        return n * w

    # -------------------------------------------------------------- validation (sis weight)
    P("\n[validation of M3 (sis weight), before any P number of M3]")
    VAL = {}
    lit = args.lit
    S4 = [r for r in slf4_mags(lit) if r["m"] is not None]
    zl4 = np.array([r["z_l"] for r in S4]); zs4 = np.array([r["z_s"] for r in S4]); m4 = np.array([r["m"] for r in S4])
    P("  V1 SLF IV systems with a source magnitude: %d (of %d parsed); observed median z_s %.3f" % (len(S4), len(slf4_mags(lit)), np.median(zs4)))
    # V2 lenses
    M = [m for m in csv.DictReader(open(os.path.join(EUC10, "euc10_matches.csv"), newline="")) if m["status"] == "USED"]
    known = [(m["eclipse_id"], float(m["z_s"])) for m in M]
    for lid, zs_ in (("EUCL-DR1-L012826", 1.1374), ("EUCL-DR1-L014688", 0.9926), ("EUCL-DR1-L006816", 0.4685)):
        if lid not in [k[0] for k in known]: known.append((lid, zs_))
    V2L = []
    for lid, zs_ in known:
        r = byid.get(lid); ma = m_arc_of(lid)
        if r is None or ma is None: continue
        zl_ = r["zspec"] if np.isfinite(r["zspec"]) and r["zspec"] > 0 else (r["z"] if r["z"] > 0 else None)
        if zl_ is None: continue
        V2L.append((lid, zl_, zs_, ma))
    P("  V2 known-source ECLIPSE lenses evaluable: %d of %d (%s)" % (len(V2L), len(known), ", ".join(v[0][-7:] for v in V2L)))
    surv_mu = []
    for s in MU_SET:
        n4, _ = n_table(FLD, m4, s); p4 = n4 * w_sis(zl4)
        F, edges, cm = mix_cdf_fn(p4)
        med = float(np.interp(0.5, cm, edges)); ksp = float(kstest(zs4, F).pvalue)
        v1 = abs(med - np.median(zs4)) <= 0.25 and ksp > 0.01
        if len(V2L) >= 5:
            n2, _ = n_table(FLD, np.array([v[3] for v in V2L]), s); p2 = n2 * w_sis(np.array([v[1] for v in V2L]))
            u = np.array([row_cdf_at(p2[k], V2L[k][2]) for k in range(len(V2L))])
            ksu = float(kstest(u, "uniform").pvalue); ext = int(np.sum(np.minimum(u, 1 - u) < 0.005))
            v2 = ksu > 0.01 and ext <= 1
        else:
            u, ksu, ext, v2 = np.array([]), float("nan"), 0, True
        VAL[s] = dict(V1_model_median=med, V1_obs_median=float(np.median(zs4)), V1_ks_p=ksp, V1_pass=bool(v1),
                      V2_N=len(V2L), V2_pit=[float(x) for x in u], V2_ks_p=ksu, V2_extreme=ext, V2_pass=bool(v2), survives=bool(v1 and v2))
        P("  %-7s V1: model median %.3f vs observed %.3f, KS p %.3g -> %s;  V2: PIT KS p %.3g, extreme %d -> %s;  setting %s"
          % (s, med, np.median(zs4), ksp, "pass" if v1 else "FAIL", ksu, ext, "pass" if v2 else "FAIL", "SURVIVES" if v1 and v2 else "DROPPED"))
        if v1 and v2: surv_mu.append(s)
    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc13_results.json"))); surv_mu = ref["M3_surviving_mu"]
    RES["validation"] = VAL; RES["M3_surviving_mu"] = surv_mu
    P("  M3 surviving magnification settings: %s" % (surv_mu if surv_mu else "NONE -> M3 DROPPED"))

    # -------------------------------------------------------------- M3 full weight, self-consistent
    WF, CAP, BSTAR, CONV = {}, {}, {}, {}
    def selfcons(nm, a0, s):
        b = BT0.b(np.arange(N), np.full(N, E.ZS_INF), nm); last = None
        for it in range(3):
            w, cap = w_full(Pm, z0, 10.0 ** b, a0)
            p = predictive(s, w); c = cdf_rows(p)
            # median of b under p: b at the predictive median z_s (b is monotone in z_s)
            zmed = ZC[np.minimum((c < 0.5).sum(axis=1), len(ZC) - 1)]
            bn = BT0.b(np.arange(N), zmed, nm); last = float(np.max(np.abs(bn - b))); b = bn
        w, cap = w_full(Pm, z0, 10.0 ** b, a0)
        return w, cap, b, last
    if surv_mu:
        sref = "mumarg" if "mumarg" in surv_mu else surv_mu[0]
        P("\n[M3 full weight: self-consistent boost per footing (3 iterations; n(z) of setting %s used for the boost)]" % sref)
        for nm, a0 in FOOT.items():
            WF[nm], CAP[nm], BSTAR[nm], CONV[nm] = selfcons(nm, a0, sref)
            pc = predictive(sref, WF[nm]); pc = pc / pc.sum(axis=1, keepdims=True)
            P("  %-9s median self-consistent b* %+.3f; largest change in the last iteration %.4f; predictive mass at capped theta_E %.3f"
              % (nm, np.median(BSTAR[nm]), CONV[nm], float(np.mean((pc * CAP[nm]).sum(axis=1)))))
        RES["selfconsistency"] = {nm: dict(b_star_med=float(np.median(BSTAR[nm])), last_change=CONV[nm]) for nm in FOOT}

    # -------------------------------------------------------------- members: point + replicates
    CLS = {"theta_E < 1.0": tE0 < 1.0, "1.0 - 1.3": (tE0 >= 1.0) & (tE0 < 1.3), "theta_E >= 1.3": tE0 >= 1.3}
    def summarise(name, bfun_point, bfun_rep):
        """bfun_point(rng) -> (idx, b dict, zs);  bfun_rep(r, rng) -> (idx, b dict)"""
        out = {}
        rng = np.random.default_rng(SEED)
        pts = {nm: dict(med=[], f25=[], cls={c: [] for c in CLS}) for nm in FOOT}; zsm = []
        for _ in range(NDRAW):
            idx, bb, zs = bfun_point(rng); zsm.append(float(np.median(zs)))
            for nm in FOOT:
                pts[nm]["med"].append(float(np.median(bb[nm]))); pts[nm]["f25"].append(float(np.mean(bb[nm] > E.B_STAR)))
                for c, m in CLS.items(): pts[nm]["cls"][c].append(float(np.median(bb[nm][m[idx]])))
        reps = {nm: dict(med=[], f25=[], cls={c: [] for c in CLS}) for nm in FOOT}
        if not MUT:
            rng = np.random.default_rng(SEED + 7)
            for r in range(NREP):
                idx, bb = bfun_rep(r, rng)
                for nm in FOOT:
                    reps[nm]["med"].append(float(np.median(bb[nm]))); reps[nm]["f25"].append(float(np.mean(bb[nm] > E.B_STAR)))
                    for c, m in CLS.items(): reps[nm]["cls"][c].append(float(np.median(bb[nm][m[idx]])))
        for nm in FOOT:
            o = dict(z_s_median=float(np.median(zsm)))
            for st in ("med", "f25"):
                pt = float(np.median(pts[nm][st]))
                o[st] = interval(pt, reps[nm][st]) if reps[nm][st] else dict(point=pt)
            o["cls"] = {c: (interval(float(np.median(pts[nm]["cls"][c])), reps[nm]["cls"][c]) if reps[nm]["cls"][c]
                            else dict(point=float(np.median(pts[nm]["cls"][c])))) for c in CLS}
            out[nm] = o
            if MUT:
                P("  %-12s %-9s b_med %+.3f  f25 %.3f  (median z_s %.2f)" % (name, nm, o["med"]["point"], o["f25"]["point"], o["z_s_median"]))
            else:
                P("  %-12s %-9s b_med %+.3f [%+.3f, %+.3f] (raw %+.3f..%+.3f)  f25 %.3f [%.3f, %.3f]  median z_s %.2f"
                  % (name, nm, o["med"]["point"], o["med"]["lo"], o["med"]["hi"], o["med"]["raw_lo"], o["med"]["raw_hi"],
                     o["f25"]["point"], o["f25"]["lo"], o["f25"]["hi"], o["z_s_median"]))
        return out

    ALL = np.arange(N)
    MEM = {}
    P("\n[members on P: point (catalogued values, %d draws) and recentred 95 %% interval (%d replicates)]" % (NDRAW, NREP))
    for mem in ("M1", "M2"):
        rr = PUB[mem]
        def bp(rng, rr=rr):
            zs = pub_draw(rr, z0, rng, ALL); k = np.isfinite(zs); idx = ALL[k]
            return idx, {nm: BT0.b(idx, zs[k], nm) for nm in FOOT}, zs[k]
        def brp(r, rng, rr=rr):
            bt = ERR[r % NERR]; idxP = rng.integers(0, N, N); rrb = [rr[j] for j in rng.integers(0, len(rr), len(rr))]
            zs = pub_draw(rrb, bt.z, rng, idxP); k = np.isfinite(zs); idx = idxP[k]
            return idx, {nm: bt.b(idx, zs[k], nm) for nm in FOOT}
        MEM[mem] = summarise(mem, bp, brp)

    for s in surv_mu:
        for wf in W_SET:
            name = "M3 %s %s" % (s, wf)
            def bp(rng, s=s, wf=wf):
                bb = {}; zs_keep = None
                nb = NBR[np.arange(len(miss)), rng.integers(0, 20, len(miss))] if len(miss) else None
                for nm in FOOT:
                    p = predictive(s, WF[nm] if wf == "full" else WS, nb)
                    sub = np.random.default_rng(rng.integers(1 << 62))
                    zs = draw_rows(p, sub); bb[nm] = BT0.b(ALL, zs, nm); zs_keep = zs
                return ALL, bb, zs_keep
            def brp(r, rng, s=s, wf=wf):
                bt = ERR[r % NERR]; idxP = rng.integers(0, N, N)
                nb = NBR[np.arange(len(miss)), rng.integers(0, 20, len(miss))] if len(miss) else None
                bb = {}
                for nm in FOOT:
                    p = predictive(s, WF[nm] if wf == "full" else WS, nb)[idxP]
                    p = np.where(ZC[None, :] >= bt.z[idxP][:, None] + GUARD, p, 0.0)       # truncation under the error draw
                    bad = p.sum(axis=1) <= 0
                    if bad.any(): p[bad] = np.where(ZC[None, :] >= bt.z[idxP][bad][:, None] + GUARD, 1.0, 0.0)
                    zs = draw_rows(p, rng); bb[nm] = bt.b(idxP, zs, nm)
                return idxP, bb
            MEM[name] = summarise(name, bp, brp)

    # -------------------------------------------------------------- B-fixed readings (bounding the approximation)
    if surv_mu and not MUT and "mumarg" in surv_mu:
        P("\n[M3 readings with the lens boost fixed (full form, mu marginal; not in the envelope)]")
        RB = {}
        for bfix in (0.0, 0.5):
            for nm, a0 in FOOT.items():
                w, _ = w_full(Pm, z0, np.full(N, 10.0 ** bfix), a0)
                rng = np.random.default_rng(SEED); meds = []
                for _ in range(50):
                    nb = NBR[np.arange(len(miss)), rng.integers(0, 20, len(miss))] if len(miss) else None
                    zs = draw_rows(predictive("mumarg", w, nb), rng); meds.append(float(np.median(BT0.b(ALL, zs, nm))))
                RB["b%.1f_%s" % (bfix, nm)] = float(np.median(meds))
                P("  boost fixed at b = %.1f  %-9s b_med %+.3f (self-consistent %+.3f)" % (bfix, nm, np.median(meds), MEM["M3 mumarg full"][nm]["med"]["point"]))
        RES["bfixed"] = RB

    RES["members"] = MEM
    if MUT:
        ref = json.load(open(os.path.join(HERE, "euc13_results.json")))
        up = all(MEM[k][nm]["med"]["point"] > ref["members"][k][nm]["med"]["point"] for k in MEM for nm in FOOT)
        P("\n[MUTATE %s] b_med rose in every member and footing: %s" % (MUT, "yes, as required; exit 1" if up else "NO"))
        for k in MEM:
            P("  %-16s %s" % (k, "  ".join("%s %+.3f -> %+.3f" % (nm, ref["members"][k][nm]["med"]["point"], MEM[k][nm]["med"]["point"]) for nm in FOOT)))
        RES["mutate_rose"] = bool(up)
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
        sys.exit(1 if up else 2)

    # -------------------------------------------------------------- gate
    P("\n[EUC13-P: per footing over surviving members; M3 = envelope over its surviving settings]")
    GATE = {}
    for nm in FOOT:
        ivs, fvs, rowsg = [], [], []
        for mem in ("M1", "M2"):
            ivs.append(MEM[mem][nm]["med"]); fvs.append(MEM[mem][nm]["f25"]); rowsg.append(mem)
        m3 = [k for k in MEM if k.startswith("M3")]
        if m3:
            env = dict(lo=min(MEM[k][nm]["med"]["lo"] for k in m3), hi=max(MEM[k][nm]["med"]["hi"] for k in m3))
            fenv = dict(lo=min(MEM[k][nm]["f25"]["lo"] for k in m3), hi=max(MEM[k][nm]["f25"]["hi"] for k in m3))
            ivs.append(env); fvs.append(fenv); rowsg.append("M3 envelope")
            P("  %-9s M3 envelope: b_med [%+.3f, %+.3f], f25 [%.3f, %.3f]" % (nm, env["lo"], env["hi"], fenv["lo"], fenv["hi"]))
        GATE[nm] = dict(members=rowsg, b_med=[dict(lo=v["lo"], hi=v["hi"]) for v in ivs], f25=[dict(lo=v["lo"], hi=v["hi"]) for v in fvs],
                        word=gate_word(ivs), f25_word=f25_word(fvs))
        P("  %-9s gate word: %s;  f25 statistic: %s" % (nm, GATE[nm]["word"], GATE[nm]["f25_word"]))
    RES["gate"] = GATE

    P("\n[readings: theta_E classes against EUC5's sealed bands (NOT EUC5-F)]")
    for c in CLS:
        for nm in FOOT:
            P("  %-15s %-9s band [%+.2f, %+.2f]: %s" % (c, nm, *BANDS[c][nm], "; ".join(
                "%s %+.3f [%+.3f, %+.3f] %s" % (k.replace(" full", "F").replace(" sis", "S"), MEM[k][nm]["cls"][c]["point"], MEM[k][nm]["cls"][c]["lo"],
                                                 MEM[k][nm]["cls"][c]["hi"], band_place(MEM[k][nm]["cls"][c], BANDS[c][nm])) for k in MEM)))
    P("  class sizes: %s" % ", ".join("%s %d" % (c, m.sum()) for c, m in CLS.items()))

    # -------------------------------------------------------------- outputs
    with open(os.path.join(HERE, "euc13_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f)
        cols = ["unique_identifier", "z_l", "theta_E", "arc_vis_mag"] + ["zs_med_M3_%s_%s_%s" % (s, wf, nm) for s in surv_mu for wf in W_SET for nm in FOOT]
        w.writerow(cols)
        meds = {}
        for s in surv_mu:
            for wf in W_SET:
                for nm in FOOT:
                    c = cdf_rows(predictive(s, WF[nm] if wf == "full" else WS)); meds[(s, wf, nm)] = ZC[np.minimum((c < 0.5).sum(axis=1), len(ZC) - 1)]
        for i, r in enumerate(Pm):
            w.writerow([r["id"], "%.3f" % z0[i], "%.4f" % tE0[i], "%.3f" % marc[i] if has[i] else ""] +
                       ["%.3f" % meds[(s, wf, nm)][i] for s in surv_mu for wf in W_SET for nm in FOOT])
    allok = all(v["ok"] for v in CK.values())
    RES["checks"] = CK; RES["checks_all_pass"] = allok
    verdict = "%s / %s" % (GATE["canonical"]["word"], GATE["alt"]["word"]) if allok else "NOT EVALUABLE / NOT EVALUABLE"
    RES["verdict"] = verdict
    P("\n[summary]")
    P("  checks: %s;  direct solves beyond the table: %d (catalogued) / %d (error realisations)" % ("all pass" if allok else "FAILED -> NOT EVALUABLE",
      BT0.ndirect, sum(b.ndirect for b in ERR)))
    P("  EUC13-P (canonical / alt): %s" % verdict)
    P("  f25 statistic (canonical / alt): %s / %s" % (GATE["canonical"]["f25_word"], GATE["alt"]["f25_word"]))
    P("  kappa = 1/2 FITTED. One-sided: no outcome favours the framework.  (%.0f s)" % (time.time() - t0))
    json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
