# The weighted clock obstruction is not sign definite

The general functional proposed after the two-shell test can be positive or negative. This closes the sign question with exact admissible Fourier polynomials; it does not construct a transverse-vector rescue. Both examples have nonzero weighted obstruction and therefore fail this necessary compatibility test.

## Scope and identity

Use the inherited n=3 projected action and its pure decaying scalar seed, on a connected flat periodic torus. Let f be a real smooth zero-mean function, u=(-Delta)^(-1)f, w=Delta f, and

R=div(f grad f−2w grad u).

The actual second-order clock equation with a possible smooth divergence-free transverse shift V requires V·grad w=(H/a)R. Consequently, for every smooth G, integral G(w)R=0 is necessary: G(w)V·grad w=div[V A_G(w)] with A_G'=G. Periodicity kills the integral. This necessary identity does not solve the full vector or higher-order field equations.

For G(w)=w², integrating the first divergence and the inverse-Poisson term gives

I=integral w²R=integral w²|grad f|²+(7/3)integral f w³.

Indeed, expand R=|grad f|²+fw−2grad w·grad u+2fw. Then integral w² grad w·grad u=(1/3)integral grad(w³)·grad u=(1/3)integral f w³. There are no boundary terms. The positive gradient term does not determine the sign of I.

## Exact counterexample

Take the 2pi-periodic one-dimensional polynomial

f(x)=cos x+(1+cos x/2)(cos(40x)−cos(80x))/100.

It is real, smooth, and has zero mean. Extend it constantly in the other two torus directions. Exact rational Fourier convolution, with frequencies at most 81 and zero coefficient giving the normalized spatial mean, yields

I/(2pi)=237477851379173/25600000000 > 0.

The display value is approximately 9276.47857. The script computes R using the inverse Laplacian and independently computes the integrated expression without the inverse Laplacian; both rational outputs coincide. No numerical quadrature, sampling alias, floating precision, or truncation of an infinite Fourier series enters this equality. In three dimensions the extra two period factors multiply I by a positive number.

In contrast, f=cos x has u=f, w=−f, R=−3 cos(2x), and I/(2pi)=−3/4. Thus neither a universal nonpositive nor a universal nonnegative sign holds within the declared smooth zero-mean class.

The exact finite assertion is sufficient to disprove the universal sign claim: the displayed finite polynomial is itself an admissible member of that class. A check count is not the proof. The Fourier coefficient construction is precisely multiplication/differentiation/inversion of this finite polynomial, followed by its exact integral.

## Implication and limitations

The older cos x+alpha cos(2x) negative formula remains correct in its restricted family. It cannot be extended to arbitrary f on the basis of this weighted sign. A positive I still obstructs V just as a negative I does; the required value is zero. This example therefore provides no escape from the local clock condition, and does not weaken the separately proved finite-Fourier scalar obstruction. It does not classify functions with I=0, infinitely supported fields, general time-dependent seeds, relative flat modes, nonlinear health or cold abundance.

Development: a finite FFT diagnostic suggested the example; it is not evidence for the exact claim and is superseded by rational Fourier arithmetic. The reproducible script checks both implementations, a hand-computable eigenfunction, reality/mean and inverse-Poisson conventions. Controls replace the actual transport coefficient 2 by 1, wrongly impose universal nonpositivity, or confuse zero unweighted mean with weighted compatibility. Standard runner manifests freeze these artifacts. No inherited parent inputs were changed.
