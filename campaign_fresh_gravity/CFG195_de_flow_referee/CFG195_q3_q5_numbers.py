#!/usr/bin/env python3
"""CFG195_q3_q5_numbers.py -- IV-4 (C and |beta| ranges by footing), IV-5 numerics (Q5), IV-6 (Q3-I accumulation), I-6a (thawing best nodes).
Reads only the three committed DESI chains (for the Gaussian-proxy distances and the thawing conditioning)."""
import math, os, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from CFG195_common import Run, find_repo
run = Run("CFG195_q3_q5_numbers", ()); repo = find_repo(); assert repo
G, c, MPC, MSUN, GYR = 6.6743e-11, 299792458.0, 3.0856775814913673e22, 1.98847e30, 3.15576e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
H0 = 67.4e3 / MPC; OL = 0.6847; rho_crit = 3 * H0 ** 2 / (8 * math.pi * G); rhoL = OL * rho_crit
print(f"rho_L (H0=67.4, Omega_L=0.6847) = {rhoL:.4e} kg/m^3")
# ------------------------------------------------------------------ IV-4
print("\n== IV-4 C = rho_c/rho_L and |beta| >= 2 C Omega_L, by footing ==")
def rho_c(M, a0):  # a0/(4 sqrt2 pi G r_M),  r_M = sqrt(GM/a0)
    rM = math.sqrt(G * M / a0); return a0 / (4 * math.sqrt(2) * math.pi * G * rM), rM
def rho_ph_numeric(M, a0):
    GM = G * M; rM = math.sqrt(GM / a0)
    f = lambda r: r * r * (math.sqrt((GM / r ** 2) ** 2 + (GM / r ** 2) * a0) - GM / r ** 2)   # r^2 g_ph  (P2)
    h = rM * 1e-5; return (f(rM + h) - f(rM - h)) / (2 * h) / (4 * math.pi * G * rM ** 2)
chk = max(abs(rho_ph_numeric(1e10 * MSUN, a) / rho_c(1e10 * MSUN, a)[0] - 1) for a in A0.values())
run.check("IV-4a rho_c = a0/(4 sqrt2 pi G r_M) equals the P2 phantom density (1/4 pi G r^2) d(r^2 g_ph)/dr at r = r_M (numerical derivative)", f"max rel diff {chk:.1e}", chk < 1e-6)
tab = {}
for f, a0 in A0.items():
    for M in (1e9, 1e10, 1e11, 1e12):
        rc, rM = rho_c(M * MSUN, a0); C = rc / rhoL; tab[(f, M)] = (C, 2 * C * OL, C ** 4, rM / 3.0856775814913673e19)
        print(f"  {f:9s} M={M:.0e} Msun: r_M={rM/3.0856775814913673e19:6.2f} kpc  rho_c={rc:.3e}  C={C:.3e}  |beta|>={2*C*OL:.3e}  compression C^(1/0.25)={C**4:.2e}")
run.num("IV4", {f"{k[0]}_{k[1]:.0e}": v for k, v in tab.items()})
Cs = [v[0] for v in tab.values()]; Cc = [v[0] for k, v in tab.items() if k[0] == "canonical"]; Bc = [v[1] for k, v in tab.items() if k[0] == "canonical"]; Ba = [v[1] for v in tab.values()]
print(f"  C range all footings {min(Cs):.3e} - {max(Cs):.3e}; canonical only {min(Cc):.3e} - {max(Cc):.3e}")
print(f"  |beta| range canonical only {min(Bc):.3e} - {max(Bc):.3e}; both footings {min(Ba):.3e} - {max(Ba):.3e}")
run.check("IV-4b C range 1.1e4-4.8e5 spans BOTH footings (canonical 1e12 lowest, alt 1e9 highest) within 5%", f"{min(Cs):.3e}-{max(Cs):.3e}", abs(min(Cs) / 1.1e4 - 1) < 0.05 and abs(max(Cs) / 4.8e5 - 1) < 0.05)
run.check("IV-4c |beta| range: README 1.6e4-4.9e5 equals the CANONICAL-only range (upper end 3.6e5 x 2 x 0.6847); the both-footings upper end is 6.5e5 (LABEL mismatch with C's range)", f"canonical {min(Bc):.3e}-{max(Bc):.3e}; both {min(Ba):.3e}-{max(Ba):.3e}", abs(min(Ba) / 1.6e4 - 1) < 0.05 and abs(max(Bc) / 4.9e5 - 1) < 0.05 and abs(max(Ba) / 6.5e5 - 1) < 0.03)
run.check("IV-4d volume compression C^(1/0.25) = 10^16-10^23 (1.7e16 ... 5e22)", f"{min(v[2] for v in tab.values()):.2e}-{max(v[2] for v in tab.values()):.2e}", 1e16 < min(v[2] for v in tab.values()) < 3e16 and 3e22 < max(v[2] for v in tab.values()) < 1e23)
# ------------------------------------------------------------------ IV-5 numerics
print("\n== IV-5 Q5 numbers ==")
HL = H0 * math.sqrt(OL); dens, pull = [], []
for M in (1e9, 1e10, 1e11, 1e12):
    a0 = A0["canonical"]; rM = math.sqrt(G * M * MSUN / a0); GM = G * M * MSUN
    rc_ = 3 * HL * math.sqrt(2 * GM) / (8 * math.pi * G * rM ** 1.5); dens.append(rc_ / rhoL)
    pull.append(0.5 * HL * math.sqrt(2 * GM / rM) / a0)
print(f"  negative-energy cross-term density at r_M / rho_L (H_L = H0 sqrt(Omega_L)): {[round(d,1) for d in dens]}; pull/a0: {[round(p,4) for p in pull]}")
run.check("IV-5c linear-superposition negative density 219-1230 rho_L and pull 0.001-0.005 a0 (1e9-1e12 Msun, canonical)", f"{min(dens):.0f}-{max(dens):.0f}; {min(pull):.4f}-{max(pull):.4f}", abs(min(dens) / 219 - 1) < 0.03 and abs(max(dens) / 1230 - 1) < 0.03 and 0.0007 < min(pull) < 0.0015 and 0.004 < max(pull) < 0.006)
Om3, OL3 = 0.3111, 0.6889; RR = {"canonical": 0.2928, "alt": 0.3539}
Ore = 2.4728e-5 / 0.6766 ** 2 * (1 + 0.2271 * 3.044)     # standard values (T_CMB=2.7255 K, N_eff=3.044) -- REPORTED ONLY
out = []
for f, R in RR.items():
    On = R * OL3; zdom = Om3 / On - 1; E_l = math.sqrt(Om3 * 3.5 ** 3 + OL3); E_n = math.sqrt(Om3 * 3.5 ** 3 + OL3 + On * 3.5 ** 4)
    out.append((On, zdom, E_n / E_l, On / Ore)); print(f"  null flow {f}: Omega_null={On:.3f}; dominates matter before z={zdom:.3f}; H(2.5) x{E_n/E_l:.3f}; x{On/Ore:.0f} of CMB+nu density (standard T_CMB, N_eff; reported only)")
run.check("IV-5d null flow: Omega_null 0.20/0.24, z_dom 0.54/0.28, H(2.5) x1.77/x1.89", str([(round(o[0], 3), round(o[1], 3), round(o[2], 3)) for o in out]),
          abs(out[0][0] - 0.20) < 0.005 and abs(out[1][0] - 0.24) < 0.005 and abs(out[0][1] - 0.54) < 0.01 and abs(out[1][1] - 0.28) < 0.01 and abs(out[0][2] - 1.77) < 0.02 and abs(out[1][2] - 1.89) < 0.02)
# ------------------------------------------------------------------ IV-6 Q3-I
print("\n== IV-6 accumulation reading, density tie: rho_DE ~ t^2 (flat, no radiation, Om=0.3111) ==")
Om, OLq = 0.3111, 0.6889
def integrate(h):
    ti = 1e-6; ai = (1.5 * math.sqrt(Om) * h * ti) ** (2 / 3)
    f = lambda tau, y: [y[0] * h * math.sqrt(Om * y[0] ** -3 + OLq * tau ** 2)]
    return solve_ivp(f, (ti, 1.0), [ai], rtol=1e-12, atol=1e-16, dense_output=True)
h = brentq(lambda h_: integrate(h_).y[0, -1] - 1.0, 0.8, 1.4, xtol=1e-12)
sol = integrate(h); tau = np.linspace(1e-4, 1.0, 40001); aa = sol.sol(tau)[0]
Eq = np.sqrt(Om * aa ** -3 + OLq * tau ** 2); wq = -1 - 2 / (3 * h * Eq * tau)
w0q = -1 - 2 / (3 * h)
sel = aa >= 1 / 3.5; A = np.vstack([np.ones(sel.sum()), 1 - aa[sel]]).T
# uniform in a: resample
agrid = np.linspace(1 / 3.5, 1.0, 400); tg = np.interp(agrid, aa, tau); Eg = np.sqrt(Om * agrid ** -3 + OLq * tg ** 2); wg = -1 - 2 / (3 * h * Eg * tg)
cf = np.linalg.lstsq(np.vstack([np.ones_like(agrid), 1 - agrid]).T, wg, rcond=None)[0]
tz = lambda z: float(np.interp(1 / (1 + z), aa, tau)); adot = {z: math.log10(tz(z)) for z in (0.85, 1.5, 2.5)}
Ez = lambda z: math.sqrt(Om * (1 + z) ** 3 + OLq * tz(z) ** 2); El = lambda z: math.sqrt(Om * (1 + z) ** 3 + OLq)
print(f"  H0 t0 = {h:.4f}; w0 = {w0q:.4f}; CPL fit (a in [1/3.5,1]) = ({cf[0]:.3f}, {cf[1]:.3f}); H(0.5)/H_LCDM(0.5) - 1 = {Ez(0.5)/El(0.5)-1:+.3f}; log10 a0(z)/a0(0) at z=0.85/1.5/2.5: {[round(v,3) for v in adot.values()]}")
run.num("IV6", dict(H0t0=h, w0=w0q, cpl=list(cf), H05=Ez(0.5) / El(0.5) - 1, a0dex=adot))
D = os.path.join(repo, "fable_independent_2026", "data", "desi_dr2_w0wa_thinned")
CH = {n: np.loadtxt(os.path.join(D, f + ".txt")) for n, f in (("DESY5", "desy5sn"), ("Pantheon+", "pantheonplus"), ("Union3", "union3"))}
def maha(pt, d):
    wt, w0, wa = d[:, 0], d[:, 1], d[:, 2]; m = np.array([np.sum(wt * w0) / wt.sum(), np.sum(wt * wa) / wt.sum()])
    c00 = np.sum(wt * (w0 - m[0]) ** 2) / wt.sum(); c11 = np.sum(wt * (wa - m[1]) ** 2) / wt.sum(); c01 = np.sum(wt * (w0 - m[0]) * (wa - m[1])) / wt.sum()
    ci = np.linalg.inv(np.array([[c00, c01], [c01, c11]])); dv = np.array(pt) - m; return math.sqrt(float(dv @ ci @ dv))
dm = {n: (maha(cf, d), maha((-1.0, 0.0), d), float(d[:, 0][d[:, 1] <= w0q].sum() / d[:, 0].sum())) for n, d in CH.items()}
print("  Mahalanobis distance of the model CPL / of LCDM (-1,0) from each chain; chain weight with w0 <= model w0:", {n: tuple(round(x, 3) for x in v) for n, v in dm.items()})
run.check("IV-6a H0 t0 = 1.030+/-0.003 and w0 = -1.647+/-0.01 (self-consistent solve; consistency w0 = -1-2/(3 H0 t0))", f"H0t0 {h:.4f}, w0 {w0q:.4f}", abs(h - 1.030) < 0.003 and abs(w0q + 1.647) < 0.01)
run.check("IV-6b CPL fit (-1.70+/-0.03, -0.52+/-0.05); H(0.5) 13% below LCDM +/-2%", f"{cf.round(3)}, {Ez(0.5)/El(0.5)-1:+.3f}", abs(cf[0] + 1.70) < 0.03 and abs(cf[1] + 0.52) < 0.05 and abs(Ez(0.5) / El(0.5) - 1 + 0.13) < 0.02)
run.check("IV-6c a0(z)/a0(0) = -0.34/-0.53/-0.75 dex at z=0.85/1.5/2.5 within 0.02 dex", f"{[round(v,3) for v in adot.values()]}", abs(adot[0.85] + 0.34) < 0.02 and abs(adot[1.5] + 0.53) < 0.02 and abs(adot[2.5] + 0.75) < 0.02)
run.check("IV-6d Gaussian-proxy distance 27-36 sigma (model) vs 3.0-4.3 sigma (LCDM); chain weight with w0 <= model = 0", str({n: (round(v[0], 1), round(v[1], 2), v[2]) for n, v in dm.items()}), all(25 < v[0] < 40 for v in dm.values()) and all(2.8 < v[1] < 4.5 for v in dm.values()) and all(v[2] == 0 for v in dm.values()))
# ------------------------------------------------------------------ I-6a thawing best nodes (own CLW implementation)
print("\n== I-6a exponential-potential thawing field (CLW system, dust + field, frozen at z=30), best node per chain ==")
Zi = 30.0
def clw(lam, yi2):
    s3 = math.sqrt(1.5)
    def rhs(N, u):
        x, y = u; com = 1.5 * (2 * x * x + (1 - x * x - y * y))
        return [-3 * x + lam * s3 * y * y + x * com, -lam * s3 * x * y + y * com]
    return solve_ivp(rhs, (-math.log(1 + Zi), 0.0), [0.0, math.sqrt(yi2)], rtol=1e-10, atol=1e-14, dense_output=True)
def shoot(lam, Ophi0):
    g = lambda ly: (lambda s_: s_.y[0, -1] ** 2 + s_.y[1, -1] ** 2)(clw(lam, math.exp(ly))) - Ophi0
    return math.exp(brentq(g, math.log(1e-9), math.log(0.2), xtol=1e-10))
def track(lam, Om_):
    Ophi0 = 1 - Om_; sol_ = clw(lam, shoot(lam, Ophi0)); Ns = np.linspace(-math.log(1 + Zi), 0.0, 1500); x, y = sol_.sol(Ns)
    Ophi = x * x + y * y; E2 = Om_ * np.exp(-3 * Ns) / (1 - Ophi); rho = Ophi * E2 / Ophi0; w = (x * x - y * y) / Ophi
    return Ns, np.sqrt(E2), rho, w
def F_thaw(Ns, E, rho, w, Om_, k=0.75):
    integrand = np.maximum(1 + w, 0) * rho / E; num = np.trapz(integrand, Ns)
    t0H0 = np.trapz(1 / E, Ns) + math.exp(1.5 * Ns[0]) / (1.5 * math.sqrt(Om_))
    return k * num / t0H0
def cpl_equiv(Ns, w):
    a = np.exp(Ns); sel = a >= 1 / 3.5 - 1e-12; A_ = np.vstack([np.ones(sel.sum()), 1 - a[sel]]).T
    return np.linalg.lstsq(A_, w[sel], rcond=None)[0]
res = {}
for n, d in CH.items():
    wt = d[:, 0]; Omm = float(np.sum(wt * d[:, 3]) / wt.sum()); best = None
    for lam in np.linspace(0.1, 2.0, 20):
        try: Ns, E, rho, w = track(lam, Omm)
        except Exception: continue
        cp = cpl_equiv(Ns, w); dd = maha(cp, d)
        if best is None or dd < best[0]: best = (dd, lam, cp, F_thaw(Ns, E, rho, w, Omm), F_thaw(Ns, E, rho, w, Omm, k=math.sqrt(3) / 2))
    res[n] = best; print(f"  {n:10s} best lambda {best[1]:.2f} (grid of 20 on [0.1,2]); CPL-equivalent ({best[2][0]:+.3f},{best[2][1]:+.3f}); Mahalanobis distance to chain mean {best[0]:.2f}; F(k=3/4) = {best[3]:.4f}; F(k=sqrt3/2) = {best[4]:.4f}")
run.num("I6a", {n: dict(lam=v[1], cpl=list(v[2]), dist=v[0], F34=v[3], F_sq3h=v[4]) for n, v in res.items()})
run.check("I-6a NEC-respecting thawing field best node: F(k=3/4) < 0.07 (well below R) for all three chains", str({n: round(v[3], 4) for n, v in res.items()}), all(v[3] < 0.07 for v in res.values()))
run.finish()
