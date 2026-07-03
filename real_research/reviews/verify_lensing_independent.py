#!/usr/bin/env python3
"""Independent adversarial verification of confront_lensing_rar.py.
Different code path: closed-form deep-MOND WLS estimator + scipy minimize,
plus units audit (Brouwer ESD->g, G in pc^3/Msun/s^2, h-scaling)."""
import numpy as np
from scipy.optimize import minimize_scalar

A0F, A0M = 9.36e-11, 1.20e-10
M24 = np.array([[-11.41,-10.65,.06,.03],[-11.65,-10.78,.06,.03],[-11.90,-10.88,.06,0],
 [-12.15,-11.00,.06,0],[-12.39,-11.11,.05,.02],[-12.64,-11.21,.05,0],[-12.89,-11.29,.05,.01],
 [-13.13,-11.47,.05,.02],[-13.38,-11.59,.05,.01],[-13.63,-11.76,.06,.03],[-13.87,-11.93,.07,.05],
 [-14.12,-12.08,.07,.07],[-14.37,-12.27,.08,.13],[-14.61,-12.44,.08,.25],[-14.86,-12.85,.12,.67]])
B21K = np.array([[-11.407,-10.719,.053],[-11.654,-10.730,.041],[-11.900,-10.840,.040],
 [-12.147,-10.964,.040],[-12.393,-11.018,.035],[-12.640,-11.167,.037],[-12.887,-11.223,.032],
 [-13.133,-11.393,.036],[-13.380,-11.456,.032],[-13.626,-11.660,.039],[-13.873,-11.772,.038],
 [-14.120,-11.835,.034],[-14.366,-12.004,.039],[-14.613,-12.146,.042],[-14.859,-12.372,.055]])

def fw(g,a0): return np.sqrt(g*g+g*a0)
def mcg(g,a0): return g/(-np.expm1(-np.sqrt(g/a0)))

def chi2(la0,x,y,s,mod,d=0.0):
    return np.sum(((y-np.log10(mod(10**(x+d),10**la0)))/s)**2)

def freefit(x,y,s,mod=fw):
    r = minimize_scalar(lambda l: chi2(l,x,y,s,mod), bounds=(-11.5,-8.5), method='bounded')
    la = r.x; c0 = r.fun
    # 1-sigma from Delta-chi2=1 via bisection each side
    def cross(sgn):
        lo,hi = 0.0, 1.5
        for _ in range(60):
            m=(lo+hi)/2
            if chi2(la+sgn*m,x,y,s,mod)-c0 < 1: lo=m
            else: hi=m
        return (lo+hi)/2
    return la, c0, cross(+1), cross(-1)

# ---- 1. UNITS AUDIT ----
G_si, Msun, pc = 6.674e-11, 1.989e30, 3.0857e16
Gpc = G_si*Msun/pc**3
print(f"G in pc^3/(Msun s^2) = {Gpc:.4e}  (script uses 4.52e-30) -> {'OK' if abs(Gpc/4.52e-30-1)<0.01 else 'FAIL'}")
# g = 4 G ESD (ESD in Msun/pc^2) gives g in pc/s^2; *pc_in_m -> m/s^2. Dimensional: OK.
# h-scaling: gbar = G M/r^2, M~h70^-2, r~h70^-1 => gbar ~ h70^0; gobs = 4G*ESD, ESD ~ h70 Msun/pc^2
# => gobs ~ h70^1. B21 quotes h70=1 (H0=70): identity, no double-scaling. M24 uses H0=73 explicitly
# in their masses; tables are as-published accelerations -> no h correction should be applied. OK.
print("h-scaling: B21 h70=1 identity; both tables published in physical m/s^2 -> no correction. OK")

# ---- 2. fixed-a0 ladder (independent chi2 code) ----
lg,lo = M24[:,0],M24[:,1]
s_ss = np.hypot(M24[:,2],M24[:,3]); s_ssm = np.sqrt(M24[:,2]**2+M24[:,3]**2+0.01)
for nm,s in [("stat+sys",s_ss),("stat+sys+0.1",s_ssm)]:
    for cn,cut in [("REL",-13.001),("EXT",-14.001),("FULL",-99)]:
        m = lg>cut
        c = chi2(np.log10(A0F),lg[m],lo[m],s[m],fw)/m.sum()
        print(f"M24 {nm:13s} {cn}: chi2/dof(fw,9.36e-11) = {c:.2f}")
# reference
m = lg>-13.001
print(f"M24 ref mcg@1.2e-10 stat+sys REL: {chi2(np.log10(A0M),lg[m],lo[m],s_ss[m],mcg)/m.sum():.2f}")

# ---- 3. free-a0 + closed-form deep-limit cross-check ----
for cn,cut in [("REL",-13.001),("EXT",-14.001)]:
    m = lg>cut
    la,c0,ep,em = freefit(lg[m],lo[m],s_ss[m])
    # closed-form deep-MOND WLS: log gobs = 0.5(log gbar + log a0) => la0 = mean_w(2*lo - lg)
    w = 1/s_ss[m]**2
    la_cf = np.sum(w*(2*lo[m]-lg[m]))/np.sum(w)
    nsF = np.sqrt(max(chi2(np.log10(A0F),lg[m],lo[m],s_ss[m],fw)-c0,0))
    nsM = np.sqrt(max(chi2(np.log10(A0M),lg[m],lo[m],s_ss[m],fw)-c0,0))
    print(f"M24 stat+sys {cn}: a0_hat={10**la:.3e} (+{ep:.3f}/-{em:.3f}), closed-form deep={10**la_cf:.3e}, "
          f"9.36e-11 at +{nsF:.1f}s, 1.2e-10 at +{nsM:.1f}s")
    la2,c02,ep2,_ = freefit(lg[m],lo[m],s_ssm[m])
    print(f"    with +0.1 M* quad: a0_hat={10**la2:.3e}, 9.36e-11 at "
          f"+{np.sqrt(max(chi2(np.log10(A0F),lg[m],lo[m],s_ssm[m],fw)-c02,0)):.1f}s")
kg,ko,ks = B21K[:,0],B21K[:,1],B21K[:,2]; kt = np.sqrt(ks**2+0.01)
for cn,cut in [("REL",-13.001),("EXT",-14.001)]:
    m = kg>cut
    la,c0,ep,em = freefit(kg[m],ko[m],kt[m])
    print(f"B21K stat+0.1 {cn}: a0_hat={10**la:.3e} (+/-{ep:.3f})")

# ---- 4. delta* degeneracy: exact deep-MOND analytic ----
m = lg>-13.001
la0,_,_,_ = freefit(lg[m],lo[m],s_ss[m])
for d in (0.10,0.20,0.201,0.210):
    lad,_,_,_ = freefit(lg[m]+d,lo[m],s_ss[m])
    print(f"delta={d:+.3f}: a0_hat={10**lad:.3e} vs analytic {10**(la0-d):.3e} "
          f"(ratio {10**lad/10**(la0-d):.4f})")
dstar_fw = la0-np.log10(A0F); dstar_mo = la0-np.log10(A0M)
print(f"delta*(9.36e-11)={dstar_fw:+.3f}, delta*(1.2e-10)={dstar_mo:+.3f}, diff={dstar_fw-dstar_mo:.4f} (fork 0.1079)")

# ---- 5. profiled fork Dchi2 (independent 2D profiling) ----
dg = np.linspace(-0.6,0.8,1401)
def prof(x,y,s,a0,pen):
    return min(chi2(np.log10(a0),x,y,s,fw,d)+pen(d) for d in dg)
penA = lambda d: (d/0.2)**2
penB = lambda d: 0.0 if 0<=d<=0.3 else (min(abs(d),abs(d-0.3))/0.2)**2
for nm,(x,y,s) in [("M24",(lg,lo,s_ss)),("B21K",(kg,ko,kt))]:
    for cn,cut in [("REL",-13.001),("EXT",-14.001)]:
        m = x>cut
        dA = prof(x[m],y[m],s[m],A0F,penA)-prof(x[m],y[m],s[m],A0M,penA)
        dB = prof(x[m],y[m],s[m],A0F,penB)-prof(x[m],y[m],s[m],A0M,penB)
        print(f"{nm} {cn}: Dchi2 priorA={dA:+.2f}, priorB={dB:+.2f}")

# ---- 6. correlated-normalization check: is the 0.82 quadrature ladder honest? ----
# Proper treatment of the 0.1 dex mass-norm sys = a fully correlated nuisance shift.
m = lg>-13.001
c_fix = prof(lg[m],lo[m],s_ss[m],A0F,lambda d:(d/0.1)**2)  # 0.1 dex Gaussian norm nuisance
lam,c0m,_,_ = freefit(lg[m],lo[m],s_ss[m])
print(f"correlated 0.1-dex-norm treatment: chi2p(9.36e-11)={c_fix:.2f}/{m.sum()-1} = {c_fix/(m.sum()-1):.2f} "
      f"(quadrature ladder gave 0.82); Dchi2 vs free = {c_fix-c0m:.2f} -> {np.sqrt(max(c_fix-c0m,0)):.1f}sigma")
print("DONE")
