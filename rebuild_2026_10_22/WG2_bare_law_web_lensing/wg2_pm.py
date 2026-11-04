#!/usr/bin/env python3
"""WG2 engine (FROZEN_CRITERIA.md, 8f484be581): one particle-mesh run of the law alone on the web, from a baryons-only CLASS field.
Adapted from CFG359's PM (campaign_fresh_gravity/CFG359_native_pm_growth/cfg359_pm.py, read only): f_b = 1 (baryons are the only
clustering matter), Milgrom's simple nu replaces nu_mono, no switch, radiation in E(a), ICs from CLASS with omega_cdm ~ 0.
R0 = law OFF (Newton, baryons), R1 = law ON (QUMOND on the peculiar field). a0: TIE (flat) or RIVAL (a0_foot E(z)).
Usage: python3 wg2_pm.py run RULE A0RULE BG AS N NSTEP ZON FOOT   (writes runs/<tag>.json)
       python3 wg2_pm.py checks                                  (K1 growth, K2 QUMOND exactness; writes runs/checks.json)
       WG2_MUTATE=1 halves the Poisson factor (K1 must FAIL); outputs carry _MUTATE.
kappa = 1/2 FITTED; the cold sector stays retired; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy import fft as sfft
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, os.path.join(REPO, "a0kit")); import a0kit                       # read only
MUTATE = os.environ.get("WG2_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""

H = 0.6736; OMB_H2 = 0.02237; OMB = OMB_H2 / H ** 2; OMR = 4.18e-5 / H ** 2; NS = 0.9649; KP = 0.05   # KP in 1/Mpc
OFLD = 0.2504                                      # B2's smooth, unexplained matter term (CLASS fluid, w -0.001, cs2 1)
MPC = 3.0856775814913673e22; C_MS = 299792458.0
ACC_UNIT = 1e10 * H / MPC                          # H0^2 (Mpc/h) in m/s^2
PSI_UNIT = (1e5 / C_MS) ** 2                       # code potential (100 km/s)^2 -> Psi = Phi / c^2
A0 = a0kit.footings()
L = 1600.0; SEED = 2026
PFAC = 0.75 if MUTATE else 1.5
SNAP_Z = [30, 20, 15, 10, 7, 5, 4, 3, 2.5, 2, 1.6, 1.3, 1, 0.8, 0.6, 0.45, 0.3, 0.2, 0.1, 0]

def background(bg):
    """(E(a), Omega of the clustering source)."""
    if bg == "B2": om, ol, orr, ocl = OMB + OFLD, 1 - OMB - OFLD - OMR, OMR, OMB
    elif bg == "B1": om, ol, orr, ocl = OMB, 1 - OMB - OMR, OMR, OMB
    elif bg == "EDS": om, ol, orr, ocl = 1.0, 0.0, 0.0, 1.0                     # K1 only
    else: raise ValueError(bg)
    return (lambda a: math.sqrt(orr / a ** 4 + om / a ** 3 + ol)), ocl

def nu_simple(y):
    y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)

# ---------------------------------------------------------------- mesh (from cfg359_pm.Mesh, L set here)
class Mesh:
    def __init__(self, M):
        self.M = M; self.dx = L / M
        k1 = 2 * np.pi * sfft.fftfreq(M, d=self.dx); kz = 2 * np.pi * sfft.rfftfreq(M, d=self.dx)
        self.kx = k1[:, None, None].astype(np.float32); self.ky = k1[None, :, None].astype(np.float32)
        self.kz = kz[None, None, :].astype(np.float32)
        k2 = self.kx ** 2 + self.ky ** 2 + self.kz ** 2; k2[0, 0, 0] = 1.0
        self.ik2 = (1.0 / k2).astype(np.float32); self.ik2[0, 0, 0] = 0.0
        self.kvec = (self.kx, self.ky, self.kz)
        self.kk = np.sqrt(k2).astype(np.float64); self.kk[0, 0, 0] = 0.0
        W = 1.0
        for kv in self.kvec:
            W = W * np.sinc(kv * self.dx / (2 * np.pi)) ** 2
        self.W2 = (W ** 2).astype(np.float64)
        # Amendment A1 (after K1 failed as frozen, before any production run): deconvolve the CIC window once for the deposit and
        # once for the interpolation, inside the Nyquist sphere; modes outside it are zeroed.
        kny = math.pi / self.dx
        self.DEC = np.where(self.kk <= kny, 1.0 / W, 0.0).astype(np.float32)
    def fwd(self, x): return sfft.rfftn(x, workers=1)
    def inv(self, xk): return sfft.irfftn(xk, s=(self.M,) * 3, workers=1).astype(np.float32)
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
    def pk(self, fk, deconv=True):
        """binned power of a Fourier field (k in h/Mpc, P in (Mpc/h)^3), CIC-deconvolved."""
        M = self.M; p3 = (np.abs(fk) ** 2) * L ** 3 / M ** 6
        if deconv: p3 = p3 / self.W2
        wt = np.full(fk.shape, 2.0); wt[..., 0] = 1.0
        if M % 2 == 0: wt[..., -1] = 1.0
        wt[0, 0, 0] = 0.0
        kf = 2 * np.pi / L; edges = np.arange(0.5, M // 2 + 1, 1.0) * kf
        ib = np.digitize(self.kk.ravel(), edges); wv = wt.ravel()
        nb = np.bincount(ib, weights=wv, minlength=len(edges) + 1)
        sk = np.bincount(ib, weights=wv * self.kk.ravel(), minlength=len(edges) + 1)
        sp = np.bincount(ib, weights=wv * p3.ravel(), minlength=len(edges) + 1)
        ok = nb[1:len(edges)] > 0
        return (sk[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok], (sp[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]

# ---------------------------------------------------------------- gravity
def a0_code(a, a0rule, foot, E):
    base = A0[foot] / ACC_UNIT
    return base if a0rule == "TIE" else base * E(a)

def potential_k(mesh, delta, a, rule, a0rule, foot, E, ocl, diag=None):
    """Fourier potential (code units): Newton from lap phi_N = PFAC ocl delta / a; R1 adds QUMOND's phantom,
    lap phi_ph = -div[(nu(|g_N|/a0) - 1) g_N] with g_N = -grad phi_N (comoving; physical = g_N / a)."""
    dk = mesh.fwd(delta) * mesh.DEC                                    # A1: deposit window removed
    phik = (-PFAC * ocl / a) * dk * mesh.ik2
    if rule == "R1":
        gN = [-mesh.inv(1j * kv * phik) for kv in mesh.kvec]
        y = np.sqrt(gN[0] ** 2 + gN[1] ** 2 + gN[2] ** 2) / (a * a0_code(a, a0rule, foot, E))
        w = (nu_simple(y) - 1.0).astype(np.float32)
        if diag is not None:
            diag.update(y_p05=float(np.percentile(y, 5)), y_med=float(np.median(y)), y_p95=float(np.percentile(y, 95)), nu_med=float(np.median(w) + 1))
        del y
        divk = sum(1j * kv * mesh.fwd(w * g) for kv, g in zip(mesh.kvec, gN)); del gN, w
        phik = phik + divk * mesh.ik2
    return phik

def accel(mesh, phik, a):
    return [-a * mesh.inv(1j * kv * phik * mesh.DEC) for kv in mesh.kvec]   # -grad(a phi), as CFG359; A1: interpolation window removed

# ---------------------------------------------------------------- initial conditions
def class_ics(bg, z_on):
    """CLASS d_b(k) at z_on and d d_b / d ln a (central difference at a_on (1 +- 2 %)), per unit curvature; k in h/Mpc."""
    from classy import Class
    a_on = 1 / (1 + z_on); zp = 1 / (a_on * 1.02) - 1; zm = 1 / (a_on * 0.98) - 1
    p = {"h": H, "omega_b": OMB_H2, "omega_cdm": 1e-7, "n_s": NS, "A_s": 2.1e-9, "output": "mTk", "z_max_pk": zm + 1.0,
         "P_k_max_h/Mpc": 3.0}
    if bg == "B2":
        p.update({"Omega_fld": OFLD, "w0_fld": -0.001, "wa_fld": 0.0, "cs2_fld": 1.0, "use_ppf": "no"})
    c = Class(); c.set(p); c.compute()
    t0 = c.get_transfer(z=z_on); tp = c.get_transfer(z=zp); tm = c.get_transfer(z=zm)
    k = t0["k (h/Mpc)"]; db = t0["d_b"]; dlna = (tp["d_b"] - tm["d_b"]) / (math.log(a_on * 1.02) - math.log(a_on * 0.98))
    c.struct_cleanup()
    return k, db, dlna

def p_curv(k):
    """curvature power P_R(k) in (Mpc/h)^3 for k in h/Mpc, A_s = 1 (scaled by A_s outside)."""
    return 2 * math.pi ** 2 * (k * H / KP) ** (NS - 1) / k ** 3

def make_ics(N, amp_fn, damp_fn, E, a_on):
    """Zel'dovich particles from delta_k = w_k sqrt(N^6/L^3) amp(k) and d delta/d ln a = w_k sqrt(N^6/L^3) damp(k)."""
    rng = np.random.default_rng(SEED)
    m = Mesh(N)
    wk = sfft.rfftn(rng.standard_normal((N,) * 3), workers=1) / N ** 1.5
    kk = np.where(m.kk > 0, m.kk, 1.0)
    norm = math.sqrt(N ** 6 / L ** 3)
    dk = wk * norm * amp_fn(kk); vk = wk * norm * damp_fn(kk)
    for f in (dk, vk):
        f[N // 2, :, :] = 0; f[:, N // 2, :] = 0; f[:, :, -1] = 0; f[0, 0, 0] = 0
    psi = np.stack([sfft.irfftn(1j * kv * dk * m.ik2, s=(N,) * 3, workers=1).ravel() for kv in m.kvec], 1)
    dpsi = np.stack([sfft.irfftn(1j * kv * vk * m.ik2, s=(N,) * 3, workers=1).ravel() for kv in m.kvec], 1)
    q = (np.indices((N,) * 3).reshape(3, -1).T + 0.5) * (L / N)
    pos = (q + psi) % L
    mom = a_on ** 2 * E(a_on) * dpsi                                  # p = a^2 dx/dt = a^2 H d psi / d ln a
    return pos.astype(np.float64), mom.astype(np.float64), m

# ---------------------------------------------------------------- run
def step_grid(a_on, nstep):
    snaps = [1 / (1 + z) for z in SNAP_Z if 1 / (1 + z) > a_on]
    a = list(np.exp(np.linspace(math.log(a_on), 0.0, nstep + 1)))
    a = sorted(set([round(x, 12) for x in a + snaps]))
    return np.array(a), set(round(s, 12) for s in snaps)

def run(rule, a0rule, bg, As, N, nstep, z_on, foot, amp_fn=None, damp_fn=None, tag=None, save=True):
    E, ocl = background(bg); a_on = 1 / (1 + z_on); t0 = time.time()
    if amp_fn is None:
        kc, db, ddb = class_ics(bg, z_on)
        amp_fn = lambda k: np.sqrt(As * p_curv(k)) * np.interp(k, kc, db)
        damp_fn = lambda k: np.sqrt(As * p_curv(k)) * np.interp(k, kc, ddb)
    tag = tag or f"{rule}_{a0rule}_{bg}_As{As:g}_N{N}_s{nstep}_zon{z_on:g}_{foot}{SUF}"
    pos, mom, mesh = make_ics(N, amp_fn, damp_fn, E, a_on)
    aa, snapset = step_grid(a_on, nstep)
    res = dict(tag=tag, rule=rule, a0rule=a0rule, bg=bg, As=As, N=N, nstep=len(aa) - 1, z_on=z_on, foot=foot, L=L, h=H, mutate=MUTATE,
               psi_unit=PSI_UNIT, snaps=[])
    kin, pin = mesh.pk(mesh.fwd(np.zeros((N,) * 3, np.float32)))  # bins only
    res["k_in"] = kin.tolist(); res["P_in"] = (amp_fn(kin) ** 2).tolist()
    def snapshot(a):
        delta = mesh.deposit(pos); dg = {}
        phik = potential_k(mesh, delta, a, rule, a0rule, foot, E, ocl, diag=dg)
        kb, pd = mesh.pk(mesh.fwd(delta)); _, pp = mesh.pk(phik, deconv=False)   # A1: phik already carries the deposit deconvolution
        res["snaps"].append(dict(a=a, z=1 / a - 1, k=kb.tolist(), P_delta=pd.tolist(), P_psi=(pp * PSI_UNIT ** 2).tolist(),
                                 delta_rms=float(delta.std()), t=time.time() - t0, **dg))
        print(f"  [{tag}] z={1 / a - 1:7.3f} delta_rms={delta.std():.4g} {('y_med=%.3g nu_med=%.3g' % (dg['y_med'], dg['nu_med'])) if dg else ''} t={time.time() - t0:.0f}s", flush=True)
    snapshot(a_on)
    delta = mesh.deposit(pos); accp = mesh.interp(accel(mesh, potential_k(mesh, delta, a_on, rule, a0rule, foot, E, ocl), a_on), pos)
    for n in range(len(aa) - 1):
        a0_, a1 = aa[n], aa[n + 1]; am = math.sqrt(a0_ * a1)
        mom += quad(lambda x: 1 / (x * x * E(x)), a0_, am)[0] * accp
        pos = (pos + quad(lambda x: 1 / (x ** 3 * E(x)), a0_, a1)[0] * mom) % L
        delta = mesh.deposit(pos); accp = mesh.interp(accel(mesh, potential_k(mesh, delta, a1, rule, a0rule, foot, E, ocl), a1), pos)
        mom += quad(lambda x: 1 / (x * x * E(x)), am, a1)[0] * accp
        if round(a1, 12) in snapset:
            snapshot(a1)
    res["runtime_s"] = time.time() - t0
    if save:
        os.makedirs(RUNS, exist_ok=True); json.dump(res, open(os.path.join(RUNS, tag + ".json"), "w"))
    return res

# ---------------------------------------------------------------- checks K1, K2 (K3 and K4 are in wg2_grade.py)
def checks():
    out = {}
    # K1: Newtonian growth in EdS with all matter clustering: P(a)/P(a_i) = (a/a_i)^2 at k < 0.05 h/Mpc
    z_i = 49.0; a_i = 1 / (1 + z_i)
    amp = lambda k: np.sqrt(2e3 * (k / 0.01) ** -1.0) * a_i                          # linear: delta_rms ~ 1e-2 at a = 0.5
    r = run("R0", "TIE", "EDS", 1.0, 128, 120, z_i, "canonical", amp_fn=amp, damp_fn=amp, tag="K1", save=False)   # A1: at 128^3
    s0 = r["snaps"][0]; s1 = [s for s in r["snaps"] if abs(s["z"] - 1.0) < 1e-9][0]
    k = np.array(s0["k"]); m = k < 0.05
    ratio = float(np.mean(np.array(s1["P_delta"])[m] / np.array(s0["P_delta"])[m]) / (s1["a"] / s0["a"]) ** 2)
    out["K1"] = dict(ratio_over_expected=ratio, tol=0.03, pass_=abs(ratio - 1) < 0.03)
    print(f"K1 growth: P ratio / (a/a_i)^2 = {ratio:.4f} (tol 3 %) -> {'PASS' if out['K1']['pass_'] else 'FAIL'}")
    # K2: 1D sinusoid, curl-free, the solver's total g equals nu g_N pointwise (k = 0 and x-Nyquist components removed)
    M = 64; mesh = Mesh(M); E, _ = background("B2"); a = 0.5
    x = (np.arange(M) + 0.5) * mesh.dx
    delta = np.broadcast_to((1e-3 * np.cos(2 * np.pi * x / L))[:, None, None], (M, M, M)).astype(np.float32).copy()
    phN = (-PFAC * OMB / a) * mesh.fwd(delta) * mesh.DEC * mesh.ik2         # same Newton input as the engine: K2 tests QUMOND only
    gN = [-mesh.inv(1j * kv * phN) for kv in mesh.kvec]
    y = np.sqrt(sum(g ** 2 for g in gN)) / (a * a0_code(a, "TIE", "canonical", E))
    want = [mesh.fwd((nu_simple(y) * g).astype(np.float64)) for g in gN]
    for wk_ in want:
        wk_[0, 0, 0] = 0; wk_[M // 2, :, :] = 0
    want = [mesh.inv(wk_) for wk_ in want]
    ph = potential_k(mesh, delta, a, "R1", "TIE", "canonical", E, OMB)
    got = [-mesh.inv(1j * kv * ph) for kv in mesh.kvec]
    err = max(float(np.max(np.abs(g - w_))) for g, w_ in zip(got, want)) / float(np.max(np.abs(want[0])))
    out["K2"] = dict(max_rel_err=err, tol=1e-4, pass_=err < 1e-4, y_median=float(np.median(y)))
    print(f"K2 QUMOND plane wave: max |g - nu g_N| / max = {err:.2e} (tol 1e-4; y median {np.median(y):.3g}) -> {'PASS' if out['K2']['pass_'] else 'FAIL'}")
    os.makedirs(RUNS, exist_ok=True); json.dump(out, open(os.path.join(RUNS, f"checks{SUF}.json"), "w"), indent=1)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "checks":
        checks()
    else:
        _, _, rule, a0r, bg, As, N, ns, zon, foot = sys.argv
        run(rule, a0r, bg, float(As), int(N), int(ns), float(zon), foot)
