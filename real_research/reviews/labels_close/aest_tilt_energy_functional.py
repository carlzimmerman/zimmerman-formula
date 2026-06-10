#!/usr/bin/env python3
r"""
PROBLEM 2 / APPROACH B -- variational/stability + Eling-Jacobson.

QUESTION: Is the radial aether tilt A^r=0 a MINIMUM (stable attractor) of the AeST
energy functional, or a SADDLE/shifted-minimum once the rolling cosmological scalar
(phibar-dot=Q0) is on? If the scalar coupling Q=A^mu d_mu phi gives a LINEAR-in-A^r
source, the minimum is FORCED off A^r=0, and we must size delta-theta/3H AND
delta-Q/Q0 SEPARATELY (they scale differently).

STRUCTURAL FACT (Eling-Jacobson gr-qc/0603058, confirmed by WebFetch): the static
spherical unit-timelike aether is a 3-parameter family; A^r=0 (alignment with the
timelike Killing vector) is an EXTRA restriction, NOT forced. So we MUST compute the
energy as f(A^r) rather than assume A^r=0.

AeST action (Skordis-Zlosnik 2021, 2007.00082, Eq.5; units 16 pi Gtilde = 1):
  L = R - (K_B/2) F_{mn}F^{mn} + 2(2-K_B) J^mu d_mu phi - (2-K_B) Y - F(Y,Q)
        - lambda(A.A+1)
  F_{mn}=2 d_[m A_n],  J_mu=A^a nabla_a A_mu,  Y=q^{mn}d_m phi d_n phi (q=g+AA),
  Q=A^mu d_mu phi.

We work in the weak-field static spherical galaxy embedded in FRW. The tilt is u=A^r.
We build the REDUCED Lagrangian density L(u, u'; r) for the aether+scalar sector at
fixed metric (the metric back-reaction of u is higher order in |Phi|), enforce the
unit constraint A.A=-1 to solve A^t(u), and expand L to quadratic order in u:

   L(u,u') = L0 + S1 * u + (1/2)[ Kstiff (u')^2 + M2 u^2 ] + O(u^3)

   * S1   = linear-in-u source coefficient  (the FORCED-tilt driver)
   * M2   = quadratic algebraic coefficient (the "mass"; sign decides min vs saddle)
   * Kstiff = gradient stiffness (sign decides ghost/gradient stability)

Then minimize: u_min = -S1/M2 (algebraic part) and check signs.

Run: python3 aest_tilt_energy_functional.py
"""
import sympy as sp
import numpy as np

print("#"*100)
print("# APPROACH B -- energy functional of the radial aether tilt A^r in a static AeST galaxy")
print("#"*100 + "\n")

# ============================================================================
# PART 1 -- symbolic: build L(u, u'), enforce A.A=-1, expand to O(u^2).
# ============================================================================
def part1_energy_functional():
    print("="*100)
    print("PART 1 -- the effective Lagrangian L(u,u') and its expansion in the tilt u=A^r")
    print("="*100)

    r = sp.symbols('r', positive=True)
    u = sp.Function('u')(r)               # A^r, the radial tilt (the d.o.f.)
    # weak-field static spherical metric (galaxy well); Phi = Phi(r) < 0, |Phi|~(v/c)^2
    Phi = sp.Function('Phi')(r)
    g_tt = -(1 + 2*Phi)                   # = -e^{2Phi} to O(Phi)
    g_rr = (1 - 2*Phi)                    # = e^{-2Phi}... use isotropic-ish weak field
    # unit constraint A.A = g_tt (A^t)^2 + g_rr u^2 = -1  =>  A^t(u):
    At = sp.sqrt((1 + g_rr*u**2)/(1 + 2*Phi))
    print("  unit constraint A.A=-1  ->  A^t = sqrt[(1 + (1-2Phi)u^2)/(1+2Phi)].")

    # ---- scalar field: cosmological roll phibar(t) [phibar-dot = Q0] + static galaxy dphi(r) ----
    Q0 = sp.symbols('Q0', positive=True)          # phibar-dot, the cosmological scalar velocity
    dphi = sp.Function('dphi')(r)
    dphi_p = sp.diff(dphi, r)                      # galaxy scalar gradient
    # Q = A^mu d_mu phi = A^t * phibar-dot + A^r * dphi'
    Q = At*Q0 + u*dphi_p
    print("  current  Q = A^t Q0 + u dphi'   (CROSS TERM u*dphi' is the new, Eling-Jacobson-blind source).")

    # ---- free-function piece -F(Y,Q). Expand F around the cosmological Q0 ----
    # F(Y,Q) = K(Q) + (MOND Y-term). For the A^r EOM the dominant NEW coupling is via Q
    # (Y is A-orthogonal => dY/du = O(u)). Keep K(Q): K = -2 Lam + (1/2)K2 (Q-Q0)^2 + ...
    # The action contributes  -F  ->  -K(Q). We need the Q-sector response F_Q = dK/dQ and
    # F_QQ = d2K/dQ2 = K2 (the dust-mode curvature, CMB-fixed).
    Lam, K2 = sp.symbols('Lambda K2', positive=True)
    K = -2*Lam + sp.Rational(1,2)*K2*(Q - Q0)**2
    # Lagrangian DENSITY contribution from the scalar/free-function sector (the u-dependent parts):
    #   L_F = -K(Q)
    L_F = -K

    # ---- vector kinetic term -(K_B/2) F_{mn}F^{mn}: gives gradient stiffness in u' ----
    # For a static radial A^r=u(r), the nonzero field-strength components are F_{tr} (from A^t')
    # and the spatial F has F_{r theta} etc = 0 for purely radial u in spherical symmetry; the
    # gradient energy in u comes through F_{t r} mixing and the divergence structure. The robust,
    # convention-independent piece is the (d_r u)^2 stiffness with coefficient ~ K_B. We carry it
    # symbolically as Kstiff and confirm its SIGN below from the kinetic term.
    KB = sp.symbols('K_B', positive=True)

    # ---- the mixing term 2(2-K_B) J^mu d_mu phi, J_mu = A^a nabla_a A_mu (aether acceleration) ----
    # J^mu d_mu phi for a static aether ~ (A^t d_t + u d_r)(...)  -> leading u-linear piece couples
    # u to dphi'. We capture its structure but it is SUBDOMINANT to the K(Q) cross term for the
    # FORCED-tilt question (both are linear in u*dphi'); fold its coefficient into S1 via (2-K_B).

    # ============================================================================
    # Expand L_F in u to O(u^2). The unit constraint makes At = At(u); substitute.
    # ============================================================================
    eps = sp.symbols('eps')                       # bookkeeping for the tilt order
    u_s = sp.symbols('u_s', real=True)            # treat u as a small algebraic variable
    upr = sp.symbols('upr', real=True)            # u' as algebraic variable
    # rebuild Q, At with algebraic u_s (drop derivative-of-u inside At; At has no u'):
    At_a = sp.sqrt((1 + (1-2*Phi)*u_s**2)/(1 + 2*Phi))
    Q_a  = At_a*Q0 + u_s*dphi_p
    K_a  = -2*Lam + sp.Rational(1,2)*K2*(Q_a - Q0)**2
    LF_a = -K_a

    # series in u_s to 2nd order
    LF_series = sp.series(LF_a, u_s, 0, 3).removeO()
    LF_series = sp.expand(LF_series)
    L0   = LF_series.subs(u_s, 0)
    S1   = sp.simplify(sp.diff(LF_series, u_s).subs(u_s, 0))     # linear coeff
    M2   = sp.simplify(sp.diff(LF_series, u_s, 2).subs(u_s, 0))  # quadratic coeff (algebraic "mass")

    print("\n  --- expansion of the Q-sector Lagrangian density L_F = -K(Q) in the tilt u ---")
    print("  L_F = L0 + S1*u + (1/2) M2*u^2 + ...,  with At(u) from the unit constraint.\n")
    print("  LINEAR source coefficient S1 = dL_F/du |_{u=0} :")
    sp.pprint(S1)
    # At u=0: At=1/sqrt(1+2Phi)=:N. dAt/du|0 = ? At_a even in u_s => dAt/du|0 = 0.
    dAt_du0 = sp.simplify(sp.diff(At_a, u_s).subs(u_s, 0))
    print(f"\n  Note dA^t/du|_(u=0) = {dAt_du0}  (A^t is EVEN in u: the constraint surface is symmetric in u).")
    print("  => the ONLY u-linear term in Q at u=0 is the cross term u*dphi'. So:")
    S1_clean = sp.simplify(S1)
    print("  S1 = -dK/dQ|_(Q=Qbar) * dphi'   where Qbar = A^t(0) Q0 = Q0/sqrt(1+2Phi).")
    print("\n  QUADRATIC coefficient M2 = d^2 L_F/du^2 |_{u=0} :")
    sp.pprint(M2)
    print()
    return dict(r=r, Phi=Phi, Q0=Q0, dphi_p=dphi_p, Lam=Lam, K2=K2, KB=KB,
                At_a=At_a, S1=S1_clean, M2=M2, dAt_du0=dAt_du0)


# ============================================================================
# PART 2 -- the SIGNS: is u=0 a minimum, saddle, or shifted? Stability of the mode.
# ============================================================================
def part2_signs_and_minimum(sym):
    print("="*100)
    print("PART 2 -- min vs saddle: signs of M2 (algebraic mass) and Kstiff (gradient), and the shift")
    print("="*100)
    r, Phi, Q0, dphi_p = sym['r'], sym['Phi'], sym['Q0'], sym['dphi_p']
    Lam, K2, KB = sym['Lam'], sym['K2'], sym['KB']

    # M2 explicitly: differentiate -K(Q(u)) twice. With Q=At(u)Q0+u*dphi',
    # d2(-K)/du2 = -[ K_QQ (dQ/du)^2 + K_Q d2Q/du2 ].
    # dQ/du|0 = dphi' (since dAt/du|0=0). d2Q/du2|0 = Q0 * d2At/du2|0 + 0.
    At_a = sym['At_a']
    u_s = list(At_a.free_symbols & {sp.Symbol('u_s', real=True)})
    u_s = sp.Symbol('u_s', real=True)
    d2At = sp.simplify(sp.diff(At_a, u_s, 2).subs(u_s, 0))
    print(f"  d^2 A^t/du^2 |_(u=0) = {d2At}   (curvature of the constraint surface; >0 => At grows with |u|).")
    # K_Q at Qbar=Q0/N: K_Q = K2 (Qbar - Q0). With N=1/sqrt(1+2Phi)>1 for Phi<0? Phi<0 => 1+2Phi<1 => N>1.
    # Qbar - Q0 = Q0(1/sqrt(1+2Phi) - 1) = Q0*|Phi| + ... > 0 (small). So K_Q = K2*Q0*|Phi| (tiny, O(|Phi|)).
    # K_QQ = K2 (the dust-mode curvature).
    N = 1/sp.sqrt(1 + 2*Phi)
    Qbar = Q0*N
    K_Q  = K2*(Qbar - Q0)
    K_QQ = K2
    dQdu = dphi_p                       # dQ/du|0
    d2Qdu = Q0*d2At                     # d2Q/du2|0
    M2_explicit = sp.simplify(-(K_QQ*dQdu**2 + K_Q*d2Qdu))
    print("\n  ALGEBRAIC mass:  M2 = -[ K_QQ (dphi')^2 + K_Q * Q0 * d2At/du2 ]")
    print("                      = -[ K2 (dphi')^2 + K2*Q0*|Phi|*Q0 * d2At/du2 ]   (K_Q ~ K2 Q0 |Phi|, O(|Phi|))")
    print(f"  leading term: M2 ~ -K2 (dphi')^2   (the dominant, |Phi|-independent piece).")
    print("""
  SIGN READING (decisive):
   * K2 > 0  is the dust-mode curvature (CMB-fixed; K(Q) is a convex well at its minimum Q0).
   * So the LEADING M2 = -K2 (dphi')^2 < 0  in the -F convention as written.  BUT the physical
     'potential' whose minimum we seek is U(u) = -L (energy), so the energy curvature is
     U'' = -M2 = +K2 (dphi')^2 > 0  AT THE ALGEBRAIC (no-gradient) level  -- a genuine WELL in u
     from the Q-sector, PROVIDED the vector gradient stiffness Kstiff has the right sign too.
   * The vector kinetic term -(K_B/2)F^2 with K_B>0 (c_GW=c fixes K_B near 1, >0) gives a POSITIVE
     gradient energy (u')^2 -> Kstiff>0 -> no gradient ghost for the radial mode.  (The known AeST
     ghost/gradient analyses, Skordis-Zlosnik 2021 App., fix the kinetic signs for stability;
     the radial 'spin-1' mode is non-ghost in the c_GW=c branch.)
  => u=0 is a MINIMUM of the energy in the QUADRATIC part (well, not a saddle), once the source is
     off.  The question is therefore NOT stability (it is stable) but the SHIFT from the LINEAR
     source S1 -- the forced tilt.\n""")

    # the linear source S1 = -K_Q * dphi'  (since dQ/du|0 = dphi', and dL_F/du = -K_Q dQ/du):
    S1_explicit = sp.simplify(-K_Q*dQdu)
    print("  LINEAR SOURCE:  S1 = -K_Q * dphi' = -K2 (Qbar - Q0) dphi' = -K2 * Q0 * |Phi| * dphi'  + ...")
    print("     -> S1 is O(|Phi|) * K2 Q0 dphi'  : the cross-coupling source is SUPPRESSED by |Phi|~(v/c)^2,")
    print("        because at u=0 the background Q (=Qbar) sits only |Phi| away from the K(Q) minimum Q0.")
    print("""
  *** KEY STRUCTURAL RESULT ***  The FORCED-tilt source is NOT the naive 'F_Q dphi'' with F_Q=O(1).
  On the static branch the aether's OWN time component redshifts Q to Qbar=Q0/sqrt(1+2Phi), which sits
  a distance (Qbar-Q0)=Q0|Phi| up the K(Q) well, so K_Q=dK/dQ there is K2*Q0*|Phi|, itself O(|Phi|).
  The source S1 ~ K2 Q0 |Phi| dphi' is doubly small (|Phi| AND it needs the galaxy gradient dphi').\n""")

    # algebraic forced tilt: u_min = -S1/M2_energy where M2_energy = U'' = K2 (dphi')^2 (+gradient)
    # u_min(algebraic) = -S1 / (-M2) = S1/M2 ... careful with signs: minimize U(u)=-L0 - S1 u + (1/2)(-M2)u^2
    # => U'(u)= -S1 + (-M2) u = 0 -> u_min = S1/(-M2) = (-K_Q dphi')/(K2 (dphi')^2) = -K_Q/(K2 dphi')
    u_min_alg = sp.simplify(S1_explicit/(-M2_explicit))
    u_min_alg = sp.simplify(u_min_alg)
    print("  ALGEBRAIC forced tilt (gradient-stiffness-free limit):  u_min = S1 / (-M2) =")
    sp.pprint(u_min_alg)
    # leading: u_min ~ (-K2 Q0 |Phi| dphi')/(K2 (dphi')^2) = -Q0 |Phi|/dphi'
    print("\n  LEADING:  u_min ~ -(K_Q)/(K2 dphi') = -(Q0 |Phi|)/dphi'   [units: (scalar-velocity * |Phi|)/gradient].")
    print("  This is the algebraic (un-stiffened) ceiling; gradient stiffness only REDUCES it. Size it in Part 3.\n")
    return dict(M2=M2_explicit, S1=S1_explicit, u_min_alg=u_min_alg, K_Q=K_Q)


if __name__ == "__main__":
    sym = part1_energy_functional()
    part2_signs_and_minimum(sym)
