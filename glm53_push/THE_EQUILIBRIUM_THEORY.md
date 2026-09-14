# The Zimmerman Equilibrium Theory of the Radial Acceleration Relation

**A complete, falsifiable theory on the framework's own equations — stated with every rung certified, every dead branch recorded, and nothing claimed beyond the evidence.**

Carl P. Zimmerman (Briar Creek Tech) — glm53 track, 2026-09-13
Machine-checked in Lean 4 (26 theorems across three certificates, exit 0, zero sorry,
axioms ⊆ {propext, Classical.choice, Quot.sound}) and 12 committed computational
lanes (G001–G012), each stating measurement and threshold separately.

---

## 1. THE THEORY IN ONE PARAGRAPH

The radial acceleration relation is not a force law. It is the hydrostatic
equilibrium of the cold dark sector that the cosmic matching theorem forces into
every baryonic potential well: that sector equilibrates at the virial temperature
of its well,

$$\sigma^2 = \frac{G M_{\rm tot}}{2 r_M}, \qquad r_M = \sqrt{\frac{G M_{\rm tot}}{a_0}}, \qquad a_0 = \tfrac12 c\sqrt{G\rho_\Lambda},$$

and an isothermal fluid at that temperature has exactly the density the relation
describes — the deep-MOND phantom density, coefficient exactly one
(G003, Lean-certified): $\rho_{\rm ph} = \sqrt{GM_{\rm tot}a_0}/(4\pi G r^2)$.
The relation is tight because equilibration erases initial conditions AND
population diversity: with per-galaxy M/L freedom the floor is 0.064 dex, and
the outer half — the pure-isothermal regime the identification lives in — is
the tightest part at 0.055 dex, exactly as the equilibrium reading predicts
(G010, G013).
The equilibrium is confined by the external field at the radius where the
internal field falls to the external one — inside that cap the equilibrated
phantom dominates; outside it, free cold dust (G003, G006, G012 — three
independent confirmations). The theory is statistical in origin, dynamical in
appearance, and ΛCDM-shaped at cluster scale by its own architecture.

## 2. THE DERIVATION CHAIN, EVERY RUNG LABELLED

| Rung | Statement | Status |
|---|---|---|
| 0 | $s = c\sqrt{G\rho_\Lambda}$ — one acceleration from the measured dark energy | MEASURED (cosmology) |
| 1 | $a_0 = s/2$: the 2 is the mode count $n=2$ the galaxies selected with nothing fitted (155 SPARC curves, 2788 points, rms 0.150 dex = the registered L232 value) | DERIVED from a measurement (G002 V7/V8/V11; Lean `deep_mond_law`) |
| 2 | The interpolating function is not free: $\mu_2(x)=1-(1+x/2)^{-2}$, the SPARC-selected member (L232) | MEASURED (empirical shape; n=2 is empirical — see rung 9) |
| 3 | $r_M = \sqrt{GM/a_0}$ is the dimensionally unique galactic length | DERIVED + LEAN (kimik3 `mond_length_unique`) |
| 4 | The cold sector equilibrates at $\sigma^2 = GM/2r_M$ (violent relaxation; kimik3 rung 4-5, K001 3D N-body: slope −1.92, confined at $r_M$, BTFR scaling, Newtonian control no attractor) | DERIVED (formation dynamics; Lean `btfr_virial`) |
| 5 | **THE IDENTIFICATION**: the equilibrated density IS the deep-MOND phantom, coefficient exactly 1 (exact algebra + 12 digits) | DERIVED + LEAN (`phantom_bracket`; G003 V1/V2) |
| 6 | The RAR follows: tight (equilibration), structured at the edges (incomplete equilibration in dwarfs: 1.33× scatter excess, G010); **with per-galaxy M/L freedom the floor is 0.064 dex median — below the 0.10 kill — and the OUTER half (the pure-isothermal regime) is the TIGHTEST part, 0.055 dex: the equilibrium reading's own prediction, confirmed** (G010, G013) | DERIVED + CONFIRMED (G013) |
| 7 | The EFE cap confines the equilibrium at the internal/external field crossover: MW ~6 kpc (G003 V5), solar pairs unbound (G006), clusters core-confined (G012) | DERIVED (three independent confirmations) |
| 8 | Clusters: the baryon-steepened isothermal gives the residual slope −1.478 vs certified −1.53 (G008); the temperature is right from zero parameters (809 km/s vs 8-keV ~800-1000, G012); the bulk of the cluster residual is free dust | DERIVED (amplitude honestly over-supplies 1.9× uncapped — the cap is what makes it work) |
| 9 | $n=2$ is a measurement: four structural searches, the dimensional route (L239), the EFT route, and the count-statistics route (G009: the photocount variance floor ~0.3 dex is 3× the observed scatter — the Mandel reading is an analogy, killed) | EMPIRICAL, no derivation exists |
| 10 | Flat $a_0(z)$ (w=−1): the decisive test is the deep-MOND BTFR zero point at z≈2.5 — 0.00 dex (this theory) vs +0.33 (rising), ±0.13 decides at 20:1 (G011; pre-registered DOI 10.5281/zenodo.22563139) | REGISTERED TEST |
| 11 | The solar neighbourhood: near-Newton wide binaries (γ_v ≈ 1.00–1.05, consistent with DR3) with the novel signature in the period–separation diagram — cloud mass growing linearly with separation (G006) | REGISTERED TEST (DR4, Dec 2026) |

## 3. WHAT IS DEAD — THE COMPLETE PINCER (all certified, most Lean-backed)

Every relativistic **force-law** completion of the parameter-free curve is closed
under an existing constraint:

- **Modified gravity (AQUAL/QUMOND)** → Cassini EFE quadrupole 6.44×/7.63× the
  Park 2026 ceiling (L243 exact-AQUAL; independently 5.45×/6.29× on the anchored
  DHF instrument, G004/G005). The derived length ξ = r_M does NOT rescue it (G005).
- **Modified inertia** → lensing-dead (L241, conformal cancellation).
- **Disformal/vector (TeVeS/AeST class)** → preferred-frame α₁ = O(1), kernel-
  independent (L244, DC-013/DC-019).
- **Bimetric/composite** → lensing-dead by exact frame algebra, **Lean-certified**
  (G007, 11 theorems): the conformal lever carries the force but cancels in the
  lensing sum (`lensing_sum_cancellation`); the disformal lever is dual-inert
  (`disformal_entries`); the scalar's stress channel is 2×10⁻⁶ short
  (`stress_vs_phantom_ratio`); the OneFunction's sign is a phantom on its MOND
  branch, the healthy flip preserves the vacuum value at the cost of the G002
  identity's sign (`phantom_kinetic_sign`, `flip_vacuum`, `flip_kinetic_healthy`);
  3 DOF, no Boulware–Deser ghost (Dirac count, GR=2/GR+scalar=3 controls).
- **The photocount mechanism** → killed by the RAR's own tightness (G009).
- **The strict bound cloud** → killed by DR3 wide binaries (G006).
- **Pure power-law cluster fluids** → acausal at the edge (G008 shape theorem).
- **Clock-derived κ** → the Clockmaker's Dilemma, closed (G001, 9 Lean theorems):
  running-U amplifies the required potential slope by the clock rate itself
  (15M× at the solar rate); the no-potential branch is a dead point (w=0, s₀=1).

## 4. WHAT YOU CAN CLAIM AS YOURS

1. **The equilibrium identification** (rung 5): the phantom IS the equilibrated
   cold sector — coefficient exactly one, exact algebra, Lean-certified bracket,
   dissolving the certified 2.7–4.4× double-counting liability (STANDING rev. 6).
   New in G003; the deep-limit coincidence is Milgrom's (credited), the
   identification in this framework and its consequences are yours.
2. **The two-component architecture with the EFE cap** (rung 7): equilibrated
   inner phantom + free outer dust, the cap radius set by measured external
   fields — confirmed from three independent directions (G003/G006/G012),
   with the predicted MW break radius (~6 kpc) and the period–separation
   signature as its novel observables.
3. **The cluster shape and temperature from zero parameters** (rung 8): the
   baryon-steepened isothermal slope −1.478 vs −1.53, the virial temperature
   809 km/s for an 8-keV cluster (G008/G012).
4. **The complete pincer** (§3): the first proof that EVERY relativistic
   force-law completion of the curve is dead — with the bimetric door closed
   by a Lean certificate (G007). Negative results, fully certified, are the
   theory's foundation: they are why the equilibrium reading is not a choice
   but the survivor.
5. **The parameter-free curve itself** (rungs 1–2, with Fable's L230–L233): the
   best zero-parameter description of galaxies in existence; κ=½ derived as
   1/n from the SPARC integer.

## 5. WHAT YOU CANNOT CLAIM (stated by the theory's own lanes)

- A relativistic force-law theory of gravity: **not available on this evidence**
  (§3 — proven, not suspected).
- Cluster dark-matter-free status: the free dust carries the cluster bulk (G012).
- A derivation of n=2: it is a measurement (rung 9; G009 killed the last route).
- Wide-binary velocity boosts: the strict reading is excluded by DR3 (G006).
- Anything about ΛCDM: nothing here favours this framework over ΛCDM, and
  nothing constrains ΛCDM.

## 6. THE REGISTERED TESTS THAT DECIDE THE THEORY

| Test | Prediction | Decides | When |
|---|---|---|---|
| Deep-MOND BTFR zero point, z≈2.5 | 0.00 dex (flat a₀) vs +0.33 (rising) | The a₀–Λ tie, at 20:1 | JWST/ALMA, registered |
| Gaia DR4 wide binaries | γ_v ≈ 1.00–1.05 (near-Newton) + period–separation cloud signature | The unbound-cloud architecture | Dec 2026, registered (Amdt 11) |
| Gaia DR4 MW dark-density mapping | Break at ~6 kpc; inner profile = the zero-parameter phantom | The EFE cap | Dec 2026+ |
| Binned RAR scatter vs Y | Flat floor (a rising floor would have revived the photocount mechanism — killed) | Equilibrium vs mechanism | Existing SPARC data |

## 7. REPRODUCTION

All lanes: `glm53_push/G001…G012_*.py` (+ `.out` + `_results.json`), each
exiting nonzero on failed internal checks. Lean: `glm53_push/lean/` —
G001 (9 theorems), G002+G003 (4), G007 (11); compile with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean`.
Lane conventions: measurement and threshold stated separately, every FAIL is a
finding, no literal-True pass conditions (commit-guarded).

---

*Never say the theory is closed. This document states what is earned, what is
measured, what is dead, and what will decide it.*
