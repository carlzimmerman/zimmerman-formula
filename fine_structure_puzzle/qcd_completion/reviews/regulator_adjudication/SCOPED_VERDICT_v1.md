# Scoped independent analytic adjudication

2026-10-19 UTC. **Analytic-only; no computation contract or run is claimed.**
The independent raw derivation was saved before reading the two targets or
receiving a candidate coefficient. This note audits only their common-PV and
dimensional-regulator electric/magnetic difference, the exact local electric
oscillator check, the Coulomb IBP surface and associated tail signs, and their
stated physical scope. It does not audit their literature claims, previous
computations, GPY derivation, magnetic coupling conversion, or whole phase.

## Normalized claim and verdict

For connection-normalized SU(2), `tr(Ta Tb)=delta_ab/2`, background Feynman
gauge, charged frequencies `w_n=2pi n/L+h`, and fixed `0<nu=Lh/(2pi)<1`, define

`Gamma_1,2 = integral d^3x [K_B(h) B^2 + K_E(h)(grad h)^2]`

with no extra factor `1/2`. Subtract the identical vector/ghost determinants
with a common positive four-dimensional mass-squared `M^2`, before taking
`M -> infinity`. The fully integrated-by-parts bulk difference is

`K_E-K_B = c`, `c=L/(24pi^2)`.

The common-PV local diagonal density instead has

`K_B B^2 + (K_B-c)E^2 + A(h) Delta h`,
`A(h)=(1-2nu)/(12pi)`,

and differs from the bulk density by `div[A(h) grad h]`. The two
representatives must retain the corresponding surface functional on a region.

**Primary verdict: proved as written**, for this normalized claim and the
targets' associated Coulomb-tail correction and surface signs. This verdict
does not extend to every claim in either target document.

## Exact artifacts reviewed

All paths below are relative to `fine_structure_puzzle/qcd_completion/`.

| Artifact | SHA-256 at review |
|---|---|
| `far_field/ADDENDUM_2026-10-19_COMMON_PV.md` | `234dc4a55e2cfe7ff007e2a2c525285f2d19f087399b001b6d734bc187acba18` |
| `reviews/far_field/ADJUDICATION.md` | `108e0db3e4fd36a92b7d13fb7624e0628507569fe5afd6e3cfbb8694d94d4235` |
| `reviews/regulator_adjudication/four_dimensional_pv_raw_v1.md` | `50d53d2c4b04b6c540cac3114d894c943da8267ad6cc45aebf82ba19235583d3` |

The coordinator supplied the target locators only after the raw derivation
was saved and its result sent. The coordinator's own report was hashed but
its content was not read or relied on. Its hash at that time was
`63043cb705eadea568b1d37ac1857ad951375dc063acfbb2cdb74a0d5ea13f90`.
No target or executed artifact was edited. Only this permitted review
directory was written by this agent.

## Dependency graph and decisive evidence

The determinant convention implies one charged-pair contribution
`tr_D log(K delta+S)-2 log K` for each `n in Z`. Thus its orbital multiplicity
is `D-2=d-1`; the spin trace is `-4 I_2(B^2+E^2)`. Here

`I_2(m)=(4pi)^(-d/2) Gamma(2-d/2)m^(d-4)`,
`I_3/I_2=(4-d)/(4m^2)`.

The electric scalar bubble uses the vertex `2w delta h`, including in the
PV determinant, and yields the bulk coefficient `(2/3)w^2 I_3`. The magnetic
scalar coefficient is `I_2/6`. Consequently, at `d=3`, the regulator alone has

`(K_E-K_B)_reg = -M^2/[24pi(w^2+M^2)^(3/2)]`.

The physical-minus-regulator difference is therefore positive. Its sum is
absolutely convergent at finite `M`, and the rescaled Riemann sum tends to
`L/pi` times the prefactor `1/(24pi)`. This proves `c=L/(24pi^2)`.

Independent analytic branch: for `d=3-2epsilon` and `D=d+1`,

`K_E-K_B = [(d-1)(3-d)/6] sum_n I_2(|w_n|)`.

The large-frequency tail gives
`sum I_2=L/(16pi^2 epsilon)+O(1)`, while the prefactor is
`2epsilon/3+O(epsilon^2)`. Their product gives the same `c`. This identifies
precisely the finite term lost by specializing each mode to `d=3` before
summing. No numerical extrapolation or source attribution is needed.

The exact local electric oscillator gives, for scalar mass
`m^2=w^2+M^2`,

`Kscalar(x,x;s)=(4pi s)^(-3/2) exp(-sM^2)`
`  *sqrt[2Es/sinh(2Es)]*exp[-w^2 tanh(Es)/E]`.

Its expansion has factor
`1-E^2s^2/3+w^2E^2s^3/3+O(E^4)`.
Multiplication by the exact vector-minus-ghost spin weight `2cosh(2Es)`
gives the local diagonal coefficient

`K_E,diag(w,M)=-11 I_2/3 + [M^2/(3m^2)] I_2`.

After the physical-minus-PV subtraction, its difference from magnetic is
`-c`. The scalar diagonal/bulk identity

`Lscalar_diag = (2/3)w^2 I_3 E^2 + div[(w I_2/3) grad h]`

converts it to the bulk answer. In the regulated charged-pair sum the
coefficient of the divergence tends to `A(h)` above. Thus the oscillator
confirms the target's distinction; an `M=0` oscillator calculation alone
could not have tested the common-PV finite term.

### Supplemental direct magnetic bubble

The raw note used the magnetic heat kernel. A direct transverse scalar bubble
checks the same coefficient without adding a source assumption. Its quadratic
`A_i A_j` kernel is

`delta_ij I_1(m) - (1/2) integral_p
 (2p+k)_i(2p+k)_j/[(p^2+m^2)((p+k)^2+m^2)]`.

After a Feynman parameter and a shift, contract with a transverse external
field. Rotational integration and
`integral l_i l_j/(l^2+Delta)^2 = delta_ij I_1(Delta)/2`
reduce the scalar multiplier to

`I_1(m^2)-integral_0^1 dx I_1(m^2+x(1-x)k^2)`
` = k^2 I_2(m)/6+O(k^4)`.

Here `I_1` is interpreted with the same background-consistent regulator or
dimensional continuation, so the displayed rotational IBP relation is valid.
Since `B^2=k^2 A_T^2` at this order, the coefficient is `I_2/6` as used.

## Coulomb tail and boundary check

On the annulus `r0<r<R`, take `h=v-1/r`, so `E^2=r^(-4)` and
`Delta h=0` away from the excluded core. The positive common-PV bulk correction
contributes

`delta Gamma_bulk = 4pi c(1/r0-1/R)`.

Thus its inverse-radius coefficient is `-L/(6pi)` in Gamma and `+L/(6pi)`
in the log weight. This agrees with both targets.

The exact local-minus-bulk outer surface is

`4pi R^2 A(h(R)) h'(R)=4pi A(v-1/R)`
` =4pi A(v)+L/(3pi R)`.

The inner surface must be kept separately. The outer inverse-radius surface
coefficient is `+L/(3pi)` in Gamma, agreeing with both targets. Therefore the
common-PV local diagonal bulk-only coefficient differs from the harmonic-first
one by `+L/(6pi)` in Gamma, whereas the fully IBP bulk-only coefficient differs
by `-L/(6pi)`. The opposing signs are required by the boundary identity.
Pointwise `Delta h=0` does not remove the divergence: it leaves
`A'(h)E^2=-2cE^2`.

Conditional only on the targets' separately established GPY inverse-radius
logweight term `+L/(3pi)` and their displayed magnetic harmonic coefficient,
adding this audited electric correction gives their corrected loop number

`L/(2pi)-11L(1+n_mag^2)F(nu_v)/(12pi)`.

This last arithmetic consequence is checked; this scoped review does not
rederive the GPY input or magnetic matching. The center-holonomy substitution
`F(1/2)=4log 2` gives the displayed `-22L log 2/(3pi)` magnetic-plus-common
kinetic term for unit magnetic tail.

## Obligation matrix

| Obligation | Status | Basis |
|---|---|---|
| Charged real-adjoint/vector/ghost factors | passed | Explicit charged-pair determinant and `D-2` orbital count |
| Massive regulator electric vertex | passed | `delta(w^2+M^2)=2w delta h+(delta h)^2` |
| Magnetic scalar and spin factors | passed | Direct bubble/heat kernel and Lorentz trace |
| Common-PV finite difference | passed | Convergent positive sum and analytic Riemann limit |
| Dimensional-regulator finite difference | passed | Explicit evanescent factor and UV pole residue |
| Exact local constant-electric kernel | passed | Harmonic-oscillator diagonal and spin-weight expansion |
| Local-diagonal/IBP conversion | passed | Explicit differential identity with `A'(h)=-2c` |
| Coulomb inverse-radius signs | passed | Elementary annular integral and outer surface evaluation |
| Full corrected loop number | conditional on named inputs | GPY and magnetic harmonic terms not reaudited here |
| Full finite-wall spectral determinant | not addressed | Requires operator domains, BCs, and boundary heat-kernel terms |
| External source formula adjudication | out of scope | Targets' literature record was not independently checked |
| Physical alpha/QCD/stress conclusion | out of scope | No such bridge or observable follows from this calculation |

## Strongest safe conclusion and remaining gap

The stated common-PV bulk electric correction and its dimensional/oscillator
checks are correct. The corrected addendum and the independent adjudication
both preserve the necessary distinction between local diagonal, IBP bulk, and
full action with boundaries. Their qualified physical scope is appropriate:
a holonomy mass that screens E removes this electric operator's algebraic
large-radius tail, while a full finite-wall determinant still needs boundary
data. Neither off-shell local number establishes a physical coupling bridge,
vacuum stress, or alpha.

No gap remains in the narrow normalized common-PV claim audited here. The
separate source-to-regulator matching issue recorded by the targets is neither
settled nor contradicted by this review. The cheapest useful next check, only
if the phase later needs a finite-wall observable, is to specify an operator
domain and retain its boundary functional in the same regulator. Repeating
strictly three-dimensional per-mode coefficient checks cannot settle that
different question.

## Provenance and final self-review

Review provenance: independent raw analytic derivation first, followed by a
target comparison; this report's proofreading is self-review. The raw file is
unchanged. No mathematical computation was executed; no source browsing was
needed. Executed shell inputs after the raw save were bounded path discovery,
`cat` on the two targets, SHA-256 hashing of the listed artifacts, and reads of
the proof-audit checklist and proofread-math skill. No existing run/manifest
was re-executed or certified by this agent.

Proofread: the new raw derivation and this scoped verdict, prose and displays.
Routine edits: none. Mathematical-token changes: none. Unresolved proofreading
issues: none. Validation: analytic formula/sign/normalization review, with
artifact hashes captured; no compiler or numerical validation applies to these
Markdown analytic notes. The targets remain unchanged. This scoped review is
frozen at version 1.
