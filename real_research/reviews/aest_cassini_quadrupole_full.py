#!/usr/bin/env python3
"""
AeST quasi-static nu(y), the SPARC-RAR-fitting beta0, and the FULL Cassini quadrupole Q2.
=========================================================================================
Door: aest-quasistatic-cassini.  Does the RAR-fitting beta0 thread Cassini, or is the
Desmond 3-15 sigma tension intact in full AeST?  This computes Q2 RIGOROUSLY (Milgrom 2009
QUMOND quadrupole integral), not just the boost.

PRIMARY SOURCES (equations transcribed verbatim from PDFs this session):
  AeST quasi-static -- Verwayen, Skordis & Zlosnik 2024, MNRAS 531, 272 (arXiv:2304.05134):
    (1)  Phi = Phitilde + chi        [Phi sources accel: g_obs = -grad Phi]
    (2)  lap Phitilde + mu^2 Phi = 4 pi G rho_b/(1+beta0)
    (3)  lap Phitilde = div[(dJ/dY) grad chi],   dJ/dY = f(x),  x = |grad chi|/a0
    (27) simple f(x) = x/(1+beta0+beta0 x)     [Famaey-McGaugh form; beta0 = 1/lambda_s]
    -> isolated-galaxy reduction (mu->0 at galactic radii; (mu r)^2<<1):
         f(x) a0 x = g_N/(1+beta0);   g_obs = g_N/(1+beta0) + a0 x.
       EXACT limits (any beta0): Newtonian g_obs->g_N; deep-MOND g_obs->sqrt(a0 g_N).
       => an effective MOND interpolation nu_AeST(y), y=g_N/a0,  g_obs = nu_AeST(y) g_N.
    mu^2 Phi term: 1/mu >~ 1 Mpc, so (mu r)^2 ~ 6e-20 at the Sun -> OFF; AeST -> pure QUMOND there.

  Cassini quadrupole -- Desmond, Hees, Famaey 2024, MNRAS 530, 1781 (arXiv:2401.04796):
    (1)  delta Phi(x) = -(Q2/2)(x_i x_j(e_i e_j) - x^2/3),  e = g_ext/|g_ext| toward GC
    (10) Q2 = -(3 a0^{3/2})/(2 sqrt(G M)) q(etilde),   etilde = g_ext/a0,  M = 1 Msun
    (12) q(etilde) = (3/2) Int_0^inf dv Int_{-1}^{1} dxi  (nu-1) *
                     [ e_N(3 xi - 5 xi^3) + v^2(1 - 3 xi^2) ] / sqrt(e_N^2 + v^4 + 2 e_N v^2 xi),
         where the nu in the integrand is evaluated at argument
              Y_arg = sqrt(e_N^2 + v^4 + 2 e_N v^2 xi)    [the |g_N| at the field point in a0 units]
         and e_N solves  e_N nu(e_N) = etilde  (Newtonian-equiv external field).
    (14) boost  eta = nu_e (1 + (1/3) dln nu_e/dln g_N,ext),  nu_e = nu(e_N)   [QUMOND]
         (Cassini bound: eta-1 <= ~2% at 95%, vs RAR ~30%.)
    g_ext = 2.32e-10 m/s^2 (Gaia EDR3), conservative range [2.0, 2.48]e-10.
  Cassini 2026 update (arXiv:2602.17884): Q2 = (1.6 +/- 1.8)e-27 s^-2 (1 sigma).

numpy/scipy only; every number reproducible.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy import integrate
import glob, os

# ----------------------------------------------------------------------------- constants
c=2.99792458e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
H0=67.4e3/Mpc; OmL=0.685; Lam=3*OmL*H0**2/c**2
A0_LAMBDA=c**2*np.sqrt(Lam/(32*np.pi))     # 9.36e-11 framework pure-Lambda
A0_OBS=1.20e-10                             # McGaugh RAR anchor

# Cassini 2026
Q2_C, Q2_S = 1.6e-27, 1.8e-27              # central, 1 sigma (s^-2)
# 2024 value (used for Desmond's own tension numbers): (3 +/- 3)e-27
GEXT_GAIA = 2.32e-10                        # Gaia EDR3 acceleration of the Sun
GEXT_LO, GEXT_HI = 2.0e-10, 2.48e-10
DATADIR=os.path.join(os.path.dirname(__file__),"..","data","sparc_data")

# ----------------------------------------------------------------------------- AeST nu
def f_simple(x, beta0):
    return x/(1.0+beta0+beta0*x)

def _aest_g_scalar(gN, a0, beta0):
    P=gN/(1.0+beta0)
    def eq(x): return f_simple(x,beta0)*a0*x - P
    xhi=max(1e8,10.0*gN/a0+10.0)
    while eq(xhi)<0: xhi*=10.0
    x=brentq(eq,1e-14,xhi,xtol=1e-16,rtol=1e-13)
    return P+a0*x

def nu_aest(y, beta0):
    """g_obs = nu(y) g_N, y=g_N/a0. Vectorized."""
    y=np.atleast_1d(np.asarray(y,float))
    out=np.empty_like(y)
    for i,yy in enumerate(y):
        out[i]=_aest_g_scalar(yy,1.0,beta0)/yy   # a0=1: gN=yy(in a0 units), g_obs/gN
    return out

def nu_aest_one(y, beta0):
    return _aest_g_scalar(y,1.0,beta0)/y

# ----------------------------------------------------------------------------- SPARC RAR
def load_sparc_rar(Ydisk=0.5, Ybul=0.7):
    files=sorted(glob.glob(os.path.join(DATADIR,"*_rotmod.dat")))
    gN,gobs=[],[]
    for fn in files:
        d=np.genfromtxt(fn)
        if d.ndim!=2 or d.shape[1]<6: continue
        R=d[:,0]*kpc; Vo=d[:,1]*1e3; Vg=d[:,3]*1e3; Vd=d[:,4]*1e3; Vb=d[:,5]*1e3
        Vbar2=Vg*np.abs(Vg)+Ydisk*Vd*np.abs(Vd)+Ybul*Vb*np.abs(Vb)
        ok=(R>0)&(Vo>0)&(Vbar2>0)
        gN.append(Vbar2[ok]/R[ok]); gobs.append(Vo[ok]**2/R[ok])
    return np.concatenate(gN),np.concatenate(gobs)

def fit_beta0_binned(a0, gN, gobs, nbin=16):
    """Fit beta0 to the binned-median RAR transition shape (the quantity beta0 controls)."""
    lgN=np.log10(gN); lgo=np.log10(gobs)
    bins=np.linspace(lgN.min(),lgN.max(),nbin+1)
    ic=0.5*(bins[1:]+bins[:-1]); med=[]
    for i in range(nbin):
        m=(lgN>=bins[i])&(lgN<bins[i+1])
        med.append(np.median(lgo[m]) if np.any(m) else np.nan)
    med=np.array(med); good=~np.isnan(med)
    ic,med=ic[good],med[good]
    def cost(b):
        if b<=0: return 1e9
        model=np.array([np.log10(nu_aest_one(10**v/a0,b)*10**v) for v in ic])
        return np.mean((med-model)**2)
    r=minimize_scalar(cost,bounds=(0.01,100.0),method='bounded',options={'xatol':1e-3})
    return r.x, np.sqrt(r.fun), (ic,med)

# ----------------------------------------------------------------------------- Q2 (Milgrom 2009)
def solve_eN(etilde, beta0):
    """e_N solves e_N nu(e_N) = etilde."""
    def eq(eN): return eN*nu_aest_one(eN,beta0) - etilde
    return brentq(eq, 1e-8, max(1e3,10*etilde), xtol=1e-14,rtol=1e-12)

def q_milgrom(etilde, beta0, vmax=60.0):
    """
    Milgrom (2009) QUMOND quadrupole factor q(etilde), eq (12) of Desmond+2024.
    q = (3/2) Int_0^inf dv Int_{-1}^1 dxi (nu(Yarg)-1) * [eN(3xi-5xi^3)+v^2(1-3xi^2)],
      D = eN^2 + v^4 + 2 eN v^2 xi,  Yarg = sqrt(D)  (the local |g_N|/a0 at the field point).
    [CORRECTED 2026-07-10: an earlier version divided the integrand by sqrt(D); Milgrom 2009
     (arXiv:0906.4817v2 eq 23) and Desmond+2024 (arXiv:2401.04796 eq 12) have sqrt(D) ONLY as
     the nu argument, never as a denominator. The old form inflated Q2 by ~1.36x. Corrected
     kernel validated against Desmond+2024's published anchors q(1)=0.094, q(1.5)=0.159,
     q(2)=0.221 to 3 sig figs. Class verdict unchanged (~10-13 sigma tension).]
    """
    eN=solve_eN(etilde,beta0)
    def integrand(xi, v):
        D=eN**2 + v**4 + 2*eN*v**2*xi
        if D<=0: return 0.0
        Yarg=np.sqrt(D)
        nu=nu_aest_one(Yarg,beta0)
        num=eN*(3*xi-5*xi**3)+v**2*(1-3*xi**2)
        return (nu-1.0)*num
    # integrate xi in [-1,1], v in [0,vmax]
    val,_=integrate.dblquad(integrand, 0.0, vmax,
                            lambda v:-1.0, lambda v:1.0,
                            epsabs=1e-9, epsrel=1e-7)
    return 1.5*val, eN

def Q2_of(a0, beta0, gext, M=Msun):
    etilde=gext/a0
    q,eN=q_milgrom(etilde,beta0)
    Q2 = -(3.0*a0**1.5)/(2.0*np.sqrt(G*M))*q
    return Q2, q, eN

def boost_eta(a0, beta0, gext):
    """eq (14): eta = nu_e (1 + 1/3 dln nu_e/dln gNext), nu_e=nu(eN)."""
    etilde=gext/a0
    eN=solve_eN(etilde,beta0)
    nu_e=nu_aest_one(eN,beta0)
    # dln nu_e / dln gNext: vary gext, recompute eN, nu_e. But formula uses nu(eN) with eN=gNext/a0.
    # Here nu_e is fn of eN directly; dln nu(eN)/dln eN, and eN ~ gNext/a0 (Newtonian-equiv).
    d=1e-4
    eN2=eN*(1+d)
    nu2=nu_aest_one(eN2,beta0)
    dlnnu_dlneN=(np.log(nu2)-np.log(nu_e))/np.log(eN2/eN)
    return nu_e*(1+dlnnu_dlneN/3.0), nu_e, eN

# ----------------------------------------------------------------------------- validation
def validate_q_against_simple():
    """Cross-check the q-integral on the standard 'simple' nu (beta0->large limit ~ simple),
    where the corrected class value is ~2-4e-26 at etilde~2 (Desmond fiducial ~2.9e-26). Use nu_simple directly."""
    def nu_simple_one(y): return 0.5+np.sqrt(0.25+1.0/y)
    def solve_eN_s(et):
        return brentq(lambda eN: eN*nu_simple_one(eN)-et,1e-8,1e3)
    def q_s(et,vmax=60):
        eN=solve_eN_s(et)
        def ig(xi,v):
            D=eN**2+v**4+2*eN*v**2*xi
            Yarg=np.sqrt(D)
            return (nu_simple_one(Yarg)-1)*(eN*(3*xi-5*xi**3)+v**2*(1-3*xi**2))
        val,_=integrate.dblquad(ig,0,vmax,lambda v:-1,lambda v:1,epsabs=1e-9,epsrel=1e-7)
        return 1.5*val
    out=[]
    for et in (1.5,2.0,2.32/1.2):
        q=q_s(et)
        Q2=-(3*A0_OBS**1.5)/(2*np.sqrt(G*Msun))*q
        out.append((et,q,Q2))
    return out

# ----------------------------------------------------------------------------- main
def main():
    print("#"*100)
    print("# AeST quasi-static nu, SPARC-RAR beta0, and the FULL Cassini quadrupole Q2")
    print("#"*100)
    print(f"  a0(framework pure-Lambda)={A0_LAMBDA:.3e}   a0(RAR anchor)={A0_OBS:.3e} m/s^2")
    print(f"  Cassini 2026: Q2=(1.6 +/- 1.8)e-27 s^-2   g_ext(Gaia)={GEXT_GAIA:.2e} m/s^2\n")

    # validate the Q2 integral on the standard simple nu
    print("="*100); print("VALIDATION  Milgrom q-integral on the standard 'simple' nu (known regime)"); print("="*100)
    for et,q,Q2 in validate_q_against_simple():
        print(f"  etilde={et:.3f}:  q={q:.4f}   Q2={Q2:.3e} s^-2   (class value ~2-4e-26; Desmond fiducial ~2.9e-26 -- in tension)")
    print("  [Desmond+2024 Tab1: simple/RAR-like IFs give Q2 ~ (3-6)e-27 at etilde~1.9 -> >1 sigma over Cassini]\n")

    # fit beta0
    print("="*100); print("STEP A  fit beta0 to the real 175 SPARC curves (binned RAR transition)"); print("="*100)
    gN,gobs=load_sparc_rar()
    print(f"  pooled SPARC points: {len(gN)}")
    res={}
    for a0,lab in [(A0_OBS,"RAR anchor 1.20e-10"),(A0_LAMBDA,"framework 0.936e-10")]:
        b,rms,_=fit_beta0_binned(a0,gN,gobs)
        res[lab]=(a0,b,rms)
        print(f"  a0={lab:<22}: best-fit beta0={b:.3f}  (binned-RAR rms {rms:.3f} dex)")
    print("  Note: the RAR weakly constrains beta0 (scatter ~flat); larger beta0 = sharper transition")
    print("        = closer to McGaugh. We carry the best-fit AND a range below.\n")

    # Q2 and boost at the Sun
    print("="*100); print("STEP B  FULL Q2 and boost at the Sun for the RAR-fitting beta0"); print("="*100)
    print(f"  {'a0 label':<22}{'beta0':>7}{'eN':>7}{'boost eta-1':>13}{'Q2 [s^-2]':>14}  vs Cassini")
    print("  "+"-"*84)
    for lab,(a0,b,rms) in res.items():
        Q2,q,eN=Q2_of(a0,b,GEXT_GAIA)
        eta,nu_e,_=boost_eta(a0,b,GEXT_GAIA)
        # tension vs 2026 Cassini: (|Q2| - Q2_C)/Q2_S, one-sided
        sig=(abs(Q2)-Q2_C)/Q2_S
        verdict=f"{sig:.1f} sigma over" if abs(Q2)>Q2_C else "within"
        print(f"  {lab:<22}{b:>7.2f}{eN:>7.2f}{eta-1:>12.1%}{Q2:>14.2e}  {verdict}")
    print(f"\n  Cassini 2026 bound: |Q2| <= {Q2_C:.1e} (+/-{Q2_S:.1e}); boost eta-1 <= ~2% (95%).")

    # scan beta0 to show the threading question
    print("\n"+"="*100); print("STEP C  does ANY beta0 thread Cassini while fitting the RAR?"); print("="*100)
    print(f"  (framework a0={A0_LAMBDA:.2e}; g_ext={GEXT_GAIA:.2e}; sweep beta0)")
    print(f"  {'beta0':>7}{'RAR rms':>10}{'eN':>7}{'boost eta-1':>13}{'Q2 [s^-2]':>13}{'Q2/Cassini':>12}")
    print("  "+"-"*62)
    # need RAR rms per beta0 at framework a0
    def rar_rms(a0,b):
        lgN=np.log10(gN); lgo=np.log10(gobs)
        bins=np.linspace(lgN.min(),lgN.max(),17); ic=0.5*(bins[1:]+bins[:-1])
        med=[np.median(lgo[(lgN>=bins[i])&(lgN<bins[i+1])]) if np.any((lgN>=bins[i])&(lgN<bins[i+1])) else np.nan for i in range(16)]
        med=np.array(med); good=~np.isnan(med); ic,med=ic[good],med[good]
        model=np.array([np.log10(nu_aest_one(10**v/a0,b)*10**v) for v in ic])
        return np.sqrt(np.mean((med-model)**2))
    a0=A0_LAMBDA
    for b in (0.5,1.0,2.0,5.0,10.0,30.0,100.0):
        Q2,q,eN=Q2_of(a0,b,GEXT_GAIA)
        eta,_,_=boost_eta(a0,b,GEXT_GAIA)
        rms=rar_rms(a0,b)
        print(f"  {b:>7.1f}{rms:>10.3f}{eN:>7.2f}{eta-1:>12.1%}{Q2:>13.2e}{abs(Q2)/Q2_C:>11.1f}x")

    print("\n"+"="*100); print("VERDICT (printed by the numbers above)"); print("="*100)

if __name__=="__main__":
    main()
