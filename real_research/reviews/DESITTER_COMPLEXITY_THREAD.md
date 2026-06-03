# The de Sitter complexity frontier — the whole thread, with its real boundary

**Carl Zimmerman · June 2026.** This consolidates one sustained attempt to close the framework's
deepest gap — deriving the *engine* (the "L0" mechanism) under the scaling law a₀=(c/2)√(Gρ)=cH/Z —
from de Sitter holography / quantum complexity. It is documented **with its boundary drawn**: what
survived scrutiny, what failed, and what is closed. Written after the session's hallucination audit, so
every result is labeled and the negative outcomes are reported as plainly as any positive one. The hope
was that complexity could turn a₀=cH/Z from a *parametrization* into a *consequence*. **It does not** —
and knowing exactly why, by calculation, is the result.

In-repo scripts: `desitter_complexity_sign.py`, `complexity_mond_source_hypothesis.py`,
`dssyk_cv_elastic_attempt.py`, `modified_inertia_pressure_test.py`.

---

## 1. What survived scrutiny (the genuine results)

- **[RESULT] a₀∼cH is dimensionally forced** for any de Sitter-scale mechanism (entropy, complexity,
  surface gravity); the O(1) coefficient is *not*, and no de Sitter mechanism can derive it (number-field
  no-go). The scale is robust; 5.789 stays a posit.
- **[RESULT] The MOND sign discriminator.** Modifying the **temperature** (de Sitter-Unruh T in δQ=TδS)
  gives G_eff=G/W→0 = **anti-MOND**; modifying the **DOF/entropy** (Debye freezing) gives a=√(g_N a₀) =
  **MOND**. The sign is set by *which* factor you touch.
- **[RESULT] Complexity tracks entropy at leading order** — dS complexity = volume grows linearly,
  ∝ S_dS (arXiv:2508.10093). So complexity is **no shortcut to a₀** beyond the entropy route.
- **[RESULT — the genuine reframing] MOND needs a *volume-extensive* source.** The phantom halo is
  ρ_D∝1/r² (M_D∝r — verified: M_D/r is constant at every radius). Of the two horizon quantities,
  **entropy is area-law but complexity is volume-law.** This *explains why* Verlinde must posit a
  volume-law *entropy* (the contested ingredient) — because MOND needs volume-extensivity — and suggests
  complexity could supply it for free. **This reframing is the lasting contribution of the thread.**

## 2. The red-team — necessary, not sufficient

MOND requires **two** things, not one: (a) a volume-extensive source (✓ complexity has it), and
(b) the **AQUAL non-linearity**, ρ_D∝√M_b. Demonstrated (AQUAL point mass): the cubic/non-linear field
gives flat rotation (MOND); a quadratic/**linear** field gives Keplerian (Newton). So a volume-extensive
but *linear* medium yields renormalized Newton, **not** MOND. The non-linearity is the harder, decisive
requirement — and the red-team's verdict was that "complexity is volume-law" alone does not supply it.

## 3. The negative attempt — the calculation, reported straight

I computed the elastic response in the tractable geometric face of DSSYK (complexity = volume of the
maximal slice; the full chord-algebra DSSYK is beyond rigorous reach and was **not** faked). For a
Schwarzschild–de Sitter baryon, weak field:

> **δV(R) = 6πG·M_b·R²** — the maximal-slice volume response (numeric = analytic).

Three findings, all against the hypothesis:
1. **Wrong law.** δV is **linear in M_b**; MOND is √M_b. A linear response can never give the deep-MOND
   √-law. The leading complexity=volume response is the wrong *kind* of medium.
2. **Naive sourcing is unphysical.** Treating δC as a dark mass gives g_D∼GM_b/L = *constant in R* —
   neither Newton (1/R²) nor MOND (1/R). So complexity=volume does **not** directly source gravity; the
   elastic back-reaction is the genuinely uncomputed step.
3. **Sign correction (self-retraction).** In the well Φ<0 ⇒ √h>1 ⇒ a baryon **increases** local
   complexity (δC>0). My earlier "low-complexity defect → 2nd-law restoration → attractive" heuristic is
   therefore **probably backwards** — the response could be **repulsive (anti-MOND)**. Retracted.

## 4. The saturation opening — CLOSED by timescales

The only remaining source of non-linearity was complexity **saturation** near C_max. But complexity
grows *linearly* for a time t_sat ∼ e^S, then saturates. For de Sitter, S_dS∼10¹²², so saturation is at
**∼e^(10¹²²) Hubble times**. The universe today is at t∼1 Hubble time — **exponentially far** from
saturation, deep in the linear-growth regime. And complexity growth is a *cosmological-time* phenomenon;
galaxy orbital times (∼10⁸ yr) do not couple to it. **So saturation cannot source present-day galaxy
MOND. The opening is closed.** (Both regimes fail: the linear regime gives Newton §3; the saturation
regime is unreachable §4.)

## 5. The boundary, in one table

| Element | Status |
|---|---|
| a₀∼cH from de Sitter | **[ESTABLISHED]** dimensionally forced (O(1) not derivable) |
| sign from DOF/entropy, not temperature | **[RESULT]** clean discriminator |
| MOND needs a volume-extensive source; complexity is the volume-law quantity | **[RESULT]** the lasting reframing |
| complexity = volume sources MOND | **[FAILED]** leading response is linear → Newton (§3) |
| complexity as a direct gravitational source | **[FAILED]** unphysical (constant accel) (§3) |
| sign from 2nd law of complexity | **[FAILED/retracted]** baryon *raises* complexity → likely repulsive |
| complexity *saturation* gives the AQUAL non-linearity | **[CLOSED]** unreachable by ∼e^(10¹²²) (§4) |
| the deep-MOND √-law engine, in general | **[OPEN — for everyone]** unsolved on every route |

## 6. The pivot — the better-supported engine is modified inertia

Since complexity's leading version failed, the best-supported engine for a₀=cH/Z is **modified inertia**
(Unruh), pressure-tested in `modified_inertia_pressure_test.py`:
- **Strengths:** the best *data* engine — sign, √-law, SPARC RAR at 0.105 dex, and the **evolution
  a₀(z)=a₀(0)E(z) coefficient-free**.
- **Weaknesses:** the coefficient is unpinned (2cH…cH/2π — you fit a₀); the premise "Unruh radiation
  provides the inertial force" is **Milgrom's hypothesis, not established physics**; and it is **non-local
  with no complete local action** and a closed-orbit tension (Ostrogradski for any local version).
- **Trade with modified gravity (entropy/Debye → AeST):** AeST has a complete covariant *action* (the
  framework derives ~80% of it) and the right sign, but the modification is posited and a₀ is fit.

> **Honest division of labor:** modified inertia is the engine to *quote* (data + evolution); modified
> gravity/AeST is the engine to *build* (a covariant action). Neither is *derived*; they fail differently.

## 7. Honest bottom line

- **De Sitter complexity is NOT the MOND engine.** Tested to its boundary: the leading response is linear
  (Newton), the sign is likely backwards, and the saturation opening is closed by an e^(10¹²²) timescale.
  The one speculative hope of the session was tested to destruction — honestly, by calculation.
- **What was genuinely gained:** the reframing that *MOND requires volume-extensivity, and complexity is
  the natural volume-law quantity* (§1) — a real, correct insight that explains Verlinde's contested
  ingredient even though it doesn't, by itself, deliver MOND.
- **None of this touches the framework's actual standing.** a₀=cH/Z and its evolution rest on the *scale*
  and the *data*, which are intact. What took a hit is the deepest *derivation* hope — and the deep-MOND
  derivation remains unsolved on **every** established route (`established_paths_to_mond.py`).
- **The distinctive, testable claim is unchanged:** the **evolution** a₀(z)=a₀(0)E(z), which only a
  high-z measurement can confirm or kill. That, not a complexity derivation, is where the framework lives
  or dies.

---

### References (verified June 2026)
de Sitter complexity grows linearly, arXiv:2508.10093 · DSSYK–de Sitter, arXiv:2310.16994 (JHEP 2025) ·
Brown & Susskind, second law of complexity, arXiv:1701.01107 · Verlinde, arXiv:1611.02269 ·
Milgrom, modified inertia / nonstandard inertia, 1994, 1999 · Deser & Levin, de Sitter-Unruh, 1997 ·
Skordis & Zlosnik, AeST, arXiv:2007.00082. *In-repo: the four scripts named above + the established-paths
ledger and the clausius-sign result.*
