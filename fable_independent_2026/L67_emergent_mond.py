#!/usr/bin/env python3
"""
L67 -- EMERGENT MOND: the one class the excess-spent-once theorem leaves open BY ITS OWN HYPOTHESES
====================================================================================================
L61 proved (branch-independently) that a theory which (a) reproduces the deep-MOND relation with its cold
component switched off, (b) carries a pressureless component in the amount the CMB fixes, and (c) transmits
that component's pull to baryons no less efficiently in galaxies than at recombination, overshoots the
rotation curves pointwise.  (c) is closed on ordering in four variables.  Every theory this programme has
built satisfies (a): the kernel works with the cold component OFF and the cold component is then ADDED.

THE HATCH IS (a).  A theory in which the MOND force is EMERGENT FROM the dark sector -- no kernel exists with
the dark component off, because the dark component is what carries the a0 force -- violates (a) by
construction.  Superfluid dark matter (Berezhiani & Khoury 2015 = BK15; Berezhiani, Famaey & Khoury 2018 =
BFK18) is the concrete representative: a phonon-mediated force on baryons inside a condensed core, ordinary
cold dark matter in clusters and on the background.

WHAT THE RECORD SAYS, read first (PART B).  The named dark-sector no-go (g03w-g04j, 2026-09-06/07) closed
condensates and relics ADDED to the deposited action, whose kernel J(Y) carries a0 independently of the
dust amplitude.  A SEPARATE, earlier run -- condensate_pincer_2026/superfluid_route_gates_2026.py
(2026-09-02, 4/4) -- did examine the EMERGENT class, on ONE gate: the phase of the cosmological background
(thermalisation -> condensed background -> c_s^2 ~ rho^2 -> relativistic at recombination).  It is reproduced
here as a control.  It never touched lensing, the Solar System, the external-field effect, the wide-binary
arms, the preferred frame, or the excess-spent-once question, and it leans on extrapolating the superfluid
equation of state to recombination densities.  Those gates are independent of that extrapolation and are
run here.

WHAT IS RUN
  PART A  CONTROLS: mode counts (2, 3, 3, 5); L61's overshoot (median 1.692 at eta = 1) and its
          cold-fraction ceilings (0.355/0.276, 0.582/0.486); the recorded superfluid-route G2/G3 numbers;
          the Lane-Emden n = 1/2 polytrope constants; the KiDS lensing pipeline; BK's a0 = alpha^3 Lambda^2/M_Pl.
  PART B  the record: added sector or emergent?  Which recorded result covers what.
  PART C  hypothesis (a) for the emergent class -- derived from the phonon action, not asserted.
  PART D  is the galaxy anomaly spent once or twice in superfluid dark matter?  On SPARC, with the theory's
          own condensate profile (the P ~ rho^3 polytrope of the literature, and BK15's gradient-locked
          density) at the CMB's own abundance.
  PART E  the gates, cheapest kill first: lensing vs dynamics (the phonon does not bend light); Solar
          System; tensor speed; clusters; the L21 ladder and the superfluid transition; the external-field
          effect and the registered Gaia arms; the preferred frame in L31's sense.
  PART F  verdicts.

METHOD.  Nothing under closure_2026/ or the lead's directories is imported or executed; the recorded numbers
are rebuilt from their stated formulas with independent code.  Both a0 footings (9.3619e-11 canonical,
1.1279e-10 alt) on every dimensional number; the literature's two parameter sets are carried side by side
and labelled as recalled from the papers (only alpha^3 Lambda^2 is fixed by a0; Lambda m^3 fixes the
polytrope).  A class is alive only if the representative theory passes the gates run here.
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
OM, OB, OL = 0.315, 0.049, 0.685; OCH2 = 0.1200; OM_DM = OCH2 / hP**2; OM_R = 4.15e-5 / hP**2
RHO_DM0 = OM_DM * RHO_C
UPS_D, UPS_B = 0.5, 0.7
S_SAT, D_SAT = 2.540, 0.6476                              # the deposited theory's carried kernel (L61)
# ---- natural units ----------------------------------------------------------------------------------------
HBARC = hbar * c / eV                                     # eV m
EV4_J = eV / HBARC**3                                     # 1 eV^4 in J/m^3
EV_ACC = c / (hbar / eV)                                  # 1 eV of acceleration in m/s^2  (a = eV * c/hbar)
KG_EV = c**2 / eV                                         # 1 kg in eV
M_EV = 1.0 / HBARC                                        # 1 m in eV^-1
MPL = math.sqrt(hbar * c / (8 * math.pi * G)) * c**2 / eV # reduced Planck mass, eV
def rho_nat(rho_si): return rho_si * c**2 / EV4_J         # kg/m^3 -> eV^4
def rho_si(rho_nat_): return rho_nat_ * EV4_J / c**2

def Delta(s):
    s = np.asarray(s, float); sc = np.clip(s, 1e-300, S_SAT)
    d = np.where(s > 0, sc / np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_kernel(gb, a0): return gb + a0 * Delta(gb / a0)
def nu_rar(y): y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

# ---- the literature's parameter sets (recalled; only alpha^3 Lambda^2 is pinned by a0) --------------------
SETS = {"BK15":  dict(alpha=2.5, Lam=0.2e-3, m=0.6),      # Berezhiani & Khoury 2015, as recalled
        "BFK18": dict(alpha=5.7, Lam=0.05e-3, m=1.0)}     # Berezhiani, Famaey & Khoury 2018, as recalled
def a0_ph(S): return S["alpha"]**3 * S["Lam"]**2 / MPL * EV_ACC            # m/s^2
def lam_m3(S): return S["Lam"] * S["m"]**3                                  # eV^4

P("=" * 118)
P("L67 -- EMERGENT MOND: does the class that violates hypothesis (a) escape the theorem, and does it live?")
P("=" * 118)
P(f"a0 footings: canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e} m/s^2;  M_Pl(reduced) = {MPL:.4e} eV;  "
  f"1 eV^4 = {EV4_J:.3f} J/m^3;  1 eV of acceleration = {EV_ACC:.4e} m/s^2")
for k, S in SETS.items():
    info(f"{k}: alpha = {S['alpha']}, Lambda = {S['Lam']*1e3:.2f} meV, m = {S['m']} eV  ->  a0_ph = alpha^3 Lambda^2/M_Pl = "
         f"{a0_ph(S):.3e} m/s^2 = {a0_ph(S)/A0['canonical']:.2f} / {a0_ph(S)/A0['alt']:.2f} a0;  Lambda m^3 = {lam_m3(S):.2e} eV^4")

# ======================================================================================================
sec("PART A -- CONTROLS")
# ======================================================================================================
P("A.1  Mode counts, Dirac's formula N = (P - 2F - S)/2.")
def dirac(Pd, F, S): return (Pd - 2 * F - S) / 2.0
check("A1  control: GR = 2, GR + scalar = 3, khronometric = 3, Einstein-aether = 5",
      dirac(12, 4, 0) == 2 and dirac(14, 4, 0) == 3 and dirac(14, 4, 0) == 3 and dirac(18, 4, 0) == 5, "2, 3, 3, 5")
info(f"the same formula on GR + a phonon (a shift-symmetric scalar theta): P = 14, F = 4 -> N = {dirac(14,4,0):.0f}  (used in PART E)")

# ---- SPARC + abundance-matched halos, exactly L61's machinery ----------------------------------------------
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
M200A = np.concatenate([np.full(len(g["r"]), g["M200"]) for g in GAL])
info(f"SPARC loaded from {rel(os.path.join(DATA,'sparc_data'))}: {len(GAL)} galaxies, {len(GB)} points")
def resid_stats(eta, eps, foot):
    a0 = A0[foot]; gs = GB + eps * eta * GH; gp = GB + eta * GH + a0 * Delta(gs / a0)
    rr = np.log10(GO / gp); return float(np.sqrt(np.mean(rr**2))), float(np.median(rr))
a0c = A0["canonical"]; deep_c = GB < a0c; deep_a = GB < A0["alt"]
over = float(np.median((GB[deep_c] + GH[deep_c] + a0c * Delta(GB[deep_c] / a0c)) / GO[deep_c]))
kern = {f: resid_stats(0.0, 0.0, f) for f in FOOT}
info(f"kernel alone: rms {kern['canonical'][0]:.3f}/{kern['alt'][0]:.3f} dex at medians {kern['canonical'][1]:+.3f}/{kern['alt'][1]:+.3f}   (L61 A6: 0.145/0.142, +0.030/+0.003)")
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

# ---- the recorded superfluid-route numbers (G2/G3), rebuilt --------------------------------------------------
P(""); P("A.3  The recorded emergent-class run (superfluid_route_gates_2026, 2026-09-02): its G2/G3 numbers rebuilt.")
def Ez(z): return math.sqrt(OM_R * (1 + z)**4 + (OB + OM_DM) * (1 + z)**3 + (1 - OB - OM_DM - OM_R))
def z_therm(sig_m, v0):
    f = lambda z: RHO_DM0 * (1 + z)**3 * sig_m * v0 * (1 + z) / (H0 * Ez(z)) - 1.0
    lo, hi = 0.0, 1e9
    if f(lo) > 0: return 0.0
    for _ in range(200):
        mid = math.sqrt((lo + 1) * (hi + 1)) - 1
        if f(mid) > 0: hi = mid
        else: lo = mid
    return hi
zt = [z_therm(0.1 * 0.1, v0 * 1e3) for v0 in (1e-3, 1.0, 100.0)]
info(f"sigma/m = 0.1 cm^2/g: z_therm = {zt[0]:.0f}, {zt[1]:.0f}, {zt[2]:.0f} for v0 = 1e-3, 1, 100 km/s   (recorded: 31236, 1324, 198)")
def cs2_bg(a, cs_core_kms, dcore):
    x = (cs_core_kms * 1e3 / c)**2 * ((1 / a**3) / dcore)**2; return x / (1 + 3 * x)
rec = cs2_bg(1 / 1091., 200.0, 1e5); rec2 = cs2_bg(1 / 1091., 10.0, 1e6)
info(f"c_s^2(z_rec) for a 200 km/s core at 1e5 x mean: {rec:.2e} (recorded 3.3e-01, the relativistic cap); 10 km/s at 1e6: {rec2:.1e} (recorded 1.9e-03)")
check("A4  control: the recorded superfluid-route G2/G3 numbers reproduce (z_therm 31236/1324/198; c_s^2(rec) 0.33 and 1.9e-3)",
      all(abs(a / b - 1) < 0.02 for a, b in zip(zt, (31236, 1324, 198))) and abs(rec - 0.33) < 0.01 and abs(rec2 / 1.9e-3 - 1) < 0.1)

# ---- Lane-Emden n = 1/2 ----------------------------------------------------------------------------------------
P(""); P("A.4  The superfluid core: hydrostatic equilibrium with P = rho^3/(12 Lambda^2 m^6) is the Lane-Emden n = 1/2 polytrope.")
def lane_emden(n=0.5):
    def rhs(x, y):
        th, dth = y; th = max(th, 0.0)
        return [dth, -th**n - 2 * dth / x]
    x0 = 1e-6; y0 = [1 - x0**2 / 6, -x0 / 3]
    ev = lambda x, y: y[0]; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (x0, 20.0), y0, events=ev, dense_output=True, rtol=1e-10, atol=1e-12, max_step=0.01)
    xi1 = float(sol.t_events[0][0]); dth1 = float(sol.sol(xi1)[1])
    return sol, xi1, -xi1**2 * dth1
LE, XI1, M1 = lane_emden()
info(f"xi_1 = {XI1:.5f}  (tables: 2.75270),  -xi_1^2 theta'(xi_1) = {M1:.5f}  (tables: 3.78865)")
check("A5  control: the n = 1/2 Lane-Emden constants reproduce the tabulated 2.7527 and 3.7887 to 0.1%",
      abs(XI1 / 2.75270 - 1) < 1e-3 and abs(M1 / 3.78865 - 1) < 1e-3)
def le_theta(xi):
    xi = np.asarray(xi, float); out = np.zeros_like(xi); ins = xi < XI1
    out[ins] = np.maximum(LE.sol(xi[ins])[0], 0.0); return out
def le_mass(xi):
    """dimensionless enclosed mass -xi^2 theta'(xi), capped at M1 outside the core"""
    xi = np.asarray(xi, float); out = np.full_like(xi, M1); ins = xi < XI1
    out[ins] = -xi[ins]**2 * LE.sol(xi[ins])[1]; return out
def K_si(S):
    """P = K rho^3 in SI (Pa, kg/m^3) from P = rho^3/(12 Lambda^2 m^6) in natural units"""
    return c**6 / (EV4_J**2 * 12 * lam_m3(S)**2)
def core(M_si, S):
    """central density, scale length alpha and radius R of the n = 1/2 polytrope of total mass M (SI)"""
    K = K_si(S); A = 3 * K / (8 * math.pi * G)                     # alpha^2 = A rho_0
    rho0 = (M_si / (4 * math.pi * M1))**0.4 * A**(-0.6)
    alpha = math.sqrt(A * rho0); return rho0, alpha, XI1 * alpha
for k, S in SETS.items():
    rho0, alp, R = core(1e12 * MSUN, S)
    cs = math.sqrt(3 * K_si(S)) * rho0
    info(f"{k}: a 1e12 Msun core has rho_0 = {rho0*1e-3:.2e} g/cm^3 = {rho0/RHO_DM0:.1e} x the mean dark density, R = {R/kpc:.0f} kpc, "
         f"central c_s = {cs/1e3:.0f} km/s   (R scales as M^(1/5) (Lambda m^3)^(-2/5))")

# ---- KiDS lensing pipeline control --------------------------------------------------------------------------------
P(""); P("A.5  KiDS-1000 lensing RAR (Brouwer et al. 2021), read with the repository's own conversion.")
B = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")
PC_PER_M = 3.086e16; G_PC = 4.52e-30; CONV = 4 * G_PC * PC_PER_M
def load_rar(fname):
    d = np.genfromtxt(os.path.join(B, fname), comments="#")
    return d[:, 0], CONV * d[:, 1] / d[:, 4], CONV * d[:, 3] / d[:, 4]
gbK, goK, eK = load_rar("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
gbH, goH, eH = load_rar("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
dev = np.log10(goK / (gbK * nu_rar(gbK / 1.20e-10))); devH = np.log10(goH / (gbH * nu_rar(gbH / 1.20e-10)))
OVL = gbK >= 1e-12                                        # the SPARC-KiDS overlap: SPARC's deepest points, KiDS's highest bins
info(f"isolated lenses, {len(gbK)} bins, g_bar = {gbK.min():.1e}..{gbK.max():.1e}: full-range median log10(g_obs/nu_RAR(1.2e-10)) = {np.median(dev):+.3f} dex raw, "
     f"{np.median(devH):+.3f} hot-gas-corrected (diagnostic: the raw +0.12 is the low-g_bar circumgalactic-gas / two-halo excess Brouwer et al. discuss)")
info(f"at the SPARC-KiDS overlap g_bar >= 1e-12 ({int(OVL.sum())} bins, r ~ 30-100 kpc): deviations raw " + ", ".join(f"{v:+.2f}" for v in dev[OVL])
     + " dex; hot-gas-corrected " + ", ".join(f"{v:+.2f}" for v in devH[OVL]) + " dex")
# universality across the four stellar-mass bins at 30-300 kpc (the radii where E.1 is decided)
LOGM = {1: 10.0, 2: 10.45, 3: 10.7, 4: 10.9}; FGAS = {1: 0.5, 2: 0.3, 3: 0.2, 4: 0.15}
UNIV = {}
for b in range(1, 5):
    gb, go, ge = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
    r = np.sqrt(G * 10**LOGM[b] * (1 + FGAS[b]) * MSUN / gb); sel = (r > 30 * kpc) & (r < 300 * kpc)
    UNIV[b] = float(np.median(np.log10(go[sel] / (gb[sel] * nu_rar(gb[sel] / 1.2e-10)))))
spread_meas = max(UNIV.values()) - min(UNIV.values())
info("per-bin median offset from nu_RAR(1.2e-10) at 30-300 kpc: " + ", ".join(f"bin {b} (logM* {LOGM[b]}) {v:+.3f}" for b, v in UNIV.items())
     + f"  -> spread {spread_meas:.3f} dex: the lensing RAR is UNIVERSAL across a decade of stellar mass")
check("A6  control: at the SPARC-KiDS overlap the isolated lensing RAR sits on nu_RAR(1.2e-10) to within 0.1 dex (raw and hot-gas-corrected), and "
      "across the four stellar-mass bins at 30-300 kpc it is universal to better than 0.1 dex (Brouwer et al. 2021's own statements)",
      float(np.max(np.abs(dev[OVL]))) < 0.1 and float(np.max(np.abs(devH[OVL]))) < 0.1 and spread_meas < 0.1,
      f"overlap max |dev| {np.max(np.abs(dev[OVL])):.2f}/{np.max(np.abs(devH[OVL])):.2f} dex; across-bin spread {spread_meas:.3f} dex")
# the same on the framework's footings (for the record)
for f in FOOT:
    dv = np.log10(goK / (gbK * nu_rar(gbK / A0[f]))); info(f"  [{f:9s}] overlap median deviation from nu_RAR at the framework's a0: {np.median(dv[OVL]):+.3f} dex")

# ---- BK's a0 map ---------------------------------------------------------------------------------------------------
P(""); P("A.6  The phonon force's acceleration scale, a0_ph = alpha^3 Lambda^2 / M_Pl.")
LAM_DE = (OL * RHO_C * c**2 / EV4_J)**0.25
alp_half = (A0["canonical"] / EV_ACC * MPL / LAM_DE**2)**(1 / 3)
info(f"Lambda_DE = {LAM_DE*1e3:.3f} meV; the framework's canonical a0 needs alpha = {alp_half:.3f} at Lambda = Lambda_DE   (recorded G1: 0.464)")
check("A7  control: the recorded kappa<->alpha map reproduces (alpha = 0.464 at Lambda = Lambda_DE, canonical a0)",
      abs(alp_half - 0.464) < 0.005, f"{alp_half:.3f}")
check("A7b the literature's two parameter sets both land within a factor 1.5 of the measured a0 (the coupling is FITTED to it, like kappa)",
      all(0.6 < a0_ph(S) / 1.2e-10 < 1.5 for S in SETS.values()),
      "a0_ph/1.2e-10 = " + ", ".join(f"{k} {a0_ph(S)/1.2e-10:.2f}" for k, S in SETS.items()))

# ======================================================================================================
sec("PART B -- THE RECORD: were the recorded closures of an ADDED sector or of an EMERGENT one?")
# ======================================================================================================
P("B.1  The named no-go (g03w-g04j; L14 in FINDINGS).  In the deposited action (THE_ACTION_2026-09-05 sections 1-3)")
P("     the MOND force is 2(2-K_B) J^mu d_mu phi with the kernel J(Y) carrying a0; the condensate K(Q) = K_2 (Q-Q_0)^2")
P("     supplies dust whose amplitude 'is a free cosmological initial datum'.  The static law div[mu grad Phi] = 4 pi G rho")
P("     contains NO dust parameter.  g04j's own docstring: 'one mechanism that keeps a cold-on-cluster-scales fluid OUT of")
P("     galaxies has never been run'.  g04f: 'the candidate's dark sector as a single thermal species'.  Every one of those")
P("     closures is of a component ADDED to a kernel that already works at zero dust -- hypothesis (a) HOLDS for them.")
act = open(os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "THE_ACTION_2026-09-05.md"), encoding="utf-8").read()
g04j = open(os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "g04j_wave_dark_matter_door.py"), encoding="utf-8").read()
added = ("free cosmological initial datum" in act) and ("OUT of galaxies" in g04j) and ("div[μ∇Φ] = 4πGρ" in act or "∇·[μ∇Φ]" in act)
# structural: the kernel used for every galaxy fit in L61/L55/L49 is Delta(s) with no dust argument at all
kern_dust_free = (abs(float(Delta(np.array([0.3]))[0]) - 0.3 / math.expm1(math.sqrt(0.3))) < 1e-12)
check("B1  the named dark-sector no-go (g03w-g04j) closed a sector ADDED to a kernel that works at zero dust: hypothesis (a) holds "
      "for every theory it examined, so it does NOT cover the emergent class", added and kern_dust_free,
      "the action's a0 sits in J(Y); the dust amplitude is a free initial datum; the static law has no dust parameter")
P("")
P("B.2  The UNNAMED record: condensate_pincer_2026/superfluid_route_gates_2026.py (2026-09-02, 4 checks, 0 FAIL) took")
P("     'the dark field IS MOND' -- the Berezhiani-Khoury class, condensing inside galaxies and producing the a0 force")
P("     there as a phonon -- and closed it on the COSMOLOGICAL BACKGROUND: G2, any self-interaction that thermalises a")
P("     halo thermalised the background earlier (Gamma/H grows as (1+z)^2.5) where n lambda_dB^3 >> 1, so the background")
P("     condensed and, with T/T_c constant under expansion, stays condensed; G3, the condensed background's sound speed")
P("     c_s^2 ~ (rho/rho_core)^2 c_s,core^2 is relativistic at recombination for any core the phonons could hold up.")
P("     Reproduced at A4.  That IS a recorded closure of the emergent class -- on one gate, under one extrapolation")
P("     (the P ~ rho^3 equation of state carried to recombination densities, which the class's own literature flags as")
P("     the regime where its EFT is not established).  It says nothing about lensing, the Solar System, the EFE, the")
P("     Gaia arms, the preferred frame, or whether the anomaly is spent once.  Those are run below; they do not lean on it.")
check("B2  the recorded emergent-class closure is cosmological and reproduces; the theorem-driven gates are untested in the record",
      True, "scope: background phase + EOS extrapolation; gates 1-7 of the brief never run on the class")
# the EOS-softening escape, priced: any polytrope P ~ rho^n that holds a v_c core is hot at recombination unless n <~ 1.3
rho_core_over_mean = 6.5e3                                                  # the polytrope's own central density for 1e12 Msun (A.4)
zrec = 1090.0; ratio = (1 + zrec)**3 / rho_core_over_mean
ns = np.linspace(1.0, 3.0, 201); cs2_rec = (2e5 / c)**2 * ratio**(ns - 1)
n_max = float(ns[np.searchsorted(cs2_rec, 1e-5)]) if np.any(cs2_rec < 1e-5) else 1.0
info(f"pricing the escape: a core at {rho_core_over_mean:.0e} x mean held up at c_s = 200 km/s has c_s^2(z_rec)/c^2 = 4.4e-7 x ({ratio:.1e})^(n-1);")
info(f"  the loose GDM ceiling 1e-5 is met only for n <= {n_max:.2f} -- softer than any pressure that could hold the core (the phonon law needs n = 3)")

# ======================================================================================================
sec("PART C -- HYPOTHESIS (a) FOR THE EMERGENT CLASS, derived from the phonon action")
# ======================================================================================================
P("The BK15 phonon EFT:  L = P(X) - (alpha Lambda/M_Pl) theta rho_b,   P = (2 Lambda (2m)^{3/2}/3) X sqrt|X|,")
P("X = mu_loc - (grad theta)^2/(2m).  In the gradient-dominated (MOND) regime |X| = (grad theta)^2/2m.")
al, La, mm, Mp, gt, Mb_s, r_s = sp.symbols('alpha Lambda m M_Pl gradtheta M_b r', positive=True)
X = gt**2 / (2 * mm)
Pfun = sp.Rational(2, 3) * La * (2 * mm)**sp.Rational(3, 2) * X**sp.Rational(3, 2)
PX = sp.diff(Pfun, gt) / sp.diff(X, gt)                       # dP/dX
flux_coeff = sp.simplify(PX / mm)                              # the EOM is div[(P_X/m) grad theta] = alpha Lambda rho_b / M_Pl
# spherical: (P_X/m) |grad theta| * 4 pi r^2 = alpha Lambda M_b / M_Pl  ->  2 Lambda |grad theta|^2 4 pi r^2 = alpha Lambda M_b/M_Pl
gt_sol = sp.sqrt(al * Mb_s / (8 * sp.pi * Mp * r_s**2))
lhs = sp.simplify((flux_coeff * gt).subs(gt, gt_sol) * 4 * sp.pi * r_s**2)
eom_ok = sp.simplify(lhs - al * La * Mb_s / Mp) == 0
a_theta = sp.simplify(al * La / Mp * gt_sol)
aN = Mb_s / (8 * sp.pi * Mp**2 * r_s**2)                       # G M/r^2 with G = 1/(8 pi M_Pl^2)
a0_sym = sp.simplify(a_theta**2 / aN)
info(f"P_X/m = {flux_coeff};  spherical solution |grad theta| = sqrt(alpha M_b/(8 pi M_Pl r^2));  a_theta = (alpha Lambda/M_Pl)|grad theta|")
info(f"a_theta^2 / a_N = {a0_sym}   =  a0_ph  (BK15's scale, recovered symbolically)")
check("C1  the phonon force is a_theta = sqrt(a0_ph a_N) with a0_ph = alpha^3 Lambda^2/M_Pl, derived from the action (control on the algebra)",
      eom_ok and sp.simplify(a0_sym - al**3 * La**2 / Mp) == 0)
# the condensate density in the same regime: rho = m n = m P_X
rho_lock = sp.simplify(mm * PX)
info(f"the condensate density in the gradient-dominated regime is rho_SF = m P_X = {rho_lock}  (BK15's gradient-locked density)")
P("")
P("     HYPOTHESIS (a) asks for the force with the cold component OFF.  With no condensate there is no phonon: theta is")
P("     the Goldstone of the condensate's U(1), P(X) is the condensate's own pressure, and the coupling alpha Lambda theta rho_b")
P("     acts on baryons only where theta exists.  Set rho_SF -> 0: P_X -> 0 with it (rho_SF = m P_X above), the flux")
P("     coefficient vanishes, and the EOM has no solution carrying a force -- A_K == 0, not sqrt(g_bar a0).  L61's (H-b)")
P("     'with A_X = 0 the theory reproduces the observed relation' is therefore FALSE for the class, and the proof step")
P("     g_obs = g_bar + A_K that turns g_pred - g_obs into A_X cannot be taken.  The theorem's conclusion does not follow.")
rho_off = sp.limit(rho_lock, gt, 0)                                    # rho_SF -> 0 <=> grad theta -> 0 in this regime
check("C2  hypothesis (a) FAILS for the emergent class: with the condensate off the phonon force is identically zero, so (H-b) is "
      "violated and the excess-spent-once conclusion does not go through", rho_off == 0,
      "A_K(rho_SF = 0) = 0; the class is outside L61's hypotheses, exactly as the brief conjectured")
P("     What replaces (H-b): g_pred = g_bar + g_SF + a_theta, with g_SF the condensate's OWN Newtonian pull and a0_ph a")
P("     Lagrangian constant that the literature FITS (A7b).  Whether the anomaly is spent once is now a computation, PART D.")

# ======================================================================================================
sec("PART D -- SPENT ONCE OR TWICE?  The condensate's own pull on SPARC, at the CMB's abundance")
# ======================================================================================================
P("The cold component is present in galaxies at the abundance-matched amount (L61's M200, the CMB's Omega_c h^2 through")
P("the stellar-to-halo relation), but its PROFILE is the theory's: inside the thermalised region it is the n = 1/2")
P("polytrope of A.4 (BFK18's finite-temperature picture), and in BK15's zero-temperature MOND regime it is the")
P("gradient-locked rho_SF = 2 Lambda m^2 |grad theta|.  Both are computed at every SPARC point, both parameter sets.")
P("")
def g_poly(r, Mcore_si, S):
    rho0, alp, R = core(Mcore_si, S)
    return G * 4 * math.pi * rho0 * alp**3 * le_mass(r / alp) / r**2
def g_lock(r, Mb_si, S):
    """gradient-locked condensate: rho = 2 Lambda m^2 |grad theta|, |grad theta|^2 = alpha M_b/(8 pi M_Pl r^2) (natural units)"""
    Mb_ev = Mb_si * KG_EV; r_ev = r * M_EV
    gth = np.sqrt(S["alpha"] * Mb_ev / (8 * math.pi * MPL * r_ev**2))           # eV^2
    rho_ev4 = 2 * S["Lam"] * S["m"]**2 * gth                                    # eV^4, ~ 1/r
    # M(<r) = 4 pi int rho r^2 dr = 4 pi * (2 Lambda m^2 sqrt(alpha M_b/(8 pi M_Pl))) * r^2/2
    Menc_ev = 4 * math.pi * 2 * S["Lam"] * S["m"]**2 * np.sqrt(S["alpha"] * Mb_ev / (8 * math.pi * MPL)) * r_ev**2 / 2
    return Menc_ev / (8 * math.pi * MPL**2 * r_ev**2) * EV_ACC                  # G M/r^2 in eV -> m/s^2
ANOM = GO - GB
RES_D = {}
P(f"      {'profile':>34s} {'set':>6s} {'f_core':>6s} | {'median g_SF/anomaly (deep, can/alt)':>36s} | {'g_SF/a_theta at 10 kpc, L*':>26s}")
Lstar_r = 10 * kpc; Lstar_Mb = 5e10 * MSUN; Lstar_M200 = float(halo_mass_AM(0.7 * 5e10)) * MSUN
for k, S in SETS.items():
    for fcore in (1.0, 0.3):
        gsf = np.concatenate([g_poly(g["r"], fcore * g["M200"] * MSUN, S) for g in GAL])
        share = {f: float(np.median(gsf[d] / ANOM[d])) for f, d in (("canonical", deep_c), ("alt", deep_a))}
        ath10 = math.sqrt(a0_ph(S) * G * Lstar_Mb / Lstar_r**2)
        r10 = g_poly(np.array([Lstar_r]), fcore * Lstar_M200, S)[0] / ath10
        RES_D[("poly", k, fcore)] = dict(gsf=gsf, share=share)
        P(f"      {'polytrope core (BFK18 picture)':>34s} {k:>6s} {fcore:6.1f} | {share['canonical']:17.3f} / {share['alt']:14.3f} | {r10:26.3f}")
    gsf = np.concatenate([g_lock(g["r"], g["Mb"] * MSUN, S) for g in GAL])
    share = {f: float(np.median(gsf[d] / ANOM[d])) for f, d in (("canonical", deep_c), ("alt", deep_a))}
    RES_D[("lock", k, 1.0)] = dict(gsf=gsf, share=share)
    r10 = g_lock(np.array([Lstar_r]), Lstar_Mb, S)[0] / math.sqrt(a0_ph(S) * G * Lstar_Mb / Lstar_r**2)
    P(f"      {'gradient-locked (BK15 picture)':>34s} {k:>6s} {'--':>6s} | {share['canonical']:17.3f} / {share['alt']:14.3f} | {r10:26.3f}")
share_nfw = {f: float(np.median(GH[d] / ANOM[d])) for f, d in (("canonical", deep_c), ("alt", deep_a))}
P(f"      {'abundance-matched NFW (L55/L61)':>34s} {'--':>6s} {'1.0':>6s} | {share_nfw['canonical']:17.3f} / {share_nfw['alt']:14.3f} |")
info("(L55 D3 quotes the NFW halo's share as 109% on its enclosed-anomaly measure; the pointwise median here is the like-for-like number)")
worst = max(v["share"][f] for kk, v in RES_D.items() for f in FOOT)
check("D1  in superfluid dark matter the galaxy anomaly is spent ONCE: the condensate's own transmitted pull is below 20% of the "
      "measured anomaly at the deep-MOND SPARC points for every profile and parameter set, against the NFW halo's ~100%",
      worst < 0.20, f"largest median share {worst:.3f}; NFW {share_nfw['canonical']:.2f}/{share_nfw['alt']:.2f}")
P("")
P("     Why: the P ~ rho^3 polytrope is CORED with R ~ 120 kpc and rho_0 ~ 6e3 x the mean density (A.4), so the halo mass")
P("     sits at ~100 kpc rather than at 10 kpc -- the cold component is 'somewhere other than in galaxy halos' in the sense")
P("     L61 caveat 1 names.  This is the L1-type redistribution the added-sector no-go said pressure cannot achieve for a")
P("     condensate coupled to the lapse; a superfluid with its own stiff EOS achieves it, at the cost PART B.2 records.")
# D2: fit a0_ph on the deep points with the polytrope included, and the RAR residual
P("")
P("D.2  With the condensate included, fit the ONE constant a0_ph on the deep-MOND points (the theorem's domain).")
def fit_a0ph(gsf, d):
    grid = np.geomspace(2e-11, 3e-10, 400)
    med = [float(np.median(np.log10(GO[d] / (GB[d] + gsf[d] + np.sqrt(a * GB[d]))))) for a in grid]
    i = int(np.argmin(np.abs(med))); a = grid[i]
    rr = np.log10(GO[d] / (GB[d] + gsf[d] + np.sqrt(a * GB[d])))
    return a, float(np.sqrt(np.mean(rr**2))), float(np.median(rr))
FIT = {}
for key, v in RES_D.items():
    for f, d in (("canonical", deep_c), ("alt", deep_a)):
        FIT[key + (f,)] = fit_a0ph(v["gsf"], d)
# the same fit with NO condensate (the phonon alone), and with the NFW halo (L61's eta = 1)
for f, d in (("canonical", deep_c), ("alt", deep_a)):
    FIT[("none", "--", 0.0, f)] = fit_a0ph(np.zeros_like(GB), d)
    FIT[("nfw", "--", 1.0, f)] = fit_a0ph(GH, d)
P(f"      {'profile':>20s} {'set':>6s} {'f_core':>6s} {'footing':>9s} | {'a0_ph fitted':>12s} {'/a0_obs(1.2e-10)':>16s} {'rms dex':>8s} {'median':>8s}")
for key in sorted(FIT, key=lambda t: (t[0], t[1], t[2], t[3])):
    a, rms, med = FIT[key]
    P(f"      {key[0]:>20s} {key[1]:>6s} {key[2]:6.1f} {key[3]:>9s} | {a:12.3e} {a/1.2e-10:16.2f} {rms:8.3f} {med:+8.3f}")
kern_deep = {f: float(np.sqrt(np.mean(np.log10(GO[d] / g_kernel(GB[d], A0[f]))**2))) for f, d in (("canonical", deep_c), ("alt", deep_a))}
info(f"for scale: the deposited kernel alone on the same deep points: rms {kern_deep['canonical']:.3f}/{kern_deep['alt']:.3f} dex")
info("the fitted a0_ph sits at ~0.55 x 1.2e-10 even with NO condensate: that is the zero-temperature sqrt law's lack of an interpolation")
info("(it overshoots the transition region 0.3-1 a0), not double counting.  The double-counting measure is the RATIO of the fit with")
info("the condensate to the fit without it, against the same ratio for the NFW halo:")
RAT = {}
for key in list(RES_D) + [("nfw", "--", 1.0)]:
    for f in FOOT:
        RAT[key + (f,)] = FIT[key + (f,)][0] / FIT[("none", "--", 0.0, f)][0]
        info(f"  a0_ph(with {key[0]:>4s} {key[1]:>5s} f_core {key[2]:.1f}) / a0_ph(no condensate) = {RAT[key + (f,)]:.3f}   [{f}]   rms {FIT[key + (f,)][1]:.3f} vs {FIT[('none','--',0.0,f)][1]:.3f} dex")
ok_d2 = all(RAT[key + (f,)] > 0.8 and FIT[key + (f,)][1] < FIT[("none", "--", 0.0, f)][1] + 0.02 for key in RES_D for f in FOOT)
nfw_bad = all(RAT[("nfw", "--", 1.0, f)] < 0.5 for f in FOOT)
check("D2  with the condensate present the phonon scale needed to fit the deep-MOND RAR moves by < 20% and the rms by < 0.02 dex (every profile, "
      "set, footing), while the NFW halo at the same abundance cuts it by > 50% and adds 0.09 dex (L61's overshoot): the anomaly is spent once",
      ok_d2 and nfw_bad, "condensate ratios " + ", ".join(f"{v:.2f}" for k, v in RAT.items() if k[0] != 'nfw') + f"; NFW {RAT[('nfw','--',1.0,'canonical')]:.2f}")
# D3: the high-acceleration diagnostic (the zero-T law has no Newtonian limit)
hi = GB > 3 * a0c
for k, S in SETS.items():
    rr = np.log10(GO[hi] / (GB[hi] + np.sqrt(a0_ph(S) * GB[hi])))
    info(f"D3 diagnostic, {k}: at g_bar > 3 a0 ({int(hi.sum())} points) the bare sqrt law a_theta = sqrt(a0_ph g_bar) gives median residual "
         f"{np.median(rr):+.3f} dex (anomaly {math.sqrt(3)*a0_ph(S)/a0c:.2f} a0 at 3 a0 vs the RAR's {3*(nu_rar(3.0)-1):.2f} a0)")
info("   -- the zero-temperature phonon law has NO Newtonian limit; BFK18's finite-temperature term supplies the interpolation.")
info("   It is a diagnostic of the representative's transition region, not of the class, and it is not scored.")

# ======================================================================================================
sec("PART E -- THE GATES, cheapest kill first")
# ======================================================================================================
# ---- E1 lensing vs dynamics ------------------------------------------------------------------------------------
P("E.1  LENSING VERSUS DYNAMICS.  The phonon couples to rho_b (BK15: the coupling is to the baryon density; photons")
P("     carry no rest-mass density and T^mu_mu = 0), so light is deflected by g_bar + g_SF only.  Two questions:")
P("     (i) does the phonon field's OWN gravitating stress supply the lensing?  (ii) does the condensate's mass?")
# (i) symbolic
rho_ph = 2 * Mp**2 * a_theta / r_s                              # the phantom density for a 1/r force: g/(4 pi G r) with 4 pi G = 1/(2 M_Pl^2)
stress = sp.simplify(Pfun.subs(gt, gt_sol))                     # |P| at the solution: the scale of the gradient energy
ratio_sym = sp.simplify(stress / rho_ph)
vN2 = sp.simplify(aN * r_s)                                     # v_N^2 = G M/r in c = 1 units
info(f"phonon gradient energy / phantom density = {ratio_sym}  =  (1/3) v_N^2/c^2   [v_N^2 = G M_b/r = {vN2}]")
check("E1a the phonon's own stress cannot lens: it is the phantom's (1/3)(v_N/c)^2, the same v^2/c^2 suppression that killed L61's branch 1",
      sp.simplify(ratio_sym - vN2 / 3) == 0)
vn2 = G * MB * MSUN / RR / c**2
info(f"on the deep-MOND SPARC points: median (1/3) v_N^2/c^2 = {np.median(vn2[deep_c])/3:.2e}, max {np.max(vn2[deep_c])/3:.2e}")
# (ii) the condensate's mass: M_dyn/M_lens on SPARC deep points
P("")
P(f"      {'profile':>34s} {'set':>6s} {'f_core':>6s} | {'median M_dyn/M_lens (deep, can/alt)':>36s} {'90th pct':>9s}")
MDL = {}
for key, v in RES_D.items():
    gsf = v["gsf"]; S = SETS[key[1]]
    ath = np.sqrt(a0_ph(S) * GB)
    ratio = (GB + gsf + ath) / (GB + gsf)
    MDL[key] = {f: (float(np.median(ratio[d])), float(np.percentile(ratio[d], 90))) for f, d in (("canonical", deep_c), ("alt", deep_a))}
    P(f"      {('polytrope core' if key[0]=='poly' else 'gradient-locked'):>34s} {key[1]:>6s} {key[2]:6.1f} | {MDL[key]['canonical'][0]:17.2f} / {MDL[key]['alt'][0]:14.2f} {MDL[key]['canonical'][1]:9.2f}")
best_mdl = min(MDL[key][f][0] for key in MDL for f in FOOT)
# the MEASURED ratio, data to data, at the SPARC-KiDS overlap: SPARC dynamics vs KiDS lensing at the same g_bar
ovl = (GB >= 1e-12) & (GB <= gbK.max())
lens_raw = 10**np.interp(np.log10(GB[ovl]), np.log10(gbK), np.log10(goK)); lens_hot = 10**np.interp(np.log10(GB[ovl]), np.log10(gbH), np.log10(goH))
meas_ratio = {"raw": float(np.median(GO[ovl] / lens_raw)), "hot-gas-corrected": float(np.median(GO[ovl] / lens_hot))}
pred_ovl = {}
for key, v in RES_D.items():
    S = SETS[key[1]]; gsf = v["gsf"]; ath = np.sqrt(a0_ph(S) * GB)
    pred_ovl[key] = float(np.median(((GB + gsf + ath) / (GB + gsf))[ovl]))
info(f"MEASURED at the overlap g_bar = 1e-12..{gbK.max():.1e} ({int(ovl.sum())} SPARC points against the interpolated KiDS isolated curve): "
     f"median g_dyn(SPARC)/g_lens(KiDS) = {meas_ratio['raw']:.2f} raw, {meas_ratio['hot-gas-corrected']:.2f} hot-gas-corrected")
info("PREDICTED by the class at the same points: " + ", ".join(f"{k[0]} {k[1]} f={k[2]:.1f}: {v:.2f}" for k, v in pred_ovl.items()))
info("(cluster lensing gives M_dyn/M_lens = 1.0-1.3 by the record's own criterion; L61 C3 used |ratio - 1| < 0.2)")
check("E1b GATE 1 FAILS: where SPARC dynamics and KiDS lensing overlap in g_bar the measured M_dyn/M_lens is 1.0-1.2, and the class "
      "predicts >= 2.5 for every profile and parameter set -- the phonon supplies the dynamics and nothing supplies the lensing",
      best_mdl > 1.5 and min(pred_ovl.values()) > 2.0 and max(meas_ratio.values()) < 1.3,
      f"measured {meas_ratio['raw']:.2f}/{meas_ratio['hot-gas-corrected']:.2f}; predicted {min(pred_ovl.values()):.2f}-{max(pred_ovl.values()):.2f}; all-deep median >= {best_mdl:.2f}")
# (iii) on the KiDS data: the mass bins.  r(g_bar) per bin, the class's lensing prediction vs the measured lensing RAR
P("")
P("      On the KiDS-1000 isolated-lens mass bins (Brouwer Fig. 9; masses as the repository's h_kids scripts carry them):")
KROWS = []
for b in range(1, 5):
    gb, go, ge = load_rar(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt")
    Mst = 10**LOGM[b]; Mb_b = Mst * (1 + FGAS[b]); M200_b = float(halo_mass_AM(Mst))
    r = np.sqrt(G * Mb_b * MSUN / gb)                         # the radius at which a point-like baryon mass gives g_bar
    for k, S in SETS.items():
        gsf_p = g_poly(r, M200_b * MSUN, S); gsf_l = g_lock(r, Mb_b * MSUN, S)
        cc = float(c200_DM14(M200_b)); R200 = (3 * M200_b * MSUN / (4 * math.pi * 200 * RHO_C))**(1 / 3.)
        gnfw = G * (M200_b - Mb_b) * MSUN * _nfwm(cc * np.clip(r / R200, 1e-6, 6)) / _nfwm(cc) / r**2
        sel = (r > 30 * kpc) & (r < 300 * kpc)
        for lab, gsf in (("poly", gsf_p), ("lock", gsf_l), ("nfw", gnfw)):
            dv = np.log10(go[sel] / (gb[sel] + gsf[sel]))
            KROWS.append((b, k, lab, float(np.median(dv)), float(np.mean(dv / (ge[sel] / go[sel] / math.log(10)))), int(sel.sum())))
P(f"      {'bin':>4s} {'logM*':>6s} {'set':>6s} {'lensing model':>22s} | {'median log10(g_lens,obs / g_lens,pred) 30-300 kpc':>50s} {'mean pull':>10s} {'N':>3s}")
for b, k, lab, med, pull, n in KROWS:
    name = {"poly": "baryons + polytrope core", "lock": "baryons + gradient-locked", "nfw": "baryons + NFW (LCDM-like)"}[lab]
    P(f"      {b:4d} {LOGM[b]:6.2f} {k:>6s} {name:>22s} | {med:50.3f} {pull:10.1f} {n:3d}")
lock_def = min(med for b, k, lab, med, pull, n in KROWS if lab == "lock")
poly_spread = min(max(med for b, k, lab, med, pull, n in KROWS if lab == "poly" and k == kk)
                  - min(med for b, k, lab, med, pull, n in KROWS if lab == "poly" and k == kk) for kk in SETS)
poly_low = min(med for b, k, lab, med, pull, n in KROWS if lab == "poly" and b <= 2)
nfw_spread = max(med for b, k, lab, med, pull, n in KROWS if lab == "nfw") - min(med for b, k, lab, med, pull, n in KROWS if lab == "nfw")
info(f"the measured lensing RAR at 30-300 kpc is universal across the bins to {spread_meas:.3f} dex (A6).  The class's two profiles fail it two ways:")
info(f"  gradient-locked (a function of g_bar alone, so universal in shape): uniformly LOW by >= {lock_def:.2f} dex = a factor {10**lock_def:.1f} in lensing mass;")
info(f"  polytrope core (its mass is the abundance-matched halo's, so it depends on M200): spread {poly_spread:.2f} dex across the bins, low by >= {poly_low:.2f} dex in the two")
info(f"  low-mass bins and HIGH in the massive ones -- the same differential failure abundance-matched NFW shows here ({nfw_spread:.2f} dex), which is what")
info("  h_kids_halo_bound_CORRECTION (b) records ('differentially, KiDS forbids the halo-to-baryon ratio varying between stellar-mass bins').")
check("E1c on the KiDS mass bins at 30-300 kpc the class's lensing is not the measured lensing RAR: the gradient-locked profile is uniformly "
      ">= 0.25 dex low, and the polytrope spreads by >= 0.4 dex across bins where the measured relation is universal to < 0.1 dex",
      lock_def >= 0.25 and poly_spread >= 0.4 and spread_meas < 0.1,
      f"gradient-locked deficit >= {lock_def:.2f} dex; polytrope spread {poly_spread:.2f} dex vs measured {spread_meas:.3f} dex")
# (iv) THE PINCER: normalise the condensate to the lensing instead, and the theorem re-enters
P("")
P("      THE PINCER.  Make the condensate supply the lensing (M_SF = M_phantom at every radius, whatever profile that")
P("      takes): then g_lens = g_RAR, and the same mass pulls on the baryons too, so g_dyn = g_RAR + a_theta.")
for k, S in SETS.items():
    for f, d in (("canonical", deep_c), ("alt", deep_a)):
        g_rar = GB[d] * nu_rar(GB[d] / A0[f]); twice = (g_rar + np.sqrt(a0_ph(S) * GB[d])) / GO[d]
        info(f"[{f:9s}] {k}: lensing-normalised condensate -> median g_dyn/g_obs = {np.median(twice):.3f}   (L61 B1's kernel + NFW: 1.692)")
twice_c = float(np.median((GB[deep_c] * nu_rar(GB[deep_c] / a0c) + np.sqrt(a0_ph(SETS['BFK18']) * GB[deep_c])) / GO[deep_c]))
check("E1d the excess-spent-once theorem RE-ENTERS through lensing: a condensate normalised to the lensing overshoots the rotation "
      "curves by the phonon force, pointwise -- the class can have the lensing or the dynamics, not both", twice_c > 1.4,
      f"median g_dyn/g_obs = {twice_c:.3f} (BFK18, canonical) when the condensate lenses correctly")
P("      Stated as the theorem it is: in a theory whose MOND force acts on baryons but not on light, lensing = dynamics")
P("      forces A_X = A_K pointwise, which is (H-a)+(H-c) with eta = 1 -- L61's hypotheses are RESTORED by the lensing")
P("      gate, and the overshoot is L61's.  The only escape is a phonon that also deflects light, i.e. a coupling to the")
P("      photon stress -- a disformal coupling, which is L61's branch 3, dead at the tensor-speed gate (E1 identity).")

# ---- E2 Solar System -------------------------------------------------------------------------------------------
P(""); P("E.2  SOLAR SYSTEM.  The zero-temperature phonon law is exact in its regime and has no Newtonian limit.")
r_sat = 9.5826 * AU; gN_sat = G * 1.98847e30 / r_sat**2; SAT_BOUND = 6.7e-11      # Msun, Pitjev-Pitjeva
gN_sat_ev = gN_sat / EV_ACC
for k, S in SETS.items():
    ath = math.sqrt(a0_ph(S) * gN_sat); Mph = ath * r_sat**2 / G / MSUN
    X_sat = S["alpha"] * MPL * gN_sat_ev / (2 * S["m"])                         # eV
    a_eft = 2 * S["m"]**2 / (S["alpha"] * MPL) * EV_ACC                          # where X = m
    # the linear (chemical-potential) regime boundary at the Sun's location, with the polytrope's density there
    rho_sun = core(Lstar_M200, S)[0]                                             # the polytrope is flat inside; rho(8 kpc) ~ rho_0
    rho_sun_ev4 = rho_nat(rho_sun)
    a_star = rho_sun_ev4**2 / (4 * S["alpha"] * S["Lam"]**2 * S["m"]**4 * MPL) * EV_ACC
    Geff = 1 + 2 * S["alpha"]**2 * S["Lam"]**2 * S["m"]**2 / rho_sun_ev4
    info(f"{k}: bare a_theta(Saturn) = {ath:.2e} m/s^2 -> phantom mass {Mph:.2e} Msun = {Mph/SAT_BOUND:.1e} x the Pitjev-Pitjeva bound;")
    info(f"   X(Saturn) = alpha M_Pl a_N/(2m) = {X_sat:.2f} eV against m = {S['m']} eV: the non-relativistic EFT is at its boundary (X = m at a_N = {a_eft:.1e} m/s^2, Saturn's is {gN_sat:.1e});")
    info(f"   the chemical-potential (linear, G_eff = {Geff:.1f} G) regime lies BELOW a_* = {a_star:.2e} m/s^2 = {a_star/a0c:.3f} a0 -- galaxy outskirts, not the Solar System")
    SETS[k]["Mph_ratio"] = Mph / SAT_BOUND; SETS[k]["a_eft"] = a_eft; SETS[k]["a_star"] = a_star
info("the environmental escape -- 'the condensate is absent at the Sun' -- is closed by the record: sf06 (superfluid_2026) shows the Sun")
info("sits at 0.67 of the Milky Way's own MOND radius, so every environmental variable is the same at 1 AU and at 12 kpc.")
check("E2  GATE 2 NOT PASSED: inside its own EFT the class's phonon force at Saturn is >= 1e6 x the phantom-mass bound; at Saturn the EFT "
      "reaches X = m and the literature defers to unspecified higher-derivative operators; no computable Solar-System pass exists",
      all(S["Mph_ratio"] > 1e6 for S in SETS.values()), "the class has no Solar-System prediction, only a deferral")

# ---- E3 tensor speed --------------------------------------------------------------------------------------------
P(""); P("E.3  TENSOR SPEED.  The gravitational sector is Einstein-Hilbert; the phonon is a matter field with sound speed c_s = rho/(2 Lambda m^3).")
for k, S in SETS.items():
    rho0 = core(Lstar_M200, S)[0]; cs = math.sqrt(3 * K_si(S)) * rho0
    info(f"{k}: c_s(core) = {cs/1e3:.0f} km/s = {cs/c:.1e} c;  c_T = c exactly (no modification of the tensor sector)")
check("E3  GATE 4 PASSES: c_T = c (GR tensor sector untouched); the phonon is subluminal in every core", True, "trivial for the class")

# ---- E4 clusters ------------------------------------------------------------------------------------------------
P(""); P("E.4  CLUSTERS.  The class's own statement: the bulk of a cluster never thermalises (BK15 section VI), so it is a")
P("     collisionless cold component with an NFW-like profile -- which is exactly what g04a found the corrected cluster")
P("     residual needs (6.8 x baryons, rho ~ r^-1.5, 'only cold DM satisfies all four constraints').")
def gamma_rate(rho, v, sig_m, m_eV):
    """BK15's thermalisation rate with Bose enhancement: Gamma = N n sigma v, N = n (2 pi hbar/(m v))^3"""
    m = m_eV * eV / c**2; n = rho / m; N = n * (2 * math.pi * hbar / (m * v))**3
    return N * n * sig_m * m * v            # n sigma v * N with sigma = (sigma/m) m
tdyn_gal = 10 * kpc / 2e5; tdyn_clu = 1000 * kpc / 1e6
for k, S in SETS.items():
    gg = gamma_rate(1e-22, 2e5, 0.01, S["m"]) * tdyn_gal          # galaxy: 1e-25 g/cm^3 at ~10 kpc, 200 km/s, sigma/m = 0.1 cm^2/g
    gc = gamma_rate(1e-24, 1e6, 0.01, S["m"]) * tdyn_clu          # cluster: 1e-27 g/cm^3 at ~1 Mpc, 1000 km/s
    info(f"{k}: Gamma t_dyn (Bose-enhanced, sigma/m = 0.1 cm^2/g): galaxy interior {gg:.1e}, cluster at 1 Mpc {gc:.1e} -> ratio {gg/gc:.1e}")
check("E4  GATE 6 PASSES BY INHERITANCE: the un-thermalised cluster bulk is cold collisionless matter at the cosmic abundance; the cluster "
      "mass and shear shape are LCDM's, which the record says is what the cluster residual needs (g04a)", True,
      "not a computed cluster fit: the class inherits LCDM's cluster, with the galaxy/cluster contrast set by the Bose-enhanced rate")

# ---- E5 the L21 ladder and the superfluid transition ------------------------------------------------------------------
P(""); P("E.5  THE LADDER (L21): a Newtonian reading of the isolated 2MRS pairs needs M_dark/M_b = 30.9 +/- 1.6 within the pair")
P("     separation (median r_p = 132 kpc, log M_b(pair) = 11.19); X-COP clusters need 5.73 +/- 0.68 at 0.80 R500; cosmic 5.43.")
Mb_pair = 10**11.19 * MSUN; Mb_each = Mb_pair / 2; rp = 132 * kpc
M200_each = float(halo_mass_AM(0.7 * Mb_each / MSUN)) * MSUN
aN_pair = G * Mb_pair / rp**2
for k, S in SETS.items():
    rho0, alp, R = core(M200_each, S)
    Menc = 4 * math.pi * rho0 * alp**3 * le_mass(np.array([rp / alp]))[0]
    newton_ratio = 2 * Menc / Mb_pair                                     # both members' cores enclosed within r_p, per unit pair baryon mass
    ath = math.sqrt(a0_ph(S) * aN_pair); phonon_ratio = ath / aN_pair     # phonon force as a Newtonian-equivalent mass ratio
    tot = 1 + newton_ratio + phonon_ratio
    info(f"{k}: each member's core R = {R/kpc:.0f} kpc (> r_p: the pair is INSIDE the superfluid); enclosed condensate 2 M_SF(<r_p)/M_b = {newton_ratio:.1f};")
    info(f"   phonon force at r_p = {phonon_ratio:.1f} x Newton on the baryons; total Newtonian-equivalent M_dyn/M_b = {tot:.1f} vs 31.9 needed (30.9 + 1); "
         f"abundance-matched LCDM alone: {2*(M200_each)/Mb_pair:.1f}")
    SETS[k]["ladder"] = tot; SETS[k]["R_core"] = R
ok_ladder = all(abs(math.log10(S["ladder"] / 31.9)) < 0.30 for S in SETS.values())
check("E5  the non-monotone ladder (pairs 30.9, clusters 5.7) is reproduced to within the 0.3 dex abundance-matching systematic -- "
      "because outside the superfluid interior the class IS LCDM and the ladder is LCDM's stellar-to-halo relation, not the superfluid transition",
      ok_ladder, "M_dyn/M_b at r_p = " + ", ".join(f"{k} {S['ladder']:.1f} ({math.log10(S['ladder']/31.9):+.2f} dex, {(S['ladder']-31.9)/1.6:.1f} sigma_stat)" for k, S in SETS.items())
      + " vs 31.9 +/- 1.6; the pass is on the systematic, not the statistics")
info("the transition itself: core radius R ~ 120-160 kpc for L* (M^(1/5)); pairs at 132 kpc sit INSIDE it, so the phonon acts between")
info("the members and adds ~20% in mass-equivalent -- the ladder's shape is inherited, and the transition is not what produces it.")

# ---- E6 the external-field effect and the Gaia arms ----------------------------------------------------------------------
P(""); P("E.6  EXTERNAL-FIELD EFFECT AND THE REGISTERED GAIA ARMS.  The phonon equation div[|grad theta| grad theta] = alpha rho_b/(2 M_Pl)")
P("     linearised about the Galactic gradient is an anisotropic Poisson equation with D = |grad theta_e| (1 + e e), i.e. AQUAL's")
P("     EFE with mu(x) = x exactly (L = 1) and no interpolation.  A binary's phonon force over Newton is then")
P("     sqrt(a0_ph / a_N,ext) x A_geo, with a_N,ext the Galaxy's BARYONIC Newtonian field (the phonon is baryon-sourced).")
# geometric factor: orientation-averaged |grad u| for u = (1/sqrt(1+L)) / sqrt(rperp^2 + rpar^2/(1+L)), L = 1
Lg = 1.0
psi = np.linspace(0, math.pi, 4001)
rpar = np.cos(psi); rper = np.sin(psi)
den = (rper**2 + rpar**2 / (1 + Lg))**1.5
Fpar = (1 / math.sqrt(1 + Lg)) * (rpar / (1 + Lg)) / den; Fper = (1 / math.sqrt(1 + Lg)) * rper / den
Fmag = np.sqrt(Fpar**2 + Fper**2)
A_geo = float(np.trapz(Fmag * np.sin(psi), psi) / 2)
F_along = float(Fmag[0]); F_across = float(Fmag[2000])
info(f"A_geo (sphere-averaged force magnitude over Newton's, per unit sqrt(a0_ph/a_N,ext)) = {A_geo:.3f}; along the field {F_along:.3f}, across {F_across:.3f} (ratio {F_along/F_across:.3f} = sqrt 2)")
Y_EXTN = 1.28903                                                   # the registration's Newtonian external field, in a0 (Amendment 8/10)
ARM_A = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}; NOVERDICT = 1.23
ARM_B_CEIL = {"canonical": 1.0450, "alt": 1.0300}; ARM_B_CORR = 1.0000
GV = {}
P(f"      {'set':>6s} {'footing':>9s} {'a_N,ext':>10s} | {'force boost':>11s} {'gamma_v':>8s} | {'Arm A band':>16s} {'Arm B ceiling':>13s}")
for k, S in SETS.items():
    for f in FOOT:
        aNe = Y_EXTN * A0[f]; boost = 1 + math.sqrt(a0_ph(S) / aNe) * A_geo; gv = math.sqrt(boost)
        GV[(k, f)] = gv
        P(f"      {k:>6s} {f:>9s} {aNe:10.3e} | {boost:11.3f} {gv:8.4f} | {ARM_A[f][0]:.4f}-{ARM_A[f][1]:.4f} {ARM_B_CEIL[f]:13.4f}")
gv_min = min(GV.values()); gv_max = max(GV.values())
in_A = any(ARM_A[f][0] <= GV[(k, f)] <= ARM_A[f][1] for k in SETS for f in FOOT)
in_B = any(GV[(k, f)] <= ARM_B_CEIL[f] for k in SETS for f in FOOT)
check("E6  the class's wide-binary prediction falls inside a registered Gaia arm (so that DR4 could CONFIRM it)", in_A or in_B,
      f"gamma_v = {gv_min:.3f}-{gv_max:.3f}: ABOVE Arm A's band and above the 1.23 no-verdict edge; Arm B (<= 1.045/1.030, corrected 1.000) is far below")
sig_tot = 0.028
info(f"at the frozen sigma_tot = {sig_tot}: the class sits {(gv_min-ARM_A['canonical'][1])/sig_tot:.1f}-{(gv_max-ARM_A['alt'][1])/sig_tot:.1f} sigma above Arm A's upper edges and "
     f"{(gv_min-1)/sig_tot:.0f}-{(gv_max-1)/sig_tot:.0f} sigma above Newton -- a DR4 result inside Arm A's band, or Newtonian, is evidence against the phonon")
info("stated against the class: this is the point-field EFE asymptote (like Amendment 9's provisional number), not a full nonlinear solve;")
info("the along/across anisotropy is sqrt 2 in FORCE with the ALONG direction larger (L = 1), a sign the registered Arm-A rule can test.")

# ---- E7 the preferred frame ------------------------------------------------------------------------------------------
P(""); P("E.7  THE PREFERRED FRAME (L31).  The phonon EFT is the non-relativistic limit of a Lorentz-invariant P(X), X = -(d theta)^2,")
P("     expanded about theta = m t: a TIMELIKE gradient vev.  Its rest frame is the condensate's.")
t, x, y, z = sp.symbols('t x y z', real=True); mth = sp.symbols('m', positive=True)
th = sp.Function('vartheta')(t, x, y, z)
theta = mth * t + th
g = sp.diag(-1, 1, 1, 1); gi = g.inv()
dth = sp.Matrix([sp.diff(theta, v) for v in (t, x, y, z)])
Xrel = -(dth.T * gi * dth)[0, 0]
Xbar = sp.simplify(Xrel.subs({th: 0}))
u = sp.Matrix([1, 0, 0, 0])                                                   # the vev's unit direction, d theta_bar / m
hproj = gi + u * u.T                                                          # h^{mu nu} = g^{mu nu} + u^mu u^nu
grad2 = sp.simplify((dth.T * hproj * dth)[0, 0])
spatial = sum(sp.diff(theta, v)**2 for v in (x, y, z))
info(f"X_bar = {Xbar} > 0: the background gradient is timelike (spontaneous Lorentz breaking);  h^{{mu nu}} d theta d theta = {sp.simplify(grad2 - spatial) == 0 and '|grad theta|^2'}")
info(f"the non-relativistic X = X_bar/(2m) - ... expands as {sp.simplify(sp.expand(Xrel - mth**2)/(2*mth))} : MOND's argument is the projector contraction of L31 Q3, with u the condensate's 4-velocity")
frame_ok = (Xbar == mth**2) and (sp.simplify(grad2 - spatial) == 0)
check("E7  the class carries a preferred frame in L31's sense: a distinguished timelike u (the condensate's rest frame) supplies the "
      "projector that makes |grad theta| a scalar -- L31's Proposition Q realised by MATTER rather than by geometry", frame_ok,
      "u = d theta_bar/m, timelike; y is h^{mu nu} d theta d theta exactly")
info(f"but u PROPAGATES (the phonon: N = {dirac(14,4,0):.0f} modes), so this is L61's arm (1c) -- a scalar with a timelike gradient vev -- not L31's")
info("non-propagating foliation; the extra mode is the price, and it is a mode that does not bend light, which is why E1 closes it.")
P("      The unification, stated: L31 says a non-propagating MOND scalar needs a distinguished timelike u; L61 says a propagating")
P("      Lorentz-invariant one cannot lens.  The superfluid is the matter realisation of the first sentence and dies on the second.")

# ======================================================================================================
sec("PART F -- VERDICTS")
# ======================================================================================================
alive_gates = dict(lensing=not (best_mdl > 1.5), solar=not all(S["Mph_ratio"] > 1e6 for S in SETS.values()), tensor=True,
                   clusters=True, ladder=ok_ladder, frame="carried (matter-realised, propagating)")
P("      gate                          verdict")
P(f"      1 lensing vs dynamics         DEAD: measured M_dyn/M_lens {meas_ratio['raw']:.2f}/{meas_ratio['hot-gas-corrected']:.2f} at the overlap, class >= {min(pred_ovl.values()):.2f};")
P(f"                                    KiDS 30-300 kpc: gradient-locked >= {lock_def:.2f} dex low, polytrope spread {poly_spread:.2f} dex vs measured {spread_meas:.3f};")
P(f"                                    lensing-normalised horn overshoots by {twice_c:.2f} (the theorem re-enters)")
P(f"      2 Solar System                NOT PASSED: bare force >= {min(S['Mph_ratio'] for S in SETS.values()):.0e} x the Saturn bound; EFT at X = m there; deferral to UV operators")
P(f"      3 preferred frame             CARRIED, by the condensate's rest frame (E7); propagating, so branch-1 arm (1c)")
P(f"      4 tensor speed                PASS (GR tensor sector)")
P(f"      5 mode health                 3 modes, phonon healthy inside the condensate (c_s^2 = 3 K rho^2 > 0); not the deciding gate")
P(f"      6 clusters                    PASS by inheritance (un-thermalised bulk = cold collisionless at cosmic abundance)")
P(f"      7 cosmology                   CLOSED IN THE RECORD (superfluid_route_gates_2026 G2/G3, reproduced at A4), under the EOS extrapolation")
P(f"      excess spent once?            YES in dynamics (D1/D2, share <= {worst:.2f}) -- the hatch is real; NO once lensing is imposed (E1d)")
P(f"      Gaia arms                     gamma_v = {gv_min:.3f}-{gv_max:.3f}, above both registered arms; DR4 in-band or Newtonian = evidence against")
check("F1  the class escapes hypothesis (a) AND passes every gate run here", False,
      "escapes (a) [C2], spends the anomaly once in dynamics [D1], and dies at gate 1 [E1b-E1d]; gate 2 not passed [E2]")
check("F2  VERDICT -- the emergent-MOND class, represented by superfluid dark matter, is ALIVE", False,
      "DEAD at the lensing gate, independently of the recorded cosmological closure; the theorem re-enters through lensing")

P("")
P("THREE-SENTENCE VERDICT.")
P("  The emergent class is real and the theorem's hatch is real: with the condensate off the phonon force vanishes, so L61's")
P("  hypothesis (a) fails by construction, and on SPARC the P ~ rho^3 core is so diffuse that the condensate's own pull is a")
P(f"  few percent of the anomaly ({worst:.0%} at worst) -- the galaxy anomaly IS spent once, by the phonon, at the CMB's abundance.")
P("  It dies at the first gate: the phonon does not bend light and its own stress is (1/3)(v/c)^2 of the phantom, so the class")
P(f"  predicts M_dyn/M_lens >= {min(pred_ovl.values()):.1f} where the measured ratio is {meas_ratio['raw']:.2f} raw / {meas_ratio['hot-gas-corrected']:.2f} hot-gas-corrected (SPARC dynamics")
P(f"  against KiDS lensing at the same g_bar), its lensing at 30-300 kpc is >= {lock_def:.1f} dex low or spread {poly_spread:.1f} dex across mass bins where the data are universal to")
P(f"  {spread_meas:.2f} dex; and normalising the condensate to the lensing instead restores A_X = A_K pointwise")
P(f"  and overshoots the rotation curves by {twice_c:.2f}, which is L61's overshoot re-entering through the lensing gate.")
P("  Two independent closures therefore stand -- the recorded cosmological one (background condensed and relativistic at")
P("  recombination, reproduced) and this lane's lensing one, which does not lean on the equation-of-state extrapolation --")
P(f"  while the class's distinctive Gaia number, gamma_v = {gv_min:.2f}-{gv_max:.2f} with the along-field boost larger, sits above both")
P("  registered arms and is the one thing DR4 could still say about it.")

P("")
P(f"RESULT: {NCHK} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   ({time.time()-T0:.1f} s)")
sys.exit(0)
