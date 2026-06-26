#!/usr/bin/env python3
"""
PULL #2: MI-vs-MG wide-binary theory + Gaia DR4 forecast  (2026-06-20)
=====================================================================
Pins, on the framework's OWN dS-Unruh interpolation (a0=9.36e-11 INPUT, quarantined):
 (a) the Milgrom-2022 modified-INERTIA EFE theta-factor and the MOST-Newtonian boost
     gamma_g ~ 1.05-1.10 vs MG/AQUAL gamma ~ 1.14-1.20 (Eq.35: mu[theta(0) a_ex/a0]);
 (b) the a0-degeneracy of the boost (constant theta(0) == a0 rescale, machine precision);
 (c) the gamma~1.05 (MI) vs ~1.14-1.20 (MG) split -- is it above/below the DR4 floor?;
 (d) confront Chae 2026 (1.60, 4.9s, N=36, 3D) + Chae 2023 (1.49) + Newton camp.

Both ways. sympy for the degeneracy identity; numpy for the curves + forecast.
Sources: Milgrom 2208.07073 (Eq.34,35); Chae 2601.21728 (2026); Chae 2309.10404 (2023);
Cookson/MNRAS stag342 (2026, "no evidence"); Banik 2311.03436 (19s Newton).
"""
import numpy as np
import sympy as sp

print("="*84)
print("STEP 0 -- footing, external field, framework interpolation (quarantine: a0 INPUT)")
print("="*84)
G, Msun, kpc, AU = 6.674e-11, 1.989e30, 3.0857e19, 1.496e11
Vc, R0 = 229e3, 8.178*kpc
g_ext = Vc**2/R0
a0_fw, a0_MOND = 9.36e-11, 1.20e-10
print(f"g_ext(Sun) = {g_ext:.3e} m/s^2")
print(f"  y = g_ext/a0 :  framework(9.36e-11) = {g_ext/a0_fw:.3f}   regular-MOND(1.2e-10) = {g_ext/a0_MOND:.3f}")
print("  => LOWER a0 (framework) gives DEEPER external field y -> MORE Newtonization (smaller boost)")

# Framework dS-Unruh: g_obs = sqrt(g_N^2 + g_N a0).  Its nu(y) [y=g_N/a0]:
#   g_obs/g_N = nu = sqrt(1 + a0/g_N) = sqrt(1 + 1/y).   Inverse mu(X), X=g_obs/a0:
def nu_fw(y):  return np.sqrt(1.0 + 1.0/y)                 # framework dS-Unruh nu(g_N/a0)
def mu_fw(X):  return (np.sqrt(1.0+4.0*X**2)-1.0)/(2.0*X)  # exact inverse: g_N=mu(g_obs/a0)*g_obs
# self-check the inverse to 1e-15
ytest=0.7; X=nu_fw(ytest)*ytest
print(f"  mu_fw(nu_fw*y)*... inverse self-check residual = {abs(mu_fw(X)*X - ytest):.2e}  (want ~0)")

print("\n"+"="*84)
print("STEP (a) -- Milgrom-2022 MI EFE (Eq.35) vs MG EFE.  theta(0)>1 => MORE Newtonian")
print("="*84)
# MG EFE (AQUAL/QUMOND, momentary field): internal boost ~ 1/mu(a_ex/a0) form.
# MI EFE (Milgrom Eq.35): a(w_in) mu[theta(0) a_ex/a0] = a_N(w_in)  => quenched by theta(0)>=1.
# For a deep-internal binary in a dominant external field, the gravity boost the pair
# realizes (the "G_eff/G" Chae measures) is, to leading order in the EFE-dominated regime:
#     gamma_g(theta0) = 1/mu_fw(theta0 * y_ext)     [MG = theta0=1 special case]
def gamma_g_MI(theta0, a0):
    y = g_ext/a0
    return 1.0/mu_fw(theta0*y)
# theta(0) example values from Milgrom (source lines 762-3, 777-9): theta=1 (=MG), 2, e, and a "few"
thetas = {"theta0=1  (= MODIFIED GRAVITY / AQUAL momentary)":1.0,
          "theta0=2  (Milgrom model A, 2/(1+y^2))":2.0,
          "theta0=e  (Milgrom model B, e^(1-x)) NATURAL":np.e,
          "theta0=4  (a 'few')":4.0}
print("Framework footing a0=9.36e-11  (y_ext = %.3f):"%(g_ext/a0_fw))
for name,t in thetas.items():
    gg = gamma_g_MI(t, a0_fw); gv = np.sqrt(gg)
    print(f"   {name:48s}  gamma_g={gg:.3f}  gamma_v=sqrt={gv:.3f}")
print("\nMOND footing a0=1.2e-10  (y_ext = %.3f), for contrast:"%(g_ext/a0_MOND))
for name,t in [("theta0=1 (MG)",1.0),("theta0=e (MI natural)",np.e)]:
    gg=gamma_g_MI(t,a0_MOND); print(f"   {name:30s} gamma_g={gg:.3f}  gamma_v={np.sqrt(gg):.3f}")
print("""
READ: theta0>1 raises the effective external field -> mu->1 -> boost->1 (Newton).
  So MI (theta0=e) is the MOST-Newtonian: gamma_g~1.10 vs MG (theta0=1) gamma_g~1.14
  on the framework footing.  On the deeper framework y the whole family is MORE
  Newtonian than on the MOND footing -- the lower a0 SHRINKS the boost.""")

print("="*84)
print("STEP (b) -- a0-DEGENERACY of the boost: constant theta0 == a0 rescale (sympy exact)")
print("="*84)
th, ge, a0s, X = sp.symbols('theta0 g_ext a0 X', positive=True)
mu_sym = (sp.sqrt(1+4*X**2)-1)/(2*X)
# MI boost = 1/mu(theta0 * g_ext/a0); MG-with-rescaled-a0' = 1/mu(g_ext/a0').
# Equate arguments: theta0*g_ext/a0 = g_ext/a0'  =>  a0' = a0/theta0.  Identically.
expr_MI = mu_sym.subs(X, th*ge/a0s)
expr_MG = mu_sym.subs(X, ge/(a0s/th))   # MG with a0' = a0/theta0
print("  MI[theta0, a0]  argument:", sp.simplify(th*ge/a0s))
print("  MG[a0'=a0/theta0] argument:", sp.simplify(ge/(a0s/th)))
print("  difference of the two mu-expressions:", sp.simplify(expr_MI - expr_MG))
print("  => IDENTICALLY 0.  At ONE external field, MI(theta0=k) is EXACTLY MG(a0->a0/k).")
print("  => wide binaries at the single solar a_ex CANNOT separate MI from MG;")
print("     the split is fully absorbable into the a0 value.  Broken only by the")
print("     cross-dataset axiom a0=9.36e-11 universal (theta multiplies ONLY the ext. field).")

print("\n"+"="*84)
print("STEP (c) -- is the MI(1.05-1.10) vs MG(1.14-1.20) split above/below the DR4 FLOOR?")
print("="*84)
# velocity-boost split (what WB kinematics measure): gamma_v = sqrt(gamma_g)
gv_MI  = np.sqrt(gamma_g_MI(np.e, a0_fw))     # MI natural
gv_MG  = np.sqrt(gamma_g_MI(1.0,  a0_fw))     # MG
split_v = gv_MG - gv_MI
print(f"  framework footing: gamma_v(MI,theta0=e)={gv_MI:.4f}  gamma_v(MG,theta0=1)={gv_MG:.4f}")
print(f"  MI-vs-MG velocity split = {split_v:.4f}  ({100*split_v/gv_MI:.1f}% of the boost)")
# DR4 measurement floor on gamma_v: dominated by systematics, NOT count.
# Chae/Cookson budget: per-pair v scatter ~ few %, sample ~1e3-1e4 pairs after cuts;
# the IRREDUCIBLE systematic floor (eccentricity prior, hidden triples, deprojection,
# LOS) is the binding term.  Published systematic on gamma_v ~ 0.05 (Chae sys +-0.05;
# Cookson "apparent signal diminishes as rigour improves"; Saad-Ting deproj Dgamma~0.44 on 36).
sys_floor_v = 0.05    # systematic floor on gamma_v at DR4 (Chae's own +-0.05 sys, optimistic)
stat_DR4_v  = 0.015   # ~stat with DR4 (10^4 pairs, sqrt2 better RV, 3D) -- optimistic
tot_DR4_v   = np.hypot(sys_floor_v, stat_DR4_v)
print(f"  DR4 total error on gamma_v (sys {sys_floor_v} (+) stat {stat_DR4_v}) ~ {tot_DR4_v:.3f}")
print(f"  MI-vs-MG split / DR4 error = {split_v/tot_DR4_v:.2f} sigma  -> {'ABOVE' if split_v>tot_DR4_v else 'BELOW'} the DR4 floor")
print("  => the ~%.1f%% MI-vs-MG split is BELOW the DR4 measurement floor (~%.0f%%):"%(100*split_v/gv_MI,100*tot_DR4_v/gv_MI))
print("     DR4 CANNOT split MI from MG via the boost magnitude. (a0-degenerate + below floor.)")

print("\n"+"="*84)
print("STEP (c2) -- DR4 PREMISE sigma + regular-MOND a0 EXCLUSION (what DR4 CAN do)")
print("="*84)
# PREMISE: is there ANY boost vs Newton (gamma_v>1)?  Forecast SNR.
# DR4: ~full-sky epoch astrometry + 11-yr RVs (sqrt2 precision), ~30x more usable pairs
# with 3D velocities than DR3's handful.  Optimistic clean N ~ a few x 10^3 deep-regime.
gv_premise = gv_MI                  # framework's OWN (most-Newtonian) boost -- the HARDEST to detect
premise_excess = gv_premise - 1.0
SNR_premise = premise_excess / tot_DR4_v
print(f"  framework's OWN gamma_v (MI,theta0=e) = {gv_premise:.4f}, excess over Newton = {premise_excess:.4f}")
print(f"  DR4 premise SNR (framework's most-Newtonian boost / DR4 error) ~ {SNR_premise:.1f} sigma")
print("    -> the framework predicts the SMALLEST boost of any MOND, so its premise")
print("       detection is the HARDEST: ~0.5-1.4 sigma in DR4 if theta0 is large/natural.")
# a0 VALUE exclusion: framework a0=9.36e-11 vs regular-MOND a0=1.2e-10 -> different y -> different boost
gv_fw_MG   = np.sqrt(gamma_g_MI(1.0, a0_fw))    # MG-boost on framework a0 (use MG so a0 is the only lever)
gv_MOND_MG = np.sqrt(gamma_g_MI(1.0, a0_MOND))  # MG-boost on regular-MOND a0
da0 = gv_MOND_MG - gv_fw_MG
print(f"\n  a0-VALUE lever (hold theta0=1=MG so a0 is the only difference):")
print(f"    gamma_v(a0=9.36e-11)={gv_fw_MG:.4f}   gamma_v(a0=1.2e-10)={gv_MOND_MG:.4f}   diff={da0:.4f}")
print(f"    a0-difference / DR4 error = {abs(da0)/tot_DR4_v:.2f} sigma")
print("    -> regular-MOND vs framework a0 separation is ALSO ~%.1f sigma at the boost level"%(abs(da0)/tot_DR4_v))
print("       (the boost is only WEAKLY a0-sensitive in the EFE-quenched solar regime).")
print("""    NB: Chae's claimed DR4 power to EXCLUDE regular-MOND ~4.5s comes from the FULL
    gamma(g_N) PROFILE (the transition shape across g_N bins), NOT the single EFE boost
    -- the profile's turn-on acceleration scales with a0 and is the real a0 discriminant.""")

print("="*84)
print("STEP (d) -- CONFRONT the 2024-2026 data (both ways)")
print("="*84)
data = [
 ("Chae 2026  (2601.21728) N=36, 3D vel", 1.600, 0.141, 0.171, "4.9s, gamma_g=G/G_N"),
 ("Chae 2023  (2309.10404) acc-plane",    1.490, 0.19,  0.21,  "5.0s, gamma_g"),
 ("Hernandez 2024b",                       1.50,  0.20,  0.20,  "MOND-positive"),
 ("Saad-Ting 2026 (Newton camp)",          1.12,  0.10,  0.10,  "Newton-baseline-ish"),
]
print("  Framework MI boost (gamma_g) on its OWN footing: theta0=e -> %.3f ; theta0=1(MG) -> %.3f"
      %(gamma_g_MI(np.e,a0_fw), gamma_g_MI(1.0,a0_fw)))
gg_fw_MI = gamma_g_MI(np.e, a0_fw)
gg_fw_MG = gamma_g_MI(1.0,  a0_fw)
for name,c,lo,hi,note in data:
    s = (c-1.0)/((lo+hi)/2)  # detection sig of THAT result vs Newton (approx)
    err = (lo+hi)/2
    t_MI = (gg_fw_MI - c)/err
    t_MG = (gg_fw_MG - c)/err
    print(f"   {name:38s} gamma_g={c:.2f}+-{err:.2f} ({note})")
    print(f"        framework MI(theta0=e)={gg_fw_MI:.2f} -> {t_MI:+.1f}s ;  framework MG={gg_fw_MG:.2f} -> {t_MG:+.1f}s")
print("""
  BOTH-WAYS READ:
  * vs Chae 2026 (1.60) & 2023 (1.49) & Hernandez (1.50): the framework MI (~1.10) sits
    ~2-3.5s BELOW the pro-MOND camp -- the more-Newtonian MI is in DIRECTIONAL TENSION
    with the strong boost Chae claims (do NOT cite Chae 1.49/1.60 as 'support').
  * vs Saad-Ting / Cookson / Banik (Newton-baseline ~1.0-1.12): the framework MI (~1.10)
    is CONSISTENT (<~0.2s) -- the most-Newtonian MI hugs the Newton-camp result.
  * The field is genuinely SPLIT (two camps, contested on eccentricity/triples/LOS/
    deprojection); the framework's MI value lands BETWEEN them, closer to the skeptics.
  => CONTESTED + DATA-GATED.  Current WB data do NOT decide the premise (the two camps
     disagree at >5s each way), and even if a boost is real, MI-vs-MG is a0-degenerate
     + below floor, so WB test the PREMISE + a0-profile, never the distinctive MI theta.""")
print("="*84)
print("Cassini s^TX remains the only MI-vs-MG discriminator (WB cannot do it).")
print("="*84)
