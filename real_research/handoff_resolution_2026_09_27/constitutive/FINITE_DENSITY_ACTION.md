# A conditional causal finite-density fluid branch

This extends the conserved-current construction with an explicitly supplied material edge state. It proves constitutive energy and sound-speed inequalities on the fluid branch. It does not prove gravitational equilibrium stability, nonlinear moving-boundary well-posedness, formation selection or observational agreement.

Fix Pc>0, V>0, ye>0 and c²>0. At fixed material label define, for y>=ye,

    rho = (Pc/V) y/sqrt(1+y),
    F(y) = sqrt(1+y) + log[(sqrt(1+y)-1)/(sqrt(1+y)+1)],
    epsilon = rho {c² + V[F(y)-F(ye)]} + Pc ye,
    P = Pc(y-ye).

Here epsilon and P are energy density, rho is rest-mass density, and V is specific energy. Pc=a0²/(8 pi G) gives the previous hydrostatic family. This is a definite choice of the formerly arbitrary energy-zero function, not a deduction that the original field selects it. The positive Pc ye term is a physical vacuum-like contribution within the material branch. The exterior is separately specified vacuum; the formulas are not extended through densities 0<rho<rho(ye).

The pressure follows from rho epsilon_rho-epsilon. Since rho_y>0, this defines a single-valued barotrope at fixed V and ye. Set h=epsilon_rho and Q=P_rho. Then

    h = c² + V[F(y)-F(ye)+sqrt(1+y)],
    Q = V (1+y)^(3/2)/(1+y/2) > 0,
    h-Q = c² + V {F(y)-F(ye)-y sqrt(1+y)/(y+2)}.

The last expression increases strictly with y, because

    d(h-Q)/dy = 4 V sqrt(1+y)/[y(y+2)²] > 0.

Consequently the **single boundary inequality**

    c² > V ye sqrt(1+ye)/(ye+2)

implies h>Q>0 for every y>=ye. The adiabatic relativistic sound speed satisfies 0<c_s²/c²=Q/h<1 on the entire branch. This is an analytic all-y statement under the fixed positive-state hypotheses, not an extrapolation from a sampled grid.

Energy conditions also hold on this branch. F is increasing, so epsilon>=rho c²+Pc ye>0, while P>=0. At the edge, epsilon-P=rho_e c²+Pc ye>0. Since d(epsilon-P)/d rho=h-Q>0, epsilon>P everywhere. Thus the perfect-fluid weak, null and dominant energy inequalities follow. These local constitutive conditions do not settle gravitational or interface stability.

In the Newtonian Euler--Poisson point-baryon equilibrium used by CFG2, V=sqrt(G M_b a0)/2 and ye=G M_b/(a0 re²). The pressure is exactly a0 M_b(1/r²-1/re²)/(8 pi), and the rest-mass density remains the P2 density. Mass is retained outside re. This does not establish the same radial profile as an exact Einstein/TOV solution, where energy density and pressure gravitate. A uniform weak-field approximation also cannot extend to the singular point center. The causal inequality is easily checked for any supplied host and edge. It selects an admissible domain, **not** re: neither this inequality nor current conservation determines the material functions V(s), ye(s), or their host correlation. Those are still extra initial/constitutive information.

At P=0 the fluid has a finite density jump to the separately declared exterior vacuum. Pressure continuity avoids a prescribed pressure jump, but a complete action must specify its material domain and moving boundary and match the gravitational equations. Vacuum conversion, merging, entropy production, finite-mass equilibrium stability and a phase transition cannot be inferred from the local EOS proof. The global cosmological cold abundance is likewise not supplied.

This is the strongest constructive constitutive result here: a conserved-current action can realize a positive-energy causal finite-density P2 fluid branch once its state and energy normalization are supplied. It upgrades the earlier equilibrium-only statement while leaving the zero-extra-input and formation requirements explicit.
