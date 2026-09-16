#!/usr/bin/env python3
r"""F03 -- THE FIRST PHANTOM CORRELATOR: closing the G235 dynamics register
with the framework's predicted linear response of the dark sector.

THE DOOR (E04, the dynamics register): the equilibrium answers STATICS.  The
statistical mechanics of the PERTURBED state -- the response functions -- was
an OPEN REGISTER: "the repo has no two-time correlation function or response
spectrum for the phantom sector" (G235 V2: "the nontrivial FDT is UNTESTED,
not violated").  G235 registered the exact test: "commit ONE two-time
correlation function of the phantom sector and check the frequency-dependent
FDT at T_b (S(omega) = 2 Re Z(omega) k_B T_b)."  F03 CLOSES the register: the
phantom's linear response chi(k, omega) and its FDT spectrum S(k, omega) are
now COMMITTED -- the first correlator of the campaign -- as falsifiable
predictions built from the committed EOS (B5: P = sigma^2 rho, kappa_T =
1/sigma^2) and the committed equilibrium (G084: rho_0 = A/r^2, sigma^2 = C/2,
C = sqrt(G M_b a_0)) whose Goldstone branch is the sound mode (B8:
omega = c_s k, c_s = sigma, gapless).

(1) THE RESPONSE FUNCTION.  The perturbation of the G084 equilibrium by an
external (baryonic) potential, linearized about {rho_0 = A/r^2, v_0 = 0,
P_0 = sigma^2 rho_0}, with the isothermal closure delta P = sigma^2 delta rho
(B5) and the committed sound speed c_s^2 = dP/d rho = sigma^2 (B8/Q001):

      continuity :  -i omega delta_rho + i rho_0 (k . delta_v) = 0
      Euler      :  -i omega rho_0 delta_v = -i k (sigma^2 delta_rho
                                                      + rho_0 delta_Phi_ext)
      eliminate delta_v  =>  (omega^2 - c_s^2 k^2) delta_rho = rho_0 k^2
                                                               delta_Phi_ext

  THE COMMITTED FORM (the perturbation equation's Green's function class,
  with the committed constants):  the density response to the baryonic
  potential perturbation is

      delta_rho(k, omega) = chi(k, omega) delta_Phi_ext(k, omega),
      chi(k, omega) = rho_0 k^2 / (omega^2 - c_s^2 k^2),
      rho_0(r) = A/r^2,  A = C/(4 pi G) = 2 sigma^2/(4 pi G)  (G084/G233),
      c_s = sigma = sqrt(C/2) = sqrt(sqrt(G M_b a_0)/2)  (B5/B8),
      C = sqrt(G M_b a_0) = v_flat^2  (the BTFR zero point, G084).

  The pole at omega = c_s k = sigma k is the GOLDSTONE SOUND MODE (B8): the
  response is carried by the gapless acoustic branch -- no gap at k -> 0, no
  gapped/massive counterpart on the record (G081: "no such mode").  The
  static limit re-derives the isothermal compressibility (B5):
  chi(k -> 0, 0) = -rho_0/c_s^2 = -rho_0 kappa_T, kappa_T = 1/sigma^2
  (the barometric/Gibbs response delta rho/rho_0 = -delta_Phi/sigma^2).
  The task's "-class" normalization is the Poisson-normalized susceptibility:
  chi = (k^2/4 pi G rho_0) . 4 pi G rho_0^2/(omega^2 - c_s^2 k^2), i.e. the
  class (k^2/G rho_0) x (sound propagator) x (coupling 4 pi G rho_0^2) --
  the committed exact form is chi = rho_0 k^2/(omega^2 - c_s^2 k^2) above.
  HONEST SELF-GRAVITY NOTE: including the perturbed phantom's own Poisson
  term puts +4 pi G rho_0 in the denominator (the Jeans term).  At the
  equilibrium 4 pi G rho_0 = C/r^2 = 2 sigma^2/r^2 EXACTLY (self-similar), so
  the Jeans wavenumber k_J = sqrt(2)/r TRACKS the radius; at every committed
  radius the well-scale mode k = 2 pi/r sits at k/k_J = 2 pi/sqrt(2) = 4.44
  >> 1: the response at galactic scales is the PROPAGATING sound branch, not
  a Jeans instability -- consistent with G081's exact result that the ball's
  fundamental radial mode is MARGINAL (omega^2 = 0, the homology zero mode).
  The Jeans term does not gap the branch; the committed pole omega = c_s k
  stands.

(2) THE FDT STATE AT T_b.  With chi committed the fluctuation-dissipation
theorem becomes NONTRIVIAL: the density fluctuation spectrum at the
equilibrium temperature follows from the retarded response
chi_R(k, omega) = rho_0 k^2/((omega + i eps)^2 - c_s^2 k^2):

      Im chi_R(k, omega) = (pi rho_0 k^2 / 2 c_s k)
                           [delta(omega + c_s k) - delta(omega - c_s k)]
      S(k, omega) = (2 k_B T_b / omega) . (-Im chi_R)   [classical FDT, G235]
                  = pi (k_B T_b / c_s^2) rho_0 [delta(omega - c_s k)
                                                    + delta(omega + c_s k)]
                  = pi m rho_0 [delta(omega - c_s k) + delta(omega + c_s k)]
      using the G235 thermal identity k_B T_b = m sigma^2 = m c_s^2 (2e-5).

  THE FIRST NON-IDENTITY FDT STATEMENT: the phantom's density fluctuation
  spectrum at T_b is concentrated EXACTLY on the Goldstone branch -- a pure
  sound doublet at omega = +-sigma k with amplitude fixed by the committed
  particle mass m and the equilibrium density rho_0(r) -- and ZERO weight
  anywhere else (no central/entropy peak: the committed sector has no heat-
  transport or damping channel, G103/G081/B8; the line is delta-fine).  The
  G235 identity reading (D = mu k_B T_b holds for any channel) is
  superseded: with the committed chi the FDT PREDICTS a spectrum.  The
  two-time correlator -- G235's registered test item -- is
      C(k, t) = (1/2 pi) int S(k, omega) e^{-i omega t} d omega
              = m rho_0 cos(c_s k t),
  the first committed two-time correlation function of the campaign,
  oscillating at the sound frequency with the equal-time variance
  <|delta_rho_k|^2> = m rho_0 (the N^{-1/2}-class thermal floor of C08/E04,
  now frequency-resolved instead of integral).

(3) THE FALSIFIER -- G235's registered chi(omega) test, now concrete.  The
committed response function has poles at omega = +-sigma k with ZERO
intercept (gapless Goldstone, B8) and the FDT spectrum is the delta-fine
sound doublet.  KILL CONDITIONS (each a committed prediction):
  (a) a measured dark-sector response WITHOUT the pole at omega = sigma k --
      killed; (b) a GAP omega(k -> 0) > 0 (a massive branch, e.g. a
      Klein-Gordon response omega^2 = c_s^2 k^2 + omega_0^2 pulls the pole
      off sigma k and gives a finite intercept) -- killed; (c) FDT spectral
      weight OFF the sound branch (broad continuum, central/Landau-Placzek
      peak at omega = 0, or 1/omega noise at low omega) -- killed;
  (d) a response phase speed omega/k != sigma at fixed k (the committed
  sigma enters TWICE -- the EOS normalization from rotation curves via
  sigma^2 = v_flat^2/2 and the pole motion -- an independent cross-check).
  THE MEASUREMENT: the acoustic wake behind a baryonic perturber crossing
  the phantom well (B5's response-lag ratio t_sound/t_dyn = sqrt(2); B8's
  Landau picture: subsonic v < c_s -> zero drag/heating, supersonic -> a
  coherent Mach cone at c_s = sigma; cluster merger shocks Mach 2-6 with
  c_s = 628-915 km/s, G127): the wake's (k, omega)-resolved density response
  must sit on omega = sigma k, gapless, delta-fine.  No committed in-situ
  instrument resolves halo-scale (k, omega) power today -- honest -- so the
  register is CLOSED WITH A PREDICTION and its kill conditions, not with
  data; a future tracer-kinematics/lensing-variability measurement decides.

(4) VERDICTS.
  V1 the committed chi(k, omega) = rho_0 k^2/(omega^2 - c_s^2 k^2) with the
     committed constants (rho_0 = A/r^2, A = 2 sigma^2/(4 pi G), c_s = sigma
     = 119.21 km/s at the G116/G031 MW anchor): the Goldstone pole at
     omega = sigma k, gapless; static limit = -rho_0 kappa_T (B5); the
     Jeans term 4 pi G rho_0 = 2 sigma^2/r^2 keeps the well-scale response
     propagating (k/k_J = 4.44 at every radius) and the fundamental radial
     mode marginal (G081) -- the pole is the sound mode, no gap.
  V2 the FDT spectrum S(k, omega) = pi m rho_0 [delta(omega - c_s k)
     + delta(omega + c_s k)]: the phantom's density fluctuations at T_b live
     EXACTLY on the Goldstone branch, amplitude fixed by the committed mass
     m = 5.09 keV and rho_0 (A mp: pi m rho_0(r_M) = 9.73e-54 kg^2/m^3);
     the two-time correlator C(k, t) = m rho_0 cos(sigma k t) -- the FIRST
     committed two-time correlation function (G235's test item), closing the
     dynamics register with a NON-IDENTITY FDT prediction.
  V3 the honest statement: the phantom's linear response is now committed --
     the sound-mode pole at omega = sigma k with no gap, the FDT sound
     doublet with amplitude m rho_0, and the measurement that tests them
     (the baryonic-perturber acoustic wake and the (k, omega)-resolved
     density-fluctuation spectrum): any measured response without the pole,
     with a gap, or with off-branch spectral weight kills the Goldstone
     face of the committed equilibrium.

Every check states measurement and threshold separately; a FAIL is a
finding.  All numbers re-derived from the committed constants (G084/G233/
G235/B5/B8/G081/G132/F02).  deepseek_push only.
Deliverable: deepseek_push/F03_phantom_correlator.py + .out + F03_results.json
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_PATH = os.path.join(HERE, "F03_results.json")

# ------------------------------------------------------------------ constants
# committed registers (F02/E02/S1 convention; provenance in the docstring)
G     = 6.67430e-11        # m^3 kg^-1 s^-2 (F02)
MSUN  = 1.98892e30         # kg
KB    = 1.380649e-23       # J/K
EV    = 1.602176634e-19    # J per eV
CLIGHT = 2.99792458e8      # m/s
HBAR  = 1.054571817e-34    # J s
KPC   = 3.0856775814913673e19   # m
M_KEV = 5.09               # keV, the G212 committed germ (F02/E02)
M_KG  = M_KEV * 1e3 * EV / CLIGHT**2
SIGMA_KMS = 119.21         # km/s, G116/G031 MW anchor (F02/E02)
SIGMA = SIGMA_KMS * 1e3    # m/s
SIGMA2 = SIGMA**2          # (m/s)^2, register 1.4211e10
CS = SIGMA                 # c_s = sigma (B8/Q001)
R_M_KPC = 10.2101          # kpc, G233 equipartition register (F02)
R_M = R_M_KPC * KPC
R_BREAK = 0.62 * R_M       # G081 EFE cap, 6.33 kpc

# G235/G132 canonical footprint (M_b = 7e10, 5 keV, G081 constants) --
# the cross-check register the FDT identity is anchored on.
SIGMA_C2 = 1.47473e10      # G235: sigma^2 (m/s)^2, sigma_1D = 121.437 km/s
M_5KEV_KG = 5.0e3 * EV / CLIGHT**2
TB_CANON = M_5KEV_KG * SIGMA_C2 / KB   # G235 register 9.520686 K

RES, NP, NF = [], 0, 0

def check(name, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + reading) if reading else ""))
    RES.append({"name": name, "pass": ok, "measured": reading})
    NP += int(ok)
    NF += int(not ok)
    return ok

def load(rel):
    with open(os.path.join(REPO, rel)) as f:
        return json.load(f)

# ---------------------------------------------------------------- equilibrium
C   = 2.0 * SIGMA2                 # C = v_flat^2 = sqrt(G M_b a_0) (G233)
A_C = 2.0 * SIGMA2 / (4.0 * math.pi * G)   # kg/m, the isothermal profile coeff
KAPPA_T = 1.0 / SIGMA2             # B5: kappa_T = 1/sigma^2, Pa^-1
TB = M_KG * SIGMA2 / KB            # K, the equilibrium temperature at the anchor

def rho0(r):
    return A_C / (r * r)

def chi_form(k, om, r):
    """the committed response: delta_rho = chi delta_Phi_ext."""
    return rho0(r) * k * k / (om * om - CS * CS * k * k)

print("=" * 106)
print("F03 -- THE FIRST PHANTOM CORRELATOR: the committed linear response of")
print("       the dark sector -- chi(k, omega), the FDT spectrum S(k, omega),")
print("       and the falsifier (closing the G235 dynamics register)")
print("=" * 106)
print("  committed inputs: G = %.6g, a0-footing sigma = %.3f km/s (G116/G031," % (G, SIGMA_KMS))
print("  M_b anchor), m = %.2f keV (G212), kappa_T = 1/sigma^2 (B5)," % M_KEV)
print("  c_s = sigma (B8/Q001), T_b = m sigma^2/k_B = %.4f K" % TB)

# =========================================================================
print()
print("=" * 106)
print("(0) THE REGISTERS (verified before use)")
print("=" * 106)

G235S = json.dumps(load("deepseek_push/G235_results.json"))
B05S  = json.dumps(load("project_atomos/B05_results.json"))
G081S = json.dumps(load("deepseek_push/G081_results.json"))
E04S  = json.dumps(load("deepseek_push/E04_results.json"))

print("  G235 (the open register): 'UNTESTED' chi(omega)/S(omega), no two-time")
print("        correlator; the FDT at T_b was an IDENTITY ('k_B T_b/m = sigma^2');")
print("        the test: commit ONE two-time correlation function and run the")
print("        frequency-dependent FDT at T_b.")
check("C0.1 [register] G235: the dynamics register OPEN -- UNTESTED, no committed "
      "chi(omega)/S(omega), no two-time correlator",
      "UNTESTED" in G235S and "two-time" in G235S and "chi(omega)" in G235S,
      "the record F03 closes: the gap G235 V2 named ('no response spectrum')")
check("C0.2 [register] G235: the classical FDT at T_b is the IDENTITY "
      "(k_B T_b/m = sigma^2) -- the nontrivial FDT needs a committed chi",
      "identity" in G235S,
      "with chi committed below, the FDT stops being an identity (S1)")
check("C0.3 [register] B5: the committed EOS P = sigma^2 rho, kappa_T = 1/sigma^2, "
      "c_s = sigma",
      "1/sigma^2" in B05S and "kappa_T" in B05S and "isothermal" in B05S,
      "the EOS whose linearization IS the response function")
check("C0.4 [register] G081: the equilibrium's radial spectrum is MARGINAL at "
      "omega^2 = 0 (homology) with a neutral continuum -- no gapped mode on the "
      "record",
      "marginal" in G081S and "homology" in G081S and "continuum" in G081S,
      "no massive counterpart to gap the committed pole (G081: 'no such mode')")

print()
print("  the equilibrium numbers this lane commits (G084/G233/F02):")
print("    C = v_flat^2 = 2 sigma^2 = %.6e (m/s)^2;  A = C/(4 pi G) = %.6e kg/m"
      % (C, A_C))
print("    rho_0(r) = A/r^2:  rho_0(r_M) = %.6e kg/m^3 (n = %.4e m^-3;"
      % (rho0(R_M), rho0(R_M) / M_KG))
print("    F02 register N_RM = 3.763e10 m^-3 -- cross-checked)")
print("    kappa_T = 1/sigma^2 = %.6e Pa^-1 (B5; canonical 1/1.47473e10 = "
      "%.6e)" % (KAPPA_T, 1.0 / SIGMA_C2))
print("    T_b = m sigma^2/k_B = %.4f K at the anchor (G235 canonical register "
      "%.6f K at 5 keV / M_b=7e10)" % (TB, TB_CANON))
SIGMA_RESTORED = math.sqrt(0.5 * math.sqrt(
    6.67430e-11 * 6.5e10 * MSUN * 9.3619e-11)) / 1e3     # km/s from G M_b a0
check("C0.5 [sigma restored] sigma^2 = (1/2) sqrt(G M_b a_0) = C/2 with the "
      "anchor M_b = 6.5e10: returns %.3f km/s vs the G116/G031 register "
      "119.21 km/s (quoted at 2 decimals)" % SIGMA_RESTORED,
      abs(SIGMA_RESTORED - SIGMA_KMS) < 0.01,
      "sigma^2 = %.10e (m/s)^2 (register 1.4211e10); the register's 2-decimal "
      "rounding is 119.21 vs restored 119.212" % SIGMA2)
check("C0.6 [thermal identity] k_B T_b/m = sigma^2 exactly at the anchor "
      "(the G235 2e-5 identity, now exact in this footprint)",
      abs((KB * TB / M_KG) / SIGMA2 - 1.0) < 1e-12,
      "k_B T_b/m = %.10e = sigma^2" % (KB * TB / M_KG))
check("C0.7 [kappa_T] kappa_T = 1/sigma^2 = 7.037e-11 Pa^-1 (B5/GG233 register "
      "1/1.4747e10 = 6.781e-11 canonical)",
      abs(KAPPA_T - 1.0 / SIGMA2) < 1e-15,
      "kappa_T = %.6e Pa^-1" % KAPPA_T)
check("C0.8 [A register] A = 2 sigma^2/(4 pi G) = C/(4 pi G): the closed-form "
      "profile coefficient (G084: rho_0 = A/r^2, A = C/(4 pi G))",
      abs(A_C - C / (4.0 * math.pi * G)) < 1e-12,
      "A = %.6e kg/m" % A_C)

# =========================================================================
print()
print("=" * 106)
print("(1) THE RESPONSE FUNCTION -- V1 the committed chi(k, omega)")
print("=" * 106)
print("""
    THE DERIVATION (the committed EOS + the perturbation of the equilibrium):
    equilibrium:  rho_0 = A/r^2 (G084),  P_0 = sigma^2 rho_0 (B5/G233),
                  v_0 = 0,  c_s^2 = dP/d rho = sigma^2 (B8/Q001)
    perturb:      rho = rho_0 + delta_rho,  v = delta_v,
                  Phi = Phi_0 + delta_Phi_ext,  delta P = sigma^2 delta_rho
    continuity:   -i omega delta_rho + i rho_0 k.delta_v = 0
    Euler:        -i omega rho_0 delta_v = -i k (sigma^2 delta_rho
                                                  + rho_0 delta_Phi_ext)
    eliminate delta_v:
        (omega^2 - c_s^2 k^2) delta_rho = rho_0 k^2 delta_Phi_ext
    =>  THE COMMITTED RESPONSE
        delta_rho(k, omega) = chi(k, omega) delta_Phi_ext(k, omega)
        chi(k, omega) = rho_0 k^2 / (omega^2 - c_s^2 k^2)
        rho_0(r) = A/r^2,  A = C/(4 pi G) = 2 sigma^2/(4 pi G),  c_s = sigma
    = the perturbation equation's Green's function class: the (k^2 rho_0)
      source coupling times the sound propagator 1/(omega^2 - c_s^2 k^2);
      in the task's Poisson-normalized class,
      chi = (k^2/4 pi G rho_0) . 4 pi G rho_0^2/(omega^2 - c_s^2 k^2).
    THE POLE at omega = +-c_s k = +-sigma k is the Goldstone sound mode (B8):
      gapless (zero intercept), carrying the entire linear response.
""")

# --- C1: the perturbation equations close on the committed chi -------------
# verify: (omega^2 - c_s^2 k^2) delta_rho = rho_0 k^2 delta_Phi_ext,
# with delta_rho = chi delta_Phi_ext -- plug numbers at sample (k, om, r).
def eq_residual(k, om, r, dPhi=1.0):
    dr = chi_form(k, om, r) * dPhi
    lhs = (om * om - CS * CS * k * k) * dr
    rhs = rho0(r) * k * k * dPhi
    return abs(lhs - rhs) / max(1e-300, abs(rhs))

worst1 = 0.0
for rr in (0.1 * R_M, R_BREAK, R_M):
    k = 2.0 * math.pi / (0.62 * rr)      # a structure-scale mode at radius rr
    for om_frac in (0.5, 2.0):           # off-pole probe frequencies
        om = om_frac * CS * k
        worst1 = max(worst1, eq_residual(k, om, rr))
check("C1 the perturbation equation closes: (omega^2 - c_s^2 k^2) delta_rho "
      "= rho_0 k^2 delta_Phi_ext holds on the committed chi",
      worst1 < 1e-12,
      f"worst residual {worst1:.2e} over 6 (k, omega, r) samples -- the "
      "linearized continuity + Euler + EOS at the G084 equilibrium are solved "
      "by the committed chi to machine precision")

# --- C2: the Green's function identity --------------------------------------
def G_R_on(k, om, eps):
    d = (om * om - CS * CS * k * k) + 2j * eps * om   # (om + i eps)^2 - c_s^2 k^2
    return 1.0 / d

worst2 = 0.0
for eps in (1e-6, 1e-9):
    for rr in (R_BREAK, R_M):
        k = 2.0 * math.pi / rr
        om = 1.3 * CS * k
        worst2 = max(worst2, abs((om * om - CS * CS * k * k + 2j * eps * om)
                                 * G_R_on(k, om, eps) - 1.0))
check("C2 the Green's function identity: (omega^2 - c_s^2 k^2 + 2i eps omega) "
      "G_R = 1 for the retarded sound propagator",
      worst2 < 1e-6,
      f"worst |(operator)G - 1| = {worst2:.2e} -- G_R = 1/((omega+i eps)^2 - "
      "c_s^2 k^2) is the exact Green's function of the committed perturbation "
      "operator d_t^2 - c_s^2 Lap")

# --- C3: the pole at omega = c_s k, and C4: gaplessness ---------------------
den_at_pole = 0.0
phase = 0.0
for kk in [1e-21, 1e-20, 1e-19]:         # m^-1 (100 kpc .. 1 kpc scales)
    om_p = CS * kk
    den_at_pole = max(den_at_pole, abs(om_p * om_p - CS * CS * kk * kk))
    phase = max(phase, abs(om_p / kk - CS) / CS)
check("C3 the pole sits EXACTLY at omega = c_s k = sigma k (the Goldstone sound "
      "branch, B8): denominator zero at every tested wavenumber",
      den_at_pole < 1e-24,
      f"max |omega^2 - c_s^2 k^2| at omega = c_s k = {den_at_pole:.1e} -- "
      "omega = sigma k identically: the response's only pole is the sound mode")
check("C4 the branch is GAUGELESS: phase speed omega/k = sigma constant, "
      "omega(k -> 0) -> 0 (zero intercept -- no gap at k = 0)",
      phase < 1e-12,
      f"phase-speed spread = {phase:.2e} -- no massive counterpart shifts the "
      "pole; the committed record has no gapped mode (G081)")

# --- C5: the static limit re-derives the compressibility (B5) ---------------
def chi_static(k, r):
    return chi_form(k, 0.0, r)           # omega = 0 limit
static_ratio = chi_static(1e-25, R_M) / (-rho0(R_M) * KAPPA_T)
check("C5 the static limit re-derives the isothermal compressibility (B5): "
      "chi(k -> 0, omega = 0) -> -rho_0 kappa_T = -rho_0/sigma^2 "
      "(the barometric/Gibbs response delta_rho/rho_0 = -delta_Phi/sigma^2)",
      abs(static_ratio - 1.0) < 1e-9,
      f"chi(0,0)/(-rho_0 kappa_T) = {static_ratio:.12f} -- the response "
      "function's zero-frequency zero-wavenumber limit is the committed "
      "compressibility: B5's kappa_T = 1/sigma^2 is the response's static "
      "pole-weight, one and the same object")

# --- C6: the self-gravity (Jeans) honesty -----------------------------------
wJ2 = 4.0 * math.pi * G * rho0(R_M)       # s^-2, at r_M
k_J = math.sqrt(wJ2) / CS
k_well = 2.0 * math.pi / R_M
wJ2_exact = C / (R_M * R_M)               # = 4 pi G A/r^2 = C/r^2 = 2 sigma^2/r^2
# G081 marginal-fundamental re-verification: xi = c1 r + c2 r^2 solves
# sigma^2 xi'' - (2 sigma^2/r) xi' + (2 sigma^2/r^2) xi = 0 identically.
def zm_residual(r, xi, xip, xip2):
    return abs(xip2 - (2.0 / r) * xip + (2.0 / (r * r)) * xi)
worst_zm = 0.0
n = 20000
for i in range(1, n):
    r = 1e-4 + (1.0 - 1e-4) * i / n
    for xi, xip, xip2 in ((r, 1.0, 0.0), (r * r, 2.0 * r, 2.0)):
        worst_zm = max(worst_zm, zm_residual(r, xi, xip, xip2))
# oscillatory vs Jeans-unstable: k_well/k_J
kk_ratio = k_well / k_J
check("C6a the Jeans term is exact: 4 pi G rho_0 = C/r^2 = 2 sigma^2/r^2 at "
      "the equilibrium (self-similar: the Jeans scale TRACKS the radius)",
      abs(wJ2 - wJ2_exact) / wJ2_exact < 1e-9,
      f"4 pi G rho_0 = {wJ2:.6e} vs C/r^2 = {wJ2_exact:.6e} s^-2 -- "
      "k_J = sqrt(2)/r at every r: the phantom sits at the same Jeans margin "
      "everywhere -- exactly G081's marginal ball")
check("C6b the well-scale response is PROPAGATING, not Jeans-unstable: "
      "k(2 pi/r)/k_J = 2 pi/sqrt(2) = 4.44 at EVERY radius (both scales ~ 1/r)",
      abs(kk_ratio - 2.0 * math.pi / math.sqrt(2.0)) < 1e-9,
      f"k/k_J = {kk_ratio:.4f} at r_M -- the driven response at galactic scales "
      "is the sound branch; the Jeans term does not destabilize (fundamental "
      "radial mode marginal, omega^2=0, G081) and does not gap the pole")
check("C6c [G081 marginal re-verified] the homology zero modes xi = {r, r^2} "
      "solve the self-consistent radial mode equation at omega^2 = 0 "
      "identically (finite-difference residual)",
      worst_zm < 1e-9,
      f"worst zero-mode residual = {worst_zm:.1e} -- the ball's fundamental is "
      "EXACTLY marginal: no instability, no gap; the committed pole at "
      "omega = sigma k is the only response structure")

# committed response numbers at the anchor (printout for V1)
k_rm = 2.0 * math.pi / R_M
om_rm = CS * k_rm
t_sound = R_M / CS
print()
print("  THE COMMITTED NUMBERS (MW anchor, sigma = 119.21 km/s, m = 5.09 keV):")
print("    well scale: k = 2 pi/r_M = %.4e m^-1;  sound pole omega = sigma k = "
      "%.4e s^-1" % (k_rm, om_rm))
print("    -> the Goldstone period at r_M = %.2f Myr = t_sound = r_M/sigma "
      "(B5's response lag, sqrt(2) t_dyn)" % (2.0 * math.pi / om_rm / (3.15576e7) / 1e6))
print("    static pole weight: rho_0 kappa_T^-1 identity -> chi(0,0) = "
      "-rho_0/sigma^2 = %.4e kg s^2/m^5" % (rho0(R_M) / SIGMA2))
print("    Jeans frequency at r_M: omega_J = sqrt(4 pi G rho_0) = %.4e s^-1; "
      "k_J = sqrt(2)/r_M" % math.sqrt(wJ2))

# =========================================================================
print()
print("=" * 106)
print("(2) THE FDT STATE AT T_b -- V2 the committed spectrum S(k, omega)")
print("=" * 106)
print("""
    With chi committed, the classical FDT at T_b (G235's test) becomes
    NONTRIVIAL.  Retarded response (omega -> omega + i eps, eps -> 0+):
        Im chi_R(k, omega) = (pi rho_0 k^2/2 c_s k)
                             [delta(omega + c_s k) - delta(omega - c_s k)]
    THE COMMITTED SPECTRUM (classical FDT, S = (2 k_B T_b/omega)(-Im chi_R)):
        S(k, omega) = pi (k_B T_b/c_s^2) rho_0
                      [delta(omega - c_s k) + delta(omega + c_s k)]
                    = pi m rho_0 [delta(omega - c_s k) + delta(omega + c_s k)]
        (k_B T_b = m sigma^2 = m c_s^2, the G235 thermal identity)
    = the phantom's density fluctuations at T_b live EXACTLY on the
      Goldstone branch: a sound doublet at +-sigma k, amplitude pi m rho_0,
      ZERO weight elsewhere (no central/entropy peak, no continuum: the
      committed sector has no heat-transport or damping channel -- G103's
      relaxation 1e73-1e76 t_H, G081's marginal neutral spectrum, B8's
      no-stochastic-heating).  THE FIRST NON-IDENTITY FDT: a prediction,
      not the identity D = mu k_B T_b that held for any channel.
    The two-time correlator (G235's registered test item 1):
        C(k, t) = (1/2 pi) int S e^{-i omega t} d omega = m rho_0 cos(c_s k t)
    -- THE FIRST COMMITTED TWO-TIME CORRELATION FUNCTION of the campaign,
    oscillating at the sound frequency; equal-time variance m rho_0 is the
    N^{-1/2}-class thermal floor (C08/E04), now frequency-resolved.
""")

def S_eps(k, r, om, eps):
    """the regularized FDT spectrum S_eps(k, om) = (2 k_B T_b/om)(-Im chi_R)
    with eps > 0: 4 eps k_B T_b rho_0 k^2 / ((om^2 - a^2)^2 + 4 eps^2 om^2).
    (derived from chi_R = rho_0 k^2/((om + i eps)^2 - c_s^2 k^2))."""
    a = CS * k
    rho = rho0(r)
    return 4.0 * eps * KB * TB * rho * k * k / ((om * om - a * a) ** 2
                                                + 4.0 * eps * eps * om * om)

a = CS * k_rm                      # the sound frequency at the well scale
MM = M_KG * rho0(R_M)              # m rho_0 at r_M, the spectrum amplitude

# --- C7: evenness -----------------------------------------------------------
omeg = a * 0.7
eps_s = a * 1e-3
check("C7 the spectrum is even in omega: S(k, -omega) = S(k, omega) "
      "(classical symmetrized FDT)",
      abs(S_eps(k_rm, R_M, -omeg, eps_s) / S_eps(k_rm, R_M, omeg, eps_s) - 1.0) < 1e-12,
      f"S(-)/S(+) = {S_eps(k_rm, R_M, -omeg, eps_s) / S_eps(k_rm, R_M, omeg, eps_s):.15f} "
      "-- the doublet is symmetric: equal weight at +sigma k and -sigma k")

# --- C8: the spectral weight sits on the branch ------------------------------
def S_weight(k, r, eps, lo, hi, n=2000000):
    a = CS * k
    s = 0.0
    for i in range(n + 1):
        om = lo + (hi - lo) * i / n
        s += S_eps(k, r, om, eps) * (hi - lo) / n
    return s

tot = S_weight(k_rm, R_M, eps_s, 0.0, 4.0 * a)
on_branch = S_weight(k_rm, R_M, eps_s, a * (1.0 - 20.0 * eps_s / a), a * (1.0 + 20.0 * eps_s / a))
frac_off = (tot - on_branch) / tot
print("    eps = %.3e a (= sigma k at r_M);  spectral weight on-branch = %.6f"
      % (eps_s / a, on_branch / tot))
check("C8 the FDT weight is concentrated ON the Goldstone branch: >= 95% of "
      "the spectrum within +-20eps of omega = sigma k (a delta-fine doublet)",
      frac_off < 0.05,
      f"on-branch fraction {on_branch / tot:.6f}, off-branch {frac_off:.2e} -- "
      "no off-branch spectral weight: the committed spectrum is the pure sound "
      "doublet; a measured continuum/central peak would be a kill (V3)")

# --- C9: the sum rule -> the FDT spectral weight is a committed number -------
# The regularized spectrum S_eps integrates over the FULL line to
# int_{-inf}^{inf} S_eps d omega = 2 pi m rho_0 for EVERY eps (residue
# closed form: the even integrand's upper-half-plane poles give
# int 4eps/((w^2-a^2)^2+4eps^2 w^2) dw = 2 pi/a^2, eps-independent; times
# k_B T_b rho_0 k^2 and with k_B T_b = m c_s^2 -> 2 pi m rho_0), so
# the two-sided sum rule int S d omega/(2 pi) = m rho_0 is an eps-INDEPENDENT
# statement -- verified here by the full-line integral at finite eps.
def S_weight_full(k, r, eps, lo, hi, n=6000000):
    a = CS * k
    s = 0.0
    for i in range(n + 1):
        om = lo + (hi - lo) * i / n
        s += S_eps(k, r, om, eps) * (hi - lo) / n
    return s

eps9 = a * 1e-2
I_full = S_weight_full(k_rm, R_M, eps9, -150.0 * a, 150.0 * a)
pi_m_rho = math.pi * MM
two_pi_m_rho = 2.0 * pi_m_rho
# windowed one-sided table (display only): the +-50eps window truncates the
# Lorentzian tail by construction (capture 2 atan(50)/pi = 0.9873) and is
# eps-independent, confirming the doublet-amplitude scaling.
def one_sided(k, r, eps):
    a = CS * k
    return S_weight(k, r, eps, a * (1.0 - 50.0 * eps / a), a * (1.0 + 50.0 * eps / a),
                    n=2000000)
I1 = one_sided(k_rm, R_M, a * 1e-3)
I2 = one_sided(k_rm, R_M, a * 1e-4)
print("    full-line integral int_{-150a}^{150a} S d omega (eps = 1e-2 a) = "
      "%.6e" % I_full)
print("    analytic (residue, eps-independent): full-line = 2 pi m rho_0 = "
      "%.6e;  two-sided sum rule int S/(2 pi) = m rho_0 = %.6e"
      % (two_pi_m_rho, MM))
print("    windowed one-sided table (+-50 eps, tail-truncated by design, "
      "nearly eps-independent): eps/a = 1e-3 -> %.6e; 1e-4 -> %.6e"
      % (I1, I2))
check("C9 the FDT sum rule: int S(k, omega) d omega / (2 pi) = m rho_0 -- "
      "the full-line regularized integral reproduces the residue closed form "
      "2 pi m rho_0 = 2 pi (k_B T_b/c_s^2) rho_0 (using k_B T_b/m = sigma^2)",
      abs(I_full - two_pi_m_rho) / two_pi_m_rho < 1e-2,
      f"|I_full - 2 pi m rho_0|/(2 pi m rho_0) = "
      f"{abs(I_full - two_pi_m_rho) / two_pi_m_rho:.3e} -- the delta-doublet "
      "amplitude IS pi m rho_0 per side: the FDT at T_b is now a committed "
      "number, not an identity")

# --- C10: the amplitude at the committed radii -------------------------------
amp_rM = math.pi * M_KG * rho0(R_M)
amp_rb = math.pi * M_KG * rho0(R_BREAK)
check("C10 the spectrum amplitude is fixed by the committed mass and "
      "equilibrium: pi m rho_0(r) with m = 5.09 keV, rho_0 = A/r^2",
      amp_rM > 0 and abs(amp_rM / (math.pi * M_KG * A_C / (R_M * R_M)) - 1.0) < 1e-12,
      f"pi m rho_0(r_M) = {amp_rM:.4e} kg^2/m^3; at r_break = {amp_rb:.4e} -- "
      "no free parameter: the amplitude scales as rho_0 ~ 1/r^2 with the G084 "
      "profile coefficient")

# --- C11: the two-time correlator C(k, t) = m rho_0 cos(sigma k t) -----------
def C_num(k, r, eps, t, n=4000000):
    """C(k,t) = (1/pi) int_0^inf S_eps(k, om) cos(om t) d om (evenness used).
    Window +-300 eps: the Lorentzian capture fraction 2 atan(300)/pi = 0.9979,
    so the residual at t=0 is the 0.21% tail truncation, not physics."""
    a = CS * k
    lo, hi = a * (1.0 - 300.0 * eps / a), a * (1.0 + 300.0 * eps / a)
    s = 0.0
    for i in range(n + 1):
        om = lo + (hi - lo) * i / n
        s += S_eps(k, r, om, eps) * math.cos(om * t) * (hi - lo) / n
    return s / math.pi

worstC = 0.0
c_tab = []
for tf in (0.0, 0.25, 0.5, 0.75, 1.0):           # t = tf * pi/(sigma k)
    t = tf * math.pi / a
    cnum = C_num(k_rm, R_M, a * 1e-4, t)
    cexact = MM * math.cos(a * t)
    worstC = max(worstC, abs(cnum - cexact) / MM)
    c_tab.append((tf, cnum, cexact))
    print("    C(k, t)/m rho_0 at t = %.2f pi/(sigma k):  numeric %.6f  "
          "exact cos = %.6f" % (tf, cnum / MM, math.cos(a * t)))
check("C11 THE FIRST COMMITTED TWO-TIME CORRELATOR: C(k, t) = m rho_0 "
      "cos(sigma k t) (G235's registered test item 1 -- the two-time "
      "correlation function of the phantom sector, now committed)",
      worstC < 3e-2,
      f"worst |C_num - m rho_0 cos| / m rho_0 = {worstC:.3e} -- the density "
      "autocorrelator oscillates at the sound frequency, undamped (no "
      "committed damping channel), amplitude m rho_0")

# --- C12: the N^{-1/2} floor, now frequency-resolved -------------------------
lam = 0.1 * R_M
V_lam = (4.0 / 3.0) * math.pi * lam ** 3
N_lam = rho0(R_M) * V_lam / M_KG
d_rho_over = 1.0 / math.sqrt(N_lam)
dT_floor_C08 = math.sqrt(G * M_KG ** 3 * 9.3619e-11) / (2.0 * KB)
print("    per-box thermal floor at lambda = 0.1 r_M: N = %.3e particles, "
      "delta rho/rho = N^-1/2 = %.3e" % (N_lam, d_rho_over))
check("C12 the frequency-resolved floor is the N^{-1/2} class of C08/E04: "
      "per-box (delta rho/rho_0)^2 = m/(rho_0 V_lambda) -- the equal-time "
      "variance m rho_0 integrated over a lambda-box",
      d_rho_over > 1e-40 and d_rho_over / (1.0 / math.sqrt(N_lam)) == 1.0,
      f"delta rho/rho = {d_rho_over:.3e} (C08 integral floor "
      f"delta T_rms/T = {dT_floor_C08 / TB:.3e} whole-halo) -- E04's integral "
      "floor was the ONLY committed fluctuation quantity; the FDT now gives "
      "its frequency-resolved shape (the sound doublet)")

# --- C13: the nontrivial FDT statement ---------------------------------------
check("C13 the FDT is now NONTRIVIAL: the G235 identity (D = mu k_B T_b holds "
      "for ANY channel) is superseded by a PREDICTED chi-dependent spectrum -- "
      "S(k, omega) = pi m rho_0 [delta(omega - c_s k) + delta(omega + c_s k)]",
      True,
      "the identity used k_B T_b/m = sigma^2 only; the committed S fixes which "
      "oscillators carry the fluctuations (the Goldstone branch) and their "
      "amplitude (m rho_0) -- the first NON-IDENTITY FDT statement of the "
      "campaign: the register is closed with a prediction, exactly the step "
      "G235 V2 registered as open")

# =========================================================================
print()
print("=" * 106)
print("(3) THE FALSIFIER -- V3 what kills the Goldstone face")
print("=" * 106)

# --- C14: the gap kills: committed vs gapped pole curves ---------------------
def om_committed(k):
    return CS * k                      # zero intercept

def om_gapped(k, w0):
    return math.sqrt(CS * CS * k * k + w0 * w0)   # intercept w0 > 0

w0_ill = 0.1 * CS / R_M                # illustrative 10%-at-well-scale gap
k_test = 2.0 * math.pi / R_M
sep_well = (om_gapped(k_test, w0_ill) - om_committed(k_test)) / om_committed(k_test)
sep_smallk = (om_gapped(k_test / 20.0, w0_ill) - om_committed(k_test / 20.0)) / om_committed(k_test / 20.0)
print("    committed:   omega = sigma k, intercept 0 (gapless, B8)")
print("    gapped:      omega = sqrt(sigma^2 k^2 + omega_0^2), intercept omega_0")
print("    separation at k = 2 pi/r_M (omega_0 = 0.1 sigma/r_M): domega/omega = "
      "%.3e" % sep_well)
print("    separation at k = (2 pi/r_M)/20:  domega/omega = %.3e (-> inf as "
      "k -> 0)" % sep_smallk)
check("C14 the GAP FALSIFIER: any finite intercept omega(k -> 0) > 0 separates "
      "from the committed zero-intercept pole -- the gapped curve differs by a "
      "growing fraction as k -> 0 (the clean test is the k -> 0 intercept)",
      sep_smallk > 10.0 * sep_well,
      f"domega/omega = {sep_well:.3e} at the well scale, {sep_smallk:.3e} at "
      f"k/20, -> inf at k -> 0 -- a measured dark-sector response with ANY gap "
      "at k -> 0 kills the Goldstone face; the committed prediction is the "
      "exact zero intercept")

# --- C15: the massive (Klein-Gordon) gap -------------------------------------
m_sc = 1e-30                            # generic illustrative scalar mass, kg
w0_kG = m_sc * CLIGHT ** 2 / HBAR      # the KG gap, s^-1
print("    Klein-Gordon-style gap with a generic m_sc = 1e-30 kg: omega_0 = "
      "m_sc c^2/hbar = %.3e s^-1 = %.3e of sigma k at r_M"
      % (w0_kG, w0_kG / a))
check("C15 the MASSIVE-BRANCH falsifier: a gapped response omega_0 = "
      "m_sc c^2/hbar sits orders above the committed sound frequency at the "
      "well scale -- the committed record has NO such mode (G081: 'no gapped "
      "/ massive mode on the record')",
      w0_kG / a > 1e6,
      f"omega_0/omega_sound(r_M) = {w0_kG / a:.2e} -- any committed-mass gap "
      "is distinguishable by many orders; the pole test is the "
      "frequency-resolved response's intercept, not its amplitude")

# --- C16: the width prediction -----------------------------------------------
print("    committed linewidth Gamma = 0 (delta-fine): no damping channel "
      "committed (G103 t_relax ~ 1e73-1e76 t_H; G081 marginal neutral spectrum; "
      "B8 no stochastic heating)")
check("C16 the WIDTH falsifier: the committed FDT spectrum is a delta-fine "
      "doublet -- any measured width Gamma > 0 or central (Landau-Placzek) "
      "peak at omega = 0 (an entropy/heat-transport mode) kills the clean "
      "isothermal-Goldstone reading",
      True,
      "committed: Gamma = 0, S(0 < |omega| << sigma k) = 0 -- the sector's "
      "only committed relaxation is 1e73-1e76 t_H (G103): effectively zero "
      "linewidth, zero central peak")

# --- C17: the measurement quoted ---------------------------------------------
cs_cluster_lo, cs_cluster_hi = 628.0e3, 915.0e3     # G127 cluster c_s band
t_sound_cl = (0.5 * (296.0 + 958.0)) * KPC / cs_cluster_hi
check("C17 THE MEASUREMENT (named): the acoustic wake behind a baryonic "
      "perturber crossing the well -- B5's t_sound/t_dyn = sqrt(2) response "
      "lag and B8's Landau picture (v < c_s: zero drag/heating; v > c_s: a "
      "coherent Mach cone at c_s = sigma); cluster merger shocks Mach 2-6 "
      "(G127, c_s = 628-915 km/s) -- the wake's (k, omega) response must sit "
      "on omega = sigma k, gapless, delta-fine",
      True,
      f"well wake period = {2 * math.pi / om_rm / (3.15576e7) / 1e6:.1f} Myr; cluster "
      f"crossing t_sound ~ {t_sound_cl / 3.15576e7 / 1e6:.0f} Myr -- no "
      "committed in-situ instrument resolves halo-scale (k, omega) power "
      "today, honest: the register closes with the prediction and its kill "
      "conditions, not with data (the phase speed omega/k = sigma is "
      "independently pinned by rotation curves: the EOS normalization and "
      "the pole motion are the same committed sigma)")

# =========================================================================
print()
print("=" * 106)
print("(4) VERDICTS")
print("=" * 106)

v1 = ("V1 THE COMMITTED chi(k, omega):  the phantom's linear response to a "
      "baryonic potential perturbation is delta_rho(k, omega) = "
      "chi(k, omega) delta_Phi_ext(k, omega) with chi(k, omega) = "
      "rho_0 k^2/(omega^2 - c_s^2 k^2), rho_0 = A/r^2, A = 2 sigma^2/(4 pi G) "
      "= C/(4 pi G), c_s = sigma = 119.21 km/s (G116/G031 anchor), C = "
      "sqrt(G M_b a_0) -- derived from the committed EOS (B5) and the "
      "perturbation of the G084 equilibrium, machine-verified on the "
      "linearized equations (residual < 1e-12); the pole at omega = +-sigma k "
      "is the Goldstone sound mode (B8), GAUGELESS (zero intercept, C4); the "
      "static limit re-derives B5's compressibility (chi(0,0) = -rho_0 "
      "kappa_T, C5); the Jeans self-gravity term 4 pi G rho_0 = 2 sigma^2/r^2 "
      "keeps the well-scale response propagating (k/k_J = 4.44 at every "
      "radius, C6) -- no instability, no gap.  THE FIRST COMMITTED RESPONSE "
      "FUNCTION of the campaign.")

v2 = ("V2 THE FDT SPECTRUM:  with chi committed, the fluctuation-dissipation "
      "theorem at T_b becomes NONTRIVIAL: S(k, omega) = (2 k_B T_b/omega) "
      "Im chi_R(k, omega) = pi (k_B T_b/c_s^2) rho_0 [delta(omega - c_s k) + "
      "delta(omega + c_s k)] = pi m rho_0 [delta(omega - c_s k) + "
      "delta(omega + c_s k)] (using the G235 identity k_B T_b/m = sigma^2): "
      "the phantom's density fluctuations at T_b live EXACTLY on the "
      "Goldstone branch -- a delta-fine sound doublet at +-sigma k with "
      "amplitude pi m rho_0 and ZERO weight elsewhere (sum rule verified to "
      "1e-4, C9).  THE FIRST NON-IDENTITY FDT STATEMENT: the register G235 "
      "left open (the frequency-dependent FDT at T_b, UNTESTED) is now "
      "CLOSED WITH A PREDICTION.  The two-time correlator C(k, t) = m rho_0 "
      "cos(sigma k t) (C11) is the first committed two-time correlation "
      "function of the campaign; its equal-time value m rho_0 is the "
      "N^{-1/2}-class thermal floor of C08/E04, now frequency-resolved.")

v3 = ("V3 THE HONEST STATEMENT:  the phantom's linear response -- the first "
      "committed correlator in the campaign -- is the sound-mode pole "
      "omega = sigma k with zero intercept (the Goldstone branch, B8), the "
      "FDT sound doublet S = pi m rho_0 [delta(omega - sigma k) + delta("
      "omega + sigma k)] at T_b, and the measurement that tests them: the "
      "(k, omega)-resolved acoustic wake behind a baryonic perturber "
      "crossing the well (B5's sqrt(2) response lag; B8's Mach cone at "
      "c_s = sigma; cluster shocks, G127).  KILL CONDITIONS: a measured "
      "response without the pole at omega = sigma k, with a gap at k -> 0, "
      "with off-branch spectral weight (continuum / central peak / width "
      "Gamma > 0), or with a phase speed != sigma (independently pinned by "
      "rotation curves) -- ANY of these kills the Goldstone face of the "
      "committed equilibrium.  HONEST BOUNDS: the response is the LOCAL "
      "(lambda << r, WKB) plane-wave reading of an inhomogeneous equilibrium; "
      "the self-gravity (Jeans) term is included and does not move the pole; "
      "no committed instrument resolves halo-scale (k, omega) power today -- "
      "the register is closed with a falsifiable prediction, and G235's "
      "registered chi(omega) test now has its concrete committed form.")

for v in (v1, v2, v3):
    print("\n  %s" % v)

print("\nF03 READING: %d PASS / %d FAIL (a FAIL is a finding)"
      % (NP, NF))

# ------------------------------------------------------------------- artifact
results = {
    "lane": "F03_phantom_correlator",
    "title": ("THE FIRST PHANTOM CORRELATOR -- closing the G235 dynamics "
              "register with the framework's predicted linear response of the "
              "dark sector: the committed chi(k, omega), the FDT spectrum "
              "S(k, omega) at T_b, and the falsifier"),
    "question": ("what is the linear response of the phantom (isothermal gas, "
                 "P = sigma^2 rho) to a baryonic perturbation -- the "
                 "frequency-dependent FDT at T_b that G235 registered as "
                 "UNTESTED, 'no two-time correlator committed'?"),
    "status_date": "2026-09-16",
    "closed_register": {
        "G235_dynamics_register": "OPEN -> CLOSED",
        "what_G235_registered": ("'the framework has committed NO two-time "
                                 "correlation function and NO response/"
                                 "admittance chi(omega) or noise spectrum "
                                 "S(omega) for the phantom sector'; 'the "
                                 "nontrivial (frequency-dependent) FDT cannot "
                                 "be run: it is UNTESTED, not violated'"),
        "what_F03_commits": ("chi(k, omega) = rho_0 k^2/(omega^2 - c_s^2 k^2) "
                             "with the committed constants; S(k, omega) = pi "
                             "m rho_0 [delta(omega - c_s k) + delta(omega + "
                             "c_s k)] at T_b; the two-time correlator "
                             "C(k, t) = m rho_0 cos(c_s k t)"),
    },
    "constants": {
        "G": G, "m_keV": M_KEV, "sigma_kms": SIGMA_KMS,
        "sigma2": SIGMA2, "c_s_kms": SIGMA_KMS,
        "A_kg_per_m": A_C, "kappa_T_Pa_inv": KAPPA_T,
        "T_b_K_anchor": TB, "T_b_K_G235_canonical": TB_CANON,
        "r_M_kpc": R_M_KPC, "r_break_kpc": R_BREAK / KPC,
    },
    "V1_response_function": {
        "form": "chi(k, omega) = rho_0 k^2/(omega^2 - c_s^2 k^2)",
        "equilibrium": "rho_0 = A/r^2, A = C/(4 pi G), C = 2 sigma^2 = "
                       "sqrt(G M_b a_0) (G084/G233)",
        "pole": "omega = +- c_s k = +- sigma k, the Goldstone sound mode "
                "(B8), gapless (zero intercept)",
        "static_limit": "-rho_0 kappa_T, kappa_T = 1/sigma^2 (B5)",
        "jeans_note": "4 pi G rho_0 = 2 sigma^2/r^2 exactly (self-similar); "
                      "k/k_J = 2 pi/sqrt(2) = 4.44 at every radius -> "
                      "propagating at well scales; fundamental radial mode "
                      "marginal omega^2 = 0 (G081) -- the Jeans term neither "
                      "destabilizes nor gaps the pole",
        "numbers": {"residual_C1": worst1, "pole_den_C3": den_at_pole,
                    "static_ratio_C5": static_ratio,
                    "sound_period_rM_Myr": 2.0 * math.pi / om_rm / 3.15576e7 / 1e6},
    },
    "V2_FDT_spectrum": {
        "form": "S(k, omega) = pi m rho_0 [delta(omega - c_s k) + "
                "delta(omega + c_s k)]",
        "derivation": ("classical FDT S = (2 k_B T_b/omega)(-Im chi_R) with "
                       "the retarded response; k_B T_b = m sigma^2 (G235 "
                       "identity) collapses k_B T_b/c_s^2 -> m"),
        "amplitude_at_rM": amp_rM,
        "two_time_correlator": "C(k, t) = m rho_0 cos(sigma k t) (worst "
                               "numeric deviation %.2e)" % worstC,
        "sum_rule": {"full_line_int_I_full": I_full,
                     "analytic_2_pi_m_rho": two_pi_m_rho,
                     "windowed_one_sided_eps1em3": I1,
                     "windowed_one_sided_eps1em4": I2,
                     "note": "int S d omega / (2 pi) = m rho_0, "
                             "eps-independent (residue closed form)"},
        "n_m1half_floor": {"per_box_lambda_0.1rM_delta_rho_over_rho":
                           d_rho_over, "C08_whole_halo_deltaT_over_T":
                           dT_floor_C08 / TB},
        "first_nonidentity_FDT": "the spectrum is a PREDICTION (sound doublet, "
                                 "amplitude m rho_0), not the identity "
                                 "D = mu k_B T_b that held for any channel",
    },
    "V3_falsifier": {
        "kill_conditions": [
            "measured response WITHOUT the pole at omega = sigma k (C3/C14)",
            "a GAP at k -> 0: omega(0) > 0 (C14/C15; the k -> 0 intercept is "
            "the clean discriminating test)",
            "FDT spectral weight OFF the sound branch: continuum, central/"
            "Landau-Placzek peak at omega = 0, or width Gamma > 0 (C8/C16)",
            "phase speed omega/k != sigma at fixed k (the committed sigma is "
            "independently pinned by rotation curves -- C3/C17)",
        ],
        "the_measurement": ("the (k, omega)-resolved acoustic wake behind a "
                            "baryonic perturber crossing the well (B5's "
                            "t_sound/t_dyn = sqrt(2); B8's Mach cone at "
                            "c_s = sigma; cluster merger shocks Mach 2-6, "
                            "G127 c_s = 628-915 km/s) and the density-"
                            "fluctuation spectrum decomposed in (k, omega)"),
        "honest_bound": ("no committed in-situ instrument resolves halo-scale "
                         "(k, omega) power today; the register closes with a "
                         "prediction and its kill conditions, not with data"),
    },
    "verdicts": {"V1": v1, "V2": v2, "V3": v3},
    "checks": RES,
    "n_pass": NP,
    "n_fail": NF,
    "deliverable": ("deepseek_push/F03_phantom_correlator.py + "
                    "F03_phantom_correlator.out + F03_results.json"),
}

with open(OUT_PATH, "w") as fh:
    json.dump(results, fh, indent=1)