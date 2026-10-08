# GF1 — The germ-flip: the 32π² puzzle reduced to one integer

**Lane GF1, `deepseek_push`, 2026-10-08. Run: `python3 GF1_germ_flip.py` → `GF1 COMPLETE: 23/23`
(exit 0). MUTATE: `GF1_MUTATE=1` → 22/23, R4b fires as declared (window widened to 1%).**

## The puzzle, in the framework's own language

The framework's one empirical closure is the tie between the galactic acceleration scale and
the dark-energy density. In the record it appears as several spellings of one statement:
`A·Λ = 32π²` (sonnet lane), `Z² = 32π/3` (C06/G058), `Gρ_Λ = 4a₀²/c²`, `a₀ = c²/(Z·R_dS)`,
`κ = ½`. The committed Lean-certified identity (G058, C06 `closure_iff_zSq`) says the measured
`Ω_Λ = 0.685` closes **iff** `Z² = 32π/3` — so the tie is already exact to register precision;
what has never been delivered is a *derivation* of the number. Roughly 110 lanes across the
record (sonnet55 `puzzle_32pi`: 70 sections/50 lanes → FITTED; deepseek PD01–PD22: conditional
chain, degree-2 joint named open; opus_48 `kappa_audit`: two-channel count obstructed for
dust, escape shape closed modulo closed loopholes; T-wave `t4_sharp_constants`: no forced
constant; T8: the kernel appears nowhere in the 722-manuscript corpus) have each attacked one
spelling.

## The result of this lane (all exact, sympy residual 0)

**R1 — THE ONE-INTEGER REDUCTION.** Every target is one parameter `n` times *certified*
π-bookkeeping (Einstein 8π, Friedmann 3):

| identity | n-general form | at n = 2 (committed) |
|---|---|---|
| tie | `a₀ = c√(Gρ_Λ)/n` | `Gρ_Λ = 4a₀²/c²` |
| germ square | `Z² := (cH_Λ/a₀)² = n²·8π/3` | `Z² = 32π/3`, `Z = 5.788810036…` |
| sonnet target | `A·Λ = 8π²n²/c⁴` | `A·Λ = 32π²/c⁴` |
| closure | `Ω_Λ = 8πn²a₀²/(3H₀²c²)` | `Ω_Λ = 32πa₀²/(3H₀²c²) = 0.685` |
| boundary | `cH₀/a₀ = n√(8π/(3Ω_Λ))` | `6.995 ≈ 7` |
| kappa | `κ = a₀/s = 1/n`  (s := n a₀; s = 2a₀ committed) | `κ = ½` |

**The entire "32π²" content is the integer `n = 2`.** All π's are the Friedmann–Einstein
bookkeeping `8π/3` (H² = 8πGρ/3) and the Einstein 8π; none of them is underived.

**R2 — COMPOSITION = KERNEL (one open step, not two).** The PD-wave OR-composition equals the
max-entropy kernel exactly: `p+q−pq` at `p = q = u/(1+u)` **IS** the committed kernel CDF
`1 − (1+u)⁻²`; the family `f_n(u) = n(1+u)⁻⁽ⁿ⁺¹⁾` has log-moment `c = 1/n = κ`, shape
`ℓ₁ = n+1 = 3`, entropy `S = 3/2 − ln2` at n = 2. So the opus_48 work order's "degree-2 joint"
(PD22-P4) and the E/F/G lanes' "ℓ₁ = 3 selection" are **the same open step**.

**R3 — THE AUDIT.**
- *n-power table (exact):* every committed sheet carries `n` at one consistent power
  (Z: n¹; closure: n²; σ²: n^−½; E_bind: n^−½; m-ladder: n^+½; kernel c: n⁻¹) — no
  inconsistency, and no sheet closes on `n` alone.
- *Overdetermination search:* 0 of 6 elimination pairs of committed relations pins `n` —
  every pair restates G058-gen. **The flip is underdetermined by exactly one integer.**
- *Flatness transport lemma (new, certified):* under rung-5 (the phantom IS the response), a
  profile `ρ = Ar^−γ` gives `g_φ ∝ g_N^((γ−1)/2)`: the observed flat asymptote (γ = 2)
  *transports* to the square-root response (exponent ½) — but transports the exponent, not
  the normalization of the tie.
- *Data pin:* `n_germ = 2.00010 ± 0.0172` from (Ω_Λ, H₀, a₀) at declared 1%-class inputs; the
  committed slope channel (`b = 1.004 ± 0.011`, n = 542, G131/G162) measures the same integer.
  Central values agree at the 10⁻⁴ level; the two channels are consistent.

## Verdicts (pre-registered)

- **V1 REDUCED** — the 32π² puzzle is exactly the integer `n = 2`; every π is certified
  bookkeeping; the physics content is the tie `a₀ = c√(Gρ_Λ)/n`.
- **V2 UNDERDETERMINED-BY-ONE-INTEGER** — no committed relation forces `n`; the count-2
  delivery is obstructed for dust (opus_48, cited not re-run); the degree-2 joint and the
  ℓ₁ = 3 selection are one step (R2).
- **V3 DATA-CONSISTENT** — `n_germ = 2.000 ± 0.017` vs slope register; both are one integer.
- **V4 OPEN (registered)** — a structural origin of `n = 2`. Three candidate homes with
  precise obstructions: (i) the two-channel count (obstructed for dust — engaged rank 1);
  (ii) the degree-2 max-entropy route (⟸ the anchor `σ² = C/2`, whose five derivations share
  the equilibrium premise); (iii) the tie's normalization (the flatness route transports the
  exponent only, R3b).
- **H1/H2 honesty** — R1/R2 are identity-class (true by construction, reported as reduction,
  never as derivation); the tie remains an empirical closure (0.06%-class footing). This lane
  derives nothing new about nature; it reduces the target space to one integer and proves the
  reduction exact.

## Falsification tests (registered here)

1. **Lockstep.** The germ closure and the deep-slope measurement are the same integer: a
   > 3σ split between {Ω_Λ, H₀, a₀}-pinned `n` and the slope-pinned `n` kills the
   one-integer reading. (Both currently ~1%; JWST z ≈ 2.5 BTFR + future a₀ precision
   tighten both.)
2. **Overdetermination.** Any committed relation that, combined with existing ones, yields an
   n-only equation closes the puzzle mechanically — the lane's pair scan is the template;
   adding a seventh sheet that pins `n` would fire R3c backward.
3. **Sharp decoy.** The germ ratio 4 = n² is not a π-coincidence: no (p/q)π^m (p,q ≤ 12,
   |m| ≥ 1) within 0.5%; MUTATE widens the window and the check fires — the scan is live.

## Files

- `GF1_germ_flip.py` — the lane (sympy exact; controls → claims → honesty; MUTATE env).
- `GF1_germ_flip.out` — 23/23 run; `GF1_germ_flip.out_run1_unevaluated_meijerg` — first run
  (22/23: the general-n direct sympy integral left a Meijer-G; substitution route fixed it;
  both kept, append-only).
- `GF1_germ_flip_MUTATE.out`, `GF1_results_MUTATE.json` — declared decoy flip.
- `GF1_results.json`, `GF1_results_run1.json` — structured results.

Registers used (re-read, cited in-script): a₀ = 9.3619e-11 (C06), ρ_c = 8.533238720309458e-27,
Ω_Λ = 0.685, Z = 5.788810036466141 (C06); slope b = 1.004 ± 0.011 (G131/G162); G = 6.674e-11.
