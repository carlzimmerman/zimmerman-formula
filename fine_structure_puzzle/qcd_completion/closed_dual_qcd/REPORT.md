# Closed deformed-QCD ensemble: controlled leading result

The physical fine-structure target remains open. This route computes the complete tree plus Gaussian contribution of the monopole/dual-photon EFT on **closed S3_R x S1_L**, with small L fixed, and obtains a zero coefficient of 1/R in its bulk-subtracted spatial stress at fixed matched local fugacity. It also computes the response to an unspecified 1/R shift in the matching coefficients. This is partial progress in center-stabilized pure SU2 gauge theory, not physical QCD or electromagnetic-alpha dependence.

## The ensemble and its global measure

Start from the authenticated [Unsal–Yaffe exact v2 primary paper](https://arxiv.org/abs/0803.0344v2), with its full flat-space monopole prefactor retained symbolically. Let f denote the weight of **each signed event**. Summing both species and both antiparticles gives

    S = integral_S3 sqrt(g) [kappa/2 (d phi)²
                              -4f cos(theta/2) cos(phi)],
    kappa=g²/(8pi²L),  mW=pi/L.

Its UV-regulated compact functional integral enforces exact magnetic neutrality. Each species then has the same net event number Q, so total topological charge is integer Q. The uniform-sector sum is exactly

    I0(4fV cos(theta/2)) = sum_(Q in Z) I_Q(2fV)² exp(i Q theta),
    V=2pi²R³.

It is smooth and 2pi periodic at finite V; at large V the stable theta branch minimizes -4f cos[(theta+2pi k)/2], k=0,1. The massive-saddle calculation excludes theta=pi mod 2pi, where the retained order-f potential vanishes. The exact uniform-sector integral is not substituted for the interacting gas.

For the canonical field sqrt(kappa) phi, the orthonormal constant coefficient is sqrt(kappa V) phi0. Thus normalized compact Haar measure must be multiplied by

    J0=p mu sqrt(2pi kappa V).

Here p is the finite number of identical compact cells (p=2 in the root-cell description); it is metric independent. At a stable saddle, with u=4f|cos(theta/2)| and m²=u/kappa,

    J0 I0(uV) ~ p (mu/m) exp(uV).

This cancels the apparent +1/(2V) metric term from normalized Haar measure alone. The constant eigenvalue is m², and is included once in the all-mode determinant. The full partition remains **N_hard[g,L] times this canonical EFT partition**. Neither the Jacobian nor theta derivatives determine N_hard.

There is a source-convention issue worth preserving: the exact PDF assigns zeta per signed event in (3.22), but its cosine in (3.25) lacks the corresponding factor two. Equation (3.29) prints an imaginary theta argument inconsistent with its phase weights; appendix (A.6) also prints a deformation sign inconsistent with the main fugacity suppression. These are confirmed in actual PDF pixels, physical pages 19, 20 and 27. This calculation fixes all event coefficients by expansion and does not use the source's printed mass eigenvalue normalization. See `SOURCES.json` and immutable `DERIVATION.md`.

## Actual determinant and spatial stress

At fixed u,kappa and mR>>1, the leading weak-plasma partition is

    Z_EFT = p exp(uV) det[(-Delta_S3+m²)/mu²]^-1/2

at Gaussian order. The spectrum is P_n=(n²+a²)/R², degeneracy n², a=sqrt((mR)²-1), n>=1. A common zeta/proper-time finite-part scheme gives

    W_m=-pi a³/6+pi integral_a^infinity t²/(exp(2pi t)-1) dt.

This includes the compact constant mode. Flat bulk matching subtracts -Vm³/(12pi). Define the spatial response by varying the sphere metric at fixed L and fixed matched coefficients:

    tau_s=(1/L) d_V W.

The exact retained correction for mR>1 is

    Delta tau_s = m³/(12pi L)
      [1-sqrt(1-(mR)^-2) coth(pi sqrt((mR)²-1))]
      = m/(24pi L R²)+1/(96pi L mR^4)+... .

Therefore **lim_(R->infinity) R Delta tau_s=0** for the stated tree plus Gaussian compact ensemble. This follows analytically from the determinant; finite grid agreement is only a check. The order-f contact/vacuum term -uV is present and cancels its own flat subtraction when u is radius independent.

The effective-action density differs: Delta W/(LV)=m/(8pi L R²)+..., three times the leading spatial metric response. The temporal Euclidean response is (1/V) partial_L W and involves partial_L m²; its determinant correction is (partial_L m²)m[1-sqrt(1-(mR)^-2)coth(pi sqrt((mR)²-1))]/(8pi), also starting at R^-2. The anisotropic product geometry does not by itself specify a Lorentzian vacuum-energy observable.

The normalized monopole-gas partition divides out the compact free-photon/scalar partition. Its global canonical normalization gives W_0=-(1/2)log(kappa R)+constant, so that normalized gas has an extra +1/(6LV) in spatial response. Restoring the perturbative partition removes it. Neither convention produces 1/R. Local analytic gravitational matching terms can change the R^-2 and higher even-power coefficients; their values are not computed here.

## Independent Coulomb cancellation and its limit

The exact mean-zero S3 Green kernel is

    G_R(chi)=[(pi-chi)cot(chi)-1/2]/(4pi²R),  chi=d/R.

Its fixed-separation expansion has constant regular part -3/(8pi²R). Including the same regular self energies and pair terms gives

    delta S_(1/R)=-3(sum q_e)²/(16pi²kappa R)=0

for every neutral finite configuration. A single self-energy correction would miss that cancellation. The expansion is not uniform at separations of order R and is not promoted to an all-orders thermodynamic proof. `CLOSED_GREEN.md` gives the derivation; the massive determinant independently performs the leading screening resummation.

## Where an unknown matching coefficient would enter

Allow hypothetical f_R=f0+f1/R+... and kappa_R=kappa0+kappa1/R+..., writing u_i=4|cos(theta/2)|f_i and m0²=u0/kappa0. At the computed tree plus one-loop order, the local density -u-m³/(12pi) gives

    C1= -[1+m0/(8pi kappa0)]u1 + m0³ kappa1/(8pi kappa0),
    Delta[W/(LV)]=C1/(LR)+...,
    Delta tau_s=2C1/(3LR)+...,
    Delta tau_L=(partial_L C1)/R+... .

These are sensitivities to unknown input coefficients, not assigned values. A matching factor with W_hard proportional to R² would add another such coefficient. Local hard matching analytic in the closed-sphere curvature generates even inverse powers of R; deriving that locality and the full common-regulator core/gauge/global normalization is the first unresolved gauge-theory arrow. An isolated ball zero-mode norm does not supply it.

## Executed evidence and scope

Base FSP-003 inputs and source PDF/text/pixel hashes are pinned in `INPUTS_001.json`. No original scientific input or executed script was edited. This lane made no Git mutation; concurrent repository work changed HEAD, so content hashes define ancestry.

- `runs/closed-002`: **completed**, 1.477316 seconds. It passed 91 checks at each of 60 and 85 decimal digits. The worst scaled check residual was 4.423e-45 at 60 digits and 2.251e-60 at 85 digits, below the declared 1e-40 tolerance. Checks cover compact quadrature/Bessel/topology sums, analytic topology tails, direct/Poisson heat traces, winding integral/polylog identity, an independently summed mass Hessian with bounded tail, metric differentiation, canonical zero-mode cancellation, and matching-shift chain rule.
- Scientific output tables retain 45 significant digits. The script's tiny cross-precision serialized-table error is limited by that serialization and is not advertised as 92-digit accuracy. There is no interval certification.
- `runs/green-003`: **completed**, 0.547307 seconds. Exact symbolic checks verify the radial equation, antipodal regularity and local series; 60/85-digit quadrature checks the zero mean; six finite neutral configurations check self/pair cancellation. The general cancellation follows from (sum q)², not enumeration alone.
- `runs/closed-001`: preserved **launch-failed** record, `preexec_fn` exception with a memory cap. Before it, an affinity-capped invocation was rejected in preflight because macOS lacks that API; no run directory or scientific execution was created for that preflight rejection. The successful fresh run retained CPU, wall-time, thread and log caps, with no unsupported memory/affinity promise.

All three v2 manifests validate with current input hashes. Finite test parameters are dimensionless checks, not independently matched physical couplings. The proof audit is a self-review; an independent derivation has not yet been returned to this lane. See `AUDIT.md`, `REPRODUCE.md`, and the hash receipt.

The next executable step is a common-regulator gauge-to-dual matching computation on the closed product geometry, retaining the full monopole-core determinant, gauge/global factors and curvature terms. This route remains open at that matching arrow. The small-circle-to-strong-QCD, state/geometry, QED and proton-mass arrows remain separate.
