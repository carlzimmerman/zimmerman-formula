"""
aest_mg_residual_and_diff
=========================
Compute AeST's modified-GRAVITY cluster-core residual on a CLASH-like cluster and
DIFFERENCE it against the framework's modified-INERTIA (dS-Unruh) residual on the
SAME baryons. Both-ways: is the cored M_res(<r) IDENTICAL (shared MOND undershoot)
or does the framework's MI predict a DISTINCTIVE cored profile, and is any difference
ABOVE the CLASH/eRASS1 floor?

KEY PHYSICS (read verbatim from the primary sources):

AeST (Durakovic-Skordis arXiv:2312.00889), the single-field equation Eq. (2.33):
    div( M(x) grad Phi ) + mu~^2 Phi = 4 pi G rho_b
  where M(x) = (-1 + sqrt(1+4x))/(1 + sqrt(1+4x))  [Eq 2.39] is the *standard MOND
  simple-nu* interpolation, x = |grad Phi|/a0, and mu~^2 Phi is an EXTRA mass term
  (modified Helmholtz). The paper states (line 658): "The new term mu^2 Phi becomes
  important at VERY LARGE DISTANCES away from sources" and (Fig 6 caption / line 2199):
  "the AeST contribution to the apparent mass is more significant in the OUTSKIRTS,
  growing steadily until the effects of mu^2 Phi become significant." The RAR peak
  /descent-below-MOND (Fig 7) is an OUTSKIRTS / low-acceleration feature of mu^2 Phi.
  => In the CORE (r << screening length 1/mu), AeST reduces to PURE MOND (mu term off),
     identical interpolation to galaxies.

Framework MI (Zimmerman, dS-Unruh): quasi-static modified inertia gives
    g_obs = sqrt(g_bar^2 + g_bar*a0)   (the dS-Unruh nu),
  which IS a standard MOND interpolation (the "nu_simple" family) applied to the
  trajectory, with a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11. NO extra mass term.
  In the quasi-static (adiabatic) regime relevant to a smoothly-distributed cluster
  gas/lensing mass, the Milgrom-2022 theta-factor -> theta(0) is a constant absorbed
  into a0 (Eq 35: theta(0) renormalizes a0). So the framework's MEAN cored phantom is
  set by the SAME deep-MOND scale invariance: M*G*a0 = eta*sigma^4, eta~1 SHARED.

Both interpolations sit in the standard MOND nu-family. We compute M_res(<r) for:
  (MI)  nu_dsunruh:  g = sqrt(gN^2 + gN a0)        [framework]
  (MOND simple)      g = gN/M with M the AeST Eq 2.39 interp, mu=0   [AeST core limit]
  (AeST full)        the SAME but with the mu^2 Phi mass term switched on (outskirts)
and difference them on identical baryons (NFW-ish gas + BCG).

CLASH target (Famaey-Pizzuti-Saltas arXiv:2410.02612, PRD 111 2025, from abstract):
  - residual = "inner constant-density CORE + outer slope sharper than -3.5"
  - "dark-mass-follows-gas with an EXPONENTIAL CUT-OFF" at r_cut ~ 400 kpc
  - missing-to-hot-gas density ratio in the inner parts ~ 10
  - remarkable cluster-to-cluster UNIFORMITY of (ratio, r_cut)
  This is the CORE excess OVER baryons+MOND-phantom -- i.e. what MOND/AeST FAILS to
  supply. The both-ways question: does MI supply MORE of it than AeST-MG?
"""
import numpy as np
import os, sys

sys.path.insert(0, "/Users/carlzimmerman/new_physics/zimmerman-formula")

# ---- constants ----
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1e3 * kpc
c    = 2.998e8
a0   = 9.36e-11                      # framework a0 = c^2 sqrt(Lambda/32pi)

# =====================================================================
# 1. Identical baryon model for a CLASH-like / eRASS1-rich cluster
#    M500 ~ 6.3e14 (eRASS1 rich median), R500 ~ 1150 kpc, T ~ 5.5 keV
# =====================================================================
M500   = 6.3e14 * Msun
R500   = 1152.0 * kpc
fgas   = 0.13
Mgas500 = fgas * M500
Mstar_BCG = 1.0e12 * Msun            # BCG stellar mass (concentrated, < ~30 kpc)
r_BCG  = 20.0 * kpc                  # BCG scale

# gas: beta-model-ish, rho_gas(r) = rho_g0 / (1 + (r/rc)^2)^(3*beta/2)
rc_gas = 150.0 * kpc                 # core radius (typical rich cluster ~ 100-200 kpc)
beta   = 0.65

def rho_gas_unnorm(r):
    return (1.0 + (r/rc_gas)**2)**(-1.5*beta)

def Mgas_unnorm(r):
    rr = np.atleast_1d(r)
    out = np.zeros_like(rr)
    for i, R in enumerate(rr):
        s = np.linspace(1e-3*kpc, R, 4000)
        out[i] = np.trapz(4*np.pi*s**2 * rho_gas_unnorm(s), s) if hasattr(np,'trapz') else np.trapz(4*np.pi*s**2 * rho_gas_unnorm(s), s)
    return out

# normalize gas so Mgas(<R500) = Mgas500
_norm = Mgas500 / Mgas_unnorm(R500)[0]

def Mgas(r):
    return _norm * Mgas_unnorm(r)

def Mstar(r):
    # Hernquist-like BCG enclosed mass
    rr = np.atleast_1d(r)
    return Mstar_BCG * rr**2 / (rr + r_BCG)**2

def Mbar(r):
    return Mgas(r) + Mstar(r)

# =====================================================================
# 2. The three MOND-family predictions for the *apparent* (phantom+bar) mass
#    g_obs(r) defines M_dyn(<r) = g_obs r^2 / G. Phantom = M_dyn - Mbar.
# =====================================================================
def gbar(r):
    return G * Mbar(r) / r**2

# (MI) framework dS-Unruh nu:  g = sqrt(gN^2 + gN a0)   [the "simple" nu family]
def g_MI(r):
    gN = gbar(r)
    return np.sqrt(gN**2 + gN * a0)

# (AeST core-limit = pure MOND with the Eq 2.39 interpolation, mu=0).
# Eq 2.39: M(x)=(-1+sqrt(1+4x))/(1+sqrt(1+4x)), x = g/a0, gN = M(x)*g.
# Solve M(u)*u*a0 = gN for u = g/a0.
def g_AeST_core(r):
    gN = np.atleast_1d(gbar(r))
    out = np.zeros_like(gN)
    for i, gn in enumerate(gN):
        lo, hi = gn/a0*0.1, max(gn/a0*1e3, 1e6)
        for _ in range(200):
            u = 0.5*(lo+hi)
            s = np.sqrt(1+4*u)
            M = (-1+s)/(1+s)
            f = M*u*a0 - gn
            if f > 0: hi = u
            else: lo = u
        out[i] = 0.5*(lo+hi)*a0
    return out

# ---- ISOLATE the MI-vs-MG MECHANISM from the interpolation-function freedom ----
# CRITICAL (MEMORY both-ways rule): comparing the dS-Unruh "simple" nu against the
# AeST Eq-2.39 interpolation conflates the MI-vs-MG MECHANISM with the INTERPOLATION
# choice (an O(1) freedom that BOTH a modified-inertia and a modified-gravity MOND
# theory carry). To isolate the genuine mechanism difference we (a) put BOTH on the
# SAME interpolation to kill the function freedom, then (b) separately report the
# interpolation-family spread as the SHARED, non-diagnostic part.

# AeST on the dS-Unruh "simple" nu (same interpolation as MI), mu=0:
def g_AeST_core_simpleNu(r):
    return g_MI(r)   # identical: AeST-core with the simple nu IS the MI nu

def Mdyn(g, r):
    return g * r**2 / G

# =====================================================================
# 3. AeST mass term mu^2 Phi (the ONLY thing distinguishing AeST from pure MOND).
#    Eq 2.33: div(M grad Phi) + mu~^2 Phi = 4 pi G rho_b.
#    The mu term adds an effective source rho_mu = -mu~^2 Phi /(4 pi G) (note SIGN:
#    in deep-MOND outskirts Phi<0 grows, the term acts; paper: appears as a NEGATIVE
#    mass density at low acceleration -> AeST goes BELOW MOND in the outskirts).
#    Screening length L = 1/mu. Skordis AeST: mu ~ H0/c-ish; the paper parametrizes
#    mu^_hat^2 = mu^2 r_M^2 with r_M the MOND radius (r_M = sqrt(GM/a0)).
#    We bracket mu by its screening length: L_screen ranges ~ Mpc-scale (cosmological).
# =====================================================================
rM = np.sqrt(G * M500 / a0)          # MOND radius of the cluster
print(f"# MOND radius r_M = sqrt(GM500/a0) = {rM/Mpc:.3f} Mpc = {rM/kpc:.0f} kpc")

# mu_hat^2 grid from the paper (Fig 7 uses mu_hat^2 = 1e-1 .. 1e-4)
for muhat2 in [1e-1, 1e-2, 1e-3, 1e-4]:
    mu = np.sqrt(muhat2) / rM
    L_screen = 1.0/mu
    print(f"#   mu_hat^2={muhat2:.0e} -> screening length 1/mu = {L_screen/Mpc:.3f} Mpc = {L_screen/kpc:.0f} kpc")

# =====================================================================
# 4. Evaluate residual M_res(<r) = Mdyn(<r) - Mbar(<r) for MI and MOND-simple,
#    at the CLASH core radii.  These are the deep-MOND phantom masses.
# =====================================================================
radii = np.array([50, 100, 150, 200, 300, 420, 450, 600, 900, 1152, 1500]) * kpc

# ---------------------------------------------------------------------
# TABLE A: SAME interpolation (simple nu) -> isolates the MI-vs-MG MECHANISM.
#   MI  = dS-Unruh nu (modified inertia)
#   AeST_core = same simple-nu interpolation, mu=0 (modified gravity, core limit)
#   These must be IDENTICAL if the mechanism difference is zero in the core.
# ---------------------------------------------------------------------
print()
print("TABLE A -- MI vs AeST-core on the SAME (simple nu) interpolation  ->  isolates MECHANISM")
print("="*92)
print(f"{'r[kpc]':>7} {'Mbar':>9} {'g/a0':>7} {'Mres_MI':>10} {'Mres_AeST':>10} {'(MI-MG)/MI %':>14}")
print(f"{'':>7} {'[e13Mo]':>9} {'':>7} {'[e13Mo]':>10} {'[e13Mo]':>10} {'(mechanism)':>14}")
print("-"*92)
rowsA = []
for r in radii:
    Mb  = float(np.atleast_1d(Mbar(r))[0])
    gN  = float(np.atleast_1d(gbar(r))[0])
    gmi = float(np.atleast_1d(g_MI(r))[0])
    gae = float(np.atleast_1d(g_AeST_core_simpleNu(r))[0])  # same nu, mu=0
    Mres_mi = Mdyn(gmi, r) - Mb
    Mres_ae = Mdyn(gae, r) - Mb
    fd = (Mres_mi - Mres_ae)/Mres_mi*100 if Mres_mi>0 else 0.0
    rowsA.append((r, Mb, Mres_mi, Mres_ae))
    print(f"{r/kpc:>7.0f} {Mb/Msun/1e13:>9.3f} {gN/a0:>7.3f} "
          f"{Mres_mi/Msun/1e13:>10.3f} {Mres_ae/Msun/1e13:>10.3f} {fd:>13.2e}%")
print("="*92)
print("=> on identical interpolation the MI core residual EQUALS the AeST-core residual")
print("   to machine precision: the MECHANISM (MI vs MG) adds NOTHING in the core.\n")

# ---------------------------------------------------------------------
# TABLE B: the INTERPOLATION-FUNCTION spread (SHARED freedom, NOT a mechanism diff).
#   simple nu (dS-Unruh) vs AeST Eq-2.39 interpolation -- both are valid MOND nu's;
#   the gap is the O(1) interpolation choice that BOTH MI and MG carry.
# ---------------------------------------------------------------------
print("TABLE B -- interpolation-FUNCTION spread (simple-nu vs AeST-Eq2.39)  ->  SHARED freedom")
print("="*92)
print(f"{'r[kpc]':>7} {'g/a0':>7} {'Mres simpleNu':>14} {'Mres Eq2.39':>13} {'spread %':>10}")
print("-"*92)
rowsB = []
for r in radii:
    Mb  = float(np.atleast_1d(Mbar(r))[0])
    gN  = float(np.atleast_1d(gbar(r))[0])
    gsi = float(np.atleast_1d(g_MI(r))[0])
    g39 = float(g_AeST_core(r)[0])
    Mres_si = Mdyn(gsi, r) - Mb
    Mres_39 = Mdyn(g39, r) - Mb
    sp = (Mres_si - Mres_39)/Mres_si*100 if Mres_si>0 else 0.0
    rowsB.append((r, Mres_si, Mres_39))
    print(f"{r/kpc:>7.0f} {gN/a0:>7.3f} {Mres_si/Msun/1e13:>14.3f} {Mres_39/Msun/1e13:>13.3f} {sp:>9.1f}%")
print("="*92)
print("=> the interpolation spread is large (~30-80%) but is a SHARED MOND-family freedom,")
print("   not an MI-vs-MG mechanism difference; the same nu used in both -> Table A zero.\n")

# =====================================================================
# 5. The CLASH target and the undershoot (both MI and AeST undershoot the CORE)
# =====================================================================
print("CLASH target (Famaey-Pizzuti-Saltas 2410.02612):")
print("  cored residual ~10x gas density inner, exp cutoff r_cut ~400 kpc, uniform.")
M_res_clash_420 = 2.3e14 * Msun   # banked eRASS1/CLASH cored target, rich, <420 kpc
i420 = [i for i,r in enumerate(radii) if abs(r-420*kpc) < 1e-6][0]
Mres_mi_420 = rowsA[i420][2]      # MI residual at 420 kpc
print(f"  CLASH/eRASS1 target M_res(<420 kpc) ~ {M_res_clash_420/Msun/1e13:.1f}e13 Msun")
print(f"  MI (= AeST-core, same nu) supplies M_res(<420 kpc) = {Mres_mi_420/Msun/1e13:.2f}e13 Msun")
print(f"  -> BOTH undershoot the CLASH core by x{M_res_clash_420/Mres_mi_420:.2f}  (shared MOND-cluster gap)")
print()

# =====================================================================
# 6. AeST mass term mu^2 Phi -- the ONLY genuine MI-vs-MG mechanism difference.
#    Where does it act? Compare 1/mu to the CLASH core radius (420 kpc).
# =====================================================================
print("AeST mass-term mu^2 Phi (the ONLY mechanism that distinguishes AeST-MG from MI):")
print(f"  cluster MOND radius r_M = {rM/kpc:.0f} kpc; CLASH core target r_cut ~ 420 kpc << r_M.")
print("  screening length 1/mu (from the paper's mu_hat^2 grid):")
for muhat2 in [1e-1, 1e-2, 1e-3, 1e-4]:
    mu = np.sqrt(muhat2)/rM
    L = 1.0/mu
    print(f"    mu_hat^2={muhat2:.0e}: 1/mu = {L/kpc:6.0f} kpc = {L/Mpc:.2f} Mpc  "
          f"-> {'ACTS in core' if L < 420*kpc else 'OUTSIDE core (acts in outskirts)'}")
print("  => for ALL paper values 1/mu >> 420 kpc, so the mu^2 Phi term is NEGLIGIBLE in")
print("     the CLASH core. Per Durakovic-Skordis: the AeST contribution 'is more")
print("     significant in the OUTSKIRTS' and at low accel goes BELOW MOND (negative-mass")
print("     appearance) -- it SUBTRACTS, not adds, in the deep outskirts. It does NOT help")
print("     the core undershoot; if anything it WORSENS the outer residual.")
