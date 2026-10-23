"""H2_aest_clusters (criteria 364a56c250): can AeST's quasi-static mass term mu^2 Phi supply F1's cluster-core (MID) lensing
excess without overshooting OUTER?  Exact spherical solve of VSZ (arXiv:2304.05134) eqs. Phi-Orig / Chi-Orig at beta0 = 0
with C1's capped J (=> AQUAL mu = x/(1+x)), on F1's per-cluster stack (read-only scratch cache f1_meas.pkl).
Usage: h2_aest_clusters.py <F1 scratch cache dir> [--mutate].  --mutate flips the mass-term sign (Yukawa): K3/K4 must FAIL.
Deterministic, no network, single thread."""
import os, sys, json, time, pickle, hashlib, resource, numpy as np
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]; TAG = "_MUTATE" if MUT else ""
SGN = -1.0 if MUT else 1.0                                   # sign of the mass term (+1 = AeST Helmholtz)
OUTF = open(os.path.join(HERE, f"h2_aest_clusters{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
import ctypes
try: _LIBC = ctypes.CDLL(None); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception: _LIBC = None
def relieve():                                                  # macOS: hand freed large blocks back to the OS (RSS hygiene only)
    if _LIBC is not None and sys.platform == "darwin": _LIBC.malloc_zone_pressure_relief(None, ctypes.c_size_t(0))
def mem(tag):
    pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; say(f"  [mem] {tag}: max RSS so far {pk/1e9 if sys.platform == 'darwin' else pk/1e6:.3f} GB")
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
# ---------------------------------------------------------------- constants and F1's conventions (copied, F1 f1_cluster_cores.py)
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; KG_PC2 = MSUN/(3.0857e16)**2; KPC = MPC/1e3
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # kappa = 1/2 FITTED
from scipy.interpolate import PchipInterpolator
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
def DA_lcdm(z, H0=70.0, Om=0.3):
    zz = np.linspace(0, z, 600); E = np.sqrt(Om*(1 + zz)**3 + 1 - Om); return _trap(1/E, zz)*C/1e3/H0/(1 + z)
HS = {"h0672": 0.672, "h0686": 0.686}
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
def g_aqual(gN, a0):                                          # odd extension of the spherical AQUAL root (mu = x/(1+x))
    x = np.abs(gN); return np.sign(gN)*(0.5*x + np.sqrt(0.25*x**2 + x*a0))
RG = np.logspace(-3, np.log10(30), 3000); RF = np.logspace(np.log10(2e-3), np.log10(3.5), 90); UU = np.linspace(0, 1, 2001)
RGF = np.logspace(-3, np.log10(30), 5999)                      # RGF[0::2] == RG; odd points = RK4 midpoints
assert np.allclose(RGF[::2], RG, rtol=1e-12)
def gas_mass_grid(Mg500, R500, r):                             # F1 gas_mass(shape="G0") on an arbitrary grid
    rc = 0.15*R500; sh = (1 + (r/rc)**2)**(-1.0); sh = np.where(r > 3.0, 0.0, sh)
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    return M*(Mg500*MSUN/np.interp(R500, r, M))
# F1's own log projector (reference for K2 only)
def f1_project(rho, r=RG):
    lr = np.log(r); pos = rho > 0; lrho = np.log(np.where(pos, rho, 1e-300))
    umax = np.arccosh(r[-1]/RF); u = UU[None, :]*umax[:, None]; rr = RF[:, None]*np.cosh(u)
    Sig = 2*_trap(np.exp(np.interp(np.log(rr), lr[pos], lrho[pos]))*rr*MPC, u, axis=1)
    return Sig
def f1_dsig(Sig):
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return 2*cum/RF**2 - Sig
def f1_offset(Sig, d):
    if d <= 1e-4: return Sig
    ph = np.linspace(0, np.pi, 181); Rp = np.sqrt(RF[:, None]**2 + d**2 + 2*RF[:, None]*d*np.cos(ph[None, :]))
    return _trap(np.exp(np.interp(np.log(Rp), np.log(RF), np.log(Sig))), ph, axis=1)/np.pi
def f1_bins(ds): return np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(ds, 1e-30))))
# ---------------------------------------------------------------- my signed linear operators (rho on RG -> binned DeltaSigma)
def interp_weights(xq, xg):
    """rows of linear-interpolation weights (clamped, like np.interp) of points xq on grid xg"""
    xq = np.clip(xq, xg[0], xg[-1]); i = np.clip(np.searchsorted(xg, xq) - 1, 0, len(xg) - 2)
    t = (xq - xg[i])/(xg[i + 1] - xg[i]); return i, t
def build_P():
    lr = np.log(RG); P = np.zeros((len(RF), len(RG)))
    umax = np.arccosh(RG[-1]/RF); wu = np.full(len(UU), UU[1] - UU[0]); wu[[0, -1]] *= 0.5
    for j in range(len(RF)):
        u = UU*umax[j]; rr = RF[j]*np.cosh(u); w = 2*wu*umax[j]*rr*MPC
        i, t = interp_weights(np.log(rr), lr); np.add.at(P[j], i, w*(1 - t)); np.add.at(P[j], i + 1, w*t)
    return P
def build_D():
    n = len(RF); E = np.eye(n); return np.stack([f1_dsig(E[:, k]) for k in range(n)], 1)
def build_O(d):
    n = len(RF); O = np.zeros((n, n))
    if d <= 1e-4: return np.eye(n)
    ph = np.linspace(0, np.pi, 181); wp = np.full(len(ph), ph[1] - ph[0]); wp[[0, -1]] *= 0.5
    for j in range(n):
        Rp = np.sqrt(RF[j]**2 + d**2 + 2*RF[j]*d*np.cos(ph)); i, t = interp_weights(np.log(Rp), np.log(RF))
        np.add.at(O[j], i, wp*(1 - t)/np.pi); np.add.at(O[j], i + 1, wp*t/np.pi)
    return O
def build_B():
    B = np.zeros((len(RC), len(RF))); i, t = interp_weights(np.log(RC), np.log(RF))
    B[np.arange(len(RC)), i] = 1 - t; B[np.arange(len(RC)), i + 1] = t; return B
# ---------------------------------------------------------------- the AeST spherical solver (exact quasi-static, RK4 in ln r)
def solve(r_nodes_Mpc, Mb_nodes, Mb_mid, Phi0, D0, mu2, a0, store_all=True):
    """y = (Phi, D): Phi' = g_AQUAL(G (Mb + D)/r^2), D' = -SGN mu2 r^2 Phi / G  (D = extra effective mass from mu^2 Phi).
    Mb_* broadcast over leading dims (radial axis last); returns (Phi, D, g) at nodes, or g only (store_all=False).
    r in Mpc, SI otherwise."""
    r = r_nodes_Mpc*MPC; rm = np.sqrt(r[1:]*r[:-1])
    Mn = np.ascontiguousarray(np.moveaxis(Mb_nodes, -1, 0)); Mm = np.ascontiguousarray(np.moveaxis(Mb_mid, -1, 0))
    shape = np.broadcast(np.asarray(Phi0), Mn[0]).shape
    g = np.empty((len(r),) + shape); Phi = np.empty_like(g) if store_all else None; D = np.empty_like(g) if store_all else None
    def f(rr, Mb, ph, dd):
        a = g_aqual(G*(Mb + dd)/rr**2, a0) if a0 > 0 else G*(Mb + dd)/rr**2
        return rr*a, -SGN*mu2*rr**3*ph/G, a
    ph = np.broadcast_to(Phi0, shape).astype(float).copy(); dd = np.broadcast_to(D0, shape).astype(float).copy()
    for k in range(len(r) - 1):
        h = np.log(r[k + 1]/r[k])
        k1p, k1d, gk = f(r[k], Mn[k], ph, dd)
        g[k] = gk
        if store_all: Phi[k], D[k] = ph, dd
        k2p, k2d, _ = f(rm[k], Mm[k], ph + 0.5*h*k1p, dd + 0.5*h*k1d)
        k3p, k3d, _ = f(rm[k], Mm[k], ph + 0.5*h*k2p, dd + 0.5*h*k2d)
        k4p, k4d, _ = f(r[k + 1], Mn[k + 1], ph + h*k3p, dd + h*k3d)
        ph = ph + h/6*(k1p + 2*k2p + 2*k3p + k4p); dd = dd + h/6*(k1d + 2*k2d + 2*k3d + k4d)
    _, _, g[-1] = f(r[-1], Mn[-1], ph, dd)
    if store_all: Phi[-1], D[-1] = ph, dd
    mv = lambda x: np.moveaxis(x, 0, -1)
    return (mv(Phi), mv(D), mv(g)) if store_all else mv(g)
def lam_max(mu, rM): return (2/3)*(1 - np.log(3*np.sqrt(2)/(mu*rM)))      # VSZ eq_chioutmax (lengths in m)
def phi_c_for(Mb_nodes, Mtot, a0, mu, Delta, r_nodes_Mpc, Rref=3.0):
    """central Phi giving VSZ's lambda = lambda_max + Delta in the MOND exterior, imposed on the mu = 0 solution at Rref (H8)."""
    r = r_nodes_Mpc*MPC; gl = g_aqual(G*Mb_nodes/r**2, a0)
    Phi_mu0 = np.concatenate([np.zeros(Mb_nodes.shape[:-1] + (1,)), np.cumsum(0.5*(gl[..., 1:] + gl[..., :-1])*np.diff(r), -1)], -1)
    k = np.searchsorted(r_nodes_Mpc, Rref); s = np.sqrt(G*Mtot*a0); rM = np.sqrt(G*Mtot/a0); R = r[k]
    lam = lam_max(mu, rM)[..., None] + np.asarray(Delta)[None, :] if np.ndim(Delta) else lam_max(mu, rM) + Delta
    if np.ndim(Delta): target = -(G*Mtot/R)[..., None] + s[..., None]*(lam + np.log(R/rM)[..., None]); return (target - Phi_mu0[..., k][..., None]).T
    return -(G*Mtot/R) + s*(lam + np.log(R/rM)) - Phi_mu0[..., k]
# ---------------------------------------------------------------- K3, K4: analytic Helmholtz tests (Newtonian, a0 = 0)
mu_t = 1.0/MPC; mu2t = mu_t**2
rr = RG*MPC; ok = rr <= 10/mu_t; Phic = 1e12
x0 = mu_t*rr[0]; D0 = (rr[0]**2*Phic*(x0*np.cos(x0) - np.sin(x0))/(x0*rr[0]))/G     # r0^2 Phi'(r0)/G, Mb = 0
Ph, _, _ = solve(RG, np.zeros(len(RG)), np.zeros(len(RG) - 1), Phic*np.sin(x0)/x0, D0, mu2t, 0.0)
e3 = float(np.max(np.abs(Ph[ok] - Phic*np.sin(mu_t*rr[ok])/(mu_t*rr[ok])))/Phic)
check("K3", e3 <= 1e-6, f"max|Phi - Phic sin(mu r)/(mu r)|/Phic = {e3:.2e}", "<= 1e-6 (r <= 10/mu)")
ka = int(np.argmin(np.abs(RG - 0.3))); a_th = RG[ka]*MPC; rho0 = 1e-22; Mth = lambda r_: 4/3*np.pi*rho0*np.minimum(r_*MPC, a_th)**3
Phic4 = -2e12; Kc = 4*np.pi*G*rho0/mu2t; A_ = Phic4 - Kc
def th_in(r_): x = mu_t*r_; return Kc + A_*np.sin(x)/x, A_*(x*np.cos(x) - np.sin(x))/(x*r_)
Pa, dPa = th_in(a_th); ca, sa = np.cos(mu_t*a_th), np.sin(mu_t*a_th)
M2 = np.array([[ca/a_th, sa/a_th], [(-mu_t*a_th*sa - ca)/a_th**2, (mu_t*a_th*ca - sa)/a_th**2]]); Bc, Cc = np.linalg.solve(M2, [Pa, dPa])
def th_d(r_):
    din = th_in(np.minimum(r_, a_th))[1]; x = mu_t*r_
    dout = Bc*(-mu_t*r_*np.sin(x) - np.cos(x))/r_**2 + Cc*(mu_t*r_*np.cos(x) - np.sin(x))/r_**2
    return np.where(r_ <= a_th, din, dout)
p0, dp0 = th_in(rr[0]); D04 = rr[0]**2*dp0/G - Mth(RG[0])
_, _, g4 = solve(RG, Mth(RG), Mth(np.sqrt(RG[1:]*RG[:-1])), p0, D04, mu2t, 0.0)
e4 = float(np.max(np.abs(g4[ok] - th_d(rr[ok])))/np.max(np.abs(th_d(rr[ok]))))
check("K4", e4 <= 1e-5, f"max|Phi' - analytic|/max|Phi'| = {e4:.2e} (top-hat a = {RG[ka]:.4f} Mpc)", "<= 1e-5")
# ---------------------------------------------------------------- F1's measurement (read-only) and statistic
PK = os.path.join(CACHE, "f1_meas.pkl"); sha = hashlib.sha256(open(PK, "rb").read()).hexdigest()
MEAS = pickle.load(open(PK, "rb")); N = len(MEAS); say(f"F1 measurement {PK} sha256 {sha}  clusters {N}"); RES["f1_meas_sha256"] = sha
order = np.argsort([o["ra"] for o in MEAS]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N)*30//N
def A_band(D, P, W, sel): return {b: float((W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*P[sel][:, j]).sum()) for b, j in BANDS.items()}
def jk(D, P, W):
    full = A_band(D, P, W, np.ones(N, bool)); reps = [A_band(D, P, W, PATCH != p) for p in range(30)]
    return {b: (full[b], float(np.sqrt(29/30*np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps]))**2)))) for b in full}
DAT = {}
for hk in HS:
    D = np.array([o[hk]["D"] for o in MEAS]); Eh = np.array([o[hk]["E"] for o in MEAS]); W = np.where(Eh < 1e8, 1/Eh**2, 0)
    B = np.array([o[hk]["den"] for o in MEAS]).sum(0)/np.array([o[hk]["den_r"] for o in MEAS]).sum(0)
    DAT[hk] = dict(D=D, W=W, B=B)
# baryons (F1 PRIMARY: gas rescaled q^{5/2}, R500 x q, beta-model G0, f* = 0.20), on RG and on the RK4 midpoints
MB, MBM, MISD = {}, {}, {}
for hk, h in HS.items():
    mb, mbm, mis = [], [], []
    for o in MEAS:
        q = (float(DM(o["z"], h))/(1 + o["z"]))/DA_lcdm(o["z"]); Mf = gas_mass_grid(o["Mgas500"]*q**2.5, o["R500"]*q, RGF)*1.20
        mb.append(Mf[0::2]); mbm.append(Mf[1::2]); mis.append(np.radians(o["off_deg"])*float(DM(o["z"], h))/(1 + o["z"]))
    MB[hk], MBM[hk], MISD[hk] = np.array(mb), np.array(mbm), np.array(mis)
# operators
Pm = build_P(); Dm = build_D(); Bm = build_B(); BD = Bm @ Dm
_TC = {}
def getT(hk):                                                    # (N, 8, Nr): rho -> binned DeltaSigma; one h held at a time (memory)
    if hk not in _TC:
        _TC.clear(); import gc; gc.collect(); relieve(); T_ = np.empty((len(MISD[hk]), len(RC), len(RG)))
        for i, d in enumerate(MISD[hk]): T_[i] = BD @ build_O(d) @ Pm
        _TC[hk] = T_
    return _TC[hk]
mem("operators built")
def rho_from_g(g):
    ML = g*(RG*MPC)**2/G; return np.gradient(ML, RG*MPC, axis=-1)/(4*np.pi*(RG*MPC)**2)
def pred(hk, g): return np.matmul(getT(hk), rho_from_g(g)[..., None])[..., 0]/KG_PC2
def A_cell(hk, Pp, boost=True):
    d = DAT[hk]; return jk(d["D"]*(d["B"][None, :] if boost else 1.0), Pp, d["W"])
PB = [3, 4, 5, 6, 7]; HARTLAP = (30 - len(PB) - 2)/29
def chi2_prof(hk, Pp, boost=True):
    """A1: residual stack s_j = sum_i W (D B - P) / sum_i W over bins 3-7, jackknife covariance (30 patches), Hartlap."""
    d = DAT[hk]; Dd = d["D"]*(d["B"][None, :] if boost else 1.0); W = d["W"]
    f = lambda sel: (W[sel][:, PB]*(Dd[sel][:, PB] - Pp[sel][:, PB])).sum(0)/W[sel][:, PB].sum(0)
    s0 = f(np.ones(N, bool)); reps = np.array([f(PATCH != p) for p in range(30)]); Cv = 29/30*(reps - reps.mean(0)).T @ (reps - reps.mean(0))
    return float(HARTLAP*s0 @ np.linalg.solve(Cv, s0)), s0.tolist()
# ---------------------------------------------------------------- K1 / K2 / K5: mu = 0 reproduction
F1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json")))
LAW, dev1 = {}, []
for hk in HS:
    for f in A0:
        gl = g_aqual(G*MB[hk]/(RG*MPC)**2, A0[f]); LAW[(hk, f)] = pred(hk, gl); a = A_cell(hk, LAW[(hk, f)])
        ref = F1J["rows"][f"PRIMARY {hk}"][f]; dev1 += [abs(a["MID"][0] - ref["MID"][0]), abs(a["OUTER"][0] - ref["OUTER"][0])]
        say(f"  mu=0 {hk} {f:9s}: MID {a['MID'][0]:.4f}+-{a['MID'][1]:.4f} (F1 {ref['MID'][0]:.4f})  OUTER {a['OUTER'][0]:.4f} (F1 {ref['OUTER'][0]:.4f})")
for hk in HS:
    for f in A0: say(f"  A1 law profile chi2 (bins 3-7) {hk} {f}: {chi2_prof(hk, LAW[(hk, f)])[0]:.1f}")
check("K1", max(dev1) <= 0.01, f"max |A - A_F1| over MID/OUTER x 4 cells = {max(dev1):.4f}", "<= 0.01")
rat = []
for i, o in enumerate(MEAS):                                   # F1's own projector chain for the same cluster (canonical, h0672)
    gl = g_aqual(G*MB["h0672"][i]/(RG*MPC)**2, A0["canonical"]); ML = gl*(RG*MPC)**2/G; rho = np.gradient(ML, RG*MPC)/(4*np.pi*(RG*MPC)**2)
    ref = f1_bins(f1_dsig(f1_offset(f1_project(rho), MISD["h0672"][i])))/KG_PC2; rat.append(LAW[("h0672", "canonical")][i, 3:]/ref[3:])
rat = np.abs(np.array(rat) - 1)
check("K2", np.median(rat) <= 2e-3 and rat.max() <= 2e-2, f"median {np.median(rat):.2e} max {rat.max():.2e}", "median <= 2e-3, max <= 2e-2")
Mtot = {hk: MB[hk][:, -1] for hk in HS}
def aest_pred(hk, f, mu_Mpc, Delta):
    mu = mu_Mpc/MPC; Dl = np.atleast_1d(np.asarray(Delta, float))
    Phc = phi_c_for(MB[hk], Mtot[hk], A0[f], mu, Dl, RG)                     # (nDelta, N)
    out = []
    for c0 in range(0, len(Dl), 4):                                          # chunks of 4 Delta values (memory)
        g = solve(RG, MB[hk][None], MBM[hk][None], Phc[c0:c0 + 4], 0.0, mu**2, A0[f], store_all=False)
        out += [pred(hk, g[k]) for k in range(g.shape[0])]
        del g; relieve()
    return np.array(out), None
P5, _ = aest_pred("h0672", "canonical", 1e-6, [0.0]); e5 = float(np.max(np.abs(P5[0]/LAW[("h0672", "canonical")] - 1)))
mem("mu = 0 reproduction done"); check("K5", e5 <= 1e-6, f"max |P(mu=1e-6)/P(mu=0) - 1| = {e5:.2e}", "<= 1e-6")
# ---------------------------------------------------------------- galaxy-RAR guard (Hernquist 1e11 Msun, a_h = 3 kpc)
RGg = np.logspace(-5, np.log10(30), 4000); RGgm = np.sqrt(RGg[1:]*RGg[:-1]); Mg_ = 1e11*MSUN; ah = 3e-3
Mh = lambda r_: Mg_*r_**2/(r_ + ah)**2
def galaxy_dev(f, mu_Mpc, Deltas):
    mu = mu_Mpc/MPC; Dl = np.atleast_1d(np.asarray(Deltas, float)); Mn = Mh(RGg)
    Phc = phi_c_for(Mn[None], np.array([Mg_]), A0[f], mu, Dl, RGg)[:, 0]
    g = solve(RGg, Mn[None], Mh(RGgm)[None], Phc[:, None], 0.0, mu**2, A0[f], store_all=False)[:, 0]
    gl = g_aqual(G*Mn/(RGg*MPC)**2, A0[f]); dv = np.abs(g/gl - 1)
    return {"max_dev_le_200kpc": dv[:, RGg <= 0.2].max(1), "dev_100kpc": dv[:, np.searchsorted(RGg, 0.1)], "dev_1Mpc": (g/gl - 1)[:, np.searchsorted(RGg, 1.0)]}
# ---------------------------------------------------------------- the scan (frozen grids)
MU_OK = [0.1, 0.3, 0.5, 0.7, 1.0]; MU_PROBE = [1.58, 2.0, 3.0]; DEL = np.round(np.arange(-8, 2.0001, 0.25), 4); i0 = int(np.argmin(np.abs(DEL)))
CELLS = [(hk, f) for hk in HS for f in A0]
SCAN = {}
say("\n=== AeST quasi-static mass term on F1's PRIMARY stack: A = data / AeST prediction (jackknife sigma) ===")
GAL = {}
for hk in HS:
  for mu_Mpc in MU_OK + MU_PROBE:
    lab = "allowed" if mu_Mpc <= 1.0 else "EXCLUDED (mu^-1 < 1 Mpc)"
    if mu_Mpc not in GAL: GAL[mu_Mpc] = {f: galaxy_dev(f, mu_Mpc, DEL) for f in A0}
    gal = GAL[mu_Mpc]
    for f in A0:
        Pp, _ = aest_pred(hk, f, mu_Mpc, DEL)
        rows = []
        for k, dl in enumerate(DEL):
            a = A_cell(hk, Pp[k]); ac = A_cell(hk, Pp[k], boost=False)
            ratio = [(DAT[hk]["W"][:, j]*Pp[k][:, j]).sum()/(DAT[hk]["W"][:, j]*LAW[(hk, f)][:, j]).sum() for j in range(8)]
            zm, zo = (a["MID"][0] - 1)/a["MID"][1], (a["OUTER"][0] - 1)/a["OUTER"][1]
            gd = float(gal[f]["max_dev_le_200kpc"][k])
            c2, res = chi2_prof(hk, Pp[k]); p_fz = bool(abs(zm) <= 2 and zo >= -2 and gd <= 0.10)
            rows.append(dict(Delta=float(dl), A=a, A_clip=ac, Z_MID=zm, Z_OUT=zo, boost_vs_law=ratio, gal_maxdev_200kpc=gd,
                             gal_dev_1Mpc=float(gal[f]["dev_1Mpc"][k]), passes=p_fz, chi2_prof=c2, resid_stack=res,
                             passes_A1=bool(p_fz and abs(zo) <= 2 and c2 <= 11.07)))
        SCAN[(mu_Mpc, hk, f)] = rows
        r0 = rows[i0]; ok_ = [r for r in rows if r["Z_OUT"] >= -2]; best = min(ok_, key=lambda r: r["A"]["MID"][0]) if ok_ else None
        npass = [r["Delta"] for r in rows if r["passes"]]
        say(f"mu {mu_Mpc:4.2f} [{lab}] {hk} {f:9s} | Delta=0: MID {r0['A']['MID'][0]:.3f}+-{r0['A']['MID'][1]:.3f} (Z {r0['Z_MID']:+.1f}) "
            f"OUT {r0['A']['OUTER'][0]:.3f}+-{r0['A']['OUTER'][1]:.3f} (Z {r0['Z_OUT']:+.1f}) bin-ratio AeST/law "
            + " ".join(f"{x:.2f}" for x in r0["boost_vs_law"]) + f" gal200 {r0['gal_maxdev_200kpc']:.3f}"
            + (f" | best MID with Z_OUT>=-2: {best['A']['MID'][0]:.3f} (Z {best['Z_MID']:+.1f}) at Delta {best['Delta']:+.2f}, OUT {best['A']['OUTER'][0]:.3f}, gal200 {best['gal_maxdev_200kpc']:.3f}" if best else " | no Delta keeps Z_OUT >= -2")
            + f" | passing Delta: {npass if npass else 'none'}"
            + f" | A1: min chi2_prof {min(r['chi2_prof'] for r in rows):.1f} at Delta {min(rows, key=lambda r: r['chi2_prof'])['Delta']:+.2f}, chi2(Delta=0) {r0['chi2_prof']:.1f}, passing {[r['Delta'] for r in rows if r['passes_A1']] or 'none'}")
for mu_Mpc, gal in GAL.items():
    say(f"   galaxy guard mu {mu_Mpc}: Delta=0 max|dev| (r<=200 kpc) can {gal['canonical']['max_dev_le_200kpc'][i0]:.3f} alt {gal['alt']['max_dev_le_200kpc'][i0]:.3f}; "
        f"dev at 1 Mpc can {gal['canonical']['dev_1Mpc'][i0]:+.3f}; Delta range keeping <=0.10: "
        f"{[float(d) for d, v in zip(DEL, gal['canonical']['max_dev_le_200kpc']) if v <= 0.10][:1]}..{[float(d) for d, v in zip(DEL, gal['canonical']['max_dev_le_200kpc']) if v <= 0.10][-1:]}")
mem("scan done")
# ---------------------------------------------------------------- r_C and verdict (frozen rule)
rC = {}
for mu_Mpc in MU_OK + MU_PROBE:
    rM = np.sqrt(G*Mtot["h0672"]*A0["canonical"]/A0["canonical"]**2); rC[mu_Mpc] = float(np.median((1/3)*(18*rM/(mu_Mpc/MPC)**2)**(1/3))/MPC)
say("median VSZ r_C (Delta = 0, canonical, h0672) [Mpc]: " + "  ".join(f"mu {k}: {v:.2f}" for k, v in rC.items()))
say(f"median baryon mass M_b(<3 Mpc) h0672: {np.median(Mtot['h0672'])/MSUN:.3e} Msun; median r_M (canonical) {np.median(np.sqrt(G*Mtot['h0672']/A0['canonical']))/MPC:.3f} Mpc")
def all_cells(mu_Mpc, k): return all(SCAN[(mu_Mpc, hk, f)][k]["passes"] for hk, f in CELLS)
can0 = [m for m in MU_OK if all_cells(m, i0)]
knob = [(m, float(DEL[k])) for m in MU_OK for k in range(len(DEL)) if all_cells(m, k)]
probe_pass = [(m, float(DEL[k])) for m in MU_PROBE for k in range(len(DEL)) if all_cells(m, k)]
anycell_ok = [(m, hk, f, r["Delta"]) for (m, hk, f), rows in SCAN.items() if m <= 1.0 for r in rows if r["passes"]]
envelope = {}
for (m, hk, f), rows in SCAN.items():
    ok_ = [r for r in rows if r["Z_OUT"] >= -2]; best = min(ok_, key=lambda r: r["A"]["MID"][0]) if ok_ else None
    envelope[f"{m}|{hk}|{f}"] = dict(best_A_MID=best["A"]["MID"][0] if best else None, best_Delta=best["Delta"] if best else None,
                                    A_MID_Delta0=rows[i0]["A"]["MID"][0], A_OUT_Delta0=rows[i0]["A"]["OUTER"][0])
ck_ok = all(ok for n, ok in CHECKS if n in ("K1", "K2", "K3", "K4", "K5"))
if not ck_ok: V = "UNDECIDED (checks)"
elif can0: V = "AeST CAN SUPPLY IT"
elif knob: V = "CAN ONLY WITH A FITTED ZERO POINT"
elif anycell_ok: V = "UNDECIDED (cell split)"
else: V = "CANNOT"
say(f"\npassing at Delta=0 (allowed mu): {can0}; passing with a universal Delta (allowed mu): {knob[:12]}{' ...' if len(knob) > 12 else ''}")
say(f"cells passing anywhere at allowed mu: {len(anycell_ok)}; all-cell passes at EXCLUDED probe mu: {probe_pass[:12]}")
say(f"VERDICT (frozen rule): {V}")
say("\n=== AMENDMENT A1 (POST-RESULT): two-sided OUTER + bins 3-7 profile chi2 ===")
def all_A1(mu_Mpc, k): return all(SCAN[(mu_Mpc, hk, f)][k]["passes_A1"] for hk, f in CELLS)
can0_A1 = [m for m in MU_OK if all_A1(m, i0)]; knob_A1 = [(m, float(DEL[k])) for m in MU_OK for k in range(len(DEL)) if all_A1(m, k)]
probe_A1 = [(m, float(DEL[k])) for m in MU_PROBE for k in range(len(DEL)) if all_A1(m, k)]
cells_A1 = [(m, hk, f, r["Delta"]) for (m, hk, f), rows in SCAN.items() if m <= 1.0 for r in rows if r["passes_A1"]]
best_A1 = {f"{m}|{hk}|{f}": min(rows, key=lambda r: r["chi2_prof"])["chi2_prof"] for (m, hk, f), rows in SCAN.items()}
V_A1 = ("UNDECIDED (checks)" if not ck_ok else "AeST CAN SUPPLY IT" if can0_A1 else "CAN ONLY WITH A FITTED ZERO POINT" if knob_A1
        else "UNDECIDED (cell split)" if cells_A1 else "CANNOT")
say(f"A1 all-cell passes at Delta=0: {can0_A1}; with a universal Delta (allowed mu): {knob_A1}; at EXCLUDED probes: {probe_A1}")
say(f"A1 single cells passing at allowed mu: {cells_A1}")
say("A1 smallest profile chi2 over Delta per (mu, cell): " + "  ".join(f"{k}:{v:.1f}" for k, v in best_A1.items()))
say(f"VERDICT under A1 (post-result): {V_A1}")
RES.update(verdict_A1=V_A1, A1_can_Delta0=can0_A1, A1_knob=knob_A1, A1_probe=probe_A1, A1_cells=cells_A1, A1_min_chi2=best_A1)
pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; pk_gb = pk/1e9 if sys.platform == "darwin" else pk/1e6
check("K6", pk_gb < 1.0, f"peak RSS {pk_gb:.3f} GB", "< 1 GB")
RES.update(verdict=V, can_Delta0=can0, knob_passes=knob, probe_passes=probe_pass, anycell_allowed=anycell_ok, rC_median_Mpc=rC,
           envelope=envelope, scan={f"{m}|{hk}|{f}": rows for (m, hk, f), rows in SCAN.items()}, N=N, runtime_s=time.time() - T0, peak_rss_GB=pk_gb)
npass = sum(ok for _, ok in CHECKS); say(f"H2_AEST_CLUSTERS COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"h2_aest_clusters_results{TAG}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
sys.exit(0 if npass == len(CHECKS) else 1)
