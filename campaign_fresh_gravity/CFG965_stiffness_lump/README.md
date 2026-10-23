# CFG965: the stiffness-bound cold lump (NA-3). Class: NO FORMULATION

**In plain words.**
1. NA-3 asked whether a lump of cold energy that feels its own gravity and also carries the stiffness pressure πG L*²ρ²
   would have a fixed size, 2.22 L*, which would turn the dwarfs' 100–200 pc clump into a second measurement of L*.
2. Every live formulation on the record that has the stiffness, the screened theory v3 included, puts it in the same sector as
   the hold (the tether), and that sector cancels the cold mass's own linear gravity, so in v3 an isolated lump's density
   can only rise outward (γ_L D′ = u²/(a₀ − u) ≥ 0) and no lump forms.
3. v3's one self-gravitating piece, its BS dust on scales above 1/μ_K, does make lumps of the n = 1 shape, but their size
   is set mainly by μ_K, and a dwarf-sized lump needs μ_K at 372–1936 × BS24's cap (344 × at the most favourable h), so the
   size would measure μ_K, not L*.
4. The polytrope appears only in variants the record already rejects (CFG941's R1, which breaks the galactic law, and
   CFG938's local-equation-of-state stiffness with the tether switched off), so the frozen class is NO FORMULATION and the
   dwarf fit (Part B) was not run.
5. Nothing here addresses the lump's **mass**, which stays the open supply problem.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻² are never pooled. Only AQUAL μ = x/(1+x) is used: no QUMOND and no
EFE recipe. Cold energy is gravitating mass, not a particle species. Not "theory closed". Nothing here says the data favour
the framework.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (40afd03902), before any script or number. It discloses that
  the record reading and the hand sketches came before the freeze, and that NO FORMULATION was the expected outcome.
- **Derivation:** `DERIVATION.md`.
- **Script:** `cfg965.py` (sympy, numpy, scipy).
  - Main run: **19/19 PASS**, exit 0, ~1 s, peak RSS 0.12 GB, one thread, in-script 1 GB guard.
  - MUTATE: 11/18, exit 1 by design.
- **Footings:** D2 runs per footing. D1 and D3 are dimensionless (units L*, a₀), so footing-free.
- No downloads. No other lane, LEDGER or THEORY file edited.

## Part A result

**v3 (the coordinator's primary target).**
- **The equation of state is there.** v3's cold (khronon) fluid feels −γ_L∇(D·P). Where μ_K can be dropped, that is
  exactly the NA-3 pressure πG L*²ρ_τ².
- **The self-gravity is not.**
  - The exact static spherical equation at μ_K = 0 is γ_L D′ = u²/(a₀ − u) − g_N,b. It is the same equation as CFG938's
    E[M] and the canonical screened law.
  - Without baryons, D′ ≥ 0. Integrated from central u(L*)/a₀ = 0.001–0.5, the density rises monotonically until the hold cap
    (u → a₀ at 1.4–25 L*). There is no edge.
  - H4's dispersion at μ_K = 0 is ω² = ρ_τ[K(M_θ − 1) + γ_L k²] with M_θ ≥ 1. The self-gravity is over-cancelled, and no
    static (Jeans-marginal) scale exists.
- **With μ_K (BS dust):**
  - The static condition is γ_L k⁴ + [K(M_θ − 1) − μ_K²γ_L]k² − KM_θμ_K² = 0, and the profile is sin(k_s r)/(k_s r).
  - NA-3's radius needs μ_K L* = √(2M_θ/(1 + M_θ)) (= 1 at M_θ = 1), a coincidence relation the theory does not contain.
  - The dwarf targets (CFG877 r_t 199 / 163 pc as the edge; CFG870 r_c 104 pc as the half radius) need
    1/μ_K = 52–269 pc. That is μ_K = 5.5e3–2.9e4 h/Mpc: **372–1936 × the BS cap** (344 × at the most favourable h), and
    13–70 × the growth requirement of 411 h/Mpc.
  - d ln R / d ln L* = 0.001–0.49. The size tracks μ_K and the hold, not L*.
  - At the BS cap the lump is 3.9–38.5 kpc (M_θ = 1) or 128–173 kpc with the hold bracket.

**v4 (AeST + γ_L).** Its statics are v3's with μ_K → μ (S4). Against H2's bound μ ≤ 1 Mpc⁻¹, the requirement is ≥ 3714 × the
bound.

**Other formulations** (full table in `DERIVATION.md` §4; the 29 record citations are verified in their files):
- canonical S2/S3 and CFG938/939: the medium is held, so it has no self-gravity;
- canonical S4 free population: no action written, so no stiffness;
- class A, CFG848 and SCT: Newtonian self-gravity, but no stiffness;
- CFG941 R2/R3: the stiffness goes away with the tether;
- the NA-3 lump exists only in **R1** (edge 2.2215 L* at u → 0; 2.27 / 2.34 / 2.53 L* at u(L*)/a₀ = 0.05 / 0.1 / 0.2;
  the law fails by 1.64 / 1.88) and in **CFG938's local EOS with the tether off**. That form is BBN-excluded if the medium
  exists then, and no switch is written. A population born free after z ≈ 8e4 would escape BBN, but no formulation gives
  it this term.

## Deliverables against the frozen task

| item | result |
|---|---|
| class | **NO FORMULATION** (kill condition 1) |
| derivation | v3 carries p = πG L*²ρ² on its held fluid, which has no self-gravity. Its self-gravitating BS dust has a μ_K-set size. No live formulation gives NA-3 |
| L* | none derived. A second, independent L* is not obtainable in v3 (elasticity ≤ 0.49) |
| ΔBIC vs CFG880 / CFG877 | not computed: Part B not run (FROZEN_CRITERIA §3) |
| compact vs large, Sextans, globulars | not run (Part B) |
| K | K1–K6 PASS. These reproduce the scout's A3 numbers, H4's dispersion, H4 ≡ CFG938 S5a, and CFG888 S1/S4. The Part B K (CFG880/877 stored statistics) was not run, because Part B is gated |
| MUTATE | c₂ = 0 (no critical quadratic). K3, K4, K6, D1c, D1d, D2e and OUTCOME fail. The v3 lump gets an edge at 2.2224 L* (1.0004 × πL*/√2) and the outcome flips to A-PASS. Exit 1 |
| lump mass | not addressed. Supply is open (CFG823/930/959, E3, P1) |

## Input ledger

| input | class | source |
|---|---|---|
| v3 action, γ_L = K L★²/2, J_x (AQUAL μ = x/(1+x)) | FRAMEWORK-NATIVE | THEORY_V3_DRAFT §1; H4 A1 |
| μ_K cap 14.8 h/Mpc (BS24 Eq. 39); growth 411; literal-K BBN 1.84e8 | record bounds (cap = verdict line; others reported) | THEORY_V3_DRAFT lines 48, 75, 79 |
| AeST μ ≤ 1 Mpc⁻¹ | record bound (H2 C3) | H2 README line 64 |
| L* values 21.68 / 22.85, 28.85 / 29.12 pc | FITTED (globular floor, D10 / E4 native) | D10 JSON |
| L* 90 pc, soft edge 2.04 / 2.14 kpc | record window edges | THEORY_V3_DRAFT line 44; 10-21 draft line 47 |
| CFG877 M_cl, r_t; CFG870 r_c | record empirical clump (SURVEY-CALIBRATION via LVD, Υ_V = 2) | their JSONs |
| x_cl = 0.1975 | by CFG877's construction (≈ 16/81) | derived here |
| h = 0.674 (bracket 0.55–0.73) | unit conversion of μ_K only (ΛCDM-PROCESSED convention, ±25 % at most) | declared |
| CFG938 BBN ratios | record | CFG938 JSON S2 |
| ΛCDM inputs | none in any verdict | |
| STANDARD-MOND machinery | none | |

## What this does not show

- D2 is linear and WKB with a frozen M_θ, so the v3 lump shape is exact only in that limit. D1 (μ_K = 0) is exact and
  nonlinear, but spherical.
- It does not test v3 with μ_K above the cap as a theory, i.e. the halo double counting the record flags.
- It does not prove that no future formulation can give the free population the stiffness. §5 of `DERIVATION.md` lists what
  one would need: a local (γ/2)ρ_f² on the untethered population, a written switch, and avoiding R2's failure.
- No data were fitted.

## Run

```
OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG965_stiffness_lump/cfg965.py                   # exit 0
CFG965_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG965_stiffness_lump/cfg965.py   # exit 1
```
