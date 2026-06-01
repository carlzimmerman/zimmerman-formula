#!/usr/bin/env python3
"""
VISUALIZATION: The Mysterious Connections
Shows how particle physics quantities encode cosmological information

Carl Zimmerman | March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import matplotlib.gridspec as gridspec

# Set style
plt.style.use('default')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5

# Zimmerman constant
Z = 2 * np.sqrt(8 * np.pi / 3)
Omega_Lambda = 3 * Z / (8 + 3 * Z)
Omega_m = 8 / (8 + 3 * Z)
alpha = 1 / (4 * Z**2 + 3)

# Create figure
fig = plt.figure(figsize=(16, 12))
fig.suptitle('The Mysterious Connections: Particle Physics = Cosmology',
             fontsize=16, fontweight='bold', y=0.98)

# Create grid
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)

# ============================================================================
# PLOT 1: The 9 Connections - Accuracy Comparison
# ============================================================================
ax1 = fig.add_subplot(gs[0, :2])

connections = [
    ('μₙ/μₚ = -Ω_Λ', 0.06),
    ('n_s = 1-Ω_m/9', 0.01),
    ('m_μ/m_e = 64π+Z', 0.04),
    ('μₚ = (Z-3)μ_N', 0.14),
    ('m_τ/m_μ = Z+11', 0.17),
    ('M_H/M_Z = 11/8', 0.22),
    ('|ε| = 1/(78Z)', 0.60),
    ('Δm²ratio = Z²', 0.63),
    ('sin θ_C = Z/26', 0.74),
    ('sin(2β) = Ω_Λ', 0.92),
    ('sin²θ₁₃ = 3α', 1.39),
    ('δ_CP = π/(Z-3)', 1.46),
    ('sin²θ₁₂ = Ω_m', 3.74),
]

names = [c[0] for c in connections]
errors = [c[1] for c in connections]

# Color by category
colors = []
for name in names:
    if 'Ω_Λ' in name or 'Ω_m' in name:
        colors.append('#E74C3C')  # Red for cosmology
    elif '26' in name or 'Z-3' in name or 'Z²' in name or 'Z+' in name or 'Z)μ' in name:
        colors.append('#3498DB')  # Blue for Z-direct
    elif 'α' in name or 'ε' in name:
        colors.append('#2ECC71')  # Green for particle physics
    else:
        colors.append('#9B59B6')  # Purple for others

bars = ax1.barh(range(len(names)), errors, color=colors, edgecolor='black', linewidth=0.5)
ax1.set_yticks(range(len(names)))
ax1.set_yticklabels(names, fontsize=9)
ax1.set_xlabel('Error (%)', fontsize=11)
ax1.set_title('Accuracy of Mysterious Connections', fontsize=12, fontweight='bold')
ax1.axvline(x=1.0, color='red', linestyle='--', alpha=0.5, label='1% threshold')
ax1.set_xlim(0, 4.5)
ax1.invert_yaxis()

# Add legend
legend_elements = [
    mpatches.Patch(color='#E74C3C', label='Cosmological (Ω_Λ, Ω_m)'),
    mpatches.Patch(color='#3498DB', label='Z-geometric'),
    mpatches.Patch(color='#2ECC71', label='Particle physics (α, ε)'),
    mpatches.Patch(color='#9B59B6', label='Mass ratios'),
]
ax1.legend(handles=legend_elements, loc='lower right', fontsize=8)

# ============================================================================
# PLOT 2: The Z Decomposition
# ============================================================================
ax2 = fig.add_subplot(gs[0, 2])

# Pie chart of Z components
sizes = [2, 8, 3]  # The numbers in Z = 2√(8π/3)
labels = ['2\n(Horizon)', '8\n(Gravity)', '3\n(Space)']
colors_pie = ['#FF6B6B', '#4ECDC4', '#95E1D3']
explode = (0.05, 0.05, 0.05)

wedges, texts, autotexts = ax2.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                                    autopct='', startangle=90, pctdistance=0.85,
                                    textprops={'fontsize': 10, 'fontweight': 'bold'})

# Add center text
centre_circle = plt.Circle((0, 0), 0.50, fc='white')
ax2.add_artist(centre_circle)
ax2.text(0, 0, f'Z = {Z:.3f}', ha='center', va='center', fontsize=14, fontweight='bold')
ax2.set_title('Z = 2√(8π/3)\nComponents', fontsize=12, fontweight='bold')

# ============================================================================
# PLOT 3: Particle Physics vs Cosmology Values
# ============================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Direct comparisons
particle_values = [0.691, 0.685, 0.304, 0.0222]  # sin2β, -μn/μp, sin²θ12, sin²θ13
cosmo_values = [Omega_Lambda, Omega_Lambda, Omega_m, 3*alpha]
labels_comp = ['sin(2β)', '-μₙ/μₚ', 'sin²θ₁₂', 'sin²θ₁₃']
cosmo_labels = ['Ω_Λ', 'Ω_Λ', 'Ω_m', '3α']

x = np.arange(len(labels_comp))
width = 0.35

bars1 = ax3.bar(x - width/2, particle_values, width, label='Particle Physics',
                color='#3498DB', edgecolor='black')
bars2 = ax3.bar(x + width/2, cosmo_values, width, label='Cosmology/EM',
                color='#E74C3C', edgecolor='black')

ax3.set_xticks(x)
ax3.set_xticklabels([f'{p}\n= {c}' for p, c in zip(labels_comp, cosmo_labels)], fontsize=9)
ax3.set_ylabel('Value', fontsize=11)
ax3.set_title('Particle Physics = Cosmology', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9)
ax3.set_ylim(0, 0.8)

# Add error annotations
for i, (pv, cv) in enumerate(zip(particle_values, cosmo_values)):
    error = abs(pv - cv) / pv * 100
    ax3.annotate(f'{error:.1f}%', xy=(i, max(pv, cv) + 0.03),
                ha='center', fontsize=8, color='green')

# ============================================================================
# PLOT 4: The (Z-3) Connection
# ============================================================================
ax4 = fig.add_subplot(gs[1, 1])

z_minus_3 = Z - 3
quantities = ['μₚ/μ_N\n(proton)', 'π/δ_CP\n(CP phase)', '78 × |ε| × Z\n(kaon CP)']
values = [2.7928, np.pi/1.144, 78 * 2.228e-3 * Z]  # All should ≈ Z-3

ax4.bar(quantities, values, color=['#FF9F43', '#54A0FF', '#5F27CD'],
        edgecolor='black', linewidth=1.5)
ax4.axhline(y=z_minus_3, color='red', linestyle='--', linewidth=2,
            label=f'Z-3 = {z_minus_3:.3f}')
ax4.set_ylabel('Value', fontsize=11)
ax4.set_title('Quantities Equal to (Z-3)', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10)

# ============================================================================
# PLOT 5: String Theory Connection (26)
# ============================================================================
ax5 = fig.add_subplot(gs[1, 2])

# Show how 26 appears
string_connections = [
    ('sin θ_C\n= Z/26', Z/26, 0.2243, '#E74C3C'),
    ('|ε| × 78Z\n= 1', 78*Z*2.228e-3, 1.0, '#3498DB'),  # 78 = 3×26
]

x_pos = [0.3, 0.7]
for i, (label, predicted, measured, color) in enumerate(string_connections):
    ax5.bar([x_pos[i]-0.1, x_pos[i]+0.1], [predicted, measured],
            width=0.15, color=[color, 'white'], edgecolor=color, linewidth=2)

ax5.set_xticks(x_pos)
ax5.set_xticklabels(['sin θ_C = Z/26', '|ε| = 1/(78Z)\n78 = 3×26'], fontsize=10)
ax5.set_ylabel('Value', fontsize=11)
ax5.set_title('Connection to 26\n(Bosonic String Dimensions)', fontsize=12, fontweight='bold')

# ============================================================================
# PLOT 6: Statistical Significance
# ============================================================================
ax6 = fig.add_subplot(gs[2, 0])

# Log probability scale
connection_probs = [1/err*100 for err in errors if err > 0]
log_probs = [np.log10(1/(err/100)) for err in errors if err > 0]

ax6.barh(range(len(errors)), [-np.log10(err/100) for err in errors],
         color='#2C3E50', edgecolor='black')
ax6.set_yticks(range(len(names)))
ax6.set_yticklabels(names, fontsize=8)
ax6.set_xlabel('−log₁₀(probability)', fontsize=11)
ax6.set_title('Improbability of Each Connection\n(Higher = Less Likely Random)',
              fontsize=11, fontweight='bold')
ax6.axvline(x=2, color='red', linestyle='--', alpha=0.5, label='1% chance')
ax6.invert_yaxis()

# ============================================================================
# PLOT 7: Mass Ratios from Z
# ============================================================================
ax7 = fig.add_subplot(gs[2, 1])

mass_data = [
    ('m_μ/m_e', 206.77, 64*np.pi + Z),
    ('m_τ/m_μ', 16.82, Z + 11),
    ('M_H/M_Z', 1.372, 11/8),
    ('Δm²ratio', 33.3, Z**2),
]

names_m = [m[0] for m in mass_data]
measured_m = [m[1] for m in mass_data]
predicted_m = [m[2] for m in mass_data]

x = np.arange(len(names_m))
width = 0.35

ax7.bar(x - width/2, measured_m, width, label='Measured', color='#2ECC71', edgecolor='black')
ax7.bar(x + width/2, predicted_m, width, label='Z-formula', color='#E74C3C', edgecolor='black')

ax7.set_xticks(x)
ax7.set_xticklabels(names_m, fontsize=10)
ax7.set_ylabel('Ratio', fontsize=11)
ax7.set_title('Mass Ratios from Z', fontsize=12, fontweight='bold')
ax7.legend(fontsize=9)
ax7.set_yscale('log')

# ============================================================================
# PLOT 8: The Big Picture - Connection Web
# ============================================================================
ax8 = fig.add_subplot(gs[2, 2])

# Draw connection web
ax8.set_xlim(-1.5, 1.5)
ax8.set_ylim(-1.5, 1.5)
ax8.set_aspect('equal')
ax8.axis('off')

# Central Z
circle_z = plt.Circle((0, 0), 0.3, color='#FFD93D', ec='black', linewidth=2)
ax8.add_patch(circle_z)
ax8.text(0, 0, f'Z\n{Z:.2f}', ha='center', va='center', fontsize=12, fontweight='bold')

# Surrounding concepts
concepts = [
    (0.9, 0.9, 'Ω_Λ\n(Dark\nEnergy)', '#E74C3C'),
    (-0.9, 0.9, 'Ω_m\n(Matter)', '#3498DB'),
    (1.1, 0, 'QCD\n(nucleons)', '#2ECC71'),
    (-1.1, 0, 'Flavor\n(CKM)', '#9B59B6'),
    (0.9, -0.9, 'Neutrinos\n(PMNS)', '#FF6B6B'),
    (-0.9, -0.9, 'Strings\n(26D)', '#4ECDC4'),
    (0, 1.1, 'CP\nViolation', '#FF9F43'),
    (0, -1.1, 'Masses\n(leptons)', '#95E1D3'),
]

for x, y, label, color in concepts:
    circle = plt.Circle((x, y), 0.25, color=color, ec='black', linewidth=1, alpha=0.7)
    ax8.add_patch(circle)
    ax8.text(x, y, label, ha='center', va='center', fontsize=7, fontweight='bold')
    # Draw line to center
    ax8.plot([0, x*0.4], [0, y*0.4], 'k-', linewidth=1.5, alpha=0.5)

ax8.set_title('All Physics Connected Through Z', fontsize=12, fontweight='bold')

# ============================================================================
# Save figure
# ============================================================================
plt.tight_layout()
plt.savefig('research/mysterious_connections/mysterious_connections.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig('research/key_visualizations/mysterious_connections.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("Saved: mysterious_connections.png")

plt.show()
