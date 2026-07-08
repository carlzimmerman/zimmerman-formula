"""
ADVERSARIAL REFUTE CHECK: is the SURVIVES a robust OPEN region, or does it hinge on
sitting EXACTLY on the measure-zero PPN-safe surface alpha1=alpha2=0?

The refutation hypothesis (LENS): alpha1=alpha2=0 is codim-2 in (c1..c4). A theory
Cassini-safe only ON that surface is a tuning; radiative corrections detune it and
reintroduce a preferred-frame quadrupole. If SURVIVES needs EXACT alpha1=alpha2=0,
downgrade to PARTIAL.

The DEFENSE hypothesis: what actually matters for Cassini is not alpha1=alpha2=0 but
whether the induced preferred-frame quadrupole Q2 stays below the ceiling. There is a
FINITE WINDOW of nonzero (alpha1,alpha2) that is Cassini-safe. If that window is WIDE
(order-1 in alpha1,alpha2, i.e. an OPEN 4-D neighborhood, not a codim-2 surface), then
the corner is robust: you don't need to sit exactly on it, just near it, and the near-
region is a genuine 4-D open set. Detuning by radiative corrections of size delta_c
only matters if it pushes alpha out of that window.

We test: (1) the empirical PPN bounds on alpha1, alpha2 (solar-system preferred-frame),
(2) translate to a WIDTH in c-space around the surface, (3) compare to the natural size
of radiative corrections. If the Cassini-safe window in alpha is MUCH wider than any
plausible radiative shift, SURVIVES is robust (open 4-D neighborhood). If it is narrower,
it is a tuning -> PARTIAL.
"""
import numpy as np

# ---------------------------------------------------------------------------
# 1. Empirical solar-system preferred-frame bounds (these are the REAL constraints,
#    independent of Cassini-Q2; the strongest come from lunar laser ranging + pulsars).
#    alpha1, alpha2 are the PPN preferred-frame parameters.
#    Observational bounds (order of magnitude, well-established):
#       |alpha1| < ~1e-4   (LLR / binary pulsars)
#       |alpha2| < ~1e-7   (solar-spin / pulsar; tightest is ~1e-9 from pulsars but
#                            use the conservative solar-system LLR-class ~1e-5..1e-7)
# ---------------------------------------------------------------------------
alpha1_bound = 1e-4     # conservative solar-system
alpha2_bound = 1e-7     # conservative (pulsars push to 1e-9; solar-system ~1e-5)

print("="*78)
print("PPN preferred-frame window (the ACTUAL Cassini-class constraint on aether):")
print(f"  |alpha1| < {alpha1_bound:.0e},  |alpha2| < {alpha2_bound:.0e}")
print("="*78)

# ---------------------------------------------------------------------------
# 2. alpha1, alpha2 as functions of (c1..c4). Expand around the PPN-safe surface.
#    alpha1 = -8(c3^2 + c1 c4)/(2c1 - c1^2 + c3^2)
#    On the surface c4* = -c3^2/c1 the numerator c3^2 + c1 c4 = 0.
#    Perturb c4 = c4* + eps4. Then alpha1 ~ -8 c1 eps4 / D,  D = 2c1 - c1^2 + c3^2.
#    So a shift eps4 in c4 gives alpha1 ~ -8 c1 eps4 / D  =>  the WIDTH in c4 that keeps
#    |alpha1| < bound is  |eps4| < bound * |D| / (8 c1).
# ---------------------------------------------------------------------------
def alpha1_of(c1,c3,c4):
    D = 2*c1 - c1**2 + c3**2
    return -8*(c3**2 + c1*c4)/D

def alpha2_of(c1,c2,c3,c4):
    c13=c1+c3; c14=c1+c4; c123=c1+c2+c3
    D = 2*c1 - c1**2 + c3**2
    return ( (2*c13 - c14)**2/(c123*(2-c14))
             - (12*c3*c13 + 2*c1*c14*(1-2*c14) + (c1**2-c3**2)*(4-6*c13+7*c14))
               /((2-c14)*D) )

# a robust interior witness on the corner
c1,c3 = 0.526, 0.261
c4s = -c3**2/c1
c2s = (-2*c1**2 - c1*c3 + c3**2)/(3*c1)
print(f"\nwitness on corner: c1={c1} c3={c3} c2={c2s:.4f} c4={c4s:.4f}")
print(f"  alpha1 on surface = {alpha1_of(c1,c3,c4s):.3e}")
print(f"  alpha2 on surface = {alpha2_of(c1,c2s,c3,c4s):.3e}")

# width in c4 keeping |alpha1|<bound
D = 2*c1 - c1**2 + c3**2
eps4_width = alpha1_bound * abs(D)/(8*c1)
print(f"\n  d(alpha1)/d(c4) = {8*c1/abs(D):.3f}  -> |eps4| < {eps4_width:.2e} keeps |alpha1|<{alpha1_bound:.0e}")

# width in c2 keeping |alpha2|<bound (numerical derivative wrt c2, c4 held at c4*)
h=1e-6
da2_dc2 = (alpha2_of(c1,c2s+h,c3,c4s)-alpha2_of(c1,c2s-h,c3,c4s))/(2*h)
eps2_width = alpha2_bound/abs(da2_dc2)
print(f"  d(alpha2)/d(c2) = {da2_dc2:.3f}  -> |eps2| < {eps2_width:.2e} keeps |alpha2|<{alpha2_bound:.0e}")

# Also alpha2 depends on c4; width in c4 from alpha2 alone
da2_dc4 = (alpha2_of(c1,c2s,c3,c4s+h)-alpha2_of(c1,c2s,c3,c4s-h))/(2*h)
eps4_from_a2 = alpha2_bound/abs(da2_dc4) if abs(da2_dc4)>0 else np.inf
print(f"  d(alpha2)/d(c4) = {da2_dc4:.3f}  -> |eps4| < {eps4_from_a2:.2e} keeps |alpha2|<{alpha2_bound:.0e}")

print("\n" + "="*78)
print("3. IS THIS A 4-D OPEN NEIGHBORHOOD OR A CODIM-2 SURFACE?")
print("="*78)
print(f"""
  The Cassini-safe / PPN-safe REGION in the full 4-D (c1,c2,c3,c4) space is:
     |alpha1(c)| < {alpha1_bound:.0e}   AND   |alpha2(c)| < {alpha2_bound:.0e}.
  These are TWO INEQUALITIES, not two equalities. They carve out a 4-D SLAB of
  thickness ~|eps2|,|eps4| around the alpha1=alpha2=0 surface -- an OPEN set of
  FULL DIMENSION 4, not the measure-zero surface itself.

  Widths at the witness:
     c4 direction: |eps4| < {min(eps4_width,eps4_from_a2):.1e}  (from alpha1 & alpha2)
     c2 direction: |eps2| < {eps2_width:.1e}  (from alpha2)

  So you do NOT need to sit EXACTLY on the surface. You need |alpha1|,|alpha2| below
  the empirical bounds -- a slab of finite (if small) thickness in c2,c4.
""")

print("="*78)
print("4. THE ACTUAL REFUTATION QUESTION: radiative detuning vs the slab width")
print("="*78)
print(f"""
  This is where robustness is decided. The alpha1=alpha2=0 surface is NOT protected by
  a symmetry (Einstein-aether has no symmetry enforcing alpha1=alpha2=0; it is a special
  locus). So radiative corrections shift (c1..c4) by some delta_c. The theory stays
  Cassini-safe ONLY if delta_c keeps |alpha1|,|alpha2| inside the slab:
     delta(alpha1) ~ 8 c1/|D| * delta_c ~ {8*c1/abs(D):.1f} * delta_c  <  {alpha1_bound:.0e}
     delta(alpha2) ~ {abs(da2_dc2):.1f} * delta_c                      <  {alpha2_bound:.0e}
  =>  the alpha2 bound is the binding one: delta_c  <  {eps2_width:.1e}.

  In an EFFECTIVE FIELD THEORY the aether is a low-energy field with a cutoff M (the
  scale M^2 in front of L_kin). The dimensionless couplings c_i receive radiative
  corrections of NATURAL size delta_c ~ (c_i)^2/(16 pi^2) ~ 1e-2 * c_i^2 per loop from
  aether self-interaction, and ~ (m_matter/M)^n from matter loops. With c_i ~ O(0.1-1):
     delta_c(aether self-loop) ~ 1e-2 * (0.5)^2 ~ 2.5e-3.
  Compare to the slab half-width delta_c < {eps2_width:.1e} (alpha2, the tight one).
""")

slab = eps2_width
delta_c_loop = 1e-2 * c1**2
print(f"  natural 1-loop delta_c ~ {delta_c_loop:.1e}")
print(f"  alpha2 slab half-width  ~ {slab:.1e}")
ratio = delta_c_loop/slab
print(f"  ratio (loop shift / slab) = {ratio:.1f}")
if ratio > 1:
    print(f"  => a single loop OVERSHOOTS the alpha2 slab by ~{ratio:.0f}x.")
    print("     alpha2=0 is NOT radiatively stable at its natural size -> a TUNING is needed")
    print("     to hold alpha2 below its (very tight) empirical bound. This is a fine-tuning")
    print("     of the SAME kind that afflicts every Lorentz-violating EFT with tight alpha2.")
else:
    print(f"  => the loop shift is INSIDE the slab; no tuning needed -> robust.")

print("\n" + "="*78)
print("5. BUT: is this tuning SPECIAL to the framework, or GENERIC to all LV gravity?")
print("="*78)
print("""
  Key observation: the tightness of the alpha2 bound (~1e-7, pulsars 1e-9) forces a
  small-coupling / tuning in EVERY Einstein-aether-class theory, INCLUDING pure AeST and
  pure Einstein-aether. It is NOT a new problem introduced by the MI matter coupling.
  The MI question was strictly: does the MI matter coupling FORCE u to source a Cassini-
  failing quadrupole ON TOP of whatever the aether does? That is answered NO (source is
  l=0/parallel-to-u, absorbed by lambda; residual is (nu-1)^2-suppressed).

  So the detuning issue is a pre-existing property of the aether sector's Lorentz
  violation, shared with all such theories and with the Standard-Model-Extension
  literature (naturalness of small LV coefficients). It does NOT distinguish the MI
  completion from a bare healthy Einstein-aether. The MI-specific claim (the matter
  coupling does not ADD a quadrupole) is untouched.
""")
