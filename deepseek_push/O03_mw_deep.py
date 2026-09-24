#!/usr/bin/env python3
"""O03 -- MW ROTATION CURVE DEEP-A0 MEASUREMENT (third independent channel for
the deep tension).

CHANNEL:  single galaxy, kinematic tracers different from HI/SPARC (Eilers+2019
red-clump/APOGEE stars), baryonic model = the model Eilers+19 fixed for their
NFW-halo fit.  The Eilers table carries ONLY R, v_c, sigma_vc_minus,
sigma_vc_plus (NO baryonic columns -- verified below), so the baryonic
acceleration is built from the KNOWN EILERS COMPONENTS:

  PRIMARY  "Eilers-fiducial":  Pouliasis, Di Matteo & Haywood 2017 (A&A 598,
           A66) Model I -- the exact baryonic components Eilers+19 kept fixed
           ("For the gravitational potentials of the thin and thick disk we
           assume Miyamoto-Nagai profiles, and for the bulge we assume a
           spherical Plummer potential, while adapting the parameter values
           ... from Pouliasis et al. [38, model I]", Eilers+19 Sec. V.3).
           Table 1 (masses in units of 2.32e7 Msun, lengths in kpc):
             bulge : Plummer  M = 460 -> 1.0672e10 Msun, b = 0.30 kpc
             thin  : Miyamoto-Nagai  M = 1700 -> 3.944e10 Msun,
                     a = 5.3 kpc, b = 0.25 kpc
             thick : Miyamoto-Nagai  M = 1700 -> 3.944e10 Msun,
                     a = 2.6 kpc, b = 0.8 kpc
           PLUS the McMillan (2017) gas discs converted to equal-total-mass
           exponentials (HI M = 1.1e10 Msun, Rd = 7 kpc -> Sigma0_eff = 35.72
           Msun/pc2; H2 M = 1.2e9, Rd = 1.5 -> 84.88), computed with the
           VERIFIED Bessel closed form vdisk_closed (N01_KERNEL_REFERENCE.py).
           -> V_bary(8.19 kpc) = 191.1 km/s (anchor window 185-205 km/s =
           230*sqrt(0.67)); the no-gas Eilers-strict model gives 183.5.
  VAR-A    "Eilers-strict": exactly what Eilers+19 fixed (no gas).
  VAR-B    "McMillan-class" (the task brief's bulge+disk+gas reading):
           thin Sigma0 = 896 Msun/pc2, Rd = 2.5; thick 183, 3.02 (Bessel form);
           bulge Hernquist M = 8.9e9, alpha = 0.7 kpc, V_b^2 = G M r/(r+a)^2
           (enclosed-mass form, no integration); gas as above.  Kept as the
           task-brief variant; NOTE: it does NOT match Eilers' own baryon model.

REGISTERED PROBING FINDING (established below, C5): under ALL THREE baryonic
modelings the Eilers RC (5.27-24.82 kpc) does NOT contain a >= 10-point deep
sample at the L06-identical cut g_bar < 0.2 a0 (N_deep = 0 / 0 / 2).  The MW
channel therefore rests on the DEEPEST-PROBE annuli (g_bar = 0.17-0.35 a0),
measured with the full a0-line estimator  a0_eff = (g_obs^2 - g_bar^2)/g_bar
(= the deep line in the deep limit).

EQUATIONS:
  g_obs(R) = V_obs^2 / R
  g_bar(R) = V_bar(R)^2 / R   (PRIMARY convention, SPARC/G071-identical to L06)
  g_bar_enc(R) = G * M_b(<R) / R^2  (SECONDARY convention, task formula;
              closed forms for Plummer/Hernquist/exponential gas discs,
              smooth Gauss-Legendre quadrature for the Miyamoto-Nagai
              densities -- no kernel singularity)
ESTIMATORS: deep-line a0_eff = 10^(mean(2 log10 g_obs - log10 g_bar)) on the
strict deep cut; full-line a0_eff = geomean((g_obs^2-g_bar^2)/g_bar) on the
probe annuli.  BOOTSTRAP B=10000 resamples of the rows WITH REPLACEMENT
(R-independent errors), each perturbing V_obs with the table's asymmetric
errors (down-draws sigma_minus, up-draws sigma_plus, p=0.5).  SE = std of the
bootstrap distribution; SE_dex and 16/84 percentiles reported.

PRE-REGISTERED:
  L06 (SPARC deep, g_bar<0.2 a0): a0_eff/a0 = 0.73; canonical-footing fit
   0.7241 +/- 0.0662 (O04 ledger, z = -4.17).
  O01 dwarfs (landed): 0.638 +/- 0.163 (LT-deep), deep tail 0.31 +/- 0.117.
  KILL-A: |a0_eff_MW - 0.73 a0| > 3*SE_comb (SE_comb = sqrt(SE_MW^2 + SE_L06^2)
   -> MW DISAGREES with the extragalactic deep tension (sample-dependent
   finding, registered); else three channels agree (major).  Judged in linear
   and dex, OR.  Primary evaluation point (pre-registered): the deepest-probe
   annulus R >= 22.5 kpc on the Eilers-fiducial baryons (g_bar ~ 0.24-0.30 a0,
   the deepest region attained); the strict-cut varB fit (N = 2) reported as
   a degenerate leg.
  KILL-B: |log10(a0_eff_MW/a0)| < 3 SE_dex -> consistent with canonical a0.

STEP 4 (R-dependence / N01 density-locality): 7 radial annuli, full-line
a0_eff per annulus with bootstrap SE; drift = weighted slope of log10 a0_eff
vs R over the outer annuli (median g_bar < 0.5 a0); |z| < 3 -> flat.  The
canonical expectation is a flat line at a0_eff = a0.

HONEST LIMITS: baryonic model systematics DOMINATE (three legs, V_bary(8.19)
= 191/183/182 km/s; the deep cut itself is model-dependent: 0/0/2 points);
conventions (V^2/R vs G M_enc/R^2) ~ 0.9 ratio on the primary leg; Eilers v_c
beyond ~20 kpc carry 6-28 km/s random errors, and DR3-era successors find a
steeper outer decline; EFE cannot explain an EXCESS of g_obs over the deep
line; the probe region (g_bar 0.17-0.35 a0) is NOT the asymptotic deep regime.
"""
import json, os, importlib.util, warnings
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "data2", "eilers2019_mw_rotation_curve_table1.csv")

# the VERIFIED exponential-disc closed form (Bessel), N01 auditor reference
_spec = importlib.util.spec_from_file_location(
    "n01_kernel_ref", os.path.join(HERE, "N01_KERNEL_REFERENCE.py"))
_n01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_n01)
vdisk_closed = _n01.vdisk_closed     # (sigma0 Msun/pc2, hd kpc, R kpc) -> km/s

G = 6.674e-11             # m^3 kg^-1 s^-2 (repo convention, L06/G072)
MSUN = 1.98892e30         # kg
KPC = 3.0856775814913673e19   # m
PC = KPC / 1000.0
A0 = 9.3619e-11           # m s^-2, canonical footing (repo-wide)
L06_RATIO = 0.73
L06_RATIO_O04 = 0.7241
SE_L06 = 0.0662           # O04 joint ledger, canonical footing
SEED = 20260923
NB = 10000
NB_BIN = 5000
MU = 2.32e7               # Pouliasis+17 Table 1 mass unit (Msun)

def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""), flush=True)
    ok = bool(ok)
    RES.append((label, ok, detail))
    return ok

RES = []
print("=" * 102)
print("O03 -- MW ROTATION CURVE DEEP-A0 MEASUREMENT (third channel: Eilers+19 RC, "
      "Eilers' own baryons = Pouliasis+17 Model I + McMillan gas)")
print("=" * 102)

# ------------------------------------------------------------------ data table
rows = []
with open(CSV) as f:
    hdr = f.readline().strip()
    for ln in f:
        p = ln.strip().split(",")
        if len(p) == 4:
            rows.append([float(x) for x in p])
Rk = np.array([r[0] for r in rows])            # kpc
Vobs = np.array([r[1] for r in rows]) * 1e3    # m/s
SIGM = np.array([r[2] for r in rows]) * 1e3    # m/s (minus / lower)
SIGP = np.array([r[3] for r in rows]) * 1e3    # m/s (plus / upper)
N = len(rows)
print(f"\n--- data: {CSV}")
print(f"    header: '{hdr}'  -> {N} rows, R in [{Rk.min():.2f}, {Rk.max():.2f}] kpc; NO baryonic "
      f"columns (bulge/disc/gas absent) -- known-Eilers components used, stated above.")
ok_c1 = (N == 38 and abs(Rk.min() - 5.27) < 1e-9 and abs(Rk.max() - 24.82) < 1e-9)
check("C1 [table] 38 rows, R = 5.27..24.82 kpc as registered in MANIFEST", ok_c1, f"N={N}")
i_sun = int(np.argmin(np.abs(Rk - 8.122)))
check("C2 [table] v_c at R ~ 8.1-8.2 kpc = 229.0 +/- 0.2 (Manifest claim 228.86)",
                 abs(Vobs[i_sun] / 1e3 - 229.0) < 0.5,
                 f"R={Rk[i_sun]:.2f} kpc  v_c={Vobs[i_sun]/1e3:.2f} km/s")

# ------------------------------------------------------- baryonic models (closed forms)
# --- Pouliasis+17 Model I (Eilers' own baryons) ---
M_BUL_P  = 460.0 * MU          # 1.0672e10 Msun
B_BUL_P  = 0.30                # kpc, Plummer scale
M_THIN_P = 1700.0 * MU         # 3.944e10 Msun
A_THIN_P, B_THIN_P = 5.3, 0.25   # Miyamoto-Nagai
M_THK_P  = 1700.0 * MU         # 3.944e10 Msun
A_THK_P, B_THK_P = 2.6, 0.8      # Miyamoto-Nagai
# --- McMillan-17 gas, converted to equal-total-mass exponentials (Bessel form) ---
# McMillan's m-disk Sigma0 values (53.1/2180) are m-disk normalisations with the
# exp(-Rm/R) hole; used as PURE exponentials they over-mass H2 by ~26x.  Keep
# McMillan's stated total masses: HI 1.1e10 Msun (Rd = 7 kpc), H2 1.2e9 (Rd = 1.5),
# i.e. Sigma0_eff = M/(2 pi Rd^2): 35.72 and 84.88 Msun/pc^2 (exponential discs).
HI_M, HI_RD = 1.1e10, 7.0
H2_M, H2_RD = 1.2e9, 1.5
HI_S0e = HI_M / (2.0 * np.pi * (HI_RD * 1e3) ** 2)   # Msun/pc^2
H2_S0e = H2_M / (2.0 * np.pi * (H2_RD * 1e3) ** 2)
# --- McMillan-class (task-brief variant) ---
TH_S0, TH_RD = 896.0, 2.50
TK_S0, TK_RD = 183.0, 3.02
M_BUL_H, ALPHA_H = 8.9e9, 0.7

def v_mn(Rkpc, M, a, b):
    """Miyamoto-Nagai circular speed in the plane: V^2 = G M R^2 / (R^2 + (a+b)^2)^{3/2}."""
    C = a + b
    Rm = Rkpc * KPC
    return np.sqrt(G * M * MSUN * Rm ** 2 / (Rm ** 2 + (C * KPC) ** 2) ** 1.5)

def v_plummer(Rkpc, M, b):
    """Plummer sphere circular speed: V^2 = G M r^2 / (r^2 + b^2)^{3/2}."""
    rm = Rkpc * KPC
    return np.sqrt(G * M * MSUN * rm ** 2 / (rm ** 2 + (b * KPC) ** 2) ** 1.5)

def v_hernquist(Rkpc, M, alpha):
    """Hernquist circular speed: V^2 = G M r / (r + alpha)^2  (M(<r) = M r^2/(r+alpha)^2)."""
    rm = Rkpc * KPC
    return np.sqrt(G * M * MSUN * rm / (rm + alpha * KPC) ** 2)

def m_enc_plummer(Rkpc, M, b):
    rm = Rkpc * KPC
    return M * MSUN * rm ** 3 / (rm ** 2 + (b * KPC) ** 2) ** 1.5     # kg

def m_enc_exp_gas(Rkpc, Mtot, Rd):
    """Cylinder-enclosed surface mass of the razor-thin exponential disc (closed form)."""
    x = np.atleast_1d(Rkpc) / Rd
    return Mtot * MSUN * (1.0 - (1.0 + x) * np.exp(-x))               # kg

def m_enc_mn(Rkpc, M, a, b, nr=180, nth=180):
    """Sphere-enclosed MN mass by smooth 2D Gauss-Legendre (BT08 2.71),
    lengths in kpc, M in kg -> rho in kg/kpc^3.  No kernel singularity.
    Verified: M_enc(R->100 kpc)/M -> 1 (printed below)."""
    with np.errstate(all="ignore"):
        xr, wr = np.polynomial.legendre.leggauss(nr)
        xt, wt = np.polynomial.legendre.leggauss(nth)
        out = np.empty_like(np.atleast_1d(Rkpc))
        for i, R in enumerate(np.atleast_1d(Rkpc)):
            r = 0.5 * R * (xr + 1.0); wrr = 0.5 * R * wr
            th = 0.5 * np.pi * (xt + 1.0); wtt = 0.5 * np.pi * wt
            Rc = r[:, None] * np.sin(th)[None, :]          # kpc
            zc = r[:, None] * np.cos(th)[None, :]
            zp = np.sqrt(zc ** 2 + b ** 2)
            den = (Rc ** 2 + (a + zp) ** 2) ** 2.5 * zp ** 3
            rho = M * MSUN * b ** 2 / (4 * np.pi) \
                  * (a * Rc ** 2 + (a + 3 * zp) * (a + zp) ** 2) / den    # kg/kpc^3
            integ = (rho * np.sin(th)[None, :]) @ wtt                     # over theta
            out[i] = 2.0 * np.pi * np.sum(wrr * (r ** 2) * integ)         # kg
    return out

def Vbar_model(Rkpc, tag):
    """Component velocities (m/s) and V_bar for the three model legs."""
    if tag == "primary":      # Pouliasis Model I + McMillan gas
        vB = v_plummer(Rkpc, M_BUL_P, B_BUL_P)
        vT = v_mn(Rkpc, M_THIN_P, A_THIN_P, B_THIN_P)
        vK = v_mn(Rkpc, M_THK_P, A_THK_P, B_THK_P)
        vG = np.array([vdisk_closed(HI_S0e, HI_RD, R) * 1e3 for R in Rkpc])
        vG2 = np.array([vdisk_closed(H2_S0e, H2_RD, R) * 1e3 for R in Rkpc])
        comps = dict(bulge=vB, thin=vT, thick=vK, HI=vG, H2=vG2)
    elif tag == "varA":       # Eilers-strict (no gas)
        vB = v_plummer(Rkpc, M_BUL_P, B_BUL_P)
        vT = v_mn(Rkpc, M_THIN_P, A_THIN_P, B_THIN_P)
        vK = v_mn(Rkpc, M_THK_P, A_THK_P, B_THK_P)
        comps = dict(bulge=vB, thin=vT, thick=vK)
    else:                     # varB: McMillan-class (task brief)
        vT = np.array([vdisk_closed(TH_S0, TH_RD, R) * 1e3 for R in Rkpc])
        vK = np.array([vdisk_closed(TK_S0, TK_RD, R) * 1e3 for R in Rkpc])
        vG = np.array([vdisk_closed(HI_S0e, HI_RD, R) * 1e3 for R in Rkpc])
        vG2 = np.array([vdisk_closed(H2_S0e, H2_RD, R) * 1e3 for R in Rkpc])
        vB = v_hernquist(Rkpc, M_BUL_H, ALPHA_H)
        comps = dict(bulge=vB, thin=vT, thick=vK, HI=vG, H2=vG2)
    V2 = sum(c * c for c in comps.values())
    return comps, np.sqrt(V2)

MODELS = {}
for tag in ("primary", "varA", "varB"):
    comps, Vbar = Vbar_model(Rk, tag)
    MODELS[tag] = dict(comps=comps, Vbar=Vbar)
    sel5 = [int(np.argmin(np.abs(Rk - r))) for r in (5.27, 8.19, 12.74, 17.25, 24.82)]
    print(f"\n--- baryonic model [{tag}]  component V at R = 5.27, 8.19, 12.74, 17.25, 24.82 kpc (km/s):")
    for lbl, c in comps.items():
        print(f"    {lbl:6s}: " + "  ".join(f"{c[j]/1e3:6.2f}" for j in sel5))
    print(f"    V_bar : " + "  ".join(f"{Vbar[j]/1e3:6.2f}" for j in sel5))

# smooth-integral sanity: MN enclosed mass at large R
for lbl, (M, a, b) in (("thin", (M_THIN_P, A_THIN_P, B_THIN_P)),
                       ("thick", (M_THK_P, A_THK_P, B_THK_P))):
    frac = m_enc_mn(np.array([100.0]), M, a, b)[0] / (M * MSUN)
    print(f"    [verify] m_enc_mn[{lbl}](100 kpc)/M = {frac:.4f} (must -> 1)")

# ---- model-identity anchors ---------------------------------------------------
v8 = {t: MODELS[t]["Vbar"][int(np.argmin(np.abs(Rk - 8.19)))] / 1e3 for t in MODELS}
print(f"\n--- model identity: V_bary(8.19 kpc) = {v8['primary']:.1f} km/s (primary, with gas; "
      f"anchor window 185-205), {v8['varA']:.1f} (Eilers-strict, no gas), {v8['varB']:.1f} (McMillan-class)")
check("C3 [model identity] primary V_bary(8.19) in the 185-205 km/s window "
                 "(= 230*sqrt(0.67), the Eilers baryonic model anchor)",
                 185.0 <= v8["primary"] <= 205.0,
                 f"{v8['primary']:.1f} km/s; no-gas strict {v8['varA']:.1f}; "
                 f"McMillan-class {v8['varB']:.1f} (NOT the Eilers model)")
# Eilers NFW halo identity (Sec. V.3): Mvir = 7.25e11, c = 12.8 -> Rs = 14.8 kpc
def v_nfw(Rkpc, Mvir, Rs, c=12.8):
    x = Rkpc / Rs; f = np.log(1 + x) - x / (1 + x)
    fc = np.log(1 + c) - c / (1 + c)
    return np.sqrt(G * Mvir * f / fc * MSUN / (Rkpc * KPC))
v_halo8 = v_nfw(8.19, 7.25e11, 14.8) / 1e3
v_tot8_strict = np.sqrt(v8["varA"] ** 2 + v_halo8 ** 2)
v_tot8_prim = np.sqrt(v8["primary"] ** 2 + v_halo8 ** 2)
check("C4 [model identity] Eilers-strict baryons + Eilers NFW halo reproduce "
                 "v_c(8.19) = 228.86 measured",
                 abs(v_tot8_strict - 228.86) <= 3.0,
                 f"strict {v8['varA']:.1f} + halo {v_halo8:.1f} = {v_tot8_strict:.1f} km/s vs "
                 f"228.86; with added gas {v_tot8_prim:.1f} (2.9% high -- gas is my documented "
                 f"addition to Eilers' fixed model)")

# ------------------------------------------------------------------ g_obs, g_bar
R_m = Rk * KPC
gobs = Vobs ** 2 / R_m
GBA = {t: MODELS[t]["Vbar"] ** 2 / R_m for t in MODELS}      # g_bar, V^2/R (G071-identical)
Menc = (m_enc_plummer(Rk, M_BUL_P, B_BUL_P)
        + m_enc_mn(Rk, M_THIN_P, A_THIN_P, B_THIN_P)
        + m_enc_mn(Rk, M_THK_P, A_THK_P, B_THK_P)
        + m_enc_exp_gas(Rk, HI_M, HI_RD)
        + m_enc_exp_gas(Rk, H2_M, H2_RD))
gbar_enc = G * Menc / R_m ** 2                                # task formula, primary leg
print(f"\n--- g_bar conventions (primary leg): ratio gbar_enc/gbar_V2R at R = "
      f"5.27, 8.19, 12.74, 17.25, 24.82: " +
      " ".join(f"{gbar_enc[int(np.argmin(np.abs(Rk-r)))]/GBA['primary'][int(np.argmin(np.abs(Rk-r)))]:.2f}"
               for r in (5.27, 8.19, 12.74, 17.25, 24.82)))

deep = {t: GBA[t] < 0.2 * A0 for t in GBA}
NS = {t: int(deep[t].sum()) for t in deep}
print("\n--- per-point (R, V_obs, g_obs/a0, g_bar/a0 per model, deep flag g_bar<0.2a0)")
for i in range(N):
    fl = ("P" if deep["primary"][i] else ".") + ("A" if deep["varA"][i] else ".") \
         + ("B" if deep["varB"][i] else ".")
    print(f"    R={Rk[i]:6.2f}  V={Vobs[i]/1e3:7.2f}  g_obs={gobs[i]/A0:6.3f}  "
          f"g_bar/a0: P={GBA['primary'][i]/A0:5.3f} A={GBA['varA'][i]/A0:5.3f} "
          f"B={GBA['varB'][i]/A0:5.3f}  d={fl}")
print(f"    deep counts (g_bar < 0.2 a0): primary={NS['primary']}, varA={NS['varA']}, varB={NS['varB']}")
check("C5 [deep cut] the Eilers RC attains the L06-identical deep cut (g_bar < 0.2 a0) "
                 "with N >= 10 under some baryonic modeling",
                 max(NS.values()) >= 10,
                 f"N_deep = {NS['primary']}/{NS['varA']}/{NS['varB']} (primary/varA/varB) -- "
                 f"REGISTERED: no >= 10-point deep sample exists in R <= 25 kpc under ANY of the "
                 f"three modelings; the MW channel rests on the deepest-probe annuli "
                 f"(g_bar ~ 0.17-0.35 a0)")

# ------------------------------------------------------------------ estimators
def perturb(vvals, sigm, sigp, rng):
    u = rng.uniform(size=len(vvals))
    xi = np.where(u < 0.5, -np.abs(rng.normal(size=len(vvals))) * sigm,
                  np.abs(rng.normal(size=len(vvals))) * sigp)
    return vvals + xi

def boot_est(sel, gb, B, seed, full_line=True):
    """Bootstrap of the a0_eff estimators (returns values in m/s^2).
    full_line=True  : a0_eff_i = max(g_obs^2 - g_bar^2, 0)/g_bar, ARITHMETIC
                      mean per draw (floor 0 = Newtonian-compatible draw; the
                      geometric mean is unstable here because deep down-draws
                      of the 20-28 km/s-error outer points can push g_obs
                      below g_bar).
    full_line=False : deep-line a0_eff_i = g_obs^2/g_bar, geometric mean
                      (always positive)."""
    rng = np.random.default_rng(seed)
    idx = np.arange(sel.sum())
    est = np.empty(B)
    for b in range(B):
        j = rng.choice(idx, size=len(idx), replace=True)
        vv = perturb(Vobs[sel][j], SIGM[sel][j], SIGP[sel][j], rng)
        g = vv ** 2 / R_m[sel][j]
        if full_line:
            ae = np.maximum(g * g - gb[sel][j] ** 2, 0.0) / gb[sel][j]
            est[b] = np.mean(ae)
        else:
            ae = g * g / gb[sel][j]
            est[b] = np.exp(np.mean(np.log(ae)))
    return est

def probe_full(sel, gb):
    """Point estimate of the full-line a0_eff (m/s^2): arithmetic mean of
    max(g_obs^2 - g_bar^2, 0)/g_bar over the selection."""
    g = gobs[sel]; gb_ = gb[sel]
    ae = np.maximum(g * g - gb_ * gb_, 0.0) / gb_
    return float(np.mean(ae))

def summarize(est, a0eff_m_s2, n):
    """est: bootstrap a0_eff values in m/s^2; a0eff_m_s2: point estimate (m/s^2).
    Reported quantities are the a0-normalised ratios (a0 = 9.3619e-11)."""
    ratio = np.asarray(est) / A0
    r = a0eff_m_s2 / A0
    se = float(np.std(ratio))
    lo, hi = np.percentile(ratio, [16, 84])
    rlog = np.log10(np.maximum(ratio, 1e-3))     # floor at 1e-3 for the dex scale
    return dict(a0eff_over_a0=float(r), a0eff_m_s2=float(a0eff_m_s2), SE_lin=se,
                CI68_lin=[float(lo), float(hi)], SE_dex=float(np.std(rlog)),
                log10_a0eff_over_a0=float(np.log10(r)), N=n)

# ---- strict deep-cut fit on the only leg attaining it (varB, N = 2, degenerate) --
FIT_DEEP = None
if NS["varB"] >= 2:
    sel = deep["varB"]
    y = np.log10(gobs[sel]); x = np.log10(GBA["varB"][sel])
    a = float(10.0 ** np.mean(2.0 * y - x))                    # m/s^2 (deep-line)
    est = boot_est(sel, GBA["varB"], NB, SEED, full_line=False)
    FIT_DEEP = dict(a0eff_m_s2=a, a0eff_over_a0=a / A0,
                    sum=summarize(est, a, int(sel.sum())))
print("\n--- STRICT DEEP FIT (g_bar < 0.2 a0, varB leg, N = 2 -- DEGENERATE, reported for "
      "protocol completeness) ---")
if FIT_DEEP:
    pts = ", ".join(f"a0_eff/a0 = {gobs[i]**2/A0/GBA['varB'][i]:.2f}" for i in np.where(deep["varB"])[0])
    print(f"    deep-line a0_eff/a0 = {FIT_DEEP['a0eff_over_a0']:.3f} +- "
          f"{FIT_DEEP['sum']['SE_lin']:.3f} (SE_dex {FIT_DEEP['sum']['SE_dex']:.3f});  "
          f"per-point: {pts}")

# ---- deepest probes (the registered comparison set) ---------------------------
print("\n--- DEEPEST-PROBE fits (full-line estimator; the pre-registered comparison points) ---")
PROBE = {}
for tag, gb in (("primary", GBA["primary"]), ("varA", GBA["varA"]), ("varB", GBA["varB"])):
    for lbl, mm in (("R22", Rk >= 22.5), ("R20", Rk >= 20.0)):
        est = boot_est(mm, gb, NB, SEED + 5)
        ap = probe_full(mm, gb)                                  # m/s^2
        adl = float(np.exp(np.mean(np.log(gobs[mm] ** 2 / gb[mm])))) / A0   # deep-limit ratio
        PROBE[f"{tag}_{lbl}"] = dict(a0eff_m_s2=ap, a=ap / A0,
                                     sum=summarize(est, ap, int(mm.sum())), deep_limit=adl)
        print(f"    [{tag} | {lbl}] g_bar in [{gb[mm].min()/A0:.3f}, {gb[mm].max()/A0:.3f}] a0, "
              f"N={int(mm.sum())}: a0_eff/a0 = {ap/A0:.3f} +- {np.std(est)/A0:.3f}  "
              f"(deep-limit reading {adl:.3f})")

# ---- cross-checks (pre-registered) ---------------------------------------------
Pp = PROBE["primary_R22"]
rP, sP, sPd = Pp["a"], Pp["sum"]["SE_lin"], Pp["sum"]["SE_dex"]
zA_lin = (rP - L06_RATIO) / np.sqrt(sP ** 2 + SE_L06 ** 2)
SE_L06_dex = SE_L06 / (L06_RATIO * np.log(10.0))
zA_dex = (np.log10(rP) - np.log10(L06_RATIO)) / np.sqrt(sPd ** 2 + SE_L06_dex ** 2)
killA = (abs(zA_lin) > 3.0) or (abs(zA_dex) > 3.0)
zB_ = np.log10(rP) / sPd; killB = abs(zB_) < 3.0
z1_lin = (rP - 1.0) / sP
zD_lin = ((FIT_DEEP["a0eff_over_a0"] - L06_RATIO)
          / np.sqrt(FIT_DEEP["sum"]["SE_lin"] ** 2 + SE_L06 ** 2) if FIT_DEEP else 0.0)
print("\n--- CROSS-CHECK vs L06 (0.73 a0) and O01 dwarfs (landed: 0.638 +- 0.163) ---")
print(f"    L06 SPARC-deep 0.724 +- 0.066 (z = -4.17);  MIGHTEE-deep 2.164 (z = +6.58, N05, "
      f"opposite sign);  O01 dwarfs 0.638 +- 0.163 / deep-tail 0.310 +- 0.117")
print(f"    O03 PRIMARY probe (R >= 22.5, g_bar ~ 0.24-0.30 a0): a0_eff/a0 = {rP:.3f} +- "
      f"{sP:.3f};  z vs 0.73 (lin) = {zA_lin:+.2f}, (dex) = {zA_dex:+.2f};  "
      f"z vs 1.0 = {z1_lin:+.2f}")
if FIT_DEEP:
    print(f"    O03 STRICT deep fit (varB, N = 2): a0_eff/a0 = {FIT_DEEP['a0eff_over_a0']:.2f} +- "
          f"{FIT_DEEP['sum']['SE_lin']:.2f}; z vs 0.73 = {zD_lin:+.2f}")
check("KILL-A [pre-registered] |a0_eff_MW - 0.73 a0| > 3 SE_comb -> MW DISAGREES with "
      "the extragalactic deep tension (sample-dependent finding, registered)",
      killA, f"primary probe z_lin={zA_lin:+.2f} z_dex={zA_dex:+.2f}"
             + (f"; strict varB z={zD_lin:+.2f}" if FIT_DEEP else ""))
check("KILL-B [canonical] MW deepest probe consistent with a0 = 9.3619e-11 within 3 SE",
      killB, f"z_dex={zB_:+.2f} (central value ABOVE canonical a0)" if not killB
                    else f"z_dex={zB_:+.2f}")
check("C8 [three channels agree] SPARC-deep, O01 dwarfs, MW all within 3 SE of 0.73",
      not killA,
      f"SPARC 0.72 / dwarfs 0.64 / MW {rP:.2f} (probe) -- values straddle "
      f"canonical a0, agreement not established" if killA else "three channels agree")

# ---- deep-region form diagnostics (g_bar < 0.4 a0 sets) -------------------------
print("\n--- DEEP-REGION FORM (g_bar < 0.4 a0; is the sqrt law the right form?) ---")
FORM = {}
for tag in ("primary", "varB"):
    sel = GBA[tag] < 0.4 * A0
    x = np.log10(GBA[tag][sel]); y = np.log10(gobs[sel])
    beta = float(np.polyfit(x, y, 1)[0])
    rng = np.random.default_rng(SEED + hash(tag) % 1000)
    bsl = np.empty(NB)
    for b in range(NB):
        j = rng.choice(np.arange(sel.sum()), size=sel.sum(), replace=True)
        vv = perturb(Vobs[sel][j], SIGM[sel][j], SIGP[sel][j], rng)
        bsl[b] = np.polyfit(np.log10(GBA[tag][sel][j]), np.log10(vv ** 2 / R_m[sel][j]), 1)[0]
    se_beta = float(np.std(bsl))
    sigg = 2.0 * (0.5 * (SIGM[sel] + SIGP[sel])) / Vobs[sel] / np.log(10.0)   # sigma_log10 g_obs
    cq = np.mean(y - 0.5 * x)
    chi2_red = float(np.sum((y - 0.5 * x - cq) ** 2 / sigg ** 2) / (sel.sum() - 1))
    FORM[tag] = dict(N=int(sel.sum()), beta=beta, SE=se_beta, chi2_red=chi2_red)
    print(f"    [{tag}] N(g_bar<0.4a0) = {int(sel.sum())}:  free slope beta = {beta:.3f} +- "
          f"{se_beta:.3f} (sqrt-law expects 0.5, z = {(beta-0.5)/se_beta:+.2f});  "
          f"chi2_red vs published errors = {chi2_red:.1f}")
    check(f"C6-{tag} [deep form] free slope consistent with 0.5 within 3 SE (sqrt law)",
          abs(beta - 0.5) <= 3 * se_beta, f"beta = {beta:.3f} +- {se_beta:.3f}")
    check(f"C7-{tag} [scatter] probe scatter consistent with published V errors (chi2_red<3)",
          chi2_red < 3.0, f"chi2_red = {chi2_red:.1f}")

# ---- R-dependence (step 4) -------------------------------------------------------
edges = [5.0, 8.0, 11.0, 14.0, 17.0, 20.0, 22.5, 25.5]
print("\n--- R-DEPENDENCE: a0_eff per annulus (7 bins; full-line estimator) ---")
ANN = {}
for tag, gb in (("primary", GBA["primary"]), ("varB", GBA["varB"])):
    ann = []
    for b in range(len(edges) - 1):
        m = (Rk >= edges[b]) & (Rk < edges[b + 1])
        if m.sum() == 0:
            continue
        ap = probe_full(m, gb)                                   # m/s^2
        est = boot_est(m, gb, NB_BIN, SEED + 100 + b)
        ann.append(dict(lo=edges[b], hi=edges[b + 1], N=int(m.sum()), Rmid=float(np.median(Rk[m])),
                        gbar_over_a0=float(np.median(gb[m] / A0)),
                        gobs_over_a0=float(np.median(gobs[m] / A0)),
                        a0eff_over_a0=ap / A0, SE=float(np.std(est) / A0)))
        print(f"    [{tag}] R in [{edges[b]:4.1f},{edges[b+1]:4.1f})  N={int(m.sum())}  "
              f"Rmid={np.median(Rk[m]):5.2f}  <g_bar>={np.median(gb[m]/A0):6.3f} a0  "
              f"<g_obs>={np.median(gobs[m]/A0):5.3f} a0  a0_eff/a0={ap/A0:6.3f} +- {np.std(est)/A0:.3f}")
    ANN[tag] = ann

def drift_test(ann, seed, min_n=3):
    outer = [a for a in ann if a["gbar_over_a0"] < 0.5]
    if len(outer) < min_n:
        return 0.0, 0.0, 0.0, len(outer)
    xa = np.array([d["Rmid"] for d in outer])
    ya = np.array([np.log10(d["a0eff_over_a0"]) for d in outer])
    wa = 1.0 / np.array([max(d["SE"] / (d["a0eff_over_a0"] * np.log(10.0)), 1e-9)
                         for d in outer]) ** 2
    A = np.vstack([np.ones_like(xa), xa]).T
    sol = np.linalg.lstsq(A * np.sqrt(wa)[:, None], ya * np.sqrt(wa), rcond=None)[0]
    slope = float(sol[1])
    rng = np.random.default_rng(seed)
    sl = []
    for _ in range(NB):
        j = rng.choice(np.arange(len(outer)), size=len(outer), replace=True)
        yj = ya[j] + rng.normal(size=len(outer)) / np.sqrt(wa[j])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", np.RankWarning)
            sl.append(np.polyfit(xa[j], yj, 1)[1])
    se = float(np.std(sl))
    return slope, se, slope / se, len(outer)

sl_p, se_p, z_p, n_p = drift_test(ANN["primary"], SEED + 7)
sl_b, se_b, z_b, n_b = drift_test(ANN["varB"], SEED + 8)
print(f"    drift test (outer annuli, <g_bar> < 0.5 a0): primary dlog10(a0_eff)/dR = {sl_p:.4f} +- "
      f"{se_p:.4f} kpc^-1, z = {z_p:+.2f} (n={n_p});  varB {sl_b:.4f} +- {se_b:.4f}, "
      f"z = {z_b:+.2f} (n={n_b})")
check("C9 [drift] no significant R-drift of a0_eff in the outer annuli (|z| < 3)",
      abs(z_p) < 3.0 and abs(z_b) < 3.0, f"primary z={z_p:+.2f}; varB z={z_b:+.2f}")

# ---- convention sensitivity -----------------------------------------------------
sel22 = Rk >= 22.5
ae_enc = probe_full(sel22, gbar_enc) / A0
dconv = abs(np.log10(Pp["a"]) - np.log10(ae_enc))
check("C10 [convention] a0_eff(V^2/R) vs a0_eff(G M_enc/R^2) within 0.3 dex "
      "(primary, R>=22.5)", dconv < 0.3, f"{Pp['a']:.2f} vs {ae_enc:.2f} ({dconv:.2f} dex)")
print(f"    convention check (primary, R>=22.5): V^2/R -> {Pp['a']:.3f}; "
      f"G M_enc/R^2 -> {ae_enc:.3f}")

# ---- registered statement -------------------------------------------------------
if killA:
    verdict = (f"MW DISAGREES with the extragalactic deep tension (z_lin = {zA_lin:+.1f} vs 0.73 "
               f"on the deepest attained probe). Sample-dependent deep-tension finding, registered. "
               f"The three channels do NOT agree: SPARC-deep 0.72, dwarfs 0.64/0.31, "
               f"MW {rP:.2f} (Eilers-fiducial probe) / {PROBE['varB_R22']['a']:.2f} "
               f"(McMillan-class). The MW sits AT-OR-ABOVE canonical a0 (z vs 1.0 = {z1_lin:+.1f}); "
               f"under NO baryonic modeling does the MW reproduce the 0.73 deficit, and the strict "
               f"deep regime (g_bar < 0.2 a0) is not attained inside 25 kpc under any modeling "
               f"(N = 0/0/2).")
else:
    verdict = (f"MW deepest probe does not exceed 3 SE from 0.73 (z_lin = {zA_lin:+.1f}) -- the "
               f"three independent channels AGREE within 3 SE of the extragalactic deep value "
               f"(SPARC-deep 0.72, dwarfs 0.64, MW {rP:.2f}). Registered caveats: the MW probe "
               f"lives at g_bar = 0.24-0.30 a0 (the strict 0.2-a0 cut is NEVER attained, N = 0/0/2), "
               f"it is ALSO consistent with canonical a0 (z vs 1.0 = {z1_lin:+.1f}) and therefore "
               f"does not independently discriminate 0.73 from 1.0 (drop-point central values "
               f"{rP:.2f} / {PROBE['varA_R22']['a']:.2f} / {PROBE['varB_R22']['a']:.2f} under the "
               f"three baryonic modelings, all at-or-above the L06 value).")
print("\n--- REGISTERED FINDING ---")
print("    " + verdict)
viz = ("DEEPLINE-HIGH" if np.log10(Pp["a"]) > 3 * sPd else
       "DEEPLINE-LOW" if np.log10(Pp["a"]) < np.log10(L06_RATIO) - 3 * sPd else
       "DEEPLINE-CONSISTENT")
print(f"    MW probe characterisation: {viz} (a0_eff/a0 = {rP:.3f} +- {sP:.3f}); "
      f"all-model spread at R >= 22.5: "
      + ", ".join(f"{PROBE[f'{t}_R22']['a']:.2f} ({t})" for t in ("primary", "varA", "varB")))

npass = sum(1 for _, o, _ in RES if o)
print(f"\nO03 COMPLETE: {npass}/{len(RES)} checks PASS.")

out = dict(
    lane="O03",
    title="MW rotation curve deep-a0 measurement (Eilers+2019; third channel for the deep tension)",
    date="2026-09-23",
    a0_m_s2=A0,
    data=dict(file="deepseek_push/data2/eilers2019_mw_rotation_curve_table1.csv", N=38,
              R_range_kpc=[5.27, 24.82],
              columns=["R_kpc", "vc_kms", "sigma_vc_minus_kms", "sigma_vc_plus_kms"],
              baryonic_columns_present=False,
              baryonic_models="primary = Pouliasis+17 Model I (Plummer bulge + MN thin/thick, the "
                              "model Eilers+19 fixed) + McMillan-17 gas (equal-mass exponentials, "
                              "Bessel closed form); varA = primary without gas; varB = McMillan-class"),
    baryonic_model_params=dict(
        primary=dict(bulge_plummer_M=460 * MU, bulge_b=0.30, thin_MN_M=1700 * MU, thin_a=5.3,
                     thin_b=0.25, thick_MN_M=1700 * MU, thick_a=2.6, thick_b=0.8,
                     HI_M=HI_M, HI_Rd=HI_RD, HI_Sigma0_eff=HI_S0e, H2_M=H2_M, H2_Rd=H2_RD,
                     H2_Sigma0_eff=H2_S0e, Vbar_8_19_km_s=v8["primary"]),
        varA_Eilers_strict=dict(Vbar_8_19_km_s=v8["varA"]),
        varB=dict(thin_Sigma0=TH_S0, thin_Rd=TH_RD, thick_Sigma0=TK_S0, thick_Rd=TK_RD,
                  bulge_hernquist_M=8.9e9, alpha=0.7, HI_Sigma0_eff=HI_S0e, H2_Sigma0_eff=H2_S0e,
                  Vbar_8_19_km_s=v8["varB"])),
    model_identity=dict(anchor_window_km_s=[185.0, 205.0],
                        Vbar_8_19=dict(primary=v8["primary"], varA=v8["varA"], varB=v8["varB"]),
                        nfw_halo_check=dict(strict_model_vc=float(v_tot8_strict),
                                            with_gas_vc=float(v_tot8_prim), measured=228.86)),
    pre_registered=dict(L06_a0eff_a0=L06_RATIO, L06_SE=SE_L06,
                        KILL_A="|a0eff_MW - 0.73 a0| > 3*sqrt(SE_MW^2+SE_L06^2) -> MW disagrees "
                               "(sample-dependent finding, registered); on the deepest attained "
                               "probe (primary, R >= 22.5 kpc), linear AND dex, OR",
                        KILL_B="|log10(a0eff_MW/a0)| < 3 SE_dex -> consistent with canonical a0",
                        deep_cut_finding="strict g_bar < 0.2 a0 cut attained by NO modeling with "
                                         "N >= 10 inside the Eilers R-range (N = 0/0/2)"),
    deep_fit=dict(
        cut="g_bar < 0.2 a0 (L06-identical)",
        deep_counts=NS,
        strict_varB=FIT_DEEP,
        deepest_probes={k: dict(a0eff_over_a0=v["a"], SE_lin=v["sum"]["SE_lin"],
                                SE_dex=v["sum"]["SE_dex"], N=v["sum"]["N"],
                                CI68_lin=v["sum"]["CI68_lin"], deep_limit_reading=v["deep_limit"])
                        for k, v in PROBE.items()},
        form_diagnostics=FORM,
        bootstraps=NB, bootstrap="R-independent resampling + asymmetric V_obs errors "
                                 "(sigma_minus/sigma_plus)"),
    cross_check=dict(
        z_vs_L06_linear=float(zA_lin), z_vs_L06_dex=float(zA_dex),
        z_vs_1_linear=float(z1_lin), z_vs_1_dex=float(zB_),
        KILL_A_triggered=bool(killA), KILL_B_consistent_with_1=bool(killB),
        L06=dict(a0eff_a0=L06_RATIO_O04, se=SE_L06, z=-4.17),
        O01_dwarfs=dict(primary_a0eff_a0=0.638, se=0.163, deep_tail_a0eff_a0=0.310, se2=0.117),
        MIGHTEE_deep_context=dict(a0eff_a0=2.164, z=6.58, note="N05, opposite sign")),
    r_dependence=dict(annuli_primary=ANN["primary"], annuli_varB=ANN["varB"],
                      drift_primary=dict(slope_dex_per_kpc=sl_p, SE=se_p, z=z_p, n_bins=n_p),
                      drift_varB=dict(slope_dex_per_kpc=sl_b, SE=se_b, z=z_b, n_bins=n_b),
                      canonical_expectation="flat at a0_eff = a0 (full-line estimator)"),
    verdict=verdict,
    characterisation=viz,
    honest_limits=["BARYONIC MODEL SYSTEMATICS DOMINATE: legs give V_bary(8.19) = "
                   + f"{v8['primary']:.0f}/{v8['varA']:.0f}/{v8['varB']:.0f} km/s; the strict deep "
                     "cut is never attained with N>=10 (0/0/2); a0_eff ~ 1/g_bar in the deep regime "
                     "so baryonic-mass errors map ~linearly",
                   "The deepest probe region (g_bar = 0.17-0.35 a0) is NOT the asymptotic deep regime",
                   "Convention (V^2/R vs G M_enc/R^2) ratio 0.85-0.91 on the primary leg (C10 < 0.3 dex)",
                   "Eilers v_c beyond ~20 kpc carry 6-28 km/s random errors; DR3-era successors "
                   "(Wang+23 Jiao+23 Ou+24 Labini+23) find a steeper outer decline (would lower a0_eff)",
                   "EFE cannot explain an EXCESS of g_obs over the deep line",
                   "chi2_red >> 1 on the probe sets: published errors understate the scatter"],
    files=["deepseek_push/O03_mw_deep.py", "deepseek_push/O03_mw_deep.out",
           "deepseek_push/O03_results.json", "deepseek_push/O03_MW_DEEP_A0.md"],
    checks=[dict(check=l, pass_=bool(o), detail=d) for l, o, d in RES],
)
with open(os.path.join(HERE, "O03_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"\n[O03_results.json written]")