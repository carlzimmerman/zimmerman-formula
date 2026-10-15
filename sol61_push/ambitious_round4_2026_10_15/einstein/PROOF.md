# An actual static Einstein/current/gauge/wall body at critical charge

EINSTEIN-JOIN-1, 15 October 2026. **An explicit weak-field branch exists for
the minimally covariantized joined critical body**, with both positive-density
fluids varied, proper conserved stocks, the full bulk Hilbert stress, an
uncharged Nambu–Goto wall satisfying both Israel equations, and a genuine
Maxwell/Reissner–Nordström exterior. The existence proof is a quantitative
contraction on the complete coupled static equations, uniform in
`eta=1/c^2` from zero through `1/10000`; it is not a numerical shooting claim.
The selected EOSs, occupied phase and reflecting wall remain inputs.
No GR stability conclusion is imported from the previous hybrid theorem.

The inherited originals are preserved. Five read-only source snapshots and
their SHA-256 values are in `inputs/source_manifest.json`; the definition and
finite-run contract were pinned before computation in `inputs/definitions.json`
and `contract.json`. The requested base was
`a553a4a663d393f29ec5da69c8cae68c164bb5b0`; this work executed in the existing
dirty shared checkout, whose actual HEAD is recorded in the snapshot/run
manifests. Only this `einstein/` directory was edited by its author.

## 1. Covariant action and frozen definitions

Use signature `-+++`, one gauge potential, two separately conserved number
currents, positive particle rest masses, and the dark current frame only:

\[
 n_a=\sqrt{-N_a^2},\quad \rho_a=m_an_a,\quad U_c=N_c/n_c,
 \quad q_b=0,\quad q_c/m_c=\zeta=\sqrt{4\pi G}>0.
\]

In covariant formulas set `c=1`, restoring it in the equations below. The
action is Einstein–Hilbert with its boundary terms, the inherited diagonal
current actions `-epsilon_a(n_a)+N_a.(dtheta_a+alpha_a dchi_a)`, dark minimal
coupling `+q_c N_c.A`, and

\[
 \int_\Omega\!\sqrt{-g}\,[L_e(E_{U_c})-\tfrac12\beta(E_{U_c},h_c)B_{U_c}^2]
 +\int_{\Omega^c}\!\sqrt{-g}\,[-F_{\mu\nu}F^{\mu\nu}/4]
 -\sigma\int_\Sigma\!\sqrt{-\gamma}.
 \tag{1}
\]

Here beta is precisely the smooth occupied-center coefficient of the frozen
vacuum proof. Both fluids are impermeable at the same varied timelike
boundary, `N_a.n=0`; ideal contact enforces their common normal velocity
without an external source of work. The wall has constant positive area
energy/tension sigma, surface stress `S^i_j=-sigma delta^i_j`, no free gauge
charge/current, and no separately conserved wall particle number. This
reflecting phase/contact interaction is a chosen effective physical premise.

The EOSs, electric function and Hamiltonian are

\[
 P_a=K_a\rho_a^2,\quad \epsilon_a=\rho_ac^2+P_a,\quad
 w_a=2K_a\rho_a,\quad \epsilon_a+P_a=\rho_a(c^2+w_a),
\]
\[
 L_e=D_0E-D_0^2\log(1+E/D_0),\quad
 D=L_e'=\frac E{1+E/D_0},\quad E=\frac D{1-D/D_0},
\]
\[
 x=D/D_0,\quad H=ED-L_e=D_0^2[-x-\log(1-x)],\quad
 \Delta H=H-D^2/2>0.                                  \tag{2}
\]

All densities in this document are proper rest densities. All mass functions
have mass units. Fix the dimensionally assigned scales

```
R=D0=rho_b0=1, G=1/100000000,
rho_c0=f=1341/250, Kc=1/100, Kb=f(1+f)/100,
eta=1/c^2 in [0,1/10000].
```

Finite positive eta gives the Einstein body. Eta zero denotes its smooth
classical limit, not a spacetime with a finite speed of light. The central
density ratio f and EOS constants are inputs; total proper-stock ratios are
outputs. Critical charge refers to the actual dark charge/rest-mass ratio,
not its charge/ADM-energy ratio.

## 2. Hilbert stress from this action, including the varied frame

On the static co-moving pure-electric state, the first variation with respect
to the normalized dark frame vanishes: `E^mu F_mu nu=-E^2 U_nu` and
`U.delta U=0`. The beta term and every first derivative of beta vanish at
`B=0`. This also removes its explicit stock derivative from the background
chemical potential. These statements follow after variation, without
holding the frame externally fixed.

For the metric variation, take a local diagonal metric
`diag(-a^2,b^2,z_1^2,z_2^2)` and `F_tr=f_0`. At fixed current vector
density, its normalized static direction is `U^t=1/a`, so
`E=f_0/(ab)` and `sqrt(-g)=ab z_1 z_2`. The logarithmic metric-scale
derivatives of `sqrt(-g)L_e` are `L_e-ED`, `L_e-ED`, `L_e`, `L_e`.
Consequently the **actual Hilbert gauge stress**, in its rest orthonormal
frame, is

\[
 T^{\hat\mu}{}_{\hat\nu,\rm gauge}
       =\operatorname{diag}(-H,-H,L_e,L_e).             \tag{3}
\]

The current minimal/Clebsch terms are metric independent in vector-density
form. Each fluid supplies its ordinary perfect-fluid stress. Hence with
`P=P_b+P_c` the complete interior stress has

\[
 \epsilon=\epsilon_b+\epsilon_c+H,\quad
 p_r=P-H,\quad p_t=P+L_e.                             \tag{4}
\]

Gauge energy, internal energy, radial gauge tension and tangential gauge
stress all gravitate. They have not been replaced by a rest-density Poisson
source. The negative wall pressures likewise enter both junctions below.

## 3. Complete static Einstein, Gauss and two-current equations

Write

\[
 ds^2=-e^{2\nu(r)}c^2dt^2+\frac{dr^2}{F(r)}+r^2d\Omega^2,
 \quad F=1-\frac{2Gm(r)}{c^2r}.
\]

The independent bulk equations are

\[
 m'=\frac{4\pi r^2}{c^2}(\epsilon_b+\epsilon_c+H),\qquad
 \nu'=\frac{G[m+4\pi r^3(P-H)/c^2]}{c^2r^2F},         \tag{5}
\]
\[
 S_a'=\frac{4\pi r^2\rho_a}{\sqrt F},\quad
 Q'=\zeta S_c',\quad D=\frac Q{4\pi r^2},\quad
 w_b'=-(c^2+w_b)\nu',\quad
 w_c'=-(c^2+w_c)\nu'+\frac{\zeta E}{\sqrt F}.          \tag{6}
\]

`S_a` is the proper conserved rest stock, not `m_a` in the old Poisson
construction. The minimal force uses the actual proper charge density
`zeta rho_c`. At the center `m=Q=S_a=0`, `w_a=w_a0`; regularity gives
`m,Q,S_a=O(r^3)`, `D,E,nu'=O(r)`. No interior source is held fixed.

For a potential with `Phi'=-e^nu E/sqrt(F)`, the current equations integrate
to `e^nu(c^2+w_b)=constant` and
`e^nu(c^2+w_c)+zeta Phi=constant`. The static conserved currents and
Clebsch potentials realize these constants, so solving (5)–(6) also solves
the first-order background current equations.

An explicit consistency check retains the gauge pressure anisotropy:

\[
 P'=-(\epsilon_b+\epsilon_c+P)\nu'+\zeta\rho_cE/\sqrt F,
 \quad H'=E(\zeta\rho_c/\sqrt F-2D/r),
\]
\[
 p_r'=-(\epsilon+p_r)\nu'+2(p_t-p_r)/r.              \tag{7}
\]

Thus the angular Einstein equation follows from the other Einstein equations
and the contracted Bianchi identity; no missing held-source force is needed.

The dimensions provide separate checks: `eta P` and `eta H` have mass-density
units; `Gm/(c^2r)` is dimensionless; `zeta E/sqrt F` is specific-energy
gradient; `4pi G sigma/c^4` has inverse-length units. The exact critical
identity is `zeta^2=4piG` in the specified rationalized gauge normalization.

## 4. Quantitative contraction for a whole finite-radius GR branch

Set `eta=c^-2`, `m=(4pi/3)r^3 v`, `Q=(4pi zeta/3)r^3 y`, and

\[
 A=\frac{4\pi Gr[v/3+\eta(P-H)]}{F},\quad
 F=1-\frac{8\pi}3G\eta r^2v,\quad D=\zeta r y/3.
\]

On continuous functions over `[0,1]`, use the closed product box

\[
 .99w_{a0}\le w_a\le w_{a0},\qquad
 6.3\le v\le6.4,\quad5.30\le y\le5.37.               \tag{8}
\]

The four integral maps are

\[
 T_v=\frac3{r^3}\int_0^r s^2[\rho_b+\rho_c+\eta(P+H)]ds,
 \quad T_y=\frac3{r^3}\int_0^r s^2\rho_c/\sqrt F\,ds,
\]
\[
 T_b=w_{b0}-\int_0^r(1+\eta w_b)A\,ds,
\]
\[
 T_c=w_{c0}-\int_0^r\left[(1+\eta w_c)A
             -\frac{4\pi Gs y}{3(1-x)\sqrt F}\right]ds.\tag{9}
\]

At zero, the averaged maps take their continuous limiting values. The Banach
norm is

\[
 \|\delta Z\|=\max(\|\delta w_b\|/w_{b0},
   \|\delta w_c\|/w_{c0},\|\delta v\|/100,\|\delta y\|/100).
 \tag{10}
\]

Here are uniform bounds for **every function in this box** and
`0<=eta<=10^-4`, not just for computed profiles. Using `pi<4` and
`zeta<1/2500` gives

\[
 F>F_*:=1-10^{-9},\quad x<X:=10^{-3},\quad
 H<\frac{X^2}{2(1-X)}<10^{-6},\quad E<10^{-3}.
 \tag{11}
\]

Let `P0=Kb+Kc f^2<1`. Then `P>=.99^2 P0>H` and

\[
 .99(1+f)>6.3,\quad1+f+\eta(P_0+10^{-6})<6.4,
 \quad .99f>5.30,\quad f/F_*<5.37.
\]

Thus the averaged density maps stay in the box. Both hydrostatic integrands
point inward: for the dark integrand it suffices to use

\[
 6.3-\frac{5.37}{(1-X)F_*}>0.                         \tag{12}
\]

Indeed `1+eta w_c>=1`, `eta(P-H)>=0`, `1/F>=1`, and
`1/sqrt F<=1/F_*`. The maximal enthalpy drop, after discarding the outward
electric contribution, is below `25G=2.5*10^-7`, strictly below
`.01 min(w_b0,w_c0)`. Hence the entire map preserves (8). Both species
remain positive all the way to the finite material edge.

For completeness, its uniform differential bounds are also explicit. If
`N=||delta Z||`, then

\[
 |\delta\rho_a|\le\rho_{a0}N,\quad|\delta P|\le2P_0N,
 \quad|\delta F|<2\cdot10^{-9}r^2N,
\]
\[
 |\delta F^{-1}|<3\cdot10^{-9}N,\quad
 |\delta F^{-1/2}|<2\cdot10^{-9}N,\quad
 |\delta H|<N/75000.
\]

The last inequality is `H_D=E<.001` and
`|delta D|<=r N/75`. Dividing the averaged map variations by their norm
scales gives `q_v<.07`, `q_y<.061`. In the force integrand,
`C=v/3+eta(P-H)<3`, `|delta C|<34N`; these imply
`|delta A|<6*10^-6 r N`. The electric term has derivative in y
proportional to `(1-x)^-2`, and its total variation is below
`5.5*10^-6 r N`. Integrating and using `w_b0>.6`, `w_c0>.1` gives each
enthalpy row below `.001`. Therefore

\[
 \|T(Z_1)-T(Z_2)\|<.08\|Z_1-Z_2\|.                 \tag{13}
\]

The exact conservative arithmetic supporting all displayed strict
inequalities is checked separately by `check_einstein.py`. The mathematical
argument is the uniform box/derivative calculation, not the check count.
Banach's theorem supplies a unique fixed point in (8) for every eta in the
interval. Differentiating the integral equations gives (5)–(6) and the
regular center limits. Smooth dependence on eta follows from the smooth
maps and the uniformly invertible `1-DT` (Neumann series). Consequently this
is an actual weak-field branch connecting the classical joined interior to
finite-c Einstein solutions at unchanged critical zeta. The theorem states
local uniqueness in this box, not global uniqueness among all stars.

## 5. Maxwell exterior, both wall junctions and the actual ADM mass

There is no free surface charge, so Q and normal D are continuous. Tangential
E and the gauge potential pullback match; the pure-electric radial E jump is
the constitutive phase polarization. Outside, `D=E=Q/(4pi r^2)` and

\[
 m_{\rm out}(r)=M-\frac{Q^2}{8\pi c^2r},\quad
 F_{\rm out}=1-\frac{2GM}{c^2r}+\frac{GQ^2}{4\pi c^4r^2},
 \quad e^{2\nu_{\rm out}}=F_{\rm out}.                \tag{14}
\]

Thus M is the ADM mass including the Maxwell tail; interior m(R) is not M.
Let `a=sqrt(F_-(R))`, `b=sqrt(F_+(R))`,
`k=4piG sigma/c^4`. Choose the same outward normal (inside to outside)
on both sides. With `K^theta_theta=sqrt F/R` and
`K^tau_tau=sqrt F nu'`, Israel's equations for
`S^i_j=-sigma delta^i_j` are

\[
 a-b=kR,\qquad b\nu'_+-a\nu'_-=-k.                  \tag{15}
\]

The convention matches Israel's original Lanczos equation, section 5,
equations (19)–(20), with energy rather than mass surface density:
[Israel (1966), DOI 10.1007/BF02710419](https://doi.org/10.1007/BF02710419).
The normal points from minus to plus; no wormhole orientation is selected.
The following elimination supplies a separate sign and mass check.

The angular equation gives

\[
 m_+(R)-m_-(R)=m_w a-\frac{Gm_w^2}{2c^2R},\quad
 m_w=\frac{4\pi\sigma R^2}{c^2},
\]
\[
 \boxed{M=m_-(R)+\frac{4\pi\sigma R^2}{c^2}a
       -\frac{8\pi^2G\sigma^2R^3}{c^6}
       +\frac{Q^2}{8\pi c^2R}.}                     \tag{16}
\]

This counts the positive wall rest energy, its redshift/binding, its
self-binding, and the exterior gauge energy, with their correct dimensions.
The time equation is equivalent, after (5) and the angular equation, to

\[
 \boxed{(a\nu'_-+2a/R)\sigma
       -\frac{6\pi G}{c^4}\sigma^2=P(R)-\Delta H(D_b).}\tag{17}
\]

One can derive the same load from the normal Einstein constraint:
`[T_nn]=-sigma bar K`, where
`bar K=a nu'_-+2a/R-3k/2` after the time jump.
In particular the sign of Delta H agrees with the fixed-charge phase-energy
variation, and the flat limit is `P-Delta H=2sigma/R`.
The script verifies the algebraic equivalence of (15) and (17).

The fixed-point solution makes the right side L strictly positive because
`P(R)>=.99^2P0` and `Delta H<X^3/[3(1-X)]`. Define
`A_w=a nu'_-+2a/R` and `B_w=6piG/c^4`. The bulk solution is independent
of sigma except for the additive lapse normalization; its `nu'_-` is fixed
by (5). From (11), `a>F_*`, `nu'_->=0`, so `A_w>2F_*` at R=1.
At `sigma_test=.51P0`, exact bounds give

\[
 A_w\sigma_{test}-B_w\sigma_{test}^2>P_0\ge L,
 \quad A_w-2B_w\sigma_{test}>1.99.
\]

There is therefore exactly one weak positive root in
`(0,sigma_test)`. Set that actual root as the constant material tension:

\[
 \sigma=\frac{2L}{A_w+\sqrt{A_w^2-4B_wL}}.            \tag{18}
\]

Its `b=a-kR` stays positive. Both Israel conditions and the reciprocal normal
wall equation are solved, with no uncounted surface mass or charge. Along
the exhibited one-parameter branch sigma is a smooth selected output; each
individual model holds its selected sigma fixed under perturbation. A
continuation at an independently prescribed tension would require varying
another shooting parameter and is not asserted here.

Finally normalize the interior lapse to
`nu(R)=.5 log F_+(R)`. This preserves all bulk gradients and gives continuous
induced wall metric and unit lapse at infinity. The bounds `m(R)<35`,
`sigma<.51P0`, `Q=zeta S_c` bound the entire Maxwell exterior away from a
horizon for `r>=R`; its ADM mass is finite. The center is regular, the
densities are positive, and the only distributional stress is the counted
timelike wall. This completes the static global solution.

## 6. This changes the inherited gravity at the required order

Equation (5) contains the internal and gauge energy in m, the radial
pressure/tension in the lapse, proper volume in charge and stock, and full
wall stress in (15). The old hybrid instead uses coordinate rest mass alone
in Poisson gravity. For example, expanding the GR load gives

\[
 A_w=\frac2R-\frac{Gm}{c^2R^2}
       +\frac{4\pi GR(P-H)}{c^4}+O((Gm/c^2R)^2/R),
\]

with m itself including internal and gauge energy. This exhibits the
pressure-gravity term absent from the old load. No old radial operator,
Rayleigh bound or mode positivity is a theorem for this Einstein body.

The Gamma-2 EOSs have `0<dP/d epsilon=w/(c^2+w)<1`, and the dark occupied
bulk gate still has `h_eff=rho_c c^2`, hugely larger than `E^2 x` throughout
this positive-density ball. These local matter/gauge statements do not
prove GR radial stability, angular interface stability, Einstein constraints
for perturbations, or nonlinear free-boundary wellposedness.

## 7. Evidence, limits and remaining mathematical obligations

The exact identities and conservative rational bounds are accompanied by
eight bounded DOP853 IVPs: four eta values, two tolerances/step caps each.
The frozen source snapshots, actual software versions, full commands,
resource caps, input hashes before/after, logs and scientific output hashes
are recorded by the Mathbox bounded runner. Numerical profiles illustrate
the theorem; they do not establish it. High-precision scalar wall residuals
verify the junction algebra on rounded IVP edge data and are not interval
certification of those data. `COMPUTATION.md` records the accepted run and
the illustrative values without hiding failed controls.

Closed here: one complete static full-Einstein extension of this specified
critical two-fluid, constitutive occupied phase, reflecting wall and Maxwell
vacuum, with all proper stocks and all gravitational stresses counted.

Open: full GR mode analysis in every sector, wall/phase microphysics,
formation, tension selection, production/conversion, abundance and actual
galactic/lensing/cosmological predictions. A compact high-pressure body with
selected barotropes and wall is not a derivation of the original galactic
algebraic law. The new static theorem is nevertheless an actual global
Einstein solution branch, rather than a roadmap for constructing one.
