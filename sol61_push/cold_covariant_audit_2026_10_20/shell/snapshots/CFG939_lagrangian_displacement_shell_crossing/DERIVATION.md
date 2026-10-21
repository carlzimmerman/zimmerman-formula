# CFG939 derivation: P as the exact Lagrangian displacement of a collisionless medium, and what shell crossing does

Criteria: `FROZEN_CRITERIA.md` (3524438b2), amendment A1 (7dace0a16, pre-result). Symbolic checks: `cfg939_sym.py` (30/30).
Numerics: `cfg939.py`. Notation follows THEORY_CANONICAL_2026-10-14.md S2–S3: K = 4πG, u = K|P|, R(u) ≡ K W_rem′(u) = u²/(a0 − u),
γ = K L*²/2 = 2πG L*². κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled.

This file does not repeat astra's read-only audit (sol61_push/cold_completion_2026_10_20/GRAVITY_ACTION_AUDIT.md). That audit
already gives the Eulerian field equations, the self-gravity cancellation in the identification (ID) branch, the force
a_r = −g_Nb + R(u) − γ(∇²P)_r, the statement that an inertia I|Ṗ|²/2 "does not follow from the static action", and the zero net
polarization charge of an isolated basin. What is new here is the Lagrangian-map form, the multi-stream statement, the shell-crossing
conditions, the unbinding thresholds and the S4 classification.

## 1. Kinematics

### 1.1 Sign (K1)
Write x(q, t) = q + Ψ(q, t) and ρ = ρ̄ / det(∂x/∂q). To first order δ = −∇·Ψ. With P ≡ −ρ̄Ψ:
- ∇·P − (ρ − ρ̄) = O(Ψ²);
- ∂ₜP + j = O(Ψ²).

So **P = −ρ̄Ψ** (P points back toward where the medium came from). The opposite sign fails (K1d tooth).

### 1.2 The identity is not linear-only (C3 premise)
Define P by the record's own S3, P(x, t) = P(x, 0) − ∫₀ᵗ j dt′, with j the **total** mass current. Continuity
∂ₜρ + ∇·j = 0 is exact for any number of streams, so ∇·P = ρ − ρ̄ holds **exactly at all times, before and after shell crossing**
(given ∇·P = ρ − ρ̄ at t = 0). H-SC's premise ("∇·P = ρ − ρ̄ is only the linear form") is false for the identity. What is
linear is the *displacement reading* P = −ρ̄Ψ.

**1-D (exact; K1b, K1c).** P(x) = (mass to the left of x) − ρ̄x, up to a constant.
- In a single stream, P(x(q)) = ρ̄(q − x(q)) = −ρ̄Ψ(q) **exactly**, at any amplitude.
- In a multi-stream region with streams s at the same x, P = −ρ̄ Σ_s sign(J_s) Ψ_s, an orientation-weighted (degree) sum of stream
  displacements, and ∂ₓP = ρ̄ Σ_s 1/|J_s| − ρ̄. K1c checks this through a fold: max error 8.9e-16 in P, 1.5e-9 in ∂ₓP.

**Spherical (exact; K1b).** P_r(r) = [M(<r) − (4π/3)ρ̄r³]/(4πr²), summing all streams.
- In a single stream, P_r = ρ̄(q³ − r³)/(3r²) = −ρ̄Ψ + ρ̄Ψ²/r − ρ̄Ψ³/(3r²), with Ψ = r − q.
- For a collapsed shell (r ≪ q), K P_r = G M_c(<r)/r²: **u is the Newtonian field of the enclosed cold excess.** The record's u ~ a0
  inside galaxies therefore needs the exact form. The linear form −ρ̄Ψ is off by ~(q/r)², which is large for any collapsed system.

**3-D.** Only the longitudinal part P_L = ∇∇⁻²(ρ − ρ̄) is fixed by the instantaneous map. The transverse part P_T = −∫ j_T dt
depends on the history. The static S2 equation in a geometry without symmetry also asks for some P_T. Whether the medium's
history supplies the P_T that S2 demands is an open compatibility condition. It cannot be tested in 1-D or spherical symmetry and is
not tested here.

## 2. The action in Lagrangian coordinates (1-D and spherical, where P is fixed by the map)

### 2.1 Kinetic term: FORCED
Mass conservation per element (ρ d³x = ρ̄ d³q) fixes the kinetic term of a collisionless medium as ½ρ̄|∂ₜx|² per unit Lagrangian
volume. In P language, at linear order this is |Ṗ|²/(2ρ̄) (K2d). **The inertia of P is I = 1/ρ̄, forced by S3**, not free. Exactly,
the kinetic energy is Σ_s ½ρ_s v_s² = |j|²/(2ρ) + ½ρσ². The velocity-dispersion part ½ρσ² of a multi-stream region does not appear
in P or Ṗ at all.

### 2.2 Gravity and the critical quadratic
Expand −|∇Φ − KP|²/(2K) = −|∇Φ|²/(2K) + ∇Φ·P − K|P|²/2.
- ∇Φ·P = −Φ(ρ − ρ̄) + a divergence. So the medium couples to Φ as ordinary mass, −∫ρ̄ Φ(x(q)) d³q, exactly and for all streams.
- On the longitudinal sector, −K|P|²/2 is minus the Newtonian self-energy of ρ − ρ̄. It cancels the medium's self-gravity
  (CFG888; astra §4).

Eliminating Φ, the medium's potential energy (baryons fixed) is

  E[ρ] = ∫(ρ − ρ̄)Φ_b dV + ∫W_rem(|g_c|) dV + πG L*² ∫(ρ − ρ̄)² dV,   g_c = K P = Newtonian field of the cold excess.

Equivalently, E = E_Newton + ∫W_full(|g_c|) dV with W_full = W_rem + u²/(2K) ≥ 0. W_full cancels the cold self-energy at O(u²) and
adds the repulsion u³/(3K a0) at the next order.

### 2.3 Exact Lagrangians
**1-D, single stream.** Per unit q, with J = 1 + Ψ′:

  ℒ = ½ρ̄Ψ̇² − ρ̄Φ_b(q + Ψ) − J·W_rem(Kρ̄|Ψ|) − (γρ̄²/2)(J − 1)²/J.

**Spherical, single stream.** Per shell of mass dm with its own enclosed cold mass m_q:

  ℒ = dm[½ṙ² − Φ_b(r) − Π_q(r)],   Π_q(r) = ∫_r^∞ R(G m_q/r′²) dr′ = √(G m_q a0)[artanh√(u/a0) − √(u/a0)],   u = G m_q/r²   (K8a,b).

The stiffness term becomes **(γρ̄²/2)(1 − J)²/J per unit Lagrangian length** (K2e). This diverges as J → 0. It is the energy of a
barotropic pressure p = πG L*² ρ_c², with sound speed c_s² = 2πG L*² ρ_c.

### 2.4 Equations of motion (K2a–c)

  ẍ(q) = −∇Φ_b + R(K|P|) P̂ − γ∇ρ_c

This holds for every element in 1-D and spherical symmetry, single- or multi-stream, with P from §1.2. With the tether off
(W_rem → −u²/2K) it becomes planar Newtonian self-gravity, +Kρ̄Ψ (K2c). In single-stream 1-D, each element is tethered to its own
Lagrangian position by the restoring force −R(Kρ̄|Ψ|)sgnΨ. After crossing, the element is tethered to its **mass rank**:
P = ρ̄(q_rank − x). It is not tethered to its birth label.

### 2.5 Forced vs chosen

| item | status |
|---|---|
| P = −ρ̄Ψ (sign), exact in 1-D single stream | FORCED by S3 |
| ∇·P = ρ − ρ̄ through crossing (P = −∫j dt, total current) | FORCED by S3 as written |
| kinetic term ½ρ̄\|ẋ\|² ⇔ inertia I = 1/ρ̄ for P | FORCED by the mass identification |
| medium couples to Φ as ordinary mass; self-gravity cancelled by the critical quadratic | FORCED by S2's square form + ID |
| anchor = mass rank after crossing | FORCED by S3 (total current) |
| W_rem's form (hence the law), a0, κ = ½ | CHOSEN (fitted / input) |
| γ, L* ∈ [24 pc, ≳ 1 kpc] | CHOSEN (bounded, not derived) |
| ρ̄ (background of the identity) | input |
| P_T in 3-D (history vs static S2 demand) | OPEN |
| continuation past a gradient catastrophe of the stiff cold fluid (§4.4) | NOT SPECIFIED by S2 |

## 3. Shell crossing does not untether (C3)

With S3 as written, P stays single-valued through crossing and the force law in §2.4 does not change. A multi-stream region is
tethered exactly as a single-stream one. Its tether acts on the mass profile.

The record's own CFG747/748 code already does this: it sorts the shells by radius to get the enclosed mass. Its law state is
reached by collisionless phase mixing. **The relaxed tethered state is therefore multi-stream.** In N3, 100% of the mass inside 5 r_M
has crossed. The time-averaged mass at 2 r_M is on the law to −0.1%. At 5 r_M it is still filling at t = 2000: −3.4% to −5.1%
depending on the integration step. A run to t = 6000 (A2, report only) reaches −0.6% at 5 r_M (and 0.920 of the law at 10 r_M).

Two other ways to extend S2 to multi-stream states exist. Neither is forced:
- **Identity lift.** Each element stays tethered to its birth label and birth enclosed mass. Every element is then tethered forever,
  ∇·P = ρ − ρ̄ fails after crossing, and the relaxation channel disappears (each shell is an independent oscillator).
- **Coherent-current lift.** P is sourced only by a coherent (single-stream) part of the current. This breaks S3, needs a non-unique
  coarse-graining, and **is the two-population postulate restated.**

So no regime of S2 + S3 contains untethered, self-gravitating, bound cold matter. **S4's free population is not a regime of the
single medium.**

## 4. Shell-crossing conditions

### 4.1 Newtonian control (tether off, γ = 0)
Ψ = Ψ₀ cosh(√(Kρ̄) t) and J = 1 + Ψ₀′ cosh(√(Kρ̄) t), so t_sc = arccosh(1/max(−Ψ₀′))/√(Kρ̄). K3 reproduces it: sheets 1.87390 vs
1.87382 (4e-5).

### 4.2 Canonical tether, 1-D, γ = 0
The medium has no self-gravity, and R = O(u²) gives no linear restoring force. In a single stream each element is an independent
anharmonic oscillator, Ψ̈ = −R(Kρ̄|Ψ|)sgnΨ. Then J = 1 + Ψ₀′(q)·∂Ψ/∂Ψ₀.

The period depends on amplitude (deep regime: potential ∝ |Ψ|³, so T ∝ A^(−1/2)). As a result ∂Ψ/∂Ψ₀ grows secularly, and
**crossing always happens eventually**, after t_sc ≈ 1/(|Ψ₀′| A |ω′(A)|) ~ T/(π|Ψ₀′|) in the deep regime.

N1, amplitude 0.3: the exact single-stream solution crosses at t = 17.690, which is 1.64 periods (T = 10.78). The sheets cross at
17.690. The Newtonian collapse of the same start crosses at 1.874.

W_rem therefore *promotes* crossing, through anharmonicity. A harmonic tether would not cross from smooth data.

**Literal a0 → 0 (M3).** This does **not** give Newtonian collapse. Any admissible state has u < a0. With a0 = 1e-6 and the start
scaled to the wall, J − 1 = O(a0): 1 − J_min = 1.1e-4 by t = 2000, against a Newtonian crossing at 15.7. The crossing time grows as
1/a0. The limits do not commute: Newtonian collapse comes only from switching the tether off (M2).

### 4.3 Canonical tether, spherical, γ = 0
In a single stream, shell q moves in V_q = Φ_b + Π_q with m_q fixed. It has a turning point r_min(q) > 0 (the tether barrier and the
capacity wall u < a0). Shells cross because their radial periods differ.

The small-oscillation frequency about the law is ω² = 4πGρ_b + (2g_N/r)·a0/(a0 − u). Its deep point-mass limit is ω² = 2GM_b/r³
(K8j), which is slower than the law's orbital frequency by √(2√(g_N/a0)).

### 4.4 Stiffness
**Linear (D1).** The Newtonian control gives ω² = γρ̄k² − Kρ̄, so λ_J = √2 π L*. The canonical tether gives ω² = γρ̄k²: sound
only, no Jeans scale, because the medium has no self-gravity.

**Nonlinear.** The Lagrangian stiffness energy diverges at J → 0, so a cold single-stream medium cannot reach J = 0 smoothly.
Instead the cold fluid (p = πG L*² ρ_c²) **steepens into a gradient catastrophe at finite density** (N2):
- λ = 2L* (below λ_J), Newtonian control: break at t_b = 1.794 (N = 512) / 1.773 (N = 2048), with J ≥ 0.70 throughout. The γ = 0
  run has J = 0.073 at that time.
- λ = 8L* and 16L* (above λ_J), Newtonian control: the collapse proceeds to J_min 0.20 / 0.11 and then breaks.
- Canonical tether: all four wavelengths break before any J → 0, with J_min 0.38–0.70.

S2 does not define what follows a gradient catastrophe. It needs a kinetic completion (multi-stream) or a dissipative one (a warm
pressure-supported fluid, with no crossing at all).

**Criterion.** Compression at speed v stays adiabatic (no breaking, no crossing) where the Mach number v/c_s < 1. Take
c_s² = 2πG L*² ρ_ph on the law, and v ≤ the baryonic escape speed (the cold medium is bound only by baryons, CFG749). For the deep law
with point-mass baryons this gives

  M² = 4 r_M r / L*²,

so **stiffness suppresses crossing inside r_sub = L*²/(4 r_M)**, not "below L*". The suppression is strongest in the smallest
systems (small r_M).

### 4.5 Unbinding vs S4's "tether-frame binding becomes positive"
**Single-stream energy theorem (K6).** With static baryons and γ = 0, each shell's E_q = ½ṙ² + Φ_b + Π_q is conserved (to 1e-6 or
better before the first crossing). Positive binding therefore needs one of three things:
- (a) a crossing (enclosed mass is redistributed);
- (b) a changing baryon potential (∂ₜΦ_b ≠ 0: gas loss, mergers);
- (c) stiffness work.

N3 confirms (a) is necessary in cold infall: 100% of the mass that ever reaches E > 0 had crossed first. It is not sufficient:
only 44.5% of the crossed mass is unbound at the end (0.43–0.52 across the A2 runs).

**Flat potential (A1).** On the static law the net force vanishes everywhere, so the frozen effective potential is flat:
μ = −(2/3)GM_b/R_e (deep regime, finite edge R_e; numerically −0.01339 vs −0.01333). Any element moving faster than
√((4/3)GM_b/R_e) is unbound in the frozen field. This is CFG749's "orbiting cold energy is unbound", now derived. The co-moving
binding is −(2/3)GM_b/r (numerically 1.006 × that at r > 20).

**Sudden baryon loss.** A medium at rest on the law becomes unbound where the lost fraction exceeds

  **f_crit(x) = 1 − (1 − x)(artanh√x − √x)/x^(3/2)**,   x = u/a0 at the shell,

which is **2/3 in the deep regime** and rises to 1 at high acceleration (K8c–e; table in `cfg939_sym.out`). M4 confirms it bites:
at f = 2/3 − 0.05, 0% of the deep shells are unbound; at 2/3 + 0.05, 100% are.

Unbinding by loss happens **without** any crossing (N4: C2(b) = 0.000–0.014 for f ≥ 0.7). The closed form matches the discrete
shells at t = 0+ exactly (agreement 1.000 at every f). Crossings then move energy around:
- at f = 0.7, 94% of the medium is unbound at t = 0+, but only 29% is still leaving at t = 1500, because crossings re-bind most of it;
- at f = 0.5 and 0.6, nothing is unbound at t = 0+, yet 5–6% ends up leaving through crossings;
- at f ≥ 0.8, all of it leaves.

CFG782 asks a different question, whether the gas *can* be photo-evaporated (V_init < √2 c_s). The derived condition asks whether
the loss unbinds the tethered medium. In S2 + S3 the unbound medium then expands away. That gives a deficit, never a bound free
halo.

### 4.6 S4 class (frozen rules, §4 of the criteria; A1, A2)
- **C1 is BORDERLINE.** In the primary run (dt 0.00125, all 11 K PASS), m/m_law at 5 r_M = 0.949, outside the ±0.05 window by
  0.001, so the frozen label is "UNTETHERED". The first run (dt 0.005, K5c failed) gave 0.966 and TETHERED. The A2 report-only runs
  give 0.958 and 0.956 (TETHERED), and 0.994 at t = 6000 (TETHERED).
  - The shortfall is a filling *deficit*. The tether-off control piles mass to 3.9 × the law at the same radius.
- **C2(a) fails everywhere:** crossing ⇒ E_tf > 0 for 0.43–0.52 of the mass, against the 0.9 bar.
- **C3:** no stream-dependent coupling.
- No subset evolves under the tether-off force law (the force identity holds to 7.8e-13 a0).

→ **Frozen rules at the primary run: no class's conditions hold (unassigned; C1 borderline).** DERIVED is excluded in every run.
On the analytic test C3, and on C1 in 4 of 5 runs, the outcome is **NOT DERIVABLE**. Some partial results are derivable:
- S4's *trigger* can be stated as an equation: own-mass binding E_q > 0 after a baryon-potential change, with threshold f_crit (2/3
  deep), or after ejection in violent relaxation.
- What follows cannot. S4's "stays bound by ordinary gravity, never re-tethers" needs free cold matter that gravitates (−ρΦ) but is
  outside ∇·P. That is CFG888's unwritten coupling, and the single-medium action has no term for it.
- The derivable piece of S4's third bullet ("debris moving through resting cold energy captures none") does follow from the
  tether-frame energetics. Cold energy is bound only by baryons, so a system moving through the settled medium faster than its own
  baryonic escape speed cannot capture it. That puts tidal dwarfs and DF2/DF4 at Newton (§5).

## 5. Consequences: see README (N5 table and alignment grid)

## 6. Energy bookkeeping (T4)
The Lagrangian-map dynamics comes from an action with static baryons, so it conserves energy:
- law control: dE/E 1.3e-15;
- cold infall with full crossing: 1.3e-4 over t = 2000 (1.7e-5 at dt 0.000625), at the leapfrog level.

Settling here is phase mixing plus ejection. In the cold-infall run, 44% of the mass (21.4 of 48.9) leaves on unbound outbound
orbits. It carries kinetic energy 0.54 in units of M_b V_f², against 0.20 left in the bound part, while the bound inner part lands
on the law. The energy released by settling goes to an
explicit escaping receiver. It does not go to a dark-energy partner.

CFG932 Q1's non-conservation is therefore a property of the record's class-A drift law (CFG638, a mobility rule with no potential),
not of S2 + S3. This matches CFG932's own side remark that CFG747's tether dynamics is conservative, and it makes astra's
"specify a receiver" (MASS_LEDGER_REPAIR.md, continuation 2) concrete inside the canonical action: the receiver is the ejected cold
medium.

The cost is the same one CFG776 found. A conservative tether settles only by *expelling*, so it cannot hold a surplus. The excess
family stays unexplained.
