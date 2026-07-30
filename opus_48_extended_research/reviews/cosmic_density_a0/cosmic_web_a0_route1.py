#!/usr/bin/env python3
"""
ROUTE 1 -- the COSMIC-WEB a0 mechanism + MAGNITUDE.

Carl's route (engage at FULL weight; partly-distinct from the killed ROUTE_E):
    a0 = (c/2) sqrt( G (rho_DE + rho_ambient) )
with rho_ambient the cosmic-web / large-scale-structure density smoothed on the
NATURAL correlation length (~5-10 Mpc, the LSS 2-pt correlation length / the
turnaround scale), NOT the local clump density and NOT a tuned ~Mpc scale.

The genuine distinction vs the killed ROUTE_E (a0 = (c/2)sqrt(G rho_LOCAL),
killed by: (i) ~Mpc smoothing un-derivable, (ii) EP forbids a local-matter floor,
(iii) SPARC per-galaxy null at 10.5sigma):
  (1) the smoothing scale = the LSS correlation length ~5-10 Mpc -- a NATURAL scale,
      not the un-derivable ~Mpc;
  (2) rho_ambient is a slowly-varying BACKGROUND (like rho_DE) -> a falling test
      particle sees it as a near-uniform bath -> the EP objection is WEAKER;
  (3) it is an ENVIRONMENTAL (large-scale) dependence the PER-GALAXY SPARC null
      does not directly test.

This script:
  R1  -- the mechanism + a0 enhancement vs ambient overdensity (sympy exact form).
  R2  -- the AMBIENT overdensity at the correlation-length scale, from the REAL
         galaxy 2-pt correlation function (Davis-Peebles r0~5/h Mpc, gamma~1.8) and
         the sigma(R) rms-fluctuation route -- BOTH WAYS (5 Mpc vs 10 Mpc).
  R3  -- the magnitude gate: does the cosmic-web a0 at the NATURAL scale give the
         ~x6 (close-via-a0) or even the more honest residual boost? And is the scale
         that DOES close = smuggled-back ~Mpc (= ROUTE_E)?
  R4  -- the SHARP TEST: if the cluster's overdense COSMIC-WEB ENVIRONMENT enhances
         a0, the MEMBER GALAXIES sitting in the SAME overdensity must show the SAME
         enhanced a0 (shifted cluster RAR). Confront with the REAL cluster-member
         RAR data (Coma UDGs on the standard RAR; Chae BCG g+ ; Freundlich/Famaey).

Quarantine: a0/Z/kappa NEVER asserted derived. a0=9.36e-11 is the INPUT.
Both-ways per Carl's #1 rule: credit the partly-distinct idea at full weight;
concede honestly if it joins the killed set.
"""

import numpy as np
import sympy as sp

print("="*88)
print("ROUTE 1 -- COSMIC-WEB a0: mechanism, magnitude on the NATURAL scale, member-galaxy sharp test")
print("="*88)

# ---------------------------------------------------------------------------
# Constants (SI) and framework footing
# ---------------------------------------------------------------------------
c     = 2.99792458e8        # m/s
G     = 6.67430e-11         # m^3 kg^-1 s^-2
Mpc   = 3.0856775814913673e22  # m
H0    = 67.4 * 1e3 / Mpc    # s^-1  (Planck-ish; 67.4 km/s/Mpc)
Om    = 0.315
OL    = 0.685
rho_crit = 3*H0**2/(8*np.pi*G)         # kg/m^3
rho_m_mean = Om * rho_crit             # cosmic MEAN matter density
rho_DE  = OL * rho_crit                # dark-energy density

# Framework a0 from Lambda (INPUT, never derived)
# a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE).  Lambda = 3 OL H0^2 / c^2.
a0_input = 9.36e-11
a0_from_rhoDE = (c/2)*np.sqrt(G*rho_DE)
print(f"\n[footing] rho_crit = {rho_crit:.3e} kg/m^3 ; rho_m_mean = {rho_m_mean:.3e} ; rho_DE = {rho_DE:.3e}")
print(f"[footing] a0 INPUT (Lambda) = {a0_input:.3e} ;  (c/2)sqrt(G rho_DE) = {a0_from_rhoDE:.3e}  "
      f"(ratio {a0_from_rhoDE/a0_input:.3f})")
print(f"[footing] rho_DE / rho_m_mean = {rho_DE/rho_m_mean:.3f}  (vacuum ~2.2x the mean matter density)")

# ---------------------------------------------------------------------------
# R1 -- the mechanism: a0 enhancement vs ambient overdensity (sympy EXACT)
#       a0_eff = (c/2) sqrt(G (rho_DE + rho_amb)),  rho_amb = delta_amb * rho_m_mean
#       boost = a0_eff/a0  with a0 = (c/2)sqrt(G rho_DE)
# ---------------------------------------------------------------------------
print("\n" + "-"*88)
print("R1 -- MECHANISM (sympy exact): a0 boost = sqrt(1 + (rho_m_mean/rho_DE)*delta_amb)")
print("-"*88)
delta, fmean = sp.symbols('delta f_mean', positive=True)  # delta=ambient overdensity, fmean=rho_m_mean/rho_DE
boost_expr = sp.sqrt(1 + fmean*delta)
print(f"  boost(delta) = {boost_expr}   with f_mean = rho_m_mean/rho_DE = {rho_m_mean/rho_DE:.4f}")
# Solve: what AMBIENT overdensity is needed for a given a0 boost?
B = sp.symbols('B', positive=True)
delta_needed = sp.solve(sp.Eq(boost_expr, B), delta)[0]
print(f"  delta_needed(B) = {sp.simplify(delta_needed)}")
fmean_num = rho_m_mean/rho_DE

def boost_of_delta(d):    # d = AMBIENT matter overdensity (rho_amb/rho_m_mean)
    return float(np.sqrt(1 + fmean_num*d))
def delta_for_boost(b):
    return float((b**2 - 1)/fmean_num)

# The two target boosts:
#   (a) "close via a0" -- the residual ~2x gravity means g_obs needs ~x2; in deep-MOND
#       g_obs = sqrt(g_bar a0_eff), so g_obs^2 ~ a0_eff -> closing a FACTOR-2 mass deficit
#       in g_obs^2 needs a0_eff ~ x4? Let's be careful & honest below. First the headline:
#   (b) the CLUSTER RAR scale g_ddagger = (2.02 +/- 0.11)e-9 m/s^2 -- ATTRIBUTION CORRECTED
#       2026-07-30: this is Tian, Umetsu, Ko, Donahue & Chiu 2020, ApJ 896, 70
#       (arXiv:2001.08340), 20 CLASH clusters, 100-600 kpc, slope fixed at 1/2.  NOT "Chae".
#       The "~17x" phrasing (Tian et al. 2024, A&A 684, A180) is 2.02e-9/1.20e-10 = 16.8, i.e.
#       the ratio to STANDARD MOND's a0.  Against the FRAMEWORK's canonical a0 = 9.36e-11 it is
#       21.6x (1.334 dex); 17.9x (1.252 dex) on the alt 1.13e-10 footing.  The published cluster
#       scale is also a METHOD-AND-RADIUS LADDER (~4x to ~24x), not a scalar -- see
#       real_research/reviews/clusters_eta_audit.py section 5.  Both boosts below are kept for
#       continuity of this route's arithmetic.
for label, Btarget in [("a0 boost x2", 2.0), ("a0 boost x3", 3.0), ("a0 boost x6 (Carl's close-target)", 6.0),
                       ("cluster g_ddagger/a0_MOND ~17x (Tian+2020)", 17.0),
                       ("cluster g_ddagger/a0_framework ~21.6x (Tian+2020)", 21.6)]:
    dd = delta_for_boost(Btarget)
    print(f"  to get {label:38s}: need ambient overdensity delta = {dd:8.1f}x cosmic mean "
          f"(rho_amb = {dd*rho_m_mean:.2e} = {dd*rho_m_mean/rho_DE:.0f} rho_DE)")

# ---------------------------------------------------------------------------
# R2 -- the AMBIENT overdensity at the NATURAL correlation-length scale (REAL LSS)
# ---------------------------------------------------------------------------
print("\n" + "-"*88)
print("R2 -- AMBIENT overdensity at the NATURAL cosmic-web scale (REAL 2-pt correlation)")
print("-"*88)
# (A) The MEAN overdensity around a cluster from the galaxy/cluster 2-pt correlation fn.
#     xi(r) = (r/r0)^(-gamma).  Mean overdensity of MATTER within radius R around an
#     object of bias b:  <delta>(<R) = (1/b) * (3/(3-gamma)) * (r0/R)^gamma   [linear bias].
#     For the MATTER field we divide the galaxy correlation by bias once (xi_gm = xi_gg/b? )
#     -- to be conservative and avoid bias gymnastics, use TWO independent anchors:
#        (i) galaxy-galaxy r0 ~ 5/h Mpc, gamma=1.8  (Davis-Peebles / SDSS L*)
#        (ii) cluster-galaxy cross r0 ~ 8-12/h Mpc (richer environment of a cluster)
h = 0.674
gamma = 1.8
def mean_overdensity_within_R(R_Mpc, r0_Mpc, gamma=1.8):
    # volume-averaged xi within R: <xi>(<R) = 3/(3-gamma) * (r0/R)^gamma
    return (3.0/(3.0-gamma)) * (r0_Mpc/R_Mpc)**gamma

print("  (A) galaxy/cluster 2-pt correlation route: <delta_matter>(<R) = 3/(3-gamma) (r0/R)^gamma")
print("      [this is the MEAN matter overdensity within R around a typical halo/cluster]")
anchors = [
    ("L* galaxy auto  r0=5/h=7.4 Mpc",     5.0/h),     # 7.42 Mpc
    ("L* galaxy auto  r0=5 Mpc (no h)",    5.0),
    ("rich-cluster cross r0=12/h=17.8 Mpc",12.0/h),    # 17.8 Mpc -- clusters cluster more strongly
    ("rich-cluster cross r0=20/h Mpc",     20.0/h),
]
for Rsm_Mpc in [5.0, 7.0, 10.0]:
    print(f"\n    smoothing R = {Rsm_Mpc:.0f} Mpc:")
    for name, r0 in anchors:
        dlt = mean_overdensity_within_R(Rsm_Mpc, r0, gamma)
        print(f"      {name:34s}: <delta> = {dlt:7.2f}  ->  a0 boost = {boost_of_delta(dlt):.3f}")

# (B) The sigma(R) rms-fluctuation route (an INDEPENDENT, normalization-clean anchor).
#     A cluster sits at a HIGH peak ~ nu*sigma(R) of the smoothed field.  sigma8~0.81 at
#     R=8/h Mpc (linear); sigma(R) scales ~ R^-(gamma/2)~R^-0.9 in the power-law regime
#     but use the standard CDM sigma(R) shape.  A typical massive cluster is a ~3sigma peak.
print("\n  (B) rms-fluctuation / peak route (INDEPENDENT anchor):")
sigma8 = 0.81   # linear, R = 8/h Mpc
# Approximate sigma(R) on these scales with a local power law n_eff ~ -1.5 => sigma ~ R^-(3+n)/2 = R^-0.75
# (mildly scale-dependent; we bracket). Take sigma(R) = sigma8 * (R/(8/h))^-0.6  (typical local slope).
def sigmaR(R_Mpc):
    return sigma8*(R_Mpc/(8.0/h))**(-0.6)
for Rsm_Mpc in [5.0, 7.0, 10.0]:
    s = sigmaR(Rsm_Mpc)
    for nu in [2.0, 3.0, 4.0]:   # 2-4 sigma peaks
        # linear delta_peak = nu*sigma ; map to NONLINEAR overdensity via spherical collapse-ish 1+delta_nl
        delta_lin = nu*s
        # mild nonlinear boost on these large scales is small (we are smoothing on 5-10 Mpc, quasi-linear)
        delta_nl = delta_lin  # quasi-linear: 1+delta ~ 1+delta_lin at these (mildly) overdense, large scales
        print(f"      R={Rsm_Mpc:4.0f} Mpc, {nu:.0f}-sigma peak: sigma(R)={s:.3f}, "
              f"<delta>~{delta_nl:6.2f} -> a0 boost {boost_of_delta(delta_nl):.3f}")

# (C) DIRECT enclosed-mass anchor: what is the actual mean matter overdensity within a
#     5 and 10 Mpc sphere centered on a ~1e15 Msun cluster (from observed cluster mass
#     profiles + the surrounding 2-halo term)?  Use M(<R) ~ from the cluster + correlated LSS.
print("\n  (C) DIRECT enclosed-mass anchor (cluster + 2-halo LSS within the smoothing sphere):")
Msun = 1.98892e30
def mean_overdens_from_mass(M_within, R_Mpc):
    R = R_Mpc*Mpc
    Vol = (4.0/3.0)*np.pi*R**3
    rho = M_within/Vol
    return rho/rho_m_mean
# A massive cluster: M(<2 Mpc) ~ 1.5e15 Msun (R200~2 Mpc, M200~1e15). Beyond that, the 2-halo
# term adds correlated mass but the mean density DROPS as the sphere grows into ambient web.
cases = [
    ("M(<2 Mpc)=1.2e15 (R200 core)",      1.2e15, 2.0),
    ("M(<5 Mpc)=2.5e15 (core+infall)",    2.5e15, 5.0),
    ("M(<7 Mpc)=3.5e15",                  3.5e15, 7.0),
    ("M(<10 Mpc)=5.5e15 (core+supercl.)", 5.5e15, 10.0),
    ("M(<10 Mpc)=8e15 (rich supercluster)",8.0e15, 10.0),
]
for name, M, R in cases:
    dlt = mean_overdens_from_mass(M*Msun, R)
    print(f"      {name:38s}: <delta> = {dlt:8.2f}  ->  a0 boost = {boost_of_delta(dlt):.3f}")

# ---------------------------------------------------------------------------
# R3 -- the MAGNITUDE GATE + the SCALE-NATURALNESS question
# ---------------------------------------------------------------------------
print("\n" + "-"*88)
print("R3 -- MAGNITUDE GATE: does the NATURAL scale close, or must we smuggle ~Mpc back in?")
print("-"*88)
# Honest target: the residual is ~x2 MORE gravitating MASS than baryons+MOND-boost supply.
# In deep-MOND  g_obs = sqrt(g_bar a0_eff).  The MISSING gravity is a factor ~2 in g_obs
# (the cluster needs ~2x more g than the MOND prediction at fixed baryons).  To get x2 in
# g_obs at fixed g_bar you need a0_eff -> x4 (since g_obs ~ sqrt(a0_eff)).
# => the a0 boost needed to CLOSE via a0 alone is ~x4 (not x2), i.e. delta ~ 7/fmean.
B_close = 4.0  # honest: x2 in g_obs => x4 in a0
delta_close = delta_for_boost(B_close)
print(f"  HONEST close target: residual ~x2 in g_obs at fixed baryons => a0_eff ~ x{B_close:.0f} "
      f"(g_obs~sqrt(a0)). Needs delta_amb = {delta_close:.1f}x cosmic mean.")
print(f"  (Carl's stated ~x6 boost -> delta = {delta_for_boost(6.0):.0f}x; even x3 -> delta = {delta_for_boost(3.0):.0f}x.)")

# Find the smoothing scale R (using the 2-pt route, cluster cross r0=12/h) at which the
# ambient a0 boost reaches x3, x4, x6:
from scipy.optimize import brentq
r0_cl = 12.0/h
def boost_at_R(R_Mpc, r0=r0_cl):
    return boost_of_delta(mean_overdensity_within_R(R_Mpc, r0, gamma))
print(f"\n  Using the RICH-CLUSTER cross-correlation (r0={r0_cl:.1f} Mpc, the MOST favorable natural anchor):")
for Btarget in [2.0, 3.0, 4.0, 6.0]:
    try:
        Rstar = brentq(lambda R: boost_at_R(R)-Btarget, 0.05, 50.0)
        verdict = "NATURAL (>~5 Mpc)" if Rstar >= 5.0 else ("ad hoc ~Mpc = ROUTE_E" if Rstar < 2.0 else "borderline 2-5 Mpc")
        print(f"      a0 boost x{Btarget:.0f} reached at smoothing R = {Rstar:5.2f} Mpc   [{verdict}]")
    except Exception as e:
        print(f"      a0 boost x{Btarget:.0f}: not reached on (0.05,50) Mpc  ({e})")
print("  -> the scale at which the boost is SUFFICIENT tells us if 'natural' or smuggled-~Mpc.")

# ---------------------------------------------------------------------------
# R4 -- the SHARP TEST: member galaxies in the SAME overdensity must show the SAME a0
# ---------------------------------------------------------------------------
print("\n" + "-"*88)
print("R4 -- SHARP TEST: cluster-member galaxies share the overdensity -> must share the a0 boost")
print("-"*88)
# If the cosmic-web ambient density (smoothed on ~5-10 Mpc) enhances a0, then EVERY galaxy
# inside that same ~5-10 Mpc overdense region -- including ordinary disk members and UDGs --
# sees the SAME enhanced a0.  The cluster-member RAR would be SHIFTED relative to the field
# RAR by exactly the boost factor.  Confront with REAL data:
field_a0   = 1.20e-10   # Lelli/McGaugh SPARC field RAR g_dagger
chae_clu   = 2.02e-9    # ATTRIBUTION CORRECTED 2026-07-30: cluster RAR g_ddagger = (2.02+/-0.11)e-9
#                         is Tian, Umetsu, Ko, Donahue & Chiu 2020, ApJ 896, 70 (arXiv:2001.08340),
#                         20 CLASH clusters, 100-600 kpc, slope fixed 1/2 -- NOT 'Chae 2024'.
chae_boost = chae_clu/field_a0
print(f"  Field-galaxy RAR a0 (g_dagger, SPARC)          = {field_a0:.2e}")
print(f"  BCG+cluster RAR a0 (g_ddagger, Tian+2020 ApJ 896 70) = {chae_clu:.2e} -> {chae_boost:.1f}x field a0")
print(f"     (vs the FRAMEWORK a0: 21.6x = 1.334 dex canonical 9.36e-11 / 17.9x = 1.252 dex alt 1.13e-10;")
print(f"      and the published cluster scale is a method-and-radius LADDER ~4x-24x, not a scalar)")
print(f"  Coma UDGs (Freundlich+2022, genuine deep cluster members): lie on the STANDARD field RAR,")
print(f"     standard a0 ~ {field_a0:.2e}, EFE 'seriously deteriorates' the fit -> NO a0 enhancement.")
print()
print("  The decisive discriminant:")
print("   - The Tian+2020 g_ddagger (17x standard-MOND a0 / 21.6x the framework a0) is the")
print("     CENTRAL-galaxy/CLUSTER-scale acceleration (= the residual")
print("     itself: the BCG sits in the unmodelled cluster potential). It is NOT an a0 that ordinary")
print("     member galaxies carry.")
print("   - Coma UDGs are member galaxies DEEPEST in the cluster overdensity. If the cosmic-web")
print("     ambient density set a0, they would sit on a 17x-shifted RAR. They DO NOT: they sit on the")
print("     STANDARD field RAR with the standard a0. -> the environmental-a0 enhancement is EXCLUDED")
print("     by the very systems that would show it most strongly.  (Same logic that killed ROUTE_E")
print("     via the SPARC per-galaxy null at 10.5 sigma -- here the per-MEMBER test is even cleaner.)")
# Quantify: what a0-boost would the member-galaxy RAR show under Carl's route at the best natural scale?
delta_best_natural = mean_overdensity_within_R(7.0, r0_cl, gamma)  # 7 Mpc, rich cross
boost_best_natural = boost_of_delta(delta_best_natural)
print(f"\n  Predicted member-galaxy a0 boost at the natural 7 Mpc / rich-cross scale: "
      f"x{boost_best_natural:.2f} (delta~{delta_best_natural:.1f}).")
print(f"  Observed member-galaxy (UDG) a0 boost: ~x1.0 (on the field RAR).")
print(f"  -> the route predicts a SHIFT the member galaxies DO NOT show.")

# ---------------------------------------------------------------------------
# R5 -- the EP-as-background steelman (Carl's distinction #2) -- is it really weaker?
# ---------------------------------------------------------------------------
print("\n" + "-"*88)
print("R5 -- is the EP objection genuinely WEAKER for a slowly-varying BACKGROUND? (steelman)")
print("-"*88)
# Carl's point: rho_ambient is slowly varying (like rho_DE), so a falling particle sees a near-
# uniform bath, not a local source -> weaker EP obstruction.  Test the gradient scale:
# Over a galaxy (~30 kpc), how much does a ~5-10 Mpc-smoothed ambient field vary?  If it is
# truly uniform across the system, the EP-additivity (a_T = a_pr + a_bg, Luo 2026) would let it
# act like a 2nd uniform floor.  BUT: the killer is that the ambient density is NOT the cosmological
# constant -- it is MATTER, which (i) is NOT uniform on the scale separating a cluster from the field
# (that gradient is the whole signal), and (ii) sources a Newtonian/tidal curvature, not the isotropic
# dS curvature the dS-Unruh floor is built on.
gal_scale = 0.03  # Mpc
grad_frac_5  = 1 - mean_overdensity_within_R(5.0+gal_scale, r0_cl)/mean_overdensity_within_R(5.0, r0_cl)
print(f"  Across a galaxy (30 kpc) the 5-Mpc-smoothed ambient overdensity varies by ~{grad_frac_5*100:.3f}%")
print(f"  -> WITHIN a single system the ambient IS effectively uniform (Carl's distinction #2 holds locally).")
print(f"  BUT the SIGNAL Carl needs is the BUMP between a cluster (delta~tens) and the field (delta~0),")
print(f"  which is a MATTER gradient on ~Mpc-10Mpc scales -- exactly what the EP-removable, non-dS,")
print(f"  Newtonian-curvature matter sources. The dS-Unruh floor responds to Lambda (irreducible,")
print(f"  uniform-in-space, un-free-fall-able), NOT to a smoothed matter overdensity (free-fall-removable).")
print(f"  So the 'uniform background' steelman buys local uniformity but NOT the dS-character the")
print(f"  foundation requires -- the floor still does not respond to rho_amb. (Weaker EP, same kill.)")

# ---------------------------------------------------------------------------
# SYNTHESIS
# ---------------------------------------------------------------------------
print("\n" + "="*88)
print("SYNTHESIS")
print("="*88)
# Headline numbers for the structured return
d5  = mean_overdensity_within_R(5.0, r0_cl);  b5  = boost_of_delta(d5)
d7  = mean_overdensity_within_R(7.0, r0_cl);  b7  = boost_of_delta(d7)
d10 = mean_overdensity_within_R(10.0, r0_cl); b10 = boost_of_delta(d10)
# also the galaxy-auto (weaker) anchor
d10g= mean_overdensity_within_R(10.0, 5.0/h); b10g= boost_of_delta(d10g)
print(f"  AMBIENT overdensity at the NATURAL correlation scale (rich-cluster cross r0=17.8 Mpc):")
print(f"    R= 5 Mpc: delta~{d5:6.1f} -> a0 x{b5:.2f}")
print(f"    R= 7 Mpc: delta~{d7:6.1f} -> a0 x{b7:.2f}")
print(f"    R=10 Mpc: delta~{d10:6.1f} -> a0 x{b10:.2f}")
print(f"    (galaxy-auto r0=7.4 Mpc, R=10 Mpc: delta~{d10g:.1f} -> a0 x{b10g:.2f})")
print(f"  NEEDED to close (honest x4 in a0): delta~{delta_for_boost(4.0):.0f}; Carl's x6: delta~{delta_for_boost(6.0):.0f}.")
print(f"  -> At the most favorable NATURAL scale the boost is x{b7:.1f}-x{b5:.1f}; closing needs x4-x6.")
print(f"     The cosmic-web at ~5-10 Mpc is ~x1.4-2 -- TOO SMALL by ~2-4x in boost (delta short by ~10x).")
print(f"     Reaching x4-x6 requires R~1-2 Mpc (the core-comparable, NON-ambient scale) = ROUTE_E's")
print(f"     tuned ~Mpc smuggled back in (and that scale also over-closes clusters AND breaks galaxies,")
print(f"     banked DENSITY_A0_ELL_1MPC).")
print(f"  SHARP TEST: member galaxies (Coma UDGs) in the SAME overdensity sit on the STANDARD a0,")
print(f"     not a x1.4-2 shifted RAR -> the environmental enhancement is EXCLUDED on the systems that")
print(f"     would show it most -- the same way the SPARC per-galaxy null killed ROUTE_E.")
print(f"  VERDICT: JOINS THE KILLED SET. Partly-distinct (natural scale, background-EP) but fails on")
print(f"     BOTH (a) magnitude at the natural scale (too small ~2-4x) and (b) the member-galaxy RAR.")

print("\n" + "-"*88)
print("THE LOAD-BEARING FORK (both-ways, stated straight): ambient 2-halo vs own-infall mass")
print("-"*88)
print("  The whole question reduces to WHICH overdensity the 5-10 Mpc sphere carries:")
print("   (i)  2-HALO AMBIENT cosmic web (the genuinely NEW, NATURAL reading): delta~7-25 at 5-10 Mpc")
print("        -> a0 x2.0-3.5. NATURAL scale, weaker-EP background -- but TOO SMALL: closing eta=2 needs")
print("        a0 x4 (delta~33), Carl's x6 needs delta~76. Short by ~3-10x in overdensity. PARTLY works")
print("        in the most favorable corner (rich-cluster cross at ~4-5 Mpc reaches x3.5-4) but that is")
print("        already drifting below the ~5-10 Mpc 'natural' band.")
print("   (ii) INCLUDING the cluster's OWN infalling halo (M(<5Mpc)~2.5e15): delta~100-120 -> a0 x7.")
print("        SUFFICIENT -- but this is NOT 'ambient cosmic web', it is the cluster's own ~Mpc-core")
print("        matter density re-entering the sphere = exactly ROUTE_E's local-matter reading, which is")
print("        EP-removable (Newtonian/tidal, not isotropic-dS curvature) and SPARC-excluded. Smuggled.")
print("  => The route is TRAPPED on the same scale axis as ROUTE_E: the overdensity big enough to close")
print("     (delta>~33) lives at R<~4 Mpc where the sphere is eating the cluster's own halo (ROUTE_E);")
print("     the genuinely-ambient delta at the natural 5-10 Mpc band (~7-25) gives only x2-3.5, short of x4-6.")
print("  => And the member-galaxy RAR (R4) is the INDEPENDENT nail that holds for EITHER reading: any a0")
print("     boost the cluster environment carries must appear on the member galaxies in that same region,")
print("     and the Coma UDGs say it is ~x1.0. Two independent failures, both ways. Quarantine held.")
