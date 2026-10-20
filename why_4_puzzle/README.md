# Why 4? The coefficient in G ρ_DE = 4 a₀²/c²

The framework's acceleration scale is a₀ = κ c √(G ρ_DE). With κ = ½ the following statements are all the same:

    G ρ_DE = 4 a₀²/c²      Λ = 32π a₀²/c⁴      Z = cH_Λ/a₀ = √(32π/3) = 5.7888      κ = ½

Explaining the 4, the 32π, the ¼, Z or κ is one problem. This folder is the puzzle's home: the standing answer, where the
record sits, and the lanes run here.

## Standing answer (2026-10-20)

**The 4 is FITTED, not derived.**
- **The data.** CFG493 measures κ_Λ = 0.417 ± 0.095 and κ_crit = 0.345 ± 0.078 (M/L-insensitive gas routes, shared
  systematics included). So ½ sits at 0.8σ, and 1/κ² = 4 is not pinned: today's 2σ window allows 1/κ² from about 2.7 to 19.
- **Why the data cannot decide yet.** To tell ½ from the recurring 0.461 (Z = 2π) needs a₀ to ≤ 2.8%, against a 9.3%
  shared-systematics floor.
- **The theory.** About 440 derivation attempts are on record (`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/`).
  None gives ½ without putting it in.
  - The census of every place c meets a₀ in the record (CFG891) finds no equation that yields exact ½ unless ½ or its
    premise is written in.
  - The constructive lane (CFG911) reduces what is missing to one statement. A bare-G portal a₀² = ξ G ε_DE is π-free, but ξ
    is free. **The 4 still has to come from somewhere named.**

## The walls any answer must clear (KAPPA_DOORS.md)

1. **c is required.** {a₀, G, ρ} have no dimensionless group, and the c-free cold-energy system is scale invariant (CFG893).
2. **π-parity.** A route built from a₀ and H alone gives κ² ∈ ℚ·π^odd, so never ½. Einstein's 8πG or Poisson's 4πG is always
   left over unless π cancels between sectors.
3. **ħ-freedom.** a₀ carries no ħ.
4. **The zero mode.** A local action can shift its vacuum constant freely, so a symmetry, quantisation or dynamics must be
   named that fixes it.

Plus the campaign's look-elsewhere rule. A "consistent" landing carries no weight: P_LEE(data) = 1. An exact ½ needs an
independent second prediction to reach 3σ.

## What has been tried (pointers, not a re-run list)

- **Ledger and rules.** CFG894 holds the register (one row per attempt), the rules and the doors.
  Read `KAPPA_CAMPAIGN_RULES.md` before adding anything.
- **Doors D1–D5, all closed on 2026-10-20:**
  - CFG897, the stiffness term's FRW vacuum: CLOSURE.
  - CFG898, drift-causality saturation: NOT A SELECTION.
  - CFG891, the census of c-terms: π-free but not ½.
  - CFG900, the Lorentz-invariant nodal medium: CLOSURE.
  - CFG905, Festina Lente: CLOSURE.
- **Audits.**
  - CFG904: the KMS 0.4607 withdrawal stands.
  - CFG908: none of the four unaudited "κ derived" claims derives the law's κ.
- **Structures L32 once listed as open.** All relocate the 4 into another free choice (L40):
  - S9, two-condensate transmutation;
  - S10, coset / nonlinear realisation (κ = √2, refuted at 21σ);
  - S8, horizon thermodynamics.
- **The 32π campaign.** `sonnet55_push/puzzle_32pi/README.md`, §1–70.
- **Still registered and unrun: p63 (a₀ as a field).** It belongs to the "32pi squared puzzle" chat, which also holds the
  KAPPA_LOGIC Lean file and the measured-κ provenance audit. Do not duplicate it.

## Lanes in this folder

| lane | question | verdict |
|---|---|---|
| [W4-01](W4_01_untouched_gravity_families/README.md) | Do the seven gravity families the register never touched (DGP, Kaluza–Klein, dRGT/bigravity, mimetic, Einstein–Cartan, f(T), Hořava–Lifshitz) fix the 4? | **NO FAMILY SELECTS κ.** DGP's two Planck masses make r_c π-free, but the dark energy reaches the a₀ scale only through Friedmann's 8π, giving the menu {2.894, 0.691, 0.293}, all π-odd. KK with the force-law G₅ gives a π-free a₀ = (8/3)RGρ, but R is free. Everything else is a trade, ħ-bearing or an identity. |

## What would change the answer

- **Data.**
  - κ to ≤ 2.8%. The unlock is a stellar M/L zero point and an absolute gas scale at the few-percent level.
  - The registered tests: ALMA gas predictions (sealed, releases 2026-11-06 and 11-28), Gaia DR4 (2026-12-02), and the
    a₀(z ≈ 2.5) zero point. Those decide the law; they do not derive the 4.
- **Theory.** A named principle that fixes ξ = ¼ in a π-free, c-carrying portal of a dynamical ρ_DE, checked in a second
  dimension, together with a second prediction it also fixes. Nothing on record supplies that.

## Adding a lane here

Follow `KAPPA_CAMPAIGN_RULES.md`:
1. Commit `FROZEN_CRITERIA.md` alone, before any script.
2. Declare the option space, π/ħ class and MUTATE.
3. Run a light single-core script (nothing beside a live 1024³ job beyond that).
4. Append one register row per attempt to CFG894's CSV, then rerun `kappa_campaign_lee.py`.

Name lanes W4-02, W4-03, and so on.

κ = ½ FITTED. Not theory closed.
