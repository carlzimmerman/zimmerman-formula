# A Cubic Separation Law for Wide Binaries: an Exponent With No Free Parameters

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

*Version 2 · 2026-07-28. Version 1 (2026-07-25) is superseded: the branch ambiguity it was conditional
on is now settled from the theory's own action, its open feasibility question is answered (negatively),
the exponent is generalised, and one parameter is newly declared free. Scripts listed in §8.*

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
inconsistent with $\omega_c^2/GM$; or a boost $\gamma_v\approx1.09$ found *inside* 30 kAU.

**What it cannot do.** It cannot be measured with Gaia DR3. We checked the catalogue ourselves; see §6.

---

## 1. Two scales, one of them free

The framework is *modified inertia* — the modification is in the matter sector, not in gravity. Its
acceleration scale is tied to the cosmological constant:

$$a_0=\frac{cH_\Lambda}{Z}=c^2\sqrt{\frac{\Lambda}{32\pi}}=9.36\times10^{-11}\ \mathrm{m}\,\mathrm{s}^{-2},
\qquad Z=\sqrt{32\pi/3}=5.78881 .$$

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
$|a|$, the gate would stay open and the prediction would be $\gamma_v\approx1.09$ instead. It does not.
The result below no longer rests on a choice.

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
- **$a_0$'s value, $Z$, the sign $s=-1$ and $\omega_c$ are postulated, not derived.**

**Reproducibility.** Every number is printed by committed scripts, all `exit 0`, no hard-coded verdicts,
both footings and both $\omega_c$ edges throughout: `mi_dcac_branch_settled_2026.py` (5/5, §2),
`mi_wb_gate_fork_2026.py` (11/11, §3), `mi_wb_cubic_rise_2026.py` (10/10, §4),
`mi_wb_exponent_pipeline_2026.py` (6/6, §4–5), `mi_wb_dr3_feasibility_2026.py` (5/5, §6),
`mi_omegac_anchor_2026.py` (8/8, §1), `count_wb_elbadry2021.py` (catalogue counts). Repository:
https://github.com/carlzimmerman/zimmerman-formula

**Corrections carried from Version 1**, recorded rather than quietly fixed: the 200-vs-30 kAU excess
ratio is 7×, not the >10× first stated; the fixed-separation mass scaling is asymptotic ($M^{-0.9935}$
at 10 kAU) and knee-contaminated to $M^{-0.857}$ by 30 kAU; the operative sample requirement is the
shape test's ~2000 pairs/bin, not the ~265 implied by excess-detection alone; and $\omega_c$ is now
declared a free parameter rather than described as a constrained window.

---

## References

Banik, I., Pittordis, C., Sutherland, W., et al. 2024, *MNRAS* — wide-binary Newtonian null.
Chae, K.-H. 2023–2025, *ApJ* — wide-binary boost claims.
El-Badry, K., Rix, H.-W., & Heintz, T. M. 2021, *MNRAS* **506**, 2269 — the public Gaia eDR3 catalogue.
Milgrom, M. 1983, *ApJ* **270**, 365.
Milgrom, M. 1999, *Phys. Lett. A* **253**, 273 — Eqs. (8)–(9): the kernel and identity used here.
Milgrom, M. 2015, *Can. J. Phys.* **93**, 107.
Peñarrubia, J. 2021 — wide-binary contamination.
Smolin, L. 2017, *Phys. Rev. D* **96**, 083523.
Tyler, J., Green, A., & Goodwin, S. 2023 — hierarchical contamination.
