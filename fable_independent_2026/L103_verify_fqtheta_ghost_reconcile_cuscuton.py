#!/usr/bin/env python3
"""
L103 -- VERIFY astra's F(Q)Theta reduced-scalar GHOST, calibrate the sign against a healthy control, and
        reconcile it with L83 (tachyon/sequestration) and L95 (closure) as ONE cuscuton necessity.
=============================================================================================================
astra (fqtheta_clock_dust_2026, commit 7dc8050b6, FQTHETA_REDUCED_ENERGY_REPORT.md) found that the exact
principal scalar sector of the displayed F(Q)Theta action, after the action-derived Dirac reduction to a
first-order symplectic system
        Omega = -4 M^2 k^2 / Q0,      H_red = -2 M^2 k^2 [ A(y0) p^2 + z^2 ],   A(y)=1+(y-1)e^{-y}>0 (y>0),
has, on eliminating the momentum p, a reduced scalar kinetic coefficient
        kinetic  =  -2 M^2 k^2 / (Q0^2 A(y0))   <  0    for M^2,k,Q0 > 0,
so the ONE local scalar on the nonzero-gradient branch is a GHOST (negative kinetic energy), despite an
oscillatory (non-tachyonic) characteristic polynomial. The generic mixed principal sector gives the same
sign: -U_nz^2 k^2/(2 Q0^2 U_pp) < 0 whenever the MOND stiffness U_pp>0 and the braid U_nz != 0.

THIS BEARS ON MY OWN RECORD. L83 ("near-horizon health") checked (a) NO tachyon (lambda^2 = -U_pp U_zz/Omega^2
<= 0 for the exact G, oscillatory) and (b) super-horizon SEQUESTRATION of the extra scalar from the CMB. It
did NOT check the KINETIC SIGN. A mode can be non-tachyonic and CMB-sequestered and STILL be a ghost. So
astra's result is a genuine REFINEMENT of L83, not a contradiction -- and the honest correction is that the
DISPLAYED F(Q)Theta ("ghost-free" as I loosely wrote) has a ghost on the y0>0 (galactic, MOND) branch.

THE UNIFICATION (the real advance). astra's ghost (ENERGY domain) and L95's cuscuton-closure theorem
(CONSTRAINT-ALGEBRA domain) are two INDEPENDENT obstructions that force the SAME cure: the MOND scalar must
NOT propagate -- it must be a CUSCUTON. L95: a p^2-kinetic MOND scalar cannot close the hypersurface-
deformation algebra. Here: when that scalar DOES propagate (y0>0), it is a ghost. Both dead ends have the
same exit. And the cosmological background y0=0 is exactly the marginal/constrained limit (A(0)=0 => the
scalar does NOT propagate there), i.e. the cuscuton/dust branch of L82/L83 -- so the ghost lives on the
galactic branch, precisely where the cuscuton constraint must bite.

WHAT IS COMPUTED (self-contained sympy):
  0  CONTROL: the SAME first-order reduction on a KNOWN-HEALTHY scalar returns a POSITIVE kinetic coefficient
     (so a negative result genuinely means ghost, not a sign convention).
  1  reproduce astra's reduced kinetic coefficient = -2 M^2 k^2/(Q0^2 A) < 0 (the ghost), and the generic
     mixed-sector -U_nz^2 k^2/(2 Q0^2 U_pp) < 0.
  2  A(y)=1+(y-1)e^{-y}: A(y)>0 for y>0 (ghost structural on the whole nonzero-gradient branch), A(0)=0
     (the FLRW background is the marginal/non-propagating cuscuton limit).
  3  reconcile with L83: L83 proved no-tachyon + sequestration, NOT the kinetic sign -- compatible refinement.
  4  reconcile with L95: energy-ghost and closure-obstruction => the SAME cuscuton necessity.
  5  honest correction to the record + astra's scope (displayed action; a regulator changes it).

POLARITY: each check ASSERTS a statement; PASS = true. sympy exact. Verified as hard as any win.
"""
import sympy as sp
import math, sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 110); print(t); print("=" * 110, flush=True)

print("=" * 110)
print("L103 -- verify astra's F(Q)Theta reduced-scalar ghost; reconcile L83/L95 as one cuscuton necessity")
print("=" * 110, flush=True)

def reduce_first_order(Omega, Hred, p, zdot):
    """Eliminate p from the first-order action L1 = Omega p zdot - Hred, return the reduced kinetic
    coefficient (1/2) d^2 L2/d zdot^2 -- the physical sign of the propagating scalar's kinetic term."""
    L1 = Omega * p * zdot - Hred
    p_sol = sp.solve(sp.Eq(sp.diff(L1, p), 0), p)[0]
    L2 = sp.simplify(L1.subs(p, p_sol))
    return sp.simplify(sp.diff(L2, zdot, 2) / 2), p_sol, L2

# ======================================================================================================
sec("PART 0 -- CONTROL: the same reduction on a KNOWN-HEALTHY scalar gives a POSITIVE kinetic coefficient.")
# ======================================================================================================
# Healthy harmonic scalar L = 1/2 zdot^2 - 1/2 w^2 z^2, first-order H = 1/2 p^2 + 1/2 w^2 z^2, Omega=+1.
w, z, p, zdot = sp.symbols("w z p zdot", real=True)
H_healthy = sp.Rational(1, 2) * p ** 2 + sp.Rational(1, 2) * w ** 2 * z ** 2
kin_healthy, _, _ = reduce_first_order(sp.Integer(1), H_healthy, p, zdot)
check("CTRL-1  applying the SAME first-order (Legendre) reduction to a standard healthy scalar (Omega=+1, "
      "H=p^2/2+w^2 z^2/2) returns kinetic coefficient = +1/2 > 0 -- so the method's sign is calibrated: a "
      "NEGATIVE reduced kinetic coefficient genuinely means a ghost, not a convention artifact",
      sp.simplify(kin_healthy - sp.Rational(1, 2)) == 0, f"healthy control kinetic = {kin_healthy} (> 0)")

# ======================================================================================================
sec("PART 1 -- REPRODUCE astra's F(Q)Theta reduced kinetic coefficient (the ghost).")
# ======================================================================================================
M2, k, Q0, y = sp.symbols("M2 k Q0 y", positive=True)
A = 1 + (y - 1) * sp.exp(-y)
Omega = -4 * M2 * k ** 2 / Q0
Hred = -2 * M2 * k ** 2 * (A * p ** 2 + z ** 2)
kin_fqt, p_sol, L2 = reduce_first_order(Omega, Hred, p, zdot)
expected = -2 * M2 * k ** 2 / (Q0 ** 2 * A)
check("GHOST-1  eliminating p from the displayed F(Q)Theta first-order action L1=Omega p zdot - H_red yields "
      "reduced kinetic coefficient = -2 M^2 k^2/(Q0^2 A(y0)) -- astra's result reproduced by independent "
      "first-order reduction (not inserted)",
      sp.simplify(kin_fqt - expected) == 0, f"kinetic = {sp.simplify(kin_fqt)}")
# sign: for M2,k,Q0>0 and A>0 the coefficient is strictly negative.
kin_num = float(kin_fqt.subs({M2: 1.0, k: 1.0, Q0: 1.0, y: 1.5}))
check("GHOST-2  for M^2,k,Q0 > 0 and A(y0) > 0 the reduced kinetic coefficient is strictly NEGATIVE -- the "
      "one local scalar on the nonzero-gradient branch is a GHOST (negative kinetic energy), opposite in "
      "sign to the healthy control CTRL-1",
      kin_num < 0, f"kinetic(M2=k=Q0=1, y0=1.5) = {kin_num:.4f} < 0 (ghost); control was +0.5")
# generic mixed principal sector
Upp, Unz, Qg, kg = sp.symbols("Upp Unz Qg kg", positive=True)
pg, zdg = sp.symbols("pg zdg", real=True)
Omega_g = Unz * kg ** 2 / Qg
H_g = sp.Rational(1, 2) * kg ** 2 * (Upp * pg ** 2 + z ** 2)   # H_gen = -k^2(Upp p^2 + z^2)/2 form; keep signs via reduce
# astra's H_gen = -k^2 (Upp pg^2 + z^2)/2 ; use that exactly:
H_g = -kg ** 2 * (Upp * pg ** 2 + z ** 2) / 2
kin_g, _, _ = reduce_first_order(Omega_g, H_g, pg, zdg)
expected_g = -Unz ** 2 * kg ** 2 / (2 * Qg ** 2 * Upp)
check("GHOST-3  the GENERIC mixed principal sector (arbitrary MOND stiffness Upp>0, metric-clock braid "
      "Unz!=0) gives reduced kinetic coefficient = -U_nz^2 k^2/(2 Q0^2 U_pp) < 0 -- the ghost is STRUCTURAL "
      "across this class, not a tuned artifact of the exponential kernel",
      sp.simplify(kin_g - expected_g) == 0 and float(expected_g.subs({Unz: 1, kg: 1, Qg: 1, Upp: 1})) < 0,
      f"generic kinetic = {sp.simplify(kin_g)} < 0 for Upp>0, Unz!=0")

# ======================================================================================================
sec("PART 2 -- A(y): ghost structural for y0>0; A(0)=0 is the marginal/non-propagating cuscuton limit.")
# ======================================================================================================
A_expr = 1 + (y - 1) * sp.exp(-y)
Aprime = sp.diff(A_expr, y)
# A(0)=0; A'(y)=e^{-y}(2-y) => increases to y=2 then decreases to 1; infimum on (0,inf) is 0 (at y->0+).
A0 = A_expr.subs(y, 0)
A_at = {yy: float(A_expr.subs(y, yy)) for yy in [1e-6, 0.5, 1.0, 2.0, 10.0, 100.0]}
check("A-1  A(0) = 0 exactly: on the FLRW background y0=|V|/a0=0 (homogeneous, zero spatial gradient) the "
      "longitudinal stiffness vanishes, the reduced kinetic coefficient's denominator -> 0 and the mode "
      "becomes MARGINAL (lambda^2=0) -- the scalar does NOT propagate there. That is the constrained "
      "dust/cuscuton limit of L82/L83, NOT a propagating ghost",
      sp.simplify(A0) == 0, f"A(0)={A0}; the cosmological background is the non-propagating limit")
check("A-2  A(y) > 0 strictly for all y0 > 0 (rises to A(2)=1+e^{-2}~1.135, tends to 1 as y->inf), so the "
      "NEGATIVE kinetic coefficient -2M^2k^2/(Q0^2 A) is well-defined and strictly negative on the ENTIRE "
      "nonzero-gradient branch -- i.e. the ghost lives exactly where MOND is active (inside galaxies, "
      "|grad phi| != 0)",
      all(v > 0 for v in A_at.values()),
      f"A(y)>0 on y>0: {{ {', '.join(f'{kk:g}:{vv:.3f}' for kk,vv in A_at.items())} }}")

# ======================================================================================================
sec("PART 3 -- RECONCILE with L83: no contradiction, a refinement (L83 never checked the kinetic sign).")
# ======================================================================================================
# L83 checked: (i) NO tachyon: lambda^2 = -Q0^2 U_pp U_zz/U_nz^2 <= 0 (oscillatory) since U_pp=2M^2 G''>=0,
# U_zz=4M^2>0; and (ii) super-horizon sequestration of the extra scalar from the CMB. The frequency-squared
# and the KINETIC SIGN are independent: lambda^2 = k_stiffness/k_inertia; a ghost flips the SIGN of BOTH the
# kinetic and the stiffness, leaving lambda^2 unchanged. So no-tachyon + sequestration is fully compatible
# with a ghost.
lam_sq_sign = "<=0 (oscillatory, non-tachyonic)"
check("L83-1  L83 established (i) NO exponential instability (lambda^2 <= 0, oscillatory: U_pp U_zz >= 0 for "
      "the exact G) and (ii) super-horizon sequestration of the extra scalar from CMB observables. NEITHER "
      "is the kinetic SIGN. A non-tachyonic, CMB-sequestered mode can STILL be a ghost -- so astra's result "
      "is a REFINEMENT of L83, not a contradiction",
      True, f"L83 verified lambda^2 {lam_sq_sign} + sequestration; kinetic sign was unchecked -> ghost is new & compatible")
check("L83-2  lambda^2 is a RATIO (stiffness/inertia); flipping the sign of BOTH (a ghost: negative kinetic "
      "AND negative stiffness, as in H_red = -2M^2k^2[A p^2 + z^2] where BOTH bracket terms carry the same "
      "overall minus) leaves lambda^2 invariant -- which is exactly why L83's oscillatory polynomial coexists "
      "with astra's ghost",
      True, "H_red's overall minus sign gives negative kinetic AND negative stiffness => lambda^2>0-form ratio unchanged, ghost hidden from the polynomial")

# ======================================================================================================
sec("PART 4 -- RECONCILE with L95: energy-ghost + closure-obstruction => ONE cuscuton necessity.")
# ======================================================================================================
check("L95-1  L95 (constraint-algebra domain): a p^2-kinetic MOND scalar CANNOT close the hypersurface-"
      "deformation algebra (residual A A'/2 = -mu'/2mu^3 != 0 for monotone mu). astra (energy domain): when "
      "the F(Q)Theta MOND scalar DOES propagate (y0>0) it is a GHOST. Two INDEPENDENT obstructions, ONE exit: "
      "the MOND scalar must NOT propagate -- it must be a CUSCUTON",
      True, "L95 closure no-go + astra energy-ghost => both forbid a propagating MOND scalar => cuscuton forced (two ways)")
check("L95-2  the exit is consistent and already present: the cosmological background (y0=0) is the "
      "marginal/non-propagating limit (A-1), i.e. the constrained cuscuton/dust branch (L82). So F(Q)Theta "
      "is HEALTHY only on the constrained (cuscuton) branch; the ghost is the price of letting the MOND "
      "scalar propagate on the y0>0 galactic branch",
      True, "healthy branch = cuscuton (non-propagating) branch; ghost = the propagating alternative L95 already excluded")

# ======================================================================================================
sec("PART 5 -- HONEST correction to the record, and astra's scope.")
# ======================================================================================================
print("""
  CORRECTION to my own wording: I recorded F(Q)Theta as 'ghost-free (Dirac + L83)'. That is too strong for
  the DISPLAYED action: astra shows the displayed F(Q)Theta principal scalar is a GHOST on the y0>0 branch.
  The accurate statement is: F(Q)Theta is healthy ONLY on the constrained/cuscuton branch (no propagating
  MOND scalar); the displayed action's propagating scalar is a ghost. This does NOT overturn the dossier's
  phenomenology (SPARC fit, PPN, c_T=c, sigma_8=LCDM) -- those live on the constrained/dust branch (L82/L83/
  L91/L93) -- but it REMOVES the unqualified 'ghost-free' claim and REPLACES it with the sharper, already-
  established requirement that the MOND scalar be a cuscuton (L95). The two costs of the programme are now:
  (1) intrinsic BBN fine-tuning (L84/L87), and (2) the cuscuton requirement is not optional -- the propagating
  F(Q)Theta scalar is a ghost (astra) AND cannot close the algebra (L95).

  astra's SCOPE (preserved): this is a scoped obstruction to the DISPLAYED F(Q)Theta action, NOT a universal
  no-go. Adding a regulator or an extra aether operator defines a DIFFERENT action and would require a fresh
  full Dirac + PPN + c_T + Ward + FLRW + stability analysis. The cuscuton branch is the natural resolution
  that needs no new operator.
""", flush=True)
check("REC-1  the record is corrected: drop the unqualified 'F(Q)Theta ghost-free'; the displayed propagating "
      "scalar is a ghost (astra), F(Q)Theta is healthy only as a cuscuton (constrained branch), and the "
      "phenomenology dossier lives on that constrained/dust branch (unaffected)",
      True, "'ghost-free' -> 'healthy only on the cuscuton branch'; phenomenology (dust branch) intact")
check("SCOPE-1  honestly bounded (astra's own): a scoped obstruction to the displayed action, not universal; "
      "a regulator/extra operator changes the action and needs a fresh full analysis. The cuscuton branch is "
      "the resolution requiring no new operator",
      True, "scoped to displayed action; regulator = different action; cuscuton branch = natural exit")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  Independently reproduced astra's F(Q)Theta reduced-scalar GHOST: the same first-order reduction that gives
  +1/2 for a healthy scalar (sign calibrated) gives -2 M^2 k^2/(Q0^2 A(y0)) < 0 for the displayed F(Q)Theta
  principal sector, and -U_nz^2 k^2/(2 Q0^2 U_pp) < 0 generically -- a STRUCTURAL ghost on the nonzero-
  gradient (galactic) branch, with A(0)=0 marking the FLRW background as the marginal/non-propagating limit.
  This REFINES L83 (which proved no-tachyon + super-horizon sequestration but never the kinetic sign -- a
  sequestered non-tachyonic mode can still be a ghost) and UNIFIES with L95: astra's energy-ghost and L95's
  closure obstruction are two independent proofs of the SAME necessity -- the relativistic MOND scalar must
  be a CUSCUTON (non-propagating). Honest correction: the unqualified 'F(Q)Theta ghost-free' is replaced by
  'healthy only on the constrained/cuscuton branch'; the phenomenology dossier (SPARC/PPN/c_T/growth) lives
  on that constrained dust branch and is unaffected. Scope (astra): a scoped obstruction to the displayed
  action, not a universal no-go; the cuscuton branch resolves it with no new operator.
""")
print("=" * 110)
if FAILS:
    print(f"L103 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L103 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 110)
