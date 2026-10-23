#!/usr/bin/env python3
"""S4_v3_muK_clusters (criteria f167979b09), batch R6 of N0_board_audit: v3's full static equation
    div[ mu(|grad psi|/a0) grad psi ] + mu_K^2 psi = 4 pi G rho_b ,  mu = x/(1+x),  phi = psi   (BS24 Eq. 35 via C4 K1)
solved exactly in spherical symmetry on (i) F1's 326-cluster PRIMARY KiDS stack (F1's measurement cache via argv, read-only)
and (ii) F2's Track A isolated-lens stack (B21 Fig. 3), at mu_K over BS24 Eq. 39's allowed range and F3's growth values.
Spherical form: r^2 mu(|psi'|/a0) psi' = G (M_b + M_K),  M_K' = -mu_K^2 r^2 psi / G  (M_K = hydrostatic K(Q) dust mass).
Usage: OMP_NUM_THREADS=1 nice -n 15 python3 s4_v3_muk_clusters.py <dir holding f1_meas.pkl> [--mutate] [--quick]
--mutate: mu_K^2 -> -mu_K^2 (Yukawa), on the reduced (--quick) grids; K2, K3, K4 must FAIL.  --quick: small grids, outputs to the cache dir (test only).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, time, math, pickle, hashlib, resource, gc, ctypes
import numpy as np
from scipy.integrate import quad
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
MUT = "--mutate" in sys.argv; QUICK = "--quick" in sys.argv
TAG = ("_MUTATE" if MUT else "") + ("_QUICK" if QUICK else "")
SGN = -1.0 if MUT else 1.0                       # sign of the mass term; +1 = v3 (Helmholtz)
CACHE = ARGS[0]
OUTDIR = CACHE if QUICK else HERE
np.seterr(all="ignore")
OUTF = open(os.path.join(OUTDIR, f"s4_v3_muk_clusters{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"lane": "S4_v3_muK_clusters", "batch": "R6", "criteria": "f167979b09", "mutate": MUT, "quick": QUICK}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
try: _LIBC = ctypes.CDLL(None); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception: _LIBC = None
def relieve():                                    # macOS: hand freed blocks back to the OS (RSS hygiene only)
    gc.collect()
    if _LIBC is not None and sys.platform == "darwin": _LIBC.malloc_zone_pressure_relief(None, ctypes.c_size_t(0))
def rss_gb():
    pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; return pk / 1e9 if sys.platform == "darwin" else pk / 1e6
def stamp(tag): say(f"  [{time.time() - T0:.0f} s, peak RSS {rss_gb():.3f} GB] {tag}")

# ================================================================ constants (F1's conventions)
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; PC = 3.0857e16; KG_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                    # kappa = 1/2 FITTED
FOOTS = ("canonical", "alt"); HS = {"h0672": 0.672, "h0686": 0.686}
CELLS = [(hk, f) for hk in HS for f in FOOTS]
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RCB = np.sqrt(EDGES[1:] * EDGES[:-1])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
MU_OK = [0.015637, 0.03, 0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 3.333, 5.0, 10.0]          # physical Mpc^-1; 10 = BS24 Eq. 39 cap
MU_GROW = [243.78, 277.82, 1718.0]                                                # F3 K5 (excluded by Eq. 39)
MU_PROFILE = [10.0, 3.333, 1.0]                                                   # mu_K^-1 = 0.1, 0.3, 1 Mpc
DEL = np.round(np.arange(-8, 2.0001, 0.25), 4); I0 = int(np.argmin(np.abs(DEL)))
DEL_G = np.array([-8.0, -4.0, -2.0, -1.0, 0.0, 1.0, 2.0]); I0G = 4
if QUICK or MUT:                                   # --mutate runs on the reduced grids (it only has to break K2/K3/K4)
    MU_OK = [0.1, 1.0, 10.0]; MU_GROW = [243.78]; DEL = np.array([-1.0, 0.0, 1.0]); I0 = 1; DEL_G = np.array([0.0]); I0G = 0
RMAX = 30.0                                                                       # Mpc (criteria B9)
OM_B, H_B, WB_B = 0.2976016, 0.6856427, 0.0223081                                 # model B (L1 ledger)
OMK = OM_B - WB_B / H_B ** 2
RHOC0 = 3 * (H_B * 100e3 / MPC) ** 2 / (8 * np.pi * G)
RES["dust_sign_model"] = dict(Omega_K=OMK, rho_crit0_kg_m3=RHOC0, note="Omega_K = Omega_m - Omega_b on model B; FITTED abundance")

def g_aqual(y, a0):
    """root of g^2/(g + a0) = |y| with the sign of y (AQUAL mu = x/(1+x) in spherical symmetry); Newton if a0 == 0."""
    if np.isscalar(a0) and a0 == 0: return y
    ay = np.abs(y); return np.copysign(0.5 * ay + np.sqrt(ay * (0.25 * ay + a0)), y)

# ================================================================ grids
def seg_log_lin(rmin, rmax, dlnr, drmax):
    """log steps dlnr from rmin until the step reaches drmax, then uniform <= drmax; both ends exact."""
    r_sw = drmax / (math.exp(dlnr) - 1.0)
    if r_sw > rmin:
        n = int(math.ceil(math.log(min(r_sw, rmax) / rmin) / dlnr)); r_log = rmin * np.exp(dlnr * np.arange(n + 1)); r_log = r_log[r_log < rmax]
    else: r_log = np.array([rmin])
    r0 = r_log[-1]; n = max(1, int(math.ceil((rmax - r0) / drmax)))
    return np.r_[r_log[:-1], np.linspace(r0, rmax, n + 1)]
def proj_grid(rmin, dlnr, dr_fine, r_fine=6.0, dr_far=0.05, rmax=RMAX, breaks=(3.0,)):
    """projection nodes: log, then uniform dr_fine to r_fine (3 Mpc a node), then uniform dr_far to rmax."""
    bks = [b for b in breaks if rmin < b < min(r_fine, rmax)]
    segs = [seg_log_lin(rmin, bks[0] if bks else r_fine, dlnr, dr_fine)]
    pts = bks + [r_fine]
    for a, b in zip(pts[:-1], pts[1:]): segs.append(np.linspace(a, b, max(1, int(math.ceil((b - a) / dr_fine))) + 1))
    if rmax > r_fine: segs.append(np.linspace(r_fine, rmax, max(1, int(math.ceil((rmax - r_fine) / dr_far))) + 1))
    return np.unique(np.concatenate(segs))
def nsub_for(nodes, dr_ode): return np.maximum(1, np.ceil(np.diff(nodes) / dr_ode - 1e-9).astype(int))
def dr_ode_cluster(mu, half=False):
    """ODE step (Mpc): >= ~150 steps per far-field oscillation inside 6 Mpc, >= ~40 beyond (lambda_far ~ 0.22 (10/mu)^0.8 Mpc)."""
    lam = 0.22 * (10.0 / max(mu, 1e-9)) ** 0.8; f = 0.5 if half else 1.0
    return min(2e-3, lam / 150) * f, min(1e-2, lam / 40) * f

# ================================================================ the spherical solver (RK4 in r, sub-steps per projection cell)
def integrate(pnodes, nsub, Mb_fn, phi0, D0, mu2, a0, consumers, chunk=250, sgn=None):
    """State (psi, D) per object (shape S).  Mb_fn(r_Mpc) -> array broadcastable to S (kg).
    psi' = g_aqual(G (Mb + D)/r^2), D' = -sgn mu2 r^2 psi / G.  Consumers get, at projection nodes k0..k0+m-1,
    (k0, r_nodes[m], ML[m,*S], psi, D, Mb) with ML = r^2 psi'/G.  nsub[k]: RK4 sub-steps in cell k."""
    sgn = SGN if sgn is None else sgn
    r = pnodes * MPC; n = len(r)
    psi = np.array(phi0, float); D = np.array(D0, float); psi, D = np.broadcast_arrays(psi, D); psi = psi.copy(); D = D.copy(); S = psi.shape
    c2 = -sgn * mu2 / G
    def f(rr, Mb, p, d): return g_aqual(G * (Mb + d) / (rr * rr), a0), (c2 * rr * rr) * p
    bufML = np.empty((chunk,) + S); bufP = np.empty((chunk,) + S); bufD = np.empty((chunk,) + S); bufM = np.empty((chunk,) + S)
    Mb_k = np.broadcast_to(Mb_fn(pnodes[0]), S); j = 0; k0 = 0
    for k in range(n):
        g1, d1 = f(r[k], Mb_k, psi, D)
        if consumers:
            bufML[j] = r[k] * r[k] * g1 / G; bufP[j] = psi; bufD[j] = D; bufM[j] = Mb_k
        j += 1
        if j == chunk or k == n - 1:
            for c in consumers: c(k0, pnodes[k0:k0 + j], bufML[:j], bufP[:j], bufD[:j], bufM[:j])
            k0 += j; j = 0
        if k == n - 1: break
        ns = int(nsub[k]); h = (r[k + 1] - r[k]) / ns; hM = (pnodes[k + 1] - pnodes[k]) / ns
        for s_ in range(ns):
            rs = r[k] + s_ * h; rM_ = pnodes[k] + s_ * hM
            if s_ > 0: g1, d1 = f(rs, Mb_k, psi, D)
            Mb_m = np.broadcast_to(Mb_fn(rM_ + 0.5 * hM), S); Mb_n = np.broadcast_to(Mb_fn(pnodes[k + 1] if s_ == ns - 1 else rM_ + hM), S)
            g2, d2 = f(rs + 0.5 * h, Mb_m, psi + 0.5 * h * g1, D + 0.5 * h * d1)
            g3, d3 = f(rs + 0.5 * h, Mb_m, psi + 0.5 * h * g2, D + 0.5 * h * d2)
            g4, d4 = f(rs + h, Mb_n, psi + h * g3, D + h * d3)
            psi = psi + (h / 6.0) * (g1 + 2 * g2 + 2 * g3 + g4); D = D + (h / 6.0) * (d1 + 2 * d2 + 2 * d3 + d4)
            Mb_k = Mb_n
    return psi, D

_ICACHE = {}
def lam_max(mu, rM): return (2 / 3) * (1 - np.log(3 * np.sqrt(2) / (mu * rM)))
def zero_point(pnodes, nsub, Mb_fn, Mtot, a0, mu_Mpc, Dl, key, Rref=3.0):
    """psi(r_min) such that the mu_K = 0 solution started there (same integrator, same steps) equals
    -GM/R + s(lambda + ln(R/r_M)) at R = 3 Mpc (a node), lambda = lambda_max(mu_K, r_M) + Delta (VSZ via H2).  (nDelta, nobj)."""
    k3 = int(np.argmin(np.abs(pnodes - Rref))); assert abs(pnodes[k3] - Rref) < 1e-12
    ck = (key, float(np.max(a0)), len(pnodes), float(pnodes[0]), int(np.sum(nsub[:k3])))
    if ck not in _ICACHE:
        shp = np.broadcast(np.asarray(Mb_fn(pnodes[0])), np.zeros(np.shape(Mtot))).shape
        p3, _ = integrate(pnodes[:k3 + 1], nsub[:k3], Mb_fn, np.zeros(shp), np.zeros(shp), 0.0, a0, [], sgn=1.0)
        _ICACHE[ck] = np.reshape(p3, np.shape(Mtot))
    I = _ICACHE[ck]
    a0f = np.reshape(np.broadcast_to(a0, np.broadcast(np.asarray(a0), np.zeros(np.shape(Mtot))).shape), np.shape(Mtot))
    mu = mu_Mpc / MPC; s = np.sqrt(G * Mtot * a0f); rM = np.sqrt(G * Mtot / a0f); R = Rref * MPC
    lam = lam_max(mu, rM)[None, :] + np.asarray(Dl, float)[:, None]
    return (-(G * Mtot / R))[None, :] + s[None, :] * (lam + np.log(R / rM)[None, :]) - I[None, :]

# ================================================================ projection kernels
def Iw(r, R):
    """antiderivative in r of w(r;R) = 1 (r <= R), 1 - sqrt(1 - R^2/r^2) (r > R) (fraction of a shell inside a cylinder)."""
    rr = np.maximum(r, R); out = rr - np.sqrt(np.maximum(rr * rr - R * R, 0.0)) + R * np.arccos(np.clip(R / rr, -1, 1))
    return np.where(r <= R, r, out)
def Fw(u):
    s = np.sqrt(np.clip(1 - u * u, 0, None)); return np.log1p(s) - s
def Wker(r, R1, R2):
    """int_{R1}^{R2} w(r;R)/R dR."""
    rs = np.maximum(r, 1e-300)
    return np.where(r <= R1, np.log(R2 / R1), np.where(r >= R2, Fw(R2 / rs) - Fw(R1 / rs), np.log(R2 / rs) - Fw(R1 / rs)))
def annulus_kernel(ra, rb, E1, E2):
    """(cells, J): annulus-averaged Delta Sigma per unit cell mass, M linear in each cell [ra, rb] (m)."""
    ra = ra[:, None]; rb = rb[:, None]; dr = rb - ra; rm = 0.5 * (ra + rb); E1 = E1[None, :]; E2 = E2[None, :]
    w2 = (Iw(rb, E2) - Iw(ra, E2)) / dr; w1 = (Iw(rb, E1) - Iw(ra, E1)) / dr
    return (2.0 / (E2 ** 2 - E1 ** 2)) * (Wker(rm, E1, E2) / np.pi - (w2 - w1) / (2 * np.pi))
def point_kernel(E1, E2): return (2.0 / (E2 ** 2 - E1 ** 2)) * np.log(E2 / E1) / np.pi
def shell_sigma_kernel(ra, rb, R):
    """(len(R), cells): Sigma(R) per unit cell mass, M linear in [ra, rb] (m)."""
    ra = ra[None, :]; rb = rb[None, :]; Rr = R[:, None]; lo = np.maximum(ra, Rr)
    val = (np.arccos(np.clip(Rr / rb, -1, 1)) - np.arccos(np.clip(Rr / lo, -1, 1))) / ((rb - ra) * 2 * np.pi * Rr)
    return np.where(Rr < rb, val, 0.0)

class AnnulusAcc:
    """consumer: annulus-averaged Delta Sigma (kg/m^2) of M_L (central point mass included), J annuli (edges in Mpc).
    mfac: optional callable(r_nodes_Mpc) -> multiplicative factor on M_L (the labelled EFE approximation)."""
    def __init__(self, E1, E2, mfac=None):
        self.E1 = np.asarray(E1, float) * MPC; self.E2 = np.asarray(E2, float) * MPC; self.out = None; self.prev = None; self.mfac = mfac
    def __call__(self, k0, rn, ML, P, D, Mb):
        if self.mfac is not None: ML = ML * self.mfac(rn)
        r = rn * MPC
        if self.prev is None:
            self.out = np.tensordot(ML[0], point_kernel(self.E1, self.E2), axes=0); rr = r; MM = ML
        else:
            rr = np.r_[self.prev[0], r]; MM = np.concatenate([self.prev[1][None], ML], 0)
        if len(rr) > 1:
            self.out = self.out + np.tensordot(MM[1:] - MM[:-1], annulus_kernel(rr[:-1], rr[1:], self.E1, self.E2), axes=([0], [0]))
        self.prev = (r[-1], ML[-1].copy())

class ProjT:
    """consumer: node k's mass increment (k = 0: central point mass) times column k of each per-cluster operator (float32, per Msun)."""
    def __init__(self, T): self.T = T; self.out = {w: 0.0 for w in T}; self.prev = None
    def __call__(self, k0, rn, ML, P, D, Mb):
        dM = (ML - np.concatenate([ML[:1] * 0.0 if self.prev is None else self.prev[None], ML[:-1]], 0)) / MSUN
        dMt = np.ascontiguousarray(dM.transpose(2, 0, 1))                                     # (N, m, nD)
        for w, T in self.T.items():
            self.out[w] = self.out[w] + np.matmul(T[:, :, k0:k0 + len(rn)].astype(np.float64), dMt).transpose(2, 0, 1)
        self.prev = ML[-1].copy()

class Diag:
    """consumer: values at chosen radii, first zero crossings, negative-absolute-dust volume fraction in [rlo, rhi]."""
    def __init__(self, nodes, radii, mu2, rho_bar, rlo, rhi):
        self.idx = {float(R): int(np.argmin(np.abs(nodes - R))) for R in radii}; self.mu2 = mu2; self.rho_bar = rho_bar
        self.rlo, self.rhi = rlo, rhi; self.vals = {}; self.z = None; self.vneg = None; self.vtot = 0.0; self.rprev = None
    def __call__(self, k0, rn, ML, P, D, Mb):
        if self.z is None: self.z = {k: np.full(P.shape[1:], np.nan) for k in ("psi", "MK", "ML")}; self.vneg = np.zeros(P.shape[1:])
        for R, i in self.idx.items():
            if k0 <= i < k0 + len(rn):
                j = i - k0; self.vals[R] = dict(r=float(rn[j]), psi=P[j].copy(), MK=D[j].copy(), ML=ML[j].copy(), Mb=Mb[j].copy())
        for key, cond in (("psi", P >= 0), ("MK", D < 0), ("ML", ML < 0)):
            zarr = self.z[key]; hit = cond & np.isnan(zarr)[None]
            if hit.any():
                first = np.argmax(hit, axis=0); anyh = hit.any(axis=0); zarr[anyh] = rn[first[anyh]]
        r = rn * MPC; rp = np.r_[self.rprev if self.rprev is not None else r[0], r[:-1]]
        dv = 4 * np.pi * r * r * (r - rp); inr = (rn >= self.rlo) & (rn <= self.rhi)
        if self.mu2 > 0 and inr.any():
            thr = 4 * np.pi * G * self.rho_bar / self.mu2          # delta rho_K = -mu2 psi/(4 pi G) < -rho_bar  <=>  psi > thr
            self.vneg = self.vneg + np.tensordot(dv[inr], P[inr] > thr, axes=([0], [0]))
        self.vtot += float(dv[inr].sum()); self.rprev = r[-1]
    def frac_neg(self): return self.vneg / self.vtot if self.vtot > 0 else self.vneg * np.nan

# ================================================================ K3, K4: analytic Newtonian Helmholtz tests (a0 = 0)
def k3_test(mu_Mpc, nodes, nsub):
    mu = mu_Mpc / MPC; Phic = 1e12; r0 = nodes[0] * MPC; x0 = mu * r0
    psi0 = Phic * np.sin(x0) / x0; D0 = r0 ** 2 * Phic * (x0 * np.cos(x0) - np.sin(x0)) / (x0 * r0) / G
    sel = nodes <= 20 / mu_Mpc; nn = nodes[sel]; Ps = np.empty(len(nn))
    def keep(k0, rn, ML, P, D, Mb): Ps[k0:k0 + len(rn)] = P
    integrate(nn, nsub[:len(nn) - 1], lambda r: 0.0, psi0, D0, mu ** 2, 0.0, [keep])
    rr = nn * MPC; return float(np.max(np.abs(Ps - Phic * np.sin(mu * rr) / (mu * rr))) / Phic)
PNODES = proj_grid(1e-3, 0.0035, 2e-3)                                            # cluster projection nodes, mu_K <= 2 (A1)
PNODES_F = proj_grid(1e-3, 0.00175, 5e-4)                                         # cluster projection nodes, mu_K >= 3.333 (A1)
def cluster_grid(mu): return PNODES if mu <= 2.0 else PNODES_F
def grid_growth(mu, half=False, rmin=1e-5):
    f = 0.5 if half else 1.0; dr = (2 * np.pi / mu / 200) * f
    nodes = proj_grid(rmin, 0.0035 * f, dr, r_fine=RMAX, rmax=RMAX); return nodes, np.ones(len(nodes) - 1, int)
dra, drf = dr_ode_cluster(10.0); nsA10 = np.where(PNODES[1:] <= 6.0 + 1e-9, nsub_for(PNODES, dra), nsub_for(PNODES, drf))
ng, nsg = grid_growth(1718.0)
e3a = k3_test(10.0, PNODES, nsA10); e3b = k3_test(1718.0, ng[:100000], nsg[:99999])
check("K3", max(e3a, e3b) <= 1e-6, f"max|psi - Phic sin(mu r)/(mu r)|/Phic = {e3a:.2e} (mu 10, cluster grid) / {e3b:.2e} (mu 1718, growth grid)", "<= 1e-6 (r <= 20/mu)")
del ng, nsg
mu_t = 3.333 / MPC; ka = int(np.argmin(np.abs(PNODES - 0.3))); a_th = PNODES[ka] * MPC; rho0 = 1e-22
Mth = lambda r_: 4 / 3 * np.pi * rho0 * np.minimum(r_ * MPC, a_th) ** 3
Phic4 = -2e12; Kc = 4 * np.pi * G * rho0 / mu_t ** 2; A_ = Phic4 - Kc
def th_in(r_): x = mu_t * r_; return Kc + A_ * np.sin(x) / x, A_ * (x * np.cos(x) - np.sin(x)) / (x * r_)
Pa, dPa = th_in(a_th); ca, sa = np.cos(mu_t * a_th), np.sin(mu_t * a_th)
M2 = np.array([[ca / a_th, sa / a_th], [(-mu_t * a_th * sa - ca) / a_th ** 2, (mu_t * a_th * ca - sa) / a_th ** 2]]); Bc, Cc = np.linalg.solve(M2, [Pa, dPa])
def th_d(r_):
    din = th_in(np.minimum(r_, a_th))[1]; x = mu_t * r_
    dout = Bc * (-mu_t * r_ * np.sin(x) - np.cos(x)) / r_ ** 2 + Cc * (mu_t * r_ * np.cos(x) - np.sin(x)) / r_ ** 2
    return np.where(r_ <= a_th, din, dout)
n4 = PNODES[PNODES <= 3.0]; rr4 = n4 * MPC; p0, dp0 = th_in(rr4[0]); D04 = rr4[0] ** 2 * dp0 / G - Mth(n4[0]); g4 = np.empty(len(n4))
def keep4(k0, rn, ML, P, D, Mb): g4[k0:k0 + len(rn)] = ML * G / (rn * MPC) ** 2
integrate(n4, nsub_for(n4, 1e-3), Mth, p0, D04, mu_t ** 2, 0.0, [keep4])
e4 = float(np.max(np.abs(g4 - th_d(rr4))) / np.max(np.abs(th_d(rr4))))
check("K4", e4 <= 1e-5, f"max|psi' - analytic|/max|psi'| = {e4:.2e} (top-hat a = {PNODES[ka]:.4f} Mpc, mu 3.333)", "<= 1e-5")
stamp("K3/K4 done")

# ================================================================ F1's measurement (read-only), data, baryons
PK = os.path.join(CACHE, "f1_meas.pkl"); sha = hashlib.sha256(open(PK, "rb").read()).hexdigest()
MEAS = pickle.load(open(PK, "rb")); N = len(MEAS); say(f"F1 measurement f1_meas.pkl sha256 {sha}  clusters {N}"); RES["f1_meas_sha256"] = sha
order = np.argsort([o["ra"] for o in MEAS]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N) * 30 // N
from scipy.interpolate import PchipInterpolator
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455) / (0.706 - 0.510) * (0.510 - 0.295); DMb = np.sqrt(7.942 ** 3 / (0.295 * DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33)) * HRD / h
def DA_lcdm(z, H0=70.0, Om=0.3):
    zz = np.linspace(0, z, 600); E = np.sqrt(Om * (1 + zz) ** 3 + 1 - Om); return np.trapz(1 / E, zz) * C / 1e3 / H0 / (1 + z)
DAT = {}
for hk in HS:
    D_ = np.array([o[hk]["D"] for o in MEAS]); Eh = np.array([o[hk]["E"] for o in MEAS]); W_ = np.where(Eh < 1e8, 1 / Eh ** 2, 0)
    B_ = np.array([o[hk]["den"] for o in MEAS]).sum(0) / np.array([o[hk]["den_r"] for o in MEAS]).sum(0)
    DAT[hk] = dict(D=D_, W=W_, B=B_)
ZC = np.array([o["z"] for o in MEAS])
GAS = {}
for hk, h in HS.items():
    q = np.array([(float(DM(o["z"], h)) / (1 + o["z"])) / DA_lcdm(o["z"]) for o in MEAS])
    Mg5 = np.array([o["Mgas500"] for o in MEAS]) * q ** 2.5 * MSUN; R5 = np.array([o["R500"] for o in MEAS]) * q
    rc = 0.15 * R5; x5 = R5 / rc; Kn = Mg5 / (x5 - np.arctan(x5)) * 1.20                     # x 1.20: f* = 0.20 (F1 PRIMARY)
    mis = np.array([np.radians(o["off_deg"]) * float(DM(o["z"], h)) / (1 + o["z"]) for o in MEAS])
    GAS[hk] = dict(rc=rc, K=Kn, mis=mis, Mtot=Kn * (3.0 / rc - np.arctan(3.0 / rc)))
def Mb_cluster(hk):
    rc, Kn = GAS[hk]["rc"], GAS[hk]["K"]
    def fn(r):
        x = min(r, 3.0) / rc; return Kn * (x - np.arctan(x))
    return fn
def rho_b_cluster(hk, r):
    rc, Kn = GAS[hk]["rc"], GAS[hk]["K"]; x = r / rc
    return np.where(r <= 3.0, Kn * x * x / (1 + x * x) / (4 * np.pi * (r * MPC) ** 2 * rc * MPC), 0.0)

# ================================================================ cluster operators (P1: F1 convention; P3: fine + annulus)
RF1 = np.logspace(np.log10(2e-3), np.log10(3.5), 90); RF3 = np.logspace(np.log10(2e-3), np.log10(3.5), 600)
def dsig_matrix(RF):
    n = len(RF); E = np.eye(n); out = np.empty((n, n))
    for k in range(n):
        Sig = E[:, k]
        cum = np.r_[0.5 * Sig[0] * RF[0] ** 2, 0.5 * Sig[0] * RF[0] ** 2 + np.cumsum(0.5 * (Sig[1:] * RF[1:] + Sig[:-1] * RF[:-1]) * np.diff(RF))]
        out[:, k] = 2 * cum / RF ** 2 - Sig
    return out
def interp_rows(xq, xg):
    xq = np.clip(xq, xg[0], xg[-1]); i = np.clip(np.searchsorted(xg, xq) - 1, 0, len(xg) - 2); t = (xq - xg[i]) / (xg[i + 1] - xg[i]); return i, t
def offset_matrix(RF, d):
    n = len(RF)
    if d <= 1e-4: return np.eye(n)
    O = np.zeros((n, n)); ph = np.linspace(0, np.pi, 181); wp = np.full(181, ph[1] - ph[0]); wp[[0, -1]] *= 0.5
    for j in range(n):
        Rp = np.sqrt(RF[j] ** 2 + d ** 2 + 2 * RF[j] * d * np.cos(ph)); i, t = interp_rows(np.log(Rp), np.log(RF))
        np.add.at(O[j], i, wp * (1 - t) / np.pi); np.add.at(O[j], i + 1, wp * t / np.pi)
    return O
def centre_matrix(RF):
    B = np.zeros((len(RCB), len(RF))); i, t = interp_rows(np.log(RCB), np.log(RF)); B[np.arange(len(RCB)), i] = 1 - t; B[np.arange(len(RCB)), i + 1] = t; return B
def annulus_matrix(RF, nsub=400):
    A = np.zeros((len(RCB), len(RF)))
    for j in range(len(RCB)):
        Rs = np.logspace(np.log10(EDGES[j]), np.log10(EDGES[j + 1]), nsub); w = np.r_[0.5 * (Rs[1] - Rs[0]), 0.5 * (Rs[2:] - Rs[:-2]), 0.5 * (Rs[-1] - Rs[-2])] * Rs
        w = w / ((EDGES[j + 1] ** 2 - EDGES[j] ** 2) / 2); i, t = interp_rows(np.log(Rs), np.log(RF))
        np.add.at(A[j], i, w * (1 - t)); np.add.at(A[j], i + 1, w * t)
    return A
DM1, DM3 = dsig_matrix(RF1), dsig_matrix(RF3); BC1, AN3 = centre_matrix(RF1), annulus_matrix(RF3)
def build_T(hk, nodes, which=("P1", "P3")):
    """per-cluster operators (N, 8, nodes): column 0 central point mass (no Sigma at R > 0, F1 convention), column k the
    cell (k-1, k); entries in (M_sun/pc^2) per M_sun, float32."""
    r = nodes * MPC; ra, rb = r[:-1], r[1:]; out = {}
    for w in which:
        RF, Dm, Bm = (RF1, DM1, BC1) if w == "P1" else (RF3, DM3, AN3)
        BD = Bm @ Dm; Mi = np.stack([BD @ offset_matrix(RF, GAS[hk]["mis"][i]) for i in range(N)]).reshape(N * 8, len(RF)) * (MSUN / KG_PC2)
        T = np.zeros((N, 8, len(r)), np.float32)
        for c0 in range(0, len(ra), 1500):
            Sc = shell_sigma_kernel(ra[c0:c0 + 1500], rb[c0:c0 + 1500], RF * MPC)
            T[:, :, 1 + c0:1 + c0 + Sc.shape[1]] = (Mi @ Sc).reshape(N, 8, Sc.shape[1]).astype(np.float32); del Sc
        out[w] = T; del Mi; relieve()
    return out

# ================================================================ statistics (F1 / H2 A1)
def A_band(D, P, W, sel): return {b: float((W[sel][:, j] * D[sel][:, j]).sum() / (W[sel][:, j] * P[sel][:, j]).sum()) for b, j in BANDS.items()}
def jk(D, P, W):
    full = A_band(D, P, W, np.ones(N, bool)); reps = [A_band(D, P, W, PATCH != p) for p in range(30)]
    return {b: (full[b], float(np.sqrt(29 / 30 * np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps])) ** 2)))) for b in full}
def A_cell(hk, Pp, boost=True):
    d = DAT[hk]; return jk(d["D"] * (d["B"][None, :] if boost else 1.0), Pp, d["W"])
PB = [3, 4, 5, 6, 7]; HARTLAP = (30 - len(PB) - 2) / 29
def chi2_prof(hk, Pp, boost=True):
    d = DAT[hk]; Dd = d["D"] * (d["B"][None, :] if boost else 1.0); W = d["W"]
    f = lambda sel: (W[sel][:, PB] * (Dd[sel][:, PB] - Pp[sel][:, PB])).sum(0) / W[sel][:, PB].sum(0)
    s0 = f(np.ones(N, bool)); reps = np.array([f(PATCH != p) for p in range(30)]); Cv = 29 / 30 * (reps - reps.mean(0)).T @ (reps - reps.mean(0))
    return float(HARTLAP * s0 @ np.linalg.solve(Cv, s0))
def stack_ratio(hk, Pp, Pl): W = DAT[hk]["W"]; return [float((W[:, j] * Pp[:, j]).sum() / (W[:, j] * Pl[:, j]).sum()) for j in range(8)]
def band_ratio(hk, Pp, Pl, js): W = DAT[hk]["W"]; return float(sum((W[:, j] * Pp[:, j]).sum() for j in js) / sum((W[:, j] * Pl[:, j]).sum() for j in js))
def cell_stats(hk, Pp, Pl):
    a = A_cell(hk, Pp); ac = A_cell(hk, Pp, boost=False)
    zm, zo = (a["MID"][0] - 1) / a["MID"][1], (a["OUTER"][0] - 1) / a["OUTER"][1]
    c2 = chi2_prof(hk, Pp)
    return dict(A=a, A_clip=ac, Z_MID=zm, Z_OUT=zo, chi2_prof=c2, ratio=stack_ratio(hk, Pp, Pl), R_MID=band_ratio(hk, Pp, Pl, [3, 4, 5]),
                R_03_1=band_ratio(hk, Pp, Pl, [2, 3, 4]), R_gt1=band_ratio(hk, Pp, Pl, [5, 6, 7]),
                passes=bool(abs(zm) <= 2 and abs(zo) <= 2 and c2 <= 11.07))

# ================================================================ K5: projectors on a Plummer sphere (no miscentring)
Mp, ap = 1e14 * MSUN, 0.2
def ds_pl(R): return Mp * (R * MPC) ** 2 / (np.pi * ((ap * MPC) ** 2 + (R * MPC) ** 2) ** 2) / KG_PC2
ann_pl = np.array([quad(lambda R: ds_pl(R) * R, EDGES[j], EDGES[j + 1], epsabs=0, epsrel=1e-11)[0] / ((EDGES[j + 1] ** 2 - EDGES[j] ** 2) / 2) for j in range(8)])
MLpl = Mp * PNODES ** 3 / (PNODES ** 2 + ap ** 2) ** 1.5; dMpl = np.r_[MLpl[0], np.diff(MLpl)]
ra_, rb_ = PNODES[:-1] * MPC, PNODES[1:] * MPC
p1 = np.zeros(8); p3 = np.zeros(8)
for c0 in range(0, len(ra_), 1500):
    sl = slice(c0, c0 + 1500); dm = dMpl[1 + c0:1 + c0 + len(ra_[sl])]
    p1 += BC1 @ DM1 @ (shell_sigma_kernel(ra_[sl], rb_[sl], RF1 * MPC) @ dm); p3 += AN3 @ DM3 @ (shell_sigma_kernel(ra_[sl], rb_[sl], RF3 * MPC) @ dm)
p1 /= KG_PC2; p3 /= KG_PC2
acc = AnnulusAcc(EDGES[:-1], EDGES[1:]); acc(0, PNODES, MLpl[:, None], None, None, None); p2 = acc.out[0] / KG_PC2
k5 = dict(P1=float(np.max(np.abs(p1 / ds_pl(RCB) - 1))), P3=float(np.max(np.abs(p3 / ann_pl - 1))), P2=float(np.max(np.abs(p2 / ann_pl - 1))))
K5_FROZEN = max(k5.values()) <= 2e-3
say(f"K5-frozen {'PASS' if K5_FROZEN else 'FAIL'} Plummer: P1 point {k5['P1']:.1e}, P3 annulus {k5['P3']:.1e}, P2 annulus {k5['P2']:.1e} <= 2e-3 (all three; frozen line, reported)")
check("K5", k5["P1"] <= 1e-2 and k5["P2"] <= 2e-3 and k5["P3"] <= 2e-3, f"Plummer: P1 point {k5['P1']:.1e} (F1 convention), P3 annulus {k5['P3']:.1e}, P2 annulus {k5['P2']:.1e}", "A1: P1 <= 1e-2, P2/P3 <= 2e-3 (bins 0-7)")
RES["K5"] = k5; relieve(); stamp("K5 done")

# ================================================================ the cluster scan (allowed mu_K; P1 + P3)
F1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json")))
H2J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "H2_aest_clusters", "h2_aest_clusters_results.json")))
DIAG_R = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
SCAN = {}; LAW = {}; PROF = {}; NEGF = {}
iMED = {hk: int(np.argsort(GAS[hk]["Mtot"])[N // 2]) for hk in HS}
def nsub_cluster(nodes, mu, half=False):
    if mu == 0: return nsub_for(nodes, 2e-3 * (0.5 if half else 1.0))
    a, b = dr_ode_cluster(mu, half); return np.where(nodes[1:] <= 6.0 + 1e-9, nsub_for(nodes, a), nsub_for(nodes, b))
def run_cluster_cell(hk, f, mu_Mpc, Dl, nodes, T, diag=False, half=False):
    a0 = A0[f]; Mfn = Mb_cluster(hk); ns = nsub_cluster(nodes, mu_Mpc, half)
    psi0 = np.zeros((len(Dl), N)) if mu_Mpc == 0 else zero_point(nodes, ns, Mfn, GAS[hk]["Mtot"], a0, mu_Mpc, Dl, key=(hk, f, half, mu_Mpc))
    mu2 = (mu_Mpc / MPC) ** 2; D0 = -(SGN * mu2 / G) * psi0 * (nodes[0] * MPC) ** 3 / 3.0
    pj = ProjT(T); cons = [pj]; dg = None
    if diag: dg = Diag(nodes, DIAG_R, mu2, OMK * RHOC0 * (1 + ZC) ** 3, 0.15, 3.0); cons.append(dg)
    integrate(nodes, ns, Mfn, psi0, D0, mu2, a0, cons, chunk=125)
    out = dict(pj.out); del pj; relieve()
    return out, dg

TT = {}; LAWF = {}
for hk in HS:
  for gname, gnodes, mus in (("coarse", PNODES, [m for m in MU_OK if m <= 2.0]), ("fine", PNODES_F, [m for m in MU_OK if m > 2.0])):
    if not mus and gname == "fine": continue
    TT.clear(); relieve(); TT.update(build_T(hk, gnodes, which=("P1", "P3") if gname == "coarse" else ("P3",))); stamp(f"operators {hk} built ({gname}: {len(gnodes)} projection nodes)")
    LREF = LAW if gname == "coarse" else LAWF
    for f in FOOTS:
        pr, _ = run_cluster_cell(hk, f, 0.0, [0.0], gnodes, TT); LREF[(hk, f)] = {w: pr[w][0] for w in pr}
    for mu_Mpc in mus:
        for f in FOOTS:
            t1 = time.time(); pr, dg = run_cluster_cell(hk, f, mu_Mpc, DEL, gnodes, TT, diag=True)
            rows = [dict(Delta=float(dl), P3=cell_stats(hk, pr["P3"][k], LREF[(hk, f)]["P3"]), P1=(cell_stats(hk, pr["P1"][k], LREF[(hk, f)]["P1"]) if "P1" in pr else None)) for k, dl in enumerate(DEL)]
            SCAN[(mu_Mpc, hk, f)] = rows
            fn = dg.frac_neg(); NEGF[(mu_Mpc, hk, f)] = dict(median_Delta0=float(np.nanmedian(fn[I0])), max_Delta0=float(np.nanmax(fn[I0])))
            im = iMED[hk]; zmed = lambda a: float(np.median(np.where(np.isnan(a[I0]), np.inf, a[I0])))
            prof = {}
            for R, v in dg.vals.items():
                Mb_ = v["Mb"][I0]; MK_ = v["MK"][I0]; ML_ = v["ML"][I0]; psi_ = v["psi"][I0]
                MLl = g_aqual(G * Mb_ / (v["r"] * MPC) ** 2, A0[f]) * (v["r"] * MPC) ** 2 / G
                drho = -SGN * (mu_Mpc / MPC) ** 2 * psi_ / (4 * np.pi * G); rb_ = rho_b_cluster(hk, v["r"])
                prof[str(R)] = dict(r=v["r"], MK_over_Mb_median_cluster=float(MK_[im] / Mb_[im]), ML_v3_over_law_median_cluster=float(ML_[im] / MLl[im]),
                                    drhoK_over_rhob_median_cluster=(float(drho[im] / rb_[im]) if rb_[im] > 0 else None),
                                    drhoK_over_rhobarK_median_cluster=float(drho[im] / (OMK * RHOC0 * (1 + ZC[im]) ** 3)),
                                    MK_over_Mb_median_over_clusters=float(np.median(MK_ / Mb_)), ML_ratio_median_over_clusters=float(np.median(ML_ / MLl)))
            PROF[(mu_Mpc, hk, f)] = dict(profile=prof, first_zero_psi_Mpc_median=zmed(dg.z["psi"]), first_zero_MK_Mpc_median=zmed(dg.z["MK"]),
                                         first_zero_ML_Mpc_median=zmed(dg.z["ML"]), frac_clusters_psi_zero_le_3Mpc=float(np.mean(dg.z["psi"][I0] <= 3.0)),
                                         frac_clusters_ML_zero_le_3Mpc=float(np.mean(dg.z["ML"][I0] <= 3.0)))
            r0 = rows[I0]["P3"]
            say(f"mu_K {mu_Mpc:7.4f} {hk} {f:9s} | Delta=0 (P3): MID {r0['A']['MID'][0]:.3f}+-{r0['A']['MID'][1]:.3f} (Z {r0['Z_MID']:+.1f}) "
                f"OUT {r0['A']['OUTER'][0]:.3f}+-{r0['A']['OUTER'][1]:.3f} (Z {r0['Z_OUT']:+.1f}) chi2 {r0['chi2_prof']:.1f} | v3/law "
                + " ".join(f"{x:.2f}" for x in r0["ratio"]) + f" | min chi2 over Delta {min(r['P3']['chi2_prof'] for r in rows):.1f}"
                + f" | passing Delta {[r['Delta'] for r in rows if r['P3']['passes']] or 'none'} | {time.time() - t1:.0f} s")
            del pr, dg; relieve()
    stamp(f"{hk} {gname} scan done")
TT.clear(); relieve()
dev1 = []
for hk in HS:
    for f in FOOTS:
        a = A_cell(hk, LAW[(hk, f)]["P1"]); ref = F1J["rows"][f"PRIMARY {hk}"][f]; a3 = A_cell(hk, LAW[(hk, f)]["P3"])
        dev1 += [abs(a["MID"][0] - ref["MID"][0]), abs(a["OUTER"][0] - ref["OUTER"][0])]
        c1, c3 = chi2_prof(hk, LAW[(hk, f)]["P1"]), chi2_prof(hk, LAW[(hk, f)]["P3"])
        say(f"  law {hk} {f:9s}: P1 MID {a['MID'][0]:.4f} (F1 {ref['MID'][0]:.4f}) OUTER {a['OUTER'][0]:.4f} (F1 {ref['OUTER'][0]:.4f}); "
            f"P3 MID {a3['MID'][0]:.4f}+-{a3['MID'][1]:.4f} OUTER {a3['OUTER'][0]:.4f}+-{a3['OUTER'][1]:.4f}; profile chi2 P1 {c1:.1f} P3 {c3:.1f}")
        RES.setdefault("law", {})[f"{hk}|{f}"] = dict(P1=a, P3=a3, P3_clip=A_cell(hk, LAW[(hk, f)]["P3"], boost=False), chi2_P1=c1, chi2_P3=c3)
for hk in HS:
    for f in FOOTS:
        if (hk, f) in LAWF: RES.setdefault("law_fine_grid", {})[f"{hk}|{f}"] = dict(P3=A_cell(hk, LAWF[(hk, f)]["P3"]), P3_over_coarse=stack_ratio(hk, LAWF[(hk, f)]["P3"], LAW[(hk, f)]["P3"]))
check("K1", max(dev1) <= 0.01, f"max |A - A_F1| (P1, mu_K = 0) over MID/OUTER x 4 cells = {max(dev1):.4f}", "<= 0.01")
dev2 = {}
for mu_Mpc in (0.1, 0.3, 0.5, 0.7, 1.0):
    if mu_Mpc not in MU_OK: continue
    for hk in HS:
        for f in FOOTS:
            h2r = [r for r in H2J["scan"][f"{mu_Mpc}|{hk}|{f}"] if r["Delta"] == 0.0][0]["boost_vs_law"]
            dev2[f"{mu_Mpc}|{hk}|{f}"] = float(np.max(np.abs(np.array(SCAN[(mu_Mpc, hk, f)][I0]["P1"]["ratio"]) - np.array(h2r))))
d2 = max(dev2.values()) if dev2 else float("nan")
check("K2", bool(dev2) and d2 <= 0.02, f"max |R_j(mine, P1) - H2 boost_vs_law| over mu 0.1-1.0, 8 bins, 4 cells = {d2:.4f} (worst {max(dev2, key=dev2.get) if dev2 else None})", "<= 0.02")
RES["K2_dev"] = dev2
stamp("K1/K2 done")

# ================================================================ growth mu_K (P2 only; Delta set on h 0.672, Delta = 0 on h 0.686)
GROW = {}; GLAW = {}
def run_growth(mu_Mpc, Dl, cells, half=False):
    nodes, ns = grid_growth(mu_Mpc if mu_Mpc > 0 else 243.78, half=half)
    Mfns = [Mb_cluster(hk) for hk, f in cells]; nc = len(cells)
    a0v = np.concatenate([np.full(N, A0[f]) for hk, f in cells])[None, :]
    Mfn = lambda r: np.concatenate([m(r) for m in Mfns])[None, :]
    Mtot = np.concatenate([GAS[hk]["Mtot"] for hk, f in cells])
    psi0 = np.zeros((len(Dl), nc * N)) if mu_Mpc == 0 else zero_point(nodes, ns, Mfn, Mtot, a0v, mu_Mpc, Dl, key=("grow", tuple(cells), half, mu_Mpc))
    mu2 = (mu_Mpc / MPC) ** 2; D0 = -(SGN * mu2 / G) * psi0 * (nodes[0] * MPC) ** 3 / 3.0
    acc = AnnulusAcc(EDGES[:-1], EDGES[1:]); cons = [acc]
    dg = Diag(nodes, DIAG_R, mu2, np.tile(OMK * RHOC0 * (1 + ZC) ** 3, nc)[None, :], 0.15, 3.0) if mu_Mpc > 0 else None
    if dg is not None: cons.append(dg)
    integrate(nodes, ns, Mfn, psi0, D0, mu2, a0v, cons, chunk=400)
    P = acc.out / KG_PC2
    return {c: P[:, i * N:(i + 1) * N, :] for i, c in enumerate(cells)}, dg, len(nodes)
CA = [c for c in CELLS if c[0] == "h0672"]; CB = [c for c in CELLS if c[0] == "h0686"]
pr, _, nn = run_growth(0.0, [0.0], CELLS)
for c in CELLS: GLAW[c] = pr[c][0]
stamp(f"growth-grid law (P2) done ({nn} nodes)")
for c in CELLS:
    RES.setdefault("law_P2", {})[f"{c[0]}|{c[1]}"] = dict(A=A_cell(c[0], GLAW[c]), chi2=chi2_prof(c[0], GLAW[c]))
for mu_Mpc in MU_GROW:
    t1 = time.time()
    for cells, Dl, i0 in ((CA, DEL_G, I0G), (CB, np.array([0.0]), 0)):
        pr, dg, nn = run_growth(mu_Mpc, Dl, cells)
        for ci, (hk, f) in enumerate(cells):
            rows = [dict(Delta=float(dl), P2=cell_stats(hk, pr[(hk, f)][k], GLAW[(hk, f)])) for k, dl in enumerate(Dl)]
            GROW[(mu_Mpc, hk, f)] = rows
            fn = dg.frac_neg()[:, ci * N:(ci + 1) * N]
            NEGF[(mu_Mpc, hk, f)] = dict(median_Delta0=float(np.nanmedian(fn[i0])), max_Delta0=float(np.nanmax(fn[i0])))
            r0 = rows[i0]["P2"]
            say(f"mu_K {mu_Mpc:7.2f} [EXCLUDED, growth] {hk} {f:9s} | Delta=0 (P2): MID {r0['A']['MID'][0]:.3g}+-{r0['A']['MID'][1]:.2g} OUT {r0['A']['OUTER'][0]:.3g}+-{r0['A']['OUTER'][1]:.2g} "
                f"chi2 {r0['chi2_prof']:.1f} | v3/law " + " ".join(f"{x:.3f}" for x in r0["ratio"]) + f" | neg-dust volume fraction (median) {NEGF[(mu_Mpc, hk, f)]['median_Delta0']:.2f}"
                + f" | min chi2 over Delta {min(r['P2']['chi2_prof'] for r in rows):.1f}")
        del pr, dg; relieve()
    stamp(f"growth mu {mu_Mpc} done ({nn} nodes, {time.time() - t1:.0f} s)")

# ================================================================ K7 convergence (clusters) + r_max sensitivity (reported)
hk7, f7 = "h0672", "canonical"
base10 = SCAN[(10.0, hk7, f7)][I0]["P3"]["ratio"]
PH = proj_grid(1e-3, 0.000875, 2.5e-4)
TT.update(build_T(hk7, PH, which=("P3",)))
prl, _ = run_cluster_cell(hk7, f7, 0.0, [0.0], PH, TT, half=True); pr10, _ = run_cluster_cell(hk7, f7, 10.0, [0.0], PH, TT, half=True)
half10 = stack_ratio(hk7, pr10["P3"][0], prl["P3"][0]); TT.clear(); relieve()
e7a = float(np.max(np.abs(np.array(half10) - np.array(base10))))
mug = MU_GROW[-1]
prG, _, _ = run_growth(mug, [0.0], [(hk7, f7)], half=True); prG0, _, _ = run_growth(0.0, [0.0], [(hk7, f7)], half=True)
halfG = stack_ratio(hk7, prG[(hk7, f7)][0], prG0[(hk7, f7)][0]); baseG = GROW[(mug, hk7, f7)][I0G]["P2"]["ratio"]
e7b = float(np.max(np.abs(np.array(halfG) - np.array(baseG))))
RES["K7_detail"] = dict(cluster_mu10_full=base10, cluster_mu10_half=half10, cluster_growth_full=baseG, cluster_growth_half=halfG)
say(f"  K7 detail: mu 10 ratios full " + " ".join(f"{x:.4f}" for x in base10) + " | half " + " ".join(f"{x:.4f}" for x in half10))
say(f"  K7 detail: mu {mug} ratios full " + " ".join(f"{x:.4f}" for x in baseG) + " | half " + " ".join(f"{x:.4f}" for x in halfG))
stamp("K7 cluster halving done")
RMAX_SENS = {}
for mu_Mpc in (0.1, 1.0):
    if mu_Mpc not in MU_OK: continue
    n60 = proj_grid(1e-3, 0.0035, 2e-3, rmax=60.0)
    TT.update(build_T(hk7, n60, which=("P3",)))
    l60, _ = run_cluster_cell(hk7, f7, 0.0, [0.0], n60, TT); m60, _ = run_cluster_cell(hk7, f7, mu_Mpc, [0.0], n60, TT)
    RMAX_SENS[str(mu_Mpc)] = dict(ratio_rmax60=stack_ratio(hk7, m60["P3"][0], l60["P3"][0]), ratio_rmax30=SCAN[(mu_Mpc, hk7, f7)][I0]["P3"]["ratio"],
                                  A_rmax60=A_cell(hk7, m60["P3"][0]))
    TT.clear(); relieve()
    say(f"  r_max 30 -> 60 Mpc at mu_K {mu_Mpc}: v3/law " + " ".join(f"{x:.3f}" for x in RMAX_SENS[str(mu_Mpc)]["ratio_rmax30"]) + " -> "
        + " ".join(f"{x:.3f}" for x in RMAX_SENS[str(mu_Mpc)]["ratio_rmax60"]))
RES["rmax_sensitivity"] = RMAX_SENS
stamp("r_max sensitivity done")

# ================================================================ F2 Track A (isolated lenses)
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing"))
import f2_aqual as AQ                                                    # read-only import (EFE solver, F2 projector)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar"); B21 = os.path.join(DATA, "brouwer2021_rar")
Rl, Yl = [], []
for b in range(1, 5):
    d = np.loadtxt(os.path.join(B21, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")); Rl.append(d[:, 0]); Yl.append(d[:, 1] / d[:, 4])
RB21, YB21 = np.array(Rl), np.array(Yl)
cc = np.loadtxt(os.path.join(B21, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt")); mins = sorted(set(cc[:, 0])); CB21 = np.zeros((60, 60))
for row in cc:
    m, n_ = mins.index(row[0]), mins.index(row[1]); i, j = int(np.argmin(abs(RB21[0] - row[2]))), int(np.argmin(abs(RB21[0] - row[3]))); CB21[m * 15 + i, n_ * 15 + j] = row[4] / row[6]
RBL = RB21[0].copy(); IDX_ALL = list(range(15)); IDX_IN = [i for i in range(15) if RBL[i] <= 0.31]
IDX_O1 = [i for i in range(15) if 0.4 < RBL[i] < 1.1]; IDX_O2 = [i for i in range(15) if RBL[i] > 1.1]; IDX_OUT = IDX_O1 + IDX_O2
IDX_GUARD = [i for i in range(15) if RBL[i] <= 1.1]
def sel_of(idx): return np.concatenate([np.array(idx) + 15 * b for b in range(4)])
def chi2_vec(y, m, idx, Cm):
    s = sel_of(idx); r = (y.ravel() - m.ravel())[s]; return float(r @ np.linalg.solve(Cm[np.ix_(s, s)], r))
def gls_amp(y, m, idx, Cm):
    s = sel_of(idx); Cs = Cm[np.ix_(s, s)]; mm = m.ravel()[s]; yy = y.ravel()[s]; Ci_m = np.linalg.solve(Cs, mm); F = float(mm @ Ci_m); return float(yy @ Ci_m) / F, 1 / math.sqrt(F)
def amps(y, m, Cm):
    o = {}
    for lab, idx in (("in", IDX_IN), ("O1", IDX_O1), ("O2", IDX_O2), ("out", IDX_OUT)):
        a, s = gls_amp(y, m, idx, Cm); o[f"A_{lab}"] = a; o[f"sA_{lab}"] = s
    o["chi2_all"] = chi2_vec(y, m, IDX_ALL, Cm); return o
def chi_flat(z, om):
    zz = np.linspace(0, 1.0, 4001); E = np.sqrt(om * (1 + zz) ** 3 + 1 - om)
    ch = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]); return np.interp(z, zz, ch)
LN = np.load(os.path.join(DATA, "lr_lenses.npz")); PLN = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WLENS = PLN["WW"].sum(axis=1); logMs70 = LN["logM"]; zl = LN["z"]
LBIN = np.digitize(logMs70, [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
OM_NAT, H2NAT, T_OM_A = 0.3085, 0.679, 1.0128
qDA = chi_flat(zl, OM_NAT) / chi_flat(zl, 0.3)
INV = {}
for b in range(4):
    m = LBIN == b; w = WLENS[m]
    INV[b] = dict(w=w, logMs70=logMs70[m], qDA=qDA[m], zeff=float(np.sum(w * zl[m]) / np.sum(w)), meanlogMs=float(np.sum(w * logMs70[m]) / np.sum(w)))
Rn = np.array([RB21[b] * (0.70 / H2NAT) * float(chi_flat(INV[b]["zeff"], OM_NAT) / chi_flat(INV[b]["zeff"], 0.2793)) for b in range(4)])
fdat = (H2NAT / 0.70) * T_OM_A; Yn = YB21 * fdat; Cn = CB21 * fdat * fdat
F2J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing", "f2_outer_lensing_results.json")))
Gpc = 4.30091e-3
def a0u(foot): return A0[foot] * 3.0857e16 / 1e6
YE = {f: 10 ** -3.215 * 1.2e-10 / A0[f] for f in FOOTS}
SOL = {f: AQ.solve_efe(YE[f]) for f in FOOTS}
LMG = np.round(np.arange(6.8, 11.81, 0.02), 2); RGRID_PC = np.logspace(1.0, 10.0, 3601)
def lmc_of(lm): lm70 = lm - 2 * np.log10(0.70 / H2NAT); return lm + (-0.69 * lm70 + 6.63)
def f2_meff(foot, lm, ye):                     # F2's meff_profile, central configuration (f_hot 0.5)
    a0 = a0u(foot); Ms = 10 ** lm; Mpt = Ms + 10 ** lmc_of(lm); Mhot = 0.5 * Ms
    Mb = Mpt + Mhot * np.minimum(1.0, (RGRID_PC / 1e5) ** 3); Miso = Mb * AQ.nu_simple(Gpc * Mb / RGRID_PC ** 2 / a0)
    if ye == "zero": return Miso, "linear"
    s = SOL[foot]; rM = math.sqrt(Gpc * (Mpt + Mhot) / a0); sg = RGRID_PC / rM
    Me = np.interp(np.log(sg), np.log(s["r"]), s["M"], left=np.nan, right=s["M_far"]); Cr = np.where(np.isnan(Me), 1.0, Me / AQ.M_iso(sg))
    return Miso * Cr, "const"
def stack_from_table(tab_fn, grid):
    out = np.empty((4, 15))
    for b in range(4):
        lMs_nat = INV[b]["logMs70"] + 2 * np.log10(0.70 / H2NAT) + 2 * np.log10(INV[b]["qDA"]); tab = tab_fn(b); w = INV[b]["w"]
        vals = np.array([np.interp(lMs_nat, grid, tab[:, i]) for i in range(15)]); out[b] = vals @ w / w.sum()
    return out
dA6, dC6 = [], []
for f in FOOTS:
    for ye, lab in (("zero", "OAT EFE y_e = 0"), ("noclu", "L5_plus_EFE_noclu=T_central")):
        tabs = {lm: f2_meff(f, lm, ye) for lm in LMG}
        m = stack_from_table(lambda b: np.array([AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, *tabs[lm]) for lm in LMG]), LMG)
        o = amps(Yn, m, Cn); ref = F2J["trackA"][f][lab]
        dA6 += [abs(o[k] - ref[k]) for k in ("A_in", "A_O1", "A_O2")]; dC6.append(abs(o["chi2_all"] - ref["chi2_all"]))
        say(f"  F2 reproduction [{f} {ye}]: chi2_all {o['chi2_all']:.2f} (F2 {ref['chi2_all']:.2f}) A_in {o['A_in']:.4f} ({ref['A_in']:.4f}) "
            f"A_O1 {o['A_O1']:.4f} ({ref['A_O1']:.4f}) A_O2 {o['A_O2']:.4f} ({ref['A_O2']:.4f})")
        RES.setdefault("F2_reproduction", {})[f"{f}|{ye}"] = o
check("K6", max(dA6) <= 0.005 and max(dC6) <= 0.5, f"max |dA| {max(dA6):.4f}; max |dchi2_all| {max(dC6):.3f} (rows y_e=0 and T_central, both footings)", "|dA| <= 0.005, |dchi2| <= 0.5")
stamp("F2 reproduction done")

# ---- v3 galaxy solves (annulus averages over B21 bins, r_max 30 Mpc, const beyond)
LMS = np.round(np.arange(8.30, 11.301, 0.02), 2)
EB = []
for b in range(4):
    lr_ = np.log(Rn[b]); mid = 0.5 * (lr_[1:] + lr_[:-1]); EB.append(np.exp(np.r_[lr_[0] - (mid[0] - lr_[0]), mid, lr_[-1] + (lr_[-1] - mid[-1])]))
EB = np.array(EB); E1G = EB[:, :-1].ravel(); E2G = EB[:, 1:].ravel()                         # 60 annuli (Mpc)
MSG = 10 ** LMS * MSUN; MCOLD = 10 ** np.array([lmc_of(lm) for lm in LMS]) * MSUN; MPT = MSG + MCOLD; MHOT = 0.5 * MSG; MGT = MPT + MHOT
def Mb_gal(r): return MPT + MHOT * min(1.0, (r / 0.1) ** 3)
def grid_gal(mu_Mpc, half=False):
    f = 0.5 if half else 1.0
    dr = (2.5e-4 if mu_Mpc <= 1.0 else 1.25e-4 if mu_Mpc <= 3.4 else 6.25e-5) if mu_Mpc <= 10.0 else (2 * np.pi / mu_Mpc) / 200
    nodes = proj_grid(1e-5, 0.0035 * f, dr * f, r_fine=RMAX, rmax=RMAX); return nodes, np.ones(len(nodes) - 1, int)
def efe_factor(foot):
    s = SOL[foot]; rM = np.sqrt(G * MGT / A0[foot]) / MPC
    def fac(rn):
        sg = rn[:, None] / rM[None, :]; Me = np.interp(np.log(sg), np.log(s["r"]), s["M"], left=np.nan, right=s["M_far"])
        return np.where(np.isnan(Me), 1.0, Me / AQ.M_iso(sg))[:, None, :]
    return fac
GZ = 0.2
def run_gal(foot, mu_Mpc, Dl, half=False, efe=True, diag=False):
    nodes, ns = grid_gal(mu_Mpc, half); a0 = A0[foot]
    psi0 = np.zeros((len(Dl), len(LMS))) if mu_Mpc == 0 else zero_point(nodes, ns, Mb_gal, MGT, a0, mu_Mpc, Dl, key=("gal", foot, half, mu_Mpc))
    mu2 = (mu_Mpc / MPC) ** 2; D0 = (SGN * mu2) * MPT[None, :] * (nodes[0] * MPC) ** 2 / 2.0 * np.ones((len(Dl), 1))     # point-mass series start
    acc0 = AnnulusAcc(E1G, E2G); cons = [acc0]; acc1 = None
    if efe: acc1 = AnnulusAcc(E1G, E2G, mfac=efe_factor(foot)); cons.append(acc1)
    dg = None
    if diag:
        dg = Diag(nodes, [0.035, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.6], mu2, np.full(len(LMS), OMK * RHOC0 * (1 + GZ) ** 3)[None, :], 0.035, 2.6)
        cons.append(dg)
    integrate(nodes, ns, Mb_gal, psi0, D0, mu2, a0, cons, chunk=2000)
    t0 = (acc0.out / KG_PC2).reshape(len(Dl), len(LMS), 4, 15); t1 = (acc1.out / KG_PC2).reshape(len(Dl), len(LMS), 4, 15) if efe else None
    return t0, t1, dg, len(nodes)
def gal_stack(t): return stack_from_table(lambda b: t[:, b, :], LMS)
GAL = {}; GLAWS = {}; GPROF = {}
for f in FOOTS:
    t0, t1, _, nn = run_gal(f, 0.0, [0.0]); GLAWS[f] = dict(zero=gal_stack(t0[0]), noclu=gal_stack(t1[0]))
    for ye in ("zero", "noclu"):
        o = amps(Yn, GLAWS[f][ye], Cn); RES.setdefault("F2_law_annulus", {})[f"{f}|{ye}"] = o
        say(f"  galaxy law (annulus, r_max 30) [{f} {ye}]: chi2_all {o['chi2_all']:.1f} A_in {o['A_in']:.3f} A_O1 {o['A_O1']:.3f} A_O2 {o['A_O2']:.3f}")
stamp(f"galaxy law done ({nn} nodes)")
iBIN = [int(np.argmin(np.abs(LMS - (INV[b]["meanlogMs"] + 2 * np.log10(0.70 / H2NAT))))) for b in range(4)]
def gal_entry(f, ratio): return dict(ratio=ratio.tolist(), guard=bool(np.all(np.abs(ratio[:, IDX_GUARD] - 1) <= 0.14)), shape_gal=bool(np.all(np.abs(ratio - 1) <= 0.10)),
                                     maxdev_guard=float(np.max(np.abs(ratio[:, IDX_GUARD] - 1))), maxdev_all=float(np.max(np.abs(ratio - 1))))
for mu_Mpc in MU_OK + MU_GROW:
    for f in FOOTS:
        t1s = time.time(); t0, t1, dg, nn = run_gal(f, mu_Mpc, [0.0], diag=True)
        m0, m1 = gal_stack(t0[0]), gal_stack(t1[0]); ratio = m0 / GLAWS[f]["zero"]
        o0, o1 = amps(Yn, m0, Cn), amps(Yn, m1, Cn)
        e = gal_entry(f, ratio); e.update(zero=o0, noclu_approx=o1, dchi2_zero_vs_law=o0["chi2_all"] - RES["F2_law_annulus"][f"{f}|zero"]["chi2_all"],
                                          dchi2_noclu_vs_law=o1["chi2_all"] - RES["F2_law_annulus"][f"{f}|noclu"]["chi2_all"])
        GAL[(mu_Mpc, f, 0.0)] = e
        fn = dg.frac_neg()[0]; prof = {}
        for R, v in dg.vals.items():
            Mb_ = v["Mb"][0][iBIN]; MK_ = v["MK"][0][iBIN]; ML_ = v["ML"][0][iBIN]
            MLl = g_aqual(G * Mb_ / (v["r"] * MPC) ** 2, A0[f]) * (v["r"] * MPC) ** 2 / G
            drho = -SGN * (mu_Mpc / MPC) ** 2 * v["psi"][0][iBIN] / (4 * np.pi * G)
            prof[str(R)] = dict(r=v["r"], MK_over_Mb=(MK_ / Mb_).tolist(), ML_v3_over_law=(ML_ / MLl).tolist(), drhoK_over_rhobarK=(drho / (OMK * RHOC0 * (1 + GZ) ** 3)).tolist())
        GPROF[(mu_Mpc, f)] = dict(profile_bins_1to4=prof, first_zero_psi_Mpc=[float(dg.z["psi"][0][i]) for i in iBIN],
                                  first_zero_ML_Mpc=[float(dg.z["ML"][0][i]) for i in iBIN], neg_dust_volume_frac=[float(fn[i]) for i in iBIN])
        say(f"  galaxy mu_K {mu_Mpc:8.4f} [{f:9s}] y_e=0: chi2_all {o0['chi2_all']:.1f} (dchi2 vs law {e['dchi2_zero_vs_law']:+.1f}) A_in {o0['A_in']:.3f} "
            f"A_O1 {o0['A_O1']:.3f}+-{o0['sA_O1']:.3f} A_O2 {o0['A_O2']:.3f}+-{o0['sA_O2']:.3f} | noclu(approx) A_O1 {o1['A_O1']:.3f} A_O2 {o1['A_O2']:.3f} | "
            f"v3/law max|r-1| R<=1.1 {e['maxdev_guard']:.3f}, all R {e['maxdev_all']:.3f} | guard {'OK' if e['guard'] else 'FAIL'} | {nn} nodes {time.time() - t1s:.0f} s")
        del dg; relieve()
    stamp(f"galaxy mu {mu_Mpc} done")
t0h, _, _, _ = run_gal("canonical", 10.0, [0.0], half=True, efe=False); t0l, _, _, _ = run_gal("canonical", 0.0, [0.0], half=True, efe=False)
rh = gal_stack(t0h[0]) / gal_stack(t0l[0]); e7c = float(np.max(np.abs(rh - np.array(GAL[(10.0, "canonical", 0.0)]["ratio"]))))
K7_FROZEN = e7a <= 0.005 and e7b <= 0.01 and e7c <= 0.005
say(f"K7-frozen {'PASS' if K7_FROZEN else 'FAIL'} cluster mu 10 (P3) {e7a:.4f}; cluster mu {mug} (P2) {e7b:.4f}; galaxy mu 10 {e7c:.4f} <= 0.005 / 0.01 / 0.005 (frozen line, reported)")
check("K7", e7a <= 0.005 and e7c <= 0.005, f"cluster mu 10 (P3) {e7a:.4f}; galaxy mu 10 {e7c:.4f} (growth leg reported: {e7b:.4f})", "A1: <= 0.005 / 0.005")
stamp("K7 done")

# ================================================================ guard at the Delta values the rule needs; verdict; shape test
def cells_pass(m, k): return all(SCAN[(m, hk, f)][k]["P3"]["passes"] for hk, f in CELLS)
need = sorted({(m, float(DEL[k])) for m in MU_OK for k in range(len(DEL)) for f in FOOTS if all(SCAN[(m, hk, f)][k]["P3"]["passes"] for hk in HS)})
for (m, dl) in need:
    for f in FOOTS:
        if (m, f, dl) not in GAL:
            t0, _, _, _ = run_gal(f, m, [dl], efe=False); GAL[(m, f, dl)] = gal_entry(f, gal_stack(t0[0]) / GLAWS[f]["zero"])
def guard_ok(m, dl, f): return GAL[(m, f, dl)]["guard"]
ck_ok = all(ok for n, ok in CHECKS if n in ("K1", "K2", "K3", "K4", "K5", "K6", "K7"))
def foot_verdict(f):
    p = lambda m, k: all(SCAN[(m, hk, f)][k]["P3"]["passes"] for hk in HS) and guard_ok(m, float(DEL[k]), f)
    if any(p(m, I0) for m in MU_OK): return "CAN SUPPLY IT"
    if any(p(m, k) for m in MU_OK for k in range(len(DEL))): return "CAN ONLY WITH A FITTED ZERO POINT"
    return "CANNOT"
VF = {f: foot_verdict(f) for f in FOOTS}
RANK = {"CANNOT": 0, "CAN ONLY WITH A FITTED ZERO POINT": 1, "CAN SUPPLY IT": 2}
V_A1 = "UNDECIDED (checks)" if not ck_ok else (min(VF.values(), key=lambda v: RANK[v]) + ("" if len(set(VF.values())) == 1 else f" (footing split: {VF})"))
ck_frozen = ck_ok and K5_FROZEN and K7_FROZEN
V = "UNDECIDED (checks: " + ", ".join(n for n, ok in (("K5-frozen", K5_FROZEN), ("K7-frozen", K7_FROZEN)) if not ok) + ")" if not ck_frozen else V_A1
can0 = [m for m in MU_OK if cells_pass(m, I0) and all(guard_ok(m, 0.0, f) for f in FOOTS)]
knob = [(m, float(DEL[k])) for m in MU_OK for k in range(len(DEL)) if cells_pass(m, k) and all(guard_ok(m, float(DEL[k]), f) for f in FOOTS)]
cluster_only = [(m, float(DEL[k])) for m in MU_OK for k in range(len(DEL)) if cells_pass(m, k)]
single_cells = [(m, hk, f, r["Delta"]) for (m, hk, f), rows in SCAN.items() for r in rows if r["P3"]["passes"]]
say(f"\nall-cell (P3) passes at Delta = 0 with the galaxy guard: {can0}; with a universal Delta: {knob[:12]}; cluster-only all-cell passes: {cluster_only[:12]}; single cells passing: {len(single_cells)} {single_cells[:8]}")
say(f"VERDICT (frozen rule): {V}")
say(f"VERDICT (AMENDMENT A1 gates): {V_A1}   per footing {VF}")
WHY = {}
for (m, hk, f), rows in SCAN.items():
    ok_ = [r for r in rows if abs(r["P3"]["Z_OUT"]) <= 2]; best = min(ok_, key=lambda r: abs(r["P3"]["A"]["MID"][0] - 1)) if ok_ else None
    WHY[f"{m}|{hk}|{f}"] = dict(A_MID_D0=rows[I0]["P3"]["A"]["MID"], A_OUT_D0=rows[I0]["P3"]["A"]["OUTER"], chi2_D0=rows[I0]["P3"]["chi2_prof"],
                                min_chi2=min(r["P3"]["chi2_prof"] for r in rows), min_chi2_Delta=min(rows, key=lambda r: r["P3"]["chi2_prof"])["Delta"],
                                best_A_MID_with_ZOUT_ok=best["P3"]["A"]["MID"][0] if best else None, best_Delta=best["Delta"] if best else None,
                                ratio_D0=rows[I0]["P3"]["ratio"], R_MID_D0=rows[I0]["P3"]["R_MID"], R_03_1_D0=rows[I0]["P3"]["R_03_1"], R_gt1_D0=rows[I0]["P3"]["R_gt1"])
SHAPE = {}
for m in MU_OK:
    for f in FOOTS:
        rows = SCAN[(m, "h0672", f)]
        cand = [r for r in rows if 1.4 <= r["P3"]["R_MID"] <= 1.8]
        best = min(cand, key=lambda r: max(abs(r["P3"]["ratio"][6] - 1), abs(r["P3"]["ratio"][7] - 1))) if cand else None
        if best is not None and (m, f, best["Delta"]) not in GAL:
            t0, _, _, _ = run_gal(f, m, [best["Delta"]], efe=False); GAL[(m, f, best["Delta"])] = gal_entry(f, gal_stack(t0[0]) / GLAWS[f]["zero"])
        def sh(r, dl):
            g = GAL.get((m, f, dl))
            return dict(R_MID=r["R_MID"], R6=r["ratio"][6], R7=r["ratio"][7], R_03_1=r["R_03_1"], R_gt1=r["R_gt1"],
                        cluster_shape=bool(1.4 <= r["R_MID"] <= 1.8 and 0.9 <= r["ratio"][6] <= 1.1 and 0.9 <= r["ratio"][7] <= 1.1),
                        gal_shape=(g["shape_gal"] if g else None), gal_maxdev_all=(g["maxdev_all"] if g else None))
        SHAPE[f"{m}|{f}"] = dict(Delta0=sh(rows[I0]["P3"], 0.0), best_Delta=(best["Delta"] if best else None), best=(sh(best["P3"], best["Delta"]) if best else None))
anyshape = [k for k, v in SHAPE.items() if v["Delta0"]["cluster_shape"] and v["Delta0"]["gal_shape"]]
anyshape_best = [k for k, v in SHAPE.items() if v["best"] and v["best"]["cluster_shape"] and v["best"]["gal_shape"]]
say(f"SHAPE TEST (x1.4-1.8 over MID, 0.9-1.1 in bins 6-7, galaxies within 10%): Delta=0: {anyshape or 'none'}; best Delta: {anyshape_best or 'none'}; "
    f"cluster shape alone at Delta=0: {[k for k, v in SHAPE.items() if v['Delta0']['cluster_shape']] or 'none'}; at best Delta: {[k for k, v in SHAPE.items() if v['best'] and v['best']['cluster_shape']] or 'none'}")
mu_gal = {f: next((m for m in MU_OK if not GAL[(m, f, 0.0)]["guard"]), None) for f in FOOTS}
say(f"mu_K,gal (smallest grid mu_K whose Delta = 0 galaxy guard fails): {mu_gal}")
RES.update(verdict_frozen_rule=V, verdict_A1=V_A1, verdict_per_footing=VF, K5_frozen_pass=K5_FROZEN, K7_frozen_pass=K7_FROZEN, can_Delta0=can0, knob_passes=knob, cluster_only_passes=cluster_only, single_cells_passing=single_cells, why=WHY,
           shape_test=SHAPE, shape_pass_Delta0=anyshape, shape_pass_bestDelta=anyshape_best, mu_K_gal=mu_gal,
           scan={f"{m}|{hk}|{f}": rows for (m, hk, f), rows in SCAN.items()}, growth={f"{m}|{hk}|{f}": rows for (m, hk, f), rows in GROW.items()},
           neg_dust_fraction={f"{m}|{hk}|{f}": v for (m, hk, f), v in NEGF.items()}, cluster_profiles={f"{m}|{hk}|{f}": v for (m, hk, f), v in PROF.items()},
           galaxy={f"{m}|{f}|{dl}": v for (m, f, dl), v in GAL.items()}, galaxy_profiles={f"{m}|{f}": v for (m, f), v in GPROF.items()},
           median_cluster_index=iMED, galaxy_profile_logMs_native=[float(LMS[i]) for i in iBIN], K7=dict(cluster_mu10=e7a, cluster_growth=e7b, galaxy_mu10=e7c))
check("K8", rss_gb() < 1.0, f"peak RSS {rss_gb():.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS)
say(f"S4_V3_MUK_CLUSTERS COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {time.time() - T0:.0f} s")
RES.update(runtime_s=time.time() - T0, peak_rss_GB=rss_gb())
def _js(o):
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, np.bool_): return bool(o)
    return str(o)
json.dump(RES, open(os.path.join(OUTDIR, f"s4_v3_muk_clusters_results{TAG}.json"), "w"), indent=1, default=_js)
sys.exit(0 if npass == len(CHECKS) else 1)
