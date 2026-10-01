"""B4 shared library: build/run the C programs (nice -n 10, cached by argument hash), flat-histogram table helpers, equal-weight / equal-height
line-position estimators from reweighted flat-histogram series, block jackknife, round-trip counting.  No physics claims live here."""
import sys
sys.dont_write_bytecode = True
import os
import subprocess
import hashlib
import math
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
BIN, SRC, CACHE = (os.path.join(HERE, d) for d in ("bin", "src", "cache"))
for d in (BIN, CACHE):
    os.makedirs(d, exist_ok=True)


def build(name, srcname=None, flags=("-DZFLIP",), srcdir=None):
    srcdir = srcdir or SRC
    exe = os.path.join(BIN, name)
    src = os.path.join(srcdir, (srcname or name) + ".c")
    deps = [src] + [os.path.join(SRC, h) for h in ("muca.h", "b4_common.h") if os.path.exists(os.path.join(SRC, h))]
    if (not os.path.exists(exe)) or os.path.getmtime(exe) < max(os.path.getmtime(p) for p in deps):
        r = subprocess.run(["cc", "-O3", "-march=native"] + list(flags) + ["-I", SRC, "-o", exe, src, "-lm"], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("compile failed: " + r.stderr[-800:])
    return exe


_EXEH = {}


def _exe_hash(exe):
    if exe not in _EXEH:
        _EXEH[exe] = hashlib.md5(open(exe, "rb").read()).hexdigest()[:8] if os.path.exists(exe) else "none"
    return _EXEH[exe]


def _key(tag, argv, exe=None):
    return hashlib.md5((tag + " " + " ".join(argv) + (" " + _exe_hash(exe) if exe else "")).encode()).hexdigest()[:12]


def run_cached(exe, kv, tag, outkey="out", nice=10):
    """kv: dict of key=value; output file path inserted under outkey; returns (path, stderr). Cached by hash of all arguments."""
    argv = [f"{k}={v}" for k, v in sorted(kv.items())]
    h = _key(tag + os.path.basename(exe), argv, exe)
    out = os.path.join(CACHE, f"{tag}_{h}.bin")
    log = out + ".log"
    if os.path.exists(out) and os.path.getsize(out) > 0 and os.path.exists(log):
        return out, open(log).read()
    tmp = out + ".tmp"
    r = subprocess.run(["nice", "-n", str(nice), exe] + argv + [f"{outkey}={tmp}"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{exe} {argv} failed rc={r.returncode}: {r.stderr[-300:]}")
    os.replace(tmp, out)
    open(log, "w").write(r.stderr)
    return out, r.stderr


def run_many(jobs, nworkers=8):
    """jobs: list of (exe, kv, tag, outkey); returns list of (path, stderr) in order"""
    res = [None] * len(jobs)

    def w(i):
        exe, kv, tag, ok = jobs[i]
        res[i] = run_cached(exe, kv, tag, ok)
    with ThreadPoolExecutor(max_workers=nworkers) as ex:
        list(ex.map(w, range(len(jobs))))
    return res


def load_series(path):
    return np.fromfile(path, dtype=np.float64).reshape(-1, 2)


def load_table(path):
    a = np.fromfile(path, dtype=np.float64)
    return dict(eps=a[0], lo=a[1], hi=a[2], nb=int(a[3]), lnG=a[4:4 + int(a[3])])


def W_of(O, tab):
    t = (O - tab["lo"]) / ((tab["hi"] - tab["lo"]) / tab["nb"])
    idx = np.floor(t).astype(int)
    ok = (idx >= 0) & (idx < tab["nb"])
    W = np.where(ok, tab["lnG"][np.clip(idx, 0, tab["nb"] - 1)], np.nan)
    return W, ok


def tau_int(x, c=6.0):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    if n < 20 or np.var(x) == 0:
        return 0.5
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac = ac / ac[0]
    t = 0.5
    for w in range(1, n):
        t += ac[w]
        if w >= c * t:
            return max(t, 0.5)
    return max(t, 0.5)


def round_trips(O, lo, hi, frac=0.15):
    """number of traversals between the lowest and highest `frac` of [lo,hi] (round trips = traversals/2) and the mean sample count per traversal"""
    zl, zh = lo + frac * (hi - lo), hi - frac * (hi - lo)
    side, n = 0, 0
    for o in O:
        s = -1 if o < zl else (1 if o > zh else 0)
        if s != 0:
            if side != 0 and s != side:
                n += 1
            side = s
    return n


class Pool:
    """pooled production data of one (L, point): arrays A, F, O, lnW (the table value W(O_i) of the sampled weight), chain id, in-order, plus the base couplings."""

    def __init__(self, series_list, tab, bw, bF0, bA0, Np):
        A, F, O, W, C, T = [], [], [], [], [], []
        self.ntrav = 0
        self.nsamp_chain = []
        for ci, s in enumerate(series_list):
            o = s[:, 0] + bw * s[:, 1]
            w, ok = W_of(o, tab)
            self.ntrav += round_trips(o, tab["lo"], tab["hi"])
            A.append(s[ok, 0]); F.append(s[ok, 1]); O.append(o[ok]); W.append(w[ok]); C.append(np.full(ok.sum(), ci)); T.append(np.arange(ok.sum()))
            self.nsamp_chain.append(int(ok.sum()))
        self.A, self.F, self.O, self.W, self.C, self.T = (np.concatenate(x) for x in (A, F, O, W, C, T))
        self.bF0, self.bA0, self.bw, self.Np, self.tab = bF0, bA0, bw, Np, tab
        self.nchain = len(series_list)

    def thin(self, maxn=250000):
        """thinned copy (every k-th sample, chain structure kept) for the jackknife; the autocorrelation makes this nearly lossless"""
        n = len(self.A)
        if n <= maxn:
            return self
        k = int(math.ceil(n / maxn))
        sel = (self.T % k) == 0
        c = Pool.__new__(Pool)
        for key in ("A", "F", "O", "W", "C", "T"):
            setattr(c, key, getattr(self, key)[sel])
        c.bF0, c.bA0, c.bw, c.Np, c.tab, c.nchain, c.ntrav = self.bF0, self.bA0, self.bw, self.Np, self.tab, self.nchain, self.ntrav
        c.nsamp_chain = self.nsamp_chain
        return c

    def blocks(self, nblk):
        """block id for each sample: contiguous blocks inside each chain"""
        bid = np.zeros(len(self.A), int)
        off = 0
        for ci in range(self.nchain):
            m = self.C == ci
            n = m.sum()
            bid[m] = off + (np.arange(n) * nblk // max(n, 1))
            off += nblk
        return bid, off


def _hist(A, w, lo, hi, nbin):
    idx = np.clip(((A - lo) / (hi - lo) * nbin).astype(int), 0, nbin - 1)
    return np.bincount(idx, weights=w, minlength=nbin)


def _smooth(h, k=3):
    if k <= 1:
        return h
    ker = np.ones(k) / k
    return np.convolve(h, ker, mode="same")


def eq_beta(A, lnw0, b0, mid, window=0.35, nbin=240, kind="weight", cut0=None, iters=4, F=None, dF=0.0):
    """Equal-weight (or equal-height) coupling in beta_A: weights exp(lnw0 + (b-b0) A).  `mid` separates the two phase centres (peaks are looked for on each side).
    Returns dict(b, cut, ...) or None."""
    lo, hi = A.min(), A.max()

    def lw(b):
        x = lnw0 + (b - b0) * A
        return x - x.max()

    def peaks_cut(b):
        w = np.exp(lw(b))
        h = _smooth(_hist(A, w, lo, hi, nbin), 5)
        cen = lo + (np.arange(nbin) + 0.5) * (hi - lo) / nbin
        l = cen < mid
        r = ~l
        if l.sum() < 3 or r.sum() < 3:
            return None
        il = np.argmax(np.where(l, h, -1)); ir = np.argmax(np.where(r, h, -1))
        a, c = (il, ir) if il < ir else (ir, il)
        iv = a + int(np.argmin(h[a:c + 1]))
        return dict(il=il, ir=ir, iv=iv, cut=cen[iv], hL=h[il], hR=h[ir], hV=h[iv], cen=cen, h=h)

    cut = cut0 if cut0 is not None else mid
    b = b0
    for _ in range(iters):
        if kind == "weight":
            def f(bb):
                w = np.exp(lw(bb))
                zl = w[A < cut].sum(); zh = w[A >= cut].sum()
                if zl <= 0 or zh <= 0:
                    return 50.0 * (1 if zh > 0 else -1)
                return math.log(zh / zl)
        else:
            def f(bb):
                p = peaks_cut(bb)
                if p is None:
                    return 0.0
                return math.log(max(p["hR"], 1e-300) / max(p["hL"], 1e-300))
        try:
            lo_b, hi_b = b - window, b + window
            flo, fhi = f(lo_b), f(hi_b)
            k = 0
            while flo * fhi > 0 and k < 4:
                lo_b -= window; hi_b += window; flo, fhi = f(lo_b), f(hi_b); k += 1
            if flo * fhi > 0:
                return None
            b = brentq(f, lo_b, hi_b, xtol=1e-9)
        except Exception:
            return None
        pk = peaks_cut(b)
        if pk is None:
            return None
        cut = pk["cut"]
    pk = peaks_cut(b)
    w = np.exp(lw(b)); w /= w.sum()
    out = dict(b=b, cut=cut, lnsaddle=math.log(min(pk["hL"], pk["hR"]) / max(pk["hV"], 1e-300)) if pk["hV"] > 0 else float("inf"),
               XA_lo=float((w * A)[A < cut].sum() / w[A < cut].sum()), XA_hi=float((w * A)[A >= cut].sum() / w[A >= cut].sum()))
    if F is not None:
        out["F_lo"] = float((w * F)[A < cut].sum() / w[A < cut].sum()); out["F_hi"] = float((w * F)[A >= cut].sum() / w[A >= cut].sum())
    return out


def jk_eq(pool, mid, kind="weight", nblk=8, tau_block=None, window=0.35):
    """equal-weight/height beta_A for the pooled data + delete-one-block jackknife error (Amendment-free implementation of the pre-registered rules).
    Block length rule: >= 2 x mean round-trip time; the number of blocks is reduced to >= 4 per chain, and the error inflated if still shorter."""
    Np = pool.Np
    n_full = len(pool.A)
    pool = pool.thin()
    base = eq_beta(pool.A, pool.W, pool.bA0, mid, kind=kind, window=window, F=pool.F)
    if base is None:
        return None
    n_tot = n_full
    ntrav = max(pool.ntrav, 1)
    t_rt = n_tot / (ntrav / 2.0) if ntrav > 0 else float("inf")      # samples per round trip (pooled over chains)
    per_chain = n_tot / pool.nchain
    nb = nblk
    while nb > 4 and per_chain / nb < 2.0 * t_rt / pool.nchain * 1.0:
        nb -= 1
    blen = per_chain / nb
    infl = max(1.0, math.sqrt(2.0 * (t_rt / pool.nchain) / blen)) if t_rt < float("inf") else 1.0
    bid, nbt = pool.blocks(nb)
    est = []
    for j in range(nbt):
        m = bid != j
        r = eq_beta(pool.A[m], pool.W[m], pool.bA0, mid, kind=kind, window=window, cut0=base["cut"])
        if r is not None:
            est.append(r["b"])
    est = np.array(est)
    if len(est) < 4:
        return None
    err = math.sqrt((len(est) - 1) / len(est) * np.sum((est - est.mean()) ** 2)) * infl
    base.update(err=err, infl=infl, nblk=nb, ntrav=pool.ntrav, nsamp=n_tot, t_rt_samples=t_rt)
    return base


def phase_indicator_tau(pool, bstar, cut):
    out = []
    for ci in range(pool.nchain):
        m = pool.C == ci
        x = (pool.A[m] >= cut).astype(float)
        out.append(tau_int(x))
    return float(np.max(out))


# ---------------------------------------------------------------------------------------------------------------- a flat-histogram point
def pilot_range(exe, L, bF, bA0, delta, bw=0.0, nsw=800, nth=300, seed0=11, tag="pilot"):
    """two short canonical runs (hot start below, cold start above beta_A^0); returns (lo, hi, midpoint, stats)"""
    res = {}
    for name, bA, cold in (("low", bA0 - delta, 0), ("high", bA0 + delta, 1)):
        kv = dict(mode=0, L=L, bF=f"{bF:.4f}", bA=f"{bA:.4f}", seed=seed0 + cold, cold=cold, nhit=4, refl=1, bw=bw, nth=nth, nsw=nsw, every=1)
        p, _ = run_cached(exe, kv, tag)
        s = load_series(p)
        o = s[:, 0] + bw * s[:, 1]
        res[name] = (float(o.mean()), float(o.std()), float(s[:, 0].mean()), float(s[:, 1].mean()))
    lo = res["low"][0] - 6 * res["low"][1]
    hi = res["high"][0] + 6 * res["high"][1]
    mid = 0.5 * (res["low"][0] + res["high"][0])
    return lo, hi, mid, res


def build_table(exe, L, bF, bA0, lo, hi, bw=0.0, nb=400, seed=101, nth=500, wlmax=2000000, lnf_end=1e-3, flat_int=200, flat_frac=0.5, tag="wl"):
    kv = dict(mode=1, L=L, bF=f"{bF:.4f}", bA=f"{bA0:.4f}", seed=seed, cold=0, nhit=4, refl=1, bw=bw, nth=nth, nsw=0, lo=f"{lo:.4f}", hi=f"{hi:.4f}", nb=nb,
              wlmax=wlmax, lnf_end=lnf_end, flat_int=flat_int, flat_frac=flat_frac)
    # the table is the 'table' output; run_cached's generic 'out' key is unused in mode 1, so pass table via outkey
    p, err = run_cached(exe, kv, tag, outkey="table")
    return p, err


def produce(exe, table, L, bF, bA0, nchain, nth, nsw, every, bw=0.0, mut=0, seed0=1000, nw=4, tag="prod"):
    jobs = []
    for c in range(nchain):
        kv = dict(mode=2, L=L, bF=f"{bF:.4f}", bA=f"{bA0:.4f}", seed=seed0 + 7 * c + 13 * L + int(round(bF * 1000)), cold=c % 2, nhit=4, refl=1, bw=bw,
                  nth=nth, nsw=nsw, every=every, table=table, mut=mut)
        jobs.append((exe, kv, tag + ("m" if mut else ""), "out"))
    return run_many(jobs, nw)


def table_eq(tab, b0, mid, kind="weight", bw=0.0):
    """Estimator T: equal-weight beta_A directly from the Wang-Landau density of states lnG(O) (O = A for bw = 0); bins at their centres."""
    nb = tab["nb"]
    dw = (tab["hi"] - tab["lo"]) / nb
    A = tab["lo"] + (np.arange(nb) + 0.5) * dw
    return eq_beta_binned(A, tab["lnG"], b0, mid)


def eq_beta_binned(A, lng, b0, mid, window=0.35):
    """as eq_beta (weight kind) but for a tabulated density lng(A_k) (one entry per bin): P(A_k; b) ~ exp(lng + (b-b0) A_k); the cut = valley between the two peaks."""
    def lw(b):
        x = lng + (b - b0) * A
        return x - x.max()

    def cut_of(b):
        h = np.exp(lw(b))
        hs = _smooth(h, 5)
        l = A < mid
        il = np.argmax(np.where(l, hs, -1)); ir = np.argmax(np.where(~l, hs, -1))
        a, c = (il, ir) if il < ir else (ir, il)
        iv = a + int(np.argmin(hs[a:c + 1]))
        return A[iv], iv, il, ir, hs

    cut = mid
    b = b0
    for _ in range(4):
        def f(bb):
            h = np.exp(lw(bb))
            return math.log(max(h[A >= cut].sum(), 1e-300) / max(h[A < cut].sum(), 1e-300))
        lo_b, hi_b = b - window, b + window
        k = 0
        while f(lo_b) * f(hi_b) > 0 and k < 4:
            lo_b -= window; hi_b += window; k += 1
        if f(lo_b) * f(hi_b) > 0:
            return None
        b = brentq(f, lo_b, hi_b, xtol=1e-9)
        cut = cut_of(b)[0]
    cut, iv, il, ir, hs = cut_of(b)
    return dict(b=b, cut=cut, lnsaddle=math.log(min(hs[il], hs[ir]) / hs[iv]), XA_lo=float(A[il]), XA_hi=float(A[ir]))


def hist_O(series_list, tab, bw):
    H = np.zeros(tab["nb"])
    dw = (tab["hi"] - tab["lo"]) / tab["nb"]
    for s in series_list:
        o = s[:, 0] + bw * s[:, 1]
        idx = np.floor((o - tab["lo"]) / dw).astype(int)
        idx = idx[(idx >= 0) & (idx < tab["nb"])]
        H += np.bincount(idx, minlength=tab["nb"])
    return H


def refine_table(tab, H, damp=3.0, floor=1.0):
    """Berg-Neuhaus-type update W <- W + ln(H / mean H) with damping, applied to the frozen table; returns a new table dict (declared in the pre-registration as the refinement round)."""
    Hs = np.maximum(H, floor)
    r = np.log(Hs / Hs.mean())
    r = np.clip(r, -damp, damp)
    new = dict(tab)
    new["lnG"] = tab["lnG"] + r
    return new


def save_table(tab, path):
    np.concatenate([[tab["eps"], tab["lo"], tab["hi"], tab["nb"]], tab["lnG"]]).astype(np.float64).tofile(path)


def flat_stats(H):
    return float(H.min() / H.mean()) if H.mean() > 0 else 0.0


# ---------------------------------------------------------------------------------------------------------------- generic point runner
class Model:
    """exe: built binary; cp: dict of the fixed couplings written to the command line (gauge: bF, bA0; Potts: q, beta); bkey: name of the swept coupling (bA / beta);
    Np: scale used only for reporting; bw: weight of F in the sampled variable O."""

    def __init__(self, exe, name, couplings, bkey, b0, Np, bw=0.0, extra=None, obounds=(None, None), nsig=6.0, quant=None):
        self.exe, self.name, self.cp, self.bkey, self.b0, self.Np, self.bw = exe, name, dict(couplings), bkey, b0, Np, bw
        self.extra = extra or {}
        self.obounds, self.nsig, self.quant = obounds, nsig, quant

    def kv(self, **over):
        d = dict(self.cp)
        d[self.bkey] = f"{self.b0:.5f}"
        d.update(self.extra)
        d.update(over)
        return d


def pilot(model, delta, nsw=800, nth=300, seed0=11):
    for attempt in range(4):
        res = {}
        for name, sgn, cold in (("low", -1, 0), ("high", +1, 1)):
            kv = model.kv(mode=0, seed=seed0 + cold, cold=cold, nth=nth, nsw=nsw, every=1, bw=model.bw)
            kv[model.bkey] = f"{model.b0 + sgn * delta:.5f}"
            p, _ = run_cached(model.exe, kv, "pilot" + model.name)
            s = load_series(p)
            o = s[:, 0] + model.bw * s[:, 1]
            res[name] = (float(o.mean()), float(o.std()))
        if res["high"][0] - res["low"][0] > 8 * max(res["low"][1], res["high"][1]):
            break
        delta *= 2.0
    res["delta_used"] = delta
    lo = res["low"][0] - model.nsig * res["low"][1]
    hi = res["high"][0] + model.nsig * res["high"][1]
    if model.obounds[0] is not None:
        lo = max(lo, model.obounds[0])
    if model.obounds[1] is not None:
        hi = min(hi, model.obounds[1])
    return lo, hi, 0.5 * (res["low"][0] + res["high"][0]), res


def wl_table(model, lo, hi, nb=400, seed=101, nth=500, lnf_end=1e-3, flat_int=200, wlmax=3000000):
    kv = model.kv(mode=1, seed=seed, cold=0, nth=nth, nsw=0, lo=f"{lo:.4f}", hi=f"{hi:.4f}", nb=nb, wlmax=wlmax, lnf_end=lnf_end, flat_int=flat_int, flat_frac=0.5, bw=model.bw)
    p, err = run_cached(model.exe, kv, "wl" + model.name, outkey="table")
    return p, err


def produce_m(model, table, nchain, nth, nsw, every, mut=0, seed0=1000, nw=4, tag="prod"):
    jobs = []
    for c in range(nchain):
        kv = model.kv(mode=2, seed=seed0 + 7 * c + 13 * int(model.cp.get("L", 0)) + 101 * len(model.name), cold=c % 2, nth=nth, nsw=nsw, every=every, table=table, mut=mut, bw=model.bw)
        jobs.append((model.exe, kv, tag + model.name + ("m" if mut else ""), "out"))
    return run_many(jobs, nw)


def refine_loop(model, tab, path0, nchain=4, nth=200, nsw=10000, every=2, max_rounds=8, flat_target=0.25, seed0=5000, nw=4, log=print):
    """declared refinement: W <- W + ln H damped, until the production histogram is flat enough (min/mean >= flat_target) or max_rounds."""
    cur = dict(tab)
    for rnd in range(max_rounds):
        tp = os.path.join(CACHE, f"rt_{model.name}_{_key('rt', [str(rnd), str(model.cp), str(model.b0), path0, str(nsw)])}.bin")
        save_table(cur, tp)
        outs = produce_m(model, tp, nchain, nth, nsw, every, seed0=seed0 + 100 * rnd, nw=nw, tag="ref")
        ser = [load_series(o) for o, _ in outs]
        H = hist_O(ser, cur, model.bw)
        fl = flat_stats(H)
        ntr = sum(round_trips(s[:, 0] + model.bw * s[:, 1], cur["lo"], cur["hi"]) for s in ser)
        log(f"      refine round {rnd}: flat {fl:.3f}, traversals {ntr}")
        if fl >= flat_target and rnd >= 1:
            return tp, cur, rnd, fl
        cur = refine_table(cur, H)
    tp = os.path.join(CACHE, f"rt_{model.name}_final_{_key('rtf', [str(model.cp), str(model.b0), path0])}.bin")
    save_table(cur, tp)
    return tp, cur, max_rounds, fl


def run_point(model, delta, init=None, nb=400, nchain=4, nth=300, nsw=20000, every=2, target_trav=24, max_batches=12, wl_seed=101, wl_flat_int=200, ref_nsw=10000, nw=4,
              mut=0, lnf_end=1e-3, log=print, ref_rounds=8):
    """pilot -> Wang-Landau table -> refinement rounds -> frozen-weight production batches until >= target_trav traversals (or max_batches).
    returns dict with pool, tab, mid, diagnostics."""
    lo, hi, mid, pres = pilot(model, delta)
    if model.quant:
        lo, hi, nb = model.quant(lo, hi)
    elif nb == "auto":
        smin = min(pres["low"][1], pres["high"][1])
        nb = int(min(max(round((hi - lo) / (0.4 * smin)), 60), 300))
    if init is not None:
        # start from a supplied density of states on the same bin grid (the stitched windowed estimate): written as a table file, eps from the pilot-free default
        tab = dict(eps=init["eps"], lo=lo, hi=hi, nb=len(init["lnG"]), lnG=np.nan_to_num(init["lnG"], nan=0.0))
        p = os.path.join(CACHE, f"init_{model.name}_{_key('init', [str(model.cp), str(model.b0), str(lo), str(hi), str(len(init['lnG']))])}.bin")
        save_table(tab, p)
        werr = "initial table from windowed Wang-Landau"
    else:
        p, werr = wl_table(model, lo, hi, nb=nb, seed=wl_seed, lnf_end=lnf_end, flat_int=wl_flat_int)
        tab = load_table(p)
    tp, tabr, nr, fl = refine_loop(model, tab, p, nchain=nchain, nth=nth, nsw=ref_nsw, every=every, nw=nw, log=log, max_rounds=ref_rounds)
    series = []
    ntrav = 0
    tabf = load_table(tp)
    for b in range(max_batches):
        outs = produce_m(model, tp, nchain, nth, nsw, every, mut=mut, seed0=9000 + 1000 * b, nw=nw, tag="prod")
        for o, _ in outs:
            s = load_series(o)
            series.append(s)
            ntrav += round_trips(s[:, 0] + model.bw * s[:, 1], tabf["lo"], tabf["hi"])
        if ntrav >= target_trav:
            break
    pool = Pool(series, tabf, model.bw, float(model.cp.get('bF', 0.0)), model.b0, model.Np)
    return dict(pool=pool, tab=tabf, mid=mid, lo=lo, hi=hi, pilot=pres, wl_log=werr.strip(), refine_rounds=nr, flat=fl, ntrav=ntrav, nbatch=b + 1, nchain_total=len(series))


# ---------------------------------------------------------------------------------------------------------------- V-method: three-phase equal weight
def vertex_solve(O, A, F, lw0, x0=(0.0, 0.0), nbin=200, cuts0=None, iters=4):
    """Solve the two equations ln(Z_II/Z_I) = ln(Z_III/Z_II) = 0 for the shifts x = (dbeta_F, dbeta_A) of the weights exp(lw0 + x0 F + x1 A);
    the phases I < II < III are the three peaks of the reweighted P(O), separated at the valleys (re-located at every outer iteration).  Returns dict or None."""
    from scipy.optimize import fsolve
    from scipy.signal import find_peaks
    lo, hi = O.min(), O.max()
    cen = lo + (np.arange(nbin) + 0.5) * (hi - lo) / nbin

    def lwt(x):
        v = lw0 + x[0] * F + x[1] * A
        return v - v.max()

    def find_cuts(x):
        w = np.exp(lwt(x))
        h = _smooth(_hist(O, w, lo, hi, nbin), 5)
        pk, pr = find_peaks(h / h.max(), prominence=1e-4)
        if len(pk) < 3:
            return None
        top = sorted(pk[np.argsort(h[pk])[-3:]])
        c = [top[0] + int(np.argmin(h[top[0]:top[1] + 1])), top[1] + int(np.argmin(h[top[1]:top[2] + 1]))]
        return [cen[c[0]], cen[c[1]]]

    x = np.array(x0, float)
    cuts = cuts0 if cuts0 is not None else find_cuts(x)
    if cuts is None:
        return None
    for _ in range(iters):
        def g(xx):
            w = np.exp(lwt(xx))
            z1 = w[O < cuts[0]].sum(); z2 = w[(O >= cuts[0]) & (O < cuts[1])].sum(); z3 = w[O >= cuts[1]].sum()
            return [math.log(max(z2, 1e-300) / max(z1, 1e-300)), math.log(max(z3, 1e-300) / max(z2, 1e-300))]
        sol, info, ier, msg = fsolve(g, x, full_output=True)
        if ier != 1:
            return None
        x = sol
        c2 = find_cuts(x)
        if c2 is None:
            return None
        cuts = c2
    w = np.exp(lwt(x)); w /= w.sum()
    return dict(dbF=float(x[0]), dbA=float(x[1]), cuts=cuts, z=[float(w[O < cuts[0]].sum()), float(w[(O >= cuts[0]) & (O < cuts[1])].sum()), float(w[O >= cuts[1]].sum())])


def vertex_jk(pool, nblk=8, window=None):
    """V-method triple point for a pooled flat-histogram data set in O = A + F (bw = 1) at base couplings (pool.bF0, pool.bA0): value and delete-one-block jackknife errors"""
    pool = pool.thin()
    base = vertex_solve(pool.O, pool.A, pool.F, pool.W)
    if base is None:
        return None
    bid, nbt = pool.blocks(nblk)
    est = []
    for j in range(nbt):
        m = bid != j
        r = vertex_solve(pool.O[m], pool.A[m], pool.F[m], pool.W[m], x0=(base["dbF"], base["dbA"]), cuts0=base["cuts"])
        if r is not None:
            est.append((r["dbF"], r["dbA"]))
    est = np.array(est)
    if len(est) < 4:
        return None
    n = len(est)
    e = np.sqrt((n - 1) / n * np.sum((est - est.mean(0)) ** 2, axis=0))
    base.update(bF=pool.bF0 + base["dbF"], bA=pool.bA0 + base["dbA"], sF=float(e[0]), sA=float(e[1]), ntrav=pool.ntrav)
    return base


# ---------------------------------------------------------------------------------------------------------------- windowed Wang-Landau (Amendment 2)
def window_layout(nbtot, nbw=16, step=8):
    starts = list(range(0, max(nbtot - nbw, 0) + 1, step))
    if starts[-1] + nbw < nbtot:
        starts.append(nbtot - nbw)
    return starts


def wl_window_tables(model, lo, binw, nbtot, replicas, nbw=16, step=8, nth=300, lnf_end=1e-3, flat_int=100, wlmax=400000, nw=8):
    """Wang-Landau in narrow overlapping windows of the global bin grid (hard walls at the window edges), run in parallel; one stitched ln g per replica.
    replicas: list of (cold, seed).  Returns (list of global lnG arrays with nan outside coverage, bin centres)."""
    starts = window_layout(nbtot, nbw, step)
    jobs, keys = [], []
    for ri, (cold, seed) in enumerate(replicas):
        for wi, s0 in enumerate(starts):
            lo_w, hi_w = lo + s0 * binw, lo + (s0 + nbw) * binw
            kv = model.kv(mode=1, seed=seed + 31 * wi, cold=cold, nth=nth, nsw=0, lo=f"{lo_w:.5f}", hi=f"{hi_w:.5f}", nb=nbw, wlmax=wlmax, lnf_end=lnf_end, flat_int=flat_int, flat_frac=0.5, bw=model.bw)
            jobs.append((model.exe, kv, "wlw" + model.name, "table"))
            keys.append((ri, wi, s0))
    res = run_many(jobs, nw)
    out = []
    logs = []
    for ri in range(len(replicas)):
        pieces = []
        for (r_i, wi, s0), (p, err) in zip(keys, res):
            if r_i != ri:
                continue
            t = load_table(p)
            pieces.append((s0, t["lnG"], err))
        out.append(stitch(pieces, nbtot, nbw))
        logs.append([e.strip() for _, _, e in pieces])
    cen = lo + (np.arange(nbtot) + 0.5) * binw
    return out, cen, logs


def stitch(pieces, nbtot, nbw, edge=2):
    """pieces: [(start_bin, lnG[nbw], log)] in window order -> global ln g (up to a constant): the shift of each window is the mean difference over the interior
    of the overlap with the already assembled part; only interior bins (edge bins dropped, except at the two global ends) are used."""
    g = np.full(nbtot, np.nan)
    first = True
    for s0, lg, _ in pieces:
        lg = np.asarray(lg, float)
        idx = np.arange(nbw)
        interior = (idx >= edge) & (idx < nbw - edge)
        if s0 == 0:
            interior = interior | (idx < edge)
        if s0 + nbw == nbtot:
            interior = interior | (idx >= nbw - edge)
        gb = s0 + idx
        if first:
            g[gb[interior]] = lg[interior]
            first = False
            continue
        have = interior & np.isfinite(g[gb])
        if have.sum() == 0:
            have = np.isfinite(g[gb])
        delta = float(np.mean(g[gb[have]] - lg[have]))
        new = interior & ~np.isfinite(g[gb])
        g[gb[new]] = lg[new] + delta
    return g


def window_point(model, delta, nbw=16, step=8, replicas=((0, 101), (1, 202), (0, 303), (1, 404)), lnf_end=1e-3, nw=8, nth=300, log=print, wlmax=400000):
    """pilot -> windowed Wang-Landau (replicas) -> stitched ln g -> equal-weight (and equal-height-free) beta_A* per replica; returns dict with mean, standard error, spread."""
    lo, hi, mid, pres = pilot(model, delta)
    if model.quant:
        lo, hi, nbtot = model.quant(lo, hi)
    else:
        smin = min(pres["low"][1], pres["high"][1])
        nbtot = int(min(max(round((hi - lo) / (0.4 * smin)), 60), 300))
    binw = (hi - lo) / nbtot
    tabs, cen, logs = wl_window_tables(model, lo, binw, nbtot, list(replicas), nbw=nbw, step=step, nth=nth, lnf_end=lnf_end, nw=nw, wlmax=wlmax)
    vals, sad = [], []
    for g in tabs:
        ok = np.isfinite(g)
        r = eq_beta_binned(cen[ok], g[ok], model.b0, mid)
        if r is not None:
            vals.append(r["b"]); sad.append(r["lnsaddle"])
    vals = np.array(vals)
    if len(vals) < 2:
        return None
    gs = []
    for g in tabs:
        gg = g - np.nanmean(g)
        gs.append(gg)
    gmean = np.nanmean(np.array(gs), axis=0)
    return dict(gmean=gmean, b=float(vals.mean()), err=float(vals.std(ddof=1) / math.sqrt(len(vals))), spread=float(vals.std(ddof=1)), vals=vals.tolist(), lnsaddle=float(np.mean(sad)),
                nbtot=nbtot, nwin=len(window_layout(nbtot, nbw, step)), lo=lo, hi=hi, mid=mid, pilot=pres, nsweeps=[[l.split("wl_sweeps=")[1].split()[0] for l in ls if "wl_sweeps=" in l] for ls in logs])
