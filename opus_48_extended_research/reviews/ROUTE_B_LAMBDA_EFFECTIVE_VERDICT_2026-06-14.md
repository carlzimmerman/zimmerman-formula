# Route B — does a local matter overdensity induce an effective local Λ that the a0↔Λ spine inherits? VERDICT (2026-06-14)

**Grade: CLOSED FALSIFIER — no derived in-window SPARC-safe scale; the load-bearing physics is a CATEGORY ERROR (Λ is the
w=−1 vacuum sector; ρ_matter is w=0), and where a real shift exists (Schwarzschild–de Sitter) it has the RIGHT SIGN but is
~10⁴–10⁵× too small.**
Code: `route_b_lambda_effective.py` (numpy + sympy, SdS Ricci scalar computed symbolically). Builds on the five banked nulls
(ELL_DESITTER_UNRUH_HORIZON, DENSITY_A0_RDE_CROSSOVER, DENSITY_A0_ELL_1MPC, the r_DE level-set, the +0.052±0.043 SPARC
environment coupling). Quarantine held: a0/Z never asserted derived; every candidate flagged derived-vs-tuned.

## The question, sharpened to the foundation
a0 = c²√(Λ/32π) ties a0 to the **vacuum** density ρ_DE = Λc²/8πG. Route B asks whether a local matter overdensity induces an
**effective local Λ_eff = Λ + f(ρ_local)** that the a0↔Λ relation converts into a shifted a0_local — and whether the
foundation picks a scale that boosts cluster cores (~300–450 kpc) WITHOUT touching galaxy disks. Since a0 ∝ √Λ_eff,
**a0_local/a0 = √(Λ_eff/Λ)**: the cluster boost (~2–25×) needs Λ_eff/Λ ≈ 4–625; SPARC-safe needs Λ_eff/Λ ≈ 1 (within a few %)
in galaxy disks.

**The single fact that governs every route (and dooms the density-driven ones):** galaxy-disk matter density is
**~10⁶ ρ_DE** (0.1 M⊙/pc³ → 1.14×10⁶ ρ_DE), while cluster-core matter is only **~10³ ρ_DE** (≈1460 ρ_DE near core, 730 ρ_DE
at R500). **Disk matter is ~10³× DENSER than cluster-core matter.** So any Λ_eff that scales with local ρ_matter boosts
galaxy disks MORE than cluster cores — the exact wrong sign for the cluster goal, and fatal to SPARC.

## (i) Trace / backreaction Λ_eff = Λ + f(ρ_matter) — DEAD (wrong sign, wrong scale, category error)
Moving the matter trace to the LHS gives δΛ ~ 2πGρ/c² ⟹ **Λ_eff/Λ = 1 + ρ_matter/(4 ρ_DE)** (linear in local matter
density). Numbers: disk → Λ_eff/Λ ≈ 2.9×10⁵ (a0 boost **~530×**, annihilates SPARC); cluster core → ≈366 (boost ~19×);
cluster R500 → ≈183 (boost ~14×). It boosts the **dense disk ~30× MORE than the cluster core** — wrong sign — and is the
local/clumpy reading already killed by the framework's own SPARC environment test (d log a0/d log(1+δ) = +0.052±0.043 vs the
+0.5 this predicts, 10.5σ). **Category error:** moving T_matter to the LHS does not create a vacuum term; matter (dust, w=0)
is not Lorentz-invariant and cannot masquerade as a cosmological constant (w=−1).

## (ii) Emergent-gravity readings (CKN/holographic-DE, Padmanabhan, Verlinde) — ALL FAIL
- **CKN UV-IR bound** ρ_Λ ~ M_p²/L² (Cohen–Kaplan–Nelson; verified scaling Λ²L ≲ M_p, ρ_Λ ∝ 1/L²): a0_local/a0 = L_cosmo/L_local
  with L_cosmo = c/H_Λ ≈ 5340 Mpc. The boost is the **ratio of IR scales**, and the cluster window needs L_local ≈ 210–4100 Mpc
  (still Gpc-ish, NOT the cluster core).
  - **L_local = local apparent horizon c/H_local** (ρ-driven): this is the banked ELL_DESITTER null re-derived from the CKN
    side — disk (point density) → L≈5 Mpc, boost ~1070× (breaks SPARC); cluster → ~30×. Smoothing self-consistently washes
    the disk to ρ_DE (Gpc, no boost) — same ell circularity, **not escaped by relabeling as a UV-IR cutoff.**
  - **L_local = system size** (the literal HDE IR cutoff): a0 ∝ 1/L_system, so the SMALLER galaxy (15 kpc) gets boost
    ~3.6×10⁵ and the cluster (0.4 Mpc) only ~1.3×10⁴ — **wrong sign and absurdly large.**
- **Padmanabhan holographic equipartition** gives a0 ~ cH₀ at the **Hubble radius** (N_bulk=N_surf) — a GLOBAL/cosmological
  balance producing the a0~cH₀ scale, with NO local-density dependence.
- **Verlinde 2017 local entropy** is the emergent-DM *displacement* response (apparent dark mass M_D ~ √(M a0 r²/G)) at
  **fixed a0** — it does not shift Λ. None of the three make a genuine Λ_eff(ρ_local).

## (iii) Schwarzschild–de Sitter (SdS) — the SERIOUS route: RIGHT SIGN, but ~10⁴–10⁵× too small
SdS f(r) = 1 − 2GM/c²r − (Λ/3)r² is the **exact** vacuum metric for a mass M in a Λ-vacuum, with two horizons. Reading the
"effective Λ off the cosmological horizon" Λ_eff = 3/r_c²: perturbatively (sympy) the cosmological horizon **shrinks** with
enclosed mass, δr_c = −μ/2 (μ=2GM/c²), giving
> **Λ_eff/Λ = 1 + (2GM/c²)·√(Λ/3) = 1 + (2GM/c²)/r_c0  (positive — RIGHT SIGN).**

This is the **one route with the correct sign**: it scales with **total enclosed mass** (not local density), so it boosts
massive clusters slightly MORE than galaxies — exactly the differential the cluster goal wants. **But the magnitude is
fatal:** the shift is (gravitational radius of enclosed mass)/(Hubble radius), and r_c0 ≈ 5340 Mpc is in the denominator.
Even a 10¹⁵ M⊙ cluster has 2GM/c² ≈ 0.096 Mpc, so Λ_eff/Λ − 1 ≈ 2.2×10⁻⁵ ⟹ **a0 boost ≈ 1.00001×.** Need 2–25×; get
1.00001×. The cosmological horizon barely notices a cluster — off by ~10⁴–10⁵.

## The category result (decisive, sympy-verified)
The SdS **Ricci scalar in the vacuum region is R = 4Λ EVERYWHERE, independent of M** (Schwarzschild is Ricci-flat; the mass
adds only a Ricci-flat Weyl/tidal piece). So the **local effective Λ read off the curvature around a mass is the unchanged
background Λ.** Λ is the w=−1 Lorentz-invariant vacuum trace; matter (w=0) lives in the matter Einstein source and the
Weyl/tidal sector, NOT in the vacuum Λ term. Treating a matter overdensity as "extra local Λ" **double-counts the matter**:
its gravity is already g_bar inside the a0 formula's argument; re-injecting it as a shifted a0 is the category error.
**Λ_eff(ρ_matter) is not a real derived effect — it is a category error**, with the one legitimate exception (SdS
cosmological-horizon back-reaction) being real, right-signed, and ~10⁵× too weak.

## Verdict — both ways
**CLOSED FALSIFIER for Route B.** No emergent-Λ_eff(ρ_local) mechanism delivers a derived, in-window, SPARC-safe scale.
- The density-driven readings (trace backreaction; CKN-with-local-Hubble; system-size cutoff) all have the **wrong sign**
  (disk denser/smaller than cluster ⟹ boosts galaxies more) and break SPARC by 10³–10⁵× — they are the banked clumpy/ell
  nulls reappearing under new labels.
- The mass-driven SdS route is the **honest near-miss**: it has the **right sign** (total-mass-scaling ⟹ clusters > galaxies)
  and is genuinely DERIVED from the exact metric with zero tuned input — but its magnitude is the ratio
  (enclosed grav radius)/(Hubble radius) ≈ 10⁻⁵, ~10⁴–10⁵× too small to touch the cluster deficit. Credited as real and
  right-signed; reported as empirically inert.
- The category analysis (R=4Λ in vacuum, sympy) shows **why** there is no large effect: Λ is the vacuum sector; ρ_matter is
  not vacuum. The framework's own foundation does NOT license a local-ρ_matter shift of the vacuum Λ that a0 reads.

**This converges with the spine `THE_A0_LAMBDA_BRIDGE.md`:** the faithful reading is a0 ↔ Λ (the vacuum/event-horizon
constant), and that reading is precisely the one that gives NO local-matter Λ_eff. Route B confirms, from the Λ_eff side,
that the a0↔Λ identity is a **vacuum** lock — robust against local matter — which is exactly why the density-a0 cluster
escape needs an external smoothing scale and cannot get one from the vacuum side.

**No manufactured cure** (the SdS right-sign near-miss is reported as ~10⁵× too small, not dressed up). **No high-priest
dismissal** (the SdS shift is credited as real, derived, and correctly signed; the CKN/Zel'dovich local-Λ literature is
engaged on the merits). The honest closing line: **the foundation's a0↔Λ is a vacuum identity; a local matter overdensity
does not move the vacuum Λ that a0 reads (R=4Λ), so Route B opens no derived in-window scale — the one real effect (SdS
horizon back-reaction) is right-signed but cosmologically dilute.** Bank it as closed.

*Sources: Cohen–Kaplan–Nelson 1999 (UV-IR/CKN bound); Padmanabhan holographic equipartition (0912.3165, 1207.0505);
Verlinde 2017 SciPost 2,016; Schwarzschild–de Sitter exact metric; arXiv:2501.18144 (CKN/HDE scaling Λ²L≲M_p, ρ_Λ∝1/L²);
companion nulls ELL_DESITTER_UNRUH_HORIZON_VERDICT, DENSITY_A0_RDE_CROSSOVER_VERDICT, DENSITY_A0_ELL_1MPC_VERDICT;
spine THE_A0_LAMBDA_BRIDGE.md.*
