# Theory v3 (DRAFT, 2026-10-13): one action, settled by radiation

Status: **draft**. It integrates Theory v2 (THEORY_v2_CANDIDATE_2026-10-12.md, with its 2026-10-13 reconciliation block) and the
one-action construction from the parallel Lean chat (CFG691, CFG693–696, scored here in CFG658). Pending decisive tests:
CFG650 T12 / T1x (raw KiDS, 1024³), CFG720 (supply overflow), ALMA (2026-11-06, 11-28) and Gaia DR4 (2026-12-02).
κ = ½ is FITTED. The cold energy's amount is an input. This is not "theory closed". Every claim cites a committed lane.

## 1. The statement

Empty space has a polarizable response P. Matter makes it lean; the lean saturates at the acceleration scale
a₀ = κ c √(G ρ_DE), which dark energy sets. That saturating lean is what produces the galaxy law. When the lean is out of
equilibrium it radiates its excess as P-waves and settles. What it leaves bound around each system is the **cold energy**,
in exactly the law's profile, drawn from that system's own supply. Supply the profile cannot hold stays as ordinary cold
matter (hypothesis, CFG720).

## 2. Inputs (honest list)

| input | value | status |
|---|---|---|
| κ | ½ (footings a₀ = 9.36e-11 / 1.13e-10 m s⁻², never pooled) | FITTED (CFG493: 0.42 ± 0.10) |
| ρ_DE | measured | input; a₀ tracks it, a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)) (CFG549) |
| Ω_c/Ω_b | 5.364 (CMB pair; native 5.376; BBN bracket 5.48) | measured, not derived (CFG642: no formula beats chance) |
| γ, the field stiffness | sets L* = 5.75 pc (CFG691) | hierarchy rule; not derived from the action |
| early-universe inputs | CMB A_s, n_s, θ*, BBN ω_b | measured; physics before any bound system (CFG654) |

## 3. The equations

**(1) Action (CFG694).**
$$\mathcal L=-\frac{|\nabla\Phi-4\pi G\,\mathbf P|^2}{8\pi G}-\rho_b\Phi-W(\mathbf P)-\frac{\gamma}{2}|\nabla\mathbf P|^2+\mathcal L_{\rm kin}$$

**(2) Saturating vacuum (CFG695; no new constant).**
$$W'(u)=\frac{u}{1-u/a_0}\quad\Longrightarrow\quad g_N=\frac{g^2}{g+a_0},\qquad \nu_s(y)=\tfrac12+\sqrt{\tfrac14+\tfrac1y},\quad y=g_N/a_0$$
Deep regime: g → √(a₀ g_N), so V_f⁴ = G M_b a₀. Strong regime: g → g_N (Newton, Solar System).

**(3) No external-field effect, by the equivalence principle (CFG693).** Each system reads its own free-fall basin, the
largest closed level surface of the free-fall potential. A uniform external field drops out exactly.

**(4) Stiffness hierarchy (CFG691).** Below L* the response is screened, so a star's own phantom is ≤ 0.035 of its mass
(CFG658), and stars do not become nodes.

**(5) Settling by radiation (CFG696).** P obeys a wave equation with outgoing boundaries:
- any initial state relaxes onto the law's static profile (within 0.06–0.12%);
- energy lost equals P-wave energy radiated (within 0.02–0.2%);
- the bound charge left behind, the **cold energy**, grows from 0 to the static value.

**(6) Cold energy (bound charge).** ρ_c = ρ_ph = (1/4πG) ∇·[(ν_s − 1) g_N] inside the system's basin. Spherically,
M_c(r) = (ν_s − 1) M_b(r), capped by the supply.

**(7) Supply and finite edge.** M_c,supply = 5.364 × M_b,catchment (own host only, CFG647). Finite supply forces an outer
edge: r ≤ (1 + S/M_d) √(G M_d/a₀) (Lean supply_radius_bound).

**(8) Overflow (hypothesis, CFG720 pending).** Where the supply exceeds what the profile holds (massive systems), the excess
stays collisionless and falls into the core.

**(9) Early universe.** Before any bound system exists there is no basin and no settling. Cold energy is ordinary cold
matter and the primary CMB is untouched (CFG649).

## 4. What is established (raw data unless marked)

| test | result | lane |
|---|---|---|
| SPARC rotation curves | 0.1009 / 0.0994 dex with ν_s (ν_mono 0.1003 / 0.0991) | CFG695/658 |
| Wide binaries | basins + stiffness γ̂ 1.016 / 1.020, −0.8σ vs DR3 (Newtonian, as sealed for DR4) | CFG658 |
| Cluster satellites | χ² 0.7 / 0.6 of 5 | CFG658 |
| Cluster outer lensing (318 eRASS1 + 8 ACCEPT, raw KiDS) | A_outer 1.01 ± 0.09 / 0.93 ± 0.08: law matches; Newton 7.3× short | CFG687/686 |
| Primary CMB | untouched (switch off before structure) | CFG649 |
| Settling dynamics | derived by radiation (spherical) | CFG696 |
| No cold energy at all | clusters, Bullet, Local Group, cosmic web all fail, so cold energy's mass is required | CFG624 |

## 5. What fails or is open

| problem | evidence | lead |
|---|---|---|
| **Extra mass in the cores of massive systems** | early types +0.280 ± 0.083 at 50–100 kpc (Ks Z 3.37–3.69); cluster cores ×1.8 inside ~1 Mpc (7σ); groups short | supply overflow (CFG720) |
| **Raw-KiDS cosmic shear** | all-baryon settling EXCLUDED (+68.7); condensed-capped EXCLUDED narrowly (+14.0, absolute p 0.002) | T12 / T1x pending |
| **Hot vs condensed source** | the action has no phase label (P sees all baryons), but restricting to condensed baryons removed 80% of the KiDS tension | needs a derived phase-dependent term, or overflow instead |
| **Cluster mass scaling** | outer shear ∝ M_gas^0.90 vs the law's 0.47 | selection bias, environment or real; open |
| **The switch (B1), Φ = Ψ, the relativistic completion** | not built | CFG678 gates |
| **Inputs** | κ fitted; 5.364 measured; L* a rule | — |

## 6. Dated predictions (frozen)

| prediction | test | date |
|---|---|---|
| raw KiDS-1000 / DES Y3 consistent (relative + absolute) | CFG650 T12 / T1x | 2026-10-13/14 |
| a₀ flat with redshift for w = −1 (a₀ ∝ √ρ_DE), not ∝ H(z) | ALMA U4_27928, GS4_24110; KURVS | 2026-11-06, 11-28 |
| wide binaries exactly Newtonian; MW vertical force | Gaia DR4 (can kill, not confirm against ΛCDM) | 2026-12-02 |
| finite outer edge to every halo (supply-set) | lensing profiles around isolated galaxies | proposed |
| overflow: core excess switches on above a derived mass | early types, groups, clusters | CFG720 |
| no cold-energy spike around black holes | LISA | 2030s |

## 7. What kills it

- T12 and T1x both EXCLUDED on raw KiDS with poor absolute fit.
- a₀ rising with redshift.
- Gaia DR4 wide binaries or MW force outside the sealed values.
- The core excess unexplained by any knob-free rule.
- Any new tuned constant needed to pass the gates above.
