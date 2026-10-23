# Z1_successor_design — the minimal successor: requirements, families, one design, a frozen test plan

## Verdict: DESIGN PROPOSED (CONDITIONAL)

The design **Z★ = v3s-OC** meets the frozen acceptance lines D1–D6 (`FROZEN_CRITERIA.md` §1c). It is a design, not a
theory: its ownership rule has no action. It keeps v3s's verified passes, reaches the U1 rows by a stated mechanism, has
one fewer free constant than v3, and still fails the cluster cores and the Milky Way disc and slope.
κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour
the framework.

## 1. The requirements matrix (`REQUIREMENTS_MATRIX.md`)

- **24 rows**, each with its number and `file:line` evidence in a verified lane (the coordinator's 13 plus strong field,
  inner/red and outer lensing, cosmic shear, isolated LG dwarfs, MeerKAT, groups, and the v3s health rows).
- **9 tensions.** The hub is **U1**: the record's cold medium is held by the law's own field (α ≡ 1), so it is the
  phantom, weighs nothing in a host and cannot self-gravitate (T3, D-T, D-T′). The μ_K pincer (gap 2.4e3–5.7e4), BBN vs
  growth, and the closure of every local selector (Theorems G and S, μ-pincer, J1, V1) all feed it. Clusters, the third
  peak and the MW disc are generic to the MOND class.

## 2. The families (`FAMILY_SCORES.md`), best first

1. **v3s**: the best-verified chassis (GW at c, 3-DOF algebra, well-posed saddles, screening, the law); fails every
   cold-sector row.
2. **Codex's P-medium**: the only live nonlinear self-binding mechanism; its own table needs ℓ ≥ 134 kpc for the law and
   ℓ ≤ 0.44 kpc for growth; 3D binding not certified (W1). Lane Y1 is scoring it.
3. **Dipolar (Blanchet–Le Tiec)**: new here (K1–K3, sympy): its printed NR equations come from a Lagrangian with an
   indefinite kinetic matrix (det −1); with y = x + ξ the gravitating points are **geodesic dust** and ξ is a ghost, so its
   "CDM-like growth" is CDM; W₂ = 4πG keeps the anchor at rest only while 4πG|Π| ≪ a₀, and at recombination (x ≈ 11–14)
   the anchor is pushed at x times the field. Unscreened; carries the EFE. BLT's Λ–a₀ relation maps to κ = Z/(4πα):
   α ≈ 0.8 gives κ = 0.576; κ = ½ needs α = 0.921.
4. **v4 (AeST + γ_L)**: ill-posed where the aether twists (I1); FRW runaway (C7); no cluster supply (H2).
5. **TeVeS-type / BIMOND**: original TeVeS in the GW170817-excluded class (prov); c_T = c variants and BIMOND inherit the
   unscreened and MOND-class failures.
6. **Environment-dependent phase with a local selector**: closed by the record's theorems.
- Reference only: Khoury superfluid (a particle), ΛCDM (a particle).

## 3. The design (`DESIGN.md`)

v3s (law, screening, GW at c) with the BS K(Q) dust and μ_K removed; the cold medium is one mimetic dust;
**R1 capacity**: held density 0 ≤ D·P ≤ ρ_d, so the phantom is real captured dust and total mass is baryons + dust;
**R2 ownership**: dust is held in the free-fall frame of the smallest bound system that owns it; unowned dust is free.

- **Constants: 3 continuous (κ, L★, cold abundance) vs v3's 4 — μ_K removed.** Two rules added with zero constants;
  R2 and R1's dynamics are NON-VARIATIONAL (named in `DESIGN.md` §2). Z★ escapes D-T, D-T′, G and S only through R2.
- **U1 mechanism (sympy):** an owned unit falls at exactly g_host (v3: g·M_b/(M_b+M_h)) and has no EFE (K6); held dust
  released when baryons leave is at rest and bound (E < 0 at all 30 grid points, K7); the hosted excess is then
  Δlog g ≥ ½ log(M_b,orig/M_b,now) (K9). X1's classes need lost fractions 0.62–0.95; the Coma UDGs, with CFG948's field
  HI-UDG gas fraction 0.81, give ≥ +0.361 dex against the observed +0.33 dex.
- **Static galaxy limit (K4):** exactly v3s's AQUAL leaf equation (planar and spherical residual 0).
- **Linear kernel (K8):** unowned mimetic dust, s(k) = 1 for every k, δ ∝ a (v3 at μ_K = 0: s = 0). BBN has no stiff
  partner.
- **Clusters stay red.** Supply radius r_s = r_M √(f_s(f_s+1)) = 5.84 r_M; crossing mass M_× = 2.7e13 / 4.7e13 M☉
  (200ρ_c) to 3.8e14 / 6.8e14 M☉ (18π²ρ̄_m); total/law ≤ 1.04 at X2's tercile medians, so no core excess. Beyond r_s the
  law is truncated (design/law at 2 Mpc 0.24 / 0.44 / 0.68), the direction of X2's OUTER 0.50 / 0.78 / 1.40.

## 4. The first three decisive tests (`TEST_PLAN.md`, frozen)

1. **Z-T1** hosted retention on X1's per-system table with P1's MDF supply and matched isolated-dwarf gas fractions
   (minutes). A FAIL kills the U1 mechanism.
2. **Z-T2** the capacity-truncated law on X2's cluster terciles (minutes). Forecast: MID fails, OUTER moves toward data.
3. **Z-T3** well-posedness of the two-sided obstacle on X3's slab and symbol (minutes). A FAIL kills R1.

## 5. Checks

`OMP_NUM_THREADS=1 nice -n 15 python3 z1_successor_design.py` → **10/10 PASS**, exit 0, 0.6 s, 65 MB RSS.
`Z1_MUTATE=1 …` (global foliation + flipped BLT sign) → **8/10, K1 and K6 FAIL as required**, exit 1.
Outputs: `z1_successor_design.out`, `z1_successor_design_results.json`, and the `_MUTATE` pair.

## 6. What this does not show

- No data were scored. Every Z★ number is a forecast or an identity; the tests in `TEST_PLAN.md` decide.
- R2 (ownership) has no action, and R1's held/free exchange has no action. Neither is built here.
- The owned supply per galaxy is history-dependent; with the cosmic ratio, SPARC dwarfs would be truncated inside their
  last measured radius (a 1e8 M☉ dwarf at 2.3 kpc), so Z★ needs f_own ≥ R_last/r_M (≈ 10–50). A native collapse model is
  needed (Z-T6, Z-T9).
- The isolated-galaxy outer lensing carries a supply edge, which failed in the record (F2, not robust). Z-T4.
- The MW disc and outer slope fail as in every μ-law theory. The isocurvature row needs an adiabatic origin, not given.
- Literature cells are PROVISIONAL (arXiv abstracts / ar5iv summaries). K1–K3 check BLT's equations as summarised.

## 7. Disclosures

- Not blind: hand estimates (crossing mass, tercile supply radii, member phantoms ≈ 5 % of a cluster's law mass, the
  BLT ghost structure, the retention relation) were made while designing and are listed in `FROZEN_CRITERIA.md` §5.
- Development fixes before the first committed run: `is_zero` now factors square-root radicands (K5's
  √(f_s² + f_s + ¼) = f_s + ½ was missed by plain simplify); K3(b) uses a quartic potential with symbolic coefficients
  instead of an abstract function (a sympy dummy-variable artefact left a spurious residual). No threshold changed.
- Reported diagnostics with no verdict weight, added before the first committed run: design/law enclosed-mass ratios,
  f_req, the Coma UDG side number, M_× at f = 100.
- Y1 (P-medium) had committed only its criteria when this lane read it; its verdicts are not used.

## Files

`FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (committed alone first, 99a3a3c069), `REQUIREMENTS_MATRIX.md`,
`FAMILY_SCORES.md`, `DESIGN.md`, `TEST_PLAN.md`, `z1_successor_design.py` and its outputs.
