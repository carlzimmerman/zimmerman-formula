# CFG950: the labelled-domain theory (LDT), written down and tested

**Lane label: NOT CONSISTENT AS SPECIFIED** under the frozen rule and metrics. **LDT CONDITIONAL** under the post-hoc
amendment A1.

- The only FAIL is the merger toy's frozen law metric f3. With equal-mass shells it is pinned at the innermost shell
  (field step δu₁ ≈ 0.73 at every resolution), so it cannot converge.
- A1 replaces it with a resolved-range metric plus the exact discrete identity. Under A1 the merger test passes.
- No generic obstruction is shown, so INCONSISTENT is not claimed.
- The two conditions are equally important. **Energy is not conserved by any dynamical field at label events.**
  Well-posedness inherits CFG938's premises.

**Settings.**
- **Criteria:** `FROZEN_CRITERIA.md` (324edbf93, committed alone first). **A1:** `AMENDMENT_A1_post_hoc.md` (fb9af871f,
  POST HOC; f3 metric only; frozen result reported alongside). Block 950–959.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native inputs
  only.
- Not "theory closed". Nothing here says the data favour the framework.

## The construction (DERIVATION §1)

**Primary formulation (A): per-label tether.** The labelled cold medium is the phantom (CFG945 H1 written for
populations):

  S = ∫√−g [c⁴R/16πG − Σ_q mc²n_q − Σ_{q≥1}(W_full(|D_(q)χ_q|) + (3γ/4K²)τ_q²) + Σ_{q≥1} λ_q(D_(q)²χ_q − Kmn_q)] + S_b.

There is no θ in the action. Unlabelled medium (q = 0) is dust. A label-q element feels
−∇Φ_b − Σ_{p≠q}∇χ_p + R(u_q)∇̂χ_q, so D-T cancels its own label's gravity only. Equilibrium: R(u_q) = g_b + Σ_{p≠q} u_p.

**Comparison formulation (B): CFG947 N1.** On settled domains (B) has exactly the same gravitating density, provided its
edge is the kernel's own supply root (T-EQ, 4e-16). Dynamically (B) has no action, a cap, a clip, the T-M condition, and a
merge jump.

**Label sector (no action; declared plainly).**

| rule | content |
|---|---|
| (i) assignment | θ-latch (local) plus contact inheritance within L*; seed if no labelled medium lies within L* |
| (ii) merge M-R | whole-label merge when the label's ball domain (shell-averaged tidal dominance about its centroid) shrinks to zero; fractional transfer |
| (iii) source / draw | the medium's own mass, moved by dynamics plus internal viscosity, so mass and momentum are conserved |
| (iv) satellites | keep their label; one-way re-latch of elements outside the ball domain |
| (v) debris | ≤ 3.5e-7; the rules leave none in settled galaxies |

**R-E.** A declared non-dynamical label-energy scalar that closes the energy books.

## Results (both footings)

| test | result | grade |
|---|---|---|
| (a) law, single label | NGC 3198 2.2e-16; BTFR limit 1 (y = 1e-14: 1 + 1.0e-7, exact law's value); edge r_e = 454 / 413 kpc (supply root r_M√(N(N+1)), N = 53.6; = E7) contains all radii and deep points y = 1e-2, 1e-3 | PASS |
| (b) FRW, growth | dust w = 0; latch needs δ ≥ 3/f (none in the linear regime; top-hat θ = 0 at turnaround, transversal); n = 1.000000000000 | PASS |
| (c) no hover | own-label medium falls with its stars: Δa/g_host 1.6e-5 – 2.0e-3 (tides only) ≤ ε_B 0.344 / 0.317; bound over 1 Gyr in 18/18 | PASS |
| (d) slip | per label 1.54e-5; satellite in host 2.7e-8 (≤ 1.9e-5) | PASS |
| (e) conservation | momentum exact through latch, re-latch and merge (8e-14). Energy jumps: NGC 3198 assembly 0.17–0.94 \|E_grav\|; merger 0.54–0.70 \|E_grav,merged\|, +∞ for an instant merge where u₁ + u₂ ≥ a₀; re-latch +1.6–3.1 g_host R per unit mass. **T-LE:** bound cold medium cannot pay (deficit Δ > 0 for M_b 1e7–1e15; NGC 3198 Δ ≈ (97 km/s)²). Closed only via R-E (\|e_L\|/c² ≤ 1.8e-6; PN residual ~3e-7) | CONDITIONAL |
| (f) mergers | field jump across the merge J_LDT = 0, against the class-A-type 0.33–0.36; flow reaches the merged law (×23–25); discrete identity ⟨R⟩ = g_b to 1e-11. Frozen f3 0.12 (pinned); A1 resolved-range 5.9e-4 / 9.1e-4 at 2N₀ (converging) | **FAIL frozen / PASS under A1** |
| (g) well-posedness | per label ω² ≥ 0; inertia margin ≥ 5.9e4; no θ in the action, so no CFG944 ghost; co-located labels bounded (0.707); finite label changes | CONDITIONAL |
| (h) edge, zero-sum | edge forced (M_ph(< r_ON)/M_c 2.0–11.5); r_e/r_ON 0.09–0.51 per galaxy; 0 SPARC points beyond r_e; zero-sum = mass conservation (exact) | PASS |
| (i) satellite bound | ε ≤ ε_B; uniform EFE 0 ≤ δ_c 0.082 dex (tidal term −0.0002 to −0.057 dex, reported) | PASS |

**Structural statements (all pass).**

| statement | content |
|---|---|
| T-EQ | static A = B |
| T-LE | labelling energy Kλ_q = ∫D_full dr > 0 cannot be paid kinetically |
| T-P | momentum is exact through events |
| T-T | concentric labels tie (u₁ = u₂), so M-R must be a whole-label rule |
| T-G | no θ in the action, so no ghost |
| T-θ | the θ-latch front lies inside the turnaround front: f_θ = M_θ/M_ta = 0.47–0.76 for power-law profiles |

**Reported, no class weight.**
- **R1.** Other labels' media act like baryons for a label. Satellites' own-domain media are 41–854 times their stars and
  enter a host's law: three CFG882 dwarfs at 100 kpc carry 2.8% of a 6e10 M⊙ host's baryons. Class A does not have this.
- **R2.** Labels without baryons disperse.
- **R3.** (B)'s costs.

## CFG678 scorecard

| status | gates |
|---|---|
| PASS | A5, C2 |
| CONDITIONAL | A1, A2, B3, C1 |
| FAIL | C3 (inherited) |
| NOT DECIDED | C4 |
| PENDING | D3 |
| UNTESTED | A3, A4, A6, B1 (prescribed label sector; not passable by construction), B2, D1, D2 (needs an LDT PM engine, CFG952) |
| DECLARED | A7, E1–E3 |

The hover (CFG941/945) and the linear-growth flag (CFG938/941) are gone. B1 and C3 stay. Sources per gate are in
DERIVATION §11.

## Costs

1. A non-local, action-less label sector (latch, inheritance, ball domains, one-way re-latch, M-R, seeding).
2. Energy is not conserved by dynamical fields at label events (O(1) of binding energies). It is closed only by R-E.
3. Settling needs a dissipative extension, at a rate that is not derived.
4. One pair of auxiliary fields (χ_q, λ_q) per label.
5. Per-label single stream.
6. Single-label galaxies are enforced only by the rules.
7. No instant merging in Newtonian-regime cores (the W_full wall).
8. Other labels' media act as baryons (R1).
9. θ-latch labels hold 47–76% of the catchment mass.

## Controls
- **K: 7/7 pass.**
  - CFG938's NGC 3198 law.
  - CFG941's growth exponents.
  - CFG945's H1 tidal ε, two-label, debris, ε_B and δ_c (all exact).
  - CFG947's T-F, T-M and T-E.
  - CFG938's slip and dispersion.
  - CFG945's two-label value.
  - CFG941's hover ratios.
- **MUTATE: all 6 bite (exit 1 by design).**
  - M1: labels removed, the hover returns (= CFG941).
  - M2: a prescribed asymmetric draw breaks momentum (0.13; control 6e-17).
  - M3: a global label gives n = 0.694.
  - M4: no merge rule gives 4.12 / 4.61.
  - M5: a class-A-type recomputation jumps 0.36 / 0.32.
  - M6: tether off gives no labelling energy.

## Files and commands (one core, nice 10, ≤ 0.25 GB, 2–16 s per stage, memory guard, nothing downloaded, no other lane edited)
- `CFG950_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg950.py` → `cfg950_K.out`, `cfg950_results_K.json` (exit 0).
- `CFG950_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg950.py` → `cfg950_MUTATE.out`, `cfg950_results_MUTATE.json` (exit 1
  by design).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg950.py` → `cfg950.out`, `cfg950_results.json` (exit 0). It prints both the frozen
  class and the A1 class.
- Kept for disclosure: `cfg950_firstrun_f3frozen.*`, the first complete main run before A1. It is identical apart from the
  A1 lines.
- Final script sha256: 61af2e46…. `DERIVATION.md` holds every equation, number and disclosure.

## Disclosures (full list in DERIVATION §13)
- **A1 is post hoc.** The resolved-range threshold (r ≥ √(10 dm), where the per-shell field step at N₀ is ≤ 0.1) was chosen
  after the diagnostic was seen. The 1:3 toy's 2N₀ value, 9.1e-4, is close to its 1e-3 line.
- **First main attempt.** It crashed on a sympy artefact in the T-θ toy, before any test output. The fix was an exact
  rewrite.
- **A1 diagnostic.** It was run as a scratch script outside the lane.
- **CFG945's README.** It quotes the canonical extreme of the satellite tidal term (−0.052 dex). The alt extreme, −0.057,
  matches its JSON and is reproduced here exactly.
