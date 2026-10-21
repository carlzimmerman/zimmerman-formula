# MUTATE — A23

## What is mutated

`aqual_efe(..., mut=True)` evaluates the kernel on the field with the external part removed,
$\mu(|\nabla\Phi-e\hat z|)$, while the boundary condition still carries $e$. That is precisely
the **no-EFE reading**: the external field is present at infinity but never enters the
nonlinearity. It is the premise the original tasking assumed and that A24 refuted.

Run: `python3 a23_checks.py --mutate` (writes `a23_MUTATE.out`,
`a23_results_MUTATE.json`; must exit non-zero).

## What must break, and does

The mutation must destroy exactly the checks that measure the EFE. It leaves the amplitude
ladder, the depth conversion and the lensing forecast untouched (they are $e=0$ quantities),
which is the point: a solver that has no EFE still reproduces A13's amplitude.

| check | healthy | mutated |
|---|---|---|
| K8 EFE monotone, $S(0.3)/S(0)<0.10$ | PASS 0.641 / **0.050** | **FAIL 0.977 / 0.977** |
| K9 dip absent at $e\ge0.68$ | PASS $S_{0.6}(1)=0$, $C(0.2d,1)=+0.2157$ | **FAIL $S_{0.6}(1)=-0.2284$, $C(0.2d,1)=-0.3805$** |
| K10 half-vs-full at $e=0.3$ | PASS 0.746 vs 0.050 | **FAIL 0.746 vs 0.977** |
| K12 survey requirement $e_{\rm req}<0.30$ | PASS 0.22/0.21/0.24 | **FAIL none (curve never reaches $f_{\rm req}$)** |

Recorded output:

```
K8 FAIL S(0.3)/S0=0.977, S(0.3)/S0=0.977 monotone, S(low)>0.5, S(0.3)<0.10
K9 FAIL S_0.6(1)=-2.3e-01, C(0.2d,1)=-0.380, S_0.6(0.68)=-2.3e-01 no negative midplane column and positive 0.2d density for e>=0.68
K10 FAIL half=0.746, full=0.977 half > 0.60 AND full < 0.10
K12 FAIL e_req=LSST:none, Euclid:none, Roman:none; f_req=0.21, 0.22, 0.16 all e_req < 0.30 and f_req > 0.15
A23 COMPLETE: 8/12 checks PASS.
```

Mutated EFE table:

```
e=0.00  S_0.6=-0.179259  C(0.2d)=-0.2362
e=0.30  S_0.6=-0.175200  C(0.2d)=-0.2489
e=1.00  S_0.6=-0.228447  C(0.2d)=-0.3805
retained column S_0.6(e)/S_0.6(0): 0:1.000  0.3:0.977  1:1.274
```

The mutated dip is not suppressed at all (0.977 at $e=0.3$) and is slightly *deeper* at
$e=1$ — the boundary field alone, with no kernel response, cannot fill the saddle. That is
the signature of the refuted no-EFE reading, and it is why K8–K10 are the checks with teeth.

## What the mutation shows about the real run

The healthy run's EFE (0.641 / 0.050 / 0.000) is therefore not a numerical artefact of the
boundary condition: removing $e$ from the kernel changes the answer by a factor 20 at
$e=0.3$ while leaving every $e=0$ number bit-identical. The EFE is carried by
$\mu(|\nabla\Phi|)$, exactly as the symbolic check K1 says.