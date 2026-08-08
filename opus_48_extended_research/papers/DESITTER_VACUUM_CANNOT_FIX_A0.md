# Why the de Sitter vacuum cannot fix the MOND acceleration scale: the required moment is the pole of ζ

**Carl P. Zimmerman**
Briar Creek Tech

*Version 1 (2026-08-08).*

---

## The result in one line

For a modified-inertia worldline action whose memory kernel is the de Sitter vacuum
autocorrelation, the acceleration scale is fixed by that kernel's **first** moment. All the moments
have one closed form, and

$$\boxed{\;M_{p}\;=\;\int_{0}^{\infty}\!ds\;s^{p}\,\frac{a^{2}}{\sinh^{2}(as)}\;=\;2^{\,1-p}\,\Gamma(p{+}1)\,\zeta(p)\,a^{1-p}\;,\qquad a=\tfrac{H}{2}=\frac{\pi}{\beta}\;}$$

so the moment the theory needs, $p = 1$, is **exactly the pole of $\zeta$** — the only pole $\zeta$
has. The divergence is not a technical nuisance to be renormalised away and then quietly used: it is
the same fact that forbids the required $\sqrt{\pi}$, because a half-integer power of $\pi$ enters
$M_{p}$ only through $\Gamma(3/2) = \sqrt{\pi}/2$ at *half-integer* $p$, and the rapidity gap
$\theta = (s/c)|a|$ is *linear* in $s$, which forces $p = 1$ and forbids every half-integer.

**One integer therefore carries the whole obstruction.** The consequence is positive as well as
negative: $M_{1} = c/a_{0}$ is a **renormalisation condition**, not a computable number, and $a_{0}$
is the subtraction point of the theory rather than one of its outputs.

**What this is not.** It is not a derivation of the MOND coefficient, and it is not a step toward
one — it is a proof that one particular and much-travelled route cannot produce it. Two further
routes are closed in §7 by the same $\pi$-parity mechanism. §8 states plainly what remains open.

---

## 1. What is being asked

Milgrom's vacuum reading of MOND [1] puts a constant-acceleration observer in de Sitter space,
identifies $a_{0}$ with $\sqrt{\Lambda/3}$, and forms the temperature excess
$\Delta T = T(a) - T(0)$ with $T \propto \sqrt{a^{2} + a_{0}^{2}}$ — a structure that reproduces
both MOND limits. The interpolating function that follows,
$\nu = \sqrt{1 + 1/y}$, is Eq. (9) of that paper; it is not a variant of it, and nothing about the
kernel is new here. Milgrom's companion result [2] is equally load-bearing for what follows:
modified-inertia theories are *generically time-nonlocal*. The memory-kernel framing is his.

In a worldline realisation of that picture [3] the nonlocality is explicit,

$$S \;=\; -mc^{2}\!\int\Big[\mu(\Theta)\,d\tau + \big(1-\mu(\Theta)\big)dt\Big],
\qquad
\Theta(\tau) \;=\; \int_{0}^{\infty}\!ds\,K(s)\,\cosh^{-1}\!\Big(\!-\tfrac{u(\tau)\cdot u(\tau-s)}{c^{2}}\Big),$$

and the acceleration scale enters through exactly one number, the kernel's first moment
$M_{1} = \int_{0}^{\infty} s\,K(s)\,ds$. With the memory force of general orbits included,
$a_{0} = \tfrac{2}{3}c/M_{1}$, and the coefficient question becomes a proved equivalence:

$$\kappa = \tfrac12
\quad\Longleftrightarrow\quad
M_{1} = \tfrac43\,(G\rho_{\Lambda})^{-1/2} = \tfrac43\,t_{\Lambda},
\qquad
t_{\Lambda} = 50.74\ \text{Gyr},$$

where $a_{0} = \kappa\,c\sqrt{G\rho_{\Lambda}}$ and $\kappa = \tfrac12$ gives the observed
$9.36\times10^{-11}\,\mathrm{m\,s^{-2}}$. Equivalently, in units of the thermal time
$\beta = 2\pi/H_{\Lambda}$,

$$\frac{M_{1}}{\beta} \;=\; \sqrt{\frac{32}{27\pi}} \;=\; 0.61421182 ,$$

**a footing-invariant target**: it is numerically identical under the canonical footing
($\rho_{\mathrm{DE}}$ with $cH_{\Lambda}$, $a_{0} = 9.3619\times10^{-11}$,
$t_{\Lambda} = 50.74$ Gyr) and under the alternative footing (a factor $1.2048$ larger,
$a_{0} = 1.1279\times10^{-10}$, $t_{\Lambda} = 42.11$ Gyr), because both $M_{1}$ and $\beta$ scale
the same way. Nothing below depends on that choice.

The question of this paper is therefore sharp and self-contained. **The kernel $K$ is a vacuum
autocorrelation. Compute its first moment. Does it equal $\tfrac43 t_{\Lambda}$?**

---

## 2. The correlator is exactly thermal

**Theorem 1.** *Along a geodesic in $dS_{4}$, the conformally coupled massless scalar two-point
function restricted to the worldline is*

$$k(s) \;=\; \frac{a^{2}}{\sinh^{2}(as)},\qquad a=\frac{H}{2}=\frac{\pi}{\beta},\qquad \beta=\frac{2\pi}{H},$$

*and this function is thermal at $T = H/2\pi$ in the strict KMS sense.*

Three independent verifications are carried in the accompanying script, none of them by citation:

1. **KMS periodicity.** $k(s + i\pi/a) - k(s) = 0$ identically, i.e. periodicity in imaginary time
   with period $\beta = \pi/a = 2\pi/H$. This *is* the KMS condition; the temperature is not
   inserted, it is read off.
2. **Coincidence with the flat thermal correlator.** $(\pi/\beta)^{2}/\sinh^{2}(\pi s/\beta)$ at
   $\beta = \pi/a$ is the same function, symbol for symbol. De Sitter along a geodesic *is* a heat
   bath, not merely thermal-like.
3. **Short-distance structure.** $k(s) = 1/s^{2} - H^{2}/12 + O(s^{2})$. The singularity is the
   *flat* $1/s^{2}$ with no $H$ in it — so the Hadamard subtraction is exactly $1/s^{2}$ — and the
   first correction is pure curvature. A control confirms this detects curvature rather than
   restating a trivial identity: the flat correlator's subtracted limit is exactly zero, de
   Sitter's is $-H^{2}/12$.

The large-$s$ behaviour is $k \to 4a^{2}e^{-Hs}$, decay at the thermal rate. This is all classical
[4,5,6]; it is stated with verification because everything after it is arithmetic on this function.

---

## 3. All the moments in one closed form

**Theorem 2.** *With $1/\sinh^{2}x = 4\sum_{n\ge1} n\,e^{-2nx}$ (verified numerically to
$<10^{-30}$),*

$$M_{p} \;=\; \int_{0}^{\infty}\!ds\;s^{p}\,k(s) \;=\; 2^{\,1-p}\,\Gamma(p{+}1)\,\zeta(p)\,a^{1-p}.$$

The underlying Mellin transform $\int_{0}^{\infty} x^{z-1}\sinh^{-2}x\,dx = 2^{2-z}\Gamma(z)\zeta(z{-}1)$
is a tabulated classical integral; the content here is what it says about $p = 1$.

Verification matters because $p$ ranges over both convergent and continued regimes:

| $p$ | closed form | quadrature | relative error | route |
|---|---|---|---|---|
| $1/2$ | $-1.531324582669376$ | $-1.531324582669376$ | $9.2\times10^{-23}$ | subtracted |
| $3/2$ | $2.934997656735202$ | $2.934997656735202$ | $9.5\times10^{-23}$ | bare |
| $2$ | $2.349905809783181$ | $2.349905809783181$ | $0$ | bare |
| $3$ | $3.679766030080391$ | $3.679766030080391$ | $1.3\times10^{-41}$ | bare |
| $4$ | $9.466383968318993$ | $9.466383968318993$ | $1.9\times10^{-41}$ | bare |

For $p > 1$ the bare integral converges. For $p < 1$ it power-diverges at $s \to 0$ and the
Hadamard-subtracted integral is the right object — and the two agree, which is what licenses using
the continuation at all: at $p = 0$ the closed form gives **exactly** $-a$ (because
$\zeta(0) = -1/2$), and the physically subtracted quadrature reproduces $-a$ to $10^{-25}$. The
analytic continuation and the physical subtraction are the same map.

**Corollary 2.1 (the pole).** $\zeta$ has exactly one pole, at $p = 1$, and

$$(p-1)\,M_{p} \;\longrightarrow\; 1 \qquad (p \to 1),$$

verified as $1.0067,\ 1.00007,\ 1.0000007,\ 1.0000000066$ at $p - 1 = 10^{-2},10^{-4},10^{-6},10^{-8}$:
**a simple pole with residue exactly 1, scheme-independently.** Every other integer moment
$p = 0,2,3,4,5$ is finite, so the divergence is specific, not generic. In closed form the
divergence is logarithmic with unit coefficient,

$$\int_{\delta}^{\infty}\!s\,k(s)\,ds \;=\; 1 - \ln 2 + \ln\frac{1}{a\delta},$$

confirmed against quadrature to $10^{-12}$ and, independently, by the numerical growth rate: the
integral rises exactly linearly in $\ln(1/\delta)$ with slope 1. A further control: `mpmath` itself
refuses $\zeta(1)$, so the pole is asserted by the library rather than by the author.

---

## 4. And $p = 1$ is forced

**Theorem 3.** *The rapidity gap is linear in the lag, so the action pairs $K$ against $s^{1}$ and
against no other power.*

$-u\cdot u'/c^{2} = \cosh(w - w')$ depends only on the rapidity difference; for hyperbolic motion
$w(\tau) = |a|\tau/c$ exactly, so

$$\theta(\tau,\tau-s) \;=\; \frac{s}{c}\,|a|,
\qquad \frac{\partial\theta}{\partial s} = \frac{|a|}{c},
\qquad \frac{\partial^{2}\theta}{\partial s^{2}} = 0 ,$$

and for a general worldline the midpoint rule gives $\theta = (s/c)|a(\tau - s/2)| + O(s^{3})$ [3].
Hence $\Theta = (|a|/c)\int s K(s)\,ds$ and the only moment that appears is $M_{1}$.

**Combining Theorem 3 with Corollary 2.1: the one moment the framework requires is the one moment
the correlator does not have.**

---

## 5. The same integer forbids the $\sqrt{\pi}$

This is the part that turns a divergence into a structural statement, because it shows the
divergence and the missing irrationality are not two problems.

**Theorem 4 ($\pi$-parity of the moments).** *At integer $p$, $M_{p}$ has integer $\pi$-weight; a
half-integer $\pi$-weight occurs only at half-integer $p$.*

| $p$ | $M_{p}/a^{1-p}$ | $\pi$-weight |
|---|---|---|
| $0$ | $-1$ | $0$ |
| $2$ | $\pi^{2}/6$ | $2$ |
| $3$ | $\tfrac32\zeta(3)$ | $0$ |
| $4$ | $\pi^{4}/30$ | $4$ |
| $1/2$ | $\tfrac{\sqrt2}{2}\sqrt{\pi}\,\zeta(1/2)$ | $1/2$ |
| $3/2$ | $\tfrac{3\sqrt2}{8}\sqrt{\pi}\,\zeta(3/2)$ | $1/2$ |
| $5/2$ | $\tfrac{15\sqrt2}{32}\sqrt{\pi}\,\zeta(5/2)$ | $1/2$ |

The mechanism is transparent: $\Gamma(p{+}1)$ is rational at integer $p$ and carries $\sqrt{\pi}$ at
half-integer $p$, while $\zeta$(even) is a rational multiple of an even power of $\pi$ and
$\zeta$(odd) is $\pi$-free.

The target is
$$\xi \;\equiv\; M_{1}H_{\Lambda} \;=\; \frac{8\sqrt{6}\sqrt{\pi}}{9} \;=\; \frac{2^{7/2}\sqrt{\pi}}{3^{3/2}} \;=\; 3.85920669 ,
\qquad \xi^{2} = \frac{2^{7}\pi}{3^{3}} = 2\pi\left(\tfrac43\right)^{3},$$
of $\pi$-weight $+1/2$ exactly. **So the correlator could supply the target's $\sqrt{\pi}$ only at
$p = 1/2$ or $p = 3/2$, which §4 forbids.** The divergence and the missing $\sqrt{\pi}$ are one
fact: $p = 1$.

**This is a specific exclusion, not a blanket one.** Four prespecified decoy targets — $2/3$,
$\pi/6$, $\zeta(3)$, $\pi^{2}/16$ — all have integer $\pi$-weight and would therefore be reachable
by an integer-$p$ moment ratio. The machinery admits them and rejects the actual target. A test that
rejected everything would prove nothing.

---

## 6. The memory time: a two-pronged no-go

One might hope to sidestep §3 by asking not for $M_{1}$ but for the kernel's *correlation time*
$\tau_{c} = M_{1}/M_{0}$, which is free of the coupling. Both available schemes fail, in opposite
directions.

**Prong 1 — unsubtracted: no memory at all.** $M_{0}$ diverges as $1/\delta$ (a *power*) while
$M_{1}$ diverges only logarithmically, so

| $\delta$ | $M_{0}$ | $M_{1}$ | $\tau_{c}$ |
|---|---|---|---|
| $10^{-3}$ | $999.3$ | $7.571$ | $7.58\times10^{-3}$ |
| $10^{-6}$ | $10^{6}$ | $14.479$ | $1.45\times10^{-5}$ |
| $10^{-9}$ | $10^{9}$ | $21.387$ | $2.14\times10^{-8}$ |
| $10^{-12}$ | $10^{12}$ | $28.295$ | $2.83\times10^{-11}$ |

$\tau_{c} \to 0$. **The bare de Sitter correlator has zero memory** — it is UV-dominated, and a
UV-dominated kernel cannot supply a cosmological time.

**Prong 2 — Hadamard-subtracted: the infrared takes over.** Now $M_{0} = -a$ *exactly* (finite, and
it does carry the thermal scale, which is the encouraging part), but $M_{1}$ diverges in the
**infrared** as $-\ln(aS)$: the combination $M_{1}^{H} + \ln(aS)$ converges to $0.30685281944$ as
the IR cutoff runs over four decades. There is no scheme in which both moments are finite.

**One exact curiosity, reported because it is exact and not because it predicts anything.** Cutting
the logarithm at the horizon itself, $\delta = 1/H$, gives the dimensionless first moment **exactly
1** — the $\ln 2$ from $a = H/2$ cancels the $-\ln 2$ of the closed form. It is a clean coincidence
and it fixes no dimensionful number.

---

## 7. What the failure means, and two companion no-goes

### 7.1 $a_{0}$ is a renormalisation condition

$k$ has dimension $1/\text{time}^{2}$ while the action's $K$ has $1/\text{time}$, so $K = C\,k$ with
$[C] = \text{time}$, and $M_{1} = C \times (\text{dimensionless moment})$. Both $C$ and the
subtraction point are free. **This is precisely the structure the worldline realisation already
has** — $K = (N/\lambda)e^{-s/\lambda}$ with only the *product* $N\lambda = M_{1}$ fixed — and it
explains that structure rather than merely restating it: a free-field correlator cannot deliver
$M_{1}$, because the object is a logarithmically divergent moment, and the finite part of a
divergent moment is a renormalisation condition. **$a_{0}$ is the subtraction point of the theory.**

The mismatch is robust in the way logarithms are robust. Taking the subtraction at a UV scale:

| subtraction $\delta$ | implied $\hat M_{1}$ | ratio to the target $0.61421$ |
|---|---|---|
| Planck time | $141.48$ | $73.3$ |
| nuclear, $10^{-23}$ s | $94.81$ | $49.1$ |
| atomic, $10^{-16}$ s | $78.70$ | $40.8$ |
| one second | $41.85$ | $21.7$ |
| *required* | — | $6.92$ Gyr |

Forty-three decades of cutoff move the answer by a factor of 3.4 and never approach the target, and
the subtraction that *would* reproduce $a_{0}$ sits at $6.92$ Gyr — a cosmological time, not a
short-distance scale. So this is not a UV renormalisation at all.

**Stated against my own framing: §7.1 is not a kill.** Because $C$ is free, a Planck-scale
subtraction gives $\tau_{c} = 7.6\times10^{-42}$ s, which *passes* the ephemeris bound
$\lambda \le 39$ yr comfortably, at kernel weight $N = 2.8\times10^{59}$ — and $N$ is a free
coupling. Nothing in this table excludes anything. Nothing in it predicts anything either. **The
kill is Corollary 2.1 with Theorems 3 and 4, not the arithmetic of cutoffs.**

### 7.2 Companion no-go: the mode sum over the $SO(1,3)$ generators

The target's algebraic part is $(8/9)\sqrt{6}$, and $\sqrt{6} = \sqrt{\dim\mathfrak{so}(1,3)}$ —
verified from the $D_{2}$ root data (rank 2 plus 4 roots) and the $\mathfrak{su}(2)\oplus\mathfrak{su}(2)$
split, with $D = 4$ the **only** integer satisfying $D(D-1)/2 = 6$. That is suggestive. It does not
survive.

- **The $\sqrt{\pi}$ cannot be group-theoretic.** Every sphere volume
  $\mathrm{Vol}(S^{n-1}) = 2\pi^{n/2}/\Gamma(n/2)$ has *integer* $\pi$-weight for $n = 2,\dots,10$,
  because $\Gamma$ at half-integer argument returns the compensating $\sqrt{\pi}$; and
  $\mathrm{Vol}(SU(2)) = 2\pi^{2}$, $\mathrm{Vol}(SO(4)) = 2\pi^{4}$ are $\pi$-even. So the
  half-integer weight has exactly one address, the odd-dimensional momentum measure
  $(4\pi)^{-3/2}$, and no mode sum can reach it.
- **And $8/9$ is not selected.** Closing the canonical invariants of $\mathfrak{so}(1,3)$
  (dimension, rank, dual Coxeter number, adjoint Casimir, Weyl group order, positive-root count,
  and the $\mathfrak{su}(2)$ factor's dimension and Casimir) under ratios of products of at most two
  gives a menu of **33** distinct rationals, of which **30** are equally "nice-looking" and which
  contains all four prespecified decoys $9/8$, $4/3$, $3/4$, $16/9$. A prespecified entry carries
  $p = 0.030$. *This is more favourable than the "hundreds" I asserted before running it, and the
  correction is recorded rather than absorbed.*
- **Decisively, the Casimir is convention-dependent.** $C_{2}(\text{adjoint})$ is $4$ in the
  highest-root normalisation and $2$ in the spin normalisation — a factor of 2, which is exactly the
  size of the quantity such a derivation would be asked to explain.

The route dies, and the $\sqrt{6}$ is downgraded to a coincidence. What survives is only the
reduction $\kappa = Z/(3\xi)$ with $\xi = 2Z/3$.

### 7.3 Companion no-go, and a withdrawal against interest

A previous note of mine observed that $\kappa = \tfrac23\,(D-1)/D$ returns exactly $1/2$ at $D = 4$
with no fitted quantity, while hedging that this was not a proof. **The hedge was right and the form
is now withdrawn.** The framework's own $D$-dependence is derivable, and it is a different function.

Three ingredients, each computed rather than asserted:

1. **The $D$-dimensional Friedmann coefficient.** Building the FRW Einstein tensor in $D = 4,\dots,7$
   gives $G_{tt} = 3, 6, 10, 15\,H^{2}$, hence
   $H^{2} = 16\pi G_{D}\rho/((D-1)(D-2))$ — the standard $8\pi G\rho/3$ at $D = 4$. A control
   confirms the extractor rejects all three prespecified decoy coefficients. **So the target's
   $\sqrt{6}$ is Friedmann, not numerology.**
2. **$T_{dS} = H/2\pi$ in every dimension.** The static-patch function is $f(r) = 1 - H^{2}r^{2}$
   identically once $H^{2} = 2\Lambda/((D-1)(D-2))$, so the surface gravity is $H$ with no $D$ in
   it. Control: for Schwarzschild–de Sitter the surface gravity *is* $D$-dependent, so this is a
   property of pure de Sitter and not of the method.
3. **The memory factor is a worldline scalar.** The gap depends only on $\cosh(w-w')$ — no spatial
   index — so neither the $2/3$ nor the kernel shape can carry $D$; and
   $a_{0} = \tfrac23 c/M_{1}$ together with $a_{0} = cH_{\Lambda}/Z$ forces $\xi = 2Z/3$ uniquely.

Therefore

$$\kappa_{D} \;=\; \tfrac12\sqrt{\frac{6}{(D-1)(D-2)}} ,$$

which agrees with $\tfrac23(D-1)/D$ at $D = 4$ and nowhere else: the ratio is $1.000$, $1.509$,
$2.029$, $2.556$, $4.157$ at $D = 4,5,6,7,10$. And the single point cannot select a form — **five**
prespecified functions pass through exactly $1/2$ at $D = 4$: $2/D$, $\tfrac23(D-1)/D$,
$3/(2(D-1))$, the constant $\tfrac12$, and the derived one. The $D = 4$ *value* stands; the *form*
does not.

### 7.4 The residue

With $\sqrt{6}$ traced to Friedmann (§7.3) and $\sqrt{\pi}$ to the odd-dimensional momentum measure
(§7.2), the unexplained part of the target is a pure rational:

$$\xi^{2} = 2\pi\left(\tfrac43\right)^{3}
\quad\Longleftrightarrow\quad
M_{1} = \tfrac43\,t_{\Lambda},
\qquad \tfrac43 = 2\times\tfrac23 ,$$

and the $2/3$ is the derived memory-force renormalisation. **The entire residue is one factor of
2** — which is the same factor already banked as $Z^{2} = 4\,(8\pi/3)$. That part is a
re-presentation, not progress, and is labelled as such. The new ground is §§2–6 and 7.2–7.3.

---

## 8. What is not claimed

- **This does not derive $\kappa = \tfrac12$, and it is not a partial derivation.** It closes
  routes. $\kappa = \tfrac12$ remains **fitted**.
- **No claim is made regarding particle physics, the Standard Model, or unification.** The author
  publicly withdrew earlier statements of that kind and does not restate them. Nothing here is a
  theory of everything, and nothing here is evidence for one.
- **Theorem 4 is a statement about this class of moment integrals**, not a general theorem that
  $\sqrt{\pi}$ cannot arise in physics. It says the *de Sitter correlator's moments* cannot carry a
  half-integer $\pi$-weight at integer $p$. A different object with a different measure could.
- **The load-bearing structural step in §7.3 is an argument, not a computation.** That the kernel
  shape and the memory factor carry no $D$ follows from their being proper-time scalars; that is
  reasoning about the objects, not an evaluation of them.
- **The conclusion of §3 is, in one sense, standard QFT wearing a costume.** Any kernel with $1/s^{2}$
  short-distance behaviour has a logarithmically divergent first moment; that is the same logarithm
  that makes mass renormalisation necessary. A referee will not find the divergence surprising. What
  is new is *where it lands* — on the unique moment the action is permitted to use — and the
  $\pi$-parity tie in §5.
- **The interpolating function is not new.** $\nu = \sqrt{1+1/y}$ is Eq. (9) of [1].
- **Milgrom's own assessment of the vacuum program** is that an actual inertia-from-vacuum mechanism
  is still far off. This paper does not change that. It narrows it.

### What a referee should attack first

1. **The identification of $K$ with a vacuum autocorrelation.** This is the paper's one physical
   postulate. If $K$ is instead a *response* kernel, everything changes — but not favourably: for a
   free field the commutator $(1+n) - n = 1$ is exactly temperature-independent, so the retarded
   kernel carries no $H$ and could never have supplied a memory scale at all. The temperature must
   live in the noise kernel. That is verified as a control, and it closes the obvious alternative.
2. **The conformal coupling.** A minimally coupled massless scalar in de Sitter is infrared-pathological
   and was not used. Whether the physical kernel is conformally coupled is not established here.
3. **The midpoint rule.** $\theta = (s/c)|a(\tau-s/2)| + O(s^{3})$ is exact for hyperbolic motion
   and third order otherwise. A kernel with support at large $s$ probes that error.

---

## 9. Prior work

[1] M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A **253**, 273 (1999)
[arXiv:astro-ph/9805346]. **The closest prior art, and closer than expected.** Same physical
picture; the route goes through the *temperature*, not through a kernel moment, so it never
encounters $\zeta$'s pole. The interpolating function used here is his Eq. (9).

[2] M. Milgrom, *Dynamics with a non-standard inertia-acceleration relation*, Ann. Phys. **229**,
384 (1994). Modified-inertia theories are generically time-nonlocal. The memory-kernel framing is
his.

[3] C. P. Zimmerman, *A causal variational worldline action for modified inertia: the rapidity gap*,
Zenodo, DOI 10.5281/zenodo.21845411 (concept). Supplies the action, the equivalence
$\kappa = \tfrac12 \Leftrightarrow M_{1} = \tfrac43 t_{\Lambda}$, the memory force and the
$\tfrac23$.

[4] G. W. Gibbons and S. W. Hawking, *Cosmological event horizons, thermodynamics, and particle
creation*, Phys. Rev. D **15**, 2738 (1977).

[5] T. S. Bunch and P. C. W. Davies, Proc. R. Soc. Lond. A **360**, 117 (1978).

[6] H. Narnhofer, I. Peter and W. Thirring, Int. J. Mod. Phys. B **10**, 1507 (1996).

[7] S. Deser and O. Levin, *Accelerated detectors and temperature in (anti-) de Sitter spaces*,
Class. Quantum Grav. **14**, L163 (1997); see also T. Jacobson, arXiv:gr-qc/9709048. Source of the
$\sqrt{a^{2}+H^{2}}$ structure that [1] uses.

The Mellin transform of $\sinh^{-2}$, the KMS condition, $\mathfrak{so}(4) = \mathfrak{su}(2)\oplus\mathfrak{su}(2)$,
the $D_{2}$ root system, Macdonald's volume formula, $\mathrm{Vol}(S^{n-1}) = 2\pi^{n/2}/\Gamma(n/2)$,
$D$-dimensional FRW and Tangherlini's solution (Nuovo Cim. **27**, 636 (1963)) are all classical.

**A literature check was performed for this paper.** No prior work was found computing the moments
of the de Sitter worldline correlator, expressing them as $\Gamma(p{+}1)\zeta(p)$, or connecting
$p = 1$ to an acceleration scale. The absence is unsurprising: the question only exists once one
posits $M_{1} = c/a_{0}$, which is a relation of [3].

---

## 10. AI-assistance disclosure

Portions of the analysis, numerical verification and drafting were carried out with the assistance of
a large language model (Anthropic Claude). The author directed the work, specified and reviewed every
load-bearing calculation, and takes full responsibility including for any errors. No AI system
satisfies the criteria for authorship and none is listed as an author. Several intermediate claims
produced during the work were found to be incorrect and were withdrawn before this deposit — among
them the "hundreds of rationals" figure corrected in §7.2 and the $\tfrac23(D-1)/D$ form withdrawn
in §7.3.

## 11. Reproducibility

Every quantitative claim above is produced by a committed script that exits non-zero if any internal
consistency check fails, and each carries negative controls that must trip. The three scripts are
included in this deposit:

- `mi_wightman_first_moment_2026.py` — §§2–6, 30/30 checks.
- `mi_lorentz_mode_sum_2026.py` — §7.2, 23/23 checks.
- `mi_kappa_D_dependence_rigidity_2026.py` — §7.3, 23/23 checks.

Both footings are carried on every dimensionful number.
