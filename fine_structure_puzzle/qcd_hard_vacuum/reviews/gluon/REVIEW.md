# Independent review of finite gluon matching

The finite heavy-vector operator coefficients pass this source-first review at the stated perturbative order. The sharp-photon conversion passes as a separate leading-power, fixed-order matching statement with the explicitly stated ultraviolet-density and remainder assumptions. A complete physical proton response, a complete next-order hadronic endpoint, unconditioned curved-QCD R, and alpha remain open.

The reviewed author packet is `gluon_matching/DELIVERY.json`, with all 27 files in its hash map checked against their current bytes. `TARGET_PINS.json` records the exact target and source hashes. This reviewer changed only `reviews/gluon/`.

## Independence and primary sources

Before opening the author packet, I queried the existing ignored cache by the exact identifier `arxiv:1812.04100v3`, read the primary PDF-layout extraction, visually checked printed PDF pages 11, 12, 14 and 16, and wrote/pinned `PRETARGET.md` and `SOURCE_CRITICAL.md`. The source-first pins are in `PRETARGET_PINS.json`, timestamped 2026-10-19 18:01:38 UTC. The independent script, rational inputs and contract were frozen at 18:03:06 UTC before their execution and before author inspection. No author code or coefficient JSON was imported into the independent calculation.

Primary source: Stephen P. Martin, *Matching relations for decoupling in the Standard Model at two loops and beyond*, [arXiv:1812.04100v3](https://arxiv.org/pdf/1812.04100v3), PDF cover dated 25 January 2019, SHA-256 `dd48e1f2a843c5cc3c8355511013d45f5995c5cfa2979ea028e1335ac5742f71`. I authenticated the title, author, version stamp and requested formulas from the primary document, and recomputed the PDF hash. The exact PDF equations used are (1.15), (2.1)-(2.3), (2.15)-(2.16), (2.20), (2.26), and (3.1)-(3.3),(3.7). Generic one-loop and mixed mass formulas are PDF (2.20),(2.26); the differing HTML numbering was not used.

After the source-first freeze, I also queried and read A. V. Bednyakov, *On the electroweak contribution to the matching of the strong coupling constant in the SM*, [arXiv:1410.7603v4](https://arxiv.org/pdf/1410.7603v4), cover dated 27 December 2018, SHA-256 `7e0159b6eca069db9605d424c5477d8eadd499c4109246e3f2b87191d5b2d51b`. I inspected its matching prescription, equations (6),(9),(15), pole/gauge checks and Fig. 1 (also visually on printed page 6). Its final pole-top-mass formula was not inserted into Martin's running-mass formula. That would require an explicit additional conversion. No full PDF was copied into the review directory; the existing ignored cache supplied both documents. The cache records have empty author arrays, so PDF title pages, rather than those fields, authenticated authorship. No new network retrieval or external job occurred.

Source authentication, formula extraction and project application are distinct checks. Martin explicitly supplies the finite Standard Model and QCD+QED formulas. The generic canonical massive-vector result is derived here by a hierarchical composition/current projection; it is not a formula quoted verbatim from either source. Neither source's two-loop master integrals, d-dimensional tensor algebra, or counterterm pole cancellations were recalculated in this review.

## Results checked independently

Write `a=1/(16 pi^2)`, `L=log(lambda^2/mu^2)`, with all high-energy MSbar parameters fixed at mu. For fundamental massless active quarks and a conserved canonical Abelian vector, the supported results are

```
delta alpha_s/alpha_s = a^2 e^2 g_s^2 S_Q (2 L-3/2),
delta g_s/g_s         = a^2 e^2 g_s^2 S_Q (L-3/4),
delta m_q/m_q        = a e^2 Q_q^2 (-3 L+5/2)
                      +a^2 e^2 g_s^2 C_F Q_q^2 (-3 L+17/4),
S_Q=sum_active Q_q^2,  T_F=1/2, C_F=4/3.
```

These are truncated operator coefficients, not a complete next-order hadronic prediction. For six active quarks S_Q=5/3; for five S_Q=11/9. There is no additional N_c in the gluon coefficient: its color trace is T_F, and the vector has two equal chiral couplings. Converting the fractional alpha_s coefficient to the fractional g_s coefficient divides by two.

The crucial finite subtraction passes. Let r=W/Z, with fixed g,g',v,h,W,Z, and take y_t to zero with t=y_t^2 v^2/2. The apparent inverse-t terms in F(t,h) and F(t,Z) do not leave a Yukawa remnant: their prefactors cancel at most one inverse t, and the remaining y_t^2 makes them vanish as t log t. This is a formal fixed-order hierarchy, not a numerical unresummed prediction at the physical SM masses. Taking t to zero independently of y_t would be invalid.

After removing the top QED threshold of PDF (3.7), one must also subtract `(4/3) g_s^2 theta_mtop^(1)`: the intermediate squared mass has `ln t_EFT=ln t+2a theta_mtop^(1)`. Inserting it into the one-loop top strong threshold supplies precisely that two-loop term. The independent algebra obtains

```
3 LW+(11/(6r)-11/3+10r/3) LZ+1/2-5r/2-11/(8r)
 = 3(LW-3/4)+(11/(6r)-11/3+10r/3)(LZ-3/4).
```

It checks both cancellation of the top logarithm and the finite terms. A deliberately omitted mass-subtraction control has a nonzero, exactly identified defect. Thus the check is sensitive to the material missing step rather than only the infrared logarithm.

The neutral charge sum and charged-current orientations reproduce the two factors. At this order the colorless vector joins two points on one quark loop; both external-gluon orderings and the self-energy/vertex topologies are included in the source's complete result. Bednyakov Fig. 1 confirms the vector and scalar graph classes. No direct colorless-vector/gluon or vector/ghost vertex exists. Scalar/Goldstone exchanges vanish with Yukawa couplings in the extraction limit. The source's bare-to-renormalized relation includes the required coupling and mass counterterms.

For neutral mass matching, the independent calculation retains the full axial difference term before projecting:

```
theta_m^(1)|neutral
 = -cL cR(3L-5/2)+3/4(cL-cR)^2,
theta_m^(2)|neutral,mixed /(C_F g_s^2)
 = -3cL cR(L-17/12)+(cL-cR)^2(9L/2-15/8).
```

Setting cL=cR=eQ gives the vector result. This was checked for up-type, down-type and charged-lepton source quantum numbers. Treating the whole axial coefficient as the vector coefficient would fail. An additional way to isolate the strong vector coefficient avoids reliance on any axial finite equality: the coefficient of r in the subtracted neutral expression is `(5/3)(2LZ-3/2)`. Only the common Q-dependent vector coupling contributes that highest power; isospin-only and vector-isospin pieces have lower powers. This agrees with the conserved-current/one-loop trace reduction.

The VEV/tadpole convention is material. Martin uses the Landau-gauge effective-potential minimum and omits the summed tadpoles consistently. Its uncharged finite mass terms must be retained until the sequential composition is done. Bednyakov explains the corresponding tadpole/top-mass conversion in his different bookkeeping. Mixing these conventions without conversion is not licensed. For the vector current, longitudinal terms cancel by Ward identities with the current contacts included. The complete source finite parts include evanescent-times-pole effects; no four-dimensional numerator shortcut or beta-function-only argument supplied the finite 3/4, 5/2 or 17/4 here.

## Separate regulator conversion

The massive photon and the sharp O(4) cutoff remain different prescriptions. The author supplies an additional bridge for the declared sharp photon cutoff, with every other line uncut. For a leading-power density B/t, its low-pass filter difference is

```
int_0^infinity dx/x [1/(1+x)-theta(1-x)] = 0.
```

This integral is convergent at both ends and across x=1. In y=log x, my independently frozen calculation checks the opposite, high-pass difference: its zeroth moment is zero and its first moment is `-pi^2/6`. The author's low-pass first moment is consequently `+pi^2/6`; there is no sign discrepancy. Numerical quadrature at 60 digits agrees within 1e-50 with the analytic values. Oddness supplies the exact zeroth moment. The author's v3 absolutely summable geometric-series proof is valid; the retained earlier SymPy complex-branch failures do not change this integral.

For completeness, if `g(t)=B/t+r(t)`, `int_0^T t|r(t)|dt` is finite at fixed T, and the tail is bounded by `C t^(-1-delta) log^p t` for some delta>0, the low-t contribution to the difference is O(1/s). The tail below s is bounded by `(C/s) int_T^s t^(-delta)log^p t dt`, and the tail above s by `Cs int_s^infinity t^(-2-delta)log^p t dt`. Both vanish. This proves the needed transfer under a concrete sufficient remainder condition; the review has not proved that bound for the full nonperturbative QCD proton density.

At the displayed fixed Wilson orders there is only a single logarithm in each heavy-vector matching coefficient. A log(t)/t ultraviolet density would instead generate a higher logarithm under this convolution. Thus the additional constant-density assumption is consistent with the complete fixed-order matching. At higher strong order, running, scalar mixing and logarithmic density terms require new finite transfer moments. The result does not identify the prescriptions to all orders and gives no finite-s numerical error bound. The conserved-current/contact convention must also remain fixed.

## Scalar proton insertion and chiral corollary

The sign and normalization of the gluon insertion pass independently. With `H_g=<p|[G^2]|p>/(2M)`, `gamma_m=-dlnm/dlnmu`, and `Sigma=sum(1+gamma_mq)sigma_q`, dimensional homogeneity and the pure-QCD RG equation give `beta_s partial_g M=-M+Sigma`. Combining this with the trace identity gives `partial_g M=-H_g/(2g)` at fixed renormalized masses. The same sign follows from differentiating the rescaled kinetic term and applying Feynman-Hellmann.

Consequently the author factor

```
B_g=a^2 g_s^2 S_Q <p|[G^2]|p>/(4M^2)
```

gives `f_g(s)=-B_g(L-3/4)`. With `beta_s=-beta0 g_s^3 a`, the trace gives `B_g=-S_Q a/beta0 (1-Sigma/M)+O(g_s^2)`. In the explicitly defined exactly massless three-flavor theory, `S_Q=2/3`, `beta0=9`, and Sigma=0, so

```
B_g=-1/(216 pi^2)+O(alpha_s),
D_ct^g/M at mu=Lambda = -1/(288 pi^2)+O(alpha_s).
```

This is an analytic local subtraction constant in the declared theory. It uses no measured alpha, hadron mass calibration or fitted sigma term. It is not the full proton electromagnetic mass derivative, and choosing a matching point does not retune the original fixed-MSbar path. Physical nonzero quark masses and other active-flavor choices change the scalar trace data and charges.

The author's ADDENDUM correctly limits hadronic power counting. Since H_g scales as 1/g_s^2, the next gluon coupling threshold contributes at the same hadronic order as the known mixed quark term. The latter cannot be advertised as a complete relative-order-g_s^2 proton result without the next gluon coefficient, consistent operator evolution and matrix elements. The leading chiral local constant remains correct with an O(alpha_s) qualification.

## Computation and provenance

There are exactly three v2 manifests in this review directory:

| Run | Status | Content |
| --- | --- | --- |
| run_v1 | completed | 18 exact source/group/composition checks; three quadratures and two symmetry filter checks, 23 total |
| trace_run_v1 | failed | Reviewer diagnostic expected the wrong sign for an unspecified positive next coupling increment; exact code/contract retained |
| trace_run_v2 | completed | 10 canonical action/trace/sign/charge/chiral/order-counting identities |

The failed reviewer control is an expectation error, not a source-coefficient discrepancy. In massless asymptotically free QCD, `partial_g M=-M/beta_s>0`, so an unspecified positive next delta g produces a positive mass change. The v2 control corrects that expected sign and leaves the finite source coefficients unchanged. `TRACE_PRE_RUN_PINS_v2.json` records the correction before execution. All three reviewer manifests validate against current input/output hashes. Both successful runs use wall/CPU/log/thread bounds, without RLIMIT_AS or CPU affinity on macOS.

All three author manifests also validate. Their actual statuses are failed, failed, completed; only run_v3 has the final result file with 16 checks. I inspected the author scripts, contracts, outputs and branch note. They check exact transcribed-source algebra and filter normalization, and do not independently recalculate a Feynman diagram. I did not execute author code or rewrite author results. My independent arithmetic overlaps the algebra while adding full axial decomposition, explicit color/charge checks, a direct beta-log sign control, independent real quadrature of the filter, and separate canonical trace checks.

Outcome: implementation and finite algebraic assertions verified in the stated domain, with source-based perturbative matching supported by the stated topology/current reduction. The sharp conversion is conditional on its distinct regulator/contact and asymptotic assumptions; no nonperturbative tail bound was established. The original physical QCD R/alpha goal is incomplete.

Self-review: mathematical proofreading covered this review, its source-critical note and reproduction instructions. Notation, PDF equation numbers, gamma_m sign, alpha_s versus g_s, canonical matrix-element factors and filter-sign conventions were checked. No mathematical-token change was made to the frozen source-first notes or successful independent input files. The substantive reviewer control correction is preserved in a new version with its failed predecessor, rather than treated as a proofreading edit.
