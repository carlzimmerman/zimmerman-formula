# Independent audit of the local obstruction and external-field virial

**Normalized claim.** For the local, instantaneous variational field law in
`dynamics/GENERAL_OBSTRUCTION.md`, a C² energy curve
`f(h)=E(g0,h nn)` that tends to a finite limit from above at least once has
`f''(h*)>0` at some positive-density rank-one jet. Ordinary pressureless
continuity/Euler matter then has an unbounded growing high-frequency branch
in the **frozen** system at that jet. Separately, the external-field curvature
term in `efe/MECHANISM.md` has negative scalar binding virial in its stated
asymptotic regime. A **negative total** binding virial excludes a stationary
gravity-only realization of the prescribed mass/tracer profile with
nonnegative kinetic stress and vanishing virial surface terms.

**Primary verdict: proved as written.** This verdict applies to those analytic,
conditional statements and their stated scopes. It does not certify the
finite numerical counts or identify an unstable observed galaxy. No
mathematical gap was found in the energy-curve implication, frozen symbol,
Euler sign, homology sign, or negative-total-virial implication. The two
wording clarifications below have been incorporated by the source owners
and do not change these results.

## Claim card and dependencies

- Domain: three spatial dimensions; real `g`; symmetric real `H`; `G>0`;
  `g0!=0`; `|n|=1`; `h>0`; `E` C² near every jet on the specified ray.
  Derivatives with respect to symmetric `H` use the Frobenius pairing.
- Convention: `g=grad psi`, `H=Hess psi`, `Delta psi=4 pi G rho`, and matter
  acceleration is `-grad Phi`. Thus positive `r.grad Phi` is attractive in
  the scalar virial convention.
- Exact conclusion: existence of at least one admissible local jet with
  `N(n)>0`, and exponential frozen-system growth asymptotic to
  `k sqrt[h* f''(h*)/2]`. This is not a statement about every background.
- Virial domain: centered fixed-mass homology at fixed uniform auxiliary
  external gradient, with the subtractions and decay specified in
  `efe/DERIVATION.md`. Equilibrium uses finite integrated kinetic stress and
  zero surface stress; it is not inferred from a positive computed virial.
- Recorded evidence: the obstruction is analytic; finite tensor checks and
  external-field quadratures are supporting computations, not leaves needed
  for the normalized analytic implication.

Dependency graph:

```text
C² ray + finite endpoint + one value above endpoint
  -> negative f' somewhere -> positive f'' somewhere             [internal]
  -> E_HH[nn,nn] > 0 and trace(H)=h*>0                            [definitions]
variational field equations + symmetric second variation
  -> delta Phi = (K + N k²) delta psi                            [internal]
Poisson + ordinary continuity/Euler + rho0>0
  -> gamma² = 4 pi G rho0 K + (4 pi G rho0 N - c_s²) k²           [internal]
  -> unbounded cold frozen growth                               [internal]

background-subtracted on-shell U + vanishing boundary terms
  -> delta U = integral Phi delta rho                            [internal]
fixed-mass homology
  -> dU/d(log lambda) = -W                                       [internal]
simple-Q primitive + controlled external-field expansion
  -> R'<0 -> U_H>0 -> W_H=-(6p-3)U_H<0 for p>1/2                [internal]
stationary momentum balance + nonnegative kinetic stress
  + zero virial surface term
  -> W_total >= 0; hence W_total<0 is incompatible                [internal]
```

There are no external-theorem or numerical leaves in this graph. The graph
does not use the obstruction as input to the virial argument or vice versa.

## Independent reconstruction of the decisive signs

Write the frozen second derivatives as `E_gg`, `E_gH`, `E_Hg`, and `E_HH`.
For `delta psi = u exp(i k n.r)`,

```text
delta g = i k n delta psi,
delta H = -k² nn delta psi.

Delta delta Phi =
  -(k²/2) E_gg[n,n] delta psi
  -(i k³/2) E_gH[n,nn] delta psi
  +(i k³/2) E_Hg[nn,n] delta psi
  -(k⁴/2) E_HH[nn,nn] delta psi.
```

The mixed contractions are equal by C² symmetry. Dividing by `-k²` gives
`delta Phi=(K+N k²)delta psi`, with exactly the positive sign in front of
`N`. No algebraic replacement of the Hessian field equation is made.

In the local comoving frame, continuity and Euler give

```text
delta rho_tt = rho0 Delta delta Phi + c_s² Delta delta rho,
delta psi_hat = -4 pi G delta rho_hat/k²,

delta rho_hat_tt =
  [4 pi G rho0 K + (4 pi G rho0 N - c_s²)k²] delta rho_hat.
```

Therefore `N>0` reduces restoring compressibility, while `N<0` increases
it. This also follows from the high-frequency gravitational quadratic
energy `-2 pi G N |delta rho|²`, added to the matter term
`c_s² |delta rho|²/(2 rho0)`. `N` has length-squared units, so
`4 pi G rho0 N` has sound-speed-squared units.

The one-variable proof is sufficient: a later value below `f(h0)` gives
`f'(h1)<0`; if `f''<=0` on the remaining ray, this negative slope never
increases and forces `f` to minus infinity, contrary to the finite limit.
At the resulting `h*`, `H=h* nn` has positive trace and
`N=f''/2>0`. The local polynomial has this jet at its origin; it is not a
global constant-gradient background. A uniform-density quadratic plus a
traceless harmonic quadratic realizes the required local Hessian.

For the frozen system, growth `exp(c k t)` at any fixed positive time cannot
be bounded by Sobolev polynomial weights in `k`. Continuity in direction
also gives an open cone around the positive direction, so the argument is
not dependent on a measure-zero Fourier ray. This proves the stated frozen
failure, without a nonlinear or variable-coefficient well-posedness claim.

For the KT39 application, the simple primitive has `Q'(z)>1`, with
`Q'(z)->1`, and `Q(0)=0`. Hence `R=Q/z>1` and `R->1`. At `g0!=0`, `ell>0`,
`p>0`, and `h>0`, both `s` and `z` are positive; fractional powers are smooth
there. This validates all positive powers in the stated local application,
without requiring smoothness at `H=0` or the joint zero jet. A finite energy
endpoint alone does not establish a force-derivative endpoint.

For the virial, variation of the subtracted functional gives

```text
delta U_ph = -(1/(4 pi G)) integral
  [(A-A_ext).grad(delta psi) + B:Hess(delta psi)]
 = (1/(4 pi G)) integral delta psi (div A - double_div B)
 = integral Phi_ph delta rho.
```

The single integration by parts for `A` and the double integration by parts
for `B` produce opposite signs, as in the source. With
`delta rho=div(rho r)`, another integration by parts gives
`dU/d(log lambda)=-integral rho r.grad Phi=-W`. Thus a positive compression
energy gives a negative binding virial, not an additional attraction.

The energy's constant and tangent subtractions at nonzero external field
make its integral convergent. The tangent contributes zero angular average
for this centered spherical homology. At zero external field, the fixed-mass
homology derivative remains valid although absolute isolated energy diverges:
`delta psi=O(r^-3)` makes the Green surface terms vanish even for
`Phi_ph=O(log r)`. A uniform physical acceleration contributes no centered
virial because `integral rho r=0`.

Since `Q'` decreases, its average `R` exceeds its endpoint value `Q'`, so
`R'=(Q'-R)/z<0`. In the stated external-dominated, curvature-weak expansion,

```text
U_H = -e² R'(eta²) ell^(2p)/(8 pi G a0^(2p))
      * integral (H:H)^p > 0,
U_H(lambda) = lambda^(6p-3) U_H(1),
W_H = -(6p-3) U_H < 0,  p>1/2.
```

For Plummer, direct insertion of the Hessian eigenvalues gives
`H:H=(GM/a³)² 3(1+2u⁴)/(1+u²)^5`. The radial integral behaves as
`u^(2-6p)` at infinity, hence converges exactly for `p>1/2`.
The stated coefficient
`sigma_H²=(p-1/2) J_p e² R' ell^(2p) (GM)^(2p-1) a^(3-6p)/a0^(2p)`
has the correct sign, factor, and dimensions. For `p=9/8`, it scales as
`M^(5/4)` at fixed size and external field; this does not determine finite
dwarf masses. The ordinary linear external-field factor
`nu(eta)+eta nu'(eta)/3` also has the correct angular-average normalization.

Finally, stationary momentum balance gives
`W=integral trace(T)` when the virial surface term vanishes. For collisionless
matter `T_ij=rho <v_i v_j>` is positive semidefinite, so `W=2K>=0`, independently
of velocity anisotropy. The same positivity applies to ordinary positive
pressure included in the kinetic stress. Consequently a genuinely negative
**total** `W` is incompatible with that fixed stationary configuration.
A negative curvature contribution alone does not imply this contradiction.
For the infinite Plummer profile, this stationary stress derivation avoids
assuming a finite global moment of inertia, which the profile does not have.

## Obligation matrix

| Obligation | Status | Result or limitation |
|---|---|---|
| Energy endpoint implies some positive rank-one second variation | passed | Mean-value/concavity contradiction is sufficient. |
| Positive-density jet is admissible | passed | `trace(H)=h*>0`; claim is local, not a global equilibrium. |
| Full susceptibility and mixed-term cancellation | passed | Both mixed terms retained; signs reconstructed above. |
| Ordinary matter dispersion sign | passed | Positive `N` destabilizes dust at high frequency. |
| Frozen Sobolev growth obstruction | passed | Exponential frequency growth defeats polynomial norm weights. |
| KT39 application for every positive power | passed | Uses nonzero `g` and `H`, where all derivatives exist. |
| Fixed-mass homology and virial sign | passed | Fixed external gradient and boundary subtractions retained. |
| External-field curvature stress and Plummer scaling | passed | Asymptotic regime, convergence range, and factors checked. |
| Negative total trace virial excludes the stated equilibrium | passed | Requires gravity-only balance and no confining surface stress. |
| Existence of an equilibrium from positive trace virial | out of scope | Necessary condition is not sufficient. |
| Full nonstationary/background-variable PDE theorem | out of scope | Only frozen result and local principal diagnostic are established. |
| Numerical quadrature values, counts, and finite-grid margins | not addressed | No experiments or artifact regrading were requested in this audit. |
| Actual MW or satellite evolution; all modified gravity | out of scope | Not implied and explicitly disclaimed in the sources. |

## Precision notes, remaining gap, and strongest safe statement

1. The original `dynamics/GENERAL_OBSTRUCTION.md:59` described background
   motion as lower order. Constant background translation actually gives
   the leading Doppler shift `omega -> omega-k_vector.v0` in laboratory
   coordinates; it disappears in a local comoving frame and does not change
   the exponential growth rate. The owner corrected this in both dynamics
   documents. The final text explicitly displays the laboratory frequency
   and restricts the lower-order statement to background gradients and
   finite `K`. This resolves the precision issue without changing the
   frozen theorem.
2. In the preserved `efe/DERIVATION.md:59`, “positive scalar binding virial”
   denotes the sign convention, not guaranteed positivity. The owner added
   `efe/DERIVATION_v2.md:59` and `efe/ERRATA.md` to state the convention
   explicitly while preserving the original computation-pinned document.
   Direct comparison confirms that the sole revision is this clarification;
   equations and hypotheses are unchanged.

This reviewer changed only this report and inspected the owners' completed
clarifications. No correction to an existing displayed formula was needed.
There is no remaining implication missing from the normalized analytic
claims. The smallest gap before claiming a physical instability is a
specified, admissible matter/background completion at the galaxy in
question, including the wavelengths where that closure applies. The
smallest gap before excluding an observed satellite is establishing its
actual source/tracer configuration and external field, including any tides
or stresses omitted from the uniform-field diagnostic. A negative exact
virial for the prescribed profile needs no assumption of isotropic velocity.

The strongest safe statement is that this finite-endpoint local action
family cannot provide uniformly bounded short-wave growth for ordinary
pressureless matter on every positive-density local background, and that
its controlled external-field expansion contains a repulsive scalar virial
stress. Neither result excludes all completions or all gravity models.
The cheapest next check is to preserve these hypotheses explicitly in the
final summary; physical generalization requires new input, not another
formal sign check.

## Provenance and exact revision

Independent focused subagent review, performed 2026-11-04. Critical signs
were reconstructed from the four raw target files before consulting nearby
scope summaries. No previous audit verdict was used as mathematical evidence.
This is independent derivation within the same model family, not independent
experimental evidence. No literature claim, new numerical experiment, or
change to historical source was made by this reviewer. The source owners'
two wording clarifications were subsequently inspected, as recorded above.

The shared repository was dirty and the KT40 directory was untracked at
review time. Git HEAD was `009f39ec2fb18b33d68a539f4fe6a222d08d7810`; the file
hashes, rather than HEAD alone, identify the audited mathematics. No
applicable `AGENTS.md` or local `.mathbox` ledger was found on the relevant
ancestor path. Read-only inspection used `rg`, `cat`, `nl -ba`,
`git rev-parse HEAD`, scoped `git status`, and `shasum -a 256`.

| Audited file, relative to KT40_mechanism | SHA-256 |
|---|---|
| `dynamics/GENERAL_OBSTRUCTION.md` | `84cc5e8d643ce01edf66b88709257538148fc274db1208ff30da81f01a87805a` |
| `dynamics/DERIVATION.md` | `8aef9dcbfda9387b7a28e4aedf7e9372ced3e2ea00ff300e4cc5343797c51fab` |
| `efe/DERIVATION.md` | `0da8d12b437ff07a1a3ef26b3d01536118035950b2d172303e6055a567b40d78` |
| `efe/DERIVATION_v2.md` | `06e9aad842cee3d969142ed55674e844310f91e575d81fc4713022e60061b83a` |
| `efe/MECHANISM.md` | `5e9747b0164c3238a8a58f2c89019b5c2f8c50d4154c53894646391e8b975088` |
| `efe/ERRATA.md` | `e08a8dc04d0699e1144b030e70e5e547347611e7a5cb61b3447778e607fc8d5c` |

The initial dynamics revisions, before the Doppler clarification, had hashes
`a266c7ae395f2734c91365853467a17de9b10b967030ef588f5b35e249b0a264`
(`GENERAL_OBSTRUCTION.md`) and
`2fe33367b4287c8f86f2cb8a014e4071dc74c02edf2555713cec1bcd8c062265`
(`DERIVATION.md`).

Self-proofreading coverage: this report only; no mathematical-token changes
to the audited sources. Source hashes were rechecked after report creation.
