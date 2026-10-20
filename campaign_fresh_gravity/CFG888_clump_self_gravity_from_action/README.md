# CFG888: does a cold-energy clump's own gravity follow the law? Decided from the record's equations

**Bottom line: no formulation in the record lets cold energy feed the law.** In every formulation, the law's g_N (and so ρ_ph) is
computed from baryons only. A clump of extra cold energy therefore never gets a law-boosted self-gravity. What it gets instead
depends on the formulation:
- **Class-A equations of motion (CFG541/638):** its self-gravity is Newtonian.
- **Canonical action with the S3 identification ∇·P = ρ_c:** it has **no self-gravity at all.** The critical quadratic cancels it
  exactly (sympy), and the tether pushes any excess outward. CFG877's clump on three hosts feels a net outward force at every
  radius. A self-bound clump cannot exist in this formulation.
- **Self-boost (CFG871/872/877/878 A's H-LINK)** needs a coupling the record does not write: free cold energy entering the action as
  ordinary −ρΦ matter. That is CFG722's coupling G, which CFG722 rejects for tethered cold energy as double counting.

So **CFG871's r_c = (9/2)σ²/a0 and CFG877's M_cl = 81σ⁴/(4Ga0) are NOT DERIVED by the record's equations.** In the record's branch
the clump is a Newtonian isothermal:
- its core is r_0 = 3σ/√(4πGρ0), which contains no a0;
- its mass grows ∝ r with V_c = √2σ = V_x (an identity), which is CFG870's extended form, the form CFG876 broke;
- it is finite only if something truncates it. The host's own field does this only for M_b > 9σ⁴/(Ga0) ≈ 2e6 M_⊙. Below that the
  truncation is a new parameter.

Branch (b), if someone adopted it, does not rescue CFG877 either:
- the clump's boost has to be made of tethered cold energy, about 6e6 M_⊙ inside 200 pc, which is more than the whole catchment
  stock for M_b ≤ 1e5 M_⊙;
- its outer field is the law of (M_b + M_cl), not CFG877's capped Newtonian term;
- the stiffness screens the boost at the clump's scale.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are kept apart and never pooled. Cold energy is real gravitating mass; no particle
species. Framework-native only. Not "theory closed". This lane compares the record with itself and makes no data comparison.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dd7b30afb), owner block 880–889.
- **Script:** `cfg888.py` (numpy, scipy, sympy; one process, about 1 min, < 150 MB).
  - `OMP_NUM_THREADS=1 nice -n 10 python3 cfg888.py` writes `cfg888.out` and `cfg888_results.json` and exits 0, with 13/13 K PASS.
  - `CFG888_MUTATE=1` writes `cfg888_MUTATE.out` and `cfg888_results_MUTATE.json` and exits 1 by design: all four teeth bite.
- **Inputs, read only:** CFG877's σ = V_x/√2 (7.534 / 7.486 km/s) and M_cl (5.25e6 / 4.24e6 M_⊙); CFG870's r_c 104 pc and ρ0_870
  0.582 / 0.575 M_⊙/pc³; CFG878's f table (for K3 only); CFG882's hosts H1 (1e4 M_⊙, 30 pc), H2 (3e5, 200 pc), H3 (2e7, 700 pc).
  Nothing was downloaded, and no other lane was edited.

## Q1. The law's source in the record: BARYONS ONLY (every formulation)

The script greps each of these strings and prints its file:line (`cfg888.out`, Q1 block).

| formulation | what the record says | file:line |
|---|---|---|
| Class A, gravity | ∇²Φ = 4πG(ρ_b + ρ_c). Only real mass gravitates, and the cold energy feels the full Φ, so its self-gravity is Newtonian | CFG541 EQUATIONS.md:65; CFG638 README:24 |
| Class A, phantom | the round rule uses "only the region's own baryons"; "ρ_ph is a functional of the baryons" | CFG541 EQUATIONS.md:90, :106 |
| Class A, code | `y = G * self.Mbf / (rf**2 * a0)`; `self.Mphf = self.Mbf * nu_m1(y)` (baryon mass only) | CFG541 cfg541.py:255–256 |
| Class A, overfill | "overfill not handled" | CFG638 README:63 |
| Canonical action (S2) | L = −\|∇Φ − KP\|²/(2K) **− ρ_b Φ** − W_rem(u) − (γ/2)\|∇P\|². The only matter term is baryonic | THEORY_CANONICAL_2026-10-14.md:18 |
| Canonical S3 (ID) | cold energy is the medium "whose displacement is P (∂ₜP = −j, ∇·P = ρ − ρ̄)" | THEORY_CANONICAL_2026-10-14.md:26 |
| Canonical S4 | free cold energy is "bound by ordinary gravity"; its coupling is not written in the action | THEORY_CANONICAL_2026-10-14.md:33–34 |
| ID bridge | "the critical quadratic cancels the carrier's self-gravity"; the carrier sees ∇Φ_N[ρ_b] plus the residual tether; "the tether reads g_N of all baryons" | CFG722 README:75–76, :98 |
| Coupling G (rejected) | "the phantom would be sourced by M_b + M_c (two-sector double counting)" | CFG722 README:67 |
| ID overflow | "overflow **cannot sit in the core**" | CFG722 README:112; CFG747 README:15; CFG776 README:10 |
| Free mass in code | H-EX: the law's source is the core baryons and the free reservoir is returned separately; CFG822 sums M_core + M_set + free; CFG877 adds the clump to σ² Newtonianly | CFG809 cfg809.py:119, :124; CFG822 cfg822.py:34; CFG877 cfg877.py:30 |
| **H-LINK (the claim at stake)** | CFG877's mass uses 81σ⁴/(4Ga0); CFG878 A puts the clump's own mass inside ν; CFG871 calls the self-boost "an assumption of H-LINK" | CFG877 cfg877.py:80; CFG878 cfg878.py:20; CFG871 README:21 |

**CFG877 is a hybrid.** Its clump *mass* comes from the self-boosted formula (cfg877.py:80). Its clump *field on the stars* is
Newtonian, G M_x/(3r), capped at that mass (cfg877.py:28–30). No formulation in the record has both at once.

## Q1b. The clump's own gravity, derived

**S1. Canonical action, ID (sympy, exact).** Take one Fourier mode, ρ_b = B cos kx and ρ_c = C cos kx, with ∇·P = ρ_c, and Φ from
its own Euler–Lagrange equation. The on-shell Lagrangian is

  ⟨L⟩ = K B (B + 2C)/(4k²), against the Newtonian −V = K (B + C)²/(4k²).

The C² term (the carrier's self-gravity) is **exactly 0**. The B–C term (baryons on carrier, and carrier on baryons) is the
Newtonian one. Expand the square: −|∇Φ|²/2K + ∇Φ·P − K|P|²/2. The last term, the critical quadratic, cancels the carrier's
self-energy. The modes decouple, so this holds for any density.

**S2/S3. The source of the law's g_N.**
- Under ID: (Φ′ − KP)′ = K ρ_b. The ρ_c coefficient is 0, so the law reads baryons only.
- Under coupling G (matter term −(ρ_b + ρ_c)Φ, P independent): (Φ′ − KP)′ = K(ρ_b + ρ_c). The cold mass then sources the phantom,
  and its self-gravity follows the law. **This is H-LINK.** The record does not write this coupling.

**S4. Stiffness under ID.** For longitudinal P, (γ/2)|∇P|² = (γ/2)ρ_c² = πG L*² ρ_c² (1-D and 3-D, exact). It is a local
*repulsive* self-energy, i.e. a pressure πG L*² ρ_c². It cannot bind anything.

**S5. The tether force on CFG877's clump (ID, static, spherical, carrier at rest).** E[M] = −∫M g_Nb dr + ∫W(GM/r²) 4πr² dr gives
F(r) = δE/δM(<r) = −g_Nb + u²/(a0 − u), with u = G M_c(<r)/r². F > 0 means outward. This is CFG747's
r̈ = −1/r² + m²/r⁴ with the full kernel.

| host | law state \|F\|/g_Nb | law + clump: F/g_Nb on 1–1000 pc | max u/a0 | stiffness (24 pc) / tether push at r_half |
|---|---|---|---|---|
| H1 (can / alt) | 7e-16 / 6e-16 | **+0.34 … +109 / +0.30 … +81** | 0.23 / 0.19 | 0.14 / 0.21 |
| H2 | 7e-16 / 6e-16 | **+0.93 … +20 / +0.65 … +16** | 0.25 / 0.21 | 0.10 / 0.15 |
| H3 | 7e-16 / 7e-16 | **+0.14 … +13 / +0.10 … +10** | 0.28 / 0.24 | 0.07 / 0.12 |

The result is **EXCESS PUSHED OUT (no self-bound clump).** The sign is analytic: u²/(a0 − u) increases with u, so any positive
excess raises the outward tether above the baryons' pull. The numbers confirm it, and the excess stays below the capacity wall
everywhere.

**Implemented branch.** A clump that is not expelled can exist in only two places:
- class A with CFG639's deficit gate (CFG882);
- S4's free population, as the record implements it (H-EX, CFG877's σ²).

Both are **branch (a): Newtonian self-gravity**, plus the host's law field. Branch (b) is CONDITIONAL on writing free cold energy
into the action as −ρΦ matter. That would be a new assumption.

## Task 2. The clump for σ = 7.53 km/s (isolated, as CFG878)

### Branch (a), the record's: Newtonian isothermal (Emden)

| ρ0 (M_⊙/pc³) | r_0 = 3σ/√(4πGρ0) | M(<100 pc) | M(<200) | M(<500) | M(<1000) | dlnM/dlnr at 10 kpc |
|---|---|---|---|---|---|---|
| 0.01 | 972 pc | 4.15e4 | 3.23e5 | 4.22e6 | 2.11e7 | 0.81 |
| 0.1 | 307 pc | 3.82e5 | 2.42e6 | 1.46e7 | 3.32e7 | 1.00 |
| **0.6** | **126 pc** | **1.59e6** | **5.79e6** | **1.63e7** | **2.88e7** | 1.07 |
| 3.0 | 56 pc | 3.04e6 | 6.60e6 | 1.41e7 | 2.51e7 | 1.04 |
| 0.582 (CFG870) | 127 pc | 1.56e6 | 5.75e6 | 1.63e7 | 2.89e7 | 1.07 |

These are canonical values. Alt agrees within 1.5% (σ 7.486; a0 does not enter).

- The mass is **unbounded**: M → 2σ²r/G ≈ 2.6e4 M_⊙ per pc.
- Its asymptotic circular speed is √2σ = 10.655 km/s, exactly CFG870's fitted V_x (an identity, not a coincidence).
- At CFG870's central density the Newtonian clump carries 1.23 / 1.38 / 1.29 / 1.11 × CFG870's extended M_x at 100 / 200 / 500 /
  1000 pc, and 3.1–6.7 × CFG877's capped M_x at 500–1000 pc.
- The record's clump is therefore CFG870's extended form, which CFG876 broke. It is not CFG877's finite clump.

**What truncates it in the framework (Part D, ρ0 = 0.6).**
- In a host's deep field g = V_h²/r, an isothermal has ρ ∝ r^(−V_h²/σ²). It is finite iff V_h² > 3σ², i.e.
  **M_b > M_crit = 9σ⁴/(G a0) = 2.33e6 / 1.88e6 M_⊙**.
- Checked numerically (HOST CONFINEMENT CRITERION CONFIRMED):
  - H3 (2e7 M_⊙, V_h 22.3 / 23.4 km/s) confines the clump at **8.2e6 / 7.4e6 M_⊙** (dlnM/dlnr = 0 at 10 kpc);
  - H1 and H2 do not: M(<10 kpc) = 2.3e8 and 1.0e8 M_⊙, still ∝ r (slopes 1.05 / 0.97).
- Below M_crit the host's own field cannot truncate the clump. That covers the ultra-faints and most classical dSphs. The remaining
  options all come from outside σ:
  - Milky Way / M31 tides: satellites only, and they depend on pericentre, while CFG843/875 find no host effect;
  - the finite catchment supply;
  - the gate's formation history.
- **The replacement ADDS A PARAMETER**: a truncation radius or a mass per dwarf, on top of ρ0. Above M_crit the mass becomes
  host-dependent.

### Branch (b), CONDITIONAL: self-boosted isothermal (CFG878 A reproduced, K3)

| ρ0 | M_total (f) can | alt | M(<100/200/500/1000 pc) can | r_half | clump phantom <200 / <1000 pc |
|---|---|---|---|---|---|
| 0.01 | 4.98e6 (0.948) | 4.04e6 (0.954) | 3.5e4 / 2.1e5 / 1.26e6 / 2.69e6 | 908 pc | 2.3e6 / 4.1e7 |
| 0.1 | 4.71e6 (0.897) | 3.85e6 (0.908) | 2.5e5 / 9.6e5 / 2.65e6 / 3.69e6 | 427 pc | 4.6e6 / 4.8e7 |
| **0.6** | **4.37e6 (0.833)** | **3.60e6 (0.849)** | **7.7e5 / 1.86e6 / 3.21e6 / 3.80e6** | **243 pc** | **6.2e6 / 4.9e7** |
| 3.0 | 3.99e6 (0.760) | 3.30e6 (0.779) | 1.40e6 / 2.34e6 / 3.20e6 / 3.56e6 | 153 pc | 6.8e6 / 4.7e7 |

Deep-law r_M = (9/2)σ²/a0 = 88 pc canonical / 72 pc alt. With the canonical action's own static kernel (simple ν) f changes by
< 0.3% (0.831 / 0.847 at ρ0 0.6).

**Costs of (b) that CFG871/877 did not count:**
1. **Supply (R3).** Under the action, a phantom is tethered cold energy (∇·P = ρ_c), so the clump's own boost needs 6.2e6 M_⊙ inside
   200 pc and 4.9e7 inside 1 kpc. The largest catchment stock is 53.64 M_b. Inside 200 pc the boost needs 115 / 11.5 / 1.15 / 0.12 ×
   that stock for M_b = 1e3 / 1e4 / 1e5 / 1e6 M_⊙. This is for an isolated clump; the host's own phantom draws on the same stock.
2. **External field (R2).** The clump's extra acceleration over the host's law is law(M_b + M_cl) − law(M_b).
   - Faint hosts H1, H2: **1.5–1.9 × CFG870's extended form** and 1.6–24 × CFG877's capped form at 200–2000 pc.
   - Bright host H3: 0.33–0.72 × the extended form at ≥ 500 pc, because the deep law is nonlinear and the clump's share shrinks when
     M_b ≫ M_cl.
   - **Frozen label: (b) EXTERNAL NOT ≥ CFG870 EXTENDED**, because of H3. The inference that (b) inherits CFG876's break therefore
     holds only for faint hosts, and it is not a data test.
3. **Stiffness (Part C)**, solving the canonical field equation u²/(a0 − u) − (L*²/2)∇²u = g_N with the (b) clump as source:

| L* (pc) | boost ratio R_s at 50 / 100 / 200 / 500 pc, canonical | alt |
|---|---|---|
| 1 (control, K6) | 0.9997 / 0.9999 / 1.0000 / 1.0000 | same |
| **24 (window floor)** | 0.845 / **0.943** / 0.978 / 0.992 | 0.818 / **0.928** / 0.972 / 0.991 |
| 100 | 0.461 / 0.568 / 0.694 / 0.861 | 0.418 / 0.517 / 0.642 / 0.829 |
| 300 | 0.318 / 0.342 / 0.341 / 0.400 | 0.287 / 0.304 / 0.298 / 0.353 |
| 1000 | 0.289 / 0.292 / 0.243 / 0.164 | 0.262 / 0.260 / 0.211 / 0.139 |

   - **Frozen class: MATTERS AT 24 pc**, since R_s(100 pc) = 0.943 / 0.928 < 0.95.
   - Self-consistent clump (report only, converged): total mass ×1.016 / ×1.029 at L* = 24 pc and **×1.41 / ×1.57 at 100 pc**
     (1.17 / 1.33 × M_deep).
   - So even in (b), M_cl = 81σ⁴/(4Ga0) holds only at the bottom of the L* window. L* is bounded, not derived (24 pc to ≳ 1 kpc), and
     it becomes an input to the clump mass.
   - In (a) and under ID the stiffness cannot bind (S4). Under ID it adds 7–21% to the outward push at the clump's half-mass radius.

## Task 3. Consequences (stated plainly)

- **CFG871:** r_c = (9/2)σ²/a0 is **NOT DERIVED BY THE RECORD'S EQUATIONS.**
  - In the record's branch the core is r_0 = 3σ/√(4πGρ0) (126 pc at ρ0 0.6). It contains no a0.
  - σ and r_c are independent again, as CFG871's own criteria say they would be for Newtonian self-gravity. CFG871's "consistency"
    (98 vs 133 pc) is not a test of the law; r_c ≈ 100–130 pc only restates ρ0 ≈ 0.6.
- **CFG877:** M_cl = 81σ⁴/(4Ga0) is **NOT DERIVED.**
  - In the record's branch the clump's mass is not set by σ. It grows ∝ r (CFG870's broken extended form) until something truncates
    it.
  - The truncation is a new parameter below M_crit ≈ 2e6 M_⊙, and host-dependent above it.
  - CFG877's "no new parameter" therefore does not hold. Its cap was imported from a formula the record's equations do not contain,
    and its fit is a hybrid (self-boosted mass, Newtonian field) that matches no formulation.
- **CFG878 Part A** ("the fragment mass is set by σ alone") is conditional on the unwritten coupling. **CFG872's** per-dwarf fits used
  H-LINK's r_c and are conditional as well. **CFG878 Part B**'s conclusion is reinforced: the cold-energy equations as written
  cannot make the clump, because in the record's branch σ does not even fix its mass.
- **The canonical v3 addenda for 2026-10-19 night** (THEORY_CANONICAL_2026-10-18.md lines 70–86, M_cl = 81σ⁴/(4Ga0) and "under the
  full law a self-gravitating isothermal cold clump has M = …") rest on H-LINK. This lane does not edit them; the orchestrator
  decides.
- **What would restore H-LINK** is a new, flagged coupling: free cold energy as −ρΦ matter (CFG722's G) for an untethered population
  only. Even then:
  - the boost needs tethered supply beyond the stock for M_b ≲ 1e5;
  - the outer field is no longer CFG877's capped term;
  - L* enters the mass.
  So it is not a parameter-free rescue.

## Controls

| K | test | result |
|---|---|---|
| K1 | Newtonian limit: Emden series at ξ 0.5 / 1 (2.5e-9 / 2.2e-6); dlnM/dlnr at 1e4 r_s 0.998; M/(2σ²r/G) 0.993 | PASS ×3 |
| K2 | deep limit: f(ρ0 0.01) 0.948 / 0.954; every f in [0.760, 0.954] ⊂ [0.74, 0.96] | PASS ×2 |
| K3 | CFG878's eight f values reproduced within 1% (independent integrator) | PASS |
| K4 | sympy S1 (C² term 0, B–C Newtonian), S2, S3, S4: residuals exactly 0 | PASS ×4 |
| K5 | ID energy: law state stationary (≤ 7.4e-16); finite-difference dE vs ∫F δM (≤ 2.1e-9) | PASS ×2 |
| K6 | stiffened solver at L* = 1 pc reproduces the law (R_s 0.9999 at 100 pc) | PASS |

**MUTATE** (branch swapped everywhere; `cfg888_MUTATE.out`) exits 1 by design. All four teeth bite:
- M1: self-boost forced on in Part A. K1 fails (slope 0.0002, M saturates at 3.8e6).
- M2: self-boost forced off in Part B. K2 fails (f ≈ 1500, unbounded).
- M3: critical quadratic dropped. S1 fails; the C² term comes back as the Newtonian K/(4k²).
- M4: the carrier's Newtonian self-energy added to the ID energy. The law state is no longer stationary (|F|/g_Nb up to 2.8e3).

## Corrections and disclosures

1. **Correction 1 (implementation, before any class was printed).** The first run (2026-10-20 00:27) crashed in Part C, and its Q1
   block also showed one citation needle NOT FOUND: "bound by ordinary gravity" is split across lines 33–34 of THEORY_CANONICAL
   2026-10-14. The needle was changed to "ordinary gravity and never re-tethers" (line 34), and the text it cites is unchanged.
2. **Correction 2 (implementation).** The crash came from a scalar/array shape mismatch in the BVP boundary function. It was fixed
   with a reshape. Parts S, A and B printed identical numbers in both runs (diff checked).
3. **Hand-value miss (disclosed).** The pre-freeze estimate for stiffness at 24 pc was "≈ 3%". The solver gives a 5.7% / 7.2% loss
   of boost at 100 pc, so the frozen class is MATTERS AT 24 pc. The self-consistent mass moves only 1.6% / 2.9%.
4. **Assumptions.**
   - The isotropic isothermal clump is inherited from CFG871/878, not derived.
   - S5 uses the static spherical energy with the carrier at rest. A warm carrier sits below the law (CFG722 B8), so it is pushed out
     further.
   - S5 and Part C use the action's simple ν; Parts A, B and D use ν_e. R4 shows the difference in f is < 0.3%.
   - Part D treats the host's settled cold energy as already at the law, with the clump adding Newtonianly (branch a) or entering
     the law's source (branch b).
5. **Report-only items** (R1–R5 and the self-consistent stiffness run) carry no verdict weight. R2's link to CFG876 is an inference
   by dominance, not a data test, and its frozen label is NOT.
6. The sign of the S5 force is analytic: a monotone tether with any positive excess. The numbers confirm it rather than discover it.

κ = ½ fitted; cold energy mass required; not theory closed.
