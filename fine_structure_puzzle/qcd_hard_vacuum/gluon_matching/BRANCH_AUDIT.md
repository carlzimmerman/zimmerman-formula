# Branch-free logarithmic filter moment

The original direct upper-interval integration in run_v1 and the real-interval
integration in run_v2 both received spurious imaginary terms from SymPy
1.14.0. Thus the second failure localizes the defect more specifically:
mapping the interval alone does not prevent the integration engine from
selecting a complex antiderivative branch. Neither run changed the source
coefficient identities; both failed on the optional logarithmic regulator
moment before writing a final result file.

The v3 implementation uses an exact integrated geometric series instead:

    integral_0^1 -log(x)/(1+x) dx
      =sum_(n=0)^infinity (-1)^n/(n+1)^2
      =(1-2^(1-2))*zeta(2)=pi^2/12.

Termwise integration is justified by sum integral |x^n log(x)|=zeta(2)<infinity.
The real upper-interval substitution remains separately checked. Hence the
full logarithmic filter moment is pi^2/6. This derivation does not depend
on an integral engine's analytic continuation across log branch cuts.

run_v1 and run_v2 remain failed execution records. The v3 source, contract
and this proof were frozen before its new execution.
