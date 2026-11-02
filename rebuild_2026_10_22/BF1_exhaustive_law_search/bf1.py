#!/usr/bin/env python3
"""BF1: exhaustive search for H(y, ell, f) on the a0 law. Modes: real, control, mutate, planted, known. See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, pickle, signal, sys
import numpy as np
from multiprocessing import Pool
from astropy.io import fits
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
MODE = sys.argv[1] if len(sys.argv) > 1 else "real"; NW = int(sys.argv[2]) if len(sys.argv) > 2 else 10; LIM = int(sys.argv[3]) if len(sys.argv) > 3 else 0
A0 = 9.360324825027975e-11; C = 299792458.0; G = 6.674e-11; MS = 1.989e30; PC = 3.0857e16; KMS2 = 1e6
CAP = int(os.environ.get("BF1_CAP", 150000)); LEVELS = (1, 2, 3) if os.environ.get("BF1_SUF") else (1, 2); XM, XR = (1e-6, 1e-6) if MODE == "mutate" else (0.05, 0.10); SF, SM = 1.05, 0.03
def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)
def sparc():
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"]; meta = {g["name"]: g for g in Q}
    names = sorted(meta); rows = {0: [], 1: []}; D = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod")
    for i, n in enumerate(names):
        if meta[n]["Q"] >= 3 or meta[n]["inc"] < 30: continue
        t = np.loadtxt(os.path.join(D, n + "_rotmod.dat"), comments="#"); t = np.atleast_2d(t)
        for r, v, e, vg, vd, vb, *_ in t:
            m = abs(vg) * vg + 0.5 * abs(vd) * vd + 0.7 * abs(vb) * vb; R = r * 1e3 * PC
            if r <= 0 or v <= 0 or m <= 0: continue
            rows[i % 2].append((m * KMS2 / R, v * v * KMS2 / R, R * A0 / C ** 2, min(1.0, max(0.0, abs(vg) * vg / m)), i))
    return {k: np.array(v) for k, v in rows.items()}
def xcop():
    D = os.path.join(REPO, "real_research", "data", "xcop"); out = []
    def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    for j, n in enumerate(sorted(x for x in os.listdir(D) if os.path.exists(os.path.join(D, x, f"{x}_mstar.fits")))):
        with fits.open(os.path.join(D, n, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(D, n, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (0.1, 0.2, 0.3, 0.5, 0.7):
            r = x * r5; mh = li(hm["RADIUS"], hm["M_FORW"], r); mg = li(ga["RADIUS"] * rg, ga["MGAS"], r); ms = li(st["RADIUS"], st[st.names[1]], r)
            if not np.all(np.isfinite([mh, mg, ms])): continue
            R = r * 1e3 * PC; f = 1 / R ** 2 * G * MS; out.append((f * (mg + ms), f * mh, R * A0 / C ** 2, mg / (mg + ms), j))
    return np.array(out)
S = sparc(); X = xcop()
XT = X[X[:, 4].astype(int) % 2 == 0]; XH = X[X[:, 4].astype(int) % 2 == 1]; ST = S[1]; SH = S[0]
rng = np.random.default_rng(20261102)
if MODE == "control":
    p = rng.permutation(len(XT)); XT = XT.copy(); XT[:, 2] = XT[p, 2]; XT[:, 3] = XT[p, 3]
sub = ST[rng.choice(len(ST), 240, replace=False)]
PL = None
if MODE == "planted":
    def H_pl(y, e, f): return (1 + f) * np.log1p(1 / y)
    for arr in (XT, sub, ST, XH, SH):
        y = arr[:, 0] / A0; arr[:, 1] = law(arr[:, 0], A0) * H_pl(y, arr[:, 2], arr[:, 3])
EV = np.vstack([XT, sub]); NX = len(XT)
def leaves(A): return {"y": A[:, 0] / A0, "ell": A[:, 2], "f": A[:, 3]}
U = {"sqrt": np.sqrt, "log1p": np.log1p, "inv1p": lambda x: 1 / (1 + x), "sq": lambda x: x * x}
B = {"+": np.add, "-": np.subtract, "*": np.multiply, "/": np.divide}
def tree_eval(s, A):
    L = leaves(A); e = {"sqrt": np.sqrt, "log1p": np.log1p, "inv1p": lambda x: 1 / (1 + x), "sq": lambda x: x * x, "pi": math.pi, "y": L["y"], "ell": L["ell"], "f": L["f"], "np": np}
    return eval(s, {"__builtins__": {}}, e) * np.ones(len(A))
def closure():
    L0 = [("y", 1), ("ell", 1), ("f", 1), ("1.0", 1), ("2.0", 1), ("0.5", 1), ("pi", 1)]
    vec = {s: tree_eval(s, EV) for s, _ in L0}; seen = {}; lev = []
    def add(s, n, v, out):
        if not np.all(np.isfinite(v)) or np.max(np.abs(v)) > 1e30: return
        k = np.round(v / (np.abs(v).max() + 1e-300), 9).tobytes() + np.float64(np.round(np.log(np.abs(v).max() + 1e-300), 6)).tobytes()
        if k in seen: return
        seen[k] = 1; out.append((s, n, v))
    L = []
    for s, n in L0: add(s, n, vec[s], L)
    prev = list(L); sets = [list(L)]
    for level in LEVELS:
        new = []
        pool_ = [t for st in sets for t in st]
        for s, n, v in prev:
            for u, fn in U.items(): add(f"{u}({s})", n + 1, fn(v), new)
        for s1, n1, v1 in prev:
            for s2, n2, v2 in pool_:
                for o, fn in B.items():
                    add(f"({s1}{o}{s2})", n1 + n2 + 1, fn(v1, v2), new)
                    if o in "-/": add(f"({s2}{o}{s1})", n1 + n2 + 1, fn(v2, v1), new)
            if len(new) > 4 * CAP: break
        new.sort(key=lambda t: (t[1], t[0])); sets.append(new); prev = new
    al = [t for st in sets for t in st]; al.sort(key=lambda t: (t[1], t[0])); return al[:CAP], len(al)
def score(gp, A, gh=None):
    return np.log10(A[:, 1] / gp)
_law = None
def stage1(Hmat, names):
    """Hmat n x points on EV. Returns survivors of gates 1 and sub-sample prefilter."""
    gb = EV[:, 0]; gh = EV[:, 1]; res = []
    ok = np.all(np.isfinite(Hmat), axis=1) & np.all(Hmat > 0, axis=1)
    if not ok.any(): return res
    H = Hmat[ok]; idx = np.nonzero(ok)[0]
    for w in (1, 2, 3):
        Hx = H[:, :NX]; g = gb[:NX]
        p = law(g, A0 * Hx) if w == 1 else law(g * Hx, A0) if w == 2 else law(g, A0) * Hx
        d = np.log10(gh[:NX] / p); m = d.mean(axis=1); rm = np.sqrt((d * d).mean(axis=1)); keep = (np.abs(m) <= XM) & (rm <= XR)
        if not keep.any(): continue
        Hs = H[keep][:, NX:]; g = gb[NX:]; p = law(g, A0 * Hs) if w == 1 else law(g * Hs, A0) if w == 2 else law(g, A0) * Hs
        ds = np.log10(gh[NX:] / p); r = np.sqrt((ds * ds).mean(axis=1)); md = np.median(ds, axis=1); kk = (r <= 1.3 * RL) & (np.abs(md) <= 2 * SM)
        for i in np.nonzero(keep)[0][kk]: res.append((int(idx[i]), w))
    return res
g0 = law(sub[:, 0], A0); RL = float(np.sqrt((np.log10(sub[:, 1] / g0) ** 2).mean()))
def full(s, w, A):
    H = tree_eval(s, A); g = A[:, 0]; p = law(g, A0 * H) if w == 1 else law(g * H, A0) if w == 2 else law(g, A0) * H; return np.log10(A[:, 1] / p)
LV = None; NAMES = None
def init(names, lv): 
    global LV, NAMES; LV = lv; NAMES = names; signal.signal(signal.SIGINT, signal.SIG_IGN)
def work(ia):
    i, op = ia; fn = B[op]; a = LV[i]; out = []; step = 2000; n = len(LV); c = 0
    for j in range(i if op in "+*" else 0, n, step):
        H = fn(a[None, :], LV[j:j + step]); c += H.shape[0]
        for k, w in stage1(H, None): out.append((i, op, j + k, w))
    return i, op, c, out
def main():
    if MODE == "known":
        d = np.log10(X[:, 1] / law(X[:, 0], A0)); print(f"H = 1 on all X-COP rows: mean {d.mean():+.4f}, rms {np.sqrt((d*d).mean()):.4f}, n {len(d)}, record +0.467, 0.476"); return
    al, tot = closure(); names = [t[0] for t in al]; lv = np.array([t[2] for t in al]); print(f"{MODE}: L2 {len(al)} of {tot} before cap, EV {EV.shape}, X-COP train {NX}, SPARC train {len(ST)}, holdout {len(SH)}, RL {RL:.4f}", flush=True)
    W = os.path.join(HERE, "chunks", MODE + os.environ.get("BF1_SUF", "")); os.makedirs(W, exist_ok=True); json.dump(names, open(os.path.join(W, "names.json"), "w"))
    done = os.path.join(W, "done.txt"); dn = set(open(done).read().split()) if os.path.exists(done) else set()
    jobs = [(i, o) for i in range(len(lv)) for o in B if f"{i}{o}" not in dn]
    if LIM: jobs = jobs[:LIM]
    stop = {"x": 0}
    signal.signal(signal.SIGTERM, lambda *a: stop.__setitem__("x", 1))
    tot_c = 0
    with Pool(NW, init, (names, lv)) as P, open(os.path.join(W, "hits.jsonl"), "a") as HF, open(done, "a") as DF:
        for k, (i, op, c, out) in enumerate(P.imap_unordered(work, jobs, chunksize=1)):
            tot_c += c
            for h in out: HF.write(json.dumps(h) + "\n")
            HF.flush(); DF.write(f"{i}{op}\n"); DF.flush()
            if k % 200 == 0: print(f"{k}/{len(jobs)} jobs, {tot_c:.3g} expressions this run", flush=True)
            if stop["x"]: print("SIGTERM: checkpointed", flush=True); P.terminate(); return
    print(f"DONE {MODE}: {tot_c:.4g} expressions this run", flush=True); open(os.path.join(W, "COMPLETE"), "w").write("1")
if __name__ == "__main__": main()
