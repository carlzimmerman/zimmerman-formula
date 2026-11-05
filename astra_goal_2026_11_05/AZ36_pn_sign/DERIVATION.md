# Exact radial signs; the full nonspherical claim remains open

This is a conditional theorem about the vacuum spherical radial principal
block, plus a covariant frozen-matter consistency check. It is not the
complete Solar-System perturbation operator. Kappa = 1/2 FITTED; not theory
closed. The scalar matter's independent perturbations are not eliminated.

## Covariant reduction

In unitary gauge tau=t use

    ds² = -N²dt² + A²(dr+b dt)² + r²dOmega²,
    P^t=0, P^r=w/A, Q=1/N, s=D.P=(w'+2w/r)/A.

N,A,r are positive. The action has beta=eta=gamma_F=0, xi=1. The script
computes the3D Christoffel symbols and Ricci tensor directly and verifies

    R3 = 2(1-A^-2)/r² + 4A'/(A³r).

The radial and angular mixed extrinsic curvatures are

    k_r = (A_dot/A - b A'/A - b')/N,
    k_t = -b/(Nr).

Thus KijKij-Ktrace²=-4k_r k_t-2k_t². After one radial integration by parts,
the Einstein shift-dependent density (angular4pi omitted) is

    L_shift^GR = r b A_dot/(K N) - r D b²/(2K N),
    D = A' + A N'/N.

The discarded term is the exact radial derivative -[Arb²/(2KN)]'.
The static gravitational and polarization action is

    L_static = N A r² R3/(4K) + r²w N' - N A r² W(Kw)
             - N A r² gamma s²/2
             + A r² mu²(1-N)²/(2K N) + L_m.

This uses the open switched branch s>0. There is no two-sided Hessian at
s=0. No PN expansion was made in these formulas.

## Background constraints and the matter cancellation

Let rho_m and p_r denote the normal-frame static energy density and radial
pressure. Their first variations give E_N^m=-Ar²rho_m and E_A^m=Nr²p_r.
The exact static Euler-operator combination is

    E_N - (A/N) E_A
      = rD/(K A²) - A r² [B_tau + rho_m+p_r],
    B_tau = s + gamma s² + mu²(1-N)/(K N²).

W cancels in this combination. On a background satisfying both Einstein
equations,

    D=K A³ r [B_tau+rho_m+p_r].

It would be wrong to insert this into the vacuum shift expression while
omitting the matter shift Hessian. For an explicit minimally coupled
static scalar chi(r), arbitrary potential V,

    L_m = -NAr²[(A^-2-b²/N²)chi'^2/2 + V],
    rho_m+p_r = chi'^2/A²,

so L_m adds +A³r²(rho_m+p_r)b²/(2N). Consequently the actual denominator
in this frozen-scalar sub-block is

    D_eff = D-KA³r(rho_m+p_r) = KA³r B_tau.

The script verifies these identities without assigning V or W. Eliminating
b gives L_kin=T_A A_dot²/2, with

    T_A = r/(K N D_eff) = 1/(K² N A³ B_tau).

For gamma>0, s>0,0<N<=1, B_tau>0, so T_A>0 exactly. In the vacuum exterior
this is a gravitational-sector statement, independent of a matter model.
With matter present it is only the declared sub-block until delta chi and
any other matter perturbations are included.

If D_eff=0, b is a multiplier enforcing A_dot=0; division by D_eff is
invalid. In particular Schwarzschild with no P and no K(Q) has A=1/N,
D=0 and R3=0. It does not acquire an infinite-kinetic radial scalar.

## Spatial principal Schur complement

Integrating the EH static density once gives

    L_GR,static = N(A+1/A)/(2K) + rN'/(KA)

up to the documented radial derivative. For local high-frequency radial
amplitudes a=delta A, p=delta w and n=delta N, the principal block can be
written, after choosing relative Fourier phases, as

    L_pr = -g k² p²/2 + k n(c_a a+c_w p) + h n²/2,
    g=N gamma r²/A,
    c_a=r/(KA²), c_w=-r²(1+gamma s),
    h=Ar²mu²/(K N³).

Changing all cross-term signs by a Fourier phase does not change the Schur
complement. Crucially, lapse and polarization are retained until this
elimination; dropping h would drop K(Q)'s contribution.

Sequential elimination and direct inversion of the2x2 constraint block
give the same radial gradient coefficient:

    G_A = c_a²/(h+c_w²/g)
        = N gamma / [K² A^5 ((1+gamma s)²+gamma mu²/(K N²))].

The physical radial speed is the coordinate speed multiplied by A²/N²:

    c_rad² = (A²/N²) G_A/T_A
           = gamma B_tau / [(1+gamma s)²+gamma mu²/(K N²)].

Under the stated hypotheses this is positive. In vacuum with mu=0, writing
y=gamma s yields exactly y/(1+y)=y-y²+O(y³). Thus the omitted radial
correction reduces the leading PN speed but cannot reverse its sign.
At gamma->0 the leading radial gradient term vanishes. These limits are
checked symbolically. For positive gamma the denominator minus numerator
is1+gamma s+gamma mu²/(K N)>0, so this radial propagating root is also below
the local metric light speed. That does not settle instantaneous constraints.

## What does not follow

1. The Solar System is embedded in a Galactic external field, so its adopted
   background is not spherically symmetric. The areal-gauge one-field
   reduction has no transverse metric/polarization block, no arbitrary-angle
   propagation and no tensor/scalar mixing. A nonspherical background does
   not inherit the theorem merely because GM/(c²r) is small.
2. The calculation controls the high-frequency radial principal signs,
   not the finite-wavelength potential operator or all global eigenvalues.
   The W Hessian and background derivatives can enter those missing terms.
3. It assumes an exact static background obeying the constraints. The
   finite coefficient grid is not a new background solve; N,A,s are local
   coefficient values satisfying the theorem's sign hypotheses conditionally.
4. The matter shift cancellation is exact in the declared static scalar
   completion; treating its frozen sub-block as the full coupled spectrum
   would be an error. Real solar fluid perturbations remain a separate block.
5. Neither the switch interface nor moving/rotating sources is covered.

The next full-PN calculation is the constrained second variation on the
actual nonspherical screened background, retaining shift/lapse, transverse
polarization, metric tensor perturbations and the relevant matter variables.
Its physical kinetic and gradient operators must be compared with their
PN limits after constraint elimination. The radial result supplies a known
answer for that calculation, not a substitute.

## Self-review

The geometric invariants are computed directly. The shift integration,
background equations, matter cancellation and spatial Schur complement each
have an independent identity check. The scalar matter completion was added
before computation (A1). The Schur complement is checked by two elimination
routes. The degenerate GR limit is treated before dividing. The mode scope
is kept distinct from the full claim. This is adversarial self-review,
not an independent-agent review.
