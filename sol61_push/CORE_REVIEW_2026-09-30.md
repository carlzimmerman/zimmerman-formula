# Core-theory review and forward calculations — 2026-09-30

**The repository has several distinct candidate theories; no reviewed core derives 32pi or closes every required physical gate.** The strongest executable new result is an exact point-source solution for the declared nonlocal polarization model. A second route generates the needed cubic response in an isotropic three-dimensional spectral toy. Both expose additional assumptions rather than solving the vacuum coefficient.

Base checkpoint `ec25883ef`. Scope: selected theory/action documents, their declared equations, the CFG43 source action, the later FP0/chain conventions, and independent calculations described below. This is not a rerun or line-by-line review of the entire repository. Source hashes are in `runs/core_coefficient_audit/results.json`. Other sessions' files remain untouched.

## 1. Which core is actually being used?

| Core | What its own record establishes or declares | What remains missing |
|---|---|---|
| Historical expansion-based AeST spine (`real_research/FOUNDATIONS.md`, `THE_SURVIVING_THEORY.md`) | Declares a0=kappa sqrt(G rho_total), equivalently proportional to H; coefficient explicitly posited | A different scale law from the later vacuum-based chain; full health was open in this record |
| Later FP derivation chain (`real_research/derivation_chain_2026/README.md`, `FP0_core_postulates.py`) | Declares a0=kappa sqrt(G rho_DE), P2 in the infrared, and kappa=1/2 fitted; realizes a tie via an HT multiplier | Declared coupling, cosmological separator and dark-matter metric coupling still have action/observational obligations |
| Fable September 8 action (`fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md`) | Provides a clock/scalar action and discusses local health on its operative branch; explicitly labels kappa fitted and CMB dark component missing | A galaxy limit or local sign check is not the missing cosmological dark sector |
| Qwen/MMG August consolidation (`qwen_claude_field_theory/FINAL_THEORY_MMG_CONSOLIDATED_2026-08-27.md`) | Carries an explicit same-day retraction notice for its earlier “conditionally closed” assessment | Its reported matter-conservation and PPN defects prevent using the superseded closure claim |
| Candidate B and closure map (`campaign_fresh_gravity/closure_map/README.md`) | An effective galaxy law, ownership rules and cold component; no committed common action was established by the map | Dynamical selection of the baryon-conditioned density and a legal ownership mechanism |
| CFG43 HT fluid tie (`campaign_fresh_gravity/CFG43_fluid_tie/A1_action_field_equations_dof.py`) | A conserved fluid's cap can depend on the same integration constant as the cosmological term | Entry form and cap coefficient are postulated; this does not produce the required galaxy fluid density |
| Flowing-vacuum door 11 (`closure_map/DOOR11_RESULT_2026-09-29.md`) | Records failures within declared directional/timelike/inflow classes and a pending region-gate branch | Does not prove every field-mediated stream impossible; successful imposed kernels are restatements |
| Ten-dimensional formal action (`real_research/papers/v12_FORMAL_CORE_action.md`) | Explicitly calls its volume modulus value Z²=32pi/3 an input | Dimensional reduction with that modulus does not select it |

Health/observational verdicts in this table are documentary findings from the specified records, not independently reproduced numerical exclusions. They must not be transferred between actions. The new audit independently reproduces only the convention identities and CFG43 constitutive calculation below.

For c=1 and Lambda=8pi G rho_vac, the vacuum-based convention gives

    Lambda/a0² = 8pi/kappa².

Setting kappa=1/2 makes this 32pi as an identity. In the H-based convention the same ratio is instead 8pi Omega_DE/kappa². At kappa=1/2 it is 32pi Omega_DE, equaling the target only in a vacuum-dominated de Sitter limit. These alternatives were already distinguished in the later FP0 record; this review confirms the distinction rather than announcing a newly discovered inconsistency.

Likewise P2 is g=sqrt(b²+a0 b), whereas the “simple” law is g=(b+sqrt(b²+4a0 b))/2. They differ at b=a0 and have high-field residuals a0/2 and a0, respectively. The door-11 gate document already carries an erratum correcting its initial kernel label. An implementation or citation must retain that correction. Neither infrared kernel is automatically Solar-System-safe.

## 2. Directly audit the core's proposed coefficient tie

Let Mp²=1/(8pi G), x=mn/(nu_s Mp² Lambda), and use CFG43's declared EOS

    rho = mn + epsilon Mp² Lambda x atan x.

Independent differentiation gives

    P = n rho_n-rho = epsilon Mp² Lambda x²/(1+x²),
    rho_Lambda|n = -P/Lambda,
    P_cap = epsilon Mp² Lambda.

Its response dictionary a0²=P_cap/Mp² therefore gives Lambda/a0²=1/epsilon. The desired value requires epsilon=1/(32pi). The HT clock equation changes its divergence to absorb rho_Lambda; the T variation keeps Lambda spacetime-constant. Neither is an equation fixing epsilon. No additional clock-boundary constraint has been specified in this test.

Can ordinary fluid characteristic conditions select epsilon? No, for this EOS. For x>0, epsilon>0 and nu_s>0, rho_n>0 and

    c_s² = n rho_nn/rho_n
         = 2epsilon x / [nu_s(1+x²)²
                         +epsilon((1+x²)² atan x+x(1+x²))].

The denominator exceeds the numerator. A useful exact proof is to define B(x)=atan x+x(x²-1)/(1+x²)²: B(0)=0 and B'=8x²/(1+x²)³>0. Thus 0<c_s²<1 for every positive epsilon, not just its target value. The tested cap strengths corresponding to 16pi, 32pi and 64pi all satisfy these local fluid conditions. This is not a full gravitational perturbation/constraint proof or a galaxy-selection mechanism. It proves that these particular conditions leave the coefficient undetermined.

## 3. Carry the nonlocal response into an actual force solution

The previous round found a massless spatial kernel; merely reporting its size did not solve the resulting force equation. Here declare the **phenomenological isotropic three-dimensional** functional

    W = |g|²/2 - g dot p + |p|²/2 + alpha|p|³
        + (beta/2) p dot |grad|p,
    g = grad Phi,   a0 = 1/(3alpha),   alpha,beta > 0.

The equations are

    g = p + 3alpha|p|p + beta|grad|p,
    div(g-p) = 4pi G rho_b.

This three-dimensional operator is not automatically the determinant of a collection of two-dimensional fermion sheets. For an ideal point source and r>0, set p=A grad(log r)=A rhat/r. With Fourier inverse measure d³k/(2pi)³,

    F[1/r²]=2pi²/|k|,
    |grad|log r = -pi/(2r),
    |grad|p = pi A rhat/(2r²).

An additive constant/distribution at zero momentum in log r does not change p. Regulated oscillatory Fourier quadratures independently check the pi/2 coefficient. The exact solution is

    A²/a0 + (pi beta/2) A = GM,
    A = 2GM / [pi beta/2 + sqrt((pi beta/2)²+4GM/a0)],
    g(r) = GM/r² + A/r.

The baryonic source flux is exactly 4pi GM. The far-field circular speed has v²=A. Large M gives A approximately sqrt(GM a0), recovering the MOND velocity–mass limit. Small M gives A approximately 2GM/(pi beta), yielding a mass-versus-speed slope of two instead of four.

More precisely,

    d log A/d log M = (A/a0+pi beta/2)/(2A/a0+pi beta/2),
    d log M/d log v = 2 / (d log A/d log M),

so the latter slope lies strictly between two and four for finite positive beta. The acceleration scale inferred from v⁴/(GM) is

    a0_inferred/a0 = (sqrt(1+eta²)-eta)²,
    eta = pi beta sqrt(a0)/(4sqrt(GM)).

This is an explicit falsifiable mass dependence, not the desired exact universal law. The scale-invariant point-source solution has logarithmically divergent polarization/cubic energy and requires IR/UV completion. Introducing finite boundaries changes a nonlocal operator globally; this ideal branch is not a finite-energy galaxy solution. Its all-radius interpolation also does not inherit P2's or any other kernel's observational checks.

Under the earlier *conditional massless sheet dictionary*, beta a0=pi/(4y), giving eta=pi²/[16y sqrt(GM a0)]. But the fermion mass is m=y|p|. The massless operator is appropriate only in the regime where spatial momentum is not small relative to that gap; the finite-mass kernel from the previous round must replace it elsewhere. The exact equation solved here is a declared static model, not a controlled use of the massless approximation at every M.

## 4. Try generating the cubic term in an isotropic bulk

A separate calculation removes the sheet-dimension assumption at the cost of a new nonlocal spectral assumption. For occupied fermion bands with

    E(k,m)=sqrt(k³/mu+m²),   mu>0,

the massless dispersion exponent is z=3/2. In three spatial dimensions, the energy scales as |m|^(1+3/z)=|m|³. Transforming t=k^(3/2)/sqrt(mu) gives k²dk=(2mu/3)t dt. After subtracting the massless energy and its analytic quadratic divergence, the finite energy density is

    E_ren = +nu mu |m|³/(9pi²).

Nine direct integrals in physical momentum verify the regulated expression independently of the substitution. Ordinary relativistic bulk modes with z=1 instead have fourth-power scaling (with the familiar logarithmic renormalization issue); the fractional spectrum is a substantive additional assumption.

If m=y|p| and the static normalization is 4pi G, this toy gives

    alpha = 4G nu mu y³/(9pi),
    a0 = 3pi/(4G nu mu y³).

It supplies the desired cubic sign and power without planes. It does not select z, mu, y or the critical quadratic counterterm. The spectrum has a nonanalytic spatial operator and group velocity growing without bound in the ultraviolet as written. A causal UV completion remains uncomputed. The massless spatial kernel is calculated next; the finite-mass and nonuniform kernels remain open. There is no claim that this is a viable covariant theory.

The absolute vacuum constant remains free. Matching the original target would require rho_vac=9pi²/(4G³ mu² nu² y⁶), an added relation. No subtraction convention is promoted to a physical prediction of that density.

## 5. Compute the bulk spatial kernel rather than importing the sheet result

An explicit eight-band Hamiltonian uses six anticommuting Hermitian matrices: three momentum matrices with coefficients k_i sqrt(|k|/mu), and three polarization mass matrices with coefficients y p_i. Their Clifford algebra gives E²=k³/mu+y²|p|² and four occupied negative-energy bands per flavor. This is still a nonlocal spatial spectral toy, not a causal covariant action.

For the static massless two-point function, integrate frequency exactly and subtract the zero-momentum curvature symmetrically. Writing E=k^(3/2)/sqrt(mu), E'=|k+q|^(3/2)/sqrt(mu), and c=khat dot (k+q)hat, the remaining integral is

    DeltaPi(q) = (8y²/2) integral d³k/(2pi)³
                [(1/E+1/E')/2 - (1+c)/(E+E')].

Its integrand equals [(E-E')²+2EE'(1-c)]/[2EE'(E+E')], which is nonnegative. Momentum rescaling gives the exact power

    DeltaPi(q) = C8 y² sqrt(mu) |q|^(3/2).

For the declared eight-band model the bounded quadrature estimate is C8 approximately 0.20510. The last 1024-to-2048 refinement changes it by 5.28e-5 relatively, below the predeclared 1e-4 criterion. Independent q=0.5 and q=2 integrations satisfy the stated scaling tolerance. This is a finite numerical estimate, not a certified exact value or a 32pi selection.

The first calculation failed two declared checks (12/14): the linear radial map left a slowly converging ultraviolet tail. A squared radial map and a stable logarithmic ratio improved this, but its next run still failed the 1e-4 refinement criterion (13/14). Raising the final resolution to 2048 then passed 14/14 without relaxing either tolerance. All three scripts, contracts and raw runs are retained. Integrable massless singularities still limit convergence; adjacent-resolution agreement is not a rigorous error bound.

This changes the spatial discriminator. In the sheet model, m times r is constant along p=A/r. In this bulk spectrum the ratio of characteristic momentum energy to the local mass gap is

    E_(1/r)/(y|p|) = 1/[y A sqrt(mu r)],

which tends to zero at large r. Thus the gap hierarchy improves toward the far field instead of remaining fixed. The massless |q|^(3/2) correction would scale as r^(-5/2) on a scale-free p profile, faster than the local cubic r^(-2) term. In the actual massive regime one must replace the massless kernel. If its leading analytic derivative term is q², dimensional scaling fixes its coefficient to be proportional to mu^(1/3) m^(-1/3); it would also decay faster than the cubic term along that profile. **That finite-mass coefficient and the nonuniform equation have not been computed**, so this is a reason to investigate the route, not proof of a galaxy solution.

## 6. Evidence, correction and the next hard calculation

Current evidence consists of four principal bounded runs:

- `runs/core_coefficient_audit`: 18/18 checks, plus hashes of the selected reviewed sources.
- `runs/nonlocal_point_source`: 23/23 checks, including independent Fourier quadrature and mass-slope bounds.
- `runs/bulk_cubic_spectrum`: 17/17 checks, including nine direct physical-momentum integrals.
- `runs/bulk_spatial_kernel_converged`: 14/14 checks at the final declared resolutions; the two preceding failed kernel runs are retained separately.

That is **72 principal checks**, not independent confirmation of the theory. An initial nonlocal run is retained separately as `runs/core_nonlocal_solution` (21/21): its check label incorrectly says the velocity–mass slope “exceeds MOND four,” although the checked algebraic expression was correct. The corrected script `nonlocal_point_source.py` fixes the label and explicitly proves that the slope lies below four and above two. The original script/run are retained unchanged for provenance; their misleading label must not be quoted as a physical conclusion.

The core review favors a field-mediated response as the next executable investigation, while retaining the distinction between a through-stream intuition and the required equations. The next important discriminator is the finite-mass, nonuniform spatial response of the isotropic bulk cubic generator, together with a mechanism protecting quadratic cancellation. A completed route must then compute its cosmological vacuum stress with the same action and state. The 32pi target has not been derived; neither repeated coefficient identities nor replacing one free scale by another closes it.
