# Independent focused review of the physical finite-k response

2026-10-19. Reviewer: sibling occupations lane, fresh derivation of the
source projection and static coefficients. Review requested by the parent.
The author's coefficients were supplied as the audit target, so this is
independent calculation, not a blinded review. No source/action file is edited.

**Normalized claim and verdict: proved as written within the expressly
declared n=1 common-density fluid approximation and constrained COM frame.**
The physical common source has a positive internal susceptibility

\[
 \chi_D(k)=\frac{R^3}{G}
 \left[\left(\frac{2}{9\pi^2}-\frac4{189}\right)(kR)^4
             +O((kR)^6)\right].
\]

This is not a verification that the common-profile baryon closure follows
from the original action, a finite-GP convergence theorem, a dynamical mode
spectrum, nonlinear saturation, or a selected occupation/normalization.
Those limitations are already stated in the reviewed record.

## Revision and evidence audited

Observed Git HEAD: `aa0d1a83d15c1fe2a0c9d32f189bdbbff49dd19a`.
Files are concurrent research artifacts; the exact reviewed bytes are:

- `finite_wavelength/FINITE_WAVELENGTH.md`: SHA256
  `beda1ae428681f9c53412b13c2450fe932709f65fffb8a1e524727d96df7f03c`.
- `finite_wavelength/check_response.py`: SHA256
  `6dc4037400897326bb7e5b4d53b2f5f5de97531db33df9c9fd7be4eff2fe3cfd`.

The computation-audit v2 validator was run against
`finite_wavelength/run_002/manifest.json` with the project root. It reports
`valid evidence record (run status: completed)`. Its actual stdout reports
29 checks, `C_smallk=0.0013517974231650083`,
`modal_l1_64=0.04055314763231677`; stderr is empty. The recorded run used
45-second wall, 30-second per-process CPU, 65536-byte logs and one-thread
limits, taking 0.345 seconds. I inspected the implementation and result,
but did not rerun it: the independent evidence below is analytic and the
existing run's hashes validate. Binary64 quadrature is not certified arithmetic.

## Source, constraint and signs

Let the quadratic energy be
`E2=K int(delta rho)^2-(G/2) int int delta rho delta rho'/|x-x'|`.
For applied potential `Ue=-E f` and COM constraint `int z delta rho=0`,
stationarity gives `2K delta rho+delta U-E f-lambda z=0`.
Defining `H=delta U-E f-lambda z` therefore gives
`delta rho=-H/(2K)`. With `G=R=1,K=2/pi`, Poisson's equation implies
`(laplacian+pi^2)H=-E laplacian f`. This checks both the sign of the
source and the factor of two from the quadratic energy. The source is
conjugate to `D=int rho f`, and a positive susceptibility follows from a
positive constrained Hessian; reversing the source sign would be erroneous.

For `h_k=sin(kz)/k`, its first two odd multipoles are

\[
 h_k=rP_1-k^2r^3(P_1/10+P_3/15)+O(k^4r^5).
\]

This follows from `z^3=r^3(3P1+2P3)/5` and the sine Taylor series.
The whole `rP1` observable is zero on the COM-constrained variations.
The physical `r^3P1` compression is not zero. Eliminating all l=1
perturbations would miss part of the response. The leading source for the
remaining internal problem is of order `k^2`, so its quadratic susceptibility
is of order `k^4`. This is a common Newtonian mass source; no species-only
force or replicated host is introduced by the projection.

## Independent l=1 cubic calculation

For `f=r^3P1`, `laplacian f=10rP1`, and the regular solution is
`H=[A j1(pi r)-10Er/pi^2]P1`. The self-potential is
`delta U=H+E r^3P1+lambda rP1`. Since the induced total mass dipole is
constrained to zero, its exterior l=1 potential is zero; continuity at the
surface requires both its value and its derivative to vanish. Using
`j1(pi)=1/pi` and `j1'(pi)=-2/pi^2` gives

\[
 A=2\pi E/3,\qquad \lambda/E=10/\pi^2-5/3.
\]

The independent COM check is
`int_0^1 r^3 j1(pi r)dr=3/pi^3` and `int_0^1 r^4 dr=1/5`, so
`int r^3 delta rho dr=0` exactly. For the conjugate cubic moment,

\[
 \int_0^1r^5j_1(\pi r)dr=5/\pi^3-30/\pi^5,
\]

which follows directly from `j1(x)=sin(x)/x^2-cos(x)/x` and integration
by parts. Multiplying the density moment by the angular factor `4pi/3`
gives

\[
 \chi_1=20/(3\pi^2)-40/63>0
\]

in these units. The dimensional factor is `R^7/G` because the observable
is a cubic mass moment and the source potential is `-E r^3P1`.

## Independent l=3 cubic calculation and normalization

For `f=r^3P3` the source is harmonic, so `H=A j3(pi r)P3`.
The exterior self-potential decays as `r^-4P3`. Its matching condition is
`delta U'(1)+4delta U(1)=0`. The recurrence
`x j3'(x)+4j3(x)=x j2(x)` and `j2(pi)=3/pi^2` give
`A=-7pi E/3` with the author's sign. Finally

\[
 \int_0^1r^5j_3(\pi r)dr=j_4(\pi)/\pi
 =105/\pi^5-10/\pi^3.
\]

Including `4pi/7` from `int P3^2 dOmega` gives
`chi3=(105-10pi^2)/(3pi^2)>0`, again times `R^7/G`.
Angular orthogonality eliminates a cross term. The squared source
coefficients are `1/100` and `1/225`, so

\[
 C=\chi_1/100+\chi_3/225=2/(9\pi^2)-4/189.
\]

For a cell volume `4piR^3/3`, multiplying `chi_D/V` by `4piG`
therefore gives exactly `3C(kR)^4` to leading order. In particular the
cell-volume convention and its factor three agree with the claimed
normalization. A separate population's filling fraction must still be
included. The result cannot equal a wavelength-independent unit coefficient
in its controlled small-`kR` limit.

## Independent COM-projected eigenbasis check

The radial Newton-kernel eigenfunctions in l=1 are `j1(n pi r)`.
Write `s_n=(-1)^n` and `q_n=n pi`. Direct integration gives

\[
 z_n=-3s_n/q_n^3,\quad
 f_n=s_n(30/q_n^5-5/q_n^3),\quad
 \|j_1(q_nr)\|^2_{r^2dr}=1/(2q_n^2).
\]

The `n=1` coefficient costs zero quadratic energy because it is the
translation mode. It must be chosen to enforce the COM constraint.
Substitution into the source then replaces `f_n` by
`f_n-f_1 z_n/z_1`, rather than just deleting the first basis function.
With Hessian eigenvalues `2K(1-1/n^2)`, each term is

\[
 t_n=\frac{4\pi}{3}
 \frac{(f_n-f_1z_n/z_1)^2}{[1/(2q_n^2)]2K(1-1/n^2)}
 =\frac{600}{\pi^6}(n^{-4}-n^{-6}).
\]

Summing `n>=2` gives `600[pi^4/90-pi^6/945]/pi^6=chi1`.
Positivity and the integral test give
`0<sum_{n>N}t_n<600/(3pi^6N^3)`. Thus the stated finite-N correction
is mathematically justified; the original tolerance failure did not refute
the fluid response. It would have been incorrect to call the N=64 sum the
infinite coefficient without accounting for this positive tail.

## Implementation and obligation matrix

- Physical source, COM projection and source signs: **passed**.
- Both cubic coefficients, angular factors and dimensional restoration:
  **passed** by the fresh integrations above.
- Full finite-k radial solver: **passed in the declared implemented range**.
  Its `c=k^2/(pi^2-k^2)` follows from applying the Helmholtz operator to
  each plane-wave multipole. Its l=1 boundary equations eliminate the
  same COM translation; l>=3 uses the correct exterior Robin condition.
- Partial waves l=1,3,5,7 at the six listed `kR`: **finite evidence only**.
  Modes l>=9 are not exhaustively checked or asserted absent. They cannot
  affect the analytically derived leading coefficient.
- Independent finite eigenbasis sum and analytic omitted tail: **passed**.
- Generic original-model equilibrium, finite-GP surface convergence,
  baryon EOS selection and nonlinear saturation: **outside this audit**.
- Occupied microscopic local dipoles or a universal acceleration scale:
  **not established** by this calculation, as the author states.

The cheapest relevant next check is comparison of the l=1 source-weighted
sum over *dynamical* shared modes with `chi1`, using the same physical
source and COM constraint. The static density-kernel eigenfunctions above
are not themselves that dynamical spectrum.
