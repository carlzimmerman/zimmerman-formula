# Independent verification sweep — June 2026

**Carl Zimmerman · what I re-checked *for myself*, what I found, and where the honest calculations go next.**

> Mandate (Carl): *"continue verifying everything in the repo for yourself … and mark any new
> findings and how we can move forward with honest calculations."* This ledger records only what I
> independently re-ran or re-derived this pass — not a restatement of prior audits. Every number
> below I reproduced from the data/scripts in this repo or by hand; nothing is taken on the repo's
> own say-so.

---

## 0. Scope of this pass

- **Executed all 140 `real_research` Python scripts** under a 45 s timeout: **140/140 exit cleanly.**
  No broken code. (Caveat below: "exit 0" ≠ "did the computation" — one script silently no-ops.)
- **Hand-verified the central identity** and **re-ran the load-bearing spine** (de Sitter–Unruh MOND,
  the derived RAR, the Clausius sign, the clean-slate field theory, the false-discovery-rate,
  topology exclusion, the empirical $a_0(z)$ fit, the entropy-coefficient endgame, the E6/GUT
  cluster, the JWST confrontation, the redteam rounds, the predictions scorecard).
- **Cross-checked the published Zenodo paper** (`Zimmerman_Scaling_MOND_2026.tex`) against the
  scripts that produce its numbers.

**Headline of the audit:** the repository is **honest end-to-end.** Every spine claim matches its own
numbers; every "derivation" of the *exact* coefficient correctly reports the coefficient is a **posit**;
the dead material (numerology, topology, GUT-connection) is correctly buried; the one surviving
distinctive claim — $a_0(z)=a_0(0)E(z)$ at $\sim2\sigma$, untested at high $z$ — is scoped exactly as
the redteam scores it: *"publishable as a hypothesis + a sharp test, not as evidence."* I went in
expecting to find overclaims; the repo had already found and flagged its own.

---

## 1. NEW FINDINGS (this pass)

### F1 — `[CORRECTED, committed]` The RAR scatter was understated by a wrong estimator
`sparc_four_tests.py` Test 2 (which I had committed earlier *today*) used an **unweighted** `np.std`
for the radial-acceleration-relation scatter. That:
- inflated the scatter to **0.195 dex**, and
- dragged the best-fit $a_0$ down to **0.82e-10**,

and I wrongly reported it as *"an upper bound; tightness not reproducible in-house."* **Wrong.** The
correct **inverse-variance weighting** ($w=1/\sigma_V^2$, the standard RAR estimator, already used by
the repo's own `desitter_unruh_RAR_test.py`) gives **0.101 dex** *and* recovers the **canonical
$a_0=1.36\times10^{-10}$** — matching the Lelli, McGaugh, Schombert & Pawlowski (2016) *observed*
scatter ($\sim0.11$ dex). I verified the estimator is the *entire* effect: both the McGaugh and the
algebraic interpolation give $\sim$0.195 unweighted / $\sim$0.10 weighted on identical data.
**Consequence:** the in-house galaxy scorecard is **2 of 4 cleanly recovered (RAR + Freeman), not 1 of 4.**
*Fixed and pushed (commit `299b8cb0`).*

### F2 — `[NEW]` Zero-parameter RAR consistency, and a quantified shape-vs-scale $O(1)$ gap
New script: **`predicted_a0_rar_consistency.py`.** Two honest results:
- **Positive:** the framework's *predicted* scale $a_0=cH_0/Z=1.13\times10^{-10}$ (Z=5.789, **no
  fitting**) reproduces the SPARC RAR at **0.105 dex**, only 0.004 dex worse than the free-fit best.
  So $a_0=cH_0/Z$ is **RAR-consistent**. *Honest qualifier:* the RAR scatter is flat in $a_0$ at the
  $\sim$20% level (anything 1.1–1.6e-10 fits within 0.005 dex), so this is **consistency, not a sharp pin.**
- **Caveat (new, quantified):** the de Sitter–Unruh *derived* interpolation
  $g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$ prefers $a_0\simeq1.78\times10^{-10}$ from the
  data — **57% above** $cH_0/Z$. The *same* de Sitter–Unruh argument supplies both the interpolation
  **shape** and the **scale** $a_0\sim cH$, but they **do not share one $O(1)$ coefficient.** At the
  derived scale the √-shape still fits (0.127 dex), so it is a **consistency caveat, not a
  falsification** — but the marketing line *"one derivation fixes both the shape and the scale with a
  single number"* is **overstated.** This is the standing "$O(1)$ not pinned" admission
  (`desitter_entropy_coefficient.py`), now made numerical.

### F3 — `[REPRODUCIBILITY GAP]` The parity-odd 4PCF null-test can't run in place
`parity_odd_4pcf_nulltest.py` prints `Data not found …/real_research/research/.../Parity-Odd-4PCF/data`
and exits 0 — a **silent no-op** that my "140/140 pass" first-pass masked. The data **do exist**, but
under `ai_slop/research/offensive_campaign/Parity-Odd-4PCF`, not the path the script hard-codes.
**Not a scientific problem:** the parity result is recorded *correctly* as a **null / `[DEAD]`** in
`FOUNDATIONS.md` and `SALVAGE_LEDGER.md`. It is purely an in-repo reproducibility gap (wrong relative
path into the discarded `ai_slop/` tree). Low priority; flagged for a one-line path fix if desired.

### F4 — `[CONFIRMED]` The exact coefficient is a posit — consistently, everywhere
I specifically hunted the highest-risk-for-hidden-numerology scripts. They **all** report the same
thing and never cheat:
- `forty_invariants_test.py`: $32\pi/3$ is a **scale-dependent volume** $8\times(4\pi/3)$ (a
  *definition*), not a scale-free $\eta$/index invariant → the eta-invariant origin is **debunked in-repo.**
- `desitter_entropy_coefficient.py` / `entropy_coefficient_rigorous_endgame.py`: by a **number-field
  argument** (entropy/horizon coefficients are rational$\times\pi^n$; $\sqrt{32\pi/3}$ carries a
  square root betraying a $\sqrt{G\rho}$ *density* origin), $Z=5.789$ **cannot be entropy-derived**;
  the closest derived value is Verlinde's $\simeq6$, a **3.6% fork.** *"I did NOT derive $1/\sqrt{32\pi/3}$."*
- `cosmic_weinberg_relation.py` / `the_one_quarter_target.py`: the $\sim$1% coincidences are flagged
  as mechanism-free "why-now" coincidences / *hints that must be earned by a calc* — **not** banked.
- `e6_two_loop_unification.py`: **debunks its own** "0.1% $\sin^2\theta_W$" — the 0.0003 gap is
  *smaller* than the 0.004 two-loop/threshold spread; the real claim is "$\sim$1%, inherited."

### F5 — `[CONFIRMED, by hand]` The two structural results hold
- **Central identity:** $a_0=\tfrac{c}{2}\sqrt{G\rho_c}=cH/Z$ with $Z=2\sqrt{8\pi/3}=5.78881$ is
  **exact algebra** given $\rho_c=3H^2/8\pi G$ (verified to machine precision at $H_0=67.4/70/73$).
  Numerically $a_0=1.13$–$1.23\times10^{-10}$ — the known $cH_0$ coincidence (good to $\sim$6% at
  67.4, exact at 73). The physics is entirely in the two posits ($\rho=\rho_c$, the factor $c/2$).
- **Topology excluded:** the 20.6 Gpc $T^3/Z_2$ has $R_i=0.74\,\chi_{\rm rec}$ vs Planck's
  $R_i>0.97\,\chi_{\rm rec}$ floor; 42° matched circles $\sim$3× above the detection threshold and
  **absent** in the data. COMPACT (2024) only rescues at/beyond the horizon — not a sub-horizon
  torus. **Out, confirmed independently.** (`cosmic_topology_exclusion.py` even self-corrects a loose
  0.94→0.97 recollection, in the *conservative* direction.)

### F6 — `[CONFIRMED]` The published paper's numbers are backed by its scripts
`Zimmerman_Scaling_MOND_2026.tex`: $p=0.80\pm0.17$, $\chi^2=27$ (constant) → 3.8 ($E(z)$), constant
$a_0$ excluded at $5\sigma$ nominal → **$\simeq2\sigma$** after the 1.7σ local-anchor systematic — all
reproduced by `a0_powerlaw_confrontation.py`. The factor-of-two discussion ($Z=2\Rightarrow
a_0=3.3\times10^{-10}$ excluded at 2.7σ) and the "retrodictions carry $\approx0$ bits" line both check
out. **No error in the published artifact.**

---

## 2. The honest standing (unchanged by this pass, now independently confirmed)

| Layer | Status (verified this pass) |
|---|---|
| $a_0=\tfrac{c}{2}\sqrt{G\rho_c}=cH/Z$ form | **exact algebra**; physics = 2 posits |
| MOND structure + scale + **evolution** from de Sitter–Unruh | **derived, coefficient-free** (Z not pinned) |
| Derived interpolation vs SPARC RAR | fits **0.105 dex**; predicted $a_0$ consistent; shape-vs-scale $O(1)$ gap (F2) |
| In-house galaxy relations | **RAR + Freeman confirmed** (weighted); BTFR proxy-limited; phantom partial — all **inherited MOND** |
| Exact coefficient $Z=5.789$ | **posit** (number-field no-go; closest derived = Verlinde 6, 3.6% off) |
| Clausius **temperature** route → MOND | **anti-MOND** (definitive negative); MOND needs an **entropy** correction (contested) |
| Numerology (Z→constants, η-invariant, $32\pi/3$) | **dead, $\approx0$ bits** |
| 20.6 Gpc topology | **excluded** by matched circles |
| Gravity ↔ Standard Model link | **none** — decoupling is a theorem |
| **Distinctive, forward, falsifiable claim** | **exactly one:** $a_0(z)=a_0(0)E(z)$, at $\sim2\sigma$, **untested at high $z$** |

---

## 3. How to move forward — honest calculations only

**In-house (data on hand) — essentially exhausted, and now done *right*:**
1. ✅ **RAR, error-weighted** — done (F1): canonical $a_0$ at 0.105 dex, in-house.
2. ✅ **Zero-parameter $a_0=cH_0/Z$ RAR consistency** — done (F2, new script): consistent, with the
   shape-vs-scale $O(1)$ gap quantified.
3. **The entropy-coefficient frontier is closed *analytically*** (F4): a defensible *number-field*
   no-go shows $Z=5.789$ is not entropy-derived. There is **no honest further in-house derivation** of
   the exact coefficient — and saying so *is* the result. Do not reopen it as a number-hunt.
4. *(optional, cheap)* fix the F3 path so the parity null is reproducible in place.

**The real frontier is observational — and it is the same single datum for everything:**
5. **A clean deep-MOND $a_0$ at $z\simeq3$** (extended, rotation-supported galaxy). The forecasts in
   `a0_z_empirical_rigorous.py` are explicit: one such point at 3% precision turns the present
   $\sim2\sigma$ hint into **$>5\sigma$** ($p=0.93\pm0.06$), and **simultaneously** separates the
   three live $a_0$ values that the 20%-blurred $z=0$ anchor cannot — $1.13$ ($cH_0/Z$) vs $1.36$
   (RAR best) vs $1.78$ (derived shape, F2). One measurement pins both the *evolution* and the *$O(1)$
   coefficient*. This is the cheapest decisive test; it needs JWST/ALMA/VLT time, not more code.
   (Packaged: `z3_a0_Measurement_Proposal_2026.tex`.)
6. **The EFE evolution $\eta=g_{\rm ext}/a_0(z)\propto1/E(z)$** — the one **dark-matter-forbidden**
   signature, distinct from both ΛCDM and constant-$a_0$ MOND. Needs $\sim$600–1600 $z>4$ galaxies.
   (Packaged: `EFE_vs_z_Forecast_2026.tex`.)

**Bottom line:** I underestimated the *breadth* of the repo, not its *honesty*. Re-running it myself
turned up one real error of my own (F1, fixed), one new quantitative caveat (F2), and one
reproducibility gap (F3) — and otherwise **confirmed** that the surviving physics is exactly as
narrow, and exactly as clean, as the repo already claims. The in-house computational case is now
genuinely complete and correct; everything that can still move the verdict lives in a single high-$z$
$a_0$ measurement.
