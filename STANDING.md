# STANDING

**de Sitter–Unruh modified inertia — where the programme actually stands**
Last updated **2026-07-30** (rev. 4). Maintained as the single entry point: what is claimed, what is earned,
what is postulated, what is live, and what is closed. If a statement anywhere in this repository
conflicts with this file, this file is newer unless it says otherwise.

---

## 0. The claim, stated as narrowly as it should be

One claim: **the acceleration scale of the mass-discrepancy–acceleration relation is set by the
dark-energy density.**

$$a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda}\;=\;\frac{cH_\Lambda}{Z},
\qquad \kappa=\tfrac12,\qquad Z=\sqrt{32\pi/3}=5.78881,
\qquad a_0 = 9.36\times10^{-11}\ \mathrm{m\,s^{-2}} .$$

Realised as **modified inertia**. **⚠️ KERNEL CHANGED 2026-07-30: the interpolation is now $\alpha\ge2$**,
$K=\sqrt{z/(1+z)}$ with $z=|a|^2/a_0^2$, replacing $\nu(y)=\sqrt{1+1/y}$ ($\alpha=1$). $a_0$ is
**unaffected** — the new kernel satisfies every premise the $a_0$ derivation uses (Herglotz positivity,
passivity $\sup K=1$, the unit sum rule) and its spectral measure $\rho(s)=(1/\pi)\sqrt{s/(1-s)}$ on
$0<s<1$ is *simpler* than the old one. **What is withdrawn is the word "exact": the relation
$g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ is an $\alpha=1$ identity and is no longer claimed.**
Reason: $\alpha=1$ costs 1279× the Earth ephemeris bound and 257× the disformal construction's own
$B<1$ premise, and buys 0.0033 dex on SPARC. See §5.0 and `mi_alpha2_migration_2026.py`.

**⚠️ CREDIT, CORRECTED 2026-07-30 (rev. 4) — the previous line understated it.** It is not merely the
same *kernel*. **Milgrom (1999, *Phys. Lett. A* **253**, 273, Eqs. 6–9) derives this exact LAW from the
de Sitter–Unruh balance AND fixes its coefficient at $a_0=2cH_\Lambda$.** Verified: his Eq. (9)
$\hat\mu(x)=\sqrt{1+(2x)^{-2}}-(2x)^{-1}$ with Eq. (8) is *identically* $g_{\rm obs}^2=g_{\rm
bar}^2+a_0g_{\rm bar}$ (sympy difference exactly 0). The same law was independently re-derived
entropically by **Pikhitsa (2010, arXiv:1010.0318)** and **Klinkhamer & Kopp (2011, MPLA 26, 2783,
arXiv:1104.2022)**, both also landing on $2cH_\Lambda$.
**So the dS–Unruh argument does not leave the coefficient free — it PREDICTS one, and that prediction
is $2Z=11.58\times$ the value in use.** The programme's actual contribution is therefore: a
**re-normalisation of the coefficient to fit data** ($\kappa=\tfrac12$ in place of Milgrom's 2), plus
the modified-inertia completion. Not a derivation of the law, and not a derivation of its scale.

**Retracted, 2026-06-23, publicly, to ~40 physicists.** All theory-of-everything and Standard-Model
claims. They are not to be revived. The true position is the $a_0$ reframing above and nothing wider.

**Two footings are carried on every dimensional number, always:** canonical $\rho_{\rm DE}$
($a_0=9.36\times10^{-11}$) and alternative $\rho_{\rm total}$ ($1.13\times10^{-10}$).

---

## 1. Earned

| result | status |
|---|---|
| Radial-acceleration relation, SPARC, framework's $a_0$ | **0.1116 dex** at $\alpha=2$ (0.1083 at the retired $\alpha=1$; the $+0.0033$ switch cost is $0.10\,\sigma_{\rm int}$) — still at or better than regular MOND's 0.122–0.140 |
| ~~The $a_0$-line $g_{\rm obs}^2-g_{\rm bar}^2=a_0\,g_{\rm bar}$~~ | **WITHDRAWN 2026-07-30.** An exact identity *of the $\alpha=1$ kernel only*, which the framework no longer uses. Retained as history, not as an earned result |
| $\kappa$ reduction $a_0=\kappa c\sqrt{G\rho_\Lambda}$ | every $\pi$, the 32 and the 3 cancel |
| Modified-inertia action, v1–v11 | published; constraint structure machine-verified, 0 frame dof |
| Disformal lensing construction (v7–v10) | closed, Cassini-safe, Ostrogradsky-free |
| Seven structural theorems | **v4 DOI 10.5281/zenodo.21711577** (concept **21707844**, always latest), 2026-07-30. **v3 re-derived all seven under the $\alpha\ge2$ kernel and added the new spectral measure**; all survive, three with new numbers (Hessian $-3\sqrt2/64$; $h(x)=x(x^2+2)/(1+x^2)^{3/2}$; dipole 5.4–15.4%), one falsifier qualified (the dipole sign flips in the $e\gg y$ corner at sub-0.2%). **v4 is a file-set fix only** — v3 dropped `PROVENANCE.md` and the dSph CSV; no scientific content differs. v2 (21708842) states the retired $\alpha=1$ kernel and is superseded |

## 2. Postulated — not derived, and not to be presented otherwise

- **$\kappa=\tfrac12$.** Its *value* is not derived. Ghost-freedom, unitarity and holography have each
  been shown insufficient to force it; the CKN degrees-of-freedom bridge is closed. **One-parameter
  effective theory, not a zero-parameter derivation.**
- **$Z$.** Same status.
- **The sign $s$** — **demoted 2026-07-30.** No longer a parameter awaiting data: within the closure
  family that reproduces the relation, the channel it would sign is *identically zero*, so $s$ has no
  observable consequence (Thm 2, Cor 2.2). This is a reduction in free content, not a measurement.
- **⚠️ THE LAW ITSELF — status corrected THREE times on 2026-07-30. The current reading is the PINCER
  below, which is sharper than anything the corpus had.** Two theorems now close on each other:
  **Theorem 3** (proof CORRECTED 2026-07-30, and the statement got *wider*): no **local**
  $L(x,\dot x,\ddot x)$ gives the law. The published proof was wrong — its "det $H=0$, *i.e.* $L$ linear
  in $\ddot x$" is a false equivalence, and it tested $\mu$'s Hessian rather than $L$'s. The correct
  argument: the $x^{(4)}$ coefficient **is** $\partial^2L/\partial\ddot x^2$, an $x^{(4)}$-free *vector*
  law forces it to vanish **identically** (not merely to be singular), that means linear in $\ddot x$,
  and that means an EL equation linear in $a$ — which the law is not. This excludes **all** local $L$,
  degenerate or not, where the old proof excluded only non-degenerate ones.
  **Theorem 8** (REDONE on the $\alpha=2$ kernel 2026-07-30; survives, mechanism replaced): the
  **nonlocal operator** action does not supply the amplitude. Its old reason — $|K_1|=1$ on the cut —
  was an $\alpha=1$ accident and is gone ($|K_2|=\sqrt{s/(1-s)}$ is *not* unimodular). The replacement
  is **kernel-independent**: on a circular orbit the action's argument is $w=c\Omega/a_0$ while the law's
  is $x=a/a_0$, and $w/x=c/v$ **exactly** — 300 to $7\times10^5$ for real systems. No choice of $K$
  repairs a mismatch in its own *argument*, and the deep regime is the regime *furthest* from the cut.
  **THE GAP IS ONE INEQUALITY:** $K(\langle\Box_u\rangle_u)\neq\langle K(\Box_u)\rangle_u$ — the closure
  swaps the function and the average. Theorem 1 gives $\langle\Box_u\rangle_u=+|a|^2$ exactly, so the
  first-moment closure is the left side and the action's variation is the right side. An action in the
  **scalar** $|a|^2$ has the right argument but is local (Thm 3 kills it); an action in the **operator**
  $\Box_u$ is nonlocal and allowed but has the wrong argument (Thm 8 kills it). **A solution must exhibit
  an action, nonlocal in the worldline, whose variation produces $K$ at the u-contracted first moment
  rather than at the operator's spectrum.** Milgrom's virial $f(u)$ does exactly that on circles — which
  is why the four-family no-go was withdrawn — so the object is not impossible, only unwritten off
  circles. Scripts: `mi_theorem3_corrected_proof_2026.py`, `mi_theorem8_redone_alpha2_2026.py`.
- **⭐ THE OFF-CIRCULAR ACTION, WRITTEN DOWN (2026-07-30) — the pincer is now *sharp*, with an explicit
  witness on the local horn.** `mi_offcircular_action_2026.py` (44 checks, exit 0). The action is
  $$S[x]=\int\!dt\;m\Big(|\dot x|^2\,f(|\ddot x|/a_0)-\phi(x)\Big),\qquad f(u)=u^{-2}\!\int_0^u\!v\,\mu(v)\,dv,$$
  with $f_1=[2u\sqrt{4u^2+1}-4u+\operatorname{asinh}2u]/(8u^2)$ ($\alpha{=}1$) and **NEW,
  $\alpha{=}2$: $f_2=[u\sqrt{1+u^2}-\operatorname{asinh}u]/(2u^2)$** — the corpus carried only $f_1$.
  Its honest EL equation is fourth-order:
  $\frac{d^2}{dt^2}\big[(|\dot x|^2/a_0)f'(u)\hat a\big]-2f(u)\ddot x-2\dot f\,\dot x=\nabla\phi$.
  **WHAT IS GAINED.** A circular orbit solves that *full* equation **exactly**, and the equation it
  satisfies is the framework's own closure $g_{\rm bar}=A\,\mu(A/a_0)$ — verified for **generic** $f$
  (sympy residual 0, so kernel-independent), plus both explicit kernels, with two negative controls
  failing as required. This **promotes** the corpus's earlier result, which varied only *inside* the
  two-parameter circular family and therefore never established that the real EL equation holds.
  $f''$ and $f'''$ are provably **absent** from the circular result — that is *why* circles are the
  family that works. Newtonian limit exact ($f(\infty)=\tfrac12$).
  **WHAT IT COSTS, and these are not footnotes.** (i) The acceleration-Hessian is not merely
  non-degenerate but **indefinite** ($f''<0$ along $\hat a$, $f'/u>0$ transverse, verified at 50-digit
  precision over 15 decades — a float64 scan reports thousands of *spurious* sign flips from an
  $O(u^3)$ cancellation, checked and discarded). So Ostrogradsky applies and $\omega_{\rm extra}^2<0$:
  the extra modes are **runaways**, e-folding in **0.57 s** at Earth and $5\times10^7$ yr at 30 kpc
  ($|\omega|/\Omega_{\rm orb}=2.8$ — *not* parametrically separated anywhere). Not a fundamental action.
  (ii) **Off circles it does not reproduce the closure.** A second exactly-solvable family (uniform
  straight-line acceleration) gives a *different* interpolating function $\mu_{\rm lin}=2(f-uf')$:
  deep-regime $u^3$ instead of $u^1$, i.e. **251× weaker at $u=0.1$ and 25 000× at $u=0.01$**.
  Measured residual on exact closure-solving eccentric orbits (deep regime, both footings): 0 at $e=0$
  to machine precision, then 0.033 at $e{=}0.01$, 0.33 at $e{=}0.1$, **2.7 at $e{=}0.6$** — order-unity,
  not a correction. Validated by a scaling ladder: residual $\propto u^{-1.00}$ ($\alpha{=}1$) and
  $u^{-1.84}$ ($\alpha{=}2$, predicted $-2$), so **the $\alpha=2$ switch cures the solar system off
  circles too** — the Newtonian residual falls below double precision and is *reported as unresolved*,
  not claimed as zero.
  **READ:** every observation the closure has been tested against — SPARC rotation curves, BTFR, RAR —
  is a **circular-orbit** measurement. Closure and action are the same theory there and different
  theories elsewhere. Prior art: Milgrom 1994 (Ann. Phys. 229:384) for the class, 2022 PRD 106:064060
  for single-frequency-only.
- **⚠️ THE LOCALLY-DRAGGED FRAME — SWUNG HARD 2026-07-31 AND LARGELY CLOSED. The door named below is
  narrower than it looked, and the reason is partly that my own framing of it was wrong.** Four
  independent routes, 48 adversarial verifiers (three lenses per surviving claim), **39/44 verdicts
  REFUTED**. All four routes returned PARTIAL. Scripts, all exit 0: `mi_machian_frame_routeA_2026.py`
  (64 checks), `route_b_memory_time_2026.py` (64), `mi_hierarchy_falsifier_routeC_2026.py` (55),
  `mi_route_d_dragged_frame_nogo_2026.py` (43).
  **THE FRAMING ERROR, corrected.** "The missing factor is a speed, and the preferred frame supplies
  one" **overstates it**: the framework *already* contains the object that supplies $c/v$. Theorem 1's
  u-contracted first moment gives $z=x^2=(|a|/a_0)^2$ directly — **no** frame speed, **no** drag
  prescription, **no** new dof. So $\tau_{\rm mem}=v_{\rm rel}/a_0$ is exact (2.55e-51 at 50 dps,
  independently reproduced) but is a **definition restated, not a mechanism**. It **does NOT pin
  $\omega_c$** — it trades one bounded constant for a free function plus a drag prescription, and an
  unfixed exponent alone moves $g_{\rm bar}$ by **4.46×** at $e{=}0.6$. Any claim that this pins
  $\omega_c$ would be false.
  **THE ONE CONSTRUCTION RESULT (real, and it kills my axisymmetry worry).** Hypersurface-orthogonality
  plus azimuthal periodicity makes the potential-stationary frame the **unique ZAMO**, with residual
  rotation costing **4.8e-7 dex** of $a_0$ against a 0.2232 dex budget. ⚠️ Holds only *within* the
  stationary axisymmetric congruence ansatz $u\sim(1,0,\Omega(R,z),0)$ — not a general proof.
  **WHAT IT COSTS, and this is what closes it.** (i) **Carina kills it on data already in hand**:
  predicted $\sigma\to$ **1.74 km/s** against **6.6 ± 1.2** measured = **4.05σ low**, and *p*-independent
  (a monotone-weight lemma pins $f\ge\tfrac12$ for all $p>0$); the framework's baseline predicts 4.77 km/s
  and fits. (ii) **Front B dissolves**: $s^{TX}$ goes 8.68e-10 (margin 1.50×) → **1.82e-17**, margin
  7.1e7× — one of the two live gravity fronts becomes unobservable. And Route B's frame **flips the
  frozen $s^{TX}$ sign** ($n_X$: −0.971 → +0.4941; the galactic-rotation apex is 131.5° from the Planck
  CMB apex). (iii) **It does not open the pincer**: Thm 3 still forbids all local $L$; Thm 8's mismatch
  is repaired *only on circles*, failing by 0.78–3.13× at $e{=}0.6$. (iv) RAR universality is **not** fully
  restored — worst corner injects 0.227–0.383 dex vs the 0.2232 budget (**1.72× over**, 2 of 9 cells
  fail); it converts a uniform 5× failure into a corner-dependent one.
  **ROUTE D's AIRTIGHT LEG:** exact co-motion requires $-\kappa_d\rho(x)=3$ **pointwise**, impossible for
  one global coupling on a varying profile. Solar-system ranging caps frame vorticity at **1/25** of the
  Milky Way's measured Oort vorticity (killing co-moving drag); the only construction meeting that cap
  for free is a potential flow leaving **84% of 135 real SPARC galaxies at >90% the cosmic frame**.
  ⚠️ Self-demoted: that bound derives from the *local witness action*, which is Ostrogradsky-unstable
  (above). **And I was wrong about which obstruction would close it** — I bet on passivity; passivity
  **survived** ($c_1=c_4$ gives zero propagating modes with spatial gradients intact). 2 of 6
  obstructions died. **A gravitomagnetic vector-drag corner at ~1e2 kpc is NOT closed**, nor is a frame
  sourced by the framework's own ghost-condensate Q-mode rather than baryons.
  **NOT closed, NOT a derivation of $a_0$, and $\kappa=\tfrac12$ still fitted.** Prior art: Mach;
  Sciama 1953; Milgrom 1994 already requires a definition of absolute acceleration for modified inertia.
  The Machian idea is **not** novel here.
- **⚠️⚠️ TWO DEFECTS FOUND INSIDE THE FROZEN DR4 PRE-REGISTRATION — AMENDMENT 4 FILED IN THE OPEN
  2026-07-31.** `mi_prereg_gext_argument_audit_2026.py`, 16 structural checks, exit 0; freeze manifest
  re-verified, all 5 pipeline hashes **unchanged**.
  **(1) The amendments feed ν the OBSERVED external field, not the Newtonian one.** ν takes
  $y=g_{\rm bar}/a_0$ *by construction* (sympy residual 0). Amendments 2 and 3 evaluate ν and
  $d(\nu g)/dg$ at $g_{\rm ext,obs}/a_0=1.8996$. Demonstrated, not asserted: the observed argument
  reproduces the frozen table to **3.3e-5** (A3) and **7.9e-4** (A2), the Newtonian argument misses by
  **1.1e-2** and **2.8e-2** — a **330× discrimination**, with a negative control (a deliberately wrong
  argument misses by 8.6e-2). **§1.1 already publishes the right quantity, `y_extN`, and §3's gate shape
  uses it — the amendments bypassed it.** ⚠️ **Same bug class as the forest chain (§5.1).**
  **(2) `y_extN` = 1.4647/1.1513 are the α=1 inversions** (confirmed to 4.3e-4/3.2e-4) and are **stale**
  under the α=2 kernel in force, where they are **1.6809/1.3280**.
  **CORRECTED (Amendment 4):** orientation-averaged γ_v 1.0246 → **1.0310**; full range 1.0182–1.0350 →
  **1.0218–1.0472**; γ∥ 0.9669 → **0.9636**; γ⊥ 1.0523 → **1.0631**.
  **BOTH Amendment 3 conclusions SURVIVE** (computed): still below the frozen band edge 1.05 on **4/4**
  combinations, and γ∥ still sub-Newtonian on **4/4** (0.9592–0.9688). Shift is 88×–716× the 4.1e-5
  reproduction tolerance — real, but too small to flip any pre-registered PASS/FAIL.
  **⭐ THE ERROR RAN AGAINST THE FRAMEWORK:** on every footing and both kernels the as-frozen numbers are
  **more Newtonian** than the corrected ones (|γ−1| = 0.0246 vs 0.0310), i.e. it made the wide-binary
  anomaly look *less* detectable. It manufactured a **deficit**, not a win.
  **⚠️ STILL OWED:** Amendment 3's **framework-as-MG row (1.0473–1.0885)** plausibly carries the same
  argument error and is **not** corrected; the **§2 s^TX Door-4B** numbers were not examined at all.
  Neither may be assumed sound.
- **⚠️ THE DR4 WIDE-BINARY AGGREGATE IS STRUCTURALLY DEAD as a hierarchy discriminator** — frozen
  $\sigma_{\rm sys}=0.02$ caps the γ_v separation at **0.91σ at INFINITE N**, not a sample-size problem.
  The better near-term handle is a **3.20–3.61× median dwarf-spheroidal dispersion deficit on archival
  data**, but this is a **LEAD, NOT A RESULT**: it uses $|a|=\sigma^2/R_h$ with no virial coefficient and
  $v_c=220$ km/s for every satellite (real orbits span ~50–350 km/s), and §5.4 already records dSph
  $\Upsilon_V$ systematics as coherent and dominant (0.322 dex = 8.7× the signal on the related test).
  Route C also found and fixed the **same Newtonian-vs-observed bug in its own first draft**, which had
  been understating this deficit by ~2×.
- **⭐ AND IT NAMES A DOOR, WITH ITS LOCK.** $u=w\,(v/c)$ **exactly** — so what Theorem 8 found missing
  is a **speed**, and the $|\dot x|^2$ prefactor is exactly how the local action supplies it. A speed is
  not an invariant of a lone worldline, which is *why* the covariant operator route failed; but this
  framework has a **passive preferred frame**, which does supply one. Target, now specific: a nonlocal
  worldline action whose kernel argument is the frame-relative frequency rescaled by the frame-relative
  speed. **The lock, computed not deferred:** a *cosmic*-frame speed is **excluded by the framework's own
  RAR** — peculiar velocities span ~1.0 dex against a total $a_0$ budget of $2\times0.108=0.216$ dex
  ($4.6\times$ over). The frame must be **locally dragged** so a star's frame-relative speed is its
  orbital speed, not its galaxy's bulk motion. Whether the passive $u$ does that is **not settled and
  not claimed**.
  **⚠️ ALSO NEW: the $\alpha=2$ kernel violates passivity for $z<-1$** ($K_2=w/\sqrt{w^2-1}>1$),
  by ~$10^{-13}$ at orbital frequencies and order 7 near the cut edge. It does **not** touch the $a_0$
  derivation, which uses $z>0$ only, where $0\le K_2\le1$ over sixteen decades — but it is a real cost
  of the switch and belongs in the ledger.
- **⚠️ THE LAW ITSELF — the rev.-4 reading, retained below for the record.** The
  law is **not** the Euler–Lagrange equation of the *published* action (Thm 8: on circular orbits that
  action's operator sits on $K$'s branch cut where $|K|=1$, so it is amplitude-free). **But my earlier
  "four-family no-go" OVER-REACHED and is withdrawn as stated:** the exact law *does* arise
  variationally in a **nonlocal, NON-quadratic** class — there is a closed form
  $f(u)=[2u\sqrt{4u^2+1}-4u+\mathrm{asinh}\,2u]/(8u^2)$ whose circular-orbit reduction
  $\mu=(1/u)\,\mathrm{d}(u^2f)/\mathrm{d}u$ returns $\mu_{\rm fw}$ **exactly** (sympy-verified), with
  the correct Newtonian ($f\to\tfrac12$) and deep-MOND ($f\to u/3$) limits. This is **Milgrom's own
  virial result** (arXiv:astro-ph/0510117). **SCOPE, and it is the honest limit:** $f$ pins the
  functional only on the two-parameter family of circles; infinitely many Galilei-invariant nonlocal
  extensions share that slice and none is written down. Milgrom's own status line applies — *"we do not
  have a MI theory for MOND at the level of satisfaction achieved for MG formulations."*

---

## 3. Live fronts

| # | front | state | clock |
|---|---|---|---|
| **A** | **Wide-binary $\gamma_v$ / gate fork** | pre-reg frozen 2026-07-16, hash-stamped; **Amendment 1** (2026-07-27) fixed a scoring defect that would have scored a confirmation as a kill; **Amendment 2** (2026-07-30) discharges the EFE prescription flag and adds an orientation-resolved statistic | **Gaia DR4, ~Dec 2026** |
| **B** | **$s^{TX}$ SME boost dipole** | prediction $8.68\times10^{-10}$ canonical / $1.048\times10^{-9}$ alt; bound $\sigma\sim1.3\times10^{-9}$ (Hees+ 2016) → margin **1.50× / 1.24×** | Gaia DR4 |
| **C** | **Rotation-curve dipole from the derived EFE** | **new 2026-07-30.** 4.2–22.3% for $e\ll y$, attractor-faster, **footing-free**. Retires the banked "MI predicts exactly zero directional asymmetry" and flips the observable from MI-blind to **MI-favourable** | archival + DR4 |
| **D** | **Dwarf-spheroidal closure discrimination** | **new 2026-07-30, then DOWNGRADED the same day by real data.** Predictions stand: ultralocal closure → dispersion-supported systems *exactly* on the rotation relation (1.6e-15); orbit-averaged → $-0.037$ dex. But the McConnachie (2012) catalogue (46 dwarfs, 29 after cuts) shows the test is **systematics-limited, not sample-limited**: per-object scatter 0.38–0.48 dex (not 0.15–0.20), and the dominant $\Upsilon_V$ error is **coherent**, so $\sqrt N$ does not help. $\Upsilon_V$ span 1–4 moves the mean residual 0.322 dex = **8.7× the signal**; needs $\Upsilon_V$ to 19% vs a 50–100% literature spread. **"N~150, archival" RETRACTED.** One route survives: the $\Upsilon$ direction has slope $-0.067$/dex against $\log(g_{\rm bar}/a_0)$ while the closure offset is flat, so partially separable over 5.28 dex — needs the offset computed *across* $g_{\rm bar}$ | **blocked on theory, not data** |
| **E** | **$a_0(z)$ evolution** | correct law is $(1+z)^{1.5(1+w_0+w_a)}e^{-1.5w_az/(1+z)}$ — **bump-then-decline**, not a rise. DESI-dependent signal only ~0.01 dex at $z=1$, sign-changing near $z\simeq1$, 0.11–0.20 dex by $z=3$ | **$z\gtrsim2$ test**; hostage to DESI |

**⚠️ On front A, the standing instruction:** a frozen pre-registration must be amended **in the open,
before data**. Both amendments to date were filed pre-DR4 and hash-stamped. Amendment 2 moved **no
frozen target** — the derived orientation average $\gamma_v=1.0799$ landed inside the frozen 1.05–1.10
band, 0.0101 from the point target 1.09.

**⚠️ Do not cite "~9.6× margin" for $s^{TX}$.** Superseded 2026-06-21. Live figure is 1.50× / 1.24×.

---

## 4. Closed — do not reopen without new physics

| door | why it is closed |
|---|---|
| Local-density $a_0$ ($a_0\propto\sqrt{G\rho_{\rm local}}$) | 10.5σ null on the framework's own SPARC environmental test, **plus** a structural trap: cluster cores are less dense than galaxy inners, so no density-monotone floor boosts clusters without boosting galaxies more |
| Forcing $\kappa$ | provably unforceable (ghost-freedom + unitarity + holography); CKN bridge closed |
| **Milgrom-2022 frequency-ratio route to the $\alpha=1$ planetary anomaly** | **closed 2026-07-30, three independent grounds.** (i) It cannot reach the planets: $\theta$ enters *additively* against $a_{\rm in}$ (his Eq. 34), and Earth has $a_{\rm in}/a_{\rm ex}=3.3\times10^7$, so any $\theta(0)$ of order a few leaves the $a_0/2$ anomaly bit-for-bit unchanged; the required $\theta(0)\sim4.3\times10^{10}$ is ten orders above his own examples. Deeper: the anomaly is a **single-frequency** effect and a ratio construction has no purchase on a one-frequency trajectory. (ii) The kernel is **exactly unimodular** on the oscillatory branch (sympy), so it cannot source $\theta$'s $y$-dependence. (iii) **Theorem B forces quadrature** — the argument is $\lvert a_{\rm tot}\rvert^2$ with a vector cross term, not Milgrom's linear $a_{\rm in}+\theta a_{\rm ex}$. **So $\omega_c$ is NOT shown unnecessary** — it was doing a job ratios structurally cannot do. Residue, reported but not promoted: $\theta$ *distinguishes* this framework from Milgrom's general MI family (his $\theta$ free, ours pinned to 1 by two theorems — a falsifiability virtue), but the two $\gamma_v$ predictions separate by **under 3σ** at the frozen DR4 error model, so it is not a near-term test. `mi_milgrom2022_theta_efe_2026.py` |
| Standard-Model / particle numerology | number-field obstruction: $Z$ carries $\sqrt\pi$ (transcendental), all flavour data algebraic → structurally gauge-blind. Exceptional door hosts but does not force the SM |
| Cluster no-particle theory programme | complete across both corpora. Residual is **real**, ~50–71% covered with no new particle. Shared with AeST by an in-corpus argument (MI $\equiv$ AeST to machine precision in static systems) — **"shared across the whole relativistic-MOND family" is that argument, not a published result**; see §5.4. Not framework-specific, not a referee-proof kill |
| Collective / clumpy EFE | redistributes only; **−0.95%**, wrong sign. Deep-MOND sub-additivity + enclosed-mass theorem |
| Bulk-flow 1.9× boost | all three routes closed: $\sigma_8$ (122σ), RSD $f\sigma_8$ (19σ), BAO/LSS shape |
| SN-Ia host-step as an $a_0$ effect | null. Global SDSS-size ($N{=}449$) and local-SB ($N{=}450$) both give ~0 beyond mass. Location coincidence stays coincidental |
| CMB / Tully–Fisher-evolution novelty | prior art: Gnedin 2008, arXiv:0809.2790 |
| "Apparent phantom dark energy from modified inertia" | **closed 2026-07-30, seven channels.** Mechanism doubly occupied prior art (arXiv:2605.27301 review; arXiv:2012.03446 puts Milgrom's $a_0$ in a modified Friedmann equation). Background channel closed *structurally* — see below |
| MI modifying the cosmological background | **structurally impossible** (Thm 4): comoving FRW makes $u$ an exact zero mode, $K(0^+)=0$, the term vanishes identically, and $K\sim\sqrt z$ leaves no perturbative expansion. $cH_0/a_0=7.00$ is a coincidence of **scales**, not a coupling |
| Dissipative / secular-drift channel | **identically zero** (Thm 2). Independently, the alternative closure's universal drift is excluded at **8.5σ** by PSR J0737−3039 |
| Local $a_0$ from dark-matter dynamics | same as row 1 — already closed by Carl's own SPARC test |
| `project_atomos` SM parameter search | null, published (DOI 10.5281/zenodo.21654272) after an audit withdrew two false claims |
| **Deriving the law from an action — all four families** | **closed 2026-07-30.** (1) Nonlocal, $K$ as an operator on $u$ (the *published* action): on a circular orbit $K$ is evaluated at the eigenvalue $-(c\Omega/a_0)^2$, on the cut, $\|K\|=1$ exactly — amplitude-free, and variation-generated $\mathrm{d}K$ terms are 4–13 orders too small (Thm 8). (2) Local, $F$ of the scalar first moment: nondegenerate at every finite acceleration, so 4th-order EL equation — *and* the acceleration Hessian is **indefinite**, i.e. Ostrogradsky-unstable. (3) Local + degenerate ($F$ linear in $\|a\|$, the unique escape): deep-MOND branch only, diverges from the law by +9950% by $a/a_0=100$. (4) Nonlocal velocity-bilinear (Milgrom 1994's class): EL equation *is* second order — but $\tilde Q$ is diagonal in **frequency** while the law is diagonal in **acceleration**, and at fixed $\Omega$ the required kernel value spans **19.7×** across radii. **General obstruction:** a fixed potential-independent kernel is diagonal in frequency by time-translation invariance; the law is diagonal in acceleration; $A=\Omega^2R$ ties the labels, so no such action reproduces the law for all potentials |
| Non-adiabatic relational σ-spread as a **near-term** discriminator | repriced **down 3–15×** on 2026-07-30 (1.45–2.21% max−min, 0.22–0.72% population RMS vs banked 6.2–14.1%). Still MG-impossible *in principle*; $N(3\sigma)$ at the ELT tier is ~2e5–2e7, past the whole CHANCES budget |

---

## 5. Open liabilities — stated plainly

0. **⚠️ THE SHARPEST ONE, AND IT IS NEW (2026-07-30): the exact law is excluded by the inner-planet
   ephemerides.** The signature relation $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ has
   $1-\mu\sim1/(2x)$ **identically** — the $\alpha=1$ class — so held to all accelerations it predicts a
   **constant sunward anomaly $a_0/2=4.68\times10^{-11}\,$m/s²** that does *not* decay as $a/a_0$ grows.
   This retires the corpus's own reasoning that "Cassini is safe because $a\gg a_0$ at the Sun"; that
   argument works for $\alpha\ge2$, not for $\alpha=1$.
   - **Bounds verified from primary sources, not quoted.** Sereno & Jetzer 2006 (astro-ph/0606197)
     Table 1 (Pitjeva EPM2004) inverted through their own Eq (9) gives $\delta A_R\le3.66\times10^{-14}$
     m/s² (Earth, 2σ) and $3.72\times10^{-14}$ (Mars). Bare $a_0/2$ is **1278× over**; the framework's
     *own* derived EFE (Thm 5) suppresses it only to **119–189× over**. Milgrom 2009 (arXiv:0906.4817)
     p.6 states the case verbatim: $\alpha=1$ "produces too strong effects on the planets"; Sereno &
     Jetzer "roughly allow only $\alpha\gtrsim1.5$". Blanchet & Novak 2011 call the class ruled out.
   - **The known escape does not reach.** Milgrom prefers Fienga+2009's global-refit method, which is
     ~200× looser — but those are **outer-planet** limits (Uranus/Neptune/Pluto), orbits loose enough
     to absorb a constant acceleration. It acts on *every* planet, its precession grows as $a^{1/2}$,
     and meter-level Earth/Mars ranging cannot absorb it into $GM_\odot$ or the semimajor axes.
   - **Galaxy data does not require $\alpha=1$** — verified on real SPARC, 175 galaxies: $\alpha=1$,
     $\alpha=2$ and $\alpha=\infty$ fit within **0.0084 dex** of one another at fixed $a_0$, and within
     0.019 dex in the highest bin at shared M/L, against Desmond 2023's $\sigma_{\rm int}=0.034$ dex.
     Only 5.2% of SPARC points reach $g_{\rm bar}/a_0>10$; the sample tops out at 110, the Earth sits at
     $\sim6\times10^7$. So the framework holds $\alpha=1$ **because its law forces it**, not because the
     rotation curves ask for it.
   - **Therefore the conflict is between exactness and the planets, and one of them must go.** The
     honest default: the relation is an **infrared** statement, empirically supported for
     $y\lesssim100$, where every galaxy datum lives — which costs nothing in SPARC but **withdraws the
     claim that it is exact**. The corpus does make that claim; it must be narrowed. The alternative is
     a frequency gate, which needs a fifth constant unless Milgrom 2022's frequency-*ratio*
     construction supplies it.
   - **⚠️ THE CONFLICT IS NARROWER THAN THIS ENTRY FIRST STATED — settled 2026-07-30 by the disformal
     swing.** It is **not** $a_0$-vs-planets. **$a_0$'s derivation does not depend on $\alpha=1$ at all.**
     Every premise that derivation uses — Herglotz–Nevanlinna positivity, passivity $\sup K=1$, the unit
     sum rule $\int\mathrm{d}\mu/|t|=K(\infty)-K(0)=1$, the horizon floor — is satisfied *equally* by the
     $\alpha=2$ kernel $K=\sqrt{z/(1+z)}$, which also keeps the deep-MOND $\sqrt z$ origin. Verified with
     two negative controls (a negative-measure and a $\sup K=2$ kernel) that are correctly rejected. So
     **the $a_0=cH_\Lambda/Z$ reframing — the one claim that survived the June 2026 retraction — is not
     at risk from this liability.** What is at risk is *exactness*, and only that: the relation
     $g_{\rm obs}^2=g_{\rm bar}^2+a_0g_{\rm bar}$ holds identically **iff** $\alpha=1$ (symbolic).
     Switching to $\alpha=2$ costs **+0.0033 dex** on 175 SPARC galaxies ($0.10\,\sigma_{\rm int}$) and
     takes the planets from 1279× over to $2\times10^{-5}$× — i.e. passing.
   - **And the disformal lensing construction sends a SECOND BILL for the same item.** $B$ is fixed by
     the same kernel, $\nabla B=4(\nu-1)g_{\rm bar}$, and the construction needs $B<1$. On $\alpha=1$,
     $(\nu-1)g_{\rm bar}\to a_0/2$ so $\mathrm{d}B/\mathrm{d}r\to2a_0$ is **constant** and $B$ varies by
     **257 (canonical) / 311 (alt) across Mercury→Saturn** — ~2 orders over its own premise; on
     $\alpha=2$ it varies by $1.3\times10^{-4}$. **This is not independent evidence** — $\mathrm{d}B/\mathrm{d}r$
     is exactly 4× the ephemeris anomaly, verified to $4\times10^{-9}$ — but it means keeping $\alpha=1$
     also costs the disformal construction, which §1 lists as **earned**.
   - **Recommendation the calculation supports:** adopt $\alpha\ge2$, keep $a_0=cH_\Lambda/Z$, withdraw
     the word *exact*. One word buys the ephemerides *and* the lensing construction. P8 (the loop-sector
     $\rho_m$ definition) stays **open** and nothing above depends on it.
   - Scripts: `real_research/reviews/mi_alpha1_solar_system_2026.py`,
     `real_research/reviews/mi_tail_exponent_rar_cost_2026.py`,
     `real_research/reviews/mi_disformal_tail_freedom_2026.py` (all exit 0).
1. **The diffuse-baryon sector — ⚠️ THE BANKED "~6–8σ, STRONGLY DISFAVOURED" IS WITHDRAWN (2026-07-30).
   This correction runs FOR the framework and is reported at the same weight as the ones against it.**
   Three independent defects, each found by adversarial verification and each inflating the constraint:
   - **The observed cutoff values were unsourceable.** The sequence $b_{\rm cut}=$ 15/17/22/24 km/s at
     $z=$ 3.70/3.35/2.85/2.30, introduced as "web-verified", matches no published table. Schaye+2000 has
     no table of fitted cutoffs at all — "16" and "22" are that figure's **y-axis tick labels**, on a
     *simulation* panel, with a Jeans/Hubble mechanism rather than a thermal one. The four *redshifts*
     trace to Schaye's sample medians (3.72/3.37/2.84/2.29) at mismatched pivots. Replaced by Hiss+2018
     (ApJ 865, 42) Table 4, eight bins with their own asymmetric errors.
   - **The error bar was invented, and in the flattering-to-the-test direction.** $\pm2.0$ km/s was a
     fiction. Hiss's statistical bars are 0.33–1.37 km/s — *tighter* — but the **calibration systematic
     is 3.36 km/s**, from Hiss's own §5.3 Rudie comparison (their 18.68 vs Rudie rescaled to their pivot
     15.32, ">3σ"), and is explicitly *not* in the Table 4 bars. Every significance must be quoted on
     **both** channels; the calibration one is the defensible one.
   - **★ The response kernel was evaluated at the wrong acceleration, in all four scripts and in the
     original corpus versions.** $h(x)=d(x\mu_{\rm fw})/dx$ takes the **observed** $x=|a|/a_0$; the
     scripts passed the **Newtonian** $y=g_{\rm bar}/a_0$. The framework's own closure gives
     $x=\sqrt{y^2+y}$, and in the deep regime $\sqrt{y}\gg y$, so the true response is
     $1/h\to1/(2\sqrt{y})$, **not** $1/(2y)$. Sympy-verified. At the corpus's own $x_{\rm rms}=0.0372$
     the conservative amplification is **1.65×, not 3.67×** — an inflation of 1.9–5.6× depending on
     estimator, propagating linearly into every σ. Restoring the wrong argument makes all three
     runnable scripts fail 8 internal checks, so the old checks passed *only* because of the mismatch.
   **The corrected numbers, both error channels, both footings:**

   | estimator | statistical | **calibration (defensible)** |
   |---|---|---|
   | $x_{\rm rms}$, CAMB total acceleration (**best treatment**) | 1.1–9.0σ | **0.4–0.9σ** |
   | after the density-conditioning lever | 1.0–8.5σ | **0.4–0.9σ** |
   | single-absorber convention (the primary script's own) | 4.1–26σ | **1.7–3.0σ** |
   | across all five $a_0$ forks (single-absorber $g$) | 3.7–70σ | **1.4–7.4σ** |

   **On the best estimator and the defensible channel this is 0.4–0.9σ — not an exclusion.** All eight
   Hiss bins fall below 3σ on the calibration channel, and five of eight fall below 3σ even
   statistically. The magnitude is **convention-owned to a factor ~32** ($x$ for forest gas spans
   $4\times10^{-5}$ to $6\times10^{-2}$ depending on absorber size and mass component — Aguirre, Schaye
   & Quataert 2001, ApJ 561, 550, is direct prior art on this exact test and puts it at the deep end).
   The *sign* of the effect is robust across every fork; the *exclusion* is not.
   **Counterweight, both ways:** Arnold, Puchwein & Springel 2015 (MNRAS 448, 2275) find even strong
   $f(R)$ leaves forest line widths "hardly affected at all" — but only $|f_{R0}|=10^{-4},10^{-5}$ were
   run (**not** $10^{-6}$), the Voigt line-width null is established for $10^{-5}$ only, and $f(R)$ is
   screened and modifies the Poisson source whereas MI amplifies the velocity response of unscreened
   low-acceleration gas. It does **not** transfer as positive evidence either way.
   **AND THE SAME ERROR WAS IN THE GROWTH/σ₈ CHAIN, where it was worth a factor 59.** The forest
   scripts inherited $h$ from `mi_growth_amplification_founded_2026.py`, and that script is
   *inconsistent* row by row: every bound-structure row enters by a **measured** $v^2/R$, which *is*
   $|a|$ and was always right; but the **diffuse-IGM** row enters by a Newtonian
   $(4\pi/3)G\rho_m\delta R$, and the **filament** row by an *assumed* $v=100$ km/s that disagrees with
   the $g_{\rm bar}$ of its own matter by **162×**. The framework's law forbids this: given
   $g_{\rm bar}$, $|a|$ is *determined*, so no row may supply both. Re-done under one convention —
   measured $|a|$ where one exists, otherwise $g_{\rm bar}$ converted through $x=\sqrt{y^2+y}$:

   | quantity | banked | consistent |
   |---|---|---|
   | diffuse IGM amplification | 135 | **8.25** |
   | WHIM/filament amplification | 722 | **4.58** |
   | baryon-weighted $\langle 1/h\rangle_b$ | ~357 | **6.08** |
   | total-matter growth amplification | — | **1.80** canonical / 1.89 alt |
   | required suppression vs the 1σ budget | ×10²–10³ | **×7–41** |

   So the "×650–3500 suppression, impossible" framing is **withdrawn**. Against the defensible
   growth budget (CMB-lensing+BAO $\sigma_8=0.829\pm0.009$ ⇒ ≤1.011 at 1σ, ≤1.033 at 3σ) it is still
   **24.5× over at 3σ** — reduced by a factor ~59, **not closed**. Two things are untouched: the
   **non-analyticity** objection ($K\sim\sqrt{z}$ at the FRW expansion point, $K'(0^+)$ divergent) needs
   no amplification number at all, and every galaxy-scale result is unaffected because the RAR's
   0.108 dex never depended on $h$. Script: `mi_growth_kernel_argument_audit_2026.py`, exit 0.

   **Status: a real but WEAK tension, 0.4–3σ on the defensible channel, convention-dominated.** Not
   "strongly disfavoured". The regulator is still wanted — the σ-spread and the non-analyticity
   arguments (§5.2, $K\sim\sqrt{z}$) stand on their own — but the forest is no longer the thing forcing
   it. Scripts: `mi_forest_bcut_data_2026.py` (shared verified data + the kernel derivation),
   `mi_forest_b0_convention_audit_2026.py`, `mi_lyalpha_forest_b_test_2026.py`,
   `mi_forest_total_acceleration_2026.py`, `mi_forest_conditional_accel_2026.py`,
   `mi_forest_a0_footing_forks_2026.py` — all exit 0, 41 checks, all structural (no encoded verdicts).
2. **The closure-vs-action gap — RESOLVED, NEGATIVELY, 2026-07-30.** No longer "not established": the
   law is **not** the EL equation of any fixed-kernel action, across four families (§4). Theorem 1's
   **moment identity** stands and is exact; what does not exist is a variational derivation.
   **And the variational route leads out of modified inertia:** the only evasion of the general
   obstruction is a kernel sourced by matter, i.e. potential-dependent — which is modified *gravity*,
   with the structure in a field equation rather than in inertia. This is consistent with the corpus's
   own repeated finding that MI $\equiv$ AeST($=$MG) to machine precision in static systems, and with
   the published lensing construction being **disformal** (a metric statement) rather than an inertia
   statement. What survives as *distinctively* modified-inertia, needing no variational law: the EFE's
   quadrature $+$ vector-cross-term structure with its footing-free RC dipole (Thm 5), and the
   dispersion-supported closure discriminator (Prop 7). The residual freedom is a single function $w$
   (the time-weighting), and Prop 7 measures it on archival dwarfs.
3. **Cassini $Q_2$ quadrupole.** A **3–15σ** tension that the framework's AeST(=MG) realisation
   *inherits* (Desmond-Hees-Famaey 2024; Park+ 2026). The γ-pass is MOND-shared and trivial.
   **Cassini is not a favourable in-hand discriminator** — corrected 2026-06-28.
4. **Clusters — numbers corrected 2026-07-30, and the correction runs against the framework.** Real,
   soft, central, not a kill; but three of the four figures previously carried here were wrong.
   - **$\eta(R_{500})=2.334$ median / $2.542$ geomean** raw on eRASS1 (Bulbul+2024, $N=9830$,
     $f_\star=0.20$) using the framework's **own** kernel $\nu=\sqrt{1+1/y}$. The old headline $2.149$
     was the **simple-$\mu$** number — a mislabel, and judging the framework through a foreign $\nu$ is
     against §8's own rule. So was the significance block: it read $+0.372$ dex and 3.7/2.5/1.9σ. On
     the framework's own kernel it is **$+0.405$ dex and 4.05/2.70/2.03σ** against a 0.10/0.15/0.20 dex
     absolute-scale floor. **Quote the floor-limited number; the 367σ statistical figure is
     meaningless here.** Applying the repo's own rule correctly makes the deficit *worse*.
   - **$\eta\sim1.6$–1.8 is a weak-lensing mass-calibration result, not an XRISM one** (Li+2024: WL
     runs ~110% above hydrostatic *and* kinematic, which agree with each other).
   - **XRISM: the old framing is withdrawn, but the replacement is narrower than "XRISM tightens" —
     I overstated this first and am correcting it.** What is solid: every primary XRISM measurement is
     *small*, so the claim that XRISM licenses a large non-thermal component and thereby softens the
     cluster problem is **withdrawn outright**. A2029 core $2.6\pm0.3\%$ (ApJL 982, L5) and $\le2\%$ at
     all radii out to $R_{2500}=670$ kpc *decreasing outward* (PASJ 77, S242); Coma centre
     $3.1\pm0.4\%$ (ApJL 985, L20 = arXiv:2504.20928 — **not** A&A 704, A35, which the corpus miscited);
     Perseus $\sim$0.5–5% over most of the map (A&A 707, A109); X-COP "hydrostatic masses require
     little correction", median $5.9^{+2.9}_{-3.3}\%$ at $R_{500}$ and $10.5^{+4.3}_{-5.5}\%$ at
     $R_{200}$ (Eckert+2019, A&A 621, A40; 12 tabulated clusters despite its own abstract saying 13).
     $P_{\rm nth}$ *raises* a thermal $\eta$ ($M_{\rm true}=M_{\rm HSE}/(1-f_{\rm nth})$) and cannot
     lower it. **But it does not close the front either, and four things cut the other way:**
     (i) radius-matched against Kelleher & Lelli's requirement the factors are only **1.7–6.8× at
     $R_{500}$ and 0.95–3.8× at $R_{200}$ — i.e. the ranges *overlap* at $R_{200}$**; (ii) the XRISM
     velocity measurements all stop *inside* 1 Mpc and so do not bound a requirement stated at
     $r>1$ Mpc; (iii) individual clusters reach 15–44% at $R_{500}$ (A2319 $43.6\%$), and Eckert's own
     mean-level bound is 13%; (iv) Coma's kinetic fraction inside $R_{500}$ rises to
     $10^{+8}_{-4}\%$ once large-scale bulk motions are folded in (A&A 704, A35), and Perseus's
     *outermost* regions are the high ones ($\gtrsim10\%$) — the direction the MOND comparison needs.
     Correct phrasing: **"does not relieve, does not close."** The repo's own
     `SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER_2026-06-15.md` had the direction right and the summary layers
     drifted from it; the retired bracket "post-XRISM $\eta\in[1.0,2.33]$" still reads as relief.
   - **Kelleher & Lelli's requirement needs three qualifiers that the corpus dropped.** Their 10–40%
     is (a) the **minimum**, obtained *with a maximal external field effect* — without EFE it is
     10–100%; (b) stated at **$r>1$ Mpc, i.e. beyond $R_{500}$** (they fit to 1 Mpc precisely because
     bias should be minor inside it); (c) a fractional **mass/acceleration** residual, not
     $P_{\rm NT}/P_{\rm tot}$ — the two agree only to ~30% (median ratio 1.10 at $R_{500}$). They report
     **no value at $R_{500}$ at all**, so the corpus's $\eta(R_{500})\sim1.0$–1.3 is *not* a
     Kelleher–Lelli number and must not be cross-quoted against their $R_{\rm out}$ column. Their
     $M_{\rm mm}/M_{\rm bar}$ at $R_{\rm out}$ is 0.38–1.10 (relaxed, EFE) and 3.99–5.43 (mergers) —
     the figures 1.38–2.10 and 5.0–6.4 in circulation are exactly $1+M_{\rm mm}/M_{\rm bar}$, i.e.
     total-to-baryonic, and were being compared against the wrong quantity.
   - **The cluster acceleration scale, as a method-and-radius ladder rather than one number.** Tian,
     Umetsu, Ko, Donahue & Chiu 2020 (ApJ 896, 70; arXiv:2001.08340) give
     $g^{\ddagger}=(2.02\pm0.11)\times10^{-9}$ — note **$g^\ddagger$, double dagger**: they reserve
     $g^\dagger$ for the *galaxy* value $1.20\times10^{-10}$, and writing $g^\dagger=2.02\times10^{-9}$
     inverts their notation. Slope $0.51^{+0.04}_{-0.05}$, and the scatter on the slope-fixed fit that
     actually yields $2.02\times10^{-9}$ is $14.5\%$ (the $14.7\%$ in circulation is the free-slope
     fit); residual spread 0.11 dex. Verbatim: "there is no universal RAR that holds on all scales from
     galaxies to clusters" — though the same paper also finds the CLASH RAR consistent with a ΛCDM
     semi-analytic model, so that line is not an endorsement of modified inertia.

     | method | scale (m s⁻²) | × canonical $a_0$ | dex |
     |---|---|---|---|
     | CLASH lensing, 100–600 kpc (Tian+2020) | $2.02\times10^{-9}$ | 21.6 | 1.334 |
     | X-ray, at $r_c$ (Chan & Del Popolo 2020) | $1.9\times10^{-9}$ | 20.3 | 1.308 |
     | X-ray, at $2r_c$ | $1.2\times10^{-9}$ | 12.8 | 1.108 |
     | X-ray pooled, 52 non-cool-core | $9.5\times10^{-10}$ | 10.2 | 1.006 |
     | member-galaxy dynamics, 29 HIFLUGCS (Tian+2021) | $(0.8$–$2.2)\times10^{-9}$ | 8.5–23.5 | 0.93–1.37 |
     | X-ray, at $3r_c$ | $3.9\times10^{-10}$ | 4.2 | 0.620 |
     | Coma, The & White 1988 (**lower bound** $2h_{50}^{1.5}$) | — | $\ge3.1$ at $H_0{=}67.4$ | $\ge0.49$ |

     So the published factor spans roughly **3× to 24×**, it **grows toward cluster centres** (stated in
     Chan & Del Popolo), and the pooled X-ray value is interpolation-loaded (their Eq. 1 is McGaugh's
     e-folding $\nu$, so a framework-native refit would move it). **"$17\times$" is a real published
     phrase** — Tian+2024 (A&A 684, A180; arXiv:2402.12016) abstract: "a seventeen times larger
     acceleration scale by the gravitational lensing effect" — but the arithmetic behind it is
     $2.02/1.20=16.8$, the ratio to **McGaugh's galaxy $a_0$**. Applied to *this* framework it must be
     rescaled to **21.6× (1.334 dex) canonical / 17.9× (1.252 dex) alt**, so quoting 17× here
     understated the framework's own gap by 28%. There is **no "Tian & Ko 2016" cluster paper** — that
     is MNRAS 462, 1092 on elliptical galaxies, which adopts $a_0=1.21\times10^{-10}$ and makes no
     cluster claim; do not cite it. Against Desmond 2023's RAR universality budget
     ($\sigma_{\rm int}=0.034$ dex $\Rightarrow\pm0.068$ at 1σ), 1.334 dex is **19.6× over at 1σ,
     6.5× at 3σ**.
   - **The framework's own coefficient costs it here:** $\sqrt{1.20\times10^{-10}/9.36\times10^{-11}}
     =1.132$, so $\eta$ is **13.2% worse** than standard MOND (alt footing: 3.1%). Erasing $\eta$ needs
     $a_0\times\eta^2=\mathbf{\times5.45}$ (+0.736 dex).
   - **Does the cluster constraint transfer to a modified-inertia reading? It does — and the quote the
     corpus would want to lean on is truncated.** Kelleher & Lelli §2.2, in full: "Equation (5) is also
     valid in MOND modified inertia theories in the case of isolated systems with purely circular orbits
     (Milgrom 1994), which is clearly not the case for the random gas motions in the ICM. **In this
     work, therefore, we are primarily testing MOND modified gravity theories, albeit we expect Eq. (5)
     to provide the correct order of magnitude also in modified inertia theories (for isolated
     systems).**" The bolded clause is the half that gets dropped, and it reverses the rhetorical force.
     So: their *exact numbers* are not MI predictions to better than order of magnitude — fair — but the
     residual is itself an order-of-magnitude-level object, and the framework's own repriced
     non-adiabatic σ-spread is only **1.45–2.21%** max−min
     (`prep_2026/sigma_spread/GAP_STATEMENT.md` Amendment 1), which cannot close a ~100% residual.
     **The escape does not work, and the corpus should say so explicitly instead of leaving it implicit.**
   - **"Shared across the whole relativistic-MOND family" is an argued pattern, not a published
     theorem.** The in-corpus argument (MI $\equiv$ AeST to machine precision in static systems) is
     sound for MI-vs-AeST. But Skordis & Zlosnik 2021 does not discuss clusters, Durakovic & Skordis
     2023 claim only "potential", and Famaey/Pizzuti/Saltas 2024 call it "an open question". §4's
     phrasing ("shared across the whole relativistic-MOND family") overstates this and should read
     *argued in-corpus*.
   - Script: `real_research/reviews/clusters_eta_audit.py`.
5. **"No dark matter" is forfeited.** The framework *has* a dark sector — the AeST/ghost-condensate
   Q-mode, a gravity mode rather than a particle. Honest framing: MOND galaxies **plus** a
   no-particle CDM-like sector.
6. **arXiv endorsement** remains the blocker on everything that matters.

---

## 6. Retractions and corrections in force

- **2026-06-23, public:** all TOE / Standard-Model claims. Never to be revived.
- **2026-07-30:** "pure MI predicts *exactly zero* directional asymmetry" — **wrong**. An artifact of
  the borrowed scalar-θ ansatz; quadrature has a vector cross term, so orientation survives.
- **2026-07-30:** treating the sign $s$ as a parameter awaiting data — superseded by Cor 2.2.
- **2026-07-30 (paper v2):** Proposition 7's observational forecast — "~1.2–1.9σ on 40–60 dwarfs, 3σ at
  $N\sim150$, both routes archival." Retracted after running it on McConnachie (2012): the test is
  systematics-limited by a **coherent** $\Upsilon_V$, so $\sqrt N$ does not apply. Props 7.1/7.2 stand.
- **2026-07-30:** any phrasing that the law is **"derived from"** the action. Correct phrasing is
  "a law with an action-based motivation and an exact moment interpretation" (§2). Four action families
  checked and closed; the law is a fit that is exact as a first moment.
- **2026-07-30:** "the phase acts only on perturbations (epicycles, tides, waves)" in
  `KERNEL_THEORY.md` — **incoherent**, retire it. Theorem B applies pointwise to the total
  acceleration and returns one non-negative real number.
- **2026-07-28:** the σ-spread band 6.2–14.1% — repriced down; `GAP_STATEMENT.md` Amendment 1.
- **Standing:** $s^{TX}$ margin is 1.50×/1.24×, **not** ~9.6×. $\alpha_2^{\rm MI}\sim10^{-13}$
  (~$10^6\times$ safe), **not** $10^{-8}$ and not live.
- **Assistant-side errors corrected the same day, recorded so they are not re-inherited:** a wide-binary
  Zenodo release that stripped 9 reproducibility files (fixed as v4); a growth-amplification figure
  using the large-scale peculiar acceleration where Theorem B specifies the element's own, and
  $1/\mu_{\rm fw}$ where the linear response is $1/h$; an external-field balance that omitted the
  host's own acceleration and inflated the dipole to 129%; a conditional-acceleration direction
  asserted before the parity argument was checked.

---

## 7. Published record

| DOI | what |
|---|---|
| 10.5281/zenodo.21707845 | **Structural Theorems for dS–Unruh Modified Inertia** (7 results, 2026-07-30) |
| 10.5281/zenodo.21706870 | Crispy Dark Matter — accommodation ledger. **Conditional, methodological; not a physics claim** |
| 10.5281/zenodo.21702746 | Wide-binary $s^3$ gate law, v4 ($\kappa$ reduction + closure narrowing) |
| 10.5281/zenodo.21264727 | MI action v4 |
| 10.5281/zenodo.21284144 | one-loop dS edge (v11) |
| 10.5281/zenodo.21654272 | `project_atomos` null |
| 10.5281/zenodo.20779562 | AeST phase no-go |

## 8. Rules for anyone working on this

1. **Test the framework on its own terms.** It is modified *inertia* with a horizon-derived $a_0$ and
   its own interpolation. Never judge it through the standard-MOND lens; never use McGaugh's $\nu$.
2. **Verify a deficit as rigorously as a win.** Manufacture neither.
3. **Run both footings on every dimensional number**, and show the spread.
4. **Back every load-bearing claim with a committed, runnable script** that exits non-zero on a failed
   internal check. No hard-coded verdicts.
5. **Never say "the theory is closed."**
6. **Amend frozen pre-registrations in the open, before data.**
7. **Nothing personal in this repository** — no email addresses, no correspondence.
