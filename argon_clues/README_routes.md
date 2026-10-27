# Ten proposed routes to kappa = 1/2 / 32pi — audit (`audit_ten_routes.py`)

Result: every route's **arithmetic** checks (chi(S^4)=2, 32pi^2 = 3 pi Z^2, <cos>=1/2, mu_fw quadratic, 1/2 * 1/(4pi)^2), but **none derives kappa**. Each either (a) restates kappa=1/2 / Z^2=32pi/3 as a factorisation chosen after the fact, or (b) fails on dimensions/structure.

| # | verdict | why |
|---|---|---|
| 1 Moyal | dead | a0 has no hbar; hbar/2 cannot set a classical coefficient |
| 2 Komar | no | real 1/2 in M normalisation, absorbed in G |
| 3 free-energy | no | rescaling a0 IS the kappa freedom; the "4" in sqrt(1+4x^2) is shape, not kappa |
| 4 hemisphere | unmotivated | <cos>=1/2 is true, but solid-angle vs flux weighting and 2pi vs 4pi give other numbers; no derivation that a0 is this average |
| 5 Kramers-Kronig | no | half-residue is generic; no pole at H_Lambda derived |
| 6 S^4 -> B^3 | numerology | divide by pi and 3 picked to reach 32pi/3; 32pi^2 = (2pi)^2*2!*4 is one of many factorisations |
| 7 Seeley-DeWitt | no | 1/(32pi^2) is a loop normalisation, no link to acceleration |
| 8 Brown-York | circular | rho_DE/4 is a0^2 = c^2 G rho/4 with kappa already in |
| 9 instanton | numerology | Vol(S^4) is R^4, a0 needs R^-1; extra /pi ad hoc |
| 10 Wald/MM | no | the 32pi is the MM normalisation of the 1/16piG EH term; it is not the 32pi in a0 |

Also: the pasted claim "32pi^2 = MM topological divisor / pi" is exactly the kind of Z^2 integer/pi numerology the repo retracted; and kappa=1/2 vs Milgrom's 1/(2pi) is footing-conditional (kappa_closure/, project memory).
Prior art: `sonnet55_push/puzzle_32pi/` (12 lanes + audit, no derivation) already covers Komar, Brown-York, Seeley-DeWitt, hemisphere, instanton (p10), Kramers-Kronig (`real_research/papers/DESITTER_UNRUH_A0_NOGO_2026.md`). Moyal, Wald and the worldline-instanton route were not found as dedicated scripts — all three fail on the structural points above.

kappa stays FITTED. Not "theory closed".
