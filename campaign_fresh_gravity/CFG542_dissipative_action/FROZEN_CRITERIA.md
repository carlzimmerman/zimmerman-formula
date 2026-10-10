# CFG542 FROZEN CRITERIA -- one dissipative variational principle for candidate B (cold-energy settling, its sink, the switch)

Committed alone, before any script of this lane exists and before any number of this lane is computed. Date 2026-10-09.
Owner-approved lane (queued 10-09).

## Question

CFG541 showed that class A (the cold-energy settling drift) is the Onsager/Wasserstein gradient flow of the deficit field energy
F = (1/8 pi G) int |grad psi|^2 with mobility rho_c alpha tau_ff, once the census edge is removed from the deficit. It left open:
alpha O(1) FREE; the energy sink (only an exchange with DYNAMICAL, non-clustering dark energy allowed, coupling Q not derived);
the overdamped reading fails in diffuse reservoirs; angular momentum not conserved; the switch B and catchment C are field-defined
but not derived. This lane asks whether ONE dissipative principle yields, from a single statement, (1) the settling flow,
(2) its energy sink, (3) a local/covariant definition of "bound", with no knobs.

## Settings (unchanged from the record)

kappa = 1/2 FITTED; a0 = kappa c sqrt(G rho_DE); footings 9.3603e-11 (can) and 1.1312e-10 (alt), never pooled; kernel
nu(y) = 1/(1 - exp(-sqrt y)); no EFE (round per-region phantom, R6/R7); G9 (matter conservation; the cold energy feels the
baryons only through gravity); Omega_c/Omega_b = 5.364 input. No dark-matter particle species. The cold energy's mass is still
required. Not "theory closed". MS1 (owner decision 09-26): the switch reads baryons, never the carrier or curvature.
No downloads; data already on disk only (the DESI DR2 w0wa chains used by CFG508, for item K10). Compute: `nice -n 10`,
<= 2 threads, sympy + small 1-D numerics; NO PM runs. Other lanes are read or imported read-only (CFG541's `Model` class and
results JSON); CFG539 (Stage 2 possibly running) is not touched.

**No knobs.** Every constant must be one of kappa, 5.364/f_b, G, c, rho_DE (via a0), the DE background (w(z), read from the
chains), or an INHERITED item named with its source lane. Any new dimensionless O(1) factor the principle does not fix is
reported as FREE, never tuned.

## Principles to construct (each written out, field equations derived in sympy)

- **Pa -- Schwinger-Keldysh / MSR open-system action.** Cold energy (overdamped drift sub-flow) plus response fields, coupled to
  a dark-energy scalar phi; classical (MSR) limit; dynamical KMS / fluctuation-dissipation imposed. Test whether KMS/FDR fixes
  the mobility, and derive the friction of a linearly coupled bath (Caldeira-Leggett form) to see what sets alpha.
- **Pb -- metriplectic (GENERIC) Onsager principle with a partner field.** State (f_b, f_c, phi, pi_phi); energy
  E = E_N + E_phi; dissipative functional S = -F/Theta; dissipative operator built edge-wise so that M dE = 0 (energy
  degeneracy) and dS/dt >= 0. Derive the drift, Q, the phi equation, and the condition on the partner's temperature.
- **Pb* -- Pb with an inertial (flux-relaxation) slip.** The drift becomes a slip velocity w obeying
  d_t w + (w.grad) w = -grad psi - w/(alpha tau_ff) (relaxation time = the same mobility time; no new constant). Extended
  Lyapunov F + int (1/2) rho_c |w|^2. This is the candidate answer to CFG541 open item 3.
- **Pc -- forced alternatives.** (c1) the conservative single-velocity reading: cold energy feels the real force -grad psi plus
  friction on its velocity; (c2) the conservative reading with psi carried by a healthy dynamical scalar (the CFG541 damped-wave
  completion read as a Lagrangian field): the sign of the induced force.

## Checks (per principle; each PASS / FAIL, numbers from the JSON)

- **K0 (control).** CFG541's `Model.run` (overdamped, imported read-only) reproduces CFG541's JSON t90(alpha = 1) for the MW-like
  Hernquist system (can) to <= 1e-6 relative. If it fails, all 1-D numerics are void.
- **K1 class-A limit.** In the Newtonian, overdamped limit the principle gives exactly v_s = -alpha 1_B 1_C tau grad psi and the
  same stationary set (rho_c grad psi = 0 on B∩C). sympy.
- **K2 energy.** A conserved total energy exists including the partner: sympy identity d(E_N + E_partner)/dt = 0 exactly.
  1-D numerics (reported): the time-integrated local Q agrees with -Delta W within 2%.
- **K3 matter (G9).** Rest mass of each species conserved (flux form; no cold energy converted; baryons untouched by the drift).
  sympy structure + 1-D |dM|/M <= 1e-12.
- **K4 Lyapunov.** dF/dt <= 0 (Pb*: d/dt[F + int rho_c w^2/2] <= 0) on the drift sub-flow, sympy identity. 1-D: largest per-step
  relative increase reported; flagged if > 1e-6 of the initial value.
- **K5 alpha.** FIXED iff a relation inside the principle (energy balance, KMS/FDR, stationarity, causality/stability)
  determines a unique value with no new constant; FREE otherwise. Bounds (e.g. from stability) are reported as bounds, not values.
- **K6 Q.** DERIVED iff a closed local expression in the state fields follows with no added coupling constant; NOT otherwise.
- **K7 a0 tracking.** The energy injected into dark energy, cosmically averaged (CFG541's bound rescaled by this principle's
  energy per settled mass), shifts log10 a0 by <= 4e-3 dex (one tenth of CFG512's +-0.04 dex) on both a0 forks
  (a0 ∝ sqrt(rho_DE) and a0 ∝ sqrt(-p_DE), CFG511).
- **K8 non-clustering.** The partner's local response to Q gives delta rho_DE/rho_DE <= 1e-3 in the MW-like and cluster-like
  systems (computed from the derived phi equation, both the near-field and the outgoing part).
- **K9 causality.** With the CFG541 damped psi wave (tau_psi = beta tau_ff, beta = 1), Routh-Hurwitz stability for every k > 0 and
  every state q = rho_c/rho_m in (0, 1). Label CAUSAL-WITH-tau if a nonzero alpha range is stable in every state (alpha_max
  reported); UNSTABLE if no alpha > 0 is. Nonlinear drift speed (C1, cluster-like) reported against the 1e-2 c margin.
- **K10 partner viability vs DESI.** For a canonical scalar partner, Q enters as Q/phi_dot, singular where w = -1. Report the
  weight fraction of each DESI DR2 chain whose CPL w(z) crosses -1 at z > 0. If > 50% in every chain: open item "a canonical
  partner cannot follow DESI's preferred w(z) through the crossing".

**Labels per principle:** CONSISTENT (K1-K4, K6-K9 pass, nothing open); CONSISTENT WITH OPEN ITEMS (K1-K4 pass; others listed);
INCONSISTENT (K1, K2, K3 or K4 fails; the failure named). Also alpha: FIXED (value, relation) / FREE; Q: DERIVED (form) / NOT.

## The switch (task 2)

- **S1 (sympy).** Gate inside F with reading u: the first variation acquires a term from dF/du du/drho_c. Label LEAK iff nonzero
  when u reads rho_c (total-density tidal reading, CFG541 E8, or curvature/lapse); NO LEAK when u reads baryons only.
- **S2 (sympy).** Gate inside the mobility only: no term in the drive for any reading (state).
- **S3.** Switch DERIVED iff the principle's own equations single out the bound region without an external indicator; INPUT
  otherwise. A covariant candidate (expansion of the baryon congruence, theta_b <= 0) is evaluated: coincidence with turnaround
  for a spherical top-hat, and behaviour for a one-axis (Zel'dovich sheet) collapse; it is reported, not adopted unless derived.
- **MS1 statement.** State CONFLICT / NO CONFLICT for CFG541's E8 (tidal tensor of the total density) inside this principle.

## Diffuse reservoirs (task 3)

1-D spherical runs of Pb* (static baryons, cold energy at rest in a top-hat to r_ta at the cosmic ratio, instantaneous psi; the
CFG541 set-up and grid N = 400), MW-like Hernquist and cluster-like point mass, both footings, alpha = 0.5, 1, 2. Report: max |w|/c,
max Pi, t90, steady r_* vs the analytic value. **INERTIA-LIMITED REGIME: YES** iff (i) the slip speed obeys the sympy bound
|w| <= sqrt(2 max|psi|) in every run, (ii) max |w|/c <= 1e-2 in the cluster-like runs, and (iii) no new constant was added;
otherwise NO. Report the alpha sensitivity t90(0.5)/t90(2) against the overdamped value 4, and whether the edge stays within 2% of
the analytic r_* (else the edge moved, reported with the overfill).

## Angular momentum (task 4)

sympy: a radial slide in the system frame with a velocity-space term a_s chosen so that each element's j = x × v is conserved;
derive a_s (minimal: no radial-velocity change), its energy effect, and the condition on psi (round about the system centre)
under which the drift is radial. Label CONSERVED (conditions) / NOT CONSERVED.

## MUTATE (`CFG542_MUTATE=1`, writes `_MUTATE` outputs; all teeth must bite, exit 1)

- M1 partner removed: E_N alone is not conserved (|Delta E_N|/|Delta W| >= 0.5 detected).
- M2 dissipative sign flipped: F rises (positive per-step increase detected).
- M3 thermal (finite-temperature) partner: the stationary condition shifts off psi = const (sympy: nonzero extra term).
- M4 conservative healthy-scalar reading: the induced force on cold energy points up the deficit gradient (settling reverses).

## Deliverables

`cfg542.py` (writes `cfg542.out`, `cfg542_results.json`; MUTATE writes `cfg542_MUTATE.out`, `cfg542_results_MUTATE.json`),
`ACTION.md` (the principle written out), `README.md`. Results committed with a message starting "CFG542 results:", lane folder
only. Not pushed.
