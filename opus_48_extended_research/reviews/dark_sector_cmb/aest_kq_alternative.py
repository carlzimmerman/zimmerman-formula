#!/usr/bin/env python3
"""
aest_kq_alternative.py  (topic: aest_kq_alternative)
====================================================
Does the AeST K(Q) "dark-matter-mimic" field let the Zimmerman framework do the
CMB third peak WITHOUT a dark particle, or does it just RELOCATE the free function?

Three calculations, all both-ways, quarantine held (a0/Z NOT asserted derived):

  (a) THE THIRD-PEAK MECHANISM: the AeST shift-symmetric scalar redshifts as a^-3
      (dust). Show numerically that (i) a baryon-only / modified-inertia universe
      cannot make the 3rd peak and (ii) you need ~Omega_dm of a^-3 clustering
      density -- i.e. AeST's K(Q) dust is doing the LCDM-DM job, by amount.

  (b) a0-vs-K(Q) INDEPENDENCE: is a0 = c^2 sqrt(Lambda/32pi) tied to the AeST CMB
      fit? Check whether the dust amplitude (Q0*I0 -> Omega_dust) is a FUNCTION of
      a0/Lambda, or an orthogonal integration constant. Quantify the "why-now"
      ratio Omega_dust/Omega_DE that a0=sqrt(Lambda) does NOT predict.

  (c) HOT-vs-COLD third-peak tension (the task's KEY TENSION): AeST's K(Q) dust is
      a FIELD condensate (effectively cold, w=0, c_s^2~0 on sub-horizon scales) and
      has NO free-streaming -- UNLIKE Angus's 11-eV hot sterile neutrino. So the
      FIELD route does NOT inherit the hot/cold tension that the PARTICLE route
      (cluster-hot vs CMB-cold) does. Quantify both, and the Cassini/CMB co-test
      that the V(Q) modification (no Y^3/2 suppression) leaves OPEN.

Sources (primary, verified this session):
  Skordis & Zlosnik 2021, PRL 127 161302 (arXiv:2007.00082)
  Durakovic & Skordis 2024, JCAP 04 040 (arXiv:2312.00889)  [Q=Q0+I0(1+z)^3; Omega set by I0]
  Verwayen, Skordis & Zlosnik 2024, MNRAS 531 272 (arXiv:2304.05134)  [mu free; Helmholtz]
  Corpus: ROUTE2_CMB_THROUGH_AEST_2026-06-15.md, ROUTE_AEST_JOINT_COEFFICIENT_2026-06-15.md,
          SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER_2026-06-15.md, CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md
"""
import numpy as np

c     = 2.99792458e8         # m/s
G     = 6.674e-11
H0    = 2.197e-18            # s^-1 (67.7 km/s/Mpc)
Mpc   = 3.0857e22            # m
eV    = 1.602e-19            # J
kB    = 1.381e-23
hbar  = 1.0546e-34

print("="*78)
print("(a) THIRD-PEAK MECHANISM: AeST K(Q) scalar redshifts as a^-3 (dust)")
print("="*78)
# AeST FLRW: shift-symmetric scalar -> dK/dQ = I0/a^3  =>  rho ~ rho0/a^3 (PRL Eq.3-4).
# The a^-3 scaling is the SAME redshift law as pressureless CDM. Show the 3rd-peak
# obstruction is branch-independent: a clustering a^-3 density of ~Omega_dm is REQUIRED.

# Banked real-CAMB result (cmb_third_peak_dm_mimic.py, ROUTE2 deepdive), reproduced here
# as the calibrated P3/P2 vs Omega_c h^2 monotone curve (CAMB 1.6.6):
Omega_c_h2 = np.array([0.000, 0.030, 0.060, 0.090, 0.1202])   # baryon-only -> LCDM
P3_over_P2 = np.array([0.527, 0.673, 0.793, 0.894, 0.980])     # real CAMB (banked)
print(" P3/P2 vs clustering (a^-3) density Omega_c h^2 (real CAMB 1.6.6, banked):")
for x,y in zip(Omega_c_h2, P3_over_P2):
    tag = "  <- baryon/MI-only: 3rd peak CRUSHED" if x==0 else ("  <- Planck/LCDM" if x>0.11 else "")
    print(f"   Omega_c h^2={x:.4f}  ->  P3/P2={y:.3f}{tag}")
# Planck observed P3/P2 ~ 0.98; baryon-only best (any tuning) ~ 0.54.
need = 0.1202   # the a^-3 clustering density the 3rd peak demands (= LCDM DM)
print(f"\n  Planck observes P3/P2 ~ 0.98  ->  REQUIRES Omega_c h^2 ~ {need:.4f}")
print( "  a0 is ABSENT from linear perturbations (Bridge-1) -> adds 0 to transfer fns.")
print( "  => the 3rd peak is a BRANCH-INDEPENDENT demand for an a^-3 CLUSTERING field.")
print( "  AeST's K(Q) scalar IS that field (a^-3 dust). MECHANISM = REAL (credit it).")

print()
print("="*78)
print("(b) IS a0 = c^2 sqrt(Lambda/32pi) TIED TO THE AeST DUST AMPLITUDE? -> NO")
print("="*78)
# a0 from the framework (pure-Lambda footing):
OmL   = 0.685
rho_crit = 3*H0**2/(8*np.pi*G)
rho_DE   = OmL*rho_crit
Lambda   = 8*np.pi*G*rho_DE/c**2 * 3/ (3)        # Lambda = 8piG rho_DE / c^2 ... keep dim check below
# canonical: a0 = c^2 sqrt(Lambda/(32 pi)), Lambda = 3 OmL H0^2 / c^2
Lambda  = 3*OmL*H0**2/c**2
a0      = c**2*np.sqrt(Lambda/(32*np.pi))
print(f"  Lambda            = {Lambda:.3e} m^-2")
print(f"  a0 = c^2 sqrt(Lambda/32pi) = {a0:.3e} m/s^2   (target 9.36e-11)")
print(f"  => a0 fixes the DARK-ENERGY face: Omega_DE = {OmL:.3f}  (REAL unification, z=0)")

# The AeST dust amplitude:  8 pi Gtilde rho_dust0 = Q0 * I0   (PRL).
# I0 is a FREE initial condition: "the density rho-bar is not (classically) predicted"
# Q0 is a free K-expansion constant. NEITHER is a function of a0 or Lambda.
# a0 lives in the Y-sector (Y^3/2 / J(Y)); Lambda+dust live in the ORTHOGONAL Q-sector.
Omega_dm = 0.1202/0.677**2     # ~0.262
print(f"\n  Dust amplitude 8piG~ rho_dust0 = Q0 * I0  (I0 = FREE initial condition).")
print(f"  Durakovic-Skordis 2024: Q = Q0 + I0 (1+z)^3 ; Omega_AeST 'set by I0'.")
print(f"  => Omega_dust must be TUNED to ~{Omega_dm:.3f} to fit the 3rd peak.")
why_now = Omega_dm / OmL
print(f"\n  'why-now' ratio Omega_dust / Omega_DE = {why_now:.3f}  (an O(1) coincidence)")
print(f"  a0=c^2 sqrt(Lambda/32pi) does NOT predict this ratio: a0 and I0 are")
print(f"  DISJOINT slots of one free K(Y,Q). VERDICT (b): a0 and the AeST CMB dust")
print(f"  are INDEPENDENT. The CMB fit does NOT give a0; it does not falsify it either")
print(f"  (a0 absent from linear theory). UNIFICATION HOLDS for dark-ENERGY only.")

print()
print("="*78)
print("(c) HOT-vs-COLD THIRD PEAK: FIELD (K(Q)) vs PARTICLE (11-eV sterile)")
print("="*78)
# The task's KEY TENSION lives in the PARTICLE route:
#   cluster fix (Angus 11-eV hot sterile) free-streams ~Mpc -> likely CANNOT make
#   the cold/clusterable 3rd peak. Quantify the particle free-streaming, then show
#   the FIELD route (K(Q)) sidesteps it (condensate, no thermal velocity).

# ---- Particle route: hot sterile free-streaming (Tremaine-Gunn / FS scale) ----
def free_stream_Mpc(m_eV):
    # thermal relic neutrino-like: comoving FS length ~ 20 (eV/m) Mpc  (standard estimate)
    return 20.0*(1.0/m_eV)
for m in [0.072, 2.0, 11.0, 390.0, 1000.0]:
    lam = free_stream_Mpc(m)
    note = ""
    if m==11.0:   note = "  <- Angus cluster sterile: HOT, FS~Mpc (washes small-scale power)"
    if m==390.0:  note = "  <- dSph TG floor (galaxy-safe needs >= this)"
    if m==1000.0: note = "  <- ~keV: FS<<Mpc, cluster+CMB-able, but is COLD DM (a particle)"
    print(f"   m={m:7.1f} eV : free-streaming ~ {lam:8.3f} Mpc{note}")
print("  => an 11-eV HOT sterile (cluster fix) free-streams ~2 Mpc -> suppresses the")
print("     sub-horizon clustering the 3rd peak needs (cold). PARTICLE tension is REAL:")
print("     the cluster-hot and CMB-cold demands pull the SAME particle's mass opposite")
print("     ways -> needs ~keV (cold, cluster+CMB) which is just CDM by another name,")
print("     OR TWO species. Either way 'no dark matter' is forfeited.")

# ---- Field route: K(Q) condensate sound speed / Jeans scale ----
# Shift-symmetric k-essence: rho ~ a^-3 (w=0 background) AND c_s^2 = (dp/drho)|_phi
# ~ 0 on sub-horizon scales (ghost-condensate / dust limit) -> NO free-streaming,
# NO thermal velocity. It clusters like cold dust at ALL k below the (tiny) scalar
# mass scale 1/mu >~ 1 Mpc. So the FIELD does the 3rd peak as COLD by construction.
inv_mu_Mpc = 1.0   # 1/mu >~ 1 Mpc (CMB-pinned, Verwayen+2024); Jeans ~ this
print(f"\n  FIELD K(Q): shift-symmetric k-essence, w=0, c_s^2 ~ 0 sub-horizon.")
print(f"     -> NO thermal free-streaming; Jeans/coherence scale ~ 1/mu >~ {inv_mu_Mpc:.0f} Mpc.")
print(f"     -> clusters as COLD dust for the 3rd peak (this is WHY AeST fits Planck).")
print(f"  => The FIELD route does NOT inherit the particle's hot/cold third-peak")
print(f"     tension. It pays a DIFFERENT price: the dust amplitude is the FREE I0.")

print()
print("="*78)
print("(c-cont) THE CASSINI/CMB CO-TEST THE V(Q) MOD LEAVES OPEN (banked risk)")
print("="*78)
# The V(Q) / mass-term modification lives in K(Q), which has NO Y^3/2 suppression.
# The Y^3/2 (a0) term is CMB-safe by a THEOREM (Y=0 on FRW; O(delta phi^3)) AND
# solar-system-safe (deep-MOND screening). The K(Q) mass term mu^2 is NOT Y^3/2-
# suppressed -> it is the SAME free mu pulled by galaxy-WL (m^2/f_G < 1 Mpc^-2,
# Mistele 2023) and clusters (>~1 Mpc^-2) in OPPOSITE directions, AND it can leak
# into the solar system (Cassini) since it does not vanish at high Y.
mu_inv_cmb     = 1.0    # Mpc, CMB-pinned upper coherence
galaxy_WL_max  = 1.0    # Mpc^-2  (Mistele: m^2/f_G < 1)
cluster_min    = 1.0    # Mpc^-2  (clusters want >= 1)
print(f"  Y^3/2 (a0) sector : CMB-safe (theorem, Y=0 FRW) AND Cassini-safe (screened).")
print(f"  K(Q) mass sector  : NO Y^3/2 suppression -> mu^2 is a FREE constant that")
print(f"     galaxy-weak-lensing wants  m^2/f_G < {galaxy_WL_max:.0f} Mpc^-2 (Mistele 2023)")
print(f"     clusters want              m^2/f_G >~ {cluster_min:.0f} Mpc^-2")
print(f"     -> the SAME mu pulled OPPOSITE ways (a squeeze), AND it is NOT Y-screened")
print(f"        so the Cassini/CMB co-test on V(Q) is GENUINELY OPEN (not closed here).")

print()
print("="*78)
print("BOTH-WAYS SUMMARY  (an Omega coincidence is NOT a unification)")
print("="*78)
print(f"  CREDIT:  AeST fits Planck incl. 3rd peak via an a^-3 K(Q) dust = real first.")
print(f"           a0 <-> Lambda(dark ENERGY) is a real z=0 unification (Omega_DE=0.685).")
print(f"           The FIELD route avoids the PARTICLE hot/cold third-peak tension.")
print(f"  KILL:    the dust amplitude Omega_dust~{Omega_dm:.2f} is the FREE I0, ORTHOGONAL")
print(f"           to a0=c^2 sqrt(Lambda/32pi). Omega_dust ~ {Omega_dm:.2f} ~ LCDM 0.26 is a")
print(f"           COINCIDENCE of TUNING, not a derivation. 'Two sectors one number'")
print(f"           HOLDS at z=0 (a0<->dark energy), FAILS at recombination (needs I0).")
print(f"  NET:     AeST RELOCATES the free function (particle DM -> field I0); it lets")
print(f"           the framework do the CMB WITHOUT a dark PARTICLE, but NOT without a")
print(f"           ~LCDM-amount of (cold, a^-3) dark DENSITY. 'No dark matter' is")
print(f"           forfeited as a DENSITY even when it is kept as a PARTICLE.")
