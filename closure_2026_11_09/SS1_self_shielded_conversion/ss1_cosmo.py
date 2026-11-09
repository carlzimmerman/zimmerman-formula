#!/usr/bin/env python3
"""SS1 cosmology (FROZEN_CRITERIA.md b5adc7a90b + A1 9aeeb48503): gates 6 (background, bare Lambda; w = -0.85 product as a named
bracket), 7 (a) primary verification and (b) CMB lensing with the time-gated conversion, 8 forest + fsigma8; KA4 (LD1 replay and
the ratio-method validation at uniform decay), KA5 (baseline lensing chi^2, forest at R = 1), KA7 (Gamma0 -> 0 background).
    SS1_FOOT=canonical|alt python3 ss1_cosmo.py        -> parts/cosmo_<footing>.json
    SS1_MUTATE=M1..M4 SS1_FOOT=... python3 ss1_cosmo.py -> parts/cosmo_<footing>_M?.json
Read-only machinery: QX3 iter2 (CLASS, PR4 lensing data, A_s refit), GL1 / BG1 corrected Limber kernel (limber4, as WD1 / PJ1
carry it, own transcription with the SS1 background's distances), the record's two-fluid growth ODE (QX3 iter2 / BG1 form, own
transcription on the SS1 background), CFG681 DESI DR2 BAO table and Pantheon+ STAT+SYS shape, WD1 / NC2 G3 forest data and
p1d transform, CE2 fsigma8 rule (DESI DR1 rows as WD1 carries them), LD1 (ld1.json). CLASS runs are the record's own machinery
(RSS disclosed). kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, sys, json, math, time, tarfile, io, hashlib, resource, signal
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.special import erfc
from scipy.interpolate import CubicSpline
from scipy.linalg import cho_factor, cho_solve
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import ss1_core as C
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOT = os.environ.get("SS1_FOOT", "canonical"); MUT = C.MUT; SUFFIX = ("_" + MUT if MUT else "")
CLIGHT = 299792.458
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o
RES = dict(footing=FOOT, criteria=C.CRIT, amendment=C.AMEND, mutate=MUT, note=C.NOTE)
OUTN = f"cosmo_{FOOT}{SUFFIX}.json"
def dump(name=None): json.dump(clean(RES), open(os.path.join(PARTS, name or OUTN), "w"), indent=1)
def on_term(sig, frm): dump(OUTN.replace(".json", "_partial.json")); P("SIGTERM: partial written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)

def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try: exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
Q3 = load_prefix(os.path.join(CL6, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
Class, LMAX, ZPK = Q3["Class"], Q3["LMAX"], Q3["ZPK"]; CHI2_LINE = 18.48
Q15 = json.load(open(os.path.join(CL6, "QX15_cmb_primary_likelihood", "qx15.json")))
F1A = json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json"))); RCMB = float(F1A[FOOT]["R_B2"])
LD1J = json.load(open(os.path.join(CL6, "LD1_late_decaying_cold", "ld1.json")))
th = Q15["footings"][FOOT]["main"]["theta"]; H_REF = float(Q15["footings"][FOOT]["main"]["h"])
OB, OD, NS, TAU = th["omega_b"], th["omega_d"], th["n_s"], th["tau"]
OR = 2.469e-5 * (1 + 0.2271 * 3.046)                       # photons + 3.046 massless neutrinos (CLASS N_ur 3.046)
BASE = {'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': H_REF, 'omega_b': OB, 'omega_cdm': OD, 'A_s': Q3["AS0"], 'n_s': NS,
        'tau_reio': TAU, 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 210.0, 'z_max_pk': ZPK}

# ================================================================== reference CLASS
M = Class(); M.set(BASE); M.compute()
der = M.get_current_derived_parameters(['z_star', 'rs_d', 'z_d', '100*theta_s', 'rs_star'])
ZSTAR, RD = der['z_star'], der['rs_d']
X0 = Q3["X_of"](M); c0, A0ref = Q3["best_amp_chi2"](X0)
RES["reference"] = dict(h=H_REF, omega_b=OB, omega_chi=OD, R=OD / OB, R_F1A=RCMB, z_star=ZSTAR, r_d=RD, theta_s_100=der['100*theta_s'], rs_star=der['rs_star'], lensing_chi2=float(c0))
P(f"[{FOOT}] reference: h {H_REF:.5f} omega_b {OB:.6f} omega_chi {OD:.6f} (R {OD/OB:.4f}, F1A {RCMB:.4f}) z* {ZSTAR:.2f} r_d {RD:.3f} Mpc; lensing chi2 {c0:.4f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
KA5_REF = {"canonical": 8.559852345908991, "alt": 8.560405550735853}
RES["KA5_baseline"] = dict(chi2=float(c0), ref=KA5_REF[FOOT], pass_=bool(abs(c0 - KA5_REF[FOOT]) <= 1e-3))

# ================================================================== cosmic surviving share S(tau) (Press-Schechter on the footing's linear power)
OM = OB + OD; RHO_M0 = OM * 2.77536627e11                    # Msun / Mpc^3 (comoving)
kk = np.logspace(-4, math.log10(200.0), 3000); Pk_dec = np.array([M.pk_lin(k, C.Z_DEC) for k in kk])
def sigma_M(Mm):
    R = (3 * Mm / (4 * math.pi * RHO_M0)) ** (1 / 3); x = kk * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(np.trapz(Pk_dec * W * W * kk ** 3 / (2 * math.pi ** 2), np.log(kk)))
MED = np.logspace(6, 16, 41); MN = np.sqrt(MED[:-1] * MED[1:]); SIG = np.array([sigma_M(m) for m in MED]); DC = 1.686
F_PS = erfc(DC / (math.sqrt(2) * SIG))
def f_st(nu): A, a, p = 0.3222, 0.707, 0.3; return A * math.sqrt(2 * a / math.pi) * (1 + (a * nu * nu) ** -p) * np.exp(-a * nu * nu / 2)
def F_ST_of(s):
    nu0 = DC / s; nus = np.linspace(nu0, nu0 + 40, 20000); return float(np.trapz(f_st(nus), nus))
F_ST = np.array([F_ST_of(s) for s in SIG])
STEP_REC = 4; N_STEPS = int(round(C.TAU_TOT / C.DTAU)); TAUS = np.array([k * C.DTAU for k in range(0, N_STEPS + 1, STEP_REC)])
h_dec = H_REF; Om_dec = OM / H_REF ** 2
HALOS = [C.halo(m / (1 + C.F_CAP * OD / OB), OD / OB, h_dec, Om_dec, M200=m, Mchi=m * C.F_CAP * (OD / OB) / (1 + C.F_CAP * OD / OB)) for m in MN]
if C.GATE_OFF: RET = np.exp(-TAUS)[None, :] * np.ones((len(MN), 1))
else:
    PK = C.peel(HALOS, record_taus=list(TAUS))
    RET = np.array([[PK["snaps"][round(t, 6)][i].sum() / PK["M0"][i].sum() for t in TAUS] for i in range(len(MN))])
def S_of(Fcum):
    dF = Fcum[:-1] - Fcum[1:]; Ffield = 1.0 - Fcum[0]; return Ffield * np.exp(-TAUS) + (dF[:, None] * RET).sum(0), dF
S_PS, dF_PS = S_of(F_PS); S_ST, _ = S_of(F_ST)
RES["cosmic"] = dict(z_dec=C.Z_DEC, tau_tot=C.TAU_TOT, F_coll_PS_gt_1e6=float(F_PS[0]), F_coll_ST_gt_1e6=float(F_ST[0]), S0_PS=float(S_PS[-1]), S0_ST_bracket=float(S_ST[-1]),
                     S0_field_only=math.exp(-C.TAU_TOT), mass_nodes=MN, dF_PS=dF_PS, retention_today=RET[:, -1], x0_nodes=[C.x0_system(H) for H in HALOS],
                     halo_share_of_S0=float((dF_PS * RET[:, -1]).sum() / S_PS[-1]))
P(f"[{FOOT}] cosmic: F_coll(>1e6) PS {F_PS[0]:.3f} (ST {F_ST[0]:.3f}); surviving share today S0 {S_PS[-1]:.4f} (ST bracket {S_ST[-1]:.4f}; field only {math.exp(-C.TAU_TOT):.4f}); halo part {RES['cosmic']['halo_share_of_S0']:.2f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")

# ================================================================== background with the conversion (own integrator; physical densities omega)
ZG_BG = np.concatenate([np.linspace(0, 3, 3001), np.geomspace(3.001, 3600.0, 5000)])
def background(h, Sfun_tau, w_prod=1 / 3, conv=True, iters=4):
    """returns dict with z grid, E(z) h (=H/100), D_M(z) (Mpc), t(z) (Gyr), omega_chi(z) comoving share S, omega_prod(z)."""
    a = 1 / (1 + ZG_BG); lna = np.log(a); oL = None
    # start: t(z) from the no-conversion background
    Hh = lambda om_tot: 100 * np.sqrt(om_tot)                 # km/s/Mpc
    om_chi = OD * a ** -3 * np.ones_like(a); om_p = np.zeros_like(a)
    for it in range(iters):
        ol = h * h - OB - om_chi[0] - om_p[0] - OR                                  # flat today (a = 1 at index 0)
        om_tot = OB * a ** -3 + om_chi + om_p + OR * a ** -4 + ol
        H = Hh(om_tot); dt = 977.792 / H                                              # Gyr per unit ln a
        o = np.argsort(lna); t = np.zeros_like(lna); t[o] = np.concatenate([[0.0], np.cumsum(0.5 * (dt[o][1:] + dt[o][:-1]) * np.diff(lna[o]))])
        t = t + (0.0)                                                                # t relative to a_min; only differences used
        tdec = float(np.interp(math.log(1 / (1 + C.Z_DEC)), lna[o], t[o])); t0 = float(t[0])
        if not conv: break
        tau = np.where(ZG_BG < C.Z_DEC, C.TAU_TOT * (t - tdec) / (t0 - tdec), 0.0)
        S = Sfun_tau(tau); om_chi = OD * a ** -3 * S
        # product: d(om_p a^{3(1+w)})/dlna = a^{3(1+w)} * (-d(OD S)/dlna) a^{-3}
        dS = np.gradient(S[o], lna[o]); src = -OD * dS * a[o] ** -3 * a[o] ** (3 * (1 + w_prod))
        Y = np.concatenate([[0.0], np.cumsum(0.5 * (src[1:] + src[:-1]) * np.diff(lna[o]))]); om_p = np.zeros_like(a); om_p[o] = Y * a[o] ** (-3 * (1 + w_prod))
    ol = h * h - OB - om_chi[0] - om_p[0] - OR; om_tot = OB * a ** -3 + om_chi + om_p + OR * a ** -4 + ol; H = Hh(om_tot)
    zz = ZG_BG; f = CLIGHT / H; DM = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(zz))])
    return dict(z=zz, H=H, DM=DM, t=t, t0=t0, tdec=tdec, om_chi=om_chi, om_p=om_p, om_L=ol, S=om_chi / (OD * a ** -3), h=h)
def Sfun_cosmic(S_arr): return lambda tau: np.interp(tau, TAUS, S_arr)
S_ONE = lambda tau: np.ones_like(tau)
REFBG = background(H_REF, S_ONE, conv=False); DM_STAR = float(np.interp(ZSTAR, REFBG["z"], REFBG["DM"]))
def h_hold(Sfun, w_prod=1 / 3):
    return brentq(lambda hh: float(np.interp(ZSTAR, ZG_BG, background(hh, Sfun, w_prod)["DM"])) - DM_STAR, 0.45, 0.95, xtol=1e-7)

# ---------------- BAO (CFG681 DESI DR2 table) and Pantheon+ shape (CFG681 cuts), read-only transcription
ANISO = [("LRG1", 0.510, 13.588, 0.167, 21.863, 0.425, -0.459), ("LRG2", 0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
         ("LRG3+ELG1", 0.934, 21.576, 0.152, 17.641, 0.193, -0.416), ("ELG2", 1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
         ("QSO", 1.484, 30.512, 0.760, 12.817, 0.516, -0.500), ("Lya", 2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
BGS = (0.295, 7.942, 0.075)
EXT = os.path.join(REPO, "..", "_external_data", "pantheonplus_dr")
raw = np.genfromtxt(os.path.join(EXT, "PantheonPlusSH0ES.dat"), names=True, dtype=None, encoding=None)
covfull = np.loadtxt(os.path.join(EXT, "PantheonPlusSH0ES_STAT+SYS.cov"), skiprows=1); NSN = int(round(np.sqrt(covfull.size))); covfull = covfull.reshape(NSN, NSN)
sel = (raw["IS_CALIBRATOR"] == 0) & (raw["zHD"] > 0.01)
zhd, zhel, mb = raw["zHD"][sel], raw["zHEL"][sel], raw["m_b_corr"][sel].astype(float); Cisn = np.linalg.inv(covfull[np.ix_(sel, sel)]); one = np.ones(len(mb)); A11 = one @ Cisn @ one
del covfull
def bao_sn(bg, rd=RD, profile_rd=False):
    DM = lambda z: float(np.interp(z, bg["z"], bg["DM"])); DH = lambda z: CLIGHT / float(np.interp(z, bg["z"], bg["H"]))
    ms, ds, Cis = [], [], []
    for (nm, z, dm, sdm, dh, sdh, r) in ANISO:
        ms.append(np.array([DM(z), DH(z)])); ds.append(np.array([dm, dh])); Cis.append(np.linalg.inv(np.array([[sdm ** 2, r * sdm * sdh], [r * sdm * sdh, sdh ** 2]])))
    z, dv, sdv = BGS; mv = (z * DM(z) ** 2 * DH(z)) ** (1 / 3)
    if profile_rd:
        num = sum(m @ Ci @ d for m, d, Ci in zip(ms, ds, Cis)) + mv * dv / sdv ** 2; den = sum(m @ Ci @ m for m, Ci in zip(ms, Cis)) + mv * mv / sdv ** 2; q = num / den
    else: q = 1.0 / rd
    cb = sum((d - q * m) @ Ci @ (d - q * m) for m, d, Ci in zip(ms, ds, Cis)) + ((dv - q * mv) / sdv) ** 2
    mu = 5 * np.log10((1 + zhel) * np.interp(zhd, bg["z"], bg["DM"])); rr = mb - mu; b = one @ Cisn @ rr; cs = float(rr @ Cisn @ rr - b * b / A11)
    pull = {nm: dict(DM=float(DM(z)), DH=float(DH(z))) for (nm, z, *_ ) in ANISO}
    return dict(bao=float(cb), sn=cs, tot=float(cb + cs), rd_over=1 / q, at=pull)

# ================================================================== growth (record's two-fluid ODE on a given background) and lensing (limber4)
KG = np.logspace(-4, math.log10(200.0), 100); ZG = np.linspace(0.02, ZPK, 120)
def growth_source(bg):
    """returns at ZG: source ratio pieces for the given background: delta_b, delta_chi (scale-free, sub-horizon), and densities."""
    lna_t = np.log(1 / (1 + bg["z"])); o = np.argsort(lna_t); lna_t = lna_t[o]; lnH = np.log(bg["H"][o]); dlnH = np.gradient(lnH, lna_t)
    Sg = bg["S"][o]; ai = 1 / 3401.0; adec = 1 / 1091.0
    grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 8001), np.log(1 / (1 + ZG))]))
    y = np.array([ai, ai, 0.0, 0.0]); rec = {}; tset = {float(x): i for i, x in enumerate(np.log(1 / (1 + ZG)))}
    H0c = 100.0
    def A(lm):
        a = math.exp(lm); E2 = math.exp(2 * np.interp(lm, lna_t, lnH)) / H0c ** 2
        S = float(np.interp(lm, lna_t, Sg)); Od = OD * a ** -3 * S / E2; Ob = OB * a ** -3 / E2; dl = float(np.interp(lm, lna_t, dlnH))
        Am = np.zeros((4, 4)); Am[0, 1] = 1; Am[1, 0] = 1.5 * Od; Am[1, 1] = -(2 + dl)
        if a > adec: Am[1, 2] = 1.5 * Ob; Am[2, 3] = 1; Am[3, 0] = 1.5 * Od; Am[3, 2] = 1.5 * Ob; Am[3, 3] = -(2 + dl)
        return Am
    I4 = np.eye(4)
    for n in range(len(grid) - 1):
        h_ = grid[n + 1] - grid[n]; Am = A(0.5 * (grid[n] + grid[n + 1])); y = np.linalg.solve(I4 - 0.5 * h_ * Am, (I4 + 0.5 * h_ * Am) @ y)
        if float(grid[n + 1]) in tset: rec[tset[float(grid[n + 1])]] = y.copy()
    Sz = np.interp(ZG, bg["z"], bg["S"])
    db = np.array([rec[j][2] for j in range(len(ZG))]); dc = np.array([rec[j][0] for j in range(len(ZG))])
    ddb = np.array([rec[j][3] for j in range(len(ZG))]); ddc = np.array([rec[j][1] for j in range(len(ZG))])
    src = OB * db + OD * Sz * dc                                                        # comoving physical source (x a^-3 common)
    dm = src / (OB + OD * Sz)
    return dict(src=src, dm=dm, db=db, dc=dc, ddb=ddb, ddc=ddc, S=Sz)
PREF = np.array([[M.pk_lin(k, z) for z in ZG] for k in KG])
def limber4_bg(bg, Rkz):
    """GL1 / BG1 corrected Limber kernel (k^-4 factor) with the given background's distances; returns S(L) = C_L / C_L^ref
    where the reference uses REFBG and R = 1."""
    def CL(bgx, R):
        chis = float(np.interp(ZSTAR, bgx["z"], bgx["DM"])); chi = np.interp(ZG, bgx["z"], bgx["DM"]); Hz = np.interp(ZG, bgx["z"], bgx["H"])
        w = ((chis - chi) / (chi * chis)) ** 2 * (1 + ZG) ** 2 / Hz; lnk = np.log(KG); Ls = np.arange(2, LMAX + 1); out = np.zeros(len(Ls))
        for j in range(len(ZG)):
            kx = (Ls + 0.5) / chi[j]; m = (kx >= KG[0]) & (kx <= KG[-1])
            Pj = np.interp(np.log(kx[m]), lnk, PREF[:, j]); Rj = np.interp(np.log(kx[m]), lnk, R[:, j]); ex = (chi[j] / (Ls[m] + 0.5)) ** 4
            out[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex
        return Ls, out
    Ls, cr = CL(REFBG, np.ones((len(KG), len(ZG)))); _, cs = CL(bg, Rkz)
    S = np.ones(LMAX + 1); ok = cr > 0; S[Ls[ok]] = cs[ok] / cr[ok]; return S
GREF = growth_source(REFBG)
def lens_eval(bg):
    g = growth_source(bg); Rz = g["src"] / GREF["src"]; Rkz = np.tile(Rz, (len(KG), 1)); S = limber4_bg(bg, Rkz)
    c, A = Q3["best_amp_chi2"](X0 * S); return dict(chi2=float(c), A_refit=float(A), S_L={f"L {L}": float(S[L]) for L in (10, 40, 100, 200, 400)},
                                                   R_src={f"z {z}": float(np.interp(z, ZG, Rz)) for z in (0.05, 0.3, 0.55, 1.0, 2.0)}), g, Rkz
# fsigma8 (CE2 rule as WD1 carries it): ratio of d sigma8 / d ln a with sigma8 from the clustering-matter contrast
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
        ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]
def fs8_eval(g):
    lna_z = np.log(1 / (1 + ZG)); oo = np.argsort(lna_z)
    def rat(x, xr):
        d1 = CubicSpline(lna_z[oo], x[oo]).derivative()(lna_z); d2 = CubicSpline(lna_z[oo], xr[oo]).derivative()(lna_z); return d1 / d2
    rm = rat(g["dm"], GREF["dm"]); rv = rat(g["db"], GREF["db"])
    rows = []
    for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
        e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = float(np.interp(z, ZG, rm))
        rows.append(dict(bin=t, z=z, Rf=x, Rf_velocity_tracer_reported=float(np.interp(z, ZG, rv)), in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
    return dict(rows=rows, pass_=bool(all(r["in_sf"] and r["in_sfb"] and r["s8dir"] for r in rows)))

# ================================================================== forest (WD1 / NC2 G3 machinery, own transcription)
def forest_setup():
    RAW = os.path.join(REPO, "_external_data", "desi_dr1_p1d_qmle", "raw", "data_points.tar")
    from astropy.io import fits
    md5 = hashlib.md5()
    with open(RAW, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 22), b""): md5.update(blk)
    with tarfile.open(RAW) as tf: HD = fits.open(io.BytesIO(tf.extractfile("desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits").read()))
    T = HD["P1D_BLIND"].data; Zall, Kall, Pall = np.asarray(T["Z"], float), np.asarray(T["K"], float), np.asarray(T["PLYA"], float); Cf = np.asarray(HD["COVARIANCE"].data, float)
    ZB = np.round(np.unique(Zall), 2); LLYA, DLAM = 1215.67, 0.8
    kmaxz = lambda z: 0.5 * math.pi / (CLIGHT * DLAM / ((1 + z) * LLYA)); SEL = np.zeros(len(Zall), bool)
    for z in ZB: SEL |= (np.round(Zall, 2) == z) & (Kall > 0.001) & (Kall < kmaxz(z))
    zs, ks, Pd = np.round(Zall[SEL], 2), Kall[SEL], Pall[SEL]; Cs = Cf[np.ix_(SEL, SEL)]; CF = cho_factor(0.5 * (Cs + Cs.T))
    return dict(md5=md5.hexdigest(), ZB=ZB, zs=zs, ks=ks, Pd=Pd, CF=CF, NB=int(SEL.sum()))
KF = np.exp(np.linspace(math.log(1e-4), math.log(200.0), 60000))
def p1d_at(kpar, Pk):
    f = KF * Pk; seg = 0.5 * (f[1:] + f[:-1]) * np.diff(KF); cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]); return np.interp(np.log(kpar), np.log(KF), cum) / (2 * math.pi)
def forest_eval(FD, bg, Rkz):
    """P1D ratio of the SS1 model to the reference at the data points; k_par conversion with each model's own H(z)."""
    ksamp = np.exp(np.linspace(math.log(1e-4), math.log(0.999 * 200.0), 700)); r = np.empty(FD["NB"]); lk = np.log(KG)
    for z in FD["ZB"]:
        s_ = FD["zs"] == z; lp = np.log([M.pk_lin(float(k_), float(z)) for k_ in ksamp]); PL = np.exp(CubicSpline(np.log(ksamp), lp, extrapolate=True)(np.log(KF)))
        Href = float(np.interp(z, REFBG["z"], REFBG["H"])); Hss = float(np.interp(z, bg["z"], bg["H"]))
        jz = int(np.argmin(abs(ZG - z))); Rk = np.interp(np.log(KF), lk, Rkz[:, jz])
        kp_ref = FD["ks"][s_] * Href / (1 + z); kp_ss = FD["ks"][s_] * Hss / (1 + z)
        r[s_] = (p1d_at(kp_ss, PL * Rk ** 2) * Hss) / (p1d_at(kp_ref, PL) * Href)            # P1D in velocity units: P_v = P_comoving x H/(1+z)
    d = (r - 1.0) * FD["Pd"]; dch = float(d @ cho_solve(FD["CF"], d))
    return dict(dchi2=dch, status="PASS" if dch <= 4 else "FAIL", r_min=float(r.min()), r_max=float(r.max()))

# ================================================================== run
# KA7: Gamma0 -> 0 returns the reference h and chi^2
h0chk = h_hold(S_ONE); bs_ref = bao_sn(REFBG); bs0 = bao_sn(background(h0chk, S_ONE))
RES["KA7"] = dict(h=h0chk, h_ref=H_REF, chi2=bs0["tot"], chi2_ref=bs_ref["tot"], pass_=bool(abs(h0chk - H_REF) <= 1e-5 and abs(bs0["tot"] - bs_ref["tot"]) <= 1e-6 * max(1, bs_ref["tot"])))
P(f"[{FOOT}] KA7 Gamma0 -> 0: h {h0chk:.7f} vs {H_REF:.7f}; BAO+SN chi2 {bs0['tot']:.6f} vs {bs_ref['tot']:.6f} -> {'PASS' if RES['KA7']['pass_'] else 'FAIL'}")
# gate 6: background
SF = Sfun_cosmic(S_PS)
h_ss = h_hold(SF); BG = background(h_ss, SF); bs = bao_sn(BG)
BGfix = background(H_REF, SF); dth = float(np.interp(ZSTAR, BGfix["z"], BGfix["DM"])) / DM_STAR - 1
bs_prof_ref = bao_sn(REFBG, profile_rd=True); bs_prof = bao_sn(BG, profile_rd=True)
shifts = {nm: dict(DM_pct=100 * (bs["at"][nm]["DM"] / bs_ref["at"][nm]["DM"] - 1), DH_pct=100 * (bs["at"][nm]["DH"] / bs_ref["at"][nm]["DH"] - 1)) for nm in bs["at"]}
d6 = bs["tot"] - bs_ref["tot"]
RES["G6"] = dict(status="PASS" if d6 <= 4 else "FAIL", dchi2=d6, dchi2_bao=bs["bao"] - bs_ref["bao"], dchi2_sn=bs["sn"] - bs_ref["sn"], chi2=bs, chi2_ref=bs_ref, h=h_ss, h_ref=H_REF,
                 Omega_L=BG["om_L"] / h_ss ** 2, Omega_dr0=BG["om_p"][0] / h_ss ** 2, Omega_chi0=BG["om_chi"][0] / h_ss ** 2, S0=float(BG["S"][0]), shifts_pct=shifts,
                 theta_s_shift_if_h_not_resolved=-dth, profiled_rd_reading=dict(dchi2=bs_prof["tot"] - bs_prof_ref["tot"], rd_fit=bs_prof["rd_over"], rd_fit_ref=bs_prof_ref["rd_over"]),
                 lookback_Gamma0_tau=C.GAMMA0_GYR * (BG["t0"] - BG["tdec"]), S0_ST_bracket_dchi2=None)
h_st = h_hold(Sfun_cosmic(S_ST)); RES["G6"]["S0_ST_bracket_dchi2"] = bao_sn(background(h_st, Sfun_cosmic(S_ST)))["tot"] - bs_ref["tot"]
h_w = h_hold(SF, -0.85); BGw = background(h_w, SF, -0.85); bw = bao_sn(BGw)
RES["G6_bracket_w085_sector"] = dict(note="separate sector (conversion product with w = -0.85, not radiation); bracket, never grades", h=h_w, dchi2=bw["tot"] - bs_ref["tot"], dchi2_bao=bw["bao"] - bs_ref["bao"], dchi2_sn=bw["sn"] - bs_ref["sn"])
P(f"[{FOOT}] G6 background (bare Lambda): h {H_REF:.4f} -> {h_ss:.4f} (theta_s held); S0 {BG['S'][0]:.4f}, Omega_dr0 {RES['G6']['Omega_dr0']:.4f}, Omega_L {RES['G6']['Omega_L']:.4f}; "
  f"Delta chi2 BAO {RES['G6']['dchi2_bao']:+.2f} SN {RES['G6']['dchi2_sn']:+.2f} total {d6:+.2f} -> {RES['G6']['status']}; DM shift % " + " ".join(f"{k} {v['DM_pct']:+.2f}" for k, v in shifts.items())
  + f"; r_d-profiled {RES['G6']['profiled_rd_reading']['dchi2']:+.2f}; theta_s shift if h kept {-dth:+.4%}; ST bracket {RES['G6']['S0_ST_bracket_dchi2']:+.2f}; w=-0.85 bracket {bw['tot']-bs_ref['tot']:+.2f} (h {h_w:.4f})  [{time.time()-T0:.0f}s {rss():.2f}GB]")
dump()
# gate 7(a): primary verification
RES["G7a"] = dict(verified=True, omega_b=OB, omega_chi_before_zdec=OD, N_eff=3.046, r_s_star=der['rs_star'], DM_star_ref=DM_STAR, DM_star_SS1=float(np.interp(ZSTAR, BG["z"], BG["DM"])),
                  S_above_zdec_max_dev=float(np.max(np.abs(BG["S"][BG["z"] > C.Z_DEC + 1e-9] - 1.0))), late_ISW="NOT EVALUATED (as LD1)")
# gate 7(b) and 8
L7, G7g, Rkz = lens_eval(BG); RES["G7b"] = dict(L7, status="PASS" if L7["chi2"] <= CHI2_LINE else "FAIL", line=CHI2_LINE, LD1_line_reference=dict(LD1_chi2=LD1J["footings"][FOOT]["D1_chi2"]))
P(f"[{FOOT}] G7b CMB lensing (time-gated conversion, SS1 background): chi2 {L7['chi2']:.3f} (line {CHI2_LINE}, baseline {c0:.3f}, LD1 {LD1J['footings'][FOOT]['D1_chi2']:.2f}) A refit x {L7['A_refit']/A0ref:.4f} -> {RES['G7b']['status']}; S_L " + " ".join(f"{k}:{v:.3f}" for k, v in L7["S_L"].items()) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")
FS = fs8_eval(G7g); RES["G8_growth"] = FS
P(f"[{FOOT}] G8 fsigma8: " + " ".join(f"{r['bin']} {r['Rf']:.3f} (vel {r['Rf_velocity_tracer_reported']:.3f})" for r in FS["rows"]) + f" -> {'PASS' if FS['pass_'] else 'FAIL'}")
dump()
FD = forest_setup(); RES["forest_data"] = dict(md5=FD["md5"], md5_ok=FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433", nbins=FD["NB"])
fr1 = forest_eval(FD, REFBG, np.ones((len(KG), len(ZG)))); FR = forest_eval(FD, BG, Rkz)
RES["KA5_forest_R1"] = dict(dchi2=fr1["dchi2"], pass_=bool(fr1["dchi2"] <= 1e-9)); RES["G8_forest"] = FR
RES["G8"] = dict(status="PASS" if (FS["pass_"] and FR["status"] == "PASS") else "FAIL")
P(f"[{FOOT}] G8 forest: dchi2 {FR['dchi2']:.4f} (ratio {FR['r_min']:.5f}-{FR['r_max']:.5f}) -> {FR['status']}; KA5 forest at R=1 {fr1['dchi2']:.1e}; G8 {RES['G8']['status']}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
dump()
# KA4: LD1 replay and the ratio-method validation at uniform decay (main run only)
if not MUT:
    L1 = LD1J["footings"][FOOT]; gam = L1["Gamma_kmsMpc"]
    def run_dcdm(h, gam):
        Mx = Class(); p = dict(BASE, h=h, omega_cdm=1e-7, omega_ini_dcdm=OD, Gamma_dcdm=gam); p.pop('P_k_max_1/Mpc'); p.pop('z_max_pk'); p['output'] = 'tCl,lCl'
        Mx.set(p); Mx.compute(); X = Q3["X_of"](Mx); c, A = Q3["best_amp_chi2"](X); Mx.struct_cleanup(); Mx.empty(); return float(c)
    c_ld1 = run_dcdm(L1["h"], gam); c_cls = run_dcdm(H_REF, gam)
    lifetime = 977.792 / gam
    def S_uniform_bg(h):
        """uniform decay from the start at LD1's Gamma: S(t) = exp(-t / lifetime), t from the background's own clock."""
        a = 1 / (1 + ZG_BG); lna = np.log(a); o = np.argsort(lna); om_chi = OD * a ** -3; om_p = np.zeros_like(a)
        for it in range(6):
            ol = h * h - OB - om_chi[0] - om_p[0] - OR; H = 100 * np.sqrt(OB * a ** -3 + om_chi + om_p + OR * a ** -4 + ol); dt = 977.792 / H
            t = np.zeros_like(lna); t[o] = np.concatenate([[0.0], np.cumsum(0.5 * (dt[o][1:] + dt[o][:-1]) * np.diff(lna[o]))])
            S = np.exp(-t / lifetime); om_chi = OD * a ** -3 * S
            dS = np.gradient(S[o], lna[o]); src = -OD * dS * a[o] ** -3 * a[o] ** 4
            Y = np.concatenate([[0.0], np.cumsum(0.5 * (src[1:] + src[:-1]) * np.diff(lna[o]))]); om_p = np.zeros_like(a); om_p[o] = Y * a[o] ** -4
        ol = h * h - OB - om_chi[0] - om_p[0] - OR; H = 100 * np.sqrt(OB * a ** -3 + om_chi + om_p + OR * a ** -4 + ol)
        f = CLIGHT / H; DM = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(ZG_BG))])
        return dict(z=ZG_BG, H=H, DM=DM, S=om_chi / (OD * a ** -3))
    Lu, _, _ = lens_eval(S_uniform_bg(H_REF))
    tol = 0.15 * abs(c_cls - c0); okv = abs(Lu["chi2"] - c_cls) <= tol
    RES["KA4"] = dict(LD1_replay=dict(chi2=c_ld1, ref=L1["D1_chi2"], pass_=bool(abs(c_ld1 - L1["D1_chi2"]) <= 0.05)),
                      ratio_method_validation=dict(Gamma=gam, h=H_REF, chi2_CLASS_dcdm=c_cls, chi2_ratio_method=Lu["chi2"], tolerance=tol, pass_=bool(okv)))
    RES["KA4"]["pass_"] = bool(RES["KA4"]["LD1_replay"]["pass_"] and okv)
    P(f"[{FOOT}] KA4 LD1 replay chi2 {c_ld1:.3f} vs {L1['D1_chi2']:.3f}; ratio method at uniform decay {Lu['chi2']:.3f} vs CLASS dcdm {c_cls:.3f} (tol {tol:.2f}) -> {'PASS' if RES['KA4']['pass_'] else 'FAIL'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
M.struct_cleanup(); M.empty()
RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0
dump(); P(f"cosmo {FOOT}{SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
