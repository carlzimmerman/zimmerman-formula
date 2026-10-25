# Finite hold rather than only diagonal projection

The prepared state's final instantaneous polarization had visible mode-quadrature
sensitivity even though its diagonal projection was stable. Check actual finite
time averages independently. Integrate the same angular protocol using DOP853
and a continuous work variable W_dot=sum w*(m_dot*r_y-e_dot*r_z), instead of the
midpoint rotation/quench ledger in prepare.py. Record the final U-U0-W residual.
This is an independent integrator and work accounting, but uses the same physical
assumptions and is a self-review, not an independent research review.

At final b=(u,0,-e_f), split r=r_parallel+r_perp. Holding the externally supplied
field constant gives exact unitary evolution

r(t)=r_parallel+cos(omega*t)*r_perp+sin(omega*t)*(axis cross r), omega=2|b|.

For each recorded interval [t1,t2], integrate the sine and cosine analytically.
The time-averaged polarization differs from the diagonal value by at most

    sum w*2*sqrt(r_perp,z^2+(axis cross r)_z^2)/(omega*(t2-t1)).

This is a bound for each discretized mode ensemble, without assuming random
phases or actual thermalization. It becomes a continuum statement only when the
mode integrals are justified; the finite runs check N=384,768,1536 and two ODE
tolerances. There is no extra energy input during the fixed-field hold since
b_dot=0. This does not make the earlier prescribed preparation autonomous.
No spatial relaxation, collisions, cooling, gravity or countercharge transport
is added. A finite time-averaged response is not a proof that the instantaneous
live-field feedback has the same law.
