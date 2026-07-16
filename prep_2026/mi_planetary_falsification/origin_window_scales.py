#!/usr/bin/env python3
r"""
ORIGIN OF omega_c -- is the surviving ~Myr crossover corner FORCED by a physical scale, or FREE?
=================================================================================================
Framework: de Sitter-Unruh MODIFIED INERTIA (Carl Zimmerman), judged on ITS OWN terms.
Own interpolation nu(y)=sqrt(1+1/y), mu(x)=(sqrt(1+4x^2)-1)/(2x)=K(x^2); horizon-derived
a0=cH_Lambda/Z. Published covariant MI action, kernel K(Box_u/a0^2), Herglotz-Nevanlinna,
sum rule INT dmu(t)/|t| = 1. Both footings carried EVERYWHERE:
    canonical a0 = cH_Lambda/Z = 9.36e-11 m/s^2   (rho_DE)
    alt       a0 = rho_tot/cH0  = 1.13e-10 m/s^2

CONTEXT (established upstream, cited file:line):
  * The a0/2 landmine: Reading A (the constitutive first-moment reduction that CARRIES the galactic
    RAR) reproduces a constant sunward tail a0/2 at every planet, excluded 10^3-10^4x per planet
    (planetary_doors/KERNEL_PLANETS.md:97-107; mi_closure_pin/CONSEQUENCES.md:96-102).
  * The operator/spectral reading (Reading B) suppresses the tail kinematically (10-13 orders) but
    (i) ERASES the galactic RAR (KERNEL_PLANETS.md:136-142) and (ii) carries an excluded universal
    secular drift a0/c ~ 1e-11/yr (KERNEL_PLANETS.md:117-134).
  * The published action FORCES the kernel memory corner to a0: omega_c(action)=a0/2c, tau_mem=2c/a0
    = 203 Gyr (canon)/168 Gyr (alt) -- and REJECTS an orbital-scale corner as a new scale absent from
    S (mi_field_theory/CLOSURE_MAP.md:59, item d).
  * The only RAR-preserving solar-system survivor is a GATED "Reading C": MI amplitude x a Lorentzian
    frequency gate L_c(omega/omega_c), corner omega_c FREE (CLOSURE_MAP.md:88-115; the pullback leaves
    the reduction weighting eta(beta) free, mi_closure_pin/CONSEQUENCES.md:20-30).

THIS SCRIPT does two things, both exit-0, both footings, NO hard-coded verdict booleans:
  PART 1 -- recompute the JOINT allowed omega_c window from the ACTUAL published bounds:
      lower edge = galactic RAR preservation (gate >= 0.90 at the deepest confirmed MOND orbit);
      upper edge = LLR secular-drift ceiling (Biskupek & Mueller 2021 Gdot/G);
      show the per-planet reactive edge (Fienga & Minazzoli 2024, binding planet Saturn) and the
      MESSENGER Gdot/G edge (Genova 2018) are BOTH looser -> LLR binds. => WINDOW NON-EMPTY.
  PART 2 -- test each candidate physical ORIGIN of omega_c explicitly:
      (a) dS-Unruh bath re-thermalization / KMS Matsubara scale at T_dS;
      (b) local matter density / screening ("plasma-like") scale sqrt(4 pi G rho);
      (c) finite light-crossing / retardation scale of the source (c/r) and the kernel's own c/a0;
      (d) a second dimensionful scale in the Herglotz measure beyond a0.
    For each: compute the frequency, ask does it land in [omega_lo, omega_hi], and is it FORCED (a
    derived theory scale) or CHOSEN (environmental/contingent/absent). Report FORCED (name it) or FREE.

Every measured bound is cited with value+sigma in-line. Every derived number is printed.
"""
import numpy as np, sys

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond)
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

# ----------------------------------------------------------------------------- constants + footings
C      = 2.99792458e8       # m/s
G      = 6.674e-11          # m^3 kg^-1 s^-2
YR     = 3.155815e7         # s (Julian yr)
GYR    = YR*1e9
MYR    = YR*1e6
MSUN   = 1.989e30           # kg
PC     = 3.0857e16          # m
KPC    = 1e3*PC
FOOTINGS = (("canonical", 9.36e-11), ("alt", 1.13e-10))

print("#"*98)
print("# PART 1 -- THE JOINT ALLOWED omega_c WINDOW FROM THE ACTUAL PUBLISHED BOUNDS (both footings)")
print("#"*98)

# --- lower edge: galactic RAR preservation ---------------------------------------------------------
# Gated Reading C: MOND amplitude retained at orbital frequency omega is the Lorentzian low-pass
# L_c(omega/omega_c) = 1/(1+(omega/omega_c)^2). To KEEP the galactic RAR we require the gate to be
# OPEN (>= 0.90) at the DEEPEST CONFIRMED MOND orbit. That orbit: y = a/a0 ~ 0.8 (deep-MOND SPARC
# edge), circular speed v ~ 25 km/s (dwarf/outer-disk), so omega_gal = a/v = y a0 / v.
# L_c >= 0.90  <=>  (omega_gal/omega_c)^2 <= 1/9  <=>  omega_c >= 3 omega_gal.  (exact)
y_deep, v_deep = 0.8, 25e3   # deepest confirmed MOND orbit
def Lc(omega, wc): return 1.0/(1.0 + (omega/wc)**2)

# --- upper edge: LLR secular-drift ceiling ---------------------------------------------------------
# Biskupek, Mueller & Torre 2021, Universe 7:34 (arXiv:2012.12032): Gdot/G = (-5.0 +/- 9.6)e-15 /yr.
# 2-sigma ceiling on |drift| = |central| + 2*sigma = 5.0e-15 + 2*9.6e-15 = 2.42e-14 /yr.
LLR_central, LLR_sigma = 5.0e-15, 9.6e-15                 # /yr
LLR_2sig = LLR_central + 2*LLR_sigma                      # /yr = 2.42e-14
# Gated drift channel at the LLR body (the Moon). The phase/dissipative channel is opened by the gate
# up to the corner: d ln r/dt = (a0/g_N) * omega_c evaluated at the Moon (g_N,moon = 2.70e-3 m/s^2).
# [derivation: Im K = a0/(2 c omega); tangential drag d ln r/dt = 2 omega Im K = a0/c ungated
#  (KERNEL_PLANETS.md:117-124); the GATE makes the secular channel scale linearly with the corner,
#  d ln r/dt|gated = (a0/g_N) omega_c at the probed body -> reproduces the banked edge exactly.]
gN_moon = 2.70e-3            # m/s^2, Earth-Moon Newtonian accel (KERNEL_PLANETS.md:105)

# --- looser edges, shown for completeness (LLR must BIND) -------------------------------------------
# Per-planet REACTIVE edge, Fienga & Minazzoli 2024 (LRR 27:1, arXiv:2303.01821, Table 10). Binding
# planet = Saturn, delta_g bound 7.0e-15 m/s^2. Gated reactive residual at Saturn: 1-ReK ~ 1/(8W^2)
# with W=c omega/a0 -> under the gate the reactive residual ~ g_N,Sat * L_c(omega_Sat/omega_c); the
# banked reactive ceiling is omega_c <= 8.27e-11 (canon)/7.52e-11 (alt) rad/s -- 3-4 orders LOOSER.
reactive_edge = {"canonical": 8.27e-11, "alt": 7.52e-11}  # rad/s (banked, KERNEL_PLANETS.md:152-153)
# MESSENGER Gdot/G, Genova et al. 2018 (Nat. Commun. 9:289): |Gdot/G| < 4e-14 /yr -- LOOSER than LLR.
MESSENGER_Gdot = 4e-14      # /yr

windows = {}
for name, a0 in FOOTINGS:
    omega_gal = y_deep*a0/v_deep
    lo = 3*omega_gal                                       # RAR-preservation lower edge
    hi = LLR_2sig/(YR*(a0/gN_moon))                        # LLR drift upper edge  (rad/s)
    # cross-check: MESSENGER edge (rad/s) using the same channel -> must be looser (larger) than LLR hi
    hi_messenger = MESSENGER_Gdot/(YR*(a0/gN_moon))
    windows[name] = (lo, hi)
    print(f"\n [{name}] a0 = {a0:.3e} m/s^2")
    print(f"   deepest MOND orbit: omega_gal = y a0/v = {omega_gal:.3e} rad/s (y={y_deep}, v={v_deep/1e3:.0f} km/s)")
    print(f"   LOWER edge (RAR gate >=0.90): omega_c >= 3 omega_gal = {lo:.3e} rad/s")
    print(f"   UPPER edge (LLR Gdot/G 2sig={LLR_2sig:.2e}/yr): omega_c <= {hi:.3e} rad/s")
    print(f"     [LLR at Moon: d ln r/dt = (a0/g_N) omega_c ; g_N,moon={gN_moon:.2e} m/s^2]")
    print(f"   ...vs MESSENGER edge (Genova 2018, <{MESSENGER_Gdot:.0e}/yr): omega_c <= {hi_messenger:.2e} rad/s  (LOOSER)")
    print(f"   ...vs per-planet reactive edge (Saturn, Fienga-Minazzoli 2024): omega_c <= {reactive_edge[name]:.2e} rad/s  (LOOSER by ~{np.log10(reactive_edge[name]/hi):.1f} dex)")
    tau_lo, tau_hi = 1.0/hi, 1.0/lo                        # memory time tau = 1/omega_c
    print(f"   ===> WINDOW  omega_c in [{lo:.2e}, {hi:.2e}] rad/s  =  tau in [{tau_lo/MYR:.2f}, {tau_hi/MYR:.2f}] Myr"
          f"  (width x{hi/lo:.2f})")
    check(f"[{name}] window NON-EMPTY (RAR-lower < LLR-upper)", hi > lo)
    check(f"[{name}] LLR BINDS from above (LLR edge < MESSENGER edge < reactive edge)",
          hi < hi_messenger < reactive_edge[name])

print("\n   PART 1 RESULT: the joint window is NON-EMPTY on BOTH footings; the LLR secular-drift")
print("   ceiling (Biskupek & Mueller 2021) BINDS from above, ~3-4 dex tighter than the per-planet")
print("   reactive edge and tighter than MESSENGER. The framework SURVIVES the solar system IFF the")
print("   corner sits in this ~Myr sliver. PART 2 asks whether any theory scale PUTS it there.")

# ==================================================================================================
print("\n"+"#"*98)
print("# PART 2 -- IS THE ~Myr CORNER FORCED BY A PHYSICAL SCALE, OR FREE? (test each candidate)")
print("#"*98)

def verdict_scale(label, omega_by_footing, forced, note):
    """Print whether a candidate scale lands in the window on each footing, and FORCED vs CHOSEN."""
    lands_any = False
    for name, a0 in FOOTINGS:
        lo, hi = windows[name]
        om = omega_by_footing[name]
        inside = (lo <= om <= hi)
        lands_any = lands_any or inside
        rel = np.log10(om/lo) if om < lo else (np.log10(om/hi) if om > hi else 0.0)
        where = "IN-WINDOW" if inside else (f"{-rel:.1f} dex BELOW" if om < lo else f"{rel:.1f} dex ABOVE")
        print(f"     [{name}] omega = {om:.3e} rad/s  -> {where}")
    print(f"     origin: {'FORCED (theory scale)' if forced else 'CHOSEN (not a theory constant)'} ; {note}")
    return lands_any, forced

results = {}

# --- (a) dS-Unruh bath re-thermalization / KMS Matsubara scale at T_dS -----------------------------
print("\n (a) dS-Unruh BATH re-thermalization / KMS Matsubara scale at T_dS = H_Lambda/2pi:")
# The dS thermal bath's intrinsic response frequencies are its Matsubara poles. CLOSURE_MAP.md:58 and
# CONSEQUENCES.md:20-27: the nearest Matsubara pole sits at kappa = H_Lambda (the HORIZON), NOT any
# orbital scale; the pullback pole is kappa_eff = sqrt(H_Lambda^2 + (a/c)^2) >= H_Lambda. So the bath's
# only intrinsic re-thermalization frequency is ~H_Lambda. Compute H_Lambda two consistent ways.
# way 1: H_Lambda = c sqrt(Lambda/3), Lambda ~ 1.1e-52 m^-2 (Planck 2018).
Lambda = 1.1e-52
H_Lambda_cosmo = C*np.sqrt(Lambda/3.0)
print(f"     H_Lambda (=c sqrt(Lambda/3), Lambda={Lambda:.1e} m^-2) = {H_Lambda_cosmo:.3e} rad/s")
oa = {}
for name, a0 in FOOTINGS:
    # way 2 (footing-consistent): the action's own memory corner a0/2c, and the bath scale ~H_Lambda.
    # In the framework a0 = c H_Lambda / Z, so H_Lambda = Z a0/c is the SAME family as a0/2c up to the
    # O(1) constant Z/2. Both are ~1e-18..1e-19 rad/s. Use H_Lambda_cosmo as the bath scale (footing-
    # independent physical horizon rate); the action corner a0/2c is shown alongside.
    wc_action = a0/(2*C)
    oa[name] = H_Lambda_cosmo
    print(f"     [{name}] action memory corner a0/2c = {wc_action:.3e} rad/s (tau_mem=2c/a0={2*C/a0/GYR:.0f} Gyr)")
la, fa = verdict_scale("(a)", oa, forced=True,
    note="H_Lambda is a genuine theory scale, but it is the HORIZON rate ~1e-18 rad/s; the dS bath has "
         "NO intrinsic ~Myr re-thermalization time -- its only response scale is kappa=H_Lambda, ~4 dex "
         "BELOW the window. A ~Myr bath time is not present in the theory.")
results["(a) dS bath / Matsubara"] = (la, fa)

# --- (b) local matter density / screening ("plasma-like") scale ------------------------------------
print("\n (b) DENSITY / SCREENING scale  omega = sqrt(4 pi G rho)  (a plasma-like corner?):")
# A density-set corner would be the gravitational dynamical/Jeans frequency sqrt(4 pi G rho). Evaluate
# at the two physically relevant densities; note it is ENVIRONMENTAL (not a theory constant) and spans
# orders across environments -- and planets share the local density with the local galactic orbit.
rho_local = 0.10*MSUN/PC**3      # solar-neighborhood total (Oort) dynamical density ~0.1 Msun/pc^3
rho_cosmic = 2.7e-27             # kg/m^3, cosmic mean matter density (~0.3 rho_crit)
w_local  = np.sqrt(4*np.pi*G*rho_local)
w_cosmic = np.sqrt(4*np.pi*G*rho_cosmic)
print(f"     rho_local  = {rho_local:.2e} kg/m^3 (0.1 Msun/pc^3)  -> sqrt(4 pi G rho) = {w_local:.3e} rad/s")
print(f"     rho_cosmic = {rho_cosmic:.2e} kg/m^3 (0.3 rho_crit)  -> sqrt(4 pi G rho) = {w_cosmic:.3e} rad/s")
ob = {name: w_local for name, _ in FOOTINGS}   # local-stellar is the closest candidate; test it
lb, fb = verdict_scale("(b)", ob, forced=False,
    note=f"the local-stellar value {w_local:.1e} is the CLOSEST candidate (a factor ~{windows['canonical'][0]/w_local:.1f} "
         f"below the window bottom) but density is ENVIRONMENTAL, not a theory constant: it spans "
         f"{w_cosmic:.0e}..{w_local:.0e} rad/s (3+ dex) across environments, and planets share the LOCAL "
         f"density with the local galactic orbit -- so a density-set corner cannot separate them. CHOSEN.")
results["(b) density / screening"] = (lb, fb)

# --- (c) light-crossing / retardation scale of the source ------------------------------------------
print("\n (c) LIGHT-CROSSING / RETARDATION scale  omega = c/r  (and the kernel's own c/a0):")
# Retardation of the Sun's field across the orbit: omega = c/r. r-DEPENDENT (not universal). The
# theory's OWN retardation/memory length is c/a0 (Compton length of the massive auxiliary modes,
# CONSEQUENCES.md:157-159) -> omega = a0/c ~ horizon.
r_saturn = 1.434e12   # m
r_galaxy = 8.2*KPC
for r, lab in ((r_saturn, "Saturn orbit"), (r_galaxy, "galactic 8.2 kpc")):
    print(f"     c/r ({lab}, r={r:.2e} m) = {C/r:.3e} rad/s")
oc = {}
for name, a0 in FOOTINGS:
    oc[name] = a0/C     # the theory's own retardation frequency (kernel Compton scale)
    print(f"     [{name}] kernel retardation a0/c = {a0/C:.3e} rad/s (Compton length c/a0 = {C/a0/(GYR*C):.0f} Gyr-light)")
lc, fc = verdict_scale("(c)", oc, forced=True,
    note="source light-crossing c/r is r-DEPENDENT (1e-12 at galaxies, 1e-4 at Saturn -- ABOVE the "
         "window and non-universal); the theory's OWN retardation a0/c is the HORIZON scale ~3e-19 "
         "rad/s (~4 dex below). No retardation scale in the theory lands at ~Myr.")
results["(c) retardation c/r, c/a0"] = (lc, fc)

# --- (d) a second dimensionful scale in the Herglotz measure ---------------------------------------
print("\n (d) A SECOND SCALE IN THE HERGLOTZ MEASURE beyond a0?")
# The measure dmu(t) lives on the K(z)=(sqrt(1+4z)-1)/(2 sqrt z) cut. Its ONLY structure is the branch
# point at z=-1/4 (i.e. t=1/4 in units of a0^2) -- a DIMENSIONLESS pure number, not a new dimensionful
# scale: the argument is Box_u/a0^2, so t=1/4 <-> |a|=a0/2, still set by a0 alone. Sum rule and ||K||<=1
# fix NORMALIZATION only, not a second scale. Verify the branch point and that it carries no new scale.
z_branch = 0.25   # dimensionless
print(f"     measure cut boundary t = {z_branch} (dimensionless, in units of a0^2) -> |a| = a0/2 = a0*{np.sqrt(z_branch):.3f}")
print(f"     sum rule INT dmu/|t| = 1 (v11) and ||K||<=1 fix NORMALIZATION only; no 2nd dimensionful scale.")
# The ONLY dimensionful scale the measure introduces is a0 itself. So any frequency built from the
# measure is a0/c-family -> horizon, not Myr. Represent as omega = sqrt(z_branch)*a0/c (|a|=a0/2 -> a0/2c).
od = {}
for name, a0 in FOOTINGS:
    od[name] = np.sqrt(z_branch)*a0/C   # = a0/2c, the ONLY frequency the measure can build
    print(f"     [{name}] only measure frequency sqrt(1/4)*a0/c = a0/2c = {od[name]:.3e} rad/s")
ld, fd = verdict_scale("(d)", od, forced=True,
    note="the Herglotz measure has NO second dimensionful scale: its only structure (branch point t=1/4) "
         "is dimensionless in a0^2 units; the sum rule/||K||<=1 fix normalization only. Every frequency it "
         "builds is a0/c-family (~1e-19 rad/s, ~4-5 dex below the window). Single-scale by construction.")
results["(d) Herglotz 2nd scale"] = (ld, fd)

# ==================================================================================================
print("\n"+"#"*98)
print("# VERDICT")
print("#"*98)
any_forced_in_window = any(lands and forced for (lands, forced) in results.values())
any_lands = any(lands for (lands, forced) in results.values())
print("   candidate scale                     lands in window?   forced theory scale?")
for k,(lands,forced) in results.items():
    print(f"     {k:<34} {'YES' if lands else 'no ':<17} {'YES' if forced else 'no'}")
print()
# The corner is FORCED only if SOME candidate is BOTH a forced theory scale AND lands in the window.
check("NO forced theory scale lands in the ~Myr window: (a) dS bath = horizon H_Lambda (~4 dex below); "
      "(c) retardation a0/c = horizon (~4 dex below) and c/r is r-dependent & above; (d) the Herglotz "
      "measure is single-scale a0 (no 2nd scale). The one near-miss (b) density is ENVIRONMENTAL, not a "
      "theory constant, and spans 3+ dex. => omega_c is NOT forced.",
      not any_forced_in_window)
check("=> the surviving ~Myr corner is a FREE add-on: an honest 5th constant {s,a0,Z,eta} -> +omega_c. "
      "The published action forces the memory corner to a0/2c (~200 Gyr, RAR-dead), NOT into the window; "
      "the pullback leaves eta(beta) free; no dS-bath/density/retardation/measure scale supplies it.",
      not any_forced_in_window)

print("""
   HONEST FINDING (reported straight -- this is a CONDITIONAL survival, neither a manufactured kill
   nor a manufactured save):
     * PART 1: the joint window is NON-EMPTY on both footings. Lower edge = galactic RAR preservation;
       upper edge = the LLR secular-drift ceiling (Biskupek & Mueller 2021), which BINDS ~3-4 dex
       tighter than the per-planet reactive edge (Fienga-Minazzoli 2024) and tighter than MESSENGER
       (Genova 2018). canon [9.0e-15, 2.2e-14] rad/s = tau 1.43-3.53 Myr; alt [1.1e-14, 1.8e-14] =
       tau 1.73-2.92 Myr. So the framework SURVIVES the solar system as a gated Reading-C crossover.
     * PART 2: the required ~Myr corner is NOT forced by any physical scale in the theory. Every
       genuine theory scale (dS bath H_Lambda; kernel retardation a0/c; the single-scale Herglotz
       measure) is the HORIZON scale ~1e-18..1e-19 rad/s -- ~4-5 dex BELOW the window. The one
       near-miss is the local-density plasma-like scale sqrt(4 pi G rho_local) ~ 2e-15 rad/s (a factor
       ~4 below the window bottom), but density is environmental, spans 3+ dex, and cannot separate
       planets from the co-located galactic orbit -- CHOSEN, not forced.
     * VERDICT: SURVIVES, CONDITIONALLY. omega_c is a FREE 5th constant. The framework passes the
       solar system only by ADDING an honest postulate the published action does not supply (the
       action's own corner, a0/2c ~ 200 Gyr, is RAR-dead). Not a falsification; not a clean win.
   HONEST CEILING: at planetary accelerations (10^4-10^8 a0) GR and healthy MOND-family theories both
   predict ~0; every number here discriminates among the framework's OWN readings, never vs LCDM.
   Two-sided falsifiable: a confirmed Chae-type AQUAL-strength wide-binary boost kills the gated
   survivor; a x3 INPOP/EPM secular refit either detects the drift or closes the window from above.""")

print("="*98)
print(f" ORIGIN: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*98)
sys.exit(0 if PASS else 1)
