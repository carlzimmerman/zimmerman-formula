# DE00 — INDEX of the directional-EFE programme (deepseek lane; 2026-09-17)

Execution of GAME_PLAN_DIRECTIONAL_EFE.md in the deepseek_push lane (the fable
track runs its own copy in kappa_slot_2026; files here do not collide).
State per lane, with the number that decided it.

| Lane | Status | Deciding number | Verdict |
|---|---|---|---|
| DE01 AQUAL anisotropy table | LANDED 15/16 (C12 FAIL = the finding) | A_phi(mu2,0.5) = -0.1322 at 0.5 r_EFE; CAP beyond (1.03-2.02) r_EFE | THE DECISION RULE FROZEN: AQUAL = 7-15% downstream depression near r_EFE + the directional r_cap; nu_RAR = 0 at all 60 shells (direction-blind); Milgrom's closed form OVERESTIMATES the solver 5-6x (median 87%: linear-EFE form is not a quantitative surrogate -- C12 FAIL-as-finding) |
| DE02 framework decline + floors | LANDED 14/15 | NFW5/framework 0.43 dex; AQUAL vs FW NOT separable | floor law v^2 r -> nu(eta) G M_b certified; the magnitude channel cannot separate AQUAL from the framework |
| DE03 dSph eps_Phi(eta) | LANDED 6/6 | eps_Phi band 0.098-0.170 | the identity (sqrt(1+L)-1)/(sqrt(1+L)+1) certified; AQUAL elongation DECREASES with eta (brief's "growing" phrasing corrected); per-dSph MOND-boosted eta table; L(0.5) fractions mu1=2/3, mu2_reg=8/15 |
| DE04 sample audit | LANDED 4/4 | max eta_env = 0.019; median R_out/r_EFE = 0.256 | THE PLAN'S PREMISE IS FALSE: zero SPARC galaxies at eta >= 0.3; direction test underpowered by construction on the environmental channel; re-points to MOND-boosted satellite/cluster channels |
| DE05 direction regression | REDIRECTED (blocked by DE04) | n/a | ENVIRONMENTAL channel blind; the direction test lives in DE07/DE09/DE08 |
| DE06 magnitude floor | SUBSUMED by DE02 + DE08 | NFW5 separates 0.43 dex | decision bar defined; the LMC is the strongest resolvable eta |
| DE07 wide-binary angular | LANDED 9/9 | split +0.0068+-0.0106 p=0.522; widest -1.7σ | ABSENT at DR3 (direction-blind survives); N_need ~ 8000 vs 372 in-repo; the A=+2.95 prior is a different statistic, not reproduced |
| DE08 extreme-eta (LMC) | LANDED 4/4 | M_dyn/M_b measured 4.86 vs cap 1.14 (z=1.9) | DISPUTED-ON-THE-DUST: the strongest resolvable eta shows no turnover (against the cap) but the free-dust class is the registered escape; separation 4.4x in one object |
| DE09 dSph alignment | LANDED 3/3 | chi2 p=0.50, KS p=0.21, n=59 | DIRECTION-BLIND SURVIVES: MW dwarf PAs uniform vs the GC bearing; AQUAL's eps_Phi ~ 0.15 absent |
| DE10 lopsided HI | OPEN (no WHISP in-repo) | — | spec'd: same statistic on the HI m=1 phase; data not on disk |

Headline: the plan's data premise (Chae+21 environmental eta >= 0.3 for SPARC)
is FALSE on the archival record (max 0.019), SPARC curves never enter the EFE
zone (median R_out/r_EFE = 0.256) -- the direction test lives in the MOND-
boosted channels (MW satellites eta ~ 0.3-1.2, Virgo spirals eta ~ 0.4-1.7),
and on the two channels scoreable today (wide binaries DE07, dSph shapes
DE09) the direction-blind rule SURVIVES; the extreme-eta rotator (LMC) shows
no turnover (against the cap, suspended on the dust).

Timeline log:
- T+0   DE04 built + landed (premise audit) and the plan re-pointed.
- T+10m DE09 built + landed (dSph alignment; first execution of the
         direction-blind test on real satellite shapes).
- T+15m DE07 landed (wide-binary re-run; ABSENT at DR3).
- T+20m DE08 built + landed (LMC extreme-eta; the honest FAIL-as-finding).
- T+25m DE02 landed (floor law theorem; magnitude channel blind to AQUAL-vs-FW).
- T+30m DE00_INDEX written; DE01/DE03 in flight (subagents, steered).