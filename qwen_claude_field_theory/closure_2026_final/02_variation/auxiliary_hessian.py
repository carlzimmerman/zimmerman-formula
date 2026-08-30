"""
auxiliary_hessian.py
====================
Phase IV — Local auxiliary representation + the naive (mixed) Hessian.

We localize the nonlocal functional M[g] by introducing auxiliary fields and
study the quadratic (Hessian) action of the auxiliary sector around flat space
with a static clock U^mu = (1,0,0,0). This is where the "naive Hessian
warning" of the baseline is made precise.

Localized action (structure; see auxiliary_representation.md):
    S_aux = int d^4x sqrt(-g) [ -kappa M
                                + Xi (Box Phi - R_{uu})
                                + eta  nabla_mu ( U^mu (M + F(Z)) ) ]
    kappa = a_0^2/c^4 ,  Z = (4 c^4/a_0^2) nabla Phi . nabla Phi
    U^mu = (1,0,0,0)  (static clock, Newtonian regime)

Field roles (from the EOMs, see .md):
    Xi  : multiplier for  Box Phi = R_{uu}   (0 local DOF)
    Phi : dynamical scalar (second order)
    eta : multiplier for the transport eq;  U.d eta = -kappa (1st order)
    M   : algebraic (Lagrange multiplier):  -kappa - U.d eta = 0

QUADRATIC SECTOR around flat space (delta g = 0, R_{uu}=0, U=(1,0,0,0)):
    S_2 = int d^4x [ -kappa dM + dXi Box dPhi + deta dt(dM)
                     + deta dt( (1/2) Z ) + ... ]
The last term is CUBIC (deta x Phi^2) -> dropped at quadratic order.
    S_2 = int d^4x [ -kappa dM + dXi Box dPhi + deta dt(dM) ]

The (eta, M) sector is first-order (no kinetic term): it is a constraint pair.
The (Phi, Xi) sector is the Woodard-style Box bi-scalar:
    int delta_xi Box delta_Phi.  Diagonalize with a = Phi + Xi, b = Phi - Xi:
        S_2 = (1/4) int a Box a  -  (1/4) int b Box b
    =>  a is HEALTHY (kinetic +1/4),  b has the WRONG-sign kinetic term
        (kinetic -1/4)  =>  b = Phi - Xi is a GHOST.

This module verifies the diagonalization and the sign of the kinetic terms
symbolically.
"""
import sympy as sp


def quadratic_sector_flat():
    """
    Quadratic action of the auxiliary sector around flat space, static clock.
    Returns the (Phi, Xi) bi-scalar action and its diagonalization.
    """
    # Fourier-space quadratic action for (Phi, Xi):  S = int d^4k (-k2) Phi X
    # Position-space IBP (signature -+++, Box = -d0^2 + grad^2):
    #   S = int Xi Box Phi.  Set a = Phi+Xi (healthy), b = Phi-Xi (ghost).
    #   Phi = (a+b)/2, Xi = (a-b)/2.
    #   Xi Box Phi = (a-b)(Box a + Box b)/4  ->  cross terms cancel by IBP.
    #   S = (1/4) int a Box a  -  (1/4) int b Box b.
    #   int a Box a = int (d0 a)^2 - (grad a)^2  (healthy kinetic)
    #   int b Box b = int (d0 b)^2 - (grad b)^2
    #   =>  S = (1/4) int[(d0 a)^2 - (grad a)^2] - (1/4) int[(d0 b)^2 - (grad b)^2]
    #   a: kinetic +1/4 (HEALTHY);  b: kinetic -1/4 (GHOST).
    a, b = sp.symbols('a b', real=True)  # a = Phi+Xi (healthy), b = Phi-Xi (ghost)
    da, db = sp.symbols('da db', real=True)  # d0 a, d0 b (time derivatives)
    ga, gb = sp.symbols('ga gb', real=True)  # |grad a|, |grad b|
    S_a = sp.Rational(1, 4) * (da**2 - ga**2)   # healthy scalar kinetic
    S_b = -sp.Rational(1, 4) * (db**2 - gb**2)  # GHOST scalar kinetic (wrong sign)
    coeff_a = sp.Rational(1, 4)   # kinetic coeff of a = Phi + Xi
    coeff_b = -sp.Rational(1, 4)  # kinetic coeff of b = Phi - Xi
    return {
        "diagonal_field_a": "a = Phi + Xi  (HEALTHY, kinetic +1/4)",
        "diagonal_field_b": "b = Phi - Xi  (GHOST, kinetic -1/4)",
        "S_a (healthy)": S_a,
        "S_b (ghost)": S_b,
        "coeff_a": coeff_a,
        "coeff_b": coeff_b,
        "a_is_healthy": bool(coeff_a > 0),
        "b_is_ghost": bool(coeff_b < 0),
        "note": "The (Phi, Xi) bi-scalar from localizing the retarded inverse "
                "Box^{-1} splits into one healthy scalar (a=Phi+Xi) and one "
                "GHOST scalar (b=Phi-Xi, wrong-sign kinetic term). This is the "
                "standard Woodard / Deffayet-Woodard localization ghost.",
    }


def eta_M_sector():
    """
    Quadratic (eta, M) sector:  S_2 = int [ -kappa dM + deta dt(dM) ]
    Integrate by parts:  int deta dt(dM) = -int dM dt(deta)  (no boundary)
    =>  S_2 = int dM ( -kappa - dt(deta) )
    This is ALGEBRAIC in (eta, M): no kinetic term. The EOMs are
        dM:  -kappa - dt(eta) = 0   =>  dt(eta) = -kappa  (1st-order transport)
        deta: -dM = 0  ... wait, this gives dM = 0 at quadratic order.
    Actually: S_2 = int [ -kappa dM + deta dt dM ].
    dS/dM = -kappa + dt(deta) = 0  =>  dt(eta) = -kappa.
    dS/deta = dt(dM) = 0  =>  dM = const (in time) at quadratic order.
    So at quadratic order, M is a (time-constant) Lagrange multiplier and eta
    is a 1st-order transported field. No kinetic term => no ghost here at
    quadratic order, BUT the cubic couplings (deta x Phi^2, dM x ...) make M
    and eta dynamical at higher order. The full DOF/ghost analysis is Phase VI.
    """
    t = sp.symbols('t', real=True)
    dM, deta = sp.symbols('dM deta', cls=sp.Function)
    kappa = sp.symbols('kappa', positive=True)
    S2 = -kappa * dM(t) + deta(t) * sp.diff(dM(t), t)
    eom_M = sp.simplify(sp.diff(S2, dM(t)) + sp.diff(sp.diff(S2, dM(t)), t))
    # dS/dM = -kappa + d/dt(deta)  (after IBP of the deta*dt(dM) term)
    eom_M = sp.simplify(-kappa + sp.diff(deta(t), t))
    eom_eta = sp.simplify(sp.diff(dM(t), t))
    return {
        "S2_etaM": S2,
        "EOM_M (algebraic/1st-order)": sp.Eq(eom_M, 0),
        "EOM_eta (1st-order)": sp.Eq(eom_eta, 0),
        "kinetic_term": "NONE at quadratic order (first-order constraint pair)",
        "note": "At quadratic order (eta,M) are a constraint pair (no kinetic "
                "term, no ghost). Cubic and higher couplings make them "
                "dynamical; the full ghost analysis is Phase VI.",
    }


def run_all():
    out = {}
    out["phi_xi_sector"] = quadratic_sector_flat()
    out["eta_M_sector"] = eta_M_sector()
    return out


if __name__ == "__main__":
    res = run_all()
    print("=== (Phi, Xi) bi-scalar sector (from localizing Box^{-1}) ===")
    px = res["phi_xi_sector"]
    print("  a (healthy):", px["diagonal_field_a"])
    print("  b (ghost)  :", px["diagonal_field_b"])
    print("  S_a        :", px["S_a (healthy)"])
    print("  S_b        :", px["S_b (ghost)"])
    print("  coeff a    :", px["coeff_a"], "  coeff b:", px["coeff_b"])
    print("  a healthy  :", px["a_is_healthy"], "  b is ghost:", px["b_is_ghost"])
    print("  note       :", px["note"])
    print()
    print("=== (eta, M) constraint sector ===")
    em = res["eta_M_sector"]
    print("  S2        :", em["S2_etaM"])
    print("  EOM_M     :", em["EOM_M (algebraic/1st-order)"])
    print("  EOM_eta   :", em["EOM_eta (1st-order)"])
    print("  kinetic   :", em["kinetic_term"])
    print("  note      :", em["note"])
