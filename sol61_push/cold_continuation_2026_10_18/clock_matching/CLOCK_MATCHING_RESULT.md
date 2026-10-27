# The charged host supplies a low-energy clock margin, with a host-scale cutoff

19 October 2026 UTC / 18 October America/New_York. Claim
`CE-CONT-CLOCK-MATCH-001`. Original cold-energy research goal remains **OPEN**.
Writes are confined to this `clock_matching/` folder.

The canonical charged complex scalar plus real mediator already generates a
positive clock compressibility on its locally stable occupied phase. It is
therefore unnecessary to add an independent `P_XX` to obtain the CE-FM-079
low-energy temporal margin. The exact frequency-dependent kernel and full
four-field dispersion below show both the scope and its limit: the derivative
expansion is controlled by a light host-amplitude eigenvalue, not by the heavy
mediator mass. If the existing derivative response ansatz is extended past that
scale without further matching, its canonical superluminal front survives.

This matches the **host-clock sector only**. The response action itself remains
the CE-FM-079 proposal; its coefficients and high-frequency derivative structure
have not been derived from the mediator. No all-frequency UV matching is claimed.

## 1. Microscopic branch and conventions

Use signature `(-+++)`, `m_host=1`, `X=-(partial theta)^2` with no factor one-half,
and `Psi=sqrt(I) exp(i theta)`. The canonically normalized microscopic action is

    L_host = -(partial sqrt(I))^2 + I X
             - (partial chi)^2/2 - V(I,chi),
    V = I + lambda I^2 + a chi I
        + M^2 chi^2/2 + mu chi^3/3 + chi^4/4,
    lambda=2-1/M, a=2M, mu=-3M/8.

The saved coexistence rows satisfy `V_I=X`, `V_chi=0`. Their positive variable
`x` is `-chi`. Define the canonical real radial amplitude `rho=sqrt(2I)` and
the amplitude Hessian at fixed background frequency `sqrt(X)`:

    H = [[Ar,h],[h,Bh]],
    Ar = 4 lambda I,
    Bh = M^2+3Mx/4+3x^2,
    h = a sqrt(2I),
    Aeff = Ar-h^2/Bh.

The positive sign in `3Mx/4` matters: it is `2 mu chi` with both `mu,chi<0`.
The selected coexistence rows have `H>0`. A local occupied branch consequently
exists under small changes in X. This is branchwise matching, not the global
thermodynamic pressure across the degenerate vacuum/occupied coexistence edge.
No interface, vacuum continuation through `I=0`, or phase-production calculation
is supplied.

Under the earlier exact weak-coupling rescaling, the host action in base fields
is multiplied by `1/epsilon`, H and X are unchanged, and all host clock
coefficients below are divided by epsilon. The finite runs here use epsilon=1;
they do not require increasing the carrier inventory.

## 2. P_X and P_XX are fixed by the canonical amplitudes

For the local stationary branch define

    P(X) = [I(X) X - V(I(X),chi(X))]/epsilon.

Stationarity gives `P_X=I/epsilon`. Differentiating the two stationary equations,

    dchi/dI = -a/Bh,
    dX/dI = 2 lambda-a^2/Bh = Aeff/(2I),

and hence

    P_XX = 2I/(epsilon Aeff),
    kappa = 2P_X = 2I/epsilon,
    Delta0 = 4X P_XX = 4 kappa X/Aeff,
    B_clock = kappa+Delta0,
    c_host^2 = Aeff/(Aeff+4X).

Thus the prior adiabatic coefficient `kappa/c_host^2` is recovered directly.
P_XX is not freely selectable while the microscopic potential and phase are held
fixed. At M=10 and epsilon=1 this gives

    kappa=8.7031882486, Delta0=28.2248768992, c_host^2=.2356795086.

For the CE-FM-079 response `F(y)=gamma y^3/3`, `A(y)=Z0+2gamma y`, the exact
low-energy all-direction inequalities previously derived become a restriction
on these microscopic parameters:

    2I/epsilon > (Z0+gamma y)y^2/X,
    4 kappa X/Aeff >= gamma(Z0+gamma y)y^3/(Z0 X).

For example, `gamma=Z0=1`, M=10, epsilon=1, y=1 has positive spatial margin
`6.1199262231` and radial common-cone determinant `25.6416148737`. These are
actual matched host values on the specified homogeneous branch. They are not a
derivation of the response coefficients or of a halo background.

## 3. Exact nonlocal Schur complement and a quantitative validity criterion

Let `Omega` be the perturbation frequency (distinct from background `sqrt(X)`),
`k=|wavevector|` and `s=k^2-Omega^2`. Keeping the canonical radial and mediator
kinetic terms, their inverse kernel is `H+s 1`. Integrating them out at quadratic
order gives the exact tree-level phase entry

    kappa Omega^2 - kappa k^2 + Delta(s) Omega^2,
    Delta(s) = 4 kappa X [(H+s 1)^(-1)]_rr
             = 4 kappa X (Bh+s)/Q(s),
    Q(s) = (Ar+s)(Bh+s)-h^2.

This is a frequency- and momentum-dependent Schur complement. It is not a new
constant P(X) operator. Its poles are the Dirichlet amplitude-kernel poles;
they are not by themselves poles or instabilities of the coupled full theory.
The unreduced determinant in section 4 is regular there.

Write the positive eigenvalues of H as `lambda_j` and the squared radial
overlaps as `w_j>=0`. Then

    [(H+s1)^(-1)]_rr = sum_j w_j/(lambda_j+s).

For `|s| <= eta lambda_min(H)`, `0<=eta<1`, the positive spectral sum proves

    Delta0/(1+eta) <= Delta(s) <= Delta0/(1-eta),
    |Delta(s)/Delta0-1| <= eta/(1-eta).

This is a uniform analytic kernel-error estimate, not a numerical sample. It
holds, for example, whenever both `|Omega|` and `k` are at most
`Lambda=.1 sqrt(lambda_min(H))`: then eta=.01 and the relative error is at most
`1/99`, about 1.011%. For a subluminal phase branch `0<=s<=k^2`, the sharper
one-sided bounds are

    Delta0/(1+k^2/lambda_min) <= Delta(s) <= Delta0.

The first dispersive correction is also fixed:

    Delta(s) = Delta0 - Delta1 s + O(s^2),
    Delta1 = 4 kappa X (Bh^2+h^2)/(Ar Bh-h^2)^2 > 0.

For a low-mode expansion `Omega^2=c^2 k^2+b k^4+...`, let f(z) be the
CE-FM-079 quadratic polynomial in `z=c^2`. Direct substitution gives

    b = Delta1 (A c^2-C) c^2(1-c^2)/f'(c^2).

For either strictly subluminal simple low root this is nonnegative: the signs
of `A c^2-C` and `f'(c^2)` agree. The exact modes therefore acquire an upward
frequency correction; replacing Delta(s) by Delta0 loses this physical effect.
The analytic kernel bound alone does not prove a uniform exact group-speed
bound. Derivatives of the kernel and the margins of the dispersion roots also
matter.

## 4. The full amplitude + phase + response determinant

Retain the same response ansatz, with `u=-partial theta/sqrt(X)` and background
`theta=sqrt(X)t`, `phi=y x`. Set `t_angle=cos(angle)^2`; below this is denoted T
to avoid confusing it with time. Define

    A=Z0+2gamma y, C(T)=gamma y(1+T), q=Z0+gamma y,
    r=q y^2/X, E(T)=kappa-r T, d=q y/sqrt(X).

The exact reduced two-field matrix has entries

    A Omega^2-C k^2,          d Omega k sqrt(T),
    d Omega k sqrt(T),       kappa Omega^2-E k^2+Delta(s)Omega^2.

Multiplying out the amplitude denominator gives the full four-mode quartic in
`z=Omega^2`, `K=k^2`, `s=K-z`:

    D(z,K,T) = (A z-C K)[(kappa z-E K)Q(K-z)
                       +4 kappa X z(Bh+K-z)]
               -d^2 z K T Q(K-z) = 0.

An independent first-order implementation uses canonical phase
`psi=sqrt(kappa) pi`. Its Lagrangian contains the physical radial/clock mixing
`2sqrt(X) a dot(psi)` and response mixing
`-d/sqrt(kappa) dot(phi_pert) partial_x(psi)`. It diagonalizes the resulting
8x8 generator, rather than finding the quartic roots. Quartic roots and
eigenspectra are compared separately. Group velocities are computed from the
Hermitian quadratic pencil by implicit differentiation and checked against
centered differences of eigenfrequencies.

For `H>0`, `E(T)>0`, `A,C(T)>0`, the quadratic Hamiltonian is positive: kinetic
terms are positive squares after the momentum shifts, and the potential is
the sum of the positive H form, canonical amplitude gradients, `E|grad pi|^2`
and `C|grad phi_pert|^2`. The mixed velocity terms cancel in its velocity form.
For nonzero k its finite-mode energy norm gives a generator skew-adjoint in a
positive inner product. Its frequencies are consequently real. The full finite
calculation checks this implication rather than interpreting the kernel poles
as growth.

Two useful exact checks distinguish scales and notions of speed:

* At k=0 there are two zero-frequency modes and the two nonzero **physical**
  gap squares are the eigenvalues of `H+4X diag(1,0)`. These differ from the
  eigenvalues of H governing the derivative expansion.
* At the matter light cone, `Omega^2=k^2`, s=0 exactly. Thus, for every nonzero k,
  `D/(k^4 det(H))` equals the old adiabatic common-cone determinant
  `Delta0(q-gamma y T)-gamma y r T^2`. This identity is not a statement that
  every massive phase speed is below one, or that group speeds cannot exceed
  one. Phase, group and front speed are distinct in this dispersive system.

## 5. The controlling gap remains near the host mass

All entries below use the actual saved phase rows, in host-mass units.

| M | sqrt(lambda_min(H)) | lowest physical k=0 gap | chosen Lambda | kappa | Delta0 |
|---:|---:|---:|---:|---:|---:|
| 1 | .58239319 | 1.24988856 | .05823932 | 1.0619341 | 5.8777788 |
| 10 | .85761376 | 1.76202050 | .08576138 | 8.7031882 | 28.2248769 |
| 100 | .98080432 | 1.96560586 | .09808043 | 97.9786194 | 295.5389269 |
| 1000 | .99800837 | 1.99638083 | .09980084 | 997.8581013 | 2995.0306121 |

This is structural, rather than merely a trend in four rows. The coexistence
polynomial in `mediator_phase_matching.py`, divided by M^3, gives

    x = 1 - 81/(32M) + O(M^-2),
    I = M/2 - 69/64 + O(M^-1), X -> 3/4.

Consequently `Ar=4M-85/8+O(M^-1)`,
`h^2/Bh=4M-93/8+O(M^-1)`, so `Aeff->1`. Also `Bh~M^2` and the largest
amplitude eigenvalue is asymptotic to Bh. From the determinant and trace,

    lambda_min(H) -> 1,
    lambda_min(H+4X diag(1,0)) -> 4,
    kappa~M/epsilon, Delta0~3M/epsilon, c_host^2->1/4.

Making the mediator heavy increases the clock inertia but does not move this
clock derivative expansion to the mediator mass. Using `Omega<<M` as its only
validity condition would omit the light radial amplitude.

## 6. Finite exact-dispersion results and the surviving obstruction

The bounded run tested eight (M,y) backgrounds at epsilon=gamma=Z0=1. Each has
153 spectra: nine fixed angles `T=0,1/8,...,1` and 17 logarithmic wavenumbers
from `.001 Lambda` to Lambda. All four modes are kept; the two low modes are
the two smallest positive frequencies. No filtering or random sampling occurs.

| M | y | maximum sampled low-mode group speed | maximum relative low-frequency EFT error |
|---:|---:|---:|---:|
| 1 | .1 | .42410863 | .00339414 |
| 1 | .6 | .79376711 | .00339414 |
| 10 | .1 | .49046741 | .00290169 |
| 10 | 1 | .85296395 | .00290169 |
| 10 | 1.5 | .93757017 | .00311116 |
| 100 | 1 | .82083426 | .00280570 |
| 100 | 3 | .96828940 | .00297702 |
| 100 | 3.6 | .99827518 | .00313382 |

All sampled group speeds of all four modes are also below one in this band.
The maximum observed kernel relative error is .00955815, within the analytic
1/99 bound; maximum quadratic-pencil residual is 4.19e-12. These 1224 spectra
are finite evidence. The analytic low-energy principal inequalities cover all
angles at the specified backgrounds, while exact group-speed sampling covers
only the stated points. No continuum exact group-speed theorem is asserted.

A separate M=10, y=1 radial continuation evaluates 121 wavenumbers from .001
to 10000. The first detected maximum-group-speed crossing is bracketed by
`3.6168736144 < k < 4.1368204024`; root refinement gives

    k_cross = 3.6600041200,
    Omega_of_crossing_mode = 4.5942153875,
    dOmega/dk = 1 (to floating tolerance).

This is above both the conservative matching cutoff .08576138 and the lowest
k=0 physical gap 1.76202050. The first-crossing label refers to the sampled
bracket followed by refinement, not a proof that no narrower earlier crossing
exists. A gapped mode crosses first. Even a gapless mode later has a sampled
group speed above one; its phase speed can remain below one. Large massive
phase speeds near k=0 alone have not been counted as a causality violation.

The high-frequency **front** obstruction is analytic. At a generic fixed
`Omega/k !=1`, `Delta(k^2-Omega^2)=O(k^-2)`. The amplitude/clock gyroscopic
mixing is of lower differential order. The four principal fronts are therefore
the two canonical amplitude fronts of speed 1 and the two response/clock
fronts with Delta=0. The radial matter-cone determinant is

    -gamma (Z0+gamma y)y^3/X < 0.

For the M10,y1 witness, the two latter speeds are
`.6342057877` and `1.0795880635`. The full quartic approaches these, with the
largest phase speed at k=10000 agreeing with the superluminal front to better
than 1e-7. Thus matching the low-energy host compressibility does not cure the
canonical principal obstruction **if this response action is extrapolated**.
That extrapolation is not justified by the host calculation. A different
microscopic response could change its high-frequency derivative structure.

## 7. Execution, source hashes and scope of review

`run_001/manifest.json` is a completed, validated computation-audit v2 record.
The run passed 3957 checks in .947861 seconds, exit 0; the enforced wall cap
was 60 s, CPU cap 45 s and conventional numerical thread cap 1. Python 3.9.6,
NumPy 1.26.2, SciPy 1.11.4, SymPy 1.14.0, macOS 26.5.2 arm64. No large job,
source rerun or external literature claim was used.

The assigned historical base was `ea2da902eeddc0a9612e5ef0d393ed6f3c794e37`.
The shared repository HEAD advanced during this work: a preliminary read saw
`123fefe43e02bcd44fe919fd11613ec83553bc54`, while the bounded runner recorded
`b9f4f4d3b798b8245fb14ca493b9366d3a8027cc`. The pre-existing tree was dirty.
No Git state was changed by this work. Input content hashes, rather than an
assumption of an unmoving shared HEAD, pin this calculation.

| Input (relative to repository) | SHA-256 before = after |
|---|---|
| `sol61_push/closure_particle_bridge_2026_10_16/mediator_phase_matching.py` | `74573429e7df19a170a07ad04c19ee7c18ce99ba636a26d8b1e41516179d663a` |
| `sol61_push/closure_particle_bridge_2026_10_16/mediator_phase_matching_run_002/results.json` | `e2df12078387b810f130932499ea26936df8a65cce75f23bfa9fcbb84f79ad36` |
| `sol61_push/closure_particle_bridge_2026_10_16/four_gap_audit.py` | `6976ef8a51b1fe9385e1cd97aaaf933e93b95b2ac2b71daa6502132fe8a6f15e` |
| `sol61_push/closure_particle_bridge_2026_10_16/dynamical_clock_cones.py` | `db98509ee4ebe68cf1313feee6bcc630a708f8277952e33cf607b6a12557a912` |
| `sol61_push/cold_advance_2026_10_18/cones/FINITE_CLOCK_STIFFNESS.md` | `3df08b50aed0affaa4aa083639ad3a3f233ab8290e259f773a3c5042e2ff17a8` |

Script, contract and output hashes are also in the manifest. The results JSON
hash is `03744a79c37c869aa1fb0934f7018fc9e363449bf6aaa80b2e51a754d03b0943`.
The exact runner invocation and validation command are in `COMMANDS.txt`.

Outcome: **implementation and finite assertion verified in the stated range,
conditional on floating eigenspectrum tolerances and the retained response
ansatz**. Exact matching and kernel-error inequalities are analytic results;
numerical tolerances do not turn the finite dispersion sample into a theorem.
The symbolic identities, independent quartic roots, quadratic-pencil residuals,
and finite-difference group derivatives are orthogonal checks, but this is a
self-reviewed computation, not external certification.

Remaining physical obligations include microscopic response matching (especially
near and above the light host gap), loops and radiative control, a physical
occupied interface and stock conservation, formation/abundance, metric/lensing,
and observational tests. No current pointer, frozen record, manuscript, live
source process or other chat has been altered.

Proofreading self-review covered this new note and its equations: routine edits
none; mathematical-token corrections none; unresolved issue is the explicitly
unmatched response sector, not a typographical ambiguity.
