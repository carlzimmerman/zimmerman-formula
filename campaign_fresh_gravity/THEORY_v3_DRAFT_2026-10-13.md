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

**⚠️ Correction to (1)–(2) (astra CE-FM-010, sol61_push/cold_final_mile_2026_10_13/ACTION_CORRECTION.txt):** pairing the completed-square term with the FULL saturating potential W_full double-counts the critical quadratic; the literal Euler–Lagrange equation then gives g_N = W′_full and ν → 2, losing the deep law. The correct (equivalent, no new parameter) forms are either the expanded action with −W_full, or the completed square with the REMAINDER W_rem(u) = W_full(u) − u²/(8πG). CFG722's selector already uses the residual R = u²/(a₀ − u), so its results stand. Read (1) below with W → W_rem.

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
- **⚠️ Correction (CFG659, e2704e330):** this holds for a SUDDEN start. Real halos assemble over ≳ 10⁹ dynamical units — far slower than the local P-wave gap — so the response is evanescent: P follows the baryons ADIABATICALLY and the radiated fraction is ≤ 1e-195 even at the most favourable corner (CFG696's own equation: a ramped source radiates ∝ T^-2.2). Settling is therefore an adiabatic, reversible exchange with the baryons, not radiation; this bears on CFG696's energy ledger and on CFG630's "settling feeds dark energy" reading (open). P leaves no visible signature in matter or light (all channels below threshold; light would need a new coupling).

**⚠️ Correction to (6) (CFG722, b7e5958b7):** the bound charge ∇·P is a field quantity with ZERO net mass (interior +23.9 M_b, edge shell −23.9 M_b) and no inertia of its own; it follows the instantaneous field of ALL baryons (in the Bullet: the stripped gas — the excluded instant-response class). So it CANNOT be the cold mass CFG624 requires. Together with CFG624 this forces a COLLISIONLESS CARRIER — plainly, a new particle species with a free mass (in tension with the programme's no-particle rule; open). If the carrier IS the polarizable medium (∇·P = ρ_c − ρ̄_c), the action yields a conservative tether force whose unique static minimum is exactly the law's profile (selector C_sel = −∇_v·(a_T f), a_T = W′(u)P̂), with capacity Σ̄_c ≤ a₀/πG and EXPORT-only exchange; it does not distinguish hot from condensed gas (A5 obstructed) and pushes overflow to the basin edge, not the core (contradicts the overflow hypothesis unless a second, untethered population exists).
**(6) Cold energy (bound charge).** ρ_c = ρ_ph = (1/4πG) ∇·[(ν_s − 1) g_N] inside the system's basin. Spherically,
M_c(r) = (ν_s − 1) M_b(r), capped by the supply.

**(7) Supply and finite edge.** M_c,supply = 5.364 × M_b,catchment (own host only, CFG647). Finite supply forces an outer
edge: r ≤ (1 + S/M_d) √(G M_d/a₀) (Lean supply_radius_bound).

**(8) Overflow (hypothesis, CFG720 pending).** Where the supply exceeds what the profile holds (massive systems), the excess
stays collisionless and falls into the core.

**(9) Early universe.** Before any bound system exists there is no basin and no settling. Cold energy is ordinary cold
matter and the primary CMB is untouched (CFG649).

## 3b. Two kinds of cold energy (2026-10-13 synthesis; CFG722, CFG723, CFG724, CFG725)

Evidence-first chain:
1. The P bound charge has zero net mass, so it cannot be the cold mass CFG624 requires (CFG722).
2. Only a carrier with real rest mass meets the data (CFG723).
3. The viable carrier is a cold collisionless **medium whose displacement IS P** (∂_tP = −j ⇒ ∇·P = ρ − ρ̄), possibly with its mass value set by ρ_DE (CFG723 B/D5).
4. Coupled that way, the action gives a tether whose unique static minimum is the law, with a **capacity Σ̄ ≤ a₀/πG** (214 / 258 M☉/pc²) (CFG722).
5. Galaxies sit below the capacity (SPARC deep-regime median ≈ 0.3 of it); massive cluster cores exceed it by 3.6–4.8× (Bullet) (CFG724).

**⚠️ Update (CFG721):** the law's own tethered phantom never reaches the cap a₀/πG, so the capacity does not bind anywhere that matters; the cluster-core excess is mass beyond the law, and supply overflow (H-OF / H-OF2) FAILS to supply it (Bullet main ≤ 0.79, sub ≤ 0.11; early types Z 3.7–3.8). The free component below remains a data-required hypothesis with NO derived origin yet (astra's escape channel CE-FM-026/027 is the live candidate).

**So cold energy comes in two kinds:**
- **Tethered**: in the law's shape, capped at a₀/πG. It dominates galaxies and gives the RAR.
- **Free**: supply the tether cannot hold. It is collisionless and follows the total potential, pooling in the cores of massive systems. It is the candidate for the early-type, group and cluster-core excess (CFG669/652/687). Testing: the CFG721 two-population variant H-OF2.

**New, framework-specific predictions:**

| # | prediction | test | status |
|---|---|---|---|
| P1 | No system's tethered dark surface density exceeds a₀/πG; any excess above it is free cold energy with a NON-law profile | galaxy RAR plus lensing, by surface-density bin | SPARC consistent (CFG724) |
| P2 | Galaxies whose dark Σ exceeds the capacity across the whole curve hold free cold energy and should deviate from the RAR shape in a specific way (flatter inner, non-law outer) | e.g. NGC 3738 (2–4× capacity, CFG725) | to test |
| P3 | Free fraction = 1 − (tether capacity × area)/(dark mass): ~0 in galaxies, ~0.7–0.8 in cluster cores | cluster strong lensing minus baryons minus capacity | Bullet ~0.75–0.8 (CFG724/725) |
| P4 | If the medium is a condensate: σ/m ≈ 0.1–0.8 cm²/g, cored and thermalised free cluster cores with ρ₀,free ≲ 1.4–5.7 × 10⁻³ M☉/pc³ (σ_v 1000 km/s, 10 Gyr) | relaxed-cluster strong lensing plus BCG kinematics | window OPEN-PARTIAL / OPEN (CFG725) |
| P5 | Merger offsets scale ~41–44 kpc per cm²/g at Bullet conditions | merging-cluster lensing–galaxy offsets | Bullet bound ≤ 0.71 (tight side) |
| P6 | Lab and direct detection: null (gravity-only carrier; the law is off at Earth's g) | direct-detection experiments | consistent |

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
