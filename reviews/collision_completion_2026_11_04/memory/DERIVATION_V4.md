# Occupation-independent memory, charged absorption and signed action work

This continues the immutable v2 checkpoint in `DERIVATION.md`. Preferred
API is `response_api_v4.py`; v3 and v2 inputs and records remain unchanged.

## Physical cell-pair operator

`band_kernel` integrates actual conditional q² dq measures inside each radial
cell and dc/2 for the pair angle, independently of f. It returns Kij=<sigma v>,
rho_ij, exact time-dilation-weighted exit rho_ij and channel matrices Kij,a.
The physical one-sign bin density is

    n_i±=12 Tc³/(2pi²) Wi fS_i, Wi=(qhi³-qlo³)/3.

Therefore dfS_i/dtau=-fS_i sum_j Kij n_j-, pair production is
sum_ij n_i+ n_j- Kij, and charged carrier loss is twice this. This preserves
the physical six particle/six antiparticle species with actual fC=2fS.
The positive source moment, parent energy density, actual massive neutral exit
energy and separate source-energy moments are exposed, rather than assuming
all removed energy is radiation. K contractions agree with the independent
v2 occupied-continuum response below 7.4e-14 in three finite checks; daughter
channel sums agree below 1.5e-15.

## Passive Floquet-space charged-width bound

The explicit local on-shell charged absorptive matrix is

    GammaC(theta)=144 G beta(theta)/(32pi M),
    beta=sqrt(max(0,1-4 mC(xmid+amp cos theta)²/M²)).

Each momentum mode multiplies both GammaC and Gammaout by M/EN. On periodic
L² functions let L=dt+i delta(t)+Gammaout/2 and B=GammaC(t)/2. The derivative
and real detuning are anti-Hermitian; B is positive. For the perturbed and
unperturbed responses, (L+B) da=-B a0. Taking the real inner product with da
and applying the weighted Cauchy inequality gives

    ||Gammaout^(1/2) da|| <= epsilon ||Gammaout^(1/2) a0||,
    epsilon=sup_t ||Gammaout^(-1/2) GammaC(t) Gammaout^(-1/2)||.

Triangle and reverse triangle bound the neutral exit-rate ratio by
[max(0,1-epsilon)²,(1+epsilon)²]. This is an operator bound on Floquet space,
not a Gamma/omega criterion, and survives positive integration over the
actual occupied continuum. It does not require truncating a pair tail. The
common boost cancels. Monotonic mC(x) fixes the supremum at the inner turning
point. The actual matrix, not merely the nearly rank-one shortcut, is used
for the reported epsilon.

At Tc=1e-5, 3.11923e-6 and 1e-6, epsilon is .09604, .04008 and .01708.
Corresponding rate intervals are [.8172,1.2013], [.9214,1.0818] and
[.9661,1.03445]. An actual four-state FFT fixed-point solution with the
time-dependent charged width on the occupied continuum gives .9595, .9918
and .9873; node/iteration repeat differences are below 2.85e-5. This numerical
discriminator uses radial1/angular8; it is not the finer radial rate table.
The intermediate .146 stationary ratio and final 7.038 ratio cannot be
removed by this specified local positive absorption. A nonlocal/dispersive
charged retarded kernel is a different operator and is explicitly not bounded
by this argument.

## Signed energy/action moment

Instantaneous charged production need not be positive. For each incoming
mode the source current is J(theta)=2 Re(v†a(theta)); its period average is
the positive neutral hazard. Use delta=delta0-A cos theta and z=A/omega. The
actual periodic response has a=e^(iz sin theta) u with

    u_n=(-1)^n J_n(z) R_n v,
    r_n=J_n(z)² v† R_n† Gamma_lab R_n v.

The Bessel recurrence gives

    A <cos theta J(theta)>=-sum_n n omega r_n.

The oscillatory charged-number correction obeys dn_osc/dtau=-(J-<J>). Its
background work is <dot(Epair) n_osc>=A<cos theta J>. Therefore scalar power
is the opposite, Pscalar=sum n omega r_n. This is the actual signed work
input to dJfield/dN=-3 Jfield+Pscalar/(omega H). It should not be replaced by
the covariance of an invented positive instantaneous BW rate. The independent
four-state ODE current test agrees with this work moment to 8.3e-7, 9.9e-6
and 1.35e-4 relative in three occupied-mode cases.

The nonnegative sideband sum sum |n omega| r_n bounds the absolute scalar
power. `response_api_v4.py` exposes both moments. The previously reported
`absolute_energy_exchange_bound_pair` remains an upper bound only on an
on-shell phase-energy assignment under positive exit counting; **it is not
a general signed action-covariance bound**. In particular the 6.74e-6 number
in the first stage record must be read with that narrower meaning. The new
work-stage record supplies the actual sideband work and its valid bound.

The fixed on-shell exit energy has a separate residual

    R=sum_n (delta0+n omega) r_n
     = EN <neutral hazard> - <Epair(theta) J(theta)>.

The ODE comparison subtracts the finite-window parent-energy boundary before
testing this periodic identity. `run_work001` retained that boundary, failed
the comparison, and is preserved unchanged; the separately named v2 script
and `run_work002` implement the proper finite-window subtraction. R is
exposed explicitly for common-ledger matching of finite-width daughter
energy; it is not silently allocated to radiation or scalar action. The
finite radial-cell population projection also has a separately computed
energy moment because a cell-constant occupation cannot keep every intra-cell
correlation. These are quantified residuals, not an assertion that the whole
quantum energy ledger is already closed.

## Actual changing shape and massive cascade stage

`run_stage001` solves the nonlinear scalar cell distribution using Kij, rather
than multiplying the old optical depth. On the recorded slow orbit it reaches
Ycharged=1.72351e-13; an independently evolved stationary kernel control gives
6.27471e-13. Root feedback is still required for a full history.

For the actual neutral cascade A from the cascades package, partition nodes
into unstable U and stable Z. The channel terminal map is

    T_Z=inj_Z-A_ZU A_UU^-1 inj_U.

It is checked positive and preserves each channel's energy. The first
terminal-delay moment is A_ZU A_UU^-2 inj_U. Its maximal conditional terminal
delay times H at the start is 6.51e-7, permitting elimination at cosmological
N while still allowing many orbital periods of delay. Stable terminal
momentum cohorts are injected and redshifted individually, retaining actual
mass, energy, pressure and force. No massive daughter is declared radiation.

The newly produced S3_0 and S8_0 yields are 1.76223e-12 and 2.41092e-13.
Their retained rest energy per entropy is 3.68907e-8 GeV, 83.84 times the DM
reference .44e-9 GeV. This is a conditional new neutral-pair/relic obligation;
the stage omits their 2-to-2 annihilation and occupied inverse channels, so it
is not a global exclusion. Their force shifts the final well center by
8.86e-14, 2.65e-8 of the saved orbit amplitude. Primary four-state parent
energy is at most 4.45e-10 of the recorded oscillation energy. The massive
energy budget matters for relic abundance even though its field correction
is tiny in this late stage.

## Measured action correction on the evolving distribution

`run_workstage002` reconstructs exactly the nonlinear stage fS solution from
its occupation-independent kernels and computes all work moments afresh.
The fast diagonalized moment sum agrees with the full matrix band API below
1e-10 at three points; K itself reconstructs below 1e-12 on all eighty
orbits. Integrating dJ/dN=-3J+Pscalar/(omega H) on this prescribed-orbit
response gives a maximal relative correction 5.95214e-8, bounded by the
absolute sideband sum at 1.00672e-7. The separate finite-width on-shell exit
energy residual accumulates to at most 3.64351e-8 and the radial-cell energy
projection residual to 1.77738e-9 on the same relative action scale. The
maximum instantaneous absolute collision dlogJ/dN bound is 4.09678e-7.
These are conditional first-response bounds on the actual newly evolving
shape, not the old fixed-shape optical-depth diagnostic.

The first `work_stage.py` attempt failed before evaluating a moment because
Python star import excludes the private `_bin` helper. Its exact source and
failed record remain intact. The separately named `work_stage_v2.py` imports
that helper explicitly and supplies the completed calculation. This is an
implementation failure, not a physical counterexample or resource failure.
