# agentJJ — the transient fingerprint confronted: kicked deep-MOND systems above the RAR?

*agentJJ, 2026-06-11. The built EOM's one untested novel prediction (agentX §6b, R3; corrected by
agentFF [FF-2]) turned into an observational confrontation. Files: `agentJJ_transient_fingerprint.py`
→ `agentJJ_transient_fingerprint.out` (RAR placements with real numbers). Inputs read first:
`agentX_sk_gate.md` (the ×2.32 transient, the adaptive-window construction, N_cyc), 
`agentFF_x_hostile_audit.md` (the per-event co-payment ×7–34 on quiet worldlines; the integrable
t^(−1/3) onset), `agentM_milgrom2022_gauntlet.md` (M22 conventions). Both footings carried
(a0_fw = 9.36e-11, a0_canonMOND = 1.2e-10); C3 fence n/a (all laboratories z ≈ 0). Per the standing
working rule: any "data contradict the fingerprint" claim below is checked against convention
artifacts (footing, Υ, EFE treatment) before being reported. No git.*

**STATUS: COMPLETE — relaunch-continuation 2026-06-11 (prior agent died after §0); all sections
computed and banked. VERDICT (§8): CONFRONTED on the headline — the transplanted "+0.37 dex above
the RAR" is dead at ~11σ (TDGs sit 0.63–0.68 ± 0.09 BELOW the isolated RAR); the construction's own
EFE-embedded predictions PASS (the external line erases the enhancement: predicted +0.02…+0.07 dex);
NON-DIAGNOSTIC between the two operator readings of (X-4) found split here (IMPL vs COMP — the ×2.32
was a prescribed-μ statement, not an action-EOM result); the live regime for the positive branch =
ISOLATED young rotators, registered as watch entry 13.**

---

## 0. The prediction being confronted (verbatim lineage)

agentX §6b (machine-measured, banked): a deep-MOND worldline whose forcing steps up (x: 0.1 → 1.0)
responds with the STALE window's μ — i.e. temporarily ENHANCED MOND behavior — with response
enhancement μ_loud/μ_ret = **×2.32** immediately post-step, decaying with half-life 1.2 cycles
(0.15 N_cyc), full window refill ~N_cyc cycles. Invisible at high x (μ ≡ 1 regardless of window
state). agentFF [FF-2] hardened the energetics side: on a QUIET deep-MOND worldline the per-event
medium co-payment is ×7–34 the external work (not X's geometry-specific ~1%), and the onset is an
integrable t^(−1/3) spike — finite physics. agentX R3: "falsifiable in principle, unconstrained by
current data." This memo tests that last clause.

(Sections 1–9 below; appended incrementally as computed, per the relaunch discipline.)

---

## 1. Gates — machinery certified before any new use (run §[0])

All three gates **PASS** (`agentJJ_transient_fingerprint.py 0`):

- **(a) the banked fingerprint reproduced:** agentX §6b geometry re-run with the same single-stage
  machinery: enhancement μ_loud/μ_ret(0+) = **2.320** (banked 2.32), half-life **1.2 cycles** (banked
  1.2), pre-onset deviation **1.0e-2** = window ripple (banked 1.0e-2). Asserted, not eyeballed.
- **(b) full regression rerun:** `agentX_sk_dynamics.py` rerun end-to-end 2026-06-11 →
  **byte-identical** to the banked `.out` (shell `diff` clean; sha256[:16] = `3f6f4fa67b8aeac1` both).
- **(c) the SPARC conventions locked:** agentCC/mi_f4 baseline reproduced exactly before the SPARC
  locus is used: fw a0 = 9.36e-11 → Ud = 0.52, dex RMS 0.1950; canon a0 = 1.2e-10 → Ud = 0.46, RMS
  0.1977 (both match the locked rows to print precision).

## 2. A structural finding met on the way in: the construction's transient response is operator-form-split

Found while porting the banked integrators (reported per house rule, before any data): the corpus
carries **two readings of (X-4) that agree on loaded windows but disagree at an empty one** —

- **COMP form** (the action-derived EOM, agentX `run_driven`, used for §6c-i/ii/iii):
  m·z̈ + Σ_ch (μ_ch − 1)[z̈]_ch = F. With an **empty window** the filter-bank reconstruction
  [z̈]_ch ≈ 0, so the MI correction **vanishes**: the onset response is **NEWTONIAN** (a = F),
  rising to the settled MOND value **from below** as the window fills.
- **IMPL form** (agentX §3c-iv, ported approvingly by agentFF [FF-2a/2b]): a·μ(A_ret(a)) = F with
  the own term in its own window (θ(1) = 1). With an empty window μ is evaluated near zero: the onset
  response is **ENHANCED** — the integrable t^(−1/3) spike agentFF measured — decaying to settled
  **from above**.

The equivalence claimed in (X-4), "m z̈ + Σ(μ−1)[z̈]_ω = F ⟺ m μ∘z̈ = F", holds only when the filter
bank reconstructs the worldline (Σ_ch [z̈]_ch = z̈); a stale or empty window breaks it. **The SIGN of
the transient fingerprint is therefore an unfixed convention of the construction, alongside N_cyc** —
neither agentX nor agentFF flagged this (each used one form where it was natural).

**The machine then overruled this memo's own first guess** (recorded per house rule): the draft
assumed the two forms at least agree on the §6b stale-but-LOADED step, making ×2.32 form-robust.
They do not (run §[1-bridge], x: 0.1→1.0 step, N_cyc = 8, both integrators on the loaded window):

| form | response/settled at 0.5 / 1 / 2 / 4 / 8 / 16 / 40 cycles |
|---|---|
| IMPL | **2.30** / 2.24 / 1.99 / 1.58 / 1.23 / 1.04 / 0.99 — the banked ×2.32, decaying on the window |
| COMP | **0.70** / 0.71 / 0.71 / 0.73 / 0.79 / 0.88 / 0.97 — rises monotonically FROM BELOW; no boost at all |

The banked "×2.32 response enhancement" (agentX §6b, R3) is a **prescribed-μ statement** — response
*assumed* = F/μ_ret — i.e. the IMPL reading; it was never integrated through the action EOM. Under
the literal (X-4) EOM the stale window's comp term is the OLD amplitude, so a = F + (1−μ_stale)·comp
*under*-responds until the window refills (agentX's own §3c-iii kick, which WAS integrated in COMP
form, shows exactly this: no response boost, only the small flux event — the corpus's two transient
numbers were never about the same object). Consequence: every prediction below is computed in BOTH
forms, and the data confrontation adjudicates between them where it can.

## 3. The assembly transient quantified (run §[1]) — quiet history, then turn-on

Self-consistent integrations of both forms, turn-on from rest at t = 0 (the agentFF step geometry),
observable = Δdex(t) = log₁₀(response envelope / settled response) — the vertical RAR offset a
rotation measurement at age t would read at fixed g_bar. Matrix: x_set ∈ {0.05, 0.1, 0.2} (the TDG
range), N_cyc ∈ {8, 16, 32}, preps ISOLATED (empty window, the e_N → 0 limit) and EFE-EMBEDDED
(standing external line e_g = 0.2 a0 at y_efe = 0.3, θ_A weight 1.83 → A_bg = 0.37 a0 — the real-TDG
regime, NGC 5291-pinned). Headline rows (x_set = 0.1; full grid in the .out):

| prep | form | Δdex at 0.25 / 0.5 / 1 / 2 / 4 / 8 orbits | character |
|---|---|---|---|
| ISO | COMP | −0.56 / −0.57 / −0.57 / −0.56 / −0.53 / −0.47 (N=8) | **Newtonian onset** (= log μ_set), refills over ~2.6 N_cyc/⟨d(xμ)/dx⟩ ≈ tens of orbits |
| ISO | IMPL | **≥+1.5** / ≥+1.2 / +0.56 / +0.33 / +0.17 / +0.05 (N=8) | t^(−1/3) spike (early marks dt-creeping, quoted as lower bounds); +0.20 dex per N_cyc doubling |
| EFE | COMP | −0.30 / −0.31 / −0.30 / −0.30 / −0.29 / −0.25 (N=8) | Newtonian onset = log μ(A_bg-pinned); N_cyc-insensitive at TDG ages |
| EFE | IMPL | +0.04 / +0.04 / +0.04 / +0.03 / +0.03 / +0.03 (x=0.1) | the external line PINS μ: enhancement capped at ≤ +0.07 dex (x=0.2), invisible |

Structure worth naming:
- **The EFE line acts as a transient regulator.** With e_N ≈ 0.2 standing in the window, the IMPL
  enhancement collapses from ≥+1.5 dex (isolated) to +0.02…+0.07 dex — *the same external field that
  suppresses the settled MOND boost also kills the assembly transient.* An observable fingerprint
  needs ISOLATED young systems; TDGs near their parents are the wrong laboratory for the POSITIVE
  branch (quantified in §6/§8).
- **The COMP (action-EOM) transient is large, negative, and slow** — at TDG ages it is simply the
  Newtonian floor, Δ ≈ log₁₀ μ_set ≈ −0.30 (EFE-embedded), nearly independent of N_cyc and x_set
  inside the bracket, because the own-channel window is still empty at <1 orbit and the deep-MOND
  refill time is ~N_cyc/⟨d(xμ)/dx⟩ ≈ 2.6 N_cyc orbits, with a further nonlinear early-time slowdown.
  Sharp, falsifiable: **young TDGs should show g_obs ≈ g_bar (Mdyn/Mbar ≈ 1) under this reading.**
- θ-shape dependence (θ_A vs exp tails): ±0.03 dex on the EFE-embedded curves — subdominant.
- dt-honesty: ISO/IMPL 0.25–0.5-orbit marks creep +0.06 dex per dt halving (spike tail) — lower
  bounds only; all EFE-embedded marks dt-stable to <0.01 dex.
- v²-based curves (the toy's velocity memory) are reported in the .out but not used for the verdict:
  the 1D toy cannot phase-mix the spike's parked impulse; real discs re-virialize.

## 4. The realistic TDG preparation (run §[2]) — parent-disc memory loaded, and a ghost

The TDG's material was not quiet before assembly: it orbited the parent's outer disc at x_par ~
0.5–1, T_par ≈ 0.6 T_int, ejected ~0.1–0.5 Gyr pre-condensation. The remembered line (θ_A(1.65) =
0.54 weight, ×0.9 ejection-lag fade) added to the EFE prep:

| form | x_par | Δdex_w0 (w0-coherent) at 0.25 → 8 orbits | note |
|---|---|---|---|
| COMP | 0.5 / 1.0 | **−0.305 → −0.27** (all N_cyc; identical to no-parent COMP) | memory can't move a response the empty own-channel already decoupled from μ |
| IMPL | 0.5 | −0.039 → −0.02…−0.04 | suppression via A; decays on N_cyc·T_par |
| IMPL | 1.0 | **−0.085 → −0.05…−0.08** | ditto, ~2× deeper; par_fade 0.9→0.7 scales it ×0.79 |

**Bug log (caught in-run):** the first-draft broadband RMS envelope showed COMP+parent at
+0.31…+0.49 dex — not a rotation boost but the **(μ_par−1)·comp_par ghost force**: under the COMP
form the worldline keeps being forced at the REMEMBERED parent frequency while that window drains
(amplitude (1−μ_par)·x_par·fade ≈ 0.3 = ×6 the internal drive, decaying on N_cyc·T_par). A
velocity-field fit reads that as non-circular motion / inflated σ_HI, not Vrot — the verdict
observable was switched to the w0-coherent amplitude (trailing least-squares with the ghost line
included in the design matrix). Two corollaries worth registering: (i) the COMP form predicts
freshly-assembled systems RING at remembered frequencies — direction-compatible with Lelli+15's own
note that the NGC 5291 dwarfs' σ_HI ≈ 20 km/s "may indicate unresolved non-circular motions"
(direction-compatible only; NOT claimed as evidence); (ii) the IMPL form has no ghost channel at all
(memory enters only through μ) — a third qualitative form-discriminant.

So the realistic-prep does NOT rescue a positive fingerprint for these objects: at the sample's ages
the construction predicts (per form, w0-coherent, x_set ≈ 0.05–0.2, any N_cyc ≥ 8):

> **COMP: Δ ≈ −0.27…−0.33 dex below the settled EFE locus (i.e. g_obs ≈ g_bar, Mdyn/Mbar ≈ 1).**
> **IMPL: Δ ≈ +0.04 (no parent memory) to −0.09 (full parent memory) — observationally settled.**

## 5. Physical-time conversion (run §[3])

For T_orb = 0.3/0.5/1 Gyr (the TDG/dwarf range; sample T_orb ≈ 0.7–2.3 Gyr): the IMPL/ISO positive
transient stays |Δ| > 0.1 dex for 6.75/12.5/23.75 orbits (N_cyc = 8/16/32) = 2.0–24 Gyr — alive in
any young isolated dwarf but ERASED by an e_N ≈ 0.2 external field (IMPL/EFE never exceeds +0.07 dex). The
COMP negative state is far longer-lived: |Δ| < 0.1 dex only after ~29–114 orbits (EFE prep) — the
deep-MOND window refill runs at ~2.6 N_cyc/⟨d(xμ)/dx⟩ orbits with a nonlinear early stall, so a
fast-assembled dwarf would stay quasi-Newtonian for ~9–114 Gyr depending on (N_cyc, T_orb).
Adiabatically-grown settled dwarfs are untouched by both readings (their windows were never empty) —
no conflict with the locked SPARC baseline.

## 6. The data (run §[4]) — the six Lelli+2015 TDGs on the RAR

**Provenance.** Lelli+2015 A&A 584 A113 (ar5iv 1509.05404, fetched 2026-06-11): Table 1 (D = 62 /
66.5 / 17 Mpc; ages: NGC 5291 ring ~360 Myr, NGC 7252 merger ~600–700 Myr, VCC 2062 0.5–1 Gyr),
Table 7 (Rout, Vrot, i, σ_HI, Vcirc = asymmetric-drift-corrected; **t_merg/t_orb = 0.5/0.2/0.3/0.3/
0.2/0.4–0.8 — every TDG is ≤ 0.8 internal orbits old**, exactly the fingerprint's live window),
Table 8 (M_HI, M*, M_mol, M_bar, M_dyn, M_dyn/M_bar). External fields: NGC 5291 trio **PINNED** from
Gentile+2007 (0706.1976): g_ext ≈ 0.2 a0 (≤ 0.3 a0) at separations 58–75 kpc → g_ext = 2.4e-11 SI
[1.2–3.6e-11]; NGC 7252 (V 180–260 km/s, d 50–90 kpc) and VCC 2062 (NGC 4694: V 80–140, d 15–30 kpc)
are literature **BRACKETS, marked UNPINNED**. g_obs = Vcirc²/Rout; g_bar = G·Mbar/Rout² (spherical;
geometry confound §7d). Cross-check: g_obs/g_bar reproduces Lelli's published Mdyn/Mbar per object
(1.45/1.29/1.23/0.87/0.96/1.11 vs 1.5/1.3/1.2/0.9/1.0/1.0) — the table transcription is verified.

Per-TDG placements (errors: V, M, R propagated with the R-correlation through each prediction's
local slope):

| TDG | g_bar (SI) | g_obs (SI) | g_obs/g_bar | age/orbits | e_N (can/fw) |
|---|---|---|---|---|---|
| NGC 5291N | 9.44e-12 | 1.37e-11 | 1.45 | 0.55 | 0.20 / 0.26 |
| NGC 5291S | 4.28e-12 | 5.51e-12 | 1.29 | 0.28 | 0.20 / 0.26 |
| NGC 5291SW | 4.30e-12 | 5.29e-12 | 1.23 | 0.34 | 0.20 / 0.26 |
| NGC 7252E | 2.69e-12 | 2.33e-12 | 0.87 | 0.42 | 0.18 / 0.24 |
| NGC 7252NW | 1.93e-12 | 1.86e-12 | 0.96 | 0.29 | 0.18 / 0.24 |
| VCC 2062 | 2.89e-12 | 3.19e-12 | 1.11 | 0.75 | 0.17 / 0.21 |

**Weighted-mean offsets Δ = log₁₀(g_obs/g_pred) (six TDGs):**

| reference locus | fw footing | canon footing |
|---|---|---|
| ISOLATED settled RAR | **−0.634 ± 0.086 (−7.4σ)** | **−0.683 ± 0.086 (−7.9σ)** |
| QUMOND-radial EFE (repo convention), g_ext mid | −0.102 ± 0.098 (−1.0σ) | −0.134 ± 0.098 (−1.4σ) |
| M22-native EFE (θ-weighted shiluta, per-TDG y_efe) | −0.238 ± 0.096 (−2.5σ) | −0.273 ± 0.096 (−2.8σ) |

EFE-bracket sweep (canon): QUMOND −0.230 (g_ext lo) → −0.075 (hi); M22-native −0.346 (lo) → −0.213
(hi). So under the repo QUMOND convention the sample is **fully consistent with settled EFE-MOND**
within the g_ext bracket; under the framework-native M22 EFE (which suppresses *less* — its locus
sits 0.1–0.2 dex higher) the sample runs 2.2–3.6σ low unless helped by the transient suppression
(§4) or the high-EFE end. The two conventions differ here for a NAMEABLE physical reason: M22's EFE
is frequency-keyed — the external line enters with weight θ(Ω_ext/Ω_int), and these slow rotators
have T_int comparable to their orbital period around the parent (y_efe ≈ 0.3–1.0 → θ_A ≈ 1.0–1.9 <
θ(0) = 2), so the M22 EFE *weakens* exactly where QUMOND's field-strength-keyed EFE does not. TDG
samples are therefore an EFE-convention discriminator in their own right — at six objects the data
lean QUMOND-ward (or demand the §4 suppression on top of M22-native), at 2.2–2.8σ: suggestive, not
decisive.

**Zero-point honesty (working rule, both ways).** The SPARC band locus (locked conventions, g_bar ∈
[2e-12, 1.1e-11]): whole-band median offset −0.000 (fw) / −0.028 (canon) — the analytic curve centers
the band. But the settled-DWARF subset sits below it: median −0.142/−0.182 (all dwarf points),
**−0.116/−0.159 (dwarf OUTERMOST points — the like-for-like comparison set)**. Referenced to the
empirical settled-dwarf outer locus instead of the analytic curve, every TDG offset above moves UP by
+0.12…+0.16 dex: the vs-ISO deficit becomes ~−0.51 (still ≥ 6σ), vs-QUMOND-EFE becomes ~+0.02…+0.05
(dead-center settled), vs-M22-EFE becomes ~−0.11…−0.15 (~1.2–1.6σ). **No deficit claim survives at
>3σ under every reasonable convention choice simultaneously; the BELOW-ISOLATED-RAR placement
survives them all.**

"Published consensus says TDGs are roughly MOND-consistent" — quantified: **'roughly' = −0.13 ± 0.10
dex from the settled QUMOND-EFE locus (canon, mid g_ext), with a −0.23…+0.05 spread across the
g_ext bracket × zero-point choice.** Gentile+2007's MOND fit of the NGC 5291 trio was an
EFE-included fit — consistent with this placement, not with the isolated RAR.

## 7. Confounds, quantified (run §[5])

- **(a) The EFE is the dominant term, opposite-signed to the enhanced fingerprint.** Per TDG it moves
  the expectation −0.41…−0.69 dex (QUMOND) / −0.32…−0.48 (M22-native) below isolated — ×3–10 the
  size of any surviving transient signal. Any TDG test of the transient is a test *on top of* the
  EFE model; the two are separable only because the transient is age-keyed while the EFE is
  geometry-keyed (the §8 future test exploits exactly this).
- **(b) Out-of-equilibrium Newtonian expectation: UNPINNED** (no simulation source within the fetch
  budget; kicked self-gravitating systems can scatter V²/R both ways). Pinned in its place: Lelli+15's
  own statements — "less than a full rotation since the interaction", equilibrium "unclear",
  t_merg/t_orb = 0.2–0.8. The 1D toy isolates window physics from kinematic startup by construction
  (cos-phase startup has no amplitude transient in the settled law); real 2D radial readjustment and
  phase mixing enter the data as extra scatter, not as a sign-definite bias this memo may claim.
- **(c) Inclination** (Lelli's dominant systematic; Table 7 errors already include their adopted Δi):
  a ∓15° error swings g_obs by +0.21/−0.12 dex (5291N) … +0.30/−0.18 (VCC 2062, i = 45°). Inclination
  would need to be wrong by ≳15° **coherently across six objects in three independent systems** to
  manufacture or hide a 0.2-dex mean shift — possible for any one object (cf. AGC 114905), not
  plausibly coherent.
- **(d) Mbar geometry factor** (spherical vs thin-disc edge vs gas beyond Rout): ±0.06 dex on the
  means — subdominant.
- **(e) Vrot vs Vcirc:** raw-Vrot offsets are all LOWER (mean −0.44 vs QUMOND-EFE): the
  asymmetric-drift-corrected Vcirc is the **conservative** choice for testing an enhancement.
- **(f) Υ\*:** gas fractions 0.78–0.93 → doubling Υ\* moves g_bar < 0.06 dex — the usual Υ fork is
  **moot** here (the working-rule's Υ check passes trivially).

## 8. VERDICT

**CONFRONTED on the headline; NON-DIAGNOSTIC between the construction's two operator readings; the
positive branch's live regime identified and registered (watch entry 13).** Component by component,
each checked against the convention forks before being stated:

1. **The naive transplanted prediction — "young TDGs sit up to +0.37 dex ABOVE the RAR" — is DEAD,
   and robustly so.** Measured: **−0.63…−0.68 ± 0.09 dex BELOW the isolated settled RAR (7.4–7.9σ)**;
   the gap to +0.37 is ~11σ. Survives both footings (Δ between them 0.05), both EFE conventions
   (this row has none), the zero-point fork (−0.51, ≥6σ at the most generous), Υ (moot), geometry
   (±0.06), inclination-coherence, and the V-choice (Vcirc is the pro-enhancement choice). But the
   honest frame: that number was never the construction's TDG prediction — it is what §6b's ×2.32
   becomes if transplanted ignoring (i) the standing external field and (ii) the operator-form
   question. This memo computed the actual predictions; the transplant is retired, not strawmanned.
2. **The construction's actual predictions at the sample's ages (0.2–0.8 internal orbits,
   e_N ≈ 0.2) are form-split** (§2–§4): IMPL ⇒ +0.02…+0.07 dex (parent-memory variant −0.04…−0.09);
   COMP ⇒ −0.27…−0.33 dex (quasi-Newtonian floor, N_cyc-insensitive). **The data land between and
   cannot convention-robustly kill either** (run §[6]): vs the QUMOND-EFE locus the best fit is
   IMPL+parent (0.1–0.4σ; COMP runs 1.8–2.1σ high); vs the M22-native-EFE locus the best fit is COMP
   (0.4–0.8σ; IMPL-no-parent runs 2.8–3.1σ low). The worst case anywhere is 3.1σ (IMPL-no-parent ×
   M22-EFE × canon), erased by the zero-point shift (+0.15) or the parent-memory term or the QUMOND
   convention. χ² of the six offsets about their mean = 0.7–1.4 / 5 dof — quoted errors conservative
   (the offsets are internally over-consistent; no hidden scatter). Per the working rule this is
   reported as **NON-DIAGNOSTIC**, not dressed up as a kill of either reading.
3. **What the sample DOES establish:** (i) TDGs at <1 internal orbit show **no transient MOND
   enhancement at the ≳+0.1-dex level** in an e_N ≈ 0.2 environment — consistent with the
   construction's own EFE-regulated prediction (+0.02…+0.07), and a hard cap on any enhancement
   mechanism that survives an external field; (ii) the sample **re-confirms the settled EFE
   phenomenology from a new direction** (the deficit vs isolated RAR is EFE-shaped and EFE-sized,
   echoing agentCC's environment-keyed theme — and the QUMOND-radial convention fits it better than
   the M22-native θ-weighted EFE, a 0.1–0.2-dex convention gap now measured on real objects);
   (iii) agentX R3's "unconstrained by current data" is now false in the EFE-embedded regime —
   constrained and passed there; still true in the isolated regime.
4. **Where the fingerprint is actually testable (pre-registered, watch entry 13):** the IMPL/ISO
   branch predicts **+0.3…+1.9 dex** (N_cyc 8–32; ≥ +1.4 in the first half-orbit) for *isolated*
   young deep-MOND rotators (e_N ≲ 0.05, age ≲ 2 internal orbits), decaying over 7–24 orbits; the
   COMP branch predicts the
   opposite for the same objects: **quasi-Newtonian g_obs ≈ g_bar for tens of orbits**; settled MOND
   predicts on-RAR. Three readings, three separated loci, ≥0.3 dex apart — a SINGLE age-dated
   isolated young dwarf with a resolved HI curve and pinned inclination adjudicates all three. The
   deficit channel alternatively sharpens with sample size: at current per-object quality, N ≈ 12
   TDGs separates the COMP floor from settled-EFE at 3σ (gap 0.21 dex vs σ_mean 0.07). Secondary
   COMP-only discriminant: the ghost-ringing channel — inflated σ_HI/non-circular power at the
   remembered parent frequency, decaying over N_cyc·T_par (direction-compatible with the observed
   σ_HI ≈ 20 km/s in NGC 5291N; not claimed as evidence).

**Both-ways honesty.** Framework-favorable reading: the construction *passes* its first data contact
in the regime the data actually probe — its own EFE machinery predicted the near-settled placement
the sample shows, and the structural finding (the form split) was caught by this confrontation
rather than by a referee. Hostile reading, equal weight: the confrontation has no discriminating
power where the construction is novel — the EFE term the framework needs for survival here is also
what hides its new physics; the form split means the corpus's most-advertised "falsifiable novelty"
(the ×2.32) was not a prediction of the built EOM at all but of a shorthand reading of it, and until
N_cyc *and* the operator form are fixed by something, the "fingerprint" spans a sign flip. Nothing
in this memo derives Z, a0, or the tail; the TDG pass is a pass of MOND+EFE phenomenology generally,
not of this framework specifically.

## 9. Chain bookkeeping, patches, bug log

**Patches applied (one line each, no git):**
- `DERIVATION_CHAIN.md` Link 6: the JJ sentence appended (transient fingerprint confronted; form
  split named; TDG cap; isolated regime open).
- `TOE_STATUS_AND_DOORS.md` live door 3 (JJ): marked REPORTED with the verdict line.
- `data_watch/WATCHLIST.md`: **entry 13** added (the isolated-young-rotator three-way discriminator
  + the N≈12 TDG deficit channel).
- agentX R3's clause is corrected *here* (this memo is the citable correction; agentX's memo left
  verbatim per the no-rewrite discipline).

**Bug log (all caught in-run, none in banked output):** (i) first-draft broadband-RMS observable
read the COMP ghost ringing (+0.31…+0.49 dex) as a rotation boost — replaced with the w0-coherent
trailing-LSQ extraction (the ghost line included in the design matrix); the ghost itself promoted to
a named COMP-only observable. (ii) the §2 draft asserted the two forms agree on loaded windows —
machine-overruled by the bridge run (×2.30 vs ×0.70); text corrected, finding upgraded. (iii) the
first bridge implementation pre-loaded a twin channel at w0(1+1e-9) — double-counts via θ(1) = 1;
replaced with a same-channel preload. (iv) IMPL/ISO 0.25–0.5-orbit envelope marks creep +0.06 dex
per dt halving (the spike's dt^(1/3) tail) — quoted as lower bounds; all EFE-embedded marks stable
to <0.01 dex. (v) sec2's dead "phase spot-check" print replaced with the par_fade sensitivity row.

**Citations:** Lelli, Duc, Brinks, McGaugh et al. 2015, A&A 584, A113 (arXiv:1509.05404) — the TDG
sample, Tables 1/7/8, the t_merg/t_orb column, the equilibrium caveat. Gentile, Famaey, Combes,
Kroupa, Zhao, Tiret 2007, A&A 472, L25 (arXiv:0706.1976) — the NGC 5291 MOND+EFE analysis, g_ext ≈
0.2 a0 (≤0.3), separations 58–75 kpc, baryonic masses. Bournaud et al. 2007 (Science 316, 1166) —
the NGC 5291 trio discovery data (used via Lelli/Gentile re-analysis, not refetched). Milgrom 2007
(the TDG MOND prediction letter) — pointer only, via Lelli's citation. In-repo: agentX_sk_gate.md
(+ .py twins), agentFF_x_hostile_audit.md, agentM_milgrom2022_gauntlet.md (conventions),
agentCC_astar_hunt.md (locked SPARC baseline + EFE-vs-floor precedent), SPARC rotmod files
(data/sparc_data/, Lelli+2016).

**STATUS: COMPLETE — verdict final, watch entry registered.**
