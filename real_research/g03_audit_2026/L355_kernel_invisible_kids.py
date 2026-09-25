#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L355 -- KiDS-1000 FOR THE KERNEL-INVISIBLE CONSTRUCTION (L353): with the kernel reading baryons only, how much
Newtonian dark mass must sit around isolated galaxies at 0.3-3 Mpc, and can the Lambda-triggered carrier supply it?

WHY.  L353 makes the MOND kernel read the baryonic Newtonian field only.  The web's baryons still pull on every lens, so
the phantom is truncated by the external-field effect at e_b ~ (Omega_b/Omega_m) x the web's field: BS2's E10 (baryons-
only kernel) passes inside 0.3 Mpc and fails the full KiDS-1000 profile by ~+250 without any extra mass.  In the
construction the missing lensing can only come from real, unboosted mass -- the carrier's surviving halo and correlated
structure (2-halo).  This lane asks how much, and whether L319's carrier provides it.

MACHINERY (copied with attribution, not imported, so nothing of the parallel lanes is edited):
  * BS2's exact stacked-lens QUMOND law M_dyn = M_b N(y, e), N = <nu(w)(y - e mu)>_mu / y, with the lens population's
    field magnitudes Maxwell-distributed (real_research/switch_audit_2026/BS2_efe_vs_switch.py);
  * the ESD projection and the four stellar-mass bins of Brouwer+2021 with full covariance, M_b profiled per bin
    (L342/BS2); the linear 2-halo shape with a free amplitude per bin (L352);
  * the carrier's surviving halo: (1 - f_b) x NFW(M200) x S(z_l), M200 from the Moster+2013 stellar-to-halo relation at
    each bin's typical stellar mass, S(z_l = 0.25) from L319's decay law (Gamma ~ Omega_Lambda^2) for L354's f_d(0).
    The carrier is kernel-invisible (L353), so its halo lenses at its Newtonian mass.
  Two web fields: the linear-theory baryonic rms (BS2 E8 x Omega_b/Omega_m, Maxwell-stacked) and Brouwer+21's adopted
  isolated-lens field e = 0.003 scaled to baryons (x Omega_b/Omega_m).  No switch (the most favourable case for the
  phantom: a switch would also cancel its excess beyond the switch edge, L352).

CHECKS
  K1 CONTROL: with no external field the model reproduces the isolated-MOND base fit (the reference).
  K2 THE DEFICIT: the baryons-only kernel without extra mass, at both fields (BS2's E10, re-derived).
  K3 WITH THE CARRIER: + the carrier's surviving halo (L319's S(z_l) at f_d(0) = 0.8, 0.9) + a bias-like 2-halo (A <= 2).
  K4 WHAT KiDS WANTS: the carrier fraction f_s (free, >= 0) that minimises chi^2, and chi^2 there.
  PRE-DECLARED CRITERION (fixed before the run): the construction passes KiDS if, at its OWN field (linear theory), the
  carrier's surviving halo plus a bias-like 2-halo (A <= 2) brings Delta chi^2 within +9 of isolated MOND on both footings.
  MUTATE=1 makes the kernel blind to the web (no external field in its argument): K2's deficit must vanish (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L355_kernel_invisible_kids.py
"""
import os, sys, json, math, time, warnings, io, contextlib
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious macOS-Accelerate BLAS flags (as L342/BS2); results finite
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L355_kernel_invisible_kids"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L355", "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
_trap = getattr(np, "trapezoid", None) or np.trapz


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the kernel is blind to the web (no external field); K2 must FAIL ***")

# ---------------------------------------------------------------------------------- constants and kernel (as BS2/L342)
c = 2.99792458e8; Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200
H0 = 100 * h * 1e3 / Mpc; rho_crit0 = 3 * H0**2 / (8 * math.pi * G)
Ob, Oc = om_b / h**2, om_c / h**2; Om = Ob + Oc; OL = 1 - Om
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FB = Ob / Om


def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10**LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def nu_mono_arr(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM) / y


# ---------------------------------------------------------------------------------- KiDS data and projection (BS2, verbatim logic)
B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
MS, PCm = 1.98892e30, 3.0857e16; MPCm = PCm * 1e6
Rd, Ed, Sd = [], [], []
for b in (1, 2, 3, 4):
    d = np.genfromtxt(os.path.join(B, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#")
    Rd.append(d[:, 0]); Ed.append(d[:, 1] / d[:, 4]); Sd.append(d[:, 3] / d[:, 4])
cv = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
vv = cv[:, 4] / cv[:, 6]; npb = len(Rd[0]); Cf = vv.reshape(4, 4, npb, npb).transpose(0, 2, 1, 3).reshape(4 * npb, 4 * npb)
Cf = (Cf + Cf.T) / 2; Ci = np.linalg.inv(Cf)
rr = np.geomspace(1e-3, 30, 4000) * MPCm; Rp = np.geomspace(0.02, 4, 240) * MPCm
W = np.zeros((len(Rp), len(rr)))
for i, Rv in enumerate(Rp):
    m = np.where(rr > Rv * 1.0000001)[0]; r_ = rr[m]; dr = np.diff(r_)
    wt = np.zeros_like(r_); wt[:-1] += 0.5 * dr; wt[1:] += 0.5 * dr
    W[i, m] = 2 * r_ / np.sqrt(r_**2 - Rv**2) * wt


def esd_of_M(M, Mb):
    """ESD [Msun/pc^2] of an enclosed-mass profile M(r) [kg] with a point-mass Mb (BS2's esd_from_M, no switch)."""
    rho = np.gradient(M - Mb, rr) / (4 * math.pi * rr**2)
    Sig = W @ rho
    Mc = np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * Rp[1:] + Sig[:-1] * Rp[:-1]) * np.diff(Rp))]) * 2 * math.pi \
        + math.pi * Rp[0]**2 * Sig[0]
    return (Mc / (math.pi * Rp**2) - Sig + Mb / (math.pi * Rp**2)) * PCm**2 / MS


LYT = np.linspace(-9.5, 6.5, 1601); YT = 10**LYT; MU = np.linspace(-1.0, 1.0, 4001)


def N_of(y, e):
    """BS2's exact stacked-lens law: < nu(w) (y - e mu) >_mu / y."""
    y = np.atleast_1d(np.asarray(y, float))
    if e == 0: return nu_mono_arr(y)
    out = np.empty_like(y)
    for s in range(0, len(y), 64):
        yy = y[s:s + 64, None]
        w = np.sqrt(np.maximum(yy**2 + e**2 - 2 * yy * e * MU[None, :], 0.0))
        out[s:s + 64] = 0.5 * _trap(nu_mono_arr(w) * (yy - e * MU[None, :]), MU, axis=1) / yy[:, 0]
    return out


ES = [0.0] + [float(v) for v in np.geomspace(1e-5, 0.1, 25)]
NTAB = {e: N_of(YT, e) for e in ES}
LM = np.round(np.arange(9.8, 11.8001, 0.05), 3)
rs_ = np.random.default_rng(7); GAUSS = rs_.standard_normal((200000, 3))
LOGE = np.log10(np.array(ES[1:]))


def stack_weights(e_samples):                                         # BS2's binning of |g_ext|/a0 samples onto ES
    w = np.zeros(len(ES)); le = np.log10(np.maximum(e_samples, 1e-12))
    below = le < LOGE[0] - 0.5 * (LOGE[1] - LOGE[0]); w[0] += below.sum()
    idx = np.clip(np.rint((le[~below] - LOGE[0]) / (LOGE[1] - LOGE[0])).astype(int), 0, len(LOGE) - 1) + 1
    np.add.at(w, idx, 1.0); return w / w.sum()


def maxwell_e(sig3d): return np.linalg.norm(GAUSS, axis=1) * sig3d / math.sqrt(3)


# phantom tables per footing: ESD of M_b N(y, e) for every (e, M_b), interpolated at the data radii
TAB = {}
for foot in A0:
    T = np.zeros((len(ES), len(LM), 4, npb))
    for ie, e in enumerate(ES):
        for im, lm in enumerate(LM):
            Mb = 10**lm * MS; y = G * Mb / rr**2 / A0[foot]
            M = Mb * (nu_mono_arr(y) if e == 0 else np.interp(np.log10(y), LYT, NTAB[e]))
            dS = esd_of_M(M, Mb)
            T[ie, im] = [np.interp(Rd[b], Rp / MPCm, dS) for b in range(4)]
    TAB[foot] = T
P(f"  phantom tables built: {len(ES)} external fields x {len(LM)} masses x 2 footings ({time.time() - T0:.0f} s)")

# ---------------------------------------------------------------------------------- the web's field (BS2 E8's integral)
def T_eh(k):
    th = 2.7255 / 2.7; omh2 = Om * h * h; fb = Ob / Om
    s_ = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * (Ob * h * h) ** 0.75)
    aG = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb**2
    Gm = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s_) ** 4)); q = k * th**2 / (Gm * h)
    L_ = np.log(2 * np.e + 1.8 * q); C_ = 14.2 + 731 / (1 + 62.5 * q); return L_ / (L_ + C_ * q * q)
def W_th(x): return 3 * (np.sin(x) - x * np.cos(x)) / x**3
kk = np.geomspace(1e-5, 50, 20000); Pk = kk**0.9649 * T_eh(kk)**2
Pk *= 0.8111**2 / _trap(Pk * W_th(kk * 8 / h)**2 * kk**2 / (2 * math.pi**2), kk)
def Dgr(a1):
    aa = np.linspace(1e-4, a1, 20001); E = np.sqrt(Om / aa**3 + OL); return math.sqrt(Om / a1**3 + OL) * _trap(1 / (aa * E)**3, aa)
ZL = 0.25; DZ = Dgr(1 / (1 + ZL)) / Dgr(1.0)
I16 = _trap(Pk * W_th(kk * 16.0)**2, kk) / (2 * math.pi**2)
sig_all = 1.5 * Om * H0**2 * (1 + ZL)**2 * DZ * math.sqrt(I16) * Mpc          # m/s^2, 3D rms, 16 Mpc (BS2 E8)
FIELDS = {"linear-theory (16 Mpc)": sig_all, "Brouwer+21 quiet (e = 0.003 a0)": 0.003 * A0["canonical"] * math.sqrt(3)}
P("  web field (3D rms): " + "; ".join(f"{k_}: {v_ / A0['canonical']:.4f} a0 all-matter" for k_, v_ in FIELDS.items()))

# ---------------------------------------------------------------------------------- the 2-halo shape (L352)
rho_m_z = Om * rho_crit0 * (1 + ZL)**3 * (Mpc**3 / MS)
kkM = np.geomspace(1e-4, 50, 6000); PkM = np.interp(kkM, kk, Pk) * DZ**2
def xi_lin(rM): return _trap(kkM**2 * PkM * np.sinc(kkM * rM / math.pi) * np.exp(-(kkM * 0.05)**2), kkM) / (2 * math.pi**2)
rgrid = np.geomspace(0.005, 200, 1200); xig = np.array([xi_lin(r0) for r0 in rgrid])
def w_proj(Rm):
    chi = np.geomspace(1e-4, 150, 3000); r2 = np.sqrt(Rm**2 + chi**2)
    return 2 * _trap(np.interp(np.log(r2), np.log(rgrid), xig), chi)
Rp_M = Rp / MPCm; Sig2h = rho_m_z * np.array([w_proj(R0) for R0 in Rp_M]) / 1e12
M2h = np.concatenate([[0], np.cumsum(0.5 * (Sig2h[1:] * Rp_M[1:] + Sig2h[:-1] * Rp_M[:-1]) * np.diff(Rp_M))]) * 2 * math.pi * 1e12 \
    + math.pi * Rp_M[0]**2 * Sig2h[0] * 1e12
ESD2h = M2h / (math.pi * (Rp_M * 1e6)**2) - Sig2h
T2H = [np.interp(Rd[b], Rp_M, ESD2h) for b in range(4)]

# ---------------------------------------------------------------------------------- the carrier's surviving halo
LOGMS = [10.0, 10.45, 10.70, 10.90]                                  # typical log M* of the four bins (h70^-2 Msun)
def moster13_Mstar(M200):                                           # Moster, Naab & White 2013, z ~ 0.25
    z = ZL; M1 = 10**(11.590 + 1.195 * z / (1 + z)); N = 0.0351 - 0.0247 * z / (1 + z)
    be = 1.376 - 0.826 * z / (1 + z); ga = 0.608 + 0.329 * z / (1 + z)
    return 2 * N * M200 / ((M200 / M1)**(-be) + (M200 / M1)**ga)
M200s = [10**brentq(lambda lm: math.log10(moster13_Mstar(10**lm)) - ls, 10.5, 15.5) for ls in LOGMS]
def c200(M200): return 10**(0.905 - 0.101 * math.log10(M200 / (1e12 / h)))
rho_c_z = rho_crit0 * (Om * (1 + ZL)**3 + OL) * (Mpc**3 / MS)        # Msun/Mpc^3
def nfw_M(M200, r_mpc):
    cc = c200(M200); r200 = (3 * M200 / (4 * math.pi * 200 * rho_c_z))**(1 / 3); rs = r200 / cc
    mm = lambda s: np.log(1 + s) - s / (1 + s)
    return M200 * mm(np.minimum(r_mpc, r200) / rs) / mm(cc), r200
TCAR = []
for b in range(4):
    Mn, r200 = nfw_M(M200s[b], rr / MPCm)
    Mc = (1 - FB) * Mn * MS
    dS = esd_of_M(Mc + 1.0, 1.0)                                     # the carrier halo alone (unboosted, kernel-invisible)
    TCAR.append(np.interp(Rd[b], Rp / MPCm, dS))
P("  bins: log M* " + ", ".join(f"{l:.2f}" for l in LOGMS) + " -> Moster+13 M200 " + ", ".join(f"{m:.2e}" for m in M200s))
# L319's survival at the lens redshift for L354's f_d(0) values
_s19 = open(os.path.join(REPO, "real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay.py")).read().split(
    "# ============================================================================================ controls")[0]
G19 = {"__name__": "l319", "__file__": os.path.join(REPO, "real_research", "dark_sector_2026", "L319_lambda_triggered_kicked_decay.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s19, G19)
SURV = {}
for fd0 in (0.8, 0.9):
    with contextlib.redirect_stdout(io.StringIO()):
        sv, _ = G19["surv_triggered"](fd0, 2)
    SURV[fd0] = float(np.interp(1 / (1 + ZL), G19["a_grid"], sv))
P("  carrier surviving fraction at z_l = 0.25 (L319, Gamma ~ Omega_Lambda^2): " + ", ".join(f"f_d(0) = {k_}: S = {v_:.3f}" for k_, v_ in SURV.items()))


def fit(foot, wts, fs, allow_2h, fs_free=False):
    """chi^2 with M_b per bin profiled (grid), carrier amplitude fs (fixed, or free >= 0 per the stack), 2-halo A in [0, 2]."""
    blk = np.tensordot(wts, TAB[foot], axes=(0, 0))                  # stacked phantom ESD [im, bin, radius]
    D = np.concatenate(Ed); chosen = []; tot = 0.0
    best_fs = fs
    fs_grid = np.linspace(0, 1.2, 25) if fs_free else [fs]
    best_all = None
    for fsv in fs_grid:
        mods = []; pars = []
        for b in range(4):
            bb = None
            for im in range(len(LM)):
                mk = blk[im, b] + fsv * TCAR[b]
                A = 0.0
                if allow_2h:
                    t2 = T2H[b]; wv = 1 / Sd[b]**2
                    A = float(np.clip(np.sum(wv * t2 * (Ed[b] - mk)) / np.sum(wv * t2 * t2), 0.0, 2.0)); mk = mk + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b])**2))
                if bb is None or c_ < bb[0]: bb = (c_, mk, LM[im], A)
            mods.append(bb[1]); pars.append((bb[2], bb[3]))
        dv = D - np.concatenate(mods); c2 = float(dv @ Ci @ dv)
        if best_all is None or c2 < best_all[0]: best_all = (c2, fsv, pars)
    return best_all


# ============================================================================================ K1 control
banner("K1  CONTROL: no external field reproduces the isolated-MOND base fit")
w0 = np.zeros(len(ES)); w0[0] = 1.0
REF = {}
for foot in A0:
    REF[foot] = fit(foot, w0, 0.0, False)[0]
P("    isolated MOND (no EFE, no carrier, no 2-halo): chi^2 = " + ", ".join(f"{f_} {v_:.1f}" for f_, v_ in REF.items()))
OUT["numbers"]["K1"] = REF
check("K1 (control) the isolated-MOND base fit is the record's (L342/BS2 base chi^2 ~ 106-116 on 60 points)",
      REF, all(90 < v_ < 130 for v_ in REF.values()), load_bearing=False)

# ============================================================================================ K2 the deficit
banner("K2  THE DEFICIT: baryons-only kernel (EFE from the web's baryons), no extra mass")
KFAC = 0.0 if MUTATE else Ob / Om                                     # kernel's field: baryons only (MUTATE: blind to the web)
K2 = {}
for foot in A0:
    for lab, s3 in FIELDS.items():
        wts = stack_weights(maxwell_e(s3 * KFAC / A0[foot]))
        c_ = fit(foot, wts, 0.0, False)[0]
        K2[(foot, lab)] = c_ - REF[foot]
        P(f"    {foot:9s} {lab:32s}: kernel field rms {s3 * KFAC / A0[foot]:.5f} a0 -> Delta chi^2 {c_ - REF[foot]:+.1f}")
OUT["numbers"]["K2"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in K2.items()}
check("K2 a kernel that reads baryons only does NOT remove the external-field deficit: Delta chi^2 >= +100 at the "
      "construction's own (linear-theory) field and >= +50 at Brouwer+21's quiet field, both footings (BS2's E10 re-derived)",
      {f"{k_[0]}/{k_[1][:12]}": round(v_, 1) for k_, v_ in K2.items()},
      all(K2[(f_, "linear-theory (16 Mpc)")] >= 100 for f_ in A0) and all(K2[(f_, "Brouwer+21 quiet (e = 0.003 a0)")] >= 50 for f_ in A0),
      "dividing the web's field by Omega_m/Omega_b ~ 6 leaves it 10-30x above KiDS's bound e <~ 7e-5 (BS2 E7)")

# ============================================================================================ K3 with the carrier
banner("K3  WITH THE CARRIER'S SURVIVING HALO (L319, f_d(0) = 0.8 / 0.9) + a bias-like 2-halo (A <= 2)")
K3 = {}
for foot in A0:
    for lab, s3 in FIELDS.items():
        wts = stack_weights(maxwell_e(s3 * KFAC / A0[foot]))
        for fd0, S in SURV.items():
            c_, fsv, pars = fit(foot, wts, S, True)
            K3[(foot, lab, fd0)] = (c_ - REF[foot], pars)
            P(f"    {foot:9s} {lab:32s} f_d(0) {fd0}: carrier S = {S:.3f} -> Delta chi^2 {c_ - REF[foot]:+.1f}; "
              f"2-halo A per bin {[round(p_[1], 2) for p_ in pars]}")
OUT["numbers"]["K3"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in K3.items()}

# ============================================================================================ K4 what KiDS wants
banner("K4  WHAT KiDS WANTS: the carrier fraction f_s (free) with a bias-like 2-halo")
K4 = {}
for foot in A0:
    for lab, s3 in FIELDS.items():
        wts = stack_weights(maxwell_e(s3 * KFAC / A0[foot]))
        c_, fsv, pars = fit(foot, wts, 0.0, True, fs_free=True)
        K4[(foot, lab)] = (c_ - REF[foot], fsv)
        P(f"    {foot:9s} {lab:32s}: best f_s = {fsv:.2f} of the LCDM halo -> Delta chi^2 {c_ - REF[foot]:+.1f}")
OUT["numbers"]["K4"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in K4.items()}

# ============================================================================================ the pre-declared reading
banner("THE READING (criterion fixed before the run: Delta chi^2 <= +9 vs isolated MOND, at the construction's own field)")
own = "linear-theory (16 Mpc)"
k3_own = {(f_, fd0): K3[(f_, own, fd0)][0] for f_ in A0 for fd0 in SURV}
k3_pass = {fd0: all(k3_own[(f_, fd0)] <= 9.0 for f_ in A0) for fd0 in SURV}
k4_own = {f_: K4[(f_, own)] for f_ in A0}
P("    own field: " + "; ".join(f"f_d(0) {fd0}: " + ", ".join(f"{f_} {k3_own[(f_, fd0)]:+.1f}" for f_ in A0) for fd0 in SURV))
P("    what KiDS wants at the own field: " + ", ".join(f"{f_} f_s = {v_[1]:.2f} (Delta {v_[0]:+.1f})" for f_, v_ in k4_own.items()))
OUT["numbers"]["reading"] = {"k3_own": {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in k3_own.items()}, "k3_pass": k3_pass,
                             "k4_own": {f_: v_ for f_, v_ in k4_own.items()}}
RESULT_PASS = any(k3_pass.values())
check("K3 against the pre-declared criterion the construction plus the carrier's surviving halo and a bias-like 2-halo FAILS "
      "KiDS-1000 at its own field (Delta chi^2 > +9 for every f_d(0), both footings)",
      "; ".join(f"f_d(0) {fd0}: " + ", ".join(f"{f_} {k3_own[(f_, fd0)]:+.1f}" for f_ in A0) for fd0 in SURV),
      not RESULT_PASS, "the carrier cannot replace the phantom's EFE-truncated tail")
k4_min = min(v_[0] for v_ in K4.values()); fs_max = max(v_[1] for v_ in K4.values())
check("K4 (reported) KiDS wants essentially no NFW-shaped carrier (best f_s <= 0.1 of the LCDM halo) and still misses: the "
      "deficit is the missing isothermal phantom beyond the EFE radius, which no halo shape supplies",
      {f"{k_[0]}/{k_[1][:12]}": (round(v_[1], 2), round(v_[0], 1)) for k_, v_ in K4.items()}, fs_max <= 0.1,
      "KiDS needs the kernel blind to the large-scale field at the ~1e-4 a0 level (BS2's door ii), not only blind to dark matter",
      load_bearing=False)

banner("VERDICT")
P(f"""  Making the kernel read baryons only divides the web's pull in its argument by ~6, not by the ~100-200 KiDS needs.  At
  the construction's own field the external-field deficit is {min(K2[(f_, own)] for f_ in A0):+.0f}..{max(K2[(f_, own)] for f_ in A0):+.0f} (K2); the carrier's surviving
  halo plus a bias-like 2-halo leaves {min(k3_own.values()):+.0f}..{max(k3_own.values()):+.0f} against the pre-declared +9 (K3); and KiDS wants almost none
  of an NFW-shaped carrier (K4): what is missing is the isothermal phantom beyond the EFE radius.  The construction fixes
  reciprocity and the boost; KiDS requires more -- a kernel blind to the large-scale field altogether (sourced by the
  bound region's own matter), which the Solar-System floor must still see (the Galaxy's field is inside the bound region).
  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
