#!/usr/bin/env python3
r"""
refute_strongcoupling.py  --  ADVERSARIAL REFUTATION, LENS = strong coupling / well-posedness.

CLAIM UNDER TEST (ROBUST_SURVIVES): the covariant MI completion is a predictive, well-posed
field theory in the fully-nonlocal dynamical-u regime; the mixed propagator is ghost-free,
hyperbolic, no-Cherenkov, and the spin-0 kinetic norm is "bounded away from 0 (no strong
coupling)" on the witness corner c1=0.526, c3=0.261.

THE KNOWN PHYSICS (Foster-Jacobson gr-qc/0509083; Jacobson 0801.1547 status report;
gr-qc/0509083 + web-confirmed this session):
  - The framework's "SURVIVES corner" c4=-c3^2/c1, c2=(-2c1^2-c1c3+c3^2)/(3c1) is EXACTLY the
    alpha1 = alpha2 = 0 preferred-frame PPN surface. c+/-=c1+/-c3 are the only free params.
  - On THIS surface the spin-0 and spin-1 speeds are FINITE (good), BUT:
      * The observational corner from binary-pulsar orbital decay forces  c+ = c1+c3  <~ O(10^-2)
        (Foster's estimate; c_i << 1).
      * As c_i -> 0 the aether KINETIC NORMS (N1 ~ 2c14(1-c13), spin-0 norm ~ c14(2-c14),
        and the true spin-0 kinetic coefficient) -> 0  => the modes become INFINITELY STRONGLY
        COUPLED (the classic ae-theory strong-coupling problem: the interaction scale
        M_sc ~ M_Planck * sqrt(c_i) -> 0).
  - The refutation question: the witness point c1=0.526, c3=0.261 has c+ = 0.787 = O(1), which is
    RULED OUT by the very binary-pulsar bound that defines the phenomenologically-viable corner.
    At the PHYSICAL corner (c_i<<1) the kinetic norms are TINY -> strong coupling. Does the
    nonlocal MI matter coupling CURE, IGNORE, or WORSEN this? And is the Cauchy problem well-posed
    (finite strong-coupling scale) at the physical corner, not just the cherry-picked O(1) witness?

DEFAULT refuted=TRUE unless the compute survives at the PHYSICAL (c_i<<1) corner too.
"""
import sympy as sp
import numpy as np

print("#"*100)
print("# [A] Confirm the 'SURVIVES corner' IS the alpha1=alpha2=0 surface, and get alpha1,alpha2")
print("#"*100)
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)
c13=c1+c3; c14=c1+c4; c123=c1+c2+c3; cm=c1-c3

# Foster-Jacobson alpha1, alpha2 (gr-qc/0509083, eqs. 4.9-4.10). Standard published forms:
alpha1 = sp.simplify( (-8*(c3**2 + c1*c4)) / (2*c1 - c1**2 + c3**2) )
alpha2 = sp.simplify(
    alpha1/2
    - ( (c1+2*c3-c4)*(2*c1+3*c2+c3+c4) ) / ( c123*(2-c14) )
)
print(" alpha1 =", alpha1)
print(" alpha2 =", alpha2)

# The framework corner:
c4_corner = -c3**2/c1
c2_corner = (-2*c1**2 - c1*c3 + c3**2)/(3*c1)
a1c = sp.simplify(alpha1.subs({c4:c4_corner}))
a2c = sp.simplify(alpha2.subs({c2:c2_corner, c4:c4_corner}))
print("\n On the framework corner (c4=-c3^2/c1, c2=(-2c1^2-c1c3+c3^2)/(3c1)):")
print("   alpha1 ->", a1c)
print("   alpha2 ->", a2c)
print("   => CONFIRMED: the framework's SURVIVES corner is EXACTLY the alpha1=alpha2=0 surface"
      if (sp.simplify(a1c)==0 and sp.simplify(a2c)==0) else
      "   => NOT the alpha1=alpha2=0 surface (alpha values above)")

print("\n"+"#"*100)
print("# [B] KINETIC NORMS on the corner as functions of c+=c1+c3 (the ONLY free param direction)")
print("#     The strong-coupling test: do the norms -> 0 as c_i -> 0 (the physical corner)?")
print("#"*100)
# On the corner, express everything in c1,c3 (c+ = c1+c3, c- = c1-c3).
c14_c = sp.simplify(c1 + c4_corner)       # = (c1^2-c3^2)/c1 = c+*c-/c1
c13_c = c13
c123_c = sp.simplify(c1 + c2_corner + c3)
N1_c   = sp.simplify(2*c14_c*(1-c13_c))                       # spin-1 kinetic norm (Jacobson)
spin0_norm_c = sp.simplify(c14_c*(2-c14_c))                   # spin-0 energy/kinetic sign proxy
print(" c14 on corner       =", c14_c, "  (= (c1^2-c3^2)/c1 = c+ c- / c1)")
print(" c123 on corner      =", sp.simplify(c123_c))
print(" N1 (spin-1 norm)    =", N1_c)
print(" spin-0 norm c14(2-c14) =", spin0_norm_c)

# The TRUE spin-0 kinetic coefficient (Jacobson 0801.1547): the spin-0 canonical kinetic
# normalization is proportional to  c14 (2 + c13 + 3 c2)/( something )... but the physically
# decisive strong-coupling diagnostic is the OVERALL scale at which the modes' kinetic terms
# vanish. Track the LEADING small-c behavior. Put c1 = x, c3 = r*x (r fixed ratio), x->0.
x, r = sp.symbols('x r', positive=True)
sub_small = {c1: x, c3: r*x}
c14_small  = sp.series(c14_c.subs(sub_small), x, 0, 3).removeO()
N1_small   = sp.series(N1_c.subs(sub_small), x, 0, 3).removeO()
s0norm_small = sp.series(spin0_norm_c.subs(sub_small), x, 0, 3).removeO()
print("\n SMALL-COUPLING SCALING (c1=x, c3=r x, x->0 -- the PHYSICAL binary-pulsar corner):")
print("   c14      ~", c14_small, "   -> O(x) -> 0")
print("   N1(spin1)~", N1_small, "   -> O(x) -> 0")
print("   c14(2-c14)~", s0norm_small, "   -> O(x) -> 0")
print("""
 READING: EVERY aether kinetic norm -> 0 LINEARLY in x=c1 as the couplings shrink. This IS the
 textbook ae-theory strong-coupling problem: the canonical kinetic terms vanish, so the
 interaction (strong-coupling) scale M_sc ~ M_Pl * sqrt(kinetic norm) ~ M_Pl*sqrt(c_i) -> 0.
 The witness c1=0.526,c3=0.261 (c+=0.787=O(1)) HIDES this by sitting at O(1) couplings that the
 binary-pulsar bound c+<~O(10^-2) EXCLUDES.""")

print("\n"+"#"*100)
print("# [C] Is the witness point c+=0.787 observationally ALLOWED? (Cherenkov + pulsar bounds)")
print("#"*100)
# Gravitational Cherenkov / GW170817 requires the spin-2 speed s2 within ~1e-15 of c.
# s2^2 = 1/(1-c13). c13=c+ => s2^2 = 1/(1-c+). For c+=0.787, s2^2 = 1/0.213 = 4.695 => s2=2.17c.
# That is a 117% superluminal graviton -> RULED OUT by GW170817 at the 1e-15 level.
c_plus = sp.symbols('c_plus', real=True)
s2sq = 1/(1-c_plus)
for cp in [0.787, 1e-2, 1e-3, 1e-15]:
    val = float(s2sq.subs(c_plus, cp))
    print(f"   c+={cp:>8.0e}:  s2^2 = 1/(1-c+) = {val:.6f}  => spin-2 speed = {np.sqrt(val):.6f} c"
          f"  {'[GW170817-EXCLUDED: |s2-1|>>1e-15]' if abs(np.sqrt(val)-1)>1e-14 else '[ok]'}")
print("""
 The witness c+=0.787 gives a graviton moving at 2.17c -- EXCLUDED by GW170817 (|c_gw/c-1|<1e-15)
 by ~15 orders of magnitude. So s2^2>=1 'no-Cherenkov' was read BACKWARDS: for the framework's
 matter to not Cherenkov it needs s_matter<s_grav, but GW170817 pins s_grav = c to 1e-15, i.e.
 c13 = c+ <~ 1e-15. THAT is the physical corner -- and there, ALL kinetic norms ~ c+ ~ 1e-15 -> 0.""")

print("\n"+"#"*100)
print("# [D] STRONG-COUPLING SCALE at the PHYSICAL corner (c+ ~ 1e-15), with the MI matter coupling")
print("#"*100)
print(r"""
 The nonlocal MI matter coupling adds  eps * a0^2 * Q(z) to the transverse (spin-1) inverse
 propagator, where Q(z) is O(1) at the a0 scale and the aether kinetic term is N1*(s1^2 k^2-omega^2).
 STRONG COUPLING is governed by the RATIO of the interaction vertex to the kinetic norm. As the
 aether norm N1 ~ c+ -> 0, the canonically-normalized aether/frame field is
   v_canonical = sqrt(N1) * v   =>  every self-interaction vertex ~ 1/sqrt(N1)^n BLOWS UP.
 Question: does the MI matter term eps*a0^2*Q RE-NORMALIZE the kinetic term back up (curing strong
 coupling) or is it itself (nu-1)-suppressed and thus NEGLIGIBLE vs the vanishing N1?
""")
# The matter kinetic contribution to the spin-1 norm is eps*a0^2*(coefficient of omega^2 in Q at
# high freq). Q(z)->1 as z->-inf (deep Newton), and near omega~a0 Q~O(1). The coefficient of the
# omega^2 kinetic term from the matter piece: d/d(omega^2)[eps a0^2 Q(-omega^2/a0^2)] at large omega.
# Since Q saturates to a CONSTANT (=1) at high omega, dQ/d(omega^2) -> 0 => the matter piece adds
# NO omega^2 kinetic term at high frequency. It only renormalizes the norm near omega~a0.
zc = sp.symbols('zc', real=True)
Kz = (sp.sqrt(1+4*zc)-1)/(2*sp.sqrt(zc))
Qz = sp.simplify(Kz + 2*zc*sp.diff(Kz,zc))
# matter kinetic-norm contribution: coefficient of omega^2 = -eps*(dQ/dz)*(1/a0^2)*a0^2 = -eps dQ/dz
dQ = sp.simplify(sp.diff(Qz, zc))
print(" Q(z) =", Qz)
print(" dQ/dz =", dQ)
# At the aether pole z = -s1^2 k^2 / a0^2. At the physical (deep-Newton) high-freq pole z->-inf:
dQ_deepNewton = sp.limit(dQ, zc, -sp.oo)
print(" dQ/dz at z->-inf (deep-Newton, solar) =", dQ_deepNewton, " => matter adds ZERO extra kinetic norm at high freq")
# At the a0-scale (z ~ -1), dQ/dz is O(1):
dQ_a0 = sp.N(dQ.subs(zc, -1))
print(f" dQ/dz at z=-1 (a0 scale)              = {dQ_a0}  => O(1) matter norm ONLY at omega~a0 (galactic bath)")

print(r"""
 VERDICT of [D]: the MI matter coupling adds an O(eps) kinetic renormalization ONLY at the a0
 scale (omega ~ a0 ~ 1e-10 s^-1, the galactic bath). At SOLAR / laboratory / pulsar frequencies
 (omega >> a0) the matter piece saturates to a CONSTANT (dQ/dz->0) and contributes NOTHING to the
 kinetic norm. So the aether spin-0/spin-1 kinetic norm at ALL frequencies relevant to the strong-
 coupling problem (which lives at high energy, the UV) is STILL just N1 ~ c+ ~ 1e-15 -> 0.
 The nonlocal MI matter coupling therefore does NOT cure the strong-coupling problem -- it is
 a0-scale-gapped and IR, while strong coupling is a UV disease. It IGNORES it.""")

print("\n"+"#"*100)
print("# [E] Explicit strong-coupling scale M_sc and where the EFT breaks vs relevant physics")
print("#"*100)
# For ae-theory, the strong-coupling scale for the spin-0 mode is M_sc ~ sqrt(c) * M_Pl (schematic;
# more precisely the scalar becomes strongly coupled at M_sc ~ (c * M_Pl^2 * ...)-type). Use the
# canonical estimate M_sc ~ sqrt(c14) * M_Pl for the transverse and the spin-0 scale set by c14,c123.
Mpl = 2.435e18  # GeV reduced Planck mass
for cp in [0.787, 1e-2, 1e-15]:
    # on the corner set c1=c3=c+/2 (r=1) for a representative; c14 = c+ c-/c1, take c- ~ c+ scale.
    # Use N1 ~ c+ scaling; M_sc ~ sqrt(N1)*Mpl ~ sqrt(c+)*Mpl.
    Msc = np.sqrt(cp)*Mpl
    print(f"   c+={cp:>8.0e}: strong-coupling scale M_sc ~ sqrt(c+)*M_Pl ~ {Msc:.3e} GeV")
print("""
 At the OBSERVATIONALLY REQUIRED corner c+<~1e-15 (GW170817), M_sc ~ 3e-8 * M_Pl ~ 1e11 GeV.
 That is still high (nucleosynthesis/lab safe), BUT the point for THIS lens is different:
 the spin-0 mode of ae-theory at the alpha1=alpha2=0 surface is the KNOWN strong-coupling mode,
 and the compute CERTIFIED ghost-freedom / hyperbolicity at c+=0.787 -- a point excluded by
 GW170817 by 15 orders. At the ALLOWED c+~1e-15 corner the compute's own diagnostics (N1, spin-0
 norm) are ~1e-15, i.e. the linear-propagator analysis is at the EDGE of its validity and the
 nonlinear strong-coupling / Cauchy analysis (explicitly deferred as caveat (b)) is REQUIRED and
 NOT done. The MI matter coupling is a0-gapped (IR) and cannot lift a UV strong-coupling scale.""")

print("\n"+"#"*100)
print("# REFUTATION READING")
print("#"*100)
print(r"""
 (1) The 'SURVIVES corner' is EXACTLY the alpha1=alpha2=0 surface (confirmed symbolically, [A]).
     This is the surface with the KNOWN Einstein-aether strong-coupling problem in the spin-0 mode.
 (2) The witness point c1=0.526,c3=0.261 (c+=0.787) used for ALL the ghost/hyperbolicity/no-Cherenkov
     PASSES gives a spin-2 graviton at 2.17c -- EXCLUDED by GW170817 by ~15 orders of magnitude ([C]).
     The certification was done at a point the theory is not ALLOWED to occupy.
 (3) At the observationally-required corner (c+ <~ 1e-15) ALL aether kinetic norms ~ c+ -> 0 ([B]),
     i.e. the modes are near-strongly-coupled; the linear 2-point analysis loses control there.
 (4) The nonlocal MI matter coupling is a0-scale-gapped (dQ/dz->0 for omega>>a0, [D]): it adds
     kinetic norm ONLY in the IR galactic bath and NOTHING in the UV where strong coupling lives.
     => it does NOT cure the strong-coupling problem; it IGNORES it.
 CONCLUSION: The ROBUST_SURVIVES 2-point verdict is manufactured at a GW170817-excluded O(1) corner.
 At the physically-required corner the strong-coupling / well-posedness question is OPEN (the
 nonlinear Cauchy analysis is deferred, caveat (b)), and the MI coupling does not close it. The
 correct verdict under the strong-coupling/well-posedness lens is NOT a clean ROBUST_SURVIVES:
 it is PARTIAL at best (2-point ghost-freedom shown ONLY at an excluded point; UV strong coupling
 at the allowed corner UNADDRESSED), leaning WALLED for predictivity if c+ is forced to ~1e-15.
""")
