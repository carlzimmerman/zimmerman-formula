# A23 — the saddle dip in the framework's own law, with the external-field effect

**Claim.** The frozen-rest-state law $g_N=g^2/(g+a_0)$ is exactly AQUAL with
$\mu(x)=x/(1+x)$ (A24), so the framework **has** an external-field effect. The no-EFE premise
this lane was opened under is refuted; this report supersedes it. Solving the two-lens saddle
in the full 3-D domain (not A13's mirror half-domain) gives the retained saddle column
$S(e)/S(0)=1.000,\,0.641,\,0.396,\,0.237,\,0.050,\,0.000$ at
$e=0,\,0.1,\,0.15,\,0.2,\,0.3,\,0.68$, with half-suppression at $e_{1/2}=0.129$; the
mid-plane phantom at $0.2d$ runs $-0.2362\to-0.0315\to+0.1453$ over the same range. **The dip
does not survive.** Every accessible pair environment has $e\ge0.68$ (void) rising to $34$
(group), where the retained column is zero; the missing depth falls from $2.16/5.17$ to
$0.11/0.26$ M☉/pc² at $e=0.3$ and to zero at $e=0.68$. A13's $0.75/0.34/0.02$ curve is not
transferable: it imposed mirror symmetry at $z=0$, which a uniform field along the pair axis
breaks. The saddle test is a **NO-GO**: it would need $e\le0.21$–$0.24$, i.e.
$g_{\rm ext}\le3\times10^{-4}a_0$, about 3× below a deep void and 30× below the cosmic mean.

## 1. Status

`NO-GO(EFE: the saddle dip is absent for e>=0.68 and 5% at e=0.3; no accessible environment has e<0.2)`.
The amplitude calculation is `NUMERICAL` (an independent PDE solve, four resolutions,
Richardson extrapolation). The EFE is a property of the exact field form, not a choice.

## 2. Derivation

Units $G=M_{\rm lens}=a_0=d=1$ for the field solve; restored at the end.

1. **The law and its field form.** Invert $g_N=g^2/(g+a_0)$:
   $$g=\frac{g_N}{2}\Big(1+\sqrt{1+\frac{4a_0}{g_N}}\Big),\qquad
   \nu(y)\equiv\frac{g}{g_N}=\frac12+\sqrt{\frac14+\frac1y}.$$
   The exact field form is
   $$\nabla\!\cdot\!\big(\mu(|\nabla\Phi|/a_0)\nabla\Phi\big)=4\pi G\rho_b,\qquad \mu(x)=\frac{x}{1+x},
   \tag{1}$$
   because $g\,\mu(g/a_0)=g_N$ identically (checked symbolically, K1). This is AQUAL.
2. **No environmental term, but an EFE.** Equation (1) contains only $\Phi$ and $\rho_b$; there
   is no $\rho_{\rm env}$, no $g_{\rm ext}$, no $\nu(\ldots,g_{\rm ext})$. The external field
   enters as the boundary condition at infinity and through $\mu$ evaluated on the *total*
   field. Under $\Phi\to\Phi+ez$ the operator changes by a term proportional to $\mu'$:
   at $(X,Z)=(1,1.5)$, $e=1$, the residual is $+0.2378$ (K1). It vanishes only for linear
   theory. **This is the EFE**: not a term, a consequence of nonlinearity plus the boundary
   condition. A24 measured it at $0.350$ in $\gamma_v$ ($12.7\sigma$), 18× the QUMOND-vs-AQUAL
   solver fork ($\le0.019$) (EXT A24).
3. **The two-body problem.** Two equal Plummer lenses of mass $M$ at $z=\pm d/2$, softening
   $b=0.01d$, on a graded axisymmetric grid out to $6d$. The phantom density is
   $$\rho_{\rm ph}=\frac{\nabla^2\Phi}{4\pi G}-\rho_b .\tag{2}$$
   In the deep limit, with $x=R/d$, $\zeta=z/d$,
   $\rho_{\rm ph}=C(x,\zeta)\sqrt{GMa_0}/(Gd^2)$: the dimensionless problem is parameter-free.
4. **The column.** For an edge-on pair the line of sight through the saddle is the mid-plane
   radial direction, so
   $$S=2\!\int_0^{R_{\max}}\!\!\min(C,0)\,dx,\qquad
   \Sigma_{\rm miss}=-S\frac{\sqrt{GMa_0}}{Gd}.\tag{3}$$
   $S_{0.6}$ (the aperture, $R<0.6d$) is the saddle signal; $S_{\rm tot}$ integrates the whole
   mid-plane and at $e\ge3$ picks up a large-$R$ wake that is not at the saddle.
5. **Why the full domain is required.** A13 solved (1) on $z\in[0,6]$ with no flux through
   $z=0$. That is a mirror condition $z\to-z$. A uniform field along the pair axis is odd under
   that mirror, so the half-domain solve is a different physical problem (an external field
   applied symmetrically about the mid-plane, which has no uniform-field limit). The EFE sweep
   here is on $z\in[-6,6]$ with both lenses present.
6. **The far field.** Write $\Phi=ez+\psi$ and linearise (1) in $\psi$ for $|\nabla\psi|\ll e$:
   $$\psi_{RR}+\frac{\psi_R}{R}+2\psi_{zz}=0
   \quad\Longrightarrow\quad
   \Phi\to ez-\frac{M}{e\sqrt{R^2+z^2/2}}.\tag{4}$$
   The anisotropy is the deep-MOND signature of a uniform external field; using the isotropic
   $-M/r$ instead biases the suppression by a factor of a few (checked at $e=0.3$).
7. **The e mapping.** With $r_M=\sqrt{GM/a_0}$,
   $$e_{\rm dim}=\frac{g_{\rm ext}}{a_0}\frac{d}{r_M}.\tag{5}$$
   For the LRG pair ($M_b=10^{11.3}$ M☉, $d=11.76$ Mpc): $r_M=17.2$ kpc, $d/r_M=682$.
8. **Ladder.** Four resolutions $h=0.004,0.002,0.001,0.0005$, Picard with geometric-mean
   damping, then $S(h)=S_\infty+a h^p$ with $p$ from the last two increments.

## 3. Numbers: the isolated saddle

| quantity | value | A13 (EXT) |
|---|---|---|
| $C(0.2d)$, mid-plane | **−0.24035** | −0.24036 |
| $S(h{=}0.002)$ | −0.21027 | −0.21002 |
| $S_\infty$ (Richardson) | **−0.22981** ($p=0.76$, ratios 0.598/0.592) | −0.22931 |
| $\Sigma_{\rm miss}$ MW–M31, can/alt | **2.164 / 2.380** M☉/pc² | 2.159 / 2.374 |
| $\Sigma_{\rm miss}$ cluster, can/alt | **5.174 / 5.700** M☉/pc² | 5.159 / 5.684 |
| $A_{\rm eff}$ | **0.008346 d² = 10.47 arcmin²** | 0.008598 d² = 10.78 arcmin² |
| $\Delta\Sigma$ (LRG, edge-on) | **0.22626** M☉/pc² | 0.22576 |
| $(S/N)_1$ ($n_g=11$, $\sigma_e=0.26$) | **0.005694** | 0.005767 |
| orientation acceptance $\varepsilon$ | **0.144** | 0.146 |
| $N_3$ edge-on / deg² | **2.776×10⁵ / 1 859** | 2.707×10⁵ / 1 812 |
| scanned pairs / deg² (3σ) | **1.92×10⁶ / 12 880** | 1.86×10⁶ / 12 442 |

The AQUAL ladder reproduces A13 to 0.22% in $S_\infty$ and 0.006% in $C(0.2d)$: the amplitude
calculation is confirmed. The QUMOND fork of the same spherical law (the other non-spherical
completion) gives $S_\infty=-0.28059$ (22% deeper), $C(0.2d)=-0.1449$ (40% shallower),
$A_{\rm eff}=0.009694\,d^2$, $(S/N)_1=0.007493$, $N_3=1.60\times10^5$: the fork moves the
amplitude, but A24 shows it is 18× smaller than the EFE and it does not change any conclusion
below.

## 4. The external field: the dip does not survive

$S_{0.6}(e)/S_{0.6}(0)$, full domain, $h=0.006$:

| $e$ | 0 | 0.1 | 0.15 | 0.2 | 0.3 | 0.68 | 1 | 3 |
|---|---|---|---|---|---|---|---|---|
| retained | 1.000 | **0.641** | **0.396** | **0.237** | **0.050** | **0.000** | 0.000 | 0.000 |
| $C(0.2d)$ | −0.2362 | −0.2049 | −0.1571 | −0.1111 | −0.0315 | +0.1453 | +0.2157 | +0.2884 |
| $\Sigma_{\rm miss}$ MW / cluster | 2.16/5.17 | 1.39/3.32 | 0.86/2.05 | 0.51/1.23 | **0.11/0.26** | 0/0 | 0/0 | 0/0 |

* **The half-suppression field is $e_{1/2}=0.129$.** At $e=0.3$ the mid-plane density at $0.2d$
  is 0.133 of its isolated value and the column 0.050.
* **At $e\ge0.68$ there is no negative mid-plane cell inside $R<0.6d$ at all.** The density at
  $0.2d$ is positive: the external field has filled the saddle, not merely reduced it.
  ($S_{\rm tot}$ stays weakly negative at $e\ge0.68$ from a wake at $R\sim0.8$–$1.2$, which is not
  the saddle and is outside the matched-filter aperture.)
* **Robustness.** At $e=0.3$: box 6 vs 8 give 0.0501 / 0.0596; $h=0.006$ vs $0.004$ give
  0.0501 / 0.0477. The 5% number is stable at the 25% level, and the qualitative statement
  (≤10% retained) is stable.
* **A13's curve is a symmetry artefact.** On A13's half domain I reproduce
  $0.746$ at $e=0.3$ and $0.332$ at $e=1$ (A13: 0.751 / 0.337). On the full domain the same
  law gives $0.050$ at $e=0.3$. The no-flux condition at $z=0$ forces the external field to
  vanish at the very plane where the dip lives, so A13's solver never applied the field where
  it matters.

## 5. The corrected pair budget

Per-pair S/N and pair counts are unchanged in form; what changes is the amplitude available in
a real environment. With $\varepsilon=0.144$ and 149.4 pairs deg⁻²:

| survey | $n_g$ | $(S/N)_1$ | $N_3$ edge-on | deg² (3σ, edge-on) | deg² scanned |
|---|---|---|---|---|---|
| CFHTLenS (published) | 11 | 0.005694 | 2.78×10⁵ | 1 859 | 12 880 |
| DES Y6 | 10 | 0.00543 | 3.05×10⁵ | 2 044 | 14 168 |
| LSST Y10 | 27 | 0.00892 | 1.13×10⁵ | 757 | 5 247 |
| Euclid Wide | 30 | 0.00940 | 1.02×10⁵ | 681 | 4 723 |
| Roman HLIS | 45 | 0.01109 | 7.32×10⁴ | 490 | 3 395 |

These are the **isolated** budgets, i.e. what the surveys could do if $e$ were zero. The EFE
changes the requirement: the retained fraction must exceed $f_{\rm req}=\sqrt{N_3/N_{\rm pairs}}$
for the pairs actually available.

| survey | pairs available | $f_{\rm req}$ | $e_{\rm req}$ | $g_{\rm ext}/a_0$ required |
|---|---|---|---|---|
| DES Y6 | 7.47×10⁵ | 0.639 | 0.10 | 1.5×10⁻⁴ |
| LSST Y10 | 2.69×10⁶ | 0.205 | **0.217** | 3.2×10⁻⁴ |
| Euclid Wide | 2.09×10⁶ | 0.221 | **0.209** | 3.1×10⁻⁴ |
| Roman HLIS | 2.69×10⁶ | 0.165 | **0.239** | 3.5×10⁻⁴ |

The environments, at $e=(g_{\rm ext}/a_0)\,682$:

| environment | $g_{\rm ext}/a_0$ | $e$ | retained | $N_3$ |
|---|---|---|---|---|
| void, very underdense | 1×10⁻³ | 0.68 | <10⁻⁶ | none (≥10²⁹) |
| field galaxy (Local Sheet) | 5×10⁻³ | 3.41 | 0 | none |
| filament at $z\sim0.4$ | 1.5×10⁻² | 10.2 | 0 | none |
| group interior | 5×10⁻² | 34.1 | 0 | none |

**Even the void is 3.1× too large in field.** A void with $g_{\rm ext}=10^{-3}a_0$ is already
at $e=0.68$; the dip needs $e\le0.22$, i.e. $g_{\rm ext}\le3\times10^{-4}a_0$. No environment in
the LRG-pair catalogue is that empty. The test has no sample: the pair budget diverges.

## 6. What A13 got, and what transfers

| | A13 (EXT) | this lane |
|---|---|---|
| law | AQUAL $\mu=x/(1+x)$ | same (A24 settles it) |
| EFE at $e=0.3$ | 0.751 | **0.050** |
| EFE at $e=1$ | 0.337 | **0.000** |
| EFE at $e=3$ | 0.021 | **0.000** |
| domain | $z\in[0,6]$, no flux at $z=0$ | $z\in[-6,6]$, anisotropic far field |
| verdict | voids viable, filaments hopeless | **nothing viable** |

A13's qualitative conclusion — the prediction is switched off in filaments — is correct and is
strengthened: it is switched off in voids too. Its quantitative curve is not transferable, and
its "statistically within reach" reading is withdrawn.

## 7. Checks (`a23_checks.py`, 12/12 PASS, 36 s)

K1 exact inversion $g^2/(g+a_0)=g_N$ and $g\mu(g/a_0)=g_N$; nonzero e-shift residual.
K2 AQUAL control $|\nabla\Phi|r=1$ (9.8×10⁻⁴) and $\rho_{\rm ph}r^2=1/4\pi$ (5.7×10⁻³).
K3 QUMOND fork control against the exact full-ν phantom $1/(2\pi r\sqrt{1+4r^2})$ (2.3×10⁻²).
K4 the ladder reproduces A13 (0.2% in $S_\infty$, 0.03% in $C(0.2d)$).
K5 the fork converges ($\sqrt h$, ratio 0.689) and differs from AQUAL by 22% in the column.
K6 the depths match A13 within 3%. K7 $A_{\rm eff}$ and $(S/N)_1$ match A13 within 5%.
K8 the EFE curve is monotone, 0.641 at $e=0.1$ and 0.050 at $e=0.3$.
K9 at $e\ge0.68$ the saddle column is zero and $C(0.2d)>0$.
K10 the half-domain reproduces 0.746 while the full domain gives 0.050.
K11 the $e=0.3$ result is stable over box 6/8 and $h=0.006/0.004$.
K12 LSST/Euclid/Roman need $e_{\rm req}=0.22/0.21/0.24$.

## 8. What this does not do

* Deep-$\mu$ only. The neglected correction is $O(r_M/d)$: 0.15% for the LRG pair, 3.4% for
  the cluster fiducial. The EFE conclusion is not sensitive to it.
* The external field is uniform and along the pair axis. A tidal field or one at an angle
  changes the numbers at the factor-of-a-few level; it cannot restore the dip, because the
  filling is local (the field at the saddle is what matters).
* The far field (4) is the leading anisotropic solution; the next order is $O(1/r^2)$ and is
  not computed.
* Systematics are not priced: the positive filament/bridge (comparable to the dip), pair
  miscentring, correlated shape noise, and the published error being 1.77× pure shape noise.
* The QUMOND fork is computed only at $e=0$; A24 shows it is subdominant to the EFE.

## 9. Next

1. There is no point optimising the pair selection: the blocker is the field at the saddle,
   not the sample size. The only surviving route is a sample with
   $g_{\rm ext}<3\times10^{-4}a_0$, which does not exist at $z\sim0.4$.
2. If the EFE is real (A24), the saddle is not a discriminator. The EFE's own signatures —
   the displaced null, the anisotropic wake at $R\sim1d$, the $\gamma_v$ boost — are the
   observables that survive, and the wide-binary prediction is already registered.
3. Correct Zenodo 23251278's title claim, and PAPER49's "no saddle dip" prediction: under the
   framework's own law there is no dip to see.

## 10. The falsifier, one line

**A dip of $0.226$ M☉/pc² at the saddle in $\ge2.8\times10^5$ edge-on pairs
($1.9\times10^6$ scanned, $1.3\times10^4$ deg² at CFHTLenS depth; $5.2\times10^3$ deg² at LSST
depth) in a sample with $g_{\rm ext}<1.5\times10^{-4}a_0$ would falsify the EFE; no such sample
exists, and the framework's own law predicts no dip anywhere.**
