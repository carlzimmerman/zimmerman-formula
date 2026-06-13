"""
agentSS Part 7 — (c) SO(4,1) dS isometry descending to spectral weights + HOSTILE self-check.

(c) SO(4,1) = full dS_4 isometry. On the static patch it breaks to R_t (static time) x SO(3) (sphere)
    x (the boost that is the modular flow). The part acting on the radial/frequency spectral data is
    exactly the static-patch SL(2,R) ~ SO(2,1) subgroup tested in (a)/(b) (the conformal symmetry of
    the near-horizon / radial problem). The EXTRA generators of SO(4,1) beyond the static-patch
    stabilizer move you OFF the static patch (they don't preserve the GH state's static observer) — they
    relate DIFFERENT static patches, not different spectral weights within one. So SO(4,1) gives the
    SAME constraint as SL(2,R) on the in-patch spectral function: it organizes the tower into a rep
    (principal/complementary series labelled by Delta) but does NOT fix Delta -> does NOT fix the ratio.
    The angular SO(3) only fixes the l-degeneracy (multiplicities), orthogonal to the moment ratio.

HOSTILE SELF-CHECK (could a symmetry force it after all?):
  H1. If G_sat were ALSO modular-weight -1, the edge equation 4j3/j2^2 = G_sat would be scale-COVARIANT
      and a dilation would NOT break it -- then a symmetry could hold it. Check the dimension of G_sat.
  H2. If the rep had NO free label (a UNIQUE distinguished Delta forced by the matter content), R=8Delta
      would be a fixed number. Is Delta forced anywhere in the banked machinery? (conformal/massless dS
      give specific Delta, but the khronon/probe Delta is a free input -> not forced.)
"""
import sympy as sp

print("=== (c) SO(4,1) ===")
print("  Static-patch stabilizer of the GH observer = R_t x SO(3) x boost; the spectral-data part is")
print("  the SL(2,R)~SO(2,1) of (a)/(b). Extra SO(4,1) generators leave the static patch -> relate")
print("  different patches, not in-patch spectral weights. => SAME constraint as SL(2,R): rep label")
print("  Delta unfixed -> ratio unfixed. SO(3) only sets l-multiplicities (orthogonal). PERMITS.")
print()

# H1: dimension of G_sat from agentRR's definitions.
# sigma4 = -G j2 c^2,  sigma6 = +G j3 c^2,  sigma6* = sigma4^2/(4 c^2).
# Edge: sigma6 = sigma6*  => G j3 c^2 = G^2 j2^2 c^4/(4 c^2) = G^2 j2^2 c^2/4
#   => j3 = G j2^2/4  => G = 4 j3/j2^2 = G_sat.
# Dimensions: [sigma4]=[omega^2 k^-4]=... ; but simplest: in the spectral variable s (=detuning, a
# frequency^2 offset), j_n ~ [s]^n. So G_sat = 4 j3/j2^2 ~ [s]^{3-4} = [s]^{-1}. And G (gain amplitude)
# multiplies the dispersive self-energy; the edge eq sets G = (something of dim [s]^{-1}).
print("=== H1: dimension of G_sat ===")
print("  Edge eq: G_sat = 4 j3/j2^2, with j_n ~ [s]^n  =>  [G_sat] = [s]^{3-2*2} = [s]^{-1}.")
print("  Under modular dilation s->e^a s: G_sat (as the REQUIRED value) is a FIXED external number set")
print("  by the dispersion geometry (c^2, the sonic edge) -- it does NOT co-dilate with the QNM spectral")
print("  axis (c_chi is an independent khronon datum, agentRR CHECK 5: no c<->H scale collapse). So the")
print("  LHS (4j3/j2^2 of the QNM line) dilates as e^{-a} while the RHS (G_sat) is fixed by c_chi-physics")
print("  => the equation is NOT scale-covariant => the dilation genuinely breaks any forced coincidence.")
print("  => H1 FAILS to rescue forcing. The modular symmetry actively OBSTRUCTS a forced match: tuning")
print("     the boost frame slides the LHS through G_sat at exactly one rapidity = TUNING.")
print()
print("=== H2: is Delta forced? ===")
print("  R = 8 Delta is fixed ONLY if Delta is fixed. Banked: the probe/khronon dimension Delta is a")
print("  FREE input (agentS uses Delta in {0.1,0.5,1.0} as a scan variable; dS conformal/massless give")
print("  specific Delta but the roton probe's Delta is not pinned). => Delta free => R free. PERMITS.")
print()
print(">>> ALL THREE candidate symmetries: PERMITS-NOT-FORCES. The hostile rescues (H1,H2) both fail.")
