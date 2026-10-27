# Independent review of the n=1 self-gravitating TF bridge

Reviewer: `self_gravity_dipoles`, independently assigned by `/root`.
Reviewed file:
`sol61_push/scalar_dipole_bridge_2026_10_19/virial_normalization/VIRIAL_NORMALIZATION.md`.
SHA-256: `febe978ddd8813db3b8da63ea3879da9048688b77828f393e1f866f6f2cc5bfe`.
Mathematical parent: CE087. Review date: 19 October 2026. No reviewed file was
edited. Scope includes the full note, with independent reconstruction of the
tidal coefficient, the quadrupole-to-polarization projection, and TF stability.

**Primary verdict: proved as written**, for the note's stated Newtonian
Thomas-Fermi density-perturbation model and separated-object, long-wavelength
ensemble. The original two-field model application remains conditional on a
coherent dilute daughter state and a controlled TF-to-GP continuation, as the
note expressly says. In particular this review does not certify an actual
occupied population, an acceleration-driven internal dipole, or a Love-number
error bound for a finite quantum-pressure surface layer.

## Claim card and dependencies

The normalized claim is: for `p=K rho^2`, `K>0`, the regular compact spherical
`n=1` Newtonian TF equilibrium of fixed positive mass has nonnegative
mass-preserving quadratic density energy, with its sole density zero directions
being translations, and its adiabatic STF susceptibility is
`Q_ij=-lambda_T E_ij`, where

\[
 \lambda_T={15-\pi^2\over3\pi^2}{R^5\over G}.
\]

For separated identical objects with uniform number density `n_o`, retaining
only their STF quadrupole response, the induced bookkeeping field has
`chi_eff=n_o lambda_T k^2/3`. In terms of geometric filling `f`,
`4 pi G chi_eff=[(15-pi^2)/(3pi^2)]f(kR)^2`. These statements are not the
desired local internal acceleration dipole law.

Dependencies are: threshold-matched one-component GP input and valid state
(declared assumptions) → TF equation of state → regular equilibrium and
Poisson boundary matching → STF susceptibility; TF fixed-mass quadratic energy
and its angular/radial spectral decomposition → density stability;
mass-moment multipole expansion plus STF divergence → ensemble response.
No appeal to the desired rational law enters any of these implications.

| Obligation | Assessment |
|---|---|
| Matching `g2=lambda_rep/(2m^2)` to `K=lambda_rep/(4m^4)` | Passed as the supplied matched input; no bare source-only coefficient substituted |
| n=1 radius, mass normalization, energies and homology factors | Passed by direct differentiation/integration and dimensions |
| Static quadrupole boundary conditions, sign and factor | Passed by independent reconstruction below |
| Moment tensor versus apsidal Love convention | Passed; exact primary convention checked |
| Quadrupole source to effective P and `k^2` suppression | Passed by tensor differentiation below |
| Mass-preserving TF density Hessian, translation exception | Passed on the declared regular tangent class |
| Full nonlinear, finite-temperature or two-field stability | Out of scope and not claimed |
| GP surface-layer continuation and Love-number convergence | Conditional; not established by the TF calculation |
| Formation, occupied hosts and universal a0/spectrum | Not addressed; accurately retained as missing bridges |
| Finite numerical implementation and provenance | Passed in the declared finite range; validated manifest |

## Independent derivation of the decisive tidal coefficient

The regular TF profile follows from `2K rho+U=constant` and Poisson:
`Delta rho+(2piG/K)rho=0`. Its first zero gives `2piG/K=pi^2/R^2`.
For the axisymmetric source with `Ezz=e`, `Exx=Eyy=-e/2`, the imposed
potential is `(e/2)r^2 P2`. Linear hydrostatics sets

\[
 \delta\rho=-{H\over2K},\qquad
 H=A j_2(\pi r/R)P_2,
 \quad\delta U_{\rm self,in}=H-(e/2)r^2P_2,
 \quad\delta U_{\rm self,out}=Br^{-3}P_2.
\]

Continuity of potential and radial derivative at the free surface gives

\[
 {B\over R^3}=Aj_2(\pi)-{eR^2\over2},\qquad
 -{3B\over R^3}=A\pi j_2'(\pi)-eR^2.
\]

Adding these equations yields
`A[pi j2'(pi)+3j2(pi)]=5eR^2/2`. The bracket is `pi j1(pi)=1`;
`j2(pi)=3/pi^2`. Thus
`B=eR^5(15-pi^2)/(2pi^2)`.

For the note's STF moment, `Qij n_i n_j=Qzz P2` in this axisymmetric sector,
and the exterior Newtonian moment potential is `-3GQzz P2/(2r^3)`.
Consequently `Qzz=-2B/(3G)` gives exactly the displayed `lambda_T`, including
its sign. Independently the angular integral is
`int P2(cos theta)(cos^2 theta-1/3)dOmega=8pi/15`, which confirms the direct
moment coefficient used in the computation. There is no factor-of-two or
factor-of-three mismatch between the tensor and exterior-potential conventions.

The regular first-order surface displacement introduces no surface delta
mass because `rho_0(R)=0`. Using the unperturbed radius in these first-order
potential matching conditions is therefore valid. This is the TF free surface,
not a claim about a discontinuously truncated GP wavefunction.

## Independent quadrupole-to-P calculation

The second moment gives a coarse source `delta rho=(1/2)partial_i partial_j
S_ij`, with `S_ij=n_o Q_ij`. The choice `P_i=-(1/2)partial_j S_ij` therefore
has `delta rho=-div P`. With uniform `n_o`,

\[
 \partial_j\mathcal E_{ij}
 =\partial_i\nabla^2U-\tfrac13\partial_i\nabla^2U
 =\tfrac23\partial_i\nabla^2U,
 \qquad P_i={n_o\lambda_T\over3}\partial_i\nabla^2U.
\]

For `grad→ik` and `g=-grad U`, this is
`P_i=(n_o lambda_T/3)k^2 g_i`, with positive susceptibility. Multiplying by
`4piG` and inserting `n_o=3f/(4piR^3)` gives the note's coefficient exactly.
The source density is `-n_o lambda_T Delta^2 U/3`; it is of fourth derivative
order in potential. This is a derivative-dependent quadrupole response, not
an `O(k)` internal mass-dipole source. In a uniform vacuum-harmonic region
`partial_j E_ij=0`, so the leading bulk bookkeeping polarization vanishes
even though the individual objects deform. Spatially varying population and
boundaries fall under the explicit derivatives in the general formula.

The stated restriction to the STF response is necessary: a plane-wave
potential is generally traceful and also probes a separate radial/trace
channel. The note retains that qualification, so its calculation neither
omits a claimed component of `chi_eff` nor establishes a bound on every
possible compressional response of a many-body medium.

## TF stability scope

For `l>=1`, the Newton potential operator in the ball has the decaying exterior
matching condition `x j_l'(x)+(l+1)j_l(x)=x j_(l-1)(x)=0`. Its eigenvalue is
`4piG R^2/x^2`, so the energy coefficient is indeed
`K[1-pi^2/x^2]`. The lowest `l=1` root is `pi`, and its density profile is
proportional to `-a.grad rho_0`: an exact translation, not a new internal
polarizer. Higher roots are positive-energy directions. For `l>=2`, the
regular Dirichlet radial equation for `x j_(l-1)(x)` has increasing angular
barrier, so the first zero is bounded below by the first `j1` zero `x1>pi`.

For `l=0` the fixed total mass removes the exterior monopole. With enclosed
perturbation mass `q(r)`, the energy is
`K/(4pi) int q'^2/r^2 -G/2 int q^2/r^2`. The regular weighted Dirichlet
eigenfunction `q=r^2 j1(x1 r/R)` gives the least quotient `x1^2/R^2`.
Substituting the TF radius produces strict positivity. The quoted
`0.51118136` is the dimensionless **density energy** comparison gap; it is
not a claim that all dynamical squared frequencies equal that number.

Together with positive velocity energy this excludes exponentially growing
finite-energy linear density modes in this TF model. Relabeling/vortical
zero modes, free COM drift and translations do not contradict that statement.
The argument treats regular mass-preserving interior tangents and smooth
free-surface deformations; it is not a nonlinear global stability theorem
for arbitrary exterior additions or shocks. The note expressly disclaims
that stronger result. The exact TF profile has an inadmissible divergent
kinetic integral if inserted literally into full GP, so its continuation
and the static tidal limit require the stated separate surface-layer input.

## Source, finite computation and residual gap

I inspected the current code, inputs, result and manifest; the validator
reported `valid evidence record (run status: completed)`. The code's regular
ODE transformation, boundary quotient, direct mass moment and Bessel checks
implement the declared finite assertions. The nine ODE checks cover exactly
`l=2,3,4` at three tolerances. The strict general stability conclusion is
carried by the analytic spectrum argument, not those nine samples. I did not
repeat a numerical run because the existing passed checks and independent
algebra already settle the requested review obligations.

I authenticated and read the exact primary PDFs
[Yagi–Yunes arXiv:1303.1528v3](https://arxiv.org/pdf/1303.1528v3), equations
(49)–(51), (78)–(81), and
[Chavanis arXiv:1103.2050v2](https://arxiv.org/pdf/1103.2050v2), equations
(35)–(44). They agree with the limited equilibrium and Love-convention
comparisons in the note. No source PDF was retained; no retained-file hash
is claimed. This check does not import a general GP or microscopic stability
theorem.

The strongest safe result is an internally consistent, stable TF shape
polarizer with exact tidal inverse-G coefficient and a controlled separated-
object quadrupole suppression. The missing implication is from this tidal
operator and unselected host population to a physical local acceleration
dipole spectrum and rational law. The cheapest next physical check is a
finite-GP equilibrium plus its adiabatic l=2 response across the surface layer;
it would test transfer of this established TF response, not repair an error
in its coefficient. Review provenance is an independent sibling derivation;
agreement is not a formal proof certificate.
