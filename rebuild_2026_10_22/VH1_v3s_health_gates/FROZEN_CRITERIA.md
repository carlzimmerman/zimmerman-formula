# VH1_v3s_health_gates — FROZEN CRITERIA (written and committed before any script or number)

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not theory closed.
Adopts nothing: the 10-24 verdict and the owner's 11-04 FN1 decision (no action selected) stand whatever this finds.

## Question

KT40 and KT42 (branch `codex/kt33-kt42-research-closeout`, commit c1ac71c574) added three physical-health checks that the
fixed-length curvature response (p = 9/8, ℓ = 3 kpc) fails, although it passed the four Milky Way cuts and Cassini Q2:

1. **outward vertical force** in the outer Milky Way disc (dΦ/dz < 0 above the plane at R = 12 kpc, z = 0.3 kpc);
2. **negative scalar binding virial** of fixed Plummer dwarfs in a uniform external field (2,624 / 2,952 configurations
   lower than isolated, 1,805 negative);
3. **planet radial anomaly and monopole precession** against AZ11 / AZ12's lines (all 16 cases fail by 1e4).

v3s is the only form in the record that passes the Solar System (AX1, C6P). It has its own fixed length L★. AX1, V3W
and V3X never applied these three checks to it. Does v3s pass them?

## The theory tested (framework-native, no new posit)

v3s's static weak-field equations as solved in the record (P4's `p4_solver.py`, the D10 stiffened two-field form,
μ(x) = x/(1 + x), μ_K² term dropped as in P4/X5):

    L★ > 0 :  ∇²Φ = 4πGρ + ∇·p(∇χ),   χ = Φ + (L★²/2) ∇·p(∇χ),   p(v) = v/(1 + |v|/a₀)
    L★ = 0 :  ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ                                   (AQUAL)

**Primary L★ = 21.7 pc (canonical) / 22.9 pc (alt)**, the record's lower bounds (D10). This is the smallest screening
and the most AQUAL-like for galaxies; for the planets it gives the largest hedgehog. L★ = 0 (AQUAL) is reported beside
it, not graded.

## Inputs (read-only, from the record)

- Solver: `rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_solver.py`, imported read-only; MW machinery via
  `rebuild_2026_10_22/X5_mw_joint_baryons/x5_lib.py` (`load_p4`, `Family`), imported read-only, no bytecode written.
- MW baryons: P4's four models (B1 McMillan17, B2, B2b, B3) and X5's passing cells (7 canonical, 4 alt; X5 README
  table) — the light-disc corner that is v3s's best Milky Way.
- Dwarfs: KT40's four objects (Draco, Sculptor, Leo II, Fornax) from `real_research/data/dsph/mcconnachie2012_dsph.csv`
  with KT39's recipe: Plummer a = R2 (half-light), L from M_V, M = Υ L + 1.33 M_HI, Υ on 41 points in [1, 3].
  KT40's auxiliary Newtonian external fields η = e/a₀ ∈ {0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3}, mapped to the
  physical uniform field v3s sees: g_e/a₀ = η ν(η), ν(y) = 1/2 + √(1/4 + 1/y) (η = 0 is isolated).
- Planets: `rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json` PLANETS (a, EPM, INPOP, dg_tight), AZ12's
  eccentricities (Mercury .206, Venus .007, Earth .017, Mars .093, Jupiter .048, Saturn .054), GM☉ 1.32712440018e20.
  AZ11's σ = dg_tight × max(EPM, INPOP)/min(EPM, INPOP); AZ12's σ = max(EPM, INPOP) mas/yr. The v3s planet anomaly is
  C6/C6P's carried result: inside L★ the extra field is the hedgehog, a constant inward GM☉/L★² (C6P: agrees with
  C6's Route F monopole to four digits). It is not re-solved here.

## Methods

**G1 (Milky Way force sign).** One isolated solve per model and footing on P4's MW grid (half grid, equatorial
symmetry). At every cell centre with R ≤ 25 kpc, 0.02 ≤ z ≤ 5 kpc and r ≥ 0.1 kpc, compute ∂Φ/∂z of the internal
potential (positive = toward the plane, the record's sign convention). A cell is **outward** if
∂Φ/∂z < −1e-3 |∇Φ| at that cell. Also interpolate ∂Φ/∂z at (12, 0.3) and (R₀, 1.1) kpc.

**G2 (dwarf virial).** One full-θ solve (axis along the external field) per object, Υ, η, footing. With the internal
potential φ (the uniform field removed, as P4), the scalar binding virial is

    W = ∫ ρ r ∂φ/∂r dV,    σ²_W = W/(3M)  [(km/s)²],

positive for attraction. The uniform field contributes ∫ρ g_e z dV = 0 for a centred profile. Grid A: P4's
`sphere_grid`-style log edges, 16 per decade from 1e-3 a to `r_out_for(M, g_e, 10a)`, Nt = 32 full. Grid B (ladder): 24
per decade, Nt = 48, at Υ ∈ {1, 2, 3}.

**G3 (planets).** Anomaly A = −GM☉/L★² (inward, constant). Radial Z = |A|/σ_AZ11. Precession by AZ12's own first-order
eccentric-anomaly average (its `rate` formula re-implemented here, not imported: the astra lane is read-only), Z =
|rate|/σ_AZ12. All six planets; Mars and Saturn are KT42's two.

## Verdict lines (frozen)

- **G1 PASS** if, on every graded model (P4's four and X5's passing cells) and both footings, at L★ primary: zero outward
  cells in the region, and ∂Φ/∂z > 0 at (12, 0.3) kpc. **FAIL** if any graded model has an outward cell or the wrong
  sign at (12, 0.3).
- **G2 PASS** if W > 0 in every configuration (4 objects × 41 Υ × 9 η × 2 footings = 2,952) at L★ primary, and the
  grid-B ladder agrees in sign everywhere it is run. **FAIL** if any configuration has W ≤ 0 with the ladder agreeing.
  **NO VERDICT** if the ladder disagrees in sign.
- **G3 PASS** if every planet has radial Z ≤ 2 and precession Z ≤ 2 on both footings at L★ primary. FAIL otherwise.
- **Overall: PASS** if G1, G2 and G3 all pass on both footings; **FAIL** if any fails; else **UNDECIDED**.

Reported, not graded: L★ = 0 (AQUAL) twins for G1 and for G2 at Υ ∈ {1, 2, 3}; G3 at L★ = 24, 50, 90 pc and against
C6's tighter dg_tight; σ_W against the observed σ★ (|σ − obs| ≤ 2 err) as context only (v3s's hosted dwarfs already
FAIL in the 10-24 verdict through U1/X1, which this lane does not revisit); net self-force on the dwarfs.

## Checks (the lane is NOT EVALUABLE if any fails; each prints PASS/FAIL, exit non-zero on failure)

- **K1 Newtonian virial.** P4's Newton solve of a Plummer sphere gives σ²_W = πGM/(32a) to ≤ 1 % (grid A).
- **K2 deep-MOND virial.** An isolated AQUAL (L★ = 0) Plummer sphere with GM/a² ≤ 1e-3 a₀ gives Milgrom's exact
  σ²_W = (2/9)√(GMa₀) to ≤ 2 %.
- **K3 momentum.** In every external-field solve, |∫ρ ∇φ dV| ≤ 2e-2 × ∫ρ |∇φ| dV.
- **K4 P4 reproduction.** B1 McMillan17, canonical, L★ = 0: K_z(R₀, 1.1) = 92.3 ± 0.5 (P4 T4).
- **K5 X5 reproduction.** X5's best canonical cell (Σ_b 40.3, M_bb 1.64e10, R_d 1.933) at L★ = 24 pc: K_z(R₀) =
  76.66 ± 0.5, v_c(R₀) = 229.71 ± 0.5.
- **K6 G3 oracles.** AZ12's three orbit oracles (constant → −√(1−e²), r → −1.5√(1−e²), 1/r² → 0) to ≤ 1e-10.
- **K7 convergence.** Every solve's scaled residual ≤ 1e-8.

## MUTATE twin (must bite)

The detectors are graded on the solved fields with the non-Newtonian part reversed and tripled:
Φ_mut = Φ_N − 3(Φ − Φ_N) (G1, B1 McMillan17 and X5 best, per footing) and W_mut = W_N − 3(W − W_N) (G2, every Υ at
η = 0 and 0.01). The twin must give **G1 FAIL** and **G2 FAIL** on both footings. For G3 the twin is A × 1e3, which must
give FAIL at Mars and Saturn. If the twin does not bite, the lane is NOT EVALUABLE.

## Lean (written now)

G3 PASS (C6P already puts Mars at 0.173 of the tight bound at 24 pc). G1 PASS: AQUAL with a monotone μ has no
derivative stress, and the outward force KT40 found came from its Hessian term B. G2 PASS: AQUAL's energy is convex
and has no curvature term, so I expect W to fall with the external field but stay positive. Medium confidence on G2:
I have not seen an AQUAL virial computed in an external field in the record.

## Resources

Single thread (OMP/MKL/OPENBLAS = 1), nice, < 1 GB RSS, wall < 2 h. Another session's lam10 shards are running; this lane
stays small. Outputs: `vh1_gates.json/.out`, `vh1_gates_MUTATE.json/.out`, `vh1_gates_RERUN.json/.out` (byte-identical
rerun of the planets and one MW model).

## Amendments

Any change after this commit is filed below with its date and reason, before the number it touches is seen.
