"""Amendment A8 of ../FROZEN_RECIPE.md: effective particle properties for the a0 law. Effective description, not a claim a particle exists. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
hbar, eV, c, h_ = 1.0546e-34, 1.602e-19, 2.998e8, 6.626e-34; T = 13 * 3.156e16; KAP = .5; GeV = 1e9
yy = [(law(g.gb) - g.gb) for g in GS]; Y = np.concatenate(yy); GN = ALLB; res = np.abs(Y**2 / (A0 - Y) / GN - 1)
print(f'P1 y^2/(a0-y) = g_N: max |ratio-1| on {len(Y)} points {res.max():.1e}; max y/a0 {(Y / A0).max():.3f}; stiffness ratio p50 {np.median((2 * A0 - Y) / (A0 - Y)):.2f}, max {((2 * A0 - Y) / (A0 - Y)).max():.2f}')
MPl = 2.435e18 * GeV; a_eV = A0 * hbar / c / eV; L = np.sqrt(a_eV * MPl); rde = (A0 / (KAP * c))**2 / G; LDE = (rde * (hbar * c)**3 / c**2 * c**2 / eV**4 / eV**0 * 1)**.25 if False else ((rde * c**2) * (hbar * c)**3 / eV**4)**.25
print(f'P2 a0 = {a_eV:.3e} eV; Lambda(alpha = 1) = {L * 1e3:.3f} meV; rho_DE^(1/4) from the law = {LDE * 1e3:.3f} meV; ratio {L / LDE:.3f}; (kappa/sqrt(8 pi))^(1/2) = {(KAP / np.sqrt(8 * np.pi))**.5:.3f}')
def prof(gb_fn, rlo, rhi, q):
    x = np.linspace(np.log(rlo) - 1, np.log(rhi) + 5, 900); rr = np.exp(x); gb = gb_fn(rr); gl = law(gb); md = rr**2 * (gl - gb) / G; rho = np.maximum(np.gradient(md, x) / (4 * np.pi * rr**3), 1e-40); s2 = np.cumsum((rho * gl * rr)[::-1])[::-1] * (x[1] - x[0]) / rho; return [(np.interp(np.log(a), x, rho), np.sqrt(np.interp(np.log(a), x, s2)), np.sqrt(np.interp(np.log(a), x, gl) * a)) for a in q]
SP = []
for g in GS:
    lr = np.log(g.r); lg = np.log(g.gb); tail = G * max(g.mbtot, g.mb[-1])
    fn = lambda rr, lr=lr, lg=lg, g=g, tail=tail: np.exp(gaussian_filter1d(np.where(np.log(rr) > lr[-1], np.log(tail / rr**2), np.interp(np.log(rr), lr, lg)), 5))
    SP.append(prof(fn, g.r[0], g.r[-1], [g.r[-1]])[0])
SP = np.array(SP); Qs = SP[:, 0] * h_**3 / SP[:, 1]**3; mu_ = lambda Q, nm=1.: (Q / nm)**.25 * c**2 / eV
mU = mu_(Qs).min(); print(f'\nP3 SPARC last point: rho p50 {np.median(SP[:, 0]) * (kpc / 1e3)**3 / Msun:.2e} Msun/pc^3, sigma p50 {np.median(SP[:, 1]) / 1e3:.1f} km/s; m upper bound, all 171 condensed: {mU:.3f} eV; p50 galaxy {np.median(mu_(Qs)):.3f}, best {mu_(Qs).max():.3f}')
CL = []
for Mb in (1e13, 1e14):
    r = prof(lambda rr, Mb=Mb: G * Mb * Msun / rr**2, 10 * kpc, 3000 * kpc, [100 * kpc])[0]; Q = r[0] * h_**3 / r[1]**3; CL.append(mu_(Q)); print(f' M_b {Mb:.0e} at 100 kpc: rho {r[0] * (kpc / 1e3)**3 / Msun:.2e} Msun/pc^3, sigma {r[1] / 1e3:.0f} km/s; not condensed if m > {mu_(Q):.3f} eV')
mL = max(CL); print(f' lower bound on m {mL:.3f} eV, upper {mU:.3f} eV: {"WINDOW" if mL < mU else "NO WINDOW"} [gate]')
for m in (.03, .1, .3, 1, 3, 10, 30, 100):
    print(f'  m {m:g} eV: SPARC condensed at last point {(mu_(Qs) >= m).sum()} of 171; M_b 1e13, 1e14 condensed at 100 kpc: {CL[0] >= m}, {CL[1] >= m}')
sm = 10 / (SP[:, 0] * SP[:, 1] * 4 / np.sqrt(np.pi) * T); print(f'\nP4 sigma/m one scatter in 13 Gyr at last point, cm^2/g: p16, p50, p84 {np.round(np.percentile(sm, [16, 50, 84]), 2).tolist()}')
for m in (mL, mU, .1, 1):
    N = Qs / (m * eV / c**2)**4; print(f'  with Bose factor at m {m:.3f} eV: p50 {np.median(sm / np.maximum(N, 1)):.2e} cm^2/g; median N {np.median(N):.2e}')
print(f'\nP5 thermal relic, Omega_c h^2 = 0.12: 94 eV x 0.12 = {94 * .12:.1f} eV (fermion, g = 2); a thermal relic there is hot, so a light window must be non-thermal')
rho0 = .12 * 1.054e-5 * GeV * (1.973e-14)**3 * 1e-9**0 * 1  # eV^4: Omega h^2 x 1.054e-5 GeV/cm^3 x (hbar c in eV cm)^... below
hc = 1.973e-5  # eV cm
rho0 = .12 * 1.054e-5 * 1e9 * hc**3
for m in (1e-22, 1e-20, 1e-3, .1, 1, 10):
    gs = 3.91 if m < 1e-27 else (3.91 if m < 1e-17 else (10.75 if m < 1e-10 else 106.75)); Tosc = (m * MPl / (np.pi * np.sqrt(gs / 90)))**.5; s0 = 2891 * hc**3; sosc = 2 * np.pi**2 / 45 * gs * Tosc**3; f = np.sqrt(2 * rho0 * sosc / s0) / m
    print(f'  m {m:.0e} eV: T_osc {Tosc:.1e} eV, f theta_i about {f / GeV:.1e} GeV')
for nm, r_ in (('1 AU', 1.496e11), ('Saturn', 1.43e12)):
    gn = 1.327e20 / r_**2; y = .5 * (-gn + np.sqrt(gn**2 + 4 * gn * A0)); print(f'P6 {nm}: g_N {gn:.2e}, y {y:.3e} m/s^2, y/a0 {y / A0:.4f}')
print('Unscreened tail; PAPER58 records failure of Cassini by 2.44-4.59x, CFG770 2557x without stiffness on a different statistic; read from the record. Effective description only. kappa = 1/2 FITTED; not theory closed.')
