#!/usr/bin/env python3
"""
g04i -- the galaxy-capture gate for the thermal relic: does a 28 eV relic end up inside the RAR radii?
=======================================================================================================
The N_eff argument (relayed OpenAI note, checked in g04g) pushes the relic completion to m = 11.2 eV/xi^3 with xi = T_x/T_nu ~ 0.74,
i.e. m ~ 28 eV, and predicts a galaxy phase-space core R_c ~ 52 kpc x Delta N_eff ~ 15 kpc.  The framework fits the RAR with baryons
and MOND alone, so any relic mass inside 10-30 kpc comparable to the baryons breaks its own galaxy sector.  Three questions, each a
check that can fail:

  C1 [cold?]       the relic's rms velocity v_rms(z) = 3.6 T_x(z)/m at z = 3-8 against the escape speed of a 5e10 Msun disc's MOND well
                   (v_flat = (G M_b a0)^1/4, log potential truncated by the 0.02 a0 external field): v_rms < 0.15 v_esc(10 kpc) means the
                   relic falls in like cold dark matter once galaxies form;
  C2 [phase space] the Tremaine-Gunn/Liouville ceiling inside the well, rho_max(r) = (g/2h^3) m^4 (4 pi/3) v_esc(r)^3, integrated inside
                   10, 20, 30 kpc, in units of the baryonic mass, for m = 28 eV (and 11.4 eV as the reference): protection means the ceiling
                   holds the relic below 25% of the baryons inside 10 kpc; the pincer is that 11.4 eV is protected and 28 eV is not;
  C3 [dynamics]    g03r's cold collisionless infall of the cosmic share onto the assembling 5e10 disc with the MOND field on the peculiar
                   field (the relic is cold by C1, so the shells are the relic): the captured mass inside 10, 30 and 100 kpc in units of
                   the baryons, at both footings, capped by the C2 ceiling;
  C4 [verdict]     the relic mass inside 10 kpc (dynamics capped by phase space) exceeds 25% of the baryons -> the galaxy gate FAILS for
                   28 eV; the mass at which the ceiling would restore protection (M_TG(<10 kpc) = 0.25 M_b) is reported against the N_eff
                   floor 27.6 eV -- the width of the pincer.

OUTCOME (2026-09-06 run): C1 PASS (v_rms/v_esc = 0.10); C2 FAIL of its own threshold -- 11.4 eV gives 0.28/0.31 M_b inside 10 kpc, just above 0.25, while
27.6 eV gives 9.7/10.8; C3 PASS (cold infall delivers 2.7/3.3 M_b inside 10 kpc); C4 PASS (protection mass 11.1/10.8 eV, a factor 2.5 below the N_eff
floor).  The galaxy gate fails for the N_eff-compatible relic at both footings; the light reference relic is itself only marginally protected.
"""
import numpy as np, math, json, sys, time, importlib.util
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
T0 = time.time()
G = 6.674e-11; c = 2.998e8; hpl = 6.626e-34; kB = 1.381e-23; eV = 1.602e-19; MSUN = 1.989e30; kpc = 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}; Mb = 5e10*MSUN; xi = 0.74; m_eV = 11.2/xi**3; m = m_eV*eV/c**2; gdeg = 2
Tnu0 = 1.945*kB; v_rms = lambda z: 3.6*xi*Tnu0*(1 + z)/(m*c)
print("=" * 110); print(f"g04i -- galaxy capture of the thermal relic: m = 11.2 eV/xi^3 = {m_eV:.1f} eV at xi = {xi}"); print("=" * 110, flush=True)
# ---- C1: the well and the relic's velocity ----
def well_speeds(a0):
    vf = (G*Mb*a0)**0.25; gext = 0.02*a0; r_efe = vf**2/gext                                              # MOND log potential out to where the field falls to the external field
    def vesc(r): return math.sqrt(2*vf**2*math.log(r_efe/r) + 2*G*Mb/r*0) if r < r_efe else 0.0             # log potential (the Newtonian core adds little at >= 10 kpc for a 5e10 disc)
    return vf, r_efe, vesc
for foot, a0 in A0.items():
    vf, r_efe, vesc = well_speeds(a0)
    print(f"    {foot}: v_flat = {vf/1e3:.0f} km/s, external-field radius {r_efe/kpc:.0f} kpc, v_esc(10 kpc) = {vesc(10*kpc)/1e3:.0f} km/s, v_esc(30 kpc) = {vesc(30*kpc)/1e3:.0f} km/s; relic v_rms = {v_rms(8)/1e3:.0f} (z = 8), {v_rms(3)/1e3:.0f} (z = 3), {v_rms(0)/1e3:.1f} (z = 0) km/s", flush=True)
vf_c, _, vesc_c = well_speeds(A0["canonical"])
check("C1 [cold] at z = 3-8 the 28 eV relic's rms velocity is below 15% of the escape speed at 10 kpc: it falls in like cold dark matter once galaxies form", v_rms(8) < 0.15*vesc_c(10*kpc), f"v_rms(z=8)/v_esc(10 kpc) = {v_rms(8)/vesc_c(10*kpc):.2f}")
# ---- C2: the phase-space ceiling inside the well ----
def M_TG(m_kg, vesc, R):
    r = np.geomspace(0.1*kpc, R, 2000); rho = np.array([(gdeg/(2*hpl**3))*m_kg**4*(4*math.pi/3)*vesc(x)**3 for x in r])
    return float(np.trapz(4*math.pi*r**2*rho, r))
TGM = {}
for foot, a0 in A0.items():
    vf, r_efe, vesc = well_speeds(a0)
    for mm_eV in (m_eV, 11.37):
        mk = mm_eV*eV/c**2; TGM[(foot, mm_eV)] = [M_TG(mk, vesc, R*kpc)/Mb for R in (10, 20, 30)]
        print(f"    {foot}: m = {mm_eV:.1f} eV: phase-space ceiling on M_relic/M_b inside 10, 20, 30 kpc = {np.round(TGM[(foot, mm_eV)], 3).tolist()}", flush=True)
check("C2 [phase space, the pincer] the ceiling protects the RAR at 11.4 eV (M_TG(<10 kpc) < 0.25 M_b) but NOT at 28 eV (> 1 M_b), at both footings", all(TGM[(f, 11.37)][0] < 0.25 and TGM[(f, m_eV)][0] > 1.0 for f in A0), json.dumps({f: {"11.4": round(TGM[(f, 11.37)][0], 3), f"{m_eV:.1f}": round(TGM[(f, m_eV)][0], 2)} for f in A0}))
# ---- C3: dynamics (g03r's cold collisionless infall, MOND on the peculiar field) ----
spec = importlib.util.spec_from_file_location("g03r", "g03r_converged_collapse_adaptive_shells.py"); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
CAP = {}
for foot, a0 in A0.items():
    o = R.run("galaxy", 1e30, N=800, cs_fixed=0.0, a0=a0)                                                 # cold shells, MOND on the peculiar field (the field at 30 kpc is 80% established by z ~ 6.6, g03s)
    share = o["Mshare"]; Mavg = o["frac"]*share                                                            # apertures: 100 kpc and 10 kpc (g03r's run reports [R, 0.2 R] = [100, 20]? -> its apertures are R and 0.2 R)
    # g03r's apertures are (R, 0.2 R) = (100 kpc, 20 kpc); take M(<10 kpc) from the time-averaged profile
    r_prof, M_prof = o["prof"]; M10 = float(np.interp(10*kpc, r_prof, M_prof)); M30 = float(np.interp(30*kpc, r_prof, M_prof)); M100 = float(np.interp(100*kpc, r_prof, M_prof))
    vf, r_efe, vesc = well_speeds(a0); capped = [min(M10, M_TG(m, vesc, 10*kpc))/Mb, min(M30, M_TG(m, vesc, 30*kpc))/Mb, M100/Mb]
    CAP[foot] = dict(raw=[M10/Mb, M30/Mb, M100/Mb], capped=capped)
    print(f"    {foot}: cold-infall capture (g03r, N = 800, {o['secs']:.0f}s): M_relic/M_b inside 10, 30, 100 kpc = {np.round(CAP[foot]['raw'], 2).tolist()}; capped by phase space (28 eV): {np.round(capped, 2).tolist()}", flush=True)
check("C3 [dynamics] the cold infall delivers more than 25% of the baryonic mass inside 10 kpc at both footings (the RAR's tolerance)", all(CAP[f]["capped"][0] > 0.25 for f in A0), json.dumps({f: np.round(CAP[f]["capped"], 2).tolist() for f in A0}))
# ---- C4: verdict and the pincer's width ----
def m_protect(foot):
    vf, r_efe, vesc = well_speeds(A0[foot]); lo, hi = 5.0, 60.0
    for _ in range(40):
        mid = 0.5*(lo + hi)
        if M_TG(mid*eV/c**2, vesc, 10*kpc)/Mb > 0.25: hi = mid
        else: lo = mid
    return 0.5*(lo + hi)
MP = {f: m_protect(f) for f in A0}
print(f"    C4: the mass below which phase space keeps the relic under 25% of the baryons inside 10 kpc: {json.dumps({f: round(v, 1) for f, v in MP.items()})} eV; the N_eff floor is 27.6 eV (Delta N_eff <= 0.3) -- the pincer's width is a factor {27.6/max(MP.values()):.1f} in mass", flush=True)
check("C4 [verdict] the galaxy gate fails for the N_eff-compatible relic: the mass needed for phase-space protection lies below the 27.6 eV floor at both footings, and the delivered mass inside 10 kpc exceeds 25% of the baryons", all(MP[f] < 27.6 for f in A0) and all(CAP[f]["capped"][0] > 0.25 for f in A0), json.dumps({f: [round(MP[f], 1), round(CAP[f]["capped"][0], 2)] for f in A0}))
print(f"\n  caveats: spherical cold infall onto an assembling disc (g03r's model, MOND on the peculiar field with the 0.02 a0 external field); the ceiling uses the MOND log potential's escape speed truncated at the external-field radius; a relic that never collapses with the galaxy (nuHDM's smooth-background picture) is exactly what C3 tests and does not find; no relic thermal pressure beyond C1's cold verdict.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
