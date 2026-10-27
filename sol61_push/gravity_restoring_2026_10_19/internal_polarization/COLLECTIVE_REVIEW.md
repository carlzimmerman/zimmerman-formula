# Independent audit of the collective density/phase calculation

Reviewed source:
`sol61_push/gravity_restoring_2026_10_19/collective_response/COLLECTIVE_RESPONSE.md`,
25,068 bytes, SHA-256
`e7b87c2ba808a630fc8d9cfa60435192b1db955c9e221742bf3fa0861024366a`.
Scope: raw NR Hamiltonian through the density/phase Hessians, full boxed
susceptibility numerator, low-momentum mode assignment, charge-odd
instability, matched dilute miscibility condition, and density versus
nonlocal longitudinal-displacement spectral measures in Sections 1-5.
The author's code/numerical point, collisionless Section 6 and broader
program were not audited or rerun. This is a separate agent's reconstruction
from the displayed Hamiltonian, with shared project context.

**Claim card.** Under the declared conservative NR envelope theory,
equal-density coherent stationary state, leading reference-mass gravity
vertex and `k>0`, the displayed matrices and response follow from the raw
Hamiltonian. The odd block is dynamically unstable at sufficiently small
nonzero momentum, with a sound-branch identification only when its
conversion gap stays positive. Under a stable even block, the density and
inverse-derivative displacement operators have the stated different
one-phonon spectral weights. **Primary verdict: proved as written** for
these scoped analytic claims. This does not certify the coherent saddle as
the state produced by the original dynamics or the reference-mass vertex
as exact relativistic gravity.

## 1. Hessians reconstructed from the original NR energy

Write the grand-energy potential as

\[
 V_\mu=\sum_{\sigma=\pm}
 [(\delta-2\mu)s_\sigma-\mu n_\sigma
             -2c n_\sigma\sqrt{s_\sigma}]
       +k_c(n_+^2+n_-^2+4n_+n_-),
\]

at the phase-locked minimum and `s_sigma=beta²`. The same-species atomic
density curvature is `2 k_c`, the cross-sign atomic curvature is `4 k_c`,
the atomic/source mixed curvature is `-c/beta`, and the source-density
curvature is `c n/(2 beta³)`. Orthonormal even/odd rotation therefore gives
atomic entries `6 k_c` and `-2 k_c`, with unchanged source/mixed entries.
No conversion term has a second derivative with respect to atomic density
at fixed source density because it is linear in `n_sigma`.

Quantum pressure contributes energy `|grad delta n|²/(8 m n)` and
`|grad delta s|²/(8 M beta²)`. With the convention `energy=x^T A x/2`,
these add `z/(4mn)` and `z/(4M beta²)` to `A`. Thus both boxed `A_e`
and `A_o` are recovered without assuming them.

The phase-gradient energies give `z diag(n/m,beta²/M)` in `B`. The
conversion term expands as

\[
 -2cn\beta\cos(2\theta_a-\theta_b)
 =-2cn\beta+cn\beta(2\theta_a-\theta_b)^2+\cdots.
\]

Hence `B=z diag(d_a,d_b)+J vv^T`, with `J=2cn beta`, `v=(2,-1)^T`.
The common weighted number direction `r=(1,2)^T` obeys `r^T v=0`.
The density source is `sqrt(2) m r` only in the even block, as stated.

## 2. Inverse and full susceptibility numerator

Direct inversion gives

\[
 \det B=z[J(d_a+4d_b)+z d_ad_b],\qquad
 \operatorname{adj}B=Jrr^T+z\operatorname{diag}(d_b,d_a),
\]

which reproduces the boxed inverse. From
`L=-x^T theta_dot-x^T A x/2-theta^T B theta/2-source^T x`, the
equations are `x_dot=B theta` and `-theta_dot=A x+source`. Thus the
retarded density inverse is `A-s B^-1` with `s=(omega+i0)²`.

For `A=[[a,b],[b,D]]`, independently evaluate

\[
 r^T\operatorname{adj}(A)r=D+4a-4b=L,\quad
 \operatorname{tr}(AB)=JL+z(ad_a+Dd_b)=JL+zt,
 \quad r^TBr=zd.
\]

For a two-by-two matrix the adjugate is linear, and
`adj(B^-1)=B/det B`. Therefore multiplying the contracted adjugate of
`A-s B^-1` by `det B` gives

\[
 L\det B-s r^TBr
 =z\{d[JL-s]+z d_ad_bL\}.
\]

The susceptibility is consequently exactly

\[
 \chi_\rho=
 {2m^2z\{d[JL-s]+z d_ad_bL\}
  \over s^2-s[JL+zt]+\det A\,z[Jd+z d_ad_b]},
\]

including the stated numerator. At zero frequency it reduces to
`2m² L/det A`, with no leftover common-phase pole. At a fixed nonzero
frequency away from a pole its leading small-`z` term is `-2m² d z/s`.
If `A(0)>0`, the sound coefficient is `d det A(0)/L(0)` and
`rho_I=2m² d`. At the nonzero gapped root, the `O(z)` numerator cancels,
so its residue is `O(z²)=O(k⁴)`, under the stated nonzero distinct-gap
restriction. No static material `+K_G/z` term follows from this mode.

The Newtonian feedback sign also checks directly. Combining
`delta rho=-chi Phi_N` with `-z Phi_N=K_G(rho_b+delta rho)` shifts the
inverse by `-K_G/z`. It is attractive and yields the stated Jeans term.
The distinction between `rho_I` and the leading reference rest density
when `M!=2m` is explicitly an NR accuracy issue, not a new equivalence-
principle prediction.

## 3. Odd instability and its exact scope

At `z=0`, the odd atomic entry is `-2k_c`, so

\[
 \det A_o(0)=-{k_c cn\over\beta^3}-{c^2\over\beta^2}<0.
\]

For sufficiently small `z>0`, `B>0` and `det A_o<0` persist. The
frequency matrix is similar to the real symmetric matrix
`B^(1/2) A_o B^(1/2)`, whose determinant is negative. Thus exactly one
squared frequency is negative. If `J L_o(0)>0`, the nonzero conversion
root is positive and it is the sound root that is negative. If the gap
is negative it is instead the conversion root; a gap-closing boundary
needs its own expansion. The note correctly avoids extending the sound
label beyond its positive-gap regime.

The fully matched dilute comparison also checks. The same-charge contact
has relativistic normalization `-8m² g_same`, while the distinguishable
particle/antiparticle contact has `-4m² g_cross`. Threshold source exchange
therefore gives the stated

\[
 g_{\rm same}={\lambda_{\rm rep}\over2m^2},\quad
 g_{\rm cross}={\lambda_{\rm tot}-g^2/M^2\over m^2},\quad
 g_{\rm cross}-g_{\rm same}
 ={\lambda_{\rm rep}\over2m^2}+{4g^2\over M^2(M^2-4m^2)}>0.
\]

The density Hessian eigenvalues in the matched two-atom theory are
`g_same+-g_cross`; multiplying by `n/m` gives the displayed sound
coefficients. Global integrated neutrality permits zero-mean nonzero-
momentum odd perturbations and does not remove this instability. A
finite box or thermal entropy can change which modes/states are allowed;
the note marks these as different assumptions.

## 4. Operator-specific spectral measures

For `chi_rho=F_rho/(Omega²-s)`, a normalized harmonic oscillator has
one-quantum squared matrix element `F_rho/(2 Omega)`. With
`F_rho=rho_I k²+...` and `Omega=c_s k+...`, the density weight is
`rho_I k/(2c_s)+...`. The radial momentum measure and frequency delta
function add `k²/(2pi²)` and `1/c_s`. Substitution `k=Delta/c_s`
therefore gives

\[
 J_\rho(\Delta)={\rho_I\Delta^3\over4\pi^2c_s^5}+\cdots.
\]

The vector longitudinal displacement `P_L=-i k rho/k²` divides its
squared matrix element by `k²`, giving instead

\[
 J_{P_L}(\Delta)={\rho_I\Delta\over4\pi^2c_s^3}+\cdots.
\]

For the full single-component Bogoliubov comparator,
`Omega²=c_s²k²+k⁴/(4m²)`, define
`S=sqrt(c_s⁴+Delta²/m²)`. On its positive branch,
`k²=2m²(S-c_s²)` and `dOmega/dk=kS/Omega`. Hence

\[
 J_{P_L}={\rho_0 k^2\over4\pi^2\Omega}
            {\Omega\over kS}
         ={\rho_0 k\over4\pi^2S},\qquad
 J_\rho=k^2J_{P_L}.
\]

In a physically available particle-like NR window this gives
`J_P~rho0 m sqrt(2m)/(4pi² sqrt(Delta))`; extending that asymptotic to
arbitrarily high energy is outside NR control. The note correctly
distinguishes this squared-matrix-element measure from the dipole-
magnitude population weight of saturating two-level systems. Its momentum
integral is not automatically a local internal spectrum responding to a
spatially uniform source. A harmonic oscillator also has no saturation.

## 5. Minor wording correction and audit limits

Section 5 obstruction 2 calls `-q²E²/(2 I Omega²)` an energy lowering.
That quantity is the **ground-state energy shift**; the positive lowering
`F=e(0)-e(E)` is its negative. The induced displacement and all response
formulas are unaffected. This wording issue was sent to the author and
coordinator and is not a failure of the scoped analytic claims.

| Obligation | Assessment |
|---|---|
| Bare density/phase blocks from raw NRH | Passed by independent differentiation |
| Full retarded numerator and matrix inverse | Passed by adjugate reconstruction |
| Static, fixed-frequency and sound limits | Passed with declared gap restrictions |
| Odd instability | Passed; sound assignment correctly conditional |
| Matched dilute odd comparison | Passed with identical/distinguishable factors |
| Density versus nonlocal-P spectral weights | Passed including full Jacobian |
| Physical existence/preparation of coherent state | Not established, and not claimed |
| Numerical example and code manifest | Not audited or rerun here |

No external theorem or numerical assertion is load-bearing for this narrow
review: the matrix algebra, Hessian derivatives and spectral change of
variables are given above. Source edits after the pinned bytes require
their own reconciliation; the review does not silently certify later
versions.

## Reconciliation of the terminology correction

The corrected source is 25,078 bytes, SHA-256
`231d9e1e2a71539d9fd615a453463dff110cdbb9eae342c9cf36f9a147b972a5`.
Replacing its unique phrase `Its ground-state energy shift is` by
`Its energy lowering is` reconstructs the original reviewed SHA-256 above
exactly. Thus this reconciliation verifies that the only byte change was
the stated terminology correction. It resolves the minor issue without
changing any formula, hypothesis or scoped verdict.
