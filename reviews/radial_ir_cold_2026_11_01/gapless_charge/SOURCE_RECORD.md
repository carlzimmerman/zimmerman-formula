# Source audit, 1 November 2026

Primary tool reads only; no full external sources are copied or downloaded.
All locators below were checked in the actual returned source text. Failed
version-suffixed fetches were retried without a suffix, whose displayed version
is recorded explicitly. No source supports a complete physical lifetime by
itself; model-specific traces and conditions are derived in DERIVATION.md.

| Source | Authenticated locator | Exact use and restriction |
|---|---|---|
| [Martin, hep-ph/0509115v2](https://arxiv.org/pdf/hep-ph/0509115v2),7Oct2005 | §II.A Eq2.19–2.24; §II.C Eq2.44–2.47; §III Eq3.2,3.4,3.6, printedp8 | Scalar Yukawa/gauge conventions, loop normalization, finite chirality flip. Massive vectors are retained at one loop; only its two-loop treatment assumes massless vectors. DR has delta_MS=0. |
| [Giudice–Rattazzi, hep-ph/9801271v2](https://arxiv.org/pdf/hep-ph/9801271v2),19Apr1999 | Eq2.19–2.20, printedp14 | Exact finite-F ordinary chiral messenger benchmark. F_aux=−W_X* in our input convention. Its chiral-messenger formula is not substituted for gauge messengers. |
| [Intriligator–Sudano,1001.5443v2](https://arxiv.org/pdf/1001.5443v2),1Feb2010 | §2.10 Eq2.45–2.49, printedpp17–18; §6.6 Eq6.36 | Gauge messenger masses need not obey chiral logdet screening. Eq2.49 connects heavy R anomaly to gauge kinetic matching. Small-breaking formulas in §6.6 do not replace our finite-F self-energy. |
| [Ellis–Wells,PRD91,075016](https://link.aps.org/accepted/10.1103/PhysRevD.91.075016),22Apr2015, accepted manuscript | §III Eq2–3, printedp5 | Displayed MS heavy vector/physical scalar/fermion threshold weights. Only physical scalars enter. Original Hall matching citation is NPB178(1981)75; its publisher metadata was authenticated, not its inaccessible equation text. |
| [Martin–Vaughn,hep-ph/9308222v2](https://arxiv.org/pdf/hep-ph/9308222),24Jul2008 | Eq2.4, printedp4 | MS/DR gauge coupling conversion cancels the heavy-vector constant in DR at this order. |
| [Martin,Primer v7](https://arxiv.org/pdf/hep-ph/9709356v7),27Jan2016 | Eq6.5.9–6.5.10 | Supersymmetric one-loop beta and gaugino running; specialized here below heavy thresholds. |
| [Gross–Wilczek,PRL30,1343](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.30.1343),25Jun1973 | Publisher record; original article reproduced in [Gross Nobel slides](https://www.nobelprize.org/uploads/2018/06/gross-slides.pdf) | Pure gauge asymptotic freedom. Our one-loop Lambda is a running definition, not a theorem of confinement. |
| [Anber–Sorbo,astro-ph/0606534v2](https://arxiv.org/pdf/astro-ph/0606534),5Oct2006 | Eq7,15–18, printedpp4–5 | Local axion-Maxwell/helicity equations. Flat constant rotation, finite patch and conductivity conditions are derived here; inflationary amplification results are not imported. |
| [Arnold–Son–Yaffe,hep-ph/9810216v1](https://arxiv.org/pdf/hep-ph/9810216),1Oct1998 | Eq1.1–1.2, printedp2, and accompanying high-temperature/plasma assumptions | Nonabelian thermal diffusion scaling alpha^5 T^4 log(1/alpha). Not a T=0 rate; coefficient remains unknown. |
| [Cè et al.,1607.05939](https://arxiv.org/pdf/1607.05939),returned DESY16-131 paper | §2 definition; §4–5 finite-N/continuum susceptibility results | Evidence of nonzero pure-YM susceptibility in the studied theories. No numeric coefficient is imported into the present SU3/SU2 strong-scale estimate. |

The R-anomaly normalization is fixed by a unit topological charge carrying
2T(R) zero modes per charged left Weyl fermion. Tr(q_R T²)=5 therefore gives
Delta Q_R=10, Delta Q_theta=5. Direct raw generator traces independently
check each embedded subgroup; no assumption about an exactly conserved
low-energy global charge enters the calculation.
