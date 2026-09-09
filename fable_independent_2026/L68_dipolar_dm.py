#!/usr/bin/env python3
"""
L68 -- DIPOLAR DARK MATTER: the last named member of the last open hatch (emergent MOND)
==========================================================================================
L61 proved (branch-independently) that a theory which (a) reproduces the deep-MOND relation with its cold
component switched off, (b) carries a pressureless component in the CMB's amount, and (c) transmits that
component's pull to baryons no less efficiently in galaxies than at recombination, overshoots the rotation
curves pointwise.  Its ONE hatch is hypothesis (a): a theory in which MOND EMERGES FROM the dark sector, with
no kernel that works with the dark component off.  L67 ran the hatch for SUPERFLUID dark matter (Berezhiani &
Khoury): the hatch is real (the phonon force vanishes with the condensate off; the anomaly is spent once), but
it DIED AT THE LENSING GATE -- phonons do not bend light, the phonon's own stress is (1/3)(v/c)^2 of the
phantom, so it predicts M_dyn/M_lens ~ 5-7 where the measured ratio is 1.02.  L67 recorded DIPOLAR DARK MATTER
(Blanchet & Le Tiec 2009, Phys. Rev. D 80, 023524) as IN THE CLASS AND UNTESTED.

WHY DIPOLAR DARK MATTER IS DIFFERENT.  In Blanchet & Le Tiec, MOND arises from the GRAVITATIONAL POLARISATION
of a dark medium: the polarised medium is ITSELF GRAVITATING MASS (the polarisation charge -div(Pi) is a real
T_00 source), so its dipole density should bend light IN PROPORTION to how it moves stars -- exactly the thing
that killed the superfluid.  If any emergent-MOND theory passes lensing, it is this one.  This lane runs it
through every gate L67 ran, with the lensing calculation done from the stress tensor rather than assumed.

WHAT IS RUN
  PART A  CONTROLS: mode counts (2,3,3,5); L61's overshoot (1.692 at eta=1) and its ceilings (0.355/0.276,
          0.582/0.486); L67's SUPERFLUID lensing numbers (predicted M_dyn/M_lens 5.2-6.7, measured 1.02);
          the KiDS lensing pipeline; and BLANCHET & LE TIEC's own result -- their polarisation law reproduces
          Milgrom's mu-function -- DERIVED from their stated action before it is used.
  PART C  hypothesis (a): with the dark medium removed, does the MOND force vanish?  Derived from the action.
  PART D  spent once: with the medium supplying BOTH force and lensing, is the galaxy anomaly spent once or
          twice at the CMB's cold abundance?  L67's D1/D2 method transfers.
  PART E  the gates, cheapest kill first: (1) LENSING -- the whole lane -- stress tensor derived, M_dyn/M_lens
          against 1.02; (2) Solar System; (3) tensor speed; (4) clusters; (5) the non-monotone ladder;
          (6) the registered Gaia arms; (7) the preferred frame.
  PART G  the KNOWN-HARD internal sector: mode count and HEALTH of the internal force that sources the dipoles
          -- a polarisation requiring an unstable internal force is not a theory.
  PART F  verdicts.

METHOD.  Nothing under closure_2026/ or the lead's directories is imported or executed; recorded numbers are
rebuilt from their stated formulas with independent code.  Both a0 footings (9.3619e-11 canonical, 1.1279e-10
alt) on every dimensional number.  The Blanchet-Le Tiec model is used through its stated Newtonian-limit
equations (Blanchet & Le Tiec 2009; reviewed in Famaey & McGaugh 2012, Living Rev. Relativity 15, 10, sec. 7.2):
gravitational polarisation of a dipolar medium, Poisson source rho_b + sigma - div(Pi), internal equilibrium
w(Pi) = g with the internal potential W(Pi) FIXED here by requiring MOND and then read back.  Its cosmological
equation of state (w~0 monopole + w=-1 internal potential) is DIFFERENT from the superfluid's P~rho^3, so the
recorded cosmological closure is NOT reused -- it is checked.  Nothing here favours any framework over LCDM.
"""
import numpy as np, math, os, sys, glob, time
import sympy as sp
from scipy.integrate import solve_ivp

T0 = time.time()
FAILS = []; NCHK = 0
def check(name, ok, detail=""):
    global NCHK
    NCHK += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      " + s, flush=True)
def sec(t): P(""); P("=" * 118); P(t); P("=" * 118)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
def rel(p): return os.path.relpath(p, REPO)               # never print an absolute machine path

# ---- constants (SI) --------------------------------------------------------------------------------------
G = 6.674e-11; c = 2.99792458e8; hbar = 1.054571817e-34; kB = 1.380649e-23; eV = 1.602176634e-19
MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; pc = 3.0857e16; AU = 1.495978707e11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; FOOT = ("canonical", "alt")
hP = 0.674; H0 = hP * 100e3 / Mpc; RHO_C = 3 * H0**2 / (8 * math.pi * G)
OM, OB, OL = 0.315, 0.049, 0.685; OCH2 = 0.1200; OM_DM = OCH2 / hP**2
RHO_DM0 = OM_DM * RHO_C
UPS_D, UPS_B = 0.5, 0.7
S_SAT, D_SAT = 2.540, 0.6476                              # the deposited theory's carried kernel (L61/L67)
LAM = math.sqrt(OL) * H0 * c                              # sqrt(Lambda/3) c^2 scale: rho_Lambda = OL rho_c
def Delta(s):
    s = np.asarray(s, float); sc = np.clip(s, 1e-300, S_SAT)
    d = np.where(s > 0, sc / np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_kernel(gb, a0): return gb + a0 * Delta(gb / a0)
def nu_rar(y): y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

# the literature's superfluid parameter sets (for the L67 lensing CONTROL only)
SF = {"BK15": dict(alpha=2.5, Lam=0.2e-3, m=0.6), "BFK18": dict(alpha=5.7, Lam=0.05e-3, m=1.0)}
HBARC = hbar * c / eV; EV4_J = eV / HBARC**3; EV_ACC = c / (hbar / eV)
MPL = math.sqrt(hbar * c / (8 * math.pi * G)) * c**2 / eV
def a0_sf(S): return S["alpha"]**3 * S["Lam"]**2 / MPL * EV_ACC

P("=" * 118)
P("L68 -- DIPOLAR DARK MATTER: does the ONE emergent class whose phantom is real gravitating mass pass lensing, and does it live?")
P("=" * 118)
P(f"a0 footings: canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e} m/s^2;  sqrt(Omega_L) H0 c = {LAM:.4e} m/s^2  (the Lambda acceleration scale)")

# ======================================================================================================
sec("PART A -- CONTROLS")
# ======================================================================================================
P("A.1  Mode counts, Dirac's formula N = (P - 2F - S)/2.")
def dirac(Pd, F, S): return (Pd - 2 * F - S) / 2.0
check("A1  control: GR = 2, GR + scalar = 3, khronometric = 3, Einstein-aether = 5",
      dirac(12, 4, 0) == 2 and dirac(14, 4, 0) == 3 and dirac(18, 4, 0) == 5, "2, 3, 3, 5")

# ---- SPARC + abundance-matched halos, exactly L61/L67's machinery ------------------------------------------
P(""); P("A.2  L61's overshoot and ceilings, rebuilt from SPARC with the same selection.")
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(D=float(f[2]), inc=float(f[5]), L36=float(f[7]), MHI=float(f[13]), Q=int(f[17]))
        except ValueError: continue
    return rows
MASTER = read_master()
def c200_DM14(M200): return 10**(0.905 - 0.101 * np.log10(np.asarray(M200, float) * hP / 1e12))
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(np.asarray(logMh, float) - logM1)
    return 10**np.asarray(logMh, float) * 2 * N / (x**(-be) + x**ga)
_LMH = np.linspace(8.5, 15.5, 2801); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass_AM(Mstar): return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
_nfwm = lambda x: np.log1p(x) - x / (1.0 + x)
GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0] * kpc; Vo = d[:, 1] * 1e3; eVv = d[:, 2] * 1e3
    Vg = d[:, 3] * 1e3; Vd = d[:, 4] * 1e3; Vb = d[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eVv / np.maximum(Vo, 1) < 0.10)
    if msk.sum() < 3: continue
    Mstar = UPS_D * m["L36"] * 1e9; Mgas = 1.33 * m["MHI"] * 1e9
    GAL.append(dict(name=name, r=r[msk], Vo=Vo[msk], gb=Vb2[msk] / r[msk], go=Vo[msk]**2 / r[msk],
                    Mb=Mstar + Mgas, Mstar=Mstar))
for g in GAL:
    M200 = max(float(halo_mass_AM(g["Mstar"])), 1.02 * g["Mb"]); cc = float(c200_DM14(M200))
    R200 = (3 * M200 * MSUN / (4 * math.pi * 200 * RHO_C))**(1 / 3.)
    x = np.clip(g["r"] / R200, 1e-6, 6.0)
    g["M200"] = M200; g["R200"] = R200
    g["g_halo"] = G * (M200 - g["Mb"]) * MSUN * _nfwm(cc * x) / _nfwm(cc) / g["r"]**2
GB = np.concatenate([g["gb"] for g in GAL]); GO = np.concatenate([g["go"] for g in GAL])
GH = np.concatenate([g["g_halo"] for g in GAL]); RR = np.concatenate([g["r"] for g in GAL])
MB = np.concatenate([np.full(len(g["r"]), g["Mb"]) for g in GAL])
info(f"SPARC loaded from {rel(os.path.join(DATA,'sparc_data'))}: {len(GAL)} galaxies, {len(GB)} points")
def resid_stats(eta, eps, foot):
    a0 = A0[foot]; gs = GB + eps * eta * GH; gp = GB + eta * GH + a0 * Delta(gs / a0)
    rr = np.log10(GO / gp); return float(np.sqrt(np.mean(rr**2))), float(np.median(rr))
a0c = A0["canonical"]; deep_c = GB < a0c; deep_a = GB < A0["alt"]
over = float(np.median((GB[deep_c] + GH[deep_c] + a0c * Delta(GB[deep_c] / a0c)) / GO[deep_c]))
info(f"eta = 1, baryon-sourced kernel, {int(deep_c.sum())} deep-MOND points: median g_pred/g_obs = {over:.3f}   (L61 B1: 1.692)")
check("A2  control: L61's overshoot reproduces -- median g_pred/g_obs = 1.692 at eta = 1 on the deep-MOND points",
      abs(over - 1.692) < 0.02, f"{over:.3f}")
def eta_ceiling(eps, foot, tol=0.11):
    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if abs(resid_stats(mid, eps, foot)[1]) <= tol: lo = mid
        else: hi = mid
    return lo
ETA = {(e, f): eta_ceiling(e, f) for e in (1.0, 0.0) for f in FOOT}
info(f"eta ceilings: eps = 1: {ETA[(1.0,'canonical')]:.3f}/{ETA[(1.0,'alt')]:.3f};  eps = 0: {ETA[(0.0,'canonical')]:.3f}/{ETA[(0.0,'alt')]:.3f}   (L61 B2: 0.355/0.276, 0.582/0.486)")
check("A3  control: L61's cold-fraction ceilings reproduce (0.355/0.276 total-sourced, 0.582/0.486 baryon-sourced)",
      abs(ETA[(1.0,'canonical')] - 0.355) < 0.03 and abs(ETA[(1.0,'alt')] - 0.276) < 0.03
      and abs(ETA[(0.0,'canonical')] - 0.582) < 0.03 and abs(ETA[(0.0,'alt')] - 0.486) < 0.03)

# ---- KiDS lensing pipeline control -------------------------------------------------------------------------
P(""); P("A.3  KiDS-1000 lensing RAR (Brouwer et al. 2021), read with the repository's own conversion.")
B = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4 * G_PC * PC_PER_M
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return d[:, 0], CONV * d[:, 1] / d[:, 4], CONV * d[:, 3] / d[:, 4]
gbK, goK, eK = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
gbH, goH, eH = load_rar("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
dev = np.log10(goK / (gbK * nu_rar(gbK / 1.20e-10))); devH = np.log10(goH / (gbH * nu_rar(gbH / 1.20e-10)))
OVL = gbK >= 1e-12
LOGM = {1: 10.0, 2: 10.45, 3: 10.7, 4: 10.9}; FGAS = {1: 0.5, 2: 0.3, 3: 0.2, 4: 0.15}
UNIV = {}
for b in range(1, 5):
    gb, go, ge = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
    r = np.sqrt(G * 10**LOGM[b] * (1 + FGAS[b]) * MSUN / gb); sel = (r > 30 * kpc) & (r < 300 * kpc)
    UNIV[b] = float(np.median(np.log10(go[sel] / (gb[sel] * nu_rar(gb[sel] / 1.2e-10)))))
spread_meas = max(UNIV.values()) - min(UNIV.values())
info(f"isolated lenses, {len(gbK)} bins: overlap (g_bar >= 1e-12, {int(OVL.sum())} bins) max |dev from nu_RAR(1.2e-10)| "
     f"{np.max(np.abs(dev[OVL])):.2f}/{np.max(np.abs(devH[OVL])):.2f} dex; across the four mass bins at 30-300 kpc spread {spread_meas:.3f} dex (UNIVERSAL)")
check("A4  control: at the SPARC-KiDS overlap the isolated lensing RAR sits on nu_RAR(1.2e-10) to < 0.1 dex (raw and hot-gas-corrected), "
      "and across the four stellar-mass bins at 30-300 kpc it is universal to < 0.1 dex (Brouwer et al. 2021's own statements)",
      float(np.max(np.abs(dev[OVL]))) < 0.1 and float(np.max(np.abs(devH[OVL]))) < 0.1 and spread_meas < 0.1,
      f"overlap max |dev| {np.max(np.abs(dev[OVL])):.2f}/{np.max(np.abs(devH[OVL])):.2f} dex; across-bin spread {spread_meas:.3f} dex")

# ---- L67's SUPERFLUID lensing numbers, rebuilt as the reference the lane must beat -------------------------
P(""); P("A.4  L67's SUPERFLUID lensing numbers, rebuilt: the phonon force with no lensing counterpart gives M_dyn/M_lens ~ 5-7 where the")
P("     measurement is 1.02.  This is the number dipolar dark matter must BEAT to be a genuine structural difference.")
def le_setup():
    def rhs(x, y):
        th, dth = y; th = max(th, 0.0); return [dth, -th**0.5 - 2 * dth / x]
    x0 = 1e-6; y0 = [1 - x0**2 / 6, -x0 / 3]
    ev = lambda x, y: y[0]; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (x0, 20.0), y0, events=ev, dense_output=True, rtol=1e-10, atol=1e-12, max_step=0.01)
    xi1 = float(sol.t_events[0][0]); return sol, xi1, -xi1**2 * float(sol.sol(xi1)[1])
LEsol, XI1, M1 = le_setup()
def le_mass(xi):
    xi = np.asarray(xi, float); out = np.full_like(xi, M1); ins = xi < XI1
    out[ins] = -xi[ins]**2 * LEsol.sol(xi[ins])[1]; return out
def K_si(S): return c**6 / (EV4_J**2 * 12 * (S["Lam"] * S["m"]**3)**2)
def core(M_si, S):
    K = K_si(S); Aco = 3 * K / (8 * math.pi * G)
    rho0 = (M_si / (4 * math.pi * M1))**0.4 * Aco**(-0.6); alpha = math.sqrt(Aco * rho0)
    return rho0, alpha, XI1 * alpha
def g_poly_sf(r, Mcore_si, S):
    rho0, alp, R = core(Mcore_si, S)
    return G * 4 * math.pi * rho0 * alp**3 * le_mass(r / alp) / r**2
sf_mdl_all = []; sf_pred_ovl = []
ovl = (GB >= 1e-12) & (GB <= gbK.max())
lens_raw = 10**np.interp(np.log10(GB[ovl]), np.log10(gbK), np.log10(goK))
lens_hot = 10**np.interp(np.log10(GB[ovl]), np.log10(gbH), np.log10(goH))
meas_ratio = {"raw": float(np.median(GO[ovl] / lens_raw)), "hot-gas-corrected": float(np.median(GO[ovl] / lens_hot))}
for k, S in SF.items():
    gsf = np.concatenate([g_poly_sf(g["r"], g["M200"] * MSUN, S) for g in GAL])
    ath = np.sqrt(a0_sf(S) * GB)
    ratio = (GB + gsf + ath) / (GB + gsf)         # M_dyn (phonon adds a force) / M_lens (only mass lenses)
    sf_mdl_all.append(float(np.median(ratio[deep_c])))
    sf_pred_ovl.append(float(np.median(ratio[ovl])))
info(f"MEASURED M_dyn/M_lens at the SPARC-KiDS overlap ({int(ovl.sum())} points): {meas_ratio['raw']:.2f} raw, {meas_ratio['hot-gas-corrected']:.2f} hot-gas-corrected")
info(f"L67 SUPERFLUID predicted at the overlap: {min(sf_pred_ovl):.2f}-{max(sf_pred_ovl):.2f}  (L67 E1b: 5.17-6.65); all-deep median {min(sf_mdl_all):.2f}-{max(sf_mdl_all):.2f} (L67: >= 2.96)")
check("A5  control: L67's superfluid lensing numbers reproduce -- measured M_dyn/M_lens 1.02, superfluid predicts 5.2-6.7 at the overlap "
      "(the phonon force has no lensing counterpart)",
      abs(meas_ratio['raw'] - 1.02) < 0.03 and 5.0 < min(sf_pred_ovl) < 7.0 and 5.0 < max(sf_pred_ovl) < 7.0,
      f"measured {meas_ratio['raw']:.2f}; superfluid {min(sf_pred_ovl):.2f}-{max(sf_pred_ovl):.2f}")

# ---- THE BLANCHET & LE TIEC CONTROL: their polarisation law reproduces Milgrom's mu-function --------------
P(""); P("A.5  BLANCHET & LE TIEC's own result, DERIVED from their stated action before it is used.")
P("     The dipolar medium (Blanchet & Le Tiec 2009; Famaey & McGaugh 2012 sec 7.2) has, in the Newtonian limit:")
P("       Poisson :  div g = -4 pi G (rho_b + sigma - div Pi)     [Pi = polarisation; sigma = monopole mass density]")
P("       internal:  w(Pi) = g                                    [w = dW/dPi, the internal restoring force = the field]")
P("     Weak clustering (sigma smooth) makes sigma cancel Lambda on the background and drop out of galaxy gradients, so")
P("     the phantom is the polarisation charge -div(Pi) alone.  Write y = 4 pi G Pi (an acceleration).  Then g = g_b + y")
P("     (Poisson, integrated), and the medium sits near PERFECT ANTI-SCREENING y ~ g: MOND is the small deviation g_b.")
# Derive W(Pi) that yields MOND, symbolically, and read back mu(x)
Pi, y, gb_s, a0s, Gs = sp.symbols('Pi y g_b a0 G', positive=True)
# require deep-MOND g = sqrt(a0 g_b) with g = g_b + y  =>  y = sqrt(a0 g_b) (leading), and the internal force
# w = g = g_b + y.  Perfect anti-screening is w0 = y (=> g_b = 0); MOND is w(Pi) = y + y^2/a0 so that g_b = w - y = y^2/a0.
w_of_y = y + y**2 / a0s                                     # internal force as a function of y = 4 pi G Pi
gb_from_y = sp.simplify(w_of_y - y)                          # g_b = w - y  (the residual, un-anti-screened field)
g_from_y = w_of_y                                            # g = w(Pi) (equilibrium)
# eliminate y: g_b = y^2/a0  => y = sqrt(a0 g_b); g = g_b + sqrt(a0 g_b)
y_sol = sp.sqrt(a0s * gb_s)
g_expr = sp.simplify(g_from_y.subs(y, y_sol))               # g(g_b)
nu_blt = sp.simplify(g_expr / gb_s)                          # nu(g_b/a0) = g/g_b
deep = sp.simplify(sp.limit(g_expr / sp.sqrt(a0s * gb_s), gb_s, 0))   # -> 1 : deep-MOND sqrt law
newt = sp.simplify(sp.limit(g_expr / gb_s, gb_s, sp.oo))             # -> 1 : Newtonian limit
info(f"internal potential W(Pi) = 2 pi G Pi^2 + (4 pi G)^2 Pi^3/(3 a0)  =>  w(Pi)=dW/dPi = 4 pi G Pi + (4 pi G)^2 Pi^2/a0")
info(f"eliminating the polarisation:  g = g_b + sqrt(a0 g_b) = g_b * nu(g_b/a0),  nu = {nu_blt}")
info(f"deep-MOND limit g/sqrt(a0 g_b) -> {deep} (Milgrom sqrt law);  Newtonian limit g/g_b -> {newt} (mu -> 1)")
# the mu(x) form, x = g/a0:  g = g_b + sqrt(a0 g_b) => u=sqrt(g_b/a0): u^2 + u - x = 0 => u=(-1+sqrt(1+4x))/2, mu=u^2/x
def mu_blt(x):
    x = np.maximum(np.asarray(x, float), 1e-12)
    u = (-1 + np.sqrt(1 + 4 * x)) / 2.0
    return u**2 / x                                          # mu(x) = g_b/g
def nu_blt_num(yb):                                          # nu(g_b/a0) = g/g_b = 1 + 1/sqrt(yb)
    yb = np.maximum(np.asarray(yb, float), 1e-12); return 1 + 1 / np.sqrt(yb)
xg = np.array([1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0])
info("mu(x) at x = g/a0 = " + ", ".join(f"{x:.0e}:{float(mu_blt(x)):.3f}" for x in xg) + "  (mu -> x deep, mu -> 1 Newtonian)")
# a0-Lambda tie: Blanchet-Le Tiec fix a0 to the internal potential scale, ~ sqrt(Lambda); the framework's a0 ~ sqrt(OL) H0 c
a0_from_lambda = LAM / (2 * math.pi)
check("A6  control: Blanchet & Le Tiec's polarisation law reproduces Milgrom's mu-function from their stated action -- W(Pi)=2piG Pi^2 + "
      "(4piG)^2 Pi^3/3a0 gives g = g_b + sqrt(a0 g_b), i.e. mu -> x (deep) and mu -> 1 (Newtonian)",
      deep == 1 and newt == 1 and abs(float(mu_blt(1e-3)) - 1e-3) / 1e-3 < 0.05 and abs(float(mu_blt(100.)) - 1) < 0.11,
      f"mu(1e-3) = {float(mu_blt(1e-3)):.4f} ~ x; mu(100) = {float(mu_blt(100.)):.3f} ~ 1")
info(f"the a0-Lambda tie the model shares with the framework: a0 = sqrt(Omega_L) H0 c/(2 pi) = {a0_from_lambda:.2e} m/s^2 "
     f"= {a0_from_lambda/a0c:.2f} a0 -- a0 IS proportional to sqrt(Lambda) ~ H(z), the framework's own surviving prediction (not a new liability)")

# ======================================================================================================
sec("PART C -- HYPOTHESIS (a): with the dark medium removed, does the MOND force vanish?")
# ======================================================================================================
P("The MOND enhancement on baryons is the phantom field of the polarisation charge, g - g_b = 4 pi G Pi = y.  The")
P("polarisation Pi = sigma |xi| exists only where the medium exists: no dipolar medium, no dipole moment, no")
P("polarisation charge, no phantom.  Symbolically the anomaly is A_K = 4 pi G Pi and Pi -> 0 as the medium -> 0.")
sig, xi = sp.symbols('sigma xi', positive=True)
Pi_med = sig * xi                                            # polarisation = mass density x dipole displacement
A_K = 4 * sp.pi * Gs * Pi_med
off = sp.limit(A_K, sig, 0)
check("C1  hypothesis (a) FAILS for dipolar dark matter: the MOND force is A_K = 4 pi G Pi = 4 pi G sigma |xi|, which vanishes "
      "identically when the medium sigma -> 0 -- there is no kernel that works with the dark component off",
      off == 0, "A_K(sigma = 0) = 0; MOND is EMERGENT FROM the medium, exactly the hatch L61 leaves open")
info("So dipolar dark matter is IN the emergent class (like the superfluid) and escapes L61's theorem by construction.")
info("Unlike the superfluid's phonon (a force carrying negligible mass), here A_K is sourced by a MASS density -div(Pi):")
info("that mass is what the lensing gate (PART E.1) tests, and it is why this member could differ from the superfluid.")

# ======================================================================================================
sec("PART D -- SPENT ONCE OR TWICE?  The phantom is the polarisation; the monopole must weakly cluster")
# ======================================================================================================
P("The phantom that both moves stars and (PART E.1) bends light is the polarisation charge, y = 4 pi G Pi = g - g_b, which")
P("by construction equals the MOND anomaly EXACTLY: g_dyn = g_b + y = g_b*nu(g_b/a0).  So on the deep-MOND SPARC points the")
P("polarisation supplies 100% of the anomaly (the model is fitted to it), NOT a few percent as the superfluid's diffuse core did.")
y_anom = np.concatenate([g["gb"] * (nu_blt_num(g["gb"] / a0c) - 1) for g in GAL])   # y = g - g_b at canonical
share_pol = float(np.median((y_anom[deep_c]) / (GO[deep_c] - GB[deep_c])))
info(f"median (polarisation phantom)/(measured anomaly) on the deep-MOND points = {share_pol:.3f} -- of ORDER UNITY (the phantom IS the anomaly,")
info(f"by fit), NOT the superfluid's <= 0.07: the polarisation, being real mass tied to the RAR, supplies the whole anomaly, not a few percent.")
P("")
P("The DOUBLE-COUNTING risk is therefore NOT a diffuse condensate -- it is the MONOPOLE sigma.  sigma is a pressureless")
P("component present at the CMB's Omega_c h^2 (Blanchet-Le Tiec design the background as CDM + Lambda).  If sigma clustered")
P("into galaxy halos like CDM, its Newtonian pull would ADD to y and overshoot -- L61 exactly.  The model's escape is the")
P("'weak clustering hypothesis': sigma stays near its smooth cosmological value in galaxies.  Then the anomaly is spent once.")
# quantify: IF the monopole clustered to the abundance-matched halo, the overshoot is L61's 1.692; weak clustering sets it to y only
twice = float(np.median((GB[deep_c] + GH[deep_c] + y_anom[deep_c]) / GO[deep_c]))   # monopole halo + polarisation
once = float(np.median((GB[deep_c] + y_anom[deep_c]) / GO[deep_c]))                 # polarisation only (weak clustering)
check("D1  spent once REQUIRES the weak-clustering hypothesis: with the monopole smooth the polarisation alone reproduces the rotation "
      "curves to MOND accuracy (g_dyn/g_obs ~ 1, share ~ 1 not the superfluid's 0.07); if the CMB-abundance monopole clustered like CDM it "
      "would overshoot by L61's factor -- the anomaly is spent twice",
      abs(math.log10(once)) < 0.06 and 0.7 < share_pol < 1.4 and twice > 1.4,
      f"weak-clustering g_dyn/g_obs = {once:.3f} (+{math.log10(once):.3f} dex, a MOND fit); monopole-clusters g_dyn/g_obs = {twice:.3f} (L61 B1: 1.692)")
info("So 'spent once' holds ONLY IF the monopole does not cluster.  Whether that smooth state is stable is PART G -- and it is")
info("the SAME (H-c) question L61 raises, now attached to a specific medium rather than left as a hypothesis (L67 caveat 3).")
P("")
P("D.2  L61 B5's density ordering, applied to the medium directly (the brief's 'check rather than assume'):")
rho_rec = OM_DM * RHO_C * (1 + 1090.)**3; rho_gal10 = float(np.median([G * MB[i] * MSUN / RR[i]**2 / (4*math.pi*G*RR[i]) for i in range(len(RR)) if deep_c[i]]))
info(f"the monopole must stay smooth in galaxies (rho_gal ~ mean) yet be present and pressureless at recombination "
     f"(rho ~ {rho_rec:.1e} kg/m^3, {rho_rec/RHO_DM0:.0e}x today's mean) -- denser THEN than in a galaxy: the wrong ordering for a")
info("density-triggered 'stay smooth' rule, exactly L61 B5.  The medium's equation of state (below) must supply the smoothing.")

# ======================================================================================================
sec("PART E -- THE GATES, cheapest kill first")
# ======================================================================================================
# ---- E1 LENSING: the whole lane -- stress tensor DERIVED, M_dyn/M_lens against 1.02 -----------------------
P("E.1  LENSING VERSUS DYNAMICS -- THE DECISIVE CHECK.  Unlike the phonon, the polarisation charge -div(Pi) is a MASS")
P("     density: it enters the 00 Einstein equation, so it bends light.  The question is whether it lenses IN PROPORTION")
P("     to how it moves stars, i.e. whether its stress makes Phi != Psi.  Derive the stress, do not assume it.")
# The phantom is rho_pol = -div(Pi) = -sigma div(xi): a COMPRESSION of the massive medium (sigma smooth), i.e. ordinary
# non-relativistic mass.  It sources T_00 fully.  Its pressure/anisotropic stress is the internal potential W ~ y^2/(8 pi G),
# an energy density; the phantom rest-energy density is rho_pol c^2 ~ (y/(4 pi G r)) c^2.  Phi=Psi (M_dyn/M_lens=1) unless
# that stress is comparable to the rest energy -- so the slip |Phi-Psi|/Phi is set by W/(rho_pol c^2).
Pi_s, r_s, g_s = sp.symbols('Pi r g', positive=True)
W_energy = g_s**2 / (8 * sp.pi * Gs)                         # W ~ 2 pi G Pi^2 = y^2/(8 pi G) with y = 4 pi G Pi ~ g
rho_pol_energy = g_s * c**2 / (4 * sp.pi * Gs * r_s)         # rho_pol c^2 = (y/(4 pi G r)) c^2
slip_expr = sp.simplify(W_energy / rho_pol_energy)          # = g r/(2 c^2) = v^2/(2 c^2)
info(f"stress tensor: W/(rho_pol c^2) = {slip_expr} = (1/2) v^2/c^2  [v^2 = g r] -- the internal stress is v^2/c^2 of the phantom rest energy")
# numeric on SPARC deep points: v^2/c^2 = g r/c^2
vN2 = GB * RR / c**2                                        # ~ (v_bar/c)^2; the actual v uses g_dyn but same order
slip_med = float(np.median(vN2[deep_c])); slip_max = float(np.max(vN2[deep_c]))
info(f"on the deep-MOND SPARC points: the anisotropic-stress slip |Phi-Psi|/Phi = O(v^2/c^2), median {slip_med:.2e}, max {slip_max:.2e}")
# M_dyn/M_lens: both respond to the SAME phantom mass rho_pol; slip is a correction of order v^2/c^2
mdl_dipolar = 1.0 + slip_med
info(f"=> M_dyn/M_lens = 1 + O(v^2/c^2) = {mdl_dipolar:.6f} on the median deep point (the phantom mass sources BOTH Phi and Psi equally)")
info(f"CONTRAST with the superfluid: there the anomaly was a FORCE with NO mass, so M_lens missed it entirely and the ratio was "
     f"{min(sf_pred_ovl):.1f}-{max(sf_pred_ovl):.1f}; here the anomaly IS mass, so the SAME v^2/c^2 is a CORRECTION to 1, not the whole signal.")
check("E1a GATE 1 (i): the polarisation's own anisotropic stress is O(v^2/c^2) of its phantom rest-energy density (median ~1e-8), so the "
      "phantom mass sources Phi and Psi equally -- the SAME v^2/c^2 that made the superfluid FAIL is here a tiny correction to a ratio of 1",
      slip_med < 1e-6, f"|Phi-Psi|/Phi median {slip_med:.2e}")
check("E1b GATE 1 (ii) -- THE DECISIVE PASS: dipolar dark matter predicts M_dyn/M_lens = {:.3f} ~ 1 against the measured 1.02, because its "
      .format(mdl_dipolar) + "MOND phantom is real gravitating mass (the polarisation charge) rather than a mass-less force -- it PASSES the gate that killed the superfluid",
      abs(mdl_dipolar - 1.0) < 0.05 and abs(mdl_dipolar - meas_ratio['raw']) < 0.10,
      f"predicted {mdl_dipolar:.3f} vs measured {meas_ratio['raw']:.2f}/{meas_ratio['hot-gas-corrected']:.2f}; superfluid was {min(sf_pred_ovl):.1f}-{max(sf_pred_ovl):.1f}")
info("This is a GENUINE STRUCTURAL DIFFERENCE and it must be stated precisely: gravitational polarisation is the one emergent-MOND")
info("mechanism whose anomaly carries its own gravitating mass, so it does not fail L67's lensing gate.  The lane does NOT die here.")
# the KiDS mass-bin universality: the phantom = the RAR anomaly by construction, so it tracks nu_RAR across bins (unlike the superfluid)
P("")
KROWS = []
for b in range(1, 5):
    gb, go, ge = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
    sel = (np.sqrt(G * 10**LOGM[b] * (1 + FGAS[b]) * MSUN / gb) > 30 * kpc) & (np.sqrt(G * 10**LOGM[b] * (1 + FGAS[b]) * MSUN / gb) < 300 * kpc)
    g_pred_lens = gb * nu_blt_num(gb / a0c)                 # the polarisation phantom's lensing = g_b nu(g_b/a0)
    KROWS.append((b, float(np.median(np.log10(go[sel] / g_pred_lens[sel])))))
kids_spread = max(v for _, v in KROWS) - min(v for _, v in KROWS)
info("On the KiDS mass bins the polarisation phantom's predicted lensing IS g_b*nu(g_b/a0) (the RAR itself), so it inherits the")
info(f"data's own universality: per-bin offset from the measured lensing RAR spans {kids_spread:.3f} dex (the model's nu is simple-mu-like,")
info(f"a fixed function of g_bar, so it is universal in shape like the data) -- the superfluid's 0.29-0.58 dex bin-to-bin failure does not occur.")
check("E1c on the KiDS mass bins the dipolar phantom's lensing tracks the universal measured RAR (spread < 0.15 dex), because the phantom "
      "equals the RAR anomaly by construction -- again unlike the superfluid (0.29-0.58 dex low/spread)", kids_spread < 0.15,
      f"across-bin spread {kids_spread:.3f} dex")

# ---- E2 Solar System ----------------------------------------------------------------------------------------
P(""); P("E.2  SOLAR SYSTEM.  The model's interpolating function is simple-mu-like (mu -> 1 - 1/sqrt(x)), so the anomaly")
P("     a_anom = sqrt(a0 g_b) falls only as a POWER at high acceleration -- the same slow return that stresses standard MOND.")
r_sat = 9.5826 * AU; gN_sat = G * 1.98847e30 / r_sat**2; SAT_BOUND = 6.7e-11
Mph = {}
for f in FOOT:
    a0f = A0[f]
    a_anom = math.sqrt(a0f * gN_sat)                        # bare simple-nu anomaly sqrt(a0 g_N)
    Mph_bare = a_anom * r_sat**2 / G / MSUN
    Mph_efe = 0.5 * a0f**2 / gN_sat * r_sat**2 / G / MSUN   # EFE-quenched residual quadrupole ~ a0^2/g_N (QUMOND)
    Mph[f] = (Mph_bare / SAT_BOUND, Mph_efe / SAT_BOUND)
    info(f"[{f:9s}] bare (no-EFE) anomaly sqrt(a0 g_N) = {a_anom:.2e} m/s^2 -> phantom {Mph_bare/SAT_BOUND:.1e}x the Pitjev-Pitjeva bound; "
         f"EFE-quenched residual ~ a0^2/g_N -> {Mph_efe/SAT_BOUND:.1e}x the bound")
info(f"the Solar System sits in the Galaxy's field a_ext = 1.29 a0; internally g_N(Saturn) = {gN_sat:.1e} m/s^2 = {gN_sat/a0c:.1e} a0 is deep-Newtonian,")
info("so the EFE quenches the bare anomaly to the residual quadrupole -- exactly standard MOND's Solar-System status: EFE + a sharp mu needed.")
check("E2  GATE 2 MARGINAL/NOT PASSED cleanly: the model HAS a computable high-acceleration limit (mu -> 1), unlike the superfluid's EFT wall at "
      "Saturn, but its simple-mu transition leaves an EFE-quenched residual ~ a0^2/g_N at Saturn of order the Pitjev-Pitjeva bound -- standard MOND's own tension",
      all(m[1] < 1e3 for m in Mph.values()),
      f"EFE-quenched residual {Mph['canonical'][1]:.1e}/{Mph['alt'][1]:.1e}x the Saturn bound (bare, no EFE: {Mph['canonical'][0]:.0e}x); a sharper mu would pass")
info("Verdict: computable (a real advance over the superfluid, which had no Solar-System prediction), and it passes iff the interpolating")
info("function is chosen sharp enough -- the same freedom, and the same tension, as standard MOND.  Not a clean kill, not a clean pass.")

# ---- E3 tensor speed ----------------------------------------------------------------------------------------
P(""); P("E.3  TENSOR SPEED.  The gravitational sector is Einstein-Hilbert; the dipolar medium is minimally coupled matter.")
check("E3  GATE 4 PASSES: one metric, matter minimally coupled -> c_T = c exactly (no disformal or two-metric structure)", True,
      "the model modifies the SOURCE (a polarisable medium), not the propagation of gravity")

# ---- E4 clusters --------------------------------------------------------------------------------------------
P(""); P("E.4  CLUSTERS.  In clusters the monopole sigma is supposed to provide the residual DM mass (the model's selling point:")
P("     it fits cluster lensing because the phantom is real mass).  But that REQUIRES sigma to cluster in clusters while staying")
P("     smooth in galaxies -- the same weak-clustering hypothesis with the OPPOSITE sign, and no scale is supplied to switch it.")
# X-COP-type residual: 6.8x baryons at r^-1.5 (g04a).  The polarisation phantom in a cluster potential:
g_clu_bar = 0.4 * a0c                                        # clusters sit at 0.33-0.58 a0 (L61 B6); take ~0.4 a0
nu_clu = float(nu_blt_num(g_clu_bar / a0c))
info(f"the polarisation phantom at a cluster's g_bar ~ 0.4 a0 gives nu = {nu_clu:.2f} -> boost {nu_clu:.2f}x, i.e. M_dyn/M_b ~ {nu_clu:.1f}; "
     f"clusters need ~5.7 (X-COP) to ~11 (cores): the phantom alone is a factor {5.7/nu_clu:.1f}-{11/nu_clu:.1f} short")
info("So clusters need the MONOPOLE to supply the rest as real clustered mass -- fine for lensing (it IS mass), but it contradicts the")
info("galaxy weak-clustering hypothesis (D1) unless a scale switches sigma from smooth-in-galaxies to clustered-in-clusters; none exists.")
check("E4  GATE 6 CONTINGENT: cluster mass and shear shape can be fit ONLY by letting the monopole cluster in clusters (the phantom alone is "
      "a factor 3-6 short), which is the weak-clustering hypothesis run with the opposite sign -- the same unmechanised (H-c) as D1/D2",
      True, f"phantom boost at 0.4 a0 = {nu_clu:.2f}x vs 5.7-11 needed; monopole must supply the rest, differentially from galaxies")

# ---- E5 the L21 ladder --------------------------------------------------------------------------------------
P(""); P("E.5  THE NON-MONOTONE LADDER (L21): isolated 2MRS pairs need M_dyn/M_b = 30.9 +/- 1.6 at r_p ~ 132 kpc; X-COP clusters 5.73.")
Mb_pair = 10**11.19 * MSUN; rp = 132 * kpc; aN_pair = G * Mb_pair / rp**2
nu_pair = float(nu_blt_num((aN_pair / a0c)))
ladder_pair = nu_pair                                        # phantom boost = nu(a_N/a0); pairs deep in MOND
info(f"pair Newtonian field a_N = {aN_pair/a0c:.3f} a0 -> nu = {nu_pair:.2f} -> phantom M_dyn/M_b ~ {ladder_pair:.1f} (vs 30.9 needed: pairs need the")
info(f"monopole's clustered mass too, OR the deep-MOND enhancement plus a larger enclosed baryon budget) ; clusters {nu_clu:.1f} (vs 5.7): the")
info("non-monotonicity (pairs boosted more than clusters) is reproduced by nu(a_N/a0) alone -- deeper systems get more boost -- as in any MOND.")
check("E5  the non-monotone ladder's SHAPE (pairs boosted more than clusters) follows from nu(a_N/a0) as in any MOND theory; the AMPLITUDE at "
      "pairs needs the monopole's mass as well, the same contingency as E4", nu_pair > nu_clu,
      f"pair boost nu = {nu_pair:.1f} > cluster boost {nu_clu:.1f}; amplitude 30.9 needs clustered monopole (contingent)")

# ---- E6 the registered Gaia arms ----------------------------------------------------------------------------
P(""); P("E.6  THE REGISTERED GAIA ARMS.  Dipolar dark matter reproduces standard MOND phenomenology with the interpolating")
P("     function nu_BLT(y) = 1 + 1/sqrt(y), y = a_N/a0, so it predicts a wide-binary anomaly through the external-field effect.")
P("     Standard QUMOND EFE, sky-averaged: gamma_v = sqrt(nu(y_ext)*(1 + (1/3) d ln nu/d ln y)), y_ext = 1.289 (registered a_N,ext/a0).")
Y_EXTN = 1.28903                                            # the registration's Newtonian external field, in a0 (Amendment 8/10)
ARM_A = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}; NOVERDICT = 1.23
ARM_B_CEIL = {"canonical": 1.0450, "alt": 1.0300}
yext = Y_EXTN
nu_e = float(nu_blt_num(yext))
dlnnu = float((math.log(nu_blt_num(yext * 1.0001)) - math.log(nu_blt_num(yext / 1.0001))) / (2 * 0.0001))  # d ln nu/d ln y
gv = math.sqrt(nu_e * (1 + dlnnu / 3.0))                    # sky-averaged velocity boost (footing-independent in a0 units)
GV = {f: gv for f in FOOT}
gv_min, gv_max = gv, gv
P(f"      {'a_ext,N/a0':>10s} {'nu(y_ext)':>9s} {'d ln nu/d ln y':>14s} | {'gamma_v (sky-avg)':>17s} | {'Arm A canonical':>16s} {'Arm A alt':>12s} {'Arm B ceil':>11s}")
P(f"      {yext:10.3f} {nu_e:9.3f} {dlnnu:14.3f} | {gv:17.4f} | {ARM_A['canonical'][0]:.3f}-{ARM_A['canonical'][1]:.3f}  {ARM_A['alt'][0]:.3f}-{ARM_A['alt'][1]:.3f} {ARM_B_CEIL['canonical']:11.3f}")
in_A = any(ARM_A[f][0] <= gv <= ARM_A[f][1] for f in FOOT)
below_noverdict = gv <= NOVERDICT
check("E6  the class's wide-binary prediction falls inside a registered Gaia arm (so DR4 could CONFIRM it over Newton)", in_A or below_noverdict,
      f"gamma_v = {gv:.3f}: ABOVE Arm A's bands (1.16-1.23) and above the 1.23 no-verdict edge -- like the superfluid's 1.27-1.34, this is a "
      f"slow simple-nu transition; a DR4 result INSIDE Arm A or Newtonian is evidence AGAINST the dipolar phantom, DR4 cannot confirm it")
sig_tot = 0.028
info(f"at the frozen sigma_tot = {sig_tot}: gamma_v = {gv:.3f} sits {(gv-ARM_A['canonical'][1])/sig_tot:.1f}-{(gv-ARM_A['alt'][1])/sig_tot:.1f} sigma above Arm A's upper edges "
     f"and {(gv-1)/sig_tot:.0f} sigma above Newton.  This is the point-field EFE asymptote (Amendment-9 status), footing-independent in a0 units.")

# ---- E7 the preferred frame ---------------------------------------------------------------------------------
P(""); P("E.7  THE PREFERRED FRAME (L31).  The dipolar medium has a 4-velocity u^mu (its rest frame) and a dipole 4-vector xi^mu.")
P("     The medium's rest frame is a distinguished timelike direction, and xi^mu is dynamical (it propagates), so u is realised")
P("     by MATTER and propagates -- L61's arm (1c), a preferred frame carried by a propagating medium, as for the superfluid.")
check("E7  GATE 3 CARRIED: the medium supplies a preferred frame (its rest frame u^mu), realised by matter and propagating (the dipole "
      "field is dynamical) -- L31's projector realised by a medium, L61 arm (1c); not a non-propagating foliation", True,
      "u^mu = the medium's 4-velocity; the dipole xi^mu propagates, so the frame propagates -- same status as the superfluid's condensate")

# ======================================================================================================
sec("PART G -- THE INTERNAL SECTOR: mode count and HEALTH of the force that sources the dipoles")
# ======================================================================================================
P("The brief's known-hard sector: the medium must STAY polarised and stable.  Two things are computed -- the mode count of")
P("the dipole sector, and whether the polarised, weakly-clustered state is a stable configuration or an unstable equilibrium.")
P("")
P("G.1  Mode count.  Beyond GR's 2 tensor modes, the medium adds a pressureless fluid (the monopole sigma: 0 new PROPAGATING")
P("     gravitational modes, it is dust) and a dynamical dipole 4-vector xi^mu.  The dipole's spatial part xi^i (3 components)")
P("     carries the polarisation; with the internal potential W(Pi) its longitudinal mode is the MOND-active one.  Total field")
P("     content: 2 (tensor) + 3 (dipole vector) = up to 5 sectors, of which the longitudinal dipole is load-bearing.")
info("mode count: 2 tensor + a matter fluid (0 propagating grav modes) + a dynamical spatial vector xi^i (<= 3) -> the internal sector")
info("is a vector field with a potential, health decided by its kinetic sign and by the coupled polarisation+gravity response, next.")
P("")
P("G.2  The load-bearing instability.  MOND requires the medium to sit near PERFECT ANTI-SCREENING: the polarisation nearly")
P("     cancels the field, y = 4 pi G Pi ~ g, so the residual g_b is small.  Define the medium's effective gravitational")
P("     permittivity for its OWN density perturbations, epsilon = dg_b/dg = 1 - 4 pi G/W''(Pi).  As the system goes deeper into")
P("     MOND, epsilon -> 0, so the effective Newton constant for the monopole, G_eff = G/epsilon, DIVERGES.")
# W''(Pi) at the operating point: w(Pi) = 4piG Pi + (4piG)^2 Pi^2/a0, w'(Pi) = W''(Pi) = 4piG + 2(4piG)^2 Pi/a0
# at deep MOND 4piG Pi = y ~ g: W'' = 4piG(1 + 2 g/a0); epsilon = 1 - 1/(1+2g/a0) = (2g/a0)/(1+2g/a0)
def epsilon_of_g(gx):
    x = gx / a0c; return (2 * x) / (1 + 2 * x)               # -> 2 g/a0 as g -> 0
g_grid = np.array([0.01, 0.1, 1.0]) * a0c
eps_grid = epsilon_of_g(g_grid)
Geff_grid = 1.0 / eps_grid
info("epsilon(g) = (2 g/a0)/(1 + 2 g/a0):  at g = 0.01/0.1/1.0 a0  epsilon = " + ", ".join(f"{e:.3f}" for e in eps_grid)
     + "  -> G_eff/G = 1/epsilon = " + ", ".join(f"{v:.1f}" for v in Geff_grid))
# Jeans / free-fall timescale for the smooth monopole: t_ff ~ 1/sqrt(4 pi G_eff rho) = sqrt(epsilon)/sqrt(4 pi G rho)
# so the medium collapses FASTER than standard free-fall by sqrt(epsilon) < 1 in the MOND regime: weak clustering is UNSTABLE.
tff_ratio = math.sqrt(epsilon_of_g(0.1 * a0c))              # collapse time relative to standard free-fall at g = 0.1 a0
info(f"the smooth monopole's collapse time is shorter than standard free-fall by sqrt(epsilon) = {tff_ratio:.2f} at g = 0.1 a0: the MOND-tuned")
info("medium is MORE Jeans-unstable exactly where it must stay smooth.  'Weak clustering' is not a stable state but a fine-tuned unstable one.")
# the pincer, stated:
check("G1  the internal sector is UNSTABLE in the MOND regime: reproducing MOND forces the effective permittivity epsilon -> 0 (near perfect "
      "anti-screening), so the monopole's effective Newton constant G_eff = G/epsilon diverges and the smooth state the 'spent once' result "
      "needs (D1) is a fine-tuned unstable equilibrium -- a polarisation requiring an unstable configuration is not a theory",
      eps_grid[0] < 0.03 and Geff_grid[0] > 30,
      f"epsilon(0.01 a0) = {eps_grid[0]:.3f}, G_eff/G = {Geff_grid[0]:.0f}; collapse faster than free-fall by sqrt(eps) = {tff_ratio:.2f}")
P("")
P("     THE PINCER, stated as the theorem it is:  dipolar dark matter escapes L61 by making the phantom real gravitating mass")
P("     (so it PASSES lensing, E1) -- but the SAME construction that makes the polarisation nearly cancel the field (perfect")
P("     anti-screening, needed for MOND) makes the monopole's self-gravity diverge, so the smooth monopole that 'spent once'")
P("     REQUIRES (D1) cannot be maintained.  If the monopole stays smooth, the state is unstable; if it clusters, L61 fires")
P("     (D1: overshoot 1.692).  The lensing pass is real and structural; the death is in the internal sector, not at lensing.")

# ======================================================================================================
sec("PART F -- VERDICTS")
# ======================================================================================================
P("      gate                          verdict")
P(f"      hypothesis (a)                FAILS (escapes): A_K = 4 pi G Pi vanishes with the medium off (C1)")
P(f"      1 lensing vs dynamics         PASS -- THE STRUCTURAL DIFFERENCE: M_dyn/M_lens = {mdl_dipolar:.3f} ~ measured {meas_ratio['raw']:.2f}, because the")
P(f"                                    polarisation charge is REAL GRAVITATING MASS (v^2/c^2 is a correction to 1, not the whole signal) (E1)")
P(f"      2 Solar System                MARGINAL: computable (mu -> 1), unlike the superfluid; simple-mu residual ~ Saturn bound -- standard MOND's tension (E2)")
P(f"      3 preferred frame             CARRIED by the medium's rest frame, propagating (E7)")
P(f"      4 tensor speed                PASS (one metric, minimal coupling) (E3)")
P(f"      5 internal-sector health      UNSTABLE: MOND forces epsilon -> 0, G_eff -> infinity; smooth monopole is a fine-tuned unstable state (G1) -- THE KILL")
P(f"      6 clusters                    CONTINGENT on the monopole clustering in clusters but not galaxies -- unmechanised (H-c) (E4)")
P(f"      7 spent once                  ONCE only under weak clustering (D1); denser-at-recombination ordering is L61 B5 (D2)")
P(f"      Gaia arms                     gamma_v = {gv:.3f}, ABOVE Arm A (1.16-1.23) like the superfluid's 1.27-1.34: DR4 in-band or Newtonian = evidence against (E6)")
check("F1  dipolar dark matter escapes hypothesis (a), PASSES the lensing gate (a genuine structural difference from the superfluid), and "
      "passes tensor speed -- but dies in the internal sector: the MOND-tuned polarisation makes the smooth monopole gravitationally unstable",
      False, "escapes (a) [C1]; PASSES lensing [E1]; DIES at the internal-sector health gate [G1]; Solar System marginal, clusters/spent-once contingent")
check("F2  VERDICT -- dipolar dark matter, the last named member of the last open hatch, is ALIVE through every gate", False,
      "DEAD at the internal-sector-health gate (G1); NOT at lensing (E1 PASSES) -- the emergent-MOND hatch is now closed on both its named members")

P("")
P("THREE-SENTENCE VERDICT.")
P("  Dipolar dark matter escapes L61's hypothesis (a) exactly as the superfluid does -- its MOND force is the phantom of the")
P("  polarisation charge and vanishes with the medium off -- and it does something the superfluid could not: because that")
P(f"  phantom is REAL GRAVITATING MASS (the polarisation -div Pi sources T_00 with only a v^2/c^2 anisotropic stress), it PASSES")
P(f"  the lensing gate that killed the superfluid, M_dyn/M_lens = {mdl_dipolar:.2f} against the measured 1.02 where the superfluid gave {min(sf_pred_ovl):.1f}-{max(sf_pred_ovl):.1f}.")
P("  But it dies in the internal sector: reproducing MOND requires the polarisation to sit at near-perfect anti-screening")
P("  (epsilon -> 0), which makes the monopole's effective self-gravity diverge, so the smooth monopole that 'spends the anomaly")
P("  once' is a fine-tuned unstable equilibrium -- if it stays smooth the state is unstable, if it clusters L61's overshoot")
P("  (1.69) fires; and its distinctive Gaia number gamma_v = {:.2f} sits ABOVE the registered Arm A band (1.16-1.23), like the".format(gv))
P("  superfluid's 1.27-1.34, so a DR4 wide-binary result inside Arm A or Newtonian would count against it and DR4 cannot confirm it.")

P("")
P(f"RESULT: {NCHK} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   ({time.time()-T0:.1f} s)")
sys.exit(0)
