#!/usr/bin/env python3
"""CFG596 lean engine (FROZEN_CRITERIA.md, commit f6c27d401): a memory-lean COPY of CFG527's cfg527_pm.py
(sha256 aeabd0ba..., the census lineage CFG518 -> 521 -> 524 -> 527 used by CFG530), switch RES (census, shell draw, NOFILT,
RC = 0) and the S0 control.  NO formula, constant, threshold, switch, mask rule, time step or output definition is changed.

Engineering only (the frozen list):
  * in-place padded real FFTs done axis by axis (bitwise identical to scipy rfftn / irfftn; checked in cfg596_validate.py);
  * slab-wise evaluation of every large elementwise expression (bitwise identical), 1/k^2 computed per slab;
  * kick / kick fused per component and the drift as one pass -> no stored particle accelerations; per-component CIC interpolation;
  * f_ret painted as a uint8 code into a float32 table (bitwise identical values);
  * gb recomputed per component (twice) instead of three stored fields (bitwise identical);
  * spill of temporaries to disk (CFG596_SPILL=1);
  MODE = exact (CFG596_MODE=exact): float64 wrapped positions + float64 momenta, unchunked deposit, original six-field tidal transform,
         original IC routine -> must reproduce cfg527_pm.py bit for bit (gate V-E);
  MODE = lean (default): float32 Lagrangian displacement + float32 momentum; windowed chunked deposit; factorised tidal transforms
         (kx-free factors applied after the axis-0 transform); component-wise in-place IC (gate V-L tolerances).
Snapshots: the engine's own z = 1, 0.5, 0 (original side effects on the catchment / f_ret state) plus EXTRA steps (CFG596_EXTRA, default
'128,141' = z 0.7548, 0.2562) that are measurement only (that state is saved and restored).  Each snapshot stores particle P(k), sigma8,
the GRAVITATING P(k), sigma8 (delta_grav = -k^2 phi_k a / (1.5 Om), CFG555 definition), and 256^3 block means of both fields.
Usage: python3 cfg596_pm.py SWITCH(RES|S0) FOOT(canonical|alt) N      env: CFG596_L, CFG596_NSEED, CFG596_RMIN, CFG596_THREADS, CFG596_WORK,
       CFG596_MODE, CFG596_SPILL, CFG596_MAXSTEPS (stop early, memory tests), CFG596_SEED.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys
NTH = int(os.environ.get("CFG596_THREADS", "4"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import json, math, time, resource, gc
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from scipy import fft as sfft
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.environ.get("CFG596_WORK", os.path.join(EXT, "cfg596_work"))
DTA_FILE = os.path.join(EXT, "cfg527_work", "cfg361_delta_ta_table.json")      # read only (CFG530 copies this file)
MODE = os.environ.get("CFG596_MODE", "lean"); assert MODE in ("lean", "exact")
SPILL = os.environ.get("CFG596_SPILL", "0") == "1"
MAXSTEPS = int(os.environ.get("CFG596_MAXSTEPS", "100000"))
EXTRA = [int(x) for x in os.environ.get("CFG596_EXTRA", "128,141").split(",") if x.strip()]
RC = 0.0; MIX = "NOFILT"; VETO = False; FRETX = 1.0
_INC = {"mask": None, "catch": None, "fcode": None, "ftab": None, "calls": 0}     # mask / catch packed bits; fcode a DField
FRET_MODE = "census"; NOCOMP = False; DRAW = "SHELL"
RMIN_PHYS = float(os.environ.get("CFG596_RMIN", "1.56"))
MIXES = {"MIXA": (0.28, 0.54, 0.18), "MIXB": (0.57, 0.25, 0.18), "HOT1": (0.0, 1.0, 0.0), "NOFILT": (0.0, 0.0, 1.0)}
MUTATE = False
DIAGX = True

# ---------------------------------------------------------------- constants (L352 values; cfg527_pm.py verbatim)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om; FB = om_b / (om_b + om_c)
NS, SIG8 = 0.965, 0.811
MPC = 3.0856775814913673e22
ACC_UNIT = 1e10 * h / MPC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
W0, WA = -0.838, -0.62
L = float(os.environ.get("CFG596_L", "200")); ZI = 49.0; AI = 1.0 / (1 + ZI)
SEED = int(os.environ.get("CFG596_SEED", "359")); NSEED = int(os.environ.get("CFG596_NSEED", "256"))
EPS = 0.077
E = lambda a: math.sqrt(Om / a ** 3 + OL)

def a0_code(a, branch, foot):
    base = A0[foot] / ACC_UNIT
    if branch == "FLAT": return base
    if branch == "CRIT": return base * E(a)
    if branch == "DE": return base * math.sqrt(a ** (-3 * (1 + W0 + WA)) * math.exp(-3 * WA * (1 - a)))
    raise ValueError(branch)

def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y

def T_eh(k):
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000)
_PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_PK *= SIG8 ** 2 / (np.trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
def P_lin0(k):
    return np.interp(np.log(np.maximum(k, 1e-5)), np.log(_KG), _PK, left=0, right=0)
def Dgrow(a):
    g = lambda x: quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, x)[0] * E(x)
    return g(a) / g(1.0)
def fgrow(a, e=1e-4):
    return (math.log(Dgrow(a * (1 + e))) - math.log(Dgrow(a * (1 - e)))) / (2 * e)
def dta_table():
    return json.load(open(DTA_FILE))

STAGE = ["init"]; MEMST = {}
try:
    import ctypes
    _LIBC = ctypes.CDLL("/usr/lib/libSystem.dylib"); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception:
    _LIBC = None
RELIEF = os.environ.get("CFG596_RELIEF", "1") == "1"
def _relief_loop():
    while True:
        time.sleep(1.0)
        _LIBC.malloc_zone_pressure_relief(None, 0)
if RELIEF and _LIBC is not None:
    import threading
    threading.Thread(target=_relief_loop, daemon=True).start()          # keep RSS ~ live memory between stage changes too
def stage(name):
    """stage label (memory profile) + return freed malloc pages to the OS (macOS keeps freed pages resident as 'reusable'
    until pressure; this keeps the process RSS equal to its live memory; no effect on any number)."""
    STAGE[0] = name
    if RELIEF and _LIBC is not None: _LIBC.malloc_zone_pressure_relief(None, 0)
def _profiler():
    import psutil, threading
    pr = psutil.Process()
    import tracemalloc
    tracemalloc.start(int(os.environ.get("CFG596_TMDEPTH", "1")))
    TOP = {"cur": 0.0}
    def loop():
        while True:
            r = pr.memory_info().rss / 1e9; k = STAGE[0]
            cur, pk = tracemalloc.get_traced_memory(); tracemalloc.reset_peak()
            if r > MEMST.get(k, 0.0): MEMST[k] = r
            if pk / 1e9 > MEMST.get("live:" + k, 0.0): MEMST["live:" + k] = pk / 1e9
            tms = os.environ.get("CFG596_TMSTAGE")
            if os.environ.get("CFG596_TMSNAP") and (tms is None or tms == k) and cur / 1e9 > TOP["cur"] + 0.05:
                TOP["cur"] = cur / 1e9; sn = tracemalloc.take_snapshot()
                st = sn.statistics("traceback")[:12]
                MEMST["top"] = [f"{k} {cur / 1e9:.2f}"] + [f"{x.size / 1e9:.2f}GB " + " | ".join(str(f) for f in x.traceback) for x in st]
            time.sleep(0.05)
    threading.Thread(target=loop, daemon=True).start()
if os.environ.get("CFG596_PROFILE", "0") == "1": _profiler()
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9        # macOS: bytes (peak)

# ---------------------------------------------------------------- disk-backed fields (CFG596_SPILL=1) or in-memory (validation sizes)
class DField:
    """a full (M, M, M) field addressed by x-slabs; on disk via pread/pwrite (not mapped, so not in the process RSS) when SPILL."""
    _n = 0
    def __init__(self, name, M, dtype, inner=None):
        self.M = M; self.dt = np.dtype(dtype); self.inner = tuple(inner) if inner else (M, M)
        self.per = int(np.prod(self.inner)) * self.dt.itemsize; self.arr = None; self.fd = None
        if SPILL:
            DField._n += 1
            d = os.path.join(WORK, "tmp"); os.makedirs(d, exist_ok=True)
            self.fn = os.path.join(d, f"df_{os.getpid()}_{DField._n}_{name}.bin")
            self.fd = os.open(self.fn, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o600); os.ftruncate(self.fd, M * self.per)
        else:
            self.arr = np.empty((M,) + self.inner, self.dt)        # in-memory (np.empty: pages committed only when written)
    def write(self, s, x):
        if self.fd is None: self.arr[s] = x; return
        mv = memoryview(np.ascontiguousarray(x, dtype=self.dt)).cast("B"); off = s.start * self.per; o = 0
        while o < len(mv): o += os.pwrite(self.fd, mv[o:], off + o)
    def write_all(self, x):
        if self.fd is None: self.arr = x; return
        for i in range(0, self.M, 16): self.write(slice(i, min(i + 16, self.M)), x[i:i + 16])
    def read(self, s):
        if self.fd is None: return self.arr[s]
        n = (s.stop - s.start) * self.per; off = s.start * self.per; parts = []; got = 0
        while got < n:
            c = os.pread(self.fd, n - got, off + got); parts.append(c); got += len(c)
        return np.frombuffer(b"".join(parts) if len(parts) > 1 else parts[0], self.dt).reshape((s.stop - s.start,) + self.inner)
    def read_all(self):
        if self.fd is None: return self.arr
        out = np.empty((self.M,) + self.inner, self.dt)
        for i in range(0, self.M, 16): out[i:i + 16] = self.read(slice(i, min(i + 16, self.M)))
        return out
    def close(self):
        if self.fd is not None:
            os.close(self.fd); os.remove(self.fn); self.fd = None
        self.arr = None

# ---------------------------------------------------------------- mesh with in-place padded FFTs
class Mesh:
    def __init__(self, M):
        self.M = M; self.dx = L / M
        k1 = 2 * np.pi * sfft.fftfreq(M, d=self.dx); kz = 2 * np.pi * sfft.rfftfreq(M, d=self.dx)
        self.kx = k1[:, None, None].astype(np.float32); self.ky = k1[None, :, None].astype(np.float32)
        self.kz = kz[None, None, :].astype(np.float32)
        self.kvec = (self.kx, self.ky, self.kz)
        self.SL = max(1, min(M, int(os.environ.get("CFG596_SLAB", str(max(1, (1 << 24) // (M * M)))))))
        self.slabs = [slice(i, min(i + self.SL, M)) for i in range(0, M, self.SL)]
        PS = max(1, min(M, int(os.environ.get("CFG596_PSLAB", str(max(1, (1 << 20) // (M * M)))))))
        self.pslabs = [slice(i, min(i + PS, M)) for i in range(0, M, PS)]       # thread-pool tasks (bounded temporaries per thread)
    def kv_s(self, c, s):
        return self.kx[s] if c == 0 else self.kvec[c]
    def k2_s(self, s):
        return self.kx[s] ** 2 + self.ky ** 2 + self.kz ** 2
    def ik2_s(self, s):
        k2 = self.k2_s(s)
        if s.start == 0: k2[0, 0, 0] = 1.0
        ik2 = (1.0 / k2).astype(np.float32)
        if s.start == 0: ik2[0, 0, 0] = 0.0
        return ik2
    def cbuf(self, dt=np.complex64):
        return np.empty((self.M, self.M, self.M // 2 + 1), dt)
    def real(self, buf):
        return buf.view(np.float32 if buf.dtype == np.complex64 else np.float64)[:, :, :self.M]
    def fwd_ip(self, buf):
        M = self.M; rv = buf.view(np.float32 if buf.dtype == np.complex64 else np.float64)
        for s in self.slabs:
            t = sfft.rfft(rv[s, :, :M], axis=2, workers=NTH); buf[s] = t
        r = sfft.fft(buf, axis=0, overwrite_x=True, workers=NTH)
        if not np.shares_memory(r, buf): buf[...] = r
        for s in self.slabs:
            r = sfft.fft(buf[s], axis=1, overwrite_x=True, workers=NTH)
            if not np.shares_memory(r, buf): buf[s] = r
        return buf
    def inv_ip(self, buf, skip_axis0=False):
        M = self.M; rdt = np.float32 if buf.dtype == np.complex64 else np.float64; rv = buf.view(rdt)
        if not skip_axis0:
            r = sfft.ifft(buf, axis=0, overwrite_x=True, norm="forward", workers=NTH)
            if not np.shares_memory(r, buf): buf[...] = r
        sc = rdt(1.0 / M ** 3)
        for s in self.slabs:
            t = sfft.ifft(buf[s], axis=1, norm="forward", workers=NTH)
            rv[s, :, :M] = sfft.irfft(t, n=M, axis=2, norm="forward", workers=NTH) * sc
        return rv[:, :, :M]
    def fwd(self, x):                                   # = sfft.rfftn(x) bitwise, into a fresh buffer
        b = self.cbuf(np.complex64 if x.dtype == np.float32 else np.complex128)
        rv = self.real(b)
        for s in self.slabs: rv[s] = x[s]
        return self.fwd_ip(b)
    def inv_copy(self, xk):                             # = sfft.irfftn(xk).astype(float32) bitwise, contiguous result
        b = xk.copy(); r = self.inv_ip(b); out = np.empty(r.shape, r.dtype)
        for s in self.slabs: out[s] = r[s]
        return out
    def cic_idx(self, pos):
        u = pos / self.dx; i0 = np.floor(u).astype(np.int64); w = (u - i0).astype(np.float32)
        return i0 % self.M, (i0 + 1) % self.M, w

POOL = None
def EACH(mesh, fn):
    pmap(fn, mesh.pslabs)
def pmap(fn, slabs):
    global POOL
    if POOL is None: POOL = ThreadPoolExecutor(NTH)
    list(POOL.map(fn, slabs))

def eig_l2(t):
    """cfg527 eig3, l2 only (identical elementwise arithmetic)."""
    a11, a22, a33, a12, a13, a23 = [x.astype(np.float64) for x in t]
    p1 = a12 ** 2 + a13 ** 2 + a23 ** 2; q = (a11 + a22 + a33) / 3
    p2 = (a11 - q) ** 2 + (a22 - q) ** 2 + (a33 - q) ** 2 + 2 * p1; p = np.sqrt(p2 / 6); ps = np.where(p > 0, p, 1.0)
    b11, b22, b33 = (a11 - q) / ps, (a22 - q) / ps, (a33 - q) / ps; b12, b13, b23 = a12 / ps, a13 / ps, a23 / ps
    r = 0.5 * (b11 * (b22 * b33 - b23 ** 2) - b12 * (b12 * b33 - b23 * b13) + b13 * (b12 * b23 - b22 * b13))
    ph = np.arccos(np.clip(r, -1, 1)) / 3
    l1 = q + 2 * p * np.cos(ph); l3 = q + 2 * p * np.cos(ph + 2 * np.pi / 3); l2 = 3 * q - l1 - l3
    return l2.astype(np.float32)

# ---------------------------------------------------------------- particles
class Particles:
    """state per component c: exact -> pos[c] float64 (wrapped), mom[c] float64; lean -> disp[c] float32 (from lattice point), mom[c] float32."""
    def __init__(self, npg):
        self.npg = npg; self.N = npg ** 3
        self.CH = npg * npg * max(1, int(os.environ.get("CFG596_CHUNK_PLANES", "8")))
        self.chunks = [(i, min(i + self.CH, self.N)) for i in range(0, self.N, self.CH)]
        ICH = int(os.environ.get("CFG596_ICHUNK", str(1 << 19)))
        self.ichunks = [(i, min(i + ICH, self.N)) for i in range(0, self.N, ICH)]   # thread-pool particle tasks
    def q(self, c, i0, i1):
        idx = np.arange(i0, i1, dtype=np.int64); n = self.npg
        ic = idx // (n * n) if c == 0 else ((idx // n) % n if c == 1 else idx % n)
        return (ic + 0.5) * (L / n)
    def positions(self, i0, i1):
        if MODE == "exact":
            return np.stack([self.x[c][i0:i1] for c in range(3)], 1)
        return np.stack([(self.q(c, i0, i1) + self.x[c][i0:i1]) % L for c in range(3)], 1)
    def kick(self, c, i0, i1, cc, accp):
        self.mom[c][i0:i1] += cc * accp
    def drift(self, d):
        for c in range(3):
            def task(ch):
                i0, i1 = ch
                if MODE == "exact": self.x[c][i0:i1] = (self.x[c][i0:i1] + d * self.mom[c][i0:i1]) % L
                else: self.x[c][i0:i1] += d * self.mom[c][i0:i1]
            pmap(task, self.ichunks)

def deposit(mesh, P):
    """cfg527 Mesh.deposit (CIC, rho/mean - 1, float32).  exact: unchunked, the original statement order; lean: chunked, windowed bincount."""
    M = mesh.M
    if MODE == "exact" or len(P.chunks) == 1:
        pos = P.positions(0, P.N); i0, i1, w = mesh.cic_idx(pos); del pos
        rho = np.zeros(M ** 3, np.float64)
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
        rho = rho.reshape((M,) * 3); Dd = DField("delta", M, np.float32); Dd.write_all((rho / rho.mean() - 1.0).astype(np.float32)); return Dd
    rho = np.zeros((M, M * M), np.float64)
    for a_, b_ in P.chunks:
        pos = P.positions(a_, b_); i0, i1, w = mesh.cic_idx(pos); del pos
        lag0 = (a_ // (M * M)) % M
        x0 = (lag0 - M // 4) % M
        s0 = (i0[:, 0] - x0) % M; s1 = (i1[:, 0] - x0) % M
        lo = int(min(s0.min(), s1.min())); hi = int(max(s0.max(), s1.max()))
        Wn = hi - lo + 1
        idx = []; wts = []
        for cx in (0, 1):
            ix = (s1 if cx else s0) - lo; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    idx.append((ix * M + iy) * M + iz); wts.append(wx * wy * wz)
        del i0, i1, w, s0, s1
        idx = np.concatenate(idx); wts = np.concatenate(wts)
        acc = np.bincount(idx, weights=wts, minlength=Wn * M * M).reshape(Wn, M * M); del idx, wts
        start = (x0 + lo) % M
        n1 = min(Wn, M - start)
        rho[start:start + n1] += acc[:n1]
        if n1 < Wn: rho[:Wn - n1] += acc[n1:]
        del acc
    m = rho.mean(); r3 = rho.reshape(M, M, M)
    Dd = DField("delta", M, np.float32)
    def _b(s): Dd.write(s, (r3[s] / m - 1.0).astype(np.float32))
    EACH(mesh, _b)
    return Dd

def interp1(mesh, gpad, pos):
    """cfg527 Mesh.interp for ONE grid (identical per-component arithmetic); gpad = padded real view (M, M, M+2) of the field."""
    M = mesh.M; i0, i1, w = mesh.cic_idx(pos); out = np.zeros(pos.shape[0], np.float32)
    flat = gpad.reshape(-1); Mp = gpad.shape[2]
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                out += (wx * wy * wz) * flat[(ix * M + iy) * Mp + iz]
    return out

def fwd_field(mesh, x):
    """= mesh.fwd(x) for an array or a DField (filled slab-wise into a fresh buffer; bitwise identical)."""
    if not isinstance(x, DField): return mesh.fwd(x)
    b = mesh.cbuf(); rv = mesh.real(b)
    def _b(s): rv[s] = x.read(s)
    EACH(mesh, _b)
    return mesh.fwd_ip(b)

def measure_pk(mesh, delta):
    """cfg527 measure_pk (sigma8 plus sigma2/sigma4 diagnostics); slab accumulation of the bin sums (measurement only)."""
    M = mesh.M; dk = fwd_field(mesh, delta)
    kf = 2 * np.pi / L; edges = np.arange(0.5, M // 2 + 1, 1.0) * kf
    nb = np.zeros(len(edges) + 1); sk = np.zeros(len(edges) + 1); sp = np.zeros(len(edges) + 1); sig = {8.0: 0.0, 2.0: 0.0, 4.0: 0.0}
    for s in mesh.slabs:
        W = 1.0
        for c in range(3):
            W = W * np.sinc(mesh.kv_s(c, s) * mesh.dx / (2 * np.pi)) ** 2
        pk3 = (np.abs(dk[s]) ** 2) * L ** 3 / M ** 6 / W ** 2
        kk = np.sqrt(mesh.k2_s(s))
        wt = np.full(dk[s].shape, 2.0, np.float32); wt[..., 0] = 1.0
        if M % 2 == 0: wt[..., -1] = 1.0
        if s.start == 0: wt[0, 0, 0] = 0.0
        ib = np.digitize(kk.ravel(), edges); wv = wt.ravel()
        nb += np.bincount(ib, weights=wv, minlength=len(edges) + 1)
        sk += np.bincount(ib, weights=wv * kk.ravel(), minlength=len(edges) + 1)
        sp += np.bincount(ib, weights=wv * pk3.ravel(), minlength=len(edges) + 1)
        for R_ in sig:
            x = (kk * R_).astype(np.float64); x = np.where(x > 0, x, 1e-3)
            sig[R_] += float(np.sum(wt * pk3 * (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2))
    del dk
    ok = nb[1:len(edges)] > 0
    kb = (sk[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]; pb = (sp[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]
    sg = {R_: math.sqrt(v / L ** 3) for R_, v in sig.items()}
    return kb.tolist(), pb.tolist(), sg[8.0], {"sigma2": sg[2.0], "sigma4": sg[4.0]}

# ---------------------------------------------------------------- initial conditions (the ONLY LCDM input)
def initial_conditions_exact(npg, amp=1.0):
    """cfg527 initial_conditions verbatim (float64 state)."""
    rng = np.random.default_rng(SEED)
    wk = sfft.rfftn(rng.standard_normal((NSEED,) * 3), workers=NTH) / NSEED ** 1.5
    ix = np.concatenate([np.arange(0, npg // 2), np.arange(NSEED - npg // 2, NSEED)])
    wk = wk[ix][:, ix][:, :, :npg // 2 + 1].copy()
    m = Mesh(npg)
    k2 = m.kx ** 2 + m.ky ** 2 + m.kz ** 2; k2[0, 0, 0] = 1.0
    ik2 = (1.0 / k2).astype(np.float32); ik2[0, 0, 0] = 0.0; del k2
    kk = np.sqrt(m.kx ** 2 + m.ky ** 2 + m.kz ** 2).astype(np.float64)
    dk = wk * np.sqrt(P_lin0(kk) / (L / npg) ** 3) * npg ** 1.5 * amp
    dk[npg // 2, :, :] = 0; dk[:, npg // 2, :] = 0; dk[:, :, -1] = 0; dk[0, 0, 0] = 0
    psi = [sfft.irfftn(1j * kv * dk * ik2, s=(npg,) * 3, workers=NTH) for kv in m.kvec]
    psi = np.stack([p.ravel() for p in psi], 1)
    q = (np.indices((npg,) * 3).reshape(3, -1).T + 0.5) * (L / npg)
    Di = Dgrow(AI)
    pos = (q + Di * psi) % L
    mom = AI ** 2 * E(AI) * fgrow(AI) * Di * psi
    return pos.astype(np.float64), mom.astype(np.float64)

def initial_conditions_lean(m, P, amp=1.0):
    """same field, component by component, complex128 in-place padded buffer; state stored as float32 displacement / momentum."""
    npg = m.M; rng = np.random.default_rng(SEED)
    if NSEED == npg:                                              # production: in place, no mode selection needed (ix = identity)
        buf = np.empty((NSEED, NSEED, NSEED // 2 + 1), np.complex128); rv = buf.view(np.float64)
        sl = max(1, (1 << 24) // (NSEED * NSEED))
        for i in range(0, NSEED, sl):
            j = min(i + sl, NSEED); rv[i:j, :, :NSEED] = rng.standard_normal((j - i, NSEED, NSEED))
        m.fwd_ip(buf)
        for s in m.slabs: buf[s] /= NSEED ** 1.5
    else:                                                         # validation sizes only (NSEED > N): cfg527 statements verbatim
        wk = sfft.rfftn(rng.standard_normal((NSEED,) * 3), workers=NTH) / NSEED ** 1.5
        ix = np.concatenate([np.arange(0, npg // 2), np.arange(NSEED - npg // 2, NSEED)])
        buf = wk[ix][:, ix][:, :, :npg // 2 + 1].copy(); del wk
    for s in m.slabs:
        kk = np.sqrt(m.k2_s(s)).astype(np.float64)
        buf[s] = buf[s] * np.sqrt(P_lin0(kk) / (L / npg) ** 3) * npg ** 1.5 * amp
    buf[npg // 2, :, :] = 0; buf[:, npg // 2, :] = 0; buf[:, :, -1] = 0; buf[0, 0, 0] = 0
    Ddk = DField("dk", npg, np.complex128, inner=buf.shape[1:]); Ddk.write_all(buf)
    if SPILL: del buf
    Di = Dgrow(AI); cm = AI ** 2 * E(AI) * fgrow(AI) * Di
    P.x = [np.empty(P.N, np.float32) for _ in range(3)]; P.mom = [np.empty(P.N, np.float32) for _ in range(3)]
    for c in range(3):
        b = m.cbuf(np.complex128)
        for s in m.slabs: b[s] = (1j * m.kv_s(c, s)) * Ddk.read(s) * m.ik2_s(s)
        psi = m.inv_ip(b)
        for i0, i1 in P.chunks:
            p = psi[i0 // (npg * npg):i1 // (npg * npg)].reshape(-1)
            P.x[c][i0:i1] = (Di * p).astype(np.float32)
            P.mom[c][i0:i1] = (cm * p).astype(np.float32)
        del b, psi
    Ddk.close(); gc.collect()

def step_grid():
    seg = [(AI, 0.5, 123), (0.5, 2 / 3, 11), (2 / 3, 1.0, 16)]
    a = [AI]
    for lo, hi, n in seg:
        a += list(np.exp(np.linspace(math.log(lo), math.log(hi), n + 1))[1:])
    a[-1] = 1.0
    return np.array(a)

def catch_labels(m):
    """periodic 6-connected component labels of mask m (cfg527): returns r = component index of every True cell in C order
    (= the original r[mm], int32) and nc.  Callers guarantee m.any()."""
    from scipy import ndimage
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    lab, n = ndimage.label(m)
    pa, pb = [], []
    for ax in range(3):
        l0 = np.take(lab, 0, axis=ax).ravel(); l1 = np.take(lab, -1, axis=ax).ravel(); k = (l0 > 0) & (l1 > 0)
        pa.append(l0[k]); pb.append(l1[k])
    pa = np.concatenate(pa); pb = np.concatenate(pb)
    g = coo_matrix((np.ones(len(pa), np.int8), (pa, pb)), shape=(n + 1, n + 1))
    nc, root = connected_components(g, directed=False)
    lv = lab.reshape(-1); del lab
    r = root.astype(np.int32)[lv[lv > 0]]
    return r, nc

def fret_of(lM):
    if FRET_MODE == "one": return 1.0
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def M_ta(R, Dta):
    return (4 * math.pi / 3) * R ** 3 * Dta * 0.315 * 2.775e11
def x_supply(R, Dta, a, branch, foot):
    Mta = M_ta(R, Dta)
    fr = fret_of(math.log10(Mta)); Mbn = fr * FB * Mta / 0.674
    a0p = a0_code(a, branch, foot) * ACC_UNIT
    rM = math.sqrt(6.674e-11 * Mbn * 1.989e30 / a0p) / 3.0857e22 * 0.674 / a
    return min(rM / math.log(1.0 + fr * FB / (1.0 - FB)) / R, 1.0)

def cover_peaks(mesh, delta, Dta):
    """cfg527 in_cover, first half (resolved peaks and their r_ON); identical arithmetic.  The original evaluates this twice per
    refresh with identical inputs (mask call, catchment call); it is evaluated once and shared (deterministic -> identical)."""
    from scipy import ndimage
    M, dx = mesh.M, mesh.dx
    tau = (Dta - 1.0) / 3.0
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pk = (delta == mx) & (delta >= 3 * (tau - EPS)); del mx
    if not pk.any():
        return None
    Rg = np.geomspace(dx, 8.0, 14)
    rhok = mesh.cbuf(); rr = mesh.real(rhok)
    def _b(s): rr[s] = (1.0 + delta[s]).astype(np.float32)
    EACH(mesh, _b)
    mesh.fwd_ip(rhok)
    idx = np.argwhere(pk); del pk
    ok = np.ones(len(idx), bool); ron = np.zeros(len(idx))
    b = mesh.cbuf()
    for R in Rg:
        def fill(s):
            kr = np.sqrt(mesh.k2_s(s)) * R; out = np.ones_like(kr)
            nz = kr > 1e-8; out[nz] = 3 * (np.sin(kr[nz]) - kr[nz] * np.cos(kr[nz])) / kr[nz] ** 3
            b[s] = rhok[s] * out.astype(np.float32)
        pmap(fill, mesh.pslabs)
        mean = mesh.inv_ip(b)[idx[:, 0], idx[:, 1], idx[:, 2]]
        ok &= mean >= Dta
        ron[ok] = R
    del rhok, b
    return idx, ron, Rg

def cover_balls(mesh, peaks, Dta, x, a=1.0, branch='FLAT', foot='canonical', want_fret=False):
    """cfg527 in_cover, second half (union of balls); returns the PACKED mask (and, with want_fret, a uint8 f_ret code + float32 table)."""
    M, dx = mesh.M, mesh.dx
    if peaks is None:
        z = np.zeros((M, M, M), bool)
        return (pack(z), np.zeros((M, M, M), np.uint8), np.ones(1, np.float32)) if want_fret else pack(z)
    idx, ron, Rg = peaks
    res = ron >= RMIN_PHYS
    mask = np.zeros((M, M, M), bool)
    code = np.zeros((M, M, M), np.uint8) if want_fret else None; tab = [np.float32(1.0)]
    g = np.arange(M); g = np.minimum(g, M - g) * dx
    b = None; bb = None
    for R in Rg[Rg >= RMIN_PHYS - 1e-9]:
        sel = res & (np.abs(ron - R) < 1e-9)
        if not sel.any():
            continue
        if want_fret: tab.append(np.float32(fret_of(math.log10(M_ta(R, Dta))))); kc = len(tab) - 1
        rb = (x_supply(R, Dta, a, branch, foot) if x is None else x) * R
        if rb < 0.5 * dx:
            mask[idx[sel, 0], idx[sel, 1], idx[sel, 2]] = True
            if want_fret: code[idx[sel, 0], idx[sel, 1], idx[sel, 2]] = kc
            continue
        if b is None: b = mesh.cbuf(); bb = mesh.cbuf()
        pr = mesh.real(b)
        def _b(s): pr[s] = 0.0
        EACH(mesh, _b)
        pr[idx[sel, 0], idx[sel, 1], idx[sel, 2]] = 1.0
        br = mesh.real(bb)
        def fball(s):
            br[s] = ((g[s][:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2) <= rb * rb).astype(np.float32)
        pmap(fball, mesh.pslabs)
        mesh.fwd_ip(b); mesh.fwd_ip(bb)
        def _b(s): b[s] *= bb[s]
        EACH(mesh, _b)
        conv = mesh.inv_ip(b)
        def _b(s):
            cs = conv[s] > 0.5
            mask[s] |= cs
            if want_fret: code[s][cs] = kc
        EACH(mesh, _b)
    del b, bb
    pm = pack(mask); del mask
    return (pm, code, np.array(tab, np.float32)) if want_fret else pm

def pack(m):
    return np.packbits(m, axis=-1)
def unpack(p, s=slice(None)):
    M = p.shape[0]
    return np.unpackbits(p[s], axis=-1, count=M).astype(bool)

def tidal_exact_fsw(mesh, dk, tau, Dfsw):
    """exact mode: the original six-field transform, eig3 -> l2 -> f_sw (written to Dfsw)."""
    M = mesh.M; tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = []
    for i, j in tk:
        b = mesh.cbuf()
        def _b(s): b[s] = mesh.kv_s(i, s) * mesh.kv_s(j, s) * dk[s] * mesh.ik2_s(s)
        EACH(mesh, _b)
        r = mesh.inv_ip(b); out = np.empty(r.shape, np.float32)
        def _b(s): out[s] = r[s]
        EACH(mesh, _b)
        t.append(out); del b
    def ev(s):
        l2 = eig_l2_blocked([x[s] for x in t])
        Dfsw.write(s, np.clip(0.5 + (l2 - tau) / (2 * EPS), 0, 1).astype(np.float32))
    pmap(ev, mesh.pslabs); del t

def tidal_lean_fsw(mesh, dk, tau, Dfsw):
    """lean mode: F_p = A0[kx^p dk / k^2] (p = 0, 1, 2; p = 2 in dk's own buffer), then per x-slab the kx-free factors and the
    axis-1 / axis-2 transforms, eig3 -> l2 -> f_sw written to Dfsw (no full l2 or tensor field held)."""
    M = mesh.M; F = []
    for p in range(3):
        b = mesh.cbuf() if p < 2 else dk
        def _b(s):
            kxp = 1.0 if p == 0 else (mesh.kx[s] if p == 1 else mesh.kx[s] * mesh.kx[s])
            b[s] = (kxp * dk[s]) * mesh.ik2_s(s) if p else dk[s] * mesh.ik2_s(s)
        EACH(mesh, _b)
        r = sfft.ifft(b, axis=0, overwrite_x=True, norm="forward", workers=NTH)
        if not np.shares_memory(r, b): b[...] = r
        F.append(b)
    ky, kz = mesh.ky, mesh.kz; sc = np.float32(1.0 / M ** 3)
    fac = {(0, 0): (2, 1.0), (1, 1): (0, ky * ky), (2, 2): (0, kz * kz), (0, 1): (1, ky), (0, 2): (1, kz), (1, 2): (0, ky * kz)}
    order = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    def ev(s):
        comps = []
        for ij in order:
            p, f = fac[ij]
            t = sfft.ifft(F[p][s] * f, axis=1, norm="forward", workers=1)
            comps.append(sfft.irfft(t, n=M, axis=2, norm="forward", workers=1) * sc)
        l2 = eig_l2_blocked(comps)
        Dfsw.write(s, np.clip(0.5 + (l2 - tau) / (2 * EPS), 0, 1).astype(np.float32))
    pmap(ev, mesh.pslabs)
    del F

def eig_l2_blocked(t):
    """eig_l2 over y-blocks (bounded float64 temporaries per thread; elementwise -> identical)."""
    n0, M = t[0].shape[0], t[0].shape[1]; out = np.empty(t[0].shape, np.float32)
    yb = max(1, (1 << 17) // (n0 * t[0].shape[2]))
    for j in range(0, M, yb):
        out[:, j:j + yb] = eig_l2([x[:, j:j + yb] for x in t])
    return out

def forces(mesh, box, a, switch, branch, foot, dta, diag=False, keep_state=False):
    """cfg527 forces for switch RES (RC = 0, census, SHELL draw, NOFILT) or S0; returns (phik buffer, info).
    box = [delta] (taken over, so the caller holds no reference).  Accelerations = -a irfftn(1j k phik), formed by the caller.
    keep_state (extra snapshots only): the diagnostic call's catchment / f_ret refresh is NOT stored (measurement only)."""
    info = {}; M = mesh.M
    Dd = box.pop(); delta = None
    stage("f_dk"); dk = fwd_field(mesh, Dd)
    if switch == "S0":
        Dd.close()
        def _b(s): dk[s] = ((-1.5 * Om / a) * dk[s]) * mesh.ik2_s(s)
        EACH(mesh, _b)
        if diag: info["finite"] = bool(np.all(np.isfinite(dk)))
        return dk, info
    D = math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))
    tau = (D - 1.0) / 3.0
    Dfsw = DField("fsw", M, np.float32)
    stage("f_tidal")
    if MODE == "exact": tidal_exact_fsw(mesh, dk, tau, Dfsw)
    else: tidal_lean_fsw(mesh, dk, tau, Dfsw)
    del dk
    # ---- census edge (every 10th call) and catchments / f_ret
    refresh = (not diag) and (_INC["mask"] is None or _INC["calls"] % 10 == 0)
    if refresh or diag:
        stage("f_incover")
        if delta is None: delta = Dd.read_all()
        peaks = cover_peaks(mesh, delta, D)
        if SPILL: del delta; delta = None
        edge_p = cover_balls(mesh, peaks, D, None, a, branch, foot)
        catch_p, code, tab = cover_balls(mesh, peaks, D, 1.0, a, branch, foot, want_fret=True)
        del peaks
        Dcode = DField("fcode", M, np.uint8); Dcode.write_all(code); del code
        if not diag:
            _INC["mask"] = edge_p
        if not keep_state:
            if _INC["fcode"] is not None and _INC["fcode"] is not Dcode: _INC["fcode"].close()
            _INC["catch"], _INC["fcode"], _INC["ftab"] = catch_p, Dcode, tab
    if not diag: _INC["calls"] += 1
    if not diag: edge_p = _INC["mask"]
    if not (diag and keep_state): catch_p, Dcode, tab = _INC["catch"], _INC["fcode"], _INC["ftab"]
    info.update(tau=tau, Delta_ta=D)
    # ---- MOND input: retained baryons f_ret(x)(1 + delta), W(k) = 1 (NOFILT)
    fc, fh, fs = MIXES[MIX]
    kJ = lambda T: math.sqrt(1.5 * Om / a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    kJ4, kJ6 = kJ(1e4), kJ(1e6)
    stage("f_mond")
    phb = mesh.cbuf(); pr = mesh.real(phb)
    def _b(s): pr[s] = (tab[Dcode.read(s)] * (1.0 + Dd.read(s))).astype(np.float32)
    EACH(mesh, _b)
    if diag and keep_state: Dcode.close()
    mesh.fwd_ip(phb)
    def _b(s): phb[s] = ((-1.5 * Om / a) * phb[s]) * mesh.ik2_s(s)
    EACH(mesh, _b)
    def gb_comp(c, b):
        def _b(s):
            kk = mesh.k2_s(s)
            Wk = (fc / (1.0 + kk / kJ4 ** 2) + fh / (1.0 + kk / kJ6 ** 2) + fs).astype(np.float32)
            b[s] = (1j * mesh.kv_s(c, s)) * phb[s] * Wk
        EACH(mesh, _b)
        r = mesh.inv_ip(b)
        def _b(s): r[s] = FB * (-r[s])
        EACH(mesh, _b)
        return r
    ysq = np.empty((M,) * 3, np.float32); gbuf = mesh.cbuf()
    for c in range(3):
        g = gb_comp(c, gbuf)
        if c == 0:
            def _b(s): ysq[s] = g[s] ** 2
        else:
            def _b(s): ysq[s] += g[s] ** 2
        EACH(mesh, _b)
    a0c = a * a0_code(a, branch, foot)
    if diag and DIAGX: info["y_median"] = float(np.median(np.sqrt(ysq) / a0c))
    Dw = DField("w", M, np.float32)
    def fw(s):
        for j in range(s.start, s.stop):
            y = np.sqrt(ysq[j:j + 1]) / a0c
            Dw.write(slice(j, j + 1), nu_mono(y).astype(np.float32) - 1.0)
    pmap(fw, mesh.pslabs); del ysq
    divk = mesh.cbuf()
    for c in range(3):
        g = gb_comp(c, gbuf)
        def _b(s): g[s] = Dw.read(s) * g[s]
        EACH(mesh, _b)
        mesh.fwd_ip(gbuf)
        if c == 0:
            def _b(s): divk[s] = (1j * mesh.kv_s(c, s)) * gbuf[s]; divk[s] += 0
        else:
            def _b(s): divk[s] += (1j * mesh.kv_s(c, s)) * gbuf[s]
        EACH(mesh, _b)
    del gbuf, phb; Dw.close()
    s_ph = mesh.inv_ip(divk)                                      # divk buffer now holds the real field
    def _b(s): s_ph[s] = -s_ph[s]
    EACH(mesh, _b)
    # ---- source: e = f_sw max(s_ph - s_c, 0) on the catchments; per-catchment draw from the shell (catchment AND NOT edge)
    stage("f_source")
    cs = (1.5 * Om * (1.0 - FB) / a)
    e = s_ph
    def _b(s):
        fsw_s = Dfsw.read(s) * unpack(edge_p, s).astype(np.float32)
        e[s] = fsw_s * np.maximum(s_ph[s] - cs * (1.0 + Dd.read(s)), 0.0)
        e[s] = e[s] * unpack(catch_p, s)
    EACH(mesh, _b)
    Dfsw.close()
    catch = unpack(catch_p)
    if not catch.any():                                            # cfg527: no components -> nc = 1, q = 0, comp = 0, src = e
        del catch
        if diag:
            es = _psum(e); info.update(overdraw_mass=0.0, q_max=0.0, cap_active=False, n_catch=1, e_sum=es, e_mean=es / M ** 3, src_sum=es)
        return _finish_phik(mesh, divk, Dd, a, info, diag)
    stage("f_labels")
    r, nc = catch_labels(catch); del catch
    # groups of planes: exact mode one group (= the original single bincount); lean mode groups of GP planes
    GP = M if MODE == "exact" else max(1, int(os.environ.get("CFG596_GROUP_PLANES", "16")))
    groups = [slice(i, min(i + GP, M)) for i in range(0, M, GP)]
    E_ = np.zeros(nc); C_ = np.zeros(nc); W_ = np.zeros(nc) if diag else None
    offs = [0]
    def gsel(gs):
        cm = unpack(catch_p, gs).reshape(-1)
        sh = (unpack(catch_p, gs) & ~unpack(edge_p, gs)).reshape(-1)[cm]
        dl = np.ascontiguousarray(Dd.read(gs)).reshape(-1)[cm]
        sc_sel = cs * (1.0 + dl)
        rv_sel = (sc_sel * sh).astype(np.float32)
        e_sel = _sel(e[gs], cm)
        return cm, dl, rv_sel, e_sel
    sel_cache = []
    o = 0
    for gs in groups:
        cm, dl, rv_sel, e_sel = gsel(gs); n = int(cm.sum()); rr = r[o:o + n]
        if GP == M:
            E_ = np.bincount(rr, weights=e_sel.astype(np.float64), minlength=nc)
            C_ = np.bincount(rr, weights=rv_sel.astype(np.float64), minlength=nc)
            if diag: W_ = np.bincount(rr, weights=(1.0 + dl).astype(np.float64), minlength=nc)
        else:
            E_ += np.bincount(rr, weights=e_sel.astype(np.float64), minlength=nc)
            C_ += np.bincount(rr, weights=rv_sel.astype(np.float64), minlength=nc)
            if diag: W_ += np.bincount(rr, weights=(1.0 + dl).astype(np.float64), minlength=nc)
        o += n
    q = E_ / np.maximum(C_, 1e-30)
    q_raw = q.copy(); capf = np.where(q > 1.0, 1.0 / np.maximum(q, 1e-30), 1.0)
    capon = bool((q > 1.0).any())
    if capon: q = np.minimum(q, 1.0)
    if diag:
        info["overdraw_mass"] = float(W_[q_raw > 1].sum() / max(W_.sum(), 1e-30)); info["q_max"] = float(q_raw.max()) if nc else 0.0
        info["cap_active"] = capon; info["n_catch"] = int(nc)
    o = 0; es = 0.0; ss = 0.0
    for gs in groups:
        cm, dl, rv_sel, e_sel = gsel(gs); n = int(cm.sum()); rr = r[o:o + n]
        if capon: e_sel = (e_sel * capf[np.maximum(rr, 0)]).astype(np.float32)
        comp_sel = (rv_sel * q[rr]).astype(np.float32)
        _put(e[gs], cm, e_sel)
        if diag and GP == M:
            ec = _contig(e); info["e_sum"] = float(ec.sum()); info["e_mean"] = float(ec.mean()); del ec
        elif diag: es += _psum(e[gs])
        _put(e[gs], cm, e_sel - comp_sel)
        if diag and GP == M:
            ec = _contig(e); info["src_sum"] = float(ec.sum()); del ec
        elif diag: ss += _psum(e[gs])
        o += n
    if diag and GP != M: info.update(e_sum=es, e_mean=es / M ** 3, src_sum=ss)
    del r
    return _finish_phik(mesh, divk, Dd, a, info, diag)

def _psum(x):
    return float(sum(float(x[i].astype(np.float64).sum()) for i in range(x.shape[0])))

def _finish_phik(mesh, divk, Dd, a, info, diag):
    # ---- total potential: phik = (-1.5 Om / a) dk / k^2 - fwd(src) / k^2
    stage("f_finish"); srck = mesh.fwd_ip(divk)                     # in place: src (real) -> its transform
    phik = mesh.cbuf(); pr = mesh.real(phik)
    def _b(s): pr[s] = Dd.read(s)
    EACH(mesh, _b)
    Dd.close()
    mesh.fwd_ip(phik)
    def _b(s):
        ik2 = mesh.ik2_s(s)
        phik[s] = ((-1.5 * Om / a) * phik[s]) * ik2
        phik[s] = phik[s] - srck[s] * ik2
    EACH(mesh, _b)
    del srck
    if diag: info["finite"] = bool(np.all(np.isfinite(phik)))
    return phik, info

def _sel(x, mm):
    """x.ravel()[mm] in C order for a possibly strided (padded) 3D view."""
    M = x.shape[0]; per = x.shape[1] * x.shape[2]; parts = []
    for i in range(M):
        parts.append(x[i].reshape(-1)[mm[i * per:(i + 1) * per]])
    return np.concatenate(parts) if parts else np.zeros(0, x.dtype)
def _put(x, mm, v):
    M = x.shape[0]; per = x.shape[1] * x.shape[2]; o = 0
    for i in range(M):
        m_ = mm[i * per:(i + 1) * per]; n = int(m_.sum())
        if n:
            xi = x[i]; t = np.ascontiguousarray(xi).reshape(-1); t[m_] = v[o:o + n]; x[i] = t.reshape(xi.shape)
        o += n

def _contig(x):
    out = np.empty(x.shape, x.dtype)
    out[...] = x
    return out

def grav_field(mesh, phik, a):
    """delta_grav = -k^2 phik a / (1.5 Om) via the CFG555 capture formula: num = sum_c kv_c (1j kv_c phik); dgk = -num / (1j 1.5 Om) * a."""
    b = mesh.cbuf()
    for s in mesh.slabs:
        num = sum(mesh.kv_s(c, s) * ((1j * mesh.kv_s(c, s)) * phik[s]) for c in range(3))
        b[s] = ((-num / (1j * 1.5 * Om)) * a).astype(np.complex64)
    b[0, 0, 0] = 0
    return mesh.inv_ip(b)

def block_mean(x, f):
    M = x.M if isinstance(x, DField) else x.shape[0]; n = M // f; out = np.empty((n, n, n), np.float32)
    for i in range(n):
        sl = x.read(slice(i * f, (i + 1) * f)) if isinstance(x, DField) else x[i * f:(i + 1) * f]
        out[i] = sl.astype(np.float64).reshape(f, n, f, n, f).mean(axis=(0, 2, 4)).astype(np.float32)
    return out

# ---------------------------------------------------------------- run
def run(switch, branch, foot, npg, amp=1.0):
    try: os.nice(10)
    except OSError: pass
    os.makedirs(WORK, exist_ok=True)
    tag = f"cfg596_{switch}_{foot}_N{npg}_L{L:g}_ns{NSEED}_{MODE}" + (f"_seed{SEED}" if SEED != 359 else "")
    global DIAGX
    DIAGX = npg <= 512
    mesh = Mesh(npg); dta = dta_table(); t0 = time.time(); P = Particles(npg)
    if MODE == "exact":
        pos, mom = initial_conditions_exact(npg, amp)
        P.x = [np.ascontiguousarray(pos[:, c]) for c in range(3)]; P.mom = [np.ascontiguousarray(mom[:, c]) for c in range(3)]; del pos, mom
    else:
        stage("ic"); initial_conditions_lean(mesh, P, amp)
    aa = step_grid(); nsteps = len(aa) - 1
    snaps = {0.5: "z1", 2 / 3: "z0.5", 1.0: "z0"}
    extra = {i: f"x{1 / aa[i] - 1:.4f}" for i in EXTRA if 0 < i <= nsteps}
    res = {"tag": tag, "lane": "CFG596", "engine": "cfg596_pm.py (lean copy of cfg527_pm.py sha256 aeabd0ba...)", "mode": MODE,
           "switch": switch, "branch": branch, "foot": foot, "np": npg, "mesh": npg, "L": L, "nseed": NSEED, "seed": SEED, "rmin": RMIN_PHYS,
           "draw": DRAW, "mix": MIX, "z_i": ZI, "nsteps": nsteps, "threads": NTH, "spill": SPILL, "snap": {}, "mem": []}
    jfn = os.path.join(WORK, f"{tag}.json")
    def log(msg):
        print(f"  [{tag}] {msg} t={time.time() - t0:.0f}s maxrss={rss_gb():.2f}GB", flush=True)
    def snapshot(name, a, restore=False):
        stage("snap_deposit"); Dd = deposit(mesh, P)
        kb, pb, s8, sig = measure_pk(mesh, Dd)
        f = max(1, npg // 256); bm_p = block_mean(Dd, f)
        box = [Dd]; del Dd
        phik, info = forces(mesh, box, a, switch, branch, foot, dta, diag=True, keep_state=restore)
        stage("snap_grav"); dg = grav_field(mesh, phik, a); del phik
        dgc = _contig(dg); del dg
        _, pg, s8g, sigg = measure_pk(mesh, dgc)
        np.savez_compressed(os.path.join(WORK, f"{tag}_{name}_mesh256.npz"), dpart=bm_p, dgrav=block_mean(dgc, f))
        del dgc
        res["snap"][name] = dict(a=a, z=1 / a - 1, D=Dgrow(a), k=kb, P=pb, sigma8=s8, **sig, P_grav=pg, sigma8_grav=s8g,
                                 sigma2_grav=sigg["sigma2"], sigma4_grav=sigg["sigma4"], measurement_only=restore, **info, t=time.time() - t0)
        res["mem"].append([name, rss_gb()]); res["mem_stage"] = dict(MEMST)
        json.dump(res, open(jfn, "w"))
        log(f"snapshot {name} a={a:.4f} sigma8={s8:.4f} grav {s8g:.4f}")
    def final_positions():
        return np.concatenate([P.positions(i0, i1).astype(np.float32) for i0, i1 in P.chunks])
    def accel_pass(phik, a, kicks):
        b = mesh.cbuf()
        for c in range(3):
            def _b(s): b[s] = (1j * mesh.kv_s(c, s)) * phik[s]
            EACH(mesh, _b)
            r = mesh.inv_ip(b)
            def _b(s): r[s] = -a * r[s]
            EACH(mesh, _b)
            gpad = b.view(np.float32)
            def task(ch):
                i0, i1 = ch
                accp = interp1(mesh, gpad, P.positions(i0, i1))
                for cc in kicks: P.kick(c, i0, i1, cc, accp)
            pmap(task, P.ichunks)
        del b
    snapshot("zi", AI)
    stage("deposit"); box = [deposit(mesh, P)]; phik, _ = forces(mesh, box, AI, switch, branch, foot, dta)
    stage("accel")
    a0_, a1_ = aa[0], aa[1]; am = math.sqrt(a0_ * a1_)
    accel_pass(phik, AI, [quad(lambda x: 1 / (x * x * E(x)), a0_, am)[0]]); del phik
    stage("drift"); P.drift(quad(lambda x: 1 / (x ** 3 * E(x)), a0_, a1_)[0])
    log("step 0 drift done")
    TM = res.setdefault("timing_s", {"deposit": 0.0, "forces": 0.0, "accel": 0.0, "drift": 0.0, "snap": 0.0})
    for n in range(nsteps):
        a0_, a1_ = aa[n], aa[n + 1]; am = math.sqrt(a0_ * a1_)
        stage("deposit"); t_ = time.time(); box = [deposit(mesh, P)]; TM["deposit"] += time.time() - t_
        t_ = time.time(); phik, _ = forces(mesh, box, a1_, switch, branch, foot, dta); TM["forces"] += time.time() - t_
        kicks = [quad(lambda x: 1 / (x * x * E(x)), am, a1_)[0]]
        last = n == nsteps - 1
        if not last:
            b0, b1 = aa[n + 1], aa[n + 2]; bm = math.sqrt(b0 * b1)
            kicks.append(quad(lambda x: 1 / (x * x * E(x)), b0, bm)[0])
        stage("accel"); t_ = time.time(); accel_pass(phik, a1_, kicks); del phik; TM["accel"] += time.time() - t_
        t_ = time.time()
        for asn, nm in snaps.items():
            if abs(a1_ - asn) < 1e-9: snapshot(nm, a1_)
        if (n + 1) in extra: snapshot(extra[n + 1], a1_, restore=True)
        TM["snap"] += time.time() - t_
        if not last:
            t_ = time.time(); P.drift(quad(lambda x: 1 / (x ** 3 * E(x)), b0, b1)[0]); TM["drift"] += time.time() - t_
        if (n + 1) % 5 == 0 or n < 3: log(f"step {n + 1}/{nsteps} a={a1_:.4f} timing " + " ".join(f"{k} {v:.0f}" for k, v in TM.items()))
        res["mem"].append([f"step{n + 1}", rss_gb()]); res["mem_stage"] = dict(MEMST)
        if n + 1 >= MAXSTEPS:
            res["stopped_at_step"] = n + 1; break
    if _INC["fcode"] is not None: _INC["fcode"].close()
    res["runtime_s"] = time.time() - t0; res["maxrss_gb"] = rss_gb()
    if npg <= 512 and "stopped_at_step" not in res:
        np.savez_compressed(os.path.join(WORK, f"{tag}_z0pos.npz"), pos=final_positions())
    json.dump(res, open(jfn, "w"))
    log("done")
    return res

if __name__ == "__main__":
    sw, ft, npg = sys.argv[1], sys.argv[2], int(sys.argv[3])
    assert sw in ("RES", "S0")
    run(sw, "FLAT", ft, npg, 1.0)
