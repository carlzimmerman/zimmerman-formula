# Which gravity and dark-energy link is being tested

The current repository V3 action contains the Einstein term plus a khronon,
an independent spatial covector P, J(Y), K(Q) and a fitted stiffness. Its
recorded acceleration relation is a0=kappa c sqrt(G rho_Lambda), with
kappa=1/2 fitted. The law/certificate correction does not change that status.
The source is covariant_push_2026_10_22/V3_FULL_PICTURE.md, lines 21--41
as read at the TP05 base; the exact source hash is pinned by the coordinator.

The concrete N=1 SUGRA constructions here supply particle actions coupled to
Einstein-frame supergravity and calculate their potential, local stationary
point and spectrum. They do not automatically supersymmetrize the khronon/P
action, derive J(Y) or select kappa. A complete V3 embedding would additionally
need the multiplets, constraints and matching operators for those fields.
This missing map is not filled by a small net cosmological constant.

Three energy statements must remain separate:

1. The rigid auxiliary norm is F_eff^2=mu^4/31 on the specified branch.
   Setting this raw energy equal to the DE benchmark fixes mu near
   5.286e-12 GeV and gives an ultralight radiative photino.
2. A SUGRA potential contains positive auxiliary terms and a negative
   3 m_3/2^2 M_P^2 term, together with any D terms or added sectors. These
   affect stationarity and the spectrum; they are not an arbitrary constant
   added after the rigid calculation.
3. The final gravitating positive residual rho_net determines Lambda in an
   Einstein-frame description. If it equals the observed DE benchmark, it
   can be inserted into the repository's already postulated acceleration
   formula. Choosing W0 or another residual parameter to make this happen
   is a tuning/input, unless a mechanism actually selects it.

For a leading canonical cancellation, W0^2=M_P^2(F_eff^2-rho_net)/3.
Its fractional sensitivity is

    d rho_net/d ln W0 = -6W0^2/M_P^2,
    delta W0/W0 required for delta rho~rho
        =rho/[2(F_eff^2-rho)].

A no-scale identity, protected modulus or stabilization mechanism must be
tested with its full specified K,W and physical modes. If its cancellation
leaves an independent residual parameter, it preserves a conditional net
link but does not derive the microscopic source link. Loop thresholds and
new soft masses can change the vacuum again and must be accounted for.

The original microscopic stiffness target B_curv/V_total also changes when
a large F energy is cancelled. A small net residual does not force the
radiative curvature to cancel with it. No comparison to the earlier numerical
target is used to select couplings or presented as a derivation of kappa.

Constants and cosmological values remain the TP04 NIST/Planck benchmark.
rho in the field-theory calculation is an energy density; rho_Lambda in
the SI acceleration formula is its mass-density equivalent. The bridge is
rho_mass=rho_energy/c^2 and Lambda=8pi G rho_energy/c^4.
