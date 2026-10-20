# CFG905: κ door D5, a gauged carrier and the Festina Lente bound. CLOSURE

**Bottom line.** No κ comes out. κ = ½ stays FITTED. The door asked whether gauging the record's carrier U(1) and applying
the Festina Lente (FL) bound, which ties a charged particle's mass to the de Sitter rate, could fix κ if the same carrier
also set 𝒦 = G a₀. It cannot, for three computed reasons:

1. **FL is natively a bound on the vacuum energy, not on G.** From the Einstein–Maxwell–Λ product geometry (explicit metric,
   d = 4 and 5), the largest electric field on the charged-Nariai branch is E_uc² = 2V/(d − 3), with no Planck mass in it.
   In d = 4, V = 3M_P²H² gives E_uc = √6 M_P H, which reproduces the recalled √6. So FL reads m⁴ ≥ 2s²e²V. The door's
   "the 8π cancels against the reduced M_P" just restates that FL never contained G. It ties the carrier's mass and charge to
   ρ_DE, π-free. It says nothing about a₀.
2. **Applying FL (it is an inequality) bounds the carrier and leaves κ untouched.** The record's carrier action has no G and
   no a₀, and 𝒦 belongs to the separate fermion force sector with S_bridge unspecified. So ∂κ/∂m = ∂κ/∂e = 0 (BOUND,
   κ-free). At the record's benchmark m = 1 MeV the bound is slack by 6.8 × 10⁸ in mass at e = 0.303. It only binds for
   e ≥ 1.4 × 10¹⁷.
3. **Saturating FL and adding a carrier→a₀ map gives a one-parameter map.** Every acceleration that can be built from
   (m, e, ħ, c, G) is 𝒩 eⁿ (mc³/ħ)(Gm²/ħc)^w. At saturation m ∝ ħ^{3/4}, so ħ drops out only at w = ½ and e only at n = −1.
   The unique ħ-free, e-free carrier acceleration is therefore
   a_FL = √G m² c^{5/2}/(e ħ^{3/2}) = √2 s c√(Gρ_DE), the law's own unit times a number. So a₀ = 𝒩 a_FL gives
   **κ = √2 s 𝒩**. Nothing fixes 𝒩: not FL, not the carrier action, not the record (TRADE, rule S5).
   - The map's normalisation sets π. Written with G it gives κ² = 2s²𝒩² (π-even); with 4πG, 8πs²𝒩²; with 8πG (reduced
     M_P), 16πs²𝒩² (π-odd).
   - The only π-even branch is the G-normalised one, which is **premise A** ("the MOND sector couples through G, not 8πG").
     That is forbidden as a premise.

The other variants fail outright:
- **FL's own acceleration** (the saturating charge in the ultracold field) is mc³/ħ ∝ ħ^{−1/4}. It is ħ-bearing (wall 3) and
  3.6 × 10³⁰ times the law's unit.
- **The FL geometry** gives the ultracold Nariai c²/R (κ = 4√π = 7.09) and the neutral Nariai value (κ = √(8π) = 5.01). Both
  are horizon-type (X3), π-odd and misses.
- **Gauging the force sector's baryon charge q_b instead** gives a repulsive force, while the record's scalar force attracts.

Frozen outcome: **CLOSURE** (rules §7: TRADE/CLOSURE class). p_exact = 0, p_data = 0.

**The four questions the door asks:**

| | requirement | answer |
|---|---|---|
| (i) | a pure number | **No.** κ = √2 s 𝒩 with 𝒩 free; s is an O(1) convention of the "≳" |
| (ii) | independent of galaxy mass | Yes, trivially: nothing galactic enters. The route is purely cosmological |
| (iii) | not π-odd, if it is to give ½ | π-even only for the G-normalised map, which is premise A. The 4πG and 8πG normalisations are π-odd. Under the non-reduced Planck mass (M1), π returns |
| (iv) | a second independent prediction | **No.** The only by-product is the saturating carrier mass mc² = (2s²e²)^{1/4}(ħc)^{3/4}ε_Λ^{1/4} (1.47 meV at e = 0.303). It depends on the free e and concerns an unobserved field |

Standing facts:
- **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078).
- The footings 9.3603e-11 and 1.1312e-10 m/s² are never pooled. This lane declares ρ_DE: FL is a de Sitter statement, with
  V = ε_Λ = ρ_DE c². The ρ_crit reading is printed separately.
- No de Sitter–Unruh argument is used. GF2's ½ is the SIS ratio, not κ.
- **Not a dark-matter species.** The charged field is the record's own MODEL carrier (Φ, X) (FRAMEWORK_EQUATIONS §3a; MASTER
  carrier section), not a new particle, and nothing here claims it exists. Gauging its U(1), though, **adds one massless
  hidden vector** that the record does not contain (hypothesis H_g). The door cannot exist without that addition.
- Not theory closed. No knob scan: every variant and convention was declared in the frozen criteria before any script.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (9e3b6754e): recalled FL form, hypotheses H_g/H_FL/H_sat/H_map/H_dS, variants V1–V5, checks, MUTATE, outcome classes, hand estimates (including the in-window natural value, disclosed in advance) |
| `cfg905.py` | sympy, one process, about 1 s, 63 MB peak (measured) |
| `cfg905.out`, `cfg905_results.json` | normal run: 20/20 checks PASS, exit 0 |
| `cfg905_MUTATE.out`, `cfg905_results_MUTATE.json` | `CFG905_MUTATE=1`: 4/4 teeth bite, exit 1 by design |

Run from the repo root:

    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG905_kappa_D5_festina_lente/cfg905.py
    CFG905_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG905_kappa_D5_festina_lente/cfg905.py

The script reads no data file. The inputs are symbolic. Measured H₀ = 67.4 km/s/Mpc and Ω_Λ = 0.685 enter only the
report-only numbers at the end, as do the electromagnetic e = 0.303 and the proton mass. Nothing was downloaded. No other lane,
LEDGER.md, canonical file, register or sol61 file was edited.

## The bound used (recalled, flagged)

**Festina Lente**, recalled from memory and not re-read. The source is Montero, Van Riet and Venken, "Festina Lente: EFT
constraints from charged black hole evaporation in de Sitter", JHEP (2020), arXiv:1910.01648. In ħ = c = 1 units, with
M_P = (8πG)^{−1/2} the reduced Planck mass, every particle of mass m and charge q under an unbroken U(1) of coupling g in de
Sitter space with Hubble rate H obeys

  m² ≳ √6 g q M_P H.

The recalled reasoning: large charged Nariai black holes must be able to evaporate back to empty de Sitter. If charged states
are too light, Schwinger discharge (rate ∝ exp(−π m²/(gqE))) pushes them off the Nariai branch. The bound is
m² ≳ gqE_uc, with E_uc the field at the ultracold point.

Recalled caveats:
- the "≳" carries an O(1) uncertainty;
- the bound assumes an unbroken (massless) photon;
- it is a swampland conjecture, not a theorem.

K1 re-derives E_uc and reproduces the √6 and the reduced M_P. That checks the internal consistency of the recalled form, not
the conjecture itself.

**Saturation convention s** (declared before the run): m² = s·e·E_uc.
- s = 1 is the literature form (Schwinger exponent ≥ π).
- s = 1/π corresponds to an exponent ≥ 1.

## Carrier and coupling assumptions

- **Carrier (record).** ℒ_c = |∂Φ|² + |∂X|² − V_c, with V_c = m²|Φ|² + 4m²|X|² + |√Δ_c X + (g_c/√Δ_c)Φ²|² + λ_rep|Φ|⁴.
  - The U(1) acts as (Φ, X) → (e^{iθ}Φ, e^{2iθ}X), with charges 1 and 2, and gives the bound E ≥ m|Q|.
  - M = 2m√(1+u_*²).
  - The benchmark m = 1 MeV is a choice, not data.
- **H_g (gauging).** The U(1) is gauged and unbroken, with D_μΦ = (∂_μ − igA_μ)Φ, D_μX = (∂_μ − 2igA_μ)X, and e ≡ gq
  (Heaviside–Lorentz, dimensionless). K7 checks that the gauging is consistent: V_c is invariant and both covariant derivatives
  transform correctly. It adds a hidden photon.
- **H_FL** (FL, the recalled form, with s). **H_sat** (the binding state saturates). **H_dS** (FL is applied with V = ε_Λ and
  H = H_Λ).
- **H_map** (the S_bridge that MASTER leaves unspecified): the carrier sets a₀. V2 uses the unique ħ-free, e-free form; V3 uses
  FL's own acceleration; V4 uses the FL geometry.
- **Force sector (record, untouched).** D = C∇φ − P, ∇·D = q_bρ_b, g_s = −q_b∇φ, 𝒦 = q_b³/(4πC³β₃). MASTER lists the
  identities 𝒦 ≟ G_N a₀ and a₀ ≟ (c/2)√(G_N ρ_DE) as TARGETS.

## Equations (all checked in `cfg905.out`)

**Ultracold field (K1).** Take M₂ (curvature k) × S^n (radius R), d = n + 2, with a uniform electric field E (T^a_b = −(E²/2)δ
on M₂ and +(E²/2)δ on S^n) and vacuum energy V. Solve M_grav G^μ_ν = T^μ_ν.
- The explicit metric −(1 − kx²)dt² + dx²/(1 − kx²) + R²dΩ_n² was put through sympy's Christoffel and Ricci computation for
  n = 2 and 3. It agrees with the closed form G^t_t = −n(n−1)/(2R²) and G^θ_θ = (n−1)/R² − k − n(n−1)/(2R²).
- At the ultracold point (k = 0):

  E_uc² = 2V/(d − 3),  1/R_uc² = 2V/((d − 3)² M_grav)  (d = 4: E_uc = √6 M_P H, 1/R_uc² = 6H²).

- Neutral Nariai (E = 0): 1/R² = 2V/(n(n−1)M_grav), which is 3H² at d = 4.

**FL in vacuum form (K3, K4).** m⁴ = s²e²E_uc² = 2s²e²V/(d − 3). In SI at d = 4:

  (mc²)⁴ ≥ 2 s² e² (ħc)³ ε_Λ,  ε_Λ = ρ_DE c².

- This is π-free and M_P-free.
- With the reduced M_P and H² = V/(3M_P²) it is identical to m² ≥ √6 s e M_P H.

**Dimensional theorem (K5).**
- Accelerations from (m, e, ħ, c, G): a = 𝒩 eⁿ m^{2w+1} ħ^{−1−w} c^{3−w} G^w.
- At saturation, ħ appears to the power w/2 − 1/4 and e to the power n + w + ½. Both vanish only at (w, n) = (½, −1).
- The result:

  a_FL ≡ √G m² c^{5/2}/(e ħ^{3/2}) = √2 s c √(G ρ_DE)  (exact at saturation).

**V2 (saturate + map).** a₀ = 𝒩 √(G_x) m² c^{5/2}/(e ħ^{3/2}):

| G_x | κ | κ² | π-weight |
|---|---|---|---|
| G | √2 s 𝒩 | 2s²𝒩² | 0 (premise A) |
| 4πG | 2√(2π) s 𝒩 | 8πs²𝒩² | 1 |
| 8πG | 4√π s 𝒩 | 16πs²𝒩² | 1 |

- **General d** (G-normalised): κ² = 2s²𝒩²/(d − 3).
- **κ = ½** needs 𝒩 = √2/4 (s = 1) or √2π/4 (s = 1/π). That is a posit.
- **Natural values (𝒩 = 1), report only.** They are not a trial and can never be CONSISTENT or EXACT:

| s | G_x | κ | κ² | in W_data (ρ_DE) |
|---|---|---|---|---|
| 1 | G | √2 = 1.414 | 2 | no |
| 1 | 4πG | 2√(2π) = 5.013 | 8π | no |
| 1 | 8πG | 4√π = 7.090 | 16π | no |
| 1/π | G | √2/π = 0.4502 | 2/π² | **yes** (disclosed in the frozen criteria before the run) |
| 1/π | 4πG | 2√2/√π = 1.596 | 8/π | no |
| 1/π | 8πG | 4/√π = 2.257 | 16/π | no |

  The one in-window entry, √2/π, results from three unforced choices: 𝒩 = 1, s = 1/π and the premise-A normalisation. It is
  not ½ (κ² = 2/π²). It is exactly the kind of landing the look-elsewhere rule discounts. It lies close to the MNRAS R1 figure
  0.450 ± 0.073 by coincidence. **Do not cite it as a match.**

**V3 (FL's own acceleration).** At saturation, eE_uc/m = m (natural units), so
a = mc³/ħ = 2^{1/4} c^{9/4} e^{1/2} ρ_DE^{1/4}/ħ^{1/4} (with s = 1).
- Its ħ-dependence is d ln a/d ln ħ = −1/4, so it violates wall 3.
- κ_V3 = 2^{1/4} c^{5/4} e^{1/2}/(√G ħ^{1/4} ρ_DE^{1/4}).

**V4 (excluded class X3, report only).** With Einstein coupling η (M_P² = 1/(ηG)):
- ultracold c²/R: κ² = 2η;
- neutral Nariai: κ² = η;
- a₀ = cH_Λ: κ² = η/3.

At η = 8π these are 16π, 8π and 8π/3 (κ = 7.090, 5.013, 2.894). All are π-odd and all miss.

**V5 (gauge q_b instead).** For a point mass, the record's force (P = 0) is g_r = −q_b²M_b/(4πC r²) (attractive). A Gauss-law
vector gives g_r = +q_b²M_b/(4π r²) between like charges (repulsive). NO SOLUTION (sign).

**V1 (apply, no bridge).** κ_record = q_b³/(4πC³β₃ G^{3/2} c √ρ_DE). Its derivatives with respect to m, e and s vanish. If a
map a₀ = 𝒩 a_FL existed, applying FL without saturating it would give only κ ≥ √2 s 𝒩.

## Report-only numbers (H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685)

| quantity | value |
|---|---|
| ε_Λ^{1/4} | 2.240 meV |
| law unit c√(Gρ_DE) (κ-free) | 1.872e-10 m/s² |
| m_sat (e = 0.303; s = 1 / s = 1/π) | 1.467 meV / 0.827 meV |
| m_sat (e = 1, s = 1) | 2.664 meV |
| e needed to saturate at the record benchmark m = 1 MeV | 1.41e17 (non-perturbative) |
| benchmark mass slack at e = 0.303 | 6.8e8 |
| messenger S (10 MeV, photon): mass slack | 6.8e9 |
| proton under a gauged baryon charge: g_max | 1.24e23 |
| V3 acceleration (e = 0.303) / law unit | 6.68e20 m/s² / 3.6e30 |
| a_FL at the benchmark (1 MeV, e = 0.303) / law unit | 6.6e17 (FL slack, as expected away from saturation) |
| Coulomb/gravity between two saturating carriers (e = 0.303) | 5.1e59 |
| ρ_crit reading: m_sat (e = 0.303) | 1.612 meV |

**Side result on H_g (report only; not a κ statement).**
- A net-charged gauged carrier halo binds only if e ≤ m/(√2 M_P). If Φ satisfies the electric weak-gravity bound (recalled:
  m ≤ √2 e M_P), the two inequalities are opposite.
- At FL saturation the dark Coulomb force exceeds gravity by 5 × 10⁵⁹.
- So a gauged carrier would have to form charge-neutral (Φ + Φ̄) halos, which is a dark plasma. That is a further cost of H_g.

## Checks (all PASS in the normal run; 20/20)

- **I1:** no forbidden constant appears outside the quoted standing-fact line.
- **K1:** the product geometry from the explicit metric (n = 2, 3) matches the closed form. It gives E_uc² = 2V/(d−3) with no
  Planck mass, reproduces the recalled √6, and gives 1/R_uc² = 6H² (neutral: 3H²).
- **K2:** at Schwinger saturation the proper acceleration is m (natural units), i.e. mc³/ħ.
- **K3:** the V form m⁴ = 2s²e²V equals the H form via Friedmann. It is π-free and M_P-free.
- **K4:** the SI dimensions check out: (mc²)⁴ against (ħc)³ε, and a_FL is an acceleration.
- **K5:** the exponent family is one-parameter. The ħ-free, e-free solution (w, n) = (½, −1) is unique, and a_FL equals
  √2 s c√(Gρ_DE).
- **K6:** Φ is the binding state. X's slack at Φ saturation is 2seE(1 + 2u_*²) > 0. Saturating X would violate Φ's bound.
- **K7:** the gauging is consistent.
- **K8:** the V2 κ² formulas and the general-d form.
- **K9:** the V4 values are π-odd. The V5 sign test.
- **K10:** in V1, κ does not depend on the carrier.
- **K11:** V3 carries ħ (power −1/4).
- **K12:** the numbers round-trip.
- **I2:** every graded κ depends on free constants: V1 on q_b, C, β₃; V2 on 𝒩, s; V3 on ħ, e.
- **I3:** under G → λG, ρ → μρ, c → νc, a₀ scales by ν√(λμ) and κ is invariant.
- **I4 (rename test):** with the law's κ set to 2/5, the required 𝒩 moves (√2/4 → √2/5 at s = 1), so V2 is a consistency
  relation in 𝒩. The natural values do not move, and none equals 0.4.
- **I5:** V2's G-normalised κ uses FL's V form and no Friedmann relation. It is not Z² = 32π/3.
- **I6:** only the declared footing is used.
- **I7:** ħ bookkeeping. a_FL goes as ħ^{−3/2} at fixed m and as ħ⁰ at saturation; V3 goes as ħ^{−1/4}. No
  Bekenstein–Hawking ¼ appears.
- **I8:** the π-weights are as declared.

## MUTATE (exit 1: every tooth bites)

- **M1, non-reduced Planck mass in FL** (the door's own mutation). The V form becomes m⁴ = 16πs²e²V, so π returns. The
  G-normalised κ² is multiplied by 8π (2s²𝒩² → 16πs²𝒩²), and its π-weight goes from 0 to 1.
- **M2, Einstein coupling 8πG → 4πG, applied consistently** (FL's M_P² is the Einstein–Hilbert coefficient). FL's V form does
  not change, and the G-normalised κ correctly does **not** move. The H-type values halve: 16π → 8π, 8π → 4π and
  8π/3 → 4π/3. So the "π cancellation" is structural (FL is a V statement), not an interlock between two independent places.
- **M3, d = 4 → 5** (the explicit S³ metric). E_uc² goes from 2V to V, and the G-normalised κ² halves.
- **M4, global instead of gauged U(1).** FL constrains only gauge charges, so the bound disappears and V2/V3 are undefined.

## Entry screen (rules §3)

- **S1 (c).** c enters through FL's relativistic content and through ε_Λ = ρ_DE c². After ħ cancels, the surviving c is only
  the law's own ρ → ε conversion. Formally PASS, flagged.
- **S2 (counterfactual).** V2 holds for every κ by choice of 𝒩 (CONDITION). V1 is κ-free.
- **S3 (dimension).** κ²_G = 2s²𝒩²/(d − 3). Disclosed: at 𝒩 = s = 1 this equals ¼ only at d = 11. That is a dimension
  choice, void under S3. **Do not cite it.**
- **S4 (second prediction).** Not reached.
- **S5 (reparametrisation).** V2 is the monotone map κ = √2 s 𝒩, a probe.
- **S6 (vacuum constant).** FL gives V ≤ m⁴/(2s²e²), an inequality. Saturation is unnamed.
- **S7 (excluded classes).** V2's natural values are horizon-type in disguise (a_FL ∝ cH_Λ). Its π-even branch is premise A.
  V4 is X3.
- **S8 (a₀(z)).** For a fixed carrier mass, saturation can hold at one epoch only, unless ρ_DE is constant. Using today's
  H(z) instead would track H(z), which is the rival law.

## Look-elsewhere

- No determinate graded value: p_exact = 0 and p_data = 0, so P_LEE is unchanged.
- The naive figure, which counts menus, would add the natural-value menu: 1/6 in W_data, 0/6 at ½.

## What this does to the door list

D5 closes. Its predicted one-page closure holds. FL does supply a new π-free coupling, but that coupling is between a charged
state's mass and the vacuum energy (m⁴ = 2e²ε_Λ), not between a₀ and ρ_DE. Turning it into κ needs exactly what CFG891
identified as missing:
- a map from the carrier to a₀ (S_bridge);
- the G-normalisation (premise A).

Neither is supplied, so κ = √2 s 𝒩 with 𝒩 free. Together with CFG891, CFG897, CFG898 and CFG900, all five κ doors in
KAPPA_DOORS.md have now run without producing κ.

## Disclosures

1. **The FL form is recalled.** Its O(1) factor is uncertain in the literature. The s ∈ {1, 1/π} variants were declared in
   the frozen criteria to cover that uncertainty.
2. **The general-d FL form is this lane's derivation**, not a literature value. It uses the d-independent Schwinger exponent
   and the product-geometry ultracold field.
3. **The record's charged messenger S** (sol61 charged_messenger) is electrically charged, so FL applies to it without H_g.
   It is slack by 6.8e9 in mass and does not set a₀.
4. The first run passed all checks. No amendments, no reruns, no edits to the frozen file.

## Proposed register line (not appended by this lane; for the orchestrator)

`K599,CFG905,QG,campaign_fresh_gravity/CFG905_kappa_D5_festina_lente,"gauged carrier U(1) + Festina Lente (recalled m^2 >~ sqrt6 g q M_P H; V form m^4 >= 2 s^2 e^2 V) with the carrier setting a0 (posited S_bridge)",,,free,0,"CLOSURE: FL is a bound on V, G-free (E_uc^2 = 2V/(d-3)); applied: BOUND on the carrier, kappa-free; saturated: unique hbar-free e-free carrier acceleration = sqrt2 s c sqrt(G rho_DE) (the law's unit) so kappa = sqrt2 s N, N free (TRADE; pi-even only for the G-normalised map = premise A; 4piG/8piG pi-odd); FL's own acceleration mc^3/hbar hbar-bearing (x3.6e30); Nariai geometry X3 7.09/5.01; gauged q_b repels; natural N=1 menu 1/6 in W (sqrt2/pi, kappa^2 = 2/pi^2, not 1/2)",<this commit>`

Use the next free K id (K599 unless another lane has taken it). κ = ½ FITTED; not theory closed.
