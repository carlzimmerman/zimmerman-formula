# Independent raw derivation, saved before comparison with source equations

Prepared 2026-10-19 UTC. This file was derived from the metric in the assignment, without reading any coordinator claim, checker, results, or author/team verdict. At this checkpoint only source-file hashes and equation-location searches have been seen; the source equations themselves have not been read. This is a hand proof, with no finite numerical experiment.

Let b=τ0>0, a=τ1, τ=a+ib, coordinates x0,x1 in [0,L), m>0, V=bL². The metric is ds²=b² dx0²+(a dx0+dx1)². Define -Δ to be nonnegative. Its orthonormal Fourier modes have eigenvalues

p(n)²=(2π/L)²[(n0-a n1)²/b²+n1²].

The massive scalar kernel is Gm(x)=V^(-1) Σ_n exp(2πi n·x/L)/(p(n)²+m²). Its coincidence diverges logarithmically. A coincidence value means a specified common local subtraction; Gm-G0' and the fourth-order kernel below are finite and scheme independent. Here G0' omits n=(0,0). Fix point splitting along x1, whose physical length equals |x1|, and define Greg=lim[x1→0](G(x1)+(1/(2π))log|x1|).

Write μ=mL/(2π), r_n=√(n²+μ²). Summing n0 by the one-dimensional resolvent identity gives

Gm(0), formally = [1/(2mL)]coth(mLb/2)+(1/(2π))Σ_{n≥1}(1/r_n)[1+2 Re{1/(exp(2πb r_n-2πia n)-1)}].

The phase can be conjugated with no change to its real part. In particular the n1=0 contribution is 1/(2mL), not b/(2mL), times the coth. This follows immediately by keeping all n0 with n1=0 and using V=bL².

Define the convergent sums

F(μ)=Σ_{n≥1}[1/n-1/√(n²+μ²)],
H(a,b,μ)=Σ_{n≥1}(1/√(n²+μ²)) Re{1/[exp(2πb√(n²+μ²)-2πia n)-1]}.

Then

Gm,reg=(1/(2π))log(L/(2π)) + [1/(2mL)]coth(mLb/2) -F/(2π)+H/π.  (A)

For the massless zero-mean kernel, the n1=0,n0≠0 term is b/12. The remaining thermal series and the eta product give

G0',reg=(1/(2π))log(L/(2π)) - (1/π)log|η(τ)|.  (B)

Indeed log|η(τ)|=-πb/12+Σ_{k≥1}log|1-exp(2πikτ)|, and Σ_n≥1 n^(-1) Re[q^n/(1-q^n)]=-Σ_k≥1 log|1-q^k|. The b/12 cancels the eta exponential when this identity is used.

The exact, absolutely convergent scalar requested in the assignment is

K=V^(-1)Σ_{n≠0}1/[p(n)²(p(n)²+m²)]
 =[1/m²][G0',reg-Gm,reg+1/(Vm²)]
 =[1/m²]{-(1/π)log|η(τ)|-[1/(2mL)]coth(mLb/2)+F/(2π)-H/π+1/(Vm²)}.  (C)

The plus 1/(Vm⁴) term in K is mandatory: the massive Green function includes its n=0 term 1/(Vm²), while G0' does not. It is an algebraic consequence of the prime in K, before any bosonization or gauge-sector argument.

An independent representation is obtained from the heat kernel and Poisson summation. A winding vector w gives physical length ℓw=L√[b²w0²+(aw0+w1)²]. For m>0,

Gm,reg=-(1/(2π))[log(m/2)+γ]+(1/(2π))Σ_{w∈Z²\{0}} K0(mℓw).  (D)

This is the standard massive plane logarithm with all nonzero winding images; it follows by integrating (4πt)^(-1)exp[-m²t-ℓw²/(4t)] over t>0. Thus at fixed nondegenerate τ every finite-size contribution to the *full* massive local Green function is exponentially small as L→∞. There is no intrinsic inverse-L term in that function. The eigenvalue decomposition and Bessel image representation are two exact reorganizations of the same elliptic operator.

For consistency, Poisson summation of F yields

F(μ)=γ+log(μ/2)+1/(2μ)-2Σ_{k≥1}K0(2πkμ).

Consequently the apparent -1/(2mL) in C cancels F/(2π)'s +1/(2mL) as L→∞. H and coth-1 are exponentially small for fixed b>0. Retaining an uncancelled inverse-L term after this substitution signals mismatched coefficients or omitted modes. This conclusion is nonuniform in a degenerate shape limit b→0 or b→∞ with L, and does not cover boundaries, fixed-temperature limits, or different observables/normal-ordering prescriptions.

The condensate itself needs a separately specified theory, bosonization normalization, eta/determinant prefactor, global gauge/flux integration and constant-mode prescription. The scalar calculation alone cannot settle those factors, and it cannot imply a statement about four-dimensional QCD. In the usual full massless one-flavor Schwinger-model vacuum, the appropriate combination is expected to cancel the explicit eta and global 1/V factors and reduce to a normal-ordered massive scalar vertex expectation; this expectation is only a bridge to be checked against the exact source conventions below, not assumed as part of C.
