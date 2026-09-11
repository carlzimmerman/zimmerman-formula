#!/usr/bin/env python3
"""Regular nonlinear initial slice of the fixed action, not time evolution.

Units are the existing dimensionless background units. The source is normal-rest
dust rho=amplitude*exp(-(r/width)**2), with R=r, chi'=0, Q=q, Kr=Ko=H.
The Hamiltonian is integrated exactly. The lapse follows from preserving the
varied clock equation, not an imposed force law. See slice_action/ for derivation.
"""
import math

import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import solve_banded
from scipy.special import gammainc

from background import background


def coefficients(gamma=1e-6):
    b = background(gamma)
    q,H,M,g,W = (b[k] for k in ("q","H","M2","gamma","W0"))
    J = 2*q*b["PX"]-6*g*H*q*q
    Bh = 2*b["PX"]+4*q*q*b["PXX"]-12*g*q*H+6*g*g*q**4/M
    C = 2*q*b["PXt"]+3*g*q*q*W/M
    S = W-2*q*q*b["WY"]
    delta0 = 3*J*(-W*q/(2*M)+C*(H+g*q**3/M)/Bh)
    crho = -W/(2*M)+g*q*q*C/(M*Bh)
    F0 = b["Vtt"]-b["Ptt"]+3*H*b["Wt"]-3*W*W/(2*M)+C*C/Bh
    b.update(J=J, Bhat=Bh, C=C, S=S, lambda0=-delta0,
             lambdab=-crho, F0=F0)
    if min(Bh,S,-delta0,-crho) <= 0:
        raise ValueError("outside this tested positive elliptic branch")
    if abs(F0+delta0) > 1e-12:
        raise ValueError("background clock preservation is inconsistent")
    return b


def geometry(r, amplitude, width, M2):
    """enclosed = integral rho*r² dr; 4pi*enclosed is areal-energy mass.

    Proper rest mass instead includes the radial metric factor A=1/sqrt(f).
    Incomplete gamma avoids subtractive cancellation near the center.
    """
    r = np.asarray(r, dtype=float)
    rho = amplitude*np.exp(-(r/width)**2)
    enclosed = amplitude*width**3*math.sqrt(math.pi)/4*gammainc(1.5,(r/width)**2)
    compactness = np.divide(enclosed,M2*r,out=np.zeros_like(r),where=r!=0)
    f = 1-compactness
    fp = np.divide(compactness,r,out=np.zeros_like(r),where=r!=0)-rho*r/M2
    return rho,f,fp,enclosed


def solve_slice(amplitude, width, *, gamma=1e-6, outer=None, points=501,
                tolerance=2e-9):
    if amplitude < 0 or width <= 0 or points < 20:
        raise ValueError("positive width, nonnegative density and sufficient grid required")
    c = coefficients(gamma)
    M,q,H,g,W = (c[k] for k in ("M2","q","H","gamma","W0"))
    S,l0,lb = c["S"],c["lambda0"],c["lambdab"]
    # Uniform certificate: I/r <= amplitude*r²/3 for r<=width;
    # I/r <= I(infinity)/width for r>=width. Sufficient, not necessary.
    f_lower_bound = 1-amplitude*width**2*max(1/3,math.sqrt(math.pi)/4)/M
    if f_lower_bound <= 0:
        raise ValueError("uniform f>0 certificate unavailable for this source")
    outer = float(outer if outer is not None else max(12.,12*width))
    if outer <= 4*width:
        raise ValueError("outer boundary must lie beyond the localized source")
    # Resolve both the source and the background screening length.
    inner = min(4*width,outer)
    mesh = np.r_[np.linspace(0,inner,points),
                 np.linspace(inner,outer,points)[1:]]
    if np.min(geometry(mesh,amplitude,width,M)[1]) <= 0:
        raise ValueError("f<=0: this areal-coordinate patch is inadmissible")
    scale = amplitude if amplitude else 1.

    def rhs(r,y):
        rho,f,fp,_ = geometry(r,amplitude,width,M)
        # y[0]=delta/scale avoids an absolute tolerance hiding small sources.
        return np.vstack((y[1],-fp*y[1]/(2*f)
                          +((l0+lb*rho)*y[0]+lb*rho/scale)/(S*f)))

    raw = solve_bvp(rhs,lambda left,right: np.array([left[1],right[0]]),
                    mesh,np.zeros((2,len(mesh))),S=np.diag([0.,-2.]),
                    tol=tolerance,max_nodes=30000)
    if not raw.success:
        raise RuntimeError(raw.message)

    class ScaledSolution:
        def sol(self,r,nu=0):
            return scale*raw.sol(r,nu)
    solution = ScaledSolution()
    r = mesh
    delta,Np = solution.sol(r)
    N = 1+delta
    rho,f,fp,enclosed = geometry(r,amplitude,width,M)
    if np.min(N) <= 0:
        raise ValueError("nonpositive lapse")
    Npp = solution.sol(r,1)[1]
    ratio = np.divide(Np,r,out=Npp.copy(),where=r!=0)
    lap = f*Npp+(2*f)*ratio+fp*Np/2
    # Evolution equations solve for Q_t and K_t, not q/N or a static field.
    D0 = 3*c["J"]*(H+g*q**3/M)
    dQ = -(D0*delta+g*q*q*rho*N/M)/c["Bhat"]
    Qdot0 = -(D0+c["C"])/c["Bhat"]
    Qdot = Qdot0+dQ
    Z = (3*q*c["J"]+rho)/(2*M)
    Kdot = lap-N*Z-3*W/(2*M)-3*g*q*q*Qdot/M
    mass_over_r3 = np.divide(enclosed,r**3,out=np.full_like(r,amplitude/3),where=r!=0)
    hdot = f*ratio-N*(mass_over_r3/(2*M)+q*c["J"]/(2*M))-W/(2*M)-g*q*q*Qdot/M
    gN = np.divide(enclosed,2*M*r*r,out=np.zeros_like(r),where=r!=0)
    # Background-subtracted geodesic areal acceleration, evaluated stably.
    g_areal = gN+r*(2*g*q*q*dQ-c["U"]*delta)/(2*M*N)
    equation = S*lap-(l0+lb*rho)*delta-lb*rho
    source_scale = max(float(np.max(abs(lb*rho))),1e-30)
    # A fresh off-collocation grid prevents nodal interpolation identities from
    # masquerading as an independent differential residual check.
    probe = raw.x[:-1]+.37*np.diff(raw.x)
    pd,pz = solution.sol(probe)
    pzz = solution.sol(probe,1)[1]
    prho,pf,pfp,_ = geometry(probe,amplitude,width,M)
    plap = pf*pzz+(2*pf/probe+pfp/2)*pz
    offgrid = S*plap-(l0+lb*prho)*pd-lb*prho
    trace = -2*M*Kdot-6*g*q*q*Qdot+2*M*lap-N*(3*q*c["J"]+rho)-3*W
    chi = (2*c["PX"]+4*q*q*c["PXX"]-12*g*H*q)*Qdot-2*g*q*q*Kdot
    chi += 2*g*q*q*lap+3*N*H*c["J"]+2*q*c["PXt"]
    tau = c["Vtt"]-c["Ptt"]+3*H*c["Wt"]+W*Kdot-2*q*c["PXt"]*Qdot-2*q*q*c["WY"]*lap
    metric_A = M*(N*mass_over_r3/M-2*f*ratio)+N*q*c["J"]+W+2*M*hdot+2*g*q*q*Qdot
    return dict(r=r,rho=rho,f=f,fp=fp,enclosed=enclosed,N=N,delta=delta,Nprime=Np,
                Nsecond=Npp,laplacian=lap,Qdot=Qdot,Kdot=Kdot,hdot=hdot,
                chi_gradient_dot=q*Np,dust_gradient_dot=Np,
                dust_density_dot=-3*N*H*rho,gN=gN,g_areal=g_areal,
                clock_relative_acceleration=-np.sqrt(f)*Np/N,
                coefficients=c,solution=solution,collocation_nodes=len(raw.x),
                f_lower_bound=f_lower_bound,
                equation_relative_residual=float(np.max(abs(equation))/source_scale),
                offgrid_equation_relative_residual=float(np.max(abs(offgrid))/source_scale),
                unit_lapse_relative_residual=float(np.max(abs(lb*rho))/source_scale),
                time_equation_absolute_residuals={key:float(np.max(abs(value)))
                    for key,value in dict(trace=trace,chi=chi,tau=tau,metric_A=metric_A).items()})


def independent_fd(amplitude,width,outer,points,c):
    """Independent second-order uniform finite difference solve for delta.

    Solves the unscaled equation, using the regular-center 3D Laplacian.
    This does not call the collocation right-hand side or reuse its solution.
    """
    r = np.linspace(0,outer,points)
    dr = r[1]
    rho,f,fp,_ = geometry(r,amplitude,width,c["M2"])
    potential = (c["lambda0"]+c["lambdab"]*rho)/c["S"]
    b = np.divide(2*f,r,out=np.zeros_like(r),where=r!=0)+fp/2
    main = 2*f/dr**2+potential
    lower = -f/dr**2+b/(2*dr)
    upper = -f/dr**2-b/(2*dr)
    main[0] = 6*f[0]/dr**2+potential[0]
    upper[0] = -6*f[0]/dr**2
    main[-1],lower[-1] = 1.,0.
    rhs = -c["lambdab"]*rho/c["S"]
    rhs[-1] = 0.
    matrix = np.zeros((3,points))
    matrix[0,1:],matrix[1],matrix[2,:-1] = upper[:-1],main,lower[1:]
    return r,solve_banded((1,1),matrix,rhs)


def force_bound(out,amplitude,width):
    """Analytic maximum-principle bound for this decreasing Gaussian profile.

    PDE argument in REPORT.md is not machine-formalized. This function evaluates
    its hypotheses and bound; it does not infer positivity from sampled data.
    """
    c,r = out["coefficients"],out["r"]
    M,q,g,H = (c[k] for k in ("M2","q","gamma","H"))
    d = c["lambdab"]/c["lambda0"]  # sup exp(-(r/width)^2)=1
    D0 = 3*c["J"]*(H+g*q**3/M)
    Ueff = c["U"]+2*g*q*q*D0/c["Bhat"]
    mass_unit = geometry(r,1.,width,M)[3]
    n = np.divide(mass_unit,2*M*r*r,out=np.zeros_like(r),where=r!=0)
    bound = n+r*Ueff*d/M
    hypotheses = (M>0 and c["S"]>0 and c["Bhat"]>0 and c["lambda0"]>0
                  and c["lambdab"]>0 and Ueff>=0 and 0<=amplitude<=1/(2*d)
                  and g*g*q**4/(M*c["Bhat"])<=1/6 and out["f_lower_bound"]>0)
    return dict(d=d,C=bound,n=n,Ueff=Ueff,hypotheses=bool(hypotheses))


if __name__ == "__main__":
    import json
    result = solve_slice(.04,.5)
    print(json.dumps({"lapse_min":float(np.min(result["N"])),
                      "f_min":float(np.min(result["f"])),
                      "equation_relative_residual":result["equation_relative_residual"],
                      "time_equation_absolute_residuals":result["time_equation_absolute_residuals"]},indent=2))
