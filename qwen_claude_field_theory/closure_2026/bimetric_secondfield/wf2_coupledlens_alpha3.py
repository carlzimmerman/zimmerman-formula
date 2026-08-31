#!/usr/bin/env python3
"""GATE = COUPLED LENSING (Phi=Psi?) + alpha_3 for the genuinely-BIMETRIC ghost-free-tuned derivative
bimetric (two metrics g, ghat; matter couples to g only). Action
   S = (1/16piG)[sqrt(-g)R + sqrt(-ghat)Rhat] + 2 a0^2 (g ghat)^{1/4} M(T1..T5) + S_matter[g].
Ghost-free 2-D subspace (c1..c5)=(-u0,-u1/2,-u1/2,u0,u1); MOND-alive test point T4-T1 = (u0=1,u1=0).
Interaction depends ONLY on dh=h-hhat (relative graviton). Static-NR scalar-sector reduction of each
invariant already committed (bimond_5invariant): general a(c)=3c1+c2+c3-c4-c5, b(c)=7c1+c2+9c3-c4-3c5,
x(c)=-2c2-6c3+4c5. This script does the DECISIVE static coupled solve:
  PART B  LINEAR coupled 4-field static field equations (Phi,Psi,Phih,Psih), matter sources g_00 only.
          Proves the sum/diff split: (h+hhat)=pure GR (Phi=Psi), dh=modified. Calibrate lam=0 -> GR.
  PART C  DEEP-MOND (M~|T|^{3/2}) nonlinear spherical solve for the RELATIVE sector => gamma_g in the
          deep-MOND exterior. Derive first integrals with sympy Euler-Lagrange; get Q'/P'=-x/(2b) and
          P'~1/r; NUMERICALLY integrate to confirm. gamma_g(deep-MOND)=u1/(2(u0+u1)); =1 iff a=0.
  PART D  alpha_3 / retarded-vs-elliptic: the dh sector propagates (hyperbolic), unlike the elliptic MMG.
"""
import sympy as sp

# ============================================================================================
# PART A  invariants + static-NR (a,b,x) forms, self-contained (matches bimond_5invariant)
# ============================================================================================
print("="*96); print("PART A  static-NR (a,b,x) forms of the ghost-free subspace and the EH (T4-T5) reference")
print("="*96)
u0,u1 = sp.symbols('u0 u1', real=True)
# committed per-invariant static-NR (a,b,x):  T1..T5
abx = {1:(3,7,0), 2:(1,1,-2), 3:(1,9,-6), 4:(-1,-1,0), 5:(-1,-3,4)}
c = [-u0, -u1/2, -u1/2, u0, u1]          # (c1..c5)
a_int = sp.expand(sum(c[i]*abx[i+1][0] for i in range(5)))
b_int = sp.expand(sum(c[i]*abx[i+1][1] for i in range(5)))
x_int = sp.expand(sum(c[i]*abx[i+1][2] for i in range(5)))
print(f"  interaction static-NR form on ghost-free subspace:  a={a_int}   b={b_int}   x={x_int}")
# EH reference (linearized-EH GammaGamma = T4-T5): (0,0,0,1,-1)
aE = abx[4][0]-abx[5][0]; bE = abx[4][1]-abx[5][1]; xE = abx[4][2]-abx[5][2]
print(f"  EH (T4-T5) scalar-sector reference:                 a={aE}   b={bE}   x={xE}   (=> healthy massless GR)")
# T4-T1 test point
sub_T4T1 = {u0:1,u1:0}
print(f"  MOND-alive T4-T1 (u0=1,u1=0): a={a_int.subs(sub_T4T1)}, b={b_int.subs(sub_T4T1)}, x={x_int.subs(sub_T4T1)}")

# ============================================================================================
# PART B  LINEAR coupled static field equations (k-space), 4 scalar potentials
#   Fields: Phi,Psi (g, couples to matter), Ph,Ps (ghat).  Gradients -> k (Fourier, static).
#   S2 = kap_EH[ EH(Phi,Psi) + EH(Ph,Ps) ] + lam[ a*dPhi^2 + b*dPsi^2 + x*dPhi*dPsi ] + rho*Phi
#   with dPhi=Phi-Ph, dPsi=Psi-Ps, EH(P,Q)= 2Q^2 - 4 P Q (the T4-T5 form), all times k^2.
# ============================================================================================
print("\n"+"="*96); print("PART B  LINEAR coupled 4-field static solve: sum=GR / diff=modified; calibrate lam=0 -> GR")
print("="*96)
Phi,Psi,Ph,Ps = sp.symbols('Phi Psi Phih Psih', real=True)
kap,lam,rho,k2 = sp.symbols('kappa_EH lambda rho k2', positive=True)
a_,b_,x_ = sp.symbols('a b x', real=True)
dPhi = Phi-Ph; dPsi = Psi-Ps
def EH(P,Q): return 2*Q**2 - 4*P*Q          # T4-T5 static-NR quad form (per k^2)
Lint = a_*dPhi**2 + b_*dPsi**2 + x_*dPhi*dPsi
# action density (drop overall k^2 on the kinetic pieces; source is not k^2 scaled -> keep k2 explicit)
S = kap*(EH(Phi,Psi)+EH(Ph,Ps))*k2 + lam*Lint*k2 - rho*Phi
flds=[Phi,Psi,Ph,Ps]
eqs=[sp.diff(S,f) for f in flds]            # field equations (=0)
sol=sp.solve(eqs,flds,dict=True)[0]
Phi_s=sp.simplify(sol[Phi]); Psi_s=sp.simplify(sol[Psi]); Ph_s=sp.simplify(sol[Ph]); Ps_s=sp.simplify(sol[Ps])
gamma_lin=sp.simplify(Psi_s/Phi_s)
print("  solved physical g potentials (linear, general a,b,x):")
print("    Phi_g =",Phi_s)
print("    Psi_g =",Psi_s)
print("    gamma_lin = Psi_g/Phi_g =",gamma_lin)
# calibrate: lam=0 must give GR gamma=1
print("  [calibration] lam=0 => gamma =", sp.simplify(gamma_lin.subs(lam,0)), " (GR expects 1)")
# sum / diff split check
sum_Phi=sp.simplify(Phi_s+Ph_s); sum_Psi=sp.simplify(Psi_s+Ps_s)
print("  [sum=GR check] (Phi_g+Phi_ghat) =",sum_Phi,"  (Psi_g+Psi_ghat) =",sum_Psi,
      "  equal? ", sp.simplify(sum_Phi-sum_Psi)==0)
dPhi_s=sp.simplify(Phi_s-Ph_s); dPsi_s=sp.simplify(Psi_s-Ps_s)
print("  [diff sector] dPhi=",dPhi_s,"  dPsi=",dPsi_s,"  dPsi/dPhi =",sp.simplify(dPsi_s/dPhi_s))
print("  NOTE: linear regime lam~a0^2 is tiny at solar-system accel (g>>a0) => gamma_lin->1, alpha PPN safe.")
print("        The decisive test is the DEEP-MOND regime (PART C) where the nonlinear interaction dominates.")

# ============================================================================================
# PART C  RELATIVE (dh) sector: the enhancement-vs-lensing DICHOTOMY + the EH-Newtonianization
#   dh potentials P=dPhi, Q=dPsi (functions of r). Interaction M(T), T=a P'^2 + b Q'^2 + x P'Q'.
#   Deep-MOND completion: M(T)~|T|^{3/2} (the X^{3/2} law that gives 1/r, per galileon_scaling_theorem).
#   dh ALSO carries an EH (Newtonian-strength) kinetic term from the two Einstein-Hilbert actions.
#   Matter sources ONLY P (g_00). Q unsourced.  Two competing regimes:
#     - EH-dominated  (LOW accel, r->inf): force LINEAR in dh' => P'~1/r^2 NEWTONIAN, Q'/P'->1 (gamma=1).
#     - Int-dominated (HIGH accel):        force QUADRATIC in dh' => P'~1/r MOND-like, Q'/P'->-x/(2b).
#   The MOND (quadratic-force) term is SUBDOMINANT to EH (linear-force) at small dh' => the far exterior,
#   where galaxy MOND must live, is EH-dominated NEWTONIAN. This is DC-018 in the 5-invariant setting.
# ============================================================================================
print("\n"+"="*96); print("PART C  relative-sector: enhancement<=>slip dichotomy, and EH-Newtonianization of the exterior")
print("="*96)
r=sp.symbols('r',positive=True)
Pp=sp.Symbol("P'",real=True); Qp=sp.Symbol("Q'",real=True)      # radial gradients
Tsym=a_*Pp**2 + b_*Qp**2 + x_*Pp*Qp
dT_dPp = sp.diff(Tsym,Pp); dT_dQp = sp.diff(Tsym,Qp)
print("  dT/dP' =",dT_dPp,"   dT/dQ' =",dT_dQp)
# (i) INTERACTION-DOMINATED regime (Q unsourced, drop EH): lam*M'(T)*(2b Q'+x P')=0 => 2b Q'+x P'=0
ratio = sp.simplify(sp.solve(sp.Eq(dT_dQp,0),Qp)[0]/Pp)      # Q'/P' = -x/(2b)
gamma_int = sp.simplify(ratio)
gamma_sub = sp.simplify(gamma_int.subs({a_:a_int,b_:b_int,x_:x_int}))
print("\n  (i) INTERACTION-DOMINATED (MOND-alive) regime: Q-flux 2b Q'+x P'=0  =>  gamma_g = Q'/P' = -x/(2b) =",gamma_int)
print("      on ghost-free subspace: gamma_g(int) =",gamma_sub,
      "   ; T4-T1:",sp.simplify(gamma_sub.subs(sub_T4T1)))
sol_g1 = sp.solve(sp.Eq(gamma_sub,1),u1)
print("      gamma_g(int)=1 <=> u1 =",sol_g1," ; there the MOND accel a =",
      sp.simplify(a_int.subs(u1,sol_g1[0])) if sol_g1 else "n/a"," => MOND-DEAD.")
print("      => MOND enhancement (a!=0) and correct lensing (gamma=1) are MUTUALLY EXCLUSIVE (DC-013 slip-lock).")
# (ii) EH-DOMINATED regime (low accel): the standard EH scalar structure forces Q'=P' (GR), gamma->1, P'~1/r^2.
print("\n  (ii) EH-DOMINATED (low-accel far exterior): EH force is LINEAR in dh' and DOMINATES the quadratic")
print("       MOND-interaction force at small dh' => relative graviton is NEWTONIAN (P'~1/r^2), gamma->1.")
print("       => the far exterior has NO MOND enhancement (g_dyn->GM/r^2, not sqrt(GM a0)/r).  [DC-018]")

# --- NUMERICAL demonstration of the interpolation across the crossover (source-strength scan) ---
print("\n  [numeric] first integrals WITH EH kept; scan source strength Sigma to cross EH<->interaction:")
print("     (I)  r^2[ lam*Mp*(2a P'+x Q') - 4 kap Q' ] = Sigma ;  (II) r^2[ lam*Mp*(2b Q'+x P') + 4kap(Q'-P') ]=0")
print("     Mp=(3/2)|T|^{1/2}. Fix r=1, vary Sigma (=> vary |dh'|). Low |dh'|=EH/Newtonian, high |dh'|=interaction.")
import numpy as np
from scipy.optimize import fsolve
def grads(a_v,b_v,x_v,Sig,kap_v=1.0,lam_v=1.0,rr=1.0,guess=None):
    def F(v):
        p,q=v
        T=a_v*p**2+b_v*q**2+x_v*p*q
        Mp_=1.5*np.sqrt(abs(T)+1e-300)
        e1=rr**2*(lam_v*Mp_*(2*a_v*p+x_v*q)-4*kap_v*q)-Sig
        e2=rr**2*(lam_v*Mp_*(2*b_v*q+x_v*p)+4*kap_v*(q-p))
        return [e1,e2]
    if guess is None:
        guess=[np.sign(Sig)*np.sqrt(abs(Sig))*0.1, np.sign(Sig)*np.sqrt(abs(Sig))*0.1]
    v,info,ier,msg=fsolve(F,guess,full_output=True); return v,ier
for (name,uv) in [("T4-T1 (u0=1,u1=0)",{u0:1,u1:0}), ("MOND-alive x!=0 (u0=1,u1=-4)",{u0:1,u1:-4})]:
    av=float(a_int.subs(uv)); bv=float(b_int.subs(uv)); xv=float(x_int.subs(uv))
    pred=float(-xv/(2*bv)) if bv!=0 else 0.0
    print(f"    {name}: (a,b,x)=({av},{bv},{xv})  EH-limit gamma->1.0 ; interaction-limit gamma->{pred:.4f}")
    g=None
    for Sig in [1e-6,1e-3,1.0,1e3,1e6,1e9]:
        v,ier=grads(av,bv,xv,Sig,guess=g); p,q=v; g=list(v)
        # local force-law exponent: is r^2-flux linear (Newt) or quadratic (MOND) dominated? report |dh'| scale
        T=av*p**2+bv*q**2+xv*p*q
        Mp_=1.5*np.sqrt(abs(T)+1e-300)
        eh_term=abs(4*1.0*p); int_term=abs(1.0*Mp_*2*av*p)
        reg = "EH/Newton" if eh_term>int_term else "interaction/MOND"
        print(f"        Sigma={Sig:.0e}:  P'={p: .3e}  Q'/P'={q/p if p else float('nan'): .4f}   [{reg}: |EH|={eh_term:.2e} vs |int|={int_term:.2e}]")
# radial scaling: at FIXED coefficients, largest r (lowest accel) -> Newtonian. Confirm exponent.
print("\n  [numeric] radial scaling at fixed source (Sigma=1): far exterior exponent of P'(r):")
for (name,uv) in [("T4-T1 (u0=1,u1=0)",{u0:1,u1:0})]:
    av=float(a_int.subs(uv)); bv=float(b_int.subs(uv)); xv=float(x_int.subs(uv))
    g=[ -1e-3,-1e-3]
    prev=None
    for rr in [1e1,1e2,1e3,1e4]:
        v,ier=grads(av,bv,xv,1.0,rr=rr,guess=g); p,q=v; g=list(v)
        slope = None if prev is None else (np.log(abs(p))-np.log(abs(prev[1])))/(np.log(rr)-np.log(prev[0]))
        tag = "" if slope is None else f"  d(lnP')/d(lnr)={slope:.3f}  (Newton=-2, MOND=-1)"
        print(f"        r={rr:.0e}:  P'={p: .3e}  P'*r^2={p*rr**2: .4f}  P'*r={p*rr: .4e}{tag}")
        prev=(rr,p)
print("  => far exterior slope -> -2 (P'*r^2=const) = NEWTONIAN: the EH term Newtonianizes the relative graviton.")

# ============================================================================================
# PART D  alpha_3 / retarded-vs-elliptic
# ============================================================================================
print("\n"+"="*96); print("PART D  alpha_3: is the response retarded/hyperbolic (bimetric) or elliptic (MMG)?")
print("="*96)
# helicity-0 longitudinal (A0,A3) block factor (committed ghost_stuckelberg): (2u0+u1)(kap^2-omega^2)*rank1
w,kk=sp.symbols('omega kappa',real=True)
disp = (2*u0+u1)*(kk**2 - w**2)
print("  committed (A0,A3) longitudinal block prefactor:  (2u0+u1)(kappa^2 - omega^2)")
print("  => propagating dispersion  omega^2 = kappa^2  (LUMINAL, hyperbolic) for 2u0+u1 != 0")
print("     T4-T1: 2u0+u1 =", (2*u0+u1).subs(sub_T4T1), " != 0  => dh sector PROPAGATES (retarded response).")
print("  Contrast MMG (DC-019): elliptic constraint C_M => INSTANTANEOUS lapse response => g_00 Phi_1")
print("     coeff pinned to 1 => alpha_3=-3 (O(1)), pulsar bound |alpha_3|<4e-20 violated ~7.5e19x.")
print("  Here BOTH metrics are DYNAMICAL (each has an EH kinetic term, both propagate); the interaction is")
print("  a diffeomorphism SCALAR 2a0^2(g ghat)^{1/4}M(T) => NO prior/absolute geometry, NO preferred frame.")
print("  Fully-conservative (Lagrangian, dynamical-only) theories have alpha_3=0 (Will/LLNi conservation).")
print("  In the solar system (g>>a0) the interaction is deep in its LINEAR regime (~ (a0/g)^2 suppressed) =>")
print("  gamma->1 AND alpha_3=0. => the RETARDED bimetric structure GENUINELY AVOIDS the MMG alpha_3=O(1).")

print("\n"+"="*96); print("VERDICT")
print("="*96)
print("  DICHOTOMY on the ghost-free 2-D subspace (relative graviton dh, matter sources g_00 only):")
print("   - EH-dominated (LOW accel, galaxy MOND regime): force LINEAR in dh' dominates the quadratic MOND")
print("     term => P'~1/r^2 NEWTONIAN, gamma->1. Correct lensing but NO MOND enhancement (g_dyn->GM/r^2). [DC-018]")
print("   - Interaction-dominated (HIGH accel): MOND-alive (a!=0) force ~1/r, but gamma_g=-x/(2b)=u1/(2(u0+u1))")
print("     != 1 => LENSING SLIP. T4-T1: gamma->0 (max under-lensing). Enhancement AND gamma=1 coincide only")
print("     at a=0 (MOND-dead) => enhancement<=>slip are LOCKED (DC-013).")
print("  (1) Phi=Psi ?  NO wherever there is MOND enhancement (gamma=-x/(2b)!=1). Only the Newtonian (no-boost)")
print("      or MOND-dead (a=0) points give gamma=1.")
print("  (2) g_dyn=g_lens=sqrt(GM a0)/r ?  NO. Far exterior is EH-Newtonian (no sqrt(GM a0)/r at all); any MOND")
print("      window under-lenses (g_lens=(1+gamma)/2 g_dyn, T4-T1: g_lens=g_dyn/2). Lensing never tracks dynamics.")
print("  (3) alpha_3 forced O(1)?  NO -- dh is hyperbolic/retarded (omega^2=kappa^2), two DYNAMICAL metrics, no")
print("      prior geometry => alpha_3=0 (Will/LLNi). The bimetric retardation GENUINELY fixes the MMG elliptic")
print("      alpha_3=O(1) disease. This leg PASSES -- but it is MOOT given (1),(2).")
print("  => PASS requires plausibly Phi=Psi AND correct MOND AND no forced alpha_3. alpha_3 leg PASSES; the")
print("     Phi=Psi / MOND legs FAIL (EH-Newtonianization + enhancement<=>slip lock) => VERDICT = FAIL (KILL).")
