# Restricted clock-band pressure bound for the same repair

This is a separate continuation, not a change to the accepted repair runs. Consider the same perspective B and QGamma compensation, but demand Pi-concavity only on the rectangular domain `1<=Q<=qmax`, `Pi>=0`. It is not a claim for an arbitrary correlated domain Q(Pi).

Write x_max=qmax-1 and `tmax=x_max²/(L² qmax)`. Since t(Q) increases for Q>1,

```text
Bband = sup_(1<=Q<=qmax) B(Q)/Q = CL²[1-exp(-tmax)].
```

The clock-energy fraction is at least `1-exp(-tmax)` for every S>=0. Requiring it to be at most delta at qmax therefore gives `tmax<=a=-log(1-delta)`. The function `f(t)=(1-exp(-t))/t` decreases on t>0 because `f'(t)=[(t+1)exp(-t)-1]/t²<0`. Consequently

```text
Bband = C x_max²/qmax * f(tmax)
      >= C x_max²/qmax * delta/[-log(1-delta)].               (1)
```

No approximation S=0 is needed for this necessary bound. The Q=1 condition still forces Gamma_uu>=0, and concavity throughout the rectangular band forces Gamma_uu>=Bband S'' wherever S''>0. The same finite-u moment argument gives, for u>=u0=(2/3)^(1/3),

```text
p_mean >= Q Bband[3exp(-2/3)-(3u³+1)exp(-u³)].              (2)
```

Original gamma>=0 and the unchanged QX17 W do not weaken this mean-stress bound. A correlated invariant domain that omits qmax at some u values changes the supremum and is not excluded by this argument.

Using the same pinned target inputs and weak clock mapping as the accepted repair calculation gives:

| mu_K (/Mpc) | Minimum K Bband (/Mpc²) | Minimum outer K p_mean (/Mpc²) | Minimum outer pressure/Pi |
|---:|---:|---:|---:|
| 198.25 | 9.66699480529e-8 | 1.48896077566e-7 | .20356854955 |
| 25120 | .00155206493784 | .00239057107226 | 3268.35396696 |

The pressure obstruction remains large for the mu_K=25120 target even after this rectangular clock-band restriction. This bound alone does **not** exclude the lower-mu target. Static integrated-field consequences are owned by the matching lane; no new static background or time evolution is claimed here. The proof, numerical inputs and a fresh bounded v2 execution are separate from the preceding unrestricted-Q repair result.
