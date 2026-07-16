# LANE K — THE PUBLISHED KERNEL ON PLANETS (the never-done calculation)

**Date:** 2026-07-16. **Compute script:** `laneK_kernel_planets.py` (this dir; numpy+sympy+scipy;
**exit 0, 16/16 checks PASS**; full log `laneK_kernel_planets.out`). **Independent adversarial
re-derivation:** `vfy_kernel_planets.py` (**exit 0, 20/20 PASS**, `vfy_kernel_planets.out`) — see
`VERIFY.md`. Recon banked in `BOUNDS.md` + `laneR_bounds_compute.py`. Cross-suite: `prep_2026/mi_fingerprint/`
RB2 lane reached the same closure fork independently (`rb2_frequency_dependence.out`, exit 0).

Framework: **de Sitter–Unruh MODIFIED INERTIA** (Carl Zimmerman) — NOT standard MOND. Own
interpolation ν(y)=√(1+1/y), μ(x)=(√(1+4x²)−1)/(2x)=K(x²). Both footings carried everywhere:
**canonical a₀ = cH_Λ/Z = 9.362×10⁻¹¹ m/s²** (ρ_DE), **alt a₀ = 1.130×10⁻¹⁰** (ρ_total/cH₀).
Published covariant MI action (Zenodo concept 21253644, v4–v13):
S_matter = −½∫√−g ρ_m [ s uᵘ K(□_u/a₀²) u_μ ], s=−1 (postulate), □_u f = uᵃ∇_a(uᵇ∇_b f);
K Herglotz–Nevanlinna, unique positive measure on the cut, ‖K‖≤1, causal-retarded, v11 sum rule
∫dμ(t)/|t| = K(∞)−K(0) = 1.

---

## 0. The question, and the honest one-line answer

**The landmine.** ν−1 → 1/(2y) means a naive **algebraic circular-orbit reading predicts a constant
sunward anomaly a₀/2 ≈ 4.68×10⁻¹¹ (canon) / 5.65×10⁻¹¹ (alt) m/s² at EVERY planet** — excluded by
ephemerides **1018× (Mercury) to 33 436× (Mars, canon) / 40 357× (alt)**. Blanchet & Novak 2011
(arXiv:1105.5815 p.8) already called this class *"ruled out because not seen from the motion of
planets."* The committed Cassini-evasion work (`cassini_mi_evasion_2026/`) suppressed the **anisotropic
EFE θ(y) response** (true l=2 quadrupole 7.4×10⁻³⁴ s⁻²). It never asked whether the **published
Herglotz kernel K(□_u/a₀²) forces suppression of the ISOTROPIC a₀/2 tail** at planetary (a, ω). That
is this lane.

**The answer (honest, both directions).** Whether the kernel suppresses the tail depends entirely on
**which evaluation of the same published operator** you use, and the two evaluations that carry weight
land on opposite verdicts:

- On the **constitutive / first-moment closure** (Reading A — the evaluation the framework's galactic
  ν-recovery actually uses), the kernel **reproduces the a₀/2 tail at full strength** (verified to <0.1%,
  V5). The kernel does **NOT** suppress it. And — contrary to the natural "it just hides in GM" guess —
  the constant a₀/2 is **NOT absorbable into a GM rescaling** (V2): it is a genuine, observable,
  non-absorbable secular residual (nonzero linear-in-A perihelion precession). So on the closure that
  holds the galactic wins, Door C is **dead at planets by 3.0–4.6 orders**, with **no DC-into-GM rescue**.
- On the **operator / spectral closure** (Reading B — the v4 Borel-functional-calculus definition), a
  **bounded orbit kinematically cannot feed the kernel the positive argument z=+(a/a₀)² the tail lives
  on** (V5, S1). Its u_μ(τ) spans only z ∈ {0, −(γω)²} ≤ 0, where K is a **pure phase, |K|=1** (S2). The
  reactive residual is g_N·(a₀/cω)²/8 ≈ 10⁻²⁸–10⁻²⁵ m/s² — **suppressed 10–13 orders, kinematically
  forced.** BUT the same spectral evaluation (i) **erases the framework's own RAR** (1−ReK ≤ 2×10⁻⁶ at
  every rotation-supported system, S5) and (ii) carries a **universal secular drift a₀/c ≈ 10⁻¹¹/yr** that
  the previously-uncomputed dissipative channel **excludes by ~250–500× (Ġ/G class) and ~47–57σ (LLR)** (S4).

**So the published kernel does NOT uniquely force the a₀/2 suppression at the level that preserves the
framework's phenomenology.** The one kernel-level suppression that is real (operator reading) is a
kinematic selection, not a magnitude rolloff, and it is bundled with RAR-death and an excluded drift.
The only RAR-preserving survivor is the **gated Reading C** (SPEC's off-circular completion) with a
**free ~Myr corner** — a conditional, two-sided-open pass, not a forced suppression. **This is the honest
finding, and it is reported as such — not a failure.**

---

## 1. The structural fact (S1, exact sympy) — why "which reading" is the whole question

On a worldline, □_u = d²/dτ². The v4 operator definition evaluates K by the Borel functional calculus:
K acts on each spectral component of its operand at that component's □_u-eigenvalue. So "what does K see
on an orbit" = "what is the spectrum of the orbit's u_μ(τ)". Exact results (all PASS):

| trajectory | □_u u eigenvalue | scalar uᵘ□_u u_μ |
|---|---|---|
| circular (spatial) | **−(γω)² < 0** (oscillatory) | −\|a\|² |
| circular (time) | **0** (DC; K(0)=0 sector) | — |
| Rindler / hyperbolic | **+α² > 0** (exponential; the dS-Unruh slice) | −α² |

**The positive spectral argument z=+(a/a₀)² — on which the framework's ν-recovery evaluates K — is
reachable ONLY by hyperbolic (e^{+ατ}) worldlines.** A bound orbit spans {0, ±γω} only: the Borel
calculus evaluates K at z=0 and z=−(cω/a₀)² ≤ 0, **on the cut, never on the positive axis**. Any (u·∇)ⁿ
insertion generates only harmonics −(kω)² ≤ 0. The a₀/2 tail lives at z>0; **a bound orbit cannot feed
the kernel that argument. This is kinematics, not tuning.**

## 2. The published Herglotz machinery, re-verified (S2, sympy+scipy)

- **v11 sum rule** ∫dμ/|t| = 1 (to <1e-8). Region-B share = 2/π exactly (cross-checked in rb2).
- **Master deviation identity** 1−K(z) = ∫dμ(t)/(|t|+z) on z>0, exact to <1e-7 (now via a u=√|t|
  substitution stable at all z; the naive t-quad silently lost the slow region-B tail for z≳10⁵). On z>0
  the deviation is a Stieltjes transform of the positive measure: **1−K(x²) → a₀/(2a) at a≫a₀ = the
  landmine term**, *if* z=+(a/a₀)² is fed.
- **Cut boundary values** (the arguments a bound orbit actually feeds), K(−W²+i0), W=cω/a₀:
  **K = (√(4W²−1)+i)/(2W) exactly** ⟹ **|K|²=1** (pure phase), Re K = √(1−1/4W²), **|Im K| = 1/(2W) =
  a₀/(2cω)**. Reactive deviation 1−Re K = 1/(8W²); the phase 1/(2W) is the new secular channel.

Same identities independently PASS in `rb2_frequency_dependence.out` ([2]) and in `vfy_kernel_planets.py`
(V3, max deviation 2×10⁻¹⁶).

## 3. The three closures of the same action, per planet (S3, both footings)

Reading A = constitutive "constant-|a| reduction" K(+a²/a₀²) → scalar μ_fw(|a|/a₀) (the published
galactic ν-recovery). Reading B = spectral (Borel calculus on the orbit's own spectrum). Reading C =
SPEC's gated off-circular completion S(|a|/a₀)·L(ω/ω_c), free corner ω_c.

**Canonical footing** (a₀=9.362e-11):

| body | ω [rad/s] | g_N [m/s²] | W=cω/a₀ | A: δg=a₀/2 | excl. | B react δg | margin | B drift |
|---|---|---|---|---|---|---|---|---|
| Mercury | 8.27e-7 | 3.96e-2 | 2.65e12 | 4.68e-11 | **1018×** | 7.06e-28 | 6.5e13 | 0.57 m/yr |
| Venus | 3.24e-7 | 1.13e-2 | 1.04e12 | 4.68e-11 | 585× | 1.32e-27 | 6.1e13 | 1.07 m/yr |
| Earth | 1.99e-7 | 5.93e-3 | 6.38e11 | 4.68e-11 | 5380× | 1.82e-27 | 4.8e12 | 1.47 m/yr |
| **Mars** | 1.06e-7 | 2.55e-3 | 3.39e11 | 4.68e-11 | **33 436×** | 2.78e-27 | 5.0e11 | 2.25 m/yr |
| Jupiter | 1.68e-8 | 2.19e-4 | 5.38e10 | 4.68e-11 | 84× | 9.47e-27 | 5.9e13 | 7.67 m/yr |
| Saturn | 6.76e-9 | 6.46e-5 | 2.16e10 | 4.68e-11 | 6687× | 1.72e-26 | 4.1e11 | 14.1 m/yr |
| Moon | 2.66e-6 | 2.70e-3 | 8.52e12 | 4.68e-11 | — | 4.64e-30 | — | 3.79 mm/yr |

**Alt footing** (a₀=1.130e-10): a₀/2=5.65e-11; exclusions 1228× (Mercury) … **40 357× (Mars)**; drifts ×1.21.

- **Reading A — the landmine at full strength.** A constant sunward a₀/2 at every planet, excluded 10³–10⁴×.
  BN11 already ruled this class out. If the constant-|a| reduction is the circular-orbit law (it is stated
  as exactly that at galaxies), Door C is dead at planets. No EFE rescue exists in MI, and (V2) no
  DC-into-GM rescue exists either.
- **Reading B — killed by kinematics.** Reactive residuals 10⁻²⁸–10⁻²⁵ m/s², i.e. 10¹⁰–10¹³× under the
  per-planet bounds. Milgrom's 2009 folk-expectation is realized with 10–13 orders to spare — but the same
  pure phase carries the drift confronted in §4, and the same theorem erases the RAR in §5.

## 4. The secular drift a₀/c — the previously-uncomputed dissipative channel (S4)

Chain: (1) K=e^{iφ}, φ=arcsin(a₀/2cω) [exact, S2]; (2) the phase lag leaves a tangential imbalance
f_t = tan φ·g_N ≈ Im K·g_N [exact trig]; (3) a tangential force drives d ln r/dt = 2f_t/(ωr) = 2f_t/v
[orbital mechanics] ⟹ **d ln r/dt = 2ω Im K = a₀/c — universal, every orbit, both footings.** Step (3),
the load-bearing orbital-mechanics factor, is confirmed in the time domain to **0.2%** (direct tangential
drag, ε=10⁻⁶, integrator-baseline subtracted; ratio 0.9979). Confrontation (magnitude sign-blind; the
inspiral-vs-outspiral **sign inherits the s=−1 postulate**):

| footing | a₀/c [/yr] | vs MESSENGER Ġ/G<4e-14 | vs LLR Ġ/G 2σ | lunar drift vs ±0.08 mm/yr | Saturn/Mars vs proxies |
|---|---|---|---|---|---|
| canon | 9.86e-12 | **×246** | ×407 | 3.79 mm/yr → **47σ** | Sat ×6, Mars ×45 |
| alt | 1.19e-11 | **×297** | ×492 | 4.57 mm/yr → **57σ** | Sat ×7, Mars ×54 |

Honest scope: the Ġ/G numbers are fits of that signal class, not a dedicated refit of this kernel — a
factor-few, not orders, of slack. rb2's independent ~0.4 m/yr Earth estimate is the same physics with an
O(π) orbit-averaging convention (ours is ODE-checked). **Reading B is excluded in this channel by ~2.4–2.7
orders**, independently of the RAR kill.

## 5. The galactic side of the fork (S5) — the same theorem that kills the tail kills the RAR

Under Reading B every rotation-supported system is Newtonian to ~10⁻⁷ (1−ReK: MW@Sun 1.4e-8, SPARC edge
8.0e-8, deep dwarf 9.7e-9 vs needed ν−1 = 0.199 / 0.732 / 1.082). **The published nu-recovery lives
entirely on Reading A.** And no *pure-frequency* kernel can substitute: at fixed y, ω=ya₀/v varies by
1.18 dex across SPARC, so a frequency-keyed ν_eff would split the dwarf/giant RAR branches by ~0.59 dex vs
the observed <0.06 dex coherence — **frequency-only closures are RAR-dead independently of the planets.**

## 6. Reading C — the exact condition for a planetary pass (S6)

K_eff(a,ω) = 1 − S(|a|/a₀)·L_c(ω/ω_c), Lorentzian gate (form the SPEC says is forced by the dS 1/sinh²
envelope), free corner ω_c. Three requirements: (i) reactive perihelion (binding: **Saturn**), (ii)
secular drift (binding: **Moon Ġ/G**), (iii) RAR floor (gate ≥0.90 at the deepest confirmed MOND points).

| footing | reactive ceiling | drift ceiling | RAR floor | **WINDOW** | width |
|---|---|---|---|---|---|
| canon | ω_c ≤ 8.27e-11 | ω_c ≤ 2.21e-14 (τ≥1.4 Myr) | ω_c ≥ 8.99e-15 | **[9.0e-15, 2.2e-14] rad/s = [1.4, 3.5] Myr** | ×2.5 |
| alt | ω_c ≤ 7.52e-11 | ω_c ≤ 1.83e-14 (τ≥1.7 Myr) | ω_c ≥ 1.08e-14 | **[1.1e-14, 1.8e-14] rad/s = [1.7, 2.9] Myr** | ×1.7 |

**Reading C passes all planetary bounds IFF the corner sits in a ~Myr sliver** — a **conditional** pass:
nothing published pins ω_c (the SPEC says so verbatim); of its three named corner candidates only the ~Myr
"d1-pole" lands in the window (ω_int ~0.4 Gyr and H_Λ ~17.5 Gyr corners close the MOND gate on galaxies
and are RAR-dead). **Falsifiable both ways:** (1) at the surviving corner the gate kills ≥84–96% of the
MOND boost in 3–20 kAU wide binaries → a confirmed Chae-type AQUAL-strength WB boost **kills** gated Door
C; a Banik-type Newtonian WB result is what it **predicts**. (2) the drift at the max corner sits **at**
current Saturn/Mars secular sensitivity → a dedicated INPOP/EPM secular refit improving ×3 either detects
it or closes the window.

## 7. Ledger and verdict (S7)

**FORCED (kinematics + the published K, no knobs):** bound orbits feed the kernel only z≤0, so the a₀/2
landmine is **not** a prediction of the published *operator* on planets — it is an artifact of the
constitutive constant-|a| reduction; the operator reactive residual is 10⁻²⁸–10⁻²⁵ m/s² (10–13 orders
under bounds), but the same theorem erases the RAR and forces the excluded drift a₀/c; no pure-frequency
kernel carries the RAR.

**FREE (named, not pinned by Herglotz + sum rule + ‖K‖≤1 + causality — verified corner-blind):** the
off-circular closure map (ω_c "corner-location FREE"); the planetary data now **pin it two-sidedly** to
ω_c ∈ [~1e-14, ~3.5e-14] rad/s; the s=−1 MOND sign (owns the drift direction).

**VERDICT, both directions at full strength:**
1. The published Herglotz kernel, on its own operator definition, **does** suppress the a₀/2 tail — 10–13
   orders, kinematically. Milgrom's folk-theorem holds for this kernel.
2. But that same evaluation (a) fails to reproduce the framework's own galactic phenomenology and (b) is
   excluded ~250–500× in the previously-uncomputed dissipative/phase channel (universal drift a₀/c).
3. The constitutive evaluation — the one the published galactic wins actually use — **IS** the landmine,
   excluded 10³–10⁴×, with **no DC-into-GM absorption escape** (V2).
4. Door C survives the solar system **only as gated Reading C**: acceleration-keyed amplitude × frequency
   gate with the corner in a ~Myr sliver — a falsifiable, two-sided, currently-open **conditional** pass.
5. **HONEST CEILING:** none of this can prefer the framework over ΛCDM. At planetary accelerations
   (10⁴–10⁸ a₀) GR predicts zero anomaly and healthy MOND-family theories predict near-zero; these numbers
   **discriminate BETWEEN the framework's own doors only.**

**Bottom line for the tasked question:** the published Herglotz kernel does **not** force the a₀/2
suppression at the reading that keeps the framework's physics — the only kernel-level suppression is a
kinematic non-generation on the operator reading (RAR-dead + drift-excluded), and there is no
standard-DC-into-GM absorption of the constant tail either. MI does not *uniquely* evade at the kernel
level; the evasion that survives is the gated Reading-C completion with a free corner.
