# TP03: finite diagrams and current matching

User authorization, 1 November 2026: compute missing finite two-loop diagrams
and kinetic/current matching in weak coupling, and test their effect on the
pressure verdict. Initial shared-checkout revision:
`7b1880de2caded85da4b8c34d84b5dc6c005650e`. Other sessions may advance HEAD.
TP01 and TP02 are immutable scientific inputs; exact dirty versions are hashed
by execution records. This directory owns only new research artifacts.

The microscopic model, canonical real-field normalization, Landau gauge and
supersymmetric DRbar-prime subtraction are the TP02 conventions. Start with
f=1, h=lambda=e, g=sqrt(29/200)e at e=.01,.03. These trial values do not select
a physical coupling or abundance. Retain the original reference-X chart.

Targets: actual finite two-loop vacuum graphs, counted once with the known
heavy-displacement correction; actual finite angular/current coefficients
about the broken-supersymmetry background; and native-phase pressure after
combining terms of the stated order. Partial graph sums are explicitly partial.
Required controls include mass/vertex reconstruction, master-integral limits,
supersymmetric cancellation, scale identities where applicable, and derivative
convergence before interpreting a shifted endpoint. Residual scale dependence
is not a bound on omitted finite graphs. No full physical no-go is presumed.

Ownership: two_loop/ contains scalar and fermion graphs; gauge_diagrams/
contains vector graphs and coordinator controls; master_integrals/ contains
authenticated sunset functions and checks; current_matching/ contains the
finite current calculation. Coordinator owns root records and synthesis.
Subroute contracts precede bounded computations; preserve failures and record
software, hashes, exact commands, domain and exclusions in v2 manifests.

One numerical thread per process; minutes per experiment; below 1 GB where
feasible, reporting measured RSS. Unsupported macOS affinity/address-space
limits are not claimed. No installation, production simulation, queue edits,
Git staging/commit/push or changes to earlier research are authorized by this
contract. Primary-source tool reads are permitted. Complete finite matching,
IR control and state selection remain separate obligations until supplied.
