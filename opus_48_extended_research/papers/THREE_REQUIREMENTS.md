# Three Requirements on a Relativistic Home for MOND Phenomenology

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
2026-08-18

---

## Abstract

Aether-Scalar-Tensor gravity (AeST; Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302) is
the only relativistic MOND-class theory reproducing the CMB power spectrum, and it contains a
single free function $\mathcal{F}(\mathcal{Y},\mathcal{Q})$ that its authors leave
unspecified. We show that specifying it is obstructed, and we extract from the obstruction
three necessary conditions on *any* relativistic completion of MOND phenomenology. Each is
established by an explicit construction that satisfies the previous conditions and fails the
next.

**(R1)** The free function must depend on the gradient of the **total** potential, not on the
scalar's own. With $\mathcal{F}(\mathcal{Y})$ the quasi-static reduction forces the anomalous
acceleration $U(y)$ to be monotone increasing, hence to saturate at some $U\to s$, hence to
produce a *constant* sunward anomaly $s\,a_0$ at every planetary distance. Perihelion
precession then requires $s\le1.27\times10^{-5}$ while the radial acceleration relation
requires $s\ge0.435$ — **incompatible by $1.2$–$3.4\times10^{4}$.** There is no
external-field relief: computed for this family rather than imported, it is $1.000000\times$.

**(R2)** The cosmological background must not coincide with the deep-MOND end of the
interpolation. Replacing $\mathcal{Y}$ by $Z\equiv J^\mu J_\mu$, the squared aether
acceleration, satisfies R1 exactly — $J^i=\nabla^i\Psi$ with unit coefficient, the reduction
becomes AQUAL, the exponential interpolation becomes legal, and the 1 AU anomaly falls to
$10^{-3458.7}\,\mathrm{m\,s^{-2}}$, voiding the gap. But $\bar Z=0$ identically on FRW, so
linear cosmology sees $K_B\to K_B-\mathcal{F}_Z(0)$, and any $\mathcal{F}$ performing the
interpolation has $\mathcal{F}_Z(0)=K_B$ exactly: the aether's electric kinetic coefficient
vanishes and the perturbation equation degenerates.

**(R3)** Neither may be purchased with a split between the cosmological and local
gravitational constants. Rescaling the free function repairs both R1 and R2 simultaneously,
but forces $\tilde G/G_N\le0.121$ — an $8.3\times$ split — which gives $Y_p=0.086$ against an
observed $0.2449\pm0.0040$ ($-42\sigma$), and a gravitational radiation density *below that of
the photons alone*, whose value is fixed by FIRAS with no gravity in the chain.

We also record a structural identity, verified three times independently: AeST's action
already contains an explicit $+(2-K_B)a^\mu a_\mu$, so its apparent $c_4=0$ is an artifact of
variables. And $c_T=1$ holds exactly, for any free function, derived rather than quoted.

---

## 1. Setup

AeST's action, verified verbatim against the authors' LaTeX (arXiv:2007.00082 Eq. 5, restated
independently as arXiv:2109.13287 Eq. 1):

$$S=\int d^4x\,\frac{\sqrt{-g}}{16\pi\tilde G}\Big[R-2\Lambda-\frac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\varphi-(2-K_B)\mathcal{Y}-\mathcal{F}(\mathcal{Y},\mathcal{Q})
-\lambda(A^\mu A_\mu+1)\Big]+S_{\rm m}[g]$$

with $\mathcal{Q}=A^\mu\nabla_\mu\varphi$,
$\mathcal{Y}=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\varphi\nabla_\nu\varphi$,
$F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}$, and $J^\mu=A^\nu\nabla_\nu A^\mu$ the aether's
acceleration. Matter couples to $g_{\mu\nu}$ alone.

Throughout we use the acceleration scale $a_0=\kappa c\sqrt{G\rho_\Lambda}=
9.3619\times10^{-11}\,\mathrm{m\,s^{-2}}$ (an alternative footing gives
$1.1279\times10^{-10}$; both are carried). $\kappa=\tfrac12$ is fitted, not derived: three
determinations give $0.551\pm0.043$, $0.465\pm0.076$ and $0.537\pm0.071$, combining to
$0.529\pm0.034$. Write $y=g_{\rm bar}/a_0$ and $U(y)=u/a_0$ for the anomalous acceleration.

---

## 2. R1 — the free function must eat the total gradient

With $\mathcal{F}(\mathcal{Y})$, the quasi-static gradient sector diagonalises: $\Psi=\Psi_N+\chi$
with $\nabla^2\Psi_N=4\pi\hat G\rho$, and in spherical symmetry Gauss's theorem gives the local
algebraic law $u\,J_Y(u^2)=g_{\rm bar}$ with $u=|\nabla\chi|$. The scalar's own gradient *is*
the anomalous acceleration. Reconstructing the free function from a chosen interpolation gives
$J_Y(Y)=y(U)/U$, invertible iff $U$ is strictly increasing; equivalently the longitudinal
eigenvalue of $M_{ij}=J_Y\delta_{ij}+2J_{YY}u_iu_j$ is positive under the same condition. A
non-monotone $U$ means both a multi-valued $\mathcal{F}$ and a longitudinal gradient ghost.

**This is specific to AeST.** In AQUAL the free function depends on the total potential's
gradient and stability requires only $dg_{\rm obs}/dg_{\rm bar}>0$ — satisfied by the
exponential interpolation $\nu=1/(1-e^{-\sqrt y})$, minimum $0.968$. The same kernel is legal
in one theory and fatal in the other, purely from which gradient the free function eats.

Monotonicity plus $U/y\to0$ forces saturation, $U\to s$: a constant sunward anomaly $s\,a_0$
at every planetary distance. By the Gauss planetary equations a constant radial perturbation
gives $\dot\varpi=s\,a_0\sqrt{1-e^2}/(na)$; against EPM/INPOP-class anomalous-precession limits
the worst planet requires

$$s\le1.27\times10^{-5}\ \text{(canonical)},\qquad 1.05\times10^{-5}\ \text{(alt)}.$$

Applying $U(2)\ge0.4$ to the family $J_Y=v/(1-v/s)$, $v=\sqrt{Y}/a_0$, gives $s\ge0.4348$;
relaxing to a global fit (rms $\le0.15$ dex on 3389 SPARC points, $\Upsilon$ in the Spitzer
band) gives $0.157$–$0.294$ depending on treatment.

$$\boxed{\text{GAP: }1.2\text{–}3.4\times10^{4}.}$$

Every candidate relief was computed and none helps. **The external-field effect contributes
nothing**: derived for this family by two independent routes (an $\ell=1$ penetration ODE and
a flux bound requiring no perturbation theory), the relief on the saturated anomaly is
$1.000000\times$ — the external field screens *itself*, not the anomaly, and somewhere on the
1 AU sphere the anomaly is at least $s\,a_0(1-4\times10^{-9})$. A density-dependent $a_0$
*hurts*: with suppression $f$ the constrained product is $s f$, and $f\,U_s(2/f)=0.4$ gives
$0.435$ at $f=1$ but $2.00$ at $f=0.1$, unsatisfiable below $f=0.080$ because $U\le\sqrt y$
caps the family. Solving the non-spherical problem for a Miyamoto–Nagai disc raises the
required floor by 1.07–1.10. Refitting $\Upsilon$ buys $1.34\times$.

---

## 3. R2 — the cosmological background must not be the deep-MOND point

R1 says: use the total gradient. AeST already contains the object that supplies it. With
$D^\mu=q^{\mu\nu}\nabla_\nu\varphi$ one has the identity, verified three times independently
and requiring no computer algebra,

$$2(2-K_B)J\!\cdot\!\nabla\varphi-(2-K_B)\mathcal{Y}\;\equiv\;+(2-K_B)Z-(2-K_B)|D-J|^2,
\qquad Z\equiv J^\mu J_\mu .$$

**AeST therefore already contains an explicit $+(2-K_B)a^\mu a_\mu$: its apparent $c_4=0$ is
an artifact of variables.** And $J^i=\nabla^i\Psi$ with coefficient exactly 1, with $Z$'s
leading coefficient independent of $\varphi$, $\Phi$ and the aether perturbation — so $Z$ *is*
the total potential gradient squared.

Replacing $\mathcal{F}(\mathcal{Y},\mathcal{Q})$ by $\mathcal{F}(Z,\mathcal{Q})$ then works
exactly as R1 requires. The aether-longitudinal equation becomes $v=\nabla\Psi$ pointwise, the
$(1+J_Y)$ factor disappears, and the reduction is **AQUAL exactly**, with
$\mu(g_{\rm obs})=J_Z(g_{\rm obs}^2)$ and $\hat G$ unchanged. The exponential kernel becomes
legal (min $dx/dy=0.968$, against min $dU/dy=-0.032$ under $\mathcal{F}(\mathcal{Y})$ for the
same kernel), and the 1 AU anomaly becomes $10^{-3458.7}\,\mathrm{m\,s^{-2}}$ — some
$10^{3445}$ below the Sereno–Jetzer bound, replacing an $s\,a_0$ that sat $1279\times$ above
it. Further, $c_T^2=1$ exactly for any free function (the TT sector sees neither the aether nor
the scalar: on a pure TT perturbation $J^\mu=0$, $Z=0$, $F_{\mu\nu}F^{\mu\nu}=0$, $\mathcal{Y}=0$,
all exactly), and $G_N$ is finite and equal to the unmodified value.

It fails on cosmology, for a reason that is the exact inverse of what protects
$\mathcal{F}(\mathcal{Y})$. On FRW the aether is $A^\mu=(1,0,0,0)$ and its acceleration
vanishes, so $\bar Z=0$ **identically** — the cosmological background *is* the deep-MOND end
of the interpolation. Expanding about it, the $O(\epsilon^2)$ action carries
$[K_B-\mathcal{F}_Z(0)]Z^{(2)}$, so linear cosmology sees $K_B\to K_B-\mathcal{F}_Z(0)$. Any
$\mathcal{F}$ that performs the MOND interpolation has $\mathcal{F}_Z(0)=K_B$ exactly, so the
coefficient vanishes and the aether's electric evolution equation collapses to a constraint.
$\mathcal{F}(\mathcal{Y})$ escapes only because $J_Y(\bar{\mathcal{Y}}=0)=0$.

---

## 4. R3 — and neither may be bought with a $\tilde G/G_N$ split

Both sector conditions constrain only the total $Z$-coefficient: static attraction needs it
positive, vector no-ghost needs it below $K_B$. Rescaling the free function, $J\to sJ$,
satisfies both at every acceleration for $s<K_B/(2-K_B)$, and — the point — also repairs R2,
since the rescaled normalisation gives $K_B-\mathcal{F}_Z(0)=K_B$ exactly on the deep-MOND
branch. The window is $0<s<0.138$ at $K_B=0.25$. The solar-system screening is untouched,
being $s$-independent.

The price is that with $\mathcal{F}(Z)$ the non-$\mathcal{F}$ static Lagrangian is annihilated
identically by $v=\nabla\Psi$, making the free function's normalisation the sole source of
Newton's constant: $G_N=\hat G/s$. The no-ghost condition is therefore equivalent to
$2\tilde G<K_B G_N$, i.e.

$$\tilde G/G_N\le0.121\quad(K_B=0.25),\qquad 0.048\quad(K_B=0.10),$$

against AeST's $0.875$ — an $8.3\times$ to $20.7\times$ split between the cosmological and
local gravitational constants. It cannot be paid:

- **Big-bang nucleosynthesis.** $Y_p=0.086$ at the no-ghost ceiling against an observed
  $0.2449\pm0.0040$: $-42\sigma$ from the same calculation's $\tilde G/G_N=1$ control. A
  closure-free bound assuming no nucleosynthesis model at all still gives $Y_p\le0.176$,
  $-17\sigma$.
- **The CMB, and this is an inconsistency rather than a tension.** The gravitational sector's
  radiation density comes out at $0.20$ of the thermal photon density — *below the photons
  alone*, whose value FIRAS fixes with no gravity anywhere in the chain. The equivalent
  $N_{\rm eff}=-3.5$. The hard floor is missed by $4.9\times$ ($K_B=0.25$) to $12.2\times$
  ($K_B=0.10$), and the ceiling sits $139\sigma$ from viability in cosmic-variance units.
- **Gravitational waves.** A claimed exact blindness of the standard-siren amplitude to $s$
  holds only for a tensor-only flux ledger; on the repaired ledger the escape predicts
  $d_L^{\rm GW}/d_L^{\rm EM}=7.99$ against a measured $0.983\pm0.349$. Accepting the
  tensor-only ledger instead makes matters worse, bounding $K_B<0.013$ and widening the split
  to $154\times$.

---

## 5. What is and is not claimed

**Claimed.** The three requirements, each with an explicit construction that satisfies its
predecessors and fails it. The identity of §3 and its corollary that AeST's $c_4=0$ is a
choice of variables. That $c_T=1$ holds exactly in AeST and in the $\mathcal{F}(Z)$ theory for
any free function. That the monotonicity obstruction of R1 is genuinely escapable, and what
escaping it costs.

**Not claimed.** That the requirements are sufficient — they are necessary conditions
extracted from three failures, and a completion satisfying all three is not thereby viable.
That $\kappa=\tfrac12$ is derived; it is fitted, and must be quoted with its $H_0$, the
distance-free determination carrying an unpriced $\sim7\%$ systematic. That dark matter is
absent: $\Omega_{\rm dm}$ is full here and the claim is "no dark-matter *particle*". Whether
the dark sector's dust remains bound inside galaxies is unresolved and untouched by any of
this — it is a $\mathcal{Q}$-sector problem, and all three constructions modify the
$\mathcal{Y}$-sector.

**Unaffected by any of the above**, being independent of which completion carries them: the
normalisation $a_0=\kappa c\sqrt{G\rho_\Lambda}$, the radial acceleration relation at 0.108 dex
on 175 SPARC galaxies, weak lensing from 40 kpc to 2.2 Mpc with no dark component, the
baryonic Tully–Fisher relation, and a hash-frozen wide-binary prediction decided by Gaia DR4.

**What a viable completion must supply.** A screening mechanism that is not a non-monotone
interpolation (R1), whose free function's argument does not vanish on FRW or whose derivative
vanishes there (R2), and which does not separate the cosmological and local gravitational
constants (R3). Superfluid constructions, in which the MOND force exists only inside a
condensate phase and there is no interpolation function to have a deep-MOND end, satisfy R2
vacuously and are the obvious next candidate.

---

**Reproducibility.** Every number is produced by a committed self-checking script at
<https://github.com/carlzimmerman/zimmerman-formula>: `real_research/reviews/typeII_*_2026.py`
(the quasi-static reduction and R1), `opt1_*_2026.py` and `c14_*_2026.py` (the
$\mathcal{F}(Z)$ construction, the identity, and R2), `esc_*_2026.py` (R3),
`a0_local_ephemeris_2026.py`, and `nbody_2026/stage7*.py`. Each prints numbered checks and
exits non-zero on failure. Withdrawn claims are recorded, dated, in `RETRACTIONS.md`.

**Attribution.** AeST is Skordis & Złośnik, *Phys. Rev. Lett.* **127**, 161302 (2021),
arXiv:2007.00082, with arXiv:2109.13287. The interpolation family is Milgrom & Sanders,
*ApJ* **678**, 131 (2008). PPN aether results are Foster & Jacobson, *Phys. Rev. D* **73**,
064015 (2006). The constant-acceleration bound is Sereno & Jetzer (2006); anomalous-precession
limits are EPM/INPOP-class (Pitjeva & Pitjev 2013; Fienga et al. 2011). Superfluid dark matter
is Berezhiani & Khoury. The $a_0$–$\Lambda$ coincidence has prior art in Milgrom (1999),
Blanchet & Le Tiec (2009), Pikhitsa (2010) and Klinkhamer & Kopp (2011).
