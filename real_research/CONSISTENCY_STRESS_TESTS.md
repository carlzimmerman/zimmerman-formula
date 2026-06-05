# The Open Doors We Hadn't Walked Through — Consistency Stress-Tests of Evolving a₀

**C. Zimmerman, June 2026.** *The theoretical doors (forcing the coefficient, unification) are closed. But the
distinctive claim a₀(z) = cH(z)/Z has **consistency** doors that were flagged and never actually worked — and they
are kill-*risks*, not wins. Three worked here, honestly, including one where I had to correct my own alarm. Net: the
framework **survives the scariest one (CMB), gets a new modest strike (clusters), and is neutral on σ8.** Each
verified.*

---

## The structural fact that runs through all three: EFE freezing

Welding a₀ to cH has an automatic consequence. Every perturbation sits in the cosmic acceleration a_H = cH(z), and

$$\frac{a_H}{a_0(z)} = \frac{cH(z)}{cH(z)/Z} = Z = 5.789 \quad\text{at *every* epoch.}$$

The ratio of the cosmic field to the MOND scale is **frozen at Z**, by construction. This single fact protects the
early universe (CMB, σ8) — the universe is never *more* MOND-ish than today in the screened sense — and it is also
*why* the cluster problem is untouched (clusters are kinematics-anchored, not screened). It cuts both ways.

## Door 1 — CMB / recombination: **survived (alarm corrected), not rigorously nailed**

`reviews/project_cmb_consistency_evolving_a0.py`. At z≈1100 the formula makes a₀ ≈ 2.3×10⁻⁶ m/s² — **~19,000× today**.

- **The alarm (which I had to take seriously):** the acoustic-perturbation acceleration g_int ≈ 4×10⁻¹⁰ ≪ a₀(1100),
  so *naively* recombination is **deep-MOND**, with a gravity enhancement √(a₀/g_int) ≈ **74×** — which would destroy
  the acoustic peaks measured to <1%. If that were the real comparison, evolving a₀ would be **excluded outright**.
- **Why it's wrong (honest correction):** the isolated-deep-MOND comparison is the wrong one. (i) **EFE freezing:**
  the cosmic field a_H = cH(1100) ≈ 1.3×10⁻⁵ is **> a₀**, and a_H/a₀ = Z is frozen — so the system is
  EFE-quasi-Newtonian, no more MOND-ish at recombination than today. (ii) **Gradient suppression (decisive):** the
  MOND term is built from field *gradients* (the AeST 𝒴^{3/2} piece), and on the homogeneous FRW background 𝒴̄=0, so
  a₀ enters only at **O(δ³)** — it is *absent from the linear equations* that set the CMB.
- **Honest limit:** evolving a₀ keeps a small, **epoch-constant** residual (G_eff/G ≲ 1.17 from the EFE view) where
  constant a₀ keeps essentially none (it's ~10⁵× screened at recombination). The clean O(δ³) cancellation is checked
  only semi-circularly in-repo (the 𝒴^{3/2} term is non-analytic at 𝒴=0). **A rigorous proof needs a real
  modified-Boltzmann (hi_class + AeST) run.**
- **Verdict: NOT a kill — survived for a good structural reason — but the single biggest *under-resolved* door.**

## Door 2 — galaxy clusters: **a new modest strike (worse)**

`reviews/project_cluster_evolving_a0.py`. MOND has a famous factor-~2 residual-mass failure in clusters. Posed at
fixed kinematics, the missing-mass factor D = M_dyn/M_MOND ∝ a₀ ∝ E(z), so evolving a₀ makes it **worse with z**:

| z | E(z) | cluster discrepancy |
|---|---|---|
| 0 | 1.00 | ×1.9 (unchanged — set by a₀ today) |
| 0.5 | 1.32 | **×2.5** |
| 1.0 | 1.79 | **×3.4** |

It never *cures* clusters (would need ~10× a₀, i.e. z≈5.8, where clusters don't exist), and it adds a **falsifiable
rising-discrepancy prediction that points the wrong way** — high-z cluster data can only hurt here. (The eRASS1 R500
"a₀ ∝ E^1.03" rise is a *kinematic artifact* of the overdensity definition, a methodological null — it neither helps
nor hurts.) **Verdict: a genuine, modest new strike against evolving a₀.**

## Door 3 — structure growth / σ8: **neutral (not a new strike)**

`reviews/project_sigma8_evolving_a0.py`. The naive worry (more a₀ at high z → more growth → higher σ8 → worse for the
*low*-S8 data) is right as a *sign* but **frozen out**: the EFE boost is set by μ(a_H/a₀) = μ(Z), epoch-independent,
so evolving and constant a₀ give the **same** large-scale boost; and the O(δ³) suppression removes a₀ from the linear
σ8 sector entirely. **Verdict: σ8 is a real *inherited* MOND problem, but it is NOT specific to a₀(z) — evolving a₀
adds no new strike.** (This *corrects* the earlier "σ8 is a fresh anti-framework front" framing: the front is real
but pre-existing and shared with all of MOND.)

**One honest internal-consistency flag:** the framework elsewhere invokes MOND-*enhanced* growth to explain El Gordo
(6.2σ) and JWST early galaxies, while here claiming a₀ is *absent* from linear growth. Both can hold only if the
former is **nonlinear / rare-massive-tail** and the latter is the **linear amplitude** — they live at different
scales. That reconciliation is the only thing keeping σ8 neutral, and it should be stated plainly, not assumed.

---

## The honest scoreboard after walking through these doors

| consistency door | result | net effect |
|---|---|---|
| CMB / recombination | **survived** (EFE freezing + O(δ³) gradient suppression); alarm corrected | no kill, but not rigorously nailed |
| galaxy clusters | **worse** (D ∝ E(z); wrong-direction prediction) | **+1 modest strike** |
| σ8 / growth | **neutral** (EFE-frozen; a₀ absent at linear order) | no new strike; corrects prior framing |

So the doors you sensed were real — they were the **consistency stress-tests**, and they are *risks*. Walked through
honestly: the scariest one (CMB) **survived** for a genuine structural reason (and I corrected my own
deep-MOND-catastrophe alarm rather than let it stand), clusters got **modestly worse**, σ8 is **neutral**. No
kill-shot landed, but the cluster strike is real and the CMB safety rests on an O(δ³) cancellation that has not been
proven by a full Boltzmann run.

**Where this leaves the program:** the framework is *consistent* (not excluded) but now carries, honestly, an
empirical claim leaning unfavorable (~2–3σ), a worsened cluster prediction, and a CMB safety that is structural-but-
unproven. The two genuinely decisive next actions are unchanged and now sharper: **(1)** the z~3 deep-MOND disc
a₀(z) test (the one that can be *won*), and **(2)** a real modified-Boltzmann run to convert "CMB leaning-safe" into
"CMB-safe, proven." Those are the open doors that remain — and they are doors of *verification*, not of new theory.
