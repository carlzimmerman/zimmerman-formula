# Necessary energy and travel inequalities

These inequalities address the near-fold threshold loophole without replacing
the unknown nonabelian collision operator by an asserted annihilation rate.
Assume a cold sigma population, Einstein expansion, no energy transfer to SM,
and positive-energy hidden particles with averaged 0<=w<=1/3. The present
photino rest density is fixed to rho_chi,0=.265 rho_c. The light SU3/SU2
particles may annihilate, scatter and thermalize in any way preserving this
hidden stress tensor. The neutral photino must remain collisionless; this is
a named separate assumption, checked for the computed heavy-contact class.

Define K(a)=rho_hidden(a) a^4. Stress conservation gives
dK/dln a=(rho_hidden-3P_hidden)a^4>=0. Start with N_sigma cold mothers.
After every mother decays, even if every daughter immediately becomes massless,

    K(a_rec)>=N_sigma m_sigma <a_decay>.

Subsequent rest mass only increases K. Since H>=H_SM at fixed a, the cold
mother's decay scale-factor distribution is stochastically later than in SM
radiation. In constant-g radiation with H=C/a²,

    <a_decay>_SM=sqrt(pi C/(2 Gamma)),
    a_median,SM=sqrt(2 C ln2/Gamma).

All threshold controls decay after electron annihilation, where this C is
the exact low-temperature limit of the implemented SM radiation table.
For a phase-closed mother the maximum number of photinos per sigma is 2Bchi.
Pauli suppression or additional mother widths can only decrease this yield.
Thus N_sigma>=rho_chi,0/(2Bchi mchi), and

    K_rec >= rho_chi,0 m_sigma <a_decay>_SM/(2Bchi mchi).

For the budget control we generously permit extra matter equal to10% of the
target photino matter plus pressure-equivalent DeltaNeff=.3. For any massive
particle E-m<=p²/E, so kinetic energy is bounded by3P. Consequently

    K_rec <= Kmax=1.1 rho_chi,0 a_rec + .3 rho_one_neutrino,0,
    a_rec=1/1101.

This is an explicit benchmark budget, not a fitted likelihood. It is more
generous than requiring photinos alone to occupy the target dark matter.
The resulting necessary Bchi bound prohibits arbitrary beta_chi→0 while
fitting the full abundance. It does not depend on whether nonabelian energy
is temporarily matter or radiation.

A travel lower bound begins **at recombination**, not before production.
At least one half of direct photinos have a_birth>=a_median,SM, hence
q>=mchi sqrt(r²-1) a_median,SM, r=m_sigma/(2mchi). The allowed energy
budget also yields H<=sqrt((rho_SM+rho_b+rho_L+Kmax/a_rec/a³)/(3Mp²))
after recombination because hidden energy cannot redshift slower than matter.
Before recombination H<=sqrt((rho_SM+(Kmax/a⁴)+rho_b+rho_L)/(3Mp²));
integrating this bound controls the residual undecayed fraction there.
The solver integrates the subsequent travel of at least one half minus
that residual population. Earlier travel is nonnegative. This proves the
displayed lower bound for each tested parameter point under the neutral
collisionless assumption; it makes no pre-production Pauli-floor claim.

The numerical threshold controls tune the physical mass ratio r, and do not
pretend that a one-loop photino mass locates a fixed-t threshold at precision
better than its uncomputed higher-order counterterms. Actual finite-action
stationary rows m_sigma/mchi>=2.01 are separately transported.

# A distinct existing-action source: thermal gravitational scattering

The universal coupling h_mu_nu T^mu_nu/Mp is already present in the Einstein
embedding. Tang and Wu, arXiv1708.05138v2,26October2017, equations3.7,3.15
and TableI authenticate the photon-to-fermion cross section. Converting their
Dirac final state to one Majorana species and kappa=2/Mp gives
sigma(gamma gamma->chi chi)=s/(640pi Mp^4) in the relativistic limit.
The identical-photon event factor1/2 cancels the two produced photinos.
For Maxwell-Boltzmann photons, direct integration gives

    dnchi/dt+3Hnchi = [3/(20pi^5)] T^8/Mp^4.

The code independently integrates the Bessel representation and verifies
integral z^6 K1(z) dz=384. In constant-g RD the yield is C/(3sH/T^5)
times (TR/Mp)^3. We also compute a deliberately excessive all-SM source
envelope:128² ordered incoming polarization pairs, two photinos per event,
and sigma<=s/(8pi Mp^4) for each. It counts forbidden mixed-species pairs
and exceeds the massless TableI kernels. This is a conservative abundance
test, not the exact SM coefficient. TR<=.01Mp is the declared weak-gravity
benchmark range. Failure there does not prove no possible Planck-scale
reheating history, nor compute the full hidden heavy-spectrum cascade.

Sources were authenticated by primary arXiv PDF tool reads. No old observational
limits are imported. Hasenkamp/Kersten1212.4160v2 equation33 supports the
general travel integral; Hall et al0911.1120v2 equations6.7--6.9 support the
source/yield convention. The equations used here are independently derived.

V2 strengthens the late-travel bound by integrating all exponential birth
quantiles u=Gamma t with measure exp(-u)du, using64-point Gauss-Laguerre
quadrature. Every actual birth quantile lies at a>=sqrt(2C u/Gamma).
The residual not yet born by recombination is bounded explicitly and removed
with a deliberately large path bound. The original half-population bound is
retained as an orthogonal weaker control. A root at the Ward survival=.99
boundary and energy-budget saturation checks the narrow optimum missed by a
coarse e grid; this is a boundary control, not a global monotonicity proof.

V2 also evaluates exact massless-SM direct-source multiplicities. The MB
T8/Mp4 coefficient is [4/80+45(3/80)+12(3/20)]/pi5 for four real Higgs,
45 Weyl fermions and12 massless gauge generators, producing one Majorana
species. Quantum initial distributions multiply each bosonic contribution
by zeta(4)^2 and each fermionic one by [(7/8)zeta(4)]^2 because the massless
cross section is linear in s and the radial incoming integrals are E³ f(E).
This source remains only direct photinos; gravitational production of the
entire hidden heavy spectrum and its later cascades has not been computed.

V3 correction after adversarial review: replace every low-T C in birth
quantile bounds by Cmin=sqrt[rho_SM(ai) ai^4/(3Mp²)], ai at the stipulated
20MeV start. Since rho_SM a^4 is nondecreasing for the exact electron,
photon and neutrino EOS, H>=Cmin/a² holds throughout the run, including
e± annihilation. Every birth obeys a>=sqrt(ai²+2Cmin u/Gamma); dropping
ai² is conservative. The named mean_decay_a_RD is now this conservative
lower bound, not the physical low-T mean. The pre-rec Hupper includes the
full SM table, baryons, Lambda and Kmax/a^4. Its time integral tmin_rec
bounds how many actual mothers have decayed by recombination. The Krec
inequality uses the explicitly truncated integral up to Umin=Gamma tmin_rec,
namely sqrt(pi Cmin/(2Gamma))*gammainc(3/2,Umin). All future decays are
omitted from that lower bound. Late travel subtracts the remaining fraction
exp(-Umin) times1e5Mpc. This length exceeds the entire post-rec relativistic
path even using only the positive Omega_b=.05 term as the H lower bound.
Thus the literal finite-recombination statement and the thermodynamic
history are covered. V1/V2 numerical records remain preserved, but V3 is
the preferred necessary-control evidence.
