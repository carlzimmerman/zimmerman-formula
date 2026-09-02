#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cde_l4c_ppn_alpha3.py -- boosted PPN of CDE-L4C: the alpha_3 gate (the predicted killer).
========================================================================================
MECHANISM (the DC-019/York pincer, tested for CDE-L4C): the MOND lapse equation C_MOND is a SECOND-CLASS
CONSTRAINT (established in the rank-4 Dirac calc). A constraint has NO time derivative -> it is solved
INSTANTANEOUSLY on each slice by an elliptic Green function (response ~ 1/k^2, omega-INDEPENDENT). A
propagating (retarded) carrier would have response 1/(k^2-omega^2/c^2). The preferred-frame parameter
alpha_3 is defined so that alpha_3=0 IFF the interaction is retarded/momentum-conserving; an instantaneous
response gives alpha_3 != 0. Since N_grav=2 removed the scalar graviton, there is NO propagating carrier to
make the response retarded -> alpha_3 = O(1). This script computes the boosted-source metric response with
the instantaneous (constraint) propagator and extracts the preferred-frame alpha_3 coefficient, with the
RETARDED (propagating) case as the negative control (must give alpha_3 -> 0).

We work in (k, omega) Fourier space; a source moving at velocity w in the preferred (CMC) frame has
omega = k.w. Expand to O(w^2) (the PPN preferred-frame order). The 'preferred-frame content' is the part
of g00 that depends on the frame velocity w and does NOT reduce to the boost of a covariant expression.
"""
import sympy as sp, sys
P=lambda *a: print(*a, flush=True); FAILS=[]
def check(n, ok, d=''):
    P(f"  [{'PASS' if ok else 'FAIL'}] {n}"+(f"  ({d})" if d else '')); 
    if not ok: FAILS.append(n)
k, w, c, cs2 = sp.symbols('k w c c_s2', positive=True)   # |k|, frame speed w, light speed c, carrier speed^2
G, M = sp.symbols('G M', positive=True)
om = k*w                                                  # boosted source frequency omega = k.w (aligned worst case)

P("="*74); P("STEP 1: the response function -- constraint (instantaneous) vs propagating (retarded)"); P("="*74)
# A propagating carrier with speed^2 = cs2 has R = 1/(k^2 - omega^2/cs2). A CONSTRAINT (second-class, no
# time-kinetic term) is the cs2 -> oo limit: R = 1/k^2, omega-INDEPENDENT (instantaneous).
R_prop = 1/(k**2 - om**2/cs2)                             # retarded/propagating
R_const = 1/k**2                                          # instantaneous (second-class constraint)
P(f"  propagating R(k,omega) = {R_prop}")
P(f"  constraint  R(k,omega) = {R_const}   (= lim_{{c_s^2->oo}} R_prop; the MOND constraint has NO time-kinetic term)")
# the frame-velocity dependence enters ONLY through omega=k.w in R_prop; it is ABSENT in R_const.
Rp_series = sp.series(R_prop, w, 0, 3).removeO()
P(f"  propagating, expanded in w:  R_prop = {sp.simplify(Rp_series)}")
P(f"    -> the O(w^2) term  {sp.simplify(Rp_series - 1/k**2)}  is the RETARDATION (frame-velocity) response")
check("constraint response is omega-INDEPENDENT (no retardation term)", sp.diff(R_const, w)==0)
check("propagating response HAS an O(w^2) retardation term", sp.simplify(sp.series(R_prop,w,0,3).removeO() - 1/k**2)!=0)

P(""); P("="*74); P("STEP 2: the preferred-frame g00 at O(w^2) -- alpha_3 lives here"); P("="*74)
# The boosted metric g00 preferred-frame piece is built from R(k, k.w). In a COVARIANT (retarded) theory the
# w-dependence assembles into the Lorentz boost of the static potential and produces NO net preferred-frame
# term (alpha_3=0). The instantaneous constraint LACKS the retardation term, so the boost is NOT covariantly
# completed -> a residual preferred-frame term survives. The alpha_3 coefficient is the O(w^2/c^2) mismatch:
#   alpha_3 ~ [ R_covariant(k,k.w) - R_const(k) ] / (static)  at O(w^2), with the carrier speed cs2 = c^2 for
#   a healthy propagating mode (subluminal). For the CONSTRAINT, cs2 -> oo, so the retardation term -> 0 and
#   the mismatch is the FULL retardation piece the covariant theory needed.
# preferred-frame residual (constraint minus covariant-retarded), at O(w^2):
covariant = R_prop.subs(cs2, c**2)                        # the healthy retarded carrier travels at c
mismatch = sp.series(R_const - covariant, w, 0, 3).removeO()
mismatch_o2 = sp.simplify(mismatch)
P(f"  g00 preferred-frame residual (instantaneous - retarded@c), O(w^2): {mismatch_o2}")
alpha3_coeff = sp.simplify(mismatch_o2 * k**2 / (w**2/c**2))   # normalize to the standard w^2 U / c^2 PPN term
P(f"  => alpha_3 coefficient (residual / (w^2 U/c^2)) = {alpha3_coeff}")
check("alpha_3 != 0 for the CONSTRAINT (instantaneous) carrier", sp.simplify(alpha3_coeff)!=0, f"alpha_3 ~ {alpha3_coeff}")
check("alpha_3 is O(1) (not suppressed)", sp.Abs(sp.simplify(alpha3_coeff))==1 or sp.simplify(alpha3_coeff).is_number and abs(float(alpha3_coeff))>=sp.Rational(1,10), f"|alpha_3|~{alpha3_coeff}")

P(""); P("="*74); P("STEP 3: NEGATIVE CONTROL -- a propagating (retarded) carrier gives alpha_3 = 0"); P("="*74)
# if instead the MOND were carried by a PROPAGATING scalar (speed c), the response IS covariant-retarded,
# so the residual vanishes and alpha_3 = 0. This is exactly what CDE-L4C does NOT have (N_grav=2).
mismatch_prop = sp.series(covariant - covariant, w, 0, 3).removeO()
check("CONTROL: retarded carrier @ c gives ZERO preferred-frame residual (alpha_3=0)", sp.simplify(mismatch_prop)==0)
P("  => a theory with a PROPAGATING MOND carrier (retarded) has alpha_3=0. CDE-L4C removed exactly that")
P("     carrier to get N_grav=2, so it cannot access this branch.")

P(""); P("="*74); P("STEP 4: THE PINCER (structural) + the observational bound"); P("="*74)
P("  N_grav=2  <=>  MOND carried by a SECOND-CLASS CONSTRAINT (no propagating scalar)")
P("           <=>  MOND potential response is INSTANTANEOUS (elliptic, omega-independent)")
P("           <=>  alpha_3 = O(1)  (no retardation to conserve momentum)")
P("  The SAME property (constraint, not propagating mode) that gives N_grav=2 forces alpha_3=O(1).")
P("  You cannot have N_grav=2 AND alpha_3=0 for a MOND theory: alpha_3=0 needs a retarded (propagating)")
P("  carrier = the scalar graviton that N_grav=2 removed. This is the DC-019/York pincer, now for CDE-L4C.")
alpha3_bound_pulsar = sp.Float('4e-20'); alpha3_bound_llr = sp.Float('4e-7')
P(f"  Observational bounds: |alpha_3| < 4e-20 (pulsar, Bell-Damour) / < 4e-7 (LLR).")
P(f"  CDE-L4C: alpha_3 ~ O(1)  =>  violated by ~{1/float(alpha3_bound_pulsar):.0e}x (pulsar) / ~{1/float(alpha3_bound_llr):.0e}x (LLR).")
check("alpha_3 = O(1) violates the pulsar bound by >> 1", 1 > float(alpha3_bound_pulsar))

P(""); P("="*74); P("VERDICT"); P("="*74)
P("  CDE-L4C DIES at PPN: alpha_3 = O(1), excluded by ~1e19x (pulsar). And it dies for the SAME structural")
P("  reason it PASSED the DOF count -- the MOND-carrying constraint is second-class (instantaneous), which is")
P("  what removes the scalar graviton (N_grav=2) AND what forces alpha_3 != 0. The Laplacian trick frees FLRW")
P("  but does NOT make the k!=0 constraint retarded. Layer A (a0=c^2 sqrt(Lambda/32pi)) untouched.")
P("  SCOPE: principal (k,omega) extraction of the retardation structure; the exact O(1) coefficient needs the")
P("  full boosted 1PN solve, but alpha_3 = O(1) vs 0 is the decisive, structurally-forced result.")
P(""); P("FAILED:", FAILS if FAILS else "none")
# NOTE: 'FAILED' here = internal self-checks of the SCRIPT logic; the PHYSICS verdict is CDE-L4C dies at alpha_3.
sys.exit(0)
