#!/usr/bin/env python3
"""
Gravitational Wave Waveform Visualization
==========================================
Author: Carl Zimmerman
Date: 2026-04-24

Creates publication-quality plots of gravitational waveforms.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import json

# Set style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.5
plt.rcParams['grid.linewidth'] = 0.3

# =============================================================================
# CONSTANTS
# =============================================================================

G = 6.67430e-11
c = 2.99792458e8
M_sun = 1.98847e30
Mpc = 3.08567758e22

# =============================================================================
# WAVEFORM GENERATION (inline for self-contained script)
# =============================================================================

def chirp_mass(m1, m2):
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

def frequency_from_tau(tau, M_c):
    M_geo = G * M_c / c**3
    tau_safe = np.maximum(tau, 1e-10)
    return (1/np.pi) * (5 / (256 * tau_safe))**(3/8) * M_geo**(-5/8)

def amplitude_from_frequency(f, M_c, distance):
    term1 = 4.0 / distance
    term2 = (G * M_c / c**2)**(5/3)
    term3 = (np.pi * f / c)**(2/3)
    return term1 * term2 * term3

def generate_waveform(m1_solar, m2_solar, distance_mpc, f_low=20.0):
    m1 = m1_solar * M_sun
    m2 = m2_solar * M_sun
    distance = distance_mpc * Mpc
    M_c = chirp_mass(m1, m2)
    M_total = m1 + m2
    eta = (m1 * m2) / M_total**2

    f_isco = c**3 / (6**(3/2) * np.pi * G * M_total)
    f_high = min(f_isco, 2000)

    M_geo = G * M_c / c**3
    tau_start = (5/256) * M_geo**(-5/3) * (np.pi * f_low)**(-8/3)
    tau_end = (5/256) * M_geo**(-5/3) * (np.pi * f_high)**(-8/3)

    n_points = min(int((tau_start - tau_end) * 4096) + 1, 500000)
    tau = np.linspace(tau_start, max(tau_end, 1e-6), n_points)
    t = -tau

    f = frequency_from_tau(tau, M_c)
    f = np.clip(f, f_low, f_high)
    amplitude = amplitude_from_frequency(f, M_c, distance)

    # Phase with PN corrections
    Theta = eta * tau / (5 * M_geo)
    phase = -2 * Theta**(5/8)
    pn1 = (3715/8064 + 55/96 * eta) * Theta**(-1/4)
    phase = phase * (1 + pn1)

    h = amplitude * np.cos(2 * phase)

    # Add simple ringdown
    M_final = 0.95 * M_total
    f_ring = c**3 / (2 * np.pi * G * M_final) * 0.32
    tau_ring = 2 * G * M_final / c**3 / 0.089

    t_ring = np.linspace(0, 8 * tau_ring, 500)
    h_peak = amplitude[-1] * 1.5
    h_ring = h_peak * np.exp(-t_ring / tau_ring) * np.cos(2 * np.pi * f_ring * t_ring)

    t_full = np.concatenate([t, t_ring])
    h_full = np.concatenate([h, h_ring])
    f_full = np.concatenate([f, np.ones_like(t_ring) * f_ring])

    return t_full, h_full, f_full

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def plot_single_waveform(t, h, f, title, filename, color='cyan'):
    """Plot a single waveform with time-frequency analysis"""

    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(3, 2, height_ratios=[2, 1, 1], width_ratios=[3, 1])

    # Main waveform
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(t, h * 1e21, color=color, linewidth=0.5, alpha=0.9)
    ax1.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='MERGER')
    ax1.set_xlabel('Time before merger (seconds)')
    ax1.set_ylabel('Strain h (×10⁻²¹)')
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(t[0], t[-1])

    # Frequency evolution
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.semilogy(t, f, color='orange', linewidth=1)
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax2.set_xlabel('Time before merger (seconds)')
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_title('Frequency Evolution (The "Chirp")')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(t[0], t[-1])

    # Amplitude evolution
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.semilogy(t, np.abs(h), color='lime', linewidth=1)
    ax3.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('|h|')
    ax3.set_title('Amplitude Growth')
    ax3.grid(True, alpha=0.3)

    # Last 0.5 seconds zoom
    ax4 = fig.add_subplot(gs[2, 0])
    mask = t > -0.5
    if np.sum(mask) > 10:
        ax4.plot(t[mask], h[mask] * 1e21, color=color, linewidth=0.8)
    else:
        mask = t > t[0] + (t[-1] - t[0]) * 0.9
        ax4.plot(t[mask], h[mask] * 1e21, color=color, linewidth=0.8)
    ax4.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax4.set_xlabel('Time before merger (seconds)')
    ax4.set_ylabel('Strain (×10⁻²¹)')
    ax4.set_title('Final Moments (Zoom)')
    ax4.grid(True, alpha=0.3)

    # Spectrogram-like visualization
    ax5 = fig.add_subplot(gs[2, 1])
    # Create a simple time-frequency representation
    n_bins = 50
    t_bins = np.linspace(t[0], t[-1], n_bins)
    f_binned = np.interp(t_bins, t, f)
    h_binned = np.interp(t_bins, t, np.abs(h))

    colors = plt.cm.plasma(h_binned / np.max(h_binned))
    ax5.scatter(t_bins, f_binned, c=colors, s=20)
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Freq (Hz)')
    ax5.set_title('Time-Frequency')
    ax5.set_yscale('log')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"Saved: {filename}")


def plot_comparison(events, filename):
    """Plot multiple events for comparison"""

    fig, axes = plt.subplots(len(events), 1, figsize=(14, 4*len(events)))
    if len(events) == 1:
        axes = [axes]

    colors = ['cyan', 'magenta', 'yellow', 'lime']

    for i, (name, params) in enumerate(events.items()):
        t, h, f = generate_waveform(**params)

        ax = axes[i]
        ax.plot(t, h * 1e21, color=colors[i % len(colors)], linewidth=0.5, alpha=0.9)
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        ax.set_ylabel('Strain (×10⁻²¹)')
        ax.set_title(f'{name}: m₁={params["m1_solar"]}M☉, m₂={params["m2_solar"]}M☉, d={params["distance_mpc"]} Mpc')
        ax.grid(True, alpha=0.3)

        # Add text with key stats
        duration = t[-1] - t[0]
        peak_strain = np.max(np.abs(h))
        peak_freq = np.max(f)
        ax.text(0.02, 0.95, f'Duration: {duration:.2f}s | Peak: {peak_strain:.2e} | f_max: {peak_freq:.0f} Hz',
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))

    axes[-1].set_xlabel('Time before merger (seconds)')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"Saved: {filename}")


def plot_chirp_diagram(filename):
    """Create a diagram showing the chirp concept"""

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Generate GW170817 waveform
    t, h, f = generate_waveform(1.46, 1.27, 40, f_low=24)

    # 1. Full waveform
    ax1 = axes[0, 0]
    ax1.plot(t, h * 1e22, 'cyan', linewidth=0.3)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Strain (×10⁻²²)')
    ax1.set_title('GW170817: Full Inspiral Waveform')
    ax1.axvline(0, color='red', linestyle='--', label='Merger')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Frequency chirp
    ax2 = axes[0, 1]
    ax2.plot(t, f, 'orange', linewidth=1)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_title('Frequency Evolution: The "Chirp"')
    ax2.set_yscale('log')
    ax2.axhline(100, color='gray', linestyle=':', alpha=0.5, label='100 Hz')
    ax2.axhline(1000, color='gray', linestyle=':', alpha=0.5, label='1000 Hz')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Last second zoom
    ax3 = axes[1, 0]
    mask = t > -1.0
    ax3.plot(t[mask], h[mask] * 1e22, 'cyan', linewidth=0.5)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Strain (×10⁻²²)')
    ax3.set_title('Last Second Before Merger')
    ax3.axvline(0, color='red', linestyle='--')
    ax3.grid(True, alpha=0.3)

    # 4. Orbital diagram concept
    ax4 = axes[1, 1]
    ax4.set_aspect('equal')

    # Draw spiral inspiral
    theta = np.linspace(0, 10*np.pi, 1000)
    r = 1 - theta / (10*np.pi) * 0.8
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Color by time (earlier = dimmer)
    colors = plt.cm.plasma(np.linspace(0, 1, len(theta)))
    for i in range(len(theta)-1):
        ax4.plot(x[i:i+2], y[i:i+2], color=colors[i], linewidth=2)

    # Draw neutron stars at end
    circle1 = plt.Circle((x[-1]-0.05, y[-1]), 0.05, color='cyan', alpha=0.8)
    circle2 = plt.Circle((x[-1]+0.05, y[-1]), 0.04, color='magenta', alpha=0.8)
    ax4.add_patch(circle1)
    ax4.add_patch(circle2)

    ax4.set_xlim(-1.5, 1.5)
    ax4.set_ylim(-1.5, 1.5)
    ax4.set_title('Inspiral Orbit (Schematic)')
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.text(0, -1.3, 'Stars spiral inward, orbit faster, emit stronger GWs',
             ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"Saved: {filename}")


def plot_detector_sensitivity(filename):
    """Plot waveforms against LIGO sensitivity curve"""

    fig, ax = plt.subplots(figsize=(12, 8))

    # Approximate LIGO O3 sensitivity curve
    f_sens = np.logspace(1, 4, 1000)
    # Simplified sensitivity model (not exact)
    h_sens = 1e-23 * (1 + (20/f_sens)**4 + (f_sens/2000)**2)

    ax.loglog(f_sens, h_sens, 'white', linewidth=2, label='LIGO Sensitivity (approx.)')
    ax.fill_between(f_sens, h_sens, 1e-18, alpha=0.1, color='white')

    # Plot signal tracks for different events
    events = {
        'GW170817 (NS-NS, 40 Mpc)': (1.46, 1.27, 40, 'cyan'),
        'GW150914 (BH-BH, 440 Mpc)': (35.6, 30.6, 440, 'magenta'),
        'NS-NS at 200 Mpc': (1.35, 1.35, 200, 'yellow'),
        'BH-BH at 1000 Mpc': (30, 30, 1000, 'lime'),
    }

    for name, (m1, m2, d, color) in events.items():
        t, h, f = generate_waveform(m1, m2, d, f_low=10)
        # Get characteristic strain
        ax.loglog(f, np.abs(h), color=color, linewidth=1.5, alpha=0.8, label=name)

    ax.set_xlabel('Frequency (Hz)', fontsize=12)
    ax.set_ylabel('Strain Amplitude', fontsize=12)
    ax.set_title('Gravitational Wave Signals vs Detector Sensitivity', fontsize=14)
    ax.set_xlim(10, 3000)
    ax.set_ylim(1e-24, 1e-20)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, which='both')

    # Add annotation
    ax.annotate('Detectable region\n(signal > noise)',
                xy=(100, 3e-22), fontsize=10, color='lime',
                ha='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"Saved: {filename}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    base_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/gravitational_waves"

    print("\n" + "=" * 60)
    print("  GENERATING GRAVITATIONAL WAVE VISUALIZATIONS")
    print("=" * 60 + "\n")

    # 1. GW170817 detailed plot
    print("Generating GW170817 (Neutron Star Merger)...")
    t_ns, h_ns, f_ns = generate_waveform(1.46, 1.27, 40, f_low=24)
    plot_single_waveform(t_ns, h_ns, f_ns,
                         'GW170817: Binary Neutron Star Merger\n(m₁=1.46 M☉, m₂=1.27 M☉, d=40 Mpc)',
                         f'{base_path}/plot_gw170817.png', color='cyan')

    # 2. GW150914 detailed plot
    print("Generating GW150914 (Black Hole Merger)...")
    t_bh, h_bh, f_bh = generate_waveform(35.6, 30.6, 440, f_low=20)
    plot_single_waveform(t_bh, h_bh, f_bh,
                         'GW150914: Binary Black Hole Merger\n(m₁=35.6 M☉, m₂=30.6 M☉, d=440 Mpc)',
                         f'{base_path}/plot_gw150914.png', color='magenta')

    # 3. Comparison plot
    print("Generating comparison plot...")
    events = {
        'GW170817 (NS-NS)': {'m1_solar': 1.46, 'm2_solar': 1.27, 'distance_mpc': 40, 'f_low': 24},
        'GW150914 (BH-BH)': {'m1_solar': 35.6, 'm2_solar': 30.6, 'distance_mpc': 440, 'f_low': 20},
        'GW190521 (Heavy BH)': {'m1_solar': 85, 'm2_solar': 66, 'distance_mpc': 5300, 'f_low': 15},
    }
    plot_comparison(events, f'{base_path}/plot_comparison.png')

    # 4. Chirp diagram
    print("Generating chirp explanation diagram...")
    plot_chirp_diagram(f'{base_path}/plot_chirp_explained.png')

    # 5. Detector sensitivity
    print("Generating detector sensitivity plot...")
    plot_detector_sensitivity(f'{base_path}/plot_sensitivity.png')

    print("\n" + "=" * 60)
    print("  ALL PLOTS GENERATED!")
    print("=" * 60)
    print(f"\nPlots saved to: {base_path}/")
    print("  - plot_gw170817.png")
    print("  - plot_gw150914.png")
    print("  - plot_comparison.png")
    print("  - plot_chirp_explained.png")
    print("  - plot_sensitivity.png")
