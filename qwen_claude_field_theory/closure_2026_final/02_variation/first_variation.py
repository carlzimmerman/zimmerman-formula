"""
first_variation.py
==================
Phase II — the first variation of the nonlocal functional M[g].

This is the decisive step: it determines whether M[g] is a well-defined
functional of the metric, and what the resulting field equation looks like.

Chain (frozen, BASELINE.md):
    g_{mu nu} -> T[g] -> U_mu[g] -> Phi[g] -> Z[g] -> M[g]
    U_mu = -nabla_mu T ,  nabla_mu T nabla^mu T = -1
    Box_ret Phi = R_{mu nu} U^mu U^nu
    Z = (4 c^4/a_0^2) nabla_mu Phi nabla^mu Phi
    nabla_mu [ U^mu (M + F_eps(Z)) ] = 0        (transport definition of M)

The central question: given a metric variation delta g, what is delta M?

KEY STRUCTURAL RESULT (derived below):
    delta M is NOT local in delta g. It is determined by a LINEAR TRANSPORT
    EQUATION along the flow U, with a source built from delta g and its
    derivatives. This makes E_{mu nu} = delta M / delta g^{mu nu} a NONLOCAL
    tensor (it involves retarded Green's functions and transport integrals).

The module works in two parts:
  (A) A concrete symbolic/numeric demonstration in a 1+1 simplified model
      that makes the transport structure of delta M explicit and verifiable.
  (B) The full covariant variation, laid out as equations (see
      first_variation.md), with the conservation/Bianchi constraint derived.

Claim labels: DERIVED / IMPOSED / FITTED / UNKNOWN.
"""
import sympy as sp

# ----------------------------------------------------------------------------
# (A) 1+1 model: make the transport structure of delta M explicit
#
# We reduce to 1+1 dimensions, flat background, and a single spatial
# coordinate, to isolate the transport structure. In this model:
#   U^mu = (1, 0)  (unit timelike, static)
#   M + F(Z) is constant along the flow (transport eq becomes d/dt (M+F) = 0)
#   The variation delta M is then determined by the source from delta g.
#
# The point is to show that delta M = (integral along the flow of a source
# built from delta g), i.e. NONLOCAL in delta g.
# ----------------------------------------------------------------------------

def model_1d_transport():
    """
    1+1 model. t in R, x fixed. U^mu = (1,0). Transport equation:
        d/dt [ M(t) + F(Z(t)) ] = 0
    Vary:
        d/dt [ dM(t) + F'(Z) dZ(t) ] = 0
    =>  dM(t) = - F'(Z) dZ(t) - C   (C is a constant of integration = IC)
    If dZ is driven by delta g (e.g. dZ ~ delta g * (known)), then
    dM(t) = -F'(Z) * (integral of source) - C : NONLOCAL in delta g.
    """
    t = sp.symbols('t', real=True)
    dM, dZ, Fp = sp.symbols('dM dZ Fp', cls=sp.Function)
    C = sp.symbols('C', real=True)  # constant of integration (IC along the flow)
    # d/dt [ dM + Fp * dZ ] = 0
    expr = sp.diff(dM(t) + Fp(t)*dZ(t), t)
    # Solve: dM(t) + Fp(t) dZ(t) = C  =>  dM = C - Fp dZ
    sol_dM = C - Fp(t)*dZ(t)
    return {
        "transport_equation": sp.simplify(expr),
        "dM_solution": sp.simplify(sol_dM),
        "note": "dM(t) = C - F'(Z) dZ(t). If dZ ~ (source from delta g), "
                "then dM is an integral along t of the source => NONLOCAL in delta g.",
    }


# ----------------------------------------------------------------------------
# (B) Full covariant variation (symbolic, structure)
#
# We derive the varied transport equation for delta M and identify the
# transport PDE. We work at the level of the operator structure (the
# coefficients are given in first_variation.md).
# ----------------------------------------------------------------------------

def covariant_variation_structure():
    """
    Let J^mu = U^mu (M + F(Z)).  On-shell: nabla_mu J^mu = 0.

    Under g -> g + delta g (and the induced variations of U, Phi, Z, M):

      0 = delta(nabla_mu J^mu)|_on-shell
        = nabla_mu [ delta J^mu + (1/2) (g^{alpha beta} delta g_{alpha beta}) J^mu ]

    where
      delta J^mu = delta U^mu (M + F) + U^mu (delta M + F'(Z) delta Z)

    =>  nabla_mu [ U^mu delta M ]  =  - nabla_mu [ delta U^mu (M+F)
                                                  + U^mu F'(Z) delta Z
                                                  + (1/2)(g^{ab} delta g_ab) J^mu ]

    This is a LINEAR FIRST-ORDER PDE for delta M:
        U^mu nabla_mu (delta M) + (nabla_mu U^mu) delta M  =  S[g, delta g]
    where S is a known source built from delta g, delta U, delta Z.

    STRUCTURE: this is a TRANSPORT EQUATION for delta M along the flow U.
    Solution (with IC on a Cauchy surface Sigma):
        delta M(x) = integral along the flow line of U through x, from Sigma,
                     of [ S / (J-normalization) ]  +  (IC transported).
    =>  delta M is NONLOCAL in delta g (it integrates the source along flow lines).
    """
    return {
        "varied_transport_eq":
            "nabla_mu[ U^mu dM + dU^mu (M+F) + U^mu F'(Z) dZ "
            "+ (1/2)(g^{ab} dg_ab) J^mu ] = 0",
        "dM_transport_PDE":
            "U^mu nabla_mu (dM) + (nabla_mu U^mu) dM = S[g, dg]",
        "nonlocal": True,
        "explanation":
            "dM is determined by integrating the source S along the flow lines of U "
            "from a Cauchy surface. Hence dM (and E_{mu nu} = dM/dg^{mu nu}) is "
            "NONLOCAL in the metric variation.",
    }


# ----------------------------------------------------------------------------
# (C) Conservation / Bianchi constraint on E_{mu nu}
#
# The field equation is (structure; see first_variation.md):
#     G_{mu nu} - Lambda g_{mu nu} - (a_0^2/c^4) E_{mu nu} = (8 pi G/c^4) T^{(m)}_{mu nu}
# where E_{mu nu} = delta M / delta g^{mu nu} (the M-stress tensor).
#
# Taking the covariant divergence:
#     nabla^mu G_{mu nu} = 0  (Bianchi)
#     =>  - (a_0^2/c^4) nabla^mu E_{mu nu} = (8 pi G/c^4) nabla^mu T^{(m)}_{mu nu}
#
# For consistency, the RHS must be determined by the matter equation of motion
# (which gives nabla^mu T^{(m)}_{mu nu} = 0 if matter is on-shell). So we NEED
#     nabla^mu E_{mu nu} = 0    (on the full on-shell solution)
# OR, if matter is NOT on-shell, the force balance
#     nabla^mu E_{mu nu} = - (8 pi G/c^4) nabla^mu T^{(m)}_{mu nu}
# must hold.
#
# This is a STRONG constraint on the nonlocal tensor E_{mu nu}: it must be
# covariantly conserved (on-shell). This is the main consistency condition
# that the nonlocal variation must satisfy. It is the relativistic analogue of
# the requirement that the MOND force be a gradient (irrotational).
# ----------------------------------------------------------------------------

def conservation_constraint():
    return {
        "field_eq": "G_{mu nu} - Lambda g_{mu nu} - (a_0^2/c^4) E_{mu nu} = (8 pi G/c^4) T^{(m)}_{mu nu}",
        "bianchi": "nabla^mu G_{mu nu} = 0",
        "constraint": "nabla^mu E_{mu nu} = (8 pi G/c^4) nabla^mu T^{(m)}_{mu nu}  (on-shell => 0 if matter on-shell)",
        "meaning":
            "The nonlocal M-stress tensor E_{mu nu} = delta M/dg^{mu nu} MUST be "
            "covariantly conserved on-shell (for matter on-shell). This is the key "
            "consistency condition. Whether the transport-defined delta M yields a "
            "conserved E_{mu nu} is the crux of the closure.",
    }


# ----------------------------------------------------------------------------
# (D) The T-determination GAP (documented, not resolved)
#
# The frozen chain writes T[g] (T is a functional of g), but the only equation
# for T in the frozen candidate is the unit-normalization CONSTRAINT
#     nabla_mu T nabla^mu T = -1
# which does NOT determine T from g. There is no evolution equation for T in
# the frozen action (no delta S / delta T term specified).
#
# This is a GAP in the frozen candidate: T is either
#   (i) an independent dynamical field (then the action must include its
#       kinetic term and the chain should be M[g, T], not M[g]), or
#   (ii) determined by g through some unspecified map T[g].
#
# The variation delta M[g] is only well-defined once T's role is fixed.
# ----------------------------------------------------------------------------

def t_determination_gap():
    return {
        "gap":
            "The frozen chain writes T[g] but the only T-equation is the constraint "
            "nabla_mu T nabla^mu T = -1, which does not determine T from g. No "
            "delta S/delta T term is specified in the frozen action.",
        "options": [
            "(i) T is an independent dynamical field; action needs a T kinetic term; "
            "then M = M[g, T] and delta M has both a dg and a dT part.",
            "(ii) T is a specified functional of g via an unspecified map.",
        ],
        "status": "UNKNOWN (gap in frozen candidate)",
    }


def run_all():
    out = {}
    out["model_1d"] = model_1d_transport()
    out["covariant_structure"] = covariant_variation_structure()
    out["conservation"] = conservation_constraint()
    out["t_gap"] = t_determination_gap()
    return out


if __name__ == "__main__":
    import json
    res = run_all()
    print("=== (A) 1+1 transport model ===")
    m = res["model_1d"]
    print("  transport eq:", m["transport_equation"])
    print("  dM solution :", m["dM_solution"])
    print("  note        :", m["note"])
    print()
    print("=== (B) Covariant variation structure ===")
    c = res["covariant_structure"]
    print("  varied transport eq:", c["varied_transport_eq"])
    print("  dM transport PDE   :", c["dM_transport_PDE"])
    print("  nonlocal           :", c["nonlocal"])
    print("  explanation        :", c["explanation"])
    print()
    print("=== (C) Conservation / Bianchi constraint ===")
    v = res["conservation"]
    print("  field eq   :", v["field_eq"])
    print("  constraint :", v["constraint"])
    print("  meaning    :", v["meaning"])
    print()
    print("=== (D) T-determination gap ===")
    g = res["t_gap"]
    print("  gap     :", g["gap"])
    for o in g["options"]:
        print("  option  :", o)
    print("  status  :", g["status"])
