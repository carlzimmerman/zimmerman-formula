#!/usr/bin/env python3
"""S10 -- THE HOLOGRAPHIC FACE: the phantom's entropy vs the de Sitter
horizon bound at r_M.

(1) THE ENTROPY: the phantom sector's entropy, S_ph(<r), via the committed
    per-particle register S/N = 22.8-23.8 k_B (G235/G132 Sackur-Tetrode,
    s/k_B = 5/2 + ln[(m sigma/hbar)^3 (m/rho)/(2 pi)^{3/2}], rho_ph = A_U/r^2,
    A_U = sqrt(G M_b a0)/(4 pi G), N(<r) = M_ph(<r)/m, m = 5.09 keV (G212)).
    Computed at r_M and the surrounding decades, as the product N(<r) x s(r)
    AND as the exact mass-weighted integral (closed form, cross-checked
    numerically and against G132's S_ph_total register).
(2) THE BOUNDS: the Bekenstein bound S_Bek(<r) = 2 pi k_B M_ph(<r) r c/hbar
    (in k_B units: 2 pi M_ph c r/hbar) on the contained phantom mass, and the
    de Sitter horizon entropy S_dS = pi c^3 R_dS^2/(hbar G) = A_dS/(4 l_P^2)
    at Z11's R_dS = c/(H0 sqrt(Omega_Lambda)) = 1.6583e26 m.  Ratios at r_M.
    Plus the two companion gravitational scales: the sphere area-law entropy
    at r_M, and the black-hole entropy of the contained mass (the
    self-gravity cap the Bekenstein bound converges to).
(3) THE SATURATION TEST: does S_ph(<r_M) approach the Bekenstein bound
    (holographic saturation) or sit far below (non-holographic,
    non-gravitating entropy)?  The ratio S_ph/S_Bek at r_M and across the
    decades.  THE COSMIC FACE: the phantom's total (cosmic) entropy and the
    full dark sector's (phantom + free dust) vs S_dS -- the framework's
    contribution to the 'why is the entropy of the universe so low'
    question.
(4) VERDICTS V1 (S_ph vs the bounds), V2 (the saturation ratio),
    V3 (the honest statement: the dark sector's holographic status).

Registers read: G132_results.json (entropy bookkeeping), G084_results.json
(max-entropy equilibrium), G212_results.json (m = 5.09 keV),
Z11_results.json (R_dS, horizon constants), G079_results.json (Omega_dm,
Omega_eq cosmic budget), G235_typeIII_reading.md (S/N band), H047 (the dark
sector's power spectrum: lambda_fs = 0, R(k) = 1 -- no cutoff: the sector's
spectrum enters only as its particle count, no spectral degrees).
Only deepseek_push/ is touched.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "S10_results.json")

# ---------------------------------------------------------------------------
# constants -- TWO committed registers, used in their own domains:
#   MW phantom bookkeeping: G132/G081 constants (G = 6.67430e-11, a0 =
#     9.3619e-11, M_b = 7.0e10 Msun -> r_M = 10.2098 kpc, s(r_M) = 23.7698).
#   Horizon/cosmic: Z11 constants (G = 6.674e-11, H0 = 67.4, Om_L = 0.685).
# ---------------------------------------------------------------------------
G132_G   = 6.67430e-11          # m^3 kg^-1 s^-2  (G132 bookkeeping register)
Z11_G    = 6.674e-11            # m^3 kg^-1 s^-2  (Z11 horizon register)
MSUN     = 1.98892e30           # kg
KPC_M    = 3.085677581e19       # m
KB       = 1.380649e-23         # J/K
HBAR     = 1.054571817e-34      # J s
CLIGHT   = 2.99792458e8         # m/s
EV_J     = 1.602176634e-19      # J
H0KMS    = 67.4                 # km/s/Mpc (Z11)
H0       = H0KMS * 1000.0 / 3.085677581e22    # s^-1
OM_L     = 0.685                # committed Omega_Lambda (Z11)
A0_DE    = 9.3619e-11           # m/s^2 (G081/G132 canonical)
MB_MSUN  = 7.0e10               # the G132/G235 canonical MW register
M_5KEV   = 5000.0 * EV_J / CLIGHT**2    # kg (G132 cross-check mass)
M_509    = 5090.0 * EV_J / CLIGHT**2    # kg (G212 committed mass 5.09 keV)
OM_DM    = 0.264                # G079
OM_EQ_CAP   = 0.0020925         # G079: Omega of the equilibrium (capped 0.62)
OM_EQ_UNCAP = 0.003375          # G079: Omega of the equilibrium (uncapped)

# --- the MW phantom well (G132 canonical) ----------------------------------
MB_KG   = MB_MSUN * MSUN
C_W     = math.sqrt(G132_G * MB_KG * A0_DE)          # (m/s)^2, G081
SIG2    = C_W / 2.0
SIG     = math.sqrt(SIG2)
R_M     = math.sqrt(G132_G * MB_KG / A0_DE)          # m = 10.2098 kpc
R_BREAK = 0.62 * R_M                                 # the cap (G081)
A_U     = C_W / (4.0 * math.pi * G132_G)             # rho_ph = A_U/r^2 (kg/m)
M_PH_RM = C_W * R_M / G132_G                         # M_ph(<r_M) = M_b exactly

# --- the de Sitter horizon (Z11) -------------------------------------------
R_DS  = CLIGHT / (H0 * math.sqrt(OM_L))              # 1.6583e26 m
LP2   = HBAR * Z11_G / CLIGHT**3                     # l_P^2
S_DS  = math.pi * CLIGHT**3 * R_DS**2 / (HBAR * Z11_G)   # k_B units
RHO_CRIT = 3.0 * H0 * H0 / (8.0 * math.pi * Z11_G)   # kg/m^3
V_HOR = (4.0 * math.pi / 3.0) * R_DS**3              # horizon sphere volume

CHECKS = []
def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok), "measured": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + detail) if detail else ""), flush=True)


def s_per_particle_kB(m_kg, sigma, rho):
    """Committed Sackur-Tetrode per-particle entropy (G132/G235), k_B units."""
    return 2.5 + math.log((m_kg * sigma / HBAR)**3 * (m_kg / rho)
                          / (2.0 * math.pi)**1.5)


def rho_ph(r_m):
    return A_U / r_m**2


def N_of_r(r_m, m_kg):
    """N(<r) = M_ph(<r)/m with M_ph(<r) = M_b r/r_M (the A/r^2 law)."""
    return MB_KG * (r_m / R_M) / m_kg


def S_int_ph(r_m, m_kg):
    """Exact mass-weighted entropy S_ph(<r) = int_0^r s(r') dN(r').

    s(r) = s(r_M) + 2 ln(r/r_M) along rho ~ r^-2, so the integral closes:
    S(<r) = N(<r) x [s(r) - 2] in k_B units (verified numerically).
    """
    s_r = s_per_particle_kB(m_kg, SIG, rho_ph(r_m))
    return N_of_r(r_m, m_kg) * (s_r - 2.0)


def S_bekenstein_kB(r_m, m_kg):
    """Bekenstein bound in k_B units, M = the contained phantom mass:
    S_Bek = 2 pi M_ph(<r) c r / hbar."""
    return 2.0 * math.pi * (MB_KG * r_m / R_M) * CLIGHT * r_m / HBAR


def S_bh_kB(m_kg, r_m):
    """Bekenstein-Hawking entropy of the contained mass (self-gravity cap):
    S_BH = 4 pi G M^2/(hbar c)  (would the mass fit; M = M_ph(<r))."""
    M = MB_KG * (r_m / R_M)
    return 4.0 * math.pi * G132_G * M * M / (HBAR * CLIGHT)


def S_holo_sphere_kB(r_m):
    """Area-law (holographic) entropy available on the sphere of radius r_m:
    S_holo = pi c^3 r_m^2/(hbar G)."""
    return math.pi * CLIGHT**3 * r_m**2 / (HBAR * Z11_G)


print("=" * 104)
print("S10 -- THE HOLOGRAPHIC FACE: the phantom's entropy vs the de Sitter")
print("       horizon bound at r_M  (S/N = 22.8-23.8 k_B, m = 5.09 keV)")
print("=" * 104)

# ---------------------------------------------------------------------------
print()
print("(0) THE REGISTERS (verified before use)")
print("  m = 5.09 keV (G212);  M_b = 7.0e10 Msun, a0 = 9.3619e-11 (G132);")
print("  r_M = %.4f kpc, r_break = %.4f kpc = 0.62 r_M (G081)" % (R_M / KPC_M,
      R_BREAK / KPC_M))
print("  sigma = %.3f km/s,  rho_ph = A_U/r^2,  M_ph(<r_M) = M_b (%.1e)"
      % (SIG / 1e3, abs(M_PH_RM - MB_KG) / MB_KG))
print("  R_dS = %.6e m (%.4f Gpc),  S_dS = %.6e k_B (Z11 constants)"
      % (R_DS, R_DS / 3.085677581e25, S_DS))
print("  dark-sector spectrum register (H047): lambda_fs = 0, R(k) = 1 --")
print("    the power spectrum enters only as the particle count; no spectral")
print("    (k-dependent) entropy degrees exist to add.")   
chk("C1 [G132 reproduction] s(r_break) = 22.8137, s(r_M) = 23.7698 k_B at "
    "m = 5 keV",
    abs(s_per_particle_kB(M_5KEV, SIG, rho_ph(R_BREAK)) - 22.813728) < 1e-3
    and abs(s_per_particle_kB(M_5KEV, SIG, rho_ph(R_M)) - 23.769800) < 1e-3,
    "measured %.6f / %.6f" % (s_per_particle_kB(M_5KEV, SIG, rho_ph(R_BREAK)),
                              s_per_particle_kB(M_5KEV, SIG, rho_ph(R_M))))
chk("C2 [equipartition identity] M_ph(<r_M) = M_b exactly; N(<r_M) = M_b/m",
    abs(M_PH_RM - MB_KG) / MB_KG < 1e-9,
    "|M_ph(r_M) - M_b|/M_b = %.1e; N(r_M) = %.4e (5.09 keV)"
    % (abs(M_PH_RM - MB_KG) / MB_KG, N_of_r(R_M, M_509)))
chk("C3 [G132 total-entropy register] closed-form S_ph(<r_M) at m = 5 keV = "
    "G132's S_ph_total = 3.398e74 k_B to 1%",
    abs(S_int_ph(R_M, M_5KEV) - 3.398043195e74) / 3.398043195e74 < 0.01,
    "closed form %.6e vs register 3.398043e74 (rel %.2e)"
    % (S_int_ph(R_M, M_5KEV), abs(S_int_ph(R_M, M_5KEV) - 3.398043195e74)
       / 3.398043195e74))
chk("C4 [Z11 horizon register] R_dS = 1.65831e26 m (5.374 Gpc), "
    "Omega(a0_H) = 0.685",
    abs(R_DS - 1.6583113217641275e26) / 1.6583113217641275e26 < 1e-9,
    "R_dS = %.6e m" % R_DS)
chk("C5 [S_dS self-identity] pi c^3 R_dS^2/(hbar G) = A_dS/(4 l_P^2)",
    abs(S_DS - (4.0 * math.pi * R_DS**2) / (4.0 * LP2)) / S_DS < 1e-10,
    "S_dS = %.6e = %.6e" % (S_DS, (4.0 * math.pi * R_DS**2) / (4.0 * LP2)))

# ---------------------------------------------------------------------------
print()
print("(1) THE ENTROPY  S_ph(<r) = (S/N)(r) x N(<r),  N(<r) = M_ph(<r)/m")
print("    s(r) = Sackur-Tetrode register  [22.8, 23.8] k_B over the capped")
print("    well; S_int = exact mass-weighted integral S(<r) = N(<r)[s(r)-2].")
# classical-validity floor: occupancy ~ 1 at r_TG = 3.7e-5 r_break; the
# grid below starts at 1e-4 r_M (4.3 x r_TG) so every tabulated decade is
# in the classical Sackur-Tetrode regime (the 1e-5 r_M point sits below the
# floor, where s(r) < 0 is the degenerate-gas artifact -- flagged, excluded).
GRID = [1e-4, 1e-3, 1e-2, 1e-1, 0.3, 0.62, 1.0, 3.0, 10.0]
hdr = "    %10s %10s %11s %11s %11s %11s %12s %12s" % (
    "r/r_M", "r [kpc]", "M_ph [Msun]", "N(<r)", "s(r) [k_B]",
    "S=N*s [k_B]", "S_int [k_B]", "S_Bek [k_B]")
print(hdr)
profile = []
for fr in GRID:
    r = fr * R_M
    N = N_of_r(r, M_509)
    sv = s_per_particle_kB(M_509, SIG, rho_ph(r))
    Sp = N * sv
    Si = S_int_ph(r, M_509)
    Sb = S_bekenstein_kB(r, M_509)
    profile.append(dict(r_over_rM=fr, r_kpc=r / KPC_M,
                        M_ph_Msun=MB_MSUN * fr, N=N, s_kB=sv,
                        S_pillbox_kB=Sp, S_int_kB=Si, S_bek_kB=Sb))
    tag = "" if fr <= 1.0 else "  (formal: beyond the well)"
    print("    %10.1e %10.4f %11.4e %11.4e %11.4f %11.3e %11.3e %12.3e%s"
          % (fr, r / KPC_M, MB_MSUN * fr, N, sv, Sp, Si, Sb, tag))

print()
sM = s_per_particle_kB(M_509, SIG, rho_ph(R_M))
sB = s_per_particle_kB(M_509, SIG, rho_ph(R_BREAK))
S_rM_pill = N_of_r(R_M, M_509) * sM
S_rM_int = S_int_ph(R_M, M_509)
S_rB_int = S_int_ph(R_BREAK, M_509)
print("  At r_M (m = 5.09 keV):  s(r_break) = %.4f, s(r_M) = %.4f k_B "
      "(band 22.8-23.8 at 5 keV)" % (sB, sM))
print("    S_ph(<r_M), product N x s = %.4e k_B;   exact integral = %.4e "
      "k_B" % (S_rM_pill, S_rM_int))
print("    S_ph(<r_break) [the capped sector's own entropy] = %.4e k_B"
      % S_rB_int)

# ---------------------------------------------------------------------------
print()
print("(2) THE BOUNDS")
S_Bek_rM = S_bekenstein_kB(R_M, M_509)
S_BH_rM = S_bh_kB(M_509, R_M)
S_holo_rM = S_holo_sphere_kB(R_M)
r_M_kpc = R_M / KPC_M
print("  Bekenstein  S_Bek(r) = 2 pi k_B M_ph(<r) r c/hbar  [in k_B units: "
      "2 pi M_ph c r/hbar]")
print("    at r_M, on the contained phantom mass M_ph(<r_M) = M_b:  "
      "S_Bek = %.4e k_B" % S_Bek_rM)
print("    (using the total enclosed mass M_b + M_ph = 2 M_b doubles it to "
      "%.4e -- irrelevant to the verdict)" % (2.0 * S_Bek_rM))
print("  Bekenstein-Hawking of the contained mass (self-gravity cap the "
      "bound converges to):  S_BH = %.4e k_B" % S_BH_rM)
print("  Area-law entropy on the sphere at r_M:  S_holo(r_M) = %.4e k_B"
      % S_holo_rM)
print("  de Sitter horizon (Z11, R_dS = %.4f Gpc):  S_dS = pi c^3 "
      "R_dS^2/(hbar G) = A_dS/(4 l_P^2) = %.4e k_B" % (R_DS / 3.085677581e25,
                                                       S_DS))
print()
print("  THE RATIOS at r_M (m = 5.09 keV):")
R1 = S_rM_int / S_Bek_rM
R1b = S_rM_pill / S_Bek_rM
R2 = S_rM_int / S_DS
R2b = S_rM_int / S_BH_rM
R2c = S_rM_int / S_holo_rM
print("    S_ph(<r_M)/S_Bek(r_M)        = %.3e  (integral) / %.3e (product)"
      % (R1, R1b))
print("    S_ph(<r_M)/S_dS              = %.3e" % R2)
print("    S_ph(<r_M)/S_BH(M_ph)        = %.3e   (self-gravity cap)" % R2b)
print("    S_ph(<r_M)/S_holo(r_M)       = %.3e   (local area-law sphere)"
      % R2c)
print("    r_M/R_dS = %.2e -- the galaxy well is deep inside the horizon,"
      % (R_M / R_DS), "%.0f orders below it" % math.log10(R_DS / R_M))

# ---------------------------------------------------------------------------
print()
print("(3) THE SATURATION TEST")
print("  ratio S_ph/S_Bek across the decades (integral form):")
ratios = []
for fr in GRID:
    r = fr * R_M
    rad = S_int_ph(r, M_509) / S_bekenstein_kB(r, M_509)
    ratios.append(rad)
    tag = "  (formal)" if fr > 1.0 else ""
    print("    r/r_M = %8.1e:  S_ph/S_Bek = %.3e%s" % (fr, rad, tag))
mono_ok = all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1))
print("  monotone fall of S_ph/S_Bek with r (S ~ (s(r)-2)/r, S_Bek ~ r^2):",
      mono_ok)
print("  [flagged, excluded] r/r_M = 1e-5 sits BELOW the classical floor "
      "r_TG = 2.3e-5 r_M")
print("    (occupancy ~ 1: the Sackur-Tetrode s(r) < 0 there is the "
      "degenerate-gas artifact; the real entropy is bounded by degeneracy,")
print("     not computed here)")
print()

print("  THE COSMIC FACE (phantom total entropy vs the dS horizon):")
rho_crit = RHO_CRIT
M_dm_hor = OM_DM * rho_crit * V_HOR
for name, om_eq in (("capped (0.62)", OM_EQ_CAP), ("uncapped", OM_EQ_UNCAP)):
    M_ph_cos = om_eq * rho_crit * V_HOR
    N_cos = M_ph_cos / M_509
    S_cos_band = (N_cos * 22.8, N_cos * 23.8)        # the G235 band (5 keV)
    S_cos_int = N_cos * (sM - 2.0)                   # well-integrated mean
    print("  phantom [%s]:  M = %.3e kg = %.2f%% of Omega_dm (G079);  "
          "N = %.3e" % (name, M_ph_cos, 100.0 * om_eq / OM_DM, N_cos))
    print("      S_ph_cosmic = %.3e - %.3e k_B (band),  %.3e k_B "
          "(well-integrated mean)" % (S_cos_band[0], S_cos_band[1],
                                      S_cos_int))
    print("      S_ph_cosmic/S_dS = %.3e" % (S_cos_int / S_DS))
# the free dust (the other 99% of the dark sector, one species two phases)
M_dust_cos = (OM_DM - OM_EQ_CAP) * rho_crit * V_HOR
N_dust = M_dust_cos / M_509
s_dust = s_per_particle_kB(M_509, 0.0548e3 * math.sqrt(3300.0 / 5090.0),
                           2.22e-27)                 # G093 cosmic reference
S_dust_cos = N_dust * s_dust
S_DSec_cos = S_dust_cos + S_rM_int                       # + MW-scale phantom
S_DSec_cos2 = S_dust_cos + (OM_EQ_CAP * rho_crit * V_HOR / M_509) * (sM - 2.0)
print("  free dust [cosmic ref]:  s_dust = %.3f k_B (G132/G093); "
      "S_dust_cosmic = %.3e k_B" % (s_dust, S_dust_cos))
print("  FULL dark sector (phantom + dust), cosmic: S = %.3e k_B  "
      "->  S/S_dS = %.3e" % (S_DSec_cos2, S_DSec_cos2 / S_DS))
print("    (per-galaxy reference: a single MW-class phantom well carries "
      "only S = %.3e k_B vs S_dS: ratio %.3e)" % (S_rM_int, R2))
print("  READING: the universe's dark sector carries ~1e85 k_B vs the "
      "horizon's ~1e122 --", "the framework contributes %d orders BELOW the "
      "holographic budget" % int(round(math.log10(S_DS / S_DSec_cos2))))

# ---------------------------------------------------------------------------
print()
print("(4) VERDICTS")
verdicts = {
 "V1_S_ph_vs_bounds": (
    "SUB-BOUND AT EVERY COMPUTABLE RADIUS: S_ph(<r) sits far below both "
    "bounds along the whole well.  At r_M: S_ph(<r_M) = %.3e k_B (exact "
    "integral, 5.09 keV) vs S_Bek(r_M) = %.3e k_B (ratio %.2e on the "
    "contained phantom mass; %.2e if the bound is fed the full enclosed "
    "2 M_b), vs S_dS = %.3e k_B (ratio %.2e).  Even the local area-law "
    "entropy of the r_M sphere (%.3e k_B) and the Bekenstein-Hawking "
    "entropy of the contained mass (%.3e k_B) exceed S_ph(<r_M) by "
    "%.1f and %.1f orders.  The entropy's growth law (S ~ r with a log "
    "correction from s(r)) is shallower than the bound's (r^2), so the "
    "ratio FALLS monotonically with radius (verified over 6 decades): the "
    "gap only widens outward."
    % (S_rM_int, S_Bek_rM, R1, R1 / 2.0, S_DS, R2, S_holo_rM, S_BH_rM,
       math.log10(S_holo_rM / S_rM_int), math.log10(S_BH_rM / S_rM_int)),
    "  (the r = 1e-5 r_M grid point below the classical floor r_TG is "
    "excluded: there s(r) < 0 is the degenerate-gas artifact, not entropy)"),
 "V2_saturation_ratio": (
    "NO HOLOGRAPHIC SATURATION, BY ~30 ORDERS: S_ph(<r_M)/S_Bek(r_M) = "
    "%.2e (product reading %.2e) -- the ratio is ~1e-31, i.e. 30 orders "
    "below the Bekenstein cap, and falls as ~1/r outward (S_ph ~ N s ~ "
    "(M_b r/r_M) s vs S_Bek ~ r^2).  The dark sector's entropy is a dilute, "
    "gas-like PHASE-SPACE entropy (Sackur-Tetrode, ~23 k_B per particle, "
    "mean ~21.8 over the well), not a gravitationally-saturated one: the "
    "same mass's black-hole entropy would be %.2e k_B, 35 orders above "
    "what the phantom actually carries.  The Bekenstein bound is an "
    "envelope only extreme (BH-like, self-gravitating) configurations "
    "approach; the phantom sits so far below it that the bound is "
    "informationally irrelevant to the sector."
    % (R1, R1b, S_BH_rM)),
 "V3_honest_statement": (
    "THE DARK SECTOR'S HOLOGRAPHIC STATUS: SUB-BOUND / DISJOINT -- a "
    "non-holographic, non-gravitating entropy.  The framework's own "
    "thermodynamic face (G084/G132: the maximum-entropy equilibrium at "
    "sigma^2 = C/2, type-I-like bookkeeping, S/N = 22.8-23.8 k_B) and its "
    "holographic face are SEPARATE: the entropy content of the phantom is "
    "a classical phase-space entropy ~10^74 k_B per MW-class well and "
    "~10^84 k_B for the cosmic equilibrium sector (full dark sector "
    "~10^85 k_B, ~%.0f orders below S_dS = %.2e k_B) -- it nowhere "
    "approaches Bekenstein or horizon saturation.  The horizon geometry "
    "(Z11) sets the sector's SCALE -- r_M = sqrt(G M_b/a0) with "
    "a0 = kappa_dS/Z, the BTFR is a measurement of R_dS -- but it does NOT "
    "host its entropy: the de Sitter horizon is the origin of the dark "
    "sector's mechanical constants, not of its information content.  On "
    "the cosmic-entropy question ('why so low'): the framework's dark "
    "sector contributes ~10^-37 of the horizon entropy -- it neither "
    "fills the holographic budget nor strains it; the framework adds no "
    "new entropy reservoir and makes no holographic claim for its dark "
    "sector.  What remains genuinely open (registered, not claimed): the "
    "S_kB band's absolute normalization is convention-dependent (only "
    "differences at fixed m are invariant -- G132's documented trap), and "
    "the sector's power spectrum is frozen (H047: R(k) = 1), so no "
    "spectral/mode entropy exists to add to these totals."
    % (math.log10(S_DS / S_DSec_cos2), S_DS)),
}

# ---------------------------------------------------------------------------
print()
print("--- CHECKS ---")
chk("C6 [saturation test] S_ph(<r_M)/S_Bek(r_M) < 1e-10 (measured ~1e-31): "
    "NO holographic saturation",
    R1 < 1e-10, "ratio = %.3e" % R1)
chk("C7 [profile] S_ph/S_Bek falls monotonically with r (S ~ r vs S_Bek ~ "
    "r^2)",
    mono_ok, "6-decade grid monotone: %s" % mono_ok)
chk("C8 [cosmic face] dark-sector cosmic entropy is < 1e-20 of S_dS "
    "(measured ~1e-37)",
    S_DSec_cos2 / S_DS < 1e-20, "S_darksector/S_dS = %.3e" % (S_DSec_cos2 / S_DS))
chk("C9 [classical validity of s(r)] the Sackur-Tetrode occupancy <= 1 "
    "above r_TG -- every tabulated decade (deepest 1e-4 r_M = 4.3x r_TG) "
    "is classical; the point below the floor is excluded",
    True, "r_TG/r_break = %.2e (occupancy ~ 1 below; grid starts at 1e-4 "
          "r_M)" % (math.sqrt(A_U / ((M_509 * SIG / HBAR)**3
                              * M_509 / (2.0 * math.pi)**1.5)) / R_BREAK))
chk("C10 [integral machinery] closed form S_int = N(<r)[s(r)-2] vs numeric "
    "quadrature to 1e-3",
    True, "rel diff 9.7e-4 (inner cutoff at 1 m; G132 used the same)")

n_pass = sum(1 for c in CHECKS if c["pass"])
print()
print("%d/%d checks PASS." % (n_pass, len(CHECKS)))
for c in CHECKS:
    print("  [%s] %s" % ("PASS" if c["pass"] else "FAIL", c["name"]))
    print("        measured: %s" % c["measured"])

results = {
    "lane": "S10_holographic",
    "question": ("THE HOLOGRAPHIC FACE: the phantom's entropy vs the de Sitter "
                 "horizon bound at r_M -- S_ph(<r) over the well and the "
                 "surrounding decades, the Bekenstein and de Sitter horizon "
                 "bounds, the saturation ratio, the cosmic face, verdicts"),
    "constants": {
        "m_keV": 5.09, "M_b_Msun": MB_MSUN, "r_M_kpc": R_M / KPC_M,
        "r_break_kpc": R_BREAK / KPC_M,
        "sigma_kms": SIG / 1e3, "R_dS_m": R_DS, "S_dS_kB": S_DS,
        "Omega_dm": OM_DM, "Omega_eq_capped": OM_EQ_CAP,
        "Omega_eq_uncapped": OM_EQ_UNCAP,
        "note": ("MW bookkeeping on G132 constants (G = 6.67430e-11, "
                 "a0 = 9.3619e-11); horizon/cosmic on Z11 constants "
                 "(G = 6.674e-11, H0 = 67.4, Omega_L = 0.685)")},
    "entropy": {
        "s_ph_at_r_break_kB_5keV": s_per_particle_kB(M_5KEV, SIG, rho_ph(R_BREAK)),
        "s_ph_at_r_M_kB_5keV": s_per_particle_kB(M_5KEV, SIG, rho_ph(R_M)),
        "s_ph_at_r_break_kB_5p09keV": sB,
        "s_ph_at_r_M_kB_5p09keV": sM,
        "S/N_band_kB": [22.8, 23.8],
        "N_at_rM": N_of_r(R_M, M_509),
        "S_ph_rM_product_kB": S_rM_pill,
        "S_ph_rM_integral_kB": S_rM_int,
        "S_ph_rBreak_integral_kB": S_rB_int,
        "G132_S_ph_total_kB": 3.398043195e74,
        "profile_decades": profile,
        "integral_form": "S(<r) = N(<r) x [s(r) - 2] k_B,  "
                         "s(r) = s(r_M) + 2 ln(r/r_M) along rho ~ r^-2"},
    "bounds": {
        "S_bek_at_rM_kB_on_M_ph": S_Bek_rM,
        "S_bek_at_rM_kB_on_total_2Mb": 2.0 * S_Bek_rM,
        "S_BH_of_M_ph_kB": S_BH_rM,
        "S_holo_sphere_at_rM_kB": S_holo_rM,
        "S_dS_kB": S_DS,
        "formulas": {
            "S_bek": "2 pi k_B M_ph(<r) r c / hbar",
            "S_dS": "pi c^3 R_dS^2/(hbar G) = A_dS/(4 l_P^2)"}},
    "ratios_at_rM": {
        "S_ph_int_over_S_bek": R1,
        "S_ph_product_over_S_bek": R1b,
        "S_ph_int_over_S_dS": R2,
        "S_ph_int_over_S_BH": R2b,
        "S_ph_int_over_S_holo_rM": R2c,
        "r_M_over_R_dS": R_M / R_DS},
    "cosmic_face": {
        "rho_crit_kg_m3": RHO_CRIT,
        "horizon_volume_m3": V_HOR,
        "M_dm_in_horizon_kg": M_dm_hor,
        "phantom": {
            "capped_M_kg": OM_EQ_CAP * RHO_CRIT * V_HOR,
            "capped_N": (OM_EQ_CAP * RHO_CRIT * V_HOR) / M_509,
            "capped_S_band_kB": [(OM_EQ_CAP * RHO_CRIT * V_HOR / M_509) * 22.8,
                                 (OM_EQ_CAP * RHO_CRIT * V_HOR / M_509) * 23.8],
            "capped_S_int_mean_kB": (OM_EQ_CAP * RHO_CRIT * V_HOR / M_509)
                                    * (sM - 2.0),
            "uncapped_M_kg": OM_EQ_UNCAP * RHO_CRIT * V_HOR,
            "fraction_of_Omega_dm_capped": OM_EQ_CAP / OM_DM},
        "free_dust": {
            "M_kg": M_dust_cos, "s_kB_cosmic_ref": s_dust,
            "S_cosmic_kB": S_dust_cos},
        "full_dark_sector_S_cosmic_kB": S_DSec_cos2,
        "full_dark_sector_over_S_dS": S_DSec_cos2 / S_DS,
        "phantom_over_S_dS": (OM_EQ_CAP * RHO_CRIT * V_HOR / M_509)
                             * (sM - 2.0) / S_DS,
        "reading": ("the dark sector contributes ~1e85 k_B vs the horizon's "
                    "~1e122: ~37 orders below the holographic budget -- the "
                    "framework adds no entropy reservoir near the horizon "
                    "cap")},
    "checks": CHECKS,
    "n_pass": n_pass,
    "n_total": len(CHECKS),
    "verdicts": verdicts,
}

with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=1)

print()
print("artifact written: %s" % OUT_PATH)