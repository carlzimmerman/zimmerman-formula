# CCT-003: extended live receiver, pre-run contract

Scope: new dimensionless isolated wave-Poisson candidate, not v3s/L1 and not a four-dwarf fit. Continue CCT-002's failed rotating collapse. Total G=M=1 and eta=.7 are unchanged. Test whether a diffuse part of the SAME wave field gains angular momentum from the inner region before substantial mass escapes. No collision term, artificial friction, controlled mass removal or manual escape switch.

Initial density: (1-f) times the normalized Gaussian with widths (4,2,2), plus f times a spherical Gaussian width 5, f={0,.2,.4}. Multiply density by a smooth compact taper: 1 for r<=10, cos^4[pi(r-10)/4] for 10<r<12, zero outside; normalize total mass. Phase S=exp(-r^2/50)[-.03 r^2/2+.03 xy], common to all f. This is a new matched set; its confined phase differs from CCT-002 and is not claimed as the same initial cloud.

Domain L=32, N=64, dt=.06, T=60; one refinement f=.2 at N=80; one padding f=.2 at L=40,N=80 (same dx=.5). Absorber always r>12, rate .15[(r-12)/4]^4. Record t=30 as an intermediate diagnostic, not a switched action. If initial E>=0 flag initial-bound gate failed; preserve outcome rather than silently changing data. Single numerical thread; measured peak memory must stay <1 GB. Sequential runs, no shared jobs/queues touched, no automation or publication.

Inner region r<3 is a fixed diagnostic aperture, not a fitted dwarf core. At t=0,30,60 and regular snapshots record inner and outer M,Jz; total K,W,E; all absorber changes; full radius profile and half-mass radius. No invariant identity of the original density components is assumed after initialization. A retained outer component is not proven bound by its location in a periodic cube.

Numerical gates: M ledger abs<=1e-8, E ledger rel<=.01, J ledger rel<=.02 of initial total |J|. Refinement and padding compare inner M, J and retained M to 10% relative or .01 absolute tolerance. Failure prevents a converged physical transport claim. No isolated infinity-energy certificate from one padding check.

Exploratory storage target at t=30: inner J decreases and outer J increases in the same sign by >=50% of initial inner J, while cumulative mass removal <=.01146. Formation target at T=60: inner mass >=1.25 initial inner mass; inner specific |J|/M <=.5 initial value; cumulative mass removal <=.01146 (older conditional Sextans stock fraction); final-quarter inner mass varies <=10%. Report all, including cases failing any gate; these thresholds are toy discriminators, not observed dwarf posterior intervals.

Stellar guard: compute the whole-Plummer spherical-tracer virial moment for scales a={.5,1,2,4}: integral G dM/[3a(1+(r/a)^2)^(3/2)], with radial averaging. This is an instantaneous force diagnostic, NOT live stellar heating, a Jeans likelihood or a Fornax/Leo I pass. Coupling remains ordinary Newtonian Poisson; no automatic transfer to AQUAL. The CCT-002 double-counting/coupling gate remains OPEN.

Reproduction: python3 envelope.py --fraction F --tag TAG [--n 80] [--L 40]. Source and inputs pinned in receipt. No heavy cosmological experiment repeated.
