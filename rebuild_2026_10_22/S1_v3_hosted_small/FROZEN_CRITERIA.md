# S1_v3_hosted_small — FROZEN CRITERIA (written and committed before any script or number of this lane)

Batch R1 of `rebuild_2026_10_22/N0_board_audit/AUDIT.md`: recompute, for the current best theory v3
(`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1–3), the small systems that sit in a host's field.

- **Tile 26, dwarf satellites vs screened law** (old: FAIL; E3's +0.89 dex used CFG691's isolated S(s) recipe, no EFE).
- **Tile 29, Coma ultra-diffuse galaxies** (old: UNDEC; CFG933/CFG948 used the isolated, EFE-free law).
- **Tile 19 (tidal dwarfs, NGC 1052-DF2/DF4) is lane P4's.** This lane does not compute it. If P4's outputs are
  committed before this lane's README, they are read and cited, not duplicated.
- Feeds tile 31 (one selector for the family) with the v3 excess numbers.

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. No dark-matter particle (the cold sector is BS K(Q) dust,
"cold energy"). Never "theory closed". Never "the data favour the framework". No downloads. Every run
`OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS. CFG960 is not touched.

**Seen before freezing (disclosed).** E3's README/JSON numbers (+0.89/+1.52/+0.56 dex canonical; clean primary +2.01;
W +1.64), CFG933/CFG948's (⟨E⟩ +0.760/+0.669 ln, se 0.262, σ_sys 0.372/0.371), L23's corrected 1-D EFE offset for the
Coma UDGs (+1.16/+1.11 dex, standard-MOND recipe), D10's solver timing at generic parameters (y = 0.001–0.01,
x_e = 0–0.5, Λ = 0–3: boosts printed, no system's data used), and the per-satellite table of y, x_e (MW E_mid law field
at the LVD host distance) and Λ = L★/R_e. No Δ, E, z or class of this lane had been computed.

## 1. The theory solved (FRAMEWORK-NATIVE; no new posit)

v3's static limit with the stiffness term, exactly as D10 solves it (C4-literal, γ_F = 0; D10 K1 sympy):

    ∇²ψ = ∇·p(∇χ),   χ = Φ_N + ψ + (L★²/2) ∇·p(∇χ),   p(v) = v/(1 + |v|/a₀),   ∇Φ = ∇Φ_N + ∇ψ.

L★ = 0 is AQUAL with μ = x/(1+x); L★ → ∞ is Newton. The host enters only as the uniform **total** background field
∇χ_e = g_e ẑ (x_e = g_e/a₀), and the system's response to it is **solved** (no EFE recipe, no ν(y_i + y_e), no
QUMOND). Solver: `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py`, imported read-only (2D axisymmetric finite
volume, exact-Jacobian Newton; D10's grid nper = 24, N_θ = 16, r ∈ [1e-3, 1e4] a). Independent cross-check of the
embedded AQUAL solve: `rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py` (`solve_efe`, point mass, own discretisation),
imported read-only.

**Each system:** a Plummer sphere, scale a = R_e (projected half-light radius), mass = light, M = M★ (gas not in the
source; as E3 and CFG933). Units y = GM/(a²a₀), Λ = L★/a. **Dispersion estimators** from the solved field (monopole of
the radial field, isotropic Jeans; `d10_solver.jeans`):
- **E-W (primary):** σ² = r₁₂ g(r₁₂)/3 at r₁₂ = (4/3) a — the record's Wolf convention, so the data side
  (g_obs = 3σ²/r₁₂) is unchanged from E3/CFG933 and every move is physics;
- **E-V (reported):** the global virial σ² = −(1/3M)∫ρ r·g dV (exact orientation average for a global
  luminosity-weighted dispersion).
The class must be stated for E-V too; if E-V would change it, that is reported.

**μ_K² term (BS24 Eq. 35).** Not solved; bounded (§4, S5). At BS's cap μ_K ≤ 14.8 h/Mpc (h = 0.6856, F3/L1 model B)
its static term is a Helmholtz piece of relative size ε = μ_K² r²/μ(x) on the internal problem, and its only other
possible effect is host dust inside the system, whose density cannot exceed the host's total local dynamical density.

## 2. The ingredient chain (one change at a time; the statistic is reported after each)

| step | satellites (tile 26) | Coma UDGs (tile 29) |
|---|---|---|
| S0 old | E3: CFG691 S(s) on ν₁, isolated, g_bar = G(M★/2)/r₁₂² (reproduced, K1) | CFG933/948: isolated ν_e law, Wolf (reproduced, K7) |
| S1 kernel | ν₁ (already E3's: zero move, stated) | ν_e → ν₁ |
| S2 geometry | AQUAL solve of the Plummer sphere, isolated, L★ = 0, E-W | same |
| S3 EFE | the same solve in the host field (MW/M31 E_mid law field) | the same solve in Coma's measured field at dmean |
| S4 native screening = **v3** | + γ_L at L★ = floor (21.68 canonical / 22.85 alt, D10), 24, 90 pc | same |
| S5 μ_K² | bound ε (internal) and host-local-density bound (§4) | same |
| S6 native H₀ | none (stellar distances, H₀-free) | Coma distance × 70/67.9 = 1.031, labelled ASSUMED (source H₀ not on disk) |

Reported side rows (no verdict weight unless named in §4): isolated native screening (x_e = 0) at each L★ against
CFG691's recipe; estimator E-V; host-field bracket.

## 3. Inputs and errors

**Satellites.** E3's sample rebuilt from `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` with E3's code
path (own implementation): 45 canonical / 46 alt below M_crit = a₀(24 pc)²/G. Data choices exactly E3's: **clean primary**
(LVD σ × Arroyo-Polonio free-f ratio, Υ_V = 2), **raw** (A26), **worst-clean W** (Υ_V 4, f = 0.7 ratios, lower of
LVD/Geha σ, upper limits dropped). Per-system Monte Carlo (σ, R_e, distance modulus; M★ ∝ D², R_e ∝ D) × bootstrap over
systems, NMC = 2000, NBOOT = 4000, own seed. **Host field:** v3's law field of a Hernquist baryonic host (a_H = 3 kpc)
at the LVD `distance_host`: MW **E_mid** 6e10 M☉, **E_lo** 4e10, **E_hi** D10's Mb_hi(a₀) (law field at 8 kpc = 2.0592e-10);
M31 1e11 M☉ (E3/D2 external label) with the same fractional bracket; the one field system (Leo T) gets the MW field at
its LVD heliocentric distance. M31 satellites ignore the MW (≤ 0.02 a₀). Spherical host ⇒ AQUAL host field = law field
exactly. **MC propagation of the prediction:** per system log B is tabulated on a 3 × 3 grid (Δlog y = −0.6, 0, +0.6;
Δlog Λ = −0.3, 0, +0.3 about the central values) and interpolated bilinearly in logs (linear extrapolation outside);
per draw y = GM_draw/(a_draw² a₀), Λ = L★/a_draw. Host-bracket rows use the per-system central shift.

**Coma UDGs.** `real_research/data/freundlich2022_coma_udgs.tsv`; CFG933's admission rules S1–S5 give the 9 admitted
(DF44, J125904.06 reported as "all 11"). M★ = L × M/L; σ_obs ± esig. Per galaxy E = 2 ln(σ_obs/σ_pred) (CFG933's sealed
convention), sE = 2 e/σ_obs; ⟨E⟩ = unweighted mean; se_obs = max(scatter term, measurement term) (CFG933 `summ`).
**σ_sys** = CFG948's recipe recomputed with the v3 prediction: half the ± difference of ⟨E⟩ for M★ × 10^±0.2,
σ × 1.15^±1, distance × 0.95/1.05 (M★ ∝ D², R_e ∝ D and the Coma-centric distance ∝ D), in quadrature.
**Host field:** Coma's measured total (hydrostatic) acceleration, Freundlich+2022's isothermal β-model as in L23/CFG948
(kT 8.6 keV, r_c 276 kpc, β 0.71, μ 0.6): g(r) = 3βkT r/(μ m_p (r² + r_c²)), at **dmean** (mean 3-D distance,
primary) and **dproj** (projected, bracket). Reported: field ÷ 2 (proxy for v3's law-on-baryons Coma field, which F1
finds 1.5–1.9× short inside 1 Mpc), the isolated bound (x_e = 0), all 11 Coma.

## 4. Statistics and verdict lines (frozen)

**Satellites.** Δ = bootstrap median over systems of log₁₀(g_obs/g_pred), g_obs = 3σ²/r₁₂, g_pred = 3σ_pred²/r₁₂;
σ_Δ = bootstrap sd. Per footing, per L★, per data choice.

Tile 26 verdict:
- **FAIL** if, with the clean primary, |Δ| ≥ 3σ_Δ at L★ = floor, 24 and 90 pc on both footings, **and** the worst-clean
  W is still ≥ 2σ_W from the v3 prediction at the floor (both footings), **and** the most favourable host-bracket cell
  (E_lo/E_mid/E_hi) at the floor is still ≥ 3σ_Δ.
- **PASS** if |Δ| ≤ 2σ_Δ at the floor on both footings.
- **CONDITIONAL** otherwise, naming the reason (2–3σ; ≥ 3σ on the primary but W within 2σ; footing or bracket split).
- **NOT DECIDABLE** if any of K2–K6 fails, or if the host-local-density bound (S5) could supply ≥ the median system's
  missing mass (then the μ_K² zero point decides, which v3 does not fix).

**Coma UDGs.** z_stat = ⟨E⟩/se_obs; z_sys = ⟨E⟩/√(se_obs² + σ_sys²); per footing; at dmean and dproj.

Tile 29 verdict:
- **FAIL** if |z_sys| ≥ 3 on both footings at dmean **and** at dproj. Label **ROBUST** if also |z_sys| ≥ 3 with the
  field ÷ 2, else **FIELD-DEPENDENT**.
- **PASS** if |z_stat| ≤ 2 on both footings at dmean and at dproj.
- **CONDITIONAL** otherwise, naming the reason.
- **NOT DECIDABLE** if any of K2–K6 fails, or if the host-local-density bound could supply ≥ the mean galaxy's missing
  mass.

**S5 bounds (reported, and used only in the NOT DECIDABLE clauses).** (i) ε = μ_K² (3r₁₂)²/μ(x_e) at μ_K = 14.8 h/Mpc,
max over systems; reported as negligible if < 1e-2. (ii) Host-local density ρ_h at the system's position: satellites,
the law field's phantom-inclusive density ρ_h = (1/4πG r²) d(r² g)/dr of the Hernquist host (E_hi); Coma, the same from
the β-model field. Ratio ρ_h/ρ_need, ρ_need = (M_dyn − M_pred(<r₁₂))/((4/3)π r₁₂³), median and max over systems.

**Old → v3.** Each tile is reported as old colour → v3 verdict, with the chain step responsible for the change.

## 5. Checks (script `s1_v3_hosted_small.py` prints `Kn PASS/FAIL value threshold`; exit 0 iff all pass)

- **K1** E3 reproduced (own code): N = 45 / 46; Δ above the CFG691 recipe at L★ 24, 90 and the unscreened law within
  0.02 dex of +0.886 / +1.518 / +0.557 (canonical), +0.846 / +1.489 / +0.508 (alt); clean primary E_N within 0.02 of
  +2.013 / +1.998.
- **K2** isolated L★ = 0 (D10 2D) vs the algebraic law, E-W and E-V, y ∈ {3e-4, 3e-3, 3e-2}: < 2e-3.
- **K3** embedded L★ = 0: D10 2D vs F2's independent AQUAL point-mass solver; angle-averaged M_eff(r)/M at r/r_M ∈ {3, 10},
  y = 100 (r_M = 10 a), x_e ∈ {0.1, 0.5} (F2 called with y_e = x_e²/(1 + x_e)): < 2e-2.
- **K4** linear EFE: D10 2D monopole field at r = a vs Route F (C6 kernel), x_e ∈ {0.05, 0.5}, y = 1e-4 x_e,
  Λ ∈ {0, 0.5, 2}: < 2e-2.
- **K5** convergence (UFD-like y 3e-3, x_e 0.1, Λ 0.3; UDG-like y 0.03, x_e 0.6, Λ 0.02): doubling N_r and N_θ, and
  r_out × 10, change σ (E-W and E-V) by < 5e-3.
- **K6** Newton limit: Λ = 1e4, x_e 0.1, y 3e-3: σ within 2e-3 of Newton.
- **K7** CFG933 reproduced: per-galaxy E_obs of the 9 (isolated ν_e, Wolf) equal `cfg933_results.json` to 1e-9;
  ⟨E⟩ and se_obs within 1e-6 (both footings).
- **K8** CFG948's σ_sys components reproduced with the isolated ν_e law: s_M, s_A, s_D within 2e-3 of the JSON
  (canonical 0.2400 / 0.2795 / 0.0500; alt 0.2391 / 0.2795 / 0.0500).
- **K9** every production solve converged (scaled residual < 1e-8).
- **K10** peak RSS < 1 GB.

`--mutate`: the host-field convention bug (the solver's background set to the Newtonian external field
y_e = x_e²/(1 + x_e) instead of the total x_e). K3 must FAIL. Mutate runs the checks only; outputs `*_MUTATE.out`,
`*_results_MUTATE.json`.

## 6. What each outcome means

- Tile 26 FAIL: in v3 the satellites sit above their own baryons' prediction in the host field, after the data
  systematics; v3 has no bound cold component at these scales (BS dust at μ_K ≤ 14.8 h/Mpc does not cluster below
  ~0.1 Mpc), so the excess is unexplained by v3. A changed number with the same colour is reported as such.
- Tile 29 FAIL: the Coma UDGs exclude v3's prediction in Coma's field; old UNDEC → FAIL, cause named (the EFE step).
- CONDITIONAL / NOT DECIDABLE: the missing ingredient is named.

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the
framework over ΛCDM.
