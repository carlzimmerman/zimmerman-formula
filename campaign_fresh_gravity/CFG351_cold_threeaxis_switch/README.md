# CFG351: a switch that reads the cold component's three-axis shell crossing (full-rank sigma_c)

Criteria: `FROZEN_CRITERIA.md` (commit b88c8e84f, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; no DM particle (the cold MASS is still required; this lane describes its phase-space state).
**Owner decision 2026-10-06 (verbatim in the frozen file): "yeah let the switch read the cold component".** MS1 is
relaxed for this exploration only. **Under the original MS1, every route here is NOT ADMISSIBLE.**

**Verdict (frozen rule): PARTIAL (R-3, 4 of 5, 0 constants).** The switch passes (a), (a'), (b) and conservation. It
fails the edge: the full-rank region ends at the SECOND caustic, 0.232 r_ta, below the frozen >= 0.3 r_ta line and
136-2543 kpc inside B's turnaround edge. The smooth route R-3s is NO-GO (3 of 5). This is a scoped result, not a closure.

## The switch, its action, and the B extension
- sigma_c,ij(x) = sum_s w_s (v_s - vbar)_i (v_s - vbar)_j, the fine-grained stream sum of the cold phase-space sheet
  (no smoothing scale).
- **R-3:** f = H(det sigma_c), 0 constants. **R-3s:** f = 27 det/(tr)^3, 0 constants. **MUTATE:** f = H(tr sigma_c).
- Action: L = L_cold(Vlasov-Poisson sheet) + L_gas + f(sigma_c) L_M. f is a state function, so the action is ordinary.
  For R-3, sigma adj(sigma) = det I, so the switch stress -2 L_M sigma df/dsigma = det delta(det) = 0. And adj(sigma)
  kills every stream offset on rank-deficient states. So **R-3 exerts no force or momentum on the cold component.**
- **Extension cost (structural, 0 constants):**
  - B's cold component becomes a full phase-space (Vlasov) sheet, not dust.
  - The 10-moment closure keeps rank invariant (sigma = G sigma0 G^T), so rank can only change in the kinetic caustic step.
  - The initial state must be exactly cold. A4: any primordial isotropic dispersion eps I turns both routes fully ON
    on FRW for every eps > 0. So R-3 is discontinuous in the initial data at eps = 0.

## Results (24 DE12 hosts, both footings)
| test | R-3 H(det) | R-3s 27det/tr^3 | under MS1 |
|---|---|---|---|
| (a) FRW/linear | PASS | PASS | n/a |
| (a') sheets/filaments | PASS | PASS | n/a |
| (b) bound + fidelity | PASS | FAIL (B3: f dips 6e-4) | n/a |
| (c) transition + edge | FAIL (edge 0.232 r_ta) | FAIL (edge; chi up to 19) | n/a |
| (d) conservation | PASS | PASS | n/a |
| tier | **PARTIAL** | NO-GO | NOT ADMISSIBLE |

- **(a) FRW / linear.** The closure keeps sigma_c0 = 0 exactly 0 (sigma0 > 0 follows a^-2 to <1e-8). 1D Zel'dovich
  at D A = 0.9 has 1 stream and sigma exactly 0. L341 growth with f = 0 gives D/D_LCDM = 1.00000000, sigma_8 0.8101,
  on both footings.
- **(a') Unbound web.** Separable 3-axis Zel'dovich, A = (1, 0.7, 0.45), 343 points per stage. The numerical rank
  equals the number of multistream axes at every point:
  - sheet (D 1.3): rank 1, f = 0;
  - filament (D 1.8): rank 2, f_R3 = 0, f_R3s 1e-31;
  - knot (D 2.6): rank 3 at 49 points, f_R3 = 1.
- **Is third-axis crossing a proxy for "bound"?** It is sufficient but late (Lean T11):
  - In ZA (EdS) each axis turns around at lambda D = 1/2 and crosses at 1, a lag of x2 in D (x2.83 in time).
  - In a top-hat, turnaround is at delta_lin 1.062 and collapse at 1.686.
  - So matter that has turned around and is falling in, but has not crossed, is bound and still OFF.
- **A'3 (reported).** With CDM-like small-scale structure, collapsed sub-clumps inside sheets are full rank and ON
  locally, while the diffuse sheet stream stays OFF. This needs the pointwise (fine-grained) reading.
- **(b) Bound.**
  - Isotropic Jeans sigma_r(30 kpc) is 54-440 km/s. 30 kpc is inside r_rank3 on 24/24 hosts (r_rank3 = 41-769 kpc;
    the tightest is the smallest host, 41 kpc).
  - Fidelity: a 10% gas compression reaches the cold component only through gravity. The bound on the gas-mass share at
    30 kpc is 0.053-0.595. sigma_c^2 responds by at most 4.4% (gas, CFG350: 6.6%).
  - det > 0 throughout, so R-3 has df = 0, dev 0 and 0 flips (rank is invariant under any invertible congruence;
    Lean T6b).
  - R-3s has dev 1.2e-3 but dips by 6e-4 under anisotropic deformation, which fails the frozen no-decrease line B3.
- **(c) Transition / edge.**
  - C1: strongly hyperbolic on 1000 full-rank states. Random rank-1/2 states (P_xx != 0) also have 10 eigenvectors, so
    the Jordan block is only dust's sigma = 0. Rank is invariant under 3000 congruences, so the 2 -> 3 change is a
    kinetic caustic event and never a closure step.
  - C2: R-3 stress is 0 identically. For R-3s, chi = 0 at isotropy, but in the anisotropic worst case it is up to 4.2
    at 30 kpc and 19.5 at the edge.
  - C3: OFF on FRW, in voids, and in sheets/filaments.
  - **Edge.** N streams give rank <= N-1, so full rank needs >= 4 streams; spherical counts are odd, so >= 5. A
    self-similar Bertschinger iteration (EdS, delta M/M ∝ M^-1, small angular-momentum regulator alpha = 0.1) gives:
    - caustics at 0.359 r_ta (K3: Bertschinger 1985 quotes 0.364, so 1.4% off), 0.232 and 0.176;
    - so the full-rank region is r < 0.232 r_ta, which **FAILS the frozen >= 0.3 r_ta line**;
    - the offset from B's turnaround edge is 136-2543 kpc (0/24 within 100 kpc).
  - Edge width: R-3 is a step at a fold caustic, so its width is zero.
  - CFG337's ell_min came from a switch field's gradient energy. A state function has no gradient energy, so that
    obstruction does not arise in that form. But R-3's front impulse |L_M|/(rho_c sigma_c^2) at the edge is
    0.06-9.8 (reported), so the energy exchanged at the rank front is not small on the largest hosts.
- **(d) Conservation.** sympy gives 0 momentum and energy residuals in the conservative 10-moment form. The action is
  ordinary, with no multiplier. On 1000 random three-stream points, max |adj(sigma)(v_s - vbar)| = 2e-16.

## Ownership and the UFD link (reported)
- **Class E (GCs, wide binaries):** they sit inside the host's full-rank sigma_c, so f = 1 at their positions. The
  switch cannot make them Newtonian. That needs the ownership rule unchanged (CFG333 R2: no own cold clump, no own
  phantom). Read literally, "the outermost bound system owns the phantom" would also strip satellite dSphs (class A),
  so R2 is the working rule. The switch neither supplies R2 nor breaks it.
- **Class A dwarfs:** they have their own full-rank clump, so ON.
- **UFD link:** CFG344's CDM-like cold structure is consistent. The exact coldness that (a) needs gives small-scale
  clumps, and UFD clumps are full rank, so ON.

## Constants
R-3: 0, and R-3s: 0, beyond kappa = 1/2. The cost is structural: a Vlasov sheet instead of dust, a kinetic caustic
step, and exact primordial coldness.

## Controls
- K1: FRW sigma_c = 0 stays exactly 0.
- K2: sheet rank 1, filament rank 2, isotropic (isothermal-type) sigma full rank.
- K3: first caustic 0.359 vs 0.364.
- MUTATE (H(tr)): ON in the Zel'dovich sheet, which reproduces CFG350's R-c failure (rc 1).

## Lean
`CFG351_threeaxis_certificates.lean`: 17 theorems, no sorry, standard axioms only, rc 0 (`.out`). They cover:
- single-stream invariance;
- det = 0 for sheet, two-axis and three-stream states;
- isotropic det > 0, with smooth f = 1;
- congruence det law and rank invariance both ways;
- FRW-off; MUTATE ON on a sheet;
- sigma adj sigma = det I (stress 0), and no force;
- conservative telescoping;
- 0 <= 27abc <= (a+b+c)^3;
- crossing implies turnaround (ZA).

## Deviation from the frozen file
Section 4 named a direct numpy shell run (softened, radial). Run as a test, it heated numerically: shells escaped past
r_ta. So the caustic radii come from Bertschinger's own self-similar iteration, with a small angular-momentum regulator
(alpha = 0.1, numerical, not a theory constant). K3 validates the replacement (first caustic within 1.4%). The
>= 5-stream reading of the frozen file is unchanged.

## Run
```
python3 campaign_fresh_gravity/CFG351_cold_threeaxis_switch/cfg351_threeaxis_switch.py > campaign_fresh_gravity/CFG351_cold_threeaxis_switch/cfg351_threeaxis_switch.out   # rc 0, ~250 s
CFG351_MUTATE=1 python3 campaign_fresh_gravity/CFG351_cold_threeaxis_switch/cfg351_threeaxis_switch.py > campaign_fresh_gravity/CFG351_cold_threeaxis_switch/cfg351_threeaxis_switch_MUTATE.out   # rc 1 (mutation detected), ~30 s
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG351_cold_threeaxis_switch/CFG351_threeaxis_certificates.lean
```

**Scope:**
- The spherical self-similar model sets the edge. Real halos are triaxial with substructure, so their multi-stream
  boundary may differ, but rank 3 still needs >= 4 streams.
- The Jeans sigma is isotropic and Newtonian; only its positivity is used.
- The gas-share bound puts all baryons inside 30 kpc.
- |L_M| ~ g_ph^2/(8 pi G), as in CFG350.
- Bertschinger's 0.364 is quoted, not re-read.
