# AZ25: nonlinear cosmic attraction does not select the cusp width

κ = ½ FITTED; not theory closed

**PASS** for the homogeneous attractor in the declared completion; **FAIL** for selection of normalization by that attractor; **NO VERDICT** for galaxy evolution and all-mode health; **NOT EVALUABLE** for physical κ. Same separate grades on canonical and alt. No full requirement or RQ3 row established. Criteria commit f8b6e97ec1.

This is a genuinely nonlinear, conserved-matter evolution calculation. It is also an explicitly chosen mathematical completion, not a physically derived branch law. Its purpose is to distinguish attraction to one background from selection of a force normalization. No numerical integration or parameter scan is needed: the constraint can be inverted monotonically for all future times.

## The new model and its exact constraint

Keep the AZ24 action and let I0=−9C2 H0²/m², xa=C1 A²/m², with all C1,C2,H0,A,m,B positive and unselected. Set

    I−I0=xa q|q|,    q>−1,
    F'=2/[C1(1+q)],
    F=F0+(4xa/C1) sign(q)[q−ln(1+q)],
    F0=4I0/C1−6H0²/m².

The value at q=0 is understood by continuity. F and F' match there; F'' diverges. On q>=0 this reproduces the inherited cusp. On q<0 it is a new, declared continuation. It is not uniquely required by the old action or by a symmetry, and no microscopic justification is claimed.

For homogeneous expansion with conserved baryonic dust, q lies in (−1,0), and the invariant fixes

    Y(q)=H²=H0²+(C1 A²/(9C2))q².

Let r=ρ/B. The original lapse equation gives, exactly,

    r(q)=3Y−(m²/2)[2I F'−F]
        =3Y+18C2 Y/[C1(1+q)]+m²F/2.

Its derivative has a useful sign decomposition:

    r'(q)=2C1 A² q/(3C2)+2A² q/(1+q)
          −18C2 Y/[C1(1+q)²] < 0.

Every term is strictly negative on −1<q<0. Also r(0)=0 and r(q) tends to positive infinity as q approaches −1 from above; the positive pole dominates the negative logarithm. Consequently each finite positive density has exactly one homogeneous q on this branch, for **every A>0**.

Dust conservation produces the nonlinear equation

    qdot=−3 sqrt(Y(q)) r(q)/r'(q)>0.

This also satisfies the spatial metric equation

    [2+3C2(F'+2I F'')] Hdot=−r,

which checks compatibility with the original homogeneous gravitational stress, rather than merely fitting a constraint trajectory. The foliation is aligned with the homogeneous time slices. This does not prove well-posedness of inhomogeneous perturbations or health at the singular cusp.

## Exact late-time result

For finite initial density, H0<=H<=sqrt(H0²+C1 A²/(9C2)). Conservation therefore implies

    0<r(t)<=r(t0) exp[−3H0(t−t0)].

The monotonic inverse r↦q exists throughout that future trajectory. It follows that r→0, q→0 and H→H0, without encountering q=−1 or a finite-time density singularity. This proves future attraction in the homogeneous sector for every positive width A, not just one fitted example.

The first asymptotic terms are

    r(q)=−(18C2 H0²/C1)q+O(q²),
    qdot=−3H0 q+O(q²),
    H²−H0²=[C1³ A²/(2916 C2³ H0⁴)](ρ/B)²+o((ρ/B)²).

Thus the same vacuum background attracts a continuum of different widths. **The width remains explicitly in the first nonzero response coefficient.** Cosmic attraction does not make it disappear or select one member of the family. The linear homogeneous susceptibility dH²/dρ at the endpoint is zero; this is a model prediction to be tested, not evidence that the completion is viable. No cosmological observations or acceptance rows were graded.

In particular, A is a parameter in the action, not a dynamical variable with an equation driving it toward a special value. In the conditional MOND/tensor dictionary of AZ24,

    b=(H0/(2A)) sqrt(3/(8pi)),
    κ=(A/H0) sqrt(8pi/3)=1/(2b).

Every A>0 has the same homogeneous attractor, so this attractor alone does not enforce b=1 or κ=1/2. This is **not** a complete counterfamily of observationally viable galaxies, nor a no-go for every possible microscopic selection principle. A subsequent full source solution or health condition could restrict the family, but that has not been demonstrated.

## Verification and disposition

`results.json` records exact symbolic checks of the two-sided derivative, vacuum, original Friedmann and spatial equations, monotonicity decomposition, boundary coverage, nonlinear conservation and late-time coefficients. Known-answer controls recover the vacuum and continuous cusp. The stress MUTATE omits 2I F' and produces the nonzero vacuum residual −18C2 H0²/C1. Lean verifies finite rational coefficient witnesses and rejects the deliberately false width-equality control. It does not certify the full homogeneous theorem or physical κ. The interval monotonicity and convergence argument above is a self-reviewed analytic proof supported by those identities.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ25_nonlinear_cosmic_attractor/run.py`. Input hashes and versions are in the result. No fitted observational numbers, new species, cold component, external data, heavy run or push.

The requested full nonlinear galaxy response remains uncomputed. Its next equations are AZ24's coupled lapse/shift constraints plus metric evolution and conserved matter, now with an explicit two-sided F. The first required test is well-posed branch crossing and constrained kinetic health, not another fitted choice of A. This homogeneous result supplies a rigorous warning for that test: convergence to one H0 is insufficient evidence that the physical normalization has been selected.
