# SA1 REDUCTION: "settling-age dependence of the cold component" reduces to cells already closed. No lane run.

Lane named by the owner 2026-11-08. First deliverable was to decide whether the hypothesis is new before freezing
anything. It is not new: it splits into cells the record has already closed, both footings, with KA and MUTATE. No
criteria were frozen, no script was written, no number was graded. Synthesis from the record only. Adopts nothing.
The component is cold dark energy (v3s's K(Q) dust); there is no particle.

## The hypothesis

The action's cold component (K(Q) = mu_K^2 (Q - 1)^2) responds to the khronon in a way that depends on how long a
system has been dynamically settled: old, cold, rotation-supported galaxies expelled it or never captured it; young,
hot, still-merging clusters still hold or accrete it. It would connect F1 (CMB 5.41 x baryons), F2 (galaxies hold
none) and F3 (clusters 4.2 / 3.8, cored, smooth, collisionless).

## Step 1: is there a term in the action for it? No (NO TERM IN ACTION)

- K depends on Q alone, the local clock rate. The certified field equations (QX17, QX17D: sympy residuals <= 7e-40,
  Lean twins) are second order and local in time. No field or constant in S records elapsed time since a system
  virialised. The dust's flow is the khronon normal, which is hypersurface-orthogonal, so its vorticity is zero
  everywhere (DX1 D2): it cannot tell a rotation-supported host from a pressure-supported one by its own flow.
- So "settling age" can enter only through the dust's present state (captured or not, how hot, where), i.e. through
  its history of capture and energy input. Each route is a closed cell (step 2).

## Step 2: every route is a closed cell

| Route by which age could act | Cell that already graded it | Verdict on record |
|---|---|---|
| Never captured by old systems: capture depends on age | KD1 capture; KQ1 (a3a5efb25d) | Capture at turnaround is history-blind: f_cap 4.11 in every class (DX1 D4). The K(Q) dust itself is captured at 4.11 even at the closest stiffness (KQ1). |
| Never captured: hot early, cold late | HC1 / EW4 (wall 3); QX7 iter_4 time-dependent Jeans window -> CE2 | Hot enough to stay out of galaxies today = too hot at z 1100 (CMB lensing chi^2 166-194). Time-dependent Jeans window: KX1 + CE2 (29cbfdbb95) FAIL every cell. |
| Never captured: born only at the nodes | NC2 (47c50d2827), NC4 | CMB bias tolerance 0.997-1.001; forest <= 0.13-0.28 % clumped. FAIL. |
| Expelled after settling, above escape | Cell A (L321-L390), CK1 (8e171a71a8) | Law escape speeds 740-1480 km/s keep a 500-650 km/s carrier in massive spirals; the kick that empties galaxies puffs X-COP. FAIL every v_k, both footings. |
| Expelled / puffed after settling, below escape (late heating, dark-energy era) | Cell B: QX10, KX1 (6e1b777482), CE2 | Bound halo excluded by KiDS once kSZ gas is drawn; evaporated form C3 fails X-COP +0.324 / +0.287, groups, Bullet. FAIL. |
| Expelled by the system's own settling (feedback, contraction) | DX1 D4 (disc formation history) | DEAD: contraction pulls it in (wrong sign); expulsion needs 5-23 % of all SN energy coupled through gravity alone, and the ordering is inverted (gas-poor spheroids had the most feedback and need the component). |
| A key on the host's age or assembly history | FA3 I3 (formation-epoch z_f) and I4 (conserved merger charge, N_eff) | I3: z_f built (SPARC 12.1, X-COP 3.70, groups 1.87); moves offsets <= 0.04 dex, wrong sign; FAIL G2-G7. I4 is the dynamical-age proxy: SPARC passes only at N_eff = 1, and with the history left free X-COP and groups still fail their scatter. FAIL. |
| A key on a state that correlates with age (sigma, depth, environment, residual surface) | HX1, EV1, SE1, RS3, QX20 | Every local key dead; the step sits at fixed local M_b, g_N, depth, r/r_M, f_gas (QX20). |
| Any switch at all, perfect, reading a class tag | DX1 oracle O1/O2 | A perfect "settled discs off, everything else on" oracle passes X-COP but fails groups, ellipticals, dSphs, Coma UDGs and KiDS early, both footings. |

## Step 3: the age ordering is contradicted by the needs themselves

DX1's needed amounts by class (under the law, before SE2): ellipticals 0.86 / 0.77, dSphs 1.3-1.8, groups 0.9-3.5,
X-COP 4.2 / 3.8, Coma UDGs 78-86, discs 0. After SE2's joint systematics the residue that stands is X-COP +0.440 /
+0.408 dex, groups +0.232 / +0.194, Coma UDGs +1.120 / +1.075. The Coma UDGs are old, quenched, dynamically settled
systems, and they carry the largest need in the record. So "settled -> none" is broken by the record's own classes,
not only by the mechanism. NC3 is consistent with a per-galaxy reading (members as clean as field galaxies), but that
does not rescue the UDGs.

## Conclusion

SA1 reduces to the closed cells above: NO TERM IN ACTION (step 1), and every route through which a settling age could
act is a frozen FAIL or DEAD on both footings (step 2: DX1 D4, KD1/KQ1, HC1, CE2/KX1, NC2/NC4, CK1, FA3 I3/I4, DX1
oracle). A settling-age lane would re-run those cells. Per the brief, the lane stops here. What would reopen it: a new
term in the action that carries a clock of the host's dynamical state (not of the local field) and that comes with
its own field equations; none exists in the record.

Kappa = 1/2 FITTED; not theory closed.
