#!/usr/bin/env python3
"""GAL1: what growth and CMB lensing allow for the volume law-on regions fill, as a history f(z).
Criteria b6f30f6460, amendment A1 2a8a04b3e0. TEST lane, quarantined; adopts nothing. kappa = 1/2 FITTED; not theory closed.
One thread. Usage: python3 gal1.py [--mutate sign|potonly]

Read-only reuse: QX3 iter2 (run_class, X_of, best_amp_chi2, limber_ratio; PR4 via cfg917_lib), cfg917_lib.limber_X (KA4c),
SWT1 swt1.py (radii tables and `compensated`, executed up to `RES = dict(`).
"""
import os, sys, json, math, time, io, contextlib, types
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline, RegularGridInterpolator
from scipy.optimize import brentq
if not hasattr(np, "trapz"): np.trapz = np.trapezoid

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = sys.argv[sys.argv.index("--mutate") + 1] if "--mutate" in sys.argv else None
assert MUT in (None, "sign", "potonly")
TAG = "gal1" if MUT is None else f"gal1_MUTATE_{MUT}"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

# ------------------------------------------------------------------ record's machinery (read-only)
I2D = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust")
sys.path.insert(0, I2D)
with contextlib.redirect_stdout(io.StringIO()):
    import iter2 as I2                      # loads PR4 (cfg917_lib) at import
LIB, DPR4 = I2.LIB, I2.D
OB, OD, H0, NS = 0.0215, 0.11958060485606123, 65.0, 0.95
h = H0 / 100.0; OMCL = (OB + OD) / h ** 2
M = I2.run_class(OB, OD, H0, NS, pk=True)
X0 = I2.X_of(M)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
F_SWT1 = 0.0231
RES = dict(lane="GAL1", criteria="b6f30f6460", amendment_A1="2a8a04b3e0", tag=TAG, mutate=MUT,
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, rows={}, histories={}, allowances={},
           readings={}, reported={}, labels={}, MUTATE={})
P(f"GAL1 {'MUTATE ' + MUT + ' ' if MUT else ''}run. Background omega_b {OB} omega_d {OD:.6f} H0 {H0} n_s {NS} (QX3 iter2 corner); "
  f"Omega_cl {OMCL:.5f}")

# ------------------------------------------------------------------ KA1: the record's PR4 row
def amp_fit(X):
    u = LIB.wsum(DPR4["W"], X) + LIB.wsum(DPR4["M"], X)
    a = LIB.qform(u, DPR4["Cinv"], DPR4["d"] + DPR4["F"]); b = LIB.qform(u, DPR4["Cinv"]); A = a / b
    r = A * u - DPR4["F"] - DPR4["d"]
    return dict(A=A, sig_abs=1.0 / math.sqrt(b), chi2_refit=LIB.qform(r, DPR4["Cinv"]))
FX0 = amp_fit(X0)
AX0, SIGREL = FX0["A"], FX0["sig_abs"] / FX0["A"]
sv5 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "SV5_growth_mechanism", "sv5_t0.json")))
it2 = json.load(open(os.path.join(I2D, "iter2.json")))
c2ref = max(it2["G1"], key=lambda r: r["chi2_min"])["chi2_min"]
ka1 = dict(A_X0=AX0, A_X0_record=sv5["A_X0"], sigma_A_rel=SIGREL, sigma_A_rel_record=sv5["sigma_A_rel"], chi2_X0=FX0["chi2_refit"],
           chi2_record=c2ref, rel=[abs(AX0 / sv5["A_X0"] - 1), abs(SIGREL / sv5["sigma_A_rel"] - 1), abs(FX0["chi2_refit"] / c2ref - 1)])
ka1["pass_"] = bool(ka1["rel"][0] <= 1e-6 and ka1["rel"][1] <= 1e-6 and ka1["rel"][2] <= 1e-3)
RES["KA"]["KA1"] = ka1
P(f"KA1 PR4 row: A_X0 {AX0:.7f} (record {sv5['A_X0']:.7f}), sigma_A,rel {SIGREL:.7f} (record {sv5['sigma_A_rel']:.7f}), chi2 {FX0['chi2_refit']:.4f} "
  f"(record {c2ref:.4f}); rel {ka1['rel'][0]:.1e} / {ka1['rel'][1]:.1e} / {ka1['rel'][2]:.1e} -> {'PASS' if ka1['pass_'] else 'FAIL'}")
LINE2 = 2 * SIGREL; LINE3 = 3 * SIGREL
S8LINE = 2 * 0.0225 / 0.759
APHI2 = 0.062                                   # reported only: CMB3 A_phi scan, own interpolation
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]   # CE2 ce2.py
RES["rows"] = dict(cmb_lensing=dict(row="PR4 amplitude of the reference X0 (SV5 T0.4)", A_X0=AX0, sigma_A_rel=SIGREL, line_2sig=LINE2, line_3sig=LINE3),
                   fsigma8=dict(row="DESI DR1 Table 9 ratios as CE2 transcribed (ShapeFit / ShapeFit+BAO), errors symmetrised",
                                rows=[dict(bin=t, z=z, sf=r1, e_sf=0.5 * (p1 + m1), sfb=r2, e_sfb=0.5 * (p2 + m2)) for (t, z, r1, p1, m1, r2, p2, m2) in DESI]),
                   S8=dict(row="KiDS-1000 S8 0.759 +- 0.0225 (SS4 CS line)", line=S8LINE))
P(f"Rows: lensing |r_eff - 1| <= {LINE2:.6f} (2 sigma; 3 sigma {LINE3:.6f}); f sigma8 DESI DR1 four bins x two panels at 2 err; S8 |s - 1| <= {S8LINE:.5f}")

# ------------------------------------------------------------------ background and growth ODE
ZI = 30.0
lna_t = np.linspace(math.log(1 / (1 + ZI)) - 0.01, 0.0, 6001)
lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t])
SPH = CubicSpline(lna_t, lnH_t); SPHd = SPH.derivative()
H0c = M.Hubble(0.0)
def Om_cl(lna): return OMCL * math.exp(-3 * lna) * (H0c / math.exp(float(SPH(lna)))) ** 2
def dlnH(lna): return float(SPHd(lna))
def ode_rhs(qfun, Ofun, dfun):
    def rhs(lna, y):
        return [y[1], -(2 + dfun(lna)) * y[1] + 1.5 * Ofun(lna) * (1 + qfun(lna)) * y[0]]
    return rhs
def integrate(qfun, Ofun, dfun, lna0, y0, lna_eval, breaks):
    """piecewise in ln a between breakpoints (steps / knots of q); returns delta and delta' at lna_eval (sorted increasing)."""
    lna_eval = np.asarray(lna_eval); edges = sorted(set([lna0] + [b for b in breaks if lna0 < b < lna_eval[-1]] + [float(lna_eval[-1])]))
    y = np.array(y0, float); outD = np.empty(len(lna_eval)); outV = np.empty(len(lna_eval))
    rhs = ode_rhs(qfun, Ofun, dfun)
    for a_, b_ in zip(edges[:-1], edges[1:]):
        m = (lna_eval >= a_) & (lna_eval <= b_)
        te = lna_eval[m]
        so = solve_ivp(rhs, (a_, b_), y, t_eval=te if te.size else None, rtol=1e-11, atol=1e-14, method="DOP853")
        if te.size: outD[m] = so.y[0]; outV[m] = so.y[1]
        y = so.y[:, -1]
    return outD, outV

DCL = lambda z: M.scale_independent_growth_factor(z)
FCL = lambda z: M.scale_independent_growth_factor_f(z)
Y0 = [DCL(ZI), FCL(ZI) * DCL(ZI)]
LNA0 = math.log(1 / (1 + ZI))

# KA2
ZK2 = [0.0, 0.295, 0.51, 0.706, 0.919, 1.5, 2.0, 3.0]
lnk2 = np.sort(np.log(1 / (1 + np.array(ZK2))))
d2, v2 = integrate(lambda x: 0.0, Om_cl, dlnH, LNA0, Y0, lnk2, [])
z2 = 1 / np.exp(lnk2) - 1; D0m = d2[-1]; S80 = M.sigma8(); R8 = 8.0 / h
rows2 = []
for zz, dd, vv in zip(z2, d2, v2):
    myD = dd / D0m; myf = vv / dd; myfs8 = myf * myD * S80
    clD = DCL(zz) / DCL(0.0); clf = FCL(zz); clfs8 = clf * M.sigma(R8, zz)
    rows2.append(dict(z=float(zz), D=myD, D_class=clD, f=myf, f_class=clf, fs8=myfs8, fs8_class=clfs8,
                      rel=max(abs(myD / clD - 1), abs(myf / clf - 1), abs(myfs8 / clfs8 - 1))))
ka2 = max(r["rel"] for r in rows2)
RES["KA"]["KA2"] = dict(rows=rows2, max_rel=ka2, pass_=bool(ka2 <= 2e-3))
P(f"KA2 G_eff = G vs CLASS growth (D/D0, f, f sigma8 at z {', '.join(f'{z:g}' for z in ZK2)}): max rel {ka2:.2e} -> {'PASS' if ka2 <= 2e-3 else 'FAIL'}")
P("     f sigma8 mine / CLASS: " + ", ".join(f"z {r['z']:.3f} {r['fs8']:.5f}/{r['fs8_class']:.5f}" for r in rows2))

# KA3
rows3 = []
for q in (0.0, 0.05, 0.3, -0.2):
    d, v = integrate(lambda x: q, lambda x: 1.0, lambda x: -1.5, 0.0, [1.0, 0.3], np.array([20.0]), [])
    p_ex = (-1 + math.sqrt(1 + 24 * (1 + q))) / 4; slope = float(v[0] / d[0])
    rows3.append(dict(q=q, slope=slope, p=p_ex, err=abs(slope - p_ex)))
ka3 = max(r["err"] for r in rows3)
RES["KA"]["KA3"] = dict(rows=rows3, max_err=ka3, pass_=bool(ka3 <= 1e-6))
P("KA3 EdS growth index: " + ", ".join(f"q {r['q']:+.2f}: {r['slope']:.8f} vs {r['p']:.8f}" for r in rows3) + f"; max err {ka3:.1e} -> {'PASS' if ka3 <= 1e-6 else 'FAIL'}")

# ------------------------------------------------------------------ Limber (standard kernel, cfg917_lib.limber_X form)
ZSTAR = 1089.0; CHIS = M.angular_distance(ZSTAR) * (1 + ZSTAR)
STEPS = (0.5, 1.5, 3.0, 4.0, 6.0)
zg = np.concatenate([np.linspace(1e-4, 6.5, 3251), np.geomspace(6.5, ZSTAR, 801)[1:-1], [ZSTAR * (1 - 1e-9)]])
zg = np.unique(np.concatenate([zg, [s - 1e-7 for s in STEPS], [s + 1e-7 for s in STEPS]]))
chi = np.array([M.angular_distance(z) * (1 + z) for z in zg])
LG = np.unique(np.concatenate([np.round(np.geomspace(2, 2500, 400)).astype(int), [100, 200, 300, 400]])).astype(float)
KT = np.geomspace(1e-5, 10.0, 320); ZT = np.unique(np.concatenate([np.linspace(0, 7, 141), np.linspace(7, 20, 53)]))
LPT = np.log(np.array([[M.pk_lin(k, z) for z in ZT] for k in KT]))
PINT = RegularGridInterpolator((np.log(KT), ZT), LPT, bounds_error=False, fill_value=None)
D20 = DCL(20.0)
def Pk(k, z):
    """P_lin(k, z) [Mpc^3], k array (1/Mpc); 0 outside [1e-5, 10]; z > 20 by CLASS's growth factor."""
    k = np.asarray(k, float); out = np.zeros_like(k); m = (k >= KT[0]) & (k <= KT[-1])
    if m.any():
        zz = min(z, 20.0); out[m] = np.exp(PINT(np.column_stack([np.log(k[m]), np.full(m.sum(), zz)])))
        if z > 20.0: out[m] *= (DCL(z) / D20) ** 2
    return out
KER = ((1 + zg) * (CHIS - chi) / CHIS) ** 2
PM = np.array([Pk((LG + 0.5) / c, z) for z, c in zip(zg, chi)]).T          # (nL, nz)
TW = np.zeros_like(chi); dchi = np.diff(chi); TW[:-1] += 0.5 * dchi; TW[1:] += 0.5 * dchi
KMAT = PM * (KER * TW)[None, :]
DEN = KMAT.sum(axis=1)
def S_of(Rz, Lout=None):
    """S(L) = C_L[R] / C_L[1] on all L 0..2500 (S = 1 below L 2), R on zg."""
    s = (KMAT * (Rz ** 2)[None, :]).sum(axis=1) / DEN      # explicit sum (Accelerate BLAS raises spurious FP flags in matmul; cfg917_lib does the same)
    Lall = np.arange(LIB.LMAX + 1.0); S = np.ones(LIB.LMAX + 1)
    S[2:] = np.interp(np.log(Lall[2:]), np.log(LG), s); return S
def X_abs():
    pref = (1.5 * OMCL * H0c ** 2) ** 2
    C = 4.0 / (LG + 0.5) ** 4 * pref * DEN
    return dict(zip(LG.astype(int), (LG * (LG + 1)) ** 2 * C / (2 * math.pi)))

# KA4a
S_c = S_of(np.full_like(zg, 1.37)); ka4a = float(np.max(np.abs(S_c[2:] / 1.37 ** 2 - 1)))
# KA4b
XA = X_abs(); rows4b = [dict(L=L, mine=float(XA[L]), class_=float(X0[L]), rel=float(XA[L] / X0[L] - 1)) for L in (100, 200, 300, 400)]
ka4b = max(abs(r["rel"]) for r in rows4b)
P(f"KA4a R = 1.37 constant: max |S / 1.37^2 - 1| {ka4a:.1e} -> {'PASS' if ka4a <= 1e-10 else 'FAIL'}")
P("KA4b absolute Limber X_L vs CLASS X0: " + ", ".join(f"L {r['L']} {r['rel']:+.4f}" for r in rows4b) + f" -> {'PASS' if ka4b <= 0.02 else 'FAIL'}")

# ------------------------------------------------------------------ histories -> observables
LNAG = np.log(1 / (1 + zg)); ORD = np.argsort(LNAG)
ZD = np.array([r[1] for r in DESI])
ZEVAL = np.unique(np.concatenate([zg[zg <= 6.5], ZD, [0.0, 0.3, 0.5]]))
LNE = np.sort(np.log(1 / (1 + ZEVAL)))
dref, vref = integrate(lambda x: 0.0, Om_cl, dlnH, LNA0, Y0, LNE, [])
ZE_sorted = 1 / np.exp(LNE) - 1

class Hist:
    """q(z): kind 'step' (q0 for z <= z_on) or 'knots' (linear in z on knots, 0 above the last knot)."""
    def __init__(self, name, kind, q0=None, z_on=None, zk=None, qk=None, fk=None):
        self.name, self.kind, self.q0, self.z_on = name, kind, q0, z_on
        self.zk = None if zk is None else np.asarray(zk, float); self.qk = None if qk is None else np.asarray(qk, float)
        self.fk = fk
    def q(self, z):
        if self.kind == "step": return self.q0 if z <= self.z_on else 0.0
        return float(np.interp(z, self.zk, self.qk)) if z <= self.zk[-1] else 0.0
    def breaks(self):
        zs = [self.z_on] if self.kind == "step" else list(self.zk)
        return [math.log(1 / (1 + z)) for z in zs]

def observe(H, mode):
    """mode: 'main', 'sign' (q -> -q), 'potonly' (potential boosted, growth = reference)."""
    sg = -1.0 if mode == "sign" else 1.0
    qa = lambda lna: sg * H.q(1 / math.exp(lna) - 1)
    if mode == "potonly":
        dq, vq = dref.copy(), vref.copy()
    else:
        dq, vq = integrate(qa, Om_cl, dlnH, LNA0, Y0, LNE, H.breaks())
    ratio = dq / dref; rv = vq / vref
    zmax = H.z_on if H.kind == "step" else H.zk[-1]
    Rz = np.ones_like(zg)
    on = zg <= min(zmax, 6.5)
    gro = np.interp(zg[on], ZE_sorted[::-1], ratio[::-1])
    Rz[on] = np.array([1 + sg * H.q(z) for z in zg[on]]) * gro
    if zmax > 6.5:                                   # only the z_on 1089 M-POT check uses this; growth there is the reference
        off = (zg > 6.5) & (zg <= zmax); Rz[off] = np.array([1 + sg * H.q(z) for z in zg[off]])
    S = S_of(Rz); fit = amp_fit(S * X0)
    r_eff = AX0 / fit["A"]
    s0 = float(np.interp(0.0, ZE_sorted[::-1], ratio[::-1]))
    Rf = {t: float(np.interp(z, ZE_sorted[::-1], rv[::-1])) for (t, z, *_ ) in DESI}
    shear = {str(z): float((1 + sg * H.q(z)) * np.interp(z, ZE_sorted[::-1], ratio[::-1])) for z in (0.3, 0.5)}
    Lr = np.arange(100, 401)
    return dict(r_eff=float(r_eff), A_boost=fit["A"], sig_boost=fit["sig_abs"], chi2_shape=fit["chi2_refit"], s0=s0, Rf=Rf, shear=shear,
                S_L={str(L): float(S[L]) for L in (100, 200, 400)}, S_mean_100_400=float(S[Lr].mean()), _Rz=Rz)

def margins(o):
    """>= 0 passes. graded: lens2, fs8, s8. reported: lens3, lens_data, ce2_suppress, shear, aphi."""
    fs = min(min(2 * 0.5 * (p1 + m1) - abs(o["Rf"][t] - r1), 2 * 0.5 * (p2 + m2) - abs(o["Rf"][t] - r2)) for (t, z, r1, p1, m1, r2, p2, m2) in DESI)
    return dict(lens2=LINE2 - abs(o["r_eff"] - 1), fs8=fs, s8=S8LINE - abs(o["s0"] - 1),
                lens3=LINE3 - abs(o["r_eff"] - 1), lens_data=2 * o["sig_boost"] - abs(o["A_boost"] - 1),
                ce2_suppress=1.001 - max(o["Rf"].values()), shear=S8LINE - max(abs(v - 1) for v in o["shear"].values()),
                aphi=APHI2 - abs(o["r_eff"] - 1))
GRADED = ("lens2", "fs8", "s8"); REPORTED = ("lens3", "lens_data", "ce2_suppress", "shear", "aphi")
def qf(f): return 1.5 * f / (1 - f)
def const_hist(f, z_on): return Hist(f"const_f{f:g}_zon{z_on:g}", "step", q0=qf(f), z_on=z_on)

_OBS = {}
def obs_const(f, z_on, mode):
    key = (float(f), float(z_on), mode)
    if key not in _OBS: _OBS[key] = margins(observe(const_hist(f, z_on), mode))
    return _OBS[key]
def allowance(z_on, key, mode):
    """largest f in (0, 0.5) passing the probe: first failure on a log pre-scan, then bisection."""
    g = lambda f: obs_const(f, z_on, mode)[key]
    if g(1e-6) < 0: return dict(f_max=0.0, note="fails at f -> 0")
    fs = np.geomspace(1e-4, 0.5, 40); prev = 1e-6
    for f in fs:
        if g(f) < 0:
            fm = brentq(g, prev, f, xtol=1e-7, rtol=1e-9); return dict(f_max=float(fm))
        prev = f
    return dict(f_max=None, note="passes at 0.5: allowance > 0.5")

# KA4c: independent quadrature (cfg917_lib.limber_X on its own z grid)
H4c = const_hist(0.02, 1.5); o4c = observe(H4c, "main"); Rz4c = o4c["_Rz"]
zgL = LIB.zgrid()
chiL = np.array([M.angular_distance(z) * (1 + z) for z in zgL])
inp = types.SimpleNamespace(chi=lambda zz: chiL, chi_star=CHIS)
Rz_L = np.interp(zgL, zg, Rz4c)
def Pfun_ref(k, a, z): return Pk(k, z)
_R_lookup = dict(zip(zgL.tolist(), Rz_L.tolist()))
def Pfun_b(k, a, z): return Pk(k, z) * _R_lookup[float(z)] ** 2
Xr = LIB.limber_X(Pfun_ref, inp, zgL, OMCL, Lmax=400); Xb = LIB.limber_X(Pfun_b, inp, zgL, OMCL, Lmax=400)
S4c = S_of(Rz4c)
rows4c = [dict(L=L, mine=float(S4c[L]), limber_X=float(Xb[L] / Xr[L]), diff=float(S4c[L] - Xb[L] / Xr[L])) for L in (100, 200, 400)]
ka4c = max(abs(r["diff"]) for r in rows4c)
P("KA4c f 0.02 z_on 1.5, S(L) mine vs cfg917_lib.limber_X: " + ", ".join(f"L {r['L']} {r['mine']:.6f} / {r['limber_X']:.6f}" for r in rows4c)
  + f"; max |diff| {ka4c:.1e} -> {'PASS' if ka4c <= 1e-3 else 'FAIL'}")
RES["KA"]["KA4"] = dict(a=dict(max_rel=ka4a, pass_=bool(ka4a <= 1e-10)), b=dict(rows=rows4b, pass_=bool(ka4b <= 0.02)),
                        c=dict(rows=rows4c, pass_=bool(ka4c <= 1e-3)))
KA_OK = all([RES["KA"]["KA1"]["pass_"], RES["KA"]["KA2"]["pass_"], RES["KA"]["KA3"]["pass_"], RES["KA"]["KA4"]["a"]["pass_"],
             RES["KA"]["KA4"]["b"]["pass_"], RES["KA"]["KA4"]["c"]["pass_"]])
P(f"Known answers all pass: {KA_OK}  ({time.time() - T0:.0f} s)")

# reported: QX3 iter2's limber_ratio (extra chi^-4 weight) against the standard kernel, same history
kg_ = np.logspace(-4, 1, 70); zg_ = np.linspace(0.02, 20.0, 120)
Rk = np.tile(np.interp(zg_, zg, Rz4c), (len(kg_), 1))
S_i2 = I2.limber_ratio(M, H0, kg_, zg_, Rk)
w4 = (CHIS - chi) ** 2 / CHIS ** 2 * (1 + zg) ** 2 / chi ** 4             # iter2's weight per dchi, on my grid
KM4 = PM * (w4 * TW)[None, :]; s4 = (KM4 * (Rz4c ** 2)[None, :]).sum(axis=1) / KM4.sum(axis=1)
RES["reported"]["iter2_limber_ratio_check"] = dict(history="f 0.02, z_on 1.5", rows=[dict(L=L, standard=float(S4c[L]), iter2_limber_ratio=float(S_i2[L]),
    chi_minus4_weight_on_my_grid=float(np.interp(math.log(L), np.log(LG), s4))) for L in (100, 200, 400)])
P("reported: QX3 iter2 limber_ratio vs standard kernel, f 0.02 z_on 1.5: " + ", ".join(
    f"L {r['L']} standard {r['standard']:.5f}, iter2 {r['iter2_limber_ratio']:.5f}, chi^-4 weight on my grid {r['chi_minus4_weight_on_my_grid']:.5f}"
    for r in RES["reported"]["iter2_limber_ratio_check"]["rows"]))

# ------------------------------------------------------------------ SWT1 readings: q(z), f(z) from swt1.py's `compensated`
SW = os.path.join(REPO, "fable52_push", "SWT1_switch_theorems", "swt1.py")
src = open(SW).read(); cut = src.index("RES = dict(")
NSW = {"__file__": SW, "__name__": "swt1_reused"}
argv0, sys.argv = sys.argv, [SW]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], SW, "exec"), NSW)
sys.argv = argv0
ZR = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]; ZR_EXT = [4.0, 6.0]
READ = ("L", "C", "NC", "NL")
RTAB = {}
_MAINJ = os.path.join(HERE, "gal1.json")
if MUT == "sign" and os.path.exists(_MAINJ):          # the twin reuses the main run's q(z) inputs, so it differs from main only in the sign
    for k, v in json.load(open(_MAINJ))["histories"]["readings_qz"].items():
        RTAB[tuple(k.split("_", 1))] = v
    P(f"M-SIGN: reading histories q(z) read from gal1.json (main run's inputs)")
for foot, a0 in (A0.items() if (MUT is None or (MUT == "sign" and not RTAB)) else []):
    for w in READ:
        rows = []
        for z in ZR + ZR_EXT:
            tab = NSW["radii_table"](w, a0, z); d = NSW["compensated"](tab, a0, z)
            rows.append(dict(z=z, f_V=d["f_V"], dilute=d["dilute"], q_C=d["q_C"], q_ff=d["q_ff"], q_tot=d["q_tot"]))
        RTAB[(foot, w)] = rows
        P(f"[{foot}] reading {w}: " + "; ".join(f"z {r['z']:g} f {r['f_V']:.4f} q {r['q_tot']:.4f}{'' if r['dilute'] else '*'}" for r in rows))
P(f"   (* filling over 0.30: q_C is SWT1's lower bound)  readings done ({time.time() - T0:.0f} s)")
RES["histories"]["readings_qz"] = {f"{k[0]}_{k[1]}": v for k, v in RTAB.items()}

def reading_hist(foot, w, ext=False):
    rows = [r for r in RTAB[(foot, w)] if (r["z"] <= 3.0 or ext)]
    return Hist(f"{foot}_{w}{'_ext6' if ext else ''}", "knots", zk=[r["z"] for r in rows], qk=[r["q_tot"] for r in rows])

# ------------------------------------------------------------------ main / MUTATE runs
ZON = (3.0, 1.5, 0.5)
def mono_check(z_on, mode):
    fs = np.linspace(0, 0.5, 11); vals = {k: [] for k in GRADED}
    for f in fs:
        o = observe(const_hist(f, z_on), mode)
        vals["lens2"].append(o["r_eff"]); vals["s8"].append(o["s0"]); vals["fs8"].append(max(o["Rf"].values()))
    return {k: bool(np.all(np.diff(v) > 0)) for k, v in vals.items()}

def strip(o): return {k: v for k, v in o.items() if not k.startswith("_")}

if MUT is None or MUT == "potonly":
    mode = "main" if MUT is None else "potonly"
    AL = {}
    for z_on in ZON:
        AL[str(z_on)] = {k: allowance(z_on, k, mode) for k in GRADED + REPORTED}
        a = AL[str(z_on)]
        fmt = lambda d: (f"{d['f_max']:.5f}" if d.get("f_max") is not None else "> 0.5")
        P(f"[{mode}] z_on {z_on:g}: allowance on f, graded: lensing 2 sigma {fmt(a['lens2'])}, f sigma8 {fmt(a['fs8'])}, S8 {fmt(a['s8'])}; "
          f"reported: lensing 3 sigma {fmt(a['lens3'])}, lensing data-centred {fmt(a['lens_data'])}, CE2 Rf <= 1.001 {fmt(a['ce2_suppress'])}, "
          f"shear S8 {fmt(a['shear'])}, CMB3 A_phi {fmt(a['aphi'])}")
        AL[str(z_on)]["monotonic_on_11_point_grid"] = mono_check(z_on, mode)
        P(f"      monotonic in f (11-point grid 0-0.5): {AL[str(z_on)]['monotonic_on_11_point_grid']}")
    RES["allowances"] = AL
    # what the tight allowance looks like as observables
    vals = [AL[str(z)][k]["f_max"] for z in ZON for k in GRADED if AL[str(z)][k].get("f_max") is not None]
    f_tight = min(vals) if vals else None
    which = [(z, k) for z in ZON for k in GRADED if AL[str(z)][k].get("f_max") == f_tight]
    RES["f_tight"] = dict(f=f_tight, at=[dict(z_on=z, probe=k) for z, k in which], ratio_to_0231=(f_tight / F_SWT1 if f_tight else None))
    P(f"[{mode}] tightest graded allowance f_tight {f_tight:.5f} at {which}; / 0.0231 = {f_tight / F_SWT1:.3f}")
    for z_on in ZON:
        for f in (0.0231, f_tight):
            o = observe(const_hist(f, z_on), mode); RES["histories"][f"const_f{f:.5f}_zon{z_on:g}"] = strip(o)
            P(f"   [{mode}] const f {f:.5f} (q {qf(f):.5f}) z_on {z_on:g}: r_eff {o['r_eff']:.5f} (S at L 100/200/400 " +
              "/".join(f"{v:.5f}" for v in o["S_L"].values()) + f", mean 100-400 {o['S_mean_100_400']:.5f}); s(0) {o['s0']:.5f}; Rf " +
              ", ".join(f"{t} {v:.4f}" for t, v in o["Rf"].items()) + f"; shape chi2 {o['chi2_shape']:.2f} (line 18.48)")
    if MUT == "potonly":
        # check: boost on at every z, 3 sigma, direct only -> SWT1's 0.0231
        def g1089(f): return margins(observe(const_hist(f, 1089.0), "potonly"))["lens3"]
        f1089 = brentq(g1089, 1e-4, 0.2, xtol=1e-9)
        q_ex = math.sqrt(1 + LINE3) - 1; f_ex = q_ex / (1.5 + q_ex)
        okc = abs(f1089 / F_SWT1 - 1) <= 5e-3
        RES["MUTATE"]["potonly_check_zon1089_3sigma"] = dict(f=f1089, closed_form=f_ex, swt1=F_SWT1, rel_to_swt1=f1089 / F_SWT1 - 1, pass_=bool(okc))
        P(f"M-POT check, boost at every z, 3 sigma, potential only: f {f1089:.5f} (closed form {f_ex:.5f}; SWT1 0.0231, rel {f1089 / F_SWT1 - 1:+.4f}) -> {'PASS' if okc else 'FAIL'}")
        # bite: growth untouched, lensing allowance looser than main's
        o = observe(const_hist(0.0231, 3.0), "potonly")
        flat = abs(o["s0"] - 1) == 0.0 and all(abs(v - 1) == 0.0 for v in o["Rf"].values())
        main3 = allowance(3.0, "lens2", "main")["f_max"]; pot3 = AL["3.0"]["lens2"]["f_max"]
        bite = flat and pot3 > main3 * 1.01
        RES["MUTATE"]["M_POT"] = dict(growth_flat=bool(flat), lens2_zon3_potonly=pot3, lens2_zon3_main=main3, bites=bool(bite))
        P(f"MUTATE M-POT: growth flat {flat}; lensing 2 sigma allowance z_on 3: potential-only {pot3:.5f} vs main {main3:.5f} -> {'BITES' if bite else 'NO BITE'}")

if MUT == "sign":
    rows = []; bite = True
    hs = [const_hist(0.0231, z) for z in ZON] + [reading_hist(f, w) for f in A0 for w in READ]
    for H in hs:
        o = observe(H, "sign"); ok = o["s0"] < 1 and all(v < 1 for v in o["Rf"].values()) and o["r_eff"] < 1
        bite &= ok; rows.append(dict(history=H.name, s0=o["s0"], Rf=o["Rf"], r_eff=o["r_eff"], growth_drops=bool(ok)))
        P(f"MUTATE M-SIGN {H.name}: s(0) {o['s0']:.5f}, Rf " + ", ".join(f"{v:.4f}" for v in o["Rf"].values()) + f", r_eff {o['r_eff']:.5f} -> {'drops' if ok else 'DOES NOT DROP'}")
    RES["MUTATE"]["M_SIGN"] = dict(rows=rows, bites=bool(bite))
    P(f"MUTATE M-SIGN -> {'BITES' if bite else 'NO BITE'}")

if MUT is None:
    # readings
    RG = {}
    for foot in A0:
        RG[foot] = {}
        for w in READ:
            o = observe(reading_hist(foot, w), "main"); m = margins(o)
            st = {k: ("PASS" if m[k] >= 0 else "FAIL") for k in GRADED + REPORTED}
            ov = "PASS" if all(st[k] == "PASS" for k in GRADED) else "FAIL"
            oe = observe(reading_hist(foot, w, ext=True), "main"); me = margins(oe)
            ste = {k: ("PASS" if me[k] >= 0 else "FAIL") for k in GRADED + ("lens3",)}
            RG[foot][w] = dict(obs=strip(o), status=st, overall=ov, ext_z6=dict(obs=strip(oe), status=ste))
            P(f"[{foot}] reading {w} (q on to z 3): r_eff {o['r_eff']:.5f} (2 sigma line {1 + LINE2:.5f}, 3 sigma {1 + LINE3:.5f}); s(0) {o['s0']:.5f}; Rf "
              + ", ".join(f"{t} {v:.4f}" for t, v in o["Rf"].items()) + f"; lensing {st['lens2']} f sigma8 {st['fs8']} S8 {st['s8']} -> {ov}"
              f"  [3 sigma lensing {st['lens3']}; to z 6: r_eff {oe['r_eff']:.5f} {ste['lens2']}]")
    RES["readings"] = RG
    # labels
    lo, hi = F_SWT1 / 1.5, F_SWT1 * 1.5
    for foot in A0:
        L_f = RG[foot]["L"]["overall"] == "FAIL"; C_f = RG[foot]["C"]["overall"] == "FAIL"
        NC_p = RG[foot]["NC"]["overall"] == "PASS"; NL_p = RG[foot]["NL"]["overall"] == "PASS"
        changed = [w for w, ok in (("L", L_f), ("C", C_f), ("NC", NC_p), ("NL", NL_p)) if not ok]
        ft = RES["f_tight"]["f"]
        if not KA_OK: lab = "NO VERDICT (known answer failed)"
        elif lo <= ft <= hi and not changed: lab = "ALLOWANCE CONFIRMED"
        elif ft < lo: lab = "ALLOWANCE TIGHTER"
        elif ft > hi: lab = "ALLOWANCE LOOSER"
        elif ("NC" in changed or "NL" in changed): lab = "ALLOWANCE TIGHTER"
        else: lab = "ALLOWANCE LOOSER"
        RES["labels"][foot] = dict(label=lab, f_tight=ft, band=[lo, hi], readings_changing_side=changed)
        P(f"LABEL [{foot}]: {lab} (f_tight {ft:.5f}, band {lo:.5f}-{hi:.5f}; readings changing side: {changed if changed else 'none'})")

P(f"runtime {time.time() - T0:.0f} s. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
