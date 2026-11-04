# CW3_cz1_defect_sweep: AMENDMENTS

Each entry is dated and written before it is used. κ = ½ FITTED; not theory closed.

## A1, 2026-11-04, before the amended MUTATE runs: MUTATE for closed-form deep-MOND estimators
Some lanes predict with a ν call in one branch and a closed-form deep-MOND formula in another (for example hunt item 8: σ⁴ = (4/81) G M a0 when the dwarf is not external-field dominated). That formula is ν's deep limit written out, so a ν-only MUTATE leaves MOND in place there.
- Under MUTATE, such a closed-form deep-MOND estimator is also set to its ν ≡ 1 value (the Newtonian estimator of the same script).
- Disclosure: hunt item 8's MUTATE was first run with ν ≡ 1 only. Item 42 (DF2, DF4) then agreed between the two fields (8.5 and 9.5 km/s both). In item 8 every external-field branch gave the Newtonian floor (MW +0.967 both), but M31 read +0.569 with the original field and +0.106 with the Newtonian one. The gap came from the regime switch sending dwarfs to the deep-MOND branch, not from ν. Those first outputs are replaced by the amended MUTATE.

## A2, 2026-11-04, before the triage is labelled: the "named interpolating function" filter
The frozen filter's tokens are `nu(`, `nu_`, `mu(`, `mu_`, `ν`, `μ`, "or a named interpolating function". The names used for the last clause, chosen after a first look at the hits and before any labels: `law_v(`, `rar(`, `g_mond`, `gobs_from`, `mcgaugh(`, `interp_fn`, `simple_interp`, `standard_interp`, and function definitions named `g_obs*`, `gobs*` or `mond*`. They add 24 files to the 1,706 the six tokens select.

## A3, 2026-11-04, before the triage is labelled: how priority-3 rows get a label
- A script (`cw3_triage.py`) reads every ν/μ call in each file. It looks for an external-field name in the call's arguments, and for an observed-field literal anywhere in the file.
- If no ν/μ call in a file carries an external-field name, the row is labelled CORRECT, marked as machine triage. The grep hit was incidental (for example `GE` used for Newton's constant, `eta` for an efficiency, or "EFE" in a string).
- A ν call carrying an external-field name, a μ call carrying one, or an observed literal in the file flags the file. Flagged files are read by hand and get one of the frozen labels. Hand reading goes in priority order: rebuild_2026_10_22, campaign_fresh_gravity, claude_goal_2026_11_03, doors_push and covariant_push, prep_2026, real_research, hunt_2026, then the rest. Any flagged file not read by hand is listed as not read, with no label.
- Limit: a field that reaches ν through a variable with an unrecognised name passes the triage as CORRECT. The table says so.

## A4, 2026-11-04, before the CFG478 and cm14b reruns: the corrected cluster field and the bracket factors
CFG478 and cm14b set the host field from the cluster's measured NFW mass, g_obs = G M_NFW(<R)/R², which is an observed (total) field. Neither lane has a host baryon model, so the corrected field is g_obs inverted through the lane's own ν: solve y ν(y) = g_obs/a0 per kernel (P2, ν_mono) and per footing. CFG478's bracket rows keep their meaning as multipliers on the host field: Q2 = ½ g_Ne, Q3 = ¼ g_Ne. The cluster's true baryon-only Newtonian field is smaller than the inverted value (clusters keep a mass deficit under the law), so the inverted value is the lane-native correction and not a lower bound.

## A5, 2026-11-04, before labelling the modified-inertia rows: how the NOT-QUMOND clause is read
The frozen NOT-QUMOND clause covers modified inertia "or any form whose declared variable is the kinematic (observed) acceleration". Several scripts call themselves modified inertia but apply the record's ν, which the record declares on y = g_bar/a0 (`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md`, framework statement: g_obs = √(g_bar² + g_bar a0)). Others write μ(a/a0) a = g and then feed an observed value in as g.
- If the script applies that ν, or feeds an observed value into the force slot g, the row is labelled DEFECT-Q and marked "MI-named". By the script's own declaration the slot is Newtonian, so in either reading the boost should be ν(y_N) = 1/μ(x_obs), not ν(x_obs).
- If the script's own text makes ν's argument kinematic, or leaves it open, the row is AMBIGUOUS.
- If a form is written in the kinematic variable (μ of the observed acceleration), an observed field is correct and the row is NOT-QUMOND.

## A6, 2026-11-04, before the L? rows are labelled: a taint trace in place of hand reading for files with only a literal
In the triage, class L? means the file holds an observed-field literal but no ν/μ argument carries an external-field name or a variable assigned from that literal. There are 191 such files, too many to read by hand in this lane.
- `cw3_triage.py` runs a taint trace on them. A name assigned from an observed literal is tainted, and so is any name assigned from an expression that holds a tainted name, iterated to a fixed point. An inversion call (`newton_from`, `y_newt_from_obs`, `brentq`, `invert`, and the like) clears the taint.
- An L? file with a tainted name in a ν argument, or in a μ argument where the name was inverted, goes to hand reading.
- The rest are labelled CORRECT, marked as machine triage. The limit stated in A3 applies to them.
