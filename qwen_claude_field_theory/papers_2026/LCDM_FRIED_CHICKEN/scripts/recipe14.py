"""Amendment A12 of ../FROZEN_RECIPE.md: one-scale action tying the field cap to rho_DE. A posit, not a derivation. Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
from lib import *
from scipy.optimize import brentq
hbarc = 1.97327e-7; kg = 5.6096e35; MPl = 2.435e27; KAP = .5; c_ = 2.998e8; hbar = 1.0546e-34; eV = 1.602e-19
rde = (A0 / (KAP * c_))**2 / G; Lam = ((rde * c_**2) * (hbarc)**3 / eV)**.25; L2 = Lam**2; beta = KAP / np.sqrt(8 * np.pi); cc_ = 2 * beta**2
a_n = beta * L2 / MPl; a_si = a_n * eV / hbar * c_ / 1e0 * 1; a_si = a_n * c_ * eV / hbar
print(f'Lambda = rho_DE^(1/4) = {Lam * 1e3:.3f} meV; beta {beta:.4f}; c {cc_:.4f}; a0 from action {a_si:.4e} m/s^2 against {A0:.4e}, ratio {a_si / A0:.4f}')
H = lambda s: -s**2 / 2 - s - np.log(1 - s)
R, Smax = [], 0
for g in GS:
    Mn = g.mb * kg; rn = g.r / hbarc; q = beta * Mn / (4 * np.pi * rn**2 * MPl) / (cc_ * L2); s = .5 * (-q + np.sqrt(q**2 + 4 * q)); y = s * a_si; R.append(np.log10(g.gb + y) - np.log10(g.gl)); Smax = max(Smax, s.max())
R = np.concatenate(R); e = np.sqrt((R**2).mean()); print(f'D1 Gauss solve, {len(R)} points: rms to law {e:.5f} dex, mean {R.mean():+.5f} [{"PASS" if e <= .005 else "FAIL"}]; max s {Smax:.3f}')
print(f'D2 field energy/rho_DE: at SPARC max s {cc_ * H(Smax):.4f}')
gn = 1.327e20 / 1.496e11**2; s1 = 1 - A0 / gn; print(f'   at 1 AU, 1 - s about {A0 / gn:.2e}: {cc_ * H(s1):.3f}')
print(f'D3 (grad phi max)^2 / rho_DE = {(a_n * MPl / beta)**2 / L2**2:.4f}, equal by the posit')
print(f'D4 epsilon = beta_b/beta at most about {1 / 4.59:.3f} (2.44-4.59x failure, linear scaling, order of magnitude); {1 / 2.44:.3f} at the mild end')
hc = 1.973e-5; rho0 = .12 * 1.054e-5 * 1e9 * hc**3; m = Lam; gs = 106.75; Tosc = (m * MPl / (np.pi * np.sqrt(gs / 90)))**.5; s0 = 2891 * hc**3; sosc = 2 * np.pi**2 / 45 * gs * Tosc**3; fneed = np.sqrt(2 * rho0 * sosc / s0) / m; fone = L2 / m
print(f'D5 m = Lambda: T_osc {Tosc:.1e} eV; f needed {fneed:.1e} eV; one-scale f = Lambda^2/m = {fone:.1e} eV; mismatch {np.log10(fneed / fone):.1f} decades; rho from one scale / rho needed about 1e{2 * np.log10(fone / fneed):.0f}')
print('A posit, not a derivation; UW1 stands. kappa = 1/2 FITTED; not theory closed.')
