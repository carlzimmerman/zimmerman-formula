# Frontier 3 — the unified scalar: does ONE K(Q) field do BOTH the CMB dust AND the cluster residual? (2026-06-15)

*Opus 4.8 [1m]. The cost-reduction frontier, pushed to the PHYSICS (the sound-speed gate the banked work
flagged "open" but never computed). sympy: the AeST k-essence sound speed cs²; the Jeans-scale-blindness
argument. Web-verified: Skordis/Verwayen/Durakovic structure formation + the Mistele squeeze + the
dynamical-systems late-time fate. Both ways. Quarantine held: a0/Z never asserted derived; I0, μ, K2/Q0 flagged
as free AeST constants. No manufactured +1 win, no dismissal of genuine structure.*

## Bottom line — the cost is +2, NOT +1. The unified-scalar recovery FAILS, by a structural sound-speed squeeze.
The single most promising cost-reduction route (one I0 does both CMB and clusters) **does not close**, and the
reason is now a COMPUTED physics result, not a literature "open" flag: the k-essence dust's sound speed cs² is
**scale-blind**. The CMB third-peak fit forces cs²→0 (so the dust clusters like CDM) — but a cs²→0 pressureless
condensate has a vanishing Jeans scale, so it clusters at galaxy scales TOO, which would spoil the pure-MOND RAR
that a0=Λ delivers. There is no single cs² that clusters at 1–3 Mpc (clusters) yet stays smooth at 30 kpc
(galaxies). So the dust amplitude I0 cannot be reused to supply the cluster residual while keeping galaxies pure
MOND. The cluster boost in AeST is instead the SEPARATE Y-sector mass term μ (Verwayen/Durakovic), a distinct
free parameter that the Mistele squeeze independently double-binds. **Concede +2: I0 for the CMB dust, μ for the
clusters.**

---

## (i) The sound speed — COMPUTED (sympy), the gate the banked work left open
AeST cosmological sector: shift-symmetric k-essence in the temporal scalar Q=A^μ∇_μφ, with
K(Q) = −2Λ + K2(Q−Q0)² + …  Background ρ = Q K′(Q) − K, p = K(Q).

**sympy-exact result** (`/tmp/kessence_soundspeed.py`): the adiabatic AND the Garriga–Mukhanov perturbation
sound speeds COINCIDE for this K:
> **cs² = (Q − Q0)/Q = 1 − Q0/Q.**

Background relaxation: K′(Q)=I0/a³ ⟹ Q−Q0 = I0/(2K2 a³) ∝ a⁻³. So
> **cs²(a) ∝ a⁻³** — it is ~1 early (field far from the minimum) and → 0 late (field at the dust minimum Q→Q0).

This is the correct, known k-essence behavior; the dust mimic (ρ∝a⁻³, the CMB CDM-stand-in) lives exactly where
Q→Q0 and cs²→0. **Gate (i) — "does it cluster?" — PASSES on sound speed:** the CMB-fitting dust has cs²≈0, so it
is gravitationally unstable and clusters like CDM. *But passing this gate is necessary, not sufficient — and it is
the SAME property that breaks galaxies (see iii).*

**Quantified, the CMB already forces cs² steep** (`/tmp/kessence_cs2_quant.py`): for the dust to drive the third
acoustic peak it must not free-stream at recombination, i.e. cs²(a_rec) ≪ 1. Since cs² ∝ a⁻³ and a_rec⁻³ ≈ 1.3×10⁹,
the CMB forces cs²_0 ≲ 10⁻⁹ today. Propagating that SAME K2 to the cluster epoch (z≲1, a≳0.5): cs²(cluster) ≲ 10⁻⁷
— **effectively zero. The dust does cluster at cluster scales.** The K2 curvature is a separate model scale (2K2Q0²),
not fixed by I0, but the CMB pins it steep, and steep is steep at all later times.

## (ii) Is the cluster-clustering amount set by the SAME I0 as the CMB? — YES, but that is the PROBLEM, not the win
If the dust truly clusters like CDM (cs²≈0, pressureless), it does what CDM does: forms halos tracing the SAME
cosmic Ω_dust ≈ Ω_dm ≈ 0.265 = the SAME I0 that fits the CMB. Ω_dm/Ω_b ≈ 5.4, cluster f_b(cosmic) ≈ 0.156, CDM
supplies the rest → FULL cluster closure. So in the regime where the dust clusters, **one amplitude I0 does both
the CMB and the clusters — superficially the +1 win the frontier hoped for.** BUT this regime is exactly CDM: the
dust supplies the WHOLE cluster mass (ratio ~5), not the modest MOND residual η~1.3–2.33. The framework would have
become ΛCDM-with-a-scalar — and would then DOUBLE-COUNT in galaxies (MOND boost + a clustered dust halo). It is not
a +1 *unification* win; it is a collapse to CDM.

## (iii) The Mistele squeeze, now at the level of the dust's sound speed (the decisive structural point)
The Jeans scale of the dust is λ_J ~ cs/√(Gρ). With cs²≈0 (CMB-forced), λ_J → 0: a pressureless condensate is
unstable and clusters on ALL scales below λ_J ≈ 0. **There is no scale-selective clustering for a single cs².** So:
- **To keep galaxies pure MOND** (the a0=Λ RAR with NO dark halo — the framework's central win), the dust must
  stay SMOOTH at ≲100 kpc.
- **To supply the cluster residual**, the dust must CLUSTER at ~1–3 Mpc.
Both are governed by the SAME cs²≈0. A single pressureless field clusters at both scales or (if some mechanism
keeps it smooth) neither — you cannot have it cluster at 1 Mpc and stay smooth at 30 kpc with one knob. **This IS
the Mistele/McGaugh/Hossenfelder 2023 squeeze (the combination m²/f_G is pulled ≲1 Mpc⁻² by galaxy weak lensing and
≳1 by clusters — same free knob, opposite directions), seen here at the cosmological-dust level.** Web-verified
verbatim (arXiv:2301.03499): AeST "reproduces MOND only up to a maximum galactocentric radius… m²/f_G can be
adjusted to explain [clusters]… shows deviations from MOND at the radii probed by weak lensing, creating tension."

Therefore the cluster boost is NOT the cosmological dust (I0) — it is the SEPARATE Y-sector shift-symmetry-breaking
mass term μ (Verwayen-Skordis-Zlosnik 2024, MNRAS 531 272; Durakovic-Skordis 2024, JCAP 04 040). The Verwayen
quasi-static cluster solution needs **μ, β₀, and a free boundary constant χ_out/Δ** — and it is banked-FALSIFIED as
a clean cure (peak-then-deficit "as if negative mass," per-cluster-tuned, Mistele-squeezed). Its μ is a distinct
free parameter, NOT I0.

## The dust's late-time fate — an additional both-ways nuance (web-verified)
The canonical CMB-fitting model (K2(Q−Q0)², n=2) keeps the dust ∝(1+z)³ to z=0 — so it IS present at clusters, and
the analysis above applies. **But** the AeST dynamical-systems exploration (arXiv:2309.06232) finds the dust-like
contribution "generally occurs for a limited period of cosmic time," and for n=1/2-type K-shapes it deviates from
dust at late times. Both ways: this does not rescue the unification (a decaying dust is even LESS able to supply
clusters), and it does not change the verdict (the CMB-fitting branch has the dust present, scale-blind, squeezed).

## The +1-vs-+2 ledger (the frontier's actual question, answered)
| component | what supplies it | parameter | shared with CMB? |
|---|---|---|---|
| CMB third peak / P(k) | K(Q) dust mode, ρ∝a⁻³ | **I0** (free integration constant ≈Ω_dm) | — |
| galaxy RAR/BTFR | a0=c²√(Λ/32π) Y-sector | a0=Λ (the spine) | no (orthogonal sector) |
| cluster residual η | **NOT the I0 dust** (scale-blind/squeezed) — the μ²Φ mass term | **μ** (distinct, double-bound) | **NO** |

**Verdict: +2.** The unified-scalar hope (one I0 for CMB and clusters) is structurally blocked: the cs²≈0 that lets
the dust cluster at clusters also clusters it in galaxies and kills pure MOND. The cluster boost costs the separate
μ. Concede +2 (I0 + μ), exactly as the banked CMB/cluster reviews suspected — now backed by the computed cs² and
the Jeans-scale-blindness argument, not just a literature "open" flag.

## Both ways (one line)
The sound-speed gate the dust must pass to cluster (cs²≈0, CMB-forced) is the SAME gate it CANNOT pass selectively
— a single pressureless condensate is scale-blind, so it cannot cluster at clusters while staying smooth in
galaxies; the cluster boost is the separate, Mistele-squeezed mass term μ, so the cost is +2 (I0 + μ), not the +1
the unified-scalar hoped for. Credit at full weight: the dust DOES cluster (cs²≈0 verified), and IF one allowed it
to be full CDM, one I0 would do both — but that fork is just ΛCDM and breaks the galactic MOND win. No manufactured
+1; the genuine structure (cs²=(Q−Q0)/Q, the dust clusters) is credited; the squeeze that defeats the unification
is the honest blocker. Quarantine held: a0/Z never asserted derived.

## Sources (web-verified this session)
- Skordis & Zlosnik 2021, PRL 127 161302 (arXiv:2007.00082) — AeST; k-essence dust ρ∝a⁻³; I0 free.
- Verwayen, Skordis & Zlosnik 2024, MNRAS 531 272 (arXiv:2304.05134) — quasi-static cluster solution: μ, β₀, χ_out/Δ; "warrants N-body beyond spherical isolated sources."
- Durakovic & Skordis 2024, JCAP 04 040 (arXiv:2312.00889) — isothermal-sphere cluster μ²Φ; peak-then-deficit.
- Mistele, McGaugh & Hossenfelder 2023, A&A 676 A100 (arXiv:2301.03499) — the m²/f_G galaxy↔cluster squeeze, verbatim.
- AeST dynamical-systems (arXiv:2309.06232) — dust "limited period of cosmic time"; n=2 vs n=1/2 late-time fate.
- Garriga & Mukhanov 1999 (arXiv:hep-th/9904176) — k-essence cs² = P_X/(P_X+2XP_XX), used in the sympy check.
