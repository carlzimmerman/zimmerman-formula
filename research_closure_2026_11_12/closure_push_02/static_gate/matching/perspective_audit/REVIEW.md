# Independent review: perspective gate with Q Gamma compensation

**Primary verdict: correct only after a stated restriction.** The derivative, energy, boundary and pressure-moment statements are proved on `Q>0`, finite `u=Pi/Pi_c>=0`; the positive-energy suppression comparison uses `Q>1`. The universal compensator bound requires concavity for **every Q>=1**, not merely a small interval around Q=1. These are algebraic and static on-shell stress results, not a complete constrained-GR health theorem or an exclusion of every possible theory.

Within those restrictions the final repair does restore the asymptotic force coefficient, but its pressure cannot be discarded or independently canceled by the apparent polarization-gradient stress terms. The finite-u pressure bound below is stronger than an endpoint-only argument and applies on the static polarization shell at an ordinary off-center point.

## Claim and source

Audited definitions:

\[
F=C(Q-1)^2,\quad t=(Q-1)^2/(L^2Q),\quad
B=CL^2Q(1-e^{-t}),\quad S=e^{-u^3},
\]
\[
H=F-B+BS-Q\Gamma(u),\qquad
\Gamma(0)=\Gamma_u(0)=0.
\]

The explicit example has `Gamma_uu=9CL²u⁴S`. The general pressure bound allows any C² Gamma making H concave in Pi for all Q>=1, with the stated endpoint conditions.

Source: the health lane's `repair/DERIVATION.md`, preserved here as `source_snapshot.md`, SHA256 `af8f85581196be9a6b89f202d8910cc48795e959db68410d59dfb03de4dc6ff7`. The fixed-J static stress calculation was independently reconstructed from the action after the parent proposed that variable choice. It is checked separately rather than inferred from the author's label.

Dependency graph: definitions → exact derivatives and energy identity → required L² on the supplied target; global positive-Pi concavity → Gamma curvature bound → finite pressure moment; fixed-J variation plus the P equation → physical spatial stress → pressure lower bound. Leaves are internal algebra, the QX17 action/conventions, and the explicitly assumed physical target. No external theorem is needed.

## 1. Exact identities and their domain

Independent symbolic differentiation verifies

\[
B_{QQ}=Ce^{-t}\left[2-\frac{(Q^2-1)^2}{L^2Q^3}\right]\le2C,
\quad QB_Q-B=C(Q^2-1)e^{-t},
\]
\[
H_{QQ}=2C-(1-S)B_{QQ}>0,
\]
\[
H_{\Pi\Pi}=-\frac{QCL^2S}{\Pi_c^2}
\left[9u^4e^{-t}+6u(1-e^{-t})\right]\le0
\]

for Q>0 and finite u>=0. The Pi inequality is strict for u>0. Also `0<=B<=min(F,QCL²)`.

There is no uniform positive lower bound for H_QQ as u tends to infinity: at Q=1 it equals `2C exp(-u³)` and tends to zero. This does not contradict strict positivity at every finite u.

The literal gate's extension to negative u does **not** preserve these inequalities. The executed audit gives negative H_QQ at `(Q,L,u)=(10,1,-3)` and positive H_uu at `(2,1,-.01)`. The report's explicit restriction to positive Pi is necessary. The consistent extension `S=1,Gamma=0` for negative Pi is C² and preserves the algebraic signs, but is a changed action. Algebra for Q<1 also does not certify positive cosmological clock enthalpy; the FRW quadratic clock has H_Q<0 there.

The exact normal energy identity is

\[
\rho_H=QH_Q-H=C(Q^2-1)[1-(1-S)e^{-t}].
\]

For Q>1, requiring `rho_H/[C(Q²-1)]<=delta`, with `0<=S<delta<1`, is exactly equivalent to

\[
\boxed{L^2\ge\frac{(Q-1)^2}
{Q[\log(1-S)-\log(1-\delta)]}.}
\]

This is an **energy** suppression condition. Replacing it by the earlier H_Q suppression condition would give a different bound. The ratio is undefined at Q=1, although the un-divided energy identity remains valid and gives zero.

## 2. Endpoint moment and finite-u bound

For the explicit compensator,

\[
\lambda=\frac{3\Gamma_{\rm Euler}(5/3)CL^2}{\Pi_c},\quad J=3CL^2,
\]
\[
\Gamma(u)=\lambda\Pi_c u-J+E(u),\qquad
E(u)=\int_u^\infty(v-u)\Gamma_{vv}(v)\,dv\ge0.
\]

The coefficients and sign of the remainder are verified independently. At u=4,

\[
E/(CL^2)=1.62018127450\times10^{-28}.
\]

The asymptote is valid for each fixed Q, or uniformly for Q in a bounded interval. Multiplying E by an unbounded Q does not give uniform absolute convergence over all Q>0. The finite-u bound below avoids relying on that uniformity.

For a general compensator, concavity at Q=1 forces Gamma_uu>=0. Since `sup_(Q>=1) B/Q=CL²`, concavity for every Q>=1 also gives

\[
\Gamma_{uu}\ge CL^2 S''\quad\text{where }S''>0.
\]

Let `u0=(2/3)^(1/3)`. For u>=u0,

\[
\boxed{u\Gamma_u-\Gamma=\int_0^u v\Gamma_{vv}\,dv
\ge CL^2[3e^{-2/3}-(3u^3+1)e^{-u^3}].} \tag{A}
\]

The asymptotic lower bound is `J>=3exp(-2/3)CL²=1.540251357097776... CL²` whenever the first moment is finite. Divergent first moment means no finite intercept; it does not permit a smaller intercept. At u=4 the finite-u subtraction is only `3.09535501876e-26 CL²`.

The Q-domain quantifier matters: if concavity is required only on a derived compact Q interval, the supremum B/Q can be smaller. This review does not assume that such a restricted physical state domain has been proved. The given global statement uses all Q>=1 legitimately.

## 3. The spatial boundary removes the slope, not the pressure

For a constant lambda, `sqrt(-g) Q Pi` is a spatial divergence. Thus the term `-lambda Q Pi` contributes no bulk field equation under the stated boundary conditions. The remaining `QJ` has

\[
\rho_{QJ}=Q\partial_Q(QJ)-QJ=0,\qquad
T_{ij}^{QJ}=QJ\,h_{ij}.
\]

It has positive pressure and zero normal energy. It is not a cosmological constant. The repair therefore genuinely removes the first construction's force-normalization defect, while retaining an inequivalent stress contribution.

A concern raised during review was whether covariant terms involving `P dot grad(H_Pi)` could independently cancel this pressure away from P=0. **That concern is resolved on the static polarization shell.** It must not be retained as an open loophole after the following calculation.

In static unitary variables set `J^i=sqrt(h)P^i`, so `Pi=partial_i J^i/sqrt(h)`. The matter action density is

\[
N\sqrt h[H(Q,\Pi)-W(|P|)]+J^i\partial_iN.
\]

At fixed J and N, the last term is independent of the spatial metric. Varying the metric gives

\[
T^{ij}=[H-\Pi H_\Pi+P W_P-W]h^{ij}
-\frac{W_P}{P}P^iP^j.
\]

The metric-dependent change from P to J is legitimate for the on-shell stress: differences from varying at fixed original P are proportional to its Euler–Lagrange equation. This is precisely where the apparent covariant gradient terms cancel; they are not an independently adjustable stress.

Therefore, with the third direction along P,

\[
p_\parallel=H-\Pi H_\Pi-W,\quad
p_\perp=H-\Pi H_\Pi+P W_P-W,
\]
\[
\bar p=\frac{p_\parallel+2p_\perp}{3}
=H-\Pi H_\Pi+\frac23P W_P-W.
\]

For QX17's W, `P W_P>=2W>=0`. One direct proof writes `w(p)=-p-log(1-p)`, notes `(p w'-2w)'=p²/(1-p)²>=0`, and uses its zero value at p=0. Consequently

\[
\bar p\ge H-\Pi H_\Pi
=R+B(S-uS')+Q(u\Gamma_u-\Gamma),\quad R=F-B\ge0.
\]

Every term on the right is nonnegative for u>=0. Combining with (A) proves a **pointwise finite-u mean-pressure lower bound** on the static P shell, not only at a center or after taking an asymptotic limit. Original positive one-sided stiffness adds `gamma Pi_+²/2` to this mean pressure and cannot weaken it. Independent diagonal-metric variation reproduces all three principal pressures exactly.

This result concerns the specified static action and its on-shell stress. It does not preclude another independently varied sector, a different background, or another theory.

## 4. Independent physical-target conversion

The physical input is the same pinned canonical annulus, not a solution of this repaired action: `Mb=1e11 Msun`, maximum weak clock offset `2.21794508245e-6`, `u_R=4`, and the historical effective clock-energy ceiling `delta=(1/mu_K)^2` in the stated Mpc units. Using `Q=1+abs(phi)` and the corrected energy bound gives, for mu_K=25120/Mpc,

\[
L^2\ge0.003104129875684614,
\quad KCL^2\ge979375.3255136007\ {\rm Mpc}^{-2},
\]
\[
KJ_{\min}=1508484.1742303998\ {\rm Mpc}^{-2}.
\]

At the outer point, including its Q factor and the finite-u bound,

\[
K\bar p\ge1508484.7708174305\ {\rm Mpc}^{-2},\qquad
\bar p/\Pi_{\rm reference}\ge2.06237841745\times10^{12}.
\]

The corresponding inverse curvature scale `(KJ_min)^(-1/2)` is `0.00081419723 Mpc`, about 0.814 kpc. These are conditional comparisons to the supplied weak-field target and energy ceiling. They show that this repair cannot silently preserve that target while omitting its stress. They do not constitute a fresh empirical fit or an all-theory impossibility theorem.

The numerical off-gate bound at the inner radius takes S=0 because the actual S is below exp(-10^12); the difference is far below the displayed precision. All finite-u pressure bounds and endpoint remainders are separately evaluated without setting S(4) to zero.

## 5. Restricting Q to the actual weak-field band

The lower pressure cost is not solely an artifact of allowing Q to grow without bound. Retain this same perspective/Q-Gamma class, but require concavity only on the **rectangular** domain `1<=Q<=Qmax`, `Pi>=0`, where `Qmax=1+2.21794508245e-6` is the supplied target's maximum Q. The domain must still contain Q=1 for the Gamma_uu>=0 conclusion. This does not address an unproved correlated nonrectangular Q–Pi state restriction.

Because `t(Q)` increases for Q>=1,

\[
B_{\rm band}=\sup_{1\le Q\le Q_{\max}}B/Q
=CL^2(1-e^{-t_{\max}}).
\]

Let `T=-log(1-delta)`. The energy ceiling implies `t_max<=T`, even without setting S to zero. The function `(1-exp(-t))/t` decreases for t>0, since its derivative is `[(1+t)exp(-t)-1]/t²<=0`. Therefore

\[
\boxed{B_{\rm band}\ge
\frac{C(Q_{\max}-1)^2}{Q_{\max}}
\frac{\delta}{-\log(1-\delta)}.}
\]

The Gamma curvature, moment and on-shell stress proofs above all hold with this B_band in place of CL². This is an independently checked three-step finite-domain extension; it does not invoke concavity beyond the given Q band.

The energy fraction is at least S. Requiring the fraction to be <=delta therefore also forces `u>=(-log delta)^(1/3)`. For the present delta values this is above u0, so the universal local pressure floor can use

\[
I_\delta=3e^{-2/3}-(1-3\log\delta)\delta>0,
\qquad \bar p\ge Q B_{\rm band} I_\delta.
\]

It does not require a general Gamma to have reached its linear asymptote at u=4, nor assume the reference Pi profile remains exact. It requires the stated clock-energy ceiling throughout the target region.

For mu_K=25120, the independent executed finite-band bounds are

\[
K B_{\rm band}\ge0.001552064937842307\ {\rm Mpc}^{-2},
\quad K\bar p\ge0.002390569974838304\ {\rm Mpc}^{-2},
\]

where the second inequality conservatively uses Q>=1 and u>=u_delta. The separate u=4 evaluation is slightly stronger. The much smaller mu_K=198.25 finite-band bound is `K p>=1.48815e-7/Mpc²`; it does **not** produce the exclusion below.

## 6. Integrated static lapse test on the stated target

For a static zero-shift geometry, direct evaluation gives

\[
R_{nn}=N^{-1}D^2N=K(\rho+3\bar p)-\Lambda.
\]

The Lambda term is part of the actual QX17 equation and cannot be silently omitted from a universal claim. The executed annulus benchmark neglects cosmological background curvature. The following numerical test uses that same target assumption; an exact nonzero Lambda or an additional negative-active stress can be restored explicitly in the volume integral.

Here Q>=1, Pi>=0, W>=0 and rho_H>=0, so the model-sector normal density is nonnegative; the original one-sided stiffness only increases it. On the static polarization shell,

\[
\oint_{\partial\Omega}\nu^iD_iN\,dA
=\int_\Omega N[K(\rho+3\bar p)-\Lambda]dV
\ge\int_\Omega N[3Kp_{\min}-\Lambda]dV.
\]

For the supplied nearly flat annulus and negligible Lambda, division by 4pi gives

\[
R^2N'(R)-r_1^2N'(r_1)
\gtrsim Kp_{\min}N_{\min}(R^3-r_1^3).
\]

The approximation is only the target's weak spatial geometry. Its relative corrections are tiny compared with the high-mu mismatch. The numerical script uses `N=1/Q`, the prescribed weak potential and boundary accelerations, and `N_min=1/Qmax`.

At mu_K=25120 the target left side is `2.81853380e-7 Mpc`. Global Q>=1 concavity requires at least `5.92280224e5 Mpc`. Even concavity restricted to the actual finite Q band requires `9.38616020e-4 Mpc`: a factor **3330.16** above the target lapse flux. Thus this same repair cannot simultaneously satisfy its static on-shell equations, retain the stipulated energy suppression, and preserve that weak-field annulus without an explicitly compensating stress/background change. This is a bounded integrated inconsistency, not a failed solver or merely a comparison of dimensional scales.

For mu_K=198.25 the finite-band required/target ratio is only `0.207306`, before including potentially comparable cosmological background curvature. **No finite-band low-mu exclusion follows.** The large-mu result must not be generalized to it.

The high-mu comparison remains a statement about this action class and matching target. Choosing another independently varied sector, deriving a correlated admissible Q–Pi domain, or changing the target are separate research routes, not ruled out by this audit.

## Obligation matrix and provenance

| obligation | result |
|---|---|
| B derivatives and normal energy | passed, exact symbolic residuals zero |
| finite positive-Pi convexity/concavity | passed; negative-Pi extension explicitly excluded |
| asymptotic slope, intercept, remainder sign | passed; convergence not claimed uniform on unbounded Q |
| arbitrary-compensator moment lower bound | passed under global Q>=1 concavity and endpoint conditions |
| fixed-J spatial variation and physical on-shell stress | passed, independently reconstructed and symbolically checked |
| potential gradient-stress cancellation | resolved: not independent on the P shell |
| corrected energy-suppression scale | passed on the pinned target; distinct from old H_Q bound |
| finite rectangular Q-band pressure bound | passed; high-mu target contradiction only |
| integrated lapse comparison | passed under explicit static/weak-geometry/background hypotheses |
| complete GR health, formation and all-theory exclusion | out of scope |

`run04/manifest.json` has status **completed** and validates against all pinned inputs. It includes the earlier exact checks, the integrated lapse test, and the finite-Q-band extension. The script uses exact SymPy identities and 70-digit mpmath endpoint calculations; direct tail quadrature agrees to relative error below 8e-66. The literal negative-Pi counterexamples are intentional domain checks. `run01` is the earlier algebra/moment check; run02 adds the resolved on-shell spatial stress calculation; run03 adds the global-domain integrated test; run04 adds the finite-Q-band bound. Every run preserves its own immutable inputs and outputs.

This is an independent reconstruction by the static-route agent, followed by explicit coordination on the fixed-J variable choice. Agent agreement is not used as a proof. No historical source was edited. The source snapshot and execution hashes identify the exact reviewed revision.
