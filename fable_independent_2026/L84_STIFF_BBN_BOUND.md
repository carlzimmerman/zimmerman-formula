# L84 — The BBN / N_eff bound on the a⁻⁶ stiff component in astra's F(Q)Θ affine cosmology

**Script:** `L84_stiff_bbn_bound.py` · **Output:** `L84_stiff_bbn_bound.out` · **Result:** 13/13 checks PASS
(each PASS = the stated claim is TRUE). Self-contained sympy/numpy; imports nothing from
`qwen_claude_field_theory/`.

## The formula (reproduced faithfully before interpreting)

astra's F(Q)Θ affine action yields, on flat FLRW, the eliminated auxiliary density (independently verified in
`L80_verify_fqtheta_dust.py`, and quoted verbatim in astra's `fqtheta_clock_dust_2026/REPORT.md`):

```
ρ = B + 3 M² H² − (M²/3f²) (A + C/a³)²
```

with `C = a³(−K_Q + 3H F_Q)` the shift-symmetric conserved (Noether) charge (L81). Expanding the square
(reproduced in exact sympy, check **C0a**):

```
ρ = [ B − M²A²/(3f²) ]              ← Λ-like constant
    + 3 M² H²                        ← gravitational back-reaction
    − (2 M² A C)/(3f²) · a⁻³         ← DUST (dark matter): pressureless, sign set by sign(AC)   [L81/L82]
    − (M² C²)/(3f²)   · a⁻⁶          ← STIFF (w=1) correction: THIS LANE
```

astra's REPORT: the dust "is exactly pressureless at this order; the C²/a⁶ term is a separate stiff correction."

## (a) The scaling → BBN sets the bound

A w=1 fluid dilutes as `a⁻⁶` (control **C2**: continuity `a dρ/da = −3(1+w)ρ` ⇒ `ρ ∝ a^{−3(1+w)}`, w=1 gives
`a⁻⁶` exactly). Against radiation (`a⁻⁴`):

```
ρ_stiff/ρ_rad = (Ω_stiff,0/Ω_rad,0) · a⁻²        (check R1)
```

The ratio **grows as a⁻²** toward early times (relative to matter it grows as a⁻³; relative to Λ as a⁻⁶), so
the tightest, earliest robust handle is **BBN** (n/p freeze-out, T ≈ 1 MeV, a_BBN ≈ 2.3×10⁻¹⁰).

## (b) The bound on Ω_stiff today

The stiff density at BBN must sit inside the ΔN_eff budget. With T_ν = T_γ at BBN,
`ρ_stiff = ΔN_eff·(7/8)ρ_γ` and `ρ_rad = (g_*/2)ρ_γ`, g_*(1 MeV)=10.75, so the allowed ratio is
`R_max = ΔN_eff·(7/8)/(g_*/2)`. Propagating back with a⁻²:

| ΔN_eff | T_BBN | a_BBN | **Ω_stiff,0 bound** |
|:---:|:---:|:---:|:---:|
| 0.5 | 1 MeV (simple) | 2.35e-10 | **4.1×10⁻²⁵** ← fiducial |
| 0.5 | 1 MeV (entropy-corr) | 1.68e-10 | 2.1×10⁻²⁵ |
| 0.5 | 0.07 MeV (D bottleneck) | 3.36e-09 | 8.4×10⁻²³ |
| 0.3 | 1 MeV | 2.35e-10 | 2.5×10⁻²⁵ |
| 0.3 | 0.07 MeV | 3.36e-09 | 5.1×10⁻²³ |

**Fiducial: Ω_stiff,0 ≲ 4×10⁻²⁵** (ρ_stiff,0 ≲ 3.5×10⁻⁵¹ kg/m³), spanning ~10⁻²⁵–10⁻²² across the plausible
range. Extraordinarily tiny — the a⁻² growth over ~20 e-folds crushes any present-day stiff density (check **B1**).

**Both a₀ footings give the identical bound** (check **B2**): a₀ enters astra's action only through the galaxy
MOND term `M² a₀² G(|V|/a₀)`, **not** the FLRW stiff term. The BBN bound is a₀-independent — demonstrated by
computing on both footings (9.3619e-11 / 1.1279e-10 m/s²) and getting bit-identical numbers.

## (c) Fine-tuning or natural? → **Fine-tuning (a real cost).**

The **same charge C** sources both pieces: dust ∝ A·C (linear), stiff ∝ C² (quadratic). Their ratio is
independent of M, f (check **F1**):

```
Ω_stiff,0 / Ω_dust,0 = |C| / (2|A|)
```

If this dust **is** the observed dark matter (Ω_dust,0 ≈ 0.264), the BBN bound forces **|C|/|A| ≲ 3×10⁻²⁴** —
C tuned ~24 orders of magnitude below A while the product |A·C| stays fixed at the DM abundance. Since `C/a³`
and `A` share units inside `(A + C/a³)`, "natural" is |C|/|A| ~ 1; and absent tuning (|C| ~ |A|), the stiff
term **overshoots the BBN radiation budget by ~3×10²³ — >20 orders of magnitude** (check **F2**). No shift
symmetry or other principle suppresses C² relative to A·C (C is an integration constant, A a Lagrangian
coefficient), so this is a **genuine fine-tuning**, not a symmetry-protected/derived smallness (check **F3**).

**Honest both-ways note:** there is a tuning-free corner, A = 0, which kills the dust cross term and leaves
only the stiff piece (trivially BBN-safe) — but it supplies **no dark matter**. The fine-tuning is intrinsic to
the *interesting* dust=DM reading: the very charge that gives the dark matter also sources the stiff term.

## Sign concern: negative-energy stiff — ghost?

`ρ_stiff = −M²C²/(3f²a⁶) < 0` for **either** sign of C (∝ −C²; check **C1**). A negative component growing as
a⁻⁶ threatens `ρ_total < 0` (H² < 0: breakdown/bounce) at early times.

**Verdict (check S3):** this is **not, by itself, a ghost theorem** — a ghost is a wrong-sign *kinetic* term
in the perturbation action, not a negative background ρ (spatial curvature also enters ρ as a negative a⁻²
piece). At the BBN-saturated bound the crossover `a_crit = √(Ω_stiff,0/Ω_rad,0) ≈ 7×10⁻¹¹` sits **below** a_BBN
(check **S2**), so the observable universe stays radiation-dominated and positive; the negative-energy
breakdown is pushed into the untested pre-BBN regime. **But** it compounds astra's own, independently-flagged
health warnings for this same scalar — the decoupling `c_bare² = −1` (L80/REPORT) and the loss of longitudinal
ellipticity `G''(y)→0` as y→0 (astra's `ACTUAL_PRINCIPAL_GATE.md`). The negative stiff energy is another face
of the same **open** propagating-health question; a concern to record, feeding the ADM analysis astra names as
decisive — not an independent kill.

## Confidence

- **HIGH** on the bound and the a⁻² scaling — elementary cosmology on astra's verified formula.
- **HIGH** that the smallness is a fine-tuning, not a derived/protected number — C and A are independent, and
  the same charge does double duty.
- **MEDIUM** on the sign verdict — negative background energy is a real concern, but the decisive statement is
  the perturbative-health/ADM analysis that remains open upstream. This lane sharpens that question; it does
  not settle it.

This is a **cost recorded honestly**, not a clean kill: astra's dust route survives BBN *if* the charge is
tuned |C|/|A| ~ 10⁻²⁴, and the negative stiff sign adds to (does not by itself close) the standing health
question.
