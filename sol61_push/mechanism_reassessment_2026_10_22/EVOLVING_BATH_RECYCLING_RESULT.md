# Evolving Phi bath: inverse conversion changes the survival calculation

The new calculation evolves a thermal Phi/X bath with inverse reactions,
number-changing losses and energy conservation. In the reference conditional
thermal branch it gives a final cold yield YPhi approximately 7.41e-8,
about 17% of the target 4.37e-7. **This is not a seed-free prediction of the
high-H cosmology.** The missing evolution from coherent quantum-produced
fields into this thermal branch is not supplied by this calculation.

The substantive mechanism identified here is a recycling loss cycle:

    Phi + Phi <-> X,
    anti-Phi + anti-Phi <-> anti-X,
    X + anti-X <-> Phi + anti-Phi.

Together, two inverse formations and one pair conversion implement an
on-shell 4-Phi-to-2-Phi route. Inverse formation can therefore promote
number loss, rather than merely delaying the production of daughters.
No new vertex, coupling or initial cold Phi population was added.

## Action, closure and starting state

The action remains

    V=m^2|Phi|^2+M^2|X|^2+g(X*Phi^2+X Phi*^2)+lambda|Phi|^4,
    m=0.001 GeV, M=2m sqrt(1+0.02^2),
    g=2.168e-6 GeV, lambda=0.00881292.

The energy normalization is inherited from the previous high-H free-envelope
continuation. At its illustrative weak-field anchor |X|=0.001 GeV,
rho=M^2|X|^2=4.0016e-12 GeV^4 and H=3.90251e-21 GeV.
This is a counterfactual surviving reservoir, not a demonstrated late state.

The following additional assumption is explicit: this energy reaches internal
chemical and kinetic equilibrium. Matching its energy to a Bose-Einstein gas
of both complex fields gives Tdark=1.36982 MeV and fixes its entropy. Adiabatic
entropy matching then initializes a Maxwell-Boltzmann moment description at
Tdark=m/2. The visible sector uses constant g*=g*s=106.75, consistent with the
previous diagnostic background but not an accurate late standard-model
entropy history. These choices must not be hidden in a claimed cosmological
prediction.

Within the kinetic run, fast X <-> Phi Phi conversion enforces muX=2muPhi.
The initial decay width exceeds H by 5.78e9. A leading Hartree Phi mass shift
is at most 0.3123 of the small vacuum decay gap throughout the reference run,
so that diagnostic does not close the decay channel on this branch. Initial
linear chemical relaxation at fixed total energy is about 359H. These checks
support the kinetic approximation once its starting bath exists; they do not
prove that coherent fields form it.

## Evolving reactions and temperature

All densities include both charge signs, with zero net charge. Set
alpha=muPhi/T, n=nPhi, nx=nX and W=n+2nx. In the rapid-decay limit,

    nx = K(T) n^2,  K(T)=nx,eq(T)/nPhi,eq(T)^2

for Maxwell-Boltzmann distributions. The pair conversion and direct contact
4-to-2 loss give

    dW/dt + 3H W = -R,
    R = [ (sigma_pair v/2) nx^2 + Ccontact(T) n^4 ]
        * [1-exp(-2 alpha)].

The last factor includes inverse pair conversion and inverse 2-to-4. It
vanishes at chemical equilibrium. The chemical-potential relation and this
forward/reverse statistical ratio also obey the exact Bose detailed-balance
identities; the numerical collision averages here are nevertheless MB
approximations, not full Bose collision integrals.

The temperature is evolved from

    d rho/dt + 3H(rho+P)=0.

For U=rho-mW, the equivalent stable equation is

    dU/dt + 3H(U+P)=mR.

Thus number loss heats the remaining population. Temperature is not forced
to follow a^-2 during the reacting phase, and rest energy is not silently
deleted by a number sink.

The resonant recycling contribution behaves as an effective 4-to-2 coefficient

    Cres(T) = (sigma_pair v/2) K(T)^2.

In the nonrelativistic limit,

    K(T) ~ (1/2)(M/m)^(3/2) [2pi/(mT)]^(3/2) exp[-(M-2m)/T].

This is strongly temperature dependent. It cannot be replaced by the earlier
constant zero-velocity 4-to-2 coefficient while real X formation is active.

## Collision calculation and omissions

The pair cross section is thermally averaged from the exact vacuum tree
amplitude. The direct quartic 4-to-2 kernel is calculated at finite incoming
momenta, with all allowed two-quartic-vertex diagrams for the 31 and 22 charge
channels. Two scrambled Sobol integrations use 16384 and 65536 samples at
each of 25 temperatures, T/m=0.02 to 2. Their largest difference is 4.12%.
Threshold amplitudes, four-momentum conservation and the cold pair limit
pass their checks. Below the table, only the contact kernel's smooth
nonrelativistic limit is used.

Real X reactions are explicit, so no bare X resonance is inserted into an
additional 4-to-2 integral. However, the nonresonant cubic-containing higher
reaction terms and a full real-intermediate-state-subtracted collision
network have not been calculated. In particular, this is not a complete
all-channel quantum evolution of the original action. The direct contact
term is an identified subset of that action, not its complete six-point
amplitude at arbitrary momentum.

The largest Bose occupation diagnostic for the MB trajectory is 0.1565.
At fixed T and chemical potentials, simple pointwise bounds put the Bose
forward/contact correction below 2.393 and the pair correction below 1.388
for this maximum fugacity. These are bounds on those statistical factors,
not certified bounds on the relic after changing the thermodynamics and
collision distributions. Rate-multiplier tests below measure sensitivity;
they do not repair the missing quantum closure.

## Reference conditional survival result

At the kinetic starting point,

    YW,start = 1.2186813e-7.

With pair recycling, direct contact loss and both inverse processes,

    YPhi,final = 7.4090706e-8,
    Yfinal/YW,start = 0.607958,
    Yfinal/Ytarget = 0.169544.

The residual weighted X fraction at the cold endpoint is negligible. Relative
to the hypothetical freely surviving source's initial weighted stock, the
final ratio is 0.126925; that includes the assumed earlier equilibration and
entropy matching. Neither ratio is a measured survival probability of the
original quantum state.

The endpoint has Tdark/m=1e-5. Collisionless redshift thereafter gives an
illustrative rms speed about 1.03e-7 c at visible temperature 0.8 eV, using
the same fixed early g* and late entropy factor 3.91. This remains a conditional
cooling calculation, not a transfer-function or collapse calculation.

| Conditional network | Final yield |
|---|---:|
| Pair recycling + direct contact 4-to-2 | 7.4091e-8 |
| Pair recycling, no direct contact loss | 7.4321e-8 |
| Direct contact loss, no pair conversion | 9.0276e-8 |
| No weighted-number loss | 1.21868e-7 |
| Direct contact coefficient multiplied by 10 | 7.2798e-8 |
| Direct contact coefficient multiplied by 0.1 | 7.4296e-8 |
| Pair coefficient multiplied by 0.5 | 7.7199e-8 |
| Pair coefficient multiplied by 2 | 7.1156e-8 |

Approximately 79% of the integrated post-start loss is through pair recycling
in the reference trajectory. Removing a channel changes the bath history,
so differences between final yields are not an additive channel decomposition.

## Dependence on the unresolved formation history

Moving the assumed energy-to-thermal-bath matching point along the same
free-envelope continuation gives:

| Assumed matching amplitude | Final conditional yield | Fraction of target |
|---|---:|---:|
| 0.010 GeV | 2.6045e-8 | 5.96% |
| 0.003 GeV | 4.5476e-8 | 10.41% |
| 0.001 GeV | 7.4091e-8 | 16.95% |
| 0.0003 GeV | 1.21694e-7 | 27.85% |

This is a sensitivity experiment, not an allowed cosmological parameter range,
a statistical uncertainty interval, or permission to choose the latest
matching point to obtain a desired abundance. In particular a reservoir
cannot be assumed to coast through an efficient reaction regime unchanged.
Its actual matching time, entropy and correlations must be derived.

The high-H normalization itself was selected in earlier work using an
abundance estimate. Its order of magnitude agreement must not be presented
as a parameter-free prediction.

## Independent checks and evidence

- Refining ODE tolerance changes the reference yield by about 5.5e-8 relative.
- A separate finite-decay system approaches the rapid-decay constraint:
  at Gamma_decay/H=10000 its temperature and weighted number agree at one
  expansion e-fold to 4.27e-5 and 1.57e-5 relative, respectively.
- The independent thermodynamic Jacobian check has maximum discrepancy
  6.74e-10. Integrated energy and entropy checks pass, with errors about
  2.26e-6 and 4.67e-7 on the original stored trajectory.
- Without number-changing reactions, weighted number and comoving entropy
  are conserved within the numerical tolerance.
- Exact Bose statistical detailed balance is checked independently for
  decay, pair conversion and 4-to-2 at conserved external energies.

The first entropy audit demanded samplewise monotonicity at 1e-8 despite
ODE relative tolerance 2e-7; it failed on numerical decreases around 1.2e-8.
The preserved version-2 audit instead checks the stable entropy expression,
nonnegative collision entropy production and its integrated balance. The
first channel-loss assessment also failed its integration check because
1201 stored samples underresolved the initial relaxation layer. A dedicated
24001-sample output run was generated without changing the dynamics; the
version-2 assessment uses that trajectory. Failed records are retained.

Current evidence is in `thermal_recycling_rates_run`,
`thermal_recycling_evolution_run`, `thermal_recycling_dense_run`,
`thermal_recycling_anchor0_run`, `thermal_recycling_anchor1_run`,
`thermal_recycling_anchor3_run`, `audit_thermal_recycling_v2_run`, and
`assess_thermal_recycling_v2_run`.

Number-changing heating in a thermally decoupled sector is the established
[cannibal mechanism](https://arxiv.org/abs/1602.04219). The result here is its
specific implementation and the X-recycling channel in this action, not a
claim that cannibalism or resonant conversion is new physics.

The source-to-bath transition, complete quantum collision network and unique
high-H cold abundance remain open. No cold seed was inserted into the fields,
and no conditional relic has been fed into the separate collapse model.

Final provenance verification: all ten new manifests validate against current
inputs. Eight current runs have `completed` status. The original entropy
audit and coarse-output channel assessment remain `failed`. The dense
channel-loss integration agrees with total weighted-number loss to 3.03e-6
relative and assigns 78.574% of that loss to pair recycling. All launched
calculations have finished.
