# Compact surplus: a matched core exists, but the joint explanation fails

CS-20261022, continuation of RF-2026-10-22-1. The local passive action admits numerically matched, finite-mass cold cores. A fitted member is compatible with the previous dwarf/rotation summary statistics when added phenomenologically to the existing law. A single central compact core fails the cached cluster profile test. Neither its abundance nor its mass is selected by the action, and the phenomenological addition is not a global solution. The requested common explanation has therefore **not** been obtained.

All results are self-reviewed. The original parent action remains incomplete; these are Newtonian necessary tests. Write scope is this directory only.

## 1. What the exterior changes

Use the reciprocal-field action with X=0, no polarization gradient stiffness, isolated reference density zero, and the local passive scalar limit. Write K=4piG, h=e/chi, u=KP_r, g=Phi', and

    e=rho_c-div P,  chi=chi0+h^2/(2mu_phase^2),
    F(u)=a0 u/(a0-u),  0<=u<a0.

Inside occupied stationary cold matter, its Euler equation gives h=mu_c-Phi and the polarization equation gives F(u)=g. In vacuum only the polarization equation remains:

    h'=-F(u),    (r^2 u)'/r^2=-K chi h.

It is wrong to extend h=mu_c-Phi into vacuum. The exterior gravitational field follows Poisson and the actual mass; polarization carries no independent Newtonian Poisson source in this action.

With x=r/ell0, ell0=(K chi0)^(-1/2), s=h/(a0 ell0), y=g/a0, w=u/a0 and lambda=(a0 ell0)^2/(2mu_phase^2 chi0), the interior equations are

    Q'=x^2[B+s+lambda s^3],  s'=-y,
    Q=x^2 y^2/(1+y),        w=y/(1+y).

The exterior equations are

    s'=-w/(1-w),  w'=-2w/x-s-lambda s^3.

Match s,w and the gravitational field at a free cold boundary, requiring s,w to decay at infinity. The decaying linear tail is s proportional to exp(-x)/x, w proportional to exp(-x)(x+1)/x^2. The finite numerical boundary uses this asymptotic relation, not zeroing both fields artificially.

**A density jump is necessary and permissible in this reduced action.** Define C=rho_c/[a0/(K ell0)] and S=s+lambda s^3. Direct differentiation gives

    C = [B+(1+y)^2 S+2y^2/x]/[y(2+y)].

For positive s,y and nonnegative baryons this is positive even at the occupied edge; C drops to zero outside. P and h remain continuous, so there is no delta function in div P or in grad h, no mass shell, and no unbalanced delta-function material force. The radial free-interface corner condition is also continuous: after subtracting mu_c rho_c, the matter/field energy's corner expression reduces on both sides to r^2[W+V-e h-2P_r h/r]. No separately imposed confining wall is used. Positive scalar/polarization gradient regularizers would require a new interface analysis.

The density has an integrable central cusp, not a constant-density centre. For d=[B(0)+s0+lambda s0^3]/3,

    y ~ sqrt(d x),  C ~ (5/2)sqrt(d)/sqrt(x),  M(<r) ~ r^(5/2).

The potential/field energy and enclosed mass remain finite. Thus these are weak static candidates with a cusp and an edge jump, not globally smooth stellar equilibria.

The exterior also satisfies the necessary constrained-density condition Phi+h>=mu_c. At the edge equality holds. Its derivative is A=g-F(u). At any subsequent zero of A,

    A'=K rho_b + 2[u F'(u)-F(u)]/r + K chi h F'(u)>0,

on a positive exterior branch. Hence A cannot cross from positive to negative. The numerical solutions check the potential gap directly as well.

### Correction to the interpretation of the earlier radius bound

The earlier comparison proof applies while cold matter is occupied and h'=-g. A matched core ends **before** the first zero of the artificially continued occupied equations. In its physical vacuum exterior e=chi h is still positive, with div P=-e and rho_c=0. Thus positive mismatch does not itself represent a local gravitating density, and its tail is not bounded in extent by pi ell0. The cold edge in these matched positive branches remains below that bound. This distinction prevents a false exclusion and a false extra lensing halo.

## 2. Mass profile and conditional lensing

The mass scale is M0=a0 ell0^2/G. For an interior Plummer baryonic source of dimensionless total mass b and scale ell0,

    M_c(<r)/M0 = x^2 y(x)-b x^3/(1+x^2)^(3/2),    x<x_edge.

Outside the cold edge this mass is constant. The actual total gravitational field there is

    g(r)=G[M_c+M_b(<r)]/r^2.

The mismatch mass inside the edge is M_e/M0=Q-b x^3/(1+x^2)^(3/2). The remaining difference M_c-M_e=M0 x_edge^2 w_edge is the polarization flux; an equal positive mismatch integral exists outside, cancelled locally by div P. Counting that exterior e again as gravitating mass would double count.

The action supplies no second metric potential or photon coupling. **Conditional on** a weak-field metric with equal potentials and negligible extra field stress, the cold mass has the usual thin-lens projection:

    Sigma_c(R)=2 integral_R^edge rho_c(r) r dr/sqrt(r^2-R^2),
    DeltaSigma_c=M_cyl(<R)/(pi R^2)-Sigma_c(R).

Outside the cold edge:

    Sigma_c=0,  DeltaSigma_c=M_c/(pi R^2),
    physical deflection alpha_c=4G M_c/(c^2 R).

These formulas are mass projections and a conditional lensing mapping, not a relativistic prediction of the parent theory. The standard mapping is documented, for example, in [Bartelmann & Schneider's lensing review](https://arxiv.org/abs/astro-ph/9912508) and [the galaxy–galaxy lensing analysis](https://academic.oup.com/mnras/article/432/2/1046/1021994). No source redshift geometry is required for DeltaSigma; converting to shear requires Sigma_crit.

## 3. Matched solutions and what they do not select

All 16 declared combinations s0=.01,.1,1,10; lambda=0,1; b=0,1 match to a positive decaying exterior. Repeating with tighter tolerance and extending the far boundary from edge+20 to edge+30 changes the checked radius/mass/edge potential by at most 3.00e-6 relatively. Independent volume integration reproduces enclosed mass; exterior constrained-density inequalities pass to tolerance. This verifies this finite bank, not a general existence/uniqueness theorem or stability.

For the constant-susceptibility limit lambda=0 with no baryons:

| s0 | edge / ell0 | cold mass / M0 |
|---:|---:|---:|
| .01 | .267095 | .00175946 |
| .1 | .629062 | .0473922 |
| 1 | 1.459137 | 1.345168 |
| 10 | 2.569509 | 26.691624 |

At ell0=.440422 kpc, M0 is 1.30258e8 solar masses on the canonical footing and 1.57418e8 on the alternate footing. Changing s0 changes conserved mass. Vacuum matching determines the edge for that state; it does **not** choose the state or supply mass from nothing. The b=1 trials impose a baryonic density profile; their baryonic equation of state/distribution function was not solved. The b=0 trials establish the cold-sector candidates without that extra background assumption.

## 4. Dwarf and rotating-dwarf compatibility: encouraging but conditional

To connect to the prior empirical work without falsely calling it an action solution, retain CFG870's nu_e law and add the finite enclosed mass of a pure-cold lambda=0 core. Freeze ell0=.440422 kpc. Fit only s0 to the inherited MW calibration sample; use no per-object core masses. This generously assumes the law halo survives and the core profile can be superposed. Neither assumption follows from the nonlinear action. The fixed-chi limit also gives this diagnostic its simplest profile.

| quantity | canonical footing | alternate footing |
|---|---:|---:|
| calibration objects under inherited selection | 10 | 9 |
| fitted central s0 | .148204 | .115932 |
| fitted cold mass | 1.0950e7 solar masses | 9.2496e6 solar masses |
| cold edge | 321.5 pc | 293.0 pc |
| calibration RMS ln dispersion residual | .2156 (law .5683) | .2199 (law .5569) |
| M31/field, 17: mean ln dispersion residual | +.0551 +/- .0542 | +.0458 +/- .0560 |
| UFD, 21: mean ln dispersion residual | +.0923 +/- .1157 | +.0654 +/- .1129 |
| SPARC rotating dwarfs, 56: mean dex acceleration residual | +.0267 +/- .0220 | -.0077 +/- .0221 |

The uncertainties here are sample standard errors, not full observational likelihoods. The UFD scatter remains large. Dwarf dispersions use the predecessor's half-light mass estimator; no anisotropic Jeans or distribution-function fit was performed. The SPARC statistic uses galaxy medians and the predecessor's quality cuts. It changes little from the law-only mean (+.0319 / -.00398 dex), so this small fitted core need not spoil that summary statistic.

This is evidence for a **phenomenological dwarf-sized compact component**, not mass selection, abundance, capture, retention, stability, or a solution with dynamical baryons. The previously derived reciprocal mediator force remains another required contribution in a real rotating solution.

## 5. The central compact-cluster test fails on shape

Use the cached 318-object CFG687 arrays, independently reproducing the canonical baseline band amplitudes exactly. Fit one centred unresolved core template only on MID bins; predict INNER and OUTER without refitting. Test both a common mass and mass proportional to gas mass. The two baselines separate actual finite-core gravity from a generous preservation assumption:

- PN: baryons' Newtonian lensing plus a compact cold mass, as follows outside the finite cold support in this action.
- PL: the existing empirical law lensing plus a compact mass. This is a favorable phenomenological extension, **not** the matched action solution.

A is observed/model band amplitude; A<1 means too much predicted signal.

| baseline / mass prescription | fitted median mass, solar masses | INNER A | OUTER A |
|---|---:|---:|---:|
| PN + common mass | 9.514e13 | .196 | 1.853 |
| PN + gas-scaled mass | 8.789e13 | .160 | 1.837 |
| PL + common mass | 5.028e13 | .329 | .833 |
| PL + gas-scaled mass | 4.645e13 | .273 | .831 |

All MID amplitudes equal one by construction. Even keeping the law baseline, the compact core overpredicts INNER by factors 3.0--3.7. With only baryons outside it, INNER is overpredicted by factors 5.1--6.3 and OUTER is underpredicted. The 30-group RA jackknife repeats the MID fit; its descriptive PL/common INNER and OUTER residual scores are -12.1 and -2.29. These are not full-covariance exclusion significances. The more robust conclusion is the large radial shape mismatch.

All core edges allowed by the strict inherited bound are below 1.384 kpc, far below the first lensing bin (150 kpc). Changing the internal core profile cannot alter its R^-2 signal at those radii. Raising the core mass or refitting its central state therefore cannot cure this centred-template failure. The conditional test uses the canonical cached baseline only; it is not an alternate-footing cluster likelihood. Miscentring, an extended population of many orbiting cores, and new field stresses would change the tested model and need independent prescriptions.

## 6. Growth and the simultaneous requirements

A compact core does not introduce a new linear scalar source in the homogeneous background. At the retained ell0, the predecessor's EdS/quasistatic diagnostic retains .999500 of dust amplitude at k=.1/Mpc and .955654 at k=1/Mpc. That conditional result remains unchanged; it is not a full cosmological pass. If a significant fraction condenses into cores, their collective dynamics and formation history cannot simply inherit the homogeneous-fluid calculation. No abundance/formation model has been supplied to compute that change.

Outside a single finite core plus finite baryons, circular velocities ultimately decline as r^-1/2. Polarization alone does not restore flat curves in a vacuum Poisson region. The law-plus-core dwarf test thus cannot establish global rotation-curve preservation. With an independently preserved baseline of 200 km/s at 10 kpc, a 10% speed tolerance would allow at most 1.95e10 solar masses of additional compact matter there, neglecting mediator cancellation. The fitted dwarf core is small enough; cluster-sized cores would be disastrous if assigned indiscriminately to galaxies. This illustrates the missing population selection, not a prohibition on different conserved inventories.

**Disposition:** compact cold equilibria survive the exterior check; fitted dwarf compatibility survives the limited empirical check; one central compact core does not explain the cluster shape. The original joint target remains open. The next materially different compact route would require an extended distribution of moving cores with derived formation/transport and reciprocal baryon dynamics, plus a metric completion. It must predict both mass inventory and spatial distribution; assigning a cluster-only profile would not resolve the mechanism.
