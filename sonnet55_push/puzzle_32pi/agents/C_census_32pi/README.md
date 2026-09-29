# Census of 32π and its neighbours (lane C): where the factor appears, and where it comes from

(c = G = 1 unless stated; "the puzzle" = Λ = 32π a₀², equivalently Gρ_Λ = 4a₀², AΛ = 32π² with A = π/a₀²; κ = ½ stays FITTED.)

## Bottom line
- I catalogued 41 instances of 32π^k and its neighbours (16π, 8π, 64π, 128π, 96π, 15360π, 4π×8, 8π×4, ...), recomputed each one by script
  (c01–c04: 140 checks, 21 of them controls that must fail; c05: 4 clean runs pass and 10 deliberately mutated runs are caught, 14/14) and decomposed each coefficient
  into labelled origins whose product is verified exactly.
- The instances are **not one thing**. The two-π ones (32π²) are topological normalisations ((4π)ⁿ n! at n = 2; Vol(S³) × 16), scale-free. The one-π ones (32π, 1/32π)
  are field normalisations of the quadratic Einstein–Hilbert action (κ² = 32πG, Isaacson, Bondi), where "32 vs 16" is the convention e_ij e_ij = 2. The other "32"s are an
  angle integral (free fall 3π/32 = (π/2)²·3/(8π)), a divisor by accident (Hawking 15360π = 32π × 480), or 2⁵ with no π at all (Peters 32/5).
- The extra "4" in 32π = 8π × 4 has four distinct, derivable origins (action normalisation, cycloid angle, Schwarzschild r_s = 2M, Pfaffian/trace norm) plus the puzzle's own
  fitted 1/κ². Only the black-hole-geometry instances share the puzzle's horizon-type 4 (r_s κ = ½), and that horizon cannot exist in its own universe (p06).
- No classical instance links an acceleration/rate to Gρ with a π-free coefficient (the puzzle's a₀² = Gρ/4); every classical rate at density ρ is 3.7–7.1× faster than a₀.
  Isaacson's coefficient in Einstein form is π-free (Λ = ¼⟨ḣ_ij ḣ_ij⟩), so it cannot supply the π.
- **Verdict: NOTHING NEW on the derivation** (a clean negative census; scoped no-go for a common cause among the listed instances). κ = ½ stays FITTED.

## 1. What I did
Scripts (all in this directory, each with a `.out`; run `python3 c0N_*.py`; exit 0 = all checks and controls behave; `c05` takes about 100 s):

| script | content | checks (controls) |
|---|---|---|
| `c01_gravity_instances.py` | EH action to O(ε²) for a TT wave (sympy Ricci/Einstein tensor); Isaacson by two independent routes; κ² conventions; quadrupole (angular integral 8π/5, Peters 32/5, 64/5, chirp 96/5 π^{8/3}); Larmor; Kerr first law/Smarr; Komar/ADM; A κ² ≤ π over Kerr–Newman; Nariai/dS horizons; mean density of a Schwarzschild ball | 47 (7) |
| `c02_dynamics_thermal_instances.py` | Friedmann 8π/3 (FRW G_tt); free-fall integral (exact + quadrature); Jeans dispersion; Stefan–Boltzmann; Hawking power 1/(15360π) and lifetime 5120π; Casimir (dim. reg. + ζ(−3)); Euler–Heisenberg 1/(360π²) and the Schwinger rate 1/(4π³) from the proper-time residues | 31 (5) |
| `c03_topology_loops_anomalies.py` | Gauss–Bonnet from Riemann tensors (S⁴, S²×S², dS) and (4π)ⁿ n! for n = 1..6; explicit BPST instanton (F² = 192ρ⁴/(x²+ρ²)⁴, self-dual, ∫FF̃ = 32π², S = 8π²/g²); Chern–Simons 2πk; loop 1/(16π²); anomaly a, c → 1/(2880π²), ρ_dS = H⁴/(960π²), ∫⟨T⟩_{S⁴} = −1/90, GH² = 360π/N; Polyakov 96π; sphere volumes | 39 (5) |
| `c04_census_and_analysis.py` | the census as data (41 rows; decompositions verified exactly), classification, frequency table, origin-of-4 incidence, π-power of rate²–Gρ relations, rate/√(Gρ) table, hypothesis tests H_GW/H_FF/H_BH/H_TOP/H_ħ, MOND-literature coefficients | 23 (4) |
| `c05_mutation_runs.py` | re-runs c01–c04 clean, then 10 copies each with ONE load-bearing constant mutated (Isaacson 32π→16π, Peters 32/5→64/5, κ² 32π→16π, t_ff 3π/32→3π/16, lifetime 5120π→2560π, ∫FF̃ 32π²→16π², E₄ 24→12, ρ_dS 960π²→480π², two census atoms); every mutation must exit non-zero | 14/14 |

Sources actually opened (PDF fetched, text extracted, equations read): gr-qc/0501041 (eq. 4.1, 5.38, 5.40), 1703.05448 (eq. 2.9.11), 0802.1862 (eq. 1.1, 10.3, 12.7),
hep-th/9308075 (eq. 16, 30, 31, 35), hep-th/0406216 (eq. 1.9–1.11), hep-th/0402009 (eq. 2.3, 2.4, App. B), astro-ph/9805346 (eq. 6–9), 0801.3133, 1611.02269 (eq. 1.2, 1.7, 7.43),
1704.00780 (eq. 3, 31, 32), 1005.3537 (eq. 5, 6), 1104.2022 (eq. 9); Wikipedia pages "Hawking radiation", "Free-fall time", "Schwinger effect", "Schwarzschild radius" (secondary).
**Not opened, from memory, unverified as citations** (the numbers are re-derived by script, the attribution is not): Peters 1964, Isaacson 1968, Bardeen–Carter–Hawking 1973, Page 1976, the Bondi–Sachs mass-loss formula,
the textbook value ρ_dS = H⁴/(960π²) (the script reproduces it from the anomaly), Eddington luminosity, the Oppenheimer–Snyder collapse time equalling the Newtonian one, and the textbook source that the Wikipedia free-fall page cites.

## 2. The census (41 instances)
Origin tags: **E8** Einstein 8πG; **ACT** quadratic-action normalisation (EH ½, second-order expansion ¼, canonical ½, e_ij e_ij = 2, virial 2); **SPH** solid angle / sphere volume;
**HOR** Schwarzschild horizon (r_s = 2M, κ = 1/4M); **THM** thermal period 2π; **ANG** an angle integral (π/2); **SPEC** spectral integral/zeta/loop measure; **TOP** Pfaffian/winding/trace normalisation;
**NRM** norm convention; **FIT** the fitted κ. The product of the atoms equals the coefficient exactly (c04, 41/41); the labels are interpretation backed by the derivations, not unique numerics.

| id | instance (formula) | coefficient | origin | class | status |
|---|---|---|---|---|---|
| I01 | Isaacson GW energy ρ = ⟨ḣ_ij ḣ_ij⟩/(32πG) | 1/(32π) | E8⁻¹ · ½ · ¼ · 2 (ACT) | scale | opened gr-qc/0501041; derived c01 A (two routes) |
| I02 | graviton coupling κ² = 32πG (tensor-canonical) | 32π | 8π · 2 · 4 · ½ | scale | opened 1703.05448; derived c01 B |
| I03 | per-polarisation κ² = 16πG | 16π | as I02 × ½ (e_ij e_ij = 2) | scale | derived c01 B |
| I04 | Bondi mass loss (1/32π)∮N_AB N^AB | 1/(32π) | as I01 | scale | from memory; follows from I01 |
| I05 | ADM mass 1/(16πG)∮(∂_j h_ij − ∂_i h) | 1/(16π) | 1/(8π) · ½ (linearised G₀₀) | scale | derived c01 E |
| I06 | Komar mass 1/(4πG)∮ | 1/(4π) | 1/(8π) · 2 | scale | derived c01 E |
| I07 | first law δM = (κ/8π)δA + ΩδJ (Kerr, sympy) | 1/(8π) | 1/(2π) THM · ¼ (S = A/4) | scale (ħ) | derived c01 E |
| I08 | Schwarzschild area A = 16πM² | 16π | 4π · 4 HOR | scale | derived c01 E |
| I09 | Aκ² = π for Schwarzschild; ≤ π over Kerr–Newman | π | 4π · ¼ HOR | dimensionless-geometric | derived c01 E |
| I10 | Hawking T = 1/(8πGM) | 1/(8π) | 1/(2π) · ¼ HOR | scale (ħ) | derived c01 E |
| I11 | mean density of the Schwarzschild ball ρ̄ = 3/(32πG³M²) = 3/(8πr_s²) | 3/(32π) | 3 · 1/(4π) · ⅛ HOR | scale | opened Wikipedia; c01 F |
| I12 | Hawking power 1/(15360πG²M²) (photons, geometric cross section) | 1/(15360π) | (π²/60)(16π)/(8π)⁴ | scale (ħ) | derived c02 D4; opened Wikipedia |
| I13 | evaporation time 5120πG²M³ | 5120π | ⅓ × 15360π | scale (ħ) | derived c02 D4; opened Wikipedia |
| I14 | free fall Gρ t_ff² = 3π/32 | 3π/32 | (π/2)² ANG · 3/(8π) | scale | derived c02 D2 (exact + quadrature) |
| I15 | Friedmann H² = (8π/3)Gρ | 8π/3 | 8π · ⅓ (dim SO(3)) | scale | derived c02 D1 (FRW G_tt = 3H²) |
| I16 | Jeans (k_J c_s)² = 4πGρ | 4π | Poisson 4π | scale | derived c02 D3 |
| I17 | Peters P = (32/5)G⁴μ²M³/a⁵ (π-free) | 32/5 | 2 · 64 · ¼ · ⅕ | scale | derived c01 C |
| I18 | chirp ḟ = (96/5)π^{8/3}(GM_c)^{5/3}f^{11/3} | 96π^{8/3}/5 | 3 · 32/5 · π^{8/3} (ω = πf) | scale | derived c01 C |
| I19 | Larmor P = q²a²/(6π) (HL); Abraham–Lorentz shares the 6π | 1/(6π) | (4π)⁻² · 8π/3 (∮sin²) | scale | derived c01 D |
| I20 | Chern–Gauss–Bonnet ∫E₄ = 32π²χ | 32π² | 2! · (4π)² | topological | derived c03 T1 (S⁴, S²×S², n = 1..6); hep-th/9308075 eq. 35 form |
| I21 | BPST instanton ∫F^a F̃^a = 32π² (Q = 1) | 32π² | Vol(S³)=2π² · 16 (= 192/12) | topological | derived c03 T2; opened 0802.1862 |
| I22 | instanton action 8π²/g² | 8π² | 2π² · 16 · ¼ | topological | derived c03 T2; opened 0802.1862 eq. 1.1 |
| I23 | loop factor 1/(16π²) | 1/(16π²) | Vol(S³)/(2π)⁴ · ½ | scale-free (ħ) | derived c03 T4 |
| I24 | Chern–Simons level: ΔS = (k/12π)(24π²) = 2πk | 2π | | topological | derived c03 T3 |
| I25 | Euler–Heisenberg e⁴/(360π²m⁴) | 1/(360π²) | 1/(8π²) · 1/45 | scale (ħ) | derived c02 D6; opened hep-th/0406216 eq. 1.9 |
| I26 | Schwinger rate (eE)²/(4π³) e^{−πm²/eE} | 1/(4π³) | 2 · 1/(8π²) · π · π⁻² | scale (ħ) | derived c02 D6 (residues); opened hep-th/0406216 |
| I27 | trace anomaly a_scalar/(16π²) = 1/(5760π²) | 1/(5760π²) | 1/(16π²) · 1/360 | scale-free (ħ) | derived c03 T5; opened hep-th/9308075 |
| I28 | dS conformal scalar ρ = H⁴/(960π²) | 1/(960π²) | 6 · 1/(16π²) · 1/360 | scale (ħ) | derived c03 T5 |
| I29 | semiclassical dS: GH² = 360π/N | 360π | 3 · 960π² · 1/(8π) | scale-free (ħ) | derived c03 T5 |
| I30 | Polyakov (c/96π)∫R □⁻¹R = (c/24π)∫ω∇²ω × 4 | 1/(96π) | 1/(24π) · ¼ (R = −2∇²ω) | scale-free (ħ) | derived c03 T6; opened hep-th/0402009 |
| I31 | Casimir E/A = −π²/(720 d³) | π²/720 | ζ(−3) = 1/120 · π³/(6π) | scale (ħ) | derived c02 D5 |
| I32 | Stefan–Boltzmann σ = π²/60 | π²/60 | ¼ · π²/15 | scale (ħ) | derived c02 D4 |
| I33 | 32π² = 12 Vol(S⁴) = ∫_{S⁴(1)} R dV | 32π² | 12 · 8π²/3 | topological | derived c03 T1, T7 |
| I34 | dS horizon AΛ = 12π | 12π | 4π · 3 | dimensionless-geometric | derived c01 F |
| I35 | Nariai horizon AΛ = 4π (each) | 4π | 4π | dimensionless-geometric | derived c01 F |
| I36 | **puzzle** Λ = 32πa₀² (Gρ_Λ = 4a₀²) | 32π | 8π · 4 (FIT: 1/κ²) | scale | the record |
| I37 | **puzzle** AΛ = 32π², A = π/a₀² | 32π² | 8π · 4π | dimensionless-geometric | the record |
| I38 | Eddington L = 4πGMc/κ_es | 4π | 4π | scale | from memory |
| I39 | quadratic EH action (1/64πG)∫(ḣ_ij ḣ_ij − ...) | 1/(64π) | 1/(8π) · ½ · ¼ | scale | derived c01 A |
| I40 | Euclidean Nariai S²×S²: ∫E₄ = 128π² (χ = 4) | 128π² | 4 · 2 · (4π)² | topological | derived c03 T1 |
| I41 | Euclidean S⁴ / Schwarzschild: ∫E₄ = 64π² (χ = 2) | 64π² | 2 · 2 · (4π)² | topological | derived c03 T1; p01 |

Class counts (c04): scale 26, topological 7, scale-free 4, dimensionless-geometric 4. Not in the table: the domain-wall repulsion acceleration 2πGσ (from memory, not 32π-type) and string/LQG/brane-world normalisations (not surveyed).

## 3. Results

### 3.1 Scale versus topological
- **Topological (scale-free integers):** GB 32π²χ (I20, I40, I41), instanton ∫FF̃ = 32π²k and 8π²/g² (I21, I22), Chern–Simons 2πk (I24), the S⁴ identity (I33). c03 confirms they are the same at every radius / instanton size
  (∫E₄ = 64π² for every L; ∫FF̃ independent of ρ). They explain why 32π² is *the unit* of S⁴ topological charge; they carry no scale, so they cannot say how large a horizon is relative to Λ (agrees with p01, p10).
- **Scale-carrying:** all the G-, ħ- or ρ-dressed relations (I01–I19, I25, I26, I28, I31, I32, I36, I38, I39). The one-π ones with G are the Einstein 8π (source normalisation) times a rational.
- **Dimensionless-geometric but not topological:** Aκ² = π (Schwarzschild), AΛ = 12π (dS), 4π (Nariai), and the puzzle's AΛ = 32π². The first three are forced by exact solutions; the fourth is realised by no solution (p06; c01 F: the cosmological-horizon area over SdS stays in [4π, 12π]/Λ, the puzzle needs 32π² = 8π/3 × 12π).
- The puzzle sits in the "scale" column (a coefficient between two dimensionful quantities, Λ and a₀²) and, in its dimensionless form, in the "geometric" column; it is *literally* a topological number only by numerical coincidence with I20/I21/I33.

### 3.2 The "4" in 32π = 8π × 4 has four derivable origins (plus the fitted one); two of them are conventions
| where | origin of the extra factor | verified in |
|---|---|---|
| κ² = 32π, Isaacson 1/(32π), Bondi | ACT: EH's ½, the ¼ from expanding √−g R to second order (A0 = 1, c01 A), the canonical ½, the virial 2 | c01 A, B |
| free fall 3π/32 | ANG: (π/2)² from the cycloid angle; the 8π is Gauss/Friedmann; net π-count is +1 in the numerator | c02 D2 |
| BH area, T_H, first law, ρ̄, Hawking power | HOR: r_s = 2M and κ = 1/(4M), i.e. (r_s κ)² = ¼ | c01 E, c02 D4 |
| GB 32π² | TOP: (4π)ⁿ n! with n = 2; with the 2-form norm the constant is 8π² (factor 4 = norm convention, checked on S⁴ and S²×S²) | c03 T1 |
| instanton 32π² | 2π² · 16; 32π² = 8π² × 2 × 2 (trace normalisation ½, F∧F = ½ F F̃) | c03 T2 |
| the puzzle | FIT: 1/κ² with κ = ½ (fitted); on the horizon reading it is the HOR entry | record; p04 |

- Conventions inflate the literal count: κ² = 32π (tensor-canonical) versus 16π (per polarisation) versus 8π (another convention) all describe the same physics; the 2 between 32π and 16π is e_ij e_ij = 2 (c01 B).
  The GB constant is 32π² with tensor norms and 8π² with 2-form norms (c03 T1).
- Every "4" is the square of a linear 2 because it multiplies a quadratic quantity (h², t², r², a₀²). The linear 2 comes from different places: polarisation/EH normalisation, a quarter-cycle (π/2), the Schwarzschild escape factor r_s = 2GM,
  and, for the puzzle, the fitted κ = ½. (Interpretation, not a script result.)
- Tag incidence (c04 A2): across {I01, I02, I04, I14} the only common tag is Einstein's 8πG coupling itself; ACT is shared by I01/I02/I04 (one cause: the quadratic EH action, I39) but not by free fall; HOR is shared only by the black-hole-geometry rows I07–I13.
- Literal-32 set = {I01, I02, I04, I20, I21, I33, I36, I37}: apart from the puzzle, every member is a topological normalisation or a field normalisation (c04 A1). The frequency of 32π^k is over-represented by construction (I searched for it); it measures nothing.

### 3.3 π-counting
- Sources of π in the census: (i) Einstein's 8π (a local dressing of the source: κ², Isaacson, ADM, Komar, Friedmann); (ii) sphere volumes/solid angles (global integrals: GB, instanton, Jeans 4π, area 4πr²);
  (iii) angles and periods (π/2 in free fall, 2π thermal, ζ(4) in Stefan–Boltzmann).
- A solid-angle integral *cancels* the 1/(32π): Peters' 32/5 and 64/5 are π-free because (1/32π)·4·(8π/5) = 1/5 (c01 C). So the 32π of the action does not survive into radiative observables.
- Isaacson in Einstein form is π-free: 8πG t_μν = ¼⟨∂h_ij ∂h_ij⟩, i.e. Λ = ¼⟨ḣ_ij ḣ_ij⟩. It cannot supply the puzzle's π; the π would have to hide in the strain amplitude (H_GW below).
- Rate² versus Gρ (c04 A3): Friedmann (8π/3), free fall (32/(3π)), Jeans (4π), uniform-ball oscillation (4π/3) all carry π^{±1}. **The puzzle's a₀² = Gρ/4 carries π⁰.** The π-free relations among G, M, r, κ are exactly the Schwarzschild ones (r_s = 2GM, κ = 1/(2r_s), GM/r_s² = 1/(2r_s): the 4π of Gauss cancels the 4π of the sphere); the puzzle is r_s = R* with R* = 1/√(Gρ_Λ),
  the π-free dimensional-analysis length. A rate built from a *ball, a wave or a cycloid* of density ρ instead picks up π from the Poisson/Gauss volume integral or the angle. So the only census rows with the puzzle's π-structure are the horizon rows (HOR), the object p06 excludes.
  Relative to Friedmann's rate the puzzle's extra factor is 1/Z² = 3/(32π): all the π sits in Friedmann's 8π; the 4 is the only new content.

### 3.4 Does any instance couple an acceleration scale to Λ or ρ?
| relation | coefficient of √(Gρ) | note |
|---|---|---|
| Friedmann rate H | 2.894 (= √(8π/3)) | exact (I15) |
| free-fall rate 1/t_ff | 1.843 | exact (I14) |
| uniform-ball oscillation ω₀ | 2.047 | exact |
| Jeans k_J c_s | 3.545 | exact (I16) |
| **puzzle a₀** | **0.500** | fitted |
- Every classical dynamical rate of a self-gravitating density ρ is 3.7 to 7.1 times faster than a₀ (c04 A4). a₀ is not a dynamical rate of the vacuum; this is the README's "sub-Hubble" statement seen from the census, not a new result.
- Exact acceleration↔Λ relations that exist: the de Sitter surface gravity κ_dS = H = √(Λ/3), Nariai (AΛ = 4π), and the Schwinger acceleration a = eE/m (ρ = E²/2, but e/m is a free coupling ratio; cf. p07). None gives ½√(Gρ).
- Unruh/entropic MOND derivations (opened): astro-ph/9805346 eq. 9 gives â₀ = 2H_Λ; 1104.2022 eq. 9 gives A₀ = 2H; 1704.00780 eq. 32 gives a² = 2a_N a_Λ (a_Λ = √3 H); 1005.3537 eq. 5 has F = m a²/(2H). All are π-free and of size 2–3.5 H_Λ.
  The coefficients that match the data are H/(2π) (0801.3133: "2πa₀ ≈ cH₀", an observed coincidence), H/6 (1611.02269 eq. 1.7: (d−3)/((d−2)(d−1)) at d = 4, a separate derivation) and 1/Z = 0.173 (framework).
  So the Unruh-type derivations over-shoot by 4π = 12.6, 12 and 2Z = 11.6 respectively (c04 A6). Restating the puzzle as "Z = ½ × (Unruh overshoot 2Z)" adds nothing. (In astro-ph/9805346 the text extraction printed (Λ/3)^{1/3} once; eq. 6, 7, 9 and the abstract read a square root, which I used.)

### 3.5 Hypothesis tests: could a census cause be the cause of the puzzle's 32π?
| hypothesis | result |
|---|---|
| H_GW: the puzzle's 32π is Isaacson's 1/(32πG) (vacuum energy as a GW-like condensate) | ρ_Λ = ⟨ḣ_ij ḣ_ij⟩/(32πG) forces ω²⟨h_ij h_ij⟩ = 128π a₀²: h₊ ≈ 14 at ω = a₀ (non-perturbative), or ω ≥ 200 a₀ for h² ≤ 0.01. A second scale (frequency) and a free amplitude enter, and the π lands in the amplitude. Fails. (At ω = H_Λ it needs ⟨h_ij h_ij⟩ = 12 exactly = 3 × 4, outside Isaacson's ω ≫ H domain; illustrative only.) |
| H_FF: free fall | a₀ t_ff = ½√(3π/32) = 0.271; wrong π-power (π⁻¹ in rate²) and no ½. The identity Z√(Gρ)t_ff = π is a tautology (Z = 2√(8π/3), t_ff = (π/2)/√(8πGρ/3)); flagged as such. Fails. |
| H_BH: horizon with κ = a₀ (r_s κ = ½) | the only census cause that shares the puzzle's π-structure and 4; but M_s/M_Nariai = 3√3 Z/4 = 7.52 > 1, so SdS with that κ has no horizon (p06, recomputed); realisable only if Z ≤ 2. Excluded as a realised object. |
| H_TOP: Gauss–Bonnet/instanton | scale-free (same at every L and ρ, c03); cannot fix a₀/H. Explains the unit, not the size. |
| H_ħ: Hawking/Schwinger/loops/anomalies | the puzzle carries no ħ (README §4 of the parent notes); [bookkeeping check]. Excluded. |
| H_common: one cause behind all the gravitational 32π's | no: ACT (I01, I02, I04, I39), ANG (I14), HOR (I07–I13), TOP/NRM (I20, I21) are different, each derived. The only shared ingredient is 8πG itself. |

### 3.6 Small sharp facts (elementary; I did not search for prior statements)
- **Aκ² ≤ π over Kerr–Newman, equality only for Schwarzschild** (proof: A κ² = π(r₊ − r₋)²/(r₊² + a²) and r₋ ≤ r₊; 200 000 random holes give max 0.99847 π; control: the reverse bound is rejected). So the puzzle's A = π/a₀² is the *maximal* horizon area for surface gravity a₀ in that family.
- The de Sitter horizon radius L is exactly the Schwarzschild radius of a ball of density ρ_Λ (ρ̄(r_s = L) = 3/(8πL²) = ρ_Λ). The puzzle's horizon has r_s = √(8π/3) L, so ρ_Λ = (8π/3) ρ̄(r_s): the Friedmann 8π/3 again (c01 F). This is p06's A_s = (8π/3)A_dS, seen through the mean density (I11).
- 32π literally appears as 4π × 2³ in the volume of the Schwarzschild ball (4π/3)(2M)³ = 32πM³/3 and hence in ρ̄ = 3/(32πM²). Another instance of the horizon origin of the "8" (HOR), nothing more.

## 4. What is NOT established
- The table is selection-biased (I searched for 32π); the frequency of 32π^k is not a measurement and there is no false-positive rate. The census is not exhaustive (string/brane, LQG, higher-dimensional and Kerr–Newman–dS normalisations were not surveyed).
- The origin tags are interpretations supported by the derivations; a coefficient has many numerical factorisations. What is verified exactly is the product identity and the derivations behind each label.
- Several attributions are from memory (Section 1, last paragraph); the numbers were re-derived by script. Wikipedia was used only as a secondary check.
- I read the coefficients in the MOND-literature papers; I did not re-derive their internal steps.
- H_GW numbers are illustrative (Isaacson's average needs ω ≫ H). H_ħ is a classification statement, not a derivation.
- Nothing here shows κ = ½ is anything but fitted; nothing here derives 32π; "no common cause among these instances" does not exclude an undiscovered principle.

## 5. Verdict: NOTHING NEW (clean negative census)
The 32π-type factors in physics and mathematics are unrelated in origin: topological normalisations ((4π)ⁿ n!, Vol(S³) × 16), field/action normalisations (κ², Isaacson; convention-laden by exactly e_ij e_ij = 2), an angle integral (free fall), black-hole geometry (r_s = 2M), and accident (Hawking 15360π = 32π × 480; Peters 32/5 = 2⁵/5).
No common cause ties them to the puzzle: the only instances sharing its π-structure are the horizon ones, which p06 rules out as a realised object; the action-normalisation cluster is π-free in Einstein form and would need a second scale; the topological ones are scale-free.
What would change this: a classical (ħ-free) relation that links an acceleration to Gρ with a π-free coefficient and is *not* a point-mass/horizon relation, or a derivation of the horizon's r_s κ = ½ from a dynamical principle inside the Λ-universe. κ = ½ stays FITTED.
