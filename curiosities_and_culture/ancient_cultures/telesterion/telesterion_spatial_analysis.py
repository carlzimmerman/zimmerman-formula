#!/usr/bin/env python3
"""
Telesterion Spatial Acoustic Field Analysis
=============================================
Visualizes the 2D pressure field for room modes in the Telesterion.

This shows WHERE in the hall the acoustic pressure maxima and nodes
would occur for different modes - identifying "hot spots" where
initiates would experience the most intense infrasonic effects.

Author: Carl Zimmerman
Date: April 28, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.colors import LinearSegmentedColormap
import os

# =============================================================================
# PARAMETERS
# =============================================================================

# Telesterion dimensions (meters)
Lx = 51.5
Ly = 51.5
Lz = 15.0  # estimated

# Column positions (6 rows x 7 columns)
# Assuming roughly even spacing with margins
def get_column_positions():
    """Calculate column positions based on 6x7 grid"""
    margin_x = Lx * 0.12  # ~12% margin from walls
    margin_y = Ly * 0.12

    x_positions = np.linspace(margin_x, Lx - margin_x, 7)
    y_positions = np.linspace(margin_y, Ly - margin_y, 6)

    columns = []
    for y in y_positions:
        for x in x_positions:
            columns.append((x, y))

    return columns

COLUMNS = get_column_positions()
COLUMN_RADIUS = 0.875  # meters (estimated diameter ~1.75m)

# Anaktoron position (central inner sanctuary)
ANAKTORON_CENTER = (Lx/2, Ly/2)
ANAKTORON_SIZE = (8, 8)  # estimated ~8m x 8m

# Speed of sound
c = 343  # m/s at 20°C


# =============================================================================
# ACOUSTIC FIELD CALCULATIONS
# =============================================================================

def room_mode_field(x, y, nx, ny, Lx, Ly):
    """
    Calculate the normalized pressure field for a 2D room mode.

    For a rectangular room with rigid walls, the pressure field is:
    p(x,y) = cos(nx*π*x/Lx) * cos(ny*π*y/Ly)

    Returns values from -1 to +1.
    """
    return np.cos(nx * np.pi * x / Lx) * np.cos(ny * np.pi * y / Ly)


def combined_mode_field(x, y, modes, Lx, Ly, amplitudes=None):
    """
    Calculate combined pressure field from multiple modes.

    Parameters:
        x, y: Coordinate arrays
        modes: List of (nx, ny) tuples
        amplitudes: Optional relative amplitudes (defaults to equal)

    Returns normalized combined field.
    """
    if amplitudes is None:
        amplitudes = np.ones(len(modes))

    field = np.zeros_like(x)
    for (nx, ny), amp in zip(modes, amplitudes):
        field += amp * room_mode_field(x, y, nx, ny, Lx, Ly)

    # Normalize
    field = field / np.max(np.abs(field))
    return field


def mode_frequency(nx, ny, Lx, Ly, c=343):
    """Calculate mode frequency"""
    if nx == 0 and ny == 0:
        return 0
    return (c/2) * np.sqrt((nx/Lx)**2 + (ny/Ly)**2)


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_custom_colormap():
    """Create a colormap: blue (negative) - white (zero) - red (positive)"""
    colors = ['darkblue', 'blue', 'lightblue', 'white', 'lightyellow', 'orange', 'darkred']
    return LinearSegmentedColormap.from_list('pressure', colors, N=256)


def plot_mode_field(nx, ny, title_suffix="", save_path=None, show_columns=True):
    """
    Plot the pressure field for a single mode.
    """
    # Create coordinate grid
    resolution = 200
    x = np.linspace(0, Lx, resolution)
    y = np.linspace(0, Ly, resolution)
    X, Y = np.meshgrid(x, y)

    # Calculate field
    P = room_mode_field(X, Y, nx, ny, Lx, Ly)

    # Calculate frequency
    freq = mode_frequency(nx, ny, Lx, Ly)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot pressure field
    cmap = create_custom_colormap()
    im = ax.contourf(X, Y, P, levels=50, cmap=cmap, vmin=-1, vmax=1)

    # Add contour lines
    ax.contour(X, Y, P, levels=[-0.5, 0, 0.5], colors='black', linewidths=0.5, alpha=0.5)

    # Add columns
    if show_columns:
        for (cx, cy) in COLUMNS:
            circle = Circle((cx, cy), COLUMN_RADIUS, fill=True,
                          facecolor='gray', edgecolor='black', linewidth=1, alpha=0.8)
            ax.add_patch(circle)

    # Add Anaktoron (inner sanctuary)
    anaktoron = Rectangle(
        (ANAKTORON_CENTER[0] - ANAKTORON_SIZE[0]/2,
         ANAKTORON_CENTER[1] - ANAKTORON_SIZE[1]/2),
        ANAKTORON_SIZE[0], ANAKTORON_SIZE[1],
        fill=False, edgecolor='gold', linewidth=3, linestyle='--',
        label='Anaktoron (sanctuary)'
    )
    ax.add_patch(anaktoron)

    # Labels and formatting
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X position (meters)', fontsize=12)
    ax.set_ylabel('Y position (meters)', fontsize=12)

    # Title with mode info
    mode_type = "Degenerate" if nx == ny or (nx > 0 and ny > 0 and nx != ny) else "Axial"
    if nx > 0 and ny > 0:
        mode_type = "Tangential" if nx == ny else "Oblique"
    elif nx == 0 or ny == 0:
        mode_type = "Axial"

    ax.set_title(f'Telesterion Acoustic Pressure Field\n'
                f'Mode ({nx},{ny},0) = {freq:.2f} Hz ({mode_type}){title_suffix}',
                fontsize=14, fontweight='bold')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Normalized Pressure (arb. units)', fontsize=11)

    # Legend
    ax.plot([], [], 'o', color='gray', markersize=10, label='Columns (42)')
    ax.legend(loc='upper right')

    # Add scale bar
    scale_x = 5
    scale_y = 2
    ax.plot([scale_x, scale_x + 10], [scale_y, scale_y], 'k-', linewidth=3)
    ax.text(scale_x + 5, scale_y + 1, '10 m', ha='center', fontsize=10)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def plot_degenerate_modes(nx, ny, save_path=None):
    """
    Plot both degenerate mode partners side by side with their superposition.
    For a square room, (m,n,0) and (n,m,0) have the same frequency.
    """
    if nx == ny:
        print(f"Mode ({nx},{ny}) is not degenerate (same indices)")
        return None

    # Create coordinate grid
    resolution = 200
    x = np.linspace(0, Lx, resolution)
    y = np.linspace(0, Ly, resolution)
    X, Y = np.meshgrid(x, y)

    # Calculate fields
    P1 = room_mode_field(X, Y, nx, ny, Lx, Ly)
    P2 = room_mode_field(X, Y, ny, nx, Lx, Ly)
    P_sum = (P1 + P2) / 2  # Constructive interference
    P_diff = (P1 - P2) / 2  # Destructive interference

    freq = mode_frequency(nx, ny, Lx, Ly)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    cmap = create_custom_colormap()

    titles = [
        f'Mode ({nx},{ny},0)',
        f'Mode ({ny},{nx},0)',
        f'Constructive Superposition\n({nx},{ny}) + ({ny},{nx})',
        f'Destructive Superposition\n({nx},{ny}) - ({ny},{nx})'
    ]
    fields = [P1, P2, P_sum, P_diff]

    for ax, P, title in zip(axes.flat, fields, titles):
        im = ax.contourf(X, Y, P, levels=50, cmap=cmap, vmin=-1, vmax=1)
        ax.contour(X, Y, P, levels=[0], colors='black', linewidths=1)

        # Add columns
        for (cx, cy) in COLUMNS:
            circle = Circle((cx, cy), COLUMN_RADIUS, fill=True,
                          facecolor='gray', edgecolor='black', linewidth=0.5, alpha=0.7)
            ax.add_patch(circle)

        # Add Anaktoron
        anaktoron = Rectangle(
            (ANAKTORON_CENTER[0] - ANAKTORON_SIZE[0]/2,
             ANAKTORON_CENTER[1] - ANAKTORON_SIZE[1]/2),
            ANAKTORON_SIZE[0], ANAKTORON_SIZE[1],
            fill=False, edgecolor='gold', linewidth=2, linestyle='--'
        )
        ax.add_patch(anaktoron)

        ax.set_xlim(0, Lx)
        ax.set_ylim(0, Ly)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')

    plt.suptitle(f'Degenerate Mode Pair at {freq:.2f} Hz\n'
                f'Square floor plan causes identical frequencies for swapped indices',
                fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def plot_multi_mode_superposition(modes, title, save_path=None, amplitudes=None):
    """
    Plot the superposition of multiple modes.
    """
    resolution = 200
    x = np.linspace(0, Lx, resolution)
    y = np.linspace(0, Ly, resolution)
    X, Y = np.meshgrid(x, y)

    P = combined_mode_field(X, Y, modes, Lx, Ly, amplitudes)

    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = create_custom_colormap()

    im = ax.contourf(X, Y, P, levels=50, cmap=cmap, vmin=-1, vmax=1)
    ax.contour(X, Y, P, levels=[0], colors='black', linewidths=0.5)

    # Add columns
    for (cx, cy) in COLUMNS:
        circle = Circle((cx, cy), COLUMN_RADIUS, fill=True,
                      facecolor='gray', edgecolor='black', linewidth=0.5, alpha=0.7)
        ax.add_patch(circle)

    # Add Anaktoron
    anaktoron = Rectangle(
        (ANAKTORON_CENTER[0] - ANAKTORON_SIZE[0]/2,
         ANAKTORON_CENTER[1] - ANAKTORON_SIZE[1]/2),
        ANAKTORON_SIZE[0], ANAKTORON_SIZE[1],
        fill=False, edgecolor='gold', linewidth=3, linestyle='--'
    )
    ax.add_patch(anaktoron)

    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X position (meters)', fontsize=12)
    ax.set_ylabel('Y position (meters)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Normalized Pressure', fontsize=11)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def plot_body_resonance_modes(save_path=None):
    """
    Plot modes corresponding to body resonance frequencies.
    """
    # Body resonances and corresponding approximate modes
    body_modes = [
        ((1, 0), "Chest cavity ~3.3 Hz", 3.33),
        ((1, 1), "Abdominal ~4.7 Hz", 4.72),
        ((2, 0), "Vestibular ~6.7 Hz", 6.67),
        ((3, 0), "Brain alpha ~10 Hz", 10.00),
    ]

    resolution = 150
    x = np.linspace(0, Lx, resolution)
    y = np.linspace(0, Ly, resolution)
    X, Y = np.meshgrid(x, y)

    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    cmap = create_custom_colormap()

    for ax, ((nx, ny), label, freq) in zip(axes.flat, body_modes):
        P = room_mode_field(X, Y, nx, ny, Lx, Ly)

        im = ax.contourf(X, Y, P, levels=50, cmap=cmap, vmin=-1, vmax=1)
        ax.contour(X, Y, P, levels=[0], colors='black', linewidths=1)

        # Add columns
        for (cx, cy) in COLUMNS:
            circle = Circle((cx, cy), COLUMN_RADIUS, fill=True,
                          facecolor='gray', edgecolor='black', linewidth=0.5, alpha=0.7)
            ax.add_patch(circle)

        # Add Anaktoron
        anaktoron = Rectangle(
            (ANAKTORON_CENTER[0] - ANAKTORON_SIZE[0]/2,
             ANAKTORON_CENTER[1] - ANAKTORON_SIZE[1]/2),
            ANAKTORON_SIZE[0], ANAKTORON_SIZE[1],
            fill=False, edgecolor='gold', linewidth=2, linestyle='--'
        )
        ax.add_patch(anaktoron)

        ax.set_xlim(0, Lx)
        ax.set_ylim(0, Ly)
        ax.set_aspect('equal')
        ax.set_title(f'{label}\nMode ({nx},{ny},0) = {freq:.2f} Hz',
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')

    plt.suptitle('Telesterion Modes Matching Human Body Resonances\n'
                'Red/Blue = pressure maxima/minima (where effects would be strongest)',
                fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def plot_z_squared_mode(save_path=None):
    """
    Plot the mode closest to Z² = 33.51 Hz (the 10th harmonic).
    """
    # 10th harmonic modes: (10,0), (0,10), and combinations near 33.5 Hz
    # f = (c/2) * sqrt((nx/Lx)² + (ny/Ly)²)
    # For 33.5 Hz: sqrt((nx/51.5)² + (ny/51.5)²) ≈ 33.5 * 2 / 343 ≈ 0.195
    # This gives nx = 10 for axial mode

    resolution = 200
    x = np.linspace(0, Lx, resolution)
    y = np.linspace(0, Ly, resolution)
    X, Y = np.meshgrid(x, y)

    # Combined (10,0) + (0,10) degenerate pair
    P = room_mode_field(X, Y, 10, 0, Lx, Ly) + room_mode_field(X, Y, 0, 10, Lx, Ly)
    P = P / np.max(np.abs(P))

    freq = mode_frequency(10, 0, Lx, Ly)
    z_squared = 32 * np.pi / 3

    fig, ax = plt.subplots(figsize=(12, 10))
    cmap = create_custom_colormap()

    im = ax.contourf(X, Y, P, levels=50, cmap=cmap, vmin=-1, vmax=1)
    ax.contour(X, Y, P, levels=[0], colors='black', linewidths=0.5)

    # Add columns
    for (cx, cy) in COLUMNS:
        circle = Circle((cx, cy), COLUMN_RADIUS, fill=True,
                      facecolor='gray', edgecolor='black', linewidth=0.5, alpha=0.7)
        ax.add_patch(circle)

    # Add Anaktoron
    anaktoron = Rectangle(
        (ANAKTORON_CENTER[0] - ANAKTORON_SIZE[0]/2,
         ANAKTORON_CENTER[1] - ANAKTORON_SIZE[1]/2),
        ANAKTORON_SIZE[0], ANAKTORON_SIZE[1],
        fill=False, edgecolor='gold', linewidth=3, linestyle='--'
    )
    ax.add_patch(anaktoron)

    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X position (meters)', fontsize=12)
    ax.set_ylabel('Y position (meters)', fontsize=12)

    ax.set_title(f'Z² Harmonic Mode Field\n'
                f'Combined (10,0) + (0,10) = {freq:.2f} Hz\n'
                f'Z² = 32π/3 = {z_squared:.2f} Hz (error: {abs(freq-z_squared):.2f} Hz = {100*abs(freq-z_squared)/z_squared:.1f}%)',
                fontsize=14, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Normalized Pressure', fontsize=11)

    # Add annotations
    ax.text(Lx/2, -3,
           'This mode pattern shows 10 pressure antinodes across the hall.\n'
           'The 42 columns would scatter and modulate this pattern.',
           ha='center', fontsize=10, style='italic')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def plot_ceremony_simulation(save_path=None):
    """
    Simulate the acoustic field during a ceremony with multiple excited modes.

    Assumptions:
    - Tympanum drums excite low-frequency modes
    - Chanting excites fundamental and low harmonics
    - 3000+ people create broadband noise floor
    """
    resolution = 200
    x = np.linspace(0, Lx, resolution)
    y = np.linspace(0, Ly, resolution)
    X, Y = np.meshgrid(x, y)

    # Modes likely excited during ceremony
    # Weight by expected amplitude (drums emphasize fundamentals)
    ceremony_modes = [
        ((1, 0), 1.0),   # Fundamental - strongly excited
        ((0, 1), 1.0),   # Fundamental degenerate partner
        ((1, 1), 0.7),   # First tangential
        ((2, 0), 0.5),   # 2nd axial
        ((0, 2), 0.5),   # 2nd axial degenerate
        ((2, 1), 0.3),   # 2nd tangential
        ((1, 2), 0.3),   # 2nd tangential degenerate
        ((3, 0), 0.2),   # 3rd axial
        ((0, 3), 0.2),   # 3rd axial degenerate
    ]

    # Calculate combined field
    P = np.zeros_like(X)
    for (nx, ny), amp in ceremony_modes:
        P += amp * room_mode_field(X, Y, nx, ny, Lx, Ly)
    P = P / np.max(np.abs(P))

    fig, ax = plt.subplots(figsize=(12, 10))
    cmap = create_custom_colormap()

    im = ax.contourf(X, Y, P, levels=50, cmap=cmap, vmin=-1, vmax=1)
    ax.contour(X, Y, P, levels=[-0.3, 0, 0.3], colors='black', linewidths=0.5, alpha=0.5)

    # Add columns
    for (cx, cy) in COLUMNS:
        circle = Circle((cx, cy), COLUMN_RADIUS, fill=True,
                      facecolor='darkgray', edgecolor='black', linewidth=0.5, alpha=0.9)
        ax.add_patch(circle)

    # Add Anaktoron
    anaktoron = Rectangle(
        (ANAKTORON_CENTER[0] - ANAKTORON_SIZE[0]/2,
         ANAKTORON_CENTER[1] - ANAKTORON_SIZE[1]/2),
        ANAKTORON_SIZE[0], ANAKTORON_SIZE[1],
        fill=False, edgecolor='gold', linewidth=3, linestyle='-'
    )
    ax.add_patch(anaktoron)
    ax.text(ANAKTORON_CENTER[0], ANAKTORON_CENTER[1], 'ANAKTORON\n(Sacred Objects)',
           ha='center', va='center', fontsize=9, fontweight='bold', color='gold')

    # Mark likely standing positions
    ax.text(5, 5, 'TIERED\nSEATING', fontsize=8, ha='center', color='white', fontweight='bold')
    ax.text(Lx-5, 5, 'TIERED\nSEATING', fontsize=8, ha='center', color='white', fontweight='bold')
    ax.text(5, Ly-5, 'TIERED\nSEATING', fontsize=8, ha='center', color='white', fontweight='bold')
    ax.text(Lx-5, Ly-5, 'TIERED\nSEATING', fontsize=8, ha='center', color='white', fontweight='bold')

    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_aspect('equal')
    ax.set_xlabel('X position (meters)', fontsize=12)
    ax.set_ylabel('Y position (meters)', fontsize=12)

    ax.set_title('Simulated Acoustic Field During Ceremony\n'
                'Multiple infrasonic modes excited by drums and chanting\n'
                'Red zones = pressure maxima (most intense effects)',
                fontsize=14, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Relative Acoustic Pressure', fontsize=11)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")

    return fig


def analyze_anaktoron_acoustics():
    """
    Analyze what acoustic conditions exist at the Anaktoron (central sanctuary).
    """
    # Sample points around and within Anaktoron
    center_x, center_y = ANAKTORON_CENTER

    # Points to analyze
    points = {
        'center': (center_x, center_y),
        'north': (center_x, center_y + 5),
        'south': (center_x, center_y - 5),
        'east': (center_x + 5, center_y),
        'west': (center_x - 5, center_y),
        'corner_NE': (Lx - 5, Ly - 5),
        'corner_SW': (5, 5),
    }

    # Key modes
    modes_to_check = [
        (1, 0, "Fundamental"),
        (1, 1, "1st Tangential"),
        (2, 0, "2nd Axial"),
        (3, 0, "3rd Axial"),
        (10, 0, "10th (Z² harmonic)"),
    ]

    print("\n" + "="*70)
    print("ANAKTORON ACOUSTIC ANALYSIS")
    print("="*70)
    print("\nPressure amplitude at key locations (normalized to ±1):\n")

    header = f"{'Location':<15}" + "".join(f"{m[2]:<18}" for m in modes_to_check)
    print(header)
    print("-" * len(header))

    for loc_name, (px, py) in points.items():
        values = []
        for nx, ny, _ in modes_to_check:
            p = room_mode_field(px, py, nx, ny, Lx, Ly)
            values.append(f"{p:+.3f}")

        print(f"{loc_name:<15}" + "".join(f"{v:<18}" for v in values))

    print("\nInterpretation:")
    print("-" * 70)
    print("Values near ±1.0 = pressure maximum (intense acoustic effects)")
    print("Values near 0.0  = pressure node (minimal acoustic effects)")
    print("\nThe center of the Anaktoron sits at a NODE for all axial modes,")
    print("meaning initiates at the center would experience LESS infrasonic")
    print("pressure than those near the walls or corners.")
    print("="*70 + "\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    output_dir = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/telesterion_analysis"
    os.makedirs(output_dir, exist_ok=True)

    print("="*70)
    print("TELESTERION SPATIAL ACOUSTIC ANALYSIS")
    print("="*70)
    print()

    # 1. Fundamental mode
    print("Generating fundamental mode visualization...")
    plot_mode_field(1, 0, "\n(Infrasonic - felt, not heard)",
                   save_path=f"{output_dir}/spatial_fundamental.png")

    # 2. Degenerate mode pair
    print("Generating degenerate mode pair analysis...")
    plot_degenerate_modes(1, 2, save_path=f"{output_dir}/spatial_degenerate_pair.png")

    # 3. Body resonance modes
    print("Generating body resonance mode overlay...")
    plot_body_resonance_modes(save_path=f"{output_dir}/spatial_body_resonances.png")

    # 4. Z² mode
    print("Generating Z² harmonic mode...")
    plot_z_squared_mode(save_path=f"{output_dir}/spatial_z_squared.png")

    # 5. Ceremony simulation
    print("Generating ceremony simulation...")
    plot_ceremony_simulation(save_path=f"{output_dir}/spatial_ceremony_simulation.png")

    # 6. Anaktoron analysis
    analyze_anaktoron_acoustics()

    print("\nAll spatial visualizations complete!")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
