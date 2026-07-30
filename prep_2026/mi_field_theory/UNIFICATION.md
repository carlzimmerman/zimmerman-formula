# Lane C — Unification of Dynamics + Lensing in One Action

**Question (verbatim).** Does a *single* action yield BOTH the MI dynamics kernel AND lensing —
via the disformal photon metric $\tilde g_{\mu\nu}=g_{\mu\nu}+B(|a|/a_0)\,u_\mu u_\nu$ with $B$
derived FROM the same kernel $K(\Box_u)$ that gives the dynamics — Cassini-safe, Ostrogradsky-free,
$c_T=1$? Or does lensing *structurally* require the separate Branch-B elastic medium?

**Answer (one line).** Unification **HOLDS in the minimal-disformal sense**: one action, one metric,
one passive frame, one kernel $K(\Box_u)$, one scale $a_0$, **no new free function** ($B$ fixed by the
same $\nu=1/K$) and **no new propagating dof**. The heavy Branch-B medium is **NOT required**. But
lensing does **not** fall out of the dynamics term by itself — the single-metric self-lensing route is
*closed by double-counting*, so a **separate photon-sector coupling is structurally forced**. The
disformal term is the minimal such coupling. Its correctness off spherical symmetry **inherits gap A**
(the free off-circular closure), and one honest sub-check is only *order-of-magnitude satisfied*
(photon-timing, below).

Every load-bearing step is re-derived from the action in `unification.py` (17/17 checks, exit 0), not
trusted from the banked `mi_disformal_*.py`. Both $a_0$ footings carried
($9.36\times10^{-11}$ canonical / $1.13\times10^{-10}$ alt).

> **⚠️ SCOPE NOTE ADDED 2026-07-30 — what "re-derived from the action" does and does not cover here.**
> The 17/17 checks derive the **photon-sector (disformal) coupling** from the action *given* the
> dynamics law $\mu_{\rm fw}(|a|/a_0)\,a=g_{\rm bar}$. They do **not** derive that law. As of
> 2026-07-30 the law is known **not** to be the Euler–Lagrange equation of any fixed-kernel action,
> across four checked families (`mi_action_eom_vs_rar_2026.py`,
> `mi_action_reformulation_nogo_2026.py`, `mi_family4_variational_nogo_2026.py`; Thms 3 and 8 of DOI
> 10.5281/zenodo.21707845). The law is exact as a **first spectral moment** and is a successful fit,
> but it is not variational. **Consequence for this document:** the lensing construction is
> conditional on the law, not on the action alone, so "structurally forced" in §1 should be read as
> *forced given the dynamics law*. Nothing in the 17 checks is retracted; only their scope is
> clarified. Section 0's "inherits gap A (the free off-circular closure)" caveat already pointed this
> way — the residual freedom is now identified precisely as the single time-weighting function $w$,
> which Proposition 7 of the same DOI measures on archival dwarf spheroidals.

---

## 1. Why a second (photon-sector) coupling is structurally FORCED

The framework is modified **inertia** with host gravity **unmodified** ($S_{\rm EH}[g]$,
`MI_COMPLETION_WRITTEN_2026-07.md:19`). The metric $g$ is therefore the **baryonic** one, and the RAR
$g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}=\nu\,g_{\rm bar}$ is produced by the *inertial* response
$\mu(a/a_0)\,a=g_{\rm bar}$, $\mu=1/\nu$ (re-derived: `unification.py` Block 1, `a_obs==g_obs` PASS).

Light has no inertia → it follows null geodesics of $g$ → it feels $g_{\rm bar}$ → it **under-lenses by
$\nu$**. Trying to fix this by putting the enhancement in the metric ($g_{\rm bar}\to\nu_g g_{\rm bar}$)
and re-solving the *same* MI EOM gives dynamics $a'=\nu\cdot\nu_g\,g_{\rm bar}=\nu_g\,g_{\rm obs}$;
consistency with the observed rotation curve ($a'=g_{\rm obs}$) **forces $\nu_g=1$**
(`unification.py` Block 1, solved symbolically, PASS; reproduces `mi_lensing_doublecount_audit.py:47-52`).

**Structural conclusion.** With one metric you cannot share the enhancement between dynamics and light —
that is a genuine, non-manufactured double-count obstruction. **Lensing must live in a *separate*
coupling.** The only question is whether that coupling is (a) the minimal disformal photon term
built from ingredients already in the action, or (b) a whole separate action (Branch-B).

---

## 2. The disformal construction — and $B$ fixed by the SAME kernel

Light couples to $\tilde g_{\mu\nu}=g_{\mu\nu}+B\,u_\mu u_\nu$; matter keeps MI in $g$ (so **no
double-count by construction**). Re-derived from the metric (`unification.py` Block 2):

- **Only the disformal $u_\mu u_\nu$ part bends light.** A pure conformal rescaling $\tilde g=\Omega^2 g$
  leaves the null cone invariant ($\tilde g^{\mu\nu}k_\mu k_\nu=\Omega^{-2}g^{\mu\nu}k_\mu k_\nu$, same
  zero set — PASS). So the correct device is disformal, not conformal.
- **Lensing potential.** Static observer, $u_0^2=-g_{00}=1+2\Phi$: $\tilde g_{00}=-(1+2\Phi)(1-B)$ gives
  $\tilde\Phi=\Phi-B/2$; $\tilde\Psi=\Phi$ (the $u_iu_j$ block is zero, $u_i=0$). Hence
  $(\tilde\Phi+\tilde\Psi)/2=\Phi-B/4$ (PASS, up to the 2nd-order $B\Phi$ cross term).
- **$B$ fixed by $\nu$ — not free.** Requiring the deflection to match the RAR field
  $g_{\rm obs}=\nu g_{\rm bar}$ gives $\nabla B=4(\nu-1)\,g_{\rm bar}$, i.e. $B=4(\Phi-\Phi_{\rm MOND})$
  (PASS). $\nu$ is the **same** interpolation the dynamics use: the first-moment closure gives
  $\mu_{\rm fw}(x)=K(x^2)$, and the circular balance inverts *exactly* because
  $1+4(y^2+y)=(2y+1)^2$ → $\nu(y)=\sqrt{1+1/y}$ (both identities PASS, radical-robust).

**So one function $K(\Box_u)$ feeds both roles**: dynamics via the first-moment closure
$K(a^2/a_0^2)=\mu_{\rm fw}$, lensing via $B$ tied to $\nu=1/\mu_{\rm fw}$. $B$ introduces **no new free
function** — the concern that "$B$ is a second tunable" is answered.

---

## 3. The minimal unified action

$$\boxed{\,S=\underbrace{\frac{c^4}{16\pi G}\!\int\!\sqrt{-g}\,R}_{S_{\rm EH}[g]}
\;\underbrace{-\!\int\!\sqrt{-g}\,\tfrac{\lambda}{2}(u^\mu u_\mu+1)}_{S_u\ (\text{passive frame})}
\;\underbrace{-\tfrac12\!\int\!\sqrt{-g}\,\rho_m\,[\,s\,u^\mu K(\Box_u/a_0^2)u_\mu]}_{S_{\rm matter}\ (\text{MI dynamics})}
\;\underbrace{-\tfrac14\!\int\!\sqrt{-\tilde g}\,\tilde g^{\mu\alpha}\tilde g^{\nu\beta}F_{\mu\nu}F_{\alpha\beta}}_{S_\gamma\ (\text{disformal lensing})}\,}$$

with $\tilde g_{\mu\nu}=g_{\mu\nu}+B[K]\,u_\mu u_\nu$, $B$ the AQUAL potential of $4(\nu-1)g_{\rm bar}$,
$\nu=1/K(a^2/a_0^2)$, $K(z)=(\sqrt{1+4z}-1)/(2\sqrt z)$, $s=-1$, $a_0=cH_\Lambda/Z$.

**Ledger of the union.** One metric $g$; one passive frame $u$ (0 propagating dof, machine-verified,
`constraint_structure.py`/`A10_dirac_block.py`); one kernel $K$; one scale $a_0$; propagating content
**2 (graviton) + 2 (photon)**, unchanged. **No new field, no new free function, no new scale.** This is
"one nonlocality, two roles," and it is a genuine single action — *not* "one kernel written into two
sectors by hand," because the second insertion ($S_\gamma$) is **forced** (§1) and its coefficient
($B$) is **fixed** by the first (§2).

---

## 4. The three hard constraints — re-checked from the action

| Constraint | Verdict | Basis (`unification.py`) |
|---|---|---|
| **$c_T=1$ (GW170817 tensor speed)** | **EXACT pass** | The graviton propagates on $g$ ($S_{\rm EH}$ unmodified); $B\,u_\mu u_\nu$ has **zero spatial $ij$** components ($u_i=0$ in the rest frame), so the TT sector is untouched (Block 4, PASS). |
| **Cassini / solar system** | **Safe, both footings** | $B\sim(\nu-1)\to a_0/2a\to0$ at high $a$; $|\Delta\gamma|\sim7.2\times10^{-7}$ (canonical) / $8.7\times10^{-7}$ (alt) at Saturn, $\ll2.3\times10^{-5}$ (Block 5, PASS). Frame is passive → no aether Cassini bill. |
| **Ostrogradsky (ghost-free)** | **Yes — with a stated distinction** | *Local* $B(a)$: $a\sim\partial g$ (passive frame) → $S_\gamma$ first-order in every dynamical field → Ostrogradsky hypothesis never met, all orders (Block 3, PASS, machine-verified $\max\partial$-order $=1$). *Nonlocal* $B$ (needed off-sphere): an **elliptic/AQUAL constraint** ($\nabla^{-2}$), no time-kinetic term → ghost-free as a *constrained/auxiliary* field, **same standing as the framework's own nonlocal $K(\Box_u)$** — not the Ostrogradsky-trivial argument. |
| **Photon-timing (a *separate*, weaker bound)** | **⚠ Order-of-magnitude OPEN** | Photons on $\tilde g$ are subluminal ($\sqrt{1-B}$, $B>0$, causal — Block 2 PASS). The **photon-vs-graviton** LOS delay $\int(B/2)\,dl$ is **not** the tensor-speed bound and is **not obviously small**: per-galaxy $\delta B\sim4(\nu-1)a_0 r_{\rm MOND}/c^2\sim10^{-16}$, but if $B$ is sustained over Mpc-scale segments the accumulated delay can approach tension. **Flagged as a genuine open LOS computation, not asserted.** |

The photon-timing item is the one place the banked "$c_T=1$ exact" statement must be read carefully:
the **graviton** $c_T=1$ is exact and clean (that *is* GW170817); the **photon** disformal speed differs
by $B$, and its cosmological line-of-sight integral is a separate, unfinished check.

---

## 5. The obstruction that remains — and what it means

**5a. Lensing does not emerge from the dynamics term alone.** §1 is a real single-metric obstruction:
MI modifies the worldline, not null geodesics, and the source-side $T_{\mu\nu}$ route cannot enhance the
*shared* metric without double-counting the rotation curve. So a photon-sector coupling is **mandatory**.
The disformal term is the **minimal** one (no new field/function); therefore the **Branch-B elastic
medium is not required** — and Branch B is independently *evidence-tilted to fail Cassini* (its free shear
Poisson scalar $\beta$ lands below $\beta_{\rm crit}$ for every natural value, $\times1.1$–$1.8$ over the
ceiling, `ELASTIC_MEDIUM_ACTION_2026.md:47`). The unified action in §3 **strictly dominates** the
two-action Branch-B alternative.

**5b. Off spherical symmetry, lensing inherits gap A.** A *local* $B(|a|/a_0)$ is an exact lensing
potential only when $g_{\rm obs}=\nu(|g_{\rm bar}|)g_{\rm bar}$ is curl-free: **true for spherical**
symmetry (curl $=0$ identically), **false in general** (two point masses: curl $=-0.31$, order-unity —
`unification.py` Block 5, both PASS; reproduces `mi_disformal_locality.py`). In general $B$ must be the
**nonlocal AQUAL potential** $\nabla\!\cdot[\mu(|\nabla\Phi_M|/a_0)\nabla\Phi_M]=\nabla\!\cdot g_{\rm bar}$
— which *is* the framework's own $K(\Box_u)$. But then $\nabla\Phi_M\neq\nu\,g_{\rm bar}$ off spherical
symmetry: the **dynamical RAR** (algebraic, first-moment) and the **lensing RAR** (AQUAL, curl-free) are
two *different* reductions of the same nonlocal operator. They **coincide exactly only where the
first-moment closure pins them** (spherical / circular). Off it, both are **free** — this is exactly
**gap A** (`BASELINE_ACTION.md` §3(II.b): the closure map is O(1)-free off circles). Lensing does not add
a *new* gap; it **inherits** the existing one.

**Precise statement of unification standing.** The single action of §3 delivers dynamics-RAR = lensing-RAR
**exactly** on the spherical/circular configurations where the closure is pinned, with $c_T=1$ exact,
Cassini-safe (both footings), and ghost-free. Off those configurations, the equality of the two RARs is
**undetermined at the same O(1) level** as the dynamics — the open closure/ordering map is the *single*
thing gating both. The minimal unified action is therefore as complete as the dynamics sector itself, and
no more.

---

## 6. DERIVED vs POSTULATED (this lane)

**DERIVED (re-derived here, `unification.py`, 17/17, exit 0):**
- U1 — Single-metric self-lensing is obstructed; the RAR-calibrated MI forces $\nu_g=1$ (Block 1).
- U2 — Only the disformal $u u$ part bends light; lensing potential $=\Phi-B/4$; $\nabla B=4(\nu-1)g_{\rm bar}$ (Block 2).
- U3 — One kernel $K$ feeds both roles; the RAR-collapse identity $1+4(y^2+y)=(2y+1)^2$ and the circular balance $\mu_{\rm fw}(x^*)x^*=y$ (Block 2).
- U4 — $c_T=1$ **exact** (graviton on $g$; $Buu$ has no TT part) (Block 4).
- U5 — Cassini-safe both footings; $|\Delta\gamma|\sim10^{-7}$ at Saturn (Block 5).
- U6 — Ostrogradsky-free: local $B$ first-order (trivial); nonlocal $B$ an elliptic constraint (Block 3).
- U7 — Off-sphere $B$ must be nonlocal ($=K(\Box_u)$); curl$(\nu g_{\rm bar})=0$ spherical / $\neq0$ non-spherical (Block 5).

**POSTULATED / OPEN (named, not tuned away):**
- P1 — $s=-1$ (sets the disformal sign $B>0$/subluminal too), and $a_0$'s value $cH_\Lambda/Z$ — inputs.
- P2 — **Off-spherical closure (gap A), inherited by lensing:** dynamical-RAR = lensing-RAR only where the first-moment closure is pinned; off it both are free.
- P3 — **Photon-timing LOS bound (⚠):** the photon-vs-graviton disformal delay $\int(B/2)dl$ is only order-of-magnitude checked and is *not* obviously safe over Mpc paths — an open quantitative computation.
- P4 — Explicit $K(\Box_u)$ AQUAL lensing solve for one specific non-spherical galaxy (standard, no new physics, undone).
- P5 — Full nonlinear coupled $g+u+\gamma$ back-reaction / metric $T_{\mu\nu}$ (gap B) still uncomputed; the ghost-free/causal results are kinematic + first-order-Lagrangian (§4), not the fully-coupled all-orders proof.

---

## 7. Bottom line

**A single action unifies dynamics and lensing** — §3, with one metric, one passive frame, one kernel
$K(\Box_u)$, one scale $a_0$, no new free function, and no new propagating dof; $c_T=1$ exact; Cassini-safe
both footings; ghost-free. **Lensing does not emerge from the dynamics term by itself** — the single-metric
route is closed by double-counting, so the disformal photon coupling is *structurally forced*; it is the
*minimal* forced coupling, so **the separate Branch-B medium is not required** (and Branch B is
evidence-tilted to fail Cassini). The unification is **exact where the closure is pinned** (spherical /
circular) and **inherits gap A off it**; one honest sub-check (photon-timing over cosmological baselines)
is only order-of-magnitude satisfied and is flagged open. This is the most complete *honest* unified MI
field-theory statement the current structure supports — a well-posed single action gated, like the
dynamics, by the one free off-circular closure map. **No completeness or TOE claim.**

---

### Reproduction
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_field_theory
python3 unification.py     # exit 0; 17/17 structural checks, both a0 footings
```
Sources read (frozen read-only `zimmerman-formula/`): `real_research/papers/MI_COMPLETION_WRITTEN_2026-07.md`
(§5 lensing, §6), `real_research/papers/ELASTIC_MEDIUM_ACTION_2026.md:40-47`,
`real_research/reviews/mi_formal_completion_2026/{mi_disformal_lensing.py, mi_disformal_ghostfree.py,
mi_disformal_ostrogradsky.py, mi_disformal_locality.py, mi_lensing_doublecount_audit.py,
mi_lensing_from_stress_tensor.py, operator_definition.py}`, `agentY_quasistatic.out` (c_T=1 slip sector).
Local baseline: `prep_2026/mi_field_theory/BASELINE_ACTION.md`, `rederive_identity.py`.
Both $a_0$ footings throughout. $s=-1$ postulated, $a_0$'s value underived.
```
```
