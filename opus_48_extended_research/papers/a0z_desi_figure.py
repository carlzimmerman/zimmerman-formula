#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
a0(z) under DESI DR2 evolving dark energy — the centerpiece computation + figure for
"Dark Energy Sets the Galaxy Acceleration Scale: A Parameter-Free a0(z) Test LCDM Cannot Take".

Framework: a0(z) = (c/2) sqrt(G rho_DE(z))  =>  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0).
CPL: rho_DE(z)/rho0 = (1+z)^(3(1+w0+wa)) * exp(-3 wa z/(1+z)).
DESI DR2 (arXiv:2503.14738) w0wa CDM, three SNe combinations.
Rival "rising" reading: a0 ~ cH/E(z) => sqrt(rho_total)/sqrt(rho_DE0)-normalized.
Quarantine: a0(0)=9.36e-11 is the INPUT; only the SHAPE a0(z)/a0(0) is the prediction.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def a0z(z, w0, wa):
    rho = (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
    return np.sqrt(rho)

Om = 0.3153; OL = 1 - Om
def rising_total(z):
    return np.sqrt(Om*(1+z)**3 + OL)/np.sqrt(OL)

combos = {
    'DESI+CMB+DESY5  (w0=-0.752, wa=-0.86)': (-0.752, -0.86),
    'DESI+CMB+Pantheon+  (-0.838, -0.62)':   (-0.838, -0.62),
    'DESI+CMB+Union3  (-0.667, -1.09)':      (-0.667, -1.09),
}

# ---- data table ----
print("a0(z)/a0(0)  [quarantine: a0(0) is INPUT; the SHAPE is the prediction]")
zs = [0.0, 0.2, 0.4, 0.5, 1.0, 1.5, 2.0, 3.0]
hdr = f"{'z':>4} | {'const(LCDM)':>11} | " + " | ".join(f"{k.split()[0]:>9}" for k in combos) + f" | {'rising_tot':>10}"
print(hdr); print('-'*len(hdr))
for z in zs:
    row = f"{z:>4.1f} | {1.000:>11.3f} | " + " | ".join(f"{a0z(z,*v):>9.3f}" for v in combos.values()) + f" | {rising_total(z):>10.3f}"
    print(row)

zf = np.linspace(0,1,2001); cv = a0z(zf,-0.752,-0.86); ip = np.argmax(cv)
print(f"\nDESY5 low-z BUMP peak: a0(z={zf[ip]:.3f})/a0(0) = {cv[ip]:.4f}  (+{100*(cv[ip]-1):.1f}%)")
print(f"DESY5 z=3: {a0z(3,-0.752,-0.86):.4f} (canonical ~0.74) | rising_tot z=3: {rising_total(3):.2f}")
print(f"discriminator @ z=3: framework {a0z(3,-0.752,-0.86):.2f} vs const 1.00 vs rising {rising_total(3):.2f} (factor {rising_total(3)/a0z(3,-0.752,-0.86):.1f})")

# ---- figure ----
z = np.linspace(0, 3.2, 400)
fig, ax = plt.subplots(figsize=(8.2, 5.6))
ax.axhline(1.0, color='0.5', lw=2.2, ls='--', label='Constant $a_0$  (pure $\\Lambda$ / standard MOND)')
# DESI band across the three combos
band = np.vstack([a0z(z,*v) for v in combos.values()])
ax.fill_between(z, band.min(0), band.max(0), color='#1f6feb', alpha=0.18, label='Framework $a_0(z)=(c/2)\\sqrt{G\\rho_{\\rm DE}(z)}$  (DESI DR2 $w_0w_a$ band)')
ax.plot(z, a0z(z,-0.752,-0.86), color='#1f6feb', lw=2.6, label='   central (DESI+CMB+DESY5)')
ax.plot(z, rising_total(z), color='#d1242f', lw=2.4, ls='-.', label='Rival rising $\\sqrt{\\rho_{\\rm tot}}$ reading ($\\propto cH/E(z)$)')
# annotate the bump + the z=3 split
ax.annotate(f'+{100*(cv[ip]-1):.0f}% bump @ z$\\approx${zf[ip]:.2f}', xy=(zf[ip], cv[ip]), xytext=(0.7, 1.18),
            fontsize=9, color='#1f6feb', arrowprops=dict(arrowstyle='->', color='#1f6feb'))
ax.annotate('factor $\\sim$7.5 split\nby z=3', xy=(3.0, 0.74), xytext=(2.25, 2.4), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='0.3'))
ax.set_xlabel('redshift  $z$', fontsize=12)
ax.set_ylabel('$a_0(z)\\,/\\,a_0(0)$', fontsize=12)
ax.set_title('The acceleration scale is made of dark energy: three falsifiable fates of $a_0(z)$', fontsize=11.5)
ax.set_xlim(0, 3.2); ax.set_ylim(0.6, 3.0)
ax.legend(fontsize=8.6, loc='upper left', framealpha=0.95)
ax.grid(alpha=0.25)
fig.tight_layout()
out = 'opus_48_extended_research/papers/a0z_desi_figure.png'
fig.savefig(out, dpi=170); fig.savefig(out.replace('.png','.pdf'))
print(f"\nfigure -> {out} (+ .pdf)")
