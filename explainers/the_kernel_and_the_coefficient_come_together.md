# The de Sitter–Unruh mechanism forces an interpolation function and an acceleration scale together

### The shape is forced unconditionally, the coefficient is locked to one ambient scale — and the α = 1 → α = 2 switch left the derived family altogether

*Revised 2 August 2026 (same day). §4 of the first draft claimed the kernel and the coefficient are an
"inseparable package." **That was too strong and is corrected in §4a below:** the kernel shape is independent
of the ambient acceleration, so the framework keeps its derived kernel at any $a_0$. The 11.58× gap is
unchanged in size; what changes is where it lives.*

**C. P. Zimmerman**, Briar Creek Tech
Draft, 2 August 2026. Companion scripts: `reviews/mi_dsunruh_kernel_package_2026.py` (7/7) and
`reviews/mi_dsunruh_freedom_audit_2026.py` (7/7), both exit 0.

---

## Abstract

A uniformly accelerated observer in de Sitter space sees a thermal bath at temperature
$T(a) \propto \sqrt{a^2 + a_{\rm dS}^2}$ with $a_{\rm dS} = cH_\Lambda$. If inertia tracks the *excess* of
that temperature over the ambient Gibbons–Hawking value, the resulting effective-mass ratio is

$$\mu_{\rm dS}(u) \;=\; \frac{\sqrt{1+u^2}-1}{u}, \qquad u = a/a_{\rm dS}.$$

We record two facts and one consequence. **First**, $\mu_{\rm dS}$ is *identically* the interpolation
function of the law $g_{\rm obs}^2 = g_{\rm bar}^2 + g_{\rm bar}a_0$ — the α = 1 kernel — once one sets
$a_0 = 2a_{\rm dS}$. The symbolic residual is exactly zero. **Second**, that same substitution is not
optional: the deep-regime slope of $\mu_{\rm dS}$ is $u/2$, which *forces* $a_0 = 2A$ for whatever ambient acceleration $A$ enters the temperature. Neither
fact is new — both are Milgrom's (1999) — but their **conjunction** has not been stated, and it sharpens the
problem considerably.

**Crucially, the shape does not depend on $A$.** Written in units of $a_0 = 2A$, $\mu$ is
$(\sqrt{1+4x^2}-1)/2x$ for *every* ambient scale, with $A$ absent from the expression. And among power-law
responses $f(T) = T^n$, deep-MOND linearity forces $n = 1$ **uniquely** ($n=2$ gives a constant $\mu$ — no
MOND regime at all; $n \geq 3$ diverges as $a \to 0$). So the mechanism fixes the *shape* unconditionally and
the *relation* $a_0 = 2A$, but **not $A$ itself.** Milgrom supplies $A$ from the de Sitter horizon; that is a
physical choice, not an algebraic necessity.

**So the framework's $\kappa = 1/2$ is exactly one statement:** the ambient acceleration a bound system
samples is $A = \tfrac14 c\sqrt{G\rho_\Lambda} = cH_\Lambda/11.58$, not the horizon scale $cH_\Lambda$. The
kernel then comes along free. That is a well-posed physics question rather than a bare postulate — which is
progress in clarity, though not yet in physics: nothing here supplies the argument for that $A$.

The consequence we had not priced: the α = 1 → α = 2 kernel switch, made in July 2026 for
solar-system reasons, **forfeits the derivation of the kernel as well**, because $\mu_2(x) = x/\sqrt{1+x^2}$
is not $\mu_{\rm dS}$ (they differ by 14.4% at $x = 1$). Under α = 2 the framework holds neither half of the
package. We also withdraw a claim made three days ago that de Sitter thermality *derives*
$a_0 = cH_\Lambda/2\pi$; it disagrees with the construction above by exactly $4\pi$, and the construction
above is the correct reading.

---

## 1. What is claimed, and what is not

**Claimed.** (i) The de Sitter–Unruh construction yields the α = 1 interpolation function exactly, and does
so for *every* ambient acceleration $A$ — so the framework's kernel is derived unconditionally (§4a).
(ii) The same algebra locks $a_0 = 2A$, and no power-law response law can move that lock (§4b) — so the
framework's $\kappa = 1/2$ reduces to the single claim $A = \tfrac14 c\sqrt{G\rho_\Lambda}$, which is
11.58× below the horizon scale Milgrom uses. (iii) The α = 1 → α = 2 switch puts the kernel now in force
*outside* the derived family entirely, which is a cost absent from our own accounting of that switch.

**Corrected from the first draft, same day.** We claimed the kernel and coefficient are an "inseparable
package" and that the framework cannot hold both. §4a shows it can: the shape is $A$-independent. The 11.58×
gap does not shrink, but it is one unexplained ambient scale rather than a conflict between two claims.

**Not claimed.** We do not claim to derive $a_0$. We do not claim novelty for the construction, for
$\mu_{\rm dS}$, or for $a_0 = 2cH_\Lambda$ — all three are Milgrom's. We claim novelty only for the
$A$-independence of the shape, the $n=1$ uniqueness, the reduction of $\kappa = 1/2$ to a statement about
$A$, and the α = 2 cost. And nothing here improves any fit. **Restating a postulate as a different postulate
is progress in clarity only**; it becomes physics if and only if someone derives $A$ from bound-system
kinematics.

---

## 2. The temperature (prior art, stated first)

For a detector on a worldline of constant proper acceleration $a$ in de Sitter space, the response is
thermal at

$$T(a) \;=\; \frac{\hbar}{2\pi c k_B}\sqrt{a^2 + a_{\rm dS}^2}, \qquad a_{\rm dS} = cH_\Lambda ,$$

reducing to the Gibbons–Hawking value $T_{\rm GH} = \hbar H_\Lambda/2\pi k_B$ at $a = 0$. This is Narnhofer,
Peter & Thirring (1996) and Deser & Levin (1997); Milgrom states the MOND-relevant reading of it in his own
pedagogical review, noting that the *excess* temperature behaves "exactly as MOND inertia should."

The excess an accelerated observer sees over what an inertial one already sees is

$$\Delta T(a) \;\propto\; \sqrt{a^2 + a_{\rm dS}^2} \;-\; a_{\rm dS}. \tag{1}$$

**Note where the constants sit.** The $2\pi$ and the $\hbar$ are a *common prefactor*. They cancel out of any
ratio built from (1). This is the single most important bookkeeping fact in this note, and §7 is where it
bites.

---

## 3. The interpolation function, and the identity

Take inertia proportional to the excess: $m_{\rm eff}/m \propto \Delta T(a)/a$. Then

$$\mu_{\rm dS}(u) = \frac{\sqrt{1+u^2}-1}{u}, \qquad u = \frac{a}{a_{\rm dS}},$$

which interpolates correctly: $\mu_{\rm dS} \to 1$ as $u \to \infty$ (Newtonian) and $\mu_{\rm dS} \to u/2$
as $u \to 0$ (deep MOND). Now set $a_0 = 2a_{\rm dS}$, so that $u = 2x$ with $x = a/a_0$:

$$\mu_{\rm dS} = \frac{\sqrt{1+4x^2}-1}{2x} \;=\; \mu_1(x),$$

and $\mu_1$ is precisely the interpolation function of

$$g_{\rm obs}^2 = g_{\rm bar}^2 + g_{\rm bar}\,a_0 . \tag{2}$$

The symbolic residual $\mu_{\rm dS} - \mu_1$ is **zero identically** (verified in `D2a`), and $\mu_1$
reproduces (2) exactly (`D2b`), so this is a statement about our published law and not a paraphrase of it.

**Credit, plainly.** Equation (2)'s kernel is algebraically Milgrom (1999), Phys. Lett. A **253**, 273,
Eq. (9). Our corpus already carries that credit line. What §3 adds is only that the same paper's de
Sitter–Unruh argument is where that kernel *comes from*.

---

## 4. The coefficient is locked to the ambient scale — but the ambient scale is not locked

The substitution $a_0 = 2a_{\rm dS}$ in §3 was not a convenience. The deep-regime limit of $\mu_{\rm dS}$ is
$u/2$; matching that to $\mu_1 \to x$ requires $u = 2x$, hence

$$\boxed{\,a_0 = 2A\,}$$

for whatever ambient acceleration $A$ appears in $\sqrt{a^2+A^2}$. And that $1/2$ in the deep slope is the
Taylor coefficient of the square root, so **no reshaping of the response can move it** — see §4b.

### 4a. The correction: the shape is $A$-independent

Write $\mu$ in units of $a_0 = 2A$, i.e. $a = 2Ax$:

$$\mu = \frac{\sqrt{4A^2x^2 + A^2} - A}{2Ax} = \frac{\sqrt{1+4x^2}-1}{2x},$$

and $A$ has **cancelled entirely**. The α = 1 shape is what the mechanism gives for *every* ambient scale.
Our first draft's claim that the kernel and coefficient are "inseparable," and that the framework "cannot
hold the kernel derivation and the coefficient at the same time," was therefore wrong. **It can.** What it
owes is not a different kernel but an argument for $A = \tfrac14 c\sqrt{G\rho_\Lambda}$ — one unexplained
ambient scale, with the kernel supplied free.

### 4b. Why the response law cannot help either

Generalise "inertia tracks the excess temperature" to "inertia tracks the excess in $f(T) = T^n$," normalised
by the flat-space Unruh value at the same acceleration. With $T/T_0 = \sqrt{1+v^2}$ and $T_U/T_0 = v$:

$$\mu_n(v) = \frac{(1+v^2)^{n/2}-1}{v^n} \;\longrightarrow\; \frac{n}{2}\,v^{\,2-n} \quad (v \to 0).$$

Deep-MOND linearity requires $2-n = 1$, so **$n = 1$ uniquely**. At $n=2$ the ratio tends to a constant —
Newtonian everywhere, no MOND regime. At $n \geq 3$ it diverges as $a\to0$. Two further variants fail the
same way: $\sqrt{T^2-T_0^2}/T_U \equiv 1$ identically (pure Newton), and a logarithmic response gives
$v^2/\log v$, which is not linear and yields neither flat rotation curves nor the baryonic Tully–Fisher
relation. **The coefficient cannot be bought by changing the response law; only a different $A$ moves it.**

---

## 5. Where our coefficient sits — in the clean form

Write $a_0 = cH_\Lambda/Z$. The framework uses

$$Z_{\rm fw} \;=\; 2\sqrt{\tfrac{8\pi}{3}} \;=\; 5.78881 ,$$

which is *identical* to $\sqrt{32\pi/3}$ but written so the content is visible: $\sqrt{8\pi/3} = 2.894405$ is
the $\kappa = 1$ reference point, and the framework sits exactly **one factor of 2** away from it — that
factor is $\kappa = 1/2$, and it is the whole of the distinctive claim. Meanwhile the mechanism of §4 gives
$Z_{\rm dS} = 1/2$. The gap is

$$\frac{Z_{\rm fw}}{Z_{\rm dS}} \;=\; 4\sqrt{\tfrac{8\pi}{3}} \;=\; 11.5776 .$$

(The framework's $a_0$ is *smaller* than the mechanism's by that factor.) The 11.58 was already stated in
`A0_HALF_THE_DARK_ENERGY_RATE`; §4 is what makes it expensive rather than merely noted. One curiosity, offered
as arithmetic and not as meaning: $\kappa_{\rm dS} = 2\sqrt{8\pi/3}$ is numerically the same as $Z_{\rm fw}$,
because $\kappa = \sqrt{8\pi/3}/Z$ and $Z_{\rm dS} = 1/2$. It signifies nothing.

---

## 6. The cost of the α = 1 → α = 2 switch — the new result

In July 2026 the framework moved from $\mu_1$ to $\mu_2(x) = x/\sqrt{1+x^2}$, because the exact form (2)
forces a constant $a_0/2$ sunward anomaly at 1279× the Earth ephemeris bound. That switch was priced at
**+0.0033 dex on 175 SPARC rotation curves** plus the solar-system relief. Both figures stand.

What was not priced: $\mu_2 \neq \mu_{\rm dS}$. They differ by 0.0891 at $x = 1$ — $\mu_1(1) = 0.618034$
against $\mu_2(1) = 0.707107$, a **14.4%** discrepancy. So the switch also **forfeits the de Sitter–Unruh
derivation of the kernel**. The honest ledger:

| | kernel derived from the mechanism? | solar system |
|---|---|---|
| **α = 1** | **yes**, exactly (§3) | fails at 1279× the Earth bound; post-EFE = bare |
| **α = 2** | **no** (14.4% off at $x=1$) | fails at 6.2–12.4× the Mars budget |

Neither kernel is free, and under the kernel now in force the framework has **neither** the derivation nor a
viable solar system. That trade is now explicit; it was not before.

**And §4a/§4b make this worse, not better.** Since the α = 1 shape is forced for *every* ambient scale and
*every* viable response law, $\mu_2$ does not sit at some other point inside the derived family — it lies
**outside the family altogether.** So the solar-system liability cannot be repaired by rescaling or reshaping
within the mechanism. Any fix — screening, a frequency gate, or the exponential tail — must come from outside
it, and pays the kernel derivation as its price.

---

## 7. A withdrawal

Three days ago we claimed that de Sitter thermality *derives* $a_0 = cH_\Lambda/2\pi$, i.e.
$\kappa = \sqrt{2/(3\pi)} = 0.4607$, by identifying the kernel's dimensionless frequency
$w = \omega c/a_0$ with the de Sitter thermal variable $x_{\rm th} = 2\pi\omega/H_\Lambda$.

**That is withdrawn.** It disagrees with §4 by exactly $4\pi = 12.57$, and §4 is correct. The reason is §2's
bookkeeping note: the $2\pi$ lives in a common prefactor of $T(a)$ and cancels out of $\mu$, so a turnover
condition on the *acceleration* carries no $2\pi$. Our reading instead converted a temperature into a
frequency, which introduces a $2\pi$ that the physics does not. The sentence "the de Sitter tie derives
$\kappa = \sqrt{2/(3\pi)}$" should not be repeated.

**What survives that swing**, unaffected, because both results are arithmetic about $Z$ and independent of
which identification one uses:

1. $Z^2/\pi = 32/3$ is rational while $Z/\pi^k$ is irrational for every integer $k$. So ingredients that are
   rational multiples of integer powers of $\pi$ can force $Z^2$ but never $Z$.
2. Being simultaneously quadratic in $Z$, $\hbar$-free, and carrying the Bekenstein–Hawking $1/4$ is
   impossible: $a_0$ is $\hbar$-free, the $1/4$ rides $S \sim \hbar^{-1}$ and survives only un-ratioed, and
   the only $\hbar^{+1}$ available to cancel it is a temperature — which is a frequency scale, returning one
   to the class barred by (1).

Indeed the withdrawal *sharpens* those results: the mechanism's actual output, $Z = 1/2$, is a rational
number, squarely inside the class those theorems say cannot reach $Z = 2\sqrt{8\pi/3}$.

---

## 8. Observational status

The two coefficients are not observationally equivalent, but the discrimination is modest and it favours us.
Profiling $a_0$ on 175 SPARC galaxies with the stellar mass-to-light ratio free **per galaxy** — so that any
global population-synthesis offset is absorbed — gives $\sigma(a_0)/a_0 = 1.24\%$ treating points as
independent and 5.44% with within-galaxy clustering. Against $\kappa = 1/2$ the fit gives $\Delta\chi^2 =
63.9$; against Milgrom's (2020) empirical $\kappa = 1/2\pi$, $154.3$ — favouring $\kappa = 1/2$ at roughly
2.2σ on the conservative counting.

Stated against interest: both sit *low* of the free best fit $a_0 = 1.077\times10^{-10}\,{\rm m\,s^{-2}}$,
and the alternative footing $\rho_{\rm tot}/cH_0 = 1.13\times10^{-10}$ fits better than the canonical one
($\Delta\chi^2 = 7.0$). And the mechanism's $2cH_\Lambda$ is excluded by these data by a wide margin — which
is the long-standing problem with the derivation, not with the framework.

So: **theory naturalness points away from $\kappa = 1/2$; the data point toward it.** Neither is decisive.

---

## 9. What would resolve it

One thing, now stated exactly: **a derivation of the ambient acceleration $A$ that a bound system samples,
giving $A = \tfrac14 c\sqrt{G\rho_\Lambda}$ rather than $cH_\Lambda$.** Per §4b the response law cannot
supply it and per §4a the kernel does not constrain it, so this is the entire remaining question — and it is
the *only* one. Physically it asks whether a star on a bound galactic orbit samples the horizon's surface
gravity or something 11.58× smaller.

Two prior no-go results apply to it unchanged and should temper expectations: ingredients that are rational
multiples of integer powers of $\pi$ can force $Z^2$ but never $Z = 2\sqrt{8\pi/3}$; and being at once
quadratic in $Z$, $\hbar$-free, and carrying the Bekenstein–Hawking $1/4$ is impossible. Failing such a
derivation, the coefficient remains what our own coefficient paper calls it: **fitted, not derived** — but
now demonstrably fitted *alongside a kernel that is derived*, which is a better position than §6 alone
suggests, and a worse one than §4a alone suggests.

---

## 10. Reproducibility

Every number above is produced by `reviews/mi_dsunruh_kernel_package_2026.py` (7 checks, exit 0, no
`check(True)`), which computes $\mu_{\rm dS}$ symbolically, tests the identity against the published form of
(2), derives the forced coefficient, evaluates the α = 2 discrepancy, and quantifies the withdrawal. The §8
likelihood is `real_research/reviews/mi_a0_profile_likelihood_sparc_2026.py`; the α = 2 solar-system standing
is `real_research/reviews/mi_alpha2_sun_reflex_2026.py`; the two no-go results of §7 are
`reviews/mi_kernel_measure_from_desitter_2026.py` and `reviews/mi_quadratic_z_escape_2026.py`.

## References

- Narnhofer, Peter & Thirring (1996), *Int. J. Mod. Phys. B* **10**, 1507 — thermalisation for accelerated
  observers in de Sitter space.
- Deser & Levin (1997), *Class. Quantum Grav.* **14**, L163 — $T \propto \sqrt{a^2 + a_{\rm dS}^2}$.
- Milgrom (1999), *Phys. Lett. A* **253**, 273 — the de Sitter–Unruh argument, $a_0 = 2cH_\Lambda$, and the
  interpolation function of Eq. (9), which is the kernel of (2).
- Milgrom, *MOND — A Pedagogical Review* — states the excess-temperature reading of the mechanism.
- Milgrom (2020) — the empirical $a_0 = cH_\Lambda/2\pi$.
- Gibbons & Hawking (1977), *Phys. Rev. D* **15**, 2738 — $T_{\rm GH}$.

---

*One-paragraph summary for the impatient (revised). The de Sitter horizon's temperature formula, applied to inertia,
hands you a MOND interpolation function and an acceleration scale in the same breath. The function it hands
you is exactly the one our framework used until last month — and, it turns out, it hands you that same
function whatever ambient acceleration you feed it. So the kernel is ours for free. What the mechanism will
not give us is the scale: it says $a_0 = 2A$, and no choice of response law changes that. Our $\kappa = 1/2$
therefore says one specific thing — that a star on a bound orbit samples an ambient acceleration 11.58×
smaller than the horizon's. That is a real question someone could answer, which is better than a bare
postulate, though it is not yet an answer. Two things cut the other way: the kernel we actually switched to in
July, to survive the solar system, is outside this family altogether; and a derivation we announced three days
ago was wrong by 4π and is withdrawn here.*
