# CFG558: velocity part: is isotropy forced, overfill removal, α by the age

**Result:**
- **ISOTROPY CHOSEN.** The dissipative bracket is rotation-invariant in velocity and fixes no temperature by itself. The
  scalar constraint follows only from one added principle, which Pb does not imply.
- **OVERFILL NOT HANDLED.** The knob-free overfill rule (V3) leaves P at 0.38–0.43, and it blows up the cluster cells.
- **NOT α-ROBUST.** In the MW cells α×0.5 settles by 13.8 Gyr but fails the edge. The cluster cells fail at every α (V3 blow-up).
- **Overall: VELOCITY PART INCONSISTENT**, because the frozen V3 fails G550, energy and blow-up in the clusters at α = 1.
- **Full-system Lyapunov: NOT ESTABLISHED.**
- FIX-2 (CFG554 b) is unchanged as the working candidate. Its target is still POSITED.

κ = ½ is fitted. The footings (9.3603e-11 can / 1.1312e-10 alt) are never pooled. The cold energy's mass is still required.
No dark-matter particle. This is not a closed theory. Every number below is from `cfg558_results.json`,
`cfg558_results_MUTATE.json` or `cfg558_diag.json`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (f6b7ced5d).
- **Equations:** `VELOCITY_PART_v3.md`.
- **Scripts:**
  - `cfg558.py`. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg558.py`, 4 processes, exit 0.
  - `CFG558_MUTATE=1` exits 1, as designed: both teeth bite.
  - `cfg558_diag.py`: post-freeze diagnostic; no label depends on it.
- **Bench:** CFG544's toy, imported unchanged through CFG554's module.
- **Controls pass:**
  - C2: pure Vlasov, all 4 cells.
  - C5: with the cap off, the code reproduces CFG544's fix2_C exactly (Δ = 0).
  - C8: the identity holds (difference 0).
  - Mass is exact in every run.

## Q1: is the scalar (isotropic) constraint forced? CHOSEN

Every sympy item passes (I1–I5):
- **I1.** δE/δf = v²/2 + Φ and the pair weight Δ(v²/2) are invariant under a general rotation. The pair weight reaches the
  second moment only through its trace. The position block's drive −ψ/Θ (round ψ) does not depend on v.
  - So argument (i) holds as stated: M built from the scalar ψ and δE couples only to ρ and tr Π.
- **I2.** Every rotation-invariant linear constraint on Π_ij is a constraint on tr Π (the invariant A is a·I).
- **I3.** At fixed trace, entropy is maximised by an isotropic covariance.
- **I4 (argument ii).** Maximise S_B with only what the bracket conserves (ρ(x), tangential momentum). The energy goes to the
  zero-entropy partner. The stationary point is not normalisable.
  - **So the bracket alone fixes no temperature profile.** The profile has to be imported from the reversible flow L.
- **I5.** The tensor multiplier term is rotation-invariant iff the state is isothermal.

**Why this is not "forced" (argument iii stands).**
- What L supplies is the tensor moment ∂_t(ρu) = −J, which is the framework's own exact stationarity statement.
- Using its rotation average (tr Π/3)·I instead gives FIX-2's target. That choice amounts to one principle: an equivariant
  bracket uses only invariant constraints.
- No committed element implies that principle:
  - the velocity block is valid for any reference measure (CFG550/554 S2);
  - roundness acts on the position block, and in spherical symmetry the tensor condition is already a single radial
    condition;
  - G9 holds either way.
- This structural audit is recorded as an argued item (`Q1_structural_refutation_of_tensor = false`, with its reasons in
  `Q1_structural_note`), not as a sympy proof.

**The bench selects the scalar constraint but does not force it.** MUTATE MI swaps in CFG554's tensor solver, run on ρ̂:
- It fails G550 in both cluster cells: log X_J −0.167 / +0.121, D −0.185 / −0.191.
- In the MW cells it passes.

**Toy (iii), α = 1 end states (MW):**
- The realised state is mildly radial, median β +0.04 to +0.06, even though the reference is isotropic.
- Tensor and scalar Jeans residuals are comparable (0.077–0.089 against 0.032–0.080) at the toy's noise level. Collisionless
  dynamics keeps some orbital anisotropy against an isotropic reference.

## Q2: overfill: NOT HANDLED

The V3 rule: σ_*² = P̂/ρ̂, with ρ̂ = min(ρ_c, ρ_ph) and P̂ = ∫_r ρ̂ g (real-mass field, G9). It has no constant.

| | MW can | MW alt | cluster can | cluster alt |
|---|---|---|---|---|
| P (5 Gyr) | 0.383 | 0.396 | 0.377 | 0.426 |
| FIX-2 P (MUTATE MO) | 0.427 | 0.427 | 0.339 | 0.301 |
| G550 α = 1, IC-B / IC-C | pass / pass | pass / pass | FAIL / FAIL | FAIL / FAIL |
| edge IC-B / IC-C | +0.221 / +0.232 | +0.252 / +0.268 | **+9.36 / +6.47** | **+9.89 / +7.01** |
| energy (IC-B net / IC-C whole history) | +0.243 / +0.247 | +0.266 / +0.268 | blow-up | blow-up |

**Mechanism 1: P is barely changed in MW.** The excess-pressure force is −P̂∇q:
- it smooths gradients of q = ρ_c/ρ̂;
- it does not act on a uniform overfill;
- at r_*, where the mass would have to leave, P̂ is small.

So the injected mass spreads inside r_* rather than leaving it. P falls only from 0.43 to 0.38–0.40.

**Mechanism 2: the clusters blow up** (verified in `cfg558_diag.json`).
- In the point-mass core the law's ρ_ph is tiny. A bin there holding only 2 particles reads ρ_c/ρ_ph = 12.9 (can) / 9.5 (alt).
- σ_*² = P̂/ρ̂ then reaches 51.4 / 40.9 V_f², which is 10.9 / 7.9 × FIX-2's value.
- The heated particles escape, the tail runs away, and r_99 grows from 0.99 to 52 r_* by 2.5 Gyr (cluster_can over_base).
- The trigger is shot noise. The flaw is structural: P̂/ρ̂ is unbounded wherever ρ_ph ≪ ρ_c with P̂ > 0.
- In MW the same quantity stays at 0.93–0.94 × FIX-2, and no MW run blows up.

**Status of the cap.** It projects ρ_c onto T1 (ρ_c ≤ ρ_ph), which is the law's inequality. Using the hydrostatic temperature
of that projection is a declared choice, not a derivation. The point is moot because V3 fails.

## Q3: α by the age: NOT α-ROBUST

The gate at 13.8 Gyr requires |log X_J| ≤ 0.05, |D| ≤ 0.05, steady over 2 Gyr, and the edge within its allowance.

| | α×0.5 B / C | α×1 B / C | α×2 B / C |
|---|---|---|---|
| MW can | FAIL (edge +0.465) / FAIL (edge +0.741) | pass / pass | pass / pass |
| MW alt | FAIL (edge +0.526) / FAIL (edge +0.693) | pass / pass | pass / pass |
| clusters | FAIL (blow-up) | FAIL (blow-up) | FAIL (blow-up) |

- **MW at α×0.5:** the profile and dispersion do settle by 13.8 Gyr.
  - |log X_J| ≤ 0.027, |D| ≤ 0.038, and the changes over the preceding 2 Gyr are ≤ 0.044.
  - This is new relative to CFG554, which stopped at 10 Gyr.
  - The failure is the edge. Kinetic softening grows as α falls: r_99 reaches 1.67–2.06 r_* against allowances of
    +0.355 / +0.433 in ln r_99.
- **t90 (MW, IC-B):** 6.99 / 6.27 Gyr at α×0.5, 4.24 / 3.76 at α×1, 2.25 / 2.01 at α×2 (can / alt). That is roughly ∝ 1/α.
  - t_band is 13.2 / 12.8, 5.2 / 4.8 and 3.0 / 2.8 Gyr.
  - IC-C t90 (log X_J) is 0.25–0.75 Gyr.
- **α×0.25 (MUTATE, reported):** MW IC-B is not settled by 13.8 Gyr (D +0.121 / +0.062; t90 9.48 / 8.78 Gyr). MW IC-C has
  edge +1.72 / +1.86. The clusters blow up.
- **Physical reading (MW):** α ≳ 1 settles well within the age. Below that, the edge spreads beyond the allowance.

## Checks

| check | result |
|---|---|
| G9 | holds: the target field is real mass only; ρ_ph is only the T1 comparison |
| Energy | COMPATIBLE in MW: IC-B +0.243 / +0.266, IC-C whole history +0.247 / +0.268. FAILS in the clusters (blow-up). |
| H-theorem of the relaxation sub-step | S2′ (nonlocal reference) PASS. The moment KL drops across the relaxation step in 75–100% of sampled snapshots (mean 93%). The misses have not been diagnosed; finite-N sampling noise is the likely cause. |
| Angular momentum | the rotating-shell test keeps J to 9.6e-16 (S3) |
| Full-system Lyapunov | NOT ESTABLISHED: dL/dt has a maximum A²/(4Cα) − Bα > 0 for small α |
| Integrator error and mass | MW integrator error ≤ 1.1e-2; mass exact everywhere |

## MUTATE (exit 1: both teeth bite)

- **MI (tensor swapped in): bites.** Both cluster cells fail G550. **Disclosure:** the tensor solver applied to ρ̂ fails to
  bracket in 98.9% / 99.0% of the cluster steps, so those steps get no relaxation.
  - The bite therefore comes from infeasibility, not from CFG554 (a)'s hot-tail mechanism: the edge here is +0.49 / +0.53, not
    +1.80 / +1.92.
  - "Reproduce CFG554 (a)'s cluster failure" is met as a G550 failure, not as a mechanism.
- **MO (overfill rule removed, which is FIX-2): bites.** P = 0.427 / 0.427 / 0.339 / 0.301, all > 0.2. These match CFG554 (b).

## Disclosures (dated 2026-10-10; the frozen text is not edited)

- **The bench kernel** is CFG544's analytic ν (unchanged import). It equals ν_mono at the toy's y (≤ 2.5), as CFG544/554 note.
- **The Q1 structural refutation** is an argued audit item, encoded in the script as a boolean with its reasons. The sympy items
  I1–I5 are proofs. The criteria required a structural refutation for FORCED, and none was found.
- **The overfilled-bin fraction is 0.43–0.69 even in MW**, because of Poisson noise. The cap is active in noise-overfilled
  bins. In MW this lowers σ_*² only slightly; in the point-mass core it is the blow-up trigger.
- **`cfg558_diag.py`** was written after the run to verify the blow-up mechanism.

## Plain reading

- Isotropy is not forced by the framework's structure. The dissipative side is isotropic but blind to temperature. The
  temperature has to come from the reversible side, which is tensorial. Choosing the isotropic (rotation-averaged) version is
  one clean principle, and the bench prefers it.
- The obvious knob-free overfill fix, which heats overfilled matter to the temperature of the law-admissible density, does
  not move overfill out of r_*. Where the law's density vanishes it is unbounded, which destroys the clusters.
- FIX-2 stays the working candidate, with its target POSITED. Overfill and the low-α edge remain open, and so does a
  full-system Lyapunov function.
