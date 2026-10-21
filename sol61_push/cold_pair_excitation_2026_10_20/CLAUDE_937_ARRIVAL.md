# CFG937 finalized arrival: a supply-floor clue, with the selector gap still open

Audited 2026-10-20. Read-only examination of committed evidence; no Claude experiment was rerun. Earlier `CLAUDE_ARRIVAL.md` is unchanged. Exact source receipts and the independent arithmetic checks are in `sources_claude_937.json`.

**Result:** CFG937's extra filtering floor can activate cold stock in Draco, but it does not establish a physical rule that concentrates Draco/Sextans while protecting Fornax/Leo I. The finalized primary verdict is **PARTIAL (corner-selectable), FRAGILE**, on each footing; the upper temperature bracket is also only PARTIAL-UPPER (corner-selectable). Choosing a passing corner is a discrete fit under the frozen criteria.

## Revision identity

| Evidence | Exact commit |
|---|---|
| Criteria, committed alone | `73144fddbea9625b33a814d6c2e2062d9018c322` |
| Script, controls and sealed P937 | `a8792e8b4cac71322d67b541ebe2bd69eca3855b` |
| Main results, stdout and README | `d1b1b476f40c65823554b9434a67eb801728be6d` |
| Ledger arrival | `9b3b82aa706ced6a25bd4917bf5c3985afb84178` |

All 14 current CFG937 artifacts equal their corresponding criteria/seal/result commit blobs byte for byte. Current script SHA-256 is `1c8170c771fb193e03dfca1ea516ef899f09d410c41bc0c92f77044ea6e9ed44`, matching the script hash inside P937. The seal SHA-256 is `75987b4250ef246cb7ed65de8835b65fbc51fc70063aa37fe5de8719f557e89e`; main JSON is `ec2bcc65e6476ed38a26884968ace944cd3661c7819638743441f3e751a651e0`. The inherited CFG934 script hash also matches the dependency named in every CFG937 result.

## What the rule actually supplies

H-CF2 assumes primordial cold collisionless matter and NFW halos. A quenched system receives the ordinary atomic-cooling halo floor; a late former receives the larger of that floor and a filtering floor with `V_th = sqrt(2) c_s(T_IGM)`, `mu_f = 0.59`, `T_IGM = 1, 1.5, 2 × 10^4 K`. This uses ordinary gas retention as a halo-selection condition. It is distinct from this packet's alternative charged `Psi/X/chi` matter action and pair evolution. No microscopic coupling, merger rate, mass-unit conversion, action normalization, cold capture or transport law transfers between these models.

For primary reading S, the inherited prescription is

`f_ex = max(0, 1 - M_ph,edge / [(1-f_b) M_floor])`,

`sigma_pred^2 = sigma_law^2 + f_ex × sigma_N,cold-floor^2`.

Reading M is the separate max prescription, rather than an independently derived common gravitational action. `M_floor` in `per_object` is total virial mass; the named-dwarf table's `cold_floor` is `(1-f_b) M_floor`. Those quantities must not be interchanged with each other or with enclosed mass at the stellar radius.

## Four-dwarf implication

**All four targets receive the same late-former label.** Draco, Fornax and Leo I use Weisz+14 SFHs; Sextans uses the `sat-bright median N21` group default. Their total floor masses at the hot end (`T_IGM = 2 × 10^4 K`) are:

| Target | SFH input | `M_floor(tau50)` [solar masses] | `M_floor(tau90)` [solar masses] |
|---|---|---:|---:|
| Draco | own Weisz+14 | 1.1478072e9 | 1.8132770e9 |
| Sextans | group default | 1.9085040e9 | 4.8246839e9 |
| Fornax | own Weisz+14 | 3.1317018e9 | 5.6070297e9 |
| Leo I | own Weisz+14 | 4.1733833e9 | 5.8597782e9 |

These are assumed stocks, not transported core masses or wind budgets. The floor gives Fornax and Leo I larger halos too. Different formation epochs, NFW density and the edge subtraction can change the inner contribution, but the binary selector itself does not favor Draco/Sextans over Fornax/Leo I. Under the own-evidence selector V8, Sextans is placed in Q and loses this extra filtering-floor assignment. This is a directly relevant fragility in the needed Sextans supply.

The named canonical Draco diagnostic has edge phantom `8.1706516e8` solar masses. Its cold-stock `f_ex` at temperatures `1/1.5/2 × 10^4 K` is `0/0/0.155731` using tau50 and `0/0.177201/0.465576` using tau90. Alternate-footing values are respectively `0/0/0.026838` and `0/0.051586/0.383987`. Thus a hotter filtering floor can switch Draco's leftover stock on; that is not a demonstration that the stock settles to the required dense core.

Independent classification of all **864 main class/corner/footing cells** reproduces their labels. Primary S has seven all-class-consistent corners on canonical and six on alternate, with **six common corners**, representing only three `(tau, C, T)` settings repeated at both mu. At those common corners, the intermediate luminosity-bin residual `mean ln(sigma_obs/sigma_pred)` remains **+0.101312 to +0.233865** canonical, **+0.083020 to +0.221694** alternate. At `mu=.59, tau50, C=6000, T=2e4`, it shrinks to +0.081231/+0.089924 while UFDs are overpredicted: residual -0.169382/-0.169267 dex and z -3.407/-3.502. The alternative M reading has eight common passing corners and still leaves intermediate-bin residuals +0.107385…+0.215820 canonical and +0.097782…+0.196378 alternate there. Class-mean consistency does not certify the four individual dwarf guards.

The useful next step remains a physical retention/concentration calculation with separate enclosed masses for all four targets. A higher shared floor alone is insufficient. Any proposed transfer of these floor stocks into the pair-action calculation additionally needs an explicit common mass, time and gravity normalization.

## Controls, sealed prediction and limitations

K reports all checks passing. Independently comparing MUTATE_EQ's saved corner data to CFG934 reproduces **10,224 numbers exactly**, including labels. The frozen oversupply control **MUTATE_T10 fails 231/504 cells**, as reported; independent counts are C 54, M-Collins 48, **M-LVD 6**, SPARC 68, U 20, I 24, L 11. The README's class breakdown omits the six M-LVD failures, although its total is correct. Of the failed cells, 159 have the overprediction sign but do not reach z <= -2. Therefore passing main class labels cannot be treated as powerful over-supply controls at every diffuse-halo corner.

P937 is a model prediction sealed before the main run, rather than a scored new observation. Independently checked all **4,032** `E_L-E_Q` grid differences, **432** bin means and their corner ranges. For matched intermediate-luminosity dwarfs, its primary S late-minus-quenched prediction is +0.059349…+0.366896 ln canonical and +0.041406…+0.326104 alternate. Alternative M reverses the bin-mean sign: -0.524226…-0.016551 and -0.484294…-0.010928. These signs concern the specified bin averaging/templates, not every individual matched size/luminosity cell. The frozen future test requires at least five objects per group and matching within 0.5 mag and 0.15 dex radius; LVD-83 has only three quenched objects and cannot score it now. Its reionization bracket is inert because the SFH grid's first lookback node, 12.589 Gyr, is later than the z=6/8 reionization lookbacks.

CFG940 currently contains only committed criteria (`798e98d78e8019c983bc01e0f94b8cee81478318`) for a faint-rotator discriminator; no local script/results/README were present at inspection. That lane is reserved and was not executed here.

No result above supplies an energy/angular-momentum receiver, survival history, fragmentation/capture mechanism or a four-dwarf mass-budget closure. The meaningful new clue is the narrow supply/overboost tradeoff, especially Sextans' dependence on an imputed SFH, rather than completion of the theory.
