#!/usr/bin/env python3
"""CFG378 engine: two species (baryons f_b, cold fluid 1 - f_b) from the same ICs, NEWTONIAN gravity from both, and the cold
particles settled toward the law's target in T1-ON cells by a DECLARED linearised Monge-Ampere (JKO) step (FROZEN_CRITERIA.md 18bfc1a98).
The settling scheme is declared, not derived (candidate mechanism: CFG373's khronon lapse channel, CONDITIONAL).
Pieces copied (not imported) from CFG374's engine cfg374_pm.py: constants, nu_mono, EH ICs, Delta_ta, Mesh/CIC, eig3, P(k), step grid,
the T1 switch and the MIX-A phase-weighted pressure filter of the phantom's baryon source.
Usage: python3 cfg378_pm.py MODE FOOT NP G      MODE = TWO (two species) | S0 (single species, control C2);  G = settling rate in 1/t_dyn
Env: CFG378_THREADS (default 2), CFG378_MUTATE=1 (target x10, separate outputs), CFG378_TAG (dev label).
"""
import os, sys
NTH = int(os.environ.get("CFG378_THREADS", "2"))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = str(NTH)
import json, math, time
import numpy as np
from scipy import fft as sfft
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg378_work"))
MUTATE = os.environ.get("CFG378_MUTATE", "0") == "1"
TMULT = 10.0 if MUTATE else 1.0                  # MUTATE: target x10
MIXA = (0.28, 0.54, 0.18)                        # CFG374 MIX-A (f_cool, f_hot, f_coll)
FLOOR_FRAC = 0.01                                # F = 0.01 (1 - f_b)
CAP_CELLS = 1.0                                  # |u| <= 1 mesh cell per step

# ---------------------------------------------------------------- constants (L352 values)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om; FB = om_b / (om_b + om_c)
NS, SIG8 = 0.965, 0.811
MPC = 3.0856775814913673e22
ACC_UNIT = 1e10 * h / MPC                       # H0^2 (Mpc/h) in m/s^2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
W0, WA = -0.838, -0.62                          # DESI DR2 CPL (chart_a0z_one.py), A0-DE only
L = 200.0; ZI = 49.0; AI = 1.0 / (1 + ZI); SEED = 359; NSEED = 256
EPS = 0.077
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
DTA_FILE = os.path.join(WORK, "cfg361_delta_ta_table.json")   # copied table name; computed locally if absent
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
    x = (kk * 8.0).astype(np.float64); x = np.where(x > 0, x, 1e-3)
    s8 = math.sqrt(float(np.sum(wt * pk3 * (3 * (np.sin(x) - x * np.cos(x)) / x ** 3) ** 2)) / L ** 3)
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

# ================================================================ CFG378 additions
def deposit_raw(mesh, pos):
    """CIC mass counts (float64, particle units); total = N exactly up to float64 rounding."""
    M = mesh.M; u = pos / mesh.dx; i0 = np.floor(u).astype(np.int64); w = u - i0; del u    # float64 weights (exact partition of unity)
    i1 = (i0 + 1) % M; i0 %= M; rho = np.zeros(M ** 3, np.float64)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
    return rho.reshape((M,) * 3)

def switch_field(mesh, dk_tot, a, dta):
    """CFG361 T1 switch f on the TOTAL field (copied logic from CFG374 forces())."""
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [mesh.inv(mesh.kvec[i] * mesh.kvec[j] * dk_tot * mesh.ik2) for i, j in tk]
    l1, l2, l3 = eig3(t); del t
    D = math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))
    tau = (D - 1.0) / 3.0
    return np.clip(0.5 + (l2 - tau) / (2 * EPS), 0, 1).astype(np.float32)

def target_field(mesh, d_b, a, foot):
    """rho_t / rho_bar_m = max(TMULT * s_ph / (1.5 Om / a), F); s_ph from the MIX-A-filtered BARYON species (CFG374 algebra)."""
    dkb = mesh.fwd(d_b); phik_b = (-1.5 * Om / a) * dkb * mesh.ik2; del dkb
    fc, fh, fs = MIXA; kk = mesh.kx ** 2 + mesh.ky ** 2 + mesh.kz ** 2
    kJ = lambda T: math.sqrt(1.5 * Om * a) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (fc / (1.0 + kk / kJ(1e4) ** 2) + fh / (1.0 + kk / kJ(1e6) ** 2) + fs).astype(np.float32); del kk
    gb = [FB * (-mesh.inv(1j * kv * phik_b * Wk)) for kv in mesh.kvec]; del Wk, phik_b
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (a * a0_code(a, "FLAT", foot))
    w = (nu_mono(y) - 1.0).astype(np.float32); del y
    divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gb)); del gb, w
    s_ph = -mesh.inv(divk); del divk
    F = FLOOR_FRAC * (1.0 - FB)
    return np.maximum(TMULT * s_ph / (1.5 * Om / a), F).astype(np.float32), s_ph

def settle(mesh, pos_c, rho_c_raw, rho_t, lam):
    """one linearised Monge-Ampere step: lap psi = S - <S>, S = lam log(rho_c/rho_t); cold particles move by grad psi (capped)."""
    F = FLOOR_FRAC * (1.0 - FB)
    rho_c = np.maximum(rho_c_raw, F)
    S = (lam * np.log(rho_c / rho_t)).astype(np.float32); S -= np.float32(S.mean())
    Sk = mesh.fwd(S); del S
    ug = [mesh.inv(1j * kv * (-Sk * mesh.ik2)) for kv in mesh.kvec]; del Sk   # psi_k = -S_k/k^2, u = grad psi
    u = mesh.interp(ug, pos_c).astype(np.float64); del ug
    mag = np.sqrt((u * u).sum(1)); cap = CAP_CELLS * mesh.dx
    clip = mag > cap
    if clip.any():
        u[clip] *= (cap / mag[clip])[:, None]
    pos_c += u; pos_c %= L
    um = np.minimum(mag, cap)
    return dict(u_rms=float(np.sqrt(np.mean(um ** 2))), u_max=float(um.max()), clip_frac=float(clip.mean()),
                u_rms_moving=float(np.sqrt(np.mean(um[um > 0] ** 2))) if (um > 0).any() else 0.0)

def cosmic_dt(a0, a1):
    return quad(lambda x: 1.0 / (x * E(x)), a0, a1)[0]       # 1/H0 units

class State:
    def __init__(self, mode, foot, npg, g):
        self.mode, self.foot, self.npg, self.g = mode, foot, npg, g
        self.mesh = Mesh(npg); self.dta = dta_table(); self.N = npg ** 3
    def fields(self, pos_b, pos_c):
        m = self.mesh
        rc = deposit_raw(m, pos_c); dc = (rc / (self.N / m.M ** 3) - 1.0).astype(np.float32)
        if pos_b is None:
            return None, dc, dc, rc
        db = m.deposit(pos_b)
        dt = (FB * db + (1.0 - FB) * dc).astype(np.float32)
        return db, dc, dt, rc
    def settle_step(self, a, dtc, pos_b, pos_c):
        db, dc, dtot, rc = self.fields(pos_b, pos_c)
        m = self.mesh; dk = m.fwd(dtot)
        fsw = switch_field(m, dk, a, self.dta); del dk
        rho_t, _ = target_field(m, db, a, self.foot)
        Gam = self.g * np.sqrt(np.maximum(1.5 * Om * (1.0 + dtot) / a ** 3, 0.0) / (4 * math.pi))   # sqrt(G rho_phys) in H0
        lam = (fsw * (1.0 - np.exp(-Gam * dtc))).astype(np.float32); del Gam
        info = settle(m, pos_c, (1.0 - FB) * (1.0 + dc), rho_t, lam)
        info["lam_mean_on"] = float(lam[fsw > 0.5].mean()) if (fsw > 0.5).any() else 0.0
        info["v_rms_kms"] = 100.0 * a * info["u_rms"] / dtc; info["v_max_kms"] = 100.0 * a * info["u_max"] / dtc
        return info
    def accel(self, a, pos_b, pos_c):
        _, _, dtot, _ = self.fields(pos_b, pos_c)
        m = self.mesh; phik = (-1.5 * Om / a) * m.fwd(dtot) * m.ik2
        return [-a * m.inv(1j * kv * phik) for kv in m.kvec]
    def diag(self, a, pos_b, pos_c):
        db, dc, dtot, rc = self.fields(pos_b, pos_c)
        m = self.mesh; out = {}
        out["cold_count"] = int(pos_c.shape[0]); out["cold_mass_total_rel_err"] = float(abs(rc.sum() - self.N) / self.N)
        out["cold_min_cic"] = float(rc.min())
        kb, pb, s8 = measure_pk(m, dtot, self.N); out.update(k=kb, P=pb, sigma8=s8)
        if pos_b is not None:
            _, pc, s8c = measure_pk(m, dc, self.N); _, pbb, s8b = measure_pk(m, db, self.N)
            out.update(P_cold=pc, sigma8_cold=s8c, P_bar=pbb, sigma8_bar=s8b)
            fsw = switch_field(m, m.fwd(dtot), a, self.dta)
            rho_t, s_ph = target_field(m, db, a, self.foot)
            rho_c = (1.0 - FB) * (1.0 + dc)
            F = FLOOR_FRAC * (1.0 - FB)
            den = float(np.sum(fsw * rho_t))
            out["R"] = float(np.sum(fsw * np.minimum(rho_c, rho_t))) / den if den > 0 else None
            out["Q"] = float(np.sum(fsw * rho_c)) / den if den > 0 else None
            out["target_on_mass"] = float(np.sum(fsw * rho_t)) / fsw.size; out["cold_on_mass"] = float(np.sum(fsw * rho_c)) / fsw.size
            on = fsw > 0.5; rho = 1.0 + dtot
            out["mass_on"] = float((rho * on).mean())
            out["mass_on_cold_above_target"] = float((rho * (on & (rho_c > rho_t))).sum() / max((rho * on).sum(), 1e-30))
            out["target_floor_frac_on"] = float((on & (rho_t <= F * 1.0000001)).sum() / max(on.sum(), 1))
            out["vol_on"] = float(on.mean())
        return out

def run(mode, foot, npg, g):
    try:
        os.nice(10)
    except OSError:
        pass
    os.makedirs(WORK, exist_ok=True)
    dev = os.environ.get("CFG378_TAG", "")
    tag = f"{mode}_g{g:g}_FLAT_{foot}_N{npg}" + (f"_{dev}" if dev else "") + ("_MUTATE" if MUTATE else "")
    st = State(mode, foot, npg, g); t0 = time.time()
    pos, mom = initial_conditions(npg, 1.0)
    if mode == "TWO":
        pos_b, mom_b = pos.copy(), mom.copy(); pos_c, mom_c = pos, mom
    else:
        pos_b = mom_b = None; pos_c, mom_c = pos, mom
    aa = step_grid(); snaps = {0.5: "z1", 2 / 3: "z0.5", 1.0: "z0"}
    res = {"lane": "CFG378", "frozen": "18bfc1a98", "tag": tag, "mode": mode, "foot": foot, "np": npg, "g": g, "mutate": MUTATE,
           "target_mult": TMULT, "L": L, "z_i": ZI, "nsteps": len(aa) - 1, "snap": {}, "settle_log": []}
    def snapshot(name, a):
        d = st.diag(a, pos_b, pos_c); res["snap"][name] = dict(a=a, D=Dgrow(a), t=time.time() - t0, **d)
        print(f"  [{tag}] {name} a={a:.4f} s8={d['sigma8']:.5f} R={d.get('R') or float('nan'):.3f} Q={d.get('Q') or float('nan'):.3f} "
              f"massrel={d['cold_mass_total_rel_err']:.1e} t={time.time() - t0:.0f}s", flush=True)
    snapshot("zi", AI)
    def kick_all(acc, dK):
        for p, mm in ((pos_b, mom_b), (pos_c, mom_c)):
            if p is not None:
                mm += dK * st.mesh.interp(acc, p)
    acc = st.accel(AI, pos_b, pos_c)
    for n in range(len(aa) - 1):
        a0, a1 = aa[n], aa[n + 1]; am = math.sqrt(a0 * a1)
        kick_all(acc, quad(lambda x: 1 / (x * x * E(x)), a0, am)[0])
        dD = quad(lambda x: 1 / (x ** 3 * E(x)), a0, a1)[0]
        for p, mm in ((pos_b, mom_b), (pos_c, mom_c)):
            if p is not None:
                p += dD * mm; p %= L
        if mode == "TWO" and g > 0:
            info = st.settle_step(a1, cosmic_dt(a0, a1), pos_b, pos_c); info["a"] = a1; res["settle_log"].append(info)
        acc = st.accel(a1, pos_b, pos_c)
        kick_all(acc, quad(lambda x: 1 / (x * x * E(x)), am, a1)[0])
        for asn, nm in snaps.items():
            if abs(a1 - asn) < 1e-9:
                snapshot(nm, a1)
    res["runtime_s"] = time.time() - t0
    json.dump(res, open(os.path.join(WORK, f"cfg378_{tag}.json"), "w"))
    np.savez_compressed(os.path.join(WORK, f"cfg378_{tag}_z0.npz"), pos_c=pos_c.astype(np.float32),
                        pos_b=(pos_b.astype(np.float32) if pos_b is not None else np.zeros(0, np.float32)))
    return res

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
