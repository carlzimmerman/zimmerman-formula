# The Baseline de Sitter–Unruh Modified-Inertia Action — Consolidated Statement

**Purpose.** A single, self-contained statement of *the most complete action currently established* for
the Zimmerman de Sitter–Unruh **modified-inertia** framework, with every term traced to a committed,
runnable script or published equation (file:line), and a clean DERIVED-vs-POSTULATED ledger. This is the
consolidation baseline for the "full field theory of MI" goal — it is **not** a claim that the theory is
complete. The three genuine completion gaps (closure/ordering map, matter coupling + full Tμν,
unification of dynamics and lensing) are named at the end and left open.

**Organizing scale (the whole point).**
$$a_0 = \frac{cH_\Lambda}{Z} = c^2\sqrt{\frac{\Lambda}{32\pi}} = 9.36\times10^{-11}\ \mathrm{m\,s^{-2}}\quad(\text{canonical, }\rho_{\rm DE}),\qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.78881.$$
ALT footing $\rho_{\rm total}/cH_0 \to 1.13\times10^{-10}$. **Both footings carried throughout.** Inertia is
modified (not gravity) at $|a|\lesssim a_0$; the passive frame $u^\mu$ is the cosmic rest frame
(dS-Unruh/CMB); the nonlocal kernel $K(\Box_u/a_0^2)$ carries the trajectory memory. The framework's OWN
interpolation is $\nu(y)=\sqrt{1+1/y}$, $y=g_{\rm bar}/a_0$, giving $g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$
(NEVER McGaugh's $\nu$).

Provenance root: the frozen read-only repo `zimmerman-formula/`. Primary published statement:
`real_research/papers/MI_COMPLETION_WRITTEN_2026-07.md` (v13; Zenodo concept 21253644, loop arc DOI 21284144).

---

## 1. The single most-complete action currently established

With signature $(-+++)$, host GR unmodified, the established action is a **three-piece single-metric**
functional $S[g_{\mu\nu},u^\mu,\lambda,\psi_{\rm matter}]$:

$$\boxed{\,S = \underbrace{\frac{c^4}{16\pi G}\!\int\!\sqrt{-g}\,R}_{S_{\rm EH}[g]}
\;\underbrace{-\int\!\sqrt{-g}\,\frac{\lambda}{2}\big(u^\mu u_\mu+1\big)}_{S_u[g,u,\lambda]\ (\textbf{passive frame})}
\;\underbrace{-\frac12\int\!\sqrt{-g}\,\rho_m\big[\,s\,u^\mu K(\Box_u/a_0^2)u_\mu\,\big]}_{S_{\rm matter}[g,u,\psi]\ (\textbf{MI content})}\,}$$

$$K(z)=\frac{\sqrt{1+4z}-1}{2\sqrt z},\qquad \Box_u f=u^a\nabla_a(u^b\nabla_b f),\qquad s=-1\ (\textbf{postulate}).$$

**Term-by-term provenance.**

| Term | Content | Established status | file:line provenance |
|---|---|---|---|
| $S_{\rm EH}$ | standard Einstein–Hilbert; host gravity **unmodified** | GR, no MI in metric sector | `MI_COMPLETION_WRITTEN_2026-07.md:19` |
| $S_u$ | unit-timelike constraint on $u^\mu$ via Lagrange multiplier $\lambda$; **no aether kinetic term** | frame is **passive**: 0 propagating dof (machine-verified Dirac closure) | action `MI_COMPLETION_WRITTEN_2026-07.md:19`; dof `constraint_structure.py`, `A10_dirac_block.py` |
| $S_{\rm matter}$ | MI lives in the **matter kinetic sector**: $\rho_m$ dressed by $s\,u^\mu K(\Box_u/a_0^2)u_\mu$ | worldline sector machine-verified | `MI_COMPLETION_WRITTEN_2026-07.md:20`; `oneloop_laneA_divergences.py:5-9` |
| $K(z)$ | non-polynomial kernel, single branch cut, single healthy pole (residue +1) | rigorously defined (Herglotz–Nevanlinna, positive measure) | `operator_definition.py:52`, `:124-140` |
| $\Box_u$ | directional (along-$u$) wave operator $(u\!\cdot\!\nabla)^2$; ultralocal on dS ($\partial_\tau^2+3H\partial_\tau$) | essentially self-adjoint on passive-$u$ background | `operator_definition.py:57-67`; dS form `SETUP.md:50-51` |
| $\lambda$ | fixed algebraically **on-shell** by the $u$-equation: $\lambda=-\rho_m s$ (no tertiary tower) | derived (Dirac analysis) | `MI_COMPLETION_WRITTEN_2026-07.md:39` |
| $s=-1$ | the MOND-sign choice | **POSTULATE** (not derived anywhere) | `MI_COMPLETION_WRITTEN_2026-07.md:21` |
| $a_0$ | value $cH_\Lambda/Z$ | **value POSTULATED** (one-parameter EFT; $\kappa=1/2$ unforceable) | `MI_COMPLETION_WRITTEN_2026-07.md:21`; footing MEMORY `project_zimmerman_coefficient_footing` |

**Equivalent worldline (Galley doubled) form** used for phenomenology: the conservative gradient
$G(a)^\mu = a^\mu\,\mu_{\rm fw}(|a|/a_0)$ with $\mu_{\rm fw}$ the exact inverse of $\nu(y)=\sqrt{1+1/y}$;
the external-field kernel $\theta(y)=\theta_0/(1+(\theta_0-1)y^2)$, $\theta_0=\sqrt2$ (shape forced by the
dS Wightman function). Provenance `MI_COMPLETION_WRITTEN_2026-07.md:21`.

**Reduction to phenomenology (the load-bearing bridge, re-derived here — §3).** The nonlocal operator
reduces to the algebraic inertia dressing through the **first-moment closure**:
$$K(\Box_u/a_0^2)\ \xrightarrow{\text{first moment}}\ K(|a|^2/a_0^2)=\mu_{\rm fw}(|a|/a_0),$$
which on a circular orbit inverts *exactly* to $g_{\rm obs}=\nu(y)\,g_{\rm bar}$ at every radius. The
enabling identity is $u_\mu\Box_u u^\mu=-|a|^2$ (any timelike worldline).

**Lensing sector — currently SEPARATE (two candidate constructions, neither unified into the box above).**
1. **Disformal photon metric** (preferred, framework-native): light propagates on
   $\tilde g_{\mu\nu}=g_{\mu\nu}+B\,u_\mu u_\nu$ with $B$ fixed by the *same* $\nu$ the RAR uses; matter keeps
   MI in $g$. Universal, Cassini-safe ($|\Delta\gamma|\sim10^{-13}$ at the Sun), ghost-free/causal
   nonlinearly, $B$ fixed non-locally by the framework's own $K(\Box_u)$ (AQUAL-type potential).
   Provenance `MI_COMPLETION_WRITTEN_2026-07.md:45-49`; scripts `mi_disformal_lensing.py`,
   `mi_disformal_ghostfree.py`, `mi_disformal_ostrogradsky.py`, `mi_disformal_locality.py`. The one
   residual: explicit $K(\Box_u)$ lensing solve for a specific non-spherical galaxy.
2. **Branch-B elastic medium** (alternative, modified-gravity-with-a-medium): a relativistic two-invariant
   elastic solid, $S=\int\sqrt{-g}\big[\frac{c^4(1+h(J))R}{16\pi G}-\rho_\Lambda c^2\,\mathcal E(J,\Sigma)\big]$,
   the relaxed medium *is* the dark energy. Provenance `ELASTIC_MEDIUM_ACTION_2026.md:11-13`. **Honest
   standing: evidence-tilted to FAIL Cassini** — the deciding shear Poisson ratio $\beta$ is a free material
   scalar and every *natural* value marginally fails ($\times1.1$–$1.8$ over the ceiling)
   (`ELASTIC_MEDIUM_ACTION_2026.md:47`). The lens-only slip sector ($c_T=1$ exact, FRW quietness) is banked
   in `agentY_quasistatic.out`/`agentY_eqs.pkl` (repo-root copies of `real_research/reviews/toe_law/agentY_*`;
   the root `agentY_gates.out` is a *truncated* older copy — see `SETUP.md:99-110`).

**The unification question (gap C) is therefore OPEN**: it is not established that ONE action yields both
the MI dynamics kernel and the lensing. The disformal route derives $B$ from the same $K(\Box_u)$ (so it is
"one nonlocality, two roles") but the explicit non-spherical solve is not done; the elastic route is a
*separate* action tilted to fail. Reported as open, not papered over.

---

## 2. Degrees of freedom and hard constraints (what the action must never break)

- **Propagating content = 2 (graviton) + 2 (photon).** The frame $u^\mu$ carries **0** propagating dof
  (passive). Machine-verified: the curved-spacetime Dirac–Bergmann analysis terminates at the secondary
  level; the unit-norm pair is genuinely second-class with Dirac block determinant $4(u\!\cdot\!u)^2\to4$
  on-shell; frame-sector count $=\frac12[10-0-10]=0$. Provenance `MI_COMPLETION_WRITTEN_2026-07.md:39`;
  `constraint_structure.py`, `A10_dirac_block.py`.
- **The "$u$ inside $\Box_u$" crux resolves negatively** (no induced kinetic term): exact quadratic symbol
  $S_n=(-1)^n k_\perp^2 k_0^{2n}$, whose only root is $k_0=0$ independent of spatial $k$ — a
  transport-along-$u$ ODE, no wave cone, zero group velocity. `MI_COMPLETION_WRITTEN_2026-07.md:11,39`;
  `transverse_mode_analysis.py`, `principal_symbol_blockdiag.py`.
- **$K(\Box_u)$ rigorously defined**: Herglotz–Nevanlinna function of $z$, unique positive Borel measure,
  closed-form density $\rho_A=(1-\sqrt{1-4|t|})/(2\pi\sqrt{|t|})$ on $-\tfrac14<t<0$,
  $\rho_B=1/(2\pi\sqrt{|t|})$ on $t<-\tfrac14$; $\|K\|\le1$ (operator-monotone), causal-retarded, additive
  constant $a=0.65411$. Provenance `operator_definition.py:124-140`; `oneloop_laneA_divergences.py:24-26`.
- **HARD constraint $c_T=1$** (GW170817): satisfied — disformal metric leaves tensor modes at $c$
  (`agentY_quasistatic.out`); elastic medium's tensor sector is standard GR (`ELASTIC_MEDIUM_ACTION_2026.md:32`).
- **HARD constraint Cassini/solar-system**: the MI realization evades the quadrupole by $\sim7$ orders
  ($\nu-1\approx7\times10^{-7}$ deep-Newton); the MG realization fails at $+6$ to $+14\sigma$.
  `MI_COMPLETION_WRITTEN_2026-07.md:25`. **Caveat (MEMORY `project_directional_efe_test`, `project_cluster_standing`):**
  the $\gamma$-pass is MOND-shared and the $Q_2$ quadrupole is an inherited $3$–$15\sigma$ tension for the
  *AeST(=MG)* limb — Cassini is NOT a clean in-hand discriminator; the MI evasion above is the passive-frame
  reading, which is the point of the whole construction.

---

## 3. Independent re-derivation of the load-bearing kinematics (`rederive_identity.py`, exit 0)

The bridge from the nonlocal action to the RAR rests on two facts. Both were **re-derived from scratch**
here (not trusted from the banked `rb1_circular_exactness.py`), and the banked claim is **confirmed and
strengthened**.

**(I) The first-moment identity $u_\mu\Box_u u^\mu=-|a|^2$ — WORLDLINE-GENERAL.**
The task asked explicitly: is it worldline-general, or does it need circularity? Answer, established three
independent ways in `rederive_identity.py`:
- **[I.A] Flat, fully general worldline (off-shell master identity):** for *arbitrary* $u^\mu(\tau)$,
  $\frac{d}{d\tau}(u\!\cdot\!a)=a\!\cdot\!a+u\!\cdot\!(\Box_u u)$ identically (pure Leibniz). On the
  constraint surface $u\!\cdot\!u=-1\Rightarrow u\!\cdot\!a=0\Rightarrow u\!\cdot\!\Box_u u=-|a|^2$.
- **[I.B] General curved metric, general worldline:** same off-shell master identity verified symbolically
  with an *arbitrary* $g_{ab}(x)$ and full Christoffel connection. The only inputs are the product rule and
  metric compatibility ($\nabla g=0$) — **no** circularity, geodesy, or spacetime symmetry.
- **[I.C] Concrete curved, non-geodesic, non-circular check:** the static Schwarzschild observer (manifestly
  not circular, not freely falling) gives $u\!\cdot\!\Box_u u = M^2/[r^3(2M-r)] = -|a|^2$ in closed form.

**Verdict:** the identity needs *only* unit norm + metric compatibility. It is worldline-general; the RB
banked claim ("ANY worldline, curved space too") is **correct** and now backed by an independent general-metric
symbolic proof plus a concrete example (the banked version verified flat + asserted curved; this closes that
gap). Hence $\langle\Box_u\rangle_u\equiv(u\!\cdot\!\Box_u u)/(u\!\cdot\!u)=+|a|^2$ exactly, for every
timelike worldline.

**(II) The first-moment closure and the exact RAR.**
- $K(0^+)=0$, $K(\infty)=1$, and $K(x^2)=\mu_{\rm fw}(x)$ exactly.
- The circular balance $\mu_{\rm fw}(x)\,x=y$ inverts *exactly* to $x=y\,\nu(y)$ (the nested radical
  collapses because $1+4(y^2+y)=(2y+1)^2$), so $g_{\rm obs}=\nu(y)\,g_{\rm bar}$ at **every** radius; numeric
  ring residual $7\times10^{-13}$ (algebraic — no radius mixing, no field equation).
- $\nu(y)\,g_{\rm bar}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$ to $<10^{-12}$, **both footings**.

**(II.b) Honesty check — the closure is the exact FIRST moment and no more.**
On the exact helix, $u\!\cdot\!\Box_u^n u$ matches the prescription $(a^2)^n(u\!\cdot\!u)$ **only at $n=1$**;
the $n=2$ ratio is $1-1/v^2=-1/(\gamma^2v^2)$, diverging as $v\to0$ — the moment expansion is *uncontrolled*
beyond first order. The **literal** frequency-domain evaluation gives $|K(-w^2)|\approx1$ (NO MOND) at every
orbital frequency, differing from the prescription at $O(1)$. So the reduction is a genuine *choice* of
closure (the first-moment family), exact on circles (where $|a|$ is constant) and **free off circles**. This
is the theory's real open structure, re-derived not asserted.

---

## 4. DERIVED-vs-POSTULATED ledger of the existing theory

### DERIVED (proven, machine-verified, no knobs)
| # | Statement | Provenance |
|---|---|---|
| D1 | **Frame dof = 0** — passive frame, machine-verified curved Dirac closure (2nd-class block det $=4$, no tertiary tower) | `constraint_structure.py`, `A10_dirac_block.py`; `MI_COMPLETION_WRITTEN_2026-07.md:39` |
| D2 | **No induced aether kinetic term** — no-wave-cone symbol $S_n=(-1)^nk_\perp^2k_0^{2n}$, all orders | `transverse_mode_analysis.py`, `principal_symbol_blockdiag.py` |
| D3 | **$K(\Box_u)$ is Herglotz–Nevanlinna with a unique positive measure**, $\|K\|\le1$, causal-retarded ($\rho_A,\rho_B$ closed-form, $a=0.654$) | `operator_definition.py:124-140` |
| D4 | **First-moment identity $u_\mu\Box_u u^\mu=-|a|^2$, worldline-general** (re-derived 3 ways here) | `rederive_identity.py` [I.A/B/C] |
| D5 | **Ring-exact RAR** $g_{\rm obs}=\nu(y)g_{\rm bar}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$, both footings, residual $\sim10^{-13}$ | `rederive_identity.py` [II]; `rb1_circular_exactness.py` |
| D6 | **Newton, deep-MOND, BTFR $v^4=GMa_0$, $\sqrt2$-DC-weight EFE kernel, ghost-freedom** (single healthy pole) | `MI_COMPLETION_WRITTEN_2026-07.md:23-25` |
| D7 | **Causal, ghost-free two-point propagator**; Källén–Lehmann positivity across the whole cut; principal symbol = GR light-cone | `MI_COMPLETION_WRITTEN_2026-07.md:33-35`; `mi_propagator_2026/` |
| D8 | **Nonlinear classical stability / principal-symbol well-posedness** (hyperbolicity inherited from GR via $K\to1$ UV) | `stability.py`, `principal_symbol_blockdiag.py` |
| D9 | **MI evades the Cassini quadrupole** by $\sim7$ orders (passive-frame reading); MG limb fails $+6$–$14\sigma$ | `MI_COMPLETION_WRITTEN_2026-07.md:25` |
| D10 | **One-loop dS: $a_0$ unrenormalized** (no $z^0$ tadpole; sum rule $\int d\mu/|t|=1$ exact), linear vertex zero all orders (geodesy theorem), **no transverse $(\nabla u)^2$**, dressed KL+KMS positivity | `mi_oneloop_desitter.py`, `oneloop_lane{A,B,C}.py`; sum rule `oneloop_laneA_divergences.py:131-143` |
| D11 | **$a_0$ additive non-renormalization all-orders exact** (shift symmetry $T\to T+c$ + unit-norm); two-loop matter- and graviton-sector transverse aether term not generated (at divergence level) | `twoloop_laneC_a0.py`, `twoloop_aether_resolution.py`, graviton census `twoloop_graviton_*.py` |
| D12 | **One-loop finite parts bounded below** ($\|K\|\le1$, $s=-1$ confine $M^2\in(0,m^2]$); dS IR regulated by friction gap $3H/2$ | `twoloop_laneA_finite.py` (mislabeled — is the one-loop finite lane; `SETUP.md:16-21`) |
| D13 | **Disformal lensing kinematics**: $\tilde g=g+Bu_\mu u_\nu$ ghost-free, causal, Cassini-safe, $B$ fixed by the same $K(\Box_u)$; $c_T=1$ | `mi_disformal_*.py`; `agentY_quasistatic.out` |

### POSTULATED / FREE / OPEN (named, not tuned away)
| # | Statement | Status | Provenance |
|---|---|---|---|
| P1 | **MOND sign $s=-1$** | POSTULATE (also sets the dissipation sign) | `MI_COMPLETION_WRITTEN_2026-07.md:21` |
| P2 | **$a_0$'s VALUE $cH_\Lambda/Z$** | POSTULATE — one-parameter EFT; $Z$/$\kappa=1/2$ **provably unforceable** (ghost-freedom+unitarity+holography) | MEMORY `project_zimmerman_coefficient_footing`; `MI_COMPLETION_WRITTEN_2026-07.md:11` |
| P3 | **$a_0$ footing** ($\rho_{\rm DE}/cH_\Lambda\to9.36$ vs $\rho_{\rm tot}/cH_0\to1.13\times10^{-10}$) | FORK — both carried; decisive tests still degenerate | MEMORY `project_zimmerman_coefficient_footing` |
| P4 | **The closure/ordering map beyond the first moment** (gap A) | **FREE, bounded** — literal-frequency closure is DEAD (no MOND + secular drift $a_0/2c$); only the first-moment *family* survives, ring-exact but off-circular undetermined | `rederive_identity.py` [II.b]; `rb1`/`rb3`; `mi_offcircular_completion_SPEC.py` |
| P5 | **The measure IF not pinned** | Actually PINNED: Herglotz class + RAR calibration $\Rightarrow$ unique (identity theorem). Not free. | `KERNEL_THEORY.md` §2 |
| P6 | **Matter coupling + full $T_{\mu\nu}$** (gap B) | OPEN — $T_{\mu\nu}=-\frac{2}{\sqrt{-g}}\delta S_{\rm matter}/\delta g$ and on-shell $\nabla^\mu T_{\mu\nu}=0$ **not computed**; established only at frame-equation ($l=0$ source) and principal-symbol ($l=0$ isotropic) order. A finite classical calculation, **not walled** | `MI_COMPLETION_WRITTEN_2026-07.md:31`; `mi_lensing_from_stress_tensor.py` |
| P7 | **Unification of dynamics + lensing** (gap C) | OPEN — disformal route derives $B$ from the same $K(\Box_u)$ but the non-spherical solve is undone; elastic route is a *separate* action **evidence-tilted to fail Cassini** | `MI_COMPLETION_WRITTEN_2026-07.md:49`; `ELASTIC_MEDIUM_ACTION_2026.md:47` |
| P8 | **$\rho_m$ proxy** ($=m^2\phi^2$) in the loop sector; the $T_{\mu\nu}$/disformal-$\rho_m$ variant | OPEN/proxy — divergence results argued to survive since $W_{\rm dS}=0$, not computed; finite fork P (proxy-literal) vs fork C (composite) | `SETUP.md:211-229` |
| P9 | **Finite one-loop coefficient function** (candidate $\delta\nu(y)$); all-$n$ TT-vertex zero; finite nonlocal parts; genuinely higher loops | OPEN — TT vertex CAS-proven $n=1,2$ only; the "all orders $n$" script `mi_oneloop_tt_vertex_all_n.py` has **hard-coded `True`** checks (lines 56,66) — do NOT lean on it | `SETUP.md:62-68,91-97` |

**Bottom line of the ledger.** The **statics** are in excellent shape: the action is written, the frame is
provably passive (0 dof), the kernel is a rigorous positive-measure Herglotz operator, the RAR is
ring-exact and worldline-derived, and the loop structure protects $a_0$ at one and (divergence-level) two
loops. The **three completion gaps are real and honestly open**: (A) the off-circular closure map is FREE
(only the first-moment family is pinned, and only on circles), (B) the full metric stress tensor $T_{\mu\nu}$
and its conservation are uncomputed, (C) dynamics+lensing are not yet one action. Plus the two irreducible
inputs: $s=-1$ and $a_0$'s value. **This is a one-scale effective field theory carried to a sharp, named
boundary — not a finished theory and not a TOE** (the earlier TOE/SM claims were publicly retracted 2026-06-23
and are not reasserted).

---

## 5. Reproduction

```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_field_theory
python3 rederive_identity.py      # exit 0; 18 checks: worldline-general identity (3 ways) + first-moment closure + honesty
```
Sources read (READ-ONLY frozen repo `zimmerman-formula/`): `real_research/papers/MI_COMPLETION_WRITTEN_2026-07.md`,
`real_research/papers/ELASTIC_MEDIUM_ACTION_2026.md`, `real_research/reviews/mi_formal_completion_2026/`
(`operator_definition.py`, `constraint_structure.py`, `A10_dirac_block.py`, `oneloop_laneA_divergences.py`,
`mi_oneloop_desitter.py`, `twoloop_laneA_finite.py`, `twoloop_laneC_a0.py`, `mi_disformal_*.py`),
`agentY_quasistatic.out`/`agentY_eqs.pkl` (repo root). Local prep sources:
`prep_2026/mi_fingerprint/{rb1_circular_exactness.py,KERNEL_THEORY.md,RING_RESULTS.md}`,
`prep_2026/oneloop_finite/SETUP.md`. Program concept DOI 10.5281/zenodo.21253644; loop arc 21284144.

*Both $a_0$ footings throughout. Every element flagged derived / postulated / open. $s=-1$ postulated,
$a_0$'s value underived. No completeness or theory-of-everything claim.*
