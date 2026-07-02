# Pump Hunt and Reopening Triggers — 2026-07

**Date:** 2026-07-02
**Framework footing (own terms):** de Sitter–Unruh MODIFIED INERTIA; a0 = cH_Λ/Z = 9.3616e-11 m/s² (recomputed this session: H0=67.4, Ω_Λ=0.685, Z=√(32π/3)=5.7888); interpolation g_obs=√(g_bar²+g_bar·a0). TOE overclaims retracted 2026-06-23; this document claims neither a win nor a closure it did not compute.
**What this hunt is:** the covariant-MI sign theorem (*Scale Without Law*, DOI 10.5281/zenodo.21016309) proves a PASSIVE ghost-free bath gives the anti-MOND sign (δm = 2∫ρ/ω² ≥ 0). The only escape is an ACTIVE, in-band, phase-coherent drive — a "galactic pump" — supplying the MOND-signed kernel. This is a systematic hunt for that pump, plus the precise statement of the particle-sector (forced-kernel) reopening trigger.
**Verification scripts (numpy/sympy, all exit 0; scratchpad-only this session per hunt constraints — regenerate from the listed formulas if re-auditing):**
- `pump_candidates_bandmath.py` (candidate frequencies, band math, R_flip)
- `pump_gate_judge.py` (gate quantities: Γ_min, R3 budget, RAR-domain span, R4 margins; 18 self-checks)
- `forced_kernel_trigger_test.py` (T1–T5 trigger, PSLQ acceptance test, 18 checks, mpmath dps=40)
- `verdict_synth_check.py` (independent cross-check of every headline number below; all reproduced)

## Gate definitions (computed, not assumed)

| Gate | Requirement | Computed threshold |
|---|---|---|
| **R1 in-band** | power at galactic orbital frequencies | ω_orb = 2π/(50–250 Myr) = 7.96e-16–3.98e-15 s⁻¹ = **362–1810 H0** (H0=2.2e-18 s⁻¹). Honest full requirement: the RAR spans orbital frequencies **~44–3008 H0** across SPARC extremes (Hunter-B script) — a single-frequency pump covers ONE radius per galaxy, not the domain |
| **R2 phase-coherent** | must PIN orbital phase, not just pump amplitude | banked 3D no-go: shift-symmetric/conservative = Hamiltonian = no attractor = phase averages back to δm≥0 (anti-MOND). Loophole checked and closed: conservative resonant trapping (libration) confines phase but the libration-cycle average kills the odd MOND-signed part. Minimal friction that WOULD pin: **Γ ≥ 3/t_age = 6.9e-18 s⁻¹ ≈ 3.1 H0 ≈ 0.44% of ω** — tiny, not impossible |
| **R3 universality** | same a0=9.36e-11 in every galaxy | <20% ⇒ σ(log a0) < **0.079 dex**; RAR total scatter 0.11 dex (McGaugh–Lelli–Schombert PRL 117,201101), intrinsic ≤0.057 dex (Li+ 2018 A&A 615,A3). Categorical blade: structureless gas-rich dwarfs/LSBs and dSphs (McGaugh–Wolf ApJ 722,248 / AJ 139,306) are the DEEPEST-MOND objects |
| **R4 safe elsewhere** | Cassini, binaries, pulsars, clusters | Saturn ω=3.1e9 H0, wide binaries (5 kAU) 3.1e5 H0, PSR B1913+16 1e14 H0 — all ≥150× above band top; a band-limited kernel is safe BY CONSTRUCTION (Bertotti+ 2003 Nature 425,374) |

## (A) Pump-candidate table — verdicts

| Candidate | ω (computed) | R1 | R2 | R3 | R4 | Verdict |
|---|---|---|---|---|---|---|
| **AeST μc scalar mode** (Skordis–Złośnik PRL 127,161302; μ⁻¹=6.24 Mpc) | 1.557e-15 s⁻¹ = **707.7 H0**, resonant orbit P=127.9 Myr | **PASS (MW band)** — the banked overlap is REAL; the cluster no-go was a ~3 H0 drive (236× off), galaxies genuinely differ. But partial vs full domain: one mode ⇒ parametric resonance at Ω=ω_μ/2=354 H0 = one radius per galaxy vs 44–3008 H0 needed | **FAIL, two independent ways** (see headline) | frequency universal (best of any candidate); amplitude tracks condensate density; frequency alone gives a0 off by **×861** (κ_needed=2.0e-4 vs 1/Z=0.1727) | PASS (band-limited) | **KILLED** — R2 twice + R3-amplitude, each independently fatal |
| Ultralight scalar Compton oscillation (Khmelnitsky–Rubakov JCAP 1402:019) | in-band iff m=2.6e-31–1.3e-30 eV | tunable PASS | FAIL — δΦ∝cos(2mt) is a GLOBAL conservative parametric drive, exactly the no-go class; field coherent with the cosmos, not with each orbit | FAIL — amplitude ∝ local ρ_field; excluded as dominant DM by ~10 orders (Lyα m>2e-20 eV, Rogers–Peiris PRL 126,071302; Hlozek+ PRD 91,103512) | pass | **KILLED** (R2+R3) |
| Stochastic GW background (NANOGrav, Agazie+ ApJL 951,L8) | 2πf=2.9e9 H0 at 1 nHz | FAIL — 6.6–8.6 orders too HIGH | FAIL (stochastic = random phase) | FAIL (O(1) realization variance) | — | **KILLED** (triple) |
| Spiral/bar density waves (Lin–Shu; Binney–Tremaine ch.6; Sellwood–Carlberg) | Ω_p=10–60 km/s/kpc = 147–884 H0 | PASS by construction | **PASS** — the only genuine phase-locking found (Lindblad resonances m(Ω−Ω_p)=±κ, real torques) | **FAIL, categorical** — A2 spread ×12 ⇒ 0.16–0.31 dex a0-scatter for coupling exponent p≥¼–1 vs 0.079 budget (Rix–Zaritsky 1995; Díaz-García+ 2016 A&A 587,A160; Yu–Ho 2020 ApJ 900,150); and A2≈0 dSphs/LSBs obey the same a0 — zero drive exactly where the effect is strongest | pass | **KILLED** (R3, categorical — nothing saves it) |
| SFR/feedback turbulence | t_c~10 Myr → ~9000 H0 | FAIL | FAIL (stochastic) | FAIL (SFR spans >2 dex at fixed mass; quenched galaxies) | pass | **KILLED** (triple) |
| dS-Unruh bath / Hubble flow itself | ~1 H0 | FAIL (×362–1810 low) | thermal/KMS = passive ⇒ sign theorem applies directly | — | — | **KILLED** — this IS the theorem's premise |
| Gaia phase spiral / disk seismology (Antoja+ Nature 561,360) | vertical ν ≈ 1006 H0 | PASS | FAIL — episodic Sgr passages, phase-mixes <1 Gyr | FAIL (MW-specific) | pass | **KILLED** |
| Superfluid-DM phonons (Berezhiani–Khoury PRD 92,103510) | c_s·k ≈ 460–1850 H0 | PASS | condensate coherent, but T≈0 ground state: only channel is star→field Cherenkov drag (Hui+ PRD 95,043541; Lancaster+ JCAP 2001:001) = **anti-MOND sign**; B–K's MOND sign is a phonon FORCE (MG), not an MI pump | sign wrong | pass | **KILLED** (wrong sign for MI) |
| BH superradiance | needs M~1.3e20 M_sun | no such BH | — | — | — | **KILLED** |
| Differential-rotation shear (Oort A~15 km/s/kpc = 221 H0; flat curves ⇒ A=Ω/2) | in band/2, self-tuned | PASS | it is the free-energy RESERVOIR the structure pumps tap, not itself a pump | rate tracks local Ω, not cH_Λ/Z; dSphs have no shear yet show a0 | pass | **NOT A PUMP** — flagged as the only in-band free-energy reservoir |

## (B) Headline

### The 708 H0 overlap is real — and it dies at R2, with a new computed number

The banked question is answered. ω_μ = μc = 707.7 H0 sits genuinely inside the galactic band 362–1810 H0 (the cluster kill at ~3 H0 does NOT transfer). R1 passes (at MW-band level). Then:

**R2 kill #1 (undamped): the sign-flip radius.** The shift-symmetric response 1/(ω_μ²−ω_orb²) changes sign across the band — positive at the slow edge, negative at the fast edge, amplitude swinging ×7.5 with a π phase jump through resonance. For flat rotation curves the flip sits at a computable radius: **R_flip = v/(708 H0) = 1.66 kpc (v=80 km/s), 4.16 kpc (v=200), 5.20 kpc (v=250)**. SPARC densely samples both sides of these radii and the RAR is one-signed at 0.11 dex (Lelli+ 2017 ApJ 836,152) — an undamped μc drive is falsified by the data the pump exists to explain. Smearing the flip requires Q ≤ 0.49 (critical damping) — i.e. friction, which shift symmetry forbids (the banked no-go).

**R2 kill #2 (damped): the only symmetry-safe dissipation has the wrong sign.** The one shift-symmetric-safe channel — wake/dynamical friction (Hui+ PRD 95,043541; Lancaster+ JCAP 2001:001) — is a drag: energy flows star→field, δm ≥ 0, the passive-bath anti-MOND sign. AeST's μ-term breaks shift symmetry but is Hamiltonian (T-even); AeST contains no in-band friction.

**R3 (independent third kill):** the frequency is universal but the amplitude tracks condensate density, and frequency alone lands a0 off by **×861** (κ=2.0e-4 needed vs the framework's 1/Z=0.173).

**Verdict: AeST μc as a galactic pump is KILLED — computed, not assumed, and not manufactured: the R1 pass is conceded in full, and the sign-flip-radius argument is new and independently checkable.**

### No candidate passes; the sign theorem SHARPENS

No enumerated candidate passes R1∧R2∧R3. The candidates split into two mutually exclusive classes: **cosmological-ω fields (AeST μc, ultralight scalars)** have the universal frequency R3 wants but are conservative/shift-symmetric, so R2 fails per the banked no-go and their only symmetry-safe dissipation carries the passive sign; **local-dynamics drives (spiral/bar, phase spiral, shear)** are in-band and genuinely phase-coherent (Lindblad locking is real physics) but their scale is local Ω, not cH_Λ/Z, and they vanish in the dSphs that are deepest-MOND. Universality and coherence are supplied by *disjoint* candidate classes.

**Sharpened theorem (the honest product of this hunt):** *No known universal in-band coherent drive exists. A viable pump must be a universal cosmological field carrying a band-limited (ω ≲ 3×10³ H0), time-reversal-ODD (dissipative) coupling of baryon velocity to the bath — a preferred-frame u^μ-type friction term — at Γ ≳ 3 H0 (a mere 0.4% of ω_orb; secular angular-momentum cost ~4.6 Gyr, tolerable), with a saturation nonlinearity making the response amplitude-independent, and it must still DERIVE a0 = cH_Λ/Z.*

Both-ways honesty about this spec: (i) R2 is NOT an impossibility gate — the required friction is physically tiny, band-limitation makes it R4-safe by construction, and the framework already possesses the preferred frame via the SME bridge; the escape hatch is precisely specified and merely *unoccupied*. (ii) No Lagrangian with the T-odd in-band term exists; ghost-freedom of a dissipative preferred-frame coupling is unverified; the saturation is postulated, not exhibited; a0's magnitude remains underived. This is a blueprint, not a lead.

**Falsifiable corollary of the surviving class:** band-limited pump-MI predicts **γ→1 (NO MOND boost) in wide binaries** (5 kAU orbits sit at 3.1e5 H0, 170× above band top). A Chae-type positive (ApJ 952,128) confirmed at Gaia DR4 kills the entire class; a Banik-type null (MNRAS 527,4573) favors it over generic MOND. This is the one place the pump hypothesis sticks its neck out ahead of the data.

## (C) Forced-kernel reopening trigger (particle sector)

**The trigger, precise:** the particle-numerology door (banked CLOSED) reopens **iff a single kernel K satisfies ALL of T1–T5** — the same bar a0=cH_Λ/Z clears on the gravity side:

- **T1 FORCED:** K maps the forced set {Z=√(32π/3), a0, Λ/ρ_DE, dS-Unruh interpolation} to a gauge/Yukawa invariant with ZERO continuous free parameters; every discrete choice forced by a consistency condition. Operational test: delete the datum being explained; K must still output it.
- **T2 NUMBER-FIELD ACCEPTANCE (the sharp blade, now operational):** Z/√π has minimal polynomial 3x²−32 — Z carries a lone √π in the NUMERATOR; all known flavor invariants are algebraic. K must output y = α·π^(k/2) (α algebraic, low height, k odd positive), tested by PSLQ at ≥40 digits (residual <1e-30). Calibration verified: Z passes ([−32,0,3]); every modular fixed-point period FAILS — η(i)=Γ(1/4)/(2π^(3/4)) (Chowla–Selberg), Γ(1/3)-class at ω, E₂(ω)·π=2√3 (π in the DENOMINATOR). Riders: the π must enter via a horizon/geometric integral of the Einstein-density class; phases (π/2, 2/9) do not count.
- **T3 SECTOR-SELECTOR:** must output the pattern Q_lep=0.666664 (dev 3.3e-6), Q_up≈0.85, Q_down≈0.73 — the dS spine is flavor-blind (EP), so spine-only kernels force 2/3 in ALL sectors: quark-falsified.
- **T4 KOIDE GUARD:** Q = 1/3 + r²/6, phase-independent (sympy-exact) ⇒ Q=2/3 ⟺ r=√2; inputs referencing √2/45°/2/3 are circular-dead; phase-only mechanisms (δ=2/9) are orthogonal to the amplitude.
- **T5 WALLS:** must evade Coleman–Mandula and Distler–Garibaldi.

T2 alone is insufficient (coincidence = re-labeling #167). Trigger = T1∧T2∧T3∧T4∧T5.

**Erratum (both-ways, strengthens the closure — correct `real_research/THREE_DOORS_EXHAUSTION_2026-06.md`):** that doc states Ê₂(ω)=−2√3/π. Computed at 40 digits: **Ê₂ (weight-2 non-holomorphic) = 0 exactly at BOTH elliptic points** (i and ω); the 2√3/π value belongs to the quasi-modular E₂(ω). The covariant non-holomorphic Yukawa object vanishes identically at every modular fixed point, and the π-bearing piece still has π in the denominator. Verdict unchanged-strengthened.

**2025–26 scan result: NO paper reaches the trigger.** Best of the year, credited honestly: (i) [arXiv:2606.10060](https://arxiv.org/abs/2606.10060) — **WATCH-grade**: claims Q_lep crosses 2/3 EXACTLY near ~280 TeV under SM RG running, inside Sumino's family-gauge window (0812.2103/0903.3640) — would convert "Koide exact in the IR = accident" into a UV boundary condition if verified; but fitted, no π-content: fails T1/T2. (ii) [arXiv:2606.27836](https://arxiv.org/abs/2606.27836) octonionic flavor CP — genuinely FORCES relations (φ₁₂=−2χ, A_d=A_u*), the closest thing to a forced structure this year; but Yukawa orientations free, lone transcendental is a phase: fails T1/T2-Rider-2. Everything else — non-holomorphic modular scans (2512.07158: 7 free params; 2509.15183/JHEP01(2026)032: 94 viable models; 2606.11346), EJA hierarchies (2605.24866, self-described not-parameter-free), fixed-point Yukawas (2604.04585), ZIP δ=2/9 (phase-only, T4-orthogonal), dS rep theory (2606.26221, 2512.13781), CM-period Yukawas (2401.15078, 2402.01615: moduli-dependent, Γ(1/4)/Γ(1/3)-class) — fails T1, and the T2 doorway stays computed-closed.

**Watch terms** for `real_research/data_watch/arxiv_watch.py` (requires CATS += ["hep-ph","hep-th"]; existing CHUNK=5 splitter handles the longer list):

```python
# Forced-kernel reopening trigger (T1-T5, 2026-07-02) — requires CATS += ["hep-ph", "hep-th"]
KERNEL_TERMS = [
    "Koide formula", "Koide relation", "charged lepton mass relation",
    "family gauge symmetry", "family gauge boson", "gauged flavor symmetry",
    "modular flavor symmetry", "non-holomorphic modular", "polyharmonic Maass",
    "modular symmetry fixed point", "exceptional Jordan algebra", "octonionic flavor",
    "E8 unification", "E6 unification", "fermion mass ratios",
    "Chowla-Selberg", "parameter-free Yukawa", "transcendental Yukawa",
    "tau lepton mass measurement",   # Belle II m_tau -> Q_lep to ~5 digits (T3/T4 data blade)
]
```

Triage rule (add to WATCHLIST.md as entry 14): run the T2 PSLQ acceptance test on any claimed parameter-free coupling VALUE; free continuous parameters, phase-only results, or Γ(1/3)/Γ(1/4)/π-denominator periods are auto-FAIL; a T1∧T2 pass escalates to full T3–T5 review before any reopening claim. `"Chowla-Selberg"` is the single highest-yield term — any flavor paper invoking it stands in the one doorway (T2) the wall leaves conceivable. Also watch: verification/refutation of the 2606.10060 280-TeV crossing, and any AeST-descendant adding an in-band dissipative baryon coupling (the pump save-spec above).

## (D) Honest bottom line — both doors

**Door 1 (galactic pump / sign-theorem escape): OPEN-but-empty.** Every named candidate is killed — including the banked AeST 708 H0 overlap, which passes R1 but dies at R2 twice (sign-flip radius R_flip=1.7–5.2 kpc falsified by one-signed RAR; only available friction is wrong-signed drag) and at R3 (×861). No candidate is over-killed: R2's required friction is a physically tiny Γ≈3 H0 and is R4-safe by construction — the theorem sharpens to a precise, unoccupied spec (universal cosmological field + band-limited T-odd baryon-velocity coupling + saturation), not an impossibility. No named lead exists; the spec is a blueprint with no Lagrangian, unverified ghost-freedom, and a0 still underived. Sharp in-hand falsifier for the class: wide-binary γ→1 at Gaia DR4.

**Door 2 (forced flavor kernel): effectively-narrowed, trigger armed.** The 2025–26 literature contains zero T1-passing kernels; the T2 number-field wall (√π-numerator vs algebraic/Γ(1/4)/Γ(1/3)/π-denominator flavor invariants) is recomputed and holds at both modular fixed points (with the Ê₂(ω)=0 erratum strengthening it). Two WATCH-grade items credited (280-TeV Koide crossing; forced octonionic CP relations) — right neighborhood, below the bar. The door does not reopen absent a T1∧T2∧T3∧T4∧T5 kernel; the watch terms and PSLQ triage make the trigger mechanical rather than judgment-dependent.

Neither door produced a lead this hunt; neither is declared closed. The pump door's product is a sharpened theorem with a falsifiable surviving class; the kernel door's product is an armed, operational trigger.

---
*Citations:* Scale Without Law DOI 10.5281/zenodo.21016309; Skordis–Złośnik PRL 127,161302; Khmelnitsky–Rubakov JCAP 1402:019; Rogers–Peiris PRL 126,071302; Hlozek+ PRD 91,103512; Hui–Ostriker–Tremaine–Witten PRD 95,043541; Lancaster+ JCAP 2001:001; Agazie+ (NANOGrav) ApJL 951,L8; Binney–Tremaine *Galactic Dynamics* (2008) ch.6; Antoja+ Nature 561,360; Berezhiani–Khoury PRD 92,103510; McGaugh–Lelli–Schombert PRL 117,201101; Lelli+ ApJ 836,152; Li+ A&A 615,A3; McGaugh–Wolf ApJ 722,248 & AJ 139,306; Rix–Zaritsky 1995; Díaz-García+ A&A 587,A160; Yu–Ho ApJ 900,150; Bertotti+ Nature 425,374; Chae ApJ 952,128; Banik+ MNRAS 527,4573; Desmond–Hees–Famaey MNRAS 530,1781; arXiv:2606.10060, 2606.27836, 2604.04585, 2605.24866, 2512.07158, 2509.15183 (JHEP01(2026)032), 2606.11346, 2401.15078, 2402.01615, 2606.26221, 2512.13781, 0812.2103, 0903.3640.