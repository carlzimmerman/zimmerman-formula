# FC_B SCORECARD — Architecture B: constraint-first MMG + mu_10

**Architecture B** = original constraint-first spatially-covariant MMG (2 gravitational
DOF via a second-class MOND constraint on q = -(1/6) ln det gamma; constraint set
{pi_N, C_M, D^2 q, D^2 p}) + frozen kernel mu_10(y) = y/(1+y^10)^(1/10).

**OVERALL: FAIL** — three independent, structural, **kernel-blind** contradictions with
observation, each derived from B's own certified constraint set and each **untouched** by
the mu_exp -> mu_10 swap. FAIL attaches to the frozen chassis, not the program: the
nonrelativistic core (exact AQUAL, derived EFE anisotropy, 2-DOF skeleton) is healthy and
two named within-family repair forks remain OPEN (each a new certification program;
neither, as named, repairs alpha_3).

All gate scripts below were **re-run this session** and reproduce. The kernel-blindness of
the three FAILs for **mu_10 specifically** is certified in
`FC_B_kernel_blindness_cert.py` (this dir) and in the committed gates' own mu_n branches.

---

## HARD-GATE LADDER (eliminate on earliest irreparable structural fail)

| # | Gate | Verdict | Basis | Cause-class (on FAIL) | Evidence (re-run this session) |
|---|------|---------|-------|-----------------------|--------------------------------|
| 1 | Action / constitutive | PASS | DERIVATION | — | `scripts/01_constitutive.py`; C_M = D_i[c^2 mu D^i ln N] |
| 2 | DOF count | PASS* | THEOREM | — | `scripts/05_dof_count.py` -> N_DOF=2 (TT pair); 20-12-4=4 generic branch |
| 3 | Legendre regularity | PASS | COMPUTATION | — | `scripts/09_legendre_check.py`; `scripts/04_rank_and_ellipticity.py` |
| 4 | Ghosts / L_N eigenvalues | PASS | THEOREM | — | eigenvalues lam_perp=mu, lam_par=(y mu)'>0 for y>0, mu_exp AND mu_n |
| 5 | Hyperbolicity / ellipticity | PASS | THEOREM | — | `scripts/13_kernel_swap_ellipticity.py` — mu_10 satisfies every condition |
| 6 | c_T (tensor speed) | PASS | DERIVATION | — | TT sector untouched by scalar constraints (`05_dof_count.py` part E) |
| 7 | k=0 background sector | PASS | DERIVATION | — | `sf54_mmg_k0_zero_mode_sector_2026.py`: Friedmann first-class, DOF continuous |
| 8 | matter-consistency | **FAIL** | DERIVATION | **CONSTRAINT-ARCHITECTURE** | `gate_matter_conservation_derivation.py`: grad_mu T^{mu i} = -rho D^i X at **Newtonian** order |
| 9 | PPN alpha_1, alpha_2, alpha_3 | **FAIL** | DERIVATION | **CONSTRAINT-ARCHITECTURE** | `scripts/ppn_mmg_gate_2026.py`: alpha_1=+4, alpha_3=-1, beta=1, alpha_2=0 |
| 10 | PPN gamma / lensing (Phi,Psi) | **FAIL** | DERIVATION | **CONSTRAINT-ARCHITECTURE** | `gate_lensing_weakfield_derivation.py`: Phi=0, gamma_PPN=0, M24 Δχ²=+403..+498 |
| 11 | FLRW background | PARTIAL | DERIVATION | (a0-blind; Λ by hand) | `sf54`; background a0-blind, no DE from chassis; dust-like E const |
| 12 | FLRW perturbations / IR | OPEN | MODEL-ASSUMPTION | (linear scalar sector empty) | `scripts/14_flrw_perturbations.py`: mu(0)=0 kills linear flux; nonlinear solver needed |

\* **DOF PASS is CONDITIONAL** — see the unverified {D^2 q, H_i} first-class hypothesis below.

The ladder is **eliminated at Gate 8** (first irreparable structural FAIL). Gates 9 and 10
are additional independent FAILs on the same structural cause. Gates 1–7 pass; the healthy
core is genuine but does not survive the relativistic filter.

---

## THE THREE FAILs — all CONSTRAINT-ARCHITECTURE, all kernel-blind for mu_10

Every one traces to the **single defining move** of architecture B: the Hamiltonian
constraint H_perp is **deleted** to buy the 2-DOF count, replaced by the second-class pair
{D^2 q, D^2 p}. That deletion is what removes the equation that would source the missing
physics.

### FAIL 1 — Lensing / gamma_PPN = 0 (Gate 10)
- **Derived twice independently**: `gate_lensing_weakfield_derivation.py` (Phi=0 from
  S_2 = D^2 q = 0) and `ppn_mmg_gate_2026.py` (gamma=0 kernel-independent to <1e-19).
- Light sees **half** the MOND and half the Newtonian potential (deflection ratio
  **0.5000 in all six kernel×footing cells**, incl. mu_10 — Part D of the lensing gate).
- Numbers: Cassini Shapiro **43,479 σ**; solar deflection 0.875" (dead at 1919 precision);
  M24 KiDS lensing RAR **Δχ² = +403..+498** (~20–22 σ); cluster lensing shortfall doubles
  to 3.44–4.16×.
- **Cause-class CONSTRAINT-ARCHITECTURE**: S_2 = D^2 q is the flat Laplacian with **no mu**.
  The deleted H_perp is precisely the GR equation that sourced Phi; MMG has no ij-Einstein
  equation to regenerate it (the MMG analogue of the york ν²-gap, harder: the ij sector is
  UNSOURCED, not under-supplied).
- **Kernel-blindness (mu_10)**: certified — d/dmu[coefficient of q in S_2] = 0.
  `FC_B_kernel_blindness_cert.py` part (1); lensing gate Part D ratio 0.5000 mu_10 cell.

### FAIL 2 — PPN momentum sector alpha_1=+4, alpha_3=-1 (Gate 9)
- `ppn_mmg_gate_2026.py` (34/34 checks): **gamma=0, beta=1, alpha_1=+4, alpha_2=0,
  alpha_3=-1**, kernel-independent to <1e-19, verified across mu_exp, mu_5, mu_10.
- alpha_1=+4 is **4.0e4×** its bound; alpha_3=-1 is **2.5e19×** the pulsar bound
  (momentum non-conservation, sourced by C_M's instantaneous response = the MOND law
  itself); Mercury perihelion at 1/3 GR (716 σ).
- **Cause-class CONSTRAINT-ARCHITECTURE**: alpha_3 = -1 comes from C_M itself and is
  **repair-resistant inside this chassis** — the named S_2' lensing repair does NOT touch it.
- **Kernel-blindness (mu_10)**: certified — the mu-normalization cancels in the
  source ratio (`FC_B_kernel_blindness_cert.py` part 2); numerically <1e-19 with mu_10 run
  explicitly in the committed PPN gate.

### FAIL 3 — Matter non-conservation at NEWTONIAN order (Gate 8)
- `gate_matter_conservation_derivation.py`: r_4 = {pi_N, H_can} = -(H_perp + eps_n) ~
  -rho c², so mu_1 is density-sourced and chi = X solves C_M with source 4πGρ. Matter EOM
  a = -grad(Psi + X); the X-force is **(v/c)^0 = Newtonian order** — Gate 10's original
  O(v²/c²) claim is **FALSIFIED**.
- grad_mu T^{mu i}|_chassis = -rho D^i X != 0. Unrescaled 1 AU anomaly **1.62e11×** the
  Sereno-Jetzer bound. Even the maximally charitable G_bare = G_lab/2 absorption forces
  kappa_bare = 0.6285 (**+1.80/+2.15 σ** vs measured κ) plus an unpriced chi-channel
  Cassini load 0.90/3.88/8.99× (mu_exp/mu_5/mu_10) — **largest for the mu_n family**.
- **Cause-class CONSTRAINT-ARCHITECTURE**: the DELETED Hamiltonian constraint is what
  sources mu_1. Structural, not kernel.
- **Kernel-blindness (mu_10)**: certified — the doubling uses mu only at mu(inf)=1 (shared
  by all three kernels) and the deep-MOND coefficient is 1 for all (`FC_B_kernel_blindness_cert.py`
  part 3). NOTE the chi-channel Cassini load is **worst** for mu_10 (8.99×), so mu_10 makes
  this FAIL *harder*, never softer.

---

## KERNEL-SWAP: what mu_10 DOES and DOES NOT repair

- **DOES**: the EFE-Q2 quadrupole. mu_exp fails Cassini Q2 at 4.6×/6.1× ceiling (canon/alt);
  mu_10 clears it at **0.078×/0.203×** (independently confirmed vs route1B's 0.078 claim).
  This is the ONLY reason mu_n is on the table.
- **DOES NOT**: any of the three structural FAILs above. The mu_n swap is ellipticity-
  preserving (Gate 13, mu_10 PASS) — the Dirac matrix / rank / DOF / preservation gates
  depend on mu only through L_N ellipticity, so they are unchanged — but that same
  invariance means the FAILs sourced by the constraint STRUCTURE (not by mu) are equally
  unchanged.

**Net**: mu_10 trades away the one kernel-repairable liability (Q2) and inherits every
structural one. Verdict unchanged: **FAIL**.

---

## Conditional / open items (do not launder into PASS)

1. **{D^2 q, H_i[xi]} first-class hypothesis — UNVERIFIED.** The PPN attack found an
   uncomputed inhomogeneous piece (1/3) D^2(D·xi) != 0 in the bracket of the MOND
   constraint against the spatial diffeomorphisms. If the E-mode is physical, the 2-DOF
   certificate (Gate 2) itself **collapses**. This gates the survival of the *strongest*
   result. Status: **OPEN** (basis MODEL-ASSUMPTION, not THEOREM). Required computation:
   {D^2 q, H_i} closure.
2. **Two named within-family repair forks — both OPEN, neither repairs alpha_3:**
   - (a) S_2' = D^2(q + ln N): restores gamma_PPN=1 and cluster lensing to the standing ~2×,
     but needs Gates 3/6/7/8 re-derived and the L_N K = d c degeneracy locus characterized;
     leaves alpha_3=-1 and the chi-force untouched.
   - (b) C_M as a secondary constraint from an N-dependent potential: kills the chi-force,
     but then Gate 8's four-multiplier certificate describes a DIFFERENT theory and the DOF
     count must be re-proved.
   Both needed JOINTLY, plus a fix for alpha_1/alpha_3 sourced by C_M itself. Per standing
   rule this is **NOT "no open doors"** — but the doors are new certification programs.
3. **FLRW**: background is **a0-blind** (the a0 = cH_Λ/Z tie is NOT realized dynamically in
   this chassis; Λ by hand); linear scalar sector is **empty** (mu(0)=0 kills the linearized
   flux — no linear Poisson, no G_eff, no growth eq). CMB/growth cannot be confronted at
   linear order. Basis: DERIVATION (empty) / OPEN (nonlinear front).

---

## Reproduction (all re-run this session, all reproduce)

```
cd /Users/carlzimmerman/new_physics/zimmerman-formula/openai_push/final_closure
python3 scripts/05_dof_count.py                    # DOF = 2 (conditional)
python3 scripts/13_kernel_swap_ellipticity.py      # mu_10 ellipticity PASS
python3 scripts/ppn_mmg_gate_2026.py               # alpha_1=+4, alpha_3=-1, gamma=0; mu_10 run
python3 gate_lensing_weakfield_derivation.py       # Phi=0, gamma=0, ratio 0.5000 mu_10; DERIVED-FAIL
python3 gate_matter_conservation_derivation.py     # Newtonian-order non-conservation; DERIVED-FAIL
cd ../../qwen_claude_field_theory/closure_2026
python3 sf54_mmg_k0_zero_mode_sector_2026.py       # k=0 Friedmann first-class
python3 fried_chicken_final/FC_B_kernel_blindness_cert.py   # mu_10 blindness certificate
```

**Citation caveat (from referee):** `ppn_mmg_gate_2026.py` and `gate_dirac_branch_proofs.py`
are the source of the alpha_3/gamma numbers; confirm they are committed (they are present in
the tree under `openai_push/final_closure/scripts/` and `closure_2026/` this session) before
external citation.
