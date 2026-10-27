# Backreaction changes the resonance: a fixed-angle prediction

This calculation concerns the local retained mode-wave Hamiltonian, not a
self-forming galaxy or a measured infall angular spectrum. No coupling or
initial mode energy is changed in the tests below. Angles are fixed throughout
each run; no chirp, extra force or external work drives them.

The complete conservative inertia increases daughter transfer, but the linearly
resonant triad only reaches28% daughter energy and exports less total energy
than the omitted-inertia control by100Myr. The actual outgoing field generates
a reactive frequency shift; satisfying only the bare resonance is insufficient.

Let D be the static overlap kernel of the same normalized radial source profile.
For parent frequency Omega and coherent opposite-mode pairs, the leading
reactive envelope Hamiltonian is

 Hreact=-Lambda |O|², Lambda=16g2² Omega²D/c²,
 O=sum_parent A² b_k b_-k.

With two initially equal coherent parent pairs of occupation N0,

 deltaOmega_parent=-2Lambda A^4 N0.

The wave calculation does not insert this approximate force separately: its
field already supplies the full reaction. This formula predicts which fixed
angles to test. At approximately doubled daughter frequency, its reactive
shift grows as the parent population depletes. To leading quantum-wave order,
writing f=N_daughter/N0, the effective detuning is

 Delta_eff ~= Delta_bare+4Lambda A^4N0(1-2f).

Matching the initial state alone gives Delta_bare=-4Lambda A^4N0. Centering the
detuning over0<=f<=1/2 instead gives half that shift. The latter minimizes the
largest detuning in that interval within this approximation. Actual tests use
the full time-dependent reciprocal field, not this envelope formula.

For the already specified benchmark near3kpc, g2=171.680273197, initial weak
normalization5%, D=6.97735805 in dimensionless units. The prediction is
parent shift-0.01940246rad/Myr. The two constant angles are90.460908deg
(half compensation) and90.983027deg (full initial compensation), obtained from
Omega(k1+k2) with both parent |k| fixed. They are available geometries in the
stated local3D continuation, not a fitted galaxy-law parameter.

By150Myr:

| Fixed geometry | Max daughter energy | Actual outgoing absorption |
|---|---:|---:|
| Bare linear resonance |27.7925%|3.70176%|
| Half predicted nonlinear shift |64.7862%|5.03080%|
| Full predicted initial shift |41.5588%|4.05270%|

All energies are fractions of the same initial local mode energy. Total-energy
errors are at most5.4e-10 relative in these runs. A separate half-step check
for the half-shift case is recorded in run_wave_shift_time/results.json.
This gives a finite region of improved local transfer/export, not a full
phase-space coverage theorem or proof that an actual infall populates it.

A useful diagnostic explains the cooling tradeoff. In the high-k regime with
coherent degenerate parents, Qosc/E is proportional1/Omega, so averaged
radiation power at fixed geometry is proportional Omega² E². If fraction f
moves to a daughter of frequency ratio r, ignoring small form-factor shifts,

 P/P_initial ~= (1-f)²+r²f².

For r near2, instantaneous power exceeds its original value only for f>0.4.
This is an instantaneous coherent-source approximation, not a guarantee about
integrated cooling. It does explain why modest redistribution can reduce
export, and why crossing into much larger transfer can help. Random phases
change the coherent sums; actual occupation and phase data are still required.

The global mean-flow and angular-seed obligations in MEAN_FLOW_OBLIGATION.md
remain open. Improved export from prepopulated local parents does not assign
any fraction of the full collapse release to this channel.
