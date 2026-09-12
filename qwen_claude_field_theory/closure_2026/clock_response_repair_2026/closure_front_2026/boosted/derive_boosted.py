#!/usr/bin/env python3
"""Exact local aligned clock/scalar principal symbol and conserved-dust forcing.

No coefficient fit. stdout JSON by default; --output is the only write option.
The sourced result additionally assumes Einstein gravity and minimal matter.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sympy as S


def derive():
    e = S.symbols('epsilon', real=True)
    q, s = S.symbols('q s', positive=True)
    p, r, W, d, gamma, h0, hs = S.symbols('PX PXX W0 WY gamma H00 Hspace', real=True)
    M2 = S.symbols('M2', positive=True)
    pt, px, st, sx = S.symbols('pi_t pi_x sigma_t sigma_x', real=True)
    checks = {}
    def zero(name, expression):
        checks[name] = S.simplify(expression) == 0
        if not checks[name]:
            raise AssertionError((name, expression))

    # Exact 1+1 invariants; isotropy restores the sum over all spatial axes.
    # A Taylor jet P=P0+p*dX+r*dX²/2 suffices at quadratic derivative order.
    X = (q+e*pt)**2-e**2*px**2
    sr = S.sqrt((s+e*st)**2-e**2*sx**2)
    inner = -(s+e*st)*(q+e*pt)+e**2*sx*px
    Y = -X+inner**2/sr**2
    Y2 = S.simplify(S.diff(Y,e,2).subs(e,0)/2)
    zero('projector_quadratic_mixing', Y2-(px-q*sx/s)**2)
    lag = p*(X-q*q)+r*(X-q*q)**2/2+sr*(W+d*Y)
    L2 = S.simplify(S.diff(lag,e,2).subs(e,0)/2)
    expected = (p+2*q*q*r)*pt**2-p*px**2+s*d*(px-q*sx/s)**2-W*sx**2/(2*s)
    zero('raw_action_quadratic_jet',L2-expected)
    zero('clock_has_no_principal_time_kinetic',S.diff(L2,st,2))
    clock = S.diff(L2,sx,2)
    cross = S.diff(L2,px,sx)
    zero('clock_block',clock-(2*q*q*d-W)/s)
    sx_solution = S.factor(-cross*px/clock)
    Lreduced = S.factor(L2.subs(sx,sx_solution))
    K0 = 2*p+4*q*q*r
    G0 = 2*p-2*s*d*W/(W-2*q*q*d)
    zero('clock_schur_reduction',Lreduced-(K0*pt**2-G0*px**2)/2)
    zero('W0_zero_cancellation',G0.subs(W,0)-2*p)

    eta = S.diag(-1,1,1,1)
    H = S.diag(h0,hs,hs,hs)
    v = S.Matrix([q,0,0,0]); vu=eta*v
    box = S.trace(eta*H)
    directZ = 4*gamma*(box*eta-eta*H*eta)
    # This tensor follows by linearizing 2gamma[(Box chi)^2-H.H].
    dh = S.diag(*S.symbols('dH00 dH11 dH22 dH33', real=True))
    raw = 2*gamma*(S.trace(eta*(H+e*dh))**2-S.trace(eta*(H+e*dh)*eta*(H+e*dh)))
    zero('direct_hessian_linearization',S.diff(raw,e).subs(e,0)-S.trace(directZ*dh))

    # Independent trace reversal of the actual cubic metric stress, with an
    # arbitrary symmetric perturbation Hessian, then Einstein substitution.
    entries = S.symbols('a00 a01 a02 a03 a11 a12 a13 a22 a23 a33', real=True)
    a00,a01,a02,a03,a11,a12,a13,a22,a23,a33=entries
    A=S.Matrix([[a00,a01,a02,a03],[a01,a11,a12,a13],[a02,a12,a22,a23],[a03,a13,a23,a33]])
    T3=2*gamma*(S.trace(eta*A)*v*v.T-v*(A*vu).T-(A*vu)*v.T+eta*(vu.T*A*vu)[0])
    R3=(T3-eta*S.trace(eta*T3)/2)/M2
    deltaZ=-2*gamma**2*q*q*(q*q*eta+4*vu*vu.T)/M2
    zero('cubic_einstein_debraiding',-2*gamma*(vu.T*R3*vu)[0]-S.trace(deltaZ*A))
    K = S.factor(K0-directZ[0,0]-deltaZ[0,0])
    G = S.factor(G0+directZ[1,1]+deltaZ[1,1])
    zero('full_kinetic',K-(K0+12*gamma*hs+6*gamma**2*q**4/M2))
    zero('full_gradient',G-(G0+4*gamma*(-h0+2*hs)-2*gamma**2*q**4/M2))

    # Uniform dust moves at w in the clock frame. Rest density rho is a
    # scalar. Fourier modes of its eternal conserved source obey omega=w*kx.
    w=S.symbols('w', real=True)
    rho=S.symbols('rho', real=True)
    boost=1/S.sqrt(1-w*w)
    U=S.Matrix([boost,boost*w,0,0]); Ul=eta*U
    Tm=rho*Ul*Ul.T
    Rm=(Tm-eta*S.trace(eta*Tm)/2)/M2
    source=S.factor(2*gamma*(vu.T*Rm*vu)[0])
    zero('dust_trace',S.trace(eta*Tm)+rho)
    zero('action_derived_dust_source',source-gamma*q*q*rho*(1+w*w)/(M2*(1-w*w)))
    kx,ky,kz=S.symbols('kx ky kz',real=True)
    xi=S.Matrix([-w*kx,kx,ky,kz])
    zero('dust_fourier_conservation',(xi.T*U)[0])
    for j in range(4):
        zero('cubic_principal_stress_conservation_'+str(j),(xi.T*eta*T3.subs(dict(zip(entries,[xi[0]**2,xi[0]*xi[1],xi[0]*xi[2],xi[0]*xi[3],xi[1]**2,xi[1]*xi[2],xi[1]*xi[3],xi[2]**2,xi[2]*xi[3],xi[3]**2]))))[j])

    Ka,Ga=S.symbols('K G',real=True)
    # Source-rest Fourier wavevector k': omega_clock=Gamma*w*k'_parallel.
    Dsource=Ga*(ky*ky+kz*kz)+(Ga-Ka*w*w)*kx*kx/(1-w*w)
    Dclock=Ga*(kx*kx+ky*ky+kz*kz)-Ka*w*w*kx*kx
    zero('lorentz_covariant_denominator',Dclock.subs(kx,boost*kx)-Dsource)
    zero('static_source_control',source.subs(w,0)-gamma*q*q*rho/M2)
    # Actual leading stationary lapse response in the source rest frame.
    # R00=Delta Phi, with g00=-(1+2Phi), and A=-xi xi^T*pi_hat.
    pi_hat=S.symbols('pi_hat',real=True)
    source_xi=S.Matrix([0,kx,ky,kz])
    source_v=S.Matrix([q*boost,q*boost*w,0,0]);source_vu=eta*source_v
    source_A=-source_xi*source_xi.T*pi_hat
    source_T3=2*gamma*(S.trace(eta*source_A)*source_v*source_v.T-source_v*(source_A*source_vu).T-(source_A*source_vu)*source_v.T+eta*(source_vu.T*source_A*source_vu)[0])
    source_R3=(source_T3-eta*S.trace(eta*source_T3)/2)/M2
    coupling=S.factor(source/rho)
    zero('stationary_lapse_back_response',source_R3[0,0]+(kx*kx+ky*ky+kz*kz)*coupling*pi_hat)
    # At fixed |k_clock|, residue wrt mu=cos(theta). Fourier amplitude pi=-S/D.
    kmag,mu,cs=S.symbols('k mu cs', positive=True)
    angularD=Ka*kmag**2*(cs**2-w*w*mu*mu)
    angular_residue=S.factor(-source/S.diff(angularD,mu).subs(mu,cs/w))
    zero('simple_pole_residue',angular_residue-source/(2*Ka*kmag**2*w*cs))
    return dict(
        scope='Exact local frozen-jet principal coefficients, timelike aligned gradients and isotropic scalar Hessian; not an on-shell sourced solution or PPN.',
        conventions={'signature':'-+++','action':'P(X,tau)-V(tau)+s W(Y,tau)+gamma X Box chi','q':'proper clock-frame chi time derivative; q>0','s':'proper tau rate; s>0','H':'covariant Hessian chi=diag(H00,Hspace,Hspace,Hspace)','Einstein':'M2 G_mu_nu=T_mu_nu; minimal matter','Fourier':'exp(-i omega t+i k.x)','normalization':'L2=(K*pi_t²-G*grad(pi)²)/2 after elimination'},
        exclusions=['W0-2q² WY=0: clock Schur division unavailable','k_clock=0: clock principal row is zero and cannot be eliminated','Coefficient derivatives, tau mass/mixing, and other lower derivative terms are excluded','Metric sources retained at leading principal curvature order only','No finite-gradient nonlinear branch, boundary Green function or PPN coefficients computed'],
        quadratic={'Y2':str(Y2),'L2_frozen_metric':str(expected),'clock_spatial_block':str(clock),'sigma_over_pi_nonzero_k':str(S.factor(sx_solution/px)),'K_frozen_metric':str(K0),'G_frozen_metric':str(G0),'K_with_Einstein':str(K),'G_with_Einstein':str(G)},
        moving_source={'source_forcing_S':str(source),'scalar_amplitude':'pi_hat=-S_hat/D; S from 2 gamma v^mu v^nu trace_reverse(T_m)_mu_nu/M2','clock_frame_D':str(Dclock),'source_rest_D':str(Dsource),'source_rest_clock_k_squared':str(boost**2*kx*kx+ky*ky+kz*kz),'stationary_lapse_coupling_a':str(coupling),'stationary_lapse_response':'Phi_hat=-rho_hat/(2 M2 |k_source|²)+a*pi_hat; cubic part=-a²*rho_hat/D. Principal order only; excludes homogeneous solutions.','simple_angular_residue_at_mu_cs_over_w':str(angular_residue),'sound_speed_squared':'G/K, conditional K>0 and G>=0','positive_sound_pole':'For 0<cs<|w|<1, angular poles mu=+-cs/|w| occur in clock frame. If gamma*q²*rho_hat is nonzero there, the leading dust scalar residue is nonzero.','zero_sound':'G=0,K!=0,w!=0 gives D=-K*w²*k_parallel² in clock frame: double angular degeneracy; simple-pole residue formula must not be used. w=0 gives identically zero stationary principal D.','tiny_sound_limit':'The cs>0 simple angular residue scales as 1/cs at fixed K,w,k,gamma,q,rho, conditional on jets realizing that limit. No finite retarded solution follows.'},
        checks=checks,
        provenance={'python':platform.python_version(),'sympy':S.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'base_revision_reported_by_parent':'ac2052ae0','git_inspected':False})


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=derive();text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')
