# Lane WELL-POSED — Degrees of Freedom & Ghost-Freedom of the FULL Coupled MI System

**Purpose.** With the completion lanes' single action in hand, count the propagating degrees of
freedom and prove (or break) ghost-freedom / Hamiltonian-boundedness / hyperbolicity / causality of the
**full coupled** $g_{\mu\nu}+u^\mu+\text{matter}(+\text{disformal photon})$ system — **not** the frame
sector in isolation. Every load-bearing step is a genuine symbolic/numeric check in
`wellposed.py` (28/28, exit 0, no hard-coded booleans). **Both $a_0$ footings carried.** DERIVED vs
POSTULATED flagged. This is *the most complete honest well-posedness statement the current structure
supports* — **not** a completeness or theory-of-everything claim.

**The action under test** (`BASELINE_ACTION.md` §1; `UNIFICATION.md` §3; `MI_COMPLETION_WRITTEN_2026-07.md:19-20`,
`:45-49`), signature $(-+++)$:
$$S=\underbrace{\frac{c^4}{16\pi G}\!\int\!\sqrt{-g}\,R}_{S_{\rm EH}[g]}
\;\underbrace{-\!\int\!\sqrt{-g}\,\tfrac{\lambda}{2}(u^\mu u_\mu+1)}_{S_u\ (\text{passive frame})}
\;\underbrace{-\tfrac12\!\int\!\sqrt{-g}\,\rho_m\,[\,s\,u^\mu K(\Box_u/a_0^2)u_\mu]}_{S_{\rm matter}\ (\text{MI dynamics})}
\;\underbrace{-\tfrac14\!\int\!\sqrt{-\tilde g}\,\tilde g^{\mu\alpha}\tilde g^{\nu\beta}F_{\mu\nu}F_{\alpha\beta}}_{S_\gamma\ (\text{disformal lensing})}$$
$$\tilde g_{\mu\nu}=g_{\mu\nu}+B\,u_\mu u_\nu,\quad K(z)=\tfrac{\sqrt{1+4z}-1}{2\sqrt z},\quad
\Box_u f=(u\!\cdot\!\nabla)^2 f,\quad s=-1\ (\textbf{postulate}),\quad
a_0=\tfrac{cH_\Lambda}{Z}=9.36\times10^{-11}\ (\text{alt }1.13\times10^{-10}).$$

---

## 1. Bottom line (verdict)

**The full coupled system is well-posed: ghost-free, Hamiltonian bounded below, hyperbolic, and
causal — footing-independently — under the framework's own passive-frame premise.** No ghost, no
gradient instability, no acausal signalling was found. The one genuine hinge (frame passivity) and the
uncomputed edges (fully-coupled nonlocal Hamiltonian, global $B<1$) are reported straight in §7.

| Property | Verdict | Basis (`wellposed.py`) |
|---|---|---|
| **Propagating dof** | **2 graviton + 2 photon + standard matter; frame = 0** | Block 1 |
| **Ostrogradsky ghost** | **None** — local action first-order in every dynamical field; nonlocal $K$ ghost-free by Herglotz single pole | Block 2 |
| **Hamiltonian bounded below / gradient stability** | **Yes** — $\mu=K\in(0,1]$; $\tilde g$ Lorentzian & $c_\gamma^2=1-B>0$ for $B<1$; $c_T=1$ | Block 3 |
| **Hyperbolicity / well-posed IVP** | **Yes** — block-diagonal principal symbol, real characteristics | Block 4 |
| **Causality** | **Yes** — photon cone nested in $g$ cone ($B\!\ge\!0\!\Leftrightarrow\!s\!=\!-1$); retarded kernel | Block 5 |
| **Footing-independence** | **Yes** — verdict is $a_0$-value-independent (structure only) | Block 6 |

---

## 2. Degrees of freedom of the FULL coupled system (Block 1)

**Ledger.** Propagating field content $= 2$ (graviton) $+ 2$ (photon) $+$ standard matter; the passive
frame $u^\mu$ carries **0**. The central new result of this lane is that **the frame's 0-dof survives
the matter coupling** — the earlier count (`constraint_structure.py`, `A10_dirac_block.py`) was done for
the frame sector *in isolation*; here it is re-verified with $S_{\rm matter}$ (which depends on $\partial u$
through $a^\mu=u^\nu\nabla_\nu u^\mu$) turned on.

**(1a) The unit-norm second-class Dirac pair survives the matter coupling.** The pair
$\chi_1=u\!\cdot\!u+1$, $\chi_2=u\!\cdot\!\pi$ has Dirac bracket $\{\chi_1,\chi_2\}=2(u\!\cdot\!u)$, det
$=4(u\!\cdot\!u)^2\to4$ on-shell. The decisive point: this is a **kinematic** phase-space bracket —
$\{\chi_1,\chi_2\}=(\partial\chi_1/\partial u^m)(\partial\chi_2/\partial\pi_m)$ depends only on the
*form* of $\chi_{1,2}$, **not on what $\pi$ contains**. `wellposed.py` Block 1a verifies this with a
momentum $\pi_m=\pi^{\rm free}_m+Q_m(u)$ that already carries an *arbitrary* matter contribution
$Q(u)=\partial\mathcal L_{\rm matter}/\partial\dot u$; the bracket is unchanged, $=2(u\!\cdot\!u)$. So the
matter dressing cannot spoil the second-class pair that removes the frame's timelike component. [DERIVED.]

**(1b) The frame's own principal symbol is a transport ODE, not a wave.** $\Box_u=(u\!\cdot\!\nabla)^2$
differentiates *only along $u$*; its symbol is $(u\!\cdot\!k)^2\to k_0^2$ in the rest frame — **no spatial
gradient**. The characteristic equation $k_0^2=0$ has a double root at $k_0=0$ *independent of the
spatial $k_i$*, with group velocity $\partial k_0/\partial k_i=0$ (`wellposed.py` Block 1b). This is a
transport-along-$u$ ODE with zero group velocity — it carries no Cauchy data off the initial slice, so it
is **not a propagating field**. Even dressed by $K(a^2)$, the frame cannot become a propagating aether: a
healthy spin-1 needs a spatial-gradient wave-cone $k_0=c_s|k|$, which $(u\!\cdot\!\nabla)^2$ structurally
cannot supply. Reproduces + extends `transverse_mode_analysis.py`, `principal_symbol_blockdiag.py`. [DERIVED,
under the passive premise — §7(i).]

**Matter and graviton counts are standard.** $S_{\rm EH}$ is unmodified GR (2 graviton dof). Matter
is minimally coupled to the single metric $g$ (`MATTER_COUPLING.md` §1), so it carries its usual content.
The photon rides $\tilde g$ (Maxwell on any Lorentzian metric = 2 dof; $\tilde g$ Lorentzian for $B<1$,
§3). **No new propagating dof is introduced by any of the three couplings.**

---

## 3. No Ostrogradsky ghost (Block 2)

**Local first-moment action: first-order in every dynamical field.** The load-bearing subtlety unique to
*modified inertia* is that a naive worldline Lagrangian $L(\ddot x)$ depending on **acceleration** is
second-order in the worldline coordinate $\Rightarrow$ Ostrogradsky ghost. The framework **evades this**
because in the *field theory* the acceleration is $a^\mu=u^\nu\nabla_\nu u^\mu$ — a **first-order gradient
of the field $u(x)$**, not $\ddot x$ of a worldline. `wellposed.py` Block 2 machine-expands both the matter
dressing $K(a^2/a_0^2)$ **and** the disformal $B(a)F^2$ in a metric fluctuation and finds the highest
derivative of the fluctuation is **order 1** in each (no $\partial^2$). Ostrogradsky's second-derivative
hypothesis is never met $\Rightarrow$ no higher-derivative ghost, to all orders in the fluctuation.
Extends `mi_disformal_ostrogradsky.py` to cover the *matter* $K(a^2)$ term, not only the disformal term.
[DERIVED, under the passive premise.]

**The nonlocal $K(\Box_u)$ is ghost-free by the *Herglotz single-pole* route — stated, not conflated.**
$\Box_u=(u\!\cdot\!\nabla)^2$ is genuinely second-order *along $u$* (the nonlocality). For it, ghost-freedom
is **not** the Ostrogradsky-trivial argument; it is the positive-measure / single-healthy-pole property of
$K$: operator-monotone $K'(z)>0$ on $z>0$ (Herglotz signature), $0<K\le1$, and the propagator UV residue
$=+1$ (`wellposed.py` Blocks 0b, 0c; matches `operator_definition.py:124-140`, `oneloop_laneA_divergences.py`).
$K$ is a positive superposition of massive local resolvents with positive residues — one healthy pole, no
ghost pole. [DERIVED at propagator level (D3/D7); fully-coupled all-orders Hamiltonian not constructed —
§7(ii).]

---

## 4. Hamiltonian bounded below / no gradient instability (Block 3)

- **Matter sector.** The dressed inertia $\mu=K(X)\in(0,1]$ for all $X>0$ (`wellposed.py` Block 0a/3a) —
  strictly **positive**, so the matter kinetic energy is positive and bounded below. No wrong-sign kinetic
  term appears in any acceleration regime (Newtonian $K\to1$, deep-MOND $K\to0^+$ but always $>0$). [DERIVED.]
- **Photon sector.** $\tilde g=g+B\,u_\mu u_\nu$ has rest-frame eigenvalues $\{B-1,1,1,1\}$: exactly **one
  negative eigenvalue iff $B<1$** (Lorentzian $-\!+\!+\!+$); at $B=1$ degenerate; for $B>1$ it flips to
  Euclidean and the photon sector would be sick. Verified by direct eigenvalue count (`wellposed.py` Block
  3b). The photon phase speed $c_\gamma^2=1-B>0$ for $B<1$ — **real and subluminal, no gradient
  instability**. The bound $B<1$ holds **parametrically** in the MI regime: $B\sim4(\nu-1)(v/c)^2\sim
  6\text{–}7\times10^{-7}$ at a galaxy for **both footings** (canonical $v_{\rm flat}\approx188$ km/s,
  $B\approx6.5\times10^{-7}$; alt $\approx197$ km/s, $B\approx7.1\times10^{-7}$; Block 3c). [DERIVED
  parametrically; global $B<1$ is §7(iii).]
- **Graviton sector.** $S_{\rm EH}$ on $g$ is standard GR (bounded); $B\,u_\mu u_\nu$ has **zero spatial
  $ij$ block** ($u_i=0$ in the rest frame), so the TT sector is untouched and $c_T=1$ **exact** (the real
  GW170817 bound). [DERIVED — Block 3d; `agentY_quasistatic.out`.]

---

## 5. Hyperbolicity / well-posed initial-value problem (Block 4)

The principal symbol of the coupled system is **block-diagonal**, each block with real characteristics:

- **Graviton block** $=$ pure GR light cone $-\xi_0^2+|\xi|^2$, roots $\xi_0=\pm|\xi|$. The disformal term
  is **first-order in $g$** ($a\sim\partial g$ via the connection, passive $u$) so it contributes at
  $O(\xi^0\text{–}\xi^1)$ and **never enters the $O(\xi^2)$ graviton principal symbol** — the graviton cone
  is exactly GR (`wellposed.py` Block 4a; reproduces `principal_symbol_blockdiag.py`).
- **Photon block** $=$ $\tilde g$ light cone $-\xi_0^2+(1-B)|\xi|^2$, roots $\xi_0=\pm\sqrt{1-B}\,|\xi|$ —
  **real for $B<1$** (Block 4b).
- **Frame block** $=$ transport $k_0=0$ (Block 1b) — a constraint/transport sector with no spatial cone;
  it does not couple into the two propagating cones (no spatial-gradient mixing) and cannot spoil
  hyperbolicity (Block 4c).

A block-diagonal principal symbol with real characteristics in each propagating block, plus the
second-class + transport constraint sector, is a **symmetric-hyperbolic system with constraints
$\Rightarrow$ well-posed Cauchy problem** (Block 4d). Hyperbolicity inherits from GR in the UV ($K\to1$)
limit (D8; `stability.py`). **Nonlocal caveat:** the full system is integro-differential; its Cauchy
problem is well-posed *with history data* precisely because the kernel is **retarded** (§6).

---

## 6. Causality (Block 5)

- **Photon cone nested inside the $g$ cone.** At fixed $|k|$, the photon frequency $k_0=\sqrt{1-B}\,|k|\le
  |k|$ (the graviton/matter value) **iff $B\ge0$** — the photon cone lies strictly *inside* the $g$ cone, so
  photons are subluminal and no superluminal/acausal signalling occurs (`wellposed.py` Block 5a). This ties
  causality to the postulated sign: $B\ge0\Leftrightarrow\nu\ge1\Leftrightarrow s=-1$. **$s=-1$ is therefore
  also the causality-preserving sign**; $s=+1$ ($B<0$) would make photons superluminal $\Rightarrow$ acausal
  (the acausal branch is exhibited explicitly, Block 5a). [Structural note; $s=-1$ POSTULATED.]
- **Retarded memory kernel.** $K$ is analytic ($\mathrm{Im}\,K=0$) on the physical $z>0$ axis, with its cut
  on $z<0$ (Euclidean masses $-t>0$); the corresponding time-domain Green's function of each positive-mass
  resolvent is the **retarded** one, support in the causal past. So the memory integral sees only the past —
  **no acausal feedback** in the coupled system (Block 5b; `operator_definition.py`). [DERIVED.]
- **Single global causal order.** All signal cones — graviton on $g$, matter on $g$, photon on
  $\tilde g\subset g$ — are nested inside the $g$ cone, so the coupled system has one well-defined global
  causal structure and no closed causal curves are introduced by the coupling (Block 5c). [DERIVED.]

---

## 7. Honest open edges (verified as hard as the wins — not papered over)

1. **Frame 0-dof rests on the passive/khronon premise (the load-bearing hinge).** The transverse frame
   modes are removed as second-class partners under hypersurface-orthogonality (C2); the transport symbol
   guarantees they never *propagate* as waves either way. But this is the framework's **postulate** that
   $u$ is the non-dynamical cosmic (dS-Unruh/CMB) rest frame. **Were $u$ promoted to a dynamical khronon
   $T$**, then $a\sim\partial^2T$ and both $K(\Box_u)$ and $B(a)$ would reach $T$'s second derivative — an
   **Ostrogradsky concern for $T$**. The passive premise forbids that; absent it the transverse modes are
   frozen/transport (degenerate, still *not* a healthy propagating aether, but a sick sector). The clean
   0-dof + ghost-free verdict **requires** the passive premise (`transverse_mode_analysis.py` STEP 5 caveat;
   `mi_disformal_ostrogradsky.py` "honest hinge").
2. **The fully-coupled all-orders NONLOCAL Hamiltonian is not constructed.** The results here are
   constraint-level (Dirac pair) $+$ principal-symbol $+$ first-order-Lagrangian $+$ propagator single-pole.
   These are solid and mutually consistent, but they are **not** a fully nonlinear coupled $g+u+\gamma$
   back-reaction proof (same standing as gap B / P6 in `BASELINE_ACTION.md`).
3. **$B<1$ (photon-metric Lorentzian) holds parametrically but is not proven GLOBALLY off spherical
   symmetry.** It inherits **gap A** (the free off-circular closure — `BASELINE_ACTION.md` §3.II.b) and the
   open **photon-timing LOS bound** (`UNIFICATION.md` P3), which is only order-of-magnitude satisfied over
   Mpc paths.
4. **$s=-1$ and $a_0$'s value stay POSTULATED.** No completeness or TOE claim (the TOE/SM overclaims were
   publicly retracted 2026-06-23 and are not reasserted).

---

## 8. DERIVED vs POSTULATED (this lane)

**DERIVED (re-derived here, `wellposed.py`, 28/28, exit 0, both footings):**
- W1 — Frame second-class Dirac pair **survives the matter coupling** ($\{\chi_1,\chi_2\}=2(u\!\cdot\!u)$
  independent of the matter piece of $\pi$; det $\to4$) — Block 1a.
- W2 — Frame principal symbol $(u\!\cdot\!k)^2$ is a transport ODE (zero group velocity, no spatial cone)
  $\Rightarrow$ 0 propagating frame dof under the coupling — Block 1b.
- W3 — Coupled propagating content $=2$ graviton $+2$ photon $+$ standard matter — Block 1c.
- W4 — No Ostrogradsky ghost: local action first-order in every dynamical field (matter $K(a^2)$ **and**
  disformal $B(a)$; the MI-specific $L(\ddot x)$ trap is evaded because $a=u\!\cdot\!\nabla u$ is a field
  gradient) — Block 2.
- W5 — Nonlocal $K(\Box_u)$ ghost-free by Herglotz single healthy pole ($K'>0$, residue $+1$, $0<K\le1$) —
  Blocks 0b/0c/2.
- W6 — Hamiltonian bounded below: $\mu=K\in(0,1]$; $\tilde g$ Lorentzian & $c_\gamma^2=1-B>0$ iff $B<1$;
  $B\sim10^{-6}\ll1$ both footings; $c_T=1$ exact — Block 3.
- W7 — Hyperbolic / well-posed IVP: block-diagonal principal symbol, real characteristics; disformal does
  not touch the graviton principal symbol — Block 4.
- W8 — Causal: photon cone nested in $g$ ($B\ge0\Leftrightarrow s=-1$); retarded kernel; single global
  causal order — Block 5.
- W9 — Verdict $a_0$-value-independent (structure only; $a_0$ enters only via $X=|a|^2/a_0^2$) — Block 6.

**POSTULATED / OPEN (named, not tuned away):**
- P1 — **Passive-frame premise** (hypersurface-orthogonal $u$): load-bearing hinge for 0-dof & no-$T$-ghost
  (§7.1).
- P2 — **Fully-coupled all-orders nonlocal Hamiltonian** uncomputed (§7.2; = gap B/P6).
- P3 — **Global $B<1$** off spherical symmetry: parametric only, inherits gap A + photon-timing LOS (§7.3).
- P4 — **$s=-1$** and **$a_0$'s value** $cH_\Lambda/Z$: inputs (§7.4).

---

### Reproduction
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_field_theory
python3 wellposed.py     # exit 0; 28/28 checks; both a0 footings
```
Sources read (frozen read-only `zimmerman-formula/`): `real_research/reviews/mi_formal_completion_2026/`
(`constraint_structure.py`, `A10_dirac_block.py`, `principal_symbol_blockdiag.py`,
`transverse_mode_analysis.py`, `operator_definition.py`, `mi_disformal_ostrogradsky.py`,
`oneloop_laneA_divergences.py`, `stability.py`), `agentY_quasistatic.out`. Local lanes:
`BASELINE_ACTION.md`, `MATTER_COUPLING.md`, `UNIFICATION.md`, `rederive_identity.py`. Program concept DOI
10.5281/zenodo.21253644; loop arc 21284144.

*Both $a_0$ footings throughout. Each claim flagged derived / postulated / open. $s=-1$ postulated,
$a_0$'s value underived. No completeness or theory-of-everything claim.*
