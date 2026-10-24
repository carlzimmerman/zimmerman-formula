# X24b_vacuum_heated_cold: FROZEN CRITERIA (committed alone, before any script or number of this lane)

κ = ½ FITTED. Footings canonical a₀ 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. The cold component ("cold energy",
Ω_c/Ω_b = 5.364) is gravitating field mass, never a particle. ε is one new dimensionless constant: it is bounded from the
forest (above) and from SPARC (below), never fitted to clusters or dwarfs, and never scanned. Never "theory closed". Never
"the data favour the framework". Theory frozen as v3s (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §7–8).

**Folder id.** A peer lane `rebuild_2026_10_22/X24_dwarf_velocity_floor` (7a79903c3f / 19d31a99d9) holds the X24 id, so this
lane is `X24b_vacuum_heated_cold`. Cite both by full folder name.

## 0. Hypothesis VHC and prior lanes

VHC: the vacuum transfers energy to the cold sector at a rate per unit VOLUME Q = ε H ρ_Λ c² (H the global Hubble rate,
ρ_Λ the framework's own vacuum density, a₀ = κ c √(G ρ_Λ)). The cold sector conserves its number (Q goes to internal
energy, not rest mass), so the specific heating is Q/ρ_c ∝ ρ_Λ/ρ_c.

Prior lanes found by grep (none is equivalent; nothing is re-run except as Step 0 below):
- CFG131 door 8 (+ CFG156 referee): interacting vacuum with Q^μ = Q u_c^μ **creating cold mass** (vacuum → rest mass).
  SCOPED NO-GO for the halo target. Its covariant identity ∂_μ ρ_Λ = −Q u_μ (Lorentz-invariant vacuum) applies to any Q
  and is reported here as an action-level constraint.
- CFG253: dark energy converted into cold mass (rest mass, background). Different channel (mass, not heat).
- why_4_puzzle W4_09 E9: Q = ξHρ_DE as a "why 4" route: TRADE, no amplitude. Not a halo test.
- CFG643: baryon → cold heat exchange Q_c = C a₀ v ρ_b: CLOSED. Different source (baryons, not vacuum).
- CFG638: the cold-energy fluid equations (Israel–Stewart moments). Supplies the kinetic closure p = ρσ²; no Q term.
- X22_cosmic_dust_window: universal late heating window, p ≥ 3, c_s,need 190.0 / 201.3 km/s. X23_late_heating_graded and
  X23_late_heated_cold: a universal fixed c_s graded on classes / KT clusters. VHC differs: c_s is not universal; it is
  derived per density history.

## 1. Derivation (sympy, PYTHONHASHSEED=0; script `x24b_derive.py`)

Assumptions (stated): isotropic kinetic pressure p = ρσ², u = (3/2)σ² (γ = 5/3; the background result is closure-free since
momenta redshift ∝ 1/a); number conservation; ρ_Λ spatially uniform; Q uses the global H; cold self-gravity is part of the
matter in the spherical collapse; the isothermal sound speed used by X22/X23 is c_s ≡ σ.

- **D1 background:** du/dt = (2/3) u dlnρ/dt + Q/ρ with ρ̄_c ∝ a⁻³ ⇒ ū = (ε c²/5)(ρ_Λ/ρ̄_c0) a³ exactly in ΛCDM (H cancels),
  c̄_s² = (2ε/15)(Ω_Λ/Ω_c) c² a³, i.e. X22's Jeans power p = 2.
- **D2 entropy:** K ≡ σ² ρ^{-2/3}, dK/dln a = (2/3) ε ρ_Λ c² ρ^{-5/3}. Entropy only grows.
- **D3 linear (non-barotropic):** with s ≡ δu/ū, s′ = (2/3)δ′ − 5(δ + s) (′ = d/dln a, exact), δp/p̄ = δ + s. Matter-era
  growing-mode attractor s = −(13/18)δ ⇒ δp = (5/18) c̄_s² δρ.
- **D4 vacuum:** ρ̇_Λ = −Q ⇒ ρ_Λ ∝ a^{−ε}, w_Λ = −1 + ε/3; thermal energy today ū ρ̄_c0 = ε ρ_Λ c²/5.
- **D5 inversion:** for an element at fixed density ρ after collapse, u grows by ε ρ_Λ c² ρ^{-1} ln(1/a_c) per unit mass ⇒ at
  fixed age, the specific heat of a dense element is below the background's.

## 2. The ε bounds

- **ε_up (forest + σ₈):** the largest ε for which X22's window rule holds (forest_class ≠ FAIL with X22's L346/L319 lines,
  and R_σ₈ ≥ 0.95), using X22's linear two-fluid ODE (copied verbatim) with the D3 non-barotropic term J·(δ_c + s) and
  c̄_s(a) from D1. Bisection in ln ε on [1e-12, 1e-2], 40 steps. Footing-independent (a₀ absent at linear order on FRW).
- **ε_low (SPARC, the brief's definition):** the smallest ε at which **late-accreted** material, an element of the ΛCDM
  spherical-collapse history that turns around at a = 1, has c_s ≥ c_s,need (X22's JSON, per footing) at X22's normalisation
  density (DTA ρ̄_c0, DTA = 5.55): c_s² = (2ε/3)(Ω_Λ/Ω_c)c² k_late DTA^{2/3}, with k ≡ ∫(ρ_c/ρ̄_c0)^{-5/3} dln a along the
  history. Closed form in ε.
- **Window** non-empty on a footing iff ε_low ≤ ε_up. Reported: ε_bg (background c̄_s(z=0) = c_s,need) and ε_low,SPARC-class
  (the SPARC small / large class histories at their own z_c, §3).
- No knob scan. If the window is non-empty, classes are evaluated at ε_low, ε_up and √(ε_low ε_up). If it is empty, they are
  evaluated at ε_low and ε_up only, labelled "outside a window" (sign diagnostic, reported).

## 3. The per-class model (derived, X23's grader unchanged)

- Spherical collapse of the class's Lagrangian shell in ΛCDM (CFG946 constants, X22's): ÿ = −(Ω_m/2)(1+δ_i)/y² + Ω_Λ y,
  τ = H₀t, growing-mode start at a_i = 1e-3; δ_i bisected so the shell collapses at a_c. Turnaround where ẏ = 0; virial
  density ρ_vir = 8 ρ_shell(a_ta). Cold density along the path ρ_c = (Ω_c/Ω_m) min(ρ_shell, ρ_vir) to a_c, then ρ_vir to a = 1.
- k_class = ∫_{a_i}^{1} (ρ_c/ρ̄_c0)^{-5/3} dln a; c_s,class² = (2ε/3)(Ω_Λ/Ω_c) c² k_class DTA^{2/3} (the class's entropy at X22's
  normalisation density, which is where X22/X23's flat-well profile is normalised). Then c_s,class / c_s,need = √(k_class / k_late)
  at ε_low.
- E_pred = X23's `e_pred` (verbatim: β = 2σ²/c_s², cap 2.9 = CAPTURED, X22's hydrostatic flat-well content, X6-d2 sourcing,
  class medians from X19's JSON, measurement radius from x and ρ_b), with c_s = c_s,class.
- **Collapse epochs z_c (PROVISIONAL, from memory; standard ΛCDM half-mass assembly and stellar-age estimates; central [lo, hi]):**
  SPARC small 1.5 [1.0, 2.5]; SPARC large 1.2 [0.8, 2.0]; Groups 0.8 [0.5, 1.2]; Clusters T1 0.6 [0.4, 0.9], T2 0.5 [0.3, 0.8],
  T3 0.4 [0.2, 0.7]; MW disc 1.2 [0.8, 2.0]; LG field 2.0 [1.0, 4.0]; MW classical 3.0 [2.0, 5.0]; MW ultra-faint 8.0 [6.0, 10.0];
  bright M31 3.0 [2.0, 5.0]; M31 others 4.0 [2.0, 8.0]; Crater II 3.0 [2.0, 5.0]; Antlia II 3.0 [2.0, 5.0]; Coma UDGs 2.0 [1.0, 3.0];
  UMa members 1.2 [0.8, 2.0]; TDGs 0.1 [0.02, 0.3]; DF2/DF4 1.0 [0.5, 1.5]. TDGs and DF2/DF4 formed late from debris: their cold
  content is whatever their own collapse history gathers (the hypothesis predicts heated, i.e. none; checked, not assumed).
- Predicted label (X23 A1 reading): EXTRA iff E_pred/s ≥ 2; NONE iff < 1; else AMBIGUOUS. A decisive class (X19 L-S label
  EXTRA or NONE on that footing) has the WRONG SIGN iff predicted EXTRA vs NONE or NONE vs EXTRA; predicted AMBIGUOUS is
  UNSETTLED. Sign ROBUST iff the predicted label is the same at z_c lo, central, hi.
- Amplitude (graded only if a class has the right sign): Z_res = (E_obs − E_pred)/s, REPRODUCED iff |Z_res| < 2.
- Cosmic background: graded by ε_up only.
- Clusters: X19's terciles T1–T3 (MGAS500 cut). KT trend (reported, not the peer lane's C* test): VHC's E_pred order across
  T1→T3 against X21's KT-tercile A_MID (canonical / alt, h 0.672) read from X21's JSON or README.

## 3a. Coordinator input received before freezing (A0; logged here because no number exists yet)

Peer lane `X24_dwarf_velocity_floor` (19d31a99d9) found the dwarf extra MASS-DRIVEN, not host-driven (hosted − field at matched
M★ +0.04 / +0.02, Z ≈ 0.2; field dwarfs show the same rise toward low M★: Leo T +0.41, Phoenix +0.40), and a velocity floor
c₀ ≈ 4.6 / 4.1 km/s fits most dwarfs. Therefore:
- **The dwarf prediction is scored per system on ALL dwarfs on disk in `X1_hosted_recount/x1_per_system.csv`** (MW ultra-faint,
  bright M31, M31 others, MW classical, LG field; hosted and field alike), with E and log M★ / log r_half from
  `X20_hosted_dwarf_requirement/x20_per_system.csv` (B_iso) where present, else X1's columns, σ and r_h from X1 (X23's convention),
  z_c by class (§3). Graded lines per footing: (i) Spearman ρ(E_pred, log M★) has the observed sign (negative) and
  |ρ_pred − ρ_obs| reported; (ii) fraction of systems with |E_obs − E_pred| < 2s. **Low-M★ dwarf sign line:** RIGHT iff
  more than half of the systems with log M★ < 6 are predicted EXTRA (E_pred/s ≥ 2); WRONG iff more than half are predicted
  NONE (E_pred/s < 1); else UNSETTLED.
- **Floor reading (reported):** c_s,class of the smallest systems at each ε vs c₀ 4.59 / 4.05 km/s, and whether the retained
  component (captured, β ≥ cap) acts like an internal floor, i.e. the implied σ_floor = √(σ_obs² − σ_iso,pred²) is roughly
  constant in the smallest systems.
- The X19 class labels for the hosted classes are kept as frozen for the class-level sign test; the per-system low-M★ line is
  the dwarf grade that enters the verdict (it replaces the three hosted classes as the "core dwarf" entry in §4).

## 4. Verdict (per footing; both must agree, else UNDECIDED; stop rule: any Step-0 failure ⇒ UNDECIDED, no graded number)

- **NO ε WINDOW** iff ε_low > ε_up. The sign class at ε_low and at ε_up (rule below) is attached as a qualifier.
- Otherwise, at each evaluation ε (central z_c): core entries = SPARC small, SPARC large, Clusters T2, T3, and the low-M★ dwarf
  line (§3a).
  - **VHC RIGHT SIGN EVERYWHERE** iff no decisive class and no core entry has the wrong sign at all evaluated ε (then amplitudes
    graded separately).
  - **WRONG SIGN (where)** iff a core entry has the wrong sign.
  - **RIGHT SIGN EXCEPT {classes}** iff only non-core decisive classes have the wrong sign.
  - UNSETTLED classes are listed; if a core entry is UNSETTLED and nothing is wrong, **UNDECIDED**.

## 5. Reported only

Energy fraction ε/5 of ρ_Λc² and w_Λ + 1 = ε/3 against DESI's w₀ + 1 scale (PROVISIONAL from memory, ~0.1–0.3); a₀ drift
∝ a^{−ε/2}; action status (CFG131 identity; GRAVITY_ACTION_AUDIT §5; a local replacement of H by θ/3 flips the sign of Q in
collapsing regions, cf. CFG944 Theorem G); runaway (a depleted region heats faster per unit mass); the Bullet Cluster (a
heated cold fluid shocks with the gas) and fossil groups (early formers retain more); variant ρ_in = fair share at the measured
ρ_b instead of ρ_vir.

## 6. Checks and MUTATE

- K0 (Step 0): c_s,need read = 190.014 / 201.315 km/s (to 0.01); X22's p = 2 and p = 3 rows (forest class, R_σ₈, T2(k5) z3/z2)
  reproduced with the copied ODE in barotropic mode to ≤ 1e-9; X23's e_pred reproduces X23's JSON E_pred for every class at
  c_s,need to ≤ 1e-12 and its hosted median.
- K1: sympy D1–D5 all hold (x24b_derive.py exits 0).
- K2: SC solver: EdS limit gives δ_lin(collapse) = 1.686 and ρ_ta/ρ̄ = 9π²/16 to ≤ 5e-3; k for the δ_i = 0 history equals a⁵/5
  closed form to ≤ 1e-6.
- K3: VHC linear ODE: ε → 0 gives T² = 1 to 1e-10; s/δ → −13/18 to ≤ 1e-3 at a = 0.1, k = 0.1 h/Mpc.
- K4: peak RSS < 1 GB.
- **MUTATE** (`X24B_MUTATE=1`, outputs `*_MUTATE.*`, exit 1): heating per unit MASS (specific heating ε H (ρ_Λ/ρ̄_c) c²,
  independent of local density). Named checks that MUST FAIL: K1 (D3 attractor and D5 inversion), K3 (attractor). The
  background (D1) is unchanged by construction.

## 7. Compute

One thread, `nice -n 15`, PYTHONHASHSEED=0, < 1 GB, minutes. No download, no `compute_queue/`. README numbers only from the
committed `.out` / `_results.json`. Commit by pathspec; no push.
