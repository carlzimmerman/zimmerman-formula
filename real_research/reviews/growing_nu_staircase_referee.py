#!/usr/bin/env python3
"""
GROWING-nu REFEREE RESTART: staircase m_nu(z)=m0*sqrt(rho_DE(z)/rho_DE0), CPL-literal (w0,wa)=(-0.727,-1.05)
[task footing; NB repo's own dr2_sensitivity labels this the DR1 DESY5 point -- DR2 DESY5 central =(-0.752,-0.86),
run as m(z)-history fork, no extra CAMB]. Piecewise-constant m in 4 vs 8 z-shells via CAMB; growth-matched stitch
P(k,z); convergence; step + amplitude-marginalized Fisher vs the published endpoint bracket (0.65%/1.4%; 1.4/3.9 sig).
Conventions mirror real_research/reviews/growing_nu_camb_fisher.py exactly (same params, ksel, Veff, nbar, ZS).
"""
import numpy as np, camb

H0, ombh2, omch2, ns, As = 67.4, 0.02237, 0.1200, 0.9649, 2.1e-9
ZS_OBS = [0.0, 0.5, 1.0]; KMAX = 2.0
W0, WA = -0.727, -1.05
W0b, WAb = -0.752, -0.86      # DR2 DESY5 published central (fork, history-only)

def rho_ratio(z, w0=W0, wa=WA):
    return (1.0+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
def m_of_z(z, Sig, w0=W0, wa=WA):
    return Sig*np.sqrt(rho_ratio(z, w0, wa))

_cache = {}
def camb_pk(mnu, zs):
    key = (round(mnu,6), tuple(np.round(zs,4)))
    if key in _cache: return _cache[key]
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=max(mnu,1e-3),
                       num_massive_neutrinos=3, omk=0)
    pars.InitPower.set_params(As=As, ns=ns)
    pars.set_matter_power(redshifts=list(zs), kmax=KMAX)
    pars.NonLinear = camb.model.NonLinear_none
    r = camb.get_results(pars)
    kh, zret, pk = r.get_matter_power_spectrum(minkh=2e-3, maxkh=KMAX, npoints=240)
    out = (kh, {round(float(z),4): pk[i] for i,z in enumerate(zret)})
    _cache[key] = out; return out

def shell_masses(bounds, Sig):
    ms = []
    for i in range(1, len(bounds)):
        x = np.linspace(np.log1p(bounds[i-1]), np.log1p(bounds[i]), 400)
        ms.append(float(np.trapz(m_of_z(np.expm1(x), Sig), x)/(x[-1]-x[0])))
    return ms

def stitch_lnP(bounds, ms, zall, zobs):
    """growth-matched stitch: propagate through shells top-down with each shell's constant-mass run"""
    N = len(ms); runs = [camb_pk(ms[i], zall) for i in range(N)]
    kh = runs[0][0]
    lnP = np.log(runs[N-1][1][round(bounds[N],4)])           # anchor at top (m~0 there, error O(f_nu^top))
    i = N
    while i >= 1:
        ztop, zbot = round(bounds[i],4), round(bounds[i-1],4)
        P = runs[i-1][1]
        if zobs >= zbot - 1e-9:
            lnP = lnP + np.log(P[round(zobs,4)]) - np.log(P[ztop]); return kh, lnP
        lnP = lnP + np.log(P[zbot]) - np.log(P[ztop]); i -= 1
    return kh, lnP

def fisher_snr(kh, lnratios):
    ksel = (kh>0.008)&(kh<0.2); Veff, nbar = 20.0, 1e-3; snr2 = 0.0
    for (sig_full, Pz_full) in lnratios:
        sig = sig_full[ksel] - sig_full[ksel].mean()          # amplitude/DE-degenerate part removed
        Pz = Pz_full[ksel]; k = kh[ksel]; dk = np.gradient(k)
        Nm = Veff*1e9*k**2*dk/(2*np.pi**2); w = (Pz/(Pz+1.0/nbar))**2
        snr2 += np.sum(0.5*Nm*w*sig**2)
    return np.sqrt(snr2)

def step_z0(kh, lnr):
    r = np.exp(lnr); sL = 1-r[kh>0.2].mean(); sS = 1-r[kh<0.01].mean(); return sL-sS, sL, sS

print("="*100)
print(" STAIRCASE m_nu(z)=m0*sqrt(rho_DE/rho_DE0), CPL (w0,wa)=(-0.727,-1.05): 4 vs 8 shells, stitched CAMB")
print("="*100)
zt = np.array([0,0.35,0.5,1,2,3,4.6,10,20,50])
print(" m(z)/m0 task-CPL : " + " ".join(f"z={z:g}:{np.sqrt(rho_ratio(z)):.3f}" for z in zt))
print(" m(z)/m0 DR2-cent : " + " ".join(f"z={z:g}:{np.sqrt(rho_ratio(z,W0b,WAb)):.3f}" for z in zt))
print(" (fork note: DR2 central less phantom -> mass higher at high z -> staircase closer to constant-mass)")

B4 = [0.0, 1.0, 3.0, 10.0, 50.0]
B8 = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]
results = {}
for Sig in (0.059, 0.10):
    print(f"\n--- Sigma_today = {Sig:.3f} eV ---")
    zall = sorted(set([round(z,4) for z in B8+ZS_OBS]))
    khN, dnull = camb_pk(1e-3, zall)                          # ~massless null (CMB-anchored fit, m_CMB~0.0014*m0)
    # (0) endpoint-bracket reproduction (published convention: const Sig vs const 0.6*Sig)
    _, dhi = camb_pk(Sig, zall); _, dlo = camb_pk(0.6*Sig, zall)
    lnr_ep = {z: np.log(dhi[round(z,4)])-np.log(dlo[round(z,4)]) for z in ZS_OBS}
    st_ep,_,_ = step_z0(khN, lnr_ep[0.0])
    snr_ep = fisher_snr(khN, [(lnr_ep[z], 0.5*(dhi[round(z,4)]+dlo[round(z,4)])) for z in ZS_OBS])
    print(f"  [calib] endpoint bracket reproduction: step={100*st_ep:.2f}%  SNR={snr_ep:.1f} (published 0.65/1.4 | 1.40/3.9)")
    for lab, B in (("4-shell", B4), ("8-shell", B8)):
        ms = shell_masses(B, Sig)
        lnr = {}; Pmid = {}
        for z in ZS_OBS:
            kh, lnP = stitch_lnP(B, ms, zall, z)
            lnr[z] = lnP - np.log(dnull[round(z,4)])
            Pmid[z] = 0.5*(np.exp(lnP)+dnull[round(z,4)])
        st, sL, sS = step_z0(kh, lnr[0.0])
        snr = fisher_snr(kh, [(lnr[z], Pmid[z]) for z in ZS_OBS])
        results[(Sig,lab)] = (st, snr, ms)
        print(f"  {lab}: masses(eV)={['%.4f'%m for m in ms]}")
        print(f"    stitched vs massless-CMB-fit: z=0 supp k>0.2 {100*sL:.2f}% | k<0.01 {100*sS:.2f}% | STEP={100*st:.2f}%  SNR={snr:.1f}")
    st4,snr4,_ = results[(Sig,"4-shell")]; st8,snr8,_ = results[(Sig,"8-shell")]
    print(f"  CONVERGENCE 4->8: step {100*st4:.2f}->{100*st8:.2f}% ({100*abs(st8-st4)/max(abs(st8),1e-9):.0f}% shift), SNR {snr4:.1f}->{snr8:.1f}")
    # best-fit CONSTANT-mass null (honest absorption check): min SNR over constant m_c
    grid = [0.2*Sig, 0.35*Sig, 0.5*Sig, 0.65*Sig, 0.8*Sig, Sig]
    best = (1e9, None)
    ms8 = results[(Sig,"8-shell")][2]
    for mc in grid:
        _, dc = camb_pk(mc, zall)
        pairs = []
        for z in ZS_OBS:
            kh, lnP = stitch_lnP(B8, ms8, zall, z)
            pairs.append((lnP-np.log(dc[round(z,4)]), 0.5*(np.exp(lnP)+dc[round(z,4)])))
        s = fisher_snr(kh, pairs)
        if s < best[0]: best = (s, mc)
    print(f"  best-fit-constant-mass absorption: residual SNR={best[0]:.1f} at m_c={best[1]:.3f} eV "
          f"(vs {snr8:.1f} against the massless CMB fit)")

print("\n"+"="*100)
print(" TWO-TRACER NOTE (illustrative ceiling, NOT in-hand): adding DESI-like tracer Veff=10 Gpc^3/h^3, nbar=4e-4,")
print(" independent-volume quadrature -> SNR x ~1.15-1.25; real multi-tracer needs overlap covariance + bias marg.")
print("="*100)
