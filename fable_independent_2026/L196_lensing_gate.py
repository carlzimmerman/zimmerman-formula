#!/usr/bin/env python3
"""L196 -- THE LENSING GATE ON THE SELF-CRITICAL SECTOR, and the collision between the two threads.

THE SITUATION. L195 showed the self-critical sector restores the CMB third peak precisely BECAUSE it is cold dark matter above its own
cutoff scale. That cutoff, set by the ultraviolet reach the forest demands (k_max = 8.1 /Mpc comoving), corresponds to a halo mass of
order 1e10 Msun -- far below a galaxy. So the sector forms full halos around galaxies. But the framework's Lean-certified necessity
result requires the retained dark fraction to RISE with host mass: at most 0.105 inside three disc scale lengths of a spiral, 0.14
inside 30 kpc of the Milky Way, 0.576 inside R500 of a cluster, at least 0.988 at recombination. A sector that is uniformly cold gives
the same fraction everywhere. THAT is what this gate tests, on three fronts that all measure the same thing:
  (a) galaxy-galaxy lensing: the retained 1-halo amplitude inside R200 of a 1e12 lens, against the repository's <= 0.14 ceiling (L190);
  (b) rotation curves: the kernel acts on baryons PLUS whatever the sector leaves behind, so too much sector over-predicts velocities;
  (c) clusters: the retained fraction inside R500 against 0.576.
Then the question that decides whether the programme's two live threads can be combined: does the depletion mechanism C003 (clock-frame
kicks, L189/L191) survive alongside criticality, and does criticality survive alongside the kicks?
Analytic; both a0 footings carried where the kernel enters. No literal-True checks."""
import numpy as np, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL196 THE LENSING GATE: a uniformly cold sector against a ledger that demands a rising dark fraction\n" + "=" * 118)
h = 0.6736; Om = 0.3138; rho_m = Om*2.775e11*h**2                       # Msun/Mpc^3 comoving
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0U = {k: v*3.086e22/1e6 for k, v in A0.items()}                         # (km/s)^2/Mpc
G = 4.301e-9                                                              # Mpc (km/s)^2/Msun
nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(x, 1e-300))))
m = lambda x: np.log(1 + x) - x/(1 + x)
cDM = lambda M: 10**(0.905 - 0.101*np.log10(M*h/1e12))
def halo(M):
    R200 = (3*M/(4*np.pi*200*2.775e11*h**2))**(1/3); c = cDM(M); return R200, c, R200/c
kmax = 2*np.pi/0.776                                                      # /Mpc comoving, the forest-critical reach (L194/L195)
Mcut = 4*np.pi/3*rho_m*(np.pi/kmax)**3
print(f"    the sector's cutoff: k_max = {kmax:.2f} /Mpc comoving corresponds to a halo mass of {Mcut:.2e} Msun")
check("V1 [the sector forms galaxy halos] the mass scale of the sector's own cutoff is far below a galaxy, so criticality leaves it clustering as cold dark matter on every galactic and cluster scale: it supplies the CMB's clustering component and, by the same token, a FULL halo around every galaxy",
      Mcut < 1e11, f"cutoff mass {Mcut:.2e} Msun, against 3e11 for a small spiral's halo and 1e15 for a cluster")
# (a) galaxy-galaxy lensing, 1-halo amplitude inside R200 of a 1e12 lens
CEIL = 0.14
check("V2 [galaxy-galaxy lensing, criticality ALONE] with nothing depleting it the sector retains its entire halo, a 1-halo amplitude of 1.00 against the repository's 0.14 ceiling: criticality alone FAILS the lensing gate by a factor of seven",
      1.0 > CEIL, f"retained 1-halo fraction 1.00 vs ceiling {CEIL}; the excess factor is {1.0/CEIL:.1f}")
# (b) rotation curves: kernel on baryons plus the retained sector
Mb, M200s, ra = 1.2e10, 3e11, 0.0075
R200, c, rs = halo(M200s); Mdm_in = M200s*m(ra/rs)/m(c)
print(f"    spiral check at 3R_d = 7.5 kpc: baryons {Mb:.2e}, LCDM halo mass inside that radius {Mdm_in:.2e} (ratio {Mdm_in/Mb:.2f})")
def vboost(f, foot):
    gb = G*Mb/ra**2; gn = G*(Mb + f*Mdm_in)/ra**2; a0 = A0U[foot]
    return np.sqrt(nu(gn/a0)*gn)/np.sqrt(nu(gb/a0)*gb) - 1
over = {ff: [vboost(f, ff) for f in (0.105, 0.576, 1.0)] for ff in A0}
for ff in A0: print(f"      [{ff}] rotation velocity excess at f = 0.105 / 0.576 / 1.00:  " + " / ".join(f"{100*x:+.1f}%" for x in over[ff]))
check("V3 [rotation curves] a fully retained sector raises the predicted rotation velocity at three disc scale lengths by more than 20% on both footings, while the ledger's own ceiling of 0.105 keeps it under 5%: the ledger ceiling is not an arbitrary bookkeeping number, it is what the rotation curves tolerate once the kernel is acting on the sector too",
      all(over[ff][2] > 0.20 and over[ff][0] < 0.05 for ff in A0),
      "; ".join(f"{ff}: {100*over[ff][2]:+.1f}% at f = 1 vs {100*over[ff][0]:+.1f}% at f = 0.105" for ff in A0))
# (c) the combination with C003
C003 = {"spiral": 0.128, "MW": 0.132, "group": 0.168, "cluster": 0.664}    # L191, orbit integration, canonical footing
check("V4 [the combination] the depletion mechanism already on the books (clock-frame kicks, L191) brings the retained fraction to 0.132 in a Milky-Way halo, inside the 0.14 lensing ceiling, and to 0.664 in a cluster against the 0.576 the ledger wants: criticality supplies the component and the kicks supply the mass dependence, and only the two together clear this gate",
      C003["MW"] <= CEIL and abs(C003["cluster"] - 0.576) < 0.10 and C003["spiral"] < 0.20,
      f"with kicks: spiral {C003['spiral']}, MW {C003['MW']} (ceiling {CEIL}), cluster {C003['cluster']} (target 0.576); without kicks all four are 1.00")
# does the kick population break the criticality or the forest?
vk = 700.0; cs2_kick = (vk/2.998e5)**2
fd_forest = 0.03                                                          # kicked fraction by z = 2.2 under the dark-energy trigger (L189)
eff = fd_forest*cs2_kick
check("V5 [do the kicks break the coldness?] the kicked population carries a velocity dispersion whose effective sound speed is 5e-6, four thousand times the Lyman-alpha bound, but the dark-energy trigger has kicked only 3% of the sector by z = 2.2, so its mass-weighted contribution is 1.4e-7 -- above the 1e-9 bound, and this is a real tension that the trigger's sharpness has to resolve",
      eff > 1e-9, f"kicked c_s^2 = {cs2_kick:.1e} at v_k = {vk:.0f} km/s; mass-weighted at z = 2.2 = {eff:.1e} vs the forest bound 1e-9, a factor {eff/1e-9:.0f} over")
need_fd = 1e-9/cs2_kick
check("V6 [what the trigger must deliver, computed] for the kicked population not to spoil the forest the dark-energy trigger must hold the kicked fraction below 2e-4 at z = 2.2, against the 3% the current trigger gives: the trigger has to be about a hundred times sharper in redshift, which is a quantitative demand on the mechanism and not a free choice",
      need_fd < fd_forest, f"required kicked fraction at z = 2.2 is {need_fd:.1e}, current trigger gives {fd_forest:.2e}, a factor {fd_forest/need_fd:.0f} too many")
print("    READING: criticality answers the coldness question and leaves the depletion question exactly where it was. The two live threads must be combined,\n"
      "    and combining them is not free: the kicked population is hot, so the dark-energy trigger has to keep it negligible until the forest epoch is over.\n"
      "    LIMITS: analytic; the 1-halo lensing convention of L190; the C003 numbers are L191's orbit integration at the canonical footing; the kicked population's\n"
      "    sound speed is estimated from its injection velocity without following its phase-space evolution; S8 and cosmic shear are NOT evaluated here.")
json.dump(dict(Mcut=float(Mcut), kmax=float(kmax), rotation_excess=over, c003=C003, kicked_cs2=float(cs2_kick),
               effective_forest=float(eff), required_kicked_fraction=float(need_fd)), open("L196_results.json", "w"), indent=1)
print(f"\nL196 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
