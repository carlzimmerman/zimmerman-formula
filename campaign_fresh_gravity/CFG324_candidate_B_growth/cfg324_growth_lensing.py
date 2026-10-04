#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG324 part 1 -- CANDIDATE B'S LARGE-SCALE GROWTH, derived per reading of B's declared rule, scored on Planck 2018 CMB lensing.

Frozen criteria: FROZEN_CRITERIA.md in this folder (committed alone, 197ee7c08).  kappa = 1/2 FITTED and fixed; both footings
(9.3603e-11 / 1.1312e-10 m/s^2); nu_mono.  The cold component (Omega_c h^2 = 0.1200) is kept in every reading: the mass is
still required and it is not a particle species.  Nothing here says the theory is closed.

READINGS (never pooled; FROZEN_CRITERIA section 1):
  R1  bound-only switch (T3, Delta(<r) >= Delta_ta) + identity bookkeeping (T5) + FG001  -- B as declared
  R2  bound-only switch + ADDITIVE bookkeeping (the bound regions' phantom adds; CFG4_switch H6 / S5), variants est and min
  R3  acceleration door (ON where y_b > y_th <= 2.1e-5; CFG4 H3 field-strength row, 09-26 'all doors', MS1): baryon-sourced
      nu_mono boost on the whole linear web from z = 100
CONTROLS: C1 LCDM (XR26 chi^2, Limber vs CLASS, ODE vs CLASS D); C2 the chassis 'all matter feels nu_mono' (audit harness);
C4 R3's premise (delta_b/delta_cdm at z = 100); C5 the harness's nu_mono = FP1's.  MUTATE (CFG324_MUTATE=1): R1's growth
boosted x2 in amplitude for z <= 10; its lensing row must FAIL (rc = 1).

Run from the repository root:  python3 campaign_fresh_gravity/CFG324_candidate_B_growth/cfg324_growth_lensing.py
"""
import os, sys, io, json, math, time, hashlib, contextlib, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg324_common as K
sys.path.insert(0, K.CFG)
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erfc
from classy import Class

warnings.filterwarnings("ignore")
R = K.Run("cfg324_growth_lensing")
P, banner, check = R.P, R.banner, R.check
P(__doc__.strip())
if K.MUTATE:
    P("\n  *** MUTATE=1: R1's growth is boosted x2 in amplitude for z <= 10 (P x 4, f sigma_8 x 2); R1's lensing row must FAIL ***")
import CFG4_common as C4                                           # read-only executor and FP1's committed nu_mono
trapz = K.trapz

# ================================================================================================ inputs (committed)
XR26 = os.path.join(C4.HUB, "XR26_cmb.py")
XI = C4.exec_slices(XR26, [("# ================================================================================================ inputs (published, committed)",
                            "fp0 = json.load(")], ns={"np": np, "math": math}, name="xr26_inputs")[0]
PL18_MV, LENS_AMP, P18 = XI["PL18_MV"], XI["LENS_AMP"], XI["P18"]
J26 = json.load(open(os.path.join(C4.HUB, "XR26_cmb_results.json")))["numbers"]
H0F = J26["K1"]["H0"] / 100.0
BASEPAR = {"h": H0F, "omega_b": P18["omega_b"], "omega_cdm": P18["omega_cdm"], "tau_reio": P18["tau_reio"],
           "ln_A_s_1e10": P18["ln_A_s_1e10"], "n_s": P18["n_s"], "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "YHe": J26["K1"]["YHe"]}
LA = LENS_AMP["8-400"]
# f sigma_8 points typed in CFG4_cosmology.py (published): 6dFGS, SDSS MGS, BOSS DR12, eBOSS DR16 (reported only)
FS8 = [(0.067, 0.423, 0.055), (0.15, 0.53, 0.16), (0.38, 0.497, 0.045), (0.51, 0.458, 0.038), (0.61, 0.436, 0.034),
       (0.70, 0.473, 0.041), (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)]
SW = json.load(open(os.path.join(K.CFG, "CFG4_switch_results.json")))["numbers"]["D1"]
TB = json.load(open(os.path.join(K.CFG, "CFG4_target_results.json")))["numbers"]["H3"]["budget"]
ZD1 = np.array(sorted(float(z) for z in SW))
DLTA = np.array([SW[str(z) if str(z) in SW else f"{z}"]["delta_lin_ta"] for z in ZD1])
OPDTA = np.array([SW[str(z) if str(z) in SW else f"{z}"]["one_plus_delta_ta"] for z in ZD1])
dlin_ta = lambda z: float(np.interp(z, ZD1, DLTA))                 # held at z = 3's value above (record table ends there)
opd_ta = lambda z: float(np.interp(z, ZD1, OPDTA))
XE = "0.4"                                                         # B's declared density edge x_e (GATES line 14)
OMPH = {f: {0.0: TB[f"{f}|nu_mono|z0.0|m7.0"][XE][0], 0.25: TB[f"{f}|nu_mono|z0.25|m7.0"][XE][0]} for f in K.FOOTS}
OM0_T = 0.3153                                                     # CFG4_target's Omega_m (its budget's normalisation)
P(f"\n  inputs: XR26 Planck 2018 (h = {H0F:.5f}); lensing gate {LA[0]} +- {LA[1]} (8-400, 9 MV bins); CFG4_switch D1 turnaround table "
  f"z = {ZD1.min():g}-{ZD1.max():g}; CFG4_target phantom budget at x_e = {XE}: " +
  "; ".join(f"{f} Omega_ph(z=0) {OMPH[f][0.0]:.4f}, (z=0.25) {OMPH[f][0.25]:.4f}" for f in K.FOOTS))

# ================================================================================================ CLASS
banner("C1  CONTROLS: CLASS at XR26's parameters (lensing chi^2, amplitude), this lane's Limber vs CLASS, the growth ODE vs CLASS D(z)")
t0 = time.time()
cl = Class()
cl.set(dict(BASEPAR, output="tCl,pCl,lCl,mPk", lensing="yes", l_max_scalars=3500, non_linear="halofit",
            **{"P_k_max_h/Mpc": 30.0, "z_max_pk": 50.0}))
cl.compute()
CPP = cl.lensed_cl(2500)["pp"]
hC = cl.h()
BG = cl.get_background()
zbg = BG["z"][::-1]; Hbg = BG["H [1/Mpc]"][::-1]; chibg = BG["comov. dist."][::-1]
rcb = (BG["(.)rho_cdm"] + BG["(.)rho_b"])[::-1]; rcr = BG["(.)rho_crit"][::-1]
Om_tot0 = cl.Omega_m()
der = cl.get_current_derived_parameters(["z_rec", "conformal_age", "tau_rec"])
CHI_STAR = der["conformal_age"] - der["tau_rec"]
chi_of = lambda z: np.interp(z, zbg, chibg)
H_of = lambda z: np.interp(z, zbg, Hbg)
Ocb_of = lambda z: np.interp(z, zbg, rcb / rcr)


def bandpowers(cpp, rng="8-400"):
    out = []
    for (lo, hi, A_, sA, fid) in PL18_MV[rng]:
        ll = np.arange(lo, hi + 1)
        out.append(1e7 * np.mean((ll * (ll + 1.0)) ** 2 * cpp[ll] / (2 * math.pi)))
    return np.array(out)


DAT = np.array([b_[2] * b_[4] for b_ in PL18_MV["8-400"]]); ERR = np.array([b_[3] * b_[4] for b_ in PL18_MV["8-400"]])
W8 = 1 / np.array([b_[3] for b_ in PL18_MV["8-400"]]) ** 2
BP_L = bandpowers(CPP)


def score(cpp):
    bp = bandpowers(cpp)
    A_ = float(np.sum(W8 * bp / BP_L) / np.sum(W8))
    return dict(amp=A_, chi2=float(np.sum(((DAT - bp) / ERR) ** 2)), pull=(A_ - LA[0]) / LA[1])


S_L = score(CPP)
P(f"    LCDM: chi^2 {S_L['chi2']:.4f} (XR26 committed {J26['L2']['8-400']['chi2_lcdm']:.4f}); amplitude {S_L['amp']:.4f}, pull {S_L['pull']:+.2f} "
  f"sigma; sigma_8 {cl.sigma8():.4f} ({time.time() - t0:.0f} s)")
check("C1a CONTROL: CLASS at XR26's parameters reproduces XR26's LCDM lensing chi^2 (to 1e-3) and lies within 2 sigma of Planck's 1.011 +- 0.028",
      f"chi^2 {S_L['chi2']:.5f} vs {J26['L2']['8-400']['chi2_lcdm']:.5f}; pull {S_L['pull']:+.2f}",
      abs(S_L["chi2"] - J26["L2"]["8-400"]["chi2_lcdm"]) < 1e-3 and abs(S_L["pull"]) <= 2)

# Limber on CLASS spectra
ZL = np.concatenate([np.geomspace(1e-3, 1.0, 90), np.geomspace(1.0, 50.0, 140)[1:]])
CHL = chi_of(ZL)
LG = np.unique(np.round(np.geomspace(8, 400, 70)).astype(int))
KMAX = 30.0 * hC
PK = {}
for base in ("lin", "NL"):
    arr = np.zeros((len(LG), len(ZL)))
    for j, (z_, ch) in enumerate(zip(ZL, CHL)):
        for i, L in enumerate(LG):
            k = (L + 0.5) / ch
            if k < KMAX:
                arr[i, j] = cl.pk_lin(k, z_) if base == "lin" else cl.pk(k, z_)
    PK[base] = arr
WGT = ((CHI_STAR - CHL) / CHI_STAR) ** 2 * (1.5 * Om_tot0 * (cl.Hubble(0)) ** 2 * (1 + ZL)) ** 2


def limber(base, F=None):
    """C_L^pp on LG for P_X = F(z) * P_base (F: array over ZL, scale independent)."""
    Fz = np.ones_like(ZL) if F is None else F
    return np.array([4.0 / (L + 0.5) ** 4 * trapz(WGT * Fz * PK[base][i], CHL) for i, L in enumerate(LG)])


LIM0 = {b: limber(b) for b in ("lin", "NL")}
ll8 = np.arange(8, 401)
lim_class_ratio = float(np.mean(np.interp(ll8, LG, LIM0["NL"]) / CPP[ll8]))
P(f"    Limber (halofit, z <= 50) / CLASS C_L^pp averaged over 8-400: {lim_class_ratio:.4f}")
check("C1b CONTROL: this lane's Limber integral on CLASS's halofit P(k, z) agrees with CLASS's C_L^pp to <= 1% averaged over 8-400",
      f"ratio {lim_class_ratio:.4f}", abs(lim_class_ratio - 1) <= 0.01)


def cpp_X(base, F):
    """CLASS C_L^pp times the Limber ratio for a scale-independent modification F(z) of P on the given base."""
    Rr = limber(base, F) / LIM0[base]
    cpp = CPP.copy()
    cpp[ll8] = CPP[ll8] * np.interp(ll8, LG, Rr)
    return cpp


def lens_scores(F):
    return {b: score(cpp_X(b, F)) for b in ("lin", "NL")}


# growth ODE on CLASS's background (source: the clustering cold component + baryons)
NI = math.log(1 / 51.0)


def growth_class(q_of=None):
    """D'' + (2 + dlnH/dN) D' = 1.5 Omega_cb(a) [1 + q(z)] D, from z = 50 in the growing mode; returns dense solution."""
    def rhs(N, Y):
        a = math.exp(N); z = 1 / a - 1
        e = 1e-4
        za, zb = (1 / math.exp(N - e) - 1), (1 / math.exp(N + e) - 1)
        dlnH = (math.log(H_of(zb)) - math.log(H_of(za))) / (2 * e)
        q = 0.0 if q_of is None else q_of(z)
        return [Y[1], 1.5 * Ocb_of(z) * (1 + q) * Y[0] - (2 + dlnH) * Y[1]]
    return solve_ivp(rhs, (NI, 0.0), [1.0, 1.0], method="DOP853", rtol=1e-10, atol=1e-13, dense_output=True)


GL = growth_class()
zc = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0])
Dode = np.array([GL.sol(math.log(1 / (1 + z)))[0] for z in zc]); Dode /= Dode[0]
Dcls = np.array([cl.scale_independent_growth_factor(z) for z in zc]); Dcls /= Dcls[0]
dmax = float(np.max(np.abs(Dode / Dcls - 1)))
P("    D(z)/D(0): ODE " + ", ".join(f"z={z:g}: {a:.4f}" for z, a in zip(zc, Dode)) + " | CLASS " + ", ".join(f"{a:.4f}" for a in Dcls))
check("C1c CONTROL: the R1 growth ODE on CLASS's background matches CLASS's D(z)/D(0) to <= 0.5% for z <= 5", f"max |dev| {dmax:.2e}", dmax <= 0.005)
R.num("C1", dict(lcdm=S_L, limber_over_class=lim_class_ratio, ode_vs_class_maxdev=dmax, chi_star=CHI_STAR))


def Dfun(sol):
    return lambda z: float(sol.sol(math.log(1 / (1 + z)))[0])


def fz(sol, z):
    y = sol.sol(math.log(1 / (1 + z)))
    return float(y[1] / y[0])


DL = Dfun(GL)
S8Z = lambda z: cl.sigma(8.0 / hC, z)
FS8_L = {z: cl.scale_independent_growth_factor_f(z) * S8Z(z) for z, _, _ in FS8}
chi_rsd_L = sum(((FS8_L[z] - v) / e) ** 2 for z, v, e in FS8)
ZFS = np.round(np.arange(0.0, 0.2001, 0.005), 4)                  # the velocity script's interpolation grid

# ================================================================================================ the audit harness (chassis, R3)
banner("C2  CONTROL: the chassis 'all matter feels nu_mono' in the audit's harness (L341's machinery) reproduces sigma_8 and its lensing exclusion")
SRC = os.path.join(K.CFG, "AUDIT_SIGMA8_2026-10-03", "L341_rerun_copy.py")
ORIG = os.path.join(K.REPO, "real_research", "g03_audit_2026", "L341_chk_frw_gate.py")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
assert sha(SRC) == sha(ORIG), "the L341 copy differs from L341's committed script"
code = open(SRC).read(); cut = code.index('banner("F1')
ns = {"__file__": SRC, "__name__": "l341_defs"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), ns)
if _old is None:
    os.environ.pop("MUTATE")
else:
    os.environ["MUTATE"] = _old
G, H0, Om, Or, rho_crit0, h = (ns[k] for k in ("G", "H0", "Om", "Or", "rho_crit0", "h"))
Mpc, KH, DREF, A0H, nu_mono_h, sigma8_of = ns["Mpc"], ns["KH"], ns["DREF"], ns["A0"], ns["nu_mono"], ns["sigma8_of"]
FB = ns["Ob"] / Om
OL = 1 - Om - Or
Ez = lambda a: math.sqrt(Or / a ** 4 + Om / a ** 3 + OL)
dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / Ez(a) ** 2
yy = np.logspace(-6, 3, 400)
dnu = max(abs(nu_mono_h(y) / float(C4.nu_mono(y)) - 1) for y in yy)
check("C5 CONTROL: the harness's nu_mono (L341) equals FP1's committed nu_mono (CFG4_common) on y = 1e-6..1e3",
      f"max relative difference {dnu:.2e}", dnu < 1e-4)


def harness(mode, foot, z_on=None, z_i=1000.0):
    """mode 'lcdm' | 'chassis' (nu on all matter, the audit's run_rms; harness a0) | 'R3' (baryon-sourced: 1 - f_b + f_b nu(f_b y),
    standing a0, on for z <= z_on).  Returns (dense solution of D in units of D(z_i) = 1, initial amplitude Di)."""
    a_i = 1 / (1 + z_i)
    sL = solve_ivp(lambda N, Y: [Y[1], 1.5 * (Om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
                   (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    Di = DREF / sL.sol(0.0)[0]
    a0 = A0H[foot] if mode == "chassis" else K.A0[foot]

    def grms(a, D):
        rho = Om * rho_crit0 / a ** 3
        gk = 4 * math.pi * G * rho * np.abs(Di * D) / (KH * h / (a * Mpc))
        return math.sqrt(trapz(gk ** 2 / KH, KH) / trapz(1 / KH, KH))

    def rhs(N, Y):
        a = math.exp(N); D, Dp = Y
        boost = 1.0
        if mode == "chassis":
            boost = nu_mono_h(grms(a, D) / a0)
        elif mode == "R3" and (z_on is None or 1 / a - 1 <= z_on):
            boost = 1 - FB + FB * nu_mono_h(FB * grms(a, D) / a0)
        return [Dp, 1.5 * (Om / a ** 3 / Ez(a) ** 2) * boost * D - (2 + dlnH(a)) * Dp]
    if mode == "lcdm":
        return sL, Di, grms
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-8, atol=1e-12, dense_output=True)
    return s, Di, grms


HL, DiL, _ = harness("lcdm", "canonical")
ratio_h = lambda s, z: float(s.sol(math.log(1 / (1 + z)))[0] / HL.sol(math.log(1 / (1 + z)))[0])
fz_h = lambda s, z: float(s.sol(math.log(1 / (1 + z)))[1] / s.sol(math.log(1 / (1 + z)))[0])
CH, R3 = {}, {}
for f in K.FOOTS:
    s, Di, gof = harness("chassis", f)
    s8 = sigma8_of(Di * s.sol(0.0)[0])
    B = np.array([ratio_h(s, z) for z in ZL])
    ls = lens_scores(B ** 2)
    CH[f] = dict(sigma8=s8, B_z=dict(zip([0, 1, 2, 5], [ratio_h(s, z) for z in (0, 1, 2, 5)])), lens=ls,
                 fs8={z: fz_h(s, z) * S8Z(z) * ratio_h(s, z) for z in ZFS}, sol=s)
    P(f"    chassis {f:9s}: sigma_8 {s8:.3f}; growth ratio at z = 0/1/2/5: " + "/".join(f"{v:.2f}" for v in CH[f]["B_z"].values()) +
      f"; lensing amplitude {ls['lin']['amp']:.2f} (linear base, pull {ls['lin']['pull']:+.0f}) / {ls['NL']['amp']:.2f} (halofit)")
check("C2a CONTROL: the harness reproduces the audit's chassis sigma_8 = 23.32 / 27.48 (canonical / alt) to 1%",
      f"{CH['canonical']['sigma8']:.3f} / {CH['alt']['sigma8']:.3f}",
      abs(CH["canonical"]["sigma8"] / 23.32 - 1) < 0.01 and abs(CH["alt"]["sigma8"] / 27.48 - 1) < 0.01)
check("C2b CONTROL: the chassis's CMB-lensing amplitude is > 2 sigma above Planck on the linear base on both footings (the audit / FP22 L22j exclusion)",
      "; ".join(f"{f}: {CH[f]['lens']['lin']['amp']:.1f} ({CH[f]['lens']['lin']['pull']:+.0f} sigma)" for f in K.FOOTS),
      all(CH[f]["lens"]["lin"]["pull"] > 2 for f in K.FOOTS))

# C4: R3's premise
banner("C4  R3's PREMISE: baryons have caught up with the cold component by z = 100 (CLASS transfer functions)")
c2 = Class()
c2.set(dict(BASEPAR, output="mTk", **{"P_k_max_h/Mpc": 2.0, "z_max_pk": 100.0}))
c2.compute()
TK = c2.get_transfer(100.0)
kk = TK["k (h/Mpc)"]
rb = float(np.interp(0.1, kk, TK["d_b"] / TK["d_cdm"]))
P(f"    delta_b / delta_cdm at z = 100, k = 0.1 h/Mpc: {rb:.4f}")
rb_k = {k_: float(np.interp(k_, kk, TK["d_b"] / TK["d_cdm"])) for k_ in (0.02, 0.05, 0.2, 0.5, 1.0)}
P("    (reported, context) the same ratio at k = " + ", ".join(f"{k_:g}: {v:.3f}" for k_, v in rb_k.items()) + " h/Mpc")
check("C4 CONTROL (R3 premise): CLASS delta_b/delta_cdm >= 0.9 at z = 100 for k = 0.1 h/Mpc", f"{rb:.4f}", rb >= 0.9)
R.num("C4", dict(ratio_k01=rb, ratio_other_k=rb_k))
c2.struct_cleanup()

# ================================================================================================ H1 boundness of the web
banner("H1  IS THE LARGE-SCALE WEB 'BOUND' BY B'S DEFINITION?  Press-Schechter turned-around mass fraction f_ta(R, z) with the record's delta_lin,ta(z)")
f_ta = lambda Rh, z: float(erfc(dlin_ta(z) / (math.sqrt(2) * cl.sigma(Rh / hC, z))))
BT = {}
for Rh in (8.0, 20.0, 50.0):
    BT[Rh] = {z: f_ta(Rh, z) for z in (0.0, 1.0, 2.0)}
    P(f"    R = {Rh:4.0f} Mpc/h: sigma(R, 0) = {cl.sigma(Rh / hC, 0.0):.3f}; f_ta at z = 0/1/2 = " + "/".join(f"{v:.2e}" for v in BT[Rh].values()))
check("H1 R1/R2 PREMISE: the large-scale web is unbound by T3 (f_ta(R >= 20 Mpc/h, z = 0) < 0.05): the switch is off on every linear mode",
      f"f_ta(20) = {BT[20.0][0.0]:.2e}, f_ta(50) = {BT[50.0][0.0]:.2e}; at 8 Mpc/h {BT[8.0][0.0]:.3f}", BT[20.0][0.0] < 0.05 and BT[50.0][0.0] < 0.05)
R.num("H1", dict(f_ta=BT))

# ================================================================================================ H2 R1
banner("H2  R1 (B as declared): bound-only switch + identity -> D'' + (2 + dlnH/dN) D' = 1.5 Omega_cb D, exactly LCDM on every linear mode")
if K.MUTATE:
    F_R1 = np.where(ZL <= 10.0, 4.0, 1.0)
    P("    [MUTATE] R1's amplitude x2 for z <= 10 (P x 4)")
else:
    F_R1 = np.ones_like(ZL)
L_R1 = lens_scores(F_R1)
env = abs(score(cpp_X("lin", np.ones_like(ZL)))["amp"] - 1.0)
cpp_lin_full = CPP.copy(); cpp_lin_full[ll8] = CPP[ll8] * np.interp(ll8, LG, LIM0["lin"] / LIM0["NL"])
A_lin_full = score(cpp_lin_full)["amp"]
mfac = 2.0 if K.MUTATE else 1.0
FS8_R1 = {z: mfac * cl.scale_independent_growth_factor_f(z) * S8Z(z) for z in ZFS}
chi_rsd_R1 = sum(((mfac * FS8_L[z] - v) / e) ** 2 for z, v, e in FS8)
P(f"    lensing: linear base {L_R1['lin']['amp']:.4f} (pull {L_R1['lin']['pull']:+.2f}, chi^2 {L_R1['lin']['chi2']:.2f}); halofit base "
  f"{L_R1['NL']['amp']:.4f} (pull {L_R1['NL']['pull']:+.2f}, chi^2 {L_R1['NL']['chi2']:.2f})")
P(f"    in-halo redistribution envelope (reported): a fully linear C_L^pp gives {A_lin_full:.4f}, so |dA| <= {abs(1 - A_lin_full):.4f} "
  f"({abs(1 - A_lin_full) / LA[1]:.2f} sigma)")
P(f"    f sigma_8(z = 0) = {FS8_R1[0.0]:.4f}; RSD chi^2 {chi_rsd_R1:.2f} vs LCDM {chi_rsd_L:.2f} (d {chi_rsd_R1 - chi_rsd_L:+.2f})")


def lens_verdict(ls):
    lin_ok = abs(ls["lin"]["amp"] - LA[0]) <= 2 * LA[1]
    nl_ok = abs(ls["NL"]["amp"] - LA[0]) <= 2 * LA[1]
    return "PASS" if (lin_ok and nl_ok) else ("FAIL" if not lin_ok else "NOT DETERMINED")


V_R1 = lens_verdict(L_R1)
check("H2 R1 CMB LENSING: within 2 sigma of Planck 2018 (8-400) on the linear and halofit bases (pre-declared EXPECT TRUE, P 0.9)",
      f"verdict {V_R1}: linear {L_R1['lin']['amp']:.4f} ({L_R1['lin']['pull']:+.2f}), halofit {L_R1['NL']['amp']:.4f} ({L_R1['NL']['pull']:+.2f}); "
      f"envelope {abs(1 - A_lin_full):.4f}", V_R1 == "PASS")
check("H2b (reported) R1 RSD: Delta chi^2 vs LCDM <= 4 over the 8 typed f sigma_8 points (gate 3.03)",
      f"{chi_rsd_R1 - chi_rsd_L:+.2f}", chi_rsd_R1 - chi_rsd_L <= 4, load_bearing=False)
R.num("R1", dict(lens=L_R1, verdict_lens=V_R1, envelope=abs(1 - A_lin_full), fs8=FS8_R1, rsd_chi2=chi_rsd_R1, rsd_chi2_lcdm=chi_rsd_L))

# ================================================================================================ H3 R2
banner("H3  R2: bound-only + ADDITIVE phantom: D'' + (2 + dlnH/dN) D' = 1.5 Omega_cb [1 + Omega_ph(z)/Omega_m] D; lensing source x [1 + Omega_ph/Omega_m]")
FTA1 = lambda z: float(erfc(dlin_ta(z) / (math.sqrt(2) * cl.sigma(1.0 / hC, z))))
Sfac = lambda z: ((1 + z) ** 3 * opd_ta(z) / opd_ta(0.0)) ** (-1.0 / 3.0)


def omph(f, variant):
    o0, o25 = OMPH[f][0.0], OMPH[f][0.25]
    def fn(z):
        if z <= 0.25:
            return o0 + (o25 - o0) * z / 0.25
        if variant == "min":
            return 0.0
        return o25 * (Sfac(z) / Sfac(0.25)) * (FTA1(z) / FTA1(0.25))
    return fn


R2 = {}
for f in K.FOOTS:
    for var in ("est", "min"):
        om = omph(f, var)
        zt = np.unique(np.concatenate([np.geomspace(1e-3, 50, 400), [0.25, 0.25 + 1e-9]]))
        qt = np.array([om(z) / OM0_T for z in zt])
        q_of = lambda z, zt=zt, qt=qt: float(np.interp(z, zt, qt)) if z >= 1e-3 else float(qt[0])
        sol = growth_class(q_of)
        Bz = np.array([Dfun(sol)(z) / DL(z) for z in ZL])
        qz = np.array([q_of(z) for z in ZL])
        F = Bz ** 2 * (1 + qz) ** 2
        ls = lens_scores(F)
        fs8 = {z: fz(sol, z) * S8Z(z) * Dfun(sol)(z) / DL(z) for z in ZFS}
        rsd = sum(((fz(sol, z) * S8Z(z) * Dfun(sol)(z) / DL(z) - v) / e) ** 2 for z, v, e in FS8)
        R2[(f, var)] = dict(lens=ls, verdict_lens=lens_verdict(ls), fs8=fs8, rsd_chi2=rsd,
                            q={z: q_of(z) for z in (0.0, 0.25, 0.5, 1.0, 2.0, 3.0)}, B={z: Dfun(sol)(z) / DL(z) for z in (0.0, 0.5, 1.0, 2.0)})
        P(f"    {f:9s} R2-{var}: Omega_ph/Omega_m at z = 0/0.25/0.5/1/2 = " + "/".join(f"{R2[(f, var)]['q'][z]:.3f}" for z in (0.0, 0.25, 0.5, 1.0, 2.0)) +
          f"; growth ratio z = 0/1 {R2[(f, var)]['B'][0.0]:.3f}/{R2[(f, var)]['B'][1.0]:.3f}; lensing {ls['lin']['amp']:.3f} (lin, {ls['lin']['pull']:+.1f}) / "
          f"{ls['NL']['amp']:.3f} (NL, {ls['NL']['pull']:+.1f}) -> {R2[(f, var)]['verdict_lens']}; f sigma_8(0) {fs8[0.0]:.3f}; RSD d chi^2 {rsd - chi_rsd_L:+.1f}")
for var in ("est", "min"):
    vs = [R2[(f, var)]["verdict_lens"] for f in K.FOOTS]
    check(f"H3{'a' if var == 'est' else 'b'} (reported) R2-{var} CMB LENSING within 2 sigma on both bases, both footings "
          f"(pre-declared: est EXPECT FALSE P 0.7; min UNCERTAIN)",
          "; ".join(f"{f}: {R2[(f, var)]['lens']['lin']['amp']:.3f}/{R2[(f, var)]['lens']['NL']['amp']:.3f} {R2[(f, var)]['verdict_lens']}" for f in K.FOOTS),
          all(v == "PASS" for v in vs), load_bearing=False)
R.num("R2", {f"{k[0]}|{k[1]}": v for k, v in R2.items()})

# ================================================================================================ H4 R3
banner("H4  R3: the acceleration door: the whole web ON (y_b > y_th), baryon-sourced boost 1 - f_b + f_b nu_mono(y_b), from z = 100")
R3 = {}
for f in K.FOOTS:
    s, Di, gof = harness("R3", f, z_on=100.0)
    yb = {z: FB * gof(1 / (1 + z), s.sol(math.log(1 / (1 + z)))[0]) / K.A0[f] for z in (100.0, 10.0, 2.0, 0.0)}
    nub = {z: nu_mono_h(v) for z, v in yb.items()}
    s8 = sigma8_of(Di * s.sol(0.0)[0])
    B = np.array([ratio_h(s, z) for z in ZL])
    ls = lens_scores(B ** 2)
    fs8 = {z: fz_h(s, z) * S8Z(z) * ratio_h(s, z) for z in ZFS}
    rsd = sum(((fz_h(s, z) * S8Z(z) * ratio_h(s, z) - v) / e) ** 2 for z, v, e in FS8)
    R3[f] = dict(sigma8=s8, y_b=yb, nu_b=nub, lens=ls, verdict_lens=lens_verdict(ls), fs8=fs8, rsd_chi2=rsd,
                 B={z: ratio_h(s, z) for z in (0.0, 1.0, 2.0, 5.0)})
    P(f"    {f:9s}: y_b at z = 100/10/2/0 = " + "/".join(f"{v:.2e}" for v in yb.values()) + " (y_th <= 2.1e-5: ON throughout); nu_mono(y_b) = " +
      "/".join(f"{v:.1f}" for v in nub.values()) + f"; sigma_8 {s8:.2f}; growth ratio z = 0/1/2/5 " + "/".join(f"{v:.2f}" for v in R3[f]["B"].values()) +
      f"; lensing {ls['lin']['amp']:.2f} (lin, {ls['lin']['pull']:+.0f}) / {ls['NL']['amp']:.2f} -> {R3[f]['verdict_lens']}; f sigma_8(0) {fs8[0.0]:.3f}")
check("H4a (reported) R3's switch is ON across the whole linear web (y_b > 2.1e-5 at every z <= 100, both footings)",
      "; ".join(f"{f}: min y_b {min(R3[f]['y_b'].values()):.2e}" for f in K.FOOTS), all(min(R3[f]["y_b"].values()) > 2.1e-5 for f in K.FOOTS),
      load_bearing=False)
check("H4b (reported) R3 CMB LENSING within 2 sigma on both bases, both footings (pre-declared EXPECT FALSE, P 0.9)",
      "; ".join(f"{f}: {R3[f]['lens']['lin']['amp']:.2f} {R3[f]['verdict_lens']}" for f in K.FOOTS),
      all(R3[f]["verdict_lens"] == "PASS" for f in K.FOOTS), load_bearing=False)
R.num("R3", R3)
R.num("chassis", {f: {k: v for k, v in CH[f].items() if k != "sol"} for f in K.FOOTS})
R.num("fs8_grid_z", list(ZFS))

# ================================================================================================ summary
banner("SUMMARY: lensing per reading (the weaker footing decides; velocities in cfg324_velocities.py)")
worst = lambda vs: "FAIL" if "FAIL" in vs else ("NOT DETERMINED" if "NOT DETERMINED" in vs else "PASS")
LV = {"R1": V_R1,
      "R2-est": worst([R2[(f, "est")]["verdict_lens"] for f in K.FOOTS]),
      "R2-min": worst([R2[(f, "min")]["verdict_lens"] for f in K.FOOTS]),
      "R3": worst([R3[f]["verdict_lens"] for f in K.FOOTS])}
LV["R2"] = LV["R2-est"] if LV["R2-est"] == LV["R2-min"] else "NOT DETERMINED"
for k, v in LV.items():
    P(f"    {k:7s}: lensing {v}")
R.num("lens_verdicts", LV)
sys.exit(R.finish())
