# A local, generally covariant field theory of modified inertia

**Carl P. Zimmerman**
Briar Creek Tech

*Version 5 (2026-08-08). Changes from earlier versions are listed in §11.*

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
   nonempty window (§4), **with a strong-coupling scale that clears every scale the theory is
   applied at by dozens of orders, and no Vainshtein-type screening anywhere** (§5).

And the acceleration scale is no longer the first moment of a postulated kernel:

$$\boxed{\;a_{0}=\tfrac{2}{3}\,c\,\frac{m^{2}}{g}\;}$$

**the ratio of the auxiliary field's mass squared to its coupling.** Together with the companion
no-go result [2] — that this moment is logarithmically divergent, so it cannot be computed from a
free-field correlator — this means $g/m^{2}$ is a *renormalised coupling*. Which is what every
coupling in every local field theory is.

**The honest caption, which must travel with the box.** $a_{0}$'s *value* is still not derived, and
the covariantisation *added* two free parameters ($\lambda,\eta$) rather than removing any. The
theory is complete in the sense that a local, covariant, ghost-free action exists, has a
strong-coupling scale far above every regime it is applied in, and yields MOND; it is not complete in
the sense of predicting its own constants. And it says nothing whatever about
particle physics — see §10.

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
exits non-zero on any internal failure and carries negative controls that must trip (§11).

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

## 5. Strong coupling and the static nonlinearity

### 5.1 The strong-coupling scale

Section 4 leaves one danger: preferred-frame PPN pushes $(\lambda-1)$ and $\eta$ small, and a
kinetic term proportional to a small number is exactly when self-interactions turn on early. That
was the sharpest open risk in v1 of this paper, and it is now computed.

**Why the danger is real, stated precisely.** Restore the khronon fluctuation, $T=t+\pi$. Then

$$\ln N=-\dot\pi+\tfrac12\dot\pi^{2}+\tfrac12(\partial\pi)^{2}+O(\pi^{3}),
\qquad a_{i}=-\partial_{i}\dot\pi+O(\pi^{2}),
\qquad K_{ij}=-\partial_{i}\partial_{j}\pi+O(\pi^{2}),$$

and **at $\lambda=\xi=1$, $\eta=0$ the khronon action vanishes identically** — the $K$ sector gives
$K\!\cdot\!K-K^{2}=k^{4}\pi^{2}-k^{4}\pi^{2}=0$, so $\pi$ is pure gauge in general relativity, as it
must be. A prespecified $\lambda=3/2$ decoy does *not* cancel, so this detects the GR limit rather
than an artefact of the substitution. Everything that survives is therefore proportional to the
small parameters:

$$S_{2}\sim M_{\rm Pl}^{2}\Big[-\delta\,(\partial^{2}\pi)^{2}+\eta\,(\partial_{i}\dot\pi)^{2}\Big],
\qquad \delta=\lambda-1 .$$

**And an independent cross-check falls out.** That action's dispersion is
$\eta\,\omega^{2}k^{2}=\delta\,k^{4}$, i.e.

$$c_{s}^{2}=\frac{\delta}{\eta}=\frac{\lambda-1}{\eta}$$

which is **exactly** the PPN-corner limit of §4 — obtained there from the unitary-gauge $\zeta$ with
the ADM constraints eliminated, and here from the Stückelberg $\pi$ in flat space. Two independent
gauges and variables, one answer; a prespecified decoy $\delta/(2\eta)$ is rejected.

**The static nonlinearity of the $\eta$ sector vanishes.** Canonical normalisation from the $\eta$
term is $\pi_{c}=\sqrt{\eta}\,M_{\rm Pl}k\,\pi$, and the leading self-interaction is

$$-2\dot\pi(\partial_{i}\dot\pi)^{2}-2\,\partial_{i}\dot\pi\,\partial_{j}\pi\,\partial_{i}\partial_{j}\pi$$

— **every term carries a time derivative, so the whole cubic part vanishes for static
configurations.** There is no static Vainshtein-type screening radius from this sector; the
nonlinearity needs time dependence to switch on. A decoy cubic $(\partial_{x}\pi)^{3}$ does not
vanish statically, so this is a property of the actual terms. Derivative counting on the same terms
gives cubic/quadratic $=c_{s}E/(\sqrt{\eta}M_{\rm Pl})$, hence

$$\boxed{\;\Lambda_{\rm sc}\sim\frac{\sqrt{\eta}\;M_{\rm Pl}}{c_{s}}\;\approx\;7.7\times10^{14}\ {\rm GeV}\quad(\eta=10^{-7})\;}$$

So the PPN-preferred corner does lower the cutoff, but only as $\eta^{1/2}$, and from the Planck
mass.

**The comparison that settles it, built to be robust to the power.** The theory is applied at
absurdly low energies. Scanning $\Lambda_{\rm sc}=\eta^{p}M_{\rm Pl}$ over $p=\tfrac12,1,2,3,4$ —
deliberately allowing powers far worse than the one derived:

| scale where the theory is applied | energy | $\Lambda_{\rm sc}/E$ at $p=\tfrac12$ | at $p=4$ |
|---|---|---|---|
| Milky Way orbital frequency | $5.7\times10^{-31}$ eV | $1.4\times10^{54}$ | $4.3\times10^{29}$ |
| Milky Way inverse size (8.2 kpc) | $7.8\times10^{-28}$ eV | $9.9\times10^{50}$ | $3.1\times10^{26}$ |
| solar system, $1/{\rm AU}$ | $1.3\times10^{-18}$ eV | $5.8\times10^{41}$ | $1.9\times10^{17}$ |
| laboratory, $1/{\rm m}$ | $2.0\times10^{-7}$ eV | $3.9\times10^{30}$ | $1.2\times10^{6}$ |

**$\Lambda_{\rm sc}$ exceeds every scale at which the theory is applied, for every power tested** —
26 orders of galactic margin even at the pessimistic $p=4$, and 50 at the derived $p=\tfrac12$. So
the strong-coupling scale bears on whether this is a UV-complete *quantum* theory, which it never
claimed to be, and **not** on the phenomenology.

**Against interest, and this corrects a claim of my own.** A first draft of the accompanying script
asserted that the cutoff clears every scale *including* the LHC ($1.4\times10^{13}$ eV). **That is
false: at $p\ge3$ the cutoff falls below collider energies**, so the khronon effective theory would
not cover the LHC at those powers. It is harmless only because the matter–khronon coupling there is
$|B|\sim a_{0}^{2}/8g^{2}=1.1\times10^{-23}$, and the *derived* power $p=\tfrac12$ clears the LHC by
10 orders — but the claim needed correcting rather than softening. Two further caveats: **only the
scaling is computed, not the coefficient** (§5's table is built to be insensitive to it, but a
factor of 100 in the prefactor is excluded by nothing here); and **the $\delta$-sector's static
nonlinearity is not analysed** — the $\eta$ sector's static cubic dies, but the
$(\partial^{2}\pi)^{2}$ sector's cubics need not, and a Vainshtein radius from *that* sector is
uncomputed. That is now the honest residual. The analysis is flat-space throughout.

**A note on which theory this is.** The notorious $\lambda\to1$ strong coupling belongs to
*projectable* Hořava gravity. The non-projectable "healthy extension" carrying the $a_{i}a^{i}$ term
is the known repair [5] — and §3 landed on it **by theorem** rather than by choice, since the
vorticity of a gradient-built $n$ vanishes identically.

---

### 5.2 The static nonlinearity of both sectors

§5.1 established that the $\eta$ sector's cubic self-interaction vanishes for static
configurations, and flagged the $\delta$ sector — the $-\delta K^{2}$ term — as unanalysed. That was
v2's sharpest remaining gap. It closes by a parity theorem.

**Theorem 4 ($K$ is odd in $\pi$, to all orders).** *For a static khronon $T=t+\pi(\mathbf{x})$, the
unit normal is $n^{\mu}=(1/w,\,-\partial_{i}\pi/w)$ with $w=\sqrt{1-(\partial\pi)^{2}}$. Under
$\pi\to-\pi$ the normalisation $w$ is invariant — it depends on $(\partial\pi)^{2}$ — while
$\partial_{i}\pi$ flips. Hence $K[-\pi]=-K[\pi]$ exactly.*

Verified on the full three-dimensional closed form with **no series truncation**. In one dimension
the divergence has an exact closed form that makes the parity manifest:

$$K=-\frac{\pi''}{\left(1-\pi'^{2}\right)^{3/2}}$$

— odd numerator, even bracket. Its expansion has **zero even orders** (checked through fifth):
$-\pi''$, then $-\tfrac32\pi''\pi'^{2}$, then quintic. And the general three-dimensional cubic
$-\tfrac12\partial^{2}\pi(\partial\pi)^{2}-\partial_{i}\pi\,\partial_{j}\pi\,\partial_{i}\partial_{j}\pi$
reduces in one dimension to exactly $-\tfrac32\pi''\pi'^{2}$, so the 3-D formula is *validated
against* the exact 1-D result rather than asserted. Inserting a genuine even piece into $n^{i}$ by
hand gives $K$ a nonzero quadratic term, so the theorem is a measurement and not an algebraic
accident.

**Corollary. $K^{2}$ is even, so the $\delta$ sector has no static cubic; its leading static
self-interaction is quartic**, with

$$\frac{\text{quartic}}{\text{quadratic}}=3\pi'^{2}\qquad\text{(one dimension)}$$

i.e. of *order* $(\partial\pi)^{2}$ with an $O(1)$ coefficient. (A first draft of the accompanying
script wrote "exactly $(\partial\pi)^{2}$"; the coefficient is 3, and the script records the
correction.)

**And on the aligned static foliation it vanishes outright.** For a static, shift-free metric the
constant-$t$ surfaces have $K_{ij}=\tfrac{1}{2N}(\dot h_{ij}-D_{i}N_{j}-D_{j}N_{i})=0$ identically,
so both $K\!\cdot\!K$ and $K^{2}$ vanish at *every* order — only $\eta\,a_{i}a^{i}$ survives. And
$\delta(K^{2})/\delta T=2K\,\delta K$ vanishes with $K$, which makes that foliation a **solution** of
the $K$ sector rather than an imposed ansatz. A time-dependent metric gives $K_{ij}\neq0$, so this is
a property of staticity and not of the formula.

**The nonlinearity, priced.** $|\partial\pi|$ is the tilt of the khronon foliation relative to the
local frame, i.e. $\sim v/c$:

| setting | $v$ | $(\partial\pi)^{2}$ |
|---|---|---|
| solar system vs the CMB frame | 369.8 km/s | $1.5\times10^{-6}$ |
| galactic rotation | 220 km/s | $5.4\times10^{-7}$ |
| cluster velocities | 1000 km/s | $1.1\times10^{-5}$ |
| a relativistic probe | $0.1c$ | $1.0\times10^{-2}$ |

**So there is no Vainshtein-type screening radius: the nonlinearity never reaches $O(1)$.** It would
require $|\partial\pi|\to1$ — a foliation boosted at near-light speed relative to the local frame —
which happens near a black-hole horizon and nowhere else.

**Combining the two sectors.** The $\eta$ cubic dies by carrying a time derivative; the $\delta$ cubic
dies by parity in $\pi$. Two different mechanisms, so **the leading static self-interaction of the
whole khronon sector is quartic** — worth a factor of 811 over a surviving cubic
($1.5\times10^{-6}$ instead of $1.2\times10^{-3}$). The result is not cosmetic.

**What remains, and it is narrower than what it replaces.** (i) **The full $T$ field equation around
a real source is not solved.** The aligned foliation is shown consistent with the $K$ sector and the
nonlinearity is priced *given* $|\partial\pi|\sim v/c$, but $\pi(r)$ is not obtained, so a larger
$|\partial\pi|$ than the kinematic estimate is not excluded. (ii) **$|\partial\pi|\to1$ near a
black-hole horizon is exactly where this analysis fails**; universal horizons in Lorentz-violating
gravity [12] are a real known issue and are not addressed. (iii) The $\eta$ sector's quartic is not
computed either — only that its cubic vanishes.

---

## 6. Step 3: MOND from the joint field equations

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
$d(m\mu v)/dt=-m\nabla\Phi$ gives (the accompanying script demonstrates the limits on the $\alpha=2$
form for definiteness; the in-force exponential kernel of §10 has the same two limits, so the
conclusion is unchanged — see [13])

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

## 7. A fork the covariantisation exposes

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

## 8. Confrontation: the pre-registered wide-binary test

A field theory that cannot be killed is not worth much. This section states the live observational
test, its registered numbers and — the part usually omitted — **its power**, computed before the
data.

**What this construction does and does not supply.** It must be said plainly first: **the
wide-binary prediction is not derived from steps 1–3.** It follows from the external-field effect
applied to the framework's interpolation kernel, both of which predate this paper. What §§2–6 supply
is the *theory behind* the number — a local, covariant, ghost-free action in which that number is
the prediction of something rather than of a rule. The number itself does not move.

**The registered prediction.** The observable is $\gamma_{v}$, the ratio of the measured
velocity-scale to the Newtonian one for wide binaries in the 2–30 kAU window:

$$\gamma_{v}=1.1582,\qquad
\text{range }1.1311\text{–}1.1964\ (\text{radial}),\quad 1.1339\text{–}1.2007\ (\text{magnitude})$$

on the exponential kernel of §10, over both $a_{0}$ footings and both external-field conventions. This
is the author's frozen, hash-stamped pre-registration as amended [13]; nothing in this paper alters
it.

**The one decisive statement, at the registered sample size $N=30{,}000$.** A **Newtonian** result
across 2–30 kAU is evidence against the framework at **4.74–7.10 $\sigma_{\rm tot}$**. That figure is
clean for a specific reason: under a Newtonian truth the estimator's shape bias is identically zero,
so it survives every systematic the registration declares. **It is the number the theory should be
judged on, and no re-hedging is permitted after the fact.**

**Three things that limit the test, all registered in advance.**

1. **The scoring bins collide with the prediction.** $1.1582$ falls in the interval the frozen
   decision table pre-declared "MG-side; MI disfavored", and the frozen modified-gravity target
   $1.137$ lies *inside* the MI range, $0.77\,\sigma_{\rm tot}$ from the point value. A scorer
   executing the table on a measurement **at the framework's own prediction** would record the
   framework as disfavored. The registration's remedy is binding and is implemented: report the raw
   $\hat\gamma$ with $\sigma_{\rm fit}$ and **both** distances — to $1.000$ and to $1.1582$ — and
   never a single verdict word.
2. **A nuisance parameter sits outside its frozen window.** The estimator's calibration nuisance
   lands at $1.0575$–$1.0959$ against a registered window of $[0.95,1.05]$, whose pre-declared
   consequence is *"systematic-limited, no verdict — reported, not repaired."* The exponential kernel
   fails this on both variance treatments where the retired $\alpha=2$ kernel passed both. This is a
   cost of the kernel change, and it is not repaired here.
3. **One corner is pre-declared unscoreable.** On the magnitude convention the alternative-footing
   corner is $1.20069$, which is $0.00069$ **above** the $>1.20$ no-verdict edge. A genuine detection
   there cannot be scored. Quoting only the radial convention would hide this at its convenient end.

**Two further checks, both underpowered, and that is stated rather than discovered afterwards.**

- **The anisotropy falsifier**, whose sign was pre-declared: perpendicular pairs must show the larger
  boost, and the opposite sense at $\ge3\sigma$ falsifies the derived external-field effect
  *independently* of the aggregate. The 3-D eigenvalue spread is $0.176$–$0.199$ — strengthened by the
  kernel change. **But only the sky-projected angle is observable.** Averaging
  $\gamma(\psi)=\gamma_{\perp}+(\gamma_{\parallel}-\gamma_{\perp})\cos^{2}\psi$ over isotropic 3-D
  orientations gives a projection dilution of $D=0.2367$ by Monte Carlo over the registered
  $|b|>15^{\circ}$ sky, against the in-plane closed form $4/(3\pi)=0.4244$. So the **observable** split
  is $0.042$–$0.047$, reaching only $1.00$–$1.13\,\sigma$ at $N=30{,}000$ and requiring
  $N\sim2.1$–$2.7\times10^{5}$ for $3\sigma$ — **seven to nine times the registered sample.**
- **The gated branch**, which must be scored alongside the ungated one. In the aggregate it is
  $0.03$–$0.06\,\sigma$ from Newton and would need $N\sim8.6\times10^{7}$ to separate: **an
  aggregate-only scorer would report "Newtonian" for a universe in which the gated branch is true.**
  Its only handle is an internal rise across the window, $0.001\,\sigma$ at 2 kAU to $1.56\,\sigma$ at
  30 kAU — falsifiable in *shape*, but $1.56$ is not $3$. A watch item. What the two *branches*
  separate by is large: the ungated signal is $135\times$ the gated amplitude.

**And the fork of §7 has its own test.** The choice of what sources $\Theta$ — the particle's $|a|$
(pure modified inertia) or the khronon's $|a[n]|=g_{\rm bar}$ — is decided by a *directional*
external-field measurement, in which **pure modified inertia predicts exactly zero** aligned
asymmetry while an external-field-driven $\Theta$ does not. That is a separate front from the
aggregate $\gamma_{v}$ and it is not settled here.

**Summary of the confrontation.** One number with teeth (4.74–7.10 $\sigma$ against a Newtonian
result), three with context, one unscoreable corner, and one nuisance outside its window. That is a
weaker test than the registration originally expected — §1.5 of it anticipated a decidable outcome —
and the honest position is that DR4 can *disfavor* this framework decisively and can *support* it only
weakly.

---

## 9. Limitations

- **Single-stream: a formulation preference, not a restriction on the physics.** A first draft of
  this paper called this the sharpest gap. That was wrong, and the correction is recorded rather than
  absorbed. $\Theta(\tau)$ is an integral over *the particle's own past*, so
  $\ddot\chi+2m\dot\chi+m^{2}\chi=g|a|/c$ is an ODE in the particle's own proper time: $\chi$ is a
  **per-worldline internal variable**, like a spin or an internal clock, and two stars crossing at a
  point simply carry different $\chi$. Multi-stream is then a non-issue. And the metric sector never
  sees $\chi$ at all, because $m_{\rm grav}=m$ is $\mu$-independent (§6) — the first $\chi$-dependent
  source term is the kinetic $m\mu v^{2}/2$, suppressed by $(v/c)^{2}=5.4\times10^{-7}$ at galactic
  speeds. So the single-stream restriction binds only a *continuum rewriting of $\chi$ undertaken for
  its own sake*: it does not restrict test-particle dynamics, which is what rotation curves are, and
  it does not touch the field equations.
- **Strong coupling and the static nonlinearity are now both computed** (§5) and neither threatens
  the phenomenology. Three narrower residuals remain in their place: only the *scaling* of
  $\Lambda_{\rm sc}$ is derived and not its coefficient; **the full $T$ field equation around a real
  source is not solved**, so a larger $|\partial\pi|$ than the kinematic $v/c$ estimate is not
  excluded; and the $\eta$ sector's quartic is uncomputed.
- **Strong field and near-horizon behaviour is the one regime where the analysis genuinely fails.**
  $|\partial\pi|\to1$ invalidates §5.2's expansion, and **universal horizons** in Lorentz-violating
  gravity [12] are not addressed. This is now the sharpest structural gap.
- **Nothing new is derived.** $a_{0}$ is the coupling ratio of §2, and $\mu$'s shape is an *input*:
  the framework's in-force kernel is the exponential one, $\nu=1/(1-e^{-\sqrt{y}})$, adopted because
  **both** power-law kernels fail solar-system ephemerides — $\alpha=1$ by $1279\times$ the
  Earth/Mars bound and $\alpha=2$ by $8.5$–$12.4\times$ the Mars ranging budget, the latter because
  its $1/g$ tail binds at the *Sun* via the Jupiter reflex rather than at a planet [13]. **Steps 1–3
  are insensitive to that choice**: the localisation concerns the *memory* kernel $K(s)$ and not
  $\mu(Y)$, so $a_{0}=\tfrac23 c\,m^{2}/g$ carries no reference to $\mu$'s shape; and §6 used only
  the two limits $\nu\to1/\sqrt{y}$ (deep) and $\nu\to1$ (Newtonian), which the exponential kernel
  satisfies. Steps 1–3 establish *consistency and locality*, not predictive content.
- **The full bilocal cannot be localised** by the auxiliary-field route (§2).
- Strong fields, black-hole universal horizons, and nonlinear stability: not addressed. The analysis
  of §4 is flat-space, quadratic order, scalar sector.
- **Ostrogradsky is not evaded in the localised writing** (§2), only in the exact one.

### What a referee should attack first

1. **Whether $\Theta$ should be sourced by $|a|$ at all** — §6's fork is a genuine ambiguity of the
   covariant theory, not a detail.
2. **The near-horizon regime** — $|\partial\pi|\to1$ breaks §5.2, and universal horizons are
   unaddressed.
3. **The two new parameters** $\lambda,\eta$ — whether a theory that gained parameters to become
   covariant has really gained ground.

---

## 10. What is not claimed

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

## 11. Reproducibility, and version history

Every quantitative claim above is produced by a committed script that exits non-zero if any internal
consistency check fails, and each carries negative controls that must trip. All four are included:

- `mi_kernel_localisation_2026.py` — §2, 27/27 checks.
- `mi_khronon_covariantisation_2026.py` — §3, 26/26 checks.
- `mi_khronon_spin0_health_2026.py` — §4, 30/30 checks.
- `mi_khronon_strong_coupling_scale_2026.py` — §5.1, 24/24 checks. **New in v2.**
- `mi_khronon_delta_sector_static_2026.py` — §5.2, 22/22 checks. **New in v3.**
- `mi_step3_joint_field_equations_2026.py` — §§6–9, 32/32 checks.
- `mi_dr4_readiness_audit_2026.py` — §8, 31/31 checks. **New in v5.**
- `mi_dr4_anisotropy_and_gated_2026.py` — §8, 20/20 checks. **New in v5.**

### Changes in v5

1. **New §8: the confrontation.** The paper now states the live pre-registered wide-binary test, its
   registered numbers, and — the part usually omitted — **its power, computed before the data**.
2. **Said first and plainly: the wide-binary prediction is NOT derived from steps 1–3.** It follows
   from the external-field effect applied to the framework's kernel, both of which predate this
   paper. §§2–6 supply the theory *behind* the number; the number does not move.
3. **The honest headline is that the test is asymmetric:** one decisive number (a Newtonian result is
   evidence against at 4.74–7.10 $\sigma_{\rm tot}$), against a scoring-bin collision, a nuisance
   parameter outside its frozen window, an unscoreable corner, and two further checks that are
   underpowered at the registered $N$ (anisotropy 1.00–1.13 $\sigma$ needing 7–9× the sample; the
   gated branch 0.03–0.06 $\sigma$ in the aggregate). **DR4 can disfavor this framework decisively
   and can support it only weakly**, and §8 says so.
4. Two verification scripts added (31/31, 20/20). Sections 8–10 renumbered to 9–11.
5. Nothing else changes. $a_{0}$'s value is still not derived and no claim is made about particle
   physics.

### Changes in v4

1. **A factual correction, found by auditing this paper against the author's own frozen
   pre-registration and made rather than left standing.** v1–v3 stated that $\mu$'s shape is "the
   $\alpha=2$ interpolation that solar-system ephemerides force." **That is false**: $\alpha=2$
   misses the Mars ranging budget by $8.5$–$12.4\times$, because its $1/g$ tail binds at the Sun via
   the Jupiter reflex rather than at a planet, and the framework's in-force kernel is the
   exponential $\nu=1/(1-e^{-\sqrt{y}})$ [13]. §9 now says so.
2. **Nothing structural moves.** The localisation concerns the *memory* kernel $K(s)$, not $\mu(Y)$,
   so $a_{0}=\tfrac23c\,m^{2}/g$ is untouched; and §6 used only the deep and Newtonian limits, which
   the exponential kernel satisfies. §6 now names the kernel used in the demonstration and records
   that the substitution is harmless.
3. No other change. $a_{0}$'s value is still not derived and no claim is made about particle physics.

### Changes in v3

1. **New §5.2: the static nonlinearity of both sectors**, which was v2's sharpest named gap. It
   closes by a **parity theorem** — $K$ is odd in $\pi$ to all orders, so $K^{2}$ is even and the
   $\delta$ sector has **no static cubic**. Its leading static self-interaction is quartic.
2. On the aligned static foliation the $K$ sector vanishes at every order, and it is a *solution*
   rather than an ansatz, since $\delta(K^{2})/\delta T\propto K$.
3. The nonlinearity is priced at $(\partial\pi)^{2}\sim(v/c)^{2}\le1.1\times10^{-5}$ everywhere the
   theory is applied: **no Vainshtein-type screening radius exists.**
4. Combining with §5.1, **the leading static self-interaction of the whole khronon sector is
   quartic** — the two cubics vanish for two different reasons.
5. **A claim of the author's own is corrected:** a draft wrote the quartic/quadratic ratio as
   "exactly $(\partial\pi)^{2}$"; the coefficient is 3.
6. The limitations list is updated again: the $\delta$-sector item is discharged, and the **near-horizon
   regime with universal horizons** becomes the sharpest structural gap.
7. Nothing else changes. $a_{0}$'s value is still not derived and no claim is made about particle
   physics.

### Changes in v2

1. **New §5: the strong-coupling scale**, which was v1's sharpest named risk. It is computed and
   **does not threaten the phenomenology**: $\Lambda_{\rm sc}\sim\sqrt{\eta}M_{\rm Pl}/c_{s}$, and
   the conclusion survives a scan over powers $\eta^{p}$, $p=\tfrac12\ldots4$.
2. **A cross-check gained, not assumed:** the Stückelberg $\pi$ formulation reproduces
   $c_{s}^{2}=(\lambda-1)/\eta$, which §4 obtained from unitary-gauge $\zeta$ — two gauges, one
   answer.
3. **The $\eta$-sector static nonlinearity is shown to vanish**, so there is no static
   Vainshtein-type screening from it.
4. **A claim of the author's own is corrected rather than softened:** a first draft asserted the
   cutoff clears *every* scale including the LHC. It does not — at $p\ge3$ it falls below collider
   energies. Stated in §5.
5. The limitations list is updated: the strong-coupling item is discharged and replaced by the
   narrower and now-sharpest gap, **the $\delta$-sector's static nonlinearity**.
6. Nothing else changes. Every equation, result and caveat of v1 stands, including that $a_{0}$'s
   value is not derived and that no claim is made about particle physics.

Both $a_{0}$ footings (canonical $\rho_{\rm DE}$ with $cH_{\Lambda}$; ALT $\times1.2048$) are carried
on every dimensionful number.

**AI-assistance disclosure.** Portions of the analysis, numerical verification and drafting were
carried out with the assistance of a large language model (Anthropic Claude). The author directed the
work, specified and reviewed every load-bearing calculation, and takes full responsibility including
for any errors. No AI system satisfies the criteria for authorship and none is listed as an author.
Several intermediate claims produced during the work were found to be incorrect and were withdrawn
before this deposit — among them a past-directed sign for $n_{\mu}$, an assumed rather than derived
reparametrisation invariance, an asserted BTFR band that was replaced by the computed value, the
overstated single-stream limitation withdrawn in §8, an assertion that the strong-coupling scale
clears collider energies at every power (corrected in §5.1), a cubic-order counter that returned zero
terms and thereby made a check pass vacuously (found and replaced), and a quartic/quadratic ratio
written as exact when its coefficient is 3 (corrected in §5.2).

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

[12] D. Blas and S. Sibiryakov, *Horava gravity versus thermodynamics: the black hole case*, Phys.
Rev. D **84**, 124043 (2011).

[13] Amendment 8 to the author's frozen Gaia DR4 pre-registration (2026-08-03), which retires both
power-law kernels on solar-system grounds and adopts $\nu=1/(1-e^{-\sqrt{y}})$; see also the
companion Bekenstein–Milgrom field theory for that kernel, whose ellipticity, convexity,
ghost-freedom and subluminality are proved for the same interpolation.
