# AZ30: weak-curvature scalar derivative gate survives; cutoff not derived

κ = ½ FITTED; not theory closed

**PASS** for the retained scalar derivative block in the stated domain; **FAIL** to derive a physical cutoff from AZ28 alone; **NOT EVALUABLE** for the actual effective-theory validity window; **NO VERDICT** for complete curved scalar stability. Both footings receive these separate grades. Physical κ remains NOT EVALUABLE and no full requirement/RQ3 row is earned. Criteria commit a1187d176b.

This is a cheap exact expansion and sign test. No galaxy simulation, numerical spectrum, parameter scan or chosen cutoff was used. It does not repair AZ29's unrestricted high-curvature failure.

## 1. What the action says about a cutoff

The coefficient ell² defines a dimensional crossover at spatial momentum of order 1/ell. It does not by itself identify a mass threshold, a UV completion, a strong-coupling scale or the error of truncating the action. The inequality ell²|R| much less than one is a formal derivative-expansion condition, not an independently derived numerical cutoff.

For example, the allowed omitted curvature term c3 ell^4 R³ has magnitude relative to the retained ell²R² term equal to |c3|ell²|R|. The action supplies no c3 or bound on it. Other spatial-curvature invariants and higher-derivative terms also require coefficients. Assuming these are order unity would be an additional power-counting assumption, not a result. If AZ28 is treated instead as the exact action at all scales, the AZ29 curved instability applies and there is no justified cutoff that removes it.

Thus one can write a conditional weak-curvature regime without tuning a numerical boundary, but cannot certify its physical range from the present inputs. This is a missing matching/UV input, not a proof that every microscopic completion is impossible.

## 2. Exact scalar spatial derivative expansion

Take closed FRW spatial slices with reference curvature R=6/a², scalar metric gamma_ij=exp(2zeta) bargamma_ij and lapse N=1+n. The exact conformal identity is

    R[gamma]=exp(−2zeta)[R−4 barDelta zeta−2|barD zeta|²].

Expanding N sqrt(gamma)(R[gamma]−ell²R[gamma]²), integrating spatial boundaries, and considering a harmonic with −barDelta=X gives the quadratic derivative terms

    [(2+12ell²R)X−16ell²X²] zeta²
       +4(1−2ell²R)X n zeta.

The acceleration action adds 2X n² because its zero-gradient Hessian is 2. The 12ell²R term must be retained: replacing the Einstein coefficient by V_R alone misses a conformal-curvature cross term. The script records the remaining zero-spatial-derivative terms rather than pretending they vanish.

On a constant-curvature slice, the shift contraction identity is

    integral |D_i D_j chi|²
      =integral (Delta chi)²−(R/3)integral |D chi|².

Consequently the derivative-order temporal/shift bracket, with beta=Delta chi and S=3lambda−1, is

    −3S zetadot²+2S zetadot beta
       +(1−lambda−R/(3X))beta².

Here beta is a shift variable, not normalization b. Eliminating this block's shift and the derivative-order lapse gives

    beta=S zetadot/[lambda−1+R/(3X)],
    n=−(1−2ell²R)zeta,
    C_R=(3lambda−1)(2−R/X)/[lambda−1+R/(3X)],
    L_derivative=C_R zetadot²−P_R zeta²,
    P_R=16ell²X²+(−20ell²R+8ell^4R²)X.

These equations describe the **retained derivative block**, not the exact lapse or shift of the full evolving background. In particular, Hn terms, background temporal boundaries, matter perturbations, cosmological-constant terms and zero-derivative curvature pieces have not been included in this reduction. They can change low-frequency behavior. They can also contribute to subleading coefficients in a full large-X expansion; the displayed P_R is not advertised as the complete curved dispersion relation.

## 3. Positivity and its useful scope

For closed scalar harmonics X=l(l+2)/a²=R l(l+2)/6. For the l>=2 sector, X>=4R/3. Homogeneous and exceptional l=1 sectors require separate constraint/gauge treatment and are not graded here. With lambda>1,

    2−R/X>=5/4>0,
    lambda−1+R/(3X)>0,
    P_R=ell²X[16X−20R+8ell²R²]
       >=ell²X[4R/3+8ell²R²]>0.

Thus C_R and P_R are positive on that sector for R>0. At R=0 the result continuously recovers AZ28's positive C and 16ell²X² stabilizer. The scalar derivative block therefore does not exhibit an additional wrong-sign obstruction in weak positive curvature. The tensor test still separately requires ell²R<1/2.

This positivity does not pass the full low-harmonic scalar problem: at X of order R and ell²R small, the retained restoring term is of order ell²R², while omitted zero-derivative terms can be of order R. They need not be small. Nor does this calculation classify ordinary matter growth versus a gravitational-field instability.

For a genuinely short-wavelength conditional test, let M_bg² bound R,H²,|Hdot|,rho/B,Lambda and the other background scales with fixed finite couplings. A sufficient formal hierarchy is

    X >> M_bg²,
    ell²X² >> M_bg²,
    ell²X << 1.

The first two inequalities suppress omitted background effects relative to the leading retained kinetic and k^4 terms. The last is a hypothetical derivative-expansion condition, not a measured cutoff. Such an interval can exist parametrically when ell²M_bg² is small, assuming controlled omitted coefficients. Neither that coefficient control nor the actual physical UV scale is supplied here. We therefore do not claim that an observed galaxy or cosmic background lies in a certified window.

## 4. Decision before simulations

The cheap scalar derivative gate **survives conditionally**. It does not justify a numerical cutoff or a fully stable effective theory. The next useful input is a microscopic matching calculation or independently motivated power counting that bounds the omitted operators and specifies the validity window. With that in hand, derive the complete curved scalar/matter quadratic action and its actual time-dependent constraints in that window before running galaxies. If the exact untruncated AZ28 theory is the intended object, its already established high-curvature failure remains.

No step here constrains the force width A or relates it to the vacuum scale. The physical b=1 and κ=1/2 goals remain open.

## Evidence

`results.json`: **18/18 checks**. Exact conformal expansion, retained/remainder separation, curved constraint elimination, flat known answers and analytic positivity reparameterizations verify. The missing-curvature-cross-term mutation disagrees with the original expansion. Lean verifies two finite bounds and rejects the false negative-bound control; it is not a certificate of the full scalar PDE or physical κ. Interval reasoning and scope are self-reviewed. All numerical margins are exact algebraic controls, not observational significance.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ30_weak_curvature_scalar/run.py`. Inputs and versions are hashed. A,lambda,ell,Lambda,B, boundary data and omitted-operator coefficients remain unselected/FITTED if assigned. No new data, species, cold component, heavy computation or push.
