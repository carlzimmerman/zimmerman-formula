# Lane B — Matter Coupling and the Full Stress-Energy Tensor of the de Sitter–Unruh Modified-Inertia Action

**Purpose.** Close (as far as an honest classical computation allows) the completion gap **B** named in
`BASELINE_ACTION.md` (row P6) and `MI_COMPLETION_WRITTEN_2026-07.md:31`: *how matter couples to the
frame/kernel, the full metric stress tensor* $T_{\mu\nu}=-\tfrac{2}{\sqrt{-g}}\delta S_{\rm matter}/\delta g^{\mu\nu}$,
*and whether $\nabla_\mu T^{\mu\nu}=0$ holds on-shell (Bianchi/Noether consistency)* — with $a_0=cH_\Lambda/Z$
confirmed as the single, unrenormalized scale. Every load-bearing step is a runnable check in
`matter_coupling_Tmunu.py` (exit 0, 14/14 checks). Both $a_0$ footings carried. DERIVED vs POSTULATED
flagged throughout. This is **not** a completeness or theory-of-everything claim.

Baseline action (`BASELINE_ACTION.md` §1; `MI_COMPLETION_WRITTEN_2026-07.md:19-20`), signature $(-+++)$:
$$S = \underbrace{\tfrac{c^4}{16\pi G}\!\int\!\sqrt{-g}\,R}_{S_{\rm EH}[g]}
\;\underbrace{-\!\int\!\sqrt{-g}\,\tfrac{\lambda}{2}(u^\mu u_\mu+1)}_{S_u[g,u,\lambda]}
\;\underbrace{-\tfrac12\!\int\!\sqrt{-g}\,\rho_m\big[\,s\,u^\mu K(\Box_u/a_0^2)u_\mu\,\big]}_{S_{\rm matter}[g,u,\psi]},$$
$$K(z)=\tfrac{\sqrt{1+4z}-1}{2\sqrt z},\quad \Box_u f=u^a\nabla_a(u^b\nabla_b f),\quad s=-1\ (\textbf{postulate}).$$

---

## 1. How matter couples — the explicit coupling term (question 1)

**The coupling is a universal *inertial-scalar dressing*, not a disformal matter metric.**
Matter is **minimally coupled to the single metric $g$** (rods, clocks, and **photons** ride $g$).
Modified inertia enters *only* as the universal frame scalar that multiplies the rest-mass density,
$$W[u,g]\;=\;s\,u^\mu K(\Box_u/a_0^2)\,u_\mu\;\xrightarrow[\text{first-moment closure}]{}\;s\,(u\!\cdot\!u)\,K\!\big(|a|^2/a_0^2\big),\qquad
a^\mu=u^b\nabla_b u^\mu,\ \ |a|^2=a_\mu a^\mu.$$
So **matter feels the kernel through its own 4-acceleration** $a^\mu$ (the acceleration of the worldline/
frame relative to the cosmic rest frame), via the scalar $|a|^2/a_0^2$. The first-moment closure is the
load-bearing bridge $u_\mu\Box_u u^\mu=-|a|^2$, re-derived worldline-general (flat, arbitrary curved
metric, and a concrete Schwarzschild example) in `rederive_identity.py` [I]. The dressing $K(|a|^2/a_0^2)=
\mu_{\rm fw}(|a|/a_0)$ is exactly the framework's inertia interpolation.

**WEP is exact ($\eta=0$) — a DERIVED win.** $W$ is built only from $(u,g,\partial u)$; it carries **no
matter-species label**. Every body's inertial coefficient is the *same* function $\mu_{\rm fw}(|a|/a_0)$,
so two bodies in the same external field $g_{\rm bar}$ acquire identical acceleration:
the balance $\mu_{\rm fw}(x)\,x=y$ inverts (nested radical collapsing, $1+4x^2=(2y+1)^2$) to the
species-independent $x=y\,\nu(y)$, giving $\eta=(a_A-a_B)/a_{\rm avg}=0$ **exactly**
(`matter_coupling_Tmunu.py` §1a; residual $<10^{-12}$ over $y\in[10^{-2},10^2]$).

**Why not a disformal matter metric.** A disformal *matter* metric $\tilde g^{\rm M}_{\mu\nu}=g_{\mu\nu}+C\,u_\mu u_\nu$
would *also* be universal, but it would drag **light** (Maxwell built on $\tilde g^{\rm M}$ acquires an
$O(C)\,(u^aF_{ab})(u^cF_{cd})$ term), modifying lensing *in the matter sector* and **double-counting** the
dynamics. The framework rejects this: $W$ contains no $F_{\mu\nu}$, so photons stay on $g$ exactly, and
lensing is carried *separately* by the light-only disformal **photon** metric
(`MI_COMPLETION_WRITTEN_2026-07.md:45-49`). [DERIVED modelling choice.]

---

## 2. The three variations (question 2)

Worked in the local **first-moment (quasistatic) action** — exact on circular orbits; the off-circular
ordering (gap A) is FREE (`rederive_identity.py` II.b), so the *nonlocal* $T_{\mu\nu}$ differs off-circles
by that same undetermined closure. Lagrange-multiplier form, $X\equiv|a|^2/a_0^2$:
$$\mathcal L = -\tfrac12\rho_m\,s\,(u\!\cdot\!u)\,K(X)\;-\;\tfrac{\lambda}{2}(u\!\cdot\!u+1).$$

**(2a) $\delta/\delta\lambda$:** $\;-\tfrac12(u\!\cdot\!u+1)=0\Rightarrow u\!\cdot\!u=-1$ — the unit-timelike
constraint (verified).

**(2b) $\delta/\delta u^\mu$ — the frame equation, source is $\ell=0$.** The algebraic (non-derivative)
part of the $u$-variation — the part that can source the metric — is strictly **parallel to $u_\mu$**:
$$J^{\rm alg}_\mu=-\big[\rho_m s\,K(X)+\lambda\big]\,u_\mu\quad(\ell=0).$$
Contracting with $u^\mu$ (and $u\!\cdot\!u=-1$) fixes the multiplier **algebraically**,
$\lambda=-\rho_m s\,K(X)$, with **no tertiary tower** (2nd-class Dirac pair, block determinant
$4(u\!\cdot\!u)^2\to4$; `constraint_structure.py`, `A10_dirac_block.py`). The remaining $K'$ (derivative)
terms are the worldline dynamics — the acceleration $a^\mu$, an $\ell=1$ vector — and **never populate the
$\ell=2$ traceless-shear** whose divergence is AeST's Cassini Bianchi lock. This is *"MOND does not force
modified gravity"* realized at the frame-equation level (`MI_COMPLETION_WRITTEN_2026-07.md:31`, §4a).
[DERIVED.]

**(2c) $\delta/\delta g^{\mu\nu}$ — the stress tensor.** Building blocks (passive $u^\mu$ upper is
metric-free at algebraic order): $\partial(u\!\cdot\!u)/\partial g^{\mu\nu}=-u_\mu u_\nu$,
$\partial(a\!\cdot\!a)/\partial g^{\mu\nu}=-a_\mu a_\nu$, and $\delta\sqrt{-g}\to g_{\mu\nu}\mathcal L$. With
$T_{\mu\nu}=-2\,\partial\mathcal L/\partial g^{\mu\nu}+g_{\mu\nu}\mathcal L$, the matter stress tensor is
$$\boxed{\,T_{\mu\nu}=\alpha\,u_\mu u_\nu+\beta\,g_{\mu\nu}+\gamma\,a_\mu a_\nu\,},\qquad
\alpha=-\rho_m s K,\ \ \beta=\tfrac12\rho_m s K,\ \ \gamma=\frac{\rho_m s\,K'(X)}{a_0^2}\quad(u\!\cdot\!u=-1).$$

- **Principal (UV) limit** $K\to1,\ K'\to0$: $\gamma\to0$, so $T_{\mu\nu}\to\alpha\,u_\mu u_\nu+\beta\,g_{\mu\nu}$ —
  an **isotropic perfect fluid**, i.e. **no anisotropic stress ⇒ no gravitational slip** ($\Psi=\Phi$),
  the same no-slip property AeST has but sourced here by the **modified-inertia matter tensor**, not a
  dynamical aether — hence **no Cassini bill** (`mi_lensing_from_stress_tensor.py`;
  `principal_symbol_blockdiag.py`).
- **The only anisotropic (slip/enhancement-capable) stress is $\gamma\,a_\mu a_\nu$**, carried by $K'(X)$,
  and it is **nonzero only in the low-acceleration MOND/IR regime**. This is precisely the open
  *"enhancement"* piece for lensing (gap C): present in the tensor and of the right (horizon-$a_0$) order,
  but its exact IR magnitude and higher multipoles require the full curved $\delta S_{\rm matter}/\delta g$
  (the connection piece of $a^\mu$) — the named open classical computation. [Structure DERIVED; IR
  magnitude OPEN.]

*(Normalization note: the framework's $-\tfrac12\rho_m s(u\!\cdot\!u)K$ convention gives a rest-frame
$\rho_e=2\rho_m$, $p=-\tfrac12\rho_m$ at $K\to1$; the physical content is the tensor **structure**, which is
what fixes slip and conservation. The $\ell=0$ $u_\mu u_\nu$ source is soaked by the $\lambda$-sector stress
$T^\lambda_{\mu\nu}=-\lambda u_\mu u_\nu$ with $\lambda=-\rho_m s K$, the explicit statement of frame
passivity.)*

---

## 3. Conservation $\nabla_\mu T^{\mu\nu}=0$ and frame consistency (question 3)

**Theorem (diffeomorphism invariance).** $S_{\rm matter}+S_u$ is a covariant scalar of $(g,u,\lambda,\rho_m)$.
Under $x\to x+\xi$, $\delta S=0$ collects into the off-shell Noether/Bianchi identity
$$\nabla_\mu T^{\mu\nu}=-(E_u)_a(\text{frame-eq terms})-E_\lambda(\text{constraint})-E_{\rho}(\text{continuity}),$$
so $\nabla_\mu T^{\mu\nu}=0$ **on-shell** — when the $u$-equation, the $\lambda$-constraint, and matter
continuity all hold. The physically load-bearing fact (from §2b): the $u$-equation **is** imposed (it fixes
$\lambda$), its source is $\ell=0$ (parallel to $u$) and is **soaked by $\lambda$**, so on-shell conservation
is attained with **no $\ell=2$ obstruction** — no forced metric shear, no Cassini Bianchi lock.

**Verified two ways** (`matter_coupling_Tmunu.py` §3):
1. **Exact generic Noether identity.** For any first-order $\mathcal L(\phi,\partial\phi)$, the canonical
   tensor $\Theta^\mu{}_\nu=(\partial\mathcal L/\partial(\partial_\mu\phi))\partial_\nu\phi-\delta^\mu_\nu\mathcal L$
   satisfies $\partial_\mu\Theta^\mu{}_\nu=-(EL_\phi)\partial_\nu\phi$ **identically** (symbolic, exact).
   Hence on-shell $\partial_\mu\Theta^\mu{}_\nu=0$; the Hilbert $T$ equals canonical + Belinfante
   improvement (identically conserved), so $\nabla_\mu T^{\mu\nu}_{\rm Hilbert}=0$ on-shell too.
2. **MI-kernel instantiation.** With the frame rapidity $\xi(t,x)$, $u=(\cosh\xi,\sinh\xi)$ (unit-timelike
   identically), $a^\mu=u^b\partial_b u^\mu$, $\mathcal L=\tfrac12 s\rho_0 K(a\!\cdot\!a/a_0^2)$, the identity
   residual is **$2.6\times10^{-16}$** (machine zero) at 12 random $(t,x)$ — the *specific* MI inertial
   dressing conserves its stress tensor on-shell. The $\rho_m$ (dust) sector adds the standard
   perfect-fluid piece, conserved by continuity.

**Frame-constraint consistency.** $u\!\cdot\!u=-1$ is dynamically preserved: $\tfrac{d}{d\tau}(u\!\cdot\!u)=2\,u\!\cdot\!a$
and $u\!\cdot\!a=0$ on the unit-norm surface (`rederive_identity.py` [I]); $\lambda$ is fixed algebraically
(2nd-class pair, no tertiary tower). The passive frame stays passive under the matter coupling — **0
propagating frame dof**. **No composition dependence and no conservation breakage were found** — the WEP
and conservation results are structural wins, verified as hard as any deficit.

---

## 4. $a_0=cH_\Lambda/Z$ is the single, unrenormalized scale (question 4)

**Single scale.** $a_0$ enters $T_{\mu\nu}$, $E_u$, and $E_\lambda$ **only** through the argument
$X=|a|^2/a_0^2$ of $K$. No other scale appears in the matter coupling. **Both footings** just rescale $X$
— the tensor **structure** ($\alpha,\beta,\gamma$ decomposition, slip, conservation) is identical; only the
number differs:

| footing | $a_0$ (m s$^{-2}$) | $X(|a|=10^{-10})$ | $K(X)$ |
|---|---|---|---|
| canonical $\rho_{\rm DE}$, $cH_\Lambda/Z$ | $9.36\times10^{-11}$ | $1.141$ | $0.636$ |
| alternate $\rho_{\rm total}/cH_0$ | $1.13\times10^{-10}$ | $0.783$ | $0.584$ |

**Not renormalized by the matter coupling.** The coupling introduces no new scale, and the one-loop dS
result already shows $a_0$ is neither additively nor multiplicatively renormalized
(`MI_COMPLETION_WRITTEN_2026-07.md:43`; `oneloop_laneA_divergences.py`). Re-derived here from the same
positive Herglotz–Nevanlinna measure that $T_{\mu\nu}$ inherits (`operator_definition.py:124-140`):
- **Sum rule** $\displaystyle\int \frac{d\mu(t)}{|t|}=K(\infty)-K(0)=1$ — unit resolvent weight, so there is
  **nothing spare to feed a $z^0$ tadpole** (numeric $1.00000$, robust $T=u^2$ quadrature).
- $K(0)=0$ from the exact measure (numeric $-1.3\times10^{-6}$): the deep-MOND DC part drops, no tadpole seed.

Because $K$ is a positive superposition of local massive resolvents (`MI_COMPLETION_WRITTEN_2026-07.md:43`),
$T_{\mu\nu}=\int d\mu(t)\,T^{\rm local}_{\mu\nu}(t)$ with $a_0$ living **only** in the argument — the matter
coupling generates **no counterterm at the scale $a_0$**. [DERIVED.]

---

## 5. Verdict and honest ledger

| # | Result | Status |
|---|---|---|
| B1 | **Coupling term explicit**: matter minimal on $g$; MI = universal scalar dressing $s\,u^\mu K(\Box_u/a_0^2)u_\mu$ of the matter kinetic term, through the worldline's own 4-acceleration $a^\mu$; **not** a disformal matter metric | **DERIVED** |
| B2 | **WEP exact, $\eta=0$** — the dressing carries no species label | **DERIVED (win)** |
| B3 | **Three variations done**: $\delta/\delta\lambda$ = unit constraint; $\delta/\delta u$ = frame eq with $\ell=0$ source soaked by $\lambda=-\rho_m sK$, no tertiary tower; $\delta/\delta g$ = $T_{\mu\nu}=\alpha u_\mu u_\nu+\beta g_{\mu\nu}+\gamma a_\mu a_\nu$ | **DERIVED** |
| B4 | **Principal $T_{\mu\nu}$ isotropic ⇒ no slip** ($\Psi=\Phi$); only anisotropic stress $\gamma\,a_\mu a_\nu$ ($\propto K'$) lives in the MOND/IR | **DERIVED structure** |
| B5 | **$\nabla_\mu T^{\mu\nu}=0$ on-shell** — diff-invariance theorem + canonical Noether identity (generic exact + MI-kernel residual $2.6\times10^{-16}$); no conservation breakage | **DERIVED (win)** |
| B6 | **Frame constraint preserved** ($u\!\cdot\!a=0$; $\lambda$ algebraic; 0 frame dof) | **DERIVED** |
| B7 | **$a_0$ single scale, unrenormalized** by the coupling (sum rule $\int d\mu/|t|=1$, $K(0)=0$; both footings one structure) | **DERIVED** |

**Open edges (not papered over).**
- The $T_{\mu\nu}$ above uses the **first-moment (quasistatic) closure** — exact on circular orbits; the
  off-circular ordering (**gap A**) is FREE, so the full **nonlocal** $T_{\mu\nu}$ differs off-circles by
  that same undetermined closure.
- The **exact IR magnitude and higher multipoles** of the anisotropic $\gamma\,a_\mu a_\nu$ stress — the
  curved $\delta S_{\rm matter}/\delta g$ with the connection piece of $a^\mu$, i.e. the lensing
  *enhancement / unification* question (**gap C**) — remain the named open classical computation. Present
  in the tensor and of the right order; magnitude not yet pinned.
- **$s=-1$** and **$a_0$'s value** stay POSTULATED. No completeness / TOE claim.

**Bottom line.** Matter couples as a universal, WEP-exact inertial-scalar dressing through its own
4-acceleration; the full metric stress tensor is $T_{\mu\nu}=\alpha u_\mu u_\nu+\beta g_{\mu\nu}+\gamma a_\mu a_\nu$
with an isotropic (no-slip) principal part and an IR-only anisotropic $a_\mu a_\nu$ term; it is
**covariantly conserved on-shell** (Noether identity, machine-verified for the MI kernel) with an $\ell=0$
frame source soaked by $\lambda$ (no $\ell=2$ Bianchi lock); and $a_0=cH_\Lambda/Z$ is the **single,
unrenormalized** scale. Gap B is **closed at the tensor-structure + conservation level**; its residual
(the exact nonlocal/curved IR magnitude) coincides with gaps A and C and is reported open.

---

### Reproduction
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_field_theory
python3 matter_coupling_Tmunu.py     # exit 0; 14 checks: coupling+WEP, 3 variations, T_munu, conservation, a0 single-scale
```
Sources read (frozen read-only repo `zimmerman-formula/`): `real_research/papers/MI_COMPLETION_WRITTEN_2026-07.md`,
`real_research/reviews/mi_formal_completion_2026/` (`operator_definition.py`, `constraint_structure.py`,
`A10_dirac_block.py`, `oneloop_laneA_divergences.py`, `mi_lensing_from_stress_tensor.py`,
`crux_variation_check.py`, `principal_symbol_blockdiag.py`). Local prep: `BASELINE_ACTION.md`,
`rederive_identity.py`. Program concept DOI 10.5281/zenodo.21253644; loop arc 21284144.

*Both $a_0$ footings throughout. Each claim flagged derived / postulated / open. $s=-1$ postulated, $a_0$'s
value underived. No completeness or theory-of-everything claim.*
