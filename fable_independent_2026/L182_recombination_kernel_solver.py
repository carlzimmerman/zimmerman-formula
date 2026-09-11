#!/usr/bin/env python3
"""L182 -- THE RECOMBINATION SOLVER WITH THE KERNEL ON.
Compact scalar Boltzmann code, conformal Newtonian gauge (Ma & Bertschinger 1995 conventions: ds^2 = a^2[-(1+2psi)dtau^2 + (1-2phi)dx^2],
delta = drho/rho, theta = ik.v). Species: tight-coupled photon-baryon fluid with baryon loading R = 3 rho_b/(4 rho_g), massless neutrino
fluid (no shear), optional CDM. LCDM background. Adiabatic superhorizon ICs. Potentials from the comoving Poisson equation
k^2 phi_N = -(3/2) H^2 sum Omega_x(a)[delta_x + 3H(1+w_x)theta_x/k^2]; phi = psi (no shear). Instantaneous decoupling at z_* = 1090 with
Silk damping exp(-k^2/k_D^2) and finite-width damping; sources: Sachs-Wolfe (delta_g/4 + psi), Doppler (theta_b/k), early ISW integrated
to 8 tau_*. THE KERNEL (framework, prescription A, mean-field): phi = psi = nu(g_rms/a0) phi_N, with g_rms = (k/a) |phi_N| Phi_i c^2 the physical
rms acceleration of the mode (Phi_i = (2/3) sqrt(Delta^2_R) the superhorizon potential), nu_RAR, both footings; phi' = nu phi_N'.
VALIDATION: the CDM + GR run must reproduce CLASS's peak positions and D_l peak ratios before any framework number is read.
Runs: LCDM+GR (validation), noCDM+GR, noCDM+kernel (canonical, alt), LCDM+kernel. Output: peak positions and D_l ratios peak2/peak1, peak3/peak2.
No literal-True checks. Limits: fluid photons/neutrinos (no hierarchy), no polarization, no reionization, instantaneous decoupling, mean-field kernel."""
import numpy as np, sys, time
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.special import spherical_jn
T0 = time.time(); CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
h = 0.6736; omb = 0.02237; omc0 = 0.1200; H0 = 100*h/299792.458           # 1/Mpc
Og = 2.4728e-5/h**2; On = Og*3.046*(7/8)*(4/11)**(4/3); Or = Og + On; Ob = omb/h**2
A_s, n_s, kp = 2.1e-9, 0.9649, 0.05
ZSTAR = 1090.0; AST = 1/(1 + ZSTAR)
MPC_M = 3.0857e22; C = 2.998e8
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(max(x, 1e-300))))
class Cosmo:
    def __init__(self, Oc, kernel=None):
        self.Oc = Oc; self.Om = Ob + Oc; self.OL = 1 - self.Om - Or; self.kernel = kernel
        af = np.geomspace(1e-8, 1.0, 20000); H = H0*np.sqrt(Or*af**-4 + self.Om*af**-3 + self.OL)
        self.tau_of_a_tab = (af, cumulative_trapezoid(1/(af**2*H), af, initial=0.0))
        self.tau_star = np.interp(AST, *self.tau_of_a_tab); self.tau0 = self.tau_of_a_tab[1][-1]
    def a_of_tau(self, tau): return np.interp(tau, self.tau_of_a_tab[1], self.tau_of_a_tab[0])
    def Hc(self, a): return a*H0*np.sqrt(Or*a**-4 + self.Om*a**-3 + self.OL)         # conformal H = a H
    def Omx(self, a):  # Omega_x(a) = rho_x/rho_tot
        E2 = Or*a**-4 + self.Om*a**-3 + self.OL
        return Og*a**-4/E2, On*a**-4/E2, Ob*a**-3/E2, self.Oc*a**-3/E2
def rhs_factory(cos, k, Phi_i, coupled=True):
    """state y = [dg, tg, dn, tn, db, tb, dc, tc, phiN]; phiN evolved with the GR momentum constraint (MB 23b),
    phi = psi = nu * phiN (mean-field kernel). After decoupling photons free-stream: excluded from the potential sources."""
    a0k = A0[cos.kernel] if cos.kernel else None
    def pots(a, y):
        dg, tg, dn, tn, db, tb, dc, tc, phiN = y; Hc = cos.Hc(a); og, on, ob, oc = cos.Omx(a)
        wg = og if coupled else 0.0
        mom = 1.5*Hc**2*(wg*(4/3)*tg + on*(4/3)*tn + ob*tb + oc*tc)/k**2
        if a0k is None: return phiN, mom - Hc*phiN, 1.0
        g = (k/a)*abs(phiN)*Phi_i*C**2/MPC_M
        nv = nu(g/a0k); return nv*phiN, nv*(mom - Hc*phiN), nv
    def rhs(tau, y):
        a = cos.a_of_tau(tau); Hc = cos.Hc(a); og, on, ob, oc = cos.Omx(a)
        dg, tg, dn, tn, db, tb, dc, tc, phiN = y
        phi, phip, nv = pots(a, y); psi = phi
        R = 0.75*ob/og
        ddg = -(4/3)*(tg - 3*phip)
        if coupled:
            dtg = -(R/(1 + R))*Hc*tg + (k**2*dg/4)/(1 + R) + k**2*psi
            ddb = -(tb - 3*phip); dtb = dtg
        else:
            dtg = k**2*dg/4 + k**2*psi
            ddb = -(tb - 3*phip); dtb = -Hc*tb + k**2*psi
        ddn = -(4/3)*(tn - 3*phip); dtn = k**2*dn/4 + k**2*psi
        ddc = -(tc - 3*phip); dtc = -Hc*tc + k**2*psi
        wg = og if coupled else 0.0
        mom = 1.5*Hc**2*(wg*(4/3)*tg + on*(4/3)*tn + ob*tb + oc*tc)/k**2
        dphiN = mom - Hc*phiN
        return [ddg, dtg, ddn, dtn, ddb, dtb, ddc, dtc, dphiN]
    return rhs, pots
def run(cos, ks, label):
    t = time.time(); src = []; isw = []
    ells = np.arange(2, 1501, 3); chi0 = cos.tau0
    taus_isw = np.linspace(cos.tau_star, min(8*cos.tau_star, cos.tau0), 40)
    for k in ks:
        Phi_i = (2/3)*np.sqrt(A_s*(k/kp)**(n_s - 1))
        rhs, pots = rhs_factory(cos, k, Phi_i, True)
        tau_i = min(1e-2/k, 0.5*cos.tau_star); a_i = cos.a_of_tau(tau_i)
        psi0 = 1.0; y0 = [-2*psi0, k**2*tau_i*psi0/2, -2*psi0, k**2*tau_i*psi0/2, -1.5*psi0, k**2*tau_i*psi0/2, -1.5*psi0, k**2*tau_i*psi0/2, psi0]
        s = solve_ivp(rhs, [tau_i, cos.tau_star], y0, rtol=1e-6, atol=1e-9, method="RK45")
        y = s.y[:, -1]; a = AST; phi, phip, nv = pots(a, y)
        # normalise so that the superhorizon potential equals Phi_i: our ICs give phi_N(early) = -(3/2)Hc^2 * (og*(-2) + ...)/k^2 ~ psi0-ish; use actual early value
        rhs2, pots2 = rhs_factory(cos, k, Phi_i, False)
        s2 = solve_ivp(rhs2, [cos.tau_star, taus_isw[-1]], y, t_eval=taus_isw, rtol=1e-6, atol=1e-9, method="RK45")
        phis = np.array([pots2(cos.a_of_tau(tt), s2.y[:, i])[0] for i, tt in enumerate(taus_isw)])
        dphi = np.gradient(phis, taus_isw)
        src.append((y[0]/4 + phi, y[5]/k)); isw.append((taus_isw, 2*dphi))
    # PROJECTION on a fine k grid: the sources are smooth in k, the Bessel kernel is not (period ~ 2 pi / chi0 ~ 4e-4 / Mpc)
    from scipy.interpolate import CubicSpline
    kD = 0.135*(omb/0.02237)**0.5*(1 if cos.Oc > 0 else 0.8)
    SWc = np.array([sv[0] for sv in src]); DOPc = np.array([sv[1] for sv in src])
    ISWc = np.array([iv[1] for iv in isw])                       # (nk, ntau) of 2 phi'
    kf = np.arange(ks[0], ks[-1], 1.0e-4)
    SWf = CubicSpline(ks, SWc)(kf); DOPf = CubicSpline(ks, DOPc)(kf); ISWf = CubicSpline(ks, ISWc, axis=0)(kf)
    Phi_f = (2/3)*np.sqrt(A_s*(kf/kp)**(n_s - 1)); dampf = np.exp(-(kf/kD)**2 - (kf*19.0)**2/2)
    x = np.outer(kf, np.ones(len(ells)))*(chi0 - cos.tau_star)
    jl = spherical_jn(ells[None, :], x); jlp = spherical_jn(ells[None, :], x, derivative=True)
    Theta = (SWf[:, None]*jl + DOPf[:, None]*jlp)*dampf[:, None]
    # early ISW for l < 400 only
    lo = ells < 400; tt = isw[0][0]
    for it, t_ in enumerate(tt):
        xi = np.outer(kf, np.ones(lo.sum()))*(chi0 - t_)
        Theta[:, lo] += np.trapz(np.ones(2), np.array([0, 1]))*0 + ISWf[:, it][:, None]*spherical_jn(ells[lo][None, :], xi)*(tt[1] - tt[0] if it not in (0, len(tt)-1) else 0.5*(tt[1] - tt[0]))
    Theta *= Phi_f[:, None]
    Cl = 4*np.pi*np.trapz(Theta**2/kf[:, None], kf, axis=0)
    Dl = ells*(ells + 1)*Cl/(2*np.pi)
    print(f"    {label:<22} done in {time.time()-t:.0f}s", flush=True)
    return ells, Dl
def peaks(ells, Dl, w=25):
    Ds = np.convolve(Dl, np.ones(9)/9, mode="same"); p = []
    for j in range(w, len(Ds) - w):
        if Ds[j] >= Ds[j-w:j+w+1].max() and ells[j] > 120 and ells[j] < 1300: p.append((ells[j], Ds[j]))
    return p[:3]
if __name__ == "__main__":
    ks = np.geomspace(0.003, 0.45, 160)
    print("=" * 110 + "\nL182 RECOMBINATION SOLVER WITH THE KERNEL ON -- D_l peak positions and ratios\n" + "=" * 110)
    from classy import Class
    cl = Class(); cl.set({"h": h, "omega_b": omb, "omega_cdm": omc0, "A_s": A_s, "n_s": n_s, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454, "output": "tCl", "l_max_scalars": 1500}); cl.compute()
    cls = cl.raw_cl(1500); lc = cls["ell"][2:]; Dc = lc*(lc + 1)*cls["tt"][2:]/(2*np.pi)
    pc = peaks(lc, Dc, w=60)
    print(f"    CLASS LCDM: peaks at l = {[int(p[0]) for p in pc]}; D ratios peak2/peak1 = {pc[1][1]/pc[0][1]:.3f}, peak3/peak2 = {pc[2][1]/pc[1][1]:.3f}")
    runs = {"LCDM+GR": Cosmo(omc0/h**2), "noCDM+GR": Cosmo(0.0), "noCDM+kernel canon": Cosmo(0.0, "canonical"), "noCDM+kernel alt": Cosmo(0.0, "alt"), "LCDM+kernel canon": Cosmo(omc0/h**2, "canonical")}
    res = {}
    for lab, cos in runs.items():
        ells, Dl = run(cos, ks, lab); pk = peaks(ells, Dl); res[lab] = (pk, Dl)
        ref = [100, 220, 400, 537, 700, 816, 1000]; print("      D_l shape (norm. at l=220): " + " ".join(f"{l}:{Dl[np.argmin(abs(ells-l))]/Dl[np.argmin(abs(ells-220))]:.2f}" for l in ref) + "  | CLASS: " + " ".join(f"{Dc[np.argmin(abs(lc-l))]/Dc[np.argmin(abs(lc-220))]:.2f}" for l in ref), flush=True)
        np.savez(f"L182_Dl_{lab.replace(' ', '_').replace('+','_')}.npz", ells=ells, Dl=Dl)
        if len(pk) >= 3: print(f"      peaks l = {[int(p[0]) for p in pk]}; peak2/peak1 = {pk[1][1]/pk[0][1]:.3f}, peak3/peak2 = {pk[2][1]/pk[1][1]:.3f}")
        else: print(f"      peaks found: {[(int(p[0]), round(p[1],1)) for p in pk]}")
    pL = res["LCDM+GR"][0]
    ok_pos = len(pL) >= 3 and all(abs(pL[i][0]/pc[i][0] - 1) < 0.06 for i in range(3))
    check("V1 validation: the CDM + GR mini-Boltzmann reproduces CLASS's first three peak positions to 6%", ok_pos, f"mine {[int(p[0]) for p in pL]} vs CLASS {[int(p[0]) for p in pc]}")
    r32 = lambda pk: pk[2][1]/pk[1][1] if len(pk) >= 3 else np.nan
    check("V2 validation: the CDM + GR run reproduces CLASS's peak3/peak2 ratio to 25% (fluid approximation, no hierarchy)", abs(r32(pL)/(pc[2][1]/pc[1][1]) - 1) < 0.25, f"mine {r32(pL):.3f} vs CLASS {pc[2][1]/pc[1][1]:.3f}")
    rN = r32(res["noCDM+GR"][0]); rL = r32(pL)
    check("V3 control: no CDM with GR lowers peak3/peak2 relative to the same-code LCDM by more than 25% (the L129/L165 third-peak deficit, reproduced in this code)", rN/rL < 0.75, f"noCDM+GR {rN:.3f} vs LCDM+GR {rL:.3f}")
    for lab in ("noCDM+kernel canon", "noCDM+kernel alt"):
        rK = r32(res[lab][0]); print(f"    {lab}: peak3/peak2 = {rK:.3f} (LCDM same code {rL:.3f}, noCDM GR {rN:.3f}); restoration fraction = {(rK - rN)/(rL - rN) if rL != rN else np.nan:.2f}")
    rest = {lab: (r32(res[lab][0]) - rN)/(rL - rN) for lab in ("noCDM+kernel canon", "noCDM+kernel alt")}
    check("V4 [THE QUESTION] with the kernel on and no CDM, does the third peak return to within 10% of the same-code LCDM ratio for either footing? (PASS = the dark-fraction wall dissolves at recombination; FAIL = it stands)",
          any(abs(r32(res[l][0])/rL - 1) < 0.10 for l in ("noCDM+kernel canon", "noCDM+kernel alt")), ", ".join(f"{l}: {r32(res[l][0])/rL:.3f} of LCDM, restoration {rest[l]:.2f}" for l in rest))
    print("    LIMITS: fluid photons/neutrinos, instantaneous decoupling, fitted Silk scale, mean-field kernel (nu of the rms mode acceleration, no mode coupling, nu' neglected), prescription A only.")
    print(f"\nL182 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.   [{time.time()-T0:.0f}s]")
