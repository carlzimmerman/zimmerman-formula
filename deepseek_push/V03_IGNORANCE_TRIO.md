# V03 — THE IGNORANCE-ORTHOGONAL TRIO: R (kernel-free) × U (radius-free) × B (density-free) as ONE decision surface

**2026-09-25 · deepseek lane · follow-on to J05/J06/J09/J10/J11, K08/K09, L07, N04, U05 · no git commit**

## PRE-REGISTRATION (locked BEFORE the V03 numbers are drawn)

### 0.1 The three falsifiers (each immune to a different ignorance)

| falsifier | definition | immune to | record |
|---|---|---|---|
| **R** | R ≡ −ln A / E[D], A = P(no collision) = E[I(N=0)], D = lag | **kernel (phase function)**: A never fires the kernel; E[D]'s scattering term is ∝ E[μ] = 0 for symmetric kernels (L07, 46/46) | J09: central flat window R ∈ [4/3, 2], τ₀-free, closed form W_C(q) = (1+q/3)/(½+q/4); J11/K09: volume window τ₀-dependent |
| **U** | U ≡ std(D)/E[D] (width ratio) | **physical radius**: ratio cancels R (N04, K09 width surface) | N04: kernel-***tagged*** (isotropic shift z ≈ 5–12), 29–49× cheaper than R |
| **B** | bound: E[D²] ≥ 3 E[Dv²]² / E[v⁴], slack_B ≡ E[D²]·E[v⁴]/(3 E[Dv²]²) ≥ 1 | **density, geometry, kernel** (Cauchy–Schwarz; conditional-Gaussian hierarchy J05/J06, exact slack = 1/ρ₀²) | J05: central τ₀=1 slack 1.25/1.13/1.06 at q = 0/3/10; U05 thin limits 4/3, 448/375, 91/81 |

### 0.2 The landscape grid (all cells, both kernels)

- **CORE (36 cells, n = 8×10⁵ each)**: geometry ∈ {central, volume} × q ∈ {0, 3, 10} × τ₀ ∈ {0.5, 1, 2} × kernel ∈ {thomson, isotropic}.
- **SHELL-EXT (36 cells, n = 2×10⁵ each)**: geometry ∈ {shell(a=0.3), shell(a=0.5)} × same q × τ₀ × kernel.
- Engine: J02 exact optical-depth bisection (verbatim copy + L07 kernel switch + K09 shell birth law); parity-checked bitwise against `J02_moment_hierarchy.simulate` and `K09_geometry_reading.simulate_shell` before science cells (P1).
- SEs: R, U by the N04 delta method **and** by 24-block jackknife (block covariance matrix of (R, U, slack) → 3×3 sampling covariance; SE everywhere).

### 0.3 The observer bands (fixed from the RECORD, not from this run)

| band | geometry | provenance | value (widened ±3·tol) |
|---|---|---|---|
| W_C | central | J09-D closed form, exact | [4/3, 2], tol = 0 |
| W_V | volume | K09 Table (τ₀ ∈ {0.5,1,2}, q ∈ {0,3,10}) | [0.9184, 1.9144], tol = 0.010 |
| W_S | shell | K09 union over a ∈ [0.1, 0.99] on-grid | [1.4298, 2.0063], tol = 0.025 |
| U_C | central | N04 U-table (9 cells), union ±3·se | [0.804, 1.982] |
| U_V | volume | N04 U-table (9 cells), union ±3·se | [1.233, 2.536] |
| U_S | shell | **this run** (flagged CIRCULAR for shell cells) | [min−3σ, max+3σ] over its 18 measured cells |
| B | any | J05 theorem, slack ≥ 1 | [1, ∞), violated iff slack < 1 − 3·se |

Membership (Tier-1 verdicts): g ∈ v_R iff R ∈ W_g (3σ margins included); g ∈ v_U iff U ∈ band_g; B-PASS iff slack ≥ 1 − 3·se.

### 0.4 Disagreement classes (locked; cells where B-PASS unless stated)

Let vR, vU be the Tier-1 membership sets over {C, V, S}.

1. **KILL-B** — slack < 1 − 3σ: the density-free gate fails ⇒ the transfer function is not a Thomson-sphere LRD for ANY geometry/kernel/density (J05 F), regardless of (vR, vU). Expected count on-model: 0.
2. **VOID-X** — vX = ∅ for X ∈ {R, U}: falsifier X excludes ALL geometries (K09-F3 outright-kill channel). Expected in-model at shell q=10 cells if the recorded W_S (built over q∈{0,3} only) fails there — the *incomplete-atlas* signature.
3. **MIRROR** — vR ∩ vU = ∅, both nonempty: an exclusive contradiction (R admits only geometries U excludes). Expected rare; diagnostic content: the two geometry channels are driven by different ignorance projections (R ≈ density-integrated chord skimming; U ≈ width/residence), so a mirror = the cloud's geometry lives outside the recorded atlas.
4. **CROSS** — vR ∩ vU ≠ ∅ but sets cross (S∈vR ≠ S∈vU, or non-nested): partial contradiction in exactly one geometry axis (e.g. R admits shell, U does not). Diagnostic content: the disputed axis is where the atlas is thinnest (shell a-line) — the trio *localizes* the ignorance.
5. **HIERARCHY** — vR ⊊ vU or vU ⊊ vR (proper subset): one falsifier strictly more restrictive. Diagnostic content: the restrictive one is operating in its immune band, the admitting one in its blind band (e.g. U admits volume while R excludes it: U's τ₀-spread band is wide because U is τ₀-resolved only AFTER R pins the operating point).
6. **TRIO-AGREE** — vR = vU: no disagreement.

Kernel axis: every R, U, slack value reported per kernel; kernel-independence of R tested per cell (gate: |R_iso − R_thom| ≤ 5 combined SE, L07-KILL); kernel-tagging of U per cell (gate: z ≥ 3 ⇒ tagged, N04).

### 0.5 Pre-registered checks (thresholds fixed before the run)

- **P1 parity**: engine ≡ J02 bitwise (central, τ₀=1, q=3, n=2e5); shell engine ≡ K09 simulate_shell bitwise (a=0.3, τ₀=1, q=3). KILL if max|D − D_ref| > 1e-9.
- **C1 U-record**: U(central, τ₀=1, q=0/3/10) = 1.437/1.074/0.898, U(volume, τ₀=1, q=0/3/10) = 1.893/1.400/1.258 (N04/K09 record), each within 3 SE. KILL if any |z| > 5.
- **C2 R-law**: central R ∈ {2.000, 1.600, 4/3+2/3·... = 1.4444} at q = 0/3/10, τ₀-free across τ₀ ∈ {0.5,1,2} (3 cells agree within 3 combined SE). KILL if |z| > 5 vs closed form.
- **C3 R-kernel-free**: |R_iso − R_thom| ≤ 5 combined SE at **every** core cell (L07 proof re-grid; volume q=3,10 cells are NEW territory). KILL if any |z| > 5.
- **C4 B-record**: slack(central, τ₀=1, q=0/3/10) = 1.25/1.13/1.06 (J05) within |z| ≤ 4.
- **C5 B-theorem**: slack ≥ 1 − 3σ at ALL 72 cells (density-free bound under every geometry/kernel on-grid). KILL if any violation at |z| > 5.
- **C6 doorB**: at (central, q=0, τ₀=1), 0.90889·R = 1.8178 ± 3·se (K09 record, reading reproduction), and the trio verdict at the corner is **CONSISTENT-OPEN** (reading ∈ W_C and ∈ W_V and ∈ W_S at the single point; B-PASS; U consistent with central).
- **C7 U-kernel-tag**: U tagged (z ≥ 3) at the operating cells (τ₀=1, q ∈ {0,3}) — the instrument must carry the kernel-tag onto the U coordinate (N04 re-grid).

### 0.6 Decision-tree read-out (locked structure)

An observer measures (A, E[D], E[D²], E[Dv²], E[v⁴]) — three numbers R, U, slack_B — from ONE 2D transfer function:

- **Node 1 — B gate (model-free)**: slack ≥ 1 − 3σ? NO → KILL-B (not a Thomson-sphere LRD for any density/geometry/kernel). Failure mode: slack−1 < 3σ (n too small → UNDET), or E[v⁴] tail-noise.
- **Node 2 — R test (kernel-freedom + operating-point pin)**: (i) R ∈ [4/3, 2] ± 3σ? (central window, kernel-free); (ii) K06-inv (A, E[D]) → (τ̄₀, q̄) pins the operating point — **valid only if (i) passes**. Failure modes: R outside ALL three bands (outright kill, K09-F3); R in-band but inversion q̄ on the grid edge; central-excluded ⇒ no pin (fall back to Tier-1 U verdict, flag INV-FAIL).
- **Node 3 — U read-out (geometry)**: at pinned (τ̄₀, q̄) compare U against the N04-resolved U-table columns U_C, U_V (±3·se_table + 3·se_meas). Geometry = nearest column within 3σ; ambiguous if two. Failure modes: (i) U is **kernel-tagged** (use the kernel-matched column; unknown kernel ⇒ UNTRUSTED flag); (ii) inversion bias at non-central true geometry (reported per cell); (iii) (τ̄₀, q̄) off-grid.
- Minimum n per falsifier for 3σ per cell: n_req = n·(3·se/gap)², gap = distance from the measured value to the nearest competing band edge (R, U, B as defined in §0.3; resolved U gaps from the N04 table).

### 0.7 Joint 3σ acceptance regions (locked method)

Per class (geometry, kernel): centroid μ = mean of its 9 cells in (R, U, slack); Σ = Σ_landscape + Σ_samp(operating cell τ₀=1, q=0, n=8e5/2e5); the class's 3σ region = Mahalanobis ellipsoid {x : (x−μ)ᵀΣ⁻¹(x−μ) ≤ 9}. Pairwise overlap = Monte Carlo (2×10⁶ draws from A's Gaussian, fraction inside B's ellipsoid; symmetric mean). **Residual degeneracy** = (geometry, kernel) pairs with overlap ≥ 1%.

---

## RESULTS (computed AFTER the locked pre-registration above)

*(filled by V03_trio.py run — see V03_trio.out)*