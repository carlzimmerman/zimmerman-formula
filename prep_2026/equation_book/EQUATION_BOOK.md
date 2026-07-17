# THE EQUATION BOOK
## Novel closed forms, identities, and estimators of the de Sitter–Unruh modified-inertia framework

**Date:** 2026-07-16 · **Status:** post-adversarial-verify (see `VERIFY.md`; all verdicts carried verbatim)

**The framework, on its own terms:** modified INERTIA with horizon-derived
$a_0 = cH_\Lambda/Z$, $Z = \sqrt{32\pi/3}$, interpolation $\nu(y)=\sqrt{1+1/y}$, hence the law

$$g_{\rm obs} \;=\; \sqrt{\,g_{\rm bar}^2 + g_{\rm bar}\,a_0\,}$$

**Both footings on every number:** canonical $a_0 = 9.362\times10^{-11}\,{\rm m/s^2}$ ($\rho_{\rm DE}/cH_\Lambda$) · alternate $a_0 = 1.130\times10^{-10}$ ($\rho_{\rm total}/cH_0$). $Z$-only results are footing-free.

**The wellhead credit (load-bearing, applies to every entry):** Milgrom 1999 (Phys. Lett. A 253:273, astro-ph/9805346) Eqs (5)+(8)–(9) contain the parent law — his vacuum-$\Delta T$ function $\hat\mu(x)=\sqrt{1+(2x)^{-2}}-(2x)^{-1}$ is machine-verified identical to the framework kernel, and with $a\,\mu(a/a_0)=g_N$ it implies $g_{\rm obs}^2-g_{\rm bar}^2=a_0 g_{\rm bar}$ exactly. What is NOT his: the coefficient (his $\hat a_0 = 2cH_\Lambda$ vs the framework's $cH_\Lambda/Z$ — factor $2Z\approx11.58$, the banked floor tension), and the elevation of $\hat\mu$ to the circular-orbit rotation-curve function (he explicitly declined). This credit cuts both ways: the framework's law carries Milgrom's own dS-vacuum pedigree. Everything DOWNSTREAM of the law in this book — the landmarks, estimators, cubics, elliptic pair, memory function, throttle invariants — survives adversarial re-derivation and remains unfound in the literature.

**The structural vein (verified):** every closed form here exists *because* the law is quadratic in $g_{\rm obs}$ and linear in $a_0$. The identical eliminations for McGaugh's exponential $\nu$ are transcendental (sympy: no closed form). This family is a signature of this specific $\nu$. (Also structurally distinct from Verlinde: his relation is additive $g_{\rm obs}-g_{\rm bar}\propto\sqrt{g_{\rm bar}a_0}$, not quadratic-in-quadrature. Desmond–Bartlett–Ferreira 2023 exhaustive symbolic regression had $\sqrt{x^2+\theta_0 x}$ in its search space but not among its winners — no scoop.)

**Rails honored:** no proof language; exact-vs-approx flagged per equation; both footings; no numerology ($Z$ symbolic throughout); every equation backed by a committed, runnable, exit-0 script in this directory; frozen repo read-only. Two sentences from the mining lanes were retracted by the verify pass and do NOT appear here (FIRE-2's "exact 1.500 to ~1%"; "only piecewise arctan forms exist").

---

## THE ARCHETYPE

### E0 — The a₀-line
$$\boxed{\;g_{\rm obs}^2 - g_{\rm bar}^2 \;=\; a_0\,g_{\rm bar}\;}$$
- **Status:** EXACT (identical rewrite of the law). **Novelty: CREDITED at law level** — contained in Milgrom 1999 Eqs (5)+(9) with coefficient $2cH_\Lambda$ vs the framework's $cH_\Lambda/Z$. The *linear-identity / slope-measurement packaging* of the RAR is not found written anywhere.
- **Chain:** square the law, subtract.
- **Enables:** the RAR becomes a zero-fit slope measurement — plot $Y=g_{\rm obs}^2-g_{\rm bar}^2$ vs $X=g_{\rm bar}$: a line through the origin with slope $a_0$.
- **Test:** SPARC/WALLABY per-point. **Mandatory method note (verified finding):** naive WLS-through-origin is biased low ~3× by M/L-correlated $g_{\rm bar}$-side errors in the difference of squares — use robust/median, a low-$y$ band, or full errors-in-variables. (`m2_massline_sparc_fire.py`)

---

## SEAM S1 — ALGEBRAIC CONSEQUENCES OF ν = √(1+1/y)

### E1 — The RAR landmark triplet  *(top-ranked, 12/12)*
With $y = g_{\rm bar}/a_0$, the log-log RAR slope and curvature are exactly
$$\sigma(y) = \frac{2y+1}{2(y+1)}, \qquad C(y) = \frac{d\sigma}{d\ln y} = \frac{y}{2(y+1)^2}$$
$$\boxed{\;\sigma(y)+\sigma(1/y) = \tfrac{3}{2}\ \ \forall y\;}\qquad
\boxed{\;C(1/y) = C(y)\;}\qquad
\boxed{\;C_{\max}\ \text{at}\ y=1:\ \big(\sigma,C\big)=\big(\tfrac34,\tfrac18\big),\ g_{\rm obs}(a_0)=\sqrt2\,a_0\;}$$
- **Status:** EXACT from the law. **Novelty: KEEP-NOVEL** (no literature hit on any RAR curvature-landmark, reciprocity symmetry, or slope sum rule; parent law credited to Milgrom 1999).
- **Chain:** differentiate $\ln g_{\rm obs}$ in $\ell=\ln y$; symmetry and sum rule are $\ell\to-\ell$ identities (re-derived independently by chain rule, `verify_audit_2026_07_16.py` §B).
- **Enables:** a parameter-free $\nu$-discriminator. Computed comparisons: McGaugh's $\nu$ peaks at $y=3.46$ with $(0.829, 0.103)$; MOND "simple" $\nu$ at $y=2.00$ with $(0.789, 0.096)$ — both break the sum rule and the symmetry. The symmetry/sum-rule tests are Υ-rescale-immune in shape (a global M/L shift slides the profile in $\ln y$ but cannot create or destroy evenness); the landmark *location* then reads off $a_0$: curvature max at $g_{\rm bar}=a_0$ = $9.36\times10^{-11}$ / $1.13\times10^{-10}$ (canonical/alt).
- **Test:** hierarchical slope-field fit on SPARC/WALLABY RAR (not binned medians). **Calibrated SPARC quick-fire (post-verify):** at the framework's committed $\Upsilon_{\rm disk}=0.70$, the binned-median sum reads 1.481–1.496 vs law-true pipeline expectation $1.53\pm0.05$ — **consistent within pipeline noise**; at $\Upsilon=0.50$ it reads ~1.40, the M/L-convention artifact per the banked ledger. Non-diagnostic at this crudeness; needs hierarchical errors. (`eqbook_S1_algebraic.py`, `eqbook_quickfire_sparc.py`)

### E2 — The exact inversion / floor form (numerically stable)
$$\boxed{\;g_{\rm bar} \;=\; \sqrt{g_{\rm obs}^2 + (a_0/2)^2}\; -\; \frac{a_0}{2}\;}
\qquad\Longleftrightarrow\qquad (2g_{\rm bar}+a_0)^2 - (2g_{\rm obs})^2 = a_0^2$$
- **Status:** EXACT. **Novelty: CREDITED** — this is verbatim Milgrom 1999's $2\pi\Delta T$ vacuum expression (machine-verified); the framework-new content is the two welds: (i) the floor $a_0/2$ **is** the Herglotz measure's cut edge ($|t|=\tfrac14 \leftrightarrow \omega_{\rm edge}=a_0/2c$) — thermal floor ≡ spectral gap; (ii) the floor sits $2Z\approx11.58$ below the framework's own dS scale $cH_\Lambda$ — an honest structural tension carried, not hidden.
- **Chain:** solve the law (a quadratic in $g_{\rm bar}$); complete the square. Algebraically the SAME identity as the a₀-line (verified: hyperbola ≡ −4 × a₀-line).
- **Enables:** catastrophe-free $g_{\rm bar}$-from-$g_{\rm obs}$ in any estimator (no cancellation of near-equal squares); the dS-Unruh temperature-excess reading $k_B[T_{\rm eff}-T_*]=\hbar g_{\rm bar}/(2\pi c)$, $T_*=T_{\rm dS}/(2Z)$.
- **Test:** internal (use in E3, E10); the floor-vs-horizon $2Z$ tension is a standing theory target. (`s2_thermal_identities.py`)

### E3 — The zero-fit baryon-mass predictor + velocity a₀-line + exact BTFR
$$\boxed{\;M_{\rm bar}(<r) = \frac{r^2}{2G}\left(\sqrt{a_0^2 + 4v^4/r^2}\; -\; a_0\right)\;}$$
$$\boxed{\;v_{\rm obs}^4(r) - v_{\rm bar}^4(r) = a_0\, G\, M_{\rm bar}(r)\quad\text{(exact at every radius)}\;}
\qquad \boxed{\;v^4 = GMa_0 + \left(\frac{GM}{r}\right)^{\!2}\ \text{(point mass)}\;}$$
- **Status:** law EXACT; spherical-equivalent $M$ for disks approximate (geometry factor ~1.1–1.3, flagged). **Novelty: KEEP-CREDITED** — the inversion inside is Milgrom-1999 content; the per-radius velocity identity and the exact $(GM/r)^2$ finite-radius BTFR correction are IF-specific corollaries not found written.
- **Chain:** E2 with $g_{\rm obs}=v^2/r$, $g_{\rm bar}=GM/r^2$.
- **Enables:** predict a galaxy's baryonic mass from kinematics + $a_0$ alone, zero free parameters; the BTFR "curvature" at high mass is *predicted*, not fitted — the correction term is exactly the Newtonian $(GM/r)^2$.
- **Test:** SPARC fire (10 most extended Q=1 galaxies, outermost point): median $M_{\rm pred}/M_{\rm phot}$ = **1.15 canonical / 0.97 alternate** (16–84%: ~0.8–2.3); order-unity zero-fit agreement, tails (NGC 2841 at 2.9) are the classic distance/M-L cases; not footing-diagnostic. (`eqbook_S1_algebraic.py`, `eqbook_quickfire_sparc.py`)

---

## SEAM S8 — ESTIMATOR IDENTITIES (nuisance parameters cancelling exactly)

### E4 — The pair estimator (distance-free AND inclination-free a₀)  *(11/12)*
With pure observables $R_{12} = (v_{{\rm los},1}/v_{{\rm los},2})^4\,(\theta_2/\theta_1)^2$:
$$\boxed{\;\frac{a_0}{\Upsilon} = \frac{s_1^2 - R_{12}\, s_2^2}{R_{12}\, s_2 - s_1}\;}\ \ \text{(disk-dominated, $s_j$ = photometric shape)}
\qquad \boxed{\;a_0 = \frac{g_1^2 - R_{12}\, g_2^2}{R_{12}\, g_2 - g_1}\;}\ \ \text{(gas-dominated: $D$, $i$, $\Upsilon_*$ ALL cancel)}$$
- **Status:** EXACT given the law (real-data systematics: asymmetric drift, warps, non-circular motions). **Novelty: KEEP-NOVEL** — no two-point ratio $a_0$ estimator found; standard practice fits $D,i$ as nuisances. Verified by blind `sp.solve` elimination: unique solution, $D$ and $\sin i$ structurally absent.
- **Chain:** the law at two radii is linear in $a_0$; take the ratio, eliminate. Exists only because the law is quadratic — the same elimination for McGaugh's $\nu$ is transcendental.
- **Derived conditioning fact (honest):** deep-deep pairs are singular ($R\to g_1/g_2$, denominator → 0); well-conditioned only for pairs **straddling $y=1$** — so the fully-Υ-free gas variant is ill-conditioned in practice (SPARC: 2 usable pairs, shown failing, not hidden).
- **Enables:** $a_0$ with no distance ladder and no inclination; feeds the Hubble chain (E7).
- **Test:** SPARC fire: 10,196 straddling pairs → median $\hat a_0 = 1.5\times10^{-10}$ (16–84%: 0.7–3.3e-10) — brackets both footings. A deliberate 20% distance error shifts the estimator by <1e-12 relative on real data: **exact D-cancellation confirmed numerically**. Forward: Cepheid/TRGB-anchored galaxies calibrate the non-circular systematic since $D$ cancels. (`eqbook_S8_estimators.py`, `eqbook_quickfire_sparc.py`)

### E5 — The three-radius consistency polygon (tests the LAW itself, no parameters at all)
$$\boxed{\;(s_1^2 - R_{12}s_2^2)(R_{23}s_3 - s_2) \;=\; (s_2^2 - R_{23}s_3^2)(R_{12}s_2 - s_1)\;}$$
- **Status:** EXACT. **Novelty: KEEP-NOVEL.**
- **Chain:** E4 at radii (1,2) must equal E4 at (2,3); cross-multiply.
- **Enables:** a pure-observable identity that must hold with **no** $a_0$, no Υ, no D, no i — a falsifiable test of the functional form itself, per galaxy.
- **Test:** any three well-measured radii per SPARC/WALLABY galaxy; residual distribution vs zero. (`eqbook_S8_estimators.py`)

### E6 — Per-radius kinematic distance + inclination estimator
$$\boxed{\;D = \frac{v_{\rm los}^2}{\sin^2 i\;\theta\,\sqrt{g_{\rm bar}(g_{\rm bar}+a_0)}}\;}\qquad
\boxed{\;\sin^2 i = \frac{v_{\rm los}^2}{D\,\theta\,\sqrt{g_{\rm bar}(g_{\rm bar}+a_0)}}\;}$$
- **Status:** EXACT given the law. **Novelty: KEEP-NOVEL** (BTFR distances known — McGaugh, credited; the per-radius closed form not found).
- **Chain:** invert the law for the nuisance.
- **Enables:** constancy-of-$D$-across-radii as a new per-galaxy consistency test (the BTFR-distance's per-radius generalization); inclinations for face-on gas-rich galaxies.
- **Test:** SPARC per-galaxy $D(r)$ flatness; compare against Cepheid/TRGB anchors. (`eqbook_S8_estimators.py`)

---

## SEAM S5 — EXTERNAL FIELD EFFECT (postulate-dependent: θ₀ = √2 DC-weight kernel, BASELINE_ACTION.md)

### E7 — The EFE cubic and the attenuated a₀-line  *(11/12)*
With $x = g_{\rm obs}/a_0$, $b = g_{\rm bar}/a_0$, $e = \sqrt2\, g_{\rm ext}/a_0$:
$$\boxed{\;x^3 + e\,x^2 - b(b+1)\,x - b^2 e = 0\;}\qquad\Longleftrightarrow\qquad
\boxed{\;g_{\rm obs}^2 - g_{\rm bar}^2 \;=\; a_0\, g_{\rm bar}\cdot\frac{g_{\rm obs}}{g_{\rm obs} + \sqrt2\, g_{\rm ext}}\;}$$
Corollaries (all sympy-verified):
$$\text{half-quench: } \sqrt2\,g_{\rm ext} = g_{\rm obs}\ \Rightarrow\ \text{MOND excess exactly halved}
\qquad\quad \chi \equiv \left.\frac{dg_{\rm obs}}{d(\sqrt2 g_{\rm ext})}\right|_{0} = -\frac{1}{2(1+g_{\rm bar}/a_0)}\ \xrightarrow{\ \rm deep\ }\ -\frac12$$
- **Status:** EXACT given θ₀ = √2 (postulate-dependent, flagged); scalar/aligned composition per the framework's own usage; direction-blind — consistent with pure-MI zero directional asymmetry. **Novelty: KEEP-NOVEL-CONDITIONAL** (no closed EFE cubic found; genre prior art to cite: Famaey–McGaugh 2012 1D EFE, Chae–Milgrom 2022 Eq 15, Zonoozi+ 2021 fitting functions; the external-dominated limit recovers Milgrom's known $G_{\rm eff}=G/\mu$ — credited, not claimed). Unique positive root in closed trig-Cardano form, verified against the unsquared balance; re-derived by resultant elimination.
- **Chain:** the framework's worldline EFE kernel adds $\sqrt2 g_{\rm ext}$ at DC; eliminate the auxiliary radical.
- **Enables:** the a₀-line generalizes to environment by an exact attenuation factor — measured slope $a_{0,\rm eff} = a_0\langle g_{\rm obs}/(g_{\rm obs}+\sqrt2 g_{\rm ext})\rangle$. Worked numbers (canonical): MW-like $g_{\rm ext}=2\times10^{-11}$ quenches the MOND boost 90/55/18% at $g_{\rm bar}=10^{-12}/10^{-11}/10^{-10}$.
- **Test:** Chae-style samples — slope vs $|g_{\rm ext}|$ with the exact attenuation factor; one parameter, falsifiable; deep-limit susceptibility $-\tfrac12$ is a sharp number. (`eqbook_S5_efe.py`)

---

## SEAM S3 — COSMOLOGICAL WELDS

### E8 — The triangle and Pythagorean welds (the consistency polygon)
$$\boxed{\;H_0\sqrt{\Omega_\Lambda} = \frac{Z a_0}{c}\;}\qquad
\boxed{\;H_0^2 = \left(\frac{Z a_0}{c}\right)^{\!2} + \frac{8\pi G}{3}\rho_{m0}\;}\qquad
\Lambda = \frac{3 Z^2 a_0^2}{c^4}$$
- **Status:** EXACT given the premise (flat FRW + definitions). **Novelty: KEEP-CREDITED (downgraded by verify)** — the $a_0\sim cH_0$ coincidence is Milgrom's (1983/1999); McGaugh 2020 is prior art for ladder-free $H_0$ from galaxy kinematics; the definite coefficient $1/Z$ and the estimator chain are the framework's.
- **The circularity, documented:** the canonical $a_0$ is Planck-defined, so "canonical + Planck $\omega_m = 0.1430$ → $H_0 = 67.38$, $\Omega_\Lambda = 0.6850$" is **input-recovery, not prediction**. The chain is predictive ONLY when $a_0$ enters distance-free from galaxies (E4): rotation-curve shapes + CMB $\omega_m$ → $H_0$ with no distance ladder anywhere. Alternate footing → 77.2 km/s/Mpc (fork shown).
- **Enables:** a consistency polygon where galaxy + CMB + SNe data must intersect; maps the Hubble tension onto an 8.3% $a_0$ split (Planck → 9.36e-11, SH0ES → 1.014e-10) — few-percent galactic $a_0$ arbitrates it inside this framework.
- **Test:** E4 on gas-rich straddling pairs (distance-free $\hat a_0$) + Planck $\omega_m$ → compare $H_0$ against both ladder camps. (`eqbook_S3_welds.py`)

### E9 — The CPL bump closed form (declining footing only)
$$\boxed{\;z_{\rm pk} = -\frac{1+w_0}{1+w_0+w_a}\;}\qquad
\frac{a_0(z_{\rm pk})}{a_0(0)} = \left[\left(\frac{w_a}{1+w_0+w_a}\right)^{3(1+w_0+w_a)} e^{3(1+w_0)}\right]^{1/2}$$
- **Status:** EXACT given CPL + the declining $\sqrt{\rho_{\rm DE}}$ footing. **Novelty: KEEP-NOVEL-CONDITIONAL.**
- **Chain:** $a_0(z)\propto\sqrt{\rho_{\rm DE}(z)}$ with CPL $w(z)$; extremize.
- **Enables:** a **footing discriminator**: declining footing + DESI-class $(w_0,w_a)$ → $z_{\rm pk}=0.41$ with a +6.3% $a_0$ bump; the RISING footing is monotonic — no bump.
- **Test:** high-z RAR/BTFR samples (JWST/DESI era) bracketing $z\approx0.4$. (`eqbook_S3_welds.py`)

### E10 — The memory-time weld (footing-free)
$$\boxed{\;\tau_{\rm mem}\, H_\Lambda = 2Z \approx 11.58\;}\qquad \tau_{\rm mem} = \frac{2c}{a_0} = \frac{2Z}{H_0\sqrt{\Omega_\Lambda}} = 203\ /\ 168\ \text{Gyr (canonical/alt)}$$
- **Status:** EXACT, framework-internal. **Novelty: KEEP** (weld). The memory time is $2Z$ horizon times — a pure-$Z$, footing-free statement.
- **Enables/Test:** consistency weld; sets the scale for E13's time-domain tail. (`eqbook_S3_welds.py`, `s2_thermal_identities.py`)

---

## SEAM S2 — THERMAL / UNRUH WELDS

### E11 — The thermal a₀-line (temperature-squared statement)
$$\boxed{\;(c\,\kappa_{\rm eff})^2 - (cH_\Lambda)^2 = g_{\rm bar}^2 + a_0\, g_{\rm bar}\;}\qquad
\left(\frac{T_{\rm eff}}{T_{\rm dS}}\right)^{\!2} = 1 + \frac{y(y+1)}{Z^2}\qquad
\frac{\kappa_{\rm eff}(a_0)}{H_\Lambda} = \sqrt{1+\frac{1}{Z^2}} = 1.01481$$
- **Status:** EXACT. **Novelty:** the Pythagorean pole $\kappa_{\rm eff}=\sqrt{H^2+(a/c)^2}$ is **CREDIT-NOT-CLAIM** (Milgrom 1999 Eqs 6–7 via Deser–Levin 1997 / Narnhofer–Peter–Thirring 1996); the a₀-line-as-$\Delta T^2$ rewrite and the welds are the framework's — **KEEP (welds)**.
- **Enables/Test:** consistency welds only — Unruh temperatures unmeasurable at these accelerations. Honest label: not tests. (`s2_thermal_identities.py`)

---

## SEAM S4 — KERNEL / SPECTRAL (the published Herglotz measure)

### E12 — The memory function in closed form  *(framework-internal novelty; Reading-B convention flagged)*
With $b = s/\tau_{\rm mem}$, $\tau_{\rm mem}=2c/a_0$ ($J$ = Bessel, $H$ = Struve):
$$\boxed{\;\Gamma(s) = \frac{1}{\tau_{\rm mem}}\int_{b}^{\infty}\frac{J_1(x)}{x}dx
= \frac{1}{\tau_{\rm mem}}\left[1 + J_1(b) - b J_0(b) - \frac{\pi b}{2}\big(J_1(b)H_0(b) - J_0(b)H_1(b)\big)\right]\;}$$
- **Status:** EXACT given the published unique measure; convention $z = c^2\Box_u/a_0^2$; kernel of the operator (Reading B) representation — reading-dependence inherited and flagged. **Novelty: KEEP** — the framework's time-domain kernel was never written anywhere; standard MOND has no unique measure so no such object exists there. Verified end-to-end: $\mathcal{L}[\Gamma_{\rm closed}](\lambda) = 1 - K(\lambda^2)$ (one-shot Laplace closure, independent route).
- **Physical content (all exact):** $\Gamma(0) = a_0/2c = 1/\tau_{\rm mem}$ — the memory amplitude IS the cut edge; $\int_0^\infty \Gamma\,ds = 1$ — **the v11 sum rule is unit total memory weight**; tail $\Gamma \sim -\tau_{\rm mem}^{-1}\sqrt{2/\pi}\, b^{-3/2}\sin(b - 3\pi/4)$: power-law (not exponential) memory, oscillation period $2\pi\tau_{\rm mem} \approx 1275/1056$ Gyr (canonical/alt).
- **Enables:** direct time-domain/secular integrations (wide-binary, cluster-orbit, cosmological drift) without frequency-domain detours; any kernel deformation must preserve $\int\Gamma = 1$.
- **Test:** theory-internal instrument; feeds any future secular computation. (`s4_kernel_spectral.py`)

### E13 — Unitarity circle, phase-lag law, spectral dichotomy  *(Reading-B, NOT endorsed phenomenology)*
$$K = \frac{\sqrt{4W^2-1} + i}{2W},\quad |K| = 1\ \text{exactly}\ (W = c\omega/a_0 > \tfrac12)\qquad
\boxed{\;\varphi(\omega) = \arcsin\!\frac{a_0}{2c\,\omega}\;}\qquad 2\omega\,{\rm Im}K = \frac{a_0}{c}$$
**Dichotomy at the edge:** $\omega > a_0/2c$ → pure phase ($|K|=1$); $\omega < a_0/2c$ → purely dissipative (${\rm Re}K = 0$).
- **Status:** EXACT given Reading B. **Flag (honest):** the drift channel $2\omega\,{\rm Im}K = a_0/c$ (laneK's, credited) is already excluded ~250–500× at planets; these are exact consequences of the operator reading, not endorsed phenomenology; under gated Reading C suppressed by the ~Myr corner. Wide-binary numbers: $\varphi = 10^{-7}$–$10^{-6}$ rad.
- **Novelty: KEEP** as framework-internal structure. (`s4_kernel_spectral.py`)

### E14 — The inverse-moment family (sum-rule generalization)
$$\boxed{\;M_p \equiv \int\frac{d\mu(t)}{|t|^p} = \frac{2^{2p-2}\,\Gamma(\tfrac32 - p)}{\sqrt{\pi}\,(2p-1)\,\Gamma(2-p)},\qquad p\in(\tfrac12,\tfrac32)\;}$$
- **Status:** EXACT from the unique measure; verified at untested $p = 0.55, 0.9, 1.45$ (independent route). **Novelty: KEEP-NOVEL** (framework-internal).
- **Content:** $M_1 = 1$ recovers the v11 sum rule; region-B share $2/\pi$ re-derived; endpoint divergences land exactly on the region-B tail ($p\to\tfrac12^+$) and the cut edge ($p\to\tfrac32^-$ — the same $a_0/2c$ edge as E2's floor).
- **Enables:** a one-parameter kernel fingerprint — any future deformation must reproduce ALL $M_p$, not just $M_1$. (`s4_kernel_spectral.py`)

---

## SEAM S6 — DISFORMAL LENSING (deflecting field = the RAR field, forced by UNIFICATION U2)

### E15 — The deflection closed form (complete elliptic E)  *(headline, 19/20)*
$$\boxed{\;\alpha(b) = \frac{4GM}{c^2 b}\,\sqrt{1+u^2}\;E\!\left(\frac{1}{1+u^2}\right),
\qquad u = \frac{b}{r_M},\quad r_M = \sqrt{GM/a_0}\;}$$
- **Status:** EXACT within weak-field, thin-lens, spherical (closure-pinned), isolated (no-EFE); off-sphere inherits gap A. **Novelty: KEEP-NOVEL** — verified twice by independent routes ($r = b\cosh t$ parametrization, sqrt cancels analytically, matches to <1e-25). Genre credit: Mortlock & Turner 2001 (piecewise forms + the deep-MOND asymptote $\alpha_\infty = 2\pi\sqrt{GMa_0}/c^2$, theirs); **Zhao–Bacon–Taylor–Horne 2006** derived an analytic TeVeS point-lens deflection for the standard $\mu$ (verify-pass amendment) — the elliptic-E form for THIS $\mu$ remains unfound.
- **Chain:** the framework's $\nu$ makes $g_{\rm obs} = \sqrt{GMa_0}\,\sqrt{r_M^2+r^2}/r^2$ algebraic — that is what turns the LOS integral elliptic. Limits exact: $b \ll r_M$ → Einstein $4GM/c^2 b$; $b \gg r_M$ → $\alpha_\infty$.
- **The new approach law (an $a_0$-estimator from lensing shape):**
$$\alpha(b) = \alpha_\infty\left[1 + \frac{r_M^2}{4b^2} + O(u^{-4})\right]$$
- **Numbers:** $M = 10^{11} M_\odot$: $r_M = 12.2/11.1$ kpc, $\alpha_\infty = 0.508''/0.558''$ (canonical/alt).
- **Test:** stacked galaxy–galaxy lensing (KiDS/DES/Euclid) around isolated galaxies — the $+r_M^2/4b^2$ approach term is the falsifiable shape signature. (`s6_lensing_closed_form.py`)

### E16 — The mass-line / mass hyperbola (the lensing Σ-line analog)  *(19/20)*
Point mass: $M_{\rm eff}(r) = g_{\rm obs}r^2/G = M\sqrt{1+(r/r_M)^2}$ (exact hyperbola). General spherical system, exact at every $r$:
$$\boxed{\;G\left[M_{\rm eff}(r)^2 - M_b(r)^2\right] = a_0\, M_b(r)\, r^2\;}$$
- **Status:** EXACT (any spherical system; symbolic with arbitrary $M_b(r)$). **Novelty: KEEP** — algebra trivial, framing novel; the value is the **equal-slope consistency test**: because the disformal $B$ is fixed by the same kernel, the framework REQUIRES lensing mass-line slope = kinematic a₀-line slope EXACTLY. MG theories with independent lensing sectors need not pass this.
- **Enables:** the a₀-line in mass coordinates usable with deprojected lensing masses: plot $G(M_{\rm eff}^2 - M_b^2)/M_b$ vs $r^2$ → line through origin, slope $a_0$, zero fit parameters.
- **Test:** SPARC fire (175 galaxies / 3389 points, read-only): robust median $\hat a_0 = 1.40/1.05/0.81/0.63\times10^{-10}$ at $\Upsilon = 0.5/0.6/0.7/0.8$ — brackets BOTH footings inside physical M/L; **non-diagnostic between footings** (as the banked RAR audit requires; no win, no deficit). Forward: weak-lensing $M_{\rm eff}$ vs kinematic $a_0$-line on the same systems. (`m2_massline_sparc_fire.py`)

### E17 — The phantom halo and its projection: the (K,E) elliptic pair
$$\boxed{\;\rho_{\rm ph}(r) = \frac{\sqrt{GMa_0}}{4\pi G}\,\frac{1}{r\sqrt{r^2 + r_M^2}}\;}\qquad
\boxed{\;\Sigma_{\rm ph}(b) = \frac{\sqrt{GMa_0}}{2\pi G}\,\frac{K(m)}{\sqrt{b^2 + r_M^2}},\quad m = \frac{1}{1+u^2}\;}$$
- **Status:** EXACT (same construction flags as E15). **Novelty: KEEP-NOVEL-for-this-IF** — phantom-density concept is Milgrom's (credited, e.g. arXiv:0709.2561 / 2009 rings-shells); these closed forms and the (K,E)-pair structure unfound. Closure $dM_{2D}/db = 2\pi b\,\Sigma_{\rm ph}$ machine-verified symbolically; re-verified by independent Abel projection + finite difference.
- **Content:** the framework's "dark halo" of a point mass: inner **1/r cusp** (not NFW, not cored) rolling to exact isothermal $1/r^2$ at $r \gg r_M$; the convergence's modulus $m$ is the SAME as the deflection's — deflection and convergence are one elliptic system.
- **Test:** strong+weak lensing profile fits around isolated compact masses — a falsifiable alternative template to NFW. (`s6_lensing_closed_form.py`)

---

## SEAM S7 — CLUSTER THROTTLE (POSTULATE-DEPENDENT: Branch-B y_c = Z/2; uncut MI has NO throttle)

### E18 — The throttle line + a₀-line saturation
Above the kink ($y > y_c = Z/2$, depletion $n=1$), with $D \equiv g_{\rm obs} - g_{\rm bar}$:
$$\boxed{\;g_{\rm bar}\, D\,(D + Z a_0) = \frac{Z^2}{4}\, a_0^3\quad(\text{y-independent, zero-fit})\;}$$
In the a₀-line plane: $Y = a_0 X$ exactly below the kink; above it
$$\boxed{\;Y_\infty = \frac{Z}{2}\,a_0^2 = a_0\, g_{\rm kink}\quad\text{(the a₀-line goes exactly horizontal)}\;}
\qquad \text{general } n:\ (g_{\rm obs}-g_{\rm bar})\,g_{\rm bar}^n \to \frac{y_c^n\, a_0^{n+1}}{2}$$
- **Status:** EXACT given Branch-B (flagged; located targets, NOT detections — the y_c paper's own 0.5–0.6σ SPARC indistinguishability and the 4–6× BCG-M/L systematic stand). **Novelty: KEEP-CONDITIONAL**; verified with fresh symbols at 6 random $y$.
- **Enables:** the cluster signature drawn in the archetype's own plane — a saturating a₀-line is the throttle's fingerprint.
- **Test:** cluster RAR samples spanning the kink; the saturation level is parameter-free given $a_0$. (`s7_throttle_closed_form.py`)

### E19 — The kink landmark: a direct Λ-meter (Z cancels)
$$\boxed{\;g_{\rm kink} = y_c\, a_0 = \frac{cH_\Lambda}{2} = c^2\sqrt{\frac{\Lambda}{12}}\;}
\qquad\Longleftrightarrow\qquad \Lambda = \frac{12\, g_{\rm kink}^2}{c^4},\quad H_\Lambda = \frac{2 g_{\rm kink}}{c}$$
- **Status:** EXACT given Branch-B. **Novelty: CREDITED** — the $g_{\rm bar} = a_0 V/2$ kink statement is already in the y_c paper (ELASTIC_MEDIUM_YC_Z2_2026.md); the $\Lambda$-inversion packaging is the new frame.
- **Numbers:** $g_{\rm kink} = 2.709\times10^{-10}\ /\ 3.271\times10^{-10}$ m/s² (canonical/alt; matches TARGET_SPEC).
- **Companions (new, all exact given Branch-B):** slope break at the kink $(Z+1)/(Z+2) = 0.8716 \to 0.7337$ ($n=1$, $\nu_c = \sqrt{1+2/Z}$) / $0.5958$ ($n=2$): break invariants $\Delta = -0.1379/-0.2749$ **pure-Z, footing-free**; peak landmark $y_* = 6.06/5.24$ at $0.0170/0.0264$ dex; Hernquist-BCG kink radius $r_{\rm kink} = \sqrt{2GM_{\rm BCG}/(cH_\Lambda)} - a_H$ = 9.4 kpc for $M_* = 5\times10^{11}M_\odot$ (TARGET_SPEC's 9.5 reproduced).
- **Test:** the broken-RAR kink location in deep cluster/BCG data reads Λ directly with no $a_0$ and no $Z$ in it — currently below detectability (systematics 4–6× the signal), an exact target equation. (`s7_throttle_closed_form.py`)

---

## SUMMARY TABLE

| # | Equation (short) | Seam | Exact? | Novelty verdict | Test surface |
|---|---|---|---|---|---|
| E0 | a₀-line $g_o^2-g_b^2 = a_0 g_b$ | — | EXACT | CREDITED (Milgrom 1999 law) / packaging new | SPARC/WALLABY slope (robust fit only) |
| E1 | Landmark triplet (3/2 sum rule; even C; y=1: 3/4, 1/8) | S1 | EXACT | KEEP-NOVEL | hierarchical RAR slope-field |
| E2 | Floor inversion $g_b = \sqrt{g_o^2+(a_0/2)^2}-a_0/2$ | S1/S2 | EXACT | CREDITED (Milgrom ΔT) + new welds | internal; floor≡cut-edge weld |
| E3 | $M_{\rm bar}$ predictor; velocity a₀-line; exact BTFR $+(GM/r)^2$ | S1 | EXACT (sphericity flagged) | KEEP-CREDITED (corollaries new) | SPARC zero-fit masses |
| E4 | Pair estimator (D, i, Υ cancel) | S8 | EXACT | KEEP-NOVEL | straddling pairs; TRGB anchors |
| E5 | Three-radius polygon | S8 | EXACT | KEEP-NOVEL | per-galaxy law test, no parameters |
| E6 | Kinematic distance / inclination closed forms | S8 | EXACT | KEEP-NOVEL | D(r) constancy |
| E7 | EFE cubic + attenuated a₀-line + χ = −1/(2(1+y)) | S5 | EXACT given θ₀=√2 | KEEP-NOVEL-CONDITIONAL | Chae-style EFE samples |
| E8 | Hubble triangle + Pythagorean weld | S3 | EXACT given premise | KEEP-CREDITED (downgraded; circularity documented) | E4-chained ladder-free H₀ |
| E9 | CPL bump $z_{\rm pk}$ closed form | S3 | EXACT given CPL+footing | KEEP-NOVEL-CONDITIONAL | high-z RAR near z≈0.4 |
| E10 | $\tau_{\rm mem}H_\Lambda = 2Z$ | S3/S2 | EXACT | KEEP (weld) | consistency |
| E11 | Thermal a₀-line (ΔT² form) | S2 | EXACT | pole CREDITED; welds KEEP | consistency only |
| E12 | Memory function Γ(s) Bessel–Struve | S4 | EXACT (Reading-B conv.) | KEEP (framework-internal) | time-domain instrument |
| E13 | Unitarity circle; φ = arcsin(a₀/2cω); dichotomy | S4 | EXACT given Reading B | KEEP (flagged non-endorsed) | theory-internal |
| E14 | Inverse moments $M_p$ | S4 | EXACT | KEEP-NOVEL | kernel fingerprint |
| E15 | Deflection α(b) elliptic-E | S6 | EXACT (weak-field, spherical, isolated) | KEEP-NOVEL (Zhao+06 genre credited) | KiDS/DES/Euclid stacked shape |
| E16 | Mass-line; equal-slope lensing≡kinematics | S6 | EXACT (spherical) | KEEP (framing) | lensing vs kinematic slope |
| E17 | Phantom halo (K,E) pair | S6 | EXACT | KEEP-NOVEL-for-this-IF | anti-NFW template |
| E18 | Throttle cubic invariant; a₀-line saturation | S7 | EXACT given Branch-B | KEEP-CONDITIONAL | cluster RAR saturation |
| E19 | Kink Λ-meter $g_{\rm kink}=cH_\Lambda/2$ + break invariants | S7 | EXACT given Branch-B | CREDITED (kink) / companions new | broken-RAR kink (target, not detection) |

---

## REPRODUCTION (all exit 0)
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/equation_book
python3 eqbook_S1_algebraic.py        # 17 checks
python3 eqbook_S3_welds.py            # 9
python3 eqbook_S5_efe.py              # 11
python3 eqbook_S8_estimators.py       # 10
python3 eqbook_quickfire_sparc.py     # SPARC read-only, 131 galaxies
python3 s2_thermal_identities.py      # 12
python3 s4_kernel_spectral.py         # 44
python3 s6_lensing_closed_form.py     # 14
python3 s7_throttle_closed_form.py    # 22
python3 m2_massline_sparc_fire.py     # SPARC read-only, 175/3389
python3 verify_audit_2026_07_16.py    # 31 independent re-derivations
```

## STANDING CORRECTIONS CARRIED (from VERIFY.md — do not regress)
1. FIRE-2's "exact 1.500 to ~1%" is RETRACTED → "consistent within pipeline noise ($1.53\pm0.05$ law-true) at Υ=0.70"; the EIV-bias sign in the quickfire code comment is wrong (pipeline biases ABOVE 3/2, not below).
2. "Only piecewise arctan forms exist" is AMENDED for Zhao–Bacon–Taylor–Horne 2006 (TeVeS analytic point-lens for the standard μ).
3. Every law-level statement carries the Milgrom-1999 credit (Eqs 5 + 8–9, coefficient fork $2Z$); the credit cuts both ways — the framework's law has Milgrom's own dS-vacuum pedigree.
4. The Hubble chain's canonical "$H_0 = 67.4$" is input-recovery; predictive content lives only in the E4-chained distance-free route.

## WHAT THIS BOOK DOES NOT CLAIM
No derivation of $a_0$'s value or $Z$ (kappa-closure memory: postulated); no front opened or closed; no proof language; conditional entries (θ₀=√2, Branch-B, Reading-B, CPL) usable only with their flags; search absence is strong but not conclusive evidence of novelty in a 40-year literature.
