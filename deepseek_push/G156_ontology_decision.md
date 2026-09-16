# G156 — THE ONTOLOGY DECISION PRE-REGISTRATION: dust = CHARGE or RELIC, and what the data already say

**Status:** 2026-09-16. Pre-registration lane over the committed ontology
contradiction (H048 DOOR 2). All framework numbers load from `H047_results.out`
(char), `G093_results.json` and `G115_results.json` (relic) — COMMITTED. All
published numbers carry citations and are flagged **UNVERIFIED in-repo**
(they are quoted, not re-derived). Companion artifacts: `G156_ontology_decision.py`
(8/8 checks PASS), `G156_ontology_decision.out`, `G156_results.json`.

**The question:** is the framework's free dust a *conserved Noether charge* of
a coherent field (H047: R(k) = 1 at every k, no cutoff) or a *warm
thermal-relic-equivalent species* (G093/G115: WDM transfer cut, λ_fs = 0.50 Mpc,
halo function truncated ~1e6 M☉)? The two readings are mutually exclusive, and —
as H048 recorded — **nobody has yet adjudicated them.** This lane pre-registers
the decision before the deciding data arrive.

---

## 1. THE TWO PREDICTIONS, SIDE BY SIDE

**R(k) = P_framework/P_LCDM** (the k-space cut; charge committed in H047 N10,
relic from the committed G115 damping tail 1 − T²):

| k [h/Mpc] | CHARGE (H047) | RELIC 5.7 keV | RELIC 3.5 keV (H047 col.) |
|---|---:|---:|---:|
| 0.1 | 1.000000 | 0.99987 | 0.999997 |
| 1.0 | 1.000000 | 0.99987 | 0.999560 |
| 10.0 | 1.000000 | 0.978 | 0.926623 |
| 30.0 | 1.000000 | 0.769 | — |
| 100.0 | **1.000000** | **0.038** | 0.000290 |
| 300.0 | 1.000000 | ~0 | ~0 |

A **1.1–3.5 orders-of-magnitude separation at k = 100 h/Mpc** (factor 26 at the
relic's 95% CL mass 5.7 keV; factor ~3500 at the H047-comparison 3.5 keV).

**The sub-halo mass function** (Aquarius-class, normalized to N(>1e8) = 64;
G115 D1, COMMITTED):

| M [M☉] | N_CDM | N_5.7 keV | S_5.7 | N_3.3 keV | S_3.3 |
|---|---:|---:|---:|---:|---:|
| 1e5 | 32,076 | 8,622 | 0.27 | 1,696 | 0.05 |
| 1e6 | 4,038 | 3,927 | 0.97 | 1,640 | 0.41 |
| 1e7 | 508 | 508 | 1.00 | 505 | 0.99 |
| 1e8 | 64 | 64 | 1.00 | 64 | 1.00 |

**Differential slope dN/dlnM(1e5)/dN/dlnM(1e7): CDM 63.1 (RISING) → 5.7 keV
0.49 (INVERTED) → 3.3 keV 0.002 (INVERTED).** The two ontologies agree to ~3%
at 1e7+ and differ by factor 26–31,600 in the 1e5–1e6 decade. Other axes:
λ_fs = 0.000 Mpc (charge) vs 0.50/0.82 Mpc (relic 5.7/3.3 keV); M_hm(5.7 keV) =
5.03e5 (sim-fit) / 5.77e6 (window convention). G115's budget re-closure to
**0.60–0.79 is built on the truncation**; the G079 reference 0.79–0.95 required
the guessed sub-1e6 floor (0.05–0.15 of matter) that the truncation replaces.

---

## 2. THE CURRENT-DATA SOUNDINGS

### (a) MW satellite luminosity function — CITED, UNVERIFIED in-repo

- **Observed:** ~65 confirmed MW satellites today (M_V to ~−1; ~38 sit in the
  M_V ∈ [−4, −1] ultra-faint band, approximate inventory), up from the 11
  classical bright (M_V < −8) pre-survey.
- **Charge's no-cutoff prediction:** the completeness-corrected total
  **265^(+79,−47) satellites with M_V ≤ 0** (10–300 kpc) from the DELVE census
  (Tan et al. 2026, arXiv:2509.12313). The DES Y3+PS1 census at 10σ ~22.5 mag
  (Drlica-Wagner et al. 2020, ApJ 893:47) recovered **no new high-significance
  candidates** — the observed census (65/265 ≈ **25%**) is completeness-limited.
- **The "missing-satellites" factor is a galaxy-formation statement, not a DM
  statement:** the ~10–50× raw deficit (11 bright vs thousands of CDM subhalos)
  is absorbed by the galaxy–halo connection — occupation consistent with 100%
  down to < 3e8 M☉, M_50 < 8.5e7 M☉ (95%, Nadler et al. 2020, ApJ 893:48); the
  completeness-corrected counts are CDM-consistent for L ≳ 340 L☉ (M_V ≲ −1.5),
  with WDM < 4 keV in tension (Kim, Peter & Hargis 2017, PRL 121, 211302).
- **What the faint counts already constrain:** the SHMF normalization at
  1e8–1e10 M☉ to ~30–50%, and **m_WDM > 6.2–6.5 keV (95%) from satellites alone**
  (Nadler et al. 2021) — i.e. the relic's **lower window (3.3–5.3 keV) is
  already excluded at 95%**. The N(>1e5, >1e6) SHMF rows (32,076/8,622/1,696 and
  4,038/3,927/1,640 for CDM/5.7/3.3 keV) are committed (G115); the *observed*
  satellite counts at those halo masses are **NOT yet measured** (UNVERIFIED).

### (b) Strong-lensing flux-ratio anomalies — CITED, UNVERIFIED in-repo

- Quads probe subhalos 1e6–1e9 M☉: the 1e7–1e9 decades dominate the largest
  flux-ratio anomalies, ≲1e7 the small ones (Gilman et al. 2018, arXiv:1712.04945).
- **The JWST 28-quad survey with arcs + flux ratios** (Gilman et al. 2026,
  arXiv:2511.07513): subhalo abundance consistent with CDM-model predictions to
  ~30%, suppression scale **m_hm < 10^7.2 (95%, Bayes factor 10:1)**.
- **Unified with the MW satellites** (Nadler et al. 2021): M_hm < 1e7 → **m_WDM
  > 9.7 keV (95%)**, 7.4 keV disfavored at 20:1.
- **Constraint on the 1e6–1e8 subhalo abundance:** consistent with full-CDM
  within ~1–2σ (amplitude within factor ~2–4). The lightest excluded suppression
  scale (m_hm ~ 1e7) sits only **×2.7–2.8 (5.7 keV window floor 5.77e6) to
  ×9.7 (8.33 keV floor 1.63e6) to ×31.5 (sim-fit floor 5.03e5)** above the
  relic's committed floors — the relic's open upper window survives *only*
  behind convention factors.

### (c) Stellar-stream gaps (GD-1, Pal 5) — CITED, UNVERIFIED in-repo

- Joint GD-1 + Pal 5 (Banik, Bertone, Bovy, Erkal & de Boer 2021, JCAP
  10(2021)043; arXiv:1911.02662): dark subhalos 1e5–1e9 M☉ **required**;
  **n_sub/n_sub,CDM = 0.4^(+0.3,−0.2) (68%), < 0.9 (95%)** within 20 kpc;
  f_sub = 0.14^(+0.11,−0.07)% (< 0.3% at 95%). The 1e5–1e6 and 1e6–1e7 decade
  posteriors are flat; very low abundances ≲ 0.2×CDM disfavored (95%).
- **The 1e5–1e8 impactor abundance is currently consistent with CDM within the
  68–95% bands — with a twist:** the joint posterior *peaks* at 0.4×CDM (1.3–2σ
  below the charge's 1.0 — mildly pro-truncation), while the GD-1 spur-and-gap
  single perturber (1e6–1e8 M☉) is favored **2–3σ ABOVE the LCDM subhalo density**
  ("The Spur and the Gap in GD-1", 2019) — mildly pro-charge. The two stream
  readings lean opposite ways.
- Mass bound: **m_WDM > 3.6 keV (streams), > 4.6 keV (GD-1), > 6.2 keV
  (+ satellites)** — again excluding the relic's 3.3–5.3 keV sub-window.

### (d) Lyman-alpha at high k — COMMITTED, NON-DISCRIMINATING

The relic's cut lives at k_hm = 64.9 (5.7 keV) to 98.9 (8.33 keV) h/Mpc; the
forest's resolved window stops at k_max ~ 3 h/Mpc at z = 3 (G115 D2): the cut
sits **22–33× beyond kmax — the forest sees NOTHING at the cut.** Self-consistent
with BOTH ontologies (the dust's effective pressure passes the L194/L224 forest
registers either way, G093 C3). The forest is the *measurer* of the relic's mass,
not a *witness* to its cutoff — which is exactly why the decision is not in the
forest (G093 C2: λ_fs ~ 0.9 keV/Mpc/m is one statement with the forest tolerance).

---

## 3. THE PRE-REGISTRATION — WHICH MEASUREMENT, AT WHAT PRECISION, FLIPS THE ONTOLOGY

Pre-registered *now*, before the deciding data arrive. Every number below is
either committed-register or cited-with-citation.

### (a) The DES/LSST/LSST-class faint-satellite counts at M_V ≤ −1 (the census discriminant):

- **CHARGE (no cutoff) predicts:** the no-cutoff empirical total **265^(+79,−47)
  (M_V ≤ 0)** with the committed SHMF rows N(>1e5) = 32,076 and N(>1e6) = 4,038
  continuing below 1e6 (G115).
- **RELIC (truncated) predicts:** N(>1e5) = 8,622 (5.7 keV, S = 0.27) / 1,696
  (3.3 keV, S = 0.05); N(>1e6) = 3,927 (S = 0.97) / 1,640 (S = 0.41).
- **The discriminant N_req** (completeness-corrected counts N_obs/c required to
  separate the two Poisson predictions at 95% CL):

  | bin | S_5.7 | N_req(5.7) | S_3.3 | N_req(3.3) |
  |---|---|---:|---:|---:|---:|
  | >1e5 M☉ | 0.27 | **14** | 0.05 | **9** |
  | >1e6 M☉ | 0.97 | **~10⁴** | 0.41 | **22** |
  | >1e7 M☉ | 1.00 | ~10⁹ | 0.99 | ~2e5 |

  against the survey scale (~265 satellites at M_V ≤ 0 fully complete): the
  **3.3 keV-level discriminant (N_req ~ 9–22) is achievable inside the census;
  the 5.7 keV-level at 1e6 (N_req ~ 10⁴) is ~38× beyond any full-sky census.** →
  The LF alone flips the ontology **only for the relic's lower edge
  (m ≲ 3.5–4 keV)** — the same conclusion as Kim-Peter-Hargis's L > 340 L☉
  threshold — and cannot decide the 5.7–8.3 keV window.

### (b) The sub-halo-mass-function slope below 1e6 from the lensing/stream probes:

- CHARGE: the differential slope **keeps rising** (63.1 over 1e5→1e7, committed).
- RELIC: the slope **inverts** below M_hm: 0.49 (5.7 keV) / 0.002 (3.3 keV), committed.
- Current state of this axis: lensing m_hm < 10^7.2 (95%) with n_sub
  CDM-consistent to ~30% (Gilman+26); streams 0.4^(+0.3,−0.2)×CDM in 1e5–1e9
  (Banik+21). **The 1e5–1e6 differential is OPEN** — that is where the decision lives.

### (c) THE STATEMENT — the ontology is DECIDED when:

> **DECIDED = RELIC** when the measured differential SHMF slope in the 1e5–1e8
> decade **inverts at 95% CL**, dN/dlnM(1e5–1e6)/dN/dlnM(1e6–1e7) **≤ 0.5**, at an
> inversion scale M_hm ∈ **[5e5, 5.8e6] M☉**, mass-consistent with
> m_WDM ∈ [5.6, 8.3] keV.
> → G115's 0.60–0.79 closure stands as *closed-with-cutoff*.
>
> **DECIDED = CHARGE** when the measured SHMF at 1e6–1e7 is within **[0.5, 1.5] ×
> full-CDM at 95% CL** across the lensing + streams + census combination, i.e.
> **m_hm < 1.6e6 (95%, window convention)** — below the lightest committed floor
> M_hm(8.33 keV) = 1.63e6.
> → H047's R(k) = 1 stands; G115's closure mechanism (built on the truncation)
> is **voided**, the budget returns to the G079 reference (0.79–0.95 with the
> guessed sub-1e6 floor), and the sub-1e6 residual re-opens as OPEN.

**The precision required:** lensing — N_quads ≥ 100 (28 today) or extended-arc
reconstruction at 2–3× current precision (m_hm to < 3e6); streams — ≥ 5 streams
at Gaia-DR3/Rubin depth (2 today), with per-decade Poisson counts in the 1e5–1e6
and 1e6–1e7 bins; census — complete to M_V ≤ −1 with the DELVE/DES-Y6
completeness function fit and N_obs/c ≥ N_req (9–22 at the 3.3 keV level).

**The two rules are exclusive:** an inverted slope and a CDM-full slope cannot
both be measured at percent precision. The current data sit *in the gap*
(lensing m_hm < 10^7.2 vs the relic's floors at ×2.7–31.5; streams peak 0.4×CDM,
95% < 0.9×CDM) — **UNDECIDED by factor ~3–30 in the mass-function slope, and the
next 2–3× in lensing precision or the completed census is the deciding step.**

---

## 4. VERDICTS

[PASS] **V1 the two-prediction table** — the full side-by-side table of §1:
charge R(k) = 1.000000 at every k (R(100) = 1 vs 0.038 at 5.7 keV; differential
SHMF slope 63.1 vs 0.49/0.002; N(>1e5) 32,076 vs 8,622/1,696; λ_fs 0 vs
0.50 Mpc; M_hm none vs 5e5–5.8e6). Same axes, one table, no mixture: **the
ontologies agree to 3% at 1e7+ and differ by 26–31,600× in the 1e5–1e6 decade.**

[PASS] **V2 the current-data soundings** — every probe is CDM-consistent at 95%
(charge-consistent); the 95% WDM bounds **6.2–6.5 keV (satellites), 9.7 keV
(lensing + satellites), 3.6–6.2 keV (streams) already exclude the relic's lower
window 3.3–5.3 keV**; the 5.7–8.33 keV open edge survives only behind m_hm
convention factors ×2.7–9.7; the streams posterior peaks at 0.4×CDM (mildly
pro-truncation) against the GD-1 perturber 2–3σ above CDM density
(pro-charge); the forest is non-discriminating (22–33× beyond kmax, committed).
**NET: undecided, leaning charge on the normalization, excluding the relic's
lower half-mass window, with the decision living in the 1e5–1e8 dark-halo decade.**

[PASS] **V3 the pre-registered decision rule** — §3(c): RELIC on a 95% slope
inversion ≤ 0.5 at M_hm ∈ [5e5, 5.8e6]; CHARGE on the 1e6–1e7 decade within
[0.5, 1.5]×CDM (m_hm < 1.6e6). Precision: ≥ 100 quads or arcs at 2–3×, ≥ 5
streams, census to M_V ≤ −1 with N_obs/c ≥ N_req = 9–22 (3.3 keV level) —
unreachable ~10⁴ at the 5.7 keV level, hence **the LF alone flips only the
lower edge; the physical decision is the dark-halo slope.** Consequences
pre-committed: RELIC validates G115's 0.60–0.79 closure; CHARGE voids it and
re-opens G079's sub-1e6 residual.

---

**Honest labels.** Committed numbers load from G115/G093/H047. All published
numbers are cited and UNVERIFIED in-repo: the observed satellite census and the
DELVE 265^(+79,−47) total (Tan+26; Drlica-Wagner+20; Nadler+20; Kim-Peter-Hargis
2017), the lensing bounds (Gilman+18/26; Nadler+21), and the stream bounds
(Banik+21; spur-and-gap 2019). The N_req arithmetic is derived here from the
committed S(M) rows (two-Poisson 95% separation, z = 1.96, √2 for two counts).
No new physics is asserted: this lane is the ontology arbiter's bookkeeping —
the decision rule exists so that the *next* precision step, not a later
retrospective, settles H048 DOOR 2.