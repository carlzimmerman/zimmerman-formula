# H1_aest_F: FROZEN CRITERIA (committed alone, before any scored number)

## Question

Is there a free function F(Y, Q) in AeST's class (Skordis & Złośnik, arXiv:2007.00082, eq. `NT_A_action`) that meets
all five conditions below at once?

- (i) healthy at Y = 0;
- (ii) normal linear growth on FRW;
- (iii) the galactic law on SPARC, within the data;
- (iv) the stiffness-screened Solar System (γ_L operator, C6);
- (v) BBN (C2 P2: K_B < 0.078 and λ_s > 24.7).

Background lanes: C1 (capped F gives μ = x/(1+x) exactly), C5 (that F has a negative-energy ω = 0 mode at Y = 0),
F3 (v3's J′(0) = −1 removes Newtonian growth), C2/C7 (AeST dust growth; C7 names λ_c = F_Y(0)/(2−K_B) and sets it to 0).

## What was done before this file (disclosure)

A scratch sympy run (outside the repo) built the Jeans-swindle quadratic action described in §2 and found the closed form
of the dust growth rate Γ²(k; λ₀, L★), and that E_J/Γ² is minus a perfect square. These are derivations, not scores.
**No SPARC fit, no Q₂ and no growth number at the declared parameters below has been computed.**
The pass lines below were written before any of those.

## 1. The F family (frozen; nothing outside it is scored for the verdict)

Write f(x) ≡ dJ/dY with J = F(Y, Q₀)/(2−K_B), x = √Y/a₀ (VSZ, arXiv:2304.05134, eq. `def_f_general`), and
λ₀ ≡ f(0) = F_Y(0, Q₀)/(2−K_B), which is SZ's Minkowski "λ_s" (C7's λ_c).

**SZ's own family.** VSZ eqs. `mu_Simple`, `mu_Exp`, `mu_Hyp`, with the limits SZ eqs. `Jcal_GR` / `Jcal_MOND`:

| id | f(x) | λ_s |
|---|---|---|
| SZ-simple | x/(1+β₀+β₀x), β₀ = 1/λ_s | 24.7 (the BBN edge, C2 P2) |
| SZ-exp | λ_s(1 − e^{−x/(1+λ_s)}) | 24.7 |
| SZ-sharp | min(x, λ_s+1)/(1+β₀) | 24.7 |
| SZ-∞ | x (the λ_s → ∞ limit of all three) | ∞ (SZ's CMB "MOND models") |

**Boundary members (λ_s = ∞ with a cap; "simple smooth interpolants" from the record's capacity family, D7c):**

| id | f(x) | law |
|---|---|---|
| cap-n1 | x/(1−x) | C1's F; μ = x/(1+x), the canonical law exactly |
| cap-n2 | x/(1−2x) | ν = √(1+1/y), the n = 2 law |

Free constants that F carries: a₀ (both footings, κ = ½ FITTED) and λ_s (at the two declared values only). K_B, K₂, Q₀
(μ) are AeST's other constants; F does not fix them. **No constant is scanned or fitted to data.**

**Outside the family (supplementary, never a FOUND):** the floor door f = λ₀ + x/(1−x), evaluated only at the
declared λ₀ ∈ {1e-3, 1e-2, 1e-1}. It costs one POSTULATED constant. Its numbers map the conflict; no λ₀ is selected.

## 2. Conditions, computations and pass lines

**Static map used throughout (VSZ eqs. `Phi-Orig`, `Chi-Orig`, μ-term dropped at galaxy radii, C3 r_C ≥ 230 kpc for 1e11 M☉):**
g/a₀ = y/(1+β₀) + x, with f(x)·x = y/(1+β₀), y = g_N/a₀.

**(i) Health at Y = 0.** C5's Minkowski scalar action (SZ eq. `Minkowski_action`, exec'd from C5's source, read-only),
with λ_s → λ₀, plus C5's γ_L term.
- (i-lit) PASS iff λ₀ > 0 (SZ's literal condition; 0 < K_B < 2 and K₂ > 0 are parameter choices, always admissible).
- (i-band) reported: the ω = 0 Jordan-mode energy E_J(k) is > 0 for all k above a finite k_c (without and with γ_L).
- (i-strict) reported: E_J(k) ≥ 0 at every k.
- The verdict's (i) is (i-lit).

**(ii) Linear growth.** Jeans swindle on Minkowski: C5's scalar action (λ_s → λ₀) plus the dust-background term
2I[√−g (Q − Q̄)]⁽²⁾ from √−g·2K(Q), with I = K′(Q̄) > 0, K(Q̄) = 0. The growth rate Γ²(k) = −ω² is the O(I) root.
- (ii-IR) PASS iff Γ²(k → 0) = 4πG̃ρ̄ (= IQ̄/2 in 16πG̃ = 1 units) exactly.
- (ii-q) PASS iff max over k ∈ [1e-3, 0.3] h/Mpc of |Γ²_F(k)/Γ²_ref(k) − 1| ≤ 0.01.
  - Γ²_ref is the same AeST with λ₀ = 0, so the test isolates the F change.
  - Declared values: μ⁻¹ = 1 Mpc (SZ's floor), L★ = 24 pc, K_B = 0.05, h = 0.68.
  - μ⁻¹ = 10 Mpc and Γ²_ref/Γ²_GR (the F-independent AeST suppression) are reported, not graded.
- (ii-lit) reported: λ₀ = 0 (C7's linear system unchanged).
- The verdict's (ii) is (ii-IR) AND (ii-q).

**(iii) SPARC.** AG4b's pipeline, reproduced verbatim: 170 galaxies, per-galaxy MAP Υ_disk under N(log 0.5, 0.10 dex),
bulge 1.4 Υ, s₀ = 0.05 dex, both footings.
- PASS iff the paired median-rms z of the candidate against the canonical law (n = 1) is > −2 on both footings.
- Reported for both footings:
  - the paired z against ν_RAR = 1/(1 − e^{−√y}) (a reference description, not a law);
  - S1 = Σ Δχ²_min against the canonical law and against ν_RAR;
  - the canonical law's own z and S1 against ν_RAR, as the yardstick.

**(iv) Solar System.** C6's Route F, with the background response generalised to
J = diag(M_T, M_T, M_L), M_T = 1 + f(x_V), M_L = 1 + f + x_V f′(x_V).
- x_V is the candidate's own background at C6's Milky Way baryonic field g_Ne (E0–E3, per footing).
- Q₂ = −(2GM/5πL★³)·I₂.
- PASS iff Q₂ ≤ Park 5.2e-27 s⁻² at L★ = 24 pc for E0–E3 on both footings, AND M_T, M_L ≥ 1.
- Planets: the hedgehog GM/L★² is the κ⁻² term, which is independent of F; C6's values carry over (reported).

**(v) BBN.** PASS iff λ_s ≥ 24.7. K_B < 0.078 is admissible for every F (F does not fix K_B).

## 3. Validation checks (script prints `Kn PASS/FAIL value threshold`)

- **K1** C5 reproduction: the AeST Jordan energies (without and with γ_L) from C5's own source equal C5's JSON strings
  (sympy difference 0).
- **K2** E_J/Γ² + 8k²D²/(I Q̄³ N²) = 0 symbolically, with and without γ_L (D, N being the bracket polynomials), so
  E_J < 0 ⟺ Γ² > 0. Also Γ²(k→0) = IQ̄/2, and the λ₀ = 0, L★ = 0 closed form 1/(1 + 2u/(2−K_B)), u = k²/μ².
- **K3** On the Y = 0 background, Y has no O(ε⁰) or O(ε¹) part, and its O(ε²) part is |∇φ + Q̄A|². So any
  F term beyond linear in Y is at least cubic, and health at Y = 0 sees F only through λ₀ (and K″).
- **K4** Static maps:
  - cap-n1 equals the canonical ν₁ to 1e-12 on y ∈ [1e-6, 1e4], and cap-n2 equals √(1+1/y) to 1e-12;
  - the tabulated maps match a direct solve to 1e-8 at 200 test points;
  - SZ-simple's deep limit g → √y (rel ≤ 1e-3 at y = 1e-8) and Newtonian limit g → y (rel ≤ 1e-3 at y = 1e8).
- **K5** AG4b reproduction: n = 1 vs n = 2 primary D and z equal AG4b's JSON to 1e-9 on both footings.
- **K6** C6 reproduction: the generalised I₂ at (1 + x_e, (1 + x_e)²) equals c6_solver.routeF_I2(x_e, 0) to 1e-10, and
  Q₂ equals C6's R1_physical canonical/alt |24| E0–E3 to 1e-6 relative.

## 4. Verdict rule

- **FOUND:** a family member (§1, family only) passes (i), (ii), (iii), (iv) and (v) on both footings.
- **NONE IN THE FAMILY:** no member passes all five. The README names which condition conflicts with which, and why.
- **UNDECIDED:** any of K1–K6 fails.
- The floor door is reported separately: "outside the family, +1 POSTULATED constant". It is never a FOUND.

## 5. Mutation (`H1_MUTATE=1`, outputs `*_MUTATE.*`)

The sign of the dust-background term flips (I → −I in ΔL), and cap-n1 becomes x/(1+x). K2 and K4 must FAIL.

## 6. Assumption ledger

| ingredient | class | source |
|---|---|---|
| SPARC rotmod V_obs, e_V, V_gas, V_disk, V_bul | RAW | `real_research/data` via `campaign_fresh_gravity/CFG4_common.py` |
| distances, inclinations (master table) | SURVEY-CALIBRATION | same |
| Υ prior N(log 0.5, 0.1 dex), bulge 1.4 Υ | SURVEY-CALIBRATION (E1/E4: SPS soft) | AG4b |
| s₀ = 0.05 dex floor; paired median-rms z; S1 | record statistic | AG4b |
| algebraic per-point law (exact in spherical AQUAL, approximate in discs) | approximation, applied identically to every law | AG4b, D7c |
| a₀ footings 9.3603e-11 / 1.1312e-10 | FITTED (κ = ½) | CFG4_common (FP0) |
| ν_RAR | reference description of the data's shape (comparator only) | CFG4_common |
| AeST action, Minkowski action, VSZ static equations and f families | literature, on disk | `../_external_data/aest_papers_2026_10_22/` (C2 PROVENANCE sha256) |
| C5 linearisation code | FRAMEWORK-NATIVE, exec'd read-only | `covariant_push_2026_10_22/C5_health/c5_health.py` |
| Jeans swindle (Minkowski + dust density, no Hubble friction; k ≫ aH) | approximation | this lane |
| μ⁻¹ ≥ 1 Mpc | literature (SZ) | SZ eq. `NT_quasi_Phi` text |
| μ-term neglected at SPARC radii | AeST-native, bounded by C3 r_C | C3 |
| λ_s ≥ 24.7, K_B < 0.078 | FRAMEWORK-NATIVE + BBN (A78) | C2 P2 |
| L★ = 24 pc | FITTED | D10 / C6 |
| C6 Route F kernel, g_Ne (E0–E3), Q₂ values | FRAMEWORK-NATIVE | `covariant_push_2026_10_22/C6_literal_cassini/` |
| Hees 9.0e-27, Park 5.2e-27 s⁻² | RAW-derived ephemeris bounds | C6 |
| h = 0.68 | FRAMEWORK-NATIVE (C2 native H₀ 67.2–68.6) | C2 |

No ΛCDM-processed input enters a graded line.

Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes, no downloads (a 1024³ job is live).
κ = ½ FITTED. Footings never pooled. No dark-matter particle. Never "theory closed". Nothing here says the data favour the framework.
