# Regular inverse and linear work for exact cold-dominated halos

Checkpoint ZAR-2026-10-19-11-CX. This is the synthesis of the raw proofs in
this directory. Their exact independent review status is recorded in README
and CHECKPOINT.json. Every result concerns the original spherical two-species
deep-cubic model. No claim of nonlinear confinement is made.

## Statement and quantifiers

Let `r_M=sqrt(G M_b/a_0)`, take `f=1/64`, and use the original smooth hollow
profile at radii

    (r_0,r_1,r_2,R)=D r_M (1,2,3,4).

There is a locally finite exceptional set of positive scales `D`, described
in `GEOMETRY_AND_CAP.md`, outside which both species have finitely many
simple epicyclic extrema. Choose any sufficiently large `D` outside that
set and then one sufficiently small **fixed positive** intrinsic warmth
`delta` for the exact smooth DF inverse and the stated frequency geometry.
The law-annulus cold mass is `M/M_b=D x>=2D`, so this is a cold-dominated
halo. Constants below need not be uniform as `D` varies or `delta` tends
to zero.

Fix the exact smooth equilibrium supplied by that inverse. In a sufficiently
small neighborhood of its exact density-null distribution variations, there
is an open dense subset `U_good` for which the following conclusions hold.
The parameter topology, exact right inverse and positivity margins are those
in `GENERIC_FORCE_CANCELLATION.md`, Section 2. These variations retain each
species' density, mass, occupied support, potentials and frequency geometry
**exactly**. They preserve positive DFs and strictly negative physical energy
derivatives. They change the kinetic distribution within its existing warm
tube. An independently specified original DF has not been certified to lie
in `U_good`.

For every fixed equilibrium in `U_good`:

1. Its full actual boundary feedback pencil has only finitely many singular
   real frequencies `E`, all genuine neutral energy-mode frequencies. The
   ordinary boundary inverse exists elsewhere and is bounded on compact sets
   avoiding `E`. At large frequency it is bounded by a convergent Neumann
   series, with no small-cold-mass hypothesis.
2. On a closed upper strip there are finite-rank residues `R_nu` and an
   operator-valued bounded Holder function `B_reg` such that

       (I-K(z))^-1=sum_(nu in E) R_nu/(z-nu)+B_reg(z).

   This is the regular inverse after the actual mode poles. The ordinary
   inverse at a mode frequency itself is not asserted.
3. Every actual mode has bounded work on the entire closed occupied action
   set. At a fundamental circular threshold the required radial force trace
   vanishes; all eccentric cap limits and physical radial endpoints are
   controlled as well.
4. For every smooth compact radial fixed-`L` canonical generator `g_0`, the
   full linear self-consistent evolution from `h_0=-w Dg_0` satisfies

       sup_(t>=0,i,q in CLOSED occupied actions,theta_0)
             |W_i(t;theta_0,q)| <= C_halo N(g_0)<infinity,

   where `N` is a finite sum of smooth-source seminorms and the initial energy
   norm. In particular it is bounded by a fixed finite smooth norm of `g_0`
   on a neighborhood of the occupied physical set. The associated linear
   label `u`, extended to the boundary by its transport equation, is uniformly
   bounded there.

The genericity is in the **exact DF choices at fixed density and potential**.
There is no genericity claim for all unspecified halo profiles, no numerical
parameter certificate, and no assertion that every admissible DF has these
conclusions. The choices can be arbitrarily close to the original exact DF.

## Proof from the raw obligations

`GEOMETRY_AND_CAP.md` gives the nonempty cold-dominated family, proves the
full action-frequency gradient remains nonzero in the chosen warm tube,
and controls eccentric cap resonances and physical endpoints.
`BOUNDARY_PAIRING.md` then supplies the complete source anti-dual map,
reciprocity, optical form and compact field boundary operator.

`REGULAR_INVERSE.md` uses that optical form and the source smoothing exponent
`1-gamma>1/2` to reconstruct every boundary kernel as an actual energy mode,
uniformly near simple circular thresholds. Orthogonality and compactness
make the exceptional frequencies locally finite. `HIGH_FREQUENCY_INVERSE.md`
proves `||K(z)||<=C(1+|z|)^(-p)` for some `p>0`, so their full set is finite.
This proves conclusion 1 and its leading-pole description.

`THRESHOLD_MODES.md` bootstraps actual mode fields to `C^(1,1)` by direct
physical radial density estimates. It identifies the only remaining local
modal obstruction in this geometry as the nonzero fundamental circular force
trace. `GENERIC_FORCE_CANCELLATION.md` discharges that obstruction on `U_good`:
exact density-null variations, a distributional density-adjoint argument,
and incompatible circular blow-ups prove scalar transversality; local
constancy of the minimal Fredholm nullity then forces every threshold kernel
to have zero force trace on an open dense parameter set. The threshold list
is finite and fixed because the potential is fixed.

`REDUCED_INVERSE.md` proves that this force condition makes both frequency
off-diagonal blocks divisible by `z-nu` and the kernel block equal to
`(z-nu)Q_Gram/nu+(z-nu)^2 C(z)`, with Holder `C`. Schur inversion leaves a
bounded Holder remainder after the leading pole. A finite patching argument,
together with the high-frequency inverse, proves conclusion 2. The cap,
endpoint, higher-harmonic and fundamental-force criteria prove conclusion 3.

Finally `CONDITIONAL_WORK.md` proves the smooth-source transform estimates,
the needed modal left-coupling difference quotient, and the exact identity
between its residue and the energy spectral projection. After the actual
mode terms are subtracted, its derivative field transform is Holder with
`O(1/|z|)` decay. The receiving Dini estimate is summable in the orbital
harmonics, uniformly through the closed occupied set. The finite modal sum
is bounded by conclusion 3. The endpoint label identity then gives conclusion
4. No future work bound, nonlinear trajectory estimate or stationary
replacement is a dependency of this proof.
