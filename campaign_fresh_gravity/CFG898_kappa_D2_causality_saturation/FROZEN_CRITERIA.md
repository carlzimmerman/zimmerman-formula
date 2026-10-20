# CFG898 FROZEN CRITERIA: κ door D2, saturating the drift-causality bound

This file was written before any script of this lane existed, and it is committed alone. The lane is attempt D2 of the κ
campaign, under `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md` (the rules) and `KAPPA_DOORS.md`
(door D2).

## 0. Standing facts (rules §0) and disclosure

- **κ = ½ is FITTED.** CFG493 measured κ_Λ = 0.417 ± 0.095 (ρ_DE footing) and κ_crit = 0.345 ± 0.078 (ρ_crit footing).
- The footings, 9.3603e-11 and 1.1312e-10 m/s², are κ = ½ statements and are never pooled. Z ≡ κ.
- No de Sitter–Unruh argument is used. GF2's "κ derived" is the SIS ratio (AUDIT_GF2), not the law's κ.
- This lane does not claim "theory closed" and runs no knob scan: the option space below is a declared, finite list.

**What I read before freezing:**
- the rules and the doors file (CFG894);
- CFG893's README, FROZEN_CRITERIA and results JSON (R12 table);
- CFG638's README;
- CFG542's README and ACTION.md;
- CFG541's EQUATIONS.md, §1 and §6 (the damped-ψ completion);
- the first lines of CFG639's README.

**What I estimated by hand before freezing.** These are expectations, not results; the script decides.
- c_ν = 0.64761 (ν_mono, at y = 2.540) and 1 (simple). Both come from CFG893.
- Saturating the ceiling at the declared loci gives the 18 values in §4, from 2.89 to 10.95, so I expect every one to MISS.
- The Israel–Stewart (IS) closure itself sets no bound on α. Its characteristic speeds u, u ± √3σ (CFG638 K5) do not contain α,
  and the IS shear front speed² η/(ρτ_π) = p/ρ, because α cancels between η = pτ/2α and τ_π = τ/2α.
- The record's "α ≲ 1" comes from the damped-ψ completion (CFG541 §6; CFG542 K9): Γτ_ψ < 1, i.e. αβq < 1. So α_max = 1/(βq),
  which is conditional on β.
- With the field actually present at a ρ_DE-defined locus, rather than its global maximum c_ν a₀, the deep-regime drift ceiling is
  α V_f/c at L1 and L2b, and α V_f/(√3 c) at L2, where V_f⁴ = G M_b a₀. ρ_DE and κ both cancel. Saturation would then need
  V_f = c/α or √3 c/α, and the κ it implies scales as M_b⁻¹ (about 1e11 for a Milky-Way mass).
- The phantom locus L3 (y = 2.540) gives a₀ = 16π² c⁴ h(y_m)²/(α⁴ c_ν⁴ G M_b). That expression is κ-free and depends on mass.
- Inverse problem: κ = ½ with the simple kernel and α = 1 would need the luminal locus at ρ* = ρ_DE/(16π). That is the target
  (G ρ_Λ = 4a₀²/c²) restated, not a locus.

## 1. Mechanism and assumptions (rules §1.1)

**Record equations, each with its file:**
- E1, the drift: v_s = −α τ 1_B 1_C 1[d > 0] ∇ψ, with τ = (4πG ρ_m,loc)^(−1/2). Sources: CFG541 E4 and CFG639.
- E2, the field bound: |∇ψ| ≤ g_ph = a₀ F(y), where F(y) = y(ν(y) − 1), y = g_N/a₀, and F ≤ c_ν. This holds for the round rule
  with the one-sided deficit in spherical symmetry (CFG893 K6, R12). It inherits CFG893's caveat: with the two-sided deficit,
  |∇ψ| is not bounded by c_ν a₀.
- E3, the law: a₀ = κ c √(G ρ_DE) (CFG541 §1, A2).
- E4, the ceiling (CFG893 R12): |v_s|/c ≤ α c_ν κ √(ρ_DE/(4π ρ_m,loc)). It does not depend on c or on galaxy mass.
- E5, the IS closure (CFG638): ∂ₜΠ + … = −(2α/τ)(Π − ρσ_J²), with τ_π = τ/2α and η = pτ/2α.
- E6, the causal completion (CFG541 §6): c⁻²∂ₜ²ψ + (c²τ_ψ)⁻¹∂ₜψ − ∇²ψ = −4πG d, with τ_ψ = βτ and Γ = α q/τ, q = ρ_c/ρ_m.
  Stability requires Γτ_ψ < 1, i.e. αβq < 1 (CFG542 K9).
- E7, the kinetic operator (CFG638, CFG544 FIX-2): Fokker–Planck friction γ = α/τ, acting on (v − u).
- E8, the zero-gravity surface in a vacuum of equation of state w: the matter density there is ρ_m = −(1 + 3w) ρ_DE, which is
  2ρ_DE at w = −1. In D spacetime dimensions it is −[(D − 3) + (D − 1)w] ρ_DE/(D − 3). This is also the maximum turnaround
  radius, where the mean enclosed density is 2ρ_DE.

**Added hypotheses, each named:**
- **H_sat.** Marginal causality: the drift ceiling equals c at a declared locus (a posit, not something the equations imply).
- **H_α.** α is fixed by one of the following, not fitted:
  - **A.** Saturation of the causal-completion bound: α = 1/(βq) with β = 1 (CFG541's admissible convention) and q → 1 (the most
    restrictive state), so α = 1.
  - **B1.** One relaxation time, Fokker–Planck form. The drift is the overdamped response to −∇ψ under friction γ = α/τ in the
    baryon frame. The mobility is then 1/γ = τ/α, and equating it to ατ gives α = 1.
  - **B2.** One relaxation time, BGK form, with τ_c = τ_π = τ/2α (the IS relaxation time). The mobility is τ_c, and equating it to
    ατ gives α = 1/√2.
  - Without H_α, α is FREE (CFG542 K5).
- **H_locus.** The luminal locus is defined through ρ_DE alone (see §4).

## 2. Inputs and provenance (rules §1.2)

- **Symbols:** G, c and ρ_DE. ħ does not enter.
- **Pure numbers:** 4π (from Poisson), c_ν (the kernel maximum, computed), α* (from H_α), and the locus ratio ρ*/ρ_DE (from E8 or
  from matter–vacuum equality).
- **Read-only record JSON**, used for K-tests only: CFG893's c_ν, its R12 table, and f_b. f_b enters only K3's reproduction of
  1.186 and never a κ value.
- **Report-only conversions:** H₀ = 67.4 and Ω_Λ = 0.685, used to evaluate the mass-dependent numbers of the realized branch and the
  end conversion κ_crit = κ_Λ √Ω_Λ. Neither enters a verdict.
- **Forbidden inputs (rules §2) are absent from every κ value:**
  - no footing a₀, measured κ, Z, 0.1727, 5.364, Ω_m/Ω_Λ, f_ret or H₀ upstream of κ;
  - no fitted constant of the record. β = 1 is a convention, flagged as a TRADE (§7).

## 3. Footing (rules §1.3)

- **Declared: ρ_DE.** The verdict is on κ_Λ against W_data = [0.227, 0.607].
- **The ρ_crit footing is reported separately and never pooled**, in two ways:
  - (a) the same relation with ρ_DE → ρ_crit and the loci in ρ_crit units, which gives identical numbers;
  - (b) the end conversion κ_crit = κ_Λ √Ω_Λ.
  Both are compared with W_data,crit = [0.189, 0.501].

## 4. Option space Ω (rules §1.4)

The bound-saturation form, with mass and c dropping out, is κ = √(4π ρ*/ρ_DE)/(α* c_ν).

**The variants:**
- **Loci, declared now:**
  - **L1:** ρ* = ρ_DE (matter–vacuum equality).
  - **L2:** ρ* = 2ρ_DE (the zero-gravity surface, or maximum turnaround radius; the vacuum's active mass |ρ + 3p/c²|).
  - **L2b:** ρ* = 2ρ_DE/3 (the local density at the L2 surface for an r⁻² profile whose mean is 2ρ_DE; an identification variant).
- **Kernels:** ν_mono (canonical, owner decision of 09-26) and simple.
- **α\*:** A (1), B1 (1) and B2 (1/√2).

This gives 3 × 2 × 3 = 18 cells, each with weight 1/18. My hand values:

| α* | L1 ν_mono | L1 simple | L2 ν_mono | L2 simple | L2b ν_mono | L2b simple |
|---|---|---|---|---|---|---|
| 1 (A, B1) | 5.47 | 3.54 | 7.74 | 5.01 | 4.47 | 2.89 |
| 1/√2 (B2) | 7.74 | 5.01 | 10.95 | 7.09 | 6.32 | 4.09 |

**Declared outside the κ menu, each with its class decided symbolically:**
- **L1r, L2r, L2br (realized).** The same loci, but with the field actually present there, |∇ψ| ≤ g_ph(r_L) rather than c_ν a₀, for
  a point mass M_b with exact kernels. The class follows from the symbolic exponent d ln κ/d ln M_b. Numbers are given at
  M_b ∈ {1e8, …, 1e12} M_⊙.
- **L3.** ρ* = ρ_ph at y = 2.540, for a point mass.
- **Loci tied to ρ̄_m:** the cosmic mean, the present-day turnaround Δ_ta ρ̄_m, and the catchment edge. They need Ω_m/Ω_Λ (and f_ret
  for the edge), which are forbidden inputs (§2, X13), and they run with z (S8). They are VOID as selections, and only their
  symbolic form and their running with z are printed. CFG893's table already holds their numbers.

## 5. π-parity and ħ (rules §1.5)

- This is a ρ-type route, through ρ_DE and c via causal propagation. It is not an a₀-and-H route.
- κ² = 4π (ρ*/ρ_DE)/(α*² c_ν²).
  - With the simple kernel, κ² ∈ ℚ·π¹ (odd).
  - With ν_mono, c_ν is transcendental (class cont).
- So exact ½ (κ² = ¼, π⁰) is impossible in every cell: p_exact = 0 is declared in advance.
- ħ does not appear (I7).

## 6. Entry screen (rules §3)

- **S1 passes.** c enters through causal propagation (|v_s| ≤ c).
- **S2 passes.** The condition fails for a different κ: it is an equation in κ, not an identity.
- **S3 passes.** The route is stated in D dimensions. The Poisson coefficient is 8πG(D − 3)/(D − 2) (Einstein convention), and the
  loci follow E8. It is not ½ in any D.
- **S4 is expected to FAIL, and this is declared now.** Beyond κ itself, saturation fixes only:
  - the luminal density (the locus, by construction);
  - the drift speed at a given density, v/c = √(ρ*/ρ_m,loc).
  The cold-energy drift is not observed directly, so no independent measurement tests either. The lane runs as the assigned
  closure computation of door D2. **The outcome is capped below EXACT CANDIDATE** even if a cell landed in the window.
- **S5.** κ ∝ 1/α* is a monotone map. With α* fixed by H_α the route is a number; with α* = 1/(βq) it is a TRADE in β (§7).
- **S6 passes.** ρ_DE is the gravitating vacuum density, used as a locus density. The route ties a₀ to it and does not set it.
- **S7, flagged overlap.** The saturated relation is a₀ = c √(4πG ρ*)/(α* c_ν), i.e. c times a free-fall rate at a declared
  density. That is the same family as X7 (c²/2R*). The O(1) number comes from the drift law plus the locus rather than from J = 1,
  but the locus density is chosen.
- **S8.** L1, L2 and L2b read ρ_DE(z) locally, so κ is constant and a₀(z) is flat. The ρ̄_m loci fail S8.

## 7. Selection test, outcome classes and overall label (frozen)

**Requirements for a κ selection** (all must hold):
- (i) one pure number;
- (ii) independent of galaxy mass and of free density choices, meaning that every admissible cell gives the same κ, or the spread
  of κ is smaller than the width of W_data (0.380 for ρ_DE, 0.312 for ρ_crit);
- (iii) a second independent testable prediction (S4).

**Per-branch classes** (the first that applies):
- **VOID:** a forbidden input, a failed identity check, or a mutation tooth that does not bite.
- **MASS-DEPENDENT:** ∂ ln κ/∂ ln M_b ≠ 0 symbolically, or a₀ comes out κ-free and depends on mass. Such a branch is also
  **EXCLUDED** if the implied κ lies outside [0.01, 100].
- **TRADE:** κ depends on a free record constant (β), or on α left free.
- **MENU:** the admissible mass-free cells are determinate one by one but spread wider than the window.
- **EXACT CANDIDATE / CONSISTENT / MISS:** a determinate single value (spread below the window width) that is exactly ½, inside
  W_data, or outside it, respectively (rules §7).

**Overall label:**
- **κ SELECTED** only if (i), (ii) and (iii) all hold, and the class is then reported per rules §7.
- Otherwise **NOT A SELECTION**. It is reported with the campaign class of the mass-free admissible set (MENU / MISS / CONSISTENT),
  together with p_data and p_exact on each footing, the class of the α source, and the classes of the realized branches, L3 and
  the ρ̄_m branches.
- **The canonical single cell** (L2, ν_mono, α* = 1) is also reported on its own. It never upgrades the label.

## 8. Checks (the script exits 1 if any fails; normal run)

**K-tests:**
- **K1.** c_ν for ν_mono, by bounded maximisation, equals CFG893's JSON value to 1e-6 (y_m to 1e-3). The simple kernel's supremum
  is 1 (sympy limit).
- **K2.** The ceiling reproduces the structure of CFG893's R12 table: κ_H12 ∝ √Δ_loc/c_ν across its cells, as ratios, to 1e-9.
- **K3.** Routh–Hurwitz on the cubic s³ + s²/τ_ψ + c²k² s + Γc²k² gives stability ⟺ Γτ_ψ < 1 ⟺ αβq < 1 (sympy). Then
  α_max(β = 1, q = 1 − f_b) equals 1.186 (CFG542 K9) to 1e-3, with f_b read from CFG893's JSON.
- **K4.** In the 1-D IS (ρ, u, P) system, the eigenvalues of the principal-part Jacobian are {u, u ± √(3P/ρ)}, and their derivative
  with respect to α is 0. Also η/(ρτ_π) = p/ρ.
- **K5.** The Fokker–Planck/Smoluchowski stationary state does not depend on the mobility (reproduces CFG542 K5).
- **K6.** The overdamped momentum moment with friction γ in the baryon frame gives u = −∇ψ/γ. Under H_α, B1 then gives α² = 1 and B2
  gives α² = ½ (sympy).
- **K7.** Deep-regime realized loci (sympy):
  - v/c = α V_f/c at L1 and L2b, and α V_f/(√3c) at L2;
  - the saturated a₀ contains no ρ_DE.
- **K8.** With exact kernels, the realized v/c at the loci matches K7's deep form to within 5%, at M_b = 1e10 M_⊙ and fitted κ.
  This is a report-only evaluation.
- **K9.** The closed forms of the point-mass phantom density, ρ_ph = M_b (F/y − F′)/(2πr³), match sympy's derivative of
  r² g_ph to 1e-12 for both kernels. L3's saturated a₀ contains no ρ_DE.
- **K10.** The saturation relation is dimensionally consistent, and κ is dimensionless.
- **K11.** Classifier controls:
  - a₀ = ½ c √(Gρ_DE) classifies as a pure number;
  - a₀ = c⁴/(G M_b) classifies as MASS-DEPENDENT;
  - a two-value list spread wider than the window classifies as MENU;
  - a single in-window value classifies as CONSISTENT.

**Identity checks I1–I8 (rules §6):**
- **I1.** The script greps itself for the §2 constants and fails on any hit.
- **I2.** κ is computed symbolically, with G, c, ρ_DE and ħ as symbols, and its dependence on each is printed.
- **I3.** Scaling G → λG, ρ → μρ, c → νc leaves κ invariant.
- **I4.** Setting the law's κ to 0.4 does not move the selected values.
- **I5.** No Friedmann relation is used.
- **I6.** The declared footing only.
- **I7.** ħ is absent.
- **I8.** The π-weight of κ² is printed for each cell and checked against §5.

## 9. MUTATE (`CFG898_MUTATE=1`; writes `_MUTATE` outputs; exits 1 by design if every tooth bites, and 2 if any does not)

Each tooth is checked on the mass-free cells to 1e-9:
- **M1.** α* → 2α*: every κ scales by exactly 0.5.
- **M2.** ν_mono → simple: the ν_mono cells scale by c_ν.
- **M3.** The Poisson coupling 4πG → 8πG in τ: the cells scale by √2.
- **M4.** w = −1 → −0.9: L2 and L2b scale by √0.85, and L1 does not move (declared).
- **M5.** D = 4 → 5 (Einstein convention): L1 scales by √(4/3) and L2 by √(2/3).
  - L2b is not a tooth for M5. In n spatial dimensions an r⁻² profile has local/mean = (n − 2)/n, which is 1/3 at n = 3 and ½ at
    n = 4.
  - Combined with E8 and the D = 5 Poisson coefficient 16πG/3, that gives κ²(L2b) = 8π/3 in both D = 4 and D = 5, so the ratio is
    exactly 1. This is declared in advance as a coincidence of the two D factors, and the script checks it as ratio 1.

## 10. Second prediction (rules §1.8)

The candidates are the ones listed under S4 in §6: the luminal density and the drift-speed profile v/c = √(ρ*/ρ_m,loc). Neither is
independently observable today, so S4 is declared FAILED in advance. That is why the outcome can never exceed CONSISTENT.

## 11. Resources

- One process, `OMP_NUM_THREADS=1 nice -n 10`, under 1 GB, seconds to a few minutes.
- No downloads, and no repo-wide searches.
- Commits cover only this lane's directory. LEDGER.md, the THEORY_CANONICAL files and CFG894's register are not edited; the
  register row is returned to the orchestrator.
