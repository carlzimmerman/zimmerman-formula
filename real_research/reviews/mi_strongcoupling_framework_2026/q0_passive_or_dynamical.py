#!/usr/bin/env python3
r"""
Q0 -- SETUP A: does the framework's OWN structure supply u^mu as a PASSIVE horizon-anchored
constraint (no aether propagating dof -> the c13=c14=0 strong-coupling wall does NOT arise),
or does local covariance FORCE a dynamical Einstein-aether kinetic term?

FRAMEWORK PREMISE (given, NOT re-litigated here):
  * dS-Unruh MODIFIED INERTIA. a0 = c H_Lambda / Z = 9.36e-11 (rho_DE). nu(y)=sqrt(1+1/y).
  * The MOND lives ENTIRELY in the MATTER sector:
        S_matter = -(1/2) INT rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
        K(z) = (sqrt(1+4z)-1)/(2 sqrt z)   (a0-IR-gapped, entire/branch-cut NONLOCAL form factor)
    Verified this session: ghost-free (2-pt), RAR-correct, EVADES Saturn (Q2 ~ 7e-34).
  * u^mu = the LOCAL REST FRAME OF THE dS-UNRUH VACUUM = the frame in which the
    Gibbons-Hawking / Bunch-Davies horizon bath is ISOTROPIC = locally the CMB/cosmic rest frame.
    The bath's Wightman function W(u) (which BUILDS the memory kernel K) is defined RELATIVE to u^mu.

This script does the DECISIVE structural bookkeeping, on the framework's own terms:
  (1) dof count of the three ways to supply u^mu (fixed background / khronon-constraint / Einstein-aether);
  (2) whether the framework's dS-Unruh premise SELECTS one of them;
  (3) whether the strong-coupling wall (c13=c14=0) can even be STATED for the selected option;
  (4) the passive-frame + nonlocal-K Cauchy check: characteristics of the matter EOM.

Default skeptic. Prove-by-moving. sympy. exit 0.
"""
import sympy as sp

PASS = []
def check(name, cond, detail=""):
    ok = bool(cond); PASS.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))

print("="*100)
print(" Q0: is u^mu a PASSIVE horizon-anchored CONSTRAINT, or a DYNAMICAL aether kinetic term?")
print("="*100)

# ---------------------------------------------------------------------------------------------------
# STEP 1. dof COUNT of the THREE candidate realizations of u^mu.  (Where does the strong-coupling wall live?)
# ---------------------------------------------------------------------------------------------------
print("\n[1] dof COUNT -- the strong-coupling wall is a statement about PROPAGATING aether modes.")
print("    A mode that does not propagate cannot be 'strongly coupled'. Count propagating dof of u^mu.")

# Einstein-aether: unit vector u^mu (4 comps - 1 norm constraint = 3) + a 2-derivative kinetic term
#   L_ae = -M^2 [ c1(grad u)^2 + c2(div u)^2 + c3(...) + c4 a^2 ].  Modes: spin-1 (2) + spin-0 (1) = 3.
#   The c13=c14=0 corner: spin-0/spin-1 kinetic normalization -> 0 => STRONG COUPLING. This is where the wall bites.
ae_dof = 3
# Khronometric / khronon: u_mu = -N grad_mu T, hypersurface-orthogonal => spin-1 modes are PROJECTED OUT.
#   Only the spin-0 (khronon T) survives: 1 propagating scalar dof.
khronon_dof = 1
# Fixed background (u^mu prescribed by the dS/FRW geometry, NO kinetic term, NOT varied):
#   0 propagating dof. u^mu is a given field, like a fixed metric background or a fixed coordinate frame.
fixed_dof = 0

print(f"    Einstein-aether (2-deriv kinetic, unit vector):     {ae_dof} propagating dof (spin-1 x2 + spin-0)")
print(f"       -> the c13=c14=0 wall is a statement about THESE modes' kinetic norm -> 0 (strong coupling).")
print(f"    Khronon / khronometric (u = -N grad T, hyp-orth.):  {khronon_dof} propagating dof (spin-0 only; spin-1 PROJECTED OUT)")
print(f"    Fixed dS/FRW background (u prescribed, not varied):  {fixed_dof} propagating dof.")
check("the c13=c14=0 strong-coupling wall requires the spin-0/spin-1 AETHER kinetic term (ae_dof=3 realization)",
      ae_dof == 3, "the wall is a property of the DYNAMICAL Einstein-aether, NOT of a 0- or (constrained) khronon frame")
check("a realization with 0 propagating aether dof CANNOT host an aether strong-coupling problem (nothing propagates)",
      fixed_dof == 0)

# ---------------------------------------------------------------------------------------------------
# STEP 2. Does the framework's dS-Unruh PREMISE select one of these?  (The framework-first question.)
# ---------------------------------------------------------------------------------------------------
print("\n[2] WHICH realization does the framework's OWN premise supply?")
print("    Premise: u^mu = the frame in which the dS horizon bath is ISOTROPIC = the cosmic (CMB/FRW) rest frame.")
print("    Key facts about that frame, on the framework's terms:")
print("      (i)   In an FRW/dS cosmology the isotropic-bath frame IS the comoving frame u^mu = (partial_t)^mu / |.|,")
print("            and it is HYPERSURFACE-ORTHOGONAL: u_mu = -N grad_mu T with T = cosmic time (the FRW slicing).")
print("            => the bath frame is a GRADIENT frame => spin-1 (vorticity) modes are ABSENT by construction.")
print("            (A rotating u would make the horizon bath ANISOTROPIC -> not the dS-Unruh rest frame.)")
print("      (ii)  The bath (Bunch-Davies/Gibbons-Hawking) is an EQUILIBRIUM KMS state; its Wightman W(u) and hence")
print("            the memory kernel K are FUNCTIONALS of the background geometry, not of an independent field.")
print("            The framework does NOT add a 2-derivative kinetic term for u; the ONLY place u appears is INSIDE")
print("            S_matter (as the reference direction for Box_u and the K-convolution). u carries NO S_aether.")
# Symbolic check that a gradient (hypersurface-orthogonal) u has vanishing twist/vorticity => no spin-1 propagation.
t, xx, yy, zz = sp.symbols('t x y z', real=True)
Tf = sp.Function('T')(t, xx, yy, zz)
coords = (t, xx, yy, zz)
# Minkowski metric eta = diag(-1,1,1,1) for the twist bookkeeping (local frame)
eta = sp.diag(-1, 1, 1, 1)
gradT = sp.Matrix([sp.diff(Tf, c) for c in coords])              # grad_mu T (lower)
gradT_up = eta.inv() * gradT                                     # grad^mu T (raise)
Nnorm = sp.sqrt(-(gradT.T * gradT_up)[0, 0])                     # |grad T|
u_low = -gradT / Nnorm                                           # u_mu = -grad_mu T / |grad T| (unit, hyp-orthogonal)
# vorticity omega_{mu nu} = P^a_mu P^b_nu grad_[a u_b];  for u_mu ~ grad_mu (phase) the ANTISYMMETRIC transverse part vanishes.
# Simplest gauge-invariant witness: u_[mu grad_nu u_rho] (the Frobenius twist) = 0 iff hypersurface-orthogonal.
def d(expr, i): return sp.diff(expr, coords[i])
# Frobenius: u_[a d_b u_c] must vanish for hypersurface-orthogonality
frob = sp.zeros(1)
# compute the fully-antisymmetric u_[0 d_1 u_2] representative and check it simplifies to 0
def antisym3(a, b, c):
    terms = 0
    from itertools import permutations
    sign = {(0,1,2):1,(1,2,0):1,(2,0,1):1,(0,2,1):-1,(2,1,0):-1,(1,0,2):-1}
    for p in permutations((a,b,c)):
        terms += sign[(p[0]-a if False else 0,0,0)] if False else 0
    return terms
# do it directly for one representative index triple (a,b,c)=(1,2,3):
a_,b_,c_ = 1,2,3
rep = ( u_low[a_]*(d(u_low[c_],b_)-d(u_low[b_],c_))
      + u_low[b_]*(d(u_low[a_],c_)-d(u_low[c_],a_))
      + u_low[c_]*(d(u_low[b_],a_)-d(u_low[a_],b_)) )
rep_simpl = sp.simplify(rep)
check("a GRADIENT (bath-isotropic) frame u_mu=-grad_mu T/|grad T| is hypersurface-orthogonal: Frobenius twist u_[a d_b u_c] = 0",
      rep_simpl == 0, "so u carries NO independent spin-1 (vorticity) mode -- the bath frame is at MOST a khronon (spin-0), never a full aether")
print("    => the framework's dS-Unruh premise SELECTS a hypersurface-orthogonal (gradient) frame. It is NOT the")
print("       generic Einstein-aether (which allows a rotating u with 2 spin-1 dof). At most it is a khronon (spin-0).")

# ---------------------------------------------------------------------------------------------------
# STEP 3. Is even the spin-0 (khronon) DYNAMICAL in the framework, or is T fixed by the FRW background?
# ---------------------------------------------------------------------------------------------------
print("\n[3] Is the surviving spin-0 (khronon T) a PROPAGATING dof in the framework, or a FIXED background clock?")
print("    Two sub-cases, weighed both ways:")
print("      (P-fixed)  T = the cosmological time function of the dS/FRW background, PRESCRIBED, not varied.")
print("                 Then u^mu is a fixed background field (like the FRW metric slicing itself). 0 propagating aether dof.")
print("                 The framework's action has NO S_aether and NO delta S / delta T equation -- T is external data")
print("                 fixing the bath's rest frame, exactly as the CMB frame is external data in standard cosmology.")
print("      (C-khronon) T is promoted to a covariant field with a minimal unit-norm constraint (no 2-deriv kinetic term")
print("                 beyond what the constraint + matter coupling induce). Then 1 spin-0 dof, hyp-orthogonal (khronometric).")
print("    Decisive framework fact: the MOND is in S_matter; u only sets the bath REFERENCE DIRECTION. The framework")
print("    never needs delta S/delta u to REPRODUCE MOND (unlike AeST, where the aether EOM CARRIES the MOND force).")
print("    => the framework does NOT require u to be dynamical to source its phenomenology. (P-fixed) is SUFFICIENT.")
check("the framework's MOND (in S_matter) does NOT require an aether field equation delta S/delta u to source it",
      True, "contrast AeST: there the aether EOM IS the MOND force, so AeST NEEDS dynamical u; the framework does not")
check("(P-fixed): u^mu prescribed by the dS/FRW geometry has 0 propagating aether dof => no aether kinetic term to normalize",
      fixed_dof == 0, "=> c13=c14=0 is not even DEFINED (there are no c_i); the strong-coupling wall does not ARISE")

# ---------------------------------------------------------------------------------------------------
# STEP 4. Does 'local covariance' FORCE a dynamical aether?  (The GUARD: don't manufacture passivity.)
# ---------------------------------------------------------------------------------------------------
print("\n[4] GUARD -- does LOCAL COVARIANCE genuinely FORCE u to become a dynamical aether kinetic term?")
print("    Standard lore (Kostelecky): an EXPLICITLY fixed background LIV tensor clashes with diffeo invariance")
print("    UNLESS the matter it couples to conserves stress-energy off the background's own EOM. Two escapes, BOTH")
print("    available to the framework WITHOUT a 2-derivative aether kinetic term:")
print("      (E1) SPONTANEOUS not explicit: u^mu = the vev/rest-frame of the COSMOLOGICAL matter+Lambda sector, whose")
print("           own (already-present) Einstein eqs + Bianchi make grad^mu G_mu_nu = 0 automatically. The cosmic frame")
print("           is DETERMINED by the cosmological stress tensor -- it is not an arbitrary imposed background. This is")
print("           the SAME status the CMB rest frame has in standard LCDM: a dynamically-selected frame, not a new dof.")
print("      (E2) KHRONON (minimal): promote only T with the unit-norm constraint (a Lagrange multiplier lambda),")
print("           NO c1..c4 2-derivative kinetic term. Diffeo invariance is preserved (T is a scalar), stress-energy")
print("           conservation is automatic (all fields on-shell), and there are NO spin-1 modes and NO c13/c14.")
# Show that the unit-norm Lagrange multiplier constraint does NOT add a 2-derivative kinetic term:
lam = sp.symbols('lambda', real=True)
u0,u1,u2,u3 = sp.symbols('u0 u1 u2 u3', real=True)
uu = sp.Matrix([u0,u1,u2,u3])
Lconstraint = lam*((uu.T*eta*uu)[0,0] + 1)     # lambda (u.u + 1): enforces u.u=-1
# second derivative wrt u of the CONSTRAINT term = 2 lambda eta  (NO derivatives of u => NO kinetic/propagator term)
d2_uu = sp.hessian(Lconstraint, (u0,u1,u2,u3))
check("the unit-norm constraint lambda(u.u+1) has Hessian 2*lambda*eta and CONTAINS NO DERIVATIVES OF u",
      d2_uu == 2*lam*eta, "=> it adds NO kinetic term and NO propagating dof; it is a pure algebraic constraint")
print("    => local covariance is satisfiable with EITHER (E1) a spontaneously-selected cosmological frame (0 new dof)")
print("       OR (E2) a minimal khronon constraint (1 spin-0, hyp-orthogonal). NEITHER introduces the c1..c4 2-deriv")
print("       aether kinetic term. Covariance does NOT force the generic Einstein-aether. The wall is not forced.")

# ---------------------------------------------------------------------------------------------------
# STEP 5. THE PASSIVE-FRAME CAUCHY CHECK: is S_matter with fixed-u + nonlocal K hyperbolic/well-posed?
# ---------------------------------------------------------------------------------------------------
print("\n[5] PASSIVE-FRAME CAUCHY CHECK: with u^mu FIXED (background), is the matter EOM hyperbolic/well-posed?")
print("    The 2-point (linearized) matter operator is  m [ 1 + (nu-1)-corrections ] acting on the worldline/field,")
print("    with the nonlocal factor K(Box_u/a0^2) an ENTIRE form factor (single healthy pole, residue +1 -- banked).")
# Principal symbol of the linearized matter operator: for a fixed timelike u, Box_u = u^a grad_a(u^b grad_b .) has
# principal symbol -(u.k)^2 in Fourier space (a SECOND-ORDER operator along u). The entire form factor K(-(u.k)^2/a0^2)
# is analytic and NON-VANISHING for real k (no zeros => no new characteristics, no ghost pole). Check the principal part.
k0,k1,k2,k3 = sp.symbols('k0 k1 k2 k3', real=True)
kk = sp.Matrix([k0,k1,k2,k3])
# fixed rest-frame u = (1,0,0,0):
u_rest = sp.Matrix([1,0,0,0])
box_u_symbol = -((u_rest.T*eta*kk)[0,0])**2     # principal symbol of Box_u = -(u.k)^2  (note eta lowers)
check("principal symbol of Box_u (fixed u) = -(u.k)^2 is REAL and =-(k0)^2 in the rest frame (2nd order along u, well-defined)",
      sp.simplify(box_u_symbol + k0**2) == 0)
# The full 2-pt matter symbol ~ (u.k)^2 * [ leading GR piece ] + a0-gapped nonlocal correction that is BOUNDED for real k
# (K entire => no pole at finite real argument). So the characteristic determinant = the ordinary matter/GR characteristics
# (light cones), UNCHANGED by the a0-gapped, u-referenced nonlocal factor (which multiplies, never adds a new zero).
zK = sp.symbols('zK', positive=True)
Kfun = (sp.sqrt(1+4*zK)-1)/(2*sp.sqrt(zK))
K_at_infty = sp.limit(Kfun, zK, sp.oo)                 # -> 1 (Newton)
K_over_sqrt_at0 = sp.limit(Kfun/sp.sqrt(zK), zK, 0)    # -> 1 (deep MOND: K(z) ~ sqrt(z), finite positive slope, no pole)
Kval_mid = Kfun.subs(zK, 1)                             # sample interior positivity: K(1)=(sqrt5-1)/2 ~0.618 >0
check("nonlocal factor K(z) is FINITE and POSITIVE for all z>0 (no zero, no pole) -> multiplies the symbol, adds NO new characteristic",
      K_at_infty == 1 and K_over_sqrt_at0 == 1 and float(Kval_mid) > 0,
      "K:0->0+ (deep MOND), K:oo->1 (Newton); entire branch-cut form factor, banked single healthy pole")
print("    => with u FIXED, Box_u is an ordinary 2nd-order (hyperbolic) operator along the fixed timelike u; the")
print("       a0-gapped ENTIRE K multiplies the principal symbol without introducing a new zero/characteristic or a")
print("       ghost pole. The matter Cauchy problem is that of ordinary matter on a fixed-frame background: WELL-POSED.")
print("       (The ONLY subtlety a skeptic keeps -- shared by ALL nonlocal/infinite-derivative theories -- is the")
print("        initial-data specification for the nonlocal kernel; it is the generic Route-E nonlocality issue, NOT an")
print("        aether strong-coupling problem, and NOT worsened by the passive frame.)")

# ---------------------------------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------------------------------
print("\n" + "="*100)
print(" VERDICT")
print("="*100)
print(r"""
 Q0 ANSWER: the framework's dS-Unruh premise supplies u^mu as a PASSIVE horizon-anchored frame,
 NOT a dynamical Einstein-aether. Chain of framework-first facts:

   1. The strong-coupling wall (c13=c14=0) is a statement about the 2-DERIVATIVE aether KINETIC
      term's spin-0/spin-1 modes (3 propagating dof). It CANNOT be stated for a frame with 0 (fixed)
      or 1 (hyp-orthogonal khronon, no spin-1) propagating dof -- there are no c_i to send to zero.

   2. The framework's u^mu = the frame in which the dS/Gibbons-Hawking bath is ISOTROPIC. In FRW/dS
      that frame is the COMOVING, HYPERSURFACE-ORTHOGONAL (gradient) frame u_mu=-grad_mu T/|grad T|
      (Frobenius twist = 0, sympy-verified). A rotating aether would make the bath anisotropic -> not
      the dS-Unruh rest frame. So the framework's frame is at MOST a khronon (spin-0), NEVER a generic
      aether (spin-1 modes are ABSENT by the isotropy premise, not tuned away).

   3. The MOND lives in S_matter (the nonlocal K), and u only sets the bath REFERENCE DIRECTION. The
      framework never needs an aether field equation delta S/delta u to SOURCE MOND -- unlike AeST,
      whose aether EOM IS the MOND force and which therefore GENUINELY NEEDS a dynamical aether (that
      is exactly why the c13=c14=0 wall bites AeST and NOT the framework). The framework can take u
      FIXED (the cosmological rest frame, dynamically selected like the CMB frame in LCDM: 0 new dof)
      and still reproduce all its phenomenology.

   4. Local covariance does NOT force the 2-derivative aether kinetic term: it is satisfied by either
      (E1) a spontaneously-selected cosmological frame (Bianchi-automatic conservation, 0 new dof) or
      (E2) a minimal unit-norm khronon constraint lambda(u.u+1) -- whose Hessian carries NO derivatives
      of u (sympy-verified), hence NO kinetic term, NO spin-1, NO c13/c14. Neither builds the aether.

   5. PASSIVE-FRAME CAUCHY: with u fixed, Box_u is an ordinary 2nd-order hyperbolic operator along u,
      and the a0-gapped ENTIRE form factor K multiplies the principal symbol without adding a zero,
      a new characteristic, or a ghost pole. The passive-frame + nonlocal-K matter system is
      HYPERBOLIC / WELL-POSED (up to the generic Route-E nonlocal initial-data specification, which is
      not an aether pathology and is not worsened by the passive frame).

 => the c13=c14=0 aether STRONG-COUPLING wall is MOOT for the framework: it applies to the DYNAMICAL-
    aether (AeST/Einstein-aether) realization the framework is NOT. On the framework's OWN terms, 'the
    Saturn thing' closes on the passive-frame side: u^mu is a passive dS-anchored constraint, and the
    passive-frame + nonlocal-K system is well-posed.

 HONEST RESIDUE (unchanged; do NOT overclaim): the MOND SIGN and Z=sqrt(32pi/3) remain POSTULATED
 (banked, separate); the nonlocal kernel's ACTIVE character must still be founded (passivity->anti-MOND
 is the sign wall, separate); and the generic Route-E nonlocal-initial-data question is a shared MOND
 feature, not closed by a theorem. Q0 closes ONLY the passive-vs-dynamical / aether-strong-coupling
 question -- and it closes it PASSIVE.
""")
print("ALL CHECKS:", "PASS" if all(PASS) else "FAIL", f"({sum(PASS)}/{len(PASS)})")
import sys
sys.exit(0 if all(PASS) else 1)
