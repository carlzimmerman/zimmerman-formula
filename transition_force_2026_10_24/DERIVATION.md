# Transition force, exact target, and a constitutive test

Continue MI-14's populated, restoring branch. The existing energy has response from enclosed T mass, F pressure, and response-weighted barrier/stiffness. A correction must change the energy and all density/phase derivatives, not add an acceleration after equilibrium.

Write gd=M(<r)/r², u=MT(<r)/r², q=sin²(πx/2), s=sin²(πx)/π², h=(5/2)K[rho(1−q)]^(2/3), and

    A=W′(u)+beta C F′(u)s+(ell²/2)F′(u)x′²,
    Psi(r)=∫ᵣ∞ A(t)dt,
    Xi=beta C F(u)s′(x)−ell² r⁻²∂r(r²F(u)x′).

The old material chemical potential at fixed phase is Phi+q Psi+(1−q)h. Its radial equilibrium equation is

    g = q A − (1−q)h′ − q′(Psi−h).

The phase equation is rho q_x(Psi−h)+Xi=0. Thus the exact mixed-transition correction to the cold total-density response is

    D = W′(gd) − q A + (1−q)h′ + q′(Psi−h).

Here μ_non-gravity′=−W′(gd)+D. To obtain the original galaxy law, an added constitutive contribution must supply μ_correction′=−D, including its conversion variation. At the existing stationary profile, D=W′(gd)−g. This diagnostic is not a recipe to freeze and subtract the measured force: D changes when density and phase move, and an arbitrary radial subtraction need not have an energy or preserve restoration.

## TF-1: coherent mixture response

This alternative is an explicit new constitutive hypothesis, not a consequence of the galaxy formula. It tests whether coherent response of the whole mixture, rather than T mass alone, can remove the transition correction while an inactive exterior stays a pressure-supported free phase. It also postulates pressure quenching in the coherent mixture; its microscopic and thermal justification is not established.

Set t=clamp(q/.2,0,1), S=t³(10−15t+6t²), and use

    E = Egravity + ∫r²[S W(gd)+(3/2)K(1−S)rho^(5/3)
                      +beta C Fs s(x)+(ell²/2)Fs x′²]dr.

Fs is a positive constant, not a prescribed density or radius. No galaxy-law discrepancy enters the objective. The old response-weighted barrier/stiffness are replaced by constant coefficients, since retaining them would retain their material-force correction. This changes the constitutive model substantially; any numerical gain must be labelled conditional on that change.

Define P=∫ᵣ∞ S W′(gd)dt and h0=(5/2)K rho^(2/3). Complete derivatives per radial volume are

    μrho = Phi+P+(1−S)h0,
    cx = S_x[W(gd)−(3/2)K rho^(5/3)]
         +beta C Fs s′(x)−ell² Fs r⁻²∂r(r²x′).

The two species potentials are μT=μrho+(1−q)cx/(rho q_x), μF=μrho−q cx/(rho q_x); forces are their negative radial gradients. At pure endpoints use variations of the energy rather than division by q_x=0. All discrete derivatives are taken from this single action.

Where S=1, the material equation is exactly g=W′(gd)=gd/(1−gd). Since gd=g−gb, it yields g²/(1+g)=gb. This holds regardless of the local mixture fraction within that plateau. Where S=0, the transport potential is Phi+h0, giving an ordinary positive-pressure free fluid. In the switch region, S′ and pressure terms reappear: law preservation there is not proved. A test must locate that region, report the full gravity curve, and check whether the boundary still restores and matter stays present. Moving the switch beyond the measured range is not proof of universal law preservation across every transition.

TF-1 screens Fs=.01,.03,.1 at n96,domain12,K15,beta.5,ell10kpc, from the old mobile-density state. The total-density saturation inequality replaces the old T-only inequality. No exterior W tail is added because S is assumed zero beyond the box; an appreciable activation at the endpoint invalidates that isolated interpretation. A constant unweighted phase gradient has a nonzero exterior capacity, so endpoint and domain dependence must also be checked before success.
