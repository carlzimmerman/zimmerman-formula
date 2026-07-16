# Lane A — The Closure / Ordering Map

**Question (verbatim from the task).** Beyond the first moment, the map from the nonlocal operator
$K(\Box_u/a_0^2)$ to worldline dynamics is $O(1)$ free (the RB lane killed the *literal-frequency*
closure: no MOND + a fatal secular drift $a_0/2c$; only the first-moment *family* survives, ring-exact
but off-circular-undetermined). Can that map be **pinned uniquely** — or reduced to finitely many
constants — by imposing **simultaneously** (a) Herglotz analyticity + the sum rule
$\int d\mu/|t|=1$, (b) causal-retardedness, (c) KMS/detailed-balance at the dS temperature,
(d) descent from a **well-posed action**, (e) $c_T=1$ and Cassini safety? For each principle, what
exactly is forced. If pinned: the forced off-circular numbers. If free: the exact residual.

**One-line answer.** The map is **partially pinned, not free and not unique**. The nonlocal *operator*
is pinned to a unique measure with its only scale $a_0$; the *circular* reduction is forced (ring-exact
RAR); requirement (d) additionally **removes the corner-location freedom** the prior SPEC left open. What
irreducibly survives is **one reduction-weighting degree of freedom** — how the finite horizon-memory
weights the orbit *history* — equivalently one function $\eta(\beta)$ on orbit-shape space whose **sign
is forced** (MG-impossible) and whose **magnitude is bracketed, not pinned**. This is the honest boundary
of the field theory's off-circular predictivity.

All claims below are machine-checked in `closure_map.py` (exit 0, 22 checks, no hard-coded booleans;
output `closure_map.out`). Both $a_0$ footings carried: $a_0=9.36\times10^{-11}$ (canonical, $\rho_{\rm DE}$)
and $1.13\times10^{-10}$ (alt, $\rho_{\rm tot}/cH_0$).

---

## 0. The object and the precise locus of the ambiguity

The MI content of the baseline action (`BASELINE_ACTION.md` §1) is
$$S_{\rm matter}=-\tfrac12\!\int\!\sqrt{-g}\,\rho_m\big[\,s\,u^\mu K(\Box_u/a_0^2)u_\mu\,\big],\qquad
K(z)=\frac{\sqrt{1+4z}-1}{2\sqrt z},\quad \Box_u f=(u\!\cdot\!\nabla)^2 f,\quad s=-1.$$

Two facts locate the ambiguity precisely:

- **The nonlocal *operator* is unambiguous** once the boundary condition is retarded. $K$ is
  Herglotz–Nevanlinna with a **unique** positive measure; $\Box_u=(u\!\cdot\!\nabla)^2$ is the along-$u$
  second proper-time derivative. There is no operator-ordering freedom in $K(\Box_u)$ itself.
- **The ambiguity is entirely in the *reduction* to a *local* worldline dressing** $\mu(|a|)$. On a
  general worldline the contraction $u^\mu K(\Box_u)u_\mu$ is a memory integral over the $|a|(\tau)$
  history; collapsing it to an algebraic $\mu(|a|)$ is an approximation whose off-stationary form is
  what "the closure map" names.

Why the reduction cannot be pinned by moment-matching: the moment tower does **not** collapse. The
first moment is worldline-general, $u_\mu\Box_u u^\mu=-|a|^2$ (re-derived here from $u\!\cdot\!u=-1$ and
metric compatibility alone), but the **second** moment on a non-stationary worldline gives
$u\!\cdot\!\Box_u^2 u/[(|a|^2)^2(u\!\cdot\!u)]\neq 1$ identically (`closure_map.py` (d.2); the boosted
worldline check yields a ratio that is not $1$, matching the banked $n{=}2$ ratio $1-1/v^2$ that diverges
as $v\to0$). So **no finite moment expansion pins the local dressing off-stationary** — the residual is
genuine, not an artifact of a lazy truncation.

---

## 1. What each principle forces (the decision procedure)

| Principle | What it **forces** | Pins the map? |
|---|---|---|
| **(a) Herglotz + $\int d\mu/|t|=1$** | (i) DC inertia normalization $K(\infty)-K(0)=1$ (region B $=2/\pi$ exact, total $=1$). (ii) The response on the whole oscillatory branch is a **pure phase**, $\lvert K(-w^2+i0)\rvert=1$ exactly for $w\ge\tfrac12$ — **no amplitude MOND from any orbital frequency**. (iii) The measure is **unique** (identity theorem, given the RAR calibration on $z>0$): the kernel and its **only** scale $a_0$ are fixed. | **Pins the operator.** Kernel + measure + scale unique. Does *not* by itself pin the local reduction. |
| **(b) Causal-retarded** | The retarded BC (poles in the lower half-plane) fixes the **sign of the phase lag** ($\sin\phi=1/2w>0$, lag not lead → dissipation for a passive bath). But a KK-causal single-corner kernel exists for **every** $\omega_c>0$: causality is **corner-blind**. | Fixes a sign. **Corner-location-blind** → does not pin. |
| **(c) KMS at $T_{\rm dS}=H_\Lambda/2\pi$** | The fluctuation–dissipation ratio $\coth(\pi w/H_\Lambda)$ and the $\pm$-frequency tie of the dS bath; nearest Matsubara pole at $\kappa=H_\Lambda$ (horizon), **not** any orbital scale. It is **corner-independent** and does **not** source the MOND sign (that stays $s=-1$). | **Consistency, not a pin.** Corner-blind. |
| **(d) Descent from a well-posed action** | The action carries **one** scale, $a_0$; $\Box_u/a_0^2$ places the corner at $\omega_c=a_0/2c$, memory time $\tau_{\rm mem}=2c/a_0=203$ Gyr (canonical) / $168$ Gyr (alt) — **longer than the Hubble time**. Any *orbital*-scale corner (the Milgrom-1994 averaging bandwidth) is a **new scale absent from $S$**; for every bound system $\omega_{\rm orbit}/\omega_c({\rm action})\gtrsim10^6$. **Requiring descent from $S$ rejects the orbital-corner family.** | **The discriminator.** Forces corner $=a_0$; kills the SPEC's corner-*location* freedom. Does *not* resolve the local-reduction weighting (moment tower uncontrolled). |
| **(e) $c_T=1$ + Cassini** | Satisfied by the **whole** surviving family: MI lives in $S_{\rm matter}$, the graviton kinetic term is pure $S_{\rm EH}$ and $\Box_u$ is transverse-blind ($c_T=1$); deep-Newton $\nu-1=a_0/2g\sim7\times10^{-7}$ at Saturn. | **Family-wide consistency.** Zero discriminating power between closures. |

**Net.** (a) pins the operator; (d) additionally pins the corner *location* to $a_0$ (this is the new
result over the prior `mi_offcircular_completion_SPEC.py`, which left the corner among three candidate
scales). (b), (c), (e) are consistency/sign/bound conditions that are **corner- and closure-blind**.
None of the five, alone or together, pins the local-reduction weighting off-stationary.

---

## 2. What is therefore PINNED (forced numbers)

1. **The operator, its measure, its scale.** Unique; only scale $a_0$; $\tau_{\rm mem}=2c/a_0$ exceeds
   the Hubble time in **both** footings.
2. **The AC/orbital sector is passed as pure phase** ($\lvert K\rvert=1$) — the actual orbital
   oscillation is essentially unmodified; MOND lives entirely in the DC/secular sector.
3. **The stationary (circular, constant-$|a|$) reduction is exact and forced** = the ring-exact RAR
   $g_{\rm obs}=\nu(y)g_{\rm bar}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$, both footings. No freedom on circles.
4. **The sign and qualitative pattern of the off-circular offset are forced.** Dispersion-supported
   **isotropic** systems sit **on-or-below** the rotation RAR; **radially-anisotropic** systems are
   pushed **up/hotter** (rms $|a|$ rises monotonically with eccentricity → $d\ln\eta/d\beta>0$, verified).
   The offset is **anisotropy-correlated**. MG-with-the-same-$\nu$ gives **exactly 0 and zero
   anisotropy-dependence** for an isolated spherical system → **this pattern is MG-impossible**.
5. **The secular scale** $2c/a_0=203/168$ Gyr, universal and orbit-independent; the conservative
   wide-binary/galactic split at fixed $a=a_0$ is forced to $\sim3\times10^{-8}$ (footing-independent).

---

## 3. What stays FREE — the exact residual freedom

**One reduction-weighting degree of freedom.** How the finite horizon-memory weights the orbit
*history*, interpolating the two endpoints:

- **Closure A (instantaneous $|a|$):** pointwise-algebraic; dispersion systems sit **exactly** on the
  rotation RAR (offset $0$, verified to $4\times10^{-14}$ over 6 decades). Identical to MG-same-$\nu$ in
  spherical symmetry.
- **Closure B (orbit-history-averaged $\langle|a|^2\rangle$):** the signed, anisotropy-correlated
  pattern. Near-circular epicyclic offset $\Delta\ln g_{\rm obs}=-(d\ln\mu/d\ln x)\,\tfrac{C}{2}\,\epsilon^2$
  with $C=\beta(2\beta+1)/2$ (exact, sympy), **strictly negative** for every $\epsilon>0$ (isotropic);
  deep-MOND coefficient $-0.326\,\epsilon^2$ dex. Isotropic ensemble mean $\sim-0.02$ to $-0.05$ dex
  (deep regime, footing-stable $\sim10$–$15\%$), with the radial tail flipping positive (pericentre
  kinetic pump — the published $\sigma$-hysteresis direction).

Equivalently: **one free function $\eta(\beta)$** on the 2-D orbit-shape space (eccentricity ×
anisotropy). Its **sign is forced** (§2.4); its **magnitude is bracketed**, $[\,0\ (\text{A})\ \dots\
\text{B's signed pattern}\,]$, not a point.

**Physical steer, not a theorem.** The action's memory ($\tau_{\rm mem}>$ Hubble time $\gg$ orbital
period) means the DC inertia integrates the orbit *history* — physically favoring the orbit-averaged end
(closure **B**). But because the moment tower is uncontrolled, this is a physical-regime argument, not a
derivation; the honest deliverable is the **bracket**.

**What would close it.** The off-circular dS-Unruh **Wightman pullback** on a *non-uniform* worldline
(`mi_offcircular_completion_SPEC.py` Stage 4) would fix the finite-memory retention and collapse the
bracket to a point — its honest prior is that the pole structure stays at $\kappa/$above-band (FREE
stands). Alternatively an **empirical proxy** (dwarf $\sigma$-hysteresis amplitude, or the cluster
$\eta(\beta)$ slope) **measures** the retention rather than deriving it. Neither is done here.

---

## 4. The one clean falsifier (both-ways)

A **confirmed frequency-split RAR at fixed $g_{\rm bar}$** — same $g_{\rm bar}$, orbital frequency
differing by $>2$ dex, $\nu$ differing by $>\!\sim\!10^{-7}$ — kills the published kernel outright: the
unique measure leaves **no** freedom to absorb it (the forced conservative split is $\sim3\times10^{-8}$).
This is the sharp edge where the pinned part of the map is exposed to data.

---

## 5. Ledger (DERIVED vs POSTULATED, this lane)

| # | Statement | Status |
|---|---|---|
| C-D1 | Operator/measure unique; only scale $a_0$; corner $=$ horizon; $\tau_{\rm mem}>$ Hubble time | **DERIVED** (a)+(d) |
| C-D2 | AC sector pure phase $\lvert K\rvert=1$; no amplitude MOND from orbital frequency | **DERIVED** (a) |
| C-D3 | Circular reduction exact = ring RAR, both footings | **DERIVED** (first-moment identity) |
| C-D4 | Corner-location freedom removed (orbital corner rejected as non-action) | **DERIVED** (d) — *new over SPEC* |
| C-D5 | Off-circular offset sign + anisotropy-correlation forced; MG-impossible | **DERIVED** (positivity + amplitude functional) |
| C-P1 | The reduction-weighting DOF (A↔B); equivalently $\eta(\beta)$ magnitude | **FREE, bracketed** (moment tower uncontrolled) |
| C-P2 | $s=-1$ (owns the secular-drift/dissipation sign) | **POSTULATE** (unchanged) |
| C-P3 | $a_0$ value and footing | **POSTULATE / FORK** (both carried) |

**Bottom line.** Off-circular predictivity is **not free and not unique**. Five principles pin the
operator, the circular RAR, the corner location, and the *sign/pattern* of the off-circular response;
they leave exactly **one bracketed reduction-weighting function** whose sign is forced and whose
magnitude is bounded between a zero-offset endpoint and a computed signed pattern. That bracket — closable
only by the off-circular Wightman pullback or an empirical proxy — is the honest boundary of the MI field
theory's off-circular predictivity.

---

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_field_theory && python3 closure_map.py`
(exit 0; 22 checks). Sources read (frozen read-only repo): `real_research/reviews/mi_formal_completion_2026/operator_definition.py`,
`.../transverse_mode_analysis.py`, `real_research/reviews/mi_offcircular_completion_SPEC.py`,
`real_research/papers/MI_COMPLETION_WRITTEN_2026-07.md`; local prep: `mi_fingerprint/{rb1,rb2,rb3}`,
`BASELINE_ACTION.md`, `rederive_identity.py`. Both $a_0$ footings throughout; $s=-1$ and $a_0$'s value
postulated; no completeness or TOE claim.*
