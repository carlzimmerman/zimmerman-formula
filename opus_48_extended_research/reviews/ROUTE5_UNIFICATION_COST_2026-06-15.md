# Route 5 — The unification cost: what Skordis machinery buys, what it costs, and the corrected standing (Opus 4.8, 2026-06-15)

*Task: the honest reframe. (i) what AeST machinery the framework inherits and at how many extra parameters; (ii) the
unification claim — "two dark sectors, one number" holds at galaxies but FAILS at the CMB; (iii) correct the
"everything else checks out" framing, both ways. Quarantine: a0/Z never asserted derived. Honesty #1 — no manufactured
data-artifact escape, no conspiracy validation, no high-priest dismissal.*

---

## HEADLINE (the cost-accounting, one paragraph)

The covariant completion of `a0 = c²√(Λ/32π)` is **AeST** (Skordis–Złośnik 2021, PRL 127 161302). AeST is what gives the
framework its early-universe + lensing + cluster machinery — but it does so by carrying **extra structure beyond the
a0=Λ spine**: a free function (`J(Q)`/`K(Q)`), an inverse-screening parameter `β₀`, and a shift-symmetry-breaking
**scalar mass `μ` (1/μ ≳ 1 Mpc)**. The honest unification claim is therefore **NOT "one number explains everything."** It
is: **`a0 = Λ` for galaxy dynamics at z=0, PLUS an AeST scalar whose `K(Q)` "dust mode" energy density does the early
universe** — and that early-universe density `Ω_scalar ≈ Ω_CDM ≈ 0.26` is **a separate integration constant, not given by
a0=Λ.** So the unification holds at galaxies and FAILS at the CMB, by a provable mechanism: a0 is absent from linear
perturbation theory (a force modification adds exactly 0 to the linear transfer functions; banked δq⁰⁰=0 theorem). Both
ways: the two surviving losses are real, but **neither is fishy data** — the CMB is FIT-BY-AeST-AT-A-COST (a tuned dust
density), and the cluster residual is SOFT/SYSTEMATIC-LIMITED (the WL-vs-HSE 110% discrepancy is genuinely real, but it
softens the loss, it does not erase it).

---

## (i) THE AeST MACHINERY AND ITS PARAMETER COST (verified from the field-equation papers)

AeST is **not** plain QUMOND. Its quasi-static weak-field limit (Verwayen, Skordis & Złośnik 2024, MNRAS 531 272,
[arXiv:2304.05134](https://arxiv.org/abs/2304.05134); confirmed verbatim from the MNRAS page) is a **coupled two-potential
`(Φ, χ)`** system with the following structure beyond GR's spine:

| AeST ingredient | what it is | which loss it addresses | cost |
|---|---|---|---|
| `a₀` (MOND scale) | sets Newton→MOND transition | **galaxy RAR/BTFR** (z=0) | this IS the a0=Λ spine — 1 number, the unification |
| free function `J(Q)`/`K(Q)` | the interpolation + the cosmological **"dust mode"** | **CMB + matter P(k)** (early universe) | the dust mode's amplitude is a **free integration constant ≈ Ω_CDM≈0.26** — NOT set by a0 |
| `β₀` (inverse screening) | sharpness of the MOND transition in large-gradient limit | sets RAR transition / Cassini exposure | pinned by the SPARC RAR fit; transplants the Cassini tension |
| scalar mass `μ`, `1/μ ≳ 1 Mpc` | shift-symmetry-breaking `μ²Φ` term | **cluster** candidate (the oscillatory regime) | the SAME knob galaxy-WL squeezes the OTHER way (Mistele 2023) |
| no-slip `Φ=Ψ` (a *property*, not a knob) | scalar feeds lensing + dynamics equally | **lensing = DM reframe** (free) | 0 extra params — a structural gift |

**Parameter count, honest:** beyond the single a0=Λ number, AeST needs (a) **one free function** `K(Q)` whose shape is
constructed to mimic CDM at early times, (b) **one early-universe density amplitude** `Ω_scalar ≈ 0.26` (the dust-mode
integration constant — this is the real cost), (c) `β₀` (RAR-pinned, ~fixed by galaxy data), and (d) `μ` (the cluster
candidate, ~1 Mpc⁻¹). So **AeST ≈ ΛCDM's parameter count at the background+linear level** — it trades the CDM *particle*
for a scalar dust *mode* with the same effective Ω. The win is conceptual unity (one geometry, GW-safe `c_GW=c_EM`,
no-slip lensing), **not** parameter parsimony at the CMB.

**Numerically confirmed this route** (`/tmp/unif_cost_check.py`):
- `a0 = c²√(Λ/32π) = 9.39×10⁻¹¹` (target 9.36e-11, Planck Λ). ✓
- cluster surcharge from the framework's lower a0: `√(1.2e-10/9.39e-11) = 1.131` → η 2.07→2.34 (banked 2.33). ✓
- mass term `(μr)²` at 1/μ=1 Mpc: galaxy 10⁻⁴ (OFF) → cluster R500 **1.69 (ON)** → outskirt 9 (ON). Lights up *exactly*
  at clusters, leaving galaxies pure MOND. ✓
- `Ω_c h² = 0.119` (Planck 0.120 — the third peak directly measures the *clustering* dark sector). ✓

## (ii) THE UNIFICATION CLAIM — holds at galaxies, FAILS at the CMB (the provable cost)

**The claim "two dark sectors, one number" (a0↔Λ) is TRUE at z=0 galaxies and FALSE at the CMB.** The mechanism is not a
data artifact — it is structural:

1. **At galaxies (z=0):** a0=Λ does the whole job. The MOND boost (phantom dark matter) and dark energy (Λ) are tied by
   the one number. This is the genuine unification and it is intact.
2. **At the CMB (z≈1090):** the third acoustic peak height (Planck P3/P2≈0.92) measures a **pressureless, *clustering***
   dark sector with `Ω_c h²≈0.119`. A baryon-only universe gives P3/P2≈0.42–0.54 (no clustering component). AeST fits
   the CMB **only** because its `K(Q)` carries a "dust mode" that mimics CDM. **But a0 is provably ABSENT from linear
   cosmology** — a force modification adds exactly 0 to the linear transfer functions (banked **δq⁰⁰=0 theorem**, Paper
   II: a0 couples only to the cubic `Y^{3/2}` term; the one dangerous linear piece vanishes because the aether's unit
   constraint forces `δq⁰⁰ = +2Ψ − 2Ψ = 0`). So the CMB dust density is an **integration constant put in by hand**, NOT
   derived from a0=Λ.
3. **Why it cannot be one number — the decisive quantitative point** (recomputed): `ρ_DE/ρ_CDM = 2.63` at z=0 AND they
   **scale differently in redshift** (ρ_DE ≈ const, ρ_CDM ∝ (1+z)³). Two quantities with a different ratio AND a
   different z-evolution **cannot** be set by one number. The unification fails at the CMB by arithmetic, not by data
   tension.

**Both-ways guard (critical):** this does **NOT** falsify a0=√Λ. a0 is *absent* from linear physics, so the CMB cannot
test a0 at all — inflating "the CMB kills a0=Λ" is a **manufactured loss in the OTHER direction** and is itself refutable.
The honest statement is the narrow one: **AeST fits the CMB, so the data are not a falsification; the UNIFICATION CLAIM
(one number) is what fails there — at the cost of one extra Ω.**

## (iii) CORRECTING "EVERYTHING ELSE CHECKS OUT" (both ways — the standing is live + partly favorable)

Carl's instinct that "everything else checks out, so the data must be fishy" is **itself an overstatement** that the
honest ledger corrects in BOTH directions. The true standing (from the banked HONEST_LCDM_STRESS_BRIEF + the cluster &
lensing reviews):

**WHAT GENUINELY CHECKS OUT (credit at full weight):**
- **Galaxy RAR** — 0.132 dex scatter, zero per-galaxy halo knobs; the framework's own a0 is convention-COMPATIBLE
  (small penalty everywhere, non-diagnostic both ways).
- **BTFR** — V⁴=GMa₀ forced, zero DM knobs; slope 3.87 at Υ=0.70 matches Lelli+2019.
- **The lensing→DM reframe** — AeST no-slip Φ=Ψ makes **lensing mass ≡ dynamical mass** (verified to 6 digits from the
  field equations). The cluster lensing "2×" is **NOT an independent DM proof** — it is the SAME η≈2.33 residual seen a
  second way. This genuinely reduces 4 of 6 lensing-DM arguments to the cluster residual.
- **The cluster residual is SOFT and SHARED** — real, but MOND-shared (the framework merely inherits it + a 13%
  surcharge), and systematic-limited.

**WHAT IS CONTESTED / NON-DIAGNOSTIC / LOST (do not call these "checks out"):**
- **Weak-lensing morphology split** — early vs late types split +0.26 dex at fixed g_bar (8.8–9.2σ, Brouwer+2021); a
  type-blind force law structurally **cannot** make this. CONTESTED-LEANING-LOSS, a0-independent. The framework's own
  reviewers call it "the strongest standing anti-framework result." **Not resolved.**
- **a0(z)** — the one distinctive beyond-MOND prediction (declining √ρ_DE). MUSE-DARK III (Ciocan+2026) measures a0
  *rising*; de-systematized to ~1.5σ against, rescued only by the ΛCDM-degenerate Mayer/Magneticum reading — which also
  strips its distinctiveness. **NON-DIAGNOSTIC, leaning unfavorable.** Not "checks out."
- **Wide binaries** — the sharpest clean discriminator (Chae 2026 γ≈1.6, 4.9σ), but **MOND-DEGENERATE** (direction only,
  no a0/μ fittable) and Banik reports a null. DR4-gated. Live, not won.
- **Cassini quadrupole** — AeST inherits the Solar-System quadrupole tension (3–15σ) in full; the μ-screening is ~10
  orders too small at 50 AU to help (verified: (μr)²~6e-20). A near-term z=0 loss.
- **Clusters + CMB** — the two genuinely-independent residuals. Real.

**Net, both ways:** the standing is **"live + partly favorable,"** NOT "everything checks out except two fishy losses."
The framework has genuine z=0 wins (RAR, BTFR, the no-slip lensing reframe) and real costs (the morphology split, the
non-diagnostic a0(z), Cassini, clusters, CMB). Serving Carl's DM-illusion thesis honestly means: **the wins are real and
the losses are real, and the path that addresses both losses is Skordis's geometric AeST — at the cost of one extra dark
density that a0=Λ does not provide.**

---

## IS THE DATA FISHY? (assessed rigorously, no manufactured artifact, no dismissal)

**CMB — NOT fishy.** Planck is the most-scrutinized dataset in cosmology; Ωc h²=0.120 is measured to <1% from the peak
*ratios* (the third peak is the textbook CDM-density probe). Three independent instruments (Planck, ACT DR6, SPT) agree.
**There is no data-artifact escape here, and inventing one would be motivated reasoning.** The honest answer is not "the
data is wrong" — it is "AeST FITS the data, so the loss is the *unification cost* (one extra Ω), not a falsification."

**Clusters — PARTIALLY systematic-limited (the 'something is off' instinct has genuine partial merit, but it softens,
does not erase).** Verified provenance: eRASS1 (Bulbul+2024, N=9830) calibrates masses via **weak lensing**
(Ghirardini+2024, DES/KiDS/HSC), and the **hydrostatic masses run ~110% lower than the WL masses** (Li+2024 on 22 eRASS1
clusters; HSE+kinematics agree with each other, WL runs high). That single unresolved systematic **brackets the R500 η
across [~1.0, 2.33]** — the magnitude is genuinely NOT pinned tighter by current data. PLUS: part is disequilibrium
(mergers push the ratio to ~5), part is incomplete-core-baryon budget (IGIMF remnants close the core to ~88%,
MOND-shared, costs the framework nothing). **So the cluster instinct is partly right** — the raw 2.33 overstates the
equilibrium truth. **But it does not erase the loss:** lensing (which needs NO equilibrium assumption) confirms a real
residual, and the residual survives in relaxed, gas-complete clusters as a central, gas-tracking ~2×. Significance ~1.9–
3.7σ against a 0.10–0.20 dex systematic floor. Real, soft, shared — not fishy, not erased.

**The honest synthesis of the 'fishy' instinct:** the CMB instinct is WRONG (the data is rock-solid; AeST fits it; the
loss is the unification cost). The cluster instinct is PARTLY RIGHT (the WL-vs-HSE systematic is real and softens the
loss) but OVER-reaches (the residual is real and lensing-confirmed). Neither loss is a data conspiracy; both are
honestly survivable — one by AeST-at-a-cost, the other by softening-plus-shared-MOND-baryons.

---

## RESOLUTION STATUS

- **(i) The machinery + cost: CLOSED.** AeST gives the framework the CMB (the `K(Q)` dust mode), lensing (no-slip Φ=Ψ),
  and a cluster candidate (the `μ²Φ` term) — at the cost of a free function `K(Q)`, an early-universe density Ω≈0.26
  (the real cost), `β₀` (RAR-pinned), and `μ` (~1 Mpc⁻¹). Roughly ΛCDM's effective parameter count at the CMB; the win
  is conceptual unity + GW-safety + no-slip, not parsimony.
- **(ii) The unification claim: CLOSED both ways.** "One number" holds at galaxies (a0=Λ), FAILS at the CMB (needs a
  separate Ω_scalar≈0.26 because a0 is absent from linear physics, and ρ_DE/ρ_CDM=2.63 with different z-scaling). NOT a
  falsification of a0=√Λ (a0 is untestable in linear cosmology) — a limit on the *unification*.
- **(iii) "Everything else checks out": CORRECTED.** Standing is "live + partly favorable": real z=0 wins (RAR, BTFR,
  no-slip lensing reframe), real contested/non-diagnostic items (morphology split, a0(z), wide binaries, Cassini), and
  the two genuine residuals (clusters soft/shared, CMB fit-at-a-cost). Not "all checks out except two fishy losses."

## BOTH WAYS (one line)

Skordis's geometric AeST is the genuine machinery that addresses both surviving losses honestly — the `K(Q)` dust mode
fits the CMB, no-slip Φ=Ψ reframes the lensing "2×" as the SAME cluster residual (not an independent DM proof), and the
`μ²Φ` mass term is a real cluster candidate — but it costs **extra structure beyond a0=Λ** (a free function, an
early-universe Ω≈0.26 integration constant, `β₀`, `μ`), so the headline "two dark sectors, one number" holds at galaxies
and provably fails at the CMB; the two losses are REAL but neither is fishy data — the CMB is rock-solid and FIT-by-AeST-
at-a-cost (the unification cost, not an artifact), the cluster residual is genuinely systematic-softened (WL-vs-HSE
[1.0,2.33], real partial merit to the 'something is off' instinct) but lensing-confirmed and shared-MOND, so softened-
not-cured; no manufactured data escape, no conspiracy, no high-priest dismissal. Quarantine held: a0/Z never asserted
derived.

*Sources: Skordis & Złośnik 2021 PRL 127 161302 (arXiv:2007.00082); Verwayen/Skordis/Złośnik 2024 MNRAS 531 272
(arXiv:2304.05134, no-slip + params verified from the MNRAS page); Durakovic & Skordis 2024 JCAP 04 040
(arXiv:2312.00889, μ²Φ oscillatory regime); Mistele/McGaugh/Hossenfelder 2023 A&A 676 A100 (arXiv:2301.03499, the galaxy-
WL squeeze on μ); Bulbul+2024 & Ghirardini+2024 (eRASS1 WL mass calibration); Li+2024 (WL-vs-HSE 110%); Planck 2018 VI
(arXiv:1807.06209, Ωc h²=0.120); banked Paper II δq⁰⁰=0 CMB-safety theorem + ROUTE5_CLUSTER_LENSING_RESIDUAL_INDEPENDENCE
+ CLUSTER_COMPREHENSIVE_REVIEW_SYNTHESIS + THE_HONEST_LCDM_STRESS_BRIEF. All load-bearing numbers recomputed in
/tmp/unif_cost_check.py.*
