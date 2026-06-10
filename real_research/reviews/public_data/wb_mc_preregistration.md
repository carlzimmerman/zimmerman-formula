# WB-R2 adjudication + WB-3 deprojection Monte-Carlo — PRE-REGISTRATION

*C. Zimmerman, 2026-06-10. Written and committed BEFORE the MC is run — the pre-commitment is the point. Triggered by
WB-R1 Outcome A (`WB_R1_EXACT_REPLICATION.md`). Inline execution, no swarms. C1/C2 only (says nothing about a₀(z); C3 fence).*

## Part 1 — WB-R2 adjudication: we landed Outcome A
The faithful Chae/Banik replication gave, for **both** teams' cuts and across the RUWE 1.2–1.4 bracket: D1≈0.12–0.15 (<0.3),
D2 super-escape≈0.10 (<0.15), D4≈1.3–1.4× (<1.5). Mapping to the three pre-registered outcomes:
- **A — clean below both thresholds (← WE ARE HERE).** The clean sample is *not* contamination/noise-dominated; the deep bins
  are usable. → proceed to the deprojection MC to test for a boost. *(Halt-before-MC was honored; table relayed.)*
- B — a threshold fires on the *clean* (Banik) sample → the deep-MOND signal is junk on the cleanest cut → framework-disfavoring,
  no MC needed. **Did not occur.**
- C — clean sample shows a boost *surviving* a matched Newtonian MC → framework-favoring → hostile-verification tier. **This is
  what the MC now tests.**

## Part 2 — the physics the MC must exploit (the scale-free insight)
For a **pure Kepler** orbit the observable ṽ ≡ v_sky / √(GM/r_sky) is **dimensionless and scale-free**: it depends ONLY on
(eccentricity e, orbital phase, viewing orientation) — NOT on M or separation. Therefore a Newtonian population predicts a
**FLAT** median ṽ across every g_N/a₀ bin. (Sanity: a circular face-random orbit gives ṽ ≈ p_v·√(p_r) ≈ 0.7·√0.8 ≈ 0.63,
matching the observed high-acceleration ≈0.57–0.59.) **Any RISE into deep-MOND must come from one of exactly four sources:**
  1. **Measurement noise** — σ_ṽ = σ_v/v_N, and v_N = √(GM/r_sky) is small in wide (deep) bins → noise inflates ṽ there. (= D1.)
  2. **Contamination** — hidden triples / interlopers add a high-ṽ tail; its fraction may rise with separation. (= D2/F4.)
  3. **Separation-dependent eccentricity** — Hwang+2022 super-thermal α(s): e rises with s → broader ṽ in wide bins. (= F2.)
  4. **A genuine boost** — modified gravity/inertia raises the true v at low g_N. **This is the only one we are testing for.**
The MC's job: build 1–3 from first principles + the *measured* per-pair noise, calibrate them on the high-acceleration bins
(where boost #4 is absent by construction: g_N≫a₀ ⇒ Newton=MOND), then ask whether the deep-bin rise is fully explained by 1–3
or leaves a residual matching the framework boost.

## Part 3 — forward model (pre-registered)
Substrate: the **Banik-exact** selection (cleanest; N≈9.5–10.8k), framework a₀=9.36×10⁻¹¹, per-pair M from the Banik cubic.
For each real pair *i* (its M_i, its measured σ on pm & parallax, its observed r_sky,i, its bin g_N/a₀ = GM_i/r_sky,i²/a₀),
draw K=40 Newtonian mocks:
- **e** ~ f(e). **GRID (pre-registered): {thermal f=2e ; uniform f=1 ; Hwang super-thermal α(s) with e_max(s)}.**
- **phase**: mean anomaly ~U(0,2π) → Kepler solve → E → true anomaly, r/a, and orbital-plane (v_x,v_y) from vis-viva.
- **orientation**: cos i ~U(−1,1); Ω, ω ~U(0,2π). Rotate; project onto sky → (r_sky/a) and v_sky/√(GM/a).
- **conditional scaling**: set a_i so the mock's projected r_sky = the observed r_sky,i (the standard Pittordis–Sutherland/Banik
  "scale-to-observed-separation" conditioning) ⇒ ṽ_mock,i = v_sky / √(GM_i/r_sky,i), a pure function of (e,phase,orientation).
- **noise**: ṽ_mock,i += 𝒩(0, σ_ṽ,i) with σ_ṽ,i the pair's measured proper-motion+parallax error propagated to ṽ (NOT a free knob).
- **contamination**: with prob f_triple(s), replace the mock by a triple draw (companion mass q~U(0.1,1)M_i, inner orbit adds a
  reflex velocity to v_sky and biases v_N low). **GRID: f_triple ∈ {0, 0.02, 0.05, 0.10}, flat and ∝log(s).**
- **framework overlay**: the MOND/framework prediction is the SAME machinery with the velocity at each phase scaled by the local
  √(g_obs/g_N), g_obs = g_N·ν(g_N/a₀), simple ν(y)=½+√(¼+1/y). *(Stated limitation: this boosts v at fixed orbit rather than
  integrating the non-closed modified-gravity orbit; it captures the observable median shift to ~few-% and is the standard
  first-pass. Full modified-orbit integration is the next refinement and is flagged, not hidden.)*

## Part 4 — calibration anchor (the anti-self-deception discipline)
The Newtonian MC **must reproduce the high-acceleration bins (g_N/a₀ > 10) within errors** — there, boost #4 is zero, so any
mismatch means the e-distribution / noise / contamination model is wrong and must be fixed BEFORE reading the deep bins. The
high-acc bins fix f(e) and f_triple; the deep bins are then a *prediction*, not a fit.

## Part 5 — decision rule (pre-registered, 3 outcomes)
Per (f(e), f_triple) on the grid, compute Newton-MC median ṽ(deep) and framework-MC median ṽ(deep), each ±MC error, and the data
median ṽ(deep) ±bootstrap. Then:
- **NEWTON-SUFFICES** — data median ⊂ Newton-MC band for ≥1 plausible (f(e),f_triple) that also passes the high-acc anchor →
  the rise is projection+noise+eccentricity; no boost needed. *Framework's distinctive WB boost is absent at this sensitivity.*
- **BOOST-DETECTED** — data median ⊂ framework-MC band AND excludes Newton-MC across the whole anchor-passing grid → boost at
  a₀=9.36e-11. **Triggers the hostile-verification tier** (vary a₀ ±30%; vary ν; re-run on Chae-exact; jackknife by sky region).
- **AMBIGUOUS** — the (f(e),f_triple) freedom spans both → unresolvable with the sky-projected DR3 observable → wait for Gaia DR4
  line-of-sight RVs (full 3D). Report the degeneracy direction.
Report the result as a **map over the (f(e), f_triple) grid**, never a single number. Whichever way it falls is reported with
equal rigor (the project's #1 rule): no manufactured boost, no reflexive Newton.

## Part 6 — what this cannot do (fences)
Sky-projected DR3 only; no line-of-sight velocities ⇒ partial deprojection. Modified-orbit integration approximated (Part 3).
Says NOTHING about a₀(z) (C3). A BOOST-DETECTED result is provisional pending hostile verification + an independent re-derivation;
a NEWTON-SUFFICES result is the honest null at this sensitivity and points to Gaia DR4 as the decider.
