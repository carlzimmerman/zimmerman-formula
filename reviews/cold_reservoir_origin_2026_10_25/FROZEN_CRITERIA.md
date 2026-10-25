# Reservoir-origin routes and pre-execution contract

Base checkpoint: rapid assembly 17f09d804c; current shared HEAD at discovery
4606a03ac9. Work only in this directory. Target: select abundance AND momentum
distribution independently of cluster/galaxy fits; eta itself remains imposed.

R1: test late de Sitter thermal selection, conditional on canonical scalar
quantization m=hbar/eta and an ideal nonrelativistic Bose gas interpretation.
H=1,1.8,3 times 10^-18 s^-1 are external illustrative vacuum scales, not fits.
Calculate the zero-total-chemical-potential Boltzmann density and the saturated
excited-state density, leaving condensate normalization explicit. Check SI
against eliminated-variable formulae. No detector temperature is asserted to
be a real homogeneous material bath; even that extra assumption is tested.

R2: test purely gravitational production in a specified relativistic scalar
completion. Choose conformal coupling 1/6, m=1 in dimensionless units,
a²=2.5+1.5 tanh(s/tau), tau=.1,.5,2; identical in/out vacua and endpoints.
Calculate exact oscillator occupations and compare nine modes (k=.1,1,3)
with direct ODE evolution on [-16 tau,16 tau]. Check Wronskian conservation.
Integrate spectra on k=[0,30] and [0,60]; no physical abundance extrapolation.
Compare normalization and normalized final velocity moments. This expansion
is an externally supplied smooth control, NOT a self-consistent cosmology or
solution of the current nonrelativistic action. Varying tau diagnoses missing
history; it is not a proposed adjustable cosmological parameter.

R3: derive covariant two-component energy bookkeeping with w_v=-1 and
pressureless cold fluid; test exact fixed-ratio identities. Distinguish exact
constant positive vacuum from evolving vacuum. No unaccounted energy injection.

Normal execution: <=60 s, one numerical thread. Mutation drops 2pi in thermal
T only and must fail independent eliminated-variable checks. ODE rtol=2e-10,
atol=2e-12; occupation tolerance 1e-8 relative + 2e-10 absolute;
Wronskian tolerance 2e-8; finite-spectrum convergence relative 1e-7.
No claim of observational success, full uncertainty analysis, all-QG no-go,
or a derived microscopic completion. A surviving mechanism requires a source
kernel from an action plus independently selected cosmological state/history.
