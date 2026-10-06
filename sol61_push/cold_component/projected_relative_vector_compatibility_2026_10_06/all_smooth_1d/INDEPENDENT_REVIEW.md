# Independent audit: all smooth one-dimensional pure-decay profiles

**Primary verdict: proved as written for the smooth periodic pure-decay class.** No nonzero real smooth zero-mean f(x) on the declared periodic torus can satisfy the unchanged projected action's second-order local clock equation by adding a smooth divergence-free relative vector shift. The conclusion permits arbitrary transverse spectrum and time dependence, but excludes additional frozen/homogeneous scalar seeds, different time branches, altered clock operators and genuinely three-dimensional profiles. It is not a global health or abundance theorem.

Pinned REPORT.md SHA256 `38b479d50fab62d7ebdf85502b6ca22ec30b80d2d6710ee2faf291998a4832e7`, checks.py SHA256 `498b396e0fdf8d739472ac7e0fb69c0809fe83a3e04b313f737df99bef5e1899`. The review independently reconstructs the parent current and the entire periodic argument; no author's verdict, imported helper or weighted-sign hypothesis is used as proof. No author scientific inputs changed.

## Raw current and necessary transport sign

The actual inherited Euler density is Etheta,2=2Ka div[(Delta nu) DeltaS+nudot gradnu]. The constrained pure-decay data are nu=f/a, DeltaS_scalar=2H grad u/a, u=(-Delta)^-1 f. Adding a divergence-free V gives, with w=Delta f,

    J=(H/a²)(2w grad u-f grad f)+(w/a)V,
    divJ=-(H/a²)R+(1/a)V·grad w,
    R=div(f grad f-2w grad u).

Thus the sign is V·grad w=(H/a)R. This is a necessary local equation inherited from the unchanged action, not a permission to choose a longitudinal vector or an assertion of full nonlinear vector admission. Enlarging the candidate class to arbitrary smooth divergence-free V is legitimate for a no-rescue conclusion.

For f(x), w=f'' and R=(ff'-2f''u')'. Average over the periodic transverse torus. Since divV=0, partial_x average(Vx)=-average(partial_y Vy+partial_z Vz)=0. Hence average(Vx)=C(t). The local equation implies R=c w', c=aC/H, constant with respect to x. No assumption that V itself is longitudinal or transverse-independent enters this step.

Integrating once gives ff'-2f''u'=c f''+d. Its mean makes d=0: integral ff'=0, integral f''=0 and integral f''u'=-integral f'u''=integral f'f=0. These use periodicity and u''=-f, with no nonzero mean discarded.

Substitution gives u''u'''+2u''''u'+c u''''=0. Setting v=u'+c/2 gives exactly

    2v v'''+v'v''=0.

The plus sign is load-bearing. On either sign component of v,

    (sqrt(|v|)v'')'
      =sqrt(|v|)/(2v) [2v v'''+v'v'']=0.

This identity remains correct on negative components; replacing sqrt(|v|) by an unqualified sqrt(v) would not be legitimate there.

## Independent component/periodic proof

If v has a zero, its nonzero set is a union of connected open arcs with zero at each endpoint, possibly the same point for the circle minus one zero. Continuity gives v->0 at each endpoint and bounded v'' makes sqrt(|v|)v''->0. Its constant value on the component must be zero; v''=0 there. An affine function on that lifted finite arc with both boundary values zero is identically zero, contradicting a nonempty nonzero component. Thus no such component exists and v is identically zero. This does not assume isolated zeros, simple crossings or a finite number of components. Flat and accumulating zero sets are included.

If v has no zero, compact connectedness makes its sign fixed and its magnitude bounded away from zero. The invariant gives v''=c0/sqrt(|v|). Periodicity implies integral v''=0, whereas the right side has fixed strict sign unless c0=0. Therefore c0=0, v''=0 and v is constant. In either case u'=v-c/2 is constant; periodicity forces u'=0 and hence f=-u''=0. The argument works at a single interior time for any value c(t); no time-constant vector average is assumed.

The conclusion follows from the full averaged local equation, not from a sign-definite weighted integral. I independently read the adjacent weighted_sign counterexample: its positive and negative witnesses both fail the necessary zero weighted moment, but preclude a blanket negativity argument. This new proof correctly bypasses that question and covers infinitely supported smooth Fourier profiles.

## Regularity precision and scope

For the stated smooth profiles every step is classical. At the weaker declared u in C4 level, f=-u'' is C2 and w=f'' is continuous, so R and w' need not be pointwise classical derivatives. They should then be interpreted in the original divergence-form Euler equation as distributions. Averaging/integrating that equation gives a continuous integrated identity; its substitution gives the displayed continuous ODE involving u''''. Thus the same component proof extends under that weak interpretation. This regularity explanation is not an author-input change, and is unnecessary for the primary smooth theorem.

The required bounded v'' follows already from periodic C4 u. The theorem does not cover a singular v'' at zero, boundary flux on a nonperiodic interval, rough vector multiplication beyond the weak divergence formulation, extra first-order scalar time branches or an action with a nonzero linear clock Euler operator. In particular the new shear-clock repair changes exactly that last premise and is not ruled out by this old-action theorem.

## Evidence audit and smallest remaining implication

Independently validated all three current standard manifests against current input and output hashes: main_a5/5; control_sign_a3/5, failing only the positive and negative integrating-factor identities after the erroneous sign substitution; control_longitudinal_a5/6, failing only the claim that a varying longitudinal average is constant. Symbolic identities corroborate the differential substitution; the component argument above, not the check count, supplies the uniform proof.

Obligations: inherited current/source convention passed; transverse divergence/torus averaging passed; integration constant passed; ODE sign and both-sign integrating factor passed; zero-component endpoints passed; no-zero periodicity passed; smooth/infinite-spectrum scope passed; current manifest/control provenance passed. Generic three-dimensional profiles and extra first-order sectors remain outside the theorem. The smallest unresolved rescue question is whether an actually admitted genuinely three-dimensional or changed-operator preparation can satisfy the full local clock and metric compatibility conditions; this theorem neither constructs nor excludes it.
