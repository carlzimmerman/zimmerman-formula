# A Cubic Separation Law for Wide Binaries: an Exponent With No Free Parameters

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

*Version 3 · 2026-07-30. The $s^3$ prediction, its five falsifiers and the frozen pre-registration are
UNCHANGED. v3 (i) reduces the coefficient to a single rational, $a_0=\kappa c\sqrt{G\rho_\Lambda}$ with
$\kappa=1/2$ (§1); (ii) tightens the ECCENTRIC-ORBIT error budget from a factor of several to
$\lesssim8\%$ using the action's own $\Box_u$, and records two exact identities (§2.1); (iii) adds an
independent CMB check of the $a_0$ footing, crediting Gnedin (2008) for posing and first deciding that
fork (§8); and (iv) reports six closed classes in the search for what fixes $\kappa$ — a negative
result. Version 2 (2026-07-28) settled the branch ambiguity, generalised the exponent, and resolved
feasibility negatively; Version 1 (2026-07-25) is superseded. Scripts listed in §8.*

---

## The claim, first

In wide binaries wider than about 50 kAU, the relative velocity should exceed the Newtonian value by an
amount growing as the **cube of the separation**:

$$\gamma_v(s) - 1 \;\simeq\; \tfrac{1}{2}\big[\nu(y_\mathrm{ext})-1\big]\,\frac{\omega_c^{2}}{GM}\,s^{3}.$$

The **exponent is 3**. It is derived, not fitted, and it cannot be tuned. Every known contamination
channel in wide-binary samples rises as $s^{1/2}$ instead. Exponent 3 against exponent 0.5 — that
contrast is the measurement.

**What would kill it.** Any one of: no excess beyond ~50 kAU in a contamination-controlled sample; an
excess whose log-slope is inconsistent with 3; a knee that does not move as $M^{1/3}$; an amplitude
inconsistent with $\omega_c^2/GM$; or a boost $\gamma_v\approx1.02$ found *inside* 30 kAU (**renumbered
2026-07-30 from 1.09 under the retired $\alpha=1$ kernel; see the notice in §2**).

**What it cannot do.** It cannot be measured with Gaia DR3. We checked the catalogue ourselves; see §6.

---

## 1. Two scales, one of them free

The framework is *modified inertia* — the modification is in the matter sector, not in gravity. Its
acceleration scale is tied to the cosmological constant:

$$a_0=\frac{cH_\Lambda}{Z}=c^2\sqrt{\frac{\Lambda}{32\pi}}=9.36\times10^{-11}\ \mathrm{m}\,\mathrm{s}^{-2},
\qquad Z=\sqrt{32\pi/3}=5.78881 .$$

**New in v3 — the coefficient is a single rational, and "$32\pi/3$" is an artifact.** Writing $32\pi$
as $8\pi/\kappa^2$ and substituting $\Lambda=8\pi G\rho_\Lambda/c^2$, *every* $\pi$, the 32 and the 3
all cancel:

$$\boxed{\,a_0=\kappa\,c\sqrt{G\rho_\Lambda}\,},\qquad \kappa=\tfrac12 .$$

So $32\pi/3$ is not a compound of three geometric factors — it is what one statement looks like after
being routed through $\Lambda$ and Einstein's $8\pi$. The framework's entire dimensionless content is
the single **rational** $\kappa=1/2$, and the honest form of the open problem is *why $\kappa=\tfrac12$*,
not *why $32\pi/3$*. Two consequences worth recording. (i) The standing transcendence obstruction —
"$Z$ carries a transcendental $\sqrt\pi$ while flavour data are algebraic" — is correct about $Z$, but
that $\sqrt\pi$ belongs to **general relativity's** $8\pi$, not to this framework, whose own number is
rational. (ii) $\kappa$ remains **postulated**: an exhaustive sweep of the kernel's own conditions
(Herglotz sum rule, $K(0)=0$, $\lVert K\rVert\le1$, retarded analyticity, branch point, thermal
saturation against every forced kernel constant, and the location statistics of the spectral measure)
found **none** that fixes it, because each is imposed at a scale-free point of the dimensionless axis
$z=\Box_u/a_0^2$ and is therefore invariant under $a_0\to\lambda a_0$. Six classes closed; the value
is not derived.

**⚠️ KERNEL CHANGED 2026-07-30.** This paper was written with $\nu(y)=\sqrt{1+1/y}$ ($\alpha=1$). The
framework has since adopted $\mu(x)=x/\sqrt{1+x^2}$ ($\alpha=2$, Milgrom 1983), because the $\alpha=1$
tail implies a constant sunward anomaly $a_0/2$ that is **1279× the Earth 2σ ephemeris bound**. Two
consequences for this paper, both stated rather than absorbed: **(i)** the identity
$g_\mathrm{obs}^2-g_\mathrm{bar}^2=a_0g_\mathrm{bar}$ below is an $\alpha=1$ identity and no longer
holds — it is retained as attribution, not as a live relation; **(ii)** the ungated boost quoted
throughout as $\gamma_v\approx1.09$ becomes $\approx\mathbf{1.02}$ (orientation-averaged 1.0246, range
1.0182–1.0350 over both $a_0$ footings and both frozen $g_{\rm ext}$ values), per Amendment 3 to
`PREREGISTRATION_DR4.md`, filed in the open before DR4. **The paper's central result is unaffected**:
the cubic gate law, its $s^{1/2}$-versus-$s^3$ contrast and the $M^{1/3}$ knee are properties of the
gate, not of the tail exponent, and the gated prediction remains $\gamma_v\to1.000$.

**Credit, plainly stated.** The interpolation $\nu(y)=\sqrt{1+1/y}$ and the identity
$g_\mathrm{obs}^2-g_\mathrm{bar}^2=a_0g_\mathrm{bar}$ are Milgrom (1999, *Phys. Lett. A* **253**, 273),
Eqs. (8)–(9), with coefficient $2cH_\Lambda$. Milgrom (1999, 2015) and Smolin (2017, *Phys. Rev. D*
**96**, 083523) had already tied $a_0$ to $\Lambda$ with a $2\pi$ coefficient. **No priority is claimed
for the $\Lambda$ tie.** What is ours: the coefficient $cH_\Lambda/Z$, the modified-inertia completion,
and the prediction below.

The second scale is a response gate. The matter sector's effective response is

$$K_\mathrm{eff}=1-S\big(|a|/a_0\big)\,G(\omega),\qquad G(\omega)=\frac{1}{1+i\omega/\omega_c},
\qquad S\to \frac{a_0}{2g_N}\ \ \text{(deep-Newtonian)},$$

with $\omega_c\in[1.782,\,2.211]\times10^{-14}\ \mathrm{s}^{-1}$. Every number below is carried on both
cosmological footings ($a_0=cH_\Lambda/Z$ and $a_0=cH_0/Z$, differing by ~21%).

**Why a gate must exist.** On the frequency axis $|K|=1$ *exactly* for every $\omega>a_0/2c$: the
kernel saturates and has no high-frequency roll-off. So $K$ gives an inner-disk star and the Earth the
**same** response. Since the solar system must be Newtonian and galaxies must not be, something
frequency-dependent with a roll-off is required. The gate's existence is forced, not assumed.

**Why its scale is not.** Stated against interest: $\omega_c$ is a **free parameter**. A dimensional
census puts every intrinsic scale of the theory 3.2–5.6 decades away from it, and consistency alone
(galaxies must survive, the solar-system monopole must not) brackets it only to ~3 orders of magnitude.
So $a_0$'s value, $Z$, the sign $s=-1$, **and $\omega_c$** are postulated, not derived. Version 1 did
not say this clearly enough; it does now.

## 2. What frequency a binary presents to the gate

The kernel's argument is fixed by the action, not chosen. The committed matter term is

$$S_\mathrm{matter}=-\tfrac12\int d^4x\sqrt{-g}\,\rho_m\big[s\,u^\mu K(\Box_u/a_0^2)u_\mu\big],
\qquad \Box_u f=u^a\nabla_a(u^b\nabla_b f),$$

so $\Box_u$ is the second derivative *along the worldline*. On a circular orbit $u_\mu$ is an
eigenvector of it:

$$\Box_u u_\mu = -\Omega^2 u_\mu \qquad\text{(identically; verified symbolically)}.$$

The argument is therefore $z=-(\Omega c/a_0)^2$ — the **orbital frequency**. The acceleration
*magnitude* $|a|=\Omega^2R$ genuinely is constant on a circular orbit, but the action never feeds $|a|$
to $K$.

**This settles an ambiguity Version 1 was explicitly conditional on.** Had the kernel responded to
$|a|$, the gate would stay open and the prediction would be $\gamma_v\approx1.02$ instead (1.09 under the
retired $\alpha=1$ kernel). It does not.
The result below no longer rests on a choice.

### 2.1 New in v3 — eccentric orbits, and how sharp the prediction actually is

Real wide binaries are **not circular**, so §2's identity is the wrong tool for them on its own, and
this is the honest soft spot of v1 and v2. Off circles the eigenvector relation fails and a *closure*
must be chosen — a prescription for reducing $\Box_u u_\mu$ to the scalar argument of $K$. The repo's
prior verdict on that closure was **free, bounded**. Two things are new here.

**(a) The freedom is much smaller than "free" suggests — by two orders of magnitude.** The prior
bracket was computed over time-weightings of $|a|^2$, which know nothing about $\Box_u$. Using the
action's actual $\Box_u u$ instead collapses the spread. On radial infall onto $10^{12}M_\odot$ — the
maximally non-circular case, i.e. a hard upper bound on eccentricity effects:

| infall from | $|a|^2$-weighting family | action $\Box_u$ family | narrowing |
|---|---|---|---|
| 300 kpc | $\nu = 1.170,\,2.364,\,7.837$ — spread **570%** | $\nu = 1.0004,\,1.0062,\,1.0797$ — spread **7.9%** | **72×** |
| 100 kpc | spread **172%** | spread **0.9%** | **189×** |

So the off-circular ambiguity in $\nu$ is $\lesssim8\%$ in the worst case, not a factor of several. The
$s^3$ prediction is correspondingly **sharp to that level for eccentric pairs**, which is what the
Gaia DR4 shape test actually needs. This upgrades the prediction from quasi-linear to nearly sharp.

**(b) Two exact identities, and an honest limit.** Symbolically, at matched local acceleration $a$ and
radius $r$:

$$\text{circular:}\quad \frac{\Box_u u}{u}=-\Omega^2=-\frac{a}{R},
\qquad\qquad \text{radial infall:}\quad \frac{\Box_u u^r}{u^r}=\frac{2GM}{r^3}=+\frac{2a}{r}.$$

A factor **2** and an **opposite sign**. Stated against interest: the action does **not** eliminate the
freedom, because $\Box_u u$ is *not parallel* to $u$ off circles — the spatial and time components
differ by 8 to 5 orders along the infall — so a projection must still be chosen. The action narrows;
it does not close.

## 3. The gate is shut in the window everyone measures

A pair of total mass $M$ at separation $s$ has $\Omega=(GM/s^3)^{1/2}$. For M = 1.5 M⊙ at 10 kAU,
$\Omega=2.44\times10^{-13}\ \mathrm{s}^{-1}$ — **11× above the top of the whole $\omega_c$ window.** The
gate is shut, $\mathrm{Re}\,G=0.005$–$0.008$, and $\gamma_v=1.0004$–$1.0006$: within $0.04\sigma$ of
Newton.

Two radii run in opposite directions with separation:

$$r_M=\sqrt{GM/a_0}\quad(\text{sub-}a_0\text{ begins}),\qquad
r_\mathrm{gate}=(GM/\omega_c^2)^{1/3}\quad(\text{gate opens}).$$

Since $\Omega\propto s^{-3/2}$ while $g\propto s^{-2}$, always $r_\mathrm{gate}>r_M$ — the ratio is
4.54–7.76 across 0.5–3.0 M⊙, both footings, both edges. **Between them a pair is already below
$a_0$ but still gate-shut, so it must look Newtonian.** For 1.5 M⊙ that dead zone runs ~10 to
~50–60 kAU.

**Galaxies are untouched, which is what makes the gated reading admissible.** Galactic orbital
frequencies are $\Omega=v/r$, nine orders smaller. Across the Milky Way solar circle and outer disk,
dwarfs, low-surface-brightness disks, massive spirals and the inner disk, the largest value found is
$\Omega/\omega_c=0.364$ ($\mathrm{Re}\,G\ge0.883$). Gate open in galaxies, shut in wide binaries: the
radial acceleration relation and the baryonic Tully–Fisher relation are unaffected.

## 4. The cubic law — and why the exponent counts poles

Deep in the gate-shut regime $\Omega\gg\omega_c$, so $\mathrm{Re}\,G\to(\omega_c/\Omega)^2$; substituting
$\Omega=(GM/s^3)^{1/2}$ gives $\mathrm{Re}\,G\to(\omega_c^2/GM)\,s^3$, hence the boxed law. The measured
local slope $d\ln(\gamma_v-1)/d\ln s$ is **3.00** at 5 kAU, falling through the knee to 0.06 once
saturated.

An $n$-pole gate gives $|G_n|^2\to(\omega_c/\Omega)^{2n}$, so

$$\gamma_v-1\propto s^{3n}\qquad\Longrightarrow\qquad n=p/3 .$$

Verified numerically at $n=1,2,3$ (slopes 3.00, 6.00, 8.99). **The measured exponent returns the gate's
pole count.** The committed gate is one-pole and predicts exactly 3; 6 would mean two poles; anything
not a multiple of 3 rules out the rational-pole form. *(The identity $|G|^2=\mathrm{Re}\,G$ used above
holds only at $n=1$; for $n>1$ the law uses $|G_n|^2$.)*

**The exponent is parameter-free even though the amplitude is not.** $\omega_c$ is free (§1) and enters
the amplitude — but it does **not** enter the exponent. That asymmetry is the whole reason this is
worth measuring. Three mass powers follow from the same closed form and are recovered numerically:
$r_\mathrm{gate}\propto M^{0.3333}$, $r_\mathrm{efe}\propto M^{0.5000}$, fixed-separation excess
$\propto M^{-0.9935}$ (asymptotic; knee-contaminated to $M^{-0.857}$ by 30 kAU, so fit the local slope
rather than assuming a global $1/M$).

## 5. The discriminant

Every published contamination channel carries a *fixed velocity scale*, so its scaled relative velocity
rises as $s^{1/2}$: chance alignment (El-Badry, Rix & Heintz 2021, via $R_\mathrm{chance\,align}$),
unresolved tertiaries (Peñarrubia 2021; Tyler, Green & Goodwin 2023), close-binary contamination.
**Exponent 0.5 against 3.0.** Signal and background have different separation dependences, so a joint
fit is well posed.

This matters because the *amplitude* axis is unusable: the two groups analysing the same public
catalogue differ by $\Delta\gamma_v\approx0.174$, about **2.1× the entire predicted boost.** No
amplitude test survives that spread. A shape test does.

## 6. Why this waits for Gaia DR4 — now resolved, negatively

Version 1 said feasibility "cannot be settled without the catalogue in hand" and "may be fatal to a DR3
test." We pulled the catalogue. It is fatal.

Because the excess grows as $s^3$, nearly all the signal sits at large separation:

| $s$ [kAU] | $\gamma_v$ | note |
|---|---|---|
| 30 | 1.0125 | the cut used by every published analysis |
| 50 | 1.0392 | — |
| 100 | 1.0808 | — |
| 200 | 1.0932 | catalogue's reach |

At the 30 kAU cut the predicted excess ($1.2\times10^{-2}$) is an order of magnitude below the
inter-group systematic — **the conventional window cannot test this.** And at our own recipe's cuts
($d<200$ pc, $R_\mathrm{chance\,align}<0.1$, RUWE $<1.4$ both components, MS–MS), the El-Badry, Rix &
Heintz (2021) Gaia eDR3 catalogue contains only

$$436\;/\;270\;/\;155\;/\;60\;/\;24\;/\;3\ \ \text{pairs across the }30\to236\ \text{kAU bins},$$

i.e. **364 clean pairs beyond 50 kAU** and ~70 beyond 100 kAU. The shape test needs ~2000 per bin for
5σ separation of $p=3$ from $p=0.5$ (~400 gives only ~2.3σ). Relaxing the distance cut does not rescue
it: proper-motion velocity error scales as (distance × pm error) while the sample requirement scales as
$\sigma^2$, so raw counts at $d<1000$ pc are ~15× larger but the usable gain is far smaller — and even
at face value only 2 of 6 bins clear 2000, while a log-slope fit needs most bins populated.

Ground-based astrometry cannot substitute. The test needs $\sigma_\mathrm{pm}\lesssim0.02$ mas yr$^{-1}$ at
200 pc; Rubin/LSST delivers ~0.1–1.0 over ten years. **Gaia DR4 is the only route.**

## 7. Pre-registration

Since the test cannot run until DR4, the prediction is frozen in the open beforehand. The pre-registration
(`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, Amendment 1, 2026-07-27, SHA-256
`a309a502332b84ad521385b1c2031652849c9ce358c396f680f2308dd5ba1c13`) records:

- the frozen prediction **$p=3$** for the log-slope beyond $r_\mathrm{gate}$;
- $\gamma_v=1.0004$–$1.0006$ inside 2–30 kAU, i.e. **a Newtonian DR4 result in that window confirms
  this branch rather than refuting it** — which the unamended pre-registration would have scored as a
  kill;
- the five falsifiers listed at the top of this note;
- and that DR4 $\gamma_v$ constrains the $\nu$+EFE+gate prescription, **not** the value of $a_0$ or
  $Z$. No outcome may be reported as measuring either.

## 8. What is not claimed

- **Not a test of $a_0$ or $Z$.** A confirmed $s^3$ rise establishes a frequency scale $\omega_c$ and a
  one-pole response. $Z=5.7888$ and the conventional $2\pi=6.2832$ differ by 7.87%, both lie inside the
  $\pm16\%$ empirical $a_0$ box, and no arena examined here separates them. Against interest: matching
  Chae (2024b)'s central $\gamma$ on this framework's own kernel needs $a_0\approx1.9\times$ canonical,
  which at face value disfavours the $\Lambda$-tied coefficient specifically.
- **Nothing about whether dark matter exists.** A wide-binary result constrains the weak-field *force
  law*, not the matter content. $\gamma_v=1$ is Newton's prediction — shared by ΛCDM, by this
  framework's own gated branch, and by modified-force-plus-particle hybrids.
- **$a_0$'s value, $\kappa$ (equivalently $Z$), the sign $s=-1$ and $\omega_c$ are postulated, not
  derived.** New in v3: six independent classes of condition on the kernel's own spectral structure
  were swept for one that would fix $\kappa$, and all six are closed — every committed condition sits
  at a scale-free point of $z=\Box_u/a_0^2$ and is invariant under $a_0\to\lambda a_0$.

**New in v3 — the footing this paper carries is the one independently favoured, and credit for that
question is not ours.** The paper runs both $a_0$ footings throughout. The fork itself — whether $a_0$
couples to $cH(z)$ or to the dark-energy density $\sqrt{8\pi G\rho_\Lambda/3}$ — was posed and tested
long before this work: **Gnedin (2008)**, *The Redshift Evolution of the Tully–Fisher Relation as a
Test of Modified Gravity* (arXiv:0809.2790), states both options explicitly, tests them against
high-$z$ Tully–Fisher data to $z=1.2$, and concludes that dark-energy coupling can be consistent while
Hubble coupling requires unreasonable $w$ — *"this would appear to favor coupling to the dark energy
density."* See also arXiv:0802.1526 on whether $G$ and $a_0$ vary with epoch.

We add only an **independent check from a different epoch and different systematics**, which is worth
recording because Gnedin explicitly flagged possible unaccounted systematics. Applying the two footings
to the recombination plasma: since the acoustic acceleration is $a_\mathrm{ac}\sim c_sH$, a rising
$a_0=cH(z)/Z$ makes $H$ **cancel**, leaving $y=Z/\sqrt{3(1+R)}\approx2.6$–$3.3$ at *every* epoch — so
$\nu-1\approx15\%$ throughout the entire acoustic era, not as a late correction. Propagated through
$c_s^2=c^2/[3(1+R)]$ over CAMB's exact background (our sound-horizon integral reproduces CAMB's own
$r_\star=144.44$ Mpc to $0.00\%$), this shifts $\theta_\star$ by $\approx1.5\%$ against Planck's
$0.03\%$ measurement — excluded. The constant, $\rho_\Lambda$-tied footing shifts $\theta_\star$ by
$3\times10^{-7}$ and is consistent. **Same verdict as Gnedin (2008), from the CMB rather than from
Tully–Fisher.** Stated as a limitation: this is a background-plus-recombination treatment, not a
modification of the Boltzmann perturbation hierarchy, and a fully relativistic MOND theory (AeST;
Skordis & Złośnik) already reproduces the CMB — so the rigorous form of this question belongs to that
theory, not to an $a_0(z)$ scaling argument.

**Reproducibility.** Every number is printed by committed scripts, all `exit 0`, no hard-coded verdicts,
both footings and both $\omega_c$ edges throughout: `mi_dcac_branch_settled_2026.py` (5/5, §2),
`mi_wb_gate_fork_2026.py` (11/11, §3), `mi_wb_cubic_rise_2026.py` (10/10, §4),
`mi_wb_exponent_pipeline_2026.py` (6/6, §4–5), `mi_wb_dr3_feasibility_2026.py` (5/5, §6),
`mi_omegac_anchor_2026.py` (8/8, §1), `count_wb_elbadry2021.py` (catalogue counts). New in v3: `mi_kappa_spectral_reduction_2026.py` (§1, the kappa reduction), `mi_offcircular_closure_collapse_2026.py` (§2.1, the closure narrowing and the two identities), `mi_three_classes_2026.py` + `mi_thermal_class_nogo_2026.py` + `mi_bootstrap_circularity_2026.py` (§8, the six closed classes), `mi_cmb_camb_run_2026.py` (§8, the CAMB footing check). Repository:
https://github.com/carlzimmerman/zimmerman-formula

**Corrections carried from Version 1**, recorded rather than quietly fixed: the 200-vs-30 kAU excess
ratio is 7×, not the >10× first stated; the fixed-separation mass scaling is asymptotic ($M^{-0.9935}$
at 10 kAU) and knee-contaminated to $M^{-0.857}$ by 30 kAU; the operative sample requirement is the
shape test's ~2000 pairs/bin, not the ~265 implied by excess-detection alone; and $\omega_c$ is now
declared a free parameter rather than described as a constrained window.

---

**New in v3, and stated plainly:** nothing in this version changes the $s^3$ prediction, its five
falsifiers, or the frozen pre-registration. v3 sharpens the *error budget* (§2.1: eccentric-orbit
closure now $\lesssim8\%$ instead of a factor of several), simplifies the *coefficient* (§1: one
rational $\kappa=1/2$), and adds an *independently-credited* footing check (§8). No new observable,
no new claim, and one additional negative result — six closed classes in the search for what fixes
$\kappa$.

---

## References

Banik, I., Pittordis, C., Sutherland, W., et al. 2024, *MNRAS* — wide-binary Newtonian null.
Chae, K.-H. 2023–2025, *ApJ* — wide-binary boost claims.
El-Badry, K., Rix, H.-W., & Heintz, T. M. 2021, *MNRAS* **506**, 2269 — the public Gaia eDR3 catalogue.
Milgrom, M. 1983, *ApJ* **270**, 365.
Gnedin, O. Y. 2008, arXiv:0809.2790 — the redshift evolution of the Tully–Fisher relation; poses and tests the $a_0\propto cH$ versus $a_0\propto\sqrt{\rho_\Lambda}$ fork.
Milgrom, M. 1999, *Phys. Lett. A* **253**, 273 — Eqs. (8)–(9): the kernel and identity used here.
Milgrom, M. 2015, *Can. J. Phys.* **93**, 107.
Peñarrubia, J. 2021 — wide-binary contamination.
Smolin, L. 2017, *Phys. Rev. D* **96**, 083523.
Tyler, J., Green, A., & Goodwin, S. 2023 — hierarchical contamination.
