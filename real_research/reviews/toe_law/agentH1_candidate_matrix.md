# Agent H1 — the spec sheet vs every published field-level candidate (the candidate matrix)

*Agent H1 for C. Zimmerman, 2026-06-10. Task: confront the non-Huygens door's spec sheet
(`NONHUYGENS_DOOR_SYNTHESIS.md` + `TOE_TRILEMMA.md`) against every published FIELD-LEVEL candidate that could host
the missing object. Literature pulled and pinned this session (arXiv ids verified by fetch unless marked
[repo-banked] or [standard-pin]); no new computation run — this is a confrontation memo, and every repo number it
uses is quoted from the banked artifact that computed it. Both ways at full weight throughout, per the project #1
working rule: a candidate's "fails" is sourced as rigorously as its "works", and convention-sensitivity is flagged
wherever it could flip a cell. **One id correction to the commissioning prompt, recorded first:** the prompt's
"arXiv:1602.08831" resolves to a condensed-matter defect-pattern paper (Azadi–Grason); the intended companion is
**arXiv:1602.05961** (Khoury, "Another Path for the Emergence of Modified Galactic Dynamics from Dark Matter
Superfluidity," PRD 93, 103533), scored below as its own row. No git.*

---

## 0. The eight spec items, operationalized (what a cell must mean before any row is scored)

The spec is the residue of the bath-mechanism closure (agentN1–N5 + agentE + agentD + the lensing program). Each
item below carries its repo source and the exact number a candidate must meet. **The matrix is GATED, not
additive**: items 4–7 are pass/fail data gates (a NO on any of them is a kill or a standing wound), items 1–3 are
structural-spec matches (what the swarm *derived* the object must be), item 8 is a liability-vs-prediction
differentiator. A high YES-count with the wrong NO is a dead candidate — the calibration rows (§3) demonstrate
this on purpose.

| # | Item | Operational test | Repo source |
|---|---|---|---|
| 1 | **Inertia-DEFICIT sign growing toward low a** | The matter-sector modification is a *deficit in effective inertia* (response boost), growing monotonically toward low acceleration — N3's m²<2H² tail structure, the program's only right-signed bath channel. Right sign via an extra *force* is scored NO\* (sign ✓, lever ✗): on circular orbits μ(a)·a = g_N and a = g_N/μ are equivalent, but they separate exactly where the repo's kill-tests live (solar reflex, eccentric orbits, EFE class). | `agentN3_tail_scale.md` §2; `NONHUYGENS_DOOR_SYNTHESIS.md` item 1 |
| 2 | **Acceleration-keyed galactic dynamics, frequency dressing inside p∈[0.07,1]** | (a) The galactic law keys to acceleration — pure frequency-keying is SPARC-DEAD (+0.023 dex, 5.2σ sign-flipped V_flat structure); (b) any frequency dependence sits inside the corridor p∈[0.069, ≥1] as a₀-dressing, OR solar protection is achieved by an explicit alternative mechanism (p=0 is corridor-legal iff the solar budget is met some other way — the McGaugh-shape undressed PASS is the existence proof). | `agentN5_freq_vs_accel.md` §2, §4 |
| 3 | **A knee scale mc² ∈ [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV** | The candidate contains an ultralight field in N2's window (knee ϰ ∈ [2.0×10⁻¹⁴, 2.5×10⁻⁹] s⁻¹; hostile ceiling 2.6×10⁻²⁵ eV) — the one new scale the dS kernel cannot supply; Gaia DR4 WB amplitude = knee-position discriminator (split ~5×10⁻²⁸ eV). | `agentN2_memory_langevin.md` §4 |
| 4 | **Lensing carried by the theory** | The lensing-inferred g_obs follows the SAME MOND-amplitude RAR as kinematics (Brouwer+2021 released ESD: data continue smoothly from kinematic to lensing RAR down to g_bar ~ 10⁻¹³, radii ~Mpc). The 40.5σ wall excluded *baryon-only* (metric-passive) lensing — deep-bin amplitude deficit ~230×; the spec item is stronger: the theory must *carry* the MOND-shaped continuity, not merely add mass. | `f4_lensing_wall.out`; `TOE_STATUS_AND_DOORS.md` Door II |
| 5 | **Cassini Q₂ < ~5×10⁻²⁷ s⁻²** | The EFE quadrupole vs Park–Hees–Famaey 2026: Q₂ = (1.6±1.8)×10⁻²⁷, 2σ window [−2.0, +5.2]×10⁻²⁷ (arXiv:2602.17884). The AeST/DEW killer; binds every modified-gravity host with an AQUAL/QUMOND-like static limit and a RAR-compatible function (Desmond trade-off, arXiv:2401.04796). | `CASSINI_QUADRUPOLE_CONSTRAINT.md`; `agentD_dew_quadrupole.md` |
| 6 | **Solar-reflex budget (agentE)** | Anomalous solar response at the Jupiter-synodic carrier δa☉ ≤ 2.47–3.38×10⁻¹⁵ m/s² (the survival line s < (0.34–0.40)·a₀ killed instantaneous acceleration-keyed MI at ×8.5–×251). Binds inertia-side candidates directly; modified-gravity candidates pass by class (their solar exposure is item 5). | `agentE_solar_reflex.out`; `agentN5` §4 |
| 7 | **SPARC scatter within ~0.01 dex of McGaugh at a₀=9.36×10⁻¹¹** | 175-galaxy unweighted dex-scatter within +0.010 of the 0.1950 reference (locked conventions of `mi_f4_sparc_shape_test`), as a LAW — per-galaxy hidden freedom (boundary conditions, halo parameters) that merely *accommodates* the RAR scores OPEN at best. | `agentN5` §1; `mi_f4_sparc_shape_test.out` |
| 8 | **The ~9σ early/late lensing split: liability OR prediction** | Brouwer u−r split 8.8σ raw (+0.261 dex, early ABOVE late in 15/15 bins), survival 8.6–9.2σ after measured per-class conversion (Sérsic axis 5.6–6.3σ corroborates); gas escape needs differential M_gas/M\*≈1.1, eROSITA-disfavoured below logM\*=11. Type-blind universal laws owe an answer (liability); a candidate with a structural reason for type-dependence can score it as a PREDICTION. | `lr_battery_results.md`; `agentH_perclass_C.md` |

Convention guard (the #1 rule, applied to this memo): the SFDM family's own fiducial phonon scale is
a₀ = 0.87×10⁻¹⁰ m/s² (Mistele+ 2303.08560, quoting the BFK originals) — *closer to the framework footing
9.36×10⁻¹¹ than to the MOND default 1.2×10⁻¹⁰* (they pick it low because the condensate's Newtonian pull a_SF
adds on top). No cell below depends on the footing choice; where a published tension was checked against
parameter freedom, the source's own robustness statement is quoted (e.g. 2303.08560 App. C: "different choices
for these parameters can change the numerical details but cannot avoid the general problem").

---

## 1. The matrix — summary grid

Y = meets as specified · Y\* = meets with a named flag · N = fails/contradicts · N\* = fails the spec's lever but
not its sign · O = open/uncomputed (lean noted in the row detail). **Live** = no decisive published or repo-banked
gate failure.

| Candidate (pinned) | 1 sign/lever | 2 accel-key | 3 knee | 4 lensing | 5 Cassini | 6 reflex | 7 SPARC | 8 split | firm YES | status |
|---|---|---|---|---|---|---|---|---|---|---|
| **BK superfluid DM** (1506.07877, 1507.01019; BFK 1711.05748; review 2505.23900) | N\* | Y | N | **N** | O | Y | O(N-lean) | **O — phase prediction** | 2/8 | live-wounded (lensing) |
| **"Another path" SFDM** (1602.05961) | N\* | Y\* | N | **Y\*** | O | O(Y-lean) | O | O — phase | 2/8 (+2 starred) | live-untested |
| **Two-field SFDM** (Mistele 2009.03003; 1909.05710) | N\* | Y | N | N | O | Y | O | O — phase | 2/8 | live-wounded (same lensing) |
| **BIDM** — baryon-interacting DM (FKP 1712.01316; FKPS 1912.07626) | N | Y\* | N | O | Y | Y | O | O(pred-lean) | 3/8 | live; not a host for the kernel |
| **Pure fuzzy/ULDM** (Lee+ 1901.00305; Hlozek+ 1410.2896; Rogers–Peiris 2007.12705) | N | N | N\* | N\* | Y | Y | N | O | 2/8 | live as ΛCDM-variant; not a MOND host |
| **Baryon-correlated DM EFT** (Kamada 2605.20217, May 2026) | N | O | O | O | O | O | O | O | 0/8 | too new — all gates open |
| **Dipolar DM** (Blanchet–Le Tiec 0804.3518/0901.3114; bimetric 1504.00870) | N\* | Y | N | Y\* | N\* | Y | Y\* | N | 4/8 | **completion dead** (2302.02690) |
| **Emergent gravity / CEG** (Verlinde 1611.02269; Hossenfelder 1703.01415) | N | N | N | Y\* | **N** | N | O | N | 1/8 | **dead** (Hees+ 1702.04358, ×10⁷) |
| **AeST** [calibration] (Skordis–Złośnik 2007.00082) | N | Y | Y\* | **Y** | **N** | Y | Y | N | 5/8 | **dead** [repo-banked Cassini] |
| **DEW** [calibration] (1106.4984; 2512.10513) | N | Y | N | Y | **N** | Y | O(Y-lean) | N | 4/8 | **dead** [repo agentD, 8.8–14.6σ] |

**Read the grid honestly: the best LIVE score is 3/8 firm (BIDM, and its YESes are the cheap solar cells); the
only 5/8 row is AeST, which is dead at the exact gate the spec named as the killer. No row — live or dead — meets
items 1 or 3 at all.** That last fact is the matrix's sharpest output: the two ingredients the swarm *derived*
(the inertia-side lever; the ultralight knee field in [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV) exist in **no published
field-level candidate, anywhere**, including the dead ones.

---

## 2. Row details (every cell's one-line basis, arXiv-pinned)

### 2.1 Berezhiani–Khoury superfluid dark matter — the headline row
*Pins: PLB 753 (2016) 639 [1506.07877]; PRD 92, 103510 [1507.01019]; Berezhiani–Famaey–Khoury JCAP 09 (2018) 021
[1711.05748]; finite-T two-fluid EOS Sharma–Khoury–Lubensky JCAP 05 (2019) 054 [1809.08286]; fragmentation update
Berezhiani–Cintia–Khoury PRD 107, 123010 [2212.10577]; Physics Reports review (2026) [2505.23900]. Hostile tests:
Mistele–McGaugh–Hossenfelder JCAP 09 (2023) 004 [2303.08560]; Mistele 2201.07282; Cherenkov 2103.16954 +
2208.14308; acausality Hertzberg–Litterer–Shah JCAP 11 (2021) 015 [2105.02241]; MW vertical Jeans Lisanti+
1812.08169 + 1911.12365.*

| # | Score | Basis (one line) |
|---|---|---|
| 1 | **N\*** | Phonon-mediated extra FORCE a_θ = √(a₀ a_b) on baryons (1507.01019) — right MOND sign, grows toward low a_b, but gravity-side lever; no inertia structure (the spec's item is the N3 deficit). |
| 2 | **Y** | Keyed to the baryonic Newtonian acceleration (QUMOND-flavored ν(y)=1+1/√y inside the core; 2303.08560 eq. 2.2–2.8); static force, p=0, corridor-legal because solar protection is by phase (item 6), not frequency — N5's pure-frequency kill does not touch it. |
| 3 | **N** | DM is an eV-scale axion-like particle with strong self-interactions (fiducial m²/α = 0.18 eV², β=2; 2303.08560 §2 quoting BFK) — ~24 decades above the knee window; no field in [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV; the WB discriminator structure is replaced by core-radius/phonon-EFE structure (uncomputed). |
| 4 | **N** | Phonons do not couple to photons (GW170817 protection); lensing = GR + condensate/halo mass only; on the *same Brouwer+2021 KiDS data as the repo's wall*: "the lensing RAR almost never follows the MOND prediction", closest-match χ²_red = 15.0/14.9/28.7 (with 2 tuned parameters per galaxy) vs MOND 6.5 (zero parameters); kinematic→lensing continuity "unexpected"; verdict verbatim: "incompatible with the weak-lensing observations, at least in its current form" (2303.08560 §4–5). Both ways: it trivially clears the repo's 40.5σ *baryon-only* wall (it has DM mass — the ~230× deep-bin deficit is filled); what it fails is the MOND-amplitude continuity the data actually show. |
| 5 | **O** (lean Y-by-mechanism) | Named screen: the Sun's own field drives the local superfluid past its critical velocity — coherence lost within O(10²) AU, so no phonon force and no phonon-EFE tide on planets (1711.05748; 2505.23900 §7.2 "Solar system tests"). Qualitative; **no published Q₂ number exists**, and the kAU region where the repo's agentD analysis localizes the quadrupole source IS coherent — the matching across the decoherence bubble is uncomputed. Never faced the repo's Q₂ pipeline. |
| 6 | **Y** | No inertia modification (the Sun's response to g_N is GR) and the phonon force is locally off by the same decoherence — δa☉ from the new sector ≈ 0 by class+mechanism; agentE's budget binds MI, which SFDM does not have. |
| 7 | **O** (lean N) | 169 SPARC galaxies fit "reasonably well" BUT with an inverted M/L trend (giants systematically *lower* M/L than dwarfs — anti-stellar-population) and best fits living where the force is NOT MOND-like "without adjusting a boundary condition separately for each galaxy" (2201.07282); the kinematic RAR is not one-to-one (per-galaxy chemical-potential freedom + a baryonic-mass trend; 2303.08560 Fig. 3). It can *fit* the RAR; it does not *force* the 0.01-dex tightness as a law. The repo's exact 175-galaxy gate at the locked conventions: never run. |
| 8 | **O — PHASE PREDICTION (scored explicitly, per the task)** | The unique candidate with a *structural* reason for type-dependence: the MOND-like force exists only in the condensed phase; mergers/heating (early types' assembly) convert condensate to normal phase (1507.01019's galaxy/cluster split; 2212.10577's fragmentation/disruption machinery; 1809.08286's two-fluid fraction). Direction check, both ways: (i) the repo's split is *lensing-side* (early ABOVE late at fixed g_bar, +0.26 dex) — in SFDM lensing reads total mass, so the split maps to early types occupying heavier halos at fixed g_bar — natural for merger-built systems, qualitatively right-signed, **never computed**; (ii) the *sharp* SFDM prediction is a KINEMATIC type split (disrupted early types should sit on the CDM locus dynamically) — and the published MOND-compatibility of elliptical dispersions (review refs 399–401) cuts *against* the naive disruption story; both directions recorded. A bounded repo confrontation exists: score the phase prediction against `agentH_perclass_C`'s per-class numbers. |

**Family-level structural gates (not spec items, but they price adoption):** the zero-T phonon background is
unstable (acknowledged in 1507.01019; the finite-T/two-fluid program exists to fix it — 1809.08286); the
Lorentz-invariant completions "violate global hyperbolicity of the equations of motion in the MOND regime"
(2105.02241); star Cherenkov emission into the non-relativistic phonon mode "rules out part of the parameter
space, including the most commonly used parameters" (2103.16954; the review's §7.2 response: the EFT must break
down near stars anyway — the same decoherence that buys solar safety); the 2022 self-revision: thermalized halos
*fragment* into superfluid droplets with only the central soliton (up to a few tens of kpc) surviving tidal
disruption (2212.10577) — the coherent ~100 kpc core the 2015–2018 phenomenology assumed is no longer the
family's own default picture, and the review's "Kinematic observables" bullet concedes a detailed envelope study
is "required before a detailed fit ... can be performed outside the core."

### 2.2 Khoury's "Another path" (1602.05961) — the lensing-carrying family member
*The variant the commissioning prompt's mistyped id pointed at. Mechanism: higher-gradient superfluid corrections
+ spontaneous breaking of a discrete symmetry — unbroken (Einstein) at high acceleration, broken (MONDian
gravity) at low; symmetry restored wherever time derivatives dominate spatial gradients (cosmology is Einsteinian
on linear scales by construction).*

| # | Score | Basis |
|---|---|---|
| 1 | **N\*** | The MOND phase modifies the gravitational force law (gravity-side again); right sign, wrong lever. |
| 2 | **Y\*** | Galactic keying is to the acceleration (metric-gradient) regime via the phase boundary at a₀; *and the symmetric/Einstein phase is restored when time derivatives dominate* — a built-in high-frequency Einstein phase, structurally the closest thing in print to N5's frequency-dressed acceleration keying. Flag: no p has ever been computed; corridor compliance unchecked. |
| 3 | **N** | Same eV-scale superfluid constituent (m ~ eV, Λ ~ √(a₀ M_Pl) ~ meV; §2 of 1602.05961); no knee-window field. |
| 4 | **Y\*** | §6 constructs the relativistic version to ENFORCE Φ = Ψ — "required for dynamical and lensing mass estimates to coincide" — using the normal component's 4-velocity u^μ (no extra vector field): **the only superfluid-family member in which lensing follows the MOND force by design.** Flags, at full weight: the construction is from Feb 2016 — *pre-GW170817* — and its c_T audit has never been done (the axis that killed TeVeS; Boran+ 1710.06168 is the standing test for any "dark-matter emulator"); and the family acausality result (2105.02241) targets exactly these LI completions. |
| 5 | **O** | High-acceleration = symmetry-restored Einstein phase; if the restoration is sharp, this is the Hees+2016 sharp-function evasion realized physically rather than tuned — but the solar neighborhood's *external* field is g_ext ≈ 1.8–2.3 a₀ (broken phase at the kAU boundary), so the EFE quadrupole question transplants intact and has never been computed. |
| 6 | **O** (lean Y) | The Sun's reflex is a time-dependent perturbation; by the model's own phase criterion (time derivatives ⇒ symmetric phase) the anomalous response should vanish at the synodic carrier — uncomputed; agentE's transfer standard makes this a cheap bounded calculation. |
| 7 | **O** | No rotation-curve or RAR fits at any scale have ever been published for this variant. |
| 8 | **O — phase** | Same two-phase channel as 2.1, plus the acceleration-keyed phase boundary adds an environment keying; never computed. |

### 2.3 Two-field SFDM (Mistele 2009.03003; chemical-potential analysis 1909.05710)
Splits the phonon's two roles (energy density vs force mediation) between two fields — fixes the
equilibrium-vs-force tension, the stability problem "in a more elegant way", and evades the Cherenkov bound (the
matter-coupled mode radiates only weakly; 2208.14308). **The spec scores are otherwise row 2.1's**: lensing stays
N — the authors of 2303.08560 state §5 "we expect the same basic problems as in the original SFDM model: ... this
phonon force does not couple to photons ... no continuity between the kinematic and the lensing RAR"; items 5/6/8
inherit 2.1's mechanisms (O/Y/O-phase); item 7 inherits the 2201.07282 M/L inversion (the fits in that paper use
this two-field formulation's parametrization). Net: the refinement repairs *internal-consistency* gates, not one
spec gate. 2/8.

### 2.4 BIDM — baryon-interacting dark matter (Famaey–Khoury–Penco JCAP 03 (2018) 038 [1712.01316]; +Sharma, heating/scaling relations 1912.07626)
| # | Score | Basis |
|---|---|---|
| 1 | **N** | No new dynamical law on baryons at all — elastic DM-baryon collisions sculpt the DM profile toward an equilibrium that *reproduces* the MDAR; nothing is keyed, nothing is an inertia deficit. |
| 2 | **Y\*** | The emergent equilibrium relation is acceleration-keyed by construction (g_DM(g_b)); but only where relaxation completes (disks); a₀ emerges from interaction microphysics (cross-section ∝ 1/n), NOT from cosmology — the kernel a₀ = c²√(Λ/32π) has no home here. |
| 3 | **N** | Particle DM with a tuned velocity/density-dependent cross-section; no ultralight field. |
| 4 | **O** | Structurally the family's best: kinematics and lensing read the SAME total mass, so the observed kinematic→lensing continuity is automatic — the exact feature SFDM lacks. But the Mpc-scale lensing RAR amplitude requires the equilibrium sculpting to extend where there are no baryons to collide with; never confronted with Brouwer's 15 bins; lean: reverts to halo-shaped (NFW-ish) in the deep bins, same shape problem as SFDM's tail. |
| 5 | **Y** | No new long-range force, no modified Poisson equation — nothing for the Q₂ diagnostic to see. |
| 6 | **Y** | No MI; trivially inside the agentE budget. |
| 7 | **O** | The MDAR emergence is demonstrated qualitatively (1712.01316 derives the form; 1912.07626 the scaling relations); the 175-galaxy 0.01-dex tightness as an equilibrium *attractor* (with quantified scatter) has never been shown. |
| 8 | **O** (lean prediction) | Out-of-equilibrium systems deviate by construction (their own statement for clusters); early types (merger-built, quenched, dispersion-supported) plausibly sit off-relation — a type split is natural; sign/magnitude uncomputed. |

**Both-ways verdict on BIDM:** numerically the best live row (3 firm YES), but its YESes are the cells that pass
*because nothing new happens* (5, 6), its identity is hostile to the framework (it explains the RAR as
astrophysical equilibrium — a ΛCDM-side mechanism; the a₀↔Λ kernel cannot ride on it), and it is field-level only
in the weak sense (a particle-interaction mechanism, not an action hosting a covariant law). It is the closest
*numerically* and the farthest *conceptually*.

### 2.5 Pure fuzzy/ultralight DM (RAR claim: Lee–Kim–Lee 1901.00305; constraints: Hlozek+ 1410.2896, Rogers–Peiris 2007.12705 [standard-pins])
| # | Score | Basis |
|---|---|---|
| 1 | **N** | No modification — apparent boost is soliton+halo mass. |
| 2 | **N** | The claimed acceleration scale (~10⁻¹⁰ m/s² from the quantum pressure / soliton scaling, 1901.00305) is not a universal acceleration-keyed law — the effective a₀ runs with soliton/host mass; deep-MOND BTFR and EFE phenomenology not reproduced as laws. |
| 3 | **N\*** | The one family whose particle CAN sit near the window — but as *all* of DM the window is excluded: CMB/LSS require m ≳ 10⁻²⁴ eV (Hlozek+ 1410.2896) and Lyman-α pushes m > 2×10⁻²⁰ eV (Rogers–Peiris 2007.12705), ≥4 decades ABOVE the spec ceiling 1.6×10⁻²⁴. Build-note: a window-interior field is viable only as a *subdominant* component — which is exactly the spec's role for it (the knee field need not be the DM). |
| 4 | **N\*** | Lensing = mass (trivially "carried"), but as ΛCDM carries it — halo-by-halo accommodation, not a MOND-amplitude law; the observed MOND-shaped continuity to 10⁻¹³ is an unexplained coincidence in this model class. |
| 5,6 | **Y, Y** | Trivial (no new force; no MI). |
| 7 | **N** | RAR tightness is not a law in ULDM (diversity problem persists; soliton-host scatter); the 0.01-dex gate is not met as a prediction. |
| 8 | **O** | Type split = halo astrophysics; allowed, not predicted. |

### 2.6 Baryon-correlated DM EFT (Kamada 2605.20217, submitted 2026-05-11) — the newest entrant
Massive scalar+vector+tensor mediators with couplings tuned in the ratio 4:6:3 (degenerate masses) cancel the
fifth force on baryons while letting the dark field's interaction energy track Φ_b² (ρ_DM ∝ Φ_b²) — CDM on
cosmological scales, baryon-governed profiles on galactic scales. Three weeks old; no lensing, solar-system, RAR-
scatter, or stability confrontation exists. All eight cells O except item 1 (N — no inertia structure). Watch
item: the engineered fifth-force cancellation is the first new *mechanism* class since the superfluids — but its
acceleration scale is implicit, not keyed. 0/8 firm; too new to adopt or kill.

### 2.7 Dipolar dark matter (Blanchet–Le Tiec 0804.3518, 0901.3114; bimetric Blanchet–Heisenberg 1504.00870, 1505.05146)
Gravitational polarization: a dipolar DM medium anti-screens gravity, reproducing the Bekenstein–Milgrom (AQUAL)
equation exactly in the static weak-field limit — hence Y on item 2, Y\* on item 4 (the medium sources the
metric; built to match cosmology), Y\* on item 7 (inherits MOND's SPARC phenomenology by construction, same
function freedom as MOND itself), Y on 6, N\* on 1 (medium response, still force-side), N on 3, N on 8
(type-blind). Item 5: **N\*** — the static limit being exactly AQUAL means the repo-verified Desmond Q₂ wall
transplants (RAR-compatible μ ⇒ Q₂ ~ 3×10⁻²⁶ class) unless the medium is locally absent, which is not published.
**Decisive, and why this 4/8 row is not the closest candidate: the field-level realization is dead** — the
canonical bimetric completion "fails to recover the MONDian phenomenology at low energies" because "a consistent
gravitational polarization" cannot be achieved (2302.02690, 2023), and the original non-bimetric versions need an
ad-hoc environment-dependent internal force for stability (0901.3114's own admission). Calibration-grade lesson
#2: structure-rich, completion-less.

### 2.8 Emergent gravity / covariant EG (Verlinde SciPost 2, 016 [1611.02269]; Hossenfelder 1703.01415)
Apparent DM ∝ √(a₀) g_b from dark-energy elasticity — metric-level, so lensing is affected (Y\*; Brouwer+2017
tested it on KiDS favorably at the time). Dead at the solar system: predicted perihelion advances are "discrepant
with observational data by seven orders of magnitude" (Hees–Famaey–Bertone PRD 95, 064019 [1702.04358]); the
transition function also keys to g_N AND dg_N/dr (not pure acceleration — N on item 2). 1/8, dead. Included
because it is the only non-superfluid candidate whose *lensing* came out MOND-shaped by construction — the same
single virtue as AeST/DEW, killed by the same solar-system class of test.

---

## 3. Calibration rows — the matrix discriminates exactly where the repo's banked kills say it should

| | AeST (2007.00082) | DEW (1106.4984 → 2512.10513) |
|---|---|---|
| 1 | N — TeVeS-lineage modified gravity; right sign, force lever | N — nonlocal-metric modified gravity |
| 2 | Y — AQUAL-type static limit, RAR-compatible F | Y — static limit IS AQUAL, μ = 1−e⁻ʸ(1−y/2) [repo-derived, agentD §1] |
| 3 | Y\* — the μ mass term: 1/μ ~ Mpc ⇒ ~6×10⁻³⁰ eV, at/just below the window floor; supplies dust-like CMB behavior, NOT a frequency knee | N — no new mass scale (□⁻¹ structure) |
| 4 | **Y — the only clean item-4 pass in the literature**: lensing tracks the MOND total force by construction (CMB+lensing are the design wins) | Y — Φ = −Ψ enforced (their eqs. G00/Gij; agentD §1) |
| 5 | **N — Q₂ ≈ 3.2×10⁻²⁶ at the framework's own a₀ vs the ~5×10⁻²⁷ ceiling; μ-screening ~10 orders wrong scale; β₀ RAR-pinned** [repo-banked, 10-facet audit] | **N — Q₂ = +2.80×10⁻²⁶ (own a₀, 14.6σ) / +1.74×10⁻²⁶ (framework, 8.8σ); never below 3.2σ over g_ext; 2011 variant −5.8×10⁻²⁷ (4.1σ); rescue slivers g_ext-fragile + RAR-penalized 2.4–3.4×** [repo agentD] |
| 6 | Y — by class (MG; the binding solar gate is item 5, failed) | Y — by class (same) |
| 7 | Y — RAR/SPARC-compatible by construction (the repo's own "WORKS as EFT" row) | O(lean Y) — published f(Z): binned-RAR χ²/bin 6.8–10.4 vs floor 5.3–5.7 at best-Υ ("NOT RAR-dead", agentD §4.3); exact 0.01-dex gate never run |
| 8 | N — type-blind; the hardened 8.6–9.2σ split stands against it | N — type-blind |
| **Net** | **5/8 — DEAD.** | **4/8 — DEAD.** |

**The calibration lesson, stated plainly:** AeST is the highest-scoring row in the entire matrix and it is dead —
because the spec is gated, and its single N sits on the named killer gate. Any future "candidate X scores n/8"
claim made from this matrix must carry the gate-status, not just the count. Conversely the both-ways duty: AeST's
5/8 also shows the spec items are NOT gerrymandered to flatter the repo's hybrid — a hostile published theory can
score most of them.

---

## 4. The single closest candidate, and its open gates

**Closest candidate: the Berezhiani–Khoury superfluid family — specifically in Khoury's 1602.05961
("Another path") realization, with the vanilla BFK form (2.1) as its tested-and-wounded reference point.**

Why this and not the numerical leader (BIDM): the matrix's geometry. Across all live rows, items 1 and 3 are
universal NOs — no candidate has them — so the discriminating items are 4 (the wall), 2+6 (keying + solar), and
8 (the split). The 1602.05961 realization is the unique live construction that:
1. **carries lensing with the MOND force by design** (Φ = Ψ enforced via the normal component's u^μ — the spec's
   hardest item, and the one the vanilla family *failed in print on the repo's own data axis*, 2303.08560);
2. keys the galactic regime to **acceleration** through a phase boundary at a₀, with an **Einstein phase restored
   when time derivatives dominate** — the only published structure that natively contains both halves of N5's
   verdict (acceleration-keyed in-band, frequency-protected out-of-band);
3. inherits the family's **phase channel for the type split** (item 8 as a prediction rather than a liability) and
   the **decoherence solar screen** (item 5/6 mechanism);
4. has NOs only where *every* candidate has them (items 1, 3).

Its price, at full weight: it is the least-tested row in the matrix (4 OPEN cells; zero published rotation-curve
fits; a pre-GW170817 covariantization whose c_T audit is owed; the family's hyperbolicity result 2105.02241
hanging over its MOND regime). "Closest" here means *closest to the spec's shape* — not close in absolute terms:
2 firm + 2 starred YES out of 8.

**The open gates — which repo-banked kill-tests has it never faced (each is a bounded, pipeline-exists
confrontation):**

| Gate | Repo artifact (exists, locked conventions) | What it decides for the candidate |
|---|---|---|
| Cassini Q₂ of the phase-transition screen | `agentD_dew_quadrupole.py` (AQUAL/Picard–Legendre solver) + `CASSINI_QUADRUPOLE_CONSTRAINT.md`; bound 2602.17884 | g_ext ≈ 1.8–2.3 a₀ puts the kAU boundary in the BROKEN phase — does the symmetry restoration give Hees-2016-sharp screening (pass) or AQUAL-gradual (the AeST/DEW death)? The single most decisive uncomputed number in this row. |
| Solar reflex at the synodic carrier | `agentE_solar_reflex.py` (LM ephemeris-fit emulation; linear transfer standard) | Quantify δa☉ for the time-dependent phase criterion vs the 2.47×10⁻¹⁵ budget — the model's own §7 argument (time derivatives ⇒ Einstein phase) predicts a pass; make it a number. |
| 175-SPARC 0.01-dex gate, both footings | `mi_f4_sparc_shape_test.py` / `agentN5_freq_vs_accel.py` conventions | With a UNIVERSAL boundary-condition prescription (no per-galaxy freedom): does the phase law hold the RAR within +0.010 dex of 0.1950? Repeat 2201.07282's M/L-inversion check on this variant. |
| The Brouwer 15-bin lensing amplitude + per-class split | `lr_battery.py`, `esd_conversion.py`, `agentH_perclass_C.py` (released ESD + covariance in-repo) | Φ=Ψ holds only in the broken phase ⇒ the model PREDICTS a lensing-RAR break at the phase radius — confront with the 15 bins to ~Mpc; and score the family's phase prediction for the early/late split (item 8) against the banked 8.6–9.2σ / 5.6–6.3σ per-class numbers, sign first. |
| Wide-binary fork | `mi_f4_widebinary_efe.py`; DR4 watchlist | 7 kAU pairs sit in coherent superfluid (outside each star's ~10² AU bubble) in the broken phase: the phonon/phase EFE prediction for the Gaia DR4 amplitude — the family's analog of the knee discriminator; never computed. |
| Kernel compatibility a₀(z) | `A0Z` machinery; BIG-SPARC staged pipeline | The family's a₀_eff is set by (Λ, α, condensate state); condensate density/temperature evolve with z — does the induced a₀(z) track √ρ_DE (the framework's branch), ρ_m, or neither? Unexplored anywhere in the SFDM literature; this is where the repo's kernel either rides or falls off. |
| Imported external gates (bank these) | — | GW170817 c_T audit of the §6 covariantization (the TeVeS killer; Boran+ 1710.06168); hyperbolicity in the MOND phase (2105.02241); star-Cherenkov bound on any matter-coupled non-relativistic mode (2103.16954/2208.14308 — note: this gate will also apply to the repo's OWN hybrid if its knee field couples to baryons with sub-orbital sound speed; the MI/worldline-dressing realization responds to acceleration rather than propagating a slow mode and is likely exempt — must be checked at build time, flagged now); MW vertical-dispersion Jeans test (1812.08169/1911.12365, with the disequilibrium caveat the review itself raises). |

---

## 5. VERDICT (both ways, full weight)

**The field is EMPTY at the spec's standard: no published field-level candidate scores better than 5/8, and the
only 5/8 (AeST) is dead on the spec's named killer gate. The hybrid must be BUILT, not adopted.** Precisely:

- **Universal NOs — the two ingredients that exist nowhere:** (item 1) an inertia-side lever — every published
  candidate is force/mass-side; the trajectory-nonlocal MI matter sector the trilemma demands has no published
  field-level realization (consistent with `TOE_TRILEMMA.md`'s "does not exist yet" cell — this matrix checked
  the DM-hybrid literature too, and it isn't hiding there); (item 3) the ultralight knee field in
  [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV — no MOND-hybrid contains a field in the window (AeST's μ sits at/below the floor
  with a different job; superfluid constituents are eV-scale; viable all-DM ULDM is ≥4 decades above the
  ceiling). The swarm's two *derived* structural items are exactly the two things the literature has never built.
  That coincidence is the strongest argument that the spec is genuinely new territory and not a relabeling of an
  existing program.
- **What the literature DOES supply — adoption-grade templates the build should take rather than re-derive:**
  (i) the **phase/decoherence solar screen** (SFDM: superfluid criticality around individual stars — an existence
  proof that acceleration-keyed galactic dynamics + solar safety is achievable *without* frequency dressing);
  (ii) the **Φ = Ψ lensing partner via the medium's 4-velocity** with no extra vector field (1602.05961 §6 — a
  concrete template for the spec's "lensing-carrying metric partner");
  (iii) the **finite-T two-fluid formalism** (1809.08286) — ready-made machinery for a phase-keyed type split
  (item 8 as a prediction);
  (iv) a **worked catalog of how hybrids die**: lensing-continuity (2303.08560), Cherenkov (2103.16954),
  hyperbolicity (2105.02241), vertical Jeans (1812.08169) — four imported kill-tests the repo's falsification
  registry does not yet carry, each of which the built hybrid must face on day one alongside the banked eight.
- **The honest other way:** the superfluid family is not dead, and its phase architecture overlaps the spec more
  than any pre-2015 MOND host ever did — acceleration-keyed, solar-screened, cluster-split, type-split-capable.
  If the family's open gates (§4) were run and passed — especially a computed Q₂ inside the 2026 window and a
  lensing-RAR break that the next-generation stacking *finds* at the phase radius — the "build" verdict would
  weaken toward "extend." Nothing in this memo forecloses that; the gates are named and bounded. But on the
  published record as of 2026-06-10, every row either fails a decisive spec gate, leaves the decisive gates
  uncomputed, or isn't structurally a host for the kernel — and **no row touches items 1 or 3 at all.**
- **For the trilemma doc:** this matrix is the missing complement to `TOE_TRILEMMA.md`'s covariant-host table —
  that table closed the modified-gravity perimeter; this one closes the **DM-hybrid perimeter** at the same
  standard (every cell either failed, open-and-named, or structurally non-host). The missing object's spec
  survives contact with the entire published field-level literature with its two derived ingredients unclaimed.

## Numbers ledger (for citation)

| Quantity | Value | Source |
|---|---|---|
| SFDM lensing-RAR closest-match χ²_red (logM_b = 8.5/10.0/11.5) | 15.0 / 14.9 / 28.7 (2 tuned params/galaxy) vs MOND 6.5 (0 params) | 2303.08560 §4.1 |
| SFDM fiducial parameters | m²/α = 0.18 eV², β = 2, a₀ = 0.87×10⁻¹⁰ m/s² | 2303.08560 §2 (quoting BFK) |
| SFDM solar decoherence radius | O(10²) AU (critical velocity exceeded) | 2505.23900 §7.2; 1711.05748 |
| SFDM published Q₂ | none exists | search this session |
| SPARC fit pathology | 169 galaxies; giants' M/L < dwarfs' (inverted); MOND-regime needs per-galaxy BC | 2201.07282 |
| Cherenkov verdict | "rules out ... including the most commonly used parameters"; lifetimes ≲10 Gyr for realization (7.9); two-fluid evades | 2103.16954; 2208.14308; 2505.23900 §7.2 |
| Superfluid-completion causality | global hyperbolicity violated in the MOND regime | 2105.02241 |
| Halo fragmentation update | droplets of size ~λ_J; central soliton up to few tens of kpc | 2212.10577 |
| EG solar-system | perihelion discrepancy ×10⁷ | 1702.04358 |
| Bimetric DDM completion | "cannot achieve a consistent gravitational polarization" | 2302.02690 |
| ULDM mass bounds (all-DM) | m ≳ 10⁻²⁴ eV (CMB); m > 2×10⁻²⁰ eV (Lyman-α) [standard-pins] | 1410.2896; 2007.12705 |
| Spec windows used | knee mc² ∈ [1.3×10⁻²⁹, 1.6×10⁻²⁴] eV; corridor p ∈ [0.069, ≥1]; δa☉ ≤ 2.47–3.38×10⁻¹⁵ m/s²; Q₂ 2σ ∈ [−2.0, +5.2]×10⁻²⁷ s⁻²; SPARC +0.010 dex of 0.1950; split 8.6–9.2σ (u−r) | repo-banked (§0 table) |

**Sources (fetched/verified this session):** arXiv:1506.07877 (PLB 753, 639); 1507.01019 (PRD 92, 103510);
1602.05961 (PRD 93, 103533) [prompt's "1602.08831" corrected — that id is Azadi–Grason, curved-crystal defects];
1711.05748 (JCAP 09 (2018) 021); 1809.08286 (JCAP 05 (2019) 054); 1909.05710; 2009.03003 (JCAP 01 (2021) 025);
2103.16954 (JCAP 11 (2022) 008); 2208.14308; 2201.07282; 2303.08560 (JCAP 09 (2023) 004); 2212.10577 (PRD 107,
123010); 2505.23900 (Phys. Rep., 136 pp, v2 2026-02-16); 2105.02241 (JCAP 11 (2021) 015); 1812.08169 (PRD 100,
083009); 1911.12365 (Phys. Dark Univ. 39, 101140); 1712.01316 (JCAP 03 (2018) 038); 1912.07626; 1901.00305;
2605.20217; 0804.3518; 0901.3114; 1504.00870; 1505.05146; 2302.02690; 1611.02269 (SciPost Phys. 2, 016);
1703.01415; 1702.04358 (PRD 95, 064019); 1710.06168 (PRD 97, 041501); 2007.00082 (PRL 127, 161302); 1106.4984
(PRD 84, 124054); 2512.10513 (JCAP 04 (2026) 081); 2602.17884; 2401.04796 (MNRAS 530, 1781); 1410.2896;
2007.12705. Repo: the §0 table's banked artifacts.
