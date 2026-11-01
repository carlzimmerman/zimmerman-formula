# Finite normal-relaxation and angular pullback matching subset

Frozen before execution. The CP/unbroken-group invariant singlet slice is
A=i aD,B=bD with X held fixed. Its tree potential is
(f-15ha²)²+(15/2)lambda²a⁴+30a²(hX-lambda b)². At the valley the normal
Hessian is Haa=120fh,Hbb=60lambda²a²,Hab=0. One-loop heavy shifts are
deltaa=-CW_a/Haa,deltab=-CW_b/Hbb, giving the finite reduced two-loop piece
deltaU=-.5(CW_a²/Haa+CW_b²/Hbb). This is one calculable part of the unknown
finite reduced two-loop potential; direct two-loop diagrams remain absent.

Calculate CW_a,CW_b from exact directional derivatives of all 98-scalar,
73-Weyl,24-vector mass matrices and spectral trace h'(m²), including gaugino
mixing and D Hessian. h'(0)=0, so zero/Goldstone masses have a well-defined
first derivative. Do not treat an off-shell negative-mass realpart as a
stable vacuum. CP-odd singlet tadpoles must vanish; compare directional
matrix derivatives against independent central differences of the original
polynomial mass matrices. Independent coordinator reconstruction of tree
Hessian is recorded in the interface messages and will be written in report.

The R phase rotates X and B, not A. Thus the same computed shift gives a
known angular geometric correction deltaF=60b deltab to F=X²+30b². This
does not include direct one-loop derivative/two-point threshold graphs.
Report relative shifts and correction positivity and do not call F matched.

At e=.01,.03,.05,.1 evaluate the local terms on the central running tree
valley at Qm(X0). Add this *central* finite matching subset to rg2log U,F;
it is not added again to the scale logs. For this added subset use finite
field derivatives; float64 full-matrix roundoff cannot be differentiated
with mpmath infinitesimals. Test stencil h=.01/.005 and tight controls at
the final sample points; retain lost accuracy as a limit. Find nearby old
waterbag and native-phase pressure boundaries only if derivative signs
are resolved. The native-phase source uses a=(lnF)' and a'=(lnF)'', with
N=Uss-(a+a'/a)Us,D=Uss+(a-a'/a)Us; positivity of Us/a andD is required.

No finite two-loop graph, direct finite kinetic graph, gravity completion,
UV coupling selection or occupied cosmological state is invented. Use a
fixed one-loop subtraction/gauge convention. The relaxation subset by
itself is gauge-dependent and acquires physical meaning only with the
remaining matched contributions. One numerical thread,180wall/170CPU
seconds, low RSS, preserved failures and fresh version2 records.
