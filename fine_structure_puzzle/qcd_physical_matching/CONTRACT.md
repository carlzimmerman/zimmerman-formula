# FSP-006: physical QCD/QED response and proton matching

Parent FSP-005. The original TARGET.md is unchanged. Charge is canonical Thomson charge, alpha=e^2/(4 pi). No measured-alpha or cosmological normalization fit is permitted. Primary-source data may be used only with all calibration inputs exposed; a physical-point extraction is not a no-input prediction.

The requested object remains R(alpha)=A_rho(alpha)/m_p(alpha)^3, with rho(H)-rho(0)=A_rho H+o(H) in one specified state, regulator, and parameter path. The full nonperturbative stress coefficient, a current insertion and a proton self-energy are distinct objects.

## Executed portfolio

1. Proton/Compton: obtain the complete individual proton electromagnetic response from QCD current insertions or forward Compton matching; test whether subtraction/isoscalar terms are independently calculable rather than fitted. Owner proton_compton; write scope proton_compton/.
2. Physical vacuum: attack the global small-curvature QCD/QED response using actual QCD Ward identities, topology and primary nonperturbative evidence. Seek a decisive computable quantity beyond the earlier conditional local-gap argument. Owner vacuum_response; write scope vacuum_response/.
3. Matching path: derive the fully constrained ratio/current insertion, including quark mass and strong coupling retuning. Test whether holding a finite-volume proton mass fixed generates an apparent linear vacuum term and whether consistent flat subtraction removes it. Owner matching_path; write scope matching_path/.

Coordinator owns coordinator/, reviews/, this contract, and shared navigation. Agents must preserve prior files, record exact input hashes and primary sources, execute the cheapest decisive calculation, and distinguish operator identities from evaluated QCD matrix elements. Discriminators are an evaluated physical response with declared inputs, an exact cancellation, or an explicit independent observable obstructing the cancellation. Merely renaming the unknown function is not progress.

Numerical toy models, derivative expansions and finite-volume geometry changes must be labeled. No large external compute jobs, new dependencies, Git mutation or publication are authorized by this package. All three routes stay open if a concrete plausible next calculation remains.
