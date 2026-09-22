# Second attempt: a bare electric block projector loses the vacuum

Base `b73311096299e2f1816be00036ccdb2922bc44d4`, checkpoint YM-C1.
This tests the first attempted construction behind `SCHUR_GAP.md` rather
than supplying its projector hypothesis by definition.

The tempting choice is to retain a product of bare local vacua (and some
coarse variables), then use the positive electric energy to bound the
discarded sector. Ground-energy subtraction and volume invalidate that
argument without a vacuum dressing. The following exactly solvable model
shows the issue already in independent, uniformly gapped cells.

Let h on C^2 be

    h = [1/3  -2/3].
        [-2/3  4/3]

It has eigenvalues 0 and 5/3 and normalized vacuum omega=(2,1)/sqrt(5).
It is the true-vacuum shift of the bare Hamiltonian
[[0,-2/3],[-2/3,1]]. On L independent cells put H_L=sum_i h_i. Its
vacuum Omega=omega^{tensor L} is simple and gap(H_L)=5/3 for every L.

Choose the bare retained vector b=(1,0)^{tensor L} and projections
P=|b><b|, Q=I-P. Its squared vacuum overlap is

    p_L = |<b,Omega>|^2 = (4/5)^L.

The nonzero normalized vector

    v = (Omega-sqrt(p_L)b)/sqrt(1-p_L)

lies in Q. Since H_L Omega=0 and <b,H_L b>=L/3,

    <v,H_L v> = (L/3) p_L/(1-p_L).

Consequently

    inf Spec(Q H_L Q|_Q) <= (L/3) (4/5)^L/[1-(4/5)^L] -> 0.

The original Hamiltonian remains uniformly gapped. The would-be
eliminated block D is not: it contains almost the entire interacting
vacuum as the volume grows. Thus a bound on D after the actual vacuum
subtraction cannot be inferred merely from local electric excitations,
finite-dimensionality, or a positive gap in each cell.

For a general mixing strength t>0 in [[0,-t],[-t,1]], the same calculation
gives delta=sqrt(1+4t^2), e_bare=(delta-1)/2, p_L=[(1+1/delta)/2]^L,
and the upper bound L e_bare p_L/(1-p_L). This tends to zero for every
fixed t>0, however weak the local mixing. Small per-cell error does not
mean small error in the global vacuum vector at arbitrary volume.

This example does not rule out all gauge-compatible projectors. It rules
out the inference that a bare product projector automatically supplies
the required eliminated-sector bound. A coarse projection that retains
physical long-wavelength degrees of freedom needs its own analysis.

## A noncircular next candidate

In a ground-state representation, a conditional expectation onto coarse
variables preserves the constant vacuum exactly. Such a projection avoids
the overlap defect above. But its conditional law is the interacting
ground-state measure, not Haar measure and not the Euclidean Wilson
measure by fiat. Bounds for its discarded sector require a conditional
Poincare estimate for that law. The exact coarse Schur operator and its
induced metric then still have to be controlled.

Projecting onto the true low-energy spectral subspace would also avoid
the defect, but using a known spectral gap to construct that projection
would assume what the argument is meant to prove. The conditional-measure
route names an analytic target without making that spectral assumption;
no Yang–Mills estimate for it is established in this checkpoint.
