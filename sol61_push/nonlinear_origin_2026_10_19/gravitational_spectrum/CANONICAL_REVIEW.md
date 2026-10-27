# Independent focused audit of the canonical-response construction

19 October 2026. Reviewer: the gravitational-spectrum agent, distinct from
the author of the canonical notes. This is an independent derivation review
of the raw notes and computation, within a shared conversation/model context;
it is not a blind external referee report. Only this review file was written.

**Normalized claim.** For the globally quadratic independent-particle
Hamiltonian (1), fixed `N,T`, and `E>-a`, canonical phase space gives the
stated rational *compression-moment* response and connected free energy.
The quantum independent-particle response has a source transition at
`2 hbar omega` and a separate thermal population contribution. A reversible
constant-positive-heat-capacity receiver changes the exponent as stated.
Equation (9) is a state-dependent curvature-moment normalization identity.
The separate TF formulas are exact for their declared reduced local
contact-plus-quadratic problem; the full functional's asymptotic convergence
and source-derivative error are expressly not claimed proved.

**Primary verdict: proved as written.** This verdict applies to the scoped
reduced-model claims in the final byte-pinned notes below. It does not certify
a finite-core equilibrium, a heat-exchange rate, the full GP asymptotic
expansion, or a physical universal acceleration law. The final note expressly
separates these outstanding realization obligations. No outstanding algebra,
normalization, source-selection, or protocol error was found in that scope.

## Dependency graph and obligations

| Arrow / leaf | Kind | Disposition |
|---|---|---|
| Globally quadratic Hamiltonian and independent MB state -> Gaussian canonical trace | Defined model + internal integration | Passed |
| Gaussian radial distribution -> Gamma law, Laplace transform, rational induced width | Internal probability calculation | Passed |
| `H=H0+EQ` -> source is `m sum r_i^2/(2L)`, not a uniform-acceleration internal dipole | Operator convention + common-mass source | Passed |
| Constant-T partition ratio -> connected free energy and heat output | Internal differentiation / first law | Passed |
| Reversible isolated cloud plus constant positive `C_b` -> Eq. (6) | Declared bath input + entropy balance | Passed conditionally on that protocol |
| Quantum trace and `x_i^2` matrix -> Eqs. (7)-(8) | Internal spectral sums | Passed for N=1 / independent MB trace |
| coth partial fractions -> relative-width error bound | Official external formula + positive-term inequality | Passed |
| Uniform-core Poisson coefficient plus reference inventory -> Eq. (9) | Internal algebra + stated host closure | Passed |
| Reduced TF Euler equation -> profile, radius, moments and leading energy constants | Internal convex minimization + radial integration | Passed |
| TF scales -> orders of gravity, quartic-trap and smoothed Fisher corrections | Internal scaling estimates | Passed as scale estimates |
| Reduced TF profile -> full-functional asymptotic/source derivative theorem | Additional theorem | Not addressed, explicitly unproved in the note |
| Globally quadratic canonical trace -> actual finite Newtonian-core thermal state | Confinement, escape, tails, preparation | Conditional; final note explicitly retains this input |
| Curvature response -> uniform-acceleration polarization and universal G normalization | Physical operator/state bridge | Not established; note correctly declines it |

No circular proof dependency was found. The numerical script supplements
the analytic formulas; it does not define the physical source or replace
the absent host/formation arguments.

## Decisive independent checks

1. With `omega^2=kappa0+E/L`, a Cartesian coordinate has variance
   `T/(m omega^2)`. Therefore `Q` is Gamma with shape `3N/2` and scale
   `T/(a+E)`. At the reference source its Laplace transform is
   `(1+E/a)^(-3N/2)`, and `F(E)-F(0)=(3NT/2) log(1+E/a)`.
   Subtracting `E Q0` gives exactly Eq. (4), with the stated negative
   derivative. This uses a scalar positive quadratic source, rather than
   a signed vector-acceleration source. The result has its pole at `E=-a`
   and cannot be continued into the target odd cusp by this derivation.

2. For the bath protocol, the cloud entropy change is
   `C_s log(T/T0)-(C_s/2) log s`, while the unforced receiver contributes
   `C_b log(T/T0)`. Setting their sum to zero yields the stated `eta` and
   `Q(E)=Q0 s^(eta-1)`. Moreover
   `d[(C_s+C_b)T]/dE=C_s T/[2(a+E)]=<Q>`, so no heat/work factor is
   missing. `C_b=0` gives the isolated action-conserving power one-half;
   the isothermal power one requires an infinite capacity ratio. A
   different receiver equation of state or irreversible protocol is a
   different calculation, exactly as scoped in the note.

3. For one Cartesian oscillator,
   `q=hbar(a+a_dagger)^2/(4L omega)`. Its diagonal term is proportional
   to `2n+1`; the only nonzero-frequency source matrix elements connect
   `n` and `n+2`. The static off-diagonal Lehmann sum gives
   `hbar coth(x)/(8 L^2 omega^3)`. The diagonal canonical fluctuation is
   `beta Var(q_diag)=hbar x csch(x)^2/(8L^2 omega^3)`.
   Multiplication by `3N` gives Eq. (8), and direct differentiation of
   the trace gives their sum in Eq. (7). This checks both the energy-gap
   factor of two and the factor-of-two split in the classical limit.
   The population term is not an additional isolated retarded line.
   The note's final N=1 / MB and quantum-compression qualifications avoid
   extrapolating the independent nondegenerate gas through Bose degeneracy.

4. Official [DLMF 4.36.3](https://dlmf.nist.gov/4.36.E3), accessed
   2026-10-19, states the coth partial fraction formula. Reading its
   positive terms for real `x>0` gives
   `x coth(x)-1=2x^2 sum_{n>=1}(x^2+pi^2 n^2)^(-1)`.
   Bounding each denominator below by `pi^2 n^2` gives `x^2/3`.
   The official page displayed DLMF version 1.2.8, release 2026-09-15.
   No source file or PDF was retained. This exact external leaf was
   checked rather than inferred from the finite samples.

5. Independently substitute `rho_b=3 kappa0/(4 pi G)` and
   `<r^2>=3T/(m kappa0)` into Eq. (9). Its right side becomes
   `6 pi G (N/V)T/(L^2 kappa0^2)`, equal to the left side. The coefficient
   is `3/2`, and the proposed rms-radius convention indeed requires
   `rho_d/rho_b=2/3` to set this expression to one. The identity is
   dimensionless but contains the arbitrary reference volume/inventory
   and the curvature-source scale `L`; it cannot fix a uniform-force
   polarization coefficient by dimensions alone.

6. The reduced TF Euler equation is
   `2K rho+E r^2/(2L)=lambda` on positive support. Its unique fixed-mass
   minimizer has `lambda=E R^2/(2L)` and the stated parabolic profile.
   Radial normalization gives `M=2 pi E R^5/(15KL)`; the next moment
   gives `<r^2>=3R^2/7`. Thus the source deficit is `3MR^2/(14L)`.
   The harmonic contribution is `3M lambda/7`; scale variation gives
   `2V=3S`, so the total reduced excess energy is `5M lambda/7`.
   The quoted constants and powers are therefore consistent.

7. With `R~E^(-1/5)`, gravitational self-energy scales as `E^(1/5)`,
   and the next Plummer term as `E R^4~E^(1/5)`. A smoothed edge can
   give Fisher scale `R^(-2) log E~E^(2/5) log E`, while the sharp
   parabolic density has a logarithmically divergent Fisher integral.
   These orders are below the reduced leading `E^(3/5)` energy. They
   do not themselves justify differentiating a full minimizer's energy
   asymptotic or prove its source deficit; the note makes that limitation
   explicit. The polytropic scaling follows independently from balancing
   `R^(-3(gamma-1))` against `E R^2`.

## The finite-core scope correction

During review I identified a realization issue in the original wording:
a finite Newtonian baryonic potential approaches a constant at spatial
infinity, so its unrestricted classical canonical position integral
diverges. A supported finite core alone therefore does not supply the
globally confining equilibrium used in the exact Gaussian calculation.

The author added a paragraph explicitly distinguishing the ideal quadratic
Hamiltonian from a spatially confined or conditioned metastable finite-core
cloud, and retaining the boundary, lifetime and outer-tail error as missing
inputs. The final hash below includes that correction. This resolves the
scope issue in the audited mathematical claim; it does not solve the
physical confinement/formation obligation. No reviewer edit was made to
the author's files.

## Computation audit and validation

Read `check_canonical.py`, its contract, complete JSON results and manifest.
The 104 controls are exactly 36 Gamma tests, 36 quantum tests, 5 coth sample
checks, 24 finite-bath checks and 3 TF checks. This enumeration matches the
reported count; no hidden sampling or exhaustive claim was found. The
oscillator sums use 120 levels at nine declared frequency/temperature
pairs, while the analytic geometric sums establish the formulas. The TF
quadrature checks one normalized parabolic profile, not a sequence of full
GP minimizers. The script does not test Eq. (9), which was checked
algebraically above.

The recorded run status is `completed`, runtime `0.292669 s`, with 45 s wall
and 30 s per-process CPU caps, one conventional numerical-library thread,
and no memory/affinity hard cap. I did not rerun the scientific job.
I ran the installed computation-audit `validate_manifest.py` on
`canonical_response/run_001/manifest.json` with the project root: it
reported a valid evidence record with status completed and present input
hashes intact. This is provenance validation, not a theorem certificate.

## Exact revision and disposition

Paths below are relative to
`sol61_push/nonlinear_origin_2026_10_19/`.

| Audited artifact | SHA256 |
|---|---|
| `canonical_response/CANONICAL_RESPONSE.md` | `e97cb72d71a31a31226414184ff8bf1f5a5280596a7d01f8028ed3690727c622` |
| `canonical_response/STRONG_SOURCE.md` | `4466dae13b8e0507adf8c4b3c8c9d99f6d73e722d6065f3bc32c3fbfd6084496` |
| `canonical_response/check_canonical.py` | `a9fceffbb9416ff80de67a2b4b5a0bb102975c59b1ea31a9ba9076b4b9dcaa64` |
| `canonical_response/run_001/results.json` | `225364e8c23bc4a5e18781d58235904f95d7c635f483e6b75489c78a131f4605` |
| `canonical_response/run_001/manifest.json` | `faaa8d789633a93df45cfda380452538d9db309a43801277bd3c9c2be0dda6c8` |
| `TARGET.json` | `5950a492b172cfe08c5e35d7e44341fd42c4048764bec48c91dddc69f0fde560` |

**Disposition: pass the reduced-model formulas and the notes' calibrated
conclusion.** No change to the action or universal gravitational conclusion
is justified by this pass. The strongest safe statement is the exact
isothermal rational law for its actual quadratic compression operator,
with the independently checked quantum, protocol and normalization
distinctions. A cheap discriminating next step for a real finite host is
to declare the cloud boundary/preparation and estimate its escape and
tail error before inferring a canonical state. A supported live host and
derived thermal relaxation rate remain additional research obligations.
