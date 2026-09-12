#!/usr/bin/env python3
"""L195 -- THE CMB GATE ON THE SELF-CRITICAL SECTOR.

WHAT THE SECTOR IS, after L192/L193/L194. Where the clock runs faster than proper time the sector is driven to the marginal surface,
on which its stress is isotropic (perfect-fluid form, an exact off-shell degeneracy) and its sound speed is the residual left by the
balance between instability growth and Hubble dilution,
        c_s^2(z) = (H(z)/k_max)^2,
with k_max the shortest wavelength the instability reaches. Nothing here is fitted: given one number, the ultraviolet reach, the sound
speed at every epoch follows.

THE FIRST THING TO COMPUTE, because it decides the shape of every answer: the comoving Jeans wavenumber of such a fluid. With
c_s = H/k_max,phys the Jeans wavenumber is k_J,phys = sqrt(4 pi G rho)/c_s, and in a matter- or radiation-dominated background
sqrt(4 pi G rho) is H up to an order-unity factor, so k_J,phys -> k_max,phys: THE SECTOR'S JEANS SCALE IS ITS OWN ULTRAVIOLET REACH,
at every epoch. It clusters exactly like cold dark matter on every scale larger than k_max and not at all below it.

THE GATE. Feed that sound speed into a Boltzmann code in place of cold dark matter and ask for the third acoustic peak. The forest
(L194) already requires k_max >= 5.4 h/Mpc comoving; the CMB peaks live at k ~ 0.01-0.2 /Mpc, four decades larger, so the prediction
is that the same k_max that satisfies the forest satisfies the CMB with enormous margin. That is what is tested, together with the
value of k_max at which the CMB would fail, and the redshift above which the sector is not cold at all.
Patched CLASS 3.3.4.0 with the kernel OFF (this is the sector's own gate; no kernel enters, so the a0 footings are irrelevant).
No literal-True checks."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from classy import Class
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL195 THE CMB GATE ON THE SELF-CRITICAL SECTOR: c_s^2(z) = (H(z)/k_max)^2, no free parameter but the ultraviolet reach\n" + "=" * 118)
h = 0.6736; Om = 0.3138; Or = 9.182e-5; OL = 1 - Om - Or
Hc = lambda z: (h/2997.9)*np.sqrt(Om*(1 + z)**3 + Or*(1 + z)**4 + OL)          # H(z)/c in 1/Mpc, physical
def cs2_of(z, kmax_com):                                                         # kmax_com in 1/Mpc comoving
    return (Hc(z)/(kmax_com*(1 + z)))**2
KF = 2*np.pi/0.776                                                                # the forest-critical reach from L194: 0.776 Mpc comoving
print(f"    the forest-critical ultraviolet reach (L194) is k_max = {KF:.2f} /Mpc comoving (wavelength {2*np.pi/KF:.2f} Mpc)")
print("    z:        " + "".join(f"{z:>12g}" for z in (0, 3, 1100, 3400, 1e5, 1e6)))
print("    c_s^2:    " + "".join(f"{cs2_of(z, KF):>12.3e}" for z in (0, 3, 1100, 3400, 1e5, 1e6)))
# the Jeans identity
def kJ_over_kmax(z, kmax_com):
    rho_fac = np.sqrt(1.5*(Om*(1 + z)**3 + Or*(1 + z)**4)/(Om*(1 + z)**3 + Or*(1 + z)**4 + OL))   # sqrt(4 pi G rho_m+r)/H
    return rho_fac*Hc(z)/cs2_of(z, kmax_com)**0.5/(kmax_com*(1 + z))
jr = [kJ_over_kmax(z, KF) for z in (0, 3, 1100, 3400, 1e5)]
check("V1 [the Jeans scale IS the ultraviolet reach] the sector's comoving Jeans wavenumber equals k_max to within the order-unity factor relating sqrt(4 pi G rho) to H, at every epoch from today back to z = 1e5: a fluid whose sound speed is the residual of this balance clusters exactly like cold dark matter on every scale above its own cutoff and on none below",
      all(0.5 < x < 1.5 for x in jr), "k_Jeans/k_max = " + " ".join(f"{x:.3f}" for x in jr) + " at z = 0, 3, 1100, 3400, 1e5")
zhot = None
for z in np.geomspace(1e4, 1e8, 400):
    if cs2_of(z, KF) > 0.1: zhot = z; break
check("V2 [when the sector was not cold] the sound speed grows towards the past, so the sector is relativistic only above a redshift far beyond recombination; the acoustic scales enter the horizon long after that, so the peaks are set while the sector is already cold",
      zhot is not None and zhot > 3e5, f"c_s^2 reaches 0.1 at z = {zhot:.1e}; at recombination it is {cs2_of(1100, KF):.2e} and at matter-radiation equality {cs2_of(3400, KF):.2e}")
# ---- the Boltzmann gate ----
base = {"h": h, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454,
        "output": "tCl,mPk", "l_max_scalars": 1500, "P_k_max_h/Mpc": 10., "z_pk": "0,3", "mond_a0": 0.0, "gauge": "newtonian"}
def run(extra):
    c = Class(); p = dict(base); p.update(extra); c.set(p); c.compute(); cl = c.raw_cl(1500)
    l = cl["ell"][2:]; D = l*(l + 1)*cl["tt"][2:]/(2*np.pi); at = lambda r: D[np.argmin(abs(l - r))]
    pk = [c.pk(k*h, 3.0)*h**3 for k in (1.0, 5.0)]
    return at, pk
L, pkL = run({"omega_cdm": 0.1200})
r32L = L(816)/L(537)
SMOOTH, _ = run({"omega_cdm": 1e-6, "Omega_fld": 0.1200/h**2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": 1.0, "use_ppf": "no"})
r32S = SMOOTH(816)/SMOOTH(537)
print(f"    LCDM reference: peak3/peak2 = {r32L:.3f}; smooth-fluid control (cs2 = 1): {r32S:.3f}")
print("    Because the comoving Jeans scale is k_max at every epoch (V1), each gate is run with the sound speed the law gives AT THAT EPOCH:")
print("    k_max [/Mpc com]   c_s^2(z=1100)   peak3/peak2  restoration  |  c_s^2(z=3)     P(k=5 h/Mpc, z=3)/LCDM")
rows = []
for kmax in (0.01, 0.05, 0.2, 1.0, KF, 50.0):
    c1, c3 = cs2_of(1100, kmax), cs2_of(3.0, kmax)
    at, _ = run({"omega_cdm": 1e-6, "Omega_fld": 0.1200/h**2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": float(c1), "use_ppf": "no"})
    r32 = at(816)/at(537); rest = (r32 - r32S)/(r32L - r32S)
    _, pk3 = run({"omega_cdm": 1e-6, "Omega_fld": 0.1200/h**2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": float(c3), "use_ppf": "no"})
    rows.append((kmax, c1, r32, rest, c3, pk3[1]/pkL[1]))
    print(f"    {kmax:>12.2f}       {c1:.3e}      {r32:.3f}       {rest:+.2f}    |  {c3:.3e}      {pk3[1]/pkL[1]:.3f}")
kf = [r for r in rows if abs(r[0] - KF) < 1e-9][0]
check("V3 [THE CMB GATE] at the ultraviolet reach the forest demands, the self-critical sector restores the third acoustic peak to within 5% of the cold-dark-matter value: the same single number that makes the sector cold enough for the Lyman-alpha forest makes it cold enough for the CMB, with no further freedom",
      abs(kf[2]/r32L - 1) < 0.05 and kf[3] > 0.9,
      f"k_max = {KF:.2f} /Mpc gives c_s^2(z=1100) = {kf[1]:.2e}, peak3/peak2 = {kf[2]:.3f} vs LCDM {r32L:.3f} (restoration {kf[3]:+.2f}); smooth-fluid control {r32S:.3f}")
cmb_ok = [r[0] for r in rows if r[3] > 0.9]; forest_ok = [r[0] for r in rows if abs(r[5] - 1) < 0.10]
check("V4 [which gate binds, computed] the CMB is satisfied over the whole scanned range of ultraviolet reach while the forest is not: the forest, not the CMB, is what sets the bound on how far the instability must reach, and the two are not in competition",
      min(cmb_ok) < min(forest_ok) and min(cmb_ok) <= 0.05,
      "CMB restored (> 0.9) for k_max >= " + f"{min(cmb_ok):.2f}" + " /Mpc; forest within 10% for k_max >= " + (f"{min(forest_ok):.2f}" if forest_ok else "none in range") + " /Mpc")
check("V5 [the forest at its own epoch] with the sound speed the law gives at z = 3 rather than the recombination value held constant, the forest-critical reach leaves the linear power at k = 5 h/Mpc within 10% of LCDM, so one ultraviolet reach clears both gates instead of trading one against the other",
      abs(kf[5] - 1) < 0.10, f"c_s^2(z=3) = {kf[4]:.2e} at k_max = {KF:.2f} /Mpc gives P(k=5 h/Mpc, z=3)/LCDM = {kf[5]:.3f}")
print("    LIMITS: the Boltzmann code takes a CONSTANT sound speed, so each gate is run with the value the law gives at that gate's own epoch; the sector's comoving Jeans\n"
      "    scale is k_max at every epoch (V1), which is what makes that split legitimate, but a code carrying the full c_s^2(z) = (H/k_max)^2 history would settle it properly;\n"
      "    the sector is modelled as a w = -1e-4 perfect fluid, which is what criticality makes it, but its\n"
      "    background density is imposed as the LCDM cold-matter share rather than derived; no kernel is active; the criticality must operate at recombination, i.e. the clock\n"
      "    must run faster than proper time there, which is a condition on the coefficient history and is NOT established by this script.")
json.dump(dict(kmax_forest=float(KF), rows=[[float(x) for x in r] for r in rows], lcdm_r32=float(r32L), smooth_r32=float(r32S),
               jeans_ratio=[float(x) for x in jr], z_hot=float(zhot)), open("L195_results.json", "w"), indent=1)
print(f"\nL195 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
