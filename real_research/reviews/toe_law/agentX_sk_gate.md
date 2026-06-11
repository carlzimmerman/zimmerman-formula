# agentX — the Schwinger–Keldysh gate: does a causal, conserving M22 worldline EOM exist?

*agentX, 2026-06-11. Files: `agentX_sk_kernel.py` → `.out` (frequency-domain: banked-number gate, the
Kramers–Kronig completion, the passivity no-go, the flux invoice) and `agentX_sk_dynamics.py` → `.out`
(time-domain: the causal windowed EOM integrated — adiabatic validation against agentM's banked reflex numbers,
pre-acceleration audit, kick transient, Picard/runaway audit, energy-ledger closure). All numbers below are
machine-generated in those two runs; both scripts GATE against agentM's banked values before any new use.
Inputs read first: `agentU_khronon_m22.md` (gap-list item 1 — this gate), `agentM_milgrom2022_gauntlet.md`/
`.py`/`.out` (the M22 functional, Eq. `v`/`shiluta`, θ(1)=1, the banked inventory), `UNIFIED_ACTION_ASSEMBLY.md`
[SLOT-X], `DERIVATION_CHAIN.md` Link 6. Hostile discipline: this is the field's historical death-spot for
covariant MI — every PASS below is scoped, and the obstruction is stated as a theorem, not a vibe. Both a₀
footings + the hostile bath s = cH_Λ wherever a number depends on the footing. No git.*

**STATUS: COMPLETE — both runs banked, verdict final.**

---

## VERDICT UP FRONT

**PARTIAL — with the obstruction finally converted from folklore into a theorem, and the escape route named,
constructed, and priced.** Three sentences before the detail:

1. **A causal (retarded), Galley-consistent M22 EOM EXISTS and is written below** (§2): the doubled-variable
   split of Milgrom's nonlocal kernel goes through, the physical-limit EOM is retarded, it reproduces the
   adiabatic μ(𝓐/a₀) law on quasi-stationary worldlines (validated against agentM's banked reflex numbers to
   0.02–0.03% at the 𝓐-level, δa☉ to ≤1%), it has no pre-acceleration and no runaways (monotone xμ ⟹ unique
   fixed point; damped Picard ≤ 34 iterations across nine decades of a_N), and the energy ledger is
   well-defined with the khronon as the reservoir — total ∇_μT^{μν} = 0 closes on-shell by the doubled-action
   Noether identity (ledger closure verified numerically at 10⁻¹⁴), with the u-field playing a SECOND
   structural role found here: it is the covariant CLOCK the causal memory window requires.
2. **But the reservoir cannot be a healthy field in its vacuum — by theorem, not by failure to find one**
   (§3, Theorem X2): causality + vacuum passivity force μ̂(0) ≥ μ̂(∞) on the linearized response about any
   background (the classic dielectric sum rule), while the deep-MOND limit of ANY modified-inertia theory —
   not just M22 — forces the opposite ordering (slow probes must feel LESS inertia; that IS the MOND
   enhancement). A causal MI theory is therefore irreducibly ACTIVE at the secular channel: the medium must
   do net positive work on slowly-forced worldlines — measured in the time-domain run as exactly the
   (1/μ − 1) co-payment, ×2.58 the external power at x ≈ 0.11. This is the boundary theorem for all
   covariant MI the task pre-registered for the FAIL outcome — it explains in one line why every covariant
   MI attempt has died here.
3. **The gate therefore does not close Link 6's build — it re-derives Link 5 as MANDATORY and hands it an
   invoice:** the matter half graduates to built-at-EOM-level *conditional on a pumped (non-vacuum) reservoir*
   with free-energy throughput ~10³³–10³⁵ W per L*-galaxy (secular-to-transient ceilings). The khronon
   vacuum cannot pay it at all (passivity theorem), and the khronon background cannot either (the PPN-corner
   stockpile drains in 4×10⁶–3×10⁸ yr — short of a Hubble time by ×50–3600); the dS bath (T_dS ≠ 0, the
   Gibbons–Hawking free energy — the framework's own Link 1–3 objects) covers it with ×10²–10⁴ margin at the
   100-kpc-box level and ~15 more orders at the horizon level. Causality alone, pushed through
   Schwinger–Keldysh, lands on the framework's mechanism slot from a direction nobody ordered.

The flux the aether must carry is computed (§5): bounded by the same exponential ε(x) that passed the reflex
— ×14–21 inside the reflex budget even at the hostile footing, ×10¹¹–10¹⁴ at the physical footings, exact
zero (≤10⁻⁴⁷, down to 10⁻³⁷¹²) at every planetary channel — and only the genuinely-aperiodic galactic
channels carry a real invoice. No data-side kill exists; the constraint is structural (which reservoir signs
the check), exactly where agentU's §3 said the open gate lived — now with the sign and the amount filled in.

---

## 0. The gate, the route, the rules

agentU's gap-list item 1 (inherited verbatim from Milgrom's own flagged opens): the time-symmetric
|â(ω)|-built functional has an action and exact conservation but reads the future; the retarded version is
causal but loses the Noether guarantee. The named route (banked, 1712.07066-class): retarded nonlocal EOMs
are causal and consistent when derived in the in-in/Schwinger–Keldysh framework rather than naively varied.
The classical skeleton of in-in is **Galley's nonconservative mechanics** (1210.2745; field/Noether extension
Galley–Tsang–Leibovich 1412.3082). The gate: (1) pin Galley; (2) write M22 in doubled variables and check the
split; (3) check (a) adiabatic reproduction vs banked numbers, (b) pre-acceleration/runaways, (c) total
conservation and reservoir health; (4) verdict.

Working rules: the M22 object is the concrete published class (Eqs. `law` + `mumu` + `v`/`shiluta`, θ(1)=1,
monotone xμ) with the exponential (McGaugh-RAR) μ-tail — the assembly's data-selected member; power-law tails
are carried in the checks only to show which verdicts are tail-independent. Both scripts gate against agentM's
banked numbers before any new use (his .out: 𝓐(Ω_J)/a_J = 1.167/1.177/1.130 across his three θ examples;
exp-tail δa☉ = 1.391/1.133/3.154×10⁻²⁹ fw and 1.267/1.163/1.780×10⁻¹⁶ hostile — all reproduced verbatim,
kernel run §[0]).

---

## 1. Galley pinned (the formalism, exact statements used)

**The doubling (1210.2745).** Degrees of freedom doubled, q → (q₁, q₂); the doubled Lagrangian
> Λ(q₁, q₂) = L(q₁) − L(q₂) + K(q₁, q₂, t),
with K antisymmetric under 1↔2 and vanishing when q₁ = q₂. Convenient variables q₊ = (q₁+q₂)/2,
q₋ = q₁ − q₂. The variational principle: vary q₁,₂ independently with **initial data fixed at t_i and the
EQUALITY conditions q₁(t_f) = q₂(t_f), q̇₁(t_f) = q̇₂(t_f) at t_f** (no final values fixed). This boundary
choice — not the doubling per se — is what breaks the time symmetry of the stationarity problem: advanced
boundary terms cancel, and after the **physical limit (PL)** q₋ → 0, q₊ → q the EOM is
> d/dt(∂L/∂q̇) − ∂L/∂q = Q(t),  Q ≡ [∂K/∂q₋ − d/dt ∂K/∂q̇₋]_PL,
with Q a **retarded** functional of q whenever K couples q₋(t) to functionals of the q₊-history. This is the
classical ħ→0 skeleton of in-in/Schwinger–Keldysh (q₁ = forward branch, q₂ = backward branch; the PL is the
coincidence of branches).

**Energy bookkeeping (1412.3082).** For Λ with no explicit time dependence, time-translation invariance of
the DOUBLED action gives, in the PL, not a conservation law but a **balance law** for the physical energy
E = q̇·∂L/∂q̇ − L:
> dE/dt = Q·q̇  — (X-L1)
i.e. the open (worldline) sector's energy changes at exactly the rate the nonconservative force does work;
the books are well-defined and the deficit is a computable flux, to be carried by whatever sector K
represents. GTL extend this to field theory: when K arises from coupling to a genuine partner field, the
flux lands in that field's stress tensor and TOTAL conservation is restored on-shell. **These two statements
are the entire mechanism of the gate: existence of a retarded EOM from a stationarity principle, and a ledger
that closes onto a named reservoir.** (Both papers pinned from the task brief and the standard form of the
formalism; no new literature claims ride on details beyond the above.)

---

## 2. The M22 functional in doubled variables — the construction

### 2a. What must be doubled, and the split

M22's law, per frequency along the worldline: m μ[𝓐(ω)/a₀] â(ω) = F̂(ω), with
𝓐(ω) = (1/√2π)∫θ(ω′/ω)|â(ω′)|dω′ — built from the **modulus** of the full-worldline Fourier transform:
time-symmetric, future-reading. The acausality is total, not perturbative: on a worldline quiet in the past
and loud in the future, the symmetric 𝓐 assigns the loud inertia to the quiet epoch at **64% of the full
quiet→loud μ-shift** in the dynamics run's geometry (§6b) — there is no small parameter in which the
symmetric form is "approximately causal" on transients.

**The doubled writing.** Take the local sector intact and put the ENTIRE MI piece in K:
> Λ = ½m ż₁² − ½m ż₂² − V(z₁) + V(z₂) + K_MI,
> **K_MI[z₊, z₋] = −m ∫ dt  z₋(t) · R[z₊](t),**  — (X-1)
where R is the **retarded M22 functional**, defined by a causal per-channel estimator (the "windowed
filter bank"): for each frequency channel ω, the demodulated past-windowed component of the acceleration
> â_T(ω; t) ∝ ∫₀^∞ ds  w(s/T_w(ω))  z̈₊(t−s) e^{iω(t−s)},  T_w(ω) = N_cyc · 2π/ω, — (X-2)
(w a normalized strictly-one-sided window; constant-Q: every channel remembers N_cyc of its own cycles —
implemented in the runs as a cascaded two-stage exponential window), the causal spectral measure
𝓐_ret(ω; t) assembled from the |â_T(ω′; t)| exactly per Eq. `shiluta` (own term coefficient θ(1)=1, cross
terms θ(ω′/ω)), and
> R[z₊](t) = Σ_channels ( μ[𝓐_ret(ω; t)/a₀] − 1 ) [z̈₊]_ω(t). — (X-3)
K_MI is exactly the q₋·(functional of q₊) form — Galley's canonical case — and the PL EOM is
> **m z̈ + m Σ_ω (μ[𝓐_ret(ω;t)/a₀] − 1)[z̈]_ω = F  ⟺  m μ∘z̈ = F, retarded.** — (X-4)

**Strictly causal by construction** — every ingredient is a one-sided integral over the past. **Galley split:
PASS at the structural level.** The conservative piece (the part of the kernel even in t−t′ on resolved
spectra) can be moved into L as a time-symmetric nonlocal term; the irreducible K-remainder is the
history-dependent R-functional, which vanishes on exactly-(quasi)periodic pasts longer than the window —
where retarded and symmetric evaluations agree (agentU §3's observation, here made the design principle).

### 2b. The two limits that define correctness

- **T_w → ∞ on quasiperiodic worldlines:** the estimators converge to the exact Fourier data; (X-4) → the
  symmetric M22 law exactly. Everything agentM banked (reflex, precession, SPARC, WB) transfers verbatim,
  since all of it was computed on (quasi)periodic worldlines. Validated at finite window in §6a: the full
  Sun inventory reproduced at N_cyc = 24 to 0.02–0.03% in 𝓐, banked δa☉ to ≤1%.
- **Transients:** the law tracks spectral change with lag ~T_w. During the lag, μ is evaluated on the stale
  spectrum — the response is wrong by O(Δμ) for ~N_cyc cycles, and the energy ledger (X-L1) runs a nonzero
  flux. This is not a bug of the implementation; §3 proves a lag-or-flux of this kind is FORCED on any causal
  version. The transient fingerprint (a freshly-kicked deep-MOND worldline responds with temporarily
  ENHANCED MOND behavior until the window fills — measured ×2.32 response enhancement immediately post-step
  at x: 0.1→1, §6b) is the construction's falsifiable novelty, and it is invisible at high x (μ ≡ 1
  regardless of window state).

### 2c. The covariant doubled action and total conservation

> S_SK = S_EH[g] + S_u[g, T] + Σ_p { S_p[z_p,₊; g, u] − S_p[z_p,₋; g, u] + K_p[z_p,₊, z_p,₋; g, u] }, — (X-5)
with S_p the free point-particle action and K_p the (X-1) functional written in the u-frame: accelerations
are the u-frame kinematic A(s) of agentU §1, frequencies and the window are defined with respect to
**u-proper time s = −∫u_μdz^μ**. Two structural results:

1. **The khronon is the clock the causal memory requires (new, this memo).** A retarded window needs an
   invariant "how long ago"; on a bare metric background no diff-covariant scalar supplies a preferred time
   along the worldline without reintroducing agentC's frame problem at the level of the MEMORY rather than
   the filter. u supplies both at once. A covariant causal M22 without u would have to smuggle in a
   background time function — i.e. the frame field is forced TWICE: once by the filter (agentU), once by
   causality (here). This tightens the assembly's "one frame" interface condition: S_m's window and S_slip
   must read the same u for the conservation argument below to close.
2. **Total conservation closes by the doubled Noether identity.** K_p is built covariantly from (g, u) and
   the doubled worldlines only — no external structure. The doubled action is invariant under common
   diffeomorphisms of all fields; the PL of the resulting identity gives on-shell
   > ∇_μ (T_m^{μν} + T_u^{μν} + T_g-sector^{μν}) = 0,
   with the worldline-sector non-conservation (X-L1) appearing as a SOURCE in the khronon's field equation
   (δK/δT ≠ 0): the aether is the momentum/energy reservoir, exactly the role agentU's gate-2 assigned it on
   faith. The Noether guarantee agentU said was "LOST" at EOM level is RESTORED at doubled-action level —
   conservation is not re-derived by hand; it is automatic, PROVIDED the khronon can lawfully carry the flux
   it is sourced with. That proviso is §3's subject, and it is where the real content of the gate lives.
   (The worldline-side half of the identity — dE/dt = Q·q̇ exactly — is verified numerically in §6c at the
   10⁻¹⁴ level.)

---

## 3. The obstruction, as theorems — why this is the death-spot, exactly

Linearize the retarded law about any background worldline with dominant spectral line Ω and acceleration
content a_c (the diagonal response of a probe/perturbation at frequency ω riding the background):
> μ̂(ω) = μ[𝓐_bg(ω)/a₀],  𝓐_bg(ω) = a_c θ(Ω/ω)  (Eq. `v` with one line), — (X-6)
REAL, and **strictly rising in ω** (sympy, kernel run §[1]: dμ̂/dω = μ′·a_c·θ′-chain > 0 for all three θ
examples): μ̂(ω→0) = μ(a_c θ(∞)/a₀) = μ(0⁺) → 0 (slow probes feel vanishing inertia — the deep-MOND
enhancement, maximal at DC), and μ̂(ω→∞) = μ(θ(0)a_c/a₀) (fast probes feel the θ(0)-quenched, EFE-like
inertia). For the symmetric (acausal) theory this real rising kernel is consistent and conserves energy on
periodic content. For ANY causal version:

**Theorem X1 (rigidity — no causal kernel is exactly the real M22 kernel).** A linear-response kernel that is
(i) causal (analytic in the upper half ω-plane), (ii) bounded with finite μ̂(∞), and (iii) exactly real on the
whole real frequency axis, is CONSTANT (Schwarz reflection ⟹ entire; Liouville ⟹ constant). Hence a causal
M22 must have Im μ̂ ≢ 0: **dissipation or pumping somewhere in frequency is forced — zero net energy exchange
with the reservoir at all frequencies is impossible while μ̂ varies.** The only freedoms are WHERE the
spectral weight Im μ̂ sits (it can be parked away from a quasiperiodic worldline's discrete lines — the
adaptive escape realized by (X-2)'s spectrum-resolving window; on continuum/transient content it cannot be
parked anywhere) and WHICH SIGN it carries. Pick two of {causal, flux-free, frequency-dependent inertia}:
the symmetric M22 picks (flux-free, ω-dependent); the SK construction picks (causal, ω-dependent) and pays
flux on unresolved content. This is agentU's "violation channel ∝ [ε(x)] × [aperiodicity]" DERIVED rather
than estimated.

**Theorem X2 (the passivity sum rule — the reservoir cannot be a vacuum).** Suppose the reservoir is a
healthy field in its ground state, so the response is PASSIVE: the medium can only absorb. In the
convention pinned numerically by a damped-oscillator reference (kernel run §[2]: time-domain ⟨P_medium⟩ =
−0.120 < 0 with analytic Im μ̂ = +0.240 > 0), passivity ⟺ Im μ̂(ω) ≥ 0 for ω > 0. With the unsubtracted
dispersion relation for μ̂ − μ̂(∞) (decay O(Ω/ω), checked for (X-6); verified symbolically on the reference:
(2/π)∫Im μ̂/λ dλ = gτ = μ̂(0) − μ̂(∞) exactly):
> μ̂(0) = μ̂(∞) + (2/π) ∫₀^∞ Im μ̂(λ) dλ/λ  ≥  μ̂(∞)  — (X-7)
— the classic dielectric ordering ε_static ≥ ε_∞: **a passive causal medium's DC response cannot sit BELOW
its high-frequency response.** M22 requires exactly the inverted ordering, μ̂(0) ≈ 0 < μ̂(∞), about every
deep-MOND background — and not as an artifact of the filter: the deep-MOND limit 𝓘 → 𝓐/a₀ is forced by
scale invariance in ANY modified-inertia theory (Milgrom's Eq. `limba`), so vanishing low-frequency inertia
about low-acceleration backgrounds is the CLASS property, not a θ-choice. Therefore:
> **No causal modified-inertia dynamics with the deep-MOND limit can be closed by a passive (vacuum)
> reservoir. The low-frequency/secular channel is irreducibly ACTIVE: the medium must do net positive work
> on slowly-forced worldlines.**
Elementary cross-check, no formalism: pull a deep-MOND particle with a small steady force F. It accelerates
at a = F/(mμ) > F/m; the external agent supplies F·v; the kinetic-energy rate is F·v/μ. The medium supplies
(1/μ − 1)F·v > 0 — ×3.99 the external power at x = 0.05, ×1.89 at x = 0.18 (the WB deep bin), ×0.58 at
x = 1 (exp tail; kernel run §[1]) — and the self-consistent time-domain run reproduces exactly this
co-payment on a secular ramp (§6c-iv: measured P_æ/P_F = 2.579 = (1/μ−1) at the run's x = 0.107, with
P_æ > 0 at every step). The MOND boost is an energy-delivering response. The symmetric form hides this by
netting the future against the past (its conserved E is a nonlocal-in-time charge); the causal form must
pay in real time.

**Corollary (the invoice).** The doubled-action conservation proof of §2c is intact — but it sources the
khronon with an ACTIVE-sign flux at secular channels. A canonical khronon in its adiabatic vacuum is a
passive absorber (its linear response about the cosmological solution is ghost-free and damped by
construction — that was agentU's gate 1); it can carry energy AWAY (the absorb side of the ledger is
unconditionally healthy) but cannot SUPPLY coherent energy without being in a non-vacuum state. So exactly
one of: (a) the khronon sector is pumped — it is the local agent of a reservoir with free energy (the dS
bath at T_dS = ħH_Λ/2πk_B; budget computed in §5 — the framework's Link 1–3 objects, and the repo's Link 5
"amplitude source outside any fraction-limited carrier's budget", re-derived here from causality +
passivity alone); or (b) the khronon has active/ghost-sign modes (DEAD by agentU's gate 1 — not available);
or (c) covariant MI is dead. **The gate's outcome is that (a) is the only open door, and it is the door the
framework's mechanism slot already pointed at.**

*Scope and honesty of the theorems:* X1/X2 are statements about the LTI diagonal linearization about a fixed
background, valid on bands where the background is stationary over ≫ the resolution time; the adaptive
construction evades X1's bite exactly where spectra are discrete and resolved (that is its design), and
nothing evades X2's DC ordering — the secular channel is populated by every real system's slow drift, and
the windowed filter assigns it vanishing inertia by the same θ(∞) = 0 that makes M22's EFE one-directional.
The unsubtracted dispersion relation needs μ̂(ω) − μ̂(∞) → 0 (true for (X-6): θ(Ω/ω) − θ(0) = O(Ω/ω));
subtractions weaken (X-7) to a local statement but do not change the sign conclusion at the DC end. The
cross-channel (off-diagonal, parametric) response μ′·δ𝓐·â_bg modifies the background line, not the probe
channel, and does not rescue the ordering. The X2 class extension rides on Milgrom's Eq. `limba` (scale
invariance) plus the diagonal-kernel reading — an MI theory that somehow evades the diagonal linearization
on secular content evades the theorem, but it would also evade being MOND (the secular enhancement IS the
phenomenon, cf. the elementary check).

---

## 4. The numbers — kernel script (`agentX_sk_kernel.py` → `.out`)

### 4a. §0 gate vs banked agentM numbers: **PASS verbatim**
Inventory rebuilt to agentM's conventions (8 planetary lines + galactic line, Eq. `shiluta`, θ(1)=1):
𝓐(Ω_J)/a_J = **1.167 / 1.177 / 1.130**; exp-tail δa☉ fw **1.391/1.133/3.154e-29**, hostile
**1.267/1.163/1.780e-16** — every figure inside agentM's banked rows to print precision. The machinery is
certified before any new use.

### 4b. The KK completion of the M22 kernel: forced Im, signs, and where it can hide
Machinery validated first on an analytic causal reference (exp-memory kernel): Re reproduced to 2.2e-16,
Im recovered to 4.8e-4 of scale, sign convention pinned. Then the M22 kernel (X-6), deep-MOND backgrounds
x_c ∈ {0.05, 0.18, 1.0}, three θ's, exponential μ:
- The symmetric kernel's inverse transform puts **exactly 50.0% of its L¹ mass at τ < 0** (even symmetry —
  the future and past weighted identically; maximal, not perturbative, acausality).
- The minimal causal completion (causalize χ → 2θ(τ)χ; Re preserved to ≤2.8e-16) forces **|Im μ̂| of the
  same order as the kernel itself**, and — the numerics overruling this memo's first-draft guess of mixed
  signs — **ACTIVE at BOTH flat-curve epicyclic sidebands, at every x_c and θ tested**: at x_c = 0.18,
  θ = 2/(1+y²): Im μ̂((√2−1)Ω) = −0.181, Im μ̂((√2+1)Ω) = −0.092, i.e. |Im/Re| = **0.88 / 0.22 per radian**
  (across the grid: 0.55–1.24 at the lower sideband, 0.13–0.30 at the upper). At the DC end (x_c = 0.18,
  θ_A): Re/Im = +0.006/−0.019 at ω = 0.01Ω, +0.029/−0.062 at 0.05Ω, +0.058/−0.098 at 0.10Ω — **|Im| > Re:
  the secular channel of the minimal completion is overwhelmingly active.**
- Consequence stated plainly: a FIXED (non-adaptive) causal kernel with the M22 shape PUMPS epicyclic
  perturbations at O(0.1–1)/radian in deep MOND — disks blow up in ~1–2 orbits. **A fixed causal kernel is
  phenomenologically dead on arrival; only the spectrum-resolving adaptive construction (X-2) survives,**
  parking the spectral weight off the populated lines (verified dynamically in §6c: residual flux → 0 as
  N_cyc⁻¹·⁰⁰ on resolved spectra). This is the quantitative reason the causal EOM must be adaptive —
  Milgrom's "inertia as an acquired attribute … from the ambient medium" made mechanical: the medium must
  resolve the worldline's spectrum over many beats.
- Passivity interpolation no-go (NNLS over positive spectral measure vs signed least squares, grid-collision
  guarded): positive measure CANNOT reproduce the M22 kernel shape once the DC point is included — NNLS
  residual **92.7% of the target norm** (vs **7.2e-13** for a signed measure); at the DC point the target is
  −0.451 while the best passive fit is +0.115. Theorem X2 confirmed constructively.

### 4c. The active-power ledger at the elementary level
(1/μ_exp − 1) at x = 0.05 / 0.18 / 1.0 = **×3.99 / ×1.89 / ×0.58** of the external power — the medium's
mandatory co-payment on secular forcing in deep MOND (cross-checked to 1e-6 by the §6c-iv self-consistent
run). At precision-system x (the Sun-wobble inventory, x = 436–2629 across footings): ε = 5.6–8.5e-10
(hostile) down to 5.4e-23–1.5e-22 (fw) — the SAME exponential ε(x) that passed the reflex bounds every flux
observable.

### 4d. Solar-system flux check: **no new kill channel**
The KK-forced |Im μ̂| about the Sun's worldline is bounded by the kernel's total variation ~ ε(x): per-radian
damping/pumping of the wobble ≤ ε/π; driven-response amplitude/phase shifts ≤ ε vs the reflex budget's
1.18e-8 wobble fraction —
- exp tail: hostile **×14–22 inside budget** (ε = 5.6–8.5e-10); canon ×2.2–5.5e11; fw ×0.8–2.2e14. PASS
  at all footings.
- power-law tail: ε_std(hostile x) = 2.43–2.63e-6 → **×205–222 OVER** the same line — numerically identical
  to agentM's hostile reflex ratios (as it must be: δa☉/a_J ≡ ε; an internal consistency echo, not a new
  kill). The kill ordering is preserved; nothing new dies here, nothing dead revives.
- the planetary channels themselves (the bodies' own x = GM☉/R²/a₀, hostile): ε_exp from **10⁻³⁷¹²**
  (Mercury) to **10⁻⁴⁸** (Neptune) — exactly zero at any conceivable precision. (First-draft bug: this
  block initially reused the Sun-wobble line amplitudes; caught and corrected — bug log.)

---

## 5. The flux invoice and the reservoir (kernel run §[5])

The ledger rate (X-L1) per worldline, in channel form: P_æ = −Σ_ω m (μ−1)[z̈]_ω·ż — zero on resolved
quasiperiodic content (the conservative piece), nonzero ∝ unresolved/secular content, ACTIVE sign (X2)
wherever deep-MOND enhancement operates on secular forcing.

| system class | x = 𝓐/a₀ | ε(x) (exp tail) | flux scale | observable? |
|---|---|---|---|---|
| Sun wobble | 436–2629 | 8.5e-10 (hostile) … 5.4e-23 (fw) | fractional wobble shift ≤ ε | NO — ×14–22 inside the reflex budget hostile; ×10¹¹–10¹⁴ at physical footings |
| planetary orbits | 1.2e4–7.3e7 (hostile) | ≤ 10⁻⁴⁸ | exactly 0 | NO — channel empty |
| wide binaries | ~0.2–2 | 0.3–0.8 | ε × (unresolved fraction); ∝ N_cyc⁻¹ on resolved spectra | NO — far below DR-class statistics |
| galactic disk stars (quasi-stationary) | ~0.1–1 | O(1) | ~0 on resolved spectrum; transients pay ~1% of external work per event (§6c-iii) | NO secular drain; epicyclic channel protected by adaptivity |
| structure formation / mergers (genuine transients + secular drift) | ≪1 | O(1) | **2.3e33 W (t_H-paced) to 1.6e35 W (t_dyn-paced) per L*-galaxy** (ceiling: ε·M*v²/2 per pace time) | not directly; enters the reservoir budget below |

**Who can pay (the §3 corollary, priced):**
- **Khronon vacuum: CANNOT (theorem).** Passive absorber only — the active channel is off-limits at any
  coupling. (Absorb-side entries — damping flows worldline → aether — are unconditionally healthy.)
- **Khronon background as a stockpile:** ρ_u c² ~ α M_Pl²H²c² at the PPN generic corner (α ≲ 8e-7):
  6.6e-16 J/m³ → **1.95e49 J** per (100 kpc)³ — drained in **2.7e8 yr** at the secular ceiling
  (t_H × 0.020) and **3.9e6 yr** at the transient ceiling (t_H × 2.8e-4): **short by ×50–3600. The frame
  field cannot also be the battery.**
- **The Λ/dS reservoir:** ρ_Λc² = 5.7e-10 J/m³ → **1.68e55 J** per box — covers the secular ceiling for
  **×1.7e4 t_H** and the transient ceiling for ×242 t_H; the Gibbons–Hawking horizon scale c⁵/(GH) =
  **1.60e70 J** clears the per-galaxy bill by ~15 more orders. **The dS bath can pay the MI bill everywhere
  and always; what causality leaves open is the COUPLING — which is verbatim Link 5's open mechanism.**

---

## 6. The dynamics — time-domain script (`agentX_sk_dynamics.py` → `.out`)

### 6a. Adiabatic reproduction on the quasi-stationary worldline (check 3a): **PASS**
The full causal pipeline (X-2)–(X-3) run on the synthetic Sun-inventory worldline (7.36M steps, dt = 1.37 d,
27.7 kyr span, N_cyc = 24, cascaded two-stage windows): per-line amplitude recovery ≤0.01% for all
converged channels (Neptune −0.88%, the two-stage burn-in residual at 7 windows);
**𝓐_ret(Ω_J)/a_J = 1.167/1.177/1.130 — drift from banked 0.02–0.03%**; exp-tail δa☉ (hostile) =
1.267/1.163/1.780e-16 — **banked values to print precision**, despite the ×11 error amplification of the
exponential tail (dln ε/dln 𝓐 = −√x/2). The retarded estimator reproduces the adiabatic (symmetric-form)
filter on quasi-stationary worldlines at the sub-percent level — check 3a closed.

### 6b. Pre-acceleration audit (check 3b): **retarded clean; symmetric maximally acausal; the fingerprint**
Quiet→loud worldline (x: 0.1 → 1.0 at t = 0): the SYMMETRIC Fourier-modulus form assigns the pre-onset epoch
μ_sym = 0.502 vs μ_quiet = 0.271 — **a pre-response at 64% of the full quiet→loud shift, before the force
changes** (and decaying only as the loud epoch's window share — no exponential protection). The RETARDED
estimator's pre-onset deviation is 1.0e-2 = the window ripple (bound 1/(2πN_cyc) = 2.0e-2), i.e. **zero
future response**; post-onset, the stale window gives a transient response enhancement μ_loud/μ_ret = **2.32**
decaying with half-life 1.2 cycles (0.15 N_cyc — μ's steep small-𝓐 rise front-loads the recovery; full
refill ~N_cyc). ALD comparison: the M22 law is second-order plus memory — no third derivative exists at any
stage, so the ALD runaway/pre-acceleration disease and its order-reduction cure have no analog here; the
analog risk (implicit-μ multivaluedness) is closed in §6c by monotone xμ.

### 6c. Runaways, self-consistent integration, ledger, flux scaling (check 3c): **all clean**
- **Uniqueness/runaway:** xμ(x) strictly monotone over [1e-9, 1e9] for both tails ⟹ exactly one root for
  any a_N; damped Picard converges to 1e-12 in ≤34 iterations across a_N ∈ [1e-6, 1e3]. No runaway, no
  multi-root, uniform convergence.
- **3c-i single line (deep MOND, x ≈ 0.18):** integrated causal EOM converges to the algebraic M22
  amplitude within 0.2% at every window depth; **ledger E_kin − ∫F·v − ∫P_æ closed to 1.7e-14–7.1e-14**
  (exact discrete identity — the X-L1 balance law verified); steady residual flux ⟨P_æ⟩/⟨|P_F|⟩ = 5.3e-2 →
  6.7e-3 from N_cyc = 4 → 32, **scaling N_cyc⁻¹·⁰⁰** — the park-in-the-gaps mechanism measured: resolved
  spectrum ⟹ conservative, the residual is window ripple vanishing with memory depth.
- **3c-ii two incommensurate lines (ω = 1, √5):** flux 3.1e-3 (N_cyc = 8) → 2.2e-3 (N_cyc = 24); ledger
  ≤3.4e-14; both channel μ's settle to their shiluta values. (The two-line residual falls slower than the
  single-line N⁻¹ in this estimator — beat-frequency ripple partially survives the averaging window;
  reported as measured.)
- **3c-iii kick (drive ×3 at fixed t):** the transient deposits ∫P_æ dt = +4.5e-2 — **0.9% of the external
  work in the 40-cycle window, ACTIVE sign (reservoir → worldline)** while the window refills, then the flux
  returns to the ripple floor. The transient invoice is real, small, and one-way per event.
- **3c-iv DC/secular forcing (Theorem X2 made flesh):** constant force on a quiet worldline, implicit
  per-step solve (own term in its own window, θ(1) = 1): the self-consistent trajectory converges to the
  algebraic MOND value a·μ(a) = F_dc to +0.01%; the medium's measured co-payment **P_æ/P_F = 2.579 =
  (1/μ−1) exactly** (kernel-script cross-check PASS to 1e-6), **P_æ > 0 at every step of the secular ramp**.
  The active channel is real, finite (self-limited by the nonlinearity), and exactly the X2 co-payment. A
  vacuum reservoir cannot supply it; the pumped (dS-bath-class) reservoir of §5 must.

---

## 7. VERDICT (the four pre-registered outcomes adjudicated)

**PARTIAL — and the partial is load-bearing in both directions.**

1. **NOT GATE-FAILS clean:** the historical obstruction (causality/conservation) is NOT fatal. The Galley/SK
   doubling delivers a retarded EOM from a stationarity principle (X-1)–(X-4); the doubled Noether identity
   closes total ∇_μT^{μν} = 0 onto the khronon (§2c, ledger verified at 10⁻¹⁴); the adaptive u-clocked
   window evades the X1 rigidity exactly where the phenomenology lives (banked numbers reproduced to
   0.02–0.03%); there is no pre-acceleration (vs the symmetric form's 64%-strength future-reading) and no
   runaway (monotone xμ, Picard ≤34); the flux is confined to ε(x) × aperiodicity — zero at every precision
   system (×14–22 inside the reflex budget even hostile; ≤10⁻⁴⁸ planetary), ~1% of external work per
   galactic transient event.
2. **NOT GATE-PASSES clean:** a causal conserving M22 EOM exists ONLY with a pumped reservoir. **Theorem X2
   (the passivity sum rule, μ̂(0) ≥ μ̂(∞) for any causal kernel with a vacuum reservoir) excludes the
   vacuum-khronon version outright — and that IS the pre-registered boundary theorem for ALL covariant MI:**
   any modified-inertia theory with the scale-invariant deep-MOND limit (any filter, any tail) requires its
   low-frequency response to sit BELOW its high-frequency response about deep-MOND backgrounds, which is
   active behavior no passive medium can supply. Confirmed three independent ways: the dispersion-relation
   sum rule (symbolic), the NNLS interpolation no-go (92.7% residual vs 7e-13 signed), and the
   self-consistent time-domain co-payment (P_æ/P_F = 1/μ−1 > 0, measured). This is why the field died here:
   {causal, conservative-with-a-healthy-vacuum, MOND-enhancing} is a forbidden triangle.
3. **The named restrictions (the PARTIAL's content):** (R1) the memory window must be u-clocked and
   spectrum-resolving (N_cyc ≫ 1 in u-proper time — the khronon's second structural role, found here); a
   fixed causal kernel is dead on arrival (epicyclic pumping at 0.1–1/radian, §4b). (R2) the reservoir must
   be non-vacuum: the khronon is carrier and clock, NOT battery (its corner stockpile is ×50–3600 short);
   the dS bath pays with ×10²–10⁴ margin (box) and ~15 further orders (horizon). (R3) on genuine transients
   the law runs a computable ACTIVE flux (~1% of external work per kick event) and a transient-MOND-boost
   fingerprint (×2.3 response enhancement for ~N_cyc cycles at deep-MOND x, invisible at high x) —
   falsifiable in principle, unconstrained by current data.
4. **Chain bookkeeping (proposed SLOT-X fill):** *Link 6's covariant home moves from BUILDABLE to
   BUILT-AT-EOM-LEVEL, conditional on the Link-5 reservoir. The causal conserving EOM exists (Galley/SK
   doubling, u-clocked adaptive window, khronon ledger; agentX (X-1)–(X-5), validated against agentM's
   banked battery); the vacuum-khronon version is excluded by the passivity sum-rule theorem (X2) — the
   boundary theorem for all covariant MI — so Links 5 and 6 are now PROVABLY one problem: the mechanism must
   supply active-sign response at sub-orbital frequencies with free-energy throughput ~10³³–10³⁵ W per
   L*-galaxy, available in the dS bath with orders to spare, unavailable anywhere else in the action.*
   The TOE claim's gating is unchanged: Link 5 (now with an invoice and a sign) and Link 8 remain open.

**Both-ways honesty.** The framework-favorable reading: the field's death-spot is cleared at the price of a
reservoir the framework independently predicted (the dS bath of Links 1–3), and the SK analysis produces a
new falsifiable fingerprint plus a second structural necessity for the khronon. The hostile reading, equal
weight: "built-at-EOM-level" is conditional on physics that does not exist in the action yet — the pump
coupling is exactly as unwritten as Link 5's mechanism was this morning; the adaptive window introduces a
new dimensionless choice (N_cyc) that nothing yet fixes; the X2 theorem cuts BOTH ways — it legitimizes the
dS-bath necessity only if one already accepts MOND-as-inertia, and read cold it says this class of theory
cannot be closed by any conventional healthy field sector. Nothing here derives Z, a₀, or the exponential
tail; the construction CONSUMES all three.

---

*Bug log (all caught in-run, none result-bearing in the banked outputs): (i) kernel [3] first run — an
NNLS design-matrix near-collision (λ ≈ ω node) plus Apple-Silicon Accelerate BLAS raising SPURIOUS
divide/overflow flags on perfectly finite matmuls; fixed with a grid-collision guard (1 node dropped,
min relative gap 1.2e-3), the spurious flags verified harmless (products explicitly finite) and silenced
locally with post-checks. (ii) kernel [4] first draft computed the "planetary channels" from the Sun-wobble
line amplitudes instead of the bodies' own GM☉/R²; corrected (the wrong version showed Saturn x ≈ 34 —
the wobble line — instead of 1.2e5). (iii) dynamics [0] first draft: span = 4 Jupiter windows left the
outer channels unconverged (−26% to −53%); fixed to 7 Neptune windows. Endpoint |y| sampling rode the
crosstalk ripple (−16% Mercury); replaced with a final-window time average. Single-stage EWMA Lorentzian
skirts let Jupiter leak +145% into the Mars channel; replaced with cascaded two-stage demodulators
(1/(TΔω)² skirts) — final per-line errors ≤0.01% (Neptune 0.88%). (iv) dynamics [1] first draft: the
burn-in mask exceeded the pre-onset span (empty-array max); audit geometry fixed (N_cyc = 8, 80-cycle
pre-span). (v) dynamics [3] first draft: the ledger compared pre-step E_kin against through-step work —
a spurious one-step 3% "non-closure"; post-step pairing restores the exact discrete identity (1e-14).
(vi) this memo's §4b first draft guessed "active below the line, passive above" for the KK signs; the
machine answer is ACTIVE at both sidebands — the draft guess is recorded and replaced, per house rule.*

## Citations (arXiv ids, role)

| id | role |
|---|---|
| 1210.2745 | Galley — nonconservative classical mechanics: doubling, PL, retarded EOM from stationarity |
| 1412.3082 | Galley–Tsang–Leibovich — stationary nonconservative action; Noether/energy balance; field theory |
| 1712.07066 | Belgacem–Dirian–Foffa–Maggiore — retarded nonlocal EOMs causal/consistent in in-in (banked route precedent) |
| 2208.07073 | Milgrom 2022 — the functional being causalized (via agentM's pinned source) |
| astro-ph/9303012 | Milgrom 1994 — nonlocality license; the deep-MOND limit's scale-invariance forcing used in X2's class extension |
