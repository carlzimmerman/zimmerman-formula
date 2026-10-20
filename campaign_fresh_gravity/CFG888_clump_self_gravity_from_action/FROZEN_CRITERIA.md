# CFG888 FROZEN CRITERIA: does an overfill cold-energy clump's own gravity follow the law? Decided from the record's equations

Date: 2026-10-20. Written and committed ALONE, before any CFG888 script exists and before any CFG888 number is computed. Nothing
below may be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are judged separately and never pooled. Law
g = g_N ν_e(g_N/a0), ν_e(y) = 1/(1 − e^(−√y)) for every isothermal clump calculation; the canonical action's own static kernel
(K W′(u) = u²/(a0 − u), the simple ν) is used only where the action itself is varied (Parts S5, C). Cold energy is real
gravitating mass; no particle species. Framework-native inputs only. Not "theory closed". Nothing here says the data favour the
framework. No constant is added; no knob is scanned. The isothermal (isotropic Maxwellian) clump is INHERITED from CFG871/877/878,
not derived here (flagged assumption).

## 0. Question and what has been seen

**Question.** CFG871 (r_c = (9/2)σ²/a0), CFG872 and CFG877 (M_cl = 81σ⁴/(4 G a0)) and CFG878 Part A assume that an extra, bound
cold-energy clump's OWN gravity follows the law (hypothesis H-LINK; CFG871 README says this is "not settled"). Decide from the
record's equations: (a) the law's source is baryons only, so an overfill clump gravitates Newtonianly (plus whatever P does), or
(b) the law's source includes the clump (self-boost). Then derive the clump for the branch the record implements, and state what
survives of CFG871/877.

**Seen before freezing (read, not run):** CFG541 EQUATIONS.md (E2 gravity, E5 deficit, E7 phantom from the region's own baryons,
open item 5) and cfg541.py's phantom construction; CFG638 README + cfg638.py (∇²Φ = 4πG(ρ_b + ρ_c), ∇²ψ = 4πG(ρ_ph − ρ_c),
"overfill not handled"); THEORY_CANONICAL 2026-10-14 (S2 action with matter term −ρ_bΦ; S3 "displacement is P, ∇·P = ρ − ρ̄";
S4 free cold energy "bound by ordinary gravity"), 2026-10-16, 2026-10-18 (addenda quoting CFG877/878); CFG722 (couplings G and ID;
under ID "the critical quadratic cancels the carrier's self-gravity", the carrier sees ∇Φ_N[ρ_b] plus the residual tether; under G
"the phantom would be sourced by M_b + M_c (double counting)"; Q4 overflow pushed out); CFG723 (B: ∇·P = ρ_c − ρ̄_c); CFG747
(r̈ = −1/r² + m²/r⁴, self-gravity cancelled); CFG776 (surplus tethered cold energy unstable); CFG809 run_system and CFG822
(free mass added outside ν); CFG858 (stiffened BVP; stiffness only screens); CFG870, CFG871, CFG872, CFG877 (code: clump added
Newtonianly to σ², capped at the self-boost M_cl), CFG878 (Part A integrator and its f table), CFG882 (hosts H1–H3; gate).

**Pre-freeze hand values (disclosed; not verdict inputs).** Expected Q1 = baryons only, from reading. Expected ID: excess pushed out
(from CFG722/747). Newtonian King radius r_0 = 3σ/√(4πGρ0) ≈ 125 pc at ρ0 = 0.6, σ = 7.53; Newtonian asymptote M ≈ 2σ²r/G ≈
2.6e4 M_⊙ per pc; deep-law r_M = (9/2)σ²/a0 ≈ 88 pc (canonical); inside ~100 pc the two branches give similar masses (~2e6 M_⊙) at
ρ0 = 0.6, differing beyond ~300 pc; host-confinement threshold for a Newtonian clump 9σ⁴/(G a0) ≈ 2.3e6 M_⊙ (canonical);
stiffness at L* = 24 pc changes the clump's boost at 100 pc by roughly L*²/(2 r r_M) ≈ 3%; the self-boosted clump's field outside
~200 pc is expected to exceed CFG870's extended form.

## 1. Inputs (fixed now, read-only)

- σ per footing = V_x/√2 from `CFG877_finite_cold_clump/cfg877_results.json` (canonical ≈ 7.534, alt ≈ 7.486 km/s); V_x and
  r_c = 104 pc (CFG870); M_cl per footing as CFG877 computes it; CFG877's capped profile M_x(<r) = min(V_x² r³/(G(r² + r_c²)), M_cl).
- Central densities: ρ0 ∈ {0.01, 0.1, 0.6, 3.0} M_⊙/pc³ (CFG878's grid) plus ρ0_870 = 3V_x²/(4πG r_c²) per footing.
- Radii reported: 100, 200, 500 pc (asked) and 1000 pc.
- Hosts (CFG882's illustrative Plummer baryons, not fitted): H1 (1e4 M_⊙, a 30 pc), H2 (3e5, 200 pc), H3 (2e7, 700 pc).
- Constants as CFG878: G 6.674e-11, M_⊙ 1.989e30 kg, pc 3.0857e16 m.
- CFG878 Part A f table from `CFG878_fragment_mass/cfg878_results.json` (for K3 only).
- Largest catchment stock 53.64 M_b (5.364/f_ret at the census floor 0.10; CFG878 audit note), report-only.

## 2. What is computed

**Part S (structural; sympy + one numeric energy check).**
- S1 (ID coupling, canonical S3): one Fourier mode, ρ_b = B cos kx, ρ_c = C cos kx, longitudinal P with ∇·P = ρ_c, Φ from its
  Euler–Lagrange equation. On-shell ⟨L⟩ = ⟨−(Φ′ − KP)²/(2K) − ρ_bΦ⟩. Report its coefficients of C² and BC against the Newtonian
  −V = K(B + C)²/(4k²).
- S2 (coupling G): matter term −(ρ_b + ρ_c)Φ, P independent: the source of (Φ′ − KP)′ from the Φ equation.
- S3 (ID): the same source with P′ = ρ_c substituted.
- S4 (stiffness under ID): for longitudinal P, (γ/2)⟨|∇P|²⟩ = (γ/2)⟨ρ_c²⟩ (1-D mode; 3-D Fourier |k|²|P̂|² = |ρ̂_c|²).
- S5 (ID tether force, spherical static, carrier at rest): E[M] = −∫M g_N^b dr + ∫W(GM/r²) 4πr² dr on [r_in, R_out] with fixed
  M(R_out); first variation F(r) = δE/δM(<r) = −g_N^b + u²/(a0 − u) (F > 0 = outward), u = G M_c(<r)/r². State: host H1–H3
  law-settled carrier (simple ν, the action's kernel) plus CFG877's capped clump per footing. Report min and max F/g_N^b over
  1–1000 pc and max u/a0 (capacity). R5 (report): stiffness push F_s = −2πG L*² ρ_c′ at L* = 24 pc vs the tether push at the
  clump's half-mass radius.

**Part A (branch (a), Newtonian self-gravity), isolated clump.** dlnρ/dlnr = −g r/σ², dM/dlnr = 4πr³ρ, g = G M/r². For each
footing σ and each ρ0: r_0 = 3σ/√(4πGρ0), M(<100/200/500/1000 pc), dlnM/dlnr and M/(2σ²r/G) at 1e4 pc. R1 (report): ratio of
M(<r) at ρ0_870 to CFG870's M_x(<r) (uncapped) and to CFG877's capped M_x(<r) at the four radii.

**Part B (branch (b), self-boost; CONDITIONAL on a coupling the record does not write), isolated clump.** Same ODE with
g = g_N ν_e(g_N/a0), g_N = G M/r². Stop rule as CFG878 (r ≤ 3e5 pc and ρ > 1e-14 ρ0); a tail-corrected total is also reported.
For each footing and ρ0: total M, f = M/[81σ⁴/(4Ga0)], M(<100/200/500/1000 pc), half-mass radius, and the clump's phantom mass
M_dyn − M_true (M_dyn = g r²/G) inside 200 and 1000 pc. R3 (report): that phantom vs 53.64 M_b for M_b ∈ {1e3, 1e4, 1e5, 1e6}.
R4 (report): f at ρ0 = 0.6 with the simple ν instead of ν_e.

**Part C (stiffness at the clump scale; branch (b)).** Fixed source = Part B's clump at ρ0 = 0.6. Solve
u²/(a0 − u) − (L*²/2)(u″ + 2u′/r − 2u/r²) = g_N on [0.05 pc, 3e5 pc], u ∝ r at the centre, u = law at the outer edge (scipy
solve_bvp, as CFG858). Report R_s = (g_N + u)/(g_N + u_law) at 50/100/200/500 pc for L* ∈ {1, 24, 100, 300, 1000} pc. Report-only:
a self-consistent iteration (isothermal in g_N + u_stiff ↔ BVP) at L* = 24 and 100 pc, giving M_tot(L*)/M_deep, or "not converged"
after 40 iterations (|ΔM_tot|/M_tot < 1e-3 = converged).

**Part D (host field; both branches).** Clump at ρ0 = 0.6 in hosts H1–H3: (a) g = g_host,law(r) + G M_cl(<r)/r² (the host's law
field includes its settled cold energy; the clump adds Newtonianly); (b) g = ν_e(g_N/a0) g_N with g_N = G(M_b(<r) + M_cl(<r))/r².
Integrate to 1e5 pc; report M(<100, 200, 500, 1000, 5000, 1e4 pc) and dlnM/dlnr at 1e4 pc. Analytic criterion to be checked:
a Newtonian isothermal in a host deep field is finite iff V_h,∞² = (G M_b a0)^½ > 3σ², i.e. M_b > M_crit = 9σ⁴/(G a0).
R2 (report): the clump's extra acceleration over the host's law, (b) [law(M_b + M_cl) − law(M_b)] vs CFG870's extended form
G M_x/r² and CFG877's capped form, at 200/500/1000/2000 pc.

## 3. Decision rules

**Q1. The law's source.** "BARYONS ONLY (every record formulation)" if all three hold: (i) CFG541 E7 and cfg541.py build ρ_ph
from baryons only; (ii) the canonical action's matter term is −ρ_bΦ and S1/S3 give a P-equation source with zero ρ_c coefficient;
(iii) the record's free-mass code (CFG809 run_system, CFG822, CFG877's σ²) adds cold mass outside ν. "INCLUDES COLD MASS" if a
record formulation other than the H-LINK lanes (CFG871/872/877 mass formula/878 A) puts cold mass inside ν. "MIXED" otherwise.
Each finding is quoted with file:line in the README.

**Q1b. The clump's own gravity, by formulation.** Class A (CFG541/638): NEWTONIAN (E2). Canonical action with ID: "NO SELF-GRAVITY"
if S1's C² coefficient is exactly 0, and "EXCESS PUSHED OUT (no self-bound clump)" if F > 0 at every grid radius in 1–1000 pc for
H1–H3 on both footings (else "LOCALLY BOUND" with the radii). Coupling G: "SELF-BOOST" if S2's source contains K ρ_c.

**Implemented branch.** If Q1 = BARYONS ONLY, any clump that is not expelled (class A with the CFG639 gate, or S4's free population
as the record implements it) gravitates by branch (a); branch (b) is labelled CONDITIONAL (needs a new coupling: free cold energy as
−ρΦ matter in the action).

**Q3. Consequences.**
- CFG871 link r_c = (9/2)σ²/a0: "SURVIVES" iff the implemented branch is (b); otherwise "NOT DERIVED BY THE RECORD'S EQUATIONS",
  replaced by r_0 = 3σ/√(4πGρ0) (Part A values).
- CFG877 M_cl = 81σ⁴/(4Ga0): "SURVIVES" iff the implemented branch is (b); otherwise "NOT DERIVED". The replacement "ADDS A PARAMETER"
  if, in Part D branch (a), each host below M_crit has M(<1e4 pc) > 3 M(<1e3 pc) (its total is then set by an outer truncation, not by
  σ). "HOST CONFINEMENT CRITERION CONFIRMED" if H3 (above M_crit on both footings) has dlnM/dlnr < 0.1 at 1e4 pc and H1, H2 have ≥ 0.5.
- Stiffness: "NEGLIGIBLE AT THE WINDOW'S LOWER EDGE" if R_s(100 pc, L* = 24 pc) ≥ 0.95 on both footings; else "MATTERS AT 24 pc".
- R2 label (report-only inference): "(b) EXTERNAL ≥ CFG870 EXTENDED" if (b)'s extra acceleration ≥ CFG870's extended form at every
  r ≥ 500 pc in H2 and H3 on both footings; read as inheriting CFG876's over-prediction break by dominance (not a new data test).

## 4. K-tests (identities and limits; each PASS/FAIL)

- **K1 Newtonian limit (Part A, canonical σ, ρ0 = 0.6):** (i) ρ/ρ0 vs the Emden series e^(−ψ), ψ = ξ²/6 − ξ⁴/120 + ξ⁶/1890 −
  61ξ⁸/1632960, ξ = r√(4πGρ0)/σ, at ξ = 0.5 and 1: |Δ| ≤ 1e-4; (ii) dlnM/dlnr at 1e4 r_s within 0.05 of 1 (M ∝ r);
  (iii) |M/(2σ²r/G) − 1| ≤ 0.05 at 1e4 r_s.
- **K2 deep limit (Part B):** f(ρ0 = 0.01) within 6% of 1 on both footings, and every f on the ρ0 grid in [0.74, 0.96].
- **K3 cross-code:** Part B at σ = 7.53 reproduces CFG878's eight f values (4 ρ0 × 2 footings) within 1%.
- **K4 sympy:** S1 (C² coefficient 0; BC coefficient = Newtonian), S2 (source K(ρ_b + ρ_c)), S3 (source Kρ_b), S4 (identity):
  residuals exactly 0.
- **K5 ID energy:** (i) law state |F|/g_N^b ≤ 1e-9 at every radius 1–1e4 pc, H1–H3, both footings; (ii) centred finite-difference
  dE/dε vs ∫F δM dr for a compact δM (zero at both ends): relative difference ≤ 1e-4.
- **K6 stiffness solver:** L* = 1 pc gives R_s(100 pc) within 1e-3 of 1 on both footings.

## 5. MUTATE (env CFG888_MUTATE=1; outputs cfg888_MUTATE.out, cfg888_results_MUTATE.json)

Swap the branch everywhere: M1 self-boost forced ON in Part A → K1 must FAIL; M2 self-boost forced OFF in Part B → K2 must FAIL;
M3 the critical quadratic −K|P|²/2 dropped from S1 → K4-S1 must FAIL (self-gravity returns); M4 the carrier's Newtonian self-energy
½∫ρ_cΦ_c added to the ID energy → K5(i) must FAIL. MUTATE exits 1 iff all four bite (record convention, as CFG638/CFG882), else 0.
The normal run exits 0 iff every K passes.

## 6. Compute and scope

One process, OMP_NUM_THREADS=1, nice 10, < 10 min, < 2 GB. Nothing downloaded. Only this lane's directory is written. LEDGER and
THEORY_CANONICAL files are not edited (a ledger row is returned to the orchestrator).

κ = ½ fitted; cold energy mass required; not theory closed.
