# Fresh bounded atomic-bridge review

Primary verdict: **conditional on named inputs**. The normalized algebraic claims below pass within their stated microscopic or EFT assumptions. None establishes a quantum microscopic completion, a fully matched Standard Model, or a numerical prediction of alpha.

Reviewer: fresh subagent `/root/atomic_phase_review`, 2026-10-19 UTC. Revision: `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty shared tree. The central steps were independently derived from the raw action and displayed functions. No coordinator review or self-review file was opened. **Verdict-blindness limitation:** an initial section-locator search exposed hydrogen REPORT line 201, which mentions coordinator checks, before the derivations. This review therefore supplies fresh derivations but does not claim perfect isolation from prior-check summaries. Raw reports were read because they contain the target hypotheses and formulas; their author interpretations are not independent evidence.

## Claim card and dependency graph

1. S2, continued to reciprocal microscopic rest-mass sources, has a high-wave-number pair correction `+G m_e m_p r/L_*^2` after a common constant is subtracted. With fixed masses and an alpha-independent medium functional, a stable atomic ground-energy minimum cannot have an interior stationary point in positive alpha. The explicit global isotropic screened continuation has the stated fixed-angular-momentum radial perturbation bound.
2. In the stipulated shared-scalar truncation B6–B15, the physical common threshold and electron amplitude can vary across theories while preserving nucleon mass, the leading Coulomb size–mass product and vacuum energy; alpha then varies. Fixing the threshold removes this particular rank defect.
3. Granting the asymptotic de Sitter QCD-vacuum ansatz and the declared leading matching functions, the SI matching equation, local electromagnetic null tangent and independent-light-quark-mass positive control follow.

The dependency graph is: frozen static S2 + **unproved microscopic/reciprocal/adiabatic continuation** -> pair kernel -> Coulomb expectations and fixed-l bound; fixed-mass common-domain variational problem -> monotonicity. Separately, **stipulated B6/B7 functions and physical free threshold/Yukawa** -> finite scalar counterfamily and rank. Separately, **conditional QCD cosmological ansatz + specified chiral/QED matching** -> SI equation and Jacobian results. No branch supplies the bold physical leaves.

## Obligation matrix

| Obligation | Status | Decisive reason / restriction |
|---|---|---|
| S2 variation and reciprocal normalization | Passed | Vector Laplacian and one cross term in `1/2 rho Phi`; no doubled pair force. |
| Local correction sign and coefficient | Passed | Fourier kernel `-4 pi G/(lambda^2 k^4)`, with `lambda^2=L_*^2/2`, transforms to `+G r/L_*^2`. |
| Physical applicability to an atom | Conditional | S2 has a baryonic continuum source, not an operator-valued electron/proton source or quantum high-frequency susceptibility. |
| No alpha selection by atomic energy | Passed | Fixed masses, medium parameters and common admissible domain; positive nuclear Coulomb kernel and an attained stable ground minimum. |
| Screened radial remainder | Passed | Global isotropic `A>0`, point sources, radial sectors, `C<Delta/2`; not a bound for a general nonlinear anisotropic medium. |
| Scalar curvature signs B8/B15 | Passed | Direct differentiation agrees; B15 is stable only for `p>4a` and then lies below its constant uplift. |
| Finite scalar counterfamily B9/B10 | Passed | Positive `t<R_0/(4 pi k_gamma)`, within a common valid EFT window; varies physical threshold and Yukawa data across models. |
| Scalar rank defect and fixed-threshold control | Passed | Rank-three minor `-1/(1+r)` and augmented determinant `a/(1+r)>0`. |
| QCD SI restoration | Passed, conditional premise | Uses energy density versus mass density consistently and the asymptotic de Sitter branch. |
| Electromagnetic QCD null curve | Passed | Invertible `(Lambda,q)` minor on the stated regular domain gives a local alpha-parameterized curve. |
| Independent-q positive control | Passed as generic local statement | Its determinant can vanish on a special surface; nonzero determinant gives local identifiability, not a global unique root. |
| Real-QCD matching values, de Sitter coefficient, electron Yukawa | Not addressed | External physical inputs remain uncomputed; no source or numerical spectrum certification is implied. |

## Decisive independent derivations

For S2, variation gives

`div(grad Phi-KP)=K rho`,

`grad Phi-KP=R(u) P_hat-gamma Delta P`.

For the isotropic linear response, `grad deltaPhi=K(1+A+lambda^2 k^2)deltaP`. Eliminating `deltaP` gives

`Phi(k)=-K rho(k)/k^2 [1+1/(A+lambda^2 k^2)]`.

Using `Delta r=2/r` in three dimensions fixes the distributional normalization `F^{-1}(1/k^4)=-r/(8 pi)`, up to the constant and exterior matching conventions. Thus the local correction is positive and its force is attractive. Its pair coefficient follows from the two equal cross terms cancelling the factor one-half. An anisotropic bounded Hessian changes higher orders of the large-k expansion, while global regular matching terms still require their own boundary data.

For `A>0`, the exact correction is `-G m_e m_p(1-exp(-qr))/(A r)`, where `q=sqrt(A)/lambda`. Subtracting its origin constant gives

`W=C[1-(1-exp(-qr))/(qr)]`, `C=G m_e m_p q/A`,

so `0<=W<=C` and its linear coefficient is `Cq/2=G m_e m_p/L_*^2`. This constant subtraction cancels from transition energies; it does not fix a physical ionization threshold. If `P_n` projects onto an isolated radial Coulomb eigenstate and `Q=1-P_n`, the Schur complement bounds the remainder by

`||QW P_n||^2 / dist(E,spectrum(Q(H_0+W)Q)) <= C^2/(Delta-2C)`.

Here spectral perturbations are at most `C` and `|E-E_n|<=C`. The relevant fixed-l gaps are `3 E_h/8` for 1s and `5 E_h/72` for 2s. The 2s/2p Coulomb degeneracy is harmless only because this perturbation is radial and angular-momentum sectors decouple. The `A->0` pointwise local limit is allowed; the bounded global norm argument is not uniform in that limit.

For alpha monotonicity, the same minimizing atom/medium state at `alpha_1` is an admissible trial state at `alpha_2>alpha_1`. Its energy decreases by `(alpha_2-alpha_1) hbar c <K_charge>`, with `K_charge>0`. This proves strict ground-energy decrease independently of differentiability. A stationary-point envelope derivative gives the same sign when defined. No general monotonicity theorem for atomic radius under every alpha-independent medium operator is claimed here.

For the scalar bridge, B9 gives `Lambda(0)=M/C_N` and

`m_e(0)=M/[R_0/(4 pi k_gamma t)-1]`.

Consequently `R=4 pi k_gamma t(1+M/m_e)=R_0`, `m_N=M`, and `U_0-C Lambda(0)^4=rho_DE`, while `alpha=1/(4 pi k_gamma t)` varies. The entire QCD scalar profile is unchanged. Differentiating the constraints in `(B_*,ln M_U,ln y,U_0)` gives the reported rank-three matrix and null vector. Appending the fixed physical threshold row gives determinant `a/(1+r)`, so the finite family's direction is no longer admissible. The vacuum curvature is preserved, but a term `-beta p n_e m_e` makes total finite-density curvature vary if `n_e` is fixed and nonzero. Nor does the family preserve a separately measured electron/nucleon mass ratio.

For B13, writing `X=A exp(-p x_*)` and `Y=C Lambda_0^4 exp(-4a x_*)`, stationarity is `pX=4aY`. Hence `V''=p(p-4a)X` and `V-rho_0=(1-p/(4a))X`. Equal exponents require the separately stated constant-potential or no-stationary-point alternatives.

For QCD SI units, the posited natural-unit energy density restores as

`Delta epsilon=c_H H Lambda_energy^3/(hbar^2 c^3)`.

Combining it with `H^2=8 pi G Delta epsilon/(3c^2)` gives

`H=(8 pi/3) G c_H m_Lambda^3 c/hbar^2`.

Then the framework relation gives exactly

`a_0 hbar^2/(G c^2 m_p^3)=k_kappa sqrt(8 pi/3) c_H/C_p^3`.

This derivation requires the assumed vacuum-dominated asymptotic state; replacing its H by arbitrary-epoch H_0 is unjustified.

Let `h=1+v alpha` and `D=C_0+c_gamma alpha-2c_q q/Lambda`. Direct differentiation of `H=d q Lambda^2 h` and `m_p=(C_0+c_gamma alpha)Lambda+c_q q` gives the `(Lambda,q)` minor `-d Lambda^2 h D`. At `delta alpha=1`, `delta H=0` first gives

`delta q=-q(2 deltaLambda/Lambda+v/h)`.

Substituting into `delta m_p=0` yields exactly the reported `deltaLambda`. Thus the implicit-function theorem supplies a local finite curve, not merely a formal null vector, whenever `h D !=0`. In a physical expanding positive-mass neighborhood one must additionally retain `h>0`, `m_p>0`, positive masses/coupling, the fixed quark-mass convention and validity of the truncation. With q independently fixed, the determinant is `d q Lambda^2[2c_gamma-C_0v+c_gamma v alpha]`, generically nonzero but not everywhere nonzero.

## Source/computation audit and exact remaining gap

Source code inspection found the declared mathematical operators and formulas in `hydrogen/compute.py`, `scalar_bridge/check_scalar_bridge.py` and `qcd_mass/discriminator_v2.py`. The hydrogen code evaluates tiny effects through derivatives and high-precision rescaling rather than subtracting unresolved binary64 total energies. The scalar and QCD scripts check exact identities in their declared truncations; their checks do not compute unknown physical functions. No existing suite was rerun and no new mathematical computation or scan was executed. Computation outcome: **audited, not executed**. Quoted numerical hydrogen values and previous run manifests were not independently recertified by this review.

All eight raw input files and their SHA-256 hashes are listed in `INPUTS.json`. Whole-file hashes cover exact bytes even where only the specified sections were read. Parent revision is insufficient alone because the artifacts reside in a dirty tree. The current input hashes were rechecked after writing this review. External theorem/source claims were not independently authenticated; in particular the QCD cosmological term remains a named conditional input.

The strongest safe conclusion is that these particular static/leading models do not obtain an independent alpha-selection equation from the tested atomic or vacuum constraints while their stated physical inputs remain free. Fixed-threshold scalar and fixed-quark-mass QCD controls explicitly leave open conditional selectors. The next decisive obligations are a microscopic reciprocal dynamical response for atomic sources, independently fixed physical threshold/Yukawa data with full matching for the scalar, and computed QCD cosmological/hadronic matching functions with independently specified quark masses. More precision in the present algebra would not supply those inputs.

Self-proofreading covered this new review only: notation and prose checked; no source mathematical tokens changed. No source files were edited.
