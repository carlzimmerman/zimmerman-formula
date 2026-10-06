# Building on Claude p57: EFE and the vacuum tail moment are independent functionals

The independent QUMOND kernel integral gives `Q2=2.1986334498e−26 s^−2` for p35/p57's k2 turnoff at T128.9153707043. This agrees with p57's field-equation multipole result and retains its tension with the cited2014 Cassini estimate. Suppressing the strong-field radial anomaly does not suppress the transition-region external-field quadrupole.

A stronger mathematical result follows: two compact high-y kernel perturbations can preserve **exactly** the inner Q2 and the external far-field linear response while changing `C=integral y(nu−1)dy`. Positive, decreasing nu and an increasing y nu map survive. An illustrative Cassini-admissible base also has this freedom. Therefore one quadrupole bound, that external response, and these NR constitutive inequalities cannot uniquely select C or32pi. This is local nonidentifiability, not a claim that arbitrary target moments remain admissible or that all Solar System/gala­xy scores are unchanged.

## Actual source state, scope and overlap

Inspected HEAD `6988a2ecbab63393c26a160f81ee15a4391d6a0a` contains p57's QUMOND multipole solver and explicitly withdraws its earlier algebraic EFE model. The actual p57 and p56 code, `qumond_efe_multipole.py`, p35 kernel code and CFG355 README were read and pinned in the run manifest; none was imported or executed. p57 is a reduced secular test with giant-planet quadrupole, Galactic tide, lost-particle rule, multipoles l<=8 and150 particles. Its registered final-fraction criterion is INCONCLUSIVE; the separately declared occupancy metric retains the TNO concern. This report authenticates the field-theory dependence and one Q2 value, not that orbit integration, a full Neptune-scattering population, or a new empirical fit.

CFG355's actual results atbe5eee875 are now present: its scored rank veto removes the generic host three-stream shell, fails its continuous-edge and lensing criteria, and retains rank0/rank1 false positives. The orientation/rank regularity notes in `../../main_theory/claude_cfg354_orientation_2026_10_06/REPORT.md` remain separate action obligations. They are not replaced by the campaign's algebraic stress contractions. No CFG355 rerun or new score is claimed.

The nearest earlier Sol61 puzzle counterfamily varied high-y bumps while fixing low-y landmarks. The advance here is an **exact QUMOND Q2-null** perturbation with an explicit field-equation kernel weight, not merely low-y agreement. No global literature novelty is asserted.

Primary source versions, locators and notation are recorded in SOURCES.md. The named source claims are narrow: Milgrom's NR action/gradient projection, its external asymptotic potential, and Hees et al.'s2014 quadrupole convention and estimate. The integral reduction and null-space construction below are derived here. A relativistic vacuum normalization is an additional input throughout.

## QUMOND action, physical force and external boundary

Use the NR action

`L=−[2 gradPhi·gradPhiN−a0² Qfun(|gradPhiN|²/a0²)]/(8piG)+rho(v²/2−Phi)`,

with `nu(y)=Qfun'(y²)`. Its variations give `DeltaPhiN=4piG rho`, `DeltaPhi=div[nu(|gradPhiN|/a0)gradPhiN]`; test acceleration is `−gradPhi`. This is the gradient projection of `nu gN`, not generally that algebraic vector itself. These equations and the conserved-action setting are [Milgrom2010 Eqs3–8](https://arxiv.org/html/0911.5464v2).

For a point Sun and uniform external Newtonian field `a0 e ez`, take `G=−GM rhat/r²+a0 e ez`. Define `D=[nu(|G|/a0)−1]G−[nu(e)−1]a0 e ez`. The anomalous acceleration potential psi=−Phi_p satisfies `Delta psi=div D`; physical anomalous force is `grad psi`, with its uniform value at the Sun subtracted. In p57 the observed external magnitude is modeled as `ge=a0 e nu(e)`; its chosen ge,a0 fix e through this equation. This is the declared uniform-boundary/Galactic conversion, not a derivation of the actual nonspherical Galactic field from the observed magnitude alone.

A local example explains the withdrawn algebraic model. Around external dominance, the algebraic linearized field is `nu_e[I+K_e ez ez]delta gN`, `K_e=e nu'(e)/nu(e)`. At an oblique Fourier wavevector this vector generally has nonzero curl. The physical potential instead has the scalar Fourier response

`deltaPhi(k)=nu_e[1+K_e kz²/k²]deltaPhiN(k)`.

For a compact point source its asymptotic potential is

`Phi_internal=−GM nu_e[1+(K_e/2)sin²theta]/r`,

including the monopole fixed by the surface flux. This agrees with [Milgrom2010 SecV.1 Eqs57–60](https://arxiv.org/html/0911.5464v2). Kernels identical near e have identical nu_e,K_e and this far-field response. This is a distinct observable from the inner quadrupole and from the radial spherical force.

## Exact inner quadrupole functional

Adopt the potential convention

`Phi_Q=−(Q2/2) r²(cos²theta−1/3)`.

Then `Q2=Hessian(psi)_zz−Hessian(psi)_xx`, with psi=−Phi_p. The [Hees2014 Eq6/8](https://arxiv.org/html/1402.6950v2) convention has Milgrom's dimensionless `q=−2Q2 rM/(3a0)`, `rM=sqrt(GM/a0)`. This explicit convention fixes the sign; no observational sign is inferred from an unnamed Hessian convention.

From the Poisson Green function, axisymmetry and integration by parts,

`Q2=−(9/4) integral_0^infinity dr/r² integral_-1^1 dmu [Dr(3mu²−1)+2Dtheta mu sqrt(1−mu²)]`.

The constant external subtraction has zero angular contribution. Set `u=rM/r`, `xi=−mu`, and

`y=sqrt(e²+u^4+2e u² xi)`.

The result is the signed kernel functional

`Q2=−9a0/(4rM) integral_0^infinity du integral_-1^1 dxi [nu(y)−1]{e(3xi−5xi³)+u²(1−3xi²)}`.

Thus the physical scale is a0/rM, and the remaining functional is linear in nu at fixed e. It samples the full phantom source; it is not a pointwise force law at Saturn's very large local y.

For an exact one-dimensional reduction put t=u², `xi=(y²−e²−t²)/(2et)`. The triangle limits at fixed y are `|y−e|<=t<=y+e`. Define

`w_e(y)=integral_|y−e|^(y+e) y/[2e t^(3/2)] {e(3xi−5xi³)+t(1−3xi²)} dt`.

Then

`Q2=−9a0/(4rM) integral_0^infinity [nu(y)−1] w_e(y)dy`.

A primitive of the t integrand is

```
P(t;y,e)= y/(280e³ t^(7/2)) [
 −25e⁶+35e⁴t²+75e⁴y²−35e²t⁴+70e²t²y²−75e²y⁴
 −7t⁶−105t⁴y²−105t²y⁴+25y⁶ ].
```

The weight is `P(y+e)−P(|y−e|)`. Endpoint factoring is essential near y=e; evaluating the unfactored polynomial there catastrophically amplifies rounding errors. The integrable singularity at this cancellation shell is not a physical divergence in Q2.

The exact weight is negative below e and positive at sufficiently large y; cancellations are physical. Its high-y expansion is

`w_e(y)=e²/(10 y^(3/2))+11e⁴/(112 y^(7/2))+165e⁶/(1792 y^(11/2))+O(e⁸ y^(-15/2))`.

The source changes near y~e~O1 therefore have much stronger quadrupole leverage than high-y changes. By contrast, the proposed vacuum moment uses weight **y**, not w_e. The kernel equality at low y alone is not exact preservation of Q2: high-y sources have a small but nonzero contribution. The null construction below removes that contribution exactly.

## Why the p35 tail does not cure p57's EFE

The actual kernel is

`nu_T(y)=1+[sqrt(1+1/y)−1]/[1+(y/T)²]`.

For y of order1 and T~129 its correction to the transition is only order T^−2. Around the Sun's MOND radius the internal Newtonian field and external field are both order a0, so this region remains almost unchanged. Far inside that radius, where y>>T, the radial anomaly is suppressed. The vacuum integral, meanwhile, accumulates over the much longer high-y interval and is strongly T-dependent. These different dependencies are now exhibited by the weight above rather than assumed from orbital radius alone.

For p57's `a0=9.3603e−11 m/s²`, `ge=2.146e−10 m/s²`, `GM=1.32712440018e20 m³/s²`, the independent integral gives

`e=1.84663944422`, `nu_e=1.24153178205`, `K_e=−.175696504659`,

`Q2=2.198633449823e−26 s^−2`, `C=100.530964914879`.

The latter agrees with32pi because T was chosen for that moment; it is not a prediction of its selection. p57 reports2.199e−26 for the turnoff and2.195e−26 for the unsuppressed law. The independent result verifies the former field value without integrating particles or using p57's multipole source discretization.

Hees et al.'s specific2014 fit is `Q2=(3±3)e−27 s^−2`, corresponding to the illustrative positive two-sigma ceiling9e−27 used here. The p35 target branch is above that ceiling in this QUMOND boundary/parameter model. This reproduces an existing tension; it is not a new Cassini data reduction, a current ephemeris certification, a QUMOND-to-AQUAL equivalence, or an exclusion of all MOND actions. Other kernel shapes, screening, source models and external-boundary conversions are changed premises.

## Exact Q2-null direction with nonzero vacuum moment

For fixed e let `b1,b2` be nonnegative C2 bumps on disjoint high-y intervals and define

`qj=integral w_e bj dy`, `cj=integral y bj dy`, `r=q1/q2`.

For sufficiently high supports qj>0. The perturbation

`delta nu=t[b1−r b2]`

has exactly `deltaQ2=0`, whereas `deltaC=t(c1−r c2)`. Since `w_e(y)/y~e²/(10y^(5/2))` is nonconstant, supports can be chosen so `c1/q1 != c2/q2`; hence deltaC!=0. The analytic statement defines r by the **exact** integrals. Numerically reporting zero using the same finite ratio is not a separate exactness certificate; the linear-functional proof supplies exact cancellation. Smooth compact C-infinity bumps can replace the C2 examples without removing the independent-functional argument.

The declared examples use `B(z)=z³(1−z)³` for0<=z<=1, zero outside, `Y=1000`, `b1=B(y/Y−1)`, `b2=B(y/Y−3)`. Their exact moments are `c1=3Y²/280`, `c2=7Y²/280`. For the p35 target base,

`r=3.634627441772`, `t=5e−8`, `deltaC=−.00400757001650`.

Both bumps vanish in a neighborhood of e, so nu_e,nu'_e and the unique external root in the declared conversion remain exactly unchanged. Q2 is also unchanged, but the moment changes. For a Cassini-admissible illustrative base use

`nu_mix=.999 nu_mu20+.001 nu_T`,

where the exact spherical inverse of `mu20(x)=x/(1+x^20)^(1/20)` is

`nu_mu20(y)=[(1+sqrt(1+4/y^20))/2]^(1/20)`.

Both kernels have the same leading deep-MOND normalization, so their convex mixture does too. The independently computed mixture has `Q2=2.88342560838e−28 s^−2`, `C=.271062189096`. Its high-y null perturbation with t5e−11 gives `deltaC=−4.00757328828e−6` while preserving Q2 and the external response. This demonstrates nonuniqueness **inside** the cited Cassini margin, not only around the excluded target kernel. This mixture is not claimed to fit SPARC or to attain32pi under further constraints.

## Uniform constitutive margins and scope of “health”

The bumps obey `|B|<=1/64`, `|B'|<=3/16`. Their perturbations therefore have explicit uniform value and derivative bounds. For the tail kernel,

`(y nu_T)' >=1−9/[16sqrt(3)T]`,

because its excess `b(y)=1/[sqrt(1+1/y)+1]` satisfies0<b<1/2 and b'>0. On the two supports the negative logarithmic slope of nu_T−1 also has the lower bound used in checks.py. For the mixture, its tail contribution supplies the displayed positive-value/slope margins. Its mu20 piece is monotone decreasing and, on y>=Y, `(y nu_mu20)'>1−Y^−20`; outside the supports the unchanged exact inverse map is increasing (globally its derivative has the weaker bound1/2). Thus the reported approximately.997 source-map margin applies on the perturbation supports, not a claimed minimum over the mixture's whole low-y domain.

After perturbation the p35 uniform margins are `nu−1>1.2685e−7` and `−nu'>1.4512e−11` on the supports; the source-map margin exceeds.99748. The corresponding mixture margins are scaled but strictly positive. Away from these supports the original constitutive inequalities are unchanged.

These are standard **NR constitutive admissibility** inequalities: nu>=1, nu decreasing, and y nu increasing. They are not a full relativistic ghost, gradient, causal or energy certificate. The finite-acceleration clock ghost analysis concerns a different KGB action and physical clock-gradient operator; its result is not inferred for this QUMOND action by reusing a similar kernel symbol.

The two-bump argument preserves one inner quadrupole at one external boundary and the asymptotic linear response. Higher inner multipoles, finite-radius force, monopole precession, TNO occupancy, and other Galactic responses generally change. Full Solar System or galaxy scores are not preserved merely because Q2 is. Nor does an infinitesimal direction prove arbitrary finite moment adjustment within all constraints. It is sufficient to refute unique moment selection from the specified inputs.

## BIMOND normalization remains a separate arrow

p35's `C=integral_0^infinity y(nu−1)dy=I/2` and `Lambda/a0²=C` invoke its independent QUMOND/BIMOND vacuum-offset interpretation and normalization. QUMOND's NR force action alone does not source a relativistic cosmological constant or establish that equality. The constant in Qfun and its relativistic source interpretation remain additional obligations. Nothing here assigns this C to the log-KGB/cuscuton sector, whose action is different. The mathematical distinction between the two kernel weights remains valid conditional on adopting that vacuum dictionary.

## Evidence and exact remaining implication

`runs/main_b` has24 passing assertions: exact primitive/series/bump moments, independent 55-digit field and moment values, and uniform deformation margins. Three controls fail as intended when they assert unique C, replace the projected field by an isotropic algebraic response, or confuse observed eta with external Newtonian e. All four current manifests validate. Quadrature is high-precision but **not interval certified**; the high-y weight uses eight Taylor terms only for e/y<.001. The universal null-space argument is analytic and independent of finite precision.

The first main_a run failed numerical benchmarks because the unfactored endpoint primitive caused severe near-shell cancellation. Its raw results, log and exact historical script are retained; those enormous failed Q values are implementation errors, not physical claims. Current main_b factors the endpoints and reproduces the independently discretized p57 field result. The report is not a run input; final prose does not stale the records. No more runs are needed for this checkpoint.

The remaining selector must constrain additional kernel functionals or the full relativistic action strongly enough to eliminate the exact null directions. Cassini rules against this target-shaped kernel in the declared standard QUMOND model; it does not by itself pick a vacuum moment. A concrete next discriminator would compute the changed higher multipoles/finite-radius response of the same admissible null family, or provide an independently justified action relation that fixes its high-y function. Either must be executed; it cannot be supplied by the target32pi value itself.
