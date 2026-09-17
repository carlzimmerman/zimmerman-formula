# GAME PLAN — the framework's own fingerprint: an external-field effect with magnitude but no direction (2026-09-17)

**Orchestrator hand-off.** This is the positive programme: not "is ΛCDM wrong" but "is THIS framework right". The framework's cap
law r_b = r_M √(a₀/g_ext) uses only |g_ext|. That makes it the direction-blind rule (SW01/SW02), and it is the one prediction
on the record that neither cold dark matter nor AQUAL/QUMOND shares:

| observable in galaxies sitting in a known external field | ΛCDM | AQUAL / QUMOND | this framework |
|---|---|---|---|
| outer-curve decline correlated with the MAGNITUDE of g_ext | no (tides only, nearest neighbour) | yes | **yes**, depth = ν(η) |
| azimuthal asymmetry aligned with the DIRECTION of g_ext | no | **yes**, ~10–15% in v at η ≈ 0.5 | **no** (0%) |

"Magnitude-yes, direction-no" is the pair that only the framework produces. Nothing below is in the repository (checked against
FIFTY_NEXT_STEPS, IDEAS_100, LANES, PREDICTIONS and the L/SW/KS lanes); the one adjacent lane (the wide-binary directional test)
is re-purposed in DE07 and its prior hint is stated against interest. Rules: `README.md` in this directory (both a₀ footings, both
kernels μ₂ and ν_RAR, no literal-True checks, decision rule written before the data are touched, a FAIL is a finding). Files:
`DEnn_<slug>.py/.out/.json` here; one line per lane in `DE00_INDEX.md`; nothing committed as "confirmed" without a second
independent computation.

## The theory side (days, no data)

**DE01 — the AQUAL anisotropy table.** For a point mass in a uniform external field the EFE-dominated potential is Milgrom's
Φ ≈ −GM/(μ(η) r √(1 + L sin²θ)), L = d ln μ/d ln η. Compute, with the repository's validated axisymmetric AQUAL solver
(`theory_2026/aqual_solver_2026.py`, the L243 machinery), the exact circular-speed asymmetry A(η, r/r_M) ≡ (v_∥ − v_⊥)/v̄ for
in-plane external fields, for η ∈ {0.2, 0.3, 0.5, 1, 2} and r/r_M ∈ {1, 2, 3, 5}, both kernels. Certify in Lean the
closed-form angular factor and its small-L expansion (algebra). Deliverable: the table the data lanes score against.
Expected: A ≈ 10–15% at η = 0.5, r ≥ 2 r_M for μ₂; state the ν_RAR value.

**DE02 — the framework's decline law.** Under the isotropic rule g = ν(√(x² + η²)) g_own, compute the outer log-slope
d ln v/d ln r beyond r_b and the Keplerian floor v² r → ν(η) G M_b as functions of η; contrast with (a) AQUAL's
azimuthally-averaged decline and (b) a ΛCDM tidally truncated NFW halo (floor v² r → G M_dyn with M_dyn/M_b ≈ 3–5 inside the
tidal radius). Deliverable: the three curves v(r; η) that DE05/DE06 fit. Certify the floor identity in Lean.

**DE03 — the dSph shape prediction.** In AQUAL the phantom of a dwarf spheroidal in the Milky Way's field is elongated along
the field; compute the predicted potential ellipticity ε_Φ(η) for η of the classical dSphs (0.1–0.6) and the implied stellar
ellipticity alignment with the Galactic-centre direction. The framework predicts no field-aligned ellipticity (tidal alignment
only). Deliverable: ε_Φ(η) table for DE09.

## The data side (archival, all public)

**DE04 — the sample.** SPARC galaxies with environmental η from the Chae et al. 2021 table (2M++-based g_ext; arXiv:2109.04745)
or recomputed from 2M++ (Carrick 2015); keep η ≥ 0.3 (≈ 30–40 galaxies). For each: the UN-symmetrised approaching and receding
rotation curves (THINGS: de Blok 2008 tables; WHISP: Swaters 2002; the original HI papers for the rest), the disc position angle,
inclination, and the projected direction of g_ext on the sky. Record the geometry factor cos θ_∥ between the disc major axis and
the projected field. Deliverable: one CSV, one provenance line per galaxy.

**DE05 — the direction test (the framework's fingerprint).** Statistic: A_obs = (v_toward − v_away)/v̄ over the outer points
(r > r_b), signed by the field direction, regressed on the predicted AQUAL amplitude A_pred(η, r) cos θ_∥ from DE01. Controls:
the same statistic with the field direction rotated by 90° (the random-lopsidedness null, expected ~5%), and with η shuffled
across galaxies. Decision rule (frozen now): slope of A_obs on A_pred consistent with 1 at 2σ ⇒ AQUAL; consistent with 0 at 2σ
and inconsistent with 1 at 3σ ⇒ direction-blind (the framework); power estimate: N = 30 separates 10% aligned from 5% random at
~5σ. Deliverable: the slope with its error, both kernels.

**DE06 — the magnitude test done as a floor, not a correlation.** For the same sample, measure v² r at the last reliable points
and compare with the parameter-free framework floor ν(η) G M_b (DE02) versus the ΛCDM expectation G M_dyn with M_dyn/M_b from
abundance matching truncated at the tidal radius. Decision rule: the ratio v² r / (ν(η) G M_b) has median within 0.15 dex of 1 and
scatter < 0.2 dex ⇒ framework; median > 0.4 dex ⇒ ΛCDM-like halos survive in strong fields. This is the half Chae 2020 argued
from correlations and Freundlich 2022 disputed; the floor form is not degenerate with tides because tides do not set the
amplitude to ν(η) G M_b.

**DE07 — wide binaries: the angular modulation (re-purposed lane; prior hint stated against interest).** The repository's
directional-EFE test on Gaia wide binaries (registered as MI vs MG; its Branch-B switch fired once at Â = +2.95, p = 0.029,
N needed ~1,157) is exactly the framework's discriminator: AQUAL predicts the velocity boost to depend on the angle between the
binary's separation vector and the Galactic-centre direction (L = d ln μ/d ln η ≈ 0.27 at η = 2.5 for μ₂ ⇒ ~6% modulation);
the framework predicts zero modulation, like MI. Re-run the registered statistic on the El-Badry 2021 DR3 catalogue at the
registered N, then on DR4, under the ORIGINAL decision rule; the p = 0.029 hint is, as it stands, evidence against the
direction-blind rule and must be reported as such.

**DE08 — cluster spirals: the extreme-η case.** For Virgo spirals with HI curves (VIVA, Chung 2009; η ≈ 0.3–1 from the cluster
potential at each galaxy's projected radius) the framework predicts outer velocities reduced to the ν(√(x² + η²)) level, i.e.
Tully–Fisher offsets of 0.2–0.4 mag at the outermost HI points against the field relation, while ΛCDM predicts ≤ 0.1 mag. Use
the outermost HI velocities, not optical curves (x ≈ 1–3 there, the effect is small). Decision rule frozen from DE02's curves.

**DE09 — dSph elongation alignment.** Score the classical dSphs' measured ellipticities and position angles against the
Galactic-centre direction with DE03's ε_Φ(η): AQUAL predicts field-aligned elongation growing with η; the framework predicts
only tidal (orbit-aligned) elongation. Data: McConnachie 2012 structural parameters; Gaia DR3 proper motions for orbit directions.

**DE10 — lopsided HI morphology alignment.** The m = 1 phase of the outer HI distribution (WHISP harmonic decompositions) versus
the projected g_ext direction: AQUAL compresses the phantom along the field and the gas follows; the framework predicts no
alignment. Same statistic as DE05 on the density rather than the kinematics; an independent channel with the same sample.

## What "the framework is right" means at the end of this plan

All three hold, each with a second independent computation: DE05 direction-no at 3σ against AQUAL's amplitude; DE06 the floor
ν(η) G M_b within 0.15 dex; DE07 or DE09 or DE10 direction-no on an independent channel. Then the framework has a fingerprint no
other theory on the table produces, and the covariant construction that realises the direction-blind rule (SW02's ψ-switch, still
without an action) becomes the theory to write. If DE05 or DE07 returns direction-yes, the framework's cap law is wrong and AQUAL's
EFE stands, which Cassini has already killed: that outcome closes the modification programme by data, not by theorem. If DE06
returns median > 0.4 dex, external fields do not strip the excess and the emergent reading wins its cleanest test.

Order: DE01 and DE02 first (they set every decision rule), then DE04 → DE05 → DE06, then DE07 on DR3 now, DE08–DE10 as the
independent channels. Expected cost: DE01–DE02 two days of compute; DE04–DE06 one week of data assembly; the rest in parallel.
