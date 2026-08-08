# A local, generally covariant field theory of modified inertia

**Carl P. Zimmerman**
Briar Creek Tech

*Version 1 (2026-08-08).*

---

## The theory in one box

$$\boxed{\;S \;=\; S_{\rm EH}[g] \;+\; S_{\rm kh}[g,T] \;+\; S_{\chi}[g,u,\chi] \;+\; S_{\rm m}[g,T,\chi,x]\;}$$

$$S_{\rm kh}=\frac{1}{16\pi G}\!\int\! N\sqrt{h}\Big[K_{ij}K^{ij}-\lambda K^{2}+\xi R^{(3)}+\eta\,a_{i}a^{i}\Big],
\qquad a_{i}=\partial_{i}\ln N,\qquad n_{\mu}=-\frac{\partial_{\mu}T}{\sqrt{-(\partial T)^{2}}}$$

$$(u^{\mu}\partial_{\mu}+m)^{2}\chi = \frac{g\,|a|}{c},
\qquad
S_{\rm m}=-mc^{2}\!\int\!\Big[\mu(\chi)\,d\tau+\big(1-\mu(\chi)\big)\,dt\Big]$$

Three things are true of this action that were not true of the worldline construction it completes
[1]:

1. **It is local.** The memory kernel is gone — replaced by an auxiliary field $\chi$ whose
   retarded Green's function *is* that kernel (§2).
2. **It is generally covariant.** The preferred frame is the normalised gradient of a scalar, so the
   Lorentz violation is spontaneous rather than stipulated (§3).
3. **Its propagating content is 2 + 1 + 0 = 3 modes, and all three are healthy** in an explicit
   nonempty window (§4).

And the acceleration scale is no longer the first moment of a postulated kernel:

$$\boxed{\;a_{0}=\tfrac{2}{3}\,c\,\frac{m^{2}}{g}\;}$$

**the ratio of the auxiliary field's mass squared to its coupling.** Together with the companion
no-go result [2] — that this moment is logarithmically divergent, so it cannot be computed from a
free-field correlator — this means $g/m^{2}$ is a *renormalised coupling*. Which is what every
coupling in every local field theory is.

**The honest caption, which must travel with the box.** $a_{0}$'s *value* is still not derived, and
the covariantisation *added* two free parameters ($\lambda,\eta$) rather than removing any. The
theory is complete in the sense that a local, covariant, ghost-free action exists and yields MOND;
it is not complete in the sense of predicting its own constants. And it says nothing whatever about
particle physics — see §8.

---

## 1. What was missing

Reference [1] gives a worldline action reproducing Milgrom's modified-inertia relation via the
*rapidity gap*, $\cosh\theta = -u\!\cdot\!u'/c^{2}$, with the memory encoded in a kernel $K(s)$
whose first moment satisfies $M_{1}=\tfrac{2}{3}c/a_{0}$. Three things were owed:

- **Nonlocality.** $\Theta(\tau)=\int_{0}^{\infty}\!ds\,K(s)\,\theta(\tau,\tau-s)$ has no local
  derivative expansion, so there is no effective-field-theory power counting and no Hamiltonian.
- **Ghosts.** The equation of motion is fourth order in $x$. Ostrogradsky's theorem does not apply,
  because it requires a *local* higher-derivative Lagrangian — but that is a statement about the
  theorem's silence, not a proof of ghost-freedom.
- **A stipulated frame.** The action uses $dt$, the cosmological time, and a fixed timelike $n^{\mu}$.
  That breaks general covariance by hand, and it makes the paper's Lorentz-violation prediction
  dismissible as an artefact of choosing $n$.

This paper discharges all three. Each section's claims are produced by a committed script that
exits non-zero on any internal failure and carries negative controls that must trip (§9).

---

## 2. Step 1: the kernel is a local field

**The reduction.** For a general worldline the rapidity gap obeys
$\theta(\tau,\tau-s)=(s/c)\,|a(\tau-s/2)|+O(s^{3})$ [1] — the gap across an interval is $s/c$ times
the acceleration magnitude at the **midpoint**. So $\Theta$ carries both a factor of $s$ and a lag
of $s/2$. Substituting $s=2u$ collapses *both* into one kernel:

$$\Theta(\tau)=\int_{0}^{\infty}\!du\;G(u)\,J(\tau-u),\qquad G(u)=4u\,K(2u),\qquad J=|a|/c .$$

For the minimal causal kernel $K(s)=(N/\lambda)e^{-s/\lambda}$ this is

$$G(u)=g\,u\,e^{-mu},\qquad m=\frac{2}{\lambda},\qquad g=\frac{4N}{\lambda},$$

whose zero-frequency gain is $\int_{0}^{\infty}G\,du=g/m^{2}=N\lambda=M_{1}$ **exactly**: the
kernel's first moment *is* the local operator's DC gain.

**Theorem 1.** *$g\,u\,e^{-mu}$ is the retarded Green's function of $(d/d\tau+m)^{2}$.*

Verified three independent ways: it solves the homogeneous equation for $u>0$; its jump conditions
are $G(0)=0$, $G'(0)=g$, so $(d/du+m)^{2}G=g\,\delta(u)$; and its Laplace transform is
$g/(p+m)^{2}$. Hence

$$\boxed{\;\ddot{\chi}+2m\dot{\chi}+m^{2}\chi=\frac{g\,|a|}{c},\qquad \Theta=\chi\;}$$

— **a damped oscillator whose friction term *is* the memory.** This is closed numerically as well as
formally: integrating the local ODE forward with retarded data reproduces the nonlocal convolution
to $10^{-23}$, and perturbing $m$ by 5% breaks that agreement by $5\times10^{-2}$.

**The damping is critical, exactly, and it is forced.** The discriminant of $p^{2}+2mp+m^{2}$
vanishes identically; there is a double root at $p=-m$. And for $K\sim s^{k}e^{-s/\lambda}$ the local
operator has order $k+2$, so the exponential kernel gives the *minimal* localisation. The extra
factor of $u$ traces to the rapidity gap being **linear in $s$** — which is the same fact that, in
the companion paper [2], places the required kernel moment exactly on the pole of $\zeta$. One
structural feature, three consequences.

**The ghost question becomes a computation.** Enforcing the constraint with a multiplier $\pi$, the
adjoint of $(d/d\tau+m)^{2}$ is $(d/d\tau-m)^{2}$ — *anti*-damped, the Bateman mirror — and the
$(\Theta,\pi)$ kinetic form is off-diagonal, with eigenvalues $\pm\tfrac12$ and signature $(+,-)$.
By the naive criterion, a ghost. **It is not a new degree of freedom.** $\pi$ is a *costate*: it
carries a final-value condition rather than Cauchy data, it decays going backward
($|\pi|\sim e^{-m(T-\tau)}$, bounded by 1 on the physical interval), and the count closes exactly —
2 conditions on $\Theta$ plus 2 on $\pi$ = 4, which is the order of the fourth-order equation of
motion in $x$ already derived in [1]. The indefinite metric is the Keldysh $(-)$ branch of the
in-in formalism the construction already uses. This *replaces* the "Ostrogradsky is silent" argument
with a positive statement.

**$a_{0}$ becomes a coupling ratio.** From $a_{0}=\tfrac23 c/M_{1}$ and $M_{1}=g/m^{2}$:

| footing | $M_{1}$ (Gyr) | $\lambda$ (yr) | $m$ (s$^{-1}$) | $g$ (s$^{-1}$) | $N$ | $a_{0}$ rebuilt |
|---|---|---|---|---|---|---|
| canonical | 67.65 | $3.2\times10^{4}$ | $1.9805\times10^{-12}$ | $8.374\times10^{-6}$ | $2.114\times10^{6}$ | $9.3619\times10^{-11}$ |
| ALT ($\times1.2048$) | 56.15 | $3.2\times10^{4}$ | $1.9805\times10^{-12}$ | $6.951\times10^{-6}$ | $1.755\times10^{6}$ | $1.1279\times10^{-10}$ |

reproducing $a_{0}$ to $10^{-25}$ on both footings, with the implied kernel weight matching the
independently derived bound $N\ge2.1\times10^{6}$ of [1].

**Costs, in the same breath.** (i) The localisation is exact for the *midpoint* form and only
third-order accurate for the exact bilocal action; galactically $\lambda\Omega=8.8\times10^{-4}$, so
the relative error is $O((\lambda\Omega)^{2})=7.7\times10^{-7}$ — small, not zero. (ii) In $x$ the
localised system is *second*-derivative, because the source is $|a|$, so **Ostrogradsky is not
evaded in the localised writing.** The exact action contains only $u$, so this is an artefact of the
midpoint expansion — which is precisely why "Ostrogradsky-free" and "fourth-order equation of
motion" coexisted in [1] rather than contradicting each other. (iii) **Exact localisation of the
full bilocal $\cosh^{-1}(-u\!\cdot\!u'/c^{2})$ is not available by this route at all**: the
auxiliary-propagator trick requires linearity in the delayed field. A genuine limitation.

Covariantly, $(u^{\mu}\partial_{\mu}+m)^{2}\Theta=g|a|/c$ is a scalar advected by the matter flow
obeying second-order relaxation — structurally the Israel–Stewart class [3], whose purpose was to
restore the causality and hyperbolicity that first-order dissipative hydrodynamics destroys. A
route and an analogy; no Israel–Stewart result is imported.

---

## 3. Step 2: the preferred frame becomes dynamical

Replace $n^{\mu}$ by the normalised gradient of a scalar khronon,
$n_{\mu}=-\partial_{\mu}T/\sqrt{-(\partial T)^{2}}$. It is unit timelike by construction, and
invariant under the reparametrisation $T\to f(T)$: carrying $f'(T)$ as a positive symbol, the
derivative of $n$ with respect to it vanishes identically. So the **foliation is physical and the
labelling is gauge**.

**Theorem 2 (the vorticity vanishes identically).** *For any $n$ built from a gradient,
$\partial_{[\mu}n_{\nu]}=A_{[\mu}n_{\nu]}$ with $A=-\partial\ln N$, and the spatial projector
annihilates $n$; hence $\omega_{\mu\nu}=0$ in every metric.*

Verified termwise on a generic $T$ and generic $N$ — $T$'s second derivatives cancel — and the
Christoffels drop out of the antisymmetrisation, so the result is metric-independent. **Consequence:
the realisation is the hypersurface-orthogonal (Hořava) sub-case of Einstein-aether [4,5,6], not the
general aether, and the spin-1 sector is removed entirely.** A prespecified non-gradient decoy field
has nonzero curl, confirming the theorem is about gradients and not about the antisymmetrisation.

**Theorem 3 (the khronon's acceleration is the Newtonian field).**

$$a^{\mu}[n]=\partial^{\mu}\Phi\qquad\text{(linear order, static weak field)}$$

Computed from the Christoffels of an explicit metric, not quoted; it is purely spatial ($a^{t}=0$)
and equals the log-lapse gradient, as the general $K/\omega/a$ decomposition requires. Three
prespecified decoys — $2\partial\Phi$, $-\partial\Phi$, $\partial\Phi/2$ — are all rejected, so this
measures the coefficient *and* the sign.

**This matters more than the repair does.** Before covariantisation, the only acceleration in the
theory was the particle's own $|a|$. MOND is a relation between $g_{\rm obs}$ and $g_{\rm bar}$, and
$g_{\rm bar}$ now exists as a *geometric object*. §6 draws the consequence.

**Nothing is lost.** In the gauge $\sqrt{-(\partial T)^{2}}=1$ with $T=t$, the covariant coupling
$\sqrt{(u\!\cdot\!n)^{2}}$ equals $\gamma$ **exactly** — so the action of [1] is the *unitary gauge*
of the khronon action. The covariantisation is a completion, not a modification. It remains CPT-even
for the same reason Form III of [1] was: $(u\!\cdot\!n)^{2}$ is invariant under $n\to-n$ while
$(u\!\cdot\!n)$ flips.

**The couplings collapse from four to three.** With $\omega=0$ the decomposition
$\nabla_{\mu}n_{\nu}=K_{\mu\nu}-n_{\mu}a_{\nu}$ gives
$(\nabla_{\mu}n_{\nu})(\nabla^{\mu}n^{\nu})=K\!\cdot\!K-a\!\cdot\!a$ and
$(\nabla_{\mu}n_{\nu})(\nabla^{\nu}n^{\mu})=K\!\cdot\!K$, so $c_{1}$ and $c_{3}$ differ only by the
acceleration term, which is degenerate with $c_{4}$:

$$\sum_i c_{i}T_{i}=(c_{1}{+}c_{3})\,K\!\cdot\!K+(c_{4}{-}c_{1})\,a\!\cdot\!a+c_{2}\,(\operatorname{tr}K)^{2}$$

with Jacobian rank 3 — matching the three parameters of the infrared limit of non-projectable
Hořava gravity [4]. Reinstating a vorticity term makes $T_{1}$ and $T_{3}$ independent again with
coefficient $(c_{1}-c_{3})$, confirming the collapse is a consequence of Theorem 2 and not an
algebraic accident. **Propagating content: 2 tensor + 1 scalar, no spin-1.**

**And the Lorentz-violation prediction becomes a real coupling.** $|B|=(1-\mu)/2\approx a_{0}^{2}/8g^{2}$
[1] previously multiplied a stipulated $n$; with $n$ dynamical it is the coefficient of a
matter–khronon coupling of CPT-even $c^{\mu\nu}\sim B\,n^{\mu}n^{\nu}$ type, so the $g^{-2}$ scaling
can no longer be dismissed as an artefact of the choice of frame.

---

## 4. The spin-0 health check

This is the calculation that could have killed §3, so it is done from scratch rather than by quoting
a dispersion relation. Perturbing in the scalar sector, $N=1+\alpha$, $N_{i}=\partial_{i}B$,
$h_{ij}=(1+2\zeta)\delta_{ij}$, and working in Fourier so every integration by parts is algebra:

$$S_{2}=\!\int\!dt\Big[3(1{-}3\lambda)\dot\zeta^{2}+2(1{-}3\lambda)k^{2}\dot\zeta B+(1{-}\lambda)k^{4}B^{2}
+2\xi k^{2}\zeta^{2}+4\xi k^{2}\alpha\zeta+\eta k^{2}\alpha^{2}\Big]$$

with $\alpha$ and $B$ carrying no time derivative — they are constraints.

**The GR check passes first.** The $\alpha$ constraint gives $\alpha=-2\xi\zeta/\eta$, and **at
$\eta=0$ it degenerates to $4\xi k^{2}\zeta=0$, forcing $\zeta=0$: general relativity has no
propagating scalar.** Reproduced, not assumed — so the mode found below is genuinely the
Lorentz-violating one. Eliminating both constraints leaves $A=2(1{-}3\lambda)/(1{-}\lambda)$ and

$$\boxed{\;c_{s}^{2}=\frac{\xi\,(2\xi-\eta)(1-\lambda)}{\eta\,(1-3\lambda)}
\;\;\overset{\xi=1}{=}\;\;\frac{(2-\eta)(\lambda-1)}{\eta\,(3\lambda-1)}\;}$$

The tensor sector independently gives $\tfrac14\dot\gamma^{2}-\tfrac{\xi}{4}k^{2}\gamma^{2}$:
graviton speed$^{2}=\xi$ with a *positive* kinetic term, which is what anchors the overall sign
convention — and means **GW170817 makes $\xi=1$ a measurement to $\sim10^{-15}$, not a choice.**

**The window, and the two diseases are one band:**

- **No ghost** $\iff A>0 \iff \lambda>1$ or $\lambda<1/3$.
- **No gradient instability** $\iff c_{s}^{2}>0 \iff 0<\eta<2$.

Both exclude **exactly** $1/3<\lambda<1$, where the mode is simultaneously a ghost and
gradient-unstable. The healthy region is nonempty and explicit:

| $(\lambda,\eta)$ | $(2,1)$ | $(2,\tfrac12)$ | $(1.0001,10^{-4})$ | $(0.2,1)$ | $(0.2,\tfrac12)$ |
|---|---|---|---|---|---|
| $c_{s}^{2}$ | 0.20 | 0.60 | 0.9998 | 2.0 | 6.0 |

Four prespecified sick decoys are rejected; rescaling $\zeta$ leaves $c_{s}^{2}$ unchanged, so it is
a physical speed; and flipping the action's overall sign makes the *graviton* go bad, confirming the
no-ghost criterion is anchored to the tensor sector.

**And observation points the right way.** Preferred-frame PPN pushes both $(\lambda-1)$ and $\eta$
small, and in that corner

$$c_{s}^{2}\;\longrightarrow\;\frac{\lambda-1}{\eta}\qquad\text{exactly}$$

— **only the ratio survives**, so smallness alone drives $c_{s}$ neither to zero nor to infinity.
The vacuum Cherenkov bound [7] requires the scalar to be at least luminal, since a subluminal mode
would be radiated by ultra-high-energy cosmic rays. So it reduces to a single inequality,

$$\lambda-1\;\ge\;\eta\;>\;0,$$

and superluminal propagation is *safe* here precisely because there is a preferred frame. **PPN and
Cherenkov make independent demands: no conflict.**

**Against interest.** (i) **The health is achieved by choice, not predicted.** §3 bought general
covariance at the price of two new free parameters, and nothing in modified inertia forces either;
"the scalar is healthy" means "a viable region exists", which is much weaker than a prediction. The
theory *gained* parameters. (ii) **The $\eta\to0$ corner that PPN prefers is the known
strong-coupling corner** ($c_{s}^{2}\to\infty$ at fixed $\lambda$): the strong-coupling scale of the
infrared non-projectable theory falls as the Lorentz-violating couplings do [5], so PPN safety
pushes the cutoff *down*. **That scale is not computed here**, and it is the sharpest remaining worry
about the covariantisation. (iii) The $\alpha_{1},\alpha_{2}$ formulas are not derived; only their
qualitative pressure is used, and the $10^{-7}$ figures are standard solar-system orders [8].

---

## 5. Step 3: MOND from the joint field equations

**The metric sector stays Newtonian — and the constraint that made the khronon healthy is what
guarantees it.** Modified inertia *presupposes* an unmodified gravitational field: its entire content
is a modified *response* to a Newtonian $\Phi$. Khronon corrections to $\Phi$ are
$O(\eta,\lambda-1)\lesssim10^{-7}$, while MOND phenomenology needs $\Phi_{\rm bar}$ only to $\sim1\%$.
**Five orders of margin.** So §4's constraint is not a cost — it is a consistency requirement the
framework needed anyway. A decoy $\eta=0.5$ would leave the metric wrong by 50%, so this is a real
comparison.

**The mass question, confronted.** From $E=mc^{2}[1+\mu(\gamma-1)]$ [1]: the rest energy is $mc^{2}$,
independent of $\mu$, while the kinetic term is $m\mu v^{2}/2$. Therefore

$$m_{\rm grav}=m,\qquad m_{\rm inert}=m\mu,\qquad\text{and they differ.}$$

That is not a defect to be explained away — **it is the definitional content of modified inertia.**
And the weak equivalence principle survives: $m\mu a=mg_{\rm bar}$ gives $\mu a=g_{\rm bar}$ with no
reference to mass or composition, so universality of free fall is exact. What is violated is the
*equality* $m_{i}=m_{g}$. A decoy $\mu$ depending on the mass leaves $m$ in the answer, so the
cancellation is a real property of $\mu(\Theta)$. The consequence runs in the framework's favour: a
galaxy's **gravitating** mass is its **baryonic** mass. Energy-momentum conservation for a
time-nonlocal modified-inertia theory is cited [9], not proved here.

**The chain closes.** With the Newtonian metric established independently, the worldline equation
$d(m\mu v)/dt=-m\nabla\Phi$ gives

$$\mu(g_{\rm obs}/a_{0})\,g_{\rm obs}=g_{\rm bar}
\;\;\Longrightarrow\;\;
g_{\rm obs}=\sqrt{a_{0}g_{\rm bar}}
\;\;\Longrightarrow\;\;
v^{4}=GMa_{0}$$

exactly — flat rotation curves and the baryonic Tully–Fisher relation — with **no new parameter**,
since $a_{0}=\tfrac23 c\,m^{2}/g$ is inherited from §2. A decoy deep limit $\mu\sim Y^{2}$ fails to
reproduce $v^{4}=GMa_{0}$, so this tests the interpolation's deep power and not the algebra of
substitution. The closure is not circular: the Newtonian metric came from §5's first paragraph, not
from the MOND relation.

**The BTFR normalisation, both ways.** The framework predicts $A_{\rm fw}=1/(Ga_{0})=80.5\,M_{\odot}({\rm km/s})^{-4}$
against McGaugh's fitted $A=47$ [10] — a ratio of 1.712, i.e. **0.234 dex in mass**, or
$v_{c}=105.6$ km/s at $10^{10}M_{\odot}$ versus 120.8. Three things must be said together:

- **Against interest: the ALT footing fits better** (ratio 1.421 vs 1.712).
- **But it is not a test of $a_{0}$.** $M_{\rm bar}$ scales with the stellar mass-to-light ratio, and
  $A=47$ was obtained at $\Upsilon_{3.6}=0.5$; the framework needs $\Upsilon_{3.6}=0.856$ — high, yet
  inside the literature spread and close to the 0.70 that an independent RAR fit of this corpus
  prefers. The intercept is $\Upsilon$-degenerate.
- **And the $\Upsilon$-free estimator accepts the canonical value.** The gas-dominated $a_{0}$-line
  box $[0.84,1.36]\times10^{-10}$ contains $9.3619\times10^{-11}$.

So the offset is a mass-to-light question, not an $a_{0}$ question: **neither a win nor a deficit.**

---

## 6. A fork the covariantisation exposes

This is the genuinely new physical content, and it is a consequence of Theorem 3. The covariant
theory possesses **two** acceleration scalars: the particle's own $|a|$, and the khronon's
$|a[n]|=g_{\rm bar}$. So $\Theta$ may be sourced by either:

| source of $\Theta$ | theory |
|---|---|
| $\Theta[\,|a|\,]$ | **pure modified inertia** — the construction of [1] |
| $\Theta[\,|a[n]|\,]$ | **a third theory** — external-field-driven; neither pure MI nor AQUAL |

The second branch shares the same interpolation function and the same $a_{0}$, and is a genuinely
different theory. **The worldline formulation could not even express this fork**, because it had no
covariant object equal to $g_{\rm bar}$.

They are observationally distinguishable. In a directional external-field test — the aligned versus
anti-aligned asymmetry of rotation curves relative to the external field direction — **pure modified
inertia predicts exactly zero**, while an external-field-driven $\Theta$ does not. The fork is
exposed here and **not resolved here**.

---

## 7. Limitations

- **Single-stream: a formulation preference, not a restriction on the physics.** A first draft of
  this paper called this the sharpest gap. That was wrong, and the correction is recorded rather than
  absorbed. $\Theta(\tau)$ is an integral over *the particle's own past*, so
  $\ddot\chi+2m\dot\chi+m^{2}\chi=g|a|/c$ is an ODE in the particle's own proper time: $\chi$ is a
  **per-worldline internal variable**, like a spin or an internal clock, and two stars crossing at a
  point simply carry different $\chi$. Multi-stream is then a non-issue. And the metric sector never
  sees $\chi$ at all, because $m_{\rm grav}=m$ is $\mu$-independent (§5) — the first $\chi$-dependent
  source term is the kinetic $m\mu v^{2}/2$, suppressed by $(v/c)^{2}=5.4\times10^{-7}$ at galactic
  speeds. So the single-stream restriction binds only a *continuum rewriting of $\chi$ undertaken for
  its own sake*: it does not restrict test-particle dynamics, which is what rotation curves are, and
  it does not touch the field equations.
- **The strong-coupling scale** in the small-$(\lambda-1,\eta)$ corner is not computed. With the
  single-stream worry withdrawn above, **this is now the sharpest gap in the construction** (§4).
- **Nothing new is derived.** $a_{0}$ is the coupling ratio of §2 and $\mu$'s shape is the $\alpha=2$
  interpolation that solar-system ephemerides force [1]. Steps 1–3 establish *consistency and
  locality*, not predictive content.
- **The full bilocal cannot be localised** by the auxiliary-field route (§2).
- Strong fields, black-hole universal horizons, and nonlinear stability: not addressed. The analysis
  of §4 is flat-space, quadratic order, scalar sector.
- **Ostrogradsky is not evaded in the localised writing** (§2), only in the exact one.

### What a referee should attack first

1. **Whether $\Theta$ should be sourced by $|a|$ at all** — §6's fork is a genuine ambiguity of the
   covariant theory, not a detail.
2. **The strong-coupling scale**, since the PPN-safe corner is the dangerous one.
3. **The two new parameters** $\lambda,\eta$ — whether a theory that gained parameters to become
   covariant has really gained ground.

---

## 8. What is not claimed

- **$a_{0}$'s value is not derived**, and $\kappa=\tfrac12$ in $a_{0}=\kappa c\sqrt{G\rho_{\Lambda}}$
  remains **fitted**. The companion no-go [2] shows *why* a free-field correlator cannot supply it.
- **The theory acquired two parameters, not fewer.** General covariance and ghost-freedom were bought
  with $\lambda$ and $\eta$, whose only constraints are the health window and PPN.
- **No claim is made regarding particle physics, the Standard Model, or unification.** The author
  publicly withdrew earlier statements of that kind and does not restate them. A complete field
  theory of modified inertia is not a theory of everything, and nothing here is evidence for one.
- **The interpolating function is not new.** $\nu=\sqrt{1+1/y}$ is Eq. (9) of Milgrom (1999).
- The khronon sector is standard technology [4,5,6]; what is new here is its use to complete *this*
  construction, Theorem 3, and the fork of §6.

---

## 9. Reproducibility

Every quantitative claim above is produced by a committed script that exits non-zero if any internal
consistency check fails, and each carries negative controls that must trip. All four are included:

- `mi_kernel_localisation_2026.py` — §2, 27/27 checks.
- `mi_khronon_covariantisation_2026.py` — §3, 26/26 checks.
- `mi_khronon_spin0_health_2026.py` — §4, 30/30 checks.
- `mi_step3_joint_field_equations_2026.py` — §§5–7, 32/32 checks.

Both $a_{0}$ footings (canonical $\rho_{\rm DE}$ with $cH_{\Lambda}$; ALT $\times1.2048$) are carried
on every dimensionful number.

**AI-assistance disclosure.** Portions of the analysis, numerical verification and drafting were
carried out with the assistance of a large language model (Anthropic Claude). The author directed the
work, specified and reviewed every load-bearing calculation, and takes full responsibility including
for any errors. No AI system satisfies the criteria for authorship and none is listed as an author.
Several intermediate claims produced during the work were found to be incorrect and were withdrawn
before this deposit — among them a past-directed sign for $n_{\mu}$, an assumed rather than derived
reparametrisation invariance, an asserted BTFR band that was replaced by the computed value, and the
overstated single-stream limitation withdrawn in §7.

---

## References

[1] C. P. Zimmerman, *A causal variational worldline action for modified inertia: the rapidity gap*,
Zenodo, concept DOI 10.5281/zenodo.21845411.

[2] C. P. Zimmerman, *Why the de Sitter vacuum cannot fix the MOND acceleration scale: the required
moment is the pole of the Riemann zeta function*, Zenodo, concept DOI 10.5281/zenodo.21854464.

[3] W. Israel and J. M. Stewart, Ann. Phys. **118**, 341 (1979).

[4] T. Jacobson, *Extended Hořava gravity and Einstein-aether theory*, Phys. Rev. D **81**, 101502
(2010).

[5] D. Blas, O. Pujolàs and S. Sibiryakov, Phys. Rev. Lett. **104**, 181302 (2010); JHEP **1104**,
018 (2011).

[6] T. Jacobson and D. Mattingly, Phys. Rev. D **64**, 024028 (2001); P. Hořava, Phys. Rev. D **79**,
084008 (2009).

[7] J. W. Elliott, G. D. Moore and H. Stoica, JHEP **0508**, 066 (2005).

[8] C. M. Will, *Theory and Experiment in Gravitational Physics*.

[9] M. Milgrom, *Dynamics with a non-standard inertia-acceleration relation*, Ann. Phys. **229**, 384
(1994).

[10] S. S. McGaugh, Astron. J. **143**, 40 (2012).

[11] M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A **253**, 273 (1999).
