# Unequal weak Yukawa couplings do not rescue the raw-source link

Scope: the same canonical rigid SU5 real aligned branch, arbitrary h>0 and
lambda>0, f>0, g=sqrt(29/200)lambda, at its leading CW minimum. This is not
a theorem for arbitrary gauge coupling, extra mass sources or backgrounds.

In f=1 units set Delta=30h²+lambda², c=lambda²h/Delta and z=hX/sqrt(c).
The three X-dependent representation blocks in TP01 have

    hX=sqrt(c) z, lambda a=sqrt(2c),
    ga=sqrt(29/200)sqrt(2c), gb=sqrt(29/200)sqrt(c)z.

Every entry of their scalar/vector mass-squared matrices is c times a
universal function of z; their fermion mass matrices scale as sqrt(c).
Individual CW blocks can contain c²log(c) constants. In the full sum
STrM4=0 at this g/lambda, so CW=c²Phi(z). The remaining massive singlet
bosons/fermions cancel in CW. Thus its leading minimum z0 is universal,
even when h/lambda is highly unequal.

The external residual-U1 gaugino couples only to charged broken-sector
states. Both scalar and vector mass-eigenstate vertices carry g; all their
internal masses have the above common scaling. The leading finite pole
therefore has

    mchi_hat=Kchi(z)lambda²sqrt(c).

This also follows directly from the finite B0 self-energy: changing c adds
a log(c) constant whose chirality-flip sum vanishes by the finite threshold
identity. At z0, Kchi=sqrt31 C_equal, with the established equal-coupling
coefficient C_equal=.00011164161505832251. No small-F expansion is used.

The true rigid auxiliary norm is F_eff=f lambda/sqrt(Delta). Restoring f
then eliminates its normalization:

    mchi/sqrt(F_eff)
      =Kchi lambda^(5/2)sqrt(h)/Delta^(1/4).

The fourth power after removing Kchi is P=lambda^10 h²/Delta. Its exact
derivatives are

    dP/dh =2h lambda^12/Delta² >0,
    dP/dlambda =lambda^9 h²(300h²+8lambda²)/Delta² >0.

Consequently h,lambda<=L gives the largest leading mass at h=lambda=L.
The raw-source condition F_eff²=rhoDE then implies

    mchi <= C_equal (31rhoDE)^(1/4)L^(5/2).

At L=.03 this is9.20001e-11eV for the stated DE benchmark, while even the
generous compact-support halo benchmark requires16.16eV. The gap exceeds
eleven orders in mass. The45--50 decimal-order minimum raw-energy excess
derived in SCALE_CONSTRAINTS.md therefore extends to unequal positive h,
lambda on this critical-gauge CW branch. A small ratio of Yukawa couplings
cannot by itself repair it. New mass mechanisms, another gauge/background
branch, interacting matter or a separately tuned net vacuum alter premises.

The computation tests full matrix threshold implementations at nine coupling
pairs and three fixed z values, and verifies the two exact monotonicity
identities. The uniform conclusion comes from the scaling reduction, not
from treating a finite grid as a proof. Higher-order corrections are not a
new eleven-order mass source in a controlled perturbative expansion; a claim
outside that regime would require a new calculation.
