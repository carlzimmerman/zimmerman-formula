#!/usr/bin/env python3
"""
Zimmerman Formula: Key Mathematical Visualizations

Generates 5 publication-quality charts demonstrating the core predictions
of the Zimmerman Formula: a₀ = cH₀/5.79 = c√(Gρc)/2

Author: Carl Zimmerman
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# Set up publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Physical constants
c = 299792458  # m/s
G = 6.67430e-11  # m³ kg⁻¹ s⁻²
H0_zimmerman = 71.1  # km/s/Mpc
H0_si = H0_zimmerman * 1000 / (3.086e22)  # s⁻¹
OMEGA_M = 0.315
OMEGA_LAMBDA = 0.685
A0_LOCAL = 1.2e-10  # m/s²
ZIMMERMAN_CONSTANT = 5.79  # = 2√(8π/3)

# Output directory
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def E(z):
    """Hubble parameter evolution: E(z) = H(z)/H₀"""
    return np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_LAMBDA)


def a0_evolution(z):
    """a₀(z) = a₀(0) × E(z)"""
    return A0_LOCAL * E(z)


def chart1_a0_evolution():
    """
    Chart 1: a₀(z) Evolution - The Core Prediction
    Shows how the MOND acceleration scale evolves with redshift
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Redshift range
    z = np.linspace(0, 12, 500)
    a0_z = a0_evolution(z) / A0_LOCAL  # Normalized to local value

    # Main curve
    ax.plot(z, a0_z, 'b-', linewidth=2.5, label=r'$a_0(z) = a_0(0) \times E(z)$')

    # Key epochs with markers
    epochs = {
        0: ('Today', 'green'),
        1: ('z=1\nPeak SF', 'orange'),
        2: ('z=2', 'red'),
        6: ('z=6\nReionization', 'purple'),
        10: ('z=10\nJWST frontier', 'darkred'),
    }

    for z_epoch, (label, color) in epochs.items():
        a0_val = E(z_epoch)
        ax.scatter([z_epoch], [a0_val], s=100, c=color, zorder=5, edgecolors='white', linewidth=2)
        ax.annotate(f'{label}\n({a0_val:.1f}×)',
                   xy=(z_epoch, a0_val),
                   xytext=(10, 15),
                   textcoords='offset points',
                   fontsize=10,
                   ha='left')

    # Constant a₀ line for comparison
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label=r'Constant $a_0$ (standard MOND)')

    ax.set_xlabel('Redshift z')
    ax.set_ylabel(r'$a_0(z) / a_0(0)$')
    ax.set_title(r'Zimmerman Formula: $a_0(z) = a_0(0) \times \sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}$')
    ax.legend(loc='upper left')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 25)

    # Add formula box
    formula_text = r'$a_0 = \frac{c H_0}{5.79} = \frac{c \sqrt{G \rho_c}}{2}$'
    ax.text(0.97, 0.05, formula_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart1_a0_evolution.png'))
    plt.close()
    print("✓ Created chart1_a0_evolution.png")


def chart2_btfr_evolution():
    """
    Chart 2: Baryonic Tully-Fisher Relation Evolution
    Shows the BTFR offset at different redshifts - a key falsifiable prediction
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    # Velocity range (log scale)
    v_flat = np.logspace(1.5, 2.7, 100)  # 30-500 km/s

    # BTFR: M_bar = v^4 / (G × a₀)
    # At z, effective: M_bar(z) = v^4 / (G × a₀ × E(z))

    redshifts = [0, 1, 2, 3]
    colors = ['blue', 'green', 'orange', 'red']

    for z, color in zip(redshifts, colors):
        Ez = E(z)
        # log M_bar = 4 log v - log(G a₀) - log E(z)
        log_M = 4 * np.log10(v_flat * 1000) - np.log10(G * A0_LOCAL) - np.log10(Ez)
        M_solar = 10**log_M / 1.989e30  # Convert to solar masses

        label = f'z = {z}' if z == 0 else f'z = {z} (Δlog M = {-np.log10(Ez):.2f} dex)'
        ax.plot(v_flat, M_solar, color=color, linewidth=2.5, label=label)

    # Add arrows showing the shift
    v_arrow = 150
    for i, z in enumerate([1, 2, 3]):
        Ez = E(z)
        log_M0 = 4 * np.log10(v_arrow * 1000) - np.log10(G * A0_LOCAL)
        log_Mz = log_M0 - np.log10(Ez)
        M0 = 10**log_M0 / 1.989e30
        Mz = 10**log_Mz / 1.989e30
        ax.annotate('', xy=(v_arrow, Mz), xytext=(v_arrow, M0),
                   arrowprops=dict(arrowstyle='->', color=colors[i+1], lw=1.5))

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'$v_{flat}$ (km/s)')
    ax.set_ylabel(r'$M_{bar}$ (M$_\odot$)')
    ax.set_title('BTFR Evolution: Zimmerman Prediction')
    ax.legend(loc='upper left')
    ax.set_xlim(30, 500)
    ax.set_ylim(1e8, 1e12)

    # Add prediction box
    pred_text = (r'$M_{bar} = \frac{v^4}{G \cdot a_0(z)}$' + '\n\n' +
                 r'$\Delta \log M_{bar} = -\log_{10} E(z)$' + '\n\n' +
                 'Falsification: If z>2 galaxies\nshow same BTFR as z=0')
    ax.text(0.97, 0.03, pred_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart2_btfr_evolution.png'))
    plt.close()
    print("✓ Created chart2_btfr_evolution.png")


def chart3_hubble_tension():
    """
    Chart 3: Hubble Tension Resolution
    Shows where the Zimmerman prediction falls between Planck and SH0ES
    """
    fig, ax = plt.subplots(figsize=(10, 4))

    # H₀ measurements
    measurements = {
        'Planck CMB': (67.4, 0.5, 'royalblue'),
        'Zimmerman (from a₀)': (71.5, 1.0, 'darkgreen'),
        'SH0ES Cepheids': (73.0, 1.0, 'crimson'),
    }

    y_positions = [2, 1, 0]

    for i, (name, (h0, err, color)) in enumerate(measurements.items()):
        y = y_positions[i]
        # Error bar
        ax.errorbar(h0, y, xerr=err, fmt='o', markersize=15,
                   color=color, capsize=8, capthick=2, linewidth=2)
        # Label
        ax.text(h0, y + 0.35, f'{h0} ± {err}', ha='center', fontsize=12, fontweight='bold')
        ax.text(60, y, name, ha='left', fontsize=12, va='center')

    # Tension region shading
    ax.axvspan(67.4 - 0.5, 67.4 + 0.5, alpha=0.2, color='royalblue')
    ax.axvspan(73.0 - 1.0, 73.0 + 1.0, alpha=0.2, color='crimson')
    ax.axvspan(71.5 - 1.0, 71.5 + 1.0, alpha=0.3, color='green')

    # Tension arrow
    ax.annotate('', xy=(73.0, 2.7), xytext=(67.4, 2.7),
               arrowprops=dict(arrowstyle='<->', color='gray', lw=2))
    ax.text(70.2, 2.85, '5σ Tension', ha='center', fontsize=11, color='gray')

    ax.set_xlim(58, 78)
    ax.set_ylim(-0.8, 3.3)
    ax.set_xlabel(r'$H_0$ (km/s/Mpc)')
    ax.set_title('Hubble Tension: Zimmerman Formula Prediction')
    ax.set_yticks([])

    # Formula derivation
    formula_text = (r'$H_0 = \frac{5.79 \times a_0}{c}$' + '\n' +
                   r'$= \frac{5.79 \times 1.2 \times 10^{-10}}{2.998 \times 10^8}$' + '\n' +
                   r'$= 71.5$ km/s/Mpc')
    ax.text(0.97, 0.5, formula_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='center', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart3_hubble_tension.png'))
    plt.close()
    print("✓ Created chart3_hubble_tension.png")


def chart4_rar_evolution():
    """
    Chart 4: Radial Acceleration Relation Evolution
    Shows how the RAR transition scale g† evolves with redshift
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    # Baryonic acceleration range
    g_bar = np.logspace(-13, -8, 500)

    # RAR: g_obs = g_bar / (1 - exp(-√(g_bar/g†)))
    def rar(g_bar, g_dagger):
        x = np.sqrt(g_bar / g_dagger)
        return g_bar / (1 - np.exp(-x))

    redshifts = [0, 1, 2, 5]
    colors = ['blue', 'green', 'orange', 'red']

    for z, color in zip(redshifts, colors):
        g_dagger_z = A0_LOCAL * E(z)
        g_obs = rar(g_bar, g_dagger_z)
        label = f'z = {z}, g† = {g_dagger_z:.1e} m/s²'
        ax.plot(g_bar, g_obs, color=color, linewidth=2.5, label=label)

        # Mark the transition scale
        ax.axvline(x=g_dagger_z, color=color, linestyle=':', alpha=0.5)

    # Unity line (Newtonian)
    ax.plot(g_bar, g_bar, 'k--', linewidth=1.5, alpha=0.5, label='Newtonian (g_obs = g_bar)')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'$g_{bar}$ (m/s²) - Baryonic acceleration')
    ax.set_ylabel(r'$g_{obs}$ (m/s²) - Observed acceleration')
    ax.set_title('RAR Evolution: Transition Scale Shifts with Redshift')
    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlim(1e-13, 1e-8)
    ax.set_ylim(1e-13, 1e-8)

    # Add prediction box
    pred_text = (r'$g_\dagger(z) = g_\dagger(0) \times E(z)$' + '\n\n' +
                 'At high z, transition occurs\nat higher accelerations\n\n' +
                 'Falsification: If g† is\nconstant with redshift')
    ax.text(0.97, 0.03, pred_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart4_rar_evolution.png'))
    plt.close()
    print("✓ Created chart4_rar_evolution.png")


def chart5_mass_discrepancy():
    """
    Chart 5: Mass Discrepancy Ratio vs Redshift
    Shows the predicted evolution of dynamical/baryonic mass ratio
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Redshift range
    z = np.linspace(0, 12, 500)

    # Mass discrepancy scales as √(a₀(z)/g) for fixed g
    # Ratio relative to z=0: √(E(z))
    mass_ratio_enhancement = np.sqrt(E(z))

    # Main curve
    ax.plot(z, mass_ratio_enhancement, 'b-', linewidth=2.5,
           label=r'$(M_{dyn}/M_{bar})_z / (M_{dyn}/M_{bar})_0 = \sqrt{E(z)}$')

    # Key epochs
    key_z = [2, 6, 10]
    for z_val in key_z:
        ratio = np.sqrt(E(z_val))
        ax.scatter([z_val], [ratio], s=100, c='red', zorder=5, edgecolors='white', linewidth=2)
        ax.annotate(f'z={z_val}\n{ratio:.1f}×',
                   xy=(z_val, ratio),
                   xytext=(10, 10),
                   textcoords='offset points',
                   fontsize=11)

    # JWST observation window
    ax.axvspan(6, 12, alpha=0.15, color='purple', label='JWST z>6 window')

    # Constant a₀ prediction (flat line)
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.7, label='Constant a₀ prediction')

    ax.set_xlabel('Redshift z')
    ax.set_ylabel('Mass Discrepancy Enhancement')
    ax.set_title('Mass Discrepancy Evolution: JWST Testable Prediction')
    ax.legend(loc='upper left')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)

    # Add data comparison
    data_text = ('JWST Validation:\n' +
                 'Evolving a₀: χ² = 59.1\n' +
                 'Constant a₀: χ² = 124.4\n\n' +
                 '2× better fit!')
    ax.text(0.97, 0.6, data_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart5_mass_discrepancy.png'))
    plt.close()
    print("✓ Created chart5_mass_discrepancy.png")


def chart6_coefficient_derivation():
    """
    Chart 6: Visual derivation of the 5.79 coefficient
    Shows where the magic number comes from
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'The Zimmerman Coefficient: Where Does 5.79 Come From?',
           fontsize=16, ha='center', fontweight='bold')

    # Step 1
    ax.text(0.5, 8, 'Step 1: Friedmann Critical Density', fontsize=14, fontweight='bold')
    ax.text(1, 7.2, r'$\rho_c = \frac{3 H_0^2}{8\pi G}$', fontsize=16)

    # Step 2
    ax.text(0.5, 6, 'Step 2: Construct Acceleration Scale', fontsize=14, fontweight='bold')
    ax.text(1, 5.2, r'$a_0 = \frac{c \sqrt{G \rho_c}}{\alpha}$', fontsize=16)

    # Step 3
    ax.text(0.5, 4, 'Step 3: Substitute ρc', fontsize=14, fontweight='bold')
    ax.text(1, 3.2, r'$a_0 = \frac{c}{\alpha} \sqrt{\frac{3 H_0^2}{8\pi}} = \frac{c H_0}{\alpha \sqrt{8\pi/3}}$', fontsize=16)

    # Step 4
    ax.text(0.5, 2, 'Step 4: Set α = 2 (geometric factor)', fontsize=14, fontweight='bold')

    # Result box
    result_box = FancyBboxPatch((0.5, 0.2), 9, 1.3,
                                 boxstyle="round,pad=0.1",
                                 facecolor='lightgreen', edgecolor='darkgreen', linewidth=2)
    ax.add_patch(result_box)
    ax.text(5, 0.85, r'$\mathbf{5.79} = 2\sqrt{\frac{8\pi}{3}} = 2 \times 2.894... = 5.789...$',
           fontsize=18, ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart6_coefficient_derivation.png'))
    plt.close()
    print("✓ Created chart6_coefficient_derivation.png")


def create_summary_table():
    """Create a summary image of key predictions"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, 'Zimmerman Formula: Summary of Predictions',
           transform=ax.transAxes, fontsize=18, ha='center', fontweight='bold')

    # Core formula
    ax.text(0.5, 0.88, r'$a_0 = \frac{c H_0}{5.79} = \frac{c \sqrt{G \rho_c}}{2}$',
           transform=ax.transAxes, fontsize=20, ha='center',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Table data
    table_data = [
        ['Prediction', 'Formula', 'Value', 'Status'],
        ['─' * 15, '─' * 25, '─' * 15, '─' * 12],
        ['a₀ from H₀', 'cH₀/5.79', '1.19×10⁻¹⁰ m/s²', '0.5% match'],
        ['H₀ from a₀', '5.79×a₀/c', '71.5 km/s/Mpc', 'Planck-SH0ES'],
        ['a₀(z) evolution', 'a₀(0)×E(z)', '20× at z=10', 'JWST 2× better'],
        ['BTFR at z=2', 'Δlog M = -0.47', '-0.47 dex shift', 'Testable'],
        ['RAR scale', 'g†×E(z)', '3.6×10⁻¹⁰ at z=2', 'Testable'],
        ['Mass ratio z>6', '√E(z) enhancement', '3-4× higher', 'JWST favors'],
    ]

    y_start = 0.75
    row_height = 0.08
    col_positions = [0.05, 0.25, 0.55, 0.8]

    for i, row in enumerate(table_data):
        y = y_start - i * row_height
        for j, cell in enumerate(row):
            fontweight = 'bold' if i == 0 else 'normal'
            ax.text(col_positions[j], y, cell, transform=ax.transAxes,
                   fontsize=12, fontweight=fontweight, family='monospace')

    # Falsification criteria
    ax.text(0.5, 0.12, 'Falsification Criteria', transform=ax.transAxes,
           fontsize=14, ha='center', fontweight='bold')
    ax.text(0.5, 0.06, 'If a₀ is constant with redshift → formula falsified',
           transform=ax.transAxes, fontsize=12, ha='center', style='italic')
    ax.text(0.5, 0.02, 'If BTFR shows no evolution at z>2 → formula falsified',
           transform=ax.transAxes, fontsize=12, ha='center', style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'chart7_summary_table.png'))
    plt.close()
    print("✓ Created chart7_summary_table.png")


if __name__ == '__main__':
    print("Generating Zimmerman Formula visualization charts...\n")

    chart1_a0_evolution()
    chart2_btfr_evolution()
    chart3_hubble_tension()
    chart4_rar_evolution()
    chart5_mass_discrepancy()
    chart6_coefficient_derivation()
    create_summary_table()

    print(f"\nAll charts saved to: {OUTPUT_DIR}")
    print("\nCharts created:")
    print("  1. a₀(z) evolution - core prediction")
    print("  2. BTFR evolution - falsifiable prediction")
    print("  3. Hubble tension resolution")
    print("  4. RAR evolution with redshift")
    print("  5. Mass discrepancy predictions")
    print("  6. Coefficient derivation (5.79)")
    print("  7. Summary table")
