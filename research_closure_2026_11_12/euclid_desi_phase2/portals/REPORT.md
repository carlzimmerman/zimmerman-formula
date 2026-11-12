# Density, negative-pressure and canonical-potential portals: exact overlap and derivative-free tests

12 November 2026. Bounded analytic and symbolic route. No observations, cosmological likelihood fit, inferred agreement or healthy-action claim. Requested publication base `8db464d4bc...`; observed shared checkout HEAD `cace4617bb6a518bf910b56a4c0ee8bddce7fa07`. Exact reviewed source contents are pinned in `source_inputs.json`; no assertion that the moving checkout equals the publication base. All route writes are confined to this directory.

## Substantive result

After each portal profiles its own constant coefficient and matter amplitude, a running equation of state does **not** guarantee distinguishability. Density and canonical-potential portals have an exact overlap family consisting of an acceleration-squared power law **plus a dust-shaped term**, with different inferred matter splits. A fully positive, canonical, negative-pressure example below has evolving w and identical measured expansion and acceleration histories under both portals. No improvement in h(z) and q(z) precision can separate those two explanations on that family without extra matter or coupling information.

There is also a genuine discriminator outside the overlaps: derivative-free interval relations compare measured expansion endpoints to differently weighted integrals of the independently measured acceleration history. The pressure relation eliminates the matter amplitude exactly. It rejects the explicit density/potential counterexample at the equation level. Using it on finite noisy observations still needs an explicit latent interpolation/measurement model and full covariance; endpoint values alone do not determine the integrals.

This does not derive a new force law or close any failed gravity route. Its output is a precise boundary between a possible independent measurement and an observational-equivalence obstruction.

## 1. Definitions, branches and assumptions

Let u=1+z on a connected interval with u>0. Assume GR-form FRW background equations with a constant cosmological gravitational coupling G_cosm and a separately conserved homogeneous sector X. Let G_N be the constant local Newton coupling used in the galaxy-scale portal, and gG=G_cosm/G_N>0. Distinguish them; their equality is not derived.

Assume independent galaxy inference supplies T=DA a0, and BAO supplies dM=DM/rd and dH=DH/rd with one common constant ruler rd. Then

    q=T u/(c² dM)=a0 rd/c²,
    h=1/dH=H rd/c,
    Q=q²>0, F=h²>0.

All four quantities q,h,Q,F are dimensionless. DA=DM/u is the transverse-distance FRW relation. The assumed independent identification of T is not established here; the phase-1 nuisance obstruction remains binding.

Write the dimensionless dark density as

    X(u)=F-A u³-B u⁴-K u².

A>=0 is the conserved pressureless-matter coefficient, B>=0 the radiation coefficient, K the signed curvature coefficient. The primary exact overlap classification below sets B=K=0. The same classification applies after subtracting the **same fixed** B u⁴+K u² from F. If different unknown B,K are independently profiled under competing portals, the overlap grows; the simple power-law classification cannot be reused unchanged. Section 5 supplies the nuisance columns for that enlarged test without claiming the same theorem.

Energy conservation yields, in these dimensionless density units,

    Y = -p_X/c² in common density units = X-uX'/3,
    Z = V/c² in common density units = X-uX'/6=(X+Y)/2.

The candidate portals, with their own positive constants, are

    D: X=Cρ Q,
    P: Y=Cp Q,
    V: Z=Cv Q,
    Cj=8π gG/(3 κj²)>0.

Density promotion requires X>0. Negative-pressure promotion requires Y>0 and a positive-density branch of its integrated solution. A canonical-potential interpretation also requires Z>0 and kinetic density X-Z=uX'/6>=0; X>0 follows if both are nonnegative and at least one is positive. A formal V equation is not enough to establish canonical realizability. For the explicit smooth example these inequalities are strict. A canonical scalar background can then be reconstructed locally: its positive kinetic energy and H>0 determine a monotone field trajectory and V along it. This does not establish health of any additional coupling of that scalar to a0.

Since the coefficients are independently profiled, only shape differences count here. They measure κj/sqrt(gG), not κj separately. A common multiplicative calibration of q is absorbed into Cj; a redshift-dependent calibration can imitate portal evolution and must be constrained.

## 2. Exact pairwise-equivalence classification, flat late background

Let all constants below be independent of u. Matter amplitudes may differ between competing explanations.

### D and P: a pure power law is necessary and sufficient algebraically

Density predicts F=Aρ u³+Cρ Q. Inserting into pressure gives

    Cρ[Q-uQ'/3]=Cp Q,
    uQ'=s Q, s=3(1-Cp/Cρ).

For Q>0 on a connected interval, the solution is exactly Q=P0 u^s with P0>0. Positive Cρ,Cp imply s<3. Conversely every such power yields both equations with Cp=Cρ(1-s/3), provided the common background and chosen density split are positive. At s=3 pressure vanishes, so a positive CpQ branch is impossible. The pressure equation's dust integration constant leaves the matter-versus-X dust split unidentified, but does not enlarge this simultaneous D/P Q family.

A varying w outside this pure-power family separates D/P in principle. It is not enough merely to label a model 'evolving dark energy'; the acceleration history and expansion must supply the corresponding independent functions.

### D and V: power plus dust, with a resonant exception

Let density use Aρ and potential use Av. Then

    (Aρ-Av)u³/2+Cρ[Q-uQ'/6]=Cv Q,
    uQ'=s Q+d u³,
    s=6(1-Cv/Cρ)<6, d=3(Aρ-Av)/Cρ.

For s≠3, the complete algebraic solution is

    Q=P0 u^s+R0 u³,
    R0=d/(3-s),
    Aρ-Av=Cρ R0(3-s)/3.

For s=3, it is instead

    Q=u³[P0+d ln u], Cv=Cρ/2.

These families must be intersected with Q>0, nonnegative matter amplitudes and the canonical kinetic/potential inequalities. The logarithmic resonance is canonical on suitable intervals but need not have negative pressure; it is not silently included in a negative-pressure DE branch.

The dust term is a physical inverse-problem ambiguity, not a new matter species. With an independently fixed common matter amplitude Aρ=Av, d=0 and this overlap collapses back to pure powers. Without that information, normalized-w formulas that assume the same inferred rho_X miss an exact ambiguity.

### P and canonical V, and triple overlap

Since 2Z-Y=X, simultaneous pressure/potential conditions imply

    F-Av u³=(2Cv-Cp)Q.

Positive density requires L=2Cv-Cp>0. This reduces to D/P with Cρ=L; hence Q is a pure power with

    s=3(1-Cp/L)=6(Cv-Cp)/(2Cv-Cp)<3.

Canonical nonnegative kinetic density requires Cv>=Cp, giving 0<=s<3. The triple overlap therefore has

    F=A u³+Cρ P0 u^s,
    Cp/Cρ=1-s/3,
    Cv/Cρ=1-s/6,
    0<=s<3

on the common positive canonical/negative-pressure branch. Here w_X=s/3-1 is constant. s=0 is the vacuum limit with zero canonical kinetic energy. All portal coefficients can absorb the constant-w factors. Therefore no amount of q/h precision distinguishes all three on this family when their coefficients remain free. If the same independently fixed κ and gG are imposed in all three, equal coefficients restrict common overlap to the vacuum case; that is a stronger hypothesis than the profiled comparison requested here.

## 3. Explicit positive counterexample with evolving w

Take, for u>0,

    Q=u+u³/10,
    F=u+u³/2.

Density fits exactly with Aρ=2/5, Cρ=1:

    Xρ=u+u³/10,
    Yρ=2u/3,
    wρ=-2/[3(1+u²/10)],

which evolves and remains negative. Potential fits the **same F,Q** with Av=1/3, Cv=5/6:

    Xv=u+u³/6,
    Zv=5u/6+u³/12=(5/6)Q,
    kinetic=Xv-Zv=u/6+u³/12>0,
    Yv=2u/3>0.

Both matter coefficients and both dark densities are positive. The potential branch is a legitimate homogeneous canonical-scalar reconstruction with negative pressure; its w also evolves. This is not a constant-w loophole or a phantom example.

Pressure promotion cannot fit this pair F,Q with a single positive constant, because

    [F-uF'/3]/Q=20/[3(u²+10)]

is not constant. Thus the same example establishes (i) an exact density/potential no-go for discrimination without matter information and (ii) an actual equation-level pressure discriminator. It does not demonstrate that real data reject any portal.

## 4. Derivative-free interval observables

Let a<b be two u values. All following integrals are dimensionless. Define

    f_i=F_i/u_i³, r_i=Q_i/u_i³,
    Ip[a,b]=∫_a^b Q(u)u^-4 du,
    Iv[a,b]=∫_a^b Q(u)u^-7 du.

### Density: endpoint collinearity

D predicts f=Aρ+Cρ r. For any three distinct nodes,

    N_D=(f2-f1)(r3-r1)-(f3-f1)(r2-r1)=0.

Equivalently det[u_i³,Q_i,F_i]=0. This is exact using endpoints and does not require a Q interpolation. It becomes uninformative about Cρ when r is constant (Q proportional u³); near-collinearity requires a conditioning check. Positivity of Cρ and Aρ also matters.

### Pressure: matter-free interval ratio

The integrating factor is

    d(F/u³)/du=-3Cp Q/u⁴.

Thus Δp[a,b]=F(b)/b³-F(a)/a³=-3Cp Ip[a,b]. Two intervals give the coefficient-free null

    N_P=Δp[a,b] Ip[c,d]-Δp[c,d] Ip[a,b]=0.

No numerical differentiation of noisy H is needed, and no matter abundance enters. A strict finite-endpoint consequence of Q>0,Cp>0 is that F/u³ decreases with u. This sign condition needs no integral interpolation, though it is weaker than the full portal test.

For the explicit positive counterexample, intervals [1,2] and [2,3] give

    N_P=-0.0207828389337... ≠0.

It therefore distinguishes the pressure portal from the density/potential overlap if those continuous histories are known.

### Potential: two nuisance columns across intervals

The integrating factor gives

    d(F/u⁶)/du=-3Av/u⁴-6Cv Q/u⁷.

Hence, for each interval k=[a,b],

    Δv_k=F(b)/b⁶-F(a)/a⁶=Av X_k-6Cv Iv_k,
    X_k=b^-3-a^-3.

Three intervals produce det[Δv_k,X_k,Iv_k]=0, plus Av>=0,Cv>0. Unlike pressure this retains one matter column. For a four-node design these are not three statistically independent quantities: adjacent differences share endpoints and covariance must be retained. A collapse Iv∝X makes Av and Cv unidentifiable (for example Q∝u³).

### The finite-bin limitation is real

Exact Ip,Iv require information about Q **between** endpoints. Finitely many positive Q endpoint measurements, by themselves, do not determine either integral. Smooth positive interpolants can be made arbitrarily small between narrow endpoint layers or have arbitrarily large interior bumps without changing endpoint values. Thus the integrated nulls become data statistics only after specifying and validating a latent Q representation, resolved q sampling, bin-averaged kernels, or quantitative smoothness bounds. Calling trapezoidal integrals 'exact observables' would hide a functional prior. Endpoint-only pressure monotonicity remains exact, but the stronger N_P does not escape this limitation.

## 5. Radiation, curvature and covariance

For the full F with common ordinary radiation and curvature, the equations are

    D: F=Aρu³+B u⁴+K u²+CρQ,
    P: F-uF'/3+B u⁴/3-K u²/3=CpQ,
    V: F-uF'/6-Avu³/2-Bu⁴/3-2Ku²/3=CvQ.

Their derivative-free forms add explicit columns:

    pressure Δp=-3Cp Ip+B(b-a)+K(b^-1-a^-1),
    potential Δv=Av Δu^-3+B Δu^-2+K Δu^-4-6Cv Iv.

Known B,K can be subtracted. If B,K are free, a density design has four columns [u³,u⁴,u²,Q], pressure has three interval columns [Ip,Δu,Δu^-1], and potential has four [Δu^-3,Δu^-2,Δu^-4,Iv]. Corresponding overdetermination needs at least 5 density nodes, 4 pressure intervals, or 5 potential intervals, respectively, before accounting for interpolation parameters and correlations. These counts are necessary, not power guarantees. Competing models must treat shared curvature/radiation consistently. FRW transverse-distance geometry can supply further constraints, but it must enter the same likelihood rather than an independent, double-counted prior.

q depends on T and BAO dM, while F depends on the correlated BAO dH. Build a joint likelihood in latent T,dM,dH (and shared nuisances), propagate cross-bin and transverse/radial BAO covariance, and compute nulls or posterior predictive contrasts from that model. Noisy Q is not an exact design column. Comparing raw determinant magnitudes without their induced covariance is meaningless. A common q calibration rescales Cj and leaves shape discrimination intact; a redshift-dependent T/inclination/gradient calibration can change Q's shape and must be included.

A bounded filename search of locally available `_external_data` and `real_research/data` found no official BAO distance/covariance likelihood package usable for this route; a DESI P1D covariance is not BAO covariance. No cosmological fit was run and no public likelihood was claimed validated. A bespoke column model would in any case need consistent finite-redshift window predictions; substituting arbitrary effective-redshift endpoints is an approximation to document.

## 6. Prior-art boundary and what this advances

The September `real_research/dark_energy_inverse_2026_09_26/reconstruction/RESULT.md` already derives the pressure inverse with its dust integration constant (lines 30–55), the dust-insensitive pressure operator (83–130), and the integrated background family (132–150). The companion scales report already distinguishes G_cosm/G_N and κ/sqrt(gG), lines 24–46. Neither the pressure integrating factor nor uncalibrated acceleration/background inverse is new to this repository.

CT7 already distinguishes the density and canonical-potential portal for evolving w (report lines 30–48), and records a scoped coupling-health failure. This route does not overturn that health conclusion by reconstructing a homogeneous scalar background.

The narrower useful output is the explicit comparison **after profiling different matter amplitudes and portal constants**: pure-power D/P overlap, power-plus-dust D/V overlap and resonance, canonical triple-overlap branch, positive evolving-w counterexample, and interval-column tests with their finite-function-information limitation. This is a bounded repo-level synthesis, not a literature novelty claim.

## 7. Evidence and next discriminating step

`contract.json` was written before the symbolic experiment. `portal_checks.py` independently verifies operator identities, five specified power cases, overlap ODEs, the canonical positive counterexample, logarithmic resonance, interval determinants and a dust-shaped rank collapse. **41 checks pass** in `run02/results.json`; manifest status is completed and the installed validator reports valid evidence. The checks establish these explicit identities/cases, not arbitrary observations or a healthy completion.

First launch `run01` failed at JSON serialization of a SymPy Boolean after assertions, with no accepted result artifact. Its source is preserved as `portal_checks_failed_run01.py`; run02 converts that output boolean to a native type. No interpretation depends on the failed launch. Source-input hashes are pinned; the runner hashes code and outputs.

The next discriminating work is to determine whether the independently recoverable q histories at actual galaxy/BAO redshift windows resolve a departure from the overlap family **after nuisance projection**. Before fitting observed agreement: specify a finite Q basis/window model, derive joint covariance and test rank against its density/potential overlap directions and pressure moments. An independent matter-amplitude constraint can specifically break the D/V dust ambiguity; better precision in the same two background observables cannot do so on the exact overlap. If q reconstruction or its between-bin modes are unconstrained, report NO VERDICT rather than impose an interpolant that selects the desired portal.

The external claim remains: these are conditional observable relations. They do not fix κ from first principles, supply a stable relativistic action, establish that Euclid provides independent dynamics, or show that any theory has passed its existing gates.
