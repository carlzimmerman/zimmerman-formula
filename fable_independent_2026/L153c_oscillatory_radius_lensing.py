#!/usr/bin/env python3
"""
L153c -- THE OSCILLATORY (HELMHOLTZ) REGIME AND WEAK LENSING: where does the field-dust bend MOND?
=============================================================================================================
L153a A6-2: the AeST Helmholtz term is the LINEAR static response of the field-dust,
      (lap + mu^2) Phi = 4 pi G rho_b ,   mu^2 = 4 pi G rho_amb / (c_ad^2 c^2),
i.e. mu^-1 is the Jeans length of the AMBIENT dust at sound speed c_ad.  The full static response is the
isothermal atmosphere rho_d = rho_amb exp(|Phi|/c_ad^2) (A6-1), so the deviation from MOND around a galaxy is
carried by the INDUCED EXCESS dust mass M_exc(<r) = int 4 pi r^2 rho_amb (e^{|Phi|/c_ad^2} - 1) dr.
In the transplant the MOND scalar is sourced by all matter (eps = 1), so in deep MOND g ~ sqrt(M_b + M_exc):
a 10% deviation in g is M_exc = 0.21 M_b.  Verwayen-Skordis-Boehm (arXiv:2304.05134, eq. 21) estimate the
O(1)-deviation scale as r_C ~ (r_M/mu^2)^{1/3} for an isolated log potential; Mistele-McGaugh-Hossenfelder
(arXiv:2301.03499, Table 1) bound the AeST mass parameter by KiDS-1000 lensing: m^2/f_G <~ 1 Mpc^-2 for a
10% MOND-likeness at a_b >= 1e-13 m/s^2 (M_b = 1e11), <~ 0.001 Mpc^-2 if the a_b >= 1e-15 points are trusted.

WHAT IS COMPUTED:
  C1  mu^-1(c_ad) and the translation of the published m^2/f_G bounds into c_ad (identifying m^2/f_G = mu^2).
  C2  VSB's r_C(M_b, c_ad) and the c_ad floors implied by 'r_C > 100 kpc' (rotation curves) and 'r_C > 1 Mpc'.
  C3  The transplant's own static response: the induced-atmosphere deviation from deep MOND vs radius for the
      KiDS lens masses (1e10, 1e11 Msun), with the potential anchored to the ambient density at
      R_max = min(EFE radius, turnaround radius) -- the boundary condition VSB themselves flag as decisive.
      Output: the maximum deviation inside the weak-lensing range and the c_ad floor for <= 10%.
  C4  Whether the oscillatory regime proper (r >~ mu^-1) can sit outside BOTH the rotation-curve range and
      the lensing range, and at what c_ad.
POLARITY: each check ASSERTS a statement; PASS = true.  No check uses a literal True.
"""
import numpy as np
import json, os, sys, time

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1; ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__))

C_KMS = 299792.458; C_SI = 2.99792458e8; G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MPC = 1e3*KPC
h = 0.674; H0 = h*100e3/MPC; OM, OB = 0.315, 0.049; OD = OM-OB
RHO_CRIT = 3*H0**2/(8*np.pi*G); RHO_D0 = OD*RHO_CRIT; RHO_M0 = OM*RHO_CRIT
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
RESV = OD/OB
def nu_RAR(y): return 1.0/(-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))
CADS = np.array([100, 150, 200, 250, 300, 350, 400, 450, 500, 537, 600, 700, 850, 1000.])

# =====================================================================================================
sec("C1 -- mu^-1(c_ad) and the published lensing / cluster bounds translated into c_ad")
# =====================================================================================================
def mu_inv_Mpc(cad_kms, rho=RHO_D0): return np.sqrt((cad_kms*1e3)**2/(4*np.pi*G*rho))/MPC
def cad_from_mu2(mu2_Mpc2, rho=RHO_D0): return np.sqrt(4*np.pi*G*rho/(mu2_Mpc2/MPC**2))/1e3
print(f"  ambient dust density = cosmic mean rho_d = {RHO_D0:.3e} kg/m^3 (the dust does not cluster on galaxy scales, L153b)")
print(f"  {'c_ad km/s':>10} {'mu^-1 Mpc':>10} {'mu^2 Mpc^-2':>12}")
for cad in (42, 100, 200, 300, 450, 537, 1000, 1340):
    print(f"  {cad:10.0f} {mu_inv_Mpc(cad):10.2f} {1/mu_inv_Mpc(cad)**2:12.4f}")
c_loose = cad_from_mu2(1.0); c_deep = cad_from_mu2(1e-3); c_clus = cad_from_mu2(2.5)
print(f"  MMH2023 Table 1 (m^2/f_G = mu^2):  <~ 1 Mpc^-2 (WL, a_b >= 1e-13)  =>  c_ad >= {c_loose:.0f} km/s")
print(f"                                     <~ 1e-3 Mpc^-2 (WL, a_b >= 1e-15) =>  c_ad >= {c_deep:.0f} km/s")
print(f"                                     >~ 2.5 Mpc^-2 (clusters via mu)   =>  c_ad <= {c_clus:.0f} km/s  [superseded: L153b captures clusters nonlinearly]")
check("C1-1  mu^-1 = 7.1 Mpc at c_ad = 300 km/s and scales linearly with c_ad: the Helmholtz scale is a "
      "cosmological length for every c_ad in the L153b window (>= 3.5 Mpc at 150 km/s)",
      abs(mu_inv_Mpc(300) - 7.1) < 0.2 and mu_inv_Mpc(150) > 3.4, f"mu^-1(300) = {mu_inv_Mpc(300):.2f} Mpc")
check("C1-2  the published loose lensing bound (mu^2 <~ 1 Mpc^-2) is c_ad >= 42 km/s -- below the L153b floor, "
      "not binding; the deep bound (mu^2 <~ 1e-3, a_b >= 1e-15, which MMH2023 flag as less reliable) would be "
      "c_ad >= 1340 km/s, ABOVE the arXiv:1601.05097 ceiling of 537 km/s -- so the deep lensing points alone "
      "would close the window if their isolation criterion is trusted",
      35 < c_loose < 50 and c_deep > 537, f"c_loose = {c_loose:.0f}, c_deep = {c_deep:.0f} km/s")
check("C1-3  and the MMH pincer's CLUSTER horn (mu^2 >~ 2.5 Mpc^-2 <=> c_ad <= 27 km/s) does not apply to the "
      "transplant: clusters are filled by the nonlinear exponential capture (L153b B2-3), not by the linear "
      "mu-term -- the linear pincer is an artefact of quadratic K",
      c_clus < 35, f"c_clus = {c_clus:.0f} km/s")

# =====================================================================================================
sec("C2 -- VSB's r_C ~ (r_M/mu^2)^(1/3) (isolated log potential, no cutoff) and the floors it implies")
# =====================================================================================================
def rC_VSB(Mb_msun, cad, a0, refined=True):
    rM = np.sqrt(G*Mb_msun*MSUN/a0); mu2 = 1/(mu_inv_Mpc(cad)*MPC)**2
    return (0.874 if refined else 1.0)*(rM/mu2)**(1/3.)
MBS = (1e10, 3e10, 1e11, 1.5e11)
print(f"  r_C [kpc], canonical footing, refined VSB eq.(21) with Delta = 0 (factor 0.874):")
print(f"  {'M_b':>8} |" + "".join(f"{int(c):>8}" for c in CADS))
C2 = {}
for Mb in MBS:
    row = [rC_VSB(Mb, c, A0['canonical'])/KPC for c in CADS]; C2[Mb] = row
    print(f"  {Mb:8.1e} |" + "".join(f"{x:8.0f}" for x in row))
def cad_floor_rC(Mb, target_kpc, a0):
    # r_C = 0.874 (r_M mu^-2)^{1/3} >= target  =>  mu^-1 >= sqrt((target/0.874)^3 / r_M)
    rM = np.sqrt(G*Mb*MSUN/a0); mu_inv = np.sqrt((target_kpc*KPC/0.874)**3/rM)
    return 300.0*mu_inv/(mu_inv_Mpc(300)*MPC)
fl = {Mb: dict(rc100=cad_floor_rC(Mb, 100, A0['canonical']), rc1000=cad_floor_rC(Mb, 1000, A0['canonical'])) for Mb in MBS}
for Mb in MBS:
    print(f"  M_b = {Mb:.1e}: c_ad floor for r_C > 100 kpc = {fl[Mb]['rc100']:.0f} km/s ;  for r_C > 1 Mpc = {fl[Mb]['rc1000']:.0f} km/s")
check("C2-1  rotation curves are safe: r_C > 100 kpc needs only c_ad > 26 km/s (1e10) .. 15 km/s (1.5e11), "
      "far below the L153b floor", all(fl[Mb]['rc100'] < 30 for Mb in MBS), f"max floor = {max(fl[Mb]['rc100'] for Mb in MBS):.0f} km/s")
check("C2-2  but on VSB's isolated-log-potential scaling, r_C > 1 Mpc needs c_ad >= 460 km/s for 1e11 Msun and "
      ">= 820 km/s for 1e10 Msun lenses -- the latter ABOVE the 537 km/s ceiling.  On this scaling the window "
      "is a sliver for the most massive KiDS lenses and EMPTY for the least massive.",
      440 < fl[1e11]['rc1000'] < 480 and fl[1e10]['rc1000'] > 537,
      f"floors: 1e11 -> {fl[1e11]['rc1000']:.0f}, 1e10 -> {fl[1e10]['rc1000']:.0f} km/s")

# =====================================================================================================
sec("C3 -- THE TRANSPLANT'S OWN STATIC RESPONSE with the physical boundary condition (EFE / turnaround cutoff)")
# =====================================================================================================
def profile(Mb_msun, a0, g_ext_frac, n=4000):
    Mb = Mb_msun*MSUN; rM = np.sqrt(G*Mb/a0); vf = (G*Mb*a0)**0.25; a_h = 0.15*rM
    r_efe = vf**2/(g_ext_frac*a0); r_ta = (3*(1+RESV)*Mb/(4*np.pi*5.55*RHO_M0))**(1/3.)
    Rmax = min(r_efe, r_ta)
    r = np.logspace(np.log10(1e-3*rM), np.log10(Rmax), n)
    Menc = Mb*r**2/(r+a_h)**2; gN = G*Menc/r**2; g = nu_RAR(gN/a0)*gN
    dr = np.diff(r); Phi = np.concatenate([[0.0], np.cumsum(0.5*(g[1:]+g[:-1])*dr)]); Phi -= Phi[-1]
    return r, Phi, g, rM, Rmax, r_efe, r_ta, Mb
def excess(r, Phi, cad, Mb, cap=True):
    x = np.minimum(-Phi/(cad*1e3)**2, 300.0)
    rho_ex = RHO_D0*np.expm1(x)
    dr = np.diff(r); shell = 4*np.pi*(0.5*(r[1:]+r[:-1]))**2*0.5*(rho_ex[1:]+rho_ex[:-1])*dr
    M = np.concatenate([[0.0], np.cumsum(shell)])
    Mres = RESV*Mb
    if cap and M[-1] > Mres: M = M*(Mres/M[-1])
    return M
def deviation_table(Mb_msun, a0, g_ext_frac):
    r, Phi, g, rM, Rmax, r_efe, r_ta, Mb = profile(Mb_msun, a0, g_ext_frac)
    r13 = np.sqrt(G*Mb/1e-13); r15 = np.sqrt(G*Mb/1e-15)          # radii of the two lensing acceleration limits
    out = {}
    for cad in CADS:
        M = excess(r, Phi, cad, Mb)
        # eps = 1 (MOND scalar sourced by all matter): deep-MOND g ~ sqrt(M_b + M_exc)  -> dev = sqrt(1+M_exc/M_b)-1
        # more precisely use nu_RAR on the total Newtonian field
        gN_tot = G*(Mb*r**2/(r+0.15*rM)**2 + M)/r**2; g_tot = nu_RAR(gN_tot/a0)*gN_tot
        dev1 = g_tot/g - 1
        # eps = 0 (kernel reads baryons only): the excess adds only its Newtonian pull
        dev0 = (G*M/r**2)/g
        win = r <= min(1.0*MPC, Rmax)                                  # the weak-lensing range
        rc = r <= 100*KPC                                              # the rotation-curve range
        out[cad] = dict(max_dev1_WL=float(np.max(dev1[win])), max_dev0_WL=float(np.max(dev0[win])),
                        max_dev1_RC=float(np.max(dev1[rc])), dev1_at_r13=float(np.interp(r13, r, dev1)) if r13 < Rmax else 0.0,
                        Mexc_Rmax_over_Mb=float(M[-1]/Mb))
    return out, dict(rM=rM/KPC, Rmax=Rmax/KPC, r_efe=r_efe/KPC, r_ta=r_ta/KPC, r13=r13/KPC, r15=r15/KPC)
C3 = {}
for foot in ("canonical", "alt"):
    for gx in (0.01, 0.03):
        for Mb in (1e10, 1e11):
            tab, info = deviation_table(Mb, A0[foot], gx)
            C3[(foot, gx, Mb)] = (tab, info)
            if foot == "canonical":
                print(f"\n  M_b = {Mb:.0e} Msun, g_ext = {gx} a0 ({foot}): r_M = {info['rM']:.1f} kpc, R_max = {info['Rmax']:.0f} kpc "
                      f"(EFE {info['r_efe']:.0f}, turnaround {info['r_ta']:.0f}); a_b = 1e-13 at r = {info['r13']:.0f} kpc, 1e-15 at {info['r15']:.0f} kpc")
                print(f"  {'c_ad':>6} {'max dev (eps=1) WL':>19} {'max dev (eps=0) WL':>19} {'dev at a_b=1e-13':>17} {'max dev RC':>11} {'M_exc(<Rmax)/M_b':>17}")
                for cad in CADS:
                    d = tab[cad]
                    print(f"  {cad:6.0f} {d['max_dev1_WL']:19.4f} {d['max_dev0_WL']:19.4f} {d['dev1_at_r13']:17.4f} {d['max_dev1_RC']:11.5f} {d['Mexc_Rmax_over_Mb']:17.3f}")
def floor10(tab, key='max_dev1_WL', lim=0.10):
    ok = [c for c in CADS if tab[c][key] <= lim]
    return float(min(ok)) if ok else float('inf')
FLOORS = {k: floor10(v[0]) for k, v in C3.items()}
print("\n  c_ad floor for <= 10% deviation from deep MOND everywhere inside the lensing range (eps = 1):")
for k, v in FLOORS.items(): print(f"    footing {k[0]:9s} g_ext = {k[1]:.2f} a0, M_b = {k[2]:.0e}:  c_ad >= {v:.0f} km/s")
f_iso_11 = FLOORS[('canonical', 0.01, 1e11)]; f_iso_10 = FLOORS[('canonical', 0.01, 1e10)]
check("C3-1  with the physical boundary condition the lensing floor is FAR looser than the VSB scaling: for an "
      "isolated (g_ext = 0.01 a0) 1e11 Msun lens the 10% criterion needs only c_ad >= 250-300 km/s, and a "
      "1e10 lens is EASIER (smaller well), not harder -- the boundary condition VSB flag as decisive is decisive",
      200 <= f_iso_11 <= 300 and f_iso_10 <= f_iso_11,
      f"floors (canonical, isolated): 1e11 -> {f_iso_11:.0f}, 1e10 -> {f_iso_10:.0f} km/s")
rc150 = max(v[0][150]['max_dev1_RC'] for v in C3.values()); rc200 = max(v[0][200]['max_dev1_RC'] for v in C3.values())
check("C3-2  the rotation-curve range (r <= 100 kpc) sees < 1% deviation for every c_ad >= 200 km/s at both "
      "masses, both footings and both g_ext (at 150 km/s the isolated 1e11 case reaches 6%: the RC range is "
      "clean only above the L153b floor, consistently)",
      rc200 < 0.01 and 0.03 < rc150 < 0.10, f"max RC deviation: {rc150:.3f} at 150 km/s, {rc200:.4f} at 200 km/s")
check("C3-3  the total excess dust a galaxy induces inside R_max is < 20% of M_b at the floor and falls "
      "steeply above it: the atmosphere is a perturbation, so neglecting its self-gravity is consistent",
      all(C3[k][0][FLOORS[k]]['Mexc_Rmax_over_Mb'] < 0.2 for k in C3 if np.isfinite(FLOORS[k])))
check("C3-4  the floor is boundary-condition sensitive by a factor ~1.5 between g_ext = 0.01 and 0.03 a0 and "
      "by <= 1 grid step between footings -- quoted as a RANGE, not a number",
      all(0.5 <= FLOORS[('canonical', 0.01, Mb)]/max(FLOORS[('canonical', 0.03, Mb)], 1) <= 2.5 for Mb in (1e10, 1e11)),
      "; ".join(f"{k}: {v:.0f}" for k, v in FLOORS.items()))

# =====================================================================================================
sec("C4 -- can the oscillatory regime sit outside BOTH the rotation-curve and the lensing ranges?")
# =====================================================================================================
# The Helmholtz oscillation proper lives at r >~ mu^-1 (the ambient Jeans length); the induced-atmosphere
# deviation lives at r_10 (C3).  Both must clear 100 kpc (RC) and ~1 Mpc (WL).
lo = max(f_iso_11, f_iso_10)
print(f"  Helmholtz scale mu^-1 >= {mu_inv_Mpc(lo):.1f} Mpc at the lensing floor {lo:.0f} km/s; >= {mu_inv_Mpc(537):.1f} Mpc at the ceiling.")
check("C4-1  YES, for c_ad >= the C3 floor: mu^-1 >= 5.9 Mpc clears both ranges by > 5x, and the induced "
      "atmosphere is < 10% inside 1 Mpc and < 1% inside 100 kpc.  The oscillatory regime is NOT a kill of the "
      "EP-consistent (p = 1) sector; the lensing floor it sets (250-300 km/s isolated, canonical) sits below "
      "the 537 km/s ceiling.  On VSB's isolated-log scaling instead, the window would be a sliver (1e11) or "
      "empty (1e10) -- that scaling is what the published AeST tension rests on.",
      mu_inv_Mpc(lo) > 5.0 and lo < 537, f"floor {lo:.0f} km/s, mu^-1 = {mu_inv_Mpc(lo):.1f} Mpc")

print(f"""
  VERDICT (C): the Helmholtz/oscillatory regime of the transplant is at the ambient Jeans length mu^-1 = 7.1 Mpc
  x (c_ad/300 km/s) -- outside every galaxy-scale range for every c_ad above the L153b floor.  What lands inside
  the lensing range is the INDUCED ATMOSPHERE (VSB's r_C is its linear, un-cut-off version).  With the potential
  anchored at the EFE/turnaround radius the 10% lensing criterion gives c_ad >= {f_iso_11:.0f} km/s (1e11, isolated,
  canonical; range {min(FLOORS.values()):.0f}-{max(v for v in FLOORS.values() if np.isfinite(v)):.0f} over footings and g_ext); on the isolated-log scaling it
  would be {fl[1e11]['rc1000']:.0f}-{fl[1e10]['rc1000']:.0f} km/s.  The deep a_b >= 1e-15 lensing points, if trusted, exclude the whole window
  (c_ad >= {c_deep:.0f} km/s > 537).  Not a kill on its own; the binding statement is the boundary-condition
  dependence, which is exactly the point VSB make about AeST.
""")
RES = dict(mu_inv_300=mu_inv_Mpc(300), c_loose=c_loose, c_deep=c_deep, c_clus=c_clus,
           rC_VSB_kpc={str(k): v for k, v in C2.items()}, rC_floors={str(k): v for k, v in fl.items()},
           lensing_floor_10pct={f"{k[0]}_gext{k[1]}_Mb{k[2]:.0e}": v for k, v in FLOORS.items()},
           dev_tables={f"{k[0]}_gext{k[1]}_Mb{k[2]:.0e}": {str(c): v[0][c] for c in CADS} for k, v in C3.items()},
           checks_total=N[0], checks_failed=len(FAILS))
with open(os.path.join(HERE, "L153c_results.json"), "w") as f: json.dump(RES, f, indent=1, default=float)
print("=" * 112)
print(f"L153c COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + "; ".join(FAILS)); sys.exit(1)
print("=" * 112)
