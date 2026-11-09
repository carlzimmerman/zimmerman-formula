# EMV1 RESULT (criteria f924165783)

**EMV1: T2 HOLDS / T2 HOLDS** (canonical / alt).

TEST lane, quarantined. Not registered. Relabels nothing: SWT1, WL1, PAPER70, the closure register and fable52_push/README.md
are not edited. Footings never pooled. Every known answer passes on both footings, every Newton solve converged (0 failures),
the mu = 1 twin and the flux-dropped twin both bite, and EMV1.lean compiles with standard axioms only.

## 1. The answer

SWT1's T2 treated each law-on bubble as a linear inclusion around its galaxy's own field. A direct nonlinear solve of one bubble
in a uniform external field, over every external-field level the record has used or measured for KiDS lenses (1.6e-15 to
3.12e-12 m/s^2), moves SWT1's numbers by less than the frozen 20 % line on both footings, and no reading changes side of 0.0354.

| footing | allowance on the filling at the bracket top (SWT1 0.0231) | q_tot L at the top (SWT1) | q_tot NC at the top (SWT1) | field where the first move reaches 20 % |
|---|---|---|---|---|
| canonical | **0.0265 (+0.149)** | **0.265 (-0.125)**, 0.302859; still 7.5 x the line | **0.0168 (-0.068)**, 0.018044; still passes | allowance at **4.16e-12**, 1.33 x the bracket top |
| alt | **0.0259 (+0.123)** | **0.322 (-0.108)**, 0.361214; still 9.1 x the line | **0.0172 (-0.052)**, 0.018177; still passes | allowance at **4.98e-12**, 1.60 x the bracket top |

- At P2's measured catalogue field for GAMA-isolated KiDS lenses (median 6.1e-15 m/s^2, under 0.01 of the wall field) and at
  QX7's primary level (3.96e-13), every reading moves by at most 0.001. The allowance's +0.024 / +0.027 there is not the
  external field: it is the linear alpha_law at the allowance's wall (-0.4869 / -0.4881) against the insulating -1/2 SWT1 used
  for that one number.
- The moves pass 1 % only from about 8e-13 m/s^2 up (P2's "matter" levels and QX7's x8 ceiling, the record's numbers of the
  size the cold component outside the bubbles would add).
- **Direction.** The nonlinear correction makes the bubble a weaker insulator, so it can only ease the conflict: the allowance
  rises and q_C falls. Just below g_ext ~ g_wall it first does the opposite, slightly: alpha_inc deepens by up to 0.004 near
  g_ext / g_wall 0.3-0.6 (visible in the table), so q_tot ticks up by at most +0.005 (NC, canonical, P2's matter median).
- **The conflict does not close.** SWT1 found that law-on down to KiDS's lowest tabulated g_bar needs a filling of 0.29, 12.6 x the
  allowance. With the external field the allowance reaches 0.0265 at the bracket top; the self-consistent reach is 0.450 / 0.447 of
  R_K (SWT1 0.430), g_bar floor 6.8e-15 / 6.9e-15 (SWT1 7.46e-15). Even scanning past the record to g_ext = 7.4e-11 / 9.9e-11
  (0.79 / 0.87 a0) the allowance grows only x5.2 / x5.8, to 0.12 / 0.13.

## 2. What was solved

One bubble of radius R_w around point baryons: div[mu(|grad Phi| / a0) grad Phi] = 4 pi G M_b delta inside, Laplace outside, Phi
and the normal flux continuous at the wall, Phi -> -g_ext z far away. In units of R_w and a0 the problem depends only on
y_w = G M_b / (R_w^2 a0) and e = g_ext / a0. Axisymmetric finite volume in ln r and cos theta (Gauss-Legendre cells), the exact
exterior Dirichlet-to-Neumann map (no truncated outer domain), regular modes at an inner radius where y = 1e6, Newton with a coloured
sparse Jacobian and continuation in e (emv1_solver.py). alpha_tot = p / (R_w^3 g_ext) from the exterior l = 1 coefficient;
alpha_inc = (dp / dg_ext) / R_w^3 from the tangent problem at the converged state. Production grid ds 0.06 x 32 cells in cos theta,
fixed by the known answers before any graded number.

Graded statistic: alpha_inc (the response along the background field, as the task specified) replaces alpha_law on SWT1's 13 GSMF
masses at the L and NC radii (z 1), Maxwell-Garnett as in SWT1, SWT1's form-factor term unchanged; the allowance is
LINE / (-alpha_inc (3 + 2 LINE)) at SWT1's reach wall (g_bar 7.4625e-15). Inputs, radii and GSMF are SWT1's own functions,
loaded read-only; KA0 reproduces its q_tot exactly.

### Table: alpha_tot / alpha_inc against g_ext / g_wall (four KiDS masses at the L and NC wall radii, z 1)

**canonical** (R_w in Mpc and g_wall in m/s^2 under each column)

| g_ext / g_wall | L 9.4 | L 10.45 | L 10.7 | L 10.9 | NC 9.4 | NC 10.45 | NC 10.7 | NC 10.9 |
|---|---|---|---|---|---|---|---|---|
| R_w, g_wall | 0.459, 3.95e-13 | 0.842, 7.23e-13 | 0.973, 8.35e-13 | 1.092, 9.37e-13 | 0.152, 1.20e-12 | 0.341, 1.80e-12 | 0.413, 1.98e-12 | 0.482, 2.14e-12 |
| alpha_law (SWT1) | -0.4938 | -0.4887 | -0.4870 | -0.4854 | -0.4815 | -0.4728 | -0.4702 | -0.4679 |
| 0.01 | -0.4938 / -0.4938 | -0.4887 / -0.4887 | -0.4870 / -0.4870 | -0.4854 / -0.4854 | -0.4815 / -0.4815 | -0.4728 / -0.4728 | -0.4702 / -0.4702 | -0.4679 / -0.4679 |
| 0.0178 | -0.4938 / -0.4938 | -0.4887 / -0.4887 | -0.4870 / -0.4870 | -0.4854 / -0.4854 | -0.4815 / -0.4815 | -0.4728 / -0.4728 | -0.4702 / -0.4702 | -0.4679 / -0.4679 |
| 0.0316 | -0.4938 / -0.4938 | -0.4887 / -0.4887 | -0.4870 / -0.4870 | -0.4854 / -0.4854 | -0.4815 / -0.4815 | -0.4728 / -0.4728 | -0.4702 / -0.4702 | -0.4679 / -0.4679 |
| 0.0562 | -0.4938 / -0.4938 | -0.4887 / -0.4887 | -0.4870 / -0.4870 | -0.4854 / -0.4854 | -0.4815 / -0.4816 | -0.4728 / -0.4728 | -0.4702 / -0.4702 | -0.4679 / -0.4680 |
| 0.1 | -0.4938 / -0.4938 | -0.4887 / -0.4887 | -0.4870 / -0.4870 | -0.4854 / -0.4855 | -0.4816 / -0.4816 | -0.4728 / -0.4729 | -0.4702 / -0.4703 | -0.4680 / -0.4681 |
| 0.178 | -0.4938 / -0.4939 | -0.4887 / -0.4889 | -0.4870 / -0.4872 | -0.4855 / -0.4856 | -0.4816 / -0.4818 | -0.4729 / -0.4732 | -0.4703 / -0.4706 | -0.4681 / -0.4684 |
| 0.316 | -0.4939 / -0.4941 | -0.4889 / -0.4892 | -0.4872 / -0.4876 | -0.4857 / -0.4861 | -0.4818 / -0.4824 | -0.4732 / -0.4741 | -0.4706 / -0.4716 | -0.4684 / -0.4694 |
| 0.562 | -0.4941 / -0.4945 | -0.4892 / -0.4900 | -0.4876 / -0.4885 | -0.4862 / -0.4872 | -0.4825 / -0.4837 | -0.4741 / -0.4760 | -0.4716 / -0.4736 | -0.4694 / -0.4716 |
| 1 | -0.4937 / -0.4914 | -0.4885 / -0.4845 | -0.4868 / -0.4822 | -0.4853 / -0.4801 | -0.4814 / -0.4749 | -0.4726 / -0.4634 | -0.4699 / -0.4600 | -0.4677 / -0.4571 |
| 1.78 | -0.4911 / -0.4841 | -0.4840 / -0.4717 | -0.4816 / -0.4677 | -0.4795 / -0.4640 | -0.4741 / -0.4550 | -0.4624 / -0.4355 | -0.4589 / -0.4299 | -0.4559 / -0.4251 |
| 3.16 | -0.4853 / -0.4719 | -0.4740 / -0.4508 | -0.4702 / -0.4441 | -0.4669 / -0.4381 | -0.4587 / -0.4236 | -0.4411 / -0.3934 | -0.4360 / -0.3850 | -0.4317 / -0.3780 |
| 5.62 | -0.4750 / -0.4518 | -0.4565 / -0.4183 | -0.4506 / -0.4079 | -0.4454 / -0.3989 | -0.4329 / -0.3776 | -0.4070 / -0.3359 | -0.3998 / -0.3249 | -0.3938 / -0.3158 |
| 10 | -0.4578 / -0.4201 | -0.4289 / -0.3706 | -0.4201 / -0.3562 | -0.4125 / -0.3439 | -0.3945 / -0.3161 | -0.3593 / -0.2655 | -0.3501 / -0.2529 | -0.3424 / -0.2428 |

**alt** (R_w in Mpc and g_wall in m/s^2 under each column)

| g_ext / g_wall | L 9.4 | L 10.45 | L 10.7 | L 10.9 | NC 9.4 | NC 10.45 | NC 10.7 | NC 10.9 |
|---|---|---|---|---|---|---|---|---|
| R_w, g_wall | 0.482, 4.14e-13 | 0.882, 7.58e-13 | 1.019, 8.76e-13 | 1.144, 9.82e-13 | 0.152, 1.31e-12 | 0.341, 1.97e-12 | 0.413, 2.17e-12 | 0.482, 2.35e-12 |
| alpha_law (SWT1) | -0.4946 | -0.4901 | -0.4887 | -0.4873 | -0.4832 | -0.4751 | -0.4727 | -0.4707 |
| 0.01 | -0.4946 / -0.4946 | -0.4901 / -0.4901 | -0.4887 / -0.4887 | -0.4873 / -0.4873 | -0.4832 / -0.4832 | -0.4751 / -0.4752 | -0.4728 / -0.4728 | -0.4707 / -0.4707 |
| 0.0178 | -0.4946 / -0.4946 | -0.4901 / -0.4901 | -0.4887 / -0.4887 | -0.4873 / -0.4873 | -0.4832 / -0.4832 | -0.4752 / -0.4752 | -0.4728 / -0.4728 | -0.4707 / -0.4707 |
| 0.0316 | -0.4946 / -0.4946 | -0.4901 / -0.4902 | -0.4887 / -0.4887 | -0.4873 / -0.4873 | -0.4832 / -0.4832 | -0.4752 / -0.4752 | -0.4728 / -0.4728 | -0.4707 / -0.4707 |
| 0.0562 | -0.4946 / -0.4946 | -0.4902 / -0.4902 | -0.4887 / -0.4887 | -0.4873 / -0.4873 | -0.4832 / -0.4832 | -0.4752 / -0.4752 | -0.4728 / -0.4728 | -0.4707 / -0.4707 |
| 0.1 | -0.4946 / -0.4946 | -0.4902 / -0.4902 | -0.4887 / -0.4887 | -0.4873 / -0.4874 | -0.4832 / -0.4832 | -0.4752 / -0.4753 | -0.4728 / -0.4729 | -0.4707 / -0.4708 |
| 0.178 | -0.4946 / -0.4947 | -0.4902 / -0.4903 | -0.4887 / -0.4888 | -0.4874 / -0.4875 | -0.4832 / -0.4834 | -0.4753 / -0.4755 | -0.4729 / -0.4732 | -0.4708 / -0.4711 |
| 0.316 | -0.4947 / -0.4948 | -0.4903 / -0.4906 | -0.4888 / -0.4892 | -0.4875 / -0.4879 | -0.4834 / -0.4840 | -0.4755 / -0.4763 | -0.4732 / -0.4740 | -0.4711 / -0.4720 |
| 0.562 | -0.4949 / -0.4952 | -0.4906 / -0.4913 | -0.4892 / -0.4900 | -0.4879 / -0.4888 | -0.4840 / -0.4852 | -0.4763 / -0.4781 | -0.4741 / -0.4759 | -0.4721 / -0.4741 |
| 1 | -0.4945 / -0.4925 | -0.4900 / -0.4865 | -0.4885 / -0.4844 | -0.4872 / -0.4826 | -0.4830 / -0.4771 | -0.4749 / -0.4665 | -0.4725 / -0.4634 | -0.4705 / -0.4607 |
| 1.78 | -0.4922 / -0.4862 | -0.4860 / -0.4753 | -0.4839 / -0.4717 | -0.4821 / -0.4685 | -0.4764 / -0.4587 | -0.4655 / -0.4406 | -0.4623 / -0.4354 | -0.4596 / -0.4310 |
| 3.16 | -0.4872 / -0.4754 | -0.4772 / -0.4568 | -0.4739 / -0.4507 | -0.4710 / -0.4454 | -0.4621 / -0.4295 | -0.4457 / -0.4012 | -0.4410 / -0.3933 | -0.4370 / -0.3866 |
| 5.62 | -0.4781 / -0.4577 | -0.4617 / -0.4275 | -0.4565 / -0.4181 | -0.4518 / -0.4099 | -0.4380 / -0.3863 | -0.4137 / -0.3464 | -0.4069 / -0.3358 | -0.4012 / -0.3270 |
| 10 | -0.4628 / -0.4292 | -0.4369 / -0.3839 | -0.4288 / -0.3704 | -0.4218 / -0.3589 | -0.4018 / -0.3272 | -0.3682 / -0.2778 | -0.3592 / -0.2653 | -0.3518 / -0.2553 |


Reading the table: at g_ext / g_wall <= 0.1 nothing moves (alpha_tot = alpha_inc = alpha_law to 2e-4). The response weakens from
g_ext ~ g_wall on, faster for the incremental alpha_inc than for alpha_tot, and faster for NC (smaller, denser bubbles) than for L.
At g_ext / g_wall = 10, alpha_inc is -0.34 to -0.43 for L and -0.24 to -0.33 for NC. The bracket's top, 3.12e-12 m/s^2, sits at
g_ext / g_wall 3.2-7.9 for the L walls, 1.3-2.6 for the NC walls and 3.7 (canonical) for the allowance's wall.

## 3. Graded nodes (z 1; moves against SWT1's values)


**canonical**

| record level | g_ext (m/s^2) | alpha_inc at the allowance wall | allowance (move) | q_tot L (move) | q_tot NC (move) |
|---|---|---|---|---|---|
| P2 c10 p16 | 1.618e-15 | -0.4869 | 0.02368 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| P2 lo10 median (no completeness) | 2.398e-15 | -0.4869 | 0.02368 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| P2 c10 median (catalogue field) | 6.143e-15 | -0.4869 | 0.02368 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| P2 c20 median (to 20 Mpc) | 9.935e-15 | -0.4869 | 0.02368 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| P2 c10 p84 | 1.910e-14 | -0.4869 | 0.02368 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| QX7 noclu median e_N 0.0004 | 4.800e-14 | -0.4869 | 0.02368 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| S2 Chae noclu median | 7.314e-14 | -0.4869 | 0.02367 (+0.027) | 0.3029 (+0.000) | 0.01804 (+0.000) |
| P2 bary median | 1.290e-13 | -0.4871 | 0.02367 (+0.027) | 0.3030 (+0.000) | 0.01805 (+0.000) |
| QX7 PRIMARY maxclu median e_N 0.0033 | 3.960e-13 | -0.4883 | 0.02361 (+0.024) | 0.3033 (+0.001) | 0.01807 (+0.001) |
| S2 Chae maxclu median | 6.014e-13 | -0.4869 | 0.02368 (+0.027) | 0.3019 (-0.003) | 0.01809 (+0.003) |
| QX7 maxclu p84 e_N 0.0052 | 6.240e-13 | -0.4865 | 0.02369 (+0.028) | 0.3016 (-0.004) | 0.01810 (+0.003) |
| P2 matter median | 8.212e-13 | -0.4825 | 0.02389 (+0.036) | 0.2989 (-0.013) | 0.01813 (+0.005) |
| P2 matter p84 | 2.553e-12 | -0.4458 | 0.02586 (+0.122) | 0.2726 (-0.100) | 0.01724 (-0.045) |
| QX7 ceiling x8 e_N 0.026 | 3.120e-12 | -0.4351 | 0.02650 (+0.149) | 0.2651 (-0.125) | 0.01682 (-0.068) |

Orientation-averaged alpha_iso at the top node: A_iso 0.02532 (+0.098), L_iso -0.077, NC_iso -0.034

**alt**

| record level | g_ext (m/s^2) | alpha_inc at the allowance wall | allowance (move) | q_tot L (move) | q_tot NC (move) |
|---|---|---|---|---|---|
| P2 c10 p16 | 1.618e-15 | -0.4881 | 0.02362 (+0.024) | 0.3612 (+0.000) | 0.01818 (+0.000) |
| P2 lo10 median (no completeness) | 2.398e-15 | -0.4881 | 0.02362 (+0.024) | 0.3612 (+0.000) | 0.01818 (+0.000) |
| P2 c10 median (catalogue field) | 6.143e-15 | -0.4881 | 0.02362 (+0.024) | 0.3612 (+0.000) | 0.01818 (+0.000) |
| P2 c20 median (to 20 Mpc) | 9.935e-15 | -0.4881 | 0.02362 (+0.024) | 0.3612 (+0.000) | 0.01818 (+0.000) |
| P2 c10 p84 | 1.910e-14 | -0.4881 | 0.02362 (+0.024) | 0.3612 (+0.000) | 0.01818 (+0.000) |
| QX7 noclu median e_N 0.0004 | 4.800e-14 | -0.4881 | 0.02362 (+0.024) | 0.3612 (+0.000) | 0.01818 (+0.000) |
| S2 Chae noclu median | 7.314e-14 | -0.4881 | 0.02362 (+0.024) | 0.3613 (+0.000) | 0.01818 (+0.000) |
| P2 bary median | 1.290e-13 | -0.4882 | 0.02361 (+0.024) | 0.3613 (+0.000) | 0.01818 (+0.000) |
| QX7 PRIMARY maxclu median e_N 0.0033 | 3.960e-13 | -0.4892 | 0.02357 (+0.022) | 0.3617 (+0.001) | 0.01819 (+0.001) |
| S2 Chae maxclu median | 6.014e-13 | -0.4888 | 0.02358 (+0.023) | 0.3605 (-0.002) | 0.01822 (+0.002) |
| QX7 maxclu p84 e_N 0.0052 | 6.240e-13 | -0.4886 | 0.02360 (+0.023) | 0.3603 (-0.003) | 0.01822 (+0.002) |
| P2 matter median | 8.212e-13 | -0.4855 | 0.02375 (+0.030) | 0.3576 (-0.010) | 0.01824 (+0.004) |
| P2 matter p84 | 2.553e-12 | -0.4544 | 0.02537 (+0.100) | 0.3303 (-0.086) | 0.01759 (-0.032) |
| QX7 ceiling x8 e_N 0.026 | 3.120e-12 | -0.4451 | 0.02590 (+0.123) | 0.3223 (-0.108) | 0.01723 (-0.052) |

Orientation-averaged alpha_iso at the top node: A_iso 0.02493 (+0.081), L_iso -0.066, NC_iso -0.025


## 4. Reported (no label rests on these)

- **Field at which each move first reaches 20 %** (scan past the bracket, 8 nodes per decade, log-interpolated):
  canonical allowance 4.16e-12, L 5.02e-12, NC 6.95e-12; alt 4.98e-12, 5.81e-12, 8.21e-12 m/s^2.
- **Orientation average.** The bubble plus centred baryons is isotropic, so a perturbation perpendicular to the background field
  sees alpha_tot, and one along it alpha_inc. With alpha_iso = (alpha_inc + 2 alpha_tot) / 3 the moves at the top node are
  allowance +0.098 / +0.081, L -0.077 / -0.066, NC -0.034 / -0.025; the allowance's 20 % line moves out to 6.45e-12 / 7.83e-12.
  The graded alpha_inc is the larger move.
- **Self-consistent reach** (allowance -> reach -> wall field -> alpha, iterated 5 times): at P2's median 0.434 / 0.433 of R_K,
  at QX7's primary 0.433 / 0.433, at the top 0.450 / 0.447 (SWT1 0.430).
- **Null point.** Along the polar cell column (4 degrees off the axis) the minimum of |g| falls to 0.20 g_wall at g_ext = g_wall
  (r 0.50 R_w), so a near-axis null of the galaxy's and the external field is consistent but not resolved by the grid. KA7 shows the
  regulariser that guards it changes alpha_inc by 8.6e-9.

## 5. Checks

- **Known answers, all PASS on both footings.**
  - KA0: SWT1's z 1 q_tot for L and NC reproduced exactly (relative 0), the allowance 0.0230559 exactly, the bracket against P2's
    JSON to 1.9e-5.
  - KA1: alpha_inc at g_ext / g_wall 0.01 equals SWT1's alpha_law to 2.5e-5 (line 1e-2), for the four KiDS masses at both readings'
    radii and at the allowance's wall.
  - KA2: homogeneous sphere mu 0.1, 0.5, 2 and SWT1's three coated spheres, max error 4.5e-5 (line 2e-3).
  - KA3: no galaxy, e 1e-3 to 1: interior field uniform to 3.6e-3 (line 1e-2); alpha_tot = -1 / (2 + 3 x) and
    alpha_inc = -1 / (2 + 6 x + 3 x^2) to 2.6e-5.
  - KA4: Newton reference, no external field: the solver builds the law, r^2 g / G M_b = nu(y) to 4e-15; exterior effective mass
    exactly M_b; l >= 1 coefficients 1.3e-17 of y_w.
  - KA5: grid doubled in both directions: alpha_inc moves by at most 2.0e-5 (line 2e-3), including g_ext / g_wall = 10 and the
    top bracket node on both footings.
  - KA6: tangent alpha_inc against a central difference of p: 8.1e-7 (line 1e-3).
  - KA7: regulariser x10: 8.6e-9 (line 1e-4).
- **MUTATE, both bite.**
  - M-MU1 (mu = 1 inside; emv1_MUTATE_mu1.*): every alpha below 4.3e-5 in magnitude, KA1, KA2, KA3 and KA4 fail, label NO VERDICT.
  - M-FLUX (dPhi/dr continuous at the wall instead of mu dPhi/dr; emv1_MUTATE_flux.*): the bubble's response is wrong in sign and size (log M_b 10.45, L, canonical: alpha_tot +0.96 and alpha_inc +0.94 at
    g_ext / g_wall 0.01, against alpha_law -0.489; the homogeneous spheres return alpha 4e-5 instead of (mu - 1) / (mu + 2));
    KA1, KA2, KA3 and KA4 fail (KA4: exterior effective mass 2.0 M_b), label NO VERDICT.
- **Lean.** EMV1.lean: 13 theorems, `exit 0`, axioms propext, Classical.choice, Quot.sound only (compile.txt): the homogeneous
  sphere's -1/2 <= alpha <= 0; the uniform nonlinear solution x (mu(x) + 2) = 3 e(x), e strictly increasing (unique solution);
  alpha_tot = -1 / (2 + 3 x); de/dx (HasDerivAt); alpha_inc = -1 / (3 x^2 + 6 x + 2); -1/2 < alpha_tot < alpha_inc < 0; the
  Maxwell-Garnett allowance f <= q / (-alpha (3 + 2 q)) and that it is at least SWT1's q / (3/2 + q). EMV1_MUTATE.lean: five false
  versions, five errors, `exit 1` (compile_MUTATE.txt).

## 6. Limits and disclosures

- **The margin is a factor 1.33 in field (canonical allowance).** The bracket's levels are low-z values applied at z 1 as they stand
  (frozen). Linear-theory peculiar fields at fixed comoving scale are larger at z 1 by about (1 + z) = 2. On that reading the top
  node sits at 6.2e-12 m/s^2 and the allowance and L moves cross 20 % on both footings (from the scan, roughly allowance +30 % /
  +25 %, L -24 % / -21 %; NC stays under), which would read T2 MOVES; no reading changes side and the KiDS conflict stays
  (allowance about 0.030 against the 0.29 needed). The label is on the frozen bracket; this reading is stated, not graded.
- Graded with alpha_inc along the background field, the larger of the two responses; the orientation average moves half to two
  thirds as much.
- One bubble, a sharp wall held fixed, point baryons, a uniform external field. Maxwell-Garnett itself (dilute, non-interacting
  bubbles) is SWT1's and is not re-tested here; nor is SWT1's alpha form for anything but its linearisation.
- Hand estimate before freezing: HOLDS / HOLDS narrowly, allowance +15-17 %, L -11-13 %, NC about -8 %, the 20 % line near
  4-5e-12. The run gave +14.9 / -12.5 / -6.8 % and 4.2e-12 on canonical. The proposer's expectation (alpha between -0.5 and -0.4,
  HOLDS) also matched at the record's levels; past them alpha_inc leaves that range (-0.24 at g_ext / g_wall = 10 for NC).
- Criteria Section 1 said a null point appears once g_ext >~ 0.7 g_wall; the grid shows a near-axis minimum of 0.20 g_wall at
  g_ext = g_wall, not a resolved zero (Section 4).
- Code fix during the lane, disclosed: the first flux-dropped twin run printed alpha_inc = 1.0000 everywhere because the tangent
  problem's e-derivative was set to zero for that arm (under M-FLUX the exterior term is multiplied by mu). It was stopped, the
  derivative is now a central difference for that arm only, and the twin was rerun. The law's path uses the exact analytic
  derivative and its code path is untouched by the fix (KA6 checks that derivative; a spot solve after the fix matches to 1e-12).
  emv1.json and emv1_MUTATE_mu1.* were produced before the fix; the mu = 1 arm does not use the changed branch either.

## 7. What this lane shows and does not show

- It validates SWT1's T2 linearisation where it was used: the allowance f <= 0.0231 and the readings' q_C hold to 15 % or better at
  every external-field level in the record, and to 0.1 % at the measured ones. SWT1's statement that the class "law on in cleared
  regions, component elsewhere" stands or falls on KiDS's points below g_bar about 7.5e-15 against the lensing allowance is unchanged
  (floor 6.8-7.5e-15 across the bracket).
- It grades no mechanism and completes nothing.

## Files

FROZEN_CRITERIA.md (f924165783), emv1_solver.py, emv1.py -> emv1.json / emv1.out, emv1_MUTATE_mu1.json / .out,
emv1_MUTATE_flux.json / .out, EMV1.lean, EMV1_MUTATE.lean, compile.txt, compile_MUTATE.txt. Main run: one thread, 614 s, peak
0.81 GB. Lean compiled with `lake env lean` from the copy of fable_independent_2026/lean_2026 that has its Mathlib build.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
