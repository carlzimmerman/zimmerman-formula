# H3_jeans_control: is C5's negative-energy ω = 0 mode of AeST + γ_L + capped F only the Jeans instability?

## Verdict (frozen rule, printed first): CLAIM FAILS, on lines T1, T2 and T4

**On checking, none of the three FAIL lines is a ghost.** Each trigger traces to one of three things:
- the k-essence control's own band end;
- a Jeans-swindle artifact that the GR control shares exactly;
- AeST's own static force law at Y = 0.

What survives the hostile test, and what does not:

- **Criterion (i) is mis-specified. CONFIRMED (COMPUTED).** The same `jordan_energy` was applied to two controls.
  Both have a negative-energy ω = 0 mode with T1's exact sign structure (E_J < 0 ⟺ Γ² > 0).
  - Newtonian self-gravitating cold dust: E_J < 0 at every k, Γ² = 4πGρ̄ at every k.
  - GR + k-essence dust: E_J = 4K₂k²/(k² − K₂Q₀²), which is < 0 for k < √K₂ Q₀ ≈ μ. Its Γ² = (IQ₀/2)(1 − k²/(K₂Q₀²)).
  - So "E_J ≥ 0 at every k" (and SZ's λ_s > 0 read as a health condition) flags ordinary self-gravitating dust.
- **No ghost at linear order on the Y = 0 vacuum. COMPUTED.**
  - At I = 0, ω = 0 has multiplicity exactly 2 (one non-propagating dust degree of freedom).
  - The only propagating scalar has ω² > 0 with positive Krein signature at k = 1e-3 to 1e6 μ, with and without γ_L.
- **The vacuum (I = 0) mode is matter, not empty space. COMPUTED.**
  - It carries a dust charge perturbation δQ = −k²/(K₂Q₀²) ≠ 0 at λ₀ = 0, a static lump with δρ = 4K₂Q₀δQ.
  - Its energy is exactly the lump's self-energy in its own static potential: G_eff(energy) = G_pot at λ₀ = 0, identically.
  - The GR + k-essence control has the same kind of mode at I = 0 (δQ ≠ 0, G_eff(0) = G).
  - Both have zero background density. The mode is the zero-density limit of the Jeans mode (T3, frozen line met).
- **The rate is bounded. COMPUTED from exact roots at finite I.**
  - At I = 2e-7 (4πG̃ρ̄ ≈ H² at μ⁻¹ = 1 Mpc): max Γ²/(4πG̃ρ̄) = 0.99991. There is one unstable root per k.
  - With γ_L the growth ends at k = 240 μ, just below H1's k_c = 242.75 μ (≈ 1/(4.1 kpc)).
  - Without γ_L the band never ends (H1's result), but Γ² ∝ 1/(1 + k²/(K₂Q₀²)), so the rate falls with k.
- **What is not "ordinary": AeST's static force law at Y = 0 (the T2 FAIL).**
  - At λ₀ = 0 the lump's own static potential is G_pot/G = 1 + k²/(K₂Q₀²). That is Newton plus a contact term.
  - The binding per unit dust density therefore exceeds Newton's at k > μ. With γ_L it reaches 2.3e4 × Newton at
    k ≈ 185 μ, then turns positive at 243 μ. Without γ_L it grows without bound in k.
  - In the same band, growth is suppressed by the inverse factor. Neither control has this.
  - It is the λ₀ = 0 degeneracy of the φ sector (H1 K3: F enters only through λ₀). It is not a negative kinetic term.

**Plain reading.**
- AeST + γ_L + capped F is free of ghosts at linear order on Y = 0.
- Its negative-energy ω = 0 mode is a Jeans-type gravitational instability, with rate ≤ √(4πG̃ρ̄) and a band that ends
  at k_c with γ_L.
- But between μ and k_c (1 Mpc⁻¹ to 1/(4 kpc)) the "gravity" driving it is AeST's own Y = 0 static response. That
  response has a contact term, so it is not Newton's. "Healthy up to *ordinary* gravitational instability" is therefore
  too strong. "Healthy up to AeST's own gravitational instability, rate-bounded" is what the computation supports.
- C5's defect (b), the γ_L term giving no causal cone, is untouched by this lane and remains open.

κ = ½ FITTED. No footing enters. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

## The three frozen FAIL lines, verified

| line | what triggered it | verification |
|---|---|---|
| T1 | GR + k-essence has E_J > 0 at k > √K₂ Q₀ ≈ μ, where AeST's E_J < 0 | The pass line demanded E_J < 0 at *every* k in both controls, which the k-essence control does not have. Newtonian cold dust does (E_J < 0 at all k, like AeST). All three obey E_J < 0 ⟺ Γ² > 0. The criterion flags both controls. |
| T2 | G_eff/G = 1 + k²/(K₂Q₀²), unbounded without γ_L | G_eff = G_pot exactly at λ₀ = 0. The excess is AeST's static force law, not a sign flip of a kinetic term. T2a (Krein, I = 0) passes. |
| T4 | at the stress value I = 2e-3: two unstable roots for k ≤ 0.003 μ, and growth up to 1865 μ with γ_L | **The GR + k-essence control shows the same thing**: max 2 unstable roots per k at I = 2e-3. Both systems also have the same negative-Krein ω² > 0 root, W² ≈ 2k⁴/(9IQ₀) with Krein ∝ −I, at identical (k, W²), e.g. W² = 1.2034e-6 at k = 1e-3 μ, I = 2e-7. Source: the √−g⁽²⁾·ρ̄ metric-squared and Φφ̇ terms, which a real FRW background would cancel against its curvature. The swindle leaves them uncancelled. **This is a Jeans-swindle artifact, not AeST's.** The growth past k_c at I = 2e-3 is an O(I²) tail, Γ² → I²/4 (≤ 4πG̃ρ̄·I/2Q₀). At the physical I = 2e-7 the band ends at 240 μ. |

The frozen verdict stands as printed: CLAIM FAILS. The table is the post-result reading.

## Answers to the four questions

1. **The control.** Yes: criterion (i) flags normal gravity.
   - Newtonian cold dust: E_J = −4k² (machinery units; −2πG|δρ|²/k² after normalisation), < 0 at all k.
   - GR + k-essence dust: E_J < 0 throughout its Jeans band k < √K₂ Q₀.
   - Both have the T1 sign structure.
2. **Ghost vs instability.**
   - The kinetic structure is healthy at I = 0: one ω = 0 dust degree of freedom, and one massive scalar with positive Krein.
   - The negative energy is a gravitational binding term over a bounded band (with γ_L: k < k_c = 242.75 μ).
   - The growth rate is ≤ √(4πG̃ρ̄).
   - So it is not a ghost. It is non-Newtonian between μ and k_c (contact term).
   - The ghost-like ω² ∝ k⁴/I root seen at I > 0 is shared exactly with GR + k-essence (artifact).
3. **Vacuum.**
   - There is no background dust (ρ̄ = 2IQ̄ = 0). The mode itself is a dust lump (δQ ≠ 0), whose energy is its
     self-gravity in AeST's static potential.
   - The k-essence control has the same zero-background mode. It is not a matter-free negative-energy mode.
   - Open (nonlinear, reported only): at K's minimum, linear δρ can be negative. This holds in the control too.
4. **The rate.**
   - It is bounded: 0.99991 × 4πG̃ρ̄ at I = 2e-7, and 0.964 × 4πG̃ρ̄ at I = 2e-3.
   - It falls with k.
   - With γ_L it ends at k ≈ 240 μ (I = 2e-7). Without γ_L it decays as 1/k² but never ends.
   - It does not diverge.

## Checks: 4/5 PASS (K5 frozen FAIL kept), exit 1

| check | result |
|---|---|
| K1 | C5's two E_J and H1's two Γ² are reproduced from C5's own source (difference 0) |
| K2 | `jordan_energy` signs: free particle +, ghost −, first-order free particle + (T0) |
| K3 | the GR operator in T1a is exactly C5's `sz_lagrangian` minus the AeST terms (difference 0) |
| K4 | Clebsch: `jordan_energy` = 2 × hand Noether H (a constant normalisation); Γ² = 4πGρ̄ at every k |
| K5 **FAIL** | exact Γ² vs O(I) at k = 1e-3 μ, I = 2e-7: rel 0.077 (threshold 1e-4) |

**Why K5 fails.** The error tracks Γ²/W²_artifact: 0.077, 1.1e-3, 8.7e-6 and 3e-7 at k = 1e-3, 3e-3, 1e-2 and 0.1 μ.
The frozen test point sits where the swindle-artifact root (W² ≈ 1.1e-6) comes close to Γ² (≈ 1e-7) and mixes with it.
The exact rate is lower than the O(I) one.

**Mutation** (`H3_MUTATE=1`: repulsive Newtonian gravity, I → −I). K4 fails (Γ² − 4πGρ̄ = −ρ̄/2) and T1's sanity line
fails, as frozen. K1 and K5 are bypassed under mutation by design. Outputs: `*_MUTATE.*`.

## History (AMENDMENT A1, post-result; no pass line or declared value changed)

- Criteria frozen first (04355110c4). Run 1 is kept as `*_RUN1.*` (4/5; it printed UNDECIDED).
- A1-1: Q₀ > 0 in the k-essence norm. Run 1 left Abs(Q₀), so its Γ²(0) residual showed I(|Q₀| − Q₀)/2.
- A1-2: K5's O(I) closed form had I = 0 substituted (rel = inf). It now keeps I symbolic, and K5 fails honestly at 0.077.
- A1-3: T3 now follows the frozen wording. Run 1 also demanded the control's E_J < 0 at every k.
- A1-4 (reported only): G_pot on the Jordan mode; the GR + k-essence exact-root scan; Krein of every ω² > 0 root at I > 0.
- A1-5: the verdict mapping follows the frozen §3. Run 1 sent any K failure to UNDECIDED and any non-PASS to FAILS.
- Run: `OMP_NUM_THREADS=1 nice -n 15 python3 h3_jeans_control.py`. 73 s, 0.07 GB RSS, one thread, no downloads.

## What this does not show

- **Linear only, Jeans swindle on Minkowski.** There is no Hubble friction, and k ≫ aH. The k⁴/I artifact shows the
  swindle's limits. A consistent FRW linear run (C7's patched CLASS) is the real test of the band and the rate.
- **Strong field, nonlinear and quantum are open.**
  - The negative-δρ branch at K's minimum is nonlinear.
  - The μ < k < k_c contact term in a nonlinear collapse is open.
  - C5's strong-coupling estimate covers W's cubic only.
- **C5 defect (b) is open:** γ_L gives ω² ∝ k⁴ with no cone.
- **Whether the contact term G k²/(K₂Q₀²) is visible in data was not computed.** It is linear-only at Y = 0; it is not
  the MOND regime.

## Inputs

| input | class | source |
|---|---|---|
| SZ21 Minkowski action, "Jeans-type" remark | literature, on disk | `../_external_data/aest_papers_2026_10_22/src_2007.00082/newRMONDLett.tex` |
| C5 `quad_matrix`, `jordan_energy`, `sz_lagrangian` | FRAMEWORK-NATIVE, exec'd read-only | `covariant_push_2026_10_22/C5_health/c5_health.py` |
| H1 dust term and Γ² | FRAMEWORK-NATIVE | `rebuild_2026_10_22/H1_aest_F/` |
| K_B = 0.05, μ⁻¹ = 1 Mpc, L★ = 24 pc (FITTED), I ∈ {2e-7, 2e-3} | declared | FROZEN_CRITERIA §2 |
