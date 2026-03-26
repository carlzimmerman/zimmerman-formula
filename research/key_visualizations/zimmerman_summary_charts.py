#!/usr/bin/env python3
"""
Zimmerman Formula: Key Mathematical Visualizations
===================================================

Publication-quality charts showing:
1. a₀(z) Evolution - Core derivation visual
2. BTFR Evolution - Falsifiable prediction
3. Hubble Tension Resolution - Predicted value
4. RAR Scale Evolution - Transition scale shift
5. Mass Discrepancy vs Redshift - JWST predictions

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19199167
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patches as mpatches

# Set publication style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['figure.dpi'] = 150

# =============================================================================
# CONSTANTS
# =============================================================================
Z = 2 * np.sqrt(8 * np.pi / 3)  # 5.788810
c = 299792458  # m/s
G = 6.67430e-11  # m³ kg⁻¹ s⁻²
H0 = 70.0  # km/s/Mpc (approximate)
H0_si = H0 * 1000 / 3.086e22  # s⁻¹

Omega_m = 0.315
Omega_L = 0.685
a0_local = 1.2e-10  # m/s²

# =============================================================================
# CHART 1: a₀(z) EVOLUTION
# =============================================================================
def plot_a0_evolution():
    """Core derivation: a₀(z) = a₀(0) × E(z)"""
    fig, ax = plt.subplots(figsize=(12, 8))

    z = np.linspace(0, 15, 1000)
    E_z = np.sqrt(Omega_m * (1 + z)**3 + Omega_L)
    a0_z = a0_local * E_z

    # Main curve
    ax.semilogy(z, a0_z / a0_local, 'cyan', linewidth=3, label=r'$a_0(z)/a_0(0) = E(z)$')

    # Key epochs
    epochs = [
        (0, 'Today', 'white'),
        (0.87, 'El Gordo', 'orange'),
        (2, 'Peak Star\nFormation', 'yellow'),
        (6, 'Reionization\nEnd', 'lime'),
        (10, 'JWST\nGalaxies', 'magenta'),
    ]

    for z_ep, label, color in epochs:
        E_ep = np.sqrt(Omega_m * (1 + z_ep)**3 + Omega_L)
        ax.scatter([z_ep], [E_ep], s=150, c=color, zorder=5, edgecolor='white', linewidth=2)
        ax.annotate(f'{label}\nE={E_ep:.1f}x', (z_ep, E_ep),
                   textcoords="offset points", xytext=(15, 10),
                   fontsize=10, color=color, fontweight='bold')

    # Formula box
    formula_text = r'''$a_0(z) = a_0(0) \times E(z)$

$E(z) = \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$

$a_0(0) = \frac{cH_0}{Z} = 1.2 \times 10^{-10}$ m/s²'''

    props = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='cyan')
    ax.text(0.98, 0.98, formula_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right', bbox=props,
            family='monospace', color='white')

    ax.set_xlabel('Redshift z', fontsize=14)
    ax.set_ylabel(r'$a_0(z) / a_0(0)$', fontsize=14)
    ax.set_title(r'MOND Acceleration Scale Evolution: $a_0(z) = a_0(0) \times E(z)$',
                fontsize=16, fontweight='bold', color='cyan')
    ax.set_xlim(0, 15)
    ax.set_ylim(0.8, 100)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', fontsize=12)

    plt.tight_layout()
    plt.savefig('chart1_a0_evolution.png', dpi=200, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close()
    print("Chart 1: a0(z) Evolution saved")

# =============================================================================
# CHART 2: BTFR EVOLUTION
# =============================================================================
def plot_btfr_evolution():
    """Baryonic Tully-Fisher Relation evolution with redshift"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Velocity range (km/s)
    v = np.logspace(1.5, 2.7, 100)  # 30 - 500 km/s
    v_m = v * 1000  # Convert to m/s

    redshifts = [0, 1, 2, 3]
    colors = ['white', 'cyan', 'lime', 'orange']

    for z_val, color in zip(redshifts, colors):
        E_z = np.sqrt(Omega_m * (1 + z_val)**3 + Omega_L)
        a0_z = a0_local * E_z

        # M_bar in solar masses
        M_bar = v_m**4 / (G * a0_z) / 1.989e30

        shift = -np.log10(E_z)
        label = f'z = {z_val}' if z_val == 0 else f'z = {z_val} (Dlog M = {shift:.2f})'

        ax.loglog(v, M_bar, color=color, linewidth=2.5, label=label)

    # Add prediction box
    pred_text = r'''Zimmerman Prediction:
$M_{bar} = \frac{v^4}{G \cdot a_0(z)}$

$\Delta \log M_{bar}(z) = -\log_{10}(E(z))$

z=1: -0.23 dex
z=2: -0.47 dex
z=3: -0.67 dex'''

    props = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='lime')
    ax.text(0.02, 0.02, pred_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='left', bbox=props,
            family='monospace', color='white')

    ax.set_xlabel('Rotation Velocity (km/s)', fontsize=14)
    ax.set_ylabel(r'Baryonic Mass $M_{bar}$ ($M_\odot$)', fontsize=14)
    ax.set_title('BTFR Evolution: Falsifiable Prediction', fontsize=16, fontweight='bold', color='lime')
    ax.set_xlim(30, 500)
    ax.set_ylim(1e8, 1e13)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', fontsize=11)

    plt.tight_layout()
    plt.savefig('chart2_btfr_evolution.png', dpi=200, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close()
    print("Chart 2: BTFR Evolution saved")

# =============================================================================
# CHART 3: HUBBLE TENSION RESOLUTION
# =============================================================================
def plot_hubble_tension():
    """Hubble constant: Zimmerman prediction vs measurements"""
    fig, ax = plt.subplots(figsize=(14, 6))

    # Data points
    measurements = [
        ('Planck\n(CMB)', 67.4, 0.5, 'royalblue'),
        ('DES Y3', 68.2, 1.0, 'dodgerblue'),
        ('BAO', 68.6, 0.8, 'steelblue'),
        ('TRGB', 69.8, 1.5, 'gold'),
        ('Zimmerman\nFormula', 71.5, 0.3, 'lime'),
        ('SH0ES\n(Cepheids)', 73.0, 1.0, 'orangered'),
        ('H0LiCOW\n(Lensing)', 73.3, 1.8, 'red'),
    ]

    y_pos = np.arange(len(measurements))

    for i, (name, H0_val, err, color) in enumerate(measurements):
        ax.errorbar(H0_val, i, xerr=err, fmt='o', markersize=15,
                   color=color, capsize=8, capthick=2, elinewidth=2,
                   markeredgecolor='white', markeredgewidth=2)
        ax.text(H0_val, i + 0.35, f'{H0_val:.1f}+/-{err:.1f}',
               ha='center', va='bottom', fontsize=10, color=color, fontweight='bold')

    # Zimmerman highlight
    zimmerman_box = plt.Rectangle((70.5, 3.5), 2.0, 1.0,
                                   fill=True, facecolor='lime', alpha=0.2,
                                   edgecolor='lime', linewidth=2)
    ax.add_patch(zimmerman_box)

    formula = r'$H_0 = \frac{Z \cdot a_0}{c} = \frac{5.79 \times 1.2 \times 10^{-10}}{c} = 71.5$ km/s/Mpc'
    ax.text(71.5, 6, formula, ha='center', fontsize=12, color='lime',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.8, edgecolor='lime'))

    ax.set_yticks(y_pos)
    ax.set_yticklabels([m[0] for m in measurements], fontsize=11)
    ax.set_xlabel(r'$H_0$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=14)
    ax.set_title('Hubble Tension: Zimmerman Formula Bridges the Gap',
                fontsize=16, fontweight='bold', color='lime')
    ax.set_xlim(65, 77)
    ax.set_ylim(-0.5, 7)
    ax.axvline(71.5, color='lime', linestyle='--', alpha=0.5, linewidth=2)
    ax.grid(True, alpha=0.3, linestyle='--', axis='x')

    ax.annotate('', xy=(67.4, -0.3), xytext=(73.0, -0.3),
                arrowprops=dict(arrowstyle='<->', color='yellow', lw=2))
    ax.text(70.2, -0.5, '5sigma Tension', ha='center', fontsize=10, color='yellow')

    plt.tight_layout()
    plt.savefig('chart3_hubble_tension.png', dpi=200, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close()
    print("Chart 3: Hubble Tension saved")

# =============================================================================
# CHART 4: RAR SCALE EVOLUTION
# =============================================================================
def plot_rar_evolution():
    """Radial Acceleration Relation with evolving transition scale"""
    fig, ax = plt.subplots(figsize=(12, 8))

    g_bar_ratio = np.logspace(-2, 2, 500)

    redshifts = [0, 1, 2, 5]
    colors = ['white', 'cyan', 'lime', 'orange']

    for z_val, color in zip(redshifts, colors):
        E_z = np.sqrt(Omega_m * (1 + z_val)**3 + Omega_L)
        sqrt_term = np.sqrt(g_bar_ratio / E_z)
        g_obs_ratio = g_bar_ratio / (1 - np.exp(-sqrt_term))

        label = f'z = {z_val}' if z_val == 0 else f'z = {z_val} (g_dag = {E_z:.1f}xa0)'
        ax.loglog(g_bar_ratio, g_obs_ratio, color=color, linewidth=2.5, label=label)

    ax.loglog(g_bar_ratio, g_bar_ratio, 'gray', linestyle='--', linewidth=1.5,
             label='Newtonian (g_obs = g_bar)')
    ax.loglog(g_bar_ratio, np.sqrt(g_bar_ratio), 'gray', linestyle=':', linewidth=1.5,
             label=r'Deep MOND ($g_{obs} = \sqrt{g_{bar} \cdot a_0}$)')

    formula_text = r'''Radial Acceleration Relation:
$g_{obs} = \frac{g_{bar}}{1 - e^{-\sqrt{g_{bar}/g_\dagger}}}$

$g_\dagger(z) = a_0(z) = a_0(0) \times E(z)$

Transition scale shifts to higher
accelerations at higher redshift'''

    props = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='cyan')
    ax.text(0.98, 0.02, formula_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right', bbox=props,
            family='monospace', color='white')

    ax.set_xlabel(r'$g_{bar} / a_0(0)$', fontsize=14)
    ax.set_ylabel(r'$g_{obs} / a_0(0)$', fontsize=14)
    ax.set_title('RAR Evolution: Transition Scale Shifts with Redshift',
                fontsize=16, fontweight='bold', color='cyan')
    ax.set_xlim(0.01, 100)
    ax.set_ylim(0.05, 150)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    plt.savefig('chart4_rar_evolution.png', dpi=200, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close()
    print("Chart 4: RAR Evolution saved")

# =============================================================================
# CHART 5: MASS DISCREPANCY VS REDSHIFT
# =============================================================================
def plot_mass_discrepancy():
    """Mass discrepancy predictions for JWST"""
    fig, ax = plt.subplots(figsize=(12, 8))

    z = np.linspace(0, 20, 200)
    E_z = np.sqrt(Omega_m * (1 + z)**3 + Omega_L)
    mass_ratio = E_z

    ax.semilogy(z, mass_ratio, 'magenta', linewidth=3, label=r'$M_{dyn}/M_{bar}$ enhancement (Zimmerman)')
    ax.axhline(1, color='gray', linestyle='--', linewidth=2, label=r'Constant $a_0$ (standard MOND)')
    ax.axhline(6, color='gray', linestyle=':', linewidth=2, label=r'LCDM (~6x for typical galaxy)')

    jwst_z = [7, 10, 13, 16]
    jwst_E = [np.sqrt(Omega_m * (1 + z_val)**3 + Omega_L) for z_val in jwst_z]
    ax.scatter(jwst_z, jwst_E, s=200, c='yellow', marker='*', zorder=5,
              edgecolor='white', linewidth=2, label='JWST targets')

    for z_val, E_val in zip(jwst_z, jwst_E):
        ax.annotate(f'z={z_val}\n{E_val:.0f}x', (z_val, E_val),
                   textcoords="offset points", xytext=(15, 5),
                   fontsize=9, color='yellow')

    pred_text = r'''JWST Prediction:
At z > 6, galaxies should show
mass discrepancies 10-50x larger
than local Universe

$\frac{M_{dyn}}{M_{bar}} \propto E(z)$

This explains "impossible" early
galaxies without dark matter!'''

    props = dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8, edgecolor='magenta')
    ax.text(0.02, 0.98, pred_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='left', bbox=props,
            family='monospace', color='white')

    ax.set_xlabel('Redshift z', fontsize=14)
    ax.set_ylabel(r'Mass Discrepancy Enhancement', fontsize=14)
    ax.set_title('Mass Discrepancy Evolution: JWST Falsification Test',
                fontsize=16, fontweight='bold', color='magenta')
    ax.set_xlim(0, 20)
    ax.set_ylim(0.5, 100)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='center right', fontsize=10)

    plt.tight_layout()
    plt.savefig('chart5_mass_discrepancy.png', dpi=200, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close()
    print("Chart 5: Mass Discrepancy saved")

# =============================================================================
# CHART 6: COMPLETE Z FRAMEWORK (BONUS)
# =============================================================================
def plot_z_framework():
    """Complete Z framework showing all connections"""
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_facecolor('black')

    ax.text(50, 97, 'THE ZIMMERMAN FRAMEWORK: COMPLETE CLOSURE',
           ha='center', va='top', fontsize=20, fontweight='bold', color='white')

    z_circle = Circle((50, 50), 8, fill=True, facecolor='purple', edgecolor='white', linewidth=3)
    ax.add_patch(z_circle)
    ax.text(50, 50, f'Z = 2*sqrt(8pi/3)\n= {Z:.4f}', ha='center', va='center',
           fontsize=12, fontweight='bold', color='white')

    exact = [
        (30, 70, 'Z^2', '8 x (4pi/3) = 33.51', 'Cube x Sphere'),
        (70, 70, 'Z^4*9/pi^2', '= 1024 = 2^10', '10 bits info'),
        (20, 50, '9Z^2/(8pi)', '= 12', 'SM gauge dim'),
        (80, 50, '3Z^2/(8pi)', '= 4', 'Bekenstein'),
    ]

    for x, y, name, formula, desc in exact:
        box = FancyBboxPatch((x-10, y-5), 20, 10, boxstyle="round,pad=0.3",
                            facecolor='cyan', alpha=0.3, edgecolor='cyan', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+2, name, ha='center', va='center', fontsize=10, fontweight='bold', color='cyan')
        ax.text(x, y-2, formula, ha='center', va='center', fontsize=8, color='white')
        ax.plot([50, x], [50, y], 'cyan', linewidth=1, alpha=0.5)

    physics = [
        (15, 25, 'alpha^-1', '4Z^2 + 3 = 137.04', '0.004%', 'green'),
        (35, 20, 'Omega_L', '3Z/(8+3Z) = 0.685', '0.06%', 'orange'),
        (55, 15, 'eta_B', 'alpha^5(Z^2-4) = 6.1e-10', '0.22%', 'lime'),
        (75, 20, 'A_s', '3*alpha^4/4 = 2.1e-9', '1.3%', 'yellow'),
        (90, 25, 'n_s', '1-1/(5Z) = 0.965', '0.05%', 'orange'),
    ]

    for x, y, name, formula, error, color in physics:
        box = FancyBboxPatch((x-12, y-6), 24, 12, boxstyle="round,pad=0.3",
                            facecolor=color, alpha=0.2, edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+3, name, ha='center', va='center', fontsize=11, fontweight='bold', color=color)
        ax.text(x, y-1, formula, ha='center', va='center', fontsize=7, color='white')
        ax.text(x, y-4, f'Error: {error}', ha='center', va='center', fontsize=7, color='gray')
        ax.plot([50, x], [50, y], color, linewidth=1, alpha=0.5)

    particles = [
        (10, 85, 'm_mu/m_e', '6Z^2+Z = 206.8', '0.03%', 'pink'),
        (30, 90, 'm_tau/m_mu', 'Z+11 = 16.79', '0.03%', 'pink'),
        (70, 90, 'm_p/m_e', '54Z^2+6Z-8', '0.01%', 'pink'),
        (90, 85, 'M_Pl/m_e', '10^(3Z+5)', '0.05%', 'magenta'),
    ]

    for x, y, name, formula, error, color in particles:
        box = FancyBboxPatch((x-12, y-5), 24, 10, boxstyle="round,pad=0.3",
                            facecolor=color, alpha=0.2, edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+2, name, ha='center', va='center', fontsize=10, fontweight='bold', color=color)
        ax.text(x, y-2, formula, ha='center', va='center', fontsize=7, color='white')
        ax.plot([50, x], [50, y], color, linewidth=1, alpha=0.3)

    ax.text(50, 3, 'All derived from Z = 2*sqrt(8pi/3) combining Friedmann geometry (8pi/3) with Bekenstein holography (x2)',
           ha='center', va='bottom', fontsize=10, color='gray', style='italic')

    plt.tight_layout()
    plt.savefig('chart6_z_framework.png', dpi=200, bbox_inches='tight',
                facecolor='black', edgecolor='none')
    plt.close()
    print("Chart 6: Z Framework saved")

# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("GENERATING ZIMMERMAN SUMMARY CHARTS")
    print("=" * 60)

    plot_a0_evolution()
    plot_btfr_evolution()
    plot_hubble_tension()
    plot_rar_evolution()
    plot_mass_discrepancy()
    plot_z_framework()

    print("\n" + "=" * 60)
    print("ALL CHARTS GENERATED SUCCESSFULLY")
    print("=" * 60)
    print("\nFiles created:")
    print("  chart1_a0_evolution.png")
    print("  chart2_btfr_evolution.png")
    print("  chart3_hubble_tension.png")
    print("  chart4_rar_evolution.png")
    print("  chart5_mass_discrepancy.png")
    print("  chart6_z_framework.png")
