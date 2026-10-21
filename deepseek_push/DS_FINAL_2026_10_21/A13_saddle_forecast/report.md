# A13 — the saddle no-go as a forecast: pairs, square degrees, and the external field

**Claim.** The framework's one unique lensing prediction — *no saddle dip* — is real, is
sign-definite, and is now priced. Under the exact law the cold column through the saddle of
two equal lenses of baryonic mass $M$ at separation $d$ drops to a net $+0.016$ (in units of
$\sqrt{GMa_0}/(Gd)$, AG6C) while a $\rho\ge0$ medium can only reach $+0.229$: a **missing depth of
2.16–2.37 M☉/pc²** (MW–M31-like, 8×10¹⁰ M☉ each, 0.77 Mpc) and **5.16–5.68 M☉/pc²**
(cluster pair, 2×10¹³ M☉ each, 5 Mpc), the range running over the two footings. The published
LRG-pair stack (arXiv:1702.08485) reaches S/N = 0.87 for it. **3σ needs 2.7×10⁵ edge-on pairs
(1.9×10⁶ pairs scanned, 12 400 deg² at CFHTLenS depth; 5 100 deg² at LSST depth) and 5σ needs
2.8× that** — statistically within reach. But the dip lives where the pair's own field is
$\lesssim10^{-2}a_0$, and a uniform external field along the pair axis suppresses it by
**0.75 / 0.34 / 0.02** at $e_{\rm dim}=0.3/1/3$ (eq. 7). For 6–10 h⁻¹ Mpc
pairs the environmental field ($g_{\rm ext}\sim0.01a_0$) sits at $e\approx10$: suppression
**0.002**, i.e. **3×10¹⁰ pairs**. The prediction is therefore *decidable only in a
low-external-field subsample*, and a null in a filament subsample is uninformative.

## 1. Status

`CONDITIONAL(the stacked sample's external field)`: **DECIDABLE** at 3σ with
$N=1.9\times10^6$ scanned pairs if $g_{\rm ext}/a_0<0.3\,r_M/d$; **NO-GO** otherwise, because
both pictures then predict no dip. The amplitude calculation itself is `NUMERICAL` (an
independent PDE solve plus Richardson extrapolation); the geometry and the scaling are exact.

## 2. Derivation

Units $G=M=a_0=d=1$ for the field solve, restored at the end. Signature and constants per the
shared brief.

1. **The law in field form.** Varying the cold-energy action with $K=4\pi G$, $u=K|P|$ gives
   $g=g_N+u$ and $u^2/(a_0-u)=g_N$, hence
   $$g^2=g_N(g+a_0)\qquad\Longleftrightarrow\qquad \nabla\!\cdot\!\big(\mu(|\nabla\Phi|/a_0)\nabla\Phi\big)=4\pi G\rho_b,
   \qquad \mu(x)=\frac{x}{1+x}. \tag{1}$$
   This is AQUAL with the simple $\mu$ — *not* QUMOND (QUMOND's $\nu$ acts on the Newtonian
   field, a different theory; its phantom has the opposite sign at $R=0.2d$ and is not the
   framework's law). The deep limit used below is $\mu=x$.
2. **Phantom density.** $\rho_c=\bar\rho+\rho_{\rm ph}$ with
   $$\rho_{\rm ph}=\frac{\nabla^2\Phi}{4\pi G}-\rho_b .\tag{2}$$
   For one point mass the deep-MOND solution $|\nabla\Phi|=\sqrt{GMa_0}/r$ gives the exact
   $$\rho_{\rm ph}=\frac{\sqrt{GMa_0}}{4\pi G\,r^2}>0 .\tag{3}$$
3. **Why a spherical estimate fails.** Adding two copies of (3) at the saddle ($r_{1,2}=d/2$)
   gives $\rho_{\rm ph}=2\sqrt{GMa_0}/(\pi G d^2)$, i.e. $C=2/\pi=+0.6366$: **positive**.
   The law's own answer is negative. The negative pancake is a nonlinear effect and cannot be
   obtained by any superposition or spherical argument — the check K5 exists to keep that in view.
4. **Universality.** With $x=R/d$, $\zeta=z/d$, equation (1) in the deep limit is
   parameter-free, so
   $$\rho_{\rm ph}=C(x,\zeta)\,\frac{\sqrt{GMa_0}}{Gd^2},\qquad
   \Sigma_{\rm miss}=|S|\,\frac{\sqrt{GMa_0}}{Gd},\qquad S=2\!\int\!\min(C+\bar C,0)\,dx, \tag{4}$$
   with $\bar C=Gd^2\bar\rho/\sqrt{GMa_0}$ the dimensionless mean cold density
   ($\bar C=2.7\times10^{-3}$ for the MW–M31 fiducial, so clipping changes $S$ by about 1%).
5. **The deficit map.** A medium with $\rho\ge0$ can supply at most $\max(\rho_{\rm ph}+\bar\rho,0)$,
   so the *difference* between the two pictures is the line-of-sight integral of the negative part:
   $$\Delta(x,z)=-\int \min\!\big(\rho_{\rm ph}+\bar\rho,0\big)\,dl\ \ge 0,\qquad
   \Delta_0=\Delta(0,0)=\Sigma_{\rm miss}. \tag{5}$$
6. **Matched filter.** For shape noise $\sigma_e$ and source density $n_g$,
   $$\left(\frac{S}{N}\right)^2_{\!1}=\frac{n_g\int\Delta^2dA}{(\sigma_e\Sigma_{\rm crit})^2}
   =\frac{(\Delta_0)^2\,n_gA_{\rm eff}}{(\sigma_e\Sigma_{\rm crit})^2},\qquad A_{\rm eff}\equiv\int(\Delta/\Delta_0)^2dA, \tag{6}$$
   and stacking $N$ pairs multiplies by $\sqrt N$ exactly: $N_\sigma=(\sigma/(S/N)_1)^2$.
7. **Orientation.** The negative region is a sheet of thickness $0.1d$ perpendicular to the pair
   axis, so the deficit collapses for inclinations away from edge-on; the acceptance is
   $\varepsilon=\int\Delta(i)\,d\cos i/\Delta(90^\circ)$.
8. **External field.** With a uniform field $e$ along the pair axis, solve (1) for
   $\Psi=\Phi+ez$ (which restores the mirror symmetry). In the dimensionless system $e$ is
   measured in $a_0$, so the physical mapping is
   $$e_{\rm dim}=\frac{g_{\rm ext}}{a_0}\cdot\frac{d}{r_M},\qquad r_M=\sqrt{GMa_0}/a_0 . \tag{7}$$

## 3. Numbers

### 3.1 Geometry and depth (verify/correct the published 1.9–2.1 and 4.6–5.1)

Independent solve of (1) on a graded axisymmetric grid, four resolutions, Picard with
geometric-mean damping, Richardson extrapolation in $h$.

| quantity | value | comment |
|---|---|---|
| $C(0.2d)$ (mid-plane) | **−0.2404** | AG6C published −0.2401 (0.1%) |
| $\rho_{\rm ph}(0.2d)/\bar\rho$ | **−89.1** (MW–M31), **−33.4** (cluster) | PAPER49's −89 / −33 **verified** |
| column $S$ at $h=0.002$ | −0.2100 | AG6C published −0.2064 |
| column $S_\infty$ (Richardson) | **−0.2293** | increments ratio 0.59, $p=0.76$ |
| $\Sigma_{\rm miss}$ MW–M31 | **2.159** (can) / **2.374** (alt) M☉/pc² | paper: 1.9–2.1 |
| $\Sigma_{\rm miss}$ cluster | **5.159** (can) / **5.684** (alt) M☉/pc² | paper: 4.6–5.1 |

**Correction.** The paper's numbers are the $h$-grid column ($-0.2064$); the converged column is
$-0.2293$, 11% larger, so the depths are **+13.6% / +13.1%** (MW–M31) and **+12.2% / +11.4%**
(cluster) above the quoted values. Structure and sign are confirmed; the amplitude should read
**≈2.2–2.4** and **≈5.2–5.7 M☉/pc²**. The −89/−33 ratios are exact and unchanged.

### 3.2 Lensing signal and per-pair S/N (LRG sample: $M_b=10^{11.3}$ M☉, $d=11.76$ Mpc, $z=0.42$)

| quantity | value |
|---|---|
| $\Delta\Sigma$ at the saddle (edge-on) | **0.2258 M☉/pc²** |
| peak convergence deficit $\kappa$ | **1.38×10⁻⁴** |
| $A_{\rm eff}$ | **0.0086 d² = 10.8 arcmin²** (1.19 Mpc²) |
| peak $\lvert\gamma_t\rvert$ (azimuthal average) | **6.29×10⁻⁵** |
| $(S/N)_1$ at $n_g=11$, $\sigma_e=0.26$ | **0.00577** |
| stack of the published 23 000 pairs | **0.875** (AG7 independent: 0.87) |
| orientation acceptance $\varepsilon$ | **0.146** ($\Delta(80°)/\Delta_0=0.34$, $\Delta(70°)/\Delta_0=0.005$) |

The dip is a $30'\times1'$ sliver at $z=0.42$ (3.01 arcmin/Mpc, $D_A=1141$ Mpc); the PSF is far
smaller, so the aperture is resolvable, but only pairs within ~9° of edge-on carry it.

### 3.3 Pairs and square degrees for 3σ and 5σ

$N_3=2.71\times10^5$ edge-on pairs, $N_5=7.52\times10^5$ (11.8× and 32.7× the published stack —
the paper's "about twelve times" is confirmed). Dividing by $\varepsilon=0.146$ to count pairs
that must be *scanned*:

| source sample | $n_g$ | $(S/N)_1$ | $N_3$ edge-on | deg² (3σ, edge-on) | $N_3$ scanned | **deg² (3σ, scanned)** |
|---|---|---|---|---|---|---|
| CFHTLenS (published) | 11 | 0.00577 | 2.71×10⁵ | 1 812 | 1.86×10⁶ | **12 442** |
| DES Y6 | 10 | 0.00550 | 2.98×10⁵ | 1 993 | 2.04×10⁶ | **13 686** |
| LSST Y10 | 27 | 0.00903 | 1.10×10⁵ | 738 | 7.57×10⁵ | **5 069** |
| Euclid Wide | 30 | 0.00952 | 9.92×10⁴ | 664 | 6.81×10⁵ | **4 562** |
| Roman HLIS | 45 | 0.01123 | 7.13×10⁴ | 478 | 4.90×10⁵ | **3 280** |

5σ is 2.78× these numbers. **Aperture/selection:** matched filter of area
$A_{\rm eff}=0.0086d^2$ centred on the saddle, i.e. a $0.9d\times0.06d$ sliver at the midpoint,
with an edge-on cut $|\cos i|<0.15$; pairs at $6$–$10\,h^{-1}$ Mpc with
$\langle z\rangle=0.42$ and $M_b\approx10^{11.3}$ M☉.

### 3.4 The external field — where the forecast actually breaks

Suppression of the column $S(e)/S(0)$, computed from the same solver with a uniform field:

| $e_{\rm dim}$ | 0 | 0.3 | 1 | 3 |
|---|---|---|---|---|
| $S(e)/S(0)$ | 1.000 | **0.751** | **0.337** | **0.021** |

For the LRG pair $r_M=17.2$ kpc and $d/r_M=682$, so $e_{\rm dim}=682\,(g_{\rm ext}/a_0)$:

| environment | $g_{\rm ext}/a_0$ | $e_{\rm dim}$ | suppression | $N_3$ (LSST depth) |
|---|---|---|---|---|
| void, very underdense | 1×10⁻³ | 0.68 | **0.435** | 5.8×10⁵ |
| field galaxy (Local Sheet) | 5×10⁻³ | 3.4 | **0.016** | 4.1×10⁸ |
| filament at $z\sim0.4$ | 1.5×10⁻² | 10.2 | **0.0018** | 3.3×10¹⁰ |
| group interior | 5×10⁻² | 34 | **0.0002** | 4.1×10¹² |

The penalty on the pair budget is $1/\varepsilon_{\rm EFE}^2$: **×5.3** in a void, **×3×10⁵** in
a filament. The paper's own fiducials are milder because $d/r_M$ is small: MW–M31 ($d/r_M=70$)
keeps **0.94 / 0.43 / 0.05** of its dip at $g_{\rm ext}=10^{-3}/10^{-2}/3\times10^{-2}a_0$, and the
cluster pair ($d/r_M=29$) keeps **0.98 / 0.76 / 0.37** — the cluster survives because its own
field is far larger. The wide LRG pair is the worst case, not the best.

## 4. The falsifier, both ways

* **A dip is found at the predicted depth** (edge-on, low-$g_{\rm ext}$ subsample,
  $\Delta\Sigma=0.23\,(1-\text{EFE})$ M☉/pc², i.e. $\kappa=1.4\times10^{-4}$ scaled by the
  measured suppression): the law is exact on this geometry and the cold sector **must** be able
  to carry negative energy density. No $\rho\ge0$ medium of any kind survives; the cold energy
  is not a positive-mass fluid.
* **A null at the design sensitivity in a low-EFE subsample**: the positive-medium reading
  survives, and the law must depart from (1) near field null points — a quantitative target for
  the missing microphysics (how far, over what volume, is not computed here).
* **A null in a filament subsample says nothing.** Both pictures predict no dip there
  (suppression 0.002), so the test is only a falsifier where $g_{\rm ext}/a_0<0.3\,r_M/d$. This
  is the new, sharp statement: the published data are uninformative not merely because S/N < 1
  but because the prediction is switched off in the environments they sample.

## 5. Assumed values (explicit table)

| quantity | value | source |
|---|---|---|
| $G$, $M_\odot$, pc | 6.67430e-11, 1.98847e30 kg, 3.0856775814913673e16 m | brief |
| $a_0$ canonical / alt | 9.36e-11 / 1.13e-10 m/s² | brief |
| $\bar\rho_{\rm cold}$ | 2.2569e-27 kg/m³ | $\Omega_c/\Omega_b=5.364$, $\Omega_bh^2=0.0224$ (framework inputs) |
| $M_b$ per LRG | $10^{11.3}$ M☉ | EXT arXiv:1702.08485 ($\langle\log M_\star\rangle$) |
| $d$, $\langle z\rangle$, $N$ | 8.23 h⁻¹ Mpc, 0.42, 23 000 | EXT arXiv:1702.08485 |
| $\Sigma_{\rm crit}$, $n_g$ | 1640 M☉/pc², 11 arcmin⁻² | EXT arXiv:1702.08485 |
| box, $M_{\rm fil}$ | 7.1×2.5 h⁻¹ Mpc, (1.6±0.3)×10¹³ M☉ | EXT arXiv:1702.08485 (5σ) |
| $\sigma_e$ | 0.26 | assumed (CFHTLenS/LSST-like) |
| $h$, $\Omega_m$ | 0.7, 0.3 | EXT arXiv:1702.08485 cosmology |
| pair density | 149.4 deg⁻² | 23 000/154 deg², EXT |
| LSST / Euclid / Roman / DES $n_g$ | 27 / 30 / 45 / 10 arcmin⁻² | **assumed** survey specs |

## 6. Checks (what `a13_checks.py` proves)

K1 solver control reproduces $|\nabla\Phi|r=1$ (9.8e-4) and $\rho_{\rm ph}=1/(4\pi r^2)$ (5.7e-3).
K2 $C(0.2d)$ matches AG6C to 0.1%. K3 the column matches AG6C at matched resolution to 1.8%.
K4 the Richardson limit is −0.2293 with a converging increment ratio. K5 superposition gives
the wrong sign. K6/K7 the depths are within 20% of the paper and the −89/−33 ratios within 5–8%.
K8 reproduces AG7's 0.87 strip S/N to 7%. K9 the $\sqrt N$ scaling is exact and $\varepsilon$ is
in range. K10 the EFE curve is monotone and kills half the dip by $e=1$. K11/K12 the environment
split is quantitative. **12/12 PASS, under 60 s, deterministic, no network.**

## 7. What this does not do

* No 3-D projection of inclined pairs beyond the single-ray acceptance $\varepsilon$; the sky
  shape of the deficit for intermediate inclinations is not modelled.
* The external field is uniform and along the pair axis. A varying field, or one perpendicular
  to the axis, changes the numbers at the factor-of-a-few level, not the conclusion.
* Deep-$\mu$ only for the EFE sweep; the no-EFE solve is deep-$\mu$ with a full-$\mu$ cross-check
  at the cluster's $r_M/d$ (4%).
* Systematics not priced: the positive filament/bridge (comparable to the dip and must be
  modelled to isolate it), miscentring, correlated Kaiser–Squares noise, and the fact that the
  published error is 1.77× pure shape noise (using it would raise every $N$ by 3.1×).
* The framework's own departure from the law inside the medium is not computed — only bounded
  from below by the missing depth.

## 8. Next

1. Compute the inclined-pair deficit map properly (a 3-D projection of the same solution) and
   replace $\varepsilon$ with a selection function.
2. Run the EFE sweep with the full $\mu$ and with the field perpendicular to the axis.
3. Build the low-$g_{\rm ext}$ pair catalogue (void pairs, $|\cos i|<0.15$) from BOSS/DESI ×
   CFHTLenS/LSST and measure the actual $N$ available — that number, not the flux-limited one,
   decides whether the test exists.
