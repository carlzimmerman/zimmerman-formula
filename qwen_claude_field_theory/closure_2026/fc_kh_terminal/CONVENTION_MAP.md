# CONVENTION_MAP.md — FC-KH terminal run (Phase 1)

Start commit: `750805926eaaa1b0207e3b354d76b12deefcc1cf` (see START_COMMIT.txt). No git touched.

## Sources
- **BB** = Bonetti & Barausse, PRD 91, 084053 (arXiv:1502.05554).
- **Flanagan** = arXiv:2302.14846 (ApJ 958, 2). Full text: `../khronometric_mond/flanagan_2302.14846.txt`.
- Prefactor identity: `M_Pl^2/2 = 1/(16 pi G)`.
- Einstein-aether → khronometric coefficients: `(alpha,beta,lambda) = (c1+c4, c1+c3, c2)`.

## Target action (MISSION.md, verbatim)
```
S_FC = (M_Pl^2/2) ∫ √-g [ R − ((β+3λ)/3) θ² − β σ_{μν}σ^{μν} + f_FC(a) ] + S_m
f_FC(a) = −2Λ + α a² + 2(2−α) a0² [ 1 − (1+a/a0) e^{−a/a0} ]
```
with `a_i = D_i ln N` (khronon acceleration), `y = a/a0`, `θ=K=∇·n`, `σ²=K_ijK^ij−(1/3)K²`.
Branch: **α = 2β**, β>0, λ>0, β≪1. Benchmark P1 = (α,β,λ)=(2e-15, 1e-15, 1e-3).

## ADM reduction (verified symbolically in phase2_symbolic.py, exact identity)
```
−((β+3λ)/3)θ² − β σ²  ≡  −β K_ijK^ij − λ K²
R − β K_ijK^ij − λ K² + f_FC  ≡  ³R + (1−β) K_ijK^ij − (1+λ) K² + f_FC     (ADM: R=³R+K_ijK^ij−K²)
```
So in preferred-foliation ADM (matches MISSION seed / BB):
```
S = ∫ N√γ [ (1−β) K_ijK^ij − (1+λ) K² + ³R + f_FC(a) ]     (overall M_Pl²/2 drops from speed ratios)
```
**Coefficient of `K_ijK^ij` is `(1−β)`.**  ⇒ `c_T² = 1/(1−β)`.

### CRITICAL sign lock (the trap this run had to avoid)
The pre-existing precursor code `../khronometric_mond/wf_adm_scalar_reduction.py` and
`wf_flat_validation.py` write the K-sector as `(1+β_s) K_ijK^ij − (1+λ) K²`.
Matching to the FC-KH `(1−β)` form requires
```
   β_script  =  − β_mission ,     λ_script = λ_mission ,   α_script = α_mission.
```
`wf_flat_validation.py` PROVES this: its Minkowski `c_s²` equals BB Eq.(14) exactly only under
`β → −β_BB`. In THIS run `decisive_reduction.py` is written directly in the `(1−β)` (mission)
convention; the independent cross-check via the script pkl applies `β_script=−β` (phase5, agrees 1e-16).

## Acceleration-function lock (the SECOND trap)
Older precursor scripts used the acceleration term `a0² W(y)`, `W=y²/2+(1+y)e^{−y}−1`
(that is the OLD α=½ model, high-a coupling ½). **FC-KH v1.0 uses `f_FC`, not `a0²W`.** Relation
(verified exactly, phase2 item 10):
```
F(y) := f_FC/a0²  (drop −2Λ)  =  2 y² − 2(2−α) W(y)  =  α y² + 2(2−α)[1−(1+y)e^{−y}]
```
So in any reduction that parametrizes the potential by (value, y-deriv, y²-deriv) = (W0,W1,W2),
the PHYSICAL substitution is `W0=F(y0), W1=F′(y0), W2=F″(y0)`:
```
F(y)  = α y² + 2(2−α)[1−(1+y)e^{−y}]
F′(y) = 2y[α+(2−α)e^{−y}]              (= f'/a0 ; transverse Hessian ∝ F′/y = f'/a > 0 ∀y)
F″(y) = 2α + 2(2−α)(1−y)e^{−y}         (= f''  ; radial Hessian; <0 for 1<y<y*, y*≈31–45)
```

## Interpolation / MOND function (Phase 2, all exact)
```
χ = f'/(2a) = α + (2−α)e^{−y}
μ_phys = (1−χ/2)/(1−α/2) = 1 − e^{−y}     (identically; matches Milgrom/BB ϖ=aμ)
small-a: f → −2Λ + 2a² − (2(2−α)/3) a³/a0     large-a: f → −2Λ + α a²
```

## Constraint constants (BB, transcribed; used in Phase 10 overlay)
```
c_T²  = 1/(1−β)                                            [BB Eq.13]
c_s²  = (α−2)(β+λ) / [α(β−1)(2+β+3λ)]                      [BB Eq.14]   (Minkowski scalar)
α1_PPN = 4(α−2β)/(β−1)                                     [BB Eq.15 / Review Eq.41]
G_N = 2G/(2−α)      G_C = 2G/(2+β+3λ)                       [MISSION Phase 10]
β+λ ≳ 2.5e-7  (20% 1PN gravitomagnetic threshold)          [BB Eq.73]
```
On the branch α=2β: **α1_PPN = 0 identically**, and c_T²=1/(1−β)≈1 — FC-KH is engineered to
pass the GW170817 + solar-PPN pincer that excluded the old α=½ model. The pincer is NOT where
FC-KH fails; the transition-stability sector is (see RESULTS.md / PASS_KILL.md).

## Flanagan no-go, correctly quoted (NOT a kill by itself)
Flanagan's BM (β=λ=0) sufficient conditions: `f'≤0, f''≤0` (Eq.43, no-ghost of h^{ij}) and
`f'≤af''≤0` (Eq.54). He states they "cannot be satisfied for all a" (incompatible with the
Newtonian+deep-MOND boundary conditions), so there is a window a~a0 where they are violated and
"stationary solutions **might** therefore be unstable." Footnote 7: ρ_T0<0 "does **not** imply
the existence of an instability." Discussion: khronometric instabilities "can be cured by the
addition of higher spatial derivative terms." **Hence f''<0 alone is NOT the kill** — the mission
correctly forbids concluding from f''. The decisive object is the FULL β,λ≠0 reduced scalar
gradient speed (STABILITY_OPERATOR.md).
