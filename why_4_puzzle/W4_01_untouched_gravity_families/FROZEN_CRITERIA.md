# W4-01: do the modified-gravity families the κ register never touched fix the 4? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-01 script exists.** Append-only after this commit. Rules followed:
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md` (§1–§10).

## Question

The 4 in G ρ_DE = 4 a₀²/c² is κ = ½ in a₀ = κ c √(G ρ_DE). **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095,
κ_crit = 0.345 ± 0.078). The CFG894 register (602 rows, K001–K602) has **no row** for seven standard gravity families:
DGP brane-induced gravity, Kaluza–Klein compactification, dRGT massive gravity / Hassan–Rosen bigravity, mimetic gravity,
Einstein–Cartan (spin–torsion), teleparallel f(T), and Hořava–Lifshitz. (Searched 2026-10-20 in the register CSV for DGP,
Kaluza, compactif, dRGT, Hassan–Rosen, massive gravity, bigravity, mimetic, torsion, Einstein–Cartan, teleparallel, Hořava:
0 rows each.) Each family carries its own relation between its vacuum energy and its own scales. **Does any of them fix κ
with no free continuous constant, ħ-free, and, in particular, give exactly ½?**

Why these are worth one screen: DGP and KK have **two gravitational constants**. CFG891 found that π can cancel only between
sectors, and DGP's crossover r_c = G₅/(2G₄) is π-free because both Planck masses carry the same 8π. That is the one structural
feature of the "π-free coupling" CFG891/CFG911 say an exact ½ needs. The screen checks whether the dark energy then reaches
the a₀ scale without Einstein's 8π returning.

## Families, starting equations and declared readings (fixed list; nothing added after the run)

Units c = 1 inside the script; c is restored dimensionally. G ≡ G₄. ρ ≡ ρ_DE (the family's own dark energy). κ² ≡ a²/(G ρ).

**F1 DGP** (action S = (1/16πG₅)∫d⁵x√−g⁽⁵⁾R⁽⁵⁾ + (1/16πG₄)∫d⁴x√−g R + S_m; crossover r_c = κ₅²/(2κ₄²) = G₅/(2G₄);
brane Friedmann H² − εH/r_c = 8πGρ_m/3).
- Branch S (self-accelerating, ε = +1, no brane Λ): own vacuum H_∞ = 1/r_c, ρ_DE ≡ 3H_∞²/(8πG).
- Branch N (normal, ε = −1, brane Λ supplies ρ_DE): ρ_DE free.
- Readings for a₀: (A1) crossover acceleration c²/r_c; (A2) the π-free 5D product G₅ρ_DE (G₅ × a 4D density is an
  acceleration); (A2N) the same with the 5D *force-law* constant G₅ᴺ = 4G₅/(3π) (Φ = −G₅ᴺM/r²; from ∇²Φ = (16π/3)G₅ρ).
- Hand expectation (disclosed): S-branch κ² ∈ {8π/3, 3/(2π), 8/(3π³)} → κ {2.894, 0.691, 0.293}: MENU, all π-odd;
  N branch TRADE (r_c and ρ independent; also a₀ ∝ ρ, breaking the LOCK d ln a₀ = ½ d ln ρ).

**F2 Kaluza–Klein on a circle** (G₄ = G₅/(2πR); radius R unstabilised unless stated).
- Readings: (B1) G₅ρ_DE; (B2) G₅ᴺρ_DE; (B3) compactification acceleration c²/R.
- Radius: (R0) free; (R1) tied to the 4D vacuum, R = c/H_Λ (an H-type identification); (R2) Casimir-stabilised (ħ enters).
  R = c/√(Gρ) is NOT a reading: it is the forbidden J = 1 premise (X7).
- Hand expectation: R0 TRADE; R1 κ² ∈ {3π/2, 8/(3π), 8π/3} → {2.171, 0.921, 2.894}, π-odd; R2 ħ-bearing.

**F3 dRGT massive gravity / Hassan–Rosen bigravity** (self-accelerating branch: Λ_eff = m² X(α₃, α₄) [dRGT] or
m² X(β_n, M_f/M_g) [HR], X algebraic in its dimensionless parameters; exact X not reproduced, nothing downloaded).
- Reading: (C1) the graviton's Compton acceleration c² m (m as an inverse length, ħ-free).
- Hand expectation: κ² = 8π/X → TRADE in the free parameters; at any algebraic parameter values κ² is π-odd, so never ½.

**F4 mimetic gravity** (g_μν = (g̃^{αβ}∂_αφ∂_βφ) g̃_μν, constraint g^{μν}∂_μφ∂_νφ = 1; Λ an integration constant or from a
free V(φ)).
- Reading: (D1) none intrinsic: the constraint is scale-free.
- Hand expectation: TRADE (Λ is initial data or V's free scale).

**F5 Einstein–Cartan** (spin–torsion contact term: ρ_eff = ρ − (2πG/c⁴)s² with spin density s = ħn/2; standard Hehl form,
quoted from memory, PROVISIONAL).
- Torsion is algebraic (non-propagating), so the only scale is the spin energy |ε_s| = (π/2)Għ²n² (c = 1).
- Reading (E1a): a² = G|ε_s| with an independent ρ_DE. Hand expectation: HBAR (κ² ∝ ħ²n²/ρ_DE, n free); EXCLUDED by the
  ħ wall.
- Reading (E1b): a² = G|ε_s| with ρ_DE ≡ |ε_s| (spin energy as the dark energy). Hand expectation: κ² = 1 BY CONSTRUCTION
  (the X2 "energy density matched with a chosen convention" slot), and the sign is wrong (the spin term is negative). Flagged
  IDENTITY, never scored.

**F6 teleparallel f(T)** (f = T + α(−T)ⁿ, T = −6H²; Friedmann 12H²f_T + f = 16πGρ; vacuum de Sitter from the correction).
- Reading: (F1) acceleration of the f(T) scale, a² = |T_*| with α|T_*|^{n−1} = 1.
- Hand expectation: κ² = 16π (2n−1)^{−1/(1−n)}: TRADE in n; π-odd at every rational n.

**F7 Hořava–Lifshitz** (projectable or non-projectable; detailed balance gives Λ < 0 and needs a soft-breaking parameter).
- Reading: (G1) none beyond Λ itself.
- Hand expectation: TRADE.

## Inputs (provenance)

Symbols only: G, G₅, R, r_c, m, α, n, ρ, H, ħ. Pure numbers forced by each family's action (8π, 16π, 2πR, 4/(3π)).
No a₀ value, no measured κ, no Z, no Ω_Λ upstream of any κ (rules §2). Ω_Λ = 0.685 (GF1 register) converts finished κ_Λ to
κ_crit = κ_Λ √Ω_Λ at the very end, report only.

## Footing

Declared: **ρ_DE (canonical)**, the family's own dark energy. ρ_crit is reported only as κ√Ω_Λ; the footings are never pooled.

## Option spaces (equal weight within a family) and π / ħ declarations

- F1 S: Ω = {A1, A2, A2N}; all use ρ_DE through the brane Friedmann equation (8πG), so all are **π-odd**: exact ½ impossible
  (CFG263/L4). F1 N: class `free`.
- F2: R0 `free`; R1 Ω = {B1, B2, B3}, π-odd; R2 ħ-bearing.
- F3: `free` (κ² = 8π/X); π-odd at algebraic X.
- F4, F7: `free`. F5: E1a ħ-bearing, E1b identity (not scored). F6: `free` in n, π-odd at rational n.
- ħ enters only F2-R2 and F5-E1a; it does not cancel in either (declared now). In F5-E1b it cancels only because the density is matched to itself.

## Checks (all printed in the .out)

- **I1** grep the script's compute section for the §2 forbidden constants; any hit fails.
- **I2** κ² symbolic for every reading; print its free symbols. A free continuous constant ⇒ TRADE.
- **I3** dimensions: κ² must be dimensionless under the declared (M, L, T) assignment (c = 1 bookkeeping, ħ carried as M L).
- **I4** rename: the law's κ is set to 0.4 in code; every route's output must not move (they never read it).
- **I5** Friedmann use flagged: every S-branch / R1 value uses the family's own Friedmann relation; none is scored as matching Z.
- **I6** footing ρ_DE only; ρ_crit numbers labelled report-only.
- **I7** ħ power of κ² printed for every reading.
- **I8** π-weight of κ² printed for every determinate reading and compared with the class declared above.
- **K1** DGP: the S-branch Friedmann equation H² − H/r_c = 8πGρ_m/3 has the vacuum root H = 1/r_c (sympy solve).
- **K2** D = 5 force law: ∇²Φ = (16π/3)G₅ρ with Φ = −G₅ᴺM/r² gives G₅ᴺ = 4G₅/(3π) (4 spatial dimensions, Ω₃ = 2π²).
- **K3** f(T): f = T reproduces 6H² = 16πGρ; the vacuum root of the α-corrected equation is (6H²)^{1−n} = α(2n−1).
- **K4** each hand expectation above equals the script's symbolic value (normal run must PASS).

## Outcome classes (per reading, then per family; CFG894 §7)

EXACT CANDIDATE (determinate, κ² = 1/4 exactly, every check passes) / CONSISTENT (determinate, inside W_data) / MISS /
MENU (a family's admissible readings disagree by more than the window) / TRADE / HBAR / CLOSURE / VOID.
W_data (grading only): ρ_DE [0.227, 0.607]; ρ_crit [0.189, 0.501] (report).

**Lane verdict (frozen):**
- **CANDIDATE FOUND:** at least one family gives an EXACT CANDIDATE. It then needs an independent audit lane and the §8
  second-prediction significance before anything is said.
- **CONSISTENT ONLY:** no exact candidate, at least one determinate non-menu value inside W_data.
- **NO FAMILY SELECTS κ:** every family is MENU, TRADE, HBAR, MISS or CLOSURE.

Hand expectation for the lane: **NO FAMILY SELECTS κ** (F1 MENU with a spurious 0.293 landing; F2, F3, F4, F6, F7 TRADE;
F5 HBAR, with E1b an identity).

## Mutation control (separate run, `W4_01_MUTATE=1`, writes `_MUTATE` outputs, exits 1 when it bites)

- **M1** Einstein coupling 8πG → 4πG in every family's 4D vacuum relation. Expected: F1-S κ² 8π/3 → 4π/3, 3/(2π) → 3/π,
  8/(3π³) → 16/(3π³); F2-R1 values move likewise; π-weights stay odd. K4 must FAIL for these readings.
- **M2** KK bulk dimension 5 → 6 (torus, G₄ = G₆/(4π²R²), reading G₆ρ/R). Expected: F2-R1 B1 κ² 3π/2 → 6π³ (M2 alone;
  F2 is scored under M2 alone, and its M1-only values are printed as a report). K4 must FAIL.
- Under MUTATE, I1–I3 and K1–K3 must still PASS (the controls change physics, not bookkeeping).

## Second predictions (rules S4; stated, not scored here)

- F1 S: a₀ = c²/r_c is constant while the self-acceleration's ρ_DE,eff = 3H/(8πG r_c) drifts with H(z): a₀ FLAT while dark
  energy evolves, which is not the framework's tracking law a₀ ∝ √ρ_DE(z). Context, recalled (provisional): the self-accelerating
  branch has a ghost and is disfavoured by expansion data.
- F2: a radion drift R(z) moves G₄ and a₀ together (a varying-G signature).
- F3: a graviton mass m ~ H₀ (GW dispersion / fifth-force bounds).
- F6: w_eff(z) of the f(T) correction.

## Honesty rules

No knob scans: the readings above are the only variants. Identity-class results are flagged and never scored. κ = ½ stays
FITTED in all writing. Not theory closed. Nothing downloaded; literature forms quoted from memory are labelled PROVISIONAL.

## Files to be produced

`w4_01.py`, `w4_01.out`, `w4_01_results.json`, `w4_01_MUTATE.out`, `w4_01_results_MUTATE.json`, `README.md` (verdict); one
row per family appended to the CFG894 register (K603…), then `kappa_campaign_lee.py` rerun.
