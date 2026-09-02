# The Retarded Nonlocal MOND Kernel Is Unstable on MOND Backgrounds: a Longitudinal Gradient Instability and a Deep-MOND Ghost Close the Nonlocal Door

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

*Version 2026-09-02 · Zenodo [10.5281/zenodo.22253953](https://doi.org/10.5281/zenodo.22253953). Companion to Zenodo [10.5281/zenodo.22242701](https://doi.org/10.5281/zenodo.22242701) (the cluster polytrope) and [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562) (the cluster no-go).*

---

## Abstract

Purely metric nonlocal realizations of MOND (Deffayet, Esposito-Farèse & Woodard 2011; Woodard 2014; Deffayet & Woodard 2026) carry the MOND force in a retarded nonlocal scalar $X=\Box^{-1}_{\rm ret}(R_{\mu\nu}u^\mu u^\nu)$ through an algebraic function $f(Z)$, $Z=(4c^4/a_0^2)\,\partial_\mu X\partial^\mu X$, and are the one class that escapes the local no-go for a relativistic MOND completion with $\Phi=\Psi$ lensing and $\alpha_3=0$. No perturbation analysis of this kernel on a MOND background exists. We perform it. Around a uniform MOND field ($\bar Z=4y^2$, $y=g/a_0$), in Newtonian gauge and plane symmetry, at leading order in $a_0\to0$ at fixed $y$, the scalar sector of the in-in theory — the auxiliaries eliminated by their retarded particular solutions — has the dispersion $(e+3)\,\omega^4-(2e-1)\,k^2\omega^2+e\,k^4=0$ at $y=1$ for the exponential law, with discriminant $1-16e<0$: complex frequencies, $\mathrm{Im}\,\omega=0.39\,ck$. The instability is present for every $y\ge0.5$ tested ($\mathrm{Im}\,\omega/ck=0.21,0.39,0.44,0.36,0.18,0.05$ at $y=0.5,1,2,3,5,8$), grows without bound in $k$ (e-folding $1.3\times10^3$ yr at 1 kpc, 13 yr at 10 pc), is longitudinal only (the transverse sector is stable), is driven entirely by $f''(Z)$ — the $\mu'$ term without which there is no MOND — and appears identically for Deffayet–Woodard's own $f(Z)=\tfrac12Ze^{-\sqrt Z/3}$. In the real-frequency deep-MOND window ($y\le0.25$) one of the two propagating scalar modes has negative energy. The result holds under both definitions of the theory, the ordinary localized action and the in-in retarded functional, because $\det M=\det D\cdot\det M_{\rm red}$ and null data removes only the pure-auxiliary poles at $\omega=\pm k$. Every internal check passed first: the GR limit has no scalar metric mode and the clock mode $\omega^2=u/(1+u)\,k^2$ exactly; the static longitudinal response is $1/(\mu_\parallel k^2)$ with $\mu_\parallel=d(y\mu)/dy=1-2f'-4\bar Zf''$; $\Phi=\Psi$; the localized $(X,\xi)$ kinetic block is $[[-4e^{-y},1],[1,0]]$, $\det=-1$. The mechanism is the radial gradient instability that killed the khronometric $a_\mu$-coupled class: any dynamical carrier of $\mu(|\nabla\Phi|)$ turns $\mu'$ into a wrong-sign longitudinal kinetic term in the transition regime. Consequences: the condensate-clock nonlocal candidate we had built the same night, which passed 29 local-Lagrangian gates, is dead at the stability gate; the Deffayet–Woodard kernel inherits the result; and with the local carriers and the aether already closed, every class examined for the strict completion fails. Scope: linear order, WKB background, plane symmetry, this kernel structure; nonlocal form factors on the Weyl or Einstein tensor are not covered and no action for them exists. All numbers are printed by a committed script with checks that can fail and an ablation control.

---

## 1. The door, and what was known

A relativistic completion of MOND is asked to deliver, from one action, exact MOND with the exponential law $\mu(y)=1-e^{-y}$, no-slip lensing $\Phi=\Psi$, an acceptable full PPN set including the preferred-frame parameters, matter conservation, luminal gravitons, stability, an expanding cosmology and controlled limits (the 13-gate specification of the companion programme). By 2026-09-01 the local carriers were closed by committed computation: elliptic and algebraic constraint carriers by $\alpha_3=O(1)$ (an instantaneous constraint cannot be retarded), the frame-free scalar by $O(1)$ slip, the clock-plus-curvature carriers by $c_T\ne c$, the acceleration-coupled khronometric carrier by a radial gradient instability on $a_0<a<38a_0$, and the aether by $\alpha_1=-2(K_B+2)$. One door remained: a genuinely nonlocal, retarded carrier, for which $\alpha_3=0$ because the response $1/(k^2-\omega^2/c^2)$ carries the retardation.

The concrete instance is the Deffayet–Woodard kernel. With a timelike frame $u_\mu=\partial_\mu\phi$,
$$X=\Box^{-1}_{\rm ret}\big(R_{\mu\nu}u^\mu u^\nu\big),\qquad Z=\frac{4c^4}{a_0^2}\,g^{\mu\nu}\partial_\mu X\partial_\nu X,\qquad \Delta L=\frac{c^4}{16\pi G}\,a_0^2 f(Z)\sqrt{-g},$$
and in the static weak field $X\to\Psi$, $Z\to4|\nabla\Psi|^2c^4/a_0^2=4y^2$, so that the potential obeys $\nabla\cdot[(1-2f'(Z))\nabla\Psi]=4\pi G\varrho/c^2$: the MOND function is $\mu=1-2f'(4y^2)$. Deffayet & Woodard use $f=\tfrac12Ze^{-\sqrt Z/3}$; the exponential law is obtained exactly by $f_{\exp}=4-2(\sqrt Z+2)e^{-\sqrt Z/2}$. The kernel is localized by a multiplier, $\xi(\Box X-R_{uu})$, whose ordinary-action Hessian in the $(X,\xi)$ pair is indefinite, $[[-4e^{-y},1],[1,0]]$ with $\det=-1$ (an independent Dirac audit, 2026-09-02): two auxiliary modes, one ghost-signed. The standard resolution is to define the theory in the in-in (Schwinger–Keldysh) sense, with $X,\xi$ as retarded functionals of the metric carrying no Cauchy data. What that theory's free modes are on a background where the kernel is active had never been computed: Deffayet & Woodard (2026) defer the perturbation analysis; Woodard (2014) lists the ghost question as future work; the certification audit of the kernel in this repository was carried out on Minkowski and FLRW, where $\bar Z=0$ or $f$ is exponentially dead.

We computed it, having first built the strongest candidate the door admits.

## 2. The candidate, for the record

The condensate-clock nonlocal MOND action (CCNL) replaces Deffayet–Woodard's mimetic clock and its advected dust by the Aether–Scalar–Tensor condensate clock $K(Q)=-2\Lambda+K_2(Q-Q_0)^2$, $Q=\sqrt{-(\partial\phi)^2}$, $u_\mu=\partial_\mu\phi/Q$, whose dust is a $\gamma=2$ polytrope with $c_s^2=|\Psi|c^2$ inside wells and therefore galaxy-safe (Zenodo 22242701), and uses $f_{\exp}$. It passed 29 committed gates: the galaxy radial-acceleration relation shifts by $\le0.001$ dex at the full cosmic dust share (Deffayet–Woodard's pressureless dust shifts it by 0.06–0.24 dex), the off-shell Noether identity of the localized action holds to machine precision with the retarded kernel (so the "hand-imposed retarded operator is not Euler–Lagrange" objection is void: retardation is a choice of solution), $R^{(1)}_{uu}[h^{TT}]=0$ so $c_T=c$, $\gamma-1=-e^{-y}$ with $y=10^{12}$ at the Cassini radius, the clock's preferred-frame back-reaction is below $10^{-25}$, $\alpha_3=0$ by structure, the clock is healthy on its positive branch, and a nonlinear minisuperspace integration keeps the auxiliaries slaved and the constraint conserved to $10^{-10}$. None of that survives §4.

## 3. Setup and internal checks

Newtonian gauge, $ds^2=-(1+2\Phi)dt^2+(1-2\Psi)d\mathbf x^2$, fields of $(t,x)$, $c=1$, $16\pi G=1$. Background: $\bar X=s\,x$ with $s=y\,a_0$ (so $\bar Z=4y^2$), $\bar\xi=0$ (a uniform gradient sources no $\xi$), the clock at rest with charge $u_b$ ($\bar Q=Q_0(1+u_b)$, $c_s^2=u_b/(1+u_b)$). The quadratic action is built from the covariant pieces: $\sqrt{-g}R$ to second order; $\sqrt{-g}a_0^2f(Z)$ expanded around $\bar Z$ keeping every term carrying $s$; $\sqrt{-g}\,\xi(\Box X-R_{uu})$ at second order; $\sqrt{-g}K(Q)$ with an exact-to-second-order expansion of $Q$. Linear Euler–Lagrange equations, plane waves $e^{i(kx-\omega t)}$, and the $5\times5$ matrix $M(\omega,k)$ on $(\Phi,\Psi,\delta X,\delta\xi,\delta\phi)$. Leading order in $a_0\to0$ at fixed $y$ removes the vacuum-energy and post-Newtonian terms (all background residuals are $O(a_0^2)$: $\Lambda$, $a_0^2f_0$, $f's^2$, $K_2Q_0^2u_b$) and leaves the $O(1)$ MOND structure through $f'(\bar Z)$, $f''(\bar Z)$. In-in reduction: the auxiliary rows are eliminated by their particular solutions, the Schur complement $M_{\rm red}=A-BD^{-1}C$; $\det D=-(k-\omega)^2(k+\omega)^2$ are the pure-auxiliary poles that null data removes.

| internal check | result |
|---|---|
| GR + clock, kernel off | $(\Phi,\Psi)$ block $\det=-16k^4$: no scalar metric mode; clock $\omega^2=\tfrac{1}{21}k^2=\tfrac{u_b}{1+u_b}k^2$ exactly ($u_b=\tfrac1{20}$) |
| ordinary local auxiliary block, $y=1$ | $[[-4e^{-1},1],[1,0]]$, $\det=-1$: the Dirac audit's matrix, reproduced independently |
| static longitudinal response, $y=1$ | $\Psi k^2/\rho=-\tfrac14=-1/(4\mu_\parallel)$ with $\mu_\parallel=1-2f'-4\bar Zf''=d(y\mu)/dy=1.000$; $\Phi=\Psi$ |

## 4. The dispersion

At $y=1$ with $f_{\exp}$ the reduced $(\Phi,\Psi)$ determinant factors to
$$-\frac{256\,k^4\,(k^2-21\omega^2)\,\big[(e+3)\omega^4-(2e-1)k^2\omega^2+e\,k^4\big]\,e^{-1}}{105\,(k-\omega)^2(k+\omega)^2},$$
the clock factor times a quartic whose discriminant is $(2e-1)^2-4e(e+3)=1-16e<0$. Its roots are $\omega^2/k^2=0.388\pm0.570\,i$, i.e. $\omega/k=0.734\pm0.388\,i$: a growing and a decaying pair, growth $\propto k$.

| test | outcome |
|---|---|
| $y$-scan, $f_{\exp}$ | real $\omega^2$ at $y=0.10$ (0.056, 0.897) and $0.25$ (0.174, 0.717); complex at $y=0.5,1,2,3,5,8$ with $\mathrm{Im}\,\omega/k=0.21,0.39,0.44,0.36,0.18,0.05$ |
| Deffayet–Woodard's $f=\tfrac12Ze^{-\sqrt Z/3}$ | complex at $y=0.5,1,2,4$ ($\mathrm{Im}\,\omega/k$ up to 0.48); real at 0.25 and 8 |
| ablation $f''\to0$ at fixed $f'$ | stable at $y=1,2$ (one real mode, $\omega^2/k^2=0.30,0.61$): the instability is the $f''$ term |
| ablation $f'\to0$ at fixed $f''$ | unstable ($\mathrm{Im}\,\omega/k=0.60,0.52$) |
| transverse propagation, $\mathbf k\perp\nabla\bar X$ | stable at $y=0.5,1,2,4$ ($\omega^2/k^2=0.14,0.30,0.61,0.93$): longitudinal only |
| energy sign, deep-MOND window | $y=0.10$: $\omega/k=0.236$ ($E>0$) and $0.947$ ($E=-7.8\times10^3$); $y=0.25$: $0.417$ ($+$), $0.847$ ($-4.1\times10^2$) |
| metric content of the unstable mode, $y=1$ | $|\Phi|^2+|\Psi|^2$ share 6.4%, $(X,\xi)$ share 86%: nonzero, hence a mode of the reduced metric equation |
| e-folding times, $y=1$ | 1 kpc: $1.3\times10^3$ yr; 10 pc: 13 yr; 1000 AU: 2.4 days |
| e-folding times, $y=8$ | 1 kpc: $10^4$ yr; 10 pc: 100 yr; 1000 AU: 18 days |

Because $\det M=\det D\cdot\det M_{\rm red}$, the quartic's roots are modes of the ordinary local action as well; the in-in prescription removes only $\det D=0$, the pure-auxiliary modes at $\omega=\pm k$. The unstable modes carry metric content and survive under either definition.

## 5. Mechanism

MOND requires $\mu'\ne0$. The static AQUAL operator is elliptic and safe, with longitudinal coefficient $\mu_\parallel=\mu+y\mu'>0$ for the exponential law, and the kernel reproduces exactly that static response (§3). Its time-dependent completion is not safe: the quadratic kernel Lagrangian contributes $-4f_1(\partial_t\delta X)^2+4(f_1+2\bar Zf_2)(\partial_x\delta X)^2$, a wrong-sign time-kinetic term for $X$ in the localized pair, and the $f_2$ (curvature, $\mu'$) part of the longitudinal gradient term is what turns the coupled $(\Phi,\Psi,X,\xi)$ dispersion complex once $\bar Z$ is finite. With $f''=0$ — $f$ linear in $Z$, $\mu$ constant, no MOND — the sector is stable. This is the mechanism that killed the khronometric $a_\mu$-coupled class on $a_0<a<38a_0$ (2026-08-31): a dynamical carrier of $\mu(|\nabla\Phi|)$ converts $\mu'$ into a longitudinal instability in the transition regime. Retardation does not cure it; it only relocates the carrier.

## 6. Consequences

1. **CCNL is dead at the stability gate**, its 29 other passes notwithstanding.
2. **The Deffayet–Woodard kernel inherits the result.** Their 2026 model retains the same $X$, $Z$, and an algebraic $f$; the difference in the clock sector does not enter at this order (the clock decouples from the kernel at linear order around a vacuum background, $\bar R_{\mu\nu}=0$).
3. **The nonlocal door is closed at linear-WKB order.** With the local constraint carriers ($\alpha_3$), the frame-free scalar (slip), the curvature-coupled clock ($c_T$), the acceleration-coupled clock (radial instability) and the aether ($\alpha_1$) closed by committed computation, every class examined for the strict completion fails. In the companion programme's language this is Outcome B, a no-go, not Outcome A.
4. **What survives is unchanged**: MOND phenomenology with the acceleration scale $a_0=c^2\sqrt{\Lambda/32\pi}$ as input, the falsifiable $a_0\propto\sqrt{\rho_{\rm DE}(z)}$, and the condensate dark field of the AeST class, whose cluster yield is 23–33% of the core residual (Zenodo 22242701). No relativistic completion in hand passes the stability gate.

## 7. Scope, stated honestly

Linear order. A uniform-gradient WKB background, $a_0\to0$ at fixed $y$; since the growth is $\propto k$, the short-wavelength regime where WKB is best is the dangerous one. Plane symmetry and Newtonian gauge. The kernel structure: $u$-projected $R_{\mu\nu}$, algebraic $f(Z)$, no higher-derivative terms; Deffayet & Woodard state their philosophy is an IR modification, and a UV completion with higher spatial derivatives capping the growth at some $k_{\max}$ is not part of any published action. Not covered: nonlocal form factors acting on the Weyl or Einstein tensor (a "field-dependent spin-2" completion, for which no action exists in the literature or in this repository); the fully nonlinear problem; bounded backgrounds with their own scale. The negative-energy mode in deep MOND is a linear result on the same background.

## 8. Attribution

The kernel is Deffayet, Esposito-Farèse & Woodard (2011), Woodard (2014) and Deffayet & Woodard (2026). The Dirac structure of the localized pair for this candidate is the independent 2026-09-02 audit in the repository (it also caught a placeholder check in the candidate's gate script, since replaced by a derived one). The radial-gradient mechanism for $\mu'$-carrying relativistic MOND is the repository's khronometric result of 2026-08-31. The perturbation analysis of the retarded kernel on a MOND background, the in-in reduction with its internal checks, the $f''$ ablation and the transverse contrast are new here as far as searched; no such analysis is known to us in the literature.

## 9. Two-sided summary

For the nonlocal programme: the retarded kernel genuinely does what the local carriers cannot — $\alpha_3=0$, $\Phi=\Psi$ at 1PN, exponentially screened PPN, luminal gravitons, conservation as a Noether identity of the localized action, and, with a condensate clock, galaxy-safe dust. Those are real and were computed.

Against: on any background where the kernel is active, the scalar sector is unstable in the transition regime with growth times of years at parsec scales and unbounded in $k$, and ghostly in deep MOND; the instability is the MOND function's own curvature $\mu'$ and cannot be removed without removing MOND; Deffayet–Woodard's own interpolation function shows it. The last door is shut at this order.

## 10. Reproducibility

- In the directory `qwen_claude_field_theory/` `closure_2026/` `candidate_ccnl_2026/`: `ccnl_inin_linear_scalar_2026.py` (12 checks, rc=0; output `.out`): §3–5. The physics checks are findings that can fail to materialize; the $f''\to0$ ablation is the control.
- `ccnl_mond_gates_2026.py` (29 checks, rc=0; `MUTATE=1` breaks the galaxy comparison): §2.
- `ccnl_action_dirac_audit_2026.py` with its tests and manifest (the independent audit): the $(X,\xi)$ block.
- `CCNL_MOND_CANDIDATE.md`, `NONLOCAL_KERNEL_LINEAR_INSTABILITY_VERDICT.md`: the gate table and the verdict.

Quarantine: $a_0$ (both footings, $9.36\times10^{-11}$ and $1.13\times10^{-10}$ m s$^{-2}$), $\kappa$ and the clock's charge are inputs. Nothing here derives them.

## 11. References

- Deffayet C., Esposito-Farèse G., Woodard R. P., 2011, PRD 84, 124054 (arXiv:1106.4984)
- Deffayet C., Esposito-Farèse G., Woodard R. P., 2014, PRD 90, 064038 (arXiv:1405.0393)
- Deffayet C., Woodard R. P., 2026, JCAP 04, 081 (arXiv:2512.10513)
- Deser S., Woodard R. P., 2013, JCAP 11, 036 (arXiv:1307.6639)
- Skordis C., Złośnik T., 2021, PRL 127, 161302 (arXiv:2007.00082)
- Woodard R. P., 2014, Can. J. Phys. 93, 242 (arXiv:1403.6763)
- Zimmerman C. P., 2026, Zenodo 10.5281/zenodo.20779562 (the cluster no-go); 10.5281/zenodo.22242701 (the cluster polytrope)
