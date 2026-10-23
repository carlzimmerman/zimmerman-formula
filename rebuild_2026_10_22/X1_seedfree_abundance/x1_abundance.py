"""X1: cold abundance from the actual high-H state, no seed (FROZEN_CRITERIA §2 E3/E4, controls, isocurvature, map).

Inputs carried from earlier epochs (all derived in this lane): the box zero modes (x1_stochastic.py), the Phi bath's
conformal energy E_Phi (E1 lattice; conformal energy is conserved in the radiation-era quartic sector), the free-X
adiabatic invariant (exact Bessel / numeric), the in-bath absorption rate of the X condensate (x1_dmc.py, Codex's
amplitude). Usage: python3 x1_abundance.py point <Hinf> <Trh|inst> [--patch p50] [--closures L,K,C] [--tag T]
                   python3 x1_abundance.py control <Hinf> <Trh|inst>
Writes abundance/<tag>.json. Units GeV.
"""
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, str(Path(__file__).resolve().parent))
import x1_relic as R
from x1_relic import m, M, g, lam, MPL

HERE = Path(__file__).resolve().parent; OUTD = HERE/'abundance'; OUTD.mkdir(exist_ok=True)
H_PRIMARY = 1.3445177278709404e10


def lattice_E():
    """Conformal Phi energy (H^4 units, a_e = 1): 64^3 TW_full p50 endpoint; other patches scaled by the 32^3 ratios."""
    e64 = json.loads((HERE/'lattice/P64_TW_p50_s1.json').read_text())['rows'][-1]['Ephi_phys']
    r = {}
    base = json.loads((HERE/'lattice/P32_TW_p50_s1.json').read_text())['rows'][-1]['Ephi_phys']
    for p in ('p10', 'p50', 'p90'):
        e = json.loads((HERE/f'lattice/P32_TW_{p}_s1.json').read_text())['rows'][-1]['Ephi_phys']
        r[p] = e64*e/base
    return r


def patch_amps():
    st = json.loads((HERE/'x1_stochastic_kmin0.08_Ne60.json').read_text())['box']
    out = {}
    for p, z in st['zero_modes'].items():
        out[p] = dict(X=float(np.hypot(*z['x0'])), Phi=float(np.hypot(*z['phi0'])))
    out['quantiles'] = st['quantiles']
    return out


def E_hom(phi0):
    """Homogeneous conformal energy at tau = 0 for |Phi0|/H = phi0 (slow-roll velocity), used only for ratios."""
    pi0 = phi0-(2/3)*lam*phi0**3
    return pi0**2+lam*phi0**4


def md_ratio(Trh, Hinf, phi0):
    """rho_Phi a^4 late, MD (w=0 until a_rh) relative to instant radiation, homogeneous quartic oscillator (conformal)."""
    if Trh is None: return 1.
    vis = R.Vis(Hinf, Trh)
    def run(md):
        # conformal: phi'' - (a''/a) phi + 2 lam |phi|^2 phi = 0 (real radial mode), tau = H eta
        def a_of(t):
            if md: return (1+t/2)**2 if (1+t/2)**2 < vis.arh else None
            return 1+t
        def rhs(t, y):
            if md:
                aa = (1+t/2)**2; app = .5/aa          # a''/a = (1/2)/(1+t/2)^2
            else:
                app = 0.
            return [y[1], app*y[0]-2*lam*y[0]**3]
        T = 4000.
        sol = solve_ivp(rhs, (0, T), [phi0, phi0+(0 if md else 0)-(2/3)*lam*phi0**3], rtol=1e-10, atol=1e-12,
                        dense_output=True, max_step=1.)
        tt = np.linspace(T-500, T, 4000); ph = sol.sol(tt)
        return np.mean(ph[1]**2/2+lam*ph[0]**4/2)
    return run(True)/run(False)


def onset(Hinf, Trh, X0, EPhi_conf, phi0):
    vis = R.Vis(Hinf, Trh); fx = R.free_X(vis, X0*Hinf)
    rhoPhi = EPhi_conf*Hinf**4*md_ratio(Trh, Hinf, phi0)/fx['a_on']**4
    return vis, fx, rhoPhi


def closure(vis, fx, rhoPhi, which, crossed=0., relcut=None, rule='frozen'):
    a_on = fx['a_on']; t0 = time.time()
    if which == 'L':
        res = R.run_plasma(vis, a_on, fx['rho_on']+rhoPhi, crossed=crossed, relcut=relcut, rule=rule)
        W = res['W']*a_on**3
    elif which == 'K':
        def Tbath(rho):
            return np.exp(brentq(lambda lt: np.log(R.thermo(np.exp(lt), -R.meff_eq(np.exp(lt))/np.exp(lt), -800.)['rho']/rho),
                                 np.log(1e-9), np.log(1e6)))
        T0 = Tbath(rhoPhi); th0 = R.thermo(T0, -R.meff_eq(T0)/T0, -800.)
        GH = R.Drest(T0, crossed)*th0['nP']**2/2/vis.H(a_on)
        if GH > 10:
            # stiff limit (AMENDMENT A3 item 5): cold X absorbed at onset, energy M per X into the bath; the plasma then
            # follows the frozen E4 rule (mu = 0 while T_d > m/3 and C n^3/H > 100), as in closure L
            res = R.run_plasma(vis, a_on, rhoPhi+M*fx['Na3']/a_on**3, crossed=crossed, relcut=relcut, rule=rule)
        else:
            try:
                res = R.run_plasma(vis, a_on, NXc0=fx['Na3']/a_on**3, thP=dict(T=T0, zP=-R.meff_eq(T0)/T0), crossed=crossed,
                                   relcut=relcut, rule='pb', wall_limit=300.)
            except TimeoutError:      # slow-absorption branch not completed within the solver budget (reported)
                return dict(closure='K', Y=float('nan'), Omega=float('nan'), W_comoving=None, wall=time.time()-t0, hist=[],
                            T_end=None, extra=dict(W_absorption_Gamma_over_H_onset=GH, W_status='not completed (300 s budget)'))
        res['W_absorption_Gamma_over_H_onset'] = GH
        W = res['W']*a_on**3
    elif which == 'C':
        res = R.run_plasma(vis, a_on, rhoPhi, crossed=crossed, relcut=relcut, rule=rule)
        W = res['W']*a_on**3+2*fx['Na3']
        res['W_X_ceiling'] = 2*fx['Na3']; res['W_bath'] = res['W']*a_on**3
    Y = W/vis.S
    short = [h for h in res['hist']][::max(1, len(res['hist'])//25)]
    return dict(closure=which, Y=Y, Omega=Y*R.OMEGA_PER_Y, W_comoving=W, wall=time.time()-t0, hist=short,
                T_end=res['T_end'], extra={k: v for k, v in res.items() if k.startswith('W_')})


def point(Hinf, Trh, patch='p50', closures=('L', 'K', 'C'), crossed=0., relcut=None, Xscale=1., Phiscale=1., rule='frozen'):
    amps = patch_amps(); E = lattice_E()
    X0 = amps[patch]['X']*Xscale; phi0 = amps[patch]['Phi']
    EPhi = E[patch]*E_hom(phi0*Phiscale)/E_hom(phi0)
    vis, fx, rhoPhi = onset(Hinf, Trh, X0, EPhi, phi0*Phiscale)
    out = dict(Hinf=Hinf, Trh=Trh, patch=patch, X0_over_H=X0, Phi0_over_H=phi0*Phiscale, EPhi_conf=EPhi, a_on=fx['a_on'],
               rhoX_on=fx['rho_on'], rhoPhi_on=rhoPhi, rule=rule, NX_a3=fx['Na3'], S=vis.S, crossed=crossed, relcut=relcut,
               Y_free_condensate=2*fx['Na3']/vis.S, Omega_free_condensate=2*fx['Na3']/vis.S*R.OMEGA_PER_Y, res={})
    for c in closures:
        out['res'][c] = closure(vis, fx, rhoPhi, c, crossed, relcut, rule)
    return out


# ---- xi = 1/6 control: conformally coupled linear production (exact mode equation u'' + (k^2 + ms^2 a^2) u = 0) ----
def beta2_halfline(kap, xend=60.):
    """RD a ∝ (eta - eta_e + 1/H): u_xx + (kap^2 + x^2) u = 0 from x0 ~ sqrt(m/H) ~ 0 in the conformal vacuum."""
    w0 = kap; y0 = [1/np.sqrt(2*w0), 0., 0., -w0/np.sqrt(2*w0)]          # u = e^{-i kap x}/sqrt(2 kap): re, im parts
    def rhs(x, y): w2 = kap*kap+x*x; return [y[1], -w2*y[0], y[3], -w2*y[2]]
    sol = solve_ivp(rhs, (0, xend), [y0[0], y0[1], y0[2], y0[3]], rtol=1e-10, atol=1e-12, method='DOP853')
    ur, upr, ui, upi = sol.y[:, -1]; u = ur+1j*ui; up = upr+1j*upi; w = np.sqrt(kap*kap+xend*xend)
    # first-order adiabatic basis: u_+ ~ e^{-i int w}/sqrt(2w), u_+' = (-i w - w'/(2w)) u_+
    wp = xend/w; corr = wp/(2*w)
    return abs(w*u-1j*(up+corr*u))**2/(2*w)


def beta2_md(kap, yend):
    """w = 0 era, a ~ (H eta/2)^2: u_yy + (kap^2 + y^4) u = 0 from y ~ 0 in the conformal vacuum (scaled y = eta/t_*)."""
    y0 = [1/np.sqrt(2*kap), 0., 0., -kap/np.sqrt(2*kap)]
    def rhs(x, y): w2 = kap*kap+x**4; return [y[1], -w2*y[0], y[3], -w2*y[2]]
    sol = solve_ivp(rhs, (0, yend), y0, rtol=1e-10, atol=1e-12, method='DOP853')
    ur, upr, ui, upi = sol.y[:, -1]; u = ur+1j*ui; up = upr+1j*upi; w = np.sqrt(kap*kap+yend**4)
    corr = (2*yend**3/w)/(2*w)
    return abs(w*u-1j*(up+corr*u))**2/(2*w)


def control_xi16(Hinf, Trh):
    kap = np.concatenate([np.linspace(1e-3, 1, 60), np.linspace(1.02, 4, 60)])
    b2 = np.array([beta2_halfline(k) for k in kap])
    I_half = np.trapz(kap*kap*b2, kap); I_full = 1/(4*np.pi)
    vis = R.Vis(Hinf, Trh); md_info = {}
    def na3(ms):
        if Trh is None:
            A = Hinf
        else:
            Hrh = vis.H(vis.arh*1.000001)
            if Hrh < 10*ms:
                # production during the w = 0 era: t_* = (16 H^2/ms^2)^(1/6)/H in eta; complete if eta_rh/t_* >= 10
                tstar = (16/(ms/Hinf)**2)**(1/6); trh = 2*(np.sqrt(vis.arh)-1); yend = min(15., trh/tstar)
                kk = np.concatenate([np.linspace(1e-3, 1, 50), np.linspace(1.03, 4, 40)])
                b2m = np.array([beta2_md(k, yend) for k in kk])
                md_info[ms] = dict(t_star=tstar, y_end=yend, complete=bool(trh/tstar >= 10))
                return (Hinf/tstar)**3/np.pi**2*np.trapz(kk*kk*b2m, kk)
            A = Hrh*vis.arh**2
        return (ms*A)**1.5/np.pi**2*I_half
    nP = na3(m); nX = na3(M); W = nP+2*nX
    Y = W/vis.S
    return dict(Hinf=Hinf, Trh=Trh, I_half=I_half, I_full_line=I_full, ratio_half_to_full=I_half/I_full, md_info=md_info,
                Y=Y, Omega=Y*R.OMEGA_PER_Y, kap=kap.tolist(), beta2=b2.tolist(),
                analytic_full_line_Y=((m*Hinf)**1.5+2*(M*Hinf)**1.5)/(4*np.pi**3)/vis.S if Trh is None else None)


def isocurvature(Hinf, Trh, closures=('L', 'K', 'C'), patch='p50'):
    base = point(Hinf, Trh, patch, closures)
    dX = point(Hinf, Trh, patch, closures, Xscale=1.01); dP = point(Hinf, Trh, patch, closures, Phiscale=1.01)
    out = {}
    for c in closures:
        y0 = base['res'][c]['Y']; sx = np.log(dX['res'][c]['Y']/y0)/np.log(1.01); sp = np.log(dP['res'][c]['Y']/y0)/np.log(1.01)
        PS = sx**2/(8*np.pi**2*base['X0_over_H']**2)+sp**2/(8*np.pi**2*base['Phi0_over_H']**2)
        out[c] = dict(dlnY_dlnX=sx, dlnY_dlnPhi=sp, P_S=PS, bound=8.3e-11, ratio_to_bound=PS/8.3e-11, pass_=PS < 8.3e-11)
    return dict(base=base, iso=out)


if __name__ == '__main__':
    cmd = sys.argv[1]; Hinf = float(sys.argv[2]); Trh = None if sys.argv[3] == 'inst' else float(sys.argv[3])
    tag = sys.argv[sys.argv.index('--tag')+1] if '--tag' in sys.argv else f'{cmd}_H{Hinf:.4g}_T{sys.argv[3]}'
    patch = sys.argv[sys.argv.index('--patch')+1] if '--patch' in sys.argv else 'p50'
    cl = tuple(sys.argv[sys.argv.index('--closures')+1].split(',')) if '--closures' in sys.argv else ('L', 'K', 'C')
    if '--powerlaw' in sys.argv: R.D_MODE['hiT'] = 'powerlaw'
    crossed = 1. if '--crossed' in sys.argv else 0.
    relcut = m if '--relcut' in sys.argv else None
    rule = 'pb' if '--pb' in sys.argv else 'frozen'
    xscale = float(sys.argv[sys.argv.index('--xscale')+1]) if '--xscale' in sys.argv else 1.
    t0 = time.time()
    if cmd == 'point':
        res = point(Hinf, Trh, patch, cl, crossed, relcut, Xscale=xscale, rule=rule)
    elif cmd == 'iso':
        res = isocurvature(Hinf, Trh, cl, patch)
    elif cmd == 'control':
        res = control_xi16(Hinf, Trh)
    res['wall'] = time.time()-t0; res['D_mode'] = R.D_MODE['hiT']
    (OUTD/f'{tag}.json').write_text(json.dumps(res, indent=1, default=float))
    if cmd == 'point':
        print(tag, {c: (f"{v['Y']:.3e}", f"{v['Omega']:.3e}") for c, v in res['res'].items()}, 'free', f"{res['Omega_free_condensate']:.3e}",
              'wall', round(res['wall'], 1))
    elif cmd == 'iso':
        print(tag, {c: (f"{v['P_S']:.3e}", v['pass_'], round(v['dlnY_dlnX'], 3), round(v['dlnY_dlnPhi'], 3)) for c, v in res['iso'].items()})
    else:
        print(tag, 'Y', res['Y'], 'Omega', res['Omega'], 'half/full', res['ratio_half_to_full'])
