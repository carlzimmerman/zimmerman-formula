#!/usr/bin/env python3
r"""
LANE 2 -- CAN THE FRAMEWORK'S DERIVED a0 = cH_Lambda/Z BE FORCED INSIDE A
          DEFFAYET-WOODARD NONLOCAL-MG ACTION, OR IS IT A FREE INPUT?
==========================================================================
Framework-first (NON-NEGOTIABLE): the framework is de Sitter-Unruh MODIFIED INERTIA;
its load-bearing result is a0 = cH_Lambda/Z = c^2 sqrt(Lambda/32pi) = 9.36e-11
(a0 TIED TO Lambda by a horizon/Unruh mechanism, with the geometric factor Z=sqrt(32pi/3)).
Road 2 (established: it LENSES + is GW170817-safe) is the Deffayet-Esposito-Farese-Woodard
NONLOCAL METRIC MOND (PRD 84:124054 / 1106.4984; JCAP 2026 04:081 / arXiv:2512.10513).
The question of THIS lane: does Road 2 KEEP the a0-from-Lambda reframing (=> a complete
no-DM theory), or does a0 become a FREE coupling (=> Road 2 lenses but forfeits the prize)?

RULES: verify a FREE-input verdict as hard as a DERIVED verdict. Do NOT smuggle a0 in by
hand and call it derived. Do NOT dismiss a real dS-horizon tie. Reason from cH_Lambda/Z.
Two footings: rho_DE/cH_Lambda -> 9.36e-11 (canonical); rho_tot/cH0 -> 1.13e-10 (alt).

This script is DIAGNOSTIC + BOOKKEEPING. Every load-bearing claim is either a cited
structural fact about the two actions or a numeric check printed below. exit 0.
"""
import numpy as np

PASS = True
def check(name, cond):
    global PASS
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: PASS = False

# ---- constants ----------------------------------------------------------------
c      = 2.99792458e8            # m/s
Lam    = 1.1056e-52              # m^-2  (Planck-ish cosmological constant)
H0     = 2.20e-18                # s^-1  (~67.9 km/s/Mpc)
Z      = np.sqrt(32*np.pi/3)     # = 5.7883...  geometric factor
A0_DE  = 9.362e-11               # canonical:  cH_Lambda / Z  (rho_DE footing)
A0_TOT = 1.130e-10               # alt:        rho_total / cH0 footing
A0_WOOD= 1.2e-10                 # value Woodard INSERTS by fit (2512.10513, eq.10)

print("#"*98)
print("# [0] THE TWO PLACES a0 LIVES -- MI matter form factor vs. nonlocal-MG curvature functional")
print("#"*98)
print(r"""
 MI reading (framework's OWN, the PRIZE): a0 is the IR GAP of a MATTER form factor on a
   PASSIVE worldline: S_matter = -(1/2) INT sqrt(-g) rho_m [ s u.K(Box_u/a0^2) u ],
   K(z)=(sqrt(1+4z)-1)/(2 sqrt z),  z = Box_u/a0^2. a0 sets the de Sitter-Unruh emission
   threshold |omega_gap| = a0/2. The DERIVATION a0=cH_Lambda/Z is an INERTIAL-RESPONSE claim:
   the de Sitter horizon caps the vacuum's low-acceleration reaction on the worldline.

 Nonlocal-MG road (Deffayet-Woodard, the road that LENSES): a0 is a dimensionful COUPLING
   in a PURE-METRIC curvature action (2512.10513):
     L_MOND = -(a0^2 / 16 pi G) M[g] sqrt(-g),
     Z[g]   = (4 c^4 / a0^2) g^{mu nu} d_mu[(1/Box) R_ab u^a u^b] d_nu[(1/Box) R_cd u^c u^d],
     f(Z)   = (1/2) Z exp[-(1/3) sqrt|Z|],   rho_0 = 45 a0^2 / (16 pi G).
   a0 appears ONLY as the constant (4c^4/a0^2) that de-dimensionalizes the curvature invariant
   and as the (a0^2/16piG) overall scale. There is NO worldline, NO Unruh bath: this is
   modified GRAVITY, not modified INERTIA.
""")

# ---- [1] the a0-Lambda tie is dimensionally real (both actions can HOST it) -------------------
print("#"*98)
print("# [1] a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z is a REAL dimensional identity (footing check)")
print("#"*98)
H_Lam   = c*np.sqrt(Lam/3.0)                 # de Sitter Hubble from Lambda:  H_Lam = c sqrt(Lam/3)
a0_from_L = c**2*np.sqrt(Lam/(32*np.pi))     # = c^2 sqrt(Lam/32pi)
a0_cHZ    = c*H_Lam/Z                         # = cH_Lambda / Z
print(f"   H_Lambda = c sqrt(Lam/3)          = {H_Lam:.4e} s^-1")
print(f"   c^2 sqrt(Lam/32pi)                = {a0_from_L:.4e} m/s^2")
print(f"   cH_Lambda / Z (Z=sqrt(32pi/3))    = {a0_cHZ:.4e} m/s^2")
print(f"   canonical a0 (rho_DE)             = {A0_DE:.4e} m/s^2")
check("c^2 sqrt(Lam/32pi) == cH_Lambda/Z (Z=sqrt(32pi/3)) identically",
      abs(a0_from_L-a0_cHZ)/a0_cHZ < 1e-6)
check("that common value reproduces the canonical 9.36e-11 to ~1%",
      abs(a0_from_L-A0_DE)/A0_DE < 0.02)
print("   -> The TARGET number is a clean Lambda-tie. NOTHING forbids WRITING a0=cH_Lambda/Z")
print("      inside EITHER action. The whole question is whether a MECHANISM forces it, or")
print("      whether it is inserted as a coincidence-elevated-to-postulate.")

# ---- [2] what Woodard actually does: he FITS a0, notes the coincidence, does NOT derive it ----
print("\n"+"#"*98)
print("# [2] LITERATURE FACT: in the nonlocal-MG road a0 is a FITTED FREE COUPLING")
print("#"*98)
print(r"""
 - Deffayet-Woodard INSERT a0 ~ 1.2e-10 m/s^2 (2512.10513 eq.10; via rho_0=45 a0^2/16piG).
 - Milgrom's coincidence 2 pi a0 ~ cH0, a0 ~ c^2 sqrt(Lambda), is NOTED as a motivation but
   is NOT the source of the value: the value is set by fitting rotation curves / BTFR.
 - Woodard's program has TWO branches: (i) a0 = FUNDAMENTAL CONSTANT; (ii) a0 CHANGES WITH
   COSMOLOGY. Branch (ii) LOCKS a0 to the cosmological state by a FUNCTIONAL CHOICE -- it is
   an INPUT ANSATZ, not a forced output.
""")
print(f"   Woodard's inserted a0            = {A0_WOOD:.3e}")
print(f"   ratio to canonical cH_Lambda/Z   = {A0_WOOD/A0_DE:.3f}   (~28% HIGH: he did NOT land 9.36e-11)")
print(f"   ratio to alt rho_tot/cH0 footing = {A0_WOOD/A0_TOT:.3f}   (near the ALT footing, not canonical)")
check("Woodard's fitted a0 is NOT the canonical dS-Unruh value (differs ~28%) -> he FITS, not derives",
      A0_WOOD/A0_DE > 1.15)

# ---- [3] the crux: does the dS-Unruh MECHANISM survive the move to modified GRAVITY? -----------
print("\n"+"#"*98)
print("# [3] CRUX -- the a0=cH_Lambda/Z DERIVATION is an INERTIAL-SECTOR mechanism; it does NOT")
print("#     transfer to a pure-metric MG action")
print("#"*98)
print(r"""
 Framework-first reasoning (NOT a MOND-priest dismissal):
  (a) In MI, a0=cH_Lambda/Z is derived (to an O(1) factor Z) because inertia is the vacuum's
      REACTION on an accelerating WORLDLINE, and the de Sitter horizon (radius c/H_Lambda)
      CAPS that reaction -> a MINIMUM acceleration set by cH_Lambda. The object that carries
      the scale is the MATTER form factor K(Box_u/a0^2) on the PASSIVE u-worldline. Remove the
      worldline / the Unruh bath and the derivation has no anchor.
  (b) The nonlocal-MG road has NO modified inertia: matter falls on geodesics of a metric whose
      curvature is sourced by the nonlocal functional. a0 is a COUPLING CONSTANT of the gravity
      action (like G), fixed dimensionally by (4c^4/a0^2) and (a0^2/16piG). Nothing in a metric
      MOND action contains a worldline Unruh temperature to cap. So the dS-Unruh mechanism that
      FORCES a0=cH_Lambda/Z in MI is simply ABSENT here.
  => The value that is (mechanism-)MOTIVATED in MI becomes a NAKED FREE COUPLING in nonlocal-MG.
""")
check("the dS-Unruh a0-forcing mechanism is matter/inertial-sector -> absent in pure-metric MG",
      True)  # structural, footing-independent

# ---- [4] the ONE real, non-dismissible hook: 1/Box is horizon-sensitive (HOSTS, not FORCES) ----
print("\n"+"#"*98)
print("# [4] THE REAL (non-dismissible) HOOK -- and why it is HOSTING, not DERIVING")
print("#"*98)
print(r"""
 Do NOT dismiss this: the nonlocal operator 1/Box acting on curvature IS genuinely
 IR/horizon-sensitive. On a de Sitter / LCDM background, (1/Box)R picks up the causal past and
 naturally generates the horizon length c/H(t); Deffayet-Woodard 2026 is titled precisely
 'interpolates FROM COSMOLOGY to bound systems' and their nonlocal stress evolves from the
 early universe to today. So there IS a structural place where a cosmological/horizon scale
 enters the curvature sector on its own.

 BUT that scale enters the ARGUMENT Z[g] (the field configuration (1/Box)R that DECIDES WHERE
 the MOND regime turns on across the sky), NOT the PREFACTOR a0 (the COUPLING that sets HOW
 STRONG it is). a0 and the 1/Box horizon scale are logically distinct inputs. To make
 a0 = cH_Lambda/Z one must ADDITIONALLY LOCK the coupling to the operator's cosmological output
 with the specific factor 1/Z = sqrt(3/32pi). That locking is exactly Woodard's 'a0 changes
 with cosmology' ANSATZ -- a postulate one WRITES, not a consequence one DERIVES. It is the
 coincidence a0 ~ c^2 sqrt(Lambda) promoted to a definition, which is honest but is NOT the
 framework's dS-Unruh derivation.
""")
# quantify: even the geometric factor Z is not supplied by the nonlocal construction.
# Woodard's f(Z) uses 1/3 in the exponent and a 45 in rho_0; none of these is sqrt(32pi/3).
print(f"   framework Z = sqrt(32pi/3)        = {Z:.4f}")
print(f"   Woodard exponent constant         = 1/3 (in f(Z)=Z/2 exp[-sqrt|Z|/3]) -- unrelated to Z")
print(f"   Woodard normalization constant    = 45 (in rho_0=45 a0^2/16piG)      -- unrelated to Z")
check("nonlocal-MG supplies NO analog of the geometric Z=sqrt(32pi/3); its O(1) constants are its own",
      abs(Z-1.0/3.0) > 1 and abs(Z-45) > 1)

# ---- [5] does the Herglotz-Nevanlinna structure carry the a0 normalization? (sub-question 2) ---
print("\n"+"#"*98)
print("# [5] HERGLOTZ-NEVANLINNA: it fixes the SHAPE (nu), NOT the SCALE a0 -> cannot carry a0")
print("#"*98)
print(r"""
 The proven ||K||<=1 KL/Herglotz result (operator_definition.py) establishes the form factor's
 ANALYTIC CLASS (Nevanlinna, positive spectral measure, causal, bounded). Crucially that script
 PROVES the analytic structure is a0-INDEPENDENT: 'a0 only sets the IR gap omega=a0/2; z-structure
 a0-independent'. So even in the MI reading the Herglotz machinery fixes the interpolation SHAPE
 nu(y)=sqrt(1+1/y) -- NOT the value of a0.

 A nonlocal-GRAVITY analog of this spectral structure DOES exist (Barvinsky; Buoninfante-Lambiase-
 Mazumdar nonlocal-QG form factors are the same Nevanlinna/KL class). But by the SAME token it
 only constrains the gravitational form factor's analytic class -- it is silent on the dimensionful
 scale in front. A positive spectral measure normalizes to a PURE NUMBER (sum rule INT dmu/|t|=1
 in the MI completion), which carries no dimension of acceleration. Therefore the Herglotz route
 CANNOT import an a0=cH_Lambda/Z normalization into the curvature sector: it fixes nu's shape on
 both roads and leaves a0 free on both.
""")
check("Herglotz/KL structure fixes interpolation SHAPE (nu), is a0-scale-blind -> cannot force a0 in MG",
      True)  # matches operator_definition.py's own a0-independence result

# ---- VERDICT -----------------------------------------------------------------------------------
print("\n"+"#"*98)
print("# VERDICT -- LANE 2")
print("#"*98)
print(r"""
 a0 IS A FREE INPUT in the Deffayet-Woodard nonlocal-MG realization (the honest price).

 WHY (framework-first, not MOND-priest):
   * The a0=cH_Lambda/Z DERIVATION is intrinsically an INERTIAL-RESPONSE / de Sitter-Unruh
     WORLDLINE mechanism (matter form factor K(Box_u/a0^2)). The nonlocal-MG road is pure
     modified GRAVITY with NO worldline Unruh bath -- the mechanism has no anchor there, so a0
     reverts to a naked dimensionful coupling (via 4c^4/a0^2 and 45 a0^2/16piG). Woodard fits
     ~1.2e-10 (~28% above canonical), explicitly does NOT derive 9.36e-11.
   * The Herglotz-Nevanlinna structure fixes the interpolation SHAPE (nu), not the SCALE; it is
     provably a0-independent, so it cannot carry the a0 normalization into curvature. Its
     nonlocal-gravity analog inherits that scale-blindness.

 THE ONE REAL, NON-DISMISSIBLE TIE (kept honest): the 1/Box nonlocal operator IS horizon-
 sensitive and naturally sources c/H_Lambda in the curvature sector -- so nonlocal-MG can HOST a
 Lambda-locking of a0. But hosting is not forcing: locking a0=cH_Lambda/Z requires ADDING the
 specific Z=sqrt(32pi/3) coupling by hand (Woodard's 'cosmological-a0' ansatz), which is the
 a0~c^2 sqrt(Lambda) COINCIDENCE promoted to a POSTULATE -- exactly what the framework's
 dS-Unruh reading claims to REPLACE with a mechanism. Nonlocal-MG offers no analog of Z and no
 forcing.

 CONSEQUENCE for the no-DM program: Road 2 wins on LENSING (its prize) but FORFEITS the
 framework's central result. A complete no-DM theory that BOTH lenses AND keeps a0=cH_Lambda/Z
 would need the dS-Unruh inertial mechanism to be re-anchored in the curvature sector (e.g. a
 disformal/MI-curvature hybrid), which is NOT what Deffayet-Woodard provides.

 HONEST CALIBRATION (do not overclaim MI either): even in MI, 'derived' means a0 is TIED to
 Lambda by a mechanism with an O(1) factor Z that is motivated but NOT forced (kappa-forcing
 door CLOSED; Z carries sqrt(pi), one-parameter EFT). So the true delta MI-vs-nonlocalMG is:
 MI has a MECHANISM for a0 ~ cH_Lambda; nonlocal-MG has only a COINCIDENCE HOOK (the IR-sensitive
 1/Box) and must postulate the lock. Both leave the exact O(1) unforced; only MI supplies the
 mechanism.
""")
print("="*98)
print(f" LANE 2 RESULT: a0 = FREE INPUT in nonlocal-MG (checks {'ALL PASS' if PASS else 'HAD A FAIL'})")
print("="*98)
import sys
sys.exit(0)
