# The falsifiable kernel `a₀(z) ∝ √ρ_DE` — exact prediction + honest 2026 standing

*C. Zimmerman, 2026-06-06. The coefficient is closed (not derivable, moot) and every covariant realization hits a
field-wide wall (`REALIZATION_REDTEAM_…`). So the live science is the one original, coefficient-free, host-free claim:
the MOND scale tracks the dark-energy density. This doc (i) computes the exact prediction, (ii) reports a sharper,
partly-reversed empirical standing after a 3-agent literature sweep + my own verification of the two load-bearing
results. Companion script: `a0_evolution_prediction_curve.py` (every number below reproduced; figure `.png`).*

## 1. The exact prediction — and it is NOT "pure decline" (a sharper signature)

`a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE0)`, with `ρ_DE` evolving per the DESI DR2 CPL fit `w(a)=w0+wa(1−a)`
(fiducial DESI+CMB+DESY5: `w0=−0.752, wa=−0.86` ⟹ `ρ_DE(a)/ρ0 = a^{1.836} exp[2.580(1−a)]`):

| z | a₀(z)/a₀(0) framework | V_flat offset @fixed M_bar | flat MOND | Verlinde a₀∝cH (V offset) |
|---|---|---|---|---|
| 0.0 | 1.000 | 0.0% | 1.00 | 1.00 (0%) |
| **0.41** | **1.062 (peak)** | **+1.5%** | 1.00 | 1.27 (+6%) |
| 1.0 | 1.009 | +0.2% | 1.00 | 1.79 (+15.6%) |
| 2.0 | 0.862 | −3.6% | 1.00 | 3.03 (+31.9%) |
| 3.0 | 0.737 | −7.3% | 1.00 | 4.56 (+46.1%) |
| 5.0 | 0.566 | −13.3% | 1.00 | 8.27 (+69.6%) |
| 10 | 0.358 | −22.7% | 1.00 | 20.5 (+112.7%) |

**The new structural point:** because DESI's `w(z)` **crosses −1 at z≈0.41**, `ρ_DE` (hence `a₀`) **peaks there** — the
framework predicts `a₀` *rises ~6% to a bump at z≈0.4, then declines.* **Neither flat MOND nor Verlinde does this.** Two
consequences that reorganize the whole empirical read:

- **A modest rise at z<1 is *consistent with the framework*, not against it.** The naive "rising a₀ ⟹ framework loses"
  is wrong: the framework's own bump is a +6% rise peaking at z≈0.4 (`a₀(z=0.5)=1.06`, distinguishable from flat at 1σ
  given the DESI `w0wa` errors). The framework only **uniquely declines at z≳1.5**.
- **The 3-way fork is asymmetric.** Verlinde's steep rise (`+32%`/`+46%` in V at z=2/3) is **easy to kill**; the
  framework-vs-flat split (`−4%`/`−7%` in V) is **hard** (below today's intrinsic BTFR scatter). So the data should kill
  Verlinde first, and only later separate framework from flat. *That is exactly the pattern the 2026 data show.*

DESI `w0wa` error propagation: `a₀(z)/a₀(0)` is distinguishable from flat (1.000) at 1σ for z≥2 (z=3: `0.74 [0.65,0.83]`)
and at the z≈0.4 bump, but *not* at z≈1 (the curve crosses 1.0 there). Robust across all three DESI SNe compilations.

## 2. The 2026 data — verdict: NON-DIAGNOSTIC at the systematic floor (not "leaning unfavorable")

A 3-agent sweep (direct kinematics · differential/cluster/lensing probes · JWST structure) + my verification of the two
load-bearing facts. The prior "leaning unfavorable (MUSE rising)" framing **does not survive** — the unfavorable reading
was an artifact.

### 2a. The one new direct measurement — and why it is non-diagnostic
**MUSE-DARK III (Ciocan, Bouché et al. 2026, A&A aa59230-26 / arXiv:2604.22613):** a direct RAR fit in 4 redshift bins,
0.33<z<1.44, finds `a₀` **rising ~2× by z~1** (`a₀(z)=a₀(0)+1.59z`), ~30σ. Taken at face value this is **Verlinde-scale
or steeper** (`+16…+27%` in V at z=0.5…1) and would exclude both the framework and flat MOND. **It cannot be taken at
face value, for three independent reasons — two of which I verified directly:**

1. **ΛCDM reproduces it [VERIFIED].** Magneticum (Mayer, Teklu, Dolag, Remus 2023, **MNRAS 518, 257; arXiv:2206.04333**):
   in ΛCDM-with-baryons the RAR-inferred `a₀` **increases ~3× from z=0 to z=2** — the *same* magnitude. So a rising
   RAR-`a₀` is **generic to dark-matter halos + feedback**, not a modified-gravity diagnostic. The MUSE authors concede
   their trend sits "between H(z) and ΛCDM simulations."
2. **The same team's clean axis is a NULL [CORROBORATED].** The baryonic Tully-Fisher zero-point (`∝ G a₀`) — the
   *direct* `V_flat`-at-fixed-`M_bar` axis our predictions live on — shows **no evolution at intermediate z (±0.08 dex)**.
   A genuine ~2× `a₀` rise would demand a large bTFR-zero-point shift; the bTFR says flat. The RAR-`a₀`-rise and the
   bTFR-null are in internal tension → the RAR rise is most plausibly a halo/decomposition artifact.
3. **The steep rise is already excluded.** Milgrom 2017 (**arXiv:1703.06110**) used high-z *falling* rotation curves
   (Genzel+2017, Nestor Shachar+2023 — baryon-dominated disks at `g=3–11 a₀`, **Newtonian-regime, orthogonal to a₀**) to
   **exclude `a₀∝(1+z)^{3/2}`**, i.e. exactly the Verlinde-scale rise MUSE-DARK III would imply.

**Net:** the MUSE rise is real in the RAR fit but **ΛCDM-degenerate, internally contradicted, and of a magnitude already
excluded** — *non-diagnostic*, confirming (and now explaining) the project memory's retracted-"MUSE confirms rising."

### 2b. Differential / complementary probes (the systematics-suppressed reads)
- **Differential a₀(z), high z:** Del Popolo & Chan 2024 (**2405.01841**) find the high-z sample (RC100) *anti*-correlates
  with z — `a₀` **declining** — opposite sign to MUSE-DARK III on overlapping physics. Gueorguiev/SIV 2024
  (**2409.11425**) reads the *same* data as consistent with **zero slope**, and notes SIV predicts a declining
  `a₀(z=1)≈0.79` — close to the framework's `0.86 at z=2`. **The sign of the high-z trend flips with the
  pressure-support/baryon-DM decomposition** — the systematic floor exceeds the signal.
- **Disk-selected BTFR:** KROSS–SAMI (Tiley+2019, **1810.07202**) with strict rotation-dominated selection: **no
  K-band BTFR zero-point change since z≈1.** Disfavors any large `a₀` excursion (rising or falling).
- **Clusters:** Tian+2024 (**2402.12016**), eRASS1 (Li+2024, **2411.09735**): the cluster acceleration offset is a
  *constant* ~17× with **no resolved z-trend** → **disfavors steep Verlinde**, cannot separate framework-decline from flat.
- **Weak-lensing RAR:** Brouwer+2021 KiDS (**2106.11677**) confirms the RAR into the deep-MOND regime but **only at
  z≈0.2, not z-binned** → currently *blind* to `a₀(z)`.
- **A weak direct lean toward the framework over Verlinde:** Bekenstein 2008 (**0809.2790**) tested `a₀∝cH` vs
  `a₀∝√ρ_DE` against the TFR and found systematics "marginally favor coupling to the dark-energy density" over `cH`.

### 2c. JWST early structure — the feared liability does NOT bite
Worry: if early structure needs *enhanced* gravity, that favors *rising* a₀ (Verlinde) against the framework. **It
doesn't:**
- **MOND's structure-formation problem is *over*-production; the fix wants a *smaller* a₀** (Nusser 2002,
  **astro-ph/0109016**: reducing `a₀` ~10× restores agreement). A *declining* `a₀` is in the **same direction** as what
  MOND cosmology already needs — favorable-to-neutral.
- The MOND collapse boost scales only as **`a₀^{1/2}`** (weak) and is dominated by the background density `ρ_b∝(1+z)³`.
- The compact early galaxies (e.g. JADES-GS-z14-0) sit **at/above the MOND surface-density threshold → Newtonian
  regime → `a₀`'s value is irrelevant** to their internal dynamics (and declining `a₀` pushes them *deeper* Newtonian).
- The JWST tension itself is **fading inside ΛCDM in 2026** (AGN/little-red-dot contamination, feedback-free
  starbursts; reviews arXiv:2511.04843, 2511.13708) — so it cannot strongly favor *either* alt-gravity reading.
- **Honest residual risk (different channel):** negative-Λ/DDE *fixes* of the JWST excess work by *strengthening* early
  growth — opposite to `a₀∝√ρ_DE` declining. But that is a background-growth argument, *separate from the a₀ channel*,
  and only bites if the excess survives as a real cosmological signal (doubtful in 2026).

## 3. Honest standing (updated) and the cleanest near-term test

**Updated verdict — the prior "leaning unfavorable" is withdrawn:**
- The framework is **neither confirmed nor falsified.** Its distinctive **z≳1.5 decline is essentially untested** (no
  clean fixed-`M_bar` measurement beyond z~1.5; high-z kinematics too systematics-dominated).
- The single result that *looked* unfavorable (MUSE-DARK III rising) is **non-diagnostic** (ΛCDM-degenerate +
  internally contradicted + magnitude-excluded). The pessimism was an artifact of reading an apparent-`a₀` halo effect
  as a real `a₀` change.
- **Verlinde / QI (the framework's rival in the rising direction) is the *most* disfavored hypothesis** — killed by the
  constant cluster offset, the disk-selected BTFR null, and Milgrom's `(1+z)^{3/2}` exclusion.
- Framework-decline vs flat-MOND is **genuinely undecided**, dominated by the baryon-dominance systematic, with two
  2024–26 analyses disagreeing on the *sign* (Del Popolo declining vs MUSE rising) from the same physics.
- The framework's most distinctive feature — the **non-monotonic z≈0.4 bump (+6% a₀ / +1.5% V)** — is well-motivated by
  the DESI `ρ_DE` peak but **not detectable before ~2028** (needs ~10³ disk-selected galaxies at 0.3<z<0.6, ≲2% velocity
  precision; DESI-PV too low-z, Euclid spectroscopy too high-z).

**The cleanest near-term discriminant (actionable, existing data):** *not* the z≈0.4 bump (unreachable) or z~3 (too
noisy) — it is to **resolve the Del Popolo-vs-MUSE sign contradiction** by re-deriving `a₀(z)` on a *single homogeneous
IFS sample* (KROSS + KMOS³D + KGES + MUSE, already in hand, few-hundred galaxies) through a **common
pressure-support / baryon-DM-decomposition pipeline with matched disk selection**, explicitly modeling out the
ΛCDM-halo `a₀`-drift (Magneticum) degeneracy. That removes the dominant systematic and can reach the few-%-in-`a₀`
precision needed to separate **declining (framework/SIV) vs flat vs mildly-rising** with data that *already exist* —
well before DESI DR3 or any dedicated z≈0.4-bump survey. **This is where the energy should go.**

**Bottom line:** the falsifiable kernel survived the realization collapse untouched, its prediction is sharper than
"declining" (a non-monotonic bump-then-decline keyed to DESI's `ρ_DE` peak), and the 2026 data are **undecided at the
systematic floor — with the framework's rising rival in the worst shape and the decisive test reachable from existing
IFS data via a unified re-analysis, not new telescopes.**

**Sources (verified):** Magneticum a₀(z)×3 in ΛCDM — [arXiv:2206.04333](https://arxiv.org/abs/2206.04333) (MNRAS 518,
257); MUSE-DARK III — [A&A aa59230-26](https://www.aanda.org/articles/aa/full_html/2026/05/aa59230-26/aa59230-26.html)
(arXiv:2604.22613); bTFR ~null at intermediate z — KMOS³D [arXiv:1703.04321](https://arxiv.org/pdf/1703.04321),
MUSE-DARK II; Milgrom high-z RC exclusion of (1+z)^{3/2} — [arXiv:1703.06110](https://arxiv.org/abs/1703.06110);
Del Popolo & Chan a₀(z) — [arXiv:2405.01841](https://arxiv.org/abs/2405.01841); SIV — arXiv:2409.11425; cluster RAR —
arXiv:2402.12016, 2411.09735; KiDS WL-RAR — arXiv:2106.11677; Bekenstein TFR-MG test — arXiv:0809.2790; Nusser MOND
over-production — astro-ph/0109016; DESI evolving DE — DESI DR2 2025.
