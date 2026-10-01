# Linked theta traces in the global momentum equation

The independent auditor highlighted this explicit boundary-equation obligation
after root's main proof was fixed. Root derived the equation below from the
original equations as a cross-check; this is not independent discovery of the
boundary subtlety. The main proof already retained zeta(endpoint)=s and did
not assert a boundary-free equation for the transformed global momentum.

Write pi_theta=sigma chi_t/C, theta_x=chi_x and
P_lambda=I lambda_dot-integral_0^d pi_theta dx. Integrating the original
scale equation gives

    d/dt integral pi_theta dx
        = J[theta_x]_0^d/C + integral(T-U')/C dx.

Subtract this from the original global driver equation. The correct transformed
momentum equation is

    P_lambda_dot = integral U'(theta-lambda)/C dx
                     -V'(lambda)-J[theta_x]_0^d/C.              (A1)

It is independently obtained by varying the transformed action on its correct
domain. Bulk lambda variation supplies integral U'/C-V'. The theta spatial
term supplies the endpoint variation -J[theta_x delta theta]/C. The original
fixed chi walls require delta theta(0)=delta theta(d)=delta lambda, so this
endpoint contributes -J[theta_x]/C to the global equation. It cannot be
discarded by holding theta fixed at both endpoints while varying lambda.

Combining (A1) with the integrated theta equation recovers
I lambda_ddot+V'=integral T/C exactly. Dropping the endpoint term instead
adds the spurious J[theta_x]/C force. No equality of the two background wall
gradients is imposed by the inherited boundary data. The error can disappear
in an exceptional equal-gradient background, which would not justify dropping
it for the general family.

This is a boundary-domain identity for the same autonomous extension, not an
extra wall force or a correction to the original driver action. It preserves
the global canonical pair and the full energy already derived in the main proof.
