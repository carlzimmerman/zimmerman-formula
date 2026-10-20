# CFG882: can the cold-energy equations keep a dwarf's clump for a Hubble time?

**Bottom line: RETENTION REQUIRES THE GATE.** With the record's two-sided drift (CFG544 FIX-1 ψ, as written in CFG638), CFG877's clump
drains in about 10 Myr/α. Keeping it for 12 Gyr needs α ≲ 1.4e-3, roughly 400× below the galaxy side's α ≳ 0.5, so retention is
**EXCLUDED** on both footings. With CFG639's deficit gate (drift and OU only where d = ρ_ph − ρ_c > 0), an overfilled region does not
move at all, for any α: the clump is kept exactly, and its σ is a fossil of its formation. The gate never drains overfill anywhere,
though. Big galaxies stay on the law only if the clumped mass is a small enough fraction of their phantom mass, and the equations do
not supply that fraction.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (3a10f28a8), owner block 880–889.
- **Settings:** κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 kept apart, never pooled. ν_e. Cold energy is real gravitating mass,
  no particle species. Framework-native inputs. Not "theory closed". Nothing here says the data favour the framework. No constant
  added. α stays free.
- **Script:** `cfg882.py` (numpy + sympy, one process, under 1 min, < 200 MB).
  - `OMP_NUM_THREADS=1 nice -n 10 python3 cfg882.py` writes `cfg882.out` and `cfg882_results.json` and exits 0.
  - `CFG882_MUTATE=1` (inverted gate) writes `cfg882_MUTATE.out` and `cfg882_results_MUTATE.json` and exits 1 by design.
- **Inputs, read only:** CFG877's clump (V_x 10.655 / 10.587 km/s, M_cl 5.25e6 / 4.24e6 M_⊙, r_c 104 pc, cap r_t 199 / 163 pc);
  CFG881's F_max (D6 only). Nothing downloaded; no other lane edited.

## What is solved

- **Equation:** the record's density sub-flow, ∂ₜρ_c + ∇·(ρ_c v_s) = 0 with v_s = −α τ ∇ψ, ∇²ψ = 4πG(ρ_ph − ρ_c), τ = (4πGρ_m)^(−1/2).
  The gated version multiplies v_s by G = 1[d > 0] at the donor cell.
- **Setup:** spherical, with static Plummer baryons and a static round-rule phantom of the host's own baryons. 1_B 1_C = 1 out to
  20 kpc, with zero flux there.
- **Initial state:** a law-settled halo (ρ_c = ρ_ph) plus CFG877's capped clump.
- **Hosts:** three illustrative Plummer dwarfs, H1 (1e4 M_⊙, 30 pc), H2 (3e5, 200 pc) and H3 (2e7, 700 pc), chosen before the run
  and not fitted to anything.
- **Why the density sub-flow is the right object.**
  - Under FIX-2, the OU target is the hydrostatic (Jeans) dispersion of the current density.
  - K7 shows that the moment system (CFG638) has no stationary counter-flow u = −v_s when overfill is present: steady compression
    heating forces p = ρσ_J²/(1 − q/3), above hydrostatic, with q = ρ_ex/ρ_m.
  - So gravity cannot hold the overfill in place against the drift. The drift-only rate is the record's rate to O(1), and the V1
    margin (×36 below even the lenient floor) absorbs an O(1) change. No kinetic run was made (see the limits).

## Two exact results (sympy K4, K5)

1. **Each radius drains on its own.** ∂ₜM_ex(<r) = −Γ(r) M_ex(<r), with Γ = α 4πG τ ρ_c = α(ρ_c/ρ_m)/τ evaluated at r.
   - The cumulative overfill inside any radius decays monotonically and never changes sign.
   - Its rate is set by the local density at that radius, so the dense clump drains faster than any galaxy halo settles.
2. **A centre bound that holds for any initial state.**
   - At r = 0: ∂ₜρ_ex = −α 4πG τ ρ_c ρ_ex.
   - Therefore ρ_ex(0, t) ≤ ρ*(αt), where I(ρ*) = αt and I(ρ) = ∫_ρ^∞ √(ρ_b + x)/(√(4πG) x²) dx, which equals 2τ(ρ) at ρ_b = 0.
   - For large αt, ρ* → 1/(πGα²t²), whatever the clump started with.
   - At α = 0.5 and 12 Gyr, ρ* = 6.8e-5 M_⊙/pc³ with H2's central baryons (2.0e-6 with no baryons). CFG877's clump centre is
     0.58 M_⊙/pc³. Keeping even half of it needs α ≤ 1.31–1.37e-3.

## Results

**V1: record two-sided drift (ungated). EXCLUDED on both footings.** s_50 is the value of αt at which half of M_ex(<r_t) has left.
α_50 = s_50/12 Gyr. α_c is the centre bound with target ρ_x0/2.

| footing | host | s_50 (Myr) | α_50 | α_90 | α_c (ρ_x0/2) | α_c (ρ_x0) | R(12 Gyr) at α = 1e-3 |
|---|---|---|---|---|---|---|---|
| canonical | H1 | 12.19 | 1.02e-3 | 1.45e-4 | 1.36e-3 | 9.4e-4 | 0.505 |
| canonical | H2 | 10.37 | 8.6e-4 | 1.25e-4 | 1.31e-3 | 9.2e-4 | 0.452 |
| canonical | H3 | 8.67 | 7.2e-4 | 1.06e-4 | 1.31e-3 | 9.2e-4 | 0.390 |
| alt | H1 | 10.09 | 8.4e-4 | 1.19e-4 | 1.37e-3 | 9.5e-4 | 0.445 |
| alt | H2 | 8.58 | 7.2e-4 | 1.03e-4 | 1.31e-3 | 9.3e-4 | 0.389 |
| alt | H3 | 7.42 | 6.2e-4 | 9.0e-5 | 1.32e-3 | 9.3e-4 | 0.337 |

- **The largest value is 1.37e-3, against the floor of 0.05:** ×36 below the lenient floor, ×365 below α ≳ 0.5, and ×490–600 below
  CFG541's idealised α ≥ 0.67–0.83 for t90 ≤ 12 Gyr.
- **At α = 0.05, R(12 Gyr) ≤ 3e-6; at α = 0.5, R ≤ 1.2e-15:** the clump is gone.
- **13.5 Gyr instead of 12 Gyr** (D5): max α_50 9.0e-4 / 7.5e-4, α_c 1.2e-3.
- **More baryons drain the clump faster.** A larger phantom raises ρ_c at r_t, so H3 drains before H1.
- **Scales** (D5, H2, t = 0): τ(ρ_x0) = 5.5 Myr; τ near r_t = 11–14 Myr; ψ_ex(0) ≈ 180–200 (km/s)²; max |v_s| ≈ 10–11 α km/s
  (6–28 α km/s across the hosts).
- **Reading:** the retention α sits on the merger side of CFG623's tension (mergers allow α = 0; the gated α allowed set is {0}
  canonical, {0, 0.03} alt in CFG639). A clump kept by a small α would need galaxies to settle with the same small α, and they
  cannot.

**V2: deficit-gated mobility (CFG639 HG). GATED RETAINS.** R(12 Gyr) = 1.000000 in all 18 cells (3 hosts × 2 footings ×
α ∈ {0.5, 1, 1.186}). No face moves at t = 0.
- This is exact, not numerical. Inside the clump d = −ρ_x < 0, and around it d = 0, so G = 0 everywhere. Drift and OU are both off
  there, and the kinetic equation reduces to Vlasov.
- A clump that is a collisionless equilibrium, f = F(E, L) in the total potential (Jeans theorem), stays for any α. The bath never
  touches it, so its σ is whatever it formed with.
- This is what CFG878 route 2 needs (formation-set σ, later host-blind). It agrees with CFG872's weak host slope
  (s = 0.24 ± 0.16), but that agreement is not tested here.

**Teeth.**
- **M1, inverted gate (MUTATE): BITES.** R = 0.000000 in every cell at every α, and 455–466 faces move at t = 0.
- **M2, gate removed (V1 at α = 0.5): BITES.** R ≤ 1.2e-15 in every cell.
- So retention comes from the gate's sign, not from the solver.

## Step 2: what can still erode a gated clump

- **Phase mixing / collisionless relaxation:** an equilibrium does not phase-mix away. A non-equilibrium clump relaxes in a few
  crossing times and conserves mass. No loss.
- **Tides (D2, flat-host Jacobi estimate):** the clump keeps its identity outside D_crit = √(2V_h² r_t³/(G m)).
  - D_crit is 3.8–5.0 kpc (canonical) and 3.3–4.3 kpc (alt) for hosts of M_b 6e10–1e11 M_⊙.
  - V_h = (G M_b a0)^(1/4) = 165–197 km/s.
  - The range spans clump only and clump plus H2's baryons and phantom.
  - Only satellites with pericentres inside ~4–5 kpc lose their clump. Its mass then spreads as diffuse overfill, which is still
    frozen under the smooth gate.
- **Baryonic potential fluctuations (feedback):** not in the record (open item 7). They need gas mass inside r_t comparable to
  M_cl ≈ 5e6 M_⊙, which is far above the baryon content of faint dwarfs (H1, H2). They could matter in bright dwarfs. Not modelled.
- **The gate's knife edge (D1, diagnostic: the fluctuation level is not derived).**
  - Near a net overfill, ψ' points outward. A cell that becomes even slightly underfilled (d > 0) is pushed outward and
    **empties completely**. Its deficit deepens instead of healing, and nothing flows in from the frozen cells inside it.
  - With 1% or 10% noise in H2's settled halo:
    - 39–45% of the cells between r_t and 2 kpc are emptied (that is, nearly every cell that started with d > 0);
    - without the clump, 0–5% are emptied;
    - the clump interior is untouched (R = 1.0000 in all four runs);
    - M_ex(<1 kpc)/M_cl falls from about 1.00 to 0.91–0.94: halo mass is pushed outward and starts to compensate the clump.
  - The drift-only model shows only the first step. The end state would need orbital re-mixing (not modelled). If that ratchet runs
    to completion, the cumulative mass returns to the law beyond a compensation radius (~1 kpc in H2), while the clump core keeps
    its excess.
  - This is a structural property of the gated equation. It is conditional on fluctuations, and it is not a result.

## Step 3: big galaxies

- **One clump is invisible in big galaxies (D3).** Δg/g_law from one CFG877 clump, canonical:
  - at 1 kpc: 6.0% for M_b 1e7, 1.7% for 1e8, 0.37% for 1e9, 0.05% for 1e10 and 0.005% for 1e11;
  - at 200 pc: 19% for M_b 1e7.
  - A clump matters only in hosts whose dynamical mass inside r½ is a few M_cl, that is, faint dwarfs. This follows from the mass
    ratio alone; no host-scale rule is needed.
- **What has to be bounded is the number of clumps.**
  - The gate conserves overfill exactly (F_ret = 1): disrupted clumps spread but are never removed. So nothing in the equations keeps
    a galaxy assembled from many first-cooling blocks on the law.
  - CFG881's bound then applies directly to φ, the fraction of baryons assembled through first-cooling blocks (D6). It requires
    φ ≤ F_max: about 0.26–0.27 if the clump mass ends up inside 1 kpc (CORE1, ~500 clumps), 0.90–0.92 inside 3 kpc (CORE3), and
    ≥ 2 if it is spread like the baryons or flat.
  - Where it ends up (estimates):
    - Chandrasekhar sinking time (D4): 1.7–2.2 Gyr from 1 kpc, 15–20 Gyr from 3 kpc, 170–220 Gyr from 10 kpc.
    - So clumps that are not already central do not sink on their own.
    - Tides disrupt any clump inside ~4–5 kpc (D2).
    - An intact CORE1 concentration therefore needs clumps carried in by sinking massive satellites. The spread shapes, where
      φ ~ 1 is allowed, look more natural.
- **Does it follow from the equations?**
  - That a single clump does not matter in big galaxies: yes.
  - That big galaxies stay on the law: no. It needs a formation-side condition (φ · 1 ≤ F_max for wherever the clump mass sits) or
    the conditional ratchet above. That condition is **a new assumption**, flagged here and not adopted. The record contains
    neither the number of first-cooling blocks nor their fate.

## Controls (all in `cfg882.out`)

| test | result |
|---|---|
| K1 gated solver with G ≡ 1 = two-sided solver | PASS, max \|Δm\| = 0 |
| K2 mass \|ΔM\|/M ≤ 1e-12 in every run | **FAIL as frozen**: 1.16e-12 in one no-weight D1 control (alt, ε = 0.1, no clump; 363,789 steps of round-off). All verdict-bearing runs ≤ 3.3e-13; MUTATE run 4.8e-13 |
| K3 α = 0 | PASS, nothing moves |
| K4 cumulative-excess law (sympy) | PASS, residual 0 |
| K5 centre law, uniform solution, I(ρ) closed form and limit (sympy) | PASS |
| K6 uniform sphere vs centre ODE (αt = 4τ0) | PASS, 2.9e-5 |
| K7 no stationary counter-flow (sympy) | PASS, p = ρσ_J²/(1 − q/3) |
| K8 time rescaling α ↔ t | PASS, 0 |
| K9 centre overfill ≤ ρ*(αt) | PASS, worst ratio 0.041 (after correction 1) |
| M1 inverted gate | BITES (R = 0) |
| M2 gate removed | BITES (R ≤ 1.2e-15) |

## Corrections and disclosures (2026-10-19)

- **Correction 1 (numerics, after the first run and before any label was adopted).**
  - The first run failed K9: the centre-cell overfill rose again after draining, reaching ×238 the bound at late times.
  - Cause: the cumulative excess at a face relaxes at rate Γ however small it is. Once it is tiny, the CFL bound no longer limits
    dt·Γ, and RK2 amplified the decay (|1 − z + z²/2| > 1 for z = dtΓ ≈ 3).
  - Fix: added dt ≤ 0.5/max Γ.
  - Every V1 number printed in the first run (s_50, α_50, α_90, α_c, R values) is unchanged, as are V2 and D1. K2's
    1.2e-12 was the same in both runs.
  - The first-run log was overwritten. Its numbers are quoted here.
- **Development runs.** The script was exercised in a scratch copy before the committed run:
  - timing;
  - a positivity fix, where both RK2 stages must now satisfy the CFL bound (a first trial produced −0.5 M_⊙ in a 0.5 pc shell);
  - the K2 diagnosis.
  None of these changed physics or thresholds.
- **K2 is reported as frozen (FAIL).** It is not loosened, and the code was not changed to pass it. The failing run is a diagnostic
  control with no verdict weight.
- **Pre-freeze hand values** (in the criteria) predicted α ≲ 9e-4 to 1.3e-3. The run agrees.
- **Limits.**
  - Drift-only density sub-flow: no kinetic (Vlasov + drift + OU) run, with the O(1) argument and K7 in its place.
  - Spherical symmetry; static baryons and phantom.
  - Illustrative hosts.
  - D2–D4 are textbook estimates.
  - The gate is CFG639's hypothesis HG, and it is not established: Part A NOT DIAGNOSTIC (IC-C not steady); Part B VG-1
    UNDETERMINED; CFG641's gate is off 99.96% under RN.
  - This lane makes HG load-bearing for the dwarf clump. It does not validate it.
  - Clump formation is out of scope (CFG878).
  - CFG877's M_cl = 81σ⁴/(4Ga0) assumes the clump's own gravity is boosted by the law. The record's E2/E7 do not contain that boost:
    ρ_ph comes from baryons only. Retention here uses only the clump's density profile, so it does not depend on that question.

## Next

1. A kinetic gated test: the CFG544 toy plus a clump with gate, Vlasov and OU. It checks the Jeans-equilibrium retention and the D1
   ratchet's end state with orbital mixing.
2. A stronger galaxy-side tooth for CFG639 Part A. The gate now carries both the merger and the dwarf results.
3. A formation-side count of first-cooling blocks (φ) without ΛCDM inputs, to set against CFG881's F_max.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (3a10f28a8) |
| `cfg882.py` | script |
| `cfg882.out`, `cfg882_results.json` | main run |
| `cfg882_MUTATE.out`, `cfg882_results_MUTATE.json` | MUTATE run (inverted gate) |
