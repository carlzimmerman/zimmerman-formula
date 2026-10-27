# The patch reservoir is not its descendant galaxy

This is a conditional ancestry check of the specified M6 scale, not a measured
formation efficiency or a new forest limit. Code, inputs and outputs are pinned
by `run/manifest.json`; eight accounting checks pass.

X22 sets M_L=(Omega_m/Omega_b) M_b,law and assigns its corresponding Lagrangian
radius. X57 and P1D1/P1D2 inherit the median R_L=0.441934777 Mpc/h rather than
an observed patch mass distribution. The median effective galaxy baryon mass
is 7.3393e9 solar masses. After compensation, that fixed patch contains much
more baryonic mass:

| Quantity | Canonical | Alternative |
|---|---:|---:|
| Initial enriched patch baryon mass, solar masses | 3.6361e10 | 4.2568e10 |
| One representative descendant's effective baryon mass / patch mass | 0.20185 | 0.17242 |
| Descendant mass inventory / cosmic baryons, at the inherited budget | 0.012235 | 0.008374 |
| Same representative inventory / census stars+cold gas | 0.2046 | 0.1401 |

The last row is an inventory ratio **if every descendant has that representative
mass**. It is not a mass-function-integrated coverage fraction. The effective
mass in X22 is inferred dynamically and is not automatically the total
stars-plus-cold-gas mass in the census. The calculation exposes the missing
ancestry/retention assumption; it does not determine that assumption from data.

If the X22 radius relation were instead applied to each galaxy on a consistent
native background, then V(M_g)=M_g/rho_b and
M_patch=(1+delta_b)M_g. For a one-patch/one-galaxy assignment this would imply
epsilon=1/(1+delta_b), and a selected mass density would require
F_patch=(1+delta_b)rho_gal,selected/rho_b. This is an exact accounting identity
for that different assignment. A numerical three-bin check verifies it.
It changes the forest template's patch-size distribution; the old single-scale
variance/flux budget cannot be carried over as a measured bound.

Fragmentation, mergers, diffuse retained gas and external baryon accretion can
change the assignment. They need explicit accounting, including the cold
component carried by accretion. They cannot be handled by counting the same
patch once for each galaxy it helps form. The general efficiency/selection
calculation in [`../population/RESULTS.md`](../population/RESULTS.md) therefore
remains the main population result.
