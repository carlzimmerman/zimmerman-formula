# CFG57 — the hot-gas test on SLUGGS: does each galaxy's measured X-ray gas close the globular-cluster deficit?

- **Criteria:** frozen in `CFG57_FROZEN_CRITERIA.md` (78a5a3a0a), before any gas data were fetched.
- **Sources:** fetched with the owner's approval in this session.
  - Lakhchaura+2018 (arXiv:1806.00455): the deprojected profiles of Fig. A.2, digitised from the vector figure.
  - Fukazawa+2006 (arXiv:astro-ph/0509521): Table 4, transcribed.
  - The extraction record is in `real_research/data/cfg57_gas_sources/`: the scripts, both tables, the digitisation error (stated as 0.001 dex per coordinate) and validations V1–V4. The raw sources are git-ignored; their sha256 hashes are in that README.
- **Script:** `CFG57_sluggs_hot_gas.py` (about 6 s; both footings).
  - The main run passes 15/15 and exits 0.
  - Its MUTATE control (gas × 0) exits 1, with H1 and H2 failing as required. Here the main run exits 0, so the control shows the pipeline responds to the gas.

## Bottom line

**The measured hot gas is too small to close the SLUGGS deficit, and too small to test it. By the frozen reading map the physically meaningful run is *non-diagnostic*. The pre-registered headline "pass" is an extrapolation artefact.**

- **The frozen run "passes" H1, H2 and H3, spuriously.**
  - The frozen rule extrapolates with a power law through each profile's outermost three points.
  - In three of the four Lakhchaura profiles those points include an upturned *outermost shell*. This is the standard deprojection edge effect, where the last shell absorbs the emission of gas beyond the field.
  - The fitted slopes are +2.1, +2.3 and +3.8 (row D0), which means gas density rising outward without bound.
  - Those galaxies' offsets fall to −1.8, −2.0 and −4.2 dex. The scatter balloons, and the mean (−1.07 ± 0.63, −1.7σ) lands inside 2σ.
  - The coded verdicts are kept as they fell. The mechanical reading ("the deficit is baryonic") is not true.
- **With the upturned shell dropped (D1, a disclosed post-hoc departure), the gas barely moves anything.**
  - The law goes from +0.163 to **+0.153 ± 0.028 dex** (canonical; alt +0.153 → +0.143).
  - B's derived rule goes from +0.070 to **+0.066** (alt +0.077 → +0.072).
  - The shift in the law's mean is 0.010 dex, below the mean's error of 0.028, on both footings.
  - So under D1, H1 fails (5.4σ; alt 5.1σ), H2 fails (3.0σ; alt 3.3σ) and **H3 fails**. The frozen map says: **"non-diagnostic. The gas is too small, or too uncertain at the GC radii, to decide."** The script prints this as row D3.
- **Nulling each offset with the measured profile shape** would take 20× the measured gas (NGC 3607), at least 43× (NGC 4649), or more than 100× (NGC 4365, NGC 4697). See row R1.
- **So the deficit stands as CFG55 left it.**
  - The measured hot gas is not the explanation.
  - Gas *beyond* the X-ray fields is not tested. That matters most for M87 (table below).

**Why the significance rises when gas is added:** the gas lowers the largest offset most (M87, +0.273 → +0.233), so the scatter shrinks (0.032 → 0.028) more than the mean falls.

## Sample (fixed by coverage before any offset)

- **Covered (7):**
  - Lakhchaura+2018: M87 (NGC 4486), NGC 5846, NGC 4374 and NGC 4649. These are the only four of CFG55's 16 named anywhere in that paper's text.
  - Fukazawa+2006: NGC 4365, NGC 3607 and NGC 4697.
- **Uncovered:**
  - NGC 4494. It is in Fukazawa's Table 4, but its emission stops at 5.05 kpc, so there is no n_e(10 kpc). It is reported without gas and is not in the mean.
  - NGC 3377 (disclosure). It is also in Fukazawa's Table 4, but the frozen file's coverage list omitted it. It has no n_e(10 kpc) either, since its emission stops at 1.41 kpc. It would have been uncovered either way, so the sample is unchanged.
  - The other seven of the 16 are in neither source.
- **Where both sources cover a galaxy, Lakhchaura is used** (the frozen rule). Fukazawa is the cross-check (R4, M_gas within 20 kpc):
  - NGC 5846 and NGC 4649 agree.
  - For NGC 4374, Lakhchaura's gas is 3.2× Fukazawa's (2.9× in n_e at 10 kpc, V4). The data README gives a possible cause (the Virgo background treatment); it is untested.

**The GC radii against the X-ray fields** (GC bins from h50, `hunt_2026/h50_gc_dispersions.out`; R_max at the SLUGGS distance, from this run):

| Galaxy | GC bins (kpc) | X-ray field R_max (kpc) |
|---|---|---|
| NGC 3607 | 7.6 – 19.2 | 32 |
| NGC 4697 | 2.9 – 14.8 | 24 |
| NGC 4374 | 8.3 – 22.1 | 20 |
| NGC 4365 | 4.4 – 50.0 | 45 |
| NGC 4649 | 4.4 – 39.8 | 21 |
| NGC 5846 | 8.0 – 53.6 | 32 |
| **M87** | **8.1 – 108.7** | **30** |

## Results

Mean law offset over the seven covered galaxies (dex; σ is galaxy to galaxy):

| | law, no gas | law, frozen gas | law, D1 gas | rule, no gas | rule, D1 gas |
|---|---|---|---|---|---|
| canonical | +0.163 ± 0.032 (5.1σ) | −1.07 ± 0.63 (artefact) | **+0.153 ± 0.028 (5.4σ)** | +0.070 ± 0.023 (3.05σ) | **+0.066 ± 0.022 (3.0σ)** |
| alt | +0.153 ± 0.032 (4.85σ) | −1.08 ± 0.63 (artefact) | **+0.143 ± 0.028 (5.1σ)** | +0.077 ± 0.023 (3.3σ) | **+0.072 ± 0.022 (3.3σ)** |

Per galaxy (canonical law offset, dex):

| Galaxy | no gas | frozen gas | D1 gas |
|---|---|---|---|
| **M87** | +0.273 | −4.232 | **+0.233** |
| **NGC 5846** | +0.213 | −1.951 | **+0.195** |
| **NGC 4374** | +0.200 | −1.762 | **+0.197** |
| NGC 4365 | +0.207 | +0.204 | +0.204 |
| NGC 4649 | +0.123 | +0.115 | +0.123 |
| NGC 4697 | +0.095 | +0.093 | +0.093 |
| NGC 3607 | +0.027 | +0.025 | +0.025 |

## Controls (all pass)

- **C1:** CFG55's committed offsets are reproduced with the gas set to zero, to 9 × 10⁻¹⁴ dex.
- **C2:** rows per source (80 Lakhchaura points), a Fukazawa spot value, and a digitisation method that reproduces the paper's *printed* kT and L_X to 6 × 10⁻⁷ (V1).
- **V3 (reported alongside C2).** The paper prints no per-galaxy density or gas mass, so the digitised profiles were checked against the gas masses it *plots*.
  - Cut at exactly 10 kpc, the profiles give 0.82–0.93 of those masses.
  - Summing whole shells up to and including the one containing 10 kpc gives 1.002 for all four. That scheme was found after two others fell 7–18% short.
  - So the plotted "M_gas (10 kpc)" is the mass inside that shell's outer edge (10.3–11.4 kpc).
- **C3:** the β-model gas mass integral equals its closed form (relative deviation 0 at the printed precision).

## Reported rows

- **R1, the gas needed to null each law offset** (the measured profile scaled by k; the frozen extrapolation):
  - NGC 3607: k = 20.
  - NGC 4649: k = 43, computed with the frozen slope (−0.64). D1's slope (−2.58) puts less gas outside, so D1 would need more.
  - NGC 4365 and NGC 4697: not nulled by any k ≤ 100.
  - The three upturned profiles give k ≈ 0, an artefact of the frozen extrapolation.
- **Outer slope ±0.3:** −1.25 and −0.90 on the frozen rule (R2), and +0.150 and +0.155 around D1 (D2).
- **R3, β = 0.4 or 0.6 for the Fukazawa galaxies:** a change below 0.001 dex.
- **R5, the rule's edge phantom from M_* only:** a change of 0.0002 dex.

## Caveats

- **M87 is Virgo's central galaxy.** Its GC bins reach 109 kpc (15.5 R_e), and the X-ray field ends at 30 kpc. Beyond 30 kpc, the intracluster gas here is a galaxy-scale profile extrapolated outward (D1 slope −1.48), which likely underestimates it. **For M87 alone, the gas escape is not closed.** The GCs of NGC 5846, NGC 4649 and NGC 4365 also extend beyond their fields.
- **Unmodelled:** GC orbital anisotropy (isotropy is assumed), and the Fukazawa β-model shape outside 10 kpc.
- **Metallicity.** Lakhchaura froze each galaxy's metallicity at its 10-kpc value. Underestimating it by 2× overestimates n by about 1.35× (their §2.2.5). In the two galaxies they tested, freeing the metallicity *lowered* the densities by less than 10% (their footnote 2). So this bias, if present, makes the gas smaller still.
- **μ_e.** The frozen μ_e = 1.155 is 1.3% below the paper's own 1.170.

## Disclosures (kept as they fell)

- **D0–D3 were added after seeing the digitised profiles or the first run.** They are reported rows only; no load-bearing verdict was changed.
  - D3 applies the frozen H1–H3 and the frozen reading map to D1, using the same code paths.
  - Adding it left every other line of both logs byte-identical.
- **The script prints the mechanical reading, then a labelled "DISCLOSED" line** saying the frozen extrapolation is non-physical, then D1's frozen-map reading.
- **Which quantity the figure plots.** Fig. A.2 plots the total particle density n = n_e + n_i. The table uses the paper's own conversion, n_e = 0.53 n, confirmed through the paper's entropy figure (V2, to 1e-5). That is what the frozen spec requires (n_e with μ_e = 1.155), not a departure.
- **NGC 3377's omission** from the frozen coverage list is stated above. It changes nothing.

## Reading

**By the frozen map, the physically meaningful variant is non-diagnostic.** The measured hot gas within the X-ray fields is far too small to move the law's deficit, so this test neither closes it nor tightens it. The SLUGGS deficit stands as CFG55 left it: the law under-predicts the outer GCs even with dynamical stellar masses (this subset: 5.1σ without gas, 5.4σ with; alt 4.85σ and 5.1σ).

What stays open is unmeasured mass beyond the X-ray fields, above all M87's cluster gas; this test cannot see it.

B's derived rule leaves 3.0σ with the gas (alt 3.3σ). For comparison (CFG69): ΛCDM fits the JAM-calibrated SLUGGS at 0.0σ, largely by construction, and over-predicts with population masses (−2.4σ).

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Addendum after CFG76 (appended 2026-09-29; no result changed)

- **Every offset in this lane is at CFG55's fixed GC density slope, γ = 3.**
  - The deficit's size depends on γ. For CFG55's 16, the law's offset is zero at γ ≈ 1.83 and the rule's at ≈ 2.45 (CFG76, post hoc).
  - The deficit also leans on the group and cluster centrals, four of which are among this lane's seven: M87, NGC 4365, NGC 4374 and NGC 5846.
  - So the 5.4σ and 3.0σ here are statistical errors at γ = 3. The gas shift (0.010 dex) was computed at γ = 3 only.
- **h50's name-key artefact does not change this lane's sample.** NGC 821 is in neither gas source. NGC 720 is in Fukazawa's table but lies outside ATLAS3D, so it is not in CFG55's JAM sample.
