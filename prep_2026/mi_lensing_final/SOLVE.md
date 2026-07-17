# Single-Metric Lensing from the Full Assembled Stress Tensor of the MI Action — the Lensing-RAR Crux

**Purpose.** Complete the banked-open calculation (`MATTER_COUPLING.md` open edges; gap C):
assemble the **TOTAL** gravitating stress tensor of the de Sitter–Unruh modified-inertia action
(matter variation **and** the frame-constraint variation), linearize Einstein on **one metric**
(photons on $g$ — the only route surviving today's GW170817 erratum, the disformal photon metric
being excluded by ~6–7 orders), and compute the predicted **lensing RAR** for a real galaxy.
THE CRUX: $F(y) = g_{\rm lens}/(\nu(y)\,g_{\rm bar})$ — does the derived tensor supply the missing
deflection ($F=1$) or does the theory under-lens ($F\sim 1/\nu$, the banked trilemma)?
Confront Brouwer et al. 2021 (KiDS-1000 isolated lensing RAR, official release + full covariance).
**Both $a_0$ footings** (canonical $9.36\times10^{-11}$, alt $1.13\times10^{-10}$) throughout.
No "proves" language; honest rails both ways (no manufactured save, no manufactured kill).

**Scripts (exit 0, runnable):**
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/mi_lensing_final
python3 total_stress.py    # the assembly: kernel identities, 3 variation bookkeepings, conservation
python3 lensing_solve.py   # linearized equations, magnitude analysis, galaxy solve, Brouwer chi2
```
Inputs read (frozen repo, READ-ONLY): `prep_2026/mi_field_theory/MATTER_COUPLING.md`,
`BASELINE_ACTION.md`; data `real_research/data/lensing_rar/brouwer2021_rar/`
(`Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` + covariance, official B21 release, SIS conversion
$g_{\rm obs} = 4G\,{\rm ESD}/{\rm bias}$ per the release README).

---

## 1. The assembly (`total_stress.py`, machine-verified)

Action, signature $(-{+}{+}{+})$, quasistatic first-moment reduction $K(\Box_u/a_0^2)\to K(X)$,
$X=|a|^2/a_0^2$ (**nonlocal-variation caveat flagged**, §5):

$$S = S_{\rm EH} - \int\!\sqrt{-g}\,\tfrac{\lambda}{2}(u\!\cdot\!u+1)
      - \tfrac12\int\!\sqrt{-g}\,\rho_m\,s\,(u\!\cdot\!u)\,K(X),\qquad s=-1.$$

**Kernel identities on the RAR shell** ($|a| = g_{\rm obs} = \nu g_{\rm bar}$; sympy-exact):

| identity | value | meaning |
|---|---|---|
| $K\big|_{\rm on-shell}$ | $=1/\nu(y)$ **exactly** | the source dressing is a **suppression by exactly $1/\nu$** |
| $K'X\big|_{\rm on-shell}$ | $=\dfrac{y}{2(2y+1)\sqrt{y^2+y}}$ | the anisotropic stress weight |
| $2K'X/K$ | $=\dfrac{1}{2y+1}\le 1$ **exactly** | anisotropic/isotropic ratio: an $O(K)$ correction, never $O(\nu)$ |

**The three variation bookkeepings** (all machine-verified, exact-numeric 40-digit):

- **Matter, fixed-scalar $\rho$ (the doc's §2c):** $T^m = -\rho sK\,uu + \tfrac12\rho s(u\!\cdot\!u)K\,g + \rho s(u\!\cdot\!u)\tfrac{K'}{a_0^2}aa$ — **MATTER_COUPLING.md reproduced exactly**.
- **Frame sector:** $T^u = -\lambda\,uu$ (+ on-shell-vanishing $g$-term); the $u$-equation's algebraic
  $\ell=0$ part fixes $\lambda = -\rho sK$ (reproduced).
- **ASSEMBLY I (doc-literal free frame, $T^m+T^u$):** the $u_\mu u_\nu$ coefficients **cancel
  exactly** ($-\rho sK$ vs $+\rho sK$). Total $= \tfrac12\rho sK\,g + \gamma\,aa$. UV anchor
  $K\to1$, $s=-1$: $\rho_e = +\rho/2$, $p=-\rho/2$, $w=-1$, $\rho+3p=-\rho<0$ — **repulsive,
  $\Lambda$-like; dust does not gravitate. FAILS the theory's own Newtonian sector (D6).**
  Honest finding: the "$\lambda$ soak" that makes the frame passive in the $u$-equation
  **un-gravitates matter in the metric equation** under the free-frame reading.
- **ASSEMBLY II (free frame + dust closure $\delta(\sqrt{-g}\rho)=0$):** total $=\gamma\,aa$ only —
  zero energy density. **FAILS harder.**
- **ASSEMBLY III (composite frame $u=J^\mu/|J|$, mass-conserving dust — the standard GR dust
  bookkeeping applied to the dressed action):** $u\!\cdot\!u=-1$ **identically for every metric**
  $\Rightarrow S_u\equiv0$, $T^u\equiv0$ (no cancellation, no leg), and
  $$T^{\rm III} = \tfrac12\rho K\,u_\mu u_\nu - \tfrac{\rho K'}{a_0^2}a_\mu a_\nu \;(s=-1)
  \;\xrightarrow{K\to1}\; \tfrac12\rho\,u_\mu u_\nu = \textbf{dust. PASSES.}$$
  Newton calibration (the doc's own normalization note) fixes the physical total:
  $$\boxed{\;\hat T_{\mu\nu} = \rho\,K(X)\,u_\mu u_\nu \;-\; 2\,\frac{\rho K'(X)}{a_0^2}\,a_\mu a_\nu\;}$$
  On the RAR shell: $\rho_{\rm eff} = \rho K = \rho/\nu(y)$ (suppression), radial stress
  $\Pi = -\rho_{\rm eff}/(2y+1)$ (tension), $p_t = 0$. [Doc-$\gamma$ fork ($aa$ term halved)
  carried as robustness — verdict unchanged, $\max|\Delta F/F|$ printed.]

**The assembly fork is decided by the theory's own established Newtonian sector**: an assembly in
which the Sun does not gravitate (I, II) is a bookkeeping inconsistency, not a reading. III is the
unique Newton-consistent assembly and is what is carried to the lensing solve. The I/II failure is
itself a **real, reported finding** about the free-frame formulation of $S_u$.

**Conservation.** $\nabla_\mu T^{\mu\nu}=0$ on-shell is structural (diffeomorphism invariance);
the canonical Noether identity is machine-instantiated on the MI kernel (residual
$1.7\times10^{-16}$, machine zero). For the static spherical source the $r$-component of
$\nabla T=0$ **is** the orbit equation of the assembled theory (quantified in §4 — the internal
tension).

---

## 2. The derived linearized equations (`lensing_solve.py` step 1, sympy)

Gauge $ds^2 = -(1+2\Phi)dt^2 + (1-2\Psi)(dr^2+r^2d\Omega^2)$; sources $T^t_t=-\rho_{\rm eff}$,
$T^r_r=\Pi$, $T^\theta_\theta=0$. Read off the linearized Einstein tensor (derived, not assumed):

$$\textbf{(P)}\ \nabla^2\Psi = 4\pi G\,\rho_{\rm eff},\qquad
  \textbf{(S)}\ \Phi' - \Psi' = 4\pi G\,r\,\Pi,\qquad
  g_{\rm lens} \equiv \tfrac12(\Phi'+\Psi') = \Psi' + 2\pi G\,r\,\Pi .$$

**Magnitude analysis (the task's derive-don't-assume question):** every source term is
$O(K)\le1$: $\rho_{\rm eff}/\rho = 1/\nu \le 1$ and $|\Pi|/\rho_{\rm eff} = 1/(2y+1) \le 1$
(and $\Pi<0$: the anisotropic $K'$ stress **reduces** lensing slightly). In deep MOND
$K\to\sqrt z = |a|/a_0$ and $K'z\to K/2$ — exactly the task's noted scalings. **No $O(\nu)$
term exists anywhere in the assembled tensor.** The $K'\,a_\mu a_\nu$ stress is *not* the missing
deflection; it is a bounded $O(K)$ tension correction. Verdict is forced before any numerics:
the single metric under-lenses.

---

## 3. The real-galaxy solve — THE CRUX $F(y)$

Galaxy: $M_{\rm bar}=5\times10^{10}M_\odot$ — Hernquist stars $4\times10^{10}$
($a_*=2$ kpc, $R_{\rm eff}=3.6$ kpc) + gas $1\times10^{10}$ (Hernquist proxy $a_g=10$ kpc;
profile choice flagged, conclusions are $y$-driven not profile-driven). Matter on RAR-shell
orbits: $|a| = g_{\rm obs} = \nu(y)g_{\rm bar}$ (the framework's own dynamics), so
$K = 1/\nu(y(r))$ locally. Solve (P)+(S), deflection $\alpha(b)$ validated on a point mass
(recovers $4GM/c^2b$ to <1%).

**$F(y) = g_{\rm lens}/(\nu g_{\rm bar})$, both footings** (canonical / alt):

| $y$ | $F$ (canonical) | $F$ (alt) | $1/\nu(y)$ (trilemma) |
|---|---|---|---|
| 10   | 0.877 | 0.865 | 0.954 |
| 3    | 0.747 | 0.737 | 0.866 |
| 1    | 0.563 | 0.553 | 0.707 |
| 0.3  | 0.355 | 0.347 | 0.480 |
| 0.1  | 0.211 | 0.206 | 0.301 |
| 0.03 | 0.114 | 0.111 | 0.171 |
| 0.01 | **0.064** | **0.062** | 0.0995 |

$M_{\rm eff}(\infty)/M_{\rm bar} = 0.601$ (canonical) / $0.578$ (alt): the source itself is
dressed **down** by the mass-weighted $1/\nu$. Hence
$$F(y) \simeq \frac{M_{\rm eff}(r)}{M_{\rm bar}(r)}\cdot\frac{1}{\nu(y)} \;<\; \frac{1}{\nu(y)}:$$
**the theory under-lenses by MORE than the banked trilemma factor** — the trilemma is now exact
with the full tensor. Deflection at $b=10/30/100$ kpc: $\alpha_{\rm MI} = 0.097''/0.038''/0.012''$
= $0.288/0.111/0.034\times$ the $F{=}1$ value. Doc-$\gamma$ fork: $\max|\Delta F/F| = 4.1\%$ over
$y\in[0.01,10]$; verdict identical.

$F=1$ (lensing completed) is **not** what the assembled action delivers. $F<1/\nu$ is.

---

## 4. Conservation and the internal worldline-vs-field tension (quantified, not hidden)

The $r$-component of $\nabla_\mu\hat T^{\mu\nu}=0$ gives the assembled theory's own orbit law
$v^2/r = \Phi' + (\Pi' + 2\Pi/r)/\rho_{\rm eff}$. Numbers (canonical):
$a_{\rm FT}/(\nu g_{\rm bar}) = 0.518 / 0.203 / 0.064$ at $y = 1 / 0.1 / 0.01$, while
$\Phi'/g_{\rm lens} = 0.92$–$0.99$ — on the field side, dynamics $\simeq$ lensing (slip is the
small $O(K'X)$ $\Pi$ term): the assembled single-metric theory is *internally* consistent, but its
own field dynamics sit at the **same suppressed level as its lensing** — i.e. the assembled
$T_{\mu\nu}$ does not reproduce the worldline RAR that fits SPARC.
The worldline sector (ring-exact RAR, D5) and the assembled field sector cannot both hold; the
discrepancy lives in the same quasistatic/first-moment closure freedom as gap A. This is the
banked trilemma made exact, at the level of the full tensor including the frame legs.

---

## 5. The nonlocal-variation caveat (flagged honestly)

$K(\Box_u/a_0^2)$ depends on $g$ through the connection inside $\Box_u$ and $a^\mu$. The
quasistatic first-moment reduction keeps the algebraic legs; the dropped derivative (dipole) legs
are $\sim\nabla(\rho K' u\,a)/a_0^2$ — bounded by the **same** $O(\rho K'X)\le O(\rho K/2)$ order
as the retained $a_\mu a_\nu$ term ($2K'z/K \in [0,1]$ for all $z$, sympy-exact). They live inside
the gap-A closure freedom and **cannot supply an $O(\nu)$ factor** (no $\nu$ appears in any kernel
structure). The off-circular/nonlocal completion remains the named open door — it is the only
place a different closure could change this arithmetic, and it would have to produce an $O(\nu)$
enhancement from terms whose every bound is $O(K)$.

---

## 6. THE CONFRONTATION — Brouwer 2021 (KiDS-1000 isolated lensing RAR)

Official release, $N=15$ points, $g_{\rm bar}\in[1.4\times10^{-15}, 3.9\times10^{-12}]$, full
covariance, SIS conversion per the release README. Reliability rail (banked):
isolation clean at $g_{\rm bar}\ge10^{-13}$ ($N=7$); below $10^{-14}$ systematics dominate.
Models: **(F=1)** lensing RAR = dynamical RAR, $g=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$ (the
framework's own $\nu$); **(MI)** the single-metric prediction $g_{\rm lens}$ from §3.

| footing | rail $\Delta\chi^2$ (MI − F=1) | formal $\sigma$ | full-range $\Delta\chi^2$ | $\sigma$ |
|---|---|---|---|---|
| canonical | **+722** | ~27 | +1496 | ~39 |
| alt       | **+754** | ~28 | +1565 | ~40 |

Deficit at the rail edge ($g_{\rm bar}=1.3\times10^{-13}$): predicted $8.0\times10^{-14}$ vs
measured $6.0\times10^{-12}$ — **1.9 dex short, ~13σ in that single point**. Profiling a free
±0.3 dex coherent amplitude shift (stellar-mass / SIS-conversion systematics) does not rescue it:
rail $\chi^2(F{=}1)\to22.0$, $\chi^2({\rm MI})\to737$, $\Delta\chi^2 = 715$ (~27σ) canonical
(alt: $21.8$ / $742$ / $721$, ~27σ) — the MI **slope** is wrong ($g_{\rm lens}\propto g_{\rm bar}$
deep vs measured $\propto\sqrt{a_0 g_{\rm bar}}$); no coherent systematic fixes a slope.
Mistele–McGaugh 2024 (point-mass deprojection, same sky) extends the measured equality deeper;
the exclusion only grows.

*(Absolute-$\chi^2$ note, honest both ways: even F=1 has imperfect absolute $\chi^2$ on this
conversion/mass convention — the banked lensing-RAR standing (convention-compatible,
footing-non-diagnostic) is not re-litigated here. The MI-vs-F=1 **gap** is what this calculation
decides, and it is decisive under every nuisance treatment tried.)*

**Conclusion: Brouwer's measured lensing-RAR = dynamical-RAR equality directly falsifies
single-metric pure MI (this action, this assembled $T_{\mu\nu}$, photons on $g$) as the complete
theory — at ~27σ formal on the conservative rail, both footings, robust to the γ-fork and to
coherent amplitude systematics.**

---

## 7. Where the theory stands (the honest map, both outcomes named in advance)

- **Cassini:** safe. Solar source dressing $1-K\sim a_0/2g\sim10^{-13}$; slip vanishes exactly in
  vacuum ($\Pi\propto\rho$); anisotropic correction at Saturn $1/(2y+1)=7\times10^{-7}$;
  $\nu-1=7\times10^{-7}$ (the banked deep-Newton pass; the AeST/MG $Q_2$ caveat stays banked).
- **GW170817:** automatic — one metric, $c_\gamma = c_{\rm GW}$ exactly.
- **Dynamics + cosmology sectors:** untouched by this result (worldline sector, ring-exact RAR,
  loop-protected $a_0$ — as banked).
- **Lensing:** with the disformal photon metric excluded (GW170817 erratum) and the single-metric
  route now computed exactly: **the completion statement becomes — the theory is complete up to
  its constants in the dynamics + cosmology sectors, with lensing requiring physics beyond the
  current action.** The named remaining doors: (i) the off-circular/nonlocal closure (gap A) —
  would need to conjure $O(\nu)$ from $O(K)$-bounded structures; (ii) a lensing carrier beyond
  $S_{\rm EH}+S_u+S_{\rm matter}$ (a dark component or a new sector); (iii) the free-frame $S_u$
  bookkeeping itself (Assembly I/II failing Newton is a formulation-level wound worth closing).
- The F=1 outcome ("K′ supplies the missing deflection") is **excluded by derivation**: the
  anisotropic term is $O(K)$-bounded and tension-signed. No manufactured save was available;
  none was conjured.

*Every load-bearing number above is printed by the two committed scripts (exit 0). Both $a_0$
footings carried. No completeness claim; no "proves" language.*
