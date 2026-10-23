"""M2_cluster_compact (criteria 15f797cbaa, amendment A1 4c6f49523c): K1's C2 tidal-charge term (DMPR 'black hole on the brane'
per baryon mass element; the owner's idea), screened per object by the record's stiffness profile S(s) (CFG691 / D7d / C6),
s = r / l_g, l_g = L*^2 / (2 r_M), r_M = sqrt(G M_b / a0).  One constant l_Q calibrated on F1 MID only; L* = 24 / 50 / 90 pc
(D10 / D7d / C6 window, not fitted).  Predictions with no refit: F1 OUTER + profile chi2, isolated galaxies (F2 masses), dwarf
satellites (E3 CSV), Solar System (perihelion-equivalent anomaly vs C6 bounds; Galactic C2 tide Q2 vs Hees), wide binaries;
cosmology reported (background mode, linear growth).
--mutate: scalar Laplacian in the profile ODE (CFG691 M2): M1 must FAIL.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 m2_cluster_compact.py <dir holding F1's f1_meas.pkl> [--mutate]
Deterministic, no network, single thread."""
import os, sys, json, time, pickle, hashlib, resource, csv, math
import numpy as np
from scipy.integrate import solve_bvp, quad, solve_ivp
from scipy.interpolate import PchipInterpolator
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"m2_cluster_compact{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT, "criteria_commit": "15f797cbaa", "amendment_A1_commit": "4c6f49523c"}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def mem(tag):
    pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; gb = pk/1e9 if sys.platform == "darwin" else pk/1e6
    RES["peak_rss_GB"] = gb; say(f"  [mem] {tag}: max RSS so far {gb:.3f} GB, t = {time.time()-T0:.0f} s")
import ctypes, gc
try: _LIBC = ctypes.CDLL(None); _LIBC.malloc_zone_pressure_relief.restype = ctypes.c_size_t
except Exception: _LIBC = None
def relieve():
    gc.collect()
    if _LIBC is not None and sys.platform == "darwin": _LIBC.malloc_zone_pressure_relief(None, ctypes.c_size_t(0))
np.seterr(divide="ignore", over="ignore", invalid="ignore")   # Accelerate BLAS raises spurious FP flags; finiteness asserted below

G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; KG_PC2 = MSUN/(3.0857e16)**2; KPC = MPC/1e3; PC = 3.0857e16
AU = 1.495978707e11
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                                    # kappa = 1/2 FITTED
FEET = ("canonical", "alt"); LSTARS = (24.0, 50.0, 90.0)

# ======================================================================================= the screening profile (CFG691 ODE)
say("=== S(s): CFG691's profile -[q'' + 2q'/s - 2q/s^2] + q|q| = 1/s^2 (vector Laplacian), re-solved ===")
SMIN, SMAX = 1e-4, 1e4
def solve_profile(vector=True):
    k = 2.0 if vector else 0.0
    def f(t, y):
        s = np.exp(t); return np.vstack([y[1], -y[1] + k*y[0] + s**2*y[0]*np.abs(y[0]) - 1.0])
    def bc(ya, yb): return np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1/SMAX - 1/SMAX**2)])
    t = np.linspace(math.log(SMIN), math.log(SMAX), 4001); s = np.exp(t)
    sol = solve_bvp(f, bc, t, np.vstack([1/(s + 2), -s/(s + 2)**2]), tol=1e-8, max_nodes=200000)
    return sol, f
SOL, FF = solve_profile(vector=not MUT)
tt = np.linspace(SOL.x[0], SOL.x[-1], 20001); yy = SOL.sol(tt); dy = SOL.sol(tt, 1)
RESID = float(np.max(np.abs(dy[1] - FF(tt, yy)[1])/(1 + np.abs(FF(tt, yy)[1]))))
A_IN = float(SOL.sol(math.log(SMIN))[1]/SMIN - SMIN/8)                         # q = 1/2 + A s + s^2/16 (y2 = s q')
def q_of(s):
    s = np.asarray(s, float); out = np.empty_like(s); lo = s < SMIN; hi = s > SMAX; md = ~(lo | hi)
    out[lo] = 0.5 + A_IN*s[lo] + s[lo]**2/16; out[hi] = 1/s[hi] - 1/s[hi]**2; out[md] = SOL.sol(np.log(s[md]))[0]; return out
def qp_of(s):                                                                     # dq/ds
    s = np.asarray(s, float); out = np.empty_like(s); lo = s < SMIN; hi = s > SMAX; md = ~(lo | hi)
    out[lo] = A_IN + s[lo]/8; out[hi] = -1/s[hi]**2 + 2/s[hi]**3; out[md] = SOL.sol(np.log(s[md]))[1]/s[md]; return out
def S_of(s):
    s = np.asarray(s, float); out = np.empty_like(s); hi = s > SMAX; lo = ~hi
    out[hi] = 1 - 1/s[hi]; out[lo] = s[lo]*q_of(s[lo]); return out
TAB_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); TAB_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
dS = float(np.max(np.abs(S_of(TAB_s) - TAB_S))); q3 = float(q_of(np.array([1e-3]))[0])
ser = 0.5 + A_IN*1e-2 + 1e-4/16; dser = abs(ser - float(SOL.sol(math.log(1e-2))[0]))
say(f"  solve_bvp status {SOL.status}, nodes {SOL.x.size}, max rel ODE residual {RESID:.1e}; inner slope A = q'(0) = {A_IN:.6f}")
say("  S at " + " ".join(f"{a:g}:{b:.5f}" for a, b in zip(TAB_s, S_of(TAB_s))) + f"   (max |dS| vs CFG691 table {dS:.1e})")
check("M1", SOL.status == 0 and RESID <= 1e-6 and dS <= 1e-3 and abs(q3 - 0.5) <= 1e-3 and dser <= 1e-5,
      f"status {SOL.status}, residual {RESID:.1e}, max|dS| {dS:.1e}, |q(1e-3)-1/2| {abs(q3-0.5):.1e}, series vs solve at 1e-2 {dser:.1e}",
      "status 0; <= 1e-6; <= 1e-3; <= 1e-3; <= 1e-5")
RES["profile"] = dict(A_inner_slope=A_IN, residual=RESID, S_table=S_of(TAB_s).tolist(), max_dS_vs_CFG691=dS)
def lg_of(Mb_kg, a0, Lpc): return (Lpc*PC)**2/(2*np.sqrt(G*np.asarray(Mb_kg, float)/a0))   # metres

# ======================================================================================= F1 (copied from K1, which copied F1, read-only)
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h
def DA_lcdm(z, H0=70.0, Om=0.3):
    zz = np.linspace(0, z, 600); E_ = np.sqrt(Om*(1 + zz)**3 + 1 - Om); return _trap(1/E_, zz)*C/1e3/H0/(1 + z)
HS = {"h0672": 0.672, "h0686": 0.686}
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1])
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
RG = np.logspace(-3, np.log10(30), 3000); RF = np.logspace(np.log10(2e-3), np.log10(3.5), 90); UU = np.linspace(0, 1, 2001)
RGm = RG*MPC
def g_aqual_sph(gN, a0): return 0.5*gN + np.sqrt(0.25*gN**2 + gN*a0)
def project(rho_, r_=RG):
    lr = np.log(r_); pos = rho_ > 0; lrho = np.log(np.where(pos, rho_, 1e-300))
    umax = np.arccosh(r_[-1]/RF); u = UU[None, :]*umax[:, None]; rr = RF[:, None]*np.cosh(u)
    Sig = 2*_trap(np.exp(np.interp(np.log(rr), lr[pos], lrho[pos]))*rr*MPC, u, axis=1)
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return Sig, 2*cum/RF**2 - Sig
def offset(Sig, d):
    if d <= 1e-4: return Sig
    ph_ = np.linspace(0, np.pi, 181); Rp = np.sqrt(RF[:, None]**2 + d**2 + 2*RF[:, None]*d*np.cos(ph_[None, :]))
    return _trap(np.exp(np.interp(np.log(Rp), np.log(RF), np.log(Sig))), ph_, axis=1)/np.pi
def dsig_from_sig(Sig):
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return 2*cum/RF**2 - Sig
def at_bins(ds): return np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(ds, 1e-30))))
def gas_mass(Mg500, R500):
    rc = 0.15*R500; sh = (1 + (RG/rc)**2)**(-1.0); sh[RG > 3.0] = 0
    dm = 4*np.pi*(RG*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(RG*MPC))]
    return M*(Mg500*MSUN/np.interp(R500, RG, M))
PKL = os.path.join(CACHE, "f1_meas.pkl"); SHA = hashlib.sha256(open(PKL, "rb").read()).hexdigest()
MEAS = pickle.load(open(PKL, "rb")); N = len(MEAS)
order = np.argsort([o["ra"] for o in MEAS]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N)*30//N
def arr(key, f): return np.array([o[key][f] for o in MEAS])
def A_band(D, P_, W, sel): return {b: float((W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*P_[sel][:, j]).sum()) for b, j in BANDS.items()}
def jk(D, P_, W):
    full = A_band(D, P_, W, np.ones(N, bool)); reps = [A_band(D, P_, W, PATCH != q) for q in range(30)]
    return {b: (full[b], float(np.sqrt(29/30*np.sum((np.array([x[b] for x in reps]) - np.mean([x[b] for x in reps]))**2)))) for b in full}
DAT = {}
for hk in HS:
    Eh = arr(hk, "E"); DAT[hk] = dict(D=arr(hk, "D"), W=np.where(Eh < 1e8, 1/Eh**2, 0), B=arr(hk, "den").sum(0)/arr(hk, "den_r").sum(0))
def Dd(hk, boost=True): return DAT[hk]["D"]*(DAT[hk]["B"][None, :] if boost else 1.0)
PB = [3, 4, 5, 6, 7]; HARTLAP = (30 - len(PB) - 2)/29
def chi2_prof(hk, P_, boost=True):
    Dx = Dd(hk, boost); W = DAT[hk]["W"]
    f = lambda sel: (W[sel][:, PB]*(Dx[sel][:, PB] - P_[sel][:, PB])).sum(0)/W[sel][:, PB].sum(0)
    s0 = f(np.ones(N, bool)); reps = np.array([f(PATCH != q) for q in range(30)]); Cv = 29/30*(reps - reps.mean(0)).T @ (reps - reps.mean(0))
    return float(HARTLAP*s0 @ np.linalg.solve(Cv, s0))
MB, MISD = {}, {}
for hk, h in HS.items():
    mb, mis = [], []
    for o in MEAS:
        q = (float(DM(o["z"], h))/(1 + o["z"]))/DA_lcdm(o["z"]); mb.append(gas_mass(o["Mgas500"]*q**2.5, o["R500"]*q)*1.20)
        mis.append(np.radians(o["off_deg"])*float(DM(o["z"], h))/(1 + o["z"]))
    MB[hk], MISD[hk] = np.array(mb), np.array(mis)
GL, LAWP = {}, {}
for hk in HS:
    for f in FEET:
        g = g_aqual_sph(G*MB[hk]/RGm**2, A0[f]); GL[(hk, f)] = g; out = []
        for i in range(N):
            ML = g[i]*RGm**2/G; rho_ = np.gradient(ML, RGm)/(4*np.pi*RGm**2); Sig, ds = project(rho_)
            out.append(at_bins(dsig_from_sig(offset(Sig, MISD[hk][i])))/KG_PC2)
        LAWP[(hk, f)] = np.array(out)
F1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json")))
dev = []
for hk in HS:
    for f in FEET:
        a = jk(Dd(hk), LAWP[(hk, f)], DAT[hk]["W"]); ref = F1J["rows"][f"PRIMARY {hk}"][f]
        dev += [abs(a["MID"][0]/ref["MID"][0] - 1), abs(a["OUTER"][0]/ref["OUTER"][0] - 1)]
        say(f"  law {hk} {f:9s}: A_MID {a['MID'][0]:.4f}+-{a['MID'][1]:.4f} (F1 {ref['MID'][0]:.4f})  A_OUTER {a['OUTER'][0]:.4f}+-{a['OUTER'][1]:.4f} (F1 {ref['OUTER'][0]:.4f})")
relieve(); mem("law built")
def interp_weights(xq, xg):
    xq = np.clip(xq, xg[0], xg[-1]); i = np.clip(np.searchsorted(xg, xq) - 1, 0, len(xg) - 2); return i, (xq - xg[i])/(xg[i + 1] - xg[i])
def build_P():
    lr = np.log(RG); Pm = np.zeros((len(RF), len(RG))); umax = np.arccosh(RG[-1]/RF); wu = np.full(len(UU), UU[1] - UU[0]); wu[[0, -1]] *= 0.5
    for j in range(len(RF)):
        u = UU*umax[j]; rr = RF[j]*np.cosh(u); wgt = 2*wu*umax[j]*rr*MPC
        i, t = interp_weights(np.log(rr), lr); np.add.at(Pm[j], i, wgt*(1 - t)); np.add.at(Pm[j], i + 1, wgt*t)
    return Pm
def build_O(d):
    n = len(RF)
    if d <= 1e-4: return np.eye(n)
    O = np.zeros((n, n)); ph_ = np.linspace(0, np.pi, 181); wp = np.full(181, ph_[1] - ph_[0]); wp[[0, -1]] *= 0.5
    for j in range(n):
        Rp = np.sqrt(RF[j]**2 + d**2 + 2*RF[j]*d*np.cos(ph_)); i, t = interp_weights(np.log(Rp), np.log(RF))
        np.add.at(O[j], i, wp*(1 - t)/np.pi); np.add.at(O[j], i + 1, wp*t/np.pi)
    return O
def interp_matrix(xq, xg):
    Mx = np.zeros((len(xq), len(xg))); i, t = interp_weights(xq, xg); Mx[np.arange(len(xq)), i] += 1 - t; Mx[np.arange(len(xq)), i + 1] += t; return Mx
Pm = build_P(); Dm = np.stack([dsig_from_sig(c_) for c_ in np.eye(len(RF))], 1); Bm = interp_matrix(np.log(RC), np.log(RF)); BD = Bm @ Dm
TOP = {}
for hk in HS:
    T_ = np.empty((N, len(RC), len(RG)))
    for i, d in enumerate(MISD[hk]): T_[i] = BD @ build_O(d) @ Pm
    TOP[hk] = T_; relieve()
assert np.isfinite(Pm).all() and np.isfinite(BD).all() and all(np.isfinite(TOP[hk]).all() for hk in HS)
def predW(hk, rhoL): return np.matmul(TOP[hk], np.asarray(rhoL)[..., None])[..., 0]/KG_PC2
def rho_from_M(Mr): return np.gradient(Mr, RGm, axis=-1)/(4*np.pi*RGm**2)
dk6 = []
for hk in HS:
    for f in FEET:
        PL = predW(hk, rho_from_M(GL[(hk, f)]*RGm**2/G)); a1 = jk(Dd(hk), PL, DAT[hk]["W"]); a0_ = jk(Dd(hk), LAWP[(hk, f)], DAT[hk]["W"])
        dk6 += [abs(a1[b][0]/a0_[b][0] - 1) for b in ("MID", "OUTER")]
check("M2", SHA.startswith("961ea4fc") and SHA.endswith("e720") and max(dev) <= 1e-6 and max(dk6) <= 0.005,
      f"sha {SHA[:8]}...{SHA[-4:]}; law vs F1 PRIMARY max rel dev {max(dev):.1e}; linear vs F1 projector {max(dk6):.1e}", "sha; <= 1e-6; <= 0.005")
mem("operators built")

# ======================================================================================= the C2 kernel (K1's, read-only copy)
SMID = np.r_[RG[0]/2, np.sqrt(RG[1:]*RG[:-1])]*MPC
KMAT = np.empty((len(RG), len(SMID)))
for i0 in range(0, len(RG), 200):
    Ri = RGm[i0:i0 + 200, None]; KMAT[i0:i0 + 200] = (1/(2*Ri*SMID[None, :]))*np.log((Ri + SMID[None, :])/np.abs(Ri - SMID[None, :]))
assert np.isfinite(KMAT).all(); relieve()
def c2_fields(Mr, ell):
    Mr = np.atleast_2d(Mr); dm = np.concatenate([Mr[:, :1], np.diff(Mr, axis=1)], axis=1); PhiW = np.empty_like(dm)
    for i0 in range(0, len(dm), 64): PhiW[i0:i0 + 64] = -G*ell*(dm[i0:i0 + 64] @ KMAT.T)
    gin = np.gradient(PhiW, RGm, axis=1); Mdyn = gin*RGm**2/G
    return PhiW, Mdyn, 0.75*rho_from_M(Mdyn)
IREF = int(np.argmin(np.abs(RG - 3.0)))
MBTOT = {hk: MB[hk][:, IREF] for hk in HS}

# ======================================================================================= calibration on F1 MID (S per cluster)
J = BANDS["MID"]
def amid(hk, Ptot, boost=True):
    W = DAT[hk]["W"]; return float((W[:, J]*Dd(hk, boost)[:, J]).sum()/(W[:, J]*Ptot[:, J]).sum())
def lin_cal(hk, f, P1):
    W = DAT[hk]["W"]; return float(((W[:, J]*Dd(hk)[:, J]).sum() - (W[:, J]*LAWP[(hk, f)][:, J]).sum())/(W[:, J]*P1[:, J]).sum())
MD1 = {}; TEMPL = {}; CAL = {}; SCL = {}
for hk in HS:
    _, Md1, rho1 = c2_fields(MB[hk], MPC); MD1[hk] = Md1; TEMPL[(hk, "unscr")] = predW(hk, rho1)
    for f in FEET:
        CAL[(hk, f, "unscr")] = lin_cal(hk, f, TEMPL[(hk, "unscr")])
        for L in LSTARS:
            lg = lg_of(MBTOT[hk], A0[f], L)/MPC; Sx = S_of(RG[None, :]/lg[:, None]); SCL[(hk, f, L)] = dict(lg_pc_median=float(np.median(lg)*1e6),
                                                                                                          max_1mS_r_ge_1kpc=float(np.max(1 - Sx)))
            TEMPL[(hk, f, L)] = predW(hk, 0.75*rho_from_M(Md1*Sx)); CAL[(hk, f, L)] = lin_cal(hk, f, TEMPL[(hk, f, L)]); del Sx
    relieve()
K1J = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "K1_braneworld_weyl", "k1_braneworld_weyl_results.json")))
for hk in HS:
    for f in FEET:
        say(f"  CAL {hk} {f:9s}: l_Q unscreened {CAL[(hk, f, 'unscr')]:.6f} Mpc (K1 {K1J['CAL'][f'C2|{hk}|{f}']['const']:.6f}); screened "
            + "  ".join(f"L*{L:g}: {CAL[(hk, f, L)]:.6f} (median l_g {SCL[(hk, f, L)]['lg_pc_median']:.2e} pc, max 1-S {SCL[(hk, f, L)]['max_1mS_r_ge_1kpc']:.1e})" for L in LSTARS))
mem("calibration")

# ======================================================================================= O1 + compactness
O1 = {}; COMPACT = {}
def o1_eval(hk, f, Ptmpl, cst):
    Pt = LAWP[(hk, f)] + cst*Ptmpl; a = jk(Dd(hk), Pt, DAT[hk]["W"]); c2v = chi2_prof(hk, Pt); zo = (a["OUTER"][0] - 1)/a["OUTER"][1]
    perbin = (Dd(hk)*DAT[hk]["W"]).sum(0)/(Pt*DAT[hk]["W"]).sum(0)
    return dict(A=a, Z_OUTER=zo, chi2_prof=c2v, passes=bool(abs(zo) <= 2 and c2v <= 11.07), data_over_pred_per_bin=perbin.tolist())
for hk in HS:
    for f in FEET:
        O1[(hk, f, "unscr")] = o1_eval(hk, f, TEMPL[(hk, "unscr")], CAL[(hk, f, "unscr")])
        for L in LSTARS:
            r_ = o1_eval(hk, f, TEMPL[(hk, f, L)], CAL[(hk, f, L)]); O1[(hk, f, L)] = r_; a = r_["A"]
            say(f"  O1 {hk} {f:9s} L*{L:g}: A_INNER {a['INNER'][0]:.3f}  A_MID {a['MID'][0]:.3f}  A_OUTER {a['OUTER'][0]:.3f}+-{a['OUTER'][1]:.3f} "
                f"(Z {r_['Z_OUTER']:+.2f})  chi2_prof {r_['chi2_prof']:.2f} (line 11.07) -> {'PASS' if r_['passes'] else 'FAIL'}   data/pred per bin "
                + " ".join(f"{x:.2f}" for x in r_["data_over_pred_per_bin"]))
            if hk == "h0672":
                lg = lg_of(MBTOT[hk], A0[f], L)/MPC; MLW = 0.75*CAL[(hk, f, L)]*MD1[hk]*S_of(RG[None, :]/lg[:, None]); gas = MB[hk]/1.2; out = {}
                for rv in (0.5, 1.0, 2.0, 3.0):
                    jx = int(np.argmin(np.abs(RG - rv))); out[f"{rv}"] = float(np.median(MLW[:, jx]/gas[:, jx]))
                COMPACT[(f, L)] = out; del MLW
say("  compactness, M_lens,W / M_gas (median cluster, h 0.672) at 0.5/1/2/3 Mpc: " + "; ".join(f"{f} L*{L:g}: " + "/".join(f"{v:.2f}" for v in COMPACT[(f, L)].values()) for f in FEET for L in LSTARS)
    + "   (needed: ~1.4-1.8 inside 1 Mpc, ~0 beyond)")
relieve(); mem("O1")

# ======================================================================================= R1 isolated galaxies (F2 masses; K1 A3 point-source formula)
LMB = [10.36, 10.83, 11.01, 11.18]; BPL = 5*KPC; MGALKG = np.array([10**lm*MSUN for lm in LMB])
RB = {"O1": np.logspace(np.log10(0.4), np.log10(1.1), 25), "O2": np.logspace(np.log10(1.1), np.log10(2.6), 25)}
GOP = Dm @ Pm; SAMP = {b: interp_matrix(np.log(R_), np.log(RF)) for b, R_ in RB.items()}
MGAL = np.array([10**lm*MSUN*RGm**3/(RGm**2 + BPL**2)**1.5 for lm in LMB])
def band_int(rho_rows, Min):
    ds = rho_rows @ GOP.T + np.asarray(Min)[:, None]/(np.pi*(RF*MPC)**2)
    return {b: _trap(ds @ SAMP[b].T, np.log(RB[b]), axis=1) for b in RB}
LAWGAL = {}
for f in FEET:
    gl_ = g_aqual_sph(G*MGAL/RGm**2, A0[f]); LAWGAL[f] = band_int(rho_from_M(gl_*RGm**2/G), gl_[:, 0]*RGm[0]**2/G)
def r1_ratios(f, cst, L):
    out, oneminus = {}, 0.0
    for b, R_ in RB.items():
        Sx = np.ones((len(LMB), len(R_))) if L is None else S_of((R_[None, :]*MPC)/lg_of(MGALKG, A0[f], L)[:, None])
        oneminus = max(oneminus, float(np.max(1 - Sx)))
        out[b] = (_trap((9/16)*MGALKG[:, None]*cst*MPC*Sx/(R_[None, :]*MPC)**3, np.log(R_), axis=1)/LAWGAL[f][b]).tolist()
    return out, oneminus
R1 = {}
for hk in HS:
    for f in FEET:
        R1[(hk, f, "unscr")] = r1_ratios(f, CAL[(hk, f, "unscr")], None)[0]
        for L in LSTARS:
            rat, om = r1_ratios(f, CAL[(hk, f, L)], L); mx = max(max(abs(x) for x in rat[b]) for b in rat)
            R1[(hk, f, L)] = dict(ratios=rat, max=mx, max_1mS=om, passes=mx <= 0.14)
            say(f"  R1 {hk} {f:9s} L*{L:g}: Weyl/law O1 " + " ".join(f"{x:.3f}" for x in rat["O1"]) + "  O2 " + " ".join(f"{x:.3f}" for x in rat["O2"])
                + f"  (max 1-S {om:.1e}) -> {'PASS' if mx <= 0.14 else 'FAIL'} (max {mx:.3f} vs 0.14)")
mem("R1")

# ======================================================================================= R3 dwarf satellites (E3 CSV; A1 baseline)
E3R = list(csv.DictReader(open(os.path.join(REPO, "doors_push_2026_10_22", "E3_dwarf_excess", "e3_per_system.csv"))))
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for x in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn))):
        def fl(v):
            try: return float(v)
            except Exception: return np.nan
        LVD[x["name"]] = (fl(x["distance_gc"]), fl(x["distance_m31"]))
# E3's own B_scr recipe (e3_dwarf_excess.py L19-62, copied read-only with E3's constants)
G3, MSUN3, PC3 = 6.67430e-11, 1.989e30, 3.0856775814913673e16
def nu3(y): y = np.maximum(np.asarray(y, float), 1e-30); return 0.5*(1.0 + np.sqrt(1.0 + 4.0/y))
def S3(s):
    s = np.asarray(s, float); out = np.interp(np.log(np.clip(s, 0.01, 1000)), np.log(TAB_s), TAB_S); out = np.where(s <= 0.01, s/2, out)
    return np.where(s >= 1000, 1 - 1/np.maximum(s, 1e-300), out)
def B_scr3(Ms, r12, a0, Lpc):
    gb = G3*(Ms/2)*MSUN3/r12**2; nv = nu3(gb/a0); rM = np.sqrt(G3*Ms*MSUN3/a0); lg = (Lpc*PC3)**2/(2*rM); return 1 + S3(r12/lg)*(nv - 1)
MWM, M31M, AH, R0 = 6.0e10*MSUN, 1.0e11*MSUN, 3*KPC, 8.122*KPC
DW = {}; m4 = {}
for f in FEET:
    rows = [x for x in E3R if x["footing"] == f]
    Ms_ = 10**np.array([float(x["logMstar"]) for x in rows]); r12 = (4/3)*np.array([float(x["rh_pc"]) for x in rows])*PC
    r12_3 = (4/3)*np.array([float(x["rh_pc"]) for x in rows])*PC3
    Md = np.array([float(x["M_dyn"]) for x in rows]); Bcsv = np.array([float(x["B_scr_L24"]) for x in rows])
    Bc = {L: B_scr3(Ms_, r12_3, A0[f], L) for L in LSTARS}; d24 = np.abs(np.log10(Bc[24.0]/Bcsv))
    m4[f] = (float(np.median(d24)), float(np.max(d24)))
    host = [x["host"] for x in rows]; dist = np.array([LVD[x["name"]][1] if x["host"] == "M31" else LVD[x["name"]][0] for x in rows])*KPC
    Mp = {L: (Bcsv if L == 24.0 else Bcsv*Bc[L]/Bc[24.0])*Ms_/2 for L in LSTARS}
    DW[f] = dict(names=[x["name"] for x in rows], Ms=Ms_, r12=r12, Md=Md, Mp=Mp, host=host, dist=dist, base={L: np.log10(Md/Mp[L]) for L in LSTARS})
k9 = {f: float(np.median(DW[f]["base"][24.0])) for f in FEET}; K9REF = K1J["K9_baseline"]
check("M4", all(m4[f][0] <= 0.02 and m4[f][1] <= 0.10 for f in FEET) and all(abs(k9[f] - K9REF[f]) <= 1e-4 for f in FEET),
      f"E3 central B_scr(24) vs CSV: median/max |dlog| canonical {m4['canonical'][0]:.4f}/{m4['canonical'][1]:.4f}, alt {m4['alt'][0]:.4f}/{m4['alt'][1]:.4f}; "
      f"baseline medians {k9['canonical']:+.5f}/{k9['alt']:+.5f} vs K1 {K9REF['canonical']:+.5f}/{K9REF['alt']:+.5f}", "<= 0.02/0.10 dex; <= 1e-4 dex")
_, MdU, _ = c2_fields((MSUN*RG**3/(RG**2 + 1)**1.5)[None, :], MPC); FX = float(np.interp(1.305, RG, MdU[0]/MSUN))
def dwarf_MW(f, cst, L):
    d = DW[f]; own = np.zeros(len(d["Md"])); hst = np.zeros(len(d["Md"])); Ssat = np.ones(len(d["Md"]))
    for i in range(len(own)):
        Mh = M31M if d["host"][i] == "M31" else MWM; b_ = d["r12"][i]/1.305
        if L is not None: Ssat[i] = float(S_of(np.array([d["r12"][i]/lg_of(d["Ms"][i]*MSUN, A0[f], L)]))[0])
        own[i] = cst*MPC*d["Ms"][i]*MSUN*FX/b_*Ssat[i]/MSUN
        hst[i] = (4*np.pi/3)*d["r12"][i]**3*(-cst*MPC*Mh/(2*np.pi*d["dist"][i]**4))/MSUN
    return own + hst, Ssat
R3 = {}
for hk in HS:
    for f in FEET:
        for L in (("unscr",) + LSTARS):
            Lb = 24.0 if L == "unscr" else L; MWd, Ssat = dwarf_MW(f, CAL[(hk, f, L)], None if L == "unscr" else L); d = DW[f]
            arg = 1 + MWd/d["Mp"][Lb]; rnew = d["base"][Lb] - np.log10(np.where(arg > 0, arg, np.nan)); med = float(np.nanmedian(rnew))
            R3[(hk, f, L)] = dict(median=med, baseline=float(np.median(d["base"][Lb])), median_S_sat=float(np.median(Ssat)),
                                  S_sat_range=[float(Ssat.min()), float(Ssat.max())], median_MW_over_Mpred=float(np.median(MWd/d["Mp"][Lb])),
                                  passes=abs(med) <= 0.26, n_nan=int(np.isnan(rnew).sum()))
            if L != "unscr":
                say(f"  R3 {hk} {f:9s} L*{L:g}: baseline {R3[(hk, f, L)]['baseline']:+.3f} dex; S(r12/l_g) median {np.median(Ssat):.3f} (range {Ssat.min():.3f}-{Ssat.max():.3f}); "
                    f"C2 mass x{np.median(MWd/d['Mp'][Lb]):.2e} of the screened prediction; residual -> {med:+.3f} dex -> {'PASS' if abs(med) <= 0.26 else 'FAIL'}")
mem("R3")

# ======================================================================================= Galactic C2 tide (A1: adaptive quadrature of K1's shell kernel)
def phiW_quad(R, rho_fn, ell, rmax):
    f_ = lambda s: 4*np.pi*s**2*rho_fn(s)*(1/(2*R*s))*math.log((R + s)/abs(R - s)) if s != R else 0.0
    v1 = quad(f_, 0, R, points=None, limit=400, epsabs=0, epsrel=1e-12)[0]
    v2 = quad(f_, R, 10*R, limit=400, epsabs=0, epsrel=1e-12)[0]; v3 = quad(f_, 10*R, rmax, limit=400, epsabs=0, epsrel=1e-12)[0]
    return -G*ell*(v1 + v2 + v3)
def tide(R, rho_fn, ell, rmax):
    hh = 1e-2*R; p = [phiW_quad(R + k*hh, rho_fn, ell, rmax) for k in (-1, 0, 1)]
    d1 = (p[2] - p[0])/(2*hh); d2 = (p[2] - 2*p[1] + p[0])/hh**2
    return dict(phi=p[1], d1=d1, d2=d2, Q2=d2 - d1/R, lap=d2 + 2*d1/R)
bP = 5*KPC; MP = 1e10*MSUN; rhoP = lambda s: 3*MP/(4*np.pi*bP**3)*(1 + (s/bP)**2)**-2.5
tP = tide(100*bP, rhoP, MPC, 1e4*bP); exactP = -8*G*MP*MPC/(100*bP)**4; d6 = abs(tP["Q2"]/exactP - 1)
check("M6", d6 <= 1e-2, f"Plummer b = 5 kpc at R = 100 b: (Phi'' - Phi'/R)/(-8 G M l/R^4) - 1 = {d6:.1e}", "<= 1e-2")
rhoMW = lambda s: MWM*AH/(2*np.pi*s*(s + AH)**3)
TMW_unit = tide(R0, rhoMW, MPC, 1e3*R0)                                           # per l_Q = 1 Mpc (linear in l_Q)
say(f"  MW (Hernquist 6e10, a = 3 kpc) C2 tide at R0 per l_Q = 1 Mpc: Phi'' {TMW_unit['d2']:.3e}, Phi'/R {TMW_unit['d1']/R0:.3e}, Q2 = Phi''-Phi'/R {TMW_unit['Q2']:.3e} s^-2, "
    f"rho_eff = lap/(4 pi G) {TMW_unit['lap']/(4*np.pi*G):.3e} kg/m^3")

# ======================================================================================= R5 Solar System, R6 wide binaries
GMS = G*MSUN; ME = 3.0035e-6*MSUN; MWB = 1.5*MSUN
PLB = {"Earth": (1.0*AU, 8.7e-15), "Mars": (1.524*AU, 1.4e-15), "Saturn": (9.58*AU, 7.0e-15)}
c6src = open(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini.py")).read()
assert '"Mars": (1.524 * AU, 1.4e-15)' in c6src and '"Earth": (1.0 * AU, 8.7e-15)' in c6src and '"Saturn": (9.58 * AU, 7.0e-15)' in c6src
HEES, PARK = 9.0e-27, 5.2e-27
def own_terms(M, ellm, lg, r):
    s = np.asarray(r, float)/lg; q = q_of(s); qp = qp_of(s)
    dg = 2*G*M*ellm*q/(np.asarray(r)**2*lg)                                       # sunward (attractive) screened C2 acceleration
    dgeq = G*M*ellm*qp/(np.asarray(r)*lg**2)                                      # (1/2r) d(r^2 dg)/dr
    return dg, dgeq, 2*(ellm/lg)*q                                                # last: g/g_N - 1 from this term
# M5: screened point mass limits
lgT = 1.0; ellT = 3.0
dgT, dgeqT, _ = own_terms(1/G, ellT, lgT, np.array([1e-4]))
m5a = abs(dgT[0]*1e-8/(ellT/lgT) - 1)                                             # g r^2/(GM l/l_g) = 2 q -> 1
fd = []
for sv in (1e-3, 1e-1):
    rr = np.array([sv*(1 - 1e-4), sv, sv*(1 + 1e-4)]); dgx, dgeqx, _ = own_terms(1/G, ellT, lgT, rr)
    num = (rr[2]**2*dgx[2] - rr[0]**2*dgx[0])/(rr[2] - rr[0])/(2*rr[1]); fd.append(abs(num/dgeqx[1] - 1))
check("M5", m5a <= 1e-3 and max(fd) <= 1e-3, f"2q(1e-4) - 1 = {m5a:.1e}; finite-difference dg_eq vs analytic at s = 1e-3, 1e-1: {fd[0]:.1e}, {fd[1]:.1e}", "<= 1e-3; <= 1e-3")
R5 = {}; R6 = {}
for hk in HS:
    for f in FEET:
        for L in (("unscr",) + LSTARS):
            ellm = CAL[(hk, f, L)]*MPC
            if L == "unscr":
                R5[(hk, f, L)] = dict(raw_ratio_Mars=float(2*G*MSUN*ellm/PLB["Mars"][0]**3/PLB["Mars"][1])); continue
            lgS = float(lg_of(MSUN, A0[f], L)); tid = {k: v*CAL[(hk, f, L)] for k, v in TMW_unit.items()}
            rho_eff = tid["lap"]/(4*np.pi*G); rats, raw, parts = {}, {}, {}
            for nm, (rr, bd) in PLB.items():
                dg, dgeq, _ = own_terms(MSUN, ellm, lgS, np.array([rr])); dgM = (4*np.pi/3)*G*rho_eff*rr; dgeqM = 1.5*dgM
                rats[nm] = float(abs(dgeq[0] + dgeqM)/bd); raw[nm] = float(abs(dg[0] + dgM)/bd); parts[nm] = dict(own_eq=float(dgeq[0]), MW_eq=float(dgeqM))
            q2 = abs(tid["Q2"]); pa = all(v < 1 for v in rats.values()); pb = q2 < HEES
            own_mars = abs(parts["Mars"]["own_eq"]); room = PLB["Mars"][1] - abs(parts["Mars"]["MW_eq"])
            L_need = L*(own_mars/room)**0.25 if room > 0 else float("inf")
            geff = {nm: float(own_terms(M, ellm, float(lg_of(M, A0[f], L)), np.array([rr]))[2][0])
                    for nm, M, rr in (("Sun_1AU", MSUN, AU), ("Earth_Moon_orbit", ME, 3.844e8), ("binary1p5_20kAU", MWB, 2e4*AU))}
            R5[(hk, f, L)] = dict(dg_eq_over_bound=rats, raw_over_bound=raw, parts=parts, Q2=q2, Q2_over_Hees=q2/HEES, Q2_over_Park=q2/PARK,
                                  rho_eff_MW_at_Sun=rho_eff, l_g_Sun_pc=lgS/PC, G_eff_minus_1=geff, Lstar_needed_Mars_pc=L_need,
                                  passes_a=pa, passes_b=pb)
            # R6 wide binaries
            lgB = float(lg_of(MWB, A0[f], L)); _, _, x_cal = own_terms(MWB, ellm, lgB, np.array([AU])); out = {}
            for sep in (5e3, 2e4):
                rr = sep*AU; _, _, xs = own_terms(MWB, ellm, lgB, np.array([rr])); gN = G*MWB/rr**2
                tau = max(abs(tid["d2"]), abs(tid["d1"]/R0))*rr/gN; ratio = (1 + xs[0])/(1 + x_cal[0])
                gv = max(abs(math.sqrt(ratio + tau) - 1), abs(math.sqrt(max(ratio - tau, 0)) - 1))
                out[f"{sep:g}AU"] = dict(gamma_v_minus_1=gv, own_ratio_minus_1=float(ratio - 1), tide_over_gN=tau,
                                         uncalibrated_gamma_v=float(math.sqrt(1 + xs[0])))
            R6[(hk, f, L)] = dict(seps=out, passes=all(abs(v["gamma_v_minus_1"]) <= 0.25 for v in out.values()))
            say(f"  R5 {hk} {f:9s} L*{L:g}: l_g(Sun) {lgS/PC:.3e} pc; dg_eq/bound Earth {rats['Earth']:.2e} Mars {rats['Mars']:.2e} Saturn {rats['Saturn']:.2e} "
                f"(raw |dg|/bound Mars {raw['Mars']:.2e}) -> R5a {'PASS' if pa else 'FAIL'};  Q2 {q2:.2e} s^-2 = {q2/HEES:.2e} Hees, {q2/PARK:.2e} Park -> R5b {'PASS' if pb else 'FAIL'};"
                f"  G_eff/G-1: Sun {geff['Sun_1AU']:.3g}, Earth {geff['Earth_Moon_orbit']:.3g}; L* for Mars {L_need:.0f} pc")
            say(f"  R6 {hk} {f:9s} L*{L:g}: wide binary 1.5 Msun gamma_v-1 at 5 kAU {out['5000AU']['gamma_v_minus_1']:.2e}, 20 kAU {out['20000AU']['gamma_v_minus_1']:.2e} "
                f"(own term rel. to 1 AU {out['20000AU']['own_ratio_minus_1']:.1e}, Galactic C2 tide/g_N {out['20000AU']['tide_over_gN']:.2e}); "
                f"against masses not calibrated dynamically gamma_v = {out['20000AU']['uncalibrated_gamma_v']:.2f} -> {'PASS' if R6[(hk, f, L)]['passes'] else 'FAIL'}")
mem("R5/R6")

# ======================================================================================= M3: K1 reproduction (S = 1)
m3 = []
for hk in HS:
    for f in FEET:
        k1o = K1J["O1"][f"C2|{hk}|{f}"]; mine = O1[(hk, f, "unscr")]
        m3 += [("lQ", abs(CAL[(hk, f, "unscr")]/K1J["CAL"][f"C2|{hk}|{f}"]["const"] - 1), 1e-6),
               ("A_OUTER", abs(mine["A"]["OUTER"][0]/k1o["A"]["OUTER"][0] - 1), 1e-6),
               ("chi2", abs(mine["chi2_prof"]/k1o["chi2_prof"] - 1), 1e-4),
               ("R3", abs(R3[(hk, f, "unscr")]["median"] - K1J["R3"][f"C2|{hk}|{f}"]["median"]), 1e-6),
               ("R5", abs(R5[(hk, f, "unscr")]["raw_ratio_Mars"]/K1J["R5"][f"C2|{hk}|{f}"]["ratios"]["Mars"] - 1), 1e-6)]
worst = {}
for nm, v, thr in m3: worst[nm] = max(worst.get(nm, 0.0), v)
check("M3", all(v <= thr for _, v, thr in m3), "max deviations vs K1 C2: " + ", ".join(f"{k} {v:.1e}" for k, v in worst.items()),
      "l_Q, A_OUTER, R5 <= 1e-6 rel; chi2 <= 1e-4 rel; R3 <= 1e-6 dex")

# ======================================================================================= R7 cosmology (reported)
say("\n=== R7: cosmology (reported only) ===")
OM, HH, WB_, WC_ = 0.2976015949416498, 0.6856426703851345, 0.022208778152980592, 0.1170701352888568   # E-886 (C2 L115-116)
FB = WB_/(WB_ + WC_)
def growth(kh, ellMpc, Om=OM, a_i=0.01):
    Ef = lambda a: math.sqrt(Om*a**-3 + (1 - Om))
    def rhs(x, y):
        a = math.exp(x); E2 = Ef(a)**2; dlnE = -1.5*Om*a**-3/E2; om_a = Om*a**-3/E2
        boost = 1 + FB*(math.pi/2)*(kh*HH/a)*ellMpc
        return [y[1], -(2 + dlnE)*y[1] + 1.5*om_a*boost*y[0]]
    sol = solve_ivp(rhs, (math.log(a_i), 0.0), [a_i, a_i], rtol=1e-10, atol=1e-14, dense_output=True)
    return sol
s7 = growth(0.1, 0.0, Om=1.0); xs7 = np.linspace(math.log(0.01), 0, 50); Dv = s7.sol(xs7)[0]/np.exp(xs7)
d7 = float(np.max(np.abs(Dv/Dv[0] - 1)))
check("M7", d7 <= 1e-4, f"EdS, l_Q = 0: max |D/a / (D/a)_i - 1| = {d7:.1e}", "<= 1e-4")
ellc = CAL[("h0672", "canonical", 24.0)]; R7 = dict(l_Q_Mpc=ellc, f_b=FB, background="(-Lap)^(1/2) of a constant density is zero (k = 0 mode): rho_eff,bar = 0",
                                                    G_eff_minus_1={}, D_ratio={})
for kh in (0.01, 0.1, 1.0):
    R7["G_eff_minus_1"][f"{kh:g}"] = dict(z0=FB*(math.pi/2)*kh*HH*ellc, z1100=FB*(math.pi/2)*kh*HH*1101*ellc)
    Dw = growth(kh, ellc).y[0, -1]; Dg = growth(kh, 0.0).y[0, -1]; R7["D_ratio"][f"{kh:g}"] = Dw/Dg
    say(f"  k = {kh:g} h/Mpc: G_eff/G - 1 = {R7['G_eff_minus_1'][f'{kh:g}']['z0']:.3f} (z = 0), {R7['G_eff_minus_1'][f'{kh:g}']['z1100']:.3e} (z = 1100); "
        f"D_W/D_GR(z = 0, from z = 99) = {Dw/Dg:.4g}")
R7["growth_breaking"] = bool(R7["D_ratio"]["0.1"] - 1 > 0.1)
say(f"  background: homogeneous mode zero -> no Delta N_eff, no H(z) change (BBN-safe at the background level); "
    f"growth: D_W/D_GR - 1 at 0.1 h/Mpc = {R7['D_ratio']['0.1'] - 1:.3g} -> {'GROWTH-BREAKING on linear scales unless absent on FRW' if R7['growth_breaking'] else 'small'}")

# ======================================================================================= verdict (frozen rule)
say("\n=== VERDICT (frozen rule) ===")
VER = {}
for L in LSTARS:
    for f in FEET:
        cal = all(np.isfinite(CAL[(hk, f, L)]) and CAL[(hk, f, L)] > 0 for hk in HS)
        o1 = all(O1[(hk, f, L)]["passes"] for hk in HS); r1 = all(R1[(hk, f, L)]["passes"] for hk in HS)
        r3 = all(R3[(hk, f, L)]["passes"] for hk in HS); r5a = all(R5[(hk, f, L)]["passes_a"] for hk in HS)
        r5b = all(R5[(hk, f, L)]["passes_b"] for hk in HS); r6 = all(R6[(hk, f, L)]["passes"] for hk in HS)
        VER[f"L{L:g}|{f}"] = dict(CAL=cal, O1=o1, R1=r1, R3=r3, R5a=r5a, R5b=r5b, R6=r6)
        say(f"  L*{L:g} {f:9s}: CAL {cal}  O1 {o1}  R1 {r1}  R3 {r3}  R5a {r5a}  R5b {r5b}  R6 {r6}")
def both(L, k): return all(VER[f"L{L:g}|{f}"][k] for f in FEET)
works = any(all(both(L, k) for k in ("CAL", "O1", "R1", "R3", "R5a", "R5b", "R6")) for L in LSTARS)
part = any(both(L, "CAL") and ((both(L, "O1") and any(both(L, k) for k in ("R3", "R5a", "R6")))
                               or (not both(L, "O1") and all(both(L, k) for k in ("R1", "R3", "R5a", "R5b", "R6")))) for L in LSTARS)
OVER = "WORKS" if works else ("PARTIAL" if part else "FAILS")
say(f"OVERALL VERDICT: {OVER}")
def key(k): return "|".join(str(x) for x in k) if isinstance(k, tuple) else k
RES.update(cache_sha256=SHA, N=N, CAL={key(k): v for k, v in CAL.items()}, screening_clusters={key(k): v for k, v in SCL.items()},
           O1={key(k): v for k, v in O1.items()}, compactness={key(k): v for k, v in COMPACT.items()}, R1={key(k): v for k, v in R1.items()},
           R3={key(k): v for k, v in R3.items()}, R5={key(k): v for k, v in R5.items()}, R6={key(k): v for k, v in R6.items()}, R7=R7,
           MW_tide_per_lQ_1Mpc=TMW_unit, M4_B_scr_dlog=m4, unit_plummer_FX=FX, verdict_cells=VER, verdict=OVER)
npass = sum(ok for _, ok in CHECKS); mem("end")
say(f"M2_CLUSTER_COMPACT COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"m2_cluster_compact_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else (bool(o) if isinstance(o, np.bool_) else str(o))))
sys.exit(0 if npass == len(CHECKS) else 1)
