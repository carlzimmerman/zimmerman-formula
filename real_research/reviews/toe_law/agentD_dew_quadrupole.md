# Door II decision calculation: the Deffayet–Woodard nonlocal-metric MOND quadrupole vs Cassini 2026

*Agent D memo, 2026-06-10. Commissioned by `agentC_covariance_memo.md` §4 (the bounded calculation that settles the
Door-II loophole cell). Question: compute or rigorously bound the Solar-System EFE quadrupole Q2 of the
Deffayet–Woodard model (arXiv:2512.10513, JCAP 04 (2026) 081; class opened by arXiv:1106.4984) against the 2026
Cassini bound Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (Park–Hees–Famaey+, arXiv:2602.17884). Companion scripts (run, outputs
saved): `agentD_dew_quadrupole.py/.out`, `agentD_dew_rescue_checks.py/.out`. Sources: LaTeX of both DEW papers
fetched from arXiv this session; equations quoted verbatim below. Pre-registered settings honored: g_ext =
2.15×10⁻¹⁰ m/s² fixed (robustness 2.0–2.48), both a0 footings (1.2×10⁻¹⁰ = DEW's own; 9.36×10⁻¹¹ framework).
Both-ways discipline at full weight: §4 is an extended attempt to make the model PASS.*

---

## VERDICT (per the pre-registered fork)

**The first branch fires: the published DEW model fails the Cassini gate robustly — Q2 ≥ 1.0×10⁻²⁶ s⁻² at the
pre-registered settings under every method/footing combination — so the DEW loophole JOINS AeST at the Cassini wall
and the trilemma perimeter RE-CLOSES around the MI hybrid, with one named, quantified residual (below).**

| Method | a0 = 1.2e-10 (DEW's own) | a0 = 9.36e-11 (framework) |
|---|---|---|
| **Direct AQUAL solve (the model's true static limit)** | **Q2 = +2.80×10⁻²⁶ → 14.6σ** (5.4× the 2σ ceiling) | **Q2 = +1.74×10⁻²⁶ → 8.8σ** (3.3×) |
| QUMOND-equivalent q-integral (verified Desmond eq. 10–12) | Q2 = +2.26×10⁻²⁶ → 11.7σ | Q2 = +1.03×10⁻²⁶ → 4.8σ |

(σ = signed tension |Q2_pred − 1.6×10⁻²⁷|/1.8×10⁻²⁷; 2σ acceptance window [−2.0, +5.2]×10⁻²⁷ s⁻². The
ρ_total-footing a0 = 1.13×10⁻¹⁰ lies between the computed footings; Q2 interpolates to ≈ 2.5×10⁻²⁶, same verdict.)

Across the full g_ext robustness range (2.0–2.48×10⁻¹⁰) the published function never drops below +0.74×10⁻²⁶
(QUMOND proxy, most hostile corner) / ≈ +1.2×10⁻²⁶ (AQUAL), i.e. never below 3.2σ. **"Open gates" is no longer the
DEW row's status: its decisive gate is now computed, and it is failed** — by the same diagnostic, in the same
acceleration window (g_ext/a0 ≈ 1.8–2.3), and for the same structural reason as AeST/QUMOND: the static limit is
AQUAL and the RAR-compatible part of its function family is too gradual at y ≈ 2.

**The named residual (the honest "in between" sliver):** the DEW free function is not pinned by the construction.
Within the family that keeps their deep-MOND coefficients (§4), members sharpened beyond the published choice can
pass the 2026 measurement — but only through an accidental sign-cancellation of the quadrupole (their μ overshoots
1, an anti-MOND lobe their own f(Z) creates), and every passing member is (i) **g_ext-fragile** — its pass band
(~±0.15×10⁻¹⁰) is narrower than the current g_ext uncertainty, sitting on a knife edge between +Q2 failure at low
g_ext and −Q2 failure at high; (ii) **RAR-penalized** — binned-RAR χ²/bin 13–21 vs the achievable floor ~5.5 even
when each candidate is given its best-fit Υ (2.4–3.4× penalty; Desmond's RAR-vs-Cassini trade-off reproduced inside
the DEW family); (iii) **unselected** — nothing in the theory picks the cancellation point; the 2026 paper chose
f(Z) for simplicity and lists exploring alternatives as future work. The second fork branch ("Q2 ≤ ~1e-27 with an
RAR-compatible function → the loophole leads") is NOT met by any member. So: published instance — closed at
8.8–14.6σ; function class — closed in the same Desmond sense as AQUAL/QUMOND generally (no robust + RAR-compatible
member), modulo the tuned sliver stated above.

---

## §1 Step 1 result: the static limit IS AQUAL-reducible (method branch 2)

**What the 2026 paper supplies (verbatim, `synthesis.tex`):**

- The nonlocal invariant and its static reduction (their eq. labeled `Zdef`):
  > Z[g] ≡ (4c⁴/a0²) g^{μν} ∂_μ[□⁻¹ R_{αβ}u^α u^β] ∂_ν[□⁻¹ R_{ρσ}u^ρ u^σ] ⟶ (4c⁴/a0²) ∇Ψ·∇Ψ
  with u_μ = ∂_μφ[g], (∂φ)² = −1 (their eq. `phieqn`), and □⁻¹(R_{αβ}u^αu^β) ⟶ Ψ in statics (their eq. `Psiinterp`).
- The free function (their eq. `fdef`, with small-Z expansion `fexp` f = ½Z − ⅙Z^{3/2} + O(Z²)):
  > f(Z) = ½ Z exp[−⅓ √|Z|]
- The MOND addition: ΔL = (a0²/16πG) f(Z[g]) √−g (their eq. `invL`); lensing tie Φ = −Ψ enforced by unmodified
  ij-equations (their eqs. `G00`, `Gij`); the deep-MOND g00 equation they target (their eq. `BTFR3`):
  > (2c²/a0 r²) ∂_r[rΨ′(r)]² = (8πG/c²) ϱ(r)
- Regime structure (their conclusions): cosmology Z<0; deep MOND 0<Z≲1; Newtonian Z≫1; a0 ≃ 1.2×10⁻¹⁰ m/s² (their
  eq. `rhoDM`, tied to ρ0 = 45a0²/16πG).

**Derived here (two independent routes agree; PART 1 of the script):** varying the static weak-field Lagrangian
L_EH(Ψ,Φ) + (a0²/16πG)f(Z) gives Φ = −Ψ exactly (f carries no Φ) and the g00 equation

> **∇·[ μ(|∇Ψ|) ∇Ψ ] = 4πG ϱ/c², with μ = 1 − 2f′(Z) = 1 − e^{−y}(1 − y/2), y ≡ 2g/(3a0), g = c²|∇Ψ| (total field).**

This is exactly the Bekenstein–Milgrom AQUAL equation in the total potential. Cross-checked in the 2011 paper's
(a,b) Schwarzschild-gauge variables: their eq. `yAlone` L_MOND = (9a0²/32πG) y² e^{−y} √−g **is the identical
model** (Z = 9y²), and the same μ follows from their eqs. `gtt`/`grr`. Limits verified: μ → g/a0 as g→0 (exact
deep-MOND/BTFR normalization — the ½Z and −⅙Z^{3/2} coefficients of `fexp` are PINNED by GR-cancellation and the
BTFR amplitude; everything beyond is free); μ → 1 exponentially at high g. One structural surprise that matters
below: **μ crosses 1 at g = 3a0 and overshoots (μ_max ≈ 1.0249 at g = 4.5a0)** — an anti-MOND lobe (g_obs < g_N for
3a0 ≲ g ≲ 15a0) built into their f(Z); the EFE source (ν−1) is therefore sign-mixed.

Because the static limit is AQUAL, the **repo-verified Desmond+2024 formalism applies essentially intact**
(`CASSINI_QUADRUPOLE_CONSTRAINT.md`: Q2 = (3a0^{3/2}/2√(GM))·q, q recomputed for their function), and the full
nonlinear AQUAL problem is also solved directly.

*Scope of the reduction (honest):* (i) the reduction uses u^μ → δ^μ_0 + O(h) and □⁻¹ → ∇²⁻¹ on static fields —
their own published limit (2011 eqs. `ulimit`, `boxlimit`); corrections are O(Ψ) ~ 10⁻⁶ and O((v/c)²) ~ 10⁻⁶
(their own preferred-frame estimate). (ii) The external field enters Z[g] through the total ∇Ψ — □⁻¹R_uu is sourced
by ALL matter, so Z at the Sun contains the Galaxy's gradient; the AQUAL boundary condition |∇Ψ| → g_ext = observed
2.15×10⁻¹⁰ is exactly the standard EFE configuration. (iii) The synthesis model's M[g] must have relaxed to −f(Z)
at the solar position; the solar neighborhood is as deep in the bound regime as galaxies get (√Z = 2g_ext/a0 ≈ 3.6 >
0), and any failure of M-relaxation there would suppress galactic MOND identically — no selective escape (their own
transition mechanics is open: "a definitive analysis in a realistic setting is obviously a formidable numerical
undertaking", §4.2 of 2512.10513).

## §2 The computation and its validation chain

1. **Verified q-integral** (Desmond+2024 eq. 10–12, transcribed from the audited `aest_cassini_quadrupole_full.py`):
   validation on the RAR ν gives q = −0.272/−0.248 and Q2 = +4.65/+2.93×10⁻²⁶ at the two footings — inside the
   repo's 10-facet-verified band (q ≈ 0.21–0.27, Q2 ≈ 3–5×10⁻²⁶; Desmond Tab. 1 ≈ 2.9×10⁻²⁶; Hees+2016 ν̃_0.5 =
   3.5–4.4×10⁻²⁶). vmax-stability: q constant to 6 digits for vmax 40→160.
2. **Direct nonlinear AQUAL solver** (new; Picard + Legendre-spectral, point mass in uniform external field, MOND
   units): validation μ_simple gives Q2 = +4.27×10⁻²⁶ = 0.875× the QUMOND value with the paired ν_simple —
   inside the known ~10–30% AQUAL/QUMOND spread; μ_standard gives +2.27×10⁻²⁶, inside the Hees+2014 function-space
   interval 2.1×10⁻²⁷–4.1×10⁻²⁶. Headline numbers stable to 0.3% under grid refinement (Nr 700→1100, Nth 64→96,
   lmax 8→12). Interior-quadrupole plateau spread ≤ 2%.
3. **DEW function:** q(ẽ=1.792) = −0.132 — about half the RAR-family q, because their published f is already
   sharper at y ≈ 2 than the RAR family — not sharp enough by a factor ~5 in Q2. The AQUAL value runs 1.24–1.68×
   ABOVE the QUMOND proxy for this function (sign-mixed source; the proxy is the optimistic bracket). Both reported;
   the AQUAL number is the model's true static limit.

The headline table is in the VERDICT block. The MW boost at the Sun for the published function is +3.6% (own a0)
/ −1.8% (framework footing) vs the RAR-required ~+28–36% — i.e. the published DEW function ALREADY abandons the
RAR's solar-position boost (this is its RAR cost, §4), yet still fails Cassini by 4.3–5.4× on Q2.

## §3 Step 4 result: what the DEW papers themselves say (verbatim, pinned)

- **2512.10513 (2026), Conclusions — the EFE is named future work (agentC's finding verified exactly):**
  > "Another project is to explore the ``External Field Effect'' [Milgrom 2014], whereby the gravitational fields
  > produced by distant masses can affect whether or not a local system is in the MOND or Newtonian regimes.
  > Without a relativistic extension of MOND this could only be guessed at, but it can be addressed in detail
  > within the context of a model such as we have presented. **The key issue is how distant masses affect the
  > nonlocal functional Z[g](x).**"
  No Cassini, ephemeris, or Q2 reference appears anywhere in the paper. (This memo is, to my knowledge, the first
  computation of that "key issue" — answered: distant masses enter Z[g] through ∇Ψ_total, giving the standard AQUAL
  EFE, and the published f(Z) then fails the 2026 bound at 8.8–14.6σ.)
- **1106.4984 (2011), §"An Explicit Model" — the EFE acknowledged as present and unanalyzed:**
  > "Our final comment on explicit models concerns the ``external field effect'' in which MONDian behavior of one
  > system can be severely affected by another [Wu & Kroupa]. This property is deeply embedded in the nonlocal
  > constructions of our scalars X[g](x) and Y[g](x). … It is highly significant that they also depend upon *past
  > history*. … Of course we cannot, at this stage, claim that our model incorporates the external field effect in
  > a desirable way; what actually happens beyond the static, spherically symmetric limit is a matter for future
  > study."
- **1106.4984, the solar-system safety claim — true but covering only the ISOLATED system:**
  > "It is easy to check that the predicted deviations from general relativity are exponentially small with respect
  > to the tightest solar-system constraints, but that the MOND behavior is predicted at large distances."
  This claim is correct for the interior (g_N/a0 ≳ 10⁴ ⇒ e^{−y} ≈ 0) and **does not cover the EFE quadrupole**,
  which is sourced where the Sun's field has decayed to ~g_ext ≈ 1.8a0 (r ~ 4–5 kAU), where their suppression
  factor is only e^{−1.19} ≈ 0.30. The Cassini bound tests exactly the configuration their exponential argument
  does not reach — and now excludes it.

## §4 The rescue attempts (both-ways section — trying hard to make it pass)

The free function is the model's only flexibility ("A related project is to explore different possibilities for the
interpolation function f(Z)… The choices made… seem adequate but it would be desirable to study what other
possibilities exist" — 2512.10513, Conclusions). Scanned family: μ_α = 1 − e^{−y−αy²}(1 − y/2 − αy²) — keeps both
pinned deep-MOND coefficients, sharpens the screen; α=0 is the published 2026 f(Z); **α=1 is the OTHER published
function (2011 eq. `example2`)**. Findings (AQUAL throughout; full tables in the .out files):

1. **A passing window exists but only by accidental cancellation.** As α grows, the positive (g < 3a0) and negative
   (overshoot) lobes of the EFE source cancel; Q2 crosses zero near α ≈ 0.7 (own footing) / α ≈ 0.33 (framework
   footing) and goes NEGATIVE beyond (published 2011 example2: Q2 = −5.8×10⁻²⁷ → 4.1σ, also excluded). Pure-
   sharpness escape à la Hees+2016 ν̄₃ (tiny positive Q2, robust) is NOT available in this family: large α kills
   MOND at fixed scale g* ~ a0/√α → 0 while the overshoot relic keeps |Q2| ~ 5–10×10⁻²⁷ negative.
2. **Every passing member is g_ext-fragile.** Own footing: α=0.5 passes only for g_ext ∈ [2.32, 2.48]; α=0.6 only
   [2.15, 2.32]; α=0.75 only [2.00, 2.15]. Framework footing: α=0.25 only [2.15, 2.32]; α=0.30 only [2.00, 2.32]
   (fails 2.48). No α passes across the plausible range 2.0–2.48×10⁻¹⁰: the pass requires tuning the function to
   the true external field at the few-percent level, between two opposite-sign failures.
3. **Every passing member pays an RAR penalty, in its OWN best convention.** Free-Υ fits (Υ_disk scanned 0.30–1.00,
   SPARC 175 galaxies, 3389 points, binned-median χ² with per-bin SEs ≈ 0.009 dex): benchmark RAR-ν floor χ²/bin =
   5.3–5.7; published DEW α=0: 6.8–10.4 (best Υ 0.65–0.70 — the published shape is approximately RAR-viable with
   heavier disks, per the repo's convention-robustness rule this is reported as NOT RAR-dead); passing members:
   α=0.25: 13.3–13.6; α=0.6: 17.9–18.4; α=1: 19.5–21.0. The Cassini-passing zone costs 2.4–3.4× the achievable
   binned χ² floor — Desmond's "RAR demands gradual, Cassini demands sharp" trade-off realized inside the DEW
   family. (Caveat against overclaim: this is a binned-median proxy, not Desmond's full SPARC likelihood with
   per-galaxy nuisances; the full machinery would presumably sharpen, not soften, the penalty — it is the published
   3–15σ statement for this class.)
4. **Convention-robustness check (the repo's standing rule).** The strongest single rescue cell found anywhere in
   the scan: (α=0.25, a0 = 9.36×10⁻¹¹, Υ=0.7, g_ext = 2.15–2.32): passes Cassini at 0.7–0.9σ with binned-RAR χ²
   comparable to the RAR-ν benchmark *in that convention*. Reported at full weight — AND it fails at both ends of
   the g_ext range (2.0: +5.6×10⁻²⁷, 2.2σ; 2.48: −2.2×10⁻²⁷, 2.1σ), i.e. covers only the middle, pays the
   family's RAR penalty in absolute terms (χ²/bin 13.6 vs floor 5.3), and requires the framework's a0 footing
   rather than the model's own. A tuned sliver, not a viable published host.

**Why the sliver does not flip the fork:** the second branch required Q2 ≤ ~1×10⁻²⁷ *with an RAR-compatible
function* — i.e. a robust pass. No member achieves the measured-window pass robustly across g_ext, and none does so
at benchmark RAR quality. What survives is precisely the kind of object Desmond+2024 already priced: a sharpness-
tuned function trading RAR fit for solar-system safety — now with the extra DEW-specific liability that its pass is
a sign-cancellation accident of the anti-MOND overshoot lobe rather than a screening mechanism.

## §5 Consequences for the door map (hand-off)

1. **TOE_TRILEMMA fourth row update:** DEW-class status moves from "open gates" to **"decisive gate computed and
   failed for both published functions (2026 f(Z): +2.8×10⁻²⁶, 14.6σ; 2011 example2: −5.8×10⁻²⁷, 4.1σ; AQUAL, own
   a0, pre-registered g_ext); function family survives only as a g_ext-fragile, RAR-penalized, unselected tuning
   sliver"** — i.e. the perimeter sentence can be restored in the operational sense: every published covariant MOND
   host now fails a named gate. The honest footnote: this class's gate-failure is Desmond-type (function-space
   incompatibility, 3–15σ class level), not a theorem; the sliver is the residue.
2. **The Cassini-anticorrelation resolves toward MI** (agentC §3: "if Park+26's class tension holds against DEW's
   EFE, the loophole dies by the same sword as AeST while MI-proper survives it"): that conditional is now
   discharged on the DEW side. Modified inertia remains the only cell that evades Q2 by class (trajectory-dependent
   EFE; the repo's F4 Saturn check), and the missing object remains the §2-(d2)/lensing-wall hybrid.
3. **What would reopen this:** (i) a DEW-side computation of the genuinely nonlocal/history-dependent corrections
   to the static EFE showing O(1) suppression of the static quadrupole at fixed RAR — nothing in their papers
   suggests a mechanism (the static reduction is their own, and the corrections they estimate are ~10⁻⁶); (ii) a
   principled selection of the cancellation point α(g_ext) — would be a new physical postulate, not the published
   model; (iii) a major upward revision of the Q2 bound or of g_ext — Q2 has tightened 2014→2026 ((3±3) →
   (1.6±1.8)×10⁻²⁷) and g_ext is Gaia-pinned; the trend is hostile.
4. **Repo bookkeeping:** the published-DEW Q2 row belongs next to the AeST row in `FALSIFICATION_MATRIX.md` (same
   bound, same diagnostic); `CASSINI_QUADRUPOLE_CONSTRAINT.md`'s "is it generic?" section gains a fourth confirmed
   instance (nonlocal pure-metric class — fails like QUMOND-likes, unlike Galileon-k-mouflage which screens).

## Numbers ledger (for citation)

| Quantity | Value |
|---|---|
| DEW static-limit μ | μ(g) = 1 − e^{−y}(1−y/2), y = 2g/3a0 (derived; two routes) |
| Q2, published f(Z), AQUAL, a0=1.2e-10, g_ext=2.15e-10 | **+2.80×10⁻²⁶ s⁻² (14.6σ; 5.4× ceiling)** |
| Q2, same, framework a0=9.36e-11 | **+1.74×10⁻²⁶ s⁻² (8.8σ; 3.3×)** |
| Q2, QUMOND-proxy brackets | +2.26×10⁻²⁶ / +1.03×10⁻²⁶ |
| Q2, published 2011 example2 (α=1, AQUAL, own a0) | −5.8×10⁻²⁷ (4.1σ) |
| q(ẽ=1.79) DEW vs RAR-family | −0.132 vs −0.272 (validation in repo band 0.21–0.27) |
| Passing window (tuned) | α≈0.5–0.75 (own a0) / 0.2–0.3 (framework), each spanning ≲0.3×10⁻¹⁰ in g_ext |
| RAR cost of window (free-Υ binned χ²/bin) | 13–21 vs floor 5.3–5.7 (2.4–3.4×) |
| Cassini 2026 | Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻²; 2σ window [−2.0, +5.2]×10⁻²⁷ |

**Sources:** arXiv:2512.10513 (JCAP 04 (2026) 081); arXiv:1106.4984 (PRD 84, 124054); arXiv:2602.17884 (Cassini
2026); arXiv:2401.04796 (Desmond+2024, eq. 10–12, MNRAS 530, 1781); arXiv:1402.6950 (Hees+2014, Q2 convention and
function-space interval); arXiv:1510.01369 (Hees+2016, Table 2 anchors); repo: `CASSINI_QUADRUPOLE_CONSTRAINT.md`
(verified formula + audit), `reviews/aest_cassini_quadrupole_full.py` (verified q-integral),
`reviews/toe_law/agentC_covariance_memo.md` (commissioning fork).
