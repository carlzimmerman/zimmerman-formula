# TP04: radial dynamics, gapless sectors and a conditional cold state

There is a surviving **conditional cold-particle window** in the rigid model:
the residual neutral U(1) gaugino acquires a calculable mass and can be cold
and long-lived at weaker coupling. The rotating phase remains pressure-rich
and unstable farther out. Neither a selected cosmological dark-matter model
nor a solution to the vacuum-energy/gravity problem has been obtained.

This checkpoint starts from shared HEAD
`27a0d27db1c343e1752698da36aa300398214689`. All TP01--03 scientific sources
remain unchanged; manifests pin actual input bytes even as other sessions
advance HEAD. The complete [target contract](CONTRACT.md),
[unit conventions](UNIT_CONDITIONS.md), [source checks](SOURCE_CHECKS.md) and
[provenance verification](VERIFICATION.json) fix the scope.

## What changed physically

| State or sector | New result | Safe implication |
|---|---|---|
| Circular phase fluid | Actual finite radial coefficient and coupled dispersion; known covariant heavy derivative completion | The later negative sound speed is a finite-band spatial instability; finite radial corrections do not rescue it |
| Unbroken gauginos | All twelve acquire nonzero finite one-loop masses, with negligible neutral Goldstino mixing | The earlier tree-level massless-reservoir assumption needs this threshold; the neutral U(1) mode is a new candidate |
| Rolling phase charge | Residual U(1) anomaly produces zero-temperature gauge-helicity growth | Tiny nonabelian strong scales do not protect this rolling state; fractional depletion requires patch, plasma and seed data |
| Light adjoint fermion gas | Actual tree decay to a lighter scalar plus gaugino, in addition to Goldstino decay | A conserved particle population cannot be assumed |
| Small radial oscillations | Positive local radial pole, actual widths and measured narrow phase-production resonance | A cold coherent state exists locally; survival also depends on density, expansion, coherence and escape |
| Neutral photino population | Actual mass/source coupling, forbidden dangerous transitions, bounded leading hard and soft losses | A cold long-lived particle example survives the stated rigid finite-order tests, conditional on its initial state and independent physical scale |

## Radial dynamics and gapless response

The [radial report](radial/REPORT.md) calculates the component two-derivative
coefficient A independently of the angular F, including full scalar,
signed-Majorana, scalar/vector and vector/vector graphs. At the corrected
vacuum m_radial/mu is 1.67658e-7 at e=.01 and 8.95793e-7 at .03,
where mu=sqrt(f). The known heavy derivative completion includes both real
and relative-phase normals:

    L4 = J/2 {[(partial theta)^2-Box s-(partial s)^2]^2
                  +[Box theta+2 partial s dot partial theta]^2}.

Its order-reduced pole/growth corrections are small on the checked states;
extra high-derivative polynomial roots are not particles. At X/Xmin=1.3 the
radial/phase instability grows at Gamma_max/omega=.359 at .01 and .331 at
.03. The positive-sound interior at ratio 1.2 remains stable on the tested
momentum grid. No all-order gauge-independent pole theorem is asserted.

The uncharged oscillator decays predominantly into phase pairs. Its
gapless-phase loop gives a nonlocal p^4 log(-p^2) response and the computed
absorptive width. A homogeneous coherent pump also has a narrow Mathieu
band. Actual monodromy and expanding-band integrations check

    mu_F = eta m/2,
    I_cross = pi eta^2 m/(4H),
    I_cross/(Gamma_phase/H) = 16pi^2 rho/m^4.

Thus a tiny spontaneous width alone does not establish a coherent state's
lifetime. Random domains, escape, nonlinear depletion and actual initial
occupations remain state-dependent. The tested finite endpoint corrections
and their superseded short-crossing diagnostic are retained in the records.

The [gapless/charge report](gapless_charge/REPORT.md) matches the finite
gaugino masses and physical gauge threshold logs. Formal far-IR pure-YM
scales are exponentially small, after the gauginos decouple; they are not
calculated confinement gaps or susceptibilities. The residual photon and
Goldstino remain light, and the anomalous phase is effectively light in the
perturbative regime. This is not a massless-gaugino SYM vacuum.

The exact residual U(1) anomaly term is

    -5 g1^2 theta F1 Ftilde1/(32pi^2),
    gamma_helicity,max = 5g1^2 |omega|/(16pi^2).

For constant rolling in an infinite empty vacuum there is a tachyonic
helicity band. A finite patch must admit its wavelength; conductivity and
seed amplitude alter growth/depletion. In the illustrative raw-vacuum=DE
variant the amplitude e-fold times are about 6 s and .12 s at the matched
endpoints for .01/.03, if those vacuum/patch assumptions hold. These are
**amplitude growth times, not fractional charge lifetimes**. No thermal
sphaleron formula is imported into this zero-temperature result.

## The surviving conditional particle example

The leading neutral pole is

    m_chi = 1.1164161506e-4 mu e^(5/2),
    F_eff^2 = mu^4/31.

At e=.003 and m_chi=1 MeV, mu=1.81707e7 GeV and v=2.44405e9 GeV.
This is an explicit trial point, not a selected scale. The photino is neutral
under residual U(1); its connection to observed photons or a hidden sector
is not provided by the microscopic action.

The [cold-state derivation](cold_states/DERIVATION.md) verifies the unitary
transpose selection rule on the actual component action and vacuum. It
forbids the dangerous Goldstino/phase two-body transition and the nonabelian
gaugino one-vector dipoles perturbatively. The three-gaugino threshold is
closed. The actual mass source has dlnm_chi/dlnX=-.99037918; retaining its
rest-mass source changes the benchmark gas compressibility by only 7.61e-55
relative to the positive ideal term.
The [current cold-state status](cold_states/CURRENT_STATUS.md) links the
later bound closures while preserving the original report's historical scope.

The source-checked Goldstino/photon partial width is m_chi^5/(16pi F_eff^2).
The [hard-loop proof](gapless_charge/decay_bound/REPORT.md) goes beyond
assuming a small Wilson coefficient: all leading heavy box/seagull
two-vector transitions obey |c7_eff|<=6.6061e6, below the one-age budget
1.04e9. Their inclusive width is at most 1.070% of the Ward partial width.
[Leading soft/current completions](cold_states/SOFT_COMPLETION.md) include
phase radiation, anomaly photon splitting and light Goldstino exchange;
the dilute nonrelativistic annihilation rates are also negligible at the
explicit halo benchmark. Independent proof reviews are recorded separately.

Combining this **specified leading rigid-model loss set** gives

    lifetime >= 1.15116e20 s,
    survival over 13.8 Gyr >= .996224.

See [preferred combined result](run_loss_v2/result.json),
[exact loss scope](LEADING_LOSS_SCOPE.md), and the
[interference-safe composition addendum](LOSS_COMPOSITION_ADDENDUM.md).
Fresh proof review replaced overlapping graph-class rate sums with amplitude
triangle bounds and added the final leading four-fermion collisions. These
corrections leave the displayed survival unchanged. This is not an all-orders total
width or a finite-temperature history. Higher-loop/current, higher-derivative,
more general soft radiation and UV/gravity symmetry violations remain outside
the bound. The dilute-halo annihilation check is not an early-Universe
thermal-average calculation.

An explicit unpolarized, decoupled FD initial distribution can match the
benchmark cosmic rest density. At the 1 MeV point it has
T_chi0/T_nu0=.022456 and v_rms at equality=4.61e-8. The computed comoving
free-streaming travel distance is 103.75 pc, independently bounded below
120 pc. These are travel distances and velocity tests, not an observational
transfer-function fit. The FD occupation satisfies Pauli directly; its
infinite tail is not replaced by the separate compact-support halo bound.
The example has no coherent theta-dot and does not inherit the rolling-phase
charge instability. See [conditional distribution](run_thermal/result.json)
and [independent unit/state audit](gapless_charge/UNIT_STATE_REVIEW.md).

The FD distribution is an initial-state assumption. Production, reheating,
other gaugino populations and hidden-bath entropy are not derived. Radiation
budgets are tested only at explicitly assumed bath temperature ratios. A
visible-photon identification would require its own line/energy-injection
constraints; age alone is not a phenomenological viability test.

## The vacuum-normalization restriction is decisive

The MeV example has raw V0/rho_DE about 1.396e74. It needs an independent
vacuum-energy mechanism and a compatible gravity embedding. Subtracting a
gravitating constant does not replace F_eff in the Goldstino coupling.

If raw V0=mu^4/31 itself must equal the benchmark dark-energy density, mu is
5.28639e-12 GeV. Then at e=.03 the photino mass is only 9.20e-11 eV and is
too small for the stated halo Pauli density test; weaker e makes it smaller.
Small radial oscillations also carry far too little energy at small amplitude:
rho_radial/V0=31 alpha^2 mhat^2 vhat^2, at most 4.23e-12 for alpha=.01 and
e<=.03 at leading order. These statements close the tested small-amplitude/
photino constructions in that raw-vacuum variant, not every possible large
bosonic or nonperturbative state of the theory.

There is therefore a concrete cold-particle door in the weak rigid model,
with mass, coupling, leading loss and cold-distribution checks. A completed
dark-matter claim still requires vacuum/gravity and photon identification,
production and abundance, and the stated higher-order/thermal obligations.
The original circular pressure failure remains established in its sampled
state. The two conclusions concern different states and are kept distinct.

## Evidence and continuation

All runs are bounded local experiments, one numerical thread each; no
production job, queue edit, package install or Git mutation was performed.
Full source/output hashes, independent reviews, retained failures and earlier
checkpoint preservation are checked in VERIFICATION.json. Read
[handoff](HANDOFF.md) for the exact remaining obligations and resumption
conditions. No prior manuscript or historical checkpoint is rewritten.
