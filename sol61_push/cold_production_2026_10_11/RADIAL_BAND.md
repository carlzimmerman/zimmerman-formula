# Radial fragmentation screen

2026-10-11. Same action and exact background as [LINEAR_BAND.md](LINEAR_BAND.md).
This checks an omitted physical channel in [ENVELOPE.md](ENVELOPE.md).

## Exact radial instability band

With tau=M t, A=1+epsilon, z=A dn(A tau/2,k_e), and
q=k_e^2=2-2/A^2, a radial spatial perturbation obeys

\[
 R_p''+[p^2/M^2+(3z^2-1)/2]R_p=0.
\]

Under v=A tau/2 this becomes the n=2 Lame equation

\[
 R_{p,vv}+[h_2-6q\operatorname{sn}^2(v,k_e)]R_p=0,
 \qquad h_2=4+q+4p^2/(M^2A^2).
\]

The two-gap spectrum has ordered edges

\[
 2(1+q)-2\sqrt{1-q+q^2},\quad 1+q,\quad 1+4q,\quad
 4+q,\quad 2(1+q)+2\sqrt{1-q+q^2}.
\]

Source: [Haragus and Kapitula, printed page 16](https://sites.calvin.edu/tmk5/research/PeriodicWaveSubmissionOld.pdf),
author manuscript dated 2007-05-15, checked 2026-10-11. It gives the two-gap
operator and these edges. Our translation to the radial field equation is
separate from that paper's NLS stability applications. No local copy saved.

Since p^2>=0, only the upper gap can be reached. Thus the only exponential
radial instability is exactly

\[
 0<\frac{p^2}{M^2}<\frac{A^2}{4}
 \frac{3q^2}{2\sqrt{1-q+q^2}+2-q}.
\]

The rationalized expression avoids catastrophic subtraction at small q.
The upper bound equals 3 epsilon^2+O(epsilon^3). At epsilon=1e-7,
its square root is p_max/M=1.7320508942e-7, or p_max/m approximately
3.4641e-7 for the chosen masses. The daughter band instead lies near
p/m=0.001. This is an exact separation of linear instability momenta,
not a proof that radial fragmentation is dynamically irrelevant.
The p=0 edge has zero exponential rate; secular growth is not excluded.

## Finite growth-rate checks

[radial_band.py](radial_band.py) integrates the monodromy in an interaction
picture at epsilon=0.001,0.003,0.01,0.1,0.3, and six momenta per amplitude:
0.1,0.5,0.9,1.1,2,10 times the upper bound in squared momentum. All 30
checks pass, including predicted discriminant signs, successful integration
and determinant preservation. See [results](radial_band_run/results.json)
and [manifest](radial_band_run/manifest.json).

At the midpoint in squared momentum, growth rates divided by epsilon^2
per tau are respectively 0.750750, 0.752250, 0.757500, 0.825131, 1.029203.
These finite samples suggest a small-amplitude rate of approximately
0.75 epsilon^2 M, compared with daughter growth approximately epsilon m.
We have not established a uniform remainder bound for this rate, nor
numerically resolved the epsilon=1e-7 radial monodromy. Extrapolating the
rate to that benchmark is therefore a scaling estimate, not verified
benchmark stability evidence.

The original uniform source is linearly unstable. Small amplitude narrows
its instability and the sampled growth rates support a possible timescale
separation, but a production claim must still account for the source's
initial perturbations, expansion, daughter backreaction and nonlinear
transfer between both field components. None is settled by band width alone.
