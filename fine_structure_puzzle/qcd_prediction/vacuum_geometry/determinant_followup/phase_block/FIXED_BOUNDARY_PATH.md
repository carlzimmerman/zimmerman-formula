# Hand check: fixed wall Higgs value changes the inverse-radius coefficient

This note preserves every executed input and manifest. It checks a physical-path qualification for the already computed dimensionless static-spherical Gaussian function; it is not another experiment or a new full-theory prediction.

The BPS family used in REPORT.md has asymptotic mass parameter \(m\), radius \(R\), and \(x=mR\). Its actual Higgs magnitude on the wall is

\[
b=H(R)=m\coth(mR)-1/R=m h(x).
\]

Thus fixed \(m\) and fixed physical \(b\) are different comparison paths. With \(y=bR\),

\[
y=x\coth x-1,\qquad
x=y+1+O(ye^{-2y})\quad(y\to\infty).
\tag{B1}
\]

The calculated common-unbroken-reference result is

\[
\log\mathcal Z_{J=0,n=0}^{(0)}(x)
=\log(2/3)+\tfrac32\log x-\frac1{2x}-\frac1{2x^2}
+O(x^{-3}).
\]

Substitution of (B1), including differentiation/expansion of the leading logarithm, gives

\[
\boxed{\log\mathcal Z_{J=0,n=0}^{(0)}\big|_{b\,{\rm fixed}}
=\log(2/3)+\tfrac32\log(bR)
+\frac1{bR}-\frac3{4(bR)^2}+O((bR)^{-3}).}\tag{B2}
\]

The residual inverse-radius coefficient of this dimensionless Gaussian comparison therefore changes from \(-1/2\) at fixed \(m\), in units \((mR)^{-1}\), to \(+1\) at fixed \(b\), in units \((bR)^{-1}\). It is not invariant under changing the physical boundary matching path. The tangential BPS wall data through \(K(x)\) also change on this path, but their large-radius difference is exponentially small; strictly fixing additional finite-wall connection components can require a different saddle and is not silently imposed here.

The same distinction is already visible classically. In the conventions of REPORT.md,

\[
S_{\rm BPS}(R)=\frac{4\pi L}{g^2}R^2H(R)H'(R)
=\frac{4\pi L}{g^2}m h(x)[1-K(x)^2]
=\frac{4\pi L}{g^2}b[1-K(x)^2].\tag{B3}
\]

At fixed \(m\), \(m h(x)[1-K^2]=m-1/R+\) exponentially small terms. At fixed \(b\), (B3) has no algebraic inverse-radius correction. The classical term was not included in the reported Gaussian determinant, so this is a separate path check, not an additional claimed determinant contribution.

Equations (B1)–(B2) apply to the **dimensionless relative Gaussian function** fixed by the common endpoint-normalized one-dimensional determinant ratios. No extra measure normalization is chosen in this substitution. In these unprimed relative operators the same singular origin data and the same outer vector/ghost conditions cancel common endpoint and unit factors. Applying the result to a dimensionful full path integral still requires its common regulator, renormalization scale, coupling convention and any collective-coordinate conversion; additional mass-dependent normalization cannot be assumed absent without that matching. Such factors are not specified or fitted here.

The finite-radius scalar Robin mode remains positive and is retained. Replacing it by an infinite-space collective zero mode before varying \(b\) would define another calculation. Consequently neither (B2) nor the fixed-\(m\) coefficient supplies a universal bulk term, a cosmological \(c_H\), or physical \(R(\alpha)\).
