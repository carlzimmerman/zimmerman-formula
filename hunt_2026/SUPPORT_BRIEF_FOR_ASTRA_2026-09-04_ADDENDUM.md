# Addendum to the support brief, 2026-09-04 (night): what the target is missing, and the matched disc solve

## A. The gate the 13 requirements do not contain

Your §6 plan derives Φ and χ from metric or constrained variables, varies that action, and computes the constraint chain,
toward a static limit that is exactly AQUAL/QUMOND with the chosen kernel at every scale. Three committed numbers say that
static limit is dead before the covariant question is reached:

| the framework's kernel, modified gravity | value | script |
|---|---|---|
| Solar-System EFE quadrupole, QUMOND | 6.2× / 6.8× the Park 2026 ceiling (canonical / alt) | f23 §6 |
| same, exact AQUAL (non-spherical solve) | 7.7× / 8.8×; 7.3× / 8.3× at g_ext − 1σ | f24 |
| modified inertia, lensing | M_dyn/M_lens = 6.4 vs 1.0–1.3 observed, ~20σ | `real_research/reviews/mi_lensing_axis_2026.py` |

None of the 13 requirements is "the theory's own static limit must give |Q₂| < 5.2×10⁻²⁷ s⁻² in the Galactic external
field". Requirement 4 (Cassini/PPN) was checked in the closure program through the kernel's Newtonian tail and the
vector-sector PPN parameters; the EFE quadrupole lives in the transition at r_M(☉) ≈ 0.1 pc and is a property of the
static equation's *shape*, not of its tail. Any completion that reproduces requirement 1 exactly inherits 6–9×.

So the structural statement, which is the closest thing to a lightbulb the numbers allow: **a viable static limit cannot be
scale-free.** It must carry a length ξ below which the phantom response switches off, with 0.1 pc ≪ ξ ≲ 200 pc: the Solar
System and the Gaia wide binaries are then Newtonian, discs and dwarf spheroidals keep the RAR, and lensing keeps the
phantom because the phantom is still a real gravitating response above ξ. Nothing in the framework's own scales supplies a
parsec-scale length (f22 §4a: the Λ lengths are Gpc), so ξ would be a new measurable parameter, like κ.

What the repository has already done with this idea, so you do not repeat it: the localised version (a Helmholtz filter on
the external field, `york_Lclosure_global_2026.py` / `york_Lclosure_dirac_2026.py`, "Theorem 8") was closed as a *local*
closed theory because localising the filter adds a propagating mode. A genuinely non-localisable version, or a medium
with a healing length (condensate/superfluid-type, which supplies ξ = ħ/(m c_s) without a nonlocal kernel), has not been
written; the condensate work that exists (`project_condensate_mu_pincer`) died on the *amount* of phantom between KiDS
galaxy stacks and clusters, not on ξ.

## B. Its one clean test, and its honest status on the ledger — `hunt_2026/f27_newtonian_side_of_the_ledger.py` (3 checks, 2 hypothesis fails)

Predictions of a ξ in that window: Cassini passes; **Gaia DR4 wide binaries give γ_v = 1.00**, the opposite of the
framework's pre-registered 1.16–1.23 (this is the Cassini ↔ wide-binary lock of `cassini_widebinary_lock_2026.py`, read
the other way round); globular clusters (r_h ≈ 20 pc) are Newtonian.

The ledger, with B_Newton = B_MOND + log₁₀ν(y) computed for every row:

- Three of the four outer-halo globulars ARE Newtonian-side: Pal 4 (B_MOND −0.81, B_N −0.11), Pal 14 (−0.87, +0.15),
  NGC 2419 (−0.20, +0.02). Pal 3 is MOND-side (−0.15, +0.72). MOND over-predicts the three by 0.2–0.9 dex.
- But size does **not** order the ledger: DF2 (1.65 kpc, B_N +0.00), the Salpeter early-types, the tidal dwarfs and the
  Milky Way vertical force also sit Newtonian-side at large radii, several of them marginally (M/L choice flips the
  early-types; the tidal dwarfs and K_z are within 0.15 dex of both). "Smaller is Newtonian" has AUC 0.58, p = 0.32.

So this is a Cassini + globular-cluster + DR4 statement, not a ledger pattern, and I am not presenting it as a result.
It is the only structure I can find that passes both arms of the pincer, and DR4 falsifies it cleanly: γ_v = 1.00 keeps
it alive and kills the framework's own pre-registration; γ_v ≈ 1.2 kills it and leaves modified gravity Cassini-dead.

## C. The matched disc forward solve you asked for — `hunt_2026/f26_matched_disc_forward_solve.py` (8 checks, 2 hypothesis fails)

For each of 147 SPARC discs and each kernel: the baryonic field at the kernel's own profiled M/L (f25), inverted to a
sech² thick disc with f18's analytic Hankel inversion, solved in QUMOND with the kernel's ν on the same Hankel grid at
the profiled a₀ and ±0.15 dex, and the disc correction T(R) = log₁₀[g_QUMOND/g_algebraic] applied to the algebraic
prediction on the data before the paired comparison. Validation: the chain reproduces an exact exponential disc's
correction to 0.02 dex on interior points (0.04 at the outermost, extrapolated point). Inversion residual median 0.073
dex, 87 of 147 under 0.10; the comparison is read on the full sample and on that subset. Catalogue distance and
inclination for every kernel (paired); no external field. Descriptive MSE, no sigma.

| | median T (dex) | g_bar/a₀ 0.03–0.1 | 0.1–0.3 | 0.3–1 | 1–3 | 3–30 |
|---|---|---|---|---|---|---|
| ν_RAR | −0.025 | −0.040 | −0.027 | −0.023 | −0.019 | −0.007 |
| μ_exp | −0.023 | −0.040 | −0.027 | −0.023 | −0.013 | −0.001 |
| μ₁₀ | −0.023 | −0.044 | −0.031 | −0.030 | −0.002 | 0.000 |

1. **The disc geometry cannot separate exp from RAR.** Their corrections agree to 0.002 dex (median) against a kernel
   difference of up to 0.073 dex. After correction the paired MSE difference is a coin flip on the full sample
   (interval [−0.00111, +0.00102] dex², exp worse in 49%) and leans exp on the well-inverted subset (worse in 19%,
   interval still containing zero). Undecided stays undecided.
2. **The disc geometry weakens, but does not remove, the μ₁₀ rejection.** μ₁₀'s correction vanishes above a₀ where
   the RAR's is −0.02 dex, so the forward solve moves μ₁₀ toward the data at high acceleration: worse than ν_RAR in
   94.6% of resamples (full) and 90.2% (subset), against 99.9% algebraically. On the forward solve μ₁₀ is
   *disfavoured*, not rejected; the rejection rests on the algebraic comparison (f25, f28). This is the one place
   the forward solve changed a verdict's strength, and you were right to ask for it.
3. **The QUMOND correction makes the framework's kernel fit WORSE** (RMS 0.2015 → 0.2031 dex, ΔMSE +0.00064), leaves
   μ_exp unchanged, and improves μ₁₀. SPARC discs follow the spherical algebraic relation better than the QUMOND disc
   solution of the same kernel. That is f18's curl-sign finding on the full sample: the data do not want the
   modified-gravity disc field. It is a second, independent reason the static limit cannot be "one μ in AQUAL/QUMOND"
   — and it is the side of the fork that has no field-sourced quadrupole either.

Scope left open, as you named it: per-galaxy distance and inclination marginalisation, the external field, and the
AQUAL (rather than QUMOND) disc operator. None of these can plausibly move a 0.002-dex kernel-independence.

## D. The one-argument pincer, closed on the μ_n family — `hunt_2026/f28_one_argument_pincer.py` (4/4)

Both axes with the same machinery: the committed DHF quadrupole integral at the solar-circle field (both footings), and
the paired-galaxy comparison with a₀ and a global disc M/L profiled per kernel.

| kernel | Q₂/ceiling canonical | alt | Cassini | SPARC RMS (dex) | worse than ν_RAR in | galaxy verdict |
|---|---|---|---|---|---|---|
| ν_RAR | 6.23 | 6.83 | fail | 0.2015 | — | reference |
| μ₁ | 6.06 | 6.60 | fail | 0.2016 | 72% | tolerated |
| μ₂ | 2.81 | 3.69 | fail | 0.2042 | 98.8% | disfavoured |
| μ₃ | 1.24 | 1.96 | fail | 0.2059 | 99.8% | rejected |
| μ₄ | 0.59 | 1.10 | safe (canonical) | 0.2070 | 100% | rejected |
| μ₅ | 0.31 | 0.66 | safe | 0.2076 | 100% | rejected |
| μ₇ | 0.13 | 0.31 | safe | 0.2083 | 100% | rejected |
| μ₁₀ | 0.06 | 0.17 | safe | 0.2087 | 100% | rejected |

No member is both Cassini-safe and galaxy-tolerated. The boundary is sharp on both sides: the softest Cassini-safe
member (n = 4) loses on every paired resample; the sharpest galaxy-tolerated member (n = 1) is 6× over the ceiling.
Exact AQUAL only widens the Cassini side (f24: +8–30%). Scope: the μ_n family is the sharpness axis DHF identify as
the only lever on Q₂; it is not every one-argument law, and the statement is on that family.

Read with RESUME_HERE's own line — which field carries the halo cannot move Q₂ — this is the closure of the
one-argument class: no static law μ(g/a₀), carried by any field, passes both the Solar System and the galaxy data.
The second argument is not another acceleration (u02); it is a length.

## E. The coherence-length law, made concrete — `hunt_2026/f29_coherence_length_law.py` (12/12)

**The hardest problem, in one sentence:** *find the covariant action whose static limit is QUMOND applied to a
Helmholtz-smoothed Newtonian potential, (1 − ξ²∇²)Φ̃ = Φ_N, with Φ̃ entering as a constraint that adds no propagating
degree of freedom — because the phantom must switch off below a length ξ ≳ 0.03 pc to survive Cassini, lensing forbids
modified inertia, and no acceleration-only law can do it (f28).*

The static system (three elliptic equations, no time derivatives):
```
(i)   ∇²Φ_N = 4πG ρ_b
(ii)  Φ̃ = S_ξ Φ_N                     [a Gaussian filter of width ξ was used for the numbers; see §G for why the KERNEL'S CORE matters]
(iii) ∇²Φ = ∇·[ ν(|∇Φ̃|/a₀) ∇Φ̃ ]     [ν = the framework's kernel]
```
For sources varying on scales ≫ ξ it *is* QUMOND. For a point source it removes the phantom from inside ξ. Theorem 8
killed the version in which (ii) is a dynamical field; here it is a constraint, and whether it can stay one in a
covariant host is exactly the question your Dirac-chain machinery (§3 of your orbit-shape report, which found 0 DOF for
the two-field static block) can answer with Φ̃ as a third constrained variable.

Everything below comes from one phantom-density quadrature (axisymmetric source in the Newtonian external field),
validated at ξ → 0 against the committed DHF quadrupole to 0.2% (with the repository's Q₂ = 3G·I₂ convention) and by
the spherical null.

**Solar System, two bounds.** Quadrupole, Q₂/ceiling (canonical / alt): ξ = 0.02 pc: 4.5 / 5.4; 0.03 pc: 1.12 / 1.32;
0.04 pc: 0.46 / 0.54; 0.05 pc: 0.23 / 0.27; 0.1 pc: 0.029 / 0.034; then ∝ ξ⁻³ (slope −3.00). Monopole: smoothing spreads
the Sun's phantom over ξ, so the phantom mass inside Saturn's orbit must clear the ephemeris bound (Pitjev & Pitjeva 2013,
< 6.7×10⁻¹¹ M☉ inside 9.5 AU): ratio to bound 3.4 at 0.03 pc, 1.44 at 0.04 pc, 0.74 at 0.05 pc, 0.09 at 0.1 pc. **The
binding floor is the monopole's: ξ ≳ 0.045 pc, about one MOND radius of the Sun** (the first version of f29 lacked this
check; it is S4 now). And the law has a hard lower edge: smoothing over *less* than r_M(☉) = 0.039 pc
makes the quadrupole *larger* (the transition region moves inward where the r⁻³ weighting is strongest), so ξ below
~0.03 pc is worse than no smoothing.

**Wide binaries — the Cassini ↔ wide-binary lock is broken by a length.** The pair's phantom monopole inside the
separation, scaled to the pre-registered 1.21 where it saturates:

| ξ | 2 kAU | 4 kAU | 6 kAU | 10 kAU | 21 kAU | 31 kAU |
|---|---|---|---|---|---|---|
| 0 (the framework's own law) | 1.004 | 1.06 | 1.15 | 1.21 | 1.21 | 1.21 |
| 0.04 pc (quadrupole-safe, monopole 1.4× over) | 1.001 | 1.007 | 1.022 | 1.073 | 1.19 | 1.21 |
| 0.05 pc (the smallest admissible ξ) | 1.000 | 1.004 | 1.012 | 1.044 | 1.16 | 1.20 |
| 0.07 pc | 1.000 | 1.001 | 1.005 | 1.019 | 1.095 | 1.17 |
| ≥ 0.3 pc | 1.000 | 1.000 | 1.000 | 1.000 | 1.002 | 1.007 |

Two things the repository did not have. First, the pre-registered boost at 20–30 kAU **survives both Solar-System bounds** at
ξ ≈ 0.05 pc (1.16 at 20 kAU, 1.20 at 30 kAU) — the lock (`cassini_widebinary_lock_2026.py`) assumed a screening keyed on the external-field
strength; one keyed on length separates the two because the quadrupole is r⁻³-weighted around the Sun while the binary
boost is the monopole inside the separation. Second, **the prediction**: the coherence length moves the wide-binary
knee outward, from ~5–8 kAU (where the pair's own field equals the external one) to ~15–20 kAU. At 6 kAU the framework
says 1.15 and the smallest admissible law says 1.01; at 10 kAU, 1.21 against 1.04; they agree again by 30 kAU. Gaia DR4
binned in separation (the 4–10 kAU bins) decides it. A flat 1.00 or a flat 1.2 fits neither. And for ξ ≥ 0.3 pc the
binaries are Newtonian at every separation.

**Globular clusters measure ξ, if three of four are trusted.** Each outer-halo row with its own external field, the
fraction F of the MOND+EFE boost the data require: Pal 4, F < 0 (Newton or below, ξ unbounded above); Pal 14,
F = 0.075 → ξ ≈ 50 pc; NGC 2419, F = 0.063 → ξ ≈ 140 pc; Pal 3, F = 0.81 → ξ ≈ 9 pc (the discordant row). At ξ ≈ 84 pc
a Draco-like dwarf keeps 76% of its boost (a 0.1–0.15 dex trim, inside the dwarf rung's prescription spread) and a
3 kpc disc keeps 100.0%.

**So there are two regimes, and the data on disk already split them:**
- small ξ ≈ 0.045–0.1 pc: both Solar-System bounds pass, the wide-binary boost survives at 20–30 kAU with the knee at
  15–20 kAU, globulars stay MOND (f13's +0.3 dex over-prediction remains);
- large ξ ≈ 50–140 pc: Cassini passes, wide binaries Newtonian at all separations, three of four globulars Newtonian,
  dwarfs trimmed, discs and lensing untouched.
Gaia DR4 in separation bins and the outer-halo globulars decide between them; the Solar System is satisfied by both.

Scope: a static one-parameter law, not a relativistic theory; the globular source is a Gaussian matched to a Plummer
half-mass radius; the wide-binary numbers are a monopole-phantom ratio scaled to the pre-registration, not a rerun of
its pipeline; the pre-registration file is untouched.

## F. A candidate action — the constructive object, stated with its status

The static system of §E is the weak-field limit of a *local* action if the smoothing is carried by a spatial fourth-derivative
term rather than by a nonlocal filter. With a unit timelike aether $u^\mu$ (the foliation AeST and the khronometric hosts
already carry), $h_{\mu\nu}=g_{\mu\nu}+u_\mu u_\nu$, $D$ the spatial derivative along $h$, and $Y=h^{\mu\nu}\partial_\mu\phi\,\partial_\nu\phi$:

$$S=\int d^4x\sqrt{-g}\Big[\frac{R}{16\pi G}+\mathcal L_{\rm ae}(u;c_1..c_4)\Big]
-\frac{1}{8\pi G}\int d^4x\sqrt{-g}\Big[-\frac{K}{2}(u^\mu\partial_\mu\phi)^2+a_0^2F\!\Big(\frac{Y}{a_0^2}\Big)+\xi^2\,(D^2\phi)^2\Big]+S_m[\tilde g,\psi],$$

with matter coupled so that the potential it feels is $\Phi_E+\phi$ and light sees the same combination (the AeST/TeVeS-type
coupling this repository's lensing embedding already established: Φ = Ψ with the phantom, γ_PPN = 1 at that level).

**Static limit** ($u=\partial_t$): $\nabla\cdot[F'(|\nabla\phi|^2/a_0^2)\nabla\phi]-\xi^2\nabla^4\phi=4\pi G\rho$ — AQUAL with a
healing length. For sources varying on scales ≫ ξ it is AQUAL with $\mu=F'$ = the framework's kernel (f23 §5 gives $F$ in closed
form). Its linear response is exactly the Helmholtz filter, $\phi_k\propto\rho_k/[k^2(1+\xi^2k^2)]$, Coulomb minus Yukawa in real space.
**Correction (f30):** that kernel has a 1/r cusp, so inside ξ the screened phantom's force is *constant* and sunward,
$f_{\rm ph}GM/(2\xi^2)$, not the harmonic core of the Gaussian filter used for the §E numbers; the planetary bound on a constant
sunward acceleration (the repository's α = 1 ephemeris gate, 3.7×10⁻¹⁴ m s⁻²) then needs ξ ≥ 0.8 pc for this host. See §G.

**Quadratic health in the aether frame**, on a static-gradient background (the block your §3 analysed): with $\mu=F'>0$ and
$(x\mu)'>0$ (f23 5f: both hold for the framework's kernel on six decades) and $\xi^2>0$,

$$K\omega^2=\mu\,k_\perp^2+(x\mu)'\,k_\parallel^2+\xi^2k^4>0 .$$

No ghost ($K>0$), no gradient instability, and no Ostrogradsky mode because the higher derivatives are spatial only. It is a
Bogoliubov dispersion, $\omega^2=c_s^2k^2+\xi^2k^4/K$: the MOND scalar is a superfluid-phonon-like mode with healing length ξ.
The QUMOND-bilinear ghost you found (det W = −4A²) is absent because there is one scalar with its own kinetic term, not two
potentials with a cross term.

**What it changes, relative to the hosts already killed here.** (1) Inside ξ the scalar is k⁴-dominated and decouples: its
contribution to the Solar-System metric is suppressed by powers of $r/\xi$ with $\xi\gtrsim0.045$ pc ≈ 9000 AU. The AeST α₁ lock
(doorA_alpha1_generality_theorem: the MOND scalar's coupling to the aether forces α₁ ≠ 0) was computed with the scalar
*unscreened* at Solar-System scales; with the scalar screened, α₁ and α₂ revert to the aether's own, which the four Einstein-aether
couplings $c_1..c_4$ can zero. That reopens the PPN gate as a calculation rather than a theorem. (2) At cosmological $k$ the ξ²k⁴ term
is invisible, so the cosmological sector is the aether-scalar one the repository has already run through CLASS; AeST's separate
mass parameter for the dark-matter-like growth is a separate question, untouched here. (3) RESUME_HERE's own note that
"Vainshtein / k-mouflage is unrun — the only class that screens the force" is this: a derivative screening, but spatial and
fourth-order, with the screening scale set by a length instead of a coupling.

**Status, stated plainly.** A candidate action with a healthy quadratic sector and the right static limit. Not a theory: its
Solar-System numbers, its full PPN with the screened scalar, its Dirac count with the aether, and its FLRW background are the
four calculations that decide it, in that order. The first two your machinery can run now: the biharmonic static solve is the
AQUAL solver with one extra term, and the PPN is your `aqual_solar_gate_2026` with ξ in it.

## G. The door the finding opens — `hunt_2026/f30_ppn_screening_door.py` (5/5)

**What killed every aether-scalar host here** was the preferred-frame PPN sector sourced by an *unscreened* MOND scalar:
α₁ = −4c₁₄ − 4(2−K_B)/(J_Y+1), un-tunable (doorA_alpha1_generality_theorem), α₂ four to five orders over. The scalar's term
exists because at Solar-System scales its static field of the Sun is a 1/r potential, and every PPN parameter is the
coefficient of a 1/r-type post-Newtonian potential.

**What the coherence length does to that.** With the spatial biharmonic term the scalar's static Green's function is
Coulomb minus Yukawa, $(1-e^{-r/\xi})/r$ (verified in Fourier space, G1). Inside ξ the potential is a constant, a constant
force and an $r^2$ term — **no 1/r term** (G2). So the scalar's contributions to γ, β, α₁, α₂ are absent at leading order and
enter only through the $(r/\xi)^2$ tail: suppression 6×10⁻⁹ at 1 AU, 5×10⁻⁷ at Saturn, 5×10⁻⁶ at Neptune for ξ = 0.045 pc (P1).
The α₁ lock does not apply to a screened scalar. The aether's own α₁ = −4c₁₄ (with c₁₃ = 0 for c_T = 1) and α₂ are
Einstein-aether's and have a viable post-GW170817 region (c₁₄ ≲ 2.5×10⁻⁵; cited, not recomputed). This is RESUME_HERE's
"Vainshtein / k-mouflage — unrun, the only class that screens the force," realised with a length instead of a coupling.

**What replaces the lock: a fork set by the kernel's core, not a wall.**
- *Cuspy core (a single biharmonic term).* The constant sunward force $f_{\rm ph}GM/(2\xi^2)$ is exactly what the
  repository's α = 1 ephemeris gate bounds (3.7×10⁻¹⁴ m s⁻²). With the phantom fraction at the Sun in the Galactic field,
  $f_{\rm ph}=\nu(e_N)-1=0.35$, the floor is **ξ ≥ 0.8 pc** (C1) — eighteen times the smooth-core floor of f29. In this host
  Gaia DR4 sees γ_v = 1.00 at every separation (f29 W3), consistent with a Banik-type null and inconsistent with a Chae-type
  boost; the pre-registration would be wrong; the globulars' 50–140 pc is the natural range.
- *Smooth core (two lengths, sixth order in spatial derivatives, the Yukawa cusps cancelling).* The f29 window ξ ≈
  0.05–0.1 pc survives, with the pre-registered boost at 20–30 kAU and the knee at 15–20 kAU. The price is a second length.
- Common to both: the RAR's Newtonian end bounds the scalar's high-acceleration fraction at f ≲ 0.3 (C2), which a host whose
  scalar *is* the phantom satisfies automatically.

**Status.** No gate this repository has computed closes either branch; the four calculations of §F remain, and the first
— the full PPN expansion with the k⁴ term — is the one that could. Astra: this is the calculation to put in front of the
covariant question, because it decides whether the host class is open at all before any action is varied.
