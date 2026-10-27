# Independent focused audit of the occupied landscape

Primary verdict: **proved as written for the explicitly conditional analytic
reduced-model claims audited below**. Disposition: accept the final pinned
note; no remaining mathematical correction is required in this scope.
Formation, baryon support, actual soft-pair lifetime, a stable bath, a
controlled continuum reduction and universal normalization remain unproved,
exactly as stated by the note. The numerical evidence is a finite floating
control, not a proof of those physical hypotheses.

Reviewer: separate particle_saturation agent. This is an independent
reconstruction by a peer who developed a different spatial-mode projection,
not a blind review with a different model family. The parent supplied audit
focus areas. I read the complete raw final note, current executable,
contract and run_004 manifest/results, plus the superseded run_003 executable
snapshot and evidence. No scientific run was repeated and no source file
outside this review was edited for the landscape audit.

## Frozen inputs and version disposition

The original request named run_003. During review the parent confirmed that
run_004 supersedes it and adds the two-1s LCAO control. The executable
snapshot check_landscape_run003.py has the exact historical hash recorded
for check_landscape.py by run_003, preserving its executed bytes despite
the subsequent executable revision. Current run_004 is the live evidence.
The loading energy notation was clarified during review; the final note
below explicitly defines its full r-dependent one-body level center.

| Artifact relative to occupied_landscape/ | SHA256 |
|---|---|
| LANDSCAPE.md | `d62f206214f3f5d8e10f8d245f16d27b3538c2f1ec742f4102ef32a87873aa5e` |
| check_landscape.py | `1f707334bdd436ef3dc3b74ba4c89d3f3857d137d60406cef5f3ae1b4221a72d` |
| contract.json | `9d0aa71ad8d58178b9b74a0fe887d077bde49f1c6237a303d3cb779ffc656bcf` |
| source_pins.json | `17cb75d398d7ab5038753be862e93a8d1dd0a3757b97375c237fffea0d0a2a35` |
| run_004/manifest.json | `b161a967e5bdf3f30f581f022c1bae4ffdcb4a6fa9d52d6c013814aab463704d` |
| run_004/results.json | `b717851918fdbd8d70d6b9ce545513a1fa73c0f39d914e5ff03adce6b68489ff` |
| check_landscape_run003.py | `7924641205e0cca82d35b1e20bcb94f4aa042475bd0d39b5ca22fd069ba19e2a` |
| run_003/manifest.json | `34135296b22ad3bc5acd9e6d191278e66d5ca438de00589ef281e25e55693e28` |
| run_003/results.json | `6ec74f44efed661a198d43dd9a8d9a57c5612e61c4fe82342d419d980e4e5b42` |

Observed repository HEAD in the live runner manifest is
`e54c33252909e38a529a69f7adac265e37b54cb4`, with a dirty shared workspace.
The note's action/matching antecedents are pinned separately in its
source_pins.json; this review does not alter them.

## Normalized claim and dependency graph

The quantified reduced-model claim is: for the stated mutual-nearest-neighbor
selection from a homogeneous 3D Poisson snapshot, fixed-level two-center
scalar orbitals, complete COM source, and the stated hard-core pair trace,
the available/conditional occupied measure has the derived geometry,
source, loading and soft-tail properties. For a separately assumed supported
phonon bath, the retained density coupling has the stated spectral power
and conditional Golden Rule rates. No implication is asserted from the
bare action alone to existence or abundance of this environment.

Dependencies are:

1. Original matched daughter contact and minimal positive-mass gravity
   (pinned antecedent input).
2. Poisson landscape and disjoint mutual pairs (declared state plus exact
   empty-volume geometry).
3. Fixed binding level, BO/rigid pair, separated orbitals and their explicit
   two-1s Galerkin matrices (declared projection plus direct integrals).
4. Full daughter/baryon recoil coordinate and physical sin(kz)/k source
   (exact within that BO coordinate).
5. Single-captured-sector or hard-core local reservoir trace (declared
   occupation model plus exact finite trace).
6. Pushforward, rare-void estimate and inverse-gap moment bounds (internal
   analytic consequences).
7. A separate stable, locally sound-like fragmented scalar bath and weak
   density coupling (additional conditional input), followed by continuum
   integration and a further Markov/secular approximation for rates.

There is no circular step using the target weight or 1/(4piG) to choose a
landscape intensity, occupation, action or matrix element.

## Obligation matrix and decisive reconstruction

| Obligation | Disposition | Independent reconstruction and limits |
|---|---|---|
| Disjoint host counting | Passed | A tagged point can be in only one mutual-neighbor pair. Empty union volume is9pi r³/4. Unordered pair intensity is(n_b²/2)4pi r²exp(-b r³)dr, so n_pair=8n_b/27 and used node fraction16/27. The pair process need not be independent. |
| Physical source and COM | Passed | Daughter coordinate alpha q and baryon coordinates-beta q plus/minus r e/2 give m alpha=M beta. Summing all three sine sources yields the displayed D_k(q), and its affine operator is exactly zero. |
| Recoil packet width | Passed | The 1s characteristic F(t)=[1+(a_G t/2)²]^-2 multiplies both scalar and baryon recoil exponentials. Treating only the mean baryon shift omits a real width contribution. |
| Finite-k expansion | Passed | Expansion gives mu_r k²[(1+beta)s³/3-a_G²(alpha-beta)s/2]+O(k⁴). In particular beta²-alpha²=-(alpha-beta), which fixes the width term's sign and factor. |
| Finite-overlap source | Passed | The primitive product phi_L phi_R is even while D is odd, so its cross element vanishes. Normalized even/odd states give d_LCAO=abs(d_signed)/sqrt(1-S²). The note distinguishes this from the pre-orthogonal localized expectation. |
| LCAO gap and level center | Passed | Generalized eigenvalues are(H00+H01)/(1+S) and(H00-H01)/(1-S). Half their difference is E_H(CS-K)/(1-S²); their mean is E_H[-1/2+(C-SK)/(1-S²)]. This verifies the final loading dictionary. |
| Hard-core loading trace | Passed conditionally | With onsite n_L,n_R in{0,1}, sectors0,1,2 have energies0, E_b(r) plus/minus J,2E_b(r)+V. Their grand trace gives exactly the displayed Z and f1. The physical hard-core hierarchy and reservoir are hypotheses. |
| Attractive interwell energy | Passed in stated leading regime | The contact cross energy is2g2 int rho_L rho_R; the direct gravity is-Gm²/r plus exponentially small overlap corrections for fixed localized packets. Finite-host and relaxed-host corrections are explicitly not claimed to be negligible at every extreme endpoint. |
| Single-sector window and optimum | Passed | Comparing the grand energies gives E_b-J<mu_Q<E_b+V+J. The width is V+2J. Maximizing f1 over fugacity gives z*=exp(beta V/2) and f1max=cosh(beta J)/(cosh(beta J)+exp(-beta V/2)). Polynomial attraction eventually dominates exponential J in this projected approximation. |
| Exact exponential pushforward | Passed | x=log(2J0/Omega) yields rho_Omega=3B x²exp(-Bx³)/Omega. The subsystem diagnostic d=D xi x adds the factor d and Jacobian xi x/[Delta(1+x)], yielding x⁴/(1+x), not a raw gap density. |
| Physical reduced-gap soft tail | Passed | Bounded full source implies Delta<delta only if r>xi log[J0/(delta dmax)]. Integrating the Poisson survival law gives the stated log-cubic upper bound. Form-factor zeros and multiple roots cannot increase this cumulative bound. |
| No rational cusp in this family | Passed | At fixed nonzero k, every inverse-J moment times a bounded power of d is finite because exp(-b r³) dominates exp(c r). Dominated low-field expansion through cubic order follows for a field-independent captured f1. This does not imply a convergent full Taylor series or exclude other disorder families. |
| Phonon spectral coefficient | Passed conditionally | Angular average sin²(q.r_D/2)=[1-sinc(qr_D)]/2. With epsilon/E=q/(2m c_s), radial DOS gives gamma² n0 E³[1-sinc(E r_D/c_s)]/(8pi²m c_s^5), hence coefficient gamma² n0 r_D²/(48pi²m c_s^7) for E^5. |
| Bath limitations and occupations | Passed | The Jeans subtraction, finite supported patch, sound window, fragmented same-species projection and neglected number-changing terms are declared. The Golden Rule rates preserve detailed balance but do not determine capture f1. J=0 does not imply population equilibration. |
| Universal normalization | Correctly left open | The response still depends on host density, preparation, contact/orbital data and the physical k-dependent source. No calculation sets4piG chi_k=1. |

The mutual-pair identities can also be checked directly by integrating
r²exp(-b r³): its integral is1/(3b), so2pi n_b²/(3b)=8n_b/27.
The contact factor2 follows by evaluating the local interaction on the
normalized identical-boson state a_L†a_R†|0>; it is not a distinguishable
particle density approximation.

For the orbital formulas, in prolate coordinates the product of translated
1s functions is exp(-x mu)/(pi a_G³), the volume element is proportional
to(mu²-nu²), and division by a center radius cancels one factor(mu plus/minus
nu). The remaining elementary integrals give the displayed S and
K=-(1+x)exp(-x). The direct potential C follows from the spherical 1s
charge integral. Thus the two-1s gap is tied to the stated Newtonian
potential, while remaining a trial-subspace splitting.

## Loading notation issue resolved during review

The original isolated level in the WKB control is a fixed E_b=-E_H/2.
A loading calculation across different separations must instead use the
full projected common one-body diagonal E_b(r), including attraction to
the other baryon center. Its leading separation shift is algebraic and
cannot be silently discarded beside exponentially small J. The final
pinned note now explicitly makes this distinction in section 4 and beside
Eq (5), with the exact LCAO center written above. This resolves the only
substantive notation/application ambiguity found. No loading-control run
needs changing: it tests a generic four-sector Hamiltonian with a supplied
diagonal energy. The T=0 window width V+2J is independent of the common
one-body shift.

## Actual computation/provenance audit

I ran only the installed read-only manifest validator:

`python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/nonlinear_origin_2026_10_19/occupied_landscape/run_004/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula`

It returned a valid evidence record with run status completed. I did not
rerun check_landscape.py. The recorded run took 0.261243 s, with 45 s wall,
30 s process CPU, one conventional numerical-library thread and 1048576
log bytes; memory and affinity were not hard-capped.

The implementation covers exactly the contract's finite lists: one Poisson
density, five transformed x values, seven WKB separations, five LCAO
separations, four small-k points, four bath energies and four interwell V
values. It does not sample a population, solve a halo, compute a capture
rate or establish infinite-family asymptotics by finite enumeration.

Important numerical limits are honest: generalized eigenvalue subtraction
is compared with the LCAO closed gap only through x=20; x=40 uses the stable
closed expression because the raw split is below reliable subtraction
precision. The analytic asymptotic ratio there is .9990625. Sphere-slice
integration is an independent geometry check; finite-difference Lambert-W
inversion checks the reduced-gap Jacobian; explicit Fock diagonalization
checks the sector trace. The bath E^5 result is checked against radial
Bogoliubov dispersion and angular quadrature. The final small-k coefficient
relative error is 6.94e-7 and bath low-energy coefficient error 1.81e-6.
Neither SciPy quadrature estimates nor eigensolver success are interval
proof certificates.

Outcome label: **implementation and finite assertion verified in the stated
range, conditional on the recorded floating tolerances and libraries**.
The analytic rare-event/source arguments, rather than the finite success
flag, support the stated conditional asymptotics.

## Primary-source cross-check and exact scope

I checked [Cirone et al., arXiv:0909.2166v2](https://arxiv.org/html/0909.2166v2)
on 19 October 2026. The official v2 HTML identifies the four authors and
30 October 2009 revision. Equations (17),(28)-(30) give the spatial coupling,
sine-squared well-separation suppression and interacting-condensate
frequency power d+2. Their separate species and external traps differ from
this scalar model, and their solved zero-tunnelling dynamics is dephasing.
This verifies the narrow power/form-factor cross-check, not capture,
Markov equilibration, a stable gravitating bath or the same-species
fragmented-mode coefficient gamma=2g2. That coefficient and the displayed
noise normalization were reconstructed directly above. No source PDF was
retained; the first PDF fetch failed, while exact-version official HTML
was accessible. No novelty claim was audited.

The remaining original-state obligation is therefore physical construction:
a supported correlated baryon environment, lifetime and detuning selection,
controlled localized modes and actual capture/exchange kinetics. This
accepted conditional route supplies no universal no-go and does not close
the original normalization or rational-response target.
