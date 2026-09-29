# CFG179 — Door 11: merging rivers and a swirled river

Frozen question: `FROZEN_QUESTION.md`, written and hashed (`FROZEN_QUESTION_SHA256.txt`, verifies) before any script. Governing file: `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, with Addenda 1–2 and Erratum 1. P2 is ν = √(1 + a₀/g_N), per the Erratum. Both a₀ footings are used. κ = ½ is FITTED. This is a scoped answer: nothing here says the theory is closed, and nothing here is a mechanism for the law.

## Bottom line

- **Merging rivers must interact.** Any flow law with MOND's square-root pull is nonlinear in its source. A river inside a larger river therefore obeys a changed internal law: the external-field effect (EFE). This is proved as a no-go (S1 M3). The only way out is a rule that keeps each system's river separate. That is candidate B's ownership rule, which is nonlocal and is not a flow law.
- **How the merge's EFE scores against the record:**
  - Chae's signal: consistent in size, but it is not shown to track the environment.
  - Coma UDGs: fails at 5.4–5.6σ (the E7 form).
  - Solar System: fails through the external-field quadrupole (committed: 4.0–5.7× the ceiling).
  - Gaia DR4: predicts boosted wide binaries (Arm A 1.16–1.18, or 1.08 in the MI form). Ownership's Arm C predicts 1.000.
  - The committed population scorecard is 6/14 for the merge against 9/14 for ownership.
- **Swirl.** GR's own swirl (frame dragging) of a Milky-Way-like disc is 5 × 10⁻⁸ to 4 × 10⁻⁷ of Newtonian gravity: the river turns at about 0.1 m/s.
  - A Λ-vacuum swirl pushes co-rotating stars inward and counter-rotating stars outward.
  - A river dragged by matter (Fresnel-like) is excluded, because retrograde orbits could not exist.
  - A universal drag is limited to λ_c ≤ 0.052 by the declared co/counter-rotation bound.
  - A spin-scaled drag is limited to a median-galaxy λ_c ≤ 0.044 by the RAR's scatter.
  - The only swirl with no new constant (vorticity a₀/c) is allowed everywhere, and it is invisible (2 × 10⁻⁴ dex).

## For the owner, in plain words

**When two rivers meet.**
- In Einstein's gravity the river picture is exact for one body: space flows inward toward a mass like water toward a drain.
- Two rivers do not add their *speeds*. What adds is the speed *squared*, which is the depth of each drain.
- Ordinary gravity is "linear": a small river inside a big one behaves normally, and only the big one's tides matter.
- The extra, MOND-like pull is different. It grows as the *square root* of the mass, so two equal masses together give √2, not 2, times the pull of one. That makes the rule nonlinear.
- So a small river sitting inside a strong big river gets partly drowned: it loses much of its own extra boost. Inside the Milky Way's river at the Sun's distance, a faint system keeps only about 10–36% of its isolated pull. This is the "external-field effect".
- We proved it is not optional for any river law of this kind. The only escape is a rule under which each system keeps its own river separate. That is the "ownership" rule the program already uses (candidate B), and it is not a flowing-river law.

**How we would see a merge.**
1. Galaxies in crowded neighbourhoods should turn slightly slower in their outskirts. Chae's data show a signal of about the right size, but it has not been shown to follow each galaxy's neighbourhood.
2. Faint galaxies inside the Coma cluster should be nearly Newtonian. They are not: their stars move about 4–5 times faster than a merging river allows.
3. Wide binary stars in our Galaxy should move faster than Newton predicts: 1.16–1.18 on the registered scale, where Newton is 1.00. Gaia DR4 (2 December 2026) will measure this. A Newtonian result rules out the merging-river form of the law.
4. The Solar System sits inside the Galaxy's river. A merge would squeeze the planets' orbits by 4–6 times more than the planets allow.

**When a spinning galaxy stirs the river.**
- In Einstein's gravity a spinning mass drags space around it. For the Milky Way this drag is tiny: the river turns at about 10 cm/s, and the push is a few ten-millionths of ordinary gravity.
- A stronger swirl of the dark-energy river would do something distinctive. Stars moving *with* the swirl would be pushed inward, and stars moving *against* it would be pushed outward.
- That sign flip is the fingerprint. A galaxy with two star discs spinning in opposite directions would show two different rotation speeds. In our own Galaxy, stars orbiting backwards would feel a weaker pull than stars orbiting forwards.
- Backward-orbiting stars and counter-spinning discs exist and are bound. That rules out a river dragged along by matter, like the 19th-century idea of light dragged by moving water: such a river would fling every backward-orbiting star away.
- A weak swirl, below about 5% of a disc's speed, is still allowed by galaxy data. The one swirl that needs no new number is set by the dark energy itself (vorticity a₀/c). It is allowed everywhere and far too small to see.

## What was run

Every script runs in under 1.3 s. Every script exits 0 in main mode and 1 under MUTATE: each MUTATE control bites.

| script | checks (main) | MUTATE control | MUTATE result |
|---|---|---|---|
| `cfg179_s1_merge_symbolic.py` (sympy) | 12/12 | kernel made linear (ν ≡ 2) | M3b "merged rivers interact" FAILS; 11/12, rc 1 |
| `cfg179_s2_merge_numbers.py` | 7/7 | every external field set to 0 (ownership) | Coma headline flips to pass (1.8σ / 1.6σ); DR4 merge rows become 1.000; 5/6, rc 1 |
| `cfg179_s3_swirl_gr.py` | 7/7 | vorticity term dropped (irrotational river) | W1, W2a, W3 and W4 FAIL; 3/7, rc 1 |
| `cfg179_s4_swirl_bounds.py` | 6/6 | spin proxy made constant | S-j's scatter bound disappears (λ_max → 1); 5/6, rc 1 |

- Outputs are `<script>.out` and `_results.json`, plus `_MUTATE.out` and `_MUTATE_results.json`.
- Kept first runs:
  - `_firstrun*` for S1, S2 and S3.
  - `cfg179_s4_swirl_bounds_firstrun_crash.out` for S4.
  - What each first run shows is listed under Disclosures.
- Shared harness and constants: `cfg179_common.py`.

## Q-merge results

| id | result | status |
|---|---|---|
| M1 | **Painlevé–Gullstrand–de Sitter.** G^t_t = G^r_r = −(r v²)′/r² and G^θ_θ = −(r v²)″/(2r). The Einstein–Λ vacuum is a linear ODE in v², with solution **v² = 2M/r + Λr²/3: squared flows add**. A linear velocity sum leaves a residual −√6 √(ΛM) r^(−3/2). Its cross term pulls as r^(−½), not as deep-MOND's r^(−1). | DERIVED (sympy) |
| M2 | **The river law**, from the Newtonian limit of the river metric: ẍ = ∂_t v + (v·∇)v − w × (∇ × v), with w = ẋ − v.<br>**Two masses:** the summed infall v₁ + v₂ is irrotational, but it pulls with a spurious cross term ∇(v₁·v₂). At the declared point that term is 1.53× the Newtonian force. In the weak field the potentials (v²) add, not the velocities.<br>**GR's own merge nonlinearity** is O(U/c²) ≥ 5.4 × 10⁻⁷. GR obeys the strong equivalence principle, so it has no EFE beyond tides. | DERIVED (sympy) |
| M3 | **No-go.** A local merged law with no EFE for all (z, z_e) requires F(z + z_e) − F(z_e) = F(z). Differentiating in z_e gives F′ constant: Newton with a rescaled G. P2 violates this at all 6 declared points (residuals −0.08 to −0.38), and F′(0⁺) = ∞. Deep-MOND homogeneity: two equal sources give √2, not 2. **Merged rivers must interact.** | DERIVED (sympy) |
| M4 | **The merged law for P2.** Aligned 1-D AQUAL and QUMOND are the same law (Chae 2020's eq. 6, the one CFG8 fitted), with susceptibility −1.<br>**E7** was re-derived by clearing the radical: x³ + e₇x² − b(b+1)x − b²e₇ = 0, with e₇ = √2 g_ext/a₀. Its susceptibility is −1/(2(1+b)) per unit e₇, i.e. about 0.71× the 1-D value in deep MOND.<br>**External-dominated limits:** E7 gives G_eff/G = 1/μ_fw(e₇); P2 1-D gives ν(1+L) (parallel), ν (perpendicular) and ν(1+L/3) (isotropic). | DERIVED; E7's θ₀ = √2 POSTULATED |
| T | **Survival of a system's own pull inside a host**, x_merge/x_iso (1-D / E7):<br>• Milky Way field at the Sun (1.9 a₀), canonical: 0.10 / 0.12 at b = 0.01; 0.31 / 0.36 at 0.1; 0.72 / 0.81 at 1.<br>• Coma (0.845 a₀): 0.12 / 0.15 at b = 0.01.<br>• SPARC median environment (0.048 a₀): 0.63 / 0.72 at b = 0.01. | computed |
| M5 | **Chae (gate 1.15).** Control C1 reproduces CFG8's V4/V5 environmental fits to 4e-16.<br>**Frozen statistic** (zero-intercept A in e_fit = A·e_env):<br>• A = **0.76 ± 0.16** (canonical) / **0.88 ± 0.15** (alt).<br>• Ownership's A = 0 sits at 4.7σ / 5.9σ.<br>• The 1-D merge (A = 1) sits at 1.5σ / 0.8σ.<br>• The E7 bracket [0.46, 0.71] sits at 0.3σ / 1.1σ.<br>• By the declared rule: **"supports the merge EFE"** on both footings, and for the maxclu and noclu fields too.<br>**Post hoc (added after the first run, labelled):**<br>• The tracking test, with the intercept free and χ²/dof ≈ 9–11 inflation, gives a slope of **0.71 ± 0.80 / 0.60 ± 0.73: NON-DIAGNOSTIC**.<br>• Dropping NGC 5055 and NGC 5033: A = 0.39 ± 0.18 / 0.56 ± 0.17.<br>• Equal weights with a bootstrap: A = 0.25 ± 0.29 / 0.69 ± 0.29.<br>• Low-acceleration ratio of medians: A = 0.67 ± 0.24 / 0.99 ± 0.24.<br>• Committed: Spearman p 0.87 / 0.76 (no rank correlation); B's zero at 1.7σ / 2.7σ (CFG8 H1).<br>**Reading:** Chae's fits carry a mean EFE-like signal of about the size a merge predicts. Ownership's zero is disfavoured at 0.8–5.9σ, depending on the estimator. **Tracking of the actual environment is not shown.** So the data are consistent with a merge EFE; they do not detect one. | MIXED |
| M6 | **Coma UDGs (gate 1.16), stars only.** Control C2 reproduces L23's isolated +0.3965.<br>**E7 merge** at the β-model field at 1.13 Mpc: **+1.309 / +1.275 dex = 5.6σ / 5.4σ** against 0.235 dex, a FAIL. Over L23's field bracket (0.427–1.059 a₀) it spans 4.7–5.7σ.<br>P2 1-D: 5.3–6.1σ. P2 isotropic: 4.5–5.7σ.<br>Committed: L23's EFE rival 4.9σ / 4.7σ; B (ownership plus infall gas) 1.3σ / 1.1σ; first infall 2.7σ (L23, not recomputed with E7).<br>This lane's P2 rows sit about 0.13 dex above L23's ν_RAR row. The cause is P2's missing +½ tail (hand estimate about 0.08 dex) plus one field value for all eleven galaxies. | FAIL for the merge |
| M7 | **DR4 (gate 4.06).** Control C3: z_e = 1.4642 / 1.1494 (prereg 1.4647 / 1.1513); √ν = 1.1390 (prereg 1.1389).<br>Point-field estimates, never scored (canonical, primary field): P2 perpendicular 1.139, parallel 1.017, isotropic 1.100; E7 1.097.<br>Committed, with the distance of γ̂ = 1.000 from each:<br>• Arm A (merge, P2 as modified gravity, full solve) 1.1614–1.1814 / 1.1917–1.2267: 5.8–6.5 / 6.8–8.1 σ_tot.<br>• MI merge (Amendment 2, α = 1) 1.0799: 2.9 σ_tot.<br>• Arm C (ownership) 1.000. | cites committed |
| M8 | **Solar System (G5).** Control: P2's α = 1 monopole is a₀/2 = 1279× (alt 1545×) the Earth bound. This is P2's own liability, not specific to the merge.<br>The merge-specific EFE quadrupole has a natural scale a₀/r_M(Sun) = 7.9 × 10⁻²⁶ s⁻² = 15× (alt 20×) the Q₂ ceiling. The committed strict law gives **4.0–5.7×**, a FAIL (GATES 4.01). Ownership leaves only the host tide, 1.6–2.6 × 10⁻³¹. | FAIL for the merge (committed) |
| M9 | CFG7 H0, read from the committed `.out`: ownership 9/14, the external-field (merge) reading 6/14, on both footings. | cites committed |

## Q-swirl results

| id | result | status |
|---|---|---|
| W1 | A rigidly rotating river reproduces the rotating-frame Coriolis and centrifugal terms exactly: the river's vorticity is the Coriolis force. | DERIVED (sympy) |
| W2 | A swirl v = λ_c V φ̂ gives a_R = −λ_c²V²/R − (u − λ_c V)λ_c(V/R)(1+s).<br>**Prograde and retrograde tracers differ by 2λ_c(1+s)V²/R.** For a flat curve, prograde gets −λ_c V²/R and retrograde +λ_c V²/R.<br>The swirl exerts no vertical force. λ_c = 1 carries the stars, which is a restatement of the rotation curve. | DERIVED (sympy) |
| W3 | GR at 1PN: g₀ⱼ = −4Uⱼ/c³ gives a_GM = −(4/c²) v × (∇ × U). This is a river with shift v_s = 4U/c². | DERIVED (sympy) |
| W4 | **GR's swirl of the Milky Way disc** (6e10 M☉, exponential, R_d 2.5–3.5 kpc, h 0.05–0.2 kpc, R = 8.2 and 10 kpc):<br>• a_GM/g_N = **−2.3 × 10⁻⁷** at the base setting; range 5.0 × 10⁻⁸ to 4.4 × 10⁻⁷. It points outward for co-rotating stars.<br>• Swirl speed 0.11 m/s.<br>• Local frames rotate at 4.3 × 10⁻⁷ mas/yr (7.6 × 10⁻⁸ Ω_gal).<br>Controls: the ring kernels match quadrature to 2e-15; the Newtonian force matches Freeman's thin disc to 0.8%. | computed; PASS "negligible" |
| S-F | **Fresnel drag**, λ_c = ρ_b/(ρ_b + ρ_Λ): 1 − λ_c = 1.1 × 10⁻⁶ (solar neighbourhood) to 1.3 × 10⁻⁴ (outer HI). **No retrograde circular orbit exists** under it, yet bound retrograde and counter-rotating populations exist. | EXCLUDED |
| S-u | **Universal drag.** SPARC's prograde gas absorbs it into the fitted law. The G8 co/counter bound (declared 10.4%) gives **λ_c ≤ 0.052** (0.047–0.058 for s = ±0.1). | derived bound |
| S-j | **Spin-scaled drag**, λ_c ∝ (R_d V_flat)^p, on 123 SPARC galaxies with a 0.53-dex spread in j. RAR scatter ≤ 0.043 dex gives:<br>• p = 1: **median-galaxy λ_c ≤ 0.044** (Milky-Way-like disc 0.071; most spinning galaxy 0.44).<br>• p = 0.5: ≤ 0.13.<br>• p = 2: ≤ 0.005.<br>At the 0.048 edge: 0.048. | derived bound |
| S-L | **Λ-scale vorticity** ω = λ a₀/c (tied at λ = 1: ω = H_Λ/Z). At λ = 1 it adds **2.0 × 10⁻⁴ / 2.3 × 10⁻⁴ dex** of scatter, invisible. The scatter allows λ ≤ 299 / 266. | allowed, invisible |
| S-a₀ | **MOND-scale vorticity** ω = λ a₀/V_flat. It is mostly an a₀-shaped boost that the law absorbs: the scatter allows λ ≤ 0.25 / 0.21, while G8 gives λ ≤ 0.052. | derived bound |
| G5 | **At the Sun**, for swirls at their galaxy-side bounds:<br>• Frame rotation 0.07–0.30 mas/yr. That is ≤ 2% of GP-B's allowance, which is quoted from memory and is not a verdict.<br>• Coriolis push on Earth 18–76× the 2σ monopole bound, if the swirl reaches the Solar System unscreened and is not absorbed as a frame rotation (the declared caveat).<br>• The tied S-L passes: 0.25× the bound, 1.0 × 10⁻³ mas/yr. | CONDITIONAL / OPEN |

## Door-11 gates

| gate | merge (local EFE) | swirl |
|---|---|---|
| G1 as mechanism | not scored. The merged law is P2 written as QUMOND/AQUAL, a restatement (CFG171's L4). | not scored. A prescribed swirl is a restatement (λ_c = 1 carries the stars). |
| G2, G3, G6 | UNDEFINED (no action, no perturbation equations, no stress-energy) | UNDEFINED |
| G4 | 1-D merge: no new constant. E7 carries the postulated θ₀ = √2. | λ is a new constant, except S-L at λ = 1 (ω = a₀/c) |
| G5 | **FAIL**: the EFE quadrupole is 4.0–5.7× the Q₂ ceiling (committed strict law). P2's own α = 1 monopole (1279×) fails whatever the merge does. | GR swirl and tied S-L PASS. Galaxy-bounded swirls: CONDITIONAL (18–76× the monopole bound if unscreened and unabsorbed). |
| G7 | not scored | not scored |
| G8 | The EFE is anisotropic: point-field parallel 1.017 against perpendicular 1.139, a sign rule already in Amendment 2(f). The committed directional test O6 is contested (+2.95, p 0.029, n = 16, against −1.70 ± 2.12, n = 25). Not scored. | Declared bound λ_c ≤ 0.052 (a 10.4% co/counter contrast). **No committed counter-rotating sample exists, so this is not scored against data.** Fresnel drag FAILS. |

## DERIVED / POSTULATED / OPEN

**DERIVED** (sympy or exact numerics, in this lane):
- In GR's river, v² adds and v does not.
- The river law with vorticity.
- The two-body weak-field cross term.
- The no-go: no EFE plus a local merge requires F linear, so any deep-MOND law forces merged rivers to interact.
- AQUAL-1D ≡ QUMOND-1D for P2, with susceptibility −1.
- E7 re-derived, with susceptibility −1/(2(1+b)).
- The prograde/retrograde swirl contrast, and the absence of a vertical swirl force.
- GR's gravitomagnetism as a river shift 4U/c², and its size for a Milky-Way disc.

**POSTULATED:**
- The merge composition: aligned 1-D, or E7 with θ₀ = √2. The full 3-D merge is not solved here; Arm A's committed solve is the 3-D number.
- Every swirl law (S-F, S-u, S-j, S-L, S-a₀). None comes from an action.
- The G8 bound: the RAR's 95% scatter used as the size allowed for a co/counter contrast.
- κ = ½ (FITTED).

**OPEN:**
- Whether any action keys the river's boost to ownership (B's nonlocal C(r)) instead of the local total flow. That is the only way for rivers not to interact.
- Whether Chae's signal tracks the environment: the tracking test is non-diagnostic.
- Coma under first infall, with E7.
- DR4 (2 December 2026): a Newtonian result kills the modified-gravity merge and disfavours the MI merge at 2.9 σ_tot.
- Screening of a Galactic swirl inside the Solar System, and the ephemeris frame-tie bound on a uniform frame rotation. The data chat should verify GP-B's numbers and the frame-tie rate before any verdict.
- The direct swirl tests, not done here:
  - co- versus counter-rotating discs (NGC 4550-type);
  - prograde versus retrograde Milky Way halo tracers;
  - a radial-versus-vertical force mismatch (GATES 1.23 is NS).

## Exact hypotheses

- Static or steady weak field for M2, S3 and S4; exact GR only in M1.
- Aligned 1-D field composition for the merge; the isotropic and perpendicular factors are external-dominated limits.
- P2 is the only merge kernel; ν_mono is not run.
- Chae: CFG8's per-galaxy P2 fits and his environmental fields, converted exactly as CFG8 does. The E7 bracket is a linear-order mapping, not a refit.
- Coma: L23's estimator, weights, constants, the 0.235-dex total error and the stars-only baryons; a single field value per row.
- DR4: point-field limits only; the scored numbers are the committed Arm A, Amendment 2 and Arm C values.
- GR disc: thin exponential, the declared V_s(R), baryons only (no dark component in U).
- Swirl:
  - thin-disc midplane, flat-curve s = 0 for the headline bounds;
  - SPARC with Q ≤ 2, V_flat > 0, R_d > 0, i ≥ 30° (N = 123);
  - Υ 0.5 / 0.7, used only for S-a₀'s binning;
  - Milky Way R_d = 2.6 kpc for S-j's Milky Way row;
  - Earth u = 29.78 km/s.

## Disclosures

- **Not blind.** The frozen question lists everything read beforehand, including CFG8's slopes and L23's Coma numbers.
- **S1 first run** (`_firstrun`): M4a and M4c failed because sympy did not collapse √((z+1)²)-type radicals.
  - The zero test now simplifies, then denests, then falls back to a 40-digit numeric check at 6 fixed points.
  - M4a's AQUAL residual passes only through that numeric fallback.
- **S2 first run** (`_firstrun`): the same declared rows, without M5-R. The M5-R rows were added after the frozen zero-intercept amplitude was seen to be unable to separate tracking from a uniform offset.
- **S3 first run** (`_firstrun`): the hard-coded verdict prose said "about a millionth" and "~a metre per second", which overstated the printed numbers. The prose now prints the numbers; the numbers are identical.
- **S4 first run** crashed on log(g_bar ≤ 0) before any S-a₀ number was printed (`_firstrun_crash.out`). S-a₀ now uses only points with g_bar > 0.
- **In S2 MUTATE**, control C1 reduces to the N check, because with no external field the fit is undefined.
- **GP-B numbers** are quoted from memory and are flagged. No number in this lane's verdicts depends on them.
- **E7** is the equation book's MI worldline composition, KEEP-NOVEL-CONDITIONAL. It is used because the task names it; it is not a flow law.

Nothing here says the theory is closed. κ = ½ stays FITTED.
