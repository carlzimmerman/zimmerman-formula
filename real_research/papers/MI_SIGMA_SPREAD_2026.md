# The Relational Velocity-Dispersion Spread: A Modified-Gravity-Impossible Signature of History-Dependent Inertia

**Carl Zimmerman**
Briar Creek Tech — carl@briarcreektech.com

*2026-07-17. This paper supersedes and corrects door D3 of "No Pump-Free Corner" (Zenodo concept DOI [10.5281/zenodo.21179352](https://doi.org/10.5281/zenodo.21179352)); see the concurrent erratum of that work. Self-cites: MI Field Theory Results 2026 ([10.5281/zenodo.21403470](https://doi.org/10.5281/zenodo.21403470)); the lensing no-go ([10.5281/zenodo.21418816](https://doi.org/10.5281/zenodo.21418816)).*

---

## Abstract

In a modified-inertia (MI) reading of the MOND phenomenology, inertia is a time-nonlocal functional of a body's own worldline: its effective response depends on its acceleration history through a causal memory kernel $K(\Box_u/a_0^2)$. We show that this history-dependence generates a *relational* signature that no modified-gravity (MG) theory of the standard class can reproduce in its field sector. For any theory that (P1) sources a gravitational field $g(x)$ from the baryons and (P2) moves tracers on weak-equivalence-principle (WEP) geodesics of a single metric built from that field, a test body's acceleration at a fixed cluster-centric position is a function of position alone — independent of how it arrived there. Consequently the *equilibrium* internal velocity dispersion of a self-gravitating subsystem, evaluated at fixed external field, carries exactly zero spread across infall history: $d\sigma_{\rm int}/d(\text{history}) \equiv 0$ — and it does so *structurally*, because the field carries no worldline/history label to differentiate. We prove this within the class $\{$QUMOND, AQUAL, AeST/TeVeS, $f(R)$, local-modified-$g\}$, for any $a_0$, any interpolation function, both coefficient footings, off-adiabatically, and under retardation. The MG-zero baseline is Milgrom's MG-virial universality (Milgrom 1983, ApJ **270**:365; 2014, MNRAS **437**:2531); the interpolation kernel $\nu(y)=\sqrt{1+1/y}$ is Milgrom's (Phys. Lett. A **253**:273, 1999, Eq. 9). The novelty is (a) the general sourced-field–WEP proof of the exact-zero off-adiabatically and under retardation, (b) the demonstration that the discriminant survives a strong-anisotropy control test and is not re-labeled velocity anisotropy, (c) a designed, degeneracy-differencing observable $D(\text{zone})$, and (d) the framework-specific prediction (the *numbers*, not the discriminating power).

We carry two coefficient footings on every dimensional number: the canonical pure-$\Lambda$ footing $a_0=cH_\Lambda/Z=9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$ (with $Z=\sqrt{32\pi/3}=5.789$), and an alternative $a_0=1.13\times10^{-10}\ \mathrm{m\,s^{-2}}$ ($\rho_{\rm total}/cH_0$). We distinguish two physical channels: a star-orbit channel within one pressure-supported system (sub-percent, deep-adiabatic, ELT-gated) and the nearer, larger cluster-member infall-phase external-field-effect (EFE) channel. For the latter we design $D(\text{zone})=\langle\ln(\sigma_{\rm int}/\sigma_{\rm bary})\rangle_{\rm zone}-\langle\cdot\rangle_{\rm ancient}$, computed within a fixed deprojected external-field bin and tagged by Rhee et al. (2017) phase-space infall zones, which differences the shared radial EFE gradient out as a common mode.

The corrected prediction is two-tiered: (i) in the MG field sector the fixed-field history spread is *exactly zero*, so any genuinely field-sector history spread is MG-impossible — theorem-grade; the observed-existence claim, however, is confound-contingent, because ordinary non-equilibrium dynamics (violent relaxation, tidal shocking, incomplete phase-mixing) produce fixed-field, history-correlated spreads in Newton+dark-matter and MG alike, and must be separated by design, not asserted by the theorem. (ii) The leading sign, in the first-infall pre-pericentre zone, is that first-infall members run **hotter** than matched long-resident members — structural and timescale-free for any positive-averaging or pure-delay causal kernel, robust across a $0/125$ orbit scan; this inverts and supersedes the backwards, dated pericentre sign-flip of the earlier D3. The magnitude is **kernel-hostage**: at the framework-committed memory time it ranges from $\sim1.3\%$ (low-pass reading) to $\sim8$–$13\%$ (pure-delay $|K|=1$ reading) in the fixed-field $\ln(\sigma_{\rm int}/\sigma_{\rm bary})$ contrast, and is not pinned by the de Sitter–Unruh foundation. At the low end this sits at or below the observable's own $\sim1$–$2\%$ projection and $\sim2$–$8\%$ tidal systematic floors. The signature is **MI-class-generic** — it separates any history-dependent inertia from modified gravity, but not this framework from Milgrom's linear no-EFE MI (arXiv:2503.07106), which also spreads — and it does **not** test $a_0$'s value or the sign postulate $s=-1$ (both postulates; the leading sign rides on $s=-1$). This is a prediction-and-methods paper for a designed, currently-underpowered discriminator, honest in both directions: it manufactures neither a detection nor a deficit.

---

## 1. Introduction

The MOND regularity — that galaxy rotation curves and pressure-supported dispersions follow from the baryons alone through a single acceleration scale $a_0$ — admits two very different microphysical readings. In **modified gravity** (MG), the baryons source a modified gravitational field and matter falls freely in it: the extra physics lives in the field equation. In **modified inertia** (MI), the field equation is unchanged and the extra physics lives in the response of matter to force — inertia itself becomes a functional of the body's motion. These readings are notoriously hard to separate. For settled, phase-mixed systems they are engineered to coincide on the radial acceleration relation, and most historically proposed discriminants (rotation-curve shapes, the baryonic Tully–Fisher relation, the RAR scatter, weak-lensing profiles) turn out to be either shared between the two classes or degenerate with the same nuisance parameters.

The framework studied here is a de Sitter–Unruh modified-inertia completion in which the acceleration scale is horizon-derived, $a_0=cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}=5.789$, giving the canonical value $a_0=9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$; the framework's own de Sitter–Unruh interpolation is $g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}\,a_0}$, i.e. $\nu(y)=\sqrt{1+1/y}$ with $y=g_{\rm bar}/a_0$. This interpolation kernel is *identical* to Milgrom's (Phys. Lett. A **253**:273, 1999, Eq. 9; astro-ph/9805346); the framework's distinctive content is the $cH_\Lambda/Z$ coefficient and a covariant MI completion in which the inertial response is a retarded, time-nonlocal functional of the body's own 4-acceleration through a kernel $K(\Box_u/a_0^2)$ with an exact memory time (MI Field Theory Results 2026, [10.5281/zenodo.21403470]). Throughout, we carry **two coefficient footings** on every dimensional number. (A "footing" is the choice of which cosmological rate normalizes $a_0$: the pure-$\Lambda$ dark-energy rate $cH_\Lambda$, canonical, giving $a_0=9.36\times10^{-11}\ \mathrm{m\,s^{-2}}$; versus the total-density rate $cH_0$, alternate, giving $a_0=1.13\times10^{-10}\ \mathrm{m\,s^{-2}}$.) We state plainly at the outset, and repeat throughout: $a_0$'s value and the response sign $s=-1$ are **postulates** of the framework, not derived here, and nothing in this paper tests them.

The discriminability question has recently sharpened. A companion analysis (the lensing no-go, [10.5281/zenodo.21418816]) closed gravitational lensing as a discriminator: in the framework's disformal construction the lensing observables become shared with the MG (AeST-class) realization, so lensing does not separate MI from MG. That closure removes one of the few candidate handles and makes the search for a *genuinely* MG-impossible observable more pressing. This paper reports one — with the caveat, developed below, that the impossibility is airtight in the MG *field sector* and that the *observable* existence claim must beat same-signed dynamical confounds by design.

The idea rests on the definitional difference between the two classes. If inertia is history-dependent, then a self-gravitating subsystem's internal velocity dispersion depends on the subsystem's acceleration history — two otherwise-identical subsystems sitting at the same place, having arrived by different paths, carry different effective inertia and therefore different internal heat. If, instead, the extra physics lives in a sourced field and matter moves on WEP geodesics of it, then a body's acceleration at a fixed position is fixed by *where it is*, not *how it got there*, and the field-sector history spread vanishes identically. The MG-zero side of this statement is not new in spirit: it is Milgrom's MG-virial universality (Milgrom 1983, ApJ **270**:365; 2014, MNRAS **437**:2531), the fact that in field-based MOND the internal dynamics of a subsystem are set by its instantaneous configuration and environment. What is new here is (a) a general proof that the exact-zero holds for the entire sourced-field–WEP class off-adiabatically and under retardation, not just for a specific Lagrangian; (b) the demonstration that the resulting discriminant survives a strong-anisotropy control test and is therefore not re-labeled velocity anisotropy; (c) a specific designed observable that differences out the shared, degenerate radial gradient; and (d) the framework-specific prediction of magnitude and leading sign — the numbers, not the discriminating power, which is MI-class-generic.

We are honest in both directions throughout, because both directions are load-bearing. The MG-impossibility is airtight where it is airtight — in the field sector at fixed *true* external field — and we label it a theorem there and nowhere else. The detection, by contrast, is currently out of reach: the magnitude is small and kernel-hostage, the confounds are same-signed, and the datasets that carry the signal do not yet exist at the required size. This is a prediction-and-methods paper. It manufactures neither a detection nor a deficit.

---

## 2. Mechanism and the MG-impossibility theorem

### 2.1 History-dependent inertia versus instantaneous EFE

In the covariant MI completion, the inertial response of a body is not a local function of its instantaneous 4-acceleration $a^\mu$ but a causal functional of its worldline through the kernel $K(\Box_u/a_0^2)$, where $\Box_u$ is the d'Alembertian along the worldline. The kernel has an exact, footing-free memory time (equation-book E10):
$$
\tau_{\rm mem} = \frac{2c}{a_0} = \frac{2Z}{H_\Lambda}, \qquad \tau_{\rm mem} H_\Lambda = 2Z = 11.58 \ \text{(exact, footing-free)},
$$
which evaluates to $\tau_{\rm mem}=203\ \mathrm{Gyr}$ (canonical) / $168\ \mathrm{Gyr}$ (alt). Physically, the body's effective inertia at time $t$ is a memory-weighted functional of the force it has felt over the preceding $\sim\tau_{\rm mem}$. Because $K$ is causal, the memory-felt loading lags the instantaneous loading.

Modified gravity has no such object. In QUMOND, AQUAL, AeST/TeVeS, and $f(R)$, the extra physics is a modification of the field equation for $g(x)$; a tracer's acceleration is $a=g(x(t))$, the sourced field evaluated at the tracer's current position. The field carries no $d/dt(\text{worldline})$ label. Two tracers at the same position, with different histories, feel identical $g$.

The **external field effect (EFE)** exists in both classes and is the cleanest place to see the difference. A subsystem (a galaxy) falling into a larger system (a cluster) feels the cluster's external field $g_{\rm ext}$, which loads (suppresses) the subsystem's internal MOND boost. In MG this loading is *instantaneous*: the internal dynamics are set by the current $g_{\rm ext}=g_{\rm ext}(\text{position})$. In MI the loading is a memory-weighted functional of the subsystem's $g_{\rm ext}$-history along its infall orbit, governed by the two-frequency subsystem boost $\theta(y)$, $y=\omega_{\rm ex}/\omega_{\rm in}$ (Milgrom 2022, Phys. Rev. D **106**:064060). At *fixed current* $g_{\rm ext}$, MI predicts a spread across infall phase; the MG field sector predicts none.

### 2.2 The sourced-field–WEP proof: $d\sigma_{\rm int}/d(\text{history})=0$

Define the MG class by two premises:

- **(P1)** the theory *sources a field* $g(x)$ from the baryons (elliptic quasi-static, or hyperbolic/retarded in general);
- **(P2)** matter tracers are *WEP geodesics* of the single Jordan metric built from that field: a tracer's acceleration at event $x$ is a function of $x$ (and, with retardation, of the *source's* past light cone) — independent of the tracer's own orbit, velocity, or acceleration history.

Under (P2), the orbit shape, the infall phase $y=\omega_{\rm ex}/\omega_{\rm in}$, and the velocity $v$ all label the *tracer*, and they appear nowhere in the equations for the internal dynamics. Hence

> **Theorem (MG field-sector history spread vanishes).** Under (P1)–(P2), the equilibrium internal velocity dispersion of a self-gravitating subsystem, evaluated at fixed gravitational field and fixed internal baryons, is independent of the subsystem's orbital/infall history:
> $$
> \frac{\partial\sigma_{\rm int}}{\partial y}\equiv 0,\qquad \frac{\partial\sigma_{\rm int}}{\partial v}\equiv 0,\qquad \frac{\partial\sigma_{\rm int}}{\partial(\text{history})}\equiv 0,
> $$
> identically, for any $a_0$, any interpolation function, both coefficient footings, elliptic or retarded field equations, and off-adiabatically. *The zero is structural: under (P2) no worldline/history variable enters the internal dynamics, so there is no argument to differentiate. The hypotheses hold for QUMOND, AQUAL, AeST/TeVeS, $f(R)$, and any local-modified-$g$ theory. The sole evasion — a coupling to the tracer's own velocity/worldline — violates (P2) and is itself modified inertia.*

This is verified symbolically with an arbitrary interpolation $\mu$ and arbitrary $a_0$, and numerically across $\{$canonical, alt$\}\times\{$framework $\nu$, standard-MOND $\nu$, exponential-RAR$\}$: four orbit families matched at the same position return an identical internal boost, with peak-to-peak spread $=0$ exactly. We stress that the symbolic zero is *structural*, not a surprising computation — the algebraic-MOND EFE simply contains no worldline/history variable to differentiate — and that structural absence is precisely the physical content: a subsystem's internal heat is fixed by *where it is*, not *how it got there*. This is Milgrom's MG-virial universality, here stated as an off-adiabatic theorem for the whole class.

Two structural checks confirm the exact-zero survives the natural loopholes:

- **Time-varying potential (off-adiabatic).** Going non-adiabatic replaces the fixed position by the worldline $x(t)$ but attaches no velocity or history label to $g$. A settled member and a deep plunger that reach the same current radius by different histories have identical MG boost. The MG field is memoryless; the infall history drops out exactly.
- **Retardation / finite crossing.** The field lag is $\sim v/c\sim3.5\times10^{-3}$; retardation lives in the *source's* past light cone and is felt identically by every member at $(x,t)$. It shifts the *mean* field at the $10^{-3}$ level but adds *zero* infall-phase family spread. (Contrast MI, whose kernel is retarded along the *tracer's own* worldline.)

MI violates (P2) by construction: the inertial response is a functional of the body's own worldline through $K(\Box_u/a_0^2)$. Two members at the same position with different orbital histories carry different effective inertia, hence a spread. That is the entire field-sector distinction.

**Scope of the theorem, stated precisely and up front.** The exact-zero is a statement about the MG *field channel* at fixed *true* 3D external field. It is *not* a claim that the total observed dispersion spread of a real, recently-infalling subsystem is zero in an MG (or a Newton+dark-matter) universe. Ordinary non-equilibrium dynamics — violent relaxation, tidal shocking, incomplete phase-mixing, ram-pressure, substructure — produce fixed-field, history-correlated dispersion spreads that are entirely standard and are *not* modified inertia. They are shared dynamical confounds, same-signed with the MI excess, and they are separated (Sec. 4) by radial profile and sign, not by the theorem. The theorem-grade badge attaches to "the MG field-sector contribution to the fixed-field history spread is exactly zero," not to "any measured fixed-field spread is modified inertia." The observable existence claim of Sec. 5.1 is therefore confound-contingent — it depends on the F3 radial-profile separator holding — and is *not* itself theorem-grade.

### 2.3 The anisotropy control test (star-orbit channel)

The obvious worry is that a "spread across orbit families" is just velocity anisotropy $\beta(r)$ in disguise — the classic mass-anisotropy degeneracy, which lives in the angular sector of the velocity ellipsoid and is shared by Newton+dark matter, MG, and MI alike. If the MI signal were re-labeled anisotropy it would carry no discriminating power.

We tested this in the *star-orbit* channel (Sec. 3.1), where the relevant statistic is the orbit-family enclosed-mass split $d\ln M$. We built a *proper steady-state* distribution function with strongly radially-varying anisotropy — $\beta$ running from $+0.13$ in the center to $-0.72$ outward, i.e. $\Delta\beta\sim9$ between subsamples, with anisotropy a genuine function of the orbital integrals — and *no MI*. The mechanism is that MI multiplies the radial and tangential velocity components $(v_r,v_t)$ by the *same* per-orbit factor $f(e)$, which **cancels in the anisotropy ratio** $\beta=1-\langle v_t^2\rangle/(2\langle v_r^2\rangle)$ and surfaces only in the enclosed-mass normalization $M\propto f^2\sigma_r^2$. MI is orthogonal to $\beta$ by construction: anisotropy is a statement about velocity *direction*; MI acts on velocity *magnitude*.

We report the control test honestly, including its demotions from the verify lane. The pure-anisotropy DF returns a zero-point $d\ln M\approx+0.033$, which is **larger in magnitude than the MI signal itself** ($d\ln M_{\rm MI}\approx-0.02$) and of the *opposite sign*; across DF shapes the zero-point drifts $+0.009\to+0.062$. In other words, valid equilibrium anisotropy is separated from MI by *sign*, not by amplitude: the anisotropy contamination is signal-sized, and a real measurement would require a forward Schwarzschild / made-to-measure calibration whose residual is demonstrated sub-signal — which we have not done. What the test *does* establish is that strong, radially-varying, physically-valid anisotropy does not reach the MI-signed value and cannot fake the MI sign. It is a sign-immunity result, not a clean amplitude pass.

A separate and sharper practical mimic surfaced in the same lane: a radius-correlated *non-steady-state population mix* (a subsystem out of equilibrium, with the mix varying with radius) drives $d\ln M\approx-0.71$, roughly $35\times$ the MI signal and *MI-signed*. This is the dominant unguarded false-detection channel for the star-orbit statistic, and it is not beaten by the anisotropy argument — it is beaten only by an equilibrium/relaxed-population selection. We carry it forward into the confound budget (Sec. 4.4, F-table) rather than treating the discriminant as clean.

### 2.4 The one evasion is definitionally modified inertia

Is there *any* force that manufactures the orbit-family spread while remaining modified gravity? We stress-tested the boundary of the class:

- **Gravitomagnetic** $F=m\,v\times B_g$: velocity-dependent but antisymmetric, $F\cdot v\equiv0$, does no work, cannot heat a member — zero spread.
- **Dissipative drag** $F=-\gamma(x)v$: non-conservative, no medium in a collisionless system; if imposed it *cools* toward $\sigma\to0$, no steady spread; not a field theory of $g$.
- **$f(R)$ / chameleon** $G_{\rm eff}(x)$: environment-dependent coupling is a function of local density/potential, hence of $x$, shared by all tracers — spread zero.
- **Retarded MG**: retardation is in the source, felt identically by all members at $(x,t)$ — spread zero.
- **Disformal / Finsler / SME velocity-dependent coupling** $\delta a\sim\beta_c(v\cdot\nabla\phi)$: this *does* create an orbit split (e.g. $\sim9.5\%$ at $\beta_c=0.1$). But it couples to the *tracer's own velocity*, breaking (P2) and WEP — it is modified **inertia** in an MG costume. Standard MG is WEP-exact ($\beta_c\equiv0$).

The only door that opens is not an MG door. Any theory that manufactures a field-sector orbit-family spread has, by construction, made the tracer's acceleration depend on how it moves — it has put history into the *inertial* response. Whatever one names it, a finite field-sector fixed-field history spread **is** the modified-inertia signal. There is no pure sources-a-field-$g(x)$ channel to it.

---

## 3. The two channels

The history spread appears in two physically distinct places, which the banked analysis initially conflated and a session correction separated. They differ by roughly an order of magnitude in amplitude and are measured by entirely different means.

### 3.1 Channel A — star-orbit spread within one pressure-supported system

Inside a single dSph or elliptical, every star at radius $r$ feels the same $g_{\rm bar}(r)$. A *local* $\mu(|a|)$ inertia would give every star the same $|a|$ and no spread. The MI effect is non-adiabatic: a star on an *eccentric* orbit time-samples a *varying* $|a|$ (large at pericenter), so its memory-averaged effective inertia differs from that of a circular orbit at the same energy — a Jensen gap over the curvature of the nonlinear $\nu$. Different orbital families at the same radius carry different effective inertia, hence an intrinsic dispersion spread.

The magnitude is set by $\tau_{\rm mem}$ versus the orbital time $T_{\rm orb}\approx2\pi r/\sigma$. For every real pressure-supported system this ratio is enormous:

| system | $\tau_{\rm mem}/T_{\rm orb}$ (canonical) | regime |
|---|---|---|
| Draco / Sculptor / Fornax dSph | $1367\times$ / $1086\times$ / $544\times$ | deep adiabatic |
| Crater II (diffuse) | $83\times$ | deep adiabatic |
| Coma cluster members | $22\times$ | deep adiabatic |

Because $\tau_{\rm mem}=203/168\ \mathrm{Gyr}\gg T_{\rm orb}$, every orbit sits far above the kernel's edge frequency $a_0/2c=1/\tau_{\rm mem}$. On the pure-phase branch the memory magnitude *saturates and freezes* at the orbit-mean pre-history fixed point — there is **no resonant amplification**. The spread is the small residual adiabatic Jensen gap. Direct orbit integration through the real memory kernel (an independent, 19/19-verified integrator) gives an eccentric-orbit RAR offset $<0.007$ dex out to $e\approx0.9$, sign negative, and an isotropic-dSph ensemble $\nu_{\rm eff}/\nu_{\rm circ}=0.990$–$0.997$. Over realistic eccentricity distributions the RMS relational $\sigma$-spread is
$$
\text{Channel A: } \sim0.2\text{–}0.35\%\ \text{(fiducial cored dSph)},\quad \lesssim1\%\ \text{(point-mass ceiling)},\quad <0.1\%\ \text{(ellipticals, } y\gg1).
$$
Both footings agree to $<20\%$ ($a_0$ cancels at fixed depth $y$). The sign is negative: eccentric orbits present a slightly lower effective $\nu$ and run marginally cooler. This channel is real but small — an order of magnitude below the cluster channel — and, as Sec. 6 shows, needs ELT-class per-star velocities plus a per-star 3D orbit tag that does not yet exist.

### 3.2 Channel B — cluster-member infall-phase EFE spread

The nearer, larger channel is the *subsystem* EFE. A whole cluster-member galaxy's internal dispersion is loaded by the cluster external field through the two-frequency boost $\theta(y)$, $y=\omega_{\rm ex}/\omega_{\rm in}$ (Milgrom 2022). Here $y$ is the member's dimensionless internal depth: small $y$ means the member sits deep in the modified regime (a diffuse, low-internal-acceleration galaxy), and *only* diffuse low-$y$ members carry the signal. It is essential to separate two quantities that the banked notes stress repeatedly:

|  | current-configuration $\theta(y_{\rm cur})$ boost | MG-impossible history spread |
|---|---|---|
| **magnitude** | $6$–$13\%$ | $\sim1.3\%$ (low-pass) to $\sim8$–$13\%$ (pure-delay) |
| **status** | partly MG-**shared** (MG has its own instantaneous EFE) | MG-**impossible** in the field sector |
| **is it the discriminant?** | **NO** — absorbed by an $a_0$-rescale / EFE term | **YES** — this is the signal |

- **The instantaneous $\theta(y_{\rm cur})$ boost** — the *current-configuration* EFE contrast across infall phase. For a diffuse deep-MOND member ($a_{\rm in}\approx0.3\,a_0$ internal, $a_{\rm ex}\approx a_0$ external, at the transition shell) this is the banked **6–13%** band (kernel corners $\theta(0)=\sqrt2$ floor $\to5.5\%$, $\theta(0)=2$ fiducial $\to9.5\%$, $\theta(0)=e$ ceiling $\to11.5\%$ over $y\le1.5$; fiducial reproduction $9.5\%$, both footings). This is a current-configuration quantity that MG partly shares — MG has its own instantaneous $\theta_{\rm MG}(y_{\rm cur})$ EFE — and it is therefore *not* the discriminant. A constant EFE boost is absorbed by an $a_0$-rescale or an EFE term.
- **The MG-impossible history spread** — the residual spread *at fixed current field and fixed $y_{\rm cur}$*, riding on top of that boost, sourced only by the memory-weighted difference between the felt and the current external field. This is the discriminant. Its magnitude is set by $\tau_{\rm mem}$ *and by the kernel shape*, and here the framework's own foundation is genuinely underdetermined (Sec. 5.4): under a decaying **low-pass** reading of the committed E10 memory, both members lag the field nearly equally and the residual is *residence-time-limited* to $\sim1.3\%$ (canonical) / $\sim1.5\%$ (alt); under the framework's committed **pure-phase / all-pass** kernel ($|K|=1$, equation-book E13), the felt field is the current field delayed by an uncomputed group delay, and a resolvable transient survives, taking the fixed-field first-infall-vs-ancient contrast up to $\sim8$–$13\%$. Both readings share the *sign* (Sec. 5.2); only the magnitude differs. We write the committed-memory magnitude as a band:
$$
\text{Channel B (MG-impossible piece): } \sim1.3\text{–}13\%\ \text{in the fixed-field } \ln(\sigma_{\rm int}/\sigma_{\rm bary})\ \text{contrast (both footings, kernel-shape band)}.
$$

The magnitude is **kernel-hostage**, i.e. it depends on the undetermined loading function $\theta(y)$ and the kernel shape and is quoted as a band, not a derived number: $\theta(y)$ is not derived by the de Sitter–Unruh foundation, which fixes only the cone endpoints. The existence of the spread (in the field sector), its leading sign (Sec. 5), and MG $=0$ are the load-bearing claims; the amplitude is a band.

Two structural facts about Channel B matter for the design. First, the fractional amplitude at fixed dimensionless depth is *mass-independent* — cluster mass sets the transition-shell radius $R(a_{\rm ex}=a_0)=\sqrt{GM/a_0}$ ($0.39\ \mathrm{Mpc}$ at $10^{14}$, $1.22\ \mathrm{Mpc}$ at $10^{15}\,M_\odot$, canonical) and the crossing/memory window, but not the amplitude. Second, only *diffuse* members (low $\omega_{\rm in}$, low $y$) reach the signal-bearing regime: UDGs ($\sigma\sim15$) and dSph-scale members ($\sigma\sim10$–$50$) are the carriers, whereas $L^\ast$ ellipticals ($\sigma\sim200$) are internally near-Newtonian ($y\gg1$) and adiabatically dead. The survey-bright members are exactly the dead ones — which, as Sec. 6 shows, is the power wall.

---

## 4. The observable $D(\text{zone})$

### 4.1 The key degeneracy and the design principle

Both MI and MG have an EFE that loads the internal boost with the *current* $g_{\rm ext}$. So in *both* theories $\sigma_{\rm int}/\sigma_{\rm bary}$ varies with cluster-centric radius — the shared **radial EFE gradient**. That radial trend is not the MI signal; it is the killer common mode. The distinctive MI signal is the *residual spread at fixed cluster-centric radius (fixed current field), correlated with infall history* — for which the MG field sector predicts exactly zero.

The design principle is to project $\sigma_{\rm int}/\sigma_{\rm bary}$ onto the (radius $\times$ phase) plane and difference *along the phase axis within a fixed-radius bin*. The shared radial gradient is a common mode on the radius axis with no phase label; it cancels to the bin-width residual (the projection alias of Sec. 4.4). The MG field-sector residual at fixed *true* radius is exactly zero (the theorem); only the MI history signal — and a controllable projection alias — survive.

### 4.2 The statistic

Within one deprojected external-field bin (with $a_{\rm ext}$ from the caustic mass profile, width $\le0.3$ dex):
$$
D(\text{zone})\equiv\big\langle\ln[\sigma_{\rm int}/\sigma_{\rm bary}]\big\rangle_{\rm zone}-\big\langle\ln[\sigma_{\rm int}/\sigma_{\rm bary}]\big\rangle_{\rm ancient},
$$
with the infall-phase proxy = the Rhee et al. (2017, ApJ **843**:128) projected-phase-space zone read off from $(R_{\rm proj}/r_{200},\ |v_{\rm los}-v_{\rm cl}|/\sigma_{\rm cl})$, and $\sigma_{\rm bary}$ from the anisotropy-immune Wolf et al. (2010, MNRAS **406**:1220) half-light mass. The four Rhee zones, with their physical meaning, are: **ancient-infall** (long-virialized, the reference), **first-infall** (falling in for the first time, pre-first-pericentre), **recent-infall** (just past first pericentre), and **backsplash** (out again, past first apocentre). Operationally, $D(\text{zone})$ is the quantity an IFU delivers directly: the difference in $\langle\ln(\sigma_{\rm int}/\sigma_{\rm bary})\rangle$ between a phase zone and the ancient reference, at matched external field.

**MG field sector: $D(\text{zone})=0$ for every zone at fixed true radius** (symbolic $d/dy=0$, any $a_0$, any interpolation, both footings). **MI: a nonzero, history-correlated pattern**, whose leading term is the first-infall excess of Sec. 5. The measured $D(\text{first-infall})$ at the framework-committed memory is $\approx+1.3\%$ (canonical) / $\approx+1.5\%$ (alt) under the low-pass kernel reading — the difference between the first-infall zone ($+0.81\%$ dev-vs-mean, canonical) and the ancient zone ($-0.47\%$) — and up to $\sim8$–$13\%$ under the pure-delay reading (Sec. 5.4). This is the number an observer's $\langle\ln\sigma_{\rm int}/\sigma_{\rm bary}\rangle$ contrast equals, and it is the number that must be compared to the systematic floors below.

### 4.3 Anisotropy immunity via the Wolf normalization

The member's own internal anisotropy $\beta$ enters $\sigma_{\rm los}$, and infall can induce radial $\beta$, threatening a phase alias. The Wolf mass $M(r_{1/2})=3\langle\sigma_{\rm los}^2\rangle r_{1/2}/G$ is $\beta$-immune to first order at the half-light radius. The residual Wolf $\beta$-leak is $\lesssim1.8\%$ and *monotone* in $\beta$ — it cannot produce a sign-flip and folds into the same-signed heating-only confound family. This is a *softer* control than the star-orbit sign-immunity of Sec. 2.3 (it is a first-order cancellation, not an orthogonality); with IFU 3D internal kinematics $\beta$ is measured directly and the leak is calibrated.

### 4.4 Beating the projection alias and the same-signed confounds

The one MG evasion of $D(\text{zone})$ is **projection**: at fixed *projected* radius, radial plungers sit at a different *true* radius than settled members, so MG's real radial trend aliases into the phase axis. This is honestly the sharpest limit of the observable. An isotropic Monte Carlo puts the raw alias at $\sim2.2$–$2.4\%$; a class-*blind* scalar deprojection barely helps ($2.25\%\to2.19\%$), because the alias is driven by a class-*dependent* LOS-depth residual, not a mean bias. Two consequences follow, both toward caution:

- The Rhee zones *are* the orbit-class-aware deprojection — they are calibrated on N-body orbital history, not on a scalar radial mean — which is exactly the class-aware correction a scalar deprojection cannot supply. But the tagging has finite purity $p<1$; at $p=0.5$–$0.9$ the residual alias is $\sim1.3$–$2.0\%$, not the $\sim0.01\%$ one would get by binning on the (unobservable) simulation-true radius. The mitigation chain (caustic membership + Dressler–Shectman substructure cut + class-aware zone deprojection + relaxed-cluster selection) is **load-bearing, not optional**: a "detection" that bins by projected radius and skips the cuts measures projection and interlopers, not modified inertia.
- Anisotropic / filamentary infall (plungers entering along the major axis / LOS) can push the raw alias non-monotonically to $\sim7\%$ — band-sized — and biases the spherical caustic $a_{\rm ext}(R)$. Quantifying this needs a triaxial-potential, infall-axis forward model; the banked isotropic figure is a lower bound.

**The signal-to-systematic verdict, at the committed memory.** This is the honest crux. Under the low-pass kernel reading the measurable $D(\text{first-infall})\approx1.3$–$1.5\%$ absolute sits *at or below* its own systematic floors: the projection alias is $\sim1.3$–$2.0\%$ (up to $\sim7\%$ filamentary/triaxial) and the same-signed tidal floor is $\sim2$–$8\%$. In that corner the signal is comparable to, or below, the floors, and the honest expectation is a non-detection (Sec. 6.2). The signal clears its floors only under the pure-delay kernel corner (up to $\sim8$–$13\%$) — which is a genuinely uncomputed reading of the same committed memory, not a safe baseline. The exploratory S/N figures quoted in the scout (Sec. 6.2) that reach $\sim2$–$2.5\sigma$ used a signal of $\sim9.5\%$ (the top of the band); at the low-pass $\sim1.3\%$ the honest verdict slides to the scout's central expectation, a non-detection at every accessible sample size.

The same-signed dynamical confounds (tidal heating/stripping, ram-pressure, environmental quenching, non-equilibrium population mix) are beaten not by the phase-difference alone but by a joint four-part fingerprint that only MI trips:

| source | F1 fixed-$r$ phase contrast | F2 leading sign (first-infall hotter) | F3 rises outward | F4 baryon-blind |
|---|---|---|---|---|
| **MI (this framework, MI-class)** | ✓ | ✓ | ✓ | ✓ |
| MG (true $r$) | ✗ ($=0$) | ✗ | ✗ | ✓ |
| MG projection alias | ✓ | ✗ | ✗ | killed by zone deprojection |
| interlopers (uncut) | ✓ | ✗ | ✗ | killed by DS + caustic |
| tidal heating/stripping | ✓ | ✗ | ✗ (inward) | ✗ (tidal features) |
| ram-pressure / quenching | ✓ | ✗ | ✗ | ✗ (gas/SF marks) |
| non-equilibrium population mix | ✓ | can be MI-signed | ✗ (not outward-peaked) | ✗ (mixed populations) |

The **radial-profile separator (F3)** is the most robust: MI rises *outward*, peaking at the MOND-transition shell $a_{\rm ext}\sim0.3$–$1\,a_0$ ($\sim R_{500}$–$R_{200}$) and dying in the core, whereas tidal heating rises *inward* toward pericenter — opposite slopes. The **baryon-blind split (F4)** — environmental confounds mark the baryons (gas stripping, burst/truncated SF, tidal morphology) while the inertia signal does not — is corroborating, not decisive: it degrades for a *dry* tidal-heating episode on a gas-poor dE, exactly the diffuse carriers that carry the signal. The non-equilibrium population mix (Sec. 2.3, $d\ln M\approx-0.71$, MI-signed) is the most dangerous mimic because it can carry the MI sign; it is separated by F3 (it is not outward-peaked at the transition shell) and by relaxed-cluster / equilibrium-member selection. Treat F3 as the primary separator, sign (F2) as necessary-not-sufficient, and F4 as support. The observable-existence claim of Sec. 5.1 is theorem-grade *only through* this separation holding; the theorem itself is the field-sector zero.

---

## 5. The prediction

The prediction is two-tiered, and it **supersedes and corrects** the earlier D3 pre-registration (the dated pericentre sign-flip of "No Pump-Free Corner," [10.5281/zenodo.21179352]; see the concurrent erratum).

### 5.1 Tier (i): existence — theorem-grade in the field sector, confound-contingent as an observable

> At fixed cluster-centric gravitational field, a modified-inertia universe exhibits a nonzero internal-$\sigma$ spread correlated with infall history. In the field sector of any instantaneous-EFE gravity (QUMOND/AeST/$f(R)$; Milgrom's MG-virial universality) this fixed-field history spread is exactly zero.

The theorem-grade content is the field-sector zero: *no sourced-field–WEP theory contributes any fixed-field history spread*. It is independent of the sign and of the $s=-1$ postulate, and it holds for any $a_0$, any interpolation, both footings, off-adiabatically, and under retardation. The *observable* existence claim — that a measured nonzero fixed-field spread evidences modified inertia — is one step weaker: it is confound-contingent, because non-equilibrium dynamics, tidal shocking, and projection produce same-signed fixed-field spreads in Newton+dark-matter and MG alike (Sec. 2.2, 2.3, 4.4). What makes a *measured* spread MG-impossible is not the raw existence but the F3 outward-rising radial profile peaking at the transition shell, which the confounds do not share. We state this distinction as the honest core of the paper: the impossibility is airtight for the field sector and rides on the confound separation for the observable.

### 5.2 Tier (ii): leading sign — first-infall members run hotter

> Among members matched at the same cluster-centric field, **first-infall pre-pericentre members are hotter** (larger internal $\sigma$) than matched long-resident / post-pericentre members; equivalently, the $\sigma$-excess decreases monotonically with accumulated loading ($\approx$ time-since-infall).

This sign is **structural and timescale-free** for the physical class of kernels. On a monotonically *rising* field approach from a low-field past, the causal memory-felt external field is *always below* the current field, so the member is under-loaded, hence $\nu$-boosted hotter — for *any positive-averaging or pure-delay* causal kernel. (The one caveat: a fully dispersive all-pass kernel with a signed impulse response could in principle *overshoot* a rising ramp near onset, felt $>$ current, flipping the sign locally; the framework's committed $|K|=1$ branch was checked in the pure-delay limit and preserves the sign, and the physical reading is scoped to the monotonic pre-pericentre approach where overshoot does not occur.) The result is robust across the full grid — memory time $0.1$–$203\ \mathrm{Gyr}$, both kernel shapes (exponential low-pass and the pure-phase group-delay branch), member depth $0.1$–$1.0\,a_0$, pre-infall field $0$–$0.3\,a_0$, both footings — and across an independent 125-point orbit-distribution scan (masses $10^{14}$–$5\times10^{14}\,M_\odot$, apocenter $2$–$5\ \mathrm{Mpc}$, pericenter $0.2$–$0.6\ \mathrm{Mpc}$): **0/125 sign flips**. The signal is essentially monotone in accumulated loading, not a sharp dated event.

The corrected falsifier is therefore inverted relative to the published D3: a significantly **negative** fixed-field sign — first-infall members measured *cooler* at $\ge3\sigma$ — or a null spread at adequate power, is what would falsify Tier (ii). (What the published D3 named as the *signature* — a coherent pre-pericentre deficit — is in fact the *falsifier*.) The sign is conditional on the $s=-1$ postulate; $s=+1$ reverses it.

### 5.3 What is retracted, and why

The earlier D3 pre-registered a **dated pericentre sign-flip**: first-infall pre-pericentre members $-11$ to $-21\%$ *cold*, flipping to a post-pericentre *excess*, decisive at $3\sigma\approx2029$–$2031$. Both the polarity and the timescale were wrong.

1. **Polarity inversion (a bookkeeping error).** The "cold isolated past" of a first-infall member was encoded as a *low* value of the loading ratio $y=\omega_{\rm ex}/\omega_{\rm in}$. But the loading factor $\theta(y)$ is *maximal* as $y\to0$; true isolation is $a_{\rm ext}\to0$ (*zero* external loading for any $\theta$), not low-$y$. Holding a fixed nonzero $a_{\rm ext}$ while sending $y_{\rm hist}\to0$ injects *maximal* past loading and produces a spurious deficit. Worked correctly in field space, a first-infall member on a rising-field approach has a memory-felt field *below* its current field — under-loaded, hence *hotter, not colder*. A parallel text-label slip in a companion script (echoed in the banked GAP_STATEMENT E4/E7) printed "plungers less boosted" while its own loop output them hotter — the same conflation of "low $\theta$" with "low boost," when low $\theta$ means *less* suppression and therefore *more* boost. The claimed raw-loading-versus-memory "competition" was an artifact of this encoding; in field space the two contributions reinforce, and the net sign is fixed unambiguously by $\mathrm{sign}(a_{\rm ext,felt}-a_{\rm ext,now})$.

2. **Timescale hostage (a physics error).** The dated flip was computed with a Lorentzian memory of $\tau=0.45\ \mathrm{Gyr}$ (a dwarf-sector value), which is not the framework's committed covariant memory. The equation-book kernel gives $\tau_{\rm mem}=2c/a_0=2Z/H_\Lambda=203/168\ \mathrm{Gyr}$, footing-free and algebraic from the kernel. Against a cluster crossing time of $\sim1$–$2\ \mathrm{Gyr}$ this is deep adiabatic, in which a sharp sub-orbit pericentre flip *freezes out* under the low-pass reading (the same correction already forced on Channel A). Only the un-anchored $0.45\ \mathrm{Gyr}$ value made the flip a resolvable dated transient.

Consequently the post-pericentre and backsplash zones are timescale-hostage and **not** pre-registrable; the ancient/virialized zone is $\sim$zero. Only the existence claim (Tier i, field-sector) and the first-infall-hotter leading sign (Tier ii) survive. The corrected statement is *cleaner* than the published one: a field-sector existence claim plus a structural, timescale-free leading sign of the opposite polarity. This paper reports the correction with the same weight as the original claim.

### 5.4 Magnitude and its hostages

At the framework-committed E10 memory the MG-impossible history spread in the fixed-field $\ln(\sigma_{\rm int}/\sigma_{\rm bary})$ contrast is genuinely uncomputed *within the committed kernel*: the low-pass reading gives $\sim1.3\%$ (canonical) / $\sim1.5\%$ (alt), while the framework's committed pure-phase ($|K|=1$) reading of the same memory gives up to $\sim8$–$13\%$ (a bounded group-delay transient survives). We quote the magnitude as this $\sim1.3$–$13\%$ band and do not present the $1.3\%$ low-pass corner as "the answer" — it is one corner. Channel A is $\sim0.2$–$1\%$. Both are kernel-hostage: $\theta(y)$, the kernel *shape*, and the Jensen-gap curvature are not derived by the de Sitter–Unruh foundation, which fixes only the cone endpoints. The instantaneous $6$–$13\%$ EFE boost is a current-configuration quantity that MG partly shares, not the discriminant. Both footings are materially identical at fixed dimensionless depth ($<2\%$ on every sign fraction; $\tau_{\rm mem}H_\Lambda=2Z$ is footing-free). The leading sign is conditional on the $s=-1$ postulate: $s=+1$ reverses it.

---

## 6. Power and data availability

Both channels are underpowered today. We state the walls honestly and identify what would clear them.

### 6.1 Channel A — star-orbit spread (ELT-gated, plus a missing per-star tag)

The efficient (score/MLE) test has $z=f\,w\,D\,\sqrt{2N}$, with $f$ the fractional $\sigma$-spread, $w=\sigma^2/(\sigma^2+e^2)$ the measurement-error down-weight (variance information falls *quadratically* in error), $D$ the correlation of the orbit-tag proxy with true eccentricity, and $N$ the star count. Two independent walls, either fatal:

- **Count.** At the honest $f\sim0.2$–$1\%$, the Fisher floor needs $N\sim7\times10^4$ (1% ceiling) to $\sim6\times10^5$ (0.2% fiducial) clean per-star velocities in a *single* deep-MOND system even with a perfect tag. The biggest dSph (Fornax) has $\sim2600$; the whole stacked classical+diffuse reservoir is $\sim7100$ (perfect-tag $z<1.1$ at the ceiling, $<0.4$ fiducial). The amplitude and the count pull *opposite* — the deepest-$y$ systems (Crater II, Antlia II) that maximize $f$ have the fewest stars (150–200).
- **Tag.** There is no per-star eccentricity tag where the counts live. Gaia per-star internal proper motion has S/N $\sim0.03$–$0.05$ (bulk systemic only, $D_{\rm Gaia}\approx0$); LOS-only DF inference reaches $D\lesssim0.2$ and *is* the $\beta$-anisotropy channel MG reproduces; only HST/JWST multi-epoch 3D reaches $D\approx0.3$–$0.4$ for a few hundred bright stars in 2–3 systems, giving a best real single-system $z\approx0.05$.

No existing dataset (Walker+2009, Gaia DR3, MaNGA, ATLAS3D, Coma) comes within 1–6 orders. Powering Channel A needs $\sim10^{4.5}$–$10^{5.5}$ clean per-star velocities in one diffuse deep-MOND dSph from a 30 m-class campaign (ELT/MICADO, MSE) *plus* a per-star 3D orbit tag from multi-epoch space astrometry beyond Gaia's per-star precision — only the $\sim1\%$ point-mass-ceiling corner is within $\sim1$–$2$ orders of plausibility. Both footings shift $f$ by $<20\%$ and $N_{3\sigma}$ by $<44\%$: the discriminator is magnitude- and tag-hostage, not footing-hostage.

### 6.2 Channel B — cluster-member EFE (scaffolding ready, carrier count the wall)

The membership and phase-tagging scaffolding is *abundant and ready*, and is not the bottleneck: GalWCat19 (Abdullah et al. 2020, ApJS **246**:2; 1800 clusters, 34,471 members, caustic $M/R$ at $\Delta=500/200/100$), HeCS / HeCS-omnibus (Rines et al. 2013, ApJ **767**:15; 2016, ApJ **819**:63; dedicated caustic profiles), Yang SDSS groups, and the SAMI cluster survey (Owers et al. 2017, MNRAS **468**:1824; 8 clusters, 2899 members). DESI DR1 BGS deepens membership $\sim9.5\times$ (reaching into the dwarf regime at Coma redshift), but delivers redshifts, not IFU dispersions. The resolved stellar $\sigma$ is also served — the MaNGA data-analysis-pipeline maps recover $\sigma_{\rm int}$ inside $R_e$ (the STELLAR\_SIGMA extensions, quadrature-subtracting the LSF correction) with no pPXF re-derivation. The kinematics and the tagging are both fine.

The wall is the **diffuse IFU $\sigma$-carrier count**. The carriers are dwarf members with reliable $\sigma\sim20$–$70\ \mathrm{km\,s^{-1}}$; MaNGA is stellar-mass-limited ($M_\ast$ floor $\sim5\times10^8$), field-dominated, and its LSF ($1\sigma\approx70$–$76\ \mathrm{km\,s^{-1}}$) makes reliable stellar $\sigma$ bottom out near $35$–$45\ \mathrm{km\,s^{-1}}$, so the $\sigma\,20$–$40$ dwarfs are upper-limit-only. Worse, the accessible $\sim45$–$70\ \mathrm{km\,s^{-1}}$ carriers sit at shallower internal depth and carry a *smaller* true $D(\text{zone})$ than the headline band — a tightening toward NO-GO. Chaining the cuts (rich-cluster member $\cap$ caustic-able $\cap$ Rhee-taggable $\cap$ LSF-reliable) leaves only:

| configuration | diffuse tagged carriers $N$ | exploratory S/N $z$ (opt / mid / pes) | call |
|---|---|---|---|
| public MMU-MaNGA alone | $\sim40$–$77$ | $1.2$ / $0.5$ / $0.2$ | NO-GO — dies on statistics |
| MaNGA + public SAMI stack | $\sim135$–$237$ | $2.0$ / $0.9$ / $0.3$ | underpowered, firewalled hint |
| clean-exploratory floor | $300$–$500$ | $2.3$ / $0.9$ / $0.3$ | required floor; still marginal |

The public-MMU verdict is a **NO-GO on statistics**: the honest central expectation is a non-detection at every accessible $N$. Two cautions compound it. First, the optimistic $\sim2$–$2.5\sigma$ corner assumes a *signal of $\sim9.5\%$* (the top of the kernel band) *together with* best-case purity, scatter, and systematics; at the low-pass $\sim1.3$–$1.5\%$ signal — comparable to or below the $\sim1$–$2\%$ projection and $\sim2$–$8\%$ tidal floors (Sec. 4.4) — even the optimistic corner collapses and the honest expectation is the mid column ($z<1$). Second, the test is *statistics*-limited at all accessible $N$ (the statistical error exceeds the $\sim2\%$ systematic floor until $N\gtrsim400$) — the *opposite* failure mode from an SDSS single-fiber stack, which is *systematics*-limited (its $\sim1\%$ signal sits under a $1$–$5\%$ single-fiber $\sigma$-systematic floor and a $2$–$8\%$ same-signed confound, and its $\sigma\gtrsim90\ \mathrm{km\,s^{-1}}$ reliability floor excludes the carriers outright). Buying $N$ from SDSS does not buy the missing $\sigma$ control.

A clean detection needs *either* a dedicated wide nearby-cluster dwarf-IFU survey (with an $M_\ast$ floor to $\log M\sim8$, resolved stellar $\sigma$ reliable well below $45\ \mathrm{km\,s^{-1}}$, sub-percent systematics, and $\sim10^3$–$10^4$ diffuse members) *or* ELT/HARMONI-class IFU ($\sim2032$) to reach the $\sim20\ \mathrm{km\,s^{-1}}$ diffuse cluster-dwarf regime. The scaffolding slots in the moment such a carrier sample exists.

---

## 7. Scope and limits

We restate the boundaries plainly, because they are the difference between an honest prediction and an overclaim.

- **MI-class-generic, not framework-specific.** The signature distinguishes *any* history-dependent inertia from modified gravity (field-sector MG $=0$). It does **not** distinguish this framework from Milgrom's linear no-EFE modified inertia (arXiv:2503.07106), which also produces a fixed-field spread. It is an MI-vs-MG test, not a this-framework-vs-Milgrom test. The framework-specific content is the *numbers* (the committed $\tau_{\rm mem}=2Z/H_\Lambda$, the magnitude band), not the discriminating power.
- **It does not test $a_0$'s value or the sign $s=-1$.** Both are postulates. At fixed dimensionless depth $a_0$ cancels in the spread, so the test is $a_0$-value-blind by construction; the leading sign rides on $s=-1$ ($s=+1$ reverses it), so Tier (ii) is postulate-conditional while Tier (i) is not.
- **Magnitude is kernel-hostage.** $\theta(y)$ and the kernel shape (Channel B) and the Jensen-gap curvature (Channel A) are not derived by the de Sitter–Unruh foundation, which fixes only the cone endpoints. At the committed memory the Channel-B fixed-field contrast spans $\sim1.3\%$ (low-pass) to $\sim8$–$13\%$ (pure-delay) — genuinely uncomputed *within* the committed kernel. The $6$–$13\%$ instantaneous EFE boost is a current-configuration quantity MG partly shares, not the discriminant. Existence (field sector), leading sign, and MG $=0$ are the load-bearing claims; the amplitude is a band.
- **MG $=0$ is a theorem only in the field sector at fixed *true* field.** It is *not* a claim that the total observed spread is zero: non-equilibrium dynamics, tidal shocking, and projection produce same-signed fixed-field spreads in Newton+dark-matter and MG alike. In projection the field-sector zero becomes a mitigation-dependent baseline (Sec. 4.4): the raw alias is $\sim1$–$2\%$ at realistic tag purity and can reach $\sim7\%$ under filamentary/triaxial infall. The mitigation chain is load-bearing.
- **Same-signed confounds are real and partly unmodeled.** Tidal heating, ram-pressure, quenching, and non-equilibrium substructure carry the MI sign; a radius-correlated non-equilibrium population mix can manufacture a large MI-signed false spread ($d\ln M\approx-0.71$, $\sim35\times$ the signal, in the star-orbit statistic). They are separated (in design) by the outward-rising radial profile (F3) and the leading sign (F2), not by amplitude — and the separation is a design, not yet a demonstration on real data.
- **Both footings throughout.** Every dimensional number is carried at $a_0=9.36\times10^{-11}$ (canonical) and $1.13\times10^{-10}\ \mathrm{m\,s^{-2}}$ (alt); the spread is footing-invariant at fixed depth and $\tau_{\rm mem}H_\Lambda=2Z=11.58$ is footing-free.

No claim of proof is made for the framework. The field-sector MG $=0$ statement (at fixed true field) is the sole theorem-grade claim.

---

## 8. Conclusion

Post-lensing-no-go — with lensing now shared between the MI and MG realizations — the relational velocity-dispersion spread is the correct *kind* of test the modified-inertia program has been missing: an observable with an exact field-sector baseline that resists equilibrium anisotropy. Its logical core is airtight where we claim it. For any theory that sources a field and moves matter on WEP geodesics of it, a subsystem's internal dispersion at fixed external field carries exactly zero *field-sector* spread across infall history; a nonzero field-sector fixed-field history spread requires that inertia depend on the body's own worldline, which is the definition of modified inertia. The sole evasion — a velocity-dependent coupling to the tracer's own motion — *is* modified inertia in an MG costume and cannot serve as a rival explanation. The discriminant survives a strong-anisotropy control test in the star-orbit channel (immune by sign, the zero-point being signal-sized), so the MI sign is not re-labeled velocity anisotropy, and the designed observable $D(\text{zone})$ differences the shared radial EFE gradient out as a common mode. What the theorem does *not* deliver by itself is the *observable* existence claim: a measured fixed-field spread is MG-impossible only after the same-signed non-field confounds — non-equilibrium dynamics, tidal shocking, projection — are separated by the F3 outward-rising radial profile. That separation is the design, not the theorem.

The framework-specific prediction, corrected from the earlier D3, is two-tiered: the *existence* of the field-sector fixed-field history spread is theorem-grade and MG-impossible; its *leading sign*, in the first-infall pre-pericentre zone, is that first-infall members run hotter than matched long-resident members — a structural, timescale-free result (for positive-averaging or pure-delay kernels) that inverts the backwards, dated pericentre sign-flip now retracted. The magnitude is kernel-hostage: at the framework's committed memory it is genuinely uncomputed between a $\sim1.3\%$ low-pass corner and a $\sim8$–$13\%$ pure-delay corner in the cluster channel, and sub-percent in the star-orbit channel.

The honest status is a prediction, not a confrontation, and after the magnitude correction it is a notch more cautious than a first reading suggests. Both channels are underpowered today: the star-orbit channel needs ELT-class per-star velocities plus a per-star 3D orbit tag that does not exist; the cluster channel has its membership and phase-tagging scaffolding ready (GalWCat19, HeCS, Rhee zones, DESI-deepened membership) but is walled by the diffuse IFU $\sigma$-carrier count — a public-MMU NO-GO at $\sim40$–$77$ carriers, an underpowered $\sim2$–$2.5\sigma$ firewalled hint with a MaNGA+SAMI stack (and only if the signal sits at the top of the kernel band; at the low-pass corner even that collapses to a non-detection), and a clean detection gated on a dedicated wide-cluster dwarf-IFU survey or ELT/HARMONI ($\sim2032$). This front is the program's most distinctive *in-principle* discriminant, worth pre-registering (field-sector existence plus first-infall-hotter, with the sign statistic pinned to the single robust zone) and reanalysing at MaNGA/SAMI for a hint — but it neither manufactures a win nor a deficit, and it does not test $a_0$'s value or the sign postulate.

---

## Appendix A — Committed, verifiable scripts

Every load-bearing claim is backed by a committed, runnable script (numpy/scipy/sympy), each exiting 0 and carrying both coefficient footings. The four lanes:

**Star-orbit channel** (`prep_2026/sigma_spread/`):
- `mi_spread.py` — the deep-adiabatic Jensen-gap magnitude ($\tau_{\rm mem}/T_{\rm orb}$ table; RMS $\sigma$-spread $0.2$–$1\%$; sign negative), cross-checked against the 19/19-verified real-kernel integrator (`prep_2026/mi_integrator/`).
- `mg_zero.py` — the sourced-field–WEP MG $=0$ theorem ($d\sigma/dy=0$ symbolic; boundary stress test C1–C6; the disformal/Finsler-SME evasion identified as MI).
- `observable.py` — the $\beta$-immune orbit-family enclosed-mass consistency statistic, the anisotropy sign-immunity control (zero-point $+0.033$, signal-sized, immune by sign), and the non-equilibrium population-mix false-detection probe ($d\ln M\approx-0.71$).
- `power.py` — the Fisher floor, MC-validated ($\sqrt N$ scaling $1.99$; null calibrated), and the two-wall no-go.

**Cluster-member EFE channel** (`prep_2026/cluster_efe_channel/`):
- `predict.py` — the $\theta(y)$ magnitude band, radial structure, and mass/depth dependence.
- `mg_efe_zero.py` — the fixed-true-field field-sector MG $=0$ theorem and the quantified projection/interloper mimics.
- `observable.py` — the $D(\text{zone})$ statistic and the four-part confound fingerprint.
- `power.py` — the survey-regime power analysis (SDSS systematics-limited; MaNGA/SAMI statistics-limited exploratory).

**Sign reconciliation** (`prep_2026/cluster_efe_sign/`):
- `setup_diagnose.py`, `net_sign.py`, `robustness.py` — the diagnosis of the two label bugs on one correct baseline, the per-zone net sign against both anchors (low-pass and pure-delay kernel readings), the timescale pin, and the $0/125$ orbit-scan robustness of the first-infall-hotter sign.

**Data-availability scout** (`prep_2026/cluster_efe_data_scout/`):
- `inventory_manga.py`, `inventory_membership.py`, `overlap_power.py` — the MMU carrier census (resolved $\sigma$ served; membership abundant; carrier count $\sim40$–$77$ the binding wall).

---

## References

- Abdullah, M. H., Wilson, G., Klypin, A., et al. 2020, ApJS **246**, 2 (the GalWCat19 cluster catalog).
- Milgrom, M. 1983, ApJ **270**, 365.
- Milgrom, M. 1999, Phys. Lett. A **253**, 273 (astro-ph/9805346) — the $\nu$-kernel wellhead, $\nu(y)=\sqrt{1+1/y}$, Eq. 9.
- Milgrom, M. 2014, MNRAS **437**, 2531 — the MOND paradigm; the external field effect and MG-virial universality.
- Milgrom, M. 2022, Phys. Rev. D **106**, 064060 (cited for the two-frequency EFE subsystem boost $\theta(y)$).
- Milgrom, M. 2025, arXiv:2503.07106 — a linear no-EFE modified-inertia model (also produces a fixed-field spread; the MI-class-generic caveat).
- Owers, M. S., et al. 2017, MNRAS **468**, 1824 (the SAMI cluster redshift survey).
- Rhee, J., Smith, R., Choi, H., et al. 2017, ApJ **843**, 128 — projected-phase-space infall zones.
- Rines, K., et al. 2013, ApJ **767**, 15; 2016, ApJ **819**, 63 — the HeCS / HeCS-omnibus caustic cluster profiles.
- Wolf, J., Martinez, G. D., Bullock, J. S., et al. 2010, MNRAS **406**, 1220 — the $\beta$-immune half-light mass estimator.
- SPARC / dSph kinematics: Walker et al. 2009 (ApJ **704**, 1274) and the Battaglia et al. / Gaia dSph proper-motion literature, as needed.
- Zimmerman, C. 2026, MI Field Theory Results 2026, Zenodo [10.5281/zenodo.21403470].
- Zimmerman, C. 2026, the lensing no-go, Zenodo [10.5281/zenodo.21418816].
- Zimmerman, C. 2026, No Pump-Free Corner (superseded on D3), Zenodo [10.5281/zenodo.21179352], with the concurrent erratum (2026-07-17).

*$a_0$'s value and the sign $s=-1$ remain postulates. Field-sector MG $=0$ at fixed true field is the sole theorem-grade claim. No claim of proof is made for the framework. Both coefficient footings ($a_0=9.36\times10^{-11}$ / $1.13\times10^{-10}\ \mathrm{m\,s^{-2}}$) are carried throughout.*
