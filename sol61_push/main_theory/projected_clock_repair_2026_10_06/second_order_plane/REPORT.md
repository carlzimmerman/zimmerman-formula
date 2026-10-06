# Simultaneous second-order mean solution of the shear-repaired action

For the declared decaying relative plane scalar, the changed action's **full second-order common metric rows** have an explicit regular solution on every compact de-Sitter time interval when 0<η<1. This includes the lapse, longitudinal shift, common curvature, homogeneous trace and homogeneous anisotropy; the local clock equation follows and is checked with the actual quadratic source. This is stronger than inverting a bare clock equation.

It is not admission of the whole perturbation or a nonlinear existence theorem. The exact inherited norm-cube term supplies a separate second-order relative source. Its nonanalytic amplitude dependence and spatial cusps make smooth second-order metric admission a further physical question. This report preserves that question; it does not truncate that term and call the altered theory complete. A and η remain arbitrary.

## 1. Same action, seed and raw ADM evaluation

The parent frozen report/checks define S=S0−ηK∫(Vgσg²+Vhσh²), shared timelike clock, n=3, K>0, H>0, a=exp(Ht), Λ=3H², 0<η<1. The actual local envelope is M_eff=−A+I/2−I^(3/2)/12+… . The new operator's static and isotropic-FRW first variations vanish, but that does not establish their perturbative health. This calculation concerns the admitted empty coincident de-Sitter vacuum only.

Let the first relative lapse u(t,x)=v(t)cos(kx), vdot=−Hv, k>0 on a flat periodic box. Use an ordinary amplitude expansion; quantities below are coefficients of ε², not coefficients with a factorial 1/2. The exact convenient seed representative and common test fields are

Ng=exp(V+u/2), Nh=exp(V−u/2),
γg=a²diag(exp(2Z+u),exp(2Z−u),exp(2Z−u)),
γh=γg with u→−u,
Sg^x=S+H u_x/k², Sh^x=S−H u_x/k².

The mean Z,V,S are varied BEFORE setting them to zero. A common spatial gauge is used here; the relative first-order shear is retained in this seed. The representative's quadratic fields are a choice, so the necessary mean corrections below are defined relative to this chart, not gauge-invariant effective densities.

For one metric set γ=a²diag(e^X,e^Y,e^Y). With contravariant shift s,

kx=(H+Xdot/2−sXx/2−sx)/N,
ky=(H+Ydot/2−sYx/2)/N,
R^(3)=a^−2 e^−X[−2Yxx+XxYx−3Yx²/2].

Its exact ADM density is K a³N e^((X+2Y)/2)[(1−η)(kx²+2ky²)−(1−η/3)(kx+2ky)²+R^(3)]. The actual geometric-mean constant is −12KH²a³exp(V+3Z). The retained leading projected term is Ka exp(V+Z)cosh(u)u_x². The latter is derived from the averaged inverse spatial metrics and r=ln(Ng/Nh)=u; fixing its lapse/volume factor would miss sources.

The norm-cube begins at |ε|³ in the action. Its COMMON variation on this pure-relative seed begins at that order, not order ε², because the common clock variation of the relative acceleration cancels at coincidence. Hence the following common second-order sources apply to the full stated local envelope. This does not remove the order ε|ε| RELATIVE Euler force.

## 2. Raw sources and independent clock identity

Evaluate each Euler derivative at mean fields zero and take its ε² coefficient. With c=Ka³, the actual sources are

JV=−Ka[3H²a²k²u²−4H²a²u_x²−4k⁴u²+4k²u_x²]/k²,
JS=−(2/3)Hc(8η−15)u u_x,
JZ=−H²c(3k²u²−4u_x²)/k².

These are respectively logarithmic-common-lapse, contravariant-common-shift and common spatial-curvature Euler densities. The source-aware action contains JV V+JS S+JZ Z. For a nonzero Fourier mode, JS=∂x jt where jt=Hc(15−8η)u²/3, so integration by parts gives jt t with t=−∂xS.

Under a common temporal metric variation δZ=HT, δV=Tdot, δS=−a^−2∂xT and δθ=T, diagonal Noether invariance gives

Jθ=JVdot−HJZ−a^−2∂xJS
   =KaH(6−16η/3)(k²u²−u_x²).

The shear term can also be checked covariantly: on the seed, σ2^x_x=−2H u_x²/(3k²), σ2^y_y=σ2^z_z=H u_x²/(3k²) in both sectors. Its background clock variation is −a^−2 times the tracefree Hessian of π. Thus its Euler source is 4ηKa∂i∂jσ2ij=−16ηKaH(k²u²−u_x²)/3, agreeing with the independent temporal identity. The source integrates to zero over the box.

Raw Jθ must NOT be inserted into the already-eliminated homogeneous-row mean operator: the actual second-order lapse and shift sources also enter their elimination. Doing so gives the wrong solution. This is tested by a dedicated control.

## 3. All nonzero second-harmonic rows solved together

Let p=(2k)²/a² and r=v². Write the mean coefficients Z,V,t multiplying cos(2kx). Their sources are

JV=cr(p−7H²/2), JZ=−7cH²r/2, Jt=Hcr(15−8η)/6.

The FULL mean scalar action at this harmonic is

L=2c[−6F²−4Ft−2ηt²/3+2pZ²+4pVZ]
  +Jt t+JV V+JZ Z, F=Zdot−HV.

The intrinsic curvature and lapse coefficients are mean-sector coefficients, not the relative ones. The shift and lapse rows are both retained. Eliminating them WITH their sources gives the exact curvature Euler row

EZ=cp[9H²(1−η)r+16ηpZ+2ηpr]/[6H²(η−1)].

No curvature acceleration or velocity remains: it is the source-aware elliptic mean constraint. Therefore the simultaneous solution is

Z2=−r/8−9(1−η)H²r/(16ηp),
V2=r/8,
t2=Hr(9−8η)/(16η).

The shift is S2=−t2 sin(2kx)/(2k). Since rdot=pdot/p times r=−2Hr, the r/p part of Z2 is constant in time. Direct substitution into all three RAW linear mean Euler rows plus their quadratic sources gives zero; it is not just a reduced clock solution. On a compact time interval these fields are finite and smooth. η→0, k→0 or a global infinite-duration/large-amplitude limit is not uniform.

The linear, uneliminated clock row evaluated on these fields equals −cHpr(9−8η)/6. The raw clock source equals +cHpr(9−8η)/6. They cancel. Common spatial Noether invariance recovers the common longitudinal-spatial equation after the momentum row; it is not another independent spatial gauge choice. The plane seed and these scalar products have equal transverse y/z entries, hence no finite-k transverse-traceless or vector source. This does not classify arbitrary multipolar data.

## 4. The actual zero mode and homogeneous anisotropy

The nonzero-mode inverse cannot be extrapolated to k=0. Spatial averaging the raw sources gives JV0=JZ0=cH²r/2, JS0=0. Isotropic homogeneous mean F0=Zdot0−HV0 obeys

24cHF0+cH²r/2=0,
24c(Fdot0+3HF0)+cH²r/2=0.

They have the consistent solution F0=−Hr/48. For example mean proper-time choice V0=0 gives Z0=r/96 plus a constant; this is distinct from the original relative first-order frozen scalar.

Retain a common homogeneous tracefree spatial jet Q through X=2Z+2Q/3±u, Y=2Z−Q/3∓u. Its quadratic kinetic is c(1−η)Qdot²/3. Direct raw variation gives JQ0=2c(1−η)H²r/3. Thus

Qddot+3HQdot=H²r,
Qdot=Hr+C a^−3,

is a regular solution, including the shear deformation's own source. Homogeneous clock relabeling leaves no new constraint on this solution. No second-order effective cold density or gauge-invariant expansion is inferred from these coordinate mean fields.

## 5. Exact remaining relative regularity implication

Exchange symmetry removes smooth analytic cubic pure-relative terms, but it does NOT remove the even norm-cube. In the inherited normalization,

S3,norm=−K/(6a0)∫dt d³x |∇coord u|³,
Jν,norm=+K/(2a0)div[|∇u|∇u].

For a plane u=vcos(kx), this is −K k³v|v| |sin(kx)|cos(kx)/a0, continuous and Lipschitz but not C1 at the nodes. Its amplitude is ε|ε|. The quadratic relative source cannot be declared zero from exchange evenness, and a generic C3 implicit-function theorem is inapplicable.

For a relative harmonic the actual constrained shear action has Arel=−3(1−η)/η<0 and, with source Jν,

Lrel=c[−Arel(zdot−Hν)²+P(ν+z)²]+Jνν,
ν=[Arel H zdot+Pz+Jν/(2c)]/[Arel H²−P].

The retained shift and shear-volume rows are unchanged by this leading relative source. Kr=Arel P/(Arel H²−P)>0 on every finite harmonic; the forced reduced action includes Jν(Arel H zdot+Pz)/(Arel H²−P). Finite-time ODE solvability harmonic by harmonic does not establish uniform spatial regularity: Kr tends to a constant at high P, rather than furnishing a restoring spatial gradient. The resulting metric, curvature and possible prepared data cancellations need a physical regularity audit. This child proves the common-sector admission through order ε², not the whole smooth family.

## 6. Reproducibility and non-claims

checks.py constructs the raw plane ADM densities before variation, derives the source rows, confirms the orthogonal clock identity, and substitutes the explicit fields into every sourced mean row. Separate zero-mode and tracefree jets prevent replacing their equations by a nonzero-mode limit. The controls erase the added shear source, freeze the auxiliary lapse source, or use raw clock forcing with a previously homogeneous-eliminated operator. Finite symbolic checks corroborate the displayed analytic proof; they do not prove nonlinear existence.

The parent action/report and source inputs remain frozen. No photon kinetics, radiation perturbations, observational fit, full nonlinear initial-value theorem, physical negative-energy claim, cold abundance or 32π selection follows. Next: audit the actual relative norm-cube force's metric/curvature regularity and compatible data, or construct a physically motivated smoother source completion with its changed MOND implications stated.
