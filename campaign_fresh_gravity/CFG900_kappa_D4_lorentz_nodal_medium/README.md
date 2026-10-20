# CFG900: κ door D4, the nodal fermion medium made Lorentz-invariant (v = c) as the vacuum. CLOSURE

**Bottom line.** No κ comes out. κ = ½ stays FITTED. The door asked whether the record's fermion–polarisation medium
(sol61 `mechanism_2026_10_12`), made Lorentz-invariant with band speed v = c and with its own filled-band energy taken as the
dark energy, fixes a₀ (through 𝒦 = G a₀) and ρ_DE from one Hamiltonian. It does not, for four computed reasons:

1. **Strict Lorentz invariance removes the cubic.** A Lorentz-invariant spectrum has shells E² = ħ²c²k² + M²c⁴, so its only
   band touching is a point at k = 0. A filled Dirac sea in D spacetime dimensions then gives a vacuum term ∝ m^D (m⁴ ln m at
   D = 4), while the deep-MOND law needs |P|^{D−1}. The mismatch is one power in every D (NO LAW). The record's |P|³ exists
   because a nodal ring (codimension 2) turns the low-energy problem into an effective (2+1)-dimensional cone, and a ring at
   finite momentum k₀ picks a rest frame.
2. **The only regulator-independent part of the medium's vacuum vanishes at its cosmological state.** Keep the ring and make
   the cone Lorentz-invariant (v = v_r = c). With a Lorentz-invariant regulator (dimensional regularisation), the band energy is
   exactly β|P|³/3 with w = −1. Every P-independent piece is set by the scheme. The cosmological P of a spatial polarisation is 0
   (isotropy, minimum energy, tether, law vacuum), so the medium's own vacuum energy there is **0 for every κ** (IDENTITY).
3. **Where a regulator does tie the vacuum to β, the sign or the constant is wrong.**
   - The record's physical tube band gives E₀(0) = −βP_Λ³/3 < 0 with mode-sum w = +½ (NO SOLUTION, on both sign and equation
     of state).
   - For one species, sign E₀,tube(0) = −sign β (fermions or bosons), so a convex cubic and a positive vacuum never come
     together.
   - Pauli–Villars gives a w = −1 constant whose sign and size are set by the regulator masses (+0.83 or −6 in units of
     (A/3)M³ for two admissible sets). This is a CONDITION.
4. **Every vacuum–β link collapses to one formula, and it is a one-parameter map.** If ε₀ = σβP_x³/3, the record's dictionary
   gives κ² = 12π/(σλ_x³) with λ_x = q_b P_x/(C a₀). β, v and ħ cancel, so **v = c is not load-bearing**: c survives only in
   ρ_DE c². Today's window needs λ_x ∈ [4.68, 9.01], and ½ needs λ_x = (48π)^{1/3} = 5.32. Nothing in the Hamiltonian fixes
   λ_x, so this is a TRADE (rule S5).
   - With the record's parameters, fixing both a₀ and ρ_DE still leaves one continuous direction, so any κ is reachable.
   - Fixing λ_x by a posited locus lands in excluded classes. The transition locus (the X2 slot) gives κ = √(12π) = 6.14. The
     horizon locus (X3) gives a₀ = (2/9)cH_Λ, κ = 0.643, Z = 9/2. Both miss, and both are π-odd, so neither can be ½.

Frozen outcome: **CLOSURE** (rules §7: TRADE/CLOSURE class). p_exact = 0, p_data = 0. The door's own hand expectation, "a
TRADE (ARGON10 counts at least 6 free directions)", holds, sharpened to a closure.

Standing facts:
- **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078).
- The footings 9.3603e-11 and 1.1312e-10 m/s² are never pooled. This lane declares ρ_DE and prints ρ_crit separately as
  κ_Λ√Ω_Λ.
- No de Sitter–Unruh argument is used.
- The fermion medium is the record's own hypothetical sol61 branch, not an added dark-matter species, and nothing here claims
  that it exists.
- Not theory closed.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (32264ab5d): mechanism, hypotheses H1–H5/H_T, option space V1–V5, checks, MUTATE, outcome classes, hand estimates |
| `AMENDMENTS.md` | committed alone after the freeze and before any script (7f72af505): A1 corrects the frozen M4 factor (hand slip); A2 adds a three-regulator PV set; A3 adds ħ powers under H1r |
| `cfg900.py` | sympy + numpy, one process, about 1 s, under 100 MB |
| `cfg900.out`, `cfg900_results.json` | normal run: 20/20 checks PASS, exit 0 |
| `cfg900_MUTATE.out`, `cfg900_results_MUTATE.json` | `CFG900_MUTATE=1`: 4/4 teeth bite, exit 1 by design |

Run from the repo root:

    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG900_kappa_D4_lorentz_nodal_medium/cfg900.py
    CFG900_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG900_kappa_D4_lorentz_nodal_medium/cfg900.py

The script reads no data file. The inputs are symbolic, and measured H₀ = 67.4 km/s/Mpc and Ω_Λ = 0.685 enter only in the
report-only numbers at the end. Nothing was downloaded. No other lane, LEDGER.md, canonical file, register or argon_push file
was edited.

## Equations (SI; all checked in `cfg900.out`)

**The record's medium** (sol61 EQUATIONS.md, NODAL_RING_ORIGIN.md; MASTER fermion sector). Notation: MASTER's q_b, C are
EQUATIONS.md's α, a.
- Hamiltonian: H = q₁Γ₁ + q₂Γ₂ + h P·Γ_{3,4,5}, with q₁ = ħ²(k_⊥² − k₀²)/2m* and q₂ = ħvk_z. The spectrum is
  E_± = ±√(q₁² + q₂² + Δ²), Δ = h|P|. Radial speed at the ring: v_r = ħk₀/m*.
- Ring measure: d³k/(2π)³ = m*/(4π²ħ³v) dq₁dq₂, independent of q₁ (K2).
- Coefficients: A = N m*/(2πħ³v), β = A h³.
- Force sector:
  - D = C∇φ − P, ∇·D = q_bρ_b, D/C = β|P|P;
  - so P = B/r with B = √(q_bM_b/(4πCβ)), and V⁴ = 𝒦M_b with 𝒦 = q_b³/(4πC³β);
  - a₀ ≡ 𝒦/G (the dictionary, K6), and g_M = q_bP/C.

**V1, strict Lorentz invariance** (8×8 Clifford set, six anticommuting matrices, K1).
- Vacuum energy: ε_D(m) = N_b Γ(−D/2) m^D/(4π)^{D/2} (ħ = c = 1).
- Values: D = 3 gives N_b m³/(6π); D = 5 gives −N_b m⁵/(60π²); D = 7 gives N_b m⁷/(840π³).
- D = 4: a pole N_b m⁴/(32π²ϵ), and the MS-bar finite part −N_b m⁴[ln(m²/μ̄²) − 3/2]/(32π²) (K4).
- Exponent p = D against the needed D − 1 for D = 3–6. A codimension-c_N node gives p = c_N + 1, so the cubic in D = 4
  needs c_N = 2, a nodal line.
- Shells vanish only at k = 0, M = 0, and a boosted zero-energy ring state leaves the ring spectrum (K9).

**V2, ring with cone dimensional regularisation.**
- Master formula: ∫dⁿq/(2π)ⁿ (q² + Δ²)^a = Γ(−a − n/2)/[Γ(−a)(4π)^{n/2}] Δ^{2a+n}.
- Result: ε_dr(Δ) = A|Δ|³/3 exactly. This equals the tube's Λ⁰ part, and the ring is (m*/v) × the D = 3 sea.
- The mode-sum pressure (K5) gives p = −ε, so w = −1. The q₁-odd ring term cancels, and ⟨2cos²θ + sin²θ⟩ = 3/2.
- At P_cos = 0, ε_dr = 0.

**V3, tube band** q₁² + q₂² < Λ² (K3).
- V_band(Δ) = −(A/3)[(Λ² + Δ²)^{3/2} − |Δ|³] = E₀ − AΛΔ²/2 + A|Δ|³/3 − AΔ⁴/(8Λ) + …
- E₀,tube(0) = −AΛ³/3 = −βP_Λ³/3, with P_Λ = Λ/h.
- Pressure: p(0) = −AΛ³/6, so w = +½ (w = 0.487 and 0.160 at Δ/Λ = 0.1 and 1).

**V4, Pauli–Villars in the cone.**
- V_PV(Δ) = (A/3)Σ C_i(Δ² + M_i²)^{3/2}, with ΣC_i = ΣC_iM_i² = 0. The cubic coefficient is A/3 (universal).
- Constant: (A/3)sM³, with s = 2√2 − 2 = +0.828 for the frozen set (−2, 1; M², 2M²) and s = −6 for A2's set (−3, 3, −1;
  M, 2M, 3M).
- The constant has w = −1. Two regulators always give s > 0 (A2).

**Excitations.** A thermal or Fermi-sea population has w = ½ (ring, for any occupation at Δ = 0) and w = ⅓ (Lorentz-invariant
3D gas). Neither is dark energy.

**The unified formula** (K7, K8).
- Slot identity: β P*³/3 = a₀²/(12πG) at P* = C a₀/q_b. In n space dimensions this is a₀²/(n S_{n−1} G_n), with n S = 12π
  (n = 3) and 8π² (n = 4).
- General result: ε₀ = σβP_x³/3 ⇒ κ² = a₀²/(Gε₀) = 12π/(σλ_x³), with λ_x = q_bP_x/(Ca₀) = 4πGβC²P_x/q_b².
  - V3: σ = −1, λ_Λ = q_bΛ/(Cha₀), so κ² < 0 (no real κ).
  - V4: σ = s, λ_PV = q_bM/(Cha₀).
  - V5-N1: λ = 1, so κ² = 12π.
  - V5-N3: λ = cH_Λ/a₀, so a₀ = cH³/(12πGρ_DE) = (2/9)cH_Λ and κ_H = (8πe/3)^{3/2}/(12π) = (2/9)√(8π/3), κ_H² = 32π/243.

**The microscopic trade** (tube, magnitude only; I2, I7, K11).
- At fixed (N, m*, v, h, Λ, q_b, C): κ² = (3π/2) ħ⁹ q_b⁶ v³/(N³ m*³ C⁶ h⁶ Λ³ G³), and a₀ ∝ ħ³.
- Under H1 + H1r (v = v_r = c, m* = ħk₀/c, Λ = ε_Λħck₀/2): κ² = 12π c³ħ³ q_b⁶/(N³ ε_Λ³ k₀⁶ C⁶ h⁶ G³), and
  a₀ = c²ħ²q_b³/(2NC³h³Gk₀).
- Sensitivity: d ln κ²/d ln v = 3 at fixed microscopic parameters and 0 at fixed λ_x.
- The Jacobian of (ln a₀, ln|E₀|) with respect to (ln k₀, ln ε_Λ, ln q_b/(Ch)) has rank 2 of 3. One continuous direction is
  left after fixing a₀ and ρ_DE, plus N, so any κ is reachable.

## Results

| variant | class | value / reason |
|---|---|---|
| V1 strict Lorentz-invariant Dirac medium | **NO LAW** | m^D (m⁴ ln m at D = 4) against \|P\|^{D−1}; only point nodes are Lorentz-invariant |
| V2 ring, v = v_r = c, cone dim reg, P_cos = 0 | **IDENTITY (vanishing)** | ε₀ = 0 for every κ (the universal β\|P\|³/3 vanishes at P = 0) |
| V3 ring, tube band | **NO SOLUTION (sign and EOS)** | E₀ = −βP_Λ³/3 < 0, w = +½. Magnitude-only TRADE κ² = 12π/λ_Λ³ (window needs λ_Λ 4.68–9.01) |
| V4 ring, Pauli–Villars | **CONDITION** | constant s(A/3)M³ with s = +0.828 or −6 by regulator set, w = −1. TRADE κ² = 12π/(sλ_PV³) |
| V5-N1 q_bP⁰/C = a₀ (X2 slot) | EXCLUDED-CLASS POSIT | κ = √(12π) = 6.140 (κ_crit 5.08): miss |
| V5-N2 tether / law vacuum | **IDENTITY (vanishing)** | P⁰ = 0 |
| V5-N3 q_bP⁰/C = cH_Λ (X3 horizon) | EXCLUDED-CLASS POSIT | κ = 0.6432 (κ_crit 0.532, against the ρ_crit window [0.189, 0.501]): miss; π-odd; Z = 9/2 |
| V5-N4 free minimum | **IDENTITY (vanishing)** | minimum of P²/2C + β\|P\|³/3 at P⁰ = 0 |

**Overall: CLOSURE.** No graded variant is CONSISTENT. EXACT CANDIDATE was unreachable as frozen (§2).

**Identity checks.**
- I1: no forbidden constant in the script.
- I2: every graded κ expression carries free medium constants.
- I3: a₀(N3) → ν√(λμ)a₀ under the scaling test.
- I4, rename test: with the law's κ set to 2/5, the posits stay at 6.140 and 0.643 and fail the comparison, and the required
  λ moves from 5.32 to 6.18.
- I5: Z_H² = 81/4 ≠ 32π/3, and κ_H depends on the Friedmann coupling and the Gauss–cubic factor.
- I6: declared footing only.
- I7: ħ⁰ at fixed (β, P_x); ħ³ for a₀ and ħ⁹ for κ² at fixed microscopic parameters (ħ² and ħ³ under H1r). No
  Bekenstein–Hawking ¼ appears.
- I8: the π-weight of κ² is 1 (12π and 32π/243), and 2 for the n = 4 slot.

**MUTATE** (`cfg900_MUTATE.out`, exit 1, all four teeth bite):
- **M1, v → c/2:** β × 2, a₀ × ½, E₀,tube × 2, κ_tube² × ⅛ (κ × 0.354). The posits do not move (v cancels).
- **M2, D = 4 → 5:** the Lorentz-invariant exponent is 5 against the needed 4 (NO LAW persists). The ring's 3 against 4 means
  the ring loses the law. The slot coefficient goes from 12π to 8π² (π-weight 2). The formal horizon value at n = 4 is
  κ² = 2/9, which is π-free; that shows π-parity is a d = 4 statement.
- **M3, statistics flip:** E₀,tube > 0 and β < 0 (concave, NO LAW). The sign lock holds in both directions, and the
  dim-reg E₀(0) = 0 is unchanged.
- **M4, 8πG → 4πG:** κ_H goes from 0.643 to 0.227, a factor (1/2)^{3/2} (amendment A1). The frozen factor 1/√2 FAILS AS FROZEN
  (hand slip; see disclosures). The slot and trade outputs do not move.

**Report-only numbers.**
- Band scale: if |E₀,tube| were set equal to ρ_DE c² (N = 2, ε_Λ = 1, H1r), the ring would sit at ħck₀ = 6.6 meV, against
  ρ_DE^{1/4} = 2.24 meV.
- This is not a solution: the sign is wrong and w = +½.

## What this does to the κ campaign

- **D4 closes.** MASTER_COLD_ENERGY_EQUATIONS.md's sentence "no calculation links the independent vacuum energy to the force
  coefficients" now has a computed reason. The force coefficient comes from the medium's nonanalytic (universal) term; the
  vacuum constant is analytic and therefore scheme- or counterterm-set; and at the cosmological state the universal term is
  zero. This agrees with K227 (eight-band loop: vacuum constant independent of the loop ratio) and generalises it to the
  Lorentz-invariant and v = c cases.
- **Lorentz invariance and the cubic are incompatible in the galaxy's own dimension.** A cubic from a Dirac sea needs an
  effective one-dimension reduction: a nodal line in momentum space, or 2D sheets in position space (K224). Both define a
  frame. So a "v = c medium" can have at most emergent Lorentz invariance inside its cone, and it needs a preferred frame
  overall.
- **"c enters through v" fails.** v cancels from κ at fixed polarisation ratio (K11). The only c left is the vacuum's
  mass–energy conversion ρ_DE c², which is exactly how c enters the excluded slot class. This sharpens S1 for future doors:
  a c that enters only through ρ_DE c², with a₀ and ε₀ both built from the same β, can never fix κ.
- **The universal reduction κ² = 12π/(σλ³)** turns any "medium vacuum = cubic energy at polarisation P_x" door into the
  question "what fixes P_x/P*?". The two natural answers are the transition, which is the slot (κ = 6.14), and the horizon,
  which gives κ = 0.643 and Z = 9/2. Both are excluded classes, both miss, and both are π-odd. A mixed boson–fermion spectrum
  (K228) decouples the two signs but adds free weights (its h is free). No door of this family remains.
- κ = ½ stays FITTED. No P_LEE change: no determinate trial was added, since the posits are excluded-class.

## Disclosures

- **Hand estimates came first, as the frozen file records.** All frozen expectations were derived by hand before the freeze
  and are listed in FROZEN_CRITERIA §0, including the two posit values 6.14 and 0.643. Every one reproduces except the M4
  factor.
- **A1, the M4 factor.** The frozen file said κ_H × 1/√2 under 8πG → 4πG. The correct factor is (1/2)^{3/2}: a₀ ∝ H³/ρ
  carries the Friedmann factor e^{3/2}, and the hand estimate dropped the e inside H³ = H·H². This was found while writing the
  scorer's tooth list, after the freeze and before any script existed. It was committed alone as AMENDMENTS A1 (7f72af505)
  before the script was written or run. The scorer prints the frozen factor as FAILS AS FROZEN and grades the tooth on the
  amended factor. The tooth's purpose (κ_H moves, slot and trade do not) is unchanged.
- **A2.** The frozen two-regulator PV set always gives a positive constant, so a three-regulator set was added to show the
  sign is regulator-dependent. V4's class is unchanged.
- **A3.** Report only. ħ powers under H1r were added.
- **Runs.** The script was syntax-checked (py_compile) and edited before its first execution. The committed outputs are from
  the first execution of the normal run and the first execution of the MUTATE run. No run failed, and no output was
  regenerated after a change.
- **Scope choices.**
  - V5-N1 and V5-N3 are inside excluded classes (rules S7: X2, X3). They are printed because the door's construction reduces
    to them, and they are not graded.
  - The force sector's own quadratic energy at P*, C a₀²/2q_b² = a₀²/(8πG_s) with G_s = q_b²/(4πC), is a further slot
    reading. It is not evaluated as a variant, because the door concerns the band energy.
  - The galaxy-sourced band energy averaged over the universe belongs to the global-average class X11 (k02: five orders
    short). It is not computed.
- **Assumptions behind the numbers.**
  - Pressures use an isotropic ensemble of ring orientations, as the record's η does.
  - N is kept symbolic (the record's representation has N = 2).
  - G is the measured Newton constant. ARGON10's note that it includes the scalar inverse-square part q_b²/(4πC) changes
    nothing here.
- **Literature and overlap.** The point that a hard-cutoff vacuum does not give w = −1 is the 2D analogue of a well-known
  result for relativistic vacua. It is stated, not cited from a primary source here. K224, K227 and K228 overlap and are cited.

## Proposed ledger row (for LEDGER.md; not appended by this lane)

| CFG900 | (block 900–909; criteria 32264ab5d; amendments 7f72af505 before any script, A1 = M4-factor hand slip; agent lane; κ attempt) κ door D4: the record's nodal fermion medium (sol61 mechanism_2026_10_12) made Lorentz-invariant (v = c), its own vacuum energy as the dark energy: **CLOSURE** (no κ; κ = ½ FITTED). Strict Lorentz invariance allows only point nodes, so a Dirac sea gives m^D (m⁴ ln m at D = 4) where deep MOND needs \|P\|^{D−1}: NO LAW in every D (the cubic needs a nodal line, an effective 2+1 cone that breaks boosts). Ring with v = v_r = c: the only regulator-independent term is β\|P\|³/3 (cone dim reg exact, w = −1), which vanishes at the cosmological P = 0 (IDENTITY); tube band E₀(0) = −βP_Λ³/3 < 0 with w = +½ (NO SOLUTION; sign lock E₀ vs β per species); Pauli–Villars constant (A/3)sM³ with s = +0.83 / −6 by regulator set (CONDITION). Every vacuum–β link reduces to κ² = 12π/(σλ³), λ = q_bP_x/(Ca₀) (β, v, ħ cancel; v = c not load-bearing; window ↔ λ 4.68–9.01; one free direction left after fixing a₀ and ρ_DE). Excluded-class posits, report only: transition (X2 slot) κ = √(12π) = 6.14; horizon (X3) a₀ = (2/9)cH_Λ, κ = 0.643, Z = 9/2; both miss, π-odd. Excitations w = ½. p_exact 0, p_data 0. 20/20 checks; MUTATE 4/4 bite (v → c/2; D → 5, where the ring loses the law and the formal horizon κ² = 2/9 is π-free; statistics flip; 8πG → 4πG on the A1 factor). | (commit) |

## Proposed register line (for `kappa_attempts_register.csv`; not appended by this lane)

    K598,CFG900,VM,campaign_fresh_gravity/CFG900_kappa_D4_lorentz_nodal_medium,"nodal fermion medium made Lorentz-invariant (v = c), its own filled-band vacuum = rho_DE (strict LI Dirac sea; ring with cone dim reg / tube / Pauli-Villars; timelike P0 loci)",,,free,0,"CLOSURE: strict LI has only point nodes -> m^D vs |P|^(D-1) (NO LAW); universal beta|P|^3/3 vanishes at P_cos = 0 (IDENTITY); tube E0 = -beta P_L^3/3 < 0, w = +1/2 (sign lock); PV constant sign free; every link kappa^2 = 12pi/(sigma lambda^3) (one-parameter map; v and hbar cancel); excluded posits slot 6.14 / horizon 0.643 miss",(commit)
