#!/usr/bin/env python3
"""
L42 -- what actually decides between this framework and LambdaCDM?  A ranked forecast.
======================================================================================
Four lanes tonight each removed a source of discriminating power:

  L28  galaxy rotation curves.  The kernel's 0.142 dex is reproduced exactly, but a LambdaCDM
       halo population carrying ITS OWN predicted width (0.25 dex in log M200, 0.11 in log c)
       fits SPARC to 0.085 dex and ties the shape channel 0.070 vs 0.072.  What survives is a
       parsimony-and-prediction claim, NOT a discriminant.
  L24  cluster lensing as a separate probe.  The shortfall against lensing and against dynamics
       agree at 1.55 sigma, so no lensing sector repairs a dynamical shortfall.  It ADDED one
       genuinely new discriminating quantity: the Delta-Sigma log slope, 0.53 +- 0.06 shallower
       at 9 sigma, because the phantom is a near-uniform sheet.
  L21  binary galaxies.  Beyond ~200 kpc the framework's external-field branch and a cosmic-share
       halo are the SAME law, 11.5% apart in velocity, below the stellar M/L systematic.  All
       discriminating power lives on the isolated branch.
  L32  the coefficient.  Total comparison uncertainty 8.0%; nothing in [0.40, 0.66] rejectable at
       3 sigma; 27 simple candidate numbers already inside the band.  kappa is not an observable
       that separates anything.

THE QUESTION THIS LANE ANSWERS.  What is LEFT that can actually decide, at 3 sigma, between this
framework and LambdaCDM -- with honest forecasts against real instruments and real sample sizes,
the binding systematic named for each, and a ranking by discriminating power per unit of effort.

THE ORGANISING PRINCIPLE, and it is the first thing this lane found.  A test has discriminating
power against LambdaCDM only if LambdaCDM predicts something DIFFERENT.  Several of the corpus's
proudest predictions -- alpha_M = 0 and c_T = 1 exactly (EMPIRICAL_TESTS D1, "the strongest
prediction in the corpus"), gamma_PPN = 1 (A4), the CMB spectrum at 0.01 sigma (A3), the binary
pulsar reproducing the GR quadrupole formula (D2) -- are predictions LambdaCDM+GR makes
IDENTICALLY.  They discriminate this framework from OTHER modified-gravity theories.  Against
LambdaCDM their power is exactly zero, and the ledger does not say so.  That is scored below.

WHAT THIS LANE DOES NOT DO.  It does not edit PREREGISTRATION_DR4.md, any *_HASH.txt, FINDINGS.md
or HANDOFF_CONTRACT.md.  Registered numbers are READ from their own source files and reproduced
independently; where a registered prediction is found to be conditional on an unstated assumption
that is REPORTED, not amended.

CHECKS THAT CAN FAIL
  C1..C4  CONTROL -- reproduce registered prediction numbers from their own source files, so the
          ranking is built on verified inputs (PAPER7's LambdaCDM-native rise from Dutton-Maccio
          2014 + E(z); the DR4 frozen error model's own derived quantities; a0 = kappa c sqrt(G
          rho_Lambda)).
  C5..C7  CONTROL -- the 3-sigma forecaster reproduces published forecasts (Amendment 7(d)'s
          N ~ 102,500; PAPER7's "0.13 dex gives 20:1"; the textbook N = (3 sigma/Delta)^2).
  D1..D3  is any live test already decisive with data in hand / with an existing or approved
          facility / at all.
  X1..X4  the DR4 crux: can DR4 produce a result that both rejects Newton at 3 sigma AND leaves
          a Cassini-consistent arm alive?
  P1..P3  is any registered prediction conditional on an unstated assumption?
  V1..V3  the five-year falsifiability verdict, asked separately of the phenomenological arm and
          of the covariant candidate that passes the Solar System.

Both a0 footings throughout: 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.
A FAIL is an obstruction established, not a defect, unless the text says otherwise.
Exit code = number of FAILs.  All paths printed are repository-relative.
"""
import os, re, math, sys, json

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
def rel(p): return os.path.relpath(p, REPO)
def rd(p):
    with open(os.path.join(REPO, p), "r", encoding="utf-8", errors="replace") as f: return f.read()

BAR = "=" * 118
print(BAR); print("L42 -- what actually decides between this framework and LambdaCDM?  A ranked forecast."); print(BAR, flush=True)

A0_CAN, A0_ALT = 9.3619e-11, 1.1279e-10
FOOTINGS = {"canonical": A0_CAN, "alt": A0_ALT}

# ==================================================================================================
# SECTION 0 -- CONTROLS.  Reproduce registered prediction numbers from their own source files.
# ==================================================================================================
print("\n" + BAR); print("SECTION 0 -- CONTROLS: registered numbers reproduced from their own source files"); print(BAR)

PAPER7 = "qwen_claude_field_theory/papers_2026/PAPER7_a0z_decisive_measurement_2026.tex"
PREREG = "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md"
tex, prereg = rd(PAPER7), rd(PREREG)

# ---- C1: PAPER7's LambdaCDM-native rise, recomputed from Dutton-Maccio 2014 + E(z) --------------
OM, H_LITTLE = 0.3150, 0.674
def E_of_z(z, Om=OM):  return math.sqrt(Om*(1+z)**3 + (1-Om))
def c_DM14(M_msun, z, h=H_LITTLE):
    """Dutton & Maccio 2014 (MNRAS 441, 3359) c200c(M,z); M in Msun, their M is in h^-1 Msun."""
    a = 0.520 + (0.905-0.520)*math.exp(-0.617*z**1.21)
    b = -0.101 + 0.026*z
    return 10**(a + b*math.log10(M_msun*h/1e12))
def f_nfw(c): return math.log(1+c) - c/(1+c)
def a_scale_ratio(z, M=1e12):
    """LambdaCDM-native emergent acceleration scale, PAPER7 eq.: E(z)^(4/3) [c^2/f(c)](z)/[c^2/f(c)](0)."""
    c1, c0 = c_DM14(M, z), c_DM14(M, 0.0)
    return E_of_z(z)**(4.0/3.0) * (c1**2/f_nfw(c1)) / (c0**2/f_nfw(c0))

m = re.search(r"by factors \$([\d.]+)\$, \$([\d.]+)\$, \$([\d.]+)\$ and \$([\d.]+)\$", tex)
reg_rise = [float(x) for x in m.groups()] if m else []
my_rise  = [a_scale_ratio(z) for z in (1.0, 2.0, 2.5, 3.25)]
print(f"    source: {PAPER7}")
print(f"    registered rise factors at z = 1, 2, 2.5, 3.25 : {reg_rise}")
print(f"    recomputed (Dutton-Maccio 2014 c(M,z), M = 1e12 Msun, h = {H_LITTLE}, Om = {OM}) : "
      f"{[round(x,3) for x in my_rise]}")
ok_c1 = bool(reg_rise) and all(abs(a-b) <= 0.011 for a, b in zip(reg_rise, my_rise))
check("C1 [CONTROL] PAPER7's four registered LambdaCDM-native rise factors are reproduced independently "
      "from Dutton-Maccio 2014 and E(z)", ok_c1,
      f"max |Delta| = {max(abs(a-b) for a,b in zip(reg_rise,my_rise)):.4f}" if reg_rise else "regex miss")

DEX_LCDM = math.log10(a_scale_ratio(2.5))
reg_dex = 0.33 if "+0.33$ dex" in tex or "$+0.33$" in tex or "0.33" in tex else None
print(f"    zero-point displacement at z = 2.5 : recomputed {DEX_LCDM:+.4f} dex,  registered +0.33 dex")
check("C2 [CONTROL] the registered +0.33 dex LambdaCDM-native BTFR zero-point displacement at z = 2.5 "
      "follows from the same recomputation", abs(DEX_LCDM - 0.33) <= 0.006,
      f"recomputed {DEX_LCDM:+.4f} vs registered +0.33")

# ---- C3: the DR4 frozen error model, its own derived quantities ---------------------------------
_pre_ascii = prereg.replace("σ", "sigma")
mE = re.search(r"sigma_fit = (0\.\d+) at the frozen N = ([\d,]+), sigma_tot = (0\.\d+)", _pre_ascii)
SIG_FIT = float(mE.group(1)) if mE else 0.019      # PARSED, not derived
N0      = int(mE.group(2).replace(",", "")) if mE else 30000
SIG_TOT = float(mE.group(3)) if mE else 0.028      # the preregistration's own (rounded) convention
SIG_SYS = 0.02          # "sigma_sys = 0.02 irreducible", Amendment 7(c)
# NOTE, reported rather than corrected: sqrt(0.019^2 + 0.020^2) = 0.02765, which the document rounds
# to 0.028.  All three are used exactly as the document states them.
mA = re.search(r"canonical \*\*(\d\.\d+)–(\d\.\d+)\*\*, alt \*\*(\d\.\d+)–(\d\.\d+)\*\*", prereg)
ARM_A = {"canonical": (float(mA.group(1)), float(mA.group(2))),
         "alt":       (float(mA.group(3)), float(mA.group(4)))} if mA else \
        {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}
ARM_B = {"canonical": 1.0450, "alt": 1.0300}
for lbl, v in (("1.0450", ARM_B["canonical"]), ("1.0300", ARM_B["alt"])):
    assert lbl in prereg, f"Arm B ceiling {lbl} not found in the preregistration"
GAMMA_MI_A7 = 1.0310    # Amendment 7's in-force signal
print(f"\n    source: {PREREG}")
print(f"    parsed: Arm A band canonical {ARM_A['canonical']}, alt {ARM_A['alt']}; "
      f"Arm B ceilings {ARM_B['canonical']} / {ARM_B['alt']}")
print(f"    parsed: sigma_fit = {SIG_FIT} at N = {N0:,}, sigma_tot = {SIG_TOT}; sigma_sys = {SIG_SYS} (Amdt 7c)")
print(f"    internal consistency of the document's own error model: sqrt({SIG_FIT}^2 + {SIG_SYS}^2) = "
      f"{math.hypot(SIG_FIT, SIG_SYS):.5f}, quoted as {SIG_TOT} (rounding, reported not corrected)")

sep = ARM_A["canonical"][0] - ARM_B["canonical"]
ok_c3 = (abs(sep - 0.1164) < 5e-4 and abs(sep/SIG_TOT - 4.2) < 0.1 and abs(sep/SIG_FIT - 6.1) < 0.15
         and abs(abs(GAMMA_MI_A7 - 1.0)/SIG_SYS - 1.55) < 0.02
         and abs((ARM_A["canonical"][0]-1.0)/SIG_TOT - 5.8) < 0.05)
print(f"    Amendment 11(e) 'ceiling to floor is 0.116 = 4.2 sigma_tot (6.1 sigma_fit)' -> "
      f"recomputed {sep:.4f} = {sep/SIG_TOT:.2f} sigma_tot ({sep/SIG_FIT:.2f} sigma_fit)")
print(f"    Amendment 7(c) 'ceilings at z = 1.55 as N -> inf'            -> recomputed {(GAMMA_MI_A7-1)/SIG_SYS:.3f}")
print(f"    section 1 '5.8 sigma_tot below the canonical band floor'      -> recomputed "
      f"{(ARM_A['canonical'][0]-1.0)/SIG_TOT:.2f}")
check("C3 [CONTROL] four derived quantities of the frozen DR4 error model are reproduced from the parsed "
      "band edges and sigma_sys alone (arm separation 4.2/6.1 sigma; Amdt 7 ceiling 1.55; Arm A vs Newton 5.8)",
      ok_c3, f"sep {sep:.4f}, {sep/SIG_TOT:.2f}/{sep/SIG_FIT:.2f} sigma; ceiling {(GAMMA_MI_A7-1)/SIG_SYS:.2f}; "
             f"A-vs-Newton {(ARM_A['canonical'][0]-1.0)/SIG_TOT:.2f}")

# ---- C4: a0 = kappa c sqrt(G rho_Lambda) ---------------------------------------------------------
c_light, G_N = 2.99792458e8, 6.67430e-11
H0_SI = H_LITTLE*100e3/3.0856775814913673e22
rho_L = (1-OM)*3*H0_SI**2/(8*math.pi*G_N)
a0_from_law = 0.5*c_light*math.sqrt(G_N*rho_L)
print(f"\n    a0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2, Planck-2018 (Om = {OM}, h = {H_LITTLE}) : "
      f"{a0_from_law:.4e} m/s^2   vs canonical footing {A0_CAN:.4e}")
check("C4 [CONTROL] the framework's own headline a0 is reproduced from the law to better than 1%",
      abs(a0_from_law/A0_CAN - 1) < 0.01, f"ratio {a0_from_law/A0_CAN:.4f}")

# ==================================================================================================
# SECTION 0b -- THE FORECASTER, and its controls against published forecasts
# ==================================================================================================
print("\n" + BAR); print("SECTION 0b -- the 3-sigma forecaster, controlled against published forecasts"); print(BAR)

def n_for_nsigma(delta, sig_stat_N0, N0, sig_sys, nsig=3.0):
    """Sample size for nsig separation with a statistical error scaling as 1/sqrt(N) on top of an
    IRREDUCIBLE systematic floor.  Returns (N, reason) with N = None when the floor forbids it."""
    if sig_sys > 0 and delta/sig_sys < nsig:
        return None, f"unreachable at any N: delta/sigma_sys = {delta/sig_sys:.2f} < {nsig}"
    need_tot = delta/nsig
    need_stat = math.sqrt(max(need_tot**2 - sig_sys**2, 0.0))
    if need_stat <= 0: return None, "unreachable: systematic floor equals the requirement"
    return N0*(sig_stat_N0/need_stat)**2, ""

def odds_two_points(delta, sigma):
    """Likelihood ratio between two point hypotheses separated by delta, measurement at one of them."""
    return math.exp(0.5*(delta/sigma)**2)

# control C5 -- Amendment 7(d): "Redone statistical-only at the in-force signal it is N ~ 102,500"
N_stat, _ = n_for_nsigma(GAMMA_MI_A7-1.0, SIG_FIT, N0, sig_sys=0.0, nsig=3.0)
print(f"    Amendment 7(d) 'statistical-only 3 sigma needs N ~ 102,500' -> forecaster returns N = {N_stat:,.0f} "
      f"(from sigma_fit = {SIG_FIT:.4f} at N = {N0:,}, signal {GAMMA_MI_A7-1:.4f})")
check("C5 [CONTROL] the forecaster reproduces the preregistration's own published statistical-only "
      "3-sigma sample size, N ~ 102,500", abs(N_stat/102500 - 1) < 0.02, f"N = {N_stat:,.0f}")

# control C6 -- PAPER7: "a required total uncertainty of 0.13 dex, which gives 20:1 discrimination"
o = odds_two_points(0.33, 0.13)
print(f"    PAPER7 'total uncertainty 0.13 dex gives 20:1 discrimination' -> forecaster returns "
      f"{o:.1f}:1  ({0.33/0.13:.2f} sigma)")
check("C6 [CONTROL] the forecaster reproduces PAPER7's published 20:1 odds at 0.13 dex "
      "(and shows it is 2.54 sigma frequentist, not 3)", o >= 20.0 and abs(0.33/0.13 - 2.538) < 0.01,
      f"odds {o:.1f}:1, {0.33/0.13:.3f} sigma")

# control C7 -- textbook
N_tb, _ = n_for_nsigma(0.5, 1.0, 1, sig_sys=0.0, nsig=3.0)
check("C7 [CONTROL] the forecaster returns the textbook N = (3 sigma_pop/Delta)^2 = 36 for a half-sigma "
      "mean shift", abs(N_tb - 36) < 1e-6, f"N = {N_tb:.1f}")

# ==================================================================================================
# SECTION 1 -- THE REGISTER OF LIVE TESTS
# ==================================================================================================
print("\n" + BAR); print("SECTION 1 -- the register: what the framework predicts, what LambdaCDM predicts, "
                        "and the precision to separate them at 3 sigma"); print(BAR)

# Each entry:  key, name, framework prediction, LambdaCDM prediction, separation per footing,
#              achieved sigma per footing, systematic floor, N0/sig_stat scaling if any,
#              status letter, effort 0..5, binding systematic + its size, source.
TESTS = []
def T(**kw):
    kw.setdefault("power_cap", None); kw.setdefault("cap_why", ""); kw.setdefault("flag", "")
    kw.setdefault("lever", "N"); kw.setdefault("note", "")
    TESTS.append(kw)

T(key="T1", name="Gaia DR4 wide binaries, Arm A (frozen phenomenological band)",
  fw="gamma_v in 1.1614-1.1814 (can) / 1.1917-1.2267 (alt)", lcdm="1.0000 exactly (Newtonian; the local "
     "dark density contributes <1e-6 of a two-body force at 10 kAU)",
  sep={"canonical": ARM_A["canonical"][0]-1.0, "alt": ARM_A["alt"][0]-1.0},
  sig={"canonical": SIG_TOT, "alt": SIG_TOT}, sig_sys=SIG_SYS, N0=N0, sig_stat_N0=SIG_FIT,
  status="b", effort=1, when="Gaia DR4, scheduled ~Dec 2026; pipeline frozen and hash-stamped",
  flag="scheduled",
  syst="sigma_sys = 0.020 in gamma_v, irreducible in the frozen model (undetected hierarchical/triple "
       "companions and the eccentricity distribution). 12% of the signal; NOT binding here -- the "
       "floor-only ceiling is 8.1 sigma canonical / 9.6 sigma alt.",
  src=PREREG)

T(key="T2", name="Gaia DR4 wide binaries, Arm B (the covariant candidate that passes Cassini)",
  fw="1.000 < gamma_v <= 1.0450 (can) / <= 1.0300 (alt) -- CEILINGS, killable only from above",
  lcdm="1.0000 exactly",
  sep={"canonical": ARM_B["canonical"]-1.0, "alt": ARM_B["alt"]-1.0},
  sig={"canonical": SIG_TOT, "alt": SIG_TOT}, sig_sys=SIG_SYS, N0=N0, sig_stat_N0=SIG_FIT,
  status="c", effort=1, when="Gaia DR4 -- but see the forecast: no N suffices",
  flag="one-sided",
  syst="the SAME sigma_sys = 0.020 floor, which alone caps the separation from Newton at 2.25 sigma "
       "(can) / 1.50 sigma (alt) at INFINITE N.  This is the whole story of the test.",
  src=PREREG)

T(key="T3", name="Deep-MOND baryonic Tully-Fisher zero point at z = 2.5",
  fw="Delta_BTFR = 0.00 dex (-0.09 with DESI w0wa) on the rho_Lambda tie; -0.576 dex on the "
     "Hubble-horizon tie -- SEE THE CONDITIONALITY AUDIT",
  lcdm="+0.33 dex (Dutton-Maccio 2014), +0.45 (Duffy 2008), ~+0.50 (Magneticum apparent)",
  sep={"canonical": DEX_LCDM, "alt": DEX_LCDM}, sig={"canonical": 0.13, "alt": 0.13},
  sig_sys=0.07, N0=1, sig_stat_N0=math.sqrt(0.13**2 - 0.07**2), status="b", effort=3, lever="N",
  note="PAPER7 registers a TOTAL 0.13 dex and does not decompose it into the part that averages down "
       "over several objects and the part that does not.  This lane splits it: the coherent floor is "
       "the frozen local zero point C0 plus the shared stellar-M/L and alpha_CO prescriptions, taken "
       "here as 0.07 dex; the rest (velocity, inclination, lens model, S/N) is per-object.  THE "
       "DECOMPOSITION IS THIS LANE'S ESTIMATE, NOT THE PAPER'S, and the gap is flagged: it decides "
       "whether a second qualifying object helps, and the paper does not say.",
  when="JWST NIRSpec IFU G235H/F170LP (1.66-3.17 um; H-alpha + [OIII] in one setting for 2.32<z<3.83) "
       "then ALMA Band 3 CO(3-2) (84-116 GHz => 1.98<z<3.12).  Both instruments exist and operate.  "
       "N = ONE object -- IF it passes the gates.  The committed 21-object ledger contains NONE.",
  flag="NO TARGET",
  syst="the apparent-a0 drift nuisance.  Magneticum calibrates p = 0.92, MSA-3D's own decomposition "
       "MEASURES an apparent component p = 1.22 in a real JWST sample.  At z = 2.5 that is "
       "+0.50 to +0.67 dex -- LARGER than the 0.33 dex signal.  It is neutralised only by a genuinely "
       "deep-MOND (g_bar < 0.3 a0), rotation-dominated, lens-controlled target, which is exactly why "
       "the binding item is target DISCOVERY, not telescope time.  Second: lens magnification "
       "(two refereed models of the best current object disagree by 2.3x = 0.36 dex).",
  src=PAPER7)

T(key="T4", name="Cluster weak-lensing Delta-Sigma log-slope (L24's new quantity)",
  fw="log-slope 0.531 +- 0.058 (can) / 0.536 +- 0.058 (alt) SHALLOWER than measured -- the phantom "
     "is a near-uniform sheet",
  lcdm="the measured NFW/Einasto slope, which the data already match by construction",
  sep={"canonical": 0.531, "alt": 0.536}, sig={"canonical": 0.058, "alt": 0.058},
  sig_sys=0.058, N0=5, sig_stat_N0=0.058, status="a", effort=0,
  when="ALREADY MEASURED -- five X-COP clusters with published weak lensing, data in hand",
  flag="not novel",
  syst="sample size (5 clusters, per-cluster mass errors 20-60%) and miscentering.  NOT binding: "
       "control C10 pushes the MEASURED X-ray profile through the identical machinery and recovers "
       "the measured Delta-Sigma to a median 1.11, so even a 3x inflation of the error leaves 3.1 sigma. "
       "The honest caveat is that a lensing-sector slip below ~15% is untested rather than excluded.",
  src="fable_independent_2026/L24_lensing_vs_dynamics.out")

T(key="T5", name="Cluster residual vs the cosmic dark-to-baryon share",
  fw="M_resid/M_bar = 0 after its own kernel", lcdm="Omega_dm/Omega_b = 5.43, fixed independently by "
     "CMB + BBN, universal across clusters",
  sep={"canonical": 3.09, "alt": 2.76}, sig={"canonical": 3.09/15.0, "alt": 2.76/13.0},
  sig_sys=3.09/15.0, N0=12, sig_stat_N0=3.09/15.0, status="a", effort=0,
  when="ALREADY MEASURED -- twelve X-COP clusters at 0.80 R500, data in hand",
  syst="hydrostatic mass bias b.  L18 measured it and it moves the Newtonian ratio 5.73 -> 9.04 over "
       "b in [0, 0.33] -- i.e. the systematic STRENGTHENS the residual against the framework's zero. "
       "It cannot rescue.  (L7's separate '5% agreement with the cosmic ratio' headline is withdrawn.)",
  src="fable_independent_2026/L7_cosmic_ratio.out")

T(key="T6", name="Binary galaxies on the ISOLATED branch (L21)",
  fw="isolated deep-MOND A = 1.802 +- 0.041 (can) / 1.731 (alt); parameter-free sigma_los = "
     "0.60679 (G m a0)^(1/4) = 107.7 / 112.9 km/s at ANY separation",
  lcdm="abundance-matched halo A = 0.967 +- 0.024 (1.4 sigma from unity)",
  sep={"canonical": 1.802-0.967, "alt": 1.731-0.967}, sig={"canonical": 0.048, "alt": 0.048},
  sig_sys=0.24, N0=1900, sig_stat_N0=0.041, status="b", effort=1,
  when="DATA ALREADY PUBLIC.  1900 isolated 2MRS major pairs in hand; 3 sigma needs 384 pairs at "
       "40 km/s, 122 at 10 km/s, or 65 on the shape axis.  The FIX is a deeper spectroscopic parent "
       "catalogue: DESI DR1 (~13 million extragalactic redshifts, public) against 2MRS (~45,000, "
       "K < 11.75).  No new observations required.",
  flag="cheapest gain",
  syst="ISOLATION DEPTH, and it is large.  2MRS sees companions only above ~23% of the pair's mass, "
       "and the amplitude falls 1.99 -> 1.51 as the isolation deepens over the accessible range -- a "
       "0.48 swing against a 0.835 framework-vs-LambdaCDM separation, i.e. 57% of the signal. Every "
       "published A is an UPPER limit.  Statistics were never the limitation.",
  src="fable_independent_2026/L21_binary_galaxies.out")

T(key="T7", name="Coma ultra-diffuse galaxies (L23's corrected row)",
  fw="the EFE-dominated prediction; measured dispersions sit +1.159 dex (can) / +1.112 (alt) above it, "
     "a factor 14.4 in acceleration",
  lcdm="no prediction violated -- UDGs in a cluster carry halos",
  sep={"canonical": 1.159, "alt": 1.112},
  sig={"canonical": math.hypot(0.227, 0.062), "alt": math.hypot(0.227, 0.062)},
  sig_sys=0.227, N0=11, sig_stat_N0=0.062, status="b", effort=3, lever="precision",
  when="ALREADY 4.9 sigma (can) / 4.7 (alt) ON THE EQUILIBRIUM HYPOTHESIS; 2.7 sigma on first infall. "
       "Settling it needs (i) M/L to ~0.05 dex from IMF-sensitive resolved stellar populations and "
       "(ii) an independent equilibrium diagnostic.  ~10 objects x 30 hr of 8-10 m spectroscopy "
       "(DF44 alone took 33.3 hr of Keck/KCWI) plus JWST/HST imaging for tidal state.",
  power_cap=2.7, cap_why="the first-infall hypothesis, which the field's own MOND simulations "
      "endorse, drops the row to 2.7 sigma; the equilibrium reading alone gives 4.9",
  flag="state ambiguous",
  syst="stellar M/L and IMF at 0.148 dex, UNPROPAGATED by the source paper, dominating a 0.227 dex "
       "coherent floor that does not average down over the eleven galaxies.  AND the dynamical-state "
       "assumption, worth 2.2 of the 4.9 sigma by itself.",
  src="fable_independent_2026/L23_udg_verify.out")

T(key="T8", name="s^TX SME boost dipole from planetary ephemerides",
  fw="|s^TX| = 8.68e-10 (can) / 1.048e-9 (alt), sign locked NEGATIVE",
  lcdm="s^TX = 0 exactly (GR has no preferred frame)",
  sep={"canonical": 8.68e-10, "alt": 1.048e-9}, sig={"canonical": 1.3e-9, "alt": 1.3e-9},
  sig_sys=0.0, N0=1, sig_stat_N0=1.3e-9, status="b", effort=2, lever="precision",
  when="no new hardware.  Needs sigma(s^TX) <= 2.89e-10, a factor 4.5 on the published combined "
       "multi-planet fit (-0.2 +- 1.3)e-9 (Hees et al. 2016).  Route stated in the preregistration: "
       "INPOP/DE refits absorbing Gaia DR4 asteroid astrometry, plus BepiColombo-era Mercury ranging. "
       "The programme cannot do this alone -- it needs an ephemeris team to run the frozen template.",
  flag="needs a team",
  syst="ABSORPTION into the ephemeris global fit.  At the preregistration's own conservative level "
       "94.3% of the template is absorbed by 6 Saturn ICs + 6 EMB ICs + GM_sun + bias + drift, and a "
       "real INPOP/DE refit absorbs MORE -- so every quoted sensitivity is an upper limit.  Second: "
       "the interpretation guard -- any preferred-frame MG host gives a comparable s^TX, so a "
       "detection is a Lorentz-violation verdict shared across the MOND family.",
  src=PREREG)

T(key="T9", name="Linear structure formation without cold dark matter (P(k), sigma_8)",
  fw="best computed case sigma_8 <= 0.648, rms |log R| >= 0.94 dex over 0.1-1 h/Mpc at ANY |K_2|",
  lcdm="sigma_8 = 0.810, R(k) = 1",
  sep={"canonical": 0.810-0.648, "alt": 0.810-0.648}, sig={"canonical": 0.010, "alt": 0.010},
  sig_sys=0.010, N0=1, sig_stat_N0=0.010, status="a", effort=0, lever="precision",
  when="ALREADY DECISIVE against every computed variant, data in hand (sigma_8 = 0.81 +- 0.01)",
  flag="LOOPHOLE",
  syst="none observational.  The binding limit is a MISSING CALCULATION on the theory side: the "
       "nonlinear top-down fragmentation loophole is uncomputed, not excluded, and the linear result "
       "was obtained for the thermal-relic sector that is separately dead.  Effort to close it is "
       "theoretical (an N-body/hydro calculation), not observational.",
  src="qwen_claude_field_theory/closure_2026/g04h_pk_regeneration_causal_boost.out")

T(key="T10", name="a0(z) from the Rubin/LSST supernova stream",
  fw="R(z=3) = 0.775 on the DESI DR2 w0wa posterior; R = 1.000 if Lambda is a true constant",
  lcdm="R = 1.000",
  sep={"canonical": 1.0-0.775, "alt": 1.0-0.775}, sig={"canonical": 0.225/2.0, "alt": 0.225/2.0},
  sig_sys=0.225/4.7, N0=1, sig_stat_N0=0.225/2.0, status="c", effort=2, lever="precision",
  when="Rubin/LSST operating; 2.0 sigma at z = 3 on the DESI DR2 posterior, 4.7 sigma at z >= 2 on a "
       "tight SN+CMB/BAO forecast covariance",
  flag="measures w, not a0",
  syst="the test is not about a0 at all.  The programme's OWN preregistration warns that z = 3 is a "
       "lever arm, not a redshift where calibrated SNe exist, and that R(z=3) must not be read as a "
       "measured acceleration scale.  What is actually measured is whether w = -1.  If w = -1 the "
       "framework becomes EXACTLY degenerate with constant-a0 MOND and with flat; if w != -1 the "
       "framework merely inherits a dark-energy measurement.  Either way it separates nothing.",
  src="prep_2026/rubin_prereg/RUBIN_PREREG_2026.md")

T(key="T11", name="Directional external-field effect in wide binaries",
  fw="AQUAL-class directional signal; the kill switch has fired once, A-hat = +2.95, p = 0.029",
  lcdm="exactly zero (as does pure MI -- this is an MI-vs-MG discriminator first)",
  sep={"canonical": 2.95, "alt": 2.95}, sig={"canonical": 2.95/2.19, "alt": 2.95/2.19},
  sig_sys=0.0, N0=1157, sig_stat_N0=2.95/2.19, status="b", effort=1,
  when="needs N ~ 1157 at maximum clustering; Gaia DR4 supplies it",
  flag="no syst budget",
  syst="the same contamination and isolation systematics as T1/T6, and they are UNQUANTIFIED on this "
       "axis -- the 2.2 sigma hint has no systematic budget at all.  Until it has one the forecast "
       "is statistics-only and should not be relied on.",
  src="prep_2026/l1_bvp/l1_bvp.py")

T(key="T12", name="alpha_M and c_T from LISA / Einstein Telescope standard sirens",
  fw="alpha_M = 0 and c_T = 1 EXACTLY, for any free function, any K_B, both footings",
  lcdm="alpha_M = 0 and c_T = 1 EXACTLY",
  sep={"canonical": 0.0, "alt": 0.0}, sig={"canonical": 1.0, "alt": 1.0},
  sig_sys=0.0, N0=1, sig_stat_N0=1.0, status="c", effort=5, lever="none",
  when="LISA ~2035, ET ~2035+",
  flag="SHARED with LCDM",
  syst="NOT A SYSTEMATIC -- a degeneracy.  The ledger calls this 'the strongest prediction in the "
       "corpus' and it is, against other modified-gravity theories.  Against LambdaCDM the two "
       "predictions are IDENTICAL, so its discriminating power in THIS comparison is exactly zero, "
       "at any precision, from any facility.",
  src="EMPIRICAL_TESTS.md")

T(key="T13", name="the coefficient kappa",
  fw="kappa = 1/2 (fitted, and shown underivable by the candidate action)",
  lcdm="LambdaCDM has no kappa -- there is no competing prediction to separate from",
  sep={"canonical": 0.0, "alt": 0.0}, sig={"canonical": 0.037, "alt": 0.037},
  sig_sys=0.5*0.038, N0=1, sig_stat_N0=0.5*0.071, status="c", effort=5, lever="none",
  when="never, as a framework-vs-LambdaCDM test",
  flag="no LCDM rival",
  syst="the H0-convention systematic, 3.8% against a 7.1% statistical error => 8.0% total.  Nothing "
       "in [0.40, 0.66] is rejectable at 3 sigma and 27 simple 'principle-shaped' numbers already sit "
       "inside the band.  Landing in the band is not evidence.",
  src="fable_independent_2026/L32_kappa_necessary.out")

T(key="T14", name="SPARC rotation-curve tightness",
  fw="0.142 dex at zero parameters per galaxy",
  lcdm="0.085 dex from a fitted NFW halo whose population carries LambdaCDM's OWN width "
       "(0.25 dex in log M200, 0.11 in log c); shape channel tied 0.070 vs 0.072",
  sep={"canonical": 0.0, "alt": 0.0}, sig={"canonical": 0.005, "alt": 0.005},
  sig_sys=0.005, N0=175, sig_stat_N0=0.005, status="c", effort=4, lever="none",
  when="removed as a discriminant by L28",
  flag="removed by L28",
  syst="the halo POPULATION WIDTH.  A prior-shrink scan shows the naive prior-constrained fit reaches "
       "0.066 only by landing on a population 1.7-1.8x wider than LambdaCDM's; shrunk to LambdaCDM's "
       "own width it is 0.082-0.085 -- still tighter than the kernel.  What survives is parsimony "
       "(zero parameters vs two) and held-out prediction, not a discriminant.",
  src="fable_independent_2026/L28_tightness.out")

# ---- print the register --------------------------------------------------------------------------
print(f"\n  {'key':<5} {'test':<58} {'sep/sigma (can)':>16} {'sep/sigma (alt)':>16} {'3-sig sigma req':>16}")
print("  " + "-"*116)
for t in TESTS:
    zc = t["sep"]["canonical"]/t["sig"]["canonical"] if t["sig"]["canonical"] else 0.0
    za = t["sep"]["alt"]/t["sig"]["alt"] if t["sig"]["alt"] else 0.0
    req = t["sep"]["canonical"]/3.0
    t["z_can"], t["z_alt"] = zc, za
    t["req_sigma"] = req
    reqs = f"{req:.4g}" if req > 0 else "n/a (no gap)"
    print(f"  {t['key']:<5} {t['name'][:58]:<58} {zc:>16.2f} {za:>16.2f} {reqs:>16}")

# ==================================================================================================
# SECTION 2 -- THE HONEST FORECAST
# ==================================================================================================
print("\n" + BAR); print("SECTION 2 -- the forecast: (a) already achieved, (b) achievable with an existing "
                        "or approved facility, (c) not achievable"); print(BAR)
for t in TESTS:
    d, ss = t["sep"]["canonical"], t["sig_sys"]
    N, why = n_for_nsigma(d, t["sig_stat_N0"], t["N0"], ss, 3.0)
    achieved = max(t["z_can"], t["z_alt"]) >= 3.0
    t["achieved_3sig"] = achieved
    t["N_for_3sig"] = N
    ceiling = (d/ss) if ss > 0 else float("inf")
    t["floor_ceiling"] = ceiling
    print(f"\n  {t['key']}  {t['name']}")
    print(f"       framework : {t['fw']}")
    print(f"       LambdaCDM : {t['lcdm']}")
    print(f"       separation {d:.4g} ; 3-sigma needs sigma <= {d/3.0:.4g} ; achieved "
          f"{t['sig']['canonical']:.4g} => {t['z_can']:.2f} sigma (can) / {t['z_alt']:.2f} (alt)")
    if ss > 0:
        print(f"       systematic floor {ss:.4g} => ceiling {ceiling:.2f} sigma at INFINITE sample size")
    if t["lever"] == "none" or d <= 0:
        print(f"       3-sigma requirement : NONE EXISTS -- there is no gap between the two predictions "
              f"to resolve, at any precision, from any facility")
    elif N is None and ss > 0 and ceiling < 3.0:
        print(f"       3-sigma sample size : IMPOSSIBLE -- {why}")
    elif t["lever"] == "precision":
        print(f"       3-sigma requirement : the lever is PRECISION, not sample size -- a factor "
              f"{t['sig']['canonical']/(d/3.0):.2f} improvement on the achieved "
              f"{t['sig']['canonical']:.4g}"
              + ("  ** already achieved **" if t["sig"]["canonical"] <= d/3.0 else ""))
    elif N is not None:
        print(f"       3-sigma sample size : N = {max(N,1):,.0f} (have {t['N0']:,})"
              + ("  ** already sufficient **" if N <= t["N0"] else ""))
    if t["note"]:
        print("       NOTE       : " + t["note"][:104])
        for ln in [t["note"][i:i+104] for i in range(104, len(t["note"]), 104)]:
            print("                    " + ln)
    if t["power_cap"] is not None:
        print(f"       MODEL CAP  : {t['power_cap']:.2f} sigma -- {t['cap_why']}")
    print(f"       STATUS ({t['status']}) : {t['when']}")

# ==================================================================================================
# SECTION 3 -- THE BINDING SYSTEMATIC
# ==================================================================================================
print("\n" + BAR); print("SECTION 3 -- the systematic that binds each test, and how large it is"); print(BAR)
for t in TESTS:
    print(f"\n  {t['key']}  {t['name']}")
    for line in [t["syst"][i:i+108] for i in range(0, len(t["syst"]), 108)]:
        print(f"       {line}")

# ==================================================================================================
# SECTION 4 -- THE DR4 CRUX
# ==================================================================================================
print("\n" + BAR); print("SECTION 4 -- the DR4 crux: can DR4 reject Newton at 3 sigma AND leave a "
                        "Cassini-consistent arm alive?"); print(BAR)
print("""
  The two registered arms are not on the same footing with respect to the Solar System.
    Arm A -- the frozen phenomenological band -- is the SAME kernel taken as strict AQUAL modified
      gravity with no coherence length, and roadmap gate G01 (two independent solvers agreeing to
      0.05%) has it failing the Cassini quadrupole by 4-5x.
    Arm B -- the covariant candidate -- passes the static Solar-System gates precisely BECAUSE it
      carries a coherence length at or above the Cassini floor (0.10 pc canonical / 0.15 pc alt),
      and that same length is what lowers the wide-binary boost from A's band to B's ceiling.
  So the question is not 'which arm wins' but 'is there any gamma_v that both kills Newton and is
  consistent with a version of the framework the Solar System permits?'
""")
def Phi(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))
for foot in ("canonical", "alt"):
    ceil_B = ARM_B[foot]
    lo = 1.0 + 3.0*SIG_TOT                 # Newton rejected at 3 sigma_tot
    hi = ceil_B + 3.0*SIG_TOT              # Arm B not yet falsified (prereg's own >3 sigma_tot rule)
    width = max(hi-lo, 0.0)
    # probability of landing in that window if the truth sits at Arm B's most favourable point,
    # its ceiling (any smaller boost, i.e. larger xi, makes it strictly worse)
    p = Phi((hi-ceil_B)/SIG_TOT) - Phi((lo-ceil_B)/SIG_TOT) if width > 0 else 0.0
    print(f"    {foot:<10}: Newton dead at gamma_v >= {lo:.4f}; Arm B alive up to gamma_v <= {hi:.4f} "
          f"=> window width {width:.4f} = {width/SIG_TOT:.2f} sigma_tot")
    print(f"    {'':<10}  P(landing in it | truth AT Arm B's ceiling {ceil_B:.4f}, its best case) = {100*p:.1f}%")
    if foot == "canonical": P_WINDOW_CAN = p
    else: P_WINDOW_ALT = p
check("X1 the DR4 window in which Newton is rejected at 3 sigma AND the Cassini-consistent arm survives "
      "is narrow, and unlikely even at Arm B's most favourable point",
      P_WINDOW_CAN < 0.15 and P_WINDOW_ALT < 0.15,
      f"P = {100*P_WINDOW_CAN:.1f}% canonical / {100*P_WINDOW_ALT:.1f}% alt")
check("X2 Arm B can be separated from Newton at 3 sigma at SOME sample size (this FAILS: the frozen "
      "sigma_sys = 0.020 caps it at 2.25 sigma canonical / 1.50 sigma alt at infinite N)",
      (ARM_B["canonical"]-1.0)/SIG_SYS >= 3.0 and (ARM_B["alt"]-1.0)/SIG_SYS >= 3.0,
      f"ceilings {(ARM_B['canonical']-1)/SIG_SYS:.2f} / {(ARM_B['alt']-1)/SIG_SYS:.2f} sigma")
# Amendment 11(e)'s own stated route to confirming B
sig_tot_4x = math.hypot(SIG_FIT/2.0, SIG_SYS)
print(f"\n    Amendment 11(e) states confirming Arm B at 3 sigma_tot 'needs sigma_tot <= 0.015 (about four "
      f"times the frozen N\n    at unchanged systematics, or DR5)'.  Four times the frozen N gives "
      f"sigma_fit = {SIG_FIT/2:.4f} and sigma_tot = {sig_tot_4x:.4f},\n    which is {sig_tot_4x/0.015:.1f}x the "
      f"stated requirement: sigma_tot >= sigma_sys = {SIG_SYS} by construction, so NO N reaches 0.015.")
check("X3 Amendment 11(e)'s stated route to confirming Arm B ('about four times the frozen N at unchanged "
      "systematics') reaches sigma_tot <= 0.015 (this FAILS: sigma_tot >= sigma_sys = 0.020 at any N; "
      "the systematic itself must be reduced, and the amendment does not say so)",
      sig_tot_4x <= 0.015, f"4x N gives sigma_tot = {sig_tot_4x:.4f}, floor {SIG_SYS}")
newton_kills_B = min((ARM_B[f]-1.0)/SIG_TOT for f in ARM_B) >= 3.0
check("X4 a Newtonian DR4 result would be evidence against the framework as a whole (this FAILS: it "
      "falsifies Arm A at >= 5.8 sigma_tot and leaves Arm B -- the arm the Solar System permits -- "
      "untouched, because Arm B's Newtonian limit is reached by raising xi above its floor)",
      newton_kills_B, f"gamma-hat = 1.000 sits {(ARM_B['canonical']-1)/SIG_TOT:.2f} sigma_tot from Arm B's "
      f"canonical ceiling and {(ARM_A['canonical'][0]-1)/SIG_TOT:.2f} from Arm A's floor")

# ==================================================================================================
# SECTION 5 -- CONDITIONALITY AUDIT OF THE REGISTERED PREDICTIONS
# ==================================================================================================
print("\n" + BAR); print("SECTION 5 -- is any registered prediction conditional on an unstated assumption?"); print(BAR)

fork_src = "prep_2026/a0z_crossscale/desitter_unruh_horizon_fork_2026.py"
fork = rd(fork_src)
posit_stated = "is a POSIT" in fork
paper7_mentions_hubble = ("Hubble horizon" in tex) or ("McCulloch" in tex) or ("MiHsC" in tex)
delta_branchB = math.log10(E_of_z(2.5))
print(f"""
  P1 -- PAPER7's Delta_BTFR^framework = 0.00 dex at z = 2.5.
       The paper states the law a0 = kappa c sqrt(G rho_Lambda) and carries the DESI w0wa alternative
       (-0.09 dex).  It does NOT state that WHICH HORIZON sources a0 is an open posit.  The repository's
       own {rel(os.path.join(REPO, fork_src))}
       says verbatim that the horizon choice 'is a POSIT'  -> {posit_stated}
       and carries a second reading, a0(z)/a0(0) = H(z)/H0 (the Hubble/apparent horizon, credited to
       McCulloch), which at z = 2.5 gives Delta log a0 = {delta_branchB:+.3f} dex, i.e. a BTFR zero point
       displaced {delta_branchB:.3f} dex the OTHER way from LambdaCDM's +0.33.
       PAPER7 mentions that reading anywhere in its text -> {paper7_mentions_hubble}
       CONSEQUENCE, and it is the serious part: PAPER7's scoring rule says a result inconsistent with
       both 0.00 and +0.33 'counts against both'.  A measurement at -0.58 dex would therefore be scored
       as falsifying the framework when it is EXACTLY what the framework's other horizon reading
       predicts.  The registered number is conditional on a choice the programme has not made in the
       paper.  (STANDING.md section 4 lists 'a rising a0 ~ H(z) with no dark field' among doors shut,
       while L32's N7 and the fork script both still carry it as live -- the corpus is internally
       inconsistent about whether the branch is closed, which is precisely why the paper must state it.)
       SEPARATION AT STAKE: {abs(delta_branchB):.3f} dex = {abs(delta_branchB)/0.13:.1f}x PAPER7's own required
       total uncertainty of 0.13 dex, and {abs(delta_branchB)/DEX_LCDM:.2f}x the LambdaCDM separation the
       measurement is designed to resolve.
""")
check("P1 PAPER7's registered 0.00 dex is NOT conditional on an unstated assumption (this FAILS: the "
      "horizon choice is a posit by the repository's own script, the alternative reading moves the "
      "registered number by 0.576 dex, and the paper never names it)",
      (not posit_stated) or paper7_mentions_hubble,
      f"posit stated in the fork script = {posit_stated}; PAPER7 names the alternative = {paper7_mentions_hubble}")

l29_shift = (0.38, 0.54)
print(f"""  P2 -- a0 = kappa c sqrt(G rho_Lambda): WHICH G, and WHICH rho_Lambda.
       L29 found that L9's own closure 1 = F(Om + Or + OLambda) drives omega_Lambda down by a factor
       {l29_shift[0]}-{l29_shift[1]}, moving a0 by -38% to -27% if the G in the law is the LOCAL one and by
       -17% to -5% if it is the cosmological F G0.  Which G enters is NOT settled and both are carried.
       That is a {100*(1-math.sqrt(l29_shift[1])):.0f}-{100*(1-math.sqrt(l29_shift[0])):.0f}% ambiguity in the framework's
       central formula, against a 9.47% BTFR floor on kappa and DR4's 21% reach.  It does not change a
       RATIO like Delta_BTFR, so it does not touch the a0(z) registration -- but any registered
       prediction quoted in ABSOLUTE a0 inherits it.
""")
check("P2 the absolute normalisation of a0 in the framework's own law is unambiguous (this FAILS: the "
      "G entering a0 = kappa c sqrt(G rho_Lambda) is unsettled and the two readings differ by up to 38% "
      "under the programme's own late-time closure)", False, "L29: -38% to -27% vs -17% to -5%")

exp_carrier_B = (1.0375, 1.0275)
kernel_spread = ARM_B["canonical"] - exp_carrier_B[0]
print(f"""  P3 -- Arm A's band and the unresolved kernel conflict (D1).
       Amendment 11 registers Arm B for BOTH carriers -- nu_RAR {ARM_B['canonical']:.4f} / {ARM_B['alt']:.4f} and the
       superseded exponential {exp_carrier_B[0]:.4f} / {exp_carrier_B[1]:.4f} -- a spread of {kernel_spread:.4f} =
       {kernel_spread/SIG_TOT:.2f} sigma_tot, and it says which is in force.  That is GOOD PRACTICE and is
       credited here.  Arm A's band carries no such dual number, and L28 independently found the two
       carriers differ by up to 0.073 dex on SPARC and change its own margin from 1.20x to 1.06x.  Arm A
       is therefore registered for one kernel with no stated sensitivity to the conflict the corpus is
       still carrying.  This is a documentation gap, {kernel_spread/SIG_TOT:.2f} sigma_tot in size on the
       comparable arm -- much smaller than P1, and it is flagged rather than scored as a defect.
""")
check("P3 Amendment 11 registers Arm B for both candidate kernels and names which is in force, so the "
      "kernel conflict is disclosed on that arm", ARM_B["canonical"] in (1.0450,) and "exponential carrier" in prereg,
      f"nu_RAR {ARM_B['canonical']} in force; exponential {exp_carrier_B[0]} recorded, spread "
      f"{kernel_spread/SIG_TOT:.2f} sigma_tot")

# ==================================================================================================
# SECTION 6 -- SHARED PREDICTIONS: where the power is exactly zero
# ==================================================================================================
print("\n" + BAR); print("SECTION 6 -- predictions the framework SHARES with LambdaCDM (power exactly zero)"); print(BAR)
SHARED = [
    ("D1  alpha_M = 0, c_T = 1 from standard sirens", "the ledger's 'strongest prediction in the corpus'"),
    ("A6  GW speed |c_T - 1| < 1e-15 (GW170817)",     "already measured; GR predicts it identically"),
    ("A4  gamma_PPN = 1",                             "GR predicts it identically"),
    ("A3  CMB power spectrum at 0.01 sigma",          "matched by construction to LambdaCDM's own spectrum"),
    ("A7/D3  no Solar-System MOND signal",            "GR predicts none either"),
    ("D2  binary-pulsar GR quadrupole decay",         "GR predicts it identically"),
]
for k, why in SHARED: print(f"    {k:<48} -- {why}")
print(f"\n    {len(SHARED)} of the ledger's flagged strengths and future tests predict EXACTLY what "
      f"LambdaCDM+GR predicts.\n    They separate this framework from other modified-gravity theories.  "
      f"Against LambdaCDM their\n    discriminating power is zero at any precision from any facility, and "
      f"EMPIRICAL_TESTS.md does not say so.")
check("S1 the corpus's ledger flags which of its 'strongest predictions' are shared with LambdaCDM and "
      "therefore carry zero power in that comparison (this FAILS: six do not carry the flag, including "
      "D1, which the ledger calls the strongest prediction in the corpus)",
      "shared with" in rd("EMPIRICAL_TESTS.md").lower() and "zero discriminating" in rd("EMPIRICAL_TESTS.md").lower(),
      f"{len(SHARED)} shared predictions carry no such flag")

# ==================================================================================================
# SECTION 7 -- THE RANKING
# ==================================================================================================
print("\n" + BAR); print("SECTION 7 -- ranked by discriminating power per unit of effort"); print(BAR)
EFFORT_LABEL = {0: "0  data in hand", 1: "1  data scheduled or public, no new observations",
                2: "2  no new hardware, needs an external team", 3: "3  large approved-facility programme",
                4: "4  a survey or sample nobody has", 5: "5  a facility nobody is building"}
for t in TESTS:
    power = min(max(t["z_can"], t["z_alt"]), t["floor_ceiling"])
    if t["power_cap"] is not None: power = min(power, t["power_cap"])
    t["power"] = power
    t["score"] = power/(1.0 + t["effort"])
    t["decisive"] = power >= 3.0
RANK = sorted(TESTS, key=lambda t: (-int(t["decisive"]), -t["score"], t["effort"]))
print(f"\n  {'#':<3} {'key':<5} {'test':<46} {'power':>7} {'effort':>7} {'score':>7} {'status':>7} "
      f"{'direction':>11} {'flag':>17}")
print("  " + "-"*116)
DIRECTION = {"T1": "forward", "T2": "forward", "T3": "forward", "T4": "AGAINST fw", "T5": "AGAINST fw",
             "T6": "AGAINST fw", "T7": "AGAINST fw", "T8": "forward", "T9": "AGAINST fw",
             "T10": "none", "T11": "forward", "T12": "none", "T13": "none", "T14": "AGAINST fw"}
for i, t in enumerate(RANK, 1):
    print(f"  {i:<3} {t['key']:<5} {t['name'][:46]:<46} {t['power']:>7.2f} {t['effort']:>7} "
          f"{t['score']:>7.2f} {t['status']:>7} {DIRECTION.get(t['key'],''):>11} {t['flag']:>17}")
print("\n  power  = separation in sigma achievable at the BEST reachable precision, capped by the "
      "systematic floor")
print("  score  = power / (1 + effort);  effort levels: " + " | ".join(EFFORT_LABEL[k] for k in sorted(EFFORT_LABEL)))
print("  direction: 'AGAINST fw' = the test is already returning a result adverse to the framework; "
      "'forward' = not yet decided")
print("  flag 'LOOPHOLE' = decisive against every COMPUTED variant of the framework, but a named "
      "loophole (nonlinear\n       top-down fragmentation) is uncomputed rather than excluded, so it "
      "does not yet decide against the class.")

# ==================================================================================================
# SECTION 8 -- VERDICT CHECKS
# ==================================================================================================
print("\n" + BAR); print("SECTION 8 -- verdicts"); print(BAR)
decisive_now = [t for t in TESTS if t["status"] == "a" and t["decisive"]]
decisive_facility = [t for t in TESTS if t["status"] == "b" and t["power"] >= 3.0]
forward_decisive = [t for t in decisive_facility if DIRECTION.get(t["key"]) == "forward"]
never = [t for t in TESTS if t["power"] < 3.0]

check("D1 at least one live test is ALREADY decisive at 3 sigma with data in hand",
      len(decisive_now) >= 1, ", ".join(f"{t['key']} ({t['power']:.1f} sigma)" for t in decisive_now))
check("D2 at least one live test is decisive at 3 sigma with an existing or approved facility and a "
      "stated sample size", len(decisive_facility) >= 1,
      ", ".join(f"{t['key']} ({t['power']:.1f} sigma)" for t in decisive_facility))
check("D3 at least one UNDECIDED (forward-looking) test is decisive at 3 sigma with an existing or "
      "approved facility", len(forward_decisive) >= 1,
      ", ".join(f"{t['key']} ({t['power']:.1f} sigma, effort {t['effort']})" for t in forward_decisive))
never_ever = [t for t in never if t["lever"] == "none" or (t["sig_sys"] > 0 and t["floor_ceiling"] < 3.0)]
check(f"D4 every test in the register reaches 3 sigma at SOME precision (this FAILS: {len(never)} do not, "
      f"and {len(never_ever)} of those cannot at any precision from any facility)", len(never) == 0,
      "below 3 sigma at their best reachable precision: " + ", ".join(t["key"] for t in never)
      + " | unreachable at ANY precision: " + ", ".join(t["key"] for t in never_ever))

# five-year falsifiability, asked twice
fiveyr_any = [t for t in TESTS if t["power"] >= 3.0 and t["effort"] <= 2 and DIRECTION.get(t["key"]) == "forward"]
# the Cassini-consistent version: exclude Arm A (fails the Cassini quadrupole 4-5x per gate G01)
CASSINI_INCONSISTENT = {"T1", "T11"}   # Arm A's kernel as strict AQUAL, and its directional AQUAL signature
fiveyr_cassini = [t for t in fiveyr_any if t["key"] not in CASSINI_INCONSISTENT]
check("V1 the framework is falsifiable in practice within five years -- at least one undecided test "
      "reaches 3 sigma with data already scheduled or public", len(fiveyr_any) >= 1,
      ", ".join(f"{t['key']} ({t['power']:.1f} sigma, {t['when'][:40]})" for t in fiveyr_any))
check("V2 the version of the framework that PASSES the Solar System is falsifiable in practice within "
      "five years (this FAILS: excluding the arm that fails the Cassini quadrupole by 4-5x, no undecided "
      "test at effort <= 2 reaches 3 sigma)", len(fiveyr_cassini) >= 1,
      f"{len(fiveyr_cassini)} candidates; the covariant candidate's only registered observable, Arm B, "
      f"is capped at {(ARM_B['canonical']-1)/SIG_SYS:.2f} sigma at infinite N")
check("V3 the framework can be CONFIRMED (not merely survive) at 3 sigma within five years by a test "
      "whose positive result LambdaCDM cannot produce (this FAILS: the only such test at effort <= 2 is "
      "Arm A, whose confirmation would confirm a model excluded in the Solar System)",
      len(fiveyr_cassini) >= 1, "Arm A confirmation is internally inconsistent with gate G01")

print("\n" + BAR)
print("WHAT TO BET ON")
print(BAR)
print(f"""
  1. GAIA DR4, ARM A (T1).  {ARM_A['canonical'][0]-1.0:.4f} against Newton at sigma_tot = {SIG_TOT} is
     {(ARM_A['canonical'][0]-1.0)/SIG_TOT:.1f} sigma canonical / {(ARM_A['alt'][0]-1.0)/SIG_TOT:.1f} sigma alt,
     on a scheduled date with a hash-frozen pipeline and a systematic floor that is not binding.  It is the
     only forward test in the register that is decisive, cheap and dated.  Bet on it -- but bet knowing
     what it can return: it kills Arm A or it confirms a model that fails the Cassini quadrupole by 4-5x,
     and the window where it both kills Newton and leaves the Cassini-consistent arm alive is
     {100*P_WINDOW_CAN:.1f}% / {100*P_WINDOW_ALT:.1f}% wide even at that arm's most favourable point.

  2. THE DESI-DEEP ISOLATION CUT ON BINARY GALAXIES (T6).  Cheapest live gain in the register: the data
     are public, no new observations are needed, and it attacks the ONE systematic (isolation depth,
     worth 57% of the framework-vs-LambdaCDM separation) that currently caps the result.  Statistics were
     never the limitation; 1900 pairs against a 384-pair requirement.

  3. DO NOT SPEND ON: the coefficient (T13 -- 27 candidates already in the band, no precision helps);
     the Rubin a0(z) stream (T10 -- it measures w, and a null makes the framework degenerate with flat);
     standard sirens (T12 -- LambdaCDM predicts the same thing); and the SPARC tightness claim as a
     discriminant (T14 -- L28 removed it).  Four of these cannot reach 3 sigma at ANY precision from ANY
     facility, and that is the single most useful line in this lane.
""")

print(BAR)
if FAILS:
    print(f"RESULT: {len(FAILS)} FAIL -> {FAILS}")
else:
    print("RESULT: 0 FAIL")
print(BAR)
sys.exit(len(FAILS))
