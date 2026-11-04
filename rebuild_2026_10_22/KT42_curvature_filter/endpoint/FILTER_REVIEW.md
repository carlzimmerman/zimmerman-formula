# Independent review of the KT42 MW curvature-filter action

**Verdict: correct only after the stated frozen-coefficient and finite-domain
restrictions.** The inspected implementation differentiates its declared finite
energy with the full adjoint. Its backward-Euler operator approaches a Gaussian
as the heat-step count increases. A positive filter width bounds the frozen
cold-fluid high-frequency growth caused by the Hessian sector; it does **not**
prove stability, full variable-coefficient well-posedness, or observational
viability.

Review by `/root/audit_dynamic_options`, separate from the author of the MW
implementation, 2026-11-04. This is an independent read-only algebra/code review
and provenance validation. No MW field solve was independently rerun. Exact
reviewed hashes are in `FILTER_REVIEW_HASHES.json`.

## Reviewed object and dependencies

The inspected `mw/filtered_model.py` retains the unfiltered gradient D psi and
replaces the compatible Hessian by H T psi. Here D and H are the KT37/KT39
finite derivative maps, W is the diagonal volume weight, and

    T_m = (I - a^2 L/(2m))^(-m), L=g.Lap.

The phantom energy is

    E_ph = -(1/(8 pi)) sum W e(D psi,H T_m psi),

with the unchanged KT39 p9/8 response and ell3 kpc. Its coefficient definitions
give delta e=2 A.delta g+2 sum multiplicity_i B_i.delta H_i; the off-diagonal
Hessian component has multiplicity2. The ordinary Newtonian potential is added
separately. `generalized_v3.py` supplies the compatible spherical Hessian and
its angular weighted divergence. `power_model.py` supplies A,B,e without
changing these linear maps.

## Finite adjoint and action

For the declared W inner product,

    T_m^dagger = W^(-1) (I-a^2 L^T/(2m))^(-m) W.

`Heat.adjoint` multiplies by W, applies the repeated transpose LU solve, then
divides by W, exactly in this order. This remains the correct adjoint even
before assuming W L is symmetric. The symmetry is separately measured in the
check run, rather than substituted as an excuse to omit the adjoint.

The derivative of the energy is

    delta E_ph = -(1/(4 pi)) <D^dagger A
                    +T_m^dagger H^dagger B,delta psi>_W.

Consequently the implemented source

    b = -D^dagger A-T_m^dagger H^dagger B

satisfies delta E_ph=<b,delta psi>_W/(4 pi). Its `second` array is the full
existing H^T W multiplicity B assembly, including mixed and connection terms.
`filter.adjoint(second/W)` is T_m^dagger H^dagger B. The required transpose
order is present. The outer filter does not belong on the unfiltered-gradient
A contribution; omitting it from the B contribution would fail this variation.

Since psi=4 pi L^(-1)rho and L is W-self-adjoint with the fixed homogeneous
boundary implementation, the functional derivative with respect to density is
Phi_ph=L^(-1)b, exactly the inherited `phantom` and `response` sequence.
Thus reciprocal density response follows from the energy. This reasoning
concerns the finite energy and its declared boundary operator; an incompatible
continuum boundary prescription would define a different model.

## Frozen continuum symbol: mixed terms cancel

Let T be an isotropic, real, even scalar Fourier multiplier t(k), independent
of the fields. Freeze the real second derivatives of a C2 energy E(g,Hbar) on
one background. For a plane wave along a unit n,

    delta g = i k n delta psi,
    delta Hbar = -k^2 t(k) nn delta psi.

Define

    K=E_gg[n,n]/2, N=E_HH[nn,nn]/2,
    C=E_gH[n,nn]=E_Hg[nn,n].

In the Hermitian second variation, the two mixed contributions are
`+i k^3 t C |delta psi|^2` and `-i k^3 t C |delta psi|^2`, so they cancel.
The pure terms are k^2 E_gg[n,n] and k^4 t^2 E_HH[nn,nn]. The linearized
potential response is therefore

    delta Phi_hat = [K+N k^2 t(k)^2] delta psi_hat.

K and N are evaluated on the filtered model's background fields; they are not
assumed numerically equal to the old unsmoothed background values. The ordinary
Newtonian contribution is included in K when E denotes the full energy.

For the continuum heat/Gaussian multiplier t=exp(-a^2 k^2/2),

    T_response(k)=K+N k^2 exp(-a^2 k^2).

For the actual finite-m backward-Euler multiplier in the translation-invariant
continuum surrogate,

    T_response,m(k)=K+N k^2 (1+a^2 k^2/(2m))^(-2m).

The finite spherical grid has its own spectral and boundary errors; the
continuous wave-number formulas are not exact eigenvalues of that mesh.
Variable coefficient derivatives, boundaries, complex/odd multipliers,
state-dependent filter widths and noncommuting tensor filters require new
analysis. This cancellation is not a license to drop mixed terms in the full
inhomogeneous numerical variation.

## What is bounded, and what remains unstable

For a>0,

    max_(k>=0) k^2 exp(-a^2 k^2) = 1/(e a^2),

at k=1/a. For an integer m>=1,

    max k^2(1+a^2 k^2/(2m))^(-2m)
       = (1/a^2)[(2m-1)/(2m)]^(2m-1),
    k_peak^2 = 2m/[a^2(2m-1)].

The latter approaches 1/(e a^2). In the ordinary cold continuity/Euler closure,

    omega^2 = -4 pi G rho0 T_response(k).

Thus for fixed finite K,N,rho0 and a>0, the Gaussian case obeys

    gamma^2 <= 4 pi G rho0 [max(K,0)+max(N,0)/(e a^2)].

The bound is uniform in k on that frozen background. It is not uniform over
unbounded families of K,N,rho0, or as a tends to zero. If K>0, the limiting
short-wave cold growth remains the finite ordinary Jeans rate
sqrt(4 pi G rho0 K), and long-wave instability may remain too. The filter
removes the particular unbounded k growth, without establishing stability.
Finite sound speed adds cs^2 k^2 to omega^2 but also requires its own
background/matter consistency checks.

## Existing finite checks inspected

The current `checks_003/manifest.json` passed the installed validator with
`--root`, status **completed**, unchanged input/output hashes. Recorded checks:

| Check | Recorded error |
|---|---:|
| Heat W-adjoint pairing | 1.600e-15 |
| W L symmetry | 5.705e-17 |
| Best full-energy directional derivative | 1.277e-11 |
| Zero-width recovery of KT39 source | 1.288e-16 |
| Best density-response reciprocity | 3.707e-7 |
| Largest tested analytic Gaussian error, widths.3/1, m32/64/128 | .00237646 |

The Gaussian benchmark convolves a width2-kpc spherical Gaussian and compares
at r<10 kpc, away from the outer boundary. At width1, errors decrease from
.00237645 through .00122172 to .00064032 as m32,64,128. This is persuasive
heat-step convergence on that benchmark, not a uniform-error bound for every
MW field or a substitute for spatial/boundary refinement. Response reciprocity
passes its registered 1e-6 gate at step1e-4; step1e-5 has larger cancellation
error2.367e-6 and does not pass individually. The contract uses the best step.

The original m16 Gaussian benchmark failed the same .004 gate in
`checks_002`; it is retained. The reviewed m32/64/128 version changes numerical
resolution, not that physical or numerical tolerance. Neither a successful
finite test nor an adjoint proof certifies any subsequent scan or its physics
cuts; those result records must be reviewed separately.

## Obligation matrix and remaining gap

| Obligation | Status |
|---|---|
| Full finite energy derivative and correct outer adjoint | passed analytically and in recorded finite checks |
| Mixed-term cancellation for real even scalar T, frozen real coefficients | proved under stated hypotheses |
| Gaussian/finite-m frozen high-k bounded growth | proved under stated hypotheses |
| Exact Gaussian kernel on the finite mesh for finite m | false; an approximation with recorded benchmark error |
| Stable cold matter from bounded growth | not established; generally false when K>0 |
| Variable-coefficient global well-posedness | not addressed |
| Complete relativistic or microphysical action | out of scope |
| New MW/Cassini/EFE viable window | separate numerical/physical obligations |

The cheapest next discriminator is the fixed-baryon static-force/virial screen
already underway, with heat-step and spatial refinement on a candidate if one
exists. A merely bounded symbol cannot repair a failed static force by itself.
