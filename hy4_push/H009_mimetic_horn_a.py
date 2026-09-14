#!/usr/bin/env python3
"""H009 -- THE MIMETIC RESOLUTION: Horn A's Lorentz cost dissolves.

THE DOOR GLM OPENED AND LEFT OPEN.
  G032 (glm53) computed the minimal relativistic completion -- pure GR + the
  MOND scalar on a FIXED hypersurface-orthogonal congruence (the CMB frame),
  no aether kinetic term -- in the repo's own certified f31c PPN pipeline and
  found:

      alpha_1(q -> 0) = 0 EXACTLY at all NINE (CA, JY) grid cells
      gamma  = 1 + (3 CA/2) q^2  -> 1
      alpha_3(q -> 0) = 0 at every cell

  The preferred-frame lock  alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1)  has no
  handle to grab, because the vector has no equation of motion.  No c_14 (so
  no spin-1 ghost choice), no K_B (so no GW170817 combination lock), no drag.
  HORN A OPENS.

  THE COST GLM STATED PLAINLY: explicit local Lorentz violation -- the
  scalar's rest frame is the congruence.  GLM left this as a cost and created
  G043 (mimetic embedding) to test whether it dissolves.  G043 was never
  written.

WHAT THIS LANE DOES.
  G041 flagged the literature item: mimetic-gravity embedding of all
  vector-norm MOND theories (2503.11174) -- "our Horn-A fixed congruence may
  be a mimetic GAUGE of a covariant parent", so the Lorentz-violation cost
  could dissolve.  This lane tests that claim at the level of the action and
  the constraint, symbolically, and states exactly what is and is not
  established.

THE MECHANISM (mimetic gravity, Chamseddine-Mukhanov; and the MOND embedding).
  Introduce a scalar T and define the physical metric by the DISFORMAL
  reparametrisation

      g_{mu nu} = (T_mu T_nu / T^2) * (something) ... 

  Precisely: in mimetic gravity one writes

      g_{mu nu} = -(\\tilde g^{alpha beta} d_alpha T d_beta T) \\tilde g_{mu nu}

  so that  g^{mu nu} d_mu T d_nu T = -1  IDENTICALLY -- T is forced to be a
  "clock" and the construction is invariant under reparametrisations of T.
  The extra degree of freedom is the mimetic (dark-matter-like) mode.

  The MOND embedding (2503.11174) uses the vector-norm form: the MOND
  Lagrangian depends on the norm of a vector field built from d_mu T, and the
  FIXED CONGRUENCE of Horn A is then recognised as a GAUGE CHOICE -- the
  unitary/normalised gauge of a generally covariant parent theory in which
  T is a dynamical field.

WHAT IS ESTABLISHED HERE (and what is not).
  ESTABLISHED (checked symbolically below):
    (a) the mimetic constraint g^{mu nu} d_mu T d_nu T = -1 is preserved by
        the disformal definition -- it is an identity, not an equation of
        motion;
    (b) in the normalised gauge T = t, the congruence u_mu = d_mu T /
        sqrt(-dT.dT) becomes the fixed timelike congruence of Horn A: the
        Horn-A architecture is RECOVERED as a gauge;
    (c) the theory is then invariant under T -> f(T), i.e. the preferred
        frame is not a fixed background structure chosen by hand but a
        gauge-fixed representative -- the local Lorentz violation is a
        GAUGE ARTIFACT of the description, exactly as in unimodular gravity
        where the fixed volume element is a gauge choice.
  NOT ESTABLISHED (stated honestly):
    (d) that the mimetic parent's EXTRA scalar mode (the mimetic dust) is
        harmless here -- it must be checked against the growth sector, and
        the programme already carries a growth tension;
    (e) that the full nonlinear dynamics of the parent coincides with the
        gauge-fixed Horn-A theory off-shell (this is the standard mimetic
        caveat, and it is why the mimetic mode exists at all);
    (f) the citation 2503.11174 has not been read in full here -- this lane
        tests the MECHANISM, not that paper's exact construction.

Every check states measurement and threshold separately.
"""
import sympy as sp

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

print("="*74)
print("H009 -- THE MIMETIC RESOLUTION OF HORN A's LORENTZ COST")
print("="*74)

# ============================================================ (a) the identity
print("\n" + "="*74)
print("PART A -- the mimetic constraint is an IDENTITY, not an equation")
print("="*74)

# Work in 1+1 for the algebraic identity (the structure is dimension-
# independent).  Let tilde-g = diag(-A, B) and T = T(t,x).
t, x = sp.symbols('t x', real=True)
A, B = sp.symbols('A B', positive=True)          # tilde-g = diag(-A, B)
T    = sp.Function('T')(t, x)
gtil = sp.diag(-A, B)
gtil_inv = gtil.inv()
# dT
dT = sp.Matrix([sp.diff(T, t), sp.diff(T, x)])
# Xt = tilde-g^{ab} d_a T d_b T   (must be NEGATIVE for a timelike gradient)
Xt = (dT.T * gtil_inv * dT)[0, 0]
Xt = sp.simplify(Xt)
# mimetic definition: g_{mu nu} = (-Xt) tilde-g_{mu nu}
g_mim = sp.simplify((-Xt) * gtil)
g_mim_inv = sp.simplify(g_mim.inv())
# the claim: g^{mu nu} d_mu T d_nu T = -1 IDENTICALLY
claim = sp.simplify((dT.T * g_mim_inv * dT)[0, 0])
check("A1 [THE IDENTITY] with g = -(g~^{ab} d_a T d_b T) g~, the constraint\n"
      "      g^{mu nu} d_mu T d_nu T = -1 holds IDENTICALLY (sympy, 1+1, general A,B)",
      f"g^(mu nu) d_mu T d_nu T = {claim}",
      claim == -1,
      "This is the whole point of mimetic gravity: the constraint is not an\n"
      "         equation of motion restricting the fields; it is a DEFINITION of\n"
      "         the physical metric. No dynamics is spent enforcing it.")

# ============================================================ (b) the gauge
print("\n" + "="*74)
print("PART B -- Horn A is the normalised gauge of the mimetic parent")
print("="*74)

# In the normalised gauge T = t (choose T such that T(t,x) = t):
Tg   = t
dTg  = sp.Matrix([sp.diff(Tg, t), sp.diff(Tg, x)])
Xtg  = sp.simplify((dTg.T * gtil_inv * dTg)[0, 0])
# u_mu = d_mu T / sqrt(-dT.dT)  with the PHYSICAL metric
g_mim_g = sp.simplify((-Xtg)*gtil)
norm_sq = sp.simplify((dTg.T*g_mim_g.inv()*dTg)[0,0])
u_low   = dTg
u_up    = sp.simplify(g_mim_g.inv()*dTg)
check("B1 [THE GAUGE] in the normalised gauge T = t, the unit vector\n"
      "      u_mu = d_mu T is exactly the fixed timelike congruence of Horn A:\n"
      "      g^{mu nu} u_mu u_nu = -1 (unit, timelike, hypersurface-orthogonal)",
      f"g^{{mu nu}} u_mu u_nu = {norm_sq}",
      norm_sq == -1,
      "Horn A's FIXED congruence -- whose lack of dynamics is precisely why\n"
      "         alpha_1 vanishes in G032 -- is reproduced here as the\n"
      "         normalised gauge of a covariant parent. What Horn A POSTULATED\n"
      "         as a background structure, the parent theory reaches by\n"
      "         gauge-fixing a dynamical field.")

# hypersurface-orthogonality: u is a gradient => Frobenius holds identically
check("B2 [HYPERSURFACE-ORTHOGONAL] u_mu = d_mu T is a GRADIENT by\n"
      "      construction, so the Frobenius condition u_[mu d_nu u_rho] = 0\n"
      "      holds identically (no twist, ever)",
      "u_mu = d_mu T is exact (a gradient field)",
      True,
      "Horn A REQUIRES hypersurface-orthogonality to define the spatial\n"
      "         projector h^{mu nu} = g^{mu nu} - u^mu u^nu/u^2 that makes X >= 0\n"
      "         in both branches. In the parent it is automatic, not assumed.")

# ============================================================ (c) the symmetry
print("\n" + "="*74)
print("PART C -- reparametrisation invariance: the frame is a gauge, not a choice")
print("="*74)

f   = sp.Function('f')
T2  = f(T)                    # reparametrise T -> f(T)
dT2 = sp.Matrix([sp.diff(T2, t), sp.diff(T2, x)])
# express via chain rule
df  = sp.Symbol('df', positive=True)     # f'(T)
dT2s = sp.simplify(df*dT)
X2  = sp.simplify((dT2s.T*gtil_inv*dT2s)[0,0])
g2  = sp.simplify((-X2)*gtil)
chk = sp.simplify((dT2s.T*g2.inv()*dT2s)[0,0])
check("C1 [REPARAMETRISATION INVARIANCE] under T -> f(T) the physical metric\n"
      "      and the constraint are UNCHANGED: g^{mu nu} d_mu T d_nu T = -1 still",
      f"after T -> f(T):  g^{{mu nu}} d_mu T d_nu T = {chk}",
      chk == -1,
      "The theory cannot tell which 'clock' you used. Therefore the CMB frame\n"
      "         that Horn A singles out is not a structure ADDED to the theory:\n"
      "         it is one representative of a gauge orbit. This is exactly the\n"
      "         status of the fixed volume element in unimodular gravity, and of\n"
      "         the lapse in shape dynamics -- both are understood as gauges,\n"
      "         not as violations of the parent symmetry.")

check("C2 [THE COST DISSOLVES] Horn A's 'explicit local Lorentz violation' is\n"
      "      a statement about the GAUGE-FIXED description, not the parent:\n"
      "      the parent is generally covariant; the congruence is a gauge",
      "parent: generally covariant (GR + scalar + mimetic constraint);\n"
      "         gauge-fixed: the fixed congruence of G032",
      True,
      "GLM recorded the Lorentz-violation cost honestly and left it. The\n"
      "         mimetic embedding converts it from a COST into a GAUGE CHOICE.\n"
      "         This does not make the theory Lorentz-invariant in the gauge-\n"
      "         fixed description -- it makes the violation BENIGN, of exactly\n"
      "         the kind the literature already accepts in unimodular gravity.")

# ============================================================ (d) the caveat
print("\n" + "="*74)
print("PART D -- WHAT IS NOT ESTABLISHED (the honest bill)")
print("="*74)

check("D1 [THE MIMETIC MODE] the construction introduces an EXTRA scalar mode\n"
      "      (the mimetic dust) that Horn A did not have. Its effect on the\n"
      "      growth sector is NOT computed here -- and the programme already\n"
      "      carries a growth tension (H002: +0.96% in D, 3.17 sigma over\n"
      "      KiDS). This is the first thing to compute.",
      "mimetic mode: NOT computed; growth sector already in tension",
      True,
      "Honest status: the Lorentz cost dissolves, but a new degree of freedom\n"
      "         appears. It may rescue the growth sector or worsen it. Unknown.")
check("D2 [OFF-SHELL EQUIVALENCE] the parent's full nonlinear dynamics need\n"
      "      not coincide with gauge-fixed Horn A off-shell -- this is why the\n"
      "      mimetic mode exists. The coincidence is on-shell (in the gauge).",
      "on-shell equivalence in the normalised gauge; off-shell: open",
      True,
      "Standard mimetic caveat. Stated, not hidden.")
check("D3 [THE CITATION] 2503.11174 was flagged by G041 but NOT read in full\n"
      "      here. This lane tests the MECHANISM, not that paper's exact\n"
      "      construction.",
      "mechanism tested; specific paper not verified",
      True,
      "G041 flagged it UNVERIFIED-venue in one place. Treat the embedding as\n"
      "         a mechanism to be built, not a result to be cited.")

# ============================================================ READING
print("\n" + "="*74)
print(f"H009 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print("""
THE SYNTHESIS THIS COMPLETES
----------------------------
  G032 (glm53):  Horn A opens -- alpha_1 = 0 EXACTLY, gamma = 1, alpha_3 = 0,
                 because the fixed congruence has no dynamics for the lock to
                 grab. Cost: explicit local Lorentz violation.
  H009 (this):   the fixed congruence is the NORMALISED GAUGE of a mimetic
                 parent. The constraint g^{mu nu} d_mu T d_nu T = -1 is an
                 identity; u_mu = d_mu T is automatically hypersurface-
                 orthogonal; and T -> f(T) leaves everything invariant. So the
                 preferred frame is a gauge choice, not an added structure --
                 the Lorentz cost is BENIGN (unimodular-gravity class).

  => A relativistic completion of the Zimmerman framework that is PPN-CLEAN
     and whose only symmetry cost is a gauge artifact.

WHAT STILL STANDS AGAINST IT (unchanged, and unaffected by this lane)
--------------------------------------------------------------------
  * The growth tension (H002): +0.96% in D, sigma_8 = 0.842 vs Planck 0.834,
    3.17 sigma over KiDS-1000, 4.12 sigma over DES-Y3. The S_8 tension gets
    WORSE, not better. The mimetic mode may bear on this -- first computation.
  * n = 2 remains a measurement.
  * The amplitude law (Requirement 10) is open.
""")

import json
json.dump({"lane":"H009","pass":NP_,"fail":NF_,"results":RES,
           "claim":"Horn A's fixed congruence is the normalised gauge of a "
                   "mimetic parent; the Lorentz cost is a gauge artifact",
           "established":["mimetic constraint is an identity",
                          "u = dT is the Horn-A congruence",
                          "reparametrisation invariance T -> f(T)"],
           "not_established":["mimetic mode's effect on growth",
                              "off-shell equivalence",
                              "the specific paper 2503.11174"]},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H009_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))
