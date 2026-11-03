"""Post v1.1, not in any deposit: what the formula-exact halo R12 limits about a particle reading. Order-of-magnitude bounds, spherical, isotropic, rival language only, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
hbar, eV, c = 1.0546e-34, 1.602e-19, 2.998e8; Gyr = 3.156e16; T = 13 * Gyr
print('a0/(2 pi G) =', round(A0 / (2 * np.pi * G) * (kpc / 1e3)**2 / Msun, 1), 'Msun/pc^2')
RO, SIG, Q, ML, SM, TG, SS, RR, V, Rr1 = [], [], [], [], [], [], [], [], [], []
for g in GS:
    r = g.r; m = (g.gl - g.gb) * r**2 / G; rr = np.logspace(np.log10(r[0]), np.log10(r[-1]), 60); lm = gaussian_filter1d(np.interp(np.log(rr), np.log(r), np.log(np.maximum(m, 1e-3 * m.max()))), 3); mm = np.exp(lm)
    rho = np.gradient(mm, rr) / (4 * np.pi * rr**2); gt = np.interp(rr, r, g.gl)
    if (rho <= 0).any(): rho = np.maximum(rho, 1e-3 * rho[rho > 0].min())
    ex = rr[-1] * np.logspace(0, 2, 40); rhoe = rho[-1] * (rr[-1] / ex)**2; gte = gt[-1] * rr[-1] / ex
    X = np.r_[rr, ex[1:]]; Rho = np.r_[rho, rhoe[1:]]; Gt = np.r_[gt, gte[1:]]
    I = np.cumsum((Rho * Gt)[::-1] * np.gradient(X)[::-1])[::-1]; s2 = I / Rho
    i = np.argmax(rho / s2[:60]**1.5); q = rho[i] / (2 * np.pi * s2[i])**1.5
    SIG.append(np.sqrt(s2[i])); RO.append(rho[i]); RR.append(rr[i]); Q.append(q)
    TG.append((q * (2 * np.pi * hbar)**3 / 2)**.25 * c**2 / eV)
    ML.append(hbar / (np.sqrt(s2[i]) * rr[i]) * c**2 / eV)
    SM.append(1 / (rho[i] * np.sqrt(s2[i]) * 4 / np.sqrt(np.pi) * T))
    j = np.argmin(abs(rr - np.minimum(rr[-1], 2 * rr[i]))); Rr1.append(rho[i] * rr[i] * (kpc / 1e3)**2 / Msun)
A = lambda x, f=1: np.round(np.percentile(np.array(x) * f, [16, 50, 84]), 3 if f != 1 else 3).tolist()
print('p16, p50, p84 at each galaxy\'s max phase-space density point')
print(' radius kpc', A(RR, 1 / kpc)); print(' dark density Msun/pc^3', A(RO, (kpc / 1e3)**3 / Msun)); print(' dispersion km/s', A(SIG, 1e-3)); print(' rho r Msun/pc^2', A(Rr1))
print(f' fermion floor, g = 2, eV: p50 {np.median(TG):.1f}, largest galaxy value {np.max(TG):.1f}')
print(f' boson floor hbar/(m sigma) < r, eV: p50 {np.median(ML):.2e}, largest {np.max(ML):.2e}')
print(f' self-interaction with one scatter in 13 Gyr, cm^2/g: p50 {np.median(SM) * 10:.2f}, smallest {np.min(SM) * 10:.2f}')
print('Order of magnitude. Bounds if the particle reading is taken, not a detection. kappa = 1/2 FITTED; not theory closed.')
