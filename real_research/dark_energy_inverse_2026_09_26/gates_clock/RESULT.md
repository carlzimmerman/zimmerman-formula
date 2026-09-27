# CD26-3: what a gate edge and a clock mode can identify

The gate has a useful inverse, but an edge does not by itself identify vacuum
stress. It measures an effective switching threshold after the acceleration
profile, expansion, and background-density subtraction have been specified.
The explicit polar clock has a stronger conditional inverse: its sound
dispersion and independently separated stress determine local clock
parameters, and determine a vacuum constant only after a potential model and
its zero have been fixed. Neither inverse derives a microscopic dark-energy
mechanism.

Assigned starting revision: `7daaa5426076a2d78a50f3316007c7093255ce9a`, with the
existing CD26-2 working tree. Concurrent work advanced the shared checkout;
the computation ran at `ecffd2af3623ff3e32318234fd51e1fac50b9126`, dirty. No
previous source or result was changed by this route. The operative target is
the filtered `nu_mono` construction and criterion B; the historical DE1–DE3
tables remain conditional tests of their own stated gate/profile/mock cells.

## 1. The gate-to-edge map and its inverse

Write

\[
 f_v(z)=\frac{\Omega_v(z)}{\Omega_{v0}}>0,\qquad
 u=\tilde x f_v^p,\qquad
 D(z)=x_{c,\mathrm{eff}}=x_{c0}f_v^{-p}>0.
\]

The active branch is selected by `u >= xc0`, equivalently `x_tilde >= D`.
For the historical isolated spherical deep-MOND point-mass profile on the
**dynamical-density, phantom-inclusive upper branch**,

\[
 v_f^4=GM_ba_0,\qquad
 B=\frac{4\pi G\bar\rho}{H^2},\qquad
 \tilde x(r)=\frac{v_f^2}{H^2r^2}-B,
\]

so the largest crossing has

\[
 \boxed{r_e=\frac{v_f}{H\sqrt{D+B}},\qquad
 D=\frac{v_f^2}{H^2r_e^2}-B.} \tag{1}
\]

Use the expanding branch `H>0`; replace `H` in the radius formula by `|H|`
if applying only this algebra on a contracting branch. Equation (1) requires
`D>0` and `D+B>0`. An inferred `D<=0` is incompatible with this positive
threshold model under the adopted inputs. It is not evidence for negative
vacuum energy. With `rho_crit=3H^2/(8pi G)`, the stated definition gives
`B=(3/2) Omega_background`.

Outside deep MOND, an independently measured spherical acceleration profile
would instead give the on-branch crossing variable

\[
 D=\left.\frac{1}{H^2r_e^2}\frac{d(r^2g)}{dr}\right|_{r_e}-B. \tag{2}
\]

DE1 uses a numerical version of (2), with the full selected kernel, a
background subtraction and the largest crossing. A projected lensing break,
an external-field feature, a smooth gate, or a non-spherical source is not
automatically the `r_e` in these equations. The inverse therefore needs a
forward observable model before it becomes an observational reconstruction.

The elementary inverse relationships are

\[
 x_{c0}=Df_v^p,\qquad
 p=\frac{\ln(D/x_{c0})}{\ln(1/f_v)},\qquad
 f_v=\left(\frac{x_{c0}}D\right)^{1/p}. \tag{3}
\]

The middle inverse requires `f_v != 1`; the last requires `p != 0`.
With two independently known, distinct fractions,

\[
 p=\frac{\ln(D_2/D_1)}{\ln(f_{v1}/f_{v2})},\qquad
 x_{c0}=D_1f_{v1}^p,\qquad
 \frac{f_{v2}}{f_{v1}}=\left(\frac{D_1}{D_2}\right)^{1/p}. \tag{4}
\]

The reference epoch `f_v=1` measures the threshold normalization only.
The `p=0` gate contains no vacuum-history information. Equal-fraction epochs
cannot determine `p`. The historical restriction `p>=0` is a model choice,
not a consequence of inversion.

Defining the fractions through critical density at constant Newton coupling
gives the exact bookkeeping relation

\[
 f_v=\frac{d_v}{E^2},\quad
 d_v=\frac{\rho_v(z)}{\rho_{v0}},\quad E=\frac{H(z)}{H_0},\quad
 D=x_{c0}E^{2p}d_v^{-p}. \tag{5}
\]

Here `rho_v` must use the same density convention at both epochs. Constant
vacuum density gives `D=xc0 E^(2p)` for any specified `H(z)`; it does not
derive an expansion history. The numerical `E` used in DE1–DE3 is additional
background input. If `p` is known and nonzero,

\[
 \frac{\rho_{v2}}{\rho_{v1}}
 =\left(\frac{H_2}{H_1}\right)^2
  \left(\frac{D_1}{D_2}\right)^{1/p}. \tag{6}
\]

Neglecting `B` only where justified gives

\[
 r_e=\frac{(GM_ba_0)^{1/4}}{H_0\sqrt{x_{c0}}}
 E^{-(1+p)}d_v^{p/2}. \tag{7}
\]

No assumption about `a0(z)` has been inserted in (1)–(7). Imposing a
vacuum-linked `a0` law reduces the unknowns by an extra postulate; it must not
be counted as an independent measurement of the same vacuum history.

## 2. Identifiability and the nuisance directions

Set `b=ln xc0`, `li=ln f_vi`, `yi=ln Di`. Then

\[
 y_i=b-p\ell_i,\qquad J_i=(1,-\ell_i),\qquad
 \det J_{12}=\ell_1-\ell_2. \tag{8}
\]

For independent weights `wi>0`, the Fisher determinant is
`(sum wi)^2 Var_w(li)`; for two epochs it is `w1 w2 (l1-l2)^2`.
Thus even a formally invertible pair is ill-conditioned when its fractions
are nearly equal. This expression conditions on known fractions and
threshold measurements; it is not an error model for correlated expansion,
mass, and edge estimates.

When the fraction history is unknown, there is an exact family

\[
 p\longrightarrow p',\qquad
 f_v(z)\longrightarrow f_v(z)^{p/p'},\qquad p'\ne0, \tag{9}
\]

which preserves every threshold, with `f_v(0)=1` preserved. Gates alone
identify `p ln f_v`, not the exponent and vacuum history separately.

For fixed `G`, set `S=v_f^2/(H^2r_e^2)=D+B`. The inverse differential is

\[
 \delta\ln D=\frac{S}{D}
 \left(\tfrac12\delta\ln M_b+\tfrac12\delta\ln a_0
 -2\delta\ln H-2\delta\ln r_e\right)-\frac{\delta B}{D}. \tag{10}
\]

The forward differential is

\[
 \delta\ln r_e=\tfrac14\delta\ln M_b+\tfrac14\delta\ln a_0
 -\delta\ln H
 -\frac{D}{2(D+B)}(\delta b-\ln f_v\,\delta p-p\,\delta\ln f_v)
 -\frac{\delta B}{2(D+B)}. \tag{11}
\]

Mass and acceleration scale enter only as a product in this edge law.
Replacing `M_b -> c M_b`, `a0 -> a0/c` preserves the edge. A measured flat
speed can replace their decomposition, where such a flat segment exists on
the active branch. `H`, `B`, and a fraction inferred using `H` must carry
their shared covariance. Near `D=0`, background subtraction makes the
inverse particularly sensitive to nuisance errors.

If the only information is that the MOND branch survives at
`y_star=GM/(a0 r_star^2)`, the result is an inequality:

\[
 y_e=\frac{H^2\sqrt{GM_b}}{a_0^{3/2}}(D+B)\le y_\star,
\quad
 D\le\frac{y_\star a_0^{3/2}}{H^2\sqrt{GM_b}}-B,
\]
\[
 M_b\le\frac1G
 \left[\frac{y_\star a_0^{3/2}}{H^2(D+B)}\right]^2. \tag{12}
\]

These are the background-corrected flagship bounds. For constant vacuum,
`E>1`, and positive right side in (12),
`p_max=ln(D_max/xc0)/ln(E^2)`. A negative or vanishing admissible `D_max`
means no positive threshold satisfies this survival test.

## 3. Crosscheck of the actual DE1–DE3 cells

The computation reads committed JSON only. It does not rerun the historical
large mocks, infer a posterior, or combine different footings. DE1's gate
uses `E^2=0.3138(1+z)^3+0.6862`. Its edge `H` and mean density instead come
from L352's separate constants, translated without silently harmonizing
them. L352 subtracts its small radiation density from `Omega_L` but omits a
radiation term in its `Hz` expression; this exact historical convention was
retained for the comparison.

For `p=1, xc0=2.5`, DE2 stores the following three effective thresholds:

| Test epoch | Background used by that cell | Threshold |
|---|---|---:|
| z=0.25 | L347 gate background | 3.247726562500000 |
| z=0.5 | GP3/L363 mock background | 4.363021859625454 |
| z=2.5 | L347 gate background | 35.3509375000000 |

At z=0.5 the mock has `E^2=1.7452087438501815`; the L359/L347 value is
`1.745275`, giving threshold `4.3631875`. Their relative difference is about
`3.8e-5`. They remain different inputs, even though numerically close.

The deep inverse (1) was applied to all sixteen stored DE1 edge radii for
this same `(p,xc0,M_b)=(1,2.5,1e11 Msun)` across eight epochs and two
`a0` footings. Its inferred threshold differs from the prescribed one by at
most **0.663% canonical** and **0.501% alternate**. These finite differences
include the finite-`y` profile and stored numerical edge calculation; they
are not a universal approximation guarantee. At z=0.5, omitting `B` would
instead overestimate the ideal threshold by **20.86%**, before finite-`y`
corrections.

DE1's stored `closed p_max` uses its explicitly background-free formula.
Keeping the background in the inverse gives these distinct bounds at
z=2.5, `xc0=2.5`, `M_b=1e11 Msun`, `y_star=0.1`:

| Footing | Stored closed, without B | Corrected deep, with B | Stored full-profile numerical |
|---|---:|---:|---:|
| canonical | 1.885391444 | 1.883928485 | 1.880772760 |
| alternate | 1.990879510 | 1.989773735 | 1.986620921 |

The current `p=1` is within these conditional bounds, but the bounds do not
select it uniquely. DE2's listed passes and DE3's transfer margins depend
on their specific kernels, footings, adopted backgrounds and historical
L367 transfer inputs. They are not a measured vacuum-density evolution.

DE3's remaining inversion is the quadratic transfer bound

\[
 R=T^2+2r_xTs+s^2\le1.2,\quad s^2=P_{\rm ph}/P_{\rm NL},\quad
 T_{\max}=-r_xs+\sqrt{r_x^2s^2+1.2-s^2}. \tag{13}
\]

This is the upper root when the radicand and physical admissible interval
exist. It supplies a bound on transfer amplitude at the specified gate
cell, not an inverse determination of vacuum stress. The source is one
lens-epoch power spectrum, not a projected shear observable or a fresh
same-cell cosmological rerun.

### DE4 scope reconciliation, inspected after the inverse run

The newly committed DE4 explicitly identifies a different switch input in
the construction's particle-mesh runs: the **matter-only lower branch**.
Its edge `r_m` satisfies

\[
 \rho_{\min}=\bar\rho_m+\frac{H^2D}{4\pi G},\qquad
 \boxed{D=\frac{4\pi G}{H^2}
       [\rho_{\rm matter}(r_m)-\bar\rho_m]}. \tag{13a}
\]

The gate inverses (3)–(6) and their log-rank obstruction remain valid once
this `D` is supplied. Equations (1), (2), (7), and the deep flagship bound
(12) do **not** become matter-only edge formulas: their dynamical-density
profile includes a MOND contribution that the lower switch does not read.
For example, a specified material power law `rho_matter=A_m r^(-n)`, `n>0`,
would instead give
`r_m=[A_m/(rho_bar+H^2 D/(4pi G))]^(1/n)`. Its normalization and slope,
gas distribution, and any independently retained carrier become the
nuisance inputs. A rotation-speed measurement alone does not supply this
material profile. Branch selection is therefore another identifiability
condition, not a choice that can be hidden inside an edge fit.

DE4 stores `rho_min=4.3648825113743944e-5 Msun/pc^3` for the linear cell at
z=2.5. Its all-CGM-share F1 test fails: at the sampled 10% maximal-CGM
share no sampled retention passes, while at 30% and 100%, complete carrier
clearing does pass. The more restrictive predeclared prediction that no
retention would pass for **either** 10% **or** 30% CGM was therefore **not
confirmed**. These are different assertions. Two of eighteen listed
branch-comparison cases have the lower switch off and upper switch on.
None of this converts the old upper-branch bound into a lower-branch
verdict, or proves the actual evolution chooses either state.

This reconciliation reads DE4's script and stored output only. DE4 imports
particular spherical Hernquist/NFW and halo-shape conventions; those are
model inputs, not a cosmology-independent inverse of measured galaxy gas.
The original 60-check run is preserved unchanged, and DE4 is pinned as a
subsequently inspected source in `source_provenance.json`.

## 4. What the covariant polar clock can identify

Use the explicit CD26-2 candidate, one physical metric, signature `-+++`,
and `c=1`:

\[
 {\cal L}_{\rm clock}=-\tfrac12(\partial R)^2
 -\tfrac12R^2(\partial T)^2-V_{\rm dyn}(R)-C. \tag{14}
\]

It is a classical field action with amplitude and phase. The standalone
Einstein-plus-canonical-polar candidate has two physical scalar canonical
pairs, as counted in CD26-2; it is not a one-pair phase theory. Calling it
particle-free does not remove its independent scalar initial data or
stress. Nothing here specifies an abundance or identifies it with a dark
matter particle population. The common-action MOND embedding requires its
own constraint analysis.

At fixed metric, `C` disappears from the clock Euler–Lagrange equations of
(14):
`d(Vdyn+C)/dR=Vdyn'`. It also disappears from the local potential
derivatives and the circular-background dispersion. Metric variation
instead gives

\[
 \Delta T_{\mu\nu}=-C g_{\mu\nu},\quad
 \Delta\rho=C,\quad\Delta P=-C. \tag{15}
\]

Consequently gravity does respond to this shift. The assertion is not that
an arbitrary vacuum shift leaves a fixed self-consistent cosmology
unchanged. If a further postulate also changes a coupling through `a0(C)`,
that is an additional parameter change, not a pure additive shift in (14).
If the same action also has an independent Einstein cosmological
constant, gravity measures the combination
`Lambda_bare+8pi G C` in these units. Changing `C` by `delta C` and
`Lambda_bare` by `-8pi G delta C` leaves that constant part of the full
action unchanged. Their individual labels require a normalization choice.

For a homogeneous clock, in proper time,

\[
 K=\tfrac12(\dot R^2+R^2\dot T^2),\quad
 \rho=K+V_{\rm dyn}+C,\quad P=K-V_{\rm dyn}-C,
\]
\[
 \boxed{K=\frac{\rho+P}{2},\qquad
 V_{\rm dyn}+C=\frac{\rho-P}{2}.} \tag{16}
\]

Thus `rho+P` removes any constant vacuum contribution. It measures the sum
of radial and phase kinetic energy, not the charge alone. Only on the
circular branch `dot R=0`, `dot T=Omega` is
`W=rho+P=R0^2 Omega^2`, with charge-density magnitude
`|n_Q|=R0^2 |Omega|`. Neither `W` nor the dispersion fixes the charge sign.
The homogeneous conserved quantity in an expanding background is
`a^3 n_Q`; its value remains independent initial data.

Equation (16) identifies total potential energy, not the additive constant
inside an otherwise unknown potential. Moreover, the `rho,P` used here
must be the separately identified clock stress. A total expansion history
does not supply that separation without the gravitational equations and
the other sectors.

## 5. Bidirectional sound/dispersion inverse on a circular patch

Take a stationary local circular background `R=R0>0`, `T=Omega t` with
`Vdyn'(R0)=R0 Omega^2`. Let

\[
 q=\Omega^2>0,\quad r=R_0^2>0,\quad
 \mu^2=V_{\rm dyn}''(R_0)-q>0,\quad A=\mu^2+4q.
\]

In the fixed-background local quadratic system the light branch has

\[
 \omega_-^2=s k^2+d_4 k^4+O(k^6),\qquad
 s=\frac{\mu^2}{A},\quad d_4=\frac{16q^2}{A^3}. \tag{17}
\]

The heavy gap is `A` in squared-frequency units. The inverse for
`0<s<1`, `d4>0` is

\[
 \boxed{A=\frac{(1-s)^2}{d_4},\qquad
 q=\frac{(1-s)^3}{4d_4},\qquad
 \mu^2=\frac{s(1-s)^2}{d_4}.} \tag{18}
\]

An independently measured gap tests the redundancy `d4 A=(1-s)^2`.
With `W=rho+P>0`, additionally

\[
 r=\frac{4d_4W}{(1-s)^3},\qquad
 |n_Q|=\frac{2W\sqrt{d_4}}{(1-s)^{3/2}},\quad
 V'=\sqrt r\,q,\quad V''=\mu^2+q. \tag{19}
\]

These infer local potential derivatives, not its zero. They use canonical
field normalization; a field redefinition with noncanonical kinetic terms
changes the parameter interpretation. The nonrotating boundary
`s=1,d4=0` lies outside this inverse chart. The `s=0` boundary loses strict
positive sound speed and is not covered by the stated health assumptions.
This is a local stationary-patch dispersion, not an exact time-independent
dispersion relation on an arbitrary evolving cosmological background.

For the extra assumption of an explicitly normalized quartic potential

\[
 V_{\rm dyn}=\tfrac12m_0^2R^2+\tfrac14\lambda R^4,
\]

one obtains the fully conditional inverse

\[
 m_0^2=\frac{(1-s)^2(1-3s)}{4d_4},\quad
 \lambda=\frac{s(1-s)^5}{8d_4^2W},\quad
 \boxed{C=-P+\frac{sW}{2(1-s)}.} \tag{20}
\]

The `m0^2>=0` branch requires `s<=1/3`; an inferred negative `m0^2` need
not invalidate a different symmetry-breaking potential branch. For the
massless quartic `s=1/3`, equation (20) becomes `C=(rho-3P)/4`. A positive
vacuum requirement is the additional consistency inequality `C>0`.

In coordinates `(mu^2,q,r,C)`, the map to `(s,d4,W,P)` has determinant

\[
 \det\frac{\partial(s,d_4,W,P)}{\partial(\mu^2,q,r,C)}
 =\frac{64q^3}{(\mu^2+4q)^5}>0. \tag{21}
\]

This is a locally identifiable four-parameter inverse within this specific
model and branch. It does not make an unknown potential or an unknown
gravitating stress decomposition identifiable. Holding all clock parameters
fixed and choosing `C=0,3,10` in the bounded control leaves `s,d4,W`
identical, while shifting `rho,P` by opposite constants. This directly
detects the invalid inference of vacuum density from dispersion alone.

The CD26-2 common-action calculation remains relevant: a charged polar
clock aligned with a spatially varying lapse contributes a nonconstant
source. The present inverse does not remove that source or establish the
baryon-only filtered-MOND target. Nor does it identify the fraction in the
phenomenological gate with this clock's constant `C` by an action-level
derivation.

## 6. Evidence, interpretation and names

`run1/results.json` contains **60 passing checks**: conditional exact
identities, nuisance and rank calculations, negative controls, sixteen
stored-profile comparisons, and three explicit vacuum shifts. The pinned
runner exited zero in **1.016129 s** with all declared input hashes
unchanged. `contract.json` states the tested domains and exclusions;
`run1/manifest.json` records commands, versions, hashes and limits.
`source_provenance.json` pins the consulted local sources separately from
the computation's four execution inputs. No new observational fit or
external literature claim is made.

`GateClockInverse20260926.lean` additionally compiles four conditional
algebra lemmas: the two-environment inverse, stress-sum shift invariance,
and the two gap/rotation-rate dispersion inverses. The accepted compile
exited zero with no warnings or admissions; all axiom reports use only
`propext`, `Classical.choice`, and `Quot.sound`. `EVIDENCE.md` and
`lean_review_record.json` record the independent source/log hash review and
exact compiler record. This formal coverage does not derive the action,
stress tensor, dispersion law, or their observational identification.

Physically justified labels follow the role actually established:

- **Vacuum stress** for an identified constant component `Tmunu=-C gmunu`.
- **Clock charge** or **clock-condensate excitation** for the independent
  rotating-field stress and conserved initial datum.
- **Vacuum-fraction gate** for the prescribed `f_v^p` activation law.
- **Vacuum-linked response scale** when only a constitutive link to an
  acceleration scale has been established.

The first two are distinguishable stress contributions in the explicit
candidate action. The latter two describe phenomenological roles. The
algebra supports keeping these distinctions explicit; it does not yet
support replacing all of them by one newly identified substance.
