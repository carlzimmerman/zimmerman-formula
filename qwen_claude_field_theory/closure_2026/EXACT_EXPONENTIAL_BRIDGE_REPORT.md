# Exact exponential static bridge

The York candidate's displayed \(\nu(s)=\sqrt{1+1/s}\) is not the inverse of
the required exponential law. The exact spherical bridge is defined by

\[
s=x(1-e^{-x}),\qquad x=g/a_0,\qquad s=g_N/a_0,
\qquad \nu_{\exp}(s)=x(s)/s.
\]

The inverse is unique because

\[
\frac{ds}{dx}=1+(x-1)e^{-x}>0\quad(x>0).
\]

The Python audit solves this inverse by bracketed bisection over
\(10^{-12}\le s\le10^4\). It obtains machine-small residuals, positive
derivative, \(x/\sqrt{s}\to1\) in deep MOND, \(\nu_{\exp}\to1\) at high
acceleration, and a measurable maximum mismatch of about 9.45% with the old
square-root kernel. Lean certifies the strict slope inequality
\(ds/dx>0\) for \(x>0\) and the exact identity

\[
g=a_0x,\quad g_N=a_0s,\quad s=x(1-e^{-x})
\;\Longrightarrow\;
(1-e^{-g/a_0})g=g_N,
\]

An explicit primitive for the QUMOND carrier is also available in the inverse
parameter \(x\): with \(u=s^2\),
\[
F(u)=x^2+2-2e^{-x}(x^2+x+1),
\qquad \frac{dF}{du}=\nu_{\exp}(s).
\]
The Python gate differentiates this expression symbolically and checks the
result numerically across the same range.

On the deep-MOND branch \(g^2=a_0g_N\) with circular motion
\(v^2=rg\), derives \(v^4=GMa_0\).

This is a constructive correction to the York action's static constitutive
function. It does not yet prove the full covariant Dirac, Ward, PPN, FLRW, or
stability gates.

## Commands

```text
python3 -B exact_exponential_qumond_bridge_2026.py
python3 -B run_lean_exact_bridge.py
```
