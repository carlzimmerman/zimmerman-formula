# deepseek_moa — the fork working folder (started 2026-09-16)

Fork of the glm53 track (new chat, per Carl's directive). Read anywhere in the
repo; write ONLY here. Commit and push larger chunks as they land.

## Scope

- Target: closure on the complete theory of gravity on the Zimmerman framework,
  backed by Lean certificates, first-principles chains, and EMPIRICAL closure on
  every piece of evidence (SPARC, X-COP, Gaia, DESI, CMB, clusters).
- Focus: clusters / dark matter / the contradiction ledger. Do NOT re-run
  anything already ruled out (see DEAD.md — the token-economy guardrail).
- The theory being pushed (not rewritten): one scale
  a0 = (c/2) sqrt(G rho_Lambda), kernel mu2 with kappa = 1/2, the equilibrium
  sigma^2 = sqrt(G M_b a0)/2, the phantom rho = sqrt(G M_b a0)/(4 pi G r^2),
  equipartition M_ph(<r_M) = M_b, r_M = sqrt(G M_b/a0), the 2/3 temperature law,
  the Gauss-charge ontology. The equation content is OUR framework; textbook
  math is only a tool.

## Board

| item | status |
|---|---|
| HARVEST.md | surviving identities, certified deaths, live contradictions |
| CONTRADICTIONS.md | the five ranked contradictions + closing conditions |
| DEAD.md | everything killed (never re-attempt) |
| lean/ | Lean certificates (toolchain note inside) |
| M01 | equipartition + Gauss charge — Lean first |
| M02 | cluster amplitude WITHOUT the G059 tautology |
| M03 | static charge assignment — the novel equation |

## Conventions (inherited from the repo)

- Lean: zero sorry; axioms subseteq {propext, Classical.choice, Quot.sound};
  compile via `cd fable_independent_2026/lean_2026 && lake env lean <abs path>`.
- Python lanes: measurement and threshold printed separately; both a0 footings
  (9.3619e-11, 1.1279e-10); write .out first, then commit.
- Append-only record: never delete, never rewrite history.
- No personal data, no absolute machine paths in committed text, no __pycache__,
  no .lake.