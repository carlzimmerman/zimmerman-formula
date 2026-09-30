# Final saved checkpoint: the one-gap obstruction has a spectrum loophole

Base: 5f1809b2dc4722b6bdaf7c163cceae551bd72329. Research stopped at the user's request to conserve weekly usage. Exact 32pi remains unresolved.

Consider the phenomenological unsubtracted operator −beta M²F(P)/Theta, with no independent U, where

F(P)=sum_i w_i(P²+m_i²)^(3/2), w_i>0, sum_i w_i=1.

Define mu1=sum_i w_i m_i and mu3=sum_i w_i m_i³. The homogeneous lapse equation gives H³=4beta mu3/(9S), S=3lambda−1. The fixed-expansion reduced force law is

b=g−P=beta P sum_i w_i sqrt(P²+m_i²)/(2H).

The strict infrared stiffness is delta=beta mu1/(2H). The asymptotic cubic capacity defines the bare a0,b=2H/beta, Cb=3beta²/4. Hence on the vacuum branch

delta³=(3S/8)Cb (mu1³/mu3).

For one gap the moment ratio is one, reproducing the preceding obstruction. Jensen's inequality gives mu1³<=mu3 for positive normalized weights, but provides no strictly positive lower bound on their ratio. Thus the single-gap lower bound on delta does not hold for every positive spectrum.

## Explicit loophole and its limit

For a light gap epsilon, heavy gap L, and required vacuum moment Q=9SH³/(4beta), choose

w_heavy=(Q−epsilon³)/(L³−epsilon³),

with epsilon³<Q<L³. This exactly fixes mu3=Q. As L→infinity, w_heavy→0, w_heavy L→0, and mu1→epsilon. The vacuum moment stays fixed while the infrared stiffness can be made arbitrarily small by choosing epsilon small. This is an existence construction in the ansatz, not a parameter-selection mechanism or a demonstrated ultraviolet-valid hierarchy.

In the finite window epsilon<<P<<L, the light sector has cubic coefficient beta(1−w_heavy), so a0,light=2H/[beta(1−w_heavy)]. Its MOND window also requires P<<a0,light and P>>w_heavy L/(1−w_heavy). Distinguish this finite-window coefficient from the all-species high-P bare coefficient. No strictly asymptotic infrared MOND exists when every gap is positive.

Illustrative samples use H=1, lambda=2, epsilon=1e−8, L=10000, beta in {2,10,20}. All nine force evaluations at P in {0.001,0.003,0.01} have positive relative correction below 5.7e−5 to the light cubic flux. The bare curvature ratios are 3,75,300, and their finite-window ratios differ slightly through the light weight. These deliberately different ratios demonstrate remaining freedom; no parameter was set to produce 32pi. This tests the reduced flux only, not an observed orbital fit or conserved-source solution.

## Vacuum kinetic term must also be included

The unsubtracted constant F(0)=mu3 contributes −beta M²mu3/Theta. Its quadratic trace term about Theta=3H is −beta M²mu3 (deltaTheta)²/(27H³). Thus lambda_eff=lambda+2beta mu3/(27H³)=lambda+S/6 on the vacuum branch. This differs from the subtracted model in EXPANSION_BRIDGE_GAP_CONES_RESULTS.md, whose constant term vanishes.

Let B_eff=lambda_eff−1 and S_eff=3lambda_eff−1. The local principal scalar kinetic coefficient is 2S_eff/B_eff, and the polarization stiffness gives cs²=delta B_eff/S_eff. Both local signs are positive for lambda>1 and delta>0. This is not full de Sitter, nonlinear, strong-coupling, or causal health. Since S_eff/B_eff>3, identifying this conditional constant-speed cone radius with the bare acceleration radius at Cb=32pi still demands delta>8pi. A spectrum therefore evades the one-gap vacuum bound but does not rescue that particular horizon interpretation. A finite-window radius identification would require its own dictionary.

## Microscopic shape does not fix the normalization

For a free neutral planar Dirac band with negative-energy degeneracy d, speed v, and anticommuting masses m and yP, the filled-sea energy with momentum cutoff K is

E(P)=−d[(v²K²+m²+y²P²)^(3/2)−(m²+y²P²)^(3/2)]/(6pi v²).

After subtracting E(0) and the divergent quadratic term, the finite difference is d[(m²+y²P²)^(3/2)−m³]/(6pi v²). Writing the capacity as d y³/(6pi v²) and gap as m/y, the associated un-subtracted finite vacuum piece is proportional to m³ and independent of y, while the quadratic stiffness is proportional to y²m. This explains how a weakly coupled heavy species can affect vacuum energy much more than polarization. It also exposes the decoupling: this alone does not explain why the two scales have a fixed ratio.

Finite constant and quadratic counterterms remain physical matching inputs. The free-band calculation does not derive the assumed bulk factor M²/Theta, its area density, its vacuum stress, or a protected renormalization prescription. No claim of microscopic completion or novelty is made. SciSpace discovery returned adjacent Dirac vacuum-polarization studies; none was used as proof of the formulas, which are checked directly from the elementary radial integral.

## Evidence and handoff

`expansion_bridge_gap_spectrum.py` passes eighteen exact identities and nine bounded force samples. Contract, input hashes, raw output and validated manifest are saved under `contracts/expansion_bridge_gap_spectrum.json` and `runs/expansion_bridge_gap_spectrum/`. The moment inequality and existence argument are supplied above separately from the finite samples.

The original goal is still missing a physically selected exact coefficient, protected vacuum mechanism, full conserved-source/global matching, complete dynamics and actual observational tests. On resumption, the decisive question is an independent symmetry or microscopic relation fixing the capacity and vacuum moment together. Merely adjusting the heavy weight to match a chosen H or target ratio would be fitting. Preserve the single-gap obstruction with its original scope; the spectrum result narrows its applicability rather than invalidating its algebra.
