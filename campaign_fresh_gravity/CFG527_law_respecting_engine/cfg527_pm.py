#!/usr/bin/env python3
"""CFG527 engine (FROZEN_CRITERIA.md): cfg524_pm.py copy; compensation drawn only from the shell D = catchment AND NOT census edge,
comp = q_C s_c on D (CFG527_DRAW=SHELL, default) | q s_c over the whole catchment (SC = cfg521 exactly, MUTATE A); mix NOFILT = W(k) = 1 (unfiltered source).
CFG524 engine (FROZEN_CRITERIA.md): cfg521_pm.py copy; compensation drawn only from the unsettled reservoir
Rv = s_c - S, S = f_sw clip(s_ph, 0, s_c) (CFG524_DRAW=R2, default) | clip(s_ph, 0, s_c) (R1) | s_c (SC = cfg521 exactly, MUTATE).
CFG521 engine (FROZEN_CRITERIA.md): cfg518_pm.py copy; box size L = CFG521_L, resolved r_ON >= CFG521_RMIN, diagnostics only otherwise.
CFG518 engine (FROZEN_CRITERIA.md): CFG424 copy; phantom sourced by f_ret(host) x PM baryons (CFG416 fret_of painted over each host's
turnaround ball, 1 outside), census edge, cap q > 1 -> e/q.  CFG521_FRET_MODE=census (default) | one (K1 control); CFG521_NOCOMP=1 -> MUTATE.
CFG424 engine: CFG423 copy; RC == 0 -> per-catchment mass conservation in turnaround spheres (x = 1 cover components); CFG521_NOCOMP=1 -> MUTATE (no compensation).
CFG423 engine: CFG416 copy; edge r_M/ln(1 + f_ret f_b/(1-f_b)) with f_ret = CFG518_FRET (default 1, PM self-consistent). FROZEN_CRITERIA.md.
CFG416 engine: CFG414 copy with a per-host supply-edge radius x_h*r_ON = (5.364/f_ret) r_M(M_b,now) (FROZEN_CRITERIA.md).
Usage: python3 cfg416_pm.py RES BRANCH FOOT NP RC MIXA [FRETX]   (FRETX = f_ret multiplier; MUTATE uses 10)
CFG414 engine: CFG411 copy + T1 switch confined to IN(x): union of balls of radius x*r_ON around resolved peaks (FROZEN_CRITERIA.md).
Usage: python3 cfg414_pm.py RES BRANCH FOOT NP RC MIXA X
CFG411 engine: CFG410 copy; NSEED = max(256, NP) via CFG518_NSEED for 512^3 runs (FROZEN_CRITERIA.md).
CFG410 engine: CFG374 copy with the corrected comoving k_J = sqrt(1.5 Om / a)*100/c_s (audit 5819dd616) and an optional
filament veto (switch 0 where l3 < 0).  FROZEN_CRITERIA.md.  Usage: python3 cfg410_pm.py RES BRANCH FOOT NP RC MIXA [VETO]
CFG374 engine: CFG372's engine (copied) with a phase-weighted filter W = f_cool W(1e4) + f_hot W(1e6) + f_coll (FROZEN_CRITERIA.md 396ed0c5a).
Usage: python3 cfg374_pm.py RES BRANCH FOOT NP RC MIX   (MIX = MIXA | MIXB | HOT1 (f_hot = 1, control))
CFG372 engine: CFG366's engine (copied, not imported) + the phantom sourced by a pressure-filtered baryon field,
W(k) = 1/(1 + k^2/k_J^2), k_J = sqrt(1.5 Om a) * 100 / c_s [h/Mpc], c_s = sqrt(5 kT/(3 mu m_p)), mu = 0.6 (FROZEN_CRITERIA.md 733d27623).
Usage: python3 cfg372_pm.py RES BRANCH FOOT NP RC TGAS

CFG366 engine: CFG361's engine (cfg361_pm.py, copied not imported; itself CFG359's) with ONE added switch "RES":
the reservoir rule, extra = e - W_Rc * e with e = f max(s_ph - s_c, 0) (T5's ON excess) and W_Rc a Gaussian catchment.
Criteria: FROZEN_CRITERIA.md (5f3a22464).  Original CFG361 header follows.
CFG361: CFG359's PM engine with B's dark-mass bookkeeping in switched-ON cells.  Everything is CFG359's (background GR + Lambda, nu_mono, phantom from
baryons only, T1 switch eps = 0.077, EH ICs at z_i = 49 = the ONLY LCDM input, seed 359) except the ON-cell source.
Sources (code units s = 1.5 Om rho/rho_bar_m / a; s_ph = -div[(nu - 1) g_Nb]; s_c = 1.5 Om (1 - f_b)(1 + delta)/a):
  T5   extra = f max(s_ph - s_c, 0)           (CFG4 T5 / CFG336-338 reading M; PRIMARY)
  S    extra = f (s_ph - (1 - f_ex,R) s_c),  f_ex,R = max(0, 1 - sum_R s_ph / sum_R s_c) on connected f > 0 regions
  T5F  accel += a f f_b max(nu - 1/f_b, 0) g_N   (force analogue, reported only)
  ADD  extra = f s_ph                          (CFG359 T1, reproduction control)
  S1T5 = T5 with f = 1 everywhere;  S0 = Newtonian control.
Usage: python3 cfg366_pm.py RES BRANCH FOOT NP RC   (RC = catchment width, comoving Mpc/h; CFG518_MUTATE=1 only affects the C1 check)
"""
import os, sys
NTH = int(os.environ.get("CFG527_THREADS", "2"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import json, math, time
import numpy as np
from scipy import fft as sfft
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg527_work"))
RC = 1.0
TGAS = 0.0
MIX = "MIXA"
VETO = False
XIN = 0.4
FRETX = 1.0
_INC = {"mask": None, "catch": None, "fret": None, "calls": 0}
FRET_MODE = os.environ.get("CFG527_FRET_MODE", "census")
NOCOMP = os.environ.get("CFG527_NOCOMP", "0") == "1"
DRAW = os.environ.get("CFG527_DRAW", "SHELL")
assert DRAW in ("SHELL", "SC")

def catch_labels(m):
    """periodic 6-connected component labels of mask m (0 = outside)."""
    from scipy import ndimage
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    lab, n = ndimage.label(m)
    if n == 0:
        return lab.ravel(), 1
    pa, pb = [], []
    for ax in range(3):
        l0 = np.take(lab, 0, axis=ax).ravel(); l1 = np.take(lab, -1, axis=ax).ravel(); k = (l0 > 0) & (l1 > 0)
        pa.append(l0[k]); pb.append(l1[k])
    pa = np.concatenate(pa); pb = np.concatenate(pb)
    g = coo_matrix((np.ones(len(pa), np.int8), (pa, pb)), shape=(n + 1, n + 1))
    nc, root = connected_components(g, directed=False)
    r = root[lab].ravel(); r[lab.ravel() == 0] = -1
    return r, nc

RMIN_PHYS = float(os.environ.get("CFG527_RMIN", "1.56"))          # CFG521: 2 cells of the 256^3 mesh
MIXES = {"MIXA": (0.28, 0.54, 0.18), "MIXB": (0.57, 0.25, 0.18), "HOT1": (0.0, 1.0, 0.0), "NOFILT": (0.0, 0.0, 1.0)}     # CFG527: NOFILT -> W(k) = 1 exactly
MUTATE = os.environ.get("CFG527_MUTATE", "0") == "1"

# ---------------------------------------------------------------- constants (L352 values)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om; FB = om_b / (om_b + om_c)
NS, SIG8 = 0.965, 0.811
MPC = 3.0856775814913673e22
ACC_UNIT = 1e10 * h / MPC                       # H0^2 (Mpc/h) in m/s^2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
W0, WA = -0.838, -0.62                          # DESI DR2 CPL (chart_a0z_one.py), A0-DE only
L = float(os.environ.get("CFG527_L", "200")); ZI = 49.0; AI = 1.0 / (1 + ZI); SEED = int(os.environ.get('CFG527_SEED', '359')); NSEED = int(os.environ.get('CFG527_NSEED', '256'))
EPS = float(os.environ.get("CFG527_EPS", "0.077"))
E = lambda a: math.sqrt(Om / a ** 3 + OL)

def a0_code(a, branch, foot):
    base = A0[foot] / ACC_UNIT
    if branch == "FLAT":
        return base
    if branch == "CRIT":
        return base * E(a)
    if branch == "DE":
        return base * math.sqrt(a ** (-3 * (1 + W0 + WA)) * math.exp(-3 * WA * (1 - a)))
    raise ValueError(branch)

# ---------------------------------------------------------------- nu_mono (copied from L340 lines 104-118)
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

# ---------------------------------------------------------------- linear theory (EH no-wiggle, CFG354's T_eh)
def T_eh(k):
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000)            # h/Mpc; T_eh takes 1/Mpc
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

# ---------------------------------------------------------------- Delta_ta(z): CFG353/354 LCDM shell ODE, unchanged
def delta_ta(z):
    ai = 1e-3
    def run(di):
        Ri = ai * (1 - di / 3.0)
        GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3
        Hi = math.sqrt(Om / ai ** 3 + OL)
        def rhs(t, y):
            a, R, V = y
            return [a * math.sqrt(Om / a ** 3 + OL), V, -GM / R ** 2 + OL * R]
        ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
        s = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - di / 3.0)], events=ev, rtol=1e-10, atol=1e-13)
        if not s.t_events[0].size:
            return None
        a, R, _ = s.y_events[0][0]
        return a, (1 + di) * (Ri / ai) ** 3 * a ** 3 / R ** 3
    at = 1 / (1 + z); lo, hi = 1e-4, 0.05
    for _ in range(80):
        mid = math.sqrt(lo * hi); r = run(mid)
        if r is None or r[0] > at:
            lo = mid
        else:
            hi = mid
    return run(hi)[1]
DTA_FILE = os.path.join(WORK, "cfg361_delta_ta_table.json")
def dta_table():
    if os.path.exists(DTA_FILE):
        return json.load(open(DTA_FILE))
    zs = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0, 14.0, 20.0, 30.0, 49.0]
    tab = {"z": zs, "D": [delta_ta(z) for z in zs]}
    json.dump(tab, open(DTA_FILE, "w"))
    return tab

# ---------------------------------------------------------------- mesh helpers
class Mesh:
    def __init__(self, M):
        self.M = M; self.dx = L / M
        k1 = 2 * np.pi * sfft.fftfreq(M, d=self.dx); kz = 2 * np.pi * sfft.rfftfreq(M, d=self.dx)
        self.kx = k1[:, None, None].astype(np.float32); self.ky = k1[None, :, None].astype(np.float32)
        self.kz = kz[None, None, :].astype(np.float32)
        k2 = self.kx ** 2 + self.ky ** 2 + self.kz ** 2; k2[0, 0, 0] = 1.0
        self.ik2 = (1.0 / k2).astype(np.float32); self.ik2[0, 0, 0] = 0.0
        self.kvec = (self.kx, self.ky, self.kz)
    def fwd(self, x): return sfft.rfftn(x, workers=NTH)
    def inv(self, xk): return sfft.irfftn(xk, s=(self.M,) * 3, workers=NTH).astype(np.float32)
    def cic_idx(self, pos):
        u = pos / self.dx; i0 = np.floor(u).astype(np.int64); w = (u - i0).astype(np.float32)
        return i0 % self.M, (i0 + 1) % self.M, w
    def deposit(self, pos):
        M = self.M; i0, i1, w = self.cic_idx(pos); rho = np.zeros(M ** 3, np.float64)
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
        rho = rho.reshape((M,) * 3); return (rho / rho.mean() - 1.0).astype(np.float32)
    def interp(self, grids, pos):
        M = self.M; i0, i1, w = self.cic_idx(pos); out = np.zeros((pos.shape[0], len(grids)), np.float32)
        flats = [g.ravel() for g in grids]
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    idx = (ix * M + iy) * M + iz; ww = wx * wy * wz
                    for c, g in enumerate(flats):
                        out[:, c] += ww * g[idx]
        return out

def eig3(t):
    """closed-form eigenvalues of symmetric 3x3 fields (t = [xx, yy, zz, xy, xz, yz]); returns l1 >= l2 >= l3."""
    a11, a22, a33, a12, a13, a23 = [x.astype(np.float64) for x in t]
    p1 = a12 ** 2 + a13 ** 2 + a23 ** 2; q = (a11 + a22 + a33) / 3
    p2 = (a11 - q) ** 2 + (a22 - q) ** 2 + (a33 - q) ** 2 + 2 * p1; p = np.sqrt(p2 / 6); ps = np.where(p > 0, p, 1.0)
    b11, b22, b33 = (a11 - q) / ps, (a22 - q) / ps, (a33 - q) / ps; b12, b13, b23 = a12 / ps, a13 / ps, a23 / ps
    r = 0.5 * (b11 * (b22 * b33 - b23 ** 2) - b12 * (b12 * b33 - b23 * b13) + b13 * (b12 * b23 - b22 * b13))
    ph = np.arccos(np.clip(r, -1, 1)) / 3
    l1 = q + 2 * p * np.cos(ph); l3 = q + 2 * p * np.cos(ph + 2 * np.pi / 3); l2 = 3 * q - l1 - l3
    return l1.astype(np.float32), l2.astype(np.float32), l3.astype(np.float32)

def measure_pk(mesh, delta, npart):
    M = mesh.M; dk = mesh.fwd(delta)
    W = 1.0
    for kv in mesh.kvec:
        W = W * np.sinc(kv * mesh.dx / (2 * np.pi)) ** 2
    pk3 = (np.abs(dk) ** 2) * L ** 3 / M ** 6 / W ** 2      # no shot-noise subtraction: lattice ICs are sub-Poisson; cancels in ratios
    kk = np.sqrt(mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2)
    wt = np.full(dk.shape, 2.0, np.float32); wt[..., 0] = 1.0
    if M % 2 == 0: wt[..., -1] = 1.0
    wt[0, 0, 0] = 0.0
    kf = 2 * np.pi / L; edges = np.arange(0.5, M // 2 + 1, 1.0) * kf
    ib = np.digitize(kk.ravel(), edges); wv = wt.ravel()
    nb = np.bincount(ib, weights=wv, minlength=len(edges) + 1)
    sk = np.bincount(ib, weights=wv * kk.ravel(), minlength=len(edges) + 1)
    sp = np.bincount(ib, weights=wv * pk3.ravel(), minlength=len(edges) + 1)
    ok = nb[1:len(edges)] > 0
    kb = (sk[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]; pb = (sp[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]
    def sig(R_):
        x = (kk * R_).astype(np.float64); x = np.where(x > 0, x, 1e-3)
        return math.sqrt(float(np.sum(wt * pk3 * (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2)) / L ** 3)
    s8 = sig(8.0); _INC["sig"] = {"sigma2": sig(2.0), "sigma4": sig(4.0)}       # CFG521 diagnostics
    return kb.tolist(), pb.tolist(), s8

# ---------------------------------------------------------------- initial conditions (the ONLY LCDM input)
def initial_conditions(npg, amp=1.0):
    rng = np.random.default_rng(SEED)
    wk = sfft.rfftn(rng.standard_normal((NSEED,) * 3), workers=NTH) / NSEED ** 1.5
    ix = np.concatenate([np.arange(0, npg // 2), np.arange(NSEED - npg // 2, NSEED)])
    wk = wk[ix][:, ix][:, :, :npg // 2 + 1].copy()
    m = Mesh(npg)
    kk = np.sqrt(m.kx ** 2 + m.ky ** 2 + m.kz ** 2).astype(np.float64)
    dk = wk * np.sqrt(P_lin0(kk) / (L / npg) ** 3) * npg ** 1.5 * amp
    dk[npg // 2, :, :] = 0; dk[:, npg // 2, :] = 0; dk[:, :, -1] = 0; dk[0, 0, 0] = 0
    psi = [sfft.irfftn(1j * kv * dk * m.ik2, s=(npg,) * 3, workers=NTH) for kv in m.kvec]
    psi = np.stack([p.ravel() for p in psi], 1)
    q = (np.indices((npg,) * 3).reshape(3, -1).T + 0.5) * (L / npg)
    Di = Dgrow(AI)
    pos = (q + Di * psi) % L
    mom = AI ** 2 * E(AI) * fgrow(AI) * Di * psi       # p = a^2 dx/dt = a^3 H dD/da Psi
    return pos.astype(np.float64), mom.astype(np.float64)

def step_grid():
    seg = [(AI, 0.5, 123), (0.5, 2 / 3, 11), (2 / 3, 1.0, 16)]
    a = [AI]
    for lo, hi, n in seg:
        a += list(np.exp(np.linspace(math.log(lo), math.log(hi), n + 1))[1:])
    a[-1] = 1.0
    return np.array(a)

def fex_regions(fsw, s_ph, s_c, info=None):
    """S reading: f_ex,R = max(0, 1 - sum_R s_ph / sum_R s_c) on periodic 6-connected components of f > 0."""
    from scipy import ndimage
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    m = fsw > 0; lab, n = ndimage.label(m)
    out = np.zeros(fsw.shape, np.float32)
    if n == 0:
        if info is not None: info.update(S_nreg=0, S_fex_mass=0.0)
        return out
    pa, pb = [], []
    for ax in range(3):
        l0 = np.take(lab, 0, axis=ax).ravel(); l1 = np.take(lab, -1, axis=ax).ravel(); k = (l0 > 0) & (l1 > 0)
        pa.append(l0[k]); pb.append(l1[k])
    pa = np.concatenate(pa); pb = np.concatenate(pb)
    g = coo_matrix((np.ones(len(pa), np.int8), (pa, pb)), shape=(n + 1, n + 1))
    nc, root = connected_components(g, directed=False)
    L2 = root[lab].ravel(); mm = m.ravel()
    sph = np.bincount(L2[mm], weights=s_ph.ravel()[mm].astype(np.float64), minlength=nc)
    scs = np.bincount(L2[mm], weights=s_c.ravel()[mm].astype(np.float64), minlength=nc)
    fex = np.maximum(0.0, 1.0 - sph / np.maximum(scs, 1e-30))
    out.ravel()[mm] = fex[L2[mm]]
    if info is not None:
        w = s_c.ravel()[mm]
        info.update(S_nreg=int(len(np.unique(L2[mm]))), S_fex_mass=float(np.sum(w * out.ravel()[mm]) / np.sum(w)),
                    S_fex0_mass=float(np.sum(w * (out.ravel()[mm] == 0)) / np.sum(w)))
    return out

# ---------------------------------------------------------------- forces
def fret_of(lM):
    """CFG416 cfg416_pm.py fret_of, copied verbatim (FRETX = 1); FRET_MODE 'one' -> 1 (K1 control)."""
    if FRET_MODE == "one":
        return 1.0
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def M_ta(R, Dta):
    return (4 * math.pi / 3) * R ** 3 * Dta * 0.315 * 2.775e11                 # Msun/h (comoving mean matter density)

def x_supply(R, Dta, a, branch, foot):
    """x_h for a host of comoving r_ON = R (Mpc/h): r_edge / r_ON with r_edge = (5.364/f_ret) r_M(M_b,now) (all comoving h-units)."""
    Mta = M_ta(R, Dta)
    fr = fret_of(math.log10(Mta)); Mbn = fr * FB * Mta / 0.674             # Msun
    a0p = a0_code(a, branch, foot) * ACC_UNIT                                  # physical a0(a) in m/s^2
    rM = math.sqrt(6.674e-11 * Mbn * 1.989e30 / a0p) / 3.0857e22 * 0.674 / a   # comoving Mpc/h
    return min(rM / math.log(1.0 + fr * FB / (1.0 - FB)) / R, 1.0)

def in_cover(mesh, delta, Dta, x, a=1.0, branch='FLAT', foot='canonical', want_fret=False):
    """IN(x): union of balls of radius x*r_ON around resolved peaks (declared FFT implementation, FROZEN_CRITERIA.md)."""
    from scipy import ndimage
    M, dx = mesh.M, mesh.dx
    tau = (Dta - 1.0) / 3.0
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pk = (delta == mx) & (delta >= 3 * (tau - EPS))
    if not pk.any():
        z = np.zeros(delta.shape, bool)
        return (z, np.ones(delta.shape, np.float32)) if want_fret else z
    Rg = np.geomspace(dx, 8.0, 14)
    kk = np.sqrt(mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2)
    def tophat_k(R):
        kr = kk * R; out = np.ones_like(kr)
        nz = kr > 1e-8; out[nz] = 3 * (np.sin(kr[nz]) - kr[nz] * np.cos(kr[nz])) / kr[nz] ** 3
        return out.astype(np.float32)
    rhok = mesh.fwd((1.0 + delta).astype(np.float32))
    idx = np.argwhere(pk); ok = np.ones(len(idx), bool); ron = np.zeros(len(idx))
    for R in Rg:
        mean = mesh.inv(rhok * tophat_k(R))[idx[:, 0], idx[:, 1], idx[:, 2]]
        ok &= mean >= Dta
        ron[ok] = R
    del rhok
    res = ron >= RMIN_PHYS
    mask = np.zeros(delta.shape, bool)
    if want_fret: _INC["hosts"] = {}
    ff = np.ones(delta.shape, np.float32) if want_fret else None
    for R in Rg[Rg >= RMIN_PHYS - 1e-9]:
        sel = res & (np.abs(ron - R) < 1e-9)
        if want_fret: _INC.setdefault("hosts", {})[f"{R:.4f}"] = [int(sel.sum()), round(math.log10(M_ta(R, Dta)), 3)]   # CFG521 diag
        if not sel.any():
            continue
        pts = np.zeros(delta.shape, np.float32); pts[idx[sel, 0], idx[sel, 1], idx[sel, 2]] = 1.0
        rb = (x_supply(R, Dta, a, branch, foot) if x is None else x) * R
        if rb < 0.5 * dx:
            mask |= pts > 0.5
            if want_fret: ff[pts > 0.5] = fret_of(math.log10(M_ta(R, Dta)))
            continue
        g = np.arange(M); g = np.minimum(g, M - g) * dx
        ball = ((g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2) <= rb * rb).astype(np.float32)
        conv = mesh.inv(mesh.fwd(pts) * mesh.fwd(ball))
        mask |= conv > 0.5
        if want_fret: ff[conv > 0.5] = fret_of(math.log10(M_ta(R, Dta)))   # increasing R: the largest host wins overlaps
    return (mask, ff) if want_fret else mask

def forces(mesh, delta, a, switch, branch, foot, dta, diag=False):
    """returns (accel grids of -grad phi_tilde, phi_tilde = a phi), diag dict."""
    dk = mesh.fwd(delta)
    phik = (-1.5 * Om / a) * dk * mesh.ik2                      # lap phi_N = 1.5 Om delta / a
    info = {}
    need_t = switch in ("T1", "T1V", "T5", "S", "T5F", "ADD", "RES") or diag
    if need_t:
        tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
        t = [mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk * mesh.ik2) for i, j in tk]
        l1, l2, l3 = eig3(t); del t
        D = math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))
        tau = (D - 1.0) / 3.0
        fsw = np.clip(0.5 + (l2 - tau) / (2 * EPS), 0, 1).astype(np.float32)
        if switch == "RES" and not diag:
            if _INC["mask"] is None or _INC["calls"] % 10 == 0:
                _INC["mask"] = in_cover(mesh, delta, D, None, a, branch, foot)
                if RC == 0:
                    _INC["catch"], _INC["fret"] = in_cover(mesh, delta, D, 1.0, a, branch, foot, want_fret=True)
            _INC["calls"] += 1
            edge = _INC["mask"]
            fsw = fsw * edge.astype(np.float32)
        elif switch == "RES" and diag:
            edge = in_cover(mesh, delta, D, None, a, branch, foot)
            fsw = fsw * edge.astype(np.float32)
            if RC == 0:
                _INC["catch"], _INC["fret"] = in_cover(mesh, delta, D, 1.0, a, branch, foot, want_fret=True)
        if VETO:
            fsw[l3 < 0] = 0.0                                      # CFG410 filament veto
        if switch == "T1V":
            fsw[l3 < 0] = 0.0
        info.update(tau=tau, Delta_ta=D)
        if diag:
            rho = 1.0 + delta; on = fsw > 0.5
            info.update(vol_f=float(fsw.mean()), mass_f=float((fsw * rho).mean()), vol_on=float(on.mean()),
                        vol_on_knot=float((on & (l3 >= 0)).mean()), vol_on_fil=float((on & (l3 < 0)).mean()),
                        mass_on_knot=float((rho * (on & (l3 >= 0))).mean()), mass_on_fil=float((rho * (on & (l3 < 0))).mean()))
            info["_grids"] = (fsw, l3)
    extra_acc = None
    if switch != "S0":
        gN = [-mesh.inv(1j * kv * phik) for kv in mesh.kvec]
        if True:                                                # CFG374: phase-weighted pressure filter
            fc, fh, fs = MIXES[MIX]; kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
            kJ = lambda T: math.sqrt(1.5 * Om / a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
            Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
            if switch == "RES" and RC == 0 and _INC["fret"] is not None:    # CFG518: MOND input = retained baryons f_ret(x)(1 + delta)
                fr_ = _INC["fret"]
                phik_b = (-1.5 * Om / a) * mesh.fwd((fr_ * (1.0 + delta)).astype(np.float32)) * mesh.ik2
                if diag:
                    rho_ = (1.0 + delta) * _INC["catch"]
                    info["fret_mass_mean_catch"] = float((fr_ * rho_).sum() / max(rho_.sum(), 1e-30))
                    info["fret_min"] = float(fr_.min()); info["fret_vol_lt1"] = float((fr_ < 1).mean())
                    info["fret_mass_frac_le02"] = float(((fr_ <= 0.2) * rho_).sum() / max(rho_.sum(), 1e-30))   # CFG521 diag
                    info["hosts"] = dict(_INC.get("hosts", {}))
            else:
                phik_b = phik
            gb = [FB * (-mesh.inv(1j * kv * phik_b * Wk)) for kv in mesh.kvec]; del Wk, phik_b
        else:
            gb = [FB * g for g in gN]
        y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * a0_code(a, branch, foot))
        nu = nu_mono(y).astype(np.float32); w = nu - 1.0
        if diag:
            info["y_median"] = float(np.median(y)); info["nu_median"] = float(np.median(nu))
        del y
        if switch == "T5F":
            fac = (fsw * FB * np.maximum(nu - 1.0 / FB, 0.0)).astype(np.float32)
            extra_acc = [a * fac * g for g in gN]
        del gN
        divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)); del gb, w, nu
        s_ph = -mesh.inv(divk); del divk                        # phantom source, units of 1.5 Om delta / a
        s_c = (1.5 * Om * (1.0 - FB) / a) * (1.0 + delta)        # cosmic cold share in the same units
        if switch in ("S1", "ADD"):
            extra = s_ph if switch == "S1" else fsw * s_ph
        elif switch in ("T5", "S1T5"):
            sc_in = 0.0 if MUTATE else s_c
            extra = np.maximum(s_ph - sc_in, 0.0)
            if switch == "T5":
                extra = fsw * extra
        elif switch == "S":
            extra = fsw * (s_ph - (1.0 - fex_regions(fsw, s_ph, s_c, info if diag else None)) * s_c)
        elif switch == "T5F":
            extra = None
        elif switch == "RES":
            e = fsw * np.maximum(s_ph - s_c, 0.0)
            if RC == 0:
                cm = _INC["catch"]; e = e * cm                    # excess lives inside the catchments (edge balls lie inside)
                if NOCOMP:
                    src = e
                else:
                    r, nc = catch_labels(cm); mm = r >= 0
                    if DRAW == "SC":
                        rv = s_c                                                     # cfg521: draw in proportion to s_c (MUTATE A)
                    else:                                                            # CFG527: shell = catchment AND NOT census edge, weight s_c
                        rv = (s_c * (cm & ~edge)).astype(np.float32)
                    E_ = np.bincount(r[mm], weights=e.ravel()[mm].astype(np.float64), minlength=nc)
                    C_ = np.bincount(r[mm], weights=rv.ravel()[mm].astype(np.float64), minlength=nc)
                    q = E_ / np.maximum(C_, 1e-30)
                    q_raw = q.copy(); capf = np.where(q > 1.0, 1.0 / np.maximum(q, 1e-30), 1.0)   # CFG518 cap on available cold energy
                    if (q > 1.0).any():
                        e = (e.ravel() * np.where(mm, capf[np.maximum(r, 0)], 1.0)).reshape(e.shape).astype(np.float32)
                        q = np.minimum(q, 1.0)
                    comp = np.zeros(e.size, np.float32); comp[mm] = (rv.ravel()[mm] * q[r[mm]]).astype(np.float32)
                    src = e - comp.reshape(e.shape)
                    if diag:                                                         # CFG524 diagnostics (no effect on dynamics)
                        Sc_ = np.bincount(r[mm], weights=s_c.ravel()[mm].astype(np.float64), minlength=nc)
                        w_ = np.bincount(r[mm], weights=(1.0 + delta).ravel()[mm].astype(np.float64), minlength=nc)
                        info["res_frac"] = float(C_.sum() / max(Sc_.sum(), 1e-30))
                        info["cap_n"] = int((q_raw > 1).sum()); info["cap_mass_frac"] = float(w_[q_raw > 1].sum() / max(w_.sum(), 1e-30))
                        e_pre = float(E_.sum()); info["cap_e_removed_frac"] = float(1.0 - float(e.sum()) / max(e_pre, 1e-30)) if e_pre > 0 else 0.0
                        rho1 = (1.0 + delta).ravel()[mm].astype(np.float64); cpm = comp[mm].astype(np.float64); scm = s_c.ravel()[mm].astype(np.float64)
                        info["draw_rho_mean"] = float((cpm * rho1).sum() / max(cpm.sum(), 1e-30)); info["sc_rho_mean"] = float((scm * rho1).sum() / max(scm.sum(), 1e-30))
                        del rho1, cpm, scm
                        empty = (C_ <= 0) & (E_ > 0)
                        info["shell_frac"] = float(C_.sum() / max(Sc_.sum(), 1e-30)) if DRAW == "SHELL" else None
                        info["n_shell_empty"] = int(empty.sum()); info["e_frac_shell_empty"] = float(E_[empty].sum() / max(E_.sum(), 1e-30))
                        info["src_in_edge"] = float((e - comp.reshape(e.shape))[edge].sum()) if DRAW == "SHELL" else None
                        info["comp_in_edge"] = float(comp.reshape(e.shape)[edge].sum())
                    del rv
                    if diag:
                        w = np.bincount(r[mm], weights=(1.0 + delta).ravel()[mm].astype(np.float64), minlength=nc)
                        info["overdraw_mass"] = float(w[q_raw > 1].sum() / max(w.sum(), 1e-30)); info["q_max"] = float(q_raw.max()) if nc else 0.0
                        info["cap_active"] = bool((q_raw > 1).any()); info["e_sum"] = float(e.sum()); info["n_catch"] = int(nc)
                        if _INC["fret"] is not None:
                            info["fret_e_mean"] = float((e * _INC["fret"]).sum() / max(float(e.sum()), 1e-30))   # CFG521 diag
                        info["src_sum"] = float(src.sum()); info["e_mean"] = float(e.mean())
                    del comp
                phik = phik - mesh.fwd(src.astype(np.float32)) * mesh.ik2
                extra = None; del e, src
            else:
              ek = mesh.fwd(e.astype(np.float32))
              k2 = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
              Wk = np.exp(-0.5 * k2 * RC ** 2).astype(np.float32)
              xk = ek * (1.0 - Wk)                                 # the reservoir-compensated extra (k = 0 exactly zero)
              if diag:
                  band = (k2 > 0) & (k2 < (0.1 / RC) ** 2)
                  chk = ek if MUTATE else xk                       # MUTATE disables the compensation in the C1 check only
                  num = float(np.abs(chk[band]).mean()) if band.any() else 0.0
                  den = float(np.abs(ek[band]).mean()) if band.any() else 1.0
                  info["C1_band_ratio"] = num / max(den, 1e-30); info["C1_k0"] = float(abs(chk[0, 0, 0]))
                  info["C1_k0_e"] = float(abs(ek[0, 0, 0]))
                  comp = mesh.inv(ek * Wk)
                  info["overdraw_mass"] = float(((1.0 + delta) * (s_c - comp < 0)).mean())
                  info["e_mean"] = float(e.mean())
                  del comp
              phik = phik - xk * mesh.ik2
              extra = None; del e, ek, xk, Wk, k2
        else:                                                   # T1 / T1V as CFG359
            extra = fsw * s_ph
        if diag and switch not in ("S0",):
            rho = 1.0 + delta; on = (fsw > 0.5) if need_t else np.ones(delta.shape, bool)
            pd = on & (s_ph > s_c); info["mass_on_phantom_dom"] = float((rho * pd).mean())
            info["mass_on"] = float((rho * on).mean())
        if extra is not None:
            phik = phik - mesh.fwd(extra.astype(np.float32)) * mesh.ik2   # lap phi_extra = extra (k = 0 dropped by ik2)
        del s_ph, s_c
    if diag:
        info["finite"] = bool(np.all(np.isfinite(phik)))                 # CFG527 stability diag
    acc = [-a * mesh.inv(1j * kv * phik) for kv in mesh.kvec]   # -grad (a phi)
    if extra_acc is not None:
        acc = [x + e for x, e in zip(acc, extra_acc)]
    return acc, info

# ---------------------------------------------------------------- run
def run(switch, branch, foot, npg, amp=1.0):
    try:
        os.nice(10)
    except OSError:
        pass
    os.makedirs(WORK, exist_ok=True)
    tag = f"{switch}_{'TA' if RC == 0 else f'Rc{RC:g}'}{'_NOCOMP' if NOCOMP else ''}_{MIX}_MASSCONS_fret{FRET_MODE}_{branch}_{foot}_N{npg}" + (f"_L{L:g}" if L != 200.0 else "") + (f"_seed{SEED}" if SEED != 359 else "") + (f"_eps{EPS:g}" if EPS != 0.077 else "") + ("_MUTATE" if MUTATE else "") + f"_draw{DRAW}"
    mesh = Mesh(npg); pmesh = mesh; dta = dta_table(); t0 = time.time()
    pos, mom = initial_conditions(npg, amp)
    aa = step_grid(); snaps = {0.5: "z1", 2 / 3: "z0.5", 1.0: "z0"}
    res = {"tag": tag, "switch": switch, "branch": branch, "foot": foot, "np": npg, "mesh": npg, "amp": amp,
           "mutate": MUTATE, "draw": DRAW, "L": L, "rmin": RMIN_PHYS, "z_i": ZI, "nsteps": len(aa) - 1, "snap": {}}
    def snapshot(name, a):
        kb, pb, s8 = measure_pk(pmesh, pmesh.deposit(pos), npg ** 3)   # P(k) on the particle-lattice mesh (no lattice aliasing)
        delta = mesh.deposit(pos)
        _, info = forces(mesh, delta, a, switch if switch != "S0" else "S0", branch, foot, dta, diag=True)
        grids = info.pop("_grids")
        res["snap"][name] = dict(a=a, D=Dgrow(a), k=kb, P=pb, sigma8=s8, **_INC.get("sig", {}), **info, t=time.time() - t0)
        if name == "z0":
            np.savez_compressed(os.path.join(WORK, f"cfg527_{tag}_z0.npz"), pos=pos.astype(np.float32),
                                f=grids[0].astype(np.float16), l3=grids[1].astype(np.float16))
        print(f"  [{tag}] {name} a={a:.4f} sigma8={s8:.4f} t={time.time() - t0:.0f}s", flush=True)
    snapshot("zi", AI)
    delta = mesh.deposit(pos); acc, _ = forces(mesh, delta, AI, switch, branch, foot, dta)
    accp = mesh.interp(acc, pos); del acc
    for n in range(len(aa) - 1):
        a0, a1 = aa[n], aa[n + 1]; am = math.sqrt(a0 * a1)
        mom += quad(lambda x: 1 / (x * x * E(x)), a0, am)[0] * accp
        pos = (pos + quad(lambda x: 1 / (x ** 3 * E(x)), a0, a1)[0] * mom) % L
        delta = mesh.deposit(pos); acc, _ = forces(mesh, delta, a1, switch, branch, foot, dta)
        accp = mesh.interp(acc, pos); del acc
        mom += quad(lambda x: 1 / (x * x * E(x)), am, a1)[0] * accp
        for asn, nm in snaps.items():
            if abs(a1 - asn) < 1e-9:
                snapshot(nm, a1)
    res["runtime_s"] = time.time() - t0
    res["Rc"] = RC; res["MIX"] = MIX
    json.dump(res, open(os.path.join(WORK, f"cfg527_{tag}.json"), "w"))
    return res

if __name__ == "__main__":
    sw, br, ft, npg = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    RC = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    MIX = sys.argv[6] if len(sys.argv) > 6 else "MIXA"
    FRETX = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
    run(sw, br, ft, npg, 1.0)
