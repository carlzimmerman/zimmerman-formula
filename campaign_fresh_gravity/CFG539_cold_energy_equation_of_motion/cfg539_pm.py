#!/usr/bin/env python3
"""CFG539 engine (FROZEN_CRITERIA.md): a TWO-SPECIES PM -- baryon particles (mass share f_b) and cold-energy particles (1 - f_b) -- in which the
cold energy obeys a candidate EQUATION OF MOTION instead of the bookkeeping source (no extra source term: the gravitating mass is the particles).
  CFG539_EOM = A   overdamped settling flow (H^-1 gradient flow of the law-deficit field energy, free-fall mobility tau = 1/sqrt(4 pi G rho_m)):
                   cold particles inside turnaround catchments drift with v = MOB * tau * g_def, g_def = -grad psi, lap psi = 4 pi G d,
                   d = f_sw * edge * catch * max(rho_ph[retained baryons] - rho_c, 0); momentum untouched (dissipative); exact particle mass conservation.
  CFG539_EOM = C   inertial response: cold particles inside turnaround catchments feel the extra acceleration g_def (no timescale, no constant).
  CFG539_EOM = OFF no EoM (both species identical; reproduces the matched S0).
  CFG539_EDGE = 0  MUTATE-S (deficit not confined by the census edge).
Everything else (ICs, background, nu_mono, T1 switch, census fret_of, census edge, catchments, step grid, P(k)) is the CFG527 engine copied below.
Helpers below are copied verbatim from cfg527_pm.py (sha256 aeabd0ba...); its original header follows.
CFG527 engine (FROZEN_CRITERIA.md): cfg524_pm.py copy; compensation drawn only from the shell D = catchment AND NOT census edge,
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
NTH = int(os.environ.get("CFG539_THREADS", "2"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import json, math, time
import numpy as np
from scipy import fft as sfft
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg539_work"))
RC = 0.0
TGAS = 0.0
MIX = "NOFILT"
VETO = False
XIN = 0.4
FRETX = 1.0
_INC = {"mask": None, "catch": None, "fret": None, "calls": 0}
FRET_MODE = os.environ.get("CFG539_FRET_MODE", "census")
EOM = os.environ.get("CFG539_EOM", "A")                 # A = overdamped settling flow | C = inertial law-deficit force | OFF = no EoM (S0)
assert EOM in ("A", "C", "OFF")
EDGE = os.environ.get("CFG539_EDGE", "1") == "1"         # 0 = MUTATE-S: deficit not confined by the census edge
MOB = float(os.environ.get("CFG539_MOB", "1.0"))          # mobility multiplier (1 = the declared free-fall mobility; 0.5 / 2 robustness only)
NSUBMAX = 32

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

RMIN_PHYS = float(os.environ.get("CFG539_RMIN", "1.56"))          # CFG521: 2 cells of the 256^3 mesh
MIXES = {"MIXA": (0.28, 0.54, 0.18), "MIXB": (0.57, 0.25, 0.18), "HOT1": (0.0, 1.0, 0.0), "NOFILT": (0.0, 0.0, 1.0)}     # CFG527: NOFILT -> W(k) = 1 exactly
MUTATE = os.environ.get("CFG539_MUTATE", "0") == "1"

# ---------------------------------------------------------------- constants (L352 values)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om; FB = om_b / (om_b + om_c)
NS, SIG8 = 0.965, 0.811
MPC = 3.0856775814913673e22
ACC_UNIT = 1e10 * h / MPC                       # H0^2 (Mpc/h) in m/s^2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
W0, WA = -0.838, -0.62                          # DESI DR2 CPL (chart_a0z_one.py), A0-DE only
L = float(os.environ.get("CFG539_L", "200")); ZI = 49.0; AI = 1.0 / (1 + ZI); SEED = int(os.environ.get('CFG539_SEED', '359')); NSEED = int(os.environ.get('CFG539_NSEED', '512'))
EPS = float(os.environ.get("CFG539_EPS", "0.077"))
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


# ================================================================ CFG539: two species + cold-energy equation of motion
def deposit2(mesh, pos_b, pos_c):
    """CIC deposit of each species (float64 accumulation, as Mesh.deposit); returns delta_tot (mass-weighted), delta_b, delta_c (float32).
    If pos_c is pos_b (EOM OFF), the two species coincide and delta_tot equals the single-species engine's deposit."""
    M = mesh.M
    def raw(pos):
        i0, i1, w = mesh.cic_idx(pos); rho = np.zeros(M ** 3, np.float64)
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
        return rho.reshape((M,) * 3)
    rb = raw(pos_b); xb = rb / rb.mean()
    if pos_c is pos_b:
        d = (xb - 1.0).astype(np.float32); return d, d, d
    rc = raw(pos_c); xc = rc / rc.mean()
    return ((FB * xb + (1.0 - FB) * xc) - 1.0).astype(np.float32), (xb - 1.0).astype(np.float32), (xc - 1.0).astype(np.float32)

def deposit1(mesh, pos):
    M = mesh.M; i0, i1, w = mesh.cic_idx(pos); rho = np.zeros(M ** 3, np.float64)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
    rho = rho.reshape((M,) * 3); return (rho / rho.mean() - 1.0).astype(np.float32)

def law_fields(mesh, dtot, db, a, branch, foot, dta, diag=False):
    """Where the law acts and what it asks for, from the state (same rules as the CFG527 engine):
    tidal T1 switch f_sw (eps = 0.077), census edge IN(x_supply), turnaround catchments IN(1) with the census f_ret painted per host
    (all on the TOTAL density, cached every 10 calls; recomputed fresh in diag calls), and the phantom s_ph = -div[(nu - 1) g_b] of the
    UNFILTERED retained baryons f_ret (1 + delta_b) (W = 1).  Returns sw = f_sw * [edge] * catch, catch, edge, s_ph (code units)."""
    dk = mesh.fwd(dtot)
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk * mesh.ik2) for i, j in tk]
    l1, l2, l3 = eig3(t); del t, l1, l3, dk
    D = math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))
    tau = (D - 1.0) / 3.0
    fsw = np.clip(0.5 + (l2 - tau) / (2 * EPS), 0, 1).astype(np.float32); del l2
    if diag:
        edge = in_cover(mesh, dtot, D, None, a, branch, foot)
        catch, fret = in_cover(mesh, dtot, D, 1.0, a, branch, foot, want_fret=True)
    else:
        if _INC["mask"] is None or _INC["calls"] % 10 == 0:
            _INC["mask"] = in_cover(mesh, dtot, D, None, a, branch, foot)
            _INC["catch"], _INC["fret"] = in_cover(mesh, dtot, D, 1.0, a, branch, foot, want_fret=True)
        _INC["calls"] += 1
        edge, catch, fret = _INC["mask"], _INC["catch"], _INC["fret"]
    sw = fsw * catch.astype(np.float32)
    if EDGE:
        sw = sw * edge.astype(np.float32)
    phik_b = (-1.5 * Om / a) * mesh.fwd((fret * (1.0 + db)).astype(np.float32)) * mesh.ik2
    gb = [FB * (-mesh.inv(1j * kv * phik_b)) for kv in mesh.kvec]; del phik_b
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * a0_code(a, branch, foot))
    w = (nu_mono(y) - 1.0).astype(np.float32); del y
    divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)); del gb, w
    s_ph = -mesh.inv(divk); del divk
    return sw.astype(np.float32), catch, edge, s_ph, D

def deficit(sw, s_ph, dc, a):
    s_c = (1.5 * Om * (1.0 - FB) / a) * (1.0 + dc)
    return (sw * np.maximum(s_ph - s_c, 0.0)).astype(np.float32), s_c

def grad_psi(mesh, d):
    """grad_x psi with lap_x psi = d (code units: the deficit gravitates like mass for the cold energy)."""
    psik = -mesh.fwd(d) * mesh.ik2
    return [mesh.inv(1j * kv * psik) for kv in mesh.kvec]

def settle(mesh, pos_b, pos_c, Dacc, a, dt, branch, foot, dta, stat):
    """EOM A over the physical interval dt (units 1/H0) at epoch a: adaptive sub-steps, psi recomputed from the moving cold energy each sub-step;
    the baryons, f_sw, masks and s_ph are held for the step.  Displacement per sub-step <= 0.5 cell and Gamma h <= 0.5 (Gamma = 4 pi G rho_c tau)."""
    dtot, db, dc = deposit2(mesh, pos_b, pos_c)
    sw, catch, edge, s_ph, _ = law_fields(mesh, dtot, db, a, branch, foot, dta)
    del dtot
    cf = catch.astype(np.float32); rb1 = FB * (1.0 + db); del db
    done = 0.0; n = 0; clipped = 0; moved = 0.0
    while done < dt * (1 - 1e-12):
        d, _ = deficit(sw, s_ph, dc, a)
        if not np.any(d > 0):
            break
        g = grad_psi(mesh, d); del d
        rho = np.maximum(rb1 + (1.0 - FB) * (1.0 + dc), 1e-3)
        mob = (MOB * cf / np.sqrt(1.5 * Om * rho / a ** 3)).astype(np.float32)
        u = [(-mob * gi / (a * a)).astype(np.float32) for gi in g]; del g
        umax = float(np.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2).max())
        gam = float((1.5 * Om * (1.0 - FB) * (1.0 + dc) / a ** 3 * mob).max()); del rho, mob
        h = dt - done
        if umax > 0: h = min(h, 0.5 * mesh.dx / umax)
        if gam > 0: h = min(h, 0.5 / gam)
        last = (n == NSUBMAX - 1)
        if last: h = dt - done
        up = mesh.interp(u, pos_c) * h; del u
        if last:
            lim = 0.5 * mesh.dx; nrm = np.sqrt((up.astype(np.float64) ** 2).sum(1)); big = nrm > lim
            clipped += int(big.sum()); up[big] *= (lim / nrm[big])[:, None].astype(np.float32)
        pos_c += up; pos_c %= L; Dacc += up; moved += float(np.sqrt((up.astype(np.float64) ** 2).sum(1)).sum()); del up
        done += h; n += 1
        dc = deposit1(mesh, pos_c)
        if last: break
    stat["nsub_max"] = max(stat.get("nsub_max", 0), n); stat["nsub_sum"] = stat.get("nsub_sum", 0) + n
    stat["clipped"] = stat.get("clipped", 0) + clipped; stat["moved_cells"] = stat.get("moved_cells", 0.0) + moved / mesh.dx
    stat["nsteps"] = stat.get("nsteps", 0) + 1

def forces2(mesh, dtot, db, dc, a, branch, foot, dta, diag=False):
    """Newtonian acceleration of the real (particle) mass for both species; EOM C adds g_def to the cold energy."""
    phik = (-1.5 * Om / a) * mesh.fwd(dtot) * mesh.ik2
    acc = [-a * mesh.inv(1j * kv * phik) for kv in mesh.kvec]; del phik
    extra = None; info = {}
    if EOM == "C" or diag:
        sw, catch, edge, s_ph, D = law_fields(mesh, dtot, db, a, branch, foot, dta, diag=diag)
        d, s_c = deficit(sw, s_ph, dc, a)
        if EOM == "C":
            cf = catch.astype(np.float32)                     # the response acts only inside bound systems (catchments), as in EOM A
            extra = [-a * cf * gi for gi in grad_psi(mesh, d)]
        if diag:
            tgt = sw * np.maximum(s_ph, 0.0); rho_c = 1.0 + dc; rho = 1.0 + dtot
            info.update(Delta_ta=D, d_sum=float(d.sum()), target_sum=float(tgt.sum()),
                        unfilled_frac=float(d.sum() / max(float(tgt.sum()), 1e-30)),
                        excess_sum_bookkeeping=float((sw * np.maximum(s_ph - s_c, 0.0)).sum()),
                        cold_frac_in_edge=float((rho_c * edge).sum() / rho_c.sum()), mass_frac_in_edge=float((rho * edge).sum() / rho.sum()),
                        cold_frac_in_catch=float((rho_c * catch).sum() / rho_c.sum()), mass_frac_in_catch=float((rho * catch).sum() / rho.sum()),
                        cold_over_baryon_in_edge=float((rho_c * edge).sum() / max(float(((1.0 + db) * edge).sum()), 1e-30)),
                        vol_edge=float(edge.mean()), vol_catch=float(catch.mean()), sw_vol=float((sw > 0.5).mean()),
                        finite=bool(np.all(np.isfinite(acc[0]))))
    return acc, extra, info

def run(branch, foot, npg):
    try:
        os.nice(10)
    except OSError:
        pass
    os.makedirs(WORK, exist_ok=True)
    tag = (f"cfg539_EOM{EOM}" + ("" if EDGE else "_NOEDGE") + (f"_mob{MOB:g}" if MOB != 1.0 else "") + f"_{branch}_{foot if EOM != 'OFF' else 'S0'}"
           f"_N{npg}_L{L:g}_ns{NSEED}" + ("_MUTATE" if MUTATE else ""))
    mesh = Mesh(npg); dta = dta_table(); t0 = time.time()
    pos_b, mom_b = initial_conditions(npg, 1.0)
    if EOM == "OFF":
        pos_c, mom_c = pos_b, mom_b                      # identical species: one array (exactly the single-species S0 path)
    else:
        pos_c, mom_c = pos_b.copy(), mom_b.copy()
    Dacc = np.zeros(pos_c.shape, np.float32) if EOM == "A" else None
    stat = {}
    aa = step_grid(); snaps = {0.5: "z1", 2 / 3: "z0.5", 1.0: "z0"}
    res = {"tag": tag, "eom": EOM, "edge": EDGE, "mob": MOB, "branch": branch, "foot": foot, "np": npg, "L": L, "nseed": NSEED, "rmin": RMIN_PHYS,
           "z_i": ZI, "nsteps": len(aa) - 1, "snap": {}}
    def accel(a, diag=False):
        dtot, db, dc = deposit2(mesh, pos_b, pos_c)
        acc, extra, info = forces2(mesh, dtot, db, dc, a, branch, foot, dta, diag=diag)
        ab = mesh.interp(acc, pos_b)
        if pos_c is pos_b:
            ac = ab
        else:
            ac = mesh.interp([x + e for x, e in zip(acc, extra)] if extra is not None else acc, pos_c)
        return ab, ac, info, dtot, db, dc
    def snapshot(name, a):
        _, _, info, dtot, db, dc = accel(a, diag=True)
        kb, pb, s8 = measure_pk(mesh, dtot, npg ** 3); sg = dict(_INC.get("sig", {}))
        out = dict(a=a, D=Dgrow(a), k=kb, P=pb, sigma8=s8, **sg, **info, t=time.time() - t0)
        if pos_c is not pos_b:
            _, pbb, _ = measure_pk(mesh, db, npg ** 3); _, pcc, _ = measure_pk(mesh, dc, npg ** 3)
            out.update(P_b=pbb, P_c=pcc)
            out["mom_c_sum"] = [float(x) for x in mom_c.sum(0)]; out["mom_b_sum"] = [float(x) for x in mom_b.sum(0)]
        if Dacc is not None:
            dn = np.sqrt((Dacc.astype(np.float64) ** 2).sum(1)) / mesh.dx
            out.update(drift_frac_gt_half_cell=float((dn > 0.5).mean()), drift_frac_gt_1cell=float((dn > 1.0).mean()),
                       drift_mean_cells=float(dn.mean()), drift_p99_cells=float(np.percentile(dn, 99)), **{f"settle_{k}": v for k, v in stat.items()})
        res["snap"][name] = out
        if name == "z0":
            sv = {"pos_b": pos_b.astype(np.float32)}
            if pos_c is not pos_b: sv["pos_c"] = pos_c.astype(np.float32)
            if Dacc is not None: sv["Dacc"] = Dacc
            np.savez_compressed(os.path.join(WORK, f"{tag}_z0.npz"), **sv)
        print(f"  [{tag}] {name} a={a:.4f} sigma8={s8:.4f} unfilled={info.get('unfilled_frac', 0):.3f} t={time.time() - t0:.0f}s", flush=True)
    snapshot("zi", AI)
    ab, ac, _, _, _, _ = accel(AI)
    for n in range(len(aa) - 1):
        a0, a1 = aa[n], aa[n + 1]; am = math.sqrt(a0 * a1)
        kick1 = quad(lambda x: 1 / (x * x * E(x)), a0, am)[0]
        mom_b += kick1 * ab
        if pos_c is not pos_b: mom_c += kick1 * ac
        dr = quad(lambda x: 1 / (x ** 3 * E(x)), a0, a1)[0]
        pos_b[:] = (pos_b + dr * mom_b) % L
        if pos_c is not pos_b: pos_c[:] = (pos_c + dr * mom_c) % L
        if EOM == "A":
            settle(mesh, pos_b, pos_c, Dacc, a1, quad(lambda x: 1 / (x * E(x)), a0, a1)[0], branch, foot, dta, stat)
        ab, ac, _, _, _, _ = accel(a1)
        kick2 = quad(lambda x: 1 / (x * x * E(x)), am, a1)[0]
        mom_b += kick2 * ab
        if pos_c is not pos_b: mom_c += kick2 * ac
        for asn, nm in snaps.items():
            if abs(a1 - asn) < 1e-9:
                snapshot(nm, a1)
    res["runtime_s"] = time.time() - t0; res["settle_stat"] = stat
    json.dump(res, open(os.path.join(WORK, f"{tag}.json"), "w"))
    return res

if __name__ == "__main__":
    br, ft, npg = sys.argv[1], sys.argv[2], int(sys.argv[3])
    run(br, ft, npg)
