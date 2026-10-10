# CFG542: one dissipative variational principle for candidate B

**Bottom line.**
- One statement (a metriplectic/GENERIC principle, **Pb**) yields the cold-energy settling flow and its energy sink, with Q in
  closed form.
- It does **not** yield "bound": the switch stays an **INPUT**. What the principle settles is where the switch may sit. Placed in
  the free energy and reading the cold energy (CFG541's E8), it leaks, which **conflicts with MS1**. Placed in the mobility, or
  reading baryons only, it does not leak.
- α stays **O(1) FREE**. No balance or fluctuation–dissipation relation can fix it; causality only bounds it (α ≤ 1 at β = 1).
- The inertial completion **Pb*** (the candidate fix for diffuse reservoirs) is **INCONSISTENT**. Inertia plus the one-sided
  deficit drives the cold energy into the core, the edge is lost, and the extended Lyapunov function rises.

κ = ½ is fitted. The footings (9.3603e-11 / 1.1312e-10, can / alt) are never pooled. The cold energy's mass is still required.
No dark-matter particle. This is not a closed theory. Numbers are read from `cfg542_results.json` / `cfg542_results_MUTATE.json`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first in 3d435f032.
- **The principle written out:** `ACTION.md`.
- **Script:** `cfg542.py` (sympy plus 1-D spherical numerics; CFG541's `Model` class imported read-only).
  - Run with `OMP_NUM_THREADS=2 nice -n 10 python3 cfg542.py`. It takes about 11 min and exits 0.
  - `CFG542_MUTATE=1` writes the `_MUTATE` outputs and exits 1, as designed: all four teeth bite.
  - Data: the DESI DR2 w0wa chains already on disk (CFG508's copy). Nothing was downloaded. CFG539 and CFG541 were not touched.

## Labels

| principle | label | α | Q | switch |
|---|---|---|---|---|
| **Pa** Schwinger–Keldysh / MSR open-system action (+ dark-energy scalar φ) | **CONSISTENT WITH OPEN ITEMS** | **FREE** | DERIVED (same as Pb) | INPUT |
| **Pb** metriplectic Onsager principle + coherent dark-energy partner φ | **CONSISTENT WITH OPEN ITEMS** | **FREE** (causality bound αβq < 1) | **DERIVED: Q = ρ_c α τ_ff 1_B 1_C ∇ψ·∇Φ** | INPUT |
| **Pb*** Pb + inertial slip, relaxation time α τ_ff | **INCONSISTENT** (K4: Lyapunov rises; edge collapses) | FREE (bound qα(α + β) < 1) | DERIVED: −ρ_c w·∇Φ | INPUT |
| **Pc1** conservative force −∇ψ + friction on the cold energy's own velocity | **INCONSISTENT** | — | — | — |
| **Pc2** −∇ψ carried by a healthy dynamical field | **INCONSISTENT** | — | — | — |

Pa and Pb share the same deterministic content. Pa adds the noise that KMS/FDR ties to the mobility.

## Checks

| check | result |
|---|---|
| K0 control | CFG541's `Model.run` reproduces CFG541's MW t90(α = 1) = 10.010189 Gyr exactly: **PASS** |
| K1 class-A limit | MSR response variation gives the drift; the GENERIC flux is J = −(m/Θ)Δψ; Pb*'s overdamped limit gives class A: **PASS** |
| K2 energy | sympy: M·δE = 0 and dE/dt = 0 exactly; the φ energy identity holds. 1-D: ∫Q dt / ΔW = 1.0004–1.0009 (overdamped), 1.0000–1.0005 (slip): **PASS** |
| K3 G9 | flux form; 1-D \|dM\|/M ≤ 4.5e-14: **PASS** |
| K4 Lyapunov | sympy: dS/dt = Σ m(Δψ/Θ)² ≥ 0 (Pb); the extended identity for Pb* holds where dF/dρ_c = ψ. 1-D overdamped: largest step dF/F₀ ≤ −5e-15 (PASS). 1-D slip: F + K_w **rises** by up to 1.4e-2 of F₀ per sample (**FLAG → Pb* INCONSISTENT**) |
| K5 α | **FREE**. Energy balance is homogeneous of degree 1 in α. The Onsager–Machlup fluctuation relation and the Fokker–Planck equilibrium are independent of the mobility. A bath gives friction ∝ g² |
| K6 Q | **DERIVED**: Q = ρ_c α τ_ff 1_B 1_C ∇ψ·∇Φ, ≥ 0 in spherical symmetry; φ̈ + 3Hφ̇ − c²∇²φ + V′ = Q/φ̇ |
| K7 a₀ tracking | Q/E_sink ≤ 3.65 (Q takes all of ΔW); cosmic Δρ_DE/ρ_DE 8.2e-6; Δlog₁₀a₀ 1.8e-6 (ρ fork), 4.3e-6 (−p fork) against 4e-3: **PASS** |
| K8 non-clustering | Pb: outgoing x ≤ 6.1e-5, near field ≪ 1e-3: **PASS**. Pb*: the collapsed cores radiate, x up to ~5e3: **FAIL** |
| K9 causality | Pb with damped ψ: stable iff αβq < 1, so α_max = 1 (β = 1, q → 1) and 1.186 at q = 1 − f_b. Pb*: K → 0 needs qα(α + β) < 1, so α_max = 0.618 (q → 1) and 0.699 (q = 1 − f_b). Both **CAUSAL-WITH-τ** within these ranges; scans agree. C1: overdamped cluster drift up to 0.19 c at α = 2 (**FAILS** 1e-2, as in CFG541) |
| K10 DESI | 99.8–100% of each chain's weight crosses w = −1 (median z 0.36–0.50): **open item**. A canonical partner's Q/φ̇ is singular at the crossing |

## The switch (task 2): INPUT

- **S1.** Gate in F, reading the cold energy (u = ρ_b + ρ_c): the drive gets an extra term ½ s′(u)(ρ_ph − ρ_c)², a **LEAK**. The
  flow could lower F by dissolving bound regions. With a baryon reading the extra term is **0**.
- **S2.** Gate in the mobility only: no leak for any reading.
- **S3.** The GENERIC conditions hold for any support s(x) ≥ 0, so the principle does not pick the region. The candidate θ_b ≤ 0
  (baryon expansion) is zero at turnaround for a top-hat. It also fires in a one-axis Zel'dovich sheet at λ₁a = 3/4, where E8 needs
  λ₂ ≥ τ_ta. It is reported, not adopted.
- **MS1: CONFLICT.** CFG541's E8 reads the tidal tensor of ρ_b + ρ_c. Inside F, that is the matter door's leak.
  - The consistent choices are a baryon-read segmentation (as MS1 requires) or a gate only in the mobility.
  - The round phantom's region segmentation (x_i, the region's own baryons) must read baryons either way.
  - The threshold for a baryon tidal reading is not derived.

## Diffuse reservoirs (task 3): Pb* does not rescue class A

1-D, cold energy at rest in a top-hat, instantaneous ψ, N = 400, three α values.

- **Speeds.**
  - The slip speeds stay near the free-fall scale: max |w| = 231–521 km/s (MW-like) against overdamped 1391–6636 km/s.
  - The sympy bound |w| ≤ √(2 max|ψ|) holds in every run except the cluster at α = 2 (3272 vs 3242 km/s can, 3507 vs 3440 alt). The
    bound assumes a static ψ; here ψ evolves.
  - The cluster at α ≥ 1 reaches 0.0088–0.0117 c.
  - So **INERTIA-LIMITED REGIME: NO** by the frozen rule, narrowly on speed.
- **Rate.** The α sensitivity drops: t90(0.5)/t90(2) = 1.46–1.57, against 4.00 for overdamped.
- **The decisive failure: the edge collapses.** The sub-cell front ends at 0.61–0.67 r_* (α = 0.5), 0.040–0.110 r_* (α = 1) and
  0.001–0.004 r_* (α = 2). ΔW becomes 2.7–917 V_f² M_cat, against 0.77–1.01 for class A.
- **Mechanism (verified as hard as a pass).**
  - Material accelerated by −∇ψ coasts through the deficit zone and merges into the filled core.
  - At overfilled points dF/dρ_c = 0 (right derivative), not ψ. So F does not fall by the ψ-work already paid into the slip, and
    F + K_w rises.
  - The one-sided deficit never pushes the overfill back.
  - Three independent schemes show the same collapse at α = 1 (development runs, not scored; disclosure 1): Lagrangian shells,
    Eulerian face velocities, and the scored momentum-conserving cells.
- **The repair this implies is not tested here.** It would be a two-sided (restoring) deficit, which changes class A's minimiser,
  or a mobility confined to d > 0 for the slip.

## Angular momentum (task 4): CONSERVED, under conditions

- A radial slide w r̂ in the region's baryon-centre frame, plus a_s = −(w/r) v_⊥, conserves each element's j exactly (sympy),
  and leaves the radial velocity unchanged.
- The slide is radial only for a round ψ. That needs a shell-averaged ρ_c in d, which keeps the gradient-flow symmetry.
- A non-radial slide cannot conserve j element by element: (v × v_s)·x ≠ 0 in general.
- The energy rate per element is w(Φ′ − v_⊥²/r). Circular orbits release nothing, and spin-up heats the tangential motion.

## MUTATE (all bite, exit 1)

- **M1 partner removed:** dE/dt ≠ 0 (sympy), |ΔE_N|/|ΔW| = 1.
- **M2 sign flipped:** F rises at every step.
- **M3 thermal partner:** an extra flux m ΔΦ/T_φ shifts stationarity.
- **M4 healthy-scalar reading:** the static energy is −F, so the force is +∇ψ and settling reverses.

## Open items (Pb)

1. α FREE (bounded above by causality).
2. The GENERIC degeneracy L·δS = 0 fails: orbital transport can raise F. F is a Lyapunov function of the drift sub-flow only.
3. The diffuse-reservoir drift speeds (CFG541 item 3) remain. The inertial fix tried here fails.
4. Kinetic consistency (CFG541 item 5) is not supplied, and Q takes the whole ΔW.
5. The switch and the catchment are inputs. Only their admissible placement is fixed.
6. A canonical partner is singular at DESI's w = −1 crossing.
7. C1: overdamped cluster drift speeds exceed 1e-2 c.

## Disclosures (dated 2026-10-09; frozen text not edited)

1. **Development of the Pb* solver, before the scored run.**
   - A first Eulerian face-velocity scheme let w grow without bound on faces next to empty cells (free-fall time of an empty
     cell → ∞). That gave ΔW about 150× class A. Fixed by carrying slip only on faces with a live donor.
   - A Lagrangian 4000-shell scheme had quantisation overfill and a sticky inner boundary.
   - Both also collapsed the edge at α = 1. Neither is scored, and their outputs were not kept.
   - The scored scheme conserves slip momentum in transfers.
2. **K8 aggregation corrected before the final run.** A first full run pooled the overdamped and slip runs into one K8 number.
   The criteria score per principle, and the script now does.
3. **Reading choices.**
   - "max|ψ|" in the speed bound is taken as the maximum over space and time of the run.
   - 1 + w for K8 is the smallest chain median of 1 + w₀, which is 0.161 (Pantheon+).
4. **The 1-D model is the drift sub-flow only:** static baryons, no orbital motion, no expansion (as CFG541).
