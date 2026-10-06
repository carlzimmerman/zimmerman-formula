# Independent raw-source audit: second-order repaired plane seed

**Primary verdict: proved as written for the common-sector second-order claim.** The declared smooth decaying plane seed has the stated simultaneous common lapse/shift/curvature and homogeneous trace/anisotropy solution on every compact de-Sitter time interval, for fixed H,k>0 and 0<eta<1. The calculation does not admit the entire second-order relative perturbation or prove nonlinear existence; the norm-cube relative regularity leaf remains open.

Pinned frozen REPORT.md SHA256 `26127290b70b296faedb67434020acef3f902d0bbff98416bdc851c2b3400883`; checks.py SHA256 `e68c59efee2825212de95186bad82665de0960edc251e1b3d3df321515da892c`. No author scientific inputs were edited. Review independently constructed raw plane ADM densities and Euler variations in temporary symbolic jet code, without importing author helpers; the final analytic reconstruction is recorded below. Prior project context is acknowledged; agreement between agents is not itself proof.

## Exact target and action assumptions

The action is the frozen projected acceleration difference plus -eta K times both individual shear squares, geometric-mean interaction volume and M=-A+I/2-I^1.5/12+... . It is the coincident empty n3 on-shell de Sitter branch, not a matter/radiation background. The first relative lapse is u=v cos(kx), vdot=-Hv. The author uses exponential metric/lapse coordinates, contravariant shift S and coefficients of epsilon² without a factorial. Mean second-order variables are chart-dependent corrections, not gauge-invariant effective densities.

The necessary dependency chain is raw ADM action with both-sector normals -> source Euler variations before setting mean fields to zero -> temporal/spatial Noether identities -> actual mean lapse/shift elimination WITH sources -> curvature equation -> zero-mode trace and tracefree equations. The independent homogeneous operator alone is insufficient. The remaining relative norm-cube force is excluded from the theorem rather than silently removed from the action.

## Independent source construction

For the plane metric gamma=a²diag(exp X,exp Y,exp Y) I independently recover

    kx=(H+Xdot/2-sXx/2-sx)/N,
    ky=(H+Ydot/2-sYx/2)/N,
    R3=a^-2 exp(-X)[-2Yxx+XxYx-3Yx²/2].

The shear-deformed ADM kinetic is (1-eta)(kx²+2ky²)-(1-eta/3)(kx+2ky)². For X=2Z+u,Y=2Z-u,N=exp(V+u/2) and its opposite-relative counterpart, N exp[(X+2Y)/2]=exp(V+3Z) in both sectors exactly. This checks the actual geometric-mean constant term -12KH²a³ exp(V+3Z). The projected term is Ka exp(V+Z)cosh(u)ux²; its volume/lapse factor is varied, not fixed.

I formed independent Euler jets JV=partialL/partialV, JS=partialL/partialS-partial_x(partialL/partialSx), and JZ=partialL/partialZ-partial_t(partialL/partialZdot)-partial_x(partialL/partialZx)+partial_x²(partialL/partialZxx), then set mean variables to zero and retained epsilon². Time derivative acts on a and u, ux with adot=Ha, udot=-Hu; spatial jets retain uxx until the final eigenfunction substitution uxx=-k²u. Each independently obtained expression agrees exactly:

    JV=-Ka[3H²a²k²u²-4H²a²ux²-4k⁴u²+4k²ux²]/k²,
    JS=-(2/3)HKa³(8eta-15)u ux,
    JZ=-H²Ka³(3k²u²-4ux²)/k².

Thus these are action Euler sources, not phenomenological source assignments. Their dimensions and the distinction between a contravariant shift and the earlier covariant beta are essential.

## Temporal identity and direct shear-clock check

Using the report's common coordinate convention deltaV=Tdot, deltaZ=HT, deltaS=-Tx/a² and deltatheta=T, integration by parts gives Jtheta=JVdot-HJZ-JSx/a². Since JV=JZ+4Ka(k²u²-ux²), JZdot=HJZ and the second term has logarithmic time derivative -H, the combination reduces to

    Jtheta=KaH(6-16eta/3)(k²u²-ux²).

This is the correct sign; reversing every infinitesimal coordinate convention gives the same identity. On the seed, kx-ky=-Hux²/k² at quadratic order, so each sector's mixed tracefree curvature is sigma2xx=-2Hux²/(3k²), sigma2yy=sigma2zz=Hux²/(3k²). The background clock variation is minus the tracefree spatial Hessian divided by a². Its added Euler term is therefore +4eta Ka partial_i partial_j sigma2ij=-16eta KaH(k²u²-ux²)/3. It agrees independently with the temporal identity. The retained original projected clock source supplies the remaining +6KaH term.

The integral of this harmonic source is zero. This permits a nonzero-mode elliptic inversion but does not alone solve the metric rows or full nonlinear equations.

## Source-aware mean solution

The 2k harmonic uses p=4k²/a²,r=v²,c=Ka³. Projection of the raw sources gives JV=cr(p-7H²/2), JZ=-7cH²r/2. Since JS=partial_x jt, the source for t=-Sx is Jt=Hcr(15-8eta)/6, with its sign checked by integration by parts. The full mode action is

    2c[-6F²-4Ft-(2eta/3)t²+2pZ²+4pVZ]
    +Jt t+JV V+JZ Z,
    F=Zdot-HV.

The factors 2pZ² and4pVZ belong to the mean sector and cannot be replaced by relative-sector coefficients. Solving both auxiliary equations with these sources and retaining time derivatives of c,p,r gives the reduced row

    EZ=cp[9H²(1-eta)r+16eta pZ+2eta pr]/[6H²(eta-1)].

Its unique harmonic solution is Z=-r/8-9(1-eta)H²r/(16eta p). The actual reconstructed auxiliary fields are V=r/8,t=Hr(9-8eta)/(16eta). Because rdot=-2Hr and pdot=-2Hp, Zdot=Hr/4 and F=Hr/8.

I checked the uneliminated rows directly. The shift equation -8cF-(8eta/3)ct+Jt=0 vanishes. The lapse equation 2c(12HF+4Ht+4pZ)+JV=0 vanishes. The curvature equation 2c[4p(Z+V)+12Fdot+4tdot+3H(12F+4t)]+JZ=0 also vanishes. This directly tests simultaneous sourced admission, not merely a solved reduced clock equation.

The raw linear clock row is -(8eta/3)cpt=-cHpr(9-8eta)/6. The quadratic clock source is +cHpr(9-8eta)/6. They cancel. Substituting the latter raw source into an already homogeneous-eliminated Q=Z-Hpi constraint would omit auxiliary-source terms and give a different Z; the control correctly rejects that shortcut.

At nonzero k the common longitudinal-spatial equation follows the spatial Noether identity once the momentum row is solved, with first-order rows and background equations already satisfied. Plane symmetry gives equal transverse y/z sources, zero off-diagonal transverse entries and no finite-k TT/vector source. This reasoning is specific to this seed, not a multipolar classification.

## Zero modes independently checked

Averaging gives JV0=JZ0=cH²r/2 and JS0=0. The homogeneous isotropic lapse row is 24cHF0+cH²r/2=0, so F0=-Hr/48. Its curvature preservation row 24c(F0dot+3HF0)+cH²r/2=0 is consistent. In proper mean time V0=0, Z0=r/96 plus a constant. No p^-1 continuation of the nonzero-mode solution is used.

I independently added a homogeneous diagonal tracefree jet to the raw ADM action. With the author's normalization X=2Z+2Q/3+u,Y=2Z-Q/3-u (and opposite u for the second metric), the kinetic Hessian is 2c(1-eta)/3 and the averaged Euler source is 2c(1-eta)H²r/3. These yield Qddot+3HQdot=H²r, with Qdot=Hr+C a^-3. An alternative jet X=2Z+2q,Y=2Z-q has Q=3q; keeping that factor avoids a spurious factor-three disagreement. Both kinetic and source contain the shear deformation's factor1-eta. The positive tensor interval was already specified; this is a regular finite-time forced homogeneous solution, not an inferred abundance.

## Envelope and precise remaining scope

The norm-cube action reduces at leading amplitude to -K/(6a0) integral|gradcoord u|³. Its common variation starts at cubic order, so it does not add the common epsilon² sources above. Its relative Euler derivative is +K/(2a0)div(|grad u|grad u), equal to -Kk³v|v||sin(kx)|cos(kx)/a0 for this plane. It is continuous/Lipschitz but not C1 at the nodes and has epsilon|epsilon| amplitude dependence. Exchange evenness does not remove it. The report correctly does not claim a generic smooth cubic implicit-function theorem.

The forced relative-harmonic lapse and kinetic formulae in section5 are consistent with the parent quadratic action. A source Jnu adds Jnu times the homogeneous lapse solution to the reduced action, up to a source-only constant; this does not furnish spatial smoothing at arbitrarily high harmonics. Full relative metric/curvature regularity and prepared data remain separate obligations. This audit does not turn harmonic finite-time ODE solvability into smooth whole-field admission.

All finite-time common corrections are smooth for fixed H,k,eta on the stated interval. Limits eta0,k0,large duration or amplitude are nonuniform, and small-amplitude admissibility must be maintained. No physical density, cold abundance, matter/radiation perturbation health, observational fit or32pi follows.

## Evidence and verdict limits

Independently validated all four current manifests against pinned/current input and output hashes: main_a22/22; control_shear_a21/22 only `control_retains_added_shift_source` fails; control_auxiliary_a21/22 only `control_retains_actual_lapse_source` fails; control_clock_a21/22 only `control_raw_clock_is_not_eliminated_source` fails. Exact raw-source, Noether, all-mean-row and zero-mode obligations pass independently. Symbolic output corroborates the finite identities; it is not a nonlinear existence certificate.

The smallest unclosed implication is a sufficiently regular solution of the actual relative norm-cube forced metric equations, compatible with the common fields and all initial constraints. This report closes the common second-order mean leaf only. No blocking correction to its declared claim was found, and no author input was modified.
