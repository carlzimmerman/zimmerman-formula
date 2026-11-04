# Canonical scalar-to-broken-vector pair matrix

The canonical real-vector mass term is

    Lmass=1/2 V_i,mu MV²_ij(S) V_j^mu.

With K_aij=d MV²_ij/dS_a, its cubic term is 1/2 S_a K_aij V_i.V_j.
Differentiation with respect to the two vector legs gives vertex
i K_aij g_munu for both i=j and i!=j: the identical-leg factor cancels the
one-half in the first case; the two ordered off-diagonal mass-matrix entries
cancel it in the second. No initial scalar spin average occurs.

For on-shell physical massive vectors, summing their three polarizations
gives

    sum (epsilon_i.epsilon_j)(epsilon_i.epsilon_j)*
       =2+(ki.kj)²/(mi² mj²)
       =2+(M²-mi²-mj²)²/(4 mi² mj²).

This is checked independently with two transverse polarization vectors and
the explicit longitudinal vectors (p/mi,0,0,Ei/mi) and
(p/mj,0,0,-Ej/mj). The exact two-body phase-space integral is beta/(8pi);
the decay flux is 1/(2M). Distinct species have no symmetry division, whereas
two identical real vectors have a factor one-half. Consequently

    Gamma_ab,ij = beta/(16pi M) * K_aij K_bij/(1+deltaij)
        *[2+(M²-mi²-mj²)²/(4 mi² mj²)],  i<=j.

For identical mass m and coupling c, this reduces to

    Gamma=c² M³/(128pi m⁴) sqrt(1-4r)(1-4r+12r²), r=m²/M².

Two equally coupled real components equal one charged complex vector pair:
the latter's distinct-particle width is twice the single-real identical
width. The twelve real broken-vector species therefore equal six charged
complex pairs, without an extra factor of two. Standalone special-formula
checks cover threshold, intermediate and high-energy masses independently
of the actual model matrix.

Because the actual singlet block is proportional to the vector identity,
its vector-rotation check alone is algebraically simple. A separate generic
four-parent, five-vector symmetric-K fixture therefore tests the independent
ordered expression beta*polar/(32pi M) sum_ij K_aij K_bij against the
unordered implementation. At m/M=.02,.2,.49 they agree below 3.2e-16.
Independent nontrivial parent and vector rotations preserve covariance below
4.4e-16. This fixture tests counting and linear algebra, not an extra model.

## Actual model normalization and basis

The frozen loop.build reconstructs the actual scalar charge/Casimir basis,
vector mass basis, and K. Its gauge mass matrix is
MV²_ab=2g² Re[(Ra z)†(Rb z)]. The probe differentiates this matrix directly
at z±epsilon E O e_a in canonical scalar directions, holding the reference
vector basis fixed. It tests all four parents plus a strongly coupled
physical scalar so that a near-null vertex cannot hide a normalization
mistake. Relative derivative discrepancies are below 2.7e-11. The separate
Goldstone cubic Ward relation agrees below 3.6e-17 in normalized mass units.

The four massive parents are S1_1, indices [94,95,96,97] at the warm states
and [60,61,62,63] at the cold pole. The full actual-x cubic/Yukawa tensors
give their SSS+FFS matrices in the same basis, independently matching the
grouped tree operator below 2.1e-15 relative. No pole matrix is transplanted.
Parent and degenerate-vector real orthogonal rotations preserve the matrix
covariance below 4e-16. The broken-vector singlet block is proportional to
the twelve-dimensional identity to numerical precision.

## Finite physical result

| x | mV/mu | Average GammaVV/mu | Average GammaSSS+FFS/mu | Trace ratio |
|---|---:|---:|---:|---:|
| 3.82758980 | .03434507 | 1.21673e-9 | 6.13926e-8 | 1.98189% |
| 4.07863572 | .03527518 | 9.92755e-10 | 6.08596e-8 | 1.63122% |
| 3.86322330, corrected midpoint | .03447498 | 1.18405e-9 | 6.13215e-8 | 1.93088% |
| 25.40002540, cold pole | .14747881 | 0 | 1.89259e-9 | 0 |

Average means trace divided by four. The warm VV matrix is rank one, with
nonzero eigenwidths 4.86694e-9, 3.97102e-9 and 4.73619e-9 mu at the three
warm points. The largest eigenvalues of
Gamma_other^-1/2 GammaVV Gamma_other^-1/2 are .089462, .073138 and .087077.
Thus a coherent bright parent can see a larger relative width than the
isotropic trace average. This is an actual nonzero missing tree channel,
not an inference from an open threshold alone. It is percent-level in this
parent's inclusive width, not a demonstrated dominant whole-network rate.

At the cold pole M<2mV, so this on-shell pair width vanishes exactly. No
off-shell vector process is calculated or ruled out by that statement.
Vector final states remain massive and can carry unbroken charges; their
production is not automatically an irreversible neutral/radiation sink.
A consistent extension needs their populations, polarizations or justified
depolarization, force, inverse reactions and subsequent charged returns.

## Corrected-history kinematic coverage

The corrected target-reached history/run_advance002 endpoint is N=.00216902,
xmid=3.86322330 and orbit endpoints 3.576735 to 4.155752. Its actual Y and
40-node q/W arrays are used to reconstruct the saved eight-phase orbit.
Existing coverage.coverage gives a phase-averaged eligible-parent number
fraction .223468% and energy fraction .545969%, with maximum energy fraction
.551958%. The eligible groups are Sc_2, S8_2, S8_3, S3_2, S3_3, S1_1,
Fc_2, F8_2, F3_2 and F1_2.

This is only a conservative mass-threshold screen for omitted V+S/F exits.
It proves neither nonzero vertices nor a small reaction rate: a small
instantaneous parent population can be replenished and processed repeatedly.
The actual V+S/F amplitudes and vector reaction network remain the first
missing implication for a quantitative full-sector correction. The present
VV probe establishes a real omission but does not rank all omitted channels
or recompute a physical history.
