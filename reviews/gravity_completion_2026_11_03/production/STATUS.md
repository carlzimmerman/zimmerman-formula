# Production status, 3 November2026

**No complete cosmologically viable producer has been established.** Actual
finite-action stationary canonical and protected candidates now have computed
radial-mother decay-source distributions, abundances, expansion backreaction,
delayed massive-phase cascades, and radiation/companion budgets. The tested
radial examples are warm; their initial mother abundance is an explicit input.

Current interpretation: DERIVATION_CURRENT.md. Preferred physical transport:
run_physical/result.json. Preferred necessary threshold control:
run_controls_v3/result.json. Numerical/cubic/scattering/uncertainty checks:
run_final_checks_v2/result.json. The preferred full-dependency refresh is
run_refresh/manifest.json, with controls.json, physical.json and checks.json;
it reproduces those scientific results exactly and pins every imported local
physics source. Earlier source versions and failed records are retained.

## Decisive actual results

* Finite canonical n29 point t=1.1600439202,e=.003 has mchi25.8667keV,
  msigma6.45259MeV and ma3.97979MeV. Pair phases are closed. Actual neutral
  mean travel is10.3699Mpc in the collisionless-companion envelope. e=.004
  reduces it to2.41549Mpc with Ward survival.995990. e=.005 gives.74358Mpc
  but Ward survival.89207; e=.006 gives.27666Mpc with survival.17210.
* Actual nearfold stationary points msigma/mchi=2.01,2.1,3,4,10 are transported
  separately. At2.01 the neutral travel is47.691kpc, or152.925kpc under immediate
  companion-energy conversion. The fitted mother yield is.01356477 at20MeV.
  Companion mass or radiation is then excessive. These endpoint values are
  exploratory calculations, not proved brackets on all nonabelian histories.
* Actual protected n29 point e=.003,mu1.8170662e7GeV has msigma.443209GeV,
  ma.0758689GeV,mchi.974358MeV. The late massive-phase decay creates a genuine
  cascade. Its neutral travel is1.083516Mpc, or1.175612Mpc in the immediate
  companion-conversion endpoint. Fitted initial mother Y=3.894887e-7 is an
  input. At fixed leading dipole, the photino partial lifetime is at least
  1.32489e20s for any accessible neutral mass, maximized in width by a massless
  final fermion. It is not an established total lifetime. The81.1811eV GG
  daughter used for the tiny scalar-Ward channel is a TT-only Ward-completing
  prescription, not a determined physical neutral pole; it differs from the
  physical gravitino2.43535MeV. See ../protected_review/REVIEW.md. The transverse
  neutral1PI functions and scalar Goldstino cubics are not fully matched.
* Primordial small harmonic misalignment at H=msigma cannot supply these
  examples. Even converting **all** initial energy immediately into perfectly
  cold chi, radial displacement alpha=.01R supplies at most3.40e-5 of the
  protected abundance, and6.2e-10 to1.4e-9 of the actual canonical nearfold
  examples. This energy-only control is stronger in interpretation than a
  branching-based yield estimate. Canonical outer barriers further limit
  trapped displacements; those data belong to the canonical worker.

## Threshold corner and kinetic limits

Arbitrarily closing the neutral threshold does not justify a cold abundance:
Bchi vanishes and the required mother/companion energy grows. A necessary
energy inequality uses K=rho_hidden a^4 monotone and permits10% extra dark
matter plus DeltaNeff=.3. Full birth-quantile travel starts at recombination
and uses an **upper** H for its denominator, including every allowed hidden
energy contribution. The recombination decay tail is explicitly truncated.
Global Cmin covers the20MeV start through e± annihilation.

The5940 tested physical-ratio controls have no simultaneous energy,>=.99
Ward-survival and1kpc pass. The evaluated energy/lifetime boundary occurs at
e=.004349075159,r=msigma/(2mchi)=1.001242911,mchi167.487keV. Its post-recombination
travel alone is at least1.81466kpc at64-point birth quadrature. Independent
review obtains1.81424kpc. The32/64/128/256 quadrature control on the nearby
actual stationary base converges to1.81509kpc. This is finite evidence plus
a specified boundary evaluation, not a proof of a global minimum over gravity
models or all physical mass ratios.

The threshold inequality assumes dilute vacuum-width mother kinetics. Direct
8/3/1 source occupation is bounded: at the budget boundary every stream has
f<.01 after a region accounting for less than8.1e-8 of decays. A general
Pauli-blocked nonabelian plasma could alter the competing branching ratios;
no such full plasma solution is claimed. Nonabelian reaction dimensional
optical depths are large, so retaining those particles as collisionless is
not a validated physical companion history.

For actual transported points, named TP04 heavy-contact mean optical depths
are at most3.6e-7. At the threshold control, a broad off-shell light-scalar
envelope gives7.3e-23 and the Goldstino dipole envelope6.7e-50. There ma>msigma,
so inverse on-shell a formation is absent; cold direct sigma daughters can
form an on-shell sigma only at a zero-measure endpoint. These are named leading
channels and kinematic checks, not an all-orders thermal theorem. The fitted
protected late condensate has phase Floquet crossing exponent1.09e-8.

The scalar Goldstino widths are treated as uncertain Ward estimates. Varying
them from0 to1000 times the estimate changes protected travel by less than
1e-5 fraction and does not make any tested example cold. This tests the assumed
kernel and does not bound every unknown physical cubic. The unmatched phase
anomaly diagnostic is tiny but is not promoted to a certified inclusive bound.

## Distinct source and remaining work

Direct gravitational SM scattering into photinos has been integrated with
authenticated primary-source amplitudes and explicit Majorana/multiplicity
normalization. The Bessel normalization is reproduced to1.7e-14 relative.
With quantum SM incoming distributions and TR=.01Mp, the direct source gives
only1.49e-6 of the26.15keV target abundance, or5.71e-5 of a1MeV abundance.
TR is a stated thermal-history input, and this range is a weak-gravity
benchmark, not a measured reheating limit.

Gravitational production of the entire heavy hidden spectrum and its cascade
is **not** computed. A promising distinct continuation is heavy-messenger
decay freeze-in from an explicitly reheated hidden bath, using existing
vertices. It needs finite-temperature vacuum tracking: a bath near the heavy
threshold can overwhelm the very shallow zero-temperature restoring force.
No cold FD state, hidden temperature ratio, portal, vacuum cancellation or DE
scale has been silently derived by this work.

All runs use one numerical-library thread, wall caps<=240s, observed peak RSS,
fresh directories and v2 manifests. No queue changes, installations, Git
mutations, or TP01--05 edits were performed by this worker. The first final
checks run failed only at NumPy-bool JSON serialization; it has no result and
is retained. The fixed version is a separate completed record.
