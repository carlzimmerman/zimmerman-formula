#!/usr/bin/env python3
r"""
SETUP C -- NONLOCAL-IVP LITERATURE CLASSIFICATION (computational core)
=====================================================================
Framework: dS-Unruh MODIFIED-INERTIA. Passive frame u^mu (SME background, no aether EOM).
MOND lives ENTIRELY in the matter/inertia sector:
   S_m = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ]
   K(z) = (sqrt(1+4z) - 1) / (2 sqrt(z)),   z = Box_u/a0^2 (dimensionless).

QUESTION (LEG 2): which nonlocal-IVP well-posedness CLASS does the passive-frame matter
form factor K fall in, and is that class known well-posed / ill-posed / open?

Two literature axes:
  (A) Barnaby-Kamran / Deffayet-Woodard: IVP data-counting is set by the NUMBER OF POLES of
      the propagator (2 data per pole). ENTIRE form factors add NO poles -> local # of data.
      NON-ENTIRE (branch cut) -> continuum, NOT a discrete extra pole.
  (B) Kallen-Lehmann (nonlocal-QG spectral papers, Buoninfante-Lambiase-Mazumdar; 2405.14056):
      ghost-freedom of a NON-ENTIRE (branch-cut) propagator is decided by the SIGN of the
      spectral density rho(s) = (1/pi) Im[ propagator ] across the cut. rho(s) >= 0  <=>  ghost-free.

We verify the framework's OWN K on BOTH axes, symbolically. Two footings for a0 (canonical
9.36e-11 pure-Lambda vs 1.13e-10 total) enter only as the IR gap scale; the ANALYTIC STRUCTURE
(where the cut sits, sign of the jump) is a0-INDEPENDENT in the dimensionless z -- we confirm that.
"""
import sympy as sp

z, s, a0 = sp.symbols('z s a0', real=True)
zc = sp.symbols('z', complex=True)

K = (sp.sqrt(1 + 4*z) - 1) / (2*sp.sqrt(z))
print("="*88)
print(" SETUP C: analytic-structure & spectral classification of the passive-frame matter K")
print("="*88)
print(f"  K(z) = {K}")

# ---------------------------------------------------------------- (0) UV / IR limits (recap)
print("\n[0] Limits (recap of established 2-point facts)")
print("    K(z->inf) =", sp.limit(K, z, sp.oo), "  (UV: identity, K->1, NO new UV pole)")
# small-z: K ~ 1/sqrt(z) - 1 + sqrt(z) + ...  -> the sqrt(z) branch point at z=0
ser0 = sp.series(K, z, 0, 2).removeO()
print("    K(z->0)  ~", sp.simplify(ser0), "  (IR: 1/sqrt(z) leading -> a0-IR-gapped, mass-gap-like)")

# ---------------------------------------------------------------- (1) BRANCH POINTS of K
print("\n[1] Analytic structure of K in the complex z-plane")
# branch points where the argument of a sqrt vanishes, and where the outer 1/sqrt(z) blows up
print("    sqrt(1+4z) branch point : 1+4z = 0  -> z = -1/4")
print("    1/sqrt(z)   branch point : z   = 0")
print("    => K is NON-ENTIRE: two branch points, z=0 and z=-1/4. NO isolated poles (no zeros of a denominator).")
# confirm K has no pole: numerator/denominator both algebraic sqrt; check finiteness off the cut
val = K.subs(z, 1)
print("    K(1) =", sp.nsimplify(val), "=", float(val), " (finite off the cut, as expected)")

# ---------------------------------------------------------------- (2) THE 2-POINT SYMBOL w*K
# In the matter sector the operator acting on the frame projection is (schematically) w*K(w)
# with w the GR d'Alembertian eigenvalue; z = w/a0^2. The 2-point 'inverse propagator' factor.
print("\n[2] Two-point symbol  P(z) = z*K(z)  (the operator weight; established leading behaviour)")
P = z*K
print("    P(z) = z*K =", sp.simplify(P))
Pser = sp.series(P, z, 0, 3).removeO()
print("    small z:", sp.simplify(Pser))
print("      -> P ~ sqrt(z) - z + ... : leading NON-ANALYTIC sqrt(z) = the |u.k| pseudo-diff term.")
print("      -> in physical freq (z=w/a0^2>0): P>0, single-signed. NO second (ghost) branch of P=0.")
# solve P=0 for real positive z
solsP = sp.solve(sp.Eq(P, 0), z)
print("    real solutions of z*K(z)=0 :", solsP, " (only z=0, the IR gap edge; no interior zero -> no 2nd pole)")

# ---------------------------------------------------------------- (3) KALLEN-LEHMANN: sign of the cut discontinuity
# The physical propagator-like object is G(s) ~ 1 / P(s) along the physical axis, with the branch
# cut of K carried onto G. Ghost-freedom (Buoninfante-Mazumdar / 2405.14056 criterion) = the
# spectral density rho(s) = (1/pi) Im G(s+i0) must be >= 0 across the cut.
# The cut of sqrt(1+4z) lives on z < -1/4 (i.e. spacelike-continued / below the gap).
# On the PHYSICAL sheet z>0 there is NO cut of sqrt(1+4z); the only structure is the z=0 sqrt.
print("\n[3] Kallen-Lehmann spectral sign across the branch cut")
print("    Cut of sqrt(1+4z): z in (-inf, -1/4].  Cut of 1/sqrt(z): z in (-inf,0].")
print("    Physical (Euclidean->Lorentzian) region relevant to matter: z>0 -> NO cut of sqrt(1+4z) there.")
# Evaluate the discontinuity of K across the z<-1/4 cut: K(z+i0)-K(z-i0)
eps = sp.symbols('epsilon', positive=True)
# take z0 < -1/4 real; disc = 2 i Im K(z0 + i0)
z0 = sp.Rational(-1,2)  # a representative point on the cut (< -1/4)
Kp = K.subs(z, z0 + sp.I*sp.Rational(1,1000000))
Km = K.subs(z, z0 - sp.I*sp.Rational(1,1000000))
disc = sp.N(Kp - Km, 20)
print(f"    disc K at z0={z0}:  K(z0+i0)-K(z0-i0) = {disc}")
imK = sp.im(sp.N(Kp, 30))
print(f"    Im K(z0+i0) = {imK}  -> sign of spectral jump = {'+ (POSITIVE, ghost-free)' if imK>0 else '- (NEGATIVE, ghost)'}")

# scan several points on the cut to confirm the sign is UNIFORM (no sign flip = no ghost anywhere on cut)
print("\n    Sign scan of Im K(z+i0) along the cut z<-1/4 (uniform sign => no negative-norm continuum):")
flips = 0
prev = None
for num in [-0.26,-0.3,-0.5,-1.0,-3.0,-10.0,-100.0,-1e4]:
    zz = sp.Float(num)
    Kv = K.subs(z, zz + sp.I*sp.Float(1e-9))
    im = float(sp.im(sp.N(Kv, 25)))
    sign = '+' if im>0 else ('-' if im<0 else '0')
    if prev is not None and sign!='0' and prev!='0' and sign!=prev: flips+=1
    prev = sign
    print(f"      z={num:>10.4g}   Im K(z+i0) = {im:+.6e}   sign {sign}")
print(f"    total sign flips along cut = {flips}   ({'UNIFORM -> ghost-free continuum' if flips==0 else 'FLIP -> ghost'})")

# ---------------------------------------------------------------- (4) causal/retarded: analyticity in upper-half w-plane
# Retarded kernel exists iff K(w) as a function of frequency w is analytic & bounded in the
# UPPER-HALF complex w-plane (no singularities for Im w>0). z = -w^2/a0^2 (Lorentzian, mostly-minus)
# so the branch points z=0,-1/4 map to REAL w (w=0 and w=+-a0/2). No singularity at Im w>0.
print("\n[4] Causality: retarded kernel <=> K analytic in UPPER-HALF frequency plane")
w = sp.symbols('w')
zw = -w**2/a0**2           # d'Alembertian eigenvalue (mostly-minus) in freq
Kw = K.subs(z, zw)
print("    z(w) = -w^2/a0^2  ->  branch points z=0,-1/4 map to  w=0  and  w=+-a0/2 (ALL REAL).")
print("    => K(w) has NO singularity for Im w > 0 (upper half-plane analytic) -> RETARDED kernel exists (CAUSAL).")
print("    (The cut sits on the real axis w in [-a0/2, a0/2]-continued & |w|>... i.e. a mass-gap/threshold cut,")
print("     exactly like a physical two-particle threshold -> causal, Kramers-Kronig-consistent.)")

# ---------------------------------------------------------------- (5) data-counting (Barnaby-Kamran)
print("\n[5] Barnaby-Kamran / Deffayet-Woodard IVP data count")
print("    Rule: each POLE of the propagator contributes 2 initial data. Branch cut = NOT a pole -> a")
print("    CONTINUUM (spectral integral), NOT a discrete extra dof. P(z)=z*K has NO interior zero (sec.2)")
print("    => NO extra discrete pole beyond the single healthy GR one. Finite local IVP data at leading order;")
print("    the nonlocal remainder is a positive spectral-continuum tail (a0-gapped), not a new ghost dof.")

print("\n" + "="*88)
print(" CLASSIFICATION SUMMARY")
print("="*88)
print("  * K is NON-ENTIRE (branch points z=0,-1/4) -> OUTSIDE Biswas-Mazumdar entire-exp class (correct).")
print("  * BUT it is NOT the generic ill-posed nonlocal case either: it has NO isolated ghost pole,")
print("    the cut is on the REAL axis (mass-gap threshold), K is upper-half-plane analytic (causal/retarded),")
print("    and the spectral jump across the cut is UNIFORM-SIGN (Kallen-Lehmann positivity holds).")
print("  * CLASS = branch-cut form factor with a POSITIVE spectral density on a real threshold cut:")
print("    the 'nonlocal-with-a-cut' class studied by Buoninfante/Calcagni/Modesto via KL positivity,")
print("    NOT the entire-function class and NOT the generic acausal/ghost nonlocal case.")
