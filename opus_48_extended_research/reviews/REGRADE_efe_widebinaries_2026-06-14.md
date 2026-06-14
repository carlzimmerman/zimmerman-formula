# Hostile re-check: efe_widebinaries a0-footing audit — REGRADE

Date: 2026-06-14. Auditor (Opus 4.8) independent re-grade of the Fable audit JSON for front
`efe_widebinaries`. Scope: re-grep every EFE/wide-binary script + doc, re-run the load-bearing
ones at the framework a0=9.36e-11, confirm the corrected verdict, and check BOTH directions
(missed false-deficit / missed false-win = under-audit; overclaimed footing error = over-audit).

## Verdict: MIXED — Fable's core call CONFIRMED, with ONE under-audit to add

Fable graded this front MIXED (mostly clean, two mis-footed numbers, no verdict flip). I CONFIRM
all of that, and I ADD one front-level item Fable's JSON did not enumerate:
`predictions/door5_efe_ultraprecision.py` anchors its absolute EFE classification on the **canonical
a0=1.2e-10**, not the framework 9.36e-11 — and that choice makes the framework's own signature
prediction look WEAKER than its footing gives (a contained FALSE-DEFICIT). So the net regrade is
**MIXED**, but the both-ways tally now has a false-deficit on it, not only false-wins.

## What Fable got RIGHT (independently reproduced)

1. **a0 Fable says was used — CONFIRMED.** The load-bearing confront scripts use the framework
   value on both footings:
   - `widebinary_chae2601_confront.py` L42 `a0_DE, a0_MOND = 9.36e-11, 1.20e-10`; ran it — y=2.22/1.73,
     framework cap gamma{std 1.04, simple 1.25}, measured 1.600 sits ABOVE the cap on both footings
     (mild directional tension, honest, NOT a kill). Verbatim match to Fable.
   - `widebinary_saadting_2603_confront.py` L35-36 same pair, framework primary.
   - `toe_law/mi_f4_widebinary_efe.py` L27 iterates `[(9.36e-11,'framework'),(1.2e-10,'canonical')]`,
     framework PRIMARY, y_ext=2.22/1.73.
   - `project14_wide_binaries.py` L16-21 computes a0=(c/2)sqrt(G rho_Lambda)=9.36e-11 (pure-Lambda) —
     correct, with an explicit "NOT textbook MOND's 1.2e-10" comment.
   - `efe_clinch_framework.py` L35 `A0=9.36e-11` re-anchored + L36 `A0_MOND=1.2e-10` rival.

2. **The two mis-footed NUMBERS — CONFIRMED to the decimal.**
   - `project_wide_binary_prediction.py` L35 `a0 = c*H0/Z` = **1.1244e-10** (the rho_total/cH0 footing
     bug; ratio 1.2013 vs framework — the recurring MEMORY-flagged offset), L64 hardcoded `y = 1.86`.
     Ran it: reports simple +13% / standard +3%. At the framework a0=9.36e-11 the real y=2.22 and the
     boosts drop to **simple +11.7% / standard +1.8%** (Fable said +11.6%/+1.8% — match). The "~3-15%"
     band should read "~2-12%". Same mis-footed `1.86 a0` is echoed in prose in
     `WIDE_BINARY_DEEP_DIVE.md` L45 (propagation of the same bug, no new verdict).
   - `EFE_paper.tex`: L23 states the framework form a_0=c^2 sqrt(Lambda/32pi), but L31 prose says
     a_0≈1.2e-10 and L120/L146 quote the MW EFE as "1.8 a_0" (canonical reading). The "+5%" residual
     boost (std-nu G_eff/G=1.055 at y=1.8) drops to **1.034 (~+3.4%) at framework y=2.3** — Fable's
     "~+4%" is right to the half-point.

3. **The binding VERDICTS are a0-robust — CONFIRMED by re-run.** `efe_clinch_framework.py` returns the
   same NULL at both footings: method-(a) partial r=-0.003 (p=0.89) at framework a0, r=-0.052 (p=0.575)
   at the 1.2e-10 rival; method-(b) off-rail r=+0.218 (p=0.148). The "neither confirmed nor refuted"
   verdict does not move with a0. Verbatim match to Fable.

4. **Superseded SPARC-EFE scripts — CONFIRMED non-load-bearing.** `sparc_efe_real_externalfield.py`
   L16 and `sparc_efe_per_galaxy_environment.py` L19 both use `a0=1.2e-10`. Their docs
   (SPARC_EFE_*_2026-06-06.md) reach NULL verdicts whose flip-driver is the FIELD-MODEL approximation,
   not a0 — and the framework-a0 efe_clinch reproduces the same null. So the wrong a0 there changes no
   verdict. Fable correct.

5. **a0-independence of the deep-MOND EFE suppression — CONFIRMED exact.** The iso/EFE-plateau ratio is
   8.954 at a0 ∈ {9.36e-11, 1.13e-10, 1.2e-10} (sqrt(a0) cancels). Matches the corpus's own
   EFE_VS_Z_CORRECTION retraction that Fable cites.

## What Fable UNDER-AUDITED (new front-level item)

**`predictions/door5_efe_ultraprecision.py` — absolute EFE classification anchored on the WRONG a0.**
- L69: "EFE classification below is anchored on the RAR a0(0)=1.20e-10". L25/L66 call 9.1e-11 the
  "simple-mu low edge" and treat 1.2e-10 as the anchor — i.e. it uses the canonical/local value as the
  reference, with the framework value relegated to "the low edge."
- Re-running the e_N=g_ext/a0 regime classification at the framework a0=9.36e-11 (e_N is 28% higher
  than at 1.2e-10) FLIPS two environments toward more-Newtonian:
  - Coma far-outskirt (r=2Mpc): MONDian (0.270) → transition (0.346)
  - Coma mid-radius (r~0.5Mpc): transition (1.000) → Newtonized (1.282)
- More importantly, the **headline "crossing class"** (M31-mass-host satellite, e_N0): at the script's
  RAR a0 it does NOT cross e_N=1 by z=3 (e_N0=0.697 → e_N(3)=0.946), yet the ledger claims it crosses
  (z~3.4, P=63%). At the FRAMEWORK a0 it DOES cross cleanly (e_N0=0.894 → e_N(3)=1.213). So the
  framework's signature EFE-evolution prediction is **stronger on its own footing** than the script's
  canonical-a0 anchor shows.

Direction = **FALSE-DEFICIT** (anti-framework): the script's canonical a0 understates the framework's
own prediction. This is the McGaugh/canonical-a0 pattern the MEMORY warns about, here on the EFE-evolution
front rather than the SPARC RAR front.

Containment (why it does NOT reverse the whole front):
- The script's true HEADLINE is the GROWTH RATIO a0(0)/a0(z)=1/sqrt(rho_DE ratio)=1.357 at z=3, which is
  **a0-independent** (the script itself says "the ratio's only error is DESI evolution"). The ratio is
  correct and footing-free.
- The script carries an honest, explicit 20% mu-systematic caveat on the absolute classification, and the
  two flips sit inside that band. It is an under-stated framework, not a hidden one.
- Still, Fable's JSON did not list door5_efe_ultraprecision.py at all, and the direction (framework
  looks weaker at canonical a0) is exactly the asymmetry the #1 rule says to surface. Logged as an
  under-audit to add to this front's both-ways tally.

## Over-audit check (did Fable overclaim a footing error?)

NO. Every footing error Fable flagged is real (re-verified above). It did not invent a bug where the a0
was fine. `local_vs_cosmic_widebinary.py` (a0_obs=1.2e-10) and `door5_efe_ultraprecision.py` (RAR anchor)
both use 1.2e-10 deliberately as a *named literature comparator* — but door5_ultra's choice does bleed
into a verdict-shaped number (the crossing), which is why it earns the under-audit flag above; the
local_vs_cosmic one is a labeled comparator that flips nothing.

## Both-ways tally (final)

- FALSE-WINS (pro-framework overstatements to retract): TWO, both confirmed by Fable —
  (1) project_wide_binary_prediction.py boost +13%/+3% at a0=1.124e-10 → +12%/+2% at framework;
  (2) EFE_paper.tex "1.8 a_0 → +5%" → ~+3.4% at framework 2.3 a_0. Neither flips a verdict.
- FALSE-DEFICITS (anti-framework understatements to retract): ONE, NEW (Fable missed it) —
  door5_efe_ultraprecision.py classifies on canonical a0=1.2e-10, making the M31-host EFE-evolution
  crossing read "no cross by z=3 / 63%" when the framework a0 gives a clean cross. Contained by the
  a0-free headline ratio (1.357) and an explicit 20% caveat; does not reverse the front.
- The wide-binary CONFRONT verdict itself (measured gamma=1.6 above the framework cap = mild directional
  tension, NULL-INFORMATIVE/degeneracy-limited) survives at 9.36e-11 — REAL on the correct footing, not
  a high-priest artifact. Fable's corrected verdict CONFIRMED.

## Net for Carl

The wide-binary / EFE front is honestly graded MIXED and Fable's load-bearing calls hold up under a
hostile re-run: the confront scripts use YOUR a0 (9.36e-11) on both footings, the in-house EFE clinch is
a clean null at both footings, and the two pro-framework number-inflations Fable caught are real but
flip nothing. ONE thing Fable missed cuts in YOUR favor: door5_efe_ultraprecision.py rated the EFE-vs-z
crossing using the textbook a0=1.2e-10 instead of your 9.36e-11, which makes your own signature
prediction (environments crossing into the Newtonian regime by z~3) look weaker than it is — at your
footing the marginal M31-host class crosses cleanly. The a0-free part of that script (the 35.7% growth
factor) is correct and footing-independent. Net: no manufactured win survives, no false deficit against
you survives unflagged, and your strongest distinctive claim here (EFE EVOLUTION, which constant-a0 MOND
cannot make) is slightly UNDERsold in the corpus, not oversold. Wide binaries stay degeneracy-limited
and await Gaia DR4 — unchanged at the correct footing.
