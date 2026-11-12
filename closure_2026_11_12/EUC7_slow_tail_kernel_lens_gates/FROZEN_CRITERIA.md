# EUC7 (SLOW-TAIL KERNEL ON THE LENS GATES): FROZEN CRITERIA

Committed alone, before any EUC7 script exists and before any EUC7 number is computed. 2026-11-12.
Owner, 2026-11-12: "keep swinging". A test lane: it adopts nothing.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt), never pooled. Not "theory closed". No outcome may be
described as the data favouring the framework.

## 0. What this lane is

The Codex phase-2 review (`research_closure_2026_11_12/euclid_desi_phase2/theory/THEORY_CHECKPOINT.md` §3–4) reports
that in its unscreened parent class a cold pull that returns to zero or saturates at high acceleration cannot keep the
clock curvature non-negative, and that a **slow-tail kernel**

    μ★(x) = 1 − 1/√(1 + 2x),      x = g/a₀,      g_N = μ★ g,

does, on a declared class of backgrounds. It keeps μ ~ x at low acceleration, so the same a₀ and the same deep
relation. Its own notes say: no lensing or rotation-curve fit exists for it, and unscreened it adds 5.27e-7 m/s² at
1 AU. Law S, the kernel EUC1–EUC5 graded, is `μ = x/(1+x)`: its cold pull saturates at a₀. The slow tail's cold pull is
`g/√(1+2x)`, which grows as √(g a₀/2) and never saturates. Lens cores sit at 5 to 50 a₀, where the two differ most.

This lane puts the slow-tail kernel, unscreened, through the lens gates already built, with nothing else changed.

**Seen before freezing (disclosed).** Every law S result of EUC1, EUC4, EUC5 and the SLACS record. For the slow tail:
nothing computed; only the estimate above that its cold pull at lens radii is a few times law S's, so it may supply
too much.

## 1. Tests (frozen)

Stars, Sérsic deprojection, projection, cosmologies, Jeans model, samples and statistics exactly as in EUC1 / EUC4 /
EUC5 (their code is imported). `b` is the log₁₀ factor on the catalogued **Salpeter** stellar mass the kernel needs.

- **T1 SLACS lensing** (70 lenses, true source redshifts, n = 4, Auger cosmology): median `b` with a 95 % bootstrap
  interval, per footing.
- **T2 SLACS dynamics** (published dispersions, fibre 1.5″, seeing 1.5″, β = 0): median `b_dyn`; and the median of
  `b_dyn − b_lens`.
- **T3 Euclid ceiling** (EUC1's sample P, source at infinity): `f₂₅` and median `b∞`, and the fraction with
  `b∞ < −0.25` reported.
- **T4 Euclid wide lenses** (EUC4's W_B: grade B, θ_E ≥ 1.7″, source at infinity): `f₂₅`.
- **T5 Euclid dynamics** (EUC5's DESI dispersions divided by 1.064, the post hoc SLACS scale): median `b_dyn` on S.

## 2. The stellar-mass window and the words (frozen)

A stellar population cannot be lighter than a Chabrier / Kroupa one: `b ≥ −0.25` (the catalogue's own statement:
Chabrier is 0.2–0.25 dex below Salpeter). Massive early types are measured at Salpeter or somewhat above: `b ≤ +0.10`.

Per footing, on **T1** (the two-sided gate; SLACS has source redshifts):
- **OVERSHOOTS** if the upper 95 % bound of the median `b` < −0.25: the kernel alone supplies more than the lens
  mass allows even with the lightest stars. A fail of the unscreened kernel.
- **INSIDE THE WINDOW** if the whole interval lies in [−0.25, +0.10].
- **SHORT** if the lower bound > +0.10.
- **AT AN EDGE** otherwise.

T2 gets the same words, labelled dynamics. **ONE POTENTIAL HOLDS** on SLACS if |median (`b_dyn − b_lens`)| ≤ 0.06 dex
(law S: 0.032).

T3 and T4 get EUC1's and EUC4's words unchanged (CEILING HOLDS / BROKEN / NO VERDICT; WIDE LENSES BREAK THE CEILING /
NOT CONFIRMED / NO VERDICT). These are one-sided lower bounds: they can only show the kernel still falls short.

Lane summary = the T1 word per footing, with T2–T5 beside it.

## 3. Instrument checks (frozen; a failure makes the lane NOT EVALUABLE)

- **S1** kernel inversion: for g_N/a₀ from 1e-6 to 1e8, the recovered g satisfies `g_N = μ★(g/a₀) g` to 1e-10.
- **S2** limits: `g → √(g_N a₀)` to 1 % at g_N/a₀ = 1e-6; cold pull `→ √(g a₀/2)` to 1 % at g_N/a₀ = 1e6.
- **S3** the unscreened Solar correction at 1 AU, canonical footing, is 5.27e-7 m/s² to 1 % (the Codex number).
- **S4** with law S in place of the kernel the same code returns the record: SLACS radius ratio 0.885 ± 0.005 and
  `b_dyn − b_lens` = +0.032 ± 0.005.
- **MUTATE** (`EUC7_MUTATE=newton`, a₀ → 10⁻³⁰): T1's median `b` must rise on both footings; exit 1; separate outputs.

## 4. Not claimed

- Nothing about a screened version of the kernel: screening changes the field in exactly this regime and must be
  solved first. A fail here is a fail of the unscreened kernel as written.
- No rotation-curve statement. No health statement (that is the Codex lane's own work).
- No measurement of a₀ or κ.
