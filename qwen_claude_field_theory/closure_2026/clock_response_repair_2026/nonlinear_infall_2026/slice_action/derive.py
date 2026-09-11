#!/usr/bin/env python3
"""Exact reduction of the fixed spherical action to one normal-rest dust slice.

No spatial-gradient restriction is made before varying or differentiating.
Run directly to print the checks and compact lapse coefficients as JSON.
All arithmetic is symbolic over rational functions with formal constitutive jets.
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import time

import sympy as s

HERE = Path(__file__).resolve().parent
INPUT = HERE.parents[1] / "spherical_baryon_bridge" / "action" / "derive.py"


def build_audit():
    started = time.monotonic()
    spec = importlib.util.spec_from_file_location("unfixed_spherical_action", INPUT)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    checks = {}

    def check(name, residual):
        residual = s.cancel(s.expand(residual))
        checks[name] = residual == 0
        if not checks[name]:
            raise AssertionError(name + ": " + str(s.factor(residual)))

    mu, ga, r = m.M2, m.gamma, m.r
    N, A, R, Nr, Ar = m.N, m.A, m.R, m.Nr, m.Ar
    q, H, kd, hd, Qd, rhob = s.symbols("q H k_t h_t Q_t rho_b", real=True)
    Ptt, Vtt, WYYY, WYYt = s.symbols("P_tt V_tt W_YYY W_YYt", real=True)
    B0, charge, U, qd, Hdot = s.symbols("B0 J_bg U qdot Hdot", real=True)
    P, PX, PXX, Pt, PtX = m.P, m.PX, m.PXX, m.Pt, m.PXt
    W, d, Wt, V, Vt = m.W, m.WY, m.Wt, m.V, m.Vt
    Nrr = m.jets["N", 0, 2]

    # Vary tau at fixed g and chi before imposing tau=t. Its two derivative
    # coefficients on that gauge slice follow from ds=n^mu d_mu(delta tau)
    # and dQ=-h^{mu nu} chi_mu d_nu(delta tau)/s.
    Jsp = m.dr(R**2*d*m.u/A)/(A*R**2)
    T = Vt-Pt+W*(m.k+2*m.h)-2*d*m.k*m.Y-2*m.Q*Jsp
    tau_density = (N*A*R**2*(Pt-Vt)+A*R**2*Wt-m.dt(A*R**2*W)
                   +m.dr(m.v*A*R**2*W+2*N*R**2*m.Q*d*m.u/A))
    check("tau_covariant_variation", tau_density+N*A*R**2*T)

    # Pull back AFTER all differentiations. Time derivatives of chi_r are
    # retained: chi_tr=q N_r, chi_trr=q N_rr. N_t is arbitrary and must cancel.
    sub = {m.R:r, m.Rr:1, m.jets["R",0,2]:0, m.jets["R",0,3]:0,
           m.At:N*A*H, m.Rt:N*r*H, m.ct:N*q,
           m.jets["A",2,0]:A*(N*kd+H*m.Nt+N**2*H**2),
           m.jets["R",2,0]:r*(N*hd+H*m.Nt+N**2*H**2),
           m.jets["c",2,0]:q*m.Nt+N*Qd,
           m.jets["A",1,1]:H*(Nr*A+N*Ar),
           m.jets["R",1,1]:H*(Nr*r+N),
           m.jets["c",1,1]:q*Nr,
           m.jets["c",1,2]:q*Nrr}
    for (name, i, j), z in m.jets.items():
        if name == "v" or (name == "c" and i == 0 and j > 0):
            sub[z] = 0

    def at_slice(expr):
        return s.cancel(expr.subs(sub, simultaneous=True))

    lap = (Nrr+(2/r-Ar/A)*Nr)/A**2
    R3 = 2/r**2*(1-1/A**2+2*r*Ar/A**3)
    Kd = kd+2*hd
    B = 2*PX+4*q**2*PXX
    b = B-12*ga*q*H
    bhat = b+6*ga**2*q**4/mu
    charge_j = 2*q*PX-6*ga*H*q**2
    rho_clock = 2*q**2*PX-P+V-6*ga*H*q**3
    ham = mu*(R3/2+3*H**2-m.Lambda)-rho_clock-rhob
    check("slice_hamiltonian", at_slice(m.E["N"])/(A*r**2)-rhob-ham)
    check("slice_momentum", at_slice(m.E["v"]))
    trace = (2*mu*Kd+6*ga*q**2*Qd-2*mu*lap
             +3*N*(3*mu*H**2+P-V-mu*m.Lambda)+mu*N*R3/2+3*W)
    check("slice_metric_trace", at_slice(m.E["A"])/r**2+at_slice(m.E["R"])/(A*r)-trace)
    ricdiff = Ar/(A**3*r)-(1-1/A**2)/r**2
    hessdiff = (Nrr-(Ar/A+1/r)*Nr)/A**2
    shear_rhs = hessdiff-N*ricdiff
    # The action is varied with respect to the covariant spatial metric:
    # E_A/(N R^2)=-mu G^r_r+T^r_r. The tracefree residual has this minus sign.
    check("radial_metric_tracefree", at_slice(m.E["A"])/r**2
          -at_slice(m.E["R"])/(2*A*r)+mu*(kd-hd-shear_rhs))
    current = b*Qd-2*ga*q**2*Kd+3*N*H*charge_j+2*q*PtX+2*ga*q**2*lap
    check("slice_chi_current", -at_slice(m.E["c"])/(A*r**2)-current)
    check("generated_chi_laplacian", at_slice(m.dt(m.D))-q*lap)
    check("generated_tau_spatial_current", at_slice(m.dt(Jsp))-q*d*lap)

    # The imported chain rule needs the next explicit constitutive jets when
    # differentiating the already varied tau equation; all are held independent.
    Tt = (m.dt(T)+s.diff(T,Pt)*(Ptt+PtX*m.dt(m.X))+s.diff(T,Vt)*Vtt
          +s.diff(T,m.WYY)*(WYYY*m.dt(m.Y)+WYYt))
    tau_preserve = Vtt-Ptt+3*H*Wt+W*Kd-2*q*PtX*Qd-2*q**2*d*lap
    check("slice_tau_preservation", at_slice(Tt)-tau_preserve)

    # Elimination uses the actual trace/current coefficients, not a declared
    # number of physical degrees of freedom. Its denominator is kept explicit.
    mat = s.Matrix([[-2*mu, -6*ga*q**2], [-2*ga*q**2, b]])
    check("kinetic_determinant", mat.det()+2*mu*bhat)
    inv = s.Matrix([[-b/(2*mu*bhat), -3*ga*q**2/(mu*bhat)],
                    [-ga*q**2/(mu*bhat), 1/bhat]])
    for i in range(2):
        for j in range(2):
            check("kinetic_inverse_%d%d" % (i,j), (mat*inv-s.eye(2))[i,j])
    C = 2*q*PtX+3*ga*q**2*W/mu
    theta = H+ga*q**3/mu
    Qrhs = -(N*(3*charge_j*theta+ga*q**2*rhob/mu)+C)/bhat
    Krhs = lap-(N*(3*q*charge_j+rhob)+3*W)/(2*mu)-3*ga*q**2*Qrhs/mu
    rhs = s.Matrix([-2*mu*lap+N*(3*q*charge_j+rhob)+3*W,
                    -2*ga*q**2*lap-3*N*H*charge_j-2*q*PtX])
    for i in range(2):
        check("velocity_solution_%d" % i, (mat*s.Matrix([Krhs,Qrhs])-rhs)[i])
    # On this slice the repaired background Hamiltonian relation and P(q^2)=0
    # imply R3=2 rho_b/mu. Check its use in the trace explicitly.
    bg_energy_sub = {V:3*mu*H**2-mu*m.Lambda-q*charge_j+P}
    check("trace_constraint_reduction", (trace-(2*mu*Kd+6*ga*q**2*Qd
          -2*mu*lap+N*(3*q*charge_j+rhob)+3*W)).subs(bg_energy_sub)
          .subs(Ar,A**3*(rhob*r**2/mu-1+1/A**2)/(2*r)))
    Ktrace = lap-(N*(3*q*charge_j+rhob)+3*W)/(2*mu)-3*ga*q**2*Qd/mu
    h_rhs = (Nr/(A**2*r)-N*((1-1/A**2)/(2*r**2)+q*charge_j/(2*mu))
             -W/(2*mu)-ga*q**2*Qd/mu)
    check("angular_acceleration", ((Ktrace-shear_rhs)/3-h_rhs)
          .subs(Ar,A**3*(rhob*r**2/mu-1+1/A**2)/(2*r)))
    # At normal rest the dust geodesic has u=(1/N,0), so its physical
    # d^2 R/ds^2 is the covariant Hessian of R contracted with this vector.
    geodesic = (m.jets["R",2,0]-m.G[0,0,0]*m.Rt-m.G[1,0,0]*m.Rr)/N**2
    ageo = r*(hd/N+H**2)-Nr/(N*A**2)
    check("geodesic_areal_acceleration", at_slice(geodesic)-ageo)
    g_areal = ((1-1/A**2)/(2*r)
               +r*(U*(1-N)+2*ga*q**2*(Qd-qd))/(2*mu*N))
    ageo_bg = r*(H**2-(q*charge_j+U)/(2*mu))
    check("background_subtracted_areal_acceleration", (ageo_bg-ageo.subs(hd,h_rhs)
          -g_areal).subs(W,U-2*ga*q**2*qd))
    S = W-2*q**2*d
    delta0 = 3*charge_j*(-W*q/(2*mu)+C*theta/bhat)
    crho = -W/(2*mu)+ga*q**2*C/(mu*bhat)
    F0 = Vtt-Ptt+3*H*Wt-3*W**2/(2*mu)+C**2/bhat
    reduced = tau_preserve.subs({kd:Krhs-2*hd, Qd:Qrhs}, simultaneous=True)
    check("lapse_elimination", reduced-(S*lap+(delta0+rhob*crho)*N+F0))
    Lsymbol = s.Symbol("Laplacian_N")
    independent_lap = tau_preserve.subs({kd:Lsymbol-(N*(3*q*charge_j+rhob)+3*W)/(2*mu)
                                      -3*ga*q**2*Qrhs/mu-2*hd, Qd:Qrhs}, simultaneous=True)
    # tau_preserve still has its explicit -2q^2 d lap term: replace its real
    # N_rr dependence too, then differentiate the independent Laplacian.
    independent_lap = independent_lap.subs(Nrr,A**2*Lsymbol-(2/r-Ar/A)*Nr)
    lapse_principal = s.cancel(s.diff(independent_lap,Lsymbol))
    check("lapse_principal", lapse_principal-S)
    check("gamma_zero_current", current.subs(ga,0)-(B*Qd+6*N*H*q*PX+2*q*PtX))
    gamma0 = S*lap+N*(-3*q*W*(2*q*PX)/(2*mu)
              +3*(2*q*PX)*2*q*PtX*H/B-rhob*W/(2*mu))
    gamma0 += Vtt-Ptt+3*H*Wt-3*W**2/(2*mu)+(2*q*PtX)**2/B
    check("gamma_zero_lapse", (S*lap+(delta0+rhob*crho)*N+F0).subs(ga,0)-gamma0)

    # Same repaired background identities. Partial P_tX holds X fixed;
    # d/dt P_X(q(t)^2,t)=P_tX+2q qdot P_XX.
    bg = {PX:charge/(2*q)+3*ga*q*H,
          PXX:(B0-charge/q)/(4*q**2),
          Pt:-charge*qd-6*ga*q**2*H*qd,
          PtX:(-3*H*charge-B0*qd)/(2*q)+3*ga*(H*qd+q*Hdot),
          W:U-2*ga*q**2*qd, Vt:-charge*qd-3*H*U}
    check("background_tau", (Vt-Pt+3*H*W).subs(bg))
    bg_extra = {Hdot:-(q*charge+U)/(2*mu)}
    check("background_flow_q", (Qrhs.subs({N:1,rhob:0}).subs(bg)-qd).subs(bg_extra))
    check("background_flow_H", (Krhs.subs({N:1,Nr:0,Nrr:0,rhob:0}).subs(bg)
                                -3*Hdot).subs(bg_extra))
    # The differentiated background tau equation fixes Vtt-Ptt, not Ptt by
    # itself. The chain correction 2q qdot P_tX must be retained.
    Fbg = F0+delta0
    Vtt_bg = Ptt+2*q*qd*PtX-3*Hdot*W-3*H*Wt
    check("background_lapse_source", Fbg.subs(Vtt,Vtt_bg).subs(bg).subs(bg_extra))

    # Exact radial Hamiltonian: define mass primitive I'=rho_b r^2 and f=A^-2.
    I, Ir = s.symbols("mass_primitive mass_primitive_r")
    f = 1-I/(mu*r)
    fr = s.diff(f,r)+s.diff(f,I)*Ir
    check("mass_constraint", (1-f-r*fr-rhob*r**2/mu).subs(Ir,rhob*r**2))
    rho0, rho2 = s.symbols("rho0 rho2")
    f_center = f.subs(I,rho0*r**3/3+rho2*r**5/5)
    check("regular_origin", s.limit(f_center,r,0)-1)
    mass = s.Symbol("M_coordinate")
    check("vacuum_exterior", (1-f-r*fr).subs({I:mass/(4*s.pi),Ir:0}))

    # Independent minimal dust variation, normalization imposed only afterward.
    tht, w, wr, wd, rhod, rhor, rhodot = s.symbols(
        "theta_t w w_r w_t rho_d rho_d_r rho_d_t")
    Ld = N*A*R**2*rhod*((tht-m.v*w)**2/N**2-w**2/A**2-1)/2
    dustEN = s.diff(Ld,N).subs({tht:N,w:0,m.v:0}, simultaneous=True)
    dustEA = s.diff(Ld,A).subs({tht:N,w:0,m.v:0}, simultaneous=True)
    check("dust_rest_sources", dustEN+A*R**2*rhod)
    check("dust_rest_radial_stress", dustEA)
    check("dust_rest_angular_stress", s.diff(Ld,R).subs({tht:N,w:0,m.v:0}, simultaneous=True))
    check("dust_rest_momentum", s.diff(Ld,m.v).subs({tht:N,w:0,m.v:0}, simultaneous=True))
    # Canonical theta_t=v w+N sqrt(1+w^2/A^2) follows from the positive
    # normalization branch, NOT substituting the on-shell zero into L_d.
    Ud = s.sqrt(1+w**2/A**2)
    theta_rhs = m.v*w+N*Ud
    w_rhs = m.dr(theta_rhs)+s.diff(theta_rhs,w)*wr
    check("dust_generated_gradient", w_rhs.subs({w:0,wr:0,m.v:0})-Nr)
    pd = A*R**2*rhod*Ud
    jd = -m.v*pd-N*R**2*rhod*w/A
    pd_dt = m.dt(pd)+s.diff(pd,rhod)*rhodot+s.diff(pd,w)*wd
    jd_dr = m.dr(jd)+s.diff(jd,rhod)*rhor+s.diff(jd,w)*wr
    initial_continuity = at_slice(pd_dt+jd_dr).subs({w:0,wr:0}, simultaneous=True)
    check("dust_slice_continuity", initial_continuity-A*r**2*(rhodot+3*N*H*rhod))

    return {"checks": checks,
            "symbols": {"q":q,"W":W,"d":d},
            "expressions": {"lapse_principal":lapse_principal,
                            "Qdot_laplacian_coefficient":s.diff(Qrhs,Nrr),
                            "Bhat":bhat,"C":C,"delta0":delta0,"c_rho":crho,
                            "F0":F0,"Q_t":Qrhs,"K_t":Krhs,
                            "k_t_minus_h_t":shear_rhs,"h_t":h_rhs,"g_areal":g_areal},
            "source_check_count":len(m.checks),
            "python":platform.python_version(),"sympy":s.__version__,
            "runtime_seconds":round(time.monotonic()-started,3)}


if __name__ == "__main__":
    result = build_audit()
    print(json.dumps({"status":"passed", "checks":result["checks"],
          "check_count":len(result["checks"]),
          "source_check_count":result["source_check_count"],
          "coefficients":{k:str(v) for k,v in result["expressions"].items()},
          "python":result["python"],"sympy":result["sympy"],
          "runtime_seconds":result["runtime_seconds"],
          "non_claims":["no lapse BVP existence without coefficient and boundary hypotheses",
                        "this algebra script does not solve the initial BVP or construct spacetime evolution",
                        "no full nonspherical degree-of-freedom count, MOND, or physical health theorem"]},
          indent=2))
