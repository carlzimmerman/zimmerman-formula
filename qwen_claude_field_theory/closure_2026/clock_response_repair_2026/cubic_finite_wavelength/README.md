# Same-action finite-wavelength scalar dynamics

Base `ebb49936640781e220c7b28ac4369acf36b46711`. The preceding turn made
progress: action-derived homogeneous and principal-wave results were committed.
This checkpoint advances the **same** cubic clock candidate, not a new fitted
kernel. The complete relativistic MOND goal remains **OPEN**.
The physical motivation follows Carl's primordial-clock direction; the cubic
operator itself is known and is not credited as a newly discovered interaction.

## Action and approximation

Use the covariant action and fixed reconstructed functions in
`../cubic_background_completion/README.md`:

    S = int sqrt(-g) [M²(R-2Lambda)/2 + P(X,tau)
          + sqrt(Xtau) W(Y,tau) - V(tau) + gamma X Box(chi)] + S_m.

The functions have not been adjusted after the previous tests. They remain
inverse reconstructions, not a first-principles selection of the action or
its coefficients. No exponential MOND law or a0–Lambda relation is derived here.

The new calculation is the **full quadratic scalar action at finite nonzero
spatial wavenumber**, not merely its highest derivative terms. It is still
linear perturbation theory about the specified homogeneous branch, with no
ordinary-matter perturbations in this scalar calculation. It is not a nonlinear
Dirac count or a proof of a global solution.

## Actual ADM variation

Set tau=t and use

    h_ij=a² exp(2 epsilon z cos(kx)) delta_ij,
    N=1+epsilon n cos(kx), N^x=epsilon b sin(kx),
    chi=chi_bar(t)+epsilon sigma(t) cos(kx).

`derive.py` constructs K_ij, spatial curvature, Q, Y and the exact ADM cubic
interaction, then expands and averages the action over a spatial period.
The lapse and shift Euler equations are solved from their actual Hessian.
The determinant in this shift convention is

    det(F_n,b) = -a^6 k² (M²H+gamma q³)².

An independent compact ADM derivation agrees identically before imposing any
background equation. That comparison is retained as an executable assertion.
At k!=0, Theta=H+gamma q³/M² !=0, the lapse is

    n = [M² zdot + gamma q² sigmadot + j sigma/2]/(M²H+gamma q³),
    j=2q P_X-6 gamma Hq².

After lapse/shift elimination, the **computed**, spatially averaged velocity
Hessian is

    K_red = a³ Bhat/(2 Theta²) [[q²,-qH],[-qH,H²]],
    Bhat=2P_X+4q²P_XX-12 gamma Hq+6 gamma²q⁴/M².

Its generic rank is one; the null vector is (H,q). The script calculates both
rank and nullspace. This is not an assumed N_grav. On singular Bhat or Theta
branches the generic-rank conclusion is inapplicable.

## Finish the remaining scalar constraint

Define u=sigma-(q/H)z. The transformation is time dependent; its derivative
and the a³ volume derivative are retained. Integrating the terms containing
zdot by parts gives

    L2 = A0 udot²/2 + J z udot + Braw u udot
         + D z²/2 + E z u + Craw u²/2,
    D=D0+D2 k²,
    D2=-a Sgamma/(2H²),
    Sgamma=W_gamma(0,t)-2q² W_Y(0,t).

All six coefficients are generated from the action. The exact rational
expressions are saved in the derivation output. Where D!=0, the remaining
Euler constraint is z=-(J udot+E u)/D, giving

    Aeff=A0-J²/D,
    Beff=Braw-JE/D,
    Ceff=Craw-E²/D,
    L_eff=Aeff udot²/2+Beff u udot+Ceff u²/2.

Consequently the finite-wavelength equation is

    Aeff uddot + Adot_eff udot + (Bdot_eff-Ceff) u = 0.

The mixed term cannot be dropped while treating its coefficient as constant:
Beff contains a k² term whose time derivative contributes to the gradient.
The script retains that derivative and **exactly** recovers the independently
derived principal speed of `../cubic_principal_audit/` as k tends to infinity.

This reduced linear system has one dynamical scalar on its regular divided
branch. It is the clock/matter mode, not a new certificate of the full theory's
nonlinear gravitational degree count. Spatially homogeneous k=0 modes must
instead use the separate homogeneous constraint analysis; the shift inverse
above is undefined there.

## Verification beyond the principal limit

`ConstraintSchur.lean` proves conditional statements: if A0>0, D0<0 and
D2<0, then for every real k²>=0, D<0 and Aeff>0. This excludes an extra pole
in this scalar elimination and establishes positive quadratic kinetic energy
under those hypotheses. It does not bound the mass term, prove stability of
every background, or supply a nonlinear constraint inverse.

`PointSigns.lean` goes further at the specified epoch a=1, gamma=1e-6:
it proves the three required signs from H>0, H²=4/15 and explicit exact
coefficient expressions. `point_certificate.py` reads those actual Lean
definitions and checks their equality to the action-derived coefficients
by polynomial remainders modulo H²-4/15, with exact rational denominator
bounds. No floating sample decides these signs. This supplies an exact
selected-epoch, all-nonzero-k quadratic kinetic/constraint certificate.
The action-to-Lean bridge is verified by symbolic Python, not a formal
Lean development of the covariant action or its variation.

`numerical.py` evaluates the actual coefficients at 37 epochs from a=1e-6
to 1e3 for gamma=0 and 1e-6. It tests the sufficient signs, and separately
evaluates 17 physical-wavenumber/Hubble ratios from 1e-4 to 1e4 at each
slice. The profile is independently integrated with DOP853 and Radau;
coefficient arithmetic uses 80 digits, but the profiles themselves are
floating ODE solutions, not certified interval enclosures.

It then integrates the actual canonical equations for k=1,10,100 from
ln(a)=-2 to 0, for both couplings. For p=Aeff udot+Beff u,

    udot=(p-Beff u)/Aeff,
    pdot=Beff(p-Beff u)/Aeff+Ceff u.

No time finite-difference approximation is needed for this integration.
Two independent solvers are compared, and preservation of the canonical
transfer determinant is checked. These matrices describe arbitrary normalized
canonical initial data, not observed cosmological transfer functions or
adiabatic primordial predictions. They are not a likelihood or data fit.

## Tensor sector from the same action

`tensor_gate.py` independently varies both transverse-traceless polarizations,
constructing the spatial connection and Ricci scalar directly. On homogeneous
clock backgrounds it obtains two positive tensor kinetic eigenvalues for
M²>0 and c_T²=1 for both modes. The clock terms have zero tensor variation
in the unimodular tensor parametrization. A curvature-deformation control
changes the computed speed, guarding against an assigned result. Full details
and the inhomogeneous-background exclusion are in `TENSOR.md`.

## Radiation without coefficient retuning

`../cubic_radiation_background/REPORT.md` varies an added minimal
C_r X_r² radiation action and derives local regular expanding branches with
unchanged P/W/V functions. Its fixed-scale and fixed-original-clock-charge
families are explicitly separated. This is a homogeneous perfect-fluid
radiation proxy, not the photon/neutrino free-streaming, recombination or
anisotropic-stress physics required for a CMB calculation. The old dust-only
history is not reused as a radiation solution.

## Remaining goal and next discriminating step

These gates advance the dynamics of a constructed clock sector. They do not
select its functions from a physical principle, derive the exponential MOND
law or kappa=1/2, settle full PPN, or explain galaxy/cluster dark-fraction
evolution. No new empirical or globally novel prediction is claimed.

The highest-priority missing connection is the **nonlinear baryon-sourced
galactic branch of this same action**, retaining its clock density and time
current. Independently, the new radiation branch needs full evolution and
coupled perturbations. A healthy free clock sector alone is not the target.

The mathbox research-program and computation-audit workflows determine this
checkpoint's bounded tests and provenance. Independent proof-audit derived
the raw action and its auxiliary block separately; proofread-math self-review
checked the scope, normalization and k=0 exclusions in this report.
