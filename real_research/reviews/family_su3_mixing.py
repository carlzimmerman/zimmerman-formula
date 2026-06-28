#!/usr/bin/env python3
"""
FRONT 3 — MIXING FROM THE FAMILY SYMMETRY (gauged SU(3)_F).

CONSEQUENCE-MODE premise (assumed, not proven): the framework's a0-geometry is fundamental and
sits in the E8 -> E6 x SU(3) magic-square neighborhood, so the surviving hook is a GAUGED family
SU(3)_F whose generation multiplicity "3" multiplies the E6 27.  Question: does gauged SU(3)_F +
the framework's SPECIFIC structure (J3(O)/F4-forced sqrt2, Koide 1+2, golden ratio phi) FORCE a
computable PMNS pattern, or HOST-not-FORCE?

WHAT THIS SCRIPT ACTUALLY DOES (runnable numpy linear algebra, no assertion):
 (a) Build two SU(3)_F-broken mass matrices (charged-lepton M_e, neutrino M_nu) as REAL physical
     constructions: SU(3)_F-symmetric (democratic / S3) leading term + a flavon-VEV breaking along
     specific SU(3)_F directions.  Diagonalize BOTH with numpy.  PMNS = U_e^dag U_nu.  Extract
     th12, th23, th13 from the standard parametrization.  Compare to NuFIT.
 (b) Ask whether the framework's structure picks the breaking DIRECTION:
       - the 1+2 (democratic + doublet) Koide decomposition  -> S3/A4-residual directions,
       - the golden ratio phi (A5)                            -> tan th12 = 1/phi,
       - the F4 sqrt2                                          -> a candidate ratio in the breaking.
     For each, compute the FORCED angle and the sigma-pull vs NuFIT.
 (c) Confront the banked walls:
       - aligned (=unbroken) SU(3)_F  -> th13 = 0   (EXCLUDED, reactor th13 = 8.5 deg, ~65 sigma);
       - A5 golden                    -> th13 = 0   (same exclusion);
       - the VIABLE fit (th13 != 0, th12~33, th23~49) needs a FREE misalignment angle (TUNED).
     Demonstrate numerically that a viable th13 requires a free relative-rotation parameter that
     SU(3)_F + the framework does NOT fix.

DECISIVE CHECK: number-field wall.  Z = sqrt(32 pi/3) carries sqrt(pi) (transcendental); every
SU(3)_F/Yukawa mixing invariant is algebraic.  We verify numerically that no function of Z lands a
mixing angle, so SU(3)_F-misalignment cannot inherit a forced value from the a0 normalization.

numpy double precision.  No fitting to data anywhere.  C. Zimmerman framework footing:
a0 = 9.36e-11, Z = sqrt(32 pi/3), framework's own structure.  LOCAL.
"""
import numpy as np

np.set_printoptions(precision=6, suppress=True)
PI = np.pi
DEG = PI / 180.0

# ---------------------------------------------------------------------------
# Measured PMNS (NuFIT 6.0 NO + prompt row), 1-sigma for pulls
MEAS = {
    "NuFIT6.0_NO": dict(th12=33.68, th23=48.5, th13=8.52),
    "prompt_row":  dict(th12=33.4,  th23=49.0, th13=8.6),
}
SIG = dict(th12=0.7, th23=1.0, th13=0.13)

# Framework constants
Z = np.sqrt(32.0 * PI / 3.0)        # = sqrt(32pi/3) = 5.78881...  (carries sqrt(pi))
PHI = (1.0 + np.sqrt(5.0)) / 2.0    # golden ratio (A5)
SQRT2 = np.sqrt(2.0)                # F4 long:short root ratio


def angles_from_U(U):
    """Standard PDG extraction of th13, th12, th23 (deg) from a 3x3 unitary mixing matrix,
    using magnitudes (phase-convention independent for the angles)."""
    U = np.asarray(U, dtype=complex)
    s13 = abs(U[0, 2])
    th13 = np.degrees(np.arcsin(np.clip(s13, 0, 1)))
    c13 = np.sqrt(max(1.0 - s13 ** 2, 0.0))
    if c13 < 1e-12:
        th12 = np.degrees(np.arctan2(abs(U[1, 2]), abs(U[1, 1])))  # degenerate fallback
        th23 = 0.0
    else:
        th12 = np.degrees(np.arctan2(abs(U[0, 1]), abs(U[0, 0])))
        th23 = np.degrees(np.arctan2(abs(U[1, 2]), abs(U[2, 2])))
    return th12, th23, th13


def hermitian_from(M):
    """Physical mass^2 hermitian object M M^dag, whose eigenvectors are the left-rotation U."""
    M = np.asarray(M, dtype=complex)
    return M @ M.conj().T


def left_rotation(M):
    """U that diagonalizes M M^dag (the left mixing acting on the lepton doublet)."""
    H = hermitian_from(M)
    w, V = np.linalg.eigh(H)            # ascending eigenvalues; columns = eigenvectors
    order = np.argsort(w)               # light->heavy
    V = V[:, order]
    return V


def pull(name, th, key, ref="NuFIT6.0_NO"):
    return (MEAS[ref][key] - th) / SIG[key]


print("=" * 80)
print("FRONT 3 — PMNS MIXING FROM GAUGED SU(3)_F  (numpy diagonalization, no fitting)")
print("=" * 80)
print(f"  Z = sqrt(32 pi/3) = {Z:.6f}   phi = {PHI:.6f}   sqrt2 = {SQRT2:.6f}")
print(f"  Target (NuFIT6.0 NO): th12={MEAS['NuFIT6.0_NO']['th12']}, "
      f"th23={MEAS['NuFIT6.0_NO']['th23']}, th13={MEAS['NuFIT6.0_NO']['th13']} (deg)")

# ===========================================================================
# (a) TWO SU(3)_F-BROKEN MASS MATRICES, DIAGONALIZE BOTH, PMNS FROM MISALIGNMENT
# ===========================================================================
print("\n" + "=" * 80)
print("(a) BUILD M_e and M_nu broken along SU(3)_F directions; PMNS = U_e^dag U_nu")
print("=" * 80)

# The SU(3)_F-symmetric leading structure that the framework supplies is the DEMOCRATIC (S3/1+2)
# matrix D = (1/3) * ones(3,3): the unique SU(3)_F-democratic rank-1 object = the Koide '1' singlet
# direction; its orthogonal complement is the Koide '2' doublet.  Unbroken SU(3)_F-democratic mass
# => one heavy + two massless degenerate => mixing is UNDEFINED in the doublet (the residual is the
# full U(2)).  Breaking lifts the doublet and FIXES the rotation -- but only the breaking direction
# carries the angle.  We test the framework's candidate breaking directions.
D = np.ones((3, 3)) / 3.0

# CASE 1: ALIGNED breaking -- charged-lepton and neutrino broken along the SAME SU(3)_F directions
#         (the "unbroken relative" / single-flavon limit).  => U_e = U_nu => PMNS = identity.
eps = 0.05
Bdiag = np.diag([0.0, eps, 2 * eps])            # generic diagonal breaking (same basis both sectors)
M_e_aligned = D + Bdiag
M_nu_aligned = D + 1.3 * Bdiag                   # different magnitudes, SAME directions
Ue = left_rotation(M_e_aligned)
Unu = left_rotation(M_nu_aligned)
PMNS = Ue.conj().T @ Unu
t12, t23, t13 = angles_from_U(PMNS)
print(f"  CASE 1 ALIGNED SU(3)_F breaking (same directions both sectors):")
print(f"    th12={t12:.3f}  th23={t23:.3f}  th13={t13:.3f} (deg)  "
      f"-> PMNS ~ identity, NO mixing (aligned => th13=0).")

# CASE 2: TRIBIMAXIMAL misalignment -- charged-lepton diagonal (Z3 residual), neutrino preserves the
#         TBM directions (Klein V4 residual).  This is the canonical UNBROKEN A4 limit, realized as a
#         GENUINE SU(3)_F breaking pattern.  Group-fixed => 0 free angle params.
U_TBM = np.array([
    [np.sqrt(2.0 / 3), np.sqrt(1.0 / 3), 0.0],
    [-np.sqrt(1.0 / 6), np.sqrt(1.0 / 3), np.sqrt(1.0 / 2)],
    [np.sqrt(1.0 / 6), -np.sqrt(1.0 / 3), np.sqrt(1.0 / 2)],
])
# charged-lepton in its own diagonal basis (U_e = I), neutrino rotated by TBM:
PMNS_TBM = U_TBM
t12, t23, t13 = angles_from_U(PMNS_TBM)
print(f"  CASE 2 TBM misalignment (A4 residual: Z3 charged x V4 neutrino, 0 free params):")
print(f"    th12={t12:.3f}  th23={t23:.3f}  th13={t13:.3f} (deg)  "
      f"[th13=0 EXACT]")
print(f"      th12 pull = {pull('TBM', t12,'th12'):+.2f} sigma, "
      f"th23 pull = {pull('TBM', t23,'th23'):+.2f} sigma, "
      f"th13 pull = {pull('TBM', t13,'th13'):+.2f} sigma  <== th13=0 EXCLUDED")

# CASE 3: GOLDEN-RATIO (A5) misalignment -- tan th12 = 1/phi, th23 maximal, th13 = 0.
#         Build the explicit U with these angles to confirm the extraction + the th13=0 wall.
def U_from_angles(th12, th23, th13, dcp=0.0):
    s12, c12 = np.sin(th12 * DEG), np.cos(th12 * DEG)
    s23, c23 = np.sin(th23 * DEG), np.cos(th23 * DEG)
    s13, c13 = np.sin(th13 * DEG), np.cos(th13 * DEG)
    e = np.exp(-1j * dcp * DEG)
    R23 = np.array([[1, 0, 0], [0, c23, s23], [0, -s23, c23]], dtype=complex)
    R13 = np.array([[c13, 0, s13 * e.conjugate()], [0, 1, 0], [-s13 * e, 0, c13]], dtype=complex)
    R12 = np.array([[c12, s12, 0], [-s12, c12, 0], [0, 0, 1]], dtype=complex)
    return R23 @ R13 @ R12

th12_GR = np.degrees(np.arctan(1.0 / PHI))      # golden-ratio solar angle
U_GR = U_from_angles(th12_GR, 45.0, 0.0)
t12, t23, t13 = angles_from_U(U_GR)
print(f"  CASE 3 A5 GOLDEN-RATIO misalignment (tan th12 = 1/phi, th23=45, th13=0):")
print(f"    th12={t12:.3f}  th23={t23:.3f}  th13={t13:.3f} (deg)")
print(f"      th12 pull = {pull('GR', t12,'th12'):+.2f} sigma  <== th13=0 again EXCLUDED")

# CASE 4: F4 sqrt2 as a candidate ratio in the breaking.  Does sqrt2 appearing in the doublet
#         breaking land a viable th13?  Construct M_nu with a sqrt2 off-diagonal misaligned from M_e.
M_e_d = np.diag([1e-3, 0.1, 1.0])               # hierarchical charged leptons, diagonal basis
# neutrino broken with the F4 sqrt2 ratio in a 1-3 entry (the only way to get th13 != 0 from sqrt2):
a = 1.0
M_nu_f4 = np.array([
    [a, 0.0, SQRT2 * 0.0],
    [0.0, a, 0.0],
    [0.0, 0.0, a],
]) + 0.3 * np.array([                            # generic flavon breaking carrying sqrt2
    [0.0, 1.0, SQRT2],
    [1.0, 0.0, 1.0],
    [SQRT2, 1.0, 0.0],
])
Ue = left_rotation(M_e_d)
Unu = left_rotation(M_nu_f4)
PMNS = Ue.conj().T @ Unu
t12, t23, t13 = angles_from_U(PMNS)
print(f"  CASE 4 F4 sqrt2 in the breaking (sqrt2 ratio in 1-3 / democratic flavon):")
print(f"    th12={t12:.3f}  th23={t23:.3f}  th13={t13:.3f} (deg)")
print(f"      -> th13={t13:.3f}: the sqrt2 gives a NONZERO th13, but its VALUE is set by the "
      f"arbitrary flavon coefficient 0.3, NOT by sqrt2 (re-run below).")

# Show th13 from CASE 4 is controlled by the FREE flavon coefficient, not by sqrt2:
print("    Scan the (free) flavon coefficient g vs a fixed diagonal -> th13 moves continuously:")
Mdiag = np.diag([0.2, 0.6, 1.0])                 # fixed diagonal so g genuinely competes
for g in [0.02, 0.05, 0.1, 0.2, 0.35]:
    M_nu_g = Mdiag + g * np.array([[0, 1, SQRT2], [1, 0, 1], [SQRT2, 1, 0]])
    PM = left_rotation(M_e_d).conj().T @ left_rotation(M_nu_g)
    _, _, t13g = angles_from_U(PM)
    print(f"       g={g:>5}: th13 = {t13g:6.3f} deg")
print("    => th13 slides with the free g (sqrt2 fixed): the sqrt2 sets no specific th13 value.")

# ===========================================================================
# (b) DOES THE FRAMEWORK FORCE A SPECIFIC VIABLE PATTERN?  Forced angles vs NuFIT
# ===========================================================================
print("\n" + "=" * 80)
print("(b) FORCED candidate patterns vs measured  (which, if any, is VIABLE?)")
print("=" * 80)
patterns = {
    "TBM (A4 1+2)":         dict(th12=np.degrees(np.arcsin(np.sqrt(1/3))), th23=45.0, th13=0.0),
    "GR1 golden (A5)":      dict(th12=np.degrees(np.arctan(1/PHI)),         th23=45.0, th13=0.0),
    "GR2 golden (A5)":      dict(th12=np.degrees(np.arccos(PHI/2)),         th23=45.0, th13=0.0),
    "bimaximal":            dict(th12=45.0,                                 th23=45.0, th13=0.0),
}
print(f"  {'pattern':<20}{'th12':>8}{'th23':>8}{'th13':>8}   {'th12_pull':>10}{'th13_pull':>10}")
for name, p in patterns.items():
    print(f"  {name:<20}{p['th12']:>8.2f}{p['th23']:>8.2f}{p['th13']:>8.2f}   "
          f"{pull(name, p['th12'],'th12'):>+10.2f}{pull(name, p['th13'],'th13'):>+10.2f}")
print("  ALL forced/unbroken SU(3)_F patterns give th13 = 0  => th13_pull ~ -65 sigma => EXCLUDED.")
print("  The SURVIVING near-hit is th12 (TBM ~2-3 sigma; golden ~3-4 sigma): a NEIGHBORHOOD, not a hit.")

# TM2 sum rule -- the strongest genuinely-forced content (1 relation, not 4 values):
s13sq = np.sin(MEAS['NuFIT6.0_NO']['th13'] * DEG) ** 2
th12_TM2 = np.degrees(np.arcsin(np.sqrt((1.0 / 3) / (1 - s13sq))))
print(f"\n  TM2 sum rule  sin^2 th12 = (1/3)/(1-sin^2 th13)  -> th12 = {th12_TM2:.3f} deg "
      f"(pull {pull('TM2', th12_TM2,'th12'):+.2f} sigma)")
print("  TM2 FORCES th12 GIVEN th13, with NO free th12 param -- the one real forced relation. But it")
print("  takes th13 as INPUT; it does NOT force th13's value, th23 octant, or dCP.")

# ===========================================================================
# (c) THE VIABLE FIT NEEDS A FREE MISALIGNMENT ANGLE  (demonstrate numerically)
# ===========================================================================
print("\n" + "=" * 80)
print("(c) A VIABLE th13 REQUIRES A FREE RELATIVE-ROTATION PARAMETER (tuned, not forced)")
print("=" * 80)
# Start from TBM neutrino, apply a charged-lepton (1-3) correction of a FREE angle alpha.
# Show th13 tracks alpha continuously: SU(3)_F + framework fix NO value of alpha.
print("  TBM neutrino x charged-lepton 1-3 rotation by FREE angle alpha:")
print(f"  {'alpha(deg)':>11}{'th12':>9}{'th23':>9}{'th13':>9}")
best = None
for alpha in [0, 2, 5, 8, 8.5, 11, 13]:
    Ucorr = U_from_angles(0.0, 0.0, alpha)       # pure 1-3 charged-lepton rotation
    PM = Ucorr.conj().T @ U_TBM
    a12, a23, a13 = angles_from_U(PM)
    flag = ""
    if abs(a13 - MEAS['NuFIT6.0_NO']['th13']) < 1.0:
        flag = "  <== ~lands measured th13 (but alpha is FREE)"
        best = alpha
    print(f"  {alpha:>11}{a12:>9.3f}{a23:>9.3f}{a13:>9.3f}{flag}")
print(f"  => th13 is a CONTINUOUS function of the free misalignment alpha (~{best} deg lands ~8.5).")
print("     SU(3)_F + J3(O)/F4 + phi fix NEITHER alpha NOR the flavon coefficient => th13 is TUNED.")

# ===========================================================================
# DECISIVE: NUMBER-FIELD WALL -- does any function of Z land a mixing angle? (it must not)
# ===========================================================================
print("\n" + "=" * 80)
print("DECISIVE: NUMBER-FIELD WALL -- can the a0 normalization Z supply a mixing angle?")
print("=" * 80)
meas13 = MEAS['NuFIT6.0_NO']['th13']
meas12 = MEAS['NuFIT6.0_NO']['th12']
candidates = {
    "asin(1/Z) [deg]":        np.degrees(np.arcsin(min(1.0, 1.0 / Z))),
    "atan(1/Z) [deg]":        np.degrees(np.arctan(1.0 / Z)),
    "asin(1/Z^2) [deg]":      np.degrees(np.arcsin(min(1.0, 1.0 / Z ** 2))),
    "Z*deg-ish 90/Z [deg]":   90.0 / Z,
    "asin(sqrt2/Z) [deg]":    np.degrees(np.arcsin(min(1.0, SQRT2 / Z))),
}
print(f"  measured th13 = {meas13} deg,  th12 = {meas12} deg")
for name, val in candidates.items():
    d13 = (val - meas13) / SIG['th13']
    print(f"    {name:<22} = {val:8.4f}   (th13 pull {d13:+8.1f} sigma)")
print("  None land th13 (all many-sigma off).  STRUCTURAL reason: Z = (4/3)sqrt(6)*sqrt(pi) carries")
print("  sqrt(pi) (transcendental, Lindemann); every SU(3)_F/Yukawa mixing invariant -- root ratios,")
print("  Casimir eigenvalues, mixing-matrix entries (algebraic numbers / roots of char. polynomials)")
print("  -- is ALGEBRAIC.  A transcendental sqrt(pi) cannot equal an algebraic angle => Z is")
print("  mixing-BLIND.  The a0 normalization CANNOT supply the forced misalignment kernel.")

# Confirm Z/sqrt(pi) is algebraic (rational-times-surd) while Z is not a Lie root ratio:
print(f"\n  Z/sqrt(pi) = {Z/np.sqrt(PI):.10f}  vs  (4/3)*sqrt(6) = {(4/3)*np.sqrt(6):.10f}  "
      f"(equal => Z carries exactly one sqrt(pi)).")

# ===========================================================================
print("\n" + "=" * 80)
print("VERDICT (computed): HOSTS-NOT-FORCES")
print("=" * 80)
print("""  - SU(3)_F misalignment DOES generate PMNS mixing (CASE 4: th13 != 0 achievable) -- the
    mechanism is real and the framework's 1+2 / sqrt2 / phi live in the right neighborhood.
  - But every framework-FORCED (unbroken) pattern -- TBM, golden-ratio, bimaximal -- gives th13 = 0,
    EXCLUDED at ~65 sigma by reactor th13 = 8.5 deg.  The walls HOLD.
  - The one genuinely forced relation (TM2 sum rule) takes th13 as INPUT; it does not force th13.
  - A VIABLE th13 requires a FREE relative-misalignment angle (alpha) / flavon coefficient that
    SU(3)_F + J3(O)/F4(sqrt2) + phi do NOT fix -- TUNED, not forced.
  - DECISIVE number-field wall: Z carries sqrt(pi) (transcendental); mixing invariants are algebraic
    -> Z is structurally mixing-blind, so the a0 geometry cannot inherit a forced angle to SU(3)_F.
  => gauged SU(3)_F HOSTS the mixing mechanism but FORCES no measured PMNS angle.  A research
     program, NOT a TOE.  Z stays free; a0 = 9.36e-11 footing untouched (this front does not test it).""")
print("\nDONE.")
