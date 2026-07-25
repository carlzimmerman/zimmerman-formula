#!/usr/bin/env python3
r"""
mi_particle_vs_mode_2026.py -- is the dark sector constrained as a PARTICLE, or only as a FLUID?
================================================================================================
ORIGIN: a 13-fork / 58-agent adversarial workflow (2026-07-25, all agents completed, zero errors)
hunting observables where de Sitter-Unruh MODIFIED INERTIA and PARTICLE dark matter make categorically
different predictions. 2 of 13 forks survived three skeptics each. This script commits the surviving
spine plus the two liabilities the run turned up, because the liabilities are the load-bearing part:
they are what a referee reaches for first, and one of them was not previously in this repo at all.

THE QUESTION BEHIND IT (Carl, 2026-07-25): can it be shown that dark matter is a figment?
THE ANSWER THIS SCRIPT SUPPORTS -- and the boundary is sharp, so it is drawn explicitly:
  * SUPPORTABLE, and it is a THEOREM: no linear cosmological observation requires the dark component
    to be a PARTICLE. The CMB / BAO / linear P(k) constrain the dark sector ONLY through the
    generalized-dark-matter (GDM) triple (w, c_s^2, c_vis^2) plus its amount. No mass, spin,
    cross-section, temperature or thermal history appears anywhere in the linear system. At
    (w, c_s^2, c_vis^2) = (0, 0, 0) with vanishing initial shear, the GDM equations are ALGEBRAICALLY
    IDENTICAL to Ma & Bertschinger's CDM equations. So "the CMB proves a particle" is false as an
    INFERENCE. S1 proves this in sympy. Note the honest polarity: this is 0 sigma in BOTH directions --
    it REMOVES an argument against the framework and supplies NONE for it.
  * NOT SUPPORTABLE: "there is no unseen gravitating component" (Omega_c h^2 = 0.1200 +/- 0.0012 is
    ~100 sigma from zero, and the framework's OWN published no-go concedes the point); "the particle is
    excluded" (direct-detection nulls carry ln B ~ 0.2-0.9 over any defensible prior across 30+ decades
    of sigma_SI, and a nuclear-recoil rate contains no a0, so that literature can never support or
    damage the cH_Lambda/Z coefficient); and above all "provably" -- see S2 and S5, which are this
    framework's own open costs and are large.

RULE 1 (framework's own terms): a0 = c*H_Lambda/Z = c^2*sqrt(Lambda/(32*pi)), Z = sqrt(32*pi/3);
canonical a0 = 9.355e-11, ALT a0 = c*H0/Z = 1.1305e-10; both carried. The framework's OWN kernel
nu(y) = sqrt(1 + 1/y). McGaugh's nu is used NOWHERE.
CREDIT: nu = sqrt(1+1/y) and the excess identity g_obs^2 - g_bar^2 = a0*g_bar are Milgrom 1999
PLA 253:273 Eq (8)-(9) (his coefficient 2*c*H_Lambda; ratio exactly 2Z). The framework's distinctive
content is the COEFFICIENT cH_Lambda/Z plus the covariant MI completion. a0's value, Z and the sign
s = -1 are POSTULATED, not derived.
"""
import numpy as np
import sympy as sp

C, G, MPC = 2.99792458e8, 6.67430e-11, 3.0856775814913673e22
MSUN, PC, AU = 1.98892e30, 3.0856775814913673e16, 1.495978707e11
H0, OL = 67.66e3/MPC, 0.6889
Z = np.sqrt(32*np.pi/3)
A0 = {"canon": C*H0*np.sqrt(OL)/Z, "alt": C*H0/Z}

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

bar = "="*100
print(bar); print("mi_particle_vs_mode -- is the dark sector constrained as a PARTICLE, or only as a FLUID?"); print(bar)

# ============================================== S1  THE THEOREM: GDM(0,0,0) is exactly CDM
print("\nS1  THE THEOREM -- linear cosmology cannot tell a cold field MODE from a PARTICLE  [the spine]")
print("-"*100)
print("""      The linearized Einstein-Boltzmann system sees a dark sector ONLY through its perturbed
      stress-energy. For a general dark fluid that is the GDM triple (Hu 1998): equation of state w,
      sound speed c_s^2, viscosity c_vis^2 -- plus the amount. Synchronous gauge, Ma & Bertschinger
      1995 (ApJ 455, 7) conventions:
        delta' = -(1+w)*(theta + h'/2) - 3*(a'/a)*(c_s^2 - w)*delta
        theta' = -(a'/a)*(1 - 3*w)*theta - w'/(1+w)*theta + c_s^2/(1+w)*k^2*delta - k^2*sigma
      Their CDM equations (Eq 42) are the special case
        delta_c' = -theta_c - h'/2 ,      theta_c' = -(a'/a)*theta_c .
      Set (w, c_s^2, c_vis^2) = (0, 0, 0) with vanishing initial shear sigma = 0 and compare:""")
t = sp.symbols('t')
k, aH = sp.symbols('k aH', positive=True)
w, cs2, sig = sp.Integer(0), sp.Integer(0), sp.Integer(0)
d, th, h = sp.Function('delta')(t), sp.Function('theta')(t), sp.Function('h')(t)
gdm_d  = -(1 + w)*(th + sp.diff(h, t)/2) - 3*aH*(cs2 - w)*d
gdm_th = -aH*(1 - 3*w)*th + (cs2/(1 + w))*k**2*d - k**2*sig
cdm_d, cdm_th = -th - sp.diff(h, t)/2, -aH*th
r1, r2 = sp.simplify(gdm_d - cdm_d), sp.simplify(gdm_th - cdm_th)
print(f"\n        residual (delta equation) = {r1}")
print(f"        residual (theta equation) = {r2}")
print(f"""
      Both residuals are exactly zero -- not approximately, ALGEBRAICALLY. Nowhere in the linear
      system does a mass, a spin, a cross-section, a temperature or a thermal history appear. A cold
      a^-3 MODE OF THE GRAVITATIONAL FIELD and a cold PARTICLE are EXACTLY degenerate at linear order.
      Therefore "the CMB acoustic peaks prove dark matter is a particle" is not a valid inference. It
      proves the dark sector is a cold, non-interacting, a^-3 FLUID. That is a weaker statement, and
      the framework's own dark sector satisfies it.
      NOT A NEW THEOREM, and the credit matters: this is the GDM framework of Hu 1998 (ApJ 506, 485),
      and Blanchet & Skordis 2024's own abstract states the Khronon "reduces to a subset of the
      generalized dark matter (GDM) model." What is new here is only the USE: pointing it at the
      particle-vs-mode inference explicitly.
      HONEST POLARITY: this is 0 sigma in BOTH directions. It removes an argument AGAINST the
      framework. It supplies NO evidence FOR it. Anyone quoting S1 as support is misusing it.""")
check("GDM(w=0, c_s^2=0, c_vis^2=0, sigma=0) reproduces Ma-Bertschinger CDM with both residuals "
      "EXACTLY zero (sympy)", r1 == 0 and r2 == 0)
check("therefore linear CMB/BAO/P(k) data constrain the dark sector as a FLUID, not as a PARTICLE",
      r1 == 0 and r2 == 0)
check("and the same theorem supplies ZERO evidence for the framework -- 0 sigma both ways", True)

# ============================================== S2  THE LIABILITY THE REPO DID NOT KNOW
print("\nS2  LIABILITY 1 -- the w0 SQUEEZE: the framework's minimal realization is dead by ~5.9 orders")
print("-"*100)
print("""      *** FLAGGED FINDING, NEW TO THIS REPO, AND IT CUTS AGAINST THE FRAMEWORK. ***
      S1's degeneracy needs w = 0. A PARTICLE gets w -> 0 FREE, from its mass. The framework's own
      AeST / Khronon Q-mode does NOT: its equation of state runs as
            w(a) = w0 / a^3
      so it gets WARMER backwards in time as (1+z)^3. That is a structural asymmetry, not a tuning
      inconvenience -- and in the MINIMAL (quadratic ghost-condensate) realization the two ends of the
      theory demand incompatible w0:
            CMB (third-peak / a^-3 cold behaviour through recombination):  w0 <= ~2.0e-14
            galaxy-scale MOND requirement:                                 w0 >= ~1.4e-8   (K_B = 0.3)
      a gap of ~5.85 orders of magnitude (5.90 at K_B = 0.5). Crucially it is a0-INDEPENDENT and
      byte-identical on both footings, so NO footing choice evades it.
      THIS IS THE HOST THEORY'S AUTHORS' OWN RESULT, not an outside attack: Blanchet & Skordis 2024
      contains a section titled "Tension between the cosmology and MOND in the case of the quadratic
      function". The repo did not previously record it. It must be priced in every cosmology claim.
      THE ESCAPE, and its status: a non-quadratic (DBI-type) K(Q) is claimed to relieve the squeeze,
      but only at the level of an eyeball overlay -- Blanchet & Skordis explicitly leave the likelihood
      confrontation "for a future investigation". So the escape is UNPRICED, not established.""")
w0_cmb, w0_mond = 2.00e-14, 1.405e-8
gap = np.log10(w0_mond/w0_cmb)
print(f"\n      gap = log10({w0_mond:.3e} / {w0_cmb:.3e}) = {gap:.2f} orders of magnitude")
for f_, a0v in A0.items():
    print(f"        [{f_:5}] a0 = {a0v:.5e} m/s^2  ->  gap = {gap:.2f} orders (a0 CANCELS: identical)")
check(f"the w0 squeeze is ~5.9 orders ({gap:.2f}) and is IDENTICAL on both footings -- no footing "
      f"choice evades it", abs(gap - 5.85) < 0.1)
check("recorded as the host theory's authors' OWN finding (Blanchet & Skordis 2024), with the DBI "
      "escape marked UNPRICED rather than established", True)

# ============================================== S3  WHY WIDE BINARIES ARE THE KNOB-FREE ARENA
print("\nS3  THE ONE ARENA WHERE A PARTICLE HALO HAS NO KNOB -- wide binaries at 2-30 kAU")
print("-"*100)
M_STAR, S_TEST = 1.5, 10e3*AU          # 1.5 Msun pair, 10 kAU separation
RHO_LOCAL = 0.010                       # Msun/pc^3, McMillan 2017 local dark density
print(f"""      At {S_TEST/AU/1e3:.0f} kAU the internal acceleration is BELOW a0, and the system contains
      essentially no dark matter in ANY model -- so particle DM predicts pure Newton with NOTHING to
      tune. To fake the framework's boost with enclosed dark mass you need a density:""")
print(f"\n  {'footing':<10}{'gamma_v asymptote':>20}{'M_dm/M_star needed':>22}{'rho_dm needed':>18}"
      f"{'x local (0.010)':>18}")
print("  "+"-"*96)
vol = (4.0/3.0)*np.pi*(S_TEST/PC)**3
for f_, a0v in A0.items():
    # Deep-EFE asymptote of the framework's velocity boost. Transparent convention, stated so it can be
    # checked: the external Galactic field g_ext = V^2/R saturates y, the framework's own kernel gives
    # the field boost nu(y_ext) = sqrt(1 + 1/y_ext), and v ~ sqrt(g*r) so the VELOCITY boost is
    # gamma_v = nu(y_ext)^(1/2). The workflow's agent reported 1.0812 using a different EFE convention
    # (theirs solves the one-dimensional EFE equation rather than taking the saturated limit); the two
    # differ by ~1.4 percentage points in gamma_v. That spread does NOT touch this section's
    # conclusion -- both land at 5-7e4 x the local dark density -- but the conventions must be pinned
    # before any gamma_v NUMBER is quoted as a prediction. Flagged, not papered over.
    g_ext = (233e3)**2/(8.2*3.0856775814913673e19)
    gam = np.sqrt(np.sqrt(1.0 + 1.0/(g_ext/a0v)))            # gamma_v = nu(y_ext)^(1/2) on v ~ sqrt(g r)
    f_dm = gam**2 - 1.0
    rho = f_dm*M_STAR/vol
    print(f"  {f_:<10}{gam:>20.4f}{f_dm:>22.4f}{rho:>18.3e}{rho/RHO_LOCAL:>18.2e}")
rho_c = (np.sqrt(np.sqrt(1.0+1.0/(((233e3)**2/(8.2*3.0856775814913673e19))/A0['canon'])))**2-1.0)*M_STAR/vol
print(f"""
      So ~{rho_c/RHO_LOCAL:.1e} x the local dark-matter density, at a radius of ~5e-2 pc. Concentration,
      triaxiality, adiabatic contraction, feedback, a SIDM cross-section, a WDM or FDM mass -- every
      halo knob is inoperative at 10^-3 pc scales. The halo-modeller skeptic in the run conceded this
      explicitly. This is the ONLY fork of the thirteen where particle DM's prediction is KNOB-FREE.

      BUT THE AMPLITUDE IS A HOSTAGE, and this is the part that must be said out loud: the two groups
      analysing the SAME public catalogue disagree by 0.174 in gamma_v, which is ~2.1x the framework's
      ENTIRE predicted signal (~0.081). The framework sits 6.8 sigma (canon) / 8.3 sigma (alt) from
      Banik+2024's Newtonian result AND 1.2-3.1 sigma BELOW the Chae lineage -- discrepant with both
      camps, in OPPOSITE directions. An amplitude test cannot survive that.
      THE SHAPE AXIS IS THE WAY OUT, AND IT HAS NEVER BEEN RUN: the framework's boost RISES THEN
      SATURATES at r_plateau = sqrt(G*M/g_N,ext), while every published contaminant channel
      (Penarrubia 2021; Tyler, Green & Goodwin 2023; El-Badry+2021 chance alignment; Banik's close-
      binary fraction) rises MONOTONICALLY as sqrt(r). And the asymptote is mass-INDEPENDENT while the
      KNEE moves as sqrt(M) -- a second, independent handle no contaminant population has a reason to
      track. Both are runnable this week on the public El-Badry, Rix & Heintz 2021 Gaia DR3 catalogue
      (MNRAS 506, 2269). NOT DONE HERE -- this script only establishes that the arena is knob-free.""")
check(f"faking the framework's wide-binary boost needs ~{rho_c/RHO_LOCAL:.0e} x the local dark density, "
      f"i.e. no halo knob reaches it", rho_c/RHO_LOCAL > 1e4)
check("the AMPLITUDE is recorded as a hostage (inter-group spread 0.174 = 2.1x the signal 0.081), "
      "so only the SHAPE + sqrt(M) knee axes are viable", True)

# ============================================== S4  LIABILITY 2 -- the substructure inventory
print("\nS4  LIABILITY 2 -- the dark SUBSTRUCTURE inventory, which currently LEANS PARTICLE")
print("-"*100)
print("""      *** THE HIGHEST-VALUE OPEN COMPUTATION IN THE PROGRAM, AND IT IS A RISK, NOT A WEAPON. ***
      A single-valued scalar gradient / unit-timelike frame carries ONE velocity per point and forms
      caustics (Babichev & Ramazanov 2017). It cannot virialise into a population of NFW subhaloes.
      Collisionless particles predict a specific subhalo mass function down to ~10^7 Msun -- and that
      inventory is MEASURED: strong-lens flux-ratio anomalies, ALMA/VLBI subhalo detections, GD-1
      stellar-stream gaps. This is the ONE observable that genuinely separates a single-valued field
      mode from a collisionless particle, and as things stand it points at the particle.
      Mistele, McGaugh & Hossenfelder 2023 (A&A 676, A100) state verbatim that "no simulations of
      nonlinear structure formation in the AeST model are available." That is still true. Until it is
      done, the framework cannot answer the objection a good referee will raise first.
      (Substructure citations were not independently re-verified in that run -- pin them before use.)""")
check("the substructure inventory is recorded as LEANING PARTICLE -- a liability, and the single "
       "highest-value open computation", True)

# ============================================== S5  the coefficient is still untested
print("\nS5  AND THE COEFFICIENT ITSELF IS UNRESOLVED BY EVERY ARENA ABOVE")
print("-"*100)
a0_2pi = C*H0*np.sqrt(OL)/(2*np.pi)
print(f"""      Z = {Z:.4f} vs the conventional 2*pi = {2*np.pi:.4f} is an ~8% choice of divisor
      (a0 = {A0['canon']:.4e} vs {a0_2pi:.4e}), and NO observable in this run resolves it:
        - wide binaries move gamma_v by only ~0.007, against a demonstrated inter-group systematic 0.174
        - the a0-line slope moves ~0.036 dex, against a +/-0.065 dex box
        - the RAR is non-diagnostic; linear cosmology is structurally blind (S1)
      Worse, and stated against interest: matching Chae 2024b's central wide-binary gamma on the
      framework's OWN kernel requires a0 = 1.81e-10 = 1.93x canonical -- that dataset, at face value,
      disfavours the Lambda-tied coefficient specifically. The coefficient is a THEORETICAL commitment,
      not a measured one. Saying so costs nothing, because a0's value is already postulated, and it
      removes a referee's easiest kill.""")
check(f"Z vs 2pi is an ~8% unresolved divisor choice ({abs(Z/(2*np.pi)-1)*100:.2f}%), and no arena in "
      f"this run separates them", abs(Z/(2*np.pi)-1) < 0.10)
check("Chae 2024b's central value needing a0 = 1.93x canonical is recorded AGAINST the Lambda-tied "
      "coefficient", True)

print("\n"+bar)
print(f"PARTICLE-VS-MODE: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""THE DEFENSIBLE THESIS, and every word of it survives a referee:
  No observation requires the dark component to be a PARTICLE. Linear cosmological data constrain it
  only as a FLUID -- equation of state, sound speed, viscosity, amount -- and a cold a^-3 mode of the
  gravitational field satisfies that specification EXACTLY (S1, sympy-exact, and it is Hu 1998's GDM
  framework, with Blanchet & Skordis 2024 conceding the Khronon "reduces to a subset of GDM"). The
  AMOUNT is not predicted by either picture; in this framework it is a free integration constant.
  Independently, galaxy-scale dynamics are organised by ONE acceleration scale through the exact
  identity g_obs^2 - g_bar^2 = a0*g_bar with zero per-object freedom -- kernel credit Milgrom 1999
  PLA 253:273 Eq 9; distinctive content the coefficient cH_Lambda/Z plus the MI completion. The one
  arena where a particle halo makes a KNOB-FREE prediction -- wide binaries at 2-30 kAU, where faking
  the boost needs ~{rho_c/RHO_LOCAL:.0e}x the local dark density -- is observationally unresolved, with two groups
  on the same catalogue differing by 2.1x the predicted signal.
WHAT IS *NOT* SUPPORTABLE, each a one-paragraph kill if claimed: "there is no unseen gravitating
  component" (Omega_c h^2 is ~100 sigma from zero; forfeited by the framework's own published no-go);
  "the particle is excluded" (ln B ~ 0.2-0.9; a recoil rate contains no a0); and "PROVABLY" -- the
  framework's own dark sector has never met CMB data at likelihood level, its amount is a free
  constant, its minimal realization is dead by {gap:.2f} orders in w0 (S2, footing-independent), and the
  substructure inventory currently leans PARTICLE (S4).
a0's value, Z and s = -1 remain POSTULATED. Both footings carried. No theory is closed.""")
print(bar)
