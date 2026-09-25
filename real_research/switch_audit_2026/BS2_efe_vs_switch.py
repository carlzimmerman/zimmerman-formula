#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BS2 -- IS L342's KiDS PREFERENCE FOR THE SWITCH EVIDENCE FOR THE SWITCH, OR FOR THE EXTERNAL-FIELD EFFECT?
(Support audit of the lead track's bound-region switch; L342's file is not edited -- its lensing model is reused.)

THE CLAIM (real_research/g03_audit_2026/L342_bound_region_switch.py, B4)
  KiDS-1000's isolated-lens ESD profiles (Brouwer+2021 Fig. 3, four stellar-mass bins) prefer a switch that ends every
  galaxy's phantom at r_t = v_flat/(sqrt(x_c) H), x_c ~ 4-7, over no switch (Delta chi^2 ~ -15..-19).  L342 lists its
  own caveat: "no 2-halo or external-field term".

WHY THE EXTERNAL FIELD IS THE FIRST THING TO ADD
  The lensing model is QUMOND-form (phantom = nu(g_N/a0) g_N).  Every QUMOND galaxy sits in the Newtonian field of the
  large-scale structure, g_e = e a0, and that field ALSO ends the phantom's growth: beyond r_e ~ v^2/(e a0) the galaxy
  is quasi-Newtonian with a boosted G.  So the data's fall-off below the isolated-MOND profile at R ~ 1-3 Mpc is
  predicted by the framework's own EFE, with no new ingredient.  If the EFE absorbs the preference, L342's KiDS result
  is not evidence for the switch.  The two differ in ONE place: how the truncation radius scales with mass --
  r_t ~ v_flat ~ M_b^(1/4) (switch) versus r_e ~ v_flat^2 ~ M_b^(1/2) (EFE) -- so four mass bins can tell them apart
  if the data have the power.

THE EXACT STACKED-LENS EFE (no approximation inside the QUMOND form)
  QUMOND: div(grad Phi - nu(|g_N|/a0) g_N) = 0 everywhere, so the flux of g through ANY sphere equals the flux of
  nu g_N (the curl field carries none).  A stack of lenses with randomly oriented external fields has, on average, the
  sphere-averaged density, whose enclosed mass is therefore exactly
      M_dyn(<r) = M_b N(y, e),   N(y, e) = < nu(w) (y - e mu) >_mu / y,   w = sqrt(y^2 + e^2 - 2 y e mu),
  y = G M_b/(r^2 a0), mu uniform on [-1, 1].  N(y, 0) = nu(y) (isolated); N(y -> 0, e) = nu(e)(1 + L_e/3),
  L_e = dln nu/dln y at e (a finite, boosted Newtonian mass).

CHECKS (gates set before the run)
  E1 machinery: the vectorised projection reproduces L342's loop; the e = 0 model reproduces L342's no-switch chi^2.
  E2 the EFE law's limits: N(y, 0) = nu(y); N(y << e) -> nu(e)(1 + L_e/3); N(y >> e) -> nu(y).
  E3 THE QUESTION: with the external field in (shared e, profiled), does the switch still improve chi^2 by >= 4 on both
     footings?  (a) e free on the grid 0..0.1; (b) e restricted to the physical range for isolated field lenses,
     0.002-0.02 (linear-theory LSS field g = 3 H Omega_m v/(2f) ~ 0.005-0.01 a0 for v ~ 300-500 km/s; isolation
     lowers it, near neighbours raise it).
  E4 (documentary) the EFE-only fit: its best e and whether it is physical.
  E5 which mass scaling do the data prefer: chi^2(EFE only, shared e) vs chi^2(switch only, shared x_c).
  E6 POWER: synthetic data from each family (switch only, x_c = 5; EFE only at E4's best e) -- does the fit recover
     the true family (Delta chi^2 >= 2 in >= 70% of 20 draws each)?
  E7 THE KiDS BOUND on a single external field e (Delta chi^2 = 4 above the best, M_b and x_c profiled).
  E8 THE CONSTRUCTION'S OWN EXTERNAL FIELD.  L342's switch keeps MOND off on the linear web, which then grows as in
     LCDM with the CMB's cold fluid (sigma_8 = 0.81).  Its Newtonian field is LCDM's: sigma_g,3D = (3/2) Omega_m H0^2
     (1+z)^2 D(z) [Int P dk/2 pi^2]^(1/2), Eisenstein-Hu no-wiggle P(k), top-hat smoothed at the isolation scale
     (4 Mpc) and, conservatively, 16 Mpc; sanity: the same integral gives sigma_v,1D ~ 300 km/s.  C-H/K's kernel sees
     free-fall external fields -- L340 S1's Solar-System quadrupole floor IS the Galaxy's EFE on the freely falling Sun.
  E9 THE GATE: C-H/K + switch with that field (Maxwell-distributed |g_ext| stacked over lenses, 16 Mpc smoothing, the
     favourable choice) fits KiDS within Delta chi^2 <= 4 of the no-EFE switch fit, both footings.
  E10 (documentary) a kernel sourced by baryons only (field x Omega_b/Omega_m).
  E11 (documentary control) pure MOND, where the large-scale field is itself MOND-level: e_N = (g_ext/a0)^2.
  E12 (documentary) the KiDS bound on the rms external field of the stacked model, against E8.
  E13 THE SAME GATE INSIDE R <= 0.3 Mpc, where Brouwer+21 treat isolation as certain (R < 0.3 h70^-1 Mpc) and a
     two-halo term cannot contribute: the construction with its own field vs the no-EFE switch fit on those points.
  E14 (documentary) the field's magnitude: the construction at the ACTUAL external field Brouwer+21 adopt for isolated
     lenses (e = g_ext/g_dagger = 0.003, from Chae+20's isolated SPARC galaxies; 4x below E8's LCDM estimate).  In the
     construction that field is Newtonian (e_N = 0.003); in pure MOND it is MOND-level (e_N ~ e^2).
  PRIOR ART.  Brouwer+21 (A&A 650 A113, Sec. 5.2) show that a MOND EFE at e = 0.003 moves the prediction away from their
  isolated-lens RAR; Mistele+24 (ApJL 969 L3) find lensing circular velocities flat to ~1 Mpc.  New here: the exact
  stacked-lens flux law, the KiDS bound on the Newtonian external field, and the switch construction's own field.
  (Record: the first run used a coarse e grid, 0.001-0.1, and the pre-set physical range 0.002-0.02; every e >= 0.001
   worsened chi^2 by ~+260, which is what prompted E7-E12.  E3a/E3b are kept exactly as pre-set.)
  MUTATE=1 replaces the data with an EFE-only synthetic set (e = 1e-4, no switch): E3a must then FAIL (rc = 1).
  SCOPE: L342's base model otherwise (point-mass baryons, lens z = 0.25, no 2-halo term).

Run from the repository root:  python3 real_research/switch_audit_2026/BS2_efe_vs_switch.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious BLAS warning (no result changes)
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "BS2_efe_vs_switch"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "BS2", "mutate": MUTATE, "checks": {}, "numbers": {}}
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


# ------------------------------------------------------------------ L342's constants, kernel and data (as in BS1)
Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200
H0 = 100 * h * 1e3 / Mpc
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def nu_mono_arr(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM) / y

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
Hlens = H0 * math.sqrt(Om * 1.25 ** 3 + OL)

# vectorised form of L342's projection loop: Sig = W @ rho with the masked trapezoid weights
W = np.zeros((len(Rp), len(rr)))
for i, Rv in enumerate(Rp):
    m = np.where(rr > Rv * 1.0000001)[0]; r_ = rr[m]; dr = np.diff(r_)
    wt = np.zeros_like(r_); wt[:-1] += 0.5 * dr; wt[1:] += 0.5 * dr
    W[i, m] = 2 * r_ / np.sqrt(r_ ** 2 - Rv ** 2) * wt


def esd_from_M(M, Mb, xc, loop=False):
    if xc:
        rho_dyn = np.gradient(M, rr) / (4 * math.pi * rr ** 2); on = 4 * math.pi * G * rho_dyn / Hlens ** 2 >= xc
        it = int(np.where(on)[0].max()) if on.any() else 0
        M = np.where(np.arange(len(rr)) > it, M[it], M)
    rho = np.gradient(M - Mb, rr) / (4 * math.pi * rr ** 2)
    if loop:                                                      # L342's loop, verbatim
        Sig = np.zeros_like(Rp)
        for i, Rv in enumerate(Rp):
            m = rr > Rv * 1.0000001; r_ = rr[m]; Sig[i] = 2 * _trap(rho[m] * r_ / np.sqrt(r_ ** 2 - Rv ** 2), r_)
    else:
        Sig = W @ rho
    Mc = np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * Rp[1:] + Sig[:-1] * Rp[:-1]) * np.diff(Rp))]) * 2 * math.pi \
        + math.pi * Rp[0] ** 2 * Sig[0]
    return Rp / MPCm, (Mc / (math.pi * Rp ** 2) - Sig + Mb / (math.pi * Rp ** 2)) * PCm ** 2 / MS


# ------------------------------------------------------------------ the exact stacked-lens EFE law N(y, e)
LYT = np.linspace(-9.5, 6.5, 1601); YT = 10 ** LYT
MU = np.linspace(-1.0, 1.0, 4001)


def N_of(y, e):
    """< nu(w) (y - e mu) >_mu / y for arrays y (exact angular average, trapezoid on 4001 nodes)."""
    y = np.atleast_1d(np.asarray(y, float))
    if e == 0: return nu_mono_arr(y)
    out = np.empty_like(y)
    for s in range(0, len(y), 64):
        yy = y[s:s + 64, None]
        w = np.sqrt(np.maximum(yy ** 2 + e ** 2 - 2 * yy * e * MU[None, :], 0.0))
        f = nu_mono_arr(w) * (yy - e * MU[None, :])
        out[s:s + 64] = 0.5 * _trap(f, MU, axis=1) / yy[:, 0]
    return out


ES = [0.0] + [float(v) for v in np.round(np.geomspace(1e-6, 0.1, 36), 9)]
XCS = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.5, 10.0, 15.0, 20.0]
LM = np.round(np.arange(9.8, 11.8001, 0.02), 4)
NTAB = {e: N_of(YT, e) for e in ES}
P(f"EFE tables built for {len(ES)} external fields ({time.time() - T0:.0f} s)")


def model_M(Mb, a0, e):
    y = G * Mb / rr ** 2 / a0
    if e == 0: return Mb * nu_mono_arr(y)                         # identical to L342's isolated model
    return Mb * np.interp(np.log10(y), LYT, NTAB[e])


FOOTS = ("canonical", "alt")
TABA = np.zeros((2, len(ES), len(XCS), len(LM), 4, npb))
for jf, foot in enumerate(FOOTS):
    for ie, e in enumerate(ES):
        for im, lm in enumerate(LM):
            Mb = 10 ** lm * MS; M = model_M(Mb, A0[foot], e)
            for ix, xc in enumerate(XCS):
                Rq, dS = esd_from_M(M, Mb, xc)
                TABA[jf, ie, ix, im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
class _Tab(dict):
    def __getitem__(self, k): return TABA[FOOTS.index(k[0]), k[1], k[2], k[3]]
TAB = _Tab()
P(f"model table: {TABA.shape[0] * TABA.shape[1] * TABA.shape[2] * TABA.shape[3]} ESD profiles ({time.time() - T0:.0f} s)")


def chi2_full(models, data):
    dv = np.concatenate(data) - np.concatenate(models); return float(dv @ Ci @ dv)


def profile_block(blk, data, sel=None):
    """chi^2 of a model block blk[im, bin, radius], M_b per bin profiled by coordinate descent (full covariance);
    sel: optional index subset of the 4*npb data vector (its own sub-covariance is inverted)."""
    im = [len(LM) // 2] * 4; D = np.concatenate(data); best = None
    Cinv = Ci if sel is None else np.linalg.inv(Cf[np.ix_(sel, sel)])
    for _ in range(10):
        moved = False
        for b in range(4):
            base = np.concatenate([blk[im[bb], bb] for bb in range(4)])
            V = np.repeat(base[None, :], len(LM), axis=0); V[:, b * npb:(b + 1) * npb] = blk[:, b]
            dv = D[None, :] - V
            if sel is not None: dv = dv[:, sel]
            cs = np.einsum("ij,jk,ik->i", dv, Cinv, dv)
            j = int(np.argmin(cs))
            if j != im[b]: im[b], moved = j, True
            best = float(cs[j])
        if not moved: break
    return best, im


def profile_mass(foot, ie, ix, data):
    return profile_block(TABA[FOOTS.index(foot), ie, ix], data)


def grid_fit(foot, data, ies, ixs):
    """best chi^2 over the (e, x_c) sub-grid; returns (chi2, ie, ix, im) and the full surface."""
    surf = {}; best = None
    for ie in ies:
        for ix in ixs:
            c_, im = profile_mass(foot, ie, ix, data)
            surf[(ie, ix)] = c_
            if best is None or c_ < best[0]: best = (c_, ie, ix, im)
    return best, surf


ALL_E = list(range(len(ES))); ALL_X = list(range(len(XCS)))
def nearest_e(v): return int(np.argmin(np.abs(np.log10(np.maximum(ES, 1e-12)) - np.log10(v))))
PRIOR_E = [i for i, e in enumerate(ES) if 0.002 <= e <= 0.02]

# ------------------------------------------------------------------ synthetic data (built before the fits so MUTATE can use it)
rng = np.random.default_rng(20260925)
Lch = np.linalg.cholesky(Cf)
LMS_TRUE = [10.2, 10.6, 10.9, 11.2]
def synth(foot, ie, ix):
    ims = [int(np.argmin(np.abs(LM - l))) for l in LMS_TRUE]
    mean = np.concatenate([TAB[(foot, ie, ix, ims[b])][b] for b in range(4)])
    draw = mean + Lch @ rng.standard_normal(4 * npb)
    return [draw[b * npb:(b + 1) * npb] for b in range(4)]
DATA = [np.array(e) for e in Ed]
if MUTATE:
    DATA = synth("canonical", nearest_e(1e-4), 0)
    P(f"*** MUTATE=1: the 'data' are synthetic from the EFE-only model (e = {ES[nearest_e(1e-4)]}, no switch) ***")

# ============================================================================================ E1
banner("E1  MACHINERY: vectorised projection = L342's loop; e = 0 reproduces L342's no-switch chi^2")
Mb_t = 10 ** 10.7 * MS; M_t = model_M(Mb_t, A0["canonical"], 0.0)
d_loop = esd_from_M(M_t, Mb_t, 5.0, loop=True)[1]; d_vec = esd_from_M(M_t, Mb_t, 5.0)[1]
rel = float(np.max(np.abs(d_vec - d_loop) / np.abs(d_loop)))
l342_out = open(os.path.join(REPO, "real_research", "g03_audit_2026", "L342_bound_region_switch.out")).read()
repro = {}
for foot in ("canonical", "alt"):                                 # L342's recipe: 0.1-dex mass grid, diagonal chi^2 choice
    mods = []
    for b in range(4):
        bb = None
        for im in range(0, len(LM), 5):
            mk = TAB[(foot, 0, 0, im)][b]; c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
            if bb is None or c_ < bb[0]: bb = (c_, mk)
        mods.append(bb[1])
    repro[foot] = round(chi2_full(mods, [np.array(e) for e in Ed]), 1)
ok1 = rel < 1e-9 and all(f"{repro[f_]:.1f}" in l342_out for f_ in repro)
check("E1 the vectorised projection equals L342's loop (max rel diff < 1e-9) and the e = 0, no-switch model "
      "reproduces L342's chi^2 verbatim", f"max rel diff {rel:.2e}; no-switch chi^2 {repro}", ok1)

# ============================================================================================ E2
banner("E2  THE EFE LAW'S LIMITS (exact angular average of the QUMOND flux)")
lim = {}
for e in (0.003, 0.01, 0.03):
    ya = np.array([1e-4 * e]); yb = np.array([1e3 * e])
    nu_e = float(nu_mono_arr(e)); L_e = float((np.log(nu_mono_arr(e * 1.0001)) - np.log(nu_mono_arr(e / 1.0001))) / (2 * np.log(1.0001)))
    lo = float(N_of(ya, e)[0]) / (nu_e * (1 + L_e / 3)); hi = float(N_of(yb, e)[0] / nu_mono_arr(yb)[0])
    lim[e] = {"N(y<<e)/[nu(e)(1+L_e/3)]": round(lo, 5), "N(y>>e)/nu(y)": round(hi, 5), "boost at large r": round(nu_e * (1 + L_e / 3), 2)}
    P(f"    e = {e:<6}: N(y<<e) / nu(e)(1+L_e/3) = {lo:.5f};  N(y>>e)/nu(y) = {hi:.5f};  asymptotic M_dyn/M_b = {nu_e * (1 + L_e / 3):.2f}")
e0ok = bool(np.allclose(N_of(YT[::50], 0.0), nu_mono_arr(YT[::50])))
ok2 = e0ok and all(abs(v["N(y<<e)/[nu(e)(1+L_e/3)]"] - 1) < 0.01 and abs(v["N(y>>e)/nu(y)"] - 1) < 0.01 for v in lim.values())
OUT["numbers"]["E2"] = {str(k): v for k, v in lim.items()}
check("E2 N(y, 0) = nu(y); N -> nu(e)(1 + L_e/3) for y << e and -> nu(y) for y >> e (1%)", lim, ok2,
      "under the external field the phantom mass saturates at a finite multiple of M_b: the EFE is itself a truncation")

# ============================================================================================ E3-E5
banner("E3-E5  SWITCH vs EXTERNAL FIELD vs BOTH (shared parameters, M_b per bin profiled, full covariance)")
res = {}
for foot in ("canonical", "alt"):
    none_, _ = grid_fit(foot, DATA, [0], [0])
    sw, _ = grid_fit(foot, DATA, [0], ALL_X)
    efe, surf_e = grid_fit(foot, DATA, ALL_E, [0])
    both, surf_b = grid_fit(foot, DATA, ALL_E, ALL_X)
    efe_p, _ = grid_fit(foot, DATA, PRIOR_E, [0])
    both_p, _ = grid_fit(foot, DATA, PRIOR_E, ALL_X)
    # switch gain at each fixed e (profiled over x_c)
    gain_at_e = {ES[ie]: min(surf_b[(ie, ix)] for ix in ALL_X) - surf_b[(ie, 0)] for ie in ALL_E[::5]}
    prof_e = np.array([min(surf_b[(ie, ix)] for ix in ALL_X) for ie in ALL_E])
    ok_e = [ES[ie] for ie in ALL_E if prof_e[ie] <= both[0] + 4.0]
    res[foot] = {
        "chi2_none": none_[0], "chi2_switch": sw[0], "xc_switch": XCS[sw[2]],
        "chi2_efe": efe[0], "e_efe": ES[efe[1]], "chi2_both": both[0], "e_both": ES[both[1]], "xc_both": XCS[both[2]],
        "chi2_efe_prior": efe_p[0], "e_efe_prior": ES[efe_p[1]], "chi2_both_prior": both_p[0],
        "e_both_prior": ES[both_p[1]], "xc_both_prior": XCS[both_p[2]],
        "switch_gain_given_efe": both[0] - efe[0], "switch_gain_given_efe_prior": both_p[0] - efe_p[0],
        "efe_gain_given_nothing": efe[0] - none_[0], "efe_minus_switch": efe[0] - sw[0],
        "switch_gain_at_fixed_e": gain_at_e, "logM_efe": [float(LM[i]) for i in efe[3]],
        "logM_switch": [float(LM[i]) for i in sw[3]], "e_bound_dchi2_4": max(ok_e),
        "chi2_profile_vs_e": dict(zip(ES, prof_e.round(2).tolist()))}
    r = res[foot]
    P(f"    {foot:9s}: none {r['chi2_none']:.1f} | switch only (x_c {r['xc_switch']}) {r['chi2_switch']:.1f} | "
      f"EFE only (e {r['e_efe']}) {r['chi2_efe']:.1f} | both (e {r['e_both']}, x_c {r['xc_both']}) {r['chi2_both']:.1f}")
    P(f"               e in [0.002, 0.02]: EFE only (e {r['e_efe_prior']}) {r['chi2_efe_prior']:.1f} | both (e {r['e_both_prior']}, "
      f"x_c {r['xc_both_prior']}) {r['chi2_both_prior']:.1f}")
    P(f"               switch gain given the EFE: {r['switch_gain_given_efe']:+.2f} (e free), {r['switch_gain_given_efe_prior']:+.2f} (e in prior);"
      f"  EFE gain vs nothing: {r['efe_gain_given_nothing']:+.2f};  EFE-only minus switch-only: {r['efe_minus_switch']:+.2f}")
    P(f"               switch gain at fixed e: " + ", ".join(f"{k:.2g}: {v:+.1f}" for k, v in gain_at_e.items()))
    P(f"               chi^2 profile vs e (x_c, M_b profiled): " + ", ".join(f"{ES[ie]:.2g}: {prof_e[ie]:.1f}" for ie in ALL_E[::3]))
    P(f"               KiDS bound (Delta chi^2 <= 4 above best): e <= {max(ok_e):.3g}")
OUT["numbers"]["E3_E5"] = res
g_free = {f_: round(res[f_]["switch_gain_given_efe"], 2) for f_ in res}
g_prior = {f_: round(res[f_]["switch_gain_given_efe_prior"], 2) for f_ in res}
check("E3a the switch still improves chi^2 by >= 4 once the external field is in (e free on 0..0.1, both footings)",
      g_free, all(v <= -4 for v in g_free.values()),
      "if it fails, the KiDS fall-off is carried by the framework's own EFE and is not evidence for the switch")
check("E3b the same with e restricted to the physical range for isolated field lenses (0.002-0.02 a0)",
      g_prior, all(v <= -4 for v in g_prior.values()), "", load_bearing=True)
check("E4 (documentary) the EFE-only fit: best external field and its chi^2 gain over no truncation",
      {f_: f"e = {res[f_]['e_efe']}, Delta chi^2 {res[f_]['efe_gain_given_nothing']:+.1f}" for f_ in res}, True,
      "a best e inside 0.002-0.02 is what isolated field galaxies should feel", load_bearing=False)
check("E5 (documentary) mass scaling: chi^2(EFE only) - chi^2(switch only), one shared parameter each "
      "(r_e ~ M^(1/2) vs r_t ~ M^(1/4))", {f_: round(res[f_]["efe_minus_switch"], 2) for f_ in res}, True,
      "negative favours the EFE's scaling, positive the switch's", load_bearing=False)

# ============================================================================================ E6
banner("E6  POWER: CAN FOUR MASS BINS TELL THE SWITCH FROM THE EXTERNAL FIELD? (canonical, 20 draws each)")
NDRAW = 20
e_true = res["canonical"]["e_efe"] if res["canonical"]["e_efe"] > 0 else ES[nearest_e(1e-4)]
pw = {}
for label, (ie_t, ix_t) in (("switch only, x_c = 5", (0, XCS.index(5.0))), (f"EFE only, e = {e_true:.3g}", (ES.index(e_true), 0))):
    d_ = []
    for _ in range(NDRAW):
        dat = synth("canonical", ie_t, ix_t)
        s_, _ = grid_fit("canonical", dat, [0], ALL_X); f_, _ = grid_fit("canonical", dat, ALL_E, [0])
        d_.append(f_[0] - s_[0])                                   # > 0: switch fits better
    d_ = np.array(d_)
    right = float(np.mean(d_ >= 2)) if label.startswith("switch") else float(np.mean(d_ <= -2))
    pw[label] = {"dchi2_efe_minus_switch": d_.round(2).tolist(), "median": float(np.median(d_)), "recovered_frac": right}
    P(f"    truth = {label:24s}: chi^2(EFE) - chi^2(switch) median {np.median(d_):+.2f}; true family preferred by >= 2 in "
      f"{right:.2f} of draws")
OUT["numbers"]["E6"] = pw
fr = {k: v["recovered_frac"] for k, v in pw.items()}
check("E6 the data can tell the two truncations apart: the true family is preferred by Delta chi^2 >= 2 in >= 70% "
      "of draws, for both truths", fr, all(v >= 0.7 for v in fr.values()),
      "if not, KiDS-1000 alone cannot say WHICH mechanism ends the phantom")

# ============================================================================================ E7
banner("E7  THE KiDS BOUND ON A SINGLE EXTERNAL FIELD (M_b per bin and x_c profiled)")
bound = {f_: res[f_]["e_bound_dchi2_4"] for f_ in res}
check("E7 (documentary) KiDS-1000 bound on one shared Newtonian external field e = g_ext/a0 (Delta chi^2 <= 4)",
      {f_: f"e <= {v:.3g}" for f_, v in bound.items()}, True, "", load_bearing=False)

# ============================================================================================ E8
banner("E8  THE CONSTRUCTION'S OWN EXTERNAL FIELD: LCDM's linear web (L342 restores its growth), z = 0.25")
TH27 = 2.7255 / 2.7; NS, S8 = 0.9649, 0.8111
def T_eh(k):                                                     # Eisenstein & Hu 1998 no-wiggle, k in 1/Mpc
    omh2 = Om * h * h; fb = Ob / Om
    s_ = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * (Ob * h * h) ** 0.75)
    aG = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    Gm = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s_) ** 4)); q = k * TH27 ** 2 / (Gm * h)
    L_ = np.log(2 * np.e + 1.8 * q); C_ = 14.2 + 731 / (1 + 62.5 * q); return L_ / (L_ + C_ * q * q)
def W_th(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
kk = np.geomspace(1e-5, 50, 20000); Pk = kk ** NS * T_eh(kk) ** 2
Pk *= S8 ** 2 / _trap(Pk * W_th(kk * 8 / h) ** 2 * kk ** 2 / (2 * math.pi ** 2), kk)
def growth(z):
    a_ = np.linspace(1e-4, 1, 20001)
    def D_(a1):
        aa = a_[a_ <= a1]; E = np.sqrt(Om / aa ** 3 + OL); return math.sqrt(Om / a1 ** 3 + OL) * _trap(1 / (aa * E) ** 3, aa)
    return D_(1 / (1 + z)) / D_(1.0)
ZL = 0.25; DZ = growth(ZL); fz = (Om * (1 + ZL) ** 3 / (Om * (1 + ZL) ** 3 + OL)) ** 0.55
Hz_kms = 100 * h * math.sqrt(Om * (1 + ZL) ** 3 + OL)
sig = {}
for Rs in (4.0, 16.0):
    I_ = _trap(Pk * W_th(kk * Rs) ** 2, kk) / (2 * math.pi ** 2)                      # Mpc^2
    sg = 1.5 * Om * H0 ** 2 * (1 + ZL) ** 2 * DZ * math.sqrt(I_) * Mpc                 # m/s^2, 3D rms
    sv = fz * Hz_kms * DZ * math.sqrt(I_) / (1 + ZL)                                   # km/s, 3D rms (physical)
    sig[Rs] = {"sigma_g3D_m_s2": sg, "sigma_v1D_km_s": sv / math.sqrt(3),
               "sigma_g3D_over_a0": {f_: sg / A0[f_] for f_ in FOOTS}}
    P(f"    smoothing {Rs:>4} Mpc: sigma_g,3D = {sg:.3e} m/s^2 = {sg / A0['canonical']:.4f} a0 (canonical), "
      f"{sg / A0['alt']:.4f} a0 (alt);  sigma_v,1D = {sv / math.sqrt(3):.0f} km/s")
OUT["numbers"]["E8"] = {str(k): v for k, v in sig.items()}
check("E8 (documentary) the linear-theory field is the standard one: sigma_v,1D within 200-400 km/s at both smoothings",
      {k: round(v["sigma_v1D_km_s"]) for k, v in sig.items()}, all(200 < v["sigma_v1D_km_s"] < 400 for v in sig.values()),
      "the same integral that sets the field sets the peculiar velocities, which are observed at ~300 km/s",
      load_bearing=False)

# ------------------------------------------------------------------ stacked models: |g_ext| distributed over the lenses
rs = np.random.default_rng(7)
GAUSS = rs.standard_normal((200000, 3))
LOGE = np.log10(np.maximum(np.array(ES[1:]), 1e-12))
def stack_weights(e_samples):
    w = np.zeros(len(ES)); le = np.log10(np.maximum(e_samples, 1e-12))
    below = le < LOGE[0] - 0.5 * (LOGE[1] - LOGE[0]); w[0] += below.sum()
    idx = np.clip(np.rint((le[~below] - LOGE[0]) / (LOGE[1] - LOGE[0])).astype(int), 0, len(LOGE) - 1) + 1
    np.add.at(w, idx, 1.0); return w / w.sum()
def maxwell_e(sig3d): return np.linalg.norm(GAUSS, axis=1) * sig3d / math.sqrt(3)      # |g|/a0 samples
def stacked_fit(foot, data, w, xcs=ALL_X, sel=None):
    jf = FOOTS.index(foot); best = None
    for ix in xcs:
        blk = np.tensordot(w, TABA[jf, :, ix], axes=(0, 0))
        c_, im = profile_block(blk, data, sel)
        if best is None or c_ < best[0]: best = (c_, ix, im)
    return best

banner("E9-E12  C-H/K + SWITCH WITH ITS OWN EXTERNAL FIELD, AGAINST KiDS-1000 (stacked, full covariance)")
E9 = {}
for foot in FOOTS:
    ref = res[foot]["chi2_switch"]
    row = {"chi2_switch_no_efe": ref}
    for lab, sig3 in (("all matter, 16 Mpc", sig[16.0]["sigma_g3D_over_a0"][foot]),
                      ("all matter, 4 Mpc", sig[4.0]["sigma_g3D_over_a0"][foot]),
                      ("baryons only, 16 Mpc", sig[16.0]["sigma_g3D_over_a0"][foot] * Ob / Om)):
        c_, ix, im = stacked_fit(foot, DATA, stack_weights(maxwell_e(sig3)))
        row[lab] = {"sigma3D_over_a0": sig3, "chi2": c_, "dchi2": c_ - ref, "xc": XCS[ix]}
    sig3 = sig[16.0]["sigma_g3D_over_a0"][foot]
    c_, ix, im = stacked_fit(foot, DATA, stack_weights(maxwell_e(sig3) ** 2))                # pure MOND: e_N = e_M^2
    row["pure-MOND control"] = {"median_eN": float(np.median(maxwell_e(sig3) ** 2)), "chi2": c_, "dchi2": c_ - ref,
                                "xc": XCS[ix]}
    scan = []
    for s3 in np.geomspace(1e-5, 3e-2, 22):
        c_, ix, im = stacked_fit(foot, DATA, stack_weights(maxwell_e(s3)))
        scan.append((float(s3), c_ - ref))
    okb = [s3 for s3, d in scan if d <= 4.0]
    row["sigma_bound_dchi2_4"] = max(okb) if okb else None; row["scan"] = scan
    E9[foot] = row
    P(f"    {foot:9s}: switch, no EFE: chi^2 {ref:.1f}")
    for lab in ("all matter, 16 Mpc", "all matter, 4 Mpc", "baryons only, 16 Mpc"):
        r_ = row[lab]
        P(f"      {lab:22s}: sigma_g,3D = {r_['sigma3D_over_a0']:.4f} a0 -> chi^2 {r_['chi2']:.1f} (Delta {r_['dchi2']:+.1f}), best x_c {r_['xc']}")
    r_ = row["pure-MOND control"]
    P(f"      {'pure-MOND control':22s}: median e_N = {r_['median_eN']:.2e} -> chi^2 {r_['chi2']:.1f} (Delta {r_['dchi2']:+.1f})")
    P(f"      KiDS bound on the stacked rms field (Delta chi^2 <= 4): sigma_g,3D <= {row['sigma_bound_dchi2_4']:.3g} a0 "
      f"-- {sig[16.0]['sigma_g3D_over_a0'][foot] / row['sigma_bound_dchi2_4']:.0f}x below the construction's own field")
OUT["numbers"]["E9_E12"] = E9
d9 = {f_: round(E9[f_]["all matter, 16 Mpc"]["dchi2"], 1) for f_ in FOOTS}
check("E9 C-H/K + switch with its own external field (LCDM linear web, Maxwell-stacked, 16 Mpc smoothing) fits "
      "KiDS-1000 within Delta chi^2 <= 4 of the no-EFE switch fit, both footings", d9, all(v <= 4 for v in d9.values()),
      "the field the construction's own linear web exerts on an isolated lens, entering the kernel as the Galaxy's "
      "field enters it for the Sun (L340 S1)")
check("E10 (documentary) the same with a kernel sourced by baryons only", {f_: round(E9[f_]["baryons only, 16 Mpc"]["dchi2"], 1)
      for f_ in FOOTS}, True, "", load_bearing=False)
check("E11 (documentary control) pure MOND, whose large-scale field is MOND-level (e_N = e_M^2)",
      {f_: round(E9[f_]["pure-MOND control"]["dchi2"], 1) for f_ in FOOTS}, True,
      "the same machinery with a field ~100x weaker in the kernel's argument; it too sits above the KiDS bound (E12), "
      "by ~2x, on this base model (no two-halo term, which would help it most)", load_bearing=False)
check("E12 (documentary) KiDS bound on the rms Newtonian external field, stacked (Delta chi^2 <= 4)",
      {f_: f"sigma_g,3D <= {E9[f_]['sigma_bound_dchi2_4']:.3g} a0" for f_ in FOOTS}, True, "", load_bearing=False)

# ============================================================================================ E13
banner("E13  THE GATE INSIDE R <= 0.3 Mpc (no two-halo contribution possible; Brouwer+21's clean isolated range)")
SEL = [b * npb + i for b in range(4) for i in range(npb) if Rd[b][i] <= 0.3]
E13 = {}
for foot in FOOTS:
    ref = min(profile_block(TABA[FOOTS.index(foot), 0, ix], DATA, SEL)[0] for ix in ALL_X)
    own = stacked_fit(foot, DATA, stack_weights(maxwell_e(sig[16.0]["sigma_g3D_over_a0"][foot])), sel=SEL)[0]
    bar = stacked_fit(foot, DATA, stack_weights(maxwell_e(sig[16.0]["sigma_g3D_over_a0"][foot] * Ob / Om)), sel=SEL)[0]
    pm = stacked_fit(foot, DATA, stack_weights(maxwell_e(sig[16.0]["sigma_g3D_over_a0"][foot]) ** 2), sel=SEL)[0]
    E13[foot] = {"n_points": len(SEL), "chi2_no_efe": ref, "dchi2_own_field": own - ref, "dchi2_baryons_only": bar - ref,
                 "dchi2_pure_mond": pm - ref}
    P(f"    {foot:9s}: {len(SEL)} points; no-EFE chi^2 {ref:.1f};  own field {own - ref:+.1f};  baryons-only {bar - ref:+.1f};  "
      f"pure MOND {pm - ref:+.1f}")

banner("E14  THE FIELD'S MAGNITUDE: Brouwer+21's adopted isolated-lens field, e = 0.003 (actual), mean |g_ext|")
E14 = {}
S3_B21 = 0.003 / math.sqrt(8 / (3 * math.pi))                   # Maxwell: mean |g| = sqrt(8/(3 pi)) sigma_3D
QUIET = {f_: float(np.mean(maxwell_e(sig[16.0]["sigma_g3D_over_a0"][f_]) <= 0.003)) for f_ in FOOTS}
P(f"    fraction of E8's Maxwell field (16 Mpc) with |g_ext| <= 0.003 a0: {QUIET}")
for foot in FOOTS:
    ref_all = res[foot]["chi2_switch"]
    ref_in = min(profile_block(TABA[FOOTS.index(foot), 0, ix], DATA, SEL)[0] for ix in ALL_X)
    row = {}
    for lab, fn in (("construction (e_N = e)", lambda x: x), ("pure MOND (e_N = e^2)", lambda x: x ** 2)):
        wts = stack_weights(fn(maxwell_e(S3_B21)))
        row[lab] = {"dchi2_all": stacked_fit(foot, DATA, wts)[0] - ref_all,
                    "dchi2_inside_0.3Mpc": stacked_fit(foot, DATA, wts, sel=SEL)[0] - ref_in}
        P(f"    {foot:9s} {lab:24s}: Delta chi^2 {row[lab]['dchi2_all']:+.1f} (all points), {row[lab]['dchi2_inside_0.3Mpc']:+.1f} (R <= 0.3 Mpc)")
    E14[foot] = row
OUT["numbers"]["E14"] = E14; OUT["numbers"]["E14_quiet_fraction"] = QUIET
check("E14 (documentary) at Brouwer+21's adopted isolated-lens field (e = 0.003): construction vs pure MOND",
      {f_: {k: round(v["dchi2_inside_0.3Mpc"], 1) for k, v in E14[f_].items()} for f_ in FOOTS}, True,
      "inside 0.3 Mpc: whether the exclusion inside the clean radius survives a 4x weaker field than E8's", load_bearing=False)
OUT["numbers"]["E13"] = E13
d13 = {f_: round(E13[f_]["dchi2_own_field"], 1) for f_ in FOOTS}
check("E13 inside R <= 0.3 Mpc the construction with its own external field is within Delta chi^2 <= 4 of the no-EFE "
      "fit, both footings", d13, all(v <= 4 for v in d13.values()),
      "a failure here cannot be blamed on the missing two-halo term")

# ============================================================================================ verdict
banner("VERDICT")
rc_, ra_ = res["canonical"], res["alt"]
P(f"""  1. The switch vs the EFE.  Isolated MOND over-predicts KiDS-1000 at R ~ 1-3 Mpc.  L342's switch fixes it (chi^2 {rc_['chi2_none']:.1f} ->
     {rc_['chi2_switch']:.1f} canonical, {ra_['chi2_none']:.1f} -> {ra_['chi2_switch']:.1f} alt), but a weak external field does most of the same
     ({rc_['efe_gain_given_nothing']:+.1f} / {ra_['efe_gain_given_nothing']:+.1f} at e ~ {rc_['e_efe']:.1g}); with it in, the switch adds {rc_['switch_gain_given_efe']:+.1f} / {ra_['switch_gain_given_efe']:+.1f}, and the data cannot
     reliably tell the two truncations apart (E6).  L342's KiDS preference is not specific evidence for the switch.
  2. The construction's own external field.  KiDS allows e <= {bound['canonical']:.2g} / {bound['alt']:.2g} (stacked: sigma_g,3D <= {E9['canonical']['sigma_bound_dchi2_4']:.2g} / {E9['alt']['sigma_bound_dchi2_4']:.2g} a0).
     The switch keeps the linear web Newtonian and LCDM-like, so the web pulls on every lens with sigma_g,3D =
     {sig[16.0]['sigma_g3D_over_a0']['canonical']:.4f} / {sig[16.0]['sigma_g3D_over_a0']['alt']:.4f} a0 -- {sig[16.0]['sigma_g3D_over_a0']['canonical'] / E9['canonical']['sigma_bound_dchi2_4']:.0f}x / {sig[16.0]['sigma_g3D_over_a0']['alt'] / E9['alt']['sigma_bound_dchi2_4']:.0f}x over the bound -- and C-H/K's kernel takes free-fall fields in
     its argument (L340 S1 runs it on the Sun with the Galaxy's field).  Result: chi^2 {d9['canonical']:+.0f} / {d9['alt']:+.0f} (all 60 points),
     {d13['canonical']:+.0f} / {d13['alt']:+.0f} inside 0.3 Mpc, where no two-halo term can help: every lens's phantom would end at ~0.1 Mpc.
     SENSITIVITY: at Brouwer+21's 4x weaker adopted field (e = 0.003; {100 * QUIET['canonical']:.1f}% of points in E8's Maxwell field are
     that quiet) it passes inside 0.3 Mpc ({E14['canonical']['construction (e_N = e)']['dchi2_inside_0.3Mpc']:+.0f} / {E14['alt']['construction (e_N = e)']['dchi2_inside_0.3Mpc']:+.0f}) and fails only on all points ({E14['canonical']['construction (e_N = e)']['dchi2_all']:+.0f} / {E14['alt']['construction (e_N = e)']['dchi2_all']:+.0f}), i.e. at
     0.3-3 Mpc, where a two-halo term would have to make up the deficit.
     A kernel sourced by baryons only: {E9['canonical']['baryons only, 16 Mpc']['dchi2']:+.0f} / {E9['alt']['baryons only, 16 Mpc']['dchi2']:+.0f} on all points but {E13['canonical']['dchi2_baryons_only']:+.1f} / {E13['alt']['dchi2_baryons_only']:+.1f} inside 0.3 Mpc -- its failure
     lies where the missing two-halo term acts, so it is NOT excluded by this lane.
  3. Control: in pure MOND the large-scale field is MOND-level (e_N = e_M^2): {E9['canonical']['pure-MOND control']['dchi2']:+.1f} / {E9['alt']['pure-MOND control']['dchi2']:+.1f} on all points at E8's field,
     {E13['canonical']['dchi2_pure_mond']:+.1f} / {E13['alt']['dchi2_pure_mond']:+.1f} inside 0.3 Mpc; at e = 0.003, {E14['canonical']['pure MOND (e_N = e^2)']['dchi2_all']:+.1f} / {E14['alt']['pure MOND (e_N = e^2)']['dchi2_all']:+.1f} -- the same data and machinery do not exclude it.
  READING: as built (the kernel's argument is the total filtered Newtonian field, all matter; the switch leaves the web
  Newtonian), C-H/K + switch fails KiDS-1000 isolated lensing through its own external-field effect: by +570 on all
  points, and inside the radius where isolation is certain if isolated lenses feel the LCDM-typical field.  What would
  make it a clean exclusion: the field conditioned on isolation, and a two-halo term at 0.3-3 Mpc.  Doors this leaves: (i) a kernel sourced by baryons only (survives inside
  0.3 Mpc here; decided at 0.3-3 Mpc only once a two-halo term is modelled); (ii) a kernel blind to the large-scale
  field (e.g. sourced only by the bound region's own matter) -- new ingredients, each constrained by the Solar-System
  floor, which needs the Galaxy's field in the kernel.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} "
  f"({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
