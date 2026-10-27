# Controlled source decoupling requires work

2026-10-13. Base checkpoint: 3c0ea2255a5a4215a08c7aec48035b5156d12be1.
This follows the coherent threshold-feedback surrogate. It tests whether its
populated pair sector survives a prescribed removal of source conversion and
accounts for the energy supplied by that removal. It does not establish a
physical switch for the underlying interaction or a stored cold inventory.

## Explicit additional control assumption

Use the same dimensionless Hamiltonian, now with a prescribed real control q:

    H(q)=|a|^2+sum_j epsilon_j |b_j|^2+kappa B^2/2+q C,
    B=sum_j |b_j|^2,
    C=2 Re[a* sum_j v_j b_j].

The common rest energy has been subtracted as in the preceding package.
Physical excess energies per initial source are D0 times these quantities.
The dynamical equations are

    i a'=a+q sum_j v_j b_j,
    i b_j'=(epsilon_j+kappa B)b_j+q v_j a.

Norm remains conserved for real q. The Hamiltonian has explicit time dependence:

    dH/dtau=q'(tau) C(tau),
    W=integral q' C d tau,
    H_final-H_initial=W.

An instantaneous parameter change at fixed state instead gives exactly

    Delta W=(q_after-q_before) C.

The imposed q is an EXTRA control, absent from the original constant-coupling
action. Turning off an external photon pump does not generally set the
fundamental R-phi interaction to zero: already-created R particles can still
convert. Spatial separation could reduce overlap for some processes, but this
momentum-only model has no geometry or outgoing-wave boundary condition to
derive such a q. Accordingly this is a conditional decoupling diagnostic, not
an apparatus proposal or a demonstrated extraction protocol.

## Protocol and results

Prepare the L=5 surrogate at q=1 until tau=tau_star=53.5262762291, using the
same bare source initial state as before. Its pair-sector weight at that time is

    B_start/fstar=1.04754895,  fstar=1.6604056498e-5.

For each independent run, ramp

    q(tau_start+u)=cos^2[pi u/(2T)], 0<=u<=T,

then hold q=0. Also test an instantaneous quench T=0. Keep kappa fixed
throughout. The physical time unit under the inherited calibration is
hbar/D0, about 0.02883 ns. These are dimensionless control trials, not timing
requirements for a demonstrated laboratory device.

| Ramp duration T | Final B/fstar | Final B/B_start | Work/(D0 fstar) |
|---:|---:|---:|---:|
| 0 | 1.047549 | 1.000000 | +0.052081 |
| 0.1 | 1.047591 | 1.000040 | +0.051820 |
| 1 | 1.046521 | 0.999018 | +0.044696 |
| 10 | 1.036004 | 0.988979 | +0.031331 |
| 50 | 1.008653 | 0.962870 | +0.026742 |

Most of the initial pair-sector weight survives these particular ramps. The
short T=0.1 ramp produces slightly more weight than it started with, so the
ratio is not universally a survival probability or a monotone function of
duration. The tested T=50 ramp is not a proved adiabatic limit.

At q=0, each b_j obeys only a real diagonal phase equation, hence every
|b_j|^2 remains fixed in this surrogate. An additional hold of length 10 in
dimensionless time confirms that numerical implementation. No open-system
loss, spatial escape, scattering into additional modes or reconnection to a
source is represented by this hold.

All tested ramps require positive work. For the sudden quench this follows
directly from the initially negative coherent interaction energy:

    W=-C_start=+0.0520808 D0 fstar.

Removing a negative interaction contribution increases the system's energy.
It is not a zero-work projection that magically converts dressing into free
particles. This sign statement for the sudden quench follows from C_start<0;
no universal sign theorem for every possible dynamical ramp is claimed.

## The surviving sector is still interacting

Setting q=0 removes source conversion but leaves kappa B^2/2. For the sudden
quench, the remaining kinetic and repulsive energies are respectively about
0.550954 and 0.548679 in units of D0*fstar. A free-particle interpretation
must address the residual repulsion as well as source decoupling.

If one additionally assumes an isolated dilution in which all that repulsive
energy becomes carrier kinetic energy, with no energy lost to other channels,
the available mean kinetic-energy budget per pair is

    E_pair_budget=D0*[sum_j epsilon_j |b_j|^2+kappa B^2/2]/B.

Across the ramps this ranges from 2.344e-5 to 2.397e-5 eV. This is an energy
budget under a separate assumption, not a simulation of expansion or a
prediction of a final velocity distribution. The JSON field
relative_pair_energy_if_isolated_dilution_eV denotes this budget; it does not
resolve how expansion partitions energy between relative and collective motion.
External work or energy export during actual expansion would change it.

In particular, the original calibration came from a T=2 MeV source bath.
The surrogate includes no parent center-of-mass thermal momentum distribution.
Small energies measured relative to a pair threshold therefore do NOT imply
a cold laboratory population. A freely moving parent transfers its bulk
momentum to the daughters. Nor has a barrier or material reservoir been
supplied to contain the released population.

## Checks, evidence and formal scope

The work calculation uses explicit small parameter jumps to the midpoint q,
Hamiltonian evolution with that q fixed, and a jump to the endpoint q. Work at
each jump is exactly Delta q*C for the current state; it is not inferred by
subtracting the total final and initial energies. This supplies an independent
check of the energy-work balance. The smooth ramp is approached as the step
is refined. The fixed-q subflow is the same symmetric diagonal/rotation
splitting audited in the preceding package.

Thirty-two bounded checks pass:

- Reproduction of the preceding preparation population.
- Population constancy after decoupling, norm conservation, and work balance
  for each of nine ramp executions (five primary, three refined and one with
  a refined grid/cutoff).
- Two time-refinement comparisons and two grid/cutoff comparisons.

The largest main-run work-balance residual is below 2.3e-6 D0*fstar. Halving
the requested step from 0.01 to 0.005 changes final B by less than 4.3e-7 fstar
and switching work by less than 1.8e-6 D0*fstar in the three checked ramps.
The grid comparison uses 4096 modes/cutoff 120 against 8192 modes/cutoff 160
for T=50. These checks cover the stated finite window and L=5 spectral shape.

WorkIdentities.lean formalizes the fixed-state work difference, its conditional
sign, and retention of the repulsive energy term. The lemmas do not establish
physical control of q, continuum convergence, or the validity of the thermal
surrogate. Compilation output and source hash are recorded separately. The
run manifest pins the preceding calibration/results file and this script.

## Research consequence

The new result resolves a limited ambiguity: within the surrogate, most pair
weight can persist after an imposed source decoupling, and the associated
work is finite, positive in these trials, and explicitly accounted for.
It does not resolve the main manufacturing gap. There is no derivation of the
control q from an admissible external field or source geometry, no conversion
of the hot-bath calculation into a cold lab source, and no working confinement.

The next physical route should keep the fundamental coupling fixed and model
finite source geometry/outgoing states or a justified external change in
detuning. Repeating q ramps without supplying that mapping would only improve
an artificial control model, not establish creation and storage. This control
route is conditional; the actual source preparation and collection route
remains open.

Reproduce:

    OPENBLAS_NUM_THREADS=1 python3 sol61_push/source_decoupling_work_2026_10_13/check.py /tmp/source_decoupling_results.json
