#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03d -- the EXACT static law of the candidate with the coherence term outside J, solved for the Sun in the Galactic field.
The metric carries Newton untouched (Delta Phi_N = 4 pi G rho) and the MOND scalar psi obeys
        div[ mu(|grad(Phi_0 + psi)|/a0) grad psi ] - xi^2 Delta^2 psi = -div[ (mu - 1) grad Phi_0 ],   Phi_0 = -GM/r - eta a0 r cos(theta),
so that xi -> 0 is exactly AQUAL for the total potential and the scalar carries only the MOND part (no point source, no screening of Newton).
Axisymmetric, finite differences in s = ln r x Legendre modes (G01's discretisation extended to fourth order), Picard mu-lag.  Units GM = a0 = 1,
eps = xi/r_M.  Boundary data: psi_0' = 0 inside (Neumann: excludes the 1/r solution, a Dirichlet value at finite r_min would force a spurious point mass psi(0) r_min), psi_l = 0 inside for l >= 1, psi_l = 0 outside, Delta psi_l = 0 at the next-to-boundary nodes (regular inside:
(r psi_0)'' = 0 selects {1, sinh(r/xi)/r}; harmonic far field).  Observables from the scalar: Q2 = -3 c2 a0^{3/2}/sqrt(GM) (Park's sign, the r^2 P2
coefficient of psi_2), the monopole M_ph(<r)/M = r^2 psi_0'(r) at Saturn, the radial anomaly -psi_0'(r) at Mercury-Neptune.  Gates as G01/G02:
Park 2026 Q2 ceiling 5.2e-27 s^-2, Pitjev-Pitjeva 6.7e-11 Msun inside Saturn, 3.66e-14 m/s^2 sunward.  Both footings, three field inputs.  Checks can fail."""
import math, sys, time, numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spl, warnings; warnings.filterwarnings("ignore")
from numpy.polynomial.legendre import leggauss, legval, legder
from scipy.optimize import brentq
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
PC, AU, G, MSUN, GM = 3.0857e16, 1.495978707e11, 6.6743e-11, 1.98892e30, 1.32712440018e20
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Q2_CEIL, M_SAT_BOUND, A_SUNWARD, R_SAT = 5.2e-27, 6.7e-11, 0.5*9.36e-11/1278.0, 9.58*AU
PLANETS = {"Mercury": 0.387*AU, "Earth": AU, "Mars": 1.524*AU, "Jupiter": 5.203*AU, "Saturn": R_SAT, "Neptune": 30.07*AU}
def mu_exp(x): return 1.0 - np.exp(-x)
def solve4(mufun, eta, eps, L=8, NS=700, NT=48, rmin=1e-4, rmax=1e4, tol=1e-9, itmax=300, relax=0.5, outer_lap0=0.0):
    """outer_lap0: value of e^{2s} Delta psi_0 at the outer node (0 for the external-field far field, which is harmonic; 1 for the isolated deep-MOND
    log potential, Delta psi_0 = 1/r^2)."""
    s = np.linspace(math.log(rmin), math.log(rmax), NS); ds = s[1] - s[0]; rr = np.exp(s); es = np.exp(s)
    x, w = leggauss(NT); P = np.array([legval(x, [0]*l + [1]) for l in range(L + 1)])
    dP = np.array([legval(x, legder([0]*l + [1])) if l > 0 else np.zeros(NT) for l in range(L + 1)]); dPth = -dP*np.sqrt(1 - x**2)[None, :]
    norm = 2.0/(2*np.arange(L + 1) + 1)
    phi0 = np.zeros((L + 1, NS)); phi0[0] = -1.0/rr; phi0[1] = -eta*rr                     # Newton + external field, exact
    psi = np.zeros((L + 1, NS)); n = (L + 1)*NS; esh = np.exp(0.5*(s[1:] + s[:-1]))
    def Dmat(m):
        main = -2.0/ds**2 - m*(m + 1); up = 1.0/ds**2 + 0.5/ds; lo = 1.0/ds**2 - 0.5/ds
        return sps.diags([lo*np.ones(NS - 1), main*np.ones(NS), up*np.ones(NS - 1)], [-1, 0, 1], format="csr")
    Q4 = {m: (-eps**2*norm[m])*sps.diags(es) @ Dmat(m) @ sps.diags(np.exp(-2*s)) @ Dmat(m) for m in range(L + 1)}
    def fields(phi):
        dPhi_ds = np.gradient(phi, ds, axis=1); gr = -(P.T @ dPhi_ds)/rr[None, :]; gt = -(dPth.T @ phi)/rr[None, :]
        return np.hypot(gr, gt)
    def mu_part(m_):
        """the discrete e^{3s} div[m_ grad .] operator (interior rows exact; boundary rows arbitrary, overwritten later)"""
        B = np.einsum("j,mj,lj,js->mls", w, P, P, m_); A = -np.einsum("j,mj,lj,js->mls", w, dPth, dPth, m_); Bh = 0.5*(B[:, :, 1:] + B[:, :, :-1])
        blocks = [[None]*(L + 1) for _ in range(L + 1)]
        for mm in range(L + 1):
            for ll in range(L + 1):
                cp = np.zeros(NS); cm = np.zeros(NS); cp[:-1] = esh*Bh[mm, ll]/ds**2; cm[1:] = esh*Bh[mm, ll]/ds**2
                blocks[mm][ll] = sps.diags([cm[1:], -(cp + cm) + es*A[mm, ll], cp[:-1]], [-1, 0, 1], format="csr")
        return sps.bmat(blocks, format="csr")
    bnd = np.array([i for mm in range(L + 1) for i in (mm*NS, mm*NS + 1, mm*NS + NS - 2, mm*NS + NS - 1)])
    keep = np.ones(n); keep[bnd] = 0.0; K = sps.diags(keep)
    # boundary rows: Dirichlet at 0, NS-1; D_m psi = 0 at 1, NS-2
    rows, cols, vals = [], [], []
    for mm in range(L + 1):
        D = Dmat(mm); base = mm*NS
        if mm == 0:   # l = 0 inner: Neumann d psi/ds = 0 (kills the 1/r solution; the constant is fixed by the outer Dirichlet); second-order one-sided
            rows += [base, base, base]; cols += [base, base + 1, base + 2]; vals += [-3.0, 4.0, -1.0]
        else:
            rows.append(base); cols.append(base); vals.append(1.0)
        rows.append(base + NS - 1); cols.append(base + NS - 1); vals.append(1.0)
        for i in (1, NS - 2):
            for j in (i - 1, i, i + 1): rows.append(base + i); cols.append(base + j); vals.append(D[i, j])
    BC = sps.csr_matrix((vals, (rows, cols)), shape=(n, n)); Q4full = sps.block_diag([Q4[m] for m in range(L + 1)], format="csr")
    for it in range(itmax):
        m_ = mufun(np.maximum(fields(phi0 + psi), 1e-300))
        Mx = K @ (mu_part(m_) + Q4full) + BC
        rhs = -(K @ (mu_part(m_ - 1.0) @ phi0.reshape(-1)))
        rhs[NS - 2] = outer_lap0
        new = spl.spsolve(Mx, rhs).reshape(L + 1, NS)
        dphi = np.max(np.abs(new - psi))/max(1e-30, np.max(np.abs(new)))
        psi = (1 - relax)*psi + relax*new
        if dphi < tol: break
    return psi, rr, it + 1, dphi
def fit_l2(phi2, rr, win):
    sel = (rr > win[0]) & (rr < win[1]); Am = np.vstack([rr[sel]**2, rr[sel]**4, np.ones(sel.sum()), rr[sel]**-3]).T
    return np.linalg.lstsq(Am, phi2[sel], rcond=None)[0]
def fit_l0(psi0, rr, win):
    sel = (rr > win[0]) & (rr < win[1]); Am = np.vstack([np.ones(sel.sum()), rr[sel]**2, rr[sel]**4, rr[sel]**6]).T
    return np.linalg.lstsq(Am, psi0[sel], rcond=None)[0]
def observables(psi, rr, a0):
    rM = math.sqrt(GM/a0)
    c2s = [fit_l2(psi[2], rr, wn)[0] for wn in ((2e-3, 2e-2), (3e-3, 3e-2), (5e-3, 5e-2))]
    Q2 = [-3*c*a0**1.5/math.sqrt(GM) for c in c2s]
    a_, b_, d_, f_ = fit_l0(psi[0], rr, (2e-3, 3e-2))                                     # regular interior: a + b r^2 + d r^4 + f r^6
    rs = R_SAT/rM; Mph = 2*b_*rs**3 + 4*d_*rs**5 + 6*f_*rs**7                              # r^2 psi_0'
    ganom = {p: (2*b_*(rp/rM) + 4*d_*(rp/rM)**3 + 6*f_*(rp/rM)**5)*a0 for p, rp in PLANETS.items()}
    return dict(Q2=Q2, Mph=Mph, ganom=ganom, c2=c2s, b=b_)
print("=" * 110); print("g03d -- exact fourth-order static law of the candidate, Sun in the Galactic field"); print("=" * 110)
# ---- V1: eps -> 0 reproduces G01's strict AQUAL quadrupole
a0c = A0["canonical"]; eta_c = 2.32e-10/a0c
phi, rr, it, res = solve4(mu_exp, eta_c, 1e-3); ob = observables(phi, rr, a0c)
print(f"  V1 eps = 1e-3, canonical, g_obs 2.32e-10: Q2 = {', '.join(f'{q:+.3e}' for q in ob['Q2'])}  ({it} it, resid {res:.1e}, {time.time()-T0:.0f} s)   [G01: +2.097e-26]")
check("V1 eps -> 0 reproduces G01's strict-AQUAL quadrupole +2.10e-26 s^-2 (canonical, 2.32e-10) to 3% on all three windows", all(abs(q/2.097e-26 - 1) < 0.03 for q in ob["Q2"]) and res < 1e-8)
# ---- V2: Newtonian mu = 1: no quadrupole, no phantom
phiN, rrN, itN, resN = solve4(lambda x: np.ones_like(x), eta_c, 1.0); obN = observables(phiN, rrN, a0c)
check("V2 mu = 1 (Newton) with eps = 1: the scalar vanishes identically (no source), Q2 and the monopole are zero to 1e-12",
      max(abs(q) for q in obN["Q2"]) < 1e-12*2e-26 and abs(obN["Mph"]) < 1e-12 and float(np.max(np.abs(phiN))) < 1e-12, f"Q2 {max(abs(q) for q in obN['Q2']):.1e}, M_ph/M {obN['Mph']:.1e}, max|psi| {float(np.max(np.abs(phiN))):.1e}")
# ---- V3: eta = 0 reproduces g03c's spherical fourth-order solution (phantom kept at r_M)
for eps_, kept_ref in ((0.3, 0.8097), (1.0, 0.3679)):
    psi0, rr0, it0, res0 = solve4(mu_exp, 0.0, eps_, L=2, outer_lap0=1.0)
    g0 = -np.gradient(psi0[0] - 1.0/rr0, np.log(rr0))/rr0; g1 = float(np.interp(0.0, np.log(rr0), np.abs(g0)))       # interpolate to r = r_M exactly (a grid node is 2.6% away)
    galg = brentq(lambda g: mu_exp(g)*g - 1.0, 1e-14, 1e14); kept = (g1 - 1.0)/(galg - 1.0)
    check(f"V3 eta = 0, eps = {eps_}: the l = 0 field at r_M reproduces g03c's independent spherical solve (phantom kept {kept_ref}) to 2%", abs(kept/kept_ref - 1) < 0.02, f"kept {kept:.4f}, {it0} iterations, step {res0:.0e}")
# ---- the scan
print(f"\n  scan: footing | g_obs | xi [pc] | eps | Q2 (3 windows) | Q2/ceil | M_ph(<Sat)/bound | max planetary |g_anom|/sunward | it | admissible")
XIS_PC = [0.01, 0.02, 0.03, 0.05, 0.1, 0.3]; RES = {}
for foot, a0 in A0.items():
    rM = math.sqrt(GM/a0)
    for gobs in (2.00e-10, 2.32e-10, 2.64e-10):
        eta = gobs/a0
        for xi_pc in XIS_PC:
            eps = xi_pc*PC/rM
            phi, rr, it, res = solve4(mu_exp, eta, eps); ob = observables(phi, rr, a0)
            Qm = float(np.mean(ob["Q2"])); gmax = max(abs(v) for v in ob["ganom"].values())
            adm = abs(Qm) < Q2_CEIL and abs(ob["Mph"]) < M_SAT_BOUND and gmax < A_SUNWARD
            RES[(foot, gobs, xi_pc)] = dict(Q2=Qm, Mph=ob["Mph"], gmax=gmax, adm=adm, spread=float(np.std(ob["Q2"])/abs(Qm)) if Qm != 0 else 0.0)
            print(f"    {foot:9s} {gobs:.2e} {xi_pc:5.2f} {eps:5.2f} | {' '.join(f'{q:+.2e}' for q in ob['Q2'])} | {abs(Qm)/Q2_CEIL:7.3f} | {ob['Mph']/M_SAT_BOUND:+9.2e} | {gmax/A_SUNWARD:9.2e} | {it:3d} | {'yes' if adm else 'NO'}   ({time.time()-T0:.0f} s)", flush=True)
    fl = [xi for xi in XIS_PC if all(RES[(foot, g_, xi)]["adm"] for g_ in (2.00e-10, 2.32e-10, 2.64e-10))]
    floor = min(fl) if fl else None
    print(f"  {foot}: smallest tabulated xi admissible at all three field inputs = {floor} pc")
    check(f"F1 [{foot}] the exact fourth-order law has a nonempty admissible window at xi <= 0.1 pc", floor is not None and floor <= 0.1, f"floor {floor} pc")
    check(f"F2 [{foot}] admissibility is monotone above the floor up to 0.3 pc", floor is not None and all(all(RES[(foot, g_, xi)]["adm"] for g_ in (2.00e-10, 2.32e-10, 2.64e-10)) for xi in XIS_PC if xi >= floor))
    check(f"F3 [{foot}] the quadrupole fit is window-stable (spread < 5%) at every admissible xi", all(RES[(foot, g_, xi)]["spread"] < 0.05 for g_ in (2.00e-10, 2.32e-10, 2.64e-10) for xi in XIS_PC if floor and xi >= floor))
# ---- convergence at one point
phiA, rrA, _, _ = solve4(mu_exp, eta_c, 0.03*PC/math.sqrt(GM/a0c)); phiB, rrB, _, _ = solve4(mu_exp, eta_c, 0.03*PC/math.sqrt(GM/a0c), L=12, NS=1000, NT=64)
QA = np.mean(observables(phiA, rrA, a0c)["Q2"]); QB = np.mean(observables(phiB, rrB, a0c)["Q2"])
check("C1 refining L 8 -> 12, NS 700 -> 1000 changes the canonical Q2 at xi = 0.03 pc by < 3%", abs(QB/QA - 1) < 0.03, f"{QA:+.3e} -> {QB:+.3e}")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL", f"  ({time.time()-T0:.0f} s)"); sys.exit(1 if FAILS else 0)
