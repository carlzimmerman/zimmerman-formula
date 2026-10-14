# Binding-assisted baryon conversion: conditional rates and a reverse channel

2026-10-14. BCR-001, base0dd3b30e2a07e2156dee1cb90c42effad81d016e.
Continuation of the [neutron portal construction](../cold_to_baryon_portal_2026_10_14/REPORT.md).
Self-reviewed model calculation. The cold component has not been identified
with these new particles, and no experimental viability or working converter
is claimed.

The new result is a rate, within explicitly defined nuclear models, for
chi+p -> deuteron+S. It is nonzero and almost velocity independent at cold
incoming speeds. The same portal also permits S+hydrogen -> chi+neutrino
through an ordinary weak interaction. Together they would constitute a
catalytic proton–electron–proton fusion cycle, with no net dark particle or
new baryon production after a completed cycle. The reverse step is extremely
slow for the sample coupling; neither a prepared cycle nor its transport
and thermalization has been demonstrated.

## 1. Fixed hypothesis and a real binding threshold

Retain the previous candidate interaction

\[
 L_{\rm tr}=yS^\dagger\bar nP_L\chi+\mathrm{h.c.},\quad
 m_\chi=m_n-0.5\ \mathrm{MeV},\quad m_S=1\ \mathrm{MeV}.
\]

Chi is an electrically neutral Dirac carrier with dark charge+1 and hidden
B=1; S is a complex scalar with dark charge+1 and B=0. These assignments,
the masses and the portal are supplied hypotheses. In the earlier charged
fluid action they were not derived. The previous real neutral curvature
scalar is a different species.

If a nucleus acquires chi's baryon number as a bound neutron, then

\[
 \chi+(A,Z)\to(A+1,Z)+S,\qquad
 Q=S_n-\Delta,\quad \Delta=m_n+m_S-m_\chi.
\]

Here Sn is the final nucleus's neutron separation energy. The example has
Delta=1.5 MeV. Binding can therefore open conversion even though an isolated
chi cannot decay in vacuum. For a proton, the final nucleus is a deuteron:
Bd=2.22456637 MeV and Q=0.72456637 MeV. This is an energy threshold governed
by nuclear structure; no new spacetime-curvature threshold has been derived.

## 2. Deriving a rate in a stated nuclear model

For a definite first calculation take the leading one-body nonrelativistic
current. Positive-energy neutron and chi spinors reduce the chiral vertex to

\[
 L_{\rm NR}=\frac y2S^\dagger n_{\rm NR}^\dagger\chi_{\rm NR}
 +\mathrm{h.c.}
\]

S is kept relativistic: in this example the outgoing scalar carries kinetic
energy comparable to its mass. Proton/neutron and deuteron motion is treated
nonrelativistically in the matrix element. External particle states have
relativistic normalization2E, and the deuteron's relative wavefunction obeys
integral d³q/(2pi)³ |psi_tilde(q)|²=1.

Project the produced neutron and spectator proton onto a normalized triplet
bound state. The external normalization factor is sqrt(8mchi mp md); multiplying
by y/2 gives

\[
 \mathcal M_{m;ab}=y\sqrt{2m_\chi m_p m_d}\,
       \widetilde\psi_d(q)\,C^{1m}_{\frac12a,\frac12b}.
\]

The initial four spin states are averaged. The sum over the three triplet
states gives3/4, hence

\[
 \overline{|\mathcal M|^2}=
 \frac32|y|^2m_\chi m_pm_d|\widetilde\psi_d(q)|^2.
\]

This derivation fixes the previously missing normalization and spin factor;
it is not an arbitrary cross section assigned to an allowed reaction.

At zero incoming relative velocity W=mchi+mp, final momentum pf follows exact
two-body phase space and q=mp pf/(mn+mp). The result is

\[
 \boxed{\sigma v_{\rm rel}
 =\frac{3p_fm_d}{32\pi W}|y|^2
          |\widetilde\psi_d(q)|^2.}
\]

For small finite relative momentum ki, average over q²=ki²+a²pf²-2a ki pf cos(theta),
where a=mp/(mn+mp). The script retains the mchi mp/(Echi Ep) flux correction
and exact final phase space; the numerator remains the declared leading
nonrelativistic current. Higher recoil/current effects are not certified.

For the defined zero-range bound state,

\[
 \widetilde\psi_d(q)=\frac{\sqrt{8\pi\gamma}}{q^2+\gamma^2},\qquad
 \gamma=\sqrt{2\mu_{np}B_d}=45.7021\ \mathrm{MeV},
\]

the angular integral also has a closed form. With
A=ki²+a²pf²+gamma² and B=2a ki pf, its mean squared wavefunction is
8pi gamma/(A²-B²). Numerical64/128-node quadratures independently agree.

To expose nuclear-model dependence, also solve three finite spherical square
wells with radii1,1.5,2fm. Each depth is tuned only to the deuteron binding
energy, using a nodeless ground-state root alpha cot(alpha R)=-gamma. The
normalized reduced radial state is A sin(alpha r) inside and an exponential
tail outside. Its analytic Fourier transform is checked against a separate
radial integral. These are defined comparison models, not fits to nucleon
scattering or a controlled uncertainty interval for real deuterium.

| Bound-state model | sigma v / y² at rest, cm³/s |
|---|---:|
| Zero-range | 1.28626e-16 |
| Square well,1fm | 1.61337e-16 |
| Square well,1.5fm | 1.80025e-16 |
| Square well,2fm | 2.00397e-16 |

The finite wells change this conditional answer by25–56%. That variation is
evidence that an actual nuclear prediction needs matching, not permission to
call these numbers experimentally established. Missing ingredients include
realistic scattering/normalization inputs, short-distance and two-body
transition operators, effective-range corrections and the physical y. The
initially free chi/proton assumption excludes matter potentials and blocking.

## 3. How slow is the chosen example?

The previous illustrative unit-coupling,1-TeV mediator parent gives
y=1.44e-11. The zero-range result then becomes sigma v=2.667e-38cm³/s.
For assigned proton density np, an ideal independent-target half-conversion
time is ln2/(np sigma v):

| Assigned proton density, cm^-3 | Half-conversion time, years |
|---|---:|
| 1 | 8.24e29 |
| 1e6 | 8.24e23 |
| 6.7e22 | 1.229e7 |

These are illustrative densities, not target recommendations or measurements.
An ideal one-year half-conversion time at the last density would require
y approximately5.05e-8 in this model. That is a required input, not an allowed
coupling established by collider, nuclear, stellar or cosmological data. No
physically viable high-rate parameter point has been constructed here.

## 4. Ordinary weak physics permits a reverse transfer

The portal's Hermitian conjugate absorbs S and turns a virtual neutron into
chi. Combine it with the ordinary charged weak current for p+electron -> n+nu:

\[
 \boxed{S+H(1s)\to\chi+\nu_e.}
\]

The electric charge is zero on both sides, dark charge goes from S to chi,
and hydrogen's baryon number goes to chi. This does not violate lepton number:
the electron's lepton number is carried by the outgoing electron neutrino.

Let mH=mp+me-BH. It is energetically open when mH+mS>mchi. That is exactly
the inequality that closes chi -> S+H+antineutrino. Thus for this portal one
cannot use masses alone to close both of these channels at once; the presence
or absence of an S bath matters. Equality is a zero-phase-space boundary,
not a useful finite-rate gate. This is a statement about these two reactions,
not a theorem that ordinary matter decays spontaneously.

The example releases QH=0.71765284 MeV including an assigned13.6-eV atomic
binding. Hydrogen alone still cannot decay to chi+Sbar+neutrino: the necessary
dark final masses exceed its mass. Incoming S supplies the difference.

For a rate calculation add

\[
 L_W=-\frac{G_FV_{ud}}{\sqrt2}
 (\bar n\gamma^\mu(1-g_A\gamma_5)p)
 (\bar\nu_e\gamma_\mu(1-\gamma_5)e)+\mathrm{h.c.}
\]

Use representative gA=1.27,Vud=.974 and the PDG Fermi constant. These are
adequate for this leading calculation, not a precision electroweak fit.
With Q=pchi-pS the free-constituent amplitude is

\[
 \mathcal M_{peS}=\frac{y^*G_FV_{ud}}{\sqrt2}
 \bar u_\chi P_R\frac{\slashed Q+m_n}{Q^2-m_n^2}
 \gamma^\mu(1-g_A\gamma_5)u_p\,
 \bar u_\nu\gamma_\mu(1-\gamma_5)u_e.
\]

In an atomic1s impulse approximation project the proton/electron pair using
M_HS=sqrt(mH/(2mpme)) psi_H(0) M_peS. The Coulomb wavefunction has
|psi_H(0)|²=(alpha mu_ep)³/pi. Average the four unpolarized proton/electron
spin states; this assumes a statistical mixture, not a prepared hyperfine
singlet or triplet population. Explicit spinors and tensor traces agree.

For two incident particles at rest the leading result is

\[
 \sigma v=\frac{p_\nu}{16\pi Wm_Hm_S}
                     \overline{|\mathcal M_{HS}|^2}.
\]

The rate uses mH0=mp+me for free constituent kinematics; omitting13.6-eV
binding here is a leading atomic approximation. Binding remains included in
the separate exact rest-energy ledger. Nucleon form factors, radiative weak
terms and actual material/hyperfine effects are also omitted.

As an independent normalization control, remove the S vertex and propagator
and reproduce the small-Q neutron-mixing hydrogen-decay formula

\[
 \Gamma_{H\to\chi\nu}/\theta^2\simeq
 \frac{|\psi_H(0)|^2G_F^2|V_{ud}|^2}{2\pi}
 (1+3g_A^2)Q^2.
\]

This is Eq5 of [McKeen–Pospelov, arXiv:2003.02270v1](https://arxiv.org/html/2003.02270v1).
The exact spinor implementation agrees within0.060% for Q=.1,.3,.5MeV,
consistent with the small recoil being retained in phase space. Their direct
mixing model's observational limits are not transferred to our S-absorption
rate or unknown S density.

For the stated chiral portal the heavy-neutron leading approximation is

\[
 \frac{\sigma v_{HS}}{|y|^2}\simeq
 \frac{|\psi_H(0)|^2G_F^2|V_{ud}|^2(1+3g_A^2)Q_H^2}
      {16\pi m_S\Delta^2}.
\]

The factor1/4 relative to a scalar nonchiral portal comes from the positive-
energy chiral projection. The full Dirac numerator agrees with this limit
within0.065% for the tested scalar masses. At mS=1MeV,

\[
 \sigma v_{HS}/|y|^2=6.60434\times10^{-43}\ \mathrm{cm^3/s}.
\]

It is approximately1.95e26 times smaller than the zero-range nuclear capture
coefficient at the same y. With the sample y, it is1.37e-64cm³/s. A hydrogen
destruction rate would be nS times this coefficient, with density, velocities,
atomic preparation and occupancy supplied. Energetic permission alone is
therefore not a claim of appreciable material instability.

## 5. The complete energy ledger becomes a catalytic fusion reaction

Add the two possible reactions:

\[
 \begin{aligned}
 \chi+p&\to d+S,\\
 S+H&\to\chi+\nu_e.
 \end{aligned}
\]

Chi and S cancel from the net species ledger, leaving

\[
 \boxed{p+H\to d+\nu_e,\qquad
 Q_{\rm net}=2m_p+m_e-B_H-m_d=1.44221921\ \mathrm{MeV}.}
\]

This has proton–electron–proton fusion's net particle content. The identity
is independent of both dark masses: Qcapture+QH=Qnet. The energy comes from
the lower mass of the deuteron final state. A completed cycle regenerates the
dark carrier and does not manufacture extra total baryon number. Calling its
energy a repeated release of consumed cold rest mass would double count it.

This is a **conditional catalytic reaction sequence**, not a demonstrated
fusion mechanism in a material. The first step emits a fast S, and the atomic
rate computed above uses S at rest. We have not solved S transport, slowing,
its probability of hitting hydrogen, or a steady cycle. Even the rest-limit
weak step is so slow in the sample that no useful catalyst is established.
If instead S escapes and never returns, a single chi capture transfers hidden
B into an ordinary deuteron while exporting dark charge; that is the previous
one-pass conversion, with its remnant budget retained.

## 6. Evidence and remaining physical question

The bounded run passes62 assertions covering spin factors, well matching and
normalization, independent Fourier integrals, twenty capture cases in four
nuclear models, angular quadrature and a closed-form angular control, explicit
weak spinor/tensor sums, hydrogen-decay normalization, scalar-absorption
limits and symbolic/numeric energy bookkeeping. The input/output-hash manifest
validates. These certify execution and the stated finite/model assertions;
they do not establish the existence or viability of the hypothetical particles.

The advance is a quantitative mechanism and an identified bottleneck. Actual
prediction still requires a matched nuclear current and deuteron structure,
a justified portal coupling, an experimentally allowed microscopic spectrum,
the cold carrier's identity/asymmetry and supply, dark-remnant transport, and
the multi-species medium/gauge/metric response. Curvature activation, the
original tether certificate and dark energy have not been unified with this
particle construction. Those programme-level claims remain open.
