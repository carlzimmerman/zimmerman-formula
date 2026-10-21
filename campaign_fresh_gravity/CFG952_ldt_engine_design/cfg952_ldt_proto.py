#!/usr/bin/env python3
"""CFG952: labelled-domain-theory (LDT) PM-engine prototype -- a SEPARATE 64^3 toy.

No CFG650 / CFG654 engine code is imported or edited; every routine here is written independently (the nu_mono kernel and the
census f_ret law are re-implemented from their formulas).  Criteria FROZEN_CRITERIA.md (844ce293d), amendment A1 (7a3ade021,
pre-result).  The engine-side numbers in the EST stage are read from the record's data files and run JSON (read only).

Stages:  CFG952_STAGE=K        controls K1-K4                      -> cfg952_K.out / cfg952_results_K.json
         CFG952_MUTATE=1       teeth Mu1, Mu2, Mu3, Mu5            -> cfg952_MUTATE.out / cfg952_results_MUTATE.json (exit 1 = all bite)
         (default) MAIN        smoke tests a0-a2, b1, c1, c2 + EST -> cfg952.out / cfg952_results.json
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg952_ldt_proto.py   (one process; in-script RSS guard 1 GB -> exit 3)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
if sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    # macOS keeps freed MALLOC_MEDIUM pages resident (reclaimable), inflating RSS ~10x over the physical footprint; route those
    # sizes elsewhere so the 1 GB RSS guard measures real use.  Allocator setting only: no arithmetic changes.  exec keeps one process.
    os.execve(sys.executable, [sys.executable] + sys.argv, dict(os.environ, MallocMediumZone="0"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time, resource, threading, glob, copy
import numpy as np
from scipy import fft as sfft
from scipy import ndimage
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.environ.get("CFG952_STAGE", "MAIN").upper()
MUTATE = os.environ.get("CFG952_MUTATE", "0") == "1"
T0 = time.time()

# ---------------------------------------------------------------- RSS guard (1 GB, criteria section 6)
RSS_LIMIT = 1.0e9
def peak_rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return (r if sys.platform == "darwin" else r * 1024) / 1e9
def footprint_gb():
    try:
        import ctypes
        class _RU(ctypes.Structure):
            _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in ("ut", "st", "piw", "iw", "pageins", "wired", "resident", "footprint")] + [("pad", ctypes.c_uint64 * 40)]
        ru = _RU(); lp = ctypes.CDLL("/usr/lib/libproc.dylib")
        return ru.footprint / 1e9 if lp.proc_pid_rusage(os.getpid(), 2, ctypes.byref(ru)) == 0 else -1.0
    except Exception:
        return -1.0
def _guard():
    while True:
        if peak_rss_gb() * 1e9 > RSS_LIMIT:
            sys.stdout.write(f"RSS GUARD: peak RSS {peak_rss_gb():.3f} GB > 1 GB -> exit 3\n"); sys.stdout.flush(); os._exit(3)
        time.sleep(0.2)
threading.Thread(target=_guard, daemon=True).start()
try:                                                  # return freed malloc pages to the OS (macOS keeps them resident;
    import ctypes                                     # the class-A engine's own technique; no effect on any number)
    _LIBC = ctypes.CDLL("/usr/lib/libSystem.dylib"); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception:
    _LIBC = None
def relief():
    if _LIBC is not None: _LIBC.malloc_zone_pressure_relief(None, 0)

def log(msg):
    print(msg, flush=True)

# ---------------------------------------------------------------- toy constants (criteria section 1; A1)
G = 1.0; A0 = 1.0; L = 40.0; M = 64; DX = L / M; DV = DX ** 3; FPG = 4 * math.pi * G
RHO_TA = 1.0e-3; RMIN = 2 * DX; XH = 0.6; DT = 0.04; SIG_SM = 2 * DX          # A1.1: sigma = 2 cells
RG = np.geomspace(DX, 12.0, 14); REFRESH = 10
NEWTON_TOL = 1e-12                                                            # A1.4
FBZS = False                                                                  # A2 post-hoc fallback (zero-sum exact on Newton failure)

# ---------------------------------------------------------------- nu_mono replica (RAR h, monotone floor delta = 0.05)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_m1(y):
    """nu_mono(y) - 1."""
    y = np.maximum(np.asarray(y, float), 1e-12)
    return np.interp(np.log10(y), LYG, H_MONO) / y
def nu_rar_m1(y):
    return 1.0 / np.expm1(np.sqrt(np.asarray(y, float)))

# ---------------------------------------------------------------- periodic mesh (momentum-conserving PM: CIC both ways, ik with Nyquist zeroed)
_k1 = 2 * np.pi * sfft.fftfreq(M, d=DX); _kz = 2 * np.pi * sfft.rfftfreq(M, d=DX)
KX = _k1[:, None, None]; KY = _k1[None, :, None]; KZ = _kz[None, None, :]
K2T = KX ** 2 + KY ** 2 + KZ ** 2
IK2 = np.where(K2T > 0, 1.0 / np.where(K2T > 0, K2T, 1.0), 0.0)
_KXg = KX.copy(); _KXg[M // 2] = 0.0
_KYg = KY.copy(); _KYg[:, M // 2] = 0.0
_KZg = KZ.copy(); _KZg[..., M // 2] = 0.0
KG = (_KXg, _KYg, _KZg)

def grav(rho):
    """g = -grad Phi, lap Phi = 4 pi G (rho - mean): (3, M, M, M)."""
    rk = sfft.rfftn(rho) * IK2 * FPG
    return np.stack([sfft.irfftn(1j * KG[c] * rk, s=(M, M, M)) for c in range(3)])
def potential(rho):
    return sfft.irfftn(-FPG * sfft.rfftn(rho) * IK2, s=(M, M, M))
def cic(pos):
    u = pos / DX; i0 = np.floor(u).astype(np.int64); w = u - i0
    return i0 % M, (i0 + 1) % M, w
def deposit(pos, mass):
    rho = np.zeros(M ** 3)
    if len(pos) == 0: return rho.reshape(M, M, M)
    i0, i1, w = cic(pos)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                rho += np.bincount((ix * M + iy) * M + iz, weights=mass * wx * wy * wz, minlength=M ** 3)
    return rho.reshape(M, M, M) / DV
def interp(f3, pos):
    i0, i1, w = cic(pos); out = np.zeros((len(pos), f3.shape[0]))
    fl = f3.reshape(f3.shape[0], -1)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                out += (wx * wy * wz)[:, None] * fl[:, (ix * M + iy) * M + iz].T
    return out
def wrap(d):
    return d - L * np.round(d / L)

# ---------------------------------------------------------------- objects: truncated Plummer pairs + Jeans velocities (A1.2)
def Fpl(r, b):
    return r ** 3 / (r ** 2 + b ** 2) ** 1.5
def menc(r, Mt, b, rt):
    return Mt * np.minimum(Fpl(np.asarray(r, float), b), Fpl(rt, b)) / Fpl(rt, b)
def node_ron(menc_tot):
    ron = 0.0
    for R in RG:
        if menc_tot(R) / (4 / 3 * math.pi * R ** 3) >= RHO_TA: ron = float(R)
        else: break
    return ron
def supply_edge(Mb, Mc, ron):
    if Mb <= 0 or Mc <= 0 or ron <= 0: return 0.0
    return XH * min(math.sqrt(G * Mb / A0) / math.log(1.0 + Mb / Mc), ron)

def object_model(Mb, bb, Mc, bc):
    """isolated spherical model with the prototype's rules (r_ON node rule, edge, spherical QUMOND phantom, deficit, uniform-q
    draw) -> isotropic Jeans sigma^2(r) of baryons and cold (A1.2)."""
    rtb, rtc = 8 * bb, 2.5 * bc
    r = np.geomspace(1e-3, 1.02 * max(rtb, rtc, RG[-1]), 6000)
    Mbr = menc(r, Mb, bb, rtb); Mcr = menc(r, Mc, bc, rtc)
    ron = node_ron(lambda R: float(menc(R, Mb, bb, rtb) + menc(R, Mc, bc, rtc)))
    re = supply_edge(Mb, Mc, ron)
    gNb = G * Mbr / r ** 2; Mph = r ** 2 * gNb * nu_m1(gNb / A0) / G
    rho_ph = np.gradient(Mph, r) / (4 * np.pi * r ** 2); rho_c = np.gradient(Mcr, r) / (4 * np.pi * r ** 2)
    rho_b = np.gradient(Mbr, r) / (4 * np.pi * r ** 2)
    e = np.where(r < re, np.maximum(rho_ph - rho_c, 0.0), 0.0)
    Ecum = np.concatenate([[0.0], np.cumsum(0.5 * (4 * np.pi * r[1:] ** 2 * e[1:] + 4 * np.pi * r[:-1] ** 2 * e[:-1]) * np.diff(r))])
    Esum = float(np.interp(re, r, Ecum)) if re > 0 else 0.0
    Csh = float(menc(ron, Mc, bc, rtc) - menc(re, Mc, bc, rtc)) if ron > re else 0.0
    q = Esum / Csh if Csh > 0 else 0.0
    if q > 1: Ecum = Ecum / q; q = 1.0
    Eenc = np.interp(np.minimum(r, re), r, Ecum)
    Mc_re = float(menc(re, Mc, bc, rtc))
    drawn = q * np.clip(menc(np.minimum(r, ron), Mc, bc, rtc) - Mc_re, 0.0, None) * (r > re)
    Mg = Mbr + Mcr + Eenc - drawn
    g = G * Mg / r ** 2
    def sig2(rho):
        f = rho * g; tail = np.concatenate([np.cumsum((0.5 * (f[1:] + f[:-1]) * np.diff(r))[::-1])[::-1], [0.0]])
        return np.where(rho > 1e-14 * rho.max(), tail / np.maximum(rho, 1e-300), 0.0)
    return dict(r=r, s2b=sig2(rho_b), s2c=sig2(rho_c), ron=ron, re=re, q=q)

def plummer(rng, n, b, rt):
    Ft = Fpl(rt, b); u = np.maximum(rng.uniform(0, Ft, n), 1e-300)
    r = b / np.sqrt(u ** (-2.0 / 3.0) - 1.0)
    d = rng.standard_normal((n, 3)); d /= np.linalg.norm(d, axis=1)[:, None]
    return r[:, None] * d, r

class State:
    def __init__(self):
        self.x = np.zeros((0, 3)); self.v = np.zeros((0, 3)); self.m = np.zeros(0)
        self.kind = np.zeros(0, np.int8); self.obj = np.zeros(0, np.int8); self.lab = np.zeros(0, np.int32)
        self.labels = {}; self.sectors = {}; self.next_id = 1; self.alias = {}; self.events = []
    def add(self, x, v, m, kind, obj):
        self.x = np.vstack([self.x, x % L]); self.v = np.vstack([self.v, v]); self.m = np.concatenate([self.m, m])
        self.kind = np.concatenate([self.kind, np.full(len(m), kind, np.int8)])
        self.obj = np.concatenate([self.obj, np.full(len(m), obj, np.int8)])
        self.lab = np.concatenate([self.lab, np.zeros(len(m), np.int32)])

def add_object(st, rng, obj, Mb, bb, Mc, bc, nb, nc, centre, vbulk=(0, 0, 0), cold_offset=(0, 0, 0)):
    mdl = object_model(Mb, bb, Mc, bc)
    pb, rb = plummer(rng, nb, bb, 8 * bb); pc, rc = plummer(rng, nc, bc, 2.5 * bc)
    vb = np.sqrt(np.interp(rb, mdl["r"], mdl["s2b"]))[:, None] * rng.standard_normal((nb, 3))
    vc = np.sqrt(np.interp(rc, mdl["r"], mdl["s2c"]))[:, None] * rng.standard_normal((nc, 3))
    c = np.asarray(centre, float); vb_ = np.asarray(vbulk, float)
    st.add(c + pb, vb + vb_, np.full(nb, Mb / nb), 0, obj)
    st.add(c + np.asarray(cold_offset, float) + pc, vc + vb_, np.full(nc, Mc / nc), 1, obj)
    return mdl

# ---------------------------------------------------------------- label machinery (catchment balls, M1 partition, latch beta)
def tophat(x):
    out = np.ones_like(x); nz = x > 1e-8
    out[nz] = 3 * (np.sin(x[nz]) - x[nz] * np.cos(x[nz])) / x[nz] ** 3
    return out
def find_peaks(st):
    rk = sfft.rfftn(deposit(st.x, st.m))
    sm = sfft.irfftn(rk * np.exp(-0.5 * K2T * SIG_SM ** 2), s=(M, M, M))
    mx = ndimage.maximum_filter(sm, size=3, mode="wrap")
    idx = np.argwhere((sm == mx) & (sm >= RHO_TA))
    if len(idx) == 0: return idx, np.zeros(0)
    ok = np.ones(len(idx), bool); ron = np.zeros(len(idx)); kk = np.sqrt(K2T)
    for R in RG:
        mean = sfft.irfftn(rk * tophat(kk * R), s=(M, M, M))[idx[:, 0], idx[:, 1], idx[:, 2]]
        ok &= mean >= RHO_TA; ron[ok] = R
    res = ron >= RMIN - 1e-9
    return idx[res], ron[res]
def partition(idx, ron):
    owner = np.full((M, M, M), -1, np.int64); best = np.full((M, M, M), np.inf); g = np.arange(M)
    for h in range(len(idx)):
        d = [np.minimum(np.abs(g - idx[h, a]), M - np.abs(g - idx[h, a])) * DX for a in range(3)]
        d2 = d[0][:, None, None] ** 2 + d[1][None, :, None] ** 2 + d[2][None, None, :] ** 2
        sc = np.sqrt(d2) / ron[h] - 1e-9 * ron[h]
        upd = (d2 <= ron[h] ** 2) & (sc < best)
        owner[upd] = h; best[upd] = sc[upd]
    return owner
def eff_labels(st):
    lab = st.lab.copy()
    for a, b in st.alias.items(): lab[lab == a] = b
    return lab
def lab_mask(st, lid):
    u = st.labels[lid].get("union")
    return np.isin(st.lab, u) if u else (st.lab == lid)
def centroid(st, sel, ref):
    d = wrap(st.x[sel] - ref); m = st.m[sel]
    return (ref + (m[:, None] * d).sum(0) / m.sum()) % L
def new_sector(st, lid):
    st.sectors[lid] = dict(members=[lid], Dt=np.zeros(3), Ps=np.zeros(3), As=np.zeros(3), ramp=None, alive=True)

def refresh_labels(st, t):
    """latch rule beta at a census refresh (t = 0 and every 10th step)."""
    idx, ron = find_peaks(st)
    info = dict(t=t, n_peaks=int(len(idx)), assigned=0, born=[])
    if len(idx) == 0: return info
    owner = partition(idx, ron)
    ngp = np.floor(st.x / DX + 0.5).astype(np.int64) % M
    h = owner[ngp[:, 0], ngp[:, 1], ngp[:, 2]]; le = eff_labels(st)
    born = []
    for hh in range(len(idx)):
        inh = h == hh
        un = inh & (st.lab == 0)
        if not un.any(): continue
        lm = inh & (le > 0); target = None
        if lm.any():
            ul, inv = np.unique(le[lm], return_inverse=True); ms = np.bincount(inv, weights=st.m[lm])
            j = int(np.argmax(ms))
            if ms[j] >= 0.5 * ms.sum(): target = int(ul[j])
        if target is None:
            target = st.next_id; st.next_id += 1
            st.labels[target] = dict(r_on=float(ron[hh]), r_e=0.0, X=idx[hh] * DX, birth=t, alive=True, union=None)
            born.append(target)
        st.lab[un] = target; info["assigned"] += int(un.sum())
    for lid in born:
        mk = st.lab == lid; mb = mk & (st.kind == 0); mc = mk & (st.kind == 1)
        Mb, Mc = float(st.m[mb].sum()), float(st.m[mc].sum())
        lab = st.labels[lid]; lab["r_e"] = supply_edge(Mb, Mc, lab["r_on"]); lab["Mb0"], lab["Mc0"] = Mb, Mc
        lab["X"] = centroid(st, mb if mb.any() else mk, lab["X"])
        new_sector(st, lid)
    info["born"] = born
    return info

# ---------------------------------------------------------------- own-domain phantom (LDT-EXACT): isolated sub-box solve
_KC = {}
def kernels(n):
    if n in _KC: return _KC[n]
    P = sfft.next_fast_len(2 * n - 1, real=True); i = np.arange(P)
    o = np.where(i <= n - 1, i, i - P).astype(float); valid1 = (i <= n - 1) | (i >= P - (n - 1))
    ox, oy, oz = np.meshgrid(o, o, o, indexing="ij"); va = valid1[:, None, None] & valid1[None, :, None] & valid1[None, None, :]
    r2 = (ox ** 2 + oy ** 2 + oz ** 2) * DX ** 2; r = np.sqrt(r2); nz = va & (r2 > 0)
    Kk = []
    for oc in (ox, oy, oz):
        K = np.zeros((P, P, P)); K[nz] = -G * oc[nz] * DX / r[nz] ** 3; Kk.append(sfft.rfftn(K))
    Kp = np.zeros((P, P, P)); Kp[nz] = -G / r[nz]; Kp[0, 0, 0] = -G * 2.380 / DX
    _KC[n] = (P, Kk, sfft.rfftn(Kp))
    return _KC[n]
def sub_coords(pos, c, h):
    return wrap(pos - c * DX) / DX + h
def sub_deposit(pos, mass, c, h, n):
    rho = np.zeros(n ** 3)
    if len(pos) == 0: return rho.reshape(n, n, n), 0.0
    u = sub_coords(pos, c, h); i0 = np.floor(u).astype(np.int64); w = u - i0
    ins = np.all((i0 >= 0) & (i0 + 1 <= n - 1), axis=1); strays = float(mass[~ins].sum())
    i0, w, mm = i0[ins], w[ins], mass[ins]
    for cx in (0, 1):
        ix = i0[:, 0] + cx; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i0[:, 1] + cy; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i0[:, 2] + cz; wz = w[:, 2] if cz else 1 - w[:, 2]
                rho += np.bincount((ix * n + iy) * n + iz, weights=mm * wx * wy * wz, minlength=n ** 3)
    return rho.reshape(n, n, n) / DV, strays
def sub_interp(f, pos, c, h, n):
    u = sub_coords(pos, c, h); i0 = np.clip(np.floor(u).astype(np.int64), 0, n - 2); w = np.clip(u - i0, 0, 1)
    out = np.zeros(len(pos))
    for cx in (0, 1):
        wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                wz = w[:, 2] if cz else 1 - w[:, 2]
                out += wx * wy * wz * f[i0[:, 0] + cx, i0[:, 1] + cy, i0[:, 2] + cz]
    return out
def own_field(rho_b, n):
    P, Kk, _ = kernels(n); rk = sfft.rfftn(rho_b * DV, s=(P, P, P))
    return np.stack([sfft.irfftn(rk * Kk[c], s=(P, P, P))[:n, :n, :n] for c in range(3)])
def own_potential(rho, n):
    P, _, Kp = kernels(n)
    return sfft.irfftn(sfft.rfftn(rho * DV, s=(P, P, P)) * Kp, s=(P, P, P))[:n, :n, :n]
def phantom_fd(g):
    F = nu_m1(np.sqrt((g ** 2).sum(0)) / A0) * g; div = np.zeros(g.shape[1:])
    div[1:-1, 1:-1, 1:-1] = ((F[0, 2:, 1:-1, 1:-1] - F[0, :-2, 1:-1, 1:-1]) + (F[1, 1:-1, 2:, 1:-1] - F[1, 1:-1, :-2, 1:-1])
                             + (F[2, 1:-1, 1:-1, 2:] - F[2, 1:-1, 1:-1, :-2])) / (2 * DX)
    return -div / FPG

def comp_fields(st, lid, update_X=True):
    lab = st.labels[lid]; mk = lab_mask(st, lid); mb = mk & (st.kind == 0); mc = mk & (st.kind == 1)
    X = centroid(st, mb if mb.any() else mk, lab["X"]) if mk.any() else lab["X"]
    if update_X: lab["X"] = X
    h = int(math.ceil(lab["r_on"] / DX)) + 2; n = 2 * h + 1; c = np.rint(X / DX).astype(np.int64)
    rho_b, sb = sub_deposit(st.x[mb], st.m[mb], c, h, n); rho_c, sc = sub_deposit(st.x[mc], st.m[mc], c, h, n)
    g = own_field(rho_b, n); s_ph = phantom_fd(g)
    off = (np.arange(n) - h) * DX; base = wrap(c * DX - X)
    rv = np.stack(np.broadcast_arrays(off[:, None, None] + base[0], off[None, :, None] + base[1], off[None, None, :] + base[2]))
    rr = np.sqrt((rv ** 2).sum(0))
    inside = rr < lab["r_e"]; shell = (rr >= lab["r_e"]) & (rr < lab["r_on"])
    gi = [(c[a] - h + np.arange(n)) % M for a in range(3)]
    return dict(lid=lid, X=X, c=c, h=h, n=n, rho_b=rho_b, rho_c=rho_c, g=g, s_ph=s_ph, rv=rv, rr=rr, inside=inside, shell=shell,
                gi=gi, strays_b=sb, strays_c=sc, Mph_edge=float((s_ph * inside).sum() * DV), Mb=float(st.m[mb].sum()),
                Mc=float(st.m[mc].sum()), mb=mb, mc=mc)

def prep(F):
    e = np.where(F["inside"], np.maximum(F["s_ph"] - F["rho_c"], 0.0), 0.0)
    Esum = float(e.sum() * DV); Csum = float((F["rho_c"] * F["shell"]).sum() * DV); capped = False
    if Csum <= 0 or Esum <= 0:
        e = np.zeros_like(e); Esum = 0.0; q = 0.0
    else:
        q = Esum / Csum
        if q > 1: e = e / q; Esum = Csum; q = 1.0; capped = True
    wsh = F["rho_c"] * F["shell"]
    rc = (F["rv"] * wsh).sum((1, 2, 3)) * DV / Csum if Csum > 0 else np.zeros(3)
    F.update(e=e, Esum=Esum, Csum=Csum, q=q, capped=capped, rc=rc, De=(F["rv"] * e).sum((1, 2, 3)) * DV,
             d=F["rv"] - rc[:, None, None, None], wsh=wsh, cells=F["shell"] & (F["rho_c"] > 0))

# ---------------------------------------------------------------- the draw: E8 / LIN (frozen linear) / EXP (A1.4 tilt; DIPFREE, DIPSLAVE)
def _Fp(u): return np.where(u <= 0, np.exp(np.minimum(u, 0.0)), 1.0)
def _F(u): return np.where(u <= 0, np.exp(np.minimum(u, 0.0)), 1.0 + u)
def _Fpp(u): return np.where(u <= 0, np.exp(np.minimum(u, 0.0)), 0.0)
def _bd(b, d): return b[0] * d[0] + b[1] * d[1] + b[2] * d[2]

def solve_draw(comps, ws, target, s_amp, draw):
    """sets F['comp'] for every component; returns info (clipped, miss, iterations, headroom)."""
    info = dict(clipped=False, iters=0, headroom=0.0, lam=1.0)
    for F in comps:
        F["comp"] = np.where(F["shell"], F["q"] * F["rho_c"], 0.0)
    if s_amp <= 0: return info
    if draw == "E8":
        info["headroom"] = max([F["q"] for F in comps] + [0.0]); return info
    Rtar = sum(w * F["De"] for F, w in zip(comps, ws)) - target / s_amp       # required sum_X w_X sum comp_X r_X dV
    free = [(F, w) for F, w in zip(comps, ws) if F["Esum"] > 0 and not F["capped"] and w > 0]
    fixed = [(F, w) for F, w in zip(comps, ws) if not (F["Esum"] > 0 and not F["capped"] and w > 0)]
    T = Rtar - sum(w * (F["comp"][None] * F["rv"]).sum((1, 2, 3)) * DV for F, w in fixed) if fixed else Rtar.copy()
    if not free:
        return info
    if draw == "LIN":
        W = sum(w * F["q"] * np.array([[float((F["d"][a_] * F["wsh"] * F["d"][c_]).sum()) for c_ in range(3)] for a_ in range(3)]) * DV for F, w in free)
        D0 = sum(w * F["q"] * F["Csum"] * F["rc"] for F, w in free)
        beta = np.linalg.solve(W, T - D0)
        lam = 1.0
        for F, w in free:
            bd = np.einsum("i,i...->...", beta, F["d"])[F["cells"]]; q = F["q"]
            pos = bd > 0; neg = bd < 0
            if pos.any(): lam = min(lam, float(np.min((1.0 / q - 1.0) / bd[pos])))
            if neg.any(): lam = min(lam, float(np.min(-1.0 / bd[neg])))
        info["clipped"] = lam < 1 - 1e-12; info["lam"] = lam; beta = beta * min(lam, 1.0)
        hr = 0.0
        for F, w in free:
            f = F["q"] * (1.0 + np.einsum("i,i...->...", beta, F["d"]))
            F["comp"] = np.where(F["shell"], f * F["rho_c"], 0.0); hr = max(hr, float(f[F["cells"]].max()))
        info["headroom"] = hr; info["beta"] = beta.tolist()
        return info
    # EXP: damped Newton on the convex dual (A1.4); T for free comps about their shell-cold centroids
    T = T - sum(w * F["rc"] * F["Esum"] for F, w in free)
    K = len(free); z = np.concatenate([[math.log(F["q"]) for F, _ in free], np.zeros(3)])
    rho = [F["wsh"][F["cells"]] * DV for F, _ in free]; dd = [F["d"][:, F["cells"]] for F, _ in free]
    wv = np.array([w for _, w in free]); Ev = np.array([F["Esum"] for F, _ in free])
    scale = np.concatenate([wv * Ev, np.full(3, float(np.sum(wv * Ev * np.array([F_["rr"][F_["cells"]].max() for F_, _ in free]))))])
    def phi(z):
        b = z[K:]; tot = -float(np.sum(b * T))
        for j in range(K):
            u = z[j] + _bd(b, dd[j]); tot += wv[j] * (float((rho[j] * _F(u)).sum()) - z[j] * Ev[j])
        return tot
    def grad_hess(z):
        b = z[K:]; gr = np.zeros(K + 3); H = np.zeros((K + 3, K + 3)); gr[K:] = -T
        for j in range(K):
            u = z[j] + _bd(b, dd[j]); fp = rho[j] * _Fp(u); fpp = rho[j] * _Fpp(u)
            gr[j] = wv[j] * (fp.sum() - Ev[j]); gr[K:] += wv[j] * (dd[j] * fp).sum(1)
            H[j, j] = wv[j] * fpp.sum(); hb = wv[j] * (dd[j] * fpp).sum(1); H[j, K:] = hb; H[K:, j] = hb
            H[K:, K:] += wv[j] * np.array([[(dd[j][a] * fpp * dd[j][c]).sum() for c in range(3)] for a in range(3)])
        return gr, H
    ok = False; zbest = None; gbest = np.inf
    for it in range(200):
        gr, H = grad_hess(z)
        if np.all(np.isfinite(gr)) and np.all(np.isfinite(z)):
            gn = float(np.max(np.abs(gr) / scale))
            if gn < gbest: gbest = gn; zbest = z.copy()              # best finite iterate (used only by the A2 fallback)
        if np.all(np.abs(gr) <= NEWTON_TOL * scale): ok = True; info["iters"] = it; break
        H = H + 1e-14 * np.trace(H) * np.eye(K + 3)
        try: p = -np.linalg.solve(H, gr)
        except np.linalg.LinAlgError: p = -gr
        f0 = phi(z); slope = float(np.sum(gr * p)); tt = 1.0
        for _ in range(60):
            if phi(z + tt * p) <= f0 + 1e-4 * tt * slope: break
            tt *= 0.5
        z = z + tt * p
    info["clipped"] = not ok; info["iters"] = info["iters"] if ok else 200
    if not ok and FBZS:                                # A2 FB-ZS: zero-sum exact per component, dipole best effort over beta scaling
        bl = zbest[K:].copy() if zbest is not None else np.zeros(3); best = None
        nb = float(np.linalg.norm(bl)); ndir = bl / nb if nb > 0 and np.isfinite(nb) else np.array([1.0, 0.0, 0.0])
        rmax = max(float(np.abs(d_).max()) for d_ in dd)          # direction of beta_last, 41-point geometric magnitude grid (|beta d| <= 100)
        mags = np.concatenate([[0.0], np.geomspace(1e-2, 1e2, 40) / rmax])
        fixedD = sum(w * (F["comp"][None] * F["rv"]).sum((1, 2, 3)) * DV for F, w in fixed) if fixed else np.zeros(3)
        for lamsc in mags:
            bb = lamsc * ndir; lams = []; Dfree = np.zeros(3)
            for j in range(K):
                ud = _bd(bb, dd[j]); lo, hi = -60.0 - float(ud.max()), 60.0 - float(ud.min())
                for _ in range(80):
                    mid = 0.5 * (lo + hi)
                    if float((rho[j] * _Fp(mid + ud)).sum()) < Ev[j]: lo = mid
                    else: hi = mid
                lj = 0.5 * (lo + hi); lams.append(lj); fp = rho[j] * _Fp(lj + ud)
                Dfree += wv[j] * ((dd[j] * fp).sum(1) + free[j][0]["rc"] * fp.sum())
            Dr = s_amp * (sum(w * F["De"] for F, w in zip(comps, ws)) - Dfree - fixedD)
            miss = float(np.linalg.norm(Dr - target))
            if best is None or miss < best[0]: best = (miss, lamsc, np.array(lams), bb)
        z = np.concatenate([best[2], best[3]]); info["fbzs_scale"] = float(best[1]); info["fbzs_miss"] = best[0]
    b = z[K:]; hr = 0.0
    for j, (F, w) in enumerate(free):
        f = np.zeros(F["shell"].shape); f[F["cells"]] = _Fp(z[j] + _bd(b, dd[j]))
        F["comp"] = f * F["rho_c"]; hr = max(hr, float(f[F["cells"]].max()))
    info["headroom"] = hr; info["beta"] = b.tolist()
    return info

# ---------------------------------------------------------------- sectors, source, forces
def ramp_w(sec, t):
    r = sec["ramp"]; x = min(max((t - r["t_m"]) / r["tau"], 0.0), 1.0)
    return 0.5 * (1 - math.cos(math.pi * x))
def sector_members(sec, t):
    if sec["ramp"] is None: return [(lid, 1.0) for lid in sec["members"]]
    w = ramp_w(sec, t); A, B, C = sec["ramp"]["A"], sec["ramp"]["B"], sec["ramp"]["C"]
    return [(A, 1 - w), (B, 1 - w), (C, w)]

def build_source(st, t, draw, s_amp):
    S = np.zeros((M, M, M)); recs = {}
    for sid, sec in st.sectors.items():
        if not sec["alive"]: continue
        mem = [(lid, w) for lid, w in sector_members(sec, t) if w > 0 or sec["ramp"] is not None]
        comps, ws = [], []
        for lid, w in mem:
            F = comp_fields(st, lid); prep(F); comps.append(F); ws.append(w)
        target = sec["Dt"] if draw in ("DIPSLAVE", "LIN") else np.zeros(3)
        info = solve_draw(comps, ws, target, s_amp, draw)
        Dreal = np.zeros(3); zs = 0.0; wsum = 0.0; Dscale = 0.0
        for F, w in zip(comps, ws):
            SX = s_amp * w * (F["e"] - F["comp"]); F["SX"] = SX
            S[np.ix_(*F["gi"])] += SX
            Dreal += (SX[None] * F["rv"]).sum((1, 2, 3)) * DV; Dscale += float((np.abs(SX) * F["rr"]).sum() * DV)
            if F["Esum"] > 0 and s_amp * w > 0: zs = max(zs, abs(float(SX.sum() * DV)) / (s_amp * w * F["Esum"]))
            wsum += w * F["Mph_edge"]
        recs[sid] = dict(comps=comps, ws=ws, info=info, Dreal=Dreal, Dscale=Dscale, zs=zs, Mph=wsum,
                         miss=float(np.linalg.norm(Dreal - target)) if draw in ("DIPSLAVE", "LIN", "DIPFREE") else 0.0)
    return S, recs

def forces(st, t, draw, s_amp, with_source=True):
    if with_source: S, recs = build_source(st, t, draw, s_amp)
    else: S, recs = np.zeros((M, M, M)), {}
    g = grav(deposit(st.x, st.m) + S)
    acc = interp(g, st.x)
    for sid, r in recs.items():
        A = np.zeros(3)
        for F in r["comps"]:
            gl = g[(slice(None),) + np.ix_(*F["gi"])]
            A += (F["SX"][None] * gl).sum((1, 2, 3)) * DV
        st.sectors[sid]["As"] = A; r["As"] = A
    return acc, recs, S, g

def do_merge(st, A, B, t, mode):
    la, lb = st.labels[A], st.labels[B]; C = st.next_id; st.next_id += 1
    mk = np.isin(st.lab, [A, B]); mb = mk & (st.kind == 0); mc = mk & (st.kind == 1)
    Mb, Mc = float(st.m[mb].sum()), float(st.m[mc].sum()); ron = (la["r_on"] ** 3 + lb["r_on"] ** 3) ** (1 / 3)
    X = centroid(st, mb, la["X"])
    st.labels[C] = dict(r_on=ron, r_e=supply_edge(Mb, Mc, ron), X=X, birth=t, alive=True, union=[A, B, C], Mb0=Mb, Mc0=Mc)
    sa, sb = st.sectors[A], st.sectors[B]; sa["alive"] = sb["alive"] = False
    tau = st.labels[C]["r_e"] / (G * Mb * A0) ** 0.25
    st.sectors[C] = dict(members=[C], Dt=sa["Dt"] + sb["Dt"], Ps=sa["Ps"] + sb["Ps"], As=np.zeros(3), alive=True,
                         ramp=(dict(t_m=t, tau=tau, A=A, B=B, C=C) if mode == "RAMP" else None))
    st.alias[A] = C; st.alias[B] = C
    if mode == "INSTANT": finish_merge(st, C)
    ev = dict(t=t, A=A, B=B, C=C, mode=mode, tau=tau, r_e_C=st.labels[C]["r_e"], r_on_C=ron)
    st.events.append(ev)
    return ev
def finish_merge(st, C):
    u = st.labels[C]["union"]
    if u:
        st.lab[np.isin(st.lab, u)] = C
        for x in u:
            if x != C: st.labels[x]["alive"] = False
        st.labels[C]["union"] = None
    st.sectors[C]["ramp"] = None; st.sectors[C]["members"] = [C]

def bound_fraction(st, F, SX):
    """MR1 (CFG947 M-R): mass fraction of a label's baryons with E = v_rel^2/2 + Phi_own < 0, Phi_own from its own baryons, cold and
    source in its sub-box (isolated)."""
    phi = own_potential(F["rho_b"] + F["rho_c"] + SX, F["n"])
    mk = F["mb"] | F["mc"]; V = (st.m[mk][:, None] * st.v[mk]).sum(0) / st.m[mk].sum()
    pb = st.x[F["mb"]]; E = 0.5 * ((st.v[F["mb"]] - V) ** 2).sum(1) + sub_interp(phi, pb, F["c"], F["h"], F["n"])
    return float(st.m[F["mb"]][E < 0].sum() / st.m[F["mb"]].sum())

# ---------------------------------------------------------------- the run loop (KDK leapfrog; sectors' D_t / P_s on the same scheme)
def run(st, draw, merge="NONE", t_end=20.0, s_of=lambda t: 1.0, stop=None, diag=None, hover=None, tag=""):
    t = 0.0; nsteps = int(round(t_end / DT)); tw = time.time()
    acc, recs, S, g = forces(st, t, draw, s_of(t))
    ser = dict(t=[], Pm=[], Dsum=[], Ps=[], Asabs=[], J=[], Mph=[], clip=[], zs=[], miss=[], missrel=[], head=[], nlab=[], strays=[], hover=[])
    phi_prev = potential(S); trig = []
    def record(t, recs, S, J):
        ser["t"].append(t); ser["Pm"].append((st.m[:, None] * st.v).sum(0).tolist())
        ser["Dsum"].append(sum((r["Dreal"] for r in recs.values()), np.zeros(3)).tolist())
        ser["Ps"].append(sum((st.sectors[s]["Ps"] for s in recs), np.zeros(3)).tolist())
        ser["Asabs"].append(float(sum(np.linalg.norm(r["As"]) for r in recs.values())))
        ser["J"].append(J); ser["Mph"].append(float(sum(r["Mph"] for r in recs.values())))
        ser["clip"].append(bool(any(r["info"]["clipped"] for r in recs.values())))
        ser["zs"].append(float(max([r["zs"] for r in recs.values()] + [0.0])))
        ser["miss"].append(float(max([r["miss"] for r in recs.values()] + [0.0])))
        ser["missrel"].append(float(max([r["miss"] / max(r["Dscale"], 1e-300) for r in recs.values()] + [0.0])))
        ser["head"].append(float(max([r["info"]["headroom"] for r in recs.values()] + [0.0])))
        ser["nlab"].append(int(sum(1 for s in st.sectors.values() if s["alive"])))
        ser["strays"].append(float(sum(F["strays_b"] for r in recs.values() for F in r["comps"])))
        if hover is not None: ser["hover"].append(hover(st, acc))
    record(t, recs, S, 0.0)
    if diag is not None: diag(st, t, recs, 0)
    for k in range(nsteps):
        st.v += acc * DT / 2
        for sec in st.sectors.values():
            if sec["alive"]: sec["Ps"] = sec["Ps"] + sec["As"] * DT / 2
        st.x = (st.x + st.v * DT) % L
        for sec in st.sectors.values():
            if sec["alive"]: sec["Dt"] = sec["Dt"] + sec["Ps"] * DT
        t = (k + 1) * DT
        refreshed = (k + 1) % REFRESH == 0
        if refreshed: refresh_labels(st, t)
        if merge in ("RAMP", "INSTANT"):
            act = [s for s, sec in st.sectors.items() if sec["alive"] and sec["ramp"] is None and len(sec["members"]) == 1]
            done = False
            for i in range(len(act)):
                for j in range(i + 1, len(act)):
                    a, b = act[i], act[j]; la, lb = st.labels[a], st.labels[b]
                    if la["r_e"] <= 0 or lb["r_e"] <= 0: continue
                    ma = lab_mask(st, a) & (st.kind == 0); mbm = lab_mask(st, b) & (st.kind == 0)
                    if not (ma.any() and mbm.any()): continue
                    d = np.linalg.norm(wrap(centroid(st, ma, la["X"]) - centroid(st, mbm, lb["X"])))
                    if d < 0.5 * max(la["r_e"], lb["r_e"]):
                        Fa = comp_fields(st, a, update_X=False); prep(Fa); Fa["comp"] = np.where(Fa["shell"], Fa["q"] * Fa["rho_c"], 0.0)
                        Fb = comp_fields(st, b, update_X=False); prep(Fb); Fb["comp"] = np.where(Fb["shell"], Fb["q"] * Fb["rho_c"], 0.0)
                        bfa = bound_fraction(st, Fa, Fa["e"] - Fa["comp"]); bfb = bound_fraction(st, Fb, Fb["e"] - Fb["comp"])
                        ev = do_merge(st, a, b, t, merge); ev.update(step=k + 1, d=float(d), mr1_bound_A=bfa, mr1_bound_B=bfb)
                        trig.append(ev); done = True; break
                if done: break
        for sid, sec in list(st.sectors.items()):
            if sec["alive"] and sec["ramp"] is not None and t >= sec["ramp"]["t_m"] + sec["ramp"]["tau"] - 1e-12:
                finish_merge(st, sid); st.events.append(dict(t=t, ramp_end=sid))
        acc, recs, S, g = forces(st, t, draw, s_of(t))
        st.v += acc * DT / 2
        for sid in recs: st.sectors[sid]["Ps"] = st.sectors[sid]["Ps"] + st.sectors[sid]["As"] * DT / 2
        relief()
        phi = potential(S); nrm = float(np.linalg.norm(phi))
        J = float(np.linalg.norm(phi - phi_prev) / nrm) if nrm > 0 else 0.0; phi_prev = phi
        if trig and trig[-1].get("step") == k + 1 and "J_trigger" not in trig[-1]: trig[-1]["J_trigger"] = J
        record(t, recs, S, J)
        stopnow = stop is not None and stop(st)
        if diag is not None and (refreshed or stopnow): diag(st, t, recs, k + 1)
        if stopnow: break
    ser["wall_s"] = time.time() - tw; ser["triggers"] = trig; ser["events"] = st.events
    log(f"    [{tag}] {len(ser['t']) - 1} steps, t_end {ser['t'][-1]:.2f}, wall {ser['wall_s']:.1f} s, peak RSS {peak_rss_gb():.3f} GB, footprint {footprint_gb():.3f} GB")
    return ser

def book(ser):
    """B(t) = |P_m + sum Ddot_meas - ref| / I, central differences, from step 1; I = gross impulse."""
    Pm = np.array(ser["Pm"]); D = np.array(ser["Dsum"]); n = len(Pm)
    if n < 3: return dict(max_B_over_I=float("nan"), I=0.0)
    Dd = (D[2:] - D[:-2]) / (2 * DT); Pc = Pm[1:-1]; tot = Pc + Dd; Bv = np.linalg.norm(tot - tot[0], axis=1)
    I = float(np.sum(ser["Asabs"]) * DT)
    Ps = np.array(ser["Ps"])[1:-1]
    return dict(max_B_over_I=float(Bv.max() / I) if I > 0 else float("nan"), I=I, max_B=float(Bv.max()),
                max_Ps_vs_Ddot=float(np.max(np.linalg.norm(Ps - Dd, axis=1)) / I) if I > 0 else float("nan"),
                dPm=float(np.linalg.norm(Pm[-1] - Pm[0])), dPm_over_I=float(np.linalg.norm(Pm[-1] - Pm[0]) / I) if I > 0 else float("nan"))

# ---------------------------------------------------------------- global (E4) phantom, MASK trick, ball sums
def ball(X, R):
    g = np.arange(M) * DX; d = [wrap(g - X[a]) for a in range(3)]
    return (d[0][:, None, None] ** 2 + d[1][None, :, None] ** 2 + d[2][None, None, :] ** 2) < R * R
def phantom_spec(gv):
    Fv = nu_m1(np.sqrt((gv ** 2).sum(0)) / A0) * gv
    dk = sum(1j * KG[c] * sfft.rfftn(Fv[c]) for c in range(3))
    return -sfft.irfftn(dk, s=(M, M, M)) / FPG
def global_phantom(pos, mass):
    rho = deposit(pos, mass); rho = rho - rho.mean()
    return phantom_spec(grav(rho))

# ---------------------------------------------------------------- configurations
def cfg_a(rng):
    st = State(); c = np.array([L / 2] * 3)
    add_object(st, rng, 0, 1.0, 0.8, 5.36, 4.0, 20000, 60000, c)
    add_object(st, rng, 1, 0.2, 0.3, 1.07, 1.5, 8000, 16000, c + np.array([12.0, 0, 0]))
    return st
def cfg_H(rng):
    st = State(); add_object(st, rng, 0, 1.0, 0.8, 5.36, 4.0, 20000, 60000, np.array([L / 2] * 3)); return st
def cfg_b(rng):
    st = State(); add_object(st, rng, 0, 1.0, 0.8, 5.36, 4.0, 20000, 60000, np.array([L / 2] * 3), cold_offset=(1.5, 0, 0)); return st
def cfg_c(rng):
    st = State(); c = np.array([L / 2] * 3)
    add_object(st, rng, 0, 0.5, 0.6, 2.68, 3.0, 12000, 36000, c + np.array([-7.0, -0.25, 0]), vbulk=(0.5, 0, 0))
    add_object(st, rng, 1, 0.5, 0.6, 2.68, 3.0, 12000, 36000, c + np.array([7.0, 0.25, 0]), vbulk=(-0.5, 0, 0))
    return st
def plural_label(st, obj):
    sel = (st.obj == obj) & (st.kind == 0)
    ul, inv = np.unique(st.lab[sel], return_inverse=True); ms = np.bincount(inv, weights=st.m[sel])
    return int(ul[np.argmax(ms)])
def purity(st, obj, lid):
    sel = (st.obj == obj) & (st.kind == 0); return float(st.m[sel & (eff_labels(st) == lid)].sum() / st.m[sel].sum())

# ---------------------------------------------------------------- (a): satellite infall, own-domain phantom, EFE
def run_a(rng_seed=9521, want_mu1_only=False):
    st = cfg_a(np.random.default_rng(rng_seed)); r0 = refresh_labels(st, 0.0)
    lH, ls = plural_label(st, 0), plural_label(st, 1)
    log(f"  (a) t = 0 labels: {r0['n_peaks']} resolved peaks, labels born {r0['born']}; host label {lH}, satellite label {ls}; "
        f"r_ON/r_e host {st.labels[lH]['r_on']:.3f}/{st.labels[lH]['r_e']:.3f}, satellite {st.labels[ls]['r_on']:.3f}/{st.labels[ls]['r_e']:.3f}")
    snaps = []
    def dist(st):
        mh = (st.lab == lH) & (st.kind == 0) & (st.obj == 0); ms = (st.lab == ls) & (st.kind == 0) & (st.obj == 1)
        return float(np.linalg.norm(wrap(centroid(st, mh, st.labels[lH]["X"]) - centroid(st, ms, st.labels[ls]["X"]))))
    def diag(st, t, recs, k):
        d = dist(st); rec = dict(step=k, t=t, d=d)
        rec["purity_s"] = purity(st, 1, ls); rec["purity_H"] = purity(st, 0, lH); rec["ls_ne_lH"] = ls != lH
        rec["labels_alive"] = int(sum(1 for s in st.sectors.values() if s["alive"]))
        Ff = comp_fields(st, ls, update_X=False)
        sub = State(); keep = st.lab == ls
        sub.x, sub.v, sub.m, sub.kind, sub.obj, sub.lab = st.x[keep], st.v[keep], st.m[keep], st.kind[keep], st.obj[keep], st.lab[keep]
        sub.labels = copy.deepcopy(st.labels)
        Fa = comp_fields(sub, ls, update_X=False)
        rec["a1_max_dsph_rel"] = float(np.max(np.abs(Ff["s_ph"] - Fa["s_ph"])) / np.max(np.abs(Fa["s_ph"])))
        rec["a1_dlog_Mph"] = float(abs(math.log10(Ff["Mph_edge"]) - math.log10(Fa["Mph_edge"])))
        rec["Mph_own"] = Ff["Mph_edge"]; rec["strays_b_s"] = Ff["strays_b"]
        Xs = Ff["X"]; bl = ball(Xs, st.labels[ls]["r_e"])
        bar = st.kind == 0; sat = bar & (st.lab == ls); oth = bar & (st.lab != ls)
        M_all = float((global_phantom(st.x[bar], st.m[bar]) * bl).sum() * DV)
        M_oth = float((global_phantom(st.x[oth], st.m[oth]) * bl).sum() * DV)
        M_sat = float((global_phantom(st.x[sat], st.m[sat]) * bl).sum() * DV)
        rec["E4_EFE_dex"] = math.log10((M_all - M_oth) / M_sat)
        rho = deposit(st.x[bar], st.m[bar]); rho = rho - rho.mean(); gall = grav(rho)
        gext = (st.m[sat][:, None] * interp(gall, st.x[sat])).sum(0) / st.m[sat].sum()
        M_mask = float((phantom_spec(gall - gext[:, None, None, None]) * bl).sum() * DV)
        rec["MASK_resid_dex"] = math.log10(M_mask / M_sat); rec["own_vs_E4iso_dex"] = math.log10(Ff["Mph_edge"] / M_sat)
        rec["g_ext_at_s"] = float(np.linalg.norm(gext))
        snaps.append(rec)
        relief()
    def hover(st, acc):
        sb = (st.obj == 1) & (st.kind == 0) & (st.lab == ls); sc = (st.obj == 1) & (st.kind == 1) & (st.lab == ls); sa = st.obj == 1
        ab = (st.m[sb][:, None] * acc[sb]).sum(0) / st.m[sb].sum(); ac = (st.m[sc][:, None] * acc[sc]).sum(0) / st.m[sc].sum()
        aa = (st.m[sa][:, None] * acc[sa]).sum(0) / st.m[sa].sum()
        return float(np.linalg.norm(ab - ac) / max(np.linalg.norm(aa), 1e-300))
    ser = run(st, "DIPSLAVE", "NONE", 30.0, stop=lambda s: dist(s) <= 5.0, diag=diag, hover=hover, tag="(a) DIPSLAVE")
    pick = {}
    for want in (12.0, 8.0, 5.0):
        j = int(np.argmin([abs(r["d"] - want) for r in snaps])) if want != 5.0 or min(r["d"] for r in snaps) <= 5.0 else int(np.argmin([r["d"] for r in snaps]))
        pick[f"d{want:g}"] = snaps[j]
    hv = np.array(ser["hover"]); tt = np.array(ser["t"])
    return dict(labels=dict(host=lH, sat=ls, r_on_H=st.labels[lH]["r_on"], r_e_H=st.labels[lH]["r_e"], r_on_s=st.labels[ls]["r_on"],
                            r_e_s=st.labels[ls]["r_e"], born_t0=r0["born"], n_peaks_t0=r0["n_peaks"]),
                snapshots=pick, all_snaps=snaps, end=snaps[-1], book=book(ser),
                hover=dict(median=float(np.median(hv[tt >= 1])), max=float(np.max(hv[tt >= 1]))),
                t_end=ser["t"][-1], steps=len(ser["t"]) - 1, wall_s=ser["wall_s"], max_clip=bool(any(ser["clip"])),
                max_zs=float(max(ser["zs"])), nlab_max=int(max(ser["nlab"])))

# ---------------------------------------------------------------- (b): asymmetric host, switch-on ramp, momentum books
def s_ramp(t):
    return 0.5 * (1 - math.cos(math.pi * min(t, 10.0) / 10.0))
def run_b(draw, seed=9522):
    st = cfg_b(np.random.default_rng(seed)); r0 = refresh_labels(st, 0.0)
    nl = len(r0["born"]); fallback = False
    if nl > 1:
        lh = plural_label(st, 0)
        for lid in r0["born"]:
            if lid != lh:
                st.lab[st.lab == lid] = lh; st.labels[lid]["alive"] = False; st.sectors[lid]["alive"] = False
        fallback = True
    ser = run(st, draw, "NONE", 20.0, s_of=s_ramp, hover=lambda s_, a_: float(np.linalg.norm(sum((sec["Dt"] for sec in s_.sectors.values() if sec["alive"]), np.zeros(3)))), tag=f"(b) {draw}")
    bk = book(ser); tt = np.array(ser["t"]); cl = np.array(ser["clip"]); mr = np.array(ser["missrel"]); Dt = np.array(ser["hover"])
    diagb = dict(first_clip_t=(float(tt[cl][0]) if cl.any() else None), first_bad_miss_t=(float(tt[mr > 1e-9][0]) if (mr > 1e-9).any() else None),
                 Dt_norm_t=[[float(a), float(b)] for a, b in zip(tt[::25], Dt[::25])], Dreal_t=[[float(a), float(np.linalg.norm(b))] for a, b in zip(tt[::25], np.array(ser["Dsum"])[::25])],
                 head_t=[[float(a), float(b)] for a, b in zip(tt[::25], np.array(ser["head"])[::25])])
    return dict(diag=diagb, draw=draw, n_labels_t0=nl, fallback=fallback, book=bk, any_clip=bool(any(ser["clip"])),
                n_clip_steps=int(sum(ser["clip"])), max_miss_rel=float(max(ser["missrel"])), max_headroom=float(max(ser["head"])),
                max_zs=float(max(ser["zs"])), max_As=float(max(ser["Asabs"])), wall_s=ser["wall_s"], steps=len(ser["t"]) - 1)

# ---------------------------------------------------------------- (c): two-halo merger, phantom continuity
def run_c(mode, seed=9523, draw="DIPSLAVE"):
    st = cfg_c(np.random.default_rng(seed)); r0 = refresh_labels(st, 0.0)
    lA, lB = plural_label(st, 0), plural_label(st, 1)
    pur = dict(A=purity(st, 0, lA), B=purity(st, 1, lB), distinct=lA != lB)
    def sep(st, acc):
        ma = (st.obj == 0) & (st.kind == 0); mb_ = (st.obj == 1) & (st.kind == 0)
        ca = centroid(st, ma, st.x[ma][0]); cb = centroid(st, mb_, st.x[mb_][0])
        return float(np.linalg.norm(wrap(ca - cb)))
    ser = run(st, draw, mode, 30.0, hover=sep, tag=f"(c) {mode} {draw}" + (" FB-ZS" if FBZS else ""))
    J = np.array(ser["J"]); tt = np.array(ser["t"]); sp = np.array(ser["hover"]); cl = np.array(ser["clip"])
    diagc = dict(t_maxJ=float(tt[1:][np.argmax(J[1:])]), first_clip_t=(float(tt[cl][0]) if cl.any() else None), n_clip_steps=int(cl.sum()),
                 clip_t_range=([float(tt[cl][0]), float(tt[cl][-1])] if cl.any() else None),
                 J_gt_0p03=[[float(a), float(b)] for a, b in zip(tt[1:][J[1:] > 0.03], J[1:][J[1:] > 0.03])][:25],
                 max_J_before_first_clip=(float(J[1:][tt[1:] < tt[cl][0]].max()) if cl.any() and (tt[1:] < tt[cl][0]).any() else float(J[1:].max())),
                 sep_min=float(sp.min()), t_sep_min=float(tt[np.argmin(sp)]), sep_end=float(sp[-1]),
                 sep_t=[[float(a), float(b)] for a, b in zip(tt[::50], sp[::50])],
                 max_head=float(max(ser["head"])), max_missrel=float(max(ser["missrel"])),
                 max_J_converged_steps=float(J[1:][~cl[1:]].max()) if (~cl[1:]).any() else None,
                 max_J_infeasible_steps=float(J[1:][cl[1:]].max()) if cl[1:].any() else None)
    if ser["triggers"]:
        tm_ = ser["triggers"][0]["t"]; tau_ = ser["triggers"][0]["tau"]; t1 = tt[1:]
        pre = t1 < tm_ - 1e-9; ramp_ = (t1 >= tm_ - 1e-9) & (t1 <= tm_ + tau_ + 1e-9); post = t1 > tm_ + tau_ + 1e-9
        diagc.update(max_J_pre_trigger=float(J[1:][pre].max()) if pre.any() else None, max_J_ramp_window=float(J[1:][ramp_].max()) if ramp_.any() else None,
                     max_J_post_ramp=float(J[1:][post].max()) if post.any() else None)
    out = dict(diag=diagc, mode=mode, labels=dict(A=lA, B=lB, born_t0=r0["born"], purity_t0=pur,
               r_on_A=st.labels[lA]["r_on"], r_e_A=st.labels[lA]["r_e"], r_on_B=st.labels[lB]["r_on"], r_e_B=st.labels[lB]["r_e"]),
               max_J=float(J[1:].max()), median_J=float(np.median(J[1:])), book=bk if (bk := book(ser)) else None,
               max_zs=float(max(ser["zs"])), any_clip=bool(any(ser["clip"])), max_miss_rel=float(max(ser["missrel"])),
               triggers=[{k: (v if not isinstance(v, np.ndarray) else v.tolist()) for k, v in tr.items()} for tr in ser["triggers"]],
               Mph_first=ser["Mph"][0], Mph_last=ser["Mph"][-1], wall_s=ser["wall_s"], steps=len(ser["t"]) - 1,
               max_dMph_rel=float(np.max(np.abs(np.diff(ser["Mph"])) / np.maximum(np.array(ser["Mph"][1:]), 1e-300))))
    if ser["triggers"]:
        ts = ser["triggers"][0]["step"]; out["J_trigger"] = float(J[ts]); out["t_trigger"] = ser["triggers"][0]["t"]
        out["max_J_excl_trigger_window"] = float(np.max(np.delete(J[1:], [ts - 1])))
    if mode == "NONE":
        out["mu5"] = mu5_union(st, lA, lB)
        FA = comp_fields(st, lA, update_X=False); prep(FA); FB = comp_fields(st, lB, update_X=False); prep(FB)
        for F in (FA, FB): F["comp"] = np.where(F["shell"], F["q"] * F["rho_c"], 0.0)
        out["mr1_bound_end"] = dict(A=bound_fraction(st, FA, FA["e"] - FA["comp"]), B=bound_fraction(st, FB, FB["e"] - FB["comp"]))
        out["sep_end"] = float(np.linalg.norm(wrap(FA["X"] - FB["X"])))
    return out
def mu5_union(st, lA, lB):
    U = st.next_id + 1000
    mk = np.isin(st.lab, [lA, lB]); mb = mk & (st.kind == 0); mc = mk & (st.kind == 1)
    Mb, Mc = float(st.m[mb].sum()), float(st.m[mc].sum())
    ron = (st.labels[lA]["r_on"] ** 3 + st.labels[lB]["r_on"] ** 3) ** (1 / 3)
    st.labels[U] = dict(r_on=ron, r_e=supply_edge(Mb, Mc, ron), X=centroid(st, mb, st.labels[lA]["X"]), union=[lA, lB], alive=False)
    FU = comp_fields(st, U, update_X=False); bl = ball(FU["X"], st.labels[U]["r_e"])
    def glob(F):
        out = np.zeros((M, M, M)); out[np.ix_(*F["gi"])] += F["s_ph"]; return out
    FA = comp_fields(st, lA, update_X=False); FB = comp_fields(st, lB, update_X=False)
    mA, mB, mU = [float((glob(F) * bl).sum() * DV) for F in (FA, FB, FU)]
    del st.labels[U]
    return dict(M_A=mA, M_B=mB, M_union=mU, ratio=(mA + mB) / mU, r_e_union=supply_edge(Mb, Mc, ron))

# ---------------------------------------------------------------- K controls
def stage_K():
    res = {}
    # K1: PM momentum (S = 0) over 50 steps + discrete third law
    st = cfg_a(np.random.default_rng(9521)); acc = interp(grav(deposit(st.x, st.m)), st.x); P0 = (st.m[:, None] * st.v).sum(0); gross = 0.0
    for k in range(50):
        st.v += acc * DT / 2; st.x = (st.x + st.v * DT) % L
        acc = interp(grav(deposit(st.x, st.m)), st.x); st.v += acc * DT / 2
        gross += float((st.m * np.linalg.norm(acc, axis=1)).sum() * DT)
    dP = float(np.linalg.norm((st.m[:, None] * st.v).sum(0) - P0) / gross)
    rng = np.random.default_rng(1); S = rng.standard_normal((M, M, M)); S -= S.mean()
    rm = deposit(st.x, st.m); gS = grav(S); gm = grav(rm)
    a = (rm[None] * gS).sum((1, 2, 3)) * DV; b = (S[None] * gm).sum((1, 2, 3)) * DV
    tl = float(np.linalg.norm(a + b) / ((np.abs(rm[None] * gS)).sum() * DV))
    res["K1"] = dict(dP_over_gross=dP, third_law_rel=tl, line=1e-12, PASS=bool(dP <= 1e-12 and tl <= 1e-12))
    log(f"  [{'PASS' if res['K1']['PASS'] else 'FAIL'}] K1 PM momentum |dP|/sum|m g|dt = {dP:.3e}; third law {tl:.3e} (line 1e-12)")
    # K2 / K3: isolated H, labels by the machinery
    st = cfg_H(np.random.default_rng(9524)); r0 = refresh_labels(st, 0.0); lH = plural_label(st, 0)
    F = comp_fields(st, lH); lab = st.labels[lH]
    rr = F["rr"]; gr = (F["g"] * F["rv"]).sum(0) / np.maximum(rr, 1e-300)
    sel = (rr >= 3 * DX) & (rr <= 0.9 * lab["r_on"]); edges = np.arange(3 * DX, 0.9 * lab["r_on"] + DX / 2, DX / 2)
    ib = np.digitize(rr[sel], edges); devs = []
    for j in range(1, len(edges)):
        m_ = ib == j
        if m_.sum() < 8: continue
        rmid = float(rr[sel][m_].mean()); gnum = float(-gr[sel][m_].mean())
        gan = G * float(menc(rmid, 1.0, 0.8, 6.4)) / rmid ** 2; devs.append(abs(gnum / gan - 1))
    k2 = float(max(devs))
    res["K2"] = dict(n_labels=len(r0["born"]), r_on=lab["r_on"], max_rel_dev=k2, n_bins=len(devs), line=0.03, PASS=bool(k2 <= 0.03))
    log(f"  [{'PASS' if res['K2']['PASS'] else 'FAIL'}] K2 isolated sub-box field vs truncated Plummer: max |rel dev| {k2:.4f} over {len(devs)} radial bins (3dx..0.9 r_ON = {0.9 * lab['r_on']:.2f}; line 0.03); labels {len(r0['born'])}")
    re = lab["r_e"]; gN = G * float(menc(re, 1.0, 0.8, 6.4)) / re ** 2; Man = re ** 2 * gN * float(nu_m1(gN / A0)) / G
    k3 = abs(F["Mph_edge"] / Man - 1)
    res["K3"] = dict(r_e=re, Mph_num=F["Mph_edge"], Mph_analytic=Man, rel_dev=float(k3), line=0.05, PASS=bool(k3 <= 0.05))
    log(f"  [{'PASS' if res['K3']['PASS'] else 'FAIL'}] K3 own phantom inside r_e = {re:.3f}: {F['Mph_edge']:.5f} vs spherical QUMOND {Man:.5f} (rel dev {k3:.4f}; line 0.05)")
    # K4: nu_mono replica
    y = np.geomspace(1e-6, 1e4, 20001); g_law = y * (1 + nu_m1(y)); mono = bool(np.all(np.diff(g_law) > 0) and np.all(np.diff(nu_m1(y)) < 0))
    yl = np.geomspace(1e-6, 1.0, 5001); dev = float(np.max(np.abs((1 + nu_m1(yl)) / (1 + nu_rar_m1(yl)) - 1)))
    res["K4"] = dict(monotone=mono, max_rel_dev_vs_RAR_y_le_1=dev, Y_P=Y_P, PASS=bool(mono and dev <= 1e-6))
    log(f"  [{'PASS' if res['K4']['PASS'] else 'FAIL'}] K4 nu_mono replica: y nu(y) increasing and nu decreasing on [1e-6, 1e4]: {mono}; max rel dev vs RAR nu for y <= 1: {dev:.2e} (Y_P = {Y_P:.4f})")
    res["ALL_PASS"] = bool(all(res[k]["PASS"] for k in ("K1", "K2", "K3", "K4")))
    return res

# ---------------------------------------------------------------- EST stage: engine-side design numbers (read-only inputs)
def fret_of(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def stage_EST():
    out = {}; cfg654 = os.path.join(HERE, "..", "CFG654_independent_inputs")
    nodes = {}
    for N in (1024, 256):
        dx = 100.0 / N; Rg = np.geomspace(dx, 8.0, 14); eff = float(Rg[Rg >= 0.78125 - 1e-9][0])
        nodes[N] = dict(dx=dx, nodes=Rg.round(5).tolist(), effective_RMIN_node=eff, effective_over_RMIN_cubed=(eff / 0.78125) ** 3)
    out["r_on_grid"] = nodes
    def thresholds(R, Dta, Om_ta, h_ta, fb):
        Mta = (4 * math.pi / 3) * R ** 3 * Dta * Om_ta * 2.775e11; fr = fret_of(math.log10(Mta))
        return dict(R=R, M_ta_Msun_h=Mta, f_ret=fr, M_b_ret_Msun=fr * fb * Mta / h_ta, M_b_all_Msun=fb * Mta / h_ta)
    fb_eng = 0.02237 / (0.02237 + 0.1200)
    try:
        d_cmb = json.load(open(os.path.join(cfg654, "cfg654_delta_ta_cmb.json"))); d_bbn = json.load(open(os.path.join(cfg654, "cfg654_delta_ta.json")))
        D0 = lambda d: float(math.exp(np.interp(0.0, np.log1p(np.array(d["z"])), np.log(np.array(d["D"])))))
        Dc, Db = D0(d_cmb), D0(d_bbn)
        T = np.load(os.path.join(cfg654, "cfg654_ics_tables_cmb.npz")); hc = float(T["h"]); Omc = (float(T["omega_b"]) + float(T["omega_c"])) / hc ** 2
        fbc = float(T["omega_b"]) / (float(T["omega_b"]) + float(T["omega_c"]))
        out["inputs"] = dict(Delta_ta0_cmb=Dc, Delta_ta0_bbn=Db, h_cmb=hc, Om_cmb=Omc, fb_cmb=fbc, fb_engine=fb_eng)
        eff = nodes[1024]["effective_RMIN_node"]
        out["thresholds"] = {
            "CFG947_inputs_R0.78125 (control: 4.815e10)": thresholds(0.78125, Db, 0.315, 0.674, fb_eng),
            "CFG947_inputs_effective_node_1024": thresholds(eff, Db, 0.315, 0.674, fb_eng),
            "native_cmb_R0.78125": thresholds(0.78125, Dc, Omc, hc, fbc),
            "native_cmb_effective_node_1024": thresholds(eff, Dc, Omc, hc, fbc),
            "native_cmb_effective_node_256": thresholds(nodes[256]["effective_RMIN_node"], Dc, Omc, hc, fbc)}
    except Exception as ex:
        out["inputs_error"] = repr(ex)
    # NC1x measured stage timings and peak RSS (read only)
    nc = glob.glob(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg654_work", "NC1x", "*_lean.json"))
    base = dict(deposit=15758.447088718414, forces=28958.334972143173, accel=9407.661561489105, drift=118.19273471832275,
                snap=4314.77721452713, maxrss_gb=44.332924928, n_hosts_z0=32399, n_hosts_z05=56162, n_hosts_z1=63140)
    if nc:
        r = json.load(open(nc[0])); tm = r["timing_s"]
        base.update(deposit=tm["deposit"], forces=tm["forces"], accel=tm["accel"], drift=tm["drift"], snap=tm["snap"], maxrss_gb=r["maxrss_gb"],
                    n_hosts_z0=r["snap"]["z0"].get("m1_n_hosts"), n_hosts_z05=r["snap"]["z0.5"].get("m1_n_hosts"), n_hosts_z1=r["snap"]["z1"].get("m1_n_hosts"))
        base["source"] = "read from the NC1x run JSON"
    else:
        base["source"] = "quoted (NC1x JSON not found)"
    out["NC1x"] = base
    nst = 150; per = {k: base[k] / nst for k in ("deposit", "forces", "accel")}
    tpass = per["deposit"]; tF = 2.0; tF_lo, tF_hi = 1.5, 3.0
    N3 = 1024 ** 3; GB = 1e9
    def fftcost(P, tf): return tf * (P ** 3 * math.log2(P ** 3)) / (N3 * math.log2(N3))
    dx = 100.0 / 1024; eff = nodes[1024]["effective_RMIN_node"]
    h = int(math.ceil(eff / dx)) + 2; n = 2 * h + 1; P = sfft.next_fast_len(2 * n - 1, real=True)
    hb = int(math.ceil(8.0 / dx)) + 2; nb = 2 * hb + 1; Pb = sfft.next_fast_len(2 * nb - 1, real=True)
    scen = []
    for NL in (1000, 5000, 20000, 63140):
        ragged = NL * n ** 3 * 2 * 4 / GB; batches = max(1, math.ceil(ragged / 1.5))
        for scheme in ("exact3d", "hybrid", "mask"):
            if scheme == "exact3d": solve = lambda tf: 4 * 2.0 * NL * fftcost(P, tf)
            elif scheme == "hybrid": solve = lambda tf: 4 * 2.0 * max(1, int(0.05 * NL)) * fftcost(P, tf)
            else: solve = lambda tf: 0.0
            dE4 = -11 if scheme != "mask" else 0
            dep = (0.3 + (batches - 1)) * tpass if scheme != "mask" else 0.3 * tpass
            add = lambda tf: dE4 * tf + dep + solve(tf) + 0.1 * tpass + 0.05 * tpass
            base_step = sum(per.values()) + base["drift"] / nst
            tot = lambda tf: (nst * (base_step + add(tf)) + base["snap"]) / 3600.0
            mem_add = 1.5 + 4 * Pb ** 3 / 2 * 8 / GB + 3 * Pb ** 3 / 2 * 8 / GB
            scen.append(dict(N_labels=NL, scheme=scheme, ragged_GB=round(ragged, 3), batches=batches,
                             d_step_s=dict(lo=round(add(tF_lo), 1), mid=round(add(tF), 1), hi=round(add(tF_hi), 1)),
                             wall_h_per_run=dict(lo=round(tot(tF_lo), 2), mid=round(tot(tF), 2), hi=round(tot(tF_hi), 2)),
                             peak_RSS_GB_labels_on_disk=dict(best=round(base["maxrss_gb"] - (4.295 if scheme != "mask" else 0) + mem_add, 2),
                                                             worst=round(base["maxrss_gb"] + mem_add, 2)),
                             peak_RSS_GB_labels_in_RAM_worst=round(base["maxrss_gb"] + mem_add + 4.295, 2)))
    out["model"] = dict(t_pass_s=tpass, t_fft_1024_s=dict(lo=tF_lo, mid=tF, hi=tF_hi), small_fft_inefficiency=2.0,
                        smallest_label_subbox=dict(r_on=eff, h=h, n=n, P=P), largest_label_subbox=dict(r_on=8.0, h=hb, n=nb, P=Pb),
                        baseline_wall_h=round((sum(base[k] for k in ("deposit", "forces", "accel", "drift", "snap"))) / 3600.0, 2),
                        notes="E4 (11 full-transform equivalents) removed except in 'mask'; labelled ragged deposit replaces deposit_cond "
                              "(+0.3 pass overhead, +1 pass per extra batch); label refresh +0.1 pass/step; F' gathers + dipole "
                              "solves +0.05 pass/step; hybrid = 3D sub-box solve for 5% of labels, spherical own-phantom for the rest")
    out["scenarios"] = scen
    return out

# ---------------------------------------------------------------- main
def dump(name, obj):
    def conv(o):
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, (np.bool_,)): return bool(o)
        raise TypeError(type(o))
    json.dump(obj, open(os.path.join(HERE, name), "w"), indent=1, default=conv)

if __name__ == "__main__":
    log("CFG952  LDT PM-engine prototype (separate 64^3 toy; no CFG650/654 import)   stage=" + ("MUTATE" if MUTATE else STAGE))
    log("  criteria 844ce293d; A1 7a3ade021 (pre-result); kappa = 1/2 FITTED; footings never pooled; not theory closed")
    log(f"  toy: G = a0 = 1, L = {L}, M = {M}, dx = {DX}, rho_ta = {RHO_TA}, R_min = {RMIN}, x_h = {XH}, dt = {DT}, sigma_sm = {SIG_SM}")
    if STAGE == "K" and not MUTATE:
        log("\n==================== K CONTROLS ====================")
        res = stage_K(); res["peak_rss_gb"] = peak_rss_gb(); res["wall_s"] = time.time() - T0
        log(f"  K controls: {'ALL PASS' if res['ALL_PASS'] else 'FAIL -> main classes VOID'}   (wall {res['wall_s']:.1f} s, peak RSS {res['peak_rss_gb']:.3f} GB)")
        dump("cfg952_results_K.json", res); sys.exit(0 if res["ALL_PASS"] else 1)
    if STAGE == "POSTHOC" and not MUTATE:
        log("\n==================== POST-HOC STAGE (A2 4141650f1; reported, no class weight) ====================")
        FBZS = True; res = {}
        Bv = run_b("DIPSLAVE"); res["PH_b"] = Bv
        log(f"   PH-b DIPSLAVE+FB-ZS: max B/I {Bv['book']['max_B_over_I']:.3e}; |dP_m|/I {Bv['book']['dPm_over_I']:.3e}; infeasible steps {Bv['n_clip_steps']} (first t {Bv['diag']['first_clip_t']}); "
            f"max dipole miss/scale {Bv['max_miss_rel']:.3e}; zero-sum max {Bv['max_zs']:.2e}")
        for mode, dr in (("RAMP", "DIPSLAVE"), ("INSTANT", "DIPSLAVE"), ("NONE", "DIPSLAVE"), ("RAMP", "DIPFREE")):
            Cv = run_c(mode, draw=dr); key = f"PH_c_{mode}" + ("_DIPFREE" if dr == "DIPFREE" else ""); res[key] = Cv; dg = Cv["diag"]
            log(f"   {key}: max J {Cv['max_J']:.4f} (median {Cv['median_J']:.4f}); J at trigger {Cv.get('J_trigger', float('nan')):.4f} (t {Cv.get('t_trigger', float('nan'))}); "
                f"J max pre-trigger {dg.get('max_J_pre_trigger')}, ramp window {dg.get('max_J_ramp_window')}, post {dg.get('max_J_post_ramp')}; "
                f"converged-steps max J {dg['max_J_converged_steps']}, infeasible-steps max J {dg['max_J_infeasible_steps']}")
            log(f"        zero-sum max {Cv['max_zs']:.2e}; infeasible steps {dg['n_clip_steps']}; max dipole miss/scale {Cv['max_miss_rel']:.3e}; book B/I {Cv['book']['max_B_over_I']:.3e}; "
                f"|dP_m|/I {Cv['book']['dPm_over_I']:.3e}; separation min {dg['sep_min']:.2f} (t {dg['t_sep_min']:.2f}), end {dg['sep_end']:.2f}")
        rr = res["PH_c_RAMP"]; ri = res["PH_c_INSTANT"]
        ok = bool(rr["max_J"] <= 0.03 and ri.get("J_trigger", 0.0) >= 0.05)
        res["reading_merge_transition"] = ("ramp continuity attributed to the ramp; c1's frozen failure attributed to the fallback artefact" if ok
                                           else "c1's frozen failure NOT explained by the fallback artefact")
        log(f"  A2 reading rule: RAMP max J {rr['max_J']:.4f} (<= 0.03?) and INSTANT J at trigger {ri.get('J_trigger', float('nan')):.4f} (>= 0.05?) -> {res['reading_merge_transition']}")
        res["peak_rss_gb"] = peak_rss_gb(); res["wall_s"] = time.time() - T0
        log(f"  (wall {res['wall_s']:.1f} s, peak RSS {res['peak_rss_gb']:.3f} GB)")
        dump("cfg952_results_POSTHOC.json", res); sys.exit(0)
    if MUTATE:
        log("\n==================== MUTATE ====================")
        res = {}
        A = run_a(); c = A["snapshots"]["d5"]
        res["Mu1"] = dict(E4_EFE_dex_closest=c["E4_EFE_dex"], d=c["d"], line=0.05, bites=bool(abs(c["E4_EFE_dex"]) >= 0.05))
        log(f"  [{'BITES' if res['Mu1']['bites'] else 'TOOTHLESS'}] Mu1 E4 global phantom: satellite EFE {c['E4_EFE_dex']:+.4f} dex at d = {c['d']:.2f} (line |.| >= 0.05)")
        Bm = run_b("E8")
        res["Mu2"] = dict(max_B_over_I=Bm["book"]["max_B_over_I"], line=1e-2, bites=bool(Bm["book"]["max_B_over_I"] >= 1e-2), detail=Bm)
        log(f"  [{'BITES' if res['Mu2']['bites'] else 'TOOTHLESS'}] Mu2 E8 draw: max B/I = {Bm['book']['max_B_over_I']:.4e} (line >= 1e-2); |dP_m|/I = {Bm['book']['dPm_over_I']:.4e}")
        Cr = run_c("RAMP"); Ci = run_c("INSTANT"); Cn = run_c("NONE")
        jt = Ci.get("J_trigger", float("nan"))
        res["Mu3"] = dict(J_trigger_INSTANT=jt, max_J_RAMP=Cr["max_J"], bites=bool(Ci["triggers"] and jt >= 0.05 and jt >= 2 * Cr["max_J"]),
                          INSTANT=Ci, RAMP=Cr)
        log(f"  [{'BITES' if res['Mu3']['bites'] else 'TOOTHLESS'}] Mu3 INSTANT merge: J_Phi at trigger {jt:.4f} (line >= 0.05 and >= 2 x RAMP max {Cr['max_J']:.4f})")
        res["Mu5"] = dict(ratio=Cn["mu5"]["ratio"], line=1.1, bites=bool(Cn["mu5"]["ratio"] >= 1.1), NONE=Cn)
        log(f"  [{'BITES' if res['Mu5']['bites'] else 'TOOTHLESS'}] Mu5 no merge: sum of own phantoms / union phantom inside r_e,C = {Cn['mu5']['ratio']:.4f} (line >= 1.1); MR1 bound fractions at end A {Cn['mr1_bound_end']['A']:.3f}, B {Cn['mr1_bound_end']['B']:.3f}; separation {Cn['sep_end']:.2f}")
        allb = all(res[k]["bites"] for k in ("Mu1", "Mu2", "Mu3", "Mu5"))
        res["ALL_BITE"] = allb; res["peak_rss_gb"] = peak_rss_gb(); res["wall_s"] = time.time() - T0
        log(f"  MUTATE: {'every tooth bites (exit 1 by design)' if allb else 'a tooth is toothless (exit 2)'}   (wall {res['wall_s']:.1f} s, peak RSS {res['peak_rss_gb']:.3f} GB)")
        dump("cfg952_results_MUTATE.json", res); sys.exit(1 if allb else 2)
    # MAIN
    res = {}
    log("\n==================== (a) satellite: labels, persistence, own-domain phantom ====================")
    A = run_a(); res["a"] = A
    for nm, r in A["snapshots"].items():
        log(f"   snapshot {nm}: step {r['step']} t {r['t']:.2f} d {r['d']:.3f}; purity s {r['purity_s']:.5f} H {r['purity_H']:.5f}; "
            f"a1 max|dsph|/max {r['a1_max_dsph_rel']:.2e}, dlogM {r['a1_dlog_Mph']:.2e}; E4 EFE {r['E4_EFE_dex']:+.4f} dex; MASK {r['MASK_resid_dex']:+.4f} dex; "
            f"own vs E4-iso {r['own_vs_E4iso_dex']:+.4f} dex; |g_ext| {r['g_ext_at_s']:.4f}")
    snaps = A["all_snaps"]
    a0 = all(r["purity_s"] >= 0.99 and r["purity_H"] >= 0.99 and r["ls_ne_lH"] for r in snaps)
    a1 = all(r["a1_dlog_Mph"] <= 1e-6 and r["a1_max_dsph_rel"] <= 1e-6 for r in A["snapshots"].values())
    e = A["end"]; a2 = bool(e["purity_s"] >= 0.99 and e["purity_H"] >= 0.99 and e["ls_ne_lH"] and e["a1_dlog_Mph"] <= 1e-6 and e["a1_max_dsph_rel"] <= 1e-6)
    res["grades"] = dict(a0=a0, a1=a1, a2=a2)
    log(f"  [{'PASS' if a0 else 'FAIL'}] a0 labels: satellite/host purity >= 0.99 at t = 0 and every computed snapshot ({len(snaps)}): min s {min(r['purity_s'] for r in snaps):.5f}, min H {min(r['purity_H'] for r in snaps):.5f}")
    log(f"  [{'PASS' if a1 else 'FAIL'}] a1 no EFE (own-domain): max dlogM {max(r['a1_dlog_Mph'] for r in A['snapshots'].values()):.2e} dex, max|dsph|/max {max(r['a1_max_dsph_rel'] for r in A['snapshots'].values()):.2e}")
    log(f"  [{'PASS' if a2 else 'FAIL'}] a2 dynamic persistence at the end (t = {A['t_end']:.2f}, d = {e['d']:.3f}): purity s {e['purity_s']:.5f}, H {e['purity_H']:.5f}; a1 {e['a1_dlog_Mph']:.2e}")
    log(f"   reported: hover |a_b - a_c|/|a_sat| median {A['hover']['median']:.4f}, max {A['hover']['max']:.4f}; book B/I {A['book']['max_B_over_I']:.2e}; clipped {A['max_clip']}; labels alive max {A['nlab_max']}")
    log("\n==================== (b) momentum books (asymmetric host, switch-on) ====================")
    res["b"] = {}
    for dr in ("DIPSLAVE", "DIPFREE", "LIN"):
        Bv = run_b(dr); res["b"][dr] = Bv
        log(f"   {dr:9s}: max B/I {Bv['book']['max_B_over_I']:.3e}; |dP_m|/I {Bv['book']['dPm_over_I']:.3e}; I {Bv['book']['I']:.4e}; clip steps {Bv['n_clip_steps']}; "
            f"max dipole miss / scale {Bv['max_miss_rel']:.2e}; max headroom q f {Bv['max_headroom']:.3f}; labels t0 {Bv['n_labels_t0']} (fallback {Bv['fallback']})")
        log(f"              first infeasible (clipped) step t {Bv['diag']['first_clip_t']}; first dipole miss > 1e-9 at t {Bv['diag']['first_bad_miss_t']}")
    bs = res["b"]["DIPSLAVE"]
    b1 = bool(bs["book"]["max_B_over_I"] <= 1e-6 and not bs["any_clip"] and bs["max_miss_rel"] <= 1e-9)
    res["grades"]["b1"] = b1
    log(f"  [{'PASS' if b1 else 'FAIL'}] b1 DIPSLAVE book: max B/I {bs['book']['max_B_over_I']:.3e} (<= 1e-6), clipping {bs['any_clip']}, dipole miss {bs['max_miss_rel']:.2e} (<= 1e-9)")
    log("\n==================== (c) merger: phantom continuity (RAMP) ====================")
    C = run_c("RAMP"); res["c"] = C
    tr = C["triggers"][0] if C["triggers"] else None
    log(f"   labels A {C['labels']['A']} B {C['labels']['B']} (purity {C['labels']['purity_t0']}); r_ON/r_e A {C['labels']['r_on_A']:.3f}/{C['labels']['r_e_A']:.3f}")
    if tr: log(f"   trigger at t {tr['t']:.2f} (step {tr['step']}), d {tr['d']:.3f}; tau_m {tr['tau']:.3f}; r_e,C {tr['r_e_C']:.3f}; MR1 bound fractions A {tr['mr1_bound_A']:.3f} B {tr['mr1_bound_B']:.3f}; J at trigger {C.get('J_trigger', float('nan')):.4f}")
    else: log("   NO MERGER TRIGGERED by t = 30")
    c1 = bool(C["max_J"] <= 0.03)
    c2 = bool(C["max_zs"] <= 1e-12 and C["book"]["max_B_over_I"] <= 1e-6)
    res["grades"]["c1"] = c1; res["grades"]["c2"] = c2
    dg = C["diag"]
    log(f"   diagnostics: max J at t {dg['t_maxJ']:.2f}; clipped (Newton infeasible) steps {dg['n_clip_steps']} over t {dg['clip_t_range']}; max J before the first clip {dg['max_J_before_first_clip']:.4f}; "
        f"object separation min {dg['sep_min']:.2f} at t {dg['t_sep_min']:.2f}, end {dg['sep_end']:.2f}")
    log(f"  [{'PASS' if c1 else 'FAIL'}] c1 RAMP max J_Phi {C['max_J']:.4f} (<= 0.03); median {C['median_J']:.4f}; max per-step |dM_ph,eff|/M {C['max_dMph_rel']:.4f}")
    log(f"  [{'PASS' if c2 else 'FAIL'}] c2 zero-sum max {C['max_zs']:.2e} (<= 1e-12); book max B/I {C['book']['max_B_over_I']:.3e} (<= 1e-6); clipping {C['any_clip']}")
    log("\n==================== EST (design numbers; reported) ====================")
    est = stage_EST(); res["EST"] = est
    g1 = est["r_on_grid"][1024]; g2 = est["r_on_grid"][256]
    log(f"   r_ON grid 1024^3: effective RMIN node {g1['effective_RMIN_node']:.4f} Mpc/h (x{g1['effective_over_RMIN_cubed']:.3f} in M_ta); 256^3: {g2['effective_RMIN_node']:.4f}")
    for k, v in est.get("thresholds", {}).items():
        log(f"   {k}: R {v['R']:.4f}  M_ta {v['M_ta_Msun_h']:.4e} Msun/h  f_ret {v['f_ret']:.4f}  M_b,ret {v['M_b_ret_Msun']:.4e} Msun  (all baryons {v['M_b_all_Msun']:.4e})")
    log(f"   NC1x baseline ({est['NC1x']['source']}): wall {est['model']['baseline_wall_h']} h compute, peak RSS {est['NC1x']['maxrss_gb']:.2f} GB; hosts z0/0.5/1 {est['NC1x']['n_hosts_z0']}/{est['NC1x']['n_hosts_z05']}/{est['NC1x']['n_hosts_z1']}")
    for s in est["scenarios"]:
        log(f"   N_L {s['N_labels']:6d} {s['scheme']:8s}: ragged {s['ragged_GB']:.2f} GB ({s['batches']} batch); d_step {s['d_step_s']['lo']:+.0f}/{s['d_step_s']['mid']:+.0f}/{s['d_step_s']['hi']:+.0f} s; "
            f"wall/run {s['wall_h_per_run']['lo']}/{s['wall_h_per_run']['mid']}/{s['wall_h_per_run']['hi']} h; peak RSS (labels on disk) {s['peak_RSS_GB_labels_on_disk']['best']}-{s['peak_RSS_GB_labels_on_disk']['worst']} GB; labels in RAM worst {s['peak_RSS_GB_labels_in_RAM_worst']} GB")
    gr = res["grades"]; allp = all(gr[k] for k in ("a0", "a1", "a2", "b1", "c1", "c2"))
    kres = None
    try: kres = json.load(open(os.path.join(HERE, "cfg952_results_K.json")))
    except Exception: pass
    kpass = bool(kres and kres.get("ALL_PASS"))
    cls = "VOID" if not kpass else ("SMOKE PASS" if allp else "SMOKE PARTIAL")
    res["class"] = cls; res["K_all_pass"] = kpass; res["peak_rss_gb"] = peak_rss_gb(); res["wall_s"] = time.time() - T0
    log(f"\n  GRADES: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in gr.items()))
    log(f"  LANE CLASS: {cls}" + ("  (design ready for a 256^3 validation stage; not for production)" if cls == "SMOKE PASS" else
                                   ("  (design needs revision: " + ", ".join(k for k, v in gr.items() if not v) + ")" if cls == "SMOKE PARTIAL" else "  (K failed or missing)")))
    log(f"  (wall {res['wall_s']:.1f} s, peak RSS {res['peak_rss_gb']:.3f} GB)")
    dump("cfg952_results.json", res)
    sys.exit(0)
