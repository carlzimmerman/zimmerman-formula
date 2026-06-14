"""
agentXX ROUTE 1 -- PART 2: adversarial robustness of the 'free-must-tune' finding.

Part 1 showed the standard R/M^2 curvature correction is ~1e-60..1e-122 -> negligible.
HOSTILITY DEMANDS we check the cases that could make the correction LARGER:

(A) The dS extrinsic curvature K = theta/3 = H is O(H^1), not O(H^2). An operator
    linear in K could give delta(c_chi^2) ~ H/M (one power), much larger than (H/M)^2.
    Does such an operator exist / is it allowed? -> dimensional analysis + parity.

(B) Symmetry protection: is c_chi protected by a symmetry (so it does NOT run / is
    not shifted), or is it radiatively generated (so dS COULD in principle move it)?

(C) Could c_chi be locked by SYMMETRY rather than dynamics (e.g. a residual conformal
    or scale symmetry of the khronon in dS forcing c_chi = c = 1)? That would be a
    DIFFERENT lock (forced-by-symmetry to a FIXED value), not c_chi = f(H).

(D) The one scale that IS tied to H: the GH temperature T_dS = H/2pi. Does the
    thermal khronon bath shift c_chi by a factor f(T_dS/M) = f(H/M)? Same suppression.
"""

import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("agentXX ROUTE 1 PART 2: adversarial robustness")
print("="*78)

H0 = mp.mpf('2.2e-18')          # s^-1
hbar = mp.mpf('6.582e-25')      # GeV s
H0_GeV = hbar*H0
meV = mp.mpf('1e-12')           # GeV
Mpl = mp.mpf('2.435e18')        # GeV

print("\n[A] LINEAR-in-K operator: can delta(c_chi^2) ~ (H/M)^1 (one power)?")
print("    K = extrinsic curvature trace of the T=const leaves = del.u = 3H.")
print("    An operator like (K/M)(del chi)^2 is dim-5 (one power of M).")
print("    BUT: (del chi)^2 = g^ij d_i chi d_j chi is the GRADIENT term whose")
print("    coefficient IS c_chi^2. A term (K/M) h^{ij} d_i chi d_j chi shifts it:")
print("        delta c_chi^2 ~ (K/M) = 3H/M   (ONE power -- larger than (H/M)^2!)")
print("    Is this operator ALLOWED? Check the discrete symmetries:")
print("    - K = del.u changes sign under TIME REVERSAL (u -> -u): K is T-ODD.")
print("    - (del chi)^2 (spatial gradient squared) is T-EVEN.")
print("    => (K/M)(del chi)^2 is T-ODD: FORBIDDEN in a T-invariant (CPT) khronon")
print("       action. The khronon action S_u is built from T-even scalars")
print("       (u.del u)^2, (del u)^2, (del.u)^2 -- all QUADRATIC in u-derivatives,")
print("       hence T-even. A single power of K is T-odd -> not generated.")
print("    -> The leading allowed curvature shift is QUADRATIC: K^2/M^2 ~ (H/M)^2.")
print("       The (H/M)^1 enhancement is SYMMETRY-FORBIDDEN. Back to (H/M)^2.")

# sanity: even if one ALLOWED a linear term, size it:
for label, Mval in [("M_Pl", Mpl), ("meV (SC floor)", meV)]:
    lin = 3*H0_GeV/Mval
    print(f"      [hypothetical, if allowed] 3H/M at M={label}: {mp.nstr(lin,4)}")
print("    even the (forbidden) linear term is 1e-30 (meV) to 1e-60 (M_Pl): still dead.")

print("\n[B] Is c_chi PROTECTED (does not run) or RADIATIVELY GENERATED?")
print("    c_chi^2 = ratio of c_i couplings. The c_i are marginal (dim-4 operator")
print("    coefficients of (del u)^2). They RUN logarithmically and receive finite")
print("    matching, BUT there is NO symmetry forcing a SPECIFIC value -- they are")
print("    free inputs (like gauge couplings). So c_chi is NOT symmetry-fixed to a")
print("    number; it is a free dimensionless coupling. Radiative corrections shift")
print("    it by O(c_i^2/16pi^2)*log -- a SELF-correction (set by the c_i themselves),")
print("    NOT an H-dependent one. dS only enters through (curvature/M^2) insertions,")
print("    already shown ~ (H/M)^2. => no H-lock from running.")

print("\n[C] SYMMETRY lock to a FIXED value (c_chi = c = 1)? -- different question")
print("    If a residual symmetry forced c_chi^2 = 1 exactly, that is a lock to a")
print("    CONSTANT, NOT c_chi = f(H). Check: does dS restore boost invariance for")
print("    the khronon? NO -- the khronon EXISTS precisely to break boosts (defines")
print("    a preferred frame). c_T^2=1/(1-beta)=1 is forced by GW170817 (|beta|<1e-15)")
print("    but that is the SPIN-2 (tensor) speed, set by beta. The SPIN-0 speed c_chi")
print("    is a SEPARATE combination (c_123/...) NOT fixed by c_T. agentU banked the")
print("    spin-0 speed FREE in [1.000,1.033]. No symmetry pins it to 1.")
print("    => even a symmetry lock would give c_chi=const, NOT the f(H) the")
print("       edge coincidence needs. It would not help: R(H) still slides vs G_sat(const).")

print("\n[D] Gibbons-Hawking THERMAL shift: T_dS = H/2pi. Thermal correction to c_chi?")
TdS_GeV = H0_GeV/(2*mp.pi)
print("    T_dS = H/2pi =", mp.nstr(TdS_GeV,4), "GeV.")
print("    Finite-T correction to a sound speed ~ (T/M)^2 (thermal mass / loop):")
for label, Mval in [("M_Pl", Mpl), ("meV (SC floor)", meV)]:
    th = (TdS_GeV/Mval)**2
    print(f"      (T_dS/M)^2 at M={label}: {mp.nstr(th,4)}")
print("    Same (H/M)^2 suppression (T_dS ~ H). Thermal route gives NO lock either.")

print("\n[E] THE DECISIVE SCALE-SEPARATION (the recurring residual, quantified):")
print("    For dS to lock c_chi to H at O(1), the controlling scale M must satisfy")
print("    M ~ H. The khronon EFT cutoff / LV scale obeys M >= M_SC >~ meV.")
order_sep = mp.log10(meV/H0_GeV)
print("    log10(M_SC/H) >=", mp.nstr(order_sep,4), "  i.e. M is AT LEAST ~30 orders")
print("    of magnitude above H. (meV/H0_energy =", mp.nstr(meV/H0_GeV,3),
      "= 10^%.1f)" % float(order_sep))
print("    The two scales (c_chi-intrinsic M, and H) are DECOUPLED by >= 30 decades.")
print("    This is EXACTLY the recurring residual: R is H-intrinsic, G_sat/c_chi is")
print("    M-intrinsic (>= meV), and dS curvature cannot bridge a 30-decade gap with")
print("    an (H/M)^2 lever. NO RADIATIVE LOCK.")

print("\n" + "="*78)
print("PART-2 VERDICT:")
print("  (A) linear-K enhancement: SYMMETRY-FORBIDDEN (K is T-odd) -> stays (H/M)^2.")
print("  (B) c_chi is a free coupling, self-renormalizing, NOT H-locked by running.")
print("  (C) no symmetry pins c_chi (spin-0 != spin-2; c_T fixes beta, not c_chi);")
print("      and a symmetry lock would give const, not f(H) -- would not close the gap.")
print("  (D) GH-thermal shift ~ (T_dS/M)^2 = (H/M)^2: same dead suppression.")
print("  (E) decisive: lock needs M~H; EFT floor forces M>=meV, ~30+ decades above H.")
print("  => ROUTE 1 (dS-radiative/curvature) does NOT force c_chi=f(H).")
print("     c_chi remains a FREE PPN coupling that must be TUNED to land the")
print("     edge coincidence. lock_status = FREE-MUST-TUNE.")
print("="*78)
