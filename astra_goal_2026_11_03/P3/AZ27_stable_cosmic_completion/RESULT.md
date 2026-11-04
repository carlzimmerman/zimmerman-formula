# AZ27: cosmic gradient repair with an unfixed width and a nonlinear fold

κ = ½ FITTED; not theory closed

**PASS** for removal of AZ26's cosmic high-frequency gradient instability in the declared family; **FAIL** for uniform nonlinear momentum invertibility and width selection; **NO VERDICT** for complete nonlinear stability; **NOT EVALUABLE** for physical κ. Canonical and alt have the same separate grades. Zero full requirement/RQ3 rows established. Criteria commit 48b7492c0a.

This is an explicit constitutive repair, not a derived microscopic mechanism. Opposite-side deformations already occur in the record. The new result here is a complete cosmic-side function with all-density principal sign bounds, exact homogeneous evolution, and a nonlinear fold calculation. No width is tuned and no claim of literature novelty is made.

## 1. Construct the cosmic side from the stability inequalities

Retain I=(-C2 K²+C1 g²)/m² and the inherited source cusp at I>=I0. Set I0=-J0<0, J0=9C2 H0²/m². On I<I0 define z=I/I0>1 and

    F'(I)=2 z^(-p)/C1,       0<p<1/2,
    F(I)=F0−(2J0/C1)[z^(1−p)−1]/(1−p),
    F0=−4J0/C1−6H0²/m².

F and F' match the source-side cusp at I0 for every A>0. The source width remains xa=C1 A²/m². The cosmic-side exponent p is also unselected; stability restricts it to an open interval, not a distinguished number.

The choice follows a concrete stability condition. With alpha=C1 F', Q=F'+2I F'', lambda=1+C2 Q, the healthy cosmic scalar principal region lambda>1, 0<alpha<2 requires a decreasing positive F' as |I| grows, but not so rapidly that Q changes sign. This power family gives

    alpha=2 z^(-p) in (0,2),
    Q=(1−2p)F'>0,
    lambda>1.

After eliminating lapse and shift as in AZ26,

    C=2(3lambda−1)/(lambda−1)>0,
    c_s²=(z^p−1)(lambda−1)/(3lambda−1)>0.

These inequalities hold for every z>1, every 0<p<1/2 and every positive width A. Thus this repair removes the specific cosmic gradient sign failure found in AZ26; that failure was not inevitable for all opposite-side completions. This is a principal-symbol statement, not an all-wavelength or nonlinear stability theorem.

## 2. Exact cosmic matter evolution

For conserved homogeneous baryonic dust let r=ρ/B. The original lapse equation gives

    H²=H0² z,
    r(z)=3H0²(z−1)
          +(m²J0/C1)[(1−2p)/(1−p)](z^(1−p)−1),
    r'(z)=3H0²+(m²J0/C1)(1−2p)z^(-p)>0.

The density ranges monotonically from zero at z=1 to infinity. Every positive density has one homogeneous state. Conservation fixes

    zdot=−3H0 sqrt(z) r(z)/r'(z)<0.

For finite initial density, H>=H0 and r decays at least as exp(−3H0 t). Monotonic inversion therefore yields z→1 and H→H0 in the future. Unlike AZ25's singular negative-side choice, the first cosmological response is linear:

    H²−H0² = (ρ/B)/[3+9(C2/C1)(1−2p)] + O((ρ/B)²).

No observed expansion history has been used or fitted. These formulae make predictions to be tested, not an observational pass. They also show that A does not enter this entire homogeneous evolution or its stability inequalities.

At the cusp c_s² tends to zero. The scalar kinetic coefficient approaches

    C_left=6+2C1/[C2(1−2p)],

whereas the inherited singular source-side homogeneous limit has C_right=6. F and F' are continuous but their next derivatives are not. A complete crossing problem must treat that degeneracy and coefficient change; the cosmic-side sign cure does not resolve it by itself.

## 3. Nonlinear inhomogeneous momentum constraint

The AZ24 constraint involves F'(I)K. Holding the acceleration g fixed, its exact local Jacobian is

    d(F'K)/dK = F' [1−2p C2 K²/(C2 K²−C1 g²)].

It vanishes at

    C1 g²=(1−2p)C2 K²,
    I_fold=−2p C2 K²/m².

The fold lies strictly inside the cosmic branch whenever K²>K0²/(2p). It exists for every allowed p and for every source width A. The dimensionless check p=1/4, C1=C2=m=J0=1, K=2, g²=2 gives I=-2<I0=-1 and zero Jacobian. These are exact algebra-control values, not a physical fit.

Consequently the constraint inversion is not uniformly regular on all left-branch field configurations. This does **not** prove that every physical galaxy reaches the fold, or that a different formulation cannot continue a constrained solution through it. It prevents a claim that the completed nonlinear evolution is already globally stable or uniquely invertible.

A broader local reason explains this tradeoff within a single F(I). If a continuous match has F'(I0)=2/C1 but a stable cosmic interval has F'<2/C1 to its left, F'' must be positive somewhere on that interval. At a fixed such I<0,

    d(F'K)/dK = F'−(2C2 K²/m²)F''.

Increasing K² while increasing g² to retain the same I eventually makes this Jacobian negative. The sign change, if the homogeneous value is positive, forces a fold. This argument concerns unrestricted algebraic field configurations in the single-invariant ansatz, not the existence of fully constrained matter solutions at every such configuration and not a no-go for actions with other invariants.

## 4. What this says about the requested coefficient

The cosmic gradient instability can be repaired without assigning the source width. That repair is allowed for a continuous set of p and **every A>0**. No condition derived here selects A/H0, hence none selects

    b_conditional=(H0/(2A))sqrt(3/(8pi)),
    κ_conditional=(A/H0)sqrt(8pi/3)=1/(2b_conditional).

These remain conditional source/vacuum dictionaries; a full galaxy force calibration is absent. Selecting a preferred p or adding a potential centered on a target A would be an extra assumption. The physical origin of the function F is still missing. This lane supplies a mathematical repair of one instability, not a mechanism deriving κ.

Next: a constrained source evolution that either avoids these folds for justified matter data or resolves them within a physically motivated action with additional invariant structure. Its kinetic and gradient terms must be derived before any numerical regularization is interpreted as physics. A second arbitrary constitutive coefficient would not by itself close normalization. No full galaxy simulation or new stable theory is claimed here.

## Evidence

`results.json` records **24/24** checks: integrated action, matching, exact density and conservation, principal signs and controls, endpoint coefficients, nonlinear Jacobian and an interior fold witness. The p>1/2 mutation gives Q=-1/8 in the finite control and is rejected; Lean verifies three finite identities and rejects the false stability assertion. The interval arguments are self-reviewed analytic proofs supported by symbolic identities, not a Lean certificate of physical κ or the full PDE. Exact algebraic residuals vanish; no observational error bars or acceptance margins are used.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ27_stable_cosmic_completion/run.py`. Input hashes and tool versions are recorded. Free quantities A,p,B,m,C1,C2,H0 and initial/boundary data remain unselected/FITTED if assigned. No new external data, new species, cold component, coefficient scan, heavy run or push.
