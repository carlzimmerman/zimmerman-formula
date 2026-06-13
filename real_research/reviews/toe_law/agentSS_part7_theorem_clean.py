"""
agentSS Part 7 -- CLEAN SYMBOLIC PROOF of the load-bearing level-repulsion theorem (the spine of the
whole verdict). An ACTIVE (negative-residue) resonance at center omega0 shifts the retarded pole of a
mode at frequency wb=sqrt(c^2 k^2) into the UPPER half plane iff omega0 > wb (the mode is BELOW the
gain center). Since the roton fold lives BELOW the gain center (k<k0), the fold band is exactly the
UHP-unstable band, for ANY positive width gamma. This is why NO k-independent (scalar) clamp can hold
it, and why a stabilizing k-resolved clamp must KILL the gain on the fold band (=> no fold). The dS
heat kernel does not force such a clamp (Parts 4-6).
"""
import sympy as sp

R, g, w0, wb = sp.symbols('R gamma omega0 omega_b', positive=True)
I = sp.I
# retarded active line: Sigma_R(w) = -R*g/(-I*(w-w0)+g).  Leading shift of the +freq pole at w=wb:
#   delta1 = Sigma_R(wb)/(2 wb).  Im(delta1) sign decides UHP(>0)/LHP(<0).
Sig_wb = -R*g/(-I*(wb-w0)+g)
delta1 = Sig_wb/(2*wb)
# rationalize
den = (-I*(wb-w0)+g)
delta1_rat = sp.simplify(delta1 * sp.conjugate(den)/sp.conjugate(den))
Im_delta1 = sp.simplify(sp.im(sp.expand_complex(delta1)))
print("Sigma_R(wb) =", Sig_wb)
print("delta1 = Sigma_R(wb)/(2 wb)")
Im_simpl = sp.simplify(Im_delta1)
print("\nIm(delta1) =", Im_simpl)
# factor to expose the sign: should be proportional to (w0 - wb)
num, _ = sp.fraction(sp.together(Im_simpl))
print("numerator of Im(delta1) (sign-bearing) =", sp.factor(num))
print("\nThe denominator is g^2+(wb-w0)^2 > 0 and 2 wb>0, so sign(Im delta1) = sign(numerator).")
# show numerator = R*g*(w0-wb) up to positive factors
test = sp.simplify(Im_simpl - R*g*(w0-wb)/(2*wb*((wb-w0)**2+g**2)))
print("Im(delta1) - R*g*(w0-wb)/(2 wb ((wb-w0)^2+g^2)) =", sp.simplify(test), " (should be 0)")
print("\n=> Im(delta1) = R*gamma*(omega0 - omega_b) / [ 2 omega_b ((omega_b-omega0)^2 + gamma^2) ].")
print("   R>0, gamma>0, omega_b>0 => sign(Im delta1) = sign(omega0 - omega_b):")
print("     omega_b < omega0 (mode BELOW gain center): Im>0  -> UHP, UNSTABLE")
print("     omega_b > omega0 (mode ABOVE gain center): Im<0  -> LHP, stable")
print("     omega_b = omega0 (at center)             : Im=0  -> marginal")
print()
print("THEOREM (clean): a negative-residue (active) gain line destabilizes precisely the modes BELOW")
print("its center, for ANY width gamma>0. The roton fold band is k<k0 (below center) => the fold band")
print("is the unstable band. A scalar clamp rescales all k equally and cannot fix it (RR). A k-resolved")
print("clamp can only stabilize the fold band by zeroing the gain there -> no fold (Part 2). The dS heat")
print("kernel supplies a non-locality whose scale (H/c_chi) is forced FAR from k0 and whose memory is")
print("forced PASSIVE (KMS) -> it neither forces the stabilizing step-at-k0 nor folds (Parts 4-6).")
print("Hence: the k-structure that would clamp the fold is PERMITTED but NOT FORCED by the dS heat kernel.")
