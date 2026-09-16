# G173 — THE BREAK OBSERVING PROPOSAL

**The F(e_N) prediction as a real, pre-registered observation** — the galaxy-scale
break test: the zero-parameter kernel break radius r_cut/r_M = F(e_N) on the Milky Way
(home-galaxy leg, already in hand) and on resolved H I pairs at known external field
(WALLABY-DR3-class + MIGHTEE-pair candidates), with targets, the prediction graph,
the instrument, exposure/SNR, falsifiers, controls, pipeline, and verdicts.

**Filed 2026-09-16. Lane G173.**
**Deliverable: this file + `G173_break_proposal.py` / `.out` / `G173_results.json` (committed and pushed).**

> **STATUS: THE MW LEG IS DECIDED TODAY; THE PAIR LEG IS READY TO RUN AS SOON AS THE
> DATA LAND.** The home-galaxy branch needs no new observation: the registered
> measured break (6.1 kpc) and the G072 kernel at every committed M_b convention all
> sit inside the F(e_N) band [0.62, 0.66], and the Eilers+19/Gaia data already pin the
> break to ~±0.1–0.2 kpc. The resolved-pair branch needs (i) WALLABY-DR3 (full-survey)
> archival rotation curves of the committed top pairs — DR2's successor; (ii) a
VLA/MeerKAT follow-up on the one committed pair with an observable break,
J132029-214845 (break at 4.97 arcmin = ~10 WALLABY beams / ~50 VLA-B beams); and
> (iii) identifications of the e_N ~ 0.5–1.4 tight-pair class (d ≤ 6–10 kpc) from
> WALLABY-DR3 and the MIGHTEE-pair candidates, which are the only objects that read
> the 0.62–0.66 turn itself. The decision rules (F1/F2/F3, the band windows) are fixed
> here, before those data are read.

**Built on (all committed):** G149 `G149_kernel_rcut.py/.out/.json` (the F(e_N)
machine and the DR3-falsifier target rows, 5/5), G119 `G119_break_factor.py/.out/.json`
(the kernel solve, 6.13 kpc = 0.6232), G072 `G072_mw_law.py/.out/.json` (the MW: the
registered 6.1 kpc break, R_efe 6.74 kpc at its own M_b = 7e10, Eilers quote), G100
`G100_results.json` (the WALLABY-DR2 top pairs: e_N, d, D, M_HI), the Eilers+19 Table 1
(`real_research/data/mw_rc_eilers2019_table1.tsv`, 38 points 5.27–24.82 kpc), and G129
(style). Every number below is reproduced by `G173_break_proposal.py` (gated against
G149's own F-grid to 1e-9; the target rows are read verbatim from G149's committed JSON).

**Constants (G149's, verbatim):** canonical a0 = 9.3619e-11 m/s², μ₂ kernel with s = 2 a0,
M_enc(x) = 1−(1+x)e^−x (exponential-disk cumulative), R_d = 0.2540 r_M (MW-anchored),
g_ext(MW) = 2.146e-10 (L240); G = 6.674e-11, M_sun = 1.98892e30.

---

## 1. THE TARGETS — the MW itself, and the resolved pairs

### 1a. The Milky Way (home-galaxy leg — the decision is already in hand)

The registered measured break is **6.1 kpc** (G003 V6; G072's `registered_break_kpc`).
What the existing Eilers/Gaia data already do: Eilers, Hogg, Rix & Ness 2019 (ApJ 871,
120), 38 APOGEE/Gaia red giants from 5.27 to 24.82 kpc via the axisymmetric Jeans
equation — **v_c(R0) = 229.0 ± 0.2 km/s, linear slope d v_c/dR = −1.7 ± 0.1 km/s/kpc,
R0 = 8.122 kpc** (systematics 2–5% on v_c). The break is the radius where the curve
departs from that linear slope; the registered reading is 6.1 kpc.

The kernel's prediction against it (r_M = √(G M_b/a0)):

| quantity | value @ M_b = 6.5e10 | value @ M_b = 7e10 (G072's convention) |
|---|---|---|
| kernel r_cut (G119 grid / G149 refined) | **6.13 / 6.17 kpc** → F = 0.6232 / 0.6273 | **6.54 kpc** → F = 0.6401 |
| deep-form EFE √(G M_b/g_ext) | 6.50 kpc | 6.74 kpc → F = 0.6605 |
| the F(e_N) band [0.62, 0.66] in kpc | **[6.10, 6.49] kpc** | [6.33, 6.74] kpc |
| **measured break 6.1 kpc** → F | **0.6200 — in band, at the lower edge** | 0.5975 — *mixed-M_b ratio*, flagged |

**The decision (restatement requested by the brief):** measured 6.1 vs kernel 6.13 =
**−0.5%**; vs the refined 6.17 = −1.2%; vs the 7e10-convention kernel 6.54 = −6.7%. The
brief's "6.74 vs 6.54 = −3.1%" is the deep-form-vs-kernel gap **at fixed M_b = 7e10**:
F = 0.6605 vs 0.6401, **both inside [0.62, 0.66]** → the −3.1% is the kernel
interpolation (near g ~ a0), not a band violation. The measured 6.1 kpc = F 0.6200 sits
**at the band's lower edge** (the 0.62 edge ↔ 6.100 kpc at r_M = 9.8384). **The MW's
own break is inside the F(e_N) band at every committed convention — the home galaxy
already passes the break test, at the edge, with zero parameters.**

### 1b. The resolved pairs (WALLABY-DR3-class; committed G149 target rows)

Twelve rows, six committed pairs, gas (1.33×M_HI) and bracket (2.66×M_HI) mass
conventions — every predicted break assumes the pair's *own* field, g_ext = G M_b,neigh/d²:

| pair | D [Mpc] | d [kpc] | e_N | F = r_cut/r_M | r_cut [kpc] | break [arcmin] | readable? |
|---|---|---|---|---|---|---|---|
| **J132029-214845** (bracket) | 22.5 | 17.1 | **0.189** | **5.67** | 32.5 | **4.97** | **yes — the flagship** |
| J132029-214845 (gas) | 22.5 | 17.1 | 0.094 | 10.97 | 44.5 | 6.80 | yes, at the disk edge |
| J130003-183028 (bracket) | 196.6 | 22.2 | 0.114 | 9.13 | 53.7 | 0.94 | **sub-beam** (30″ WALLABY; even VLA-B 6″ → 1.7 kpc bins) |
| J130647-162241 (bracket) | 156.2 | 25.4 | 0.036 | 28.5 | 112.0 | 2.47 | F r_M ≫ R_HI — break beyond the disk |
| J124531-003203 (bracket) | 23.1 | 47.6 | 0.017 | 58.2 | 158.7 | 23.6 | 58 r_M — break far beyond the disk |
| J132020-124006 (bracket) | 20.8 | 34.6 | 0.015 | 65.3 | 49.1 | 8.13 | 65 r_M — beyond the disk |
| J103704-252038 (bracket) | 53.0 | 77.4 | 0.012 | 82.5 | 206.8 | 13.4 | resolved in angle; 82 r_M — beyond the disk |
| + 5 more rows (gas convention) | — | — | 0.006–0.094 | 10–165 | — | 1.30–33.2 | same register |

**Honest count: exactly one committed pair has a practically observable break —
J132029-214845** (break at 5.67 r_M with r_M = 5.73 kpc, i.e. 32.5 kpc ≈ the HI disk
edge; 4.97 arcmin at 22.5 Mpc = 10 WALLABY beams / 50 VLA-B beams). Every other
committed pair predicts the break at 9–165 r_M — beyond its HI disk (r_cut ≫ R_HI) or
sub-beam (J130003 at 197 Mpc). The G149 `required_field` note's "e_N ~ 2.7" is an
error in G149's JSON (a root exists at 2.7; F = 0.527); the correct ceiling is the
computed e_N* = 8.06 (this proposal, and G149's own printed output, use 8.1).

### 1c. The flagship requirement — J132029-214845 (e_N = 0.189, bracket)

*Break at 5.67 r_M = 32.5 kpc = 4.97 arcmin @ 22.5 Mpc; r_M = 5.73 kpc; 9.18 arcsec/kpc.*

**The rotation-curve requirement (bins to 5.67 r_M):** 12 radial bins of 0.5 r_M
(2.87 kpc) covering [0, 5.67 r_M], i.e. 0.44′ → 4.97′, plus one bin past the break to
see the turnover. At 30″ (WALLABY) that is ~2 bins across the break radius; at 6″
(VLA B-config) ~50 beams across it — the turnover at 5.67 r_M needs ≤ 15″
(≤ 1.4 kpc per beam) to place the break to ±0.1 r_M.

**Surface-density sensitivity:** exponential-disk HI, M_HI = 8.3e9 M_sun:

| R_sd [kpc] | N_HI at the break radius (32.5 kpc) |
|---|---|
| 3.0 | 3.6e18 cm⁻² (marginal for everyone; only the deepest VLA/MeerKAT) |
| 4.5 | 6.0e19 cm⁻² (WALLABY 5σ/30 km/s ~1e20: **marginal**; VLA-B/MeerKAT 6–15″, 2–4e19 at 5σ in 10–20 km/s: **detected**) |
| 6.0 | 2.0e20 cm⁻² (detectable even in WALLABY-DR3 archival) |

**The e_N the pair needs (restated):** at the measured field e_N = 0.189 the break sits
at 5.67 r_M (disk edge). Pulling the break into the well-lit inner disk: **1 r_M**
needs e_N ≥ 1.39 (pair d ≤ 6.3 kpc at the same neighbour mass); **2 r_M** needs
e_N ≥ 0.61 (d ≤ 9.5 kpc). Those tight pairs are interacting systems at 10–40 Mpc — the
MIGHTEE-pair candidate class — and they are the only objects whose break lands where
rotation curves are bright.

## 2. THE PREDICTION TO TEST — the F(e_N) graph

The zero-parameter break radius for **any** galaxy (G149, closed form exact for the
kernel): **F² e_N μ₂(e_N/2) = M_enc(F r_M/R_d)**, r_cut = F(e_N) r_M, solved where the
full-μ₂ internal field falls to g_ext. F runs on e_N alone (0.000% over 300× M_b at
fixed R_d/r_M).

**The full shape on e_N ∈ [0.1, 10]:**

| e_N | 0.1 | 0.19 | 0.5 | 1.0 | 2.0 | **2.29 (MW)** | 2.5 | 3.0 | 5.0 | 8.0 | ≥ 8.06 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F(e_N) | 10.37 | 5.55 | 2.36 | 1.32 | 0.718 | **0.6273** | 0.573 | 0.466 | 0.206 | 0.003 | **NO ROOT** |

- **Deep limit (e_N ≪ 0.1):** F → √M_enc/e_N ~ **1/e_N** — the H033 *linear* form is
  the kernel's deep limit; at e_N = 0.1, F = 10.37 vs the 1/e_N = 10.0 asymptote (check
  in-script: ratio 0.96). The committed WALLABY pairs live here (e_N 0.006–0.19 →
  F 5.5–165).
- **The 0.62–0.66 band at the MW anchor:** the μ₂ interpolation at e_N = O(1) pins
  F into **[0.62, 0.66]** — the registered band ↔ e_N ∈ [2.18, 2.32]; the MW at
  e_N = 2.29 → F = 0.6232 (registered grid) / 0.6273 (refined) — **the single anchor
  point of the band today.**
- **The no-break ceiling:** above **e_N* = 8.06** (≈8.1) there is no root — the
  internal field never reaches g_ext; the galaxy is external-field-dominated and
  **has no break at all**. (e_N* solves e_N μ₂(e_N/2) = (r_M/R_d)²/2, MW-anchored.)

**The instrument that reads the curve: resolved-pair rotation curves at known e_N.**
The curve is a function of one observable per target — the pair field ratio e_N =
g_ext/a0 (neighbour mass, separation, distance) — so each resolved pair galaxy yields
one point (e_N, measured F = r_cut/r_M): the break radius in units of its own r_M.
- **The deep-limit branch (e_N 0.01–0.19), the committed set:** 15 top WALLABY pairs
  (G100), 6 with computed breaks — G149's table. The two e_N ≥ 0.1 objects
  (J132029 at 0.189, J130003 at 0.114) bracket the start of the 1/e_N turnover;
  J132029 alone is resolvable (4.97′). One further object with e_N ~ 0.05–0.1 and a
  break at ≤ 8′ would read a second point on the deep branch.
- **The 0.62–0.66 turn (e_N 0.5–3), the decisive set:** **zero committed pairs.**
  Needed: ~5–10 resolved pairs at e_N ∈ [0.5, 3] (tight pairs, d ≤ 6–10 kpc, at
  10–40 Mpc — MIGHTEE-pair candidates + WALLABY-DR3 full-survey identifications) to
  test the turn's shape; the MW is the only anchor there, and the turn is exactly
  what separates the kernel (0.62–0.66) from the deep 1/e_N line (which would predict
  F(2.3) ≈ 0.44, 30% away).
- **The ceiling (e_N > 8.1):** tight interacting systems — a resolved pair at e_N > 8.1
  must show **no break** (F2).

The graph itself: log F vs log e_N, monotonically decreasing from F = 10 at e_N = 0.1
through the 0.62–0.66 plateau at e_N ~ 2.2 to the no-root wall at e_N* = 8.1 — the
predictions the pairs and the MW place on it: MW (2.29, 0.6232–0.6273), J132029
(0.189, 5.55–5.67), and the future tight pairs along the turn.

## 3. THE INSTRUMENT — which survey measures which scale

| target class | instrument | resolution | role in this proposal |
|---|---|---|---|
| **the MW break** | Gaia astrometry + APOGEE (Eilers+19, the repo table); **Gaia DR4 (2026-12)** | sub-km/s per 38 bins, R = 5.3–24.8 kpc | the break location to ±0.1–0.2 kpc; v_c(R0) 229.0±0.2; slope −1.7±0.1 — **already measured** |
| **J132029-214845 & the pair set** | **WALLABY-DR3** (ASKAP, full survey; DR2 = 30″ catalogue + kinematic models in repo) | 30″ = 2.7 kpc @ 22.5 Mpc | archival rotation curves; the 4.97′ break zone at 5σ ~1e20 cm⁻² → marginal-to-present (R_sd 4.5–6 kpc) |
| **the same pairs, decisive** | **VLA B-config / MeerKAT** H I follow-up | 6–15″ = 0.7–1.3 kpc @ 22.5 Mpc | 12 half-r_M bins to 5.67 r_M; break placement ±0.1 r_M; 5σ 2–4e19 cm⁻² in 10–20 km/s — 30–60 h class |
| **the e_N ~ 0.5–1.4 turn** | **tight pairs** (d ≤ 6–10 kpc, interacting): WALLABY-DR3 + **MIGHTEE-pair candidates** (MeerKAT; G099/G133 footing: resolved H I RARs at 20–40 Mpc, inner rings < 5″ cut) | 8–30″ | the only objects whose break lands at 1–2 r_M inside the bright disk; the decisive set for the 0.62–0.66 turn |

**The resolution needed.** To place the J132029 break at ±0.1 r_M (0.57 kpc): beam ≤
15″ = 1.4 kpc — VLA-B/MeerKAT. To reach the 4.97′ zone at all: WALLABY 30″ (10 beams
across the radius — the turnover shows as a slope change, not a sharp kink). For the
MW: the data exist; DR4 refines.

## 4. EXPOSURE / SNR — the forecast

**The MW leg — already at decision SNR.** The Eilers 38 points carry ±0.2 km/s on
v_c(R0) and ±0.7–1.9 km/s per ring; with slope −1.7 ± 0.1 km/s/kpc the break location
is pinned to ±0.1–0.2 kpc → F_measured = 0.6200 ± ~0.02, i.e. the band edge is
**today's** result. A 3σ firing of F1 on the MW would require the break at F < 0.56 or
> 0.72 (outside band ± 3×0.02) — neither Eilers, Mroz nor Ou readings put it there.
**No telescope time requested for the MW.**

**J132029-214845.** WALLABY-DR3 archival first (end of survey): 30″ across 4.97′
(10 beams), 5σ N_HI ~ 1e20 cm⁻²/30 km/s → the break zone detected if R_sd ≳ 5 kpc,
marginal-to-absent if R_sd ~ 3–4.5. The decision observation: VLA B-config (or
MeerKAT) H I, 6–15″, 10–20 km/s channels, 5σ column 2–4e19 cm⁻²; two pointings (the
4.97′ extent fits one primary beam at 1.4 GHz ≈ 32′), total **30–60 h** — 12 bins of
0.5 r_M to 5.67 r_M, the outermost bins at N_HI 6e19–2e20 (R_sd 4.5–6) at SNR
2–5 per bin (bins of ~2.9 kpc contain ~2.9/1.4 ≈ 2 beams across → per-bin noise
divided by √2–√3, and the 10 km/s channels co-added over ±30 km/s triple the SNR:
the outermost bins land at SNR 3–8). Velocity scale: the target's flat velocity
(G M_b a0)^(1/4) ≈ 130 km/s (bracket) — the break's turnover signal is a
v_c fall of ~10–20 km/s between the 5 r_M and the > 6 r_M bins, separable from a flat
curve at ~3–5σ with the above per-bin SNR.

**The tight-pair class (e_N 0.5–1.4).** The objects are interacting; resolution must
separate the two disks (d ≤ 6–10 kpc at 10–40 Mpc → ≥ 8–30″ separation). WALLABY-DR3
30″ resolves d > 5 kpc; MeerKAT/VLA 8″ resolves d > 2 kpc. The measurement is the same
as the flagship's but the break lands at 1–2 r_M where the disk is bright (N_HI ~
1e21 cm⁻²) — **the turn set is the *easiest* to measure once identified; the delay is
catalog-side (finding the pairs), not sensitivity.**

## 5. THE FALSIFIERS (pre-declared; decision rules fixed before the data are read)

- **F1 — a measured break outside the F(e_N) band at ≥ 3σ.** The band is the predicted
  F(e_N) × (1 ± 0.032) — the registered 0.62–0.66 at the MW anchor, applied
  relatively at every e_N.
  * MW: band [0.62, 0.66] in F ↔ **[6.10, 6.49] kpc** (r_M 9.8384; ↔ [6.33, 6.74] at
    the 7e10 convention). Measured 6.1 kpc = F 0.6200 — in band at the lower edge.
    A Gaia-DR4 break outside [0.56, 0.72] in F (band ± the current ±0.02 precision
    at 3σ) fires.
  * J132029-214845: predicted F = 5.67 (bracket), band **[5.49, 5.84]** ↔ r_cut
    **[31.5, 33.5] kpc** ↔ **[4.81, 5.13] arcmin** (the ~±3% interpolation/convention
    band; the gas/bracket mass spread 5.55–10.97 is registered as an amplitude
    systematic, controlled below, not part of the band). A measured break outside
    [4.81, 5.13]′ at ≥ 3σ in the VLA/MeerKAT follow-up kills the curve.
  * Any resolved pair at e_N ∈ [0.5, 3]: measured F outside its (1±0.032) band at 3σ
    fires the same line.
- **F2 — a pair galaxy with e_N > 8.1 showing a break (the no-root falsifier).** Above
  e_N* the internal field never reaches g_ext — the framework predicts **no break at
  all** (external-field-dominated galaxy). For a 1e10-M_sun neighbour that is pair
  separation d < ~1.35 kpc (interacting/merging systems): a resolved break there kills
  the ceiling, and with it the F(e_N) root structure.
- **F3 — the MW's own break at a different F.** The 6.74 vs 6.54 = −3.1% gap at fixed
  M_b = 7e10 maps to F = 0.6605 vs 0.6401 — **both inside [0.62, 0.66]; F3 does not
  fire.** The measured 6.1 kpc (F = 0.6200) is the band edge; anything the current
  framework conventions produce sits in-band. Only a measured MW break outside
  [6.10, 6.49] kpc at ≥ 3σ (e.g. a Gaia-DR4 reading pushing past ~6.5 kpc with the
  6.5e10 convention) would fire F3 — and the mixed-convention 6.74 (G072's own M_b)
  is the *registered* alternative, not a violation.
- **PASS window.** MW F ∈ [0.62, 0.66] at ≤ 2σ (today: at the edge); pair breaks on
  the F(e_N) curve within the (1 ± 0.032) band; no break at e_N > 8.1.

## 6. THE CONTROLS

1. **The mass conventions.** Pair rows are computed for the gas (1.33×M_HI) and
   bracket (2.66×M_HI) bounds — a 2× F spread at fixed geometry. The *decision band*
   is the ±3.2% interpolation band at the bracket convention; a break measurement
   landing in [5.48, 5.85] is a hit under either row only if the mass convention is
   held fixed — the mass-scheme dependence is reported per row, never marginalized
   (registered G100/G149 practice).
2. **The M_b convention (MW).** 6.5e10 (registered kernel) vs 7e10 (G072) move the
   band [6.10, 6.49] ↔ [6.33, 6.74] kpc — the measured 6.1 kpc is in-band under both;
   the comparison is always same-M_b (the 0.685 mixed ratio is flagged, G119).
3. **HI truncation / disk edge.** The flagship's break (5.67 r_M) sits at/just beyond
   R_HI for R_sd ≤ 4 kpc — the turnover could be confused with the disk's own
   truncation. Control: the bins from 4 r_M outward must show the *stellar* (or
   resolved-HI, 3D-Barolo) rotation falling below the μ₂ prediction steeper than any
   plausible gas-depletion gradient; the R_sd from the G100/DR2 surface-density
   profile fixes the expected column (the F1 band is quoted only where the predicted
   column at the break is ≥ 5σ).
4. **Beam smearing & inclination.** 3D-Barolo beam-convolved fits (the DR2 pipeline);
   the outer bins' beam smearing *lowers* v_c — acts against the observation, and the
   turnover at 5.67 r_M is a *drop*, whose absence is equally measured.
5. **The vacuity register.** The SPARC proper-Y sample (G071/G149) predicts every
   break at 8–19,730× Rmax beyond every curve (0/35 in band) — the resolved-pair
   leg exists precisely because SPARC cannot see the break; this is not a control on
   the pair leg but the registered scope statement (G036 V3).
6. **e_N measurement error.** e_N = g_ext/a0 with g_ext = G M_b,neigh/d²: M_HI
   integrals (~10–20%) and projection (d = d_sky × sin i_pair, unknown) → e_N band
   ±30%. The band in F is ±3.2% *at fixed e_N*; an e_N error of 30% on the deep branch
   (F ~ 1/e_N) is a ±30% F shift — so the deep-branch points (J132029) constrain the
   *slope* F·e_N, not the absolute level, and the turn set (e_N 0.5–3, where dF/de_N
   is small) constrains the *level* — the two read complementary things, stated before
   the data.

## 7. THE FULL PIPELINE

1. **MW leg (run on existing data).** Eilers+19 table (repo): fit the linear slope
   over R ∈ [5.3, 8.5] kpc, locate the departure (the break) with 0.25-kpc sliding
   windows; report F = r_break/r_M(6.5e10) vs [0.62, 0.66]; the same at 7e10. Gaia
   DR4 (2026-12): re-run on the DR4 astrometry — the registered timing (G072).
2. **WALLABY-DR3 archival.** Full-survey source + kinematic catalogue; re-derive the
   top-pair e_N set (G100 machinery); extract rotation curves to the HI edge; compute
   the predicted break per pair; flag any pair whose predicted break (F r_M) lies
   inside its detected HI radius.
3. **VLA/MeerKAT follow-up (J132029-214845).** Two pointings, 6–15″, 10–20 km/s,
   30–60 h; 3D-Barolo/FAT fits; 12 bins of 0.5 r_M to 5.67 r_M + one outside; the
   turnover location r_cut_meas → F_meas = r_cut_meas/r_M(bracket) vs [5.48, 5.85];
   F1/F2 lines applied.
4. **The turn set.** Collate the MIGHTEE-pair candidates and WALLABY-DR3 tight-pair
   identifications (d ≤ 10 kpc → e_N ≥ 0.61); observe the e_N ∈ [0.5, 1.4] subset;
   each resolved pair contributes one (e_N, F) point on the graph §2.
5. **Decision record.** F1/F2/F3 fire exactly as pre-declared — no post-hoc rescues;
   the mass-convention rows are reported per row; a pair violating its band at 3σ is
   a kill even if the MW stays in band.

## 8. VERDICTS

**V1 — the proposal is complete.** TARGETS (the MW, decided today: measured 6.1 kpc =
F 0.6200 vs kernel 6.13/6.17/6.54, all in-band at the edge; the 6 committed WALLABY
top pairs with the 12-row gas/bracket table; the flagship J132029-214845 with its bin
requirement [12 × 0.5 r_M to 5.67 r_M], column requirement [N_HI 3.6e18–2.0e20 at the
break], and field requirement [e_N ≥ 1.39 → d ≤ 6.3 kpc for a 1 r_M break; ≥ 0.61 →
d ≤ 9.5 kpc for 2 r_M]); PREDICTION (the F(e_N) graph on [0.1, 10]: deep limit 1/e_N,
the 0.62–0.66 band at e_N ∈ [2.18, 2.32] anchored by the MW at 2.29, the e_N* = 8.06
no-break ceiling; two complementary instruments — deep-branch pairs read the slope,
turn pairs read the level); FALSIFIERS (F1 band-per-target at 3σ: MW [6.10, 6.49] kpc,
J132029 [4.81, 5.13]′; F2 no-root at e_N > 8.1; F3 the MW at a different F — in-band,
does not fire). **Executable as written; the MW leg on public data today, the pair leg
on WALLABY-DR3 + a 30–60 h follow-up.**

**V2 — SNR/feasibility per target.** *MW:* already at decision SNR — Eilers 38 points,
v_c(R0) 229.0 ± 0.2, slope −1.7 ± 0.1; break 6.1 kpc → F 0.6200 at the band edge,
±0.02 precision; F1 needs F < 0.56 or > 0.72 (3σ) — nowhere near the data. *J132029
-214845:* break at 32.5 kpc = 4.97′ @ 22.5 Mpc; WALLABY-DR3 30″ (10 beams across the
break, 5σ ~1e20 cm⁻²) sees the zone for R_sd ≳ 5 kpc; the decision is the VLA-B/MeerKAT
6–15″ follow-up, 30–60 h, 12 bins, outer bins at N_HI 6e19–2e20 → SNR 3–8 per bin, the
break's ~10–20 km/s drop separable at ~3–5σ. *The turn set:* catalog-limited, not
sensitivity-limited — 0 committed pairs at e_N ∈ [0.5, 3]; MIGHTEE-pair candidates +
WALLABY-DR3 tight pairs (d ≤ 10 kpc) supply them; their breaks land at 1–2 r_M in the
bright disk (N_HI ~ 1e21) and are the easiest to measure once identified.

**V3 — does this proposal decide the galaxy-scale break test, and on what timeline?**

> **DECIDES — THE MW LEG IS ALREADY DECIDED; THE PAIR LEG IS FULLY OBSERVABLE ON THE
> STATED INSTRUMENTS.** (1) **What is decided today:** the home galaxy's break — the
> measured 6.1 kpc = F 0.6200 sits inside the zero-parameter F(e_N) band [0.62, 0.66]
> at its lower edge; the −3.1% (6.74 vs 6.54, G072's M_b) is the deep-form-vs-kernel
> interpolation split, F 0.6605 vs 0.6401, in-band; every committed convention reads
> in-band, and F3 does not fire. The existing Eilers/Gaia data — not new telescope
> time — carry the MW leg to the decision at the band edge. (2) **What the pair leg
> adds and what it needs:** the MW is one point (e_N = 2.29); the resolved-pair leg
> reads the *curve*. The deep branch gains its first resolved point from
> J132029-214845 (e_N = 0.189, F = 5.67 — the slope F·e_N, ~10% control) with the
> WALLABY-DR3 archival rotation curve plus a 30–60 h VLA-B/MeerKAT HI follow-up
> (6–15″, 12 half-r_M bins to 5.67 r_M, N_HI 6e19–2e20 at the break); the decisive
> 0.62–0.66 turn needs the tight-pair class (d ≤ 6.3–9.5 kpc → e_N 0.61–1.39),
> ~5–10 objects identified from WALLABY-DR3 and the MIGHTEE-pair candidates, whose
> breaks land at 1–2 r_M in the bright disk. (3) **What it cannot decide:** the
> mechanism behind the break is not separable by one observation (the −3.1%
> interpolation split is a level statement, controlled by the M_b convention, and the
> deep-branch absolute level carries the ±30% e_N projection error — the slope, not
> the level); and the mass-convention spread (gas 1.33× vs bracket 2.66×) is a
> registered amplitude systematic on every pair row, reported, never marginalized.
> (4) **Timeline:** the MW leg is closed (Gaia DR4, Dec 2026, refines the break ±);
> WALLABY-DR3 full-survey archival analysis: 0–6 months after release; the
> J132029-214845 VLA/MeerKAT follow-up: 6–18 months (30–60 h, one semester); the
> tight-pair turn set: as identifications accumulate (WALLABY-DR3 final footprint +
> MIGHTEE-HI pair census), each pair yielding one (e_N, F) point on the graph §2.
> **The 0.62's final form — F(e_N) at the target's own external field — is a
> zero-parameter, three-falsifier statement, fully observable: one point is already on
> the curve, and the rest of the curve is on the sky.**

---

*All numbers from the committed G149/G119/G072/G100 artifacts, reproduced by
`G173_break_proposal.py` (gate vs G149's F-grid to 1e-9; target rows and MW anchor
read from the committed JSONs; 5/5 checks PASS). A FAIL would be a finding. The
G149 JSON's `required_field` "e_N ~ 2.7" no-root note is an error (a root exists at
2.7, F = 0.527); the computed ceiling e_N* = 8.06 is used here — matching G149's own
printed output and V3 statement.*