# Fresh Observational Doors — preferred-frame sweep of arenas the framework was NOT pointed at
**Date:** 2026-06-27 · **Footing:** a0 = 9.36e-11 m/s² (canonical pure-Λ, cH_Λ/Z, INPUT) · c_T = 1 · CPT-even · apex = CMB rest frame
**Status:** LOCAL — not git-pushed. Quarantine held (nothing derived; a0 is input throughout).

## The question
Check OBSERVATIONAL arenas the framework was NOT pointed at for a genuine distinctive, **above-floor, near-term** prediction.
Key logic: the framework is modified-INERTIA at low a (<a0) → in **high-a arenas (GW/BH/pulsar) the MOND part is negligible (= GR, likely NULL)**;
but it is ALSO a **preferred-frame** theory (de Sitter vacuum = CMB frame = CPT-even SME background), and preferred-frame effects
DO appear at high a (the banked solar-system s^TX dipole). So the FRESH candidates are **preferred-frame signatures in new arenas**, not MOND signatures.
A door counts only if **distinctive + above the instrument floor + near-term**. Otherwise: NULL / below-floor / MOND-shared / already-covered.

Every magnitude below is from a runnable script in `reviews/` (exit 0). Bounds are real (WebSearch / primary sources).

---

## BOTTOM LINE (both-ways, computed, NOT a TOE)
**The sweep did NOT open a genuine new observational door.** It CONFIRMED that the framework's testable content is the already-known set:
**s^TX (solar dipole) · a0(z) (Front B) · dwarf-σ · neutrino/varying-mass · the a≤a0 CMB-apex lensing dipole.**
This is the honest expected result — *because the framework = GR in the high-a arenas, and its preferred-frame channels are all banked.*
That is a real, falsifiable content statement, **not** a "no doors": the sweep produced two sharp **falsifiers** (below) and one genuinely
in-regime arena that turns out non-discriminating. NEVER "no doors" — but no NEW *reachable distinctive* door beyond the known five.

---

## RANKED: genuine fresh above-floor near-term doors
**NONE.** No arena in this sweep yielded a signature that is simultaneously (distinctive) + (above floor) + (near-term) and *not already banked*.
The single closest thing to "fresh" is the secular-aberration arena (§A below): genuinely at a~a0 (so not a high-a null), genuinely skipped by
the four banked scripts — but it resolves **MOND-shared + baryon-degenerate**, adding no discriminating power beyond the RAR. So it is honestly
classified below, not promoted.

---

## A. The one arena the four banked scripts genuinely SKIPPED — and its honest disposition
**Secular aberration drift** = Gaia/VLBI direct kinematic measurement of the Solar System's galactocentric acceleration.
`reviews/aberration_door.py` (exit 0). Source: Klioner et al. 2021, A&A 649 A9 (arXiv:2012.02036).
- Measured |a_sun| = (2.32 ± 0.16)×10⁻¹⁰ m/s² → **a_sun/a0 = 2.48** — INSIDE the MOND transition, **not** deep-Newtonian. (So, unlike GW/BH/lab, the MOND sector is NOT negligible here — a real catch.)
- Direction = Galactic center (centripetal), NOT the CMB apex → genuinely distinct observable from the s^TX dipole.
- **But:** aberration measures the TRUE kinematic acceleration directly; every theory that fits the rotation curve predicts the SAME a_sun (= v_c²/R0 = 2.15e-10, 7% match). Read as missing-mass, the framework predicts a ~22% inertial boost over counted baryons — **(a) MOND-SHARED** (same ν family) **and (b) degenerate with the >20–30% baryonic-a_bar systematic at R0** (the same SPARC-RAR wall, banked as non-diagnostic of 9.36e-11). The framework-vs-MOND ν gap (~11%) sits above the DR5 statistical floor (~1.4%) but is swamped by the baryon systematic → not separable.
- The framework-UNIQUE CMB-apex dipole is NOT accessible from a single acceleration vector (it lives in an ensemble of a<a0 systems = the banked weak-lensing RAR dipole).
- **DOOR STATUS: MOND-shared + baryon-degenerate. NOT a fresh distinctive door** (consistent with the framework, just not a test of it).

## B. NULL — framework = GR at high a (the falsifier-but-not-a-door rows)
- **Black holes / EHT shadow / ringdown QNM** — `reviews/bh_door.py`. a/a0 = 10¹³–10²² at the photon ring → MOND dead by 13–22 orders; inverted-BH duality self-cancels to pure GR. Preferred-frame ringdown dipole is β- and scale-suppressed 9–80+ orders below the LISA/ngEHT floor. **NULL-framework-is-GR** (can falsify metric-shifting rivals MOG/STVG; never confirms the framework).
- **GW birefringence** — `reviews/gw_sme_door.py`. EXACTLY ZERO by the CPT-even theorem (dS-Unruh kernel even in u → k_(V)=0). vs GWTC-3 k_(V)00 < 3.19e-15 m. **A clean falsifier:** a confirmed GW birefringence kills the u^μ-referred framework. Not a reachable door.
- **GW d=4 dispersion** — ZERO (d=4 is nondispersive; verified vs arXiv:2302.05077 dropping d=4 as "no observable dephasing"). c_T = 1 exactly vs GW170817 |c_T/c−1| < ~1e-15. **NULL by construction** (this is why AeST survived GW170817).
- **PTA tensor-sector LV** (graviton mass m_g < 8.2e-24 eV arXiv:2310.07469; c_T; non-tensorial pols) — framework leaves the graviton lightcone untouched → returns the GR value. **NULL by construction.**

## C. BELOW-FLOOR (real signature, unreachable this decade)
- **GW anisotropic speed dipole** — `gw_sme_door.py`. A·β = 5.89e-15 vs weak anisotropic-d=4 floor ~1e-14 today (→ ~5e-16 optimistic mid-2030s). ~2× below floor now; weaker + less near-term than the in-hand solar s^TX. (The naive constant-cH0-background reading gives 8.8e-5 = ~1e9× over → that would be falsified, which *proves* the constant-background reading mis-maps the acceleration-dependent coupling — same class as the matter-c_μν "15-order kill" mis-map. Flagged, not a real signal.)
- **PTA CMB-correlated timing dipole** — `pta_door.py`. Earth-annual modulation s·β_earth·(AU/c) ≈ 0.043 ns vs SKA floor ~10 ns → ~230× below SKA-era floor, and it is the SAME s^TX physics measured far better by planetary ranging.
- **a0-scale pulsar far-field** — g = a0 at 0.046 pc (~9400 AU), far outside any timed orbit → MI out-of-regime. **NULL.**
- **Lab MOND/MI** — `lab_door.py`. Earth surface g = 1.05e11 × a0 (~11 orders above the scale); intrinsic MI boost a0/2g ≈ 4.8e-12 below any gravimeter/EP floor; reaching a<a0 needs drag-free residual <1e-10 (~2 orders below LISA-class). BELOW-FLOOR.
- **Lab s^TX dipole** — exists (s_TX = 5.7e-15) but the lab sits at the HIGHEST a = g → SMALLEST A = a0/2g; tightest lab bound (SC gravimeters, Flowers/Goodge/Tasson PRL 119 201101) ~1.7e4–5.3e7× too coarse. The s_TX test is SPACE (Saturn), not a lab.
- **BH preferred-frame ringdown dipole** — 9–80+ orders below LISA (see §B).

## D. ALREADY-COVERED (= the banked set; not new)
- **GW siren H(z)** — d=4 traceless s_μν shifts speed not amplitude → GW-friction d_L^GW/d_L^EM = 0; H(z) signature is EoS-degenerate with w(z) = the banked **a0(z) Front B**.
- **GW speed-anisotropy dipole** — literally the SAME induced s_μν as the banked solar **s^TX** (and weaker in the GW realization).
- **PTA GWB amplitude via MOND friction** — already worked (`project_nanograv_mond_gwb.py`): soft ~√3 hint, Newtonian final-parsec bottleneck, model-degenerate.
- **PTA / lab s-coefficient** — adds no sensitivity beyond banked **s^TX** (~1.5× live, Gaia DR4 ~2028-32) and **alpha2** (~1e-13, ~1e6× safe, NOT live).
- **WEP / MICROSCOPE** — predicted η = 0 exactly (universal COM-acceleration coupling, differential cancellation) vs 2e-14. NULL by construction.

## E. The two specific questions in the prompt
- **GW preferred-frame: genuine above-floor signature, or c_T-protected / below-floor?** → **c_T-protected + below-floor.** Birefringence = exactly 0 (CPT-even theorem, a falsifier); dispersion = 0 (d=4 nondispersive); the only nonzero piece (speed-anisotropy dipole, 5.9e-15) is the s^TX coefficient, ~2× below today's weak GW floor and weaker than the in-hand solar test. No fresh GW door.
- **Pioneer ~a0 coincidence: real or thermal (settled)?** → **THERMAL, settled.** `pta_door.py`. Pioneer is deeply Newtonian (g_Sun ~10³–10⁵ × a0 at 20–70 AU) → modified-INERTIA predicts ~ZERO MOND anomaly there; the preferred-frame piece is ~10⁸× too small AND points at the CMB apex, not sunward. a_P = 8.74e-10 ≈ a0 ≈ cH0 is the classic a0-coincidence trap. The decaying jerk term tracks the Pu-238 87.7-yr half-life (no constant accel can decay) = Turyshev 2012 PRL 108.241101 thermal recoil; a universal a0-scale sunward accel is independently excluded ~4 orders by Cassini/INPOP at Saturn. The framework correctly does NOT and should NOT claim Pioneer.

---

## Single best fresh door (if any)
**None genuinely fresh.** If forced to name the closest-to-fresh and the most valuable falsifier:
- **Closest-to-fresh (but non-discriminating):** the **secular-aberration a_sun** (§A) — it is the only sweep arena genuinely at a~a0 rather than a high-a null, and the four banked scripts skipped it; but it is MOND-shared + baryon-degenerate, so it does not promote.
- **Most valuable NEW falsifier the sweep sharpened:** **ZERO GW birefringence** (CPT-even theorem). A confirmed GW birefringence in any future LVK/LISA run would kill the u^μ-referred framework. It is a clean structural falsifier, not a confirmable door.

## What this means for the live-fronts ledger
Unchanged. The binding preferred-frame test remains **s^TX in the ephemerides** (~1.5× under the combined INPOP/Cassini bound, 0.67σ inside the bar; analysis-limited, Gaia DR4 SSO astrometry ~2028-32). The sweep added falsifiers and a non-discriminating a~a0 arena, but no new reachable distinctive door.

## Scripts (all exit 0)
- `reviews/gw_sme_door.py` — GW propagation (dispersion / birefringence / speed-anisotropy / siren H(z))
- `reviews/bh_door.py` — BH shadow / ISCO / QNM ringdown + preferred-frame dipole
- `reviews/pta_door.py` — PTA tensor-sector + timing dipole + pulsar far-field + Pioneer
- `reviews/lab_door.py` — ground/space EP / clock / gravimeter / atom-interferometry
- `reviews/aberration_door.py` — **NEW**: secular aberration drift (a_sun at ~2.5 a0)
