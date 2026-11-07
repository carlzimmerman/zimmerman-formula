# Handoff to the field-equations chat, 2026-11-06: how to get closure, and how to swing it

Read first: closure_2026_11_05/CLOSURE.md, closure_2026_11_06/CLOSURE_FINAL.md,
closure_2026_11_06/ALL_GATES_NOGO_2026_11_06.md, closure_2026_11_06/EQUATIONS_IN_ORDER.md,
and the QX17/QX17C field-equation and FD-solver records. Kappa = 1/2 FITTED; not theory closed.

## The one-sentence seed

Gravity carries one extra scale, a0 = (1/2) c sqrt(G rho_DE), realised by the v3s screened khronon
action; it passes every static gate from Cassini through isolated discs, lensing and c_T, and
underfills every hot pressure-supported system by an amount that varies a hundredfold between
classes (groups ~1, clusters ~4, Coma UDGs ~80 in units of the baryons), so no single switch keyed
to any host property can close the triangle, and the probable finish is the deposited scoped law
plus per-class systematics, with exactly one physics class still unlabelled: a non-isentropic,
shock-sourced sector (QX13 left it unproved).

Closure means every door has a verdict (owner rule 11-04). It does not mean every door passes.
Adopt nothing. The owner adopts.

## Doors still without a label

| Door | Why it is open | Lane below |
|---|---|---|
| Non-isentropic, shock-sourced sector | QX12 killed every isentropic and fixed-temperature sea; QX13 proved the isentropic shock class fails and wrote "non-isentropic K(r) not proved" | SE1 |
| Hot-system step as several systematics | ST1 labelled MULTI-CAUSE IN PART: ellipticals and KiDS explained by IMF; bright M31 dSphs and Coma UDGs NOT EXPLAINED | SE2 |
| Closure statement with the field equations in it | PAPER68 printed action has a misprint (Legendre form needed); PAPER69 has no covariant field equations | SE3 |

Everything else in CLOSURE_FINAL.md already carries a label. Do not reopen a labelled door unless
a new forced input appears (owner rule 11-04: test lanes may reopen, adopt nothing).

## Lane SE1: shock-entropy sector (the last physics class)

Analysis and FROZEN CRITERIA first, committed before any script or number (rule). Then build.

1. Variable. Add one scalar s to the khronon sector: entropy per unit of the sector's rest mass.
   Transport: nabla_mu (rho_x s u^mu) = Sigma >= 0, with Sigma the Rankine-Hugoniot entropy jump
   across shocks of the sector's own flow and zero for smooth flow. In a disc built by smooth
   accretion s stays at its primordial value; in anything virialised by mergers s is set by the
   host's virial shocks. This is the only key in the record that tracks virialisation without
   being a particle mass, a fixed temperature, or a cold fluid (ALL_GATES_NOGO section 3).
2. Action. Write it as a term in the v3s/AC2q action, not as a posited profile (rule: derive the
   observable from the action). Candidates to grade, in order: (a) K(Q, s) = mu_K^2 (Q - 1)^2 g(s)
   with g(0) = 0 and g monotone; (b) the sector's equation of state P(rho_x, s) non-barotropic with
   the a0 law unchanged. Derive the covariant field equations with the QX17 machinery and certify
   them the same way (sympy EL, Lean twin, FD solver on KNOWN and on the Sun).
3. Inputs. Where the per-class shock history is not on disk, BUILD it from the record's own numbers
   (owner 11-04 "swing harder": never stop at NOT EVALUABLE when the natural inputs can be built):
   X-COP and group virial temperatures already used by QX12/QX13; dSph tidal-shock histories from
   the ST1 tau cut; UDG histories from CFG948. Freeze the built inputs with their error bars before
   grading. Raw data or framework-native only; no LCDM inputs.
4. Gates. GB1 G1-G9, read-only, both footings, every line unchanged. Targets are KD1's f table:
   discs <= 0.33 / 0.19, X-COP ~4.2 / 3.8, groups 1.2-3.5 / 0.9-2.9, X-ray ellipticals ~0.9 / 0.8
   (half is IMF, QX26), dSph ~1.7 / 1.3, Coma UDGs ~80, CMB cold at z 3400 (w <= 0.01) with
   lensing chi^2 <= 18.5 at L <= 400. Growth for the class is owed (QX12 left it ungraded): run the
   linear growth with the sector's s(z) from the same transport equation.
5. Controls. KA: reproduce KD1, GB1 L0, QX13 to 0. MUTATE: (i) s set by host temperature instead
   of shocks must reproduce QX12's fixed-temperature failure; (ii) Sigma sign flipped must fail
   G1; (iii) g(s) constant must give back KD1 (f_cap 4.1 in discs, FAIL).
6. Label. PASS all gates, FAIL with the gate named, or NO VERDICT with the bracket. If the needed
   g(s) differs between classes at the same s, the label is FAIL by the no-tuning rule and the
   class is closed: write that into ALL_GATES_NOGO as a fourth wall.

Expected outcome, stated in advance: most likely FAIL, because a hundredfold spread in needed
amount is hard for any monotone g(s) to carry. A FAIL here closes the last physics class and is
the result. Verify a fail as hard as a win.

## Lane SE2: the step as systematics (the probable finish)

ST1 graded each class at the favourable edge, one systematic at a time. Finish it jointly.

1. Freeze, before touching data, an equilibrium admissibility criterion for pressure-supported
   dwarfs and UDGs (tidal radius vs half-light radius, crossing time vs orbital time, the ST1
   tau < 0.375 cut as one candidate). It applies symmetrically: it removes systems that pass the
   law as well as systems that fail it. Removing a system makes it NOT A TEST, not a pass.
2. Grade the full systematic budget as a joint likelihood per class (IMF bracket, distance,
   anisotropy, gas, membership, tides), not each knob at its edge. Report the posterior step per
   class on both footings.
3. Label each class: EXPLAINED (step consistent with zero inside the joint budget), NOT EXPLAINED
   (step excluded), or NOT A TEST (fails admissibility). Coma UDGs at 6.4-6.8 sigma_stat with
   every knob favourable will most likely stay NOT EXPLAINED; say so plainly.
4. Controls. KA: reproduce ST1's numbers to 0. MUTATE: inverted IMF bracket must bite.

## Lane SE3: the closure statement

After SE1 and SE2 carry labels, write one document: the action in Legendre form (fixing the
PAPER68 misprint), the certified covariant field equations (QX17 v3s + AC2q), the a0 law, every
gate with its label in one table, the f table, the three (or four) walls, and the seed sentence
above as the abstract. Deposit as PAPER69 v1.2 or PAPER70 only after build && verify && publish
passes; the owner holds the deposit.

## Standing rules that bind every lane here

- Own terms. Both footings (canonical and alt). Kappa = 1/2 stays FITTED. Never "theory closed".
- Frozen criteria committed before any script or number. Lane ids SE1-SE3 are checked free; do
  `ls` and `git log` before writing, and take no other id without asking.
- Raw data or framework-native inputs only. No Planck 5.364, no LCDM background, no "passes by
  construction".
- Every number from a committed script with its JSON; margins read from the JSON.
- Commit with explicit paths only (shared index). Push each lane as it lands.
- No personal names or private communications in committed files.
- Heavy compute preemptible; nothing above 1 GB RSS while a 1024^3 run is live.
- Adopt nothing. Write the label and stop.
