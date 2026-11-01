# Cold-state result: adjoint loss established, neutral survivor conditional

The old massive SU3-adjoint fermion gas is microscopically unstable. The
actual full mass-rotated action gives a tree decay into a lighter adjoint
scalar and an unbroken gaugino. A neutral residual-U1 photino is a more
serious cold-state candidate: it has an actual finite-F radiative mass,
an extremely weak derived scalar source, no nonabelian color charge, and
strong perturbative decay selection rules. Its *total* cosmological
lifetime remains conditional on the allowed finite dimension-seven
transition coefficient. A partial Goldstino lifetime is not a survival
proof. No production mechanism or abundance has been derived.

## Actual adjoint widths

The eight degenerate initial fermions and eight light real scalars are
identified from the full gauged spectrum. Projecting the 13 tree-null
Weyl modes onto the exact Goldstino and its gaugino complement gives:

| equal coupling e | parent mass / mu | total tree width / mu | Goldstino component / mu |
|---|---:|---:|---:|
| .01 | .00639800674489 | 7.63474118692e-10 | 6.28455450332e-14 |
| .03 | .0110816727493 | 1.19013836745e-8 | 9.79665093240e-13 |

The gaugino channel accounts for the rest. The total width scales as
e^(5/2) at fixed scaled vacuum, as independently checked between these
couplings. A parent lifetime is hbar/(mu Gammahat), with mu unselected.
This closes the assumption that assigning this fermion a number density
creates a conserved cold species. It does not close all hidden matter.

The light scalar's tree widths to two null fermions or two physical flat
scalars vanish to numerical precision (largest residual width below
6.1e-36 in f=1 units). Its unbroken-vector tree channels vanish by the
generator/vacuum identity. This does not exclude symmetry-allowed loop
decays such as an adjoint-scalar two-gluon invariant. No complete one-loop
scalar decay matching or nonperturbative color-singlet spectrum has been
calculated. A free colored scalar gas is therefore not established.

## Neutral photino and physical pressure

The sibling finite-F pole calculation supplies
mchi/mu=1.11641615058e-4 e^(5/2) at z0. Our repeated derivative stencils
give dln(mchi)/ds=-.99037918 at e=.003. Its actual canonical radial
Yukawa is -2.86534709e-13 at leading weak normalization. The sign follows
the finite threshold derivative; it is not an imposed matter portal.

For the parent's stated conditional mchi=1MeV,e=.003 benchmark, this
means mu=1.81706621e7GeV and leading radial mass .4987787GeV. At local
rho=.3GeV/cm³ and one-dimensional nonrelativistic velocity dispersion
.001, the attractive radial relaxation changes ideal compressibility by
only 7.6071e-55. The rest-energy source was retained. This is a positive
cold-gas response and does not use the circular-phase pressure comparator.
An unpolarized Majorana occupation has zero net axial R charge.
The parent's FD/cosmology computation specifies a conditional distribution;
it remains separate from a production calculation.

The full component tensors verify the transpose involution directly:
X fixed, A/B transpose, gauge vector and gaugino minus transpose. All
relative tensor/Hessian residuals are below 7e-16; the fixed vacuum
residual is below1.3e-14. In perturbation theory this forbids chi1 ->
Goldstino+phase/radial and the otherwise dangerous chi1 Tr(lambda3 F3)
two-body transition. The possible dimension-six three-gaugino final state
is closed: 3 m_lambda3/mchi=1.24484636; SU2 is heavier still. This is not
an authenticated nonperturbative discrete-anomaly or UV-gravity theorem.

The low-energy SUSY Ward matching gives the actual partial width
Gamma_Ggamma=mchi^5/(16pi Ftot²), Ftot=mu²/sqrt31. The primary-source
equations and hypotheses are recorded in DERIVATION.md. At the benchmark,
the partial lifetime is1.16347469e20s. The radial/photino hierarchy gives
mchi²/mrad² about4e-6; the charged physical gap is670467GeV and
mchi/Mcharged=1.49150e-9. No finite-momentum triangle was substituted
for this soft-current theorem, and the gravitational gravitino threshold
must be checked in a chosen embedding.

Allowed three-body transitions chi1 -> lambda3+two gauge bosons remain.
Define their inclusive leading dimension-seven loss by
Gamma3=c7_eff² mchi^7/(256pi³ Mcharged^6), absorbing color sums and form
factors into c7_eff. At the benchmark, c7_eff=1 would give a rate only
2.45153e-16 times Gamma_Ggamma. Equality to that partial width requires
|c7_eff|=6.38678e7; a total lifetime longer than4.355e17s permits
|c7_eff|<1.04196e9 in this normalization. These are **conditional
sufficient budgets, not bounds established on the coefficient**. A
finite-F box/seagull matching or a rigorous inclusive vertex-norm bound
is the fastest remaining microscopic lifetime check. Higher-body
phase/photon radiation is also to be included in a complete loss budget.
Perturbative analyticity and weak-coupling power counting make the
candidate promising; they are not substituted for the numerical bound.

## Radial partial widths

The sibling actual matched radial result gives the unavoidable phase
width. We also evaluated threshold-derivative gaugino-pair couplings at
the finite matched vacua and the leading Goldstino Ward width:

| e | Gamma_phase / mu | summed Gamma_gaugino-pairs / mu | Gamma_GG / mu |
|---|---:|---:|---:|
| .01 | 4.32570639411e-27 | 1.30413480994e-30 | 4.08485620667e-35 |
| .03 | 2.00494552644e-24 | 5.20363120281e-27 | 1.77868697574e-31 |

The computed additional partial widths are .03015% and .25954% of the
phase width. The local scalar coupling is the actual derivative of the
finite-F pole threshold divided by sqrt(2A). This is leading local
matching, not a new full finite-momentum vertex calculation. Possible
radial-to-vector loop decays have not been matched; they can only shorten
the lifetime from the phase partial bound. Sibling Floquet work is
additionally necessary for coherent occupation. Dilute radial quanta and
coherent oscillations are distinct states. Leading weak scalings are
mrad/mu=1.67053393911e-4 e^(3/2), v/mu=7.36714372128 e^(-1/2),
Gamma_phase/mu=4.27206427928e-16 e^(11/2). Their conditional very-weak-e
particle continuation does not select mu or a cosmology.

## Evidence and limitations

`run_002` is the main tree/symmetry/source result:16 numerical checks,
0.984s, measured peak RSS approximately180MB. `run_widths_v2` supplies
four width/budget checks,1.340s, also below1GB. Both use one numerical
thread and175s CPU/180s wall caps. macOS affinity and memory enforcement
are not claimed. The v2 manifests contain exact argv, source/result
hashes, current dirty revision and dependency versions.

`run_001` is preserved: its science checks pass, but its auxiliary charged
gap diagnostic included gauge Goldstones and read zero. Its original
script was left unchanged; `check_decays_v2.py` corrects that diagnostic
and tests positivity. `run_widths` is preserved as a failed run: the
initial guessed <1e-4 dominance threshold was too tight. The measured
ratios are reported above; a separately frozen <1% assertion passes in
`width_budget_v2.py`. No failed result was overwritten or called a pass.
The runner's first preflight rejection (input-list/contract mismatch)
executed no scientific process and created no run evidence.

The exact reproducibility commands are in each manifest; rerun in a new
output directory because evidence directories are append-only. Source
pins and independent review accompany this report. This route computes
actual decays and a derived cold-gas source, but does not establish a
total photino lifetime, a loop-stable scalar, a nonperturbative IR spectrum,
a production history, or a selected dark-energy/dark-matter connection.
