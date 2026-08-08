# Inertia from the de Sitter vacuum: a guide for cosmologists and astrophysicists

**Carl P. Zimmerman**
Briar Creek Tech

*Version 1 (2026-08-08). An expository guide. It assumes general relativity, ΛCDM and
observational cosmology; it assumes nothing about the framework it describes.*

---

## 0. What this document is, and what it is not

This is a guide to a specific proposal: that the MOND acceleration scale $a_{0}$ is not an
independent constant of nature but a **property of the de Sitter vacuum**, and that the
phenomenology follows from a **modification of inertia** rather than of gravity. As of 2026 there is
a local, generally covariant, ghost-free field theory realising it, and a frozen pre-registered test
that can disfavour it.

It is written for someone who knows ΛCDM well and MOND slightly, who is professionally sceptical,
and who wants to know in an hour whether this is worth an afternoon.

**Three things it is not.**

- **It is not a claim that dark matter is dead.** §4.4 gives the strongest reason to think this
  framework is wrong, and it is not a small one.
- **It is not a theory of everything.** Nothing here touches the Standard Model. The author publicly
  withdrew earlier statements of that kind in June 2026 and does not restate them; §9 explains the
  specific obstruction that keeps that door shut.
- **It is not a derivation of $a_{0}$.** The central number is *fitted*. §7 proves that it cannot be
  obtained the obvious way, which is a different and smaller claim than deriving it.

Everything quantitative below is produced by a committed script that exits non-zero if any internal
check fails; each carries negative controls that must trip. Where a result of the author's own has
been withdrawn, it is named as withdrawn rather than quietly dropped.

---

## 1. The coincidence, stated properly

Every cosmologist has noticed that the MOND acceleration scale is of order $cH_{0}$. With
$a_{0}\simeq1.2\times10^{-10}\,\mathrm{m\,s^{-2}}$ and $cH_{0}\simeq6.8\times10^{-10}$, the ratio is
about $2\pi$. Milgrom has remarked on it for forty years. It is usually filed as suggestive and set
aside, for a good reason: $H_{0}$ evolves, $a_{0}$ apparently does not, so any identification is
either a coincidence at the present epoch or a statement about $\Lambda$ rather than $H$.

This framework takes the second option seriously and sharpens it. Write

$$\boxed{\;a_{0}=\kappa\,c\sqrt{G\rho_{\Lambda}}=\kappa\,c^{2}\sqrt{\frac{\Lambda}{3}}
=\frac{c\,H_{\Lambda}}{Z}\;}$$

where $\rho_{\Lambda}$ is the dark-energy density, $H_{\Lambda}=c\sqrt{\Lambda/3}$ is the *asymptotic*
(de Sitter) Hubble rate rather than the present one, and $\kappa$ is a dimensionless number. Two
things follow immediately, and they are the reason to keep reading.

**First, the scale is now a constant for a structural reason, not by fiat.** $H_{\Lambda}$ does not
evolve. The awkwardness of tying a static galactic scale to a time-dependent $H_{0}$ disappears; what
remains is a relation between the *dark-energy* scale and the *dark-matter-phenomenology* scale.

**Second, and this is the part a cosmologist should weigh: ΛCDM has no reason to predict such a
relation, and this framework has no freedom to avoid it.** In ΛCDM, $\Lambda$ and the properties of
the dark-matter halo population are logically independent — nothing forbids a universe with the same
$\Lambda$ and a different rotation-curve phenomenology. Here they are the same number twice. That is
a genuine structural difference, and it is the framework's main asset. It is *not* evidence that the
framework is correct.

Numerically, taking $\kappa=\tfrac12$ and Planck's $\Lambda$:

$$a_{0}=9.36\times10^{-11}\ \mathrm{m\,s^{-2}},\qquad
Z\equiv\frac{cH_{\Lambda}}{a_{0}}=2\sqrt{\frac{8\pi}{3}}=5.7888 .$$

**$\kappa=\tfrac12$ is fitted.** It is one dimensionless number, fixed by galaxy data, and §7 is about
why it has resisted derivation. Note also that $9.36\times10^{-11}$ is some 20% below the
$1.2\times10^{-10}$ commonly quoted; §4.2 explains why that difference is *not* currently a
discriminant, in both directions.

### A caution about footings

Two conventions appear in the literature and both are defensible: $\rho_{\Lambda}$ with $H_{\Lambda}$
(giving $9.36\times10^{-11}$), or the total density with $H_{0}$ (giving $1.13\times10^{-10}$, a factor
$1.2048$ larger). They are not interchangeable, and several published claims about this framework —
including some of the author's own — have flipped sign depending on which was used. **Every number in
the underlying work is computed on both.** Where a conclusion depends on the choice, that is stated.
If you take one methodological lesson from this document, take that one.

---

## 2. The physical idea

### 2.1 De Sitter–Unruh

An observer with proper acceleration $a$ in flat space sees a thermal bath at the Unruh temperature
$T=\hbar a/2\pi ck_{B}$. In de Sitter space an *inertial* observer already sees the Gibbons–Hawking
temperature $T_{\Lambda}=\hbar H/2\pi ck_{B}$. Deser and Levin (1997) showed that an observer with
constant proper acceleration $a$ in de Sitter sees

$$T\;\propto\;\sqrt{a^{2}+a_{\Lambda}^{2}}\,,$$

i.e. the two add in quadrature. **The bath has a floor.** No matter how gently you accelerate, you
cannot get below $T_{\Lambda}$.

Milgrom (1999) drew the consequence that matters. Suppose inertia is the reaction to *the excess*
bath — that what resists acceleration is $\Delta T = T(a)-T(0)$, not $T(a)$. Then

$$\Delta T\;\propto\;\sqrt{a^{2}+a_{0}^{2}}-a_{0}\;\longrightarrow\;
\begin{cases}
a & a\gg a_{0}\quad\text{(Newtonian)}\\[2pt]
a^{2}/2a_{0} & a\ll a_{0}\quad\text{(deep MOND)}
\end{cases}$$

**Both MOND limits, from one quadrature.** The deep-MOND regime is not imposed; it is what
subtracting a floor does to a square root. And the scale at which the crossover happens is set by the
*horizon*, which is the whole point.

**Credit, unambiguously.** This is Milgrom's mechanism, and the interpolating function it yields —
$\nu=\sqrt{1+1/y}$ with $y=g_{\rm bar}/a_{0}$ — is Eq. (9) of Milgrom (1999), not a variant of it.
What this framework adds is the *coefficient*: Milgrom's paper fixes $a_{0}=2cH_{\Lambda}$, whereas
$\kappa=\tfrac12$ corresponds to $a_{0}=cH_{\Lambda}/5.79$. That factor — a little over eleven — is
the framework's distinctive quantitative content, and it is the number §7 fails to derive.

### 2.2 Why this is *modified inertia*, and why that matters

There are two ways to make rotation curves flat without dark matter, and cosmologists often conflate
them.

- **Modified gravity (MG).** The field equation changes. Bekenstein–Milgrom AQUAL replaces
  $\nabla^{2}\Phi=4\pi G\rho$ with $\nabla\!\cdot\![\mu(|\nabla\Phi|/a_{0})\nabla\Phi]=4\pi G\rho$.
  Matter responds normally to a modified field.
- **Modified inertia (MI).** The field is Newtonian; the *response* to it changes. The particle's
  inertial mass depends on its acceleration.

This framework is MI, because the de Sitter–Unruh argument is about what resists acceleration, not
about what sources the field. That commitment has three consequences you should hold onto:

1. **The metric stays Newtonian.** MI *needs* $\nabla^{2}\Phi=4\pi G\rho_{\rm bar}$ to hold; the whole
   content is a modified response to it. §6.4 shows this is satisfied with five orders of margin, and
   for an interesting reason.
2. **Inertial and gravitational mass differ.** The rest energy stays $mc^{2}$ but the inertia is
   $m\mu$. This is not a bug to be explained away — it is what MI *means*. The weak equivalence
   principle survives, because $m$ cancels: $m\mu a=m g_{\rm bar}$ gives $\mu a=g_{\rm bar}$, with no
   reference to composition. Universality of free fall is exact. What fails is the *equality*
   $m_{i}=m_{g}$. And the consequence runs the right way: a galaxy's **gravitating** mass is its
   **baryonic** mass, which is what the phenomenology requires.
3. **MI and MG differ observably**, most cleanly in the external-field effect. This is the sharpest
   live discriminant and §8.2 returns to it.

### 2.3 The price: nonlocality

Milgrom (1994) proved something that constrains every MI theory: **modified-inertia theories with
standard symmetries are generically time-nonlocal.** You cannot write a local Lagrangian in which the
inertial mass depends on the instantaneous acceleration and keep Galilean invariance and the
conservation laws. The particle must remember its own past.

So an MI theory needs a **memory kernel**, and the theory's content is in that kernel. This is where
the framework's technical work lives, and until 2026 it was where the framework was weakest: the
kernel was postulated, the action was not known to be variational, and nobody could say whether the
resulting theory had ghosts.

---

## 3. The phenomenological relation, and how to read it

For circular orbits the framework's law reduces to a relation between the observed and baryonic
accelerations:

$$g_{\rm obs}=\nu\!\left(\frac{g_{\rm bar}}{a_{0}}\right)g_{\rm bar},
\qquad\text{equivalently}\qquad g_{\rm obs}^{2}-g_{\rm bar}^{2}=a_{0}\,g_{\rm bar}$$

the second form being exact for one member of the kernel family and accurate to $2\times10^{-3}$ dex
for another. That is the **radial acceleration relation** (RAR) that McGaugh, Lelli and Schombert
measured on SPARC, and it is a genuine empirical regularity independent of any theory: the observed
acceleration is a tight function of the baryonic one, with scatter at or below the level of the
observational errors.

**How to read the RAR as a test, and how not to.** The RAR does *not* measure $a_{0}$ well. Fitting
the framework's own kernel to SPARC with a global stellar mass-to-light ratio gives $0.108$ dex
scatter at $\Upsilon_{3.6}=0.70$, which is *better* than regularised MOND's $0.122$ dex on the same
data. But the penalty for moving $a_{0}$ by 20% is under half a per cent in that scatter. **The RAR is
compatible with this framework and non-diagnostic of its coefficient.** Claims in either direction —
"$a_{0}$ is 20% too low", "$a_{0}$ is 20% too high" — are interpolation-shape and mass-to-light
artefacts. Two such claims in the author's own corpus were withdrawn for exactly this reason.

The same caution applies to the **baryonic Tully–Fisher relation**. MOND predicts $v^{4}=GMa_{0}$
exactly, so the BTFR *intercept* is a clean handle on $a_{0}$ in principle. In practice
$M_{\rm bar}\propto\Upsilon_{*}$, and the framework's $a_{0}$ requires $\Upsilon_{3.6}\approx0.86$
against the $0.5$ used in the standard fit — high, but inside the literature spread and near the
$0.70$ an independent RAR fit prefers. **A mass-to-light question, not an $a_{0}$ question.**

The sharpest $\Upsilon$-free handle is the **gas-dominated** subsample, where the stellar contribution
is small and the slope of $g_{\rm obs}^{2}-g_{\rm bar}^{2}$ against $g_{\rm bar}$ estimates $a_{0}$
directly. That gives a box $0.84$–$1.36\times10^{-10}$, roughly $\pm16\%$, which *contains* the
framework's $9.36\times10^{-11}$ — and also contains $1.2\times10^{-10}$. It does not discriminate.

**The honest summary of galaxy-scale phenomenology: it works, it works at least as well as MOND, and
it does not measure the coefficient.** Anyone who tells you the RAR settles this — either way — has
not propagated the mass-to-light freedom.

---

## 4. Where it is in trouble

A guide that only lists successes is advocacy. Four fronts deserve a sceptic's attention, and the
fourth is the serious one.

### 4.1 The interpolation function is constrained from an unexpected direction

MOND's interpolating function is usually treated as free within limits. It is not: the *solar system*
constrains its approach to Newtonian behaviour, because a residual anomalous acceleration would show
up in planetary ranging. Two natural power-law families fail. The $1/g$-tailed kernel misses the
Earth/Mars bound by a factor $\sim1300$. The next one misses the Mars ranging budget by
$8.5$–$12.4\times$, and for a subtle reason worth knowing: its slowly-decaying tail binds not at a
planet but at **the Sun**, whose acceleration in the field of Jupiter is itself only
$\sim2000\,a_{0}$.

The surviving choice is an **exponential** approach, $\nu=1/(1-e^{-\sqrt{y}})$, whose Newtonian
residual dies as $e^{-\sqrt{y}}$ — utterly negligible at ephemeris accelerations. This is a real
constraint, arrived at against the author's preference, and it retired two published kernel choices.
*It also invalidated a sentence in the author's own field-theory paper five days after the kernel
changed; that correction is recorded in §10.*

### 4.2 The coefficient is fitted, and the discrimination is marginal

$\kappa=\tfrac12$ versus Milgrom's own later $1/2\pi$ differ by a factor $\pi$ in $a_{0}$. Fitting
SPARC with per-galaxy mass-to-light ratios gives $\sigma(a_{0})$ of a few per cent against an
$8.2\%$ gap, and $\Delta\chi^{2}$ favouring $\kappa=\tfrac12$ at about $2.2\sigma$. **That is
suggestive and it is not a measurement.** Against interest: the best fit is $1.15\times$ the canonical
value, and the alternative footing fits *better*. And a further caution — that $2.2\sigma$ does not
survive the kernel change of §4.1 on the surviving kernel's own shape, where it flips to $0.66\sigma$
the other way.

### 4.3 Theory prefers a different coefficient

Stated plainly because it cuts against the framework: of the two dimensionless constants that appear
naturally in this construction, **both are $2\pi$**, which is Milgrom's value, not $\tfrac12$. The
data prefer $\tfrac12$ at $2.2\sigma$; the theory prefers $2\pi$. That tension is unresolved and it is
not in the framework's favour.

### 4.4 Clusters

**This is the strongest reason to think the framework is wrong, and it is not new to it.**

MOND-like kernels underpredict the mass discrepancy in galaxy clusters. On this framework's own
kernel, the required boost at $R_{500}$ has median $\eta=2.334$ where the kernel supplies less, a
shortfall of $+0.405$ dex, which depending on the error treatment is $2.0$–$4.1\sigma$. Equivalently,
the acceleration at which clusters would need the transition to happen is $\sim2\times10^{-9}$
m s$^{-2}$ — about $22\times a_{0}$. The discrepancy is not uniform: it grows inward, spanning roughly
$3\times$ to $24\times$ across methods and radii.

Three honest observations, none of them a rescue:

- It is a **shared** problem. Every MOND-like kernel has it. That does not make it smaller.
- Part of it is a **mass-calibration** question. Weak-lensing recalibrations move the required boost to
  $\sim1.6$–$1.8$. That helps and does not close it. (An earlier claim in the author's corpus that
  X-ray calorimetry closed it was **withdrawn**.)
- The framework's *distinctive* prediction here — a scatter in the boost induced by variations in the
  external field — is testable, but the sample sizes required are $5\times10^{3}$ to $2.6\times10^{5}$
  clusters depending on the field strength, which is $1$–$60\times$ **above** what is available. The
  front is not dead; it is not currently decidable either.

If you are looking for the observation most likely to kill this framework, it is clusters, and it has
been for thirty years.

---

## 5. Why the theory was hard

Before 2026 the objection a field theorist would raise was not about phenomenology. It was that there
was no *theory*: a kernel postulated by hand, no action known to reproduce it, and no ghost analysis.
Two obstructions stood in the way, and the first is a genuine theorem.

### 5.1 A parity theorem: no polynomial worldline action can do it

Suppose you try to build an MI action from four-velocities at several proper times —
$u(\tau)$, $u(\tau-s)$, and so on — contracted into scalars. Minkowski space admits exactly two
invariant tensors: the metric (rank 2) and the Levi-Civita tensor (rank 4). **Both have even rank.**
Every polynomial scalar you can build therefore has **even degree in $u$**, and on a circular orbit
contributes only **even powers of the orbital speed**.

But the deep-MOND limit needs the **first** power. On a circular orbit
$|a|=\gamma^{2}\Omega v$ — linear in $v$. So a polynomial construction is not merely inaccurate; it
misses by exactly one power of $v$, which at galactic speeds is a factor $(c/v)^{2}\sim10^{6}$–$10^{7}$
in amplitude.

**No polynomial worldline self-interaction, at any degree, can produce MOND.** The escape must be
non-analytic.

### 5.2 The escape: the rapidity gap

The object that supplies $|a|$ *linearly* is the **hyperbolic angle between four-velocities at two
proper times**:

$$\cosh\theta(\tau,\tau-s)=-\frac{u(\tau)\cdot u(\tau-s)}{c^{2}},\qquad
\frac{\theta(s)}{s}\;\xrightarrow[s\to0]{}\;\frac{|a|}{c}$$

because **proper acceleration is the rate at which rapidity accumulates**. The gap is non-analytic in
the bilinear $u\cdot u'$ — that is what lets it evade §5.1 — and it delivers $|a|$ with no $(v/c)^{2}$
suppression. For a general worldline the gap across an interval is $s/c$ times the acceleration
magnitude at the **midpoint**, to third order.

The action is then one line:

$$\boxed{\;S=-mc^{2}\!\int\Big[\mu(\Theta)\,d\tau+\big(1-\mu(\Theta)\big)\,dt\Big],\qquad
\Theta(\tau)=\int_{0}^{\infty}\!ds\,K(s)\,\cosh^{-1}\!\Big(\!-\frac{u(\tau)\cdot u(\tau-s)}{c^{2}}\Big)\;}$$

with $d\tau$ the proper time and $dt$ the cosmological time. Its two limits are the two most natural
scalars a worldline has: $\mu\to1$ gives $-mc^{2}\!\int d\tau$, the free relativistic particle;
$\mu\to0$ gives $-mc^{2}\!\int dt$, a Lagrangian that is exactly velocity-**independent**, so the
inertia vanishes while the rest energy stays $mc^{2}$. **The action interpolates between proper time
and cosmological time, and the interpolation variable is the accumulated rapidity gap along the
particle's own past.**

The kernel's **first moment** $M_{1}=\int s\,K(s)\,ds$ is the only surviving parameter, and
$a_{0}=\tfrac23 c/M_{1}$. The factor $\tfrac23$ is not cosmetic: on a circular orbit the acceleration
*direction* rotates, which generates a memory force, and the correct balance renormalises
$a_{0}\to\tfrac23 a_{0}$. (An earlier version of this calculation missed that and was corrected.)

---

## 6. The field theory, in four moves

As of August 2026 the construction is a local, generally covariant field theory. Here is how, at the
level of what each move buys.

### 6.1 The memory kernel becomes a local field

This is the move that removes the nonlocality. With the midpoint form, $\Theta$ carries both a factor
$s$ and a lag $s/2$; substituting $s=2u$ collapses **both** into one kernel,
$G(u)=4u\,K(2u)$. For an exponential $K$, $G(u)=g\,u\,e^{-mu}$ — **which is the retarded Green's
function of $(d/d\tau+m)^{2}$.** Therefore

$$\ddot\chi+2m\dot\chi+m^{2}\chi=\frac{g\,|a|}{c},\qquad \Theta=\chi$$

**a damped oscillator whose friction term *is* the memory.** The equivalence is closed numerically to
$10^{-23}$, not merely as a transform identity. The damping is *critically* damped, exactly, and the
second-order minimality traces back to the rapidity gap being linear in $s$ — the same fact that will
matter in §7.

Two consequences. **First, $a_{0}$ becomes a coupling ratio:**

$$a_{0}=\tfrac23\,c\,\frac{m^{2}}{g}$$

the ratio of the auxiliary field's mass squared to its coupling. **Second, the ghost question becomes
a computation.** The multiplier enforcing the constraint obeys the *anti*-damped adjoint equation, and
the kinetic form is indefinite — a ghost by the naive criterion. It is not a new degree of freedom:
that multiplier is a **costate**, carrying a final-value condition and no Cauchy data, and the count
closes exactly at four, matching the order of the equation of motion. The indefinite metric is the
Keldysh branch of the in-in formalism. This *replaces* the older argument that Ostrogradsky's theorem
is merely silent.

Covariantly the memory sector is second-order relaxation along the matter flow — structurally the
Israel–Stewart class, which exists precisely because first-order dissipative hydrodynamics is
acausal. Good company, and only an analogy.

### 6.2 The preferred frame becomes dynamical

MI presupposes a preferred frame — a cosmological rest frame in which $dt$ makes sense. Writing it as
a fixed background vector breaks general covariance by hand. The fix is standard technology: replace
it by the normalised gradient of a scalar **khronon**,
$n_{\mu}=-\partial_{\mu}T/\sqrt{-(\partial T)^{2}}$, which is invariant under $T\to f(T)$, so the
*foliation* is physical and the *labelling* is gauge. Lorentz violation becomes **spontaneous** rather
than stipulated.

Nothing is lost: in the gauge $|\partial T|=1$ with $T=t$, the covariant coupling reduces *exactly* to
the original. The published worldline action is the **unitary gauge** of the khronon action.

Two structural results fall out. **The vorticity vanishes identically** — for any $n$ built from a
gradient, in every metric — so this is the hypersurface-orthogonal (Hořava) sub-case of
Einstein-aether, and the spin-1 sector is **removed**. And, unexpectedly:

$$a^{\mu}[n]=\partial^{\mu}\Phi\qquad\text{(weak field, static)}$$

**the khronon's own acceleration is the Newtonian field.** Before covariantising, the only
acceleration in the theory was the particle's $|a|$. MOND is a relation between $g_{\rm obs}$ and
$g_{\rm bar}$, and $g_{\rm bar}$ now exists as a *geometric object*. §8.2 shows this creates a genuine
fork.

### 6.3 The scalar mode is healthy, in an explicit window

The theory has one propagating scalar beyond the graviton. Its speed is

$$c_{s}^{2}=\frac{(2-\eta)(\lambda-1)}{\eta\,(3\lambda-1)}$$

in terms of two new couplings. **No ghost** requires $\lambda>1$ or $\lambda<1/3$; **no gradient
instability** requires $0<\eta<2$. Remarkably the two conditions exclude *exactly* the same band
$1/3<\lambda<1$ — one band, two diseases. The healthy region is nonempty and explicit. The graviton's
speed is $\xi$, so GW170817 makes $\xi=1$ a **measurement** to $\sim10^{-15}$, not a choice. And a
sanity check the derivation passes: at $\eta=0$ the scalar's constraint degenerates and the mode
disappears, correctly reproducing the fact that **general relativity has no propagating scalar.**

Preferred-frame post-Newtonian constraints push both $\lambda-1$ and $\eta$ small, and in that corner
$c_{s}^{2}\to(\lambda-1)/\eta$ *exactly* — only the ratio survives. The vacuum Cherenkov bound
(a subluminal mode would be radiated by ultra-high-energy cosmic rays) then reduces to the single
inequality $\lambda-1\ge\eta>0$, and superluminal propagation is safe precisely because there *is* a
preferred frame. **Two independent constraints, no conflict.**

**Against interest, twice.** The health is achieved *by choice*, not predicted: the covariantisation
**added two free parameters** and nothing forces them into the window. And the corner that PPN prefers
is the known strong-coupling corner — though when computed, the cutoff is
$\Lambda_{\rm sc}\sim\sqrt{\eta}\,M_{\rm Pl}/c_{s}\sim10^{15}$ GeV, and a deliberately pessimistic
scan over powers $\eta^{p}$, $p=\tfrac12\ldots4$, still leaves it above every scale the theory is
applied at, with 26 orders of margin against galactic scales even in the worst case. Also computed:
the leading *static* self-interaction of the khronon sector is **quartic**, not cubic — the two sectors'
cubics vanish for two different reasons — so the nonlinearity is $(\partial\pi)^{2}\sim(v/c)^{2}\le10^{-5}$
everywhere it is applied and **there is no Vainshtein-type screening.**

### 6.4 MOND comes out of the joint equations

The pieces then close, and the way they close is the nicest thing in the construction.

MI *needs* an unmodified Newtonian field. In the khronon theory, corrections to $\Phi$ are of order
the same small parameters that §6.3 constrained — $\lesssim10^{-7}$ — while MOND phenomenology needs
$\Phi_{\rm bar}$ only to about a per cent. **Five orders of margin. The constraint that made the
scalar healthy is what guarantees the Newtonian background the framework presupposes.** It is not a
cost; it is a consistency requirement the theory needed anyway.

With the Newtonian metric established *independently*, the worldline equation gives

$$\mu\!\left(\frac{g_{\rm obs}}{a_{0}}\right)g_{\rm obs}=g_{\rm bar}
\;\Longrightarrow\;g_{\rm obs}=\sqrt{a_{0}g_{\rm bar}}
\;\Longrightarrow\;v^{4}=GMa_{0}$$

flat rotation curves and the BTFR, with **no new parameter**. The closure is not circular: the
Newtonian metric came from the gravitational sector, not from the MOND relation.

**Field content: two tensor modes, one scalar, and nothing from the memory sector.** Three propagating
degrees of freedom.

---

## 7. Why $a_{0}$ is not derived — and a theorem about why not

Everything above trades one number for another. $a_{0}=\tfrac23c\,m^{2}/g$ is a *relation*, not a
prediction: it says the acceleration scale is a coupling ratio, which is progress in status but not in
content. The obvious next move is to compute the memory kernel from the de Sitter vacuum itself. That
move has now been shown to fail, for a reason sharp enough to be worth stating.

**The de Sitter correlator is exactly thermal.** Along a geodesic, the conformally coupled massless
two-point function restricted to the worldline is

$$k(s)=\frac{a^{2}}{\sinh^{2}(as)},\qquad a=\frac{H}{2}=\frac{\pi}{\beta}$$

which satisfies the KMS condition at $T=H/2\pi$ — verifiable by imaginary-time periodicity rather than
by citation — with the *flat* $1/s^{2}$ short-distance singularity and a curvature correction
$-H^{2}/12$.

**All its moments are one closed form.** Using $1/\sinh^{2}x=4\sum_{n}n\,e^{-2nx}$,

$$M_{p}=\int_{0}^{\infty}\!ds\;s^{p}\,k(s)=2^{\,1-p}\,\Gamma(p{+}1)\,\zeta(p)\,a^{1-p}$$

checked against quadrature at $p=\tfrac12,\tfrac32,2,3,4$; at $p=0$ the analytic continuation and the
physical Hadamard subtraction agree, which is what licenses using the continuation at all.

**And now the point.** $\zeta$ has exactly one pole, at $p=1$. Meanwhile the rapidity gap is
$\theta=(s/c)|a|$ — **linear in $s$** — so the action pairs the kernel against $s^{1}$ and nothing
else. **The one moment the framework requires is the one moment the correlator does not have.**
Scheme-independently, $(p-1)M_{p}\to1$: a simple pole with residue exactly one.

The same integer forbids the required irrationality. The target carries $\sqrt{\pi}$, and a
half-integer power of $\pi$ enters $M_{p}$ only through $\Gamma(3/2)=\sqrt{\pi}/2$ at *half-integer*
$p$ — which the linear gap forbids. **The divergence and the missing $\sqrt{\pi}$ are one fact:
$p=1$.**

Two independent routes were closed alongside it. A mode sum over the Lorentz generators cannot supply
the $\sqrt{\pi}$ either, because **every** relevant group and sphere volume has integer $\pi$-weight
(the $\Gamma$ in $\mathrm{Vol}(S^{n-1})=2\pi^{n/2}/\Gamma(n/2)$ returns the compensating factor). And a
dimension-counting argument that appeared to give $\kappa=\tfrac12$ at $D=4$ was **withdrawn** when the
framework's own $D$-dependence turned out to be a different function agreeing only at $D=4$ — five
prespecified functions fit that single point equally well.

**What survives is a reframing, and it is worth having.** A logarithmically divergent moment's finite
part is a **renormalisation condition**. So $a_{0}$ is the subtraction point of the theory — the same
status as a Yukawa coupling in the Standard Model, which is a complete field theory with nineteen such
numbers. **A theory is not incomplete because it has a parameter.** But it is also not predictive
about that parameter, and no amount of restatement changes that.

What remains unexplained, after tracing $\sqrt{6}$ to the Friedmann equation and $\sqrt{\pi}$ to the
three-dimensional momentum measure, is a single rational: $M_{1}=\tfrac43 t_{\Lambda}$ where
$t_{\Lambda}=(G\rho_{\Lambda})^{-1/2}=50.7$ Gyr is the vacuum's own free-fall time. Since
$\tfrac43=2\times\tfrac23$ and the $\tfrac23$ is the derived memory-force factor, **the entire residue
is one bare factor of two.** Sixteen distinct attempts to force it have failed.

---

## 8. What would kill it

### 8.1 The pre-registered wide-binary test

Wide binaries at $2$–$30$ kAU separation have internal accelerations near $a_{0}$ while sitting in the
Galaxy's external field — the cleanest laboratory for MOND-like behaviour, and the site of the
external-field effect that distinguishes MI from MG. The author's prediction is frozen and
hash-stamped, with an amendment chain filed in the open:

$$\gamma_{v}=1.1582,\qquad 1.1311\text{–}1.1964\ \text{(radial convention)}$$

where $\gamma_{v}$ is the ratio of the measured velocity scale to the Newtonian one.

**One statement in that test has teeth: a Newtonian result across the window is evidence against at
$4.74$–$7.10\sigma$** at the registered sample size, and that figure is robust because under a
Newtonian truth the estimator's shape bias vanishes identically.

**Everything else about the test is weaker than its author originally expected, and the registration
says so.** The frozen decision table's bins *collide* with the prediction — $1.1582$ falls in an
interval pre-declared as disfavouring MI, and the modified-gravity target $1.137$ lies *inside* the MI
range — so the binding remedy is to report the raw estimate with both distances and **no verdict
word**. A calibration nuisance sits outside its frozen window, whose pre-declared consequence is
"systematic-limited, no verdict — reported, not repaired". One corner is pre-declared *unscoreable*.
And two further checks are underpowered: the anisotropy falsifier reaches $1.0$–$1.1\sigma$ at the
registered $N$ (needing seven to nine times as many pairs, after a projection dilution of $0.24$ that
costs a factor four), and the gated variant of the theory is $0.03$–$0.06\sigma$ from Newtonian in the
aggregate — meaning an aggregate-only analysis would report "Newtonian" for a universe in which it is
true.

**The honest position: this test can disfavour the framework decisively and can support it only
weakly.**

### 8.2 The directional external-field test

This is the sharpest MI-versus-MG discriminant, and §6.2 sharpened it further. Because the khronon's
acceleration *is* $g_{\rm bar}$, the covariant theory contains **two** acceleration scalars, and the
memory can be sourced by either: the particle's own $|a|$ (**pure MI**) or the khronon's
$|a[n]|=g_{\rm bar}$ (a **third theory**, external-field-driven, neither pure MI nor AQUAL, sharing the
same interpolation function). The worldline formulation could not even express this fork.

They differ observably. In a rotation-curve asymmetry aligned with the external field direction,
**pure MI predicts exactly zero**; AQUAL-class theories predict $1$–$4\%$ with a definite sign. A
first firing of this test on 237 galaxies gave a signal of the AQUAL-class sign at $p\approx0.03$ —
which, if it holds, is evidence against the *pure*-MI branch of this framework. It needs
$N\sim1000$ galaxies to settle, and the direction is reconstructable from existing peculiar-velocity
maps.

### 8.3 Redshift evolution

$a_{0}\propto\sqrt{\rho_{\Lambda}}$ makes a prediction ΛCDM does not: if dark energy evolves,
$a_{0}$ evolves with it. In the general parametrisation the closed form is

$$\frac{a_{0}(z)}{a_{0}(0)}=(1+z)^{\frac32(1+w_{0}+w_{a})}\exp\!\left(-\frac{3w_{a}z}{2(1+z)}\right)$$

which for the DESI-preferred region is a **bump followed by a decline**, not a monotonic rise. This
matters because a 2026 measurement reports $a_{0}$ *rising* with redshift. That is a **tension**, not a
confirmation — and an earlier analysis claiming otherwise was withdrawn after it was found to have
dropped $w_{a}$ in a low-redshift expansion, manufacturing agreement. If $w\to-1$ exactly, the
prediction becomes a constant and this front dissolves.

### 8.4 The one prediction nobody is testing

The framework's preferred-frame coupling scales as $g^{-2}$ with the *local* gravitational
acceleration: about $10^{-23}$ in a terrestrial laboratory, $3\times10^{-17}$ at Earth's orbit, and of
order unity only in the outer disc of a galaxy. This is the **opposite** of a constant
Lorentz-violating background — largest exactly where no experiment exists, smallest where the limits
are tightest. **Binning existing Lorentz-violation constraints by local $g$ would test it**, and to
the author's knowledge nobody has.

---

## 9. The ledger

**Derived, in the sense of following from the construction:**

- Both MOND limits, from the de Sitter quadrature (Milgrom's mechanism).
- That no *polynomial* worldline action can produce MOND (parity theorem), so the rapidity gap is
  forced rather than chosen.
- $v^{4}=GMa_{0}$ and the flat rotation curve, from the joint field equations, with no new parameter.
- The memory kernel as a local, critically damped auxiliary field; ghost-freedom by degree-of-freedom
  count; the spin-0 health window; a strong-coupling scale far above every applied regime; no
  Vainshtein screening.
- That the khronon's acceleration is the Newtonian field — and therefore the MI/MG fork.
- The $D$-dependence of the coefficient, $\kappa_{D}=\tfrac12\sqrt{6/((D-1)(D-2))}$.
- $\sqrt{6}$ from the Friedmann equation; $\sqrt{\pi}$ from the three-dimensional momentum measure.

**Fitted:**

- $\kappa=\tfrac12$, equivalently $M_{1}=\tfrac43t_{\Lambda}$. **One number.** The residue after the
  two irrationalities are accounted for is a single factor of two.
- Two new couplings from the covariantisation, constrained but not predicted.
- The kernel's memory time, bounded by planetary ranging.

**Excluded, or closed:**

- Deriving $a_{0}$ from the de Sitter correlator ($p=1$ is $\zeta$'s pole).
- Deriving it from a Lorentz-generator mode sum ($\pi$-parity).
- Both power-law interpolation kernels (solar-system ranging).
- The author's own $\kappa=(2/3)(D-1)/D$, withdrawn as a form.
- Any claim about the Standard Model: the framework's characteristic constant carries $\sqrt{\pi}$
  while all flavour observables are algebraic, so the relevant structure is *blind* to the gauge
  sector. This is the specific obstruction referred to in §0.

**Open, and honestly open:**

- Clusters, at $2$–$4\sigma$ on the framework's own kernel (§4.4). **The most likely killer.**
- The bare factor of two in the coefficient.
- Whether the memory is sourced by $|a|$ or by $g_{\rm bar}$ (§8.2) — an unresolved fork *within* the
  framework.
- Strong fields: near a horizon the khronon expansion fails, and universal horizons in
  Lorentz-violating gravity are unaddressed.
- $a_{0}(z)$, which is hostage to whether $w$ evolves.

---

## 10. What a referee should attack, and a note on error rates

**The four sharpest attacks**, in the author's own estimation:

1. **Clusters.** Not shared-problem deflection; the $+0.4$ dex and its radial growth.
2. **Whether the memory should be sourced by the particle's acceleration at all** (§8.2). The fork is
   a genuine ambiguity of the covariant theory, not a detail — and one arm of it may already be
   disfavoured.
3. **That the covariantisation added parameters.** Two new couplings bought general covariance and
   ghost-freedom. Health achieved by choice is weaker than health predicted.
4. **The identification of the memory kernel with a vacuum autocorrelation** — the one physical
   postulate §7 rests on. The obvious alternative is closed (a free field's retarded kernel is
   temperature-independent, so it could never carry $H$), but the postulate itself is a postulate.

**A note on error rates, offered because it bears on how to read any of this.** The work behind this
guide was carried out with heavy use of automated verification, and the reason is empirical: on the
single day the field theory was assembled, six load-bearing claims were drafted, checked, and found
wrong — a past-directed sign convention, an invariance argument that assumed its own conclusion, an
asserted observational band replaced by a computed one, an overstated limitation, a claimed cutoff
that did not clear collider energies at all powers, and a ratio quoted as exact when its coefficient
was three. One check passed *vacuously* on an empty list before being caught. Each is recorded in the
relevant deposit.

That rate is not unusual for exploratory theory; what is unusual is having a mechanism that surfaces
it. **Every quantitative claim in this document is generated by a script that exits non-zero on
failure and carries controls designed to trip.** Where those scripts contradicted the author, the
author lost. A reader is invited to run them, and to treat any claim here that lacks one with
appropriate suspicion.

---

## Selected references

**The mechanism and the phenomenology.** M. Milgrom, *The modified dynamics as a vacuum effect*,
Phys. Lett. A **253**, 273 (1999) — the de Sitter–Unruh argument and the interpolating function used
here. M. Milgrom, *Dynamics with a non-standard inertia–acceleration relation*, Ann. Phys. **229**, 384
(1994) — generic time-nonlocality of modified inertia, and its conservation laws. S. Deser and
O. Levin, Class. Quantum Grav. **14**, L163 (1997) — accelerated detectors in de Sitter.
J. Bekenstein and M. Milgrom, Astrophys. J. **286**, 7 (1984) — AQUAL. S. McGaugh, F. Lelli and
J. Schombert, Phys. Rev. Lett. **117**, 201101 (2016) — the radial acceleration relation.
S. McGaugh, Astron. J. **143**, 40 (2012) — the baryonic Tully–Fisher relation.

**The vacuum.** G. Gibbons and S. Hawking, Phys. Rev. D **15**, 2738 (1977). T. Bunch and P. Davies,
Proc. R. Soc. A **360**, 117 (1978). H. Narnhofer, I. Peter and W. Thirring, Int. J. Mod. Phys. B
**10**, 1507 (1996).

**The preferred-frame sector.** P. Hořava, Phys. Rev. D **79**, 084008 (2009). T. Jacobson and
D. Mattingly, Phys. Rev. D **64**, 024028 (2001). T. Jacobson, Phys. Rev. D **81**, 101502 (2010).
D. Blas, O. Pujolàs and S. Sibiryakov, Phys. Rev. Lett. **104**, 181302 (2010) and JHEP **1104**, 018
(2011). D. Blas and S. Sibiryakov, Phys. Rev. D **84**, 124043 (2011) — universal horizons.
W. Israel and J. Stewart, Ann. Phys. **118**, 341 (1979). J. Elliott, G. Moore and H. Stoica, JHEP
**0508**, 066 (2005) — vacuum Cherenkov.

**Wide binaries.** I. Banik et al. (2024). K. El-Badry, H.-W. Rix and T. Heintz, MNRAS **506**, 2269
(2021).

**This framework's own deposits**, all with reproducibility scripts: the covariant field theory
(concept DOI 10.5281/zenodo.21854914); the no-go on deriving $a_{0}$ from the vacuum correlator
(10.5281/zenodo.21854464); the worldline action (10.5281/zenodo.21845411).

---

**AI-assistance disclosure.** Portions of the analysis, numerical verification and drafting were
carried out with the assistance of a large language model (Anthropic Claude). The author directed the
work, specified and reviewed every load-bearing calculation, and takes full responsibility including
for any errors. No AI system satisfies the criteria for authorship and none is listed as an author.
Several intermediate claims produced during the work were found to be incorrect and withdrawn; §10
names them rather than omitting them.
