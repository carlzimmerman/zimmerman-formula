# One Number: the de Sitter–Unruh Inertia Class Reduces the MOND Coefficient to a Single Ratio and Cannot Fix It

**Carl P. Zimmerman** — Briar Creek Tech

*Draft, 2026-08-07. Every equation, identity and number below is reproduced by the self-checking script
`real_research/reviews/mi_r_one_parameter_nogo_paper_2026.py` (41/41 checks, exit 0), which prints `[OK]`/`[FAIL]`
per check and exits non-zero on any failure. See §8.*

---

## Abstract

Milgrom (1999) showed that a modified-inertia law built from the local de Sitter–Unruh temperature
$T(a) = \sqrt{a^2+c^2H_\Lambda^2}/2\pi$ reproduces MOND, fixed its scale at $\hat a_0 = 2cH_\Lambda$, and in 2008
remarked that the mismatch with the measured coefficient "isn't necessarily meaningful." We make that remark
quantitative and then close the route it suggests. **(1)** For any $I(a) = f(T(a)) - f(T_{\rm GH})$ the MOND
crossover is $q \equiv a_0/cH_\Lambda = 2c_1^\infty/f'(T_{\rm GH}) = 2/r$, invariant under
$f \to \alpha f + b$: the class's entire functional freedom collapses to one dimensionless ratio $r$, the slope of
$f$ at the horizon floor over its slope at infinity. **(2)** $g_{\rm obs}^2 = g_{\rm bar}^2 + a_0g_{\rm bar}$ is
*identically* Milgrom's five-acceleration balance with floor $k = a_0/2$, so $a_0 = 2k$ always and every
coefficient proposal is a choice of floor. **(3)** For **every** $r>0$ we exhibit in closed form an admissible
member whose inertia function is *exactly* that balance:
$f_r(T) = \sqrt{4\pi^2(T^2-T_{\rm GH}^2)+k^2} - k$, $k = cH_\Lambda/r$; admissibility is analytic and
unconditional. Hence $\sup r = +\infty$, both live coefficient proposals are admissible, and — since the kernel is
$\nu(y)=\sqrt{1+1/y}$ at every $r$ — **no rotation-curve shape measurement can ever fix the coefficient inside
this class.** A previously reported seven-shape admissibility ceiling excluding both proposals is withdrawn; the
correct single-scale ceiling is exactly $r=9$, a property of that menu and not of admissibility. **(4)** Every
member has a constant residual acceleration $\Delta = cH_\Lambda(1-\lambda\Phi_\infty)$, with $\mu\le1$
*equivalent* to $\Delta \ge 0$; on the balance member $\Delta = a_0/2$ exactly, which the Earth ephemeris bound
exceeds by $1279\times$. The coefficient's only handle is the floor, read in the solar system or in its redshift
dependence — not in galaxies. **$\kappa = 1/2$ is FITTED, not derived; Theorem 3 makes it less derivable, not
more.**

---

## 1. The class, and what is not ours

The interpolating function $\nu(y) = \sqrt{1+1/y}$, $y \equiv g_{\rm bar}/a_0$, and the balance
$I(a) = \sqrt{a^2+H^2}-H$ from which it follows, are **Milgrom (1999), eqs. 6–9**, who fixes
$\hat a_0 = 2cH_\Lambda$; **eqs. 10–11** there give a second functional with a different coefficient. The
temperature $T = \sqrt{a^2+\Lambda c^2/3}\,/2\pi$ of an accelerated de Sitter detector is **Narnhofer, Peter &
Thirring (1996)**; the five-acceleration reading is **Deser & Levin (1997)**; $a_\lambda = c^2\sqrt{\Lambda/3}$ is
**Milgrom (1994)**. **Milgrom (2008), §7.3.1** states that a coefficient mismatch "isn't necessarily meaningful …
would just point to a different effective $\mu(x)$." None of the *form* is available to claim; only the
dimensionless $\mathcal{O}(1)$ coefficient is open, and that is this paper's subject.

Write $H \equiv cH_\Lambda = 5.4194\times10^{-10}\ \mathrm{m\,s^{-2}}$, $T_{\rm GH} = H/2\pi$, and take

$$I(a) \;=\; f\!\left(T(a)\right) - f(T_{\rm GH}), \qquad T(a) = \frac{\sqrt{a^2+H^2}}{2\pi},$$

with $f$ increasing and asymptotically linear, $c_1^\infty \equiv \lim_{T\to\infty} f(T)/T$. The equation of
motion is $I(a) = g_{\rm bar}$, normalised so $I \to a$ at large $a$. This is *modified inertia*: the
gravitational field is unmodified and the response to it is not. Two footings are carried on every dimensional
number: canonical ($\rho_{\rm DE}$ with $cH_\Lambda$, $a_0 = 9.3614\times10^{-11}\ \mathrm{m\,s^{-2}}$) and
alternative ($\rho_{\rm total}$ with $cH_0$, larger by $1/\sqrt{\Omega_\Lambda} = 1.2082$,
$1.13\times10^{-10}$). Because $r$ is a *ratio* it is identical on both, so no conclusion depends on the fork.

## 2. Theorem 1 — the reduction

**Theorem 1.** $\displaystyle q \equiv \frac{a_0}{cH_\Lambda} \;=\; \frac{2\,c_1^\infty}{f'(T_{\rm GH})}
\;=\; \frac{2}{r}, \qquad r \equiv \frac{f'(T_{\rm GH})}{c_1^\infty},$ and $q$ is invariant under
$f \to \alpha f + b$ for any $\alpha > 0$, $b$.

*Proof.* Exactly, with no expansion, $T(a)^2 - T_{\rm GH}^2 = a^2/4\pi^2$; hence
$T - T_{\rm GH} = a^2/(4\pi H) + \mathcal{O}(a^4)$ and

$$c_2 \equiv \lim_{a\to0}\frac{I}{a^2} = \frac{f'(T_{\rm GH})}{4\pi H}.$$

At large $a$, $T \to a/2\pi$, so $c_1 \equiv \lim_{a\to\infty} I/a = c_1^\infty/2\pi$. The MOND crossover of the
law $I = c_1 a$ (Newtonian) versus $I = c_2 a^2$ (deep) is at $a_0 = c_1/c_2$, giving
$q = 2c_1^\infty/f'(T_{\rm GH})$. Invariance: $b$ cancels in $f(T)-f(T_{\rm GH})$; $\alpha$ scales $c_1$ and
$c_2$ alike and cancels in the ratio. $\square$

Note that $c_2$ reads $f'$ **at the floor** while $c_1$ reads $f$'s slope **at infinity**: different points on
$f$, connected by nothing — which is why an earlier claim in this corpus that the two MOND limits *force* $f$
linear, hence $r=1$, was a non-sequitur and has been withdrawn. Theorem 1 says the class has exactly **one**
physical parameter; all of $f$'s remaining freedom goes into the interpolation shape and never touches the
coefficient.

## 3. Theorem 2 — the coefficient is a floor, and the bookkeeping

**Theorem 2.** $g_{\rm obs}^2 = g_{\rm bar}^2 + a_0 g_{\rm bar}$ is identically
$g_{\rm bar} = \sqrt{g_{\rm obs}^2 + k^2} - k$ with $k = a_0/2$. Hence $a_0 = 2k$ *always*, and the entire
distinctive content of any coefficient proposal is the value of the floor.

*Proof.* Substitute and expand; the residual vanishes identically. The negative control $k = a_0$ leaves
$a_0(\sqrt{a_0^2+g_{\rm obs}^2} - a_0) \ne 0$. $\square$

Since $a_0 = \kappa\,c\sqrt{G\rho_\Lambda}$ and $cH_\Lambda = \sqrt{8\pi/3}\;c\sqrt{G\rho_\Lambda}$, one has
exactly $q = 2\kappa/Z$ and

$$\boxed{\,r \;=\; Z/\kappa\,}, \qquad Z \equiv 2\sqrt{8\pi/3} = 5.7888100366 .$$

| coefficient proposal | $r$ | $q = 2/r$ | $a_0$ canon | $a_0$ ALT | floor $k=a_0/2$ canon |
|---|---|---|---|---|---|
| Milgrom (1999) eqs. 6–9, $f=T$ | $1$ | $2$ | $1.084\times10^{-9}$ | $1.310\times10^{-9}$ | $5.419\times10^{-10}$ |
| Milgrom (1999) eqs. 10–11 | $2$ | $1$ | $5.419\times10^{-10}$ | $6.549\times10^{-10}$ | $2.710\times10^{-10}$ |
| conventional $2\pi a_0 = cH_\Lambda$ | $4\pi = 12.566371$ | $1/2\pi$ | $8.625\times10^{-11}$ | $1.042\times10^{-10}$ | $4.313\times10^{-11}$ |
| **this framework, $\kappa=\tfrac12$ (FITTED)** | $2Z = 8\sqrt{6\pi}/3 = 11.577620$ | $1/Z$ | $9.362\times10^{-11}$ | $1.131\times10^{-10}$ | $4.681\times10^{-11}$ |

Both $r = 4\pi$ and $r = 2Z = 4/\sqrt{8\pi/3}$ are *exact*, not decimal coincidences: the first is what a
horizon-area or solid-angle normalisation naturally supplies, the second is $4$ over the root of the Friedmann
factor. The two live proposals differ by **8.54 % in $r$**, i.e. **7.87 % in $a_0$** — so no variational bound of
realistic precision could ever separate them; any derivation must be exact. Against this framework's interest:
of the two, $4\pi$ is the one with an obvious candidate mechanism.

**A normalisation caveat travels with the table.** The value quoted in this corpus as "Milgrom 2020,
$\kappa = 1/2\pi$" means $a_0 = cH_\Lambda/2\pi$, i.e. $q = 1/2\pi$, $r = 4\pi$ — a $\kappa$ normalised against
$cH_\Lambda$, *not* the framework's, which is normalised against $c\sqrt{G\rho_\Lambda}$. Read in the framework's
normalisation, $1/2\pi$ would mean $r = 2\pi Z = 36.372$ and $a_0 = 2.98\times10^{-11}$: exactly $\pi$ below
canonical and exactly $Z/2 = 2.8944$ below the intended proposal, a displacement no SPARC fit tolerates. In the
framework's units the $r=4\pi$ proposal is $\kappa = Z/4\pi = 0.4607$.

## 4. Theorem 3 — a closed-form member at every coefficient

**Theorem 3.** For every $k>0$, put $r = H/k$ and

$$f_r(T) \;=\; \sqrt{4\pi^2\!\left(T^2 - T_{\rm GH}^2\right) + k^2} \;-\; k .$$

Then $f_r$ is real-analytic on a neighbourhood of $[T_{\rm GH},\infty)$, strictly increasing, strictly concave
for $r>1$, asymptotically linear with $c_1^\infty = 2\pi$, and

$$I_r(a) \;=\; f_r(T(a)) - f_r(T_{\rm GH}) \;=\; \sqrt{a^2+k^2}\;-\;k \quad\text{exactly},$$

with $f_r'(T_{\rm GH}) = 2\pi/k$, hence $r = f_r'(T_{\rm GH})/c_1^\infty = H/k$ and $a_0 = 2k$. At $k=H$ it
degenerates to $f_1 = 2\pi T - H$, i.e. to Milgrom's linear $f=T$ up to the affine freedom of Theorem 1.

*Proof.* Because $a^2 = 4\pi^2(T^2-T_{\rm GH}^2)$ identically, the substitution is exact; the rest is
differentiation. Verified symbolically for arbitrary $k$. $\square$

**Admissibility is analytic and unconditional.** With $\mu \equiv g_{\rm bar}/g_{\rm obs}$,

$$\frac{d\mu}{dg_{\rm obs}} \;=\; \frac{k\left(\sqrt{g_{\rm obs}^2+k^2}-k\right)}
{g_{\rm obs}^2\sqrt{g_{\rm obs}^2+k^2}} \;>\;0 \quad\text{for every } k>0,
\qquad \mu \to 1^- ,$$

so $\mu \le 1$ *and* $\mu$ monotone hold at every $r$, with no shape freedom used and no numerics.

**Corollary 3.1 (unboundedness).** $\sup r = +\infty$. In particular $r = 2Z$ ($\kappa = 1/2$) and $r = 4\pi$ are
both admissible. This is proved in one line by an exhibit that is not contrived: it is the framework's own law.

**Corollary 3.2 (the RAR is exactly blind to the coefficient).** Putting $g_{\rm bar} = a_0y$ into the balance
gives $\nu(y) = \sqrt{1+1/y}$ *with no residual $k$-dependence*: two members whose $a_0$ differ by a factor 67
have kernels agreeing to $1.9\times10^{-16}$ dex across $y\in[10^{-4},10^{4}]$, against SPARC's $0.034$ dex
marginalised intrinsic scatter. **No rotation-curve shape measurement can constrain the coefficient inside this
class.** This is the structural reason the SPARC radial-acceleration relation is non-diagnostic of any particular
$a_0$, and it sharpens Milgrom (2008) §7.3.1 in a direction he did not state: a coefficient mismatch need not
point to a different effective $\mu(x)$ at all — it can be the *same* $\mu(x)$ with a different $f$.

**Corollary 3.3.** $r=1$ is the *unique* member with $f$ linear in the temperature; every other coefficient needs
a concave $f$ whose slope falls from $2\pi/k$ at the floor to $2\pi$ at infinity — and $r$ *is* that ratio.

## 5. Admissibility does not bound $r$ — scope, and a withdrawal

Put $s = T-T_{\rm GH}$, $x = s/T_{\rm GH}$, $F' = c_1^\infty[1+\lambda\psi]$ with $\lambda = r-1$, $\psi(0)=1$,
$\psi$ non-increasing to $0$, and $\Phi(x) = \int_0^x\psi$. Then $\mu \le 1$ is $\lambda\Phi_\infty \le 1$ and
$\mu' \ge 0$ is $\lambda J(x) \le 1$ with $J = (1+1/x)\Phi - (x+2)\psi$; the first is the $x\to\infty$ limit of
the second, so only monotonicity ever binds.

A previous script in this corpus scanned seven single-scale transition shapes $\times$ 220 scales, found a maximum
admissible $r = 9.016763$, and concluded that $r=2Z$ and $r=4\pi$ are both inadmissible. **That conclusion is
withdrawn**, by Theorem 3 above and independently by a linear-programming solution of the same minimax problem
(`mi_psi_search_r2Z_2026.py`, 27/27). Two corrections belong in the record. (i) The exact ceiling of the best menu
shape $\psi = (1+x/\delta)^{-2}$ is $\lambda_{\max}(\delta) = 4(2-\delta)^2/(2+7\delta-4\delta^2)$, so
$r_{\max} = 9$ **exactly** as $\delta \to 0$, attained only in the limit; $9.016763$ was a $0.19\,\%$ quadrature
bias. (ii) *Seven shapes is not a proof* — the original script said so itself, and that is what happened.

What survives is a statement about the *shape scale*, not the coefficient: within the sharp family
(same script, §H) $r \le 1 + 2/(x_1 + \sqrt{x_1(x_1+2)})$ with $x_1$ the plateau length, i.e. $a_0$ cannot lie far
below the acceleration at which the kernel leaves its floor. Since $9 < 2Z < 4\pi$, both live coefficients require
a $\psi$ carrying a *second* scale, with the inner one near $a_0$. Recorded against interest: a coefficient that
enters through a tuned shape scale is a coefficient that has been fitted.

## 6. Theorem 4, and the one falsifiable consequence

**Theorem 4.** Every member of the class has a **constant** asymptotic residual acceleration

$$\Delta \;\equiv\; \lim_{g_{\rm bar}\to\infty}\left(a - g_{\rm bar}\right)
\;=\; cH_\Lambda\left(1 - \lambda\,\Phi_\infty\right),$$

and the condition $\mu \le 1$ is *exactly* $\Delta \ge 0$. For the balance member of Theorem 3,
$\Phi_\infty = k/H = 1/r$ in closed form, so $\lambda\Phi_\infty = 1 - 1/r$ and

$$\Delta \;=\; \frac{cH_\Lambda}{r} \;=\; \frac{a_0}{2} \quad\text{exactly.}$$

*Proof.* Expand $w(s) = \sqrt{s(s+2T_{\rm GH})}$ against $F/c_1^\infty \to s + T_{\rm GH}\lambda\Phi_\infty$ at
large $s$; $\Phi_\infty$ for the balance member is $\int_0^\infty \psi\,dx = k$ by closed-form integration.
$\square$

So "no super-Newtonian region" and "the residual acceleration points inward" are the same condition, and the
floor of Theorem 2 *is* a measurable constant sunward acceleration. That is the falsifiable consequence, and it
has already been measured: $\Delta = a_0/2 = 4.681\times10^{-11}\ \mathrm{m\,s^{-2}}$ (canonical),
$5.650\times10^{-11}$ (ALT), against the Earth constant-radial $2\sigma$ bound
$3.66\times10^{-14}\ \mathrm{m\,s^{-2}}$ (Sereno & Jetzer 2006, inverting Pitjeva's EPM2004) — **over by
$1279\times$ / $1544\times$**. Read as a bound on the class parameter, $\Delta \le 3.66\times10^{-14}$ requires
$r \ge 14807$, and that member has $a_0 = 7.3\times10^{-14}\ \mathrm{m\,s^{-2}}$, about $1279\times$ too small for
galaxies. On the balance member *no* $r$ does both jobs, and the incompatibility is $r$-independent precisely
because $a_0 = 2\Delta$.

Escape is not excluded, and we do not claim it is: $\Delta$ and $a_0$ are independent functionals of $f$ — an
integral and a slope ratio — locking as $\Delta = a_0/2$ only on the member reproducing $\nu = \sqrt{1+1/y}$. But
escape requires $\lambda\Phi_\infty$ within $6.75\times10^{-5}$ of $1$, which forces $\mu\to1$ in the
near-Newtonian regime and hence a kernel that is **not** $\sqrt{1+1/y}$ there. In the exactly solvable
single-scale family $\psi = (1+x/\delta)^{-2}$ the two demands are provably incompatible: $\Delta = 0$ forces
$\delta \ge 1/2$, hence $r \le 3$, against $r = 2Z = 11.578$. (One family, solved exactly; not a theorem about
all $\psi$.)

The same handle has a second, cosmological reading needing no new mechanism: a *local* response to the vacuum
**density** gives $k \propto \sqrt{\rho_{\rm DE}}$, exactly constant for $w=-1$, while a *global* horizon rate
gives $k \propto cH_0E(z)$, rising to $1.79$, $3.03$, $4.57$ times its present value at $z=1,2,3$
($\Omega_m = 0.3153$; the published $1.78/3.01/4.54$ assume $\Omega_m = 0.309$, so the number must be quoted with
its $\Omega_m$). The density reading — this framework's — is the *more* falsifiable, since it forbids
a branch the horizon reading permits. Recorded honestly: for $w\ne-1$ the correct $a_0(z)$ law is
bump-then-decline, not a rise, so MUSE-DARK III's measurement of a *rising* $a_0$ is a tension, not a
confirmation.

## 7. What is **not** claimed

- **The coefficient is not derived.** $\kappa = 1/2$, equivalently $r = 2Z$, is **FITTED**. Theorem 3 makes it
  *less* derivable, not more: it shows the class is exactly as free as the choice of floor and constrains that
  choice not at all. The admissibility route to deriving any coefficient — $2Z$, $4\pi$ or Milgrom's $1$ — is
  closed by theorem, not by another failed search.
- **There is no complete field theory.** Nothing here is an action, and this corpus does not have one. For the
  generic form class examined, the law is not variational in a disc; the $u$-contraction is $(v/c)^2$-suppressed,
  needing a prefactor $\sim3.8\times10^5$–$3.8\times10^7$ against $\|K\|\le1$; and that prefactor *is* the
  worldline's Frenet torsion, so the obstruction is one of sign. Torsion-free (hyperbolic) motion makes the action
  exact — it works for linear acceleration and fails for orbits, and MOND is about orbits. The disformal-$\rho_m$
  escape is now closed classically by a cone constraint. **Open and not closed:** non-quadratic-in-$u$ terms,
  $\rho_m/T_{\mu\nu}$ coupling, the $b$-projector at third-derivative cost, finite parts, all-orders rigidity,
  $T_{\mu\nu}$ variation, the ephemeris $de/dt$.
- **There is no Standard-Model connection.** None is claimed, attempted or implied.
- **Nothing here excludes the framework's galactic phenomenology.** The radial-acceleration and baryonic
  Tully–Fisher relations, the $a_0$-line and the spherical results are untouched, as is
  $a_0 = \kappa c\sqrt{G\rho_\Lambda}$ as a *statement*. What §6 excludes is the literal reading of
  $g_{\rm obs}^2 = g_{\rm bar}^2 + a_0g_{\rm bar}$ as a law valid in the solar system.
- **A second exact restatement of the same number derives nothing either.** In the ghost-condensate dark sector,
  with $M^4 = \rho_\Lambda c^2$ and $\dot\phi = a_0/c$, the decay constant is
  $f_{\rm dec} = M^2/\dot\phi = M_{\rm Pl}/\kappa$ exactly, so $\kappa=\tfrac12 \Leftrightarrow
  f_{\rm dec} = 2M_{\rm Pl}$ — linear in $1/\kappa$, hence another relabelling. Against interest twice: swampland
  folklore prefers $f_{\rm dec}\le M_{\rm Pl}$, i.e. $\kappa\ge1$, which the data do not want; and the competing
  $r=4\pi$ proposal is $f_{\rm dec} = 2.171\,M_{\rm Pl}$, **not** the $6.283\,M_{\rm Pl}$ printed elsewhere in
  this corpus (a factor $Z/2$ too large, from the conflation of §3) — so the correction favours the competitor.

## 8. Verification

`real_research/reviews/mi_r_one_parameter_nogo_paper_2026.py` — 41/41 checks, exit 0, sympy + numpy; sections A–I
map onto §§2–6. Every section carries a negative control that prints `[FAIL]` if the surrounding claim is
weakened: the wrong floor $k=a_0$ (Theorem 2), the wrong deep coefficient $f'(T_{\rm GH})/2\pi$ (Theorem 1), the
sign-flipped floor $+k$ in $\mu$ (Theorem 3), and $\delta$ on both sides of the exact $1/2$ edge (§6). Liveness
was mutation-tested: perturbing the ephemeris bound by $10^3$ breaks 3 checks; $4\pi^2\to2\pi^2$ in $f_r$ breaks
4; $Z\to2\pi$ breaks 8; $\Phi_\infty\to2k$ breaks 1; each exits non-zero. Float64 hazards are handled and
*reported* rather than tolerance-hidden: $\sqrt{G^2+k^2}-k$ and $1-\mu$ are both written difference-free, and
monotonicity is asserted only on the 16 decades where consecutive $\mu$ values are float64-resolvable.
Supporting scripts:
`mi_crossover_master_formula_2026.py` (14/14, Theorem 1 and the withdrawal of the earlier rigidity claim),
`mi_psi_search_r2Z_2026.py` (27/27, the variational solution and the withdrawal of the seven-shape exclusion),
`mi_r_admissibility_bound_2026.py` (6/6 as a computation; checks B2 and C1 withdrawn),
`mi_gw_ppn_gauntlet_2026.py` (56/56, the ephemeris and Cassini numbers),
`mi_cosmo_perturbations_2026.py` (63/63, the condensate identity),
`mi_disformal_completion_2026.py` (48/48, the disformal closure cited in §7).

---

## Bibliography

- Bekenstein, J. D. (2004). Relativistic gravitation theory for the modified Newtonian dynamics paradigm.
  *Phys. Rev. D* **70**, 083509.
- Bekenstein, J. D. & Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian
  gravity? *Astrophys. J.* **286**, 7. (AQUAL.)
- Ciocan, B. I. et al. (2026). MUSE-DARK III. (Measurement of a rising $a_0$; a tension for the constant/declining
  reading, and ΛCDM-degenerate.)
- Deser, S. & Levin, O. (1997). Accelerated detectors and temperature in (anti-) de Sitter spaces.
  *Class. Quantum Grav.* **14**, L163.
- Lelli, F., McGaugh, S. S. & Schombert, J. M. (2016). SPARC: Mass models for 175 disk galaxies.
  *Astron. J.* **152**, 157.
- McGaugh, S. S. (2008). Milky Way mass models and MOND. *Astrophys. J.* **683**, 137, eq. 11a. (Exponential
  kernel $\nu = (1-e^{-\sqrt y})^{-1}$.)
- Milgrom, M. (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass
  hypothesis. *Astrophys. J.* **270**, 365.
- Milgrom, M. (1994). Dynamics with a nonstandard inertia-acceleration relation: an alternative to dark matter in
  galactic systems. *Ann. Phys.* **229**, 384, §II eq. 3. ($a_\lambda = c^2\sqrt{\Lambda/3}$.)
- Milgrom, M. (1999). The modified dynamics as a vacuum effect. *Phys. Lett. A* **253**, 273, eqs. 6–9
  ($\nu = \sqrt{1+1/y}$, $\hat a_0 = 2cH_\Lambda$) and eqs. 10–11 (a second coefficient).
- Milgrom, M. (2008). MOND: time for a change of mind? arXiv:0801.3133, §7.3.1. ("Isn't necessarily meaningful …
  would just point to a different effective $\mu(x)$.")
- Milgrom, M. (2020). The $a_0$–cosmology connection in MOND. arXiv:2001.09729.
- Milgrom, M. (2022). Modified-inertia MOND at the level of the equations of motion. *Phys. Rev. D* **106**,
  064060. (Such theories "are not necessarily governed by an action"; requires $x\mu(x)$ monotonic.)
- Narnhofer, H., Peter, I. & Thirring, W. (1996). How hot is the de Sitter space?
  *Int. J. Mod. Phys. B* **10**, 1507. (Temperature $\sqrt{a^2+\Lambda/3}/2\pi$.)
- Pitjeva, E. V. (2005). High-precision ephemerides of planets — EPM2004. *Solar System Research* **39**, 176.
- Sereno, M. & Jetzer, P. (2006). Dark matter versus modifications of the gravitational inverse-square law:
  results from planetary motion in the solar system. *MNRAS* **371**, 626 (astro-ph/0606197), Tab. 1 and Eq. 9.
- Skordis, C. & Zlosnik, T. (2021). New relativistic theory for modified Newtonian dynamics.
  *Phys. Rev. Lett.* **127**, 161302. (AeST.)
