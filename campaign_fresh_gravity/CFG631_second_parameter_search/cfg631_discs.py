"""CFG631 discs: joint multi-property regression of the law's outer residual, SPARC + WALLABY, permutation max-T.
Criteria: FROZEN_CRITERIA.md (06ca28e0d). cfg537_wallaby.py executed unedited (head); its kernel `nu` replaced by the repaired
nu_mono (CFG4_common). MUTATE: CFG631_MUTATE=1 injects 0.20 dex across the 16-84 range of log Sigma_* in both samples.
Run: nice -n 10 python3 cfg631_discs.py ; CFG631_MUTATE=1 nice -n 10 python3 cfg631_discs.py
"""
import os, sys, io, json, math, contextlib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg631_common as K  # noqa: E402

sys.path.insert(0, K.LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4  # noqa: E402
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG631_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []
NPERM, SEED = 5000, 631
FOOTS = ("canonical", "alt")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


SCORE = ("fgas", "bul", "lSig", "T", "inc", "HF")
SADD = ("colour", "env")
WCORE = ("fgas", "lSig", "T", "inc")
WADD = ("W12",)
SHARED = ("fgas", "lSig", "T", "inc")

P("=" * 110)
P(f"CFG631 discs: what besides the law sets the outer residual?  {'*** MUTATE: +0.20 dex across the log Sigma_* range ***' if MUTATE else 'PRIMARY'}")
P("=" * 110)
ns = K.cfg537_head()
A0SI, CONV = ns["A0SI"], ns["CONV"]
SPp, WPp = K.sparc_props(ns), K.wallaby_props(ns)

# ---------------- C1: exponential kernel reproduces CFG584's WALLABY slope
P("\n--- controls")
dev = []
for f, ref in (("canonical", -0.072), ("alt", -0.069)):
    rows = ns["residual_rows"](ns["GALS"], A0SI[f])
    x = np.array([r["lMb"] for r in rows]); y = np.array([r["d_out"] for r in rows]); m = np.isfinite(y)
    s = np.linalg.lstsq(np.column_stack([np.ones(m.sum()), x[m] - 10]), y[m], rcond=None)[0][1]; dev.append((f, s, abs(s - ref)))
check(all(d[2] <= 0.002 for d in dev), "C1 exponential kernel reproduces CFG584's WALLABY slope: " + ", ".join(f"{f} {s:+.4f}" for f, s, _ in dev))
EXPO = {f: (np.array([r["d_out"] for r in ns["sparc_rows"](A0SI[f] * CONV)]), np.array([r["d_out"] for r in ns["residual_rows"](ns["GALS"], A0SI[f])])) for f in FOOTS}

# ---------------- residuals with the repaired nu_mono
ns["nu"] = C4.nu_mono
SR = {f: ns["sparc_rows"](A0SI[f] * CONV) for f in FOOTS}
WR = {f: ns["residual_rows"](ns["GALS"], A0SI[f]) for f in FOOTS}
assert [r["name"] for r in SR["canonical"]] == [p["name"] for p in SPp] and [r["name"] for r in WR["canonical"]] == [p["name"] for p in WPp]
kd = max(np.nanmax(np.abs(np.array([r["d_out"] for r in SR[f]]) - EXPO[f][0])) for f in FOOTS)
kw = max(np.nanmax(np.abs(np.array([r["d_out"] for r in WR[f]]) - EXPO[f][1])) for f in FOOTS)
P(f"  kernel swap (exponential -> repaired nu_mono): max |dDelta_out| SPARC {kd:.4f}, WALLABY {kw:.4f} dex")


def sample(props, rows, core, add):
    d = {f: np.array([r["d_out"] for r in rows[f]]) for f in FOOTS}
    ok = np.isfinite(d["canonical"]) & np.isfinite(d["alt"])
    for p in ("lMb",) + core:
        ok &= np.isfinite(np.array([q[p] for q in props], float))
    X = {p: np.array([q[p] for q in props], float)[ok] for p in ("lMb",) + core + add}
    return dict(D={f: d[f][ok] for f in FOOTS}, X=X, names=[q["name"] for q, o in zip(props, ok) if o], core=core, add=add)


S = sample(SPp, SR, SCORE, SADD)
W = sample(WPp, WR, WCORE, WADD)
for nm, s in (("SPARC", S), ("WALLABY", W)):
    s["span"] = {p: (1.0 if set(np.unique(v[np.isfinite(v)])) <= {0.0, 1.0} else float(np.nanpercentile(v, 84) - np.nanpercentile(v, 16))) for p, v in s["X"].items()}
    lm = s["X"]["lMb"]; s["q"] = np.digitize(lm, np.quantile(lm, [0.2, 0.4, 0.6, 0.8]))
if MUTATE:
    for s in (S, W):
        v = s["X"]["lSig"]; inj = 0.20 * (v - np.median(v)) / s["span"]["lSig"]
        for f in FOOTS:
            s["D"][f] = s["D"][f] + inj
        s["inj_beta"] = 0.20 / s["span"]["lSig"]
check(all(abs(np.median(s["D"][f])) < 0.1 for s in (S, W) for f in FOOTS),
      "C2 |median Delta_out| < 0.1 dex: " + ", ".join(f"{n} {f} {np.median(s['D'][f]):+.3f}" for n, s in (("SPARC", S), ("WALLABY", W)) for f in FOOTS))
P(f"  N: SPARC {len(S['names'])} (colour {np.isfinite(S['X']['colour']).sum()}, env {np.isfinite(S['X']['env']).sum()}); "
  f"WALLABY {len(W['names'])} (W1-W2 {np.isfinite(W['X']['W12']).sum()})")


# ---------------- models (vectorised OLS over many Y columns)
def models(s):
    """list of (model_name, row_index, design, tested property list)"""
    out = []
    base = np.column_stack([np.ones(len(s["names"])), s["X"]["lMb"] - 10] + [s["X"][p] for p in s["core"]])
    out.append(("core", np.arange(len(s["names"])), base, list(s["core"])))
    for a in s["add"]:
        idx = np.where(np.isfinite(s["X"][a]))[0]
        out.append((a, idx, np.column_stack([base[idx], s["X"][a][idx]]), list(s["core"]) + [a]))
    return out


def ols_t(Xd, Y):
    """Y: n x m. returns beta (p x m), t (p x m), rss (m)"""
    XtXi = np.linalg.inv(Xd.T @ Xd)
    B = XtXi @ Xd.T @ Y
    Rr = Y - Xd @ B
    rss = (Rr ** 2).sum(0); dof = Xd.shape[0] - Xd.shape[1]
    se = np.sqrt(np.outer(np.diag(XtXi), rss / dof))
    return B, B / se, rss, se


def tstats(s, Yf):
    """Yf: dict foot -> (n x m). Returns dict (prop, foot) -> t (m,), beta, se; plus omnibus F per foot."""
    res = {}
    for mname, idx, Xd, props in models(s):
        for f in FOOTS:
            B, T, rss, se = ols_t(Xd, Yf[f][idx])
            if mname == "core":
                Xm = Xd[:, :2]; _, _, rss0, _ = ols_t(Xm, Yf[f][idx])
                q = len(props); dof = Xd.shape[0] - Xd.shape[1]
                res[("OMNI", f)] = dict(F=((rss0 - rss) / q) / (rss / dof))
                res[("lMb", f)] = dict(t=T[1], beta=B[1], se=se[1])
                tested = props
            else:
                tested = [mname]
            for p in tested:
                j = 2 + props.index(p)
                res[(p, f)] = dict(t=T[j], beta=B[j], se=se[j])
    return res


def perm_matrix(s, n, rng):
    """n permutations of row indices, shuffled within mass quintiles (n_gal x n)."""
    N = len(s["names"]); Pm = np.empty((N, n), int)
    for k in range(n):
        idx = np.arange(N)
        for q in range(5):
            m = np.where(s["q"] == q)[0]; idx[m] = m[rng.permutation(len(m))]
        Pm[:, k] = idx
    return Pm


def run_family(DS, DW, nperm, seed, keep=False):
    """observed t's + permutation max-T for the whole family. DS/DW: dict foot -> residual vector."""
    rng = np.random.default_rng(seed)
    obsS = tstats(S, {f: DS[f][:, None] for f in FOOTS}); obsW = tstats(W, {f: DW[f][:, None] for f in FOOTS})
    PS, PW = perm_matrix(S, nperm, rng), perm_matrix(W, nperm, rng)
    nulS = tstats(S, {f: DS[f][PS] for f in FOOTS}); nulW = tstats(W, {f: DW[f][PW] for f in FOOTS})
    fam = [("SPARC", p, f) for p in SCORE + SADD for f in FOOTS] + [("WALLABY", p, f) for p in WCORE + WADD for f in FOOTS]
    mx = np.max(np.abs(np.array([(nulS if smp == "SPARC" else nulW)[(p, f)]["t"] for smp, p, f in fam])), axis=0)
    return obsS, obsW, nulS, nulW, mx, fam


obsS, obsW, nulS, nulW, MX, FAM = run_family(S["D"], W["D"], NPERM, SEED)
OBS = {"SPARC": obsS, "WALLABY": obsW}; NUL = {"SPARC": nulS, "WALLABY": nulW}; SAMP = {"SPARC": S, "WALLABY": W}


def fwp(t):
    return float((np.sum(MX >= abs(t)) + 1) / (len(MX) + 1))


def one_sided(smp, p, f, sign):
    t0 = float(OBS[smp][(p, f)]["t"][0]); tn = NUL[smp][(p, f)]["t"]
    return float((np.sum(sign * tn >= sign * t0) + 1) / (len(tn) + 1))


P(f"\n--- results (OLS jointly with log M_b; coefficient in dex across the 16-84 range; family-wise p from {NPERM} max-T draws over {len(FAM)} t's)")
P(f"  max-T 95th percentile |t| = {np.percentile(MX, 95):.2f}")
TABLE = {}
for smp in ("SPARC", "WALLABY"):
    s = SAMP[smp]
    for p in ("lMb",) + s["core"] + s["add"]:
        row = []
        for f in FOOTS:
            o = OBS[smp][(p, f)]; sp = 0.5 if p == "lMb" else s["span"][p]       # mass: dex of residual per 0.5 dex of M_b
            b, se, t = float(o["beta"][0]), float(o["se"][0]), float(o["t"][0])
            ent = dict(beta=b, se=se, t=t, eff_dex=b * sp, eff_lo=(b - 1.96 * se) * sp, eff_hi=(b + 1.96 * se) * sp,
                       p_fw=(fwp(t) if p != "lMb" else None), p_two=float((np.sum(np.abs(NUL[smp][(p, f)]["t"]) >= abs(t)) + 1) / (NPERM + 1)))
            TABLE[f"{smp}|{p}|{f}"] = ent
            row.append(f"{ent['eff_dex']:+.3f} [{ent['eff_lo']:+.3f},{ent['eff_hi']:+.3f}] t {t:+.2f} p_fw {ent['p_fw'] if ent['p_fw'] is not None else float('nan'):.3f}")
        lab = "lMb (per 0.5 dex)" if p == "lMb" else p
        P(f"  {smp:7s} {lab:18s} can: {row[0]}   alt: {row[1]}")
    for f in FOOTS:
        F0 = float(OBS[smp][("OMNI", f)]["F"][0]); pF = float((np.sum(NUL[smp][("OMNI", f)]["F"] >= F0) + 1) / (NPERM + 1))
        TABLE[f"{smp}|OMNI|{f}"] = dict(F=F0, p=pF)
    P(f"  {smp:7s} omnibus F (all core terms beyond mass): can F {TABLE[smp + '|OMNI|canonical']['F']:.2f} p {TABLE[smp + '|OMNI|canonical']['p']:.3f}; "
      f"alt F {TABLE[smp + '|OMNI|alt']['F']:.2f} p {TABLE[smp + '|OMNI|alt']['p']:.3f}")

# ---------------- verdict logic (frozen)
P("\n--- discovery / confirmation (frozen rules)")
disc = {}
for smp, props in (("SPARC", SCORE + SADD), ("WALLABY", WCORE + WADD)):
    for p in props:
        e = [TABLE[f"{smp}|{p}|{f}"] for f in FOOTS]
        if all(x["p_fw"] < 0.05 for x in e) and np.sign(e[0]["t"]) == np.sign(e[1]["t"]):
            disc[(smp, p)] = int(np.sign(e[0]["t"]))
P(f"  DISCOVERED: {[f'{s}:{p} ({sg:+d})' for (s, p), sg in disc.items()] or 'none'}")
status = {}
for other in ("SPARC", "WALLABY"):
    carried = [(p, sg) for (smp, p), sg in disc.items() if smp != other and p in SHARED]
    if not carried:
        continue
    ps = sorted([(max(one_sided(other, p, f, sg) for f in FOOTS), p, sg) for p, sg in carried])
    k = len(ps)
    for i, (pv, p, sg) in enumerate(ps):
        ok = pv < 0.05 / (k - i)
        status[p] = "REPLICATED" if ok else "DISCOVERY ONLY"
        P(f"  confirm {p} in {other}: one-sided p (worse footing) {pv:.4f} vs Holm {0.05 / (k - i):.4f} -> {status[p]}")
        if not ok:
            for _, p2, _ in ps[i + 1:]:
                status[p2] = "DISCOVERY ONLY"
            break
for (smp, p), sg in disc.items():
    if p not in SHARED:
        status[p] = {"colour": "DISCOVERED; confirmation = KiDS age result", "W12": "DISCOVERED (WALLABY only)"}.get(p, "DISCOVERED, UNCONFIRMABLE ON DISK")
omni_ok = all(TABLE[f"{s}|OMNI|{f}"]["p"] >= 0.05 for s in ("SPARC", "WALLABY") for f in FOOTS)
if any(v == "REPLICATED" for v in status.values()):
    verdict = "SECOND PARAMETER FOUND"
elif disc:
    verdict = "DISCOVERY ONLY"
elif omni_ok:
    verdict = "NO SECOND PARAMETER DETECTED"
else:
    verdict = "INCONCLUSIVE"
P(f"\nVERDICT (discs): {verdict}   status: {status or '-'}")
agec = [TABLE[f"SPARC|colour|{f}"] for f in FOOTS]
P(f"  disc age reading (SPARC colour B-[3.6], redder -> more excess predicted): {agec[0]['eff_dex']:+.3f} / {agec[1]['eff_dex']:+.3f} dex across the range; "
  f"one-sided p {one_sided('SPARC', 'colour', 'canonical', +1):.3f} / {one_sided('SPARC', 'colour', 'alt', +1):.3f}")

if MUTATE:
    P("\n--- MUTATE reading")
    ok_lin = True
    base = json.load(open(os.path.join(K.HERE, "cfg631_discs_results.json")))["table"] if os.path.exists(os.path.join(K.HERE, "cfg631_discs_results.json")) else None
    if base:
        for smp in ("SPARC", "WALLABY"):
            for f in FOOTS:
                sh = TABLE[f"{smp}|lSig|{f}"]["beta"] - base[f"{smp}|lSig|{f}"]["beta"]
                ok_lin &= abs(sh - SAMP[smp]["inj_beta"]) < 1e-9
                P(f"  {smp} {f}: lSig coefficient shift {sh:+.6f} vs injected {SAMP[smp]['inj_beta']:+.6f}")
    check(ok_lin and base is not None, "MUTATE linearity: coefficient shift equals the injection (1e-9)")
    check(status.get("lSig") == "REPLICATED", f"MUTATE: injected log Sigma_* dependence REPLICATED (status {status.get('lSig', 'not discovered')})")

# ---------------- SPARC variant residual (g_bar < a0/3, CFG583 definition), reported only
P("\n--- variant (reported only): SPARC g_bar < a0/3 residual, same core model, classical t")
VAR = {}
for f in FOOTS:
    a0 = A0SI[f] * CONV; dv = []
    for g in ns["SAMP"]:
        if g["name"] not in S["names"]:
            continue
        gb = (g["Vg"] * np.abs(g["Vg"]) + 0.5 * g["Vd"] ** 2 + 0.7 * g["Vb"] ** 2) / g["R"]; go = g["V"] ** 2 / g["R"]
        ok = (gb > 0) & (go > 0); Dd = np.log10(go[ok]) - np.log10(C4.nu_mono(gb[ok] / a0) * gb[ok]); sel = gb[ok] < a0 / 3
        dv.append(float(np.mean(Dd[sel])) if sel.sum() >= 3 else np.nan)
    dv = np.array(dv); m = np.isfinite(dv)
    Xd = np.column_stack([np.ones(m.sum()), S["X"]["lMb"][m] - 10] + [S["X"][p][m] for p in SCORE])
    B, T, _, se = ols_t(Xd, dv[m][:, None])
    VAR[f] = {p: dict(eff_dex=float(B[2 + i, 0] * S["span"][p]), t=float(T[2 + i, 0])) for i, p in enumerate(SCORE)}
    VAR[f]["N"] = int(m.sum())
    P(f"  [{f}] N {m.sum()}  " + "  ".join(f"{p} {VAR[f][p]['eff_dex']:+.3f} (t {VAR[f][p]['t']:+.2f})" for p in SCORE))

# ---------------- C5 null calibration (primary only)
if not MUTATE:
    P("\n--- C5 null calibration: 200 shuffled datasets x 1000 inner max-T draws")
    rng = np.random.default_rng(6311); hits = 0
    for i in range(200):
        PS1, PW1 = perm_matrix(S, 1, rng)[:, 0], perm_matrix(W, 1, rng)[:, 0]
        oS, oW, _, _, mx, fam = run_family({f: S["D"][f][PS1] for f in FOOTS}, {f: W["D"][f][PW1] for f in FOOTS}, 1000, 7000 + i)
        tt = [abs(float((oS if smp == "SPARC" else oW)[(p, f)]["t"][0])) for smp, p, f in fam]
        hits += any(np.mean(mx >= t) < 0.05 for t in tt)
    check(abs(hits / 200 - 0.05) <= 0.035, f"C5 fraction of null datasets with any family-wise p < 0.05: {hits / 200:.3f} (0.05 +- 0.035)")

P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=verdict, status=status, discovered={f"{s}|{p}": sg for (s, p), sg in disc.items()}, table=TABLE, variant_a0third=VAR,
               maxT_95=float(np.percentile(MX, 95)), n=dict(SPARC=len(S["names"]), WALLABY=len(W["names"])), spans=dict(SPARC=S["span"], WALLABY=W["span"]),
               kernel_swap_max=dict(SPARC=float(kd), WALLABY=float(kw)), checks=CHECKS),
          open(os.path.join(K.HERE, f"cfg631_discs_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(K.HERE, f"cfg631_discs{TAG}.out"), "w").write("\n".join(OUT) + "\n")
