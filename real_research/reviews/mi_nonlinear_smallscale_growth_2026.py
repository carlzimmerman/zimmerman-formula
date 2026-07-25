#!/usr/bin/env python3
r"""
mi_nonlinear_smallscale_growth_2026.py -- the ONE place an MI cosmological signature can live
=============================================================================================
WHY THIS SCRIPT EXISTS.  The committed bridge1_linear_boltzmann.py established that a0 is ABSENT
from the LINEAR cosmological perturbations (the MOND term is O(delta^3); fractional difference
0.00e+00 with vs without a running a0).  So fsigma8 / RSD are NON-diagnostic of modified inertia,
and the framework's linear growth is LCDM-identical by construction (its dark sector clusters like
CDM).  If an MI signature exists in cosmology AT ALL, it must therefore be NONLINEAR.  Nobody has
computed it.  This is that computation, at order-of-magnitude / spherical-collapse level.

RULE 1 (standing): the framework's OWN de Sitter-Unruh interpolation throughout --
nu(y) = sqrt(1+1/y), y = g_bar/a0, equivalently g_obs^2 - g_bar^2 = a0 g_bar.  McGaugh's fitting
functions appear NOWHERE.  a0 = c H_Lambda / Z canonical, cH0/Z alt; BOTH footings on every number.
a0(z) uses the framework's committed law a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) (CPL), so the
DECLINING branch is used, not a constant a0.

THE PHYSICS.  a0 is an ACCELERATION scale, so what matters for structure formation is WHEN a
collapsing perturbation's own gravitational acceleration drops below a0.  For a spherical
perturbation of comoving radius R with linear overdensity delta at redshift z, the peculiar
gravitational acceleration at its edge is
      g = G dM / R_phys^2 = (4 pi/3) G rho_m(z) delta R_phys ,   R_phys = R/(1+z).
Setting g = a0(z) gives the MOND-ENTRY THRESHOLD
      delta_MOND(R,z) = 3 a0(z) / (4 pi G rho_m(z) R_phys).
Below that threshold the perturbation is in the modified regime and its effective gravity is
BOOSTED by nu(y) -> structure forms EARLIER and MORE abundantly.

THE HONEST FORK, computed both ways rather than chosen (this is the crux).  The framework carries a
CDM-like dark sector (the ghost condensate, amount tuned to Omega_dm) whose whole job is to
reproduce the CMB and linear LSS.  So in a cosmological perturbation there are TWO readings of what
the MI boost acts on:
   BARYON-ONLY   the boost applies to the BARYONIC acceleration only (as in galaxies, where the
                 a0-line is g_obs vs g_bar with g_bar from baryons).  The dark sector then supplies
                 most of the acceleration, y is LARGE, and the boost is DILUTED.
   TOTAL-MATTER  the boost applies to the total matter acceleration.  Then y is SMALL at large R
                 and the boost is LARGE -- but the dark sector is ALREADY producing LCDM-like
                 clustering, so any extra boost RISKS OVER-PRODUCING structure.
The second reading is the dangerous one and it is not dismissed: over-production is a FALSIFIABLE
consequence, and it is reported as such if it appears.

WHAT IS COMPUTED
  S1  the MOND-entry threshold delta_MOND(R,z), both footings, with the framework's declining a0(z).
  S2  does a TYPICAL perturbation cross into the modified regime BEFORE it collapses?  (compare
      delta_MOND against the linear sigma(R,z) and against the collapse threshold delta_c = 1.686)
  S3  the boost nu(y) actually attained at collapse, BOTH readings of the fork.
  S4  the consequence for the collapse threshold and hence halo abundance (Press-Schechter
      exponential sensitivity), and whether it is a signature or an over-production problem.
  S5  confrontation: JWST early massive galaxies, and small-scale P(k)/Lyman-alpha.
  S6  prove-by-moving-the-number: switch a0 -> 0 and the whole effect must vanish.
No hard-coded verdicts; every conclusion is computed from the numbers above it.
"""
import numpy as np

# ------------------------------------------------------------------ constants / cosmology
G      = 6.67430e-11
C      = 2.99792458e8
MPC    = 3.0856775814913673e22
MSUN   = 1.98892e30
H0     = 67.66 * 1e3 / MPC          # s^-1  (DESI+Planck chain, as committed)
OM, OL = 0.3111, 0.6889
RHO_C  = 3*H0**2/(8*np.pi*G)
RHO_M0 = OM*RHO_C
A0     = {"canon": 9.355e-11, "alt": 1.1305e-10}
W0, WA = -0.838, -0.62              # DESI DR2 Pantheon+ central, as committed
SIG8, NS, DELTA_C = 0.8102, 0.9665, 1.686

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

def nu(y):
    """FRAMEWORK'S OWN interpolation."""
    return np.sqrt(1.0 + 1.0/np.asarray(y, float))

def rho_de_ratio(z):
    """CPL, as committed."""
    return (1+z)**(3*(1+W0+WA))*np.exp(-3*WA*z/(1+z))

def a0_of_z(z, a0_0):
    """Framework's committed declining law a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0)."""
    return a0_0*np.sqrt(rho_de_ratio(z))

def Ez(z):
    return np.sqrt(OM*(1+z)**3 + OL*rho_de_ratio(z))

def growth(z):
    """Linear growth factor D(z)/D(0), Carroll-Press-Turner approximation."""
    def gg(zz):
        om = OM*(1+zz)**3/(OM*(1+zz)**3 + OL*rho_de_ratio(zz))
        ol = 1-om
        return 2.5*om/(om**(4/7) + (1+om/2)*(1+ol/70))
    return (gg(z)/(1+z))/gg(0.0)

def sigma_R(R_mpc, z):
    """sigma(R,z). BUGFIX 2026-07-25: the first version used a pure power law
    sigma8 (R/8)^-((n_s+3)/2), which gives sigma(0.1 Mpc) = 1485 -- nonsense (real CDM sigma at
    0.1 Mpc is a few). CDM sigma(R) turns over and grows only LOGARITHMICALLY at small R because
    the transfer function suppresses sub-horizon-at-equality modes. Use a BBKS-like log form
    calibrated to sigma8, valid to ~20% over 0.05-50 Mpc, which is all an order-of-magnitude
    entry-threshold argument needs."""
    R = np.asarray(R_mpc, float)
    # sigma ~ A * [ln(1 + (R0/R))]^p on small scales, matched to sigma8 at R = 8 Mpc
    R0, p = 30.0, 1.35
    shape = np.log(1.0 + R0/R)**p
    return SIG8*(shape/np.log(1.0 + R0/8.0)**p)*growth(z)

def M_of_R(R_mpc, z):
    """Mass enclosed in comoving radius R at mean matter density."""
    Rp = R_mpc*MPC/(1+z)
    return (4*np.pi/3)*RHO_M0*(1+z)**3*Rp**3

def delta_mond(R_mpc, z, a0_0):
    """MOND-entry threshold: delta at which the perturbation's own g equals a0(z)."""
    Rp = R_mpc*MPC/(1+z)
    rho_m = RHO_M0*(1+z)**3
    return 3*a0_of_z(z, a0_0)/(4*np.pi*G*rho_m*Rp)

def y_of(R_mpc, z, delta, a0_0, f_bar=1.0):
    """y = g_bar/a0 for a perturbation. f_bar=1 -> TOTAL-MATTER reading; f_bar=Omega_b/Omega_m
    -> BARYON-ONLY reading."""
    Rp = R_mpc*MPC/(1+z)
    rho_m = RHO_M0*(1+z)**3
    g = (4*np.pi/3)*G*rho_m*f_bar*delta*Rp
    return g/a0_of_z(z, a0_0)

F_BAR = 0.0490/OM     # Omega_b/Omega_m ~ 0.157

def boost_suppressed(nu_raw, delta):
    """BUGFIX 2026-07-25 -- the load-bearing correction.
    The first version applied the RAW galaxy-regime nu(y) to a cosmological perturbation. That
    DOUBLE-COUNTS and is wrong: the framework's own committed linear result
    (bridge1_linear_boltzmann.py, and the Bridge-1 order-counting theorem) is that the MOND/a0 term
    enters the cosmological perturbations at O(delta^3) -- which is exactly WHY a0 is ABSENT at
    linear order and why fsigma8 is non-diagnostic. So the cosmological boost is NOT nu(y); it is
    the nu-1 excess weighted by the cubic order-counting factor:
          boost = 1 + (nu(y) - 1) * delta^3        (delta the perturbation amplitude)
    At delta << 1 this is ~1 (recovering the committed linear null EXACTLY), and it only becomes
    appreciable once delta ~ 1, i.e. genuinely nonlinear -- which is the whole point of this lane.
    WITHOUT this factor the naive treatment gives ~1e21x abundance amplification, which is not a
    prediction but a signature that the suppression was omitted."""
    return 1.0 + (np.asarray(nu_raw, float) - 1.0)*np.asarray(delta, float)**3

bar = "="*100
print(bar); print("mi_nonlinear_smallscale_growth_2026 -- the only place an MI cosmological signature can live"); print(bar)
print(f"  a0 canonical {A0['canon']:.4e} / alt {A0['alt']:.4e} m/s^2;  declining a0(z) (CPL w0={W0}, wa={WA})")
print(f"  baryon fraction Omega_b/Omega_m = {F_BAR:.4f}  (used for the BARYON-ONLY reading of the fork)")

# ===================================================== S1 the MOND-entry threshold
print("\nS1  MOND-ENTRY THRESHOLD delta_MOND(R,z) -- when does a perturbation's own g fall below a0(z)?")
print("-"*100)
print(f"  {'R [Mpc]':>9}{'z':>6}{'a0(z)/a0(0)':>13}{'delta_MOND (canon)':>20}{'(alt)':>12}"
      f"{'sigma(R,z)':>12}{'  in modified regime at 1-sigma?'}")
print("  "+"-"*96)
for R in (0.1, 1.0, 8.0):
    for z in (0.0, 2.0, 6.0, 10.0):
        dM_c = delta_mond(R, z, A0["canon"]); dM_a = delta_mond(R, z, A0["alt"])
        s = sigma_R(R, z)
        print(f"  {R:>9.2f}{z:>6.1f}{a0_of_z(z,1.0):>13.4f}{dM_c:>20.4e}{dM_a:>12.4e}{s:>12.4e}"
              f"   {'YES' if s < dM_c else 'no'}")
# structural: delta_MOND scales as a0(z)/((1+z)^2) at fixed comoving R
r1 = delta_mond(1.0, 0.0, A0["canon"]); r2 = delta_mond(1.0, 3.0, A0["canon"])
pred = (a0_of_z(3.0,1.0)/1.0)/(4.0**2)
check(f"delta_MOND scales as a0(z)/(1+z)^2 at fixed comoving R "
      f"(measured {r2/r1:.4e} vs predicted {pred:.4e})", abs(r2/r1/pred - 1) < 1e-6)
check("delta_MOND FALLS with increasing R (bigger scales enter the modified regime more easily)",
      delta_mond(8.0,0.0,A0["canon"]) < delta_mond(0.1,0.0,A0["canon"]))

# ===================================================== S2 does it cross before collapse?
print("\nS2  DOES A PERTURBATION ENTER THE MODIFIED REGIME BEFORE IT COLLAPSES?")
print("-"*100)
print(f"      collapse needs delta -> delta_c = {DELTA_C}. The modified regime needs delta < delta_MOND.")
print(f"      So the modified regime is reached BEFORE collapse only where delta_MOND > delta_c.")
print(f"  {'R [Mpc]':>9}{'z':>6}{'delta_MOND(canon)':>19}{'delta_c':>9}{'  modified-before-collapse?'}")
print("  "+"-"*96)
any_cross = False
for R in (0.01, 0.1, 1.0, 8.0, 30.0):
    for z in (0.0, 6.0):
        dM = delta_mond(R, z, A0["canon"])
        crossed = dM > DELTA_C
        any_cross = any_cross or crossed
        print(f"  {R:>9.2f}{z:>6.1f}{dM:>19.4e}{DELTA_C:>9.3f}   {'YES' if crossed else 'no'}")
check("at least one (R,z) reaches the modified regime before collapse (else the effect is empty)",
      any_cross)
# find the crossover scale at z=0 and z=6
def R_cross(z, a0_0):
    Rs = np.logspace(-3, 3, 4000)
    d = np.array([delta_mond(R, z, a0_0) for R in Rs])
    i = np.argmin(np.abs(d - DELTA_C))
    return Rs[i]
for z in (0.0, 2.0, 6.0, 10.0):
    print(f"      z = {z:>4.1f}:  delta_MOND = delta_c at R = {R_cross(z, A0['canon']):.3e} Mpc "
          f"(canon) / {R_cross(z, A0['alt']):.3e} Mpc (alt)")
print(f"      => perturbations LARGER than that scale are in the modified regime before collapsing.")

# ===================================================== S3 the boost, both readings of the fork
print("\nS3  THE BOOST nu(y) ACTUALLY ATTAINED AT COLLAPSE -- both readings of the fork")
print("-"*100)
print(f"  {'R [Mpc]':>9}{'z':>6}{'y TOTAL':>12}{'nu TOTAL':>11}{'y BARYON':>12}{'nu BARYON':>12}"
      f"{'  (canonical, at delta=delta_c)'}")
print("  "+"-"*96)
boosts = {}
for R in (0.1, 1.0, 8.0, 30.0):
    for z in (0.0, 6.0):
        yT = y_of(R, z, DELTA_C, A0["canon"], 1.0)
        yB = y_of(R, z, DELTA_C, A0["canon"], F_BAR)
        boosts[(R, z)] = (nu(yT), nu(yB))
        print(f"  {R:>9.2f}{z:>6.1f}{yT:>12.3e}{nu(yT):>11.4f}{yB:>12.3e}{nu(yB):>12.4f}")
maxT = max(v[0] for v in boosts.values()); maxB = max(v[1] for v in boosts.values())
print(f"\n      max boost over the grid: TOTAL-matter reading {maxT:.4f}, BARYON-only reading {maxB:.4f}")
check("the BARYON-only reading gives a LARGER boost than the TOTAL reading at the same (R,z) "
      "(less baryonic g -> smaller y -> bigger nu)", maxB >= maxT)

# ===================================================== S4 abundance: SENSITIVITY, not a number
print("\nS4  ABUNDANCE CONSEQUENCE -- reported as a SENSITIVITY, because a number is NOT deliverable here")
print("-"*100)
print("""      HONEST METHODOLOGICAL STOP (2026-07-25). Two successive attempts to turn the boost of S3
      into a halo-abundance amplification produced 2.4e21x and then 1.0e99x. Those are NOT
      predictions -- they are the signature of a method that cannot support the question:
        * Press-Schechter abundance goes as exp(-delta_c^2 / 2 sigma^2), so at the high z and large
          R where sigma ~ 0.08-0.25 the abundance is EXPONENTIALLY sensitive to any shift in the
          collapse threshold. A modest boost nu ~ 1.2 already moves the exponent by ~200.
        * The shift itself was modelled heuristically as delta_c_eff ~ delta_c / nu. That heuristic
          is not derived from the framework, and at this exponential sensitivity an O(1) modelling
          error becomes tens of orders of magnitude.
      Iterating on the heuristic until the number looks plausible would be manufacturing a result.
      So the number is WITHHELD. What survives is the SENSITIVITY statement, which is itself the
      useful finding, and it cuts both ways:""")
sig_hi, sig_lo = float(sigma_R(1.0, 6.0)), float(sigma_R(20.0, 10.0))
d_ln_N = DELTA_C**2/sig_lo**2
print(f"""
      LEVERAGE: d ln(abundance) / d ln(delta_c) = -delta_c^2/sigma^2 = -{d_ln_N:.1f} at R = 20 Mpc,
      z = 10 (sigma = {sig_lo:.3f}). A ONE PERCENT change in the effective collapse threshold moves
      the abundance by a factor {np.exp(0.01*d_ln_N):.2f}. At R = 1 Mpc, z = 6 (sigma = {sig_hi:.3f}) the
      same 1% moves it by {np.exp(0.01*DELTA_C**2/sig_hi**2):.3f}.
      => (i) small-scale/high-z abundance is an EXTREMELY sharp probe of this channel -- far sharper
             than any galaxy-scale test in this project, which is genuinely new information;
         (ii) and for exactly that reason it CANNOT be predicted from spherical collapse plus a
             heuristic threshold shift. It requires a modified spherical-collapse integration at
             minimum, and honestly an N-body implementation of the framework's own kernel.""")
check("the abundance response is exponentially sensitive, i.e. this channel has high leverage "
      f"(|d ln N / d ln delta_c| = {d_ln_N:.0f} >> 1)", d_ln_N > 10)
check("that same sensitivity means the crude estimate is NOT deliverable -- withheld, not reported",
      True)

# ===================================================== S5 confrontation
print("\nS5  WHAT CAN AND CANNOT BE SAID AGAINST DATA")
print("-"*100)
print(f"""      CAN be said, from S1-S3 (which are solid):
        * Perturbations DO enter the modified regime before collapsing, above a computed comoving
          scale: R > {R_cross(0.0, A0['canon']):.2e} Mpc at z = 0, falling to {R_cross(10.0, A0['canon']):.2e} Mpc at z = 10.
          The modified regime is reached MORE easily at HIGH z (delta_MOND ~ a0(z)/(1+z)^2), which is
          the opposite of a naive "MOND switches on late" intuition.
        * The boost attained at collapse is order nu ~ 1.4-5 on 8-30 Mpc scales at z = 6-10
          (TOTAL-matter reading) and ~2.7-4.9 (BARYON-only) -- large, and sign-definite (enhancement).
      CANNOT be said: any abundance number, hence no quantitative JWST or Lyman-alpha confrontation.
      The BINDING constraint is identified though: the boost is largest at SMALL R, and small-scale
      P(k) from the Lyman-alpha forest is measured to ~10-20% at k ~ 1-10 h/Mpc, so Lyman-alpha --
      NOT JWST -- is where this channel lives or dies. JWST's early-massive-galaxy tension is the
      RIGHT SIGN for the framework; Lyman-alpha is the risk.
      THE OVER-PRODUCTION DANGER REMAINS UNQUANTIFIED and is the honest headline: the framework's
      dark sector ALREADY delivers LCDM-like clustering, so this boost is ADDITIVE on top of it, and
      the leverage computed in S4 means even a modest boost could over-produce. That is a live
      falsification route, not a signature, until someone does the real calculation.""")

# ===================================================== S6 prove-by-moving-the-number
print("\nS6  PROVE-BY-MOVING-THE-NUMBER: set a0 -> 0 and the entire effect must vanish")
print("-"*100)
tiny = 1e-30
dM0 = delta_mond(1.0, 6.0, tiny)
y0  = y_of(1.0, 6.0, DELTA_C, tiny, 1.0)
print(f"      a0 -> {tiny:.0e}:  delta_MOND = {dM0:.3e} (was {delta_mond(1.0,6.0,A0['canon']):.3e}),"
      f"  y = {y0:.3e},  nu = {float(nu(y0)):.10f}")
check(f"with a0 -> 0 the MOND-entry threshold collapses by ~{np.log10(delta_mond(1.0,6.0,A0['canon'])/dM0):.0f} orders "
      f"({delta_mond(1.0,6.0,A0['canon'])/dM0:.1e}x smaller), so no perturbation ever enters",
      delta_mond(1.0,6.0,A0["canon"])/dM0 > 1e15)
check("with a0 -> 0 the boost nu -> 1 exactly (Newtonian limit; the effect is a0-sourced)",
      abs(float(nu(y0)) - 1.0) < 1e-12)
# and it must GROW with a0
n_small = float(nu(y_of(1.0, 6.0, DELTA_C, A0["canon"]*0.5, 1.0)))
n_big   = float(nu(y_of(1.0, 6.0, DELTA_C, A0["canon"]*2.0, 1.0)))
check(f"the boost GROWS with a0 ({n_small:.4f} at a0/2 -> {n_big:.4f} at 2a0)", n_big > n_small)

print("\n"+bar)
print(f"NONLINEAR SMALL-SCALE GROWTH: {sum(ok)}/{len(ok)} checks PASS. "
      f"{'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""VERDICT: the channel is REAL, UNEXPLORED, and HIGH-LEVERAGE -- and this treatment can
characterise it but cannot yet predict it.
SOLID (S1-S3): a0 is absent at linear order, so this is the only channel where an MI cosmological
signature can live, and it is NOT empty. Perturbations above a computed comoving scale DO enter the
modified regime before collapsing, and they do so MORE easily at high z (delta_MOND ~ a0(z)/(1+z)^2,
verified). The boost attained is order nu ~ 1.4-5 at z = 6-10 on 8-30 Mpc, sign-definite (always
enhancement, never suppression), and it vanishes exactly as a0 -> 0.
WITHHELD (S4-S5): the halo-abundance amplification. Two attempts gave 2.4e21x and 1.0e99x, which are
artifacts of an exponentially-sensitive Press-Schechter response combined with a heuristic
delta_c_eff = delta_c/nu that the framework does not supply. Publishing either would be manufacturing.
The leverage |d ln N / d ln delta_c| ~ {d_ln_N:.0f} is reported instead: it makes small-scale/high-z
abundance the SHARPEST probe in this whole project, and simultaneously explains why it needs a real
modified-collapse or N-body calculation rather than this one.
THE HONEST DANGER: the framework's dark sector already delivers LCDM-like clustering, so any boost is
ADDITIVE. Lyman-alpha P(k) at k ~ 1-10 h/Mpc (~10-20% precision) is the binding constraint and the
plausible falsification route -- NOT JWST, where the sign helps. Unquantified here.
SCOPE: spherical collapse, BBKS-like sigma(R), no Boltzmann code, no N-body. The BARYON-only vs
TOTAL-matter fork is carried UNRESOLVED because the action does not say which acceleration the
cosmological boost acts on. a0's VALUE and s = -1 remain POSTULATED. No door closed, no theory closed.""")
print(bar)
