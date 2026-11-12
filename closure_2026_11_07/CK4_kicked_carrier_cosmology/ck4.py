#!/usr/bin/env python3
"""CK4 (FROZEN_CRITERIA.md 16d0b4c6a5): cosmology under the kicked collisionless carrier. Cold parent at the CMB's amount
(QX7 iter_4 / CE2 background), daughters produced at halo virialisation (Sheth-Tormen on the parent's own linear power,
M >= M_min), kicked at v_k, escaping daughters a free-streaming fluid (c_s = sigma_1D). Gates GL (PR4 lensing, CE2
machinery), GF (DESI DR1 fsigma8 z < 1, CE2 machinery), GFo (linear P1D ratio z 2-4). GEB is ck4_geb.py.
    python3 ck4.py            -> ck4.json / ck4.out
    python3 ck4.py --mutate   -> ck4_MUTATE.json / ck4_MUTATE.out
QX7 iter_4 / QX3 are exec'd read-only. Cold dark energy (the carrier's cold phase), never dark matter; no particle.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, resource, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.interpolate import CubicSpline
trap = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL6 = os.path.join(REPO, "closure_2026_11_06")
MUT = "--mutate" in sys.argv; TAG = "ck4_MUTATE" if MUT else "ck4"; OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))

VK = (550.0, 575.0, 600.0); MMIN_P = 1e11; MMIN_BR = (1e10, 1e12)
GMPC = 4.30091e-9          # G in Mpc (km/s)^2 / Msun
CKM = 299792.458
VESC_FAC = 2.69            # NFW c = 5 at r_s (declared)
DVIR = 18 * math.pi ** 2   # x rho_crit(z) (fill-in, disclosed)
ST_P, ST_Q, DC = 0.3, 0.707, 1.686

# ---------------------------------------------------------------- iter_4 prefix (read-only)
I4 = os.path.join(CL6, "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.py")
s4 = open(I4).read(); c4 = s4.index("RES = dict(tag=TAG")
argv0 = sys.argv; sys.argv = [I4]; N4 = {"__file__": I4, "__name__": "qx7_iter4_reused"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(s4[:c4], I4, "exec"), N4)
sys.argv = argv0
N3, I2, g2gen, kJ_of, ode, h4, K1 = (N4[k] for k in ("N3", "I2", "g2gen", "kJ_of", "ode", "h", "K1"))
MC = N3["M"]; kgrid = N3["kgrid"]; zgrid = N3["zgrid"]; ref = N3["ref"]; c0 = float(N3["c0"])
lna_t, lnH_t, dlnH_t, H0c, Om_b0, Om_d0, ai, adec, lnz = (N3[k] for k in ("lna_t", "lnH_t", "dlnH_t", "H0c", "Om_b0", "Om_d0", "ai", "adec", "lnz"))
hh = MC.h(); OB, OD, H0 = float(N3["ob"]), float(N3["od"]), float(N3["H0"]); NS = float(N3["ns"])
P(f"CK4 {TAG}: background omega_b {OB} omega_d {OD:.5f} H0 {H0} n_s {NS} (iter_4 / CE2); Om_b0 {Om_b0:.5f} Om_d0 {Om_d0:.5f}; c0 {c0:.6f}")
RHOC0 = 2.77536627e11 * hh ** 2                      # Msun / Mpc^3
def Hkms(z): return MC.Hubble(z) * CKM                # km/s/Mpc
def E2a(a): return math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c ** 2

# ---------------------------------------------------------------- extended CLASS model (same params, larger k range)
from classy import Class
MF = Class(); pf = {'output': 'mPk', 'h': H0 / 100, 'omega_b': OB, 'omega_cdm': OD, 'A_s': I2.AS0, 'n_s': NS,
                    'tau_reio': 0.06, 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 400.0, 'z_max_pk': 20.0}
MF.set(pf); MF.compute()
kchk = {k: (MF.pk_lin(k, 0.0) / MC.pk_lin(k, 0.0) - 1) for k in (0.1, 1.0)}
P("extended CLASS model vs MC pk_lin: " + ", ".join(f"k {k}: {v:+.1e}" for k, v in kchk.items()))
KA = {"KA_MF": dict(rows=kchk, pass_=bool(all(abs(v) <= 1e-4 for v in kchk.values())))}

# ---------------------------------------------------------------- sigma(M, z) and Sheth-Tormen collapsed fraction
lnM = np.linspace(math.log(1e7), math.log(1e17), 121); Mg = np.exp(lnM)
rho_m0 = RHOC0 * (Om_b0 + Om_d0)
Rm = (3 * Mg / (4 * math.pi * rho_m0)) ** (1 / 3)
kk = np.logspace(-4, math.log10(399.0), 900); lkk = np.log(kk)
zs = np.concatenate([np.linspace(0, 3, 31), np.linspace(3.25, 10, 28), np.linspace(11, 20, 10)])
def Wth(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
W2 = Wth(np.outer(Rm, kk)) ** 2
sig = np.empty((len(zs), len(Mg)))
for j, z in enumerate(zs):
    pk = np.array([MF.pk_lin(k, z) for k in kk])
    sig[j] = np.sqrt(trap(W2 * (kk ** 3 * pk / (2 * math.pi ** 2))[None, :], lkk, axis=1))
s8chk = float(np.sqrt(trap(Wth(kk * 8 / hh) ** 2 * kk ** 3 * np.array([MF.pk_lin(k, 0.0) for k in kk]) / (2 * math.pi ** 2), lkk)))
P(f"sigma8 (cold reference, A_s {I2.AS0}) {s8chk:.4f}; CLASS {MF.sigma8():.4f}")
lna_s = np.log(1 / (1 + zs))
# Sheth-Tormen nu f(nu); A normalised numerically
nuu = np.logspace(-3, 1.5, 4000)
def nuf(nu): qn = ST_Q * nu ** 2; return np.sqrt(2 * qn / math.pi) * (1 + qn ** -ST_P) * np.exp(-qn / 2)
A_ST = 1 / trap(nuf(nuu) / nuu, nuu)
cum = np.concatenate([[0], np.cumsum(0.5 * (A_ST * nuf(nuu[1:]) / nuu[1:] + A_ST * nuf(nuu[:-1]) / nuu[:-1]) * np.diff(nuu))])
def Fgt(nu):  # fraction in halos with peak height > nu
    return np.clip(1 - np.interp(nu, nuu, cum, left=0.0, right=1.0), 0, 1)
Fcoll = Fgt(DC / sig)                       # (z, M): F(>M, z)
P(f"A_ST {A_ST:.4f}; F(>1e11, z=0) {np.interp(math.log(1e11), lnM, Fcoll[0]):.3f}, F(>1e10, 0) {np.interp(math.log(1e10), lnM, Fcoll[0]):.3f}, F(>1e12, 0) {np.interp(math.log(1e12), lnM, Fcoll[0]):.3f}")
mono = bool(all(np.all(np.diff(Fcoll[j]) <= 1e-12) for j in range(len(zs))) and np.all((Fcoll >= 0) & (Fcoll <= 1)))

def vesc(M, z):
    rhoc = 3 * Hkms(z) ** 2 / (8 * math.pi * GMPC)
    r = (3 * M / (4 * math.pi * DVIR * rhoc)) ** (1 / 3); return VESC_FAC * np.sqrt(GMPC * M / r)

def production(vk, Mmin, reading):
    """On the solver's ln a grid: F_esc(a) (fraction of the dark component escaped as daughters), r = dF_esc/dlna / F_esc,
    sigma^2(a) of the escaped daughters (km/s)^2; F_conv(a) total converted."""
    lg = np.linspace(math.log(ai), 0.0, 6001)
    # n(M, x) = dF/dlnM ; positive part of its x-derivative, splines in x (on zs grid then interp)
    sp = CubicSpline(lna_s[::-1], Fcoll[::-1], axis=0)
    dF = sp.derivative()(np.clip(lg, lna_s.min(), lna_s.max()))           # dF(>M)/dlna (n_lg, M)
    dF[lg < lna_s.min()] = 0.0
    im = int(np.searchsorted(lnM, math.log(Mmin)))
    Fc = sp(np.clip(lg, lna_s.min(), lna_s.max())); Fc[lg < lna_s.min()] = 0.0
    qtot = np.clip(np.array([np.interp(math.log(Mmin), lnM, row) for row in dF]), 0, None)
    # w(M) = positive part of d/dx of dF(>M)/dlnM... n = -dF(>M)/dlnM ; dn/dx = -d/dlnM (dF(>M)/dx)
    dn = -np.gradient(dF, lnM, axis=1); w = np.clip(dn, 0, None); w[:, :im] = 0.0
    zz = 1 / np.exp(lg) - 1
    fesc = np.zeros_like(lg); v2 = np.zeros_like(lg)
    for i in range(len(lg)):
        if qtot[i] <= 0 or w[i].sum() <= 0: continue
        if reading == "A":
            fesc[i] = 1.0; v2[i] = vk ** 2; continue
        ve = vesc(Mg, max(zz[i], 0.0)); ok = ve < vk
        tot = trap(w[i], lnM)
        if tot <= 0 or not ok.any(): continue
        we = np.where(ok, w[i], 0.0); fesc[i] = trap(we, lnM) / tot
        if fesc[i] > 0: v2[i] = trap(we * (vk ** 2 - ve ** 2), lnM) / trap(we, lnM)
    qesc = qtot * fesc
    a = np.exp(lg)
    # cumulative (trapezoid in lna)
    Fesc = np.concatenate([[0], np.cumsum(0.5 * (qesc[1:] + qesc[:-1]) * np.diff(lg))])
    Fconv = np.concatenate([[0], np.cumsum(0.5 * (qtot[1:] + qtot[:-1]) * np.diff(lg))])
    S = qesc * v2 / 3 * a ** 2
    Sc = np.concatenate([[0], np.cumsum(0.5 * (S[1:] + S[:-1]) * np.diff(lg))])
    sig2 = np.where(Fesc > 0, Sc / np.maximum(Fesc, 1e-300) / a ** 2, 0.0)
    return dict(lg=lg, Fesc=np.minimum(Fesc, 1.0), Fconv=np.minimum(Fconv, 1.0), qesc=qesc, sig2=sig2)

# ---------------------------------------------------------------- three-species solver (QX3 iter3 scheme, implicit midpoint)
def solve3(kg, zg, prod=None, jeans_all=None):
    """y = (d_c, T_c, d_d, T_d, d_b, T_b), T = -d delta/dlna. prod: production() dict or None (no daughters).
    jeans_all: kJ(a) callable -> KA2 (every dark element in the daughter slot with iter_4's Jeans term)."""
    nk = len(kg); lnzz = np.log(1 / (1 + zg))
    grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnzz]))
    y = np.zeros((nk, 6)); y[:, 0] = ai; y[:, 1] = -ai; y[:, 2] = ai; y[:, 3] = -ai
    rec = {}; tset = {float(x): i for i, x in enumerate(lnzz)}; I6 = np.eye(6)[None, :, :]
    if prod is not None:
        Fe = prod["Fesc"]; lgp = prod["lg"]; qe = prod["qesc"]; s2 = prod["sig2"]
    for n in range(len(grid) - 1):
        h_ = grid[n + 1] - grid[n]; lna = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lna)
        E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c ** 2; dl = float(np.interp(lna, lna_t, dlnH_t))
        Odt = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; on = a > adec
        if jeans_all is not None:
            F = 1.0; r = 0.0; J = 1.5 * Odt * (kg / (a * jeans_all(a))) ** 2
        elif prod is not None:
            F = float(np.interp(lna, lgp, Fe)); q = float(np.interp(lna, lgp, qe)); r = q / F if F > 1e-12 else 0.0
            sg2 = float(np.interp(lna, lgp, s2)); Hk = math.exp(float(np.interp(lna, lna_t, lnH_t))) * CKM
            J = sg2 * (kg / (a * Hk)) ** 2 if F > 1e-12 else np.zeros(nk)
        else:
            F = 0.0; r = 0.0; J = np.zeros(nk)
        Oc, Od = Odt * (1 - F), Odt * F
        A = np.zeros((nk, 6, 6))
        A[:, 0, 1] = -1.0
        A[:, 1, 1] = -(2 + dl); A[:, 1, 0] = -1.5 * Oc; A[:, 1, 2] = -1.5 * Od
        A[:, 2, 3] = -1.0; A[:, 2, 0] = r; A[:, 2, 2] = -r
        A[:, 3, 3] = -(2 + dl) - r; A[:, 3, 1] = r; A[:, 3, 0] = -1.5 * Oc; A[:, 3, 2] = -1.5 * Od + J
        if on:
            A[:, 1, 4] = -1.5 * Ob; A[:, 3, 4] = -1.5 * Ob
            A[:, 4, 5] = -1.0; A[:, 5, 5] = -(2 + dl); A[:, 5, 0] = -1.5 * Oc; A[:, 5, 2] = -1.5 * Od; A[:, 5, 4] = -1.5 * Ob
        y = np.linalg.solve(I6 - 0.5 * h_ * A, ((I6 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
        t = float(grid[n + 1])
        if t in tset: rec[tset[t]] = (y.copy(), F)
    dm = np.empty((nk, len(zg)))
    for jz in range(len(zg)):
        yy, F = rec[jz]; a = 1 / (1 + zg[jz]); E2 = E2a(a)
        Odt = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2
        dm[:, jz] = (Odt * (1 - F) * yy[:, 0] + Odt * F * yy[:, 2] + Ob * yy[:, 4]) / (Odt + Ob)
    return dm

# ---------------------------------------------------------------- CE2's GL / GF machinery (copied from ce2.py, unchanged)
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]
R8 = 8.0 / hh
Pref = np.array([[MC.pk_lin(k, z) for z in zgrid] for k in kgrid])
lk = np.log(kgrid); w2k3 = Wth(kgrid * R8) ** 2 * kgrid ** 3 / (2 * np.pi ** 2)
def sig8(Rr): return np.sqrt(trap(Pref * Rr ** 2 * w2k3[:, None], lk, axis=0))
lna_z = np.log(1 / (1 + zgrid))
def fs8_ratio(Rr):
    o = np.argsort(lna_z); s_sw = sig8(Rr); s_rf = sig8(np.ones_like(Rr))
    d_sw = CubicSpline(lna_z[o], s_sw[o]).derivative()(lna_z); d_rf = CubicSpline(lna_z[o], s_rf[o]).derivative()(lna_z)
    rr = d_sw / d_rf
    return {b[0]: float(np.interp(b[1], zgrid, rr)) for b in DESI}, {b[0]: float(np.interp(b[1], zgrid, s_sw / s_rf)) for b in DESI}, float(s_sw[0] / s_rf[0])
def fs8_gate(rf):
    rows = []
    for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
        e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = rf[t]
        rows.append(dict(bin=t, z=z, Rf=x, sf=r1, sf_err=e1, sfb=r2, sfb_err=e2, s8dir=bool(x <= 1.001), in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2)))
    return dict(rows=rows, pass_=bool(all(r_["s8dir"] and r_["in_sf"] and r_["in_sfb"] for r_ in rows)))
def limber_fixed(Rr):
    """Post-freeze reading (disclosed): I2.limber_ratio with the potential's k^-4 = (chi/L)^4 restored (the record's
    weight (chi*-chi)^2/(chi chi*)^2 / chi^2 omits it, which weights low z by chi^-4)."""
    M = MC; chis = M.angular_distance(1089.0) * 1090.0
    chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
    w = ((chis - chi) / (chi * chis)) ** 2 * (1 + zgrid) ** 2 / np.array([M.Hubble(z) for z in zgrid])
    Ls = np.arange(2, I2.LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
    for j in range(len(zgrid)):
        kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
        Pj = np.interp(np.log(kk[m]), lnk, Pref[:, j]); Rj = np.interp(np.log(kk[m]), lnk, Rr[:, j])
        wk = w[j] / chi[j] ** 2 * (chi[j] / (Ls[m] + 0.5)) ** 4
        num[m] += wk * Pj * Rj ** 2; den[m] += wk * Pj
    S = np.ones(I2.LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]; return S
def glc_of(Rr):
    S = limber_fixed(Rr); c, _ = I2.best_amp_chi2(N3["X0"] * S)
    return dict(chi2=float(c), dchi2=float(c - c0), pass_=bool(c <= 18.48 and c - c0 <= 4.0), reading="k^-4 restored (post-freeze)")
def gl_of(Rr):
    S = I2.limber_ratio(MC, N3["H0"], kgrid, zgrid, Rr); c, _ = I2.best_amp_chi2(N3["X0"] * S)
    return dict(chi2=float(c), dchi2=float(c - c0), pass_=bool(c <= 18.48 and c - c0 <= 4.0))

# forest: extended grid, z 2, 3, 4
kF = np.logspace(math.log10(0.05 * hh), math.log10(50 * hh), 60); zF = np.array([2.0, 3.0, 4.0])
PF = np.array([[MF.pk_lin(k, z) for z in zF] for k in kF])
kpar = np.logspace(math.log10(0.2 * hh), math.log10(2.0 * hh), 11)
def p1d(Pk):
    out = np.empty((len(kpar), Pk.shape[1]))
    for i, kp in enumerate(kpar):
        m = kF >= kp; out[i] = trap((kF[m] * Pk[m].T).T, kF[m], axis=0) / (2 * math.pi) if m.sum() > 1 else 0
    return out
P1ref = p1d(PF)
dmF_ref = solve3(kF, zF)
def forest_of(prod):
    RF = solve3(kF, zF, prod) / dmF_ref; rat = p1d(PF * RF ** 2) / P1ref
    return dict(ratio_min=float(rat.min()), ratio_max=float(rat.max()), per_z={f"{z:g}": [float(rat[:, j].min()), float(rat[:, j].max())] for j, z in enumerate(zF)},
                pass_=bool(np.all(np.abs(1 - rat) <= 0.10)))

def grade(vk, Mmin, reading):
    pr = production(vk, Mmin, reading)
    Rr = solve3(kgrid, zgrid, pr) / ref
    gl = gl_of(Rr); glc = glc_of(Rr); rf, s8r, s80 = fs8_ratio(Rr); gf = dict(fs8_gate(rf), sigma8_ratio=s8r)
    fo = forest_of(pr)
    lg = pr["lg"]
    rep = {}
    for z in (0, 0.5, 1, 2, 3, 5, 7):
        x = math.log(1 / (1 + z)); s2 = float(np.interp(x, lg, pr["sig2"])); a = 1 / (1 + z)
        rep[f"{z:g}"] = dict(F_conv=float(np.interp(x, lg, pr["Fconv"])), F_esc=float(np.interp(x, lg, pr["Fesc"])), sigma_kms=math.sqrt(s2),
                             k_fs=(math.sqrt(1.5) * a * Hkms(z) / math.sqrt(s2)) if s2 > 0 else None)
    R0 = {f"{k}": float(np.interp(math.log(k), lk, Rr[:, 0])) for k in (0.1, 0.3, 1.0)}
    ok = gl["pass_"] and gf["pass_"] and fo["pass_"]
    return dict(v_k=vk, M_min=Mmin, reading=reading, GL=gl, GLc=glc, GF=gf, GFo=fo, sigma8_ratio_z0=s80, R_k_z0=R0, history=rep, pass_LGF=bool(ok))

def line(t, g):
    return (f"{t}: GL chi2 {g['GL']['chi2']:.2f} (d {g['GL']['dchi2']:+.2f}) {'PASS' if g['GL']['pass_'] else 'FAIL'} | GF Rf "
            + " ".join(f"{r['Rf']:.3f}" for r in g['GF']['rows']) + f" {'PASS' if g['GF']['pass_'] else 'FAIL'} | GFo P1D ratio {g['GFo']['ratio_min']:.3f}-{g['GFo']['ratio_max']:.3f} "
            + f"{'PASS' if g['GFo']['pass_'] else 'FAIL'} | GLc(k^-4) chi2 {g['GLc']['chi2']:.2f} (d {g['GLc']['dchi2']:+.2f}) {'PASS' if g['GLc']['pass_'] else 'FAIL'} | S8 dir sigma8(0) ratio {g['sigma8_ratio_z0']:.3f} | F_esc z0 {g['history']['0']['F_esc']:.3f} z1 {g['history']['1']['F_esc']:.3f} z3 {g['history']['3']['F_esc']:.4f} z7 {g['history']['7']['F_esc']:.1e}; sigma z1 {g['history']['1']['sigma_kms']:.0f} km/s")

# ---------------------------------------------------------------- known answers
d0 = solve3(kgrid, zgrid); ka1 = float(np.max(np.abs(d0 / ref - 1)))
gl0 = gl_of(d0 / ref); rf0 = fs8_ratio(d0 / ref)[0]
KA["KA1"] = dict(max_rel=ka1, chi2=gl0["chi2"], dchi2=gl0["dchi2"], Rf=rf0, K1_iter4=K1["iter3"],
                 pass_=bool(ka1 <= 1e-9 and abs(gl0["dchi2"]) <= 1e-6 and all(abs(v - 1) <= 1e-6 for v in rf0.values()) and abs(K1["iter3"] - 55.640290726118906) <= 1e-6))
P(f"KA1 v_k 0 (no daughters) vs iter_4 ref: max |R-1| {ka1:.1e}; chi2 {gl0['chi2']:.6f} (c0 {c0:.6f}, d {gl0['dchi2']:+.1e}); Rf max |d| {max(abs(v - 1) for v in rf0.values()):.1e}; iter_4 K1 {K1['iter3']:.4f} -> {'PASS' if KA['KA1']['pass_'] else 'FAIL'}")
q4 = json.load(open(os.path.join(CL6, "QX7_unified_cold_switch", "iter_4_late_evaporation", "qx7_iter4.json")))
e1 = min((e for e in q4["evaluated"] if abs(e["p"] - 4.25) < 1e-9), key=lambda e: abs(math.log(e["lambda_0"] / 2.6102)))
kj1 = kJ_of(e1["lambda_star"], e1["p"])
dk2 = gl_of(solve3(kgrid, zgrid, jeans_all=kj1) / ref)["dchi2"]
KA["KA2"] = dict(record=e1["dchi2"], now=dk2, pass_=bool(abs(dk2 - e1["dchi2"]) <= 1e-6))
P(f"KA2 all-dark Jeans term at CE2's C1 (lambda_* {e1['lambda_star']:.4f}, p 4.25): dchi2 {dk2:.6f} vs iter_4 {e1['dchi2']:.6f} -> {'PASS' if KA['KA2']['pass_'] else 'FAIL'}")
z1 = 1.0; a1 = 0.5; s1 = 575 / math.sqrt(3); kfs = math.sqrt(1.5) * a1 * Hkms(z1) / s1
KA["KA3"] = dict(Fcoll_monotone_bounded=mono, k_fs_z1_575=kfs, pass_=bool(mono))
P(f"KA3 ST F(>M) bounded and decreasing in M: {mono}; k_fs(z 1, v 575) = sqrt(3/2) aH/sigma = {kfs:.4f} /Mpc (comoving) -> {'PASS' if mono else 'FAIL'}")
P(f"KA_MF extended CLASS model -> {'PASS' if KA['KA_MF']['pass_'] else 'FAIL'}")
# KA_LC (post-freeze reading's own check): absolute Limber C_L^pp shape vs CLASS raw_cl pp, L 20-400, normalised at L 100
def limber_abs(extra):
    chis = MC.angular_distance(1089.0) * 1090.0; chi = np.array([MC.angular_distance(z) * (1 + z) for z in zgrid]); Hz = np.array([MC.Hubble(z) for z in zgrid])
    out = []
    for L in (20, 50, 100, 200, 300, 400):
        kk = (L + 0.5) / chi; m = (kk >= kgrid[0]) & (kk <= kgrid[-1]); v = 0.0
        for j in np.where(m)[0]:
            v += ((chis - chi[j]) / (chi[j] * chis)) ** 2 * (1 + zgrid[j]) ** 2 / Hz[j] * np.exp(np.interp(math.log(kk[j]), lk, np.log(Pref[:, j]))) / chi[j] ** 2 * extra(chi[j], L + 0.5)
        out.append(v)
    pp = MC.raw_cl(500)["pp"]; r = np.array(out) / pp[[20, 50, 100, 200, 300, 400]]; return (r / r[2]).tolist()
shp_frozen = limber_abs(lambda c, L: 1.0); shp_fixed = limber_abs(lambda c, L: (c / L) ** 4)
KA["KA_LC"] = dict(L=[20, 50, 100, 200, 300, 400], frozen_over_CLASS=shp_frozen, fixed_over_CLASS=shp_fixed,
                   pass_=bool(max(abs(x - 1) for x in shp_fixed) <= 0.03), note="check of the post-freeze reading only; the frozen label uses I2.limber_ratio")
P("KA_LC Limber C_L^pp shape / CLASS (norm. L 100) at L 20..400: frozen kernel " + " ".join(f"{x:.3f}" for x in shp_frozen) + "; k^-4 restored " + " ".join(f"{x:.3f}" for x in shp_fixed) + f" -> {'PASS' if KA['KA_LC']['pass_'] else 'FAIL'}")
ce2c = {}
for cn, (l0, pp_) in {"C1": (2.6102, 4.25), "C2": (1.4678, 3.5), "C3": (8.254, 5.625), "C4": (2.1544, 3.75)}.items():
    ee = min((e for e in q4["evaluated"] if abs(e["p"] - pp_) < 1e-9), key=lambda e: abs(math.log(e["lambda_0"] / l0)))
    Rc = solve3(kgrid, zgrid, jeans_all=kJ_of(ee["lambda_star"], ee["p"])) / ref
    ce2c[cn] = dict(frozen=gl_of(Rc), fixed=glc_of(Rc), iter4=ee["dchi2"])
P("CE2 cells re-read (reported): " + "; ".join(f"{c}: frozen d {v['frozen']['dchi2']:+.2f} (iter_4 {v['iter4']:.2f}), k^-4 restored chi2 {v['fixed']['chi2']:.2f} d {v['fixed']['dchi2']:+.2f}" for c, v in ce2c.items()))
ka_ok = all(v["pass_"] for k, v in KA.items() if k != "KA_LC")

RES = dict(lane="CK4", tag=TAG, criteria="16d0b4c6a5", background=dict(omega_b=OB, omega_d=OD, H0=H0, n_s=NS), c0=c0, KA=KA, CE2_cells_reread=ce2c,
           declared=dict(VESC_FAC=VESC_FAC, DVIR="18 pi^2 x rho_crit(z)", ST=dict(p=ST_P, q=ST_Q, delta_c=DC, A=A_ST)),
           note="kappa = 1/2 FITTED; not theory closed")
if not MUT:
    rows = {}
    for vk in VK:
        g = grade(vk, MMIN_P, "B"); rows[f"B_{vk:g}_1e11"] = g; P(line(f"PRIMARY B v_k {vk:g} M_min 1e11", g))
    for vk in VK:
        for mm in MMIN_BR:
            g = grade(vk, mm, "B"); rows[f"B_{vk:g}_{mm:.0e}"] = g; P(line(f"bracket B v_k {vk:g} M_min {mm:.0e}", g))
        for mm in (MMIN_P,) + MMIN_BR:
            g = grade(vk, mm, "A"); rows[f"A_{vk:g}_{mm:.0e}"] = g; P(line(f"bracket A v_k {vk:g} M_min {mm:.0e}", g))
    RES["rows"] = rows
    prim = {f"{vk:g}": rows[f"B_{vk:g}_1e11"]["pass_LGF"] for vk in VK}
    RES["primary_LGF_pass"] = prim
    primc = {f"{vk:g}": bool(rows[f"B_{vk:g}_1e11"]["GLc"]["pass_"] and rows[f"B_{vk:g}_1e11"]["GF"]["pass_"] and rows[f"B_{vk:g}_1e11"]["GFo"]["pass_"]) for vk in VK}
    RES["primary_LGF_pass_kernel_fixed"] = primc
    P("post-freeze reading, k^-4 restored, GLc+GF+GFo per v_k: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in primc.items()))
    P("primary GL+GF+GFo per v_k: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in prim.items()) + ("" if ka_ok else "  [KA FAIL: NO VERDICT]"))
else:
    m1 = grade(3000.0, MMIN_P, "B"); P(line("M1 v_k 3000 (must FAIL GL)", m1))
    m2pr = production(0.0, MMIN_P, "B"); d2 = solve3(kgrid, zgrid, m2pr); m2r = float(np.max(np.abs(d2 / ref - 1)))
    m2 = grade(0.0, MMIN_P, "B"); P(line("M2 v_k 0 (must equal cold case, pass)", m2) + f"; max |R-1| {m2r:.1e}")
    m3 = grade(575.0, 1e8, "A"); P(line("M3 reading A, M_min 1e8 (must FAIL GFo)", m3))
    RES["MUTATE"] = dict(M1=dict(row=m1, bites=bool(not m1["GL"]["pass_"])),
                         M2=dict(row=m2, max_rel=m2r, ok=bool(m2r <= 1e-9 and m2["pass_LGF"])),
                         M3=dict(row=m3, bites=bool(not m3["GFo"]["pass_"])))
    P(f"MUTATE: M1 {'BITES' if RES['MUTATE']['M1']['bites'] else 'DOES NOT BITE'}; M2 {'OK' if RES['MUTATE']['M2']['ok'] else 'NOT OK'}; M3 {'BITES' if RES['MUTATE']['M3']['bites'] else 'DOES NOT BITE'}")
RES["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6; RES["seconds"] = time.time() - T0
P(f"peak RSS {RES['peak_rss_MB']:.0f} MB; {RES['seconds']:.0f} s")


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
