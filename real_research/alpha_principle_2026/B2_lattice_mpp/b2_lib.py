"""Shared helpers for the B2 lane: build the C programs, run Monte Carlo jobs in parallel with a cache, autocorrelation, and
binned multi-histogram reweighting (WHAM) in one coupling with block-jackknife errors.  No physics claims live here."""
import sys
sys.dont_write_bytecode = True
import os
import subprocess
import hashlib
import numpy as np
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "bin")
SRC = os.path.join(HERE, "src")
CACHE = os.path.join(HERE, "cache")
os.makedirs(BIN, exist_ok=True)
os.makedirs(CACHE, exist_ok=True)


def build(name):
    """name 'su2z'/'su3z' compiles su2.c/su3.c with -DZFLIP (center-flip proposals)"""
    exe = os.path.join(BIN, name)
    flags = []
    base = name
    if name in ("su2z", "su3z"):
        base = name[:-1]
        flags = ["-DZFLIP"]
    src = os.path.join(SRC, base + ".c")
    if (not os.path.exists(exe)) or os.path.getmtime(exe) < max(os.path.getmtime(src), os.path.getmtime(os.path.join(SRC, "b2_common.h"))):
        r = subprocess.run(["cc", "-O3", "-march=native"] + flags + ["-o", exe, src, "-lm"], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError("compile failed: " + r.stderr[-500:])
    return exe


def cache_path(tag, args):
    h = hashlib.md5(" ".join(map(str, args)).encode()).hexdigest()[:10]
    return os.path.join(CACHE, f"{tag}_{h}.bin")


def run_one(exe, args, tag):
    """args excludes the outfile; returns path.  Skips if cached output exists and is non-empty."""
    out = cache_path(tag, [os.path.basename(exe)] + list(args))
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return out
    tmp = out + ".tmp"
    r = subprocess.run([exe] + [str(a) for a in args] + [tmp], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{exe} {args} failed rc={r.returncode}: {r.stderr[-300:]}")
    os.replace(tmp, out)
    return out


def run_many(jobs, nworkers=12, verbose=True):
    """jobs: list of (exe, args, tag). Returns list of paths (same order)."""
    res = [None] * len(jobs)

    def work(i):
        exe, args, tag = jobs[i]
        res[i] = run_one(exe, args, tag)
        if verbose:
            print(f"    done {i + 1}/{len(jobs)} {os.path.basename(exe)} {args}", flush=True)
    with ThreadPoolExecutor(max_workers=nworkers) as ex:
        list(ex.map(work, range(len(jobs))))
    return res


def load(path):
    a = np.fromfile(path, dtype=np.float64)
    return a.reshape(-1, 2)


def tau_int(x, c=6.0):
    """Sokal automatic-window integrated autocorrelation time (in units of the sample spacing)."""
    x = np.asarray(x, dtype=float) - np.mean(x)
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


def logsumexp(a, axis=None):
    m = np.max(a, axis=axis, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)
    r = np.log(np.sum(np.exp(a - m), axis=axis, keepdims=True)) + m
    return np.squeeze(r, axis=axis) if axis is not None else float(np.squeeze(r))


class Wham1D:
    """Binned multi-histogram reweighting in one coupling b for weight exp(b * Np * O) (O = the observable conjugate to the coupling; Np plaquettes).
    series: list of 1D arrays (one per run) of O per measurement; betas: list of couplings of the runs; nblk: blocks per run for jackknife.
    Provides moments(beta) and the jackknife over blocks (delete-one-block from every run)."""

    def __init__(self, series, betas, Np, nblk=8, binfac=None):
        self.Np = Np
        self.betas = np.asarray(betas, float)
        allv = np.concatenate(series)
        lo, hi = allv.min(), allv.max()
        sig = max(np.std(allv), 1e-12)
        dE = min(5.0 / Np, sig / 12.0) if binfac is None else binfac
        self.nbin = int(min(max(np.ceil((hi - lo) / dE) + 1, 20), 20000))
        self.edges = np.linspace(lo, hi + 1e-15, self.nbin + 1)
        self.E = 0.5 * (self.edges[1:] + self.edges[:-1])
        self.nblk = nblk
        K = len(series)
        self.H = np.zeros((K, nblk, self.nbin))
        for k, s in enumerate(series):
            n = len(s)
            for b in range(nblk):
                seg = s[b * n // nblk:(b + 1) * n // nblk]
                self.H[k, b], _ = np.histogram(seg, bins=self.edges)

    def solve(self, drop=None, niter=4000, tol=1e-10):
        H = self.H.copy()
        if drop is not None:
            H[:, drop, :] = 0.0
        Hk = H.sum(axis=1)  # K x nbin
        nk = Hk.sum(axis=1)
        tot = Hk.sum(axis=0)
        lognk = np.log(nk)
        f = np.zeros(len(nk))  # f_k = log Z_k
        BE = np.outer(self.betas * self.Np, self.E)  # K x nbin : b_k Np E
        for it in range(niter):
            # log rho_b = log tot_b - logsumexp_k (log n_k + BE_kb - f_k)
            den = logsumexp(lognk[:, None] + BE - f[:, None], axis=0)
            lrho = np.where(tot > 0, np.log(np.where(tot > 0, tot, 1)) - den, -np.inf)
            fnew = logsumexp(lrho[None, :] + BE, axis=1)
            fnew -= fnew[0]
            if np.max(np.abs(fnew - f)) < tol:
                f = fnew
                break
            f = fnew
        den = logsumexp(lognk[:, None] + BE - f[:, None], axis=0)
        self._lrho = np.where(tot > 0, np.log(np.where(tot > 0, tot, 1)) - den, -np.inf)
        return self._lrho

    def moments(self, beta, lrho=None):
        lrho = self._lrho if lrho is None else lrho
        lw = lrho + beta * self.Np * self.E
        lw = lw - np.max(lw[np.isfinite(lw)])
        w = np.exp(lw)
        w /= w.sum()
        m1 = np.sum(w * self.E)
        m2 = np.sum(w * self.E ** 2)
        m4 = np.sum(w * self.E ** 4)
        return m1, m2, m4

    def obs(self, beta, lrho=None):
        m1, m2, m4 = self.moments(beta, lrho)
        chi = self.Np * (m2 - m1 ** 2)
        var = m2 - m1 ** 2
        # Binder-type cumulant of the fluctuation about the mean: 1 - <(E-m)^4>/(3<(E-m)^2>^2)
        lrho_ = self._lrho if lrho is None else lrho
        lw = lrho_ + beta * self.Np * self.E
        lw = lw - np.max(lw[np.isfinite(lw)])
        w = np.exp(lw)
        w /= w.sum()
        c2 = np.sum(w * (self.E - m1) ** 2)
        c4 = np.sum(w * (self.E - m1) ** 4)
        binder = 1.0 - c4 / (3.0 * c2 ** 2) if c2 > 0 else np.nan
        return m1, chi, binder


def peak(wh, lrho, fn, grid):
    """location of the max of fn(beta) over a grid, refined by a parabola through the top three points; returns (beta_peak, value)"""
    vals = np.array([fn(wh, lrho, b) for b in grid])
    i = int(np.argmax(vals))
    if 0 < i < len(grid) - 1:
        y0, y1, y2 = vals[i - 1], vals[i], vals[i + 1]
        den = y0 - 2 * y1 + y2
        if den < 0:
            dx = 0.5 * (y0 - y2) / den
            return grid[i] + dx * (grid[1] - grid[0]), y1
    return grid[i], vals[i]


def jackknife(est):
    """est: array of leave-one-out estimates (n,) -> (mean, error)"""
    est = np.asarray(est, float)
    n = len(est)
    m = est.mean()
    return m, np.sqrt((n - 1) / n * np.sum((est - m) ** 2))


def per_group(N, b_adj, b_f, expo):
    """1/alpha_crit,cont per SU(N) group from the papers' formulae (hep-ph/9311321 eqs (4),(36),(37); B1 script): fixed in the pre-registration"""
    import math
    C_adj, C_f = N, (N * N - 1) / (2.0 * N)
    full = 4 * math.pi * (C_adj * b_adj + C_f * b_f) / (N * N - 1)
    a_full = 1.0 / full
    if expo:
        fa, ff = math.exp(-math.pi * C_adj * a_full), math.exp(-math.pi * C_f * a_full)
    else:
        fa, ff = 1 - math.pi * C_adj * a_full, 1 - math.pi * C_f * a_full
    return 4 * math.pi * (C_adj * b_adj * fa + C_f * b_f * ff) / (N * N - 1), full


# ---------------------------------------------------------------------------------------------------------------- line scans for SU(N) fund-adj
def nonab_args(group, L, bF, bA, nsw, nth, seed, cold, hits, mut):
    if group.startswith("su2"):
        return [L, f"{bF:.4f}", f"{bA:.4f}", nsw, nth, seed, cold, hits, 0, int(mut)]
    return [L, f"{bF:.4f}", f"{bA:.4f}", nsw, nth, seed, cold, hits, int(mut)]


def scan_line(group, kind, L, fixed, grid, nsw, nth, seeds, hits, mut=False, nw=12, nblk=8, fine=0.005, tag_extra=""):
    """kind 'A': vary beta_A at fixed beta_F (conjugate X_A, col 1); kind 'F': vary beta_F at fixed beta_A (conjugate X_F, col 0).
    Returns dict: list of local maxima of chi = Np Var(X_conj) with (x, chi, err, edge_flag), chi curve, tau_max, run count."""
    exe = build(group)
    jobs, keys = [], []
    for g in grid:
        for sd in seeds:
            cold = 0 if sd % 2 == 1 else 1
            bF, bA = (fixed, g) if kind == "A" else (g, fixed)
            seed = 7919 * L + 104729 * sd + int(round(bF * 1000)) * 31 + int(round(bA * 1000)) * 17
            jobs.append((exe, nonab_args(group, L, bF, bA, nsw, nth, seed, cold, hits, mut), f"{group}{'m' if mut else ''}{tag_extra}"))
            keys.append((g, sd))
    paths = run_many(jobs, nw, verbose=False)
    col = 1 if kind == "A" else 0
    ser = [load(p)[:, col] for p in paths]
    bet = [k[0] for k in keys]
    Np = 6.0 * L ** 4
    wh = Wham1D(ser, bet, Np, nblk=nblk)
    lr0 = wh.solve()
    taus = [tau_int(s) for s in ser]
    blen = len(ser[0]) // nblk
    infl = max(1.0, np.sqrt(5.0 * max(taus) / blen))
    lo, hi = min(grid), max(grid)
    pg = np.arange(lo, hi + 1e-9, fine / 10.0)

    def curve(lr):
        return np.array([Np * (lambda m: m[1] - m[0] ** 2)(wh.moments(b, lr)) for b in pg])
    c0 = curve(lr0)

    def maxima(c):
        out = []
        for i in range(1, len(pg) - 1):
            if c[i] >= c[i - 1] and c[i] > c[i + 1]:
                out.append(i)
        if c[0] > c[1]:
            out.append(0)
        if c[-1] > c[-2]:
            out.append(len(pg) - 1)
        return out
    mx = maxima(c0)
    # keep maxima that are at least 5% of the global max, merge those within one grid spacing
    gm = c0.max()
    mx = [i for i in mx if c0[i] >= 0.05 * gm]
    jk = []
    for j in range(nblk):
        lrj = wh.solve(drop=j)
        cj = curve(lrj)
        jk.append((cj, maxima(cj)))
    out = []
    for i in mx:
        x0 = pg[i]
        est = []
        for cj, mj in jk:
            if not mj:
                continue
            xs = np.array([pg[k] for k in mj])
            est.append(xs[np.argmin(np.abs(xs - x0))])
        e = (np.sqrt((len(est) - 1) / len(est) * np.sum((np.array(est) - np.mean(est)) ** 2)) * infl) if len(est) > 2 else float("nan")
        edge = (i == 0) or (i == len(pg) - 1) or (x0 < lo + 0.5 * (grid[1] - grid[0]) if len(grid) > 1 else False) or (x0 > hi - 0.5 * (grid[1] - grid[0]) if len(grid) > 1 else False)
        out.append(dict(x=float(x0), chi=float(c0[i]), err=float(e), edge=bool(edge)))
    # phase occupancy per run (threshold = midpoint of the pooled 5th and 95th percentiles of the conjugate observable)
    allv = np.concatenate(ser)
    thr = 0.5 * (np.percentile(allv, 5) + np.percentile(allv, 95))
    occ = [(float(k[0]), int(k[1]), float(np.mean(s > thr))) for k, s in zip(keys, ser)]
    nmixed = sum(1 for o in occ if 0.05 < o[2] < 0.95)
    return dict(maxima=out, tau_max=float(max(taus)), infl=float(infl), nruns=len(ser), L=L, fixed=fixed, kind=kind, thr=float(thr), occ=occ, nmixed=int(nmixed), curve=(pg.tolist(), c0.tolist()))


def hyst_map(group, L, bF_list, bA_list, nsw, nth, hits, mut=False, nw=12, nblk=10):
    """Stage 1H: hot- and cold-start runs on a grid; returns dict[(bF,bA)] = (XA_cold, err, XA_hot, err, XF_cold, XF_hot, flag)."""
    exe = build(group)
    jobs, keys = [], []
    for bF in bF_list:
        for bA in bA_list:
            for cold in (0, 1):
                seed = 4241 * L + 977 * cold + int(round(bF * 1000)) * 31 + int(round(bA * 1000)) * 17 + 5
                jobs.append((exe, nonab_args(group, L, bF, bA, nsw, nth, seed, cold, hits, mut), f"{group}h{'m' if mut else ''}"))
                keys.append((bF, bA, cold))
    paths = run_many(jobs, nw, verbose=False)
    dat = {}
    for k, p in zip(keys, paths):
        dat[k] = load(p)
    out = {}
    for bF in bF_list:
        for bA in bA_list:
            r = []
            for col in (1, 0):
                vals = []
                for cold in (1, 0):
                    s = dat[(bF, bA, cold)][:, col]
                    bl = np.array_split(s, nblk)
                    m = np.array([b.mean() for b in bl])
                    vals.append((s.mean(), m.std(ddof=1) / np.sqrt(nblk)))
                r.append(vals)
            (xa_c, ea_c), (xa_h, ea_h) = r[0]
            (xf_c, _), (xf_h, _) = r[1]
            d = abs(xa_c - xa_h)
            flag = bool(d > 5 * np.hypot(ea_c, ea_h) and d > 0.005)
            out[(bF, bA)] = (float(xa_c), float(ea_c), float(xa_h), float(ea_h), float(xf_c), float(xf_h), flag)
    return out
