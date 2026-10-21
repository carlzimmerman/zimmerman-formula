#!/usr/bin/env python3
"""CFG960 SCT-M structure-formation engine (FROZEN_CRITERIA.md, commit 6fc440225).

= the CFG654 engine (imported READ-ONLY from ../CFG654_independent_inputs by a path assembled in code; sha256 asserted) + the SCT-M
source sector of CFG953 (R0-R9), realised on the PM mesh as the frozen rules S1-S13 with the declared choices U1-U13:
  S1  rho_g = sum_i w_i W_CIC(x - x_i) + sum_q sigma_q (+ M3 re-placement); w_i = 1 unlabelled / pending, f_b converted (cold share inert)
  S2  domains born at census refreshes (every 10th force call) from cover_peaks (E3, native Delta_ta), r_ON >= dx, CFG647 partition,
      labelled-majority rule (new domain iff unlabelled > half of the peak's cells' particles), latched labels
  S3  pending particles convert at t_b + u_i tau, tau = free-fall time at turnaround, u_i = splitmix64(particle index)
  S4  conversion algebra: M_c += (1 - f_b) m_p, X -> mass-weighted mean, P += (1 - f_b) m_p v_i
  S5  own baryons = f_own of the domain's labelled particles, raised per partition peak (no RMIN); A5: f_own = census f_ret(M_ta)
      (CFG953's convention, = the baryons M3 keeps in place; primary) | M2's condensed fraction (CFG960_OWNB=cond; secondary)
  S6  monopole body M_sigma(<r) = min{(nu_mono(y) - 1) M_b(<r), M_c} about X_q, cut at the supply root r_e
  S7  quadrature points (equal-width shells, antipodal Fibonacci sets) + CIC; r_e <= dx/2 -> one point
  S8  M_c dV/dt = sum_points w g(x_p) with the particles' CIC-interpolated field and KDK factors
  S9  R7 merges at refreshes (bound fraction < 1/2 or baryon-centroid coalescence), inelastic, no blend
  S10 in situ: labelled-majority peaks give no body;  S11 labelled dust inert, still geodesic;  S12 M3 unchanged
  S13 spin and E_int not tracked; NR limit; no stripping
Usage:  python3 cfg960_sctm_pm.py MODE FOOT N
  MODE = SCT (production / validation)  |  S0REF (the CFG654 engine's own S0, reference control)
  env: CFG960_M3 (1|0), CFG960_CONVERT (1|0: 0 = the K test, births/labels/merges active, nothing converts),
       CFG960_MUTATE (none|mass: painted body mass x 0.5), CFG960_RSSMAX (GB, in-script guard), plus the CFG596_* settings of the
       CFG654 engine (CFG596_L, CFG596_NSEED, CFG596_RMIN, CFG596_THREADS, CFG596_WORK, CFG596_SPILL, CFG596_MAXSTEPS, CFG596_CKPT).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, math, json, time, hashlib, importlib.util, resource, threading

HERE = os.path.dirname(os.path.abspath(__file__))
CFGD = os.path.abspath(os.path.join(HERE, ".."))
EXT = os.path.abspath(os.path.join(CFGD, "..", "..", "_external_data"))
ENG_PATH = os.path.join(CFGD, "CFG654_independent_inputs", "cfg654" + "_pm.py")
ENG_SHA = "7058f4333b8d45970af932f889ba00aa1e67372cd2f04f21d2df1da471f631c6"

SWITCH = sys.argv[1] if (__name__ == "__main__" and len(sys.argv) > 1) else os.environ.get("CFG960_SWITCH", "SCT")
M3ON = os.environ.get("CFG960_M3", "1") == "1"
CONVERT = os.environ.get("CFG960_CONVERT", "1") == "1"
MUTATE = os.environ.get("CFG960_MUTATE", "none"); assert MUTATE in ("none", "mass")
MUT_FAC = 0.5 if MUTATE == "mass" else 1.0
OWNB = os.environ.get("CFG960_OWNB", "fret"); assert OWNB in ("fret", "cond")   # A5: own baryons = census f_ret (primary) | M2 condensed (secondary)
# switches of the imported CFG654 engine (read at its import): native CMB-pair inputs; class-A modules OFF except as stated
os.environ.setdefault("CFG654_INPUTS", "native_cmb")
os.environ.setdefault("CFG596_THREADS", "1")
os.environ.setdefault("CFG596_WORK", os.path.join(EXT, "cfg960_work", "manual"))
os.environ["CFG650_M1"] = "0"; os.environ["CFG650_M4"] = "0"; os.environ["CFG650_IC"] = "sigma8"
if SWITCH == "S0REF":                                   # exactly the NCS0 module set (MODS "")
    os.environ["CFG650_M2"] = "0"; os.environ["CFG650_M3"] = "0"
else:
    os.environ["CFG650_M2"] = "1"; os.environ["CFG650_M3"] = "1" if M3ON else "0"

_sha = hashlib.sha256(open(ENG_PATH, "rb").read()).hexdigest()
assert _sha == ENG_SHA, f"CFG654 engine changed: {_sha}"
_spec = importlib.util.spec_from_file_location("cfg654_engine", ENG_PATH)
E = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(E)
import numpy as np
from scipy.integrate import quad
assert E.INPUTS == os.environ["CFG654_INPUTS"]

RSSMAX = float(os.environ.get("CFG960_RSSMAX", "1.0"))
def _guard():
    while True:
        r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
        if r > RSSMAX:
            sys.stderr.write(f"CFG960 RSS GUARD: peak {r:.3f} GB > {RSSMAX} GB -> abort\n"); sys.stderr.flush(); os._exit(3)
        time.sleep(0.25)
threading.Thread(target=_guard, daemon=True).start()

NB_LOG = 48                                              # S6: 48 log edges dx/16 ... L/2 (+ inner bin from 0, + overflow bin)
GOLD = math.pi * (3.0 - math.sqrt(5.0))
NR_CAP, NA_CAP = 128, 20000                              # implementation safety caps (never expected to bind; counted and reported)

# ------------------------------------------------------------------------------------------------ small helpers
def mi(d):
    """minimal periodic image (box E.L)."""
    return d - E.L * np.round(d / E.L)
def splitmix_u(idx):
    """u in [0, 1) from the particle's global index (splitmix64; S3)."""
    with np.errstate(over="ignore"):
        z = idx.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        z = z ^ (z >> np.uint64(31))
    return (z >> np.uint64(11)).astype(np.float64) * (2.0 ** -53)
def radial_edges(dx):
    return np.concatenate([[0.0], np.geomspace(dx / 16.0, E.L / 2.0, NB_LOG)])
def bin_of(r, edges):
    """bin j covers [edges[j], edges[j+1]); bin len(edges)-1 = overflow [L/2, inf)."""
    return np.minimum(np.searchsorted(edges, r, side="right") - 1, len(edges) - 1)
def pos_idx(P, gidx):
    """lean-mode positions of particles with global indices gidx -> (n, 3) float64 (= Particles.positions for those rows)."""
    n = P.npg; out = np.empty((len(gidx), 3))
    ic = (gidx // (n * n), (gidx // n) % n, gidx % n)
    for c in range(3):
        out[:, c] = ((ic[c] + 0.5) * (E.L / n) + P.x[c][gidx]) % E.L
    return out
def decode(lab):
    return np.where(lab >= 0, lab, -lab - 2)

# ------------------------------------------------------------------------------------------------ cosmic time, Delta_ta, tau
_LA = np.linspace(math.log(1e-8), 0.0, 4001)
def _t_table():
    a = np.exp(_LA); t = np.zeros_like(a)
    t[0] = quad(lambda x: 1.0 / (x * E.E(x)), 0.0, a[0])[0]
    for i in range(1, len(a)):
        t[i] = t[i - 1] + quad(lambda x: 1.0 / (x * E.E(x)), a[i - 1], a[i], epsrel=1e-11)[0]
    return t
_TT = None
def t_of(a):
    global _TT
    if _TT is None: _TT = _t_table()
    return float(np.interp(math.log(a), _LA, _TT))
def delta_ta(a, dta):
    return math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))
def tau_ff(a, Dta):
    """free-fall time at turnaround (1/H0 units): sqrt(3 pi / (32 G rho_ta)), rho_ta = Delta_ta rho_m(a), G rho_m = 3 Om / (8 pi a^3)."""
    return 0.5 * math.pi * math.sqrt(a ** 3 / (E.Om * Dta))

# ------------------------------------------------------------------------------------------------ particle labels (S2/S3)
class PLab:
    """int32 per particle: -1 unlabelled; q >= 0 converted into domain q; v <= -2 pending for domain -v-2.  Disk-backed when SPILL."""
    def __init__(self, N):
        self.N = N; self.fd = None; self.arr = None
        if E.SPILL:
            d = os.path.join(E.WORK, "tmp"); os.makedirs(d, exist_ok=True)
            self.fn = os.path.join(d, f"lab_{os.getpid()}.bin")
            self.fd = os.open(self.fn, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o600); os.ftruncate(self.fd, 4 * N)
            E._nocache(self.fd)
            blk = np.full(1 << 22, -1, np.int32)
            for i in range(0, N, len(blk)): self.write(i, min(i + len(blk), N), blk[:min(len(blk), N - i)])
        else:
            self.arr = np.full(N, -1, np.int32)
    def read(self, i0, i1):
        if self.fd is None: return self.arr[i0:i1].copy()
        n = 4 * (i1 - i0); parts = []; got = 0
        while got < n:
            c = os.pread(self.fd, n - got, 4 * i0 + got); parts.append(c); got += len(c)
        return np.frombuffer(b"".join(parts), np.int32).copy()
    def write(self, i0, i1, x):
        if self.fd is None: self.arr[i0:i1] = x; return
        mv = memoryview(np.ascontiguousarray(x, np.int32)).cast("B"); o = 0
        while o < len(mv): o += os.pwrite(self.fd, mv[o:], 4 * i0 + o)
    def close(self):
        if self.fd is not None: os.close(self.fd); os.remove(self.fn); self.fd = None

# ------------------------------------------------------------------------------------------------ domain table
class Dom:
    F = ("tb", "ab", "tau", "ron", "Mc", "Mb_last")
    def __init__(self):
        self.n = 0; cap = 1024
        self.d = {k: np.zeros(cap) for k in self.F}
        self.bpos = np.zeros((cap, 3)); self.X = np.zeros((cap, 3)); self.V = np.zeros((cap, 3))
        self.root = np.zeros(cap, np.int64); self.born_step = np.zeros(cap, np.int64)
        self.n_merged = 0
    def _grow(self, need):
        cap = len(self.root)
        if need <= cap: return
        nc = max(need, 2 * cap)
        for k in self.F: self.d[k] = np.concatenate([self.d[k], np.zeros(nc - cap)])
        for k in ("bpos", "X", "V"): setattr(self, k, np.concatenate([getattr(self, k), np.zeros((nc - cap, 3))]))
        self.root = np.concatenate([self.root, np.zeros(nc - cap, np.int64)]); self.born_step = np.concatenate([self.born_step, np.zeros(nc - cap, np.int64)])
    def add(self, n, tb, ab, tau, bpos, ron, step):
        i0 = self.n; self._grow(i0 + n); ids = np.arange(i0, i0 + n)
        self.d["tb"][ids] = tb; self.d["ab"][ids] = ab; self.d["tau"][ids] = tau; self.d["ron"][ids] = ron
        self.bpos[ids] = bpos; self.X[ids] = bpos; self.root[ids] = ids; self.born_step[ids] = step; self.n = i0 + n
        return ids
    def roots(self):
        r = self.root[:self.n].copy()
        while True:
            r2 = r[r]
            if np.array_equal(r2, r): return r
            r = r2
    def compress(self):
        self.root[:self.n] = self.roots()
    @property
    def Mc(self): return self.d["Mc"]
    def xref(self):
        """reference centre per id: the body centroid once it has mass, the birth peak before."""
        n = self.n; return np.where((self.Mc[:n] > 0)[:, None], self.X[:n], self.bpos[:n])
    def state(self):
        s = {k: self.d[k][:self.n] for k in self.F}
        s.update(bpos=self.bpos[:self.n], X=self.X[:self.n], V=self.V[:self.n], root=self.root[:self.n], born_step=self.born_step[:self.n],
                 n=np.array(self.n), n_merged=np.array(self.n_merged))
        return s
    def load(self, s):
        n = int(s["n"]); self.n = 0; self._grow(n); self.n = n
        for k in self.F: self.d[k][:n] = s[k]
        self.bpos[:n] = s["bpos"]; self.X[:n] = s["X"]; self.V[:n] = s["V"]; self.root[:n] = s["root"]; self.born_step[:n] = s["born_step"]
        self.n_merged = int(s["n_merged"])

def apply_conversions(dom, q, d, mom, m, acc):
    """accumulate S4 conversion sums for root ids q (d = minimal-image offsets from the root's reference centre, mom (n, 3))."""
    nd = dom.n
    acc["dm"] = acc.get("dm", np.zeros(nd)); acc["dmx"] = acc.get("dmx", np.zeros((nd, 3))); acc["dmv"] = acc.get("dmv", np.zeros((nd, 3)))
    for k in ("dm", "dmx", "dmv"):
        if len(acc[k]) < nd: acc[k] = np.concatenate([acc[k], np.zeros((nd - len(acc[k]),) + acc[k].shape[1:])])
    acc["dm"] += np.bincount(q, minlength=nd) * m
    for c in range(3):
        acc["dmx"][:, c] += np.bincount(q, weights=d[:, c], minlength=nd) * m
        acc["dmv"][:, c] += np.bincount(q, weights=mom[:, c], minlength=nd) * m
    acc["book_dp"] = acc.get("book_dp", np.zeros(3)) - m * mom.sum(0)
    acc["n"] = acc.get("n", 0) + len(q)
def finish_conversions(dom, acc, xref):
    """S4: M_c += dm; X -> xref + (M_c (X - xref) + dmx)/(M_c + dm); P += dmv.  Returns the event momentum residual vector."""
    if not acc.get("n"): return np.zeros(3)
    nd = dom.n; dm = acc["dm"][:nd]; k = np.nonzero(dm > 0)[0]
    Mc0 = dom.Mc[k].copy(); P0 = (Mc0[:, None] * dom.V[k]).sum(0)
    rel = mi(dom.X[k] - xref[k]) * Mc0[:, None]
    Mn = Mc0 + dm[k]
    dom.X[k] = (xref[k] + (rel + acc["dmx"][k]) / Mn[:, None]) % E.L
    dom.V[k] = (Mc0[:, None] * dom.V[k] + acc["dmv"][k]) / Mn[:, None]
    dom.d["Mc"][k] = Mn
    P1 = (Mn[:, None] * dom.V[k]).sum(0)
    return (P1 - P0) + acc["book_dp"]

# ------------------------------------------------------------------------------------------------ S2: partition (CFG647 rule, floor dx)
def partition_labels(mesh, peaks):
    """= the engine's own_host_labels with the selection floor r_ON >= dx instead of RMIN (every turned-around peak)."""
    M, dx = mesh.M, mesh.dx
    idx, ron, Rg = peaks
    sel = np.nonzero(ron >= dx * (1 - 1e-9))[0]
    C = idx[sel].astype(np.int64); R = ron[sel].astype(np.float64)
    lab = np.full((M, M, M), -1, np.int32); oc = {}
    for h in range(len(sel)):
        c, rb = C[h], R[h]
        if rb < 0.5 * dx:
            G = np.zeros((1, 3), np.int64); d = np.zeros(1)
        else:
            key = round(rb, 9)
            if key not in oc:
                n = int(math.floor(rb / dx)) + 1; g = np.arange(-n, n + 1)
                GG = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1).reshape(-1, 3)
                d2 = ((GG * dx) ** 2).sum(1); k = d2 <= rb * rb
                oc[key] = (GG[k], np.sqrt(d2[k]))
            G, d = oc[key]
        Pc = (G + c[None, :]) % M
        cur = lab[Pc[:, 0], Pc[:, 1], Pc[:, 2]]
        sc_new = d / rb - 1e-9 * rb
        upd = cur < 0; has = ~upd
        if has.any():
            ch = cur[has]; dd = (Pc[has] - C[ch]) % M; dd = np.minimum(dd, M - dd) * dx
            upd[has] = sc_new[has] < np.sqrt((dd ** 2).sum(1)) / R[ch] - 1e-9 * R[ch]
        lab[Pc[upd, 0], Pc[upd, 1], Pc[upd, 2]] = h
    D = E.DField("host960", M, np.int32); D.write_all(lab)
    if E.SPILL: del lab
    return D, C, R

def host_of_chunk(mesh, P, hostD, i0, i1):
    pos = P.positions(i0, i1); g = np.floor(pos / mesh.dx + 0.5).astype(np.int64) % mesh.M
    return pos, np.asarray(E._gather_window(mesh, hostD, g, i0)).astype(np.int64)

# ------------------------------------------------------------------------------------------------ S6/S7: body shape and points
class Law:
    """y(r) = Cy M_b(<r)/r^2 in the engine's code units; M_ph = (nu_mono(y) - 1) M_b."""
    def __init__(self, a, foot, N):
        self.Cy = (1.5 * E.Om / a ** 2) * (E.L ** 3 / N) / (4.0 * math.pi * E.a0_code(a, "FLAT", foot))
    def mph(self, s, Mb):
        y = self.Cy * Mb / np.maximum(s, 1e-300) ** 2
        return np.where(Mb > 0, (E.nu_mono(y) - 1.0) * Mb, 0.0)
def mb_at(s, cum, bins, edges):
    """M_b(<s) for rows (n, NB) at radii s (n,) or (n, m): linear in r^3 inside a bin; overflow = everything beyond L/2."""
    nb = bins.shape[1]; s = np.asarray(s, float); twod = s.ndim == 2; S = s if twod else s[:, None]
    j = np.minimum(np.searchsorted(edges, S, side="right") - 1, nb - 1)
    rows = np.arange(bins.shape[0])[:, None]
    lo = edges[np.minimum(j, len(edges) - 1)]; hi = edges[np.minimum(j + 1, len(edges) - 1)]
    frac = np.where(j < nb - 1, (S ** 3 - lo ** 3) / np.maximum(hi ** 3 - lo ** 3, 1e-300), 0.0)
    out = cum[rows, j] + bins[rows, j] * np.clip(frac, 0.0, 1.0)
    return out if twod else out[:, 0]
_ANG = {}
def ang_set(na):
    if na not in _ANG:
        h = na // 2; i = np.arange(h); z = (i + 0.5) / h; rr = np.sqrt(1 - z * z); ph = i * GOLD
        v = np.stack([rr * np.cos(ph), rr * np.sin(ph), z], 1); _ANG[na] = np.concatenate([v, -v])
    return _ANG[na]
R_IN = 4.0                                               # A3/A4: CIC points inside 4 dx (all of the body if r_e <= 5 dx); mesh nodes beyond
def body_points(prof, Mc, X, law, edges, dx, M, mut=1.0):
    """S6/S7 (+ A3). prof (nb, NB) own-retained-baryon mass per bin about X; Mc (nb,).  Returns a dict with the inner CIC points
    (pos (n, 3), w, own) and the outer mesh nodes (cidx flat node index (i*M + j)*M + k, cw, cown), the diagnostics and r_e (nb,)."""
    nb = len(Mc); dg = dict(n_bodies=int(nb), n_point=0, n_fallback=0, n_nobaryon=0, n_cap=0, n_outer=0, re_dx=[])
    out = dict(pos=np.zeros((0, 3)), w=np.zeros(0), own=np.zeros(0, np.int64), cidx=np.zeros(0, np.int64), cw=np.zeros(0), cown=np.zeros(0, np.int64))
    if nb == 0: return out, dg, np.zeros(0)
    cum = np.concatenate([np.zeros((nb, 1)), np.cumsum(prof, 1)[:, :-1]], 1)
    Mtot = prof.sum(1)
    re = np.full(nb, np.nan)
    s_half = np.full(nb, 0.5 * dx)
    m_half = law.mph(s_half, mb_at(s_half, cum, prof, edges))
    point = (m_half >= Mc) | (Mtot <= 0)
    dg["n_nobaryon"] = int((Mtot <= 0).sum())
    pos_l, w_l, own_l = [X[point]], [Mc[point] * mut], [np.nonzero(point)[0]]
    ci_l, cw_l, co_l = [], [], []
    dg["n_point"] = int(point.sum())
    re[point & (Mtot > 0)] = 0.5 * dx                                 # upper bound for point bodies (reported as <= dx/2)
    rest = np.nonzero(~point)[0]
    rcap = min(E.L / 4.0, 128.0 * dx)
    if len(rest):
        fe = edges[1:]                                                # finite edges dx/16 ... L/2
        me = law.mph(np.broadcast_to(fe, (len(rest), len(fe))), mb_at(np.broadcast_to(fe, (len(rest), len(fe))), cum[rest], prof[rest], edges))
        ok = me >= Mc[rest][:, None]
        has = ok.any(1)
        jfirst = np.where(has, ok.argmax(1), len(fe) - 1)
        hi = np.where(has, fe[jfirst], E.L / 2.0)
        lo = np.where(jfirst > 0, fe[np.maximum(jfirst - 1, 0)], 0.5 * dx); lo = np.maximum(lo, 0.5 * dx)
        lo = np.minimum(lo, hi)
        for _ in range(80):                                           # bisection on the monotone supply function (S6, rel tol << 1e-10)
            mid = 0.5 * (lo + hi)
            mm = law.mph(mid, mb_at(mid, cum[rest], prof[rest], edges)) >= Mc[rest]
            hi = np.where(mm & has, mid, hi); lo = np.where(mm & has, lo, mid)
        rr = np.where(has, hi, E.L / 2.0); re[rest] = rr
        dg["n_fallback"] = int((~has).sum())
        for t, q in enumerate(rest):
            rp = min(rr[t], rcap)
            if rr[t] > rcap: dg["n_cap"] += 1
            rin = rp if rp <= (R_IN + 1.0) * dx else R_IN * dx       # A4: outer nodes only when the outer region is >= 1 dx thick
            def msig(sv):
                return np.minimum(np.maximum.accumulate(law.mph(sv, mb_at(sv[None, :], cum[q:q + 1], prof[q:q + 1], edges)[0])), Mc[q])
            # inner part: S7 as frozen on [0, r_in]
            nr = int(math.ceil(2.0 * rin / dx)); sgrid = rin * np.arange(nr + 1) / nr
            ms = msig(sgrid[1:])
            if rp <= rin: ms[-1] = Mc[q]
            dM = np.diff(np.concatenate([[0.0], ms]))
            rb = 0.5 * (sgrid[1:] + sgrid[:-1])
            for k in range(nr):
                if dM[k] <= 0: continue
                na = max(6, 2 * int(math.ceil(8.0 * math.pi * rb[k] ** 2 / dx ** 2)))
                if na > NA_CAP: na = NA_CAP; dg["n_cap"] += 1
                v = ang_set(na); th = k * GOLD; ct, st = math.cos(th), math.sin(th)
                vr = np.stack([v[:, 0] * ct - v[:, 1] * st, v[:, 0] * st + v[:, 1] * ct, v[:, 2]], 1)
                pos_l.append(X[q][None, :] + rb[k] * vr); w_l.append(np.full(na, dM[k] / na) * mut); own_l.append(np.full(na, q))
            if rp <= rin: continue
            # outer part (A3): radial shells of width <= dx/2 on (r_in, r_p], each shell's mass shared equally by its mesh nodes
            dg["n_outer"] += 1
            no = int(math.ceil(2.0 * (rp - rin) / dx)); so = rin + (rp - rin) * np.arange(no + 1) / no
            mo = msig(so); mo[0] = ms[-1]; mo[-1] = Mc[q]; mo = np.maximum.accumulate(mo); dMo = np.diff(mo)
            lo3 = np.floor((X[q] - rp) / dx).astype(np.int64); hi3 = np.ceil((X[q] + rp) / dx).astype(np.int64)
            gx, gy, gz = [np.arange(lo3[c], hi3[c] + 1) for c in range(3)]
            ddx, ddy, ddz = gx * dx - X[q][0], gy * dx - X[q][1], gz * dx - X[q][2]
            r3 = np.sqrt(ddx[:, None, None] ** 2 + ddy[None, :, None] ** 2 + ddz[None, None, :] ** 2)
            sel = (r3 > rin) & (r3 <= rp)
            ii, jj, kk = np.nonzero(sel); rs = r3[ii, jj, kk]
            ks = np.clip(((rs - rin) / (rp - rin) * no).astype(np.int64), 0, no - 1)
            cnt = np.bincount(ks, minlength=no)
            if cnt.sum() == 0:                                         # A4 fallback: no node at all -> one CIC point shell at the mid radius
                rm = 0.5 * (rin + rp); na = max(6, 2 * int(math.ceil(8.0 * math.pi * rm ** 2 / dx ** 2)))
                pos_l.append(X[q][None, :] + rm * ang_set(na)); w_l.append(np.full(na, dMo.sum() / na) * mut); own_l.append(np.full(na, q))
                dg["n_node_fallback"] = dg.get("n_node_fallback", 0) + 1
                continue
            if (cnt[dMo > 0] == 0).any():                              # an empty shell: its mass goes to the nearest filled shell
                fill = np.nonzero(cnt > 0)[0]
                for k in np.nonzero((cnt == 0) & (dMo > 0))[0]:
                    j_ = fill[np.argmin(np.abs(fill - k))]; dMo[j_] += dMo[k]; dMo[k] = 0.0
            wn = dMo[ks] / np.maximum(cnt[ks], 1)
            ci_l.append((((gx[ii] % M) * M + (gy[jj] % M)) * M + (gz[kk] % M)).astype(np.int64)); cw_l.append(wn * mut); co_l.append(np.full(len(ii), q))
    dg["re_dx"] = (re[np.isfinite(re)] / dx)
    out["pos"] = np.concatenate(pos_l) % E.L; out["w"] = np.concatenate(w_l); out["own"] = np.concatenate(own_l).astype(np.int64)
    if ci_l:
        out["cidx"] = np.concatenate(ci_l); out["cw"] = np.concatenate(cw_l); out["cown"] = np.concatenate(co_l).astype(np.int64)
    return out, dg, re

def deposit_points(rho, mesh, pos, w):
    """CIC of weighted points into rho (M, M*M) float64 (the particles' CIC, mesh.cic_idx)."""
    if len(w) == 0: return
    M = mesh.M; i0, i1, wc = mesh.cic_idx(pos); flat = rho.reshape(-1)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = wc[:, 0] if cx else 1 - wc[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = wc[:, 1] if cy else 1 - wc[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = wc[:, 2] if cz else 1 - wc[:, 2]
                np.add.at(flat, (ix * M + iy) * M + iz, (wx * wy * wz).astype(np.float64) * w)

def deposit_converted(rho, mesh, P, PL, wt):
    """windowed CIC (as the engine's deposit_w) of the CONVERTED particles with weight wt, accumulated into rho (M, M*M) float64."""
    M = mesh.M; E.stage("xdep")
    for a_, b_ in P.chunks:
        lab = PL.read(a_, b_); sel = lab >= 0
        if not sel.any(): continue
        pos = P.positions(a_, b_)[sel]; i0, i1, w = mesh.cic_idx(pos); del pos
        lag0 = (a_ // (M * M)) % M; x0 = (lag0 - M // 4) % M
        s0 = (i0[:, 0] - x0) % M; s1 = (i1[:, 0] - x0) % M
        lo = int(min(s0.min(), s1.min())); hi = int(max(s0.max(), s1.max())); Wn = hi - lo + 1
        idx = []; wts = []
        for cx in (0, 1):
            ix = (s1 if cx else s0) - lo; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    idx.append((ix * M + iy) * M + iz); wts.append((wx * wy * wz).astype(np.float64) * wt)
        idx = np.concatenate(idx); wts = np.concatenate(wts)
        acc = np.bincount(idx, weights=wts, minlength=Wn * M * M).reshape(Wn, M * M); del idx, wts
        start = (x0 + lo) % M; n1 = min(Wn, M - start)
        rho[start:start + n1] += acc[:n1]
        if n1 < Wn: rho[:Wn - n1] += acc[n1:]
        del acc

# ------------------------------------------------------------------------------------------------ passes over the particles
def pass_conversions(P, PL, dom, t_now):
    """S3/S4: pending particles whose conversion time has come convert into their root domain."""
    acc = {}; E.stage("convert")
    if not CONVERT or dom.n == 0: return 0, np.zeros(3)
    roots = dom.roots(); xref = dom.xref(); tb, tau = dom.d["tb"][:dom.n], dom.d["tau"][:dom.n]
    m = 1.0 - E.FB
    for i0, i1 in P.chunks:
        lab = PL.read(i0, i1); pend = np.nonzero(lab <= -2)[0]
        if not len(pend): continue
        q0 = -lab[pend] - 2; gi = i0 + pend.astype(np.int64)
        due = tb[q0] + splitmix_u(gi) * tau[q0] <= t_now
        if not due.any(): continue
        pend = pend[due]; q = roots[q0[due]]; gi = gi[due]
        pos = pos_idx(P, gi); d = mi(pos - xref[q])
        mom = np.stack([P.mom[c][gi].astype(np.float64) for c in range(3)], 1)
        apply_conversions(dom, q, d, mom, m, acc)
        lab[pend] = q.astype(np.int32); PL.write(i0, i1, lab)
    dp = finish_conversions(dom, acc, xref)
    return int(acc.get("n", 0)), dp

def pass_profiles(P, PL, dom, edges):
    """S6 profiles: own retained baryons f_b f_d per radial bin about X_q for every live root with M_c > 0; + the mass/momentum book."""
    nd = dom.n; NB = len(edges); E.stage("profile")
    roots = dom.roots() if nd else np.zeros(0, np.int64)
    alive = (roots == np.arange(nd)) & (dom.Mc[:nd] > 0) if nd else np.zeros(0, bool)
    bid = np.nonzero(alive)[0]; cidx = np.full(max(nd, 1), -1, np.int64); cidx[bid] = np.arange(len(bid))
    prof = np.zeros(len(bid) * NB)
    book = dict(P=np.zeros(3), Pabs=0.0, M=0.0, n_conv=0, n_pend=0, n_lab=0)
    for i0, i1 in P.chunks:
        lab = PL.read(i0, i1)
        w = np.where(lab >= 0, E.FB, 1.0)
        mom = [P.mom[c][i0:i1].astype(np.float64) for c in range(3)]
        for c in range(3): book["P"][c] += float((w * mom[c]).sum())
        book["Pabs"] += float((w * np.sqrt(mom[0] ** 2 + mom[1] ** 2 + mom[2] ** 2)).sum()); book["M"] += float(w.sum())
        book["n_conv"] += int((lab >= 0).sum()); book["n_pend"] += int((lab <= -2).sum())
        lb = np.nonzero(lab != -1)[0]; book["n_lab"] += len(lb)
        if not len(lb) or not len(bid): continue
        q = roots[decode(lab[lb])]; ci = cidx[q]; s = ci >= 0
        if not s.any(): continue
        lb = lb[s]; q = q[s]; ci = ci[s]; gi = i0 + lb.astype(np.int64)
        r = np.sqrt((mi(pos_idx(P, gi) - dom.X[q]) ** 2).sum(1))
        f = E.FB * P.fd[gi].astype(np.float64)
        prof += np.bincount(ci * NB + bin_of(r, edges), weights=f, minlength=len(bid) * NB)
    Vb = dom.V[bid]; Mcb = dom.Mc[bid]
    book["P"] = book["P"] + (Mcb[:, None] * Vb).sum(0); book["Pabs"] += float((Mcb * np.sqrt((Vb ** 2).sum(1))).sum())
    book["Mc"] = float(dom.Mc[:nd].sum()) if nd else 0.0
    return bid, prof.reshape(len(bid), NB), book

# ------------------------------------------------------------------------------------------------ S2: refresh (births, accretion, f_d)
def refresh(mesh, P, PL, dom, peaks, a, t_now, Dta, foot, step):
    info = dict(n_peaks=0, n_births=0, n_accrete_peaks=0, n_insitu_peaks=0, n_accreted=0, n_pend_new=0)
    if peaks is None or dom is None: return info, None
    E.stage("partition"); hostD, C, R = partition_labels(mesh, peaks); nh = len(R); info["n_peaks"] = int(nh); E.stage("refresh_pass")
    if nh == 0: hostD.close(); return info, None
    nd = dom.n; roots = dom.roots() if nd else np.zeros(0, np.int64)
    T = np.zeros(nh, np.int64); U = np.zeros(nh, np.int64); KK = []; CC = []
    for i0, i1 in P.chunks:
        _, h = host_of_chunk(mesh, P, hostD, i0, i1); lab = PL.read(i0, i1)
        inh = h >= 0
        if not inh.any(): continue
        T += np.bincount(h[inh], minlength=nh); un = inh & (lab == -1); U += np.bincount(h[un], minlength=nh)
        lb = inh & (lab != -1)
        if lb.any() and nd:
            k = h[lb] * max(nd, 1) + roots[decode(lab[lb])]
            uk, ck = np.unique(k, return_counts=True); KK.append(uk); CC.append(ck)
    birth = (T > 0) & (2 * U > T)
    dom_h = np.full(nh, -1, np.int64)
    if KK:
        K = np.concatenate(KK); Cn = np.concatenate(CC); o = np.argsort(K, kind="stable"); K = K[o]; Cn = Cn[o]
        st = np.r_[0, np.nonzero(np.diff(K))[0] + 1]; Ku = K[st]; Cs = np.add.reduceat(Cn, st)
        hh = Ku // max(nd, 1); qq = Ku % max(nd, 1)
        o2 = np.lexsort((-Cs, hh)); hh, qq = hh[o2], qq[o2]
        first = np.r_[True, hh[1:] != hh[:-1]]
        dom_h[hh[first]] = qq[first]
    dom_h[birth] = -1
    info["n_insitu_peaks"] = int(((~birth) & (dom_h >= 0)).sum())
    nb_ = int(birth.sum()); info["n_births"] = nb_
    if nb_:
        ids = dom.add(nb_, t_now, a, tau_ff(a, Dta), C[birth] * mesh.dx, R[birth], step); dom_h[birth] = ids
    info["n_accrete_peaks"] = int(((~birth) & (dom_h >= 0) & (U > 0)).sum())
    roots = dom.roots(); xref = dom.xref()
    Ru, inv = np.unique(R, return_inverse=True)
    if OWNB == "fret":                                              # A5 primary: CFG953 census retained fraction (M3's fret_of / M_ta)
        fct = np.array([E.fret_of(math.log10(E.M_ta(float(r_), Dta))) for r_ in Ru])[inv]
    else:                                                           # secondary: M2 condensed fraction (FROZEN_CRITERIA.md U5)
        fct = np.array([E.fcond_of(float(r_), Dta, a, "FLAT", foot) for r_ in Ru])[inv]
    f16 = fct.astype(np.float32).astype(np.float16)
    acc = {}; m = 1.0 - E.FB
    for i0, i1 in P.chunks:
        pos, h = host_of_chunk(mesh, P, hostD, i0, i1)
        inh = np.nonzero(h >= 0)[0]
        if not len(inh): continue
        gi = i0 + inh
        P.fd[gi] = np.maximum(P.fd[gi], f16[h[inh]])                  # S5 (A5): own retained fraction per partition peak (irreversible)
        lab = PL.read(i0, i1); un = inh[lab[inh] == -1]
        if not len(un): continue
        hb = h[un]; tgt = dom_h[hb]; ok = tgt >= 0; un, hb, tgt = un[ok], hb[ok], tgt[ok]
        bm = birth[hb]
        lab[un[bm]] = (-(tgt[bm] + 2)).astype(np.int32); info["n_pend_new"] += int(bm.sum())
        ac = ~bm
        if ac.any():
            ua = un[ac]; qa = roots[tgt[ac]]
            if CONVERT:
                gi2 = i0 + ua.astype(np.int64); d = mi(pos[ua] - xref[qa])
                mom = np.stack([P.mom[c][gi2].astype(np.float64) for c in range(3)], 1)
                apply_conversions(dom, qa, d, mom, m, acc); lab[ua] = qa.astype(np.int32)
            else:
                lab[ua] = (-(qa + 2)).astype(np.int32)
            info["n_accreted"] += int(ac.sum())
        PL.write(i0, i1, lab)
    dp = finish_conversions(dom, acc, xref)
    info["event_dP"] = dp.tolist()
    hostD.close()
    return info, dict(C=C, R=R, dom_h=dom_h)

# ------------------------------------------------------------------------------------------------ S9: merges (R7)
def merges(mesh, P, PL, dom, pk, bid, prof, law, edges, a):
    info = dict(n_pairs=0, n_merge_bound=0, n_merge_coal=0)
    if pk is None or dom.n == 0: return info, np.zeros(3)
    nd = dom.n; NB = len(edges); roots = dom.roots(); xref = dom.xref(); E.stage("merge")
    alive = roots == np.arange(nd)
    S0 = np.zeros(nd); S1 = np.zeros((nd, 3)); S2 = np.zeros((nd, 3))
    for i0, i1 in P.chunks:
        lab = PL.read(i0, i1); lb = np.nonzero(lab != -1)[0]
        if not len(lb): continue
        gi = i0 + lb.astype(np.int64); q = roots[decode(lab[lb])]; f = E.FB * P.fd[gi].astype(np.float64)
        d = mi(pos_idx(P, gi) - xref[q]); S0 += np.bincount(q, weights=f, minlength=nd)
        for c in range(3):
            S1[:, c] += np.bincount(q, weights=f * d[:, c], minlength=nd)
            S2[:, c] += np.bincount(q, weights=f * P.mom[c][gi].astype(np.float64), minlength=nd)
    has = alive & (S0 > 0); hid = np.nonzero(has)[0]
    if not len(hid): return info, np.zeros(3)
    Xb = np.zeros((nd, 3)); Vb = np.zeros((nd, 3))
    Xb[hid] = (xref[hid] + S1[hid] / S0[hid, None]) % E.L; Vb[hid] = S2[hid] / S0[hid, None]
    cid = np.full(nd, -1, np.int64); cid[hid] = np.arange(len(hid)); nh_ = len(hid)
    pA = np.zeros(nh_ * NB); pB = np.zeros(nh_ * NB)
    for i0, i1 in P.chunks:
        lab = PL.read(i0, i1); lb = np.nonzero(lab != -1)[0]
        if not len(lb): continue
        gi = i0 + lb.astype(np.int64); q = roots[decode(lab[lb])]; ci = cid[q]; s = ci >= 0
        gi, q, ci, lbs = gi[s], q[s], ci[s], lab[lb][s]
        r = np.sqrt((mi(pos_idx(P, gi) - Xb[q]) ** 2).sum(1)); b = ci * NB + bin_of(r, edges)
        pA += np.bincount(b, weights=E.FB * P.fd[gi].astype(np.float64), minlength=nh_ * NB)
        pB += np.bincount(b, weights=np.where(lbs >= 0, E.FB, 1.0), minlength=nh_ * NB)
    pA = pA.reshape(nh_, NB); pB = pB.reshape(nh_, NB)
    fe = edges[1:]
    cumA = np.cumsum(pA, 1); tot = cumA[:, -1]
    # half-mass radius about X_b (linear in r^3 inside the crossing bin)
    rh = np.zeros(nh_)
    for t in range(nh_):
        j = int(np.searchsorted(cumA[t], 0.5 * tot[t]))
        lo_e = edges[j] if j < len(edges) else E.L / 2; hi_e = edges[j + 1] if j + 1 < len(edges) else E.L / 2
        prev = cumA[t, j - 1] if j > 0 else 0.0; bj = pA[t, j] if j < NB else 0.0
        fr = (0.5 * tot[t] - prev) / bj if bj > 0 else 0.0
        rh[t] = (lo_e ** 3 + fr * (hi_e ** 3 - lo_e ** 3)) ** (1 / 3) if hi_e > lo_e else lo_e
    # own gravitating mass enclosed at the finite edges: particles (B) + body M_sigma (from the S6 profile about X_q)
    cumB_e = np.cumsum(pB, 1)[:, :-1]                               # mass below edges[1..NB-1]
    Ms_e = np.zeros((nh_, len(fe)))
    if len(bid):
        bpos = np.full(nd, -1, np.int64); bpos[bid] = np.arange(len(bid)); bb = bpos[hid]; sb = np.nonzero(bb >= 0)[0]
        if len(sb):
            pr = prof[bb[sb]]; cum = np.concatenate([np.zeros((len(sb), 1)), np.cumsum(pr, 1)[:, :-1]], 1)
            FE = np.broadcast_to(fe, (len(sb), len(fe)))
            Ms_e[sb] = np.minimum(law.mph(FE, mb_at(FE, cum, pr, edges)), dom.Mc[hid[sb]][:, None])
    Menc = cumB_e + Ms_e; Mall = pB.sum(1) + dom.Mc[hid]
    Cg = (1.5 * E.Om / a ** 2) * (E.L ** 3 / P.N) / (4.0 * math.pi)
    g = Cg * Menc / fe[None, :] ** 2
    Phi = np.zeros_like(g); Phi[:, -1] = -a * Cg * Mall / fe[-1]
    for j in range(len(fe) - 2, -1, -1):
        Phi[:, j] = Phi[:, j + 1] - a * 0.5 * (g[:, j] + g[:, j + 1]) * (fe[j + 1] - fe[j])
    Ea = E.E(a); Sb = np.zeros(nh_)
    for i0, i1 in P.chunks:
        lab = PL.read(i0, i1); lb = np.nonzero(lab != -1)[0]
        if not len(lb): continue
        gi = i0 + lb.astype(np.int64); q = roots[decode(lab[lb])]; ci = cid[q]; s = ci >= 0
        gi, q, ci = gi[s], q[s], ci[s]
        d = mi(pos_idx(P, gi) - Xb[q]); r = np.sqrt((d ** 2).sum(1))
        v2 = np.zeros(len(gi))
        for c in range(3): v2 += ((P.mom[c][gi].astype(np.float64) - Vb[q, c]) / a + Ea * a * d[:, c]) ** 2
        j = np.clip(np.searchsorted(fe, r) - 1, 0, len(fe) - 2)
        t_ = np.clip((r - fe[j]) / (fe[j + 1] - fe[j]), 0.0, 1.0)
        ph = Phi[ci, j] * (1 - t_) + Phi[ci, j + 1] * t_
        ph = np.where(r < fe[0], Phi[ci, 0], np.where(r > fe[-1], -a * Cg * Mall[ci] / np.maximum(r, 1e-300), ph))
        Sb += np.bincount(ci, weights=E.FB * P.fd[gi].astype(np.float64) * ((0.5 * v2 + ph) < 0), minlength=nh_)
    fb_ = Sb / np.maximum(S0[hid], 1e-300)
    # host(p): the domain of the largest-r_ON peak (not p's own) whose ball contains X_b,p (periodic KD trees per r_ON class)
    from scipy.spatial import cKDTree
    C, R, dom_h = pk["C"], pk["R"], pk["dom_h"]; okp = dom_h >= 0
    hroot = np.full(len(R), -1, np.int64); hroot[okp] = roots[dom_h[okp]]
    host = np.full(nh_, -1, np.int64); Xq = Xb[hid] % E.L
    for Rv in np.unique(R[okp])[::-1]:
        g_ = np.nonzero(okp & (np.abs(R - Rv) < 1e-12))[0]
        need = np.nonzero(host < 0)[0]
        if not len(need): break
        tree = cKDTree((C[g_] * mesh.dx) % E.L, boxsize=E.L)
        lists = tree.query_ball_point(Xq[need], r=Rv)
        for t, li in zip(need, lists):
            cand = [hroot[g_[x]] for x in li if hroot[g_[x]] != hid[t]]
            if cand: host[t] = cand[0]
    # merge decisions: smaller s into larger l (by own retained baryons), f_bound,s < 1/2 or |X_b,s - X_b,l| <= r_h,l
    Mb = S0.copy(); P0 = (dom.Mc[:nd, None] * dom.V[:nd]).sum(0)
    order = np.argsort(S0[hid]); grown = set()
    for t in order:
        p = int(hid[t]); h_ = host[t]
        if h_ < 0 or _root(dom, p) != p: continue                     # p already absorbed in this refresh
        rh_ = _root(dom, int(h_))
        if rh_ == p: continue
        s_, l_ = (p, rh_) if Mb[p] <= Mb[rh_] else (rh_, p)
        if s_ in grown or cid[s_] < 0 or cid[l_] < 0: continue        # stale statistics: decided at the next refresh
        info["n_pairs"] += 1
        cs, cl = cid[s_], cid[l_]
        bound = fb_[cs] < 0.5; coal = math.sqrt(float((mi(Xb[s_] - Xb[l_]) ** 2).sum())) <= rh[cl]
        if not (bound or coal): continue
        if bound: info["n_merge_bound"] += 1
        else: info["n_merge_coal"] += 1
        Ms, Ml = dom.Mc[s_], dom.Mc[l_]
        if Ms + Ml > 0:
            dom.X[l_] = (dom.X[l_] + Ms * mi(dom.X[s_] - dom.X[l_]) / (Ms + Ml)) % E.L if Ml > 0 else dom.X[s_].copy()
            dom.V[l_] = (Ml * dom.V[l_] + Ms * dom.V[s_]) / (Ms + Ml)
        dom.d["Mc"][l_] = Ms + Ml; dom.d["Mc"][s_] = 0.0; dom.V[s_] = 0.0
        dom.root[s_] = l_; Mb[l_] += Mb[s_]; grown.add(l_); dom.n_merged += 1
    dom.compress()
    P1 = (dom.Mc[:nd, None] * dom.V[:nd]).sum(0)
    info.update(f_bound_median=float(np.median(fb_)), n_with_host=int((host >= 0).sum()))
    return info, P1 - P0
def _root(dom, i):
    while dom.root[i] != i: i = dom.root[i]
    return i

# ------------------------------------------------------------------------------------------------ checkpoint (adds labels + domains)
def ck_save(tag, P, PL, dom, n_done, calls, res):
    import shutil
    d = os.path.join(E.WORK, f"{tag}_ckpt"); new = d + ".new"
    arrs = {f"x{c}": P.x[c] for c in range(3)}; arrs.update({f"m{c}": P.mom[c] for c in range(3)}); arrs["fd"] = P.fd
    need = (sum(a_.nbytes for a_ in arrs.values()) + 4 * P.N) / 1e9
    if os.path.isdir(new): shutil.rmtree(new)
    if os.path.isdir(d) and shutil.disk_usage(E.WORK).free / 1e9 < 2 * need + 20:
        shutil.rmtree(d)
    os.makedirs(new)
    def wr(fn, a_):
        fd = os.open(fn, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600); E._nocache(fd)
        mv = memoryview(np.ascontiguousarray(a_)).cast("B"); o = 0
        while o < len(mv): o += os.write(fd, mv[o:o + (1 << 28)])
        os.fsync(fd); os.close(fd)
    for k, a_ in arrs.items(): wr(os.path.join(new, k + ".bin"), a_)
    fdl = os.open(os.path.join(new, "lab.bin"), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600); E._nocache(fdl)
    for i0, i1 in P.chunks:
        mv = memoryview(PL.read(i0, i1)).cast("B"); o = 0
        while o < len(mv): o += os.write(fdl, mv[o:])
    os.fsync(fdl); os.close(fdl)
    np.savez(os.path.join(new, "dom.npz"), **dom.state())
    meta = dict(n_done=n_done, calls=calls, res=res, arrays={k: [str(a_.dtype), int(a_.size)] for k, a_ in arrs.items()})
    with open(os.path.join(new, "meta.json"), "w") as f: json.dump(meta, f); f.flush(); os.fsync(f.fileno())
    if os.path.isdir(d): shutil.rmtree(d)
    os.rename(new, d)
def ck_load(tag, P, PL, dom):
    for d in (os.path.join(E.WORK, f"{tag}_ckpt"), os.path.join(E.WORK, f"{tag}_ckpt.new")):
        mf = os.path.join(d, "meta.json")
        if not os.path.exists(mf): continue
        meta = json.load(open(mf)); out = {}
        for k, (dt, n) in meta["arrays"].items():
            a_ = np.empty(n, dt); fd = os.open(os.path.join(d, k + ".bin"), os.O_RDONLY); E._nocache(fd)
            mv = memoryview(a_).cast("B"); o = 0
            while o < len(mv):
                r = os.readv(fd, [mv[o:o + (1 << 28)]]); assert r > 0, "truncated checkpoint"; o += r
            os.close(fd); out[k] = a_
        P.x = [out[f"x{c}"] for c in range(3)]; P.mom = [out[f"m{c}"] for c in range(3)]; P.fd = out["fd"]
        lab = np.fromfile(os.path.join(d, "lab.bin"), np.int32)
        for i0, i1 in P.chunks: PL.write(i0, i1, lab[i0:i1])
        del lab
        dom.load(dict(np.load(os.path.join(d, "dom.npz"))))
        return meta
    return None
def ck_clear(tag):
    import shutil
    for d in (os.path.join(E.WORK, f"{tag}_ckpt"), os.path.join(E.WORK, f"{tag}_ckpt.new")):
        if os.path.isdir(d): shutil.rmtree(d)

# ------------------------------------------------------------------------------------------------ the run
def run_sct(foot, npg):
    try: os.nice(10)
    except OSError: pass
    assert E.MODE == "lean", "CFG960 supports the lean engine mode only"
    os.makedirs(E.WORK, exist_ok=True)
    sw = "SCT" + ("K" if not CONVERT else "") + ("MU" if MUTATE != "none" else "")
    tag = f"cfg960sctm_{'m3' if M3ON else 'nom3'}{'' if OWNB == 'fret' else '_ownc'}_{sw}_{foot}_N{npg}_L{E.L:g}_ns{E.NSEED}_{E.MODE}" + (f"_seed{E.SEED}" if E.SEED != 359 else "")
    E.DIAGX = npg <= 512
    mesh = E.Mesh(npg); dta = E.dta_table(); t0 = time.time(); P = E.Particles(npg); E._P[0] = P
    P.fd = np.zeros(P.N, np.float16); PL = PLab(P.N); dom = Dom()
    edges = radial_edges(mesh.dx); mtot = P.N / npg ** 3
    ck = ck_load(tag, P, PL, dom) if E.CKPT else None
    if ck is None:
        E.stage("ic"); E.initial_conditions_lean(mesh, P, 1.0)
    aa = E.step_grid(); nsteps = len(aa) - 1
    snaps = {0.5: "z1", 2 / 3: "z0.5", 1.0: "z0"}
    extra = {i: f"x{1 / aa[i] - 1:.4f}" for i in E.EXTRA if 0 < i <= nsteps}
    res = {"tag": tag, "lane": "CFG960", "engine": "cfg960_sctm_pm.py = CFG654 engine (sha256 " + ENG_SHA[:16] + "...) + SCT-M sector",
           "criteria": "FROZEN_CRITERIA.md 6fc440225", "engine_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(),
           "cfg654_engine_sha256": ENG_SHA, "cfg654_inputs": E.INPUTS, "switch": sw, "sct": dict(M3=M3ON, CONVERT=CONVERT, MUTATE=MUTATE, mut_fac=MUT_FAC, own_baryons=("census f_ret (A5 primary)" if OWNB == "fret" else "M2 condensed (A5 secondary)"),
           kernel="nu_mono", domain_floor="r_ON >= dx", refresh_every=10, nb_log=NB_LOG, nr_cap=NR_CAP, na_cap=NA_CAP),
           "cosmo": dict(h=E.h, om_b=E.om_b, om_c=E.om_c, Om=E.Om, OL=E.OL, FB=E.FB, NS=E.NS, OM_TA=E.OM_TA, H_TA=E.H_TA, dta=os.path.basename(E.DTA_FILE)),
           "mode": E.MODE, "branch": "FLAT", "foot": foot, "np": npg, "mesh": npg, "L": E.L, "nseed": E.NSEED, "seed": E.SEED, "rmin_m3": E.RMIN_PHYS,
           "z_i": E.ZI, "nsteps": nsteps, "threads": E.NTH, "spill": E.SPILL, "snap": {}, "mem": [], "book": [], "events": []}
    calls = 0; n0 = 0
    if ck is not None:
        res = ck["res"]; calls = ck["calls"]; n0 = ck["n_done"]; res.setdefault("resumed_after_step", []).append(n0)
    jfn = os.path.join(E.WORK, f"{tag}.json")
    TM = res.setdefault("timing_s", {})
    def tm(k, t_): TM[k] = TM.get(k, 0.0) + time.time() - t_
    def log(msg):
        print(f"  [{tag}] {msg} t={time.time() - t0:.0f}s maxrss={E.rss_gb():.2f}GB", flush=True)
    M3S = {"Dcode": None, "cbx": None}; PK = {"pk": None}

    def forces_step(a, step_index, snapname=None, measurement_only=False):
        """deposit, refresh (every 10th call), conversions, profiles, merges, bodies, extra deposit, M3, Poisson. Returns (phik, bodies, info)."""
        nonlocal calls
        info = {}; Dta = delta_ta(a, dta); t_now = t_of(a)
        E.stage("deposit"); t_ = time.time(); Dd = E.deposit(mesh, P); tm("deposit", t_)
        meas = None
        if snapname is not None:
            t_ = time.time(); kb, pb, s8, sig = E.measure_pk(mesh, Dd); bm_p = E.block_mean(Dd, max(1, npg // 256)); meas = (kb, pb, s8, sig, bm_p); tm("snap", t_)
        refresh_now = calls % 10 == 0
        pk = None
        if refresh_now:
            E.stage("refresh"); t_ = time.time()
            delta = Dd.read_all(); peaks = E.cover_peaks(mesh, delta, Dta); del delta
            if M3ON:
                _, code, _tab = E.cover_balls(mesh, peaks, Dta, 1.0, a, "FLAT", foot, want_fret=True)
                if M3S["Dcode"] is not None: M3S["Dcode"].close()
                Dc_ = E.DField("fcode960", mesh.M, np.uint8); Dc_.write_all(code); del code
                M3S["Dcode"] = Dc_; M3S["cbx"] = {"R": np.array(E._CBX["R"]), "fret": np.array(E._CBX["fret"])}
            rinfo, pk = refresh(mesh, P, PL, dom, peaks, a, t_now, Dta, foot, step_index)
            info["refresh"] = rinfo; del peaks; tm("refresh", t_)
        calls += 1
        t_ = time.time(); ncv, dpc = pass_conversions(P, PL, dom, t_now); tm("convert", t_)
        info["n_converted_step"] = ncv
        law = Law(a, foot, P.N)
        t_ = time.time(); bid, prof, book = pass_profiles(P, PL, dom, edges); tm("profile", t_)
        ev = [float(np.abs(dpc).max())] + ([float(np.abs(np.array(info["refresh"].get("event_dP", [0.0, 0.0, 0.0]))).max())] if refresh_now else [])
        if refresh_now and pk is not None:
            t_ = time.time(); minfo, dpm = merges(mesh, P, PL, dom, pk, bid, prof, law, edges, a); info["merges"] = minfo; ev.append(float(np.abs(dpm).max()))
            if minfo["n_merge_bound"] + minfo["n_merge_coal"] > 0:
                bid, prof, book = pass_profiles(P, PL, dom, edges)
            tm("merge", t_)
        t_ = time.time()
        BB, bdg, re = body_points(prof, dom.Mc[bid], dom.X[bid], law, edges, mesh.dx, mesh.M, MUT_FAC)
        bpos_, bw, bown = BB["pos"], BB["w"], BB["own"]
        tm("bodies", t_)
        info["bodies"] = {k: v for k, v in bdg.items() if k != "re_dx"}
        if len(bdg["re_dx"]):
            info["bodies"].update(re_dx_median=float(np.median(bdg["re_dx"])), re_dx_max=float(np.max(bdg["re_dx"])), n_points=int(len(bw)), n_nodes=int(len(BB["cw"])))
        painted = float(bw.sum() + BB["cw"].sum()); Mcs = float(dom.Mc[bid].sum()) if len(bid) else 0.0
        bk = dict(step=step_index, a=a, mass_err=(book["M"] + book["Mc"] - P.N) / P.N, painted_err=(painted - Mcs) / P.N,
                  P=book["P"].tolist(), Pabs=book["Pabs"], ev_dP=max(ev), n_dom=int((dom.roots() == np.arange(dom.n)).sum()) if dom.n else 0,
                  n_bodies=int(len(bid)), conv_frac=(1 - E.FB) * book["n_conv"] / P.N, pend_frac=book["n_pend"] / P.N, lab_frac=book["n_lab"] / P.N)
        # extra source: converted particles' inert cold share (- (1 - f_b)) + bodies
        t_ = time.time()
        if book["n_conv"] or len(bw):
            rho = np.zeros((mesh.M, mesh.M * mesh.M))
            if book["n_conv"]: deposit_converted(rho, mesh, P, PL, -(1.0 - E.FB))
            deposit_points(rho, mesh, bpos_, bw)
            if len(BB["cw"]): np.add.at(rho.reshape(-1), BB["cidx"], BB["cw"])     # A3 outer body nodes
            Dx = E.DField("x960", mesh.M, np.float32); r3 = rho.reshape(mesh.M, mesh.M, mesh.M)
            for s in mesh.slabs: Dx.write(s, (r3[s] / mtot).astype(np.float32))
            del rho, r3
        else:
            Dx = None
        tm("xdep", t_)
        if M3ON and M3S["Dcode"] is not None:
            t_ = time.time(); E.stage("m3"); E.expel_m3(mesh, Dd, M3S["Dcode"], M3S["cbx"], info, snapname is not None); tm("m3", t_)
        t_ = time.time()
        if Dx is not None:
            for s in mesh.slabs: Dd.write(s, (Dd.read(s) + Dx.read(s)).astype(np.float32))
            Dx.close()
        msum = sum(float(Dd.read(s).astype(np.float64).sum()) for s in mesh.slabs) / mesh.M ** 3
        bk["mean_delta_g"] = msum
        E.stage("poisson"); dk = E.fwd_field(mesh, Dd); Dd.close()
        for s in mesh.slabs: dk[s] = ((-1.5 * E.Om / a) * dk[s]) * mesh.ik2_s(s)
        tm("poisson", t_)
        info["finite"] = bool(np.all(np.isfinite(dk))); res["book"].append(bk)
        return dk, (BB, bid), info, meas

    def snapshot(name, a, phik, info, meas, restore=False):
        t_ = time.time(); kb, pb, s8, sig, bm_p = meas
        dg = E.grav_field(mesh, phik, a); dgc = E._contig(dg); del dg
        _, pg, s8g, sigg = E.measure_pk(mesh, dgc)
        np.savez_compressed(os.path.join(E.WORK, f"{tag}_{name}_mesh256.npz"), dpart=bm_p, dgrav=E.block_mean(dgc, max(1, npg // 256)))
        del dgc
        res["snap"][name] = dict(a=a, z=1 / a - 1, D=E.Dgrow(a), k=kb, P=pb, sigma8=s8, **sig, P_grav=pg, sigma8_grav=s8g,
                                 sigma2_grav=sigg["sigma2"], sigma4_grav=sigg["sigma4"], measurement_only=restore, sct=info,
                                 book=res["book"][-1], Delta_ta=delta_ta(a, E.dta_table()), t=time.time() - t0)
        res["mem"].append([name, E.rss_gb()]); json.dump(res, open(jfn, "w"))
        tm("snap", t_); log(f"snapshot {name} a={a:.4f} sigma8={s8:.4f} grav {s8g:.4f}")

    def accel_pass(phik, a, kicks, bodies):
        BB, bid = bodies; bpos_, bw, bown = BB["pos"], BB["w"], BB["own"]
        cidx = BB["cidx"]; Mm = mesh.M
        cpad = ((cidx // (Mm * Mm)) * Mm + (cidx // Mm) % Mm) * (Mm + 2) + cidx % Mm if len(cidx) else cidx
        b = mesh.cbuf()
        Fq = np.zeros((len(bid), 3))
        for c in range(3):
            def _b(s): b[s] = (1j * mesh.kv_s(c, s)) * phik[s]
            E.EACH(mesh, _b)
            r = mesh.inv_ip(b)
            def _b(s): r[s] = -a * r[s]
            E.EACH(mesh, _b)
            gpad = b.view(np.float32)
            def task(ch):
                i0, i1 = ch
                accp = E.interp1(mesh, gpad, P.positions(i0, i1))
                for cc in kicks: P.kick(c, i0, i1, cc, accp)
            E.pmap(task, P.ichunks)
            if len(bw):
                gp = E.interp1(mesh, gpad, bpos_).astype(np.float64)
                Fq[:, c] = np.bincount(bown, weights=bw * gp, minlength=len(bid))   # bown = index into bid
            if len(cidx):                                            # A3 outer nodes: the node's own mesh acceleration
                gn = gpad.reshape(-1)[cpad].astype(np.float64)
                Fq[:, c] += np.bincount(BB["cown"], weights=BB["cw"] * gn, minlength=len(bid))
        del b
        if len(bid):
            Mi = dom.Mc[bid] * MUT_FAC                               # inertial = painted mass (MUTATE: the body still falls as a test body)
            for cc in kicks: dom.V[bid] += cc * Fq / Mi[:, None]   # S8: M_c dV/dt = sum_points w g

    def drift_bodies(dd):
        if dom.n:
            k = np.nonzero(dom.Mc[:dom.n] > 0)[0]; dom.X[k] = (dom.X[k] + dd * dom.V[k]) % E.L

    if ck is None:
        phik, bodies, info, meas = forces_step(E.AI, 0, snapname="zi")
        snapshot("zi", E.AI, phik, info, meas)
        a0_, a1_ = aa[0], aa[1]; am = math.sqrt(a0_ * a1_)
        t_ = time.time(); accel_pass(phik, E.AI, [quad(lambda x: 1 / (x * x * E.E(x)), a0_, am)[0]], bodies); del phik; tm("accel", t_)
        dd = quad(lambda x: 1 / (x ** 3 * E.E(x)), a0_, a1_)[0]
        t_ = time.time(); P.drift(dd); drift_bodies(dd); tm("drift", t_)
        log("step 0 drift done")
    else:
        log(f"RESUMED from checkpoint after step {n0} (forces calls {calls})")
    for n in range(n0, nsteps):
        a0_, a1_ = aa[n], aa[n + 1]; am = math.sqrt(a0_ * a1_)
        sn = None
        for asn, nm in snaps.items():
            if abs(a1_ - asn) < 1e-9: sn = nm
        if (n + 1) in extra: sn = extra[n + 1]
        phik, bodies, info, meas = forces_step(a1_, n + 1, snapname=sn)
        last = n == nsteps - 1
        kicks = [quad(lambda x: 1 / (x * x * E.E(x)), am, a1_)[0]]
        if not last:
            b0, b1 = aa[n + 1], aa[n + 2]; bm = math.sqrt(b0 * b1)
            kicks.append(quad(lambda x: 1 / (x * x * E.E(x)), b0, bm)[0])
        if sn is not None: snapshot(sn, a1_, phik, info, meas, restore=(n + 1) in extra)
        t_ = time.time(); accel_pass(phik, a1_, kicks, bodies); del phik; tm("accel", t_)
        if not last:
            dd = quad(lambda x: 1 / (x ** 3 * E.E(x)), b0, b1)[0]
            t_ = time.time(); P.drift(dd); drift_bodies(dd); tm("drift", t_)
        if info.get("refresh") or info.get("merges"):
            res["events"].append(dict(step=n + 1, a=a1_, refresh=info.get("refresh"), merges=info.get("merges")))
        if (n + 1) % 5 == 0 or n < 3:
            bk = res["book"][-1]
            log(f"step {n + 1}/{nsteps} a={a1_:.4f} dom {bk['n_dom']} bodies {bk['n_bodies']} conv {bk['conv_frac']:.3f} pend {bk['pend_frac']:.3f} "
                f"massErr {bk['mass_err']:.1e} paintErr {bk['painted_err']:.1e} timing " + " ".join(f"{k} {v:.0f}" for k, v in TM.items()))
        res["mem"].append([f"step{n + 1}", E.rss_gb()])
        if E.CKPT and not last and calls % 10 == 0:
            t_ = time.time(); ck_save(tag, P, PL, dom, n + 1, calls, res); log(f"checkpoint after step {n + 1} ({time.time() - t_:.0f}s)")
        if n + 1 >= E.MAXSTEPS:
            res["stopped_at_step"] = n + 1; break
    if M3S["Dcode"] is not None: M3S["Dcode"].close()
    res["runtime_s"] = time.time() - t0; res["maxrss_gb"] = E.rss_gb()
    res["domains_final"] = dict(n_total=int(dom.n), n_merged=int(dom.n_merged), n_alive=int((dom.roots() == np.arange(dom.n)).sum()) if dom.n else 0,
                                Mc_total_frac=float(dom.Mc[:dom.n].sum() / P.N) if dom.n else 0.0)
    if npg <= 256 and "stopped_at_step" not in res:
        np.savez_compressed(os.path.join(E.WORK, f"{tag}_domains.npz"), **dom.state())
    json.dump(res, open(jfn, "w"))
    PL.close()
    if E.CKPT and "stopped_at_step" not in res: ck_clear(tag)
    log("done")
    return res

if __name__ == "__main__":
    sw, ft, npg = sys.argv[1], sys.argv[2], int(sys.argv[3])
    assert sw in ("SCT", "S0REF") and ft in ("canonical", "alt")
    if sw == "S0REF":
        E.run("S0", "FLAT", ft, npg, 1.0)
    else:
        run_sct(ft, npg)
